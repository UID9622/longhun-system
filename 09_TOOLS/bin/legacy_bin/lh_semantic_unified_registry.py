#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂系统 · 语义统一注册表查询引擎 v2.0
============================================
DNA: #龍芯⚡️2026-07-14-SEMANTIC-UNIFIED-REGISTRY-ENGINE-v2.0
用途: 统一查询和管理龍魂系统所有专业术语、技能、引擎、密码学、七因子等概念
设计: 一个入口，查遍全系统所有专业概念。消除重复、统一命名、建立关联。
v2.0新增: 量子/时空织网/BraKet/CNSH/文化输出/Notion/论文引用/模9详解/三才25公式

用法:
  python3 bin/lh_semantic_unified_registry.py search <关键词>    # 搜索
  python3 bin/lh_semantic_unified_registry.py list <分类>        # 列出分类
  python3 bin/lh_semantic_unified_registry.py info <条目名>      # 查看详情
  python3 bin/lh_semantic_unified_registry.py xref <条目名>      # 交叉引用
  python3 bin/lh_semantic_unified_registry.py stats              # 统计
  python3 bin/lh_semantic_unified_registry.py audit              # 命名审计
  python3 bin/lh_semantic_unified_registry.py export             # 导出
  python3 bin/lh_semantic_unified_registry.py ai-creation        # AI创作工具一览
  python3 bin/lh_semantic_unified_registry.py engines            # 引擎一览(含量子/时空)
  python3 bin/lh_semantic_unified_registry.py skills             # 技能全览
  python3 bin/lh_semantic_unified_registry.py papers             # 论文一览
  python3 bin/lh_semantic_unified_registry.py notion-pages       # Notion知识库页面
  python3 bin/lh_semantic_unified_registry.py quantum            # 量子体系引擎
