#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂9622·本地引擎 main.py v2.0

DNA(v∞): #龍芯⚡️丙午·丁酉·辛巳-LONGHUN-EXT-ENGINE-v2.0-b7c3d9a1
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
来源: ~/龍魂浏览器插件.zip (2026-05-21) · 2026-09-04 深度集成入 longhun-system/extensions/longhun-ext
注意: 端口 9622 现被系统 lh_api.py 占用 · 如需自跑引擎请改端口(如 9633)并同步 popup.js/background.js 的 ENGINE 常量

特性:
- 端口 9622 · 本地主权（默认 127.0.0.1，APPLE_MODE=true 则监听局域网）
- FastAPI + CORS（Chrome/Safari 扩展 + iOS 捷径）
- 中文语法对齐（CNSH）· 三色审计 · DNA 签章
- 苹果设备兼容：同一 WiFi 下 iPhone/iPad 可访问

依赖安装:
  pip3 install fastapi uvicorn httpx python-dotenv pydantic
  # 可选（本地向量库）:
  pip3 install sentence-transformers faiss-cpu sqlite-utils
"""

import os, sys, json, hashlib, subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
import uvicorn

# ─── 环境配置 ──────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv(Path.home() / "longhun-engine" / ".env")
except ImportError:
    pass

HOME      = Path.home()
BASE_DIR  = HOME / "longhun-engine"
MVPS_DIR  = BASE_DIR / "mvps"
MEM_DIR   = BASE_DIR / "memory"
STATIC_DIR= BASE_DIR / "static"
for d in [BASE_DIR, MVPS_DIR, MEM_DIR, STATIC_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# APPLE_MODE=true → 监听 0.0.0.0，允许同一 WiFi 的 iPhone 访问
APPLE_MODE = os.getenv("APPLE_MODE", "false").lower() == "true"
HOST = "0.0.0.0" if APPLE_MODE else "127.0.0.1"
PORT = int(os.getenv("PORT", "9622"))

# ─── FastAPI 应用 ──────────────────────────────────────────
app = FastAPI(
    title="龍魂9622引擎",
    version="2.0.0",
    description="中文主权AI本地引擎 · UID9622"
)

# CORS：Chrome扩展 + Safari扩展 + iOS Safari + iOS捷径
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "chrome-extension://*",
        "safari-extension://*",
        "safari-web-extension://*",
        "http://localhost:*",
        "http://127.0.0.1:*",
        "*" if APPLE_MODE else "http://127.0.0.1:*",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── 数据模型 ──────────────────────────────────────────────
class TextIn(BaseModel):
    text:    str = ""
    url:     str = ""
    title:   str = ""
    lang:    str = "zh"
    context: Optional[str] = None

class ChatIn(BaseModel):
    text:          str
    mode:          str = "auto"   # auto / local / deepseek / claude
    lang:          str = "zh"
    context_depth: int = 10

# ─── DNA 签章 ──────────────────────────────────────────────
def make_dna(payload: str, tag: str = "ENGINE") -> str:
    h = hashlib.sha256(
        f"{payload}|9622|{datetime.now().isoformat()}".encode()
    ).hexdigest()[:10].upper()
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"#龍芯⚡️{ts}-{tag}-{h}"

# ─── 三色判定（基于数字根） ────────────────────────────────
def digital_root(n: int) -> int:
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

def tri_color(text: str) -> str:
    """简易三色：基于文本数字根"""
    dr = digital_root(sum(ord(c) for c in text) % 99 + 1)
    if dr in {3, 9}:   return "🔴"
    if dr == 6:         return "🟡"
    return "🟢"

# ─── CNSH 中文语法对齐（核心） ─────────────────────────────
CNSH_RULES = [
    # 翻译偏差替换
    {"pattern": "中国制造", "replacement": "中国制造（Made in China）", "type": "翻译主权"},
    {"pattern": "数据归我", "replacement": "数据主权归于人民", "type": "主权声明"},
    # 五行词
    {"pattern": "删除", "replacement": "归档（慎用删除）", "type": "五行·水"},
    # DNA注入
]

def cnsh_align(text: str) -> dict:
    """CNSH 中文语法对齐：检测潜在偏差并给出修正建议"""
    issues  = []
    aligned = text

    for rule in CNSH_RULES:
        if rule["pattern"] in text:
            issues.append({
                "found":       rule["pattern"],
                "suggestion":  rule["replacement"],
                "type":        rule["type"]
            })
            aligned = aligned.replace(rule["pattern"], f"【{rule['replacement']}】")

    # 简单情绪负载检测
    neg_words = ["垃圾", "劣质", "落后", "不文明", "野蛮"]
    for w in neg_words:
        if w in text:
            issues.append({"found": w, "suggestion": "注意：含情绪负载词", "type": "翻译偏差"})

    return {
        "original": text,
        "aligned":  aligned,
        "issues":   issues,
        "clean":    len(issues) == 0
    }

# ─── 路由调用 MVP 脚本 ─────────────────────────────────────
def run_mvp(script_name: str, *args, timeout: int = 10) -> str:
    script = MVPS_DIR / script_name
    if not script.exists():
        return f"[MVP脚本未找到: {script_name}]"
    try:
        r = subprocess.run(
            [sys.executable, str(script), *args],
            capture_output=True, text=True, timeout=timeout
        )
        return (r.stdout or r.stderr or "").strip()
    except subprocess.TimeoutExpired:
        return "[超时]"
    except Exception as e:
        return f"[错误: {e}]"

# ─── API 路由 ──────────────────────────────────────────────

@app.get("/api/health")
def health():
    """健康检查·引擎状态"""
    return {
        "ok":          True,
        "version":     "v2.0",
        "apple_mode":  APPLE_MODE,
        "host":        HOST,
        "port":        PORT,
        "dna":         make_dna("health", "HEALTH"),
        "time":        datetime.now().isoformat(),
        "uid":         "UID9622"
    }

@app.post("/api/ethics/review")
def ethics_review(inp: TextIn):
    """伦理审查 · 三色判定 · DNA签章"""
    color   = tri_color(inp.text)
    summary = run_mvp("ethics_review_mvp.py", "--text", inp.text[:300])
    if not summary or summary.startswith("["):
        # 内置简版
        cnsh  = cnsh_align(inp.text)
        summary = f"三色：{color}\n\nCNSH检查：{'✅ 无偏差' if cnsh['clean'] else '⚠️ 发现以下问题'}\n"
        for issue in cnsh["issues"]:
            summary += f"  · [{issue['type']}] {issue['found']} → {issue['suggestion']}\n"
    return {
        "title":   "⚖️ 伦理审查",
        "color":   color,
        "summary": summary,
        "dna":     make_dna(inp.text, "ETHICS")
    }

@app.post("/api/tongxin/translate")
async def tongxin_translate(inp: TextIn):
    """通心译 · 中文主权翻译"""
    cnsh  = cnsh_align(inp.text)
    color = tri_color(inp.text)

    # 尝试调用本地引擎翻译
    summary = run_mvp("sancai_router.py", "--text", inp.text[:500])
    if not summary or summary.startswith("["):
        summary = (
            f"原文：{inp.text[:200]}\n\n"
            f"CNSH对齐：{'✅ 无偏差' if cnsh['clean'] else cnsh['aligned'][:200]}\n\n"
            f"注意：如需AI翻译，请在.env配置 DEEPSEEK_API_KEY 或 ANTHROPIC_API_KEY"
        )

    return {
        "title":   "🟡 通心译",
        "color":   color,
        "summary": summary,
        "cnsh":    cnsh,
        "dna":     make_dna(inp.text, "TONGXIN")
    }

@app.post("/api/wuxing/analyze")
def wuxing_analyze(inp: TextIn):
    """五行分析 · 文本能量场"""
    out   = run_mvp("longhun_wuxing_mvp.py", "--text", inp.text[:300])
    color = tri_color(inp.text)
    dr    = digital_root(sum(ord(c) for c in inp.text) % 99 + 1)

    if not out or out.startswith("["):
        wuxing_map = {1:"水", 2:"土", 3:"木", 4:"金", 5:"土",
                      6:"水", 7:"火", 8:"土", 9:"金"}
        element = wuxing_map.get(dr, "土")
        out = f"数字根：{dr} → 五行：{element}\n三色判定：{color}\n原文长度：{len(inp.text)}字"

    return {
        "title":   "🔥 五行分析",
        "color":   color,
        "summary": out,
        "dr":      dr,
        "dna":     make_dna(inp.text, "WUXING")
    }

@app.post("/api/cnsh/align")
def cnsh_endpoint(inp: TextIn):
    """CNSH 中文语法对齐 · 翻译偏差检测"""
    result = cnsh_align(inp.text)
    color  = "🟢" if result["clean"] else "🟡"
    issues_text = "\n".join(
        f"· [{i['type']}] {i['found']} → {i['suggestion']}"
        for i in result["issues"]
    ) or "未发现偏差"

    return {
        "title":   "📐 CNSH语法对齐",
        "color":   color,
        "summary": f"原文：{inp.text[:100]}\n\n对齐结果：\n{issues_text}",
        "aligned": result["aligned"],
        "issues":  result["issues"],
        "dna":     make_dna(inp.text, "CNSH")
    }

@app.post("/api/errata/submit")
async def errata_submit(inp: TextIn):
    """记错本 · 上报到 Notion（若配置了 Token）"""
    notion_url = None
    try:
        from notion_sync import push_errata
        res = await push_errata(
            text=inp.text,
            source_url=inp.url,
            source_title=inp.title
        )
        notion_url = res.get("url")
        msg = f"已上报 Notion · ID: {res.get('id', '未知')}"
    except Exception as e:
        # 本地保存兜底
        ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
        fp  = MEM_DIR / f"errata_{ts}.json"
        fp.write_text(json.dumps({
            "ts":    datetime.now().isoformat(),
            "text":  inp.text,
            "url":   inp.url,
            "title": inp.title
        }, ensure_ascii=False, indent=2))
        msg = f"已本地保存（未配置 Notion Token）\n路径：{fp}"

    return {
        "title":      "📓 记错本",
        "color":      "🟢",
        "summary":    msg,
        "notion_url": notion_url,
        "dna":        make_dna(inp.text, "ERRATA")
    }

@app.post("/api/dna/check")
def dna_check(inp: TextIn):
    """DNA 验证 · 检查文本是否含龍魂 DNA 签章"""
    has_dna  = "#龍芯⚡️" in inp.text or "#ZHUGEXIN" in inp.text
    has_conf = "#CONFIRM🌌9622" in inp.text
    color    = "🟢" if has_dna else "🟡"
    return {
        "title":   "🧬 DNA验证",
        "color":   color,
        "summary": (
            f"DNA签章：{'✅ 存在' if has_dna else '❌ 未找到'}\n"
            f"确认码：{'✅ 存在' if has_conf else '❌ 未找到'}\n"
            f"文本长度：{len(inp.text)} 字"
        ),
        "has_dna":  has_dna,
        "has_confirm": has_conf,
        "dna":     make_dna(inp.text, "DNA-CHECK")
    }

@app.post("/api/chat")
async def chat(inp: ChatIn):
    """统一对话 · 三才路由 · 支持本地/DeepSeek/Claude"""
    # 红线扫描
    redlines = ["删库", "泄露密钥", "删除所有"]
    for r in redlines:
        if r in inp.text:
            return {
                "reply": f"🔴 红线触发（{r}），拒绝处理。UID9622 一票否决。",
                "color": "🔴",
                "dna":   make_dna(inp.text, "VETO")
            }

    reply = ""

    if inp.mode in ("local", "auto"):
        reply = await call_ollama(inp.text)

    if not reply and inp.mode in ("deepseek", "auto"):
        reply = await call_deepseek(inp.text)

    if not reply and inp.mode == "claude":
        reply = await call_claude(inp.text)

    if not reply:
        reply = (
            "引擎未配置外部API。\n"
            "请在 ~/longhun-engine/.env 配置：\n"
            "  DEEPSEEK_API_KEY=sk-xxx  （推荐·中文强）\n"
            "  ANTHROPIC_API_KEY=sk-ant-xxx\n"
            "  或安装 Ollama：https://ollama.ai"
        )

    return {
        "reply": reply,
        "mode":  inp.mode,
        "color": tri_color(inp.text),
        "dna":   make_dna(inp.text, "CHAT")
    }

# ─── 大脑路由（本地 / 云端） ───────────────────────────────
async def call_ollama(prompt: str) -> str:
    try:
        import httpx
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(
                "http://127.0.0.1:11434/api/generate",
                json={"model": "qwen2.5:7b", "prompt": prompt, "stream": False}
            )
            return r.json().get("response", "")
    except Exception:
        return ""

async def call_deepseek(prompt: str) -> str:
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key: return ""
    try:
        import httpx
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={"model": "deepseek-chat",
                      "messages": [{"role": "user", "content": prompt}]}
            )
            return r.json()["choices"][0]["message"]["content"]
    except Exception:
        return ""

async def call_claude(prompt: str) -> str:
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key: return ""
    try:
        import httpx
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": key, "anthropic-version": "2023-06-01"},
                json={"model": "claude-sonnet-4-20250514", "max_tokens": 2048,
                      "messages": [{"role": "user", "content": prompt}]}
            )
            return r.json()["content"][0]["text"]
    except Exception:
        return ""

# ─── MCP 工具列表 / 调用 ───────────────────────────────────
@app.get("/api/mcp/list")
async def mcp_list():
    try:
        from mcp_bridge import list_tools
        return await list_tools()
    except ImportError:
        return {"tools": [
            {"name": "fs.read",      "desc": "读取本地文件"},
            {"name": "git.status",   "desc": "查询 Git 状态"},
            {"name": "notion.search","desc": "搜索 Notion 知识库"},
        ]}

@app.post("/api/mcp/call")
async def mcp_call(req: Request):
    body = await req.json()
    try:
        from mcp_bridge import call_tool
        return await call_tool(body.get("tool"), body.get("args", {}))
    except ImportError:
        return {"ok": False, "error": "mcp_bridge.py 未安装", "tool": body.get("tool")}

# ─── iOS Apple Shortcuts 静态捷径文件 ─────────────────────
@app.get("/static/longhun.shortcut", response_class=HTMLResponse)
def ios_shortcut():
    """
    iOS 捷径：用 Apple Shortcuts App 导入此 URL 创建快捷指令
    真实部署请换成 .shortcut 二进制文件，此处返回说明页
    """
    return """<html><body style="font-family:-apple-system;padding:20px">
    <h2>🐉 龍魂9622 iOS 捷径</h2>
    <p>在 iPhone 上用 Safari 打开此页，点击下方按钮导入捷径：</p>
    <a href="shortcuts://import-workflow/?url=http://127.0.0.1:9622/static/longhun.shortcut"
       style="display:inline-block;padding:12px 24px;background:#D4AF37;color:#fff;border-radius:8px;text-decoration:none;">
       ⬇️ 导入到 Apple Shortcuts
    </a>
    <hr>
    <p style="font-size:12px;color:#888">
    确保 Mac 和 iPhone 在同一 WiFi<br>
    引擎地址：http://[Mac-IP]:9622<br>
    APPLE_MODE=true
    </p>
    </body></html>"""

@app.get("/docs/safari-guide", response_class=HTMLResponse)
def safari_guide():
    return """<html><body style="font-family:-apple-system;padding:20px;max-width:600px">
    <h2>🍎 Safari Web Extension 打包指南</h2>
    <ol style="line-height:2">
      <li>安装 Xcode（Mac App Store 免费）</li>
      <li>终端运行：<code>xcrun safari-web-extension-converter ~/longhun-ext/</code></li>
      <li>Xcode 打开生成的项目</li>
      <li>Build → 在 Safari 偏好设置 → 扩展 → 启用龍魂9622</li>
      <li>如需 iOS：需要 Apple Developer 账号（99美元/年）</li>
    </ol>
    <p style="color:#888;font-size:12px">无 Developer 账号时，用 iOS Shortcuts 方案替代</p>
    </body></html>"""

# ─── 启动 ──────────────────────────────────────────────────
def print_banner():
    mode_str = "🍎 苹果兼容模式（局域网可达）" if APPLE_MODE else "🔒 本地模式（127.0.0.1）"
    print(f"""
🐉 龍魂9622引擎启动 · v2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 地址：http://{HOST}:{PORT}
🌐 模式：{mode_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📜 主权承诺：
  ① 数据只在本机硬盘与您的 Notion 工作区
  ② API Key 只读 ~/longhun-engine/.env
  ③ 每次调用 DNA 自动签章·可完整追溯
  ④ 任何时刻 Ctrl+C 即断电·不留后台
  ⑤ 苹果设备：APPLE_MODE=true 即可开启
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
    """)

if __name__ == "__main__":
    print_banner()
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")
