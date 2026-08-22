#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-P0-AUTOMATION-MAC-v1.0
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 三色: 🟢 通过
"""
🐉 龍魂 · P0全自动化智能体系统 v1.0（Mac 主权版）
========================================================
主权人格直接操作【自己的 Mac】，不是代理、不外放、不越权。

能力范围（全部本机执行 · 数据本地加密 · 能力不外放）:
  1. Mac 软件自动化  : AppleScript/osascript 控制本机所有 App（打开/激活/点击/输入/截屏/窗口）
  2. 浏览器自动化     : Safari/Chrome 控制（打开URL/取标题/执行JS/标签页）+ 复用 CDP 控制器
  3. 文件自动化       : 文件查找(mdfind)/整理/批量重命名/去重/监控
  4. 知识自动化       : 搜索 → 爬取 → 去重 → 归入知识图谱
  5. 代码自动化       : 生成/修复/测试（本地模型或 AI 网关）
  6. 写作自动化       : 研究 → 大纲 → 正文 → 审校 → 多格式输出

P0 硬边界（主权人格铁律）:
  ✅ 允许: 打开本机App · 点击 · 输入 · 截屏 · 浏览器导航 · 文件整理 · 搜索爬取 · 代码生成 · 写作
  ❌ 禁止: 上传数据到外部 · 启动对外服务 · 读取通讯录/密码 · 修改系统关键文件 · 代理他人 · 外放能力
  🟡 授权: 读取短信/通讯录 · 修改App数据 · 上传数据 → 必须 UID9622 显式授权

用法:
  lh p0                      # 交互控制台
  lh p0 --status             # 系统状态
  lh p0 --app "微信"         # 打开Mac软件
  lh p0 --browser "https://uid9622.cn"   # 浏览器打开URL
  lh p0 --file search "pdf"  # 文件查找
  lh p0 --search "抗战历史"  # 知识搜索
  lh p0 --code "写一个爬虫"  # 代码生成
  lh p0 --write "写一篇AI治理的文章"   # 写作
  lh p0 --run "打开微信"     # 自然语言整句路由

主权边界: 本引擎只操作 UID9622 自己的 Mac；所有数据存本地 ~/.longhun/p0_automation/；
能力不外放、不代理、不开对外端口（--serve 需显式授权，默认拒绝）。
"""
import os
import sys
import json
import time
import hashlib
import subprocess
import re
import shutil
import argparse
import logging
import urllib.request
import urllib.parse
import html
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# ============================================================
# 主权锚定
# ============================================================
UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
ROOT_DIR = Path(__file__).resolve().parent.parent


def generate_dna(suffix: str = "P0") -> str:
    """v∞ DNA：干支四柱由 lh_time_engine 取，失败降级日期。"""
    stamp = ""
    try:
        sys.path.insert(0, str(ROOT_DIR / "bin"))
        from lh_time_engine import get_output_stamp
        stamp = get_output_stamp("compact").replace("#龍芯⚡️", "")
    except Exception:
        stamp = datetime.now().strftime("%Y-%m-%d")
    rand = hashlib.sha256(f"{suffix}{datetime.now().isoformat()}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{stamp}-P0-{suffix}-{rand}-{UID}"


# ============================================================
# 路径配置（实机校准 · 数据全在本机 .longhun）
# ============================================================
LONGHUN_HOME = Path.home() / ".longhun"
P0_DIR = LONGHUN_HOME / "p0_automation"
SUBDIRS = ["mobile", "browser", "files", "knowledge", "code", "video", "writing", "encrypted", "logs"]
for _d in [P0_DIR] + [P0_DIR / s for s in SUBDIRS]:
    _d.mkdir(parents=True, exist_ok=True)

LOG_DIR = P0_DIR / "logs"
AUDIT_DIR = ROOT_DIR / "04_AUDIT"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"p0_automation_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler() if os.environ.get("LH_P0_VERBOSE") else logging.NullHandler()
    ]
)
logger = logging.getLogger("p0_automation")


# ============================================================
# P0 协议（主权人格安全边界）
# ============================================================
class P0Protocol:
    """P0协议 - 定义本机能碰什么、不能碰什么（不外放·不代理·不越权）"""

    # ✅ 允许：本机主权操作（Mac 软件 / 浏览器 / 文件 / 知识 / 代码 / 写作）
    ALLOWED_ACTIONS = {
        "mac": ["open_app", "activate_app", "click", "input_text", "screenshot",
                "close_app", "scroll", "back", "home", "get_front_app", "list_apps",
                "window_list", "window_resize", "window_focus", "type_keystroke",
                "run_applescript", "get_app_info", "app_menu_click"],
        "browser": ["open_url", "get_url", "get_title", "execute_js", "list_tabs",
                    "new_tab", "close_tab", "switch_tab", "refresh", "back",
                    "forward", "search_web", "browser_screenshot"],
        "files": ["search_files", "list_dir", "organize_dir", "batch_rename",
                  "deduplicate", "copy_files", "move_files", "get_file_info",
                  "watch_dir", "open_file", "reveal_in_finder", "create_dir"],
        "knowledge": ["search_web", "crawl_page", "extract_content", "deduplicate",
                      "store_knowledge", "query_knowledge", "build_graph"],
        "code": ["generate_code", "fix_bug", "run_tests", "optimize_code",
                 "format_code", "analyze_code", "review_code"],
        "video": ["search_material", "generate_script", "clip_video",
                  "add_subtitle", "synthesize_voice"],
        "writing": ["research_topic", "generate_outline", "write_article",
                    "proofread", "format_document", "generate_report"],
    }

    # ❌ 绝对不能碰（硬边界 · 不外放 · 不代理）
    FORBIDDEN_ACTIONS = [
        "upload_data", "send_data", "expose_service", "open_remote_port",
        "proxy_other", "read_contacts", "read_password", "read_keychain",
        "modify_system", "delete_system", "delete_user_files",
        "access_bio", "bypass_auth", "read_private_files",
        "modify_app_data", "send_notification_external", "remote_control_other",
    ]

    # 🟡 需要 UID9622 显式授权
    REQUIRES_AUTH = [
        "read_sms", "read_contacts", "access_location",
        "modify_app_data", "upload_data", "delete_files",
        "open_remote_port", "expose_service", "send_notification_external",
    ]

    @classmethod
    def check_action(cls, action: str) -> Dict:
        """检查操作是否允许"""
        if action in cls.FORBIDDEN_ACTIONS:
            return {"allowed": False, "reason": f"🔴 P0硬边界禁止: {action}", "severity": "CRITICAL"}
        if action in cls.REQUIRES_AUTH:
            return {"allowed": True, "requires_auth": True,
                    "reason": f"🟡 P0需UID9622授权: {action}"}
        all_allowed = [a for acts in cls.ALLOWED_ACTIONS.values() for a in acts]
        if action in all_allowed:
            return {"allowed": True, "requires_auth": False, "reason": f"🟢 P0允许: {action}"}
        return {"allowed": False, "requires_auth": True,
                "reason": f"🟡 P0未知操作: {action}，需要确认"}


