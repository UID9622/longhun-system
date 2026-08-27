#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·辛未·亥时·䷕贲-DEVICE-LEDGER-v1.0-9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · 设备登记台账 v1.0（设备指纹 ↔ 持有人 ↔ 密钥）
============================================================
数字主权追溯的「腿」：不阻止数据流动，但让每一次流动可追溯到
「哪台设备 → 谁持有 → 绑哪把密钥」。
铁律：
  - 只存哈希指纹，不存 MAC/序列号/UUID 明文（本人可查·他人不可见）
  - 密钥只存指纹（SSH key 指纹 / GPG key id），不存密钥内容
  - 撤销 = 冻结留档，不删除（P0 不删除只冻结）
  - 登记自动联动统一DNA登记册（device 资产），双册互锁

用法：
  lh device fingerprint                       # 本机指纹（只打印不登记）
  lh device register --name "..." --role mac  # 登记本机
  lh device add --name 鲲鹏 --role kunpeng --fingerprint <fp> --key ssh:xxxx [--platform linux]
  lh device list                               # 台账列表
  lh device show <device_id>                   # 设备详情
  lh device revoke <device_id>                 # 撤销（冻结留档）
  lh device verify                             # 本机指纹 vs 台账
  lh device trace <device_id|指纹>             # 追溯：设备 → 持有人 → 密钥
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

UID = "9622"
HOLDER = "诸葛鑫（UID9622）"
GPG_KEY_ID = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

ROOT = Path(__file__).resolve().parent.parent
LEDGER_FILE = ROOT / "08_STATE" / "device_ledger.json"
AUDIT_FILE = ROOT / ".audit" / "device_ledger.log"
UDR_SCRIPT = ROOT / "bin" / "lh_unified_dna_registry.py"

sys.path.insert(0, str(ROOT / "bin"))
try:
    from lh_time_engine import get_output_stamp
    _STAMP_OK = True
except Exception:
    _STAMP_OK = False

LEDGER_VERSION = "1.0"


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def stamp_compact() -> str:
    """#龍芯⚡️干支四柱·卦（用于 DNA）"""
    try:
        if _STAMP_OK:
            return get_output_stamp(format_type="compact")
    except Exception:
        pass
    return "#龍芯⚡️丙午·丙申·辛未·亥时·䷕贲"


def audit(msg: str) -> None:
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now_iso()}] {msg}\n")


def sh(cmd) -> str:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=8)
        return (r.stdout or r.stderr or "").strip()
    except Exception:
        return ""


def machine_fingerprint() -> dict:
    """稳定指纹：只算哈希，不落明文标识"""
    if sys.platform == "darwin":
        uuid = sh("ioreg -rd1 -c IOPlatformExpertDevice 2>/dev/null | awk -F'\"' '/IOPlatformUUID/{print $4; exit}'")
        model = sh("sysctl -n hw.model")
        serial = sh("system_profiler SPHardwareDataType 2>/dev/null | awk -F': ' '/Serial/{print $2; exit}'")
        host = sh("hostname")
        platform = "darwin"
    else:
        uuid = sh("cat /sys/class/dmi/id/product_uuid 2>/dev/null")
        model = sh("cat /sys/class/dmi/id/product_name 2>/dev/null || uname -m")
        serial = sh("cat /sys/class/dmi/id/product_serial 2>/dev/null")
        host = sh("hostname")
        platform = "linux"
    raw = f"{uuid}|{model}|{serial}|{host}"
    fp = hashlib.sha256(raw.encode()).hexdigest()[:32]
    return {"fingerprint": fp, "platform": platform, "model": model, "host": host}


def ssh_key_fingerprint() -> str:
    for p in ("~/.ssh/id_ed25519.pub", "~/.ssh/id_rsa.pub", "~/.ssh/longhun_kunpeng_ed25519.pub"):
        fp = sh(f"ssh-keygen -lf {p} 2>/dev/null")
        if fp:
            m = re.search(r"SHA256:[A-Za-z0-9+/=]+", fp)
            if m:
                return m.group(0)
    return ""


def load_ledger() -> dict:
    if LEDGER_FILE.exists():
        try:
            return json.loads(LEDGER_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"meta": {"version": LEDGER_VERSION, "sovereign": f"UID{UID}", "updated_at": "", "total": 0}, "devices": {}}


