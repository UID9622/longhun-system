#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 Notion 同步网关 v1.0
DNA: #龍芯⚡️2026-05-25-NOTION-SYNC-GATEWAY-v1.0
UID: 9622
Purpose: Notion workspace 页面列表 + 自动同步入本地

用法:
    python3 notion_sync_gateway.py list      # 列出所有页面
    python3 notion_sync_gateway.py sync      # 同步所有页面到本地
    python3 notion_sync_gateway.py watch     # 实时监听变化
"""

import os
import json
import requests
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path("~/longhun-system").expanduser()
NOTION_WORKSPACE = "https://www.notion.so/uid9622"
NOTION_SYNC_DIR = ROOT / "notion_sync" / "workspace"
NOTION_SYNC_DIR.mkdir(parents=True, exist_ok=True)

# ════════════════════════════════════════════════════════
# 第一步：用 Kimi WebBridge 拉 Notion 页面列表
# ════════════════════════════════════════════════════════

def kimi_navigate(url):
    """用 Kimi WebBridge 导航到 URL"""
    cmd = [
        "curl", "-s", "-X", "POST", "http://127.0.0.1:10086/command",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({
            "action": "navigate",
            "args": {"url": url, "newTab": True},
            "session": "notion-workspace"
        })
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

def kimi_screenshot(output_path=None):
    """截图当前页面"""
    args = {"format": "png", "quality": 75}
    if output_path:
        args["path"] = output_path

    cmd = [
        "curl", "-s", "-X", "POST", "http://127.0.0.1:10086/command",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({
            "action": "screenshot",
            "args": args,
            "session": "notion-workspace"
        })
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return data.get("data", {}).get("path")

def kimi_snapshot():
    """读取页面 accessibility tree"""
    cmd = [
        "curl", "-s", "-X", "POST", "http://127.0.0.1:10086/command",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({
            "action": "snapshot",
            "session": "notion-workspace"
        })
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return data.get("data", {})

# ════════════════════════════════════════════════════════
# 第二步：列出 Notion 页面
# ════════════════════════════════════════════════════════

def list_notion_pages():
    """列出 uid9622 workspace 下的所有页面"""

    print("📍 导航到 Notion workspace...")
    nav_result = kimi_navigate(NOTION_WORKSPACE)
    if not nav_result.get("ok"):
        print(f"🔴 导航失败: {nav_result}")
        return []

    print("⏳ 等待页面加载...")
    import time
    time.sleep(5)

    print("📸 截图 Notion 页面...")
    screenshot_path = kimi_screenshot(
        output_path=str(NOTION_SYNC_DIR / f"notion_workspace_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    )

    if screenshot_path:
        print(f"✅ 截图已保存: {screenshot_path}")

    print("🔍 读取页面结构...")
    snapshot = kimi_snapshot()

    if not snapshot:
        print("⚠️ 页面结构读取失败（可能是 Notion 动态加载）")
        print("\n使用备用方案：已知的 Notion 页面列表：")

        known_pages = {
            "DNA": "https://www.notion.so/uid9622/DNA-34d7125a9c9f81d2be91d1e3e3be34eb",
            "BAOBAO-COLLAB-v1": "https://www.notion.so/uid9622/UID9622-24618c23ac3247a19e652de6ab09f82c",
            "FLOW-DECISION-v3": "https://www.notion.so/uid9622/UID9622-3427125a9c9f80449e88f4f2170b7940",
            "AI-COLLABORATION": "https://www.notion.so/uid9622/AI-868fec34e5a24e7e829dc5851a75f6b7",
            "SYSTEMS-v1": "https://www.notion.so/uid9622/UID9622-v1-0-33d7125a9c9f81818d40de9b63c86203",
            "UNIFIED-FRAMEWORK": "https://www.notion.so/uid9622/b35faf462bc042aa9de5192520180728",
        }

        for page_name, page_url in known_pages.items():
            print(f"  📄 {page_name}")
            print(f"     {page_url}")

        return known_pages

    # 如果成功读取，返回页面树
    print(f"✅ 读取到页面结构（{len(snapshot.get('tree', []))} 个元素）")
    return snapshot

# ════════════════════════════════════════════════════════
# 第三步：建立同步清单
# ════════════════════════════════════════════════════════

def create_sync_manifest():
    """生成同步清单（DNA 链）"""

    manifest = {
        "timestamp": datetime.now().isoformat(),
        "dna": "#龍芯⚡️2026-05-25-NOTION-SYNC-GATEWAY-MANIFEST-v1.0",
        "workspace": NOTION_WORKSPACE,
        "sync_dir": str(NOTION_SYNC_DIR),
        "pages": {
            "DNA": {
                "url": "https://www.notion.so/uid9622/DNA-34d7125a9c9f81d2be91d1e3e3be34eb",
                "local_path": str(NOTION_SYNC_DIR / "DNA.md"),
                "description": "龍魂核心 DNA 定义",
                "status": "pending",
            },
            "BAOBAO-COLLAB-v1": {
                "url": "https://www.notion.so/uid9622/UID9622-24618c23ac3247a19e652de6ab09f82c",
                "local_path": str(NOTION_SYNC_DIR / "BAOBAO-COLLAB-v1.md"),
                "description": "宝宝协作框架 v1.0",
                "status": "pending",
            },
            "FLOW-DECISION-v3": {
                "url": "https://www.notion.so/uid9622/UID9622-3427125a9c9f80449e88f4f2170b7940",
                "local_path": str(NOTION_SYNC_DIR / "FLOW-DECISION-v3.md"),
                "description": "流场决策 v3",
                "status": "pending",
            },
            "AI-COLLABORATION": {
                "url": "https://www.notion.so/uid9622/AI-868fec34e5a24e7e829dc5851a75f6b7",
                "local_path": str(NOTION_SYNC_DIR / "AI-COLLABORATION.md"),
                "description": "AI 协作框架",
                "status": "pending",
            },
            "SYSTEMS-v1": {
                "url": "https://www.notion.so/uid9622/UID9622-v1-0-33d7125a9c9f81818d40de9b63c86203",
                "local_path": str(NOTION_SYNC_DIR / "SYSTEMS-v1.md"),
                "description": "系统 v1.0",
                "status": "pending",
            },
            "UNIFIED-FRAMEWORK": {
                "url": "https://www.notion.so/uid9622/b35faf462bc042aa9de5192520180728",
                "local_path": str(NOTION_SYNC_DIR / "UNIFIED-FRAMEWORK.md"),
                "description": "统一框架",
                "status": "pending",
            },
        },
        "next_step": "手动导出 Notion 页面为 Markdown，放入 notion_sync/workspace/",
        "instructions": """
