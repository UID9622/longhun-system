#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂·降噪盾引擎 v1.0
────────────────────
根据焦虑检测结果，自动生成降噪建议。
所有建议本地生成，不上传云端。

DNA: #龍芯⚡️丙午·乙未·丁酉·丙午·䷨损-MENTAL-IMMUNE-NOISE-SHIELD-v1.0-f2b3c4d5
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import json
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

DATA_DIR = Path.home() / ".龍魂" / "mental_immune"
DATA_DIR.mkdir(parents=True, exist_ok=True)
SHIELD_CONFIG = DATA_DIR / "shield_config.json"
SHIELD_LOG = DATA_DIR / "shield_log.jsonl"


@dataclass
class ShieldRule:
    """降噪规则"""
    id: str
    name: str
    description: str
    category: str           # notification / social / algorithm / habit
    action_type: str        # suggest / auto_block / reminder
    target: str             # 目标（App名/网站/行为）
    anxiety_triggers: list[str]  # 对应的焦虑类型
    enabled: bool = True
    applied_count: int = 0
    last_applied: float = 0.0


@dataclass
class ShieldReport:
    """降噪报告"""
    timestamp: float
    anxiety_score: float
    matched_rules: list[ShieldRule] = field(default_factory=list)
    total_noise_blocked: int = 0
    suggestions: list[dict[str, str]] = field(default_factory=list)


