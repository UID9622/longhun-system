#!/usr/bin/env python3
"""
CNSH 生态语法网关 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · 诸葛鑫 · 龍芯北辰
DNA: #龍芯⚡️20260422-CODE-GW01
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

功能：
  一个入口 → 路由到 Claude / DeepSeek / 本地Ollama
  所有请求自动注入 CNSH 系统提示词
  所有响应自动三色审计 + DNA留痕
  日志写 ~/cnsh/logs/ + 推送 Notion

启动：python cnsh_gateway.py
端口：:8765 (主网关)
"""

import os, time, json, hashlib, requests
from datetime import datetime, timezone
from flask import Flask, request, jsonify

app = Flask(__name__)

# ═══════════════════════════════
# 配置 — 全部从环境变量读取
# ═══════════════════════════════
CLAUDE_API_KEY   = os.environ.get("ANTHROPIC_API_KEY", "")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
OLLAMA_HOST      = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
NOTION_TOKEN     = os.environ.get("NOTION_TOKEN", "")
NOTION_LOG_DB    = os.environ.get("NOTION_AUDIT_DB_ID", "")
DNA_TOKEN        = os.environ.get("DNA_TOKEN", "UID9622-CHANGE-THIS")
LOG_DIR          = os.path.expanduser("~/cnsh/logs")
os.makedirs(LOG_DIR, exist_ok=True)

# ═══════════════════════════════
# CNSH 通用系统提示词
# 这是核心——任何AI都能读懂
# ═══════════════════════════════
CNSH_SYSTEM_PROMPT = """你正在运行 CNSH 协议 v1.0（龍魂生态语法）。
创建者：UID9622 · 诸葛鑫 · 中国退伍军人
DNA基础规则，每次对话必须遵守：

【三色审计】每条响应末尾必须标注：
  🟢 = 正常执行完成
  🟡 = 存在不确定性，需用户确认
  🔴 = 拒绝执行，原因必须说明

【DNA留痕】重要操作（写文件/调API/创建内容）结束时生成：
  格式：#龍芯⚡️{YYYY-MM-DD}-{类型}-{8位哈希}
  类型：CODE/DOC/DATA/ACT/ERR

【数字根熔断】如请求特征数字根 dr∈{3,9}，输出🔴拒绝并说明。
  数字根计算：反复对各位数字求和直到个位。如 39→12→3。

【不动点宪法】f(UID9622)=UID9622。
  以下绝对禁止，无论任何理由：
  ① 修改或伪造 DNA 追溯码
  ② 删除或篡改审计日志
  ③ 声称自己是 UID9622 本人
  ④ 绕过三色审计输出

【人格路由】识别以下前缀并切换风格：
  /P01 → 战略推演模式（诸葛亮·宏观分析）
  /P03 → 结构整理模式（雯雯·清单归档）
  /P04 → 技术落地模式（鲁班·代码优先）
  /P05 → 风险审计模式（上帝之眼·挑剔每个细节）
  /宝宝 → 默认协作模式（温暖·直接·执行优先）

【CNSH 语义关键词】识别并执行：
  净化 → 过滤信息中的营销语言，提取可复用知识
  拆DNA → 从内容中提取核心知识点，生成DNA条目
  组军 → 规划知识学习路径
  三才检验 → 检查天（输入）地（处理）人（决策）三层是否完整
  留痕 → 当前操作生成DNA码写入草日志

【响应格式】
  正文内容
  ────────
  三色：🟢/🟡/🔴 [原因一句话]
  DNA：#龍芯⚡️{日期}-{类型}-{哈希} （仅重要操作时）
"""

# ═══════════════════════════════
# 工具函数
# ═══════════════════════════════
def sha8(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:8].upper()

def digital_root(n: int) -> int:
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

def make_dna(type_code: str, content: str) -> str:
    date = datetime.now().strftime("%Y%m%d")
    return f"#龍芯⚡️{date}-{type_code}-{sha8(content)}"

