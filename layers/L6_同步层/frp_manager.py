# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · FRP 隧道管理引擎 v1.0
DNA: #龍芯⚡️丙午·辛未·FRP-MANAGER-v1.0

架构：
  Mac(frpc) ←→ 公网VPS(frps) ←→ 鲲鹏(frpc)
  本地端口映射: 127.0.0.1:19622 → frps:19622 → 鲲鹏:9633
  本地端口映射: 127.0.0.1:29622 → frps:29622 → 鲲鹏:22 (SSH跳板)

职责：
  - frpc 进程生命周期管理（启动/停止/重启/状态）
  - 隧道健康检查（心跳+超时检测）
  - 多通道复用（API + SSH + 文件传输）
  - 断线自动重连
  - frps 服务端远程部署
"""

import hashlib
import json
import os
import platform
import shutil
import signal
import socket
import subprocess
import sys
import time
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DNA = "#龍芯⚡️丙午·辛未·FRP-MANAGER-v1.0"
CST = timezone(timedelta(hours=8))
UID_ROOT = "UID9622"

# 常量
FRP_VERSION = "0.58.1"
FRP_DIR = ROOT / "frpc"
FRP_BIN = FRP_DIR / "frpc"
FRP_CONF = FRP_DIR / "frpc.toml"
FRP_LOG = ROOT / "logs" / "frpc.log"
FRP_PID_FILE = FRP_DIR / "frpc.pid"

# 端口规划（不冲突现有端口）
# 现有端口: 9622(CNSH操作台) 9633(双节点鲲鹏) 9634(双节点Mac) 9627 9677 8777
FRP_REMOTE_API_PORT = 19622   # Mac本地→公网→鲲鹏API
FRP_REMOTE_SSH_PORT = 29622   # Mac本地→公网→鲲鹏SSH
FRP_REMOTE_MAC_API = 39622    # 鲲鹏→公网→Mac API (备用)

# 本地绑定端口
FRP_LOCAL_API_BIND = 9633     # 本地127.0.0.1:9633 → 走隧道到鲲鹏API
FRP_LOCAL_SSH_BIND = 9622     # 本地127.0.0.1:9622 → 走隧道到鲲鹏SSH


class TunnelStatus(Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    RECONNECTING = "reconnecting"
    ERROR = "error"
    NOT_INSTALLED = "not_installed"


@dataclass
class FrpConfig:
    """FRP 配置"""
    server_addr: str = ""           # 公网VPS IP
    server_port: int = 7000
    auth_token: str = "LONGHUN2026_UID9622_KUNPENG"
    local_api_port: int = 9633      # 本地API端口
    remote_api_port: int = 19622    # 公网映射端口
    local_ssh_port: int = 22
    remote_ssh_port: int = 29622

    @classmethod
    def from_env(cls) -> "FrpConfig":
        """从环境变量或配置文件加载"""
        config = cls()
        config_file = ROOT / "deploy" / ".kunpeng_config"
        if config_file.exists():
            with open(config_file) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    v = v.strip().strip('"').strip("'")
                    k = k.strip()
                    if k == "FRP_SERVER":
                        config.server_addr = v
                    elif k == "FRP_TOKEN":
                        config.auth_token = v
        return config

    def save_to_config_file(self):
        """保存到 deploy/.kunpeng_config"""
        config_file = ROOT / "deploy" / ".kunpeng_config"
        existing = {}
        if config_file.exists():
            with open(config_file) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    existing[k.strip()] = v.strip().strip('"').strip("'")

        existing["FRP_SERVER"] = self.server_addr
        existing["FRP_TOKEN"] = self.auth_token

        with open(config_file, "w") as f:
            f.write("# 龍魂 · 鲲鹏连接配置\n")
            f.write(f"KUNPENG_MGMT_IP={existing.get('KUNPENG_MGMT_IP', '119.13.90.27')}\n")
            f.write(f"KUNPENG_USER={existing.get('KUNPENG_USER', 'root')}\n")
            f.write(f"KUNPENG_SSH_PORT={existing.get('KUNPENG_SSH_PORT', '22')}\n")
            f.write(f"KUNPENG_DEPLOY_PATH={existing.get('KUNPENG_DEPLOY_PATH', '/opt/longhun-system')}\n")
            f.write(f"FRP_SERVER={self.server_addr}\n")
            f.write(f"FRP_TOKEN={self.auth_token}\n")


class FrpManager:
    """FRP 隧道管理器"""

    def __init__(self, config: Optional[FrpConfig] = None):
        self.config = config or FrpConfig.from_env()
        self._pid: Optional[int] = None

    # ─── 安装 ───

    def is_installed(self) -> bool:
        """frpc 二进制是否存在"""
        return FRP_BIN.exists() and os.access(FRP_BIN, os.X_OK)

    def install(self) -> bool:
        """下载对应平台的 frpc"""
        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == "darwin":
            if "arm" in machine or "aarch64" in machine:
                arch = "darwin_arm64"
            else:
                arch = "darwin_amd64"
        elif system == "linux":
            if "aarch64" in machine or "arm64" in machine:
                arch = "linux_arm64"
            elif "arm" in machine:
                arch = "linux_arm"
            else:
                arch = "linux_amd64"
        else:
            print(f"❌ 不支持的系统: {system} {machine}")
            return False

        url = (f"https://github.com/fatedier/frp/releases/download/"
               f"v{FRP_VERSION}/frp_{FRP_VERSION}_{arch}.tar.gz")
        tgz_path = FRP_DIR / f"frp_{FRP_VERSION}_{arch}.tar.gz"

        FRP_DIR.mkdir(parents=True, exist_ok=True)

        print(f"⬇️  下载 frp v{FRP_VERSION} ({arch})...")
        try:
            urllib.request.urlretrieve(url, tgz_path)
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            print(f"   手动下载: {url}")
            print(f"   解压到: {FRP_DIR}")
            return False

        print("📦 解压...")
        import tarfile
        with tarfile.open(tgz_path) as tar:
            extract_dir = FRP_DIR / f"_extract"
            tar.extractall(extract_dir)
            # frp_版本_架构/frpc → frp_dir/frpc
            for item in extract_dir.iterdir():
                if item.is_dir():
                    frpc_src = item / "frpc"
                    if frpc_src.exists():
                        shutil.copy2(frpc_src, FRP_BIN)
                        FRP_BIN.chmod(0o755)

        # 清理
        shutil.rmtree(FRP_DIR / "_extract", ignore_errors=True)
        tgz_path.unlink(missing_ok=True)

        print(f"✅ frpc 已安装: {FRP_BIN}")
        return self.is_installed()

    # ─── 配置 ───

    def generate_config(self) -> str:
        """生成 frpc.toml"""
        conf = f"""# 龍魂系统 · Mac frpc 配置
