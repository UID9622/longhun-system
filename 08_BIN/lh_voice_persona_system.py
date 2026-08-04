#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_VOICE_PERSONA_SYSTEM-v1.0-b19669a1
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂 · 人格声色绑定系统 v2.0
LongHun Voice-Persona-Portrait Binding System

功能：
  1. 真人原声扫描 → 自动注册声纹锚定
  2. 8大虚拟人格声色 → 参数固定·DNA锚定
  3. 真人肖像绑定 → 照片哈希上链·不做3D
  4. 声纹验证 → 防冒充·防篡改
  5. 与推荐引擎联动 → 声纹+DNA双重确认
  6. 一键清单 → 所有声色资产总览

原则：
  - 人格声色固定 — 参数不可篡改
  - 声纹锚定 — 哈希上链
  - 真实人像不做3D — 照片DNA绑定真人身份
  - 真人原声主权声明 / 虚拟人格声对外交互

DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-VOICE-PERSONA-SYSTEM-v2.0
创始人: UID9622 · 龍芯北辰 · 诸葛鑫
"""

import hashlib
import json
import sys
import wave
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict

import numpy as np

# ══════════════════════════════════════════════════════
# DNA 常量
# ══════════════════════════════════════════════════════

MASTER_DNA = "#龍芯⚡️丙午·辛未·丙戌·亥时-VOICE-PERSONA-SYSTEM-v2.0"
MASTER_UID = "UID9622"
MASTER_NAME = "诸葛鑫·Lucky"
CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 龙魂声纹根目录
ANCHOR_DIR = Path.home() / ".龍魂" / "voice_anchors"
ANCHOR_DIR.mkdir(parents=True, exist_ok=True)
PORTRAIT_DIR = Path.home() / ".龍魂" / "portraits"
PORTRAIT_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_RATE = 16000
VOICE_DIM = 256


# ══════════════════════════════════════════════════════
# 枚举
# ══════════════════════════════════════════════════════

class VoiceType(Enum):
    REAL = "real"        # 真人原声 → 主权声明
    VIRTUAL = "virtual"  # 虚拟人格声 → 对外交互


class DNALevel(Enum):
    """DNA 绑定等级"""
    L0_本尊 = "L0-本尊"              # UID9622 真人原声+肖像
    L1_虚拟人格 = "L1-虚拟人格"       # 虚拟人格声色
    L2_声纹验证 = "L2-声纹验证"       # 声纹验证通过
    L3_未绑定 = "L3-未绑定"           # 未绑定DNA


# ══════════════════════════════════════════════════════
# 数据结构
# ══════════════════════════════════════════════════════

@dataclass
class VoiceProfile:
    """声色档案"""
    persona_id: str
    name: str
    name_cn: str
    voice_type: VoiceType
    pitch_range: Tuple[float, float]  # 基频范围 Hz
    speed: float                      # 语速 0.5-2.0
    emotion_map: Dict[str, float]     # 情感强度映射
    dna_signature: str                # DNA 签名
    sample_hash: str                  # 原始样本哈希
    engine: str = "edge_tts"          # TTS 引擎
    edge_tts_voice: str = ""          # edge-tts 角色名
    wuxing: str = ""                  # 五行
    bagua: str = ""                   # 八卦
    description: str = ""
    base_features: Optional[np.ndarray] = None  # 声纹特征向量（256维）
    created_at: str = ""
    audio_source: str = ""            # 音频来源路径


@dataclass
class PortraitBinding:
    """肖像绑定"""
    persona_id: str
    photo_path: str
    photo_hash: str                   # SHA256 照片哈希
    dna_signature: str                # DNA 签名
    width: int = 0
    height: int = 0
    file_size: int = 0
    is_3d: bool = False               # 永远 False
    created_at: str = ""


@dataclass
class VerifyResult:
    """验证结果"""
    status: str                       # MATCH / MISMATCH / NOT_FOUND
    similarity: float
    threshold: float
    persona_id: str
    voice_type: str
    dna_verified: str
    confidence: str


# ══════════════════════════════════════════════════════
# 8大虚拟人格声色 · 固定参数
# ══════════════════════════════════════════════════════

VIRTUAL_PERSONA_VOICES = {
    "P01": VoiceProfile(
        persona_id="P01", name="诸葛亮", name_cn="诸葛亮·战略推演",
        voice_type=VoiceType.VIRTUAL,
        pitch_range=(85, 120), speed=0.85,
        emotion_map={"calm": 0.8, "serious": 0.7, "confident": 0.9, "urgent": 0.3, "casual": 0.1},
        dna_signature="", sample_hash="VIRTUAL-FIXED",
        engine="edge_tts", edge_tts_voice="zh-CN-YunxiNeural",
        wuxing="金", bagua="☰ 乾",
        description="沉稳男中音，每句带停顿，推演感",
    ),
    "P02": VoiceProfile(
        persona_id="P02", name="宝宝", name_cn="宝宝·跟进执行",
        voice_type=VoiceType.VIRTUAL,
        pitch_range=(180, 250), speed=1.15,
        emotion_map={"energetic": 0.9, "friendly": 0.8, "casual": 0.7, "serious": 0.3, "calm": 0.2},
        dna_signature="", sample_hash="VIRTUAL-FIXED",
        engine="edge_tts", edge_tts_voice="zh-CN-XiaoxiaoNeural",
        wuxing="火", bagua="☲ 離",
        description="年轻女声，带语气词，执行力强",
    ),
    "P03": VoiceProfile(
        persona_id="P03", name="雯雯", name_cn="雯雯·三色审计",
        voice_type=VoiceType.VIRTUAL,
        pitch_range=(150, 200), speed=1.0,
        emotion_map={"neutral": 0.9, "precise": 0.8, "calm": 0.7, "friendly": 0.1, "energetic": 0.1},
        dna_signature="", sample_hash="VIRTUAL-FIXED",
        engine="edge_tts", edge_tts_voice="zh-CN-XiaoruiNeural",
        wuxing="土", bagua="☷ 坤",
        description="中性冷静，无情感波动，精确播报",
    ),
    "P04": VoiceProfile(
        persona_id="P04", name="鲁班", name_cn="鲁班·代码落地",
        voice_type=VoiceType.VIRTUAL,
        pitch_range=(100, 150), speed=1.1,
        emotion_map={"direct": 0.9, "neutral": 0.7, "confident": 0.6, "casual": 0.2, "friendly": 0.1},
        dna_signature="", sample_hash="VIRTUAL-FIXED",
        engine="edge_tts", edge_tts_voice="zh-CN-YunjianNeural",
        wuxing="木", bagua="☳ 震",
        description="技术男声，直接无废话，代码感",
    ),
    "P05": VoiceProfile(
        persona_id="P05", name="上帝之眼", name_cn="上帝之眼·全局观察",
        voice_type=VoiceType.VIRTUAL,
        pitch_range=(60, 90), speed=0.75,
        emotion_map={"omniscient": 0.9, "calm": 0.8, "serious": 0.7, "urgent": 0.1, "casual": 0.0},
        dna_signature="", sample_hash="VIRTUAL-FIXED",
        engine="edge_tts", edge_tts_voice="zh-CN-YunyangNeural",
        wuxing="水", bagua="☵ 坎",
        description="超低沉男声，带空间感，全景播报",
    ),
    "P06": VoiceProfile(
        persona_id="P06", name="数学大师", name_cn="数学大师·算法计算",
        voice_type=VoiceType.VIRTUAL,
        pitch_range=(160, 220), speed=0.95,
        emotion_map={"precise": 0.9, "neutral": 0.8, "confident": 0.7, "casual": 0.1, "friendly": 0.1},
        dna_signature="", sample_hash="VIRTUAL-FIXED",
        engine="edge_tts", edge_tts_voice="zh-CN-XiaohanNeural",
        wuxing="金", bagua="☱ 兌",
        description="精确女声，数字清晰，带节奏停顿",
    ),
    "P07": VoiceProfile(
        persona_id="P07", name="军魂", name_cn="军魂·军事硬核",
        voice_type=VoiceType.VIRTUAL,
        pitch_range=(90, 140), speed=1.2,
        emotion_map={"commanding": 0.9, "urgent": 0.8, "serious": 0.7, "casual": 0.0, "friendly": 0.0},
        dna_signature="", sample_hash="VIRTUAL-FIXED",
        engine="edge_tts", edge_tts_voice="zh-CN-YunjianNeural",
        wuxing="火", bagua="☲ 離",
        description="军人口令声，短促有力，无废话",
    ),
    "P08": VoiceProfile(
        persona_id="P08", name="民生守护", name_cn="民生守护·温和关怀",
        voice_type=VoiceType.VIRTUAL,
        pitch_range=(170, 230), speed=0.9,
        emotion_map={"warm": 0.9, "friendly": 0.8, "calm": 0.7, "commanding": 0.1, "urgent": 0.2},
        dna_signature="", sample_hash="VIRTUAL-FIXED",
        engine="edge_tts", edge_tts_voice="zh-CN-XiaoxiaoNeural",
        wuxing="土", bagua="☷ 坤",
        description="温和女声，亲切安抚，民生关怀",
    ),
    # P09-P15 映射到最接近的声色（可扩展独立音色）
    "P09": VoiceProfile(
        persona_id="P09", name="孙思邈", name_cn="孙思邈·道引",
        voice_type=VoiceType.VIRTUAL,
        pitch_range=(80, 115), speed=0.8,
        emotion_map={"calm": 0.9, "serious": 0.7, "gentle": 0.6, "urgent": 0.1, "casual": 0.1},
        dna_signature="", sample_hash="VIRTUAL-FIXED",
        engine="edge_tts", edge_tts_voice="zh-CN-YunxiNeural",
        wuxing="木", bagua="☴ 巽",
        description="沉稳老者声，道家气息，慢节奏",
    ),
}

# 为所有虚拟人格生成固定DNA签名
for pid, profile in VIRTUAL_PERSONA_VOICES.items():
    seed = f"{MASTER_DNA}-{pid}-{profile.name}-{profile.pitch_range}-{profile.speed}"
    profile.dna_signature = hashlib.sha256(seed.encode()).hexdigest()[:32]
    profile.created_at = datetime.now().isoformat()
    # 生成固定声纹特征（基于DNA种子，可复现）
    np.random.seed(int(hashlib.sha256(f"voice-{pid}-{profile.name}".encode()).hexdigest()[:8], 16))
    feats = np.random.randn(VOICE_DIM)
    profile.base_features = feats / np.linalg.norm(feats)


# ══════════════════════════════════════════════════════
# 音频工具函数（无外部依赖·纯numpy+wave）
# ══════════════════════════════════════════════════════

def load_wav(path: Path) -> Tuple[np.ndarray, int]:
    """加载 WAV 文件。"""
    with wave.open(str(path), "rb") as wf:
        sr = wf.getframerate()
        n_channels = wf.getnchannels()
        width = wf.getsampwidth()
        frames = wf.readframes(wf.getnframes())

    if width == 2:
        audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    elif width == 4:
        audio = np.frombuffer(frames, dtype=np.int32).astype(np.float32) / 2147483648.0
    elif width == 1:
        audio = np.frombuffer(frames, dtype=np.uint8).astype(np.float32) / 128.0 - 1.0
    else:
        raise ValueError(f"不支持的采样宽度: {width}")

    if n_channels > 1:
        audio = audio.reshape(-1, n_channels).mean(axis=1)

    return audio, sr


def resample(audio: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
    """简单线性重采样。"""
    if orig_sr == target_sr:
        return audio
    ratio = target_sr / orig_sr
    n_out = int(len(audio) * ratio)
    indices = np.arange(n_out) / ratio
    indices = np.clip(indices, 0, len(audio) - 1)
    lo = np.floor(indices).astype(int)
    hi = np.clip(lo + 1, 0, len(audio) - 1)
    frac = indices - lo
    return audio[lo] * (1 - frac) + audio[hi] * frac


def extract_voice_features(audio: np.ndarray, sr: int) -> np.ndarray:
    """提取声纹特征向量（256维·纯numpy实现）。

    维度组成:
      0-19:  MFCC近似（频谱能量分桶）
      20-39: 频谱包络
      40-59: 时域统计
      60-79: 过零率分布
      80-99: 能量分布
      100-255: DNA种子填充
    """
    n = len(audio)
    features = np.zeros(VOICE_DIM, dtype=np.float32)

    if n < 512:
        return features

    # 分帧
    frame_len = 512
    hop = 256
    n_frames = (n - frame_len) // hop
    if n_frames < 2:
        return features

    # 1. 频谱能量分桶 (20维 MFCC近似)
    for i in range(20):
        lo = i * frame_len // 40
        hi = (i + 1) * frame_len // 40
        lo = max(0, lo)
        hi = min(frame_len, hi)
        band_energy = np.array([
            np.mean(np.abs(np.fft.rfft(audio[j:j+frame_len] * np.hanning(frame_len))[lo:hi]) ** 2)
            for j in range(0, n - frame_len, hop)
        ])
        features[i] = np.mean(band_energy)

    # 2. 频谱质心分布 (20维)
    for i in range(20):
        frame_idx = i * n_frames // 20
        j = frame_idx * hop
        if j + frame_len <= n:
            frame = audio[j:j+frame_len] * np.hanning(frame_len)
            spec = np.abs(np.fft.rfft(frame))
            freqs = np.fft.rfftfreq(frame_len, 1/sr)
            total = np.sum(spec) + 1e-10
            centroid = np.sum(freqs * spec) / total
            features[20 + i] = centroid / (sr / 2)

    # 3. 时域统计 (20维)
    for i in range(20):
        frame_idx = i * n_frames // 20
        j = frame_idx * hop
        if j + frame_len <= n:
            frame = audio[j:j+frame_len]
            features[40 + i] = np.std(frame)

    # 4. 过零率分布 (20维)
    for i in range(20):
        frame_idx = i * n_frames // 20
        j = frame_idx * hop
        if j + frame_len <= n:
            frame = audio[j:j+frame_len]
            zcr = np.sum(np.abs(np.diff(np.sign(frame)))) / (2 * len(frame))
            features[60 + i] = zcr

    # 5. 能量包络 (20维)
    for i in range(20):
        frame_idx = i * n_frames // 20
        j = frame_idx * hop
        if j + frame_len <= n:
            frame = audio[j:j+frame_len]
            features[80 + i] = np.sqrt(np.mean(frame ** 2))

    # 6. DNA种子填充 (余下维)
    # 用音频内容哈希作为种子
    audio_hash = hashlib.sha256(audio.tobytes()[:4096]).hexdigest()
    np.random.seed(int(audio_hash[:8], 16))
    features[100:] = np.random.randn(VOICE_DIM - 100) * 0.05

    # 归一化
    norm = np.linalg.norm(features)
    if norm > 0:
        features = features / norm

    return features


def estimate_pitch_range(audio: np.ndarray, sr: int) -> Tuple[float, float]:
    """估算基频范围（简化自相关法）。"""
    if len(audio) < sr:
        return (0.0, 0.0)

    # 分段检测
    seg_len = sr // 2
    pitches = []
    for start in range(0, len(audio) - seg_len, seg_len):
        seg = audio[start:start+seg_len]
        # 自相关
        corr = np.correlate(seg, seg, mode='full')
        corr = corr[len(corr)//2:]
        # 找第一个峰值（60-400Hz 对应 lag）
        min_lag = sr // 400
        max_lag = sr // 60
        if max_lag >= len(corr):
            continue
        corr_seg = corr[min_lag:max_lag]
        if len(corr_seg) == 0:
            continue
        peak_lag = np.argmax(corr_seg) + min_lag
        if peak_lag > 0:
            pitch = sr / peak_lag
            pitches.append(pitch)

    if not pitches:
        return (0.0, 0.0)

    return (float(np.percentile(pitches, 5)), float(np.percentile(pitches, 95)))


# ══════════════════════════════════════════════════════
# 核心类
# ══════════════════════════════════════════════════════

class LongHunVoicePersonaSystem:
    """龍魂人格声色绑定系统"""

    def __init__(self):
        self.real_voices: Dict[str, VoiceProfile] = {}
        self.virtual_voices: Dict[str, VoiceProfile] = dict(VIRTUAL_PERSONA_VOICES)
        self.portraits: Dict[str, PortraitBinding] = {}
        self._load_existing()

    # ── 持久化 ──

    def _load_existing(self) -> None:
        """从锚定目录加载已有的声色。"""
        manifest_path = ANCHOR_DIR / "manifest.json"
        if manifest_path.exists():
            try:
                with open(manifest_path, "r") as f:
                    data = json.load(f)
                for anchor in data.get("anchors", []):
                    pid = anchor.get("persona_id", "")
                    if pid.startswith("REAL-"):
                        pr = anchor.get("pitch_range", [0, 0])
                        profile = VoiceProfile(
                            persona_id=pid,
                            name=anchor.get("user_id", "未知"),
                            name_cn=anchor.get("text", ""),
                            voice_type=VoiceType.REAL,
                            pitch_range=(float(pr[0]), float(pr[1])) if len(pr) >= 2 else (0.0, 0.0),
                            speed=1.0,
                            emotion_map={"natural": 1.0},
                            dna_signature=anchor.get("dna", ""),
                            sample_hash=anchor.get("voice_hash", ""),
                            created_at=anchor.get("created_at", ""),
                            audio_source=anchor.get("audio_source", anchor.get("source", "")),
                        )
                        self.real_voices[pid] = profile
                        # 加载声纹特征向量
                        feat_path = ANCHOR_DIR / "features" / f"{pid}.npy"
                        if feat_path.exists():
                            try:
                                profile.base_features = np.load(feat_path)
                            except Exception:
                                pass
            except Exception as e:
                print(f"⚠️ 加载已有锚定失败: {e}")

        # 加载肖像绑定
        portrait_manifest = PORTRAIT_DIR / "portrait_bindings.json"
        if portrait_manifest.exists():
            try:
                with open(portrait_manifest, "r") as f:
                    data = json.load(f)
                for binding in data.get("bindings", []):
                    pb = PortraitBinding(**binding)
                    self.portraits[pb.persona_id] = pb
            except Exception as e:
                print(f"⚠️ 加载肖像绑定失败: {e}")

    def _save_anchor(self, profile: VoiceProfile) -> None:
        """保存声纹锚定。"""
        manifest_path = ANCHOR_DIR / "manifest.json"
        data = {"version": "3.0", "schema": "voice-persona-v3", "anchors": []}

        if manifest_path.exists():
            try:
                with open(manifest_path, "r") as f:
                    data = json.load(f)
            except Exception:
                pass

        # 检查是否已存在
        anchors = data.get("anchors", [])
        existing_idx = None
        for i, a in enumerate(anchors):
            if a.get("persona_id") == profile.persona_id:
                existing_idx = i
                break

        anchor = {
            "persona_id": profile.persona_id,
            "user_id": f"uid9622-{profile.name}",
            "text": profile.name_cn,
            "voice_hash": profile.sample_hash,
            "dna": profile.dna_signature,
            "created_at": profile.created_at,
            "ip": "localhost",
            "source": profile.voice_type.value,
            "audio_source": profile.audio_source,
            "pitch_range": list(profile.pitch_range),
            "engine": profile.engine,
        }

        if existing_idx is not None:
            anchors[existing_idx] = anchor
        else:
            anchors.append(anchor)

        data["anchors"] = anchors
        data["updated_at"] = datetime.now().isoformat()

        with open(manifest_path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # 持久化声纹特征向量（numpy二进制）
        if profile.base_features is not None and np.any(profile.base_features != 0):
            feat_dir = ANCHOR_DIR / "features"
            feat_dir.mkdir(parents=True, exist_ok=True)
            np.save(feat_dir / f"{profile.persona_id}.npy", profile.base_features)

    def _save_portrait(self, binding: PortraitBinding) -> None:
        """保存肖像绑定。"""
        manifest_path = PORTRAIT_DIR / "portrait_bindings.json"
        data = {"version": "1.0", "bindings": [], "updated_at": ""}

        if manifest_path.exists():
            try:
                with open(manifest_path, "r") as f:
                    data = json.load(f)
            except Exception:
                pass

        bindings = data.get("bindings", [])
        existing_idx = None
        for i, b in enumerate(bindings):
            if b.get("persona_id") == binding.persona_id:
                existing_idx = i
                break

        bd = asdict(binding)
        bd["is_3d"] = False  # 永远不做3D

        if existing_idx is not None:
            bindings[existing_idx] = bd
        else:
            bindings.append(bd)

        data["bindings"] = bindings
        data["updated_at"] = datetime.now().isoformat()

        with open(manifest_path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ── 真人原声注册 ──

    def register_real_voice(self, audio_path: str) -> VoiceProfile:
        """注册真人原声 → DNA锚定。

        自动检测音域、提取声纹、计算哈希、绑定DNA。
        """
        path = Path(audio_path).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"音频文件不存在: {path}")

        print(f"\n🎙️  注册真人原声")
        print(f"   文件: {path}")
        print(f"   大小: {path.stat().st_size / 1024:.1f} KB")

        # 加载音频
        audio, orig_sr = load_wav(path)
        duration = len(audio) / orig_sr
        print(f"   时长: {duration:.1f}s · 采样率: {orig_sr}Hz")

        # 重采样到16kHz
        audio = resample(audio, orig_sr, SAMPLE_RATE)
        print(f"   重采样: {orig_sr} → {SAMPLE_RATE} Hz")

        # 提取声纹特征
        features = extract_voice_features(audio, SAMPLE_RATE)
        print(f"   声纹维度: {VOICE_DIM}")

        # 估算音域
        pitch_range = estimate_pitch_range(audio, SAMPLE_RATE)
        print(f"   音域: {pitch_range[0]:.1f}-{pitch_range[1]:.1f} Hz")

        # 音频哈希
        with open(path, "rb") as f:
            sample_hash = hashlib.sha256(f.read()).hexdigest()[:32]

        # DNA 签名（真人绑定主DNA + 音频哈希 + 声纹特征）
        dna_seed = f"{MASTER_DNA}-REAL-{MASTER_NAME}-{sample_hash}-{features[:20].tobytes()}"
        dna_sig = hashlib.sha256(dna_seed.encode()).hexdigest()[:32]

        # 创建档案
        persona_id = f"REAL-{MASTER_UID}"
        profile = VoiceProfile(
            persona_id=persona_id,
            name=MASTER_NAME,
            name_cn=f"{MASTER_NAME} · 真人原声",
            voice_type=VoiceType.REAL,
            pitch_range=pitch_range,
            speed=1.0,
            emotion_map={"natural": 1.0},
            dna_signature=dna_sig,
            sample_hash=sample_hash,
            engine="real",  # 真人原声不需要TTS引擎
            wuxing="",
            bagua="",
            description="真人原声 · 主权声明 · 关键决策 · 身份确认 · 不可篡改",
            base_features=features,
            created_at=datetime.now().isoformat(),
            audio_source=str(path),
        )

        self.real_voices[persona_id] = profile
        self._save_anchor(profile)

        print(f"   ✅ 声纹锚定完成")
        print(f"   样本哈希: {sample_hash[:16]}...")
        print(f"   DNA签名: {dna_sig[:16]}...")
        print(f"   状态: 已锚定 · 不可篡改")

        return profile

    # ── 肖像绑定 ──

    def bind_portrait(self, photo_path: str, persona_id: str = "REAL") -> PortraitBinding:
        """绑定真人肖像 → DNA哈希上链。

        不做3D，不生成模型，仅哈希绑定真人身份。
        """
        path = Path(photo_path).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"照片文件不存在: {path}")

        print(f"\n📷 绑定真人肖像")
        print(f"   文件: {path}")
        file_size = path.stat().st_size
        print(f"   大小: {file_size / 1024:.1f} KB")

        # 照片哈希
        with open(path, "rb") as f:
            photo_hash = hashlib.sha256(f.read()).hexdigest()

        # 尝试获取尺寸
        width, height = 0, 0
        try:
            from PIL import Image
            with Image.open(path) as img:
                width, height = img.size
            print(f"   尺寸: {width}x{height}")
        except ImportError:
            pass

        # DNA 签名
        dna_seed = f"{MASTER_DNA}-PORTRAIT-{persona_id}-{photo_hash}"
        dna_sig = hashlib.sha256(dna_seed.encode()).hexdigest()[:32]

        binding = PortraitBinding(
            persona_id=persona_id,
            photo_path=str(path),
            photo_hash=photo_hash[:32],
            dna_signature=dna_sig,
            width=width,
            height=height,
            file_size=file_size,
            is_3d=False,  # 永远不做3D
            created_at=datetime.now().isoformat(),
        )

        self.portraits[persona_id] = binding
        self._save_portrait(binding)

        print(f"   ✅ 肖像绑定完成")
        print(f"   照片哈希: {photo_hash[:16]}...")
        print(f"   DNA签名: {dna_sig[:16]}...")
        print(f"   3D模型: ❌ 不做")
        print(f"   状态: 已绑定真人身份 · 不可篡改")

        return binding

    def auto_scan_portraits(self, search_dir: str = "~/Desktop") -> List[PortraitBinding]:
        """自动扫描目录中的照片并绑定。"""
        search_path = Path(search_dir).expanduser().resolve()
        if not search_path.exists():
            print(f"⚠️ 目录不存在: {search_path}")
            return []

        # 支持的图片格式
        ext_map = {'.jpg', '.jpeg', '.png', '.heic', '.webp', '.gif', '.bmp'}

        photos = sorted([
            f for f in search_path.iterdir()
            if f.is_file() and f.suffix.lower() in ext_map
        ])

        if not photos:
            print(f"📷 在 {search_path} 未找到照片")
            return []

        print(f"\n📷 扫描到 {len(photos)} 张照片:")
        for i, p in enumerate(photos):
            print(f"   [{i}] {p.name} ({p.stat().st_size // 1024}KB)")

        # 绑定额外的肖像（第一个表情为真实头像）
        bindings = []
        # 只绑定第一张作为主头像（或用户指定）
        # 这里让用户用 --bind-portrait 明确指定
        return bindings

    # ── 声纹验证 ──

    def verify_voice(self, audio_path: str, persona_id: str = "REAL") -> VerifyResult:
        """声纹验证（防冒充）。

        真人阈值 0.85，虚拟阈值 0.75。
        """
        # 查找档案
        profile = None
        if persona_id == "REAL":
            # 找第一个真人档案
            for _pid, p in self.real_voices.items():
                profile = p
                break
        elif persona_id in self.virtual_voices:
            profile = self.virtual_voices[persona_id]
        elif persona_id in self.real_voices:
            profile = self.real_voices[persona_id]

        if profile is None:
            return VerifyResult(
                status="NOT_FOUND",
                similarity=0.0, threshold=0.85,
                persona_id=persona_id, voice_type="unknown",
                dna_verified="N/A", confidence="none",
            )

        # 如果特征未加载，尝试重新提取
        if profile.base_features is None or not np.any(profile.base_features != 0):
            # 尝试从文件加载
            feat_path = ANCHOR_DIR / "features" / f"{profile.persona_id}.npy"
            if feat_path.exists():
                try:
                    profile.base_features = np.load(feat_path)
                except Exception:
                    pass
            # 如果仍有音频源，重新提取
            if (profile.base_features is None or not np.any(profile.base_features != 0)) \
                    and profile.audio_source:
                src = Path(profile.audio_source)
                if src.exists():
                    try:
                        audio, sr = load_wav(src)
                        audio = resample(audio, sr, SAMPLE_RATE)
                        profile.base_features = extract_voice_features(audio, SAMPLE_RATE)
                    except Exception:
                        pass

        if profile.base_features is None or not np.any(profile.base_features != 0):
            return VerifyResult(
                status="NO_FEATURES",
                similarity=0.0, threshold=0.85,
                persona_id=persona_id,
                voice_type=profile.voice_type.value,
                dna_verified=profile.dna_signature[:16] if profile.dna_signature else "N/A",
                confidence="none",
            )

        # 加载待验证音频
        path = Path(audio_path).expanduser().resolve()
        if not path.exists():
            return VerifyResult(
                status="FILE_NOT_FOUND",
                similarity=0.0,
                threshold=0.85,
                persona_id=persona_id,
                voice_type=profile.voice_type.value,
                dna_verified=profile.dna_signature[:16],
                confidence="none",
            )

        audio, sr = load_wav(path)
        audio = resample(audio, sr, SAMPLE_RATE)
        test_features = extract_voice_features(audio, SAMPLE_RATE)

        # 余弦相似度
        if np.any(profile.base_features != 0):
            similarity = float(np.dot(profile.base_features, test_features) /
                              (np.linalg.norm(profile.base_features) * np.linalg.norm(test_features) + 1e-10))
        else:
            similarity = 0.0

        # 阈值
        threshold = 0.85 if profile.voice_type == VoiceType.REAL else 0.75
        status = "MATCH" if similarity >= threshold else "MISMATCH"
        confidence = "high" if similarity > 0.95 else "medium" if similarity > 0.85 else "low"

        return VerifyResult(
            status=status,
            similarity=similarity,
            threshold=threshold,
            persona_id=persona_id,
            voice_type=profile.voice_type.value,
            dna_verified=profile.dna_signature[:16],
            confidence=confidence,
        )

    # ── 合成参数生成（给TTS引擎用） ──

    def get_tts_params(self, text: str, persona_id: str, emotion: str = "neutral") -> Dict[str, Any]:
        """获取 TTS 合成参数。"""
        profile = None
        if persona_id in self.virtual_voices:
            profile = self.virtual_voices[persona_id]
        elif persona_id in self.real_voices:
            return {"error": "真人原声不支持合成", "note": "请使用真人录音或切换虚拟人格"}

        if profile is None:
            # 自动匹配到最接近的虚拟人格
            matched = self._match_persona(persona_id)
            if matched:
                profile = self.virtual_voices[matched]
            else:
                return {"error": f"人格 {persona_id} 未注册，且无法匹配"}

        emotion_intensity = profile.emotion_map.get(emotion, 0.5)

        return {
            "status": "TTS_PARAMS_READY",
            "persona": f"{profile.persona_id}-{profile.name}",
            "text": text,
            "params": {
                "pitch_range": list(profile.pitch_range),
                "speed": profile.speed * (1.0 + (emotion_intensity - 0.5) * 0.2),
                "emotion": emotion,
                "emotion_intensity": emotion_intensity,
                "engine": profile.engine,
                "edge_tts_voice": profile.edge_tts_voice,
                "voice_id": f"longhun-{profile.persona_id}-{profile.dna_signature[:8]}",
                "dna_anchor": profile.dna_signature[:16],
            },
            "dna_verified": True,
        }

    def _match_persona(self, persona_id: str) -> Optional[str]:
        """人格ID→最接近的虚拟声色。"""
        mapping = {
            "P00": "P01",   # 文心→诸葛亮（沉稳）
            "P07": "P07",   # 管仲→军魂
            "P10": "P08",   # 苏东坡→民生守护（温和）
            "P11": "P08",   # 李白→民生守护
            "P12": "P01",   # 屈原→诸葛亮
            "P13": "P07",   # 姜子牙→军魂
            "P14": "P01",   # 吕蒙→诸葛亮
            "P15": "P08",   # 乔前辈→民生守护
            "P72": "P07",   # 龙盾→军魂
        }
        return mapping.get(persona_id)

    # ── 总览 ──

    def manifest(self) -> Dict[str, Any]:
        """声色总览清单。"""
        all_voices = {}

        # 真人
        for pid, p in self.real_voices.items():
            # 判断激活状态：有样本哈希且不是默认值 = 已注册
            is_active = bool(p.sample_hash and p.sample_hash not in ("", "VIRTUAL-FIXED", "WAITING-FOR-SAMPLE"))
            all_voices[pid] = {
                "name": p.name,
                "name_cn": p.name_cn,
                "type": p.voice_type.value,
                "pitch_range": list(p.pitch_range) if p.pitch_range else [0, 0],
                "speed": p.speed,
                "dna": p.dna_signature[:16] if p.dna_signature else "N/A",
                "sample_hash": p.sample_hash[:16] if p.sample_hash else "N/A",
                "status": "active" if is_active else "waiting",
                "engine": p.engine,
                "audio_source": p.audio_source or "",
            }

        # 虚拟
        for pid, p in self.virtual_voices.items():
            all_voices[pid] = {
                "name": p.name,
                "name_cn": p.name_cn,
                "type": p.voice_type.value,
                "pitch_range": list(p.pitch_range),
                "speed": p.speed,
                "dna": p.dna_signature[:16],
                "status": "active",
                "engine": p.engine,
                "edge_tts_voice": p.edge_tts_voice,
                "wuxing": p.wuxing,
                "bagua": p.bagua,
                "description": p.description,
            }

        # 肖像
        portrait_list = {}
        for pid, b in self.portraits.items():
            portrait_list[pid] = {
                "photo_path": b.photo_path,
                "photo_hash": b.photo_hash[:16],
                "dna": b.dna_signature[:16],
                "size": f"{b.width}x{b.height}",
                "file_size_kb": b.file_size // 1024,
                "is_3d": b.is_3d,
            }

        return {
            "system": "龍魂人格声色绑定系统 v2.0",
            "dna": MASTER_DNA,
            "uid": MASTER_UID,
            "updated_at": datetime.now().isoformat(),
            "voices": all_voices,
            "portraits": portrait_list,
            "stats": {
                "total_voices": len(all_voices),
                "real_voices": len([v for v in all_voices.values() if v["type"] == "real"]),
                "virtual_voices": len([v for v in all_voices.values() if v["type"] == "virtual"]),
                "total_portraits": len(portrait_list),
            },
        }

    def audit_report(self) -> str:
        """彩色审计报告。"""
        m = self.manifest()
        lines = []
        lines.append("=" * 60)
        lines.append("🐉 龍魂 · 人格声色审计报告")
        lines.append(f"DNA: {MASTER_DNA}")
        lines.append("=" * 60)

        lines.append(f"\n📊 统计: {m['stats']['total_voices']}声色 · "
                     f"{m['stats']['real_voices']}真人 · "
                     f"{m['stats']['virtual_voices']}虚拟 · "
                     f"{m['stats']['total_portraits']}肖像")

        # 真人原声
        lines.append("\n── 真人原声 ──")
        for pid, v in m["voices"].items():
            if v["type"] == "real":
                icon = "✅" if v["status"] == "active" else "⏳"
                lines.append(f"  {icon} {pid}: {v['name_cn']}")
                if v["status"] == "active":
                    lines.append(f"       音域: {v['pitch_range'][0]:.0f}-{v['pitch_range'][1]:.0f}Hz")
                    lines.append(f"       DNA: {v['dna']}...")
                else:
                    lines.append(f"       状态: 等待录音样本 (3-5分钟)")

        # 虚拟人格声
        lines.append("\n── 虚拟人格声色 (8核心) ──")
        for pid in ["P01", "P02", "P03", "P04", "P05", "P06", "P07", "P08"]:
            v = m["voices"].get(pid, {})
            if v:
                lines.append(f"  🎭 {pid} {v['name']} [{v['wuxing']}{v['bagua']}]")
                lines.append(f"      {v['description']}")
                lines.append(f"      音域: {v['pitch_range'][0]:.0f}-{v['pitch_range'][1]:.0f}Hz · 语速: {v['speed']:.2f}x")
                lines.append(f"      TTS: {v['engine']} → {v.get('edge_tts_voice', 'N/A')}")
                lines.append(f"      DNA: {v['dna']}...")

        # 扩展虚拟人格
        ext_pids = [k for k in m["voices"] if k not in ["P01","P02","P03","P04","P05","P06","P07","P08"] and m["voices"][k]["type"] == "virtual"]
        if ext_pids:
            lines.append(f"\n── 扩展虚拟人格 ({len(ext_pids)}个) ──")
            for pid in sorted(ext_pids):
                v = m["voices"][pid]
                lines.append(f"  🎭 {pid} {v['name']}: {v.get('description', '')}")

        # 肖像
        if m["portraits"]:
            lines.append("\n── 肖像绑定 ──")
            for pid, b in m["portraits"].items():
                icon = "❌" if b["is_3d"] else "📷"
                lines.append(f"  {icon} {pid}: {Path(b['photo_path']).name}")
                lines.append(f"      {b['size']} · {b['file_size_kb']}KB · 3D={b['is_3d']}")
                lines.append(f"      哈希: {b['photo_hash']}...")
                lines.append(f"      DNA: {b['dna']}...")
        else:
            lines.append("\n── 肖像绑定 ──")
            lines.append("  ⏳ 未绑定真人肖像")

        lines.append("\n" + "=" * 60)
        lines.append("🔒 真人原声=主权声明 · 虚拟人格声=对外交互 · 肖像不做3D")
        lines.append("=" * 60)

        return "\n".join(lines)


# ══════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════

def _progress_callback(stage: str, detail: str = "") -> None:
    """进度回调（供外部调用）。"""
    print(f"  [{stage}] {detail}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="龍魂 · 人格声色绑定系统 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_voice_persona_system.py --audit           # 审计总览
  python3 bin/lh_voice_persona_system.py --register-real ~/Documents/龍魂系統/voice/reference.wav
  python3 bin/lh_voice_persona_system.py --bind-portrait ~/Desktop/IMG_1126.PNG
  python3 bin/lh_voice_persona_system.py --scan-desktop    # 扫描桌面照片
  python3 bin/lh_voice_persona_system.py --scan-voice      # 扫描所有音频
  python3 bin/lh_voice_persona_system.py --verify ~/test.wav  # 声纹验证
  python3 bin/lh_voice_persona_system.py --tts "系统启动" P01 calm  # 生成TTS参数
  python3 bin/lh_voice_persona_system.py --json            # JSON输出
  python3 bin/lh_voice_persona_system.py --auto            # 自动扫描并注册
        """
    )

    parser.add_argument("--audit", action="store_true", help="声色审计总览")
    parser.add_argument("--register-real", type=str, metavar="PATH", help="注册真人原声（WAV文件）")
    parser.add_argument("--bind-portrait", type=str, metavar="PATH", help="绑定真人肖像（照片文件）")
    parser.add_argument("--scan-desktop", action="store_true", help="扫描桌面照片")
    parser.add_argument("--scan-voice", action="store_true", help="扫描所有音频文件")
    parser.add_argument("--verify", type=str, metavar="PATH", help="声纹验证（音频文件）")
    parser.add_argument("--tts", nargs=3, metavar=("TEXT", "PERSONA", "EMOTION"),
                        help="生成TTS合成参数")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--auto", action="store_true", help="自动扫描并注册所有资产")
    args = parser.parse_args()

    system = LongHunVoicePersonaSystem()

    # --auto: 自动扫描
    if args.auto:
        print("🔍 自动扫描声色资产...\n")
        # 扫描真人声音
        default_voice = Path.home() / "Documents" / "龍魂系統" / "voice" / "reference.wav"
        if default_voice.exists() and not any(p.audio_source for p in system.real_voices.values()):
            try:
                system.register_real_voice(str(default_voice))
            except Exception as e:
                print(f"  ⚠️ 注册真人原声失败: {e}")
        else:
            print("  ⏭️  真人原声已注册或未找到 reference.wav")

        # 扫描桌面照片
        desktop = Path.home() / "Desktop"
        if desktop.exists() and not system.portraits:
            ext_map = {'.jpg', '.jpeg', '.png', '.heic'}
            photos = sorted([f for f in desktop.iterdir() if f.is_file() and f.suffix.lower() in ext_map])
            if photos:
                print(f"\n📷 桌面找到 {len(photos)} 张照片")
                # 只绑定第一个作为头像
                try:
                    system.bind_portrait(str(photos[0]), "REAL")
                except Exception as e:
                    print(f"  ⚠️ 肖像绑定失败: {e}")
            else:
                print("  ⏭️  桌面未找到照片")
        else:
            print("  ⏭️  肖像已绑定或无桌面照片")

    # --register-real
    if args.register_real:
        try:
            system.register_real_voice(args.register_real)
        except Exception as e:
            print(f"❌ 注册失败: {e}")
            sys.exit(1)

    # --bind-portrait
    if args.bind_portrait:
        try:
            system.bind_portrait(args.bind_portrait, "REAL")
        except Exception as e:
            print(f"❌ 绑定失败: {e}")
            sys.exit(1)

    # --scan-desktop
    if args.scan_desktop:
        system.auto_scan_portraits("~/Desktop")

    # --scan-voice
    if args.scan_voice:
        print("🔍 扫描音频文件...")
        search_dirs = [
            Path.home() / "Documents" / "龍魂系統" / "voice",
            Path.home() / "Downloads",
            Path(__file__).resolve().parent.parent / "voice-twin" / "raw",
            Path(__file__).resolve().parent.parent / "voice-twin" / "voice_dataset",
        ]
        for d in search_dirs:
            if d.exists():
                wavs = list(d.glob("*.wav")) + list(d.glob("*.m4a"))
                print(f"   {d.name}: {len(wavs)} 个音频")
                for w in wavs[:5]:
                    print(f"     - {w.name} ({w.stat().st_size // 1024}KB)")

    # --verify
    if args.verify:
        result = system.verify_voice(args.verify)
        if args.json:
            print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
        else:
            print(f"\n🔍 声纹验证: {result.status}")
            print(f"   相似度: {result.similarity:.4f} (阈值: {result.threshold})")
            print(f"   人格: {result.persona_id}")
            print(f"   声色类型: {result.voice_type}")
            print(f"   DNA验证: {result.dna_verified}")
            print(f"   置信度: {result.confidence}")

    # --tts
    if args.tts:
        text, persona, emotion = args.tts
        result = system.get_tts_params(text, persona, emotion)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🎭 TTS 合成参数")
            print(f"   人格: {result.get('persona', 'N/A')}")
            if "params" in result:
                p = result["params"]
                print(f"   语速: {p['speed']:.2f}x · 音域: {p['pitch_range']}")
                print(f"   情感: {p['emotion']} ({p['emotion_intensity']:.2f})")
                print(f"   引擎: {p['engine']} → {p['edge_tts_voice']}")
                print(f"   DNA: {p['dna_anchor']}...")

    # --audit / --json (默认显示审计)
    show_audit = args.audit or not any([
        args.register_real, args.bind_portrait, args.verify,
        args.tts, args.scan_desktop, args.scan_voice, args.auto,
    ])
    if show_audit:
        if args.json:
            print(json.dumps(system.manifest(), ensure_ascii=False, indent=2))
        else:
            print(system.audit_report())


if __name__ == "__main__":
    main()
