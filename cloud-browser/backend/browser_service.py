# -*- coding: utf-8 -*-
"""
龍魂·云浏览器服务 v2.0（全平台生态版）
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时-☰乾-CLOUD-BROWSER-v2.0-FULL-PLATFORM
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
协议: 数据主权归用户（登录凭据只存自己的服务器·加密备份·不传第三方）

核心能力:
  - launch_persistent_context → 登录态自动落盘持久化（登录一次·AI 永久复用）
  - 单 worker 串行队列 → 规避 Playwright sync 多线程并发崩溃
  - 全平台生态: platforms.yaml(39平台·6大类) + PlatformDispatcher 自然语言调度
  - API: open/action(goto,click,type,fill,wait)/screenshot/snapshot/profiles
         /platforms(平台列表) /execute(一句话执行) /vault backup(加密备份)
  - 安全: 强 Token 鉴权(恒时比较防时序攻击) · 操作日志脱敏 · 档案加密备份
"""

import os
import queue
import secrets
import threading
import time
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException, Response
from pydantic import BaseModel

from playwright.sync_api import sync_playwright
from platform_dispatcher import PlatformDispatcher

# ---------------- 配置 ----------------
BASE_DIR = Path(os.getenv("BROWSER_DATA_DIR", "/data/browser"))
PROFILE_DIR = BASE_DIR / "profiles"
VAULT_DIR = BASE_DIR / "vault"
LOG_FILE = BASE_DIR / "browser.log"
# 🔥 强 Token：必须由环境变量注入（.env 生成 64 位随机值），无默认值则拒绝服务
TOKEN = os.getenv("BROWSER_API_TOKEN", "")
if not TOKEN:
    raise RuntimeError("BROWSER_API_TOKEN 未配置！请在 .env 中设置 64 位随机 Token")

# 全平台调度器（platforms.yaml · 39 平台）
dispatcher = PlatformDispatcher()

PROFILE_DIR.mkdir(parents=True, exist_ok=True)
VAULT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------- 优雅关闭 ----------------
_contexts: dict = {}


def _shutdown_all():
    """优雅关闭所有持久化浏览器：正常 close 让 Chromium 把 cookie/localStorage 刷盘"""
    _log(">>> shutdown 信号收到，开始优雅关闭浏览器")
    task_queue.put(("__close_all__", "", "__close_all__", {}))
    deadline = time.time() + 15
    while time.time() < deadline:
        if not any(isinstance(t, tuple) and t[0] == "__close_all__" for t in task_queue.queue):
            break
        time.sleep(0.2)
    _log("全部浏览器已优雅关闭（登录态已刷盘）")


@asynccontextmanager
async def lifespan(app):
    yield
    _shutdown_all()


app = FastAPI(title="龍魂·云浏览器服务", version="1.0.0", lifespan=lifespan)

# ---------------- 单 worker 串行队列 ----------------
task_queue: "queue.Queue[tuple]" = queue.Queue()
results: dict = {}
_task_lock = threading.Lock()
_counter = 0


def _log(msg: str):
    """审计日志：谁/何时/做什么/结果（脱敏·绝不打印 cookie 原文）"""
    line = f"[{datetime.now().isoformat()}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def _check_token(authorization: Optional[str]):
    """恒时比较防时序攻击"""
    if not authorization:
        raise HTTPException(status_code=401, detail="缺少鉴权 Token")
    token = authorization.removeprefix("Bearer ").strip()
    if not secrets.compare_digest(token, TOKEN):
        raise HTTPException(status_code=401, detail="Token 无效")


def _submit(profile: str, action: str, args: dict):
    """提交任务到串行队列并等待结果（30s 超时）"""
    global _counter
    with _task_lock:
        _counter += 1
        task_id = f"t{_counter}"
    task_queue.put((task_id, profile, action, args))
    deadline = time.time() + 45
    while time.time() < deadline:
        if task_id in results:
            r = results.pop(task_id)
            if not r["ok"]:
                raise HTTPException(status_code=500, detail=r["error"])
            return r["result"]
        time.sleep(0.1)
    raise HTTPException(status_code=504, detail="浏览器操作超时")


