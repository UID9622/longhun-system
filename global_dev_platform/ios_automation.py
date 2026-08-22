#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂全球开发者平台 · iOS 全方位自动化 v1.0
DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-IOS-AUTO-v1.0
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
工具链: xcrun simctl / xcodebuild / ideviceinstaller / fastlane
设计原则: 每个操作都留 DNA · 让任何人都能一键触发 iOS 动作 · DNA 一律走统一干支卦引擎
"""

import subprocess
import json
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

from lh_dna import lh_dna


class IosAutomation:
    """
    iOS 全方位自动化
    覆盖: 模拟器管理 / 真机操作 / 应用构建 / 截图录制 / 快捷指令 / 发布
    全部依赖 Xcode 命令行工具（macOS 原生）
    """

    def __init__(self, project_dir: Optional[str] = None):
        self.project_dir = Path(project_dir) if project_dir else Path.cwd()
        self._check_xcode()

    @staticmethod
    def _check_xcode() -> bool:
        """检查 Xcode 命令行工具是否已安装"""
        r = subprocess.run(["xcrun", "--version"],
                           capture_output=True, text=True)
        ok = r.returncode == 0
        print(f"  {'✅' if ok else '❌'} Xcode CLI: {'已安装' if ok else '未安装 → xcode-select --install'}")
        return ok

    @staticmethod
    def _dna(action: str) -> str:
        """统一 DNA · 干支卦引擎"""
        return lh_dna(module="IOS-AUTO", action=action, version="v1.0")

    # ----------------------------------------------------------------
    # A. 模拟器管理
    # ----------------------------------------------------------------

    def list_simulators(self) -> List[Dict]:
        """列出所有可用 iOS 模拟器"""
        r = subprocess.run(
            ["xcrun", "simctl", "list", "devices", "--json"],
            capture_output=True, text=True, check=True)
        data = json.loads(r.stdout)
        devices = []
        for runtime, devs in data["devices"].items():
            if "iOS" in runtime:
                for d in devs:
                    if d["isAvailable"]:
                        devices.append({
                            "udid":    d["udid"],
                            "name":    d["name"],
                            "state":   d["state"],
                            "runtime": runtime.split(".")[-1].replace("-", "."),
                        })
        return devices

    def boot_simulator(self, udid: str) -> str:
        """启动指定模拟器"""
        subprocess.run(["xcrun", "simctl", "boot", udid], check=True)
        subprocess.run(["open", "-a", "Simulator"])
        dna = self._dna("BOOT")
        print(f"  ✅ 模拟器已启动: {udid} | DNA: {dna}")
        return dna

    def shutdown_simulator(self, udid: str) -> None:
        """关闭模拟器"""
        subprocess.run(["xcrun", "simctl", "shutdown", udid])

    def install_app_simulator(self, udid: str, app_path: str) -> str:
        """向模拟器安装 .app 包"""
        subprocess.run(["xcrun", "simctl", "install", udid, app_path], check=True)
        dna = self._dna("INSTALL-SIM")
        print(f"  ✅ 应用已安装到模拟器 | DNA: {dna}")
        return dna

    def launch_app_simulator(self, udid: str, bundle_id: str) -> str:
        """在模拟器中启动应用"""
        subprocess.run(["xcrun", "simctl", "launch", udid, bundle_id], check=True)
        dna = self._dna("LAUNCH-SIM")
        print(f"  ✅ 应用已启动: {bundle_id} | DNA: {dna}")
        return dna

    def screenshot_simulator(self, udid: str, output_path: str) -> str:
        """模拟器截图"""
        subprocess.run(
            ["xcrun", "simctl", "io", udid, "screenshot", output_path],
            check=True)
        dna = self._dna("SCREENSHOT-SIM")
        print(f"  📸 截图保存: {output_path} | DNA: {dna}")
        return dna

    def record_video_simulator(self, udid: str, output_path: str,
                               duration: int = 10) -> str:
        """模拟器录制视频（后台录制 duration 秒后停止）"""
        proc = subprocess.Popen(
            ["xcrun", "simctl", "io", udid, "recordVideo", output_path])
        time.sleep(duration)
        proc.terminate()
        dna = self._dna("RECORD-SIM")
        print(f"  🎥 录屏完成: {output_path} ({duration}s) | DNA: {dna}")
        return dna

    def push_notification_simulator(self, udid: str, bundle_id: str,
                                    title: str, body: str) -> str:
        """向模拟器推送本地通知"""
        payload = {
            "Simulator Target Bundle": bundle_id,
            "aps": {
                "alert": {"title": title, "body": body},
                "sound": "default"
            }
        }
        tmp = Path("/tmp") / f"notif_{int(time.time())}.apns"
        tmp.write_text(json.dumps(payload), "utf-8")
        subprocess.run(
            ["xcrun", "simctl", "push", udid, bundle_id, str(tmp)],
            check=True)
        tmp.unlink()
        dna = self._dna("PUSH-NOTIF")
        print(f"  🔔 通知已推送: {title} | DNA: {dna}")
        return dna

    def set_status_bar(self, udid: str,
                       time_str: str = "09:41",
                       battery: int = 100,
                       wifi_bars: int = 3) -> str:
        """设置模拟器状态栏（标准发布截图必备）"""
        subprocess.run([
            "xcrun", "simctl", "status_bar", udid, "override",
            "--time",        time_str,
            "--batteryLevel", str(battery),
            "--batteryState", "charged",
            "--wifiBars",     str(wifi_bars),
        ], check=True)
        dna = self._dna("STATUS-BAR")
        print(f"  ✅ 状态栏已设置 09:41·100%·WiFi3格 | DNA: {dna}")
        return dna

    def open_url_simulator(self, udid: str, url: str) -> str:
        """在模拟器中打开 URL（包括 deeplink）"""
        subprocess.run(["xcrun", "simctl", "openurl", udid, url], check=True)
        dna = self._dna("OPEN-URL")
        print(f"  🔗 URL 已打开: {url} | DNA: {dna}")
        return dna

    def add_media_simulator(self, udid: str, file_path: str) -> str:
        """向模拟器相册添加图片/视频"""
        subprocess.run(["xcrun", "simctl", "addmedia", udid, file_path],
                       check=True)
        dna = self._dna("ADD-MEDIA")
        print(f"  🖼️ 媒体已添加: {file_path} | DNA: {dna}")
        return dna

    def erase_simulator(self, udid: str) -> str:
        """抹除模拟器（回到出厂状态，自动化测试前必须）"""
        subprocess.run(["xcrun", "simctl", "erase", udid], check=True)
        dna = self._dna("ERASE")
        print(f"  🗑️ 模拟器已抹除 | DNA: {dna}")
        return dna

    # ----------------------------------------------------------------
    # B. 真机操作（需要 libimobiledevice: brew install libimobiledevice）
    # ----------------------------------------------------------------

    def list_real_devices(self) -> List[str]:
        """列出已连接真机 UDID"""
        try:
            r = subprocess.run(["idevice_id", "-l"],
                               capture_output=True, text=True)
            return [u.strip() for u in r.stdout.strip().splitlines() if u.strip()]
        except FileNotFoundError:
            print("  ⚠️  libimobiledevice 未安装 → brew install libimobiledevice")
            return []

    def install_app_device(self, ipa_path: str) -> str:
        """向真机安装 .ipa"""
        subprocess.run(["ideviceinstaller", "-i", ipa_path], check=True)
        dna = self._dna("INSTALL-DEVICE")
        print(f"  ✅ 已安装到真机 | DNA: {dna}")
        return dna

    def screenshot_device(self, output_path: str) -> str:
        """真机截图"""
        subprocess.run(["idevicescreenshot", output_path], check=True)
        dna = self._dna("SCREENSHOT-DEVICE")
        print(f"  📸 真机截图: {output_path} | DNA: {dna}")
        return dna

    def device_syslog(self, output_path: str, duration: int = 10) -> str:
        """采集真机系统日志"""
        with open(output_path, "w") as f:
            proc = subprocess.Popen(["idevicesyslog"], stdout=f, stderr=f)
            time.sleep(duration)
            proc.terminate()
        dna = self._dna("SYSLOG")
        print(f"  📋 系统日志: {output_path} ({duration}s) | DNA: {dna}")
        return dna

    # ----------------------------------------------------------------
    # C. 构建与发布
    # ----------------------------------------------------------------

    def build_app(self, scheme: str, destination: str = "generic/platform=iOS",
                  configuration: str = "Release") -> str:
        """xcodebuild 构建 App"""
        cmd = [
            "xcodebuild", "build",
            "-scheme",        scheme,
            "-destination",   destination,
            "-configuration", configuration,
            "-derivedDataPath", str(self.project_dir / "build"),
        ]
        subprocess.run(cmd, cwd=str(self.project_dir), check=True)
        dna = self._dna("BUILD")
        print(f"  🔨 构建完成: {scheme} | DNA: {dna}")
        return dna

    def run_tests(self, scheme: str, udid: str) -> str:
        """xctest 在指定模拟器上跑测试"""
        cmd = [
            "xcodebuild", "test",
            "-scheme",      scheme,
            "-destination", f"id={udid}",
        ]
        subprocess.run(cmd, cwd=str(self.project_dir), check=True)
        dna = self._dna("TEST")
        print(f"  ✅ 测试通过: {scheme} | DNA: {dna}")
        return dna

    def export_ipa(self, archive_path: str, export_options_plist: str,
                   output_dir: str) -> str:
        """从 .xcarchive 导出 IPA"""
        cmd = [
            "xcodebuild", "-exportArchive",
            "-archivePath",        archive_path,
            "-exportOptionsPlist", export_options_plist,
            "-exportPath",         output_dir,
        ]
        subprocess.run(cmd, check=True)
        dna = self._dna("EXPORT-IPA")
        print(f"  📦 IPA 已导出: {output_dir} | DNA: {dna}")
        return dna

    def upload_to_testflight(self, ipa_path: str,
                             apple_id: str,
                             password_env: str = "FASTLANE_PASSWORD") -> str:
        """通过 altool 上传到 TestFlight (Xcode 15+ 用 xcrun notarytool)"""
        cmd = [
            "xcrun", "altool", "--upload-app",
            "-f", ipa_path,
            "-t", "ios",
            "-u", apple_id,
            "-p", f"@env:{password_env}",
        ]
        subprocess.run(cmd, check=True)
        dna = self._dna("TESTFLIGHT-UPLOAD")
        print(f"  🚀 已上传到 TestFlight | DNA: {dna}")
        return dna

    # ----------------------------------------------------------------
    # D. iOS Shortcuts 自动化（通过 macOS shortcuts CLI）
    # ----------------------------------------------------------------

    def run_shortcut(self, shortcut_name: str,
                     input_text: Optional[str] = None) -> str:
        """运行 macOS/iOS 快捷指令（iCloud 同步到 iPhone）"""
        cmd = ["shortcuts", "run", shortcut_name]
        if input_text:
            proc = subprocess.run(
                cmd, input=input_text.encode(),
                capture_output=True)
        else:
            proc = subprocess.run(cmd, capture_output=True)
        dna = self._dna("SHORTCUT-RUN")
        print(f"  ⚡️ 快捷指令已执行: {shortcut_name} | DNA: {dna}")
        return dna

    def list_shortcuts(self) -> List[str]:
        """列出所有快捷指令"""
        r = subprocess.run(["shortcuts", "list"],
                           capture_output=True, text=True)
        return [s.strip() for s in r.stdout.strip().splitlines() if s.strip()]

    def create_shortcut_from_template(self, name: str,
                                      actions: List[str]) -> str:
        """生成简单快捷指令触发脚本（示范框架）"""
        template = {
            "name":    name,
            "actions": actions,
            "dna":     self._dna("SHORTCUT-CREATE"),
            "created": datetime.now().isoformat(),
        }
        p = Path.home() / "longhun-system" / "global_dev_platform" / "shortcuts" / f"{name}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(template, ensure_ascii=False, indent=2), "utf-8")
        print(f"  ⚡️ 快捷指令模板已生成: {name} | DNA: {template['dna']}")
        return str(p)

    def accessibility_audit_simulator(self, udid: str,
                                      bundle_id: str) -> str:
        """可访问性审计 · 让每个人都能用你的 App"""
        result = subprocess.run(
            ["xcrun", "simctl", "accessibility", udid, "audit", bundle_id],
            capture_output=True, text=True)
        report = result.stdout or result.stderr
        dna = self._dna("A11Y-AUDIT")
        print(f"  ♿ 可访问性审计完成 | DNA: {dna}")
        print(report[:500] if report else "（无报告输出）")
        return dna


if __name__ == "__main__":
    ios = IosAutomation()
    devices = ios.list_simulators()
    print(f"\n可用模拟器 ({len(devices)} 台):")
    for d in devices[:5]:
        print(f"  {d['name']} ({d['runtime']}) [{d['state']}]")
    shortcuts = ios.list_shortcuts()
    print(f"\n快捷指令 ({len(shortcuts)} 个):")
    for s in shortcuts[:10]:
        print(f"  ⚡️ {s}")
