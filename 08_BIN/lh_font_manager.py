#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·乙酉·壬午·䷨损-LONGHUN-FONT-MANAGER-v2.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂字体管理引擎 CLI v2.0 · LonghunFont Manager
=================================================
底座组件 · L1_内核层/fonts 字体子系统
DNA: #龍芯⚡️丙午·辛未·乙酉·壬午·䷨损-LONGHUN-FONT-MANAGER-v2.0

v2.0 升级:
  - 集成 LonghunFontEngine (fontTools 真实元数据解析)
  - 自动发现字体变体 (不再硬编码)
  - 新增 registry 命令 (导出JSON注册表)
  - 新增 mcp 命令 (启动MCP交互模式)
  - verify 使用引擎校验

操作命令:
  install     — 安装字体到操作系统
  uninstall   — 从操作系统卸载字体
  verify      — 校验字体完整性
  list        — 列出底座+系统所有字体
  css         — 生成 @font-face CSS
  info        — 查看字体元信息
  registry    — 导出 JSON 注册表
  mcp         — 启动 MCP 交互模式
  serve       — 启动 HTTP 字体服务
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# ═══════════════════════════════════════════
# DNA 追溯
# ═══════════════════════════════════════════
__DNA__ = "#龍芯⚡️丙午·辛未·乙酉·壬午·䷨损-LONGHUN-FONT-MANAGER-v2.0"
__VERSION__ = "2.0.0"
__AUTHOR__ = "UID9622"

# ═══════════════════════════════════════════
# 底座路径
# ═══════════════════════════════════════════
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FONT_BASE = PROJECT_ROOT / "L1_内核层" / "fonts"

SYSTEM = platform.system()

# 引擎实例 (懒加载)
_engine = None


def _get_engine():
    """获取字体引擎实例"""
    global _engine
    if _engine is None:
        sys.path.insert(0, str(PROJECT_ROOT / "L5_服务层" / "services" / "shared"))
        from font_manager.engine import LonghunFontEngine
        _engine = LonghunFontEngine(font_dir=str(FONT_BASE))
    return _engine


# ═══════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════

def _get_font_dir() -> Path:
    if SYSTEM == "Darwin":
        return Path.home() / "Library" / "Fonts"
    elif SYSTEM == "Windows":
        return Path(os.environ.get("WINDIR", "C:\\Windows")) / "Fonts"
    else:
        return Path.home() / ".local" / "share" / "fonts"


def _refresh_font_cache():
    if SYSTEM == "Darwin":
        subprocess.run(["atsutil", "databases", "-remove"], capture_output=True)
        print("[缓存] 已刷新 macOS 字体缓存")


def _print_dna():
    print(f"\n🧬 {__DNA__}")


# ═══════════════════════════════════════
# 命令: install
# ═══════════════════════════════════════

def cmd_install(variant: str = "all", force: bool = False):
    """安装字体到操作系统"""
    engine = _get_engine()
    all_fonts = engine.get_all_fonts()

    font_dir = _get_font_dir()
    font_dir.mkdir(parents=True, exist_ok=True)

    installed = []
    skipped = []

    for entry in all_fonts:
        filename = entry["file_name"]
        # 如果指定了变体, 按格式/文件名筛选
        if variant != "all":
            if variant == "color" and "Wuwu" not in filename:
                continue
            if variant == "web" and "woff2" not in entry["format"]:
                continue
            if variant == "full" and "Full" not in filename:
                continue
            if variant == "standard" and ("Full" in filename or "Wuwu" in filename):
                continue

        src = Path(entry["file_path"])
        dst = font_dir / filename

        if not src.exists():
            print(f"[缺失] {filename}")
            continue

        if dst.exists() and not force:
            skipped.append(filename)
            continue

        shutil.copy2(src, dst)
        installed.append(filename)

    _refresh_font_cache()

    print(f"\n✅ 安装完成: {len(installed)} 个")
    for f in installed:
        print(f"   + {f}")
    if skipped:
        print(f"⏭ 已存在跳过: {len(skipped)} 个")
    _print_dna()


# ═══════════════════════════════════════
# 命令: uninstall
# ═══════════════════════════════════════

def cmd_uninstall(variant: str = "all"):
    font_dir = _get_font_dir()
    removed = []

    for f in font_dir.glob("LonghunFont*"):
        if variant != "all":
            if variant == "color" and "Wuwu" not in f.name:
                continue
            if variant == "web" and "woff2" not in f.suffix:
                continue
            if variant == "full" and "Full" not in f.name:
                continue
            if variant == "standard" and ("Full" in f.name or "Wuwu" in f.name):
                continue
        f.unlink()
        removed.append(f.name)

    _refresh_font_cache()
    print(f"✅ 卸载完成: {len(removed)} 个")
    for f in removed:
        print(f"   - {f}")
    _print_dna()


# ═══════════════════════════════════════
# 命令: verify
# ═══════════════════════════════════════

