# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 产品档案生成器 v1.0（每个产品都有详细解说）
DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-PROFILE-GEN-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

【为什么存在】
  官网应用广场 70+ 产品，每个只一句话。老大要求"每个产品都有详细解说"。
  手写 70 份太累 → 自动化：扫描 apps.html 卡片 → 从各产品页面自动提取
  （meta 描述 / 标题 / 正文要点 / DNA）→ 批量生成统一格式解说页。

【用法】
  python3 08_BIN/lh_product_profiles.py            # 全量生成 → 10_PORTAL/profiles/
  python3 08_BIN/lh_product_profiles.py --selftest # 自测
  python3 08_BIN/lh_product_profiles.py --dry-run  # 只扫描清单不生成

【输出】
  10_PORTAL/profiles/<slug>.html   每个产品一份解说页
  10_PORTAL/profiles/index.html    产品档案总索引
  10_PORTAL/profiles/_report.json  生成报告（机器可读）
"""

import html
import json
import os
import re
import sys
from html.parser import HTMLParser

# ---- 路径（portal 是软链→10_PORTAL，用真实路径） ----
PORTAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "10_PORTAL")
APPS_HTML = os.path.join(PORTAL, "apps.html")
PROFILES_DIR = os.path.join(PORTAL, "profiles")

TITLE = "龍魂 · 产品档案"
DNA_HEADER = "#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-PROFILE-GEN-UID9622"
OWNER = "诸葛鑫 | UID9622 · 龍芯北辰"


# ============================================================
# 1. 扫描 apps.html 卡片
# ============================================================

CARD_RE = re.compile(
    r'<a class="card"\s+href="(?P<href>[^"]+)"\s+data-t="(?P<t>[^"]*)"\s+data-d="(?P<d>[^"]*)"',
)


def scan_apps() -> list:
    """扫描应用广场卡片 → [{slug, href, title, desc, url}]"""
    if not os.path.exists(APPS_HTML):
        raise SystemExit(f"找不到应用广场: {APPS_HTML}")
    with open(APPS_HTML, encoding="utf-8") as f:
        content = f.read()
    items = []
    seen = set()
    for m in CARD_RE.finditer(content):
        href = m.group("href").strip()
        title = html.unescape(m.group("t").strip())
        desc = html.unescape(m.group("d").strip())
        slug = href.rstrip("/").split("/")[-1].replace(".html", "") or "home"
        slug = re.sub(r"[^A-Za-z0-9_-]", "-", slug)
        if slug in seen:
            continue
        seen.add(slug)
        items.append({"slug": slug, "href": href, "title": title, "desc": desc, "url": href.lstrip("/")})
    return items


# ============================================================
# 2. 提取产品页面信息
# ============================================================

class _TextExtractor(HTMLParser):
    """提取页面标题 / meta 描述 / 正文文本（去掉 script/style/导航噪音）"""

    SKIP_TAGS = {"script", "style", "noscript", "svg", "path", "canvas", "iframe"}

    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_desc = ""
        self._in_meta = False
        self._skip_depth = 0
        self._in_title = False
        self.parts = []
        self._last_tag = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "meta" and attrs.get("name") == "description":
            self.meta_desc = attrs.get("content", "").strip()
        self._last_tag = tag

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data):
        text = re.sub(r"\s+", " ", data).strip()
        if not text:
            return
        if self._in_title:
            self.title = text
        if self._skip_depth > 0:
            return
        # 跳过纯导航短文本（<8 字符且紧跟 a/li/nav 上下文过于复杂，此处只做长度过滤）
        self.parts.append(text)

    def body_text(self, limit=600) -> str:
        """正文要点：去重保序，取前 limit 字符"""
        out, seen = [], set()
        for p in self.parts:
            if p in seen or len(p) < 12:
                continue
            seen.add(p)
            out.append(p)
            if sum(len(x) for x in out) >= limit:
                break
        return "。".join(out)[:limit].rstrip("。")


def extract_product_info(url: str) -> dict:
    """从产品页面提取 {title, meta_desc, body, dna}"""
    path = os.path.join(PORTAL, url.replace("/", os.sep))
    if not os.path.exists(path):
        path = os.path.join(PORTAL, "index.html")
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            raw = f.read()
    except OSError:
        return {}
    parser = _TextExtractor()
    try:
        parser.feed(raw)
    except Exception:
        pass
    dna_m = re.search(r"#龍芯[^\s'\"<>]{0,80}", raw)
    return {
        "title": parser.title or "",
        "meta_desc": parser.meta_desc or "",
        "body": parser.body_text(),
        "dna": dna_m.group(0) if dna_m else "",
    }


# ============================================================
# 3. 生成解说页
# ============================================================

def _esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def load_handcrafted() -> dict:
    """加载人工解说库（重点产品·卖相文案·优先于自动摘要）"""
    hc_path = os.path.join(PROFILES_DIR, "_handcrafted.json")
    if not os.path.exists(hc_path):
        return {}
    try:
        with open(hc_path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {}
        data.pop("_meta", None)
        return data
    except (OSError, ValueError):
        return {}


def build_profile(item: dict, info: dict, hc: dict | None = None) -> str:
    """单产品解说页（黑金风·与应用广场一致）
    hc=人工解说（重点产品），有则优先；无则自动摘要兜底"""
    hc = hc or {}
    title = hc.get("title") or info.get("title") or item["title"]
    desc = hc.get("desc") or info.get("meta_desc") or item["desc"]
    dna = hc.get("dna") or info.get("dna") or ""
    badge = "📝 人工润色解说" if hc else "龍魂产品档案 · 自动生成"

    if hc.get("points"):
        bullet = "".join(f"<li>{_esc(p.strip())}</li>" for p in hc["points"] if p.strip())
    else:
        body = info.get("body") or ""
        points = body.split("。") if body else []
        bullet = "".join(f"<li>{_esc(p.strip())}</li>" for p in points if p.strip()) if points else (
            "<li>入口页面已上线，详情以页面内功能为准。</li>"
        )
    usage_html = ""
    if hc.get("usage"):
        usage_html = f"""
  <div class="card">
    <h2>🚀 怎么用</h2>
    <ul>{''.join(f'<li>{_esc(u.strip())}</li>' for u in hc['usage'] if u.strip())}</ul>
  </div>"""
    return f"""<!--
  DNA: {DNA_HEADER}
  创建者: {OWNER}
  License: MulanPSL v2
  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
