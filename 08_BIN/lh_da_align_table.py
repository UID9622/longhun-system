#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·乙卯·申时·䷀乾-DA-ALIGN-TABLE-AUTO-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 DA 对齐表 · 自动索引引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙卯·申时·䷀乾-DA-ALIGN-TABLE-AUTO-v1.0

设计哲学:
  不是手写表格，是自动从系统里"长出来"的对齐表。
  任何新模块、新映射、新规范加入时，运行一次就能自动补全。
  老百姓能懂、精英能懂、任何人都能懂——因为它是活的，不是死的。

对齐维度（可无限扩展）:
  1. 命名规范 — 字段/函数/文件命名统一
  2. 层级结构 — L0-L9 分层与嵌套规范
  3. 数据类型 — 类型安全与解析标准
  4. 原子性 — 最小不可分单元
  5. 可扩展性 — 预留字段与版本管理
  6+ ... 后续可通过 registry 自动扩展

用法:
  python3 bin/lh_da_align_table.py scan      # 扫描当前系统对齐状态
  python3 bin/lh_da_align_table.py report    # 生成对齐报告
  python3 bin/lh_da_align_table.py json      # 输出 JSON（给其他引擎调用）
  python3 bin/lh_da_align_table.py auto-fix  # 自动修复可修复项
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
ALIGN_REGISTRY = ROOT / "L7_数据层" / "da_align_registry.json"
ALIGN_CHAIN = ROOT / "L7_数据层" / "da_align_chain.jsonl"


# ═══════════════════════════════════════════════════════════════
# 对齐维度定义（可扩展 — 新增维度只需在此数组中追加）
# ═══════════════════════════════════════════════════════════════

ALIGN_DIMENSIONS: list[dict[str, Any]] = [
    {
        "id": "DA-001",
        "dimension": "命名规范",
        "core_indicator": "字段命名一致性",
        "acceptance_criteria": "统一采用 snake_case 或 camelCase；禁止中英文混用；标签名需具备明确语义",
        "check_pattern": "snake_or_camel",
        "auto_fixable": False,
        "scope": ["python", "json", "html_id", "css_class"],
    },
    {
        "id": "DA-002",
        "dimension": "层级结构",
        "core_indicator": "嵌套与扁平化",
        "acceptance_criteria": "复杂数据需采用合理的嵌套结构（如 metadata 包裹）；扁平数据需确保键值对独立，避免大段文本堆砌",
        "check_pattern": "structure_depth",
        "auto_fixable": False,
        "scope": ["json", "yaml", "toml"],
    },
    {
        "id": "DA-003",
        "dimension": "数据类型",
        "core_indicator": "类型安全与解析",
        "acceptance_criteria": "显式声明数据类型（String, Date, Int）；时间格式强制遵循 ISO 8601 标准；坐标采用标准经纬度格式",
        "check_pattern": "type_safety",
        "auto_fixable": True,
        "scope": ["python", "json"],
    },
    {
        "id": "DA-004",
        "dimension": "原子性",
        "core_indicator": "最小不可分单元",
        "acceptance_criteria": "复合信息需拆分（如'浙江省杭州市'拆分为 province 和 city）；禁止在一个字段中存储多种维度的信息",
        "check_pattern": "atomicity",
        "auto_fixable": False,
        "scope": ["json", "python"],
    },
    {
        "id": "DA-005",
        "dimension": "可扩展性",
        "core_indicator": "预留字段与版本",
        "acceptance_criteria": "包含 version 字段；预留 extra 或 metadata 扩展节点，确保未来新增字段不破坏现有结构",
        "check_pattern": "extensibility",
        "auto_fixable": True,
        "scope": ["json", "yaml", "toml"],
    },
    # ——— 龍魂系统专属对齐维度（从 AGENTS.md 锚点自动派生）———
    {
        "id": "DA-006",
        "dimension": "DNA 追溯",
        "core_indicator": "每个文件/模块绑定 DNA",
        "acceptance_criteria": "所有 .py/.md/.html 文件包含有效 DNA 追溯码；格式符合 v∞ 干支卦规范",
        "check_pattern": "dna_trace",
        "auto_fixable": True,
        "scope": ["python", "markdown", "html"],
    },
    {
        "id": "DA-007",
        "dimension": "三色审计",
        "core_indicator": "输出内容过三色闸",
        "acceptance_criteria": "所有对外输出/决策经过三色审计；🟢🟡🔴 判定有据可查",
        "check_pattern": "tricolor_audit",
        "auto_fixable": False,
        "scope": ["python", "markdown"],
    },
    {
        "id": "DA-008",
        "dimension": "繁简归一",
        "core_indicator": "龍字规范化",
        "acceptance_criteria": "「龍」繁体为规范形式；「龙」简体等价接收自动归一，不熔断",
        "check_pattern": "cnsh_char",
        "auto_fixable": True,
        "scope": ["python", "markdown", "html", "json"],
    },
]


