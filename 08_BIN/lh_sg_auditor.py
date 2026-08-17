#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·丙申·癸酉·乙卯·临-SEMANTIC-GUARD-AUDITOR-v∞-7D2493A7
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# CREATOR: UID9622
# PROTOCOL: 龍魂君子协议 · CC BY-NC-SA 4.0 · L0 世界老百姓最高
"""Audit semantic guard rule files against rule_template_schema.json."""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from jsonschema import Draft7Validator
except Exception:
    Draft7Validator = None

BIN_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BIN_DIR.parent
PROTO_DIR = PROJECT_ROOT / "01_protocols" / "semantic_guard"

DEFAULT_RULE_PATH = PROTO_DIR / "tongxin_guard_rules.json"
SCHEMA_PATH = PROTO_DIR / "rule_template_schema.json"


def load_json_with_header(path: Path) -> dict:
    """加载带龍魂头部注释的JSON文件。

    头部注释格式:
      # CONFIRM: ...
      # SEAL: ...
      > DNA: ...
      > CREATOR: ...
      > PROTOCOL: ...
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    body = [
        line for line in lines
        if line.strip()
        and not line.strip().startswith(">")
        and not line.strip().startswith("#")
    ]
    return json.loads("".join(body))


def log(level, msg):
    print(f"[{level}] {msg}")


def check_regex(patterns, label):
    errors = []
    for p in patterns:
        try:
            re.compile(p)
        except re.error as e:
            errors.append(f"{label} invalid regex: {p[:40]}... ({e})")
    return errors


def check_iso(dt_str):
    try:
        datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return True
    except Exception:
        return False


def check_agent_chain(chain):
    errors = []
    expected = [f"GATE-{i:02d}" for i in range(1, 11)]
    gates = [c.get("gate") for c in chain]
    if gates != expected:
        errors.append(f"agent_chain gates mismatch: {gates}")
    for gate in chain:
        if gate.get("status") == "approved" and gate.get("reviewer") != "UID9622":
            errors.append(f"{gate.get('gate')} approved reviewer must be UID9622")
    return errors


def audit(path):
    errors = []
    infos = []

    if not path.exists():
        errors.append(f"File not found: {path}")
        return False, errors, infos

    data = load_json_with_header(path)

    schema = None
    if SCHEMA_PATH.exists():
        try:
            schema = load_json_with_header(SCHEMA_PATH)
        except Exception as e:
            errors.append(f"Cannot load schema: {e}")

    if schema and Draft7Validator:
        validator = Draft7Validator(schema)
        for err in validator.iter_errors(data):
            errors.append(f"Schema: {err.message} at {list(err.path)}")
    elif schema:
        infos.append("jsonschema not installed; running built-in checks only.")

    required_top = ["dna", "version", "description", "updated_at", "categories", "actions", "agent_chain", "rules"]
    for key in required_top:
        if key not in data:
            errors.append(f"Missing top-level field: {key}")

    if "version" in data and not re.fullmatch(r"\d+\.\d+\.\d+", data["version"]):
        errors.append(f"Invalid version format: {data.get('version')}")

    if "dna" in data and not re.fullmatch(r"#龍芯⚡[\uFE0F]?[\s\S]+", data["dna"]):
        errors.append("DNA must start with #龍芯⚡")

    if "confirm_code" in data and not data["confirm_code"].startswith("#CONFIRM"):
        errors.append("confirm_code must start with #CONFIRM")

    for tfield in ("created_at", "updated_at"):
        if tfield in data and not check_iso(data[tfield]):
            errors.append(f"Invalid ISO datetime: {tfield}")

    categories = data.get("categories", {})
    if not categories:
        errors.append("At least one category is required.")

    for cat_key, cat in categories.items():
        for f in ("name", "description", "default_severity", "default_action"):
            if f not in cat:
                errors.append(f"Category {cat_key} missing {f}")
        if "description" in cat and len(cat["description"]) < 10:
            errors.append(f"Category {cat_key} description too short")
        if "default_severity" in cat and cat["default_severity"] not in ("🟢", "🟡", "🔴"):
            errors.append(f"Category {cat_key} invalid severity")

    actions = data.get("actions", {})
    for action_key, action in actions.items():
        for f in ("name", "description", "target_engine"):
            if f not in action:
                errors.append(f"Action {action_key} missing {f}")

    agent_chain = data.get("agent_chain", [])
    errors.extend(check_agent_chain(agent_chain))

    rules = data.get("rules", [])
    if not rules:
        errors.append("At least one rule is required.")

    ids = set()
    for rule in rules:
        rid = rule.get("id", "")
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", rid):
            errors.append(f"Rule id invalid: {rid}")
        if rid in ids:
            errors.append(f"Duplicate rule id: {rid}")
        ids.add(rid)

        cat = rule.get("category", "")
        if cat not in categories:
            errors.append(f"Rule {rid} references unknown category: {cat}")

        action = rule.get("action", "")
        if action and action not in actions:
            errors.append(f"Rule {rid} references unregistered action: {action}")

        if "description" not in rule or len(rule["description"]) < 20:
            errors.append(f"Rule {rid} description missing or too short")

        if "patterns" not in rule or not rule["patterns"]:
            errors.append(f"Rule {rid} has no patterns")
        else:
            errors.extend(check_regex(rule["patterns"], f"Rule {rid}"))

        if "negative_patterns" in rule:
            errors.extend(check_regex(rule["negative_patterns"], f"Rule {rid} negative"))

        if "priority" in rule and not (0 <= rule["priority"] <= 100):
            errors.append(f"Rule {rid} priority out of range")

        if "version" in rule and not re.fullmatch(r"\d+\.\d+\.\d+", rule["version"]):
            errors.append(f"Rule {rid} invalid version")

        for tfield in ("created_at", "updated_at"):
            if tfield in rule and not check_iso(rule[tfield]):
                errors.append(f"Rule {rid} invalid {tfield}")

        meta = rule.get("metadata", {})
        if "evidence_examples" not in meta or not meta["evidence_examples"]:
            errors.append(f"Rule {rid} missing evidence_examples")

        audit_obj = rule.get("audit", {})
        if audit_obj.get("status") == "approved" and audit_obj.get("reviewer") != "UID9622":
            errors.append(f"Rule {rid} approved audit reviewer must be UID9622")

    infos.append(f"Categories: {len(categories)}")
    infos.append(f"Actions: {len(actions)}")
    infos.append(f"Gates: {len(agent_chain)}")
    infos.append(f"Rules: {len(rules)}")

    return not errors, errors, infos


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_RULE_PATH
    ok, errors, infos = audit(target)
    for info in infos:
        log("INFO", info)
    if errors:
        for err in errors:
            log("FAIL", err)
        print(f"\nAUDIT FAILED: {len(errors)} issue(s).")
        sys.exit(1)
    print("\nAUDIT PASSED: all rules conform to rule_template_schema v1.1.")


if __name__ == "__main__":
    main()
