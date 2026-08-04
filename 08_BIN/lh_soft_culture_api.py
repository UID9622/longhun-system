#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·软文化污染隔离API服务 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☲离-SOFT-CULTURE-API-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

基于 engines/lh_culture_isolation_engine.py 的三层过滤引擎，
对外暴露 REST API，支持单条检测、批量检测、健康检查。

对应CSDN文章: https://uid9622-01.blog.csdn.net/article/details/163131519
"""

import hashlib
import json
import os
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

# ── 加载引擎 ──
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'engines'))
sys.path.insert(0, os.path.dirname(__file__))

try:
    from lh_culture_isolation_engine import CultureIsolationEngine, IsolationResult
    ENGINE_AVAILABLE = True
except ImportError as e:
    ENGINE_AVAILABLE = False
    ENGINE_IMPORT_ERROR = str(e)

try:
    from fastapi import FastAPI, HTTPException, Query
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel, Field
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

from pathlib import Path

DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·☲离-SOFT-CULTURE-API-v1.0"

# ══════════════════════════════════════════════════════════════════════
# 数据模型
# ══════════════════════════════════════════════════════════════════════

class AnalyzeRequest(BaseModel):
    text: str = Field(..., description="待检测文本", min_length=1)
    source_type: str = Field("self_media", description="语境类型: product_copy|short_video|comment_spam|self_media|social_post|personal_chat|academic|news_body|gov_doc")
    account_meta: Optional[Dict[str, Any]] = Field(None, description="账户元数据（可选）")

class BatchAnalyzeRequest(BaseModel):
    items: List[Dict[str, Any]] = Field(..., description="批量检测项列表", min_length=1, max_length=500)

class AnalyzeResponse(BaseModel):
    text_snippet: str
    pci: float
    layer1_score: float
    layer2_score: float
    layer3_score: float
    matched_templates: List[str]
    pollution_grade: str
    action: str
    visible: str
    audit_mark: str
    reason: str
    dna: str = ""
    timestamp: str = ""

class BatchAnalyzeResponse(BaseModel):
    total: int
    results: List[AnalyzeResponse]
    summary: Dict[str, int]

# ══════════════════════════════════════════════════════════════════════
# API 应用
# ══════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="龍魂·软文化污染隔离API",
    description="""
## 软文化污染隔离协议 v1.0

三层过滤架构：
- **L1 组合特征层**：47组话术模板（A政治包装+B宗教隐喻+C消费主义+D软内容+E焦虑制造）
- **L2 传播路径层**：复用七因子行为密码学+水军补丁v1.2（含自然簇豁免防误伤）
- **L3 语境分析层**：9种语境分类（政府公文/学术讨论等自动豁免）

综合污染指数 PCI = 0.35×L1 + 0.35×L2 + 0.30×L3

### 隔离动作
| PCI范围 | 等级 | 动作 |
|:---|:---|:---|
| 0.00–0.25 | 🟢 清洁 | 正常显示 |
| 0.25–0.45 | 🟡 观察 | 正常显示+48h复核 |
| 0.45–0.65 | 🟠 轻度 | 降权+标签 |
| 0.65–0.85 | 🔴 中度 | 折叠+污染报告 |
| 0.85–1.00 | ⚫ 重度 | 隔离归档 |
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 全局引擎实例 ──
engine: Optional[CultureIsolationEngine] = None


def get_engine() -> CultureIsolationEngine:
    global engine
    if engine is None:
        engine = CultureIsolationEngine()
    return engine


# ══════════════════════════════════════════════════════════════════════
# 端点
# ══════════════════════════════════════════════════════════════════════

