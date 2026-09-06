#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 自托管收款钱包 v1.1（多链）
DNA: #龍芯⚡️丙午·丁酉·壬午·辰时-䷙大畜-LONGHUN-WALLET-v1.1-MULTICHAIN-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)（工程实现层）
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能（多链收款登记·D1级·密钥仅本地/钱包App·AI 永不接触私钥）:
  init                    生成自托管 SOL 钱包(ed25519·cryptography 成熟库·权限600·已有则拒绝覆盖)
  register <net> <addr>   登记外部自持钱包公开地址(如 tron/btc/eth·无种子·密钥在钱包App·地址=银行卡号可公开)
  address [net]           输出收款地址(无参=全部链·不输出私钥)
  qr [net]                生成二维码(默认网络→donate.png·其余→donate-<net>.png·内容=地址文本全钱包可扫)
  status                  全部网络配置状态·默认收款链
  show-seed [net]         打印自托管种子(仅 solana·永不打印到日志/远程)

登记原则(老大 2026-08-31 定·焊死):
  地址 = 银行卡号 → 可公开、可到处放。
  私钥/助记词 = 保险柜钥匙 → 只在钱包App(TokenPocket)内·AI 不接触·永不登记。
  官方主收款 = TRON(USDT-TRC20)·TokenPocket(华为手机) · SOL 为自托管次链。

周一公司账户落地: 改 crypto.json networks 段+跑 `lh wallet qr` 即可,机制零代码改动。
用法:
  python3 08_BIN/lh_wallet.py init|register|address|qr|status|show-seed
  lh wallet init|register|address|qr|status|show-seed
