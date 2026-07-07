#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍智守 — 龍魂生活/办公智能守护入口
功能：
  - 链接安全预审（域名、短链、HTTP、敏感词）
  - 反诈/话术风险识别
  - 国学易经起卦、三六九数字根、三色状态
  - 将审核结果以飞书卡片形式发回群内
调用：
  python3 龍智守.py --input "帮我看看这个链接 https://xxx.com"
  python3 龍智守.py --input "今天运势如何" --send
DNA: #龍芯⚡️20260630-LONGZHI-SHOU-v1
"""

# 龙智守飞书卡片全局确认码（焊死）
_CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

import argparse
import datetime
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import feishu_bot

try:
    import 龍魂DNA審計門戶 as _dna_portal
except Exception:
    _dna_portal = None

# DeepSeek 底座客户端（可选加载）
_DEEPSEEK_DIR = Path.home() / "longhun-system" / "integrations" / "deepseek"
if str(_DEEPSEEK_DIR) not in sys.path:
    sys.path.insert(0, str(_DEEPSEEK_DIR))
try:
    from deepseek_client import DeepSeekClient  # type: ignore[import-untyped]
    _deepseek_client: Any | None = None
except Exception:
    DeepSeekClient = None  # type: ignore[misc, assignment]
    _deepseek_client = None


def _get_deepseek_client() -> Any | None:
    """懒加载 DeepSeek 客户端，未配置 Key 则返回 None。"""
    global _deepseek_client
    if DeepSeekClient is None:
        return None
    if _deepseek_client is None:
        try:
            _deepseek_client = DeepSeekClient()
        except Exception:
            _deepseek_client = None
    return _deepseek_client

# ============================================================
# 反詐 / 營銷套路庫加載
# ============================================================
_套路庫路徑 = Path.home() / "longhun-system" / "data" / "反诈套路库.json"
_套路日誌路徑 = Path.home() / "longhun-system" / "logs" / "龍智守_套路识别日志.jsonl"


def _加載套路庫() -> dict[str, Any]:
    if not _套路庫路徑.exists():
        return {"patterns": []}
    try:
        return json.loads(_套路庫路徑.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"🟡 加載套路庫失敗: {e}", file=sys.stderr)
        return {"patterns": []}


_套路庫 = _加載套路庫()


# ============================================================
# 64 卦（文王序）+ 一爻点睛
# ============================================================
_六十四卦 = {
    1: ("乾為天", "天行健，君子以自強不息。"),
    2: ("坤為地", "地勢坤，君子以厚德載物。"),
    3: ("水雷屯", "雲雷，君子以經綸。勿用有攸往，利建侯。"),
    4: ("山水蒙", "山下出泉，蒙；君子以果行育德。"),
    5: ("水天需", "雲上於天，需；君子以飲食宴樂。"),
    6: ("天水訟", "天與水違行，訟；君子以作事謀始。"),
    7: ("地水師", "地中有水，師；君子以容民畜眾。"),
    8: ("水地比", "地上有水，比；先王以建萬國，親諸侯。"),
    9: ("風天小畜", "風行天上，小畜；君子以懿文德。"),
    10: ("天澤履", "上天下澤，履；君子以辨上下，定民志。"),
    11: ("地天泰", "天地交，泰；后以財成天地之道。"),
    12: ("天地否", "天地不交，否；君子以儉德辟難。"),
    13: ("天火同人", "天與火，同人；君子以類族辨物。"),
    14: ("火天大有", "火在天上，大有；君子以遏惡揚善。"),
    15: ("地山謙", "地中有山，謙；君子以裒多益寡。"),
    16: ("雷地豫", "雷出地奮，豫；先王以作樂崇德。"),
    17: ("澤雷隨", "澤中有雷，隨；君子以嚮晦入宴息。"),
    18: ("山風蠱", "山下有風，蠱；君子以振民育德。"),
    19: ("地澤臨", "澤上有地，臨；君子以教思無窮。"),
    20: ("風地觀", "風行地上，觀；先王以省方觀民設教。"),
    21: ("火雷噬嗑", "雷電，噬嗑；先王以明罰敕法。"),
    22: ("山火賁", "山下有火，賁；君子以明庶政，無敢折獄。"),
    23: ("山地剝", "山附於地，剝；上以厚下安宅。"),
    24: ("地雷復", "雷在地中，復；先王以至日閉關。"),
    25: ("天雷無妄", "天下雷行，物與無妄；先王以茂對時育萬物。"),
    26: ("山天大畜", "天在山中，大畜；君子以多識前言往行。"),
    27: ("山雷頤", "山下有雷，頤；君子以慎言語，節飲食。"),
    28: ("澤風大過", "澤滅木，大過；君子以獨立不懼，遯世無悶。"),
    29: ("坎為水", "水洊至，習坎；君子以常德行，習教事。"),
    30: ("離為火", "明兩作，離；大人以繼明照於四方。"),
    31: ("澤山咸", "山上有澤，咸；君子以虛受人。"),
    32: ("雷風恆", "雷風，恆；君子以立不易方。"),
    33: ("天山遯", "天下有山，遯；君子以遠小人，不惡而嚴。"),
    34: ("雷天大壯", "雷在天上，大壯；君子以非禮弗履。"),
    35: ("火地晉", "明出地上，晉；君子以自昭明德。"),
    36: ("地火明夷", "明入地中，明夷；君子以蒞眾，用晦而明。"),
    37: ("風火家人", "風自火出，家人；君子以言有物而行有恆。"),
    38: ("火澤睽", "上火下澤，睽；君子以同而異。"),
    39: ("水山蹇", "山上有水，蹇；君子以反身修德。"),
    40: ("雷水解", "雷雨作，解；君子以赦過宥罪。"),
    41: ("山澤損", "山下有澤，損；君子以懲忿窒慾。"),
    42: ("風雷益", "風雷，益；君子以見善則遷，有過則改。"),
    43: ("澤天夬", "澤上於天，夬；君子以施祿及下。"),
    44: ("天風姤", "天下有風，姤；后以施命誥四方。"),
    45: ("澤地萃", "澤上於地，萃；君子以除戎器，戒不虞。"),
    46: ("地風升", "地中生木，升；君子以順德，積小以高大。"),
    47: ("澤水困", "澤無水，困；君子以致命遂志。"),
    48: ("水風井", "木上有水，井；君子以勞民勸相。"),
    49: ("澤火革", "澤中有火，革；君子以治曆明時。"),
    50: ("火風鼎", "木上有火，鼎；君子以正位凝命。"),
    51: ("震為雷", "洊雷，震；君子以恐懼修省。"),
    52: ("艮為山", "兼山，艮；君子以思不出其位。"),
    53: ("風山漸", "山上有木，漸；君子以居賢德善俗。"),
    54: ("雷澤歸妹", "澤上有雷，歸妹；君子以永終知敝。"),
    55: ("雷火豐", "雷電皆至，豐；君子以折獄致刑。"),
    56: ("火山旅", "山上有火，旅；君子以明慎用刑。"),
    57: ("巽為風", "隨風，巽；君子以申命行事。"),
    58: ("兌為澤", "麗澤，兌；君子以朋友講習。"),
    59: ("風水渙", "風行水上，渙；先王以享于帝立廟。"),
    60: ("水澤節", "澤上有水，節；君子以制數度，議德行。"),
    61: ("風澤中孚", "澤上有風，中孚；君子以議獄緩死。"),
    62: ("雷山小過", "山上有雷，小過；君子以行過乎恭。"),
    63: ("水火既濟", "水在火上，既濟；君子以思患而豫防之。"),
    64: ("火水未濟", "火在水上，未濟；君子以慎辨物居方。"),
}

# ============================================================
# 风险规则库
# ============================================================
_诈骗关键词 = [
    "轉賬", "轉帐", "汇款", "匯款", "驗證碼", "验证码", "刷單", "刷单",
    "安全賬戶", "安全账户", "限時", "限时", "點擊鏈接", "点击链接",
    "退款", "中獎", "中奖", "領取", "领取", "保證金", "保证金",
    "凍結", "冻结", "涉嫌", "違法", "违法", "公安", "法院", "起訴",
]

_高風險域名 = ["tk", "ml", "ga", "cf", "gq", "top", "xyz", "club", "click"]


def _extract_urls(text: str) -> list[str]:
    return re.findall(r"https?://[^\s\u3000\n\r]+", text)


def _check_url(url: str) -> dict[str, Any]:
    result = {
        "url": url,
        "domain": "",
        "https": url.startswith("https://"),
        "is_ip": False,
        "shortlink": False,
        "suspicious_tld": False,
        "title": "",
        "redirects": False,
        "risk": "🟢 低風險",
        "reasons": [],
    }
    try:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.split(":")[0]
        result["domain"] = domain
        if re.match(r"^\d+\.\d+\.\d+\.\d+$", domain):
            result["is_ip"] = True
            result["reasons"].append("IP 直連地址")
        tld = domain.split(".")[-1].lower() if "." in domain else ""
        if tld in _高風險域名:
            result["suspicious_tld"] = True
            result["reasons"].append(f"可疑頂級域名 .{tld}")
        if len(domain) <= 10 and domain.count(".") >= 1 and tld:
            result["shortlink"] = True
            result["reasons"].append("疑似短鏈接")
        if not result["https"]:
            result["reasons"].append("未使用 HTTPS")

        # 嘗試獲取標題與重定向
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (龍智守)"},
                method="HEAD",
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                final = resp.geturl()
                if final != url:
                    result["redirects"] = True
                    result["reasons"].append(f"發生跳轉到 {final}")
        except Exception:
            pass
    except Exception as e:
        result["reasons"].append(f"解析異常: {e}")

    if result["is_ip"] or (result["shortlink"] and not result["https"]) or result["suspicious_tld"]:
        result["risk"] = "🔴 高風險"
    elif result["shortlink"] or result["redirects"] or not result["https"]:
        result["risk"] = "🟡 中風險"
    return result


def _識別套路(text: str) -> list[dict[str, Any]]:
    """命中反詐/營銷套路庫，返回命中的套路列表。"""
    matched = []
    for p in _套路庫.get("patterns", []):
        if any(kw in text for kw in p.get("keywords", [])):
            matched.append({
                "id": p["id"],
                "name": p["name"],
                "category": p["category"],
                "risk_level": p["risk_level"],
                "description": p["description"],
                "counter_measure": p["counter_measure"],
            })
    return matched


def _check_text(text: str) -> dict[str, Any]:
    hits = [kw for kw in _诈骗关键词 if kw in text]
    patterns = _識別套路(text)
    # 綜合風險：命中高風險套路或 3+ 關鍵詞 = 高風險
    has_high_risk_pattern = any(p["risk_level"] == "高" and p["category"] == "詐騙" for p in patterns)
    if has_high_risk_pattern or len(hits) >= 3:
        risk = "🔴 高風險"
    elif patterns or hits:
        risk = "🟡 中風險"
    else:
        risk = "🟢 低風險"
    return {"hits": hits, "patterns": patterns, "risk": risk}


def _digital_root(n: int) -> int:
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def _起卦(seed_text: str) -> dict[str, Any]:
    seed = f"{seed_text}-{time.time_ns()}"
    h = hashlib.sha256(seed.encode()).hexdigest()
    rng = random.Random(h)
    # 六爻
    yaos = [rng.choice([6, 7, 8, 9]) for _ in range(6)]
    # 簡化起卦：以六爻和映射 1-64
    idx = (sum(yaos) % 64) or 64
    name, meaning = _六十四卦[idx]
    dr = _digital_root(sum(yaos))
    color = "red" if dr in (3, 7) else ("orange" if dr in (2, 6, 8) else "green")
    return {
        "卦名": name,
        "卦序": idx,
        "爻": yaos,
        "數字根": dr,
        "釋義": meaning,
        "color": color,
    }


# ============================================================
# 多角色白話解釋
# ============================================================

_角色說明 = {
    "普通人": "用生活裡的大白話講清楚",
    "醫生": "用醫療/專業場景類比",
    "教師": "用教學、備課、家校溝通場景講",
    "學生": "用學生聽得懂的例子",
    "老人": "慢一點、具體一點，像跟長輩聊天",
    "工人/農民": "用幹活、種地、做工的經驗比喻",
}

_角色別名 = {
    "医生": "醫生",
    "教师": "教師",
    "学生": "學生",
    "工人": "工人/農民",
    "农民": "工人/農民",
}


def _規範角色(role: str) -> str:
    return _角色別名.get(role, role)


def _白話解釋(intent: str, results: dict[str, Any], role: str = "普通人", model: str = "local") -> str:
    """把技術結果翻譯成不同角色聽得懂的話。啟用 model=deepseek 時調用 DeepSeek API。"""
    if model == "deepseek":
        client = _get_deepseek_client()
        if client is not None:
            try:
                return client.explain_for_role(
                    content=json.dumps(results, ensure_ascii=False),
                    role=role,
                    intent=intent,
                    context={"intent": intent, "results": results, "role": role},
                )
            except Exception as e:
                print(f"🟡 DeepSeek 解釋生成失敗，回退本地模板: {e}", file=sys.stderr)
    if intent == "鏈接審核":
        urls = results.get("urls", [])
        if not urls:
            return "沒發現鏈接。"
        u = urls[0]
        risk = u["risk"]
        reasons = "、".join(u.get("reasons", [])) or "暫無明顯異常"
        if role == "醫生":
            return f"這個鏈接像個來路不明的病人樣本。{risk}。原因：{reasons}。建議先隔離（別點），確認安全再處理。"
        if role == "老人":
            return f"這個網址{risk}。{reasons}。您就記住一條：不認識的鏈接不要點，拿不准就問家裡人。"
        if role == "工人/農民":
            return f"這鏈接跟地裡突然冒出來的陌生牌子一樣，{risk}。{reasons}。別瞎點，點了可能丟錢。"
        if role == "教師":
            return f"這個鏈接相當於一份沒蓋章、沒署名的通知，{risk}。{reasons}。建議轉給信息技術老師或網管再看。"
        if role == "學生":
            return f"這鏈接像遊戲裡來路不明的寶箱，{risk}。{reasons}。點了可能號被盜，別點。"
        return f"這個鏈接{risk}。{reasons}。簡單說：不認識的鏈接別亂點。"

    if intent == "反詐審核":
        tr = results.get("text_risk", {})
        hits = tr.get("hits", [])
        risk = tr.get("risk", "🟢 低風險")
        if role == "醫生":
            return f"這段話的症狀很像詐騙：{risk}。它用了「{'、'.join(hits)}」這些高風險詞，就像病人同時出現多個危急指標。"
        if role == "老人":
            return f"這話{risk}。它裡面有「{'、'.join(hits)}」，這都是騙子常用的詞。記住：要錢的、要驗證碼的、要點鏈接的，一律先掛電話。"
        if role == "工人/農民":
            return f"這話{risk}。{ '、'.join(hits) }，聽著就像「先交押金再上工」的騙局。要錢的別信。"
        if role == "教師":
            return f"這段話{risk}。高頻風險詞：{'、'.join(hits)}。可以當成反詐案例給學生講。"
        if role == "學生":
            return f"這話{risk}。關鍵詞：{'、'.join(hits)}。騙子常用這些話術，直接無視。"
        return f"這段話{risk}。它用了「{'、'.join(hits)}」這些常見騙局關鍵詞。核心原則：不轉賬、不給驗證碼、不點陌生鏈接。"

    if intent in ("營銷套路", "灰色話術審核"):
        tr = results.get("text_risk", {})
        patterns = tr.get("patterns", [])
        names = "、".join(p["name"] for p in patterns) or "未識別"
        if role == "老人":
            return f"這不是詐騙，但是賣東西的套路：{names}。就是催你趕緊買、怕你冷靜。記住：越催越不急。"
        if role == "工人/農民":
            return f"這是商家話術：{names}。跟「最後一天大甩賣」一個路數，別被緊迫感忽悠。"
        if role == "學生":
            return f"這是營銷套路：{names}。遊戲裡也常見，就是讓你覺得『不買就虧了』，其實冷靜想想未必。"
        return f"這段話屬於營銷/灰色話術，命中套路：{names}。不犯法，但會用緊迫感、稀缺感影響判斷，建議冷靜對比。"

    if intent == "國學推演":
        gx = results.get("guoxue", {})
        r = gx.get("result", {})
        if gx.get("type") == "起卦":
            if role == "醫生":
                return f"這一卦像一次體檢：{r['卦名']}，整體趨勢是「{r['釋義']}」。不是判死刑，是提醒您注意這個階段的重心。"
            if role == "老人":
                return f"今天抽到{r['卦名']}，意思是{r['釋義']}」。不用慌，就是提醒您這陣子穩著點。"
            if role == "工人/農民":
                return f"這卦叫{r['卦名']}，大白話是{r['釋義']}。就跟幹活要看天氣一樣，這陣子先別冒進。"
            if role == "教師":
                return f"此卦為{r['卦名']}（第{r['卦序']}卦），卦辭大意：{r['釋義']}。可以把它理解為當下的一個「趨勢提醒」。"
            if role == "學生":
                return f"你抽到了{r['卦名']}，第{r['卦序']}卦。它想說的是：{r['釋義']}。不是迷信，是古人總結的經驗提醒。"
            return f"此卦為{r['卦名']}（第{r['卦序']}卦）：{r['釋義']}"
        else:
            return f"數字根為 {r.get('數字根', '-')}: {r.get('提示', '')}"

    # 綜合審核
    return "已綜合檢查鏈接、話術和數字根。具體結果看上面，核心就一句：陌生東西先核實，別急著轉錢。"


def _提問模板(role: str = "普通人") -> str:
    templates = {
        "醫生": "@龍智守 幫我看這個患者發來的鏈接安不安全\n@龍智守 這段話是不是新型醫療詐騙",
        "教師": "@龍智守 家長發的這個鏈接能點嗎\n@龍智守 幫我看看這份通知有沒有問題",
        "學生": "@龍智守 同學發的鏈接能點嗎\n@龍智守 幫我起一卦看看考試運",
        "老人": "@龍智守 我收到一條短信，你幫我看看是不是騙子\n@龍智守 這個鏈接能不能點",
        "工人/農民": "@龍智守 這個招工鏈接靠不靠譜\n@龍智守 有人讓我轉押金，你幫看看",
    }
    base = "@龍智守 幫我看看這個鏈接是不是騙子\n@龍智守 這段話有沒有坑\n@龍智守 幫我起一卦"
    return templates.get(role, base)


def _生成解釋文件(intent: str, results: dict[str, Any], role: str = "普通人", model: str = "local") -> Path:
    """生成一份該角色能看懂的詳細解釋 Markdown，返回文件路徑。"""
    ts = time.strftime("%Y%m%d_%H%M%S")
    path = Path(f"/tmp/龍智守解釋_{role.replace('/', '_')}_{intent}_{ts}.md")
    lines = [
        f"# 龍智守 · {intent} · {role}版解釋",
        "",
        f"**適合對象**：{_角色說明.get(role, '所有人')}",
        "",
        "## 一句話結論",
        _白話解釋(intent, results, role, model=model),
        "",
        "## 詳細說明",
    ]
    if intent == "鏈接審核":
        for u in results.get("urls", []):
            lines.append(f"- 鏈接：{u['url']}")
            lines.append(f"- 風險：{u['risk']}")
            lines.append(f"- 原因：{'、'.join(u.get('reasons', [])) or '暫無'}")
    elif intent == "反詐審核":
        tr = results.get("text_risk", {})
        lines.append(f"- 風險：{tr.get('risk')}")
        lines.append(f"- 命中關鍵詞：{'、'.join(tr.get('hits', []))}")
        patterns = tr.get("patterns", [])
        if patterns:
            lines.append("")
            lines.append("## 命中套路庫")
            for p in patterns:
                lines.append(f"- **{p['id']} {p['name']}**（{p['category']}·{p['risk_level']}）")
                lines.append(f"  - {p['description']}")
                lines.append(f"  - ✅ 應對：{p['counter_measure']}")
    elif intent == "國學推演":
        gx = results.get("guoxue", {})
        r = gx.get("result", {})
        if gx.get("type") == "起卦":
            lines.append(f"- 卦名：{r.get('卦名')}")
            lines.append(f"- 卦序：第 {r.get('卦序')} 卦")
            lines.append(f"- 釋義：{r.get('釋義')}")
            lines.append(f"- 數字根：{r.get('數字根')}")
    elif intent in ("營銷套路", "灰色話術審核"):
        tr = results.get("text_risk", {})
        lines.append(f"- 風險：{tr.get('risk')}")
        lines.append(f"- 命中關鍵詞：{'、'.join(tr.get('hits', []))}")
        patterns = tr.get("patterns", [])
        if patterns:
            lines.append("")
            lines.append("## 命中套路庫")
            for p in patterns:
                lines.append(f"- **{p['id']} {p['name']}**（{p['category']}·{p['risk_level']}）")
                lines.append(f"  - {p['description']}")
                lines.append(f"  - ✅ 應對：{p['counter_measure']}")
    lines.extend([
        "",
        "## 你可以這樣問龍智守",
        "",
        "```",
        _提問模板(role),
        "```",
        "",
        f"DNA: #龍芯⚡️{time.strftime('%Y%m%d%H%M%S')}-LONGZHI-SHOU-EXPLAIN",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _國學分析(text: str) -> dict[str, Any]:
    lowered = text.lower()
    起卦意圖 = any(k in lowered for k in [
        "起卦", "卦象", "運勢", "运势", "占卜", "易經", "易经",
        "周易", "算一卦", "起一卦", "求卦", "卜卦", "抽卦"
    ]) or ("卦" in text and any(k in text for k in ["起", "算", "求", "卜", "抽"]))
    if 起卦意圖:
        return {"type": "起卦", "result": _起卦(text)}
    # 默認給數字根與三色
    n = sum(ord(c) for c in text)
    dr = _digital_root(n)
    color = "red" if dr in (3, 7) else ("orange" if dr in (2, 6, 8) else "green")
    return {
        "type": "數字根",
        "result": {"數字根": dr, "提示": "三才通順，可行。" if color == "green" else "需謹慎觀察。"},
        "color": color,
    }


def _判斷意圖(text: str) -> str:
    lowered = text.lower()
    if _extract_urls(text):
        return "鏈接審核"

    patterns = _識別套路(text)
    if patterns:
        # 區分詐騙與營銷套路
        has_fraud = any(p["category"] == "詐騙" for p in patterns)
        has_marketing = any(p["category"] == "營銷套路" for p in patterns)
        if has_fraud:
            return "反詐審核"
        if has_marketing:
            return "營銷套路"
        return "灰色話術審核"

    if any(kw in text for kw in _诈骗关键词):
        return "反詐審核"

    if any(k in lowered for k in ["卦", "運勢", "易經", "周易", "三六九", "369", "數字根", "太極", "八卦", "河圖", "洛書"]):
        return "國學推演"
    return "綜合審核"


def _底部按钮() -> dict[str, Any]:
    """生成飞书卡片底部按钮，焊死确认码。"""
    actions = [
        {
            "tag": "button",
            "text": {"tag": "plain_text", "content": "✅ 确认"},
            "type": "primary",
            "value": json.dumps({"action": "confirm", "code": _CONFIRM}),
        },
        {
            "tag": "button",
            "text": {"tag": "plain_text", "content": "❌ 忽略"},
            "type": "default",
            "value": json.dumps({"action": "ignore", "code": _CONFIRM}),
        },
    ]
    return {
        "tag": "action",
        "actions": actions,
    }


def _使用指南卡片() -> dict[str, Any]:
    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": "龍智守 · 使用指南"},
            "template": "blue",
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": (
                        "**龍智守能幫你什麼？**\n"
                        "• 審核鏈接安不安全\n"
                        "• 識別詐騙話術\n"
                        "• 合同/通知避坑\n"
                        "• 易經起卦、數字根速查\n\n"
                        "**固定快捷指令（直接發對應文字即可）：**"
                    ),
                },
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": (
                        "`審計 <DNA>` — 調出該 DNA 的流程審計圖\n"
                        "`套路` — 查看近7天套路趨勢\n"
                        "`DNA日報` — 查看近7天 DNA 審計日報\n"
                        "`帮助` — 顯示本菜單"
                    ),
                },
            },
            {
                "tag": "note",
                "elements": [{"tag": "plain_text", "content": "日常用法照舊：直接發鏈接、發話術、發『起一卦』，龍智守會自動判斷。"}],
            },
            _底部按钮(),
        ],
    }


def _構建卡片(input_text: str, intent: str, results: dict[str, Any], role: str = "普通人", model: str = "local") -> dict[str, Any]:
    elements: list[dict[str, Any]] = []
    elements.append({
        "tag": "div",
        "text": {"tag": "lark_md", "content": f"**輸入**：{input_text[:200]}"},
    })

    if intent == "鏈接審核":
        urls = results["urls"]
        lines = [f"**{u['risk']}** [{u['domain'] or u['url']}]({u['url']})" for u in urls]
        details = []
        for u in urls:
            if u["reasons"]:
                details.append(f"• {u['domain']}: " + "；".join(u["reasons"]))
        content = "\n".join(lines) + ("\n\n**風險詳情**\n" + "\n".join(details) if details else "")
        template = "red" if any(u["risk"].startswith("🔴") for u in urls) else ("orange" if any(u["risk"].startswith("🟡") for u in urls) else "green")
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": content}})

    elif intent in ("反詐審核", "營銷套路", "灰色話術審核"):
        tr = results["text_risk"]
        content = f"**{tr['risk']}**\n"
        if tr["hits"]:
            content += "命中關鍵詞：" + "、".join(tr["hits"])
        else:
            content += "未命中高風險關鍵詞。"
        template = "red" if tr["risk"].startswith("🔴") else ("orange" if tr["risk"].startswith("🟡") else "green")
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": content}})

    elif intent == "國學推演":
        r = results["guoxue"]["result"]
        if results["guoxue"]["type"] == "起卦":
            content = (
                f"**卦象**：第 {r['卦序']} 卦 · {r['卦名']}\n"
                f"**爻象**：{r['爻']}\n"
                f"**數字根**：{r['數字根']}\n"
                f"**釋義**：{r['釋義']}"
            )
            template = r["color"]
        else:
            content = f"**數字根**：{r['數字根']}\n**提示**：{r['提示']}"
            template = results["guoxue"]["color"]
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": content}})

    else:
        # 綜合審核：鏈接 + 文本 + 數字根
        lines = []
        if "urls" in results and results["urls"]:
            lines.append("**鏈接檢測**：")
            for u in results["urls"]:
                lines.append(f"  {u['risk']} {u['domain'] or u['url']}")
        tr = results.get("text_risk")
        if tr:
            lines.append(f"**話術風險**：{tr['risk']}")
        gx = results.get("guoxue")
        if gx:
            r = gx["result"]
            lines.append(f"**數字根**：{r.get('數字根', '-')}")
        template = "blue"
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": "\n".join(lines)}})

    # 命中套路展示（反詐 / 營銷套路）
    patterns = []
    if "text_risk" in results and results["text_risk"]:
        patterns = results["text_risk"].get("patterns", [])
    if patterns:
        pattern_lines = ["**命中套路：**"]
        for p in patterns:
            pattern_lines.append(
                f"• **{p['id']} {p['name']}**（{p['category']}·{p['risk_level']}）\n  {p['description']}\n  ✅ **應對**：{p['counter_measure']}"
            )
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": "\n\n".join(pattern_lines)}})

    # 白話解釋 + 提問模板
    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": f"**【{role}版解釋】**\n{_白話解釋(intent, results, role, model=model)}",
        },
    })

    elements.append({
        "tag": "note",
        "elements": [
            {
                "tag": "plain_text",
                "content": (
                    f"📎 詳細「{role}版」解釋將以附件發送\n"
                    f"💡 試試這樣問：{_提問模板(role).split(chr(10))[0]}"
                ),
            }
        ],
    })

    elements.append({
        "tag": "note",
        "elements": [{"tag": "plain_text", "content": f"龍智守 · {time.strftime('%Y-%m-%d %H:%M')} · DNA: #龍芯⚡️{time.strftime('%Y%m%d%H%M%S')}-LONGZHI-SHOU"}],
    })

    # 底部按钮
    elements.append(_底部按钮())

    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"龍智守 · {intent}"},
            "template": template,
        },
        "elements": elements,
    }


def _記錄套路識別(
    input_text: str,
    intent: str,
    results: dict[str, Any],
    role: str,
) -> None:
    """把每次識別結果寫入 JSONL，方便後續精準分析套路趨勢。"""
    try:
        _套路日誌路徑.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "dna": f"#龍芯⚡️{time.strftime('%Y%m%d%H%M%S')}-LONGZHI-SHOU-LOG",
            "role": role,
            "intent": intent,
            "input_hash": hashlib.sha256(input_text.encode()).hexdigest()[:16],
            "input_preview": input_text[:200],
            "urls": [u.get("domain") or u.get("url") for u in results.get("urls", [])],
            "patterns": [
                {"id": p["id"], "name": p["name"], "category": p["category"], "risk_level": p["risk_level"]}
                for p in results.get("text_risk", {}).get("patterns", [])
            ],
            "risk": results.get("text_risk", {}).get("risk", ""),
        }
        with _套路日誌路徑.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"🟡 套路識別日誌寫入失敗: {e}", file=sys.stderr)


def _構建審計卡片(dna: str, record: dict[str, Any], report_md: str) -> dict[str, Any]:
    """把 DNA 審計報告包成飛書卡片。"""
    status = record.get("three_color", {}).get("status", "🟢")
    template = "green" if status == "🟢" else ("orange" if status == "🟡" else "red")
    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"龍智守 · DNA 流程審計"},
            "template": template,
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**DNA**: `{dna}`\n**意圖**: {record.get('intent', '-')}\n**時間**: {record.get('timestamp', '-')}",
                },
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**審計結論**: {status} {record.get('three_color', {}).get('reason', '')}",
                },
            },
            {
                "tag": "div",
                "text": {"tag": "lark_md", "content": f"**輸入預覽**: {record.get('input_preview', '')[:120]}"},
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**流程圖 Mermaid**\n```mermaid\n{_dna_portal.render_mermaid(record) if _dna_portal else '# DNA門戶未加載'}\n```",
                },
            },
            {
                "tag": "note",
                "elements": [
                    {"tag": "plain_text", "content": "📎 完整審計報告（含哈希、來源鏈、工具調用）將以附件發送"}
                ],
            },
            {
                "tag": "note",
                "elements": [
                    {"tag": "plain_text", "content": f"DNA: #龍芯⚡️{time.strftime('%Y%m%d%H%M%S')}-LONGHUN-DNA-AUDIT"}
                ],
            },
            _底部按钮(),
        ],
    }


def _DNA審計回應(dna: str, role: str = "普通人") -> tuple[str, dict[str, Any], dict[str, Any], Path | None]:
    """根據 DNA 查詢流程審計記錄並返回卡片。"""
    if _dna_portal is None:
        return "DNA審計", {"error": "DNA 審計門戶未加載"}, _使用指南卡片(), None
    result = _dna_portal.audit(dna, role)
    if not result["found"]:
        card = {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": "龍智守 · DNA 未找到"}, "template": "red"},
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": f"**DNA**: `{dna}`\n未在審計庫中找到該記錄。"}},
                {"tag": "note", "elements": [{"tag": "plain_text", "content": "請確認 DNA 完整無誤，或該輸出尚未被記錄。"}]},
            ],
        }
        return "DNA審計", {"error": result.get("error", "未找到")}, card, None

    record = result["record"]
    report_path = result["report_path"]
    card = _構建審計卡片(dna, record, result["report"])
    return "DNA審計", {"record": record}, card, Path(report_path)


def _套路趨勢回應(days: int = 7, top: int = 10) -> tuple[str, dict[str, Any], dict[str, Any], Path | None]:
    """直接返回龍智守套路趨勢卡片與報告。"""
    analyzer = Path.home() / "longhun-system" / "scripts" / "龍智守_套路分析.py"
    if not analyzer.exists():
        return "套路趨勢", {"error": "套路分析脚本不存在"}, _使用指南卡片(), None
    try:
        r = subprocess.run(
            [sys.executable, str(analyzer), "--days", str(days), "--top", str(top)],
            capture_output=True, text=True, timeout=60,
        )
        data = json.loads(r.stdout) if r.returncode == 0 else {}
    except Exception as e:
        return "套路趨勢", {"error": str(e)}, _使用指南卡片(), None

    total = data.get("total_records", 0)
    categories = data.get("categories", {})
    fraud = categories.get("詐騙", 0)
    marketing = categories.get("營銷套路", 0)
    gray = categories.get("灰色話術", 0)
    status = "🔴" if fraud else ("🟡" if total else "🟢")

    lines = [
        f"**時間範圍**：{data.get('time_range', f'最近 {days} 天')}",
        f"**總識別次數**：{total}",
        f"**詐騙**：{fraud} 次 · **營銷套路**：{marketing} 次 · **灰色話術**：{gray} 次",
        "",
        "**Top 套路**：",
    ]
    top_patterns = data.get("top_patterns", {})
    if top_patterns:
        for name, count in top_patterns.items():
            lines.append(f"- {name}: {count} 次")
    else:
        lines.append("- 暫無命中套路")

    card = {
        "config": {"wide_screen_mode": True},
        "header": {"title": {"tag": "plain_text", "content": "龍智守 · 套路趨勢"}, "template": "red" if fraud else "orange"},
        "elements": [
            {"tag": "div", "text": {"tag": "lark_md", "content": "\n".join(lines)}},
            {"tag": "note", "elements": [{"tag": "plain_text", "content": "📎 詳細趨勢報告將以附件發送"}]},
            {"tag": "note", "elements": [{"tag": "plain_text", "content": f"DNA: #龍芯⚡️{time.strftime('%Y%m%d%H%M%S')}-LONGZHI-SHOU-TREND"}]},
            _底部按钮(),
        ],
    }

    ts = time.strftime("%Y%m%d_%H%M%S")
    report_path = Path(f"/tmp/龍智守套路趨勢_{ts}.md")
    report_path.write_text("# 龍智守套路趨勢\n\n" + "\n".join(lines), encoding="utf-8")
    return "套路趨勢", data, card, report_path


def _DNA日報回應(days: int = 7) -> tuple[str, dict[str, Any], dict[str, Any], Path | None]:
    """直接返回龍魂 DNA 流程審計日報卡片與報告。"""
    if _dna_portal is None:
        return "DNA日報", {"error": "DNA 審計門戶未加載"}, _使用指南卡片(), None

    records = _dna_portal.load_records()
    if not records:
        return "DNA日報", {"error": "暫無記錄"}, _使用指南卡片(), None

    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    recent = [r for r in records if datetime.datetime.strptime(r.get("timestamp", "")[:10], "%Y-%m-%d") >= cutoff]
    total = len(recent)
    fraud = sum(1 for r in recent if r.get("three_color", {}).get("status") == "🔴")
    warning = sum(1 for r in recent if r.get("three_color", {}).get("status") == "🟡")
    green = sum(1 for r in recent if r.get("three_color", {}).get("status") == "🟢")
    file_count = sum(len(r.get("output_files", {})) for r in recent)
    status = "🔴" if fraud else ("🟢" if total else "🟡")

    lines = [
        f"**時間範圍**：最近 {days} 天",
        f"**總 DNA 數**：{total}",
        f"**三色分佈**：🟢 {green} · 🟡 {warning} · 🔴 {fraud}",
        f"**附帶文件哈希數**：{file_count}",
        "",
        "**最新 DNA**：",
    ]
    for r in recent[-5:]:
        lines.append(
            f"- `{r.get('dna')}` · {r.get('intent')} · {r.get('three_color', {}).get('status', '🟢')}"
        )

    card = {
        "config": {"wide_screen_mode": True},
        "header": {"title": {"tag": "plain_text", "content": "龍智守 · DNA 日報"}, "template": "red" if fraud else "green"},
        "elements": [
            {"tag": "div", "text": {"tag": "lark_md", "content": "\n".join(lines)}},
            {"tag": "note", "elements": [{"tag": "plain_text", "content": "📎 詳細 DNA 審計日報將以附件發送"}]},
            {"tag": "note", "elements": [{"tag": "plain_text", "content": f"DNA: #龍芯⚡️{time.strftime('%Y%m%d%H%M%S')}-LONGHUN-DNA-DAILY"}]},
            _底部按钮(),
        ],
    }

    ts = time.strftime("%Y%m%d_%H%M%S")
    report_path = Path(f"/tmp/龍魂DNA日報_{ts}.md")
    report_path.write_text("# 龍魂 DNA 流程審計日報\n\n" + "\n".join(lines), encoding="utf-8")
    return "DNA日報", {"total": total, "fraud": fraud, "warning": warning, "green": green}, card, report_path


def _解析指令(text: str) -> tuple[str, str]:
    """解析極簡固定指令。返回 (cmd, arg)。"""
    t = text.strip()
    # 去掉可能的前綴 @龍智守
    t = re.sub(r"^@龍智守\s*", "", t)

    # 純 DNA
    if _dna_portal is not None and _dna_portal.looks_like_dna(t):
        return ("審計", t)

    lower = t.lower()
    if lower in ("帮助", "幫助", "菜单", "菜單", "help", "?", "？"):
        return ("帮助", "")
    if lower in ("套路", "反诈", "反詐", "营销", "營銷", "套路趋势", "套路趨勢"):
        return ("套路", "")
    if lower in ("dna日报", "dna日報", "审计日报", "審計日報", "dna"):
        return ("DNA日報", "")

    # 帶參數的指令：審計 <DNA>
    if t.startswith(("審計", "审计", "查DNA", "查dna")):
        arg = t.split(None, 1)[1] if len(t.split(None, 1)) > 1 else ""
        return ("審計", arg.strip())

    return ("", "")


def _審計檢查點(intent: str, results: dict[str, Any]) -> list[dict[str, Any]]:
    checks = []
    if "urls" in results:
        for u in results["urls"]:
            checks.append({"name": f"鏈接審核: {u.get('domain') or u.get('url')}", "result": u.get("risk", "-")})
    if "text_risk" in results:
        tr = results["text_risk"]
        checks.append({"name": "話術風險判定", "result": tr.get("risk", "-")})
        patterns = tr.get("patterns", [])
        if patterns:
            checks.append({"name": "套路庫匹配", "result": "、".join(f"{p['id']} {p['name']}" for p in patterns)})
    if "guoxue" in results:
        gx = results["guoxue"]
        if gx.get("type") == "起卦":
            r = gx.get("result", {})
            checks.append({"name": "國學推演", "result": f"{r.get('卦名')}（第{r.get('卦序')}卦）"})
        else:
            checks.append({"name": "數字根", "result": str(gx.get("result", {}).get("數字根", "-"))})
    return checks


def 守護(
    input_text: str,
    image_path: str | None = None,
    role: str = "普通人",
    model: str = "local",
) -> tuple[str, dict[str, Any], dict[str, Any], Path | None]:
    """分析輸入並返回意圖、結果、卡片、解釋文件路徑。"""
    # 空輸入：返回使用指南
    if not input_text or not input_text.strip():
        return "使用指南", {}, _使用指南卡片(), None

    # 極簡固定指令分發（先於極短輸入判斷，因為指令可能只有兩個字）
    cmd, arg = _解析指令(input_text)
    if cmd == "審計":
        if not arg:
            return "DNA審計", {"error": "缺少 DNA"}, _使用指南卡片(), None
        return _DNA審計回應(arg, role)
    if cmd == "套路":
        return _套路趨勢回應()
    if cmd == "DNA日報":
        return _DNA日報回應()
    if cmd == "帮助":
        return "使用指南", {}, _使用指南卡片(), None

    intent = _判斷意圖(input_text)
    results: dict[str, Any] = {}

    urls = _extract_urls(input_text)
    if urls:
        results["urls"] = [_check_url(u) for u in urls]

    if intent in ("反詐審核", "營銷套路", "灰色話術審核", "綜合審核") or not urls:
        results["text_risk"] = _check_text(input_text)

    if intent in ("國學推演", "綜合審核"):
        results["guoxue"] = _國學分析(input_text)

    if image_path:
        results["image_note"] = "圖片暫僅作記錄，文字/鏈接審核為主。"

    # 記錄到套路識別日誌
    _記錄套路識別(input_text, intent, results, role)

    card = _構建卡片(input_text, intent, results, role, model=model)
    explain_file = _生成解釋文件(intent, results, role, model=model)

    # 生成統一 DNA 並覆蓋卡片腳註
    dna = f"#龍芯⚡️{time.strftime('%Y%m%d%H%M%S')}-LONGZHI-SHOU"
    for el in card.get("elements", []):
        if el.get("tag") == "note":
            for e in el.get("elements", []):
                content = e.get("content", "")
                if isinstance(content, str) and "DNA:" in content:
                    e["content"] = f"龍智守 · {time.strftime('%Y-%m-%d %H:%M')} · DNA: {dna}"

    # 寫入 DNA 流程審計庫
    if _dna_portal is not None:
        try:
            tr = results.get("text_risk", {})
            risk = tr.get("risk", "")
            three_color = {"status": "🟢", "reason": "無異常"}
            if risk.startswith("🔴"):
                three_color = {"status": "🔴", "reason": "命中高風險或詐騙套路"}
            elif risk.startswith("🟡"):
                three_color = {"status": "🟡", "reason": "命中中風險或營銷套路"}
            _dna_portal.record_workflow(
                dna=dna,
                input_text=input_text,
                intent=intent,
                skills=["龍智守", "longhun-workflow-transparent"],
                tools=[{"tool": "feishu_bot.send_card", "summary": "發送交互式審核卡片"}],
                checks=_審計檢查點(intent, results),
                ironlaw_result={"passed": True, "violations": []},
                three_color=three_color,
                output_card=card,
                output_files=[str(explain_file)] if explain_file else [],
                metadata={"role": role, "image_path": image_path},
            )
        except Exception as e:
            print(f"🟡 DNA 流程審計記錄失敗: {e}", file=sys.stderr)

    return intent, results, card, explain_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="龍智守 — 龍魂生活/办公智能守护")
    parser.add_argument("--input", "-i", required=True, help="用戶輸入內容")
    parser.add_argument("--image", help="圖片路徑（可選）")
    parser.add_argument(
        "--role",
        default="普通人",
        type=_規範角色,
        choices=list(_角色說明.keys()) + list(_角色別名.keys()),
        help="解釋語氣適配的對象（普通人/醫生/教師/學生/老人/工人/農民）",
    )
    parser.add_argument("--send", action="store_true", help="將結果發送到 FEISHU_CHAT_ID")
    parser.add_argument("--chat-id", default=os.environ.get("FEISHU_CHAT_ID"), help="飛書群 chat_id")
    parser.add_argument("--model", default="local", choices=["local", "deepseek"], help="解釋生成模型：local=本地模板，deepseek=调用 DeepSeek API")
    args = parser.parse_args(argv)

    intent, results, card, explain_file = 守護(args.input, args.image, args.role, model=args.model)

    if args.send:
        chat_id = args.chat_id
        if not chat_id:
            print("🔴 未設置 FEISHU_CHAT_ID，無法發送")
            return 1
        try:
            feishu_bot.send_card(chat_id, card)
            if explain_file:
                feishu_bot.send_file(chat_id, str(explain_file))
            print(f"🟢 龍智守「{intent}」結果已發飛書（含{args.role}版解釋附件）")
        except Exception as e:
            print(f"🔴 發送失敗: {e}")
            return 1
    else:
        print(f"意圖：{intent}")
        print(json.dumps(results, ensure_ascii=False, indent=2))
        print("--- 卡片 ---")
        print(json.dumps(card, ensure_ascii=False, indent=2))
        if explain_file:
            print(f"--- 解釋文件：{explain_file} ---")

    return 0


if __name__ == "__main__":
    sys.exit(main())
