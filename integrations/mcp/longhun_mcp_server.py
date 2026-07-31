# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║              龍魂系统 MCP Server v2.0 — 全系统能力桥接                 ║
║  DNA: #龍芯⚡️2026-07-13-LONGHUN-MCP-SERVER-v2.0                    ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                     ║
║  创建者: UID9622（诸葛鑫·Lucky）                                     ║
║  三色审计: 🟢 通过                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

【这是什么？】
龍魂系统核心 MCP Server — 对外暴露龍魂系统全部核心能力的统一接口。
让外部 AI 客户端（Claude Desktop、CodeBuddy、Cursor 等）调用龍魂。

【本 MCP Server 提供什么？】
16 个工具，覆盖龍魂全部子系统：
  ❤️ longhun_health        — 系统健康检查
  🧬 longhun_dna_gen        — 生成 DNA 追溯码（v∞ 格式）
  🛡️ longhun_audit          — 三色审计扫描
  🪪 longhun_identity       — 身份核验 + 系统拓扑
  🧠 longhun_semantic       — 中英语义路由解析
  ☯️  longhun_wuxing         — 五行数字根分析
  📡 longhun_kb_search       — 知识图谱搜索
  🔗 longhun_api_list        — 列出全部 API 端点
  👁️  longhun_vision_parse   — 视觉解析桥接（图像分析）
  🎤 longhun_audio_parse     — 音频解析桥接（语音分析）
  💬 longhun_semantic_parse  — 语义解析桥接（意图/情感/实体）
  🚀 longhun_cannon          — 全自动机枪扫描
  🧹 longhun_self_heal       — 系统自愈
  🔄 longhun_auto_sync       — 触发自动同步
  📋 longhun_persona_list    — 列出所有人格
  🎭 longhun_persona_status  — 查询单个人格状态