def save_ledger(ledger: dict) -> None:
    ledger["meta"]["updated_at"] = now_iso()
    ledger["meta"]["total"] = len(ledger["devices"])
    LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_FILE.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")


def gen_dna(device_id: str, fp: str) -> str:
    h8 = hashlib.sha256(f"{fp}|{device_id}".encode()).hexdigest()[:8]
    return f"{stamp_compact()}-DEVICE-{device_id}-{UID}-{h8}"


def udr_sync(action: str, asset: str, label: str = "") -> str:
    """联动统一DNA登记册（失败降级不阻断）"""
    if not UDR_SCRIPT.exists():
        return "[skip] 统一DNA登记册不存在"
    args = [sys.executable, str(UDR_SCRIPT), action, f"UID{UID}", "device", asset]
    if label:
        args.append(label)
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=30)
        out = (r.stdout or r.stderr or "").strip().replace("\n", " ")
        return f"[udr:{action}] {out[:120]}"
    except Exception as e:
        return f"[udr:{action}:fail] {e}"


def cmd_fingerprint(args):
    info = machine_fingerprint()
    print(f"fingerprint : {info['fingerprint']}")
    print(f"platform    : {info['platform']}")
    print(f"model       : {info['model']}")
    print(f"host        : {info['host']}")
    print(f"ssh_key_fp  : {ssh_key_fingerprint() or '(未找到公钥)'}")
    return 0


def cmd_register(args):
    info = machine_fingerprint()
    ledger = load_ledger()
    for did, d in ledger["devices"].items():
        if d["fingerprint"] == f"sha256:{info['fingerprint']}":
            print(f"已在台账: {did}（{d['name']}·{d['status']}）")
            return 0
    device_id = f"DEV-{info['fingerprint'][:8].upper()}"
    key_fp = ssh_key_fingerprint()
    dna = gen_dna(device_id, info["fingerprint"])
    entry = {
        "device_id": device_id,
        "fingerprint": f"sha256:{info['fingerprint']}",
        "name": args.name or f"{info['model']}（本机）",
        "holder": HOLDER,
        "role": args.role or "mac",
        "platform": info["platform"],
        "model": info["model"],
        "host": info["host"],
        "ssh_key_fingerprint": key_fp,
        "gpg_key_id": GPG_KEY_ID,
        "registered_at": now_iso(),
        "last_active": now_iso(),
        "dna": dna,
        "status": "active",
        "note": args.note or "",
    }
    ledger["devices"][device_id] = entry
    save_ledger(ledger)
    audit(f"REGISTER {device_id} {entry['name']} fp={entry['fingerprint']}")
    print(f"✅ 已登记: {device_id} · {entry['name']}")
    print(f"   DNA   : {dna}")
    print(f"   持有人 : {HOLDER} · 角色 {entry['role']}")
    if key_fp:
        print(f"   SSH钥 : {key_fp}")
    print("   联动统一DNA登记册:", udr_sync("register", info["fingerprint"], args.name or device_id))
    return 0


def cmd_add(args):
    ledger = load_ledger()
    fp = args.fingerprint.strip()
    if not re.fullmatch(r"[0-9a-fA-F]{32,64}", fp):
        print("❌ fingerprint 必须为 32~64 位 hex（用 lh device fingerprint 生成）")
        return 1
    device_id = f"DEV-{fp[:8].upper()}"
    if device_id in ledger["devices"]:
        print(f"已存在: {device_id}")
        return 0
    dna = gen_dna(device_id, fp)
    entry = {
        "device_id": device_id,
        "fingerprint": f"sha256:{fp.lower()}",
        "name": args.name,
        "holder": args.holder or HOLDER,
        "role": args.role or "remote",
        "platform": args.platform or "unknown",
        "model": args.model or "",
        "host": args.host or "",
        "ssh_key_fingerprint": args.key or "",
        "gpg_key_id": GPG_KEY_ID,
        "registered_at": now_iso(),
        "last_active": now_iso(),
        "dna": dna,
        "status": "active",
        "note": args.note or "",
    }
    ledger["devices"][device_id] = entry
    save_ledger(ledger)
    audit(f"ADD {device_id} {entry['name']} fp={entry['fingerprint']}")
    print(f"✅ 已登记远端: {device_id} · {entry['name']}")
    print(f"   DNA: {dna}")
    return 0