def _page_text(page) -> dict:
    """提取页面可读快照（AI 理解页面用）"""
    try:
        text = page.evaluate(
            "() => document.body ? document.body.innerText.slice(0, 4000) : ''"
        )
    except Exception:
        text = ""
    inputs, buttons, links = [], [], []
    try:
        inputs = page.evaluate(
            """() => Array.from(document.querySelectorAll('input')).map((el, i) => ({
                idx: i,
                type: el.type || 'text',
                name: el.name || '',
                placeholder: el.placeholder || '',
                value: el.value ? '***' : '',
            })).slice(0, 30)"""
        )
    except Exception:
        pass
    try:
        buttons = page.evaluate(
            """() => Array.from(document.querySelectorAll('button, [role=button], input[type=button], input[type=submit]')).map(el =>
                (el.innerText || el.value || '').trim()).filter(t => t.length > 0 && t.length < 30).slice(0, 40)"""
        )
    except Exception:
        pass
    try:
        links = page.evaluate(
            """() => Array.from(document.querySelectorAll('a')).map(el =>
                (el.innerText || '').trim()).filter(t => t.length > 0 && t.length < 40).slice(0, 30)"""
        )
    except Exception:
        pass
    return {
        "url": page.url,
        "title": page.title(),
        "text": text,
        "inputs": inputs,
        "buttons": buttons,
        "links": links,
    }


def _dispatch(action: str, page, ctx, args: dict):
    """执行具体浏览器动作"""
    a = action.lower()

    if a == "open":
        page.goto(args["url"], wait_until="domcontentloaded", timeout=30000)
        time.sleep(1.2)
        return _page_text(page)

    if a == "goto":
        page.goto(args["url"], wait_until="domcontentloaded", timeout=30000)
        time.sleep(1.2)
        return _page_text(page)

    if a == "click":
        page.click(args["selector"], timeout=15000)
        time.sleep(1.0)
        return _page_text(page)

    if a == "eval":
        # 在页面主文档/iframe/shadow DOM 中执行 JS，用于处理特殊弹窗
        script = args.get("script", "")
        result = page.evaluate(script)
        time.sleep(0.5)
        return {"ok": True, "result": result}

    if a == "type":
        sel = args["selector"]
        text = args["text"]
        try:
            page.fill(sel, text, timeout=10000)
        except Exception:
            page.click(sel)
            page.keyboard.type(text)
        time.sleep(0.3)
        return {"ok": True, "filled": sel}

    if a == "press":
        page.keyboard.press(args["key"])
        time.sleep(0.6)
        return {"ok": True}

    if a == "wait":
        time.sleep(args.get("ms", 1500) / 1000)
        return {"ok": True}

    if a == "screenshot":
        png = page.screenshot(timeout=15000)
        return {"png_base64": png.decode("base64") if False else __import__("base64").b64encode(png).decode()}

    if a == "snapshot":
        return _page_text(page)

    if a == "cookies":
        # 数据主权：只返回域名与数量，绝不返回 cookie 值
        cks = ctx.cookies()
        domains = {}
        for c in cks:
            d = c.get("domain", "")
            domains[d] = domains.get(d, 0) + 1
        return {"count": len(cks), "domains": domains, "note": "cookie 值永不外泄"}

    if a == "login-check":
        # 判断登录态：返回页面标题/URL/是否有业务 cookie/关键文本
        cks = ctx.cookies()
        return {
            "url": page.url,
            "title": page.title(),
            "cookie_count": len(cks),
            "cookie_domains": sorted({c.get("domain", "") for c in cks}),
            "text_snippet": _page_text(page).get("text", "")[:800],
        }

    if a == "close":
        ctx.close()
        return {"ok": True, "closed": True}

    raise HTTPException(status_code=400, detail=f"未知动作: {action}")