class NoiseShield:
    """
    降噪盾引擎
    
    根据焦虑类型匹配降噪策略：
    - 信息过载 → 通知管理、使用时长限制
    - 社会比较 → 社交媒体屏蔽建议
    - 倦怠 → 节奏调整、休息提醒
    """
    
    # ── 预置降噪规则库 ──
    DEFAULT_RULES = [
        # 信息过载类
        ShieldRule(
            id="notif-mute",
            name="通知静默",
            description="关掉一切非必要App推送通知，只保留电话和短信。",
            category="notification",
            action_type="suggest",
            target="全部App通知",
            anxiety_triggers=["信息过载", "倦怠"],
        ),
        ShieldRule(
            id="screen-limit",
            name="屏幕使用限制",
            description="设定每天手机使用上限，到时间屏幕变灰。",
            category="habit",
            action_type="reminder",
            target="手机屏幕时间",
            anxiety_triggers=["信息过载", "倦怠"],
        ),
        ShieldRule(
            id="focus-hour",
            name="每日专注一小时",
            description="每天固定一个小时的「免打扰时段」，手机放另一个房间。",
            category="habit",
            action_type="suggest",
            target="深度工作时间",
            anxiety_triggers=["信息过载", "迷茫"],
        ),
        # 社会比较类
        ShieldRule(
            id="social-detox",
            name="社交排毒",
            description="暂时隐藏朋友圈入口，取关让你焦虑的账号，取消「推荐」算法。",
            category="social",
            action_type="suggest",
            target="微信/微博/小红书/抖音",
            anxiety_triggers=["比较焦虑", "愤怒"],
        ),
        ShieldRule(
            id="unfollow-anxiety",
            name="取关焦虑源",
            description="列出最近让你感到「不平衡」的账号或群聊，考虑取关或静音。",
            category="social",
            action_type="suggest",
            target="社交媒体关注列表",
            anxiety_triggers=["比较焦虑"],
        ),
        ShieldRule(
            id="stop-comparing",
            name="停止比较打卡",
            description="每当你打开社交媒体，先问自己：我是来放松的，还是来比较的？",
            category="habit",
            action_type="reminder",
            target="社交媒体入口",
            anxiety_triggers=["比较焦虑", "无力"],
        ),
        # 倦怠/疲惫类
        ShieldRule(
            id="rest-reminder",
            name="休息提醒",
            description="每工作45分钟，强制休息5分钟。这5分钟不许看手机。",
            category="notification",
            action_type="reminder",
            target="工作-休息节律",
            anxiety_triggers=["倦怠", "无力"],
        ),
        ShieldRule(
            id="evening-wind-down",
            name="晚间降速",
            description="晚上9点后：屏幕变暖色，只允许读书/听音乐/冥想类App。",
            category="habit",
            action_type="suggest",
            target="晚间作息",
            anxiety_triggers=["倦怠", "失眠", "恐惧"],
        ),
        ShieldRule(
            id="nature-break",
            name="自然接触",
            description="每天至少出门15分钟，不管天气。看天、看树、看云。",
            category="habit",
            action_type="suggest",
            target="户外活动",
            anxiety_triggers=["倦怠", "孤独", "迷茫"],
        ),
        # 愤怒/无力类
        ShieldRule(
            id="rage-journal",
            name="愤怒日记",
            description="写下让你愤怒的事（写完可以不保存）。愤怒是燃料，不是方向盘。",
            category="habit",
            action_type="suggest",
            target="情绪记录",
            anxiety_triggers=["愤怒", "无力"],
        ),
        ShieldRule(
            id="news-diet",
            name="新闻节食",
            description="每天只看一次新闻，看完就关。你不需要知道世界上每件事。",
            category="notification",
            action_type="suggest",
            target="新闻/热搜/头条",
            anxiety_triggers=["愤怒", "恐惧", "信息过载"],
        ),
        # 孤独类
        ShieldRule(
            id="offline-hobby",
            name="线下爱好",
            description="找一个不需要手机也能做的事：画画、弹琴、种花、养鱼。",
            category="habit",
            action_type="suggest",
            target="线下活动",
            anxiety_triggers=["孤独", "迷茫"],
        ),
        ShieldRule(
            id="pack-mentality",
            name="寻找同类",
            description="去一个跟你兴趣相关的小圈子（线下优先）。孤独的反面不是热闹，是同频。",
            category="social",
            action_type="suggest",
            target="兴趣社群",
            anxiety_triggers=["孤独"],
        ),
    ]
    
    def __init__(self):
        self.rules: dict[str, ShieldRule] = {}
        self.applied_history: list[ShieldReport] = []
        self.stats = {
            "total_noise_blocked": 0,
            "rules_applied": {},
            "anxiety_types_addressed": {},
        }
        self._load_config()
        self._load_log()
    
    def assess(self, anxiety_labels: list[str], anxiety_score: float) -> ShieldReport:
        """
        根据焦虑检测结果，匹配降噪规则。
        
        Args:
            anxiety_labels: 焦虑情绪标签列表，如 ["信息过载", "倦怠"]
            anxiety_score: 焦虑指数 0-100
        
        Returns:
            ShieldReport: 匹配的规则和行动建议
        """
        matched_rules = []
        suggestions = []
        
        for rule in self.rules.values():
            if not rule.enabled:
                continue
            
            # 规则是否匹配当前焦虑类型
            trigger_match = any(t in anxiety_labels for t in rule.anxiety_triggers)
            if not trigger_match:
                continue
            
            matched_rules.append(rule)
            
            # 生成具体建议
            suggestions.append({
                "rule_id": rule.id,
                "name": rule.name,
                "description": rule.description,
                "action_type": rule.action_type,
                "target": rule.target,
                "category": rule.category,
            })
            
            # 更新统计
            rule.applied_count += 1
            rule.last_applied = time.time()
            self.stats["rules_applied"][rule.id] = self.stats["rules_applied"].get(rule.id, 0) + 1
        
        # 如果焦虑指数高，额外建议
        if anxiety_score > 60:
            suggestions.append({
                "rule_id": "emergency-shield",
                "name": "🛡️ 紧急降噪盾",
                "description": (
                    "检测到较高的焦虑负荷。建议立刻：\n"
                    "1. 放下手机，放到另一个房间\n"
                    "2. 深呼三口气（吸气4秒，憋住4秒，缓缓呼出6秒）\n"
                    "3. 出门走10分钟，不许带耳机\n"
                    "4. 回来再决定要不要继续看手机"
                ),
                "action_type": "reminder",
                "target": "紧急干预",
                "category": "habit",
            })
        
        report = ShieldReport(
            timestamp=time.time(),
            anxiety_score=anxiety_score,
            matched_rules=[r.id for r in matched_rules],
            total_noise_blocked=len(matched_rules),
            suggestions=suggestions,
        )
        
        self.applied_history.append(report)
        self.stats["total_noise_blocked"] += len(matched_rules)
        for label in anxiety_labels:
            self.stats["anxiety_types_addressed"][label] = (
                self.stats["anxiety_types_addressed"].get(label, 0) + 1
            )
        
        self._save_config()
        self._save_log(report)
        
        return report
    
    def get_active_shields(self) -> list[dict[str, object]]:
        """获取当前激活的所有降噪盾"""
        return [
            {
                "id": r.id,
                "name": r.name,
                "category": r.category,
                "enabled": r.enabled,
                "applied_count": r.applied_count,
            }
            for r in self.rules.values()
            if r.enabled
        ]
    
    def toggle_rule(self, rule_id: str, enabled: Optional[bool] = None) -> bool:
        """开关某个降噪规则"""
        if rule_id not in self.rules:
            return False
        if enabled is None:
            self.rules[rule_id].enabled = not self.rules[rule_id].enabled
        else:
            self.rules[rule_id].enabled = enabled
        self._save_config()
        return True
    
    def get_stats(self) -> dict[str, object]:
        """获取降噪统计"""
        return {
            "total_blocked": self.stats["total_noise_blocked"],
            "top_rules": sorted(
                self.stats["rules_applied"].items(),
                key=lambda x: x[1], reverse=True
            )[:5],
            "top_anxiety_types": sorted(
                self.stats["anxiety_types_addressed"].items(),
                key=lambda x: x[1], reverse=True
            )[:3],
            "active_shields": sum(1 for r in self.rules.values() if r.enabled),
        }
    
    # ── 内部方法 ──
    
    def _load_config(self):
        """加载本地配置"""
        if SHIELD_CONFIG.exists():
            try:
                with open(SHIELD_CONFIG, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for rule_data in data.get("rules", []):
                    rule = ShieldRule(**rule_data)
                    self.rules[rule.id] = rule
                self.stats = data.get("stats", self.stats)
            except (json.JSONDecodeError, TypeError):
                self._reset_rules()
        else:
            self._reset_rules()
    
    def _reset_rules(self):
        """重置为默认规则"""
        self.rules = {r.id: r for r in self.DEFAULT_RULES}
    
    def _save_config(self):
        """保存配置到本地"""
        config = {
            "rules": [
                {
                    "id": r.id, "name": r.name, "description": r.description,
                    "category": r.category, "action_type": r.action_type,
                    "target": r.target, "anxiety_triggers": r.anxiety_triggers,
                    "enabled": r.enabled, "applied_count": r.applied_count,
                    "last_applied": r.last_applied,
                }
                for r in self.rules.values()
            ],
            "stats": self.stats,
            "updated_at": time.time(),
        }
        with open(SHIELD_CONFIG, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def _save_log(self, report: ShieldReport):
        """保存降噪日志"""
        with open(SHIELD_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "ts": report.timestamp,
                "score": report.anxiety_score,
                "rules": report.matched_rules,
                "count": report.total_noise_blocked,
            }, ensure_ascii=False) + "\n")
    
    def _load_log(self):
        """加载历史日志（仅统计用）"""
        if not SHIELD_LOG.exists():
            return
        try:
            with open(SHIELD_LOG, "r", encoding="utf-8") as f:
                for line in f.readlines()[-500:]:
                    try:
                        data = json.loads(line.strip())
                        self.applied_history.append(ShieldReport(
                            timestamp=data["ts"],
                            anxiety_score=data["score"],
                            matched_rules=data.get("rules", []),
                            total_noise_blocked=data.get("count", 0),
                        ))
                    except (json.JSONDecodeError, KeyError):
                        continue
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    shield = NoiseShield()
    
    # 模拟检测
    print("🛡️ 降噪盾引擎 — 诊断\n")
    print(f"激活的盾: {shield.get_stats()['active_shields']} 面")
    print(f"累计降噪: {shield.get_stats()['total_blocked']} 次\n")
    
    # 测试
    report = shield.assess(
        anxiety_labels=["信息过载", "倦怠"],
        anxiety_score=65
    )
    
    print(f"焦虑指数 {report.anxiety_score}/100 → 匹配 {report.total_noise_blocked} 条规则:")
    for s in report.suggestions:
        print(f"  🛡️ [{s['category']}] {s['name']}")
        print(f"     {s['description'][:80]}...")