@app.get("/health", tags=["系统"])
def health():
    """健康检查"""
    eng_status = "✅" if ENGINE_AVAILABLE else "🔴"
    return {
        "status": "ok" if ENGINE_AVAILABLE else "degraded",
        "engine": eng_status,
        "dna": DNA,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/v1/info", tags=["系统"])
def engine_info():
    """引擎信息"""
    eng = get_engine()
    return {
        "version": "1.0.0",
        "templates": eng.n_templates,
        "templates_by_category": {
            "A_政治包装": len([t for t in eng.templates if t.category == "A"]),
            "B_宗教隐喻": len([t for t in eng.templates if t.category == "B"]),
            "C_消费主义": len([t for t in eng.templates if t.category == "C"]),
            "D_软内容": len([t for t in eng.templates if t.category == "D"]),
            "E_焦虑制造": len([t for t in eng.templates if t.category == "E"]),
        },
        "pci_weights": {"L1": eng.W1, "L2": eng.W2, "L3": eng.W3},
        "thresholds": {
            "clean": eng.PCI_CLEAN,
            "watch": eng.PCI_WATCH,
            "mild": eng.PCI_MILD,
            "moderate": eng.PCI_MODERATE,
        },
        "context_types": list(eng.l3_context_score.__code__.co_varnames) if False else [
            {"key": k, "name": v["name"], "risk": v["risk"]}
            for k, v in {
                "product_copy": {"name": "商品文案/带货", "risk": "high"},
                "short_video": {"name": "短视频标题", "risk": "high"},
                "comment_spam": {"name": "评论区水军", "risk": "high"},
                "self_media": {"name": "自媒体文章", "risk": "medium"},
                "social_post": {"name": "社交动态", "risk": "medium"},
                "personal_chat": {"name": "个人聊天", "risk": "low"},
                "academic": {"name": "学术讨论", "risk": "low"},
                "news_body": {"name": "新闻正文", "risk": "low"},
                "gov_doc": {"name": "政府公文", "risk": "immune"},
            }.items()
        ],
        "dna": DNA,
    }


@app.get("/v1/templates", tags=["特征库"])
def list_templates(category: Optional[str] = Query(None, description="按分类筛选: A|B|C|D|E")):
    """获取话术模板列表"""
    eng = get_engine()
    templates = eng.templates
    if category:
        templates = [t for t in templates if t.category == category]
    return {
        "total": len(templates),
        "templates": [
            {
                "id": t.id,
                "category": t.category,
                "keywords": t.keywords,
                "min_hits": t.min_hits,
                "weight": t.weight,
                "description": t.description,
            }
            for t in templates
        ],
    }


@app.post("/v1/analyze", response_model=AnalyzeResponse, tags=["检测"])
def analyze(req: AnalyzeRequest):
    """
    单条文本检测
    
    - **text**: 待检测文本
    - **source_type**: 语境类型，默认 self_media
    - **account_meta**: 账户元数据（账号天数/发帖频率/集群信息/七因子分等）
    
    示例请求:
    ```json
    {
      "text": "历史真相一直被掩盖，你必须觉醒独立思考追求自由。",
      "source_type": "self_media",
      "account_meta": {
        "account_age_days": 3,
        "posts_per_hour": 25,
        "coordinated_timing": true,
        "cluster_id": "C-8842",
        "cluster_burst": true
      }
    }
    ```
    """
    eng = get_engine()
    result = eng.analyze(
        text=req.text,
        source_type=req.source_type,
        account_meta=req.account_meta,
    )
    return _result_to_response(result)


@app.post("/v1/batch", response_model=BatchAnalyzeResponse, tags=["检测"])
def batch_analyze(req: BatchAnalyzeRequest):
    """批量文本检测（最多500条）"""
    eng = get_engine()
    results = eng.batch_analyze(req.items)
    
    responses = [_result_to_response(r) for r in results]
    summary = {"🟢清洁": 0, "🟡观察": 0, "🟠轻度": 0, "🔴中度": 0, "⚫重度": 0}
    grade_map = {
        "🟢 清洁": "🟢清洁", "🟡 观察": "🟡观察",
        "🟠 轻度污染": "🟠轻度", "🔴 中度污染": "🔴中度", "⚫ 重度污染": "⚫重度",
    }
    for r in responses:
        key = grade_map.get(r.pollution_grade, "🟢清洁")
        summary[key] = summary.get(key, 0) + 1
    
    return BatchAnalyzeResponse(total=len(responses), results=responses, summary=summary)


@app.post("/v1/analyze-simple", tags=["检测"])
def analyze_simple(text: str = Query(..., description="待检测文本（GET参数方式）")):
    """简易检测（GET/POST，仅传文本）"""
    eng = get_engine()
    result = eng.analyze(text=text)
    return _result_to_response(result)


# ══════════════════════════════════════════════════════════════════════
# 辅助
# ══════════════════════════════════════════════════════════════════════

def _result_to_response(result: IsolationResult) -> AnalyzeResponse:
    return AnalyzeResponse(
        text_snippet=result.text_snippet,
        pci=result.pci,
        layer1_score=result.layer1_score,
        layer2_score=result.layer2_score,
        layer3_score=result.layer3_score,
        matched_templates=result.matched_templates,
        pollution_grade=result.pollution_grade,
        action=result.action,
        visible=result.visible,
        audit_mark=result.audit_mark,
        reason=result.reason,
        dna=DNA,
        timestamp=datetime.now().isoformat(),
    )


# ══════════════════════════════════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════════════════════════════════

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="龍魂·软文化污染隔离API服务 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_soft_culture_api.py              # 启动API服务 (默认:8768)
  python3 bin/lh_soft_culture_api.py --port 8769  # 指定端口
  python3 bin/lh_soft_culture_api.py --test       # 自测试（不启动服务）
  python3 bin/lh_soft_culture_api.py --cli "文本"  # 命令行单条检测
        """,
    )
    parser.add_argument("--port", type=int, default=8768, help="服务端口 (默认: 8768)")
    parser.add_argument("--host", default="0.0.0.0", help="绑定地址 (默认: 0.0.0.0)")
    parser.add_argument("--test", action="store_true", help="自测试（不启动服务）")
    parser.add_argument("--cli", type=str, help="命令行检测: 直接传入文本")
    parser.add_argument("--source", default="self_media", help="--cli 的语境类型")
    
    args = parser.parse_args()
    
    # ── CLI模式 ──
    if args.cli:
        eng = get_engine()
        result = eng.analyze(text=args.cli, source_type=args.source)
        print(f"\n{'='*60}")
        print(f"  软文化污染隔离 · CLI检测")
        print(f"{'='*60}")
        print(f"  文本: {result.text_snippet}")
        print(f"  等级: {result.pollution_grade}")
        print(f"  PCI : {result.pci:.4f}")
        print(f"  L1  : {result.layer1_score:.4f}  L2: {result.layer2_score:.4f}  L3: {result.layer3_score:.4f}")
        print(f"  模板: {', '.join(result.matched_templates) if result.matched_templates else '无'}")
        print(f"  动作: {result.action}")
        print(f"  审计: {result.audit_mark}")
        print(f"  理由: {result.reason}")
        print(f"{'='*60}\n")
        return
    
    # ── 自测试 ──
    if args.test:
        eng = get_engine()
        tests = [
            ("正常聊天", "今天天气真好，出去走走。", "personal_chat", None),
            ("明确话术", "历史真相一直被掩盖，你必须觉醒独立思考追求自由。", "self_media", {
                "account_age_days": 3, "posts_per_hour": 25,
                "coordinated_timing": True, "cluster_burst": True,
            }),
            ("学术讨论", "历史虚无主义的表现形式及其对文化认同的影响研究。", "academic", None),
            ("政府公文", "坚持对外开放，保障人民的合法权益。", "gov_doc", None),
        ]
        for name, text, source, meta in tests:
            r = eng.analyze(text=text, source_type=source, account_meta=meta)
            print(f"  [{r.pollution_grade}] {name} | PCI={r.pci:.3f} | {r.action}")
        print("\n  ✅ 自测试完成")
        return
    
    # ── API服务 ──
    if not FASTAPI_AVAILABLE:
        print("❌ FastAPI 未安装。请运行: pip install fastapi uvicorn")
        sys.exit(1)
    
    print(f"""
╔══════════════════════════════════════════════════╗
║  龍魂·软文化污染隔离API v1.0                     ║
║  DNA: {DNA[-20:]}  ║
║  端口: {args.port}                                    ║
║  文档: http://localhost:{args.port}/docs              ║
║  文章: https://uid9622-01.blog.csdn.net/163131519    ║
╚══════════════════════════════════════════════════╝
""")
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
