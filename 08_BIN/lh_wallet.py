#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 自托管收款钱包 v1.0
DNA: #龍芯⚡️2026-09-04-LONGHUN-WALLET-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)（工程实现层）
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能（自托管·种子仅本地物理隔离·主权不变让渡·D1级）:
  init            首次生成 SOL 钱包(ed25519·cryptography 成熟库·权限600·已有则拒绝覆盖)
  address         输出收款地址(不输出私钥)
  qr              生成/刷新 ~/.longhun/static/donate.png(内容=地址文本·全钱包可扫)
  status          配置状态·地址·QR 时间·降级提示
  show-seed       打印种子(仅老大本机抄录备份用·永不打印到日志/远程)

用法:
  python3 08_BIN/lh_wallet.py init|address|qr|status|show-seed
  lh wallet init|address|qr|status|show-seed

周一公司账户落地: 直接改 crypto.json networks 段+重跑 qr,机制零代码改动。
"""

import os
import sys
import json
from datetime import datetime, timezone, timedelta

CRYPTO_FILE = os.path.expanduser("~/.longhun/crypto.json")
STATIC_DIR = os.path.expanduser("~/.longhun/static")
QR_FILE = os.path.join(STATIC_DIR, "donate.png")

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
CST = timezone(timedelta(hours=8))


def base58_encode(b: bytes) -> str:
    n = int.from_bytes(b, "big")
    out = ""
    while n > 0:
        n, r = divmod(n, 58)
        out = BASE58_ALPHABET[r] + out
    pad = len(b) - len(b.lstrip(b"\x00"))
    return "1" * pad + (out or "")


def base58_decode(s: str) -> bytes:
    n = 0
    for ch in s:
        n = n * 58 + BASE58_ALPHABET.index(ch)
    body = n.to_bytes((n.bit_length() + 7) // 8 or 1, "big") if n else b""
    pad = len(s) - len(s.lstrip("1"))
    return b"\x00" * pad + body


def _self_test_base58():
    assert base58_encode(b"") == ""
    assert base58_encode(bytes([0])) == "1"
    v = bytes.fromhex("73696d706c792061206c6f6e6720737472696e67")
    assert base58_encode(v) == "2cFupjhnEsSn59qHXstmK2ffpLv2"
    assert base58_decode("2cFupjhnEsSn59qHXstmK2ffpLv2") == v


def sol_wallet():
    """ed25519 种子→SOL 地址。返回 (seed_b58, address)。成熟库实现·零手搓密码学。"""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
    seed = os.urandom(32)
    priv = Ed25519PrivateKey.from_private_bytes(seed)
    pub = priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)  # 32B
    # 自校验: 种子可重派生同一公钥
    assert Ed25519PrivateKey.from_private_bytes(seed).public_key().public_bytes(
        Encoding.Raw, PublicFormat.Raw) == pub
    return base58_encode(seed), base58_encode(pub)


def _now():
    return datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S%z")


def _load():
    if not os.path.exists(CRYPTO_FILE):
        return None
    try:
        return json.load(open(CRYPTO_FILE, encoding="utf-8"))
    except Exception:
        return None


def _store(cfg: dict):
    os.makedirs(os.path.dirname(CRYPTO_FILE), exist_ok=True)
    fd = os.open(CRYPTO_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    os.chmod(CRYPTO_FILE, 0o600)


def cmd_init():
    cfg = _load()
    if cfg and cfg.get("networks", {}).get("solana", {}).get("address"):
        print("🟡 钱包已存在,拒绝覆盖(防误生成丢失私钥)。改地址请手动编辑 crypto.json 后跑 `lh wallet qr`")
        return 1
    seed_b58, addr = sol_wallet()
    cfg = {
        "version": 1,
        "updated_at": _now(),
        "default_network": "solana",
        "note": "自托管·种子仅本地~/.longhun(600)·主权不变让渡·周一公司账户落地可整体换",
        "networks": {
            "solana": {
                "symbol": "SOL / USDC(Solana)",
                "address": addr,
                "seed_b58": seed_b58,
                "qr_content": addr,
            }
        },
    }
    _store(cfg)
    os.makedirs(STATIC_DIR, exist_ok=True)
    print("✅ SOL 钱包已生成(ed25519·本地·权限600)")
    print(f"  地址: {addr}")
    print("  ⚠️ 私钥=种子,请即刻执行 `lh wallet show-seed` 抄录冷备份,种子丢失=资产永久丢失")
    return 0


def cmd_address():
    cfg = _load()
    if not cfg:
        print("🟡 钱包未初始化: 执行 `lh wallet init`(生成自托管SOL地址·权限600)")
        return 1
    print(cfg["networks"]["solana"]["address"])


def _make_qr(addr: str) -> str:
    import qrcode
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
    from qrcode.image.styles.colormasks import SolidFillColorMask
    os.makedirs(STATIC_DIR, exist_ok=True)
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=3)
    qr.add_data(addr)
    qr.make(fit=True)
    img = qr.make_image(image_factory=StyledPilImage,
                        module_drawer=RoundedModuleDrawer(),
                        color_mask=SolidFillColorMask((24, 32, 54), (230, 180, 60)),
                        embeded_image_path=None)
    img.save(QR_FILE)
    return QR_FILE


def cmd_qr():
    cfg = _load()
    if not cfg:
        print("🟡 钱包未初始化: 先 `lh wallet init` 再生成二维码")
        return 1
    addr = cfg["networks"]["solana"]["address"]
    _make_qr(addr)
    cfg["updated_at"] = _now()
    cfg.setdefault("networks", {}).setdefault("solana", {})["qr_at"] = _now()
    _store(cfg)
    print(f"✅ 二维码已刷新: {QR_FILE}")
    print(f"  内容: {addr}(纯文本·全钱包可扫)")


def cmd_status():
    cfg = _load()
    if not cfg:
        print("🟡 钱包未初始化")
        return 1
    n = cfg["networks"]["solana"]
    print(f"网络   : {n.get('symbol', 'solana')}")
    print(f"地址   : {n['address']}")
    print(f"配置时间: {cfg.get('updated_at', '?')}")
    print(f"QR    : {'已生成 ' + os.path.basename(QR_FILE) if os.path.exists(QR_FILE) else '未生成(跑 lh wallet qr)'}")
    print("链上余额: 未配置链上查询(自托管·需要时用钱包App/区块浏览器查看)")


def cmd_show_seed():
    cfg = _load()
    if not cfg:
        print("🟡 钱包未初始化")
        return 1
    print("⚠️  种子=私钥·仅本机显示·请抄录冷备份后按回车清除屏幕")
    input()
    print(cfg["networks"]["solana"].get("seed_b58", "(缺失)"))


def main():
    _self_test_base58()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    fn = {"init": cmd_init, "address": cmd_address, "qr": cmd_qr,
          "status": cmd_status, "show-seed": cmd_show_seed}.get(cmd)
    if not fn:
        print("用法: lh wallet init|address|qr|status|show-seed")
        return 2
    return fn()


if __name__ == "__main__":
    sys.exit(main())
