#!/usr/bin/env python3
"""
龍魂字体管理引擎 v2.0 · LonghunFont Engine
=============================================
底座组件 · L1_内核层/fonts 字体子系统
DNA: #龍芯⚡️丙午·辛未·乙酉-LONGHUN-FONT-ENGINE-v2.0

升级点 (v1.0 → v2.0):
  1. fontTools 真实元数据解析 (PostScript名/家族/样式/字形数)
  2. 自动扫描发现所有字体变体 (不再硬编码变体列表)
  3. JSON注册表持久化导出
  4. 结构化查询接口 (按名称/样式/格式)
  5. 字体有效性验证 (损坏检测)
"""

import hashlib
import json
import os
import platform
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fontTools.ttLib import TTFont, TTLibError

# ═══════════════════════════════════════════
# DNA 追溯
# ═══════════════════════════════════════════
__DNA__ = "#龍芯⚡️丙午·辛未·乙酉-LONGHUN-FONT-ENGINE-v2.0"
__VERSION__ = "2.0.0"
__AUTHOR__ = "UID9622"


def _find_project_root() -> Path:
    """向上查找项目根目录 (含 L1_内核层)"""
    p = Path(__file__).resolve()
    for _ in range(10):
        if (p / "L1_内核层" / "fonts").exists():
            return p
        p = p.parent
    # 回退
    return Path(__file__).resolve().parent.parent.parent.parent.parent


