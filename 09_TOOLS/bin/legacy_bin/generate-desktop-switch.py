#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
从 desktop/menu-registry.json 与各模块的 desktop-menu.json 动态生成
桌面主开关 AppleScript 源码。

新增约定：
  - mode="daemon"   : 点一次后长期运行（窗口 / 服务），标注“🟢常驻”
  - mode="oneshot"  : 点一次执行完就结束（预设），标注“▶点一次”
  - mode="viewer"   : 只打开文件/网页/文档，标注“👁只看”
  - mode="setup"    : 安装/配置类，标注“⚙️配置”

DNA:#龍芯⚡️丙午·甲午·癸亥·戊午·䷚颐-LONGHUN-GENERATE-DESKTOP-SWITCH-FILE1-v1.2
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "desktop" / "menu-registry.json"
SOURCE_PATH = ROOT / "desktop" / "龍魂主开关.applescript"

# 模式标注（附加在菜单文字后面，让用户一眼知道要不要手动跟进）
MODE_BADGES = {
    "daemon": "  🟢常驻",
    "oneshot": "  ▶点一次",
    "viewer": "  👁只看",
    "setup": "  ⚙️配置",
}

# 菜单排序权重：常驻/配置放前面，手动执行放中间，纯查看放后面，退出最后
MODE_ORDER = {"daemon": 0, "setup": 1, "oneshot": 2, "viewer": 3, "quit": 9}


def as_string_literal(value: str) -> str:
    """Escape a Python string for embedding in an AppleScript string literal."""
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")


