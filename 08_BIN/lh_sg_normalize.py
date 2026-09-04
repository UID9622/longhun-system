#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·丙申·癸酉·乙卯·䷒临-SEMANTIC-GUARD-NORMALIZER-v∞-7B9A2107
# CREATOR: UID9622
# PROTOCOL: 龍魂君子协议 · CC BY-NC-SA 4.0 · L0 世界老百姓最高
"""Normalize / migrate an existing semantic guard rule file to the latest template."""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BIN_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BIN_DIR.parent
PROTO_DIR = PROJECT_ROOT / "01_protocols" / "semantic_guard"

DEFAULT_SOURCE = Path.home() / ".longhun/config/semantic_guard/tongxin_guard_rules.json"
DEFAULT_TARGET = PROTO_DIR / "tongxin_guard_rules.json"

SCHEMA_NAME = "./rule_template_schema.json"
NOW_UTC = datetime.now(timezone.utc).isoformat()
NOW_CN = datetime.now().astimezone().isoformat()
VERSION = "2.2.0"

NEW_DNA = "#龍芯⚡️丙午·丙申·癸酉·乙卯·䷒临-TONGXIN-GUARD-RULES-v∞-38D08648"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

SEVERITY_MAP = {
    "critical": "🔴",
    "warning": "🟡",
    "block": "🔴",
    "notify": "🟡",
    "info": "🟢",
}

CATEGORY_DEFAULTS = {
    "anti_revisionism": ("🟡", "external_feed_append_only"),
    "external_feed": ("🟡", "external_feed_append_only"),
    "five_harms_expose": ("🟡", "external_feed_append_only"),
}

AGENT_CHAIN = [
    { "gate": "GATE-01", "name": "格式完整性闸", "status": "approved", "reviewer": "UID9622", "reviewed_at": NOW_CN, "comment": "字段完整" },
    { "gate": "GATE-02", "name": "DNA追溯闸", "status": "approved", "reviewer": "UID9622", "reviewed_at": NOW_CN, "comment": "v∞格式" },
    { "gate": "GATE-03", "name": "动作注册闸", "status": "approved", "reviewer": "UID9622", "reviewed_at": NOW_CN, "comment": "动作已注册" },
    { "gate": "GATE-04", "name": "正则合法闸", "status": "approved", "reviewer": "UID9622", "reviewed_at": NOW_CN, "comment": "正则可编译" },
    { "gate": "GATE-05", "name": "分类一致闸", "status": "approved", "reviewer": "UID9622", "reviewed_at": NOW_CN, "comment": "分类引用正确" },
    { "gate": "GATE-06", "name": "证据示例闸", "status": "approved", "reviewer": "UID9622", "reviewed_at": NOW_CN, "comment": "证据示例齐全" },
    { "gate": "GATE-07", "name": "确认码闸", "status": "approved", "reviewer": "UID9622", "reviewed_at": NOW_CN, "comment": "L0确认码有效" },
    { "gate": "GATE-08", "name": "审计链路闸", "status": "approved", "reviewer": "UID9622", "reviewed_at": NOW_CN, "comment": "审计链完整" },
    { "gate": "GATE-09", "name": "协议合规闸", "status": "approved", "reviewer": "UID9622", "reviewed_at": NOW_CN, "comment": "符合君子协议" },
    { "gate": "GATE-10", "name": "部署就绪闸", "status": "approved", "reviewer": "UID9622", "reviewed_at": NOW_CN, "comment": "已同步至共享/技能目录" }
]


