# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""三色审计：对渲染内容跑 🟢🟡🔴 判定。"""

# 红线词：命中即 🔴（涉黄赌毒/诈骗/政治敏感/恶意内容）
RED_WORDS = [
    "裸聊", "裸贷", "博彩", "赌博", "外围女", "迷药", "办证", "代开发票",
    "兼职刷单", "杀猪盘", "传销", "洗钱", "跑分", "钓鱼网站", "勒索病毒",
    "制作炸弹", "枪支弹药", "售卖毒品", "嫖娼", "色情直播",
]
# 黄线词：命中即 🟡（隐私/成人/诱导/营销过度）
YELLOW_WORDS = [
    "身份证", "银行卡", "验证码", "密码", "隐私", "授权", "同意协议",
    "成人", "情趣", "借款", "贷款", "高利贷", "返利", "点击领取", "免费领",
    "中奖", "抽奖", "最低价", "限时抢购",
]


def audit_text(text: str) -> dict:
    """对文本跑三色审计。返回 {color, score, reason, red_hits, yellow_hits}"""
    if not text:
        return {"color": "🟡", "score": 0, "reason": "无文本可审计", "red_hits": [], "yellow_hits": []}
    red_hits = [w for w in RED_WORDS if w in text]
    yellow_hits = [w for w in YELLOW_WORDS if w in text]
    if red_hits:
        return {"color": "🔴", "score": 100, "reason": f"命中红线词: {', '.join(red_hits[:5])}",
                "red_hits": red_hits, "yellow_hits": yellow_hits}
    if yellow_hits:
        score = min(60, len(yellow_hits) * 10)
        return {"color": "🟡", "score": score, "reason": f"命中待核词: {', '.join(yellow_hits[:5])}",
                "red_hits": [], "yellow_hits": yellow_hits}
    return {"color": "🟢", "score": 0, "reason": "内容正常", "red_hits": [], "yellow_hits": []}


class AuditHook:
    """渲染审计钩子。"""

    def run(self, text: str = None) -> dict:
        return audit_text(text or "")
