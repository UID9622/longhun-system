#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷍大有-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
"""Web UI for LongHun WeChat Public Account integration."""

import json
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, Form, HTTPException, Request, UploadFile  # type: ignore[import-untyped]
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import-untyped]
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles  # type: ignore[import-untyped]
from fastapi.templating import Jinja2Templates  # type: ignore[import-untyped]

from config import get_settings  # type: ignore[import-untyped]
from core import ArticleManager, MediaManager, WeChatClient  # type: ignore[import-untyped]
from services import ImageService, PersonaService, VoiceService  # type: ignore[import-untyped]

app = FastAPI(
    title="龍魂生态智能内容中枢",
    description="微信公众号 + 小程序 + AI 配图 + 语音 + 人格管理",
    version="1.0.0",
)

# CORS for mini program and web clients（🛡️ P77修复：白名单替代通配符）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8766", "http://127.0.0.1:8766"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-DNA-TRACE"],
)

# Static and templates
static_dir = Path(__file__).parent / "static"
templates_dir = Path(__file__).parent / "templates"
static_dir.mkdir(parents=True, exist_ok=True)
templates_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))


def get_status():
    """Get system status."""
    settings = get_settings()
    status = settings.validate_wechat()
    return {
        "wechat_ok": status["ok"],
        "wechat_errors": status["errors"],
        "appid": status["appid"],
        "kimi_configured": bool(settings.KIMI_API_KEY),
        "deepseek_configured": bool(settings.DEEPSEEK_API_KEY),
        "openai_configured": bool(settings.OPENAI_API_KEY),
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main dashboard."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "status": get_status(),
            "personas": PersonaService().list_personas(),
        },
    )


@app.get("/api/status")
async def api_status():
    """API status endpoint."""
    return get_status()