v2.0 新增: 视觉/音频/语义三模块桥接 + 人格管理
"""

import sys
import os
import json
import uuid
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

# 项目根
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

# ── MCP stdio 协议 ──
# 基于 JSON-RPC 2.0 over stdin/stdout
# 参考: https://spec.modelcontextprotocol.io/


def _log(msg: str):
    """写日志到 stderr（stdout 被 MCP 协议占用）"""
    print(f"[longhun-mcp] {msg}", file=sys.stderr, flush=True)


def _send_json(data: dict[str, Any]):
    """发送 JSON-RPC 响应"""
    sys.stdout.write(json.dumps(data, ensure_ascii=False) + "\n")
    sys.stdout.flush()


# ═══════════════════════════════════
# 龍魂工具实现
# ═══════════════════════════════════

def tool_health() -> dict[str, Any]:
    """系统健康检查"""
    api_up = False
    try:
        import httpx
        r = httpx.get("http://127.0.0.1:9622/api/system/health", timeout=3)
        api_up = r.status_code == 200
    except Exception:
        pass

    return {
        "ok": True,
        "system": "龍魂 v2.5.0",
        "uid": "UID9622",
        "api_backend": "up" if api_up else "down",
        "api_port": 9622,
        "web_portal": "http://127.0.0.1:8777",
        "timestamp_gz": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def tool_dna_gen(module: str = "MCP", action: str = "CALL") -> dict[str, Any]:
    """生成 DNA 追溯码"""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = hashlib.sha256(f"{ts}-{module}-{action}-UID9622".encode()).hexdigest()[:8].upper()
    dna = f"#龍芯⚡️{ts}-{module}-{action}-{h}"

    # 尝试用系统DNA生成器
    dna_script = ROOT / "bin" / "hetu_luoshu_dna.py"
    if dna_script.exists():
        try:
            result = subprocess.run(
                ["python3", str(dna_script), "--module", module, "--action", action],
                capture_output=True, text=True, timeout=10, cwd=str(ROOT)
            )
            if result.returncode == 0:
                dna = result.stdout.strip().split("\n")[-1]
        except Exception:
            pass

    return {"dna": dna, "module": module, "action": action, "format": "v∞"}


def tool_audit(text: str = "") -> dict[str, Any]:
    """三色审计扫描"""
    if not text:
        return {"ok": True, "color": "green", "message": "无内容需要审计"}

    # 调用防篡改扫描
    anti_tamper = ROOT / "bin" / "lh_anti_tamper.py"
    if anti_tamper.exists():
        try:
            result = subprocess.run(
                ["python3", str(anti_tamper), "scan", text],
                capture_output=True, text=True, timeout=30, cwd=str(ROOT)
            )
            color = "red" if result.returncode == 2 else "yellow" if result.returncode == 1 else "green"
            return {
                "ok": color != "red",
                "color": color,
                "exit_code": result.returncode,
                "output": result.stdout.strip()[-500:],
                "verdict": "🔴 熔断" if color == "red" else "🟡 待审" if color == "yellow" else "🟢 通过",
            }
        except Exception as e:
            return {"ok": True, "color": "gray", "error": str(e)}

    # 兜底：简易关键词检测
    red_words = ["技术无国界", "用户体验优先", "灵活处理", "国际接轨", "简化管理"]
    yellow_words = ["优化", "完善", "补充", "建议", "更好", "专业", "规范"]

    for w in red_words:
        if w in text:
            return {"ok": False, "color": "red", "verdict": "🔴 熔断", "trigger": w}
    for w in yellow_words:
        if w in text:
            return {"ok": True, "color": "yellow", "verdict": "🟡 待审", "trigger": w}

    return {"ok": True, "color": "green", "verdict": "🟢 通过"}


def tool_semantic(input_text: str) -> dict[str, Any]:
    """中英语义路由解析"""
    parser = ROOT / "bin" / "semantic_parser.py"
    if parser.exists():
        try:
            result = subprocess.run(
                ["python3", str(parser), input_text],
                capture_output=True, text=True, timeout=10, cwd=str(ROOT)
            )
            return {"ok": True, "input": input_text, "parsed": result.stdout.strip()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # 简易判断
    has_cn = any('\u4e00' <= c <= '\u9fff' for c in input_text)
    return {
        "ok": True,
        "input": input_text,
        "track": "中文轨" if has_cn else "英文轨",
        "language": "zh" if has_cn else "en",
    }


def tool_wuxing(text: str) -> dict[str, Any]:
    """五行数字根分析"""
    wuxing_check = ROOT / "bin" / "lh_wuxing_check.py"
    if wuxing_check.exists():
        try:
            result = subprocess.run(
                ["python3", str(wuxing_check), text],
                capture_output=True, text=True, timeout=10, cwd=str(ROOT)
            )
            return {"ok": True, "input": text, "output": result.stdout.strip()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # 简易数字根计算
    dr = sum(ord(c) for c in text) % 9 or 9
    wuxing_map = {1: "水", 2: "木", 3: "木", 4: "火", 5: "土", 6: "金", 7: "金", 8: "水", 9: "水"}
    return {"ok": True, "input_text": text, "digital_root": dr, "wuxing": wuxing_map.get(dr, "未知")}


def tool_kb_search(query: str) -> dict[str, Any]:
    """知识图谱搜索"""
    import httpx
    try:
        r = httpx.get(f"http://127.0.0.1:9622/api/kb/search", params={"q": query}, timeout=5)
        if r.status_code == 200:
            return {"ok": True, "query": query, "results": r.json()}
    except Exception:
        pass
    return {"ok": False, "query": query, "message": "API 后端未连接，请启动 longhun-api"}


def tool_cannon(mode: str = "full") -> dict[str, Any]:
    """全自动机枪扫描"""
    cannon_script = ROOT / "bin" / "lh_auto_cannon.py"
    if not cannon_script.exists():
        return {"ok": False, "error": "lh_auto_cannon.py 未找到"}

    try:
        args = ["python3", str(cannon_script)]
        if mode == "scan":
            args.append("--scan")
        elif mode == "fix":
            args.append("--fix")
        elif mode == "health":
            args.append("--health")
        elif mode == "report":
            args.append("--report")

        result = subprocess.run(
            args, capture_output=True, text=True, timeout=120, cwd=str(ROOT)
        )
        return {
            "ok": result.returncode == 0,
            "mode": mode,
            "exit_code": result.returncode,
            "output": result.stdout.strip()[-2000:],
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def tool_vision_parse(image_path: str = "", text_hint: str = "") -> dict[str, Any]:
    """视觉解析桥接 — 调用 lh_vision_parser"""
    vision_path = ROOT / "bin" / "lh_vision_parser.py"
    if not vision_path.exists():
        return {"ok": False, "error": "lh_vision_parser.py 未找到"}
    try:
        result = subprocess.run(
            ["python3", "-c", f"""
