# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# #龍芯⚡️20260624010825156-AUTO-DNA-CAA4000F 自动注入·分层治理自愈引擎 · 来源可查
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-EDITOR-v1.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹

"""
LonghunFont 编辑器 v1.0
CNSH 字体 · 关键字搜索 · 字元编辑 · SVG 渲染 · DNA 审计
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# 将 engines 目录加入模块路径
sys.path.insert(0, str(Path(__file__).parent / "engines"))
from cnsh_font_engine_uid9622 import CNSH字元基础引擎_UID9622


class LonghunFontEditor:
    DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-EDITOR-v1.0"

    def __init__(self, glyph_path: str | None = None):
        self.base_dir = Path(__file__).parent
        self.glyph_path = Path(glyph_path) if glyph_path else self.base_dir / "glyphs" / "龍魂字元库_v0001.json"
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)

        self.engine = CNSH字元基础引擎_UID9622()
        if self.glyph_path.exists():
            self.engine.载入_cnsh数据_cnsh龍魂_v1(str(self.glyph_path))
        else:
            print(f"⚠️ 未找到字元库: {self.glyph_path}，使用空库")

    # ═══════════════════════════════════════════════════════════
    # 关键字搜索
    # ═══════════════════════════════════════════════════════════
    def search(self, keyword: str | None = None, unicode_prefix: str | None = None, structure: str | None = None):
        """按关键字、Unicode 前缀或结构搜索字元"""
        results = []
        for char, data in self.engine.字元集_cnsh9622.items():
            matched = False
            if keyword and keyword in char:
                matched = True
            if unicode_prefix and data.get("unicode", "").startswith(unicode_prefix.upper()):
                matched = True
            if structure and data.get("结构") == structure:
                matched = True
            if matched:
                results.append({
                    "字元": char,
                    "unicode": data.get("unicode"),
                    "结构": data.get("结构"),
                    "笔画数": data.get("笔画数"),
                    "笔画数_实际": len([s for s in data.get("笔画路径_cnsh9622", []) if s["类型"] == "移动到"])
                })
        return results

    # ═══════════════════════════════════════════════════════════
    # 渲染
    # ═══════════════════════════════════════════════════════════
    def render_char(self, char: str, filename: str | None = None):
        """渲染单个字元到 SVG"""
        if char not in self.engine.字元集_cnsh9622:
            print(f"❌ 字元库中不存在: {char}")
            return None
        if filename is None:
            filename = f"{char}.svg"
        out_path = self.output_dir / filename
        self.engine.输出SVG_cnsh龍魂_v1(char, str(out_path))
        print(f"✅ 已渲染: {out_path}")
        return str(out_path)

    def render_text(self, text: str, filename: str = "text.svg"):
        """渲染文本字符串（每个字独立 SVG，暂不支持连排）"""
        paths = []
        for i, char in enumerate(text):
            if char in self.engine.字元集_cnsh9622:
                p = self.render_char(char, f"_{i}_{char}.svg")
                paths.append(p)
            else:
                print(f"⚠️ 跳过未定义字元: {char}")
        return paths

    # ═══════════════════════════════════════════════════════════
    # 编辑字元
    # ═══════════════════════════════════════════════════════════
    def list_strokes(self, char: str):
        """列出字元笔画"""
        if char not in self.engine.字元集_cnsh9622:
            print(f"❌ 字元不存在: {char}")
            return
        strokes = self.engine.字元集_cnsh9622[char]["笔画路径_cnsh9622"]
        for idx, stroke in enumerate(strokes):
            print(f"[{idx:02d}] {stroke['类型']}: {stroke}")

    def add_stroke(self, char: str, stroke: dict[str, Any]):
        """为字元添加笔画"""
        if char not in self.engine.字元集_cnsh9622:
            print(f"❌ 字元不存在: {char}")
            return False
        self.engine.字元集_cnsh9622[char]["笔画路径_cnsh9622"].append(stroke)
        print(f"✅ 已为 {char} 添加笔画")
        return True

    def update_stroke(self, char: str, index: int, stroke: dict[str, Any]):
        """更新指定笔画"""
        if char not in self.engine.字元集_cnsh9622:
            print(f"❌ 字元不存在: {char}")
            return False
        strokes = self.engine.字元集_cnsh9622[char]["笔画路径_cnsh9622"]
        if index < 0 or index >= len(strokes):
            print(f"❌ 笔画索引越界: {index}")
            return False
        strokes[index] = stroke
        print(f"✅ 已更新 {char}[{index}]")
        return True

    def delete_stroke(self, char: str, index: int):
        """删除指定笔画"""
        if char not in self.engine.字元集_cnsh9622:
            print(f"❌ 字元不存在: {char}")
            return False
        strokes = self.engine.字元集_cnsh9622[char]["笔画路径_cnsh9622"]
        if index < 0 or index >= len(strokes):
            print(f"❌ 笔画索引越界: {index}")
            return False
        removed = strokes.pop(index)
        print(f"✅ 已删除 {char}[{index}]: {removed['类型']}")
        return True

    # ═══════════════════════════════════════════════════════════
    # 保存与审计
    # ═══════════════════════════════════════════════════════════
    def save(self, path: str | None = None):
        """保存字元库"""
        save_path = Path(path) if path else self.glyph_path
        data = {
            "DNA追溯码": self.DNA,
            "元数据": {
                "名称": "龍魂字元库",
                "版本": datetime.now().strftime("v%Y%m%d-%H%M%S"),
                "创建者": "UID9622",
                "描述": "LonghunFont 编辑后字元库",
                "编码标准": "UTF-8",
                "viewBox": "0 0 600 600"
            },
            "三色审计_cnsh9622": self.engine.审计_cnsh9622,
            "字符集_cnsh9622": self.engine.字元集_cnsh9622
        }
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 字元库已保存: {save_path}")
        return str(save_path)

    def audit(self):
        """执行三色审计"""
        try:
            self.engine.执行三色审计_cnsh龍魂_v1()
            print("✅ 三色审计通过")
            return True
        except RuntimeError as e:
            print(f"❌ 三色审计未通过: {e}")
            return False

    def stats(self):
        """打印统计信息"""
        total = len(self.engine.字元集_cnsh9622)
        print(f"\n📊 LonghunFont 字元统计")
        print(f"   总字元数: {total}")
        print(f"   DNA: {self.DNA}")
        print(f"   字元列表: {', '.join(self.engine.字元集_cnsh9622.keys())}")


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="LonghunFont 编辑器")
    parser.add_argument("--glyphs", "-g", default=None, help="字元库 JSON 路径")
    sub = parser.add_subparsers(dest="command", required=True)

    # search
    p_search = sub.add_parser("search", help="关键字搜索字元")
    p_search.add_argument("--keyword", "-k", help="关键字（字元包含）")
    p_search.add_argument("--unicode", "-u", help="Unicode 前缀，如 U+9F")
    p_search.add_argument("--structure", "-s", help="结构：单一/左右/上下")

    # render
    p_render = sub.add_parser("render", help="渲染字元到 SVG")
    p_render.add_argument("text", help="要渲染的文本或单字")
    p_render.add_argument("--out", "-o", default=None, help="输出文件名")

    # list
    p_list = sub.add_parser("list", help="列出字元笔画")
    p_list.add_argument("char", help="字元")

    # add-stroke
    p_add = sub.add_parser("add-stroke", help="添加笔画")
    p_add.add_argument("char", help="字元")
    p_add.add_argument("type", choices=["移动到", "直线段", "三次曲线"], help="笔画类型")
    p_add.add_argument("coords", help="坐标 JSON，如 '[100,200]' 或 '[[100,200],[300,400],[500,600]]'")

    # update-stroke
    p_upd = sub.add_parser("update-stroke", help="更新笔画")
    p_upd.add_argument("char", help="字元")
    p_upd.add_argument("index", type=int, help="笔画索引")
    p_upd.add_argument("type", choices=["移动到", "直线段", "三次曲线"], help="笔画类型")
    p_upd.add_argument("coords", help="坐标 JSON")

    # delete-stroke
    p_del = sub.add_parser("delete-stroke", help="删除笔画")
    p_del.add_argument("char", help="字元")
    p_del.add_argument("index", type=int, help="笔画索引")

    # save
    p_save = sub.add_parser("save", help="保存字元库")
    p_save.add_argument("--out", "-o", default=None, help="输出路径")

    # audit
    sub.add_parser("audit", help="执行三色审计")

    # stats
    sub.add_parser("stats", help="统计信息")

    args = parser.parse_args()
    editor = LonghunFontEditor(args.glyphs)

    if args.command == "search":
        results = editor.search(args.keyword, args.unicode, args.structure)
        if not results:
            print("未找到匹配字元")
        else:
            for r in results:
                print(r)

    elif args.command == "render":
        if len(args.text) == 1:
            editor.render_char(args.text, args.out)
        else:
            editor.render_text(args.text, args.out or "text.svg")

    elif args.command == "list":
        editor.list_strokes(args.char)

    elif args.command == "add-stroke":
        coords = json.loads(args.coords)
        stroke = {"类型": args.type}
        if args.type == "移动到":
            stroke["坐标"] = coords
        elif args.type == "直线段":
            stroke["终点"] = coords
        elif args.type == "三次曲线":
            stroke["控制点"] = coords
        editor.add_stroke(args.char, stroke)

    elif args.command == "update-stroke":
        coords = json.loads(args.coords)
        stroke = {"类型": args.type}
        if args.type == "移动到":
            stroke["坐标"] = coords
        elif args.type == "直线段":
            stroke["终点"] = coords
        elif args.type == "三次曲线":
            stroke["控制点"] = coords
        editor.update_stroke(args.char, args.index, stroke)

    elif args.command == "delete-stroke":
        editor.delete_stroke(args.char, args.index)

    elif args.command == "save":
        editor.save(args.out)

    elif args.command == "audit":
        editor.audit()

    elif args.command == "stats":
        editor.stats()


if __name__ == "__main__":
    main()
