#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰既济-MEMORY-AUTO-DEPOSIT-v2.2
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
"""
龍魂·记忆库自动沉淀 v2.2
─────────────────────────
v2.2新增: 七因子行为DNA自动检测·行为模式判定·行为DNA标签入库
v1.0: 从每日对话记忆中自动提取规矩/决策/架构/底线

用法:
  python3 bin/lh_memory_auto_deposit.py                      # 扫描今天日志
  python3 bin/lh_memory_auto_deposit.py --all                 # 扫描所有日志
  python3 bin/lh_memory_auto_deposit.py --since "2026-07-20"  # 指定日期
  python3 bin/lh_memory_auto_deposit.py --dry-run             # 预览模式
  python3 bin/lh_memory_auto_deposit.py --behavior-only       # 只检测七因子
"""

import os, sys, json, sqlite3, re
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import List, Tuple, Optional, Dict
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MEMORY_DIR = PROJECT_ROOT / ".codebuddy" / "memory"
MEMORY_DB = PROJECT_ROOT / "brain" / "memories.db"
CST = __import__('datetime').timezone(timedelta(hours=8))

# ━━ 提取规则（v1.0 保留）━━━
EXTRACT_RULES = [
    ('铁律', re.compile(r'(铁律|焊死|不可[逆改删变破]|必须|禁止|天条|红线|🔥)'), '金', 'P05上帝之眼', 8),
    ('决策', re.compile(r'(决定|拍板|确认|老大说|指令|训示|就这样|定了)'), '火', 'P01诸葛亮', 7),
    ('架构', re.compile(r'(架构|新增|创建|落位|部署|引擎|脚本)'), '土', 'P04鲁班', 6),
    ('规矩', re.compile(r'(规则|规范|标准|流程|三步走|自动化)'), '水', 'P13姜子牙', 6),
    ('底线', re.compile(r'(底线|原则|不可破|红线|碰不得|禁止场景|一票否决)'), '火', 'P12屈原', 9),
]

# ━━ v2.2: 七因子行为检测规则 ━━
# (因子代码, 正则, 正面/负面, 权重)
BEHAVIOR_RULES = [
    # P-承诺: 承诺产生
    ('P', re.compile(r'(承诺|答应|保证|一定|肯定会|会做到的|说到做到|今晚|明天|这周|以后)'), '有承诺', None, 0.9),
    # F-兑现: 执行结果
    ('F', re.compile(r'(搞定了|完成了|做好了|兑现了|做到了|已交付|已部署)'), '已兑现', None, 0.95),
    ('F', re.compile(r'(没做|忘了|没完成|没兑现|没搞定|食言|放鸽子)'), '未兑现', None, 0.9),
    ('F', re.compile(r'(做了一半|部分完成|差一点|还差)'), '部分兑现', None, 0.85),
    # E-情绪: 执行情绪
    ('E', re.compile(r'(心甘情愿|主动|乐意|开心地|愿意|发自内心)'), '心甘情愿', None, 0.9),
    ('E', re.compile(r'(敷衍|应付|随便|算了|就这样吧|随便吧|无所谓)'), '敷衍', None, 0.85),
    ('E', re.compile(r'(甩脸|不爽|不情愿|被迫|硬着头皮|烦躁)'), '甩脸', None, 0.9),
    ('E', re.compile(r'(麻木|没感觉|无所谓了|心死|随便了)'), '麻木', None, 0.85),
    # A-受众: 受众指向
    ('A', re.compile(r'(为自己|为了自己)'), '为自己', None, 0.8),
    ('A', re.compile(r'(为(了)?老婆|为(了)?媳妇|为(了)?伴侣|为(了)?男朋友|为(了)?女朋友|为(了)?爱人|为(了)?老大)'), '为伴侣', None, 0.9),
    ('A', re.compile(r'(为(了)?家人|为(了)?爸妈|为(了)?孩子|为(了)?父母|为(了)?家庭)'), '为家人', None, 0.9),
    ('A', re.compile(r'(为(了)?外人|为(了)?同事|为(了)?朋友|帮别人)'), '为外人', None, 0.85),
    ('A', re.compile(r'(为(了)?公众|为(了)?大家|为(了)?社会|为(了)?社区)'), '为公众', None, 0.85),
    # X-解释倾向: 失信后的反应
    ('X', re.compile(r'(因为|原因是|解释一下|听我说|那个|主要是|其实是|不是我不想)'), '爱解释', None, 0.85),
    ('X', re.compile(r'(不解释|没啥好说的|就这样|不说了|算了)'), '不解释', None, 0.85),
    ('X', re.compile(r'(我错了|我的问题|真认|承认|确实是我)'), '真认', None, 0.9),
    # Y-认错模式: 认错后的行为
    ('Y', re.compile(r'(真改|会改|马上改|这就改|下次不会|我改)'), '真改', None, 0.85),
    ('Y', re.compile(r'(硬扛|我没错|凭什么|又不是我|关我什么事)'), '硬扛', None, 0.9),
    ('Y', re.compile(r'(无所谓|随便|爱怎样怎样|就这样)'), '无所谓', None, 0.85),
    ('Y', re.compile(r'(不回应|沉默|不理|无视|假装没看见)'), '无反应', None, 0.85),
]

