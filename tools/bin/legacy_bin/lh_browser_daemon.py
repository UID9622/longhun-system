#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
龍魂浏览器操作助手 · 本地守护进程 v1.0
==============================================
本地 HTTP API 服务，通过 Playwright 控制浏览器。
全部本地运行，无外部依赖，数据主权归 UID9622。

API 端点：
  POST /navigate    — 导航到 URL
  POST /snapshot    — 页面可访问性快照
  POST /click       — 点击元素
  POST /fill        — 填表
  POST /screenshot  — 截图（返回 base64 或保存文件）
  POST /evaluate    — 执行 JS
  POST /content     — 获取页面 HTML
  POST /wait        — 等待元素出现
  GET  /status      — 守护进程状态
  POST /shutdown    — 关闭守护进程

安全：
  - 仅监听 127.0.0.1，外部不可访问
  - 操作前过三色审计
  - 密码类字段不记录明文
  - 每次操作绑定 DNA 追溯

DNA: #龍芯⚡️丙午·丙申·乙卯·辰时·䷄需-BROWSER-DAEMON-v1.0-A1B2C3D4
"""

import json
import os
import sys
import time
import hashlib
import threading
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("[FATAL] playwright 未安装。请执行: pip install playwright && python -m playwright install chromium")
    sys.exit(1)

# ============================================================
# 配置
# ============================================================
HOST = "127.0.0.1"
PORT = 19862  # 龍魂浏览器守护端口
SESSION_DIR = Path.home() / ".longhun" / "browser_sessions"
SCREENSHOT_DIR = Path.home() / ".longhun" / "browser_screenshots"
LOG_FILE = Path.home() / ".longhun" / "browser_daemon.log"
HEADLESS = False  # 默认有头模式，方便观察
DEFAULT_TIMEOUT = 30_000  # ms

SESSION_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 三色审计
# ============================================================
class TricolorAudit:
    """操作前三色审计 — 简单版"""
    
    RISKY_ACTIONS = {"evaluate", "shutdown"}
    SENSITIVE_KEYS = {"password", "passwd", "token", "secret", "key", "api_key", "credential"}
    
    @staticmethod
    def audit(action: str, args: dict[str, Any]) -> dict[str, Any]:
        result = {"level": "GREEN", "reason": ""}
        
        # 检查危险操作
        if action in TricolorAudit.RISKY_ACTIONS:
            result["level"] = "YELLOW"
            result["reason"] = f"操作 '{action}' 属于敏感操作，已记录"
        
        # 检查敏感字段
        for key in args:
            if any(sk in key.lower() for sk in TricolorAudit.SENSITIVE_KEYS):
                result["level"] = "RED"
                result["reason"] = f"参数 '{key}' 包含敏感字段，明文不会记录"
                # 不阻止，但不记录明文
                break
        
        return result


# ============================================================
# 浏览器管理器
# ============================================================
class BrowserManager:
    """单例浏览器管理器，维护一个持久的浏览器实例"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.start_time = None
        self.action_count = 0
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def start(self):
        """启动浏览器"""
        if self.browser and self.browser.is_connected():
            return {"status": "already_running"}
        
        self._do_start()
        return {"status": "started", "headless": HEADLESS}
    
    def reset(self):
        """强制重置浏览器（关闭并重建）"""
        try:
            if self.page and not self.page.is_closed():
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser and self.browser.is_connected():
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except Exception:
            pass
        self.page = None
        self.context = None
        self.browser = None
        self.playwright = None
        self._do_start()
        return {"status": "reset_ok", "headless": HEADLESS}
    
    def _do_start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=HEADLESS,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--ignore-certificate-errors",  # 内网自签名证书
            ]
        )
        storage_state = SESSION_DIR / "browser_state.json"
        if storage_state.exists():
            self.context = self.browser.new_context(
                storage_state=str(storage_state),
                ignore_https_errors=True
            )
        else:
            self.context = self.browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                ignore_https_errors=True
            )
        
        self.page = self.context.new_page()
        self.start_time = time.time()
        self.action_count = 0
        
        return {"status": "started", "headless": HEADLESS}
    
    def ensure_page(self):
        """确保页面可用"""
        if self.page and not self.page.is_closed():
            return
        if self.context:
            self.page = self.context.new_page()
        else:
            self.start()
    
    def navigate(self, url: str) -> dict[str, Any]:
        self.ensure_page()
        assert self.page is not None, "Browser not started"
        try:
            self.page.goto(url, timeout=DEFAULT_TIMEOUT, wait_until="domcontentloaded")
            self.action_count += 1
            return {"success": True, "url": self.page.url, "title": self.page.title()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def snapshot(self) -> dict[str, Any]:
        self.ensure_page()
        assert self.page is not None, "Browser not started"
        try:
            # 生成简化可访问性树
            tree = self.page.evaluate("""() => {
                function getSnapshot(el, depth=0) {
                    if (depth > 20) return null;
                    const tag = el.tagName?.toLowerCase() || '';
                    const role = el.getAttribute('role') || '';
                    const type = el.getAttribute('type') || '';
                    const name = (el.getAttribute('aria-label') || el.getAttribute('name') || el.getAttribute('title') || el.getAttribute('placeholder') || el.textContent?.trim()?.substring(0, 60) || '').replace(/\\n/g, ' ');
                    const id = el.id || '';
                    const className = (typeof el.className === 'string') ? el.className.split(' ').slice(0,3).join(' ') : '';
                    const href = el.href || '';
                    const value = el.value || '';
                    const checked = el.checked || false;
                    const disabled = el.disabled || false;
                    const visible = el.offsetParent !== null;
                    
                    if (!visible && tag !== 'body' && tag !== 'html') return null;
                    
                    const children = [];
                    for (const child of el.children) {
                        const c = getSnapshot(child, depth+1);
                        if (c) children.push(c);
                    }
                    
                    return {tag, role, type, name, id, className, href, value, checked, disabled, children};
                }
                return getSnapshot(document.body);
            }""")
            self.action_count += 1
            return {"success": True, "url": self.page.url, "title": self.page.title(), "tree": tree}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def click(self, selector: str) -> dict[str, Any]:
        self.ensure_page()
        assert self.page is not None, "Browser not started"
        try:
            el = self.page.locator(selector).first
            el.click(timeout=DEFAULT_TIMEOUT)
            self.action_count += 1
            return {"success": True, "selector": selector, "tag": el.evaluate("el => el.tagName")}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def fill(self, selector: str, value: str) -> dict[str, Any]:
        self.ensure_page()
        assert self.page is not None, "Browser not started"
        try:
            el = self.page.locator(selector).first
            el.fill(value, timeout=DEFAULT_TIMEOUT)
            self.action_count += 1
            return {"success": True, "selector": selector, "filled": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def screenshot(self, path: str | None = None, full_page: bool = False) -> dict[str, Any]:
        self.ensure_page()
        assert self.page is not None, "Browser not started"
        try:
            if path is None:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = str(SCREENSHOT_DIR / f"screenshot_{ts}.png")
            else:
                Path(path).parent.mkdir(parents=True, exist_ok=True)
            
            self.page.screenshot(path=path, full_page=full_page)
            size = os.path.getsize(path)
            self.action_count += 1
            return {"success": True, "path": path, "size_bytes": size, "url": self.page.url}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def evaluate(self, code: str) -> dict[str, Any]:
        self.ensure_page()
        assert self.page is not None, "Browser not started"
        try:
            result = self.page.evaluate(code)
            self.action_count += 1
            # 安全序列化
            return {"success": True, "result": json.loads(json.dumps(result, default=str))}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_content(self) -> dict[str, Any]:
        self.ensure_page()
        assert self.page is not None, "Browser not started"
        try:
            html = self.page.content()
            self.action_count += 1
            return {"success": True, "url": self.page.url, "title": self.page.title(), "html_length": len(html)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def wait(self, selector: str, timeout: int | None = None) -> dict[str, Any]:
        self.ensure_page()
        assert self.page is not None, "Browser not started"
        try:
            t = timeout or DEFAULT_TIMEOUT
            self.page.wait_for_selector(selector, timeout=t)
            self.action_count += 1
            return {"success": True, "selector": selector, "found": True}
        except PlaywrightTimeout:
            return {"success": False, "error": f"等待超时: {selector}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def press_key(self, key: str) -> dict[str, Any]:
        """按下键盘按键（如 Enter, Tab, Escape）"""
        self.ensure_page()
        assert self.page is not None, "Browser not started"
        try:
            self.page.keyboard.press(key)
            self.action_count += 1
            return {"success": True, "key": key}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_status(self) -> dict[str, Any]:
        if self.browser and self.browser.is_connected():
            uptime = time.time() - self.start_time if self.start_time else 0
            page_url = self.page.url if (self.page and not self.page.is_closed()) else None
            page_title = self.page.title() if (self.page and not self.page.is_closed()) else None
            return {
                "running": True,
                "url": page_url,
                "title": page_title,
                "uptime_seconds": int(uptime),
                "action_count": self.action_count,
                "headless": HEADLESS,
            }
        return {"running": False}
    
    def shutdown(self):
        try:
            if self.context:
                self.context.storage_state(path=str(SESSION_DIR / "browser_state.json"))
            if self.page and not self.page.is_closed():
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser and self.browser.is_connected():
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except Exception:
            pass
        finally:
            self.page = None
            self.context = None
            self.browser = None
            self.playwright = None


# ============================================================
# HTTP 请求处理器
# ============================================================
class BrowserAPIHandler(BaseHTTPRequestHandler):
    
    manager = BrowserManager.get_instance()
    
    def log_message(self, format, *args):
        """日志写入文件"""
        msg = f"[{datetime.now().isoformat()}] {self.client_address[0]} - {format % args}"
        with open(LOG_FILE, "a") as f:
            f.write(msg + "\n")
    
    def _send_json(self, data: dict[str, Any], status: int = 200):
        body = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
    
    def _read_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw)
    
    def _dispatch(self, action: str, args: dict[str, Any]) -> dict[str, Any]:
        """命令路由"""
        # 三色审计
        audit = TricolorAudit.audit(action, args)
        if audit["level"] == "RED":
            # 对于敏感参数，脱敏后继续
            pass  # 不阻止，仅记录
        
        routed = {
            "navigate":  lambda: self.manager.navigate(args.get("url", "")),
            "snapshot":  lambda: self.manager.snapshot(),
            "click":     lambda: self.manager.click(args.get("selector", "")),
            "fill":      lambda: self.manager.fill(args.get("selector", ""), args.get("value", "")),
            "screenshot":lambda: self.manager.screenshot(args.get("path"), args.get("full_page", False)),
            "evaluate":  lambda: self.manager.evaluate(args.get("code", "")),
            "content":   lambda: self.manager.get_content(),
            "wait":      lambda: self.manager.wait(args.get("selector", ""), args.get("timeout")),
            "press_key": lambda: self.manager.press_key(args.get("key", "")),
            "status":    lambda: self.manager.get_status(),
            "start":     lambda: self.manager.start(),
            "reset":     lambda: self.manager.reset(),
            "shutdown":  lambda: self.manager.shutdown(),
        }
        
        handler = routed.get(action)
        if handler is None:
            return {"success": False, "error": f"未知操作: {action}"}
        
        result = handler()
        result["dna_action"] = action
        result["audit"] = audit["level"]
        if audit["reason"]:
            result["audit_reason"] = audit["reason"]
        return result
    
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/status":
            result = self._dispatch("status", {})
            self._send_json(result)
        elif path == "/health":
            self._send_json({"healthy": True, "port": PORT})
        else:
            self._send_json({"error": "仅支持 /status 和 /health GET 请求"}, 400)
    
    def do_POST(self):
        path = urlparse(self.path).path
        action = path.lstrip("/")
        try:
            args = self._read_body()
        except json.JSONDecodeError:
            self._send_json({"success": False, "error": "请求体 JSON 解析失败"}, 400)
            return
        
        result = self._dispatch(action, args)
        self._send_json(result)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


# ============================================================
# 启动
# ============================================================
def main():
    global HEADLESS, PORT
    import argparse
    parser = argparse.ArgumentParser(description="龍魂浏览器操作助手 · 守护进程")
    parser.add_argument("--headless", action="store_true", help="无头模式（不显示浏览器窗口）")
    parser.add_argument("--port", type=int, default=None, help="监听端口")
    parser.add_argument("--status", action="store_true", help="仅检查守护进程状态")
    parser.add_argument("--stop", action="store_true", help="停止守护进程")
    args = parser.parse_args()
    
    HEADLESS = args.headless
    PORT = args.port if args.port is not None else PORT
    
    # 仅查询状态
    if args.status:
        try:
            import urllib.request
            resp = urllib.request.urlopen(f"http://{HOST}:{PORT}/status", timeout=3)
            data = json.loads(resp.read())
            print(json.dumps(data, ensure_ascii=False, indent=2))
        except Exception:
            print(json.dumps({"running": False, "error": "守护进程未运行"}, ensure_ascii=False))
        return
    
    # 停止进程
    if args.stop:
        try:
            import urllib.request
            resp = urllib.request.urlopen(
                f"http://{HOST}:{PORT}/shutdown",
                data=b"{}", timeout=3
            )
            print("守护进程已停止")
        except Exception:
            print("守护进程未运行或已停止")
        return
    
    print(f"🐉 龍魂浏览器操作助手 v1.0")
    print(f"   监听: http://{HOST}:{PORT}")
    print(f"   模式: {'无头' if HEADLESS else '有头'}")
    print(f"   截图目录: {SCREENSHOT_DIR}")
    print(f"   日志文件: {LOG_FILE}")
    print(f"   按 Ctrl+C 停止")
    print()
    
    server = HTTPServer((HOST, PORT), BrowserAPIHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n正在关闭...")
        BrowserAPIHandler.manager.shutdown()
        server.server_close()
        print("守护进程已停止")


if __name__ == "__main__":
    main()
