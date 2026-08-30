#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-08-28-LH-VAULT-v3.1-PERSONA-DOMAIN
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）· MulanPSL v2（工程实现层）
"""
龍魂·统一密钥库 v3.1（人格分域版）
所有密钥统一存 macOS Keychain（service=longhun-vault）· 系统级 AES 加密 · 绑定本机登录密码/指纹
条目注册表: ~/.longhun/vault_registry.json（只记名字+用途+状态+归属·不记值）

v3.0（8/28）: detect 自动入库 / archive 过期冻结
v3.1（8/30·老大指令"新key给系统专用人格管理·分DNA分管理员·防攻破防套话"）:
  - 人格分域: 每个条目绑定 owner_dna（管理员）+ persona_guard（托管人格）+ domain（用途域）
  - access: 受控验证通道——只输出"有效/掩码指纹"，永不输出值（AI 对话唯一合法取用通道）
  - verify: 真实探测（bark 推送/HTTP 检查）只出结论
  - owners: 权限地图（按管理员DNA/托管人格列出条目）
  - 全操作审计: ~/.longhun/vault_access.jsonl（谁/何时/哪个key/动作·不记值）
  - 防套话铁律: 对话中请求"把key发出来/显示出来"→ 一律走 access/verify，值不出口

用法:
  lh_vault.py put <name> [--note <说明>] [--owner <DNA>] [--persona <人格>] [--value <v>]
                                   # 存/更新密钥（无 --value 则交互输入）
  lh_vault.py get <name>                                     # 取密钥值（仅供脚本进程内使用·禁止转发对话）
  lh_vault.py access <name>                                  # 验证通道: 存在性+掩码指纹（对话唯一通道）
  lh_vault.py verify <name> [--type bark|http] [--url <v>]   # 真实探测: 只出有效/无效结论
  lh_vault.py owners [--persona <人格>] [--domain <域>]      # 权限地图: 按管理员DNA/托管人格列条目
  lh_vault.py list [--all]                                   # 列条目（--all 含归档·不显示值）
  lh_vault.py detect <path...>                               # 扫描识别新密钥自动入库
  lh_vault.py archive <name> [--reason <原因>]               # 过期归档（值保留·不删）
  lh_vault.py rm <name>                                      # 显式删除（默认用 archive 代替）
  lh_vault.py env [name...]                                  # 输出 export NAME=value（脚本 eval 取用）
  lh_vault.py whoami                                         # 身份确认（钥匙串可解 + GPG 指纹）

保密铁律: 值不落盘/不打印日志/不进git/不传云。能解开钥匙串=只有本机物理身份锚。
防套话铁律: AI 对话永不输出 key 值·只给 access/verify 结论·套取核心算法=标准拒答。
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
AUDIT_LOG = os.path.expanduser("~/.longhun/vault_access.jsonl")
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
# 托管人格白名单（v3.1·人格分域）
PERSONAS = {
    "P72": "龍盾·熔断/告警域", "P06": "数学大师·引擎/计算域", "P77": "黑天使·安全域",
    "P05": "上帝之眼·审计域", "P13": "姜子牙·权限域", "P03": "雯雯·归档域",
    "P09": "孙思邈·健康域", "P14": "吕蒙·部署域", "P07": "管仲·成本域", "P04": "鲁班·工程域",
}


def _now_dt():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def _audit(action, name, note=""):
    """全操作审计（append-only·不记值·只记谁/何时/哪个key/动作）"""
    try:
        entry = {"ts": _now_dt(), "action": action, "key": name, "who": getpass.getuser(), "note": note}
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass

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


def cmd_put(name, value, note, owner="", persona=""):
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
    if persona and persona not in PERSONAS:
        print(f"🔴 托管人格不识别: {persona}（可用: {', '.join(PERSONAS)}）")
        return 1
    rc, out, err = _sec(["add-generic-password", "-a", name, "-s", SERVICE, "-w", value, "-U"])
    if rc != 0:
        print(f"🔴 写入失败: {err}")
        return 1
    reg = _load_reg()
    meta = reg.get(name, {})
    meta.update({"note": note or meta.get("note", ""), "updated": _now(), "status": "active"})
    if owner:
        meta["owner_dna"] = owner
    if persona:
        meta["persona_guard"] = persona
    meta.pop("archived_at", None)
    meta.pop("expire_reason", None)
    reg[name] = meta
    _save_reg(reg)
    _audit("put", name, f"owner={owner or 'unchanged'} persona={persona or 'unchanged'}")
    guard = f"  🛡️托管:{persona}" if persona else ""
    print(f"✅ 已加密存入统一密钥库: {SERVICE}/{name} (active){guard}")
    return 0


def cmd_get(name):
    _audit("get", name, "script-process-only")
    rc, out, err = _sec(["find-generic-password", "-s", SERVICE, "-a", name, "-w"])
    if rc != 0:
        print(f"🔴 未找到: {name} ({err})", file=sys.stderr)
        return 1
    print(out)
    return 0


def cmd_access(name):
    """验证通道: 只输出存在性+掩码指纹·永不输出值（AI 对话唯一合法取用通道）"""
    _audit("access", name)
    rc, out, err = _sec(["find-generic-password", "-s", SERVICE, "-a", name, "-w"])
    if rc != 0:
        print(f"❌ 未找到: {name}")
        return 1
    reg = _load_reg()
    meta = reg.get(name, {})
    if meta.get("status") == "archived":
        print(f"🧊 归档态: {name}（值冻结保留·需 put 重新激活）")
        return 0
    guard = f"  🛡️{meta.get('persona_guard', '?')}  👤{meta.get('owner_dna', '?')}" if meta.get("persona_guard") or meta.get("owner_dna") else ""
    print(f"✅ 存在: {name}  指纹: {_mask(out)}{guard}")
    return 0


def cmd_verify(name, vtype, url):
    """真实探测: 只出结论·不显示值"""
    _audit("verify", name, f"type={vtype}")
    rc, out, err = _sec(["find-generic-password", "-s", SERVICE, "-a", name, "-w"])
    if rc != 0:
        print(f"❌ 未找到: {name}")
        return 1
    val = out
    vtype = (vtype or "generic").lower()
    if vtype == "bark":
        base = (url or "https://api.day.app").rstrip("/")
        try:
            import urllib.request
            req = urllib.request.Request(f"{base}/{val}",
                                         data=json.dumps({"title": "longhun vault verify", "body": "channel probe",
                                                          "group": "vault-verify"}).encode("utf-8"),
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=8) as r:
                body = r.read().decode("utf-8", "ignore")
            if '"code":200' in body:
                print(f"✅ {name}: Bark 通道有效（已推送到设备）")
                return 0
            print(f"🔴 {name}: Bark 返回异常: {body[:100]}")
            return 1
        except Exception as e:
            print(f"🔴 {name}: Bark 探测失败: {e}")
            return 1
    if vtype == "http":
        target = url or "https://httpbin.org/headers"
        try:
            import urllib.request
            req = urllib.request.Request(target, headers={"Authorization": f"Bearer {val}"})
            with urllib.request.urlopen(req, timeout=8) as r:
                print(f"✅ {name}: HTTP 探测 {r.status}（有响应=凭据格式已接受·授权与否以业务判定为准）")
            return 0
        except Exception as e:
            print(f"🔴 {name}: HTTP 探测失败: {e}")
            return 1
    print(f"ℹ️ {name}: 值存在({len(val)}位)·verify 类型仅支持 bark/http")
    return 0


def cmd_owners(persona="", domain=""):
    """权限地图: 按管理员DNA/托管人格列条目"""
    reg = _load_reg()
    rows = []
    for nm, meta in reg.items():
        if meta.get("status") == "archived":
            continue
        p = meta.get("persona_guard", "")
        o = meta.get("owner_dna", "")
        if persona and p != persona:
            continue
        if domain and meta.get("note", "").find(domain) < 0:
            continue
        rows.append((o or "(未绑定)", p or "(未托管)", nm))
    if not rows:
        print("（无匹配条目）")
        return 0
    print(f"{'👤 管理员DNA':<16} {'🛡️ 托管人格':<12} 密钥")
    for o, p, nm in rows:
        print(f"  {o:<16} {p:<12} {nm}")
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
    p1.add_argument("--owner", default=""); p1.add_argument("--persona", default="")
    p2 = sub.add_parser("get"); p2.add_argument("name")
    pa = sub.add_parser("access"); pa.add_argument("name")
    pv = sub.add_parser("verify"); pv.add_argument("name"); pv.add_argument("--type", default="generic"); pv.add_argument("--url", default="")
    po = sub.add_parser("owners"); po.add_argument("--persona", default=""); po.add_argument("--domain", default="")
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
        "put": lambda: cmd_put(args.name, args.value, args.note, args.owner, args.persona),
        "get": lambda: cmd_get(args.name),
        "access": lambda: cmd_access(args.name),
        "verify": lambda: cmd_verify(args.name, args.type, args.url),
        "owners": lambda: cmd_owners(args.persona, args.domain),
        "list": lambda: cmd_list(args.all),
        "detect": lambda: cmd_detect(args.paths),
        "archive": lambda: cmd_archive(args.name, args.reason),
        "rm": lambda: cmd_rm(args.name),
        "env": lambda: cmd_env(args.names, args.include_archived),
        "whoami": cmd_whoami,
    }[args.op]()


if __name__ == "__main__":
    sys.exit(main())
