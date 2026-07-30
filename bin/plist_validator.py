#!/usr/bin/env python3
#龍芯⚡️2026-07-06-PLIST-VALIDATOR-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🧬 龍魂 plist 文件校验工具
DNA: #龍芯⚡️2026-07-06-PLIST-VALIDATOR-v1.0

功能:
- XML 格式完整性检查
- 必填字段验证（Label, ProgramArguments, RunAtLoad）
- 路径存在性检查（ProgramArguments 中的脚本路径）
- 权限建议（owner/group）
- 中文错误提示

用法:
  python3 bin/plist_validator.py <plist路径>
  python3 bin/plist_validator.py --auto  # 检查所有 launchd plist
"""

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from dataclasses import dataclass, field

# DNA
DNA = "#龍芯⚡️2026-07-06-PLIST-VALIDATOR-v1.0"
VERSION = "1.0"

HOME = Path.home()
LH_ROOT = HOME / "longhun-system"
LAUNCHD_DIRS = [
    HOME / "Library" / "LaunchAgents",
    Path("/Library/LaunchAgents"),
    Path("/Library/LaunchDaemons"),
]

# 中文错误提示映射表
CN_ERRORS = {
    "XML_PARSE": {
        "en": "plist XML parse error at line {line}",
        "cn": "plist 文件格式错误：第{line}行存在 XML 语法错误，请检查标签闭合与特殊字符转义"
    },
    "MISSING_LABEL": {
        "en": "Missing required key: Label",
        "cn": "plist 文件缺少必填字段：Label（服务标识名称）"
    },
    "MISSING_PROGRAM": {
        "en": "Missing required key: ProgramArguments",
        "cn": "plist 文件缺少必填字段：ProgramArguments（启动命令路径）"
    },
    "SCRIPT_NOT_FOUND": {
        "en": "Script not found: {path}",
        "cn": "plist 中的脚本路径不存在：{path}，请检查路径是否正确"
    },
    "SCRIPT_NOT_EXEC": {
        "en": "Script not executable: {path}",
        "cn": "plist 中的脚本不可执行：{path}，请运行 chmod +x {path}"
    },
    "PERMISSION_WARN": {
        "en": "Permission warning: should be owned by current user",
        "cn": "权限建议：plist 文件应归当前用户所有（当前属主: {owner}），建议运行 chown {user} {path}"
    },
    "LOAD_FAILED": {
        "en": "Load failed: {code}",
        "cn": "系统级服务加载失败（错误码: {code}）：请检查 plist 文件权限或尝试手动启动脚本。\n   常见原因：① plist 格式错误  ② 脚本路径不存在  ③ 脚本无可执行权限  ④ SIP 限制"
    },
    "WORKDIR_NOT_FOUND": {
        "en": "WorkingDirectory not found: {path}",
        "cn": "工作目录不存在：{path}，请检查 WorkingDirectory 配置"
    },
    "VALIDATION_PASS": {
        "en": "Validation passed",
        "cn": "plist 文件校验通过，所有字段完整且路径存在"
    },
}

@dataclass
class ValidationIssue:
    level: str  # error / warning
    code: str
    message: str
    detail: str = ""

@dataclass
class ValidationReport:
    file_path: str
    issues: list[ValidationIssue] = field(default_factory=list)
    plist_version: str = ""
    label: str = ""
    program_args: list[str] = field(default_factory=list)
    run_at_load: bool = False
    keep_alive: bool = False
    passed: bool = False

    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.level == "error")

    def warn_count(self) -> int:
        return sum(1 for i in self.issues if i.level == "warning")

    def is_valid(self) -> bool:
        return self.error_count() == 0


def resolve_path(plist_path: str) -> Path:
    """解析 plist 路径，支持 ~ 和相对路径"""
    p = Path(plist_path).expanduser()
    if not p.is_absolute():
        p = LH_ROOT / p
    return p.resolve()


def validate_xml(file_path: Path) -> tuple[ET.Element | None, str | None]:
    """验证 XML 格式，返回 root 和错误信息"""
    try:
        tree = ET.parse(str(file_path))
        return tree.getroot(), None
    except ET.ParseError as e:
        line = e.position[0] if hasattr(e, 'position') and e.position else "?"
        return None, CN_ERRORS["XML_PARSE"]["cn"].format(line=line)
    except Exception as e:
        return None, f"无法读取 plist 文件：{e}"


def find_value(root, key: str, parent_tag: str = "dict"):
    """在 plist dict 结构中查找 key 对应的 value"""
    # 遍历 dict 中的 key-value 对
    found = root.findall(f"./{parent_tag}/key")
    for k in found:
        if k.text == key:
            # 下一个兄弟元素就是 value
            # 简单但可靠的方式：找紧跟 key 后面的元素
            for elem in root.findall(f"./{parent_tag}/*"):
                if elem.tag == "key" and elem.text == key:
                    idx = list(elem.getparent()).index(elem)
                    next_elem = list(elem.getparent())[idx + 1] if idx + 1 < len(list(elem.getparent())) else None
                    return next_elem
    return None


def walk_dict(root):
    """将 plist dict 转换为 Python 字典（简化版）"""
    result = {}
    if root.tag not in ("dict", "array"):
        # 可能是根元素下的 plist/dict 结构
        dict_elem = root.find(".//dict")
        if dict_elem is None:
            return result
        root = dict_elem

    children = list(root)
    i = 0
    while i < len(children) - 1:
        item = children[i]
        if item.tag == "key":
            key = item.text
            value = children[i + 1]
            if value.tag == "string":
                result[key] = value.text or ""
            elif value.tag == "true":
                result[key] = True
            elif value.tag == "false":
                result[key] = False
            elif value.tag == "integer":
                result[key] = int(value.text or 0)
            elif value.tag == "array":
                array_vals = []
                for child in list(value):
                    if child.tag == "string":
                        array_vals.append(child.text or "")
                result[key] = array_vals
            elif value.tag == "dict":
                result[key] = walk_dict(value)
            i += 2
        else:
            i += 1
    return result


def validate_plist(plist_path: str) -> ValidationReport:
    """主校验函数"""
    file_path = resolve_path(plist_path)
    report = ValidationReport(file_path=str(file_path))

    # 1. 文件存在性
    if not file_path.exists():
        report.issues.append(ValidationIssue("error", "NOT_FOUND",
            f"文件不存在：{file_path}"))
        return report

    if not file_path.is_file():
        report.issues.append(ValidationIssue("error", "NOT_FILE",
            f"路径不是文件：{file_path}"))
        return report

    report.file_path = str(file_path)

    # 2. XML 解析
    root, xml_err = validate_xml(file_path)
    if xml_err:
        report.issues.append(ValidationIssue("error", "XML_PARSE", xml_err))
        return report

    # 3. 提取内容
    plist_data = walk_dict(root)

    # 4. 必填字段检查
    report.label = plist_data.get("Label", "")
    if not report.label:
        report.issues.append(ValidationIssue("error", "MISSING_LABEL",
            CN_ERRORS["MISSING_LABEL"]["cn"]))

    report.program_args = plist_data.get("ProgramArguments", [])
    if not report.program_args:
        report.issues.append(ValidationIssue("error", "MISSING_PROGRAM",
            CN_ERRORS["MISSING_PROGRAM"]["cn"]))

    report.run_at_load = plist_data.get("RunAtLoad", False)
    report.keep_alive = plist_data.get("KeepAlive", False)

    # 5. 路径存在性检查
    for arg in report.program_args:
        if arg.endswith(".sh") or arg.endswith(".py"):
            script_path = Path(arg).expanduser()
            if not script_path.is_absolute():
                script_path = LH_ROOT / arg
            if not script_path.exists():
                report.issues.append(ValidationIssue("error", "SCRIPT_NOT_FOUND",
                    CN_ERRORS["SCRIPT_NOT_FOUND"]["cn"].format(path=script_path)))
            elif not os.access(str(script_path), os.X_OK):
                if script_path.suffix == ".sh" or script_path.suffix == ".py":
                    report.issues.append(ValidationIssue("warning", "SCRIPT_NOT_EXEC",
                        CN_ERRORS["SCRIPT_NOT_EXEC"]["cn"].format(path=script_path)))

    # 6. WorkingDirectory 检查
    workdir = plist_data.get("WorkingDirectory", "")
    if workdir:
        wd_path = Path(workdir).expanduser()
        if not wd_path.exists():
            report.issues.append(ValidationIssue("warning", "WORKDIR_NOT_FOUND",
                CN_ERRORS["WORKDIR_NOT_FOUND"]["cn"].format(path=workdir)))

    # 7. 权限检查
    try:
        st = file_path.stat()
        import pwd
        owner = pwd.getpwuid(st.st_uid).pw_name
        current_user = os.environ.get("USER", os.environ.get("LOGNAME", "unknown"))
        if owner != current_user and owner != "root":
            report.issues.append(ValidationIssue("warning", "PERMISSION_WARN",
                CN_ERRORS["PERMISSION_WARN"]["cn"].format(
                    owner=owner, user=current_user, path=file_path)))
    except Exception:
        pass

    # 8. 判定
    report.passed = report.is_valid()

    return report


def format_report(report: ValidationReport) -> str:
    """格式化输出校验报告"""
    lines = []
    status_icon = "🟢" if report.passed else "🔴"

    lines.append("")
    lines.append("╔═══════════════════════════════════════════════════════════╗")
    lines.append(f"║  🧬 龍魂 plist 文件校验 · {DNA.split('-')[2]}                ║")
    lines.append("╠═══════════════════════════════════════════════════════════╣")
    lines.append(f"║  文件: {report.file_path[:50]}")
    if report.label:
        lines.append(f"║  服务: {report.label[:50]}")
    lines.append(f"║  程序: {' '.join(report.program_args[:2])[:45]}")
    lines.append(f"║  自启: {'✅ 是' if report.run_at_load else '❌ 否'}  | 守护: {'✅ 是' if report.keep_alive else '❌ 否'}")
    lines.append("╠═══════════════════════════════════════════════════════════╣")

    if not report.issues:
        lines.append(f"║  {status_icon} {CN_ERRORS['VALIDATION_PASS']['cn'][:47]}║")
    else:
        for issue in report.issues:
            icon = "🔴" if issue.level == "error" else "🟡"
            lines.append(f"║  {icon} [{issue.code}] {issue.message[:45]}")

    lines.append("╠═══════════════════════════════════════════════════════════╣")
    lines.append(f"║  错误: {report.error_count()}  警告: {report.warn_count()}  {'✅ 通过' if report.passed else '🔴 未通过'}")
    lines.append("╚═══════════════════════════════════════════════════════════╝")

    return "\n".join(lines)


def find_all_plists() -> list[Path]:
    """查找所有龍魂相关 plist 文件"""
    found = []
    for d in LAUNCHD_DIRS:
        if d.exists():
            for f in d.glob("com.longhun.*.plist"):
                found.append(f)
    # 也检查项目中的
    project_plist = LH_ROOT / "launchd" / "com.longhun.symbiote.plist"
    if project_plist.exists() and project_plist not in found:
        found.append(project_plist)
    return found


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        print("\n用法:")
        print("  python3 bin/plist_validator.py <plist路径>      # 校验单个 plist")
        print("  python3 bin/plist_validator.py --auto           # 自动查找并校验所有")
        print("  python3 bin/plist_validator.py --json <路径>    # JSON 输出")
        sys.exit(0)

    # JSON 模式
    json_output = False
    if sys.argv[1] == "--json":
        json_output = True
        if len(sys.argv) < 3:
            print("❌ --json 需要指定路径", file=sys.stderr)
            sys.exit(1)
        file_arg = sys.argv[2]
    else:
        file_arg = sys.argv[1]

    # 自动模式
    if file_arg == "--auto":
        import json
        plists = find_all_plists()
        if not plists:
            print("⚠️  未找到龍魂 plist 文件")
            return

        all_reports = []
        for p in plists:
            report = validate_plist(str(p))
            all_reports.append(report)
            print(format_report(report))

        total_errors = sum(r.error_count() for r in all_reports)
        if total_errors > 0:
            sys.exit(1)
        return

    # 单文件校验
    report = validate_plist(file_arg)

    if json_output:
        import json
        output = {
            "dna": DNA,
            "file_path": report.file_path,
            "label": report.label,
            "program_args": report.program_args,
            "run_at_load": report.run_at_load,
            "keep_alive": report.keep_alive,
            "error_count": report.error_count(),
            "warn_count": report.warn_count(),
            "passed": report.passed,
            "issues": [
                {"level": i.level, "code": i.code, "message": i.message}
                for i in report.issues
            ]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(format_report(report))

    if not report.passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
