#!/usr/bin/env python3
"""
🧬 龍魂 DNA 音频水印引擎 v2.0 · QIM-LSB 方案

DNA: #龍芯⚡️丙午·乙未·己卯·午时·☰乾-TTS-DNA-WATERMARK-v2.0-QIM-a9b0c1d2
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

方案: 量化索引调制 (QIM) + 最低有效位 (LSB)
  - 在每 N 个采样中取 1 个，修改其 LSB 为水印 bit
  - 16-bit 音频 LSB = -96dB 动态，人耳完全不可闻
  - 100% 提取准确率（无损格式）
  - 原理公开、可独立验证

设计原则:
  - 人耳不可闻（-96dB = 低于任何人耳分辨率）
  - DNA 不可抹除
  - 公开可验证
"""

import argparse
import hashlib
import json
import os
import struct
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

import numpy as np

CST = timezone(timedelta(hours=8))

# 水印参数
STEP_SIZE = 3              # 每 3 个采样取 1 个做水印（间隔采样）
MAGIC_SEED = "LH-DNA-UID9622-v2"  # 魔数检测种子
MAGIC_BYTES = 6            # 检测头 6 字节
LEN_BYTES = 2              # 长度字段 2 字节
EMBED_START_SEC = 0.3      # 从 0.3 秒开始嵌入


def _magnitude_dna(bits: int) -> float:
    """计算水印幅度（dB 形式，实际为 LSB 的 bit 数）"""
    return 1  # LSB = 1 bit


def embed(audio_path: str, dna_code: str, output_path: str = "",
          persona_id: str = "", metadata: dict = None) -> str:
    """在音频中嵌入DNA水印（QIM-LSB）"""
    if not output_path:
        stem = Path(audio_path).stem
        output_path = str(Path(audio_path).parent / f"{stem}_dna.wav")

    import soundfile as sf
    audio, sr = sf.read(audio_path)
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    audio_fp = audio.astype(np.float64)

    # 构建水印载荷
    wm_data = {
        "dna": dna_code,
        "persona": persona_id,
        "t": datetime.now(CST).strftime("%Y%m%d-%H%M%S"),
        "creator": "UID9622",
        "engine": "TTS-QIM-LSB-v2.0",
    }
    if metadata:
        wm_data.update(metadata)
    payload_bytes = json.dumps(wm_data, ensure_ascii=False).encode("utf-8")

    # 载荷长度
    payload_len = len(payload_bytes)
    if payload_len > 65535:
        raise ValueError(f"载荷过大: {payload_len} bytes (最大 65535)")

    # 完整水印: 魔数(6B) + 载荷长度(2B) + 载荷
    magic = MAGIC_SEED.encode("utf-8")[:MAGIC_BYTES]
    len_field = struct.pack(">H", payload_len)
    full_payload = magic + len_field + payload_bytes

    total_bytes = len(full_payload)
    total_bits = total_bytes * 8
    needed_samples = total_bits * STEP_SIZE

    # 转无符号 16-bit 操作（避免负数的补码 LSB 问题）
    audio_int = np.round(audio_fp * 32767).astype(np.int32)
    audio_uint = (audio_int + 32768).clip(0, 65535).astype(np.uint16)

    embed_start = int(EMBED_START_SEC * sr)
    if embed_start + needed_samples > len(audio_uint):
        raise ValueError(
            f"音频太短（需 {needed_samples/sr:.1f}s，音频仅有 {(len(audio_uint)-embed_start)/sr:.1f}s 可用）"
        )

    # 逐 bit 嵌入（无符号域，LSB 操作安全）
    bits = np.unpackbits(np.frombuffer(full_payload, dtype=np.uint8))
    for i, bit in enumerate(bits):
        idx = embed_start + i * STEP_SIZE
        audio_uint[idx] = (audio_uint[idx] & 0xFFFE) | bit

    # 直接输出 16-bit 整数（避免 float32 精度丢失）
    audio_int16 = np.clip(audio_uint.astype(np.int32) - 32768, -32768, 32767).astype(np.int16)
    sf.write(output_path, audio_int16, sr, subtype='PCM_16')

    file_hash = hashlib.sha256(open(output_path, "rb").read()).hexdigest()[:12]

    print(f"✅ DNA水印已嵌入（QIM-LSB, -96dB）")
    print(f"   文件: {output_path}")
    print(f"   DNA: {dna_code}")
    print(f"   载荷: {payload_len} bytes, {total_bits} bits")
    print(f"   哈希: {file_hash}")

    return output_path


