#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成龍魂 CodeBuddy 扩展的统一品牌资产
为 4 个扩展补齐：icon.png/svg、徽章、README、CHANGELOG、LICENSE、CONTRIBUTORS、CONTRIBUTING
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent

MODULES = {
    "longhun-console": {
        "display": "龍魂控制台",
        "short": "控制台",
        "desc": "龍魂系统 CodeBuddy 侧边栏专属面板 — 系统状态、DNA锚定、审计日志、一键 lh 命令",
        "color": "#8B5CF6",  # violet
        "accent": "#D4AF37",
        "glyph": "控",
        "categories": ["Other", "Visualization"],
        "keywords": ["龍魂", "longhun", "控制台", "console", "侧边栏", "总控面板", "蚁群", "DNA锚定", "CNSH", "中国自主", "诸葛鑫", "uid9622"],
        "features": [
            ("📡 服务状态", "实时探测蚁群、神经网络、控制面板端口是否在线"),
            ("🧠 系统快照", "人格矩阵、引擎总数、蚁群 tick、涌现 E 值"),
            ("🛡️ 三色审计", "绿/黄/红审计统计，实时读取 action_log.jsonl"),
            ("🖥️ lh 命令", "一键打开终端执行 lh 命令"),
            ("📊 总控面板", "一键打开浏览器总控台"),
            ("🐜 蚁群控制台", "一键打开蚁群调试面板"),
        ],
        "commands": [
            ("龍魂: 执行 lh 命令", "快速执行 lh 控制台"),
            ("龍魂: 打开总控面板", "打开浏览器总控台"),
            ("龍魂: 打开蚁群控制台", "打开蚁群调试面板"),
            ("龍魂: 快速审计", "执行一次快速审计"),
            ("龍魂: 切换开发者面板", "显示/隐藏开发者面板"),
        ],
        "config": "longhun-console",
        "config_props": [
            ('"longhun-console.refreshInterval": 5000', "刷新间隔（毫秒）"),
            ('"longhun-console.showStatusBar": true', "在状态栏显示系统状态"),
        ],
        "dna": "CODEBUDDY-LONGHUN-CONSOLE-v1.0",
    },
    "model-router": {
        "display": "龍魂多模型路由",
        "short": "多模型路由",
        "desc": "DeepSeek/Kimi/本地模型一键切换 — 根据任务类型自动选择：代码生成→DeepSeek，审查→Kimi，敏感操作→本地模型",
        "color": "#06B6D4",  # cyan
        "accent": "#D4AF37",
        "glyph": "路",
        "categories": ["Other", "Machine Learning", "Snippets"],
        "keywords": ["龍魂", "longhun", "模型路由", "model-router", "DeepSeek", "Kimi", "本地模型", "LLM", "AI", "代码生成", "代码审查", "CNSH", "中国自主", "诸葛鑫", "uid9622"],
        "features": [
            ("🔄 一键切换", "DeepSeek / Kimi / 本地模型 快速切换"),
            ("🧠 任务路由", "按任务类型自动选择最优模型"),
            ("🔐 敏感本地", "敏感操作强制使用本地模型，数据不出本机"),
            ("⚡ 状态栏显示", "当前模型状态一目了然"),
            ("🛠️ 灵活配置", "API Key 仅本地存储，不上传云端"),
        ],
        "commands": [
            ("龍魂: 切换到 DeepSeek", "切到 DeepSeek 模型"),
            ("龍魂: 切换到 Kimi", "切到 Kimi 模型"),
            ("龍魂: 切换到本地模型", "切到本地模型"),
            ("龍魂: 自动路由（按任务类型）", "让系统按任务类型自动选择"),
            ("龍魂: 查看当前模型路由状态", "显示当前模型和任务映射"),
        ],
        "config": "longhun-model",
        "config_props": [
            ('"longhun-model.defaultModel": "auto"', "默认模型：auto / deepseek / kimi / local"),
            ('"longhun-model.codeGenModel": "deepseek"', "代码生成任务模型"),
            ('"longhun-model.codeReviewModel": "kimi"', "代码审查任务模型"),
            ('"longhun-model.sensitiveModel": "local"', "敏感操作任务模型"),
            ('"longhun-model.deepseekApiKey": ""', "DeepSeek API Key（本地存储）"),
            ('"longhun-model.kimiApiKey": ""', "Kimi API Key（本地存储）"),
            ('"longhun-model.localModelPath": ""', "本地模型路径"),
        ],
        "dna": "MODEL-ROUTER-v1.0",
    },
    "audit-tracker": {
        "display": "龍魂审计追踪",
        "short": "审计追踪",
        "desc": "AI生成代码自动审计追踪 — 记录模型来源、提示词哈希、生成时间、审核结果，写入本地审计日志，不上传云端",
        "color": "#F59E0B",  # amber
        "accent": "#D4AF37",
        "glyph": "审",
        "categories": ["Other", "Linters"],
        "keywords": ["龍魂", "longhun", "审计", "audit", "追踪", "AI生成代码", "提示词哈希", "合规", "CNSH", "中国自主", "诸葛鑫", "uid9622"],
        "features": [
            ("📝 自动记录", "保存/粘贴 AI 生成代码时自动写审计日志"),
            ("🔍 哈希追踪", "记录提示词哈希、模型来源、生成时间"),
            ("✅ 审核状态", "标记为已审核 / 待审核"),
            ("📊 报告导出", "一键生成审计报告"),
            ("🛡️ 本地优先", "日志写入本地，不上传云端"),
        ],
        "commands": [
            ("龍魂: 查看审计日志", "打开审计日志面板"),
            ("龍魂: 审计选中代码", "对选中代码进行审计"),
            ("龍魂: 生成审计报告", "导出当前审计报告"),
            ("龍魂: 标记为已审核", "将选中记录标记已审核"),
        ],
        "config": "longhun-audit",
        "config_props": [
            ('"longhun-audit.auditLogPath": ""', "审计日志路径（默认 logs/ai_audit.jsonl）"),
            ('"longhun-audit.autoAuditOnPaste": true', "粘贴代码时自动记录审计"),
            ('"longhun-audit.autoAuditOnSave": true', "保存文件时自动审计"),
            ('"longhun-audit.showStatusBar": true', "在状态栏显示审计计数"),
        ],
        "dna": "AUDIT-TRACKER-v1.0",
    },
    "protocol-checker": {
        "display": "龍魂协议校验",
        "short": "协议校验",
        "desc": "保存文件时自动扫描 — 检查DNA锚定、老祖宗规则、敏感信息泄露。违规弹窗警告，一键修复",
        "color": "#22C55E",  # green
        "accent": "#D4AF37",
        "glyph": "盾",
        "categories": ["Linters", "Other"],
        "keywords": ["龍魂", "longhun", "协议校验", "protocol-checker", "DNA锚定", "老祖宗规则", "敏感信息", "安全", "合规", "CNSH", "中国自主", "诸葛鑫", "uid9622"],
        "features": [
            ("🛡️ DNA 校验", "检查文件是否包含 DNA 锚定码"),
            ("🏛️ 老祖宗规则", "检查境外 API 导入、云端上传、敏感库"),
            ("🔐 敏感信息", "检测密钥、Token、密码、私钥泄露"),
            ("⚠️ 即时警告", "违规时弹窗提示并定位到行"),
            ("🔧 一键修复", "自动修复可修复的违规项"),
        ],
        "commands": [
            ("龍魂: 协议校验当前文件", "扫描当前文件"),
            ("龍魂: 协议校验整个工作区", "扫描整个工作区"),
            ("龍魂: 一键修复当前文件", "自动修复当前文件"),
        ],
        "config": "longhun-protocol",
        "config_props": [
            ('"longhun-protocol.enableDNA": true', "检查 DNA 锚定码"),
            ('"longhun-protocol.enableAncestors": true', "检查老祖宗规则"),
            ('"longhun-protocol.enableSensitive": true', "检查敏感信息泄露"),
            ('"longhun-protocol.autoFixOnSave": false', "保存时自动修复（谨慎开启）"),
            ('"longhun-protocol.ignoredFiles": [...]', "忽略的文件模式"),
        ],
        "dna": "PROTOCOL-CHECKER-v1.0",
    },
}