"""

import os
import sys
import json
from datetime import datetime, timezone, timedelta

CRYPTO_FILE = os.path.expanduser("~/.longhun/crypto.json")
STATIC_DIR = os.path.expanduser("~/.longhun/static")
DEFAULT_QR = "donate.png"  # 默认网络收款图(向后兼容 /donate.png 静态路由)

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
CST = timezone(timedelta(hours=8))

# 已知外部钱包元数据(登记时自动带入·可被 crypto.json 覆盖)
KNOWN_META = {
    "tron": {
        "symbol": "USDT-TRC20 / TRX",
        "custody": "TokenPocket(老大华为手机)·密钥自持·AI不接触",
        "chain_balance_hint": "链上余额需 TokenPocket / 区块浏览器查看",
    },
}


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


def _networks(cfg) -> dict:
    return cfg.get("networks") or {}


def validate_address(net: str, addr: str) -> bool:
    """轻量格式校验(防手滑错抄·非链上验证)。地址合法性以钱包App为准。"""
    if not addr or not all(c in BASE58_ALPHABET for c in addr):
        return False
    if net == "solana":
        return len(addr) in (32, 44)
    if net == "tron":
        return len(addr) == 34 and addr.startswith("T")
    return len(addr) >= 26


def _qr_path(cfg: dict, net: str) -> str:
    """默认网络→donate.png(兼容静态路由)·其余→donate-<net>.png"""
    if net == cfg.get("default_network"):
        return os.path.join(STATIC_DIR, DEFAULT_QR)
    return os.path.join(STATIC_DIR, f"donate-{net}.png")


def cmd_init():
    cfg = _load()
    if cfg and _networks(cfg).get("solana", {}).get("address"):
        print("🟡 钱包已存在,拒绝覆盖(防误生成丢失私钥)。改地址请手动编辑 crypto.json 后跑 `lh wallet qr`")
        return 1
    seed_b58, addr = sol_wallet()
    cfg = cfg or {"version": 1, "updated_at": _now(), "default_network": "solana",
                  "note": "多链收款·种子仅本地~/.longhun(600)·官方主收款见 networks.tron(外部钱包自持)·周一公司账户落地可整体换"}
    nets = _networks(cfg)
    nets["solana"] = {
        "symbol": "SOL / USDC(Solana)",
        "address": addr,
        "seed_b58": seed_b58,
        "qr_content": addr,
        "custody": "自托管·种子本地·AI可出示地址不可碰种子",
    }
    if cfg.get("default_network") == "solana":
        cfg["default_network"] = "solana"
    cfg["updated_at"] = _now()
    _store(cfg)
    os.makedirs(STATIC_DIR, exist_ok=True)
    print("✅ SOL 自托管钱包已生成(ed25519·本地·权限600)")
    print(f"  地址: {addr}")
    print("  ⚠️ 私钥=种子,请即刻执行 `lh wallet show-seed solana` 抄录冷备份,种子丢失=资产永久丢失")
    return 0


def cmd_register(net: str, addr: str, as_default: bool = False):
    """登记外部自持钱包公开地址(如 tron)。密钥在钱包App·此处只录地址+元数据。"""
    net = net.lower()
    if not validate_address(net, addr):
        print(f"🔴 地址格式校验失败(net={net}·len={len(addr)})。Tron 需 T 开头 34 位 base58。")
        return 1
    cfg = _load()
    nets = _networks(cfg)
    existing = nets.get(net, {}).get("address", "")
    if existing and existing != addr:
        print(f"🔴 网络 {net} 已有地址 {existing[:8]}…,拒绝覆盖。改地址请手动编辑 crypto.json(需老大确认)。")
        return 1
    meta = dict(KNOWN_META.get(net, {}))
    meta.update({"address": addr, "qr_content": addr,
                 "registered_at": _now(),
                 "custody": meta.get("custody", "外部钱包·密钥自持·AI不接触")})
    nets[net] = meta
    if as_default or not cfg.get("default_network") or not nets.get(cfg["default_network"], {}).get("address"):
        cfg["default_network"] = net
    cfg["updated_at"] = _now()
    _store(cfg)
    print(f"✅ 已登记 {net} 收款地址(公开·密钥仍在钱包App)")
    print(f"  地址: {addr}")
    print(f"  默认收款链: {cfg['default_network']}")
    return 0


def cmd_address(net: str | None = None):
    cfg = _load()
    if not cfg:
        print("🟡 钱包未初始化: `lh wallet init`(自托管SOL) 或 `lh wallet register tron <地址>`(官方钱包)")
        return 1
    nets = _networks(cfg)
    if net:
        node = nets.get(net.lower())
        if not node or not node.get("address"):
            print(f"🟡 网络 {net} 未登记")
            return 1
        print(node["address"])
        return 0
    if not nets:
        print("🟡 无已登记收款网络")
        return 1
    for name, node in nets.items():
        if node.get("address"):
            print(f"{name}: {node['address']}")
    return 0


def _make_qr(addr: str, path: str) -> bool:
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
    img.save(path)
    return True


def cmd_qr(net: str | None = None):
    cfg = _load()
    if not cfg:
        print("🟡 钱包未初始化: 先 `lh wallet init` 或 `lh wallet register tron <地址>`")
        return 1
    nets = _networks(cfg)
    targets = [net.lower()] if net else [n for n, v in nets.items() if v.get("address")]
    if not targets:
        print("🟡 无已登记收款网络")
        return 1
    for name in targets:
        node = nets.get(name)
        if not node or not node.get("address"):
            print(f"🟡 网络 {name} 未登记,跳过")
            continue
        path = _qr_path(cfg, name)
        if not _make_qr(node["address"], path):
            print(f"🔴 {name} 二维码生成失败(缺 qrcode 库? pip3 install qrcode)")
            return 1
        node["qr_file"] = os.path.basename(path)
        node["qr_at"] = _now()
        print(f"✅ {name} 二维码已刷新: {path}")
        print(f"  内容: {node['address']}(纯文本·全钱包可扫)")
    cfg["updated_at"] = _now()
    _store(cfg)
    return 0


def cmd_status():
    cfg = _load()
    if not cfg:
        print("🟡 钱包未初始化")
        return 1
    nets = _networks(cfg)
    if not nets:
        print("🟡 钱包已初始化但无收款网络(crypto.json 为空 networks)")
        return 1
    print(f"默认收款: {cfg.get('default_network', '?')}")
    print("-" * 46)
    for name, node in nets.items():
        if not node.get("address"):
            continue
        symbol = node.get("symbol", name)
        print(f"┌ {name} · {symbol}")
        print(f"│ 地址: {node['address']}")
        print(f"│ 保管: {node.get('custody', '?')}")
        qrf = node.get("qr_file")
        qrf_ok = qrf and os.path.exists(os.path.join(STATIC_DIR, qrf))
        print(f"│ QR  : {qrf if qrf_ok else '未生成(跑 lh wallet qr)'}")
        if node.get("seed_b58"):
            print(f"│ 种子: 本地已存(600)· show-seed 可查(勿外传)")
        print("└ 链上余额: " + node.get("chain_balance_hint", "未配置链上查询(钱包App/区块浏览器可见)"))
    return 0


def cmd_show_seed(net: str = "solana"):
    cfg = _load()
    if not cfg:
        print("🟡 钱包未初始化")
        return 1
    node = _networks(cfg).get(net)
    if not node:
        print(f"🟡 网络 {net} 未登记")
        return 1
    if not node.get("seed_b58"):
        print(f"🔴 {net} 是外部钱包(密钥在钱包App·AI 不接触),本地无种子,不可显示。")
        return 1
    print("⚠️  种子=私钥·仅本机显示·请抄录冷备份后按回车清除屏幕")
    input()
    print(node["seed_b58"])


def main():
    _self_test_base58()
    argv = sys.argv[1:]
    cmd = argv[0] if argv else "status"
    if cmd == "init":
        return cmd_init()
    if cmd == "register":
        if len(argv) < 3:
            print("用法: lh wallet register <net> <地址> [--default]\n  例: lh wallet register tron TCxxxx… --default")
            return 2
        return cmd_register(argv[1], argv[2], as_default="--default" in argv)
    if cmd == "address":
        return cmd_address(argv[1] if len(argv) > 1 else None)
    if cmd == "qr":
        return cmd_qr(argv[1] if len(argv) > 1 else None)
    if cmd == "status":
        return cmd_status()
    if cmd == "show-seed":
        return cmd_show_seed(argv[1] if len(argv) > 1 else "solana")
    print("用法: lh wallet init|register <net> <地址>|address [net]|qr [net]|status|show-seed [net]")
    return 2


if __name__ == "__main__":
    sys.exit(main())
