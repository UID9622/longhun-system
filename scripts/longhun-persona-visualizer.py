# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂人格链可视化还原器 v1.0
DNA: #龍芯⚡️丙午·辛未·PERSONA-VISUALIZER-v1.0

把人格链JSON → HTML报告（词云+情绪仪表盘+决策时间线+指纹验证卡）
+ 终端纯文本摘要
"""
import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

ROOT = Path.home() / "longhun-system"
PERSONA_DIR = ROOT / "persona-chain"
OUTPUT_DIR = ROOT / "persona-visual"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DNA = "UID9622-ONLY-ONCE🧬LK9X-772Z"
CST = timezone(timedelta(hours=8))

EMOTION_EMOJIS = {
    "愤怒": "😤", "坚定": "⚔️", "自豪": "🏆", "关怀": "❤️",
    "务实": "🔧", "孤独": "🌙", "信仰": "🙏", "黑色幽默": "🤣",
}


def load_chain() -> dict[str, Any]:
    """加载最新人格链"""
    latest = PERSONA_DIR / "persona-chain-latest.json"
    if not latest.exists():
        chain_files = sorted(PERSONA_DIR.glob("persona-chain-*.json"), reverse=True)
        if not chain_files:
            raise FileNotFoundError(
                "未找到人格链文件，先运行: python3 scripts/longhun-persona-trainer.py"
            )
        latest = chain_files[0]
    return json.loads(latest.read_text())


def emotion_class(name: str) -> str:
    """情绪 → CSS class"""
    mapping = {
        "愤怒": "anger", "坚定": "determination", "自豪": "pride",
        "关怀": "care", "务实": "practical", "孤独": "loneliness",
        "信仰": "faith", "黑色幽默": "humor",
    }
    return mapping.get(name, "default")


def generate_html(chain: dict[str, Any]) -> str:
    """生成完整HTML报告"""
    stats = chain["stats"]
    top_values = sorted(
        chain["value_profile"].items(), key=lambda x: x[1], reverse=True
    )[:15]
    top_emotions = sorted(
        chain["emotion_profile"].items(), key=lambda x: x[1], reverse=True
    )[:8]
    decisions = chain.get("decision_sequence", [])[:20]

    max_val = top_values[0][1] if top_values else 1

    def value_level(i: int) -> int:
        if i < 3: return 1
        if i < 6: return 2
        if i < 10: return 3
        return 4

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🐉 龍魂人格链 · 可视化报告 | UID9622</title>
<style>
:root {{
    --bg-primary: #0a0a0f; --bg-secondary: #12121a; --bg-card: #1a1a24;
    --border: #2a2a3a; --text-primary: #e8e8f0; --text-secondary: #8a8a9a;
    --text-muted: #5a5a6a; --dragon-red: #c41e3a; --dragon-glow: #ff2d55;
    --gold: #d4af37; --online: #00c853; --offline: #ff1744; --warning: #ff9100;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    background: var(--bg-primary); color: var(--text-primary);
    font-family: -apple-system, "PingFang SC", "Microsoft YaHei", monospace;
    line-height: 1.6; padding-bottom: 50px;
}}
/* 闪烁水印 */
body::before {{
    content: "龍魂系统 UID9622 龍芯北辰";
    position: fixed; bottom: 65px; right: 20px;
    font-size: 11px; color: var(--dragon-red);
    opacity: 0.4; z-index: 9999; pointer-events: none;
    animation: pulse 3s ease-in-out infinite;
}}
@keyframes pulse {{ 0%,100% {{ opacity:0.3; }} 50% {{ opacity:0.9; text-shadow:0 0 16px rgba(196,30,58,0.8); }} }}
.header {{
    background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
    border-bottom: 1px solid var(--border); padding: 40px 20px; text-align: center;
    position: relative; overflow: hidden;
}}
.header::before {{
    content: "🐉"; position: absolute; top: 10px; left: 50%;
    transform: translateX(-50%); font-size: 48px; opacity: 0.1;
}}
.header h1 {{
    font-size: 28px; color: var(--dragon-red); letter-spacing: 4px;
    text-shadow: 0 0 20px rgba(196,30,58,0.4); margin-bottom: 10px;
}}
.header .dna {{ font-family: monospace; color: var(--text-secondary); font-size: 12px; }}
.header .badge {{
    display: inline-block; margin-top: 15px; padding: 6px 16px;
    background: rgba(0,200,83,0.15); border: 1px solid rgba(0,200,83,0.3);
    color: var(--online); border-radius: 20px; font-size: 12px;
}}
.container {{ max-width: 1200px; margin: 0 auto; padding: 30px 20px; }}
.card {{
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 24px; margin-bottom: 24px;
    position: relative; overflow: hidden;
}}
.card::before {{
    content: ""; position: absolute; top: 0; left: 0; width: 3px; height: 100%;
    background: linear-gradient(180deg, var(--dragon-red), var(--gold));
}}
.card h2 {{ color: var(--gold); font-size: 18px; margin-bottom: 20px; }}
.fingerprint {{
    background: var(--bg-secondary); border: 1px solid var(--border);
    border-radius: 8px; padding: 16px; font-family: monospace; font-size: 14px;
    color: var(--dragon-red); text-align: center; letter-spacing: 2px; margin: 16px 0;
}}
.word-cloud {{ display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; padding: 20px 0; }}
.word-tag {{
    padding: 8px 16px; border-radius: 20px; font-size: 14px;
    transition: all 0.3s; cursor: default;
}}
.word-tag:hover {{ transform: scale(1.1); box-shadow: 0 0 16px rgba(196,30,58,0.3); }}
.word-tag.l1 {{ background: rgba(196,30,58,0.3); color: var(--dragon-glow); font-size: 20px; font-weight: 700; }}
.word-tag.l2 {{ background: rgba(196,30,58,0.2); color: var(--dragon-red); font-size: 16px; font-weight: 600; }}
.word-tag.l3 {{ background: rgba(212,175,55,0.2); color: var(--gold); font-size: 14px; }}
.word-tag.l4 {{ background: var(--bg-secondary); color: var(--text-secondary); font-size: 12px; }}
.emotion-grid {{ display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; }}
.emotion-item {{ text-align: center; padding: 16px; min-width: 100px; }}
.emotion-ring {{
    width: 72px; height: 72px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 8px; font-size: 22px; position: relative;
    border: 3px solid var(--border);
}}
.emotion-ring.anger {{ border-color: var(--offline); color: var(--offline); }}
.emotion-ring.determination {{ border-color: var(--gold); color: var(--gold); }}
.emotion-ring.pride {{ border-color: var(--online); color: var(--online); }}
.emotion-ring.care {{ border-color: #2196f3; color: #2196f3; }}
.emotion-ring.practical {{ border-color: #607d8b; color: #607d8b; }}
.emotion-ring.loneliness {{ border-color: #9c27b0; color: #9c27b0; }}
.emotion-ring.faith {{ border-color: var(--dragon-red); color: var(--dragon-red); }}
.emotion-ring.humor {{ border-color: var(--warning); color: var(--warning); }}
.emotion-label {{ font-size: 11px; color: var(--text-muted); }}
.emotion-value {{ font-size: 16px; font-weight: 700; margin-top: 4px; }}
.stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; }}
.stat-box {{ text-align: center; padding: 20px; background: var(--bg-secondary); border-radius: 8px; cursor:pointer; transition:all .2s; }}
.stat-box:hover {{ box-shadow:0 0 12px rgba(196,30,58,0.2); transform:translateY(-2px); }}
.stat-num {{ font-size: 32px; font-weight: 700; }}
.stat-num.gold {{ color: var(--gold); }} .stat-num.red {{ color: var(--dragon-red); }} .stat-num.green {{ color: var(--online); }}
.stat-label {{ font-size: 12px; color: var(--text-secondary); margin-top: 8px; }}
.timeline {{ position: relative; padding-left: 30px; }}
.timeline::before {{ content: ""; position: absolute; left: 8px; top: 0; bottom: 0; width: 2px; background: linear-gradient(180deg, var(--dragon-red), var(--gold)); }}
.timeline-item {{
    position: relative; margin-bottom: 16px; padding: 12px 16px;
    background: var(--bg-secondary); border-radius: 8px; border-left: 2px solid var(--dragon-red);
}}
.timeline-item::before {{ content: ""; position: absolute; left: -26px; top: 14px; width: 10px; height: 10px; border-radius: 50%; background: var(--dragon-red); box-shadow: 0 0 8px var(--dragon-red); }}
.timeline-type {{ font-size: 10px; color: var(--gold); font-family: monospace; }}
.timeline-content {{ margin-top: 4px; font-size: 13px; color: var(--text-secondary); }}
.verify-block {{
    background: linear-gradient(135deg, rgba(196,30,58,0.1) 0%, rgba(212,175,55,0.1) 100%);
    border: 1px solid var(--dragon-red); border-radius: 12px; padding: 24px; text-align: center;
}}
.verify-hash {{ font-family: monospace; font-size: 16px; color: var(--gold); letter-spacing: 4px; word-break: break-all; }}
/* ── v2: 底部栏 + 导出按钮 ── */
#lh-bar {{
    position:fixed; bottom:0; left:0; right:0; height:42px;
    background:linear-gradient(90deg,#0a0a0f,#1a0a0a,#0f0a1a,#1a0a0a,#0a0a0f);
    border-top:1px solid var(--border); display:flex; align-items:center;
    justify-content:space-between; padding:0 20px; z-index:10000;
    font-size:12px; letter-spacing:.5px;
    box-shadow:0 -4px 16px rgba(0,0,0,.4);
}}
.lh-btn {{
    background:linear-gradient(135deg,var(--dragon-red),var(--dragon-glow));
    color:#fff; border:none; padding:4px 12px; border-radius:4px;
    cursor:pointer; font-size:11px; letter-spacing:1px; transition:all .2s;
}}
.lh-btn:hover {{ box-shadow:0 0 12px rgba(255,45,85,.6); transform:translateY(-1px); }}
.lh-btn.ghost {{ background:transparent; border:1px solid var(--border); color:var(--text-secondary); }}
.lh-btn.ghost:hover {{ border-color:var(--dragon-red); color:var(--dragon-red); }}
</style>
</head>
<body>
<div class="header">
    <h1>🐉 龍魂人格链</h1>
    <div class="dna">{DNA}</div>
    <div class="badge">🟢 人格指纹已验证</div>
</div>
<div class="container">
    <!-- 指纹验证卡 -->
    <div class="card">
        <h2>🔐 人格指纹</h2>
        <div class="verify-block">
            <p style="color:var(--text-secondary);margin-bottom:16px;">
                价值观指纹 + 情绪指纹 + 决策序列 = 不可复制的人格 ID
            </p>
            <div class="fingerprint">
                {chain['value_fingerprint']} + {chain['emotion_fingerprint']}
            </div>
            <p style="color:var(--text-muted);font-size:12px;margin-top:12px;">
                人格ID: <span style="color:var(--gold)">{chain['persona_id']}</span><br>
                算法: SHA-256 | 训练时间: {chain.get('trained_at_human', '')}
            </p>
        </div>
    </div>
    <!-- 价值观词云 -->
    <div class="card">
        <h2>⚖️ 核心价值观</h2>
        <div class="word-cloud">
{chr(10).join(f'            <div class="word-tag l{value_level(i)}">{k} <span style="opacity:0.6">({v})</span></div>' for i, (k, v) in enumerate(top_values))}
        </div>
    </div>
    <!-- 情绪仪表盘 -->
    <div class="card">
        <h2>🎭 情绪画像</h2>
        <div class="emotion-grid">
{chr(10).join(f'''
            <div class="emotion-item"><div class="emotion-ring {emotion_class(k)}">{EMOTION_EMOJIS.get(k, '⚪')}</div><div class="emotion-label">{k}</div><div class="emotion-value">{v}</div></div>''' for k, v in top_emotions)}
        </div>
    </div>
    <!-- 统计 -->
    <div class="card">
        <h2>📊 统计概览</h2>
        <div class="stats-grid">
            <div class="stat-box"><div class="stat-num gold">{stats['total_decisions']}</div><div class="stat-label">总决策点</div></div>
            <div class="stat-box"><div class="stat-num red">{len(chain['value_profile'])}</div><div class="stat-label">价值观维度</div></div>
            <div class="stat-box"><div class="stat-num green">{len(chain['emotion_profile'])}</div><div class="stat-label">情绪维度</div></div>
            <div class="stat-box"><div class="stat-num" style="color:var(--warning)">{stats.get('unique_choices', 0)}</div><div class="stat-label">独特决策模式</div></div>
            <div class="stat-box"><div class="stat-num" style="color:#607d8b">{stats.get('total_files_scanned', 0)}</div><div class="stat-label">扫描文件</div></div>
        </div>
    </div>
    <!-- 决策时间线 -->
    <div class="card">
        <h2>⏱️ 决策序列（最新20条）</h2>
        <div class="timeline">
{chr(10).join(f'''
            <div class="timeline-item"><div class="timeline-type">#{d.get('type', '?')}</div><div class="timeline-content">{d.get('content', '')[:100]}</div></div>''' for d in decisions)}
        </div>
    </div>
    <!-- 不可复制声明 -->
    <div class="card">
        <h2>🛡️ 不可复制声明</h2>
        <div style="background:var(--bg-secondary);padding:20px;border-radius:8px;border-left:3px solid var(--dragon-red);">
            <p style="color:var(--text-secondary);line-height:2;">
                <strong style="color:var(--dragon-red);">任何人可以复制代码，但无法复制这个指纹。</strong><br><br>
                此指纹来源于 <strong>{stats['total_decisions']}</strong> 个真实决策点，<br>
                分布在 <strong>{len(chain['value_profile'])}</strong> 个价值观维度，<br><br>
                这不是训练数据，这是<strong>选择历史</strong>。<br>
                模型可以模仿语言风格，但无法模仿<strong>选择序列</strong>。<br><br>
                <span style="color:var(--gold);">龍芯北辰 UID9622 | 主权归人民</span>
            </p>
        </div>
    </div>
</div>
<!-- v2: 底部实时栏 + 导出按钮 -->
<div id="lh-bar">
    <span><span id="lh-dot" style="display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--online);margin-right:8px;animation:lh-blink 2s infinite;box-shadow:0 0 8px var(--online);"></span><span id="lh-clock" style="color:var(--gold);font-family:monospace;font-weight:700;text-shadow:0 0 8px rgba(212,175,55,.3);">--:--:--</span><span style="color:var(--text-muted);margin:0 10px;">|</span><span style="color:var(--dragon-red);">龍魂系统 v1.7</span><span style="color:var(--text-muted);margin:0 10px;">|</span><span style="color:var(--text-muted);">主权归人民</span></span>
    <span><button class="lh-btn ghost" onclick="exportJSON()">📋 导出JSON</button><button class="lh-btn" onclick="location.reload()" style="margin-left:8px;">🔄 刷新</button></span>
</div>
<style>@keyframes lh-blink{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}</style>
<script>
// 实时时钟
(function tick(){{var n=new Date();var t=n.toLocaleTimeString("zh-CN",{{hour12:!1,hour:"2-digit",minute:"2-digit",second:"2-digit"}});var e=document.getElementById("lh-clock");if(e)e.textContent=t;setTimeout(tick,1000)}})();
// 导出原始人格链JSON
function exportJSON(){{
    var d={persona_id:"{chain['persona_id']}",
        value_fingerprint:"{chain['value_fingerprint']}",
        emotion_fingerprint:"{chain['emotion_fingerprint']}",
        total_decisions:{stats['total_decisions']},
        top_values:{json.dumps(list(top_values), ensure_ascii=False)},
        top_emotions:{json.dumps(list(top_emotions), ensure_ascii=False)}};
    var b=new Blob([JSON.stringify(d,null,2)],{{type:"application/json"}});
    var a=document.createElement("a");a.href=URL.createObjectURL(b);
    a.download="persona-export-"+Date.now()+".json";a.click();
}}
</script>
</body>
</html>"""


