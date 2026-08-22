# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-c571c60e
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""🐉 龍魂流控模块 v1.2 · v1.1设计修正实装版
新增：租户级配置解析 / degrade 60秒自动恢复 / update_config桶余量迁移 / 审计采样
"""
import time, threading, logging
from typing import Optional, Dict

logger = logging.getLogger('longhun.flow_control')

class TokenBucket:
    def __init__(self, tokens_per_second=100.0, burst_size=20):
        self.tokens_per_second = tokens_per_second
        self.burst_size = burst_size
        self._tokens = burst_size
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()
    def _refill(self):
        now = time.monotonic(); el = now - self._last_refill
        if el > 0:
            self._tokens = min(self.burst_size, self._tokens + el * self.tokens_per_second)
            self._last_refill = now
    def consume(self, tokens=1):
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens; return True
            return False
    def wait_and_consume(self, tokens=1, timeout=None):
        start = time.monotonic()
        while True:
            if self.consume(tokens): return True
            if timeout is not None and (time.monotonic()-start) > timeout: return False
            time.sleep(0.001)
    def 余量(self):
        with self._lock: self._refill(); return self._tokens

class RateLimitConfig:
    def __init__(self, enabled=True, tokens_per_second=100.0, burst_size=20,
                 timeout=5.0, fallback_action="block", audit_logging=True, audit_sample=0.01):
        self.enabled=enabled; self.tokens_per_second=tokens_per_second
        self.burst_size=burst_size; self.timeout=timeout
        self.fallback_action=fallback_action; self.audit_logging=audit_logging
        self.audit_sample=audit_sample   # v1.2: allowed事件采样率，blocked/timeout恒100%

class RateLimiterPlugin:
    """v1.2：租户解析 + 降级自动恢复 + 桶迁移 + 审计采样"""
    def __init__(self, config=None, 租户配置=None):
        self.config = config or RateLimitConfig()
        self.租户配置 = 租户配置 or {}     # {"vip-*": RateLimitConfig(...), "admin": ...}
        self._buckets: Dict[str, TokenBucket] = {}
        self._session_cfg: Dict[str, RateLimitConfig] = {}
        self._degrade_until: Dict[str, float] = {}   # v1.2: 降级到期时间
        self._stats = {}
        self._audit_log = []
        self._lock = threading.Lock()
        import random; self._rand = random.random

    # ---- v1.2 新增：租户级配置解析（tenants > scenes > default 的 tenants 段实装）----
    def _解析租户配置(self, session_id):
        if session_id in self._session_cfg: return self._session_cfg[session_id]
        import fnmatch
        cfg = self.config
        for 模式, c in self.租户配置.items():
            if fnmatch.fnmatch(session_id, 模式): cfg = c; break
        self._session_cfg[session_id] = cfg
        return cfg

    def _get_bucket(self, session_id):
        cfg = self._解析租户配置(session_id)
        with self._lock:
            if session_id not in self._buckets:
                self._buckets[session_id] = TokenBucket(cfg.tokens_per_second, cfg.burst_size)
            # v1.2: 降级到期自动恢复
            if session_id in self._degrade_until and time.time() > self._degrade_until[session_id]:
                b = self._buckets[session_id]
                b.tokens_per_second = cfg.tokens_per_second
                del self._degrade_until[session_id]
                self._audit(session_id, "recover", "降级到期·速率自动还原", True)
            return self._buckets[session_id]

    def _audit(self, session_id, action, result, 重要=False):
        if not self.config.audit_logging: return
        if not 重要 and self._rand() > self.config.audit_sample: return  # v1.2: 采样
        self._audit_log.append({"时间": time.time(), "会话": session_id, "动作": action, "结果": result})

    def _st(self, sid, k, v=1):
        self._stats.setdefault(sid, {"consumed":0,"blocked":0,"timeouts":0})
        self._stats[sid][k] = self._stats[sid].get(k,0)+v

    def check(self, session_id, tokens=1):
        if not self.config.enabled: return True
        ok = self._get_bucket(session_id).consume(tokens)
        self._st(session_id, "consumed" if ok else "blocked")
        self._audit(session_id, "check", "allowed" if ok else "blocked", 重要=not ok)
        return ok

    def wait_and_check(self, session_id, tokens=1, timeout=None):
        if not self.config.enabled: return True
        cfg = self._解析租户配置(session_id)
        eff = cfg.timeout if timeout is None else timeout
        bucket = self._get_bucket(session_id)
        ok = bucket.wait_and_consume(tokens, timeout=eff)
        self._st(session_id, "consumed" if ok else "timeouts")
        if not ok:
            self._audit(session_id, "wait", "timeout", 重要=True)
            if cfg.fallback_action == "passthrough": return True
            if cfg.fallback_action == "degrade":
                bucket.tokens_per_second = cfg.tokens_per_second * 0.5
                self._degrade_until[session_id] = time.time() + 60   # v1.2: 60s自动恢复
                self._audit(session_id, "degrade", "限速50%·60秒后自动还原", 重要=True)
                return bucket.wait_and_consume(tokens, timeout=eff)
        else:
            self._audit(session_id, "wait", "allowed")
        return ok

    # ---- v1.2 修正：update_config 桶余量按比例迁移，不再清空在途会话 ----
    def update_config(self, 新config):
        旧 = self.config; self.config = 新config; self._session_cfg.clear()
        with self._lock:
            for sid, b in self._buckets.items():
                if 旧.burst_size > 0:
                    比例 = b._tokens / 旧.burst_size
                    b.burst_size = 新config.burst_size
                    b.tokens_per_second = 新config.tokens_per_second
                    b._tokens = min(b.burst_size, 比例 * b.burst_size)
        self._audit("system", "config_update", "桶余量已按比例迁移", 重要=True)

    def 统计(self, sid=None):
        return self._stats.get(sid, self._stats)
    def 审计日志(self, n=20):
        return self._audit_log[-n:]
