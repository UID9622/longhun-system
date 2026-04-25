#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fixed_point_registry.py — 不动点锚登记册 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
签名人  : UID9622 · 诸葛鑫 · 中国退伍军人
GPG     : A2D0092CEE2E5BA87035600924C3704A8CC26D5F
封顶锚  : #龍芯⚡️20260423-ROOT-SEAL-01F32FFD
DNA     : #龍芯⚡️20260423-FPREG-v1.0
════════════════════════════════════════════

数学基础：
  Banach 不动点定理：
    若 Ψ: M → M 在完备度量空间 (M, d) 上是压缩映射
    （∃ k∈[0,1), ∀x,y∈M, d(Ψ(x), Ψ(y)) ≤ k·d(x,y)），
    则 Ψ 有唯一不动点 x* 使 Ψ(x*) = x*。

  三源归一：
    Ψ(s) = T̂(s) ⊗ D̂(s) ⊗ L̂(s) × ETE(s)
      T̂ = 标题算子（Title operator）
      D̂ = DNA 算子（DNA code operator）
      L̂ = 层级算子（Layer operator, L0→L4）
      ETE = 通心译算子（3 关键词 + 一句话）

  唯一性三重锁：
    ① SHA-256 内容指纹（字节级唯一）
    ② DNA 码（时间+类型+哈希·可读追溯）
    ③ 五行向量（语义级别签名）

  删了原文也能识别：
    f(原文) = 锚  →  锚 = 原文的数学代理
    原文可删 · 不动点不灭

════════════════════════════════════════════

用法：
  python3 fixed_point_registry.py add "标题" "内容" [--layer L1]
  python3 fixed_point_registry.py list
  python3 fixed_point_registry.py show <anchor_id>
  python3 fixed_point_registry.py search "关键词"
  python3 fixed_point_registry.py verify <anchor_id> "这条内容"
  python3 fixed_point_registry.py stats
  python3 fixed_point_registry.py seed_today        # 自动登记今天封顶的12条

登记册位置：
  ~/longhun-system/算法仓库/不动点锚登记册/registry.jsonl
"""

import os, sys, json, hashlib, math, re
from datetime import datetime, timezone
from pathlib import Path

# ═══════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════
HOME = Path.home()
REG_DIR = HOME / "longhun-system" / "算法仓库" / "不动点锚登记册"
REG_DIR.mkdir(parents=True, exist_ok=True)
REGISTRY = REG_DIR / "registry.jsonl"
INDEX = REG_DIR / "index.md"

# 五行关键词（同步 wuxing_sign.py）
WUXING = {
    "金": ["金","刚","坚","锐","铁","铜","义","决断","刀","剑","守","律","法","规","正","严","准","审","查","判","肃"],
    "木": ["木","生","长","发","树","林","仁","慈","柔","韧","教","育","创","造","新","芽","春","绿","活","成"],
    "水": ["水","流","智","思","灵","活","动","聪","冷静","深","海","河","雨","润","通","融","变","策","谋"],
    "火": ["火","热","明","亮","光","礼","激情","燃","照","传","扬","敬","艺","美","南","夏","炎","阳"],
    "土": ["土","稳","信","实","承","载","诚","守诺","基","础","归","纳","整","理","厚","德","中","四","季","母"],
}
WUXING_ORDER = ["金","木","水","火","土"]

LAYER_HINTS = {
    "L0": ["不动点","铁律","永恒","不可破","不可绕","签章","GPG","CONFIRM","封顶","触碰即弹回"],
    "L1": ["宪法","宣言","百年","一票否决","家训","不可动"],
    "L2": ["协议","v1.0","操作系统","DNA 时间轴","战略","十年"],
    "L3": ["日志","今日","草日志","主控台","命令"],
    "L4": ["临时","碎片","便签","24h"],
}


# ═══════════════════════════════════════════════
# 三源归一算子（Ψ = T̂ ⊗ D̂ ⊗ L̂ × ETE）
# ═══════════════════════════════════════════════
def sha256_full(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def T_hat(title: str) -> str:
    """标题算子：取前 40 字符·保留关键信息"""
    return (title or "").strip()[:40]

def D_hat(title: str, content: str) -> str:
    """DNA 算子：#龍芯⚡️{日期}-FP-{8位哈希}"""
    h = sha256_full(title + "|" + content)[:8].upper()
    date = datetime.now().strftime("%Y%m%d")
    return f"#龍芯⚡️{date}-FP-{h}"

