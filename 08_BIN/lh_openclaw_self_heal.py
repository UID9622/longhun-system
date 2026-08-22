#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-OPENCLAW-SELF-HEAL-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# CREATOR: 诸葛鑫 (UID9622)
# -*- coding: utf-8 -*-
"""
🐉 OpenClaw 自动自愈引擎 v1.0
================================
自动发现 → 自动修复 → 异常推送（Bark）
针对 Mac 本地 OpenClaw 节点的常见小尾巴：

  [1] gateway.mode 未设置 → 网关启动被阻止
  [2] command owner 未配置 → exec 审批链路不完整
  [3] ~/.openclaw 权限过宽 → 安全风险
  [4] 会话存储目录缺失 → CRITICAL
  [5] SSH 隧道进程异常 → 节点连接 1006
  [6] openclaw 不在 PATH → 命令找不到

用法:
  python3 bin/lh_openclaw_self_heal.py --check     # 只检查
  python3 bin/lh_openclaw_self_heal.py --fix       # 自动修复可修项
  python3 bin/lh_openclaw_self_heal.py --cron      # 静默模式(供launchd)
  python3 bin/lh_openclaw_self_heal.py --push      # 异常时Bark推送

DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-OPENCLAW-SELF-HEAL-v1.0
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional

HOME = Path.home()
OPENCLAW_DIR = HOME / ".openclaw"
SESSIONS_DIR = OPENCLAW_DIR / "agents" / "main" / "sessions"
OPENCLAW_BIN = OPENCLAW_DIR / "bin"
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"

# 隧道端口（鲲鹏网关转发）
TUNNEL_PORTS = ["18789", "18790"]


@dataclass
class Issue:
    category: str
    severity: str  # info / warning / error / critical
    message: str
    auto_fix: bool = False
    fix_cmd: Optional[List[str]] = None
    detail: str = ""


class OpenClawSelfHeal:
    """OpenClaw 节点自愈引擎"""

    DNA = "#龍芯⚡️丙午·丙申·戊申·亥时·䷗复-OPENCLAW-SELF-HEAL-v1.0"

    def __init__(self):
        self.issues: List[Issue] = []
        self.fixed: List[Issue] = []
        self.failed: List[Issue] = []
        self.repaired = 0
        self.repair_failed = 0

    # ───────────────────────── 自动发现 ─────────────────────────

    def discover(self):
        self.issues = []
        self.check_path()
        self.check_permissions()
        self.check_sessions_dir()
        self.check_gateway_mode()
        self.check_service()
        self.check_auth_token()
        self.check_owner()
        self.check_tunnel()
        self.check_nodes()
        return self.issues

    def check_path(self):
        """openclaw 是否在 PATH"""
        which = shutil.which("openclaw")
        if which:
            return
        if (OPENCLAW_BIN / "openclaw").exists():
            self.issues.append(Issue(
                category="PATH",
                severity="warning",
                message=f"openclaw 未加入 PATH（二进制在 {OPENCLAW_BIN}）",
                auto_fix=True,
                fix_cmd=["bash", "-c",
                         "echo 'export PATH=\"$HOME/.openclaw/bin:$PATH\"' >> ~/.zshrc "
                         "&& echo 'export PATH=\"$HOME/.openclaw/bin:$PATH\"' >> ~/.bash_profile"],
                detail="建议: export PATH=\"$HOME/.openclaw/bin:$PATH\"",
            ))
        else:
            self.issues.append(Issue(
                category="PATH",
                severity="error",
                message="openclaw 二进制不存在，无法定位安装",
                auto_fix=False,
            ))

    def check_permissions(self):
        """~/.openclaw 权限应为 700"""
        if not OPENCLAW_DIR.exists():
            self.issues.append(Issue(
                category="权限",
                severity="warning",
                message="~/.openclaw 目录不存在",
                auto_fix=True,
                fix_cmd=["bash", "-c", f"mkdir -p {OPENCLAW_DIR} && chmod 700 {OPENCLAW_DIR}"],
            ))
            return
        mode = OPENCLAW_DIR.stat().st_mode & 0o777
        if mode & 0o077:
            self.issues.append(Issue(
                category="权限",
                severity="warning",
                message=f"~/.openclaw 权限过宽 ({oct(mode)})，应为 700",
                auto_fix=True,
                fix_cmd=["bash", "-c", f"chmod 700 {OPENCLAW_DIR}"],
            ))

    def check_sessions_dir(self):
        """会话存储目录缺失 = CRITICAL"""
        if not SESSIONS_DIR.exists():
            self.issues.append(Issue(
                category="会话目录",
                severity="critical",
                message=f"会话存储目录缺失: {SESSIONS_DIR}",
                auto_fix=True,
                fix_cmd=["bash", "-c", f"mkdir -p {SESSIONS_DIR}"],
            ))

    def _read_config(self) -> dict:
        """读取 openclaw.json（不存在返回空 dict）"""
        cfg = OPENCLAW_DIR / "openclaw.json"
        if not cfg.exists():
            return {}
        try:
            return json.loads(cfg.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def check_gateway_mode(self):
        """gateway.mode 是否设置 + 端口是否在监听"""
        cfg = self._read_config()
        gw = cfg.get("gateway", {})
        mode = gw.get("mode", "")
        port = gw.get("port", 18789)
        if not mode:
            self.issues.append(Issue(
                category="网关模式",
                severity="error",
                message="gateway.mode 未设置，网关启动会被阻止",
                auto_fix=True,
                fix_cmd=["openclaw", "config", "set", "gateway.mode", "local"],
                detail="Fix: openclaw config set gateway.mode local",
            ))
        # 端口监听检查
        listening = self._port_listening(port)
        if not listening:
            self.issues.append(Issue(
                category="网关端口",
                severity="error",
                message=f"网关端口 {port} 未监听",
                auto_fix=True,
                fix_cmd=["openclaw", "daemon", "start"],
                detail=f"Fix: openclaw daemon start (target ws://127.0.0.1:{port})",
            ))

    def check_service(self):
        """网关 LaunchAgent 服务是否安装且运行"""
        try:
            r = self._run(["bash", "-c", "launchctl list | grep ai.openclaw.gateway"], timeout=10)
            if not (r or "").strip():
                self.issues.append(Issue(
                    category="网关服务",
                    severity="error",
                    message="LaunchAgent ai.openclaw.gateway 未安装/未加载",
                    auto_fix=True,
                    fix_cmd=["openclaw", "daemon", "install"],
                    detail="Fix: openclaw daemon install",
                ))
        except Exception:
            pass

    def check_auth_token(self):
        """gateway.auth.token 与 remote.token 是否匹配 + 环境变量"""
        cfg = self._read_config()
        gw = cfg.get("gateway", {})
        auth_token = (gw.get("auth", {}) or {}).get("token", "")
        remote = gw.get("remote", {}) or {}
        remote_token = remote.get("token", "")
        env_token = os.environ.get("OPENCLAW_GATEWAY_TOKEN", "")
        auth_mode = (gw.get("auth", {}) or {}).get("mode", "")

        # 鉴权模式 token 但未配 token
        if auth_mode == "token" and not auth_token:
            self.issues.append(Issue(
                category="网关鉴权",
                severity="error",
                message="gateway.auth.mode=token 但未配置 auth.token",
                auto_fix=False,
                detail="Fix: openclaw config set gateway.auth.token '<secret>'",
            ))
        # 配置了 auth.token 但 remote.token 不匹配
        if auth_token and remote_token and auth_token != remote_token:
            self.issues.append(Issue(
                category="网关鉴权",
                severity="error",
                message="gateway.remote.token 与 gateway.auth.token 不匹配",
                auto_fix=True,
                fix_cmd=["bash", "-c",
                         f"openclaw config set gateway.remote.token '{auth_token}'"],
                detail="Fix: openclaw config set gateway.remote.token '<same as auth.token>'",
            ))
        # token 模式但 shell 环境变量缺失 → CLI 无法连接
        if auth_mode == "token" and auth_token and not env_token:
            self.issues.append(Issue(
                category="网关鉴权",
                severity="warning",
                message="OPENCLAW_GATEWAY_TOKEN 未写入 shell 配置，CLI 连接会鉴权失败",
                auto_fix=True,
                fix_cmd=["bash", "-c",
                         f"echo 'export OPENCLAW_GATEWAY_TOKEN=\"{auth_token}\"' >> ~/.zshrc "
                         f"&& echo 'export OPENCLAW_GATEWAY_TOKEN=\"{auth_token}\"' >> ~/.bash_profile"],
                detail="将 token 固化到 ~/.zshrc + ~/.bash_profile",
            ))

    def check_owner(self):
        """command owner 是否配置"""
        try:
            r = self._run(["openclaw", "config", "get", "commands.ownerAllowFrom"], timeout=15)
            val = (r or "").strip()
            if not val or "unset" in val.lower() or "not set" in val.lower() or val == "[]":
                self.issues.append(Issue(
                    category="命令所有者",
                    severity="warning",
                    message="未配置 command owner，exec 审批链路不完整",
                    auto_fix=False,
                    detail="Fix: openclaw config set commands.ownerAllowFrom '[your-user-id]'",
                ))
        except Exception as e:
            self.issues.append(Issue("命令所有者", "warning", f"无法读取 ownerAllowFrom: {e}"))

    def _port_listening(self, port: int) -> bool:
        try:
            r = self._run(["bash", "-c", f"lsof -iTCP:{port} -sTCP:LISTEN"], timeout=10)
            return bool((r or "").strip())
        except Exception:
            return False

    def check_tunnel(self):
        """网关可达性：local 模式直接探测端口，remote 模式才查 SSH 隧道"""
        cfg = self._read_config()
        mode = cfg.get("gateway", {}).get("mode", "local")
        if mode == "remote":
            try:
                r = self._run(["bash", "-c", "ps aux | grep -E 'ssh.*1879[09]' | grep -v grep"], timeout=10)
                if not (r or "").strip():
                    self.issues.append(Issue(
                        category="隧道",
                        severity="warning",
                        message="remote 模式但 SSH 隧道进程不存在（18789/18790）",
                        auto_fix=False,
                        detail="需手动确认网关端口与转发命令，避免盲修",
                    ))
            except Exception:
                pass

    def check_nodes(self):
        """节点连接状态"""
        try:
            r = self._run(["openclaw", "nodes", "list"], timeout=20)
            if r and ("1006" in r or "abnormal" in r.lower() or "disconnected" in r.lower()):
                self.issues.append(Issue(
                    category="节点连接",
                    severity="error",
                    message="节点→网关连接异常（websocket 1006）",
                    auto_fix=False,
                    detail=r.strip()[:200],
                ))
        except Exception as e:
            self.issues.append(Issue("节点连接", "warning", f"无法检查节点: {e}"))

    # ───────────────────────── 自动修复 ─────────────────────────

    def repair(self):
        for issue in self.issues:
            if not issue.auto_fix or not issue.fix_cmd:
                continue
            print(f"  🔧 修复: [{issue.category}] {issue.message}")
            try:
                r = self._run(issue.fix_cmd, timeout=30)
                # 修复后验证
                ok = self._verify(issue)
                if ok:
                    self.repaired += 1
                    self.fixed.append(issue)
                    print(f"     ✅ 已修复")
                else:
                    self.repair_failed += 1
                    self.failed.append(issue)
                    print(f"     ❌ 修复后验证未通过")
            except Exception as e:
                self.repair_failed += 1
                self.failed.append(issue)
                print(f"     ❌ 修复失败: {e}")

    def _verify(self, issue: Issue) -> bool:
        """对修复项做针对性复检"""
        cat = issue.category
        if cat == "PATH":
            return shutil.which("openclaw") is not None
        if cat == "权限":
            return OPENCLAW_DIR.exists() and not (OPENCLAW_DIR.stat().st_mode & 0o077)
        if cat == "会话目录":
            return SESSIONS_DIR.exists()
        if cat == "网关模式":
            try:
                val = (self._run(["openclaw", "config", "get", "gateway.mode"], timeout=15) or "").strip()
                return bool(val) and "unset" not in val.lower()
            except Exception:
                return False
        return True

    # ───────────────────────── 工具 ─────────────────────────

    def _run(self, cmd: List[str], timeout: int = 20) -> str:
        env = dict(os.environ)
        env["PATH"] = f"{OPENCLAW_BIN}:{env.get('PATH', '')}"
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env)
        return (r.stdout + r.stderr).strip()

    # ───────────────────────── 报告/推送 ─────────────────────────

    def summary(self) -> dict:
        crit = [i for i in self.issues if i.severity == "critical"]
        err = [i for i in self.issues if i.severity == "error"]
        warn = [i for i in self.issues if i.severity == "warning"]
        return {
            "dna": self.DNA,
            "time": datetime.now().isoformat(timespec="seconds"),
            "total": len(self.issues),
            "critical": len(crit),
            "error": len(err),
            "warning": len(warn),
            "repaired": self.repaired,
            "repair_failed": self.repair_failed,
            "issues": [
                {"severity": i.severity, "category": i.category,
                 "message": i.message, "auto_fix": i.auto_fix, "detail": i.detail}
                for i in self.issues
            ],
        }

    def print_report(self, s: dict):
        print("\n" + "=" * 60)
        print("  🐉 OpenClaw 自愈引擎 · 报告")
        print("=" * 60)
        print(f"  发现问题: {s['total']}  (critical {s['critical']} / error {s['error']} / warning {s['warning']})")
        if s["repaired"] or s["repair_failed"]:
            print(f"  已修复: {s['repaired']} / 失败: {s['repair_failed']}")
        for i in s["issues"]:
            icon = {"critical": "🔴", "error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(i["severity"], "•")
            tag = " [自动修复✓]" if i["auto_fix"] else ""
            print(f"  {icon} [{i['category']}] {i['message']}{tag}")
            if i["detail"]:
                print(f"      └ {i['detail']}")
        print("=" * 60)

    def bark_push(self, s: dict, script_path: str):
        """异常时 Bark 推送"""
        if s["total"] == 0:
            return
        level = "red" if s["error"] or s["critical"] else "yellow"
        title = f"🐉 OpenClaw自愈 · {s['total']}个小尾巴"
        body = f"[{s['time']}]\n问题: {s['total']} (critical {s['critical']} / error {s['error']})\n"
        if s["repaired"]:
            body += f"已修复: {s['repaired']}\n"
        for i in s["issues"][:8]:
            body += f"{'🔴' if i['severity'] in ('critical','error') else '⚠️'} [{i['category']}] {i['message']}\n"
        # 尝试走 bark_send.py
        bark = Path(script_path).parent.parent / "executors" / "bark" / "bark_send.py"
        if bark.exists():
            try:
                self._run(["python3", str(bark), title, "--stdin", "--group", "OpenClaw自愈"],
                          timeout=10)
            except Exception:
                pass
        else:
            print("  (无 bark_send.py，跳过推送)")


def main():
    parser = argparse.ArgumentParser(description="OpenClaw 自动自愈引擎")
    parser.add_argument("--check", action="store_true", help="只检查")
    parser.add_argument("--fix", action="store_true", help="自动修复")
    parser.add_argument("--cron", action="store_true", help="静默模式")
    parser.add_argument("--push", action="store_true", help="异常时推送Bark")
    parser.add_argument("--json", action="store_true", help="输出JSON")
    args = parser.parse_args()

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    engine = OpenClawSelfHeal()
    s = engine.summary()

    if args.cron:
        # 静默模式：修复 + 异常推送，无终端输出
        engine.discover()
        engine.repair()
        s = engine.summary()
        if args.push and (s["error"] or s["critical"] or s["repair_failed"]):
            engine.bark_push(s, __file__)
        log = LOG_DIR / "openclaw_self_heal.log"
        with open(log, "a") as f:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
        return 0

    engine.discover()
    s = engine.summary()

    if args.fix:
        print("🐉 开始自动修复...")
        engine.repair()
        s = engine.summary()

    if args.json:
        print(json.dumps(s, indent=2, ensure_ascii=False))
    else:
        engine.print_report(s)

    if args.push and (s["error"] or s["critical"] or s["repair_failed"]):
        engine.bark_push(s, __file__)

    log = LOG_DIR / "openclaw_self_heal.log"
    with open(log, "a") as f:
        f.write(json.dumps(s, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