# ━━ v2.2: 行为模式判定 ━━
def 判定行为模式(七因子标签: Dict[str, str]) -> str:
    """根据七因子标签自动判定行为模式"""
    f_val = 七因子标签.get('F', '')
    x_val = 七因子标签.get('X', '')
    y_val = 七因子标签.get('Y', '')
    z_val = 七因子标签.get('Z', '')
    
    if f_val == '未兑现' and x_val == '爱解释':
        return 'MODE-防御型失信'
    elif f_val == '已兑现' and 七因子标签.get('A', '') == '为外人':
        return 'MODE-外耗型守信'
    elif f_val == '未兑现' and y_val == '无所谓':
        return 'MODE-内耗型自毁'
    elif z_val and float(z_val) > 2:
        return 'MODE-波动型摇摆'
    else:
        return 'MODE-稳定型自律'

# ━━ v2.2: 从文本提取七因子标签 ━━
def 提取七因子(text: str) -> Dict[str, str]:
    """
    从文本中检测七因子行为模式。
    返回: {因子代码: 检测值}
    """
    factors: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
    
    for factor_code, regex, value, _, weight in BEHAVIOR_RULES:
        if regex.search(text):
            factors[factor_code].append((value, weight))
    
    # 每个因子取最高权重
    result = {}
    for code, candidates in factors.items():
        # 取权重最高的
        candidates.sort(key=lambda x: x[1], reverse=True)
        result[code] = candidates[0][0]
    
    return result

def 生成行为标签(七因子: Dict[str, str]) -> str:
    """生成行为DNA标签字符串"""
    tags = []
    for code in ['P', 'F', 'T', 'E', 'C', 'R', 'A', 'X', 'Y', 'Z']:
        if code in 七因子:
            tags.append(f"7F-{code}-{七因子[code]}")
    return ' '.join(tags)


# ━━ 去重 ━━
def load_existing_contents() -> set:
    if not MEMORY_DB.exists():
        return set()
    conn = sqlite3.connect(str(MEMORY_DB))
    rows = conn.execute("SELECT content FROM memories").fetchall()
    conn.close()
    return {r[0][:80] for r in rows}


# ━━ 日志解析（v1.0 + v2.2增强）━━━
def parse_daily_log(filepath: Path, behavior_only: bool = False) -> List[dict]:
    """解析每日日志，提取关键条目 + 七因子行为DNA"""
    if not filepath.exists():
        return []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return []

    entries = []
    lines = content.split('\n')
    
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filepath.name)
    log_date = date_match.group(1) if date_match else 'unknown'

    # ━━ v2.2: 全文七因子扫描 ━━
    # 按段落扫描，检测行为模式
    paragraphs = content.split('\n\n')
    for para in paragraphs:
        para = para.strip()
        if len(para) < 10:
            continue
        
        七因子 = 提取七因子(para)
        if len(七因子) >= 2:  # 至少检测到2个因子才记录
            模式 = 判定行为模式(七因子)
            标签串 = 生成行为标签(七因子)
            
            entries.append({
                'content': f"{标签串} {模式} | {para[:150]}",
                'wuxing': '水',
                'persona': 'P05上帝之眼',
                'dr': 9 if '失信' in 模式 or '未兑现' in str(七因子.get('F', '')) else 6,
                'source': f"{filepath.name}",
                'date': log_date,
                'category': '行为DNA',
                'context': para[:300],
                '_behavior_tags': 标签串,
                '_behavior_mode': 模式,
                '_seven_factors': 七因子,
            })

    # 如果只要行为检测，跳过标准提取
    if behavior_only:
        return entries

    # ━━ v1.0: 标准提取 ━━
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line or set(line).issubset({'─', '═', '━', '—', '-', '#'}):
            i += 1
            continue
        
        if line.startswith('## ') or line.startswith('---'):
            i += 1
            continue

        # 🔥 标记行
        if '🔥' in line and len(line) > 5:
            context_start = max(0, i - 2)
            context_end = min(len(lines), i + 3)
            context = ' '.join(l.strip() for l in lines[context_start:context_end]
                              if not l.strip().startswith('#'))
            
            for cat, regex, wuxing, persona, dr in EXTRACT_RULES:
                if regex.search(line):
                    entries.append({
                        'content': line[:200],
                        'wuxing': wuxing,
                        'persona': persona,
                        'dr': dr if '🔥' not in line else 9,
                        'source': f"{filepath.name}",
                        'date': log_date,
                        'category': cat,
                        'context': context[:300],
                    })
                    break
            else:
                entries.append({
                    'content': line[:200],
                    'wuxing': '金',
                    'persona': 'P00文心',
                    'dr': 7,
                    'source': f"{filepath.name}",
                    'date': log_date,
                    'category': '标记',
                    'context': '',
                })

        # 标准规则匹配
        for cat, regex, wuxing, persona, dr in EXTRACT_RULES:
            if regex.search(line) and len(line) > 10:
                already_matched = any(e['content'] == line[:200] for e in entries)
                if not already_matched:
                    entries.append({
                        'content': line[:200],
                        'wuxing': wuxing,
                        'persona': persona,
                        'dr': dr,
                        'source': f"{filepath.name}",
                        'date': log_date,
                        'category': cat,
                        'context': '',
                    })
                break

        i += 1

    return entries


