# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""M75 龍魂渲染编排器 · CNSH 指令总调度 · 平台路由 · DNA/审计/主权边界。"""

import datetime
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import urlparse

from .adapters.web_adapter import WebAdapter
from .adapters.desktop_adapter import DesktopAdapter
from .adapters.harmonyos_adapter import HarmonyOSAdapter
from .adapters.ios_adapter import IOSAdapter
from .core.cnsh_parser import CNSHRenderParser
from .core.variables import RenderContext
from .core.boundary import SovereigntyBoundary
from .core.audit import audit_text
from .core.hash_registry import HashRegistry

ROOT = Path(__file__).resolve().parent.parent
RENDER_DIR = ROOT / "data" / "renders"
DEFAULT_CONFIG = {
    "headless": True,
    "width": 1920,
    "height": 1080,
    "render_dir": str(RENDER_DIR),
}


class LHRenderOrchestrator:
    """龍魂渲染编排器 · 总调度。"""

    VERSION = "1.0.0"
    UID = "UID9622"

    def __init__(self, config: dict = None):
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.ctx: RenderContext = None
        self.web = WebAdapter(self.config)
        self.desktop = DesktopAdapter()
        self.hos = HarmonyOSAdapter()
        self.ios = IOSAdapter()
        self.parser = CNSHRenderParser(self)
        self.boundary = SovereigntyBoundary()
        self.secrets = {}            # {secrets.*} 命名空间（外部注入，不回日志）
        self._audit_log = []
        self._last_result = {}
        Path(self.config["render_dir"]).mkdir(parents=True, exist_ok=True)
        # M73 哈希产权引擎：截图 SHA-256 + DNA 绑定 + Merkle 链注册
        self.hash_registry = HashRegistry(
            Path(self.config["render_dir"]) / "hash_registry.jsonl")

    # ────────── CNSH 指令入口 ──────────

    def execute(self, cnsh_command: str) -> dict:
        """执行一条 CNSH 渲染指令。返回变量环境结果。"""
        try:
            result = self.parser.parse_and_run(cnsh_command)
            self._log_audit(cnsh_command, result, "🟢")
            return {"status": "ok", "context": result, "audit": "🟢"}
        except PermissionError as e:
            self._log_audit(cnsh_command, None, "🔴", str(e))
            return {"status": "blocked", "error": str(e), "audit": "🔴"}
        except Exception as e:
            self._log_audit(cnsh_command, None, "🟡", str(e))
            return {"status": "error", "error": str(e), "audit": "🟡"}

    def _log_audit(self, cmd: str, ctx, color: str, error: str = None):
        self._audit_log.append({
            "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
            "command": cmd[:200],
            "color": color,
            "dna": getattr(ctx, "dna", None) if ctx else None,
            "error": error,
        })
        if len(self._audit_log) > 500:
            self._audit_log = self._audit_log[-500:]

    # ────────── 平台路由 ──────────

    def _route(self, url: str) -> str:
        if url.startswith(("app://", "hap://")):
            return "harmonyos"
        if url.startswith("ios://"):
            return "ios"
        if url.startswith("desktop://"):
            return "desktop"
        return "web"

    # ────────── 指令实现 ──────────

    def navigate(self, url: str, light: bool = False) -> dict:
        """渲染.打开(url) → 平台路由 + 完整变量环境。

        light=True 批量轻量模式：跳过 DOM/表单/表格/截图，只取核心字段（快 3~5 倍）。
        """
        domain = self.boundary.check(url)
        platform = self._route(url)
        if platform == "web":
            ctx = self.web.navigate(url)
        elif platform == "desktop":
            ctx = self.desktop.capture_context(url)
        elif platform == "harmonyos":
            ctx = self.hos.launch_app(url.replace("app://", ""))
        elif platform == "ios":
            ctx = self.ios.launch_app(url.replace("ios://", ""))
        else:
            raise ValueError(f"未知平台: {platform}")
        self.ctx = ctx
        self._enrich_ctx(ctx, url, light=light)
        return self._summary(ctx)

    def _enrich_ctx(self, ctx: RenderContext, url: str, light: bool = False) -> None:
        """导航后补齐视觉/结构/审计字段。"""
        if ctx.platform == "web":
            if not light:
                try:
                    ctx.dom = self.web.extract_dom()
                except Exception as e:
                    ctx.error = ctx.error or f"DOM: {e}"
                try:
                    ctx.links = self.web.extract_links()
                except Exception as e:
                    ctx.links = []
                try:
                    ctx.forms = self.web.extract_forms()
                except Exception as e:
                    ctx.forms = []
                try:
                    ctx.tables = self.web.extract_tables()
                except Exception as e:
                    ctx.tables = []
                try:
                    ctx.cookies = self.web.get_cookies()
                except Exception as e:
                    ctx.cookies = []
                try:
                    ctx.scroll_pos = self.web.scroll_position()
                except Exception as e:
                    pass
            try:
                ctx.text = self.web.extract_text(mode="DOM")
            except Exception as e:
                ctx.error = ctx.error or f"TEXT: {e}"
        if not light and ctx.screenshot is None and ctx.platform == "web":
            try:
                ctx.screenshot = self.web.screenshot(full_page=True)
            except Exception:
                pass
        if ctx.screenshot:
            fname = f"render_{hashlib.sha256((url + ctx.timestamp).encode()).hexdigest()[:12]}.png"
            path = Path(self.config["render_dir"]) / fname
            try:
                path.write_bytes(ctx.screenshot)
                ctx.screenshot_path = str(path)
            except Exception:
                pass
        ctx.audit = audit_text(ctx.text or "")
        ctx.dna = ctx.generate_dna(self.UID)
        # M73：截图产权哈希自动登记（有截图才登记，不打断主流程）
        if ctx.screenshot_path:
            try:
                ctx.hash_rec = self.hash_registry.register_file(
                    ctx.screenshot_path, ctx.dna, url, ctx.platform)
            except Exception as e:
                ctx.hash_rec = {"error": str(e)}

    def _summary(self, ctx: RenderContext) -> dict:
        """返回变量环境摘要（screenshot 走路径，不塞 base64 防爆）。"""
        d = ctx.to_dict(with_screenshot=False)
        d["screenshot_base64_len"] = len(ctx.screenshot) if ctx.screenshot else 0
        d["render"] = {f: ctx.register(f) for f in RenderContext.FIELDS}
        self._last_result = d
        return d

    # ── 提取转发 ──

    def extract_dom(self, selector: str = None, depth: int = 6) -> dict:
        self._require_web()
        self.ctx.dom = self.web.extract_dom(selector, depth)
        return self.ctx.dom

    def extract_text(self, selector: str = None, mode: str = "DOM") -> str:
        self._require_web()
        self.ctx.text = self.web.extract_text(selector, mode)
        return self.ctx.text

    def extract_elements(self, selector: str = None, type: str = None,
                         contains_text: str = None) -> list:
        self._require_web()
        self.ctx.elements = self.web.extract_elements(selector, type, contains_text)
        return self.ctx.elements

    def screenshot(self, region: str = None, selector: str = None) -> dict:
        self._require_web()
        if selector:
            data = self.web.screenshot(full_page=False, selector=selector)
        else:
            data = self.web.screenshot(full_page=(region != "viewport"))
        fname = f"shot_{hashlib.sha256(datetime.datetime.now().isoformat().encode()).hexdigest()[:10]}.png"
        path = Path(self.config["render_dir"]) / fname
        path.write_bytes(data)
        self.ctx.screenshot = data
        self.ctx.screenshot_path = str(path)
        # M73：手动截图也登记产权哈希
        try:
            rec = self.hash_registry.register_file(str(path), self.ctx.dna,
                                                   self.ctx.url, self.ctx.platform)
        except Exception as e:
            rec = {"error": str(e)}
        return {"path": str(path), "bytes": len(data), "render.screenshot": str(path),
                "hash_registry": rec}

    def visual_match(self, template: str, threshold: float = 0.8) -> dict:
        from .vision.visual_match import match_template
        self._require_web()
        shot = self.web.screenshot(full_page=True)
        self.ctx.match = match_template(shot, template, threshold)
        return self.ctx.match

    def export(self, fmt: str) -> dict:
        """渲染.导出(格式=...) → 对应变量。"""
        self._require_web()
        m = {
            "DOM树": ("dom", lambda: self.ctx.dom),
            "文本": ("text", lambda: self.ctx.text),
            "截图": ("screenshot", lambda: self.ctx.screenshot_path),
            "表格": ("tables", lambda: self.web.extract_tables()),
            "链接": ("links", lambda: self.ctx.links),
            "元数据": ("meta", lambda: self.ctx.meta),
            "无障碍树": ("ax_tree", lambda: self.ctx.ax_tree),
        }
        key, fn = m.get(fmt, ("text", lambda: self.ctx.text))
        value = fn()
        return {"key": f"render.{key}", "value": value}

    def save(self, variable: str = "text", path: str = None, fmt: str = "json") -> dict:
        """渲染.保存(变量=, 路径=, 格式=)。"""
        field = variable.replace("render.", "") if variable else "text"
        value = getattr(self.ctx, field, None)
        if value is None:
            return {"error": f"变量 {variable} 为空"}
        path = path or str(Path(self.config["render_dir"]) / f"export_{datetime.date.today().isoformat()}")
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        if fmt == "json":
            p.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        elif fmt == "text":
            p.write_text(str(value), encoding="utf-8")
        elif fmt == "png":
            p.write_bytes(value)
        else:
            p.write_text(str(value), encoding="utf-8")
        return {"path": str(p), "bytes": p.stat().st_size}

    def set_dna(self, dna: str) -> dict:
        if self.ctx:
            self.ctx.dna = dna
        return {"dna": dna}

    def audit(self) -> dict:
        self.ctx.audit = audit_text(self.ctx.text or "")
        return self.ctx.audit

    # ── M73 哈希产权 ──

    def register_hash(self, path: str = None) -> dict:
        """渲染.注册哈希(路径=?) → 登记产权哈希。

        无路径时用当前截图；已登记则幂等返回既有记录。
        """
        target = path or (self.ctx.screenshot_path if self.ctx else None)
        if not target:
            return {"error": "无截图可注册，请先 渲染.打开/渲染.截图"}
        if self.ctx is None:
            self.ctx = RenderContext(platform="web", url=str(target))
        rec = self.hash_registry.register_file(str(target), self.ctx.dna or "",
                                               self.ctx.url, self.ctx.platform)
        return {"registered": True, "record": rec, "stats": self.hash_registry.stats()}

    def verify_hash(self, sha256: str = None, path: str = None) -> dict:
        """渲染.验证哈希(哈希=? / 路径=?) → 溯源归属。"""
        if path and not sha256:
            p = Path(path)
            if not p.is_file():
                return {"error": f"文件不存在: {p}"}
            import hashlib as _hl
            h = _hl.sha256()
            with open(p, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
            sha256 = h.hexdigest()
        if not sha256:
            return {"error": "缺少参数：请传 哈希= 或 路径="}
        rec = self.hash_registry.verify(sha256)
        if not rec:
            return {"registered": False, "sha256": sha256.lower(),
                    "message": "未登记（无产权记录）"}
        return {"registered": True, "record": rec}

    def set_boundary(self, allow_domains=None, deny_domains=None,
                     no_upload=None, local_only=None) -> dict:
        self.boundary.configure(allow_domains, deny_domains, no_upload, local_only)
        return self.boundary.to_dict()

    def batch(self, urls: list, concurrency: int = 4, interval: float = 0.5) -> list:
        """渲染.批量(urls=, 并发=, 间隔=)。

        说明: Playwright sync API 线程不安全，本机串行执行（稳定优先）。
        鲲鹏高并发用多实例/多进程编排（见 deploy_render.sh / Docker）。
        """
        import time
        results = []
        for u in urls:
            try:
                r = self.navigate(u, light=True)   # 批量轻量模式：快 3~5 倍
                if interval:
                    time.sleep(interval)
                results.append({"url": u, "status": "ok", "result": r})
            except Exception as e:
                results.append({"url": u, "status": "error", "error": str(e)})
        return results

    # ── 交互转发 ──

    def _require_web(self):
        if self.ctx is None or self.ctx.platform != "web":
            raise RuntimeError("请先 渲染.打开(web地址)")

    def click(self, selector=None, text=None, coords=None, match_result=None):
        self._require_web()
        self.web.click(selector, text, coords, match_result)
        return {"clicked": selector or text or coords}

    def fill(self, selector: str, value: str, mask: bool = False):
        self._require_web()
        r = self.web.fill(selector, value, mask)
        if mask:
            self.secrets.pop(selector, None)
        return {"filled": selector, **r}

    def clear(self, selector: str):
        self._require_web()
        self.web.clear(selector)
        return {"cleared": selector}

    def scroll(self, direction="下", distance=500, to_end=False,
               element=None, to_center=False):
        self._require_web()
        self.web.scroll(direction, distance, to_end, element, to_center)
        self.ctx.scroll_pos = self.web.scroll_position()
        return self.ctx.scroll_pos

    def select_option(self, selector: str, value: str):
        self._require_web()
        self.web.select_option(selector, value)
        return {"selected": selector}

    def check(self, selector: str):
        self._require_web()
        self.web.check(selector, True)
        return {"checked": selector}

    def uncheck(self, selector: str):
        self._require_web()
        self.web.check(selector, False)
        return {"unchecked": selector}

    def hover(self, selector: str):
        self._require_web()
        self.web.hover(selector)
        return {"hovered": selector}

    def keypress(self, key: str):
        self._require_web()
        self.web.keypress(key)
        return {"key": key}

    def wait(self, condition=None, selector=None, seconds=None):
        self._require_web()
        self.web.wait(condition, selector, seconds)
        return {"waited": condition or selector or seconds}

    def go_back(self):
        self._require_web()
        self.web.go_back()
        return {"back": True}

    def go_forward(self):
        self._require_web()
        self.web.go_forward()
        return {"forward": True}

    def reload(self):
        self._require_web()
        self.web.reload()
        return {"reloaded": True}

    # ── 状态 ──

    def status(self) -> dict:
        return {
            "version": self.VERSION,
            "uid": self.UID,
            "platform": self.ctx.platform if self.ctx else None,
            "url": self.ctx.url if self.ctx else None,
            "dna": self.ctx.dna if self.ctx else None,
            "boundary": self.boundary.to_dict(),
            "render_dir": self.config["render_dir"],
            "audit_entries": len(self._audit_log),
            "audit_log": self._audit_log[-10:],
        }

    def close(self):
        self.web.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
