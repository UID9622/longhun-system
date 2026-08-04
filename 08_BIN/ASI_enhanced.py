#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·ASI增强服务 v2.0 · 完整神经系统
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-ASI-ENHANCED-V2.0-NEURAL-b1a9e3c5
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能:
  - HTTP API 服务·接收自然语言触发词
  - 自动路由: 单步骤→意图引擎 | 多步骤→DAG编排引擎
  - 联动: P1任务图谱·P2 DAG引擎·意图引擎
  - 🧠 神经补全: 长期记忆·感知·决策强化·反思·模型混合
  - 后端模型: ollama longhun-v4.0 (Llama-3.1-8B LoRA)

用法:
  python3 bin/ASI_enhanced.py --port 9000
  python3 bin/ASI_enhanced.py --listen       # 默认端口9000
  curl -X POST http://localhost:9000/run -H "Content-Type: application/json" \\
       -d '{"trigger":"先审计，再签名，最后推送"}'
"""

import json
import sys
import os
import time
import uuid
import hashlib
import datetime
import argparse
import subprocess
import threading
from pathlib import Path
from typing import Optional, Dict, Any, List
from collections import defaultdict

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# 🧠 神经补全模块
from lh_asi_neural import (
    ensure_init, pre_process, post_process,
    get_neural_status, search_memory, list_reflections,
    get_recommended_strategy,
)
from lh_asi_neural import NeuralContext

# ============================================================
# 零、常量 & 路径
# ============================================================

PROJECT_ROOT = Path.home() / "longhun-system"
BIN_DIR = PROJECT_ROOT / "bin"
DNA_PREFIX = "#龍芯⚡️"

sys.path.insert(0, str(BIN_DIR))

# ============================================================
# 一、数据模型
# ============================================================

class TriggerRequest(BaseModel):
    trigger: str = Field(..., description="自然语言触发词", min_length=1, max_length=2000)
    async_mode: bool = Field(False, description="是否异步执行")
    model: str = Field("longhun-v4.0", description="后端模型名称")

class TriggerResponse(BaseModel):
    status: str = Field(..., description="🟢通过 / 🟡待核 / 🔴熔断")
    response: str = Field("", description="执行结果摘要")
    dna: str = Field("", description="DNA追溯码")
    卦象: str = Field("", description="当前卦名")
    dag_id: Optional[str] = Field(None, description="DAG执行ID(多步骤)")
    graph_node: Optional[str] = Field(None, description="图谱节点ID")
    audit_mark: str = Field("🟢", description="三色审计")
    execution_time_ms: float = Field(0, description="执行耗时ms")
    mode: str = Field("single", description="执行模式: single/dag")
    steps: int = Field(0, description="DAG步骤数(多步骤)")

class StatusResponse(BaseModel):
    service: str = "龍魂·ASI增强服务"
    version: str = "v1.0"
    model: str = "longhun-v4.0"
    dag_stats: Dict[str, Any] = {}
    uptime_seconds: float = 0
    total_requests: int = 0

# ============================================================
# 二、龍魂起卦
# ============================================================

def 起卦() -> str:
    """简易起卦·返回卦名"""
    hexagrams = [
        "乾☰", "坤☷", "屯䷂", "蒙䷃", "需䷄", "讼䷅", "师䷆", "比䷇",
        "小畜䷈", "履䷉", "泰䷊", "否䷋", "同人䷌", "大有䷍", "谦䷎", "豫䷏",
        "随䷐", "蛊䷑", "临䷒", "观䷓", "噬嗑䷔", "贲䷕", "剥䷖", "复䷗",
        "无妄䷘", "大畜䷙", "颐䷚", "大过䷛", "坎☵", "离☲",
        "咸䷞", "恒䷟", "遁䷠", "大壮䷡", "晋䷢", "明夷䷣", "家人䷤", "睽䷥",
        "蹇䷦", "解䷧", "损䷨", "益䷩", "夬䷪", "姤䷫", "萃䷬", "升䷭",
        "困䷮", "井䷯", "革䷰", "鼎䷱", "震☳", "艮☶",
        "渐䷴", "归妹䷵", "丰䷶", "旅䷷", "巽☴", "兑☱",
        "涣䷺", "节䷻", "中孚䷼", "小过䷽", "既济䷾", "未济䷿",
    ]
    idx = int(time.time() * 1000) % 64
    return hexagrams[idx]

def 生成DNA(模块: str, 动作: str) -> str:
    h = hashlib.sha256(f"{模块}{动作}{time.time()}".encode()).hexdigest()[:8]
    return f"{DNA_PREFIX}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{模块}-{动作}-{h}"

# ============================================================
# 三、意图引擎桥接
# ============================================================

def 路由意图引擎(trigger: str) -> Dict[str, Any]:
    """通过意图引擎处理单步骤请求"""
    try:
        from bin.lh_intent_engine import 意念交流引擎V3
        engine = 意念交流引擎V3()
        result = engine.处理(trigger)
        return {
            "status": result.get("状态", "🟡"),
            "response": result.get("响应", ""),
            "dna": result.get("DNA", ""),
            "卦象": result.get("卦象", ""),
            "persona": result.get("人格", "未知"),
            "audit_score": result.get("监督分数", 0),
            "dag_routed": result.get("DAG路由", False),
            "source": result.get("来源", "意图引擎"),
        }
    except Exception as e:
        return {
            "status": "🟡",
            "response": f"意图引擎处理异常: {e}",
            "dna": 生成DNA("意图引擎", "异常"),
            "卦象": 起卦(),
            "persona": "P09孙思邈",
            "audit_score": 0,
            "dag_routed": False,
            "source": "fallback",
        }

# ============================================================
# 四、DAG引擎桥接
# ============================================================

def 路由DAG引擎(trigger: str) -> Dict[str, Any]:
    """通过DAG引擎处理多步骤请求"""
    try:
        from lh_dag_engine import DAGEngine, ExecutionMode, IntentEngineHook
        # 先检测是否多步骤
        hook = IntentEngineHook()
        if not hook.detect_multi_step(trigger):
            return None  # 不触发 DAG

        engine = DAGEngine()
        nodes, name = engine.build_from_text(trigger)
        valid, msg = engine.validate(nodes)
        if not valid:
            return {
                "status": "🔴",
                "response": f"DAG验证失败: {msg}",
                "dna": 生成DNA("DAG", "验证失败"),
                "dag_id": None,
                "steps": 0,
                "error": msg,
            }

        result = engine.execute(nodes, mode=ExecutionMode.AUTO)
        return {
            "status": "🟢" if result.status == "success" else "🟡",
            "response": f"🐉 DAG完成·{len(result.nodes)}步骤·{'全部成功' if result.status=='success' else '部分失败'}",
            "dna": result.dna or 生成DNA("DAG", "执行"),
            "dag_id": result.dag_id,
            "steps": len(result.nodes),
            "node_results": {
                nid: {
                    "name": engine._node_map.get(nid, {}).get("name", nid) if hasattr(engine, "_node_map") else nid,
                    "status": r.status.value,
                    "exit_code": r.exit_code,
                }
                for nid, r in result.results.items()
            } if hasattr(result, 'results') else {},
            "error": result.error,
        }
    except Exception as e:
        return {
            "status": "🔴",
            "response": f"DAG引擎异常: {e}",
            "dna": 生成DNA("DAG", "异常"),
            "dag_id": None,
            "steps": 0,
            "error": str(e),
        }

# ============================================================
# 五、Ollama 模型调用
# ============================================================

def 调用Ollama(prompt: str, model: str = "longhun-v4.0", timeout: int = 60) -> str:
    """直接调用 ollama 模型"""
    try:
        proc = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if proc.returncode == 0:
            return proc.stdout.strip()
        return f"[模型错误: {proc.stderr[:200]}]"
    except subprocess.TimeoutExpired:
        return "[模型超时]"
    except FileNotFoundError:
        return "[ollama未安装]"
    except Exception as e:
        return f"[调用异常: {e}]"

# ============================================================
# 六、任务图谱联动
# ============================================================

def 写入图谱(trigger: str, result: Dict[str, Any], is_dag: bool = False):
    """执行结果写入P1任务关联图谱"""
    try:
        from lh_task_graph import TaskGraphEngine
        tg = TaskGraphEngine()
        task_type = "DAG多步骤" if is_dag else "单步骤"
        tg.on_task_complete(
            input_text=trigger,
            task_type=task_type,
            persona=result.get("persona", "ASI"),
            success=result.get("status") in ("🟢", "🟢 通过"),
            response=result.get("response", ""),
            audit_mark=result.get("audit_mark", "🟢"),
        )
        return True
    except Exception:
        return False

# ============================================================
# 七、核心路由逻辑
# ============================================================

def 智能路由(trigger: str, model: str = "longhun-v4.0") -> TriggerResponse:
    """
    核心路由 (v2.0·神经增强):
      1. 🧠 前置钩子: 感知 + 记忆检索
      2. 检测 DAG 触发词 → DAG 引擎
      3. 否则 → 意图引擎（含阶段12 DAG自动检测）
      4. 写入任务图谱
      5. 🧠 后置钩子: 记忆存储 + 反思 + 权重更新
    """
    t0 = time.time()
    trig_lower = trigger.lower().strip()

    # ── 🧠 前置神经钩子 ──
    neural_ctx = pre_process(trigger)
    # 多步骤场景下获取推荐策略
    steps_estimated = trigger.count("然后") + trigger.count("再") + 1
    neural_ctx.strategy = get_recommended_strategy(steps_estimated)

    is_dag = False
    dag_result = None
    intent_result = None

    # ── 显式多步骤检测 ──
    dag_keywords = ["然后", "接着", "再", "之后", "随后", "最后",
                    "先", "同时", "一并", "第一步", "第二步",
                    "并且", "还有", "另外"]
    explicit_dag = any(kw in trigger for kw in dag_keywords)

    if explicit_dag:
        dag_result = 路由DAG引擎(trigger)
        if dag_result:
            is_dag = True

    # ── 不是显式多步骤 → 走意图引擎 ──
    if not is_dag:
        intent_result = 路由意图引擎(trigger)

    # ── 组装响应 ──
    if is_dag and dag_result:
        result_data = dag_result
        mode = "dag"
    elif intent_result:
        result_data = intent_result
        mode = "single"
        if intent_result.get("dag_routed"):
            mode = "dag"
    else:
        dna = 生成DNA("ASI", "兜底")
        return TriggerResponse(
            status="🟡",
            response="无法路由，请重新描述。",
            dna=dna,
            卦象=起卦(),
            audit_mark="🟡",
            execution_time_ms=(time.time() - t0) * 1000,
            mode="fallback",
            steps=0,
        )

    elapsed = (time.time() - t0) * 1000

    # ── 🧠 后置神经钩子 ──
    result_dict = result_data.copy()
    result_dict["execution_time_ms"] = elapsed
    post_process(trigger, result_dict, neural_ctx)

    return TriggerResponse(
        status=result_data.get("status", "🟡"),
        response=result_data.get("response", ""),
        dna=result_data.get("dna", ""),
        卦象=起卦(),
        dag_id=result_data.get("dag_id"),
        audit_mark="🟢" if result_data.get("status", "").startswith("🟢") else "🟡",
        execution_time_ms=elapsed,
        mode=mode,
        steps=result_data.get("steps", 0),
    )

# ============================================================
# 八、FastAPI 应用
# ============================================================

app = FastAPI(
    title="龍魂·ASI增强服务",
    description="集成意图引擎·DAG编排·任务图谱·ollama v4.0",
    version="v1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 运行时统计
start_time = time.time()
total_requests = 0
request_lock = threading.Lock()

@app.get("/")
async def root():
    return {"service": "龍魂·ASI增强服务", "version": "v1.0", "model": "longhun-v4.0"}

@app.get("/status")
async def status() -> StatusResponse:
    try:
        from lh_dag_engine import DAGEngine
        e = DAGEngine()
        dag_stats = e.stats()
    except Exception:
        dag_stats = {"error": "DAG引擎不可用"}
    return StatusResponse(
        dag_stats=dag_stats,
        uptime_seconds=time.time() - start_time,
        total_requests=total_requests,
    )

@app.post("/run")
async def run_trigger(req: TriggerRequest):
    global total_requests
    with request_lock:
        total_requests += 1

    result = 智能路由(req.trigger, req.model)

    # 后台写图谱（不阻塞响应）
    is_dag = result.mode == "dag"
    threading.Thread(
        target=写入图谱,
        args=(req.trigger, result.model_dump(), is_dag),
        daemon=True,
    ).start()

    # 🧠 附上神经层摘要
    response_dict = result.model_dump()
    ensure_init()
    from lh_asi_neural import _LTM, _PERCEP, _REFLECT, _REINFORCE
    recent_reflections = _REFLECT.list_recent(5)
    response_dict["neural"] = {
        "memory_total": _LTM.stats().get("count", 0),
        "perception": _PERCEP.sense(),
        "strategy_weights": _REINFORCE.strategy_weights,
        "recent_reflections": [r["summary"] for r in recent_reflections[-3:]],
    }
    return response_dict

@app.get("/run")
async def run_trigger_get(
    trigger: str = Query(..., description="自然语言触发词"),
    model: str = Query("longhun-v4.0", description="模型名称"),
):
    global total_requests
    with request_lock:
        total_requests += 1

    req = TriggerRequest(trigger=trigger, model=model)
    return await run_trigger(req)

@app.post("/ollama")
async def ollama_call(req: TriggerRequest):
    """直接调用 ollama 模型"""
    response = 调用Ollama(req.trigger, req.model)
    return {"model": req.model, "prompt": req.trigger, "response": response}

@app.get("/health")
async def health():
    return {"status": "ok", "uptime": time.time() - start_time}

# ============================================================
# 九点五、🧠 神经层 API
# ============================================================

@app.get("/neural/status")
async def neural_status():
    """神经层完整状态"""
    return get_neural_status()

@app.get("/memory/search")
async def memory_search(q: str = Query(..., description="搜索关键词"), n: int = Query(5, ge=1, le=20)):
    """语义搜索长期记忆"""
    results = search_memory(q, n)
    return {"query": q, "count": len(results), "results": results}

@app.get("/perception")
async def perception():
    """获取当前感知数据"""
    ensure_init()
    from lh_asi_neural import _PERCEP
    return _PERCEP.sense()

@app.get("/reflections")
async def reflections(n: int = Query(10, ge=1, le=50)):
    """最近反思记录"""
    results = list_reflections(n)
    return {"count": len(results), "reflections": results}

@app.get("/neural/strategy")
async def neural_strategy(steps: int = Query(1, ge=1, le=20)):
    """获取推荐执行策略"""
    strategy = get_recommended_strategy(steps)
    ensure_init()
    from lh_asi_neural import _REINFORCE
    return {
        "steps": steps,
        "strategy": strategy,
        "weights": _REINFORCE.strategy_weights,
    }

# ============================================================
# 九、CLI入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="龍魂·ASI增强服务 v1.0")
    parser.add_argument("--port", type=int, default=9000, help="监听端口 (默认9000)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="监听地址")
    parser.add_argument("--listen", action="store_true", help="启动HTTP服务")
    parser.add_argument("--test", type=str, help="单次测试触发词")
    args = parser.parse_args()

    if args.test:
        print(f"🐉 测试: {args.test}")
        result = 智能路由(args.test)
        print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))
        return

    if args.listen or not args.test:
        # 🧠 初始化神经组件
        ensure_init()
        print(f"""
🐉 龍魂·ASI增强服务 v2.0 · 完整神经系统
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  端口: {args.port}
  模型: longhun-v4.0 (Llama-3.1-8B LoRA)
  路由: 意图引擎 + DAG编排 + 任务图谱
  🧠 神经: 长期记忆 + 感知 + 决策强化 + 反思 + 模型混合
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  POST /run        → 智能路由
  GET  /run         → 快速调用
  POST /ollama      → 直接模型调用
  GET  /status      → 服务状态
  GET  /health      → 健康检查
  🧠 /neural/status → 神经层状态
  🧠 /memory/search → 长期记忆搜索
  🧠 /perception    → 系统感知
  🧠 /reflections   → 反思记录
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)
        uvicorn.run(app, host=args.host, port=args.port, log_level="info")

if __name__ == "__main__":
    main()
