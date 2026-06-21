#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂主題工廠 v1.0
Longhun Theme Factory

DNA:#龍芯⚡️2026-06-07-THEME-FACTORY-v1.0
"""

import json
from typing import Dict, List
from dataclasses import dataclass, asdict

@dataclass
class ThemeColor:
    """主題顏色"""
    primary: str
    secondary: str
    accent: str
    success: str
    warning: str
    error: str
    info: str
    background: str
    surface: str
    text: str
    text_secondary: str

class Theme:
    """主題類"""
    
    def __init__(self, name: str, colors: ThemeColor, description: str = ""):
        self.name = name
        self.colors = colors
        self.description = description
    
    def generate_css_variables(self) -> str:
        """生成 CSS 變數"""
        css = ":root {\n"
        for key, value in asdict(self.colors).items():
            css_key = key.replace('_', '-')
            css += f"  --color-{css_key}: {value};\n"
        css += "}\n"
        return css
    
    def generate_css_classes(self) -> str:
        """生成 CSS 類"""
        return f"""
.theme-{self.name.lower()} {{
  --primary: {self.colors.primary};
  --secondary: {self.colors.secondary};
  --accent: {self.colors.accent};
  --success: {self.colors.success};
  --warning: {self.colors.warning};
  --error: {self.colors.error};
  --background: {self.colors.background};
  --surface: {self.colors.surface};
  --text: {self.colors.text};
}}