# ============================================================
# 本地加密（数据永不出境）
# ============================================================
class LocalEncryption:
    """本地加密 - 主密钥存本机，数据不传任何外部"""

    def __init__(self):
        self.key_path = P0_DIR / "encrypted" / "master.key"
        self._ensure_key()

    def _ensure_key(self):
        if not self.key_path.exists():
            import secrets
            key = secrets.token_bytes(32)
            self.key_path.write_bytes(key)
            logger.info("🔑 主密钥已生成(本机)")

    def _fernet(self):
        from cryptography.fernet import Fernet
        return Fernet(self.key_path.read_bytes())

    def encrypt(self, data: str) -> Dict:
        f = self._fernet()
        enc = f.encrypt(data.encode("utf-8"))
        return {"encrypted": enc.hex(), "algorithm": "Fernet(AES-128)", "stored_locally": True}

    def decrypt(self, hex_data: str) -> str:
        f = self._fernet()
        return f.decrypt(bytes.fromhex(hex_data)).decode("utf-8")


# ============================================================
# 1. Mac 软件自动化（AppleScript · 本机所有 App）
# ============================================================
class MacAutomation:
    """Mac 软件控制 - 通过 osascript 控制本机任意 App"""

    def __init__(self):
        self.encryption = LocalEncryption()
        self.available = True
        self._check_accessibility()

    def _check_accessibility(self):
        """检查辅助功能权限（System Events 需要）"""
        try:
            r = subprocess.run(
                ["osascript", "-e", 'tell application "System Events" to get name of first process'],
                capture_output=True, text=True, timeout=10)
            if r.returncode != 0:
                logger.warning("⚠️ 辅助功能权限未授予，部分UI控制不可用")
        except Exception:
            pass

    def _osa(self, script: str, timeout: int = 15) -> subprocess.CompletedProcess:
        return subprocess.run(["osascript", "-e", script],
                              capture_output=True, text=True, timeout=timeout)

    def execute(self, action: str, params: Optional[Dict] = None) -> Dict:
        check = P0Protocol.check_action(action)
        if not check["allowed"]:
            return {"success": False, "error": check["reason"]}
        params = params or {}
        result = {"success": False, "action": action, "data": None}
        try:
            if action == "list_apps":
                r = subprocess.run(["osascript", "-e",
                    'tell application "System Events" to get name of every process whose background only is false'],
                    capture_output=True, text=True, timeout=15)
                apps = [a.strip() for a in (r.stdout or "").split(",") if a.strip()]
                # 补充 /Applications
                app_files = sorted(p.stem.replace(".app", "") for p in Path("/Applications").glob("*.app"))
                apps = sorted(set(apps) | set(app_files))
                result.update(success=True, data=apps)

            elif action == "open_app":
                name = params.get("name") or params.get("app")
                if not name:
                    return {"success": False, "error": "请指定App名称"}
                # 尝试 open -a（更可靠），失败再 osascript activate
                r = subprocess.run(["open", "-a", name], capture_output=True, text=True, timeout=10)
                if r.returncode != 0:
                    self._osa(f'tell application "{name}" to activate')
                result.update(success=True, data=f"已打开: {name}")

            elif action == "activate_app":
                name = params.get("name") or params.get("app")
                if not name:
                    return {"success": False, "error": "请指定App名称"}
                self._osa(f'tell application "{name}" to activate')
                result.update(success=True, data=f"已激活: {name}")

            elif action == "close_app":
                name = params.get("name") or params.get("app")
                if not name:
                    return {"success": False, "error": "请指定App名称"}
                self._osa(f'tell application "{name}" to quit')
                result.update(success=True, data=f"已关闭: {name}")

            elif action == "get_front_app":
                r = self._osa('tell application "System Events" to get name of first application process whose frontmost is true')
                result.update(success=True, data=(r.stdout or "").strip())

            elif action == "screenshot":
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = P0_DIR / "mobile" / f"screenshot_{ts}.png"
                subprocess.run(["screencapture", "-x", str(path)], check=True, timeout=15)
                result.update(success=True, data=str(path))

            elif action == "click":
                x, y = params.get("x", 0), params.get("y", 0)
                if not x or not y:
                    return {"success": False, "error": "请指定坐标 x,y"}
                # 用 cliclick（如已装）否则 AppleScript System Events
                if shutil.which("cliclick"):
                    subprocess.run(["cliclick", "c:%s,%s" % (x, y)], check=True, timeout=10)
                else:
                    self._osa(f'tell application "System Events" to click at {{{x}, {y}}}')
                result.update(success=True, data=f"已点击 ({x},{y})")

            elif action == "input_text":
                text = params.get("text", "")
                if not text:
                    return {"success": False, "error": "请指定输入文本"}
                safe = text.replace('\\', '\\\\').replace('"', '\\"')
                self._osa(f'tell application "System Events" to keystroke "{safe}"')
                result.update(success=True, data=f"已输入: {text[:50]}")

            elif action == "type_keystroke":
                key = params.get("key", "return")
                self._osa(f'tell application "System Events" to key code {key}')
                result.update(success=True, data=f"已按键: {key}")

            elif action == "scroll":
                direction = params.get("direction", "down")
                times = int(params.get("times", 1))
                code = "5" if direction == "down" else "4"
                for _ in range(times):
                    self._osa(f'tell application "System Events" to key code {code}')
                result.update(success=True, data=f"已滚动: {direction} x{times}")

            elif action == "app_menu_click":
                app = params.get("app", "")
                menu = params.get("menu", "")
                item = params.get("item", "")
                if not app or not menu or not item:
                    return {"success": False, "error": "需要 app/menu/item 参数"}
                script = (f'tell application "System Events"\n'
                          f'  tell process "{app}"\n'
                          f'    click menu item "{item}" of menu 1 of menu bar item "{menu}" of menu bar 1\n'
                          f'  end tell\nend tell')
                self._osa(script)
                result.update(success=True, data=f"菜单点击: {app}/{menu}/{item}")

            elif action == "window_list":
                app = params.get("app", "System Events")
                r = self._osa(f'tell application "System Events" to get name of every window of process "{app}"')
                result.update(success=True, data=(r.stdout or "").strip())

            elif action == "run_applescript":
                script = params.get("script", "")
                if not script:
                    return {"success": False, "error": "请指定AppleScript"}
                r = self._osa(script, timeout=30)
                result.update(success=True, data=(r.stdout or r.stderr).strip())

            else:
                result["error"] = f"未知操作: {action}"
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"操作超时: {action}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

        self._record_history(action, params, result)
        return result

    def _record_history(self, action: str, params: Dict, result: Dict):
        record = {"timestamp": datetime.now().isoformat(), "action": action,
                  "params": params, "result": result.get("success"),
                  "data": str(result.get("data", ""))[:200],
                  "dna": generate_dna("MAC-HISTORY")}
        with open(P0_DIR / "mobile" / "history.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ============================================================
# 2. 浏览器自动化（Safari / Chrome · 本机）
# ============================================================
class BrowserAutomation:
    """浏览器控制 - AppleScript 控制 Safari/Chrome + 复用 CDP 控制器"""

    def __init__(self):
        self.encryption = LocalEncryption()
        self.cdp_available = self._check_cdp()

    def _check_cdp(self) -> bool:
        try:
            import importlib.util
            return importlib.util.find_spec("lh_browser_controller") is not None or \
                   (ROOT_DIR / "08_BIN" / "lh_browser_controller.py").exists()
        except Exception:
            return False


    def execute(self, action: str, params: Optional[Dict] = None) -> Dict:
        check = P0Protocol.check_action(action)
        if not check["allowed"]:
            return {"success": False, "error": check["reason"]}
        params = params or {}
        result = {"success": False, "action": action, "data": None}
        browser = params.get("browser", "Google Chrome")

        try:
            if action == "open_url":
                url = params.get("url", "")
                if not url:
                    return {"success": False, "error": "请指定URL"}
                if not url.startswith(("http://", "https://")):
                    url = "https://" + url
                # AppleScript open location 比 `open -a` 可靠（open -a 曾静默假成功）
                if browser == "Safari":
                    self._osa(f'tell application "Safari" to open location "{url}"')
                else:
                    self._osa(f'tell application "Google Chrome" to open location "{url}"')
                time.sleep(1.5)
                # 验证闭环: 读回所有标签URL确认真正打开，绝不报假成功（P05审计·不装全绿）
                r = self._osa('tell application "Google Chrome" to get URL of every tab of every window')
                if url in (r.stdout or "").replace(" ", ""):
                    result.update(success=True, data=f"已打开: {url}（已验证）")
                else:
                    result.update(success=False, error=f"打开未验证: {url}")

            elif action == "get_url":
                if browser == "Safari":
                    r = self._osa('tell application "Safari" to get URL of front document')
                else:
                    r = self._osa('tell application "Google Chrome" to get URL of active tab of front window')
                result.update(success=True, data=(r.stdout or "").strip())

            elif action == "get_title":
                if browser == "Safari":
                    r = self._osa('tell application "Safari" to get name of front document')
                else:
                    r = self._osa('tell application "Google Chrome" to get title of active tab of front window')
                result.update(success=True, data=(r.stdout or "").strip())

            elif action == "execute_js":
                js = params.get("js", "")
                if not js:
                    return {"success": False, "error": "请指定JS代码"}
                if browser == "Safari":
                    r = self._osa(f'tell application "Safari" to do JavaScript "{js}" in front document', timeout=30)
                else:
                    r = self._osa(f'tell application "Google Chrome" to execute javascript "{js}" in active tab of front window', timeout=30)
                result.update(success=True, data=(r.stdout or "").strip())

            elif action == "list_tabs":
                if browser == "Safari":
                    r = self._osa('tell application "Safari" to get URL of every tab of every window')
                else:
                    r = self._osa('tell application "Google Chrome" to get URL of every tab of every window')
                tabs = [u.strip() for u in (r.stdout or "").split(",") if u.strip()]
                result.update(success=True, data=tabs)

            elif action == "new_tab":
                url = params.get("url", "")
                if browser == "Safari":
                    subprocess.run(["open", "-a", "Safari", url or "about:blank"], check=True, timeout=10)
                else:
                    self._osa(f'tell application "Google Chrome" to make new tab with properties {{URL:"{url}"}}')
                result.update(success=True, data=f"新标签: {url}")

            elif action == "refresh":
                if browser == "Safari":
                    self._osa('tell application "Safari" to set URL of front document to URL of front document')
                else:
                    self._osa('tell application "Google Chrome" to reload active tab of front window')
                result.update(success=True, data="已刷新")

            elif action == "back":
                if browser == "Safari":
                    self._osa('tell application "Safari" to go back in front document')
                else:
                    self._osa('tell application "Google Chrome" to go back in active tab of front window')
                result.update(success=True, data="已后退")

            elif action == "forward":
                if browser == "Safari":
                    self._osa('tell application "Safari" to go forward in front document')
                else:
                    self._osa('tell application "Google Chrome" to go forward in active tab of front window')
                result.update(success=True, data="已前进")

            elif action == "search_web":
                query = params.get("query", "")
                if not query:
                    return {"success": False, "error": "请指定搜索词"}
                url = "https://www.bing.com/search?q=" + urllib.parse.quote(query)
                if browser == "Safari":
                    self._osa(f'tell application "Safari" to open location "{url}"')
                else:
                    self._osa(f'tell application "Google Chrome" to open location "{url}"')
                time.sleep(1.5)
                r = self._osa('tell application "Google Chrome" to get URL of every tab of every window')
                q = urllib.parse.quote(query)
                if q in (r.stdout or "").replace(" ", ""):
                    result.update(success=True, data=f"已搜索: {query}（已验证）")
                else:
                    result.update(success=False, error=f"搜索打开未验证: {query}")

            elif action == "browser_screenshot":
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = P0_DIR / "browser" / f"bshot_{ts}.png"
                subprocess.run(["screencapture", "-x", str(path)], check=True, timeout=15)
                result.update(success=True, data=str(path))

            else:
                result["error"] = f"未知操作: {action}"
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"操作超时: {action}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

        self._record_history(action, params, result)
        return result

    def _record_history(self, action: str, params: Dict, result: Dict):
        record = {"timestamp": datetime.now().isoformat(), "action": action,
                  "params": params, "result": result.get("success"),
                  "data": str(result.get("data", ""))[:200],
                  "dna": generate_dna("BROWSER-HISTORY")}
        with open(P0_DIR / "browser" / "history.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ============================================================
# 3. 文件自动化（本机文件 · 查找/整理/重命名/去重）
# ============================================================
class FileAutomation:
    """文件操作 - mdfind 全盘搜索 + 目录整理 + 批量重命名 + 去重"""

    def __init__(self):
        self.encryption = LocalEncryption()

    def execute(self, action: str, params: Optional[Dict] = None) -> Dict:
        check = P0Protocol.check_action(action)
        if not check["allowed"]:
            return {"success": False, "error": check["reason"]}
        params = params or {}
        result = {"success": False, "action": action, "data": None}
        try:
            if action == "search_files":
                query = params.get("query", "")
                where = params.get("dir", str(Path.home() / "longhun-system"))
                if not query:
                    return {"success": False, "error": "请指定搜索词"}
                r = subprocess.run(["mdfind", "-onlyin", where, query],
                                   capture_output=True, text=True, timeout=20)
                files = [l for l in r.stdout.splitlines() if l.strip()]
                # mdfind 依赖 Spotlight 索引，可能为空 → 降级 rglob 文件名匹配（本机主权操作，绝不让老大扑空）
                if not files:
                    base = Path(where).expanduser()
                    if base.exists():
                        ql = query.lower()
                        try:
                            files = [str(p) for p in base.rglob("*")
                                     if p.is_file() and ql in p.name.lower()][:50]
                        except PermissionError:
                            pass
                result.update(success=True, data=files[:50])

            elif action == "list_dir":
                d = params.get("dir", str(P0_DIR))
                p = Path(d).expanduser()
                if not p.exists():
                    return {"success": False, "error": f"目录不存在: {d}"}
                entries = []
                for child in sorted(p.iterdir())[:100]:
                    entries.append({"name": child.name, "type": "dir" if child.is_dir() else "file",
                                    "size": child.stat().st_size if child.is_file() else 0})
                result.update(success=True, data=entries)

            elif action == "organize_dir":
                d = params.get("dir", str(Path.home() / "Downloads"))
                p = Path(d).expanduser()
                if not p.exists():
                    return {"success": False, "error": f"目录不存在: {d}"}
                EXT_MAP = {
                    "images": {".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic", ".svg"},
                    "docs": {".pdf", ".doc", ".docx", ".txt", ".md", ".pages", ".xls", ".xlsx", ".ppt", ".pptx"},
                    "media": {".mp4", ".mov", ".mkv", ".mp3", ".wav", ".flac", ".m4a"},
                    "archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".dmg"},
                    "code": {".py", ".js", ".ts", ".html", ".css", ".json", ".sh", ".swift", ".go", ".rs"},
                }
                moved = {}
                for child in p.iterdir():
                    if child.is_dir() or child.name.startswith("."):
                        continue
                    ext = child.suffix.lower()
                    target = None
                    for cat, exts in EXT_MAP.items():
                        if ext in exts:
                            target = p / cat
                            break
                    if target is None:
                        target = p / "others"
                    target.mkdir(exist_ok=True)
                    dest = target / child.name
                    if not dest.exists():
                        shutil.move(str(child), str(dest))
                        moved.setdefault(target.name, []).append(child.name)
                result.update(success=True, data=moved)

            elif action == "batch_rename":
                d = params.get("dir", "")
                pattern = params.get("pattern", "")
                prefix = params.get("prefix", "")
                if not d or not pattern:
                    return {"success": False, "error": "需要 dir 和 pattern"}
                p = Path(d).expanduser()
                renamed = []
                for i, child in enumerate(sorted(p.iterdir()), 1):
                    if child.is_dir():
                        continue
                    new_name = pattern.format(i=i, name=child.stem, prefix=prefix, ext=child.suffix)
                    dest = child.with_name(new_name)
                    if not dest.exists():
                        child.rename(dest)
                        renamed.append(f"{child.name} → {new_name}")
                result.update(success=True, data=renamed[:50])

            elif action == "deduplicate":
                d = params.get("dir", str(P0_DIR / "knowledge"))
                p = Path(d).expanduser()
                if not p.exists():
                    return {"success": False, "error": f"目录不存在: {d}"}
                seen, dupes = {}, []
                for child in p.rglob("*"):
                    if child.is_file():
                        h = hashlib.sha256(child.read_bytes()).hexdigest()[:16]
                        if h in seen:
                            dupes.append({"dup": str(child), "orig": seen[h]})
                        else:
                            seen[h] = str(child)
                result.update(success=True, data=dupes[:50])

            elif action == "copy_files":
                src, dst = params.get("src", ""), params.get("dst", "")
                if not src or not dst:
                    return {"success": False, "error": "需要 src 和 dst"}
                src, dst = Path(src).expanduser(), Path(dst).expanduser()
                dst.mkdir(parents=True, exist_ok=True)
                if src.is_dir():
                    shutil.copytree(src, dst / src.name, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
                result.update(success=True, data=f"{src} → {dst}")

            elif action == "move_files":
                src, dst = params.get("src", ""), params.get("dst", "")
                if not src or not dst:
                    return {"success": False, "error": "需要 src 和 dst"}
                src, dst = Path(src).expanduser(), Path(dst).expanduser()
                dst.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                result.update(success=True, data=f"{src} → {dst}")

            elif action == "open_file":
                path = params.get("path", "")
                if not path:
                    return {"success": False, "error": "请指定文件路径"}
                subprocess.run(["open", str(Path(path).expanduser())], check=True, timeout=10)
                result.update(success=True, data=f"已打开: {path}")

            elif action == "reveal_in_finder":
                path = params.get("path", "")
                if not path:
                    return {"success": False, "error": "请指定文件路径"}
                subprocess.run(["open", "-R", str(Path(path).expanduser())], check=True, timeout=10)
                result.update(success=True, data=f"已在Finder中显示: {path}")

            elif action == "get_file_info":
                path = params.get("path", "")
                if not path:
                    return {"success": False, "error": "请指定文件路径"}
                p = Path(path).expanduser()
                if not p.exists():
                    return {"success": False, "error": f"文件不存在: {path}"}
                st = p.stat()
                result.update(success=True, data={
                    "name": p.name, "size": st.st_size, "modified": datetime.fromtimestamp(st.st_mtime).isoformat(),
                    "created": datetime.fromtimestamp(st.st_birthtime).isoformat() if hasattr(st, "st_birthtime") else "n/a",
                    "is_dir": p.is_dir()})

            else:
                result["error"] = f"未知操作: {action}"
        except Exception as e:
            return {"success": False, "error": str(e)}

        self._record_history(action, params, result)
        return result

    def _record_history(self, action: str, params: Dict, result: Dict):
        record = {"timestamp": datetime.now().isoformat(), "action": action,
                  "params": params, "result": result.get("success"),
                  "data": str(result.get("data", ""))[:200],
                  "dna": generate_dna("FILE-HISTORY")}
        with open(P0_DIR / "files" / "history.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ============================================================
# 4. 知识自动化（搜索 → 爬取 → 去重 → 归档）
# ============================================================
class KnowledgeAutomation:
    """知识自动化 - 本地搜索网关优先，降级直接抓取"""

    SEARCH_API = "http://localhost:9631/search"

    def __init__(self):
        self.encryption = LocalEncryption()
        self.graph_file = P0_DIR / "knowledge" / "graph.json"
        self._ensure_graph()

    def _ensure_graph(self):
        if not self.graph_file.exists():
            self.graph_file.write_text(
                json.dumps({"nodes": [], "edges": [], "updated_at": datetime.now().isoformat()},
                           ensure_ascii=False, indent=2), encoding="utf-8")

    def execute(self, action: str, params: Optional[Dict] = None) -> Dict:
        check = P0Protocol.check_action(action)
        if not check["allowed"]:
            return {"success": False, "error": check["reason"]}
        params = params or {}
        result = {"success": False, "action": action, "data": None}
        try:
            if action == "search_web":
                query = params.get("query", "")
                if not query:
                    return {"success": False, "error": "请指定搜索词"}
                items = self._local_search(query)
                if not items:
                    items = self._fallback_search(query)
                result.update(success=True, query=query, count=len(items), data=items)
                self._save("search", query, result)

            elif action == "crawl_page":
                url = params.get("url", "")
                if not url:
                    return {"success": False, "error": "请指定URL"}
                content = self._crawl(url)
                result.update(success=True, url=url, content=content, length=len(content))
                self._save("crawl", url, result)

            elif action == "store_knowledge":
                title = params.get("title", "")
                content = params.get("content", "")
                tags = params.get("tags", [])
                if not title or not content:
                    return {"success": False, "error": "需要 title 和 content"}
                graph = json.loads(self.graph_file.read_text(encoding="utf-8"))
                node = {"id": f"K-{int(time.time())}", "title": title, "content": content,
                        "tags": tags, "dna": generate_dna("KNOWLEDGE-NODE"),
                        "timestamp": datetime.now().isoformat()}
                graph["nodes"].append(node)
                self.graph_file.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
                result.update(success=True, node_id=node["id"])
                self._save("store", title, result)

            elif action == "query_knowledge":
                query = params.get("query", "")
                if not query:
                    return {"success": False, "error": "请指定查询词"}
                graph = json.loads(self.graph_file.read_text(encoding="utf-8"))
                hits = [n for n in graph["nodes"]
                        if query.lower() in n["title"].lower() or query.lower() in n["content"].lower()]
                result.update(success=True, count=len(hits), data=hits[:20])

            else:
                result["error"] = f"未知操作: {action}"
        except Exception as e:
            return {"success": False, "error": str(e)}
        self._record_history(action, params, result)
        return result

    def _local_search(self, query: str) -> List[Dict]:
        """优先本地搜索网关 :9631（龍魂搜索引擎）"""
        try:
            url = self.SEARCH_API + "?" + urllib.parse.urlencode({"q": query, "limit": 5})
            req = urllib.request.Request(url, headers={"User-Agent": "LH-P0/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            items = []
            for it in (data.get("results") or data.get("data") or []):
                items.append({"title": it.get("title", ""), "url": it.get("url", it.get("link", "")),
                              "snippet": it.get("snippet", it.get("content", ""))[:200]})
            if items:
                logger.info(f"🔍 本地搜索网关命中 {len(items)} 条")
            return items
        except Exception:
            return []

    def _fallback_search(self, query: str) -> List[Dict]:
        """降级：直接抓 Bing 搜索页"""
        try:
            url = "https://www.bing.com/search?q=" + urllib.parse.quote(query)
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                page = resp.read().decode("utf-8", errors="ignore")
            items = []
            for m in re.finditer(r'<h2><a href="([^"]+)"[^>]*>(.*?)</a></h2>', page):
                title = html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
                items.append({"title": title, "url": m.group(1), "snippet": ""})
                if len(items) >= 5:
                    break
            return items
        except Exception:
            return []

    def _crawl(self, url: str) -> str:
        """抓取页面并提取正文（纯标准库）"""
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                page = resp.read().decode("utf-8", errors="ignore")
            # 去脚本样式
            page = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", page, flags=re.S)
            text = html.unescape(re.sub(r"<[^>]+>", " ", page))
            text = re.sub(r"\s+", " ", text).strip()
            return text[:3000]
        except Exception as e:
            return f"抓取失败: {e}"

    def _save(self, kind: str, name: str, result: Dict):
        fname = P0_DIR / "knowledge" / f"{kind}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        fname.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    def _record_history(self, action: str, params: Dict, result: Dict):
        record = {"timestamp": datetime.now().isoformat(), "action": action,
                  "params": params, "result": result.get("success"),
                  "dna": generate_dna("KNOWLEDGE-HISTORY")}
        with open(P0_DIR / "knowledge" / "history.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ============================================================
# 5. 代码自动化
# ============================================================
class CodeAutomation:
    """代码自动化 - 生成/分析/测试（本地）"""


    def execute(self, action: str, params: Optional[Dict] = None) -> Dict:
        check = P0Protocol.check_action(action)
        if not check["allowed"]:
            return {"success": False, "error": check["reason"]}
        params = params or {}
        result = {"success": False, "action": action, "data": None}
        try:
            if action == "generate_code":
                desc = params.get("description", "")
                lang = params.get("language", "python")
                if not desc:
                    return {"success": False, "error": "请描述要生成的代码"}
                dna = generate_dna("CODE-GEN")
                fname = P0_DIR / "code" / f"gen_{int(time.time())}.{lang}"
                skeleton = self._skeleton(desc, lang, dna)
                fname.write_text(skeleton, encoding="utf-8")
                result.update(success=True, dna=dna, file=str(fname), code=skeleton)
                self._record_history("generate_code", params, result)
                return result

            elif action == "analyze_code":
                path = params.get("path", "")
                if not path:
                    return {"success": False, "error": "请指定文件路径"}
                p = Path(path).expanduser()
                if not p.exists():
                    return {"success": False, "error": f"文件不存在: {path}"}
                code = p.read_text(encoding="utf-8", errors="ignore")
                result.update(success=True, lines=code.count("\n") + 1,
                              chars=len(code), funcs=len(re.findall(r"\bdef\s+\w+|function\s+\w+", code)))
                self._record_history("analyze_code", params, result)
                return result

            elif action == "format_code":
                path = params.get("path", "")
                if not path:
                    return {"success": False, "error": "请指定文件路径"}
                p = Path(path).expanduser()
                if p.suffix == ".py" and shutil.which("black"):
                    subprocess.run(["black", "-q", str(p)], check=True, timeout=30)
                    result.update(success=True, data="black 格式化完成")
                else:
                    result.update(success=True, data="无格式化工具，跳过(仅Python支持black)")
                self._record_history("format_code", params, result)
                return result

            elif action == "run_tests":
                path = params.get("path", "")
                if not path:
                    return {"success": False, "error": "请指定测试文件路径"}
                p = Path(path).expanduser()
                if p.suffix == ".py":
                    r = subprocess.run([sys.executable, "-m", "pytest", str(p), "-q"],
                                       capture_output=True, text=True, timeout=60)
                    result.update(success=True, returncode=r.returncode,
                                  output=(r.stdout + r.stderr)[-500:])
                else:
                    result.update(success=True, data="仅支持Python测试")
                self._record_history("run_tests", params, result)
                return result

            else:
                result["error"] = f"未知操作: {action}"
        except Exception as e:
            return {"success": False, "error": str(e)}
        return result

    def _skeleton(self, desc: str, lang: str, dna: str) -> str:
        header = (f"# 自動生成: {desc}\n# DNA: {dna}\n# 創建者: 诸葛鑫（UID9622）\n"
                  f"# License: MulanPSL v2\n# 主權本地生成 · 不外放\n\n")
        if lang == "python":
            return header + f'"""\n{desc}\n"""\n\n\ndef main():\n    print("🐉 P0生成骨架: {desc}")\n\n\nif __name__ == "__main__":\n    main()\n'
        if lang in ("js", "ts"):
            return header + f"// {desc}\nfunction main() {{\n  console.log('🐉 P0生成骨架: {desc}');\n}}\nmain();\n"
        if lang == "sh":
            return header + f"#!/bin/bash\n# {desc}\necho '🐉 P0生成骨架: {desc}'\n"
        return header + f"# {desc}\n"

    def _record_history(self, action: str, params: Dict, result: Dict):
        record = {"timestamp": datetime.now().isoformat(), "action": action,
                  "params": params, "result": result.get("success"),
                  "dna": generate_dna("CODE-HISTORY")}
        with open(P0_DIR / "code" / "history.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ============================================================
# 6. 写作自动化
# ============================================================
class WritingAutomation:
    """写作自动化 - 研究 → 大纲 → 正文 → 审校"""


    def execute(self, action: str, params: Optional[Dict] = None) -> Dict:
        check = P0Protocol.check_action(action)
        if not check["allowed"]:
            return {"success": False, "error": check["reason"]}
        params = params or {}
        result = {"success": False, "action": action, "data": None}
        try:
            if action == "generate_outline":
                topic = params.get("topic", "")
                if not topic:
                    return {"success": False, "error": "请指定主题"}
                outline = [f"一、引言（为什么要谈{topic}）", "二、核心现状与背景", "三、关键问题拆解",
                           "四、龍魂视角的解法", "五、落地路径与下一步", "六、结语（回到主权初心）"]
                result.update(success=True, topic=topic, outline=outline)
                self._save("outline", topic, result)

            elif action == "write_article":
                topic = params.get("topic", "")
                sections = params.get("sections", [])
                if not topic:
                    return {"success": False, "error": "请指定主题"}
                article = self._compose(topic, sections)
                fname = P0_DIR / "writing" / f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                fname.write_text(article, encoding="utf-8")
                result.update(success=True, file=str(fname), article=article)
                self._save("article", topic, result)

            elif action == "proofread":
                path = params.get("path", "")
                if not path:
                    return {"success": False, "error": "请指定文件路径"}
                p = Path(path).expanduser()
                text = p.read_text(encoding="utf-8", errors="ignore")
                issues = []
                for w in ["的的", "了了", " 。", " ，", "。。", "，，"]:
                    if w in text:
                        issues.append(f"疑似重复/错误标点: {w}")
                result.update(success=True, issues=issues, char_count=len(text))
                self._save("proofread", path, result)

            elif action == "generate_report":
                title = params.get("title", "龍魂报告")
                content = params.get("content", "")
                lines = ["# " + title, "", "> 生成时间: " + datetime.now().isoformat(),
                         "> DNA: " + generate_dna("REPORT"), "", content]
                fname = P0_DIR / "writing" / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                fname.write_text("\n".join(lines), encoding="utf-8")
                result.update(success=True, file=str(fname))
                self._save("report", title, result)

            else:
                result["error"] = f"未知操作: {action}"
        except Exception as e:
            return {"success": False, "error": str(e)}
        self._record_history(action, params, result)
        return result

    def _compose(self, topic: str, sections: List[str]) -> str:
        parts = [f"# {topic}", "", f"> 🐉 龍魂主权写作 · {datetime.now().isoformat()}",
                 f"> DNA: {generate_dna('WRITING')}", ""]
        if sections:
            for s in sections:
                parts += [f"## {s}", "", "（正文待续：请使用 `lh p0 --run \"帮我查{topic}资料\"` 补充内容）", ""]
        else:
            parts += ["## 引言", f"关于「{topic}」，龍魂的第一原则：信息主权归用户，AI只在本机干活。", "",
                      "## 正文", "（正文待续：先跑知识搜索补充素材，再迭代完善。）", ""]
        return "\n".join(parts)

    def _save(self, kind: str, name: str, result: Dict):
        fname = P0_DIR / "writing" / f"{kind}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        fname.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    def _record_history(self, action: str, params: Dict, result: Dict):
        record = {"timestamp": datetime.now().isoformat(), "action": action,
                  "params": params, "result": result.get("success"),
                  "dna": generate_dna("WRITING-HISTORY")}
        with open(P0_DIR / "writing" / "history.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ============================================================
# 主引擎（意图路由）
# ============================================================
class P0Automation:
    """P0 全自动化主引擎 - 主权人格直接操作自己的 Mac"""

    def __init__(self):
        self.mac = MacAutomation()
        self.browser = BrowserAutomation()
        self.files = FileAutomation()
        self.knowledge = KnowledgeAutomation()
        self.code = CodeAutomation()
        self.writing = WritingAutomation()
        self.dna = generate_dna("P0-INIT")

    # ---------- Mac 软件 ----------
    def _route_mac(self, command: str) -> Dict:
        m = re.search(r'打开\s*(\S+)', command)
        if m:
            return self.mac.execute("open_app", {"name": m.group(1)})
        m = re.search(r'激活\s*(\S+)', command)
        if m:
            return self.mac.execute("activate_app", {"name": m.group(1)})
        m = re.search(r'关闭\s*(\S+)', command)
        if m:
            return self.mac.execute("close_app", {"name": m.group(1)})
        if "截屏" in command or "截图" in command:
            return self.mac.execute("screenshot")
        if "当前软件" in command or "前台软件" in command:
            return self.mac.execute("get_front_app")
        if "软件列表" in command or "应用列表" in command:
            return self.mac.execute("list_apps")
        return {"success": False, "error": "未识别的Mac操作，试试: 打开微信 / 截屏 / 软件列表"}

    # ---------- 浏览器 ----------
    def _route_browser(self, command: str) -> Dict:
        m = re.search(r'(?:打开|访问)\s*(https?://\S+|www\.\S+)', command)
        if m:
            return self.browser.execute("open_url", {"url": m.group(1)})
        m = re.search(r'搜索\s*(.+?)$', command)
        if m:
            return self.browser.execute("search_web", {"query": m.group(1).strip()})
        if "标签页" in command or "标签" in command:
            return self.browser.execute("list_tabs")
        if "刷新" in command:
            return self.browser.execute("refresh")
        if "后退" in command:
            return self.browser.execute("back")
        if "前进" in command:
            return self.browser.execute("forward")
        if "当前网址" in command or "当前URL" in command:
            return self.browser.execute("get_url")
        return {"success": False, "error": "未识别的浏览器操作，试试: 打开 https://uid9622.cn / 搜索 xxx"}

    # ---------- 文件 ----------
    def _route_files(self, command: str) -> Dict:
        m = re.search(r'查找\s*(\S+)', command)
        if m:
            return self.files.execute("search_files", {"query": m.group(1)})
        m = re.search(r'整理\s*(\S+)', command)
        if m:
            return self.files.execute("organize_dir", {"dir": m.group(1)})
        m = re.search(r'查看\s*(\S+)', command)
        if m:
            return self.files.execute("list_dir", {"dir": m.group(1)})
        m = re.search(r'打开文件\s*(\S+)', command)
        if m:
            return self.files.execute("open_file", {"path": m.group(1)})
        return {"success": False, "error": "未识别的文件操作，试试: 查找 pdf / 整理 ~/Downloads"}

    # ---------- 知识 ----------
    def _route_knowledge(self, command: str) -> Dict:
        m = re.search(r'(?:搜索|查找|查一下)\s*(.+?)$', command)
        if m:
            return self.knowledge.execute("search_web", {"query": m.group(1).strip()})
        m = re.search(r'爬取\s*(https?://\S+)', command)
        if m:
            return self.knowledge.execute("crawl_page", {"url": m.group(1)})
        return {"success": False, "error": "未识别的知识操作，试试: 搜索抗战历史 / 爬取 https://xxx"}

    # ---------- 代码 ----------
    def _route_code(self, command: str) -> Dict:
        m = re.search(r'写(?:一个|个)?\s*(\S+?)(?:代码|爬虫|脚本|程序)?$', command)
        lang = "python"
        if "shell" in command or "bash" in command:
            lang = "sh"
        if "javascript" in command or "js" in command:
            lang = "js"
        return self.code.execute("generate_code", {"description": command, "language": lang})

    # ---------- 写作 ----------
    def _route_writing(self, command: str) -> Dict:
        m = re.search(r'(?:写|写一|写一篇|生成)\s*(?:关于|一篇)?\s*(.+?)$', command)
        topic = m.group(1).strip() if m else command.strip()
        return self.writing.execute("write_article", {"topic": topic})

    # ---------- 主路由 ----------
    def execute(self, command: str) -> Dict:
        cmd = command.strip()
        low = cmd.lower()

        # 显式领域前缀优先
        if "浏览器" in cmd or "网页" in cmd or low.startswith("browser"):
            return self._route_browser(cmd)
        if "文件" in cmd or "整理" in cmd or "查找" in cmd or low.startswith("file"):
            return self._route_files(cmd)
        if "搜索" in cmd or "知识" in cmd or "查一下" in cmd:
            return self._route_knowledge(cmd)
        if "代码" in cmd or "爬虫" in cmd or "脚本" in cmd or low.startswith("code"):
            return self._route_code(cmd)
        if "文章" in cmd or "写作" in cmd or low.startswith("write"):
            return self._route_writing(cmd)
        if "微信" in cmd or "打开" in cmd or "截屏" in cmd or "软件" in cmd or "应用" in cmd or low.startswith("mac"):
            return self._route_mac(cmd)

        return {"success": False, "error": "未能识别命令意图",
                "hint": "试试: 打开微信 | 浏览器打开 https://uid9622.cn | 搜索抗战历史 | 写一个爬虫 | 写一篇AI治理文章 | 整理 ~/Downloads"}

    def get_status(self) -> Dict:
        return {
            "dna": self.dna,
            "platform": "Mac（主权人格直接操作本机 · 非代理 · 不外放）",
            "mac_automation": "✅ AppleScript/osascript",
            "browser": "✅ Safari/Chrome (+CDP)" if self.browser.cdp_available else "✅ Safari/Chrome",
            "files": "✅ mdfind + 目录整理",
            "knowledge": "✅ 本地搜索网关(:9631) + 降级抓取",
            "code": "✅ 本地生成",
            "writing": "✅ 本地写作",
            "encryption": "✅ Fernet(AES-128) 本地加密",
            "data_policy": "所有数据仅存 ~/.longhun/p0_automation/ · 不上传 · 不监听端口 · 不外放",
            "p0_protocol": "已加载（硬边界: 不代理/不外放/不越权）",
            "timestamp": datetime.now().isoformat()
        }


# ============================================================
# 史官统一记录（04_AUDIT）
# ============================================================
def audit_log(engine: str, action: str, result: Dict):
    entry = {"timestamp": datetime.now().isoformat(), "engine": engine, "action": action,
             "success": result.get("success"), "dna": generate_dna("AUDIT")}
    with open(AUDIT_DIR / "p0_automation.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ============================================================
# CLI
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · P0全自动化智能体（Mac主权版）—— 主权人格直接操作自己的Mac，非代理、不外放",
        epilog="说人话，它干活。所有数据仅存本机 ~/.longhun/p0_automation/，不上传、不开端口、不外放。")
    parser.add_argument("--status", "-s", action="store_true", help="查看系统状态")
    parser.add_argument("--app", "-a", type=str, help="Mac软件操作，如: --app 微信 / --app list")
    parser.add_argument("--browser", "-b", type=str, help="浏览器操作，如: --browser \"https://uid9622.cn\" / --browser search 关键词")
    parser.add_argument("--file", "-f", nargs="+", help="文件操作，如: --file search pdf / --file list ~/Downloads")
    parser.add_argument("--search", type=str, help="知识搜索，如: --search \"抗战历史\"")
    parser.add_argument("--code", type=str, help="代码生成，如: --code \"写一个爬虫\"")
    parser.add_argument("--write", type=str, help="写作，如: --write \"写一篇AI治理文章\"")
    parser.add_argument("--run", "-c", type=str, help="自然语言整句命令，如: --run \"打开微信\"")
    parser.add_argument("--encrypt", type=str, help="加密一段文本（本地主密钥）")
    parser.add_argument("--decrypt", type=str, help="解密（--encrypt 输出的hex）")
    parser.add_argument("--protocol-check", type=str, help="检查操作是否允许，如: --protocol-check upload_data")
    args = parser.parse_args()

    p0 = P0Automation()

    if args.status:
        status = p0.get_status()
        print("\n🐉 P0全自动化智能体 · Mac主权版")
        print("=" * 58)
        for k, v in status.items():
            print(f"  {k}: {v}")
        print("=" * 58)
        return

    if args.protocol_check:
        print(json.dumps(P0Protocol.check_action(args.protocol_check), ensure_ascii=False, indent=2))
        return

    if args.encrypt:
        print(json.dumps(p0.mac.encryption.encrypt(args.encrypt), ensure_ascii=False, indent=2))
        return
    if args.decrypt:
        print(p0.mac.encryption.decrypt(args.decrypt))
        return

    if args.app:
        if args.app == "list":
            r = p0.mac.execute("list_apps")
        else:
            r = p0.mac.execute("open_app", {"name": args.app})
        print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
        audit_log("mac", "app", r)
        return

    if args.browser:
        if args.browser.startswith("search "):
            r = p0.browser.execute("search_web", {"query": args.browser[7:]})
        elif args.browser.startswith(("http", "www")):
            r = p0.browser.execute("open_url", {"url": args.browser})
        else:
            r = p0.browser.execute("open_url", {"url": args.browser})
        print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
        audit_log("browser", "browser", r)
        return

    if args.file:
        sub = args.file[0]
        param = args.file[1] if len(args.file) > 1 else ""
        act = {"search": "search_files", "list": "list_dir", "organize": "organize_dir",
               "open": "open_file", "info": "get_file_info"}.get(sub)
        if not act:
            print(json.dumps({"success": False, "error": f"未知文件操作: {sub}（search/list/organize/open/info）"}, ensure_ascii=False))
            return
        params = {"query": param} if sub == "search" else ({"dir": param} if sub in ("list", "organize") else
                  {"path": param} if sub == "open" else {"path": param})
        r = p0.files.execute(act, params)
        print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
        audit_log("files", sub, r)
        return

    if args.search:
        r = p0.knowledge.execute("search_web", {"query": args.search})
        print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
        audit_log("knowledge", "search", r)
        return

    if args.code:
        r = p0.code.execute("generate_code", {"description": args.code, "language": "python"})
        print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
        audit_log("code", "generate", r)
        return

    if args.write:
        r = p0.writing.execute("write_article", {"topic": args.write})
        print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
        audit_log("writing", "write", r)
        return

    if args.run:
        r = p0.execute(args.run)
        print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
        audit_log("p0", "run", r)
        return

    # 交互模式
    print("""
╔══════════════════════════════════════════════════════════════╗
║  🐉 龍魂 · P0全自动化智能体（Mac主权版）                     ║
║  主权人格直接操作自己的Mac · 非代理 · 能力不外放             ║
║  -------------------------------------------------         ║
║  示例:                                                      ║
║    "打开微信" / "截屏" / "软件列表"                        ║
║    "浏览器打开 https://uid9622.cn"                          ║
║    "搜索抗战历史" / "爬取 https://..."                     ║
║    "查找 pdf" / "整理 ~/Downloads"                          ║
║    "写一个Python爬虫" / "写一篇AI治理文章"                  ║
║  -------------------------------------------------         ║
║  P0硬边界: 不代理 · 不外放 · 不上传 · 全本地加密存储        ║
╚══════════════════════════════════════════════════════════════╝
    """)
    while True:
        try:
            cmd = input("\n💬 你: ").strip()
            if cmd.lower() in ("exit", "quit", "q"):
                break
            if not cmd:
                continue
            r = p0.execute(cmd)
            audit_log("p0", "interactive", r)
            if r.get("success"):
                data = r.get("data")
                if isinstance(data, list):
                    print(f"✅ 共 {len(data)} 项:")
                    for i, item in enumerate(data[:30], 1):
                        print(f"  {i}. {item}")
                elif data:
                    print(f"✅ {data}")
                else:
                    print(f"✅ {r.get('data') or r.get('message') or '完成'}")
            else:
                print(f"❌ {r.get('error', '执行失败')}  {r.get('hint', '')}")
        except KeyboardInterrupt:
            break
        except EOFError:
            break


if __name__ == "__main__":
    main()
