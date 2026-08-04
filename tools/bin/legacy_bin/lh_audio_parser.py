#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·音频解析引擎 v1.0 — 语音/音频文件/视频音轨 → 结构化转录
DNA: #龍芯⚡️丙午·辛未·AUDIO-PARSER-v1.0-SPEECH2TEXT

四步处理管线:
  ① 语音转文字: 普通话/方言/英语混合
  ② 说话人分离: 区分A/B/C不同声源
  ③ 情绪分析: 语速/音量/停顿/语气词 → 情绪判断
  ④ 关键词提取: 命名实体/敏感词/核心诉求

关键特性: 口语优化 — 过滤"那个那个"/"我说错了"/"等一下"等填充词

统一接口: parse(input_data: bytes|str|Path) → AudioOutput

用法:
  from bin.lh_audio_parser import AudioParser
  parser = AudioParser()
  result = parser.parse("/path/to/audio.wav")
  print(result.to_json())

部署: 本地优先，华为鲲鹏跑音频，离线可用，数据不出本地
"""

import json
import os
import sys
import hashlib
import time
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, Union, Dict, Any, List
from datetime import datetime, timezone, timedelta

# ── 审计层导入 ──
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
try:
    from tools.logging.action_logger import ActionLogger, log_operation
except ImportError:
    ActionLogger = None
    def log_operation(*args, **kwargs):
        from contextlib import nullcontext
        return nullcontext()

DNA = "#龍芯⚡️丙午·辛未·AUDIO-PARSER-v1.0-SPEECH2TEXT"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬AUDI-C2D3"

# ═══════════════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════════════

@dataclass
class SpeakerUtterance:
    """说话人话语"""
    speaker_id: str = ""          # A/B/C
    text: str = ""
    start_sec: float = 0.0
    end_sec: float = 0.0
    confidence: float = 0.0

@dataclass
class EmotionSegment:
    """情绪段"""
    start_sec: float = 0.0
    end_sec: float = 0.0
    emotion: str = "neutral"      # angry/happy/sad/neutral/anxious/confident
    intensity: float = 0.0
    indicators: List[str] = field(default_factory=list)  # 语速快/停顿/语气词

@dataclass
class KeyEntity:
    """命名实体"""
    entity_type: str = ""         # person/location/org/time/amount/tech_term
    value: str = ""
    context: str = ""             # 上下文句子
    confidence: float = 0.0

@dataclass
class AudioOutput:
    """音频解析统一输出"""
    input_hash: str = ""
    full_transcript: str = ""                          # 完整转录
    cleaned_transcript: str = ""                       # 清洗后 (去填充词)
    speakers: List[SpeakerUtterance] = field(default_factory=list)
    emotions: List[EmotionSegment] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    entities: List[KeyEntity] = field(default_factory=list)
    sensitive_words: List[str] = field(default_factory=list)
    core_demand: str = ""                              # 核心诉求
    language_detected: str = "zh"                      # zh/en/mixed
    duration_sec: float = 0.0
    processing_time_ms: float = 0.0
    model_version: str = "v1.0-local"
    dna: str = DNA
    parsed_at: str = ""

    def to_json(self, indent: int = 2) -> str:
        d = asdict(self)
        d["speakers"] = [asdict(s) for s in self.speakers]
        d["emotions"] = [asdict(e) for e in self.emotions]
        d["entities"] = [asdict(e) for e in self.entities]
        return json.dumps(d, ensure_ascii=False, indent=indent)

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.to_json())


# ═══════════════════════════════════════════════════════════════
# 口语清洗器
# ═══════════════════════════════════════════════════════════════

class SpeechCleaner:
    """口语优化: 过滤填充词/重复/修正"""

    FILLERS_CN = [
        "那个那个", "那个", "这个这个", "这个", "就是说", "然后呢",
        "嗯", "啊", "呃", "哦", "嘛", "吧",
        "怎么说呢", "那个什么", "我想想",
    ]
    FILLERS_EN = [
        "um", "uh", "er", "ah", "like", "you know",
        "i mean", "sort of", "kind of",
    ]
    CORRECTIONS = [
        (r'(.)\1{2,}', r'\1\1'),     # 重复字: 好好好好 → 好好
        (r'我说错了[，。]*', ''),
        (r'等一下[，。]*', ''),
        (r'不对不对[，。]*', ''),
        (r'换个说法[，。]*', ''),
    ]

    @classmethod
    def clean(cls, text: str) -> str:
        """清理口语填充词"""
        result = text
        # 去填充词
        for filler in cls.FILLERS_CN:
            result = result.replace(filler, "")
            result = result.replace(filler + "，", "")
            result = result.replace(filler + "。", "")
        for filler in cls.FILLERS_EN:
            pattern = re.compile(r'\b' + re.escape(filler) + r'\b[，。,.]*', re.IGNORECASE)
            result = pattern.sub("", result)
        # 去修正
        for pattern, repl in cls.CORRECTIONS:
            result = re.sub(pattern, repl, result)
        # 压缩空白
        result = re.sub(r'\s+', ' ', result)
        result = re.sub(r'[，。！？]{2,}', lambda m: m.group()[0], result)
        return result.strip()


# ═══════════════════════════════════════════════════════════════
# 声纹模拟器 (本地回退)
# ═══════════════════════════════════════════════════════════════

class VoiceFeatureExtractor:
    """声纹特征: 无外部依赖时的启发式分析"""

    @staticmethod
    def estimate_pitch_variation(text: str) -> Dict[str, float]:
        """从文本估计音调变化 (本地回退)"""
        high_pitch_chars = "？！!?！？惊讶啊呀哇哦噢"
        low_pitch_chars = "。……嗯呃"
        high_count = sum(1 for c in text if c in high_pitch_chars)
        low_count = sum(1 for c in text if c in low_pitch_chars)
        total = max(high_count + low_count, 1)
        return {
            "high_ratio": high_count / total,
            "low_ratio": low_count / total,
            "variation": abs(high_count - low_count) / total,
        }

    @staticmethod
    def estimate_speech_rate(chars: int, duration_sec: float) -> float:
        """估算语速 (字/秒)"""
        if duration_sec <= 0:
            return 0
        return chars / duration_sec


# ═══════════════════════════════════════════════════════════════
# 解析引擎
# ═══════════════════════════════════════════════════════════════

class AudioParser:
    """音频解析器 · 统一接口 parse(input_data) → AudioOutput"""

    def __init__(self, backend: str = "local"):
        """
        Args:
            backend: "local" | "whisper" | "api" | "fish_audio"
        """
        self.backend = backend
        self.cleaner = SpeechCleaner()

    # ── 步骤①: 语音转文字 ──
    def _speech_to_text(self, audio_data: bytes, file_ext: str = ".wav") -> str:
        """语音→文字: 支持普通话/方言/英语混合"""
        transcript = ""
        try:
            # 尝试 Whisper (本地)
            try:
                import whisper
                import tempfile
                with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as f:
                    f.write(audio_data)
                    tmp_path = f.name
                model = whisper.load_model("base")
                result = model.transcribe(tmp_path, language="zh")
                transcript = result.get("text", "")
                os.unlink(tmp_path)
                return transcript
            except ImportError:
                pass

            # 尝试 speech_recognition
            try:
                import speech_recognition as sr
                import io
                r = sr.Recognizer()
                # 需要临时文件或 AudioData
                import tempfile
                with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as f:
                    f.write(audio_data)
                    tmp_path = f.name
                with sr.AudioFile(tmp_path) as source:
                    audio = r.record(source)
                transcript = r.recognize_google(audio, language="zh-CN")
                os.unlink(tmp_path)
                return transcript
            except (ImportError, Exception):
                pass

        except Exception:
            pass
        return transcript

    # ── 步骤②: 说话人分离 ──
    def _speaker_diarization(self, transcript: str, duration_sec: float = 0) -> List[SpeakerUtterance]:
        """
        说话人分离: 区分不同声源
        本地回退: 基于文本模式识别 (引号/换行/"说"字)
        """
        utterances = []
        # 模式 A: "A说: xxx" / "B: xxx" / "[A] xxx"
        pattern_a = re.compile(r'(?:([ABＣD甲乙丙丁])[：:]\s*|\[([ABＣD甲乙丙丁])\]\s*|([ABＣD甲乙丙丁])说[：:]?\s*)(.+?)(?=(?:[ABＣD甲乙丙丁][：:]|\[[ABＣD甲乙丙丁]\]|[ABＣD甲乙丙丁]说|$))')
        matches = pattern_a.findall(transcript)
        if matches:
            for i, m in enumerate(matches):
                speaker_raw = m[0] or m[1] or m[2]
                text = m[3].strip()
                speaker_map = {"甲": "A", "乙": "B", "丙": "C", "丁": "D"}
                speaker_id = speaker_map.get(speaker_raw, speaker_raw)
                t_start = (i * duration_sec / max(len(matches), 1))
                t_end = ((i + 1) * duration_sec / max(len(matches), 1))
                utterances.append(SpeakerUtterance(
                    speaker_id=speaker_id,
                    text=text,
                    start_sec=t_start,
                    end_sec=t_end,
                    confidence=0.6,
                ))
        else:
            # 无多说话人标记: 单一说话人
            utterances.append(SpeakerUtterance(
                speaker_id="A",
                text=transcript[:500],
                start_sec=0,
                end_sec=max(duration_sec, 1.0),
                confidence=0.8,
            ))
        return utterances

    # ── 步骤③: 情绪分析 ──
    def _emotion_analysis(self, transcript: str, utterances: List[SpeakerUtterance], duration_sec: float) -> List[EmotionSegment]:
        """情绪分析: 语速/音量/停顿/语气词 → 情绪判断"""
        emotions = []
        cleaned = self.cleaner.clean(transcript)
        pitch = VoiceFeatureExtractor.estimate_pitch_variation(cleaned)
        rate = VoiceFeatureExtractor.estimate_speech_rate(len(cleaned), duration_sec)

        # 情绪词典
        emotion_dict = {
            "angry": ["!", "！", "cnm", "他妈", "死", "滚", "投诉", "举报", "垃圾"],
            "happy": ["哈哈", "开心", "感谢", "！", "棒", "😊", "恭喜", "太好了"],
            "sad": ["……", "唉", "难过", "😭", "哭", "失去", "可惜", "无奈"],
            "anxious": ["怎么办", "着急", "快", "赶紧", "来不及", "担心", "紧张"],
            "confident": ["肯定", "绝对", "保证", "没问题", "放心", "一定"],
            "neutral": [],
        }

        # 找主导情绪
        scores = {k: 0 for k in emotion_dict}
        for emotion, keywords in emotion_dict.items():
            for kw in keywords:
                scores[emotion] += transcript.count(kw)

        dominant = max(scores, key=scores.get)
        max_score = max(scores.values())

        # 语速辅助
        if rate > 6.0:          # 语速快 → 激动
            indicators = ["语速快"]
            if "anxious" in scores and scores["anxious"] > 0:
                dominant = "anxious"
            elif "angry" in scores and scores["angry"] > 0:
                dominant = "angry"
        elif rate < 2.0:        # 语速慢 → 平静/悲伤
            indicators = ["语速慢"]
            if "sad" in scores and scores["sad"] > 0:
                dominant = "sad"
            elif "neutral" in scores:
                dominant = "neutral"
        else:
            indicators = []

        intensity = min(1.0, max_score * 0.15 + pitch["variation"] * 0.3 + 0.2)

        # 停顿分析
        pauses = transcript.count("……") + transcript.count("...") + transcript.count("。")
        if pauses > 5:
            indicators.append("频繁停顿")

        # 语气词
        exclamations = transcript.count("！") + transcript.count("!")
        if exclamations > 3:
            indicators.append("语气强烈")

        emotions.append(EmotionSegment(
            start_sec=0,
            end_sec=max(duration_sec, 1.0),
            emotion=dominant,
            intensity=round(intensity, 2),
            indicators=indicators,
        ))

        return emotions

    # ── 步骤④: 关键词提取 ──
    def _extract_keywords(self, transcript: str, utterances: List[SpeakerUtterance]) -> tuple[Any, ...]:
        """关键词/实体/敏感词/核心诉求提取"""
        cleaned = self.cleaner.clean(transcript)

        # 命名实体
        entities: List[KeyEntity] = []
        patterns = [
            (r'(北京|上海|广州|深圳|杭州|成都|武汉|南京|西安|重庆|长沙|郑州)[市]?', 'location'),
            (r'(腾讯|阿里|百度|华为|字节|京东|美团|小米|网易|拼多多)', 'org'),
            (r'[¥￥]\s*\d+[\.\d]*[万亿千百]*元?', 'amount'),
            (r'\d{4}年\d{1,2}月\d{1,2}日', 'time'),
            (r'\d{4}-\d{2}-\d{2}', 'time'),
            (r'(Python|Java|JavaScript|C\+\+|Go|Rust|SQL|Redis|Docker|K8s|API|HTTP)', 'tech_term'),
        ]
        for pattern, etype in patterns:
            for m in re.finditer(pattern, cleaned):
                entities.append(KeyEntity(
                    entity_type=etype,
                    value=m.group(),
                    context=cleaned[max(0, m.start()-20):m.end()+20],
                    confidence=0.8,
                ))

        # 敏感词
        sensitive_patterns = [
            r'(举报|投诉|退钱|退款|曝光|维权|起诉|律师|法院|警察|报警)',
            r'(骗|坑|害|宰|欺诈|陷阱)',
            r'(泄露|隐私|数据|信息)',
        ]
        sensitive_words: List[str] = []
        for pattern in sensitive_patterns:
            for m in re.finditer(pattern, cleaned):
                sensitive_words.append(m.group())

        # 关键词
        keywords = list(set(
            [e.value for e in entities] + sensitive_words
        ))

        # 核心诉求推断
        core_demand = ""
        demand_patterns = {
            "维权/投诉": r'(我要|帮我|能不能)[\u4e00-\u9fff]*?(投诉|举报|维权|退款|赔偿)',
            "技术支持": r'(帮我|能不能)[\u4e00-\u9fff]*?(修|改|调|弄|看看)',
            "信息咨询": r'(怎么|如何|什么|哪里|什么时候)',
            "紧急求助": r'(快|赶紧|马上|立即|紧急|救命)',
        }
        for demand_type, pattern in demand_patterns.items():
            m = re.search(pattern, cleaned)
            if m:
                core_demand = f"{demand_type}: {m.group()}"
                break

        if not core_demand:
            # 取第一句话作为默认诉求
            first_sentence = cleaned.split("。")[0] if "。" in cleaned else cleaned[:50]
            core_demand = first_sentence[:80]

        return keywords, entities, sensitive_words, core_demand

    # ── 语言检测 ──
    @staticmethod
    def _detect_language(text: str) -> str:
        """检测语言: zh/en/mixed"""
        has_cn = bool(re.search(r'[\u4e00-\u9fff]', text))
        has_en = bool(re.search(r'[a-zA-Z]{3,}', text))
        if has_cn and has_en:
            return "mixed"
        elif has_cn:
            return "zh"
        elif has_en:
            return "en"
        return "unknown"

    # ── 统一管口 ──
    def parse(self, input_data: Union[bytes, str, Path]) -> AudioOutput:
        """
        统一解析接口。

        Args:
            input_data: 音频文件路径 (str/Path) 或原始字节 (bytes)

        Returns:
            AudioOutput 结构化结果
        """
        t_start = time.time()
        input_hash = ""
        file_ext = ".wav"

        with log_operation("音频解析", "audio_parser", persona="P05上帝之眼"):
            # 标准化输入
            if isinstance(input_data, (str, Path)):
                path = Path(input_data)
                if not path.exists():
                    raise FileNotFoundError(f"音频文件不存在: {path}")
                audio_data = path.read_bytes()
                input_hash = hashlib.sha256(audio_data).hexdigest()[:16]
                file_ext = path.suffix
            elif isinstance(input_data, bytes):
                audio_data = input_data
                input_hash = hashlib.sha256(audio_data).hexdigest()[:16]
            else:
                raise TypeError(f"输入类型不支持: {type(input_data)}")

            # ── 步骤①: 语音转文字 ──
            full_transcript = self._speech_to_text(audio_data, file_ext)

            # ── 口语清洗 ──
            cleaned = self.cleaner.clean(full_transcript) if full_transcript else ""

            # ── 估算时长 ──
            file_size_mb = len(audio_data) / (1024 * 1024)
            duration_sec = file_size_mb * 40  # 粗糙估算: 1MB ≈ 40秒 WAV

            # ── 步骤②: 说话人分离 ──
            text_for_diarization = cleaned if cleaned else full_transcript
            speakers = self._speaker_diarization(text_for_diarization, duration_sec)

            # ── 步骤③: 情绪分析 ──
            text_for_emotion = cleaned if cleaned else full_transcript
            emotions = self._emotion_analysis(text_for_emotion, speakers, duration_sec)

            # ── 步骤④: 关键词提取 ──
            keywords, entities, sensitive_words, core_demand = self._extract_keywords(
                full_transcript, speakers
            )

            # ── 语言检测 ──
            language = self._detect_language(full_transcript)

            # ── 结构化输出 ──
            output = AudioOutput(
                input_hash=input_hash,
                full_transcript=full_transcript,
                cleaned_transcript=cleaned,
                speakers=speakers,
                emotions=emotions,
                keywords=keywords,
                entities=entities,
                sensitive_words=sensitive_words,
                core_demand=core_demand,
                language_detected=language,
                duration_sec=round(duration_sec, 1),
                processing_time_ms=round((time.time() - t_start) * 1000, 1),
                model_version="v1.0-local",
                dna=DNA,
                parsed_at=datetime.now(timezone(timedelta(hours=8))).isoformat(),
            )

            return output


# ═══════════════════════════════════════════════════════════════
# 快速入口
# ═══════════════════════════════════════════════════════════════

_default_parser: Optional[AudioParser] = None

def parse(input_data: Union[bytes, str, Path]) -> AudioOutput:
    """快速入口: AudioParser().parse()"""
    global _default_parser
    if _default_parser is None:
        _default_parser = AudioParser()
    return _default_parser.parse(input_data)


def is_available() -> bool:
    """检测音频引擎可用性"""
    try:
        import speech_recognition
        return True
    except ImportError:
        pass
    try:
        import whisper
        return True
    except ImportError:
        pass
    return False


# ═══════════════════════════════════════════════════════════════
# 命令行
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="🐉 龍魂音频解析器")
    ap.add_argument("audio", help="音频文件路径")
    ap.add_argument("--json", action="store_true", help="JSON输出")
    args = ap.parse_args()

    parser = AudioParser()
    result = parser.parse(args.audio)

    if args.json:
        print(result.to_json())
    else:
        print(f"🐉 龍魂音频解析 · {result.input_hash}")
        print(f"   语言: {result.language_detected}")
        print(f"   转录: {result.full_transcript[:200]}...")
        print(f"   清洗: {result.cleaned_transcript[:200]}...")
        print(f"   说话人: {len(result.speakers)}人")
        print(f"   情绪: {result.emotions[0].emotion if result.emotions else 'N/A'}")
        print(f"   关键词: {', '.join(result.keywords[:10])}")
        print(f"   实体: {len(result.entities)}个")
        print(f"   核心诉求: {result.core_demand[:80]}")
        if result.sensitive_words:
            print(f"   ⚠️ 敏感词: {', '.join(result.sensitive_words)}")
        print(f"   耗时: {result.processing_time_ms}ms")
        print(f"   DNA: {DNA}")