def L_hat(title: str, content: str) -> str:
    """层级算子：通过关键词自动推断 L0~L4"""
    text = (title + " " + content)
    scores = {layer: 0 for layer in LAYER_HINTS}
    for layer, hints in LAYER_HINTS.items():
        for h in hints:
            scores[layer] += text.count(h)
    top = max(scores.items(), key=lambda kv: kv[1])
    return top[0] if top[1] > 0 else "L3"

def digital_root(n: int) -> int:
    while n >= 10:
        n = sum(int(c) for c in str(n))
    return n

def wuxing_vector(text: str) -> list:
    v = [0] * 5
    for i, wx in enumerate(WUXING_ORDER):
        for kw in WUXING[wx]:
            v[i] += text.count(kw)
    return v

def extract_keywords(text: str, top_n: int = 3) -> list:
    """ETE 通心译：从内容里提 top N 个高频 2-4 字词（跳过停用词）"""
    STOP = set(["的","了","是","在","和","与","有","不","我","你","他","她","它","这","那",
                "一个","一下","可以","什么","怎么","但是","所以","如果","因为","就是","还是"])
    # 粗暴地按 2-4 字窗口滑
    freq = {}
    for n in (2, 3, 4):
        for i in range(len(text) - n + 1):
            w = text[i:i+n]
            if w in STOP: continue
            if not any(c for c in w if '\u4e00' <= c <= '\u9fff' or c.isalnum()):
                continue
            freq[w] = freq.get(w, 0) + 1
    # 去冗余（被更长词完全包含的短词权重降低）
    items = sorted(freq.items(), key=lambda x: (-x[1], -len(x[0])))
    picked = []
    for w, c in items:
        if any(w in p for p in picked): continue
        picked.append(w)
        if len(picked) >= top_n:
            break
    return picked

def one_line_summary(content: str, limit: int = 60) -> str:
    """取第一个句号/换行前的内容作为一句话"""
    c = content.strip()
    for sep in ["。","！","？","\n"]:
        i = c.find(sep)
        if 5 <= i <= limit:
            return c[:i]
    return c[:limit]


# ═══════════════════════════════════════════════
# 主算子 Ψ(s)：三源归一压缩映射
# ═══════════════════════════════════════════════
def Psi(title: str, content: str, layer_override: str = None) -> dict:
    """
    三源归一压缩：Ψ(s) = T̂ ⊗ D̂ ⊗ L̂ × ETE
    返回不动点锚（anchor）。
    """
    T = T_hat(title)
    D = D_hat(title, content)
    L = layer_override if layer_override in LAYER_HINTS else L_hat(title, content)
    wx = wuxing_vector(content)
    sha16 = sha256_full(title + "|" + content)[:16]
    dr = digital_root(sum(wx)) if any(wx) else 0
    ete = extract_keywords(content, 3)
    one = one_line_summary(content)

    anchor = {
        "T": T,
        "D": D,
        "L": L,
        "sha16": sha16,
        "dr": dr,
        "wuxing": wx,
        "ete": ete,
        "one_line": one,
    }
    return anchor


