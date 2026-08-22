# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
USDT-TRC20 链上对账监控脚本
DNA:#龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-USDT-MONITOR-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2

功能:
  1. 读 config/usdt_receive.json 收款配置
  2. 只读查询 TronGrid/Tronscan（公开链数据·不上传任何用户数据）
  3. 新入账 -> append-only 台账 xpay/logs/usdt_inbox.csv
  4. 去重（按 transaction_id）+ 报表

用法:
  python3 bin/lh_usdt_monitor.py            # 拉新入账 + 写入台账
  python3 bin/lh_usdt_monitor.py --ledger   # 只看台账
  python3 bin/lh_usdt_monitor.py --check    # 检查配置是否就绪
"""
import csv
import json
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(ROOT, "config", "usdt_receive.json")
USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"


def load_config() -> dict:
    if not os.path.exists(CONFIG):
        sys.exit("❌ 未找到配置: config/usdt_receive.json")
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def wallet_ready(cfg: dict) -> bool:
    return cfg.get("wallet", "").startswith("T") and "FILL" not in cfg.get("wallet", "")


def fetch_trc20(addr: str, api: str, contract: str, timeout: int) -> list:
    """只读查询 TRC20 转账记录（仅传公开地址）"""
    url = f"{api}/v1/accounts/{addr}/transactions/trc20?limit=50&only_to=true&contract_address={contract}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("data", [])


def load_ledger(path: str) -> set:
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        return {row["tx_id"] for row in csv.DictReader(f)}


def append_ledger(path: str, rows: list):
    new_file = not os.path.exists(path)
    with open(path, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["timestamp", "tx_id", "from_addr", "amount_usdt", "block_ts", "confirmed"])
        for r in rows:
            w.writerow([r["timestamp"], r["tx_id"], r["from_addr"], r["amount_usdt"], r["block_ts"], r["confirmed"]])


def main():
    cfg = load_config()
    arg = sys.argv[1] if len(sys.argv) > 1 else ""

    if arg == "--check":
        if wallet_ready(cfg):
            print(f"✅ 配置就绪 · 钱包: {cfg['wallet']}")
        else:
            print("🔴 未配置收款钱包: 请用 TronLink 生成 TRC20 地址后填入 config/usdt_receive.json 的 wallet 字段")
        return

    ledger_path = os.path.join(ROOT, cfg.get("ledger", "xpay/logs/usdt_inbox.csv"))
    if arg == "--ledger":
        if not os.path.exists(ledger_path):
            print("📭 台账为空（尚未收到任何款项）")
            return
        with open(ledger_path, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        total = sum(float(r["amount_usdt"]) for r in rows)
        print(f"📒 台账 {len(rows)} 笔 · 累计 {total:.2f} USDT")
        for r in rows[-10:]:
            print(f"  {r['timestamp']}  +{r['amount_usdt']} USDT  ← {r['from_addr'][:12]}...  {r['tx_id'][:16]}")
        return

    if not wallet_ready(cfg):
        sys.exit("🔴 未配置收款钱包: 请先填写 config/usdt_receive.json（TronLink 生成 TRC20 地址）")

    # 拉链上数据（主 API 失败切备用）
    rows = []
    for api in [cfg["api"], cfg["backup_api"]]:
        try:
            txs = fetch_trc20(cfg["wallet"], api, USDT_CONTRACT, cfg.get("timeout", 15))
            break
        except Exception as e:
            print(f"⚠️ {api} 不可达: {e}")
            txs = []
    if not txs:
        print("📭 无新入账（或链上 API 不可达，稍后再试）")
        return

    seen = load_ledger(ledger_path)
    new_rows = []
    for tx in txs:
        tx_id = tx.get("transaction_id", "")
        if not tx_id or tx_id in seen:
            continue
        if tx.get("token_info", {}).get("symbol", "").upper() != "USDT":
            continue
        if tx.get("to", "") != cfg["wallet"]:
            continue
        amount = int(tx.get("value", 0)) / 1_000_000.0  # TRC20 6 位小数
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        new_rows.append({
            "timestamp": ts,
            "tx_id": tx_id,
            "from_addr": tx.get("from", ""),
            "amount_usdt": f"{amount:.2f}",
            "block_ts": tx.get("block_timestamp", ""),
            "confirmed": str(tx.get("confirmed", False)),
        })
        seen.add(tx_id)

    if new_rows:
        append_ledger(ledger_path, new_rows)
        print(f"💰 新入账 {len(new_rows)} 笔:")
        for r in new_rows:
            print(f"  +{r['amount_usdt']} USDT  ← {r['from_addr'][:12]}...  tx:{r['tx_id'][:16]}")
    else:
        print("📭 无新入账（与台账一致）")


if __name__ == "__main__":
    main()
