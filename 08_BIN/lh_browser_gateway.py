#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·辛酉·未时·䷔噬嗑-BROWSER-DEVTOOLS-GATEWAY-v1.0
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 三色: 🟢 通过
"""
🐉 龍魂 · 浏览器指令网关（鲲鹏端）v1.0
================================================
跨设备控制中枢：小艺(鸿蒙)/Kimi/CodeBuddy/终端 → 鲲鹏网关 → Mac浏览器控制器

链路: 小艺/Kimi/CodeBuddy → 鲲鹏 :8768 (本网关) → SSH反向隧道 → Mac :9766

功能:
  1. 接收自然语言指令（小艺/Kimi/CodeBuddy/curl）
  2. 通心译转译（口语 → 浏览器操作）
  3. DNA注入 + 三色审计
  4. 转发到 Mac 执行
  5. 史官记录 + 耻辱墙

端点:
  POST /api/browser/command    - 执行浏览器指令（自然语言）
  GET  /api/browser/status     - 获取 Mac 浏览器状态
  GET  /api/browser/config     - 获取 Mac 浏览器配置
  GET  /api/browser/snapshot   - 页面快照
  POST /api/browser/open       - 打开 URL
  GET  /api/health             - 健康检查

部署: 鲲鹏 /opt/longhun-system/08_BIN/ · :8768
      MAC_BROWSER_HOST 默认 127.0.0.1（SSH 反向隧道打通 Mac:9766 → 鲲鹏:9766）
DNA: #龍芯⚡️丙午·丙申·辛酉·未时·䷔噬嗑-BROWSER-DEVTOOLS-GATEWAY-v1.0-9622
"""

import os
import sys
import json
import time
import re
import hashlib
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ============================================================
# DNA（v∞ 干支四柱 · 真实时间引擎）
# ============================================================

def _time_stamp_compact() -> str:
    try:
        sys.path.insert(0, "/opt/longhun-system/bin")
        from lh_time_engine import get_output_stamp  # noqa
        stamp = get_output_stamp(format_type="compact") or ""
        if "⚡️" in stamp:
            return stamp.split("⚡️", 1)[1].strip()
    except Exception:
        pass
    return datetime.now().strftime("%Y-%m-%d")


