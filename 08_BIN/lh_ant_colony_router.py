#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·ANT-COLONY-ROUTER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂蚁群触角 · 模型路由引擎 v1.0
Ant Colony Router — 国产优先 · 权重轮询 · 熔断降级 · 审计留痕

DNA: #龍芯⚡️丙午·辛未·ANT-COLONY-ROUTER-v1.0

用法:
  python3 bin/lh_ant_colony_router.py --prompt "分析台海局势" --persona military
  python3 bin/lh_ant_colony_router.py --prompt "技术方案" --dry-run
  python3 bin/lh_ant_colony_router.py --health          # 健康检查所有节点
  python3 bin/lh_ant_colony_router.py --stats           # 路由统计
  python3 bin/lh_ant_colony_router.py --serve --port 9688  # HTTP服务模式
"""

import sys
import os
import json
import time
import hashlib
import hmac
import argparse
import asyncio
import logging
from pathlib import Path
from datetime import datetime, timezone, timedelta
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DNA = "#龍芯⚡️丙午·辛未·ANT-COLONY-ROUTER-v1.0"
CST = timezone(timedelta(hours=8))

LOG_DIR = ROOT / "logs" / "antenna"
LOG_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOG = LOG_DIR / "access.jsonl"

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "router.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("ant_colony_router")


# ============================================================
# 枚举与数据类
# ============================================================

class NodeType(Enum):
    DOMESTIC = "domestic_base"
    OPEN_SOURCE = "open_source"
    LOCAL = "local_deploy"
    FUSE = "circuit_breaker"

class NodeStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"       # 性能下降但可用
    UNHEALTHY = "unhealthy"
    FUSED = "fused"             # 已熔断
    HALF_OPEN = "half_open"


@dataclass
class AntennaNode:
    id: str
    name: str
    node_type: NodeType
    endpoint: str
    priority: int
    auth_config: Dict[str, str] = field(default_factory=dict)
    fallback_id: Optional[str] = None
    weight: int = 50
    max_concurrent: int = 4
    timeout_ms: int = 15000
    domestic: bool = True

    # 运行时状态
    status: NodeStatus = NodeStatus.HEALTHY
    fail_count: int = 0
    success_count: int = 0
    last_check: float = 0.0
    last_latency_ms: float = 0.0
    fused_at: float = 0.0

    @property
    def healthy(self) -> bool:
        return self.status in (NodeStatus.HEALTHY, NodeStatus.DEGRADED, NodeStatus.HALF_OPEN)


# ============================================================
# 模型路由引擎
# ============================================================

class CircuitBreaker:
    """熔断器"""

    FAILURE_THRESHOLD = 5
    RECOVERY_TIMEOUT = 300       # 5分钟
    HALF_OPEN_MAX = 3
    SLOW_CALL_THRESHOLD_MS = 10000

    def __init__(self):
        self._half_open_calls = defaultdict(int)

    def should_break(self, node: AntennaNode) -> bool:
        """判断是否应该熔断"""
        if node.status == NodeStatus.FUSED:
            elapsed = time.time() - node.fused_at
            if elapsed >= self.RECOVERY_TIMEOUT:
                node.status = NodeStatus.HALF_OPEN
                self._half_open_calls[node.id] = 0
                log.info(f"[CB] {node.id} 进入半开状态")
                return False
            return True
        return False

    def on_success(self, node: AntennaNode):
        """成功回调"""
        node.success_count += 1
        if node.status == NodeStatus.HALF_OPEN:
            self._half_open_calls[node.id] += 1
            if self._half_open_calls[node.id] >= self.HALF_OPEN_MAX:
                node.status = NodeStatus.HEALTHY
                node.fail_count = 0
                log.info(f"[CB] {node.id} 恢复健康")
        else:
            node.fail_count = max(0, node.fail_count - 1)

    def on_failure(self, node: AntennaNode, latency_ms: float = 0):
        """失败回调"""
        node.fail_count += 1
        node.last_latency_ms = latency_ms

        if latency_ms > self.SLOW_CALL_THRESHOLD_MS:
            node.status = NodeStatus.DEGRADED
            log.warning(f"[CB] {node.id} 慢调用 {latency_ms}ms")

        if node.fail_count >= self.FAILURE_THRESHOLD:
            node.status = NodeStatus.FUSED
            node.fused_at = time.time()
            log.error(f"[CB] {node.id} 熔断! 连续失败 {node.fail_count} 次")


class RouterStats:
    """路由统计"""

    def __init__(self):
        self.total_requests = 0
        self.success_requests = 0
        self.failed_requests = 0
        self.fused_requests = 0
        self.node_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "requests": 0, "success": 0, "fail": 0,
            "total_latency_ms": 0, "avg_latency_ms": 0
        })
        self.start_time = time.time()

    def record(self, node_id: str, success: bool, latency_ms: float):
        self.total_requests += 1
        if success:
            self.success_requests += 1
        else:
            self.failed_requests += 1

        s = self.node_stats[node_id]
        s["requests"] += 1
        if success:
            s["success"] += 1
        else:
            s["fail"] += 1
        s["total_latency_ms"] += latency_ms
        s["avg_latency_ms"] = s["total_latency_ms"] / s["requests"]

    def summary(self) -> Dict[str, Any]:
        uptime = time.time() - self.start_time
        return {
            "uptime_seconds": round(uptime, 1),
            "total_requests": self.total_requests,
            "success": self.success_requests,
            "failed": self.failed_requests,
            "fused": self.fused_requests,
            "success_rate": round(self.success_requests / max(1, self.total_requests) * 100, 1),
            "nodes": dict(self.node_stats),
        }


class LongHunRouter:
    """龍魂蚁群触角 · 模型路由引擎"""

    DNA_ANCHOR = DNA
    UID = "9622"

    def __init__(self, config_path: Optional[str] = None):
        self.nodes: List[AntennaNode] = []
        self.circuit_breaker = CircuitBreaker()
        self.stats = RouterStats()
        self._load_default_nodes()

    def _load_default_nodes(self):
        """加载默认触角节点（国产优先）"""
        self.nodes = [
            AntennaNode("CN-1", "华为盘古", NodeType.DOMESTIC,
                        "https://pangu.huaweicloud.com/v1", 1,
                        {"ak": "", "sk": ""}, "CN-2", weight=100, max_concurrent=8),
            AntennaNode("CN-2", "阿里通义", NodeType.DOMESTIC,
                        "https://dashscope.aliyuncs.com/api/v1", 2,
                        {"api_key": ""}, "CN-3", weight=90, max_concurrent=8),
            AntennaNode("CN-3", "百度文心", NodeType.DOMESTIC,
                        "https://aip.baidubce.com/rpc/2.0/ai_custom/v1", 3,
                        {"client_id": "", "client_secret": ""}, "CN-4", weight=80, max_concurrent=6),
            AntennaNode("CN-4", "讯飞星火", NodeType.DOMESTIC,
                        "https://spark-api-open.xf-yun.com/v1", 4,
                        {"app_id": "", "api_secret": "", "api_key": ""}, "OS-1", weight=70, max_concurrent=6),
            AntennaNode("OS-1", "DeepSeek-V3", NodeType.OPEN_SOURCE,
                        "https://api.deepseek.com/v1", 5,
                        {"api_key": ""}, "OS-2", weight=60, max_concurrent=4),
            AntennaNode("OS-2", "Qwen-本地", NodeType.LOCAL,
                        "http://localhost:8000/v1", 6,
                        {}, "OS-3", weight=50, max_concurrent=4),
            AntennaNode("OS-3", "Llama3-本地", NodeType.LOCAL,
                        "http://localhost:8001/v1", 7,
                        {}, None, weight=30, max_concurrent=2, domestic=False),
        ]

    def sign_request(self, payload: str, persona: str = "military") -> Dict[str, str]:
        """生成签名请求头"""
        ts = str(int(time.time()))
        nonce = hashlib.sha256(f"{ts}{self.UID}{payload}".encode()).hexdigest()[:16]
        sig_raw = f"{self.DNA_ANCHOR}{ts}{nonce}{payload}"
        try:
            sig = hashlib.new("sm3", sig_raw.encode()).hexdigest()
        except (ValueError, AttributeError):
            sig = hashlib.sha256(sig_raw.encode()).hexdigest()

        return {
            "X-Longhun-UID": self.UID,
            "X-Longhun-DNA": self.DNA_ANCHOR,
            "X-Longhun-Persona": persona,
            "X-Longhun-Timestamp": ts,
            "X-Longhun-Nonce": nonce,
            "X-Longhun-Signature": sig,
            "Content-Type": "application/json",
        }

    def _select_node(self) -> Optional[AntennaNode]:
        """选择路由节点：国产优先 + 权重轮询"""
        # 过滤：健康 + 非熔断
        candidates: list[AntennaNode] = [
            n for n in self.nodes
            if n.node_type != NodeType.FUSE
            and n.healthy
            and not self.circuit_breaker.should_break(n)
        ]

        if not candidates:
            return None

        # 国产优先：国产节点全部失败才降级
        domestic_nodes = [n for n in candidates if n.domestic]
        if domestic_nodes:
            candidates = domestic_nodes
            log.debug(f"国产优先: {len(candidates)} 节点可用")
        else:
            log.warning("国产节点全部不可用，降级至非国产节点")

        # 权重排序
        candidates.sort(key=lambda n: (-n.weight, n.priority))
        # 简单权重轮询：选权重最高且失败最少的
        best = min(candidates, key=lambda n: (n.fail_count, -n.weight))
        return best

    async def _health_check_node(self, node: AntennaNode):
        """单节点健康检查"""
        if node.node_type == NodeType.FUSE or node.node_type == NodeType.LOCAL:
            return
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{node.endpoint}/health",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as resp:
                    if resp.status == 200:
                        node.status = NodeStatus.HEALTHY
                        node.last_check = time.time()
                    else:
                        node.status = NodeStatus.DEGRADED
        except Exception:
            node.status = NodeStatus.UNHEALTHY
            node.fail_count += 1

    async def health_check_all(self) -> List[Dict[str, Any]]:
        """健康检查所有节点"""
        tasks = [self._health_check_node(n) for n in self.nodes]
        await asyncio.gather(*tasks, return_exceptions=True)

        results = []
        for n in self.nodes:
            results.append({
                "id": n.id, "name": n.name,
                "type": n.node_type.value,
                "status": n.status.value,
                "domestic": n.domestic,
                "fail_count": n.fail_count,
                "last_latency_ms": n.last_latency_ms,
                "weight": n.weight,
            })
        return results

    async def route(self, prompt: str, persona: str = "military",
                    model: str = "default", dry_run: bool = False) -> Dict[str, Any]:
        """主路由方法"""

        # 1. 选择节点
        node = self._select_node()

        if node is None:
            self.stats.fused_requests += 1
            return {
                "status": "FUSE",
                "node": "FUSE",
                "message": "龍魂网络暂时离线，所有触角不可达。请稍后重试。UID9622",
                "dna": self.DNA_ANCHOR,
                "latency_ms": 0,
            }

        # 2. Dry-run 模式
        if dry_run:
            return {
                "status": "DRY_RUN",
                "node": node.name,
                "node_id": node.id,
                "node_type": node.node_type.value,
                "domestic": node.domestic,
                "persona": persona,
                "prompt_length": len(prompt),
                "dna": self.DNA_ANCHOR,
                "message": f"路由至 {node.name} (dry-run)",
            }

        # 3. 签名与请求头
        headers = self.sign_request(prompt, persona)

        # 4. 执行请求
        start_time = time.time()
        try:
            import aiohttp
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{node.endpoint}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=node.timeout_ms / 1000)
                ) as resp:
                    latency_ms = (time.time() - start_time) * 1000
                    node.last_latency_ms = latency_ms

                    if resp.status == 200:
                        result = await resp.json()
                        self.circuit_breaker.on_success(node)
                        self.stats.record(node.id, True, latency_ms)
                        self._audit_log(node, latency_ms, len(prompt), persona, "success")

                        return {
                            "status": "OK",
                            "node": node.name,
                            "node_id": node.id,
                            "node_type": node.node_type.value,
                            "domestic": node.domestic,
                            "latency_ms": round(latency_ms, 2),
                            "persona": persona,
                            "response": result,
                            "dna": self.DNA_ANCHOR,
                        }
                    else:
                        error_text = await resp.text()
                        raise Exception(f"HTTP {resp.status}: {error_text[:200]}")

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            self.circuit_breaker.on_failure(node, latency_ms)
            self.stats.record(node.id, False, latency_ms)
            self._audit_log(node, latency_ms, len(prompt), persona, "fail", str(e)[:200])
            log.error(f"[ROUTE] {node.id} 请求失败: {e}")

            # 递归降级
            if node.fallback_id:
                fallback = next((n for n in self.nodes if n.id == node.fallback_id), None)
                if fallback and fallback.healthy and not self.circuit_breaker.should_break(fallback):
                    log.info(f"[ROUTE] 降级: {node.id} → {fallback.id}")
                    return await self._route_direct(fallback, prompt, persona, model, headers)

            return {
                "status": "ERROR",
                "node": node.name,
                "node_id": node.id,
                "error": str(e)[:500],
                "fallback_triggered": True,
                "dna": self.DNA_ANCHOR,
                "latency_ms": round(latency_ms, 2),
            }

    async def _route_direct(self, node: AntennaNode, prompt: str,
                            persona: str, model: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """直接路由到指定节点（降级）"""
        start_time = time.time()
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{node.endpoint}/chat/completions",
                    headers=headers,
                    json={"model": model, "messages": [{"role": "user", "content": prompt}]},
                    timeout=aiohttp.ClientTimeout(total=node.timeout_ms / 1000)
                ) as resp:
                    latency_ms = (time.time() - start_time) * 1000
                    node.last_latency_ms = latency_ms

                    if resp.status == 200:
                        result = await resp.json()
                        self.circuit_breaker.on_success(node)
                        self.stats.record(node.id, True, latency_ms)
                        self._audit_log(node, latency_ms, len(prompt), persona, "success")

                        return {
                            "status": "OK",
                            "node": node.name,
                            "node_id": node.id,
                            "node_type": node.node_type.value,
                            "domestic": node.domestic,
                            "latency_ms": round(latency_ms, 2),
                            "persona": persona,
                            "response": result,
                            "dna": self.DNA_ANCHOR,
                            "degraded": True,
                        }
                    else:
                        raise Exception(f"HTTP {resp.status}")
        except Exception as e:
            return {
                "status": "ERROR",
                "node": node.name,
                "error": str(e)[:200],
                "dna": self.DNA_ANCHOR,
            }

    def _audit_log(self, node: AntennaNode, latency_ms: float,
                   tokens: int, persona: str, status: str, error: str = ""):
        """审计日志写入"""
        entry = {
            "timestamp": datetime.now(CST).isoformat(),
            "uid_hash": hashlib.sha256(self.UID.encode()).hexdigest()[:16],
            "node_id": node.id,
            "node_name": node.name,
            "node_type": node.node_type.value,
            "domestic_flag": node.domestic,
            "latency_ms": round(latency_ms, 2),
            "token_count_input": tokens,
            "persona": persona,
            "status": status,
            "error": error,
            "dna": self.DNA_ANCHOR,
        }
        with open(AUDIT_LOG, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ============================================================
# CLI
# ============================================================

async def async_main():
    parser = argparse.ArgumentParser(
        description="龍魂蚁群触角 · 模型路由引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--prompt", type=str, help="路由的提示词")
    parser.add_argument("--persona", type=str, default="military",
                        choices=["military", "history", "philosophy", "economy", "legal", "general"],
                        help="人格选择")
    parser.add_argument("--dry-run", action="store_true", help="仅显示路由决策，不实际调用")
    parser.add_argument("--health", action="store_true", help="健康检查所有节点")
    parser.add_argument("--stats", action="store_true", help="路由统计")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--dna", type=str, default=DNA, help="DNA追溯码")

    args = parser.parse_args()
    router = LongHunRouter()

    if args.health:
        results = await router.health_check_all()
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print("=" * 70)
            print("  龍魂蚁群触角 · 健康检查")
            print("=" * 70)
            for r in results:
                status_icon = {"healthy": "🟢", "degraded": "🟡", "unhealthy": "🔴", "fused": "⛔"}.get(r["status"], "❓")
                domestic = "🇨🇳" if r["domestic"] else "🌐"
                print(f"  {status_icon} {domestic} {r['id']:6s} {r['name']:12s} [{r['type']:15s}] "
                      f"权重:{r['weight']:3d} 失败:{r['fail_count']}")
            print("=" * 70)
        return

    if args.stats:
        summary = router.stats.summary()
        if args.json:
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        else:
            print("=" * 70)
            print("  龍魂蚁群触角 · 路由统计")
            print("=" * 70)
            print(f"  运行时间: {summary['uptime_seconds']}秒")
            print(f"  总请求: {summary['total_requests']}")
            print(f"  成功: {summary['success']} | 失败: {summary['failed']} | 熔断: {summary['fused']}")
            print(f"  成功率: {summary['success_rate']}%")
            print("-" * 70)
            for nid, ns in summary.get("nodes", {}).items():
                print(f"  {nid:6s}: {ns['requests']:4d}请求 "
                      f"成功{ns['success']} 失败{ns['fail']} "
                      f"平均{ns['avg_latency_ms']:.0f}ms")
            print("=" * 70)
        return

    if args.prompt:
        result = await router.route(args.prompt, persona=args.persona, dry_run=args.dry_run)
        if args.json:
            # 去掉response体（太长）
            if "response" in result:
                del result["response"]
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"状态: {result['status']}")
            print(f"节点: {result.get('node', 'N/A')}")
            print(f"国产: {result.get('domestic', 'N/A')}")
            print(f"延迟: {result.get('latency_ms', 'N/A')}ms")
            print(f"DNA: {result['dna']}")
        return

    parser.print_help()


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
