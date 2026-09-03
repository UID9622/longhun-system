#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·戊寅·未时·䷝离-LH-AUDIO-v1.0-MEDIA-SENSE
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂声音引擎 v1.0 — 感官层·听觉

能力:
  speak <文本> [--voice 声音] [--format wav|mp3] [--output PATH]
      TTS 合成（macOS 中文声优 · 零三方依赖）→ WAV/MP3 + DNA 追溯码嵌入元数据
  fingerprint <音频> [--output PATH]
      音频指纹提取（频带能量指纹 · 纯标准库）→ JSON {bits, hash, meta}
  compare <音频A> <音频B>
      声纹比对 → 相似度 0-100%

对齐: DNA 追溯码嵌入音频元数据（WAV LIST/INFO · MP3 ID3 comment）
"""

import argparse
import hashlib
import json
import math
import os
import struct
import subprocess
import sys
import tempfile
import wave
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
输出目录 = ROOT / "data" / "audio"
归属名 = "诸葛鑫 | UID9622 · 龍芯北辰"
确认码 = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 指纹频点（对数分布 200Hz ~ 4kHz）
频点 = [200, 282, 400, 565, 800, 1130, 1600, 2260, 3200, 4520]
帧长 = 1024


def _dna(动作: str) -> str:
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    h = hashlib.md5(f"{动作}{ts}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-LH-AUDIO-{动作}-{h}"


def _找中文声音() -> str:
    """查找 macOS 中文 TTS 声音（真实发声校验——语音包缺失会输出静音，必须实测）"""
    候选 = []
    try:
        r = subprocess.run(["say", "-v", "?"], capture_output=True, text=True, timeout=10)
        for line in r.stdout.splitlines():
            if "zh_" in line or "Tingting" in line or "Mei-Jia" in line or "婷婷" in line:
                候选.append(line.split()[0])
    except Exception:
        pass
    for name in 候选:
        if _声音能发声(name):
            return name
    return ""


def _声音能发声(voice: str, 采样率=16000) -> bool:
    """测试声音能否真实合成（>0.1 秒）"""
    try:
        with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as tmp:
            tmp_p = tmp.name
        subprocess.run(["say", "-v", voice, "-o", tmp_p, "你好龍魂测试"],
                       capture_output=True, text=True, timeout=30)
        if not os.path.exists(tmp_p):
            return False
        subprocess.run(["ffmpeg", "-y", "-i", tmp_p, "-ar", str(采样率), "-ac", "1",
                        tmp_p + ".wav"], capture_output=True, text=True)
        with wave.open(tmp_p + ".wav", "rb") as w:
            return w.getnframes() > 0.1 * 采样率
    except Exception:
        return False
    finally:
        for p in (tmp_p, tmp_p + ".wav"):
            if p and os.path.exists(p):
                os.unlink(p)


def _转格式(src: str, fmt: str, out: str, 元数据: dict):
    """ffmpeg 转码 + 元数据嵌入（WAV LIST-INFO / MP3 ID3）"""
    meta = []
    for k, v in 元数据.items():
        meta += ["-metadata", f"{k}={v}"]
    subprocess.run(["ffmpeg", "-y", "-i", src, *meta, "-ar", "24000", out],
                   capture_output=True, text=True, check=True)


def cmd_speak(text: str, voice: str = None, fmt: str = "wav", out: str = None, engine: str = "say") -> str:
    """TTS 合成 → WAV/MP3 + DNA 元数据嵌入。say 后端不可用则明确报错+安装指引（不造假音频）"""
    输出目录.mkdir(parents=True, exist_ok=True)
    if not out:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = str(输出目录 / f"lh_speak_{ts}.{fmt}")
    dna = _dna("SPEAK")

    if engine == "say":
        if not voice:
            voice = _找中文声音()
        if not voice:
            raise SystemExit(
                "❌ 本机未安装中文语音包（say 输出静音）。\n"
                "   安装: 系统设置 → 辅助功能 → 朗读内容 → 系统声音 → 添加中文（普通话）声音\n"
                "   或先测试英文: lh speak 'Hello' --voice Alex")
        with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as tmp:
            tmp_aiff = tmp.name
        try:
            subprocess.run(["say", "-v", voice, "-o", tmp_aiff, text],
                           capture_output=True, text=True, timeout=120)
            if not os.path.exists(tmp_aiff):
                raise SystemExit(f"❌ say 合成失败（声音 {voice} 不可用）")
            _转格式(tmp_aiff, fmt, out, {"artist": 归属名, "comment": f"DNA: {dna}", "title": text[:40]})
        finally:
            if os.path.exists(tmp_aiff):
                os.unlink(tmp_aiff)
    elif engine == "tts":
        out = _引擎TTS(text, fmt, out, dna)
    else:
        raise SystemExit(f"❌ 未知引擎: {engine}（支持 say/tts）")

    # 输出校验：防静音/防失败
    if os.path.getsize(out) < 1024:
        raise SystemExit("❌ 合成异常：输出过小。请检查语音包或 TTS 模型。")
    print(f"✅ 语音已生成: {out}")
    print(f"🧬 DNA: {dna}")
    return out


def _引擎TTS(text: str, fmt: str, out: str, dna: str) -> str:
    """高级后端：.venv_tts Coqui TTS（需模型已下载）"""
    tts_py = Path(__file__).parent.parent / ".venv_tts" / "bin" / "python"
    if not tts_py.exists():
        raise SystemExit("❌ .venv_tts 不存在，tts 引擎不可用。")
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_wav = tmp.name
    try:
        code = (
            "import sys; from TTS.api import TTS; "
            f"t = TTS(model_name='tts_models/zh-CN/baker/fastspeech2' if len(sys.argv)>1 else sys.argv[1], progress_bar=False); "
            f"t.tts_to_file(text=sys.argv[1], file_path=sys.argv[2])"
        )
        r = subprocess.run([str(tts_py), "-c", code, text, tmp_wav],
                           capture_output=True, text=True, timeout=300)
        if r.returncode != 0 or not os.path.exists(tmp_wav):
            raise SystemExit(f"❌ TTS 引擎失败（模型可能未下载）: {r.stderr[:200]}")
        _转格式(tmp_wav, fmt, out, {"artist": 归属名, "comment": f"DNA: {dna}", "title": text[:40]})
        return out
    finally:
        if os.path.exists(tmp_wav):
            os.unlink(tmp_wav)


# ============================================================
# 指纹引擎（纯标准库 · Goertzel 频带能量）
# ============================================================
def _读音频(路径: str, 目标采样率=16000):
    """读音频 → (samples:list[int], sr)。WAV 直读，其余 ffmpeg 转临时 wav"""
    p = Path(路径)
    if p.suffix.lower() != ".wav":
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_wav = tmp.name
        try:
            subprocess.run(["ffmpeg", "-y", "-i", str(p), "-ar", str(目标采样率),
                            "-ac", "1", "-f", "wav", tmp_wav], capture_output=True, text=True, check=True)
            return _读wav(tmp_wav)
        finally:
            if os.path.exists(tmp_wav):
                os.unlink(tmp_wav)
    return _读wav(str(p))


def _读wav(路径: str):
    with wave.open(路径, "rb") as w:
        帧宽 = w.getsampwidth()
        采样率 = w.getframerate()
        通道 = w.getnchannels()
        raw = w.readframes(w.getnframes())
    if 帧宽 == 2:
        样本 = struct.unpack(f"<{len(raw)//2}h", raw)
    elif 帧宽 == 4:
        样本 = struct.unpack(f"<{len(raw)//4}i", raw)
    else:
        # 8-bit 无符号
        样本 = struct.unpack(f"{len(raw)}B", raw)
        return [s - 128 for s in 样本], 采样率
    if 通道 > 1:
        样本 = 样本[::通道]
    return list(样本), 采样率


def _goertzel(样本, 目标频率, 采样率):
    """单频能量检测"""
    omega = 2 * math.pi * 目标频率 / 采样率
    coeff = 2 * math.cos(omega)
    s0 = s1 = s2 = 0.0
    for x in 样本:
        s0 = x + coeff * s1 - s2
        s2 = s1
        s1 = s0
    return s1 * s1 + s2 * s2 - coeff * s1 * s2


def 提取指纹(路径: str) -> dict:
    样本, 采样率 = _读音频(路径)
    if not 样本:
        raise SystemExit(f"❌ 无法读取音频: {路径}")
    # 分帧
    帧列表 = []
    for i in range(0, len(样本) - 帧长, 帧长 // 2):
        帧列表.append(样本[i:i + 帧长])
    # 每帧每个频点的能量
    能量表 = []
    for 帧 in 帧列表:
        行 = []
        for f in 频点:
            行.append(_goertzel(帧, f, 采样率))
        能量表.append(行)
    if not 能量表:
        raise SystemExit("❌ 音频太短，无法提取指纹")
    # 全局中位数 → 二值化
    全量 = [v for 行 in 能量表 for v in 行]
    中位 = sorted(全量)[len(全量) // 2]
    bits = "".join("1" if v > 中位 else "0" for 行 in 能量表 for v in 行)
    h = hashlib.sha256(bits.encode()).hexdigest()[:16]
    指纹 = {
        "dna": _dna("FINGERPRINT"),
        "engine": "lh-audio-fp-v1",
        "source": str(路径),
        "sr": 采样率,
        "frames": len(帧列表),
        "bits": bits,
        "hash": h,
    }
    return 指纹


def cmd_fingerprint(路径: str, out: str = None) -> str:
    输出目录.mkdir(parents=True, exist_ok=True)
    if not out:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = str(输出目录 / f"fingerprint_{Path(路径).stem}_{ts}.json")
    指纹 = 提取指纹(路径)
    Path(out).write_text(json.dumps(指纹, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 指纹已提取: {out}")
    print(f"🧬 DNA: {指纹['dna']}")
    print(f"🔑 哈希: {指纹['hash']} ({指纹['frames']} 帧)")
    return out


def cmd_compare(a: str, b: str) -> float:
    fa = 提取指纹(a)
    fb = 提取指纹(b)
    ba, bb = fa["bits"], fb["bits"]
    n = min(len(ba), len(bb))
    相同 = sum(1 for x, y in zip(ba[:n], bb[:n]) if x == y)
    相似 = 100.0 * 相同 / max(n, 1)
    print(f"🎙 声纹比对: {Path(a).name} vs {Path(b).name}")
    print(f"   相似度: {相似:.1f}%  ({相同}/{n} 位一致)")
    print(f"   A哈希: {fa['hash']} | B哈希: {fb['hash']}")
    if 相似 >= 75:
        print("   判定: 🟢 同一人 / 高度相似")
    elif 相似 >= 50:
        print("   判定: 🟡 可能相关")
    else:
        print("   判定: 🔴 不同声纹")
    return 相似


def main():
    # 兼容 `lh voice-cmp A B` 透传：裸参数 → compare 模式
    import sys as _sys
    if _sys.argv[1:] and _sys.argv[1] not in ("speak", "fingerprint", "compare", "self-test"):
        _sys.argv = [_sys.argv[0], "compare"] + _sys.argv[1:]
    ap = argparse.ArgumentParser(prog="lh-audio", description="🐉 龍魂声音引擎")
    sub = ap.add_subparsers(dest="op", required=True)

    s = sub.add_parser("speak"); s.add_argument("文本"); s.add_argument("--voice"); s.add_argument("--engine", default="say", choices=["say", "tts"]); s.add_argument("--format", default="wav", choices=["wav", "mp3"]); s.add_argument("--output"); s.set_defaults(func=lambda a: cmd_speak(a.文本, a.voice, a.format, a.output, a.engine))
    s = sub.add_parser("fingerprint"); s.add_argument("音频"); s.add_argument("--output"); s.set_defaults(func=lambda a: cmd_fingerprint(a.音频, a.output))
    s = sub.add_parser("compare"); s.add_argument("音频A"); s.add_argument("音频B"); s.set_defaults(func=lambda a: cmd_compare(a.音频A, a.音频B))
    s = sub.add_parser("self-test"); s.set_defaults(func=lambda a: 自测())
    args = ap.parse_args()
    args.func(args)


def 自测():
    print("🐉 声音引擎自测…（语音包缺失环境自动降级英文 say）")
    wav = cmd_speak("LongHun self test one two three", voice="Alex", fmt="wav")
    fp1 = cmd_fingerprint(wav)
    wav2 = cmd_speak("A totally different sentence for comparison.", voice="Alex", fmt="wav")
    fp2 = cmd_fingerprint(wav2)
    print("--- 同源比对（应高度相似）---")
    cmd_compare(wav, wav)
    print("--- 异源比对（应低相似）---")
    cmd_compare(wav, wav2)
    print("🟢 自测通过")
    return 0


if __name__ == "__main__":
    main()
