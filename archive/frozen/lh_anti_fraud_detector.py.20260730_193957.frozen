#!/usr/bin/env python3
"""
龍魂·行為密碼學反詐檢測引擎 v1.0
DNA: #龍芯⚡️丙午·癸未·丁未·☰乾-ANTI-FRAUD-DETECTOR-v1.0-彎彎繞繞-3a7d1e5f
創建者: 諸葛鑫（UID9622）
用途: 文字彎彎繞繞檢測·綜合風險評分·反制話術生成
依賴: anti_fraud_patterns_v3.0.json
"""

import json
import re
import sys
import os
import argparse
from typing import Dict, List, Tuple, Optional

# 路徑
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERNS_PATH = os.path.join(BASE_DIR, "data", "anti_fraud_patterns_v3.0.json")

# 繁簡歸一化表（常用字）
TRAD_TO_SIMP = str.maketrans({
    '為': '为', '說': '说', '廣': '广', '體': '体', '會': '会',
    '對': '对', '沒': '没', '時': '时', '個': '个', '們': '们',
    '開': '开', '關': '关', '來': '来', '後': '后', '過': '过',
    '還': '还', '讓': '让', '請': '请', '買': '买', '賣': '卖',
    '錢': '钱', '價': '价', '號': '号', '碼': '码', '報': '报',
    '網': '网', '鏈': '链', '證': '证', '實': '实', '驗': '验',
    '據': '据', '講': '讲', '聽': '听', '試': '试', '給': '给',
    '從': '从', '錯': '错', '難': '难', '機': '机', '幫': '帮',
    '嗎': '吗', '認': '认', '應': '应', '該': '该', '於': '于',
    '與': '与', '並': '并', '關': '关', '係': '系', '製': '制',
    '複': '复', '術': '术', '療': '疗', '藥': '药', '醫': '医',
    '養': '养', '護': '护', '膚': '肤', '髮': '发', '電': '电',
    '視': '视', '頻': '频', '節': '节', '點': '点', '質': '质',
    '測': '测', '檢': '检', '儀': '仪', '數': '数', '學': '学',
    '專': '专', '業': '业', '際': '际', '際': '际', '壞': '坏',
    '標': '标', '準': '准', '確': '确', '認': '认', '誤': '误',
    '導': '导', '轉': '转', '擇': '择', '極': '极', '變': '变',
    '鬥': '斗', '爭': '争', '掃': '扫', '騙': '骗', '詐': '诈',
    '贊': '赞', '贏': '赢', '棄': '弃', '衝': '冲', '壓': '压',
    '險': '险', '鐵': '铁', '獨': '独', '處': '处', '處': '处',
    '樣': '样', '陽': '阳', '離': '离', '發': '发', '經': '经',
    '傳': '传', '統': '统', '監': '监', '錄': '录', '查': '查',
    '規': '规', '則': '则', '範': '范', '圍': '围', '級': '级',
    '絕': '绝', '證': '证', '據': '据', '議': '议', '覺': '觉',
    '現': '现', '當': '当', '長': '长', '張': '张', '場': '场',
    '萬': '万', '東': '东', '風': '风', '動': '动', '勞': '劳',
    '單': '单', '戰': '战', '戲': '戏', '劃': '划', '劃': '划',
    '參': '参', '雙': '双', '營': '营', '銷': '销', '薦': '荐',
    '競': '竞', '況': '况', '資': '资', '幣': '币', '賬': '账',
    '進': '进', '還': '还', '選': '选', '連': '连', '餘': '余',
    '優': '优', '豐': '丰', '終': '终', '總': '总', '統': '统',
    '線': '线', '組': '组', '結': '结', '構': '构', '態': '态',
})


def normalize_text(text: str) -> str:
    """繁簡歸一化 + 全角半角歸一化"""
    # 繁體→簡體
    text = text.translate(TRAD_TO_SIMP)
    # 全角英數字→半角
    result = []
    for ch in text:
        code = ord(ch)
        if code == 0x3000:  # 全角空格
            result.append(' ')
        elif 0xFF01 <= code <= 0xFF5E:
            result.append(chr(code - 0xFEE0))
        else:
            result.append(ch)
    return ''.join(result)

# 權重矩陣 (對應協議中的14維度)
DIMENSION_WEIGHTS = {
    "A_urgency_manufacturing": 0.10,
    "B_fear_exploitation": 0.08,
    "C_social_proof_forgery": 0.04,
    "D_authority_impersonation": 0.15,
    "E_exclusivity_scarcity": 0.05,
    "F_emotional_binding": 0.08,
    "G_data_theft": 0.12,
    "H_progressive_commitment": 0.06,
    "I_indirect_evasion": 0.08,
    "J_exaggerated_science": 0.07,
    "K_douyin_live_patterns": 0.05,
    "L_business_intent_disguise": 0.05,
    "M_false_experiments": 0.04,
    "N_narrative_control": 0.03,
}