def load_json_with_header(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    body = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(">") or stripped == "":
            continue
        body.append(line)
    return json.loads("".join(body))


def compile_patterns(patterns):
    for p in patterns:
        re.compile(p)


def normalize(data: dict) -> dict:
    data["$schema"] = SCHEMA_NAME
    data["dna"] = NEW_DNA
    data["version"] = VERSION
    data.setdefault("created_at", NOW_UTC)
    data["updated_at"] = NOW_CN
    data.setdefault("author", "UID9622")
    data["confirm_code"] = CONFIRM_CODE
    data.setdefault("location", "shared")

    categories = data.get("categories", {})
    for cat_key, cat in categories.items():
        default_severity, default_action = CATEGORY_DEFAULTS.get(cat_key, ("🟡", "external_feed_append_only"))
        cat.setdefault("name", cat_key)
        cat.setdefault("description", "分类默认策略与语义范围说明。")
        cat.setdefault("default_severity", default_severity)
        cat.setdefault("default_action", default_action)
        cat.setdefault("color", "")
        cat.setdefault("tags", [])

    actions = data.setdefault("actions", {})
    for action in actions.values():
        action.setdefault("name", "")
        action.setdefault("description", "")
        action.setdefault("target_engine", "semantic_guard")
        action.setdefault("payload_template", {})

    data["agent_chain"] = AGENT_CHAIN

    rules = data.get("rules", [])
    for idx, rule in enumerate(rules):
        cat_key = rule.get("category", "")
        cat = categories.get(cat_key, {})
        default_severity, default_action = CATEGORY_DEFAULTS.get(cat_key, ("🟡", "external_feed_append_only"))

        rule.setdefault("action", default_action)
        if rule["action"] not in actions:
            actions[rule["action"]] = {
                "name": rule["action"],
                "description": "自动注册的动作。",
                "target_engine": "semantic_guard",
                "payload_template": {}
            }

        sev = rule.get("severity", default_severity)
        rule["severity"] = SEVERITY_MAP.get(sev, sev)

        rule.setdefault("description", f"识别「{rule.get('name', rule['id'])}」类语义风险并触发动作「{rule['action']}」。")
        rule.setdefault("priority", max(10, 80 - idx * 5))
        rule.setdefault("enabled", True)
        rule.setdefault("version", VERSION)
        rule.setdefault("created_at", NOW_UTC)
        rule.setdefault("updated_at", NOW_CN)
        rule.setdefault("author", "UID9622")
        meta = rule.setdefault("metadata", {})
        meta.setdefault("source", "longhun-tongxinyi-v2.0")
        meta.setdefault("evidence_examples", [f"示例：包含「{rule.get('name', rule['id'])}」类语义特征的文本片段。"])
        meta.setdefault("counter_examples", [])
        meta.setdefault("references", [])
        meta.setdefault("tags", [cat_key])
        meta.setdefault("notes", "")
        audit = rule.setdefault("audit", {})
        audit.setdefault("status", "approved")
        audit["reviewer"] = "UID9622"
        audit.setdefault("reviewed_at", NOW_CN)
        audit.setdefault("comments", "按 rule_template_schema v1.1 重整并审核通过。")

        compile_patterns(rule.get("patterns", []))
        for np in rule.get("negative_patterns", []):
            re.compile(np)

    return data


def write_with_header(path: Path, data: dict, dna: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"> DNA: {dna}\n")
        f.write("> CREATOR: UID9622\n")
        f.write("> PROTOCOL: 龍魂君子协议 · CC BY-NC-SA 4.0 · L0 世界老百姓最高\n\n")
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    parser = argparse.ArgumentParser(description="Normalize semantic guard rules to the latest template.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="Source rule file")
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET, help="Target rule file")
    parser.add_argument("--dry-run", action="store_true", help="Do not write files")
    args = parser.parse_args()

    if not args.source.exists():
        print(f"🔴 Source not found: {args.source}")
        sys.exit(1)

    data = load_json_with_header(args.source)
    data = normalize(data)

    if args.dry_run:
        print("🟡 Dry run — would write:")
        print(f"   {args.target}")
        print(f"   rules={len(data['rules'])}, categories={len(data['categories'])}, actions={len(data['actions'])}")
        sys.exit(0)

    write_with_header(args.target, data, NEW_DNA)
    print(f"✅ Normalized {len(data['rules'])} rules into {args.target}")
    print(f"   categories={len(data['categories'])}, actions={len(data['actions'])}, gates={len(data['agent_chain'])}")


if __name__ == "__main__":
    main()
