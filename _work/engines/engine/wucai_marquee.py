#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════
# 龍魂五彩跑马灯 v1.0
# DNA: #龍芯⚡️2026-05-23-WUCAI-MARQUEE-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: UID9622 诸葛鑫
# 理论指导: 曾仕强老师（永恒显示）
#
# 五行五色：金白·木绿·水蓝·火红·土黄
# 不动点缓存：颜色序列预计算·跑起来零开销
# ═══════════════════════════════════════════════════════════
# -*- coding: utf-8 -*-

import sys
import time
from typing import List, Tuple
from functools import lru_cache

# ============================================================
# 五行颜色定义（ANSI 256色）
# ============================================================

WUXING_COLORS = {
    "金": "\033[97m",      # 亮白
    "木": "\033[92m",      # 亮绿
    "水": "\033[96m",      # 亮青
    "火": "\033[91m",      # 亮红
    "土": "\033[93m",      # 亮黄
}

WUXING_COLORS_BOLD = {
    "金": "\033[1;97m",    # 粗亮白
    "木": "\033[1;92m",    # 粗亮绿
    "水": "\033[1;96m",    # 粗亮青
    "火": "\033[1;91m",    # 粗亮红
    "土": "\033[1;93m",    # 粗亮黄
}

# 渐变扩展（更丰富的视觉）
WUXING_GRADIENT = {
    "金": ["\033[38;5;255m", "\033[38;5;253m", "\033[38;5;251m", "\033[38;5;249m", "\033[38;5;247m"],
    "木": ["\033[38;5;46m",  "\033[38;5;40m",  "\033[38;5;34m",  "\033[38;5;28m",  "\033[38;5;22m"],
    "水": ["\033[38;5;51m",  "\033[38;5;45m",  "\033[38;5;39m",  "\033[38;5;33m",  "\033[38;5;27m"],
    "火": ["\033[38;5;196m", "\033[38;5;202m", "\033[38;5;208m", "\033[38;5;214m", "\033[38;5;220m"],
    "土": ["\033[38;5;226m", "\033[38;5;220m", "\033[38;5;214m", "\033[38;5;178m", "\033[38;5;136m"],
}

RESET = "\033[0m"
CLEAR_LINE = "\033[2K\r"

# 五行顺序（相生：木→火→土→金→水→木）
WUXING_ORDER = ["木", "火", "土", "金", "水"]

# ============================================================
# 不动点缓存：预计算颜色序列
# ============================================================

@lru_cache(maxsize=1)
def _precompute_marquee_frames(text: str, width: int = 60) -> Tuple[str, ...]:
    """
    预计算所有跑马灯帧（不动点）
    一次计算，无限复用，零运行时开销
    """
    frames = []
    padded = " " * width + text + " " * width
    total_len = len(padded)

    for i in range(total_len - width + 1):
        frame_chars = []
        visible = padded[i:i+width]
        for j, char in enumerate(visible):
            # 五行循环着色
            wx_idx = (i + j) % 5
            wx = WUXING_ORDER[wx_idx]
            color = WUXING_COLORS_BOLD[wx]
            frame_chars.append(f"{color}{char}{RESET}")
        frames.append("".join(frame_chars))

    return tuple(frames)


@lru_cache(maxsize=1)
def _precompute_breathing_frames(text: str) -> Tuple[str, ...]:
    """
    预计算呼吸灯效果帧（五行渐变）
    """
    frames = []
    # 每个五行走一遍渐变（5色 × 5级 = 25帧）
    for wx in WUXING_ORDER:
        gradient = WUXING_GRADIENT[wx]
        for color in gradient:
            frames.append(f"{color}{text}{RESET}")
        for color in reversed(gradient):
            frames.append(f"{color}{text}{RESET}")
    return tuple(frames)


@lru_cache(maxsize=5)
def _precompute_sparkle_line(length: int) -> Tuple[str, ...]:
    """
    预计算闪烁分隔线
    """
    frames = []
    chars = "═══════════════════════════════════════════════════════════"[:length]
    for offset in range(5):
        line = []
        for i, c in enumerate(chars):
            wx = WUXING_ORDER[(i + offset) % 5]
            line.append(f"{WUXING_COLORS_BOLD[wx]}{c}{RESET}")
        frames.append("".join(line))
    return tuple(frames)


# ============================================================
# 跑马灯播放器
# ============================================================

