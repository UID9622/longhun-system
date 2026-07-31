#!/usr/bin/env python3
"""
龍魂·行为锚引擎 v1.0
────────────────────
从用户日常行为数据中提取「固定锚点」，在焦虑升高时提醒回归稳定行为。

铁律：只分析行为模式，不评判行为好坏，不建用户画像。
锚点的定义：不是「好习惯」，而是「让你稳定的行为」。

DNA: #龍芯⚡️丙午·乙未·丁酉·MENTAL-IMMUNE-BEHAVIOR-ANCHOR-v1.0-b0c1d2e3
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import json
import time
from pathlib import Path
from collections import Counter, defaultdict
from dataclasses import dataclass, field

DATA_DIR = Path.home() / ".龍魂" / "mental_immune"
DATA_DIR.mkdir(parents=True, exist_ok=True)
ANCHOR_LOG = DATA_DIR / "behavior_log.jsonl"
ANCHORS_FILE = DATA_DIR / "anchors.json"


@dataclass
class BehaviorAnchor:
    """行为锚点 — 让你稳定的例行行为"""
    id: str
    name: str
    category: str           # 身体/心智/社交/创作/休息
    pattern: str            # 时间规律 e.g. "daily-08:00-08:30"
    frequency: str          # daily / weekday / weekend / weekly
    stability_score: float  # 0-1 稳定性评分
    first_seen: float
    last_seen: float
    total_occurrences: int = 0
    description: str = ""


@dataclass  
class AnchorCheckIn:
    """锚点签到 — 一次行为记录"""
    timestamp: float
    anchor_id: str
    day_of_week: int        # 0=Monday
    hour_of_day: int
    note: str = ""


class BehaviorAnchorEngine:
    """
    行为锚引擎
    
    不做的事：
    - ❌ 不评判行为好坏
    - ❌ 不建用户画像
    - ❌ 不分析行为动机
    - ❌ 不上传任何数据
    
    做的事：
    - ✅ 发现你生活中重复出现的稳定模式
    - ✅ 在焦虑时提醒你：这些事曾经让你稳定下来
    - ✅ 你自己定义什么是「锚」
    """
    
    # ── 锚点类别 ──
    CATEGORIES = {
        "身体": ["跑步", "散步", "健身", "瑜伽", "拉伸", "跳绳", "游泳", "骑行", "跳舞"],
        "心智": ["读书", "写作", "思考", "学习", "冥想", "记日记", "画画", "练字"],
        "社交": ["通话", "见面", "聚会", "陪伴家人", "遛狗", "喝茶"],
        "创作": ["写代码", "写文章", "做音乐", "摄影", "做手工", "烹饪"],
        "休息": ["午睡", "泡澡", "发呆", "听音乐", "看窗外", "喝咖啡", "浇花"],
    }
    
    def __init__(self):
        self.anchors: dict[str, BehaviorAnchor] = {}
        self.checkins: list[AnchorCheckIn] = []
        self._load()
    
    def log_behavior(self, name: str, category: str = "", note: str = "") -> bool:
        """
        记录一次行为。
        
        Args:
            name: 行为名称，如 "晨跑"
            category: 类别（可选，自动推断）
            note: 备注（可选）
        """
        now = time.time()
        local = time.localtime(now)
        day_of_week = local.tm_wday  # 0=周一
        hour = local.tm_hour
        
        # 自动推断类别
        if not category:
            for cat, keywords in self.CATEGORIES.items():
                if any(kw in name for kw in keywords):
                    category = cat
                    break
            if not category:
                category = "其他"
        
        # 生成或更新锚点
        anchor_id = self._anchor_id(name, category)
        
        if anchor_id not in self.anchors:
            self.anchors[anchor_id] = BehaviorAnchor(
                id=anchor_id,
                name=name,
                category=category,
                pattern=self._infer_pattern(hour),
                frequency="daily",  # 初始默认
                stability_score=0.0,
                first_seen=now,
                last_seen=now,
                total_occurrences=0,
                description=f"你在{hour:02d}:00左右会{name}",
            )
        
        anchor = self.anchors[anchor_id]
        anchor.last_seen = now
        anchor.total_occurrences += 1
        anchor.stability_score = self._calc_stability(anchor)
        anchor.description = self._describe_anchor(anchor)
        
        # 记录签到
        checkin = AnchorCheckIn(
            timestamp=now,
            anchor_id=anchor_id,
            day_of_week=day_of_week,
            hour_of_day=hour,
            note=note,
        )
        self.checkins.append(checkin)
        
        self._save()
        return True
    
    def get_anchors(self, min_stability: float = 0.3) -> list[dict]:
        """
        获取当前发现的所有锚点。
        
        Args:
            min_stability: 最低稳定性阈值
        
        Returns:
            锚点列表
        """
        result = []
        for anchor in self.anchors.values():
            if anchor.stability_score >= min_stability:
                result.append({
                    "id": anchor.id,
                    "name": anchor.name,
                    "category": anchor.category,
                    "description": anchor.description,
                    "stability": round(anchor.stability_score, 2),
                    "occurrences": anchor.total_occurrences,
                    "icon": self._category_icon(anchor.category),
                })
        
        result.sort(key=lambda x: x["stability"], reverse=True)
        return result
    
    def suggest_anchor(self, anxiety_score: float) -> dict:
        """
        在焦虑时，推荐一个稳定行为锚点。
        
        Args:
            anxiety_score: 当前焦虑指数 0-100
        
        Returns:
            推荐锚点信息
        """
        anchors = self.get_anchors(min_stability=0.2)
        
        if not anchors:
            return {
                "found": False,
                "message": "还没有发现稳定的行为锚点。没关系，从现在开始记录——任何让你觉得「还行」的小事都可以。",
                "suggestion": "现在就可以做的事：起身倒一杯水，走到窗边看30秒窗外。",
            }
        
        # 选稳定性最高的锚点
        best = anchors[0]
        
        messages = {
            "身体": "身体记得怎么让你稳定下来。",
            "心智": "你曾在书页间找到平静。",
            "社交": "有人等着你的声音。",
            "创作": "创造本身就是治愈。",
            "休息": "停下不是放弃，是给灵魂充电。",
            "其他": "你曾做过的事，再做一次就好。",
        }
        
        return {
            "found": True,
            "anchor": best,
            "message": messages.get(best["category"], "回到你熟悉的节奏里。"),
            "urgency": "high" if anxiety_score > 60 else "normal",
            "tip": f"不需要做很久，就5分钟。像以前那样{best['name']}就好。",
        }
    
    def get_daily_rhythm(self) -> dict:
        """分析每日节奏模式"""
        if not self.checkins:
            return {"message": "还没有足够的数据。开始记录你的日常吧。"}
        
        # 按时段统计
        hour_buckets = defaultdict(int)
        for c in self.checkins:
            # 如 07:30 → bucket "07"
            hour_buckets[c.hour_of_day] += 1
        
        # 找最活跃时段
        sorted_hours = sorted(hour_buckets.items(), key=lambda x: x[1], reverse=True)
        peak_hours = [h for h, _ in sorted_hours[:3]]
        
        return {
            "total_checkins": len(self.checkins),
            "total_anchors": len([a for a in self.anchors.values() if a.stability_score >= 0.3]),
            "peak_hours": peak_hours,
            "peak_hours_str": "、".join([f"{h:02d}:00" for h in sorted(peak_hours)]),
            "message": "这些是你的生活节奏。在焦虑时，回到这个节奏里——身体认得路。",
        }
    
    def manual_add_anchor(self, name: str, category: str, frequency: str = "daily") -> str:
        """手动添加一个锚点"""
        anchor_id = self._anchor_id(name, category)
        self.anchors[anchor_id] = BehaviorAnchor(
            id=anchor_id,
            name=name,
            category=category,
            pattern=f"{frequency}-00:00",
            frequency=frequency,
            stability_score=0.5,  # 手动添加的初始信任度
            first_seen=time.time(),
            last_seen=time.time(),
            total_occurrences=1,
            description=f"你为自己设定的锚：{name}",
        )
        self._save()
        return anchor_id
    
    # ── 内部方法 ──
    
    def _anchor_id(self, name: str, category: str) -> str:
        """生成锚点ID"""
        import hashlib
        raw = f"{name}-{category}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]
    
    def _infer_pattern(self, hour: int) -> str:
        """推断行为的时间模式"""
        if 5 <= hour < 8:
            return "early_morning"
        elif 8 <= hour < 12:
            return "morning"
        elif 12 <= hour < 14:
            return "noon"
        elif 14 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 21:
            return "evening"
        else:
            return "night"
    
    def _calc_stability(self, anchor: BehaviorAnchor) -> float:
        """计算锚点稳定性 0-1"""
        if anchor.total_occurrences < 2:
            return 0.1
        
        # 基础分：出现次数越多越稳定（对数增长）
        count_score = min(anchor.total_occurrences / 10, 1.0) * 0.4
        
        # 持续性：最近一次出现的时间
        days_since_last = (time.time() - anchor.last_seen) / 86400
        recency_score = max(0, (1 - days_since_last / 30)) * 0.3
        
        # 持续时间：从首次到最近的天数跨度
        span_days = max(1, (anchor.last_seen - anchor.first_seen) / 86400)
        span_score = min(span_days / 30, 1.0) * 0.3
        
        return min(count_score + recency_score + span_score, 1.0)
    
    def _describe_anchor(self, anchor: BehaviorAnchor) -> str:
        """生成锚点的自然语言描述"""
        hour = time.localtime(anchor.last_seen).tm_hour
        patterns = {
            "early_morning": f"清晨{hour:02d}:00左右",
            "morning": f"上午{hour:02d}:00左右",
            "noon": "午后时分",
            "afternoon": f"下午{hour:02d}:00左右",
            "evening": f"傍晚{hour:02d}:00左右",
            "night": f"晚上{hour:02d}:00左右",
        }
        time_desc = patterns.get(anchor.pattern, "每天")
        return f"{time_desc}，你会{anchor.name}（已发生{anchor.total_occurrences}次）"
    
    def _category_icon(self, category: str) -> str:
        icons = {"身体": "🏃", "心智": "📖", "社交": "🤝", "创作": "🎨", "休息": "☕", "其他": "📍"}
        return icons.get(category, "📍")
    
    def _save(self):
        """保存到本地"""
        data = {
            "anchors": {
                aid: {
                    "id": a.id, "name": a.name, "category": a.category,
                    "pattern": a.pattern, "frequency": a.frequency,
                    "stability_score": a.stability_score,
                    "first_seen": a.first_seen, "last_seen": a.last_seen,
                    "total_occurrences": a.total_occurrences,
                    "description": a.description,
                }
                for aid, a in self.anchors.items()
            },
            "updated": time.time(),
        }
        with open(ANCHORS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 签到追加
        recent = self.checkins[-50:]  # 只保留最近50条
        with open(ANCHOR_LOG, "a", encoding="utf-8") as f:
            for c in recent:
                f.write(json.dumps({
                    "ts": c.timestamp, "anchor_id": c.anchor_id,
                    "dow": c.day_of_week, "hour": c.hour_of_day,
                    "note": c.note,
                }, ensure_ascii=False) + "\n")
    
    def _load(self):
        """加载本地数据"""
        # 加载锚点
        if ANCHORS_FILE.exists():
            try:
                with open(ANCHORS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for aid, a in data.get("anchors", {}).items():
                    self.anchors[aid] = BehaviorAnchor(
                        id=a["id"], name=a["name"], category=a["category"],
                        pattern=a["pattern"], frequency=a.get("frequency", "daily"),
                        stability_score=a["stability_score"],
                        first_seen=a["first_seen"], last_seen=a["last_seen"],
                        total_occurrences=a["total_occurrences"],
                        description=a.get("description", ""),
                    )
            except (json.JSONDecodeError, KeyError):
                pass
        
        # 加载签到
        if ANCHOR_LOG.exists():
            try:
                with open(ANCHOR_LOG, "r", encoding="utf-8") as f:
                    for line in f.readlines()[-200:]:
                        try:
                            d = json.loads(line.strip())
                            self.checkins.append(AnchorCheckIn(
                                timestamp=d["ts"], anchor_id=d["anchor_id"],
                                day_of_week=d.get("dow", 0), hour_of_day=d.get("hour", 0),
                                note=d.get("note", ""),
                            ))
                        except (json.JSONDecodeError, KeyError):
                            continue
            except FileNotFoundError:
                pass


if __name__ == "__main__":
    engine = BehaviorAnchorEngine()
    
    print("⚓ 行为锚引擎\n")
    
    # 模拟记录
    engine.log_behavior("晨跑", "身体", "公园3公里")
    engine.log_behavior("读书", "心智", "哲学类")
    engine.log_behavior("泡茶", "休息", "龙井")
    engine.log_behavior("晨跑", "身体")
    engine.log_behavior("读书", "心智")
    
    print("已发现锚点:")
    for a in engine.get_anchors():
        bar = "█" * int(a["stability"] * 20) + "░" * (20 - int(a["stability"] * 20))
        print(f"  {a['icon']} [{bar}] {a['name']} — {a['description']}")
    
    print(f"\n🆘 焦虑时建议:")
    suggestion = engine.suggest_anchor(anxiety_score=65)
    if suggestion["found"]:
        print(f"  试试: {suggestion['anchor']['name']}")
        print(f"  原因: {suggestion['message']}")
        print(f"  {suggestion['tip']}")
    
    print(f"\n📊 每日节奏:")
    rhythm = engine.get_daily_rhythm()
    print(f"  活跃时段: {rhythm.get('peak_hours_str', '—')}")
    print(f"  总签到: {rhythm.get('total_checkins', 0)}次")