def generate_dna(content, category, date_str):
    today = date_str.replace('-', '') if date_str != 'unknown' else datetime.now(CST).strftime('%Y%m%d')
    hash_val = abs(hash(content)) % 0xFFFFFF
    return f"#龍芯⚡{date_str}-AUTO-{category.upper()}-{hash_val:06x}"


def deposit_entries(entries: List[dict], dry_run=False) -> int:
    if not entries:
        return 0

    existing = load_existing_contents()
    deposited = 0

    conn = sqlite3.connect(str(MEMORY_DB))
    
    for e in entries:
        if e['content'][:80] in existing:
            continue
        
        dna = generate_dna(e['content'], e['category'], e['date'])
        
        # v2.2: 行为标签附加入库
        tags_list = [e['category'], 'auto']
        if e.get('_behavior_tags'):
            tags_list.extend(e['_behavior_tags'].split())
        if e.get('_behavior_mode'):
            tags_list.append(e['_behavior_mode'])
        tags = json.dumps(tags_list, ensure_ascii=False)

        if not dry_run:
            conn.execute("""INSERT INTO memories (dna, content, wuxing, persona, dr, tricolor, tags, source)
                          VALUES (?, ?, ?, ?, ?, '🟢', ?, ?)""",
                         (dna, e['content'], e['wuxing'], e['persona'], e['dr'], tags, e['source']))
        deposited += 1
        existing.add(e['content'][:80])

    if not dry_run:
        conn.commit()
    conn.close()
    return deposited


def get_log_files(since_date=None) -> List[Path]:
    if not MEMORY_DIR.exists():
        return []
    
    files = sorted(MEMORY_DIR.glob("20*.md"))
    
    if since_date:
        if isinstance(since_date, str):
            since_date = date.fromisoformat(since_date)
        files = [f for f in files if date_match(f) and date_match(f) >= since_date]
    
    return files


def date_match(filepath: Path) -> Optional[date]:
    m = re.search(r'(\d{4}-\d{2}-\d{2})', filepath.name)
    if m:
        return date.fromisoformat(m.group(1))
    return None


def main():
    dry_run = '--dry-run' in sys.argv
    scan_all = '--all' in sys.argv
    behavior_only = '--behavior-only' in sys.argv
    since_date = None

    for i, arg in enumerate(sys.argv):
        if arg == '--since' and i + 1 < len(sys.argv):
            since_date = sys.argv[i + 1]

    if scan_all:
        files = get_log_files()
    elif since_date:
        files = get_log_files(since_date)
    else:
        today = datetime.now(CST).date()
        files = []
        for d in [today, today - timedelta(days=1)]:
            f = MEMORY_DIR / f"{d.isoformat()}.md"
            if f.exists():
                files.append(f)

    if not files:
        print("🟡 无日志文件")
        return

    total_deposited = 0
    total_behavior = 0
    
    for f in files:
        entries = parse_daily_log(f, behavior_only=behavior_only)
        if not entries:
            continue
        
        behavior_count = sum(1 for e in entries if e['category'] == '行为DNA')
        total_behavior += behavior_count
        
        n = deposit_entries(entries, dry_run=dry_run)
        mode = "[DRY-RUN] 将" if dry_run else "✅"
        
        detail = f"标准{len(entries)-behavior_count} + 行为DNA{behavior_count}" if behavior_count else f"标准{len(entries)}"
        print(f"  {mode} {f.name}: 提取 {len(entries)} 条 ({detail}) → 入库 {n} 条")
        total_deposited += n

    mode = "[DRY-RUN] 预览完成，" if dry_run else "✅ 沉淀完成，"
    behavior_info = f"含 {total_behavior} 条行为DNA" if total_behavior > 0 else ""
    print(f"\n{mode}共 {total_deposited} 条新记忆 {behavior_info}")
    
    # v2.2: 输出行为DNA汇总
    if total_behavior > 0 and not dry_run:
        print("\n── 🧬 行为DNA检测汇总 ──")
        behaviors = defaultdict(int)
        for f in files:
            entries = parse_daily_log(f, behavior_only=True)
            for e in entries:
                if e.get('_behavior_mode'):
                    behaviors[e['_behavior_mode']] += 1
        for mode, count in sorted(behaviors.items(), key=lambda x: x[1], reverse=True):
            print(f"  {mode}: {count} 次")


if __name__ == '__main__':
    main()
