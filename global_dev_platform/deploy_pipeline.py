#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂全球开发者平台 · 一键发布流水线 v1.0
DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-DEPLOY-PIPELINE-v1.0
创建者: 诸葛鑫（UID9622）
协议: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
设计原则:
  App Store + AppGallery 双端一键发布流水线。
  面向正式开发者 · 从骨架到上架全链路 · 每一步打 DNA。
  DNA 一律走统一干支卦引擎。
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

from lh_dna import lh_dna

OUTPUT_DIR = Path.home() / "longhun-system" / "global_dev_platform" / "output"


class DeployPipeline:
    """
    一键发布流水线
    阶段: 预检 → 构建 → 测试 → 截图 → 归档 → 上架指引
    """

    STAGES = ["preflight", "build", "test", "screenshots", "archive", "upload"]

    def __init__(self, project_dir: Optional[str] = None):
        self.project = Path(project_dir) if project_dir else Path.cwd()
        self.output  = OUTPUT_DIR
        self.output.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _dna(action: str) -> str:
        return lh_dna(module="DEPLOY-PIPELINE", action=action, version="v1.0")

    # ----------------------------------------------------------------
    # 阶段 1 · 预检
    # ----------------------------------------------------------------

    def preflight(self) -> Dict[str, bool]:
        """发布前工具链预检"""
        print("\n🔍 [1/6] 发布预检")
        checks = {}
        for tool in ["xcrun", "xcodebuild", "shortcuts", "hdc"]:
            r = subprocess.run(["which", tool], capture_output=True, text=True)
            checks[tool] = r.returncode == 0
            print(f"  {'✅' if checks[tool] else '❌'} {tool}")
        dna = self._dna("PREFLIGHT")
        print(f"     预检 DNA: {dna}")
        return checks

    # ----------------------------------------------------------------
    # 阶段 2 · 构建
    # ----------------------------------------------------------------

    def build(self, scheme: str, mode: str = "release") -> Dict[str, str]:
        """构建 iOS + HarmonyOS 双端包"""
        print("\n🔨 [2/6] 双端构建")
        results = {}
        # iOS
        cmd = ["xcodebuild", "build", "-scheme", scheme,
               "-configuration", "Release" if mode == "release" else "Debug",
               "-derivedDataPath", str(self.output / "ios-build")]
        try:
            subprocess.run(cmd, cwd=str(self.project), check=True,
                           capture_output=True, timeout=1800)
            results["ios"] = "ok"
            print("  ✅ iOS 构建成功")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            results["ios"] = f"skip: {type(e).__name__}"
            print("  🟡 iOS 构建跳过（非 iOS 工程或工具链缺失）")
        # HarmonyOS
        hvigorw = self.project / "hvigorw"
        if hvigorw.exists():
            subprocess.run([str(hvigorw), "assembleHap", "--mode", mode],
                           cwd=str(self.project), check=True)
            results["harmony"] = "ok"
            print("  ✅ HarmonyOS 构建成功")
        else:
            results["harmony"] = "skip: 非 HarmonyOS 工程"
            print("  🟡 HarmonyOS 构建跳过（无 hvigorw）")
        dna = self._dna("BUILD")
        print(f"     构建 DNA: {dna}")
        return results

    # ----------------------------------------------------------------
    # 阶段 3 · 测试
    # ----------------------------------------------------------------

    def test(self) -> None:
        """占位：测试阶段（接入项目自有测试）"""
        print("\n🧪 [3/6] 测试")
        print("  🟡 请在项目内接入 XCTest / ohosTest，此处为流水线占位")
        self._log("test")

    # ----------------------------------------------------------------
    # 阶段 4 · 截图
    # ----------------------------------------------------------------

    def screenshots(self, udid: str, app_path: str) -> List[str]:
        """自动生成双端商店截图（简化版·5 张）"""
        print("\n📸 [4/6] 商店截图")
        shots = []
        try:
            from cross_runner import CrossRunner
            runner = CrossRunner()
            shots = runner.auto_generate_app_store_shots(udid, app_path,
                                                         str(self.output / "shots"))
            print(f"  ✅ 截图 {len(shots)} 张")
        except Exception as e:
            print(f"  🟡 截图跳过: {type(e).__name__}")
        self._log("screenshots", {"count": len(shots)})
        return shots

    # ----------------------------------------------------------------
    # 阶段 5 · 归档
    # ----------------------------------------------------------------

    def archive(self, artifacts: Dict[str, str]) -> str:
        """生成发布归档清单 + 元数据"""
        print("\n📦 [5/6] 发布归档")
        dna = self._dna("ARCHIVE")
        manifest = {
            "dna":       dna,
            "created":   datetime.now().isoformat(),
            "artifacts": artifacts,
        }
        manifest_path = self.output / f"release_manifest_{datetime.now():%Y%m%d_%H%M%S}.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), "utf-8")
        print(f"  ✅ 归档清单: {manifest_path}")
        print(f"     DNA: {dna}")
        return str(manifest_path)

    # ----------------------------------------------------------------
    # 阶段 6 · 上架指引
    # ----------------------------------------------------------------

    def upload(self, store: str = "both") -> None:
        """上架指引（App Store / AppGallery 人工确认步骤）"""
        print("\n🚀 [6/6] 上架指引")
        if store in ("ios", "both"):
            print("  🍎 App Store: xcrun altool --upload-app（或 Transporter）")
            print("     → App Store Connect 填写审核信息 → 提交审核")
        if store in ("harmony", "both"):
            print("  🤖 AppGallery: 使用 AGC 控制台上传 HAP")
            print("     → 配置签名 + 隐私声明 → 提交审核")
        dna = self._dna("UPLOAD-GUIDE")
        print(f"     上架 DNA: {dna}")

    # ----------------------------------------------------------------
    # 流水线主入口
    # ----------------------------------------------------------------

    def run(self, scheme: str, udid: str = "", app_path: str = "") -> None:
        """完整跑一遍发布流水线"""
        print("🌏 龍魂全球开发者平台 · 一键发布流水线 v1.0")
        self.preflight()
        build_result = self.build(scheme)
        self.test()
        shots = self.screenshots(udid, app_path) if udid else []
        manifest = self.archive({"build": build_result, "shots": shots})
        self.upload("both")
        print(f"\n✅ 流水线完成 | 归档: {manifest}")

    def _log(self, stage: str, data: Optional[Dict] = None) -> None:
        """写发布流水线日志（append-only）"""
        log_path = self.output / "deploy_log.jsonl"
        entry = {"stage": stage, "at": datetime.now().isoformat(), "data": data or {}}
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    pipe = DeployPipeline()
    pipe.preflight()
    print("\n用法示例:")
    print("  from deploy_pipeline import DeployPipeline")
    print("  pipe = DeployPipeline('/path/to/project')")
    print("  pipe.run('MyApp')")