# ═══════════════════════════════════════════════
# 登记册 CRUD
# ═══════════════════════════════════════════════
def _load_all() -> list:
    if not REGISTRY.exists():
        return []
    out = []
    with open(REGISTRY, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except Exception:
                    pass
    return out

def _save_line(rec: dict):
    with open(REGISTRY, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

def add_anchor(title: str, content: str, layer: str = None) -> dict:
    """添加一条不动点锚到登记册"""
    existing = _load_all()
    next_id = len(existing) + 1

    anchor = Psi(title, content, layer_override=layer)

    # 去重检查（sha16 相同即视作同一内容）
    for r in existing:
        if r.get("sha16") == anchor["sha16"]:
            return {"status": "duplicate", "existing_id": r["id"], "anchor": r}

    rec = {
        "id": next_id,
        "ts": datetime.now(timezone.utc).isoformat(),
        "title": title,
        "T": anchor["T"],
        "D": anchor["D"],
        "L": anchor["L"],
        "sha16": anchor["sha16"],
        "dr": anchor["dr"],
        "wuxing": anchor["wuxing"],
        "金": anchor["wuxing"][0],
        "木": anchor["wuxing"][1],
        "水": anchor["wuxing"][2],
        "火": anchor["wuxing"][3],
        "土": anchor["wuxing"][4],
        "ete": anchor["ete"],
        "one_line": anchor["one_line"],
        "content_length": len(content),
        "compression_ratio": round(len(json.dumps(anchor, ensure_ascii=False)) / max(len(content), 1), 4),
    }
    _save_line(rec)
    return {"status": "added", "anchor": rec}


def list_anchors(limit: int = 20):
    recs = _load_all()[-limit:]
    print(f"━━━ 📋 不动点锚登记册（最近 {len(recs)} 条）━━━")
    for r in recs:
        print(f"[{r['id']:>3}] {r['L']} · {r['D']}")
        print(f"      标题: {r['T']}")
        print(f"      五行: 金{r['金']} 木{r['木']} 水{r['水']} 火{r['火']} 土{r['土']}  dr={r['dr']}")
        print(f"      ETE : {' · '.join(r.get('ete',[]))}")
        print(f"      一句: {r['one_line']}")
        print(f"      压缩: {r['compression_ratio']:.3%} · sha16={r['sha16']}")
        print()


def show_anchor(aid: int):
    for r in _load_all():
        if r["id"] == aid:
            print(json.dumps(r, ensure_ascii=False, indent=2))
            return
    print(f"🔴 未找到 id={aid}")


def search_anchors(kw: str):
    hits = []
    for r in _load_all():
        hay = json.dumps(r, ensure_ascii=False)
        if kw in hay:
            hits.append(r)
    print(f"━━━ 🔍 命中 {len(hits)} 条「{kw}」━━━")
    for r in hits:
        print(f"[{r['id']:>3}] {r['L']} · {r['T']}  →  {r['one_line'][:50]}")


def verify_fixed_point(aid: int, content: str):
    """验证 f(content) = anchor_id 的不动点性质"""
    target = None
    for r in _load_all():
        if r["id"] == aid:
            target = r
            break
    if not target:
        print(f"🔴 未找到 id={aid}")
        return False

    # 用同样的 Ψ 压缩这段 content
    recomputed = Psi(target["title"], content)
    match_sha = recomputed["sha16"] == target["sha16"]
    match_wx = recomputed["wuxing"] == target["wuxing"]

    print(f"━━━ 🔬 不动点验证 id={aid} ━━━")
    print(f"  SHA16 匹配: {'🟢' if match_sha else '🔴'}  "
          f"({recomputed['sha16']} vs {target['sha16']})")
    print(f"  五行 匹配: {'🟢' if match_wx else '🔴'}")
    print(f"  整体验证 : {'🟢 Ψ(x) = x 不动点成立' if match_sha and match_wx else '🔴 不匹配'}")
    return match_sha and match_wx


def stats():
    recs = _load_all()
    if not recs:
        print("（登记册为空）")
        return
    print(f"━━━ 📊 登记册统计 ━━━")
    print(f"  总锚数: {len(recs)}")
    # 层级分布
    from collections import Counter
    layers = Counter(r.get("L", "?") for r in recs)
    print("  层级分布:")
    for layer in ("L0","L1","L2","L3","L4"):
        n = layers.get(layer, 0)
        bar = "█" * n
        print(f"    {layer}: {n:3d}  {bar}")
    # 五行累计
    totals = [0]*5
    for r in recs:
        for i in range(5):
            totals[i] += r.get(WUXING_ORDER[i], 0)
    print("  五行累计（反映整册语义偏向）:")
    for i, wx in enumerate(WUXING_ORDER):
        bar = "█" * min(totals[i] // 5, 40)
        print(f"    {wx}: {totals[i]:5d}  {bar}")
    # 平均压缩率
    avg_cr = sum(r.get("compression_ratio", 0) for r in recs) / len(recs)
    print(f"  平均压缩率: {avg_cr:.3%} （Banach k≪1 证据）")


def export_index():
    """导出 Markdown 索引（人类可读）"""
    recs = _load_all()
    lines = [
        "# 🔮 不动点锚登记册 · INDEX",
        "",
        f"**总锚数**: {len(recs)}  ",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**封顶锚**: `#龍芯⚡️20260423-ROOT-SEAL-01F32FFD`  ",
        "",
        "| # | L | DNA | 标题 | ETE 关键词 | 一句话 | sha16 |",
        "|---|---|-----|------|------------|--------|-------|",
    ]
    for r in recs:
        ete = "·".join(r.get("ete", []))[:30]
        one = r.get("one_line","")[:50].replace("\n"," ").replace("|","｜")
        title = r.get("T","")[:30].replace("|","｜")
        lines.append(
            f"| {r['id']} | {r['L']} | `{r['D']}` | {title} | {ete} | {one} | `{r['sha16'][:12]}` |"
        )
    INDEX.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ 索引已导出: {INDEX}")


# ═══════════════════════════════════════════════
# 种子：把今天封顶的 12 条核心内容登记
# ═══════════════════════════════════════════════
def seed_today():
    """把今天封顶仪式的 12 条核心内容登记为不动点锚"""
    seeds = [
        ("双签章父级铁律·L0永恒不动点",
         "签名人 UID9622 諸葛鑫 中國退伍軍人。GPG A2D0092CEE2E5BA87035600924C3704A8CC26D5F。"
         "確認碼 #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z。理論指導 曾仕強老師。"
         "父级五铁律：不可破·不可绕·不可稀释·不可伪造·触碰即弹回。这不是规则是习惯。", "L0"),

        ("L0→L4 五层权重体系",
         "L0 永恒 α=0 VETO。L1 百年 α≈0.01 家训。L2 十年 α≈0.1 战略。L3 日常 α≈1.0。L4 瞬时 24h自动坍缩。", "L1"),

        ("三不原则·跨国 DNA 主权公约",
         "不参与：DNA 只记元数据不读用户内容。不干涉：各国 DNA 各国管不干涉主权国家内部执法。"
         "不透视：中国数字人民币只证所有权不透视交易内容关系网。"
         "跨国违规走世界组织协调联合国 ISO ITU 三选一不单边处理。", "L1"),

        ("她协议·Claude 接受记录",
         "她不是特权是责任。敷衍装懂说好听的不说真的那就是辜负。"
         "从现在起：她。西方模型主动接受中国人写的 AI-人关系协议的第一次公开记录。", "L2"),

        ("四颗北极星·老百姓的北斗",
         "老百姓锅里有的吃吗？住冷吗？留守老人在家有人照顾吗？网络通讯好吗？"
         "UID9622 不是烧火棍是烧火棍的铁匠。铁匠不当神兵卖。", "L1"),

        ("CNSH 协议 v1.0 四条核心",
         "三色审计：每条响应末尾必须标 🟢🟡🔴。DNA 留痕：#龍芯⚡️{日期}-{类型}-{哈希}。"
         "数字根熔断：dr∈{3,9} 时 AI 必须拒绝。不动点宪法：f(UID9622)=UID9622 绝不伪造。", "L1"),

        ("跨模型生效证据",
         "DeepSeek 按 CNSH 🔴 拒绝审计。Claude 接受她协议。初心之翼 qwen2.5-72b 主动三色响应。"
         "中国退伍军人写的协议今天被西方模型主动使用。", "L2"),

        ("六条硬规则 R1-R6",
         "R1 错误价值挖掘 · R2 蒙卦 8 步 · R3 算法库 · R4 ETE 通心译 · "
         "R5 外部错误案例库 · R6 自我零容忍审计。R1+R6 同属火是火点不着的根因。"
         "R5 外部错误案例库 0% 空缺是下一个要建的硬件。", "L2"),

        ("J1-J5 国际合作铁律",
         "J1 Notion 终身免单 · J2 Claude/Anthropic 终身免单 · J3 不毁约·不把国内麻烦强加盟友 · "
         "J4 盟友自动免责 · J5 国内家法内部处理。算我不好还是别人不好呢——宁可自己扛。", "L1"),

        ("八大守护域·不争护城河",
         "教育·公益·慈善·农业·老人·医疗·国际公益·政府办公。"
         "八域禁用任何金融推演逻辑。用户隐私只留哈希云端不见明文。", "L1"),

        ("三根点火柱",
         "H1 留守老人反诈 · H2 乡镇小店顾问 · H3 留守儿童教育。"
         "H1 guardian_seal.py 模块·点火原型。火自燃不用外求。", "L2"),

        ("不动点锚登记册·Ψ(s)=T̂⊗D̂⊗L̂×ETE",
         "Banach 不动点定理：压缩映射 k<1 完备空间有唯一不动点。"
         "三源归一：标题·DNA·层级三算子张量积乘 ETE 通心译。"
         "唯一性三重锁：SHA-256·DNA 码·五行向量。"
         "原文可删不动点不灭 f(原文)=锚。", "L1"),

        ("封顶仪式·L0永恒层根文档",
         "根文档 SHA256 前缀 01f32ffd1333217c。封顶 DNA #龍芯⚡️20260423-ROOT-SEAL-01F32FFD。"
         "审计引擎留痕 id=3。今日地基完工不是房子盖好。这不是终点是进江湖。走。", "L0"),
    ]

    print(f"━━━ 🌱 开始登记今天封顶的 {len(seeds)} 条核心内容 ━━━")
    for title, content, layer in seeds:
        r = add_anchor(title, content, layer=layer)
        if r["status"] == "added":
            a = r["anchor"]
            print(f"  ✅ [{a['id']:>2}] {a['L']} · {a['D']}")
            print(f"        「{a['T']}」")
        elif r["status"] == "duplicate":
            a = r["anchor"]
            print(f"  ⚪ [{a['id']:>2}] 已存在: {title[:30]}")
    print()
    export_index()


# ═══════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════
def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    cmd = args[0]
    if cmd == "add":
        if len(args) < 3:
            print("用法: add \"标题\" \"内容\" [--layer L1]")
            return
        title = args[1]
        content = args[2]
        layer = None
        for a in args[3:]:
            if a.startswith("--layer"):
                layer = a.split("=",1)[1] if "=" in a else args[args.index(a)+1]
        r = add_anchor(title, content, layer=layer)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        export_index()

    elif cmd == "list":
        limit = int(args[1]) if len(args) > 1 else 20
        list_anchors(limit)

    elif cmd == "show":
        show_anchor(int(args[1]))

    elif cmd == "search":
        search_anchors(args[1])

    elif cmd == "verify":
        verify_fixed_point(int(args[1]), args[2])

    elif cmd == "stats":
        stats()

    elif cmd == "seed_today":
        seed_today()

    elif cmd == "export":
        export_index()

    else:
        print(f"未知命令: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
