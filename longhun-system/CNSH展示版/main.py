#!/usr/bin/env python3
"""
🛡️ CNSH MVP v2.0 · 一句话造一个东西
DNA: #龍芯⚡️2026-03-31-CNSH-MVP-v2.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: 💎 龍芯北辰｜UID9622
理论指导: 曾仕强老师（永恒显示）
向善四律: L3_不替代人 — 生成只辅助，老大决定用不用
"""

import hashlib
import json
import os
import re
from datetime import datetime
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# ── 常量 ──────────────────────────────────────────────────────
PAGES_DIR = Path(__file__).parent / "pages"
PAGES_DIR.mkdir(exist_ok=True)

# ── 内存db（重启后从文件恢复）────────────────────────────────
db: dict = {}

# ── 可疑词·向善四律L1-L2 ─────────────────────────────────────
BANNED_HARM  = ["攻击", "伤害", "炸弹", "武器", "杀人"]
BANNED_FRAUD = ["诈骗", "钓鱼", "伪装成", "骗局", "欺诈"]

# ═══════════════════════════════════════════════════════════════
# 1. 治理熔断（向善四律 L1-L2）
# ═══════════════════════════════════════════════════════════════
def safety_check(text: str) -> bool:
    for w in BANNED_HARM + BANNED_FRAUD:
        if w in text:
            _log_fuse(text, w)
            return False
    return True

def _log_fuse(text: str, trigger: str):
    with open("shield_burn.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "trigger": trigger,
            "input": text[:100],
            "dna": "#CNSH-9622"
        }, ensure_ascii=False) + "\n")

# ═══════════════════════════════════════════════════════════════
# 2. 人格调度（五人格路由）
# ═══════════════════════════════════════════════════════════════
def route_persona(task: str) -> str:
    if any(w in task for w in ["安全", "验证", "检查", "熔断", "审计"]):
        return "p72_guardian"
    elif any(w in task for w in ["结构", "架构", "搭建", "设计", "系统"]):
        return "architect_builder"
    elif any(w in task for w in ["存储", "同步", "数据", "保存", "备份"]):
        return "syncer_manager"
    elif any(w in task for w in ["搜索", "查找", "分析", "检测", "扫描"]):
        return "scout_hunter"
    else:
        return "wenwen_organizer"

# ═══════════════════════════════════════════════════════════════
# 3. 输入解析（自然语言 → DSL）
# ═══════════════════════════════════════════════════════════════
def parse_input(user_text: str) -> dict:
    components = []
    kw_map = {
        "avatar":     ["头像", "avatar", "照片", "图片"],
        "bio":        ["简介", "bio", "介绍", "描述", "关于"],
        "contact":    ["联系", "contact", "邮件", "电话", "微信"],
        "login_form": ["登录", "login", "注册", "账号", "密码"],
        "portfolio":  ["作品", "项目", "portfolio", "案例"],
        "stats":      ["统计", "数据", "图表", "chart", "stats"],
        "timeline":   ["时间线", "经历", "timeline", "历程"],
        "hero":       ["banner", "首屏", "标语", "hero", "大标题"],
        "nav":        ["导航", "菜单", "nav", "navigation"],
        "footer":     ["底部", "版权", "footer"],
    }
    for comp, keywords in kw_map.items():
        if any(k in user_text.lower() for k in keywords):
            components.append(comp)

    # 风格检测
    style = "简约"
    if any(w in user_text for w in ["科技", "技术", "程序", "代码"]):
        style = "科技"
    elif any(w in user_text for w in ["商务", "专业", "企业", "公司"]):
        style = "商务"
    elif any(w in user_text for w in ["极简", "简洁", "清爽"]):
        style = "极简"

    return {
        "type": "app",
        "intent": user_text[:60],
        "components": components or ["hero"],
        "style": style,
        "dna": "#CNSH-9622"
    }

# ═══════════════════════════════════════════════════════════════
# 4. UI生成（DSL → HTML）
# ═══════════════════════════════════════════════════════════════
STYLE_THEMES = {
    "简约": {"bg": "#ffffff", "fg": "#1a1a1a", "accent": "#4a90e2", "font": "system-ui"},
    "科技": {"bg": "#0d0d1a", "fg": "#e0e0ff", "accent": "#6c3483",  "font": "monospace"},
    "商务": {"bg": "#f8f9fa", "fg": "#2c3e50", "accent": "#c0392b",  "font": "Georgia"},
    "极简": {"bg": "#fafafa", "fg": "#333333", "accent": "#999999",  "font": "sans-serif"},
}