def generate_dna(suffix: str = "GATEWAY") -> str:
    four_pillars = _time_stamp_compact()
    rand = hashlib.sha256(f"{suffix}{datetime.now().isoformat()}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{four_pillars}-GATEWAY-{suffix}-{rand}"


# ============================================================
# 配置
# ============================================================

# Mac 浏览器控制器地址（⚠️ 鲲鹏公网直连 Mac 内网 IP 不可达！
# 默认 127.0.0.1 = SSH 反向隧道打通 Mac:9766 → 鲲鹏:9766）
MAC_BROWSER_HOST = os.getenv("MAC_BROWSER_HOST", "127.0.0.1")
MAC_BROWSER_PORT = os.getenv("MAC_BROWSER_PORT", "9766")
MAC_BROWSER_URL = f"http://{MAC_BROWSER_HOST}:{MAC_BROWSER_PORT}"

# 史官/耻辱墙路径（默认鲲鹏 /opt/longhun-system；本机测试时自动识别本地仓库）
_LOCAL_ROOT = Path(__file__).resolve().parent.parent  # 本机 longhun-system
if (_LOCAL_ROOT / "04_AUDIT").exists():
    _SYSTEM_ROOT = _LOCAL_ROOT  # 本机开发/测试
else:
    _SYSTEM_ROOT = Path(os.getenv("LONGHUN_ROOT", "/opt/longhun-system"))  # 鲲鹏
AUDIT_PATH = _SYSTEM_ROOT / "04_AUDIT" / "browser_gateway.jsonl"
SHAME_PATH = _SYSTEM_ROOT / "08_STATE" / "shame_wall.jsonl"
for _p in (AUDIT_PATH.parent, SHAME_PATH.parent):
    _p.mkdir(parents=True, exist_ok=True)


# ============================================================
# 通心译映射：口语 → 浏览器操作
# ============================================================

TONXINYI_BROWSER_MAP = {
    # 启动/停止
    "打开浏览器开发者模式": {"action": "start", "params": {"devtools": True}},
    "打开浏览器": {"action": "start", "params": {"devtools": False}},
    "关闭浏览器": {"action": "stop", "params": {}},
    "浏览器状态": {"action": "status", "params": {}},
    "浏览器状态如何": {"action": "status", "params": {}},
    "强制关闭浏览器": {"action": "kill", "params": {}},

    # 参数调整
    "设置用户代理": {"action": "set_user_agent", "params": {}},
    "修改用户代理": {"action": "set_user_agent", "params": {}},
    "设置视口": {"action": "set_viewport", "params": {}},
    "设置视口大小": {"action": "set_viewport", "params": {}},
    "设置地理位置": {"action": "set_geolocation", "params": {}},
    "设置时区": {"action": "set_timezone", "params": {}},

    # 功能选择
    "开启开发者工具": {"action": "set_devtools", "params": {"enabled": True}},
    "关闭开发者工具": {"action": "set_devtools", "params": {"enabled": False}},
    "启用JavaScript": {"action": "set_js", "params": {"enabled": True}},
    "禁用JavaScript": {"action": "set_js", "params": {"enabled": False}},
    "启用缓存": {"action": "set_cache", "params": {"enabled": True}},
    "禁用缓存": {"action": "set_cache", "params": {"enabled": False}},

    # 安全防御
    "启用反指纹": {"action": "enable_anti_fingerprint", "params": {}},
    "开启反指纹": {"action": "enable_anti_fingerprint", "params": {}},
    "启用隐私模式": {"action": "enable_privacy_mode", "params": {}},
    "开启隐私模式": {"action": "enable_privacy_mode", "params": {}},

    # 查看
    "查看浏览器配置": {"action": "get_config", "params": {}},
    "浏览器配置": {"action": "get_config", "params": {}},
    "查看浏览器日志": {"action": "get_logs", "params": {}},
    "浏览器日志": {"action": "get_logs", "params": {}},
    "页面快照": {"action": "snapshot", "params": {}},
    "重置浏览器配置": {"action": "clear_config", "params": {}},

    # 导航
    "打开网页": {"action": "open_url", "params": {}},
    "打开网址": {"action": "open_url", "params": {}},
    "打开": {"action": "open_url", "params": {}},
}


def translate_command(text: str) -> Dict:
    """通心译：口语 → 浏览器操作（长关键词优先消歧）"""
    # 长关键词优先（防"打开"误触发"打开浏览器"）
    for key in sorted(TONXINYI_BROWSER_MAP.keys(), key=len, reverse=True):
        if key in text:
            return dict(TONXINYI_BROWSER_MAP[key])
    return {"action": "unknown", "params": {}}


# ============================================================
# 史官 / 耻辱墙
# ============================================================

def record_historian(action: str, dna: str, details: Dict, tricolor: str = "🟢"):
    record = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "dna": dna,
        "tricolor": tricolor,
        "details": details,
    }
    with open(AUDIT_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_shame_wall(reason: str, details: Dict):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "reason": reason,
        "details": details,
        "severity": "HIGH",
        "dna": generate_dna("SHAME"),
    }
    with open(SHAME_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ============================================================
# 转发到 Mac（urllib 零依赖·不强制 requests）
# ============================================================

def _http_json(method: str, path: str, body: Optional[Dict] = None, timeout: int = 10) -> Dict:
    url = f"{MAC_BROWSER_URL}{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        return {"status": "error", "message": f"Mac浏览器控制器不可达: {e}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# 操作 → (HTTP方法, 路径, 参数名映射)
_ACTION_ROUTES = {
    "start": ("POST", "/start", None),
    "stop": ("POST", "/stop", None),
    "status": ("GET", "/status", None),
    "kill": ("POST", "/kill", None),
    "set_user_agent": ("POST", "/set_user_agent", {"user_agent": "user_agent"}),
    "set_viewport": ("POST", "/set_viewport", {"width": "width", "height": "height"}),
    "set_geolocation": ("POST", "/set_geolocation", {"latitude": "latitude", "longitude": "longitude"}),
    "set_timezone": ("POST", "/set_timezone", {"timezone": "timezone"}),
    "set_devtools": ("POST", "/set_devtools", {"enabled": "enabled"}),
    "set_js": ("POST", "/set_js", {"enabled": "enabled"}),
    "set_cache": ("POST", "/set_cache", {"enabled": "enabled"}),
    "enable_anti_fingerprint": ("POST", "/enable_anti_fingerprint", None),
    "enable_privacy_mode": ("POST", "/enable_privacy_mode", None),
    "get_config": ("GET", "/config", None),
    "get_logs": ("GET", "/logs", None),
    "snapshot": ("GET", "/snapshot", None),
    "clear_config": ("POST", "/clear", None),
    "open_url": ("POST", "/open_url", {"url": "url"}),
}


def forward_to_mac(action: str, params: Dict) -> Dict:
    """转发指令到 Mac 浏览器控制器"""
    route = _ACTION_ROUTES.get(action)
    if not route:
        return {"status": "error", "message": f"未知操作: {action}"}
    method, path, mapping = route

    # 参数映射
    body = None
    if mapping:
        body = {}
        for src, dst in mapping.items():
            if src in params and params[src] is not None:
                body[dst] = params[src]

    if action == "get_logs":
        path = f"/logs?limit=50"

    return _http_json(method, path, body)


# ============================================================
# FastAPI 服务
# ============================================================

def build_app():
    from fastapi import FastAPI, Request
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(
        title="🐉 龍魂 · 浏览器指令网关",
        version="1.0.0",
        dna="#龍芯⚡️丙午·丙申·辛酉·未时·䷔噬嗑-BROWSER-DEVTOOLS-GATEWAY-v1.0-9622",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,   # 修复: allow_origins=* 不能与 True 并存
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        return {
            "service": "🐉 龍魂 · 浏览器指令网关",
            "status": "🟢 运行中",
            "dna": generate_dna("ROOT"),
            "confirm": CONFIRM,
            "mac_browser_url": MAC_BROWSER_URL,
            "链路": "小艺/Kimi/CodeBuddy → 鲲鹏:8768 → SSH反向隧道 → Mac:9766",
        }

    @app.post("/api/browser/command")
    async def execute_command(request: Request):
        """执行浏览器指令（自然语言·小艺/Kimi/CodeBuddy 调用）"""
        try:
            data = await request.json()
        except Exception:
            data = {}
        text = data.get("text", "") or ""
        source = data.get("source", "unknown")
        dna = generate_dna("CMD")

        # 1. 通心译转译
        command = translate_command(text)

        if command.get("action") == "unknown":
            record_historian("unknown_command", dna,
                             {"text": text[:80], "source": source}, "🟡")
            return {
                "status": "error",
                "message": f"无法识别指令: {text[:80]}",
                "dna": dna,
                "suggestions": sorted(TONXINYI_BROWSER_MAP.keys())[:8],
                "tricolor": "🟡",
            }

        # 2. 从自然语言提取参数
        params = dict(command.get("params", {}))
        action = command["action"]
        numbers = re.findall(r'-?\d+(?:\.\d+)?', text)

        if action == "set_viewport" and len(numbers) >= 2:
            params["width"] = int(float(numbers[0]))
            params["height"] = int(float(numbers[1]))
        elif action == "set_geolocation" and len(numbers) >= 2:
            params["latitude"] = float(numbers[0])
            params["longitude"] = float(numbers[1])
        elif action == "set_user_agent":
            # 取引号里的 UA
            m = re.search(r'["\']([^"\']+)["\']', text)
            if m:
                params["user_agent"] = m.group(1)
        elif action == "set_timezone":
            m = re.search(r'([A-Za-z]+/[A-Za-z_]+)', text)
            if m:
                params["timezone"] = m.group(1)
        elif action == "open_url":
            # 找 URL 或域名
            m = re.search(r'(?:https?://)?([a-zA-Z0-9][a-zA-Z0-9.-]+\.[a-z]{2,}(?:/[^\s，。]*)?)', text)
            if m:
                url = m.group(0)
                if not url.startswith("http"):
                    url = "https://" + url
                params["url"] = url

        # 3. 转发到 Mac
        result = forward_to_mac(action, params)

        # 4. 三色审计 + 史官
        tricolor = "🟢"
        if result.get("status") == "error":
            tricolor = "🔴"
            write_shame_wall("browser_command_failed", {
                "source": source, "text": text[:80], "error": str(result.get("message"))[:200],
            })
        elif "warning" in str(result.get("status", "")):
            tricolor = "🟡"
        record_historian(action, dna, {
            "source": source, "text": text[:80], "params": params, "mac_result": result,
        }, tricolor)

        return {
            "status": "success" if result.get("status") != "error" else "error",
            "dna": dna,
            "command": action,
            "text": text[:80],
            "source": source,
            "result": result,
            "tricolor": tricolor,
            "timestamp": datetime.now().isoformat(),
        }

    @app.get("/api/browser/status")
    async def get_browser_status():
        dna = generate_dna("STATUS")
        result = forward_to_mac("status", {})
        record_historian("status_check", dna, {"result": result})
        return {"dna": dna, "status": "success", "mac_status": result}

    @app.get("/api/browser/config")
    async def get_browser_config():
        dna = generate_dna("CONFIG")
        result = forward_to_mac("get_config", {})
        return {"dna": dna, "config": result}

    @app.get("/api/browser/snapshot")
    async def get_browser_snapshot():
        dna = generate_dna("SNAPSHOT")
        result = forward_to_mac("snapshot", {})
        return {"dna": dna, "snapshot": result}

    @app.get("/api/health")
    async def health_check():
        mac_status = forward_to_mac("status", {})
        return {
            "status": "healthy",
            "gateway_dna": generate_dna("HEALTH"),
            "mac_connected": mac_status.get("status") != "error",
            "mac_status": mac_status,
        }

    return app


def main():
    """CLI 入口: --serve 启动网关 / --status 显示配置 / 无参默认帮助"""
    import argparse
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 浏览器指令网关（鲲鹏端）")
    parser.add_argument("--serve", action="store_true", help="启动网关服务(:8768)")
    parser.add_argument("--status", action="store_true", help="显示网关配置")
    args = parser.parse_args()

    if args.status:
        print(json.dumps({
            "service": "龍魂 · 浏览器指令网关",
            "dna": generate_dna("STATUS"),
            "mac_browser_url": MAC_BROWSER_URL,
            "link": "小艺/Kimi/CodeBuddy → 鲲鹏:8768 → SSH反向隧道 → Mac:9766",
            "historian": str(AUDIT_PATH),
        }, ensure_ascii=False, indent=2))
        return

    if not args.serve:
        parser.print_help()
        return

    port = int(os.getenv("BROWSER_GATEWAY_PORT", "8768"))
    try:
        import uvicorn
    except ImportError:
        print(json.dumps({"status": "error",
                          "message": "uvicorn 未安装: pip install uvicorn"},
                         ensure_ascii=False, indent=2))
        return
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🐉 龍魂 · 浏览器指令网关 (鲲鹏端)                        ║
╠══════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·丙申·辛酉·未时·䷔噬嗑-BROWSER-GATEWAY ║
║  确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z              ║
╠══════════════════════════════════════════════════════════════╣
║  📡 网关: 0.0.0.0:{port}                                      ║
║  🔗 Mac: {MAC_BROWSER_URL} (SSH反向隧道)                      ║
║  📋 审计: 史官 + 耻辱墙 + 三色                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    uvicorn.run(build_app(), host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