def _worker():
    """单线程浏览器 worker：所有操作串行执行（Playwright sync 单线程约束）"""
    global _contexts
    _log("云浏览器 worker 已启动")
    with sync_playwright() as p:
        contexts: dict = {}
        _contexts = contexts
        while True:
            task = task_queue.get()
            task_id, profile, action, args = task
            if action == "__close_all__":
                for name, ctx in contexts.items():
                    try:
                        ctx.close()  # 正常关闭→cookie/localStorage 刷盘
                        _log(f"[{name}] 已关闭并刷盘")
                    except Exception as e:
                        _log(f"[{name}] 关闭异常: {e}")
                contexts.clear()
                task_queue.task_done()
                break
            try:
                if profile not in contexts:
                    ctx = p.chromium.launch_persistent_context(
                        user_data_dir=str(PROFILE_DIR / profile),
                        headless=os.getenv("HEADLESS", "1") == "1",
                        args=["--no-sandbox", "--disable-dev-shm-usage"],
                        viewport={"width": 1280, "height": 900},
                    )
                    contexts[profile] = ctx
                    _log(f"[{profile}] 持久化浏览器已启动（登录态落盘 {PROFILE_DIR / profile}）")
                ctx = contexts[profile]
                page = ctx.pages[0] if ctx.pages else ctx.new_page()
                result = _dispatch(action, page, ctx, args)
                results[task_id] = {"ok": True, "result": result}
            except Exception as e:
                _log(f"[{profile}] {action} 失败: {e}")
                results[task_id] = {"ok": False, "error": str(e)}
            finally:
                task_queue.task_done()


threading.Thread(target=_worker, daemon=True).start()

# ---------------- API ----------------
class OpenRequest(BaseModel):
    profile: str
    url: str


class ActionRequest(BaseModel):
    profile: str
    action: str
    args: dict = {}


class BackupRequest(BaseModel):
    profile: str


@app.get("/health")
def health():
    # 公开探活端点：只返回服务状态，不含档案列表（档案列表需鉴权走 /api/profiles）
    return {
        "ok": True,
        "service": "龍魂·云浏览器",
        "version": "2.0.0",
        "platforms": len(dispatcher.list_platforms()),
        "time": datetime.now().isoformat(),
    }


@app.post("/api/browser/open")
def browser_open(req: OpenRequest, authorization: Optional[str] = Header(None)):
    _check_token(authorization)
    _log(f"open {req.profile} -> {req.url}")
    return _submit(req.profile, "open", {"url": req.url})


@app.post("/api/browser/action")
def browser_action(req: ActionRequest, authorization: Optional[str] = Header(None)):
    _check_token(authorization)
    _log(f"action {req.profile} {req.action} {json.dumps(req.args, ensure_ascii=False)[:120]}")
    return _submit(req.profile, req.action, req.args)


@app.get("/api/browser/screenshot")
def browser_screenshot(profile: str, authorization: Optional[str] = Header(None)):
    _check_token(authorization)
    data = _submit(profile, "screenshot", {})
    png = __import__("base64").b64decode(data["png_base64"])
    return Response(content=png, media_type="image/png")


@app.get("/api/profiles")
def list_profiles(authorization: Optional[str] = Header(None)):
    _check_token(authorization)
    profiles = []
    for p in PROFILE_DIR.iterdir():
        if p.is_dir():
            size_mb = sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) / 1048576
            profiles.append({"name": p.name, "size_mb": round(size_mb, 1)})
    return {"profiles": profiles}


# ---------------- 全平台生态（v2.0 新增） ----------------
@app.get("/api/platforms")
def api_platforms(authorization: Optional[str] = Header(None)):
    """列出全部已接入平台（按类目分组）"""
    _check_token(authorization)
    plats = dispatcher.list_platforms()
    by_cat: dict = {}
    for p in plats:
        by_cat.setdefault(p["category"], []).append(p)
    _log(f"platforms list: {len(plats)} 个")
    return {"total": len(plats), "categories": by_cat}