def load_json(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  读取 {path} 失败: {e}", file=sys.stderr)
        return {}


def discover_menu_files(root: Path) -> list[Path]:
    discovered = []
    exclude = {".git", "__pycache__", ".pytest_cache", "node_modules", "venv", ".venv"}
    for path in root.rglob("desktop-menu.json"):
        # 跳过被排除目录
        if any(part in exclude for part in path.parts):
            continue
        if path.resolve() == REGISTRY_PATH.resolve():
            continue
        discovered.append(path)
    return sorted(discovered)


def build_registry() -> dict[str, Any]:
    registry = load_json(REGISTRY_PATH)
    if "items" not in registry:
        registry["items"] = []

    existing_ids = {item.get("id") for item in registry["items"] if item.get("id")}

    for menu_file in discover_menu_files(ROOT):
        data = load_json(menu_file)
        for item in data.get("items", []):
            item_id = item.get("id")
            if not item_id:
                continue
            if item_id in existing_ids:
                # 注册表优先，忽略同名模块项目
                continue
            # 补上来源信息，方便调试
            item["_source"] = str(menu_file.relative_to(ROOT))
            registry["items"].append(item)
            existing_ids.add(item_id)

    # 按模式分组排序，但保持各组内原有顺序
    registry["items"].sort(
        key=lambda item: MODE_ORDER.get(item.get("mode", "oneshot" if item.get("type") != "quit" else "quit"), 5)
    )

    return registry


def display_label(item: dict[str, Any]) -> str:
    """生成带模式标注的菜单显示文字。"""
    label = item.get("label", "未命名")
    if item.get("type") == "quit":
        return label
    mode = item.get("mode", "oneshot")
    badge = MODE_BADGES.get(mode, "")
    return label + badge


def generate_applescript(registry: dict[str, Any]) -> str:
    root_str = as_string_literal(str(ROOT))
    items = registry.get("items", [])

    # 收集菜单显示标签
    labels = []
    for item in items:
        label = display_label(item)
        if label:
            labels.append(label)

    labels_block = ", ".join(f'"{as_string_literal(label)}"' for label in labels)

    prompt_text = (
        "选择要执行的操作，不用记任何命令："
        "🟢常驻=点一次长期运行；"
        "▶点一次=跑完就停；"
        "👁只看=只开文件/网页；"
        "⚙️配置=改设定"
    )

    lines = [
        "-- 龍魂系统桌面主开关（动态生成）",
        "-- 来源：desktop/menu-registry.json + 各模块 desktop-menu.json",
        f"-- DNA: #龍芯⚡️丙午·甲午·癸亥·戊午·䷚颐-LONGHUN-MASTER-SWITCH-v{registry.get('version', '1.2')}",
        "",
        f'property rootPath : "{root_str}"',
        f"property menuItems : {{{labels_block}}}",
        "",
        "repeat",
        f'    set choice to choose from list menuItems with title "🐉 龍魂主开关" with prompt "{as_string_literal(prompt_text)}" default items {{item 1 of menuItems}} OK button name "执行" cancel button name "退出"',
        "    if choice is false then exit repeat",
        "    set selected to item 1 of choice",
        '    if selected is "退出" then exit repeat',
        "",
        "    try",
        "        set resultText to runMenu(selected)",
        "        if length of resultText > 900 then",
        '            set resultText to (text 1 thru 900 of resultText) & "\\n...（输出过长，请查看日志）"',
        "        end if",
        '        display dialog resultText buttons {"确定"} default button "确定" with title "🐉 龍魂主开关"',
        "    on error errMsg",
        '        display dialog "执行出错：" & errMsg buttons {"确定"} default button "确定" with icon stop',
        "    end try",
        "end repeat",
        "",
        "on runMenu(selected)",
        '    set qRoot to quoted form of rootPath',
    ]

    first = True
    for item in items:
        item_type = item.get("type", "shell")
        label = display_label(item)
        if not label or item_type == "quit":
            continue

        prefix = "    " if first else "    else "
        first = False

        lines.append(f'{prefix}if selected is "{as_string_literal(label)}" then')

        confirm = item.get("confirm", False)
        if confirm:
            lines.extend([
                '        set userChoice to display dialog "' + as_string_literal(item.get("description", "确认执行？")) + '" buttons {"取消", "确定"} default button "确定" with icon caution',
                '        if button returned of userChoice is "取消" then',
                '            return "已取消"',
                "        end if",
            ])

        mode = item.get("mode", "oneshot")

        if item_type == "shell":
            cmd = item.get("command", "echo '未设定命令'")
            cmd = cmd.replace("{root}", root_str)
            cmd = as_string_literal(cmd)
            lines.append(f'        return do shell script "{cmd}"')
        elif item_type == "open_url":
            url = as_string_literal(item.get("url", "http://127.0.0.1:9622"))
            lines.append(f'        do shell script "open \\"{url}\\""')
            lines.append(f'        return "已打开 {url}"')
        elif item_type == "open_app":
            app = as_string_literal(item.get("app", "Terminal"))
            path = as_string_literal(item.get("path", root_str).replace("{root}", root_str))
            lines.append(f'        do shell script "open -a \\"{app}\\" \\"{path}\\""')
            lines.append('        return "已打开应用"')
        else:
            lines.append('        return "未支持的类型：' + as_string_literal(item_type) + '"')

        # 常驻/配置类执行后，追加一句温馨提示
        if mode in ("daemon", "setup"):
            if mode == "daemon":
                lines.append('        -- 上面已经 return，以下只是备注：常驻服务点一次即可，不需要反复点')
            # 因为 shell 分支已经 return，这里的追加注解不会执行；保留给未来扩展使用

    if not first:
        lines.append("    end if")
    lines.append("end runMenu")
    lines.append("")

    return "\n".join(lines)


def main():
    registry = build_registry()
    source = generate_applescript(registry)

    SOURCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SOURCE_PATH, "w", encoding="utf-8") as f:
        f.write(source)

    print(f"✅ 已生成主开关源码: {SOURCE_PATH}")
    print(f"   菜单项数量: {len(registry.get('items', []))}")
    discovered = [i for i in registry.get("items", []) if i.get("_source")]
    if discovered:
        print(f"   自动发现模块菜单: {len(discovered)} 项")
        for i in discovered:
            print(f"      - {display_label(i)} ({i['_source']})")


if __name__ == "__main__":
    main()
