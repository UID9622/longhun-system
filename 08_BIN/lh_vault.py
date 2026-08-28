#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-08-28-LH-VAULT-v3.0-AUTO-ARCHIVE
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）· MulanPSL v2（工程实现层）
"""
龍魂·统一密钥库 v3.0
所有密钥统一存 macOS Keychain（service=longhun-vault）· 系统级 AES 加密 · 绑定本机登录密码/指纹
条目注册表: ~/.longhun/vault_registry.json（只记名字+用途+状态·不记值）· list/env 只读注册表·不扫全钥匙串

v3.0 新增（8/28·老大指令"检测到新密钥直接存·过期了打包放着"）:
  - detect: 扫描文件/目录自动识别新密钥 → 自动入库（不用老大说"存"）
  - archive: 过期密钥归档（打包放着·值冻结保留·不删除只冻结 = P0天条）
  - list --all: 活跃+归档一起看

用法:
  lh_vault.py put <name> [--note <说明>] [--value <v>]      # 存/更新密钥（无 --value 则交互输入）
  lh_vault.py get <name>                                     # 取密钥值（供脚本/AI 使用）
  lh_vault.py list [--all]                                   # 列条目（--all 含归档·不显示值）
  lh_vault.py detect <path...>                               # 扫描识别新密钥自动入库
  lh_vault.py archive <name> [--reason <原因>]               # 过期归档（值保留·不删）
  lh_vault.py rm <name>                                      # 显式删除（默认用 archive 代替）
  lh_vault.py env [name...]                                  # 输出 export NAME=value（训练脚本 eval 取用·跳过归档）
  lh_vault.py whoami                                         # 身份确认（钥匙串可解 + GPG 指纹 = UID9622）

保密铁律: 值不落盘/不打印日志/不进git/不传云。能解开钥匙串=只有老大本人（物理身份锚）。
归档铁律: 过期=冻结打包放归档区·不删值不删记录·复用需显式 put 重新激活。
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
import argparse
import datetime
import getpass
import json
import os
import re
import subprocess
import sys

SERVICE = "longhun-vault"
REGISTRY = os.path.expanduser("~/.longhun/vault_registry.json")
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 常见密钥格式识别正则（detect 用·宁漏勿错·值不打印）
KEY_PATTERNS = [
    # 华为云/阿里云 AK (20位大写数字混合)
    ("AK", r"\b(?:LTAI|HPU|AKIA|AK)[A-Z0-9]{16,18}\b"),
    # 通用 SK / secret (32-64位 base64-ish)
    ("SK", r"\b[A-Za-z0-9+/=_\-]{32,64}\b"),
    # token 前缀式: sk- / ghp_ / ghu_ / ntn_ / Bearer
    ("TOKEN", r"\b(?:sk|ghp_|ghu_|ghs_|ntn_|xox[baprs]?-|eyJ)[A-Za-z0-9_\-\.]{16,}\b"),
    # 键值对: xxx_key/xxx_token/xxx_secret/password = 值
    ("KV", r"(?:api[_-]?key|access[_-]?key|secret|token|password|passwd)\s*[=:]\s*[\"']?([A-Za-z0-9+/=_\-\.]{8,})[\"']?"),
]
# 黑名单: 不当作密钥的常见非敏感值
SKIP_VALUES = {"true", "false", "none", "null", "localhost", "127.0.0.1", "password", "secret", "changeme"}


def _now():
    return datetime.date.today().isoformat()


def _sec(args):
    r = subprocess.run(["security"] + args, capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def _load_reg():
    try:
        with open(REGISTRY, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_reg(reg):
    os.makedirs(os.path.dirname(REGISTRY), exist_ok=True)
    with open(REGISTRY, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)


def _mask(v):
    if not v:
        return ""
    if len(v) <= 8:
        return "*" * len(v)
    return v[:4] + "*" * (len(v) - 8) + v[-4:]


def _in_vault(name):
    rc, out, err = _sec(["find-generic-password", "-s", SERVICE, "-a", name, "-w"])
    return rc == 0


def _safe_name(src):
    """从文件名/变量名推断条目标名·去敏感字符"""
    nm = re.sub(r"[^A-Za-z0-9_\-]+", "-", src).strip("-")
    return nm[:64] or "secret"


def cmd_put(name, value, note):
    if value is None:
        v1 = getpass.getpass(f"输入 {name} 的密钥值: ")
        v2 = getpass.getpass("再次输入确认: ")
        if v1 != v2:
            print("🔴 两次输入不一致, 已取消")
            return 1
        value = v1
    if not value:
        print("🔴 空值, 已取消")
        return 1
    rc, out, err = _sec(["add-generic-password", "-a", name, "-s", SERVICE, "-w", value, "-U"])
    if rc != 0:
        print(f"🔴 写入失败: {err}")
        return 1
    reg = _load_reg()
    meta = reg.get(name, {})
    meta.update({"note": note or meta.get("note", ""), "updated": _now(), "status": "active"})
    meta.pop("archived_at", None)
    meta.pop("expire_reason", None)
    reg[name] = meta
    _save_reg(reg)
    print(f"✅ 已加密存入统一密钥库: {SERVICE}/{name} (active)")
    return 0


def cmd_get(name):
    rc, out, err = _sec(["find-generic-password", "-s", SERVICE, "-a", name, "-w"])
    if rc != 0:
        print(f"🔴 未找到: {name} ({err})", file=sys.stderr)
        return 1
    print(out)
    return 0


def cmd_list(include_archived=False):
    reg = _load_reg()
    if not reg:
        print("(空) 密钥库无条目")
        return 0
    active, archived = [], []
    for nm, meta in reg.items():
        (archived if meta.get("status") == "archived" else active).append((nm, meta))
    for nm, meta in active:
        note = f"  |  {meta.get('note', '')}" if meta.get("note") else ""
        print(f"  {nm}{note}")
    if include_archived and archived:
        print("  —— 归档区（过期冻结·打包放着·不删）——")
        for nm, meta in archived:
            when = meta.get("archived_at", "?")
            why = meta.get("expire_reason", "")
            why = f"  |  {why}" if why else ""
            print(f"  [归档 {when}] {nm}{why}")
    elif not include_archived and archived:
        print(f"  （另有 {len(archived)} 条已归档·--all 查看）")
    return 0


def cmd_archive(name, reason):
    reg = _load_reg()
    if name not in reg:
        print(f"🔴 未登记: {name}（不存在或已被删除）", file=sys.stderr)
        return 1
    if reg[name].get("status") == "archived":
        print(f"ℹ️ 已是归档态: {name}")
        return 0
    reg[name]["status"] = "archived"
    reg[name]["archived_at"] = _now()
    if reason:
        reg[name]["expire_reason"] = reason
    _save_reg(reg)
    # Keychain 值保留（不删除只冻结 = P0天条）
    print(f"✅ 已归档（打包放着·值冻结保留）: {name} @ {_now()}")
    if reason:
        print(f"   原因: {reason}")
    return 0


def cmd_detect(paths):
    """扫描文件/目录·识别新密钥·自动入库（老大不用开口）"""
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, fns in os.walk(p):
                dirs[:] = [d for d in dirs if d not in (".git", "node_modules", ".venv", "__pycache__")]
                for fn in fns:
                    fp = os.path.join(root, fn)
                    if os.path.getsize(fp) > 2 * 1024 * 1024:  # 跳过 >2MB
                        continue
                    files.append(fp)
        elif os.path.isfile(p):
            files.append(p)
        else:
            print(f"⚠️ 路径不存在, 跳过: {p}")
    if not files:
        print("🔴 无文件可扫描")
        return 1
    found = {}  # name -> (value, note)
    for fp in files:
        try:
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            continue
        base = os.path.basename(fp)
        for label, pat in KEY_PATTERNS:
            for m in re.finditer(pat, content, re.IGNORECASE):
                val = m.group(1) if m.groups() else m.group(0)
                if not val or val.lower() in SKIP_VALUES or len(val) < 8:
                    continue
                # 推断条目标名
                var_hint = ""
                line = content[max(0, content.rfind("\n", 0, m.start())):m.end()]
                vm = re.search(r"([A-Za-z_][A-Za-z0-9_]{3,})", line)
                if vm:
                    var_hint = _safe_name(vm.group(1))
                nm = f"{_safe_name(base)}-{label.lower()}-{_safe_name(var_hint or _mask(val))}"
                nm = nm[:64]
                if nm in found or _in_vault(nm):
                    continue  # 已存在, 跳过不覆盖
                note = f"auto-detect from {base} ({label})"
                found[nm] = (val, note)
    if not found:
        print("ℹ️ 未发现新密钥（已有条目或无非敏感新值）")
        return 0
    ok = 0
    for nm, (val, note) in found.items():
        rc, out, err = _sec(["add-generic-password", "-a", nm, "-s", SERVICE, "-w", val, "-U"])
        if rc != 0:
            print(f"🔴 入库失败 {nm}: {err}")
            continue
        reg = _load_reg()
        reg[nm] = {"note": note, "updated": _now(), "status": "active"}
        _save_reg(reg)
        print(f"✅ 自动入库: {nm}  (来源 {note.split(' from ')[-1]})")
        ok += 1
    print(f"—— 本次自动入库 {ok} 条新密钥 · 值已加密 · 不落盘 ——")
    return 0


def cmd_rm(name):
    rc, out, err = _sec(["delete-generic-password", "-s", SERVICE, "-a", name])
    if rc != 0:
        print(f"🔴 删除失败: {err}", file=sys.stderr)
        return 1
    reg = _load_reg()
    reg.pop(name, None)
    _save_reg(reg)
    print(f"✅ 已删除: {SERVICE}/{name}（建议日常用 archive 归档代替删除）")
    return 0


def cmd_env(names, include_archived=False):
    reg = _load_reg()
    if not names:
        names = list(reg.keys())
    for nm in names:
        if not include_archived and reg.get(nm, {}).get("status") == "archived":
            print(f"# 归档跳过: {nm}", file=sys.stderr)
            continue
        rc, out, err = _sec(["find-generic-password", "-s", SERVICE, "-a", nm, "-w"])
        if rc == 0:
            key = nm.upper().replace("-", "_")
            print(f"export {key}={out}")
        else:
            print(f"# 缺失: {nm}", file=sys.stderr)
    return 0


def cmd_whoami():
    rc, out, err = _sec(["find-generic-password", "-s", SERVICE, "-a", "hcloud-aksk", "-w"])
    vault_ok = rc == 0
    rc2 = subprocess.run(["gpg", "--list-secret-keys", "--with-colons"], capture_output=True, text=True)
    has_gpg = rc2.returncode == 0 and GPG_FINGERPRINT in rc2.stdout
    print("身份自检:")
    print(f"  [{'✅' if vault_ok else '❌'}] Keychain 解锁态(本机物理身份锚)")
    print(f"  [{'✅' if has_gpg else '❌'}] GPG 指纹 {GPG_FINGERPRINT}")
    if vault_ok and has_gpg:
        print(f"身份确认: UID9622 · 诸葛鑫 · 龍芯北辰 ✓")
        print(f"确认码: {CONFIRM_CODE}")
        return 0
    print("🔴 身份未完全确认, 拒绝密钥操作")
    return 1


def main():
    p = argparse.ArgumentParser(description="龍魂·统一密钥库")
    sub = p.add_subparsers(dest="op")
    p1 = sub.add_parser("put"); p1.add_argument("name"); p1.add_argument("--note", default=""); p1.add_argument("--value", default=None)
    p2 = sub.add_parser("get"); p2.add_argument("name")
    p3 = sub.add_parser("list"); p3.add_argument("--all", action="store_true")
    p4 = sub.add_parser("detect"); p4.add_argument("paths", nargs="+")
    p5 = sub.add_parser("archive"); p5.add_argument("name"); p5.add_argument("--reason", default="")
    p6 = sub.add_parser("rm"); p6.add_argument("name")
    p7 = sub.add_parser("env"); p7.add_argument("names", nargs="*"); p7.add_argument("--include-archived", action="store_true")
    p8 = sub.add_parser("whoami")
    args = p.parse_args()
    if not args.op:
        p.print_help()
        return 1
    return {
        "put": lambda: cmd_put(args.name, args.value, args.note),
        "get": lambda: cmd_get(args.name),
        "list": lambda: cmd_list(args.all),
        "detect": lambda: cmd_detect(args.paths),
        "archive": lambda: cmd_archive(args.name, args.reason),
        "rm": lambda: cmd_rm(args.name),
        "env": lambda: cmd_env(args.names, args.include_archived),
        "whoami": cmd_whoami,
    }[args.op]()


if __name__ == "__main__":
    sys.exit(main())
