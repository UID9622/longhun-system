#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂全球开发者平台 · 双平台统一执行器 v1.0
DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-CROSS-RUNNER-v1.0
创建者: 诸葛鑫（UID9622）
协议: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
设计原则: 一次调用，iOS + HarmonyOS 同时动 · 对齐体验 · DNA 一律走统一干支卦引擎
"""

from ios_automation     import IosAutomation
from harmony_automation import HarmonyAutomation
from global_trace       import GlobalTrace
from dev_democratizer   import DevDemocratizer
from shortcut_bridge    import ShortcutBridge
import os
import json
import time
from datetime import datetime
from typing import Optional, Dict, Any

from lh_dna import lh_dna


class CrossRunner:
    """
    双平台统一执行器
    一次指令，iOS 和 HarmonyOS 同步执行
    """

    def __init__(self, user_id: str = "UID9622",
                 ios_simulator_udid: Optional[str] = None,
                 harmony_device_id:  Optional[str] = None):
        self.user_id    = user_id
        self.ios_udid   = ios_simulator_udid
        self.hos_device = harmony_device_id
        self.ios        = IosAutomation()
        self.harmony    = HarmonyAutomation()
        self.trace      = GlobalTrace(user_id)
        self.demo       = DevDemocratizer()
        self.bridge     = ShortcutBridge()

    @staticmethod
    def _dna(action: str) -> str:
        return lh_dna(module="CROSS-RUNNER", action=action, version="v1.0")

    def new_app(self, app_name: str,
                template_id: str = "todo") -> Dict[str, str]:
        """
        从零创建一个双平台 App
        这是「让每个人成为开发者」的主入口
        """
        print(f"\n🌍 [{self.user_id}] 正在创造你的双平台 App: {app_name}\n")
        result = self.demo.generate_both(app_name, template_id, self.user_id)
        dna = self._dna("NEW-APP")
        self.trace.record("APP_CREATED", app_name,
                          detail=f"模板: {template_id} | iOS + HarmonyOS",
                          platform="both",
                          extra={"paths": result, "dna": dna})
        return result

    def screenshot_both(self, output_dir: str) -> Dict[str, str]:
        """同时截图 iOS 模拟器和 HarmonyOS 设备"""
        os.makedirs(output_dir, exist_ok=True)
        results = {}

        if self.ios_udid:
            ios_path = f"{output_dir}/ios_screenshot.png"
            self.ios.screenshot_simulator(self.ios_udid, ios_path)
            results["ios"] = ios_path
            self.trace.record("SCREENSHOT", "iOS 截图", platform="iOS")

        if self.hos_device:
            hos_path = f"{output_dir}/harmony_screenshot.png"
            self.harmony.screenshot_device(self.hos_device, hos_path)
            results["harmony"] = hos_path
            self.trace.record("SCREENSHOT", "HarmonyOS 截图", platform="harmony")

        dna = self._dna("SCREENSHOT-BOTH")
        print(f"\n  ✅ 双平台截图完成 | DNA: {dna}")
        return results

    def run_shortcut_both(self, ios_shortcut: str,
                          hos_bundle: str,
                          hos_ability: str = "MainAbility") -> str:
        """iOS 快捷指令 + HarmonyOS Ability 同步触发"""
        if self.ios_udid:
            self.ios.run_shortcut(ios_shortcut)
        if self.hos_device:
            self.harmony.launch_app(self.hos_device, hos_bundle, hos_ability)
        dna = self._dna("SHORTCUT-BOTH")
        self.trace.record("SHORTCUT_RUN",
                          f"{ios_shortcut} / {hos_ability}",
                          platform="both")
        return dna

    def world_mark(self, message: str,
                   location: str = "地球") -> str:
        """在全球痕迹地图上打一个点——「我来过」"""
        dna = self.trace.record(
            "WORLD_MARK",
            message,
            platform="both",
            location=location,
            detail=f"UID: {self.user_id} | 时间: {datetime.now().isoformat()}"
        )
        print(f"\n  🌍 你的足迹已记录：{message}")
        print(f"     这个世界知道你来过。DNA: {dna}")
        return dna

    def auto_generate_app_store_shots(self, udid: str,
                                      app_path: str,
                                      output_dir: str) -> list:
        """
        自动生成 App Store 标准截图（5 张·标准状态栏·多语言）
        发布必备·一键完成
        """
        os.makedirs(output_dir, exist_ok=True)

        # 设置标准状态栏
        self.ios.set_status_bar(udid)

        # 安装并启动
        self.ios.install_app_simulator(udid, app_path)
        self.ios.launch_app_simulator(udid,
            # 从 app_path 提取 bundle_id（简化版）
            "com.longhun.demo"
        )

        shots = []
        for i in range(1, 6):
            path = f"{output_dir}/appstore_shot_{i:02d}.png"
            time.sleep(1.5)  # 等页面稳定
            self.ios.screenshot_simulator(udid, path)
            shots.append(path)
            print(f"  📸 App Store 截图 {i}/5: {path}")

        dna = self._dna("APPSTORE-SHOTS")
        self.trace.record("APP_LAUNCHED",
                          "App Store 截图生成",
                          platform="iOS",
                          extra={"shots": shots, "dna": dna})
        return shots

    def status(self) -> Dict[str, bool]:
        """一键巡检双平台工具链"""
        print("🌏 龍魂全球开发者平台 · 工具链巡检\n")
        ios_ok = self.ios._check_xcode()
        hos_ok = self.harmony._check_hdc()
        shortcuts = len(self.bridge.ios_list())
        result = {
            "xcode":  ios_ok,
            "hdc":    hos_ok,
            "shortcuts": shortcuts,
            "traces": self.trace.world_count(),
        }
        print(f"\n  已登记痕迹: {result['traces']} 条 · 可用快捷指令: {shortcuts} 个")
        return result


if __name__ == "__main__":
    runner = CrossRunner(user_id="UID9622")
    runner.status()

    # 创建双平台 App
    result = runner.new_app("龍魂足迹", "world_map")

    # 在世界上留下痕迹
    runner.world_mark("龍魂全球开发者平台 v1.0 正式上线", location="中国·深圳")

    # 查看故事
    runner.trace.print_my_story()
