# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""Desktop 渲染适配器 · PyAutoGUI + cv2（macOS/Linux/Windows）。"""

import io
import platform
import subprocess

from ..core.variables import RenderContext


class DesktopAdapter:
    """桌面应用渲染适配器。"""

    SUPPORTED_PLATFORMS = ["macos", "linux", "windows"]

    def __init__(self):
        self.os = platform.system()  # Darwin / Linux / Windows

    # ── 截图 ──

    def screenshot(self, region: list = None) -> bytes:
        import pyautogui
        img = pyautogui.screenshot(region=region and tuple(region) or None)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

    # ── 窗口 ──

    def find_window(self, title: str) -> dict:
        if self.os == "Darwin":
            script = (
                'tell application "System Events"\n'
                f'set wins to (name of every window of every process whose name contains "{title}")\n'
                "return wins\nend tell"
            )
            r = subprocess.run(["osascript", "-e", script],
                               capture_output=True, text=True)
            return {"found": bool(r.stdout.strip()), "windows": r.stdout.strip()}
        if self.os == "Linux":
            r = subprocess.run(["xdotool", "search", "--name", title],
                               capture_output=True, text=True)
            return {"found": bool(r.stdout.strip()), "window_id": r.stdout.strip()}
        return {"found": False, "reason": f"{self.os} 暂不支持窗口查找"}

    def get_active_window_title(self) -> str:
        if self.os == "Darwin":
            script = ('tell application "System Events" to get name of first '
                      'application process whose frontmost is true')
            r = subprocess.run(["osascript", "-e", script],
                               capture_output=True, text=True)
            return r.stdout.strip()
        if self.os == "Linux":
            r = subprocess.run(["xdotool", "getactivewindow", "getwindowname"],
                               capture_output=True, text=True)
            return r.stdout.strip()
        return ""

    # ── 交互 ──

    def click(self, x: int, y: int, double: bool = False, right: bool = False):
        import pyautogui
        if double:
            pyautogui.doubleClick(x, y)
        elif right:
            pyautogui.rightClick(x, y)
        else:
            pyautogui.click(x, y)

    def type_text(self, text: str, interval: float = 0.05):
        import pyautogui
        pyautogui.typewrite(text, interval=interval)

    def keypress(self, key: str):
        import pyautogui
        pyautogui.press(key)

    def scroll(self, direction: str = "下", distance: int = 500):
        import pyautogui
        pyautogui.scroll(-distance if direction == "下" else distance)

    def capture_context(self, url: str = "") -> RenderContext:
        ctx = RenderContext(platform="desktop", url=url or "desktop://local")
        try:
            ctx.screenshot = self.screenshot()
        except ImportError:
            ctx.error = "pyautogui 未安装"
        ctx.title = self.get_active_window_title()
        return ctx

    # ── 视觉匹配 ──

    def visual_match(self, template_path: str, threshold: float = 0.8) -> dict:
        import cv2
        import numpy as np
        nparr = np.frombuffer(self.screenshot(), np.uint8)
        screen = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        template = cv2.imread(template_path)
        if template is None:
            return {"found": False, "error": f"模板不存在: {template_path}"}
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if float(max_val) >= threshold:
            h, w = template.shape[:2]
            return {"found": True, "x": int(max_loc[0]), "y": int(max_loc[1]),
                    "w": int(w), "h": int(h), "score": round(float(max_val), 4),
                    "center": [int(max_loc[0] + w // 2), int(max_loc[1] + h // 2)]}
        return {"found": False, "score": round(float(max_val), 4)}
