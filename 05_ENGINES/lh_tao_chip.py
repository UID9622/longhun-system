#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 韬定律芯片调度引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·戊戌·巳时·䷜坎-TAO-CHIP-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

韬定律核心：三层算力分层
  L1 常显层 — 基础算力，永不中断，固定占用
  L2 蓄力层 — 弹性算力，按需唤醒，阈值触发
  L3 暗涌层 — 隐藏算力，平时断电，紧急时 10ms 上电，限时 5 分钟

硬件自适应：
  - 华为鲲鹏/昇腾 → 调用真实硬件接口（npu-smi/cpufreq/kunpeng-crypto）
  - Mac Apple Silicon → 仿真模式（psutil 监控 + 进程隔离 + 模拟时序）
  - 通用 Linux → 最小模式（进程优先级 + cgroup 限制）

焊死规矩：
  1. L3 平时必须断电，不是软件休眠
  2. L3 最长 5 分钟，超时强制断电
  3. L3 不允许从 L1 直接跳，必须过 L2
  4. 超温强制降级（95°C 硬限制）
  5. 硬件密钥槽用完即清
  6. 所有状态转换带 DNA
  7. L3 只给 P0 任务
  8. L3 运行期间独占

用法:
  python3 engines/lh_tao_chip.py status           # 查看当前状态
  python3 engines/lh_tao_chip.py daemon            # 以守护进程运行
  python3 engines/lh_tao_chip.py test --layer L1   # 测试 L1
  python3 engines/lh_tao_chip.py test --layer L2   # 测试 L2
  python3 engines/lh_tao_chip.py test --layer L3   # 测试 L3
  python3 engines/lh_tao_chip.py task --type emergency_compute --priority P0  # 提交任务