def cmd_verify():
    engine = _get_engine()
    mcp_verify = engine.get_summary()

    print("🔍 龍魂字体底座完整性校验\n")

    all_fonts = engine.get_all_fonts()
    all_ok = True

    for entry in all_fonts:
        fp = Path(entry["file_path"])
        glyphs = entry.get("glyph_count", "?")
        sha = entry.get("sha256", "")[:16]
        status = "✅" if entry.get("is_valid") else "❌"
        if not entry.get("is_valid"):
            all_ok = False

        print(f"{status} {entry['file_name']:<38s} {entry['file_size_kb']:>7} KB  "
              f"字形:{glyphs:>5}  SHA256:{sha}...")

    sys_fonts = list(_get_font_dir().glob("LonghunFont*"))
    print(f"\n📂 系统已安装: {len(sys_fonts)} 个")
    for f in sys_fonts:
        print(f"   → {f.name} ({f.stat().st_size / 1024:.1f} KB)")

    if all_ok:
        print("\n✅ 底座字体完整")
    else:
        print("\n⚠️ 存在损坏的字体, 请检查")

    _print_dna()


# ═══════════════════════════════════════
# 命令: list[Any]
# ═══════════════════════════════════════

def cmd_list():
    engine = _get_engine()
    all_fonts = engine.get_all_fonts()

    print("📋 龍魂字体清单 (fontTools 元数据)\n")

    print("━ 底座字体 (L1_内核层/fonts/):")
    for entry in all_fonts:
        status = "✅" if entry.get("is_valid") else "❌"
        fmt = entry["format"]
        family = entry.get("family_name", "?")
        glyphs = entry.get("glyph_count", "?")
        sha = entry.get("sha256", "")[:12]
        print(f"  {status} {entry['file_name']:<42s} {entry['file_size_kb']:>7} KB")
        print(f"     PostScript: {entry['postscript_name']}  家族: {family}  "
              f"格式: {fmt.upper()}  字形: {glyphs}  SHA256:{sha}")

    sys_fonts = list(_get_font_dir().glob("LonghunFont*"))
    print(f"\n━ 系统已安装: {len(sys_fonts)} 个")
    for f in sys_fonts:
        print(f"  ✅ {f.name} ({f.stat().st_size / 1024:.1f} KB)")


# ═══════════════════════════════════════
# 命令: css
# ═══════════════════════════════════════

def cmd_css(base_url: str = "/fonts/"):
    engine = _get_engine()
    all_fonts = engine.get_all_fonts()

    css_lines = [
        "/* 龍魂字体 · LonghunFont @font-face */",
        "/* DNA: #龍芯⚡️丙午·辛未·乙酉·壬午·䷨损-LONGHUN-FONT-CSS-v2.0 */",
        "/* 生成工具: lh_font_manager.py css (engine v2.0) */",
        "",
    ]

    # 去重: 同一 PostScript 名只保留最优变体 (OTF优先于woff2, 标准优先于Full)
    seen_ps: set[str] = set()
    for entry in all_fonts:
        ps = entry["postscript_name"]
        fname = entry["file_name"]
        fmt = entry["format"]

        if ps in seen_ps:
            continue
        seen_ps.add(ps)

        if fmt == "woff2":
            format_str = "woff2"
        elif fmt == "otf":
            format_str = "opentype"
        elif fmt == "ttf":
            format_str = "truetype"
        else:
            continue

        # 智能命名 font-family
        if "Wuwu" in fname:
            font_family = "'LonghunFont Wuwu'"
        elif "Full" in fname:
            font_family = "'LonghunFont Full'"
        else:
            font_family = "'LonghunFont'"

        css_lines.extend([
            f"/* {fname} ({ps}) */",
            "@font-face {",
            f"  font-family: {font_family};",
            f"  src: url('{base_url}{fname}') format('{format_str}');",
            "  font-weight: 400;",
            "  font-style: normal;",
            "  font-display: swap;",
            "}",
            "",
        ])

    css_lines.extend([
        "/* === 辅助类 === */",
        ".longhun-font { font-family: 'LonghunFont', sans-serif; }",
        ".longhun-full { font-family: 'LonghunFont Full', 'LonghunFont', sans-serif; }",
        ".longhun-wuwu { font-family: 'LonghunFont Wuwu', 'LonghunFont', sans-serif; }",
        "",
    ])

    output = "\n".join(css_lines)
    print(output)

    css_path = FONT_BASE / "LonghunFont.css"
    css_path.write_text(output)
    print(f"/* CSS 已写入: {css_path} */")


# ═══════════════════════════════════════
# 命令: info
# ═══════════════════════════════════════

