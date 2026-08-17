#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂声纹DNA锚定模块（多用户注册版）
LongHun Voice DNA Anchor - Multi-User Registration

功能：
  - 录入声纹特征（麦克风采集，16kHz）
  - 提取声纹特征向量（本地 torchaudio MFCC + MelSpectrogram）
  - 将特征向量转为哈希指纹
  - 将哈希指纹 + 文本内容 + DNA追溯码 + user_id 打包成哈希链
  - 支持特征向量本地加密存储（Fernet + HMAC-SHA256）
  - 写入 ~/.龍魂/voice_anchors/manifest.json

DNA: #龍芯⚡️20260628-VOICE-ANCHOR-v2.0
"""

import os
import sys
import json
import hashlib
import socket
import wave
import datetime
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import numpy as np

warnings.filterwarnings("ignore")

# 龍魂声纹锚定根目录
BASE_DIR = Path.home() / ".龍魂" / "voice_anchors"
MANIFEST_PATH = BASE_DIR / "manifest.json"
AUDIT_LOG_PATH = BASE_DIR / "audit.jsonl"
SAMPLE_RATE = 16000

# 相似度阈值：>=0.92 视为同一人声纹重复
DUPLICATE_SIMILARITY_THRESHOLD = 0.92


def ensure_dirs() -> None:
    """确保目录存在。"""
    BASE_DIR.mkdir(parents=True, exist_ok=True)


def get_local_ip() -> str:
    """获取本地 IP（非 127.0.0.1 优先）。"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def record_audio(duration: int = 5, sr: int = SAMPLE_RATE) -> np.ndarray:
    """
    使用麦克风录制音频。

    Args:
        duration: 录制时长（秒）
        sr: 采样率

    Returns:
        归一化到 [-1, 1] 的 float32 单声道音频数组
    """
    try:
        import pyaudio
    except ImportError as e:
        raise RuntimeError("未安装 pyaudio，无法使用麦克风。请运行: pip install pyaudio") from e

    p = pyaudio.PyAudio()
    chunk = 1024
    format_ = pyaudio.paInt16
    channels = 1

    stream = p.open(
        format=format_,
        channels=channels,
        rate=sr,
        input=True,
        frames_per_buffer=chunk,
    )

    print(f"🎙️  开始录音 {duration} 秒...")
    frames = []
    for _ in range(0, int(sr / chunk * duration)):
        data = stream.read(chunk, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio = np.frombuffer(b"".join(frames), dtype=np.int16).astype(np.float32) / 32768.0
    print(f"✅ 录音完成，采样数: {len(audio)}")
    return audio


def save_wav(path: Path, audio: np.ndarray, sr: int = SAMPLE_RATE) -> None:
    """保存音频为 WAV 文件。"""
    audio_int16 = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio_int16.tobytes())


def load_wav(path: Path) -> Tuple[np.ndarray, int]:
    """加载 WAV 文件，返回 (audio, sr)。"""
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


def _resample(audio: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
    """简单线性重采样到目标采样率。"""
    if orig_sr == target_sr:
        return audio
    try:
        import torchaudio
        audio_tensor = torchaudio.functional.resample(
            torch.from_numpy(audio).unsqueeze(0), orig_freq=orig_sr, new_freq=target_sr
        )
        return audio_tensor.squeeze(0).numpy()
    except Exception:
        # 降级：线性插值
        ratio = target_sr / orig_sr
        n = int(len(audio) * ratio)
        indices = np.linspace(0, len(audio) - 1, n)
        return np.interp(indices, np.arange(len(audio)), audio)


def extract_features(audio: np.ndarray, sr: int = SAMPLE_RATE) -> np.ndarray:
    """
    提取声纹特征向量。

    使用 torchaudio 本地计算 MFCC 与 MelSpectrogram，再对时间轴做统计聚合，
    得到固定维度的特征向量。该向量不依赖外部网络或预训练大模型，可在本地跑通。
    如需 ResNet/VGGVox 等深度模型，可替换此函数为对应推理器。
    """
    import torch
    import torchaudio

    audio = _resample(audio, sr, SAMPLE_RATE)

    max_val = np.max(np.abs(audio))
    if max_val > 1e-6:
        audio = audio / max_val

    waveform = torch.from_numpy(audio).unsqueeze(0).float()

    mfcc_transform = torchaudio.transforms.MFCC(
        sample_rate=SAMPLE_RATE,
        n_mfcc=40,
        melkwargs={
            "n_fft": 400,
            "hop_length": 160,
            "n_mels": 64,
            "center": False,
        },
    )
    mfcc = mfcc_transform(waveform).squeeze(0).numpy()

    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=SAMPLE_RATE,
        n_fft=400,
        hop_length=160,
        n_mels=64,
        center=False,
    )
    mel = mel_transform(waveform).squeeze(0).numpy()
    mel = np.log(mel + 1e-6)

    features = []
    for tensor in (mfcc, mel):
        features.extend([
            np.mean(tensor, axis=1),
            np.std(tensor, axis=1),
            np.percentile(tensor, 25, axis=1),
            np.percentile(tensor, 75, axis=1),
            np.max(tensor, axis=1),
        ])

    feat = np.concatenate(features).astype(np.float32)
    norm = np.linalg.norm(feat)
    if norm > 1e-8:
        feat = feat / norm
    return feat


