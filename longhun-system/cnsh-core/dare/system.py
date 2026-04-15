"""
dare/system.py — 四敢品质系统
六爻映射 + 道德经彩蛋 + 洛书369加权
"""
import time, hashlib
from typing import Dict, List, Optional
from .store import record_action, get_actions, init_dare_tables

# ── 四敢定义 ──────────────────────────────────────────────────────

DARE_CODES = {
    "TRUST-INIT": {"name": "敢相信", "yao": "初爻", "weight_base": 1.0,
                   "desc": "信任他人，不因利益算计而退缩"},
    "SACRIFICE":  {"name": "敢吃亏", "yao": "二爻", "weight_base": 1.5,
                   "desc": "主动让利，以长远利益换取短期损失"},
    "DISSENT":    {"name": "敢说不服", "yao": "三爻", "weight_base": 1.0,
                   "desc": "公开表达异议，不随波逐流"},
    "AUDIT-OPEN": {"name": "敢公开审计", "yao": "四爻", "weight_base": 2.0,
                   "desc": "主动公开决策过程，接受监督"},
}

# 五爻(君位): 四敢俱全 + 道德经彩蛋
# 上爻(极致): 通天大道资格

TAOIST_WEIGHTS = {
    "water":       0.30,   # 上善若水
    "valley":      0.25,   # 虚怀若谷
    "valley_king": 0.45,   # 谷王
}

# 道德经彩蛋阈值
EASTER_EGG_RULES = [
    {
        "id": "shang_shan",
        "condition": lambda s: all(v > 100 for v in s.values()),
        "text": "上善若水 · 解锁私域无限权限",
        "chapter": "第八章",
        "original": "上善若水。水善利萬物而不爭",
        "yao": "五爻君位",
    },
    {
        "id": "gu_wang",
        "condition": lambda s: s.get("SACRIFICE", 0) > 200 and s.get("AUDIT-OPEN", 0) > 150,
        "text": "谷王 · 解锁公域透明通道",
        "chapter": "第六十六章",
        "original": "江海之所以能為百谷王者，以其善下之",
        "yao": "上爻通天",
    },
    {
        "id": "wu_wei",
        "condition": lambda s: s.get("DISSENT", 0) > 80 and s.get("TRUST-INIT", 0) > 80,
        "text": "无为而无不为 · 解锁自动仲裁模式",
        "chapter": "第四十八章",
        "original": "損之又損，以至於無為。無為而無不為",
        "yao": "三爻位",
    },
]

# 洛书369数字根
def digital_root(n: int) -> int:
    return 1 + ((n - 1) % 9) if n > 0 else 0

def is_369(n: int) -> bool:
    return digital_root(n) in {3, 6, 9}

# ── 级别判定 ──────────────────────────────────────────────────────

def _determine_level(scores: Dict[str, float]) -> Dict:
    total = sum(scores.values())
    filled = sum(1 for v in scores.values() if v > 0)
    all_active = all(v > 30 for v in scores.values())

    if total >= 800 and all_active:
        return {"code": "通天大道", "yao": "上爻", "desc": "四敢俱全且深厚，通天资格"}
    elif total >= 400 and all_active:
        return {"code": "君子位", "yao": "五爻", "desc": "四敢俱全，道德经彩蛋可触发"}
    elif total >= 200 and filled >= 3:
        return {"code": "历练期", "yao": "四爻", "desc": "三敢以上，正在成长"}
    elif total >= 100 and filled >= 2:
        return {"code": "起步期", "yao": "三爻", "desc": "二敢以上，初见品质"}
    elif total >= 30:
        return {"code": "萌芽期", "yao": "二爻", "desc": "开始积累四敢行为"}
    else:
        return {"code": "初入局", "yao": "初爻", "desc": "四敢尚未成型"}

# ── 主类 ─────────────────────────────────────────────────────────