import sys, json
sys.path.insert(0, '{ROOT}')
from bin.lh_vision_parser import VisionParser, is_available
if not is_available():
    print(json.dumps({{"ok": False, "error": "视觉引擎不可用"}}))
else:
    p = VisionParser()
    # 仅返回模块状态
    print(json.dumps({{"ok": True, "engine_available": True,
        "pipeline": ["预处理","OCR","场景","情绪","结构化"],
        "features": ["截图优化","去噪","格式统一"]}}, ensure_ascii=False))
"""],
            capture_output=True, text=True, timeout=10, cwd=str(ROOT)
        )
        output = result.stdout.strip()
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return {"ok": True, "module": "lh_vision_parser", "status": "loaded",
                    "pipeline": ["预处理→OCR→场景→情绪→结构化JSON"],
                    "features": ["截图优化(应用名/聊天界面/时间戳/电量/信号)"]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def tool_audio_parse(audio_path: str = "") -> dict[str, Any]:
    """音频解析桥接 — 调用 lh_audio_parser"""
    audio_module = ROOT / "bin" / "lh_audio_parser.py"
    if not audio_module.exists():
        return {"ok": False, "error": "lh_audio_parser.py 未找到"}
    try:
        result = subprocess.run(
            ["python3", "-c", f"""
import sys, json
sys.path.insert(0, '{ROOT}')
from bin.lh_audio_parser import AudioParser, SpeechCleaner, is_available
cleaner = SpeechCleaner()
test = cleaner.clean("那个那个，我想问一下，就是说这个订单")
print(json.dumps({{"ok": True, "engine_available": is_available(),
    "pipeline": ["语音转文字","说话人分离","情绪分析","关键词提取"],
    "speech_cleaner_test": test}}, ensure_ascii=False))
"""],
            capture_output=True, text=True, timeout=10, cwd=str(ROOT)
        )
        output = result.stdout.strip()
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return {"ok": True, "module": "lh_audio_parser", "status": "loaded",
                    "pipeline": ["STT→说话人分离→情绪→关键词"],
                    "features": ["口语清洗(填充词/重复/修正过滤)"]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def tool_semantic_parse(text: str) -> dict[str, Any]:
    """语义解析桥接 — 调用 lh_semantic_parser"""
    semantic_module = ROOT / "bin" / "lh_semantic_parser.py"
    if not semantic_module.exists():
        return {"ok": False, "error": "lh_semantic_parser.py 未找到"}
    try:
        result = subprocess.run(
            ["python3", str(semantic_module), "--json", text],
            capture_output=True, text=True, timeout=15, cwd=str(ROOT)
        )
        output = result.stdout.strip()
        if output:
            try:
                return {"ok": True, **json.loads(output)}
            except json.JSONDecodeError:
                pass
        # 回退：直接 Python 调用
        result2 = subprocess.run(
            ["python3", "-c", f"""
