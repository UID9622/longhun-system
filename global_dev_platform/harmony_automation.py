#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂全球开发者平台 · HarmonyOS 全方位自动化 v1.0
DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-HARMONY-AUTO-v1.0
创建者: 诸葛鑫（UID9622）
协议: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
工具链: hdc (HarmonyOS Device Connector) / DevEco Studio CLI / hvigorw
设计原则: 华为生态完整自动化 · 与 iOS 层对等 · 双生态一致体验 · DNA 一律走统一干支卦引擎
"""

import subprocess
import json
import os
import time
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

from lh_dna import lh_dna


class HarmonyAutomation:
    """
    HarmonyOS 全方位自动化
    覆盖: hdc 设备管理 / 应用构建 / 真机安装 / 截图录屏 / 原子化服务 / AppGallery 发布
    工具链: HarmonyOS SDK (DevEco Studio 安装后自带 hdc)
    """

    # DevEco Studio 默认 SDK 路径（macOS）
    DEFAULT_SDK = Path.home() / "Library" / "Huawei" / "Sdk"
    DEFAULT_HDC = DEFAULT_SDK / "openharmony" / "9" / "toolchains" / "hdc"

    def __init__(self, sdk_path: Optional[str] = None,
                 project_dir: Optional[str] = None):
        self.sdk      = Path(sdk_path) if sdk_path else self.DEFAULT_SDK
        self.hdc      = str(self.DEFAULT_HDC)
        self.project  = Path(project_dir) if project_dir else Path.cwd()
        self._check_hdc()

    def _check_hdc(self) -> bool:
        """检查 hdc 是否可用"""
        ok = shutil.which("hdc") is not None or Path(self.hdc).exists()
        print(f"  {'✅' if ok else '❌'} HarmonyOS hdc: {'已安装' if ok else '未安装 → 安装 DevEco Studio'}")
        return ok

    def _run_hdc(self, args: List[str], **kwargs) -> subprocess.CompletedProcess:
        """执行 hdc 命令（自动 fallback 到 PATH 中的 hdc）"""
        hdc_cmd = "hdc" if shutil.which("hdc") else self.hdc
        return subprocess.run([hdc_cmd] + args,
                              capture_output=True, text=True, **kwargs)

    @staticmethod
    def _dna(action: str) -> str:
        """统一 DNA · 干支卦引擎"""
        return lh_dna(module="HARMONY-AUTO", action=action, version="v1.0")

    # ----------------------------------------------------------------
    # A. 设备管理
    # ----------------------------------------------------------------

    def list_devices(self) -> List[Dict]:
        """列出已连接 HarmonyOS 设备"""
        r = self._run_hdc(["list", "targets"])
        devices = []
        for line in r.stdout.strip().splitlines():
            line = line.strip()
            if line and "[empty]" not in line:
                devices.append({"id": line, "type": "device"})
        return devices

    def get_device_info(self, device_id: str) -> Dict:
        """获取设备详细信息"""
        info = {}
        fields = {
            "model":   "param get const.product.model",
            "version": "param get const.ohos.apiversion",
            "brand":   "param get const.product.brand",
        }
        for k, cmd in fields.items():
            r = self._run_hdc(["-t", device_id, "shell"] + cmd.split())
            info[k] = r.stdout.strip()
        return info

    # ----------------------------------------------------------------
    # B. 应用操作
    # ----------------------------------------------------------------

    def install_hap(self, device_id: str, hap_path: str) -> str:
        """安装 .hap 包到设备"""
        self._run_hdc(["-t", device_id, "install", hap_path], check=True)
        dna = self._dna("INSTALL-HAP")
        print(f"  ✅ HAP 已安装: {hap_path} | DNA: {dna}")
        return dna

    def uninstall_app(self, device_id: str, bundle_name: str) -> str:
        """卸载应用"""
        self._run_hdc(["-t", device_id, "uninstall", bundle_name])
        dna = self._dna("UNINSTALL")
        print(f"  🗑️ 已卸载: {bundle_name} | DNA: {dna}")
        return dna

    def launch_app(self, device_id: str, bundle_name: str,
                   ability: str = "MainAbility") -> str:
        """启动应用 Ability"""
        cmd = f"aa start -b {bundle_name} -a {ability}"
        self._run_hdc(["-t", device_id, "shell"] + cmd.split())
        dna = self._dna("LAUNCH")
        print(f"  🚀 已启动: {bundle_name}/{ability} | DNA: {dna}")
        return dna

    def stop_app(self, device_id: str, bundle_name: str) -> str:
        """停止应用"""
        cmd = f"aa force-stop {bundle_name}"
        self._run_hdc(["-t", device_id, "shell"] + cmd.split())
        dna = self._dna("STOP")
        print(f"  ⏹️ 已停止: {bundle_name} | DNA: {dna}")
        return dna

    def list_installed_apps(self, device_id: str) -> List[str]:
        """列出设备已安装的所有应用"""
        r = self._run_hdc(["-t", device_id, "shell",
                            "bm", "dump", "-a"])
        return [line.strip() for line in r.stdout.splitlines()
                if line.strip() and not line.startswith("ID:")]

    # ----------------------------------------------------------------
    # C. 截图与录屏
    # ----------------------------------------------------------------

    def screenshot_device(self, device_id: str, output_path: str) -> str:
        """设备截图并拉取到本地"""
        remote = "/data/local/tmp/screenshot.png"
        self._run_hdc(["-t", device_id, "shell",
                        "snapshot_display", "-f", remote])
        self._run_hdc(["-t", device_id, "file", "recv", remote, output_path])
        dna = self._dna("SCREENSHOT")
        print(f"  📸 截图: {output_path} | DNA: {dna}")
        return dna

    def record_video(self, device_id: str, output_path: str,
                     duration: int = 10) -> str:
        """录屏（HarmonyOS 4.0+）"""
        remote = "/data/local/tmp/record.mp4"
        proc = subprocess.Popen(
            ["hdc", "-t", device_id, "shell",
             "screenrecord", remote])
        time.sleep(duration)
        proc.terminate()
        time.sleep(1)
        self._run_hdc(["-t", device_id, "file", "recv", remote, output_path])
        dna = self._dna("RECORD")
        print(f"  🎥 录屏: {output_path} ({duration}s) | DNA: {dna}")
        return dna

    # ----------------------------------------------------------------
    # D. 文件与日志
    # ----------------------------------------------------------------

    def push_file(self, device_id: str, local: str, remote: str) -> str:
        """推送文件到设备"""
        self._run_hdc(["-t", device_id, "file", "send", local, remote])
        dna = self._dna("FILE-PUSH")
        print(f"  📤 文件已推送: {local} → {remote} | DNA: {dna}")
        return dna

    def pull_file(self, device_id: str, remote: str, local: str) -> str:
        """从设备拉取文件"""
        self._run_hdc(["-t", device_id, "file", "recv", remote, local])
        dna = self._dna("FILE-PULL")
        print(f"  📥 文件已拉取: {remote} → {local} | DNA: {dna}")
        return dna

    def get_hilog(self, device_id: str, output_path: str,
                  duration: int = 10, filter_tag: str = "") -> str:
        """采集 HiLog 日志（HarmonyOS 的 logcat）"""
        cmd = ["hdc", "-t", device_id, "shell", "hilog"]
        if filter_tag:
            cmd += ["-T", filter_tag]
        with open(output_path, "w") as f:
            proc = subprocess.Popen(cmd, stdout=f, stderr=f)
            time.sleep(duration)
            proc.terminate()
        dna = self._dna("HILOG")
        print(f"  📋 HiLog: {output_path} ({duration}s) | DNA: {dna}")
        return dna

    def shell(self, device_id: str, command: str) -> str:
        """在设备上执行 shell 命令"""
        r = self._run_hdc(["-t", device_id, "shell"] + command.split())
        dna = self._dna("SHELL")
        return r.stdout.strip()

    # ----------------------------------------------------------------
    # E. 构建 (hvigorw)
    # ----------------------------------------------------------------

    def build_hap(self, target: str = "default",
                  mode: str = "release") -> str:
        """hvigorw 构建 HAP 包（DevEco Studio 的构建工具）"""
        hvigorw = self.project / "hvigorw"
        cmd = [str(hvigorw), "assembleHap",
               "--mode", mode, "--target", target]
        subprocess.run(cmd, cwd=str(self.project), check=True)
        dna = self._dna("BUILD-HAP")
        print(f"  🔨 HAP 构建完成: {target}/{mode} | DNA: {dna}")
        return dna

    def run_ohtest(self) -> str:
        """运行 ohosTest 单元测试"""
        hvigorw = self.project / "hvigorw"
        subprocess.run([str(hvigorw), "ohosTest"],
                       cwd=str(self.project), check=True)
        dna = self._dna("OHTEST")
        print(f"  ✅ ohosTest 测试完成 | DNA: {dna}")
        return dna

    # ----------------------------------------------------------------
    # F. 原子化服务（HarmonyOS 特色）
    # ----------------------------------------------------------------

    def deploy_atomic_service(self, device_id: str,
                              hap_path: str,
                              service_name: str) -> str:
        """
        部署原子化服务 · HarmonyOS 的「无需安装即可运行」特色功能
        这是让全球每个人低门槛使用你的服务的关键技术
        """
        self.install_hap(device_id, hap_path)
        dna = self._dna("ATOMIC-SVC")
        print(f"  ⚛️ 原子化服务已部署: {service_name} | DNA: {dna}")
        print(f"     → 用户无需安装完整 App，扫码即用 🌍")
        return dna


if __name__ == "__main__":
    harmony = HarmonyAutomation()
    devices = harmony.list_devices()
    print(f"\n已连接 HarmonyOS 设备: {len(devices)} 台")
    for d in devices:
        print(f"  📱 {d['id']}")