# DNA: {DNA}
# 生成时间: {datetime.now(CST).isoformat()}

serverAddr = "{self.config.server_addr}"
serverPort = {self.config.server_port}
auth.method = "token"
auth.token = "{self.config.auth_token}"

# ── 鲲鹏 API 通道 ──
[[proxies]]
name = "longhun-kunpeng-api"
type = "tcp"
localIP = "127.0.0.1"
localPort = {self.config.local_api_port}
remotePort = {self.config.remote_api_port}

# ── 鲲鹏 SSH 跳板 ──
[[proxies]]
name = "longhun-kunpeng-ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = {FRP_LOCAL_SSH_BIND}
remotePort = {self.config.remote_ssh_port}

# ── Mac API 暴露（供鲲鹏回连） ──
[[proxies]]
name = "longhun-mac-api"
type = "tcp"
localIP = "127.0.0.1"
localPort = 9634
remotePort = 39622

# ── 访问鲲鹏（STCP visitor模式） ──
[[visitors]]
name = "visit-kunpeng-direct"
type = "stcp"
serverName = "longhun-kunpeng-api"
secretKey = "{self.config.auth_token}"
bindAddr = "127.0.0.1"
bindPort = 9633
"""
        FRP_DIR.mkdir(parents=True, exist_ok=True)
        FRP_CONF.write_text(conf)
        return conf

    # ─── 生命周期 ───

    def start(self) -> Tuple[bool, str]:
        """启动 frpc 隧道"""
        if not self.is_installed():
            return False, "frpc 未安装，请先执行 lh tunnel install"

        if self.is_running():
            return True, f"frpc 已在运行 (PID: {self._get_pid()})"

        if not FRP_CONF.exists():
            self.generate_config()

        # 确保日志目录
        FRP_LOG.parent.mkdir(parents=True, exist_ok=True)

        try:
            log_f = open(FRP_LOG, "a")
            proc = subprocess.Popen(
                [str(FRP_BIN), "-c", str(FRP_CONF)],
                stdout=log_f, stderr=log_f,
                start_new_session=True,
            )
            FRP_PID_FILE.write_text(str(proc.pid))
            time.sleep(2)

            if self.is_running():
                return True, f"frpc 已启动 (PID: {proc.pid})"
            else:
                return False, "frpc 启动失败，查看日志: tail -20 " + str(FRP_LOG)
        except Exception as e:
            return False, f"启动失败: {e}"

    def stop(self) -> Tuple[bool, str]:
        """停止 frpc"""
        pid = self._get_pid()
        if not pid:
            # 尝试 pkill
            try:
                subprocess.run(["pkill", "-f", "frpc.*frpc.toml"], capture_output=True)
            except Exception:
                pass
            FRP_PID_FILE.unlink(missing_ok=True)
            return True, "frpc 已停止"

        try:
            os.kill(pid, signal.SIGTERM)
            time.sleep(1)
            if self._get_pid():
                os.kill(pid, signal.SIGKILL)
            FRP_PID_FILE.unlink(missing_ok=True)
            return True, "frpc 已停止"
        except ProcessLookupError:
            FRP_PID_FILE.unlink(missing_ok=True)
            return True, "frpc 已停止"
        except Exception as e:
            return False, f"停止失败: {e}"

    def restart(self) -> Tuple[bool, str]:
        """重启 frpc"""
        self.stop()
        time.sleep(1)
        return self.start()

    # ─── 状态 ───

    def _get_pid(self) -> Optional[int]:
        """从 PID 文件或进程列表获取 frpc PID"""
        if FRP_PID_FILE.exists():
            try:
                pid = int(FRP_PID_FILE.read_text().strip())
                os.kill(pid, 0)  # 检查进程是否存在
                return pid
            except (ValueError, ProcessLookupError, PermissionError):
                FRP_PID_FILE.unlink(missing_ok=True)

        # fallback: 从进程列表查找
        try:
            result = subprocess.run(
                ["pgrep", "-f", "frpc.*frpc.toml"],
                capture_output=True, text=True
            )
            if result.stdout.strip():
                pid = int(result.stdout.strip().split("\n")[0])
                FRP_PID_FILE.write_text(str(pid))
                return pid
        except Exception:
            pass

        return None

    def is_running(self) -> bool:
        """隧道是否在运行"""
        return self._get_pid() is not None

    def status(self) -> Dict[str, Any]:
        """完整状态"""
        installed = self.is_installed()
        running = self.is_running()
        pid = self._get_pid()

        status = {
            "dna": DNA,
            "uid": UID_ROOT,
            "timestamp": datetime.now(CST).isoformat(),
            "installed": installed,
            "running": running,
            "pid": pid,
            "server_addr": self.config.server_addr,
            "bindings": {
                "kunpeng_api": f"127.0.0.1:{self.config.local_api_port} → :{self.config.remote_api_port}",
                "kunpeng_ssh": f"127.0.0.1:{FRP_LOCAL_SSH_BIND} → :{self.config.remote_ssh_port}",
            },
        }

        # 各通道健康状况
        status["channels"] = self._check_channels()

        # 日志最后几行
        if FRP_LOG.exists():
            try:
                lines = FRP_LOG.read_text().split("\n")[-5:]
                status["last_logs"] = [l for l in lines if l.strip()]
            except Exception:
                status["last_logs"] = []

        return status

    def _check_channels(self) -> Dict[str, bool]:
        """检查各通道连通性"""
        channels = {}

        # API 通道
        try:
            url = f"http://127.0.0.1:{self.config.local_api_port}/health"
            req = urllib.request.Request(url, method="GET")
            resp = urllib.request.urlopen(req, timeout=5)
            data = json.loads(resp.read().decode())
            channels["kunpeng_api"] = data.get("node_role") == "kunpeng"
        except Exception:
            channels["kunpeng_api"] = False

        # SSH 通道
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex(("127.0.0.1", FRP_LOCAL_SSH_BIND))
            sock.close()
            channels["kunpeng_ssh"] = result == 0
        except Exception:
            channels["kunpeng_ssh"] = False

        return channels

    def health_check(self) -> Dict[str, Any]:
        """快速健康检查"""
        st = self.status()
        api_ok = st["channels"].get("kunpeng_api", False)
        return {
            "dna": DNA,
            "timestamp": datetime.now(CST).isoformat(),
            "tunnel_running": st["running"],
            "api_reachable": api_ok,
            "status": "healthy" if (st["running"] and api_ok) else "degraded",
            "fallback_available": self._can_ssh_direct(),
        }

    def _can_ssh_direct(self) -> bool:
        """降级检查：直接 SSH 是否可用"""
        try:
            from L6_同步层.dual_node_protocol import DualNodeProtocol
            proto = DualNodeProtocol()
            result = proto.test_connection()
            return result.get("ssh_ok", False)
        except Exception:
            return False

    # ─── 日志 ───

    def tail_logs(self, lines: int = 30) -> str:
        """获取最近日志"""
        if not FRP_LOG.exists():
            return "日志文件不存在"
        try:
            return "\n".join(FRP_LOG.read_text().split("\n")[-lines:])
        except Exception as e:
            return f"读取日志失败: {e}"

    # ─── 远程部署 ───

    @staticmethod
    def generate_frps_config(
        token: str = "LONGHUN2026_UID9622_KUNPENG",
        web_password: str = "UID9622_ADMIN",
        web_port: int = 7500,
    ) -> str:
        """生成 frps.toml（用于部署到公网VPS）"""
        return f"""# ═══════════════════════════════════════