COMP_HTML = {
    "avatar": '<div class="cnsh-avatar"><img src="https://api.dicebear.com/7.x/initials/svg?seed=UID9622" alt="头像" style="width:100px;height:100px;border-radius:50%;border:3px solid var(--accent)"/></div>',
    "bio":    '<div class="cnsh-bio"><p style="color:var(--fg-light);line-height:1.8">{intent}</p></div>',
    "contact":'<div class="cnsh-contact"><a href="mailto:uid9622@example.com" style="color:var(--accent);text-decoration:none">📧 联系我</a></div>',
    "login_form": '<form class="cnsh-form" onsubmit="return false"><input type="text" placeholder="用户名" style="display:block;width:100%;padding:.75rem;margin:.5rem 0;border:1px solid var(--accent);border-radius:8px;background:var(--bg);color:var(--fg)"/><input type="password" placeholder="密码" style="display:block;width:100%;padding:.75rem;margin:.5rem 0;border:1px solid var(--accent);border-radius:8px;background:var(--bg);color:var(--fg)"/><button type="submit" style="width:100%;padding:.75rem;border-radius:8px;border:none;background:var(--accent);color:#fff;cursor:pointer;font-weight:600">登录</button></form>',
    "portfolio": '<div class="cnsh-portfolio" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1rem"><div style="background:var(--accent);opacity:.7;border-radius:12px;height:120px;display:flex;align-items:center;justify-content:center;color:#fff">项目 1</div><div style="background:var(--accent);opacity:.5;border-radius:12px;height:120px;display:flex;align-items:center;justify-content:center;color:#fff">项目 2</div><div style="background:var(--accent);opacity:.3;border-radius:12px;height:120px;display:flex;align-items:center;justify-content:center;color:#fff">项目 3</div></div>',
    "stats":  '<div class="cnsh-stats" style="display:flex;gap:2rem;flex-wrap:wrap"><div style="text-align:center"><div style="font-size:2rem;font-weight:bold;color:var(--accent)">100+</div><div style="color:var(--fg-light);font-size:.875rem">项目</div></div><div style="text-align:center"><div style="font-size:2rem;font-weight:bold;color:var(--accent)">5年</div><div style="color:var(--fg-light);font-size:.875rem">经验</div></div></div>',
    "hero":   '<div class="cnsh-hero" style="text-align:center;padding:3rem 0"><h1 style="font-size:3rem;font-weight:800;color:var(--accent);margin:0">{intent}</h1><p style="color:var(--fg-light);margin:.5rem 0">由 CNSH 生成 · DNA: #CNSH-9622</p></div>',
    "nav":    '<nav class="cnsh-nav" style="display:flex;gap:2rem;padding:1rem 0;border-bottom:1px solid rgba(128,128,128,.2)"><a href="#" style="color:var(--accent);text-decoration:none;font-weight:600">首页</a><a href="#" style="color:var(--fg-light);text-decoration:none">关于</a><a href="#" style="color:var(--fg-light);text-decoration:none">作品</a><a href="#" style="color:var(--fg-light);text-decoration:none">联系</a></nav>',
    "timeline": '<div class="cnsh-timeline"><div style="border-left:2px solid var(--accent);padding-left:1.5rem;margin:.5rem 0"><div style="font-weight:600">2026</div><div style="color:var(--fg-light);font-size:.875rem">CNSH MVP v2.0 发布</div></div><div style="border-left:2px solid var(--accent);padding-left:1.5rem;margin:.5rem 0"><div style="font-weight:600">2025</div><div style="color:var(--fg-light);font-size:.875rem">龍魂系统启动</div></div></div>',
    "footer":  '<footer class="cnsh-footer" style="text-align:center;padding:2rem 0;border-top:1px solid rgba(128,128,128,.2);color:var(--fg-light);font-size:.875rem">© 2026 UID9622 · DNA: #CNSH-9622 · CNSH MVP v2.0</footer>',
}

def generate_ui(schema: dict) -> str:
    style  = schema.get("style", "简约")
    theme  = STYLE_THEMES.get(style, STYLE_THEMES["简约"])
    intent = schema.get("intent", "My Page")
    comps  = schema.get("components", ["hero"])

    comps_html = ""
    for comp in comps:
        tmpl = COMP_HTML.get(comp, "")
        comps_html += tmpl.replace("{intent}", intent) + "\n"

    return f"""<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{intent}</title>
  <meta name="dna" content="{schema.get('dna','#CNSH-9622')}">
  <style>
    :root {{
      --bg: {theme['bg']};
      --fg: {theme['fg']};
      --fg-light: {theme['fg']}99;
      --accent: {theme['accent']};
    }}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: {theme['font']}, -apple-system, sans-serif;
      background: var(--bg);
      color: var(--fg);
      min-height: 100vh;
    }}
    .cnsh-container {{
      max-width: 900px;
      margin: 0 auto;
      padding: 2rem 1.5rem;
    }}
    .cnsh-avatar, .cnsh-bio, .cnsh-contact, .cnsh-form,
    .cnsh-portfolio, .cnsh-stats, .cnsh-hero, .cnsh-nav,
    .cnsh-timeline, .cnsh-footer {{
      margin: 1.5rem 0;
    }}
  </style>
</head>
<body>
  <div class="cnsh-container">
    {comps_html}
  </div>
  <!-- DNA: {schema.get('dna','#CNSH-9622')} | 风格: {style} | CNSH MVP v2.0 -->
</body>
</html>"""

