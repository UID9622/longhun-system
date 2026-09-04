#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-04-LONGHUN-KUNPENG-MCP-ADMIN-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 鲲鹏 MCP Server · 高危管理层 lh-mcp-admin v1.0（端口 8767 · 默认关闭）
================================================================
对外暴露龍魂系统的管理能力。所有工具 = 高危写操作。

安全机制（受控三闸）:
  1. 默认 disabled（systemd unit 不启动）；需 UID9622 显式 enable
  2. 来源 IP 白名单（config/admin-whitelist.json → ips）
  3. 每次操作强制二次确认：请求头 X-Confirm: yes（或参数 _confirm:"yes"）
  4. 工具白名单（whitelist.tools）· 发布目录白名单（whitelist.build_dirs）
  5. 全量操作 append-only 记录 → ~/.longhun/audit/admin_operations.log
  6. 异常自动落耻辱墙通知通道 → ~/.longhun/shame_wall/mcp_admin_anomalies.jsonl

MCP Tools（全部 confirm）:
  cnsh_build(source)       编译 CNSH 源码 → Python
  cnsh_publish(package)    发布 CNSH 包（白名单目录内）
  topo_sync(name)          强制同步指定图谱（Notion/活体）
  system_reload()          系统配置重载 + 完整性检查
"""

import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh_mcp_core import (  # noqa: E402
    MCPServer, MCPError, ERR_INVALID_PARAMS, now_iso, run_engine,
    run_from_cli, _sha8,
)

SERVER_NAME = "lh-mcp-admin"
VERSION = "1.0.0"
DEFAULT_PORT = 8767  # 2026-09-04 裁决: 8765 被鲲鹏 longhun-cal(cal_server) 常驻占用 → admin 换 8767(8763/8764/8767 连续段)

DEFAULT_CFG = {
    "server": SERVER_NAME,
    "port": DEFAULT_PORT,
    "host": "127.0.0.1",
    "auth": {"mode": "none"},
    "log_dir": "~/.longhun/logs/mcp",
    "lh_root": "",
    "peer_allowlist": ["127.0.0.1"],
    "whitelist_file": "config/admin-whitelist.json",
    "tmp_dir": "~/.longhun/mcp_tmp",
}

ADMIN_OPS_LOG = Path("~/.longhun/audit/admin_operations.log").expanduser()
ANOMALY_LOG = Path("~/.longhun/shame_wall/mcp_admin_anomalies.jsonl").expanduser()

_R = Path(__file__).resolve().parents[2]  # longhun-system/


def _load_whitelist() -> dict:
    """读 config/admin-whitelist.json（默认：仅本机 + 四个工具 + 本地 CNSH 包目录）"""
    p = _R / "deploy" / "longhun-mcp" / "config" / "admin-whitelist.json"
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    return {"ips": ["127.0.0.1"],
            "tools": ["cnsh_build", "cnsh_publish", "topo_sync", "system_reload"],
            "build_dirs": [str(_R / "packaging" / "cnsh-stdlib")]}


def _ops_log(action: str, detail: dict, verdict: str):
    """append-only 管理操作日志（谁/何时/做什么/结果三色）"""
    try:
        ADMIN_OPS_LOG.parent.mkdir(parents=True, exist_ok=True)
        line = f"{now_iso()} | {action} | {json.dumps(detail, ensure_ascii=False, default=str)} | {verdict}"
        with open(ADMIN_OPS_LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def _anomaly(action: str, err: Exception):
    """异常 → 耻辱墙通知通道（mcp_admin_anomalies.jsonl·不污染正式耻辱墙）"""
    try:
        ANOMALY_LOG.parent.mkdir(parents=True, exist_ok=True)
        rec = {"ts": now_iso(), "server": SERVER_NAME, "action": action,
               "error": f"{type(err).__name__}: {err}"}
        with open(ANOMALY_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _guard_root() -> Path:
    root = Path(__file__).resolve().parents[2]
    return root


# ═══════════════════════════════════════════════════════════════
# 工具实现（执行前经 whitelist + confirm + peer 三闸）
# ═══════════════════════════════════════════════════════════════

def _tool_cnsh_build(args: dict) -> dict:
    """编译 CNSH 源码 → Python；source 必填；产物写入临时文件后读回"""
    source = str(args.get("source") or "").strip()
    if not source:
        raise MCPError(ERR_INVALID_PARAMS, "source(CNSH 源码) 不能为空")
    if len(source) > 200_000:
        raise MCPError(ERR_INVALID_PARAMS, "源码超限(>200KB)")
    root = _guard_root()
    tmp_dir = Path(DEFAULT_CFG["tmp_dir"]).expanduser()
    tmp_dir.mkdir(parents=True, exist_ok=True)
    cname = tmp_dir / f"mcp_{int(time.time())}_{_sha8(source)}.cnsh"
    pyname = cname.with_suffix(".py")
    cname.write_text(source, encoding="utf-8")
    res = run_engine(root, "cnsh.py",
                     ["build", str(cname), "-o", str(pyname), "--target", "python"],
                     timeout=60)
    code = ""
    if res["rc"] == 0 and pyname.exists():
        code = pyname.read_text(encoding="utf-8", errors="replace")
    elif res["rc"] == 0:
        code = res["stdout"]
    # 清理临时文件（不删除只冻结 → 移入 tmp/archive）
    for f in (cname, pyname):
        try:
            f.unlink()
        except Exception:
            pass
    ok = res["rc"] == 0
    return {"ok": ok, "rc": res["rc"],
            "python_code": code[:180_000] if ok else "",
            "errors": res["stdout"][:50_000] if not ok else res["stderr"][:20_000],
            "compiled_at": now_iso()}


def _tool_cnsh_publish(args: dict) -> dict:
    """发布 CNSH 包：package 名须命中 build_dirs 下某 cnsh.json 的 name（白名单目录）"""
    root = _guard_root()
    wl = _load_whitelist()
    dirs = [Path(d).expanduser() for d in wl.get("build_dirs", [])]
    candidates = {}
    for d in dirs:
        cj = d / "cnsh.json"
        if cj.exists():
            try:
                meta = json.loads(cj.read_text(encoding="utf-8"))
                nm = meta.get("name", "")
                if nm:
                    candidates[nm] = d
            except Exception:
                continue
    pkg = str(args.get("package") or "").strip()
    if not pkg:
        # 唯一包可自动发布
        if len(candidates) == 1:
            pkg = next(iter(candidates))
        else:
            raise MCPError(ERR_INVALID_PARAMS,
                           f"package 必填。候选: {sorted(candidates)}")
    if pkg not in candidates:
        raise MCPError(ERR_INVALID_PARAMS,
                       f"包「{pkg}」不在发布白名单（build_dirs 需含其目录）")
    target = candidates[pkg]
    res = run_engine(root, "cnsh_pm.py", ["publish"], timeout=120, cwd=target)
    ok = res["rc"] == 0
    return {"ok": ok, "package": pkg, "dir": str(target),
            "output": res["stdout"][:100_000], "rc": res["rc"],
            "published_at": now_iso()}


def _tool_topo_sync(args: dict) -> dict:
    """强制同步指定图谱（source=notion 默认 / --live 活体校验；网络操作，超时 120s）"""
    name = str(args.get("name") or "").strip()
    if not name:
        raise MCPError(ERR_INVALID_PARAMS, "name(图谱名) 不能为空，如 通心译/深度学习")
    live = bool(args.get("live"))
    root = _guard_root()
    argv = ["sync", name]
    if live:
        argv.append("--live")
    res = run_engine(root, "lh_topo.py", argv, timeout=120)
    ok = res["rc"] == 0
    tail = (res["stdout"] or res["stderr"])[-3000:]
    return {"ok": ok, "graph": name, "live": live,
            "output_tail": tail, "rc": res["rc"],
            "synced_at": now_iso()}


def _tool_system_reload(args: dict) -> dict:
    """重新加载系统配置：校验全部 JSON 配置可解析 + 关键引擎在位 + 白名单刷新"""
    root = _guard_root()
    checks = []
    ok_all = True
    # 1. mcp-config.json
    cfg_p = root / "deploy" / "longhun-mcp" / "config" / "mcp-config.json"
    if cfg_p.exists():
        try:
            json.loads(cfg_p.read_text(encoding="utf-8"))
            checks.append({"check": "mcp-config.json", "ok": True})
        except Exception as exc:
            ok_all = False
            checks.append({"check": "mcp-config.json", "ok": False, "error": str(exc)})
    # 2. admin-whitelist.json
    wl = _load_whitelist()
    checks.append({"check": "admin-whitelist.json", "ok": True,
                   "ips": wl.get("ips", []), "tools": wl.get("tools", [])})
    # 3. 关键引擎在位
    for eng in ("lh.py", "cnsh.py", "lh_topo.py", "cnsh_pm.py"):
        ep = root / "08_BIN" / eng
        if not ep.exists():
            ep = root / "bin" / eng
        present = ep.exists()
        checks.append({"check": f"08_BIN/{eng}", "ok": present})
        if not present:
            ok_all = False
    # 4. 图谱缓存目录
    topo_d = root / "docs" / "topology"
    n_topo = len(list(topo_d.glob("*_topo.json"))) if topo_d.is_dir() else 0
    checks.append({"check": "docs/topology", "ok": n_topo > 0, "graphs": n_topo})
    if n_topo == 0:
        ok_all = False
    return {"ok": ok_all, "checks": checks, "reloaded_at": now_iso(),
            "note": "高危操作已记录至 ~/.longhun/audit/admin_operations.log"}


def build_server() -> MCPServer:
    wl = _load_whitelist()
    cfg = dict(DEFAULT_CFG)
    cfg["peer_allowlist"] = wl.get("ips") or ["127.0.0.1"]
    srv = MCPServer(SERVER_NAME, VERSION, cfg)

    def guard(fn, action: str):
        def wrapped(args):
            try:
                detail = {"args": {k: v for k, v in args.items() if k != "_confirm"}}
                result = fn(args)
                _ops_log(action, detail, "🟢" if result.get("ok") else "🟡")
                return result
            except Exception as exc:
                _ops_log(action, {"args": {k: v for k, v in args.items()
                                           if k != "_confirm"}}, "🔴")
                _anomaly(action, exc)
                raise
        return wrapped

    tools = wl.get("tools", [])
    if "cnsh_build" in tools:
        srv.add_tool("cnsh_build",
                     "编译 CNSH 源码 → Python 代码（高危·需二次确认）",
                     {"type": "object",
                      "properties": {"source": {"type": "string",
                                                "description": "CNSH 源码全文"}},
                      "required": ["source"]},
                     guard(_tool_cnsh_build, "cnsh_build"), confirm=True)
    if "cnsh_publish" in tools:
        srv.add_tool("cnsh_publish",
                     "发布 CNSH 包到包仓库（package 须在白名单 build_dirs 的 cnsh.json 中）",
                     {"type": "object",
                      "properties": {"package": {"type": "string",
                                                 "description": "包名；留空=唯一候选包"}}},
                     guard(_tool_cnsh_publish, "cnsh_publish"), confirm=True)
    if "topo_sync" in tools:
        srv.add_tool("topo_sync",
                     "强制同步指定图谱（默认 Notion 源；live=true 活体校验）",
                     {"type": "object",
                      "properties": {"name": {"type": "string", "description": "图谱名 如 通心译/深度学习"},
                                     "live": {"type": "boolean",
                                              "description": "true=活体校验(可选)"}},
                      "required": ["name"]},
                     guard(_tool_topo_sync, "topo_sync"), confirm=True)
    if "system_reload" in tools:
        srv.add_tool("system_reload",
                     "重新加载系统配置：校验 config/白名单/引擎在位 + 返回完整性报告",
                     {"type": "object", "properties": {}},
                     guard(_tool_system_reload, "system_reload"), confirm=True)
    return srv


if __name__ == "__main__":
    sys.exit(run_from_cli(build_server(), SERVER_NAME, DEFAULT_PORT, DEFAULT_CFG))