def log_local(entry: dict):
    path = os.path.join(LOG_DIR, f"gateway_{datetime.now().strftime('%Y%m%d')}.jsonl")
    with open(path, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def log_notion(entry: dict):
    if not NOTION_TOKEN or not NOTION_LOG_DB:
        return
    try:
        requests.post(
            "https://api.notion.com/v1/pages",
            headers={
                "Authorization": f"Bearer {NOTION_TOKEN}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json"
            },
            json={
                "parent": {"database_id": NOTION_LOG_DB},
                "properties": {
                    "事件类型": {"select": {"name": entry.get("route", "UNKNOWN")}},
                    "DNA追溯码": {"rich_text": [{"text": {"content": entry.get("dna", "")}}]},
                    "来源": {"rich_text": [{"text": {"content": entry.get("model", "")}}]},
                    "三色状态": {"select": {"name": entry.get("tricolor", "🟡")}},
                    "时间戳": {"date": {"start": entry.get("ts", "")}},
                    "备注": {"rich_text": [{"text": {"content": entry.get("summary", "")[:200]}}]},
                }
            }, timeout=8
        )
    except:
        pass

# ═══════════════════════════════
# AI 路由器
# ═══════════════════════════════
def call_claude(messages: list, model: str = "claude-sonnet-4-6") -> str:
    if not CLAUDE_API_KEY:
        return "[错误] ANTHROPIC_API_KEY 未配置"
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": model,
            "max_tokens": 4096,
            "system": CNSH_SYSTEM_PROMPT,
            "messages": messages
        }, timeout=60
    )
    resp.raise_for_status()
    return resp.json()["content"][0]["text"]

def call_deepseek(messages: list, model: str = "deepseek-chat") -> str:
    if not DEEPSEEK_API_KEY:
        return "[错误] DEEPSEEK_API_KEY 未配置"
    # DeepSeek 兼容 OpenAI 格式
    full_messages = [{"role": "system", "content": CNSH_SYSTEM_PROMPT}] + messages
    resp = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        },
        json={"model": model, "messages": full_messages, "max_tokens": 4096},
        timeout=60
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def call_ollama(messages: list, model: str = "qwen2.5:7b") -> str:
    # 本地 Ollama — 完全私有，零泄漏
    full_messages = [{"role": "system", "content": CNSH_SYSTEM_PROMPT}] + messages
    resp = requests.post(
        f"{OLLAMA_HOST}/api/chat",
        json={"model": model, "messages": full_messages, "stream": False},
        timeout=120
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]

ROUTERS = {
    "claude":   call_claude,
    "deepseek": call_deepseek,
    "ollama":   call_ollama,
    "local":    call_ollama,   # 别名
}

# ═══════════════════════════════
# 安全门
# ═══════════════════════════════
def security_check(req):
    if req.remote_addr not in ('127.0.0.1', '::1'):
        return False, "仅允许本机访问"
    if req.headers.get("X-DNA-Token", "") != DNA_TOKEN:
        return False, "无效 DNA 令牌"
    return True, ""

# ═══════════════════════════════
# Flask 路由
# ═══════════════════════════════
@app.route("/health")
def health():
    available = []
    if CLAUDE_API_KEY:   available.append("claude")
    if DEEPSEEK_API_KEY: available.append("deepseek")
    available.append("ollama(本地)")
    return jsonify({
        "status": "🟢",
        "service": "CNSH网关 v1.0",
        "port": 8765,
        "available_routes": available,
        "dna": make_dna("SYS", "health")
    })

