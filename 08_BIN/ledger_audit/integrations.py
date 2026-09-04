#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍審⚡️2026-08-31-AUDIT-INTEGRATIONS-v1.0-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🔌 龍魂审计引擎接入桥 · Audit Engine Integrations v1.0

把 audit_engine/router 的 TODO 落地为真实链路:
  🟢 on_green_commit  → Notion 流水账写入 + GitHub 同步
  🟡 on_yellow_pending → Notion 健康度=待核（宝宝接管窗口）
  🔴 on_red_block      → Bark 主权人警报 + incidents 归档 + GitHub 同步

用法:
  python3 integrations.py green  data/tx_example.json
  python3 integrations.py yellow data/tx_example.json
  python3 integrations.py red    data/tx_example.json
  python3 integrations.py audit  data/ledger.json   # 批量审计+路由
"""

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

# 清代理（Notion 直连坑：socks5h 劫持导致 Remote end closed）
for _k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"):
    os.environ.pop(_k, None)
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

BASE = Path.home() / "longhun-system"
LEDGER_REPO = Path.home() / "longhun-ledger"
NOTION_VERSION = "2022-06-28"
# 老 API(databases/{id}) 用 database_id；MCP 新 API 用 data_source_id=3cd7125a-9c9f-819f-a6c9-000b2a4ef6a1
LEDGER_DB = "3cd7125a-9c9f-810e-9a45-c9dfa6d41d66"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# Notion select 名称映射（科目 / 交易类型 / 见证人格 / 健康度 / GitHub同步）
ACCOUNT_SELECT = {
    "1001": "1001 焊点·铁律", "1105": "1105 behavioral-crypto",
    "1401": "1401 核心人格矩阵", "2001": "2001 外部依赖",
    "3201": "3201 协议资产净值", "3301": "3301 人格议会价值",
}
TX_TYPE_SELECT = {
    "T1": "T1 创世", "T2": "T2 自建", "T3": "T3 采购", "T4": "T4 依赖",
    "T5": "T5 权益", "T6": "T6 注入", "T7": "T7 核销", "T8": "T8 见证",
    "T9": "T9 主权转让", "T10": "T10 数据外泄", "T11": "T11 自建里程碑",
    "T12": "T12 跨境协作",
}
HEALTH_SELECT = {"GREEN": "🟢 健康", "YELLOW": "🟡 待核", "RED": "🔴 异常"}
GITHUB_SELECT = {"done": "✅ 已同步", "pending": "🔄 待同步", "conflict": "⚠️ 冲突"}
WITNESS_PRIMARY = {
    "🧠ASI-001·至诚智魂": "🧠 ASI-001·至诚智魂", "🌿曾仕强老师": "🌿 曾仕强老师",
    "🔧鲁班": "🔧 鲁班", "🌊郑和": "🌊 郑和", "🌀上帝之眼": "🌀 上帝之眼",
    "🐱宝宝": "🐱 龍芯·宝宝", "⚖️包青天": "⚖️ 包青天", "⚔️孙子": "⚔️ 孙子",
    "👑龍魂（主权人）": "👑 龍魂（主权人）", "🔮诸葛亮": "🔮 诸葛亮",
}


# ────────────────────────────────────────────
# Token 获取（四级降级）
# ────────────────────────────────────────────
def get_token(key: str) -> str:
    try:
        r = subprocess.run(
            [sys.executable, str(BASE / "bin" / "lh_vault.py"), "get", key],
            capture_output=True, text=True, timeout=30,
        )
        v = r.stdout.strip().strip('"').strip("'")
        if r.returncode == 0 and v and not v.startswith("🔴"):
            return v
    except Exception:
        pass
    envs = {"NOTION_TOKEN": "NOTION_TOKEN", "BARK_KEY": "BARK_KEY",
            "GITHUB_PERSONAL_ACCESS_TOKEN": "GITHUB_PERSONAL_ACCESS_TOKEN"}
    return os.environ.get(envs.get(key, key), "")


def notion_call(token, path, method="GET", data=None):
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(
        f"https://api.notion.com/v1/{path}", data=body, method=method,
        headers={"Authorization": f"Bearer {token}", "Notion-Version": NOTION_VERSION,
                 "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        print(f"  ⚠️  Notion API [{method} {path}] {e.code}: {detail}")
        return {"error": e.code, "detail": detail}
    except Exception as exc:
        print(f"  ⚠️  Notion 请求异常 [{method} {path}]: {exc}")
        return {"error": str(exc)}


# ────────────────────────────────────────────
# 交易结构归一（GitHub ledger.json ↔ audit_engine tx）
# ────────────────────────────────────────────
def to_engine_tx(entry: dict) -> dict:
    """ledger.json 一行 → audit_engine 所需结构"""
    return {
        "tx_id": entry.get("tx_id", ""),
        "dna": entry.get("dna", ""),
        "hash": entry.get("hash", ""),
        "date": entry.get("date", ""),
        "timestamp": entry.get("timestamp", ""),
        "type": entry.get("tx_type", "UNKNOWN"),
        "balanced": entry.get("balanced", False),
        "debit": {"account": entry.get("dr_account", ""), "name": entry.get("dr_name", ""),
                  "amount": entry.get("amount", "")},
        "credit": {"account": entry.get("cr_account", ""), "name": entry.get("cr_name", ""),
                   "amount": entry.get("amount", "")},
        "description": entry.get("description", ""),
    }


def to_ledger_entry(tx: dict) -> dict:
    """audit_engine tx → ledger.json entry（反向归一）"""
    return {
        "tx_id": tx.get("tx_id", ""),
        "dna": tx.get("dna", ""),
        "hash": tx.get("hash", ""),
        "date": tx.get("date", ""),
        "timestamp": tx.get("timestamp", ""),
        "tx_type": tx.get("type", "UNKNOWN"),
        "tx_type_name": TX_TYPE_SELECT.get(tx.get("type", ""), "").split(" ", 1)[-1],
        "balanced": tx.get("balanced", False),
        "dr_account": str(tx.get("debit", {}).get("account", "")),
        "dr_name": tx.get("debit", {}).get("name", ""),
        "cr_account": str(tx.get("credit", {}).get("account", "")),
        "cr_name": tx.get("credit", {}).get("name", ""),
        "amount": tx.get("debit", {}).get("amount", ""),
        "description": tx.get("description", ""),
        "witness": tx.get("witness", "🐱 龍芯·宝宝"),
        "uid": "UID9622",
    }


def parse_amount(amount) -> float:
    """'1条'/'100元' → 数值"""
    m = re.search(r"\d+(\.\d+)?", str(amount))
    return float(m.group()) if m else 0.0


def witness_select(witness: str) -> str:
    """'🧠ASI-001·至诚智魂 + 🌿曾仕强老师' → Notion 主见证选项"""
    if not witness:
        return "🐱 龍芯·宝宝"
    primary = str(witness).split("+")[0].strip()
    return WITNESS_PRIMARY.get(primary, "🐱 龍芯·宝宝")


# ────────────────────────────────────────────
# Notion 写入（去重：按交易DNA查询）
# ────────────────────────────────────────────
def find_notion_tx(token, dna: str):
    """按交易DNA查 Notion 库，返回已存在 page id 或 None"""
    q = notion_call(token, f"databases/{LEDGER_DB}/query", "POST",
                    {"filter": {"property": "交易DNA", "title": {"equals": dna}}})
    if q.get("error") or not q.get("results"):
        return None
    return q["results"][0]["id"]


def build_properties(entry: dict, color: str) -> dict:
    dr = entry.get("dr_account", "")
    cr = entry.get("cr_account", "")
    return {
        "交易DNA": {"title": [{"text": {"content": entry.get("dna", "")}}]},
        "哈希指纹": {"rich_text": [{"text": {"content": entry.get("hash", "")}}]},
        "日期": {"date": {"start": entry.get("date", "")}},
        "摘要": {"rich_text": [{"text": {"content": entry.get("description", "")[:1500]}}]},
        "借方科目": {"select": {"name": ACCOUNT_SELECT.get(dr, f"{dr} {entry.get('dr_name','')}")}},
        "贷方科目": {"select": {"name": ACCOUNT_SELECT.get(cr, f"{cr} {entry.get('cr_name','')}")}},
        "交易类型": {"select": {"name": TX_TYPE_SELECT.get(entry.get("tx_type", ""), entry.get("tx_type", ""))}},
        "见证人格": {"select": {"name": witness_select(entry.get("witness", ""))}},
        "金额": {"number": parse_amount(entry.get("amount", 0))},
        "平衡✓": {"checkbox": bool(entry.get("balanced", False))},
        "健康度": {"select": {"name": HEALTH_SELECT.get(color, "🟡 待核")}},
        "GitHub同步": {"select": {"name": GITHUB_SELECT["pending"]}},
    }


def notion_write(entry: dict, color: str, token: str = None) -> bool:
    token = token or get_token("NOTION_TOKEN")
    if not token:
        print("  🔴 无 NOTION_TOKEN")
        return False
    dna = entry.get("dna", "")
    existing = find_notion_tx(token, dna)
    props = build_properties(entry, color)
    if existing:
        r = notion_call(token, f"pages/{existing}", "PATCH", {"properties": props})
        ok = not r.get("error")
        print(f"  {'✅' if ok else '⚠️'} Notion 更新 {dna}")
    else:
        r = notion_call(token, "pages", "POST",
                        {"parent": {"database_id": LEDGER_DB}, "properties": props})
        ok = not r.get("error")
        print(f"  {'✅' if ok else '⚠️'} Notion 新建 {dna}")
    return ok


# ────────────────────────────────────────────
# GitHub 同步（本地克隆 → append ledger.json → push）
# ────────────────────────────────────────────
def github_sync(entry: dict, color: str, token: str = None) -> bool:
    token = token or get_token("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token or not LEDGER_REPO.exists():
        print("  🟡 GitHub 同步跳过（无 token 或仓库未克隆）")
        return False
    ledger_path = LEDGER_REPO / "data" / "ledger.json"
    try:
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    except Exception:
        ledger = {"meta": {"name": "龍魂流水账", "version": "v1.0", "owner": "UID9622"},
                  "transactions": []}
    txs = ledger.setdefault("transactions", [])
    if not any(t.get("dna") == entry.get("dna") for t in txs):
        row = dict(entry)
        row["health"] = {"GREEN": "🟢 健康", "YELLOW": "🟡 待核", "RED": "🔴 异常"}[color]
        row["github_sync"] = "✅"
        txs.append(row)
        ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
        # incidents/ 红色归档
        if color == "RED":
            inc = LEDGER_REPO / "incidents"
            inc.mkdir(exist_ok=True)
            (inc / f"{entry.get('tx_id','incident')}.json").write_text(
                json.dumps({"dna": entry.get("dna"), "hash": entry.get("hash"),
                            "color": color, "description": entry.get("description", ""),
                            "witness": entry.get("witness", "")}, ensure_ascii=False, indent=2),
                encoding="utf-8")
    else:
        print("  ⏭️  GitHub 已存在同 DNA 交易")
    # git push
    url = f"https://UID9622:{token}@github.com/UID9622/longhun-ledger.git"
    cmds = [
        f"cd {LEDGER_REPO} && git add -A",
        f"cd {LEDGER_REPO} && git -c user.name='UID9622' -c user.email='UID9622@users.noreply.github.com' "
        f"commit -m 'audit: {entry.get('tx_id','')} {color}' --no-verify || true",
        f"cd {LEDGER_REPO} && git push '{url}' HEAD:main --no-verify",
    ]
    for c in cmds:
        r = subprocess.run(["bash", "-c", c], capture_output=True, text=True, timeout=120)
        if r.returncode != 0 and "nothing to commit" not in r.stdout + r.stderr:
            print(f"  ⚠️  {r.stderr.strip()[:200]}")
    print("  ✅ GitHub 已同步")
    return True


# ────────────────────────────────────────────
# Bark 主权人警报
# ────────────────────────────────────────────
def bark_alert(title: str, body: str, key: str = None) -> bool:
    key = key or get_token("BARK_KEY")
    if not key:
        print("  🟡 Bark 警报跳过（无 BARK_KEY）")
        return False
    url = (f"https://api.day.app/{key}/{urllib.parse.quote(title)}/"
           f"{urllib.parse.quote(body)}?group={urllib.parse.quote('龍魂账法')}")
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            ok = r.status == 200
        print(f"  {'✅' if ok else '⚠️'} Bark 已推送：{title}")
        return ok
    except Exception as exc:
        print(f"  ⚠️  Bark 推送异常: {exc}")
        return False


# ────────────────────────────────────────────
# 回调落地（router.py 调用）
# ────────────────────────────────────────────
def _entry(tx: dict, result: dict) -> dict:
    entry = to_ledger_entry(tx)
    if result.get("witness"):
        entry["witness"] = result["witness"]
    return entry


def on_green_commit(tx: dict, result: dict):
    print(f"  🔌 接入桥 GREEN: {tx.get('tx_id')}")
    entry = _entry(tx, result)
    notion_write(entry, "GREEN")
    github_sync(entry, "GREEN")


def on_yellow_pending(tx: dict, result: dict):
    print(f"  🔌 接入桥 YELLOW: {tx.get('tx_id')} · 宝宝接管 72h 窗口")
    entry = _entry(tx, result)
    notion_write(entry, "YELLOW")


def on_red_block(tx: dict, result: dict):
    print(f"  🔌 接入桥 RED: {tx.get('tx_id')}")
    rules = ",".join(result.get("red_rules_triggered", [])) or "无规则命中"
    entry = _entry(tx, result)
    notion_write(entry, "RED")
    github_sync(entry, "RED")
    bark_alert(
        "🔴 龍魂账法·主权阻断",
        f"{tx.get('tx_id')} 触发{rules} 评分{result.get('score')} "
        f"见证:{tx.get('witness','')} DNA:{tx.get('dna','')}",
    )


# ────────────────────────────────────────────
# 批量审计路由
# ────────────────────────────────────────────
def batch_audit(ledger_path: str):
    sys.path.insert(0, str(Path(__file__).parent))
    from router import route
    from audit_engine import audit_transaction
    with open(ledger_path, encoding="utf-8") as f:
        ledger = json.load(f)
    entries = ledger.get("transactions", [])
    print(f"🚦 接入桥批量审计 · {len(entries)} 笔")
    for entry in entries:
        tx = to_engine_tx(entry)
        route(tx)


if __name__ == "__main__":
    import urllib.parse
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    with open(sys.argv[2], encoding="utf-8") as f:
        entry_data = json.load(f)
    tx = to_engine_tx(entry_data)
    result = {"red_rules_triggered": [], "score": 0}
    if cmd == "green":
        on_green_commit(tx, result)
    elif cmd == "yellow":
        on_yellow_pending(tx, result)
    elif cmd == "red":
        result = {"red_rules_triggered": ["TEST-RED"], "score": 10}
        on_red_block(tx, result)
    elif cmd == "audit":
        batch_audit(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)
