#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 快速索引核心编排器 (Fast Index Core Orchestrator)
DNA: #龍芯⚡️丙午·丙申·壬戌·乙巳·䷾既济-FAST-INDEX-CORE-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
License: MulanPSL v2

功能: 统一入口，编排五层索引引擎。支持 CLI / HTTP API / 定时任务。
      鲲鹏 ARM64 优化：纯 Python 可跑，向量可选 Ollama，SQLite 持久化。

用法:
  python3 05_ENGINES/lh_fast_index_core.py init
  python3 05_ENGINES/lh_fast_index_core.py index --dir ./12_DOCS
  python3 05_ENGINES/lh_fast_index_core.py search "索引哲学"
  python3 05_ENGINES/lh_fast_index_core.py push
  python3 05_ENGINES/lh_fast_index_core.py serve --port 8768
"""

import json
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from engines.lh_behavior_learner import BehaviorLearner
from engines.lh_collective_intel import CollectiveIntel
from engines.lh_context_engine import capture_context, save_context
from engines.lh_implicit_retrieval import ImplicitRetrieval
from engines.lh_vector_index import VectorIndex

DNA_PREFIX = "#龍芯⚡️"
ENGINE_DNA = f"{DNA_PREFIX}丙午·丙申·壬戌·巳时-FAST-INDEX-CORE-UID9622"
UID = "UID9622"
CST = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(CST).isoformat()


class FastIndexCore:
    """快速索引编排器"""

    def __init__(self):
        self.vector = VectorIndex()
        self.behavior = BehaviorLearner()
        self.collective = CollectiveIntel()
        self.implicit = ImplicitRetrieval()

    def init_system(self) -> Dict[str, Any]:
        """初始化索引系统（创建 state 目录）"""
        for sub in ["context_engine", "vector_index", "behavior_learner", "collective_intel", "implicit_retrieval"]:
            (PROJECT_ROOT / ".state" / sub).mkdir(parents=True, exist_ok=True)
        return {
            "status": "initialized",
            "dna": ENGINE_DNA,
            "state_root": str(PROJECT_ROOT / ".state"),
            "timestamp": now_iso(),
        }

    def index_project(
        self,
        root: Optional[Path] = None,
        pattern: str = "*.md",
        force: bool = False,
    ) -> Dict[str, Any]:
        """索引整个项目"""
        root = root or PROJECT_ROOT
        ctx = capture_context()
        stats = self.vector.index_directory(root, pattern=pattern, force=force)
        # 同时记录行为：把整个索引动作作为一个会话
        self.collective.add_session(
            ctx.get("session_id", f"{UID}-{int(time.time())}"),
            [f"index:{root}:{pattern}"],
        )
        return {
            "dna": ENGINE_DNA,
            "timestamp": now_iso(),
            "root": str(root),
            "pattern": pattern,
            "vector_stats": stats,
        }

    def search(self, query: str, top_k: int = 10) -> Dict[str, Any]:
        """统一搜索：语义 + 行为 + 协同"""
        results = self.vector.search(query, top_k=top_k)
        # 行为加权重排
        for r in results:
            fid = Path(r["path"]).name
            # 查询行为记录增加
            self.behavior.record(fid, "search_result", r["title"], duration=0, weight_delta=0.1)
        return {
            "dna": ENGINE_DNA,
            "timestamp": now_iso(),
            "query": query,
            "results": results,
        }

    def push(self, top_k: int = 10) -> Dict[str, Any]:
        """零点击推送"""
        ctx = capture_context()
        save_context(ctx, label="push")
        result = self.implicit.push(context=ctx, top_k=top_k)
        return result

    def dashboard(self) -> Dict[str, Any]:
        """索引系统看板"""
        return {
            "dna": ENGINE_DNA,
            "timestamp": now_iso(),
            "vector": self.vector.stats(),
            "behavior": {
                "top_files": self.behavior.top_items(item_type="file", limit=5),
                "cold_candidates": self.behavior.cold_items(days=90, limit=5),
            },
            "collective": self.collective.stats(),
            "context": capture_context(),
        }

    def watch_session(self, duration: int = 60) -> Dict[str, Any]:
        """简单会话监听：每 interval 秒记录一次上下文（不依赖 fswatch）"""
        interval = 10
        snapshots = []
        end = time.time() + duration
        while time.time() < end:
            ctx = capture_context()
            path = save_context(ctx, label="watch")
            snapshots.append(str(path))
            time.sleep(interval)
        return {
            "status": "watched",
            "duration": duration,
            "snapshots": snapshots,
        }


def _serve_api(port: int = 8768):
    """启动轻量 HTTP API（Kunpeng 本地服务）"""
    try:
        from fastapi import FastAPI
        from uvicorn import run
    except ImportError:
        print("❌ 服务模式需要 fastapi + uvicorn，请安装: pip install fastapi uvicorn requests")
        sys.exit(1)

    app = FastAPI(title="龍魂快速索引 API", version="2.0")
    core = FastIndexCore()

    @app.get("/")
    def root():
        return {"dna": ENGINE_DNA, "status": "running"}

    @app.get("/stats")
    def stats():
        return core.dashboard()

    @app.post("/index")
    def index(payload: Dict[str, Any]):
        root = Path(payload.get("dir", PROJECT_ROOT))
        pattern = payload.get("pattern", "*.md")
        force = payload.get("force", False)
        return core.index_project(root, pattern=pattern, force=force)

    @app.get("/search")
    def search(q: str, top: int = 10):
        return core.search(q, top_k=top)

    @app.get("/push")
    def push(top: int = 10):
        return core.push(top_k=top)

    print(f"🐉 快速索引服务启动: http://127.0.0.1:{port}")
    run(app, host="127.0.0.1", port=port, log_level="warning")


def cli():
    import argparse

    parser = argparse.ArgumentParser(description="龍魂快速索引核心编排器")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("init", help="初始化索引系统")

    p_index = sub.add_parser("index", help="索引项目")
    p_index.add_argument("--dir", default=str(PROJECT_ROOT), help="目标目录")
    p_index.add_argument("--pattern", default="*.md", help="文件通配符")
    p_index.add_argument("--force", action="store_true", help="强制重建")

    p_search = sub.add_parser("search", help="统一搜索")
    p_search.add_argument("query", help="查询语句")
    p_search.add_argument("--top", type=int, default=10, help="返回数量")

    p_push = sub.add_parser("push", help="零点击推送")
    p_push.add_argument("--top", type=int, default=10, help="推送数量")

    sub.add_parser("dashboard", help="索引看板")

    p_watch = sub.add_parser("watch", help="会话监听")
    p_watch.add_argument("--duration", type=int, default=60, help="监听秒数")

    p_serve = sub.add_parser("serve", help="启动 API 服务")
    p_serve.add_argument("--port", type=int, default=8768, help="端口")

    p_tunnel = sub.add_parser("tunnel", help="Mac 本地建立 SSH 隧道到鲲鹏 8768")
    p_tunnel.add_argument("host", nargs="?", default="119.13.90.27", help="鲲鹏主机 IP")
    p_tunnel.add_argument("--port", type=int, default=8768, help="本地/远端端口")

    sub.add_parser("open", help="浏览器打开 127.0.0.1:8768")

    args = parser.parse_args()
    core = FastIndexCore()

    if args.cmd == "init":
        print(json.dumps(core.init_system(), ensure_ascii=False, indent=2))
    elif args.cmd == "index":
        print(
            json.dumps(
                core.index_project(Path(args.dir), pattern=args.pattern, force=args.force),
                ensure_ascii=False,
                indent=2,
            )
        )
    elif args.cmd == "search":
        print(json.dumps(core.search(args.query, top_k=args.top), ensure_ascii=False, indent=2))
    elif args.cmd == "push":
        print(json.dumps(core.push(top_k=args.top), ensure_ascii=False, indent=2))
    elif args.cmd == "dashboard":
        print(json.dumps(core.dashboard(), ensure_ascii=False, indent=2))
    elif args.cmd == "watch":
        print(json.dumps(core.watch_session(args.duration), ensure_ascii=False, indent=2))
    elif args.cmd == "serve":
        _serve_api(args.port)
    elif args.cmd == "tunnel":
        import subprocess as _sp
        key = str(Path.home() / ".ssh" / "longhun_kunpeng_ed25519")
        print(f"🐉 建立 SSH 隧道: 127.0.0.1:{args.port} ←→ {args.host}:{args.port}")
        print("   Ctrl+C 退出隧道\n")
        _sp.run(["ssh", "-i", key, "-o", "StrictHostKeyChecking=no", "-o", "ExitOnForwardFailure=yes",
                 "-N", "-L", f"127.0.0.1:{args.port}:127.0.0.1:{args.port}", f"root@{args.host}"])
    elif args.cmd == "open":
        import subprocess as _sp
        port = getattr(args, "port", 8768)
        _sp.run(["open", f"http://127.0.0.1:{port}"])
        print(f"🌐 已打开浏览器: http://127.0.0.1:{port}")
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
