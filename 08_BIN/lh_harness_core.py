#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷏豫-HARNESS-CORE-v1.0-7d3f1a2b
# 创建者: 诸葛鑫（UID9622）
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 契约对齐 🟡 分发模式待实测 🔴 无
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 · Harness 融合内核 v1.0

吸收 DeepSeek Harness 的 Cordis 插件哲学，落地为龍魂工程件：
  1. EffectScope      —— 时空可组合性 · 副作用注册表（onLoad 返回 disposer，卸载全量逆转）
  2. PluginKit        —— 统一插件契约（id/name/version/deps/provides/subscribes）
  3. DispatchBus      —— 四种事件分发模式（emit/waterfall/parallel/serial）

协议: 01_protocols/LH-HARNESS-FUSION-v1.0.md

用法:
  python3 bin/lh_harness_core.py --scope-demo      # 副作用逆转演示
  python3 bin/lh_harness_core.py --plugin-demo     # 插件契约演示
  python3 bin/lh_harness_core.py --dispatch-demo   # 四种分发演示
  或经统一入口: lh harness ...
"""
import argparse
import inspect
import json
import os
import sys
import threading
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

PROJECT_DIR = Path(__file__).resolve().parent.parent
CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


# ============================================================
# 1. EffectScope —— 时空可组合性 · 副作用注册表
# ============================================================
class EffectScope:
    """副作用作用域。

    时间可组合：register() 登记的 disposer 在 reverse_all() 时按逆序执行，
    完整逆转 onLoad 产生的副作用（事件监听/文件句柄/内存分配）。
    用于：插件卸载 · L1/L2 熔断 · 任务失败回滚。
    """

    def __init__(self, name: str = "default"):
        self.name = name
        self._disposers: List[Callable[[], None]] = []
        self._reversed = False

    def register(self, disposer: Callable[[], None]) -> None:
        """登记一个逆转函数（disposer）。"""
        self._disposers.append(disposer)

    def register_handle(self, handle: Any, closer: Optional[Callable[[Any], None]] = None) -> None:
        """登记资源句柄（文件/连接等），卸载时自动关闭。"""
        self.register(lambda h=handle, c=closer: (c(h) if c else h.close()))

    def register_listener(self, unsub: Callable[[], None]) -> None:
        """登记事件监听，卸载时自动退订。"""
        self.register(unsub)

    def reverse_all(self) -> int:
        """逆序逆转全部副作用。返回逆转数量。"""
        if self._reversed:
            return 0
        self._reversed = True
        count = 0
        for disposer in reversed(self._disposers):
            try:
                disposer()
                count += 1
            except Exception as e:
                print(f"⚠️ EffectScope[{self.name}] disposer 失败: {e}", file=sys.stderr)
        return count

    @property
    def size(self) -> int:
        return len(self._disposers)


# ============================================================
# 2. PluginKit —— 统一插件契约（Cordis 对齐）
# ============================================================
@dataclass
class PluginMeta:
    id: str
    name: str = ""
    version: str = "1.0.0"
    dependencies: List[str] = field(default_factory=list)   # 空间可组合
    provides: List[str] = field(default_factory=list)        # 提供能力
    subscribes: List[str] = field(default_factory=list)      # 订阅事件
    license: str = "MulanPSL v2"
    file: str = ""


class PluginContext:
    """插件上下文（Context 对象）：持有作用域 + 服务注册表 + 事件订阅入口。"""

    def __init__(self, registry: "PluginRegistry"):
        self.registry = registry
        self.scope = EffectScope(f"plugin:{registry.current_id or '?'}")
        self.services: Dict[str, Any] = {}
        self.data: Dict[str, Any] = {}

    def subscribe(self, topic: str, handler: Callable) -> Callable:
        """订阅事件，自动登记退订到 scope（卸载时逆转）。"""
        unsub = self.registry.bus.subscribe(topic, handler, owner=self.registry.current_id)
        self.scope.register(unsub)
        return unsub

    def provide(self, name: str, impl: Any) -> None:
        self.services[name] = impl


class Plugin:
    """插件封装：meta + onLoad/onUnload。"""

    def __init__(self, meta: PluginMeta, on_load: Callable, on_unload: Optional[Callable] = None):
        self.meta = meta
        self.on_load = on_load
        self.on_unload = on_unload
        self.loaded = False


class PluginRegistry:
    """插件注册表（Registry）：依赖解析 + 按序装载 + 卸载逆转。"""

    def __init__(self, bus: Optional["DispatchBus"] = None):
        self.bus = bus or DispatchBus()
        self.plugins: Dict[str, Plugin] = {}
        self.current_id: Optional[str] = None
        self.load_order: List[str] = []

    def register(self, plugin: Plugin) -> None:
        self.plugins[plugin.meta.id] = plugin

    def _resolve_deps(self, plugin_id: str, visited: Optional[set] = None) -> List[str]:
        """拓扑排序依赖（空间可组合：声明式依赖解析）。"""
        visited = visited or set()
        if plugin_id in visited:
            raise RuntimeError(f"循环依赖: {plugin_id}")
        visited.add(plugin_id)
        plugin = self.plugins.get(plugin_id)
        if not plugin:
            raise RuntimeError(f"依赖缺失: {plugin_id}")
        order = []
        for dep in plugin.meta.dependencies:
            order += self._resolve_deps(dep, visited)
        order.append(plugin_id)
        return order

    def load(self, plugin_id: str) -> None:
        """装载插件（含依赖），onLoad 必须返回 disposer 或 None。"""
        order = self._resolve_deps(plugin_id)
        for pid in order:
            if self.plugins[pid].loaded:
                continue
            plugin = self.plugins[pid]
            self.current_id = pid
            ctx = PluginContext(self)
            try:
                result = plugin.on_load(ctx) if plugin.on_load else None
                if result is not None:
                    # onLoad 返回 disposer（单个函数）或列表 → 全部登记逆转
                    if isinstance(result, (list, tuple)):
                        for d in result:
                            ctx.scope.register(d)
                    else:
                        ctx.scope.register(result)
                plugin._ctx = ctx
                plugin.loaded = True
                self.load_order.append(pid)
                print(f"✅ 插件装载: {pid} v{plugin.meta.version} | 副作用 {ctx.scope.size} 项已登记")
            except Exception as e:
                # 装载失败 → 逆转已登记的副作用（时间可组合性）
                ctx.scope.reverse_all()
                print(f"❌ 插件装载失败: {pid} | {e}", file=sys.stderr)
                traceback.print_exc()
                raise
        self.current_id = None

    def unload(self, plugin_id: str) -> int:
        """卸载插件：先逆转 scope 副作用，再调 onUnload。返回逆转数。"""
        plugin = self.plugins.get(plugin_id)
        if not plugin or not plugin.loaded:
            return 0
        ctx = getattr(plugin, "_ctx", None)
        n = 0
        if ctx:
            n = ctx.scope.reverse_all()
        if plugin.on_unload:
            try:
                plugin.on_unload(ctx)
            except Exception as e:
                print(f"⚠️ onUnload[{plugin_id}] 异常: {e}", file=sys.stderr)
        plugin.loaded = False
        if plugin_id in self.load_order:
            self.load_order.remove(plugin_id)
        print(f"🔄 插件卸载: {plugin_id} | 逆转副作用 {n} 项")
        return n


# ============================================================
# 3. DispatchBus —— 四种事件分发模式（Cordis EventBus 对齐）
# ============================================================
class DispatchBus:
    """事件总线：emit 广播 / waterfall 瀑布 / parallel 并行 / serial 串行。

    每个订阅者返回 (id, priority, handler)。priority 越小越先执行。
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._subs: Dict[str, List[tuple]] = {}  # topic -> [(id, priority, handler)]
        self.history: List[Dict[str, Any]] = []  # append-only 轨迹（内存版）

    def subscribe(self, topic: str, handler: Callable, owner: str = "anon", priority: int = 50) -> Callable:
        with self._lock:
            self._subs.setdefault(topic, []).append((owner, priority, handler))
        # 返回退订函数
        def _unsub():
            with self._lock:
                subs = self._subs.get(topic, [])
                self._subs[topic] = [s for s in subs if s[2] is not handler]
        return _unsub

    def _record(self, topic: str, mode: str, results: List[Any]):
        self.history.append({
            "ts": datetime.now().isoformat(),
            "topic": topic,
            "mode": mode,
            "subscribers": len(results),
            "ok": sum(1 for r in results if not isinstance(r, Exception)),
        })

    def emit(self, topic: str, payload: Any = None) -> List[Any]:
        """广播：所有订阅者各收一份（互不影响）。"""
        subs = sorted(self._subs.get(topic, []), key=lambda s: s[1])
        results = []
        for owner, _, handler in subs:
            try:
                results.append(handler(payload))
            except Exception as e:
                results.append(e)
        self._record(topic, "emit", results)
        return results

    def waterfall(self, topic: str, payload: Any = None) -> Any:
        """瀑布：前一个输出注入下一个输入（管道）。"""
        subs = sorted(self._subs.get(topic, []), key=lambda s: s[1])
        cur = payload
        results = []
        for owner, _, handler in subs:
            try:
                cur = handler(cur)
            except Exception as e:
                cur = e
            results.append(cur)
        self._record(topic, "waterfall", results)
        return cur

    def parallel(self, topic: str, payload: Any = None, timeout: float = 10.0) -> List[Any]:
        """并行：同时跑，等全部（带超时）。"""
        subs = sorted(self._subs.get(topic, []), key=lambda s: s[1])
        results: List[Any] = [None] * len(subs)
        def _run(idx, handler):
            try:
                results[idx] = handler(payload)
            except Exception as e:
                results[idx] = e
        threads = [threading.Thread(target=_run, args=(i, h)) for i, (_, _, h) in enumerate(subs)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout)
        self._record(topic, "parallel", results)
        return results

    def serial(self, topic: str, payload: Any = None) -> List[Any]:
        """串行：排队依次跑（与 emit 相似但保序记录）。"""
        subs = sorted(self._subs.get(topic, []), key=lambda s: s[1])
        results = []
        for owner, _, handler in subs:
            try:
                results.append(handler(payload))
            except Exception as e:
                results.append(e)
        self._record(topic, "serial", results)
        return results

    def stats(self) -> Dict[str, Any]:
        return {
            "topics": {t: len(s) for t, s in self._subs.items()},
            "history_events": len(self.history),
            "last": self.history[-1] if self.history else None,
        }


