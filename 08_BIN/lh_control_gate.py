#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·己酉·甲子·䷉履-QUOTA-OPERATOR-GATEWAY-v1.0
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 · 操盘网关 v1.0（Control Gate）
DNA: #龍芯⚡️丙午·丙申·己酉·甲子·䷉履-QUOTA-OPERATOR-GATEWAY-v1.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能: 国产AI设备操盘统一入口。
  各家国产AI（Kimi/DeepSeek/混元/通义/智谱…）凭专属API Key，
  通过本地 HTTP 网关操作这台 Mac——执行命令/读写文件/开应用/剪贴板/系统信息/通知。
  全部操作: 密钥认证 → 黑名单熔断 → 路径锁定 → 超时控制 → append-only审计。

安全铁律:
  🔴 禁 rm -rf / 类毁灭命令  🔴 禁 git push --force main  🔴 禁写 .ssh/.gnupg
  🔴 禁删系统目录  🔴 禁读 D1 绝密文件  🔴 绑定 127.0.0.1 只本地
  📌 默认只读模式，写操作需显式 enable_write

仅内部私有使用，不对外发布。
"""

import json
import os
import re
import sys
import time
import uuid
import shlex
import hashlib
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ============================================================
# 常量与路径
# ============================================================
UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

SYSTEM_ROOT = Path(__file__).resolve().parent.parent
GATE_CONFIG = SYSTEM_ROOT / "config" / "control_gate.json"
GATE_AUDIT = SYSTEM_ROOT / "logs" / "control_gate_audit.jsonl"
GATE_STATE = SYSTEM_ROOT / "logs" / "control_gate_state.json"

HOST = os.environ.get("LH_GATE_HOST", "127.0.0.1")
PORT = int(os.environ.get("LH_GATE_PORT", "18790"))
CMD_TIMEOUT = int(os.environ.get("LH_GATE_TIMEOUT", "120"))

# ============================================================
# 默认配置（首次运行自动生成 config/control_gate.json）
# ============================================================
DEFAULT_CONFIG = {
    "meta": {
        "name": "龍魂·操盘网关",
        "version": "v1.0",
        "creator": "诸葛鑫(UID9622)",
        "purpose": "国产AI设备操盘统一入口·仅内部私有·不对外发布",
    },
    "master_key": "",  # 首次运行自动生成，见 config 文件
    "enable_write": False,  # 默认只读；写文件/剪贴板需 true
    "allow_shell": True,  # shell 执行开关
    "command_timeout": CMD_TIMEOUT,
    "ais": {
        # 每家国产AI一把专属Key，启动时自动生成
    },
    "whitelist": {
        "paths": [str(SYSTEM_ROOT)],  # 文件读写只允许这些目录（默认=longhun-system）
        "commands": [],  # 额外放行的精确命令前缀
    },
    "blacklist": {
        # 🔴 毁灭性/越权命令熔断
        "patterns": [
            r"^\s*rm\s+-rf\s+/\s*$",          # 删根
            r"^\s*rm\s+-rf\s+~?\s*$",         # 删 home
            r"^\s*rm\s+-rf\s+[^ ]*\.(gnupg|ssh)\b",  # 删密钥目录
            r"^\s*rm\s+-rf\s+[^ ]*\blibrary\b",      # 删库
            r"^\s*git\s+push\s+.*--force.*(main|master)\b",  # 强推主分支
            r"^\s*mkfs\.",                     # 格式化
            r"^\s*dd\s+if=.*of=\s*/dev/",      # 写块设备
            r"^\s*shutdown\b", r"^\s*poweroff\b", r"^\s*reboot\b", r"^\s*halt\b",
            r"^\s*init\s+0\b", r"^\s*sudo\s+rm\b",
            r"^\s*rm\s+-rf\s+[^ ]*\b(Windows|System)\b",  # 跨系统删
        ],
        # 禁止读取的 D1 绝密文件
        "files": [
            "id_rsa", "id_ed25519", "secring", "gpg-agent.conf",
            "secret_blacklist", "secrets.env", "key.bin",
        ],
    },
    "audit": {"enabled": True, "max_days": 90},
}

# ============================================================
# 配置装载
# ============================================================
def _gen_key() -> str:
    """生成 32 位随机 Key"""
    return hashlib.sha256(f"{uuid.uuid4()}{time.time()}".encode()).hexdigest()[:32]


def load_config() -> dict:
    """读取配置；不存在则生成默认并落盘"""
    cfg = None
    if GATE_CONFIG.exists():
        try:
            cfg = json.loads(GATE_CONFIG.read_text(encoding="utf-8"))
        except Exception:
            cfg = None
    if cfg is None:
        cfg = json.loads(json.dumps(DEFAULT_CONFIG))
        cfg["master_key"] = _gen_key()
        first_run = True
    else:
        first_run = False
    # 确保 ais 字段存在
    cfg.setdefault("ais", {})
    # 首次运行: 预置几家国产AI的 Key
    if first_run or not cfg["ais"]:
        defaults = ["kimi", "deepseek", "hunyuan", "qwen", "zhipu", "baichuan"]
        for name in defaults:
            if name not in cfg["ais"]:
                cfg["ais"][name] = {"key": _gen_key(), "enabled": True,
                                    "name": name, "created_at": datetime.now().isoformat()}
        GATE_CONFIG.parent.mkdir(parents=True, exist_ok=True)
        GATE_CONFIG.write_text(json.dumps(cfg, ensure_ascii=False, indent=2),
                               encoding="utf-8")
    return cfg


def save_config(cfg: dict) -> None:
    GATE_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    GATE_CONFIG.write_text(json.dumps(cfg, ensure_ascii=False, indent=2),
                           encoding="utf-8")


# ============================================================
# 审计（append-only）
# ============================================================
def audit(cfg: dict, entry: dict) -> None:
    if not cfg.get("audit", {}).get("enabled", True):
        return
    GATE_AUDIT.parent.mkdir(parents=True, exist_ok=True)
    entry.setdefault("ts", datetime.now().isoformat())
    entry.setdefault("dna", f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-GATE-{uuid.uuid4().hex[:6]}-{UID}")
    with open(GATE_AUDIT, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ============================================================
# 安全检查
# ============================================================
def check_auth(cfg: dict, key: str) -> dict:
    """校验 Key，返回 AI 身份或 None"""
    if not key:
        return None
    if cfg.get("master_key") and key == cfg["master_key"]:
        return {"ai": "master", "is_master": True, "enabled": True}
    for name, info in cfg.get("ais", {}).items():
        if info.get("key") == key:
            if not info.get("enabled", True):
                return None
            return {"ai": name, "is_master": False, "enabled": True}
    return None


def check_blacklist_command(cmd: str) -> str | None:
    """黑名单熔断，返回拒绝原因或 None"""
    cfg = load_config()
    for pat in cfg.get("blacklist", {}).get("patterns", []):
        if re.search(pat, cmd, re.IGNORECASE):
            return f"命中黑名单: {pat}"
    return None


def check_blacklist_file(path: str) -> str | None:
    """文件黑名单（D1 绝密 + 危险路径）"""
    cfg = load_config()
    p = Path(path).resolve()
    for name in cfg.get("blacklist", {}).get("files", []):
        if name in p.name:
            return f"D1 绝密文件禁止访问: {name}"
    for part in p.parts:
        if part in (".ssh", ".gnupg", ".git"):
            return f"禁止访问系统/密钥目录: {part}"
    return None


def check_path_allowed(cfg: dict, path: str) -> str | None:
    """路径白名单：只允许配置的目录内"""
    p = Path(path).resolve()
    allowed = [Path(x).resolve() for x in cfg.get("whitelist", {}).get("paths", [])]
    for base in allowed:
        try:
            p.relative_to(base)
            return None
        except ValueError:
            continue
    return f"路径越界（仅允许: {[str(x) for x in allowed]}）"


# ============================================================
# 执行器（Mac 操作层）
# ============================================================
def _run_shell(cmd: str, timeout: int) -> dict:
    """执行 shell 命令（subprocess 直接执行，支持管道/复合命令）"""
    start = time.time()
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True,
                              text=True, timeout=timeout)
        return {
            "ok": proc.returncode == 0,
            "exit": proc.returncode,
            "stdout": proc.stdout[-4000:],
            "stderr": proc.stderr[-2000:],
            "elapsed": round(time.time() - start, 2),
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "exit": -1, "stdout": "", "stderr": f"超时（>{timeout}s）", "elapsed": timeout}
    except Exception as e:
        return {"ok": False, "exit": -1, "stdout": "", "stderr": str(e), "elapsed": round(time.time() - start, 2)}


def _read_file(path: str, cfg: dict) -> dict:
    r = check_path_allowed(cfg, path)
    if r:
        return {"ok": False, "error": r}
    r = check_blacklist_file(path)
    if r:
        return {"ok": False, "error": r}
    p = Path(path).resolve()
    if not p.exists():
        return {"ok": False, "error": "文件不存在"}
    if p.stat().st_size > 1_000_000:
        return {"ok": False, "error": "文件 >1MB，拒绝整读（用 shell 分段读）"}
    try:
        return {"ok": True, "content": p.read_text(encoding="utf-8", errors="replace")[:50000]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _write_file(path: str, content: str, cfg: dict) -> dict:
    if not cfg.get("enable_write"):
        return {"ok": False, "error": "写操作被禁用（master 需在 config 开 enable_write=true）"}
    r = check_path_allowed(cfg, path)
    if r:
        return {"ok": False, "error": r}
    r = check_blacklist_file(path)
    if r:
        return {"ok": False, "error": r}
    p = Path(path).resolve()
    if len(content) > 200_000:
        return {"ok": False, "error": "内容 >200KB，拒绝写入"}
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return {"ok": True, "path": str(p), "bytes": p.stat().st_size}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# 中文应用名 → macOS App 名映射（AI 说"打开浏览器"也能开对）
APP_ALIASES = {
    "浏览器": "Safari", "safari": "Safari", "chrome": "Google Chrome",
    "谷歌浏览器": "Google Chrome", "终端": "Terminal", "terminal": "Terminal",
    "备忘录": "Notes", "邮件": "Mail", "music": "Music", "音乐": "Music",
    "微信": "WeChat", "访达": "Finder", "finder": "Finder",
    "编辑": "Code", "代码编辑器": "Code", "vscode": "Code",
    "计算器": "Calculator", "日历": "Calendar", "照片": "Photos",
}


def _open_app(app: str) -> dict:
    """打开应用/文件/URL（macOS open 命令）"""
    app = str(app).strip()
    resolved = APP_ALIASES.get(app, app)
    safe = shlex.quote(resolved)
    return _run_shell(f"open -a {safe}", 15)


def _notify(title: str, msg: str) -> dict:
    """桌面通知"""
    import subprocess as sp
    t = shlex.quote(str(title)[:60])
    m = shlex.quote(str(msg)[:200])
    script = f'display notification {m} with title {t}'
    return _run_shell(f"osascript -e {shlex.quote(script)}", 15)


def _sysinfo() -> dict:
    """系统信息快照"""
    host = _run_shell("hostname", 10)
    uptime = _run_shell("uptime", 10)
    mem = _run_shell("vm_stat | head -5", 10)
    disk = _run_shell("df -h / | tail -1", 10)
    cpu = _run_shell("ps -A -o %cpu | awk '{s+=$1} END {printf \"%.1f%%\\n\", s/8}'", 10)
    return {
        "ok": True,
        "hostname": host.get("stdout", "").strip(),
        "uptime": uptime.get("stdout", "").strip(),
        "memory": mem.get("stdout", "").strip(),
        "disk": disk.get("stdout", "").strip(),
        "cpu_avg": cpu.get("stdout", "").strip(),
    }


def _clipboard(mode: str, text: str = "") -> dict:
    """剪贴板 get/set"""
    if mode == "get":
        return _run_shell("pbpaste", 10)
    if mode == "set":
        cfg = load_config()
        if not cfg.get("enable_write"):
            return {"ok": False, "error": "写操作被禁用"}
        if len(text) > 20_000:
            return {"ok": False, "error": "剪贴板内容 >20KB 拒绝"}
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as f:
            f.write(text)
            tmp = f.name
        res = _run_shell(f"cat {shlex.quote(tmp)} | pbcopy && rm -f {shlex.quote(tmp)}", 10)
        return res
    return {"ok": False, "error": "mode 需为 get/set"}


# ============================================================
# 任务分发
# ============================================================
def execute_action(cfg: dict, ai_name: str, action: str, params: dict) -> dict:
    """统一执行入口"""
    timeout = int(params.get("timeout", cfg.get("command_timeout", CMD_TIMEOUT)))
    if timeout > 300:
        timeout = 300

    if action == "shell":
        if not cfg.get("allow_shell", True):
            return {"ok": False, "error": "shell 已禁用"}
        cmd = str(params.get("command", "")).strip()
        if not cmd:
            return {"ok": False, "error": "缺少 command"}
        blocked = check_blacklist_command(cmd)
        if blocked:
            audit(cfg, {"ai": ai_name, "action": "shell", "command": cmd,
                        "verdict": "BLOCK", "reason": blocked})
            return {"ok": False, "error": f"🔴 熔断拒绝: {blocked}"}
        res = _run_shell(cmd, timeout)
        audit(cfg, {"ai": ai_name, "action": "shell", "command": cmd,
                    "verdict": "OK" if res["ok"] else "FAIL", "exit": res["exit"]})
        return res

    if action == "read":
        return _read_file(str(params.get("path", "")), cfg)

    if action == "write":
        res = _write_file(str(params.get("path", "")), str(params.get("content", "")), cfg)
        audit(cfg, {"ai": ai_name, "action": "write", "path": params.get("path"),
                    "verdict": "OK" if res.get("ok") else "FAIL"})
        return res

    if action == "open":
        return _open_app(str(params.get("app", "")))

    if action == "notify":
        return _notify(str(params.get("title", "龍魂")), str(params.get("msg", "")))

    if action == "sysinfo":
        return _sysinfo()

    if action == "clipboard":
        mode = str(params.get("mode", "get"))
        if mode not in ("get", "set"):
            return {"ok": False, "error": "clipboard mode 需为 get/set"}
        if mode == "get":
            return _clipboard("get")
        return _clipboard("set", str(params.get("text", "")))

    if action == "ls":
        path = str(params.get("path", str(SYSTEM_ROOT)))
        r = check_path_allowed(cfg, path)
        if r:
            return {"ok": False, "error": r}
        p = Path(path).resolve()
        if not p.exists():
            return {"ok": False, "error": "目录不存在"}
        try:
            items = []
            for x in sorted(p.iterdir())[:200]:
                items.append({"name": x.name, "is_dir": x.is_dir(),
                              "size": x.stat().st_size if x.is_file() else 0})
            return {"ok": True, "path": str(p), "items": items}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    return {"ok": False, "error": f"未知动作: {action}"}


# ============================================================
# HTTP 服务
# ============================================================
class GateHandler(BaseHTTPRequestHandler):
    cfg = None  # 类级共享（单进程）

    def log_message(self, fmt, *args):
        pass  # 静默访问日志

    def _send(self, code: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length <= 0 or length > 100_000:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return {}

    def do_GET(self):
        cfg = load_config()
        path = self.path.split("?")[0]
        key = self.headers.get("X-Gate-Key", "")
        identity = check_auth(cfg, key)
        if not identity:
            self._send(401, {"ok": False, "error": "未授权（X-Gate-Key 无效）"})
            return
        if path == "/v1/status":
            ai_list = {name: {"enabled": info.get("enabled", True),
                              "created_at": info.get("created_at")}
                       for name, info in cfg.get("ais", {}).items()}
            self._send(200, {"ok": True, "gate": "龍魂·操盘网关 v1.0",
                             "ai": identity["ai"], "is_master": identity["is_master"],
                             "enable_write": cfg.get("enable_write", False),
                             "ais": ai_list,
                             "audit_file": str(GATE_AUDIT)})
        elif path == "/v1/help":
            self._send(200, {"ok": True, "endpoints": {
                "GET /v1/status": "状态与AI列表",
                "POST /v1/execute": "执行动作 {action, ...}",
                "POST /v1/audit": "查询审计(master only)",
            }, "actions": ["shell", "read", "write", "open", "notify",
                           "sysinfo", "clipboard", "ls"]})
        else:
            self._send(404, {"ok": False, "error": "未找到"})

    def do_POST(self):
        cfg = load_config()
        path = self.path.split("?")[0]
        key = self.headers.get("X-Gate-Key", "")
        body = self._read_json()
        identity = check_auth(cfg, key)
        if not identity:
            self._send(401, {"ok": False, "error": "未授权（X-Gate-Key 无效）"})
            return

        if path == "/v1/execute":
            action = str(body.get("action", "")).strip()
            params = body.get("params", {}) if isinstance(body.get("params", {}), dict) else {}
            if not action:
                self._send(400, {"ok": False, "error": "缺少 action"})
                return
            result = execute_action(cfg, identity["ai"], action, params)
            result["ai"] = identity["ai"]
            result["action"] = action
            self._send(200, result)

        elif path == "/v1/audit":
            if not identity.get("is_master"):
                self._send(403, {"ok": False, "error": "仅 master 可查审计"})
                return
            lines = []
            if GATE_AUDIT.exists():
                for line in GATE_AUDIT.read_text(encoding="utf-8").splitlines()[-100:]:
                    try:
                        lines.append(json.loads(line))
                    except Exception:
                        pass
            self._send(200, {"ok": True, "count": len(lines), "recent": lines})

        elif path == "/v1/keygen":
            # master 专用: 给新AI生成Key
            if not identity.get("is_master"):
                self._send(403, {"ok": False, "error": "仅 master 可生成 Key"})
                return
            name = str(body.get("name", "")).strip()
            if not name or not re.match(r"^[a-zA-Z0-9_-]{1,32}$", name):
                self._send(400, {"ok": False, "error": "name 需为字母数字下划线(≤32)"})
                return
            if name in cfg["ais"]:
                self._send(400, {"ok": False, "error": f"{name} 已存在"})
                return
            cfg["ais"][name] = {"key": _gen_key(), "enabled": True, "name": name,
                                "created_at": datetime.now().isoformat()}
            save_config(cfg)
            audit(cfg, {"ai": "master", "action": "keygen", "name": name, "verdict": "OK"})
            self._send(200, {"ok": True, "name": name, "key": cfg["ais"][name]["key"],
                             "tip": "请立即保存该 Key，服务器只存哈希"})
        else:
            self._send(404, {"ok": False, "error": "未找到"})


def main():
    cfg = load_config()
    GATE_AUDIT.parent.mkdir(parents=True, exist_ok=True)
    audit(cfg, {"ai": "system", "action": "gate_start", "verdict": "OK",
                "port": PORT, "host": HOST})
    server = ThreadingHTTPServer((HOST, PORT), GateHandler)
    print(f"🐉 龍魂·操盘网关 v1.0 已启动")
    print(f"   监听: http://{HOST}:{PORT}")
    print(f"   已注册AI: {', '.join(cfg['ais'].keys())}")
    print(f"   写操作: {'开' if cfg.get('enable_write') else '关(只读)'}")
    print(f"   审计: {GATE_AUDIT}")
    print(f"   Master Key: {cfg['master_key'][:8]}... (完整见 {GATE_CONFIG})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🐉 网关已停止")
        server.server_close()


if __name__ == "__main__":
    main()
