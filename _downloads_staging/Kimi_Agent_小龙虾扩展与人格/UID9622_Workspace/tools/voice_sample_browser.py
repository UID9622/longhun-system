#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂女声样本浏览器
批量生成推荐女声样本，并生成一个本地 HTML 页面方便试听对比。
DNA: #龍芯⚡️2026-06-27-LONGHUN-VOICE-SAMPLE-BROWSER-v1.0
"""
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

AGENT_DNA = "#龍芯⚡️2026-06-27-LONGHUN-VOICE-SAMPLE-BROWSER-v1.0"
WORKSPACE = Path("/Users/zuimeidedeyihan/Downloads/Kimi_Agent_小龙虾扩展与人格/UID9622_Workspace")
SAMPLE_DIR = WORKSPACE / "temp" / "voice" / "samples"
TEXT = "老大你好，我是龙魂系统助手宝宝，请老大吩咐。"

# 推荐女声候选（可自由增删）
CANDIDATES = [
    "Daisy Studious",
    "Gracie Wise",
    "Claribel Dervla",
    "Tammie Ema",
    "Sofia Hellen",
    "Alison Dietlinde",
    "Ana Florence",
    "Annmarie Nele",
    "Gitta Nikolina",
    "Henriette Usha",
]

SERVER = "http://localhost:9624"


def ensure_server():
    try:
        urllib.request.urlopen(f"{SERVER}/health", timeout=2).read()
        return True
    except Exception:
        print("龍魂语音合成服务未启动，请先运行：tools/baobao_speak.sh '测试'")
        return False


def api(path, data=None):
    url = f"{SERVER}{path}"
    if data is None:
        with urllib.request.urlopen(url, timeout=5) as r:
            return json.loads(r.read().decode("utf-8"))
    payload = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode("utf-8"))


def generate_sample(speaker):
    safe = speaker.replace(" ", "_").replace("/", "_")
    out = SAMPLE_DIR / f"sample_{safe}.wav"
    resp = api("/speak", {
        "text": TEXT,
        "profile": "assistant",
        "speaker": speaker,
        "output_path": str(out),
    })
    if resp.get("ok"):
        return resp["audio_file"]
    else:
        print(f"  ❌ {speaker}: {resp.get('error')}")
        return None


def build_html(results):
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    html_path = SAMPLE_DIR / "index.html"
    rows = []
    for speaker, audio_file in results:
        rel = Path(audio_file).name
        rows.append(f"""
    <tr>
      <td>{speaker}</td>
      <td><audio controls src="{rel}"></audio></td>
      <td><code>{speaker}</code></td>
    </tr>
""")
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>龍魂女声样本试听</title>
<style>
  body {{ font-family: "STSong", "SimSun", "Noto Serif SC", serif; background: #0a0908; color: #f5f0e6; padding: 28px; }}
  h1 {{ color: #f0c674; letter-spacing: 2px; }}
  p {{ color: #8c8378; }}
  table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
  th, td {{ border-bottom: 1px solid #4a3b2a; padding: 12px; text-align: left; }}
  th {{ color: #b87333; }}
  audio {{ width: 320px; }}
  .hint {{ background: rgba(184,115,51,0.15); border-left: 3px solid #b87333; padding: 12px; margin-top: 24px; }}
  code {{ background: #1c1512; padding: 2px 6px; border-radius: 3px; color: #f0c674; }}
</style>
</head>
<body>
  <h1>🐉 龍魂女声样本试听</h1>
  <p>同一句话由不同内置女声生成，听完把最喜欢的名字填进 <code>data/voice_profiles.json</code> 的 <code>assistant.speaker</code>。</p>
  <p>DNA: {AGENT_DNA}</p>
  <table>
    <tr><th>Speaker</th><th>试听</th><th>配置值</th></tr>
    {''.join(rows)}
  </table>
  <div class="hint">
    <strong>设置方法：</strong><br>
    1. 听完选中最佳女声<br>
    2. 编辑 <code>data/voice_profiles.json</code>，将 <code>profiles.assistant.speaker</code> 改为对应名字<br>
    3. 重启语音服务：<code>pkill -f xtts_server.py</code> 后再喊一次「宝宝」
  </div>
</body>
</html>"""
    html_path.write_text(html, encoding="utf-8")
    return html_path


def main():
    if not ensure_server():
        return 1
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"🐉 开始生成 {len(CANDIDATES)} 个女声样本...")
    print(f"DNA: {AGENT_DNA}")
    results = []
    for spk in CANDIDATES:
        print(f"  生成: {spk} ...", end="", flush=True)
        audio = generate_sample(spk)
        if audio:
            print(f" ✅")
            results.append((spk, audio))
        time.sleep(0.2)
    html_path = build_html(results)
    print(f"\n试听页面: {html_path}")
    print(f"浏览器打开: file://{html_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