# ═══════════════════════════════════════════════════════════════
# 5. 存储系统（Merkle DNA·SHA-256内容寻址）
# ═══════════════════════════════════════════════════════════════
def store(content: str) -> str:
    hash_id = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
    record  = {
        "content":   content,
        "timestamp": datetime.now().isoformat(),
        "dna":       "#CNSH-9622",
        "version":   1,
        "parent":    None,
        "children":  []
    }
    db[hash_id] = record
    with open(PAGES_DIR / f"{hash_id}.json", "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    return hash_id

def load(hash_id: str) -> dict:
    if hash_id in db:
        return db[hash_id]
    path = PAGES_DIR / f"{hash_id}.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    raise KeyError(f"页面不存在: {hash_id}")

# ═══════════════════════════════════════════════════════════════
# 6. 主执行流（完整 pipeline）
# ═══════════════════════════════════════════════════════════════
def run_pipeline(user_input: str) -> dict:
    if not safety_check(user_input):
        return {"status": "blocked", "reason": "触发向善四律熔断·L1/L2"}
    parsed   = parse_input(user_input)
    persona  = route_persona(user_input)
    ui       = generate_ui(parsed)
    hash_id  = store(ui)
    return {
        "status":       "success",
        "id":           hash_id,
        "url":          f"/page/{hash_id}",
        "persona_used": persona,
        "components":   parsed["components"],
        "style":        parsed["style"],
        "dna":          "#CNSH-9622"
    }

# ═══════════════════════════════════════════════════════════════
# 7. FastAPI 应用
# ═══════════════════════════════════════════════════════════════
# ── UTF-8 JSON 响应（解决 ensure_ascii 转义问题）─────────────
class UTF8JSONResponse(JSONResponse):
    """强制返回人类可读中文，不转义为 unicode 转义序列"""
    def render(self, content) -> bytes:
        return json.dumps(
            content, ensure_ascii=False, allow_nan=False,
            indent=None, separators=(",", ":")
        ).encode("utf-8")

app = FastAPI(default_response_class=UTF8JSONResponse,
    title="CNSH MVP v2.0",
    description="一句话 → 造一个东西 · DNA:#龍芯⚡️2026-03-31-CNSH-MVP-v2.0",
    version="2.0.0"
)

class GenerateRequest(BaseModel):
    input: str

@app.post("/generate")
def generate(req: GenerateRequest):
    return run_pipeline(req.input)

@app.get("/page/{page_id}", response_class=HTMLResponse)
def get_page(page_id: str):
    try:
        data = load(page_id)
        return HTMLResponse(content=data["content"])
    except KeyError:
        return HTMLResponse(content="<h1>页面不存在</h1>", status_code=404)

@app.get("/health")
def health():
    return {
        "status":  "ok",
        "dna":     "#CNSH-9622",
        "version": "2.0.0",
        "pages":   len(list(PAGES_DIR.glob("*.json")))
    }

@app.get("/", response_class=HTMLResponse)
def index():
    with open(Path(__file__).parent / "index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# ═══════════════════════════════════════════════════════════════
# 8. Notion 自动同步模块（MVP规范全量实现）
# DNA: #龍芯⚡️2026-04-01-NOTION-SYNC-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导: 曾仕强老师（永恒显示）
# ═══════════════════════════════════════════════════════════════

# ── Notion固定ID（来自交接手册·不可改）──────────────────────
NOTION_DRAFT_LOG_ID   = "b35faf46-2bc0-42aa-9de5-192520180728"  # 操作留痕/草日志 ✅已授权
NOTION_PRIVATE_LIB_ID = "eaed6ce50a2841b8babf7a2a513f4805"       # 私密明细库（加密盾）⚠️需授权
NOTION_PUBLIC_PAGE_ID  = "868fec34e5a24e7e829dc5851a75f6b7"       # 公开展示页（脱敏骨架）✅已授权
NOTION_MAIN_ENTRY_ID   = "8089c682444843f0bf5de1dce79d0497"       # 主控入口 ⚠️需授权
# 授权可访问的备用写入目标（当私密库无权限时用草日志暂存）
NOTION_VERIFY_REPORT_ID = "4b010758-f636-43c8-9253-64a7e8dab0ab" # 验证报告 ✅已授权

NOTION_API = "https://api.notion.com/v1"
NOTION_VER = "2022-06-28"

# ── 加密触发词/正则（MVP规范第4节·命中任一条即加密）────────
# 加密规则表（MVP规范第4节·分类命名·Section 9 报告用）
# 格式：{规则名: [触发关键词列表]}
_RULE_KW: dict = {
    "个人隐私/可识别信息": ["私钥", "身份证", "住址", "手机号", "聊天记录",
                           "截图", "未脱敏", "原文证据", "账号密码", "聊天隐私"],
    "凭证密钥/登录凭证":   ["密码", "password", "2fa", "token", "secret", "bearer",
                           "ntn_", "sk-", "api_key", "apikey"],
}
# 格式：{正则: 规则名}（精确匹配·覆盖关键词无法捕获的格式）
_RULE_RE: dict = {
    r"\b1[3-9]\d{9}\b":               "个人隐私/手机号",
    r"ntn_[A-Za-z0-9]{10,}":             "凭证密钥/Notion Token",
    r"sk-[A-Za-z0-9]{10,}":              "凭证密钥/API Key",
    r"secret_[A-Za-z0-9]{10,}":          "凭证密钥/Secret字段",
    r"Bearer\s+[A-Za-z0-9\-._~+/]{20,}": "凭证密钥/Bearer Token",
}


def classify_content(text: str) -> dict:
    """公开/加密二分判定（MVP规范第4节）· 返回 rule 字段供 Section 9 验收"""
    t = text.lower()
    for rule, kws in _RULE_KW.items():
        for kw in kws:
            if kw in t:
                return {"result": "🔒加密", "reason": f"命中关键词: {kw}",
                        "target": "private", "rule": rule}
    for pat, rule in _RULE_RE.items():
        if re.search(pat, text):
            return {"result": "🔒加密", "reason": f"命中正则模式: {rule}",
                    "target": "private", "rule": rule}
    return {"result": "🌐公开", "reason": "不含敏感信息，符合公开条件",
            "target": "public", "rule": "无"}


def _desensitize(text: str) -> str:
    """脱敏处理：所有敏感字段替换为[已脱敏]·公开页写入专用（Section 9 强制隔离）"""
    result = text
    for pat in _RULE_RE:
        result = re.sub(pat, "[已脱敏]", result, flags=re.IGNORECASE)
    for kws in _RULE_KW.values():
        for kw in kws:
            result = re.sub(re.escape(kw), "[已脱敏]", result, flags=re.IGNORECASE)
    return result



def _load_notion_token() -> str:
    """加载 NOTION_TOKEN：longhun-system/.env 先打底，.cnsh/.env 可覆盖"""
    for p in [Path.home() / "longhun-system" / ".env",
              Path.home() / ".cnsh" / ".env"]:
        if p.exists():
            load_dotenv(p, override=True)
    token = os.environ.get("NOTION_TOKEN", "")
    return token or ""


def _dna(topic: str) -> str:
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{topic}-v1.0"


def _notion_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VER,
        "Content-Type": "application/json",
    }


def _notion_get(token: str, path: str) -> dict:
    with httpx.Client(timeout=15) as c:
        r = c.get(f"{NOTION_API}{path}", headers=_notion_headers(token))
        return r.json() if r.status_code == 200 else {}


def _notion_patch(token: str, path: str, payload: dict) -> int:
    with httpx.Client(timeout=10) as c:
        r = c.patch(f"{NOTION_API}{path}", headers=_notion_headers(token), json=payload)
        return r.status_code


def write_draft_log(token: str, summary: str, dna: str):
    """草日志写入 Notion 操作留痕页（不管失败，不阻塞主流程）"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {summary} | DNA:{dna} | #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    _notion_patch(token, f"/blocks/{NOTION_DRAFT_LOG_ID}/children", {
        "children": [{"object": "block", "type": "paragraph",
                      "paragraph": {"rich_text": [{"type": "text", "text": {"content": line}}]}}]
    })


def _extract_text(blocks: list) -> str:
    parts = []
    for b in blocks[:8]:
        btype = b.get("type", "")
        for rt in b.get(btype, {}).get("rich_text", []):
            parts.append(rt.get("plain_text", ""))
    return " ".join(parts)[:300]


def _notion_blocks(text_lines: list) -> dict:
    """把文本行列表转为 Notion paragraph block payload"""
    return {"children": [
        {"object": "block", "type": "paragraph",
          "paragraph": {"rich_text": [{"type": "text", "text": {"content": ln}}]}}
        for ln in text_lines
    ]}


def _write_to_private_lib(token: str, fp: dict):
    """私密明细库写入：完整内容 + DNA + 确认码（Section 9 强制·不脱敏）"""
    confirm = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    lines = [
        f"🔒 [私密明细] {fp['title']}",
        f"规则: {fp.get('rule','—')} | 原因: {fp['reason']}",
        f"原始摘要: {fp['snippet'][:300]}",
        f"DNA: {fp['dna']} | 确认码: {confirm}",
        f"时间: {fp['ts']}",
    ]
    _notion_patch(token, f"/blocks/{NOTION_PRIVATE_LIB_ID}/children", _notion_blocks(lines))


def _write_public_summary(token: str, fp: dict):
    """公开展示页写入：脱敏摘要（Section 9 强制·绝不出现敏感字段）"""
    desensitized = _desensitize(fp['snippet'])
    lines = [
        f"📄 [公开摘要] {fp['title']}",
        f"归类: {fp['classification']} | 原因: {fp['reason']}",
        f"脱敏摘要: {desensitized[:200]}",
        f"DNA: {fp['dna']}",
    ]
    _notion_patch(token, f"/blocks/{NOTION_PUBLIC_PAGE_ID}/children", _notion_blocks(lines))


# ── 请求模型 ─────────────────────────────────────────────────
class SyncRequest(BaseModel):
    page_id: str = NOTION_MAIN_ENTRY_ID
    depth: int = 1   # 1=只拉子页标题元数据; 2=再拉子页全文


class ClassifyRequest(BaseModel):
    content: str


# ── /sync/notion ─────────────────────────────────────────────
@app.post("/sync/notion")
def sync_notion(req: SyncRequest):
    """
    MVP自动更新规范全流程：
    拉取Notion内容 → 判定公开/加密 → 写指纹卡到对应库 → 草日志留痕
    验收标准1+2+3全覆盖
    """
    token = _load_notion_token()
    if not token:
        return {"status": "error",
                "msg": "NOTION_TOKEN未配置，检查 ~/longhun-system/.env"}

    dna = _dna("NOTION-SYNC")
    results, errors = [], []

    try:
        # Step1: 拉目标页内容
        data = _notion_get(token, f"/blocks/{req.page_id}/children?page_size=50")
        all_blocks = data.get("results", [])
        child_pages = [b for b in all_blocks if b.get("type") == "child_page"]

        # 如果有子页，遍历子页；如果没有，就把当前页作为单页处理
        if child_pages:
            pages_to_process = [(cp.get("id", ""),
                                  cp.get("child_page", {}).get("title", "无标题"),
                                  None)  # blocks延迟拉
                                 for cp in child_pages[:20]]
        else:
            # 当前页直接处理
            meta = _notion_get(token, f"/pages/{req.page_id}")
            title_prop = (meta.get("properties", {})
                          .get("title", {})
                          .get("title", [{}]))
            title = (title_prop[0].get("plain_text", "此页面") if title_prop else "此页面")
            pages_to_process = [(req.page_id, title, all_blocks)]

        for pid, title, preloaded_blocks in pages_to_process:
            # Step2: depth>=2 拉全文（子页模式）
            if preloaded_blocks is not None:
                blocks = preloaded_blocks
            elif req.depth >= 2:
                bd = _notion_get(token, f"/blocks/{pid}/children?page_size=30")
                blocks = bd.get("results", [])
            else:
                blocks = []

            # Step3: 判定
            snippet   = _extract_text(blocks) if blocks else title
            clf       = classify_content(title + " " + snippet)

            # Step4: 知识指纹卡
            fp = {
                "page_id":        pid,
                "title":          title,
                "snippet":        snippet or "（无文字内容）",
                "classification": clf["result"],
                "reason":         clf["reason"],
                "target":         clf["target"],
                "dna":            dna,
                "ts":             datetime.now().isoformat(),
            }
            results.append(fp)

            # Step5: 写到对应库（Section 9 强制隔离：私密全量·公开脱敏·不可越层）
            fp["rule"]       = clf.get("rule", "无")
            fp["written_to"] = []
            fp["write_errors"] = []

            if clf["target"] == "private":
                # 5a 私密明细库：完整内容（含原文摘要、DNA、确认码）
                try:
                    _write_to_private_lib(token, fp)
                    fp["written_to"].append("私密明细库")
                except Exception as e:
                    fp["write_errors"].append(f"私密库:{str(e)[:40]}")
                    # 降级：写草日志暂存（不写公开页·防止泄露）
                    try:
                        write_draft_log(token,
                            f"[私密暂存] {title[:20]} | 规则:{fp['rule']} | {fp['reason']}", dna)
                        fp["written_to"].append("草日志暂存")
                    except Exception:
                        pass

                # 5b 公开展示页：脱敏摘要（不含任何原始敏感字段·Section 9 一票否决保护）
                try:
                    _write_public_summary(token, fp)
                    fp["written_to"].append("公开展示页(脱敏摘要)")
                except Exception as e:
                    fp["write_errors"].append(f"公开摘要:{str(e)[:40]}")

            else:
                # 公开内容：直接写公开展示页
                try:
                    _write_public_summary(token, fp)
                    fp["written_to"].append("公开展示页")
                except Exception as e:
                    fp["write_errors"].append(f"公开页:{str(e)[:40]}")

            if fp["write_errors"]:
                errors.append(f"{title[:15]}: {'; '.join(fp['write_errors'])}")

        # Step6: 草日志（无论如何都写）
        pub = sum(1 for r in results if r["target"] == "public")
        pri = sum(1 for r in results if r["target"] == "private")
        summary = (f"同步{len(results)}页 | 🌐公开:{pub} 🔒加密:{pri}"
                   f" | 报错:{len(errors)}")
        write_draft_log(token, summary, dna)

    except Exception as e:
        summary = f"同步异常: {str(e)[:100]}"
        try:
            write_draft_log(token, summary, dna)
        except Exception:
            pass
        return {"status": "error", "msg": summary, "dna": dna}

    return {
        "status":       "ok",
        "dna":          dna,
        "confirm":      "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        "synced_pages": len(results),
        "public":       sum(1 for r in results if r["target"] == "public"),
        "private":      sum(1 for r in results if r["target"] == "private"),
        "errors":       errors,
        "draft_log":    "已写入Notion草日志",
        "results":      results,
    }


# ── /classify ────────────────────────────────────────────────
@app.post("/classify")
def classify(req: ClassifyRequest):
    """对任意内容做公开/加密判定 + 草日志留痕"""
    token = _load_notion_token()
    dna   = _dna("CLASSIFY")
    clf   = classify_content(req.content)

    if token:
        try:
            write_draft_log(token, f"判定:{clf['result']} | {clf['reason']}", dna)
        except Exception:
            pass

    return {
        "status":  "ok",
        "dna":     dna,
        "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        **clf,
    }


# ── /draft-logs（本地查看）───────────────────────────────────
@app.get("/draft-logs")
def draft_logs():
    """查看本地 shield_burn.jsonl 最近20条"""
    log_file = Path(__file__).parent / "shield_burn.jsonl"
    logs = []
    if log_file.exists():
        for line in log_file.read_text(encoding="utf-8").splitlines()[-20:]:
            try:
                logs.append(json.loads(line))
            except Exception:
                pass
    return {"status": "ok", "count": len(logs), "logs": logs}




class EncryptValidateRequest(BaseModel):
    content: str = (
        "Notion Token: ntn_303726abc123def456，"
        "手机号：13812345678，密码：P@ssw0rd#2026，"
        "Bearer eyJhbGciOiJSUzI1NiJ9.test.signature"
    )


@app.post("/validate/encryption")
def validate_encryption(req: EncryptValidateRequest):
    """
    Section 9 加密路径验收：越层即熔断·三条一票否决
    全部通过才算MVP加密路径合格
    """
    token  = _load_notion_token()
    dna    = _dna("ENCRYPT-VALIDATE")
    confirm = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

    report = {
        "dna":             dna,
        "confirm":         confirm,
        "test_input":      req.content[:50] + "...",
        "steps":           [],
        "verdict":         "PENDING",
        "one_ticket_veto": [],
    }

    # ── Step 1: 判定必须是 🔒加密 ─────────────────────────────
    clf = classify_content(req.content)
    s1  = {
        "step":   "1_classify",
        "result": clf["result"],
        "reason": clf["reason"],
        "rule":   clf.get("rule", "—"),
        "pass":   clf["target"] == "private",
    }
    report["steps"].append(s1)
    if clf["target"] != "private":
        report["one_ticket_veto"].append(f"判定失败：内容未命中任何加密规则 → {clf['reason']}")
        report["verdict"] = "❌FAIL"
        return report

    fp = {
        "title":          "加密路径验收用例",
        "snippet":        req.content[:300],
        "classification": clf["result"],
        "reason":         clf["reason"],
        "rule":           clf.get("rule", "—"),
        "target":         clf["target"],
        "dna":            dna,
        "ts":             datetime.now().isoformat(),
    }

    # ── Step 2: 写私密明细库（完整内容 + DNA + 确认码）─────────
    if token:
        try:
            _write_to_private_lib(token, fp)
            s2 = {"step": "2_write_private_lib", "pass": True,
                   "msg": f"已写入私密明细库 {NOTION_PRIVATE_LIB_ID[:8]}..."}
        except Exception as e:
            s2 = {"step": "2_write_private_lib", "pass": False,
                   "msg": f"写入失败: {str(e)[:60]}"}
    else:
        s2 = {"step": "2_write_private_lib", "pass": False, "msg": "NOTION_TOKEN未配置"}
    report["steps"].append(s2)

    # ── Step 3: 脱敏 + 验证公开页不含敏感字段（一票否决保护）──
    desensitized = _desensitize(req.content)
    recheck      = classify_content(desensitized)
    public_safe  = recheck["target"] == "public"

    if not public_safe:
        report["one_ticket_veto"].append(
            f"脱敏失败：公开页仍含敏感内容 → {recheck['reason']}（规则:{recheck.get('rule','—')}）"
        )
        s3 = {"step": "3_desensitize_check", "pass": False,
               "msg": f"脱敏后仍命中加密规则，拒绝写入公开页",
               "recheck": recheck["reason"]}
    else:
        if token:
            try:
                _write_public_summary(token, fp)
                s3 = {"step": "3_desensitize_check", "pass": True,
                       "msg": "脱敏验证通过，已写入公开展示页（脱敏摘要）",
                       "desensitized_preview": desensitized[:80]}
            except Exception as e:
                s3 = {"step": "3_desensitize_check", "pass": False,
                       "msg": f"写入公开摘要失败: {str(e)[:60]}"}
        else:
            s3 = {"step": "3_desensitize_check", "pass": True,
                   "msg": "脱敏验证通过（NOTION_TOKEN未配置，跳过写入）",
                   "desensitized_preview": desensitized[:80]}
    report["steps"].append(s3)

    # ── Step 4: 草日志留痕（时间戳+命中规则+去向+DNA）──────────
    log_msg = (
        f"加密路径验收 | 判定:{clf['result']} | 规则:{clf.get('rule','—')} "
        f"| 去向:私密明细库+公开脱敏摘要 | {confirm}"
    )
    if token:
        try:
            write_draft_log(token, log_msg, dna)
            s4 = {"step": "4_draft_log", "pass": True, "msg": "草日志已写入"}
        except Exception as e:
            s4 = {"step": "4_draft_log", "pass": False, "msg": f"草日志写入失败: {str(e)[:50]}"}
    else:
        s4 = {"step": "4_draft_log", "pass": False, "msg": "NOTION_TOKEN未配置"}
    report["steps"].append(s4)

    # ── 一票否决检查 ─────────────────────────────────────────
    import re as _re
    if not _re.match(r"#龍芯⚡️\d{4}-\d{2}-\d{2}-.+-v\d+\.\d+$", dna):
        report["one_ticket_veto"].append(f"DNA格式不符合规范: {dna}")

    if confirm != "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z":
        report["one_ticket_veto"].append("确认码被污染或缺失")

    # ── 最终裁决 ─────────────────────────────────────────────
    all_pass  = all(s["pass"] for s in report["steps"])
    no_veto   = len(report["one_ticket_veto"]) == 0
    report["verdict"] = "✅PASS · 加密路径验收合格" if (all_pass and no_veto) else "❌FAIL · 存在问题"

    return report

# ── /shield/ingest（护盾统一投递口·替代护盾自写Notion）────────
class ShieldIngestRequest(BaseModel):
    content:  str
    source:   str = "shield"   # 来源标识，如 shield/alert/session/audit
    title:    str = ""         # 可选标题
    ts:       str = ""         # 可选原始时间戳

@app.post("/shield/ingest")
def shield_ingest(req: ShieldIngestRequest):
    """
    护盾/窗口护盾 统一归档入口（不可绕过）
    护盾只负责 POST 内容过来；MVP 统一判定 公开/加密 并写回 Notion 三处：
      🔒 私密明细库（全量） · 🌐 公开展示页（脱敏摘要） · 草日志（路由留痕）
    DNA: #龍芯⚡️YYYY-MM-DD-SHIELD-INGEST-v1.0
    """
    token   = _load_notion_token()
    dna     = _dna("SHIELD-INGEST")
    confirm = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    clf     = classify_content(req.content)
    title   = req.title or f"[{req.source}] {req.content[:30]}…"
    ts_val  = req.ts or datetime.now().isoformat()

    fp = {
        "title":          title,
        "snippet":        req.content[:400],
        "classification": clf["result"],
        "reason":         clf["reason"],
        "rule":           clf.get("rule", "无"),
        "target":         clf["target"],
        "dna":            dna,
        "ts":             ts_val,
    }
    written_to, write_errors = [], []

    if token:
        if clf["target"] == "private":
            # 私密：全量写私密库 + 脱敏写公开页
            try:
                _write_to_private_lib(token, fp)
                written_to.append("私密明细库")
            except Exception as e:
                write_errors.append(f"私密库:{str(e)[:40]}")
                try:
                    write_draft_log(token, f"[私密暂存] {title[:20]} | {dna}", dna)
                    written_to.append("草日志暂存")
                except Exception:
                    pass
            try:
                _write_public_summary(token, fp)
                written_to.append("公开展示页(脱敏)")
            except Exception as e:
                write_errors.append(f"公开脱敏:{str(e)[:40]}")
        else:
            # 公开：直接写公开页
            try:
                _write_public_summary(token, fp)
                written_to.append("公开展示页")
            except Exception as e:
                write_errors.append(f"公开页:{str(e)[:40]}")

        # 草日志（无论如何都写）
        try:
            write_draft_log(token,
                f"[护盾投递] {req.source} | {clf['result']} | 规则:{fp['rule']} "
                f"| 去向:{','.join(written_to) or '暂存'} | {confirm}", dna)
            written_to.append("草日志")
        except Exception as e:
            write_errors.append(f"草日志:{str(e)[:40]}")

    return {
        "status":       "ok",
        "dna":          dna,
        "confirm":      confirm,
        "source":       req.source,
        "classification": clf["result"],
        "reason":       clf["reason"],
        "rule":         fp["rule"],
        "written_to":   written_to,
        "write_errors": write_errors,
    }


# ── /backup/archive（旧备份一次性归档·盘点清单批量写回Notion）─
class BackupArchiveRequest(BaseModel):
    inventory_path: str = str(Path(__file__).parent / "backup_inventory.json")
    dest_filter: str    = "🔒私密"  # 只处理这个去向的文件；"ALL"处理全部
    max_files:   int    = 50        # 单次最多处理文件数，防止超时

@app.post("/backup/archive")
def backup_archive(req: BackupArchiveRequest):
    """
    旧备份一次性归档：
    1. 读 backup_inventory.json（由扫描脚本生成）
    2. 对每个文件：读内容摘要 → POST /shield/ingest → Notion三处落地
    3. 返回归档结果清单
    DNA: #龍芯⚡️YYYY-MM-DD-BACKUP-ARCHIVE-v1.0
    """
    dna     = _dna("BACKUP-ARCHIVE")
    confirm = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    inv_path = Path(req.inventory_path)
    if not inv_path.exists():
        return {"status": "error", "msg": f"清单文件不存在: {inv_path}"}

    try:
        inv = json.loads(inv_path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"status": "error", "msg": f"清单解析失败: {e}"}

    files = inv.get("files", [])
    if req.dest_filter != "ALL":
        files = [f for f in files if f.get("dest") == req.dest_filter]

    files = files[:req.max_files]
    results = []
    token = _load_notion_token()

    for fi in files:
        fpath = Path(fi["path"])
        snippet = ""
        try:
            # 只读文本文件前500字；二进制/大文件只用元数据摘要
            raw = fpath.read_bytes()[:2000]
            try:
                snippet = raw.decode("utf-8", errors="replace")[:500]
            except Exception:
                snippet = f"[binary] size={fi['size_kb']}KB"
        except Exception as e:
            snippet = f"[读取失败] {str(e)[:60]}"

        content = (
            f"文件: {fpath.name} | 类型: {fi['type']} | "
            f"大小: {fi['size_kb']}KB | 修改: {fi['mtime']} | "
            f"SHA256前缀: {fi['sha256_prefix']}\n内容摘要: {snippet}"
        )
        clf = classify_content(content)
        fp = {
            "title":          f"[备份归档] {fpath.name}",
            "snippet":        content[:400],
            "classification": clf["result"],
            "reason":         clf["reason"],
            "rule":           clf.get("rule", "无"),
            "target":         clf["target"],
            "dna":            dna,
            "ts":             datetime.now().isoformat(),
        }
        written_to, write_errors = [], []

        if token:
            if clf["target"] == "private":
                try:
                    _write_to_private_lib(token, fp)
                    written_to.append("私密明细库")
                except Exception as e:
                    write_errors.append(f"私密库:{str(e)[:30]}")
                try:
                    _write_public_summary(token, fp)
                    written_to.append("公开展示页(脱敏)")
                except Exception as e:
                    write_errors.append(f"公开脱敏:{str(e)[:30]}")
            else:
                try:
                    _write_public_summary(token, fp)
                    written_to.append("公开展示页")
                except Exception as e:
                    write_errors.append(f"公开页:{str(e)[:30]}")
            try:
                write_draft_log(token,
                    f"[备份归档] {fpath.name} | {clf['result']} | "
                    f"规则:{fp['rule']} | 去向:{','.join(written_to) or '暂存'}", dna)
                written_to.append("草日志")
            except Exception as e:
                write_errors.append(f"草日志:{str(e)[:30]}")

        results.append({
            "file":       fpath.name,
            "type":       fi["type"],
            "dest_orig":  fi["dest"],
            "classified": clf["result"],
            "written_to": written_to,
            "errors":     write_errors,
        })

    priv_count = sum(1 for r in results if "私密明细库" in r["written_to"])
    pub_count  = sum(1 for r in results if "公开展示页" in r.get("written_to", [])
                     or "公开展示页(脱敏)" in r.get("written_to", []))

    return {
        "status":        "ok",
        "dna":           dna,
        "confirm":       confirm,
        "total_scanned": len(inv.get("files", [])),
        "processed":     len(results),
        "private_archived": priv_count,
        "public_archived":  pub_count,
        "results":       results,
    }


if __name__ == "__main__":
    print("🚀 CNSH MVP v2.1 启动中...")
    print("   DNA: #龍芯⚡️2026-04-01-NOTION-SYNC-v1.0")
    print("   访问: http://localhost:8000")
    print("   端点: POST /sync/notion | POST /classify | POST /validate/encryption | GET /draft-logs")
    print("   新增: POST /shield/ingest | POST /backup/archive")
    uvicorn.run(app, host="0.0.0.0", port=8000)