def cmd_info():
    engine = _get_engine()

    print("🐉 LonghunFont · 龍魂中文字体\n")
    print("═" * 50)
    print(f"版本:      v0019-龍纹书法版")
    print(f"总字符:    28957")
    print(f"汉字:      28096 (CJK全BMP)")
    print(f"拉丁/符号: 124")
    print(f"易经八卦:  75")
    print(f"甲骨文:    150")
    print(f"文化图标:  29")
    print(f"二十四节气: 24")
    print(f"十二生肖:  12")
    print(f"天干地支:  22")
    print(f"二十八宿:  28")
    print(f"传统节日:  15")
    print(f"苏州码子:  10")
    print(f"传统纹样:  15")
    print(f"文化主权图标: 20")
    print(f"实用符号:  151")
    print(f"国际符号:  188")
    print(f"龍纹水印:  U+E200 嵌入每个字形")
    print(f"许可证:    SIL Open Font License 1.1")
    print(f"主仓:      https://gitee.com/uid9622_admin/LonghunFont")
    print(f"镜像:      https://github.com/UID9622/LonghunFont")
    print("═" * 50)

    # 引擎元数据
    summary = engine.get_summary()
    print(f"\n[引擎] 版本: {summary['engine_version']}  底座: {summary['font_dir']}")
    print(f"       字体: {summary['total']} 个  "
          f"有效: {summary['valid']}  格式: {summary['formats']}")

    all_fonts = engine.get_all_fonts()
    print(f"\n[底座文件]")
    for entry in all_fonts:
        status = "✅" if entry.get("is_valid") else "❌"
        sha = entry.get("sha256", "N/A")[:20]
        print(f"  {status} [{entry['format']:>5s}] {entry['postscript_name']:<35s}  "
              f"{entry['file_size_kb']:>7} KB  SHA256:{sha}...")

    _print_dna()


# ═══════════════════════════════════════
# 命令: registry
# ═══════════════════════════════════════

def cmd_registry(output_path: Optional[str] = None):
    engine = _get_engine()
    path = engine.export_registry_json(output_path)

    summary = engine.get_summary()
    print(f"\n注册表: {path}")
    print(f"字体数: {summary['total']}  有效: {summary['valid']}")
    _print_dna()


# ═══════════════════════════════════════
# 命令: mcp
# ═══════════════════════════════════════

def cmd_mcp():
    sys.path.insert(0, str(PROJECT_ROOT / "L5_服务层" / "services" / "shared"))
    from font_manager.mcp_server import LonghunFontMCPServer
    server = LonghunFontMCPServer()
    server.run_stdio()


# ═══════════════════════════════════════
# 命令: serve
# ═══════════════════════════════════════

def cmd_serve(port: int = 8767):
    import http.server
    import socketserver

    os.chdir(str(FONT_BASE))

    class FontHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "public, max-age=86400")
            super().end_headers()

    with socketserver.TCPServer(("", port), FontHandler) as httpd:
        print(f"🐉 龍魂字体服务")
        print(f"   http://localhost:{port}/")
        print(f"   按 Ctrl+C 停止")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务已停止")


# ═══════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂字体管理引擎 CLI · LonghunFont Manager v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  python3 bin/lh_font_manager.py install              # 安装全部字体
  python3 bin/lh_font_manager.py install --variant full   # 仅安装完整版
  python3 bin/lh_font_manager.py install --force      # 强制覆盖
  python3 bin/lh_font_manager.py uninstall            # 卸载全部
  python3 bin/lh_font_manager.py verify               # 校验完整性
  python3 bin/lh_font_manager.py list                 # 列出所有
  python3 bin/lh_font_manager.py css                  # 生成 CSS
  python3 bin/lh_font_manager.py info                 # 元信息
  python3 bin/lh_font_manager.py registry             # 导出注册表 JSON
  python3 bin/lh_font_manager.py mcp                  # MCP stdio 模式
  python3 bin/lh_font_manager.py serve --port 8767    # HTTP 字体服务

DNA: {__DNA__}
        """,
    )

    sub = parser.add_subparsers(dest="command", help="可用命令")

    # install
    p = sub.add_parser("install", help="安装字体到操作系统")
    p.add_argument("--variant", default="all",
                   choices=["all", "full", "standard", "color", "web"])
    p.add_argument("--force", action="store_true", help="强制覆盖")

    # uninstall
    p = sub.add_parser("uninstall", help="卸载字体")
    p.add_argument("--variant", default="all",
                   choices=["all", "full", "standard", "color", "web"])

    # verify
    sub.add_parser("verify", help="校验字体完整性")

    # list
    sub.add_parser("list", help="列出所有字体")

    # css
    p = sub.add_parser("css", help="生成 @font-face CSS")
    p.add_argument("--base-url", default="/fonts/", help="字体 URL 基路径")

    # info
    sub.add_parser("info", help="字体元信息")

    # registry
    p = sub.add_parser("registry", help="导出 JSON 注册表")
    p.add_argument("--output", default=None, help="输出路径")

    # mcp
    sub.add_parser("mcp", help="MCP stdio 交互模式")

    # serve
    p = sub.add_parser("serve", help="HTTP 字体服务")
    p.add_argument("--port", type=int, default=8767)

    args = parser.parse_args()

    commands = {
        "install": lambda: cmd_install(args.variant, args.force),
        "uninstall": lambda: cmd_uninstall(args.variant),
        "verify": cmd_verify,
        "list": cmd_list,
        "css": lambda: cmd_css(args.base_url),
        "info": cmd_info,
        "registry": lambda: cmd_registry(args.output),
        "mcp": cmd_mcp,
        "serve": lambda: cmd_serve(args.port),
    }

    if args.command in commands:
        commands[args.command]()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
