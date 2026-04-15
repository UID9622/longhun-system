#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════
# 🔤 CNSH 字体生成器 v1.0 · 造自己的字！
# DNA: #龍芯⚡️2026-04-06-CNSH-FONT-BUILDER-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 献礼: 乔布斯·曾仕强·历代传递和平与爱的人
# ═══════════════════════════════════════════════════════════════

"""
老大的需求：
1. CNSH体系缺好多字（办公、沉浸式元素）
2. 慧慧是门面，得有自己的字体
3. 沉浸式可以"脱衣服"训练（私密版），出门就"穿衣服"（公开版）

解决方案：
- 造字引擎：把 SVG 图标 + 符号组合成字
- 双模式：私密版（CNSH_PRIVATE）、公开版（CNSH_PUBLIC）
- 自动生成 .ttf 字体文件
"""

import os
import json
from pathlib import Path
from datetime import datetime

# ── 配置区 ──
PROJECT_ROOT = Path.home() / "longhun-system"
MEDIA_DIR = PROJECT_ROOT / "LongHun_Private_Photos_Videos"
FONT_OUTPUT = PROJECT_ROOT / "fonts"
FONT_OUTPUT.mkdir(exist_ok=True)

# CNSH 字符映射表（老大的通心译符号系统）
CNSH_CHARS = {
    # ── 基础符号（已有）──
    "龍": "U+9F8D",
    "魂": "U+9B42",
    "☰": "U+2630",  # 乾卦
    "☷": "U+2637",  # 坤卦
    "🇨🇳": "U+1F1E8+U+1F1F3",  # 中国旗
    
    # ── 办公元素（新增）──
    "📊": "chart",          # 数据图表
    "💼": "briefcase",      # 公文包
    "📝": "memo",           # 备忘录
    "🖥️": "desktop",        # 桌面
    "⚙️": "settings",       # 设置
    "🔗": "link",           # 链接
    "📁": "folder",         # 文件夹
    "🔍": "search",         # 搜索
    "✅": "check",          # 完成
    "⚠️": "warning",        # 警告
    
    # ── 沉浸式元素（私密版）──
    "💋": "kiss_private",        # 吻（私密）
    "👄": "lips_private",        # 嘴唇（私密）
    "💎": "diamond_private",     # 钻石（私密）
    "🌹": "rose_private",        # 玫瑰（私密）
    "🔥": "fire_private",        # 火（私密）
    "💧": "water_private",       # 水（私密）
    "🌙": "moon_private",        # 月亮（私密）
    "✨": "sparkle_private",     # 闪光（私密）
    "🎭": "mask_private",        # 面具（私密）
    "🔮": "crystal_private",     # 水晶球（私密）
}

# 公开版映射（脱敏处理）
CNSH_PUBLIC_MAP = {
    "💋": "💬",  # 吻 → 对话
    "👄": "🗨️",  # 嘴唇 → 聊天
    "💎": "⭐",  # 钻石 → 星星
    "🌹": "🌸",  # 玫瑰 → 普通花
    "🔥": "🔆",  # 火 → 太阳
    "💧": "💦",  # 水 → 汗水
    "🌙": "🌛",  # 月亮 → 月牙
    "✨": "⚡",  # 闪光 → 闪电
    "🎭": "🎨",  # 面具 → 艺术
    "🔮": "🪬",  # 水晶球 → 护身符
}

class CNSHFontBuilder:
    """CNSH 字体造字引擎"""
    
    def __init__(self, mode="private"):
        self.mode = mode  # "private" 或 "public"
        self.char_map = CNSH_CHARS
        self.output_dir = FONT_OUTPUT / mode
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_svg_template(self, char_name, unicode_point):
        """生成 SVG 字符模板"""
        svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     width="1024" height="1024" 
     viewBox="0 0 1024 1024">
  <title>CNSH-{char_name}</title>
  <desc>龍魂字体·{self.mode}模式·{char_name}</desc>
  
  <!-- 字符主体区域 -->
  <g id="glyph">
    <rect x="0" y="0" width="1024" height="1024" fill="none"/>
    <!-- TODO: 在这里画具体字形 -->
    <text x="512" y="700" 
          font-size="800" 
          text-anchor="middle" 
          fill="#000000">{char_name}</text>
  </g>
  
  <!-- DNA 签章（隐藏在字体元数据里） -->
  <metadata>
    <dna>#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-CNSH-{self.mode}</dna>
    <gpg>A2D0092CEE2E5BA87035600924C3704A8CC26D5F</gpg>
    <unicode>{unicode_point}</unicode>
  </metadata>