def hex_to_rgb(h: str) -> tuple[Any, ...]:
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def render_icon_png(name: str, meta: dict[str, Any], size: int = 256) -> Image.Image:
    bg = hex_to_rgb("#0a0514")
    primary = hex_to_rgb(meta["color"])
    accent = hex_to_rgb(meta["accent"])

    img = Image.new("RGBA", (size, size), (*bg, 255))
    draw = ImageDraw.Draw(img)

    # outer rounded square (simulated with circles)
    margin = size // 16
    box = (margin, margin, size - margin, size - margin)
    radius = size // 8
    draw.rounded_rectangle(box, radius=radius, fill=(*primary, 40), outline=(*primary, 180), width=size//64)

    # 4-square grid inside
    cell_margin = size // 4
    cell_size = (size - 2 * cell_margin) // 2 - size // 64
    gap = size // 48
    cells = [
        (cell_margin, cell_margin, cell_margin + cell_size, cell_margin + cell_size),
        (cell_margin + cell_size + gap, cell_margin, cell_margin + 2*cell_size + gap, cell_margin + cell_size),
        (cell_margin, cell_margin + cell_size + gap, cell_margin + cell_size, cell_margin + 2*cell_size + gap),
        (cell_margin + cell_size + gap, cell_margin + cell_size + gap, cell_margin + 2*cell_size + gap, cell_margin + 2*cell_size + gap),
    ]
    for i, c in enumerate(cells):
        fill = (*accent, 220) if i == 0 else (*primary, 180)
        draw.rounded_rectangle(c, radius=size//32, fill=fill)

    # central glyph
    try:
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", size=size//2)
    except Exception:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=size//2)
        except Exception:
            font = ImageFont.load_default()
    glyph = meta["glyph"]
    bbox = draw.textbbox((0, 0), glyph, font=font)
    gw, gh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pos = ((size - gw) // 2, (size - gh) // 2 - size // 32)
    # drop shadow
    draw.text((pos[0] + size//128, pos[1] + size//128), glyph, font=font, fill=(0, 0, 0, 120))
    draw.text(pos, glyph, font=font, fill=(255, 255, 255, 255))

    return img


def render_icon_svg(name: str, meta: dict[str, Any]) -> str:
    c = meta["color"]
    a = meta["accent"]
    g = meta["glyph"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <rect width="256" height="256" rx="32" fill="#0a0514"/>
  <rect x="16" y="16" width="224" height="224" rx="28" fill="none" stroke="{c}" stroke-opacity="0.7" stroke-width="3"/>
  <rect x="64" y="64" width="60" height="60" rx="10" fill="{a}"/>
  <rect x="132" y="64" width="60" height="60" rx="10" fill="{c}" fill-opacity="0.7"/>
  <rect x="64" y="132" width="60" height="60" rx="10" fill="{c}" fill-opacity="0.7"/>
  <rect x="132" y="132" width="60" height="60" rx="10" fill="{c}" fill-opacity="0.7"/>
  <text x="128" y="148" font-family="PingFang SC, Microsoft YaHei, sans-serif" font-size="110" font-weight="bold" text-anchor="middle" fill="#ffffff">{g}</text>
</svg>"""


def generate_badge(text: str, sub: str, color: str, width: int = 200, height: int = 40) -> Image.Image:
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # rounded bg
    draw.rounded_rectangle((0, 0, width-1, height-1), radius=height//4, fill=hex_to_rgb(color))
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", height//2)
    except Exception:
        font = ImageFont.load_default()
    full = f"{text} {sub}"
    bbox = draw.textbbox((0, 0), full, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((width - tw)//2, (height - th)//2 - 1), full, font=font, fill=(255, 255, 255, 255))
    return img


def write_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def generate_readme(name: str, meta: dict[str, Any]) -> str:
    features = "\n".join(f"| {k} | {v} |" for k, v in meta["features"])
    commands = "\n".join(f"| `{k}` | {v} |" for k, v in meta["commands"])
    config_props = "\n".join(f'  {k},  // {v}' for k, v in meta["config_props"])
    keywords = " · ".join(meta["keywords"])
    categories = " · ".join(meta["categories"])
    return f"""# 🐉 {meta['display']}

> {meta['desc']}
> 龍魂系统 · 诸葛鑫(uid9622) · 中国自主可控工具链

![龍魂](images/icon.png)

---

[![龍魂](https://img.shields.io/badge/龍魂-v1.0.0-D4AF37?logo=visualstudiocode&labelColor=0a0514&logoColor=D4AF37)](https://marketplace.visualstudio.com/items?itemName=uid9622.{name})
[![License](https://img.shields.io/badge/License-CC--BY--NC--SA--4.0-22c55e?labelColor=0a0514)](./LICENSE)
[![GPG](https://img.shields.io/badge/GPG-A2D0092CEE2E5BA87035600924C3704A8CC26D5F-c41e3a?labelColor=0a0514)](https://keys.openpgp.org/search?q=A2D0092CEE2E5BA87035600924C3704A8CC26D5F)
[![Made with ❤️ in China](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F%20%E4%B8%AD%E5%9B%BD-c41e3a?labelColor=0a0514)]()

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
{features}

---

## 🚀 快速开始

1. 安装扩展后，按 `Ctrl+Shift+P`（macOS `Cmd+Shift+P`）
2. 输入：**`龍魂: `** 查看所有可用命令
3. 选择对应功能即可开始使用

---

## 🎮 命令面板

| 命令 | 作用 |
|------|------|
{commands}

---

## ⚙️ 配置项

在 `settings.json` 中搜索 `{meta['config']}`：

```json
{{
{config_props}
}}
```

---

## 🏷️ 标签与分类

- **分类**: {categories}
- **标签**: {keywords}

---

## 🤝 贡献者

欢迎提交 Issue / PR。  
详见 [CONTRIBUTORS.md](./CONTRIBUTORS.md) 与 [CONTRIBUTING.md](./CONTRIBUTING.md)。

---

## 📜 许可证

本扩展采用 **CC-BY-NC-SA-4.0** 许可协议。  
未经授权不得用于商业用途。

---

> 🐉 **龍魂系统** — 替老百姓守住数字主权，把 AI 的根扎在中国土地上。  
> DNA: `#龍芯⚡️丙午·辛未·{meta['dna']}`
"""


def generate_changelog() -> str:
    return """# 更新日志

## [1.0.0] - 2026-07-14

### 新增
- 初始版本发布
- 龍魂品牌统一：icon、徽章、README、LICENSE
- 完整命令面板与配置项

### 安全
- 纯本地运行，数据不上传云端
- 遵循龍魂 DNA 锚定与主权声明
"""


def generate_license() -> str:
    return """知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International

本作品采用 CC-BY-NC-SA-4.0 进行许可。

你可以：
- 共享 — 以任何媒介或格式复制、转载本作品
- 演绎 — 基于本作品进行再创作

但必须遵守：
- 署名 — 必须给出原作者姓名和许可链接
- 非商业性使用 — 不得用于商业目的
- 相同方式共享 — 演绎作品必须采用相同许可证

详见：https://creativecommons.org/licenses/by-nc-sa/4.0/

Copyright (c) 2026 龍魂系统 · 诸葛鑫(uid9622)
"""


def generate_contributors() -> str:
    return """# 贡献者

| 贡献者 | 角色 | 说明 |
|--------|------|------|
| 诸葛鑫 (uid9622) | 创始人 / 唯一决策者 | 龍魂系统创始人、CNSH 发起人 |
| 龍魂人格矩阵 P00-P72 | 守护与执行 | 16 人格协同审查与决策 |

## 如何贡献

1. 阅读 [CONTRIBUTING.md](./CONTRIBUTING.md)
2. 提交 Issue 描述问题或建议
3. 提交 Pull Request 并遵循龍魂 DNA 规范

> 所有贡献默认归属龍魂系统，保留 uid9622 最终决策权。
"""


def generate_contributing() -> str:
    return """# 贡献指南

## 提交前必读

1. 必须遵守 [龍魂宪法](../../../../01_protocols/BEICHEN-MOTHER-PROTOCOL-v2.0.md)
2. 不得引入境外依赖或上传云端的服务
3. 所有代码变更必须包含 DNA 锚定或主权声明
4. 不修改底座锚点（369/河图洛书/易经/道德经等）

## 开发流程

```bash
cd editors/codebuddy/<extension-name>
npm install
npm run watch    # 开发模式
npm run compile  # 生产编译
npx vsce package # 打包 VSIX
```

## 提交规范

- 提交信息使用中文
- 包含 DNA 追溯码
- 大改动先开 Issue 讨论

## 行为准则

- 为人民服务
- 数据主权归用户
- 技术服务于中国自主可控
"""


def update_package_json(pkg_path: Path, meta: dict[str, Any]):
    import json
    data = json.loads(pkg_path.read_text(encoding="utf-8"))
    data["icon"] = "images/icon.png"
    data["galleryBanner"] = {"color": "#0a0514", "theme": "dark"}
    data["repository"] = {
        "type": "git",
        "url": f"https://github.com/uid9622/longhun-system/tree/main/editors/codebuddy/{pkg_path.parent.name}"
    }
    data["bugs"] = {"url": "https://github.com/uid9622/longhun-system/issues"}
    data["homepage"] = f"https://github.com/uid9622/longhun-system/blob/main/editors/codebuddy/{pkg_path.parent.name}/README.md"
    data["categories"] = meta["categories"]
    data["keywords"] = meta["keywords"]
    pkg_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    for name, meta in MODULES.items():
        mod_dir = BASE / name
        img_dir = mod_dir / "images"
        img_dir.mkdir(parents=True, exist_ok=True)

        # icons
        icon_png = render_icon_png(name, meta)
        icon_png.save(img_dir / "icon.png")
        write_text(img_dir / "icon.svg", render_icon_svg(name, meta))

        # badges (reusable from one-click-deploy style, but generate local copies)
        badges = {
            "badge-version.png": ("龍魂", "v1.0.0", "#D4AF37"),
            "badge-license.png": ("License", "CC-BY-NC-SA-4.0", "#22c55e"),
            "badge-gpg.png": ("GPG", "A2D0...6D5F", "#c41e3a"),
            "badge-made-in-china.png": ("Made in", "China", "#c41e3a"),
        }
        for fname, (t, s, col) in badges.items():
            generate_badge(t, s, col).save(img_dir / fname)

        # docs
        write_text(mod_dir / "README.md", generate_readme(name, meta))
        write_text(mod_dir / "CHANGELOG.md", generate_changelog())
        write_text(mod_dir / "LICENSE", generate_license())
        write_text(mod_dir / "CONTRIBUTORS.md", generate_contributors())
        write_text(mod_dir / "CONTRIBUTING.md", generate_contributing())

        # package.json
        update_package_json(mod_dir / "package.json", meta)

        print(f"✅ {name} 品牌资产补齐完成")


if __name__ == "__main__":
    main()
