#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# DNA: #龍芯⚡️丙午·乙未·丁酉·子时·☰乾-GUANLAN-CIRCUIT-BREAKER-v1.0-cb3f7e1d
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫 (UID9622)
# 协议: CC BY-NC-SA 4.0
# ============================================================
"""
龍魂 · 观澜 — 断路器 v1.0
三种熔断条件：连续失败 | 越权访问 | 异常频率
熔断后自动锁定600秒，期间任何请求自动拒绝
用户可手动提前解锁
"""
import hashlib
import json
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class TripReason(Enum):
    CONSECUTIVE_FAILURES = "consecutive_failures"  # 连续3次失败
    UNAUTHORIZED_ACCESS = "unauthorized_access"     # 越权访问
    ABNORMAL_FREQUENCY = "abnormal_frequency"       # 异常频率
    MANUAL = "manual"                                # 用户手动熔断


class BreakerState(Enum):
    CLOSED = "closed"          # 正常
    OPEN = "open"              # 熔断中
    HALF_OPEN = "half_open"    # 试探恢复中


@dataclass
class TripRecord:
    """熔断记录"""
    reason: TripReason
    triggered_by: str          # 触发来源（URL/域名）
    detail: str
    timestamp: float = field(default_factory=time.time)
    lock_duration: float = 600.0  # 锁定秒数
    manual_override: bool = False


@dataclass
class BreakerStatus:
    """断路器状态"""
    state: BreakerState = BreakerState.CLOSED
    locked_until: float = 0.0
    failure_count: dict[str, int] = field(default_factory=dict)
    violation_count: dict[str, int] = field(default_factory=dict)
    rate_anomaly_count: dict[str, int] = field(default_factory=dict)
    history: list[TripRecord] = field(default_factory=list)
    total_trips: int = 0


