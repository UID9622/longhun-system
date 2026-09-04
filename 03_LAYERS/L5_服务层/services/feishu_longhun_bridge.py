#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🤖 龍魂 · 飞书桥接智能体 — 全系统功能索引
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
DNA: #龍芯⚡️丙午·乙未·壬午·丙午·䷳艮为山-FEISHU-BRIDGE-AGENT-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

定位: 龍魂系统对外唯一"出口" — 飞书机器人即全系统查询入口
一句话: 在飞书里问什么，龍魂就给什么

支持的自然语言查询:
  📊 协同场 — "看看协同场怎么样" "有没有冲突" "均衡吗" "怎么分工"
  👤 人格 — "人格 P01" "人格 top5" "人格 健康度" "人格 诸葛亮"
  🖥️ 系统 — "系统状态" "检查安全" "审计一下"
  🔢 五行 — "算一下数字根 123" "这属什么属性"
  🗺️ 路由 — "节点在哪 IPA-001" "查路由 P01"
  🧬 DNA — "查DNA #龍芯⚡️" "验证DNA"
  📖 道德经 — "第X章" "上善若水"
  🔍 安全 — "漏洞扫描" "CVE检查"

启动:
  python3 L5_服务层/services/feishu_longhun_bridge.py
  端口: 9637 (与 persona bot 9636 错开)

环境变量:
  FEISHU_APP_ID / FEISHU_APP_SECRET / FEISHU_VERIFY_TOKEN / BRIDGE_BOT_PORT