# ============================================================
# 4. wrap_legacy —— 存量引擎零侵入插件化（Harness 插件契约落地）
# ============================================================
def wrap_legacy(engine_id: str, run_fn: Callable, name: str = "", version: str = "1.0.0",
                provides: Optional[List[str]] = None, subscribes: Optional[List[str]] = None,
                dependencies: Optional[List[str]] = None) -> Plugin:
    """零侵入包装存量引擎为插件契约：不动原引擎一行代码。

    存量引擎（192 个可执行文件）大多是无插件协议的独立脚本，
    本函数将其 run_fn 包装成标准 Plugin，接入 PluginKit 后即可享受：
    依赖拓扑装载 · 副作用逆转 · 四种事件分发 · 统一生命周期。

    run_fn 签名: run_fn(ctx, payload) -> 结果
    """
    meta = PluginMeta(id=engine_id, name=name or engine_id, version=version,
                      dependencies=list(dependencies or []),
                      provides=list(provides or [engine_id]),
                      subscribes=list(subscribes or []))
    try:
        meta.file = Path(inspect.getfile(run_fn)).name
    except Exception:
        meta.file = ""

    def on_load(ctx):
        ctx.provide(engine_id, run_fn)
        return []  # 存量引擎无副作用注册 → 空 disposer 列表

    return Plugin(meta, on_load)


