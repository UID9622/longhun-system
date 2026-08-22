#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# #龍芯⚡️丙午·乙未·丙申·乙未·䷊泰-AUTO-DNA-LUBAN-STYLE-TRANSFER
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-LUBAN-STYLE-TRANSFER-v1.0
"""
书法风格迁移：把任意字体的字形轮廓转换为书法风格。

支持：
- 预设风格（颜真卿楷书、王羲之行书、张旭草书、隶书、篆书等）
- 自定义风格 JSON（与 calligraphy/styles/ 兼容）
- 倾斜、笔压、随机抖动、墨韵飞白
"""

import json
import math
import random
from pathlib import Path
from typing import Any, Optional, Union

DNA = "#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-LUBAN-STYLE-TRANSFER-v1.0"

DEFAULT_STYLE = {
    "name": "鲁班-通用书法",
    "code": "LUBAN-GENERAL",
    "category": "综合",
    "artist": "鲁班大师",
    "era": "当代",
    "description": "任意字体的通用书法化，智能笔锋与墨韵",
    "dna": DNA,
    "parameters": {
        "font_size": 220,
        "stroke_width": 28,
        "slant": 0.06,
        "ink_pressure": 0.8,
        "tip_style": "balanced",
        "spacing_x": 1.12,
        "spacing_y": 1.2,
        "randomness": 0.02,
        "background": "宣纸米黄",
        "ink_color": "#1a1d1a",
        "taper_in": 0.15,
        "taper_out": 0.12,
        "horizontal_thin": 0.75,
        "vertical_thick": 1.15,
    },
}


class StyleParameters:
    """书法风格参数容器。"""

    def __init__(self, style_dict: dict[str, Any]):
        self.raw = style_dict
        self.params = style_dict.get("parameters", {})

    @property
    def font_size(self) -> int:
        return int(self.params.get("font_size", 220))

    @property
    def stroke_width(self) -> float:
        return float(self.params.get("stroke_width", 28))

    @property
    def slant(self) -> float:
        return float(self.params.get("slant", 0.06))

    @property
    def ink_pressure(self) -> float:
        return float(self.params.get("ink_pressure", 0.8))

    @property
    def tip_style(self) -> str:
        return self.params.get("tip_style", "balanced")

    @property
    def spacing_x(self) -> float:
        return float(self.params.get("spacing_x", 1.12))

    @property
    def spacing_y(self) -> float:
        return float(self.params.get("spacing_y", 1.2))

    @property
    def randomness(self) -> float:
        return float(self.params.get("randomness", 0.02))

    @property
    def background(self) -> str:
        return self.params.get("background", "宣纸米黄")

    @property
    def ink_color(self) -> str:
        return self.params.get("ink_color", "#1a1d1a")

    @property
    def taper_in(self) -> float:
        return float(self.params.get("taper_in", 0.15))

    @property
    def taper_out(self) -> float:
        return float(self.params.get("taper_out", 0.12))

    @property
    def horizontal_thin(self) -> float:
        return float(self.params.get("horizontal_thin", 0.75))

    @property
    def vertical_thick(self) -> float:
        return float(self.params.get("vertical_thick", 1.15))

    def to_dict(self) -> dict[str, Any]:
        return self.raw


def load_style(style_code_or_path: Optional[Union[str, Path]] = None) -> StyleParameters:
    """
    加载书法风格。

    参数：
        style_code_or_path: 风格代码（如 YZQ-KA）、JSON 文件路径，或 None 用默认。
    """
    if style_code_or_path is None:
        return StyleParameters(DEFAULT_STYLE)

    p = Path(style_code_or_path)
    if p.exists() and p.suffix == ".json":
        with open(p, "r", encoding="utf-8") as f:
            return StyleParameters(json.load(f))

    # 在 calligraphy/styles 中按 code 查找
    styles_dir = Path(__file__).parent.parent / "calligraphy" / "styles"
    if styles_dir.exists():
        for json_file in styles_dir.glob("*.json"):
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("code") == str(style_code_or_path) or json_file.stem == str(style_code_or_path):
                    return StyleParameters(data)

    # 尝试已知预设
    preset = _PRESETS.get(str(style_code_or_path))
    if preset:
        return StyleParameters(preset)

    return StyleParameters(DEFAULT_STYLE)


def list_styles() -> list[dict[str, Any]]:
    """列出所有可用风格（calligraphy/styles + 内置预设）。"""
    results = []
    styles_dir = Path(__file__).parent.parent / "calligraphy" / "styles"
    if styles_dir.exists():
        for json_file in sorted(styles_dir.glob("*.json")):
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                results.append({
                    "code": data.get("code"),
                    "name": data.get("name"),
                    "category": data.get("category"),
                    "era": data.get("era"),
                    "source": str(json_file),
                })
    for code, data in _PRESETS.items():
        results.append({
            "code": code,
            "name": data.get("name"),
            "category": data.get("category"),
            "era": data.get("era"),
            "source": "built-in",
        })
    return results


