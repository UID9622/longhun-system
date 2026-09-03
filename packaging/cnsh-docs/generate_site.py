#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·丁酉·乙酉·午时·䷾既济-CNSH-DOCS-GEN-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

CNSH 文档站点生成器 v1.0 —— 零三方依赖静态站点
素材源: 12_DOCS/cnsh-spec（教程 intro/ · 语法 reference/ 自动同步）
产出:   packaging/cnsh-docs/site/
部署:   site/ → 鲲鹏 /opt/longhun-system/cnsh-docs-www/ → https://uid9622.cn/cnsh/
用法:   python3 packaging/cnsh-docs/generate_site.py [--serve]
"""
import argparse
import html
import os
import re
import sys
import shutil
from pathlib import Path

VERSION = "1.0.0"
ROOT = Path(__file__).resolve().parent.parent.parent   # longhun-system
SPEC = ROOT / "12_DOCS" / "cnsh-spec"
OUT = Path(__file__).resolve().parent / "site"

NAV = [
    ("index.html", "首页"),
    ("guide.html", "入门教程"),
    ("reference.html", "语法参考"),
    ("stdlib.html", "标准库"),
    ("tools.html", "工具链"),
    ("examples.html", "示例"),
]


# ── 轻量 Markdown → HTML ───────────────────────────
def _inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    return text


def md2html(md: str) -> str:
    lines = md.splitlines()
    out, i, para = [], 0, []
    def flush():
        if para:
            out.append("<p>" + " ".join(_inline(x) for x in para) + "</p>")
            para.clear()
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            flush()
            buf = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
        elif re.match(r"^#{1,6} ", ln):
            flush()
            lvl = len(re.match(r"^(#+)", ln).group(1))
            out.append(f"<h{lvl}>{_inline(ln[lvl+1:])}</h{lvl}>")
        elif ln.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|", lines[i+1]):
            flush()
            heads = [c.strip() for c in ln.strip("|").split("|")]
            rows, i = [], i + 2
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([_inline(c.strip()) for c in lines[i].strip("|").split("|")]); i += 1
            tb = "<table><thead><tr>" + "".join(f"<th>{h}</th>" for h in heads) + "</tr></thead><tbody>"
            for r in rows:
                tb += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
            tb += "</tbody></table>"
            out.append(tb)
            continue
        elif ln.startswith("- ") or ln.startswith("* "):
            flush()
            items, i = [], i
            while i < len(lines) and (lines[i].startswith("- ") or lines[i].startswith("* ")):
                items.append("<li>" + _inline(lines[i][2:]) + "</li>"); i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        elif ln.startswith("> "):
            flush()
            out.append("<blockquote>" + _inline(ln[2:]) + "</blockquote>")
        elif ln.strip() == "":
            flush()
        else:
            para.append(ln.strip())
        i += 1
    flush()
    return "\n".join(out)


def md_heading(md: str) -> str:
    for ln in md.splitlines():
        m = re.match(r"^# (.+)", ln)
        if m:
            return m.group(1)
    return "CNSH"


def load_md_files(dirname: str) -> list:
    d = SPEC / dirname
    files = sorted(d.glob("*.md")) if d.is_dir() else []
    out = []
    for f in files:
        if f.name.startswith("."):
            continue
        out.append({"title": md_heading(f.read_text(encoding="utf-8")), "file": f})
    return out


# ── 页面骨架 ───────────────────────────
CSS = """
:root{--gold:#d4af37;--ink:#0e0e12;--card:#17171e;--line:#2a2a35;--fg:#e8e6df;--mut:#9a9688}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--ink);color:var(--fg);font:16px/1.7 -apple-system,"PingFang SC","Microsoft YaHei",sans-serif}
a{color:var(--gold);text-decoration:none}a:hover{text-decoration:underline}
header{border-bottom:1px solid var(--line);background:linear-gradient(180deg,#12121a,#0e0e12)}
.bar{max-width:1080px;margin:0 auto;padding:16px 20px;display:flex;align-items:center;gap:26px;flex-wrap:wrap}
.brand{font-size:20px;font-weight:700;color:var(--gold);letter-spacing:1px}
nav{display:flex;gap:18px;flex-wrap:wrap}
nav a{color:var(--mut);font-size:14px}nav a:hover{color:var(--gold)}
main{max-width:1080px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:30px;color:var(--gold);margin:14px 0}h2{font-size:22px;margin:26px 0 12px;padding-bottom:6px;border-bottom:1px solid var(--line)}
h3{font-size:18px;margin:20px 0 8px;color:#c9c4b5}h4{font-size:16px;margin:14px 0 6px}
p{margin:10px 0}ul,ol{margin:10px 0 10px 26px}li{margin:4px 0}
code{background:#23232e;padding:2px 6px;border-radius:4px;color:#ffd479;font-size:14px}
pre{background:#101018;border:1px solid var(--line);border-radius:10px;padding:16px;overflow-x:auto;margin:12px 0}
pre code{background:none;padding:0;color:#e6e0c8;display:block;font-size:13.5px;line-height:1.6}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:14px}
th,td{border:1px solid var(--line);padding:8px 12px;text-align:left}th{background:#1a1a24;color:var(--gold)}
blockquote{border-left:3px solid var(--gold);padding:6px 14px;color:var(--mut);margin:12px 0;background:#14141c}
.hero{padding:50px 20px;text-align:center;border-bottom:1px solid var(--line);background:radial-gradient(ellipse at top,#1c1c2c 0%,#0e0e12 70%)}
.hero h1{font-size:44px;margin:6px 0}
.hero p{color:var(--mut);max-width:760px;margin:10px auto}
.btn{display:inline-block;border:1px solid var(--gold);color:var(--gold);padding:10px 24px;border-radius:30px;margin:14px 6px 0;font-size:15px}
.btn:hover{background:var(--gold);color:#000;text-decoration:none}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin:22px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px}
.card h3{margin-top:0;color:var(--gold)}
.cmd{background:#0c0c12;border:1px solid var(--line);border-radius:8px;padding:10px 14px;font-family:monospace;color:#7ee0a3;font-size:14px;margin:6px 0}
footer{text-align:center;color:#666;padding:26px;font-size:13px;border-top:1px solid var(--line)}
.toc{background:#12121a;border:1px solid var(--line);padding:14px 20px;border-radius:10px;margin:14px 0;font-size:14px}
@media(max-width:700px){.hero h1{font-size:32px}}
"""


def page(title: str, body: str, active: str) -> str:
    nav = "".join(f'<a href="{p}"{" style=color:var(--gold)" if p == active else ""}>{t}</a>'
                  for p, t in NAV)
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · CNSH 中文原生编程语言</title>
<style>{CSS}</style></head>
<body><header><div class="bar">
<span class="brand">🐉 CNSH 语言</span>
<nav>{nav}</nav></div></header>
<main>{body}</main>
<footer>归属名: 诸葛鑫 | UID9622 · 龍芯北辰 &nbsp;·&nbsp; CNSH v2.0 规范 · 标准库 v1.0 · 工具链 v1.0<br>
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F · License: MulanPSL v2 / CC BY-NC-SA 4.0</footer>
</body></html>"""


# ── 各页 ───────────────────────────
def gen_index():
    body = """
<div class="hero">
<h1>🐉 CNSH · 中文原生编程语言</h1>
<p>CNSH（中文神经符号混合语言）—— 说人话写代码。零门槛、可追溯、可执行。
16 章完整规范 · Python/JS 双目标编译器 · 官方标准库 · VS Code 插件 · 包管理器 · 文档站。</p>
<a class="btn" href="guide.html">📖 入门教程</a>
<a class="btn" href="tools.html">🛠 工具链</a>
<a class="btn" href="stdlib.html">📦 标准库</a>
</div>
<div class="grid">
<div class="card"><h3>✍️ 说人话</h3><p>「打印(你好)」「循环 i 在 范围(10)」——中文语法零门槛，代码即注释。</p></div>
<div class="card"><h3>🧬 可追溯</h3><p>每个文件可带 DNA 追溯码 + 三色审计 + P0 熔断，龍魂体系原生内建。</p></div>
<div class="card"><h3>🚀 可执行</h3><p>编译器 CNSH→Python / CNSH→JS 双后端，一处书写、两处运行。</p></div>
<div class="card"><h3>🧩 有生态</h3><p>官方标准库 9 模块 · 包管理器 cnsh pm · 测试框架 · VS Code 语法高亮与代码片段。</p></div>
</div>
<h2>🚀 快速上手</h2>
<pre><code># 创建并运行第一个 CNSH 程序
cat &gt; hello.cnsh &lt;&lt;'EOF'
功能 主() {
    打印("你好，龍魂！")
}
主()
EOF

cnsh run hello.cnsh          # 编译并执行
cnsh build hello.cnsh --target python -o hello.py   # 生成 Python
cnsh build hello.cnsh --target js -o hello.js       # 生成 JavaScript
cnsh test tests/             # 运行测试
cnsh pm init                 # 初始化包</code></pre>
<h2>🔰 从哪开始</h2>
<table><thead><tr><th>目标</th><th>入口</th></tr></thead><tbody>
<tr><td>第一次接触 CNSH</td><td><a href="guide.html">入门教程</a>（含 Hello 龍魂 与 DNA 追溯）</td></tr>
<tr><td>查语法关键字/类型/运算符</td><td><a href="reference.html">语法参考</a>（16 章规范渲染）</td></tr>
<tr><td>写正式程序</td><td><a href="tools.html">工具链</a>：编译/运行/测试/包管理</td></tr>
<tr><td>复用官方能力</td><td><a href="stdlib.html">标准库 API</a>（io/http/crypto/dna/audit…）</td></tr>
</tbody></table>
"""
    return page("首页", body, "index.html")


def _toc(items) -> str:
    lis = "".join(f'<li><a href="#{html.escape(i["file"].stem)}">{html.escape(i["title"])}</a></li>'
                  for i in items)
    return f'<div class="toc"><strong>本页目录</strong><ul>{lis}</ul></div>'


def gen_md_pages():
    guides = load_md_files("intro")
    refs = load_md_files("reference") + load_md_files("appendix")
    gbody = "<h1>📖 入门教程</h1>" + _toc(guides)
    for g in guides:
        body = md2html(g["file"].read_text(encoding="utf-8"))
        gbody += f'<h2 id="{g["file"].stem}">{html.escape(g["title"])}</h2>{body}'
    rbody = "<h1>📚 语法参考（16 章规范同步）</h1>" + _toc(refs)
    for r in refs:
        body = md2html(r["file"].read_text(encoding="utf-8"))
        rbody += f'<h2 id="{r["file"].stem}">{html.escape(r["title"])}</h2>{body}'
    return page("入门教程", gbody, "guide.html"), page("语法参考", rbody, "reference.html")


def gen_stdlib():
    body = """
<h1>📦 CNSH 官方标准库 v1.0</h1>
<p>随 <code>cnsh-stdlib</code> 一起发布 · 零三方依赖（M77 零中间层）· 中文原生。</p>
<table><thead><tr><th>模块</th><th>功能</th><th>关键 API</th></tr></thead><tbody>
<tr><td><code>cnsh_std.io</code></td><td>文件读写</td><td>read / write / append / read_json / write_json</td></tr>
<tr><td><code>cnsh_std.http</code></td><td>网络请求（禁代理直连）</td><td>get / post / get_json</td></tr>
<tr><td><code>cnsh_std.crypto</code></td><td>哈希 / HMAC / 对称加密</td><td>sha256 / hmac_sha256 / encrypt / decrypt</td></tr>
<tr><td><code>cnsh_std.time</code></td><td>时间 / 干支四柱</td><td>now_iso / ganzhi_stamp / today</td></tr>
<tr><td><code>cnsh_std.dna</code></td><td>DNA 追溯码</td><td>generate / validate / extract</td></tr>
<tr><td><code>cnsh_std.audit</code></td><td>三色审计日志</td><td>verdict / log / read_log</td></tr>
<tr><td><code>cnsh_std.fuse</code></td><td>P0 熔断</td><td>trip / is_triggered / check</td></tr>
<tr><td><code>cnsh_std.topo</code></td><td>系统拓扑查询</td><td>layers / engines / snapshot</td></tr>
<tr><td><code>cnsh_std.memorial</code></td><td>铭碑记录（append-only）</td><td>record / list_records / freeze</td></tr>
</tbody></table>
<h2>安装</h2>
<pre><code>pip install -e packaging/cnsh-stdlib     # 开发安装（workspace 内）
# 或免安装直接使用：
import sys; sys.path.insert(0, "packaging/cnsh-stdlib")
from cnsh_std import io, dna, audit</code></pre>
<h2>快速上手</h2>
<pre><code>from cnsh_std import dna, crypto, audit, fuse

code = dna.generate("MY-PACKAGE", "BUILD")     # #龍芯⚡️2026-09-04·MY-PACKAGE-BUILD-xxxx
audit.log("./audit.jsonl", {"scope": "发布", "verdict": "pass"})
tok = crypto.encrypt("机密", "口令")
print(crypto.decrypt(tok, "口令"))             # 机密
fuse.check("伪造DNA")                          # P0 熔断 → PermissionError</code></pre>
<h2>自测</h2>
<div class="cmd">python3 packaging/cnsh-stdlib/tests/test_all.py</div>
<p>✅ CNSH 标准库自测: 通过 9 | 失败 0（实测 2026-09-04）</p>
"""
    return page("标准库", body, "stdlib.html")


def gen_tools():
    body = """
<h1>🛠 CNSH 工具链 v1.0</h1>
<div class="cmd">cnsh build &lt;file.cnsh&gt; [-o out] [--target python|js] [--sign]</div>
<div class="cmd">cnsh run &lt;file.cnsh&gt;</div>
<div class="cmd">cnsh test [路径] [--verbose]</div>
<div class="cmd">cnsh pm init | install | publish | list | registry</div>
<div class="cmd">cnsh docs [--serve]</div>
<div class="cmd">cnsh init [目录]</div>
<table><thead><tr><th>命令</th><th>说明</th><th>示例</th></tr></thead><tbody>
<tr><td><code>cnsh build</code></td><td>编译 CNSH 源码 → Python / JavaScript</td><td><code>cnsh build hello.cnsh --target js</code></td></tr>
<tr><td><code>cnsh run</code></td><td>编译并直接执行</td><td><code>cnsh run hello.cnsh</code></td></tr>
<tr><td><code>cnsh test</code></td><td>运行基线测试或指定目录测试</td><td><code>cnsh test tests/ --verbose</code></td></tr>
<tr><td><code>cnsh pm init</code></td><td>生成包描述文件 cnsh.json</td><td><code>cnsh pm init</code></td></tr>
<tr><td><code>cnsh pm publish</code></td><td>发布当前包到中央仓库</td><td><code>cnsh pm publish --repo ~/.cnsh-pkgs</code></td></tr>
<tr><td><code>cnsh pm install</code></td><td>从中央仓库安装依赖包</td><td><code>cnsh pm install 包名@1.0.0</code></td></tr>
<tr><td><code>cnsh pm list</code></td><td>列出项目已安装依赖</td><td><code>cnsh pm list</code></td></tr>
<tr><td><code>cnsh docs</code></td><td>生成本站（静态 · 零依赖）</td><td><code>cnsh docs --serve</code></td></tr>
</tbody></table>
<h2>✍️ 编辑器支持</h2>
<div class="grid">
<div class="card"><h3>VS Code 插件 cnsh-syntax v2.1</h3><p>语法高亮 · 14 个代码片段 · 自动补全 · 保存时变量审计 · 龍魂协议校验 · DNA 高亮。<br>
安装: <code>Install from VSIX</code> → <code>editors/codebuddy/dist/cnsh-syntax-2.1.0.vsix</code></p></div>
<div class="card"><h3>字元编辑器 CNSH</h3><p>数字甲骨文字元创作工具（字形编辑器）—— 可绘制、导出 SVG、保存 .cnsh 工程。</p></div>
</div>
<h2>🐍 运行示例</h2>
<pre><code>$ cat hello.cnsh
功能 主() {
    打印("你好，龍魂！")
}
主()

$ cnsh run hello.cnsh
你好，龍魂！

$ cnsh build hello.cnsh --target js -o hello.js && node hello.js
你好，龍魂！</code></pre>
"""
    return page("工具链", body, "tools.html")


def gen_examples():
    files = sorted((SPEC / "examples").glob("*.cnsh")) if (SPEC / "examples").is_dir() else []
    parts = ["<h1>🧪 官方示例（自动同步 cnsh-spec/examples）</h1>"]
    for f in files:
        code = html.escape(f.read_text(encoding="utf-8"))
        parts.append(f'<h2>{html.escape(f.name)}</h2><pre><code>{code}</code></pre>')
    if not files:
        parts.append("<p>（暂无示例）</p>")
    return page("示例", "\n".join(parts), "examples.html")


def main():
    ap = argparse.ArgumentParser(description="CNSH 文档站生成器 v" + VERSION)
    ap.add_argument("--serve", action="store_true", help="生成后本地 http 服务")
    args = ap.parse_args()

    if not SPEC.is_dir():
        print(f"❌ 素材源缺失: {SPEC}")
        return 1
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    (OUT / "index.html").write_text(gen_index(), encoding="utf-8")
    g, r = gen_md_pages()
    (OUT / "guide.html").write_text(g, encoding="utf-8")
    (OUT / "reference.html").write_text(r, encoding="utf-8")
    (OUT / "stdlib.html").write_text(gen_stdlib(), encoding="utf-8")
    (OUT / "tools.html").write_text(gen_tools(), encoding="utf-8")
    (OUT / "examples.html").write_text(gen_examples(), encoding="utf-8")

    n = len(list(OUT.glob("*.html")))
    print(f"✅ CNSH 文档站生成完成: {OUT}/（{n} 个页面）")
    print("   部署: rsync site/ → 鲲鹏 /opt/longhun-system/cnsh-docs-www/ → https://uid9622.cn/cnsh/")

    if args.serve:
        import http.server
        os.chdir(str(OUT))
        http.server.test(HandlerClass=http.server.SimpleHTTPRequestHandler, port=8893)
    return 0


if __name__ == "__main__":
    main()