# ============================================================
# 演示
# ============================================================
def demo_scope():
    print("═══ EffectScope 副作用逆转演示 ═══")
    scope = EffectScope("demo")
    opened = []
    scope.register_handle(["log_handle", 1], lambda h: opened.append(f"closed:{h[1]}"))
    scope.register_listener(lambda: opened.append("unsubscribed"))
    scope.register(lambda: opened.append("memory_freed"))
    print(f"  登记 {scope.size} 项副作用")
    n = scope.reverse_all()
    print(f"  逆转 {n} 项: {opened}")


def demo_plugin():
    print("═══ PluginKit 插件契约演示 ═══")
    bus = DispatchBus()

    def meta_a():
        return PluginMeta(id="lh.demo.a", name="A 引擎", dependencies=[], provides=["svc.a"])

    def meta_b():
        return PluginMeta(id="lh.demo.b", name="B 引擎", dependencies=["lh.demo.a"], provides=["svc.b"])

    events_seen = []

    def load_a(ctx):
        ctx.provide("svc.a", lambda: "A 服务")
        # 订阅事件（自动登记退订）
        ctx.subscribe("demo.topic", lambda p: events_seen.append(f"A got {p}"))
        return []  # disposer 列表

    def load_b(ctx):
        # 依赖 A → ctx 可拿到 A 提供的服务
        a_svc = ctx.registry.plugins["lh.demo.a"]._ctx.services.get("svc.a")
        ctx.data["a_svc_result"] = a_svc() if a_svc else "A 缺失"
        return []

    reg = PluginRegistry(bus)
    reg.register(Plugin(meta_a(), load_a))
    reg.register(Plugin(meta_b(), load_b))
    reg.load("lh.demo.b")
    print(f"  装载顺序: {reg.load_order}")
    print(f"  B 拿到 A 的服务: {reg.plugins['lh.demo.b']._ctx.data['a_svc_result']}")
    bus.emit("demo.topic", "hello")
    print(f"  A 收到事件: {events_seen}")
    reg.unload("lh.demo.b")
    reg.unload("lh.demo.a")
    bus.emit("demo.topic", "again")  # 卸载后应不再触发 A
    print(f"  卸载后再次 emit，A 累计收到数: {len(events_seen)}（应为 1，证明退订生效）")


