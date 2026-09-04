# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""iOS 渲染适配器 · XCUITest + Simulator（需 Xcode 环境）。"""

import subprocess
import time

from ..core.variables import RenderContext


class IOSAdapter:
    """iOS App 渲染适配器（模拟器）。"""

    SUPPORTED_PLATFORMS = ["ios"]

    def __init__(self, simulator_udid: str = None, bundle_id: str = None):
        self.udid = simulator_udid or self._auto_simulator()
        self.bundle_id = bundle_id

    def _auto_simulator(self) -> str:
        try:
            r = subprocess.run(
                ["xcrun", "simctl", "list", "devices", "booted"],
                capture_output=True, text=True, timeout=20,
            )
            for line in r.stdout.splitlines():
                if "(" in line and ")" in line and "Booted" in line:
                    return line.split("(")[1].split(")")[0]
            return ""
        except FileNotFoundError:
            return ""

    def boot(self):
        if self.udid:
            subprocess.run(["xcrun", "simctl", "boot", self.udid],
                           capture_output=True, timeout=30)

    def launch_app(self, bundle_id: str = None) -> RenderContext:
        bid = bundle_id or self.bundle_id
        if not (self.udid and bid):
            raise RuntimeError("iOS 渲染需要模拟器 UDID 和 bundle_id")
        subprocess.run(["xcrun", "simctl", "launch", self.udid, bid],
                       capture_output=True, timeout=30)
        time.sleep(3)
        ctx = RenderContext(platform="ios", url=f"ios://{bid}")
        try:
            ctx.screenshot = self.screenshot()
        except Exception as e:
            ctx.error = str(e)
        return ctx

    def screenshot(self, local_path: str = "/tmp/ios_render.png") -> bytes:
        subprocess.run(["xcrun", "simctl", "io", self.udid, "screenshot", local_path],
                       capture_output=True, timeout=30)
        with open(local_path, "rb") as f:
            return f.read()

    def tap(self, x: int, y: int):
        # 通过 simctl ui 无法直接点击，需 XCUITest runner；这里留接口
        raise NotImplementedError("iOS 点击需 XCUITest runner，请配置后调用")
