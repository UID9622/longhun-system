#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·辛酉·未时·䷔噬嗑-BROWSER-DEVTOOLS-CTRL-v1.0
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 三色: 🟢 通过
"""
🐉 龍魂 · Mac浏览器开发者模式控制器 v1.0
================================================
浏览器主权控制：终端/CodeBuddy/Web面板 → 控制器 → Chrome(CDP·持久化)

功能:
  1. 参数调整  : User-Agent / 视口 / 地理位置 / 时区 / 语言
  2. 功能选择  : 开发者工具 / 网络限速 / JS / 缓存
  3. 安全防御  : 反指纹 / 隐私模式 / 自定义安全
  4. 实时监控  : CDP状态 / 页面列表 / 快照 / 日志
  5. 操作日志  : 史官记录 / 耻辱墙 / DNA追溯 / 三色审计
  6. HTTP服务  : --server 9766 供鲲鹏网关调用

浏览器引擎: 本机 Google Chrome + CDP（零三方依赖·标准库 urllib 即可控制）
  - playwright 可用时自动优先（增强）；不可用降级 Chrome CDP（本机已装 Chrome）

用法:
  lh browser-dev --start --devtools
  lh browser-dev --status
  lh browser-dev --user-agent "Mozilla/5.0 ..."
  lh browser-dev --viewport 1920 1080
  lh browser-dev --anti-fingerprint
  lh browser-dev --logs 20
  lh browser-dev --server 9766        # HTTP服务(供鲲鹏网关)

跨设备链路: 小艺/Kimi/CodeBuddy → 鲲鹏网关(:8768) → SSH反向隧道 → Mac(:9766)
DNA: #龍芯⚡️丙午·丙申·辛酉·未时·䷔噬嗑-BROWSER-DEVTOOLS-CTRL-v1.0-9622
"""

import os
import sys
import json
import time
import hashlib
import subprocess
import signal
import socket
import argparse
import logging
import shutil
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ============================================================
# 路径配置（实机校准·2026-08-15）
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
BROWSER_DIR = ROOT_DIR / "08_BIN" / "browser_profile"   # 浏览器用户数据(登录态持久化)
CONFIG_DIR = ROOT_DIR / "08_BIN" / "browser_configs"    # 配置存储
LOG_DIR = ROOT_DIR / "logs"                             # 实机: logs/ 存在 (方案写 12_LOGS 不存在)
STATE_DIR = ROOT_DIR / "08_STATE"                       # 状态/耻辱墙
AUDIT_DIR = ROOT_DIR / "04_AUDIT"                       # 史官

for _d in (BROWSER_DIR, CONFIG_DIR, LOG_DIR, STATE_DIR, AUDIT_DIR):
    _d.mkdir(parents=True, exist_ok=True)

SESSION_FILE = STATE_DIR / "browser_session.json"
CONFIG_FILE = CONFIG_DIR / "browser_config.json"
AUDIT_FILE = AUDIT_DIR / "browser_controller.jsonl"
SHAME_FILE = STATE_DIR / "shame_wall.jsonl"

# ============================================================
# 日志（敏感字段脱敏）
# ============================================================

def _mask(value: Any) -> Any:
    """敏感字段脱敏（cookie/password/token/secret 一律打码）"""
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            kl = str(k).lower()
            if any(w in kl for w in ("password", "passwd", "token", "secret", "cookie", "key")):
                out[k] = "***MELTDOWN***"
            else:
                out[k] = _mask(v)
        return out
    if isinstance(value, list):
        return [_mask(v) for v in value]
    return value

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"browser_ctrl_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("browser_controller")


# ============================================================
# DNA（v∞ 干支四柱 · 真实时间引擎）
# ============================================================

def _time_stamp_compact() -> str:
    """用 lh_time_engine 取真实干支四柱·卦（compact）；失败降级日期。"""
    try:
        sys.path.insert(0, str(ROOT_DIR / "bin"))
        from lh_time_engine import get_output_stamp  # noqa
        stamp = get_output_stamp(format_type="compact") or ""
        if "⚡️" in stamp:
            return stamp.split("⚡️", 1)[1].strip()
    except Exception:
        pass
    return datetime.now().strftime("%Y-%m-%d")