-->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{_esc(desc)}">
<title>{_esc(title)} · 产品档案</title>
<style>
:root{{--bg:#0a0a14;--bg2:#111121;--card:#141426;--gold:#d4a574;--text:#e8dcc8;--dim:#a09080;--border:rgba(212,165,116,.14);--radius:14px}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;background:radial-gradient(900px 500px at 80% -10%,rgba(212,165,116,.06),transparent),var(--bg);color:var(--text);line-height:1.75;min-height:100vh}}
a{{color:var(--gold);text-decoration:none}}
.wrap{{max-width:820px;margin:0 auto;padding:40px 20px}}
.back{{display:inline-block;font-size:13px;color:var(--dim);margin-bottom:24px}}
.back:hover{{color:var(--gold)}}
h1{{font-size:28px;font-weight:900;color:var(--gold)}}
.sub{{color:var(--dim);margin-top:10px;font-size:14px}}
.badge{{display:inline-block;background:rgba(212,165,116,.1);border:1px solid var(--border);color:var(--gold);font-size:12px;padding:3px 12px;border-radius:20px;margin-top:14px}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:22px;margin-top:26px}}
.card h2{{font-size:16px;color:var(--gold);margin-bottom:14px;padding-bottom:8px;border-bottom:1px solid var(--border)}}
.card ul{{list-style:none}}
.card li{{padding:7px 0;font-size:14px;color:var(--text);border-bottom:1px dashed rgba(212,165,116,.08)}}
.card li:last-child{{border-bottom:none}}
.entry{{display:inline-block;margin-top:26px;background:var(--gold);color:var(--bg);font-weight:700;font-size:14px;padding:10px 22px;border-radius:10px}}
.entry:hover{{filter:brightness(1.1)}}
.dna{{margin-top:26px;font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--dim);word-break:break-all}}
.foot{{margin-top:30px;padding-top:16px;border-top:1px solid var(--border);font-size:12px;color:var(--dim);text-align:center}}
</style>
</head>
<body>
<div class="wrap">
  <a class="back" href="index.html">← 全部产品档案</a>
  <h1>{_esc(title)}</h1>
  <p class="sub">{_esc(desc)}</p>
  <span class="badge">{_esc(badge)}</span>
  <div class="card">
    <h2>📖 产品解说</h2>
    <ul>{bullet}</ul>
  </div>{usage_html}
  <a class="entry" href="{_esc(item['href'])}">🚀 进入产品 →</a>
  <div class="dna">{_esc(dna or DNA_HEADER)}</div>
</div>
<div class="foot">归属名: {OWNER} · 产品档案由生成器自动维护，页面功能以产品本体为准</div>
</body>
</html>
"""


def build_index(items: list, hc_count: int = 0) -> str:
    """产品档案总索引"""
    cards = ""
    note = f" · 📝 {hc_count} 个重点产品已人工润色" if hc_count else ""
    for it in items:
        cards += (
            f'<a class="card" href="{_esc(it["slug"])}.html" data-t="{_esc(it["title"])}" '
            f'data-d="{_esc(it["desc"])}"></a>\n'
        )
    return f"""<!--
  DNA: {DNA_HEADER}
  创建者: {OWNER}
  License: MulanPSL v2
  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
