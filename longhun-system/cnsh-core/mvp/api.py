"""
MVP v2.0 FastAPI 路由
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel
from typing import Optional

from .pipeline import run_pipeline
from .store import load, list_pages

router = APIRouter(prefix="/mvp", tags=["mvp"])


@router.get("/")
def mvp_root():
    """MVP 前端入口重定向"""
    return RedirectResponse(url="/mvp/static/index.html")


class GenerateRequest(BaseModel):
    input: str
    user_id: str = "UID9622"


@router.post("/generate")
def generate(req: GenerateRequest):
    """主生成接口：一句话 → 一个页面"""
    result = run_pipeline(req.input, user_id=req.user_id)
    if result["status"] == "blocked":
        return JSONResponse(status_code=403, content=result)
    return result


@router.get("/page/{page_id}", response_class=HTMLResponse)
def get_page(page_id: str):
    """获取生成的页面 · 浏览器直接访问"""
    data = load(page_id)
    if not data:
        return HTMLResponse(
            content="<h1 style='text-align:center;margin-top:20%'>页面不存在 · CNSH-9622</h1>",
            status_code=404,
        )
    return HTMLResponse(content=data["content"])


@router.get("/pages")
def get_pages(limit: int = 20):
    """列出最近生成的页面"""
    return {"pages": list_pages(limit=limit)}


@router.get("/health")
def health():
    return {
        "status": "ok",
        "version": "2.0.0",
        "dna": "#CNSH-9622",
        "system": "CNSH MVP v2.0",
    }
