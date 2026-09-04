#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 印记二维码生成器 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-QR-CODE-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  1. 生成包含DNA/IPA的印记二维码
  2. 将二维码嵌入视频帧
  3. 从视频中提取二维码

用法：
  lh qr-code generate --dna "DNA-xxx" --output qr.png
  lh qr-code embed --video input.mp4 --output output.mp4 --dna "DNA-xxx"
  lh qr-code extract --video with_qr.mp4

依赖（可选·回退到基础二维码模式）:
  pip install qrcode[pil] opencv-python
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict
from datetime import datetime

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# ---- 可选导入 ----
try:
    import qrcode
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
    from qrcode.image.styles.colormasks import SolidFillColorMask
    HAS_QRCODE_STYLED = True
except ImportError:
    try:
        import qrcode
        HAS_QRCODE_STYLED = False
    except ImportError:
        qrcode = None
        HAS_QRCODE_STYLED = False

try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False


class QRCodeEngine:
    """印记二维码引擎"""
    
    def __init__(self, version: int = 4, box_size: int = 10, border: int = 4):
        self.version = version
        self.box_size = box_size
        self.border = border

    def generate_qr(self, data: str, output_path: Path, color: str = "#FFD60A") -> Dict:
        """生成二维码图片"""
        if qrcode is None:
            return {"status": "error", "message": "需要 qrcode: pip install qrcode[pil]"}

        qr = qrcode.QRCode(
            version=self.version,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=self.box_size,
            border=self.border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        if HAS_QRCODE_STYLED:
            # 龍魂金色风格二维码
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=RoundedModuleDrawer(),
                color_mask=SolidFillColorMask(front_color=color, back_color="#0D1117")
            )
        else:
            img = qr.make_image(fill_color=color.replace("#", ""), back_color="black")

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(output_path))

        return {
            "status": "success",
            "output": str(output_path),
            "data": data,
            "version": self.version,
            "styled": HAS_QRCODE_STYLED
        }

    def embed_qr_to_video(self, input_path: Path, output_path: Path, data: str,
                          position: str = "bottom-right", size_ratio: float = 0.15) -> Dict:
        """将二维码嵌入视频帧角标"""
        if not HAS_CV2:
            return {"status": "error", "message": "需要 opencv-python"}
        if qrcode is None:
            return {"status": "error", "message": "需要 qrcode: pip install qrcode[pil]"}

        # 生成二维码numpy数组
        qr_img = qrcode.make(data)
        qr_np = np.array(qr_img.convert('RGB'))
        qr_np = cv2.cvtColor(qr_np, cv2.COLOR_RGB2BGR)

        cap = cv2.VideoCapture(str(input_path))
        if not cap.isOpened():
            return {"status": "error", "message": "无法打开视频"}

        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

        # 调整二维码大小
        qr_size = int(min(width, height) * size_ratio)
        qr_size = max(qr_size, 50)  # 最小50px
        qr_resized = cv2.resize(qr_np, (qr_size, qr_size))

        # 位置映射
        positions = {
            "bottom-right": (width - qr_size - 20, height - qr_size - 20),
            "top-right": (width - qr_size - 20, 20),
            "bottom-left": (20, height - qr_size - 20),
            "top-left": (20, 20),
            "center": ((width - qr_size) // 2, (height - qr_size) // 2),
        }
        x, y = positions.get(position, (width - qr_size - 20, height - qr_size - 20))
        x = max(0, min(x, width - qr_size))
        y = max(0, min(y, height - qr_size))

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame[y:y+qr_size, x:x+qr_size] = qr_resized
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
            "data": data,
            "position": position,
            "qr_size": qr_size
        }

    def extract_qr_from_video(self, video_path: Path) -> Dict:
        """从视频中提取二维码"""
        if not HAS_CV2:
            return {"status": "error", "message": "需要 opencv-python"}

        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            return {"status": "error", "message": "无法打开视频"}

        ret, frame = cap.read()
        cap.release()
        if not ret:
            return {"status": "error", "message": "无法读取帧"}

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            return {"status": "success", "data": data, "frame": 0}
        return {"status": "error", "message": "未检测到二维码"}


def main():
    parser = argparse.ArgumentParser(description="龍魂 · 印记二维码引擎")
    subparsers = parser.add_subparsers(dest="command")

    p_generate = subparsers.add_parser("generate", help="生成二维码")
    p_generate.add_argument("--dna", required=True, help="要编码的DNA/数据")
    p_generate.add_argument("--output", required=True, help="输出图片路径 (.png)")
    p_generate.add_argument("--color", default="#FFD60A", help="颜色 (默认龍魂金)")

    p_embed = subparsers.add_parser("embed", help="嵌入视频")
    p_embed.add_argument("--video", required=True, help="输入视频")
    p_embed.add_argument("--output", required=True, help="输出视频")
    p_embed.add_argument("--dna", required=True, help="要编码的DNA")
    p_embed.add_argument("--position", default="bottom-right",
                         choices=["top-left", "top-right", "bottom-left", "bottom-right", "center"])
    p_embed.add_argument("--size", type=float, default=0.15, help="二维码大小比例 (0.05-0.5)")

    p_extract = subparsers.add_parser("extract", help="提取二维码")
    p_extract.add_argument("--video", required=True, help="含二维码的视频")

    p_status = subparsers.add_parser("status", help="引擎状态")

    args = parser.parse_args()

    if args.command == "status":
        print(json.dumps({
            "engine": "印记二维码引擎 v1.0",
            "qrcode_lib": qrcode is not None,
            "styled_qr": HAS_QRCODE_STYLED,
            "opencv": HAS_CV2,
            "dna": "#龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-QR-CODE-v1.0-UID9622"
        }, ensure_ascii=False, indent=2))
        return

    engine = QRCodeEngine()

    if args.command == "generate":
        result = engine.generate_qr(args.dna, Path(args.output), args.color)
    elif args.command == "embed":
        result = engine.embed_qr_to_video(Path(args.video), Path(args.output), args.dna,
                                          args.position, args.size)
    elif args.command == "extract":
        result = engine.extract_qr_from_video(Path(args.video))
    else:
        parser.print_help()
        return

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
