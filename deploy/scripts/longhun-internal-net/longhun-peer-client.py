#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║  龍魂·内网互联节点客户端 v1.0 — 安全加固版                          ║
║  DNA: #龍芯⚡️丙午·辛未·乙酉·未时·䷾既济-INTERNAL-NET-PEER-v1.0    ║
║  #CONFIRM🌌9622-ONLY-ONCE🧬NET2-001A                                ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                      ║
║                                                                      ║
║  即插即用 · 零配置 · 自动发现 · 局域网满速                           ║
║  任何设备: Mac/Win/Linux/手机/树莓派，统一客户端                     ║
║                                                                      ║
║  主权人: UID9622 💎 龍芯北辰·诸葛鑫·Lucky                           ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import os, sys, json, time, socket, hashlib, secrets, threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import platform
import subprocess
import logging

try:
    import requests
except ImportError:
    print("❌ 需要 requests: pip install requests")
    sys.exit(1)

# ═══════════════════════════════════════════════════════
# L0 常量 · 焊死
# ═══════════════════════════════════════════════════════

DNA = "#龍芯⚡️丙午·辛未·乙酉·未时·䷾既济-INTERNAL-NET-PEER-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬NET2-001A"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
SOVEREIGN_UID = "UID9622"
GATEWAY_DEFAULT_PORT = 9622

# 日志配置
LOG_DIR = Path.home() / ".longhun" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "internal_net_peer.log"),
        logging.StreamHandler(sys.stderr),
    ]
)
logger = logging.getLogger("lh_peer")

# ═══════════════════════════════════════════════════════
# 网络工具
# ═══════════════════════════════════════════════════════

def get_local_ip(gateway_hint: str = None) -> str:
    """获取本机局域网IP"""
    try:
        # 方法1: 通过连接网关获取
        if gateway_hint:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(1)
                s.connect((gateway_hint, 80))
                ip = s.getsockname()[0]
                s.close()
                return ip
            except:
                pass

        # 方法2: 通过路由表
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            pass

        # 方法3: hostname -I
        try:
            result = subprocess.run(["hostname", "-I"], capture_output=True, text=True)
            ip = result.stdout.strip().split()[0]
            if ip:
                return ip
        except:
            pass

        return "127.0.0.1"
    except:
        return "127.0.0.1"


def discover_gateway(subnet: str, port: int = GATEWAY_DEFAULT_PORT, timeout: float = 0.3) -> Optional[str]:
    """扫描局域网发现网关"""
    logger.info(f"🔍 扫描网关: {subnet}.0/24 ...")

    # 常见网关位置先检查
    common = [f"{subnet}.1", f"{subnet}.100", f"{subnet}.254"]
    for ip in common:
        try:
            resp = requests.get(f"http://{ip}:{port}/health", timeout=timeout)
            if resp.status_code == 200:
                data = resp.json()
                if "dna" in data and "龍" in data.get("status", ""):
                    logger.info(f"✅ 发现龍魂网关: {ip}")
                    return ip
        except:
            pass

    # 批量扫描 .1~.254
    for i in range(1, 255):
        target = f"{subnet}.{i}"
        if target in common:
            continue
        try:
            resp = requests.get(f"http://{target}:{port}/health", timeout=timeout)
            if resp.status_code == 200:
                data = resp.json()
                if "dna" in data:
                    logger.info(f"✅ 发现龍魂网关: {target}")
                    return target
        except:
            continue

    return None


def detect_device_type() -> str:
    """自动检测设备类型"""
    system = platform.system().lower()
    if system == "darwin":
        return "mac"
    elif system == "windows":
        return "win"
    elif system == "linux":
        # 进一步区分
        try:
            with open("/proc/cpuinfo") as f:
                content = f.read().lower()
            if "kunpeng" in content or "taishan" in content:
                return "kunpeng"
            if "loongson" in content:
                return "loongson"
        except:
            pass
        # 检测是否树莓派
        try:
            with open("/proc/device-tree/model") as f:
                if "raspberry" in f.read().lower():
                    return "raspberry"
        except:
            pass
        return "linux"
    else:
        return "unknown"


def detect_arch() -> str:
    """检测CPU架构"""
    machine = platform.machine().lower()
    if machine in ("aarch64", "arm64"):
        return "aarch64"
    elif "arm" in machine:
        return "arm32"
    elif machine in ("x86_64", "amd64"):
        return "x86_64"
    elif machine in ("loongarch64",):
        return "loongarch64"
    return machine