@app.post("/api/token/refresh")
async def api_token_refresh():
    """Refresh WeChat access token."""
    try:
        client = WeChatClient()
        token = client.get_access_token(force_refresh=True)
        return {"ok": True, "token_prefix": token[:16] + "..."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/drafts")
async def api_list_drafts(offset: int = 0, count: int = 20):
    """List draft articles."""
    try:
        manager = ArticleManager()
        result = manager.list_drafts(offset=offset, count=count)
        return {"ok": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/drafts/create")
async def api_create_draft(
    title: str = Form(...),
    content: str = Form(...),
    author: Optional[str] = Form(None),
    digest: Optional[str] = Form(None),
    source_url: Optional[str] = Form(None),
    cover: Optional[UploadFile] = None,
    publish: bool = Form(False),
):
    """Create draft and optionally publish."""
    try:
        manager = ArticleManager()

        cover_path = None
        if cover and cover.filename:
            cover_path = manager.client.cache_dir / f"upload_{cover.filename}"
            cover_path.write_bytes(await cover.read())
            cover_path = str(cover_path)

        result = manager.create_draft(
            title=title,
            content=content,
            author=author,
            digest=digest,
            cover_image_path=cover_path,
            source_url=source_url,
        )

        publish_result = None
        if publish:
            publish_result = manager.publish(result["media_id"])

        return {
            "ok": True,
            "media_id": result["media_id"],
            "publish_result": publish_result,
            "dna": manager.generate_dna("DRAFT" if not publish else "PUBLISH"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/publish/{media_id}")
async def api_publish(media_id: str):
    """Publish a draft."""
    try:
        manager = ArticleManager()
        result = manager.publish(media_id)
        return {
            "ok": True,
            "publish_id": result.get("publish_id"),
            "msg_data_id": result.get("msg_data_id"),
            "dna": manager.generate_dna("PUBLISH"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/drafts/delete")
async def api_delete_draft(media_id: str = Form(...)):
    """Delete a draft."""
    try:
        manager = ArticleManager()
        manager.delete_draft(media_id)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/image/generate")
async def api_image_generate(
    prompt: str = Form(...),
    width: int = Form(900),
    height: int = Form(500),
    style: str = Form("chinese_ink"),
):
    """Generate image."""
    try:
        service = ImageService()
        path = service.generate(prompt=prompt, width=width, height=height, style=style)
        return {"ok": True, "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/voice/generate")
async def api_voice_generate(
    text: str = Form(...),
    style: str = Form("educator"),
    soul: bool = Form(False),
):
    """Generate voice."""
    try:
        service = VoiceService()
        path = service.generate(text=text, style=style, use_soul=soul)
        return {"ok": True, "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/personas")
async def api_list_personas():
    """List personas."""
    return {"ok": True, "personas": PersonaService().list_personas()}


@app.post("/api/personas/run")
async def api_run_persona(
    task: str = Form(...),
    persona_id: Optional[str] = Form(None),
):
    """Run a persona task."""
    try:
        service = PersonaService()
        result = service.route_task(task, persona_id=persona_id)
        return {"ok": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/media/upload")
async def api_media_upload(
    file: UploadFile = ...,  # type: ignore[assignment]  # FastAPI required-param pattern
    media_type: str = Form(...),
    title: Optional[str] = Form(None),
    introduction: Optional[str] = Form(None),
):
    """Upload media material."""
    try:
        media = MediaManager()
        tmp_path = media.client.cache_dir / f"media_{file.filename}"
        tmp_path.write_bytes(await file.read())

        result = media.upload_material(
            str(tmp_path),
            material_type=media_type,
            title=title,
            introduction=introduction,
        )
        return {"ok": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _extract_description(file_path: Path, max_len: int = 120) -> str:
    """Extract a short description from markdown content."""
    try:
        text = file_path.read_text(encoding="utf-8")
        # Skip title line and find first non-empty paragraph
        lines = text.splitlines()
        desc_lines = []
        found_title = False
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#") and not found_title:
                found_title = True
                continue
            if stripped.startswith("#"):
                continue
            desc_lines.append(stripped)
            if len("".join(desc_lines)) >= max_len:
                break
        desc = " ".join(desc_lines)
        return desc[:max_len] + "..." if len(desc) > max_len else desc
    except Exception:
        return ""


def _markdown_to_html(text: str) -> str:
    """Minimal markdown to HTML converter for mini program rich-text."""
    import re

    lines = text.splitlines()
    out = []
    in_paragraph = False

    def close_p():
        nonlocal in_paragraph
        if in_paragraph:
            out.append("</p>")
            in_paragraph = False

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            close_p()
            continue

        # Headers
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            close_p()
            level = len(m.group(1))
            title = _escape_html(m.group(2))
            out.append(f'<h{level} style="font-weight:bold;margin:16px 0 8px 0;color:#1a1a2e;">{title}</h{level}>')
            continue

        # Bold/italic
        line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
        line = re.sub(r"\*(.+?)\*", r"<em>\1</em>", line)
        line = _escape_html(line)
        line = line.replace("&lt;strong&gt;", "<strong>").replace("&lt;/strong&gt;", "</strong>")
        line = line.replace("&lt;em&gt;", "<em>").replace("&lt;/em&gt;", "</em>")

        if not in_paragraph:
            out.append('<p style="margin:12px 0;line-height:1.8;">')
            in_paragraph = True
        else:
            out.append("<br/>")
        out.append(line)

    close_p()
    return "".join(out)


def _escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


@app.get("/api/longhun/articles")
@app.get("/api/articles")
async def api_longhun_articles():
    """List available LongHun articles for mini program and web."""
    try:
        root = get_settings().LONGHUN_SYSTEM_ROOT / "01_protocols"
        articles = []

        # Thesis chapters
        thesis_dir = root / "THESIS-ROOT-GOVERNANCE"
        if thesis_dir.exists():
            for f in sorted(thesis_dir.glob("*.md")):
                if f.name in ["README.md", "FULL-THESIS.md"]:
                    continue
                articles.append(
                    {
                        "id": f"thesis/{f.name}",
                        "title": f.stem,
                        "path": str(f),
                        "type": "论文章节",
                        "description": _extract_description(f),
                    }
                )

        # Protocols
        for f in sorted(root.glob("*.md")):
            articles.append(
                {
                    "id": f"protocol/{f.name}",
                    "title": f.stem,
                    "path": str(f),
                    "type": "协议",
                    "description": _extract_description(f),
                }
            )

        return {"ok": True, "articles": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/longhun/article")
@app.get("/api/articles/{article_id:path}")
async def api_longhun_article(path: Optional[str] = None, article_id: Optional[str] = None):
    """Get content of a LongHun article."""
    try:
        target = path or article_id
        if not target:
            raise HTTPException(status_code=400, detail="path or article_id required")

        # Handle article_id like "thesis/02-CHAPTER-01.md"
        if article_id and not path:
            root = get_settings().LONGHUN_SYSTEM_ROOT / "01_protocols"
            if article_id.startswith("thesis/"):
                p = root / "THESIS-ROOT-GOVERNANCE" / article_id.replace("thesis/", "")
            elif article_id.startswith("protocol/"):
                p = root / article_id.replace("protocol/", "")
            else:
                raise HTTPException(status_code=404, detail="Invalid article_id")
        else:
            p = Path(target).expanduser()

        if not p.exists():
            raise HTTPException(status_code=404, detail="Article not found")

        raw_content = p.read_text(encoding="utf-8")
        html_content = _markdown_to_html(raw_content)

        article = {
            "id": article_id or str(p.name),
            "title": p.stem,
            "path": str(p),
            "type": "论文章节" if "THESIS" in str(p) else "协议",
            "description": _extract_description(p),
        }
        return {"ok": True, "article": article, "content": html_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Ensure basic template exists
def ensure_templates():
    """Create basic HTML templates if they don't exist."""
    index_html = templates_dir / "index.html"
    if not index_html.exists():
        index_html.write_text(INDEX_TEMPLATE, encoding="utf-8")


INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>龍魂公众号智能内容中枢</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background: #f5f5f5; color: #333; line-height: 1.6; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 24px; }
        header h1 { font-size: 28px; margin-bottom: 8px; }
        header p { opacity: 0.8; }
        .card { background: white; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        .card h2 { font-size: 20px; margin-bottom: 16px; color: #1a1a2e; border-left: 4px solid #e74c3c; padding-left: 12px; }
        .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }
        .status-item { padding: 12px; border-radius: 8px; background: #f8f9fa; }
        .status-item.ok { border-left: 4px solid #27ae60; }
        .status-item.error { border-left: 4px solid #e74c3c; }
        .status-item.warn { border-left: 4px solid #f39c12; }
        .btn { display: inline-block; padding: 10px 20px; background: #e74c3c; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; margin-right: 10px; margin-bottom: 10px; }
        .btn:hover { background: #c0392b; }
        .btn.secondary { background: #34495e; }
        .btn.secondary:hover { background: #2c3e50; }
        textarea, input, select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; margin-bottom: 12px; font-family: inherit; }
        textarea { min-height: 200px; resize: vertical; }
        .result { background: #f8f9fa; padding: 16px; border-radius: 8px; margin-top: 16px; white-space: pre-wrap; font-family: monospace; font-size: 13px; display: none; }
        .persona-card { display: inline-block; padding: 16px; margin: 8px; background: #f8f9fa; border-radius: 8px; min-width: 200px; }
        .persona-card .icon { font-size: 32px; margin-bottom: 8px; }
        .tabs { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
        .tab { padding: 10px 20px; background: #ecf0f1; border-radius: 6px; cursor: pointer; }
        .tab.active { background: #e74c3c; color: white; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 768px) { .grid-2 { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🐉 龍魂公众号智能内容中枢</h1>
            <p>微信公众号 × AI 配图 × 语音朗读 × 人格管理</p>
        </header>

        <div class="card">
            <h2>系统状态</h2>
            <div class="status-grid">
                <div class="status-item {{ 'ok' if status.wechat_ok else 'error' }}">
                    <strong>微信配置</strong><br>
                    {{ '✅ 已配置' if status.wechat_ok else '❌ ' + status.wechat_errors|join(', ') }}
                </div>
                <div class="status-item {{ 'ok' if status.kimi_configured else 'warn' }}">
                    <strong>Kimi API</strong><br>
                    {{ '✅ 已配置' if status.kimi_configured else '⚠️ 未配置' }}
                </div>
                <div class="status-item {{ 'ok' if status.deepseek_configured else 'warn' }}">
                    <strong>DeepSeek API</strong><br>
                    {{ '✅ 已配置' if status.deepseek_configured else '⚠️ 未配置' }}
                </div>
                <div class="status-item {{ 'ok' if status.openai_configured else 'warn' }}">
                    <strong>OpenAI API</strong><br>
                    {{ '✅ 已配置' if status.openai_configured else '⚠️ 未配置' }}
                </div>
            </div>
            <div style="margin-top: 16px;">
                <button class="btn" onclick="refreshToken()">刷新 Access Token</button>
                <button class="btn secondary" onclick="loadDrafts()">加载草稿列表</button>
                <button class="btn secondary" onclick="loadArticles()">加载龍魂文章</button>
            </div>
            <div id="statusResult" class="result"></div>
        </div>

        <div class="tabs">
            <div class="tab active" onclick="switchTab('publish')">📝 发布文章</div>
            <div class="tab" onclick="switchTab('persona')">🎭 人格创作</div>
            <div class="tab" onclick="switchTab('image')">🎨 AI 配图</div>
            <div class="tab" onclick="switchTab('voice')">🔊 AI 语音</div>
            <div class="tab" onclick="switchTab('drafts')">📚 草稿管理</div>
        </div>

        <div id="publish" class="tab-content active">
            <div class="card">
                <h2>发布文章</h2>
                <input type="text" id="pubTitle" placeholder="文章标题">
                <input type="text" id="pubAuthor" placeholder="作者（可选）">
                <input type="text" id="pubDigest" placeholder="摘要（可选）">
                <textarea id="pubContent" placeholder="文章内容，支持 Markdown"></textarea>
                <label>封面图片：</label>
                <input type="file" id="pubCover" accept="image/*">
                <label>
                    <input type="checkbox" id="pubNow"> 立即发布（不勾选则仅保存草稿）
                </label>
                <div>
                    <button class="btn" onclick="createDraft()">保存草稿 / 发布</button>
                </div>
                <div id="publishResult" class="result"></div>
            </div>
        </div>

        <div id="persona" class="tab-content">
            <div class="card">
                <h2>人格创作</h2>
                <div>
                    {% for p in personas %}
                    <div class="persona-card">
                        <div class="icon">{{ p.icon }}</div>
                        <strong>{{ p.name }}</strong>
                        <p style="font-size: 12px; color: #666;">{{ p.role }}</p>
                        <p style="font-size: 12px;">{{ p.description }}</p>
                    </div>
                    {% endfor %}
                </div>
                <select id="personaSelect">
                    <option value="">自动选择</option>
                    {% for p in personas %}
                    <option value="{{ p.id }}">{{ p.icon }} {{ p.name }}</option>
                    {% endfor %}
                </select>
                <textarea id="personaTask" placeholder="输入任务，例如：写一段关于评分恐怖主义的短文"></textarea>
                <button class="btn" onclick="runPersona()">运行人格</button>
                <div id="personaResult" class="result"></div>
            </div>
        </div>

        <div id="image" class="tab-content">
            <div class="card">
                <h2>AI 配图</h2>
                <input type="text" id="imgPrompt" placeholder="图片描述，例如：中国基层治理 三才三色">
                <div class="grid-2">
                    <input type="number" id="imgWidth" placeholder="宽度" value="900">
                    <input type="number" id="imgHeight" placeholder="高度" value="500">
                </div>
                <select id="imgStyle">
                    <option value="chinese_ink">中国水墨</option>
                    <option value="modern">现代简约</option>
                    <option value="minimal">极简</option>
                </select>
                <button class="btn" onclick="generateImage()">生成配图</button>
                <div id="imageResult" class="result"></div>
            </div>
        </div>

        <div id="voice" class="tab-content">
            <div class="card">
                <h2>AI 语音</h2>
                <textarea id="voiceText" placeholder="要朗读的文字"></textarea>
                <select id="voiceStyle">
                    <option value="educator">教育</option>
                    <option value="storyteller">讲故事</option>
                    <option value="passionate">激情</option>
                    <option value="calm">平静</option>
                </select>
                <label>
                    <input type="checkbox" id="voiceSoul"> 使用 Soul 情感语音
                </label>
                <button class="btn" onclick="generateVoice()">生成语音</button>
                <div id="voiceResult" class="result"></div>
            </div>
        </div>

        <div id="drafts" class="tab-content">
            <div class="card">
                <h2>草稿管理</h2>
                <div id="draftsList">点击上方"加载草稿列表"查看</div>
            </div>
        </div>
    </div>

    <script>
        function switchTab(name) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(name).classList.add('active');
        }

        function showResult(id, data) {
            const el = document.getElementById(id);
            el.style.display = 'block';
            el.textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
        }

        async function refreshToken() {
            const res = await fetch('/api/token/refresh', {method: 'POST'});
            const data = await res.json();
            showResult('statusResult', data);
        }

        async function createDraft() {
            const form = new FormData();
            form.append('title', document.getElementById('pubTitle').value);
            form.append('content', document.getElementById('pubContent').value);
            form.append('author', document.getElementById('pubAuthor').value);
            form.append('digest', document.getElementById('pubDigest').value);
            form.append('publish', document.getElementById('pubNow').checked);
            const cover = document.getElementById('pubCover').files[0];
            if (cover) form.append('cover', cover);

            const res = await fetch('/api/drafts/create', {method: 'POST', body: form});
            const data = await res.json();
            showResult('publishResult', data);
        }

        async function runPersona() {
            const form = new FormData();
            form.append('task', document.getElementById('personaTask').value);
            form.append('persona_id', document.getElementById('personaSelect').value);
            const res = await fetch('/api/personas/run', {method: 'POST', body: form});
            const data = await res.json();
            showResult('personaResult', data);
        }

        async function generateImage() {
            const form = new FormData();
            form.append('prompt', document.getElementById('imgPrompt').value);
            form.append('width', document.getElementById('imgWidth').value);
            form.append('height', document.getElementById('imgHeight').value);
            form.append('style', document.getElementById('imgStyle').value);
            const res = await fetch('/api/image/generate', {method: 'POST', body: form});
            const data = await res.json();
            showResult('imageResult', data);
        }

        async function generateVoice() {
            const form = new FormData();
            form.append('text', document.getElementById('voiceText').value);
            form.append('style', document.getElementById('voiceStyle').value);
            form.append('soul', document.getElementById('voiceSoul').checked);
            const res = await fetch('/api/voice/generate', {method: 'POST', body: form});
            const data = await res.json();
            showResult('voiceResult', data);
        }

        async function loadDrafts() {
            const res = await fetch('/api/drafts');
            const data = await res.json();
            const list = document.getElementById('draftsList');
            if (!data.data || !data.data.item) {
                list.textContent = '暂无草稿';
                return;
            }
            list.innerHTML = data.data.item.map(item => {
                const news = item.content.news_item[0];
                return `<div style="padding: 12px; border-bottom: 1px solid #eee;">
                    <strong>${news.title}</strong>
                    <div style="font-size: 12px; color: #666;">
                        作者: ${news.author || 'N/A'} | Media ID: ${item.media_id}
                    </div>
                    <button class="btn" style="margin-top: 8px;" onclick="publishDraft('${item.media_id}')">发布</button>
                    <button class="btn secondary" style="margin-top: 8px;" onclick="deleteDraft('${item.media_id}')">删除</button>
                </div>`;
            }).join('');
        }

        async function publishDraft(mediaId) {
            const res = await fetch('/api/publish/' + mediaId, {method: 'POST'});
            const data = await res.json();
            alert(JSON.stringify(data, null, 2));
            loadDrafts();
        }

        async function deleteDraft(mediaId) {
            const form = new FormData();
            form.append('media_id', mediaId);
            await fetch('/api/drafts/delete', {method: 'POST', body: form});
            loadDrafts();
        }

        async function loadArticles() {
            const res = await fetch('/api/longhun/articles');
            const data = await res.json();
            showResult('statusResult', data);
        }
    </script>
</body>
</html>
"""


def main():
    ensure_templates()
    settings = get_settings()
    uvicorn.run(
        "web_ui:app",
        host=settings.WEB_HOST,
        port=settings.WEB_PORT,
        reload=False,
    )


if __name__ == "__main__":
    main()
