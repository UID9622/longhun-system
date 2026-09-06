#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 收款钱包 MCP Server v1.0（只读·永不输出私钥/种子）
DNA: #龍芯⚡️2026-09-04-LONGHUN-WALLET-MCP-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

工具（全部只读·数据源 ~/.longhun/crypto.json·周一换地址零代码）:
  wallet_address   输出收款地址(多链·默认链+全部网络)与网络信息
  wallet_qr        输出打赏二维码 PNG 路径与最近刷新时间
  wallet_status    钱包配置状态(多链地址/QR/降级提示·无链上余额造假)

用法: mcp.json 配 command=python3 args=[本文件]
"""
import asyncio
import json
import os

from mcp.server import Server  # pyright: ignore[reportMissingImports]
from mcp.server.stdio import stdio_server  # pyright: ignore[reportMissingImports]
from mcp.types import Tool, TextContent  # pyright: ignore[reportMissingImports]

app = Server("longhun-wallet")

CRYPTO_FILE = os.path.expanduser("~/.longhun/crypto.json")
QR_FILE = os.path.expanduser("~/.longhun/static/donate.png")


def _cfg():
    if not os.path.exists(CRYPTO_FILE):
        return None
    try:
        return json.load(open(CRYPTO_FILE, encoding="utf-8"))
    except Exception:
        return None


def _ok(**kw) -> TextContent:
    body = {"ok": True, **kw}
    return TextContent(type="text", text=json.dumps(body, ensure_ascii=False, indent=2))


def _err(msg: str) -> TextContent:
    body = {"ok": False, "error": msg,
            "hint": "先跑 `lh wallet init/register`(多链·私钥仅本地/钱包App)"}
    return TextContent(type="text", text=json.dumps(body, ensure_ascii=False, indent=2))


def _public_networks(cfg: dict) -> dict:
    """只暴露公开地址·seed/custody 细节不外传。"""
    out = {}
    for name, node in (cfg.get("networks") or {}).items():
        addr = node.get("address", "")
        if not addr:
            continue
        out[name] = {"symbol": node.get("symbol", name), "address": addr}
    return out


@app.list_tools()  # pyright: ignore[reportUntypedFunctionDecorator]
async def list_tools() -> list[Tool]:  # pyright: ignore[reportUnknownVariableType]
    empty_schema: dict = {"type": "object", "properties": {}}
    return [
        Tool(name="wallet_address",
             description="龍魂收款地址(多链: TRON官方 USDT-TRC20 + SOL/USDC自托管)·含默认链/配置时间。只返回地址,永不返回私钥。",
             inputSchema=empty_schema),
        Tool(name="wallet_qr",
             description="龍魂打赏二维码 PNG 路径与刷新时间(默认链=donate.png·内容=地址全钱包可扫)。",
             inputSchema=empty_schema),
        Tool(name="wallet_status",
             description="钱包状态: 多链地址/QR/保管方式/降级提示。链上余额未配置则不返回(不造假)。",
             inputSchema=empty_schema),
    ]


@app.call_tool()  # pyright: ignore[reportUntypedFunctionDecorator]
async def call_tool(name: str, arguments: dict[str, object]) -> list[TextContent]:  # pyright: ignore[reportUnknownVariableType]
    cfg = _cfg()
    if name == "wallet_status":
        if not cfg:
            return [_err("钱包未初始化")]
        pub = _public_networks(cfg)
        if not pub:
            return [_err("无已登记收款网络")]
        dft = cfg.get("default_network") or next(iter(pub))
        return [_ok(default_network=dft,
                    networks=pub,
                    configured_at=cfg.get("updated_at", ""),
                    qr_exists=os.path.exists(QR_FILE),
                    qr_path=QR_FILE if os.path.exists(QR_FILE) else None,
                    chain_balance="未配置链上查询(私钥在钱包App·到账以钱包App为准)")]
    if name == "wallet_address":
        if not cfg:
            return [_err("钱包未初始化")]
        pub = _public_networks(cfg)
        if not pub:
            return [_err("无已登记收款网络")]
        dft = cfg.get("default_network") or next(iter(pub))
        return [_ok(default_network=dft, networks=pub)]
    if name == "wallet_qr":
        if not cfg:
            return [_err("钱包未初始化")]
        if not os.path.exists(QR_FILE):
            return [_ok(ok=False, error="二维码未生成",
                        hint="先跑 `lh wallet qr`(读 ~/.longhun/crypto.json 刷新二维码)")]
        dft = cfg.get("default_network") or "solana"
        net = ((cfg.get("networks") or {}).get(dft) or {})
        return [_ok(network=dft, address=net.get("address", ""), qr_path=QR_FILE,
                    qr_content=net.get("qr_content", ""),
                    refreshed_at=net.get("qr_at") or cfg.get("updated_at", ""))]
    return [_err(f"未知工具: {name}")]


async def main():
    async with stdio_server() as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
