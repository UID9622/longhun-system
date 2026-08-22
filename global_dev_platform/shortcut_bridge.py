#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂全球开发者平台 · 快捷指令跨平台桥 v1.0
DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-SHORTCUT-BRIDGE-v1.0
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
设计原则:
  iOS Shortcuts（快捷指令）与 HarmonyOS 原子化服务之间的统一桥。
  一次编写，双端触发 · 让非开发者也能用「搭积木」方式自动化。
  DNA 一律走统一干支卦引擎。
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

from lh_dna import lh_dna

SHORTCUT_DIR = Path.home() / "longhun-system" / "global_dev_platform" / "shortcuts"


class ShortcutBridge:
    """
    快捷指令跨平台桥
    - iOS: macOS `shortcuts` CLI 触发（iCloud 同步到 iPhone）
    - HarmonyOS: 原子化服务意图（intent）模板
    - 统一清单: shortcuts/registry.json 双端登记
    """

    def __init__(self, registry_path: Optional[Path] = None):
        self.registry_path = Path(registry_path) if registry_path else SHORTCUT_DIR / "registry.json"
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self._load_registry()

    def _load_registry(self) -> None:
        """加载双端快捷指令登记表"""
        if self.registry_path.exists():
            try:
                self.registry = json.loads(self.registry_path.read_text("utf-8"))
            except json.JSONDecodeError:
                self.registry = {"items": []}
        else:
            self.registry = {"items": []}

    def _save_registry(self) -> None:
        """保存登记表"""
        self.registry_path.write_text(
            json.dumps(self.registry, ensure_ascii=False, indent=2), "utf-8")

    @staticmethod
    def _dna(action: str) -> str:
        return lh_dna(module="SHORTCUT-BRIDGE", action=action, version="v1.0")

    # ----------------------------------------------------------------
    # iOS 侧
    # ----------------------------------------------------------------

    def ios_list(self) -> List[str]:
        """列出本机可用快捷指令（macOS）"""
        try:
            r = subprocess.run(["shortcuts", "list"],
                               capture_output=True, text=True, timeout=15)
            return [s.strip() for s in r.stdout.strip().splitlines() if s.strip()]
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return []

    def ios_run(self, name: str, input_text: Optional[str] = None) -> str:
        """触发 iOS 快捷指令"""
        cmd = ["shortcuts", "run", name]
        if input_text:
            subprocess.run(cmd, input=input_text.encode(), capture_output=True, timeout=60)
        else:
            subprocess.run(cmd, capture_output=True, timeout=60)
        dna = self._dna("IOS-RUN")
        print(f"  ⚡️ iOS 快捷指令触发: {name} | DNA: {dna}")
        return dna

    # ----------------------------------------------------------------
    # HarmonyOS 侧（原子化服务意图）
    # ----------------------------------------------------------------

    def harmony_intent(self, name: str, bundle_name: str,
                       ability: str = "MainAbility",
                       params: Optional[Dict] = None) -> Dict:
        """
        登记一个 HarmonyOS 原子化服务意图
        对应华为「意图框架」(Intent Kit) 能力
        """
        dna = self._dna("HOS-INTENT")
        intent = {
            "name":        name,
            "bundle_name": bundle_name,
            "ability":     ability,
            "params":      params or {},
            "platform":    "harmony",
            "dna":         dna,
            "created":     datetime.now().isoformat(),
        }
        self.registry["items"].append(intent)
        self._save_registry()
        print(f"  ⚛️ HarmonyOS 意图已登记: {name} | DNA: {dna}")
        return intent

    # ----------------------------------------------------------------
    # 统一桥
    # ----------------------------------------------------------------

    def bridge(self, name: str,
               ios_name: Optional[str] = None,
               hos_bundle: Optional[str] = None,
               hos_ability: str = "MainAbility",
               input_text: Optional[str] = None) -> str:
        """
        一条指令同时桥接双端：
        - iOS: 触发同名（或指定）快捷指令
        - HarmonyOS: 返回/登记意图，供设备侧拉取执行
        """
        ios_hit, hos_hit = None, None
        if ios_name:
            ios_hit = self.ios_run(ios_name, input_text)
        if hos_bundle:
            hos_hit = self.harmony_intent(name, hos_bundle, hos_ability)

        bridge_dna = self._dna("BRIDGE")
        entry = {
            "name":    name,
            "ios":     ios_name,
            "harmony": hos_bundle,
            "dna":     bridge_dna,
            "at":      datetime.now().isoformat(),
        }
        self.registry.setdefault("bridges", []).append(entry)
        self._save_registry()

        print(f"\n  🌉 快捷指令桥完成: {name}")
        print(f"     iOS:      {ios_name or '未绑定'}")
        print(f"     HarmonyOS: {hos_bundle or '未绑定'}")
        print(f"     DNA: {bridge_dna}")
        return bridge_dna

    def registry_dump(self) -> Dict:
        """导出双端登记表"""
        return self.registry


if __name__ == "__main__":
    bridge = ShortcutBridge()
    print("龍魂全球开发者平台 · 快捷指令跨平台桥 v1.0")
    print(f"\n本机 iOS 快捷指令 ({len(bridge.ios_list())} 个):")
    for s in bridge.ios_list()[:10]:
        print(f"  ⚡️ {s}")
    print(f"\n登记表位置: {bridge.registry_path}")