def cmd_list(args):
    ledger = load_ledger()
    devs = ledger["devices"]
    if not devs:
        print("台账为空（lh device register 登记本机 / lh device add 登记远端）")
        return 0
    print(f"{'ID':<12} {'名称':<18} {'角色':<10} {'持有人':<14} 状态")
    for d in devs.values():
        if not args.all and d["status"] != "active":
            continue
        print(f"{d['device_id']:<12} {d['name'][:17]:<18} {d['role']:<10} {d['holder'][:13]:<14} {d['status']}")
    print(f"\n共 {len(devs)} 台（active {sum(1 for d in devs.values() if d['status']=='active')}）")
    return 0


def cmd_show(args):
    ledger = load_ledger()
    d = ledger["devices"].get(args.id)
    if not d:
        print(f"未找到 {args.id}")
        return 1
    for k, v in d.items():
        print(f"{k:<22}: {v}")
    return 0


def cmd_revoke(args):
    ledger = load_ledger()
    d = ledger["devices"].get(args.id)
    if not d:
        print(f"未找到 {args.id}")
        return 1
    d["status"] = "revoked"
    d["note"] = (d.get("note", "") + f" | REVOKED {now_iso()}").strip(" |")
    save_ledger(ledger)
    audit(f"REVOKE {args.id}")
    print(f"⛔ 已冻结: {args.id}（不删除只冻结·留档可追溯）")
    return 0


def cmd_verify(args):
    info = machine_fingerprint()
    ledger = load_ledger()
    for d in ledger["devices"].values():
        if d["fingerprint"] == f"sha256:{info['fingerprint']}":
            print(f"✅ 本机已登记: {d['device_id']} · {d['name']} · {d['status']}")
            return 0
    print(f"❌ 本机未登记（fingerprint={info['fingerprint'][:16]}...）· 执行 lh device register")
    return 1


def cmd_trace(args):
    ledger = load_ledger()
    target = args.id.lower()
    d = next((x for x in ledger["devices"].values()
              if x["device_id"].lower() == target or x["fingerprint"] == f"sha256:{target}"), None)
    if not d:
        print(f"❌ 台账无此设备（{args.id}）")
        return 1
    print(f"🔍 追溯结果: {d['device_id']} → {d['holder']} · {d['name']}")
    print(f"   指纹: {d['fingerprint']}")
    print(f"   密钥: ssh={d.get('ssh_key_fingerprint') or '-'} | gpg={d['gpg_key_id']}")
    print(f"   登记: {d['registered_at']} · 状态 {d['status']}")
    print(f"   DNA : {d['dna']}")
    print("   统一DNA登记册交叉验证:", udr_sync("verify", d["fingerprint"].replace("sha256:", "")))
    return 0


def main():
    p = argparse.ArgumentParser(prog="lh device", description="设备登记台账·指纹↔持有人↔密钥")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("fingerprint", help="本机指纹（只打印不登记）")
    sp.set_defaults(fn=cmd_fingerprint)

    sp = sub.add_parser("register", help="登记本机")
    sp.add_argument("--name", default="")
    sp.add_argument("--role", default="mac")
    sp.add_argument("--note", default="")
    sp.set_defaults(fn=cmd_register)

    sp = sub.add_parser("add", help="登记远端设备")
    sp.add_argument("--name", required=True)
    sp.add_argument("--role", default="remote")
    sp.add_argument("--fingerprint", required=True)
    sp.add_argument("--key", default="")
    sp.add_argument("--platform", default="")
    sp.add_argument("--model", default="")
    sp.add_argument("--host", default="")
    sp.add_argument("--holder", default="")
    sp.add_argument("--note", default="")
    sp.set_defaults(fn=cmd_add)

    sub.add_parser("list", help="台账列表").set_defaults(fn=cmd_list, all=False)
    sub.add_parser("list-all", help="含已撤销").set_defaults(fn=cmd_list, all=True)

    sp = sub.add_parser("show", help="设备详情")
    sp.add_argument("id")
    sp.set_defaults(fn=cmd_show)

    sp = sub.add_parser("revoke", help="撤销（冻结留档）")
    sp.add_argument("id")
    sp.set_defaults(fn=cmd_revoke)

    sub.add_parser("verify", help="本机 vs 台账").set_defaults(fn=cmd_verify)

    sp = sub.add_parser("trace", help="追溯：设备→持有人→密钥")
    sp.add_argument("id")
    sp.set_defaults(fn=cmd_trace)

    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