# 龍魂系统 · frps 服务端配置
# DNA: {DNA}
# UID: {UID_ROOT}
# ═══════════════════════════════════════

bindPort = 7000
auth.method = "token"
auth.token = "{token}"

# ── Web 管理面板 ──
webServer.addr = "0.0.0.0"
webServer.port = {web_port}
webServer.user = "longhun"
webServer.password = "{web_password}"

# ── 龍魂代理 ──
# Mac → 鲲鹏 API 通道
[[proxies]]
name = "longhun-kunpeng-api"
type = "tcp"
localPort = 9633
remotePort = 19622

# Mac → 鲲鹏 SSH 跳板
[[proxies]]
name = "longhun-kunpeng-ssh"
type = "tcp"
localPort = 22
remotePort = 29622

# 鲲鹏 → Mac API（备用反向通道）
[[proxies]]
name = "longhun-mac-api"
type = "tcp"
localPort = 9634
remotePort = 39622

allowPorts = [
  {{ start = 19622, end = 19622 }},
  {{ start = 29622, end = 29622 }},
  {{ start = 39622, end = 39622 }}
]

# 连接池
transport.maxPoolCount = 50
transport.tcpMuxKeepaliveInterval = 30
transport.heartbeatTimeout = 90

# 日志
log.to = "/opt/frp/frps.log"
log.level = "info"
log.maxDays = 30
"""

    @staticmethod
    def generate_frpc_kunpeng_config(
        server_addr: str,
        token: str = "LONGHUN2026_UID9622_KUNPENG",
    ) -> str:
        """生成鲲鹏端 frpc.toml"""
        return f"""# 龍魂系统 · 鲲鹏 frpc 配置
