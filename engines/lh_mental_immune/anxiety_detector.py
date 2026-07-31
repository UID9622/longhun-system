# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂·精神体温计 — 焦虑检测引擎 v1.0
──────────────────────────────────
本地分析用户输入文字，输出焦虑指数(0-100)和情绪标签。
铁律：纯本地运行，数据不出设备，不评判任何情绪。

DNA: #龍芯⚡️丙午·乙未·丁酉·MENTAL-IMMUNE-ANXIETY-DETECTOR-v1.0-e8f1a2c3
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import re
import json
import hashlib
import time
from pathlib import Path
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Optional

# ═══════════════════════════════════════════════════
# 数据目录 — 纯本地，用户主目录下
# ═══════════════════════════════════════════════════
DATA_DIR = Path.home() / ".龍魂" / "mental_immune"
DATA_DIR.mkdir(parents=True, exist_ok=True)
ANXIETY_LOG = DATA_DIR / "anxiety_log.jsonl"


@dataclass
class EmotionLabel:
    """情绪标签 — 描述而非评判"""
    name: str          # e.g. "愤怒", "无力", "恐惧", "孤独"
    category: str      # primary / secondary
    intensity: float   # 0.0-1.0
    description: str   # 人话解释


@dataclass
class AnxietyReport:
    """焦虑检测报告"""
    timestamp: float
    score: float                    # 0-100 焦虑指数
    labels: list[EmotionLabel] = field(default_factory=list)  # EmotionLabel 列表
    word_count: int = 0
    key_triggers: list[str] = field(default_factory=list)  # 触发关键词
    suggestion: str = ""
    hash_fingerprint: str = ""      # 内容哈希，不存原文


