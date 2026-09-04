#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-04-LONGHUN-HARMONY-SCAFFOLD-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""🐉 lh harmony · 鸿蒙接入脚手架 v1.0（本机无 DevEco → 源码脚手架 + 自检，真构建留 DevEco）

用法:
  python3 08_BIN/lh_harmony.py guide                 # 打印接入指南路径
  python3 08_BIN/lh_harmony.py check [--root DIR]    # SDK/Demo 结构自检
  python3 08_BIN/lh_harmony.py init [--out DIR]      # 复制 SDK+Demo 模板到目标目录
  经 lh:  lh harmony <guide|check|init>
"""
import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HARMONY_DIR = ROOT / "packaging" / "harmony"
GUIDE = ROOT / "docs" / "鸿蒙接入龙魂数据层指南.md"

SDK_REQUIRED = [
    "notion-mcp-sdk/oh-package.json5",
    "notion-mcp-sdk/build-profile.json5",
    "notion-mcp-sdk/index.ets",
    "notion-mcp-sdk/src/main/module.json5",
    "notion-mcp-sdk/src/main/ets/common/Config.ets",
    "notion-mcp-sdk/src/main/ets/models/McpModels.ets",
    "notion-mcp-sdk/src/main/ets/models/CatalogModels.ets",
    "notion-mcp-sdk/src/main/ets/net/HttpInfo.ets",
    "notion-mcp-sdk/src/main/ets/net/RpcClient.ets",
    "notion-mcp-sdk/src/main/ets/client/QueryClient.ets",
    "notion-mcp-sdk/src/main/ets/client/NativeQuery.ets",
]

DEMO_REQUIRED = [
    "NotionMCPDemo/build-profile.json5",
    "NotionMCPDemo/oh-package.json5",
    "NotionMCPDemo/hvigorfile.ts",
    "NotionMCPDemo/AppScope/app.json5",
    "NotionMCPDemo/entry/oh-package.json5",
    "NotionMCPDemo/entry/build-profile.json5",
    "NotionMCPDemo/entry/hvigorfile.ts",
    "NotionMCPDemo/entry/src/main/module.json5",
    "NotionMCPDemo/entry/src/main/ets/entryability/EntryAbility.ets",
    "NotionMCPDemo/entry/src/main/ets/pages/Index.ets",
    "NotionMCPDemo/entry/src/main/resources/base/profile/main_pages.json",
]


def _rows_for(base: Path, rels: list) -> list:
    rows = []
    for rel in rels:
        p = base / rel
        ok = p.is_file() and p.stat().st_size > 0
        rows.append((rel, ok))
    return rows


def cmd_check(root: Path):
    rows = []
    rows += _rows_for(root, [f"README.md"] + SDK_REQUIRED + DEMO_REQUIRED)
    print(f"\n  📱 鸿蒙接入脚手架自检 · lh harmony check")
    print("  " + "=" * 46)
    ok_n = 0
    for rel, ok in rows:
        ok_n += 1 if ok else 0
        mark = "🟢" if ok else "🔴"
        print(f"  {mark} {rel}")
    print("  " + "=" * 46)
    print(f"  ✅ {ok_n}/{len(rows)} 项就绪" + ("  🟢 全绿" if ok_n == len(rows) else "  🔴 有缺失"))
    return ok_n == len(rows)


def cmd_init(out_dir: Path):
    if out_dir.exists() and any(out_dir.iterdir()):
        print(f"🔴 目标目录非空: {out_dir}（请换 --out 或先清空）")
        return False
    for name in ("notion-mcp-sdk", "NotionMCPDemo"):
        src = HARMONY_DIR / name
        if not src.is_dir():
            print(f"🔴 模板缺失: {src}")
            return False
        shutil.copytree(src, out_dir / name)
        print(f"  ✅ 已复制 {name}/")
    if (HARMONY_DIR / "README.md").is_file():
        shutil.copy2(HARMONY_DIR / "README.md", out_dir / "README.md")
        print(f"  ✅ 已复制 README.md")
    print(f"\n  📱 SDK+Demo 已生成到: {out_dir}")
    print(f"  下一步: DevEco Studio 打开 {out_dir / 'NotionMCPDemo'}")
    return True


def cmd_guide():
    print(f"  鸿蒙接入龙魂数据层指南: {GUIDE}" +
          ("（已就绪）" if GUIDE.is_file() else "（未生成·t5 待补）"))
    return True


def main():
    ap = argparse.ArgumentParser(description="lh harmony · 鸿蒙接入脚手架")
    ap.add_argument("cmd", nargs="?", default="guide", choices=["guide", "check", "init"])
    ap.add_argument("--root", default=str(HARMONY_DIR), help="自检根目录")
    ap.add_argument("--out", default="./harmony-notion", help="init 目标目录")
    a = ap.parse_args()
    ok = True
    if a.cmd == "check":
        ok = cmd_check(Path(a.root))
    elif a.cmd == "init":
        ok = cmd_init(Path(a.out).expanduser())
    else:
        ok = cmd_guide()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
