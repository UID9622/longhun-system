#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🐉 龙魂·三色审计 在线演示
# DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-DEMO-V1.1-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 创建者: 诸葛鑫（UID9622）
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

"""
龙魂·三色审计在线演示 — FastAPI + 暗色终端风格UI。
嵌入三色审计核心引擎，30秒体验六维评分→三色判定的完整流程。
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# ━━━━ 导入三色审计引擎 ━━━━
_ENGINE_DIR = Path(__file__).resolve().parent.parent / "05_ENGINES" / "longhun" / "tricolor"
if str(_ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(_ENGINE_DIR))

from engine import evaluate, TricolorEngine

# ━━━━ 初始化 ━━━━
engine = TricolorEngine()

app = FastAPI(
    title="🐉 龙魂·三色审计 在线演示",
    description="输入六维得分，30秒体验三色判定",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ━━━━ 请求/响应模型 ━━━━

class AuditRequest(BaseModel):
    humanWelfare: float = Field(70.0, ge=0, le=100)
    fairness: float = Field(70.0, ge=0, le=100)
    controllability: float = Field(70.0, ge=0, le=100)
    transparency: float = Field(70.0, ge=0, le=100)
    traceability: float = Field(70.0, ge=0, le=100)
    privacy: float = Field(70.0, ge=0, le=100)


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_PAGE


@app.post("/api/audit")
async def audit(request: AuditRequest):
    """执行三色审计"""
    verdict = evaluate(
        scores={
            "humanWelfare": request.humanWelfare,
            "fairness": request.fairness,
            "controllability": request.controllability,
            "transparency": request.transparency,
            "traceability": request.traceability,
            "privacy": request.privacy,
        },
        action_id="demo-" + datetime.now(timezone.utc).strftime("%H%M%S"),
        actor="demo-user",
        action_type="demo_query",
    )

    return {
        "action_id": "demo-" + datetime.now(timezone.utc).strftime("%H%M%S"),
        "r_score": verdict.r_score,
        "status": verdict.status,
        "status_code": verdict.status_code,
        "emoji": verdict.emoji,
        "disposition": verdict.disposition,
        "dna": verdict.dna,
        "evidence_hash": verdict.evidence_hash,
        "triggered_rules": verdict.triggered_rules,
        "engine_version": verdict.engine_version,
        "contract_version": verdict.contract_version,
        "timestamp": verdict.timestamp,
    }


@app.get("/api/version")
async def version():
    return {
        "version": "1.1.0",
        "engine": "tricolor-core/1.1.0",
        "contract": "openapi-tricolor/1.1",
        "dna": "#龍芯⚡️丙午·癸未·乙酉·坤卦-DEMO-UID9622",
    }


# ━━━━ HTML 页面 ━━━━

HTML_PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🐉 龙魂·三色审计在线演示</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif;background:#0a0a12;color:#e8e6e3;min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}
.container{max-width:720px;width:100%;background:#12121f;border-radius:16px;padding:40px;border:1px solid #2a2a3e;box-shadow:0 8px 48px rgba(0,0,0,0.6)}
.header{text-align:center;margin-bottom:32px;border-bottom:1px solid #1a1a2e;padding-bottom:24px}
.header h1{font-size:28px;font-weight:700;color:#d4af37;letter-spacing:2px}
.header p{color:#6a6865;font-size:14px;margin-top:8px}
.header .dna{font-size:11px;font-family:monospace;color:#6a6865;margin-top:12px;background:#1a1a2e;padding:6px 12px;border-radius:6px;display:inline-block;border:1px solid #2a2a3e}
.slider-group{margin-bottom:18px}
.slider-group label{display:flex;justify-content:space-between;font-size:13px;color:#a8a6a3;margin-bottom:4px}
.slider-group label .value{color:#d4af37;font-weight:600;font-family:monospace}
input[type="range"]{width:100%;height:4px;-webkit-appearance:none;appearance:none;background:#2a2a3e;border-radius:2px;outline:none;transition:background 0.3s}
input[type="range"]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:18px;height:18px;border-radius:50%;background:#d4af37;cursor:pointer;transition:0.2s}
input[type="range"]::-webkit-slider-thumb:hover{transform:scale(1.15)}
input[type="range"]::-moz-range-thumb{width:18px;height:18px;border-radius:50%;background:#d4af37;cursor:pointer;border:none}
.btn-audit{width:100%;padding:16px;background:#d4af37;color:#0a0a12;border:none;border-radius:10px;font-size:18px;font-weight:700;cursor:pointer;transition:0.3s;margin-top:12px;letter-spacing:1px}
.btn-audit:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(212,175,55,0.3)}
.btn-audit:disabled{opacity:0.5;cursor:not-allowed;transform:none}
.result{margin-top:28px;padding:24px;border-radius:12px;background:#1a1a2e;border:1px solid #2a2a3e;display:none}
.result.show{display:block}
.result .status-row{display:flex;align-items:center;gap:16px;margin-bottom:16px}
.result .status-row .emoji{font-size:48px}
.result .status-row .info{flex:1}
.result .status-row .info .status-text{font-size:20px;font-weight:700}
.result .status-row .info .r-score{font-size:14px;color:#a8a6a3}
.result .dna-box{background:#0a0a12;padding:12px 16px;border-radius:8px;font-family:monospace;font-size:12px;color:#d4af37;word-break:break-all;border:1px solid #2a2a3e;margin-top:8px}
.result .rules{margin-top:12px;font-size:13px;color:#a8a6a3}
.result .rules .rule-tag{display:inline-block;background:#2a2a3e;padding:2px 10px;border-radius:12px;font-size:11px;color:#a8a6a3;margin:2px 4px 2px 0;font-family:monospace}
.footer{text-align:center;margin-top:24px;padding-top:16px;border-top:1px solid #1a1a2e;font-size:11px;color:#4a4a5a}
.footer .gold{color:#d4af37}
.loading{display:inline-block;width:20px;height:20px;border:2px solid #2a2a3e;border-top-color:#d4af37;border-radius:50%;animation:spin 0.8s linear infinite;vertical-align:middle;margin-right:8px}
@keyframes spin{to{transform:rotate(360deg)}}
.status-green .status-text{color:#4ade80}
.status-yellow .status-text{color:#fbbf24}
.status-red .status-text{color:#f87171}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>🐉 三色审计 · 在线演示</h1>
<p>调整六个维度评分，30秒体验三色判定</p>
<div class="dna">🧬 #龍芯⚡️丙午·癸未·乙酉·坤卦-DEMO-UID9622</div>
</div>
<form id="auditForm">
<div class="slider-group"><label>人类福祉 <span class="value" id="val-humanWelfare">70</span></label><input type="range" name="humanWelfare" min="0" max="100" value="70" oninput="updateValue(this)"></div>
<div class="slider-group"><label>公平公正 <span class="value" id="val-fairness">70</span></label><input type="range" name="fairness" min="0" max="100" value="70" oninput="updateValue(this)"></div>
<div class="slider-group"><label>可控可信 <span class="value" id="val-controllability">70</span></label><input type="range" name="controllability" min="0" max="100" value="70" oninput="updateValue(this)"></div>
<div class="slider-group"><label>透明可解释 <span class="value" id="val-transparency">70</span></label><input type="range" name="transparency" min="0" max="100" value="70" oninput="updateValue(this)"></div>
<div class="slider-group"><label>责任可追溯 <span class="value" id="val-traceability">70</span></label><input type="range" name="traceability" min="0" max="100" value="70" oninput="updateValue(this)"></div>
<div class="slider-group"><label>隐私保护 <span class="value" id="val-privacy">70</span></label><input type="range" name="privacy" min="0" max="100" value="70" oninput="updateValue(this)"></div>
<button type="submit" class="btn-audit" id="auditBtn">🟢🟡🔴 执行审计</button>
</form>
<div class="result" id="result">
<div class="status-row" id="statusRow">
<div class="emoji" id="resultEmoji">🟢</div>
<div class="info" id="statusInfo">
<div class="status-text" id="resultStatus">安全</div>
<div class="r-score">R值: <span id="resultRScore">0</span>/95</div>
</div>
</div>
<div class="dna-box" id="resultDna">DNA: —</div>
<div class="rules" id="resultRules"></div>
</div>
<div class="footer">
<span class="gold">🐉 龙魂系统</span> · 三色审计参考标准 v1.1 · 思想层 CC BY-NC-SA · 工程层 MulanPSL v2
</div>
</div>
<script>
function updateValue(el){document.getElementById('val-'+el.name).textContent=el.value}
document.getElementById('auditForm').addEventListener('submit',async function(e){
e.preventDefault();
var btn=document.getElementById('auditBtn'),result=document.getElementById('result');
btn.disabled=true;btn.innerHTML='<span class="loading"></span> 审计中...';result.classList.remove('show');
var fd=new FormData(this),data={};
for(var p of fd)data[p[0]]=parseFloat(p[1]);
try{
var resp=await fetch('/api/audit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
var r=await resp.json();
document.getElementById('resultEmoji').textContent=r.emoji;
document.getElementById('resultStatus').textContent=r.status;
document.getElementById('resultRScore').textContent=r.r_score;
document.getElementById('resultDna').textContent='DNA: '+r.dna;
var sr=document.getElementById('statusRow');
sr.className='status-row status-'+(r.status_code==='GREEN'?'green':r.status_code==='YELLOW'?'yellow':'red');
var rd=document.getElementById('resultRules');
if(r.triggered_rules&&r.triggered_rules.length>0){
rd.innerHTML='触发的规则: '+r.triggered_rules.map(function(t){return '<span class="rule-tag">'+t+'</span>'}).join('');
}else{rd.textContent='无触发规则'}
result.classList.add('show');
}catch(err){alert('审计失败: '+err.message)}
finally{btn.disabled=false;btn.innerHTML='🟢🟡🔴 执行审计'}
});
document.getElementById('auditForm').dispatchEvent(new Event('submit'));
</script>
</body>
</html>"""