class ExecuteRequest(BaseModel):
    command: str                       # 自然语言指令，如「打开阿里云开通短信服务」
    max_platforms: int = 3             # 单次最多操作平台数


@app.post("/api/execute")
def api_execute(req: ExecuteRequest, authorization: Optional[str] = Header(None)):
    """一句话执行：解析指令 → 打开目标平台 → 返回页面快照（AI 可接着精细化操作）"""
    _check_token(authorization)
    if not req.command.strip():
        raise HTTPException(status_code=400, detail="指令不能为空")

    plan = dispatcher.dispatch(req.command)
    if not plan:
        raise HTTPException(status_code=400, detail="未识别到目标平台。试试：在CSDN发布文章 / 打开阿里云 / 搜索龍魂系统")

    _log(f"execute: {req.command[:80]} → {[p.platform for p in plan]}")
    steps = []
    for pa in plan[: req.max_platforms]:
        profile = pa.platform  # 每个平台独立档案 → 独立登录态
        try:
            r = _submit(profile, "open", {"url": pa.url})
            steps.append({
                "platform": pa.platform_name,
                "profile": profile,
                "url": pa.url,
                "intent": pa.action,
                "target": pa.target[:120],
                "ok": True,
                "page": {"title": r.get("title"), "url": r.get("url"),
                         "text_head": (r.get("text") or "")[:500],
                         "buttons": r.get("buttons", [])[:20],
                         "inputs": len(r.get("inputs", []))},
            })
        except HTTPException as e:
            steps.append({"platform": pa.platform_name, "profile": profile,
                          "url": pa.url, "intent": pa.action, "ok": False, "error": e.detail})

    ok = sum(1 for s in steps if s.get("ok"))
    return {
        "command": req.command[:120],
        "plan": [{"platform": p.platform, "name": p.platform_name,
                  "action": p.action, "url": p.url} for p in plan[: req.max_platforms]],
        "steps": steps,
        "summary": f"打开 {ok}/{len(steps)} 个平台",
        "note": "平台已打开，AI 可继续用 /api/browser/action 精细化操作（点击/输入/截图）",
    }


@app.post("/api/vault/backup")
def vault_backup(req: BackupRequest, authorization: Optional[str] = Header(None)):
    """加密备份登录档案到保险柜（gpg 对称加密·密钥由环境变量注入）"""
    _check_token(authorization)
    src = PROFILE_DIR / req.profile
    if not src.exists():
        raise HTTPException(status_code=404, detail="档案不存在")
    key = os.getenv("BROWSER_VAULT_KEY", "")
    if not key:
        raise HTTPException(status_code=400, detail="未配置加密密钥 BROWSER_VAULT_KEY")
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    out = VAULT_DIR / f"{req.profile}-{ts}.tar.gz.gpg"
    try:
        subprocess.run(
            ["tar", "czf", "-", "-C", str(PROFILE_DIR), req.profile],
            stdout=open("/tmp/_vb.tar.gz", "wb"), check=True,
        )
        subprocess.run(
            ["gpg", "--batch", "--yes", "--pinentry-mode", "loopback",
             "--passphrase", key, "-c", "--cipher-algo", "AES256",
             "-o", str(out), "/tmp/_vb.tar.gz"],
            check=True,
        )
        os.remove("/tmp/_vb.tar.gz")
        _log(f"vault backup {req.profile} -> {out.name}")
        return {"ok": True, "backup": out.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"备份失败: {e}")


@app.get("/api/vault/list")
def vault_list(authorization: Optional[str] = Header(None)):
    _check_token(authorization)
    backups = sorted(VAULT_DIR.glob("*.gpg"), key=lambda f: f.stat().st_mtime, reverse=True)
    return {"backups": [f.name for f in backups[:30]]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("BROWSER_API_PORT", "8899")))