# ═══════════════════════════════════════════════════════════════
# 扫描引擎
# ═══════════════════════════════════════════════════════════════

def find_checkable_files() -> list[Path]:
    """找到所有可检查文件"""
    ignore = {".git", "__pycache__", ".venv", "node_modules", "brain", ".obsidian",
              "models", "releases", "L7_数据层/desktop_archive", "L7_数据层/desktop_media",
              ".codebuddy/memory", "cnsh/terminal/downloads-imports"}
    files = []
    for p in ROOT.rglob("*"):
        if p.is_file() and p.stat().st_size < 2 * 1024 * 1024:
            s = str(p)
            if any(f"/{ig}" in s or s.startswith(str(ROOT / ig)) for ig in ignore):
                continue
            if p.suffix.lower() in {".py", ".md", ".html", ".css", ".js", ".json", ".yaml", ".yml", ".toml"}:
                files.append(p)
    return files


def check_naming(filepath: Path) -> dict[str, Any]:
    """DA-001: 命名规范检查"""
    issues = []
    filename = filepath.stem
    # 检查文件名是否有中英混用
    has_cn = bool(re.search(r'[\u4e00-\u9fff]', filename))
    has_en = bool(re.search(r'[a-zA-Z]', filename))
    if has_cn and has_en:
        # 中英混用文件名 — 在龍魂系统中可能是合理的（CNSH命名），标记为信息
        issues.append({"level": "info", "msg": f"文件名中英混用: {filename}（CNSH命名可能合理）"})

    # Python 文件额外检查
    if filepath.suffix == ".py":
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception:
            return {"dimension_id": "DA-001", "status": "🟡", "issues": [{"level": "warn", "msg": "无法读取文件"}]}
        # 检查是否有裸 dict 类型注解（已知类型错误模式）
        if re.search(r'->\s*dict\s*:', content) or re.search(r':\s*dict\s*=', content):
            issues.append({"level": "warn", "msg": "存在裸 dict 类型注解（应为 Dict[str, Any]）"})

    status = "🟢" if not issues or all(i["level"] == "info" for i in issues) else "🟡"
    return {"dimension_id": "DA-001", "status": status, "issues": issues}


def check_type_safety(filepath: Path) -> dict[str, Any]:
    """DA-003: 类型安全检查"""
    issues = []
    if filepath.suffix == ".py":
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception:
            return {"dimension_id": "DA-003", "status": "🟡", "issues": [{"level": "warn", "msg": "无法读取文件"}]}

        # 检查 Optional 无守卫模式
        optional_vars = re.findall(r'(\w+)\s*:\s*(?:Optional\[|.*\| None)', content)
        for var in optional_vars:
            # 检查是否有 assert xxx is not None 守卫
            guard_pattern = rf'assert\s+self\.{var}\s+is\s+not\s+None'
            if re.search(guard_pattern, content):
                continue
            # 检查是否有 if xxx is not None 守卫
            guard_pattern2 = rf'if\s+self\.{var}\s+is\s+not\s+None'
            if re.search(guard_pattern2, content):
                continue
            # 只在 Optional 变量被实际使用时才报告
            if re.search(rf'self\.{var}\.', content):
                issues.append({"level": "warn", "msg": f"Optional 变量 self.{var} 可能缺少 None 守卫"})

    status = "🟢" if not issues else "🟡"
    return {"dimension_id": "DA-003", "status": status, "issues": issues}


def check_extensibility(filepath: Path) -> dict[str, Any]:
    """DA-005: 可扩展性检查"""
    issues = []
    if filepath.suffix == ".json":
        try:
            data = json.loads(filepath.read_text(encoding="utf-8"))
        except Exception:
            return {"dimension_id": "DA-005", "status": "🟡", "issues": [{"level": "warn", "msg": "JSON 解析失败"}]}

        if isinstance(data, dict):
            if "version" not in data:
                issues.append({"level": "info", "msg": "JSON 文件缺少 version 字段"})
            if "metadata" not in data and "extra" not in data:
                issues.append({"level": "info", "msg": "JSON 文件缺少 metadata/extra 扩展节点"})

    status = "🟢" if not issues else "🟡"
    return {"dimension_id": "DA-005", "status": status, "issues": issues}


