#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·CHIP-GATE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂芯片门禁 · 功能分层控制器 v1.0
Chip Gate — 检测底层芯片，按四层生态自动调整功能矩阵。

DNA: #龍芯⚡️丙午·辛未·CHIP-GATE-v1.0

四层分层:
  完美层 — 华为鲲鹏+昇腾+麒麟OS+欧拉OS → 100% 功能
  可用层 — 龙芯+兆芯+统信UOS → 85% 功能
  受限层 — x86(Intel/AMD)+Windows/macOS → 60% 功能
  拒绝层 — 含美系后门芯片（特定型号） → 0% 直接熔断

用法:
  python3 bin/lh_chip_gate.py                  # 检测芯片并输出功能矩阵
  python3 bin/lh_chip_gate.py --json           # JSON 格式输出
  python3 bin/lh_chip_gate.py --enforce        # 执行门禁（受限层会降级，拒绝层会退出）
  python3 bin/lh_chip_gate.py --check-only     # 仅检测芯片型号
  python3 bin/lh_chip_gate.py --deploy-check   # 部署前芯片校验
"""

import sys
import os
import json
import platform
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Dict, Optional, Tuple, Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DNA = "#龍芯⚡️丙午·辛未·CHIP-GATE-v1.0"
CST = timezone(timedelta(hours=8))


# ============================================================
# 芯片层级枚举
# ============================================================

class ChipTier(Enum):
    PERFECT = "perfect"         # 鲲鹏完美层
    COMPATIBLE = "compatible"   # 龙芯可用层
    RESTRICTED = "restricted"   # x86受限层
    BLOCKED = "blocked"         # 拒绝层


class ChipInfo:
    """芯片检测信息"""
    def __init__(self, chip_name: str, tier: ChipTier, raw_info: Optional[dict[str, Any]] = None):
        self.chip_name = chip_name
        self.tier = tier
        self.raw_info: dict[str, Any] = raw_info or {}
        self.detect_time = datetime.now(CST).isoformat()


# ============================================================
# 功能矩阵定义
# ============================================================

FEATURE_MATRIX = {
    ChipTier.PERFECT: {
        "tier_name": "鲲鹏完美层",
        "watermark": "🇨🇳 龍魂 · 国产完美生态",
        "message": "欢迎进入龍魂完全体。国产芯片+国产OS，全功能解锁。UID9622",
        "completeness": 100,
        "features": {
            "guomi_hw_accel": True,       # 国密SM2/3/4硬件加速
            "persona_full": True,          # 人格矩阵全五维
            "memory_local_encrypt": True,  # 长期记忆本地加密
            "audit_tamper_proof": True,    # 审计日志不可篡改
            "offline_full": True,          # 完全断网自治
            "antenna_nodes": 8,            # 蚁群触角并发节点
            "dcep_native": True,           # 数字人民币原生
            "one_click_deploy": True,      # 一键部署
            "sm4_hw_sign": True,           # SM4硬件签名
            "tpm_bind": True,              # TPM设备绑定
        }
    },
    ChipTier.COMPATIBLE: {
        "tier_name": "龙芯可用层",
        "watermark": "🇨🇳 龍魂 · 国产兼容生态",
        "message": "国产芯片检测通过。核心功能完整，部分性能依赖软件实现。UID9622",
        "completeness": 85,
        "features": {
            "guomi_hw_accel": False,       # 软件实现国密
            "persona_full": True,
            "memory_local_encrypt": True,
            "audit_tamper_proof": True,
            "offline_full": True,
            "antenna_nodes": 4,
            "dcep_native": False,          # 需适配
            "one_click_deploy": True,
            "sm4_hw_sign": False,
            "tpm_bind": True,
        }
    },
    ChipTier.RESTRICTED: {
        "tier_name": "x86受限层",
        "watermark": "⚠️ 龍魂 · 受限模式",
        "message": "检测到非国产芯片。功能受限，建议升级至鲲鹏/龙芯平台。UID9622",
        "completeness": 60,
        "features": {
            "guomi_hw_accel": False,
            "persona_full": True,          # 可用但延迟高
            "memory_local_encrypt": False, # 云端fallback
            "audit_tamper_proof": False,   # 可被系统级修改
            "offline_full": False,         # 需联网验证
            "antenna_nodes": 2,
            "dcep_native": False,
            "one_click_deploy": False,
            "sm4_hw_sign": False,
            "tpm_bind": False,
        }
    },
    ChipTier.BLOCKED: {
        "tier_name": "拒绝层",
        "watermark": "🚫 龍魂 · 拒绝运行",
        "message": "龍魂系统拒绝运行。检测到不安全芯片，直接熔断。UID9622",
        "completeness": 0,
        "features": {k: False for k in [
            "guomi_hw_accel", "persona_full", "memory_local_encrypt",
            "audit_tamper_proof", "offline_full", "antenna_nodes",
            "dcep_native", "one_click_deploy", "sm4_hw_sign", "tpm_bind"
        ]}
    }
}


# ============================================================
# 芯片检测引擎
# ============================================================

# 白名单/黑名单
PERFECT_CHIPS = ["kunpeng", "ascend", "phytium", "kirin"]
COMPATIBLE_CHIPS = ["loongson", "zhaoxin", "sw"]
BLOCKED_CHIPS = ["apple_m1", "apple_m2", "apple_m3", "apple_m4",
                 "qualcomm-sdx55", "qualcomm-snapdragon-x55"]


class ChipDetector:
    """跨平台芯片检测器"""

    @staticmethod
    def detect() -> ChipInfo:
        """主检测入口：Linux /proc/cpuinfo → macOS sysctl → Windows wmic"""
        system = platform.system().lower()

        if system == "linux":
            return ChipDetector._detect_linux()
        elif system == "darwin":
            return ChipDetector._detect_macos()
        elif system == "windows":
            return ChipDetector._detect_windows()
        else:
            return ChipInfo("unknown", ChipTier.RESTRICTED, {"system": system})

    @staticmethod
    def _detect_linux() -> ChipInfo:
        """Linux: 读 /proc/cpuinfo + 检查OS发行版"""
        raw = {}
        try:
            cpuinfo_path = "/proc/cpuinfo"
            if os.path.exists(cpuinfo_path):
                with open(cpuinfo_path, "r") as f:
                    cpuinfo = f.read().lower()
                raw["cpuinfo_sample"] = cpuinfo[:500]

                # 识别芯片
                if any(kw in cpuinfo for kw in ["kunpeng", "phytium"]):
                    chip = "kunpeng" if "kunpeng" in cpuinfo else "phytium"
                    raw["os_release"] = ChipDetector._read_os_release()
                    return ChipInfo(chip, ChipTier.PERFECT, raw)
                elif "loongson" in cpuinfo:
                    return ChipInfo("loongson", ChipTier.COMPATIBLE, raw)
                elif "zhaoxin" in cpuinfo:
                    return ChipInfo("zhaoxin", ChipTier.COMPATIBLE, raw)
                elif any(kw in cpuinfo for kw in ["intel", "amd", "x86"]):
                    # 进一步检查是否是鲲鹏昇腾环境（VM中可能显示x86）
                    os_info = ChipDetector._read_os_release()
                    raw["os_release"] = os_info
                    if any(kw in os_info for kw in ["euler", "kylin", "uos"]):
                        return ChipInfo("x86_on_domestic_os", ChipTier.COMPATIBLE, raw)
                    return ChipInfo("x86", ChipTier.RESTRICTED, raw)
                elif "sw" in cpuinfo or "sunway" in cpuinfo:
                    return ChipInfo("sw", ChipTier.COMPATIBLE, raw)

            # 检查 ARM (可能是鲲鹏)
            machine = platform.machine().lower()
            if machine in ("aarch64", "arm64"):
                raw["machine"] = machine
                os_info = ChipDetector._read_os_release()
                raw["os_release"] = os_info
                if any(kw in os_info for kw in ["euler", "kylin", "uos"]):
                    return ChipInfo("aarch64_domestic", ChipTier.PERFECT, raw)
                return ChipInfo("aarch64", ChipTier.RESTRICTED, raw)

            return ChipInfo("unknown_linux", ChipTier.RESTRICTED, raw)

        except Exception as e:
            return ChipInfo("error", ChipTier.RESTRICTED, {"error": str(e)})

    @staticmethod
    def _detect_macos() -> ChipInfo:
        """macOS: sysctl 检测 Apple Silicon / Intel"""
        raw = {"system": "darwin", "machine": platform.machine()}
        try:
            result = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True, text=True, timeout=5
            )
            brand = result.stdout.strip().lower()
            raw["brand"] = brand

            # Apple Silicon → 保守降级到受限层（非国产）
            if "apple" in brand:
                return ChipInfo(f"apple_silicon_{platform.machine()}", ChipTier.RESTRICTED, raw)
            elif "intel" in brand:
                return ChipInfo("intel_mac", ChipTier.RESTRICTED, raw)
            return ChipInfo("mac_unknown", ChipTier.RESTRICTED, raw)
        except Exception:
            return ChipInfo("mac_detect_failed", ChipTier.RESTRICTED, raw)

    @staticmethod
    def _detect_windows() -> ChipInfo:
        """Windows: wmic 检测"""
        raw = {"system": "windows", "machine": platform.machine()}
        try:
            result = subprocess.run(
                ["wmic", "cpu", "get", "name"],
                capture_output=True, text=True, timeout=5
            )
            name = result.stdout.strip().lower()
            raw["cpu_name"] = name
            if "zhaoxin" in name:
                return ChipInfo("zhaoxin", ChipTier.COMPATIBLE, raw)
            elif any(kw in name for kw in ["intel", "amd"]):
                return ChipInfo("x86_win", ChipTier.RESTRICTED, raw)
            return ChipInfo("win_unknown", ChipTier.RESTRICTED, raw)
        except Exception:
            return ChipInfo("win_detect_failed", ChipTier.RESTRICTED, raw)

    @staticmethod
    def _read_os_release() -> str:
        """读取 /etc/os-release 获取发行版信息"""
        paths = ["/etc/os-release", "/etc/euleros-release", "/etc/kylin-release"]
        for p in paths:
            if os.path.exists(p):
                try:
                    with open(p) as f:
                        return f.read().lower()
                except Exception:
                    pass
        return ""


# ============================================================
# 芯片门禁控制器
# ============================================================

class ChipGate:
    """龍魂芯片门禁 · 四层分层控制器"""

    def __init__(self, dna: str = DNA, enforce_strict: bool = False):
        self.dna = dna
        self.enforce_strict = enforce_strict
        self.detector = ChipDetector()
        self.chip_info: Optional[ChipInfo] = None
        self.feature_matrix: Optional[Dict[str, Any]] = None

    def scan(self) -> ChipInfo:
        """执行芯片检测"""
        self.chip_info = self.detector.detect()

        # 额外检查：BLOCKED_CHIPS
        chip_lower = self.chip_info.chip_name.lower()
        if any(b in chip_lower for b in BLOCKED_CHIPS):
            self.chip_info.tier = ChipTier.BLOCKED

        self.feature_matrix = FEATURE_MATRIX.get(self.chip_info.tier, FEATURE_MATRIX[ChipTier.RESTRICTED])
        return self.chip_info

    def enforce(self) -> Dict[str, Any]:
        """执行门禁检测并返回完整报告"""
        if self.chip_info is None:
            self.scan()

        info = self.chip_info
        assert info is not None, "scan() must set chip_info"
        matrix = self.feature_matrix
        assert matrix is not None, "scan() must set feature_matrix"

        report: dict[str, Any] = {
            "dna": self.dna,
            "timestamp": datetime.now(CST).isoformat(),
            "chip": {
                "name": info.chip_name,
                "tier": info.tier.value,
                "tier_name": matrix["tier_name"],
                "completeness": matrix["completeness"],
                "detect_time": info.detect_time,
                "raw": info.raw_info,
            },
            "features": matrix["features"],
            "watermark": matrix["watermark"],
            "message": matrix["message"],
        }

        # 拒绝层直接熔断
        if info.tier == ChipTier.BLOCKED:
            report["action"] = "BLOCK"
            report["exit_code"] = 77
            report["reason"] = "不安全芯片检测 → 龍魂直接熔断"
            if self.enforce_strict:
                print(json.dumps(report, ensure_ascii=False, indent=2))
                sys.exit(77)
            return report

        # 受限层降级警告
        if info.tier == ChipTier.RESTRICTED:
            report["action"] = "DEGRADE"
            report["exit_code"] = 0
            report["warnings"] = [
                "guomi_hw_accel: 国密无硬件加速，性能差10倍",
                "memory_local_encrypt: 记忆不可本地加密，使用云端fallback",
                "audit_tamper_proof: 审计日志可被系统级修改",
                "offline_full: 无法完全断网自治",
                "antenna_nodes: 蚁群触角仅2节点，熔断频繁",
                "dcep_native: 数字人民币接口不可用",
            ]
            return report

        # 可用层/完美层
        if info.tier == ChipTier.COMPATIBLE:
            report["action"] = "COMPATIBLE"
            report["warnings"] = [
                "guomi_hw_accel: 国密软件实现，性能略低于硬件加速",
                "dcep_native: 数字人民币需额外适配",
            ]
        else:
            report["action"] = "PERFECT"
            report["warnings"] = []

        report["exit_code"] = 0
        return report

    def get_deploy_command(self) -> str:
        """根据芯片层级返回对应的部署命令"""
        if self.chip_info is None:
            self.scan()

        assert self.chip_info is not None
        tier = self.chip_info.tier
        if tier == ChipTier.PERFECT:
            return "bash deploy/scripts/deploy_kunpeng_perfect.sh"
        elif tier == ChipTier.COMPATIBLE:
            return "bash deploy/scripts/deploy_loongson_compatible.sh"
        elif tier == ChipTier.RESTRICTED:
            return "bash deploy/scripts/deploy_x86_restricted.sh"
        else:
            return "# 拒绝层：无法部署"

    def get_env_vars(self) -> Dict[str, str]:
        """生成对应的环境变量"""
        if self.chip_info is None:
            self.scan()

        assert self.chip_info is not None
        assert self.feature_matrix is not None
        f = self.feature_matrix["features"]
        return {
            "LONGHUN_CHIP_TIER": self.chip_info.tier.value,
            "LONGHUN_CHIP_NAME": self.chip_info.chip_name,
            "LONGHUN_ANTENNA_NODES": str(f["antenna_nodes"]),
            "LONGHUN_GUOMI_HW": "1" if f["guomi_hw_accel"] else "0",
            "LONGHUN_OFFLINE_FULL": "1" if f["offline_full"] else "0",
            "LONGHUN_DCEP_NATIVE": "1" if f["dcep_native"] else "0",
            "LONGHUN_MEMORY_LOCAL": "1" if f["memory_local_encrypt"] else "0",
            "LONGHUN_TPM_BIND": "1" if f["tpm_bind"] else "0",
        }


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="龍魂芯片门禁 · 四层功能分层控制器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_chip_gate.py                 # 完整检测+功能矩阵
  python3 bin/lh_chip_gate.py --json          # JSON输出
  python3 bin/lh_chip_gate.py --check-only    # 仅芯片型号
  python3 bin/lh_chip_gate.py --enforce       # 严格门禁（拒绝层exit 77）
  python3 bin/lh_chip_gate.py --env           # 输出环境变量
  python3 bin/lh_chip_gate.py --deploy-check  # 部署前校验
        """
    )
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--check-only", action="store_true", help="仅检测芯片型号")
    parser.add_argument("--enforce", action="store_true", help="严格门禁（拒绝层exit 77）")
    parser.add_argument("--env", action="store_true", help="输出环境变量")
    parser.add_argument("--deploy-check", action="store_true", help="部署前校验")
    parser.add_argument("--dna", type=str, default=DNA, help="DNA追溯码")

    args = parser.parse_args()
    gate = ChipGate(dna=args.dna, enforce_strict=args.enforce)

    # 扫描
    gate.scan()

    if args.check_only:
        info = gate.chip_info
        assert info is not None, "scan() must set chip_info"
        if args.json:
            print(json.dumps({
                "chip_name": info.chip_name,
                "tier": info.tier.value,
                "tier_name": FEATURE_MATRIX[info.tier]["tier_name"],
                "detect_time": info.detect_time,
                "dna": args.dna,
            }, ensure_ascii=False, indent=2))
        else:
            print(f"芯片: {info.chip_name}")
            print(f"层级: {info.tier.value} ({FEATURE_MATRIX[info.tier]['tier_name']})")
            print(f"DNA: {args.dna}")
        return

    if args.env:
        env = gate.get_env_vars()
        for k, v in env.items():
            print(f"export {k}=\"{v}\"")
        return

    # 完整门禁
    report = gate.enforce()

    if args.deploy_check:
        print(f"芯片层级: {report['chip']['tier_name']}")
        print(f"功能完整度: {report['chip']['completeness']}%")
        print(f"部署命令: {gate.get_deploy_command()}")
        if report["chip"]["tier"] == "blocked":
            print("⛔ 无法部署：芯片在黑名单中")
            sys.exit(1)
        elif report["chip"]["tier"] == "restricted":
            print("⚠️  受限部署：功能降级，建议使用鲲鹏/龙芯")
        else:
            print("✅ 可以部署")
        return

    # 输出报告
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print(f"  龍魂芯片门禁 v1.0")
        print(f"  DNA: {args.dna}")
        print("=" * 60)
        print(f"  芯片: {report['chip']['name']}")
        print(f"  层级: {report['chip']['tier_name']} ({report['chip']['completeness']}%)")
        print(f"  动作: {report['action']}")
        print(f"  {report['watermark']}")
        print("-" * 60)
        print("  功能矩阵:")
        for feat, enabled in report["features"].items():
            icon = "✅" if enabled else "❌"
            print(f"    {icon} {feat}")
        if report.get("warnings"):
            print("-" * 60)
            print("  警告:")
            for w in report["warnings"]:
                print(f"    ⚠️  {w}")
        print("-" * 60)
        print(f"  {report['message']}")
        print("=" * 60)

    if args.enforce and report.get("exit_code", 0) != 0:
        sys.exit(report["exit_code"])


if __name__ == "__main__":
    main()
