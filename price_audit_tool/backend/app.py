#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
价格审计工具 - FastAPI后端
DNA: #龍芯⚡️丙午·乙未·辛亥·巳时·☰乾-PRICE-AUDIT-API-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import sys
from pathlib import Path

# 确保可以导入同级模块
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from detector import detect_price_anomaly, quick_check
from models import save_report, list_reports, get_report, get_stats

app = FastAPI(
    title="价格透明度审计工具",
    description="""
## 算法审计平民化

每个人都能检测大数据杀熟。

### 检测维度
- **L1 IQR统计检测**: 箱线图法识别异常价格
- **L2 用户分组**: 比较新老用户价格差异
- **L3 时间序列**: 检测短期价格剧烈波动
- **L4 综合评分**: 加权杀熟评分 0-100

### 协议
- 原创: 诸葛鑫 (UID9622)
- 协议: CC BY-NC-SA 4.0
- 数据本地存储·不上传云端
""",
    version="1.0.0",
    docs_url="/docs",
)

# CORS - 允许前端跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── 请求模型 ───

class AuditRequest(BaseModel):
    """审计请求"""
    prices: list[float] = Field(..., min_length=1, description="价格列表（必填）")
    groups: dict[str, list[float]] | None = Field(
        default=None,
        description="按用户类型分组价格，如 {\"新用户\":[9.9],\"老用户\":[12.0]}",
        example={"新用户": [9.9, 10.0], "老用户": [12.0, 12.5]}
    )
    timeseries: list[dict] | None = Field(
        default=None,
        description="带时间戳的价格序列",
        example=[{"time": "2026-07-28 10:00", "price": 9.9}]
    )
    product_name: str = Field(default="", description="商品名称（可选）")
    platform: str = Field(default="", description="平台名称（可选）")


class QuickAuditRequest(BaseModel):
    """快速审计"""
    prices: list[float] = Field(..., min_length=1)


# ─── API 路由 ───

@app.get("/")
def root():
    return {
        "service": "价格透明度审计工具 v1.0",
        "creator": "诸葛鑫 (UID9622)",
        "protocol": "CC BY-NC-SA 4.0",
        "docs": "/docs",
        "frontend": "/dashboard",
        "endpoints": {
            "POST /api/audit": "完整审计",
            "POST /api/quick": "快速审计（仅价格列表）",
            "GET /api/reports": "历史报告列表",
            "GET /api/reports/{id}": "单个报告",
            "GET /api/stats": "全局统计",
            "GET /api/health": "健康检查"
        }
    }


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.post("/api/audit")
def api_audit(req: AuditRequest):
    """执行完整价格审计。"""
    result = detect_price_anomaly(
        prices=req.prices,
        groups=req.groups,
        timeseries=req.timeseries
    )
    result["product_name"] = req.product_name
    result["platform"] = req.platform
    result["input_summary"] = {
        "price_count": len(req.prices),
        "groups": list(req.groups.keys()) if req.groups else None,
        "timeseries_count": len(req.timeseries) if req.timeseries else 0
    }
    
    # 保存报告
    report_id = save_report(result)
    result["report_id"] = report_id
    
    return result


@app.post("/api/quick")
def api_quick(req: QuickAuditRequest):
    """快速审计：只传价格列表。"""
    result = quick_check(req.prices)
    report_id = save_report(result)
    result["report_id"] = report_id
    return result


@app.get("/api/reports")
def api_reports(limit: int = 20):
    return {"reports": list_reports(limit)}


@app.get("/api/reports/{report_id}")
def api_get_report(report_id: str):
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    return report


@app.get("/api/stats")
def api_stats():
    return get_stats()


@app.get("/api/sample")
def api_sample():
    """返回示例数据，方便用户快速体验。"""
    return {
        "description": "这是一个典型的大数据杀熟场景：同一商品，新老用户看到不同价格",
        "prices": [9.9, 10.0, 9.8, 12.0, 12.5, 12.3, 10.0, 9.9, 12.8, 11.9],
        "groups": {
            "新用户": [9.9, 10.0, 9.8, 10.0, 9.9],
            "老用户": [12.0, 12.5, 12.3, 12.8, 11.9]
        },
        "timeseries": [
            {"time": "2026-07-20", "price": 9.9},
            {"time": "2026-07-21", "price": 9.8},
            {"time": "2026-07-22", "price": 10.0},
            {"time": "2026-07-23", "price": 12.0},
            {"time": "2026-07-24", "price": 12.5},
            {"time": "2026-07-25", "price": 12.3},
        ],
        "expected_result": "🔴 严重可疑 - 新老用户价格差异约22%，杀熟评分预计70+"
    }


# ─── 静态文件服务 ───
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/dashboard", StaticFiles(directory=str(frontend_path), html=True), name="dashboard")


# ─── 启动入口 ───
if __name__ == "__main__":
    import uvicorn
    print("""
╔══════════════════════════════════════════════╗
║     价格透明度审计工具 v1.0                    ║
║     Price Transparency Audit Tool             ║
║                                               ║
║  前端仪表盘: http://localhost:8899/dashboard    ║
║  API文档:    http://localhost:8899/docs         ║
║  API入口:    http://localhost:8899              ║
║                                               ║
║  创建者: 诸葛鑫 (UID9622)                      ║
║  协议: CC BY-NC-SA 4.0                         ║
║  数据本地存储 · 不上传云端                      ║
╚══════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host="0.0.0.0", port=8899, log_level="info")
