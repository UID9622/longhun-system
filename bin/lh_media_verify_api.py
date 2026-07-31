# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_MEDIA_VERIFY_API-v1.0-3fa80932
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·媒体主权验证 API v1.0
部署到鲲鹏，提供官网验证入口。

端点：
  GET  /           → 验证门户页面
  GET  /health     → 健康检查
  POST /verify     → 上传文件，返回 DNA / 水印验证结果
"""
import io
import json
import sys
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse

sys.path.insert(0, str(Path(__file__).parent.parent / "engines"))
from lh_media_sovereignty_marker import MediaSovereigntyMarker  # noqa: E402

app = FastAPI(title="龍魂·媒体主权验证 API", version="1.0.0")

# 门户 HTML
PORTAL_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>龍魂·媒体主权验证</title>
<style>
  :root { --gold: #C9A84C; --bg: #080808; --panel: #111; --red: #8B0000; }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--gold); font-family: "SF Pro", "Noto Sans SC", sans-serif; min-height: 100vh; display: flex; flex-direction: column; align-items: center; }
  .container { width: 90%; max-width: 720px; margin-top: 60px; }
  h1 { text-align: center; font-size: 2.2rem; margin-bottom: 0.4rem; letter-spacing: 0.1em; }
  .subtitle { text-align: center; opacity: 0.8; margin-bottom: 2rem; font-size: 0.95rem; }
  .panel { background: var(--panel); border: 1px solid rgba(201,168,76,0.3); border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; }
  .dropzone { border: 2px dashed rgba(201,168,76,0.5); border-radius: 6px; padding: 2rem; text-align: center; cursor: pointer; transition: all 0.2s; }
  .dropzone:hover, .dropzone.dragover { border-color: var(--gold); background: rgba(201,168,76,0.05); }
  input[type="file"] { display: none; }
  button { background: var(--gold); color: #000; border: none; padding: 0.7rem 1.4rem; font-weight: bold; border-radius: 4px; cursor: pointer; margin-top: 1rem; }
  button:disabled { opacity: 0.5; cursor: not-allowed; }
  .result { margin-top: 1rem; font-family: monospace; white-space: pre-wrap; word-break: break-all; background: #000; padding: 1rem; border-radius: 4px; border: 1px solid rgba(201,168,76,0.2); }
  .ok { color: #4caf50; }
  .warn { color: #ff9800; }
  .fail { color: #f44336; }
  footer { margin-top: auto; padding: 2rem; opacity: 0.5; font-size: 0.8rem; text-align: center; }
</style>
</head>
<body>
<div class="container">
  <h1>龍魂 · 媒体主权验证</h1>
  <div class="subtitle">上传图片、音频或字体，查验是否为龍魂生态原生出品</div>

  <div class="panel">
    <div class="dropzone" id="dropzone">
      <div>点击或拖拽文件到此处</div>
      <div style="font-size:0.8rem;opacity:0.6;margin-top:0.5rem;">支持 PNG / JPG / WAV / OTF / TTF / WOFF / MP4</div>
    </div>
    <input type="file" id="fileInput">
    <div id="fileName" style="margin-top:0.8rem;"></div>
    <button id="verifyBtn" disabled>开始验证</button>
    <div id="result"></div>
  </div>

  <div class="panel" style="font-size:0.85rem;opacity:0.9;">
    <strong>说明：</strong><br>
    1. 本服务仅读取文件中的 DNA 水印，不上传文件内容到第三方。<br>
    2. 龍魂生态生成的图片、音频、视频均会嵌入不可磨灭的 DNA 主权标记。<br>
    3. 验证通过即证明内容来自龍魂授权链路，可被追溯至源头。
  </div>
</div>
<footer>DNA: #龍芯⚡️20260726-MEDIA-VERIFY-v1.0 · UID9622</footer>

<script>
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const verifyBtn = document.getElementById('verifyBtn');
const fileName = document.getElementById('fileName');
const result = document.getElementById('result');
let currentFile = null;

dropzone.addEventListener('click', () => fileInput.click());
dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('dragover'); });
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
dropzone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropzone.classList.remove('dragover');
  if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', (e) => { if (e.target.files.length) handleFile(e.target.files[0]); });

function handleFile(file) {
  currentFile = file;
  fileName.textContent = '已选择: ' + file.name + ' (' + (file.size/1024).toFixed(1) + ' KB)';
  verifyBtn.disabled = false;
  result.innerHTML = '';
}

verifyBtn.addEventListener('click', async () => {
  if (!currentFile) return;
  verifyBtn.disabled = true;
  result.innerHTML = '验证中...';
  const form = new FormData();
  form.append('file', currentFile);
  try {
    const res = await fetch('/verify', { method: 'POST', body: form });
    const data = await res.json();
    let cls = 'warn';
    if (data.has_dna) cls = 'ok';
    else if (data.error) cls = 'fail';
    result.innerHTML = '<div class="' + cls + '">' + JSON.stringify(data, null, 2) + '</div>';
  } catch (e) {
    result.innerHTML = '<div class="fail">请求失败: ' + e.message + '</div>';
  }
  verifyBtn.disabled = false;
});
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def portal():
    return PORTAL_HTML


@app.get("/health")
def health():
    return {"status": "ok", "service": "lh-media-verify-api", "version": "1.0.0"}


@app.post("/verify")
def verify(file: UploadFile = File(...)):
    suffix = Path(file.filename or "unknown").suffix.lower()
    allowed = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".wav", ".mp3",
               ".otf", ".ttf", ".woff", ".woff2", ".mp4", ".mov", ".avi"}
    if suffix not in allowed:
        return JSONResponse({"error": f"不支持的文件类型: {suffix}"}, status_code=400)

    try:
        contents = file.file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        result = MediaSovereigntyMarker.verify(tmp_path)
        Path(tmp_path).unlink(missing_ok=True)

        media_type = result.get("media_type", "unknown")
        dna = result.get("dna")
        has_dna = bool(dna)

        response = {
            "filename": file.filename,
            "media_type": media_type,
            "has_dna": has_dna,
            "dna": dna,
        }

        if media_type == "font":
            response["native_watermark_likely"] = result.get("native_watermark_likely", False)
            response["has_pua_glyph"] = result.get("has_pua_glyph", False)

        if media_type == "video":
            response["fingerprint"] = result.get("fingerprint")
            response["note"] = result.get("note", "基于音频轨 Patchwork 盲水印 + 无音频时回退 Y 通道 DCT")

        return response
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


def main():
    import uvicorn
    import os
    port = int(os.environ.get("LH_MEDIA_VERIFY_PORT", "8780"))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
