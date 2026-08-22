#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 UID9622 主权身份卡生成器
LongHun Sovereign Identity Card Generator

功能：
  - 生成 PNG 主权身份卡（含 QR 码、UID、DNA、姓名、注册时间）
  - 支持下载 PNG
  - 生成 HTML 身份卡（便于浏览器打印为 PDF）

DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-SOVEREIGN-CARD-v1.0
"""

import os
import io
import base64
import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from PIL import Image, ImageDraw, ImageFont

from registry import CARDS_DIR, load_manifest, get_identity


def _get_font(size: int) -> ImageFont.FreeTypeFont:
    """获取字体；优先使用系统黑体，否则用默认字体。"""
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _generate_qr_code(data: str, size: int = 200) -> Image.Image:
    """生成 QR 码图片。"""
    try:
        import qrcode
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white").resize((size, size))
    except ImportError:
        # 降级：生成占位矩阵
        img = Image.new("RGB", (size, size), "white")
        draw = ImageDraw.Draw(img)
        n = 21
        step = size // n
        for i in range(n):
            for j in range(n):
                if (i + j) % 3 == 0:
                    draw.rectangle([i*step, j*step, (i+1)*step, (j+1)*step], fill="black")
        return img


def generate_card_png(uid: str, output_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    生成 PNG 主权身份卡。

    Args:
        uid: 主权身份 UID
        output_path: 输出路径；None 则自动生成

    Returns:
        {"status": "success", "path": "...", "base64": "..."}
    """
    record = get_identity(uid)
    if not record:
        return {"status": "error", "message": "主权身份不存在"}

    if output_path is None:
        CARDS_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = CARDS_DIR / f"{uid}_{ts}.png"

    # 卡片尺寸
    W, H = 800, 480
    bg = Image.new("RGB", (W, H), "#0d0d0d")
    draw = ImageDraw.Draw(bg)

    # 金色边框
    border_color = "#d4a017"
    draw.rectangle([10, 10, W-10, H-10], outline=border_color, width=3)

    # 字体
    font_title = _get_font(28)
    font_label = _get_font(18)
    font_value = _get_font(22)
    font_mono = _get_font(16)

    # 标题
    draw.text((40, 40), "🐉 龍魂 UID9622 主权身份卡", fill=border_color, font=font_title)
    draw.line((40, 85, W-40, 85), fill="#2a2a2a", width=1)

    # 信息
    y = 110
    line_h = 42
    info = [
        ("姓名", record.get("name", "")),
        ("UID", record.get("uid", "")),
        ("DNA 追溯码", record.get("dna", "")),
        ("主权哈希", record.get("sovereign_hash", "")[:32] + "..."),
        ("注册时间", record.get("registered_at", "")),
        ("证件类型", record.get("id_type", "")),
    ]
    for label, value in info:
        draw.text((40, y), f"{label}:", fill="#999999", font=font_label)
        draw.text((180, y), str(value), fill="#e8e8e8", font=font_value)
        y += line_h

    # 底部标语
    draw.text((40, H-50), "中国人能用 · 数据主权归己 · 算法根留中国", fill=border_color, font=font_label)

    # QR 码
    qr_data = f"longhun://sovereign?uid={record.get('uid')}&dna={record.get('dna')}&hash={record.get('sovereign_hash')[:16]}"
    qr_img = _generate_qr_code(qr_data, size=180)
    bg.paste(qr_img, (W - 220, 110))
    draw.text((W - 220, 300), "扫码验证身份", fill="#999999", font=font_label)

    # 保存
    bg.save(output_path, "PNG")

    # base64
    with open(output_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")

    return {
        "status": "success",
        "uid": uid,
        "path": str(output_path),
        "base64": b64,
        "mime_type": "image/png",
    }


def generate_card_html(uid: str) -> Dict[str, Any]:
    """生成可打印为 PDF 的 HTML 身份卡。"""
    record = get_identity(uid)
    if not record:
        return {"status": "error", "message": "主权身份不存在"}

    # 先生成 PNG 获取 base64
    png_result = generate_card_png(uid)
    if png_result.get("status") != "success":
        return png_result

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>龍魂 UID9622 主权身份卡 · {record.get('uid')}</title>
  <style>
    body {{ margin:0; background:#0d0d0d; color:#e8e8e8; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif; display:flex; justify-content:center; align-items:center; min-height:100vh; }}
    .card {{ width:800px; border:3px solid #d4a017; border-radius:12px; padding:40px; background:#161616; box-sizing:border-box; }}
    h1 {{ color:#d4a017; margin:0 0 20px; }}
    .row {{ display:flex; justify-content:space-between; margin:16px 0; border-bottom:1px solid #2a2a2a; padding-bottom:8px; }}
    .label {{ color:#999; }}
    .value {{ color:#e8e8e8; font-family:monospace; }}
    .qr {{ text-align:right; }}
    .qr img {{ width:180px; height:180px; }}
    .footer {{ margin-top:30px; color:#d4a017; text-align:center; }}
    @media print {{ body {{ background:#fff; }} .card {{ border-color:#000; }} }}
  </style>
</head>
<body>
  <div class="card">
    <h1>🐉 龍魂 UID9622 主权身份卡</h1>
    <div style="display:flex; justify-content:space-between;">
      <div style="flex:1;">
        <div class="row"><span class="label">姓名</span><span class="value">{record.get('name')}</span></div>
        <div class="row"><span class="label">UID</span><span class="value">{record.get('uid')}</span></div>
        <div class="row"><span class="label">DNA 追溯码</span><span class="value">{record.get('dna')}</span></div>
        <div class="row"><span class="label">主权哈希</span><span class="value">{record.get('sovereign_hash')[:40]}...</span></div>
        <div class="row"><span class="label">注册时间</span><span class="value">{record.get('registered_at')}</span></div>
        <div class="row"><span class="label">证件类型</span><span class="value">{record.get('id_type')}</span></div>
      </div>
      <div class="qr">
        <img src="data:image/png;base64,{png_result['base64']}" alt="QR">
        <div style="color:#999; margin-top:8px;">扫码验证身份</div>
      </div>
    </div>
    <div class="footer">中国人能用 · 数据主权归己 · 算法根留中国</div>
  </div>
</body>
</html>"""

    return {
        "status": "success",
        "uid": uid,
        "html": html,
        "png_base64": png_result["base64"],
    }


if __name__ == "__main__":
    import sys
    uid = sys.argv[1] if len(sys.argv) > 1 else "UID9622-AAAAAA"
    r = generate_card_png(uid)
    print(json.dumps(r, ensure_ascii=False, indent=2))
