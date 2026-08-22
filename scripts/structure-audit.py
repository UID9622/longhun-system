#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系统 · 结构健康审计脚本
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
文化归属: 思想框架归龍魂核心思想层 (CC BY-NC-SA 4.0)
LAYER: engineering
DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷕贲-STRUCTURE-AUDIT-v1.0-UID9622
署名: UID9622（诸葛鑫·Lucky）

功能：
  - 扫描仓库顶层结构健康度
  - 检查目录命名合规性
  - 识别孤儿文件、重复文件名
  - 检查 README 与 .layer_tag 覆盖率
  - 输出 JSON/Markdown 报告
"""

import os
import re
import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

# 龍魂 DNA 生成
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def generate_dna(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    import hashlib
    h = hashlib.sha256(f"{prefix}|{ts}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{prefix}-{h}"


# 配置常量
MAX_TOP_DIRS = 30
MAX_TOP_SYMLINKS = 5
TOP_DIR_PATTERN = re.compile(r"^\d{2}_[a-z0-9-]+$")
SUBDIR_PATTERN = re.compile(r"^[a-z0-9_-]+$")
ORPHAN_AGE_DAYS = 90

# 中文、日文、韩文范围（CJK）
CJK_PATTERN = re.compile(r"[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]")

# 保留的顶层文件（不检查目录名）
ROOT_FILES_WHITELIST = {
    "README.md", "README.md.asc",
    "AGENTS.md", "AGENTS.md.asc",
    "LICENSE", "LICENSE.asc",
    "CHANGELOG.md", "CHANGELOG.md.asc",
    "ROADMAP.md", "ROADMAP.md.asc",
    "CONTRIBUTING.md", "CONTRIBUTING.md.asc",
    "CODE_OF_CONDUCT.md", "CODE_OF_CONDUCT.md.asc",
    "SECURITY.md", "SECURITY.md.asc",
    "TERMS_OF_SERVICE.md", "TERMS_OF_SERVICE.md.asc",
    "PRIVACY_POLICY.md", "PRIVACY_POLICY.md.asc",
    "ATTRIBUTION.md", "ATTRIBUTION.md.asc",
    "GOVERNANCE.md", "GOVERNANCE.md.asc",
    "GENTLEMANS_PROTOCOL.md", "GENTLEMANS_PROTOCOL.md.asc",
    "CONSTITUTION.md", "CONSTITUTION.md.asc",
    "CNSH-PROTOCOL.md", "CNSH-PROTOCOL.md.asc",
    "pyproject.toml", "pyproject.toml.asc",
    "install.sh", "install.sh.asc",
    ".gitignore", ".dockerignore", ".gitlab-ci.yml",
    ".env.example", ".env.example.asc",
    ".pre-commit-config.yaml", ".pre-commit-config.yaml.asc",
    ".bandit.yaml", ".bandit.yaml.asc",
    "__init__.py", ".inventory.json", ".inventory.json.asc",
    ".audit-whitelist", "audit_log.jsonl",
}

# 不应出现在根目录的文件/目录
ROOT_BLACKLIST_DIRS = {"__pycache__", ".git", ".pytest_cache", ".venv", ".venv_tts"}


def is_top_dir_compliant(name: str) -> bool:
    """顶层目录必须匹配 NN_english-name/ 格式"""
    return bool(TOP_DIR_PATTERN.match(name))


def is_subdir_compliant(name: str) -> bool:
    """子目录必须匹配英文小写/数字/下划线/连字符"""
    return bool(SUBDIR_PATTERN.match(name))


def contains_cjk(name: str) -> bool:
    return bool(CJK_PATTERN.search(name))


def get_file_age_days(path: Path) -> float:
    try:
        mtime = path.stat().st_mtime
        return (datetime.now().timestamp() - mtime) / 86400
    except Exception:
        return 0.0


class StructureAuditor:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.checks = []
        self.violations = []
        self.infos = []

    def add_check(self, name: str, status: str, value=None, threshold=None, message: str = ""):
        self.checks.append({
            "name": name,
            "status": status,
            "value": value,
            "threshold": threshold,
            "message": message,
        })

    def run(self) -> dict:
        # 顶层目录
        top_dirs = []
        top_symlinks = []
        top_files = []
        top_others = []

        for item in sorted(self.root.iterdir()):
            if item.name in ROOT_BLACKLIST_DIRS:
                continue
            try:
                if item.is_symlink():
                    top_symlinks.append(item)
                elif item.is_dir():
                    top_dirs.append(item)
                elif item.is_file():
                    top_files.append(item)
                else:
                    top_others.append(item)
            except PermissionError:
                continue

        # 检查 1：顶层目录数量
        dir_count = len(top_dirs)
        dir_status = "ok" if dir_count <= MAX_TOP_DIRS else "fail"
        self.add_check(
            "top_level_dir_count",
            dir_status,
            value=dir_count,
            threshold=MAX_TOP_DIRS,
            message=f"顶层目录数 {dir_count}，阈值 {MAX_TOP_DIRS}",
        )

        # 检查 2：顶层 Symlink 数量
        symlink_count = len(top_symlinks)
        symlink_status = "ok" if symlink_count <= MAX_TOP_SYMLINKS else "fail"
        self.add_check(
            "top_level_symlink_count",
            symlink_status,
            value=symlink_count,
            threshold=MAX_TOP_SYMLINKS,
            message=f"顶层 Symlink 数 {symlink_count}，阈值 {MAX_TOP_SYMLINKS}",
        )

        # 检查 3：顶层目录命名合规
        # 隐藏目录（.开头）为工具配置，单独记录但不强制 NN_english-name
        naming_violations = []
        hidden_dirs = []
        for d in top_dirs:
            if d.name.startswith("."):
                hidden_dirs.append(d.name)
                continue
            if not is_top_dir_compliant(d.name):
                reason = "格式不符"
                if contains_cjk(d.name):
                    reason = "包含中文/繁体/日文"
                naming_violations.append({"path": d.name, "reason": reason})

        self.add_check(
            "top_dir_naming_compliance",
            "ok" if not naming_violations else "fail",
            value={"violations": len(naming_violations), "hidden_dirs": len(hidden_dirs)},
            threshold=0,
            message=f"顶层目录命名违规 {len(naming_violations)} 个（隐藏工具目录 {len(hidden_dirs)} 个单独记录）",
        )
        if naming_violations:
            self.violations.append({
                "rule": "top_dir_naming",
                "details": naming_violations,
            })
        if hidden_dirs:
            self.infos.append({
                "type": "hidden_tool_dirs",
                "dirs": hidden_dirs,
            })

        # 检查 4：顶层文件命名合规
        file_violations = []
        for f in top_files:
            if f.name not in ROOT_FILES_WHITELIST:
                file_violations.append(f.name)

        self.add_check(
            "root_file_whitelist",
            "ok" if not file_violations else "warn",
            value=len(file_violations),
            message=f"根目录非白名单文件 {len(file_violations)} 个",
        )
        if file_violations:
            self.infos.append({
                "type": "root_unknown_files",
                "files": file_violations,
            })

        # 检查 5：Symlink 详情
        symlink_details = []
        for s in top_symlinks:
            try:
                target = os.readlink(s)
                symlink_details.append({"link": s.name, "target": target})
            except Exception as e:
                symlink_details.append({"link": s.name, "error": str(e)})

        self.add_check(
            "symlink_inventory",
            "ok",
            value=len(symlink_details),
            message=f"已盘点 {len(symlink_details)} 个 Symlink",
        )
        self.infos.append({
            "type": "symlink_details",
            "details": symlink_details,
        })

        # 检查 6：bin 目录规模与分类
        bin_dir = self.root / "bin"
        bin_files = []
        bin_subdirs = []
        if bin_dir.exists() and bin_dir.is_dir():
            for item in bin_dir.iterdir():
                if item.is_file():
                    bin_files.append(item.name)
                elif item.is_dir():
                    bin_subdirs.append(item.name)

        bin_classified = len(bin_subdirs) > 0
        self.add_check(
            "bin_classification",
            "ok" if bin_classified else "warn",
            value={"files": len(bin_files), "subdirs": bin_subdirs},
            message="bin/ 已分类" if bin_classified else "bin/ 尚未按功能域分类，建议拆分到 08_BIN/",
        )

        # 检查 7：孤儿文件扫描
        orphan_candidates = []
        for d in top_dirs:
            if d.name.startswith(("archive", "_archive", "_work", "logs")):
                continue
            for item in d.rglob("*"):
                if item.is_file():
                    age = get_file_age_days(item)
                    if age > ORPHAN_AGE_DAYS:
                        # 简单启发式：文件扩展名常见但未被引用
                        orphan_candidates.append({
                            "file": str(item.relative_to(self.root)),
                            "age_days": round(age, 1),
                        })

        # 只保留前 20 个最老的
        orphan_candidates.sort(key=lambda x: x["age_days"], reverse=True)
        orphan_candidates = orphan_candidates[:20]

        self.add_check(
            "orphan_file_scan",
            "ok" if not orphan_candidates else "warn",
            value=len(orphan_candidates),
            message=f"疑似孤儿文件（>{ORPHAN_AGE_DAYS}天未修改）{len(orphan_candidates)} 个",
        )
        if orphan_candidates:
            self.infos.append({
                "type": "orphan_candidates",
                "details": orphan_candidates,
            })

        # 检查 8：README 覆盖率
        dirs_without_readme = []
        for d in top_dirs:
            if not (d / "README.md").exists():
                dirs_without_readme.append(d.name)

        self.add_check(
            "readme_coverage",
            "ok" if not dirs_without_readme else "warn",
            value=len(dirs_without_readme),
            message=f"缺少 README.md 的顶层目录 {len(dirs_without_readme)} 个",
        )
        if dirs_without_readme:
            self.infos.append({
                "type": "dirs_without_readme",
                "dirs": dirs_without_readme,
            })

        # 检查 9：.layer_tag 覆盖率
        dirs_without_layer_tag = []
        for d in top_dirs:
            if not (d / ".layer_tag").exists():
                dirs_without_layer_tag.append(d.name)

        self.add_check(
            "layer_tag_coverage",
            "ok" if not dirs_without_layer_tag else "warn",
            value=len(dirs_without_layer_tag),
            message=f"缺少 .layer_tag 的顶层目录 {len(dirs_without_layer_tag)} 个",
        )
        if dirs_without_layer_tag:
            self.infos.append({
                "type": "dirs_without_layer_tag",
                "dirs": dirs_without_layer_tag,
            })

        # 检查 10：重复文件名
        filename_map = defaultdict(list)
        for d in top_dirs:
            for item in d.rglob("*"):
                if item.is_file():
                    filename_map[item.name].append(str(item.relative_to(self.root)))

        duplicates = {k: v for k, v in filename_map.items() if len(v) > 1}
        # 忽略常见通用名
        common_names = {
            "README.md", ".gitkeep", "__init__.py", ".layer_tag",
            "index.html", "style.css", "main.js", "main.py", "app.py",
            "config.json", "requirements.txt", "Dockerfile",
            ".DS_Store", "package.json", "tsconfig.json",
        }
        interesting_duplicates = {
            k: v for k, v in duplicates.items()
            if k not in common_names and len(v) >= 3
        }

        self.add_check(
            "duplicate_filenames",
            "ok" if not interesting_duplicates else "warn",
            value=len(interesting_duplicates),
            message=f"值得关注的重复文件名（≥3处且非通用名）{len(interesting_duplicates)} 个",
        )
        if interesting_duplicates:
            sample = dict(list(interesting_duplicates.items())[:10])
            self.infos.append({
                "type": "duplicate_filenames",
                "details": sample,
            })

        # 汇总状态
        statuses = [c["status"] for c in self.checks]
        overall = "ok"
        if "fail" in statuses:
            overall = "error"
        elif "warn" in statuses:
            overall = "warn"

        return {
            "dna": generate_dna("STRUCTURE-AUDIT"),
            "confirm_code": CONFIRM_CODE,
            "timestamp": _now(),
            "root": str(self.root),
            "status": overall,
            "summary": {
                "top_level_dirs": dir_count,
                "top_level_symlinks": symlink_count,
                "top_level_files": len(top_files),
                "top_level_others": len(top_others),
                "bin_files": len(bin_files),
                "bin_subdirs": bin_subdirs,
            },
            "checks": self.checks,
            "violations": self.violations,
            "infos": self.infos,
        }


def to_markdown(report: dict) -> str:
    lines = []
    lines.append(f"# 龍魂系统 · 结构健康审计报告")
    lines.append("")
    lines.append(f"> DNA: {report['dna']}")
    lines.append(f"> 时间: {report['timestamp']}")
    lines.append(f"> 根目录: `{report['root']}`")
    lines.append(f"> 总体状态: {'🟢' if report['status'] == 'ok' else '🟡' if report['status'] == 'warn' else '🔴'} {report['status'].upper()}")
    lines.append("")
    lines.append("## 摘要")
    lines.append("")
    lines.append("| 指标 | 数值 |")
    lines.append("|:---|---:|")
    for k, v in report["summary"].items():
        lines.append(f"| {k} | {v} |")
    lines.append("")
    lines.append("## 检查项")
    lines.append("")
    lines.append("| 检查项 | 状态 | 值 | 阈值 | 说明 |")
    lines.append("|:---|:---:|:---:|:---:|:---|")
    for c in report["checks"]:
        status_emoji = "🟢" if c["status"] == "ok" else "🟡" if c["status"] == "warn" else "🔴"
        val = c.get("value", "-")
        thr = c.get("threshold", "-")
        if isinstance(val, (list, dict)):
            val = json.dumps(val, ensure_ascii=False)
        if isinstance(thr, (list, dict)):
            thr = json.dumps(thr, ensure_ascii=False)
        lines.append(f"| {c['name']} | {status_emoji} {c['status']} | {val} | {thr} | {c['message']} |")
    lines.append("")

    if report["violations"]:
        lines.append("## 违规详情")
        lines.append("")
        for v in report["violations"]:
            lines.append(f"### {v['rule']}")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(v.get("details", []), ensure_ascii=False, indent=2))
            lines.append("```")
            lines.append("")

    if report["infos"]:
        lines.append("## 附加信息")
        lines.append("")
        for info in report["infos"]:
            lines.append(f"### {info['type']}")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(info.get("details", info), ensure_ascii=False, indent=2))
            lines.append("```")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="龍魂系统结构健康审计")
    parser.add_argument("--root", default=".", help="仓库根目录")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="输出格式")
    parser.add_argument("--output", default="-", help="输出文件（默认 stdout）")
    parser.add_argument("--fail-on-error", action="store_true", help="发现 fail 时退出码非零")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"错误：根目录不存在 {root}", file=sys.stderr)
        sys.exit(1)

    auditor = StructureAuditor(root)
    report = auditor.run()

    if args.format == "json":
        output = json.dumps(report, ensure_ascii=False, indent=2)
    else:
        output = to_markdown(report)

    if args.output == "-":
        print(output)
    else:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        print(f"报告已保存: {out_path}")

    if args.fail_on_error and report["status"] == "error":
        sys.exit(2)


if __name__ == "__main__":
    main()
