#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 中国文化章节独立页面生成器
读取 中国文化章节.json，批量生成带真实视觉不动点的独立 HTML 页面。
DNA: #龍芯⚡️2026-07-04-LONGHUN-CHAPTER-PAGES-v1.0
"""

import json
import html
import time
import hashlib
from pathlib import Path

DNA = "#龍芯⚡️2026-07-04-LONGHUN-CHAPTER-PAGES-v1.0"
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "api" / "data"
CHAPTER_FILE = DATA_DIR / "中国文化章节.json"
P0_DIR = BASE_DIR / "p0-controls"
TEMPLATE_FILE = P0_DIR / "龍魂-章节模板.html"
CHANGE_LOG = BASE_DIR / "api" / "assets" / "cultural" / "cultural_change_log.jsonl"


def ts():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())


def log_change(action, target, detail):
    entry = {
        "timestamp": ts(),
        "dna": DNA,
        "action": action,
        "target": target,
        "detail": detail
    }
    with open(CHANGE_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def page_dna(cid, system_dna):
    h = hashlib.sha256(f"{system_dna}-{cid}-UID9622".encode()).hexdigest()[:12].upper()
    return f"#龍芯⚡️{time.strftime('%Y-%m-%d')}-CHAPTER-PAGE-{cid.upper()}-{h}-v1.0"


def build_html(ch, system_dna):
    cid = ch["id"]
    title = html.escape(ch["title"])
    subtitle = html.escape(ch["subtitle"])
    era = html.escape(ch.get("era", ""))
    era_en = html.escape(ch.get("era_en", ""))
    visual_theme = html.escape(ch.get("visual_theme", ""))
    classical = html.escape(ch["classical_text"])
    modern = html.escape(ch["modern_text"])
    voice = html.escape(ch["voice_script"])
    seal = html.escape(ch.get("seal_text", ""))
    fonts = html.escape(ch.get("font_family", "Noto Serif SC"))
    primary = html.escape(ch.get("color_primary", "#4a0000"))
    secondary = html.escape(ch.get("color_secondary", "#d4af37"))
    attribution = html.escape(ch.get("attribution", ""))
    figure = ch.get("figure_image", {})
    background = ch.get("background_image", {})
    figure_path = html.escape(figure.get("local", ""))
    bg_path = html.escape(background.get("local", ""))
    immutable = ch.get("immutable_points", [])
    change_log = ch.get("change_log", [])
    dna = page_dna(cid, system_dna)
    anchor_dna = html.escape(ch.get("visual_anchor_dna", system_dna))
    system_dna_plain = html.escape(system_dna.lstrip("#"))

    imm_list = "\n".join(
        f'<li><span class="imm-marker">◆</span>{html.escape(p)}</li>'
        for p in immutable
    )

    change_list = "\n".join(
        f'<li><span class="log-time">{html.escape(c.get("timestamp", ""))}</span> · {html.escape(c.get("action", ""))}</li>'
        for c in change_log
    )

    return f'''<!--{dna} 自动注入·中国文化章节独立页·来源可查-->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · 龍魂知识矩阵 · UID9622</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E🐉%3C/text%3E%3C/svg%3E">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{{
  --primary:{primary};
  --secondary:{secondary};
  --paper:#f7f3e8;
  --ink:#1a1a1a;
  --seal:#8b0000;
  --font:"Noto Serif SC", "Songti SC", serif;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{
  min-height:100%;
  font-family:var(--font);
  color:var(--ink);
  background:var(--paper);
}}
body{{
  background-image:url("../../api/{bg_path}");
  background-size:cover;
  background-position:center;
  background-attachment:fixed;
  background-repeat:no-repeat;
}}
body::before{{
  content:"";
  position:fixed;
  inset:0;
  background:linear-gradient(180deg, rgba(247,243,232,0.92) 0%, rgba(247,243,232,0.82) 100%);
  z-index:-1;
}}
.container{{
  max-width:900px;
  margin:0 auto;
  padding:40px 20px 80px;
}}
.topbar{{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:30px;
  padding-bottom:15px;
  border-bottom:1px solid rgba(74,0,0,0.15);
}}
.back-link{{
  color:var(--primary);
  text-decoration:none;
  font-size:15px;
}}
.back-link:hover{{text-decoration:underline}}
.era-badge{{
  font-size:13px;
  color:#666;
  border:1px solid rgba(74,0,0,0.2);
  padding:4px 12px;
  border-radius:20px;
}}
.seal-stamp{{
  width:90px;
  height:90px;
  margin:0 auto 25px;
  background:var(--seal);
  border-radius:12px;
  display:flex;
  align-items:center;
  justify-content:center;
  color:#f7f3e8;
  font-size:32px;
  font-weight:bold;
  letter-spacing:2px;
  box-shadow:0 4px 14px rgba(139,0,0,0.3);
  border:3px solid rgba(212,175,55,0.5);
}}
.title-block{{
  text-align:center;
  margin-bottom:35px;
}}
.title-block h1{{
  font-size:42px;
  color:var(--primary);
  margin-bottom:10px;
  font-weight:700;
  letter-spacing:4px;
}}
.title-block .subtitle{{
  font-size:18px;
  color:#555;
  letter-spacing:2px;
}}
.title-block .theme{{
  margin-top:12px;
  font-size:14px;
  color:var(--secondary);
  font-weight:600;
}}
.figure-card{{
  background:rgba(255,255,255,0.65);
  border:1px solid rgba(74,0,0,0.12);
  border-radius:8px;
  padding:20px;
  margin-bottom:30px;
  text-align:center;
  box-shadow:0 4px 20px rgba(0,0,0,0.05);
}}
.figure-card img{{
  max-width:100%;
  height:auto;
  border-radius:6px;
  border:1px solid rgba(74,0,0,0.1);
}}
.figure-card .caption{{
  margin-top:12px;
  font-size:13px;
  color:#666;
}}
.scroll-card{{
  background:rgba(255,255,255,0.78);
  border-left:5px solid var(--primary);
  border-radius:0 10px 10px 0;
  padding:28px;
  margin-bottom:25px;
  box-shadow:0 4px 20px rgba(0,0,0,0.06);
}}
.scroll-card h2{{
  font-size:20px;
  color:var(--primary);
  margin-bottom:15px;
  display:flex;
  align-items:center;
  gap:8px;
}}
.scroll-card .classical{{
  font-size:18px;
  line-height:1.9;
  color:var(--ink);
  text-align:justify;
}}
.scroll-card .modern{{
  font-size:16px;
  line-height:1.8;
  color:#444;
  text-align:justify;
}}
.voice-bar{{
  display:flex;
  gap:12px;
  flex-wrap:wrap;
  margin:25px 0;
}}
.voice-bar button{{
  background:var(--primary);
  color:#fff;
  border:none;
  padding:12px 22px;
  border-radius:6px;
  font-family:inherit;
  font-size:15px;
  cursor:pointer;
  transition:opacity .2s;
}}
.voice-bar button:hover{{opacity:.85}}
.voice-bar button.secondary{{
  background:transparent;
  color:var(--primary);
  border:1px solid var(--primary);
}}
.immutable-card{{
  background:rgba(212,175,55,0.08);
  border:1px dashed var(--secondary);
  border-radius:10px;
  padding:22px;
  margin-bottom:25px;
}}
.immutable-card h2{{
  font-size:18px;
  color:var(--primary);
  margin-bottom:14px;
}}
.immutable-card ul{{
  list-style:none;
}}
.immutable-card li{{
  padding:8px 0;
  font-size:15px;
  line-height:1.7;
  border-bottom:1px solid rgba(74,0,0,0.06);
}}
.immutable-card li:last-child{{border-bottom:none}}
.imm-marker{{
  color:var(--secondary);
  margin-right:8px;
}}
.meta-footer{{
  background:rgba(255,255,255,0.7);
  border-top:1px solid rgba(74,0,0,0.1);
  padding:22px;
  border-radius:10px;
  font-size:13px;
  color:#555;
  line-height:1.8;
}}
.meta-footer h3{{
  font-size:15px;
  color:var(--primary);
  margin-bottom:10px;
}}
.meta-footer .log-list{{
  list-style:none;
  margin-top:8px;
}}
.meta-footer .log-list li{{
  padding:3px 0;
}}
.dna-line{{
  margin-top:15px;
  padding-top:15px;
  border-top:1px solid rgba(74,0,0,0.1);
  font-family:monospace;
  font-size:12px;
  color:#777;
  word-break:break-all;
}}
@media (max-width:600px){{
  .title-block h1{{font-size:30px}}
  .scroll-card{{padding:18px}}
}}
</style>
</head>
<body>
<div class="container">
  <div class="topbar">
    <a class="back-link" href="龍魂知识矩阵-沉浸式AI播音员.html">← 返回龍魂知识矩阵</a>
    <span class="era-badge">{era} · {era_en}</span>
  </div>

  <div class="seal-stamp">{seal}</div>

  <div class="title-block">
    <h1>{title}</h1>
    <div class="subtitle">{subtitle}</div>
    <div class="theme">{visual_theme}</div>
  </div>

  <div class="figure-card">
    <img src="../../api/{figure_path}" alt="{title}配图">
    <div class="caption">{visual_theme} · 占位素材 · 待替换为真实公开版权图像</div>
  </div>

  <div class="voice-bar">
    <button onclick="playNarrate()">▶ 朗读本章</button>
    <button class="secondary" onclick="playClassical()">朗读古文</button>
    <button class="secondary" onclick="playModern()">朗读白话</button>
    <button class="secondary" onclick="location.href='龍魂知识矩阵-沉浸式AI播音员.html?focus={cid}'">在矩阵中查看</button>
  </div>

  <div class="scroll-card">
    <h2>📜 原文</h2>
    <p class="classical">{classical}</p>
  </div>

  <div class="scroll-card">
    <h2>💡 白话</h2>
    <p class="modern">{modern}</p>
  </div>

  <div class="immutable-card">
    <h2>⚓ 视觉不动点</h2>
    <ul>
      {imm_list}
    </ul>
  </div>

  <div class="meta-footer">
    <h3>📚 来源标注</h3>
    <p>{attribution}</p>
    <p style="margin-top:8px"><strong>推荐字体：</strong>{fonts}</p>
    <ul class="log-list">
      {change_list}
    </ul>
    <div class="dna-line" data-parent-system="{system_dna_plain}">
      页面 DNA：{dna}<br>
      不动点 DNA：{anchor_dna}<br>
      父系统 DNA：{system_dna_plain}
    </div>
  </div>
</div>

<script>
const API = "http://127.0.0.1:8766";
let currentAudio = null;

async function speak(text, voice="zh-CN-YunxiNeural"){{
  if(currentAudio){{ currentAudio.pause(); currentAudio=null; }}
  try{{
    const r = await fetch(API + "/tts", {{
      method:"POST",
      headers:{{"Content-Type":"application/json"}},
      body: JSON.stringify({{text, voice}})
    }});
    const j = await r.json();
    if(j.audio_url){{
      currentAudio = new Audio(j.audio_url);
      currentAudio.play();
    }} else {{
      alert("朗读服务暂不可用：" + (j.error || "未知"));
    }}
  }} catch(e){{
    console.error(e);
    alert("无法连接声影桥，请确认 8766 端口已启动");
  }}
}}

function playNarrate(){{ speak(`{voice.replace("`","\\`")}`, "zh-CN-YunxiNeural"); }}
function playClassical(){{ speak(`{classical.replace("`","\\`")}`, "zh-CN-YunxiNeural"); }}
function playModern(){{ speak(`{modern.replace("`","\\`")}`, "zh-CN-YunxiNeural"); }}
</script>
</body>
</html>
'''


def main():
    P0_DIR.mkdir(parents=True, exist_ok=True)
    data = json.loads(CHAPTER_FILE.read_text(encoding="utf-8"))
    generated = []

    # 保留模板文件本身
    TEMPLATE_FILE.write_text("<!-- 章节模板占位，实际页面由 generate_chapter_pages.py 生成 -->\n", encoding="utf-8")

    system_dna = data.get("metadata", {}).get("dna", DNA)
    for ch in data["chapters"]:
        cid = ch["id"]
        html_content = build_html(ch, system_dna)
        out_path = P0_DIR / f"龍魂-{cid}.html"
        out_path.write_text(html_content, encoding="utf-8")
        generated.append(str(out_path))
        log_change("生成章节独立页", str(out_path), f"章节 {cid} 独立页已生成，含视觉不动点")

    print(f"✅ 已生成 {len(generated)} 个章节独立页")
    print(f"📁 输出目录: {P0_DIR}")
    print(f"🧬 {DNA}")


if __name__ == "__main__":
    main()
