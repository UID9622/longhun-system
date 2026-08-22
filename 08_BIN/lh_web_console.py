#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LH_WEB_CONSOLE-C1CA43D6
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
龍魂 Web 控制台 v2.0 · UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
把所有命令变成点一下就执行的按钮 · 21按钮·5分组
"""
from flask import Flask, render_template_string, jsonify, request
import subprocess, json, os, datetime, time
from collections import OrderedDict

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐉 龍魂控制台 · UID9622</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { background:#0a0a12; color:#e0e0e0; font-family: monospace; padding:20px; }
        .container { max-width:1280px; margin:0 auto; }
        h1 { color:#f0c060; font-size:24px; border-bottom:2px solid #f0c06033; padding-bottom:10px; margin-bottom:12px; }
        .group-title { color:#f0c060; font-size:15px; margin:22px 0 10px 0; padding-left:10px; border-left:3px solid #f0c06088; }
        .grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(280px,1fr)); gap:12px; }
        .card { background:#1a1a2e; border:1px solid #2a2a4a; border-radius:12px; padding:16px; transition:0.2s; }
        .card:hover { border-color:#f0c06066; }
        .card h3 { color:#f0c060; font-size:14px; margin-bottom:6px; }
        .card .status { font-size:12px; color:#888; margin-bottom:10px; min-height:16px; }
        .card button { background:#2a2a4a; border:1px solid #444; color:#e0e0e0; padding:8px 16px; border-radius:6px; cursor:pointer; font-family:monospace; font-size:13px; transition:0.2s; }
        .card button:hover { background:#f0c06022; border-color:#f0c060; }
        .card button:disabled { opacity:0.4; cursor:not-allowed; }
        .output { background:#0a0a12; border:1px solid #2a2a4a; border-radius:8px; padding:15px; margin-top:20px; max-height:420px; overflow:auto; font-size:12px; white-space:pre-wrap; word-break:break-all; }
        .row { display:flex; gap:12px; flex-wrap:wrap; margin-top:8px; }
        .stat { font-size:13px; color:#aaa; }
        .stat span { color:#f0c060; font-weight:bold; }
        .footer { margin-top:30px; font-size:11px; color:#444; border-top:1px solid #1a1a2e; padding-top:15px; }
    </style>
</head>
<body>
<div class="container">
    <h1>🐉 龍魂控制台 · UID9622</h1>
    <div class="row" style="margin-bottom:15px;">
        <div class="stat">⏰ <span id="time">{{ now }}</span></div>
        <div class="stat">🟢 系统: <span id="health">检查中...</span></div>
        <div class="stat">📦 命令: <span>{{ commands|length }}</span></div>
    </div>
    {% for gname, gcmds in groups.items() %}
    <h2 class="group-title">{{ gname }}</h2>
    <div class="grid">
        {% for cmd in gcmds %}
        <div class="card">
            <h3>{{ cmd.icon }} {{ cmd.name }}</h3>
            <div class="status">{{ cmd.desc }}</div>
            <button onclick="runCommand('{{ cmd.id }}')" id="btn-{{ cmd.id }}">▶ 执行</button>
            <div id="result-{{ cmd.id }}" style="margin-top:8px;font-size:11px;color:#666;"></div>
        </div>
        {% endfor %}
    </div>
    {% endfor %}
    <div class="output" id="output">等待命令执行... (点击按钮后输出会显示在这里)</div>
    <div class="footer">🐉 龍魂 Web 控制台 v2.0 · 21按钮·5分组 · DNA: #龍芯⚡️丙午·丙申·丙寅·甲午·䷕贲-WEB-CONSOLE-V2.0-UID9622</div>
</div>
<script>
async function runCommand(cmdId) {
    const btn = document.getElementById('btn-' + cmdId);
    const result = document.getElementById('result-' + cmdId);
    const output = document.getElementById('output');
    btn.textContent = '⏳ 执行中...';
    btn.disabled = true;
    result.textContent = '执行中...';
    output.textContent = '▶ 执行 ' + cmdId + ' ...\\n';
    try {
        const resp = await fetch('/run/' + cmdId, { method: 'POST' });
        const data = await resp.json();
        output.textContent = data.output || '（无输出）';
        result.textContent = '✅ 完成 (exit: ' + data.code + ')';
        result.style.color = (data.code === 0) ? '#00ff44' : '#ff4444';
    } catch(e) {
        output.textContent = '❌ 错误: ' + e.message;
        result.textContent = '❌ 失败';
        result.style.color = '#ff4444';
    }
    btn.textContent = '▶ 执行';
    btn.disabled = false;
}
fetch('/api/health').then(r=>r.json()).then(d=>{
    document.getElementById('health').textContent = d.status || 'unknown';
}).catch(()=>{ document.getElementById('health').textContent = '⚠️ 无法连接'; });
</script>
</body>
</html>
'''

# 命令列表（可根据需要增删 · group 分组）
COMMANDS = [
    # ========== 🛡️ 安全审计 ==========
    {"group": "🛡️ 安全审计", "id": "check_all", "name": "总开关体检", "desc": "Notion指令注册表总开关只读检查", "icon": "🔍", "cmd": ["python3", "08_BIN/lh_notion_command_registry.py", "run", "check", "--all"]},
    {"group": "🛡️ 安全审计", "id": "audit_log", "name": "审计日志", "desc": "查看最近50条审计记录(根目录audit_log.jsonl)", "icon": "📋", "cmd": ["tail", "-50", "audit_log.jsonl"]},
    {"group": "🛡️ 安全审计", "id": "full_audit", "name": "全系统三色审计", "desc": "lh audit · 全系统安全扫描", "icon": "🟢", "cmd": ["python3", "bin/lh.py", "audit"]},
    {"group": "🛡️ 安全审计", "id": "align_check", "name": "代码对齐检查", "desc": "扫描重复函数/缺失DNA/缺失GPG", "icon": "📐", "cmd": ["python3", "bin/lh_align_checker.py"]},
    {"group": "🛡️ 安全审计", "id": "gpg_scan", "name": "GPG签名扫描", "desc": "全项目签名完整性验证(可能较慢)", "icon": "🔏", "cmd": ["python3", "bin/lh_gpg_sign.py", "scan", "."]},

    # ========== 📊 状态监控 ==========
    {"group": "📊 状态监控", "id": "system_status", "name": "系统状态", "desc": "lh status · 模型Val·引擎·告警", "icon": "🧠", "cmd": ["python3", "bin/lh.py", "status"]},
    {"group": "📊 状态监控", "id": "ports", "name": "端口探测", "desc": "一键看全部核心服务死活", "icon": "📡", "cmd": ["python3", "-c", "import socket\nfor p in [8771,8773,8775,8777,8789,8800,8970,8999,9602,9631,8082]:\n    s=socket.socket(); ok=(s.connect_ex(('127.0.0.1',p))==0); s.close()\n    print(('🟢' if ok else '🔴'), p)"]},
    {"group": "📊 状态监控", "id": "engine_verify", "name": "引擎验证", "desc": "全量引擎健康验证 TCP+HTTP双探", "icon": "🔬", "cmd": ["python3", "bin/lh.py", "engine-verify"]},
    {"group": "📊 状态监控", "id": "dashboard", "name": "Mac端口全览", "desc": "lh --ports · 全端口矩阵·SSH隧道·launchd", "icon": "📈", "cmd": ["python3", "bin/lh.py", "--ports"]},
    {"group": "📊 状态监控", "id": "health_check", "name": "健康检查", "desc": "巡检+Bark告警推送", "icon": "🩺", "cmd": ["bash", "deploy/scripts/health_check.sh"]},

    # ========== 🔍 知识检索 ==========
    {"group": "🔍 知识检索", "id": "idx_status", "name": "认知索引状态", "desc": "lh idx status · 五层索引", "icon": "🧬", "cmd": ["python3", "bin/lh.py", "idx", "status"]},
    {"group": "🔍 知识检索", "id": "cat", "name": "命令分类目录", "desc": "lh cat · 302命令十二大类总览", "icon": "📚", "cmd": ["python3", "bin/lh.py", "cat"]},
    {"group": "🔍 知识检索", "id": "memory_load", "name": "加载焊死记忆", "desc": "系统状态·协作者·协议·底座锚点", "icon": "📦", "cmd": ["python3", "bin/lh_memory_load.py"]},
    {"group": "🔍 知识检索", "id": "te_stamp", "name": "当前时间戳", "desc": "干支四柱·卦象·三色相位", "icon": "🐉", "cmd": ["python3", "bin/lh.py", "te", "--stamp"]},

    # ========== ⚙️ 运维操作 ==========
    {"group": "⚙️ 运维操作", "id": "git_status", "name": "Git 状态", "desc": "查看未提交变更", "icon": "📁", "cmd": ["git", "status", "--short"]},
    {"group": "⚙️ 运维操作", "id": "git_commit_push", "name": "一键提交+推送", "desc": "git add -A → commit → push", "icon": "📤", "cmd": ["bash", "-c", "git add -A && git commit -m 'web-console auto commit' && git push"]},
    {"group": "⚙️ 运维操作", "id": "gpg_sign", "name": "GPG全量签名", "desc": "全项目补签(可能较慢)", "icon": "🔑", "cmd": ["python3", "bin/lh_gpg_sign.py", "sign", "."]},
    {"group": "⚙️ 运维操作", "id": "sync_kunpeng", "name": "同步鲲鹏", "desc": "推到 119.13.90.27", "icon": "🖥️", "cmd": ["bash", "deploy/sync-to-kunpeng.sh"]},
    {"group": "⚙️ 运维操作", "id": "cannon", "name": "三端推送", "desc": "GitHub+Gitee+GitCode", "icon": "🚀", "cmd": ["python3", "bin/lh_auto_cannon.py"]},

    # ========== 🧬 采集归档 ==========
    {"group": "🧬 采集归档", "id": "persona_health", "name": "人格健康度", "desc": "日卦交叉验证", "icon": "🧬", "cmd": ["python3", "08_BIN/lh_day_gua_verify.py", "--cross-check"]},
    {"group": "🧬 采集归档", "id": "stats", "name": "系统统计", "desc": "Notion指令注册表统计", "icon": "📊", "cmd": ["python3", "08_BIN/lh_notion_command_registry.py", "run", "stats", "--all"]},
]


def build_groups():
    groups = OrderedDict()
    for c in COMMANDS:
        groups.setdefault(c["group"], []).append(c)
    return groups


@app.route('/')
def index():
    return render_template_string(HTML, commands=COMMANDS, groups=build_groups(),
                                  now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "timestamp": datetime.datetime.now().isoformat(), "commands": len(COMMANDS)})


@app.route('/run/<cmd_id>', methods=['POST'])
def run(cmd_id):
    cmd_map = {c['id']: c for c in COMMANDS}
    if cmd_id not in cmd_map:
        return jsonify({"code": -1, "output": "未知命令ID"})
    cmd = cmd_map[cmd_id]['cmd']
    os.chdir(os.path.expanduser('~/longhun-system'))
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        return jsonify({"code": result.returncode, "output": result.stdout + result.stderr})
    except subprocess.TimeoutExpired:
        return jsonify({"code": -1, "output": "执行超时（300秒）"})
    except Exception as e:
        return jsonify({"code": -1, "output": str(e)})


if __name__ == '__main__':
    print("🐉 龍魂 Web 控制台 v2.0 启动中...")
    print("   🔗 访问: http://127.0.0.1:8082")
    print("   ⏹ 停止: pkill -f lh_web_console.py")
    # 安全：只绑定本机回环，不暴露局域网（控制台带执行命令能力）
    # 8080/8081 被透明仪表盘占用，改用 8082
    app.run(host='127.0.0.1', port=8082, debug=False)
