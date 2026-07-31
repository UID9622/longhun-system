# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 矩阵章节覆盖层注入器
在沉浸式矩阵页面加入卷轴式章节覆盖层，点击章节节点/列表时弹出，
可朗读、跳转独立页、查看不动点。
DNA: #龍芯⚡️2026-07-04-LONGHUN-MATRIX-CHAPTER-OVERLAY-v1.0
"""

import json
import re
import time
from pathlib import Path

DNA = "#龍芯⚡️2026-07-04-LONGHUN-MATRIX-CHAPTER-OVERLAY-v1.0"
P0_DIR = Path(__file__).resolve().parent.parent.parent / "p0-controls"
MATRIX_FILE = P0_DIR / "龍魂知识矩阵-沉浸式AI播音员.html"
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "中国文化章节.json"
CHANGE_LOG = Path(__file__).resolve().parent.parent / "assets" / "cultural" / "cultural_change_log.jsonl"


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


OVERLAY_HTML = r'''
<!-- 章节卷轴覆盖层 -->
<div id="chapter-overlay">
  <div class="scroll-wrapper">
    <button class="close" onclick="closeChapterOverlay()">×</button>
    <div class="scroll-seal" id="co-seal">章</div>
    <h2 id="co-title">章节标题</h2>
    <div id="co-subtitle">副标题</div>
    <div id="co-era">朝代</div>
    <div class="co-figure">
      <img id="co-img" src="" alt="配图">
      <div id="co-img-caption">配图说明</div>
    </div>
    <div class="co-section">
      <h3>📜 原文</h3>
      <p id="co-classical"></p>
    </div>
    <div class="co-section">
      <h3>💡 白话</h3>
      <p id="co-modern"></p>
    </div>
    <div class="co-actions">
      <button onclick="coNarrate()">▶ 朗读本章</button>
      <button class="secondary" onclick="coReadClassical()">朗读古文</button>
      <button class="secondary" onclick="coReadModern()">朗读白话</button>
      <button class="secondary" onclick="coOpenPage()">📖 打开独立页</button>
    </div>
    <div class="co-immutable">
      <h3>⚓ 视觉不动点</h3>
      <ul id="co-immutable-list"></ul>
    </div>
    <div class="co-attribution">
      <strong>来源标注：</strong><span id="co-attribution"></span>
    </div>
    <div class="co-dna" id="co-dna"></div>
  </div>
</div>
'''

OVERLAY_CSS = r'''
/* === 章节卷轴覆盖层 === */
#chapter-overlay{position:fixed;inset:0;z-index:60;display:none;align-items:center;justify-content:center;background:rgba(10,10,15,.88);backdrop-filter:blur(6px);padding:20px}
#chapter-overlay.open{display:flex}
#chapter-overlay .scroll-wrapper{position:relative;width:100%;max-width:720px;max-height:90vh;overflow-y:auto;background:linear-gradient(180deg,#f7f3e8 0%,#efe9db 100%);border-radius:12px;border:1px solid rgba(139,0,0,.25);box-shadow:0 20px 60px rgba(0,0,0,.5);color:#1a1a1a;padding:40px 30px 30px}
#chapter-overlay .close{position:absolute;top:10px;right:14px;background:none;border:none;font-size:28px;color:#4a0000;cursor:pointer;z-index:5}
#chapter-overlay .scroll-seal{width:72px;height:72px;margin:0 auto 18px;background:#8b0000;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#f7f3e8;font-size:28px;font-weight:bold;border:2px solid rgba(212,175,55,.5);box-shadow:0 4px 12px rgba(139,0,0,.3)}
#chapter-overlay h2{text-align:center;font-size:28px;color:#4a0000;margin-bottom:6px;letter-spacing:3px}
#co-subtitle{text-align:center;font-size:15px;color:#555;margin-bottom:4px}
#co-era{text-align:center;font-size:12px;color:#8b0000;border:1px solid rgba(139,0,0,.2);display:inline-block;padding:2px 12px;border-radius:20px;margin:0 auto 18px}
#chapter-overlay .co-figure{text-align:center;margin-bottom:20px;background:rgba(255,255,255,.5);border-radius:8px;padding:12px;border:1px solid rgba(139,0,0,.1)}
#chapter-overlay .co-figure img{max-width:100%;max-height:260px;border-radius:6px;border:1px solid rgba(139,0,0,.1)}
#chapter-overlay .co-figure #co-img-caption{font-size:12px;color:#666;margin-top:8px}
#chapter-overlay .co-section{margin-bottom:18px}
#chapter-overlay .co-section h3{font-size:15px;color:#4a0000;margin-bottom:8px;border-left:4px solid #d4af37;padding-left:8px}
#chapter-overlay .co-section p{font-size:14px;line-height:1.8;color:#333;text-align:justify}
#chapter-overlay .co-actions{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px}
#chapter-overlay .co-actions button{background:#4a0000;color:#fff;border:none;padding:10px 18px;border-radius:6px;font-family:inherit;font-size:13px;cursor:pointer}
#chapter-overlay .co-actions button.secondary{background:transparent;color:#4a0000;border:1px solid #4a0000}
#chapter-overlay .co-immutable{background:rgba(212,175,55,.08);border:1px dashed #d4af37;border-radius:10px;padding:15px;margin-bottom:18px}
#chapter-overlay .co-immutable h3{font-size:14px;color:#4a0000;margin-bottom:10px}
#chapter-overlay .co-immutable ul{list-style:none}
#chapter-overlay .co-immutable li{padding:6px 0;font-size:13px;line-height:1.6;border-bottom:1px solid rgba(139,0,0,.06)}
#chapter-overlay .co-immutable li:last-child{border-bottom:none}
#chapter-overlay .co-attribution{font-size:12px;color:#555;line-height:1.6;margin-bottom:10px}
#chapter-overlay .co-dna{font-family:monospace;font-size:10px;color:#777;word-break:break-all;border-top:1px solid rgba(139,0,0,.1);padding-top:10px}
@media (max-width:600px){
  #chapter-overlay .scroll-wrapper{padding:30px 18px 20px}
  #chapter-overlay h2{font-size:22px}
}
'''

OVERLAY_JS = r'''
let currentChapter = null;

function openChapterOverlay(cid){
  if(!CHAPTER_DATA || !CHAPTER_DATA.chapters) return;
  const c = CHAPTER_DATA.chapters.find(x=>x.id===cid);
  if(!c) return;
  currentChapter = c;
  document.getElementById('co-seal').textContent = c.seal_text || '章';
  document.getElementById('co-title').textContent = c.title;
  document.getElementById('co-subtitle').textContent = c.subtitle;
  document.getElementById('co-era').textContent = (c.era || '') + (c.era_en ? ' · ' + c.era_en : '');
  const fig = c.figure_image || {};
  const img = document.getElementById('co-img');
  img.src = fig.local ? 'api/' + fig.local : '';
  img.alt = c.title + '配图';
  document.getElementById('co-img-caption').textContent = (c.visual_theme || '') + ' · ' + (fig.status==='placeholder'?'占位素材 · 待替换为真实公开版权图像':'真实公开版权图像');
  document.getElementById('co-classical').textContent = c.classical_text;
  document.getElementById('co-modern').textContent = c.modern_text;
  document.getElementById('co-attribution').textContent = c.attribution || '暂无来源标注';
  document.getElementById('co-dna').textContent = '不动点 DNA：' + (c.visual_anchor_dna || '-') + '\n系统 DNA：#龍芯⚡️2026-07-04-LONGHUN-CHINESE-CULTURE-CHAPTERS-v1.1';
  const immList = document.getElementById('co-immutable-list');
  immList.innerHTML = (c.immutable_points || []).map(p=>'<li><span style="color:#d4af37;margin-right:6px">◆</span>'+p+'</li>').join('');
  document.getElementById('chapter-overlay').classList.add('open');
}
function closeChapterOverlay(){
  document.getElementById('chapter-overlay').classList.remove('open');
  currentChapter = null;
}
function coNarrate(){ if(currentChapter) narrateChapter(currentChapter.id); }
function coReadClassical(){ if(currentChapter) speak(currentChapter.classical_text); }
function coReadModern(){ if(currentChapter) speak(currentChapter.modern_text); }
function coOpenPage(){ if(currentChapter) window.open('龍魂-'+currentChapter.id+'.html', '_blank'); }

// 加载章节数据到全局
let CHAPTER_DATA = null;
function loadChapterData(){
  fetch(API_BASE + '/chapters')
    .then(r=>r.json())
    .then(data=>{ CHAPTER_DATA = data; handleFocusParam(); });
}
function handleFocusParam(){
  const params = new URLSearchParams(location.search);
  const focus = params.get('focus');
  if(focus && CHAPTER_DATA && CHAPTER_DATA.chapters.find(c=>c.id===focus)){
    openChapterOverlay(focus);
  }
}
'''

MODIFY_RENDERS = r'''
function renderChapters(){
  fetch(`${API_BASE}/chapters`)
    .then(r=>r.json())
    .then(data=>{
      CHAPTER_DATA = data;
      const list = document.getElementById('chapter-list');
      list.innerHTML = '';
      data.chapters.forEach(c=>{
        const div = document.createElement('div');
        div.className = 'chapter-item';
        div.innerHTML = `<div class="c-title">${c.title}</div><div class="c-sub">${c.subtitle}</div>`;
        div.onclick = ()=> openChapterOverlay(c.id);
        list.appendChild(div);
      });
      handleFocusParam();
    });
}
'''


def inject():
    text = MATRIX_FILE.read_text(encoding="utf-8")
    original = text

    # 1. 注入 CSS（在第一个 </style> 之前，避开无障碍的第二个 style）
    # 找到 body 前的 </style>
    style_end = text.find("</style>")
    if style_end == -1:
        raise RuntimeError("找不到 </style>")
    text = text[:style_end] + "\n" + OVERLAY_CSS + "\n" + text[style_end:]

    # 2. 注入 HTML（在 detail 面板之后）
    detail_end = text.find('</div>\n\n<div id="help">')
    if detail_end == -1:
        # fallback
        detail_end = text.find('<div id="help">')
    if detail_end == -1:
        raise RuntimeError("找不到 help 面板插入点")
    text = text[:detail_end] + "\n" + OVERLAY_HTML + "\n" + text[detail_end:]

    # 3. 替换 renderChapters 函数
    pattern = r"function renderChapters\(\)\{[\s\S]*?\n\}"
    if not re.search(pattern, text):
        raise RuntimeError("找不到 renderChapters 函数")
    text = re.sub(pattern, MODIFY_RENDERS.strip(), text, count=1)

    # 4. 注入 JS（在 API_BASE 之后）
    api_base_pos = text.find("const API_BASE = 'http://127.0.0.1:8766';")
    if api_base_pos == -1:
        raise RuntimeError("找不到 API_BASE")
    # 在 API_BASE 行末尾插入
    line_end = text.find("\n", api_base_pos) + 1
    text = text[:line_end] + "\n" + OVERLAY_JS + "\n" + text[line_end:]

    # 5. 修改 initVoiceAvatar 调用 loadChapterData（renderChapters 里已加载，无需重复）
    # 在 DOMContentLoaded 中保留 initVoiceAvatar 即可

    # 6. 修改 narrateChapter 同时打开覆盖层
    narrate_pattern = r"(function narrateChapter\(chapterId\)\{\n  setAvatarStatus\('准备章节…'\);)"
    repl = r"\1\n  openChapterOverlay(chapterId);"
    text = re.sub(narrate_pattern, repl, text, count=1)

    # 7. 阻止覆盖层点击穿透
    click_handler_pattern = r"(function onClick\(e\) \{\n  if \(hoveredNode\) \{\n    selectNode\(hoveredNode\.userData\.node\);\n  \} else if \(!e\.target\.closest\('#detail'\) && !e\.target\.closest\('#hud'\)\) \{\n    closeDetail\(\);\n  \}\n\})"
    repl_click = r"function onClick(e) {\n  if (hoveredNode) {\n    const node = hoveredNode.userData.node;\n    if (node && node.properties && node.properties.chapter_id) {\n      openChapterOverlay(node.properties.chapter_id);\n    } else {\n      selectNode(node);\n    }\n  } else if (!e.target.closest('#detail') && !e.target.closest('#hud') && !e.target.closest('#chapter-overlay')) {\n    closeDetail();\n  }\n}"
    text = re.sub(click_handler_pattern, repl_click, text, count=1)

    # 8. 更新 DNA 标记
    text = text.replace(
        "#龍芯⚡️2026-07-04-LONGHUN-KNOWLEDGE-MATRIX-3D-v1.1",
        "#龍芯⚡️2026-07-04-LONGHUN-KNOWLEDGE-MATRIX-3D-v1.2"
    )

    if text == original:
        print("⚠️ 内容未发生变化")
    else:
        MATRIX_FILE.write_text(text, encoding="utf-8")
        log_change("注入矩阵章节覆盖层", str(MATRIX_FILE), "添加卷轴式章节覆盖层，支持朗读、跳转独立页、URL focus 参数")
        print(f"✅ 已注入章节覆盖层到 {MATRIX_FILE}")
        print(f"🧬 {DNA}")


if __name__ == "__main__":
    inject()
