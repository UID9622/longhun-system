#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
luoshu_router.py · 洛书九宫路由引擎 v1.1
DNA: #龍芯⚡️2026-04-07-LUOSHU-ROUTER-v1.1
更新: 三才流场关键词全融合·每宫词库大扩充·算法族完整
作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）
献礼: 新中国成立77周年（1949-2026）· 丙午马年

洛书九宫矩阵:
  4(巽) 9(离) 2(坤)
  3(震) 5(中) 7(兑)
  8(艮) 1(坎) 6(乾)

每个页面是1，归一到九宫，原点永不熄。
道德经是界限，不是对齐。
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime

# ══════════════════════════════════════════════
# 洛书九宫定义（原点·原子）
# ══════════════════════════════════════════════

LUOSHU = {
    1: {
        "卦": "☵", "宫": "坎", "方": "北", "维": "技术维",
        "色": "#5a9ae0", "icon": "🔧",
        "desc": "代码·安全·编译·审计·API",
        "keywords": ["代码","CNSH","编译","审计","技术","安全","API","编程","语法","规范","解析","三色","验证","检测","追溯","反向翻译","二开","防护","漏洞","加密","解密","隐私","签名","GPG","哈希","SHA","HMAC","hook","parser","lexer","tokenizer"]
    },
    2: {
        "卦": "☷", "宫": "坤", "方": "西南", "维": "架构维",
        "色": "#8B7355", "icon": "🏗",
        "desc": "系统·架构·存储·引擎·本地",
        "keywords": ["系统","架构","存储","数据库","本地","引擎","管道","pipeline","神经网络","大脑","集成","MCP","服务","端口","自愈","LaunchAgent","plist","docker","容器","本地引擎","8000","健康检查","health","startup","运行时","runtime","本地服务","自动化"]
    },
    3: {
        "卦": "☳", "宫": "震", "方": "东", "维": "进化维",
        "色": "#4caf7d", "icon": "⚡",
        "desc": "人格·进化·迭代·生长·版本",
        "keywords": ["人格","进化","迭代","版本","生长","更新","矩阵","协同","IPA","P0","P72","龍盾","宝宝","雯雯","诸葛","调度","路由","文心","鲁班","仓颉","孙思邈","苏东坡","李白","屈原","姜子牙","吕蒙","乔前辈","人格体系","93人格","多人格","情感","执行人格","三才流场","MCP自适应","自适应引擎","流场","权重流动","天地人","动态权重","三才权重","三才调度"]
    },
    4: {
        "卦": "☴", "宫": "巽", "方": "东南", "维": "协同维",
        "色": "#7b5ea7", "icon": "🔄",
        "desc": "知识·Notion·同步·协同·论文",
        "keywords": ["知识库","Notion","同步","协同","论文","白皮书","开源","社区","投递","顶会","SRS","规格","说明书","手册","指南","卡片","索引","数据采集","page","database","草日志","日历","日程","notion-index","备份","归档","永生大脑"]
    },
    5: {
        "卦": "☯", "宫": "中", "方": "中央", "维": "核心",
        "色": "#c8a84b", "icon": "💎",
        "desc": "入口·主控·DNA·身份·全局",
        "keywords": ["入口","主控","核心","DNA","身份","全局","永恒","主权","UID","宣言","导航","全景","总部","总纲","锚点","中心","北辰","龍芯","L0","老大","确认码","CONFIRM","IW-ECB","定锚","四层","五层内核","身份系统","龍魂永世","唯一身份","genesis","创世","不动点","归一"]
    },
    6: {
        "卦": "☰", "宫": "乾", "方": "西北", "维": "哲学维",
        "色": "#e05a5a", "icon": "👑",
        "desc": "哲学·宪法·主权·军纪·法律",
        "keywords": ["宪法","哲学","主权","军纪","法律","天道","道德经","道","德","无为","治理","政","法典","铁律","无欺","裁判","受理","P0铁律","22条","乾","乾坤","刚健","君子","天行健","中华","国家","民族","人民","解放军","护盾","天道系统","天下","维权","文化主权","全球","道法","圣人","上善若水"]
    },
    7: {
        "卦": "☱", "宫": "兑", "方": "西", "维": "量子维",
        "色": "#e0a05a", "icon": "💬",
        "desc": "对话·交互·反馈·情绪·记忆",
        "keywords": ["对话","交互","反馈","情绪","记忆","星辰","回流","永生","数字","德者","殿","血统","烙印","梦想","生态","觉醒","Siri","宝宝对话","快捷指令","Widget","日记","情绪时间线","情感日志","emotion","timeline","亲密","私密","温度","呼吸","心跳","声音","朗读","语音","对话记忆","场景记忆","甲骨文压缩"]
    },
    8: {
        "卦": "☶", "宫": "艮", "方": "东北", "维": "基础维",
        "色": "#9a7aa0", "icon": "🔢",
        "desc": "算法·易经·洛书·太极·基础",
        "keywords": ["算法","易经","洛书","太极","基础","数字根","三才","量子","推演","权重","数学","甲骨文","字元","立碑","训练场","沙盒",
                     # ── 三才流场全集 ──
                     "三才流场","三才算法","三才权重","三才校验","天地人","天·地·人","MCP自适应","自适应引擎","流场",
                     "动态权重","权重流动","三才调度","三才MCP","三才引擎","三才结构","三才路由","三才维度",
                     # ── 算法核心 ──
                     "洛书矩阵","九宫","九宫格","河图","数字根","伏羲","太极推演","龍魂权重","曾老师智慧","能量场",
                     "IW-ECB","四层定锚","量子纠缠","叠加态","坍缩","向量","矩阵运算","369","共振",
                     "64卦","八卦","五行","阴阳","天干","地支","四柱","节气","干支"]
    },
    9: {
        "卦": "☲", "宫": "离", "方": "南", "维": "创新维",
        "色": "#e0d45a", "icon": "🌟",
        "desc": "元宇宙·设计·创意·公开·永生",
        "keywords": ["元宇宙","设计","创意","公开","发布","永生","七大支柱","文化","全球","赋能","开天辟地","终端","完整方案","数字永生","UI","界面","视觉","配色","字体","美学","CNSH字体","字形","像素","SVG","TTF","ComfyUI","图像","生成","艺术","创作","亚特兰蒂斯","虚拟世界","概念","设计稿","海报","品牌","logo"]
    }
}

