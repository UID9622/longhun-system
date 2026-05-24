#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析 Notion 知识库导出文件，提取知识点信息
"""
import re
import json
import sys

FILE_PATH = '/var/folders/t7/xnm3vs951n9bj0g4dpksnznm0000gn/T/claude-hostloop-plugins/a287a83475e9e3a0/projects/-Users-zuimeidedeyihan-Library-Application-Support-Claude-local-agent-mode-sessions-a89d76ba-6216-42b3-ba33-e18194ebb230-b84aa772-13a2-4c76-ae42-f31f0ff2ce57-local-2b214d4a-f8ce-4287-8945-c7c87b685145-obmghn/da1e9532-8cbf-4798-be0c-3b8f4c5234c7/tool-results/mcp-00859313-fdd8-429a-8b00-23d2e76758e4-notion-query-database-view-1776857824919.txt'

OUTPUT_PATH = '/Users/zuimeidedeyihan/Library/Application Support/Claude/local-agent-mode-sessions/a89d76ba-6216-42b3-ba33-e18194ebb230/b84aa772-13a2-4c76-ae42-f31f0ff2ce57/local_2b214d4a-f8ce-4287-8945-c7c87b685145/outputs/notion_result.txt'

content = open(FILE_PATH, 'r', encoding='utf-8').read()
print(f"文件总长度: {len(content)} 字符")

# 提取所有知识点条目
# Notion MCP 格式：每个 page 用 <page url="..."> 包裹，属性在 <properties> JSON 中
pages = re.findall(r'<page url="([^"]+)">(.*?)</page>', content, re.DOTALL)
print(f"找到 page 数量: {len(pages)}")

# 提取 properties
entries = []
for url, page_content in pages:
    props_match = re.search(r'<properties>\s*(\{.*?\})\s*</properties>', page_content, re.DOTALL)
    if props_match:
        try:
            props = json.loads(props_match.group(1))
            entry = {
                'url': url,
                '知识点名称': props.get('知识点名称', ''),
                '分类': props.get('分类', ''),
                '子分类': props.get('子分类', ''),
                '是否核心': props.get('是否核心', ''),
                '学习状态': props.get('学习状态', ''),
                '是否进入系统': props.get('是否进入系统', ''),
                '学习优先级': props.get('学习优先级', ''),
                '难度等级': props.get('难度等级', ''),
            }
            entries.append(entry)
        except Exception as e:
            print(f"解析失败 {url}: {e}")

print(f"成功解析条目数: {len(entries)}")

# 按分类分组
from collections import defaultdict
by_cat = defaultdict(list)
for e in entries:
    cat = e.get('分类') or '未分类'
    by_cat[cat].append(e)

# 统计
total_dizuo = sum(1 for e in entries if '底座' in str(e.get('是否核心', '')))
total_yijie = sum(1 for e in entries if '已接入' in str(e.get('是否进入系统', '')))
total_weijie = sum(1 for e in entries if '未接入' in str(e.get('是否进入系统', '')))

# 输出结果
result_lines = []
result_lines.append(f"=== 计算机科学知识库 · 知识点完整列表 ===")
result_lines.append(f"总条目: {len(entries)} | 底座必须: {total_dizuo} | 已接入: {total_yijie} | 未接入: {total_weijie}")
result_lines.append("")

for cat, items in sorted(by_cat.items()):
    result_lines.append(f"## 【{cat}】（共{len(items)}条）")
    for e in items:
        name = e.get('知识点名称') or '（无名称）'
        he_xin = e.get('是否核心') or ''
        zhuangtai = e.get('学习状态') or ''
        jieruzhuangtai = e.get('是否进入系统') or ''
        sub = e.get('子分类') or ''
        markers = []
        if '底座' in he_xin:
            markers.append('🔴底座')
        if '已接入' in jieruzhuangtai:
            markers.append('✅已接入')
        elif '未接入' in jieruzhuangtai:
            markers.append('❌未接入')
        elif '接入中' in jieruzhuangtai:
            markers.append('🔧接入中')
        marker_str = ' '.join(markers) if markers else ''
        result_lines.append(f"  - {name} | {sub} | {he_xin} | {zhuangtai} | {jieruzhuangtai} {marker_str}")
    result_lines.append("")

result_lines.append(f"--- 统计 ---")
result_lines.append(f"底座（必须）共 {total_dizuo} 条")
result_lines.append(f"已接入共 {total_yijie} 条")
result_lines.append(f"未接入共 {total_weijie} 条")

result_text = '\n'.join(result_lines)
print(result_text)

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(result_text)
print(f"\n结果已保存到: {OUTPUT_PATH}")
