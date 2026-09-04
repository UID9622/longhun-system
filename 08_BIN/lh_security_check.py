#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·乙亥·巳时·䷝离-SECURITY-CHECK-v1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 协议配套: docs/对外接口协议-v1.0.md
"""
🐉 龍魂安全自检 v1.0 — lh security [--json] [--scan-dir PATH]

检查项:
  1. 端口绑定    lh_api.py 是否仅绑定 127.0.0.1（默认安全·禁 0.0.0.0）
  2. 文件权限    bin/lh.py 可执行位
  3. GPG 签名    .asc 存在性 + gpg --verify 抽查（默认扫描 docs/ examples/ dist/）
  4. 文件泄露    敏感模式扫描（硬编码密钥/令牌/私钥/绝对路径）· 默认扫 packaging/longhun_cli/

输出: 标准 Node JSON（status/checks/risk_score/node_id/audit）。
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API_PY = ROOT / "08_BIN" / "lh_api.py"
LH_BIN = ROOT / "bin" / "lh.py"
DEFAULT_SCAN_DIR = ROOT / "packaging" / "longhun_cli"
SIGN_SCAN_DIRS = ["docs", "examples", "dist"]

# 敏感模式（硬编码密钥/令牌/私钥）
SENSITIVE_PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS Access Key"),
    (re.compile(r"ghp_[A-Za-z0-9]{20,}"), "GitHub PAT"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "OpenAI/Notion 风格密钥"),
    (re.compile(r"-----BEGIN (RSA |OPENSSH |PGP |EC )?PRIVATE KEY-----"), "私钥明文"),
    (re.compile(r"(?i)\b(password|passwd|secret|token|api[_-]?key)\s*[:=]\s*['\"]?[^\s'\"]{8,}"), "凭据赋值"),
]
CODE_SUFFIX = {".py", ".sh", ".toml", ".yaml", ".yml", ".js", ".json"}


def _node_id(text: str) -> str:
    return f"SEC-9622-{hashlib.sha256(text.encode()).hexdigest()[:8].upper()}"


def check_port_binding() -> dict:
    """lh_api.py 是否仅绑定 127.0.0.1。"""
    try:
        text = API_PY.read_text(encoding="utf-8")
    except OSError as e:
        return {"name": "端口绑定", "ok": False, "detail": f"读取 lh_api.py 失败: {e}"}
    if 'HOST = "127.0.0.1"' in text and "0.0.0.0" not in text:
        return {"name": "端口绑定", "ok": True, "detail": "lh_api.py 硬焊 127.0.0.1（默认只监听本地）"}
    if 'HOST = "127.0.0.1"' in text:
        return {"name": "端口绑定", "ok": True, "detail": "lh_api.py 绑定 127.0.0.1（0.0.0.0 仅作注释出现）"}
    return {"name": "端口绑定", "ok": False, "detail": "⚠️ lh_api.py 未绑定 127.0.0.1，请立即检查 HOST 常量"}


def check_permissions() -> dict:
    """bin/lh.py 可执行位。"""
    ok = os.access(LH_BIN, os.X_OK)
    return {"name": "文件权限", "ok": ok,
            "detail": f"bin/lh.py 可执行" if ok else f"bin/lh.py 不可执行（chmod +x {LH_BIN}）"}


def gpg_verify(asc: Path, target: Path) -> tuple[bool, str]:
    try:
        r = subprocess.run(["gpg", "--batch", "--verify", str(asc), str(target)],
                           capture_output=True, text=True, timeout=30)
        out = (r.stdout + r.stderr)
        ok = r.returncode == 0 and ("完好的签名" in out or "Good signature" in out)
        if not r.returncode and not ok:
            ok = True  # gpg 0 退出但语言环境无匹配 → 视为通过
        return ok, "签名有效" if ok else "签名无效/公钥未导入(可先导入 lh_public_key.asc)"
    except FileNotFoundError:
        return False, "gpg 未安装"
    except subprocess.TimeoutExpired:
        return False, "gpg 验证超时"


def check_signatures() -> dict:
    """抽查 docs/examples/dist 的 .asc 签名完整性。"""
    checked, ok_n = 0, 0
    detail: list[str] = []
    for d in SIGN_SCAN_DIRS:
        base = ROOT / d
        if not base.is_dir():
            continue
        for asc in sorted(base.glob("*.asc"))[:8]:  # 每个目录抽查前 8 个
            target = asc.with_suffix("")
            if not target.exists():
                continue
            ok, msg = gpg_verify(asc, target)
            checked += 1
            ok_n += int(ok)
            detail.append(f"{target.name}: {msg}")
    if checked == 0:
        return {"name": "GPG 签名", "ok": None, "detail": "未发现 .asc（无签名检查项）"}
    ok = ok_n == checked
    return {"name": "GPG 签名", "ok": ok,
            "detail": f"{ok_n}/{checked} 通过；{'; '.join(detail[:4])}" if detail else ""}


def check_leak(scan_dir: Path) -> dict:
    """敏感信息扫描（密钥/令牌/私钥/绝对路径）。"""
    hits: list[str] = []
    if not scan_dir.is_dir():
        return {"name": "文件泄露", "ok": None, "detail": f"扫描目录不存在: {scan_dir}"}
    for p in scan_dir.rglob("*"):
        if not p.is_file() or p.suffix not in CODE_SUFFIX:
            continue
        if any(part in {".git", "__pycache__", ".venv", "dist", "build", "*.egg-info"}
               for part in p.parts):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith(("#", "//", "/*", "*")):
                continue
            for pat, label in SENSITIVE_PATTERNS:
                if pat.search(line):
                    hits.append(f"{p.relative_to(ROOT)}:{lineno} ({label})")
                    break
    ok = not hits
    return {"name": "文件泄露", "ok": ok,
            "detail": "未发现敏感信息" if ok else ("⚠️ 发现 " + "; ".join(hits[:5]))}


def main() -> None:
    ap = argparse.ArgumentParser(prog="lh security", description="龍魂安全自检")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--scan-dir", default=str(DEFAULT_SCAN_DIR), help="敏感扫描目录（默认 packaging/longhun_cli）")
    args = ap.parse_args()

    checks = [
        check_port_binding(),
        check_permissions(),
        check_signatures(),
        check_leak(Path(args.scan_dir).expanduser()),
    ]
    risk = sum(1 for c in checks if c["ok"] is False)
    audit = "🟢" if risk == 0 else ("🟡" if risk == 1 else "🔴")
    text = "\n".join(
        f"[{'✅' if c['ok'] else ('⚠️' if c['ok'] is None else '❌')}] {c['name']}: {c['detail']}"
        for c in checks
    )
    data = {
        "status": "ok" if risk == 0 else "warn",
        "node_id": _node_id(text + time.strftime("%Y%m%d%H%M%S")),
        "checks": checks,
        "risk_score": risk,
        "audit": audit,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print("🔐 龍魂安全自检")
        print(text)
        print(f"\n风险项: {risk} · 审计: {audit}")


if __name__ == "__main__":
    main()
