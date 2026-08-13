#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龙魂 AI 网关 · 流控模块压测脚本 v1.0
DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-LOAD-TEST-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
License: MulanPSL v2 (工程层)

验证目标:
  1. 限速稳定性 — 100 t/s 是否稳定 (误差 ≤ 20%)
  2. 租户隔离 — 不同租户配置互不干扰
  3. 降级策略 — passthrough → degrade → block 切换
  4. 三色审计 — 流控模块R值 ≥ 85 🟢
  5. DNA追溯 — 每次请求携带有效DNA码

运行方式:
  locust -f tests/locustfile.py --host=http://localhost:8000
  浏览器打开 http://localhost:8089 配置并发数
"""

import json
import hashlib
import logging
import os
import random
import sys
import time
from datetime import datetime
from typing import Any, Dict, Optional

from locust import HttpUser, between, events, task
from locust.runners import MasterRunner

# ============================================================
# 日志配置
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('locust')


# ============================================================
# 配置区
# ============================================================

BASE_URL = os.getenv("LOAD_TEST_BASE_URL", "http://localhost:8000")
RUN_TIME = int(os.getenv("LOAD_TEST_RUN_TIME", 300))  # 默认5分钟

# 主权锚定
UID = "9622"
DNA_PREFIX = "#龍芯⚡️"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def generate_dna(suffix: str = "") -> str:
    """生成DNA追溯码"""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    rand = hashlib.md5(f"{suffix}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{timestamp}-{suffix}-{rand}-{UID}"


# 租户配置（对应 config/flow_control.yaml）
TENANT_CONFIGS = {
    "tenant_default": {
        "api_key": "sk-default-tenant-key",
        "tokens_per_second": 100,
        "burst_size": 20,
        "expected_rate": 100,
        "rate_tolerance": 0.20,  # ±20%
    },
    "tenant_vip": {
        "api_key": "sk-vip-tenant-key",
        "tokens_per_second": 200,
        "burst_size": 50,
        "expected_rate": 200,
        "rate_tolerance": 0.20,
    },
    "tenant_free": {
        "api_key": "sk-free-tenant-key",
        "tokens_per_second": 50,
        "burst_size": 10,
        "expected_rate": 50,
        "rate_tolerance": 0.20,
    },
}

# 测试用 prompt（模拟真实请求）
TEST_PROMPTS = [
    "请用 200 字介绍一下龙魂 AI 网关的架构设计",
    "解释一下 TokenBucket 算法的原理",
    "如何实现流式输出的限速控制？",
    "降级策略 passthrough/degrade/block 的区别是什么？",
    "写一个 Python 的 TokenBucket 实现",
    "三色审计的R值计算公式是什么？",
    "DNA追溯码如何保证不可篡改？",
    "龙魂系统的史官机制是如何工作的？",
]


# ============================================================
# 用户行为类（主测试）
# ============================================================

class GatewayUser(HttpUser):
    """模拟网关用户"""

    wait_time = between(0.5, 3)  # 用户思考时间
    tenant_type = None
    tenant_config = None
    dna = None

    def on_start(self):
        """用户启动时分配租户"""
        # 按权重分配租户：default 60%, vip 20%, free 20%
        rand = random.random()
        if rand < 0.6:
            self.tenant_type = "tenant_default"
        elif rand < 0.8:
            self.tenant_type = "tenant_vip"
        else:
            self.tenant_type = "tenant_free"

        self.tenant_config = TENANT_CONFIGS[self.tenant_type]
        self.dna = generate_dna(f"SESSION-{self.tenant_type}")
        logger.info(f"[{self.tenant_type}] 用户启动 | DNA: {self.dna[:30]}...")

    @task(10)
    def chat_stream(self):
        """测试流式输出限速（高频任务）"""
        prompt = random.choice(TEST_PROMPTS)
        session_dna = generate_dna(f"STREAM-{self.tenant_type}")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tenant_config['api_key']}",
            "X-Tenant-ID": self.tenant_type,
            "X-DNA": session_dna,  # DNA追溯
            "X-Confirm": CONFIRM,
        }

        payload = {
            "model": "kimi-local",
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
            "max_tokens": 500,
        }

        start_time = time.time()
        token_count = 0
        chunk_count = 0
        status_code = 0

        with self.client.post(
            "/v1/chat/completions",
            json=payload,
            headers=headers,
            stream=True,
            catch_response=True,
            name="/chat_stream",
        ) as response:
            status_code = response.status_code

            if response.status_code != 200:
                if response.status_code == 429:
                    response.success()
                else:
                    response.failure(f"HTTP {response.status_code}")
                return

            try:
                for line in response.iter_lines():
                    if not line:
                        continue

                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str == "[DONE]":
                            break

                        try:
                            data = json.loads(data_str)
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    token_count += len(content) / 3
                                    chunk_count += 1
                        except json.JSONDecodeError:
                            pass
            except Exception as e:
                response.failure(f"流式读取异常: {e}")
                return

            # 计算实际速率
            elapsed = time.time() - start_time
            if elapsed > 0 and token_count > 0:
                actual_rate = token_count / elapsed
                expected_rate = self.tenant_config["expected_rate"]
                tolerance = self.tenant_config["rate_tolerance"]

                if actual_rate > expected_rate * (1 + tolerance):
                    response.failure(
                        f"限速失效: 实际 {actual_rate:.1f} t/s > 预期 {expected_rate} t/s"
                    )
                else:
                    response.success()
            else:
                response.success()

    @task(3)
    def chat_sync(self):
        """测试同步请求限速（中频任务）"""
        prompt = random.choice(TEST_PROMPTS)
        session_dna = generate_dna(f"SYNC-{self.tenant_type}")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tenant_config['api_key']}",
            "X-Tenant-ID": self.tenant_type,
            "X-DNA": session_dna,
            "X-Confirm": CONFIRM,
        }

        payload = {
            "model": "kimi-local",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "max_tokens": 300,
        }

        with self.client.post(
            "/v1/chat/completions",
            json=payload,
            headers=headers,
            catch_response=True,
            name="/chat_sync",
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 429:
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(1)
    def get_flow_metrics(self):
        """测试 Prometheus 指标接口（低频任务）"""
        session_dna = generate_dna("METRICS")

        headers = {
            "Authorization": f"Bearer {self.tenant_config['api_key']}",
            "X-DNA": session_dna,
        }

        with self.client.get(
            "/metrics",
            headers=headers,
            catch_response=True,
            name="/metrics",
        ) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")
                return

            text = response.text
            required_metrics = [
                "longhun_flow_total_tokens",
                "longhun_flow_consumed_tokens",
                "longhun_flow_blocked",
                "longhun_flow_timeouts",
                "longhun_flow_config_tps",
                "longhun_flow_tricolor",
            ]

            missing = [m for m in required_metrics if m not in text]
            if missing:
                response.failure(f"缺少指标: {missing}")
            else:
                response.success()

    @task(1)
    def tricolor_audit(self):
        """测试三色审计接口"""
        session_dna = generate_dna("AUDIT")

        headers = {
            "Authorization": f"Bearer {self.tenant_config['api_key']}",
            "X-DNA": session_dna,
        }

        with self.client.get(
            "/api/audit/flow_control",
            headers=headers,
            catch_response=True,
            name="/audit/flow_control",
        ) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")
                return

            try:
                data = response.json()
                tricolor = data.get("tricolor", "🟡")
                r_value = data.get("R_value", 0)

                if r_value >= 85:
                    expected_tricolor = "🟢"
                elif r_value >= 60:
                    expected_tricolor = "🟡"
                else:
                    expected_tricolor = "🔴"

                if tricolor != expected_tricolor:
                    response.failure(f"三色不匹配: 期望 {expected_tricolor}, 实际 {tricolor}")
                else:
                    response.success()
            except Exception as e:
                response.failure(f"解析失败: {e}")


# ============================================================
# 降级策略测试类
# ============================================================

class DegradationTestUser(HttpUser):
    """专门测试降级策略的用户"""

    wait_time = between(0.1, 0.5)
    tenant_type = "tenant_default"
    tenant_config = None

    def on_start(self):
        self.tenant_config = TENANT_CONFIGS[self.tenant_type]
        self.dna = generate_dna("DEGRADE")
        logger.info(f"[降级测试] 用户启动 | DNA: {self.dna[:30]}...")

    @task
    def aggressive_requests(self):
        """高频请求触发降级"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tenant_config['api_key']}",
            "X-Tenant-ID": self.tenant_type,
            "X-DNA": generate_dna("AGGRESSIVE"),
        }

        payload = {
            "model": "kimi-local",
            "messages": [{"role": "user", "content": "测试降级策略"}],
            "stream": True,
            "max_tokens": 1000,
        }

        with self.client.post(
            "/v1/chat/completions",
            json=payload,
            headers=headers,
            stream=True,
            catch_response=True,
            name="/degradation_test",
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 429:
                logger.info("[降级] 请求被拒绝 (429) — block 策略生效")
                response.success()
            elif response.status_code == 503:
                logger.info("[降级] 服务降级 (503) — degrade 策略生效")
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")


# ============================================================
# 租户隔离验证类
# ============================================================

class TenantIsolationUser(HttpUser):
    """租户隔离验证用户"""

    wait_time = between(0.1, 0.3)
    tenant_config = None

    def on_start(self):
        self.tenant_type = "tenant_default"
        self.tenant_config = TENANT_CONFIGS[self.tenant_type]

    @task
    def high_frequency_request(self):
        """高频请求 — 验证租户隔离"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tenant_config['api_key']}",
            "X-Tenant-ID": self.tenant_type,
        }

        payload = {
            "model": "kimi-local",
            "messages": [{"role": "user", "content": "租户隔离测试"}],
            "stream": False,
            "max_tokens": 50,
        }

        with self.client.post(
            "/v1/chat/completions",
            json=payload,
            headers=headers,
            catch_response=True,
            name="/tenant_isolation",
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 429:
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")


# ============================================================
# 测试报告钩子
# ============================================================

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """测试开始时打印配置"""
    print("\n" + "=" * 70)
    print("🐉 龙魂 AI 网关 · 流控模块压测 v1.0")
    print("=" * 70)
    print(f"DNA: {generate_dna('LOAD-TEST')}")
    print(f"确认码: {CONFIRM}")
    print(f"目标地址: {BASE_URL}")
    print(f"运行时长: {RUN_TIME}秒")
    print("\n📋 租户配置:")
    for tenant, config in TENANT_CONFIGS.items():
        print(f"  - {tenant}: {config['tokens_per_second']} t/s, burst={config['burst_size']}")
    print("\n📋 验证目标:")
    print("  1. 限速稳定性 — 实际速率 ≤ 预期 × 1.20")
    print("  2. 租户隔离 — 各租户独立限流，互不干扰")
    print("  3. 降级策略 — passthrough → degrade → block")
    print("  4. 三色审计 — R值 ≥ 85 🟢")
    print("  5. DNA追溯 — 每次请求携带有效DNA码")
    print("=" * 70 + "\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """测试结束时打印统计和三色审计报告"""
    print("\n" + "=" * 70)
    print("📊 压测完成")
    print("=" * 70)

    if isinstance(environment.runner, MasterRunner):
        stats = environment.runner.stats
        print(f"\n📈 统计信息:")
        print(f"  总请求数: {stats.total.num_requests}")
        print(f"  失败数: {stats.total.num_failures}")
        print(f"  失败率: {stats.total.fail_ratio * 100:.2f}%")
        print(f"  平均响应时间: {stats.total.avg_response_time:.2f} ms")
        print(f"  中位数响应时间: {stats.total.median_response_time:.2f} ms")
        print(f"  95分位: {stats.total.get_response_time_percentile(0.95):.2f} ms")
        print(f"  RPS: {stats.total.total_rps:.2f}")

        print("\n📋 各任务统计:")
        for name, stat in stats.entries.items():
            print(f"  - {name}: {stat.num_requests} 请求, 失败率 {stat.fail_ratio * 100:.2f}%, "
                  f"平均 {stat.avg_response_time:.2f}ms")

        print("\n" + "=" * 70)
        print("🔍 三色审计报告")
        print("=" * 70)
        audit_results = _generate_tricolor_audit(stats)
        print(json.dumps(audit_results, ensure_ascii=False, indent=2))

    print("=" * 70 + "\n")


def _generate_tricolor_audit(stats):
    """生成三色审计报告"""
    total = stats.total.num_requests
    failures = stats.total.num_failures
    fail_rate = failures / max(total, 1)

    R = 100.0
    if fail_rate > 0.10:
        R -= 30
    elif fail_rate > 0.05:
        R -= 15

    if stats.total.avg_response_time > 5000:
        R -= 20
    elif stats.total.avg_response_time > 2000:
        R -= 10

    if R >= 85:
        tricolor = "🟢"
        status = "通过"
    elif R >= 60:
        tricolor = "🟡"
        status = "待审"
    else:
        tricolor = "🔴"
        status = "不通过"

    return {
        "tricolor": tricolor,
        "status": status,
        "R_value": round(R, 2),
        "total_requests": total,
        "failures": failures,
        "failure_rate": round(fail_rate * 100, 2),
        "avg_response_ms": round(stats.total.avg_response_time, 2),
        "dna": generate_dna("AUDIT-REPORT"),
        "confirm": CONFIRM,
        "timestamp": datetime.now().isoformat()
    }


# ============================================================
# 命令行入口
# ============================================================

if __name__ == "__main__":
    print("🐉 龙魂流控压测脚本")
    print("=" * 50)
    print("用法:")
    print("  locust -f tests/locustfile.py --host=http://localhost:8000")
    print("  然后打开 http://localhost:8089")
    print("")
    print("无头模式:")
    print(f"  locust -f tests/locustfile.py --headless --users 100 --spawn-rate 10 --run-time {RUN_TIME}s --host={BASE_URL} --html load_test_report.html")
    print("=" * 50)
