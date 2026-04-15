#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂资源管家 · 三层省算力查询引擎

DNA追溯码: #龍芯⚡️2026-03-18-资源管家-v1.0
GPG指纹:  A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者:   UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）
创作地:   中华人民共和国
协议:     Apache License 2.0

【三层架构】
  第一层 总索引  → 始终在内存，极省算力（~5KB）
  第二层 封印包  → 命中关键词才加载摘要（~2KB/个）
  第三层 原始文件 → 只有明确需要深入才读取

【用法】
  python3 资源管家.py                    # 显示总览
  python3 资源管家.py 搜索 元字           # 搜索关键词
  python3 资源管家.py 展开 字体元字引擎   # 展开封印包详情
  python3 资源管家.py 私密               # 查看私密区目录
  python3 资源管家.py 模板               # 查看模板列表
"""

import json
import sys
import os
from pathlib import Path

BASE = Path.home() / "longhun-system"
总索引路径 = BASE / "总索引.json"
封印库路径 = BASE / "封印库"
私密区路径 = BASE / "私密区"
模板库路径 = BASE / "模板库"


def 加载总索引():
    """第一层：只加载索引，极省算力"""
    if not 总索引路径.exists():
        print("❌ 总索引不存在，请检查 ~/longhun-system/总索引.json")
        sys.exit(1)
    with open(总索引路径, encoding="utf-8") as f:
        return json.load(f)


def 加载封印包(封印包相对路径: str) -> dict:
    """第二层：按需加载封印包"""
    路径 = BASE / 封印包相对路径
    if not 路径.exists():
        return {}
    with open(路径, encoding="utf-8") as f:
        return json.load(f)


def 显示总览():
    """默认视图：只显示索引摘要，不展开内容"""
    索引 = 加载总索引()
    print(f"\n{'='*55}")
    print(f"  龍魂资源管家 · 总索引")
    print(f"  DNA: {索引.get('_DNA','')}")
    print(f"{'='*55}")

    封印资产 = 索引.get("封印资产", [])
    print(f"\n📦 封印资产（{len(封印资产)}个，已固定不改）")
    for i, 资产 in enumerate(封印资产, 1):
        状态图标 = "🔒" if 资产.get("状态") == "封印" else "✏️"
        关键词 = " ".join(f"#{k}" for k in 资产.get("关键词", [])[:3])
        print(f"  {i}. {状态图标} {资产['名称']:<18} {资产['类型']:<10} {关键词}")

    私密资产 = 索引.get("私密资产", [])
    print(f"\n🔒 私密资产（{len(私密资产)}个，永不上云）")
    for 资产 in 私密资产:
        print(f"  · {资产['名称']:<12} 📁 {资产['本地路径']}")

    活跃资产 = 索引.get("活跃资产", [])
    print(f"\n⚡ 活跃资产（{len(活跃资产)}个）")
    for 资产 in 活跃资产:
        print(f"  · {资产['名称']:<16} {资产.get('状态','')}")

    模板 = 索引.get("模板库", [])
    print(f"\n📐 模板库（{len(模板)}个，钉死不改）")
    for t in 模板:
        print(f"  · {t['名称']:<20} 适用：{t['适用']}")

    print(f"\n💡 用法: python3 资源管家.py 搜索 <关键词>")
    print(f"         python3 资源管家.py 展开 <资产名称>\n")


def 搜索(关键词: str):
    """关键词搜索，命中才展开封印包摘要"""
    索引 = 加载总索引()
    命中 = []

    for 资产 in 索引.get("封印资产", []):
        if (关键词 in 资产["名称"] or
                关键词 in 资产.get("描述", "") or
                any(关键词 in k for k in 资产.get("关键词", []))):
            命中.append(("封印资产", 资产))

    for 资产 in 索引.get("私密资产", []):
        if 关键词 in 资产["名称"] or 关键词 in 资产.get("描述", ""):
            命中.append(("私密资产", 资产))

    for 资产 in 索引.get("活跃资产", []):
        if 关键词 in 资产["名称"] or 关键词 in 资产.get("描述", ""):
            命中.append(("活跃资产", 资产))

    if not 命中:
        print(f"\n🔍 未找到「{关键词}」相关资产")
        return

    print(f"\n🔍 搜索「{关键词}」· 命中 {len(命中)} 个\n")
    for 分类, 资产 in 命中:
        print(f"  [{分类}] {资产['名称']}")
        print(f"    {资产.get('描述','')}")

        # 命中才展开封印包摘要（第二层）
        封印包路径 = 资产.get("封印包", "")
        if 封印包路径:
            封印包 = 加载封印包(封印包路径)
            if 封印包:
                print(f"    摘要: {封印包.get('摘要','')}")
                print(f"    深入: {封印包.get('深入命令','')}")
        print()


def 展开(资产名称: str):
    """展开指定封印包的完整信息（第二层）"""
    索引 = 加载总索引()

    目标 = None
    for 资产 in 索引.get("封印资产", []):
        if 资产名称 in 资产["名称"] or 资产["名称"] in 资产名称:
            目标 = 资产
            break

    if not 目标:
        print(f"\n❌ 未找到「{资产名称}」，请用完整名称或关键词")
        print("   可用资产:", [r["名称"] for r in 索引.get("封印资产", [])])
        return

    封印包 = 加载封印包(目标["封印包"])
    if not 封印包:
        print(f"❌ 封印包文件不存在: {目标['封印包']}")
        return

    print(f"\n{'='*55}")
    print(f"  🔒 封印包详情 · {封印包['名称']}")
    print(f"{'='*55}")
    print(f"  DNA:    {封印包['DNA']}")
    print(f"  版本:   {封印包.get('版本','')}")
    print(f"  协议:   {封印包.get('协议','')}")
    print(f"  封印日期: {封印包.get('封印日期','')}")
    print(f"\n  摘要:\n  {封印包.get('摘要','')}")

    核心文件 = 封印包.get("核心文件", [])
    if 核心文件:
        print(f"\n  核心文件（{len(核心文件)}个）:")
        for f in 核心文件:
            print(f"    · {f['文件']}")
            print(f"      {f['说明']}")

    命令速查 = 封印包.get("命令速查", {})
    if 命令速查:
        print(f"\n  命令速查:")
        for 名, 命令 in 命令速查.items():
            print(f"    {名}: {命令}")

    深入 = 封印包.get("深入命令", "")
    if 深入:
        print(f"\n  深入原始文件: {深入}")
    print()


def 查看私密区():
    """显示私密区目录结构（不展示内容）"""
    print(f"\n🔒 私密区 · 永不同步 · 只在本地")
    print(f"   路径: {私密区路径}\n")
    for 子目录 in 私密区路径.iterdir():
        if 子目录.is_dir():
            文件数 = len(list(子目录.glob("*")))
            print(f"  📁 {子目录.name}/ · {文件数}个文件")
    print(f"\n  引用规则: Notion只写路径引用，内容永远本地\n")


def 查看模板():
    """显示模板库"""
    print(f"\n📐 模板库 · 钉死不改\n")
    for 文件 in 模板库路径.glob("*.txt"):
        print(f"  · {文件.name}")
    print(f"\n  路径: {模板库路径}\n")


def main():
    if len(sys.argv) == 1:
        显示总览()
    elif sys.argv[1] == "搜索" and len(sys.argv) >= 3:
        搜索(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "展开" and len(sys.argv) >= 3:
        展开(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "私密":
        查看私密区()
    elif sys.argv[1] == "模板":
        查看模板()
    else:
        print("用法:")
        print("  python3 资源管家.py              # 总览")
        print("  python3 资源管家.py 搜索 元字     # 搜索")
        print("  python3 资源管家.py 展开 字体元字引擎  # 展开详情")
        print("  python3 资源管家.py 私密          # 私密区")
        print("  python3 资源管家.py 模板          # 模板库")


if __name__ == "__main__":
    main()
