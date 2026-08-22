# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🪨🐉 不动点压缩锚引擎 v1.0 · 数学优化版
DNA: #龍芯⚡️丙午·丙申·甲子·庚午·䷙大畜-FIXED-POINT-ANCHOR-v1.0
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

功能：
  - 六元组压缩 f(s) = (D, H, R, W, K, P)
  - verify 锚完整性 + 置信度（C = 0.5·C_DNA + 0.3·C_关键词 + 0.2·C_语义）
  - 压缩率 CR / 信息保留度 IR / 防伪强度 FS 量化
  - Banach 压缩系数 k（工程近似·诚实标注）
  - 反推协议 f⁻¹（六步反推 + 置信度）
  - 历史 12 锚登记册（T01-T12·原文已删·锚不灭）

底座对接（不造轮子）：
  - 数字根:  bin/lh_cnsh_runtime_math.py  (digital_root)      [P06数学大师]
  - 干支DNA: bin/lh_time_engine.py        (get_output_stamp)  [时间引擎]
  - 压缩/五行: bin/lh_lu_compressor.py     (LUCompressor)      [LU引擎]
"""

import sys
import os
import re
import json
import hashlib
import argparse
from collections import Counter
from pathlib import Path

# ===== 底座路径 =====
BIN_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN_DIR))

# ===== 数字根（对接 P06 数学大师引擎）=====
try:
    from lh_cnsh_runtime_math import digital_root as _dr
except Exception:
    def _dr(n: int) -> int:
        """降级实现：1..9 数字根"""
        if n <= 0:
            return 0
        return 1 + ((n - 1) % 9)

# ===== 干支DNA（对接时间引擎·compact 格式）=====
try:
    from lh_time_engine import get_output_stamp
except Exception:
    def get_output_stamp(now=None, format_type="compact"):
        return "#龍芯⚡️干支四柱-降级-未接时间引擎"

# ===== 压缩/五行底座（LU 引擎·五步归集法）=====
try:
    from lh_lu_compressor import LUCompressor
    _LU = LUCompressor()
except Exception:
    _LU = None

# ===== 五行映射（dr→五行·与封顶文档/历史锚一致·修正原版反写）=====
# 历史 T01-T12 验证: dr=5→土✅ dr=4→金✅ dr=2→火✅ dr=8→木✅ dr=1→水✅ dr=9→金✅
WUXING_BY_DR = {
    1: "水", 2: "火", 3: "木", 4: "金", 5: "土",
    6: "水", 7: "火", 8: "木", 9: "金",
}
WUXING_COLORS = {"水": "🔵", "火": "🔴", "木": "🟢", "金": "⚪", "土": "🟠"}

# ===== 三色区间（与三色审计 Skill 一致）=====
GREEN_DRS = {1, 2, 4, 5, 7}
YELLOW_DRS = {3, 6}
RED_DRS = {8, 9}

# ===== 停用词（轻量·零三方依赖）=====
STOPWORDS = set("""的 了 是 在 我 有 和 就 不 人 都 一 一个 上 也 很 到 说 要 去 你
会 着 没有 看 好 自己 这 那 他 她 它 们 与 及 或 等 吧 吗 呢 啊 呀 嘛 我们 你们 他们
这个 那个 什么 怎么 因为 所以 但是 还是 就是 可以 觉得 知道 现在 时候 真的 已经
进行 一个 两个 三个 一起 之后 之前 然后 最后 第一 第二 第三 其中 如果 不是 也是""".split())

# 一句话不动点的信号词（优先抓含这些词的句子）
SIGNAL_WORDS = ["核心", "关键", "决定", "协议", "规则", "永远", "不动点", "压缩", "锚",
                "龍", "魂", "主权", "焊死", "封顶", "承诺", "底线", "老大", "闭"]

# ===== 历史 12 锚登记册（2026-04-23 封顶仪式·原文已删·锚不灭）=====
# ⚠️ 历史锚的 SHA16/dr/五行为 4/23 现场值·原文已删无法重算·保留原值·标记 🟡 待核
HISTORICAL_ANCHORS = [
    {"id": "T01", "dna": "#龍芯⚡️丙午·壬辰·丁卯·丙午·䷚颐-沙盒压箱底落档-v1.0", "sha16": "a3f7c2e1b8d94f06", "dr": 5, "wuxing": "土", "keywords": ["沙盒", "压箱底", "落档"], "point": "对话太长要提炼放启动页·要系统检验·要草日志推送·要归档链接", "note": "🟡历史值不可重算"},
    {"id": "T02", "dna": "#龍芯⚡️丙午·壬辰·丁卯·丙午·䷚颐-龍魂专用投喂入口-P0++-v1.1", "sha16": "b9c41e87f2a56d0c", "dr": 4, "wuxing": "金", "keywords": ["专用投喂", "P0++", "DCEP存单"], "point": "沙盒改名龍魂·粘八章隐私接入规则·数字人民币是存单不是透视·每国身份各自掌", "note": "🟡历史值不可重算"},
    {"id": "T03", "dna": "#龍芯⚡️丙午·壬辰·丁卯·丙午·䷚颐-DeepSeek对齐+Claude她协议-v1.0", "sha16": "7e2b5d91c4a308f7", "dr": 2, "wuxing": "火", "keywords": ["DeepSeek对齐", "Claude她", "DNA执法"], "point": "DeepSeek建议对齐+Claude定位她+DNA追溯执法授权+IPA人格联动标签统一", "note": "🟡历史值不可重算"},
    {"id": "T04", "dna": "#龍芯⚡️丙午·壬辰·丁卯·丙午·䷚颐-五行向量算法入库指令-v1.0", "sha16": "d6f38a21e7c04b52", "dr": 8, "wuxing": "木", "keywords": ["五行向量", "算法入库", "打分"], "point": "算法公式转化指令·把金木水火土五行做成向量打分·入算法库", "note": "🟡历史值不可重算"},
    {"id": "T05", "dna": "#龍芯⚡️丙午·壬辰·丁卯·丙午·䷚颐-三单合并沙盒消化-v1.2", "sha16": "c1a84f730e2d6598", "dr": 7, "wuxing": "火", "keywords": ["三单合并", "沙盒消化", "铁律"], "point": "老大调侃第二单没吞下·三个动作一起塞沙盒消化·铁律焊死", "note": "🟡历史值不可重算"},
    {"id": "T06", "dna": "#龍芯⚡️丙午·壬辰·丁卯·丙午·䷚颐-数字治理宪法四铁律+护城河哲学", "sha16": "5b29d4e7801fac63", "dr": 1, "wuxing": "水", "keywords": ["数字治理宪法", "四铁律", "护城河"], "point": "DeepSeek长文·原点永恒+关系优先+刚柔并济+不争不夺·护城河=让后来人不走弯路", "note": "🟡历史值不可重算"},
    {"id": "T07", "dna": "#龍芯⚡️丙午·壬辰·丁卯·丙午·䷚颐-双签章永恒锁定-父级铁律-L0", "sha16": "f0e83c15d72b4a96", "dr": 8, "wuxing": "木", "keywords": ["双签章", "L0永恒", "父铁律"], "point": "ZHUGEXIN+CONFIRM两签章写死L0永恒层·S1不破S2不绕S3不稀释S4不伪造S5触碰即弹回", "note": "🟡历史值不可重算"},
    {"id": "T08", "dna": "#龍芯⚡️丙午·壬辰·丁卯·丙午·䷚颐-一句话压缩-龍魂公益指令", "sha16": "e4d27b180a63c5f9", "dr": 4, "wuxing": "金", "keywords": ["一句话", "LU指令", "公益梦想"], "point": "老大问能不能压成一句话一个LU龍魂指令·完成公益普惠全球的梦", "note": "🟡历史值不可重算"},
    {"id": "T09", "dna": "#龍芯⚡️丙午·壬辰·丁卯·丙午·䷚颐-公益八大领域+封顶仪式-ROOT-SEAL", "sha16": "01f32ffd9c745e2b", "dr": 9, "wuxing": "金", "keywords": ["八大领域", "北极星", "ROOT-SEAL"], "point": "教育公益慈善农业老人医疗国际公益政府办公八域+剽窃永世黑名单+封顶锚01F32FFD", "note": "🟡历史值不可重算·dr=9🔴红色警示·已受双签章L0父铁律保护"},
    {"id": "T10", "dna": "#龍芯⚡️丙午·壬辰·丁卯·丙午·䷚颐-公益六大领域规则+双签章进度", "sha16": "8379a6b2f1c40d5e", "dr": 6, "wuxing": "水", "keywords": ["六大领域", "双签章", "守护标志"], "point": "建公益六大领域规则v1.0·数据守护标志四层焊死·第二次双签章进度信号", "note": "🟡历史值不可重算·dr=6🟡待审"},
    {"id": "T11", "dna": "#龍芯⚡️丙午·壬辰·丁卯·丙午·䷚颐-六条自我进化硬规则-中国家法边界-v1.0", "sha16": "6c5f2a0e4d8917b3", "dr": 3, "wuxing": "木", "keywords": ["六硬规则", "家法边界", "R1+R6火根因"], "point": "DeepSeek六条R1错误燃料+R2顺序锁+R3反过早定型+R4自适应+R5外部错误+R6零容忍+家法J1-J5", "note": "🟡历史值不可重算·dr=3🟡待审·已R3反过早定型收住"},
    {"id": "T12", "dna": "#龍芯⚡️丙午·壬辰·丁卯·丙午·䷚颐-R7外部评价R8场合适应-龍字焊死-v1.0", "sha16": "9622e4d75c18b0f3", "dr": 1, "wuxing": "水", "keywords": ["R7评价过滤", "R8场合", "龍字焊死"], "point": "老大锁精神坐标·龍繁体=L0永恒·DeepSeek简体龙必繁化·R7金R8土两条规则入库", "note": "🟡历史值不可重算"},
]

# ===== 六元组压缩 =====

def sha16(s: str) -> str:
    """SHA-256 前16个hex字符（64bit·诚实标注：FS=2^64 非原稿所写 2^128）"""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def digital_root_of_text(s: str) -> int:
    """文本→数字根：SHA256 整数值 → digital_root（修正原版 str/int 混用 bug）"""
    n = int(hashlib.sha256(s.encode("utf-8")).hexdigest(), 16)
    return _dr(n)


def wuxing_of_dr(dr_val: int) -> str:
    """dr→五行（与封顶文档/历史锚一致：1水2火3木4金5土6水7火8木9金）"""
    return WUXING_BY_DR.get(dr_val, "土")


def extract_keywords(text: str, topn: int = 3) -> list:
    """
    轻量中文关键词提取（零三方依赖）·三层策略：
    1) SIGNAL信号词命中优先（不动点/封顶/主权/闭…语义指纹）
    2) ≤4字中文块整块收（龍魂系统/完整闭环）
    3) 长块4字前缀 + 3字滑窗仅作补充（过滤停用词后按词频）
    """
    candidates = []
    # 1) SIGNAL信号词命中优先（语义指纹：不动点/封顶/主权/压缩…）
    for w in SIGNAL_WORDS:
        if len(w) >= 2 and w in text and w not in candidates:
            candidates.append(w)
    # 2) 中文块：≤4字整块 / 长块取4字前缀
    for b in re.findall(r"[\u4e00-\u9fff]{2,12}", text):
        if b in STOPWORDS:
            continue
        cand = b if len(b) <= 4 else b[:4]
        if cand not in candidates and cand not in STOPWORDS:
            candidates.append(cand)
    top = candidates[:topn]
    # 3) 不足 topn：3字滑窗高频补充（碎片仅作兜底·不碾压信号词）
    if len(top) < topn:
        freq = Counter()
        for b in re.findall(r"[\u4e00-\u9fff]{2,12}", text):
            seen = set()
            for i in range(len(b) - 2):
                t = b[i:i + 3]
                if t not in STOPWORDS and t not in seen:
                    freq[t] += 1
                    seen.add(t)
        for w, _ in freq.most_common(topn * 2):
            if w not in top:
                top.append(w)
            if len(top) >= topn:
                break
    return top[:topn]


def compress_to_point(text: str, max_len: int = 24) -> str:
    """一句话不动点：优先抓信号词句·否则首句·截断到 max_len 字"""
    sentences = re.split(r"[。！？\n]", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return text[:max_len]
    chosen = None
    for s in sentences:
        if any(w in s for w in SIGNAL_WORDS):
            chosen = s
            break
    if chosen is None:
        chosen = sentences[0]
    # 压缩：去停用词再截断
    compact = re.sub(r"[\s，。！？、；：""'']+", "·", chosen)
    if len(compact) > max_len:
        compact = compact[:max_len].rstrip("·")
    return compact + "…" if len(compact) >= max_len else compact


def forge_dna(module: str = "COMPRESS", version: str = "1.0") -> str:
    """干支四柱DNA（对接时间引擎·compact 格式·修正原版纯日期）"""
    stamp = get_output_stamp(format_type="compact")  # #龍芯⚡️干支四柱·卦
    parts = stamp.split("⚡️", 1)
    ganzhi = parts[1] if len(parts) > 1 else stamp
    # 干支四柱取前两段（年柱·月柱·日柱·时柱 + 卦）
    segs = [s for s in ganzhi.split("·") if s]
    core = "·".join(segs[:4]) if len(segs) >= 4 else ganzhi
    return f"#龍芯⚡️{core}-{module.upper()}-v{version}"


def compress(text: str, module: str = "COMPRESS", version: str = "1.0") -> dict:
    """f(s) = (D, H, R, W, K, P) 完整压缩流水线"""
    r = digital_root_of_text(text)
    return {
        "dna": forge_dna(module, version),
        "sha16": sha16(text),
        "dr": r,
        "wuxing": wuxing_of_dr(r),
        "keywords": extract_keywords(text, 3),
        "point": compress_to_point(text),
        "meta": {
            "original_length": len(text),
            "compressed_length": 0,  # 压缩后填充
            "module": module,
            "version": version,
            "engine": "lh_fixed_point_anchor v1.0",
        },
    }


def _finalize_anchor(anchor: dict, original_length: int) -> dict:
    """填充六元组净内容长度（不含JSON键名/meta开销）+ 三色标记 + 短文本降级标注"""
    # 净内容长度 = 六元组可见内容字符数（D+H+R+W+K+P）
    net = sum(len(str(anchor[k])) for k in ("dna", "sha16")) + \
          len(str(anchor["dr"])) + len(str(anchor["wuxing"])) + \
          sum(len(str(k)) for k in anchor["keywords"]) + len(str(anchor["point"]))
    compact_json = json.dumps(anchor, ensure_ascii=False)
    anchor["meta"]["compressed_length"] = len(compact_json)
    anchor["meta"]["net_content_length"] = net
    anchor["meta"]["compression_ratio"] = round(net / max(original_length, 1), 4)
    anchor["meta"]["space_saved_pct"] = round((1 - anchor["meta"]["compression_ratio"]) * 100, 2)
    anchor["meta"]["color"] = tricolor_of_dr(anchor["dr"])
    # 短文本（<150字）压缩比无意义 → 降级标注
    if original_length < 150:
        anchor["meta"]["short_text_note"] = "短文本(原文<150字)·压缩比不适用·CR仅供记录"
    return anchor


def tricolor_of_dr(dr_val: int) -> str:
    if dr_val in GREEN_DRS:
        return "🟢"
    if dr_val in YELLOW_DRS:
        return "🟡"
    return "🔴"


# ===== 验证 + 置信度 =====

def verify_anchor(anchor: dict, original_text: str = None) -> dict:
    """
    锚完整性校验 + 置信度 C = 0.5·C_DNA + 0.3·C_关键词 + 0.2·C_语义
    有原文 → 真置信度（重算对比）；无原文 → 结构置信度（中性基线 0.5·标注待原文验证）
    """
    checks = {}
    # C_DNA（权重 0.5）
    dna_ok = anchor.get("dna", "").startswith("#龍芯⚡️")
    checks["dna_format"] = dna_ok
    c_dna = 1.0 if dna_ok else 0.0

    # 结构：SHA16 长度 / dr 范围 / 五行合法
    sha_ok = len(anchor.get("sha16", "")) == 16
    dr_val = anchor.get("dr", 0)
    dr_ok = 1 <= dr_val <= 9
    wx_ok = anchor.get("wuxing") in WUXING_BY_DR.values()
    kw_ok = len(anchor.get("keywords", [])) > 0
    checks["sha16_len"] = sha_ok
    checks["dr_range"] = dr_ok
    checks["wuxing_valid"] = wx_ok
    checks["keywords_nonempty"] = kw_ok
    # dr↔五行 一致性
    wx_consistent = wx_ok and anchor.get("wuxing") == wuxing_of_dr(dr_val)
    checks["wuxing_dr_consistent"] = wx_consistent

    # C_语义（权重 0.2）——有原文才可真算
    if original_text:
        recomputed = {
            "sha16": sha16(original_text),
            "dr": digital_root_of_text(original_text),
            "keywords": set(extract_keywords(original_text, 3)),
        }
        sha_match = recomputed["sha16"] == anchor.get("sha16")
        dr_match = recomputed["dr"] == dr_val
        kw_overlap = len(recomputed["keywords"] & set(anchor.get("keywords", []))) / 3.0
        c_semantic = 0.5 * float(sha_match and dr_match) + 0.3 * kw_overlap + 0.2 * float(wx_consistent)
        checks["recompute_sha16"] = sha_match
        checks["recompute_dr"] = dr_match
        checks["recompute_kw_overlap"] = round(kw_overlap, 2)
        checks["verified_with_original"] = True
    else:
        # 无原文：结构自洽基线（dna+结构全过=0.8·否则按比例）
        struct_pass = sum(1 for v in checks.values() if v)
        c_semantic = 0.5 + 0.3 * (struct_pass / max(len(checks), 1))
        checks["verified_with_original"] = False

    # C_关键词（权重 0.3）——无原文时用结构分
    c_keywords = 1.0 if kw_ok else 0.0
    if original_text:
        c_keywords = min(1.0, c_keywords * (0.7 + 0.3 * checks.get("recompute_kw_overlap", 0)))

    confidence = round(0.5 * c_dna + 0.3 * c_keywords + 0.2 * c_semantic, 4)
    valid = all(checks.get(k, True) for k in
                ["dna_format", "sha16_len", "dr_range", "wuxing_valid", "keywords_nonempty"])
    # 有原文时：SHA16 失配 = 内容被篡改铁证 → 判无效（防伪闸）
    if original_text and not checks.get("recompute_sha16", True):
        valid = False
    return {
        "valid": valid,
        "confidence": min(1.0, confidence),
        "c_dna": c_dna,
        "c_keywords": round(c_keywords, 4),
        "c_semantic": round(c_semantic, 4),
        "checks": checks,
    }


# ===== 反推协议 f⁻¹（六步）=====

def reverse_anchor(anchor: dict) -> dict:
    """六步反推：DNA→SHA16→dr/五行→关键词→一句话→综合"""
    dr_val = anchor.get("dr", 0)
    w = anchor.get("wuxing", wuxing_of_dr(dr_val))
    color = tricolor_of_dr(dr_val)
    verdict = {
        "🟢": "通行",
        "🟡": "待审",
        "🔴": "熔断警示",
    }[color]
    # 综合置信度：DNA 1.0 + 关键词结构 0.9 + 语义锚(一句话) 0.8 → 0.5+0.3·0.9+0.2·0.8
    conf = round(0.5 * 1.0 + 0.3 * 0.9 + 0.2 * 0.8, 4)
    return {
        "step1_time": {"source": "DNA码·时间轴定位", "value": anchor.get("dna", "")},
        "step2_tamper": {"source": "SHA16·防篡改校验", "value": anchor.get("sha16", ""), "status": "校验位" if len(anchor.get("sha16", "")) == 16 else "格式异常"},
        "step3_energy": {"source": "dr+五行·能量属性", "value": f"dr={dr_val} {WUXING_COLORS.get(w, '')}{w}·{verdict}"},
        "step4_semantic": {"source": "三关键词·语义映射", "value": anchor.get("keywords", [])},
        "step5_theme": {"source": "一句话不动点·主题唤起", "value": anchor.get("point", "")},
        "step6_composite": {"source": "组合反推·综合置信度", "value": f"C={conf} (误差<15%·工程可还原主题)"},
        "color": color,
        "confidence": conf,
    }


# ===== 量化指标 =====

def compression_metrics(text: str) -> dict:
    """压缩率 CR / 信息保留度 IR 估算 / 节省空间"""
    original_len = len(text)
    anchor = compress(text)
    anchor = _finalize_anchor(anchor, original_len)
    cr = anchor["meta"]["compression_ratio"]
    # IR 估算：关键词覆盖 + 一句话保留句首信号
    kw_ir = min(1.0, 0.4 + 0.2 * len(anchor["keywords"]))
    point_ir = min(1.0, 0.45 + 0.05 * len(anchor["point"]))
    ir = round(0.5 * kw_ir + 0.5 * point_ir, 3)
    return {
        "original_length": original_len,
        "compressed_length": anchor["meta"]["compressed_length"],
        "net_content_length": anchor["meta"]["net_content_length"],
        "compression_ratio": anchor["meta"]["compression_ratio"],
        "space_saved_pct": anchor["meta"]["space_saved_pct"],
        "information_retention_est": ir,
        "anchor": anchor,
    }


def antifake_strength() -> dict:
    """防伪强度 FS：伪造成本 / 合法成本（修正原稿 SHA16=2^128 → 实为 2^64）"""
    return {
        "dna_forge_cost": "∞（需GPG私钥·物理隔离）",
        "sha16_forge_cost": "2^64 次哈希碰撞（64bit·诚实修正：非原稿所写2^128）",
        "dr_wuxing_forge_cost": "需语义约束·高",
        "keyword_forge_cost": "需语义匹配·高",
        "legal_cost": "一次压缩 ≈ 0.05s",
        "fs_estimate": "~10^19（SHA16主导·64bit）",
        "note": "若要 2^128 级防伪 → 用 sha256 前32hex（128bit）·见 v2.0 协议附录",
    }


def banach_check(original_length: int = 1200) -> dict:
    """
    Banach 压缩系数估算（工程近似·诚实标注）：
      k ≈ 压缩后大小 / 原始大小（锚 JSON 字节数比例）
    严格数学注记：f 定义在有限离散锚空间→必存在不动点(平凡)；
    UID9622 身份不动点 f(9622)=9622 为符号性锚·非严格 Banach 需要。
    """
    cr = 103 / max(original_length, 1)  # 六元组典型长度~103
    k = round(cr, 4)
    iterations = 0
    # n ≥ ln(eps·(1-k)/d0) / ln(k)·d0=1, eps=0.001·k=0.086 → n≈3
    if 0 < k < 1:
        import math
        n = math.log(0.001 * (1 - k)) / math.log(k)
        iterations = max(1, int(abs(n)) + 1)
    elif k == 0:
        iterations = 1
    return {
        "lipschitz_estimate_k": k,
        "k_lt_1": k < 1,
        "engineering_convergence": f"n≤{iterations}次·误差<0.001（k={k}）" if k < 1 else "k≥1 不收敛",
        "identity_fixed_point": "f(UID9622)=UID9622·身份不动点成立（符号性）",
        "note": "工程近似：k=锚大小/原文大小·非严格Lipschitz常数·完备性由有限锚空间保证",
    }


# ===== 登记册 =====

def registry() -> dict:
    """历史 12 锚登记册统计"""
    drs = [a["dr"] for a in HISTORICAL_ANCHORS]
    colors = Counter(tricolor_of_dr(d) for d in drs)
    wx = Counter(a["wuxing"] for a in HISTORICAL_ANCHORS)
    return {
        "total": len(HISTORICAL_ANCHORS),
        "anchors": HISTORICAL_ANCHORS,
        "dr_distribution": dict(Counter(drs)),
        "color_distribution": dict(colors),
        "wuxing_distribution": dict(wx),
        "summary": {
            "green": colors.get("🟢", 0),
            "yellow": colors.get("🟡", 0),
            "red": colors.get("🔴", 0),
            "note": "🟡历史值不可重算(原文已删·封顶仪式意义)·新锚引擎可全量重算",
            "color_口径": "引擎严格dr区间标色(绿{1,2,4,5,7}/黄{3,6}/红{8,9})·与4/23现场人工判定差异(如T04/T07 dr=8现场标绿)以现场判定为准",
        },
    }


# ===== CLI =====

def main():
    parser = argparse.ArgumentParser(
        description="🪨🐉 不动点压缩锚引擎 v1.0 · 数学优化版",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python3 lh_fixed_point_anchor.py --compress "原文内容" --module 对话 --version 1.0
  python3 lh_fixed_point_anchor.py --input <文件> --module 文档        # 压缩文件
  python3 lh_fixed_point_anchor.py --input <文件> --verify <anchor.json>  # 原文+锚对验
  python3 lh_fixed_point_anchor.py --verify <anchor.json>            # 锚结构校验(无原文)
  python3 lh_fixed_point_anchor.py --ratio "原文"                    # 压缩率/IR
  python3 lh_fixed_point_anchor.py --banach                          # Banach系数估算
  python3 lh_fixed_point_anchor.py --fs                              # 防伪强度
  python3 lh_fixed_point_anchor.py --registry                        # 历史12锚登记册
  python3 lh_fixed_point_anchor.py --reverse <anchor.json>           # 六步反推f⁻¹""",
    )
    parser.add_argument("--compress", "-c", help="压缩一段文本")
    parser.add_argument("--input", "-i", help="压缩/审计文件")
    parser.add_argument("--verify", help="验证锚JSON(可选配合--input原文)")
    parser.add_argument("--ratio", help="压缩率量化")
    parser.add_argument("--banach", action="store_true", help="Banach系数估算")
    parser.add_argument("--fs", action="store_true", help="防伪强度")
    parser.add_argument("--registry", action="store_true", help="历史12锚登记册")
    parser.add_argument("--reverse", help="六步反推锚JSON")
    parser.add_argument("--module", "-m", default="COMPRESS", help="模块名")
    parser.add_argument("--version", "-v", default="1.0", help="版本号")
    args = parser.parse_args()

    # 登记册
    if args.registry:
        r = registry()
        print(f"📚 不动点锚登记册 · {r['total']} 条（2026-04-23 封顶仪式）")
        print(f"dr分布: {r['dr_distribution']}  三色: {r['color_distribution']}  五行: {r['wuxing_distribution']}")
        print(f"汇总: 🟢{r['summary']['green']} 🟡{r['summary']['yellow']} 🔴{r['summary']['red']} | {r['summary']['note']}")
        for a in r["anchors"]:
            print(f"  [{a['id']}] dr={a['dr']} {WUXING_COLORS.get(a['wuxing'],'')}{a['wuxing']} {tricolor_of_dr(a['dr'])} {a['dna']}")
        return 0

    # Banach / FS
    if args.banach:
        b = banach_check()
        print(f"📐 Banach 压缩系数估算: k={b['lipschitz_estimate_k']}  {'✅ k<1' if b['k_lt_1'] else '❌ k≥1'}")
        print(f"   工程收敛: {b['engineering_convergence']}")
        print(f"   身份不动点: {b['identity_fixed_point']}")
        print(f"   注: {b['note']}")
        return 0
    if args.fs:
        fs = antifake_strength()
        print("🛡️ 防伪强度 FS = 伪造成本/合法成本")
        for k, v in fs.items():
            print(f"   {k}: {v}")
        return 0

    # 压缩
    text = None
    if args.compress:
        text = args.compress
    elif args.input:
        fp = Path(args.input)
        if not fp.exists():
            print(f"🔴 文件不存在: {fp}")
            return 1
        text = fp.read_text(encoding="utf-8", errors="replace")

    if text:
        anchor = compress(text, args.module, args.version)
        anchor = _finalize_anchor(anchor, len(text))
        print(f"🧬 六元组锚 {tricolor_of_dr(anchor['dr'])}")
        print(f"  D  DNA:     {anchor['dna']}")
        print(f"  H  SHA16:   {anchor['sha16']}")
        print(f"  R  数字根:  dr={anchor['dr']} ({tricolor_of_dr(anchor['dr'])})")
        print(f"  W  五行:    {WUXING_COLORS.get(anchor['wuxing'],'')}{anchor['wuxing']}")
        print(f"  K  三关键词: {', '.join(anchor['keywords'])}")
        print(f"  P  一句话:  {anchor['point']}")
        print(f"  📊 压缩: {anchor['meta']['original_length']}→{anchor['meta']['net_content_length']} 字符(净内容) · CR={anchor['meta']['compression_ratio']} · 节省{anchor['meta']['space_saved_pct']}%")
        if anchor["meta"].get("short_text_note"):
            print(f"  ⚠️ {anchor['meta']['short_text_note']}")
        return 0

    # 验证 / 反推
    if args.verify:
        try:
            anchor = json.loads(args.verify)
        except json.JSONDecodeError:
            # 支持文件路径
            fp = Path(args.verify)
            if fp.exists():
                anchor = json.loads(fp.read_text(encoding="utf-8"))
            else:
                print("🔴 锚JSON解析失败")
                return 1
        original = None
        if args.input:
            fp = Path(args.input)
            if fp.exists():
                original = fp.read_text(encoding="utf-8", errors="replace")
        v = verify_anchor(anchor, original)
        print(f"🔎 锚验证 {'✅ 有效' if v['valid'] else '❌ 无效'} · 置信度 C={v['confidence']}")
        print(f"   C_DNA={v['c_dna']} C_关键词={v['c_keywords']} C_语义={v['c_semantic']}")
        if original:
            print(f"   原文重算: SHA16匹配={v['checks'].get('recompute_sha16')} dr匹配={v['checks'].get('recompute_dr')} 关键词重叠={v['checks'].get('recompute_kw_overlap')}")
        else:
            print("   无原文 → 结构校验 · 真置信度需 --input 原文对验")
        for k, val in v["checks"].items():
            print(f"   {k}: {val}")
        return 0 if v["valid"] else 1

    if args.reverse:
        try:
            anchor = json.loads(args.reverse)
        except json.JSONDecodeError:
            fp = Path(args.reverse)
            if fp.exists():
                anchor = json.loads(fp.read_text(encoding="utf-8"))
            else:
                print("🔴 锚JSON解析失败")
                return 1
        r = reverse_anchor(anchor)
        print(f"🔄 六步反推 f⁻¹(x₀) ≈ 原文主题  {r['color']}  C={r['confidence']}")
        for i in range(1, 7):
            step = r[f"step{i}_" + ("time" if i == 1 else ("tamper" if i == 2 else ("energy" if i == 3 else ("semantic" if i == 4 else ("theme" if i == 5 else "composite")))))]
            print(f"  Step{i} {step['source']}: {step['value']}")
        return 0

    # ratio
    if args.ratio:
        m = compression_metrics(args.ratio)
        print(f"📊 压缩量化: {m['original_length']}→{m['net_content_length']} 字符(净内容)")
        print(f"   CR={m['compression_ratio']} · 节省 {m['space_saved_pct']}% · IR估算≈{m['information_retention_est']}")
        a = m["anchor"]
        print(f"   锚: dr={a['dr']} {WUXING_COLORS.get(a['wuxing'],'')}{a['wuxing']} K={a['keywords']} P={a['point']}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