class AnxietyDetector:
    """
    精神体温计 — 焦虑检测引擎
    
    三层检测：
    L1 关键词匹配 → 快速初筛
    L2 句式分析 → 焦虑句式模式识别
    L3 语义倾向 → 整体情绪方向计算
    
    铁律：
    - 只在本地运行
    - 只存哈希指纹，不存原文
    - 不给情绪贴"好/坏"标签
    - 检测结果完全在用户控制下
    """
    
    # ── L1: 关键词库（按情绪分类） ──
    EMOTION_KEYWORDS = {
        "愤怒": [
            "气死", "火大", "受不了", "欺负", "不公平", "凭什么",
            "骂", "操", "滚", "恶心", "过分", "忍无可忍", "欺人太甚",
            "愤怒", "生气", "发火", "暴躁", "想打人", "憋屈"
        ],
        "无力": [
            "没办法", "算了", "认命", "改变不了", "就这样吧",
            "无能为力", "绝望", "放弃", "认输", "无力", "没希望",
            "走投无路", "束手无策", "有心无力", "随它去",
            "被开除", "失业", "找不到工作", "面试失败",
            "房租都", "交不起", "活不下去", "没活路"
        ],
        "恐惧": [
            "害怕", "担心", "不敢", "焦虑", "紧张", "不安",
            "吓", "怕", "慌", "忐忑", "胆战心惊", "提心吊胆",
            "失眠", "睡不着", "噩梦", "惶恐", "没安全感",
            "养不起", "还不起", "付不起", "撑不过"
        ],
        "孤独": [
            "一个人", "没人理解", "孤单", "寂寞", "没人说",
            "独来独往", "被孤立", "被遗忘", "冷漠", "无视",
            "形单影只", "格格不入", "融不进去", "没人关心"
        ],
        "迷茫": [
            "不知道怎么办", "没方向", "困惑", "迷路", "前途",
            "不知所措", "看不清", "走哪条路", "怎么选", "无解",
            "没出路", "瓶颈", "困境", "十字路口", "原地踏步",
            "看不到未来", "看不到希望", "没奔头", "出路在哪",
            "何去何从", "活着有什么意义", "人生无望"
        ],
        "倦怠": [
            "累", "疲惫", "没劲", "不想动", "没精神", "躺平",
            "卷不动", "麻木", "厌倦", "乏味", "无聊", "没意思",
            "行尸走肉", "得过且过", "机械", "空心", "耗光",
            "没电", "筋疲力尽", "透支", "被掏空", "燃烧殆尽",
            "撑不住", "扛不住", "想歇", "吃不消"
        ],
        "比较焦虑": [
            "别人都", "比不上", "落后", "赶不上", "同龄人",
            "同学都", "同事都", "朋友圈", "差距", "不如",
            "被比下去", "拉下", "掉队", "人家都"
        ],
        "信息过载": [
            "刷不完", "看不完", "消息太多", "通知太多", "信息爆炸",
            "应接不暇", "眼花缭乱", "推送", "公众号99+", "红点",
            "未读", "刷手机", "停不下来", "手机长手上"
        ],
    }
    
    # ── L2: 焦虑句式模式 ──
    ANXIETY_PATTERNS = [
        # 极端化表述
        (r"(永远|从来|一直|总是|每次|一辈子).{0,10}(不|没|无)", 8, "极端化"),
        (r"(再也|绝对|一定|肯定|百分之百)", 6, "绝对化"),
        # 无力句式
        (r"(算了|随便|反正|无所谓).{0,5}吧", 7, "放弃型"),
        (r"没办法.{0,10}(只能|只好|不得不)", 7, "被迫型"),
        # 灾难化
        (r"(完蛋|毁了|全完了|糟了|死定了|没救了)", 12, "灾难化"),
        (r"(怎么办|怎么办啊|该咋办|咋办)", 9, "恐慌疑问"),
        # 社会比较
        (r"(别人|人家|他们).{0,8}(都|已经|早就)", 8, "比较型"),
        (r"(为什么|为啥|凭什么).{0,10}(就我|只有我|偏偏我|是我)", 10, "不公平型"),
        # 自我否定
        (r"(我不行|我做不到|我太差|我没用|我真废|我真|废物)", 12, "自我否定"),
        (r"(后悔|早知道|当初).{0,10}就好了", 6, "反刍型"),
        # 未来担忧
        (r"(以后|将来|未来|老了).{0,10}(怎么办|咋办|怎么办啊)", 10, "未来恐惧"),
        # 极端表达
        (r"(死了算了|不想活|活不下去|活够|去死)", 18, "极端危机"),
        (r"(房租|工资|钱|账单|贷款|欠债).{0,8}(交不起|还不起|不够|付不起|还不上)", 10, "经济恐慌"),
    ]
    
    # ── L3: 缓冲词（降低误判） ──
    BUFFER_WORDS = [
        "但是", "不过", "还好", "至少", "幸运", "也算",
        "没关系", "慢慢来", "总会", "相信", "加油", "坚持",
        "希望", "可能", "也许", "说不定", "万一"
    ]
    
    def __init__(self):
        self.history: list[AnxietyReport] = []
        self._load_history()
    
    def detect(self, text: str) -> AnxietyReport:
        """
        分析一段文本，返回焦虑报告。
        
        Args:
            text: 用户输入的文字（日记/聊天记录/心声等）
        
        Returns:
            AnxietyReport: 包含焦虑指数、情绪标签、建议
        """
        if not text or not text.strip():
            return AnxietyReport(
                timestamp=time.time(),
                score=0.0,
                labels=[],
                word_count=0,
                key_triggers=[],
                suggestion="",
            )
        
        text = text.strip()
        word_count = len(text)
        
        # ── L1: 关键词检测 ──
        emotion_hits = {}
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            hits = []
            for kw in keywords:
                if kw in text:
                    hits.append(kw)
            if hits:
                emotion_hits[emotion] = hits
        
        # ── L2: 句式模式检测 ──
        pattern_scores = []
        for pattern, weight, pattern_type in self.ANXIETY_PATTERNS:
            matches = re.findall(pattern, text)
            if matches:
                pattern_scores.append((weight, pattern_type, len(matches)))
        
        # ── L3: 情绪倾向计算 ──
        total_kw_hits = sum(len(v) for v in emotion_hits.values())
        total_pattern_weight = sum(w * c for w, _, c in pattern_scores)
        
        # 缓冲词检测 — 降低焦虑指数
        buffer_count = sum(1 for bw in self.BUFFER_WORDS if bw in text)
        
        # 焦虑指数计算（0-100）
        # 关键词贡献 + 句式贡献，缓冲词打折
        # 短文本情绪密度更高——一条微博几十字可以承载巨大的情绪
        if word_count < 100:
            density_factor = 1.0 + (100 - word_count) / 100 * 0.5  # 短文1.0~1.5
        elif word_count < 500:
            density_factor = 1.0
        else:
            density_factor = max(0.6, 500 / word_count)  # 长文略微稀释
        kw_score = min(total_kw_hits * 6 * density_factor, 50)
        pattern_score = min(total_pattern_weight * 1.5, 40)
        base_score = kw_score + pattern_score
        
        # 缓冲词降低 15% 每词（最多降50%）
        buffer_discount = max(0.5, 1.0 - buffer_count * 0.15)
        score = min(base_score * buffer_discount, 100.0)
        
        # ── 生成情绪标签 ──
        labels = []
        for emotion, hits in emotion_hits.items():
            intensity = min(len(hits) / max(len(self.EMOTION_KEYWORDS[emotion]), 1) * 1.5, 1.0)
            # 匹配越多关键词 + 句式命中 → 强度越高
            if emotion in ["愤怒", "无力", "恐惧"] and any(pt == "灾难化" for _, pt, _ in pattern_scores):
                intensity = min(intensity * 1.3, 1.0)
            
            labels.append(EmotionLabel(
                name=emotion,
                category="primary" if intensity > 0.4 else "secondary",
                intensity=round(intensity, 2),
                description=self._label_description(emotion, intensity),
            ))
        
        # 按强度排序
        labels.sort(key=lambda x: x.intensity, reverse=True)
        
        # ── 生成建议 ──
        suggestion = self._generate_suggestion(score, labels)
        
        # ── 生成哈希指纹（存指纹不存原文） ──
        fingerprint = hashlib.sha256(
            f"{text[:50]}{word_count}{score}{time.time()}".encode()
        ).hexdigest()[:16]
        
        # 收集触发词
        all_triggers = []
        for hits in emotion_hits.values():
            all_triggers.extend(hits)
        
        report = AnxietyReport(
            timestamp=time.time(),
            score=round(score, 1),
            labels=labels,
            word_count=word_count,
            key_triggers=all_triggers[:8],  # 最多保留8个触发词
            suggestion=suggestion,
            hash_fingerprint=fingerprint,
        )
        
        # 保存到本地日志（只存哈希，不存原文）
        self._save_report(report)
        self.history.append(report)
        
        return report
    
    def get_timeline(self, days: int = 7) -> list[dict[str, object]]:
        """获取近N天的情绪波动数据"""
        cutoff = time.time() - days * 86400
        recent = [r for r in self.history if r.timestamp >= cutoff]
        
        # 按天聚合
        daily = defaultdict(list)
        for r in recent:
            day = time.strftime("%Y-%m-%d", time.localtime(r.timestamp))
            daily[day].append(r.score)
        
        timeline = []
        for day in sorted(daily.keys()):
            scores = daily[day]
            timeline.append({
                "date": day,
                "avg_score": round(sum(scores) / len(scores), 1),
                "max_score": round(max(scores), 1),
                "min_score": round(min(scores), 1),
                "count": len(scores),
            })
        
        return timeline
    
    def get_emotion_summary(self, days: int = 7) -> dict[str, object]:
        """获取近期情绪分布摘要"""
        cutoff = time.time() - days * 86400
        recent = [r for r in self.history if r.timestamp >= cutoff]
        
        emotion_counts = Counter()
        for r in recent:
            for label in r.labels:
                if label.category == "primary":
                    emotion_counts[label.name] += 1
        
        total = sum(emotion_counts.values()) or 1
        return {
            "period_days": days,
            "total_detections": len(recent),
            "dominant_emotion": emotion_counts.most_common(1)[0][0] if emotion_counts else "平静",
            "emotion_distribution": {
                e: round(c / total * 100, 1) for e, c in emotion_counts.most_common()
            },
        }
    
    # ── 内部方法 ──
    
    def _label_description(self, emotion: str, intensity: float) -> str:
        """为每个情绪标签生成人话解释"""
        descriptions = {
            "愤怒": "对不公的本能反应，说明你心中有正义",
            "无力": "面对超出控制范围的事，不是你的错",
            "恐惧": "对未知的警觉，是人类最古老的保护机制",
            "孤独": "灵魂需要同频共振，不是你不够好",
            "迷茫": "在找方向的人，才会感到迷茫——这说明你在思考",
            "倦怠": "身体在告诉你：该休息了，不是偷懒",
            "比较焦虑": "看到别人的路，忘了自己的步伐——每个人有自己的时区",
            "信息过载": "不是你的注意力差，是这个时代太吵了",
        }
        return descriptions.get(emotion, "情绪是信号，不是罪")
    
    def _generate_suggestion(self, score: float, labels: list[EmotionLabel]) -> str:
        """根据焦虑指数和标签生成建议"""
        if score < 20:
            return "状态平稳。保持你现在的节奏就好。"
        elif score < 40:
            return "有些许波动，属于正常范围。可以考虑出门走十分钟。"
        elif score < 60:
            top_label = labels[0].name if labels else ""
            suggestions = {
                "信息过载": "建议关闭非必要App通知，设置每天1小时的「无屏幕时间」。",
                "比较焦虑": "别人的朋友圈是精选集，你的人生是完整版。建议暂时减少社交媒体浏览。",
                "无力": "把关注点从「控制不了的事」转移到「能做的下一件小事」。",
                "倦怠": "身体在求救。今天先别想那么多，好好睡一觉。",
                "愤怒": "愤怒是信号不是终点。试着写下让你愤怒的事，写出来就不那么重了。",
                "孤独": "不是你孤僻，是你还没遇到同频的人。去做一件你真正喜欢的事，同类自然会出现。",
                "迷茫": "站在十字路口的人才有资格选择方向。给自己三天时间，什么都不决定。",
                "恐惧": "恐惧是保护你的哨兵。问自己：最坏的结果是什么？它真的会发生吗？",
            }
            base = suggestions.get(top_label, "心情有些沉重。试着深呼吸三次。")
            return base
        elif score < 80:
            return "今天的情绪负荷比较重。建议启动「数字排毒」：放下手机，出门走30分钟，不思考任何问题。"
        else:
            return "警报：情绪达到了一个高点。这很正常，但你不需要独自扛着。向一个你信任的人说一句话，就一句。如果暂时没人可说，写在纸上，写完撕掉。"
    
    def _save_report(self, report: AnxietyReport):
        """保存报告到本地日志（不存原文）"""
        record = {
            "ts": report.timestamp,
            "score": report.score,
            "labels": [
                {"name": l.name, "intensity": l.intensity, "category": l.category}
                for l in report.labels
            ],
            "word_count": report.word_count,
            "triggers": report.key_triggers,
            "fingerprint": report.hash_fingerprint,
        }
        with open(ANXIETY_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    def _load_history(self):
        """加载历史记录"""
        if not ANXIETY_LOG.exists():
            return
        # 只加载最近1000条
        with open(ANXIETY_LOG, "r", encoding="utf-8") as f:
            lines = f.readlines()[-1000:]
        
        for line in lines:
            try:
                data = json.loads(line.strip())
                labels = [
                    EmotionLabel(
                        name=l["name"],
                        category=l.get("category", "primary"),
                        intensity=l["intensity"],
                        description="",
                    )
                    for l in data.get("labels", [])
                ]
                self.history.append(AnxietyReport(
                    timestamp=data["ts"],
                    score=data["score"],
                    labels=labels,
                    word_count=data.get("word_count", 0),
                    key_triggers=data.get("triggers", []),
                    suggestion="",
                    hash_fingerprint=data.get("fingerprint", ""),
                ))
            except (json.JSONDecodeError, KeyError):
                continue


# ── 命令行入口 ──
if __name__ == "__main__":
    import sys
    
    detector = AnxietyDetector()
    
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        report = detector.detect(text)
        
        print(f"\n{'='*50}")
        print(f"  精神体温计 — 焦虑检测报告")
        print(f"{'='*50}")
        print(f"  焦虑指数: {report.score}/100")
        print(f"  文字长度: {report.word_count}字")
        print(f"  触发词:   {', '.join(report.key_triggers[:5]) if report.key_triggers else '无'}")
        print(f"\n  情绪标签:")
        for label in report.labels:
            bar = "█" * int(label.intensity * 20) + "░" * (20 - int(label.intensity * 20))
            print(f"    [{bar}] {label.name} ({label.intensity:.0%})")
            print(f"           {label.description}")
        
        print(f"\n  💡 {report.suggestion}")
        print(f"{'='*50}\n")
    else:
        print("用法: python3 anxiety_detector.py <要分析的文本>")
        print("示例: python3 anxiety_detector.py 今天又被老板骂了，感觉自己什么都做不好")