"""
import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# ═══════════════════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════════════════
ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "01_技能庫" / "semantic_unified_registry.json"

CATEGORY_COLORS = {
    "CRYPTO": "🔐",
    "SEVEN_FACTOR": "🎯",
    "SEMANTIC": "📖",
    "AI_CREATION": "🎨",
    "ENGINE": "⚙️",
    "SKILL": "🛠️",
    "PERSONA": "👤",
    "ALGORITHM": "🧮",
    "QUANTUM": "⚛️",
    "SPACETIME": "🌌",
    "GOVERNANCE": "⚖️",
    "CNSH": "🐉",
    "CULTURE": "🏛️",
    "INFRA": "🏗️",
    "PROTOCOL": "📜",
    "DOMAIN": "🌐",
    "NOTION": "📝",
    "BIBLIOGRAPHY": "📚"
}


def load_registry() -> dict[str, Any]:
    """加载统一注册表"""
    if not REGISTRY_PATH.exists():
        print(f"❌ 注册表不存在: {REGISTRY_PATH}")
        sys.exit(1)
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def search(args):
    """搜索关键词"""
    registry = load_registry()
    keyword = args.keyword.lower()
    matches = []

    # 搜索所有分类
    for cat_key, cat_data in registry.get("categories", {}).items():
        # 搜索分类描述
        if keyword in cat_data.get("description", "").lower() or keyword in cat_key.lower():
            matches.append({
                "category": cat_key,
                "type": "category",
                "name": cat_data.get("description", "")[:80],
                "key": cat_key
            })

        # 搜索子条目
        for sub_type in ["core_concepts", "factors", "modules", "tools", "engines", 
                          "key_concepts", "matrix", "key_modules", "key_protocols",
                          "skill_locations", "longhun_skills_codebuddy", "longhun_skills_project",
                          "skill_library_docs", "stack_layers", "scenarios", "braket_engine",
                          "subsystems", "key_formulas", "top_pages", "gates", "layers",
                          "published", "crypto_references", "philosophy_references"]:
            sub_data = cat_data.get(sub_type, {})
            if isinstance(sub_data, dict):
                for item_key, item_val in sub_data.items():
                    searchable = json.dumps(item_val, ensure_ascii=False).lower()
                    if keyword in searchable or keyword in item_key.lower():
                        matches.append({
                            "category": cat_key,
                            "type": sub_type,
                            "name": item_val.get("name", item_val.get("name_zh", item_key)) if isinstance(item_val, dict) else str(item_val)[:80],
                            "key": item_key,
                            "detail": item_val if isinstance(item_val, dict) else str(item_val)
                        })
            elif isinstance(sub_data, list):
                for i, item_val in enumerate(sub_data):
                    searchable = json.dumps(item_val, ensure_ascii=False).lower()
                    if keyword in searchable:
                        name = item_val.get("title", item_val.get("name", item_val.get("ref", str(item_val)[:80]))) if isinstance(item_val, dict) else str(item_val)[:80]
                        matches.append({
                            "category": cat_key,
                            "type": sub_type,
                            "name": name,
                            "key": str(i),
                            "detail": item_val if isinstance(item_val, dict) else str(item_val)
                        })

    # 搜索交叉引用
    for ref_key, ref_desc in registry.get("cross_references", {}).items():
        if keyword in ref_key.lower() or keyword in str(ref_desc).lower():
            matches.append({
                "category": "CROSS_REF",
                "type": "xref",
                "name": ref_desc[:80],
                "key": ref_key
            })

    # 输出
    if not matches:
        print(f"\n🔍 未找到与 '{args.keyword}' 相关的条目")
        print(f"💡 试试: python3 bin/lh_semantic_unified_registry.py list 查看所有分类")
        return

    print(f"\n{'='*70}")
    print(f"🔍 搜索: '{args.keyword}' → {len(matches)} 条结果")
    print(f"{'='*70}\n")

    for i, m in enumerate(matches, 1):
        emoji = CATEGORY_COLORS.get(m["category"], "📌")
        print(f"  {i}. {emoji} [{m['category']}] {m['name']}")
        if isinstance(m.get("detail"), dict):
            desc = m["detail"].get("desc", m["detail"].get("description", ""))
            if desc:
                print(f"     └─ {desc[:120]}")
        print()


def list_category(args):
    """列出分类内容"""
    registry = load_registry()
    cat_key = args.category.upper()
    
    # 列出所有分类
    if cat_key == "ALL":
        print(f"\n{'='*70}")
        print(f"📋 龍魂系统·统一注册表 · 全部分类")
        print(f"{'='*70}\n")
        
        taxonomy = registry.get("taxonomy", {})
        for tk, tv in taxonomy.items():
            emoji = CATEGORY_COLORS.get(tk, "📌")
            print(f"  {emoji} **{tk}**: {tv}")
        
        print(f"\n{'─'*70}")
        print(f"共 {len(taxonomy)} 个分类")
        print(f"用法: python3 bin/lh_semantic_unified_registry.py list <分类代码>")
        return

    cat_data = registry.get("categories", {}).get(cat_key)
    if not cat_data:
        print(f"❌ 分类 '{cat_key}' 不存在。试试 --list all")
        return

    emoji = CATEGORY_COLORS.get(cat_key, "📌")
    print(f"\n{'='*70}")
    print(f"{emoji} 分类: {cat_key} — {registry['taxonomy'].get(cat_key, '')}")
    print(f"{'='*70}\n")
    print(f"  {cat_data.get('description', '')}\n")

    # 输出子条目
    sub_types = {
        "core_concepts": "核心概念",
        "stack_layers": "加密堆栈层",
        "factors": "因子",
        "scenarios": "场景权重",
        "modules": "模块",
        "tools": "工具",
        "engines": "引擎",
        "key_concepts": "关键概念",
        "key_formulas": "关键公式",
        "subsystems": "子系统",
        "gates": "闸门",
        "key_modules": "关键模块",
        "key_protocols": "关键协议",
        "skill_locations": "技能存放地",
        "longhun_skills_codebuddy": "CodeBuddy技能",
        "longhun_skills_project": "项目技能",
        "skill_library_docs": "技能庫文档",
        "braket_engine": "Bra-Ket引擎",
        "top_pages": "Notion核心页面",
        "published": "已发表论文",
        "crypto_references": "密码学参考文献",
        "philosophy_references": "哲学参考文献",
        "matrix": "人格矩阵",
        "layers": "层级定义"
    }

    for key, label in sub_types.items():
        items = cat_data.get(key, {})
        if isinstance(items, dict) and items:
            print(f"  ┌─ {label} ({len(items)}):")
            for item_key, item_val in items.items():
                name = item_val.get("name", item_val.get("name_zh", item_key))
                desc = item_val.get("desc", item_val.get("description", ""))
                if desc:
                    print(f"  │  • {name}: {desc[:100]}")
                else:
                    print(f"  │  • {name}")
            print()

    # 关键文件
    key_files = cat_data.get("key_files", [])
    if key_files:
        print(f"  ┌─ 关键文件 ({len(key_files)}):")
        for f in key_files[:10]:
            print(f"  │  • {f}")
        if len(key_files) > 10:
            print(f"  │  ... 还有 {len(key_files)-10} 个文件")


def show_info(args):
    """查看条目详情"""
    registry = load_registry()
    name = args.name.lower()
    
    for cat_key, cat_data in registry.get("categories", {}).items():
        for sub_type, sub_data in cat_data.items():
            if isinstance(sub_data, dict):
                for item_key, item_val in sub_data.items():
                    if name in item_key.lower():
                        emoji = CATEGORY_COLORS.get(cat_key, "📌")
                        print(f"\n{'='*70}")
                        print(f"{emoji} {item_val.get('name', item_val.get('name_zh', item_key))}")
                        print(f"{'='*70}")
                        print(f"  分类: {cat_key}")
                        print(f"  键: {item_key}")
                        print()
                        for k, v in item_val.items():
                            if k not in ["name", "name_zh"]:
                                if isinstance(v, dict):
                                    print(f"  {k}:")
                                    for k2, v2 in v.items():
                                        print(f"    • {k2}: {v2}")
                                elif isinstance(v, list):
                                    print(f"  {k}: {', '.join(str(x) for x in v)}")
                                else:
                                    print(f"  {k}: {v}")
                        return
    
    print(f"❌ 未找到条目: '{args.name}'")


def show_xref(args):
    """显示交叉引用"""
    registry = load_registry()
    name = args.name.lower()
    xrefs = registry.get("cross_references", {})
    
    matches = {}
    for key, desc in xrefs.items():
        if name in key.lower() or name in desc.lower():
            matches[key] = desc
    
    if not matches:
        print(f"\n❌ 未找到与 '{args.name}' 相关的交叉引用")
        print(f"\n已有的交叉引用:")
        for key, desc in xrefs.items():
            print(f"  • {key}: {desc[:100]}")
        return
    
    print(f"\n{'='*70}")
    print(f"🔗 交叉引用: '{args.name}'")
    print(f"{'='*70}\n")
    for key, desc in matches.items():
        print(f"  🔗 {key}")
        print(f"     └─ {desc}")
        print()


def show_stats(args):
    """统计概览"""
    registry = load_registry()
    taxonomy = registry.get("taxonomy", {})
    categories = registry.get("categories", {})
    
    print(f"\n{'='*70}")
    print(f"📊 龍魂系统·语义统一注册表 v2.0 统计")
    print(f"{'='*70}")
    print(f"  DNA: {registry['meta']['dna']}")
    print(f"  更新: {registry['meta'].get('updated', registry['meta']['created'])}")
    print()
    
    total_entries = 0
    for cat_key in taxonomy:
        emoji = CATEGORY_COLORS.get(cat_key, "📌")
        cat_data = categories.get(cat_key, {})
        count = 0
        
        for sub_type, sub_data in cat_data.items():
            if isinstance(sub_data, dict):
                count += len(sub_data)
            elif isinstance(sub_data, list):
                count += len(sub_data)
        
        total_entries += count
        print(f"  {emoji} {cat_key}: {count} 条目")
        print(f"     └─ {taxonomy[cat_key][:80]}")
    
    print(f"\n  {'─'*50}")
    print(f"  📦 总计: {len(taxonomy)} 分类 · {total_entries} 条目")
    print(f"  🔗 交叉引用: {len(registry.get('cross_references', {}))} 条")
    print(f"  📋 命名规范: 已定义")
    print()
    
    # 同步状态
    sync = registry.get("sync_status", {})
    print(f"  ⏳ 待导入: {', '.join(sync.get('pending_imports', []))}")
    print()


def audit_naming(args):
    """命名审计——检查命名一致性"""
    registry = load_registry()
    
    print(f"\n{'='*70}")
    print(f"⚖️ 命名审计 · 龍魂系统语义统一注册表")
    print(f"{'='*70}\n")
    
    issues = []
    
    # 检查 CodeBuddy 技能命名
    cb_skills = registry.get("categories", {}).get("SKILL", {}).get("longhun_skills_codebuddy", {})
    for sid, sinfo in cb_skills.items():
        if not sid.startswith("longhun-"):
            issues.append(f"  ⚠️ CodeBuddy技能 '{sid}' 缺少 longhun- 前缀")
    
    # 检查AI创作工具命名
    ai_tools = registry.get("categories", {}).get("AI_CREATION", {}).get("tools", {})
    for tid, tinfo in ai_tools.items():
        if not tinfo.get("unified_name", "").startswith("AI创作-"):
            issues.append(f"  ⚠️ AI创作工具 '{tid}' 的 unified_name 缺少 'AI创作-' 前缀")
    
    # 检查技能分散情况
    skill_locations = registry.get("categories", {}).get("SKILL", {}).get("skill_locations", {})
    locations_count = len(skill_locations)
    if locations_count > 2:
        issues.append(f"  ⚠️ 技能分布在 {locations_count} 个位置，建议收口到 2 个以内")
    
    if issues:
        print(f"  发现问题 {len(issues)} 个:\n")
        for issue in issues:
            print(issue)
    else:
        print("  ✅ 命名审计通过，无问题")
    
    print()


def show_ai_creation(args):
    """AI创作工具一览"""
    registry = load_registry()
    tools = registry.get("categories", {}).get("AI_CREATION", {}).get("tools", {})
    
    print(f"\n{'='*70}")
    print(f"🎨 AI创作工具集 · 统一索引")
    print(f"{'='*70}")
    print(f"  命名规范: AI创作-{{类型}}")
    print()
    
    for tid, tinfo in tools.items():
        print(f"  ┌─ {tinfo['unified_name']}")
        print(f"  │  原始名称: {tinfo['name']}")
        print(f"  │  类型: {tinfo.get('type', 'N/A')}")
        print(f"  │  能力: {', '.join(tinfo.get('capabilities', []))}")
        print(f"  │  路径: {tinfo.get('skill_path', tinfo.get('file', 'N/A'))}")
        trigger = tinfo.get('trigger_keywords', [])
        if trigger:
            print(f"  │  触发词: {', '.join(trigger[:5])}")
        print()
    
    dedup = registry.get("categories", {}).get("AI_CREATION", {}).get("dedup_note", "")
    if dedup:
        print(f"  💡 {dedup}")
    print()


def show_engines(args):
    """引擎一览"""
    registry = load_registry()
    engines = registry.get("categories", {}).get("ENGINE", {}).get("engines", {})
    
    print(f"\n{'='*70}")
    print(f"⚙️ 龍魂系统·引擎全景 ({len(engines)} 个)")
    print(f"{'='*70}\n")
    
    for eid, einfo in engines.items():
        name = einfo.get("name", eid)
        desc = einfo.get("desc", "")
        file = einfo.get("file", "N/A")
        version = einfo.get("version", "")
        skill = einfo.get("skill", "")
        
        ver_str = f" v{version}" if version else ""
        skill_str = f" [{skill}]" if skill else ""
        print(f"  • {name}{ver_str}{skill_str}")
        print(f"    {desc}")
        print(f"    📁 {file}")
        print()
    
    print(f"  共 {len(engines)} 个引擎")
    print(f"  详细用法: python3 bin/lh_semantic_unified_registry.py list ENGINE")
    print()


def show_skills(args):
    """技能全览"""
    registry = load_registry()
    skill_cat = registry.get("categories", {}).get("SKILL", {})
    
    print(f"\n{'='*70}")
    print(f"🛠️ 龍魂系统·技能全景")
    print(f"{'='*70}\n")
    
    # 技能分布
    locations = skill_cat.get("skill_locations", {})
    print(f"  📍 技能分布在 {len(locations)} 个位置:\n")
    for loc_key, loc_info in locations.items():
        print(f"    {loc_key}: {loc_info['path']} ({loc_info['count']} 个) — {loc_info['desc']}")
    
    # CodeBuddy 技能
    cb = skill_cat.get("longhun_skills_codebuddy", {})
    print(f"\n  ┌─ CodeBuddy 龍魂技能 ({len(cb)}):")
    for sid, sinfo in cb.items():
        print(f"  │  • {sid} → {sinfo['name_zh']} [{sinfo['category']}]")
    
    # 项目技能
    proj = skill_cat.get("longhun_skills_project", {})
    print(f"\n  ┌─ 项目技能目录 ({len(proj)}):")
    for sid, sinfo in proj.items():
        print(f"  │  • {sid} → {sinfo['name_zh']} [{sinfo['category']}]")
    
    # 技能庫文档
    docs = skill_cat.get("skill_library_docs", {})
    print(f"\n  ┌─ 技能庫文档 ({len(docs)}):")
    for sid, sinfo in docs.items():
        print(f"  │  • {sid} → {sinfo['name_zh']} [{sinfo['category']}]")
    
    print()


def show_papers(args):
    """论文一览"""
    registry = load_registry()
    bib = registry.get("categories", {}).get("BIBLIOGRAPHY", {})
    
    print(f"\n{'='*70}")
    print(f"📚 龍魂系统·论文与参考文献")
    print(f"{'='*70}\n")
    
    published = bib.get("published", [])
    print(f"  📄 已发表/撰写论文 ({len(published)} 篇):\n")
    for i, paper in enumerate(published, 1):
        keywords = ", ".join(paper.get("keywords", []))
        print(f"  {i}. {paper['title']}")
        print(f"     📁 {paper['path']}")
        if keywords:
            print(f"     🏷️ {keywords}")
        print()
    
    crypto_refs = bib.get("crypto_references", [])
    print(f"  🔐 密码学参考文献 ({len(crypto_refs)}):\n")
    for ref in crypto_refs:
        print(f"  • {ref['ref']}")
        print(f"    标准: {ref['std']} | {ref['desc']}")
    print()
    
    philo_refs = bib.get("philosophy_references", [])
    print(f"  🏛️ 哲学参考文献 ({len(philo_refs)}):\n")
    for ref in philo_refs:
        print(f"  • {ref['ref']} ({ref.get('era', ref.get('year', ''))})")
        key = ref.get("key_quote", ref.get("desc", ref.get("topic", "")))
        if key:
            print(f"    \"{key}\"")
    print()


def show_notion_pages(args):
    """Notion知识库页面一览"""
    registry = load_registry()
    notion_data = registry.get("categories", {}).get("NOTION", {})
    
    print(f"\n{'='*70}")
    print(f"📝 Notion知识库 · 龍魂系统外部知识底座")
    print(f"{'='*70}\n")
    
    infra = notion_data.get("infrastructure", {})
    print(f"  原则: {infra.get('principle', '')}")
    print(f"  同步桥文件: {infra.get('sync_bridges', 'N/A')} 个")
    print(f"  配置文件: {infra.get('sync_config', 'N/A')}")
    print()
    
    pages = notion_data.get("top_pages", [])
    print(f"  📄 核心页面 ({len(pages)}/{notion_data.get('total_pages_mapped', 51)} 已索引):\n")
    for i, page in enumerate(pages, 1):
        pid = page.get("id", "N/A")
        priority = page.get("priority", "?")
        print(f"  {i:2d}. [P{priority}] {page['name'][:80]}")
        print(f"       ID: {pid}")
    print()
    
    print(f"  ⏳ 待导入: {notion_data.get('pending_import', '')}")
    print()


def show_notion_prompt_library(args):
    """Notion 提示词库查询 — 挂接 notion_prompt_library/library_v2.json"""
    try:
        sys.path.insert(0, str(ROOT))
        from bin.lh_prompt_library import 提示词库
    except Exception as e:
        print(f"❌ 提示词库加载器不可用: {e}")
        return

    lib = 提示词库()
    stats = lib.统计()
    print(f"\n{'='*70}")
    print(f"📝 Notion 提示词库 v2.0 · 按助手分库 (精筛真模板)")
    print(f"{'='*70}\n")
    print(f"  来源页面: {stats['pages']} | 真模板总数: {stats['total']}")
    print(f"  按助手: {json.dumps(stats['assistants'], ensure_ascii=False)}\n")

    assistant = getattr(args, "assistant", None)
    keyword = getattr(args, "keyword", None)
    limit = getattr(args, "limit", 50) or 50

    if keyword:
        items = lib.搜索(keyword, assistant)
        print(f"  🔍 关键词「{keyword}」命中 {len(items)} 条 (上限 {limit}):\n")
    elif assistant:
        items = lib.按助手(assistant)
        print(f"  🤖 助手「{assistant}」共 {len(items)} 条 (上限 {limit}):\n")
    else:
        items = lib.条目
        print(f"  📚 全部模板 (上限 {limit}):\n")
    items = items[:limit]

    for i, p in enumerate(items, 1):
        print(f"  {i:3d}. [{p['assistant']}·{p['kind']}] {p['content'][:88]}")
    print()


def show_quantum(args):
    """量子体系引擎一览"""
    registry = load_registry()
    quantum = registry.get("categories", {}).get("QUANTUM", {})
    
    print(f"\n{'='*70}")
    print(f"⚛️ 龍魂系统·量子体系")
    print(f"{'='*70}\n")
    print(f"  {quantum.get('description', '')}\n")
    
    engines = quantum.get("engines", {})
    for eid, einfo in engines.items():
        print(f"  ┌─ {einfo['name']}")
        print(f"  │  📁 {einfo.get('file', 'N/A')}")
        print(f"  │  {einfo.get('desc', '')}")
        formula = einfo.get("formula", "")
        if formula:
            print(f"  │  📐 {formula}")
        thresholds = einfo.get("thresholds", {})
        if thresholds:
            for tk, tv in thresholds.items():
                print(f"  │  📏 {tk}: {tv}")
        print()
    
    print(f"  共 {len(engines)} 个量子体系引擎")
    print()


def export_registry(args):
    """导出注册表"""
    registry = load_registry()
    fmt = args.format or "json"
    output_path = args.output or str(ROOT / "state" / f"semantic_registry_export.{fmt}")
    
    if fmt == "json":
        with open(output_path, 'w') as f:
            json.dump(registry, f, ensure_ascii=False, indent=2)
    elif fmt == "markdown":
        # 导出为 Markdown
        lines = []
        lines.append(f"# 龍魂系统·语义统一注册表 v1.0")
        lines.append(f"> DNA: {registry['meta']['dna']}")
        lines.append(f"> 导出时间: {datetime.now().isoformat()}")
        lines.append("")
        
        for cat_key in registry.get("taxonomy", {}):
            cat_data = registry.get("categories", {}).get(cat_key, {})
            emoji = CATEGORY_COLORS.get(cat_key, "📌")
            lines.append(f"## {emoji} {cat_key} — {registry['taxonomy'][cat_key]}")
            lines.append("")
            lines.append(cat_data.get("description", ""))
            lines.append("")
            
            for sub_type, sub_data in cat_data.items():
                if isinstance(sub_data, dict) and sub_data:
                    lines.append(f"### {sub_type}")
                    for item_key, item_val in sub_data.items():
                        name = item_val.get("name", item_val.get("name_zh", item_key))
                        lines.append(f"- **{name}**: {item_val.get('desc', item_val.get('description', ''))}")
                    lines.append("")
        
        with open(output_path, 'w') as f:
            f.write("\n".join(lines))
    
    print(f"\n✅ 已导出到: {output_path}")
    print(f"   格式: {fmt}")


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description="龍魂系统·语义统一注册表查询引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s search 密码学          # 搜索密码学相关
  %(prog)s search 量子             # 搜索量子体系
  %(prog)s search 时空             # 搜索时空织网
  %(prog)s list CRYPTO            # 列出密码学分类
  %(prog)s list QUANTUM           # 列出量子体系分类
  %(prog)s list all               # 列出所有分类(18个)
  %(prog)s info seven_factor      # 查看七因子详情
  %(prog)s info digital_root      # 查看数字根详情
  %(prog)s xref 七因子            # 查看交叉引用
  %(prog)s stats                  # 统计概览
  %(prog)s audit                  # 命名审计
  %(prog)s ai-creation            # AI创作工具一览
  %(prog)s engines                # 引擎一览(26个)
  %(prog)s skills                 # 技能全览
  %(prog)s papers                 # 论文与参考文献
  %(prog)s notion-pages           # Notion知识库页面
  %(prog)s quantum                # 量子体系引擎
  %(prog)s export --format markdown  # 导出
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # search
    p_search = subparsers.add_parser("search", help="搜索关键词")
    p_search.add_argument("keyword", help="搜索关键词")
    
    # list
    p_list = subparsers.add_parser("list", help="列出分类")
    p_list.add_argument("category", help="分类代码 (CRYPTO/SEVEN_FACTOR/SEMANTIC/AI_CREATION/ENGINE/SKILL/PERSONA/ALGORITHM/QUANTUM/SPACETIME/GOVERNANCE/CNSH/CULTURE/INFRA/PROTOCOL/DOMAIN/NOTION/BIBLIOGRAPHY/all)")
    
    # info
    p_info = subparsers.add_parser("info", help="查看条目详情")
    p_info.add_argument("name", help="条目名称")
    
    # xref
    p_xref = subparsers.add_parser("xref", help="查看交叉引用")
    p_xref.add_argument("name", help="关键词")
    
    # stats
    subparsers.add_parser("stats", help="统计概览")
    
    # audit
    subparsers.add_parser("audit", help="命名审计")
    
    # ai-creation
    subparsers.add_parser("ai-creation", help="AI创作工具一览")
    
    # engines
    subparsers.add_parser("engines", help="引擎一览")
    
    # skills
    subparsers.add_parser("skills", help="技能全览")
    
    # export
    p_export = subparsers.add_parser("export", help="导出注册表")
    p_export.add_argument("--format", choices=["json", "markdown"], default="json")
    p_export.add_argument("--output", help="输出路径")
    
    # papers
    subparsers.add_parser("papers", help="论文与参考文献一览")
    
    # notion-pages
    subparsers.add_parser("notion-pages", help="Notion知识库页面一览")

    # notion-prompt-library (挂接 Notion 提示词库 v2.0)
    p_npl = subparsers.add_parser("notion-prompt-library", help="Notion提示词库查询(按助手分库)")
    p_npl.add_argument("--assistant", help="助手: 宝宝/通心译/Claude/通用 (或别名)")
    p_npl.add_argument("--keyword", help="关键词过滤")
    p_npl.add_argument("--limit", type=int, default=50, help="返回条数上限")

    # quantum
    subparsers.add_parser("quantum", help="量子体系引擎一览")

    args = parser.parse_args()

    if args.command == "search":
        search(args)
    elif args.command == "list":
        list_category(args)
    elif args.command == "info":
        show_info(args)
    elif args.command == "xref":
        show_xref(args)
    elif args.command == "stats":
        show_stats(args)
    elif args.command == "audit":
        audit_naming(args)
    elif args.command == "ai-creation":
        show_ai_creation(args)
    elif args.command == "engines":
        show_engines(args)
    elif args.command == "skills":
        show_skills(args)
    elif args.command == "export":
        export_registry(args)
    elif args.command == "papers":
        show_papers(args)
    elif args.command == "notion-pages":
        show_notion_pages(args)
    elif args.command == "notion-prompt-library":
        show_notion_prompt_library(args)
    elif args.command == "quantum":
        show_quantum(args)
    else:
        # 默认显示统计
        show_stats(argparse.Namespace())
        print("\n💡 用法: python3 bin/lh_semantic_unified_registry.py <命令>")
        print("   试试: search 密码学 | list all | stats | ai-creation | engines | skills | papers | quantum")


if __name__ == "__main__":
    main()