.bg-primary {{ background-color: {self.colors.primary}; }}
.bg-secondary {{ background-color: {self.colors.secondary}; }}
.text-primary {{ color: {self.colors.primary}; }}
.border-primary {{ border-color: {self.colors.primary}; }}
.btn-primary {{ 
  background-color: {self.colors.primary}; 
  color: {self.colors.text};
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
}}
"""
    
    def export_config(self) -> Dict:
        """導出配置"""
        return {
            "name": self.name,
            "description": self.description,
            "colors": asdict(self.colors)
        }
    
    def to_json(self) -> str:
        """轉為 JSON"""
        return json.dumps(self.export_config(), indent=2, ensure_ascii=False)


class ThemeFactory:
    """主題工廠"""
    
    PRESETS = {
        "longhun-cyber": ThemeColor(
            primary="#00d4ff",
            secondary="#00f5ff",
            accent="#ff006e",
            success="#4ade80",
            warning="#facc15",
            error="#ff006e",
            info="#06b6d4",
            background="#0a0e27",
            surface="#151a3f",
            text="#ffffff",
            text_secondary="#a0aec0"
        ),
        "longhun-dark": ThemeColor(
            primary="#3b82f6",
            secondary="#1e40af",
            accent="#f97316",
            success="#22c55e",
            warning="#eab308",
            error="#ef4444",
            info="#0ea5e9",
            background="#0f172a",
            surface="#1e293b",
            text="#f8fafc",
            text_secondary="#94a3b8"
        ),
        "longhun-light": ThemeColor(
            primary="#3b82f6",
            secondary="#60a5fa",
            accent="#f97316",
            success="#22c55e",
            warning="#eab308",
            error="#ef4444",
            info="#0ea5e9",
            background="#f8fafc",
            surface="#ffffff",
            text="#1f2937",
            text_secondary="#6b7280"
        ),
        "oceanic": ThemeColor(
            primary="#0ea5e9",
            secondary="#06b6d4",
            accent="#14b8a6",
            success="#10b981",
            warning="#f59e0b",
            error="#ef4444",
            info="#3b82f6",
            background="#0f172a",
            surface="#1e293b",
            text="#f1f5f9",
            text_secondary="#cbd5e1"
        ),
        "sunset": ThemeColor(
            primary="#f97316",
            secondary="#fb923c",
            accent="#ec4899",
            success="#10b981",
            warning="#eab308",
            error="#ef4444",
            info="#3b82f6",
            background="#1f2937",
            surface="#374151",
            text="#f3f4f6",
            text_secondary="#d1d5db"
        ),
        "forest": ThemeColor(
            primary="#10b981",
            secondary="#34d399",
            accent="#8b5cf6",
            success="#22c55e",
            warning="#f59e0b",
            error="#ef4444",
            info="#3b82f6",
            background="#065f46",
            surface="#047857",
            text="#f0fdf4",
            text_secondary="#d1fae5"
        ),
        "violet": ThemeColor(
            primary="#8b5cf6",
            secondary="#a78bfa",
            accent="#ec4899",
            success="#10b981",
            warning="#f59e0b",
            error="#ef4444",
            info="#06b6d4",
            background="#1e1b4b",
            surface="#312e81",
            text="#f3f4f6",
            text_secondary="#d1d5db"
        ),
        "monochrome": ThemeColor(
            primary="#6b7280",
            secondary="#9ca3af",
            accent="#374151",
            success="#4b5563",
            warning="#6b7280",
            error="#111827",
            info="#9ca3af",
            background="#f9fafb",
            surface="#f3f4f6",
            text="#111827",
            text_secondary="#6b7280"
        ),
        "retro": ThemeColor(
            primary="#d4af37",
            secondary="#c9a961",
            accent="#8b0000",
            success="#228b22",
            warning="#ff8c00",
            error="#dc143c",
            info="#4169e1",
            background="#2f4f4f",
            surface="#36454f",
            text="#f5deb3",
            text_secondary="#daa520"
        ),
        "neon": ThemeColor(
            primary="#39ff14",
            secondary="#ff006e",
            accent="#00d4ff",
            success="#39ff14",
            warning="#ff00ff",
            error="#ff006e",
            info="#00d4ff",
            background="#0a0a0a",
            surface="#1a1a1a",
            text="#39ff14",
            text_secondary="#ff006e"
        )
    }
    
    @staticmethod
    def create_theme(name: str, colors: ThemeColor, description: str = "") -> Theme:
        """創建自定義主題"""
        return Theme(name, colors, description)
    
    @staticmethod
    def get_preset(preset_name: str) -> Theme:
        """獲取預設主題"""
        if preset_name not in ThemeFactory.PRESETS:
            raise ValueError(f"Unknown preset: {preset_name}")
        
        colors = ThemeFactory.PRESETS[preset_name]
        return Theme(preset_name, colors)
    
    @staticmethod
    def list_presets() -> List[str]:
        """列出所有預設主題"""
        return list(ThemeFactory.PRESETS.keys())
    
    @staticmethod
    def export_all_css(output_file: str = None) -> str:
        """導出所有主題的 CSS"""
        css = "/* 龍魂主題工廠 - 所有主題 */\n\n"
        
        for preset_name in ThemeFactory.list_presets():
            theme = ThemeFactory.get_preset(preset_name)
            css += f"/* {theme.name} 主題 */\n"
            css += theme.generate_css_variables()
            css += theme.generate_css_classes()
            css += "\n"
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(css)
        
        return css
    
    @staticmethod
    def export_all_json(output_file: str = None) -> str:
        """導出所有主題的 JSON"""
        themes = {}
        for preset_name in ThemeFactory.list_presets():
            theme = ThemeFactory.get_preset(preset_name)
            themes[preset_name] = theme.export_config()
        
        json_str = json.dumps(themes, indent=2, ensure_ascii=False)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_str)
        
        return json_str


# 示例使用
if __name__ == "__main__":
    print("🐉 龍魂主題工廠 v1.0")
    print("=" * 50)
    
    # 列出所有預設主題
    print("\n📋 可用的預設主題:")
    for i, preset in enumerate(ThemeFactory.list_presets(), 1):
        print(f"  {i}. {preset}")
    
    # 創建自定義主題
    print("\n🎨 創建自定義主題...")
    custom_colors = ThemeColor(
        primary="#ff0080",
        secondary="#ff6eb4",
        accent="#00ffff",
        success="#00ff00",
        warning="#ffff00",
        error="#ff0000",
        info="#00ffff",
        background="#0d0221",
        surface="#0f0935",
        text="#e0e0e0",
        text_secondary="#999999"
    )
    custom_theme = ThemeFactory.create_theme("custom-pink", custom_colors, "自定義粉紅主題")
    
    print(f"✅ 主題已創建: {custom_theme.name}")
    print("\n主題配置:")
    print(custom_theme.to_json())
    
    # 獲取預設主題
    print("\n\n📌 獲取預設主題: longhun-cyber")
    cyber_theme = ThemeFactory.get_preset("longhun-cyber")
    print(cyber_theme.generate_css_variables())
    
    # 導出所有 CSS
    print("\n💾 導出所有主題 CSS...")
    ThemeFactory.export_all_css("/mnt/user-data/outputs/themes.css")
    print("✅ CSS 已保存: /mnt/user-data/outputs/themes.css")
    
    # 導出所有 JSON
    print("\n💾 導出所有主題 JSON...")
    ThemeFactory.export_all_json("/mnt/user-data/outputs/themes.json")
    print("✅ JSON 已保存: /mnt/user-data/outputs/themes.json")
    
    print("\n✅ 所有操作已完成！")
