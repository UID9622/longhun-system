#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丁酉·乙亥·巳时·䷝离-CIL-API-GATEWAY-V2.2-OPEN-PLATFORM
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 协议配套: docs/对外接口协议-v1.0.md（§7 归一审计）
"""
🐉 龍魂 CIL API 网关 v2.2 — 开放平台（默认只监听 127.0.0.1）

v4.4 Registry 融合（2026-09-05 · M99 融合第二笔实账）:
  - 原 :9623 龍魂注册中心 v2.0(registry_server.py·纯内存无状态薄壳)挂载至 /v1/reg/{health,nodes,stats,audit,node/<id>}
  - POST 写面保留: /v1/reg/heartbeat · /v1/reg/audit/report（节点心跳通道不可断）
  - 懒加载 importlib 跨目录加载 deploy/longhun-registry/registry_server.py（模块级内存态·易失·心跳恢复）
  - 心跳客户端 com.longhun.heartbeat → localhost:9622/v1/reg（plist 双改: ProgramArguments + EnvironmentVariables）
  - 原 com.longhun.registry 停用 → 进程 -1 · 端口 -1 · 数据语义零变化(127.0.0.1 内网·无确认码闸门)

v2.3 ADS 融合（2026-09-05 · M99 最小融合·总账 P0 Item1 第一笔实账）:
  - 原 :9626 自描述子系统(ADS v4.0)只读六端点挂载至 /v1/self/{health,describe,history,diagnose,boundary,roles}
  - 懒加载模块(首次请求才 import)·复用网关归一审计·确认码闸门语义保持(无码403=在线探针可用)
  - 写面(evolve/rollback)不挂载 · 原 com.longhun.ads 停用 → 进程 -1 · 端口 -1

v2.2 开放集成（2026-09-04 · Open Platform）:
  - 对外前缀 /api/v1/*（nginx 反代 · 后端内部路径归一 /api/v1 → /）
  - X-API-Key 认证 + 角色分级 viewer < auditor < admin（~/.longhun/api_keys.json）
  - 新端点: GET /v1/judge/shamewall · GET /v1/memorial/verify
           POST /v1/judge/scan(auditor+) · POST /v1/dh/dispatch(admin)
  - keygen: 生成/管理 API Key（lh_api.py keygen --role admin --name <名字>）
  - 数据镜像: 鲲鹏部署读 ROOT/data/ 只读镜像（shame_wall/contributor_memorial）
  - 写端点=审计登记式（完整执行在数据主权端 Mac·见 docs/龙魂API集成指南-v1.0.md）

v2.1 归一审计（2026-09-01）:
  - 响应头: X-Longhun-Trace:<node_id> · X-Longhun-DigitalRoot:<dr> · X-Longhun-Audit:<🟢/🟡/🔴>
  - 响应 body 末尾自动追加 "\n# 龍魂DNA: <node_id>|DR:<dr>|五行:<el>|审计:<audit>|创建:<ts>"
  - 外部调用审计: ~/.longhun/logs/external_calls.log（只记非 127.0.0.1，append-only）
  - 节点注册表:   ~/.longhun/nodes_registry.jsonl（全部调用·供 lh trace 反向追溯）
  - --host 默认 127.0.0.1；显式 0.0.0.0 对外开放时自动开启归一审计日志

接口:
  POST /v1/lh   body: {"command": "flow 龙魂对外首发 --json"}
                 → 调 bin/lh.py 执行 → 返回 {code, stdout, stderr} + 归一回流头 + DNA 行
  GET  /health  存活自检 → {"status":"ok","version":"v4.0","uptime":"..."}
  GET  /v1/topo              全部拓扑图谱索引（JSON）
  GET  /v1/topo/通心译        单图谱 19 节点树（JSON·含 groups/assets/根哈希）
  GET  /v1/topo/通心译/html   人类可读拓扑页（HTML·页脚主权声明+根哈希）
                 ↑ v1.0 拓扑开放接口（2026-09-02·M77 零中间层·复用 lh_topo 缓存）

运维:
  --log-level debug|info|warn|error · --pidfile · --host
  日志 ~/.longhun/logs/gateway.log（RotatingFileHandler 3 份 × 10MB）

用法:
  python3 08_BIN/lh_api.py [--port 9622] [--daemon] [--log-level info] [--host 127.0.0.1]

零依赖（标准库 http.server + logging.handlers）。
"""

import argparse
import contextlib
import hashlib
import json
import logging
import logging.handlers
import os
import re
import shlex
import subprocess
import sys
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
LH = ROOT / "bin" / "lh.py"
HOME_DIR = Path.home()
LH_DIR = HOME_DIR / ".longhun"
LOG_DIR = LH_DIR / "logs"
LOG_FILE = LOG_DIR / "gateway.log"
EXTERNAL_LOG = LOG_DIR / "external_calls.log"   # 外部调用审计（非本机·append-only）
NODES_REG = LH_DIR / "nodes_registry.jsonl"     # 节点注册表（全部调用·供 lh trace）
PID_FILE = LH_DIR / "gateway.pid"

