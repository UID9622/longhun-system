# #龍芯⚡️20260721143752-AUTO-DNA-LUBAN-FONT-LOADER
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-07-21-LUBAN-FONT-LOADER-v1.0
"""
字体加载器：让鲁班大师识别并加载任意字体。

支持格式：TTF / OTF / WOFF / WOFF2 / 系统字体名
加载策略：用户指定字体 → 系统字体 → LonghunFont 回退
"""

import io
import struct
from pathlib import Path
from typing import Optional, Union

from fontTools.ttLib import TTFont
from PIL import ImageFont

DNA = "#龍芯⚡️2026-07-21-LUBAN-FONT-LOADER-v1.0"


# macOS / Linux / Windows 常见中文字体候选路径
_FONT_CANDIDATES = [
    # macOS
    "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/88d6cc32a907955efa1d014207889413890573be.asset/AssetData/Kaiti.ttc",
    "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/a304e3396d019087ab67af77f5e398977529007d.asset/AssetData/Libian.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    # Linux
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/arphic/uming.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    # Windows
    "C:/Windows/Fonts/simkai.ttf",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/msyh.ttc",
]


def _unpack_woff_header(data: bytes) -> tuple[int, int]:
    """解析 WOFF 头，返回 sfnt 大小与表目录偏移。"""
    signature, flavor, length = struct.unpack(">4sII", data[:12])
    if signature not in (b"wOFF", b"wOF2"):
        raise ValueError("不是有效的 WOFF/WOFF2 文件")
    num_tables, = struct.unpack(">H", data[12:14])
    return length, num_tables


def _is_woff(path: Union[str, Path]) -> bool:
    p = Path(path)
    return p.suffix.lower() in (".woff", ".woff2")


def _convert_woff_to_ttf(path: Union[str, Path]) -> bytes:
    """将 WOFF/WOFF2 转换为 sfnt 字节流（TTF/OTF 内部格式）。"""
    from fontTools.ttLib import TTLibError
    try:
        font = TTFont(str(path))
        buf = io.BytesIO()
        font.flavor = None
        font.save(buf)
        return buf.getvalue()
    except TTLibError as exc:
        raise RuntimeError(f"无法解析字体 {path}: {exc}")


class FontLoader:
    """
    通用字体加载器。

    用法：
        loader = FontLoader("/path/to/my.ttf")
        pil_font = loader.get_pil_font(size=120)
        tt_font = loader.get_ttfont()
        char_exists = loader.has_char("龍")
    """

    def __init__(self, font_path: Optional[Union[str, Path]] = None):
        self.user_path: Optional[Path] = None
        self.resolved_path: Path = self._resolve(font_path)
        self._ttfont: Optional[TTFont] = None
        self._pil_cache: dict[int, ImageFont.FreeTypeFont] = {}

    def _resolve(self, font_path: Optional[Union[str, Path]]) -> Path:
        if font_path:
            p = Path(font_path)
            if p.exists():
                self.user_path = p
                return p

        # 依次回退到系统字体
        for candidate in _FONT_CANDIDATES:
            cp = Path(candidate)
            if cp.exists():
                return cp

        # 最后回退到项目输出目录的 LonghunFont
        longhun_otf = Path(__file__).parent.parent / "output" / "LonghunFont-Regular.otf"
        if longhun_otf.exists():
            return longhun_otf

        raise RuntimeError(
            "未找到任何可用中文字体。请安装系统字体或提供字体文件路径。"
        )

    def get_ttfont(self) -> TTFont:
        """返回 fontTools 字体对象。"""
        if self._ttfont is None:
            if _is_woff(self.resolved_path):
                data = _convert_woff_to_ttf(self.resolved_path)
                self._ttfont = TTFont(io.BytesIO(data))
            else:
                self._ttfont = TTFont(str(self.resolved_path))
        return self._ttfont

    def get_pil_font(self, size: int) -> ImageFont.FreeTypeFont:
        """返回 PIL 字体对象（用于位图渲染）。"""
        if size not in self._pil_cache:
            if _is_woff(self.resolved_path):
                data = _convert_woff_to_ttf(self.resolved_path)
                self._pil_cache[size] = ImageFont.truetype(
                    io.BytesIO(data), size
                )
            else:
                self._pil_cache[size] = ImageFont.truetype(
                    str(self.resolved_path), size
                )
        return self._pil_cache[size]

    def has_char(self, char: str) -> bool:
        """检查字体是否包含某个字符。"""
        tt = self.get_ttfont()
        cmap = tt.getBestCmap()
        if not cmap:
            return False
        return ord(char) in cmap

    def get_char_glyph_name(self, char: str) -> Optional[str]:
        """获取字符对应的字形名。"""
        tt = self.get_ttfont()
        cmap = tt.getBestCmap()
        if not cmap or ord(char) not in cmap:
            return None
        return cmap[ord(char)]

    def get_font_info(self) -> dict:
        """提取字体元信息。"""
        tt = self.get_ttfont()
        info = {
            "path": str(self.resolved_path),
            "user_specified": bool(self.user_path),
            "sfnt_version": tt.sfntVersion,
            "num_glyphs": len(tt.getGlyphSet()),
            "tables": list(tt.keys()),
        }
        try:
            name_table = tt["name"]
            info["family"] = name_table.getBestFamilyName()
            info["subfamily"] = name_table.getBestSubFamilyName()
            info["full_name"] = name_table.getBestFullName()
        except Exception:
            info["family"] = self.resolved_path.stem
        return info


def find_system_fonts() -> list[Path]:
    """返回系统中找到的中文字体路径列表。"""
    return [Path(p) for p in _FONT_CANDIDATES if Path(p).exists()]


def is_cjk(char: str) -> bool:
    """判断字符是否属于 CJK 统一表意文字。"""
    code = ord(char)
    return (
        0x4E00 <= code <= 0x9FFF
        or 0x3400 <= code <= 0x4DBF
        or 0xF900 <= code <= 0xFAFF
        or 0x20000 <= code <= 0x2A6DF
        or 0x2A700 <= code <= 0x2B73F
        or 0x2B740 <= code <= 0x2B81F
    )


if __name__ == "__main__":
    loader = FontLoader()
    print("字体信息:", loader.get_font_info())
    print("DNA:", DNA)