def features_to_hash(features: np.ndarray) -> str:
    """将特征向量量化为稳定哈希指纹（SHA-256）。"""
    quantized = np.round(features, 6)
    return hashlib.sha256(quantized.tobytes()).hexdigest()


def compute_similarity(feat_a: np.ndarray, feat_b: np.ndarray) -> float:
    """计算两个特征向量的余弦相似度。"""
    denom = np.linalg.norm(feat_a) * np.linalg.norm(feat_b)
    if denom < 1e-12:
        return 0.0
    return float(np.dot(feat_a, feat_b) / denom)


def generate_persona_id(user_id: str, voice_hash: str, text: str) -> str:
    """生成唯一数字人 ID。"""
    seed = f"{user_id}:{voice_hash}:{text}"
    return "LHVP-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16].upper()


def create_dna(
    user_id: str,
    voice_hash: str,
    text: str,
    persona_id: str,
    timestamp: str,
    ip: str,
) -> str:
    """生成 DNA 追溯码：#龍芯⚡️YYYYMMDD-VOICE-{hash8}"""
    base = f"{user_id}:{voice_hash}:{text}:{persona_id}:{timestamp}:{ip}"
    hash8 = hashlib.sha256(base.encode("utf-8")).hexdigest()[:8].upper()
    date = datetime.datetime.fromisoformat(timestamp).strftime("%Y%m%d")
    return f"#龍芯⚡️{date}-VOICE-{hash8}"


def load_manifest() -> Dict[str, Any]:
    """加载 manifest.json。"""
    if not MANIFEST_PATH.exists():
        return {"version": "2.0", "schema": "voice-anchor-v2", "anchors": []}
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_manifest(manifest: Dict[str, Any]) -> None:
    """保存 manifest.json。"""
    ensure_dirs()
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def log_audit(
    action: str,
    persona_id: Optional[str],
    result: str,
    details: Optional[Dict[str, Any]] = None,
) -> None:
    """写入审计日志。"""
    ensure_dirs()
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "action": action,
        "persona_id": persona_id,
        "result": result,
        "details": details or {},
    }
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def get_record_features(record: Dict[str, Any]) -> Optional[np.ndarray]:
    """
    从记录中提取特征向量，兼容旧版明文与新版加密格式。
    新版加密的记录需传入正确 user_id 才能解密。
    """
    user_id = record.get("user_id", "system")

    # 新版：加密存储
    crypto_obj = record.get("feature_vector_crypto")
    if crypto_obj:
        try:
            from crypto import decrypt_features
            return decrypt_features(crypto_obj, user_id)
        except Exception as e:
            warnings.warn(f"解密记录 {record.get('persona_id')} 失败: {e}")
            return None

    # 旧版：明文存储（兼容）
    vec = record.get("feature_vector")
    if vec:
        return np.array(vec, dtype=np.float32)

    return None


def find_duplicate(
    features: np.ndarray,
    manifest: Dict[str, Any],
    user_id: Optional[str] = None,
    threshold: float = DUPLICATE_SIMILARITY_THRESHOLD,
) -> Tuple[Optional[Dict[str, Any]], float]:
    """
    在 manifest 中查找相似声纹。

    如果传入 user_id，则只在该用户下查找；否则全局查找。
    """
    best_record = None
    best_sim = 0.0
    for record in manifest.get("anchors", []):
        if user_id and record.get("user_id", "system") != user_id:
            continue
        stored = get_record_features(record)
        if stored is None or stored.shape != features.shape:
            continue
        sim = compute_similarity(features, stored)
        if sim > best_sim:
            best_sim = sim
            best_record = record
        if sim >= threshold:
            return record, sim
    return best_record, best_sim