def check_dna_trace(filepath: Path) -> dict[str, Any]:
    """DA-006: DNA 追溯检查"""
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return {"dimension_id": "DA-006", "status": "🟡", "issues": [{"level": "warn", "msg": "无法读取文件"}]}

    dna_pattern = re.compile(r'#龍芯⚡️')
    new_dna_pattern = re.compile(r'#龍芯⚡️[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]·')
    old_dna_pattern = re.compile(r'#龍芯⚡️\d{4}-\d{2}-\d{2}-')

    if not dna_pattern.search(content):
        # 非关键文件（如 CSS、小型数据文件）可以没有 DNA
        if filepath.suffix in {".css", ".js"}:
            return {"dimension_id": "DA-006", "status": "🟢", "issues": []}
        issues.append({"level": "info", "msg": "文件缺少 DNA 追溯码"})

    if old_dna_pattern.search(content) and not new_dna_pattern.search(content):
        issues.append({"level": "warn", "msg": "存在旧版格里历 DNA 格式（应为 v∞ 干支卦格式）"})

    status = "🟢" if not issues else ("🟡" if all(i["level"] == "info" for i in issues) else "🔴")
    return {"dimension_id": "DA-006", "status": status, "issues": issues}


def check_cnsh_char(filepath: Path) -> dict[str, Any]:
    """DA-008: 繁简归一检查"""
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return {"dimension_id": "DA-008", "status": "🟡", "issues": [{"level": "warn", "msg": "无法读取文件"}]}

    # 检查是否使用简体「龙」而非繁体「龍」
    if '龍魂' in content:
        issues.append({"level": "warn", "msg": "使用了简体「龍魂」应为繁体「龍魂」"})

    status = "🟢" if not issues else "🟡"
    return {"dimension_id": "DA-008", "status": status, "issues": issues}


# ═══════════════════════════════════════════════════════════════
# 扫描调度
# ═══════════════════════════════════════════════════════════════

CHECK_MAP = {
    "DA-001": check_naming,
    "DA-003": check_type_safety,
    "DA-005": check_extensibility,
    "DA-006": check_dna_trace,
    "DA-008": check_cnsh_char,
}


def scan_all(files: list[Path] | None = None) -> dict[str, Any]:
    """全维度扫描"""
    if files is None:
        files = find_checkable_files()

    results: dict[str, Any] = {
        "meta": {
            "tool": "lh_da_align_table",
            "version": "v1.0",
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "total_files": len(files),
            "dimensions": len(ALIGN_DIMENSIONS),
        },
        "dimensions": [],
        "summary": {"🟢": 0, "🟡": 0, "🔴": 0},
    }

    # 限制扫描文件数（快速模式）
    sample_files = files[:200] if len(files) > 200 else files

    for dim in ALIGN_DIMENSIONS:
        dim_id = dim["id"]
        checker = CHECK_MAP.get(dim_id)

        dim_result = {
            "id": dim_id,
            "dimension": dim["dimension"],
            "core_indicator": dim["core_indicator"],
            "acceptance_criteria": dim["acceptance_criteria"],
            "auto_fixable": dim["auto_fixable"],
            "files_checked": 0,
            "status": "🟢",
            "issues_summary": [],
        }

        if checker:
            file_issues = []
            for f in sample_files:
                result = checker(f)
                if result.get("issues"):
                    file_issues.append({"file": str(f.relative_to(ROOT)), "issues": result["issues"]})
            dim_result["files_checked"] = len(sample_files)
            dim_result["issues_summary"] = file_issues[:20]  # 限制输出
            if file_issues:
                has_warn = any(any(i["level"] == "warn" for i in fi["issues"]) for fi in file_issues)
                dim_result["status"] = "🟡" if has_warn else "🟢"
        else:
            dim_result["files_checked"] = 0
            dim_result["status"] = "🟡"
            dim_result["issues_summary"] = [{"msg": "检查器未实现（待扩展）"}]

        results["dimensions"].append(dim_result)
        results["summary"][dim_result["status"]] += 1

    return results