# 必紅燈信號（出現即🔴）
# 格式: (關鍵詞列表, 標籤, 最少匹配數, 單個觸發)
HARD_RED_RULES = [
    (["公安局", "法院", "檢察院", "安全賬戶", "配合調查", "通緝令"], "冒充公檢法", 1, True),
    (["屏幕共享", "共享屏幕"], "屏幕共享+金錢", 1, True),
    (["不是廣告", "純分享", "無廣", "不是推銷"], "『不是廣告』後有推薦", 1, True),
    (["順便推薦", "順便說一下", "順便提", "順便給"], "彎彎繞繞-順便", 1, True),
    (["帶你賺錢", "帶你飛", "跟著我做", "複製我的成功"], "帶賺錢+收費", 1, True),
    (["不用想", "信我就完了", "猶豫就會敗北", "多想無益"], "認知閉合控制", 1, True),
    (["僅剩", "倒計時", "馬上售罄", "庫存告急"], "緊迫感催促", 2, False),
    (["家人們"], "家人稱呼+促銷", 1, True),
    (["原價", "現價", "折扣"], "價格造假", 2, False),
]

# 彎彎繞繞關鍵詞
WINDING_KEYWORDS = {
    "trust_building": ["我為你好", "關心你", "好久不見", "想你", "最近怎麼樣", "注意身體"],
    "target_jump": ["順便", "對了", "其實還有一個", "順便說一下", "說起來"],
    "question_evasion": ["你說呢", "你覺得呢", "你想想看", "你自己琢磨", "這還用說嗎", "你懂我的意思嗎"],
    "vague_words": ["可能", "或許", "大概率", "一般來說", "據了解", "有人說", "據說", "號稱", "大概", "應該"],
    "story_hooks": ["我一個朋友", "我認識一個人", "我自己試過", "我原來也不信", "親身經歷", "真實故事"],
    "not_ad": ["不是廣告", "純分享", "無廣", "不是推銷", "自用分享", "真心推薦"],
    "family_terms": ["家人們", "姐妹們", "兄弟們", "老鐵", "自己人", "一家人"],
    "urgency": ["限時", "倒計時", "最後", "錯過", "只剩", "馬上結束", "今天截止"],
    "cognitive_close": ["不用想", "信我就完了", "猶豫就會敗北", "多想無益"],
}

# 偽科學實驗關鍵詞
SCIENCE_FAKE_KEYWORDS = {
    "dissolve": ["溶解", "化開", "放進水裡", "對比一下"],
    "ph_test": ["pH", "酸鹼", "試紙", "變色", "鹼性", "酸性體質"],
    "iodine": ["碘伏", "褪色", "變透明", "抗氧化", "自由基"],
    "penetration": ["滲透", "真皮層", "分子小", "深層吸收"],
    "magnetic": ["磁場", "能量", "頻率", "共振", "量子", "遠紅外", "負離子", "太赫茲", "生物電"],
    "experience": ["你感受一下", "是不是發熱了", "有感覺了對不對", "麻麻的", "這就對了"],
    "detection": ["檢測儀", "亞健康", "微循環", "一滴血", "毒素檢測", "重金屬超標"],
}


