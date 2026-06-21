#!/usr/bin/env python3
"""
從 desktop/menu-registry.json 與各模塊的 desktop-menu.json 動態生成
桌面主开关 AppleScript 源碼。

新增約定：
  - mode="daemon"   : 點一次後長期運行（窗口 / 服務），標註「🟢常駐」
  - mode="oneshot"  : 點一次執行完就結束（預設），標註「▶點一次」
  - mode="viewer"   : 只打開文件/網頁/文檔，標註「👁只看」
  - mode="setup"    : 安裝/配置類，標註「⚙️配置」

DNA:#龍芯⚡️2026-06-18-LONGHUN-GENERATE-DESKTOP-SWITCH-FILE1-v1.2
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "desktop" / "menu-registry.json"
SOURCE_PATH = ROOT / "desktop" / "龍魂主开关.applescript"

# 模式標註（附加在菜單文字後面，讓用戶一眼知道要不要手動跟進）
MODE_BADGES = {
    "daemon": "  🟢常駐",
    "oneshot": "  ▶點一次",
    "viewer": "  👁只看",
    "setup": "  ⚙️配置",
}

# 菜單排序權重：常駐/配置放前面，手動執行放中間，純查看放後面，退出最後
MODE_ORDER = {"daemon": 0, "setup": 1, "oneshot": 2, "viewer": 3, "quit": 9}


def as_string_literal(value: str) -> str:
    """Escape a Python string for embedding in an AppleScript string literal."""
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")


def load_json(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  讀取 {path} 失敗: {e}", file=sys.stderr)
        return {}


def discover_menu_files(root: Path) -> list[Path]:
    discovered = []
    exclude = {".git", "__pycache__", ".pytest_cache", "node_modules", "venv", ".venv"}
    for path in root.rglob("desktop-menu.json"):
        # 跳過被排除目錄
        if any(part in exclude for part in path.parts):
            continue
        if path.resolve() == REGISTRY_PATH.resolve():
            continue
        discovered.append(path)
    return sorted(discovered)


def build_registry() -> dict:
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
                # 註冊表優先，忽略同名模塊項目
                continue
            # 補上來源信息，方便調試
            item["_source"] = str(menu_file.relative_to(ROOT))
            registry["items"].append(item)
            existing_ids.add(item_id)

    # 按模式分組排序，但保持各組內原有順序
    registry["items"].sort(
        key=lambda item: MODE_ORDER.get(item.get("mode", "oneshot" if item.get("type") != "quit" else "quit"), 5)
    )

    return registry


def display_label(item: dict) -> str:
    """生成帶模式標註的菜單顯示文字。"""
    label = item.get("label", "未命名")
    if item.get("type") == "quit":
        return label
    mode = item.get("mode", "oneshot")
    badge = MODE_BADGES.get(mode, "")
    return label + badge


def generate_applescript(registry: dict) -> str:
    root_str = as_string_literal(str(ROOT))
    items = registry.get("items", [])

    # 收集菜單顯示標籤
    labels = []
    for item in items:
        label = display_label(item)
        if label:
            labels.append(label)

    labels_block = ", ".join(f'"{as_string_literal(label)}"' for label in labels)

    prompt_text = (
        "選擇要執行的操作，不用記任何命令："
        "🟢常駐=點一次長期運行；"
        "▶點一次=跑完就停；"
        "👁只看=只開文件/網頁；"
        "⚙️配置=改設定"
    )

    lines = [
        "-- 龍魂系統桌面主开关（動態生成）",
        "-- 來源：desktop/menu-registry.json + 各模塊 desktop-menu.json",
        f"-- DNA: #龍芯⚡️2026-06-18-LONGHUN-MASTER-SWITCH-v{registry.get('version', '1.2')}",
        "",
        f'property rootPath : "{root_str}"',
        f"property menuItems : {{{labels_block}}}",
        "",
        "repeat",
        f'    set choice to choose from list menuItems with title "🐉 龍魂主开关" with prompt "{as_string_literal(prompt_text)}" default items {{item 1 of menuItems}} OK button name "執行" cancel button name "退出"',
        "    if choice is false then exit repeat",
        "    set selected to item 1 of choice",
        '    if selected is "退出" then exit repeat',
        "",
        "    try",
        "        set resultText to runMenu(selected)",
        "        if length of resultText > 900 then",
        '            set resultText to (text 1 thru 900 of resultText) & "\\n...（輸出過長，請查看日誌）"',
        "        end if",
        '        display dialog resultText buttons {"確定"} default button "確定" with title "🐉 龍魂主开关"',
        "    on error errMsg",
        '        display dialog "執行出錯：" & errMsg buttons {"確定"} default button "確定" with icon stop',
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
                '        set userChoice to display dialog "' + as_string_literal(item.get("description", "確認執行？")) + '" buttons {"取消", "確定"} default button "確定" with icon caution',
                '        if button returned of userChoice is "取消" then',
                '            return "已取消"',
                "        end if",
            ])

        mode = item.get("mode", "oneshot")

        if item_type == "shell":
            cmd = item.get("command", "echo '未設定命令'")
            cmd = cmd.replace("{root}", root_str)
            cmd = as_string_literal(cmd)
            lines.append(f'        return do shell script "{cmd}"')
        elif item_type == "open_url":
            url = as_string_literal(item.get("url", "http://127.0.0.1:9622"))
            lines.append(f'        do shell script "open \\"{url}\\""')
            lines.append(f'        return "已打開 {url}"')
        elif item_type == "open_app":
            app = as_string_literal(item.get("app", "Terminal"))
            path = as_string_literal(item.get("path", root_str).replace("{root}", root_str))
            lines.append(f'        do shell script "open -a \\"{app}\\" \\"{path}\\""')
            lines.append('        return "已打開應用"')
        else:
            lines.append('        return "未支持的類型：' + as_string_literal(item_type) + '"')

        # 常駐/配置類執行後，追加一句溫馨提示
        if mode in ("daemon", "setup"):
            if mode == "daemon":
                lines.append('        -- 上面已經 return，以下只是備註：常駐服務點一次即可，不需要反覆點')
            # 因為 shell 分支已經 return，這裡的追加註解不會執行；保留給未來擴展使用

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

    print(f"✅ 已生成主开关源碼: {SOURCE_PATH}")
    print(f"   菜單項數量: {len(registry.get('items', []))}")
    discovered = [i for i in registry.get("items", []) if i.get("_source")]
    if discovered:
        print(f"   自動發現模塊菜單: {len(discovered)} 項")
        for i in discovered:
            print(f"      - {display_label(i)} ({i['_source']})")


if __name__ == "__main__":
    main()