class FourDareSystem:

    def __init__(self):
        init_dare_tables()

    # ── 记录行为 ────────────────────────────────────────────────

    def record(self, action_type: str,
               weight: float = None,
               context: str = "",
               dna_trace: str = "",
               user_id: str = "uid9622") -> Dict:
        """记录一次四敢行为"""
        if action_type not in DARE_CODES:
            return {"ok": False, "error": f"未知类型: {action_type}，有效值: {list(DARE_CODES)}"}

        base = DARE_CODES[action_type]["weight_base"]
        w = weight if weight is not None else base

        # 洛书369加权
        content_hash = int(hashlib.sha256(f"{action_type}|{context}|{time.time()}".encode()).hexdigest(), 16)
        dr = digital_root(content_hash % 10000)
        if is_369(dr):
            w *= 1.369  # 369加持

        aid = record_action(action_type, w, context, dna_trace, user_id)
        return {
            "ok": True,
            "action_id": aid,
            "action_type": action_type,
            "name": DARE_CODES[action_type]["name"],
            "yao": DARE_CODES[action_type]["yao"],
            "weight_applied": round(w, 3),
            "is_369_blessed": is_369(dr),
        }

    # ── 计算四敢分 ──────────────────────────────────────────────

    def calculate_score(self, user_id: str = "uid9622") -> Dict:
        """计算四敢总分 + 级别 + 彩蛋"""
        actions = get_actions(user_id)
        scores: Dict[str, float] = {k: 0.0 for k in DARE_CODES}

        for act in actions:
            atype = act["action_type"]
            if atype in scores:
                scores[atype] += act["weight"]

        # 道德经彩蛋检测
        easter_eggs = []
        for rule in EASTER_EGG_RULES:
            if rule["condition"](scores):
                easter_eggs.append({
                    "id":       rule["id"],
                    "text":     rule["text"],
                    "chapter":  rule["chapter"],
                    "original": rule["original"],
                    "yao":      rule["yao"],
                })

        level = _determine_level(scores)
        total = sum(scores.values())

        # 道德经洛书369验证
        int_total = int(total)
        dr_total = digital_root(int_total) if int_total > 0 else 0

        return {
            "user_id":     user_id,
            "scores":      {k: round(v, 2) for k, v in scores.items()},
            "scores_named": {
                DARE_CODES[k]["name"]: round(v, 2) for k, v in scores.items()
            },
            "total":        round(total, 2),
            "action_count": len(actions),
            "level":        level,
            "digital_root": dr_total,
            "is_369":       is_369(dr_total),
            "easter_eggs":  easter_eggs,
            "yao_map":      {v["yao"]: {"code": k, "name": v["name"], "score": round(scores[k], 2)}
                             for k, v in DARE_CODES.items()},
            "updated_at":   time.strftime("%Y-%m-%d %H:%M:%S"),
        }

    # ── 六爻卦象 ────────────────────────────────────────────────

    def yao_status(self, user_id: str = "uid9622") -> Dict:
        """六爻状态可视化"""
        score_data = self.calculate_score(user_id)
        scores = score_data["scores"]

        yao_lines = []
        for code, info in DARE_CODES.items():
            sc = scores[code]
            active = sc > 30
            bar = "━" * min(int(sc / 10), 20)
            yao_lines.append({
                "yao":   info["yao"],
                "code":  code,
                "name":  info["name"],
                "score": round(sc, 1),
                "active": active,
                "bar":   f"{'⚡' if active else '·'} {info['yao']} {info['name']}: {bar} {round(sc,1)}",
            })

        # 五爻/上爻
        level = score_data["level"]
        extra = []
        if level["code"] in ("君子位", "通天大道"):
            extra.append(f"⭐ 五爻(君位) 四敢俱全 {'道德经彩蛋已触发 ✨' if score_data['easter_eggs'] else ''}")
        if level["code"] == "通天大道":
            extra.append("🌌 上爻(极致) 通天大道资格")

        return {
            "level":      level,
            "yao_lines":  yao_lines,
            "extra":      extra,
            "easter_eggs": score_data["easter_eggs"],
            "total":      score_data["total"],
        }

    # ── 道德经彩蛋 ──────────────────────────────────────────────

    def get_easter_eggs(self, user_id: str = "uid9622") -> List[Dict]:
        data = self.calculate_score(user_id)
        return data["easter_eggs"]
