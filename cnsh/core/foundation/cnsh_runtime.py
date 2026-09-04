#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 CNSH 运行时引擎
回执 + 回调 + 路由

DNA: #龍芯⚡️丙午·丙申·辛酉·庚寅·䷥睽-RUNTIME-UID9622
"""

import asyncio
import hashlib
import threading
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def generate_dna(module: str = "RUNTIME") -> str:
    now = datetime.now()
    h = hashlib.md5(f"{module}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{now.strftime('%Y-%m-%d')}-{module}-{h}-{UID}"


# ============================================================
# 回执 (Receipt)
# ============================================================

@dataclass
class ExecutionReceipt:
    """执行回执"""

    receipt_id: str
    dna: str
    function_name: str
    args: Dict[str, Any]
    result: Any
    status: str  # success, failed, pending
    timestamp: str
    duration_ms: float
    signature: str = ""
    callback_url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return asdict(self)

    def sign(self) -> str:
        """模拟GPG签名（实际可接入GPG）"""
        data = f"{self.receipt_id}{self.dna}{self.result}{self.timestamp}"
        self.signature = hashlib.sha256(data.encode()).hexdigest()[:16]
        return self.signature

    def verify(self) -> bool:
        """验证签名"""
        if not self.signature:
            return False
        data = f"{self.receipt_id}{self.dna}{self.result}{self.timestamp}"
        expected = hashlib.sha256(data.encode()).hexdigest()[:16]
        return self.signature == expected


# ============================================================
# 回调管理器
# ============================================================

class CallbackManager:
    """回调管理器 - 管理异步回调"""

    def __init__(self):
        self._callbacks: Dict[str, Callable] = {}
        self._pending: Dict[str, Dict] = {}
        self._results: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def register(self, callback_id: str, func: Callable, timeout: float = 30.0):
        """注册回调"""
        with self._lock:
            self._callbacks[callback_id] = func
            self._pending[callback_id] = {
                "registered_at": time.time(),
                "timeout": timeout,
                "status": "pending",
            }

    def complete(self, callback_id: str, result: Any):
        """完成回调"""
        with self._lock:
            if callback_id in self._callbacks:
                try:
                    self._callbacks[callback_id](result)
                except Exception as e:
                    self._pending[callback_id]["error"] = str(e)
                self._callbacks.pop(callback_id, None)
                self._pending[callback_id]["status"] = "completed"
                self._results[callback_id] = result

    def cancel(self, callback_id: str):
        """取消回调"""
        with self._lock:
            self._callbacks.pop(callback_id, None)
            if callback_id in self._pending:
                self._pending[callback_id]["status"] = "cancelled"

    def get_pending(self) -> List[Dict]:
        """获取待处理回调"""
        with self._lock:
            return [
                {"id": k, **v} for k, v in self._pending.items() if v["status"] == "pending"
            ]


# ============================================================
# 路由器
# ============================================================

class RouteType(Enum):
    FUNCTION = "function"
    MODULE = "module"
    SERVICE = "service"
    EVENT = "event"


@dataclass
class Route:
    """路由定义"""

    route_id: str
    route_type: RouteType
    name: str
    handler: Callable
    pattern: Optional[str] = None
    priority: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class Router:
    """CNSH路由系统"""

    def __init__(self):
        self._routes: Dict[str, Route] = {}
        self._patterns: Dict[str, List[Route]] = {}
        self._lock = threading.Lock()

    def register(self, route: Route):
        """注册路由"""
        with self._lock:
            self._routes[route.route_id] = route
            pattern = route.pattern or route.name
            if pattern not in self._patterns:
                self._patterns[pattern] = []
            self._patterns[pattern].append(route)

    def unregister(self, route_id: str):
        """注销路由"""
        with self._lock:
            if route_id in self._routes:
                route = self._routes.pop(route_id)
                pattern = route.pattern or route.name
                if pattern in self._patterns:
                    self._patterns[pattern] = [
                        r for r in self._patterns[pattern] if r.route_id != route_id
                    ]

    def route(self, path: str, *args, **kwargs) -> Any:
        """路由分发"""
        with self._lock:
            # 精确匹配 name 或 route_id
            for route in self._routes.values():
                if route.name == path or route.route_id == path:
                    return route.handler(*args, **kwargs)

            # 模式匹配
            for pattern, routes in self._patterns.items():
                if path.startswith(pattern) or path.endswith(pattern) or pattern in path:
                    sorted_routes = sorted(routes, key=lambda r: r.priority, reverse=True)
                    for route in sorted_routes:
                        try:
                            return route.handler(*args, **kwargs)
                        except Exception:
                            continue

        raise ValueError(f"未找到路由: {path}")

    def list_routes(self) -> List[Dict]:
        """列出所有路由"""
        with self._lock:
            return [
                {
                    "id": r.route_id,
                    "type": r.route_type.value,
                    "name": r.name,
                    "pattern": r.pattern,
                    "priority": r.priority,
                }
                for r in self._routes.values()
            ]


# ============================================================
# CNSH 运行时引擎
# ============================================================

class CNSHRuntime:
    """CNSH运行时引擎 - 完整执行环境"""

    def __init__(self):
        self.router = Router()
        self.callback_manager = CallbackManager()
        self._receipts: Dict[str, ExecutionReceipt] = {}
        self._lock = threading.Lock()

    # ============================================================
    # 注册函数/模块
    # ============================================================

    def register_function(
        self, name: str, func: Callable, pattern: str = None, priority: int = 0
    ):
        """注册函数到路由"""
        route = Route(
            route_id=f"fn_{name}_{int(time.time() * 1000)}",
            route_type=RouteType.FUNCTION,
            name=name,
            handler=func,
            pattern=pattern or name,
            priority=priority,
        )
        self.router.register(route)

    def register_module(
        self, name: str, module: Any, pattern: str = None, priority: int = 0
    ):
        """注册模块到路由"""

        def module_handler(*args, **kwargs):
            return module

        route = Route(
            route_id=f"mod_{name}_{int(time.time() * 1000)}",
            route_type=RouteType.MODULE,
            name=name,
            handler=module_handler,
            pattern=pattern or name,
            priority=priority,
        )
        self.router.register(route)

    # ============================================================
    # 执行函数 (带回执)
    # ============================================================

    def execute(self, function_name: str, *args, **kwargs) -> ExecutionReceipt:
        """执行函数，生成回执"""
        receipt_id = f"RCPT_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        dna = generate_dna("EXEC")
        start_time = time.time()

        try:
            result = self.router.route(function_name, *args, **kwargs)
            status = "success"
        except Exception as e:
            result = f"{type(e).__name__}: {e}"
            status = "failed"

        duration_ms = (time.time() - start_time) * 1000

        receipt = ExecutionReceipt(
            receipt_id=receipt_id,
            dna=dna,
            function_name=function_name,
            args={"args": args, "kwargs": kwargs},
            result=result,
            status=status,
            timestamp=datetime.now().isoformat(),
            duration_ms=round(duration_ms, 2),
            metadata={"caller": "CNSH_Runtime"},
        )
        receipt.sign()

        with self._lock:
            self._receipts[receipt_id] = receipt

        return receipt

    # ============================================================
    # 异步执行 (带回调)
    # ============================================================

    async def execute_async(self, function_name: str, *args, **kwargs) -> ExecutionReceipt:
        """异步执行函数"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.execute(function_name, *args, **kwargs))

    def execute_with_callback(
        self,
        function_name: str,
        callback_id: str,
        callback_func: Callable,
        *args,
        **kwargs,
    ):
        """执行函数并在完成后回调"""
        self.callback_manager.register(callback_id, callback_func)

        def wrapper():
            receipt = self.execute(function_name, *args, **kwargs)
            self.callback_manager.complete(callback_id, receipt)

        threading.Thread(target=wrapper, daemon=True).start()

    # ============================================================
    # 获取回执
    # ============================================================

    def get_receipt(self, receipt_id: str) -> Optional[ExecutionReceipt]:
        """获取回执"""
        with self._lock:
            return self._receipts.get(receipt_id)

    def get_all_receipts(self) -> List[ExecutionReceipt]:
        """获取所有回执"""
        with self._lock:
            return list(self._receipts.values())

    def get_receipt_by_dna(self, dna: str) -> Optional[ExecutionReceipt]:
        """通过DNA获取回执"""
        with self._lock:
            for receipt in self._receipts.values():
                if receipt.dna == dna:
                    return receipt
            return None