def save_registry(results: dict[str, Any]) -> str:
    """保存对齐注册表到 JSON"""
    ALIGN_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    results["meta"]["saved_at"] = datetime.now(timezone.utc).isoformat()
    with open(ALIGN_REGISTRY, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 追加入链
    chain_entry = {
        "type": "da_align_scan",
        "timestamp": results["meta"]["saved_at"],
        "summary": results["summary"],
        "dna": f"#龍芯⚡️丙午·丙申·乙卯·申时·䷀乾-DA-ALIGN-SCAN-{hashlib.sha256(str(results['summary']).encode()).hexdigest()[:8].upper()}",
    }
    with open(ALIGN_CHAIN, "a", encoding="utf-8") as f:
        f.write(json.dumps(chain_entry, ensure_ascii=False) + "\n")

    return str(ALIGN_REGISTRY)


def format_markdown_table(results: dict[str, Any]) -> str:
    """生成 Markdown 对齐表"""
    lines = []
    lines.append("# 🐉 龍魂 DA 对齐表 · 自动索引")
    lines.append("")
    lines.append(f"> 扫描时间: {results['meta']['scanned_at']}")
    lines.append(f"> 扫描文件: {results['meta']['total_files']} 个")
    lines.append(f"> 对齐维度: {results['meta']['dimensions']} 个")
    lines.append(f"> 🟢 {results['summary']['🟢']} · 🟡 {results['summary']['🟡']} · 🔴 {results['summary']['🔴']}")
    lines.append("")
    lines.append("> 💡 此表格由 `bin/lh_da_align_table.py` 自动生成。新增对齐维度只需在脚本中追加定义。")
    lines.append("")
    lines.append("| 检查维度 | 核心指标 | 验收标准 | 状态 | 可自动修复 |")
    lines.append("| :--- | :--- | :--- | :---: | :---: |")

    for dim in results["dimensions"]:
        auto = "✅" if dim["auto_fixable"] else "—"
        lines.append(
            f"| {dim['dimension']} | {dim['core_indicator']} | {dim['acceptance_criteria']} | {dim['status']} | {auto} |"
        )

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 详细信息")
    lines.append("")

    for dim in results["dimensions"]:
        if dim["issues_summary"]:
            lines.append(f"### {dim['id']} — {dim['dimension']} {dim['status']}")
            lines.append("")
            for item in dim["issues_summary"][:10]:
                if isinstance(item, dict) and "file" in item:
                    lines.append(f"- `{item['file']}`")
                    for iss in item.get("issues", [])[:3]:
                        lines.append(f"  - {iss.get('level', '?')}: {iss.get('msg', '')}")
                elif isinstance(item, dict):
                    lines.append(f"- {item.get('msg', '')}")
            if len(dim["issues_summary"]) > 10:
                lines.append(f"- ... 还有 {len(dim['issues_summary']) - 10} 条")
            lines.append("")

    lines.append("---")
    lines.append(f"\n> DNA: `#龍芯⚡️丙午·丙申·乙卯·申时·䷀乾-DA-ALIGN-TABLE-AUTO-v1.0`")
    lines.append("> 龍魂系统 · DA 对齐表自动索引引擎 · 活文档 · 自动更新")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python3 bin/lh_da_align_table.py [scan|report|json|auto-fix]")
        return 1

    action = sys.argv[1]

    if action == "scan":
        print("🐉 龍魂 DA 对齐表 · 扫描中...")
        results = scan_all()
        registry_path = save_registry(results)
        print(f"✅ 扫描完成: {results['summary']}")
        print(f"   注册表: {registry_path}")

    elif action == "report":
        print("🐉 龍魂 DA 对齐表 · 生成报告...")
        results = scan_all()
        save_registry(results)
        report = format_markdown_table(results)
        report_path = ROOT / "docs" / "DA_ALIGN_TABLE.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
        print(f"✅ 报告已生成: {report_path}")
        print(report)

    elif action == "json":
        results = scan_all()
        save_registry(results)
        print(json.dumps(results, ensure_ascii=False, indent=2))

    elif action == "auto-fix":
        print("🐉 龍魂 DA 对齐表 · 自动修复...")
        results = scan_all()
        fixed = 0

        # DA-008: 繁简归一自动修复
        for dim in results["dimensions"]:
            if dim["id"] == "DA-008" and dim["auto_fixable"]:
                for item in dim.get("issues_summary", []):
                    if isinstance(item, dict) and "file" in item:
                        filepath = ROOT / item["file"]
                        try:
                            content = filepath.read_text(encoding="utf-8")
                            if "龍魂" in content:
                                new_content = content.replace("龍魂", "龍魂")
                                filepath.write_text(new_content, encoding="utf-8")
                                fixed += 1
                                print(f"  ✅ 繁简归一: {item['file']}")
                        except Exception as e:
                            print(f"  ❌ 修复失败: {item['file']} — {e}")

        print(f"\n✅ 自动修复完成: {fixed} 处")
        save_registry(results)

    else:
        print(f"未知动作: {action}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