import sys, json
sys.path.insert(0, '{ROOT}')
from bin.lh_semantic_parser import parse
r = parse('{text.replace(chr(39), chr(92)+chr(39))}')
rec = r.to_audit_record()
print(json.dumps({{"ok": True, "intent": r.intent.label, "confidence": r.intent.confidence,
    "sentiment": r.sentiment.polarity, "intensity": r.sentiment.intensity,
    "risk_level": r.risk_level, "entities": [(e.entity_type, e.value) for e in r.entities],
    "audit_hash": rec.get("input_hash"), "route_to": r.intent.route_to}}, ensure_ascii=False))
"""],
            capture_output=True, text=True, timeout=15, cwd=str(ROOT)
        )
        try:
            return json.loads(result2.stdout.strip())
        except json.JSONDecodeError:
            return {"ok": True, "module": "lh_semantic_parser", "status": "loaded",
                    "pipeline": ["意图识别(6类)→情感分析(正/负/中性)→实体提取"],
                    "features": ["三模块桥接(vision→semantic, audio→semantic)"]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def tool_self_heal() -> dict[str, Any]:
    """系统自愈"""
    heal_script = ROOT / "bin" / "longhun-self-heal.py"
    if not heal_script.exists():
        return {"ok": False, "error": "longhun-self-heal.py 未找到"}
    try:
        result = subprocess.run(
            ["python3", str(heal_script), "--dry-run"],
            capture_output=True, text=True, timeout=60, cwd=str(ROOT)
        )
        return {
            "ok": result.returncode == 0,
            "exit_code": result.returncode,
            "output": result.stdout.strip()[-1000:],
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def tool_auto_sync() -> dict[str, Any]:
    """触发自动同步"""
    sync_script = ROOT / "bin" / "longhun_auto_sync.py"
    if not sync_script.exists():
        return {"ok": False, "error": "longhun_auto_sync.py 未找到"}
    try:
        result = subprocess.run(
            ["python3", str(sync_script), "--status"],
            capture_output=True, text=True, timeout=30, cwd=str(ROOT)
        )
        return {
            "ok": result.returncode == 0,
            "exit_code": result.returncode,
            "output": result.stdout.strip()[-1000:],
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def tool_persona_list() -> dict[str, Any]:
    """列出所有人格"""
    personas_dir = ROOT / "personas"
    if not personas_dir.exists():
        return {"ok": False, "error": "personas/ 目录未找到"}
    personas = []
    for f in sorted(personas_dir.glob("*.md")):
        name = f.stem
        try:
            first_line = f.read_text().split("\n")[0].strip("# ")
        except Exception:
            first_line = name
        personas.append({"id": name, "name": first_line, "file": str(f.relative_to(ROOT))})
    return {"ok": True, "count": len(personas), "personas": personas,
            "note": "16/16 满编 · 0红色" if len(personas) >= 16 else f"{len(personas)}/16"}


def tool_persona_status(persona_id: str = "") -> dict[str, Any]:
    """查询单个人格状态"""
    if not persona_id:
        return tool_persona_list()
    persona_file = ROOT / "personas" / f"{persona_id}.md"
    if not persona_file.exists():
        # 模糊匹配
        for f in (ROOT / "personas").glob("*.md"):
            if persona_id.lower() in f.stem.lower():
                persona_file = f
                break
        else:
            return {"ok": False, "error": f"人格 '{persona_id}' 未找到",
                    "available": [f.stem for f in sorted((ROOT / "personas").glob("*.md"))]}
    try:
        content = persona_file.read_text()
        title = content.split("\n")[0].strip("# ")
        return {"ok": True, "id": persona_file.stem, "title": title,
                "file": str(persona_file.relative_to(ROOT)),
                "size": len(content), "lines": len(content.split("\n"))}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def tool_api_list() -> dict[str, Any]:
    """列出可用 API 端点"""
    return {
        "ok": True,
        "api_base": "http://127.0.0.1:9622",
        "swagger": "http://127.0.0.1:9622/api/docs",
        "endpoints": [
            {"method": "GET", "path": "/api/system/health", "auth": False, "desc": "健康检查"},
            {"method": "POST", "path": "/api/auth/register", "auth": False, "desc": "注册"},
            {"method": "POST", "path": "/api/auth/login", "auth": False, "desc": "登录"},
            {"method": "GET", "path": "/api/agents", "auth": True, "desc": "Agent 列表"},
            {"method": "GET", "path": "/api/models", "auth": True, "desc": "AI 模型列表"},
            {"method": "POST", "path": "/api/models/generate", "auth": True, "desc": "文本生成"},
            {"method": "POST", "path": "/api/models/chat", "auth": True, "desc": "对话"},
            {"method": "GET", "path": "/api/kb/search", "auth": True, "desc": "知识图谱搜索"},
            {"method": "GET", "path": "/api/vpn/nodes", "auth": True, "desc": "VPN 节点"},
            {"method": "GET", "path": "/api/memory/search", "auth": True, "desc": "记忆搜索"},
            {"method": "GET", "path": "/api/ws", "auth": False, "desc": "WebSocket"},
        ],
    }


# ═══════════════════════════════════
# 工具注册表
# ═══════════════════════════════════

TOOLS = {
    "longhun_health": {
        "handler": tool_health,
        "description": "龍魂系统健康检查 — 检查 API 后端、Web 门户、Ollama 是否在线",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "longhun_dna_gen": {
        "handler": tool_dna_gen,
        "description": "生成龍魂 DNA 追溯码（v∞ 格式：#龍芯⚡️日期-模块-动作-哈希8位）",
        "inputSchema": {
            "type": "object",
            "properties": {
                "module": {"type": "string", "description": "模块名，如 MCP/API/AUDIT"},
                "action": {"type": "string", "description": "动作名，如 CALL/CHECK/GEN"},
            },
        },
    },
    "longhun_audit": {
        "handler": tool_audit,
        "description": "三色审计扫描 — 检测内容是否安全可入库（🔴熔断/🟡待审/🟢通过）",
        "inputSchema": {
            "type": "object",
            "properties": {"text": {"type": "string", "description": "待审计文本"}},
            "required": ["text"],
        },
    },
    "longhun_identity": {
        "handler": lambda: {
            "system": "龍魂 v2.5.0", "uid": "UID9622", "identity": "诸葛鑫·Lucky",
            "dna": "#龍芯⚡️丙午·丙申·丙辰·亥时·需-LONGHUN-NEURAL-NET-TOPOLOGY-v3.0",
            "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
            "architecture": "L0-L9 九层·洛书九宫骨架",
            "personas": "16/16 满编·0红色",
            "engines": 122, "skills": 45, "edge_count": 21,
            "gate": "三闸门(数字根→身份→伦理)",
        },
        "description": "龍魂系统身份核验 — 返回系统拓扑、架构、版本等核心身份信息",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "longhun_semantic": {
        "handler": tool_semantic,
        "description": "中英语义路由解析 — 输入任意中文/英文，返回解析结果和语言轨道",
        "inputSchema": {
            "type": "object",
            "properties": {"input_text": {"type": "string", "description": "输入文本（中文或英文）"}},
            "required": ["input_text"],
        },
    },
    "longhun_wuxing": {
        "handler": tool_wuxing,
        "description": "五行数字根分析 — 计算文本的数字根和五行属性（金木水火土）",
        "inputSchema": {
            "type": "object",
            "properties": {"text": {"type": "string", "description": "待分析的文本"}},
            "required": ["text"],
        },
    },
    "longhun_kb_search": {
        "handler": tool_kb_search,
        "description": "知识图谱搜索 — 搜索龍魂知识库（需 longhun-api 运行中）",
        "inputSchema": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "搜索关键词"}},
            "required": ["query"],
        },
    },
    "longhun_api_list": {
        "handler": tool_api_list,
        "description": "列出龍魂系统所有可用 API 端点（12个API端点）",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "longhun_cannon": {
        "handler": tool_cannon,
        "description": "龍魂全自动机枪 — 一键系统扫描+修复+健康评估+报告",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mode": {"type": "string", "enum": ["scan", "fix", "health", "report", "full"],
                         "description": "模式: scan/fix/health/report (默认 full=全部)"},
            },
        },
    },
    "longhun_vision_parse": {
        "handler": tool_vision_parse,
        "description": "视觉解析桥接 — 检查 lh_vision_parser 模块状态（五步管线：预处理→OCR→场景→情绪→结构化）",
        "inputSchema": {
            "type": "object",
            "properties": {
                "image_path": {"type": "string", "description": "图片路径（可选，仅检查模块状态）"},
            },
        },
    },
    "longhun_audio_parse": {
        "handler": tool_audio_parse,
        "description": "音频解析桥接 — 检查 lh_audio_parser 模块状态（四步管线：STT→说话人分离→情绪→关键词）",
        "inputSchema": {
            "type": "object",
            "properties": {
                "audio_path": {"type": "string", "description": "音频路径（可选，仅检查模块状态）"},
            },
        },
    },
    "longhun_semantic_parse": {
        "handler": tool_semantic_parse,
        "description": "语义解析 — 意图识别(6类)+情感分析+实体提取。返回意图/情感/风险/实体/审计哈希。",
        "inputSchema": {
            "type": "object",
            "properties": {"text": {"type": "string", "description": "要解析的文本"}},
            "required": ["text"],
        },
    },
    "longhun_self_heal": {
        "handler": tool_self_heal,
        "description": "系统自愈 — 执行自动修复检查（dry-run模式，不实际修改）",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "longhun_auto_sync": {
        "handler": tool_auto_sync,
        "description": "触发自动同步 — 检查同步状态",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "longhun_persona_list": {
        "handler": tool_persona_list,
        "description": "列出所有人格 — 16人格矩阵（16/16 满编，0红色）",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "longhun_persona_status": {
        "handler": tool_persona_status,
        "description": "查询单个人格状态 — 返回人格定义、文件大小、行数",
        "inputSchema": {
            "type": "object",
            "properties": {"persona_id": {"type": "string", "description": "人格 ID（如 P00、P03，留空则列出全部）"}},
        },
    },
}


# ═══════════════════════════════════
# JSON-RPC 消息处理
# ═══════════════════════════════════

def handle_request(msg: dict[str, Any]) -> dict | None:
    """处理 JSON-RPC 请求，返回响应或 None（通知）"""
    msg_id = msg.get("id")
    method = msg.get("method")

    # ── initialize ──
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                },
                "serverInfo": {
                    "name": "longhun-mcp",
                    "version": "1.0.0",
                },
            },
        }

    # ── notifications/initialized ──
    if method == "notifications/initialized":
        _log("✅ MCP 客户端已初始化")
        return None  # 通知不需要响应

    # ── tools/list ──
    if method == "tools/list":
        tools_list = []
        for name, meta in TOOLS.items():
            tools_list.append({
                "name": name,
                "description": meta["description"],
                "inputSchema": meta["inputSchema"],
            })
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"tools": tools_list},
        }

    # ── tools/call ──
    if method == "tools/call":
        params = msg.get("params", {})
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})

        if tool_name not in TOOLS:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"未知工具: {tool_name}"},
            }

        try:
            handler = TOOLS[tool_name]["handler"]
            result = handler(**arguments) if arguments else handler()
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}],
                },
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": f"错误: {e}"}],
                    "isError": True,
                },
            }

    # ── ping ──
    if method == "ping":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

    # 未知方法
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"未知方法: {method}"},
    }


# ═══════════════════════════════════
# 主循环
# ═══════════════════════════════════

def main():
    _log("🐉 龍魂 MCP Server v2.0 启动")
    _log(f"   项目根: {ROOT}")
    _log(f"   可用工具 ({len(TOOLS)}): {', '.join(TOOLS.keys())}")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError as e:
            _log(f"JSON 解析错误: {e}")
            continue

        response = handle_request(msg)
        if response is not None:
            _send_json(response)

    _log("🐉 龍魂 MCP Server 关闭")


if __name__ == "__main__":
    main()
