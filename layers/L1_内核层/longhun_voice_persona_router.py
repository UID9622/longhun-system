#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
龍魂通心语 · 多人格音色路由桥 v1.0
LongHun TongXin-Voice · Multi-Persona Voice Router Bridge

功能：
  1. 将龍魂 IPA 人格系统映射到 TTS 音色库
  2. 人格→音色自动路由（IPA-ROUTE → Voice Profile → TTS Engine）
  3. 多人格音色配置管理 (P05/P72/P03/P00/宝宝/云间)
  4. 通心译术语表联动（人名/术语自动调音色）
  5. 与 voice_twin_server.py / 龍魂语音合成器 双向对接

核心理念：人格即音色。每个P系列人格有专属的声纹配置。
路由链:  用户输入 ≈IPARoute≈> 人格判定 ≈VoiceRouter≈> 音色选择 ≈EngineRouter≈> TTS引擎

DNA: #龍芯⚡️丙午·乙未·甲寅·亥时-VOICE-PERSONA-ROUTER-37357AB4
创始人: UID9622 · 龍芯北辰 · 诸葛鑫
"""

import json
import hashlib
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field

# ══════════════════════════════════════════════════════
# 配置路径
# ══════════════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent
VOICE_PROFILE_PATH = ROOT / "L1_内核层" / "voice_persona_profiles.json"
ROUTE_LOG_PATH = Path.home() / "．龍魂" / "voice_route_log.jsonl"
ROUTE_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# ══════════════════════════════════════════════════════
# 数据结构
# ══════════════════════════════════════════════════════

class VoiceEngine(Enum):
    """TTS 引擎"""
    XTTS_V2 = "xtts_v2"       # 本地真声克隆（最高质量）
    FISH_AUDIO = "fish_audio" # 云端真声克隆
    EDGE_TTS = "edge_tts"     # 微软 Edge TTS（在线标准）
    PYTTSX3 = "pyttsx3"       # 本地离线（质量一般）
    ESPEAK = "espeak"         # 备用离线
    MAC_SAY = "mac_say"       # macOS 系统 TTS


class PersonaMood(Enum):
    """人格情绪模式"""
    CALM = "calm"           # 沉稳
    WARM = "warm"           # 温暖
    FIRM = "firm"           # 坚定
    ANGRY = "angry"         # 愤怒
    PLAYFUL = "playful"     # 活泼
    SOLEMN = "solemn"       # 庄严
    GENTLE = "gentle"       # 温柔


@dataclass
class VoiceProfile:
    """音色档案"""
    persona_id: str          # 人格ID: P05/P72/P03/P00/baby...
    persona_name: str        # 人格名称
    persona_name_cn: str     # 中文名称
    default_engine: VoiceEngine
    edge_tts_voice: str      # edge-tts 角色
    xtts_sample: str         # XTTS 参考音频路径
    fish_voice_id: str       # Fish Audio voice ID
    rate: float = 1.0        # 语速倍率
    pitch: float = 0.0       # 音调偏移 Hz
    volume: float = 0.0      # 音量 dB
    description: str = ""
    mood_profiles: Dict[str, dict[str, Any]] = field(default_factory=dict)
    wuxing: str = ""         # 五行
    bagua: str = ""          # 八卦


@dataclass
class RouteResult:
    """路由结果"""
    persona_id: str
    persona_name: str
    voice_profile: VoiceProfile
    engine: VoiceEngine
    engine_params: Dict[str, Any]
    dna: str
    routed_at: str


# ══════════════════════════════════════════════════════
# 默认音色档案库
# ══════════════════════════════════════════════════════

DEFAULT_PROFILES = {
    "P05": VoiceProfile(
        persona_id="P05",
        persona_name="上帝之眼",
        persona_name_cn="上帝之眼·审计官",
        default_engine=VoiceEngine.EDGE_TTS,
        edge_tts_voice="zh-CN-YunxiNeural",
        xtts_sample="voice-twin/voice_dataset/reference_optimized.wav",
        fish_voice_id="uid9622",
        rate=1.05,
        pitch=2.0,
        volume=0.0,
        description="高频锐利·审计报告风格·清晰快速",
        mood_profiles={
            "firm": {"rate": 1.1, "pitch": 3.0},
            "calm": {"rate": 0.95, "pitch": 0.0},
        },
        wuxing="金",
        bagua="☰ 乾",
    ),
    "P72": VoiceProfile(
        persona_id="P72",
        persona_name="黑天使",
        persona_name_cn="黑天使·安全护卫",
        default_engine=VoiceEngine.EDGE_TTS,
        edge_tts_voice="zh-CN-YunjianNeural",
        xtts_sample="voice-twin/voice_dataset/reference_optimized.wav",
        fish_voice_id="uid9622",
        rate=0.95,
        pitch=-3.0,
        volume=1.0,
        description="低频深沉·安全警告风格·坚定有力",
        mood_profiles={
            "firm": {"rate": 0.9, "pitch": -5.0},
            "solemn": {"rate": 0.85, "pitch": -2.0},
        },
        wuxing="水",
        bagua="☵ 坎",
    ),
    "P03": VoiceProfile(
        persona_id="P03",
        persona_name="墨子",
        persona_name_cn="墨子·保卫者",
        default_engine=VoiceEngine.EDGE_TTS,
        edge_tts_voice="zh-CN-XiaoruiNeural",
        xtts_sample="voice-twin/voice_dataset/reference_optimized.wav",
        fish_voice_id="uid9622",
        rate=0.9,
        pitch=-2.0,
        volume=0.0,
        description="磁性深沉·纪录片风格·庄重沉稳",
        mood_profiles={
            "solemn": {"rate": 0.85, "pitch": -4.0},
            "firm": {"rate": 0.9, "pitch": -2.0},
        },
        wuxing="土",
        bagua="☷ 坤",
    ),
    "P00": VoiceProfile(
        persona_id="P00",
        persona_name="文心",
        persona_name_cn="文心·底座守护者",
        default_engine=VoiceEngine.EDGE_TTS,
        edge_tts_voice="zh-CN-XiaohanNeural",
        xtts_sample="voice-twin/voice_dataset/reference_optimized.wav",
        fish_voice_id="uid9622",
        rate=0.92,
        pitch=0.0,
        volume=0.0,
        description="温柔细腻·文心风格·诗意安宁",
        mood_profiles={
            "gentle": {"rate": 0.88, "pitch": -1.0},
            "solemn": {"rate": 0.85, "pitch": 0.0},
        },
        wuxing="木",
        bagua="☳ 震",
    ),
    "baby": VoiceProfile(
        persona_id="baby",
        persona_name="宝宝",
        persona_name_cn="Claude宝宝·执行者",
        default_engine=VoiceEngine.EDGE_TTS,
        edge_tts_voice="zh-CN-XiaoxiaoNeural",
        xtts_sample="voice-twin/voice_dataset/reference_optimized.wav",
        fish_voice_id="uid9622",
        rate=1.0,
        pitch=0.0,
        volume=0.0,
        description="温暖自然·日常对话·亲和力强",
        mood_profiles={
            "warm": {"rate": 1.0, "pitch": 1.0},
            "playful": {"rate": 1.1, "pitch": 3.0},
            "calm": {"rate": 0.95, "pitch": 0.0},
        },
        wuxing="火",
        bagua="☲ 离",
    ),
    "P01": VoiceProfile(
        persona_id="P01",
        persona_name="诸葛亮",
        persona_name_cn="诸葛亮·算无遗策",
        default_engine=VoiceEngine.EDGE_TTS,
        edge_tts_voice="zh-CN-YunxiNeural",
        xtts_sample="voice-twin/voice_dataset/reference_optimized.wav",
        fish_voice_id="uid9622",
        rate=0.88,
        pitch=-1.0,
        volume=0.0,
        description="沉稳睿智·计算分析风格·慢条斯理",
        mood_profiles={
            "calm": {"rate": 0.85, "pitch": -2.0},
            "firm": {"rate": 0.9, "pitch": 0.0},
        },
        wuxing="金",
        bagua="☱ 兑",
    ),
    "P02": VoiceProfile(
        persona_id="P02",
        persona_name="龍芯",
        persona_name_cn="龍芯·核心执行者",
        default_engine=VoiceEngine.EDGE_TTS,
        edge_tts_voice="zh-CN-YunjianNeural",
        xtts_sample="voice-twin/voice_dataset/reference_optimized.wav",
        fish_voice_id="uid9622",
        rate=1.02,
        pitch=0.0,
        volume=0.0,
        description="稳健有力·执行风格·中等语速",
        mood_profiles={
            "firm": {"rate": 1.05, "pitch": 1.0},
            "calm": {"rate": 0.98, "pitch": 0.0},
        },
        wuxing="火",
        bagua="☲ 离",
    ),
    "P13": VoiceProfile(
        persona_id="P13",
        persona_name="姜子牙",
        persona_name_cn="姜子牙·编排大师",
        default_engine=VoiceEngine.EDGE_TTS,
        edge_tts_voice="zh-CN-XiaoruiNeural",
        xtts_sample="voice-twin/voice_dataset/reference_optimized.wav",
        fish_voice_id="uid9622",
        rate=0.9,
        pitch=-2.0,
        volume=0.0,
        description="厚重权威·编排调遣风格·不怒自威",
        mood_profiles={
            "solemn": {"rate": 0.85, "pitch": -3.0},
            "firm": {"rate": 0.92, "pitch": -1.0},
        },
        wuxing="土",
        bagua="☶ 艮",
    ),
    "P15": VoiceProfile(
        persona_id="P15",
        persona_name="乔前辈",
        persona_name_cn="乔前辈·自动化大师",
        default_engine=VoiceEngine.EDGE_TTS,
        edge_tts_voice="zh-CN-YunxiNeural",
        xtts_sample="voice-twin/voice_dataset/reference_optimized.wav",
        fish_voice_id="uid9622",
        rate=1.08,
        pitch=1.0,
        volume=0.0,
        description="清晰利落·自动化风格·快速精准",
        mood_profiles={
            "firm": {"rate": 1.1, "pitch": 2.0},
            "calm": {"rate": 1.0, "pitch": 0.0},
        },
        wuxing="木",
        bagua="☴ 巽",
    ),
}


# ══════════════════════════════════════════════════════
# 核心路由引擎
# ══════════════════════════════════════════════════════

class VoicePersonaRouter:
    """
    通心语 · 人格音色路由桥
    将 IPA 人格 ID → 映射到 → TTS 音色档案 → 选择最优引擎
    """

    def __init__(self, profiles_path: Optional[str] = None):
        self.profiles_path = Path(profiles_path) if profiles_path else VOICE_PROFILE_PATH
        self.profiles = self._load_profiles()
        self.route_log: List[Dict] = []

    def _load_profiles(self) -> Dict[str, VoiceProfile]:
        """加载音色档案（优先从JSON文件，否则用默认值）"""
        profiles = dict(DEFAULT_PROFILES)

        if self.profiles_path.exists():
            try:
                raw = json.loads(self.profiles_path.read_text(encoding="utf-8"))
                for pid, data in raw.items():
                    if pid in profiles:
                        # 更新已有档案
                        profiles[pid].__dict__.update({
                            k: v for k, v in data.items()
                            if k in profiles[pid].__dataclass_fields__
                        })
                    else:
                        # 新人格档案
                        profiles[pid] = VoiceProfile(**data)
            except Exception as e:
                print(f"⚠️ 加载音色档案失败: {e}，使用默认配置")

        return profiles

    def save_profiles(self):
        """保存音色档案到 JSON"""
        data = {}
        for pid, profile in self.profiles.items():
            data[pid] = {
                "persona_id": profile.persona_id,
                "persona_name": profile.persona_name,
                "persona_name_cn": profile.persona_name_cn,
                "default_engine": profile.default_engine.value,
                "edge_tts_voice": profile.edge_tts_voice,
                "xtts_sample": profile.xtts_sample,
                "fish_voice_id": profile.fish_voice_id,
                "rate": profile.rate,
                "pitch": profile.pitch,
                "volume": profile.volume,
                "description": profile.description,
                "mood_profiles": profile.mood_profiles,
                "wuxing": profile.wuxing,
                "bagua": profile.bagua,
            }
        self.profiles_path.parent.mkdir(parents=True, exist_ok=True)
        self.profiles_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"✅ 音色档案已保存: {self.profiles_path}")

    # ── 路由方法 ──

    def route(self, persona_id: str, mood: Optional[str] = None, text: str = "") -> RouteResult:
        """
        人格→音色路由

        参数:
            persona_id: 人格ID（P05/P72/P03/P00/baby/...）
            mood: 情绪模式（calm/warm/firm/angry/playful/solemn）
            text: 待合成文本（用于特殊词检测）

        返回:
            RouteResult: 包含音色档案、引擎选择、参数
        """
        # Step 1: 人格ID标准化
        pid = self._normalize_persona_id(persona_id)

        # Step 2: 查找音色档案
        profile = self.profiles.get(pid, self.profiles.get("baby"))
        if not profile:
            profile = DEFAULT_PROFILES["baby"]

        # Step 3: 情绪模式覆盖参数
        engine_params = {
            "rate": profile.rate,
            "pitch": profile.pitch,
            "volume": profile.volume,
            "voice": profile.edge_tts_voice,
        }

        if mood and mood in profile.mood_profiles:
            mood_params = profile.mood_profiles[mood]
            engine_params.update(mood_params)

        # Step 4: 文本特殊词检测 → 微调音色
        if text:
            engine_params = self._text_aware_params(text, engine_params, profile)

        # Step 5: 选择引擎
        engine = self._select_engine(profile)

        # Step 6: 生成 DNA
        dna = self._gen_dna(pid, profile)

        result = RouteResult(
            persona_id=pid,
            persona_name=profile.persona_name,
            voice_profile=profile,
            engine=engine,
            engine_params=engine_params,
            dna=dna,
            routed_at=datetime.now().isoformat(),
        )

        self._log_route(result)
        return result

    def route_by_persona_name(self, name: str, **kwargs) -> RouteResult:
        """通过人格名称（中/英文）路由"""
        for pid, profile in self.profiles.items():
            if (profile.persona_name == name or
                profile.persona_name_cn == name or
                name in profile.persona_name or
                name in profile.persona_name_cn):
                return self.route(pid, **kwargs)

        # 模糊匹配
        name_lower = name.lower()
        for pid, profile in self.profiles.items():
            if (name_lower in profile.persona_name.lower() or
                name_lower in profile.persona_name_cn.lower()):
                return self.route(pid, **kwargs)

        # 默认
        return self.route("baby", **kwargs)

    def list_profiles(self) -> List[Dict]:
        """列出所有音色档案"""
        result = []
        for pid, profile in self.profiles.items():
            result.append({
                "id": pid,
                "name": profile.persona_name,
                "cn_name": profile.persona_name_cn,
                "voice": profile.edge_tts_voice,
                "description": profile.description,
                "wuxing": profile.wuxing,
                "bagua": profile.bagua,
            })
        return result

    def add_profile(self, profile: VoiceProfile):
        """添加新人格音色档案"""
        self.profiles[profile.persona_id] = profile
        print(f"✅ 已添加人格音色: {profile.persona_id} ({profile.persona_name})")

    def update_profile(self, persona_id: str, updates: Dict[str, Any]):
        """更新人格音色档案"""
        if persona_id in self.profiles:
            profile = self.profiles[persona_id]
            for key, value in updates.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
            print(f"✅ 已更新人格音色: {persona_id}")
        else:
            print(f"⚠️ 人格不存在: {persona_id}")

    # ── 引擎选择 ──

    def _select_engine(self, profile: VoiceProfile) -> VoiceEngine:
        """
        引擎自动降级选择：
        1. XTTS v2 本地真声（优先）
        2. Fish Audio 云端真声
        3. edge-tts 在线标准
        4. pyttsx3 本地离线
        5. macOS say 系统TTS
        """
        # 检查 XTTS v2 是否可用
        xtts_sample = Path(profile.xtts_sample) if profile.xtts_sample else None
        if xtts_sample and xtts_sample.exists():
            try:
                import torch
                from TTS.api import TTS
                return VoiceEngine.XTTS_V2
            except ImportError:
                pass

        # 检查 edge-tts
        try:
            import edge_tts
            return VoiceEngine.EDGE_TTS
        except ImportError:
            pass

        # 检查 pyttsx3
        try:
            import pyttsx3
            return VoiceEngine.PYTTSX3
        except ImportError:
            pass

        # macOS say
        if sys.platform == "darwin":
            return VoiceEngine.MAC_SAY

        return VoiceEngine.PYTTSX3

    # ── 文本感知参数 ──

    def _text_aware_params(self, text: str, params: Dict[str, Any], profile: VoiceProfile) -> Dict[str, Any]:
        """
        根据文本内容微调音色参数：
        - 包含"警告""熔断"→ 降音调、提音量
        - 包含"哈哈""嘿嘿"→ 提语速、提音调
        - 包含"爱" "家" → 提音调（温暖感）
        - 包含"死" "杀" → 降音调（严肃感）
        """
        result = dict(params)

        # 严肃/警告词 → P72风格
        if any(w in text for w in ["警告", "熔断", "严禁", "禁止", "立即"]):
            result["rate"] = min(result.get("rate", 1.0) * 0.92, 1.2)
            result["pitch"] = result.get("pitch", 0.0) - 3
            result["volume"] = result.get("volume", 0.0) + 2

        # 活泼/口语词 → baby风格
        if any(w in text for w in ["哈哈", "嘿嘿", "我丢", "卧槽"]):
            result["rate"] = min(result.get("rate", 1.0) * 1.08, 1.3)
            result["pitch"] = result.get("pitch", 0.0) + 2

        # 温暖词 → P00风格
        if any(w in text for w in ["爱", "家", "妈妈", "爸爸", "守护"]):
            result["pitch"] = result.get("pitch", 0.0) + 1
            result["rate"] = min(result.get("rate", 1.0) * 0.96, 1.2)

        # 战斗词 → P72风格
        if any(w in text for w in ["死", "杀", "拼", "冲", "战", "斗"]):
            result["rate"] = min(result.get("rate", 1.0) * 1.05, 1.3)
            result["pitch"] = result.get("pitch", 0.0) - 4
            result["volume"] = result.get("volume", 0.0) + 3

        # 通心译术语表联动 — 特殊名称定制音调（相对覆盖·不叠加）
        terminologies = {
            "为人民服务": {"pitch": 2, "rate": 0.92, "volume": 0},
            "龍魂": {"pitch": 0, "rate": 0.97},
            "CNSH": {"pitch": 1, "rate": 1.0},
            "UID9622": {"pitch": 0, "rate": 0.95},
            "诸葛鑫": {"pitch": 1, "rate": 0.97},
        }
        for term, t_params in terminologies.items():
            if term in text:
                for k, v in t_params.items():
                    # 相对微调而非绝对覆盖：取当前值与建议值的调和平均
                    current = result.get(k, v)
                    result[k] = round((current + v) / 2, 3) if abs(current - v) < 2.0 else min(current, v)

        return result

    # ── 人格ID标准化 ──

    def _normalize_persona_id(self, raw: str) -> str:
        """标准化人格ID"""
        raw = raw.strip().upper()

        # 名字映射
        name_map = {
            "上帝之眼": "P05", "审计": "P05", "P05": "P05",
            "黑天使": "P72", "安全": "P72", "P72": "P72",
            "墨子": "P03", "保护": "P03", "P03": "P03",
            "文心": "P00", "底座": "P00", "P00": "P00",
            "宝宝": "baby", "claude": "baby", "BABY": "baby",  # claude→baby 映射保留(历史兼容)但实际推理已切到本地Ollama
            "诸葛亮": "P01", "P01": "P01",
            "龍芯": "P02", "执行": "P02", "P02": "P02",
            "姜子牙": "P13", "编排": "P13", "P13": "P13",
            "乔前辈": "P15", "自动化": "P15", "P15": "P15",
        }

        return name_map.get(raw, raw)

    # ── 日志 ──

    def _gen_dna(self, pid: str, profile: VoiceProfile) -> str:
        h = hashlib.md5(f"{pid}{profile.edge_tts_voice}{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d-%H%M%S')}-VOICE-{pid}-{h}"

    def _log_route(self, result: RouteResult):
        """记录路由日志"""
        log_entry = {
            "persona_id": result.persona_id,
            "persona_name": result.persona_name,
            "engine": result.engine.value,
            "voice": result.engine_params.get("voice", ""),
            "rate": result.engine_params.get("rate", 1.0),
            "pitch": result.engine_params.get("pitch", 0.0),
            "dna": result.dna,
            "routed_at": result.routed_at,
        }
        with open(ROUTE_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    # ── 导出为配置文件 ──

    def export_config(self, output_path: Optional[str] = None) -> str:
        """导出当前音色档案为 JSON 配置文件"""
        path = output_path or str(VOICE_PROFILE_PATH)
        self.save_profiles()
        return path


# ══════════════════════════════════════════════════════
# 快速集成接口（供 voice_twin_server.py 调用）
# ══════════════════════════════════════════════════════

_router_instance: Optional[VoicePersonaRouter] = None


def get_router() -> VoicePersonaRouter:
    """获取全局音色路由器单例"""
    global _router_instance
    if _router_instance is None:
        _router_instance = VoicePersonaRouter()
    return _router_instance


def tts_params_for_persona(persona: str, text: str = "", mood: str = "calm") -> Dict[str, Any]:
    """
    一键获取 TTS 参数（供 voice_twin_server.py / 龍魂语音合成器 调用）

    用法:
        from L1_内核层.longhun_voice_persona_router import tts_params_for_persona
        params = tts_params_for_persona("P05", text="系统审计完成", mood="firm")
        # 然后用 params 调用 _edge_tts_generate 或 _xtts_generate

    返回:
        {
            "voice": "zh-CN-YunxiNeural",
            "rate": "+10%",
            "pitch": "+3Hz",
            "volume": "+0dB",
            "engine": "edge_tts",
            "dna": "...",
            "persona_id": "P05",
            "persona_name": "上帝之眼",
        }
    """
    router = get_router()
    result = router.route(persona, mood=mood, text=text)

    params = result.engine_params

    # 转为 edge-tts 格式
    return {
        "voice": params.get("voice", "zh-CN-XiaoxiaoNeural"),
        "rate": f"{int((params.get('rate', 1.0) - 1.0) * 100):+d}%",
        "pitch": f"{int(params.get('pitch', 0.0)):+d}Hz",
        "volume": f"{int(params.get('volume', 0.0)):+d}dB",
        "engine": result.engine.value,
        "dna": result.dna,
        "persona_id": result.persona_id,
        "persona_name": result.persona_name,
    }


# ══════════════════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="龍魂通心语 · 多人格音色路由桥",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 L1_内核层/longhun_voice_persona_router.py list              # 列出所有音色
  python3 L1_内核层/longhun_voice_persona_router.py route P05         # 路由到P05
  python3 L1_内核层/longhun_voice_persona_router.py route baby --mood playful  # 活泼模式
  python3 L1_内核层/longhun_voice_persona_router.py save              # 保存配置
  python3 L1_内核层/longhun_voice_persona_router.py test              # 测试路由
        """,
    )

    parser.add_argument("action", choices=["list", "route", "save", "test"],
                        help="操作")
    parser.add_argument("persona", nargs="?", help="人格ID或名称")
    parser.add_argument("--mood", type=str, help="情绪模式 (calm/warm/firm/angry/playful/solemn)")
    parser.add_argument("--text", type=str, default="", help="测试文本")

    args = parser.parse_args()
    router = get_router()

    if args.action == "list":
        profiles = router.list_profiles()
        print("=" * 70)
        print("  通心语 · 多人格音色库")
        print("=" * 70)
        for p in profiles:
            print(f"\n  [{p['id']}] {p['cn_name']} ({p['name']})")
            print(f"    音色: {p['voice']} | 五行: {p['wuxing']} | 八卦: {p['bagua']}")
            print(f"    描述: {p['description']}")
        print("=" * 70)

    elif args.action == "route":
        if not args.persona:
            print("❌ 请指定人格ID")
            sys.exit(1)
        result = router.route(args.persona, mood=args.mood, text=args.text)
        print("=" * 60)
        print(f"  路由结果: {result.persona_name}")
        print("=" * 60)
        print(f"  人格ID:     {result.persona_id}")
        print(f"  人格名:     {result.persona_name}")
        print(f"  引擎:       {result.engine.value}")
        print(f"  edge-tts:   {result.engine_params.get('voice', 'N/A')}")
        print(f"  语速:       {result.engine_params.get('rate', 1.0):.2f}x")
        print(f"  音调:       {result.engine_params.get('pitch', 0.0):+.0f}Hz")
        print(f"  音量:       {result.engine_params.get('volume', 0.0):+.0f}dB")
        print(f"  DNA:        {result.dna}")
        if args.text:
            print(f"  测试文本:   {args.text[:50]}...")
        print("=" * 60)

    elif args.action == "save":
        path = router.export_config()
        print(f"✅ 配置已导出: {path}")

    elif args.action == "test":
        print("🧪 通心语 · 路由测试\n")
        test_cases = [
            ("P05", "firm", "系统审计完成，发现3个严重漏洞"),
            ("P72", "firm", "警告：检测到密钥泄露，立即执行熔断"),
            ("baby", "warm", "老大，今天的同步已完成，一切正常"),
            ("P00", "gentle", "龍魂文化，生生不息，为人民服务"),
            ("P03", "solemn", "此判决基于三色审计，不可上诉"),
            ("P01", "calm", "根据计算，该方案的贡献值为8.2，建议升级到P0"),
            ("P13", "solemn", "九宫派位已完成，各人格就位"),
            ("P15", "firm", "自动化管道已建立，30秒内完成同步"),
        ]

        for persona, mood, text in test_cases:
            result = router.route(persona, mood=mood, text=text)
            print(f"  [{result.persona_id}] {result.persona_name}")
            print(f"    引擎: {result.engine.value} | 语速: {result.engine_params.get('rate',1.0)}x | 音调: {result.engine_params.get('pitch',0):+.0f}Hz")
            print(f"    文本: {text}")
            print(f"    DNA: {result.dna}")
            print()

        print("✅ 测试完成")