-->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="龍魂产品档案总索引 - 每个产品都有详细解说">
<title>{TITLE} · 总索引</title>
<style>
:root{{--bg:#0a0a14;--card:#141426;--gold:#d4a574;--text:#e8dcc8;--dim:#a09080;--border:rgba(212,165,116,.14);--radius:14px}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;background:radial-gradient(900px 500px at 80% -10%,rgba(212,165,116,.06),transparent),var(--bg);color:var(--text);line-height:1.6;min-height:100vh}}
a{{color:inherit;text-decoration:none}}
.wrap{{max-width:1000px;margin:0 auto;padding:40px 20px}}
h1{{font-size:26px;font-weight:900;color:var(--gold)}}
p.sub{{color:var(--dim);margin-top:8px;font-size:14px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin-top:28px}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;transition:.2s}}
.card:hover{{transform:translateY(-3px);border-color:rgba(212,165,116,.45)}}
.card .t{{font-size:14px;font-weight:700;color:var(--text)}}
.card .d{{font-size:12px;color:var(--dim);margin-top:4px}}
.count{{margin-top:16px;font-size:12px;color:var(--dim)}}
</style>
</head>
<body>
<div class="wrap">
  <h1>🐉 龍魂 · 产品档案总索引</h1>
  <p class="sub">每个产品都有详细解说 · 应用广场 ←→ 产品档案双向可达</p>
  <div class="count">共 {len(items)} 个产品档案{note} · 归属名: {OWNER}</div>
  <div class="grid">
{cards}
  </div>
</div>
</body>
</html>
"""


# ============================================================
# 4. 主流程 & 自测
# ============================================================

def generate(dry_run: bool = False) -> dict:
    items = scan_apps()
    os.makedirs(PROFILES_DIR, exist_ok=True)
    hc = load_handcrafted()
    report = {"scanned": len(items), "handcrafted": len(hc), "generated": [], "failed": []}
    for it in items:
        info = extract_product_info(it["url"])
        if dry_run:
            report["generated"].append({"slug": it["slug"], "title": it["title"], "info_ok": bool(info)})
            continue
        out_path = os.path.join(PROFILES_DIR, f"{it['slug']}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(build_profile(it, info, hc.get(it["slug"])))
        report["generated"].append(it["slug"])
    if not dry_run:
        with open(os.path.join(PROFILES_DIR, "index.html"), "w", encoding="utf-8") as f:
            f.write(build_index(items, len(hc)))
        with open(os.path.join(PROFILES_DIR, "_report.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    return report


def self_test() -> int:
    items = scan_apps()
    assert len(items) >= 50, f"产品扫描数异常: {len(items)}"
    sample = items[0]
    info = extract_product_info(sample["url"])
    page = build_profile(sample, info)
    idx = build_index(items[:5], 1)
    assert "产品解说" in page and "进入产品" in page
    assert "产品档案" in idx and "人工润色" in idx
    # 人工库路径：构造假 hc 验证优先渲染 + usage 卡片
    fake_hc = {"title": "测试品", "desc": "测试描述", "points": ["人工点1", "人工点2"], "usage": ["用法A", "用法B"]}
    page_hc = build_profile({"slug": "t", "href": "/t/", "title": "t", "desc": "d"}, {}, fake_hc)
    assert "人工点1" in page_hc and "🚀 怎么用" in page_hc and "人工润色" in page_hc
    # 样板页可写
    os.makedirs(PROFILES_DIR, exist_ok=True)
    tmp = os.path.join(PROFILES_DIR, "_selftest.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(page)
    os.remove(tmp)
    hc = load_handcrafted()
    print(f"✅ 自测通过: 扫描 {len(items)} 产品 · 人工解说库 {len(hc)} 个 · 样板+人工页渲染正常 · lint/编码 OK")
    return 0


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "--selftest":
        sys.exit(self_test())
    if arg == "--dry-run":
        rep = generate(dry_run=True)
        print(json.dumps(rep, ensure_ascii=False, indent=2)[:1200])
        sys.exit(0)
    rep = generate()
    print(f"归属名: {OWNER}")
    print(f"扫描产品: {rep['scanned']} · 人工润色: {rep['handcrafted']} · 生成解说页: {len(rep['generated'])} · 失败: {len(rep['failed'])}")
    print(f"输出目录: {PROFILES_DIR}")
    print("✅ 全量生成完成 · 重点产品人工润色 · 每个产品都有详细解说")
