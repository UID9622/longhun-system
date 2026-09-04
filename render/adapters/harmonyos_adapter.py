# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""HarmonyOS 渲染适配器 · hdc (鸿蒙设备控制器) + uitest。"""

import subprocess
import time

from ..core.variables import RenderContext


class HarmonyOSAdapter:
    """鸿蒙 App 渲染适配器。需要 hdc 已安装且设备已连接。"""

    SUPPORTED_PLATFORMS = ["harmonyos", "openharmony"]

    def __init__(self, device_id: str = None):
        self.device_id = device_id or self._auto_detect_device()

    def _auto_detect_device(self) -> str:
        try:
            r = subprocess.run(["hdc", "list", "targets"],
                               capture_output=True, text=True, timeout=10)
            lines = [l.strip() for l in r.stdout.splitlines() if l.strip()]
            return lines[0] if lines else None
        except FileNotFoundError:
            return None

    def _hdc(self, *args, timeout=30):
        if not self.device_id:
            raise RuntimeError("hdc 未连接任何鸿蒙设备")
        return subprocess.run(
            ["hdc", "-t", self.device_id, *args],
            capture_output=True, text=True, timeout=timeout,
        )

    def launch_app(self, bundle_id: str, ability: str = None) -> RenderContext:
        cmd = ["shell", "aa", "start", "-b", bundle_id]
        if ability:
            cmd += ["-a", ability]
        self._hdc(*cmd)
        time.sleep(2)
        ctx = RenderContext(platform="harmonyos", url=f"app://{bundle_id}")
        ctx.ax_tree = self.get_component_tree()
        try:
            ctx.screenshot = self.screenshot()
        except Exception as e:
            ctx.error = str(e)
        return ctx

    def screenshot(self, local_path: str = "/tmp/hos_render.png") -> bytes:
        self._hdc("shell", "snapshot_display", "-f", "/data/render_tmp.png")
        self._hdc("file", "recv", "/data/render_tmp.png", local_path)
        with open(local_path, "rb") as f:
            return f.read()

    def get_component_tree(self) -> dict:
        r = self._hdc("shell", "uitest", "dumpLayout")
        import json
        try:
            return json.loads(r.stdout) if r.stdout.strip() else {}
        except Exception:
            return {"raw": r.stdout[:2000]}

    def tap(self, x: int, y: int):
        self._hdc("shell", "uitest", "click", str(x), str(y))

    def input_text(self, text: str):
        self._hdc("shell", "uitest", "inputText", text)

    def swipe(self, x1: int, y1: int, x2: int, y2: int):
        self._hdc("shell", "uitest", "swipe", str(x1), str(y1), str(x2), str(y2))
