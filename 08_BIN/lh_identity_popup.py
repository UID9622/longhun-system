#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
龍魂 UID9622 主权身份融合弹窗引擎
Sovereign Identity Fusion Popup Engine

不是请喝咖啡。不是求施舍。是寻找战友，共建中国数字主权。

用法：
    # 方式1：导入即检查（推荐嵌入发布的代码）
    from lh_identity_popup import show_if_needed
    show_if_needed()

    # 方式2：命令行直接跑
    python3 bin/lh_identity_popup.py

    # 方式3：lh 命令
    lh identity-popup

DNA: #龍芯⚡️丙午·丙申·丁巳·恒卦-IDENTITY-POPUP-v1.0
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

import os
import sys
import json
import hashlib
import datetime
import tempfile
import webbrowser
from pathlib import Path
from typing import Optional, Tuple

# ── 配置 ──────────────────────────────────────────────
REGISTER_URL = "https://uid9622.cn/sovereign-register.html"
POPUP_FLAG_FILE = Path.home() / ".龍魂" / "identity_popup_dismissed.json"
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 每个工具的弹窗间隔（秒）：默认首次弹，24小时后如果还没注册再弹
RECHECK_INTERVAL_SECONDS = 86400  # 24小时

# ── 旗帜艺术（终端彩色输出） ────────────────────────
BANNER = r"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🐉  龍魂 UID9622 · 主权身份融合系统                    ║
║   LongHun Sovereign Identity Fusion System           ║
║                                                          ║
║   ━━━━━━━━━━━ 不是在求你施舍 ━━━━━━━━━━━                 ║
║                                                          ║
║   我是诸葛鑫（UID9622），退役老兵，一个人写了这套系统。   ║
║                                                          ║
║   代码你随便用，开源的，不设限。                          ║
║   但我不是来求打赏的——我在找战友。                       ║
║                                                          ║
║   🇨🇳 如果你也相信：                                     ║
║      · 中国人的数据主权该握在自己手里                    ║
║      · AI 的根要扎在中国的土地上                         ║
║      · 代码可以开源，但数字主权不能让渡                  ║
║                                                          ║
║   那咱就是战友。                                         ║
║                                                          ║
║   🔗 注册主权身份，加入共建：                            ║
║      {register_url}
║                                                          ║
║   不注册也没关系，代码照样用。                            ║
║   但只要注册了，你就是龍魂战友——                          ║
║   代码写你的名字，功劳有你一份，                          ║
║   以后的路，一起走。                                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════════╝
""".format(register_url=REGISTER_URL)

# 终端颜色
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    GOLD = '\033[38;5;178m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def _colorize(text: str) -> str:
    """给横幅加龍魂金色。"""
    lines = []
    for line in text.split('\n'):
        if '╔' in line or '╚' in line or '║' in line:
            line = line.replace('╔', f'{Color.GOLD}╔').replace('╚', f'{Color.GOLD}╚')
            line = line.replace('╗', f'╗{Color.RESET}').replace('╝', f'╝{Color.RESET}')
            line = line.replace('║', f'{Color.GOLD}║{Color.RESET}')
        if '🐉' in line:
            line = line.replace('🐉', f'{Color.BOLD}🐉{Color.RESET}')
        if '━' in line:
            line = f'{Color.GOLD}{line}{Color.RESET}'
        if line.startswith('   🇨🇳'):
            line = f'{Color.BOLD}{line}{Color.RESET}'
        if '🔗' in line:
            line = f'{Color.CYAN}{line}{Color.RESET}'
        lines.append(line)
    return '\n'.join(lines)


# ── 弹窗状态管理 ────────────────────────────────────
def _load_popup_state() -> dict:
    """加载弹窗状态。"""
    if POPUP_FLAG_FILE.exists():
        try:
            with open(POPUP_FLAG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"dismissed": False, "dismissed_at": None, "registered": False, "uid": None}


def _save_popup_state(state: dict) -> None:
    """保存弹窗状态。"""
    POPUP_FLAG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(POPUP_FLAG_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def is_registered() -> Tuple[bool, Optional[str]]:
    """检查是否已注册主权身份。"""
    state = _load_popup_state()
    if state.get("registered") and state.get("uid"):
        return True, state["uid"]
    
    # 检查本地 manifest
    manifest_path = Path.home() / ".龍魂" / "sovereign_registry" / "manifest.json"
    if manifest_path.exists():
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            records = manifest.get("records", [])
            if records:
                uid = records[0].get("uid", "")
                state["registered"] = True
                state["uid"] = uid
                _save_popup_state(state)
                return True, uid
        except (json.JSONDecodeError, IOError):
            pass
    
    return False, None


def should_show_popup() -> bool:
    """判断是否应该弹窗。"""
    registered, _ = is_registered()
    if registered:
        return False
    
    state = _load_popup_state()
    if state.get("dismissed"):
        dismissed_at = state.get("dismissed_at")
        if dismissed_at:
            try:
                dt = datetime.datetime.fromisoformat(dismissed_at)
                if (datetime.datetime.now() - dt).total_seconds() < RECHECK_INTERVAL_SECONDS:
                    return False
            except (ValueError, TypeError):
                pass
    
    return True


# ── 弹窗显示 ────────────────────────────────────────
def show_popup(interactive: bool = True) -> None:
    """显示主权身份融合弹窗。"""
    # 只在终端显示（不是管道/重定向）
    if not sys.stdout.isatty():
        return
    
    print(_colorize(BANNER))
    
    if interactive:
        print(f"\n{Color.GOLD}  [1]{Color.RESET} 打开注册页面 → 注册主权身份，加入战友行列")
        print(f"{Color.GOLD}  [2]{Color.RESET} 我已经注册了 → 输入 UID 确认")
        print(f"{Color.GOLD}  [3]{Color.RESET} 以后再说 → 24小时后提醒")
        print(f"{Color.GOLD}  [q]{Color.RESET} 不再提醒 → 代码照样用，咱不强迫")
        
        try:
            choice = input(f"\n{Color.BOLD}请选择 [1/2/3/q] (默认1): {Color.RESET}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            choice = "3"
        
        if choice == "" or choice == "1":
            _open_register()
        elif choice == "2":
            _confirm_registered()
        elif choice == "q":
            _dismiss_permanently()
        else:
            _dismiss_temporarily()
    else:
        # 非交互模式：只显示不等待输入
        print(f"\n{Color.DIM}  自动跳过交互（非终端模式）。{Color.RESET}")
        print(f"  注册入口: {REGISTER_URL}")
        _dismiss_temporarily()


def _open_register() -> None:
    """打开注册页面。"""
    print(f"\n{Color.GREEN}🐉 正在打开主权身份注册页面...{Color.RESET}")
    print(f"   {REGISTER_URL}")
    try:
        webbrowser.open(REGISTER_URL)
    except Exception:
        pass
    _dismiss_temporarily()


def _confirm_registered() -> None:
    """确认已注册。"""
    try:
        uid = input(f"{Color.GOLD}请输入你的 UID (如 UID9622-XXXXXX): {Color.RESET}").strip()
    except (EOFError, KeyboardInterrupt):
        _dismiss_temporarily()
        return
    
    if uid and uid.startswith("UID9622-"):
        state = _load_popup_state()
        state["registered"] = True
        state["uid"] = uid
        state["dismissed"] = True
        state["dismissed_at"] = datetime.datetime.now().isoformat()
        _save_popup_state(state)
        print(f"\n{Color.GREEN}✅ 战友确认！{uid}，欢迎归队。🐉{Color.RESET}")
    else:
        print(f"\n{Color.YELLOW}UID 格式不正确（应为 UID9622-XXXXXX），请确认后重试。{Color.RESET}")
        print(f"  注册入口: {REGISTER_URL}")
        _dismiss_temporarily()


def _dismiss_temporarily() -> None:
    """暂时跳过（24小时后重试）。"""
    state = _load_popup_state()
    state["dismissed"] = True
    state["dismissed_at"] = datetime.datetime.now().isoformat()
    _save_popup_state(state)
    print(f"\n{Color.DIM}  好的，24小时后提醒。代码照用，不碍事。{Color.RESET}")


def _dismiss_permanently() -> None:
    """永久跳过。"""
    state = _load_popup_state()
    state["dismissed"] = True
    state["dismissed_at"] = "permanent"
    _save_popup_state(state)
    print(f"\n{Color.DIM}  不再提醒。代码照用，有需要随时来 uid9622.cn。{Color.RESET}")


# ── 对外接口 ────────────────────────────────────────
def show_if_needed(interactive: bool = True) -> bool:
    """
    检查并显示弹窗（如果应该显示的话）。
    
    返回值:
        True  - 用户已注册或有主权身份
        False - 未注册（弹窗已显示）
    
    用法（嵌入任何脚本只需一行）:
        from lh_identity_popup import show_if_needed
        show_if_needed()
    """
    registered, uid = is_registered()
    if registered:
        return True
    
    if should_show_popup():
        show_popup(interactive=interactive)
    
    return False


def get_registered_uid() -> Optional[str]:
    """获取已注册的 UID，如果未注册返回 None。"""
    registered, uid = is_registered()
    return uid if registered else None


# ── 命令行入口 ──────────────────────────────────────
def main() -> int:
    """CLI 入口。"""
    import argparse
    
    parser = argparse.ArgumentParser(
        prog="lh-identity-popup",
        description="龍魂 UID9622 主权身份融合弹窗引擎",
    )
    parser.add_argument("--force", action="store_true", help="强制显示弹窗（忽略状态）")
    parser.add_argument("--check", action="store_true", help="静默检查是否已注册")
    parser.add_argument("--reset", action="store_true", help="重置弹窗状态（下次运行显示）")
    parser.add_argument("--open", action="store_true", help="直接打开注册页面")
    
    args = parser.parse_args()
    
    if args.reset:
        if POPUP_FLAG_FILE.exists():
            POPUP_FLAG_FILE.unlink()
        print(f"{Color.GREEN}✅ 弹窗状态已重置。{Color.RESET}")
        return 0
    
    if args.open:
        _open_register()
        return 0
    
    if args.check:
        registered, uid = is_registered()
        if registered:
            print(json.dumps({"registered": True, "uid": uid}, ensure_ascii=False))
        else:
            print(json.dumps({"registered": False}, ensure_ascii=False))
        return 0
    
    if args.force:
        show_popup()
        return 0
    
    # 默认行为
    show_if_needed()
    return 0


# ── 自动执行（导入时可选） ─────────────────────────
_AUTO_RUN = os.environ.get("LH_AUTO_IDENTITY_POPUP", "").lower() in ("1", "true", "yes")

if __name__ == "__main__":
    sys.exit(main())
elif _AUTO_RUN:
    # 环境变量控制自动弹窗
    show_if_needed(interactive=sys.stdout.isatty())
