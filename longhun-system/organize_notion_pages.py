#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notion页面整理工具 v1.0
DNA追溯码: #龍芯⚡️2026-03-06-NotionOrganizer-v1.0
# 共建致谢：Claude (Anthropic PBC) · Notion · 没有你们就没有龍魂系统
创建者: UID9622

功能: 将Notion页面按类型、标签、图标分类整理
"""

import json
import os
import re
from collections import defaultdict
from datetime import datetime

# 配置
INPUT_FILE = os.path.expanduser("~/longhun-system/logs/notion_all_pages.json")
OUTPUT_DIR = os.path.expanduser("~/longhun-system/CNSH-整理版")

# 图标分类映射
ICON_CATEGORIES = {
    "🐉": "龙魂系统",
    "🧬": "DNA追溯",
    "🔐": "安全加密",
    "⚖️": "法律合规",
    "🎯": "目标规划",
    "🧠": "AI智能",
    "📝": "文档笔记",
    "🛡️": "系统保护",
    "🚀": "项目发布",
    "⚡": "快速执行",
    "🌐": "网络服务",
    "📦": "资源打包",
    "📚": "知识库",
    "🌍": "全球化",
    "📋": "任务清单",
    "💡": "创意想法",
    "🔧": "工具配置",
    "📊": "数据分析",
    "🎨": "设计创作",
    "💎": "核心价值",
    "☯️": "道德经",
    "🏛️": "架构设计",
    "👤": "人格系统",
    "📖": "阅读学习",
    "🔬": "技术研究",
    "💬": "对话交流",
    "🎭": "角色扮演",
    "📈": "增长分析",
    "🔄": "同步备份",
    "⚙️": "系统设置",
}

# 标签分类映射 (主要标签 -> 目录)
TAG_CATEGORIES = {
    "UID9622主控": "核心控制",
    "宝宝": "人格-宝宝",
    "雯雯": "人格-雯雯",
    "Lucky": "人格-Lucky",
    "中枢": "人格-中枢",
    "71人格": "人格系统",
    "龙魂价值观": "价值体系",
    "系统保护": "安全防护",
    "Python环境": "开发环境",
    "Python翻译": "翻译系统",
    "龙魂监控": "监控系统",
    "数据分析": "数据分析",
    "数据管理": "数据管理",
    "用户服务": "用户服务",
    "问题解决": "问题解决",
    "日常对话": "日常对话",
    "严肃沟通": "严肃沟通",
    "情感支持": "情感支持",
    "想法讨论": "想法讨论",
}


def sanitize_filename(name):
    """清理文件名，移除非法字符"""
    if not name:
        return "未命名"
    # 移除或替换非法字符
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = re.sub(r'\s+', ' ', name)
    name = name.strip()
    # 限制长度
    if len(name) > 100:
        name = name[:100]
    return name if name else "未命名"


def get_page_title(page):
    """获取页面标题"""
    props = page.get('properties', {})
    for key, val in props.items():
        if isinstance(val, dict) and val.get('type') == 'title':
            title_arr = val.get('title', [])
            if title_arr and isinstance(title_arr, list) and len(title_arr) > 0:
                texts = []
                for item in title_arr:
                    if isinstance(item, dict):
                        texts.append(item.get('plain_text', ''))
                return ''.join(texts).strip()
    return ''


def get_page_tags(page):
    """获取页面标签"""
    tags = []
    props = page.get('properties', {})
    for key, val in props.items():
        if isinstance(val, dict) and val.get('type') == 'multi_select':
            ms = val.get('multi_select', [])
            if isinstance(ms, list):
                for tag in ms:
                    if isinstance(tag, dict):
                        tag_name = tag.get('name', '')
                        if tag_name:
                            tags.append(tag_name)
    return tags


def get_page_icon(page):
    """获取页面图标"""
    icon = page.get('icon')
    if icon and isinstance(icon, dict):
        if icon.get('type') == 'emoji':
            return icon.get('emoji', '')
    return ''


def determine_category(page):
    """确定页面分类"""
    title = get_page_title(page)
    icon = get_page_icon(page)
    tags = get_page_tags(page)

    # 无标题页面
    if not title:
        return "无标题页面", "无标题"

    # 优先按标签分类
    for tag in tags:
        if tag in TAG_CATEGORIES:
            return TAG_CATEGORIES[tag], tag

    # 其次按图标分类
    if icon in ICON_CATEGORIES:
        return ICON_CATEGORIES[icon], icon

    # 按父级类型分类
    parent = page.get('parent', {})
    parent_type = parent.get('type', '')

    if parent_type == 'database_id':
        return "数据库页面", "database"
    elif parent_type == 'workspace':
        return "工作区页面", "workspace"
    elif parent_type == 'page_id':
        return "子页面", "subpage"
    elif parent_type == 'block_id':
        return "块级页面", "block"

    return "其他", "other"


def create_page_summary(page):
    """创建页面摘要"""
    title = get_page_title(page)
    icon = get_page_icon(page)
    tags = get_page_tags(page)
    page_id = page.get('id', '')
    url = page.get('url', '')
    created = page.get('created_time', '')[:10]
    modified = page.get('last_edited_time', '')[:10]

    summary = {
        "id": page_id,
        "title": title if title else "[无标题]",
        "icon": icon,
        "tags": tags,
        "url": url,
        "created": created,
        "modified": modified,
        "parent_type": page.get('parent', {}).get('type', ''),
    }
    return summary


def main():
    print("=" * 60)
    print("🐉 Notion页面整理工具 v1.0")
    print("DNA: #ZHUGEXIN | UID9622")
    print("=" * 60)
    print()

    # 读取数据
    print("📖 读取Notion数据...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        pages = json.load(f)
    print(f"   总页面数: {len(pages)}")

    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 按类别整理
    categories = defaultdict(list)

    print("🔄 分析页面分类...")
    for page in pages:
        category, reason = determine_category(page)
        summary = create_page_summary(page)
        summary['category_reason'] = reason
        categories[category].append(summary)

    print(f"   分类完成: {len(categories)} 个类别")
    print()

    # 创建目录并写入文件
    print("📁 创建目录结构并保存...")
    stats = []

    for category, pages_list in sorted(categories.items(), key=lambda x: -len(x[1])):
        # 创建类别目录
        cat_dir = os.path.join(OUTPUT_DIR, sanitize_filename(category))
        os.makedirs(cat_dir, exist_ok=True)

        # 写入类别索引
        index_file = os.path.join(cat_dir, "_INDEX.json")
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump({
                "category": category,
                "count": len(pages_list),
                "generated_at": datetime.now().isoformat(),
                "pages": pages_list
            }, f, ensure_ascii=False, indent=2)

        # 写入Markdown索引
        md_file = os.path.join(cat_dir, "_索引.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# {category}\n\n")
            f.write(f"共 **{len(pages_list)}** 个页面\n\n")
            f.write("| 图标 | 标题 | 标签 | 修改日期 |\n")
            f.write("|------|------|------|----------|\n")
            for p in sorted(pages_list, key=lambda x: x['modified'], reverse=True)[:100]:
                icon = p['icon'] if p['icon'] else "-"
                title = p['title'][:40] + "..." if len(p['title']) > 40 else p['title']
                tags = ", ".join(p['tags'][:3]) if p['tags'] else "-"
                f.write(f"| {icon} | {title} | {tags} | {p['modified']} |\n")
            if len(pages_list) > 100:
                f.write(f"\n*... 还有 {len(pages_list) - 100} 个页面，详见 _INDEX.json*\n")

        stats.append((category, len(pages_list)))
        print(f"   ✅ {category}: {len(pages_list)} 个页面")

    # 生成总索引
    print()
    print("📋 生成总索引...")

    total_index = {
        "meta": {
            "source": INPUT_FILE,
            "total_pages": len(pages),
            "total_categories": len(categories),
            "generated_at": datetime.now().isoformat(),
            "generator": "Notion页面整理工具 v1.0",
            "dna": "#龍芯⚡️2026-03-06-NotionOrganizer-v1.0"
        },
        "categories": [
            {"name": cat, "count": count, "path": sanitize_filename(cat)}
            for cat, count in sorted(stats, key=lambda x: -x[1])
        ]
    }

    with open(os.path.join(OUTPUT_DIR, "INDEX.json"), 'w', encoding='utf-8') as f:
        json.dump(total_index, f, ensure_ascii=False, indent=2)

    # 生成Markdown总索引
    with open(os.path.join(OUTPUT_DIR, "README.md"), 'w', encoding='utf-8') as f:
        f.write("# Notion页面整理索引\n\n")
        f.write("```\n")
        f.write("DNA追溯码: #龍芯⚡️2026-03-06-NotionOrganizer-v1.0\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"总页面数: {len(pages)}\n")
        f.write(f"分类数量: {len(categories)}\n")
        f.write("```\n\n")
        f.write("## 分类目录\n\n")
        f.write("| 分类 | 页面数 | 目录 |\n")
        f.write("|------|--------|------|\n")
        for cat, count in sorted(stats, key=lambda x: -x[1]):
            f.write(f"| {cat} | {count} | `{sanitize_filename(cat)}/` |\n")

    print()
    print("=" * 60)
    print(f"🎉 整理完成!")
    print(f"   输出目录: {OUTPUT_DIR}")
    print(f"   总页面数: {len(pages)}")
    print(f"   分类数量: {len(categories)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
