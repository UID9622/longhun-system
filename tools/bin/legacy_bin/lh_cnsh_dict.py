#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
CNSH标准词典 · 查询工具
DNA: #龍芯⚡️丙午·乙未·乙未·酉时·☷坤-CNSH-DICT-QUERY-v1.0

用法:
  python3 bin/lh_cnsh_dict.py search <关键词>          # 模糊搜索
  python3 bin/lh_cnsh_dict.py lookup <英文词>          # 精确查找英文
  python3 bin/lh_cnsh_dict.py cnsh <CNSH词>           # 按CNSH名查
  python3 bin/lh_cnsh_dict.py list <分类>              # 列出某分类
  python3 bin/lh_cnsh_dict.py categories               # 列出所有分类
  python3 bin/lh_cnsh_dict.py stats                    # 统计信息
  python3 bin/lh_cnsh_dict.py export-csv               # 导出CSV
"""
import json
import sys
from pathlib import Path

DICT_PATH = Path(__file__).parent.parent / "03_知識圖譜" / "cnsh_standard_dictionary.json"

def load_dict():
    with open(DICT_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def fmt_entry(e, cat_name, show_related=True):
    """格式化一条词典条目"""
    lines = []
    lines.append(f"┌─ {e['id']} ─────────────────────────────")
    lines.append(f"│ 分类: {cat_name}")
    lines.append(f"│ 英文: {e['en']}")
    lines.append(f"│ 直译: {e['cn_direct']}")
    lines.append(f"│ CNSH: {e['cnsh']}")
    lines.append(f"│ 解释: {e['explanation']}")
    if e.get('cultural_origin'):
        lines.append(f"│ 出处: {e['cultural_origin']}")
    if e.get('scene'):
        lines.append(f"│ 场景: {e['scene']}")
    if e.get('cnsh_usage'):
        lines.append(f"│ 用法: {e['cnsh_usage']}")
    if show_related and e.get('related'):
        lines.append(f"│ 关联: {', '.join(e['related'])}")
    lines.append(f"└{'─' * 45}")
    return '\n'.join(lines)

def search(data, keyword):
    """模糊搜索"""
    keyword_lower = keyword.lower()
    entries = data['entries']
    cat_map = {c['code']: c['name'] for c in data['meta']['taxonomy']}
    
    results = []
    for e in entries:
        score = 0
        if keyword_lower in e['en'].lower():
            score += 10
        if keyword_lower in e['cn_direct'].lower():
            score += 8
        if keyword_lower in e['cnsh'].lower():
            score += 9
        if keyword_lower in e.get('explanation', '').lower():
            score += 3
        if keyword_lower in e.get('scene', '').lower():
            score += 2
        if score > 0:
            results.append((score, e))
    
    results.sort(key=lambda x: x[0], reverse=True)
    
    if not results:
        print(f"❌ 未找到 '{keyword}' 相关条目")
        return
    
    print(f"🔍 '{keyword}' 找到 {len(results)} 条:\n")
    for score, e in results[:20]:
        print(fmt_entry(e, cat_map.get(e['category'], e['category']), show_related=False))
        print()
    
    if len(results) > 20:
        print(f"... 还有 {len(results) - 20} 条，请缩小搜索范围")

def lookup_en(data, en_word):
    """精确查找英文"""
    entries = data['entries']
    cat_map = {c['code']: c['name'] for c in data['meta']['taxonomy']}
    
    for e in entries:
        if e['en'].lower() == en_word.lower():
            print(fmt_entry(e, cat_map.get(e['category'], e['category'])))
            return
    
    # 模糊匹配
    matches = [e for e in entries if en_word.lower() in e['en'].lower()]
    if matches:
        print(f"⚠️ 未精确匹配 '{en_word}'，模糊匹配 {len(matches)} 条:\n")
        for e in matches[:10]:
            print(fmt_entry(e, cat_map.get(e['category'], e['category']), show_related=False))
            print()
    else:
        print(f"❌ 未找到 '{en_word}'")

def lookup_cnsh(data, cnsh_word):
    """按CNSH名查"""
    entries = data['entries']
    cat_map = {c['code']: c['name'] for c in data['meta']['taxonomy']}
    
    matches = [e for e in entries if cnsh_word in e['cnsh']]
    if matches:
        print(f"🔍 CNSH '{cnsh_word}' 找到 {len(matches)} 条:\n")
        for e in matches:
            print(fmt_entry(e, cat_map.get(e['category'], e['category']), show_related=False))
            print()
    else:
        print(f"❌ CNSH词 '{cnsh_word}' 未找到")

def list_category(data, cat_name):
    """列出某分类"""
    entries = data['entries']
    cat_map = {c['code']: c['name'] for c in data['meta']['taxonomy']}
    rev_cat = {v: k for k, v in cat_map.items()}
    
    # 找分类
    cat_code = None
    for code, name in cat_map.items():
        if cat_name in name or cat_name.lower() in code.lower():
            cat_code = code
            break
    
    if not cat_code:
        print(f"❌ 未找到分类 '{cat_name}'")
        print(f"可用分类: {', '.join(cat_map.values())}")
        return
    
    matches = [e for e in entries if e['category'] == cat_code]
    print(f"📂 {cat_map[cat_code]} ({len(matches)} 条):\n")
    
    for e in matches:
        print(f"  {e['en']:25s} → {e['cnsh']:10s}  {e['explanation'][:50]}")
    
    print(f"\n  📊 共 {len(matches)} 条")

def list_categories(data):
    """列出所有分类"""
    cat_map = {c['code']: c['name'] for c in data['meta']['taxonomy']}
    entries = data['entries']
    from collections import Counter
    counts = Counter(e['category'] for e in entries)
    
    print("CNSH标准词典 · 十领域分类:\n")
    for code, name in cat_map.items():
        count = counts.get(code, 0)
        bar = '█' * (count // 2)
        print(f"  {code:8s} {name:25s} {count:3d} 条  {bar}")

def show_stats(data):
    """统计信息"""
    meta = data['meta']
    entries = data['entries']
    cat_map = {c['code']: c['name'] for c in meta['taxonomy']}
    from collections import Counter
    counts = Counter(e['category'] for e in entries)
    
    print(f"╔══════════════════════════════════════════╗")
    print(f"║  CNSH标准词典 · 统计                    ║")
    print(f"╠══════════════════════════════════════════╣")
    print(f"║  版本: {meta['version']}")
    print(f"║  总条目: {len(entries)}")
    print(f"║  分类数: {len(meta['taxonomy'])}")
    print(f"║  语法示例: {len(meta.get('grammar_examples', {}))}")
    print(f"║  CNSH动作前缀: {len(meta.get('action_prefixes', {}))}")
    print(f"║  CNSH层级后缀: {len(meta.get('suffix_rules', {}))}")
    print(f"╠══════════════════════════════════════════╣")
    print(f"║  分类明细:                               ║")
    for code, name in cat_map.items():
        print(f"║    {name:28s} {counts.get(code, 0):3d} 条")
    print(f"╚══════════════════════════════════════════╝")

def show_principles(data):
    """显示命名原则"""
    print("CNSH命名原则:\n")
    for p in data['meta']['principles']:
        print(f"  ▸ {p}")
    
    print(f"\n动作前缀:")
    for k, v in data['meta']['action_prefixes'].items():
        print(f"  {k}: {v}")
    
    print(f"\n层级后缀:")
    for k, v in data['meta']['suffix_rules'].items():
        print(f"  {k}: {v}")

def show_examples(data):
    """显示语法示例"""
    examples = data.get('grammar_examples', {})
    if not examples:
        print("（语法示例在词典JSON中）\n")
        return
    print("CNSH语法示例:\n")
    for name, example in examples.items():
        print(f"【{name}】")
        print(f"  Python:")
        for line in example['python'].split('\n'):
            print(f"    {line}")
        print(f"  CNSH:")
        for line in example['cnsh'].split('\n'):
            print(f"    {line}")
        print()

def show_help():
    print("""