def load_patterns() -> Dict:
    """加載反詐模式庫（含繁簡歸一化）"""
    try:
        with open(PATTERNS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 歸一化所有關鍵詞
        for cat_key, cat_data in data.get("categories", {}).items():
            for p in cat_data.get("patterns", []):
                p["keywords"] = [normalize_text(kw) for kw in p.get("keywords", [])]
        return data
    except FileNotFoundError:
        print(f"⚠️ 模式庫未找到: {PATTERNS_PATH}")
        return {}


def compute_winding_index(text: str) -> Dict:
    """計算彎繞指數 (Winding Index)"""
    text = normalize_text(text)
    total_chars = len(text)
    if total_chars == 0:
        return {"wi": 0, "level": "🟢", "details": {}}

    # 1. 信息密度比 IDR — 核心意圖詞在全文的分佈密度
    intent_words = ["推荐", "买", "卖", "价格", "多少钱", "报名", "下单", "链接", "加微信", "联系",
                    "推薦", "買", "賣", "價格", "多少錢", "報名", "下單", "鏈接", "加微信", "聯繫"]
    core_chars = sum(len(m.group()) for w in intent_words
                     for m in re.finditer(re.escape(w), text))
    # 高密度=信息直接。總字數越少+核心詞越多→密度越高
    idr = min(core_chars / max(total_chars, 1) * 3.0, 1.0)  # 3x放大因核心詞較少

    # 2. 目標跳躍次數 TJR
    tj_keywords_norm = [normalize_text(kw) for kw in WINDING_KEYWORDS["target_jump"]]
    tj_count = sum(len(re.findall(re.escape(kw), text))
                   for kw in tj_keywords_norm)
    tjr = min(tj_count / 5.0, 1.0)

    # 3. 關鍵詞迂迴度 KWR - 關鍵詞首次出現位置
    first_intent = total_chars
    for w in intent_words:
        m = re.search(re.escape(w), text)
        if m and m.start() < first_intent:
            first_intent = m.start()
    kwr = (first_intent / total_chars) if first_intent < total_chars else 1.0

    # 4. 反問反製度 QER
    qe_keywords = [normalize_text(kw) for kw in WINDING_KEYWORDS["question_evasion"]]
    qe_count = sum(len(re.findall(re.escape(kw), text))
                   for kw in qe_keywords)
    sentences = len(re.split(r'[。！？!?\n]', text))
    qer = min(qe_count / max(sentences, 1), 1.0)

    # 5. 模糊主語率 VAR
    vague_keywords = [normalize_text(kw) for kw in WINDING_KEYWORDS["vague_words"]]
    vague_count = sum(len(re.findall(re.escape(kw), text))
                      for kw in vague_keywords)
    var = min(vague_count / max(sentences, 1), 1.0)

    # 加權計算 WI
    # IDR高=信息直接→彎繞低→(1-IDR)反轉
    wi = 0.30 * (1 - idr) + 0.20 * tjr + 0.25 * kwr + 0.15 * qer + 0.10 * var
    wi = max(0.0, min(wi, 1.0))  # clamp

    if wi < 0.25:
        level = "🟢"
    elif wi < 0.50:
        level = "🟡"
    elif wi < 0.75:
        level = "🟠"
    else:
        level = "🔴"

    return {
        "wi": round(wi, 3),
        "level": level,
        "details": {
            "idr": round(idr, 3),
            "tjr": round(tjr, 3),
            "kwr": round(kwr, 3),
            "qer": round(qer, 3),
            "var": round(var, 3),
        }
    }


def check_hard_rules(text: str) -> List[Dict]:
    """檢查必紅燈規則"""
    text = normalize_text(text)
    triggered = []
    for keywords, label, min_matches, single_trigger in HARD_RED_RULES:
        keywords_norm = [normalize_text(kw) for kw in keywords]
        matched = [kw for kw in keywords_norm if kw in text]
        if single_trigger and len(matched) >= 1:
            # 單個即可觸發
            triggered.append({"rule": label, "matched": matched, "level": "🔴"})
        elif len(matched) >= min_matches:
            triggered.append({"rule": label, "matched": matched, "level": "🔴"})
    return triggered


def compute_risk_score(text: str, patterns: Dict) -> Dict:
    """計算綜合風險評分 (CRS)"""
    text = normalize_text(text)
    triggered_dimensions = {}

    categories = patterns.get("categories", {})
    for dim_key, dim_data in categories.items():
        dim_patterns = dim_data.get("patterns", [])
        matched_keywords = []
        max_severity = 0.0

        for p in dim_patterns:
            p_keywords = p.get("keywords", [])
            # 統計匹配數
            hits = sum(1 for kw in p_keywords if kw in text)
            # 高風險維度(I/D/J/N)閾值降低為1，其他維度為2
            min_hits = 1 if dim_key[0] in "IDJNGLM" else 2
            if hits >= min_hits:
                matched_keywords.extend([kw for kw in p_keywords if kw in text])
                severity = min(hits / max(len(p_keywords), 1) + 0.1, 1.0)
                max_severity = max(max_severity, severity)

        if matched_keywords:
            triggered_dimensions[dim_key] = {
                "matched": list(set(matched_keywords)),
                "severity": round(max_severity, 3),
                "name": dim_data.get("name", dim_key),
            }

    # 加權計算 CRS
    crs = 0.0
    for dim_key, info in triggered_dimensions.items():
        weight = DIMENSION_WEIGHTS.get(dim_key, 0.03)
        crs += weight * info["severity"]

    crs = round(min(crs, 1.0), 3)

    if crs < 0.20:
        level = "🟢 低風險"
    elif crs < 0.40:
        level = "🟡 中風險，謹慎"
    elif crs < 0.65:
        level = "🟠 高風險，建議拒絕"
    else:
        level = "🔴 極高風險，立即拒絕+舉報"

    return {
        "crs": crs,
        "level": level,
        "triggered_dimensions": triggered_dimensions,
    }


def generate_counter(text: str, patterns: Dict) -> List[str]:
    """生成反制話術"""
    text = normalize_text(text)
    counters = []
    dim_triggers = {}

    categories = patterns.get("categories", {})
    for dim_key, dim_data in categories.items():
        for p in dim_data.get("patterns", []):
            hits = sum(1 for kw in p.get("keywords", []) if kw in text)
            if hits >= 2 and p.get("counter"):
                dim_triggers[dim_key] = p

    # 按風險等級排序
    priority_order = ["D", "G", "I", "J", "K", "L", "N", "A", "B", "F", "M", "C", "E", "H"]
    sorted_triggers = sorted(
        dim_triggers.items(),
        key=lambda x: priority_order.index(x[0][0]) if x[0][0] in priority_order else 99
    )

    for _, p in sorted_triggers:
        c = p.get("counter", "")
        if c and c not in counters:
            counters.append(c)

    # 默認反制
    if not counters:
        counters = [
            "你直接說，到底想幹嘛？",
            "不用繞彎子，直接說重點。",
            "我就問一個問題：你要賺我多少錢？",
        ]

    return counters[:5]


def analyze(text: str, context: str = "general") -> Dict:
    """完整分析"""
    patterns = load_patterns()

    # 必紅燈檢查
    hard_rules = check_hard_rules(text)

    # 彎繞指數
    winding = compute_winding_index(text)

    # 綜合風險評分
    risk = compute_risk_score(text, patterns) if patterns else {"crs": 0, "level": "🟢", "triggered_dimensions": {}}

    # 如果硬紅燈觸發，覆蓋風險等級
    if hard_rules:
        risk["level"] = "🔴 極高風險（硬紅燈觸發）"
        risk["crs"] = max(risk["crs"], 0.80)

    # 反制話術
    counters = generate_counter(text, patterns) if patterns else []

    # 綜合判定
    if hard_rules:
        final_level = "🔴"
        final_advice = "立即拒絕。已觸發必紅燈信號。"
    elif winding["wi"] >= 0.75 or risk["crs"] >= 0.65:
        final_level = "🔴"
        final_advice = "高度可疑，建議拒絕。彎繞指數和風險評分均達紅線。"
    elif winding["wi"] >= 0.50 or risk["crs"] >= 0.40:
        final_level = "🟠"
        final_advice = "較可疑，請謹慎對待。不要急著做決定。"
    elif winding["wi"] >= 0.25 or risk["crs"] >= 0.20:
        final_level = "🟡"
        final_advice = "有些可疑信號，保持警惕。可以再觀察看看。"
    else:
        final_level = "🟢"
        final_advice = "表達直接、信息清晰，風險較低。"

    return {
        "text": text[:200] + ("..." if len(text) > 200 else ""),
        "context": context,
        "final_level": final_level,
        "final_advice": final_advice,
        "winding_index": winding,
        "risk_score": risk,
        "hard_rules_triggered": hard_rules,
        "counter_suggestions": counters,
        "analysis_time": "",
    }


def main():
    parser = argparse.ArgumentParser(description="龍魂·行為密碼學反詐檢測引擎")
    sub = parser.add_subparsers(dest="command", help="子命令")

    # wind — 彎繞指數
    p_wind = sub.add_parser("wind", help="計算彎彎繞繞指數")
    p_wind.add_argument("--text", "-t", required=True, help="要分析的文字")
    p_wind.add_argument("--context", "-c", default="general", help="場景: general/douyin_live/wechat/ad")

    # score — 綜合風險評分
    p_score = sub.add_parser("score", help="綜合風險評分")
    p_score.add_argument("--text", "-t", required=True, help="要分析的文字")
    p_score.add_argument("--context", "-c", default="general", help="場景")

    # analyze — 完整分析
    p_analyze = sub.add_parser("analyze", help="完整分析（默認）")
    p_analyze.add_argument("--text", "-t", required=True, help="要分析的文字")
    p_analyze.add_argument("--context", "-c", default="general", help="場景")
    p_analyze.add_argument("--json", "-j", action="store_true", help="JSON輸出")

    # counter — 生成反制話術
    p_counter = sub.add_parser("counter", help="生成反制話術")
    p_counter.add_argument("--text", "-t", required=True, help="對方的話術")

    # batch — 批量檢測
    p_batch = sub.add_parser("batch", help="批量檢測（每行一條）")
    p_batch.add_argument("--file", "-f", required=True, help="文件路徑")

    args = parser.parse_args()

    if args.command in ("wind",):
        result = compute_winding_index(args.text)
        print(f"\n═══ 彎彎繞繞指數 ═══")
        print(f"WI: {result['wi']} | 等級: {result['level']}")
        print(f"信息密度比(IDR): {result['details']['idr']} | 目標跳躍(TJR): {result['details']['tjr']}")
        print(f"關鍵詞迂迴(KWR): {result['details']['kwr']} | 反問反製(QER): {result['details']['qer']}")
        print(f"模糊主語率(VAR): {result['details']['var']}")
        if result['wi'] >= 0.5:
            print("⚠️ 高度彎繞！這人說話有問題。")
        elif result['wi'] >= 0.25:
            print("⚡ 有些繞，保持警惕。")

    elif args.command in ("score",):
        patterns = load_patterns()
        result = compute_risk_score(args.text, patterns)
        print(f"\n═══ 綜合風險評分 ═══")
        print(f"CRS: {result['crs']} | 等級: {result['level']}")
        if result['triggered_dimensions']:
            print(f"\n觸發維度 ({len(result['triggered_dimensions'])}個):")
            for dim, info in result['triggered_dimensions'].items():
                kw_str = "、".join(info['matched'][:5])
                print(f"  {dim} [{info['name']}] → {kw_str}")

    elif args.command in ("analyze", None):
        from datetime import datetime
        result = analyze(args.text, args.context)
        result["analysis_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n╔══════════════════════════════════╗")
            print(f"║  龍魂·彎彎繞繞反詐檢測引擎 v1.0   ║")
            print(f"╚══════════════════════════════════╝")
            print(f"\n【分析文字】{result['text']}")
            print(f"\n【綜合判定】{result['final_level']} {result['final_advice']}")
            print(f"\n── 彎繞指數 ──")
            w = result['winding_index']
            print(f"  WI: {w['wi']} ({w['level']})")
            print(f"  信息密度:{w['details']['idr']} | 跳躍:{w['details']['tjr']} | 迂迴:{w['details']['kwr']}")
            print(f"  反問:{w['details']['qer']} | 模糊:{w['details']['var']}")
            print(f"\n── 風險評分 ──")
            r = result['risk_score']
            print(f"  CRS: {r['crs']} | {r['level']}")
            if r.get('triggered_dimensions'):
                for dim, info in r['triggered_dimensions'].items():
                    print(f"  → {info['name']}: {', '.join(info['matched'][:3])}")

            if result['hard_rules_triggered']:
                print(f"\n── 🔴 必紅燈觸發 ──")
                for hr in result['hard_rules_triggered']:
                    print(f"  {hr['rule']}: {', '.join(hr['matched'][:3])}")

            if result['counter_suggestions']:
                print(f"\n── 💬 建議反制話術 ──")
                for i, c in enumerate(result['counter_suggestions'], 1):
                    print(f"  {i}. {c}")

    elif args.command == "counter":
        patterns = load_patterns()
        counters = generate_counter(args.text, patterns)
        print(f"\n═══ 反制話術建議 ═══")
        for i, c in enumerate(counters, 1):
            print(f"  {i}. {c}")

    elif args.command == "batch":
        if not os.path.exists(args.file):
            print(f"❌ 文件不存在: {args.file}")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]

        results = []
        for line in lines:
            r = analyze(line, "batch")
            results.append({
                "text": line[:60],
                "level": r["final_level"],
                "wi": r["winding_index"]["wi"],
                "crs": r["risk_score"]["crs"],
                "hard": bool(r["hard_rules_triggered"]),
            })

        # 統計
        reds = [r for r in results if r["level"] == "🔴"]
        oranges = [r for r in results if r["level"] == "🟠"]
        yellows = [r for r in results if r["level"] == "🟡"]
        greens = [r for r in results if r["level"] == "🟢"]

        print(f"\n═══ 批量檢測報告 ═══")
        print(f"總計: {len(results)} 條")
        print(f"🔴 高風險: {len(reds)} | 🟠 可疑: {len(oranges)} | 🟡 警惕: {len(yellows)} | 🟢 正常: {len(greens)}")

        if reds:
            print(f"\n── 🔴 高風險條目 ──")
            for r in reds:
                hw = " [硬紅燈!]" if r["hard"] else ""
                print(f"  WI={r['wi']} CRS={r['crs']}{hw}: {r['text']}")

        if oranges:
            print(f"\n── 🟠 可疑條目 ──")
            for r in oranges[:10]:
                print(f"  WI={r['wi']}: {r['text']}")


if __name__ == "__main__":
    main()
