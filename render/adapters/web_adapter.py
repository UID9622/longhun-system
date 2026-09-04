# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""Web 渲染适配器 · Playwright + Chromium（本地 & 鲲鹏 ARM64 兼容）。"""

import base64
import json
import os
import time
from pathlib import Path

from ..core.variables import RenderContext
from ..core.audit import audit_text

_DOM_EXTRACT_JS = """
function(arg_depth) {
  function nodeToJSON(node, depth, maxDepth) {
    if (depth > maxDepth || !node) return null;
    const obj = {
      tag: (node.tagName || node.nodeName || '').toLowerCase(),
      id: node.id || null,
      class: (typeof node.className === 'string') ? node.className : null,
      text: (node.innerText || '').trim().slice(0, 200) || null,
      attrs: {},
      children: []
    };
    if (node.attributes) {
      for (const a of node.attributes) obj.attrs[a.name] = a.value;
    }
    if (node.children) {
      for (const c of node.children) {
        const cj = nodeToJSON(c, depth + 1, maxDepth);
        if (cj) obj.children.push(cj);
      }
    }
    return obj;
  }
  const maxDepth = arg_depth || 6;
  return nodeToJSON(document.body, 0, maxDepth);
}
"""


class WebAdapter:
    """Web 渲染适配器（同步 Playwright）。"""

    SUPPORTED_PLATFORMS = ["web", "miniapp_h5", "wechat_h5"]

    def __init__(self, config: dict = None, headless: bool = True):
        self.config = config or {}
        self.headless = self.config.get("headless", headless)
        self.width = self.config.get("width", 1920)
        self.height = self.config.get("height", 1080)
        self._pw = None
        self.browser = None
        self.page = None

    def launch(self):
        """启动浏览器。优先 Playwright Chromium；失败回退系统 Chromium。"""
        if self.page is not None:
            return self
        try:
            from playwright.sync_api import sync_playwright
            self._pw = sync_playwright().start()
            try:
                self.browser = self._pw.chromium.launch(
                    headless=self.headless,
                    args=self._launch_args(),
                )
            except Exception:
                # 回退：系统 Chromium（龍魂浏览器等）
                self.browser = self._pw.chromium.launch(
                    headless=self.headless,
                    executable_path=self._system_chromium(),
                    args=self._launch_args(),
                )
        except ImportError:
            raise RuntimeError("playwright 未安装: pip install playwright && playwright install chromium")
        ctx = self.browser.new_context(
            viewport={"width": self.width, "height": self.height},
            user_agent=self.config.get(
                "user_agent",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
            ),
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )
        self.page = ctx.new_page()
        return self

    @staticmethod
    def _launch_args() -> list:
        return [
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--no-sandbox",
        ]

    @staticmethod
    def _system_chromium() -> str:
        candidates = [
            os.path.expanduser("~/Applications/龍魂浏览器.app/Contents/MacOS/Chromium"),
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/usr/bin/chromium", "/usr/bin/chromium-browser",
            "/opt/chromium/chrome",
        ]
        for c in candidates:
            if Path(c).exists():
                return c
        raise RuntimeError("找不到 Chromium，请先 playwright install chromium")

    def close(self):
        try:
            if self.browser:
                self.browser.close()
        finally:
            if self._pw:
                self._pw.stop()
            self._pw = self.browser = self.page = None

    # ── 导航 ──

    def navigate(self, url: str, timeout_ms: int = 30000) -> RenderContext:
        self.launch()
        # 主等待 domcontentloaded（快），networkidle 对重 JS 站会死等 30s+ 拖垮批量。
        # 加载后短等待动态渲染，速度与稳定性兼得。
        try:
            self.page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        except Exception:
            try:
                self.page.goto(url, wait_until="commit", timeout=timeout_ms)
            except Exception:
                pass
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=8000)
        except Exception:
            pass
        time.sleep(1.2)
        ctx = RenderContext(platform="web", url=url,
                            viewport={"width": self.width, "height": self.height})
        ctx.title = self.page.title()
        ctx.domain = url.split("//")[-1].split("/")[0].split(":")[0]
        ctx.meta = self.page.evaluate(
            "() => { const q = s => document.querySelector(s); "
            "return { description: q('meta[name=description]')?.content || null, "
            "og_title: q('meta[property=\"og:title\"]')?.content || null, "
            "og_image: q('meta[property=\"og:image\"]')?.content || null }; }"
        )
        return ctx

    # ── 提取 ──

    def screenshot(self, full_page: bool = True, selector: str = None,
                   path: str = None) -> bytes:
        self.launch()
        if selector:
            data = self.page.locator(selector).first.screenshot()
        else:
            data = self.page.screenshot(full_page=full_page)
        if path:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_bytes(data)
        return data

    def extract_dom(self, selector: str = None, depth: int = 6) -> dict:
        self.launch()
        if selector:
            el = self.page.locator(selector).first
            if el.count() == 0:
                return {"error": f"选择器未命中: {selector}"}
            return el.evaluate(_DOM_EXTRACT_JS, depth)
        return self.page.evaluate(_DOM_EXTRACT_JS, depth)

    def extract_text(self, selector: str = None, mode: str = "DOM") -> str:
        self.launch()
        if selector:
            el = self.page.locator(selector).first
            if el.count() == 0:
                return ""
            return el.inner_text()
        if mode.upper() == "DOM":
            return self.page.evaluate("() => document.body.innerText")
        # OCR 模式：截图后走 vision/ocr（可选）
        try:
            from ..vision.ocr import ocr_image
            img = self.screenshot(full_page=True)
            return ocr_image(img)
        except Exception as e:
            return f"[OCR 不可用: {e}]"

    def extract_elements(self, selector: str = None, type: str = None,
                         contains_text: str = None) -> list:
        self.launch()
        js_selector = selector or {
            "输入框": "input, textarea", "按钮": "button, [role=button], input[type=submit]",
            "链接": "a[href]", "图片": "img", "表格": "table",
        }.get(type, "a[href]")
        rows = self.page.evaluate(
            """(sel) => Array.from(document.querySelectorAll(sel)).slice(0, 200).map(el => ({
                tag: el.tagName.toLowerCase(),
                text: (el.innerText || el.value || el.alt || el.title || '').trim().slice(0, 120),
                href: el.href || null,
                id: el.id || null,
                class: (typeof el.className === 'string') ? el.className : null,
            }))""",
            js_selector,
        )
        if contains_text:
            rows = [r for r in rows if contains_text in (r["text"] or "")]
        return rows

    def extract_tables(self) -> list:
        self.launch()
        return self.page.evaluate(
            """() => Array.from(document.querySelectorAll('table')).map(t =>
                Array.from(t.querySelectorAll('tr')).map(tr =>
                    Array.from(tr.querySelectorAll('th, td')).map(c => (c.innerText||'').trim())
                ).filter(r => r.length)
            )"""
        )

    def extract_links(self) -> list:
        return self.extract_elements(selector="a[href]")

    def extract_forms(self) -> list:
        self.launch()
        return self.page.evaluate(
            """() => Array.from(document.querySelectorAll('input, textarea, select')).map(el => ({
                name: el.name || el.id || '',
                type: el.type || el.tagName.toLowerCase(),
                placeholder: el.placeholder || '',
                value: el.value || '',
            }))"""
        )

    def get_cookies(self) -> list:
        self.launch()
        try:
            return [{"name": c.get("name"), "domain": c.get("domain")}
                    for c in self.page.context.cookies()]
        except Exception:
            return []

    def scroll_position(self) -> dict:
        self.launch()
        return self.page.evaluate("() => ({ x: window.scrollX, y: window.scrollY })")

    # ── 交互 ──

    def click(self, selector: str = None, text: str = None,
              coords: list = None, match_result: dict = None):
        self.launch()
        if match_result and match_result.get("found"):
            self.page.mouse.click(match_result["center"][0], match_result["center"][1])
        elif selector:
            self.page.locator(selector).first.click()
        elif text:
            self.page.get_by_text(text).first.click()
        elif coords:
            self.page.mouse.click(int(coords[0]), int(coords[1]))
        else:
            raise ValueError("click 需要 selector / text / coords / match_result 之一")

    def fill(self, selector: str, value: str, mask: bool = False):
        self.launch()
        self.page.locator(selector).first.fill(value)
        return {"masked": bool(mask)} if mask else {}

    def clear(self, selector: str):
        self.launch()
        self.page.locator(selector).first.fill("")

    def scroll(self, direction: str = "下", distance: int = 500,
               to_end: bool = False, element: str = None,
               to_center: bool = False):
        self.launch()
        if element:
            el = self.page.locator(element).first
            if to_center:
                el.scroll_into_view_if_needed()
            else:
                delta = {"上": -distance, "下": distance}.get(direction, distance)
                el.evaluate(f"(el) => el.scrollBy(0, {delta})")
            return
        if to_end:
            self.page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        else:
            delta = {"上": -distance, "下": distance}.get(direction, distance)
            self.page.evaluate(f"() => window.scrollBy(0, {delta})")

    def select_option(self, selector: str, value: str):
        self.launch()
        self.page.locator(selector).first.select_option(value)

    def check(self, selector: str, checked: bool = True):
        self.launch()
        if checked:
            self.page.locator(selector).first.check()
        else:
            self.page.locator(selector).first.uncheck()

    def hover(self, selector: str):
        self.launch()
        self.page.locator(selector).first.hover()

    def keypress(self, key: str):
        self.launch()
        self.page.keyboard.press(key)

    def wait(self, condition: str = None, selector: str = None,
             seconds: float = None):
        self.launch()
        if seconds:
            time.sleep(seconds)
        elif selector:
            self.page.wait_for_selector(selector, timeout=30000)
        elif condition == "页面加载完成":
            self.page.wait_for_load_state("networkidle")

    def go_back(self):
        self.launch()
        self.page.go_back()

    def go_forward(self):
        self.launch()
        self.page.go_forward()

    def reload(self):
        self.launch()
        self.page.reload()

    def execute_js(self, script: str):
        self.launch()
        return self.page.evaluate(script)