class LonghunFontEngine:
    """
    龍魂字体管理引擎
    ────────────────
    扫描 L1_内核层/fonts/ 下所有 .otf/.ttf/.woff2 字体文件，
    使用 fontTools 解析真实元数据，构建内存中的字体注册表。

    职责:
      - 字体发现与注册
      - 元数据提取 (PostScript名/家族/样式/字形数)
      - 完整性校验 (SHA256 + 文件损坏检测)
      - 结构化查询 (按名/格式/样式)
      - JSON注册表导出
    """

    def __init__(self, font_dir: Optional[str] = None):
        if font_dir:
            self.font_dir = Path(font_dir)
        else:
            self.font_dir = _find_project_root() / "L1_内核层" / "fonts"

        # 注册表: key=文件名(无后缀)唯一键, value=字体元数据dict
        self.font_registry: Dict[str, dict] = {}

        # PostScript名 → 文件键 映射 (用于按PS名查询)
        self._ps_index: Dict[str, list] = {}

        # 按格式索引: "otf" / "ttf" / "woff2" → [file_key, ...]
        self._format_index: Dict[str, list] = {}

        # 按家族索引: family_name → [file_key, ...]
        self._family_index: Dict[str, list] = {}

        # 自动扫描加载
        self._load_all_fonts()

    # ═══════════════════════════════════════
    # 扫描与注册
    # ═══════════════════════════════════════

    def _load_all_fonts(self):
        """扫描目录，自动发现所有支持的字体文件"""
        if not self.font_dir.exists():
            return

        supported = list(self.font_dir.glob("*.otf")) + \
                     list(self.font_dir.glob("*.ttf")) + \
                     list(self.font_dir.glob("*.woff2"))

        for font_file in supported:
            self._register_font(font_file)

        if self.font_registry:
            print(f"[字体引擎] 已注册 {len(self.font_registry)} 个龙魂字体变体")

    def _register_font(self, font_path: Path) -> Optional[dict]:
        """使用 fontTools 解析单个字体并注册"""
        suffix = font_path.suffix.lower().lstrip(".")
        fmt = suffix  # otf / ttf / woff2
        file_key = font_path.name  # 完整文件名 = 唯一键 (.otf/.ttf/.woff2 不同)

        # woff2 不支持 fontTools 直接解析，用基础元数据
        if fmt == "woff2":
            return self._register_woff2(font_path)

        # OTF / TTF 用 fontTools
        try:
            font = TTFont(str(font_path))
            name_table = font["name"]

            # 提取关键 nameID
            family_name = None
            subfamily_name = None
            postscript_name = None
            version_str = None
            copyright_str = None

            for record in name_table.names:
                try:
                    text = record.toUnicode()
                except Exception:
                    continue
                if record.nameID == 1:
                    family_name = text
                elif record.nameID == 2:
                    subfamily_name = text
                elif record.nameID == 6:
                    postscript_name = text
                elif record.nameID == 5:
                    version_str = text
                elif record.nameID == 0:
                    copyright_str = text

            # 回退: 没有 PostScript 名用文件名
            if not postscript_name:
                postscript_name = font_path.stem

            # 字形数
            glyph_count = len(font.getGlyphOrder())

            # 文件属性
            file_size = font_path.stat().st_size
            sha256 = _sha256(font_path)

            entry = {
                "postscript_name": postscript_name,
                "family_name": family_name or "Longhun",
                "style_name": subfamily_name or "Regular",
                "version": version_str or "",
                "copyright": copyright_str or "",
                "file_path": str(font_path.resolve()),
                "file_name": font_path.name,
                "file_key": file_key,
                "format": fmt,
                "glyph_count": glyph_count,
                "file_size_kb": round(file_size / 1024, 1),
                "sha256": sha256,
                "is_valid": True,
                "registered_at": datetime.now(timezone.utc).isoformat(),
            }

            self.font_registry[file_key] = entry

            # 更新索引
            self._format_index.setdefault(fmt, []).append(file_key)
            fam = family_name or "Longhun"
            self._family_index.setdefault(fam, []).append(file_key)
            self._ps_index.setdefault(postscript_name.lower(), []).append(file_key)

            font.close()
            return entry

        except (TTLibError, Exception) as e:
            # 损坏或不支持的字体
            file_key = font_path.name
            file_size = font_path.stat().st_size if font_path.exists() else 0
            entry = {
                "postscript_name": font_path.stem,
                "family_name": "Longhun (damaged)",
                "style_name": "Regular",
                "version": "",
                "copyright": "",
                "file_path": str(font_path.resolve()),
                "file_name": font_path.name,
                "file_key": file_key,
                "format": fmt,
                "glyph_count": 0,
                "file_size_kb": round(file_size / 1024, 1),
                "sha256": _sha256(font_path) if font_path.exists() else "",
                "is_valid": False,
                "error": str(e),
                "registered_at": datetime.now(timezone.utc).isoformat(),
            }
            self.font_registry[file_key] = entry
            return entry

    def _register_woff2(self, font_path: Path) -> dict:
        """woff2 无法用 fontTools 解析字体名，使用基础信息"""
        file_key = font_path.name
        file_size = font_path.stat().st_size
        sha256 = _sha256(font_path)

        entry = {
            "postscript_name": file_key,
            "family_name": "Longhun",
            "style_name": "Regular",
            "version": "",
            "copyright": "",
            "file_path": str(font_path.resolve()),
            "file_name": font_path.name,
            "file_key": file_key,
            "format": "woff2",
            "glyph_count": -1,  # woff2 不解析
            "file_size_kb": round(file_size / 1024, 1),
            "sha256": sha256,
            "is_valid": True,
            "registered_at": datetime.now(timezone.utc).isoformat(),
        }
        self.font_registry[file_key] = entry
        self._format_index.setdefault("woff2", []).append(file_key)
        self._family_index.setdefault("Longhun", []).append(file_key)
        self._ps_index.setdefault(file_key.lower(), []).append(file_key)
        return entry

    def rescan(self):
        """重新扫描字体目录 (热加载)"""
        self.font_registry.clear()
        self._ps_index.clear()
        self._format_index.clear()
        self._family_index.clear()
        self._load_all_fonts()

    # ═══════════════════════════════════════
    # 查询接口
    # ═══════════════════════════════════════

    def get_all_fonts(self) -> List[dict]:
        """获取所有已注册字体"""
        return list(self.font_registry.values())

    def get_font_by_name(self, name: str) -> Optional[dict]:
        """按名称查找 (支持 文件名 / PostScript名 / 模糊匹配)"""
        # 精确匹配 file_key (完整文件名)
        if name in self.font_registry:
            return self.font_registry[name]
        # 匹配文件名(不含后缀)
        for key, val in self.font_registry.items():
            if val["file_name"] == name:
                return val
        # 匹配 PostScript 名
        name_lower = name.lower()
        if name_lower in self._ps_index:
            keys = self._ps_index[name_lower]
            if keys:
                return self.font_registry[keys[0]]
        # 模糊匹配 file_key / postscript_name
        for key, val in self.font_registry.items():
            if name_lower in key.lower() or name_lower in val["postscript_name"].lower():
                return val
        return None

    def get_font_by_format(self, fmt: str) -> List[dict]:
        """按格式筛选 (otf / ttf / woff2)"""
        names = self._format_index.get(fmt.lower(), [])
        return [self.font_registry[n] for n in names if n in self.font_registry]

    def get_font_by_family(self, family: str) -> List[dict]:
        """按字体家族筛选"""
        names = self._family_index.get(family, [])
        if not names:
            # 模糊
            family_lower = family.lower()
            for fam, ns in self._family_index.items():
                if family_lower in fam.lower():
                    names.extend(ns)
        return [self.font_registry[n] for n in names if n in self.font_registry]

    def get_font_by_style(self, style: str) -> List[dict]:
        """按样式筛选 (Regular/Bold/Italic...)"""
        style_lower = style.lower()
        return [v for v in self.font_registry.values()
                if style_lower in v["style_name"].lower()]

    def get_font_file_path(self, name: str) -> Optional[str]:
        """直接获取字体文件绝对路径 (供上层调用)"""
        font = self.get_font_by_name(name)
        return font["file_path"] if font else None

    def get_valid_fonts(self) -> List[dict]:
        """获取所有有效的字体 (过滤损坏的)"""
        return [v for v in self.font_registry.values() if v.get("is_valid", False)]

    def get_summary(self) -> dict:
        """获取引擎摘要"""
        return {
            "font_dir": str(self.font_dir.resolve()),
            "total": len(self.font_registry),
            "valid": len(self.get_valid_fonts()),
            "damaged": len(self.font_registry) - len(self.get_valid_fonts()),
            "formats": {k: len(v) for k, v in self._format_index.items()},
            "families": list(self._family_index.keys()),
            "engine_version": __VERSION__,
            "dna": __DNA__,
        }

    # ═══════════════════════════════════════
    # 持久化
    # ═══════════════════════════════════════

    def export_registry_json(self, output_path: Optional[str] = None) -> str:
        """导出注册表 JSON (供调试/审计)"""
        if not output_path:
            output_path = str(self.font_dir / "font_registry.json")
        data = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "dna": __DNA__,
            "version": __VERSION__,
            "font_dir": str(self.font_dir.resolve()),
            "summary": self.get_summary(),
            "fonts": self.font_registry,
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[字体引擎] 注册表已导出: {output_path}")
        return output_path

    def export_registry_dict(self) -> dict:
        """导出注册表为 dict (供 MCP 服务)"""
        return self.font_registry


# ═══════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════

def _sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ═══════════════════════════════════════
# 独立运行
# ═══════════════════════════════════════

if __name__ == "__main__":
    engine = LonghunFontEngine()

    print("\n=== 引擎摘要 ===")
    print(json.dumps(engine.get_summary(), indent=2, ensure_ascii=False))

    print("\n=== 所有字体 ===")
    for f in engine.get_all_fonts():
        status = "✅" if f.get("is_valid") else "❌"
        glyphs = f"{f.get('glyph_count', '?'):>5}"
        print(f"  {status} {f['postscript_name']:<35s} | "
              f"{f.get('family_name', ''):<12s} | "
              f"{f['format']:<5s} | "
              f"{f['file_size_kb']:>7} KB | "
              f"字形:{glyphs}")

    print("\n=== 按格式查询 ===")
    for fmt in ["otf", "woff2"]:
        fonts = engine.get_font_by_format(fmt)
        print(f"  {fmt}: {len(fonts)} 个 → {[f['file_name'] for f in fonts]}")

    # 导出注册表
    engine.export_registry_json()