# ══════════════════════════════════════════════
# 数字根算法（归一·不动点）
# ══════════════════════════════════════════════

def digital_root(n: int) -> int:
    """DR(n) = 1 + ((n-1) % 9)，归一到1-9，不动点"""
    if n <= 0: return 9
    return 1 + ((n - 1) % 9)

def title_to_dr(title: str) -> int:
    """标题→SHA256→取前4字节→数字根→洛书宫位"""
    h = hashlib.sha256(title.encode('utf-8')).digest()
    n = int.from_bytes(h[:4], 'big')
    return digital_root(n)

# ══════════════════════════════════════════════
# 关键词路由（语义优先·数字根兜底）
# ══════════════════════════════════════════════

def route_page(title: str, page_type: str = 'page') -> int:
    """
    路由规则：
    1. 关键词匹配（权重最高）
    2. 数字根兜底（归一原子）
    返回洛书宫位 1-9
    """
    # 特殊规则：数据库→2宫（架构维）
    if page_type == 'database':
        return 2

    t = title.lower()

    # 计算每宫得分
    scores = {}
    for palace, info in LUOSHU.items():
        score = 0
        for kw in info['keywords']:
            if kw.lower() in t or kw in title:
                score += len(kw)  # 长词权重更高
        scores[palace] = score

    max_score = max(scores.values())
    if max_score > 0:
        # 取最高分宫位
        winners = [p for p, s in scores.items() if s == max_score]
        return winners[0]

    # 兜底：数字根归一
    return title_to_dr(title)

# ══════════════════════════════════════════════
# 主函数：读取 index.jsonl → 分配九宫
# ══════════════════════════════════════════════

def load_pages(index_path: Path) -> list:
    pages = []
    with open(index_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try:
                d = json.loads(line)
                if 'item' not in d: continue
                item = d['item']
                title = item.get('title', '')
                url = item.get('url', '')
                ptype = item.get('type', 'page')
                if title:
                    pages.append({
                        'title': title,
                        'url': url,
                        'type': ptype,
                        'dna': d.get('dna', ''),
                        'palace': route_page(title, ptype)
                    })
            except Exception:
                continue
    return pages

def run_router():
    index_path = Path.home() / 'longhun-system' / 'notion-index' / 'out' / 'index.jsonl'
    if not index_path.exists():
        print("❌ 找不到 index.jsonl")
        return {}

    pages = load_pages(index_path)

    # 按宫位分组
    result = {i: [] for i in range(1, 10)}
    for p in pages:
        result[p['palace']].append(p)

    # 输出结果
    print(f"\n🐉 洛书九宫路由结果 · 共{len(pages)}页")
    print(f"DNA: #龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-LUOSHU-ROUTER-v1.0")
    print("="*60)

    luoshu_order = [4,9,2, 3,5,7, 8,1,6]
    for palace in luoshu_order:
        info = LUOSHU[palace]
        ps = result[palace]
        print(f"\n{info['icon']} {palace}宫·{info['卦']}·{info['宫']}({info['方']}) · {info['desc']} [{len(ps)}页]")
        for p in ps:
            dr = title_to_dr(p['title'])
            print(f"   {'pa' if p['type']=='page' else 'db'} [dr={dr}] {p['title'][:50]}")

    # 保存路由结果
    out_path = Path.home() / 'longhun-system' / 'logs' / 'luoshu_map.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({
            'dna': f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-LUOSHU-MAP-v1.0",
            'ts': datetime.now().isoformat(),
            'total': len(pages),
            'palaces': {str(k): v for k, v in result.items()}
        }, f, ensure_ascii=False, indent=2)

    print(f"\n🟢 路由完成 · 落盘 → {out_path}")
    return result

if __name__ == '__main__':
    run_router()