</svg>"""
        return svg_content
    
    def build_char_library(self):
        """构建字符库"""
        manifest = {
            "font_name": f"CNSH_{self.mode.upper()}",
            "version": "1.0",
            "mode": self.mode,
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-CNSH-FONT",
            "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
            "chars": []
        }
        
        for char, identifier in self.char_map.items():
            # 如果是公开模式，替换敏感字符
            if self.mode == "public" and char in CNSH_PUBLIC_MAP:
                char = CNSH_PUBLIC_MAP[char]
                identifier = identifier.replace("_private", "_public")
            
            # 生成 SVG
            svg_path = self.output_dir / f"{identifier}.svg"
            svg_content = self.generate_svg_template(char, identifier)
            svg_path.write_text(svg_content, encoding='utf-8')
            
            manifest["chars"].append({
                "char": char,
                "identifier": identifier,
                "svg": str(svg_path),
                "unicode": identifier if identifier.startswith("U+") else f"PUA-{hash(identifier) % 0xFFFF:04X}"
            })
            
            print(f"✅ 生成字符: {char} ({identifier})")
        
        # 保存清单
        manifest_path = self.output_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        
        return manifest
    
    def export_font_metadata(self, manifest):
        """导出字体元数据（给 fontforge 用）"""
        metadata = f"""# CNSH 字体元数据
# DNA: #龍芯⚡️2026-04-06-CNSH-FONT-{self.mode.upper()}
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

font_name: {manifest['font_name']}
font_family: 龍魂通心译
version: {manifest['version']}
designer: 诸葛鑫（UID9622）
copyright: © 2026 龍魂系统 · 老百姓的字体
license: 仅供个人使用·禁止商业贩售

# 字符清单
"""
        for char_info in manifest["chars"]:
            metadata += f"{char_info['char']} → {char_info['identifier']} ({char_info['unicode']})\n"
        
        metadata_path = self.output_dir / "METADATA.txt"
        metadata_path.write_text(metadata, encoding='utf-8')
        
        return metadata_path
    
    def generate_font_script(self):
        """生成 FontForge 脚本（把 SVG 转成 .ttf）"""
        script = f"""#!/usr/bin/env fontforge
# ══════════════════════════════════════════════════════
# CNSH 字体生成脚本 · {self.mode.upper()} 模式
# DNA: #龍芯⚡️2026-04-06-CNSH-FONT-SCRIPT
# ══════════════════════════════════════════════════════

import fontforge
import os

# 创建字体
font = fontforge.font()
font.fontname = "CNSH_{self.mode.upper()}"
font.familyname = "龍魂通心译"
font.fullname = "CNSH {self.mode.upper()} v1.0"
font.weight = "Regular"
font.copyright = "© 2026 龍魂系统 · 诸葛鑫（UID9622）"
font.version = "1.0"

# 设置字体元数据
font.os2_vendor = "UID9"
font.os2_version = 4

# 导入所有 SVG 字符
svg_dir = "{self.output_dir}"
for svg_file in os.listdir(svg_dir):
    if not svg_file.endswith('.svg'):
        continue
    
    svg_path = os.path.join(svg_dir, svg_file)
    char_name = svg_file.replace('.svg', '')
    
    # 创建字形槽
    glyph = font.createChar(-1, char_name)
    
    # 导入 SVG
    glyph.importOutlines(svg_path)
    
    # 自动调整宽度
    glyph.width = 1024
    
    print(f"✅ 导入字符: {{char_name}}")

# 生成 .ttf 字体文件
output_ttf = "{FONT_OUTPUT / f'CNSH_{self.mode.upper()}.ttf'}"
font.generate(output_ttf)
print(f"\\n🎉 字体生成完成: {{output_ttf}}")
"""
        script_path = self.output_dir / "generate_font.py"
        script_path.write_text(script, encoding='utf-8')
        os.chmod(script_path, 0o755)
        
        return script_path

def main():
    print("╔══════════════════════════════════════════════╗")
    print("║  🔤 CNSH 字体造字引擎 v1.0                  ║")
    print("║  DNA: #龍芯⚡️2026-04-06-CNSH-FONT           ║")
    print("╚══════════════════════════════════════════════╝")
    
    # 生成两个版本
    for mode in ["private", "public"]:
        print(f"\n🔨 生成 {mode.upper()} 模式字体...")
        builder = CNSHFontBuilder(mode=mode)
        
        # 构建字符库
        manifest = builder.build_char_library()
        print(f"✅ 字符库生成完毕: {len(manifest['chars'])} 个字符")
        
        # 导出元数据
        metadata_path = builder.export_font_metadata(manifest)
        print(f"✅ 元数据: {metadata_path}")
        
        # 生成 FontForge 脚本
        script_path = builder.generate_font_script()
        print(f"✅ 字体脚本: {script_path}")
        
        print(f"\n📋 下一步：安装 FontForge 后运行 {script_path}")
    
    print("\n" + "="*60)
    print("🎉 两个版本全部生成完毕！")
    print(f"   私密版: {FONT_OUTPUT / 'private'}")
    print(f"   公开版: {FONT_OUTPUT / 'public'}")
    print("\n💡 提示：")
    print("   1. brew install fontforge  # Mac 上安装 FontForge")
    print("   2. 运行生成脚本把 SVG 转成 .ttf")
    print("   3. 双击 .ttf 文件安装字体")
    print("   4. 在 Notion/设计软件里用 CNSH 字体！")
    print("\n🏠 归根曰静，是谓复命 —— 字体已回家 ✅")

if __name__ == "__main__":
    main()