_PRESETS: dict[str, dict[str, Any]] = {
    "LUBAN-KA": {
        "name": "鲁班-楷书",
        "code": "LUBAN-KA",
        "category": "楷书",
        "artist": "鲁班大师",
        "era": "当代",
        "description": "方正端庄，横细竖粗，适合标题与正文",
        "dna": "#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-LUBAN-KA-v1.0",
        "parameters": {
            "font_size": 220,
            "stroke_width": 32,
            "slant": 0.02,
            "ink_pressure": 0.9,
            "tip_style": "square",
            "spacing_x": 1.15,
            "spacing_y": 1.25,
            "randomness": 0.01,
            "background": "宣纸米黄",
            "ink_color": "#1a1d1a",
            "taper_in": 0.1,
            "taper_out": 0.08,
            "horizontal_thin": 0.7,
            "vertical_thick": 1.2,
        },
    },
    "LUBAN-XS": {
        "name": "鲁班-行书",
        "code": "LUBAN-XS",
        "category": "行书",
        "artist": "鲁班大师",
        "era": "当代",
        "description": "行云流水，略带倾斜，适合长文本与题跋",
        "dna": "#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-LUBAN-XS-v1.0",
        "parameters": {
            "font_size": 220,
            "stroke_width": 26,
            "slant": 0.08,
            "ink_pressure": 0.8,
            "tip_style": "flowing",
            "spacing_x": 1.12,
            "spacing_y": 1.2,
            "randomness": 0.03,
            "background": "宣纸本白",
            "ink_color": "#2b1d0e",
            "taper_in": 0.18,
            "taper_out": 0.15,
            "horizontal_thin": 0.8,
            "vertical_thick": 1.1,
        },
    },
    "LUBAN-CA": {
        "name": "鲁班-草书",
        "code": "LUBAN-CA",
        "category": "草书",
        "artist": "鲁班大师",
        "era": "当代",
        "description": "笔势连绵，飞白张扬，适合艺术大字",
        "dna": "#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-LUBAN-CA-v1.0",
        "parameters": {
            "font_size": 240,
            "stroke_width": 22,
            "slant": 0.14,
            "ink_pressure": 0.65,
            "tip_style": "wild",
            "spacing_x": 1.08,
            "spacing_y": 1.15,
            "randomness": 0.06,
            "background": "仿古宣纸",
            "ink_color": "#1f1810",
            "taper_in": 0.25,
            "taper_out": 0.22,
            "horizontal_thin": 0.85,
            "vertical_thick": 1.05,
        },
    },
    "LUBAN-LI": {
        "name": "鲁班-隶书",
        "code": "LUBAN-LI",
        "category": "隶书",
        "artist": "鲁班大师",
        "era": "当代",
        "description": "蚕头燕尾，波磔分明，适合招牌与匾额",
        "dna": "#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-LUBAN-LI-v1.0",
        "parameters": {
            "font_size": 220,
            "stroke_width": 30,
            "slant": 0.0,
            "ink_pressure": 0.85,
            "tip_style": "silkworm",
            "spacing_x": 1.2,
            "spacing_y": 1.25,
            "randomness": 0.02,
            "background": "洒金宣纸",
            "ink_color": "#1c1c1c",
            "taper_in": 0.12,
            "taper_out": 0.2,
            "horizontal_thin": 0.9,
            "vertical_thick": 1.0,
        },
    },
    "LUBAN-ZHUAN": {
        "name": "鲁班-篆书",
        "code": "LUBAN-ZHUAN",
        "category": "篆书",
        "artist": "鲁班大师",
        "era": "当代",
        "description": "圆润古朴，线条均匀，适合印章与碑刻",
        "dna": "#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-LUBAN-ZHUAN-v1.0",
        "parameters": {
            "font_size": 220,
            "stroke_width": 24,
            "slant": 0.0,
            "ink_pressure": 0.95,
            "tip_style": "round",
            "spacing_x": 1.25,
            "spacing_y": 1.3,
            "randomness": 0.01,
            "background": "绢本浅黄",
            "ink_color": "#252015",
            "taper_in": 0.05,
            "taper_out": 0.05,
            "horizontal_thin": 1.0,
            "vertical_thick": 1.0,
        },
    },
}


def apply_slant(points: list[tuple[float, float]], slant: float) -> list[tuple[float, float]]:
    """对点集应用斜切变换。"""
    return [(x + slant * y, y) for x, y in points]


def add_ink_texture(
    points: list[tuple[float, float]],
    randomness: float,
    seed_text: str = "",
) -> list[tuple[float, float]]:
    """给轮廓加入轻微随机抖动，模拟墨韵与宣纸纤维。"""
    if randomness <= 0:
        return points
    rng = random.Random(seed_text)
    result = []
    for x, y in points:
        dx = rng.uniform(-randomness, randomness) * 2
        dy = rng.uniform(-randomness, randomness) * 2
        result.append((x + dx, y + dy))
    return result


def bbox(points: list[tuple[float, float]]) -> tuple[float, float, float, float]:
    """返回 (min_x, min_y, max_x, max_y)。"""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    if not xs:
        return 0, 0, 0, 0
    return min(xs), min(ys), max(xs), max(ys)


if __name__ == "__main__":
    styles = list_styles()
    print(f"可用风格数: {len(styles)}")
    for s in styles[:5]:
        print(f"  {s['code']}: {s['name']}")
    print("DNA:", DNA)