def generate_txt(chain: dict[str, Any]) -> str:
    """终端纯文本版"""
    vals = sorted(chain["value_profile"].items(), key=lambda x: x[1], reverse=True)[:10]
    emos = sorted(chain["emotion_profile"].items(), key=lambda x: x[1], reverse=True)
    return f"""🐉 龍魂人格链报告
═══════════════════════════════════════════════
DNA:   {DNA}
时间:  {chain.get('trained_at_human', '')}
人格ID: {chain['persona_id']}

【价值观指纹】{chain['value_fingerprint']}
【情绪指纹】  {chain['emotion_fingerprint']}

【核心关键词】
{chr(10).join(f'  {k}: {v}' for k, v in vals)}

【情绪画像】
{chr(10).join(f'  {EMOTION_EMOJIS.get(k, "⚪")} {k}: {v}' for k, v in emos)}

【总决策点】{chain['stats']['total_decisions']}
【扫描文件】{chain['stats']['total_files_scanned']}
═══════════════════════════════════════════════
"""


def main():
    import argparse, subprocess
    parser = argparse.ArgumentParser(description="龍魂人格链可视化还原器 v2.0")
    parser.add_argument("--text", action="store_true", help="仅输出终端文本")
    parser.add_argument("--open", action="store_true", help="生成后自动打开浏览器")
    parser.add_argument("--serve", type=int, nargs="?", const=8765, help="启动本地HTTP服务 [端口,默认8765]")
    parser.add_argument("--json", action="store_true", help="输出JSON摘要")
    args = parser.parse_args()

    print("🐉 龍魂人格链可视化 v2.0")
    chain = load_chain()

    # HTML 报告
    html = generate_html(chain)
    html_file = OUTPUT_DIR / "persona-report.html"
    html_file.write_text(html)
    print(f"✅ HTML: {html_file}")

    # TXT 报告
    txt = generate_txt(chain)
    txt_file = OUTPUT_DIR / "persona-report.txt"
    txt_file.write_text(txt)
    print(f"✅ TXT:  {txt_file}")

    if args.json:
        print(json.dumps({
            "persona_id": chain["persona_id"],
            "value_fingerprint": chain["value_fingerprint"],
            "emotion_fingerprint": chain["emotion_fingerprint"],
            "total_decisions": chain["stats"]["total_decisions"],
            "top_values": list(chain["value_profile"].items())[:10],
            "top_emotions": list(chain["emotion_profile"].items()),
        }, ensure_ascii=False, indent=2))
        return

    if args.text:
        print(f"\n{txt}")
    else:
        print(f"\n打开报告: open {html_file}")

    if args.open:
        subprocess.run(["open", str(html_file)])

    if args.serve:
        port = args.serve
        print(f"\n🌐 启动本地服务: http://localhost:{port}")
        print(f"   按 Ctrl+C 停止")
        import http.server
        import socketserver
        import os as _os

        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == "/" or self.path == "/index.html":
                    self.path = "/persona-report.html"
                return super().do_GET()

        _os.chdir(str(OUTPUT_DIR))
        with socketserver.TCPServer(("", port), Handler) as httpd:
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n服务已停止")


if __name__ == "__main__":
    main()