# ── v2.2 开放平台：API Key + 数据镜像 + 审计登记（2026-09-04）────────
API_KEYS_FILE = LH_DIR / "api_keys.json"      # {"keys": {key: {role,name,created,note}}}
ROLE_LEVEL = {"viewer": 1, "auditor": 2, "admin": 3}
ROLE_CN = {"viewer": "只读", "auditor": "审计可触发", "admin": "全权"}
# 数据镜像目录：鲲鹏部署 = /apps/lh-api/data（只读快照·Mac rsync 同步）
DATA_DIR = ROOT / "data"
SHAME_MIRROR = DATA_DIR / "shame_wall.json"           # 耻辱墙镜像（Mac ~/.longhun/shame_wall）
EVIDENCE_MIRROR = DATA_DIR / "evidence.json"          # 生态证据链镜像（Mac lh evidence seal 导出·v1.0）
MEMORIAL_MIRROR = DATA_DIR / "contributor_memorial.json"  # 铭碑镜像（Mac 07_AUDIT）
SCAN_REQ_LOG = DATA_DIR / "scan_requests.log"         # judge/scan 登记（append-only）
DH_REQ_LOG = DATA_DIR / "dh_dispatch.log"             # dh/dispatch 登记（append-only）

HOST = "127.0.0.1"  # 🔒 默认只监听本地 · 永不默认 0.0.0.0
VERSION = "4.4"
DNA = "#龍芯⚡️丙午·丁酉·乙亥·巳时·䷝离-CIL-API-GATEWAY-v2.0"
START_TIME = time.time()

LOG_LEVELS = ("debug", "info", "warn", "error")

WUXING = ("水", "火", "木", "金", "土")
NODE_RE = re.compile(r"\{.*\}", re.DOTALL)
NODE_ID_RE = re.compile(r"^([A-Za-z]{2,16})-9622-([0-9A-F]{8})$")
# HTTP 响应头只能 latin-1：审计色在 header 用 ASCII 码，body DNA 行保留 emoji
AUDIT_HEADER = {"🟢": "GREEN", "🟡": "YELLOW", "🔴": "RED"}


def _uptime() -> str:
    s = int(time.time() - START_TIME)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h}h {m}m {sec}s"
    if m:
        return f"{m}m {sec}s"
    return f"{sec}s"


def _digital_root(text: str) -> int:
    """数字根·洛书369口径：字符码点和迭代至个位。"""
    n = sum(ord(c) for c in text)
    while n > 9:
        n = sum(int(x) for x in str(n))
    return n


def _make_node(command: str) -> dict:
    """从命令生成最小 Node（stdout 解析失败时兜底）。"""
    dr = _digital_root(command)
    return {
        "node_id": f"LH-9622-{hashlib.sha256(command.encode('utf-8')).hexdigest()[:8].upper()}",
        "digital_root": dr,
        "element": WUXING[(dr - 1) % 5],
        "gua": "离",
        "audit": "🟢" if dr <= 5 else "🟡",
        "action": "enter" if dr <= 4 else "stay",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }


# ── ADS 自描述懒加载（v2.3 融合 · 首次请求才 import，不污染网关启动）────
_ADS_SYS: Any | None = None


def _get_ads() -> Any:
    """懒加载 SelfDescribingSystem（模块级单例）。失败抛回 Handler 兜底。"""
    global _ADS_SYS
    if _ADS_SYS is None:
        from lh_self_describing import SelfDescribingSystem  # noqa: PLC0415
        _ADS_SYS = SelfDescribingSystem()
    return _ADS_SYS


# ── Registry 注册中心懒加载（v4.4 融合 · 原 :9623 → /v1/reg/*）────
_REG: Any = None
_REG_PATH = ROOT / "deploy" / "longhun-registry" / "registry_server.py"


def _get_reg() -> Any:
    """importlib 跨目录加载 registry_server.py（模块级单例·纯内存态·无副作用）。

    复用其 nodes/node_history/node_audit_results/常量——网关零复制数据源。
    原进程停用后：注册数据易失(心跳≤300s 自动恢复)·与独立运行语义一致。
    """
    global _REG
    if _REG is None:
        import importlib.util  # noqa: PLC0415
        spec = importlib.util.spec_from_file_location("lh_registry_embed", _REG_PATH)
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        sys.modules["lh_registry_embed"] = mod
        spec.loader.exec_module(mod)
        _REG = mod
    return _REG


def _extract_node(stdout: str, command: str) -> dict:
    """优先从 lh --json 输出提取真实 Node，失败则兜底生成。"""
    m = NODE_RE.search(stdout or "")
    if m:
        try:
            d = json.loads(m.group(0))
            if isinstance(d, dict) and d.get("node_id"):
                return d
        except Exception:  # noqa: BLE001
            pass
    return _make_node(command)


