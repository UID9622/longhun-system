# DNA: #龍芯⚡️丙午·乙未·乙丑·大有-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""Image generation service for WeChat article covers and illustrations."""

import os
import subprocess
from pathlib import Path
from typing import Optional

from config import get_settings


class ImageService:
    """Generate images for articles using available tools."""

    def __init__(self):
        self.settings = get_settings()
        self.cache_dir = self.settings.CACHE_DIR / "images"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def generate(
        self,
        prompt: str,
        output_path: Optional[str] = None,
        width: int = 900,
        height: int = 500,
        style: str = "chinese_ink",
    ) -> str:
        """Generate an image.

        Tries multiple backends in order:
        1. longhun_senses vision/generation if available
        2. Local placeholder generation with Pillow
        3. External API if configured
        """
        if output_path is None:
            import hashlib
            import time

            h = hashlib.md5(f"{prompt}-{time.time()}".encode()).hexdigest()[:8]
            output_path = str(self.cache_dir / f"image_{h}.png")

        output_path = Path(output_path).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Try longhun_senses first
        if self._try_longhun_senses(prompt, output_path):
            return str(output_path)

        # Try external API (OpenAI / DeepSeek multimodal placeholder)
        if self._try_external_api(prompt, output_path, width, height):
            return str(output_path)

        # Fallback: generate a placeholder with Chinese text
        self._generate_placeholder(prompt, output_path, width, height, style)
        return str(output_path)

    def _try_longhun_senses(self, prompt: str, output_path: Path) -> bool:
        """Try to use longhun_senses for image generation."""
        senses_script = Path("~/.longhun/scripts/longhun_senses/senses_cli.py").expanduser()
        if not senses_script.exists():
            return False

        try:
            # Note: longhun_senses may not support image generation directly,
            # but we leave the hook here for future extension.
            subprocess.run(
                ["python3", str(senses_script), "vision", prompt],
                check=False,
                capture_output=True,
                timeout=60,
            )
            # If it produced an output file, move it to output_path
            return False  # Currently not supported as file output
        except Exception:
            return False

    def _try_external_api(
        self,
        prompt: str,
        output_path: Path,
        width: int,
        height: int,
    ) -> bool:
        """
        外部图片生成 API 已禁用。
        龍魂系统要求所有外部 AI 调用必须经过 DeepSeek 执行器中转，
        OpenAI DALL-E 等直连出口不再保留。
        """
        return False

    def _generate_placeholder(
        self,
        prompt: str,
        output_path: Path,
        width: int,
        height: int,
        style: str,
    ):
        """Generate a placeholder image with text overlay."""
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            raise ImportError("Pillow is required for placeholder image generation")

        # Create gradient background
        img = Image.new("RGB", (width, height), color=(245, 245, 245))
        draw = ImageDraw.Draw(img)

        # Simple gradient
        for y in range(height):
            r = int(20 + (y / height) * 40)
            g = int(40 + (y / height) * 60)
            b = int(60 + (y / height) * 80)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Try to load font
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        ]
        font = None
        for fp in font_paths:
            if os.path.exists(fp):
                try:
                    font = ImageFont.truetype(fp, 36)
                    small_font = ImageFont.truetype(fp, 20)
                    break
                except Exception:
                    continue

        if font is None:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        # Draw title
        title = "龍魂配图"
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text(
            ((width - text_width) / 2, height / 2 - 50),
            title,
            fill=(255, 255, 255),
            font=font,
        )

        # Draw prompt
        prompt_display = prompt[:30] + "..." if len(prompt) > 30 else prompt
        bbox = draw.textbbox((0, 0), prompt_display, font=small_font)
        text_width = bbox[2] - bbox[0]
        draw.text(
            ((width - text_width) / 2, height / 2 + 20),
            prompt_display,
            fill=(200, 200, 200),
            font=small_font,
        )

        # Draw DNA
        from datetime import datetime

        dna = f"#龍芯⚡️{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-IMAGE"
        bbox = draw.textbbox((0, 0), dna, font=small_font)
        text_width = bbox[2] - bbox[0]
        draw.text(
            ((width - text_width) / 2, height - 50),
            dna,
            fill=(150, 150, 150),
            font=small_font,
        )

        img.save(output_path)