CNSH标准词典 · 查询工具
用法:
  search <关键词>     模糊搜索（英文/中文/CNSH名）
  lookup <英文词>     精确查找英文术语
  cnsh <CNSH词>       按CNSH命名查找
  list <分类>         列出某分类全部条目
  categories          列出所有分类
  stats               统计信息
  principles          命名原则
  examples            语法示例
  help                本帮助
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    data = load_dict()
    cmd = sys.argv[1].lower()
    arg = sys.argv[2] if len(sys.argv) > 2 else ''
    
    if cmd == 'search':
        search(data, arg)
    elif cmd == 'lookup':
        lookup_en(data, arg)
    elif cmd == 'cnsh':
        lookup_cnsh(data, arg)
    elif cmd == 'list':
        list_category(data, arg)
    elif cmd == 'categories':
        list_categories(data)
    elif cmd == 'stats':
        show_stats(data)
    elif cmd == 'principles':
        show_principles(data)
    elif cmd == 'examples':
        show_examples(data)
    elif cmd == 'export-csv':
        import subprocess
        subprocess.run([sys.executable, str(Path(__file__).parent / 'lh_cnsh_dict_export.py')])
    elif cmd == 'help':
        show_help()
    else:
        print(f"未知命令: {cmd}")
        show_help()

if __name__ == '__main__':
    main()