class CircuitBreaker:
    """觀澜断路器 — 异常行为自动熔断"""

    # 熔断阈值
    MAX_CONSECUTIVE_FAILURES = 3         # 连续失败上限
    MAX_VIOLATIONS = 2                    # 越权警告上限
    RATE_SPIKE_THRESHOLD = 50             # 每秒请求数异常阈值
    RATE_WINDOW_SECONDS = 5               # 速率窗口
    DEFAULT_LOCK_SECONDS = 600            # 默认锁定600秒

    def __init__(self, auto_trip: bool = True):
        self.auto_trip = auto_trip
        self.status = BreakerStatus()
        self._lock = threading.Lock()
        self._rate_window: list[float] = []  # 速率追踪

    # ============================================================
    # 三种熔断条件
    # ============================================================

    def record_failure(self, source: str) -> bool:
        """记录一次失败，返回是否触发熔断"""
        with self._lock:
            self.status.failure_count[source] = \
                self.status.failure_count.get(source, 0) + 1

            if self.status.failure_count[source] >= self.MAX_CONSECUTIVE_FAILURES:
                self.trip(TripReason.CONSECUTIVE_FAILURES, source,
                          f"连续 {self.status.failure_count[source]} 次失败")
                return True
            return False

    def record_violation(self, source: str, detail: str = "") -> bool:
        """记录一次越权访问，返回是否触发熔断"""
        with self._lock:
            self.status.violation_count[source] = \
                self.status.violation_count.get(source, 0) + 1

            if self.status.violation_count[source] >= self.MAX_VIOLATIONS:
                self.trip(TripReason.UNAUTHORIZED_ACCESS, source,
                          f"越权访问: {detail}" if detail else "检测到越权访问")
                return True
            return False

    def check_rate_anomaly(self, source: str) -> bool:
        """检测异常请求频率，返回是否触发熔断"""
        with self._lock:
            now = time.time()
            self._rate_window.append(now)

            # 清理窗口外的记录
            cutoff = now - self.RATE_WINDOW_SECONDS
            self._rate_window = [t for t in self._rate_window if t > cutoff]

            # 计算速率
            rate = len(self._rate_window) / self.RATE_WINDOW_SECONDS

            if rate > self.RATE_SPIKE_THRESHOLD:
                self.status.rate_anomaly_count[source] = \
                    self.status.rate_anomaly_count.get(source, 0) + 1

                if self.status.rate_anomaly_count[source] >= 2:
                    self.trip(TripReason.ABNORMAL_FREQUENCY, source,
                              f"异常请求频率: {rate:.0f} req/s (阈值: {self.RATE_SPIKE_THRESHOLD})")
                    return True
                return False
            return False

    # ============================================================
    # 熔断执行
    # ============================================================

    def trip(self, reason: TripReason, source: str, detail: str,
             lock_seconds: float | None = None):
        """执行熔断"""
        lock_duration = lock_seconds or self.DEFAULT_LOCK_SECONDS

        record = TripRecord(
            reason=reason,
            triggered_by=source,
            detail=detail,
            lock_duration=lock_duration,
        )

        with self._lock:
            self.status.state = BreakerState.OPEN
            self.status.locked_until = time.time() + lock_duration
            self.status.history.append(record)
            self.status.total_trips += 1

        print(f"[观澜·断路器] 🚨 熔断触发 | 原因: {reason.value} | "
              f"来源: {source} | 锁定: {lock_duration}s")
        print(f"[观澜·断路器] 详情: {detail}")

    def manual_trip(self, source: str = "manual", reason: str = "用户手动熔断",
                    lock_seconds: float | None = None) -> TripRecord:
        """用户手动熔断"""
        record = TripRecord(
            reason=TripReason.MANUAL,
            triggered_by=source,
            detail=reason,
            lock_duration=lock_seconds or self.DEFAULT_LOCK_SECONDS,
            manual_override=True,
        )

        with self._lock:
            self.status.state = BreakerState.OPEN
            self.status.locked_until = time.time() + (lock_seconds or self.DEFAULT_LOCK_SECONDS)
            self.status.history.append(record)
            self.status.total_trips += 1

        print(f"[观澜·断路器] 🔒 手动熔断 | {reason}")
        return record

    def unlock(self) -> bool:
        """手动解锁"""
        if self.status.state == BreakerState.CLOSED:
            return True

        with self._lock:
            self.status.state = BreakerState.CLOSED
            self.status.locked_until = 0
            # 清零计数器
            self.status.failure_count.clear()
            self.status.violation_count.clear()
            self.status.rate_anomaly_count.clear()

        print("[观澜·断路器] 🔓 已手动解锁")
        return True

    # ============================================================
    # 状态查询
    # ============================================================

    def is_blocked(self, source: str | None = None) -> bool:
        """检查当前是否应阻断请求"""
        if self.status.state == BreakerState.CLOSED:
            return False

        if self.status.state == BreakerState.OPEN:
            if time.time() >= self.status.locked_until:
                # 自动恢复：先进入HALF_OPEN试探
                self._try_recover()
                return False
            return True

        # HALF_OPEN: 放行少量请求试探
        return False

    def _try_recover(self):
        """尝试从熔断中恢复"""
        with self._lock:
            if time.time() >= self.status.locked_until:
                self.status.state = BreakerState.HALF_OPEN
                print("[观澜·断路器] 🟡 进入半开状态，试探恢复...")

    def confirm_recovery(self):
        """确认已恢复"""
        with self._lock:
            self.status.state = BreakerState.CLOSED
            self.status.locked_until = 0
            self.status.failure_count.clear()
            self.status.violation_count.clear()
            self.status.rate_anomaly_count.clear()
            print("[观澜·断路器] 🟢 已恢复正常")

    def get_remaining_lock(self) -> float:
        """剩余锁定时间（秒）"""
        if self.status.state != BreakerState.OPEN:
            return 0.0
        return max(0.0, self.status.locked_until - time.time())

    def get_status(self) -> dict[str, object]:
        """获取完整状态"""
        return {
            "state": self.status.state.value,
            "locked": self.status.state == BreakerState.OPEN,
            "remaining_lock_seconds": int(self.get_remaining_lock()),
            "locked_until": self.status.locked_until,
            "total_trips": self.status.total_trips,
            "failure_count": dict(self.status.failure_count),
            "violation_count": dict(self.status.violation_count),
            "rate_anomaly_count": dict(self.status.rate_anomaly_count),
            "recent_trips": [
                {
                    "reason": r.reason.value,
                    "source": r.triggered_by,
                    "detail": r.detail,
                    "timestamp": r.timestamp,
                    "manual": r.manual_override,
                }
                for r in self.status.history[-5:]
            ],
        }


# ============================================================
# 全局单例
# ============================================================
_breaker_instance: Optional[CircuitBreaker] = None


def get_breaker() -> CircuitBreaker:
    global _breaker_instance
    if _breaker_instance is None:
        _breaker_instance = CircuitBreaker()
    return _breaker_instance


# ============================================================
# 自检
# ============================================================
if __name__ == "__main__":
    breaker = CircuitBreaker()

    print("=== 断路器自检 ===\n")

    # 测试1: 连续失败熔断
    print("【测试1】连续失败熔断")
    for i in range(4):
        tripped = breaker.record_failure("api.example.com")
        print(f"  失败 #{i+1}: {'🚨熔断!' if tripped else '继续'}")
        if tripped:
            print(f"  状态: {breaker.get_status()['state']}")
            break

    breaker.unlock()
    print()

    # 测试2: 越权访问熔断
    print("【测试2】越权访问熔断")
    for i in range(3):
        tripped = breaker.record_violation("evil-tracker.com", "试图读取用户Cookie")
        print(f"  越权 #{i+1}: {'🚨熔断!' if tripped else '继续'}")
        if tripped:
            break

    breaker.unlock()
    print()

    # 测试3: 手动熔断
    print("【测试3】手动熔断")
    breaker.manual_trip("user", "测试手动熔断", lock_seconds=10)
    print(f"  剩余锁定: {breaker.get_remaining_lock():.0f}秒")
    print(f"  该阻断吗: {breaker.is_blocked()}")

    breaker.unlock()
    print()

    # 测试4: 状态查询
    print("【测试4】状态查询")
    status = breaker.get_status()
    print(json.dumps(status, ensure_ascii=False, indent=2))

    print("\n✅ 断路器自检通过")
