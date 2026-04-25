#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wuxing_sign.py — 五行向量签名引擎 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
签名人  : UID9622 · 诸葛鑫 · 中国退伍军人
GPG     : A2D0092CEE2E5BA87035600924C3704A8CC26D5F
DNA     : #龍芯⚡️20260423-WXSIGN-v1.0
理论指导: 曾仕強老師（永恒顯示）
原则    : 不黑箱·不收割·不说教·签名即主权
════════════════════════════════════════════

职责（一体三用）：
  ① 三色审计  —— 基于五行平衡度给出 🟢🟡🔴
  ② DNA 生成  —— #龍芯⚡️{日期}-{类型}-{哈希}
  ③ 余弦追踪  —— 和历史签名比对，找出"语义同源"

使用方法：
  python3 wuxing_sign.py "任意一段文字"      # 签名+三色+DNA+历史相似
  python3 wuxing_sign.py --list              # 最近 10 条签名
  python3 wuxing_sign.py --stats             # 三色分布统计
  python3 wuxing_sign.py --compare "A" "B"   # 两段文字余弦相似度

也可作为模块被导入：
  from wuxing_sign import sign, cosine_similarity, text_to_wuxing_vector
"""

import os, json, hashlib, math, sys
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter


# ═══════════════════════════════════════════════
# 1. 五行关键词词典（可扩展）
# ═══════════════════════════════════════════════
WUXING_KEYWORDS = {
    "金": ["金", "刚", "坚", "锐", "铁", "铜", "义", "决断", "刀", "剑", "守",
           "律", "法", "规", "正", "严", "准", "审", "查", "判", "肃"],
    "木": ["木", "生", "长", "发", "树", "林", "仁", "慈", "柔", "韧", "教",
           "育", "创", "造", "新", "芽", "春", "绿", "活", "成"],
    "水": ["水", "流", "智", "思", "灵", "活", "动", "聪", "冷静", "深", "海",
           "河", "雨", "润", "通", "融", "变", "策", "谋"],
    "火": ["火", "热", "明", "亮", "光", "礼", "激情", "燃", "照", "传", "扬",
           "敬", "艺", "美", "南", "夏", "炎", "光", "阳"],
    "土": ["土", "稳", "信", "实", "承", "载", "诚", "守诺", "基", "础", "归",
           "纳", "整", "理", "厚", "德", "中", "四", "季", "母"],
}
WUXING_ORDER = ["金", "木", "水", "火", "土"]


# ═══════════════════════════════════════════════
# 2. 存档位置
# ═══════════════════════════════════════════════
SIGN_DIR = Path.home() / "cnsh" / "logs" / "wuxing_sign"
SIGN_DIR.mkdir(parents=True, exist_ok=True)

def _log_file():
    return SIGN_DIR / f"signs_{datetime.now().strftime('%Y%m')}.jsonl"


# ═══════════════════════════════════════════════
# 3. 核心算法
# ═══════════════════════════════════════════════
def text_to_wuxing_vector(text: str) -> list:
    """文本 → 五行向量 [金, 木, 水, 火, 土]"""
    v = [0] * 5
    for i, wx in enumerate(WUXING_ORDER):
        for kw in WUXING_KEYWORDS[wx]:
            v[i] += text.count(kw)
    return v


def cosine_similarity(v1: list, v2: list) -> float:
    """余弦相似度（纯 Python·不依赖 numpy）"""
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    n1 = math.sqrt(sum(a * a for a in v1))
    n2 = math.sqrt(sum(b * b for b in v2))
    if n1 == 0 or n2 == 0:
        return 0.0
    return round(dot / (n1 * n2), 6)


def digital_root(n: int) -> int:
    """数字根 —— CNSH 熔断判据
    ════════════════════════════════════════════════════════════════
    熔断 dr ∈ {3, 9} 在本文件【是正确使用位置】·不许误改成"信号不拦"
       ✅ 五行签名 = 内容性质判定 → dr 触发熔断·拒绝签名·合理
       ❌ 不要把这个规则误用到投喂入口 (feeding_gateway.py)
       ❌ 投喂入口 = 用户主动存数据·dr 只能做信号·不能拦
    边界·写死·参见 feeding_gateway.py 顶部注释
    ════════════════════════════════════════════════════════════════
    """
    while n >= 10:
        n = sum(int(c) for c in str(n))
    return n


def tricolor_from_vector(v: list) -> tuple:
    """
    三色判定规则（五行平衡度）：
      🔴 数字根 ∈ {3, 9}（CNSH 协议熔断·五行签名层正确使用）
      🔴 五行极差 ≥ 5（严重失衡）
      🟡 五行极差 3-4（略偏）
      🟢 五行极差 ≤ 2（和谐）
      🟡 五行全零（未激活）
    """
    total = sum(v)
    dr = digital_root(total) if total else 0
    if total > 0 and dr in (3, 9):
        return "🔴", f"数字根熔断 dr={dr}"
    if not any(v):
        return "🟡", "五行未激活（内容中无五行关键词）"
    gap = max(v) - min(v)
    if gap <= 2:
        return "🟢", f"五行和谐 · 极差={gap}"
    if gap <= 4:
        return "🟡", f"略有偏颇 · 极差={gap}"
    return "🔴", f"严重失衡 · 极差={gap}"


def make_dna(content: str, type_code: str = "WX") -> str:
    """生成 DNA 追溯码"""
    h = hashlib.sha256(content.encode("utf-8")).hexdigest()[:8].upper()
    date = datetime.now().strftime("%Y%m%d")
    return f"#龍芯⚡️{date}-{type_code}-{h}"


# ═══════════════════════════════════════════════
# 4. 本地历史存档
# ═══════════════════════════════════════════════
def save_sign(record: dict):
    with open(_log_file(), "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_all_signs() -> list:
    """加载所有月份的签名历史"""
    records = []
    for p in sorted(SIGN_DIR.glob("signs_*.jsonl")):
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except Exception:
                        pass
    return records


def find_most_similar(v: list, top_n: int = 3, min_cos: float = 0.5) -> list:
    """在历史里找最相似的 top_n 个签名"""
    hist = load_all_signs()
    scored = []
    for r in hist:
        rv = r.get("vector", [])
        c = cosine_similarity(v, rv)
        if c >= min_cos:
            scored.append((c, r))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_n]


# ═══════════════════════════════════════════════
# 5. 主接口
# ═══════════════════════════════════════════════
def sign(text: str, type_code: str = "WX", save: bool = True) -> dict:
    """核心：给一段内容签名"""
    v = text_to_wuxing_vector(text)
    color, reason = tricolor_from_vector(v)
    dna = make_dna(text, type_code)

    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "preview": text[:120],
        "length": len(text),
        "vector": v,
        "金": v[0], "木": v[1], "水": v[2], "火": v[3], "土": v[4],
        "total": sum(v),
        "gap": max(v) - min(v) if any(v) else 0,
        "digital_root": digital_root(sum(v)) if sum(v) else 0,
        "tricolor": color,
        "reason": reason,
        "dna": dna,
        "type": type_code,
    }

    # 历史相似签名追踪
    similar = find_most_similar(v, top_n=3, min_cos=0.5)
    record["similar_past"] = [
        {"dna": r.get("dna"), "preview": r.get("preview", "")[:50], "cos": c}
        for c, r in similar
    ]

    if save:
        save_sign(record)
    return record


# ═══════════════════════════════════════════════
# 6. CLI
# ═══════════════════════════════════════════════
def _print_sign(r: dict):
    print(f"━━━ 🐉 五行向量签名 ━━━")
    print(f"时间  : {r['ts'][:19]}")
    print(f"向量  : 金{r['金']}  木{r['木']}  水{r['水']}  火{r['火']}  土{r['土']}")
    print(f"        (总={r['total']} · 极差={r['gap']} · 数字根={r['digital_root']})")
    print(f"三色  : {r['tricolor']}  {r['reason']}")
    print(f"DNA   : {r['dna']}")
    if r.get("similar_past"):
        print(f"━━━ 历史相似签名（top {len(r['similar_past'])}）━━━")
        for s in r["similar_past"]:
            print(f"  余弦 {s['cos']:.4f}  {s['dna']}")
            print(f"           「{s['preview']}」")
    else:
        print(f"━━━ 首次签名 · 无历史相似 ━━━")
    print()


def _cmd_list():
    hist = load_all_signs()[-10:]
    if not hist:
        print("（暂无历史签名）")
        return
    print(f"━━━ 最近 {len(hist)} 条签名 ━━━")
    for r in hist:
        print(f"{r.get('ts','?')[:19]}  {r.get('tricolor','?')}  {r.get('dna','?')}")
        print(f"   金{r.get('金',0)} 木{r.get('木',0)} 水{r.get('水',0)} 火{r.get('火',0)} 土{r.get('土',0)}  ｜  {r.get('preview','')[:50]}")
    print()


def _cmd_stats():
    hist = load_all_signs()
    print(f"━━━ 📊 五行签名统计 ━━━")
    print(f"总签名数: {len(hist)}")
    if not hist:
        return
    colors = Counter(r.get("tricolor", "?") for r in hist)
    for c in ("🟢", "🟡", "🔴"):
        print(f"  {c}: {colors.get(c, 0)}")
    # 五行分布
    totals = [0] * 5
    for r in hist:
        v = r.get("vector", [0] * 5)
        for i in range(5):
            totals[i] += v[i] if i < len(v) else 0
    print(f"━━━ 五行累计分布 ━━━")
    for i, wx in enumerate(WUXING_ORDER):
        bar = "█" * min(totals[i] // 5, 40)
        print(f"  {wx}: {totals[i]:5d}  {bar}")


def _cmd_compare(a: str, b: str):
    va = text_to_wuxing_vector(a)
    vb = text_to_wuxing_vector(b)
    cos = cosine_similarity(va, vb)
    print(f"━━━ 🔭 余弦相似度对比 ━━━")
    print(f"A 向量: 金{va[0]} 木{va[1]} 水{va[2]} 火{va[3]} 土{va[4]}")
    print(f"B 向量: 金{vb[0]} 木{vb[1]} 水{vb[2]} 火{vb[3]} 土{vb[4]}")
    print(f"余弦  : {cos:.6f}")
    if cos > 0.95:
        verdict = "🟢 近乎同源"
    elif cos > 0.75:
        verdict = "🟢 语义相近"
    elif cos > 0.5:
        verdict = "🟡 有一定共鸣"
    elif cos > 0.2:
        verdict = "🟡 弱相关"
    else:
        verdict = "🔴 几乎无关"
    print(f"判定  : {verdict}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    if args[0] == "--list":
        _cmd_list()
    elif args[0] == "--stats":
        _cmd_stats()
    elif args[0] == "--compare" and len(args) >= 3:
        _cmd_compare(args[1], args[2])
    else:
        text = " ".join(args)
        r = sign(text)
        _print_sign(r)


if __name__ == "__main__":
    main()