def demo_dispatch():
    print("═══ DispatchBus 四种分发模式演示 ═══")
    bus = DispatchBus()
    bus.subscribe("pipe", lambda x: (x or 0) + 1, priority=10)
    bus.subscribe("pipe", lambda x: (x or 0) * 10, priority=20)
    bus.subscribe("pipe", lambda x: (x or 0) + 100, priority=30)

    r_emit = bus.emit("pipe", 1)
    print(f"  emit(广播): {r_emit}   ← 各收一份")
    r_wf = bus.waterfall("pipe", 1)
    print(f"  waterfall(瀑布): {r_wf}  ← (1+1)*10+100 = 120")
    r_par = bus.parallel("pipe", 1)
    print(f"  parallel(并行): {r_par}")
    r_ser = bus.serial("pipe", 1)
    print(f"  serial(串行): {r_ser}")
    print(f"  轨迹记录: {bus.stats()['history_events']} 条 (append-only)")


def _legacy_digital_root(ctx, payload):
    """真实存量引擎：数字根引擎（P06）· 动态 import 失败时内联等价实现。"""
    value = int(payload)
    try:
        sys.path.insert(0, str(PROJECT_DIR))
        from bin.lh_digital_root import 数字根引擎
        eng = 数字根引擎()
        if hasattr(eng, "compute_digital_root"):
            return eng.compute_digital_root(value)
        if hasattr(eng, "calcular"):
            return eng.calcular(value)
    except Exception:
        pass
    while value >= 10:
        value = sum(int(d) for d in str(value))
    return value


def _legacy_time_stamp(ctx, payload):
    """真实存量引擎：时间引擎（L0）· 动态 import 失败时内联 ISO 时间。"""
    try:
        sys.path.insert(0, str(PROJECT_DIR))
        from bin.lh_time_engine import get_output_stamp
        return get_output_stamp()
    except Exception:
        from datetime import datetime
        return f"[{datetime.now().isoformat(timespec='seconds')}]"


