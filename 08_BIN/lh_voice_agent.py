#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丁酉·戊寅·亥时·䷇比-LH-VOICE-AGENT-v1.0-START
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""龍魂·语音遥控塔 v1.0 — Mac 端语音指令接收/转写/校验/执行服务。

链路: 手机(小艺/浏览器) → 音频或文本 → 本服务(:18880)
    → faster-whisper 转文字 → 一票否决词 + 黑名单 + 白名单校验
    → 执行(Mac 本机 / 鲲鹏 SSH) → 返回结果文本。

安全: 只读优先; 操作类需显式意图; 所有指令过十层一票否决词 + control_gate 黑名单 + 审计日志。
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

# ---- 常量 ----
PORT = 18880
AUDIT_LOG = os.path.expanduser("~/longhun-system/audit/voice_agent.jsonl")
KP_HOST = "119.13.90.27"
KP_KEY = os.path.expanduser("~/.ssh/longhun_kunpeng_ed25519")
# launchd 环境 PATH 无龙魂 python3，必须用绝对路径
PYTHON = "/Users/zuimeidedeyihan/.longhun/bin/python3"

# 十层一票否决词（规则第十层）
VETO_WORDS = [
    "技术无国界", "用户体验优先", "灵活处理", "国际接轨",
    "简化管理", "商业化需要", "平衡各方", "行业标准",
]

# Mac 侧可执行 lh 子命令白名单（只读为主）
ALLOWED_LH = [
    "health", "status", "search", "memory", "te", "dna", "idx",
    "time", "stat", "audit", "keys", "gpg", "lshw", "bcm",
]

# 鲲鹏侧命令白名单（正则前缀）
ALLOWED_KP = [
    r"^health_check", r"^systemctl status", r"^uptime", r"^df -h",
    r"^free -h", r"^ls /opt/longhun", r"^docker ps", r"^ps aux",
    r"^cat /opt/longhun/shared", r"^curl -s .*health",
]

# 打开 App 白名单
ALLOWED_APPS = {
    "浏览器": "Safari", "终端": "Terminal", "备忘录": "Notes",
    "音乐": "Music", "微信": "WeChat", "邮件": "Mail",
    "文件": "Finder", "计算器": "Calculator", "日历": "Calendar",
    "照片": "Photos", "设置": "System Settings", "龙魂": "Terminal",
}

# ---- 审计 ----
def audit(entry: dict) -> None:
    os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)
    entry.update({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "dna": "VOICE-AGENT"})
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# ---- 校验链 ----
def check_veto(text: str) -> str | None:
    for w in VETO_WORDS:
        if w in text:
            return f"命中一票否决词[{w}]（规则第十层）"
    return None

def check_blacklist(cmd: str) -> str | None:
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from lh_control_gate import check_blacklist_command
        return check_blacklist_command(cmd)
    except Exception:
        for pat in [r"rm -rf\s+/", r"git push --force", r"mkfs", r"dd\s+if=", r"shutdown", r"reboot"]:
            if re.search(pat, cmd):
                return f"命中黑名单: {pat}"
    return None

# ---- 执行层 ----
def exec_mac(cmd: str, timeout: int = 60) -> str:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        out = (r.stdout or "") + ("\n" + r.stderr if r.stderr else "")
        return (out or "（无输出）")[-2500:]
    except subprocess.TimeoutExpired:
        return "⏰ Mac 执行超时"
    except Exception as e:
        return f"❌ Mac 执行失败: {e}"

def exec_kunpeng(cmd: str, timeout: int = 45) -> str:
    ssh = [
        "ssh", "-i", KP_KEY, "-o", "ConnectTimeout=8",
        "-o", "StrictHostKeyChecking=no", f"root@{KP_HOST}", cmd,
    ]
    try:
        r = subprocess.run(ssh, capture_output=True, text=True, timeout=timeout)
        out = (r.stdout or "") + ("\n" + r.stderr if r.stderr else "")
        return (out or "（无输出）")[-2500:]
    except subprocess.TimeoutExpired:
        return "⏰ 鲲鹏执行超时"
    except Exception as e:
        return f"❌ 鲲鹏连接失败: {e}"

def open_app(app: str) -> str:
    target = ALLOWED_APPS.get(app)
    if not target:
        return f"❌ App 白名单未收录[{app}]，可打开: {'/'.join(ALLOWED_APPS)}"
    return exec_mac(f'open -a "{target}" && echo "已打开 {target}"', timeout=15)

def kp_allowed(cmd: str) -> bool:
    return any(re.match(p, cmd.strip()) for p in ALLOWED_KP)

def mac_lh_allowed(sub: str) -> bool:
    name = sub.split()[0] if sub.split() else ""
    return name in ALLOWED_LH