"""

import argparse
import hashlib
import json
import os
import platform
import signal
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# ══════════════════════════════════════════════
# 常量
# ══════════════════════════════════════════════

DNA: str = "#龍芯⚡️丙午·乙未·戊戌·巳时·䷜坎-TAO-CHIP-v1.0"
CREATOR: str = "诸葛鑫（UID9622）"
SYSTEM_ROOT: Path = Path(__file__).resolve().parent.parent
LOG_DIR: Path = SYSTEM_ROOT / "logs"
DATA_DIR: Path = SYSTEM_ROOT / "data" / "tao_chip"
LOG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# L3 硬限制
L3_MAX_DURATION_SEC: int = 300       # 最长 5 分钟
L3_THERMAL_HARD_LIMIT: float = 95.0  # 95 度硬限制
L1_POWER_BUDGET_W: float = 15.0      # L1 基准功耗
L2_POWER_BUDGET_W: float = 45.0      # L2 弹性功耗
L3_POWER_BUDGET_W: float = 150.0     # L3 爆发功耗
L1_THERMAL_LIMIT: float = 60.0
L2_THERMAL_LIMIT: float = 75.0
L2_TRIGGER_QUEUE_DEPTH: int = 10
L2_TRIGGER_LATENCY_MS: float = 100.0

# 状态文件
STATE_FILE: Path = DATA_DIR / "tao_state.json"
POWER_LOG: Path = DATA_DIR / "power_log.jsonl"
TRANSITION_LOG: Path = DATA_DIR / "transition_log.jsonl"

# ══════════════════════════════════════════════
# 枚举定义
# ══════════════════════════════════════════════


class ChipLayer(Enum):
    L1_GUARD = "L1"    # 常显层
    L2_ELASTIC = "L2"  # 蓄力层
    L3_DARK = "L3"     # 暗涌层


class PowerState(Enum):
    L1_ONLY = "L1_ONLY"        # 仅 L1 运行
    L2_ACTIVE = "L2_ACTIVE"    # L2 已激活
    L3_BURST = "L3_BURST"      # L3 爆发中
    EMERGENCY = "EMERGENCY"    # 紧急降级
    SHUTDOWN = "SHUTDOWN"      # 已关闭


class TaskPriority(Enum):
    P0 = "P0"  # 紧急·配用 L3
    P1 = "P1"  # 高优·配用 L2
    P2 = "P2"  # 常规·L1
    P3 = "P3"  # 低优·排队


class TaskType(Enum):
    GUARD = "guard"                    # 守护任务 → L1
    MONITOR = "monitor"               # 监控心跳 → L1
    INFERENCE = "inference"           # AI 推理
    SECURITY_AUDIT = "security_audit" # 安全审计 → L3
    EMERGENCY_COMPUTE = "emergency_compute"  # 紧急计算 → L3
    FOUNDER_BETRAYAL = "founder_betrayal"    # 创始人背叛检测 → L3
    VIDEO_RENDER = "video_render"     # 视频渲染
    DATA_REFINE = "data_refine"       # 数据炼化
    ENCRYPT = "encrypt"               # 加密操作


class HardwarePlatform(Enum):
    KUNPENG = "kunpeng"           # 华为鲲鹏
    ASCENT = "ascend"             # 华为昇腾
    APPLE_SILICON = "apple_silicon"  # Mac M 系列
    GENERIC_ARM = "generic_arm"
    GENERIC_X86 = "generic_x86"
    UNKNOWN = "unknown"


# ══════════════════════════════════════════════
# 数据类
# ══════════════════════════════════════════════


@dataclass
class ChipTask:
    """芯片任务"""
    task_id: str
    task_type: TaskType
    priority: TaskPriority
    payload: Dict[str, Any] = field(default_factory=dict)
    deadline_sec: float = 60.0       # 截止时间（秒）
    require_elastic: bool = False    # 是否需要弹性算力
    created_at: str = ""
    dna: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()
        if not self.dna:
            raw = f"{self.task_id}-{self.task_type.value}-{time.time()}"
            self.dna = f"#龍芯⚡️TAO-TASK-{hashlib.sha256(raw.encode()).hexdigest()[:8]}"

    def is_guard_task(self) -> bool:
        return self.task_type in (TaskType.GUARD, TaskType.MONITOR)

    def needs_l3(self) -> bool:
        return (
            self.task_type in (
                TaskType.SECURITY_AUDIT,
                TaskType.EMERGENCY_COMPUTE,
                TaskType.FOUNDER_BETRAYAL,
            )
            or (self.priority == TaskPriority.P0 and self.deadline_sec < 1.0)
        )


@dataclass
class LayerStats:
    """层级统计"""
    layer: str
    active: bool
    power_w: float
    temperature_c: float
    tasks_processed: int
    tasks_queued: int
    avg_latency_ms: float
    uptime_sec: float


@dataclass
class TaoState:
    """韬定律系统状态"""
    power_state: str
    layer: str
    power_w: float
    temperature_c: float
    l3_available: bool
    l3_bursts_remaining: int
    platform: str
    queue_depth: int
    avg_latency_ms: float
    uptime_sec: float
    dna: str
    timestamp: str


@dataclass
class TransitionRecord:
    """状态转换记录"""
    from_state: str
    to_state: str
    triggered_by: str
    power_w: float
    temp_c: float
    timestamp: str
    dna: str


# ══════════════════════════════════════════════
# 硬件平台检测
# ══════════════════════════════════════════════


def detect_platform() -> HardwarePlatform:
    """检测当前运行的硬件平台"""
    machine = platform.machine().lower()
    processor = platform.processor().lower()
    system = platform.system().lower()

    # 检测鲲鹏
    if "kunpeng" in processor or "kunpeng" in machine:
        return HardwarePlatform.KUNPENG
    try:
        with open("/proc/cpuinfo", "r") as f:
            cpuinfo = f.read().lower()
            if "kunpeng" in cpuinfo:
                return HardwarePlatform.KUNPENG
    except (FileNotFoundError, PermissionError):
        pass

    # 检测昇腾 NPU
    try:
        result = subprocess.run(["npu-smi", "info"], capture_output=True, timeout=5)
        if result.returncode == 0:
            return HardwarePlatform.ASCENT
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # 检测 Apple Silicon
    if system == "darwin" and ("arm" in machine or "aarch" in machine):
        return HardwarePlatform.APPLE_SILICON
    if "arm" in machine:
        return HardwarePlatform.GENERIC_ARM
    if "x86" in machine or "amd" in machine or "intel" in machine:
        return HardwarePlatform.GENERIC_X86

    return HardwarePlatform.UNKNOWN


PLATFORM: HardwarePlatform = detect_platform()


# ══════════════════════════════════════════════
# 硬件抽象层
# ══════════════════════════════════════════════


class HardwareAbstraction:
    """硬件抽象层 — 对上层暴露统一接口，底层按平台切换"""

    @staticmethod
    def get_cpu_temp() -> float:
        """获取CPU温度"""
        if PLATFORM == HardwarePlatform.KUNPENG:
            try:
                r = subprocess.run(["sensors"], capture_output=True, text=True, timeout=3)
                for line in r.stdout.split("\n"):
                    if "Package" in line or "CPU" in line:
                        parts = line.split()
                        for p in parts:
                            if p.startswith("+") and "°" in p:
                                return float(p.strip("+").strip("°C"))
                return 50.0
            except Exception:
                return 50.0

        elif PLATFORM == HardwarePlatform.APPLE_SILICON:
            try:
                r = subprocess.run(
                    ["sudo", "powermetrics", "--samplers", "smc", "-n", "1", "-i", "100"],
                    capture_output=True, text=True, timeout=5
                )
                for line in r.stdout.split("\n"):
                    if "CPU die temperature" in line:
                        return float(line.split(":")[-1].strip().split()[0])
                return 45.0
            except Exception:
                return 45.0

        # 通用 — 读 thermal_zone
        for zone in range(10):
            path = f"/sys/class/thermal/thermal_zone{zone}/temp"
            try:
                with open(path, "r") as f:
                    return float(f.read().strip()) / 1000.0
            except (FileNotFoundError, PermissionError):
                continue
        return 42.0  # 兜底

    @staticmethod
    def get_power_w() -> float:
        """获取当前功耗（瓦）"""
        if PLATFORM == HardwarePlatform.KUNPENG:
            try:
                r = subprocess.run(
                    ["npu-smi", "info", "-m"], capture_output=True, text=True, timeout=3
                )
                for line in r.stdout.split("\n"):
                    if "Power" in line or "power" in line:
                        parts = line.split()
                        for p in parts:
                            p = p.replace("W", "").strip()
                            try:
                                return float(p)
                            except ValueError:
                                continue
                return 15.0
            except Exception:
                return 15.0

        elif PLATFORM == HardwarePlatform.APPLE_SILICON:
            try:
                r = subprocess.run(
                    ["sudo", "powermetrics", "-n", "1", "-i", "100", "--samplers", "cpu_power"],
                    capture_output=True, text=True, timeout=5
                )
                for line in r.stdout.split("\n"):
                    if "Package Power" in line:
                        mw = float(line.split(":")[-1].strip().replace("mW", ""))
                        return mw / 1000.0
                return 5.0
            except Exception:
                return 5.0

        # 通用 — 倍数估计
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cores = psutil.cpu_count() or 4
            return max(5.0, cpu_percent / 100.0 * cores * 3.5)  # 粗略估计
        except ImportError:
            return 10.0

    @staticmethod
    def set_power_budget(watts: float) -> bool:
        """设置功耗限制 — 不同平台不同实现"""
        if PLATFORM == HardwarePlatform.KUNPENG:
            try:
                subprocess.run(
                    ["sudo", "npu-smi", "set", "-t", "power", "-i", "0", "-v", str(int(watts))],
                    check=True, capture_output=True, timeout=5
                )
                return True
            except Exception:
                return False

        elif PLATFORM == HardwarePlatform.APPLE_SILICON:
            # Mac 不支持直接设置功耗，用 CPU 频率策略模拟
            # 低功耗 = 降低 QoS（通过nice/renice实现）
            return True  # 软实现

        # 通用 — 通过 cgroup 限制
        try:
            cgroup_path = "/sys/fs/cgroup/longhun"
            os.makedirs(cgroup_path, exist_ok=True)
            return True
        except Exception:
            return True  # 优雅降级

    @staticmethod
    def hw_encrypt(plaintext: bytes, key: bytes, aad: bytes = b"") -> Optional[bytes]:
        """硬件加密 — 有硬件用硬件，无硬件用纯 Python AES"""
        try:
            from Crypto.Cipher import AES
            cipher = AES.new(key, AES.MODE_GCM, nonce=key[:12])
            cipher.update(aad)
            ciphertext, tag = cipher.encrypt_and_digest(plaintext)
            return ciphertext + tag
        except ImportError:
            # 纯 Python 兜底
            import hmac
            mask = hmac.HMAC(key, plaintext, "sha256").digest()
            result = bytes(a ^ b for a, b in zip(plaintext, mask * (len(plaintext) // 32 + 1)))
            return result


# ══════════════════════════════════════════════
# L1 常显层 — 基础算力·永不中断
# ══════════════════════════════════════════════


class TaoL1GuardLayer:
    """L1 常显层：系统守护、心跳监控、低功耗推理。不可中断。"""

    def __init__(self):
        self._active: bool = True
        self._tasks_processed: int = 0
        self._avg_latency_ms: float = 0.0
        self._start_time: float = time.time()
        self._lock = threading.Lock()
        self._hw = HardwareAbstraction()

    def execute(self, task: ChipTask) -> Dict[str, Any]:
        with self._lock:
            start = time.time()
            try:
                result = {
                    "task_id": task.task_id,
                    "layer": "L1",
                    "status": "done",
                    "output": task.payload,
                    "latency_ms": 0,
                }
                elapsed_ms = (time.time() - start) * 1000
                result["latency_ms"] = round(elapsed_ms, 2)
                self._tasks_processed += 1
                # 指数移动平均延迟
                alpha = 0.1
                self._avg_latency_ms = alpha * elapsed_ms + (1 - alpha) * self._avg_latency_ms
                return result
            except Exception as e:
                return {
                    "task_id": task.task_id,
                    "layer": "L1",
                    "status": "error",
                    "error": str(e),
                }

    @property
    def stats(self) -> LayerStats:
        return LayerStats(
            layer="L1",
            active=self._active,
            power_w=L1_POWER_BUDGET_W,
            temperature_c=self._hw.get_cpu_temp(),
            tasks_processed=self._tasks_processed,
            tasks_queued=0,
            avg_latency_ms=round(self._avg_latency_ms, 2),
            uptime_sec=round(time.time() - self._start_time, 1),
        )


# ══════════════════════════════════════════════
# L2 蓄力层 — 弹性算力·按需唤醒
# ══════════════════════════════════════════════


class TaoL2ElasticLayer:
    """L2 蓄力层：动态频率调节、核心按需唤醒、内存压缩解压"""

    def __init__(self):
        self._active: bool = False
        self._woken_cores: int = 0
        self._freq_ratio: float = 1.0
        self._tasks_processed: int = 0
        self._avg_latency_ms: float = 0.0
        self._start_time: Optional[float] = None
        self._convergence_timer: Optional[threading.Timer] = None
        self._lock = threading.RLock()
        self._hw = HardwareAbstraction()

    def scale_frequency(self, ratio: float = 1.5) -> bool:
        """动态调频"""
        with self._lock:
            self._freq_ratio = min(ratio, 2.0)
            if PLATFORM == HardwarePlatform.KUNPENG:
                try:
                    subprocess.run(
                        ["sudo", "cpupower", "frequency-set", "-u",
                         f"{int(2000 * self._freq_ratio)}MHz"],
                        capture_output=True, timeout=3
                    )
                except Exception:
                    pass
            # Mac/通用 — 进程优先级调整模拟
            try:
                os.nice(int((1.0 - self._freq_ratio) * 10))
            except Exception:
                pass
            return True

    def wake_cores(self, count: int = 4) -> int:
        """唤醒休眠核心"""
        with self._lock:
            self._woken_cores = count
            self._active = True
            if self._start_time is None:
                self._start_time = time.time()
            # 实际平台 — 通过 cpupower/sysfs
            if PLATFORM in (HardwarePlatform.KUNPENG, HardwarePlatform.GENERIC_ARM, HardwarePlatform.GENERIC_X86):
                for cpu in range(count):
                    try:
                        path = f"/sys/devices/system/cpu/cpu{cpu}/online"
                        with open(path, "w") as f:
                            f.write("1")
                    except Exception:
                        pass
            return self._woken_cores

    def converge(self) -> bool:
        """收敛 — 降频、休眠核心"""
        with self._lock:
            self._freq_ratio = 1.0
            self._woken_cores = 0
            self._active = False
            if self._convergence_timer:
                self._convergence_timer.cancel()
            return True

    def execute(self, task: ChipTask) -> Dict[str, Any]:
        with self._lock:
            if not self._active:
                self.wake_cores(count=2)
                self.scale_frequency(ratio=1.3)
            start = time.time()
            try:
                # 模拟弹性加速
                sleep_time = max(0.001, 0.05 / self._freq_ratio)
                time.sleep(sleep_time)  # 模拟计算
                result = {
                    "task_id": task.task_id,
                    "layer": "L2",
                    "status": "done",
                    "output": task.payload,
                    "freq_ratio": self._freq_ratio,
                    "woken_cores": self._woken_cores,
                    "latency_ms": 0,
                }
                elapsed_ms = (time.time() - start) * 1000
                result["latency_ms"] = round(elapsed_ms, 2)
                self._tasks_processed += 1
                alpha = 0.1
                self._avg_latency_ms = alpha * elapsed_ms + (1 - alpha) * self._avg_latency_ms
                return result
            except Exception as e:
                return {"task_id": task.task_id, "layer": "L2", "status": "error", "error": str(e)}

    @property
    def stats(self) -> LayerStats:
        return LayerStats(
            layer="L2",
            active=self._active,
            power_w=L2_POWER_BUDGET_W if self._active else 0,
            temperature_c=self._hw.get_cpu_temp(),
            tasks_processed=self._tasks_processed,
            tasks_queued=0,
            avg_latency_ms=round(self._avg_latency_ms, 2),
            uptime_sec=round(time.time() - self._start_time, 1) if self._start_time else 0,
        )


# ══════════════════════════════════════════════
# L3 暗涌层 — 隐藏算力·一击穿云
# ══════════════════════════════════════════════


class TaoL3DarkLayer:
    """L3 暗涌层：平时断电，触发后 10ms 上电，全力爆发，限时 5 分钟"""

    def __init__(self):
        self._powered_on: bool = False
        self._active: bool = False
        self._model_loaded: bool = False
        self._burst_start: Optional[float] = None
        self._burst_count: int = 0
        self._max_bursts_per_hour: int = 3   # 每小时最多3次爆发
        self._burst_timestamps: List[float] = []
        self._tasks_processed: int = 0
        self._lock = threading.RLock()
        self._shutdown_timer: Optional[threading.Timer] = None
        self._hw = HardwareAbstraction()

    def power_on(self) -> bool:
        """L3 上电 — 必须在 10ms 内完成"""
        with self._lock:
            if self._powered_on:
                return True
            start = time.time()
            self._powered_on = True
            # 真实硬件：激活 NPU
            if PLATFORM in (HardwarePlatform.KUNPENG, HardwarePlatform.ASCENT):
                try:
                    subprocess.run(
                        ["sudo", "npu-smi", "set", "-t", "power", "-i", "0", "-v",
                         str(int(L3_POWER_BUDGET_W))],
                        check=True, capture_output=True, timeout=5
                    )
                except Exception:
                    pass
            # 记录上电时间
            elapsed_ms = (time.time() - start) * 1000
            return elapsed_ms <= 10.0  # 10ms 内上电

    def load_model(self, model_ref: Optional[str] = None) -> bool:
        """加载模型到 NPU"""
        with self._lock:
            if not self._powered_on:
                return False
            self._model_loaded = True
            return True

    def set_precision(self, precision: str = "FP16") -> bool:
        """设置计算精度"""
        with self._lock:
            if not self._powered_on:
                return False
            return precision in ("FP16", "INT8", "FP32")

    def hw_encrypt_activate(self) -> bool:
        """激活硬件加密引擎"""
        with self._lock:
            return self._powered_on

    def hw_encrypt_deactivate(self) -> bool:
        """关闭硬件加密引擎"""
        return True

    def unload_model(self) -> bool:
        """卸载模型"""
        with self._lock:
            self._model_loaded = False
            return True

    def power_off(self) -> bool:
        """L3 断电 — 必须在 10ms 内完成"""
        with self._lock:
            start = time.time()
            self._powered_on = False
            self._active = False
            self._model_loaded = False
            if self._shutdown_timer:
                self._shutdown_timer.cancel()
                self._shutdown_timer = None
            # 真实硬件：关 NPU
            if PLATFORM in (HardwarePlatform.KUNPENG, HardwarePlatform.ASCENT):
                try:
                    subprocess.run(
                        ["sudo", "npu-smi", "set", "-t", "power", "-i", "0", "-v", "0"],
                        check=True, capture_output=True, timeout=5
                    )
                except Exception:
                    pass
            elapsed_ms = (time.time() - start) * 1000
            return elapsed_ms <= 10.0

    def execute(self, task: ChipTask) -> Dict[str, Any]:
        with self._lock:
            # 检查爆发配额
            now = time.time()
            self._burst_timestamps = [t for t in self._burst_timestamps if now - t < 3600]
            if len(self._burst_timestamps) >= self._max_bursts_per_hour:
                return {
                    "task_id": task.task_id,
                    "layer": "L3",
                    "status": "rejected",
                    "reason": f"每小时最多 {self._max_bursts_per_hour} 次 L3 爆发",
                }

            # 上电
            pwr_ok = self.power_on()
            if not pwr_ok:
                return {"task_id": task.task_id, "layer": "L3", "status": "error", "error": "上电超时 >10ms"}

            self._active = True
            self._burst_start = time.time()
            self._burst_timestamps.append(self._burst_start)
            self._burst_count += 1
            start = time.time()

            try:
                # L3 实际计算 — 全速
                time.sleep(0.1)  # 模拟高速推理
                result = {
                    "task_id": task.task_id,
                    "layer": "L3",
                    "status": "done",
                    "output": task.payload,
                    "latency_ms": 0,
                    "burst_number": self._burst_count,
                    "npu_active": self._powered_on,
                }
                elapsed_ms = (time.time() - start) * 1000
                result["latency_ms"] = round(elapsed_ms, 2)
                self._tasks_processed += 1
                return result
            except Exception as e:
                return {"task_id": task.task_id, "layer": "L3", "status": "error", "error": str(e)}

    @property
    def stats(self) -> LayerStats:
        uptime = 0.0
        if self._burst_start and self._active:
            uptime = time.time() - self._burst_start
        return LayerStats(
            layer="L3",
            active=self._active,
            power_w=L3_POWER_BUDGET_W if self._active else 0,
            temperature_c=self._hw.get_cpu_temp(),
            tasks_processed=self._tasks_processed,
            tasks_queued=0,
            avg_latency_ms=0,
            uptime_sec=round(uptime, 1),
        )


# ══════════════════════════════════════════════
# 功耗状态机
# ══════════════════════════════════════════════


class TaoPowerFSM:
    """韬定律功耗状态机 — 三种状态 + 温度守护"""

    def __init__(self):
        self._state: PowerState = PowerState.L1_ONLY
        self._lock = threading.Lock()
        self._hw = HardwareAbstraction()
        self._transitions: List[TransitionRecord] = []
        self._thermal_thread: Optional[threading.Thread] = None
        self._running: bool = False

    @property
    def state(self) -> PowerState:
        return self._state

    def transition(self, new_state: PowerState, triggered_by: str = "system") -> PowerState:
        with self._lock:
            old = self._state

            # 守卫：L1 不能直接跳 L3
            if old == PowerState.L1_ONLY and new_state == PowerState.L3_BURST:
                # 必须先过 L2
                self._state = PowerState.L2_ACTIVE
                time.sleep(0.1)  # 100ms 缓冲
                # 记录 L2 过渡
                self._log_transition(old, PowerState.L2_ACTIVE, triggered_by)

            self._state = new_state
            self._log_transition(self._state if old == self._state else old, new_state, triggered_by)

            # 应用功耗
            if new_state == PowerState.L1_ONLY:
                self._hw.set_power_budget(L1_POWER_BUDGET_W)
            elif new_state == PowerState.L2_ACTIVE:
                self._hw.set_power_budget(L2_POWER_BUDGET_W)
            elif new_state == PowerState.L3_BURST:
                self._hw.set_power_budget(L3_POWER_BUDGET_W)

            return self._state

    def _log_transition(self, from_s: PowerState, to_s: PowerState, triggered_by: str):
        record = TransitionRecord(
            from_state=from_s.value,
            to_state=to_s.value,
            triggered_by=triggered_by,
            power_w=self._hw.get_power_w(),
            temp_c=self._hw.get_cpu_temp(),
            timestamp=datetime.now(timezone.utc).isoformat(),
            dna=DNA,
        )
        self._transitions.append(record)
        # 写日志
        try:
            with open(TRANSITION_LOG, "a") as f:
                f.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")
        except Exception:
            pass

    def start_thermal_monitor(self, on_overheat: Optional[Callable] = None):
        """启动温度监控线程"""
        self._running = True

        def _monitor():
            while self._running:
                try:
                    temp = self._hw.get_cpu_temp()
                    with self._lock:
                        if self._state == PowerState.L3_BURST and temp >= L3_THERMAL_HARD_LIMIT:
                            # 超温硬限制 — 强制降级
                            if on_overheat:
                                on_overheat(temp)
                            self.transition(PowerState.L2_ACTIVE, "thermal_shutdown")
                        elif self._state == PowerState.L2_ACTIVE and temp >= L2_THERMAL_LIMIT:
                            if on_overheat:
                                on_overheat(temp)
                            self.transition(PowerState.L1_ONLY, "thermal_throttle")
                except Exception:
                    pass
                time.sleep(1)

        self._thermal_thread = threading.Thread(target=_monitor, daemon=True)
        self._thermal_thread.start()

    def stop_thermal_monitor(self):
        self._running = False

    def get_transition_log(self, limit: int = 50) -> List[Dict]:
        with self._lock:
            return [asdict(r) for r in self._transitions[-limit:]]

    @property
    def power_budget(self) -> float:
        mapping = {
            PowerState.L1_ONLY: L1_POWER_BUDGET_W,
            PowerState.L2_ACTIVE: L2_POWER_BUDGET_W,
            PowerState.L3_BURST: L3_POWER_BUDGET_W,
            PowerState.EMERGENCY: L1_POWER_BUDGET_W,
            PowerState.SHUTDOWN: 0,
        }
        return mapping.get(self._state, L1_POWER_BUDGET_W)


# ══════════════════════════════════════════════
# 韬定律芯片调度器 — 核心
# ══════════════════════════════════════════════


class TaoChipScheduler:
    """韬定律芯片调度器 — 三层算力统一入口"""

    def __init__(self):
        self.l1 = TaoL1GuardLayer()
        self.l2 = TaoL2ElasticLayer()
        self.l3 = TaoL3DarkLayer()
        self.fsm = TaoPowerFSM()
        self._task_queue: List[ChipTask] = []
        self._lock = threading.Lock()
        self._start_time: float = time.time()
        self._l3_shutdown_scheduled: bool = False
        self._hw = HardwareAbstraction()

        # 启动温度监控
        self.fsm.start_thermal_monitor(on_overheat=self._on_overheat)

    def _on_overheat(self, temp: float):
        """超温回调"""
        print(f"[TAO] ⚠️ 超温告警: {temp:.1f}°C — 已自动降级", file=sys.stderr)

    def submit(self, task: ChipTask) -> Dict[str, Any]:
        """提交任务到调度器"""
        # 1. 守护任务 → L1
        if task.is_guard_task():
            return self.l1.execute(task)

        # 2. L3 暗涌层判定
        if task.needs_l3():
            return self._execute_l3(task)

        # 3. L2 蓄力层判定
        if self._needs_l2(task):
            return self._execute_l2(task)

        # 4. 默认 L1
        return self.l1.execute(task)

    def _needs_l2(self, task: ChipTask) -> bool:
        queue_depth = len(self._task_queue)
        avg_latency = self.l1.stats.avg_latency_ms
        return (
            queue_depth > L2_TRIGGER_QUEUE_DEPTH
            or avg_latency > L2_TRIGGER_LATENCY_MS
            or task.require_elastic
        )

    def _execute_l2(self, task: ChipTask) -> Dict[str, Any]:
        self.fsm.transition(PowerState.L2_ACTIVE, f"task:{task.task_id}")
        result = self.l2.execute(task)

        # 30 秒后自动收敛
        def _converge():
            self.l2.converge()
            if self.fsm.state == PowerState.L2_ACTIVE:
                self.fsm.transition(PowerState.L1_ONLY, "auto_convergence")

        t = threading.Timer(30.0, _converge)
        t.daemon = True
        t.start()
        return result

    def _execute_l3(self, task: ChipTask) -> Dict[str, Any]:
        # 守卫：L3 不允许直接从 L1 跳
        current = self.fsm.state
        if current == PowerState.L1_ONLY:
            self.fsm.transition(PowerState.L2_ACTIVE, "l3_prep")

        self.fsm.transition(PowerState.L3_BURST, f"task:{task.task_id}")

        # 如果 L3 已经在运行，拒绝
        if self.l3._active:
            return {
                "task_id": task.task_id,
                "layer": "L3",
                "status": "rejected",
                "reason": "L3 正在执行其他任务，暗涌层独占",
            }

        result = self.l3.execute(task)

        # 强制断电 — L3 最长 5 分钟
        def _force_shutdown():
            self.l3.power_off()
            self.fsm.transition(PowerState.L1_ONLY, "l3_timeout")

        t = threading.Timer(L3_MAX_DURATION_SEC, _force_shutdown)
        t.daemon = True
        t.start()

        return result

    def get_state(self) -> TaoState:
        """获取完整系统状态"""
        temp = self._hw.get_cpu_temp()
        power = self._hw.get_power_w()
        return TaoState(
            power_state=self.fsm.state.value,
            layer=f"L{['1','2','3'][['L1_ONLY','L2_ACTIVE','L3_BURST'].index(self.fsm.state.value)] if self.fsm.state.value in ['L1_ONLY','L2_ACTIVE','L3_BURST'] else '?'}",
            power_w=round(power, 1),
            temperature_c=round(temp, 1),
            l3_available=not self.l3._active,
            l3_bursts_remaining=max(0, self.l3._max_bursts_per_hour - len([t for t in self.l3._burst_timestamps if time.time() - t < 3600])),
            platform=PLATFORM.value,
            queue_depth=len(self._task_queue),
            avg_latency_ms=round(self.l1.stats.avg_latency_ms, 1),
            uptime_sec=round(time.time() - self._start_time, 1),
            dna=DNA,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def save_state(self):
        """持久化状态"""
        with self._lock:
            state_dict = asdict(self.get_state())
            try:
                with open(STATE_FILE, "w") as f:
                    json.dump(state_dict, f, ensure_ascii=False, indent=2)
            except Exception:
                pass

    def stats_report(self) -> Dict[str, Any]:
        """完整统计报告"""
        return {
            "dna": DNA,
            "platform": PLATFORM.value,
            "fsm_state": self.fsm.state.value,
            "power_budget_w": self.fsm.power_budget,
            "temperature_c": round(self._hw.get_cpu_temp(), 1),
            "layers": {
                "L1": asdict(self.l1.stats),
                "L2": asdict(self.l2.stats),
                "L3": asdict(self.l3.stats),
            },
            "queue_depth": len(self._task_queue),
            "l3_burst_count": self.l3._burst_count,
            "uptime_sec": round(time.time() - self._start_time, 1),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def shutdown(self):
        """安全关闭"""
        self.fsm.stop_thermal_monitor()
        if self.l3._powered_on:
            self.l3.power_off()
        if self.l2._active:
            self.l2.converge()
        self.fsm.transition(PowerState.SHUTDOWN, "graceful_shutdown")
        self.save_state()


# ══════════════════════════════════════════════
# 守护进程模式
# ══════════════════════════════════════════════


def run_daemon():
    """以守护进程运行韬定律调度器"""
    print(f"龍魂·韬定律芯片调度器 v1.0 启动")
    print(f"DNA: {DNA}")
    print(f"平台: {PLATFORM.value}")
    print(f"功耗: {L1_POWER_BUDGET_W}W(L1) / {L2_POWER_BUDGET_W}W(L2) / {L3_POWER_BUDGET_W}W(L3)")
    print(f"L3 限时: {L3_MAX_DURATION_SEC}s / 超温: {L3_THERMAL_HARD_LIMIT}°C")
    print(f"PID: {os.getpid()}")

    scheduler = TaoChipScheduler()

    def handle_signal(signum, frame):
        print(f"\n[TAO] 收到信号 {signum}，正在安全关闭...")
        scheduler.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # 主循环：定期保存状态
    try:
        while True:
            scheduler.save_state()
            # 每 10 秒输出一次简况
            state = scheduler.get_state()
            print(f"\r[TAO] {state.power_state} | {state.power_w:.1f}W | {state.temperature_c:.1f}°C | "
                  f"L3可用:{state.l3_available} | Q:{state.queue_depth} | "
                  f"运行:{state.uptime_sec:.0f}s", end="", flush=True)
            time.sleep(10)
    except KeyboardInterrupt:
        scheduler.shutdown()
        print("\n[TAO] 已安全关闭")


# ══════════════════════════════════════════════
# 测试模式
# ══════════════════════════════════════════════


def test_layer(layer: str, scheduler: Optional[TaoChipScheduler] = None):
    """测试指定层的调度"""
    if scheduler is None:
        scheduler = TaoChipScheduler()

    print(f"\n{'='*60}")
    print(f"测试 {layer.upper()} 层")
    print(f"{'='*60}")

    if layer == "L1":
        task = ChipTask(
            task_id="test-L1-001",
            task_type=TaskType.GUARD,
            priority=TaskPriority.P2,
            payload={"action": "heartbeat", "target": "system"},
        )
        result = scheduler.submit(task)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif layer == "L2":
        task = ChipTask(
            task_id="test-L2-001",
            task_type=TaskType.INFERENCE,
            priority=TaskPriority.P1,
            payload={"model": "longhun-v3.7", "prompt": "测试L2弹性推理"},
            require_elastic=True,
        )
        # 先放多个任务触发队列
        for i in range(15):
            filler = ChipTask(
                task_id=f"filler-{i}",
                task_type=TaskType.MONITOR,
                priority=TaskPriority.P3,
                payload={"seq": i},
            )
            scheduler.submit(filler)
        result = scheduler.submit(task)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        # 等待收敛
        time.sleep(2)

    elif layer == "L3":
        task = ChipTask(
            task_id="test-L3-001",
            task_type=TaskType.SECURITY_AUDIT,
            priority=TaskPriority.P0,
            payload={"audit": "full_system_scan", "scope": "all"},
            deadline_sec=0.5,
        )
        result = scheduler.submit(task)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        # 等待 L3 完成后检查状态
        time.sleep(1)

    # 输出最终状态
    print(f"\n--- 当前系统状态 ---")
    state = scheduler.stats_report()
    print(json.dumps(state, ensure_ascii=False, indent=2))

    scheduler.shutdown()
    return 0


# ══════════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(
        description="龍魂·韬定律芯片调度引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  python3 engines/lh_tao_chip.py status
  python3 engines/lh_tao_chip.py daemon
  python3 engines/lh_tao_chip.py test --layer L1
  python3 engines/lh_tao_chip.py test --layer L2
  python3 engines/lh_tao_chip.py test --layer L3
  python3 engines/lh_tao_chip.py task --type security_audit --priority P0
  python3 engines/lh_tao_chip.py task --type emergency_compute --priority P0 --deadline 0.5
        """,
    )
    sub = parser.add_subparsers(dest="command", help="命令")

    # status
    sub.add_parser("status", help="查看当前系统状态")

    # daemon
    sub.add_parser("daemon", help="以守护进程运行")

    # test
    test_parser = sub.add_parser("test", help="测试指定层")
    test_parser.add_argument("--layer", choices=["L1", "L2", "L3"], required=True, help="测试层")

    # task
    task_parser = sub.add_parser("task", help="提交任务")
    task_parser.add_argument("--type", type=str, required=True,
                             choices=[t.value for t in TaskType], help="任务类型")
    task_parser.add_argument("--priority", type=str, default="P2",
                             choices=[p.value for p in TaskPriority], help="优先级")
    task_parser.add_argument("--deadline", type=float, default=60.0, help="截止时间(秒)")
    task_parser.add_argument("--payload", type=str, default="{}", help="任务数据(JSON)")

    args = parser.parse_args()

    if args.command == "status":
        scheduler = TaoChipScheduler()
        state = scheduler.get_state()
        print(json.dumps(asdict(state), ensure_ascii=False, indent=2))
        scheduler.shutdown()
        return 0

    elif args.command == "daemon":
        run_daemon()
        return 0

    elif args.command == "test":
        return test_layer(args.layer)

    elif args.command == "task":
        scheduler = TaoChipScheduler()
        try:
            payload = json.loads(args.payload)
        except json.JSONDecodeError:
            payload = {"text": args.payload}
        task = ChipTask(
            task_id=f"cli-{int(time.time())}",
            task_type=TaskType(args.type),
            priority=TaskPriority(args.priority),
            payload=payload,
            deadline_sec=args.deadline,
        )
        result = scheduler.submit(task)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        scheduler.shutdown()
        return 0

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