"""

import json
import os
import re
import sys
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any, Dict

from fastapi import FastAPI, Request, HTTPException  # type: ignore[import-untyped]
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import-untyped]
from fastapi.responses import JSONResponse

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "bin"))
sys.path.insert(0, str(ROOT / "scripts" / "round1"))

DNA = "#龍芯⚡️丙午·乙未·壬午·丙午·䷳艮为山-FEISHU-BRIDGE-AGENT-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
CST = timezone(timedelta(hours=8))

# ─── 飞书配置 ───
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
FEISHU_VERIFY_TOKEN = os.getenv("FEISHU_VERIFY_TOKEN", "")
BRIDGE_BOT_PORT = int(os.getenv("BRIDGE_BOT_PORT", "9637"))

app = FastAPI(
    title="龍魂 · 飞书桥接智能体",
    description="龍魂系统对外唯一查询入口 — 在飞书问什么，龍魂就给什么",
    version="1.0.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ─── 飞书 API 工具 ───
def get_tenant_access_token() -> str:
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        return ""
    import urllib.request
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    body = json.dumps({"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read()).get("tenant_access_token", "")
    except Exception:
        return ""

def reply_feishu_card(receive_id: str, msg_id: str, card: Dict[str, Any]):
    token = get_tenant_access_token()
    if not token:
        return
    import urllib.request
    url = f"https://open.feishu.cn/open-apis/im/v1/messages/{msg_id}/reply"
    body = {
        "content": json.dumps(card, ensure_ascii=False),
        "msg_type": "interactive",
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"[飞书] 回复失败: {e}")

# ─── 命令路由引擎 ───
def parse_intent(text: str) -> Dict[str, Any]:
    """解析用户输入 → 返回意图和参数
    
    优先级: 精确正则 → 语义解析器 → 未知
    """
    text = text.strip()
    
    # ── 第一层: 精确正则匹配（已知领域优先）──
    patterns = [
        # 协同场
        (r'(协同场|流场协同|协同状态|看看协同)', 'collab-status'),
        (r'(均衡|五行均衡|缺什么)', 'collab-balance'),
        (r'(冲突|相克|有没有冲突)', 'collab-conflicts'),
        (r'(融合|融合指数|融合得怎么样)', 'collab-fusion'),
        (r'(协同报告|协同总览)', 'collab-report'),
        (r'(分工|任务分配|怎么分|谁干什么|谁来干)', 'collab-task'),
        # 人格
        (r'^人格', 'persona'),
        # 系统状态（排除协同场的干扰）
        (r'^(状态|系统)$', 'system-status'),
        (r'系统状态', 'system-status'),
        # 审计
        (r'(审计|安全检查|扫一下|漏洞|安全扫描)', 'audit'),
        # 五行
        (r'(算一下|数字根|属什么|五行)', 'wuxing'),
        # 路由
        (r'(在哪|路由|节点|查.*IPA)', 'route-find'),
        # DNA
        (r'(DNA\b|追溯码|查DNA|验证DNA)', 'dna-lookup'),
        # 道德经
        (r'(道德经|第[一二三四五六七八九十\d]+章|上善若水|无为|知足)', 'daodejing'),
        # 帮助
        (r'^(帮助|help|怎么用|能干什么|功能|菜单)$', 'help'),
    ]
    
    for pattern, intent in patterns:
        m = re.search(pattern, text)
        if m:
            return {
                "source": "regex",
                "intent": intent,
                "query": m.group(1).strip() if m.lastindex else "",
                "text": text,
            }
    
    # ── 第二层: 语义解析器（兜底）──
    try:
        from semantic_parser import parse_command  # type: ignore[import-untyped]
        result = parse_command(text)
        if result.get("success") and result.get("cn_command"):
            cn = result["cn_command"]
            # 只接受已知命令域
            known = ["流场协同", "人格", "记录器", "流场总控", "同步"]
            if any(cn.startswith(k) for k in known):
                return {
                    "source": "semantic_parser",
                    "cn_command": cn,
                    "en_command": result.get("en_command", ""),
                    "text": text,
                }
    except Exception:
        pass
    
    # ── 第三层: 完全未知 → 帮助 ──
    return {
        "source": "fallback",
        "intent": "unknown",
        "text": text,
    }

def execute_command(intent: Dict[str, Any]) -> Dict[str, Any]:
    """根据意图执行对应引擎"""
    cmd = intent.get("cn_command", "") or intent.get("intent", "")
    text = intent.get("text", "")
    query = intent.get("query", "")
    
    result = {"title": "龍魂查询", "content": "", "status": "ok"}
    
    # ── 流场协同 ──
    if "流场协同" in cmd or cmd in ("collab-status", "collab-balance", "collab-conflicts", "collab-fusion", "collab-report", "collab-task"):
        sub_cmd_map = {
            "状态": "状态", "status": "状态",
            "均衡": "均衡", "balance": "均衡",
            "冲突": "冲突", "conflicts": "冲突",
            "融合": "融合", "fusion": "融合",
            "报告": "报告", "report": "报告",
            "任务": "任务", "task": "任务",
        }
        
        # 从 cn_command 提取子命令
        if " " in cmd:
            sub = cmd.split()[-1]
        else:
            sub = sub_cmd_map.get(cmd, "状态")
        
        if "均衡" in text or "缺什么" in text:
            sub = "均衡"
        elif "冲突" in text:
            sub = "冲突"
        elif "融合" in text:
            sub = "融合"
        elif "报告" in text or "总览" in text:
            sub = "报告"
        elif "分工" in text or "任务" in text or "谁干什么" in text:
            sub = "任务"
        
        engine = ROOT / "scripts" / "round1" / "flowfield_collab_engine.py"
        if engine.exists():
            try:
                proc = subprocess.run(
                    [sys.executable, str(engine), "--cmd", sub],
                    capture_output=True, text=True, timeout=15, cwd=str(ROOT)
                )
                result["title"] = f"流场协同 · {sub}"
                result["content"] = proc.stdout.strip()[:2000]
                result["status"] = "ok" if proc.returncode == 0 else "error"
                if proc.stderr.strip():
                    result["content"] += f"\n\n---\n⚠️ {proc.stderr.strip()[:500]}"
            except Exception as e:
                result["title"] = "流场协同 · 错误"
                result["content"] = str(e)
                result["status"] = "error"
        else:
            result["content"] = "流场协同引擎未找到"
            result["status"] = "error"
    
    # ── 人格 ──
    elif cmd == "persona":
        report_script = ROOT / "bin" / "lh_persona_report.py"
        if report_script.exists():
            try:
                proc_args = [sys.executable, str(report_script), "--feishu-card"]
                if query:
                    proc_args.append(query)
                proc = subprocess.run(proc_args, capture_output=True, text=True, timeout=10, cwd=str(ROOT))
                if proc.returncode == 0:
                    card_data = json.loads(proc.stdout)
                    return card_data  # 直接返回卡片 JSON
                result["title"] = f"人格查询 · {query or '总览'}"
                result["content"] = proc.stdout.strip()[:2000]
            except Exception as e:
                result["content"] = str(e)
                result["status"] = "error"
    
    # ── 系统状态 ──
    elif cmd in ("system-status",):
        result["title"] = "龍魂 · 系统状态"
        lines = []
        lines.append(f"⏰ {datetime.now(CST).strftime('%Y-%m-%d %H:%M:%S')} CST")
        lines.append(f"🧬 {DNA}")
        
        # Git 状态
        try:
            proc = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, cwd=str(ROOT), timeout=5)
            lines.append(f"📂 分支: {proc.stdout.strip()}")
            proc = subprocess.run(["git", "log", "-1", "--format=%h %s"], capture_output=True, text=True, cwd=str(ROOT), timeout=5)
            lines.append(f"📝 最新: {proc.stdout.strip()[:80]}")
        except Exception:
            pass
        
        # 内存/磁盘
        try:
            proc = subprocess.run(["df", "-h", str(ROOT)], capture_output=True, text=True, timeout=5)
            disk_line = proc.stdout.strip().split("\n")[-1]
            parts = disk_line.split()
            if len(parts) >= 5:
                lines.append(f"💾 磁盘: {parts[4]} 已用 ({parts[2]}/{parts[1]})")
        except Exception:
            pass
        
        result["content"] = "\n".join(lines)
    
    # ── 审计 ──
    elif cmd == "audit":
        result["title"] = "龍魂 · 安全审计"
        # 跑安全巡逻
        scan_script = ROOT / "bin" / "patrol_security.py"
        if scan_script.exists():
            try:
                proc = subprocess.run(
                    [sys.executable, str(scan_script), "--quick"],
                    capture_output=True, text=True, timeout=30, cwd=str(ROOT)
                )
                result["content"] = proc.stdout.strip()[:2000] or "审计完成，未发现高危问题"
                if proc.returncode != 0:
                    result["status"] = "warn"
            except subprocess.TimeoutExpired:
                result["content"] = "审计超时（>30s），请稍后重试"
                result["status"] = "error"
            except Exception as e:
                result["content"] = f"审计异常: {e}"
                result["status"] = "error"
        else:
            result["content"] = "巡逻脚本不存在: bin/patrol_security.py"
            result["status"] = "error"
    
    # ── 五行/数字根 ──
    elif cmd == "wuxing":
        result["title"] = "龍魂 · 五行数字根"
        # 提取数字
        nums = re.findall(r'\d+', text)
        if nums:
            try:
                from wuxing_engine import compute_digital_root, get_wuxing_element  # type: ignore[import-untyped]
                num = int(nums[0])
                dr = sum(int(d) for d in str(num))
                while dr > 9:
                    dr = sum(int(d) for d in str(dr))
                wuxing_map = {1: "水", 2: "木", 3: "木", 4: "火", 5: "土", 6: "金", 7: "金", 8: "水", 9: "水"}
                wx = wuxing_map.get(dr, "未知")
                result["content"] = f"数字: {num}\n数字根: {dr}\n五行属性: {wx}行"
            except Exception as e:
                result["content"] = f"计算失败: {e}"
        else:
            result["content"] = '请提供数字，如"算一下 123"'
    
    # ── 路由查找 ──
    elif cmd == "route-find":
        result["title"] = "龍魂 · 路由查找"
        result["content"] = f"路由查找: {query or text}\n\n请使用完整节点编号，如 IPA-001, GATE-003"
    
    # ── DNA 查找 ──
    elif cmd == "dna-lookup":
        result["title"] = "龍魂 · DNA 追溯"
        result["content"] = f"DNA 追溯: {text}\n\n运行 bin/lh_dna_verify.py 或搜索 01_protocols/ 目录"
    
    # ── 道德经 ──
    elif cmd == "daodejing":
        result["title"] = "龍魂 · 道德经"
        result["content"] = f"道德经查询: {text}\n\n详见 龍魂-daodejing-v4.1.html"
    
    # ── 未识别 ──
    else:
        result["title"] = "龍魂 · 帮助"
        result["content"] = (
            "🐉 我能帮你查这些:\n\n"
            "📊 协同场 · 看看协同场怎么样 / 有没有冲突 / 均衡吗 / 怎么分工\n"
            "👤 人格 · 人格 P01 / 人格 top5 / 人格 健康度\n"
            "🖥️ 系统 · 系统状态 / 检查安全\n"
            "🔢 五行 · 算一下 123 / 这属什么属性\n"
            "🗺️ 路由 · 节点在哪 IPA-001\n"
            "🧬 DNA · 查DNA / 验证DNA\n"
            "📖 道德经 · 第X章 / 上善若水\n\n"
            f"🧬 {DNA}"
        )
    
    return result

def build_feishu_card(result: Dict[str, Any], query_text: str = "") -> Dict[str, Any]:
    """将执行结果转为飞书卡片"""
    if "card" in result:
        return result["card"]
    
    title = result.get("title", "龍魂查询")
    content = result.get("content", "无内容")
    status = result.get("status", "ok")
    
    status_color = {"ok": "green", "error": "red", "warn": "yellow"}.get(status, "grey")
    status_icon = {"ok": "✅", "error": "🔴", "warn": "⚠️"}.get(status, "ℹ️")
    
    # 内容超过飞书卡片限制时分段
    content_preview = content[:2000]
    
    card = {
        "header": {
            "title": {"tag": "plain_text", "content": f"{status_icon} {title}"},
            "template": status_color,
        },
        "elements": [
            {
                "tag": "markdown",
                "content": content_preview,
            },
            {
                "tag": "hr",
            },
            {
                "tag": "note",
                "elements": [
                    {"tag": "plain_text", "content": f"{DNA} · {datetime.now(CST).strftime('%H:%M:%S')}"},
                ],
            },
        ],
    }
    
    if query_text:
        card["elements"].insert(0, {
            "tag": "markdown",
            "content": f"**查询:** {query_text[:100]}",
        })
    
    return card

# ─── API 端点 ───
@app.get("/health")
def health():
    return {"status": "ok", "service": "feishu-longhun-bridge", "dna": DNA}

@app.get("/api/query")
def api_query(q: str = ""):
    """HTTP 查询接口: GET /api/query?q=看看协同场怎么样"""
    if not q:
        return {"error": "请提供 q 参数"}
    intent = parse_intent(q)
    result = execute_command(intent)
    card = build_feishu_card(result, q)
    return {"intent": intent, "result": result, "card": card}

@app.post("/feishu/event")
async def feishu_event(request: Request):
    """飞书事件订阅"""
    body = await request.json()
    
    # URL 验证
    if body.get("type") == "url_verification":
        token = body.get("token", "")
        if FEISHU_VERIFY_TOKEN and token != FEISHU_VERIFY_TOKEN:
            raise HTTPException(status_code=403)
        return JSONResponse({"challenge": body.get("challenge", "")})
    
    # 消息事件
    if body.get("type") == "event_callback":
        event = body.get("event", {})
        if event.get("type") == "im.message.receive_v1":
            message = event.get("message", {})
            msg_id = message.get("message_id", "")
            content_str = message.get("content", "{}")
            
            try:
                content = json.loads(content_str) if isinstance(content_str, str) else content_str
            except json.JSONDecodeError:
                content = {}
            
            text = content.get("text", "").strip()
            if not text:
                return JSONResponse({"code": 0, "msg": "empty"})
            
            # 解析 + 执行
            intent = parse_intent(text)
            result = execute_command(intent)
            card = build_feishu_card(result, text)
            
            # 回复卡片
            sender = event.get("sender", {})
            open_id = sender.get("open_id", "")
            if open_id and msg_id:
                reply_feishu_card(open_id, msg_id, card)
            
            return JSONResponse({"code": 0, "msg": "ok", "intent": intent.get("cn_command", intent.get("intent"))})
    
    return JSONResponse({"code": 0})

@app.post("/webhook")
async def webhook(request: Request):
    """简化 Webhook — POST {text, open_id} → 返回卡片"""
    body = await request.json()
    text = body.get("text", "")
    webhook_url = body.get("webhook_url", "")
    
    intent = parse_intent(text)
    result = execute_command(intent)
    card = build_feishu_card(result, text)
    
    if webhook_url:
        import urllib.request
        req_body = {"msg_type": "interactive", "card": card}
        req = urllib.request.Request(webhook_url, data=json.dumps(req_body).encode(),
            headers={"Content-Type": "application/json"}, method="POST")
        try:
            urllib.request.urlopen(req)
        except Exception as e:
            print(f"Webhook 推送失败: {e}")
    
    return {"intent": intent.get("cn_command", intent.get("intent")), "card": card}

@app.get("/api/capabilities")
def api_capabilities():
    """列出所有可用查询能力"""
    return {
        "dna": DNA,
        "capabilities": [
            {"domain": "流场协同", "examples": ["看看协同场怎么样", "有没有冲突", "均衡吗", "怎么分工", "融合得怎么样", "协同报告"]},
            {"domain": "人格查询", "examples": ["人格 P01", "人格 top5", "人格 健康度", "人格 诸葛亮"]},
            {"domain": "系统状态", "examples": ["系统状态", "怎么样"]},
            {"domain": "安全审计", "examples": ["安全检查", "审计一下", "扫一下"]},
            {"domain": "五行数字根", "examples": ["算一下 123", "这属什么属性"]},
            {"domain": "路由查找", "examples": ["节点在哪 IPA-001"]},
            {"domain": "DNA追溯", "examples": ["查DNA", "验证DNA"]},
            {"domain": "道德经", "examples": ["第X章", "上善若水"]},
        ],
        "endpoints": {
            "health": "/health",
            "query": "/api/query?q=查询内容",
            "event": "/feishu/event (飞书事件订阅)",
            "webhook": "/webhook (简化调用)",
            "capabilities": "/api/capabilities",
        },
    }

# ─── 启动 ───
if __name__ == "__main__":
    import uvicorn
    print(f"""
🐉 龍魂 · 飞书桥接智能体
═══════════════════════════
  {DNA}
  {CONFIRM}

  端口: {BRIDGE_BOT_PORT}
  健康检查: http://localhost:{BRIDGE_BOT_PORT}/health
  能力列表: http://localhost:{BRIDGE_BOT_PORT}/api/capabilities
  查询接口: http://localhost:{BRIDGE_BOT_PORT}/api/query?q=看看协同场怎么样
  飞书事件: http://your-server:{BRIDGE_BOT_PORT}/feishu/event
""")
    uvicorn.run(app, host="127.0.0.1", port=BRIDGE_BOT_PORT)