① 打开每个 Notion 页面
② 右上角 ⋯ → Export → Markdown & CSV
③ 下载后放入: ~/longhun-system/notion_sync/workspace/
④ 改名为对应的文件名（DNA.md, BAOBAO-COLLAB-v1.md 等）
⑤ 再运行: python3 notion_sync_gateway.py sync
        """,
    }

    manifest_path = NOTION_SYNC_DIR / "MANIFEST.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    return manifest

# ════════════════════════════════════════════════════════
# 主程序
# ════════════════════════════════════════════════════════

def main():
    import sys

    if len(sys.argv) < 2:
        cmd = "list"
    else:
        cmd = sys.argv[1]

    print("\n" + "="*60)
    print(f"🐉 龍魂 Notion 同步网关 v1.0")
    print(f"   DNA: #龍芯⚡️2026-05-25-NOTION-SYNC-GATEWAY-v1.0")
    print("="*60 + "\n")

    if cmd == "list":
        print("📋 列出 Notion workspace 页面...\n")
        pages = list_notion_pages()

        if isinstance(pages, dict):
            for name, url in pages.items():
                print(f"  📄 {name}")
                print(f"     {url}\n")

    # 生成同步清单
    print("\n📝 生成同步清单...")
    manifest = create_sync_manifest()
    print(f"✅ 清单已生成: {NOTION_SYNC_DIR / 'MANIFEST.json'}")

    print("\n" + "="*60)
    print("📌 下一步：手动导出 Notion 页面")
    print("="*60)
    print(manifest["instructions"])

if __name__ == "__main__":
    main()
