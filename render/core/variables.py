# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""M75 {render.*} 变量环境 · 每次渲染的完整上下文快照。"""

import base64
import datetime
import hashlib
import json
import time
from urllib.parse import urlparse


class RenderContext:
    """渲染上下文变量容器。每个字段对应 {render.*} 命名空间。"""

    FIELDS = (
        "platform", "url", "title", "domain", "timestamp", "viewport",
        "screenshot", "screenshot_path", "dom", "ax_tree", "text",
        "elements", "tables", "links", "forms", "meta", "match", "cookies",
        "scroll_pos", "audit", "dna", "hash_rec", "error",
    )

    def __init__(self, platform: str = "web", url: str = "", **kwargs):
        self.platform = platform
        self.url = url
        self.title = None
        self.domain = urlparse(url).netloc if url else None
        self.timestamp = datetime.datetime.now().isoformat(timespec="seconds")
        self.viewport = kwargs.get("viewport") or {"width": 1920, "height": 1080}
        self.screenshot = None          # bytes (PNG)
        self.screenshot_path = None     # str 本地路径
        self.dom = None                 # dict
        self.ax_tree = None             # dict (App 用)
        self.text = None                # str
        self.elements = []              # list
        self.tables = []                # list
        self.links = []                 # list
        self.forms = []                 # list
        self.meta = {}                  # dict
        self.match = {}                 # dict 视觉匹配结果
        self.cookies = []               # list 仅本地
        self.scroll_pos = {"x": 0, "y": 0}
        self.audit = {"color": "🟡", "score": 0, "reason": "未审计"}
        self.dna = None
        self.hash_rec = None    # M73 产权哈希注册记录
        self.error = None

    # ── 序列化 ──

    def to_dict(self, with_screenshot: bool = True) -> dict:
        """转 dict。screenshot 默认 base64（供 {render.screenshot}）。"""
        d = {}
        for f in self.FIELDS:
            v = getattr(self, f)
            if f == "screenshot" and v and with_screenshot:
                if isinstance(v, (bytes, bytearray)):
                    d[f] = base64.b64encode(v).decode("ascii")
                else:
                    d[f] = v
            else:
                d[f] = v
        return d

    def to_json(self, with_screenshot: bool = True, indent: int = 2) -> str:
        return json.dumps(self.to_dict(with_screenshot), ensure_ascii=False,
                          indent=indent, default=str)

    # ── DNA ──

    def generate_dna(self, uid: str = "UID9622") -> str:
        """生成唯一 DNA：SHA256(url+timestamp+content)[:8]。"""
        content = f"{self.url}|{self.timestamp}|{(self.text or '')[:512]}"
        h = hashlib.sha256(content.encode("utf-8")).hexdigest()[:8].upper()
        date = datetime.date.today().isoformat()
        self.dna = f"#龍芯⚡️{date}-RENDER-{h}-{uid}"
        return self.dna

    # ── 便捷 ──

    def set_screenshot(self, data: bytes, path: str = None) -> None:
        self.screenshot = data
        self.screenshot_path = path

    def register(self, render_key: str) -> str:
        """返回变量环境引用表达式，例如 {render.url}。"""
        return "{" + f"render.{render_key}" + "}"

    def __repr__(self):
        return f"<RenderContext {self.platform} {self.url} dna={self.dna or '-'}>"