# DNA: {DNA}

serverAddr = "{server_addr}"
serverPort = 7000
auth.method = "token"
auth.token = "{token}"

# 暴露 API 到公网
[[proxies]]
name = "longhun-kunpeng-api"
type = "tcp"
localIP = "127.0.0.1"
localPort = 9633
remotePort = 19622

# 暴露 SSH 跳板
[[proxies]]
name = "longhun-kunpeng-ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 29622

# 日志
log.to = "/opt/longhun-system/logs/frpc.log"
log.level = "info"
log.maxDays = 30
"""

    @staticmethod
    def generate_frpc_mac_config(
        server_addr: str,
        token: str = "LONGHUN2026_UID9622_KUNPENG",
    ) -> str:
        """生成 Mac 端 frpc.toml"""
        return f"""# 龍魂系统 · Mac frpc 配置
# DNA: {DNA}

serverAddr = "{server_addr}"
serverPort = 7000
auth.method = "token"
auth.token = "{token}"

# 反向访问鲲鹏API：本机127.0.0.1:9633 = 鲲鹏9633
[[visitors]]
name = "visit-kunpeng-api"
type = "stcp"
serverName = "longhun-kunpeng-api"
secretKey = "{token}"
bindAddr = "127.0.0.1"
bindPort = 9633