# ============================================================
# 示例：构建CNSH中文函数
# ============================================================


def build_cnsh_runtime():
    """构建CNSH运行时示例"""
    runtime = CNSHRuntime()

    def 计算折扣(价格, 折扣率):
        return 价格 * 折扣率

    def 计算总价(价格列表):
        return sum(价格列表)

    def 过滤商品(商品列表, 最小价格):
        return [p for p in 商品列表 if p.get("价格", 0) >= 最小价格]

    runtime.register_function("计算折扣", 计算折扣)
    runtime.register_function("计算总价", 计算总价)
    runtime.register_function("过滤商品", 过滤商品)

    return runtime


# ============================================================
# 测试
# ============================================================


def test_runtime():
    """测试运行时"""
    print("🐉 CNSH 运行时引擎测试")
    print("=" * 50)

    runtime = build_cnsh_runtime()

    # 1. 执行函数
    print("\n📌 执行 '计算折扣':")
    receipt = runtime.execute("计算折扣", 100, 0.85)
    print(f"  回执: {receipt.receipt_id}")
    print(f"  DNA: {receipt.dna}")
    print(f"  结果: {receipt.result}")
    print(f"  耗时: {receipt.duration_ms}ms")
    print(f"  签名: {receipt.signature}")
    print(f"  验证: {'✅' if receipt.verify() else '❌'}")

    # 2. 异步执行
    print("\n📌 异步执行 '计算总价':")

    async def test_async():
        receipt = await runtime.execute_async("计算总价", [100, 200, 300, 400])
        print(f"  结果: {receipt.result}")
        print(f"  耗时: {receipt.duration_ms}ms")

    asyncio.run(test_async())

    # 3. 回调执行
    print("\n📌 回调执行 '过滤商品':")

    def callback(receipt):
        print(f"  回调结果: {receipt.result}")
        print(f"  DNA: {receipt.dna}")

    runtime.execute_with_callback(
        "过滤商品",
        "cb_test",
        callback,
        [{"名称": "A", "价格": 50}, {"名称": "B", "价格": 150}],
        100,
    )
    time.sleep(1)

    # 4. 列出路由
    print("\n📌 路由列表:")
    for route in runtime.router.list_routes():
        print(f"  {route['name']} ({route['type']}) -> {route['pattern']}")

    # 5. 回执列表
    print(f"\n📌 回执总数: {len(runtime.get_all_receipts())}")

    return runtime


if __name__ == "__main__":
    test_runtime()