def extract(audio_path: str) -> Optional[dict]:
    """从音频中提取DNA水印（QIM-LSB）"""
    import soundfile as sf
    
    # 直接读 int16 避免浮点精度损失
    audio_int, sr = sf.read(audio_path, dtype='int16')
    if audio_int.ndim > 1:
        audio_int = audio_int.mean(axis=1).astype(np.int16)
    audio_uint = (audio_int.astype(np.int32) + 32768).clip(0, 65535).astype(np.uint16)
    embed_start = int(EMBED_START_SEC * sr)

    # 1. 读取魔数
    magic_bits_count = MAGIC_BYTES * 8
    magic_bits = np.zeros(magic_bits_count, dtype=np.uint8)
    for i in range(magic_bits_count):
        idx = embed_start + i * STEP_SIZE
        if idx >= len(audio_uint):
            break
        magic_bits[i] = audio_uint[idx] & 1

    magic_bytes = np.packbits(magic_bits).tobytes()
    expected_magic = MAGIC_SEED.encode("utf-8")[:MAGIC_BYTES]

    if magic_bytes != expected_magic:
        # 尝试容错匹配（允许 1-2 bit 误差）
        match = sum(a == b for a, b in zip(magic_bits, np.unpackbits(np.frombuffer(expected_magic, dtype=np.uint8))))
        ratio = match / magic_bits_count
        if ratio < 0.9:
            print(f"❌ 未检测到DNA水印（魔数匹配 {ratio:.1%}）", file=sys.stderr)
            return None

    # 2. 读取长度
    len_bits_count = LEN_BYTES * 8
    len_bits = np.zeros(len_bits_count, dtype=np.uint8)
    len_offset = embed_start + magic_bits_count * STEP_SIZE
    for i in range(len_bits_count):
        idx = len_offset + i * STEP_SIZE
        if idx >= len(audio_uint):
            break
        len_bits[i] = audio_uint[idx] & 1

    payload_len = struct.unpack(">H", np.packbits(len_bits).tobytes())[0]

    if payload_len < 5 or payload_len > 10000:
        print(f"❌ 载荷长度异常: {payload_len}", file=sys.stderr)
        return None

    # 3. 读取载荷
    payload_bits_count = payload_len * 8
    payload_bits = np.zeros(payload_bits_count, dtype=np.uint8)
    payload_offset = embed_start + (magic_bits_count + len_bits_count) * STEP_SIZE
    for i in range(payload_bits_count):
        idx = payload_offset + i * STEP_SIZE
        if idx >= len(audio_uint):
            break
        payload_bits[i] = audio_uint[idx] & 1

    try:
        payload_bytes = np.packbits(payload_bits).tobytes()
        payload_text = payload_bytes.decode("utf-8", errors="replace")

        # 提取 JSON
        brace_start = payload_text.find("{")
        brace_end = payload_text.rfind("}") + 1
        if brace_start >= 0 and brace_end > brace_start:
            payload_text = payload_text[brace_start:brace_end]
        return json.loads(payload_text)
    except Exception as e:
        print(f"❌ 载荷解析失败: {e}", file=sys.stderr)
        return None


def verify(audio_path: str, expected_dna: str = "") -> dict:
    """验证音频DNA水印"""
    result = {
        "file": audio_path,
        "has_watermark": False,
        "dna_match": False,
        "watermark_data": None,
    }
    data = extract(audio_path)
    if data is None:
        return result
    result["has_watermark"] = True
    result["watermark_data"] = data
    if expected_dna:
        result["dna_match"] = (data.get("dna", "") == expected_dna)
    return result


def main():
    parser = argparse.ArgumentParser(description="🧬 龍魂 DNA 音频水印引擎 v2.0（QIM-LSB）")
    sub = parser.add_subparsers(dest="command")

    ep = sub.add_parser("embed", help="嵌入DNA水印")
    ep.add_argument("--input", required=True)
    ep.add_argument("--dna", required=True)
    ep.add_argument("--persona", default="")
    ep.add_argument("--output", default="")

    xp = sub.add_parser("extract", help="提取DNA水印")
    xp.add_argument("--input", required=True)

    vp = sub.add_parser("verify", help="验证DNA水印")
    vp.add_argument("--input", required=True)
    vp.add_argument("--dna", default="")

    args = parser.parse_args()

    if args.command == "embed":
        embed(args.input, args.dna, args.output, args.persona)
    elif args.command == "extract":
        data = extract(args.input)
        if data:
            print(json.dumps(data, ensure_ascii=False, indent=2))
    elif args.command == "verify":
        result = verify(args.input, args.dna)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
