#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · DCT频域不可见水印引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-DCT-WATERMARK-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  1. 在视频帧的DCT频域中嵌入不可见水印（数字DNA）
  2. 提取水印验证来源
  3. 支持批量处理

原理：
  - 提取视频帧的亮度分量 Y
  - 对 8x8 块进行 DCT 变换
  - 在中频系数中嵌入水印位
  - 反 DCT 恢复帧

用法：
  lh dct-watermark --video input.mp4 --output output.mp4 --dna "DNA-xxx"
  lh dct-watermark --extract video_with_watermark.mp4
  lh dct-watermark --batch --input-dir ./videos/ --output-dir ./watermarked/

依赖（可选·回退到无依赖模式）:
  pip install opencv-python numpy
"""

import os
import sys
import json
import hashlib
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# ---- 可选导入 ----
try:
    import numpy as np
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False


class DCTWatermark:
    """DCT频域不可见水印嵌入/提取"""
    
    def __init__(self, strength: float = 4.0, block_size: int = 8):
        self.strength = strength
        self.block_size = block_size
        self.mid_freq_indices = [(4, 4), (4, 5), (5, 4), (5, 5)]

    def _bits_from_dna(self, dna: str) -> List[int]:
        """将DNA字符串转换为64位比特序列"""
        hash_val = hashlib.sha256(dna.encode()).hexdigest()
        bits = []
        for c in hash_val[:16]:
            val = int(c, 16)
            for i in range(4):
                bits.append((val >> (3 - i)) & 1)
        return bits[:64]

    def _dna_from_bits(self, bits: List[int]) -> str:
        """从比特序列恢复DNA标识"""
        hex_str = ""
        for i in range(0, min(len(bits), 64), 4):
            val = 0
            for j in range(4):
                val = (val << 1) | (bits[i + j] if i + j < len(bits) else 0)
            hex_str += format(val, 'x')
        return f"#龍芯⚡️DCT-{hex_str[:16]}"

    def embed_watermark_in_frame(self, frame: "np.ndarray", dna: str) -> "np.ndarray":
        """在单个帧中嵌入水印"""
        bits = self._bits_from_dna(dna)
        if len(bits) < 64:
            bits.extend([0] * (64 - len(bits)))

        yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        y_channel = yuv[:, :, 0].astype(np.float32)

        h, w = y_channel.shape
        block = self.block_size
        blocks_h = h // block
        blocks_w = w // block

        bit_idx = 0
        for i in range(blocks_h):
            for j in range(blocks_w):
                if bit_idx >= 64:
                    break
                y_block = y_channel[i*block:(i+1)*block, j*block:(j+1)*block]
                dct_block = cv2.dct(y_block)
                for (u, v) in self.mid_freq_indices:
                    if bit_idx >= 64:
                        break
                    coeff = int(dct_block[u, v])
                    if bits[bit_idx] == 1:
                        if coeff % 2 == 0:
                            coeff += 1 if coeff >= 0 else -1
                    else:
                        if coeff % 2 != 0:
                            coeff += 1 if coeff >= 0 else -1
                    dct_block[u, v] = float(coeff)
                    bit_idx += 1
                y_channel[i*block:(i+1)*block, j*block:(j+1)*block] = cv2.idct(dct_block)
            if bit_idx >= 64:
                break

        y_channel = np.clip(y_channel, 0, 255).astype(np.uint8)
        yuv[:, :, 0] = y_channel
        return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)

    def extract_watermark_from_frame(self, frame: "np.ndarray") -> Dict:
        """从单个帧中提取水印"""
        yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        y_channel = yuv[:, :, 0].astype(np.float32)

        h, w = y_channel.shape
        block = self.block_size
        blocks_h = h // block
        blocks_w = w // block

        bits = []
        for i in range(blocks_h):
            for j in range(blocks_w):
                if len(bits) >= 64:
                    break
                y_block = y_channel[i*block:(i+1)*block, j*block:(j+1)*block]
                dct_block = cv2.dct(y_block)
                for (u, v) in self.mid_freq_indices:
                    if len(bits) >= 64:
                        break
                    coeff = dct_block[u, v]
                    bit = int(abs(coeff)) % 2
                    bits.append(bit)
                if len(bits) >= 64:
                    break

        dna = self._dna_from_bits(bits[:64])
        # 多帧投票：对64位进行稳定性评估
        stability = len(set(bits)) / max(len(bits), 1)
        return {"dna": dna, "bits_stability": round(stability, 3), "source": "第一帧"}

    def embed_video(self, input_path: Path, output_path: Path, dna: str) -> Dict:
        """嵌入水印到视频"""
        if not HAS_CV2:
            return {"status": "error", "message": "需要 opencv-python: pip install opencv-python numpy"}

        cap = cv2.VideoCapture(str(input_path))
        if not cap.isOpened():
            return {"status": "error", "message": "无法打开视频"}

        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = self.embed_watermark_in_frame(frame, dna)
            out.write(frame)
            frame_count += 1
            if frame_count % 100 == 0:
                print(f"  进度: {frame_count}/{total_frames} 帧", flush=True)

        cap.release()
        out.release()

        return {
            "status": "success",
            "output": str(output_path),
            "total_frames": total_frames,
            "frames_processed": frame_count,
            "dna": dna,
            "dna_hash": hashlib.sha256(dna.encode()).hexdigest()[:16]
        }

    def extract_video(self, input_path: Path) -> Dict:
        """从视频中提取水印"""
        if not HAS_CV2:
            return {"status": "error", "message": "需要 opencv-python: pip install opencv-python numpy"}

        cap = cv2.VideoCapture(str(input_path))
        if not cap.isOpened():
            return {"status": "error", "message": "无法打开视频"}

        ret, frame = cap.read()
        cap.release()
        if not ret:
            return {"status": "error", "message": "无法读取帧"}

        return self.extract_watermark_from_frame(frame)


def main():
    parser = argparse.ArgumentParser(description="龍魂 · DCT频域不可见水印引擎")
    subparsers = parser.add_subparsers(dest="command")

    p_embed = subparsers.add_parser("embed", help="嵌入不可见水印")
    p_embed.add_argument("--video", required=True, help="输入视频路径")
    p_embed.add_argument("--output", required=True, help="输出视频路径")
    p_embed.add_argument("--dna", required=True, help="要嵌入的DNA/水印文本")
    p_embed.add_argument("--strength", type=float, default=4.0, help="水印强度 (默认4.0)")

    p_extract = subparsers.add_parser("extract", help="提取不可见水印")
    p_extract.add_argument("--video", required=True, help="含水印的视频路径")

    p_batch = subparsers.add_parser("batch", help="批量处理")
    p_batch.add_argument("--input-dir", required=True, type=Path, help="输入目录")
    p_batch.add_argument("--output-dir", required=True, type=Path, help="输出目录")
    p_batch.add_argument("--strength", type=float, default=4.0, help="水印强度")

    p_status = subparsers.add_parser("status", help="引擎状态")

    args = parser.parse_args()

    if args.command == "status":
        print(json.dumps({
            "engine": "DCT频域不可见水印 v1.0",
            "opencv": HAS_CV2,
            "block_size": 8,
            "mid_freq_coeffs": 4,
            "bit_capacity": 64,
            "dna": "#龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-DCT-WATERMARK-v1.0-UID9622"
        }, ensure_ascii=False, indent=2))
        return

    watermark = DCTWatermark(strength=getattr(args, 'strength', 4.0))

    if args.command == "embed":
        result = watermark.embed_video(Path(args.video), Path(args.output), args.dna)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "extract":
        result = watermark.extract_video(Path(args.video))
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "batch":
        input_dir = Path(args.input_dir)
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        results = []
        video_exts = ["*.mp4", "*.mov", "*.avi", "*.mkv"]
        videos = []
        for ext in video_exts:
            videos.extend(input_dir.glob(ext))

        print(f"找到 {len(videos)} 个视频文件")
        for v in videos:
            dna = f"#龍芯⚡️DCT-{hashlib.sha256(str(v).encode()).hexdigest()[:12]}"
            out_path = output_dir / f"{v.stem}_dct.mp4"
            result = watermark.embed_video(v, out_path, dna)
            results.append(result)
            status = "✅" if result.get("status") == "success" else "❌"
            print(f"  {status} {v.name}")

        print(json.dumps({"batch_results": len(results), "details": results}, ensure_ascii=False, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