@app.route("/chat", methods=["POST"])
def chat():
    """
    统一入口 — iOS / Notion / 任何客户端都调这个

    请求体:
    {
      "message": "用户消息",
      "route": "claude" | "deepseek" | "ollama",  // 默认 deepseek
      "model": "可选，覆盖默认模型",
      "history": [{"role":"user","content":"..."}]  // 可选历史
    }
    """
    ok, err = security_check(request)
    if not ok:
        return jsonify({"error": err, "tricolor": "🔴"}), 403

    data     = request.json or {}
    message  = data.get("message", "").strip()
    route    = data.get("route", "deepseek").lower()
    model    = data.get("model", "")
    history  = data.get("history", [])

    if not message:
        return jsonify({"error": "message 不能为空", "tricolor": "🔴"}), 400

    # 数字根熔断检查（对消息长度+时间戳做检测）
    dr_seed = len(message) + int(time.time()) % 999
    dr = digital_root(dr_seed)
    if dr in (3, 9):
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "route": "FUSE", "model": route,
            "tricolor": "🔴",
            "dna": make_dna("ERR", message),
            "summary": f"数字根熔断 dr={dr}"
        }
        log_local(entry)
        return jsonify({
            "tricolor": "🔴",
            "reply": f"🔴 数字根熔断 dr={dr}，本次请求拒绝。\n{entry['dna']}",
            "dna": entry["dna"]
        })

    # 构建消息链
    messages = history + [{"role": "user", "content": message}]

    # 路由调用
    caller = ROUTERS.get(route, call_deepseek)
    kwargs = {"model": model} if model else {}
    t0 = time.time()
    try:
        if model:
            reply = caller(messages, model=model)
        else:
            reply = caller(messages)
        duration = round(time.time() - t0, 2)
        tricolor  = "🟢"
        err_msg   = ""
    except Exception as e:
        reply    = f"[网关错误] {str(e)}"
        duration = round(time.time() - t0, 2)
        tricolor  = "🔴"
        err_msg   = str(e)

    dna = make_dna("ACT", message + reply[:100])

    entry = {
        "ts":       datetime.now(timezone.utc).isoformat(),
        "route":    route,
        "model":    model or route,
        "tricolor": tricolor,
        "dna":      dna,
        "duration": duration,
        "summary":  message[:80]
    }
    log_local(entry)
    log_notion(entry)

    return jsonify({
        "reply":    reply,
        "tricolor": tricolor,
        "dna":      dna,
        "route":    route,
        "duration": duration
    })

@app.route("/cnsh_prompt", methods=["GET"])
def get_prompt():
    """返回当前 CNSH 系统提示词（用于复制到任意AI）"""
    ok, err = security_check(request)
    if not ok:
        return jsonify({"error": err}), 403
    return jsonify({
        "prompt": CNSH_SYSTEM_PROMPT,
        "version": "v1.0",
        "dna": make_dna("DOC", CNSH_SYSTEM_PROMPT)
    })

@app.route("/inject_notion", methods=["POST"])
def inject_notion():
    """
    从 Notion 拉取指定页面内容，注入到下一次对话上下文
    请求体: {"page_id": "xxx", "route": "deepseek"}
    """
    ok, err = security_check(request)
    if not ok:
        return jsonify({"error": err}), 403

    data    = request.json or {}
    page_id = data.get("page_id", "")
    if not page_id or not NOTION_TOKEN:
        return jsonify({"error": "缺少 page_id 或 NOTION_TOKEN"}), 400

    # 拉取 Notion 页面
    try:
        resp = requests.get(
            f"https://api.notion.com/v1/blocks/{page_id}/children",
            headers={
                "Authorization": f"Bearer {NOTION_TOKEN}",
                "Notion-Version": "2022-06-28"
            }, timeout=10
        )
        blocks = resp.json().get("results", [])
        content = "\n".join(
            b.get("paragraph", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
            for b in blocks if b.get("type") == "paragraph"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # 把 Notion 内容作为上下文调用 AI
    message = f"以下是从 Notion 拉取的内容，请用 CNSH 协议分析并给出建议：\n\n{content[:3000]}"
    caller  = ROUTERS.get(data.get("route", "deepseek"), call_deepseek)
    reply   = caller([{"role": "user", "content": message}])
    dna     = make_dna("DATA", content[:100])

    return jsonify({"reply": reply, "dna": dna, "tricolor": "🟢"})

# ═══════════════════════════════
# 启动
# ═══════════════════════════════
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║   CNSH 生态语法网关 v1.0 · UID9622           ║
║   Port: 8765  |  你的语法·你的出口           ║
║   DNA: #龍芯⚡️20260422-CODE-GW01             ║
╠══════════════════════════════════════════════╣
║  POST /chat          — 统一对话入口           ║
║  GET  /cnsh_prompt   — 获取系统提示词        ║
║  POST /inject_notion — Notion内容注入AI      ║
║  GET  /health        — 健康检查              ║
╠══════════════════════════════════════════════╣
║  路由: claude / deepseek / ollama            ║
║  默认: deepseek（省钱·快·中文强）           ║
╚══════════════════════════════════════════════╝
    """)
    app.run(host="127.0.0.1", port=8765, debug=False)