def anchor_voice(
    text: str,
    audio: Optional[np.ndarray] = None,
    user_id: str = "system",
    encrypt: bool = True,
    duration: int = 5,
    source: str = "mic",
    sr: int = SAMPLE_RATE,
) -> Dict[str, Any]:
    """
    录入声纹并生成 DNA 锚定链（支持多用户注册）。

    Args:
        text: 锚定文本内容
        audio: 可选，直接传入音频数组；None 则调用麦克风录制
        user_id: 用户ID，默认 system
        encrypt: 是否加密存储特征向量
        duration: 录制时长
        source: 音频来源标记
        sr: 音频采样率

    Returns:
        包含 status / persona_id / dna / similarity / user_id 等字段的字典
    """
    if not text or not text.strip():
        return {"status": "error", "message": "锚定文本不能为空"}
    if not user_id:
        user_id = "system"

    manifest = load_manifest()

    if audio is None:
        print(f"📝 请朗读以下文本进行锚定：\n   「{text}」\n")
        audio = record_audio(duration, sr=sr)

    features = extract_features(audio, sr=sr)
    voice_hash = features_to_hash(features)

    # 同用户内重复检测
    dup, sim = find_duplicate(features, manifest, user_id=user_id)
    if dup:
        log_audit(
            "anchor",
            dup.get("persona_id"),
            "duplicate",
            {"user_id": user_id, "text": text, "similarity": round(sim, 4)},
        )
        return {
            "status": "duplicate",
            "message": "该声纹已锚定",
            "user_id": user_id,
            "persona_id": dup.get("persona_id"),
            "similarity": round(sim, 4),
            "dna": dup.get("dna"),
        }

    persona_id = generate_persona_id(user_id, voice_hash, text)
    timestamp = datetime.datetime.now().isoformat()
    ip = get_local_ip()
    dna = create_dna(user_id, voice_hash, text, persona_id, timestamp, ip)

    record: Dict[str, Any] = {
        "user_id": user_id,
        "persona_id": persona_id,
        "text": text,
        "voice_hash": voice_hash,
        "dna": dna,
        "created_at": timestamp,
        "ip": ip,
        "source": source,
    }

    if encrypt:
        from crypto import encrypt_features
        record["feature_vector_crypto"] = encrypt_features(features, user_id)
    else:
        record["feature_vector"] = features.tolist()

    manifest["anchors"].append(record)
    save_manifest(manifest)

    # 保存原始音频，便于追溯
    audio_path = BASE_DIR / f"{persona_id}.wav"
    save_wav(audio_path, audio, sr=SAMPLE_RATE)

    log_audit(
        "anchor",
        persona_id,
        "success",
        {"user_id": user_id, "text": text, "dna": dna, "ip": ip, "encrypted": encrypt},
    )

    return {
        "status": "success",
        "message": "声纹锚定成功",
        "user_id": user_id,
        "persona_id": persona_id,
        "dna": dna,
        "voice_hash": voice_hash,
        "created_at": timestamp,
        "ip": ip,
        "encrypted": encrypt,
    }


def tts_synthesize(text: str, duration: int = 5, sr: int = SAMPLE_RATE) -> np.ndarray:
    """使用 macOS 本地 `say` 命令合成语音并返回音频数组（测试用）。"""
    import tempfile
    import subprocess

    with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as f:
        aiff_path = Path(f.name)

    try:
        subprocess.run(
            ["say", "-o", str(aiff_path), text],
            check=True,
            capture_output=True,
            text=True,
        )
        wav_path = aiff_path.with_suffix(".wav")
        subprocess.run(
            ["afconvert", "-f", "WAVE", "-d", "LEI16@16000", str(aiff_path), str(wav_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        audio, loaded_sr = load_wav(wav_path)
        target_len = duration * sr
        if len(audio) > target_len:
            audio = audio[:target_len]
        elif len(audio) < target_len:
            audio = np.pad(audio, (0, target_len - len(audio)))
        return _resample(audio, loaded_sr, sr)
    finally:
        try:
            aiff_path.unlink(missing_ok=True)
            aiff_path.with_suffix(".wav").unlink(missing_ok=True)
        except Exception:
            pass


def generate_test_audio(
    frequency: float = 200.0,
    duration: int = 5,
    sr: int = SAMPLE_RATE,
    noise_level: float = 0.01,
) -> np.ndarray:
    """生成测试音频（正弦波 + 噪声），用于无麦克风环境验证。"""
    t = np.linspace(0, duration, int(duration * sr), endpoint=False)
    signal = (
        np.sin(2 * np.pi * frequency * t)
        + 0.5 * np.sin(2 * np.pi * frequency * 2 * t)
        + 0.25 * np.sin(2 * np.pi * frequency * 3 * t)
    )
    signal += 0.1 * np.sin(2 * np.pi * (frequency + 5 * np.sin(2 * np.pi * 3 * t)) * t)
    noise = np.random.randn(len(t)) * noise_level
    audio = signal + noise
    return audio / np.max(np.abs(audio))


if __name__ == "__main__":
    test_text = "我是UID9622，龍魂系统唯一主权者"
    audio = generate_test_audio(frequency=210)
    result = anchor_voice(test_text, audio=audio, user_id="system", source="test")
    print(json.dumps(result, ensure_ascii=False, indent=2))
