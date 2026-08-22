#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·韬定律用量采集器 v2.2
DNA: #龍芯⚡️丙午·乙未·辛酉·甲午·䷫姤-TAO-LAW-INTEGRATED-v2.2

功能：
- 每 60 秒采集一次功耗（mJ）与调用计数
- 自动识别平台：昇腾 npu-smi / NVIDIA nvidia-smi / CPU RAPL / macOS powermetrics
- 输出 8 字段审计日志，只传用量不传内容
- 维护 sha256 审计链
"""

import hashlib
import os
import platform
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

# ═══════════════════════════════════════════════════════════
# L0 常量
# ═══════════════════════════════════════════════════════════

# 默认数据目录：/tmp/lh_test 便于无 root 测试；生产环境可用环境变量 TAO_DATA_DIR 覆盖
DATA_DIR = Path(os.environ.get("TAO_DATA_DIR", "/tmp/lh_test"))
LOG_FILE = Path(os.environ.get("TAO_USAGE_LOG", DATA_DIR / "tao_usage.log"))
LAYER = "hot"  # 采集器默认挂在热层；多平台部署时可按实机调整
CALL_COUNT = 1
ROUTE_PRIORITY = "L3"
SAMPLE_SECONDS = 60


# ═══════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════

def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def task_type_hash() -> str:
    return "sha256:" + sha256_hex("usage_collector")[:16]


def last_hash(log_file: Path) -> str:
    if not log_file.exists():
        return "sha256:" + "0" * 64
    lines = log_file.read_text().strip().splitlines()
    if not lines:
        return "sha256:" + "0" * 64
    return lines[-1].split(",")[-1]


def write_log(log_file: Path, energy_mj: int) -> str:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    prev = last_hash(log_file)
    timestamp = now_iso()
    payload = ",".join([
        timestamp,
        LAYER,
        task_type_hash(),
        str(SAMPLE_SECONDS),
        str(energy_mj),
        str(CALL_COUNT),
        ROUTE_PRIORITY,
        prev,
    ])
    new_hash = "sha256:" + sha256_hex(payload)
    line = payload + "," + new_hash
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    return new_hash


# ═══════════════════════════════════════════════════════════
# 平台功耗采集器
# ═══════════════════════════════════════════════════════════

class PowerProbe:
    """跨平台功耗探针基类"""

    def read_power_w(self) -> Optional[float]:
        raise NotImplementedError

    def name(self) -> str:
        return self.__class__.__name__


class NpuSmiProbe(PowerProbe):
    """昇腾 Ascend：npu-smi info -t power -i 0"""

    def read_power_w(self) -> Optional[float]:
        try:
            out = subprocess.run(
                ["npu-smi", "info", "-t", "power", "-i", "0"],
                capture_output=True, text=True, timeout=5
            )
            # 优先匹配数字+W 格式
            m = re.search(r"(\d+(?:\.\d+)?)\s*W", out.stdout, re.IGNORECASE)
            if m:
                return float(m.group(1))
        except Exception:
            pass
        return None

    def name(self) -> str:
        return "npu-smi(Ascend)"


class NvidiaSmiProbe(PowerProbe):
    """NVIDIA：nvidia-smi --query-gpu=power.draw --format=csv"""

    def read_power_w(self) -> Optional[float]:
        try:
            out = subprocess.run(
                ["nvidia-smi", "--query-gpu=power.draw", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=5
            )
            val = out.stdout.strip().split("\n")[0].strip()
            return float(val)
        except Exception:
            pass
        return None

    def name(self) -> str:
        return "nvidia-smi(CUDA)"


class RaplProbe(PowerProbe):
    """Linux Intel/AMD RAPL：/sys/class/powercap/intel-rapl/*"""

    def read_power_w(self) -> Optional[float]:
        base = Path("/sys/class/powercap")
        if not base.exists():
            return None
        # Intel RAPL
        domains = list(base.glob("intel-rapl/intel-rapl:*"))
        if not domains:
            domains = list(base.glob("intel-rapl:*"))
        total_uj = 0
        valid = False
        for d in domains:
            name_file = d / "name"
            if name_file.exists() and "package" not in name_file.read_text().lower():
                continue
            energy_file = d / "energy_uj"
            if energy_file.exists():
                try:
                    total_uj += int(energy_file.read_text().strip())
                    valid = True
                except ValueError:
                    pass
        if not valid:
            return None
        # 采样差值法需要两次读取，这里简化为瞬时估算：
        # 返回当前累计值的微分近似（首次调用会偏大，建议配合 time.sleep 差分）
        return self._rapl_diff()

    def _rapl_diff(self) -> Optional[float]:
        """通过 0.5s 差分估算功率"""
        readings = []
        for _ in range(2):
            total = 0
            domains = list(Path("/sys/class/powercap").glob("intel-rapl/intel-rapl:*"))
            if not domains:
                domains = list(Path("/sys/class/powercap").glob("intel-rapl:*"))
            for d in domains:
                name_file = d / "name"
                if name_file.exists() and "package" not in name_file.read_text().lower():
                    continue
                energy_file = d / "energy_uj"
                if energy_file.exists():
                    try:
                        total += int(energy_file.read_text().strip())
                    except ValueError:
                        pass
            readings.append(total)
            time.sleep(0.5)
        diff = readings[1] - readings[0]
        if diff < 0:
            # 计数器回绕，忽略
            return None
        return diff / 0.5 / 1_000_000  # W

    def name(self) -> str:
        return "RAPL(CPU)"


class MacPowerMetricsProbe(PowerProbe):
    """macOS：powermetrics --samplers smc -n 1"""

    def read_power_w(self) -> Optional[float]:
        try:
            out = subprocess.run(
                ["powermetrics", "--samplers", "smc", "-n", "1", "--format", "plist"],
                capture_output=True, text=True, timeout=10
            )
            # 匹配 <key>CPU Power</key><integer>...
            m = re.search(r"<key>CPU Power</key>\s*<integer>(\d+)</integer>", out.stdout)
            if m:
                return float(m.group(1)) / 1000.0  # mW → W
            # 备选：key 名可能为 cpu_power / package_watts
            m = re.search(r"<key>[^<]*[Pp]ower[^<]*</key>\s*<integer>(\d+)</integer>", out.stdout)
            if m:
                return float(m.group(1)) / 1000.0
        except Exception:
            pass
        return None

    def name(self) -> str:
        return "powermetrics(macOS)"


class MacIORegProbe(PowerProbe):
    """macOS 备选：ioreg -l 中 AppleSmartBattery 相关字段"""

    def read_power_w(self) -> Optional[float]:
        try:
            out = subprocess.run(
                ["ioreg", "-l", "-w", "0"],
                capture_output=True, text=True, timeout=5
            )
            # 优先匹配电池当前功耗字段（单位 mW 常见）
            for key in ["InstantAmperage", "Amperage", "Voltage"]:
                m = re.search(rf'"{key}"\s*=\s*(\d+)', out.stdout)
                if m:
                    val = float(m.group(1))
                    # 典型笔记本功耗 0-200W；超出视为异常
                    if 0 <= val < 1000:
                        return val
                    elif 0 <= val < 1000000:
                        return val / 1000.0
        except Exception:
            pass
        return None

    def name(self) -> str:
        return "ioreg(macOS-fallback)"


# ═══════════════════════════════════════════════════════════
# 探针自动选择
# ═══════════════════════════════════════════════════════════

def select_probe() -> Tuple[PowerProbe, str]:
    probes = [NpuSmiProbe(), NvidiaSmiProbe()]
    if platform.system() == "Darwin":
        probes += [MacPowerMetricsProbe(), MacIORegProbe()]
    else:
        probes += [RaplProbe()]

    for p in probes:
        val = p.read_power_w()
        if val is not None and val >= 0:
            return p, p.name()

    # 最终 fallback：返回 0，避免中断
    class ZeroProbe(PowerProbe):
        def read_power_w(self):
            return 0.0
        def name(self):
            return "zero-fallback"
    return ZeroProbe(), "zero-fallback"


# ═══════════════════════════════════════════════════════════
# 主循环
# ═══════════════════════════════════════════════════════════

def main():
    probe, probe_name = select_probe()
    print(f"[TAO-USAGE] 启用功耗探针: {probe_name}")
    print(f"[TAO-USAGE] 日志文件: {LOG_FILE}")
    print(f"[TAO-USAGE] 采样周期: {SAMPLE_SECONDS}s")

    while True:
        start = time.time()
        power_w = probe.read_power_w() or 0.0
        # energy_mj = W * s * 1000
        energy_mj = int(power_w * SAMPLE_SECONDS * 1000)
        h = write_log(LOG_FILE, energy_mj)
        print(f"{now_iso()} power={power_w:.2f}W energy={energy_mj}mJ hash={h[:16]}")
        elapsed = time.time() - start
        sleep = max(0, SAMPLE_SECONDS - elapsed)
        time.sleep(sleep)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[TAO-USAGE] 采集器退出")
        sys.exit(0)
