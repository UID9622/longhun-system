# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""OCR 封装。优先 PaddleOCR（鲲鹏 ARM 优化）；未安装给降级提示。"""

import io


def ocr_image(image_bytes: bytes) -> str:
    """识别图片文字。返回纯文本。"""
    try:
        from paddleocr import PaddleOCR
        import numpy as np
        import cv2
    except ImportError:
        return "[OCR 引擎未安装: pip install paddlepaddle paddleocr (鲲鹏 ARM 版)]"

    try:
        ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False,
                        show_log=False)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        result = ocr.ocr(img, cls=True)
        lines = []
        for block in result or []:
            for line in block or []:
                if line and len(line) >= 2:
                    lines.append(str(line[1][0]))
        return "\n".join(lines)
    except Exception as e:
        return f"[OCR 失败: {e}]"


def ocr_image_from_file(path: str) -> str:
    with open(path, "rb") as f:
        return ocr_image(f.read())
