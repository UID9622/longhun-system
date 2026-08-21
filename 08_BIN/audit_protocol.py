#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂协议审计节点 v1.0
DNA: #龍芯⚡️2026-08-21-AUDIT-PROTOCOL-v1.0
功能:
  读取 PROTOCOL_REGISTRY.md
  检查每条协议必备字段 / DNA格式 / 版本一致性
  写入 audit_log.jsonl，关联 DNA
"""

import re
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "08_BIN"))

REGISTRY_FILE = ROOT / "PROTOCOL_REGISTRY.md"
AUDIT_LOG     = ROOT / "audit_log.jsonl"

try:
    from lh_dna_ref_impl import generate as dna_generate
    DNA_OK = True
except ImportError:
    DNA_OK = False


# ────────────────────────────────────────────────
# 必备字段与规则
# ────────────────────────────────────────────────

REQUIRED_FIELDS = [
    "协议名称",
    "协议编号",
    "当前版本",
    "状态",
    "责任人",
    "生效日期",
    "最近变更",
    "DNA锚定",
    "协议范围",
    "核心规则",
    "存放位置",
    "审计周期",
]

VALID_STATUSES = {"🟢 活跃", "🟡 实验", "⚪ 弃用"}

# DNA 格式: #龍芯⚡️{date}-...
DNA_PATTERN = re.compile(
    r"#龍芯⚡️\d{4}-\d{2}-\d{2}-.+"
)

# 版本号格式: vX.Y
VERSION_PATTERN = re.compile(r"^v\d+\.\d+$")


# ────────────────────────────────────────────────
# 解析 PROTOCOL_REGISTRY.md
# ────────────────────────────────────────────────

def parse_registry(path: Path) -> list:
    """
    返回协议条目列表，每个条目是 dict：
      { 'id': 'P-001', 'title': '...', 'fields': { field_name: value } }
    """
    if not path.exists():
        return []

    text = path.read_text(encoding="utf-8")
    protocols = []

    # 按二级标题切分协议区块: ### P-XXX
    blocks = re.split(r"(?=###\s+P-\d+)", text)
    for block in blocks:
        m = re.match(r"###\s+(P-\d+)\s+·\s+(.+)", block)
        if not m:
            continue
        pid   = m.group(1).strip()
        title = m.group(2).strip()

        # 提取表格内容: | 字段 | 值 |
        fields = {}
        for row in re.finditer(
            r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|", block
        ):
            key = row.group(1).strip()
            val = row.group(2).strip()
            if key and key != "属性" and key != "内容":
                fields[key] = val

        protocols.append({"id": pid, "title": title, "fields": fields})

    return protocols


# ────────────────────────────────────────────────
# 审计单条协议
# ────────────────────────────────────────────────

def audit_protocol_entry(entry: dict) -> dict:
    pid    = entry["id"]
    title  = entry["title"]
    fields = entry["fields"]
    issues = []

    # 1. 必备字段检查
    for f in REQUIRED_FIELDS:
        if f not in fields or not fields[f].strip():
            issues.append({"level": "P1", "field": f,
                           "msg": f"必备字段缺失或为空: {f}"})

    # 2. 状态合法性
    status_raw = fields.get("状态", "")
    if status_raw not in VALID_STATUSES:
        issues.append({"level": "P1", "field": "状态",
                       "msg": f"状态字段非法: '{status_raw}'。合法値: {VALID_STATUSES}"})

    # 3. 版本号格式
    ver = fields.get("当前版本", "")
    if not VERSION_PATTERN.match(ver):
        issues.append({"level": "P1", "field": "当前版本",
                       "msg": f"版本号格式错误: '{ver}'，应为 vX.Y"})

    # 4. DNA 格式验证
    dna_val = fields.get("DNA锚定", "")
    # 去掉 backtick
    dna_clean = dna_val.strip("`").strip()
    if dna_clean and not DNA_PATTERN.match(dna_clean):
        issues.append({"level": "P0", "field": "DNA锚定",
                       "msg": f"DNA 格式不合规: '{dna_clean[:60]}'"})

    # 5. 日期格式检查
    for date_field in ("生效日期", "最近变更"):
        dv = fields.get(date_field, "")
        if dv and not re.match(r"\d{4}-\d{2}-\d{2}", dv):
            issues.append({"level": "P1", "field": date_field,
                           "msg": f"日期格式错误: '{dv}'，应为 YYYY-MM-DD"})

    # 6. 弃用协议警告
    if status_raw == "⚪ 弃用":
        issues.append({"level": "INFO", "field": "状态",
                       "msg": f"{pid} 已弃用，确认相关模块已停止使用"})

    p0_count = sum(1 for i in issues if i["level"] == "P0")
    p1_count = sum(1 for i in issues if i["level"] == "P1")

    if p0_count > 0:
        result_status = "red"
    elif p1_count > 0:
        result_status = "yellow"
    else:
        result_status = "green"

    return {
        "id": pid,
        "title": title,
        "status": result_status,
        "p0": p0_count > 0,
        "p0_count": p0_count,
        "p1_count": p1_count,
        "issues": issues,
        "dna_anchor": fields.get("DNA锚定", "").strip("`").strip(),
    }


# ────────────────────────────────────────────────
# 写入日志
# ────────────────────────────────────────────────

def write_log(record: dict):
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ────────────────────────────────────────────────
# 主函数
# ────────────────────────────────────────────────

def run_audit(list_only: bool = False, verbose: bool = False):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not REGISTRY_FILE.exists():
        print(f"❌ PROTOCOL_REGISTRY.md 不存在: {REGISTRY_FILE}")
        sys.exit(1)

    protocols = parse_registry(REGISTRY_FILE)
    if not protocols:
        print("⚠️  未解析到任何协议条目，请检查 PROTOCOL_REGISTRY.md 格式")
        sys.exit(1)

    print()
    print("╔" + "═" * 65 + "╗")
    print("║  🐉 协议审计节点 v1.0" + " " * 42 + "║")
    print("╠" + "═" * 65 + "╣")
    print(f"║  时间: {ts}" + " " * (57 - len(ts)) + "║")
    print(f"║  注册表: {REGISTRY_FILE.name}  共 {len(protocols)} 条协议" +
          " " * max(0, 40 - len(str(len(protocols)))) + "║")
    print("╠" + "═" * 65 + "╣")

    if list_only:
        print("║  {:<8} {:<30} {:<12}  ║".format("编号", "名称", "状态"))
        print("╠" + "═" * 65 + "╣")
        for p in protocols:
            fields = p.get("fields", {})
            st     = fields.get("状态", "未知")
            print("║  {:<8} {:<30} {:<12}  ║".format(
                p["id"], p["title"][:30], st[:12]))
        print("╚" + "═" * 65 + "╝")
        return

    print("║  {:<8} {:<28} {:>4} {:>4} {:^8}  ║".format(
        "编号", "名称", "P0", "P1", "结果"))
    print("╠" + "═" * 65 + "╣")

    total_p0  = 0
    all_green = True

    for entry in protocols:
        result = audit_protocol_entry(entry)
        total_p0 += result["p0_count"]
        if result["status"] != "green":
            all_green = False

        ICONS = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
        icon = ICONS.get(result["status"], "⚪")
        print("║  {:<8} {:<28} {:>4} {:>4}  {}       ║".format(
            result["id"], result["title"][:28],
            result["p0_count"], result["p1_count"], icon))

        if verbose and result["issues"]:
            for issue in result["issues"]:
                if issue["level"] in ("P0", "P1"):
                    print(f"║    [{issue['level']}] {issue['field']}: {issue['msg'][:50]}")

        # 生成审计 DNA
        dna_str = ""
        if DNA_OK:
            r = dna_generate(
                title=f"{result['id']}-协议审计",
                category="audit", action="协议审计"
            )
            dna_str = r["dna_string"]

        # 写日志
        write_log({
            "timestamp": ts,
            "dimension": "protocol",
            "protocol_id": result["id"],
            "protocol_title": result["title"],
            "status": result["status"],
            "p0": result["p0"],
            "p0_count": result["p0_count"],
            "p1_count": result["p1_count"],
            "issues": result["issues"],
            "dna_anchor": result["dna_anchor"],
            "dna": dna_str,
        })

    print("╠" + "═" * 65 + "╣")
    overall = ("🟢 全部通过" if all_green else
               "🔴 存在 P0" if total_p0 > 0 else "🟡 存在警告")
    print("║  综合结果: {:<55}║".format(overall))
    print("╚" + "═" * 65 + "╝")
    print(f"\n💾 审计日志已写入: {AUDIT_LOG}")

    if total_p0 > 0:
        print("⚠️  P0 熔断触发！")
        sys.exit(1)


# ────────────────────────────────────────────────
# 入口
# ────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="龍魂协议审计节点")
    parser.add_argument("--list", action="store_true",
                        help="仅列出协议清单，不运行审计")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细问题")
    args = parser.parse_args()
    run_audit(list_only=args.list, verbose=args.verbose)