def generate_dna(suffix: str = "BROWSER") -> str:
    """v∞ 格式: #龍芯⚡️<干支四柱·卦>-BROWSER-<动作>-<哈希8>"""
    four_pillars = _time_stamp_compact()
    rand = hashlib.sha256(f"{suffix}{datetime.now().isoformat()}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{four_pillars}-BROWSER-{suffix}-{rand}"


# ============================================================
# 史官 / 耻辱墙 / 三色审计
# ============================================================

def write_historian(action: str, dna: str, details: Dict, tricolor: str = "🟢"):
    """写入史官（append-only·敏感字段脱敏）"""
    record = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "dna": dna,
        "tricolor": tricolor,
        "details": _mask(details)
    }
    with open(AUDIT_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_shame_wall(reason: str, details: Dict):
    """写入耻辱墙（🔴 级事件）"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "reason": reason,
        "details": _mask(details),
        "severity": "HIGH",
        "dna": generate_dna("SHAME")
    }
    with open(SHAME_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def tricolor_of(result: Dict) -> str:
    """三色审计：error→🔴 / warning→🟡 / success→🟢"""
    status = str(result.get("status", ""))
    if status == "error":
        return "🔴"
    if "warning" in status:
        return "🟡"
    return "🟢"


# ============================================================
# 浏览器引擎探测（Chrome CDP 零依赖 · playwright 可选增强）
# ============================================================

def find_chrome() -> Optional[str]:
    """找本机 Chrome 可执行文件"""
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    which = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    return which


def check_playwright() -> bool:
    try:
        import playwright  # noqa
        return True
    except ImportError:
        return False


# ============================================================
# 浏览器会话/配置数据
# ============================================================

@dataclass
class BrowserSession:
    pid: int
    port: int
    user_data_dir: str
    engine: str = "chrome-cdp"       # chrome-cdp | playwright
    status: str = "running"          # running | stopped | error
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    dna: str = field(default_factory=lambda: generate_dna("SESSION"))

    def to_dict(self) -> Dict:
        return {
            "pid": self.pid, "port": self.port, "user_data_dir": self.user_data_dir,
            "engine": self.engine, "status": self.status, "started_at": self.started_at,
            "dna": self.dna
        }

    @classmethod
    def from_dict(cls, d: Dict) -> "BrowserSession":
        return cls(
            pid=int(d.get("pid", 0)), port=int(d.get("port", 0)),
            user_data_dir=d.get("user_data_dir", ""), engine=d.get("engine", "chrome-cdp"),
            status=d.get("status", "stopped"), started_at=d.get("started_at", ""),
            dna=d.get("dna", "")
        )


@dataclass
class BrowserConfig:
    """浏览器开发者模式配置（实时保存·下次启动生效）"""
    user_agent: str = ""
    viewport_width: int = 1280
    viewport_height: int = 720
    timezone: str = "Asia/Shanghai"
    locale: str = "zh-CN"
    geolocation: Optional[Dict] = None
    devtools_enabled: bool = True
    headless: bool = False
    security: Dict = field(default_factory=dict)
    network: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        d = {
            "user_agent": self.user_agent,
            "viewport_width": self.viewport_width,
            "viewport_height": self.viewport_height,
            "timezone": self.timezone,
            "locale": self.locale,
            "geolocation": self.geolocation,
            "devtools_enabled": self.devtools_enabled,
            "headless": self.headless,
            "security": self.security,
            "network": self.network,
        }
        return d

    @classmethod
    def from_dict(cls, d: Dict) -> "BrowserConfig":
        c = cls()
        c.user_agent = d.get("user_agent", c.user_agent)
        c.viewport_width = int(d.get("viewport_width", c.viewport_width))
        c.viewport_height = int(d.get("viewport_height", c.viewport_height))
        c.timezone = d.get("timezone", c.timezone)
        c.locale = d.get("locale", c.locale)
        c.geolocation = d.get("geolocation", c.geolocation)
        c.devtools_enabled = bool(d.get("devtools_enabled", c.devtools_enabled))
        c.headless = bool(d.get("headless", c.headless))
        c.security = d.get("security", {}) or {}
        c.network = d.get("network", {}) or {}
        return c


# ============================================================
# CDP HTTP 客户端（零三方依赖）
# ============================================================

def cdp_get(port: int, path: str, timeout: int = 5) -> Optional[Any]:
    """CDP HTTP 端点 GET（/json/version /json/list）"""
    url = f"http://127.0.0.1:{port}{path}"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def cdp_new_tab(port: int, url: str = "about:blank", timeout: int = 5) -> Optional[Any]:
    """CDP HTTP 端点打开新页（PUT /json/new?url）"""
    target = f"http://127.0.0.1:{port}/json/new?{urllib.parse.quote(url, safe='')}"
    try:
        req = urllib.request.Request(target, method="PUT")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


# ============================================================
# 浏览器控制器核心
# ============================================================

class BrowserController:
    """浏览器开发者模式控制器"""

    def __init__(self):
        self.session: Optional[BrowserSession] = self._load_session()
        self.config = self._load_config()
        self.chrome_path = find_chrome()
        self.playwright_available = check_playwright()

    # ---------- 持久化 ----------

    def _load_session(self) -> Optional[BrowserSession]:
        if SESSION_FILE.exists():
            try:
                d = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
                return BrowserSession.from_dict(d)
            except Exception:
                pass
        return None

    def _save_session(self):
        if self.session:
            SESSION_FILE.write_text(
                json.dumps(self.session.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    def _clear_session(self):
        if SESSION_FILE.exists():
            SESSION_FILE.unlink()

    def _load_config(self) -> BrowserConfig:
        if CONFIG_FILE.exists():
            try:
                return BrowserConfig.from_dict(json.loads(CONFIG_FILE.read_text(encoding="utf-8")))
            except Exception:
                pass
        return BrowserConfig()

    def _save_config(self):
        CONFIG_FILE.write_text(
            json.dumps(self.config.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def _get_free_port() -> int:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
        sock.close()
        return port

    @staticmethod
    def _pid_alive(pid: int) -> bool:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

    # ---------- 启动参数构建（Chrome CDP） ----------

    def build_chrome_flags(self) -> List[str]:
        """按当前配置构建 Chrome 启动 flags"""
        flags = [
            f"--remote-debugging-port={self._session_port()}",
            f"--user-data-dir={BROWSER_DIR / 'user_data'}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-background-networking",
        ]
        cfg = self.config
        # 代理支持: 环境变量 LH_BROWSER_PROXY (如 socks5://127.0.0.1:1080)
        proxy = os.environ.get("LH_BROWSER_PROXY", "").strip()
        if proxy:
            flags.append(f"--proxy-server={proxy}")
        if cfg.user_agent:
            flags.append(f"--user-agent={cfg.user_agent}")
        if cfg.viewport_width and cfg.viewport_height:
            flags.append(f"--window-size={cfg.viewport_width},{cfg.viewport_height}")
        if cfg.timezone:
            flags.append(f"--timezone-id={cfg.timezone}")
        if cfg.locale:
            flags.append(f"--lang={cfg.locale}")
        sec = cfg.security
        if sec.get("js_enabled") is False:
            flags.append("--blink-settings=scriptEnabled=false")
        if sec.get("cache_enabled") is False:
            flags.append("--disk-cache-size=1")
        if sec.get("anti_fingerprint"):
            # 反指纹: 关自动化标记 / 关WebGL(去GL指纹)
            flags.append("--disable-blink-features=AutomationControlled")
            if sec.get("webgl_enabled") is False:
                flags.append("--disable-webgl")
        if sec.get("privacy_mode"):
            flags.append("--incognito")
        if cfg.devtools_enabled:
            flags.append("--auto-open-devtools-for-tabs")
        if cfg.headless:
            flags.append("--headless=new")
            flags.append("--disable-gpu")
        return flags

    def _session_port(self) -> int:
        # 启动前占位（会在 start 中写回真实端口）
        if self.session:
            return self.session.port
        return self._get_free_port()

    # ---------- 1. 启动 / 停止 ----------

    def start(self, headless: bool = False, devtools: bool = True, engine: str = "auto") -> Dict:
        """启动浏览器（优先 Chrome CDP 零依赖；playwright 可用时可选增强）"""
        dna = generate_dna("START")

        if self.session and self.session.status == "running" and self._pid_alive(self.session.pid):
            return {"status": "warning", "dna": dna, "message": "浏览器已在运行",
                    "pid": self.session.pid, "port": self.session.port}

        # 配置覆盖：本次 CLI 参数优先
        self.config.headless = headless if headless else self.config.headless
        self.config.devtools_enabled = devtools if devtools else self.config.devtools_enabled
        self._save_config()

        # 引擎选择
        use_playwright = engine == "playwright" or (engine == "auto" and self.playwright_available)
        if use_playwright:
            return self._start_playwright(dna, headless, devtools)

        if not self.chrome_path:
            msg = ("未找到 Chrome（CDP 引擎）。请安装 Google Chrome，或 `pip install playwright && "
                   "playwright install chromium` 后重试。")
            write_shame_wall("browser_start_failed", {"error": msg})
            return {"status": "error", "dna": dna, "message": msg}

        port = self._get_free_port()
        user_data = str(BROWSER_DIR / "user_data")

        # 启动命令：先把 port 注入 session 再构建 flags
        self.session = BrowserSession(pid=0, port=port, user_data_dir=user_data, engine="chrome-cdp")
        flags = self.build_chrome_flags()

        try:
            proc = subprocess.Popen(
                [self.chrome_path] + flags,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            self.session.pid = proc.pid
            self.session.dna = dna
            self.session.status = "running"
            self._save_session()

            # 等待 CDP 就绪（最多 8s）
            ready = False
            for _ in range(16):
                time.sleep(0.5)
                if cdp_get(port, "/json/version"):
                    ready = True
                    break

            write_historian("browser_start", dna, {
                "pid": proc.pid, "port": port, "engine": "chrome-cdp",
                "headless": self.config.headless, "devtools": self.config.devtools_enabled,
                "cdp_ready": ready
            })

            logger.info(f"✅ 浏览器已启动: PID={proc.pid}, Port={port}, CDP={'就绪' if ready else '连接中'}")
            return {
                "status": "success", "dna": dna, "pid": proc.pid, "port": port,
                "engine": "chrome-cdp", "cdp_ready": ready,
                "user_data_dir": user_data,
                "cdp_url": f"http://127.0.0.1:{port}"
            }

        except Exception as e:
            write_shame_wall("browser_start_failed", {"error": str(e)})
            return {"status": "error", "dna": dna, "message": str(e)}

    def _start_playwright(self, dna: str, headless: bool, devtools: bool) -> Dict:
        """playwright 引擎（增强路径·未装时提示）"""
        try:
            proc = subprocess.Popen(
                ["playwright", "open", "--user-data-dir", str(BROWSER_DIR / "user_data")],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            self.session = BrowserSession(
                pid=proc.pid, port=0, user_data_dir=str(BROWSER_DIR / "user_data"),
                engine="playwright")
            self._save_session()
            write_historian("browser_start", dna, {"pid": proc.pid, "engine": "playwright"})
            return {"status": "success", "dna": dna, "pid": proc.pid, "engine": "playwright"}
        except Exception as e:
            return {"status": "error", "dna": dna, "message": f"playwright 启动失败: {e}"}

    def stop(self) -> Dict:
        """停止浏览器（SIGTERM→SIGKILL）"""
        dna = generate_dna("STOP")
        if not self.session or not self._pid_alive(self.session.pid):
            self.session = None
            self._clear_session()
            return {"status": "warning", "dna": dna, "message": "浏览器未运行"}

        pid = self.session.pid
        try:
            os.kill(pid, signal.SIGTERM)
            time.sleep(1.5)
            if self._pid_alive(pid):
                os.kill(pid, signal.SIGKILL)
            # 连坐：结束该进程组（Chrome 会 fork 子进程）
            try:
                os.killpg(os.getpgid(pid), signal.SIGKILL)
            except Exception:
                pass
            write_historian("browser_stop", dna, {"pid": pid, "port": self.session.port})
            logger.info(f"✅ 浏览器已停止: PID={pid}")
            self.session = None
            self._clear_session()
            return {"status": "success", "dna": dna, "pid": pid}
        except Exception as e:
            write_shame_wall("browser_stop_failed", {"error": str(e), "pid": pid})
            return {"status": "error", "dna": dna, "message": str(e)}

    def kill(self) -> Dict:
        """强制终止（SIGKILL·进程组连坐）"""
        if not self.session:
            return {"status": "warning", "message": "浏览器未运行"}
        pid = self.session.pid
        try:
            try:
                os.killpg(os.getpgid(pid), signal.SIGKILL)
            except Exception:
                os.kill(pid, signal.SIGKILL)
            write_historian("browser_kill", generate_dna("KILL"), {"pid": pid})
            logger.info(f"💀 浏览器已强制终止: PID={pid}")
            self.session = None
            self._clear_session()
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def status(self) -> Dict:
        """获取浏览器状态（进程存活 + CDP 探活 + 页面列表）"""
        if not self.session:
            return {"status": "not_running", "message": "浏览器未启动"}

        alive = self._pid_alive(self.session.pid)
        if not alive:
            self.session.status = "stopped"
            return {
                "status": "stopped", "pid": self.session.pid, "port": self.session.port,
                "started_at": self.session.started_at, "dna": self.session.dna,
                "message": "进程已退出"
            }

        cdp = cdp_get(self.session.port, "/json/version")
        pages = cdp_get(self.session.port, "/json/list") if cdp else None
        page_titles = []
        if isinstance(pages, list):
            page_titles = [p.get("title", "")[:40] for p in pages[:10]]

        return {
            "status": "running", "pid": self.session.pid, "port": self.session.port,
            "engine": self.session.engine, "user_data_dir": self.session.user_data_dir,
            "started_at": self.session.started_at, "dna": self.session.dna,
            "cdp_ready": bool(cdp),
            "browser_version": (cdp or {}).get("Browser", ""),
            "pages": page_titles
        }

    # ---------- 2. 参数调整 ----------

    def set_user_agent(self, user_agent: str) -> Dict:
        dna = generate_dna("SET-UA")
        self.config.user_agent = user_agent
        self._save_config()
        write_historian("set_user_agent", dna, {"user_agent": user_agent})
        return {"status": "success", "dna": dna, "user_agent": user_agent,
                "note": "下次启动生效（运行时需 CDP 注入）"}

    def set_viewport(self, width: int, height: int) -> Dict:
        dna = generate_dna("SET-VIEWPORT")
        self.config.viewport_width = width
        self.config.viewport_height = height
        self._save_config()
        write_historian("set_viewport", dna, {"width": width, "height": height})
        return {"status": "success", "dna": dna, "viewport": {"width": width, "height": height}}

    def set_geolocation(self, latitude: float, longitude: float) -> Dict:
        dna = generate_dna("SET-GEO")
        self.config.geolocation = {"latitude": latitude, "longitude": longitude}
        self._save_config()
        write_historian("set_geolocation", dna, {"latitude": latitude, "longitude": longitude})
        return {"status": "success", "dna": dna, "geolocation": self.config.geolocation}

    def set_timezone(self, timezone: str) -> Dict:
        dna = generate_dna("SET-TZ")
        self.config.timezone = timezone
        self._save_config()
        write_historian("set_timezone", dna, {"timezone": timezone})
        return {"status": "success", "dna": dna, "timezone": timezone}

    # ---------- 3. 功能选择 ----------

    def set_devtools(self, enabled: bool) -> Dict:
        dna = generate_dna("SET-DEVTOOLS")
        self.config.devtools_enabled = enabled
        self._save_config()
        write_historian("set_devtools", dna, {"enabled": enabled})
        return {"status": "success", "dna": dna, "devtools_enabled": enabled}

    def set_network_throttling(self, download: int, upload: int, latency: int) -> Dict:
        dna = generate_dna("SET-NETWORK")
        self.config.network = {"download": download, "upload": upload, "latency": latency}
        self._save_config()
        write_historian("set_network", dna, self.config.network)
        return {"status": "success", "dna": dna, "network": self.config.network}

    def set_js_enabled(self, enabled: bool) -> Dict:
        dna = generate_dna("SET-JS")
        self.config.security["js_enabled"] = enabled
        self._save_config()
        write_historian("set_js", dna, {"enabled": enabled})
        return {"status": "success", "dna": dna, "js_enabled": enabled}

    def set_cache_enabled(self, enabled: bool) -> Dict:
        dna = generate_dna("SET-CACHE")
        self.config.security["cache_enabled"] = enabled
        self._save_config()
        write_historian("set_cache", dna, {"enabled": enabled})
        return {"status": "success", "dna": dna, "cache_enabled": enabled}

    # ---------- 4. 安全防御 ----------

    def enable_anti_fingerprint(self) -> Dict:
        dna = generate_dna("ENABLE-ANTI-FP")
        self.config.security["anti_fingerprint"] = True
        self.config.security["webgl_enabled"] = False
        self.config.security["canvas_fingerprint"] = False
        self._save_config()
        write_historian("enable_anti_fingerprint", dna, {"enabled": True})
        return {"status": "success", "dna": dna, "anti_fingerprint": True}

    def enable_privacy_mode(self) -> Dict:
        dna = generate_dna("ENABLE-PRIVACY")
        self.config.security["privacy_mode"] = True
        self.config.security["block_cookies"] = True
        self.config.security["block_trackers"] = True
        self._save_config()
        write_historian("enable_privacy", dna, {"enabled": True})
        return {"status": "success", "dna": dna, "privacy_mode": True}

    def set_custom_security(self, security_config: Dict) -> Dict:
        dna = generate_dna("SET-SECURITY")
        self.config.security.update(security_config)
        self._save_config()
        write_historian("set_security", dna, security_config)
        return {"status": "success", "dna": dna, "security": self.config.security}

    # ---------- 5. 监控 / 日志 / 快照 ----------

    def get_config(self) -> Dict:
        return self.config.to_dict()

    def get_logs(self, limit: int = 50) -> List[Dict]:
        if not AUDIT_FILE.exists():
            return []
        logs = []
        with open(AUDIT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except Exception:
                    continue
        return logs[-limit:]

    def snapshot(self) -> Dict:
        """页面快照（CDP 页面列表 + 新开页可选）"""
        if not self.session or not self._pid_alive(self.session.pid):
            return {"status": "error", "message": "浏览器未运行"}
        pages = cdp_get(self.session.port, "/json/list")
        if not isinstance(pages, list):
            return {"status": "error", "message": "CDP 未就绪"}
        return {
            "status": "success",
            "dna": generate_dna("SNAPSHOT"),
            "page_count": len(pages),
            "pages": [
                {"id": p.get("id", "")[:12], "title": p.get("title", "")[:60],
                 "url": p.get("url", "")[:100]}
                for p in pages[:10]
            ]
        }

    def open_url(self, url: str) -> Dict:
        """打开 URL（CDP 新页）"""
        if not self.session or not self._pid_alive(self.session.pid):
            return {"status": "error", "message": "浏览器未运行"}
        if not url.startswith(("http://", "https://", "about:")):
            url = "https://" + url
        tab = cdp_new_tab(self.session.port, url)
        dna = generate_dna("OPEN-URL")
        write_historian("open_url", dna, {"url": url})
        if tab and "id" in tab:
            return {"status": "success", "dna": dna, "url": url, "tab": tab.get("id", "")[:12]}
        return {"status": "error", "dna": dna, "message": "打开失败，CDP 可能未就绪"}

    def clear_config(self) -> Dict:
        dna = generate_dna("CLEAR-CONFIG")
        self.config = BrowserConfig()
        self._save_config()
        write_historian("clear_config", dna, {})
        return {"status": "success", "dna": dna}


# ============================================================
# HTTP 服务模式（供鲲鹏网关调用 · fastapi/uvicorn 已装）
# ============================================================

def run_http_server(port: int = 9766):
    """启动 HTTP 服务 :9766，供鲲鹏网关 (lh_browser_gateway.py) 调用"""
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        import uvicorn
    except ImportError:
        print(json.dumps({"status": "error",
                          "message": "fastapi/uvicorn 未安装: pip install fastapi uvicorn"},
                         ensure_ascii=False, indent=2))
        return

    http_app = FastAPI(title="龍魂浏览器控制器 (Mac端)", version="1.0.0",
                       dna="#龍芯⚡️丙午·丙申·辛酉·未时·䷔噬嗑-BROWSER-DEVTOOLS-CTRL-v1.0-9622")
    http_app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    ctrl = BrowserController()

    @http_app.get("/")
    def root():
        return {"service": "🐉 龍魂浏览器控制器 (Mac端)", "status": "🟢 运行中",
                "dna": generate_dna("HTTP-ROOT"), "confirm": CONFIRM}

    @http_app.post("/start")
    def start(params: Dict = None):
        params = params or {}
        return ctrl.start(headless=params.get("headless", False),
                          devtools=params.get("devtools", True))

    @http_app.post("/stop")
    def stop():
        return ctrl.stop()

    @http_app.get("/status")
    def status():
        return ctrl.status()

    @http_app.post("/kill")
    def kill():
        return ctrl.kill()

    @http_app.post("/set_user_agent")
    def set_user_agent(params: Dict = None):
        params = params or {}
        return ctrl.set_user_agent(params.get("user_agent", ""))

    @http_app.post("/set_viewport")
    def set_viewport(params: Dict = None):
        params = params or {}
        return ctrl.set_viewport(params.get("width", 1280), params.get("height", 720))

    @http_app.post("/set_geolocation")
    def set_geolocation(params: Dict = None):
        params = params or {}
        return ctrl.set_geolocation(params.get("latitude", 31.23), params.get("longitude", 121.47))

    @http_app.post("/set_timezone")
    def set_timezone(params: Dict = None):
        params = params or {}
        return ctrl.set_timezone(params.get("timezone", "Asia/Shanghai"))

    @http_app.post("/set_devtools")
    def set_devtools(params: Dict = None):
        params = params or {}
        return ctrl.set_devtools(params.get("enabled", True))

    @http_app.post("/set_js")
    def set_js(params: Dict = None):
        params = params or {}
        return ctrl.set_js_enabled(params.get("enabled", True))

    @http_app.post("/set_cache")
    def set_cache(params: Dict = None):
        params = params or {}
        return ctrl.set_cache_enabled(params.get("enabled", True))

    @http_app.post("/enable_anti_fingerprint")
    def enable_anti_fingerprint():
        return ctrl.enable_anti_fingerprint()

    @http_app.post("/enable_privacy_mode")
    def enable_privacy_mode():
        return ctrl.enable_privacy_mode()

    @http_app.get("/config")
    def get_config():
        return ctrl.get_config()

    @http_app.get("/logs")
    def get_logs(limit: int = 50):
        return {"logs": ctrl.get_logs(limit)}

    @http_app.get("/snapshot")
    def snapshot():
        return ctrl.snapshot()

    @http_app.post("/open_url")
    def open_url(params: Dict = None):
        params = params or {}
        return ctrl.open_url(params.get("url", ""))

    @http_app.post("/clear")
    def clear_config():
        return ctrl.clear_config()

    @http_app.get("/health")
    def health():
        return {"status": "healthy", "service": "browser_controller",
                "chrome": bool(ctrl.chrome_path), "playwright": ctrl.playwright_available}

    print(f"🚀 Mac浏览器控制器HTTP服务: http://0.0.0.0:{port}")
    uvicorn.run(http_app, host="0.0.0.0", port=port)


# ============================================================
# 命令行接口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · Mac浏览器开发者模式控制器 v1.0（Chrome CDP 零依赖）",
        epilog="示例: lh browser-dev --start --devtools | lh browser-dev --anti-fingerprint")

    parser.add_argument("--start", action="store_true", help="启动浏览器")
    parser.add_argument("--stop", action="store_true", help="停止浏览器")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--kill", action="store_true", help="强制终止")
    parser.add_argument("--snapshot", action="store_true", help="页面快照")
    parser.add_argument("--open", type=str, help="打开URL")
    parser.add_argument("--devtools", action="store_true", help="开启开发者工具")
    parser.add_argument("--headless", action="store_true", help="无头模式")
    parser.add_argument("--engine", type=str, default="auto",
                        choices=["auto", "chrome", "playwright"], help="浏览器引擎")

    parser.add_argument("--user-agent", type=str, help="设置User-Agent")
    parser.add_argument("--viewport", nargs=2, type=int, metavar=("WIDTH", "HEIGHT"), help="设置视口大小")
    parser.add_argument("--geolocation", nargs=2, type=float, metavar=("LAT", "LNG"), help="设置地理位置")
    parser.add_argument("--timezone", type=str, help="设置时区")

    parser.add_argument("--js", type=lambda x: x.lower() == "true", help="启用/禁用JavaScript")
    parser.add_argument("--cache", type=lambda x: x.lower() == "true", help="启用/禁用缓存")
    parser.add_argument("--network", nargs=3, type=int, metavar=("DOWNLOAD", "UPLOAD", "LATENCY"), help="网络限速")

    parser.add_argument("--anti-fingerprint", action="store_true", help="启用反指纹")
    parser.add_argument("--privacy", action="store_true", help="启用隐私模式")
    parser.add_argument("--security", type=str, help="自定义安全配置 (JSON)")

    parser.add_argument("--config", action="store_true", help="查看当前配置")
    parser.add_argument("--logs", type=int, default=0, help="查看操作日志(条数)")
    parser.add_argument("--clear", action="store_true", help="重置配置")
    parser.add_argument("--server", type=int, metavar="PORT", help="启动HTTP服务(默认9766)")
    parser.add_argument("--json", action="store_true", help="JSON输出(抑制日志头)")

    args = parser.parse_args()
    controller = BrowserController()

    def out(result: Dict):
        print(json.dumps(result, indent=2, ensure_ascii=False))

    # 无实质操作（仅 --json/--headless/--devtools 等辅助flag）→ 默认看状态
    meaningful = any([
        args.start, args.stop, args.status, args.kill, args.snapshot, args.open,
        args.user_agent, args.viewport, args.geolocation, args.timezone,
        args.js is not None, args.cache is not None, args.network,
        args.anti_fingerprint, args.privacy, args.security,
        args.config, args.logs > 0, args.clear, args.server,
    ])
    if not meaningful:
        out(controller.status())
        return

    # HTTP 服务模式
    if args.server:
        run_http_server(args.server if args.server else 9766)
        return

    if args.start:
        out(controller.start(headless=args.headless, devtools=args.devtools, engine=args.engine)); return
    if args.stop:
        out(controller.stop()); return
    if args.kill:
        out(controller.kill()); return
    if args.status:
        out(controller.status()); return
    if args.snapshot:
        out(controller.snapshot()); return
    if args.open:
        out(controller.open_url(args.open)); return

    if args.user_agent:
        out(controller.set_user_agent(args.user_agent)); return
    if args.viewport:
        out(controller.set_viewport(args.viewport[0], args.viewport[1])); return
    if args.geolocation:
        out(controller.set_geolocation(args.geolocation[0], args.geolocation[1])); return
    if args.timezone:
        out(controller.set_timezone(args.timezone)); return

    if args.js is not None:
        out(controller.set_js_enabled(args.js)); return
    if args.cache is not None:
        out(controller.set_cache_enabled(args.cache)); return
    if args.network:
        out(controller.set_network_throttling(args.network[0], args.network[1], args.network[2])); return

    if args.anti_fingerprint:
        out(controller.enable_anti_fingerprint()); return
    if args.privacy:
        out(controller.enable_privacy_mode()); return
    if args.security:
        try:
            out(controller.set_custom_security(json.loads(args.security)))
        except json.JSONDecodeError:
            out({"status": "error", "message": "无效的JSON格式"})
        return

    if args.config:
        out(controller.get_config()); return
    if args.logs > 0:
        out(controller.get_logs(args.logs)); return
    if args.clear:
        out(controller.clear_config()); return

    parser.print_help()


if __name__ == "__main__":
    main()