class WucaiMarquee:
    """
    五彩跑马灯播放器
    初始化时预计算所有帧，播放时零开销
    """

    def __init__(self, text: str = "龍魂系统 · UID9622 · 守此立此 · 永不背弃", width: int = 50):
        self.text = text
        self.width = width
        self.frames = _precompute_marquee_frames(text, width)
        self.breathing = _precompute_breathing_frames(text)
        self.sparkle = _precompute_sparkle_line(width)
        self.frame_idx = 0
        self.breath_idx = 0
        self.sparkle_idx = 0

    def next_frame(self) -> str:
        """获取下一帧（跑马灯）"""
        frame = self.frames[self.frame_idx]
        self.frame_idx = (self.frame_idx + 1) % len(self.frames)
        return frame

    def next_breath(self) -> str:
        """获取下一帧（呼吸灯）"""
        frame = self.breathing[self.breath_idx]
        self.breath_idx = (self.breath_idx + 1) % len(self.breathing)
        return frame

    def next_sparkle(self) -> str:
        """获取下一帧（闪烁线）"""
        frame = self.sparkle[self.sparkle_idx]
        self.sparkle_idx = (self.sparkle_idx + 1) % len(self.sparkle)
        return frame

    def play(self, mode: str = "marquee", duration: float = 10.0, fps: float = 15.0):
        """
        播放动画
        mode: marquee（跑马灯）| breath（呼吸灯）| sparkle（闪烁线）| combo（组合）
        """
        interval = 1.0 / fps
        start = time.time()

        try:
            while time.time() - start < duration:
                if mode == "marquee":
                    sys.stdout.write(f"{CLEAR_LINE}{self.next_frame()}")
                elif mode == "breath":
                    sys.stdout.write(f"{CLEAR_LINE}{self.next_breath()}")
                elif mode == "sparkle":
                    sys.stdout.write(f"{CLEAR_LINE}{self.next_sparkle()}")
                elif mode == "combo":
                    sys.stdout.write(f"{CLEAR_LINE}{self.next_sparkle()}\n")
                    sys.stdout.write(f"{CLEAR_LINE}{self.next_frame()}\n")
                    sys.stdout.write(f"{CLEAR_LINE}{self.next_sparkle()}")
                    sys.stdout.write("\033[2A")  # 上移两行
                sys.stdout.flush()
                time.sleep(interval)
        except KeyboardInterrupt:
            pass
        finally:
            sys.stdout.write(f"{CLEAR_LINE}")
            sys.stdout.flush()


# ============================================================
# 静态彩色输出（不动画，但带五行色）
# ============================================================

def wucai_print(text: str, wuxing: str = None):
    """
    五彩打印（静态）
    wuxing: 指定五行色，None则按字符位置循环
    """
    if wuxing and wuxing in WUXING_COLORS:
        print(f"{WUXING_COLORS_BOLD[wuxing]}{text}{RESET}")
    else:
        colored = []
        for i, char in enumerate(text):
            wx = WUXING_ORDER[i % 5]
            colored.append(f"{WUXING_COLORS_BOLD[wx]}{char}{RESET}")
        print("".join(colored))


def wucai_banner(title: str = "龍魂系统"):
    """打印五彩横幅"""
    width = 60
    line = _precompute_sparkle_line(width)[0]
    print(line)
    wucai_print(f"  {title}".center(width))
    print(line)


def wucai_status(items: List[Tuple[str, str, str]]):
    """
    打印五彩状态表
    items: [(名称, 状态, 五行), ...]
    """
    for name, status, wx in items:
        color = WUXING_COLORS_BOLD.get(wx, RESET)
        print(f"  {color}●{RESET} {name}: {color}{status}{RESET}")


# ============================================================
# DNA 戳生成（带五彩）
# ============================================================

def wucai_dna(tag: str) -> str:
    """生成五彩 DNA 戳"""
    import hashlib
    from datetime import datetime
    date = datetime.now().strftime("%Y-%m-%d")
    h = hashlib.sha256(f"{tag}{time.time()}".encode()).hexdigest()[:6].upper()
    dna = f"#龍芯⚡️{date}-{tag}-v1.0-{h}"
    return dna


def print_wucai_dna(tag: str):
    """打印五彩 DNA"""
    dna = wucai_dna(tag)
    wucai_print(dna)


# ============================================================
# 主入口（演示）
# ============================================================

if __name__ == "__main__":
    print()
    wucai_banner("龍魂五彩跑马灯 v1.0")
    print()

    # 状态演示
    wucai_status([
        ("本地 Ollama", "🟢 在线", "木"),
        ("Gateway", "🟢 运行中", "火"),
        ("隧道", "🟢 已连接", "水"),
        ("cnsh-reactor", "🟢 就绪", "金"),
        ("审计系统", "🟢 正常", "土"),
    ])
    print()

    # DNA 演示
    print("DNA 戳：", end="")
    print_wucai_dna("MARQUEE-DEMO")
    print()

    # 跑马灯演示
    print("跑马灯演示（5秒）：")
    marquee = WucaiMarquee("☰ 龍魂系统 · UID9622 · 守此立此 · 永不背弃 · 留痕即正义 ☷")
    marquee.play(mode="marquee", duration=5.0, fps=12)
    print()

    print("\n呼吸灯演示（3秒）：")
    marquee.play(mode="breath", duration=3.0, fps=10)
    print()

    wucai_banner("演示完成")
    print()