def demo_legacy():
    """存量引擎插件化演示：数字根引擎 + 时间引擎零侵入接入 PluginKit。"""
    print("═══ wrap_legacy 存量引擎插件化演示 ═══")
    reg = PluginRegistry()
    reg.register(wrap_legacy("lh.digital_root", _legacy_digital_root,
                             name="数字根引擎", provides=["math.digital_root"]))
    reg.register(wrap_legacy("lh.time_stamp", _legacy_time_stamp,
                             name="时间引擎", provides=["time.stamp"]))

    reg.load("lh.digital_root")
    reg.load("lh.time_stamp")
    print(f"  装载顺序: {reg.load_order}")
    for pid in reg.load_order:
        p = reg.plugins[pid]
        print(f"    来源文件: {p.meta.file or '(inline)'}")

    # 通过 DispatchBus 分发调用存量引擎（waterfall: 369 → 数字根 → 时间戳前缀）
    bus = reg.bus
    bus.subscribe("legacy.pipeline",
                  lambda v: reg.plugins["lh.digital_root"]._ctx.services["lh.digital_root"](None, v),
                  priority=10)
    bus.subscribe("legacy.pipeline",
                  lambda v: f"[{reg.plugins['lh.time_stamp']._ctx.services['lh.time_stamp'](None, v)}] root={v}",
                  priority=20)
    final = bus.waterfall("legacy.pipeline", 369)
    print(f"  waterfall 调用存量引擎: 369 → 数字根 = {final}")
    print(f"  验证: sn=369 数字根应为 9 | 时间戳格式: [{final.split(']')[0][1:]}")

    n = reg.unload("lh.digital_root")
    print(f"  卸载逆转: {n} 项副作用")
    return reg


def demo_ai():
    """AI 网关 adapter 插件化演示（一切模型皆插件）。"""
    try:
        from bin.lh_ai_adapters import as_plugins
    except Exception as e:
        print(f"  ⚠️ 未找到 AI 适配器层: {e}")
        return
    print("═══ AI 模型插件化演示（一切模型皆插件） ═══")
    reg = PluginRegistry()
    for p in as_plugins():
        reg.register(p)
    print(f"  已注册 {len(reg.plugins)} 个模型插件: {', '.join(sorted(reg.plugins))}")
    try:
        reg.load("lh.ai.ollama")
        adapter = reg.plugins["lh.ai.ollama"]._ctx.services.get("ai.adapter.ollama")
        if adapter and adapter.check():
            # 演示用轻量模型（7B 加载快）；默认 longhun-v4.0 供日常使用
            demo_model = "qwen2.5:7b"
            print(f"  📥 调用本地模型 {demo_model}（首次加载约 30s，请稍候）...")
            r = adapter.chat([{"role": "user", "content": "用一句话自我介绍"}],
                             model=demo_model)
            print(f"  ✅ ollama 插件调用成功 [{r['model']}]: {r['content'][:120]}")
        else:
            print("  ⚠️ ollama 本地服务未就绪（插件已装载·调用降级跳过）")
        reg.unload("lh.ai.ollama")
    except Exception as e:
        print(f"  ⚠️ ollama 插件装载/调用异常: {e}")


def main():
    ap = argparse.ArgumentParser(description="龍魂 Harness 融合内核 v1.1")
    ap.add_argument("--scope-demo", action="store_true")
    ap.add_argument("--plugin-demo", action="store_true")
    ap.add_argument("--dispatch-demo", action="store_true")
    ap.add_argument("--legacy-demo", action="store_true", help="存量引擎插件化演示（wrap_legacy）")
    ap.add_argument("--ai-demo", action="store_true", help="AI 模型插件化演示（一切模型皆插件）")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    if args.all or args.scope_demo:
        demo_scope()
        print()
    if args.all or args.plugin_demo:
        demo_plugin()
        print()
    if args.all or args.dispatch_demo:
        demo_dispatch()
        print()
    if args.all or args.legacy_demo:
        demo_legacy()
        print()
    if args.all or args.ai_demo:
        demo_ai()
    if not (args.all or args.scope_demo or args.plugin_demo or args.dispatch_demo
            or args.legacy_demo or args.ai_demo):
        ap.print_help()


if __name__ == "__main__":
    main()