# 反向访问鲲鹏SSH：本机127.0.0.1:19622 = 鲲鹏22
[[visitors]]
name = "visit-kunpeng-ssh"
type = "stcp"
serverName = "longhun-kunpeng-ssh"
secretKey = "{token}"
bindAddr = "127.0.0.1"
bindPort = 19622

# 日志
log.to = "{ROOT}/logs/frpc.log"
log.level = "info"
log.maxDays = 30
"""


# ─── CLI ───

def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂 FRP 隧道管理引擎")
    sub = parser.add_subparsers(dest="cmd")

    # install
    p_install = sub.add_parser("install", help="下载 frpc 二进制")

    # start / stop / restart
    p_start = sub.add_parser("start", help="启动 frpc 隧道")
    p_stop = sub.add_parser("stop", help="停止 frpc 隧道")
    p_restart = sub.add_parser("restart", help="重启 frpc 隧道")

    # status
    p_status = sub.add_parser("status", help="隧道状态")
    p_status.add_argument("--json", action="store_true", help="JSON 输出")

    # health
    p_health = sub.add_parser("health", help="快速健康检查")
    p_health.add_argument("--json", action="store_true")

    # log
    p_log = sub.add_parser("log", help="查看最近日志")
    p_log.add_argument("-n", type=int, default=30, help="行数")

    # config
    p_config = sub.add_parser("config", help="查看/生成配置")
    p_config.add_argument("--server", help="设置公网服务器IP")
    p_config.add_argument("--token", help="设置认证Token")

    # generate — 生成各端的配置文件（供手动部署用）
    p_gen = sub.add_parser("generate", help="生成部署配置文件")
    p_gen.add_argument("--target", choices=["frps", "frpc-kunpeng", "frpc-mac"], default="frps")
    p_gen.add_argument("--server", default="", help="公网服务器IP")
    p_gen.add_argument("--token", default="LONGHUN2026_UID9622_KUNPENG")
    p_gen.add_argument("--web-password", default="UID9622_ADMIN", help="面板密码")

    # daemon — 守护模式（持续监控+自动重连）
    p_daemon = sub.add_parser("daemon", help="守护模式（自动监控+重连）")
    p_daemon.add_argument("--interval", type=int, default=30, help="检查间隔（秒）")

    args = parser.parse_args()

    cfg = FrpConfig.from_env()
    mgr = FrpManager(cfg)

    if args.cmd == "install":
        print(f"🐉 安装 frpc v{FRP_VERSION}...")
        mgr.install()

    elif args.cmd == "start":
        ok, msg = mgr.start()
        print(f"{'✅' if ok else '❌'} {msg}")

    elif args.cmd == "stop":
        ok, msg = mgr.stop()
        print(f"{'✅' if ok else '❌'} {msg}")

    elif args.cmd == "restart":
        ok, msg = mgr.restart()
        print(f"{'✅' if ok else '❌'} {msg}")

    elif args.cmd == "status":
        st = mgr.status()
        if args.json:
            print(json.dumps(st, ensure_ascii=False, indent=2))
        else:
            print(f"🐉 FRP 隧道状态")
            print(f"   frpc: {'✅ 已安装' if st['installed'] else '❌ 未安装'}")
            print(f"   运行: {'🟢 运行中' if st['running'] else '🔴 已停止'} {'(PID: ' + str(st['pid']) + ')' if st['pid'] else ''}")
            print(f"   服务器: {st['server_addr'] or '未配置'}")
            print(f"   通道:")
            for name, ok in st["channels"].items():
                print(f"     {name}: {'🟢' if ok else '🔴'}")

    elif args.cmd == "health":
        h = mgr.health_check()
        if args.json:
            print(json.dumps(h, ensure_ascii=False, indent=2))
        else:
            print(f"🐉 健康检查")
            print(f"   隧道: {'🟢 正常' if h['tunnel_running'] else '🔴 异常'}")
            print(f"   API: {'🟢 可达' if h['api_reachable'] else '🔴 不可达'}")
            print(f"   SSH降级: {'✅ 可用' if h['fallback_available'] else '❌ 不可用'}")
            print(f"   状态: {h['status']}")

    elif args.cmd == "log":
        print(mgr.tail_logs(args.n))

    elif args.cmd == "config":
        if args.server:
            cfg.server_addr = args.server
        if args.token:
            cfg.auth_token = args.token
        cfg.save_to_config_file()
        print(f"✅ 配置已保存")
        print(f"   服务器: {cfg.server_addr}")
        print(f"   Token: {'***' + cfg.auth_token[-4:]}")

        conf = mgr.generate_config()
        print(f"\n当前 frpc.toml:")
        print(conf)

    elif args.cmd == "generate":
        if args.target == "frps":
            print(FrpManager.generate_frps_config(
                token=args.token,
                web_password=args.web_password,
            ))
        elif args.target == "frpc-kunpeng":
            print(FrpManager.generate_frpc_kunpeng_config(
                server_addr=args.server,
                token=args.token,
            ))
        elif args.target == "frpc-mac":
            print(FrpManager.generate_frpc_mac_config(
                server_addr=args.server,
                token=args.token,
            ))

    elif args.cmd == "daemon":
        interval = args.interval
        print(f"🐉 FRP 守护进程启动 (间隔: {interval}s)")
        fail_count = 0
        last_restart = 0

        while True:
            try:
                h = mgr.health_check()
                if h["status"] != "healthy":
                    fail_count += 1
                    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] 🔴 隧道异常 (连续{fail_count}次)")

                    if fail_count >= 3 and time.time() - last_restart > 60:
                        print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] 🔄 自动重启...")
                        mgr.restart()
                        last_restart = time.time()
                        fail_count = 0
                else:
                    if fail_count > 0:
                        print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] 🟢 隧道恢复")
                    fail_count = 0

                time.sleep(interval)
            except KeyboardInterrupt:
                print("\n👋 守护进程退出")
                break
            except Exception as e:
                print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] ⚠️ 守护异常: {e}")
                time.sleep(interval)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
