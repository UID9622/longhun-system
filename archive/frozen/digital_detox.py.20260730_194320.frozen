#!/usr/bin/env python3
"""
龍魂·数字排毒向导 v1.0
────────────────────────
交互式引导用户完成一次数字排毒。
含：离线时间表生成、引导式呼吸训练、替代活动建议。

DNA: #龍芯⚡️丙午·乙未·丁酉·MENTAL-IMMUNE-DIGITAL-DETOX-v1.0-d6e7f8a9
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import json
import time
import random
from pathlib import Path
from dataclasses import dataclass, field

DATA_DIR = Path.home() / ".龍魂" / "mental_immune"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DETOX_LOG = DATA_DIR / "detox_log.jsonl"


@dataclass
class DetoxSession:
    """一次排毒会话"""
    session_id: str
    start_time: float
    duration_minutes: int = 30
    phases: list = field(default_factory=list)
    completed: bool = False
    mood_before: int = 0       # 1-5 排毒前心情
    mood_after: int = 0        # 1-5 排毒后心情
    activities_done: list = field(default_factory=list)


class DigitalDetox:
    """
    数字排毒向导
    
    三个核心模块：
    1. 生成离线时间表
    2. 引导式呼吸训练（3分钟）
    3. 替代活动建议
    """
    
    # ── 替代活动库 ──
    ACTIVITIES = {
        "身体类": [
            "出门散步20分钟（不带手机）",
            "做5分钟拉伸或简单的瑜伽动作",
            "原地蹦跳50下，让身体热起来",
            "去阳台/窗边站5分钟，只看天不看屏幕",
            "用冷水洗把脸，感受水的温度",
        ],
        "手工类": [
            "在纸上随意涂鸦5分钟，画什么都行",
            "整理桌面/书架/抽屉中的一个角落",
            "手写一封信或一段话（不发送也可以）",
            "做一杯手冲咖啡或泡一壶茶，慢慢品尝",
            "给一盆植物浇水，观察它的叶子",
        ],
        "心智类": [
            "翻开手边最近的一本书，读任意一页",
            "回忆今天发生的三件小事（都算）",
            "写下三个让你感激的人或事",
            "想一个童年记忆，越具体越好",
            "闭上眼睛，数自己的呼吸，数到20",
        ],
        "连接类": [
            "给一个很久没联系的朋友发一条问候（不许是工作相关的）",
            "跟身边的人说一句话（不在线说，当面说）",
            "帮身边的人做一件小事（倒水/拿东西/开窗）",
            "和家人一起吃一顿不看手机的饭",
        ],
    }
    
    # ── 呼吸训练引导 ──
    BREATHING_GUIDE = [
        {"phase": "准备", "duration": 15, "text": "找一个舒服的姿势坐好或躺好。闭上眼睛。"},
        {"phase": "吸气", "duration": 4, "text": "慢慢吸气……感受空气进入鼻腔……1……2……3……4"},
        {"phase": "屏息", "duration": 4, "text": "轻轻地屏住呼吸……1……2……3……4"},
        {"phase": "呼出", "duration": 6, "text": "缓缓呼出……让所有的紧张随这口气离开……1……2……3……4……5……6"},
        {"phase": "放松", "duration": 2, "text": "感受呼出后的那片刻空白……"},
    ]
    
    def __init__(self):
        self.sessions: list[DetoxSession] = []
        self.total_detox_minutes = 0
        self._load_log()
    
    def generate_offline_schedule(self, duration_hours: float = 2.0) -> dict:
        """
        生成离线时间表。
        
        Args:
            duration_hours: 离线时长（小时），默认2小时
        
        Returns:
            dict: 分阶段的时间安排
        """
        blocks = []
        total_min = int(duration_hours * 60)
        remaining = total_min
        
        # 热身阶段（10%）
        warmup = max(5, total_min // 10)
        blocks.append({
            "phase": "热身",
            "duration_min": warmup,
            "icon": "🟡",
            "activities": [
                "把所有电子设备调成静音/勿扰模式",
                "通知身边的人你接下来两小时不看手机",
                "倒一杯水放在手边",
                "写下你期望这两个小时后达到的状态（一句话）",
            ],
        })
        remaining -= warmup
        
        # 主活动阶段（60%）
        main_time = int(remaining * 0.6)
        main_block = {
            "phase": "沉浸",
            "duration_min": main_time,
            "icon": "🟢",
            "activities": self._pick_activities("沉浸", main_time),
        }
        blocks.append(main_block)
        remaining -= main_time
        
        # 深度阶段（30%）
        deep_time = remaining
        blocks.append({
            "phase": "深潜",
            "duration_min": deep_time,
            "icon": "🔵",
            "activities": self._pick_activities("深度", deep_time),
        })
        
        return {
            "total_minutes": total_min,
            "blocks": blocks,
            "rules": [
                "⛔ 手机放另一个房间，或至少伸手够不到的地方",
                "⛔ 屏幕亮度调至最低/暖色模式",
                "⛔ 如果有人找你——两小时后再说",
                "✅ 可以做任何不动屏幕的事",
                "✅ 可以发呆——发呆不是浪费时间",
            ],
            "tip": "两小时后回来，你会发现：天没塌，消息没丢，你没被世界抛弃。",
        }
    
    def breathing_exercise(self) -> list[dict]:
        """
        引导式呼吸训练（约3分钟）。
        
        Returns:
            逐步引导指令列表
        """
        steps = []
        rounds = 6  # 6轮呼吸，约3分钟
        
        # 准备
        steps.append({
            "step": 0,
            "phase": "准备",
            "duration_sec": self.BREATHING_GUIDE[0]["duration"],
            "instruction": self.BREATHING_GUIDE[0]["text"],
            "icon": "🧘",
        })
        
        for round_num in range(rounds):
            for i in range(1, len(self.BREATHING_GUIDE)):
                phase = self.BREATHING_GUIDE[i]
                steps.append({
                    "step": round_num * 4 + i,
                    "round": round_num + 1,
                    "phase": phase["phase"],
                    "duration_sec": phase["duration"],
                    "instruction": f"第{round_num + 1}轮 · {phase['text']}",
                    "icon": {
                        "吸气": "🌬️",
                        "屏息": "🤲",
                        "呼出": "💨",
                        "放松": "☁️",
                    }.get(phase["phase"], "🧘"),
                })
        
        # 收尾
        steps.append({
            "step": len(steps),
            "phase": "结束",
            "duration_sec": 10,
            "instruction": "最后一轮结束。保持闭眼，感受此刻的身体状态。慢慢睁开眼睛。欢迎回来。",
            "icon": "🌅",
        })
        
        return steps
    
    def get_alternatives(self, time_available_min: int = 30, mood: str = "") -> list[dict]:
        """
        推荐替代活动。
        
        Args:
            time_available_min: 可用时间（分钟）
            mood: 当前心情描述
        
        Returns:
            推荐活动列表
        """
        suggestions = []
        
        # 根据心情调整推荐
        if any(w in mood for w in ["累", "疲惫", "倦怠", "没劲"]):
            categories = ["身体类", "手工类"]
        elif any(w in mood for w in ["焦虑", "不安", "紧张", "害怕"]):
            categories = ["心智类", "身体类"]
        elif any(w in mood for w in ["孤独", "寂寞", "没人"]):
            categories = ["连接类", "手工类"]
        else:
            categories = list(self.ACTIVITIES.keys())
        
        for cat in categories:
            activities = self.ACTIVITIES.get(cat, [])
            picked = random.sample(activities, min(2, len(activities)))
            for act in picked:
                time_est = 5 if any(w in act for w in ["5分钟", "一件"]) else (
                    20 if "20分钟" in act else 10
                )
                if time_est <= time_available_min:
                    suggestions.append({
                        "category": cat,
                        "activity": act,
                        "time_est_min": time_est,
                    })
        
        random.shuffle(suggestions)
        return suggestions[:4]
    
    def start_session(self, duration_minutes: int = 30) -> DetoxSession:
        """开始一次排毒会话"""
        session = DetoxSession(
            session_id=f"detox-{int(time.time())}",
            start_time=time.time(),
            duration_minutes=duration_minutes,
        )
        self.sessions.append(session)
        return session
    
    def complete_session(self, session_id: str, mood_after: int, activities: list[str]):
        """完成排毒，记录心情变化"""
        for s in self.sessions:
            if s.session_id == session_id:
                s.completed = True
                s.mood_after = mood_after
                s.activities_done = activities
                s.mood_before = s.mood_before or 3
                self.total_detox_minutes += s.duration_minutes
                self._save(s)
                break
    
    def get_stats(self) -> dict:
        """获取排毒统计"""
        completed = [s for s in self.sessions if s.completed]
        return {
            "total_sessions": len(completed),
            "total_minutes": sum(s.duration_minutes for s in completed),
            "avg_mood_change": round(
                sum((s.mood_after - s.mood_before) for s in completed if s.mood_after and s.mood_before)
                / max(len(completed), 1), 1
            ) if completed else 0,
            "streak_days": self._calc_streak(),
            "tip": "每次排毒都是给自己的一个拥抱。不在乎次数，在于每一次都真实。",
        }
    
    # ── 内部方法 ──
    
    def _pick_activities(self, phase: str, minutes: int) -> list[str]:
        """根据阶段和时间选择活动"""
        pool = []
        if phase == "沉浸":
            pool = self.ACTIVITIES["手工类"] + self.ACTIVITIES["心智类"]
        else:
            pool = self.ACTIVITIES["心智类"] + self.ACTIVITIES["连接类"]
        
        num_activities = max(1, minutes // 15)
        return random.sample(pool, min(num_activities, len(pool)))
    
    def _calc_streak(self) -> int:
        """计算连续排毒天数"""
        if not self.sessions:
            return 0
        completed_dates = set()
        for s in self.sessions:
            if s.completed:
                completed_dates.add(time.strftime("%Y-%m-%d", time.localtime(s.start_time)))
        
        today = time.strftime("%Y-%m-%d", time.localtime())
        streak = 0
        check = today
        while check in completed_dates:
            streak += 1
            check = time.strftime("%Y-%m-%d", time.localtime(
                time.mktime(time.strptime(check, "%Y-%m-%d")) - 86400
            ))
        return streak
    
    def _save(self, session: DetoxSession):
        """保存会话记录"""
        record = {
            "id": session.session_id,
            "start": session.start_time,
            "duration": session.duration_minutes,
            "completed": session.completed,
            "mood_after": session.mood_after,
            "activities": session.activities_done,
        }
        with open(DETOX_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    def _load_log(self):
        """加载历史"""
        if not DETOX_LOG.exists():
            return
        try:
            with open(DETOX_LOG, "r", encoding="utf-8") as f:
                for line in f.readlines()[-200:]:
                    try:
                        data = json.loads(line.strip())
                        s = DetoxSession(
                            session_id=data["id"],
                            start_time=data["start"],
                            duration_minutes=data["duration"],
                            completed=data.get("completed", False),
                            mood_after=data.get("mood_after", 0),
                            activities_done=data.get("activities", []),
                        )
                        self.sessions.append(s)
                        if s.completed:
                            self.total_detox_minutes += s.duration_minutes
                    except (json.JSONDecodeError, KeyError):
                        continue
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    detox = DigitalDetox()
    
    print("🧘 数字排毒向导\n")
    
    # 生成离线时间表
    schedule = detox.generate_offline_schedule(duration_hours=2)
    print("📅 离线时间表 (2小时):")
    for block in schedule["blocks"]:
        print(f"  {block['icon']} {block['phase']} ({block['duration_min']}分钟)")
        for act in block["activities"]:
            print(f"      → {act}")
    
    print(f"\n  📏 规则:")
    for rule in schedule["rules"]:
        print(f"      {rule}")
    
    print(f"\n  💡 {schedule['tip']}")
    
    # 替代活动建议
    print(f"\n🎯 替代活动建议:")
    for alt in detox.get_alternatives(30, "有点累"):
        print(f"  [{alt['category']}] {alt['activity']} (~{alt['time_est_min']}分钟)")
    
    # 呼吸训练
    print(f"\n🌬️ 呼吸训练 (共{len(detox.breathing_exercise())}步):")
    for step in detox.breathing_exercise()[:5]:
        print(f"  {step['icon']} {step['instruction']}")
    print(f"  ... 共{len(detox.breathing_exercise())}步，约3分钟")