def setup_logging(level: str) -> logging.Logger:
    """日志 → ~/.longhun/logs/gateway.log · 自动轮转 3 份 × 10MB。"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger = logging.getLogger("lh_api")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def write_pidfile(pidfile: Path) -> None:
    pidfile.parent.mkdir(parents=True, exist_ok=True)
    pidfile.write_text(str(os.getpid()), encoding="utf-8")


def remove_pidfile(pidfile: Path) -> None:
    try:
        if pidfile.exists():
            pidfile.unlink()
    except OSError:
        pass


def _append_jsonl(path: Path, rec: dict, max_lines: int = 0) -> None:
    """append-only JSONL 写入；max_lines>0 时超限截断保留最新。"""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if max_lines and path.exists() and path.stat().st_size > 0:
            try:
                with path.open("r", encoding="utf-8") as f:
                    lines = f.readlines()
                if len(lines) >= max_lines:
                    with path.open("w", encoding="utf-8") as f:
                        f.writelines(lines[-max_lines:])
            except OSError:
                pass
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError:
        pass


# ── v2.2 API Key 认证（X-API-Key · ~/.longhun/api_keys.json）──────────
def load_api_keys() -> dict:
    try:
        if API_KEYS_FILE.exists():
            d = json.loads(API_KEYS_FILE.read_text(encoding="utf-8"))
            if isinstance(d, dict) and isinstance(d.get("keys"), dict):
                return d
    except Exception:  # noqa: BLE001
        pass
    return {"keys": {}}


def save_api_keys(data: dict) -> None:
    API_KEYS_FILE.parent.mkdir(parents=True, exist_ok=True)
    API_KEYS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                             encoding="utf-8")


def gen_api_key(role: str = "viewer", name: str = "", note: str = "") -> str:
    """生成新 API Key 并登记（唯一管理入口=UID9622 本机执行）。"""
    import secrets
    key = secrets.token_hex(12)
    data = load_api_keys()
    data.setdefault("keys", {})[key] = {
        "role": role if role in ROLE_LEVEL else "viewer",
        "name": name or "unnamed",
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "note": note,
    }
    save_api_keys(data)
    return key


def check_api_key(raw: str) -> dict | None:
    """校验 X-API-Key → {"key","role","name"} 或 None（无效/未登记）。"""
    if not raw:
        return None
    info = load_api_keys().get("keys", {}).get(raw.strip())
    if not info:
        return None
    return {"key": raw.strip(), "role": info.get("role", "viewer"),
            "name": info.get("name", "")}


def read_mirror(path: Path) -> dict | None:
    """读数据镜像 JSON（不存在返回 None）。"""
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        pass
    return None


def append_reg(log_path: Path, rec: dict) -> None:
    """审计登记（append-only JSONL）。"""
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError:
        pass


def run_lh(command: str) -> dict:
    """调用 lh.py 执行命令，返回 {code, stdout, stderr}。"""
    try:
        argv = [sys.executable, str(LH)] + shlex.split(command)
    except ValueError as e:
        return {"code": 2, "stdout": "", "stderr": f"命令解析失败: {e}"}
    try:
        r = subprocess.run(argv, cwd=str(ROOT), capture_output=True,
                           text=True, timeout=180)
        return {
            "code": r.returncode,
            "stdout": r.stdout,
            "stderr": r.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"code": 124, "stdout": "", "stderr": "执行超时(180s)"}
    except Exception as e:  # noqa: BLE001
        return {"code": 1, "stdout": "", "stderr": f"执行异常: {e}"}


class Handler(BaseHTTPRequestHandler):
    logger: "logging.Logger | None" = None  # main 注入

    def log_message(self, format: str, *args: Any) -> None:  # 访问日志按级别入文件（不刷终端）
        if self.logger:
            self.logger.debug("%s %s", self.address_string(), format % args)

    # ── 归一回流（v2.1 焊死）────────────────────────────────
    def _dna_line(self, node: dict | None) -> str:
        if node and isinstance(node, dict):
            return (f"{node.get('node_id', 'LH-9622-00000000')}"
                    f"|DR:{node.get('digital_root', '?')}"
                    f"|五行:{node.get('element', '?')}"
                    f"|审计:{node.get('audit', '🟡')}"
                    f"|创建:{node.get('timestamp', '?')}")
        return f"{DNA}|DR:9|五行:离|审计:🟢"

    def _json(self, obj, status=200, node: dict | None = None):
        body = json.dumps(obj, ensure_ascii=False)
        dna = self._dna_line(node)
        body += "\n# 龍魂DNA: " + dna          # ① body 末尾 DNA 指纹行
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        if node and isinstance(node, dict):   # ② 归一回流响应头（审计色转 ASCII）
            self.send_header("X-Longhun-Trace", str(node.get("node_id", "")))
            self.send_header("X-Longhun-DigitalRoot", str(node.get("digital_root", "")))
            self.send_header("X-Longhun-Audit",
                             AUDIT_HEADER.get(str(node.get("audit", "")), "UNKNOWN"))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # ── 归一审计日志（v2.1 焊死）────────────────────────────
    def _record(self, command: str, result: dict, node: dict | None,
                elapsed_ms: int) -> None:
        ip = self.client_address[0]
        is_external = ip not in ("127.0.0.1", "::1")
        if is_external:  # 外部调用 → 审计日志（只记非本机）
            summary = (result.get("stdout") or "").strip().replace("\n", " ")[:120]
            _append_jsonl(EXTERNAL_LOG, {
                "time": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "ip": ip,
                "command": command[:200],
                "code": result.get("code"),
                "summary": summary,
                "ms": elapsed_ms,
                "node_id": node.get("node_id") if node else None,
                "audit": node.get("audit") if node else None,
            })
        if node and isinstance(node, dict):   # 全部调用 → 节点注册表（供 lh trace）
            _append_jsonl(NODES_REG, {
                "node_id": node["node_id"],
                "timestamp": node.get("timestamp"),
                "digital_root": node.get("digital_root"),
                "element": node.get("element"),
                "gua": node.get("gua"),
                "audit": node.get("audit"),
                "action": node.get("action"),
                "input_summary": command[:200],
                "ip": ip,
            }, max_lines=10000)

    # ── 拓扑开放接口 v1.0（2026-09-02 · M77 零中间层）────────────
    def _topo(self, raw_path: str):
        """GET /v1/topo → 图谱索引 · /v1/topo/<名> → 节点树 JSON · /v1/topo/<名>/html → 页面"""
        try:
            import lh_topo  # noqa: I001  同目录引擎模块（懒加载·复用本地缓存/渲染·零重复实现）
        except Exception as e:  # noqa: BLE001
            self._json({"error": f"lh_topo 不可用: {e}"}, 500, node=_make_node("500"))
            return
        parts = raw_path.strip("/").split("/")   # ["v1","topo", name?, "html"?]
        name = parts[2] if len(parts) > 2 else ""
        is_html = bool(name) and len(parts) > 3 and parts[3] == "html"
        if is_html:
            name = parts[2]
        if self.logger:
            self.logger.info("GET /v1/topo%s", "/" + name + ("/html" if is_html else ""))

        if not name:   # ── 图谱索引 ──
            files = []
            for f in lh_topo.list_topos():
                with contextlib.suppress(Exception):
                    d = json.loads(f.read_text(encoding="utf-8"))
                    files.append({"topo_name": d.get("topo_name"), "display": d.get("display"),
                                  "groups": len(d.get("groups", [])),
                                  "last_sync": d.get("last_sync"),
                                  "path": f"docs/topology/{f.name}"})
            self._json({"tool": "lh-topo-api", "topos": files}, node=_make_node("TOPO-9622-LIST"))
            return

        try:
            if is_html:   # ── HTML 页（人类可读）──
                page = lh_topo.render_topo_html(name)
                body = page.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("X-Longhun-Owner", "Zhuge-Xin-UID9622")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            # ── 节点树 JSON ──
            data = lh_topo.find_topo(name)
            green, yellow, neutral = lh_topo.asset_stats(data)
            self._json({
                "tool": "lh-topo-api",
                "topo": data.get("display"),
                "owner": data.get("owner", "诸葛鑫 | UID9622 · 龍芯北辰"),
                "last_sync": data.get("last_sync"),
                "sync_from": data.get("sync_from"),
                "root_hash": lh_topo.topo_root_hash(data),
                "nodes": green + yellow + neutral,
                "green": green, "yellow": yellow, "neutral": neutral,
                "groups": data.get("groups", []),
            }, node=_make_node("TOPO-9622-GET"))
        except SystemExit as e:
            self._json({"error": str(e)}, 404, node=_make_node("TOPO-9622-404"))

    # ── 路径归一 v2.3：对外 /api/v1/* → 内部 /v1/*（兼容 nginx 剥或不剥）
    #   先 urlparse 剥 query 再 unquote——路由判定只认路径，query 由端点自取
    #   （2026-09-05 现场修复焊死：带 ?confirm 请求曾致 seg 失配 404）
    def _norm(self, raw_path: str) -> str:
        p = urllib.parse.unquote(urllib.parse.urlparse(raw_path).path).rstrip("/") or "/"
        for pre in ("/api/v1", "/api"):
            if p.startswith(pre):
                rest = p[len(pre):]
                p = rest or "/"
                break
        return p

    # 双候选匹配（兼容带 /v1 与不带）──
    def _m(self, path: str, name: str) -> bool:
        return path == name or path == "/v1" + name

    def _ms(self, path: str, name: str) -> bool:
        return (path == name or path.startswith(name + "/")
                or path == "/v1" + name or path.startswith("/v1" + name + "/"))

    def _as_v1(self, path: str) -> str:
        """统一成内部 /v1/... 规范路径（_topo 内部契约: /v1/topo/<名>[/html]）。"""
        return path if path.startswith("/v1") else "/v1" + path

    # ── 耻辱墙只读镜像（v2.2）──────────────────────────────
    def _shamewall(self):
        m = read_mirror(SHAME_MIRROR)
        if m is None:
            self._json({"tool": "lh-judge-api", "status": "empty",
                        "note": "耻辱墙镜像未同步（数据主权端 lh judge 生成后 rsync）"},
                       node=_make_node("SHAMEWALL-9622-EMPTY"))
            return
        mtime = ""
        with contextlib.suppress(OSError):
            mtime = time.strftime("%Y-%m-%dT%H:%M:%S%z",
                                  time.localtime(SHAME_MIRROR.stat().st_mtime))
        total = len(m.get("records", [])) if isinstance(m, dict) else None
        self._json({"tool": "lh-judge-api", "mirror": "shame_wall.json",
                    "mirror_synced_at": mtime, "total": total, "data": m},
                   node=_make_node("SHAMEWALL-9622-GET"))

    # ── 生态证据链只读镜像（v1.0 · LH-AUDIT-CHAIN 阶段A · 2026-09-05）────
    def _evidence(self):
        m = read_mirror(EVIDENCE_MIRROR)
        if m is None:
            self._json({"tool": "lh-evidence-api", "status": "empty",
                        "note": "证据镜像未同步（数据主权端 lh evidence add/sync 自动导出后 rsync）"},
                       node=_make_node("EVIDENCE-9622-EMPTY"))
            return
        self._json({"tool": "lh-evidence-api", "count": m.get("count", 0),
                    "root_hash": m.get("root_hash", ""),
                    "sealed_at": m.get("sealed_at", ""), "data": m},
                   node=_make_node("EVIDENCE-9622-GET"))

    # ── 铭碑验证（只读镜像存档根哈希）────────────────────────
    def _memorial(self):
        m = read_mirror(MEMORIAL_MIRROR)
        if m is None:
            self._json({"tool": "lh-memorial-api", "status": "empty",
                        "note": "铭碑镜像未同步（数据主权端 lh memorial --build 后 rsync）"},
                       node=_make_node("MEMORIAL-9622-EMPTY"))
            return
        self._json({
            "tool": "lh-memorial-api",
            "root_hash": m.get("merkle_root", ""),
            "contributor_count": m.get("contributor_count", 0),
            "total_commits": m.get("total_commits", 0),
            "generated_at": m.get("generated_at", ""),
            "verify_note": "存档根哈希只读镜像。完整重算校验在数据主权端: lh memorial --verify",
        }, node=_make_node("MEMORIAL-9622-VERIFY"))

    # ── ADS 自省挂载（v2.3 融合 · 原 :9626 只读六端点 → /v1/self/*）──────
    def _serve_self(self, path: str):
        """ADS v4.0 只读内省挂载。懒加载·网关审计头·确认码闸门语义保持。"""
        # path 入参经 _norm 已剥 query（v2.3 焊死）·seg 干净不含 ?query
        seg = path
        for pre in ("/v1/self", "/self"):
            if seg.startswith(pre):
                seg = seg[len(pre):].strip("/") or "health"
                break
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        confirm = qs.get("confirm", [""])[0]
        try:
            sys_ = _get_ads()
            fns = {
                "health": lambda c: sys_.introspect(c),
                "describe": lambda c: sys_.describe("api", c),
                "history": lambda c: sys_.historian(c),
                "diagnose": lambda c: sys_.diagnose(c),
                "boundary": lambda c: sys_.boundary(c),
                "roles": lambda c: {r: fn(c) for r, fn in
                                    [("introspect", sys_.introspect),
                                     ("historian", sys_.historian),
                                     ("diagnose", sys_.diagnose),
                                     ("boundary", sys_.boundary)]},
            }
            fn = fns.get(seg)
            if fn is None:
                self._json({"error": "not found"}, 404, node=_make_node("404"))
                return
            result = fn(confirm)
            status = 403 if isinstance(result, dict) and result.get("code") == 403 else 200
            self._json(result, status=status, node=_make_node(f"SELF-9622-{seg.upper()}"))
        except Exception as e:  # noqa: BLE001
            if self.logger:
                self.logger.error("self/%s %s", seg, e)
            self._json({"error": str(e), "status": "🔴"}, 500,
                       node=_make_node("SELF-9622-ERR"))

    # ── Registry 注册中心挂载（v4.4 融合 · 原 :9623 → /v1/reg/*）──────
    def _reg_cst(self, reg) -> str:
        try:
            from datetime import datetime  # noqa: PLC0415
            return datetime.now(reg.CST).isoformat()
        except Exception:  # noqa: BLE001
            return ""

    def _reg_split(self, path: str) -> str:
        seg = path
        for pre in ("/v1/reg", "/reg"):
            if seg.startswith(pre):
                seg = seg[len(pre):].strip("/")
                break
        return seg

    def _reg_online(self, reg) -> dict:
        now = time.time()
        return {k: v for k, v in reg.nodes.items()
                if now - v.get("timestamp", 0) < reg.NODE_TIMEOUT_SECONDS}

    def _reg_node_view(self, reg, nid: str) -> dict:
        n = reg.nodes.get(nid, {})
        online = nid in self._reg_online(reg)
        return {
            "last_seen": n.get("timestamp_iso", ""),
            "metrics": n.get("metrics", {}),
            "signature_valid": n.get("signature_valid", False),
            "status": "online" if online else "offline",
        }

    def _serve_reg(self, path: str):
        """GET 只读面：health/nodes/stats/audit/node/<id>（数据=registry 模块内存态）。"""
        try:
            reg = _get_reg()
        except Exception as e:  # noqa: BLE001
            self._json({"error": f"registry 不可用: {e}"}, 500,
                       node=_make_node("REG-9622-ERR"))
            return
        seg = self._reg_split(path)
        cst = self._reg_cst(reg)
        online = self._reg_online(reg)
        offline = {k: v for k, v in reg.nodes.items() if k not in online}
        if not seg or seg == "health":
            self._json({"status": "ok",
                        "registry": "longhun-registry-v2.0 (embedded @lh-api)",
                        "dna": reg.DNA_ANCHOR[:40] + "...",
                        "uptime_seconds": int(time.time() - reg.START_TIME),
                        "cst_time": cst}, node=_make_node("REG-9622-HEALTH"))
        elif seg == "nodes":
            self._json({"total_nodes": len(reg.nodes), "online": len(online),
                        "offline": len(offline),
                        "nodes": {nid: self._reg_node_view(reg, nid)
                                  for nid in reg.nodes}},
                       node=_make_node("REG-9622-NODES"))
        elif seg == "stats":
            total_storage = sum(n.get("metrics", {}).get("storage_used_gb", 0)
                                for n in reg.nodes.values())
            total_requests = sum(n.get("metrics", {}).get("requests_handled", 0)
                                 for n in reg.nodes.values())
            total_crawls = sum(n.get("metrics", {}).get("crawl_sessions", 0)
                               for n in reg.nodes.values())
            self._json({"total_nodes": len(reg.nodes), "online_nodes": len(online),
                        "total_storage_gb": round(total_storage, 2),
                        "total_requests": total_requests,
                        "total_crawl_sessions": total_crawls,
                        "dna": reg.DNA_ANCHOR[:40] + "...",
                        "cst_time": cst}, node=_make_node("REG-9622-STATS"))
        elif seg == "audit":
            self._json({"total_audited": len(reg.node_audit_results),
                        "results": reg.node_audit_results},
                       node=_make_node("REG-9622-AUDIT"))
        elif seg.startswith("node/"):
            nid = seg.split("node/")[-1]
            if nid in reg.nodes:
                self._json({"node_id": nid, "latest": reg.nodes[nid],
                            "history_count": len(reg.node_history.get(nid, [])),
                            "recent_history": reg.node_history.get(nid, [])[-5:]},
                           node=_make_node("REG-9622-NODE"))
            else:
                self._json({"error": "node not found"}, 404,
                           node=_make_node("REG-9622-404"))
        else:
            self._json({"error": "not found"}, 404, node=_make_node("REG-9622-404"))

    def do_GET(self):
        path = self._norm(self.path)
        if self.logger:
            self.logger.info("GET %s", path)
        if self._m(path, "/health"):
            node = _make_node("GATEWAY-9622-HEALTH")
            self._json({"status": "ok", "version": f"v{VERSION}",
                        "uptime": _uptime(), "service": "lh-api",
                        "open": "https://uid9622.cn/api/v1",
                        "api_keys": len(load_api_keys().get("keys", {})),
                        "dna": DNA}, node=node)
        elif self._ms(path, "/topo"):
            self._topo(self._as_v1(path))
        elif self._m(path, "/judge/shamewall"):
            self._shamewall()
        elif self._m(path, "/memorial/verify"):
            self._memorial()
        elif self._m(path, "/evidence"):
            self._evidence()
        elif path.startswith("/v1/self") or path.startswith("/self"):
            self._serve_self(path)
        elif path.startswith("/v1/reg") or path.startswith("/reg"):
            self._serve_reg(path)
        else:
            if self.logger:
                self.logger.warning("GET %s 404", self.path)
            self._json({"error": "not found"}, 404, node=_make_node("404"))

    # ── 认证守卫 v2.2：POST 写端点强制 X-API-Key + 角色 ─────────
    def _require(self, min_role: str):
        """返回 auth dict 或直接 401/403 响应。"""
        auth = check_api_key(self.headers.get("X-API-Key", ""))
        if not auth:
            self._json({"error": "unauthorized · 缺少或无效 X-API-Key"}, 401,
                       node=_make_node("401"))
            return None
        if ROLE_LEVEL.get(auth["role"], 0) < ROLE_LEVEL[min_role]:
            self._json({"error": f"forbidden · 角色 {auth['role']}（{ROLE_CN.get(auth['role'], '')}）需 {min_role}+"},
                       403, node=_make_node("403"))
            return None
        return auth

    def _read_json_body(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length", 0))
            return json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        except Exception:  # noqa: BLE001
            return {}

    def do_POST(self):
        path = self._norm(self.path)
        if self.logger:
            self.logger.info("POST %s", path)

        if self._m(path, "/lh"):
            payload = self._read_json_body()
            command = str(payload.get("command", "")).strip()
            if not command:
                self._json({"error": "缺少 command"}, 400, node=_make_node("400"))
                return
            t0 = time.time()
            result = run_lh(command)
            elapsed_ms = int((time.time() - t0) * 1000)
            if self.logger and result["code"] != 0:
                self.logger.warning("cmd 失败 code=%s", result["code"])
            node = _extract_node(result["stdout"], command)
            self._record(command, result, node, elapsed_ms)
            self._json({"command": command, "result": result}, node=node)
            return

        if self._m(path, "/judge/scan"):
            auth = self._require("auditor")
            if not auth:
                return
            body = self._read_json_body()
            ts = time.strftime("%Y-%m-%dT%H:%M:%S%z")
            append_reg(SCAN_REQ_LOG, {"ts": ts, "actor": auth["name"],
                                      "role": auth["role"],
                                      "scope": str(body.get("scope", "default"))[:80],
                                      "ip": self.client_address[0]})
            self._json({"status": "accepted", "registered_at": ts,
                        "actor": auth["name"], "role": auth["role"],
                        "note": "扫描触发已登记。完整归一扫描在数据主权端执行: lh judge scan"},
                       status=202, node=_make_node("SCAN-9622-ACCEPT"))
            return

        if self._m(path, "/dh/dispatch"):
            auth = self._require("admin")
            if not auth:
                return
            body = self._read_json_body()
            persona = str(body.get("persona", ""))[:40]
            task = str(body.get("task", ""))[:120]
            if not persona or not task:
                self._json({"error": "需 persona + task"}, 400, node=_make_node("400"))
                return
            ts = time.strftime("%Y-%m-%dT%H:%M:%S%z")
            append_reg(DH_REQ_LOG, {"ts": ts, "actor": auth["name"],
                                    "role": auth["role"], "persona": persona,
                                    "task": task, "ip": self.client_address[0]})
            self._json({"status": "accepted", "registered_at": ts,
                        "actor": auth["name"], "persona": persona,
                        "note": "数字人调度请求已登记。实际调度在数据主权端执行: lh dh dispatch"},
                       status=202, node=_make_node("DH-9622-ACCEPT"))
            return

        if path.startswith("/v1/reg") or path.startswith("/reg"):
            self._serve_reg_post(path)
            return

        if self.logger:
            self.logger.warning("POST %s 404", self.path)
        self._json({"error": "not found"}, 404, node=_make_node("404"))

    # ── Registry 注册中心 POST 写面（v4.4 · heartbeat/audit-report 通道保留）─
    def _serve_reg_post(self, path: str):
        try:
            reg = _get_reg()
        except Exception as e:  # noqa: BLE001
            self._json({"error": f"registry 不可用: {e}"}, 500,
                       node=_make_node("REG-9622-ERR"))
            return
        seg = self._reg_split(path)
        body = self._read_json_body()
        if seg == "heartbeat":
            try:
                node_id = str(body.get("node_id", "unknown"))[:80]
                sig = str(body.pop("signature", ""))[:64]
                payload = {k: v for k, v in body.items() if k != "signature"}
                expected = hashlib.sha256(
                    (json.dumps(payload, sort_keys=True, ensure_ascii=False)
                     + reg.DNA_ANCHOR + reg.CONFIRM).encode()).hexdigest()[:32]
                payload["signature_valid"] = (sig == expected)
                from datetime import datetime  # noqa: PLC0415
                payload["received_at"] = datetime.now(reg.CST).isoformat()
                reg.nodes[node_id] = payload
                reg.node_history[node_id].append(
                    {"timestamp": payload.get("timestamp", 0),
                     "timestamp_iso": payload.get("received_at", ""),
                     "metrics": payload.get("metrics", {})})
                if len(reg.node_history[node_id]) > 100:
                    reg.node_history[node_id] = reg.node_history[node_id][-100:]
                online = self._reg_online(reg)
                self._json({"status": "received", "node_id": node_id,
                            "nodes_online": len(online),
                            "total_nodes": len(reg.nodes)},
                           node=_make_node("REG-9622-HB"))
            except Exception as e:  # noqa: BLE001
                self._json({"error": str(e)[:80]}, 500,
                           node=_make_node("REG-9622-ERR"))
        elif seg == "audit/report":
            try:
                nid = str(body.get("node_id", "unknown"))[:80]
                summary = body.get("summary", {})
                reg.node_audit_results[nid] = {
                    "score": summary.get("score", 0),
                    "passed": summary.get("passed", 0),
                    "failed": summary.get("failed", 0),
                    "audited_at": str(body.get("audited_at", ""))[:40]}
                self._json({"status": "received", "node_id": nid},
                           node=_make_node("REG-9622-AUDIT-RPT"))
            except Exception as e:  # noqa: BLE001
                self._json({"error": str(e)[:80]}, 400,
                           node=_make_node("REG-9622-ERR"))
        else:
            self._json({"error": "not found"}, 404, node=_make_node("REG-9622-404"))


def daemonize() -> None:
    """双 fork 后台化（零依赖）。日志由 logging handler 负责，stdout/stderr 弃用。"""
    if os.fork() > 0:
        os._exit(0)
    os.setsid()
    if os.fork() > 0:
        os._exit(0)
    devnull = os.open(os.devnull, os.O_RDWR)
    os.dup2(devnull, sys.stdout.fileno())
    os.dup2(devnull, sys.stderr.fileno())


def main() -> None:
    global DATA_DIR, SHAME_MIRROR, MEMORIAL_MIRROR, SCAN_REQ_LOG, DH_REQ_LOG
    ap = argparse.ArgumentParser(
        description="🐉 龍魂 CIL API 网关 v2.2 开放平台 (默认只监听 127.0.0.1)")
    ap.add_argument("--port", type=int, default=9622, help="监听端口 (默认 9622)")
    ap.add_argument("--host", default=HOST,
                    help="监听地址 (默认 127.0.0.1·安全；对外开放显式用 0.0.0.0 且自动开启归一审计)")
    ap.add_argument("--daemon", action="store_true", help="后台运行")
    ap.add_argument("--log-level", choices=LOG_LEVELS, default="info",
                    help=f"日志级别 (默认 info，可选 {','.join(LOG_LEVELS)})")
    ap.add_argument("--pidfile", default=str(PID_FILE),
                    help=f"PID 文件 (默认 {PID_FILE})")
    ap.add_argument("--data-dir", default="",
                    help="数据镜像目录 (默认 {DATA_DIR}·鲲鹏 /apps/lh-api/data)")
    ap.add_argument("--keygen", action="store_true", help="生成 API Key (UID9622 本机)"
                                                            "· 配合 --role/--name")
    ap.add_argument("--role", choices=tuple(ROLE_LEVEL), default="viewer",
                    help="keygen 角色: viewer|auditor|admin")
    ap.add_argument("--name", default="", help="keygen 持钥人标识")
    ap.add_argument("--keynote", default="", help="keygen 备注")
    args = ap.parse_args()

    if args.data_dir:
        DATA_DIR = Path(args.data_dir).expanduser().resolve()
        SHAME_MIRROR = DATA_DIR / "shame_wall.json"
        MEMORIAL_MIRROR = DATA_DIR / "contributor_memorial.json"
        SCAN_REQ_LOG = DATA_DIR / "scan_requests.log"
        DH_REQ_LOG = DATA_DIR / "dh_dispatch.log"
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    if args.keygen:
        key = gen_api_key(args.role, args.name or "UID9622 签发",
                          args.keynote or "lh api keygen")
        print(f"🟢 已生成 {args.role} 级 API Key:")
        print(f"  X-API-Key: {key}")
        print(f"  持钥人: {args.name or 'UID9622 签发'} · 登记 {API_KEYS_FILE}")
        print("  ⚠️ 该 Key 仅显示一次 · 妥善保管 · 外发需最小权限")
        return

    logger = setup_logging(args.log_level)
    Handler.logger = logger
    pidfile = Path(args.pidfile).expanduser()

    if args.daemon:
        daemonize()
    write_pidfile(pidfile)

    if args.host not in ("127.0.0.1", "::1"):
        logger.warning("⚠️ 网关绑定 %s 对外开放——外部调用自动写入 %s (归一审计)",
                       args.host, EXTERNAL_LOG)

    server = ThreadingHTTPServer(server_address=(args.host, args.port),
                                 RequestHandlerClass=Handler)
    logger.info("🐉 lh-api v%s 已启动 http://%s:%s/v1/lh (log=%s pid=%s 归一审计=%s)",
                VERSION, args.host, args.port, LOG_FILE, pidfile,
                "外部" if args.host not in ("127.0.0.1", "::1") else "本机")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        remove_pidfile(pidfile)
        logger.info("lh-api v%s 已退出", VERSION)


if __name__ == "__main__":
    main()