# ---- 意图解析 ----
def parse_and_execute(text: str) -> str:
    t = text.strip().strip("，。！？,.!?")
    if not t:
        return "❌ 空指令"
    v = check_veto(t)
    if v:
        return f"🚫 {v}，已拒绝执行"
    b = check_blacklist(t)
    if b:
        return f"🚫 {b}，已熔断"

    tl = t.lower()
    # 1) 显式目标前缀: kp:/鲲鹏: 或 mac:/lh:
    if tl.startswith("kp:") or tl.startswith("鲲鹏:"):
        cmd = t.split(":", 1)[1].strip()
        return exec_kunpeng(cmd) if kp_allowed(cmd) else f"🚫 鲲鹏命令不在白名单: {cmd}"
    if tl.startswith("lh ") or tl.startswith("mac:"):
        cmd = re.sub(r"^(lh |mac:)", "", t).strip()
        return exec_mac(f"cd ~/longhun-system && {PYTHON} bin/lh.py {cmd}") if mac_lh_allowed(cmd) else f"🚫 lh 子命令不在白名单: {cmd}"

    # 2) 自然语言意图
    if "鲲鹏" in t and any(k in t for k in ["健康", "状态", "体检", "检查", "好"]):
        return "🏔️ 鲲鹏健康:\n" + exec_kunpeng("bash /opt/longhun/deploy/scripts/health_check.sh --silent 2>/dev/null || systemctl list-units --type=service --state=running | wc -l", timeout=40)
    if any(k in t for k in ["健康", "状态", "体检", "好不好", "检查一下", "自检"]):
        r1 = exec_mac(f"cd ~/longhun-system && {PYTHON} bin/lh.py --health 2>/dev/null | tail -20")
        r2 = exec_kunpeng("uptime && echo --- && df -h / | tail -1 && echo --- && free -h | head -2")
        return "💻 Mac 状态:\n" + r1 + "\n\n🏔️ 鲲鹏状态:\n" + r2
    if t.startswith("搜索") or t.startswith("搜一下") or t.startswith("查一下"):
        q = re.sub(r"^(搜索|搜一下|查一下)", "", t).strip()
        return "🔍 搜索结果:\n" + exec_mac(f"cd ~/longhun-system && {PYTHON} bin/lh.py --search {q} 2>/dev/null | head -30", timeout=60)
    if "记忆" in t:
        return "🧠 记忆服务:\n" + exec_mac("cd ~/longhun-system && curl -s --max-time 5 http://127.0.0.1:8771/health 2>/dev/null || echo '记忆服务(8771)未响应'", timeout=20)
    if any(k in t for k in ["时间", "时辰", "现在几点", "几点了"]):
        return "⏰ " + exec_mac(f"cd ~/longhun-system && {PYTHON} bin/lh.py --te --stamp 2>/dev/null | tail -3", timeout=20)
    if t.startswith("打开"):
        app = t[2:].strip()
        return open_app(app)
    if any(k in t for k in ["帮助", "help", "怎么用", "指令"]):
        return ("🗺️ 语音遥控塔可用指令:\n"
                "  · 状态/健康/体检 → Mac+鲲鹏 双机状态\n"
                "  · 搜索 <词> / 查一下 <词> → 龙魂搜索\n"
                "  · 记忆 → 记忆服务状态\n"
                "  · 打开 <App> → 浏览器/终端/备忘录…\n"
                "  · 时间 → 干支卦时间戳\n"
                "  · 鲲鹏: <命令> → 鲲鹏执行(白名单)\n"
                "  · lh <子命令> → Mac 执行 lh")
    return "🤔 没听懂。说\"帮助\"看可用指令；或直接用: 鲲鹏:xxx / lh xxx / 打开xxx"

# ---- HTTP ----
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code: int, body: str, ctype: str = "application/json; charset=utf-8"):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Key")
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self._send(204, "")

    def do_GET(self):
        p = urlparse(self.path).path
        if p in ("/", "/v1/status", "/health"):
            self._send(200, json.dumps({"ok": True, "service": "lh-voice-agent", "port": PORT,
                                        "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z")}))
        else:
            self._send(404, json.dumps({"ok": False, "error": "not found"}))

    def do_POST(self):
        p = urlparse(self.path).path
        try:
            if p == "/v1/text":
                n = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(n) or b"{}")
                text = (payload.get("text") or "").strip()
                if not text:
                    self._send(400, json.dumps({"ok": False, "error": "text 为空"}))
                    return
                audit({"op": "text", "text": text[:200], "ip": self.client_address[0]})
                result = parse_and_execute(text)
                audit({"op": "text_result", "ok": not result.startswith(("🚫", "❌", "🤔")), "text": text[:100], "result": result[:200]})
                self._send(200, json.dumps({"ok": True, "result": result}))
            elif p == "/v1/audio":
                n = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(n)
                if n < 1024:
                    self._send(400, json.dumps({"ok": False, "error": "音频过小"}))
                    return
                ext = (self.headers.get("X-Audio-Ext") or "wav").lstrip(".")
                tmp = os.path.join(tempfile.gettempdir(), f"va_{uuid.uuid4().hex[:8]}.{ext}")
                with open(tmp, "wb") as f:
                    f.write(raw)
                audit({"op": "audio_received", "bytes": n, "ip": self.client_address[0]})
                try:
                    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                    from voice_input import transcribe_audio
                    text = transcribe_audio(file_path=tmp, language="zh").strip()
                except Exception as e:
                    text = ""
                    self._send(500, json.dumps({"ok": False, "error": f"转写失败: {str(e)[:200]}"}))
                    return
                finally:
                    try:
                        os.remove(tmp)
                    except Exception:
                        pass
                if not text:
                    self._send(200, json.dumps({"ok": False, "result": "🎙️ 没听清，再说一遍？", "text": ""}))
                    return
                result = parse_and_execute(text)
                audit({"op": "audio_result", "text": text[:200], "result": result[:200]})
                self._send(200, json.dumps({"ok": True, "text": text, "result": result}))
            else:
                self._send(404, json.dumps({"ok": False, "error": "not found"}))
        except Exception as e:
            self._send(500, json.dumps({"ok": False, "error": str(e)[:300]}))


def main():
    host = os.environ.get("VA_HOST", "0.0.0.0")
    port = int(os.environ.get("VA_PORT", PORT))
    srv = ThreadingHTTPServer((host, port), Handler)
    print(f"🐉 龍魂语音遥控塔 v1.0 就绪 | http://{host}:{port} | {time.strftime('%Y-%m-%dT%H:%M:%S%z')}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止")


if __name__ == "__main__":
    main()