def detect_cpu_info() -> Dict:
    """检测CPU信息"""
    info = {
        "arch": detect_arch(),
        "cores": os.cpu_count() or 1,
    }
    system = platform.system().lower()

    if system == "linux":
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        info["cpu"] = line.split(":")[1].strip()
                        break
                    elif "Processor" in line:
                        info["cpu"] = line.split(":")[1].strip()
                        break
        except:
            pass
    elif system == "darwin":
        try:
            result = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True)
            info["cpu"] = result.stdout.strip()
        except:
            pass

    return info


# ═══════════════════════════════════════════════════════
# 龍魂 Peer 客户端
# ═══════════════════════════════════════════════════════

class LonghunPeer:
    """龍魂内网节点 — 安全加固版"""

    def __init__(self, device_name: str = None, device_type: str = None, gateway: str = None):
        self.device_type = device_type or detect_device_type()
        self.arch_info = detect_cpu_info()

        # 设备名
        if device_name:
            self.device_name = device_name
        else:
            self.device_name = f"{self.device_type}_{socket.gethostname()}"

        # 设备ID — 基于设备指纹的稳定ID
        device_fingerprint = f"{self.device_name}{self.device_type}{self.arch_info.get('arch','')}{platform.node()}"
        self.device_id = hashlib.sha256(device_fingerprint.encode()).hexdigest()[:12]

        # 网关
        self.gateway_host = gateway
        self.gateway_port = GATEWAY_DEFAULT_PORT

        # 状态
        self.registered = False
        self.chip_tier = None
        self.chip_score = None
        self.last_msg_time = "1970-01-01T00:00:00"
        self.session_id = secrets.token_hex(8)

        # 回调
        self.on_message: Optional[callable] = None
        self.on_peer_join: Optional[callable] = None
        self.on_peer_leave: Optional[callable] = None

        # 统计
        self.stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "files_uploaded": 0,
            "files_downloaded": 0,
        }

    @property
    def gateway_url(self) -> str:
        return f"http://{self.gateway_host}:{self.gateway_port}"

    # ═══════════════════════════════════════════════════
    # 网关发现
    # ═══════════════════════════════════════════════════

    def discover_and_set_gateway(self) -> bool:
        """自动发现网关"""
        if self.gateway_host:
            # 验证用户指定的网关
            try:
                resp = requests.get(f"{self.gateway_url}/health", timeout=3)
                if resp.status_code == 200:
                    logger.info(f"✅ 连接到指定网关: {self.gateway_host}")
                    return True
            except:
                logger.warning(f"⚠️ 指定网关 {self.gateway_host} 不可达，尝试自动发现...")

        my_ip = get_local_ip()
        subnet = ".".join(my_ip.split(".")[:3])
        discovered = discover_gateway(subnet, self.gateway_port)

        if discovered:
            self.gateway_host = discovered
            return True

        logger.error("❌ 未发现龍魂网关")
        return False

    # ═══════════════════════════════════════════════════
    # 注册
    # ═══════════════════════════════════════════════════

    def register(self) -> bool:
        """注册到网关"""
        if not self.gateway_host:
            if not self.discover_and_set_gateway():
                return False

        my_ip = get_local_ip(self.gateway_host)

        payload = {
            "id": self.device_id,
            "ip": my_ip,
            "name": self.device_name,
            "type": self.device_type,
            "arch": self.arch_info.get("arch", ""),
            "cpu": self.arch_info.get("cpu", ""),
            "hostname": platform.node(),
            "os": platform.system(),
            "capabilities": ["chat", "file", "stream"],
            "session": self.session_id,
            "dna": DNA,
        }

        try:
            resp = requests.post(
                f"{self.gateway_url}/register",
                json=payload,
                timeout=10,
            )
            data = resp.json()

            if data.get("registered"):
                self.registered = True
                self.chip_tier = data.get("chip_verdict", {}).get("tier", "未知")
                self.chip_score = data.get("chip_verdict", {}).get("score", 0)

                logger.info(f"🐉 注册成功: {self.device_name} ({self.device_id})")
                logger.info(f"   芯片: {self.chip_tier} ({self.chip_score}分)")
                logger.info(f"   在线节点: {data.get('peers_online', 0)}个")
                logger.info(f"   IP: {my_ip}")

                # 注册时同步DNA验证
                gw_dna = data.get("gateway_info", {}).get("dna", "")
                if "龍芯" in gw_dna:
                    logger.info(f"   🟢 DNA验证通过")
                else:
                    logger.warning(f"   ⚠️ 网关DNA验证异常")

                return True
            else:
                logger.error(f"❌ 注册被拒绝: {data.get('error', '未知原因')}")
                return False

        except requests.exceptions.ConnectionError:
            logger.error(f"❌ 无法连接网关: {self.gateway_url}")
            return False
        except Exception as e:
            logger.error(f"❌ 注册失败: {e}")
            return False

    # ═══════════════════════════════════════════════════
    # 心跳
    # ═══════════════════════════════════════════════════

    def heartbeat(self):
        """心跳线程"""
        consecutive_failures = 0
        while True:
            if self.registered:
                try:
                    resp = requests.post(
                        f"{self.gateway_url}/heartbeat/{self.device_id}",
                        timeout=5,
                    )
                    if resp.status_code == 200:
                        consecutive_failures = 0
                    else:
                        consecutive_failures += 1
                except:
                    consecutive_failures += 1

                if consecutive_failures >= 3:
                    logger.warning("⚠️ 心跳丢失，尝试重新注册...")
                    self.registered = False
                    if self.discover_and_set_gateway():
                        self.register()
                    consecutive_failures = 0

            else:
                # 未注册，尝试重新发现和注册
                if self.discover_and_set_gateway():
                    self.register()

            time.sleep(60)  # 每分钟心跳

    # ═══════════════════════════════════════════════════
    # 消息
    # ═══════════════════════════════════════════════════

    def send_message(self, content: str, to: str = None, msg_type: str = "text", room: str = "broadcast") -> Optional[str]:
        """发送消息"""
        if not self.registered:
            logger.warning("⚠️ 未注册，无法发送")
            return None

        try:
            resp = requests.post(
                f"{self.gateway_url}/message/send",
                json={
                    "from": self.device_id,
                    "to": to,
                    "type": msg_type,
                    "content": content,
                    "room_id": room,
                    "dna": DNA,
                },
                timeout=10,
            )
            data = resp.json()
            if data.get("sent"):
                self.stats["messages_sent"] += 1
                return data.get("msg_id")
            else:
                logger.warning(f"⚠️ 发送被拒: {data.get('error', '')}")
                return None
        except Exception as e:
            logger.error(f"❌ 发送失败: {e}")
            return None

    def receive_messages(self, room: str = "broadcast") -> List[Dict]:
        """拉取消息"""
        if not self.registered:
            return []

        try:
            resp = requests.get(
                f"{self.gateway_url}/message/receive/{self.device_id}",
                params={"room_id": room, "since": self.last_msg_time},
                timeout=10,
            )
            data = resp.json()
            msgs = data.get("messages", [])

            if msgs:
                self.last_msg_time = msgs[-1].get("timestamp", self.last_msg_time)
                self.stats["messages_received"] += len(msgs)

            return msgs
        except:
            return []

    # ═══════════════════════════════════════════════════
    # 文件
    # ═══════════════════════════════════════════════════

    def upload_file(self, filepath: str) -> Optional[Dict]:
        """上传文件到内网缓存"""
        if not self.registered:
            logger.warning("⚠️ 未注册")
            return None

        if not os.path.exists(filepath):
            logger.error(f"❌ 文件不存在: {filepath}")
            return None

        try:
            with open(filepath, "rb") as f:
                resp = requests.post(
                    f"{self.gateway_url}/file/upload",
                    files={"file": (os.path.basename(filepath), f)},
                    data={"device_id": self.device_id},
                    timeout=120,
                )
            data = resp.json()
            if data.get("uploaded"):
                self.stats["files_uploaded"] += 1
                logger.info(f"📁 上传: {data['original_name']} → {data['filename']} ({data['size']} bytes)")
                return data
            else:
                logger.warning(f"⚠️ 上传失败: {data.get('error', '')}")
                return None
        except Exception as e:
            logger.error(f"❌ 上传失败: {e}")
            return None

    def download_file(self, filename: str, save_dir: str = ".") -> Optional[str]:
        """下载文件"""
        if not self.registered:
            return None

        try:
            resp = requests.get(
                f"{self.gateway_url}/file/download/{filename}",
                timeout=120,
                stream=True,
            )
            if resp.status_code == 200:
                save_path = os.path.join(save_dir, filename)
                with open(save_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                self.stats["files_downloaded"] += 1
                logger.info(f"📥 下载: {filename} → {save_path}")
                return save_path
            else:
                logger.warning(f"⚠️ 下载失败: {resp.status_code}")
                return None
        except Exception as e:
            logger.error(f"❌ 下载失败: {e}")
            return None

    # ═══════════════════════════════════════════════════
    # 节点管理
    # ═══════════════════════════════════════════════════

    def get_peers(self) -> List[Dict]:
        """获取在线节点列表"""
        try:
            resp = requests.get(f"{self.gateway_url}/peers", timeout=5)
            return resp.json().get("peers", [])
        except:
            return []

    def get_health(self) -> Optional[Dict]:
        """获取网关健康状态"""
        try:
            resp = requests.get(f"{self.gateway_url}/health", timeout=5)
            return resp.json()
        except:
            return None

    # ═══════════════════════════════════════════════════
    # 消息循环
    # ═══════════════════════════════════════════════════

    def _message_loop(self):
        """后台消息接收循环"""
        while True:
            try:
                msgs = self.receive_messages()
                for msg in msgs:
                    # 排除自己发的内容
                    sender = msg.get("from", "")
                    if sender == self.device_id:
                        continue

                    content = msg.get("content", "")
                    msg_type = msg.get("type", "text")

                    # 触发回调
                    if self.on_message:
                        self.on_message(sender, content, msg_type, msg)

            except Exception as e:
                logger.debug(f"消息接收异常: {e}")

            time.sleep(2)  # 2秒轮询

    # ═══════════════════════════════════════════════════
    # 启动
    # ═══════════════════════════════════════════════════

    def start(self, max_retries: int = 10):
        """启动客户端"""
        retries = 0
        while not self.registered and retries < max_retries:
            if retries > 0:
                logger.info(f"⏳ 重试 ({retries}/{max_retries})...")
                time.sleep(5 * min(retries, 6))

            self.register()
            retries += 1

        if not self.registered:
            logger.error("❌ 无法注册，请检查：")
            logger.error("   1. 是否与鲲鹏网关在同一局域网")
            logger.error("   2. 鲲鹏网关是否已启动 (python3 longhun-api-gateway.py)")
            logger.error("   3. 防火墙是否拦截了端口 9622")
            return False

        # 启动心跳线程
        threading.Thread(target=self.heartbeat, daemon=True, name="heartbeat").start()

        # 启动消息接收线程
        threading.Thread(target=self._message_loop, daemon=True, name="msg_loop").start()

        logger.info(f"🐉 龍魂节点就绪: {self.device_name}")
        logger.info(f"   发送: peer.send_message('你好')")
        logger.info(f"   查看: peer.get_peers()")
        logger.info(f"   上传: peer.upload_file('/path/to/file')")
        return True

# ═══════════════════════════════════════════════════════
# CLI 交互模式
# ═══════════════════════════════════════════════════════

def interactive_cli(peer: LonghunPeer):
    """命令行交互模式"""
    print(f"\n{'='*60}")
    print(f"  🐉 龍魂内网节点 - {peer.device_name}")
    print(f"  ID: {peer.device_id}  芯片: {peer.chip_tier}")
    print(f"  网关: {peer.gateway_url}")
    print(f"{'='*60}")
    print(f"  /peers   - 查看在线节点")
    print(f"  /file    - 上传文件  用法: /file /path/to/file")
    print(f"  /info    - 本机信息")
    print(f"  /health  - 网关健康")
    print(f"  /help    - 帮助")
    print(f"  /quit    - 退出")
    print(f"  直接输入文字即可群发消息")
    print(f"{'='*60}\n")

    try:
        while True:
            text = input("> ").strip()
            if not text:
                continue

            if text == "/quit":
                break

            elif text == "/peers":
                peers = peer.get_peers()
                if peers:
                    print(f"\n  📡 在线节点 ({len(peers)}):")
                    for p in peers:
                        icon = {"online": "🟢", "offline": "⚫"}.get(p.get("status", ""), "❓")
                        print(f"    {icon} {p['name']:15s} | {p.get('type','?')} | {p.get('chip_tier','?')}")
                else:
                    print("  📡 暂无在线节点")
                print()

            elif text.startswith("/file "):
                filepath = text[6:].strip()
                result = peer.upload_file(filepath)
                if result:
                    print(f"  ✅ 上传成功: {result.get('filename')} ({result.get('size',0)} bytes)")
                    print(f"     下载链接: {peer.gateway_url}/file/download/{result.get('filename')}")
                else:
                    print(f"  ❌ 上传失败")

            elif text == "/info":
                print(f"\n  🖥️ 设备: {peer.device_name}")
                print(f"     类型: {peer.device_type}")
                print(f"     ID: {peer.device_id}")
                print(f"     架构: {peer.arch_info.get('arch', '?')}")
                print(f"     CPU: {peer.arch_info.get('cpu', '?')}")
                print(f"     芯片层级: {peer.chip_tier} ({peer.chip_score}分)")
                print(f"     网关: {peer.gateway_url}")
                print(f"     状态: {'🟢 在线' if peer.registered else '🔴 离线'}")
                print(f"     统计: 发送{peer.stats['messages_sent']} | 收到{peer.stats['messages_received']} | 上传{peer.stats['files_uploaded']} | 下载{peer.stats['files_downloaded']}")
                print()

            elif text == "/health":
                health = peer.get_health()
                if health:
                    print(f"\n  🏥 网关健康:")
                    print(f"     状态: {health.get('status', '?')}")
                    print(f"     在线节点: {health.get('peers', 0)}个")
                    audit_stats = health.get('audit', {})
                    print(f"     审计: 🟢{audit_stats.get('green',0)} 🟡{audit_stats.get('yellow',0)} 🔴{audit_stats.get('red',0)}")
                else:
                    print(f"  ❌ 网关不可达")
                print()

            elif text == "/help":
                print(f"\n  📖 命令列表:")
                print(f"    /peers       查看在线节点")
                print(f"    /file <路径>  上传文件")
                print(f"    /info        本机信息")
                print(f"    /health      网关健康")
                print(f"    /help        此帮助")
                print(f"    /quit        退出")
                print(f"    直接输入文字  群发消息到所有节点")
                print()

            else:
                # 群发消息
                msg_id = peer.send_message(text)
                if msg_id:
                    print(f"  ✅ 已发送 (ID: {msg_id[:12]}...)")
                else:
                    print(f"  ❌ 发送失败")

    except KeyboardInterrupt:
        pass

    print("\n👋 龍魂节点已退出")

# ═══════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="🐉 龍魂内网互联节点客户端")
    parser.add_argument("name", nargs="?", default=None, help="设备名称")
    parser.add_argument("type", nargs="?", default=None,
                        choices=["mac", "win", "linux", "kunpeng", "loongson", "phone", "pad", "raspberry", "auto"],
                        help="设备类型 (默认自动检测)")
    parser.add_argument("gateway", nargs="?", default=None, help="网关IP (默认自动发现)")
    parser.add_argument("--port", type=int, default=GATEWAY_DEFAULT_PORT, help="网关端口")
    parser.add_argument("--no-interactive", action="store_true", help="非交互模式（仅后台运行）")
    parser.add_argument("--daemon", action="store_true", help="守护进程模式")
    args = parser.parse_args()

    device_type = args.type if args.type != "auto" else None

    peer = LonghunPeer(
        device_name=args.name,
        device_type=device_type,
        gateway=args.gateway,
    )

    # 设置消息回调
    def on_msg(sender, content, msg_type, msg):
        """默认消息处理"""
        if msg_type == "file":
            print(f"\n📎 [{sender}] 发送了文件: {content}")
            print(f"   下载: {peer.gateway_url}/file/download/{content}")
        elif msg_type == "alert":
            print(f"\n🚨 [{sender}] 警报: {content}")
        else:
            print(f"\n💬 [{sender}]: {content}")

    peer.on_message = on_msg

    if not peer.start():
        if args.daemon:
            logger.error("守护模式启动失败，30秒后重试...")
            time.sleep(30)
            sys.exit(1)
        else:
            sys.exit(1)

    if args.daemon:
        logger.info("🐉 守护模式运行中...")
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            pass
    elif args.no_interactive:
        logger.info("🐉 后台模式运行中...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    else:
        interactive_cli(peer)
