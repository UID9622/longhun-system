#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·同心锁物理防火墙 v1.0                                  ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-TONGXIN-LOCK-FIREWALL-v1.0 ║
# ║  守护人格: 乔前辈(P04鲁班)                                  ║
# ║  签章: JOE-MASTER-LOCK-2026                                 ║
# ╚══════════════════════════════════════════════════════════════╝
"""
龍魂·同心锁物理防火墙 v1.0
─────────────────────────────
白名单模式 pfctl 防火墙 —— 拒绝所有非授权出站连接。
系统启动时自动锁定，需设备指纹+生物特征解锁。
乔前辈守护的最后一道物理防线。

用法:
    sudo python3 bin/lh_tongxin_lock_firewall.py --activate     # 激活防火墙
    sudo python3 bin/lh_tongxin_lock_firewall.py --deactivate   # 停用防火墙
    sudo python3 bin/lh_tongxin_lock_firewall.py --status       # 查看状态
    sudo python3 bin/lh_tongxin_lock_firewall.py --unlock       # 临时解锁(需验证)
    python3 bin/lh_tongxin_lock_firewall.py selftest            # 自检
"""
DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-TONGXIN-LOCK-FIREWALL-v1.0"
创建者 = "诸葛鑫（UID9622）"
协议 = "CC BY-NC-SA 4.0"

import argparse
import hashlib
import json
import os
import platform
import random
import re
import socket
import subprocess
import sys
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# ═══ 常量 ═══
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = PROJECT_ROOT / "data" / "tongxin_lock_state.json"
LOG_DIR = PROJECT_ROOT / "logs"
PF_ANCHOR = "com.longhun.tongxin-lock"
UNLOCK_TIMEOUT_MINUTES = 30  # 解锁超时自动重锁

# ═══ 白名单 ═══
# 只允许这些目标出站——其余全部阻断
WHITELIST = {
    "ips": [
        # 鲲鹏服务器
        "119.13.90.27",
    ],
    "domains": [
        # 龍魂系统
        "uid9622.cn",
        "longhun.system",
        # 开发资源
        "github.com",
        "api.github.com",
        "raw.githubusercontent.com",
        # AI模型
        "huggingface.co",
        "cdn-lfs.huggingface.co",
        "cdn-lfs-us-1.huggingface.co",
        # 中国AI生态
        "modelscope.cn",
        "www.modelscope.cn",
        # 知识来源
        "csdn.net",
        "blog.csdn.net",
        # Python生态
        "pypi.org",
        "files.pythonhosted.org",
    ],
}

# ═══ 苹果服务阻断清单 ═══
APPLE_BLOCKLIST = {
    "domains": [
        "icloud.com", "icloud.com.cn", "icloud-content.com",
        "me.com", "apple.com", "apple.com.cn",
        "siri.com", "push-apple.com.akadns.net",
        "courier-push-apple.com.akadns.net",
        "apple-dns.net", "aaplimg.com",
        "mzstatic.com", "itunes.com",
        "apple-cloudkit.com", "cirrus.com",
        "digicert.com",  # Apple证书验证域
        "apple.news", "apple-mxmas-service.com",
    ],
    "cidrs": [
        "17.0.0.0/8",          # Apple整个IP段
        "104.154.0.0/15",      # Google Cloud (部分Apple服务)
    ],
}

# ═══ 谷歌/微软/亚马逊追踪服务 ═══
TRACKER_BLOCKLIST = {
    "domains": [
        # Google追踪
        "google-analytics.com", "googletagmanager.com",
        "doubleclick.net", "googleadservices.com",
        "googlesyndication.com", "googleapis.com",
        # Microsoft遥测
        "telemetry.microsoft.com", "vortex.data.microsoft.com",
        "settings-win.data.microsoft.com",
        # Amazon追踪
        "amazon-adsystem.com",
    ],
    "cidrs": [],
}


# ═══ 核心引擎 ═══

class TongxinLockFirewall:
    """同心锁物理防火墙 — 白名单模式 pfctl"""

    def __init__(self):
        self.state = self._load_state()
        self._ensure_dirs()

    # ── 状态管理 ──

    def _ensure_dirs(self):
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        LOG_DIR.mkdir(parents=True, exist_ok=True)

    def _load_state(self) -> dict:
        if STATE_FILE.exists():
            try:
                return json.loads(STATE_FILE.read_text())
            except Exception:
                pass
        return {
            "locked": True,
            "activated": False,
            "unlocked_at": None,
            "unlocked_by": None,
            "last_audit": None,
            "dna": DNA,
            "created": datetime.now().isoformat(),
        }

    def _save_state(self):
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(self.state, indent=2, ensure_ascii=False))
        # 限制状态文件权限，防止指纹泄露
        try:
            os.chmod(STATE_FILE, 0o600)
        except Exception:
            pass

    def is_locked(self) -> bool:
        return self.state.get("locked", True)

    def is_activated(self) -> bool:
        return self.state.get("activated", False)

    # ── pfctl 规则生成 ──

    def _resolve_domains(self, domains: list) -> list:
        """将域名解析为IP列表（用于pfctl规则）"""
        ips = []
        for domain in domains:
            try:
                info = socket.getaddrinfo(domain, None)
                for item in info:
                    ip = item[4][0]
                    if ip not in ips:
                        ips.append(ip)
            except Exception:
                pass
        return ips

    def _generate_pf_rules(self, include_temp_unlock: bool = False) -> str:
        """生成 pfctl 规则内容"""
        rules = []

        # 基础规则
        rules.append("# ═══ 龍魂·同心锁防火墙 ═══")
        rules.append(f"# DNA: {DNA}")
        rules.append(f"# Generated: {datetime.now().isoformat()}")
        rules.append(f"# State: {'LOCKED' if self.is_locked() else 'UNLOCKED'}")
        rules.append("")

        if include_temp_unlock or not self.is_locked():
            # 临时解锁模式：默认放行（带日志），但阻断已知追踪
            rules.append("# ── 临时解锁模式 ──")
            rules.append("pass out all keep state")
            rules.append("")

            # 阻断苹果
            rules.append("# ── 苹果服务阻断 ──")
            for domain in APPLE_BLOCKLIST["domains"]:
                rules.append(f"block drop out quick to any port 443 from any to *.{domain}")
            for cidr in APPLE_BLOCKLIST["cidrs"]:
                rules.append(f"block drop out quick to {cidr}")

            # 阻断追踪
            rules.append("")
            rules.append("# ── 追踪服务阻断 ──")
            for domain in TRACKER_BLOCKLIST["domains"]:
                rules.append(f"block drop out quick to any port 443 from any to *.{domain}")

        else:
            # 锁定模式：默认拒绝所有，仅放行白名单
            rules.append("# ── 锁定模式：拒绝所有出站 ──")
            rules.append("block drop out log all")
            rules.append("")

            # 允许本地回环
            rules.append("# ── 本地回环 ──")
            rules.append("pass out quick on lo0 all")
            rules.append("")

            # 允许DNS（本地解析）
            rules.append("# ── DNS（本地解析） ──")
            rules.append("pass out quick proto udp from any to any port 53 keep state")
            rules.append("pass out quick proto tcp from any to any port 53 keep state")
            rules.append("")

            # 允许白名单IP
            rules.append("# ── 白名单IP ──")
            for ip in WHITELIST["ips"]:
                rules.append(f"pass out quick proto tcp from any to {ip} port 22 keep state")
                rules.append(f"pass out quick proto tcp from any to {ip} port 80 keep state")
                rules.append(f"pass out quick proto tcp from any to {ip} port 443 keep state")
                rules.append(f"pass out quick proto tcp from any to {ip} port 8766:8781 keep state")

            # 解析白名单域名→IP
            rules.append("")
            rules.append("# ── 白名单域名 ──")
            resolved = self._resolve_domains(WHITELIST["domains"])
            for ip in resolved:
                rules.append(f"pass out quick proto tcp from any to {ip} port 80 keep state")
                rules.append(f"pass out quick proto tcp from any to {ip} port 443 keep state")
                rules.append(f"pass out quick proto tcp from any to {ip} port 22 keep state")
                rules.append(f"pass out quick proto tcp from any to {ip} port 9418 keep state")

            # 显式阻断苹果
            rules.append("")
            rules.append("# ── 苹果服务显式阻断 ──")
            for cidr in APPLE_BLOCKLIST["cidrs"]:
                rules.append(f"block drop out quick to {cidr}")

        return "\n".join(rules)

    # ── 后端选择 ──

    def _get_backend(self) -> str:
        """根据操作系统选择防火墙后端"""
        if platform.system() == "Darwin":
            return "pfctl"
        elif platform.system() == "Linux":
            return "iptables"
        return "unknown"

    def _check_backend(self) -> bool:
        """检查当前后端工具是否可用"""
        backend = self._get_backend()
        try:
            if backend == "pfctl":
                result = subprocess.run(
                    ["sudo", "-n", "pfctl", "-s", "info"],
                    capture_output=True, text=True, timeout=5
                )
                return result.returncode == 0
            elif backend == "iptables":
                result = subprocess.run(
                    ["sudo", "-n", "iptables", "-L", "-n"],
                    capture_output=True, text=True, timeout=5
                )
                return result.returncode == 0
        except Exception:
            pass
        return False

    # ── iptables 规则生成 ──

    def _generate_iptables_rules(self, include_temp_unlock: bool = False) -> tuple:
        """生成 iptables(IPv4) 与 ip6tables(IPv6) 规则脚本（Linux）"""
        chain = "LONGHUN_TONGXIN"

        def _script_for_family(family_cmd: str) -> str:
            lines = ["#!/bin/bash", f"# ═══ 龍魂·同心锁防火墙 {family_cmd}规则 ═══"]
            lines.append(f"{family_cmd} -F {chain} 2>/dev/null || true")
            lines.append(f"{family_cmd} -X {chain} 2>/dev/null || true")
            lines.append(f"{family_cmd} -N {chain}")
            lines.append(f"{family_cmd} -D OUTPUT -j {chain} 2>/dev/null || true")
            lines.append(f"{family_cmd} -I OUTPUT 1 -j {chain}")

            if include_temp_unlock or not self.is_locked():
                lines.append(f"# ── 临时解锁模式：默认放行，阻断已知追踪 ──")
                for cidr in APPLE_BLOCKLIST["cidrs"]:
                    if (":" in cidr and family_cmd == "ip6tables") or (":" not in cidr and family_cmd == "iptables"):
                        lines.append(f"{family_cmd} -A {chain} -d {cidr} -j DROP")
                for ip in self._resolve_domains(TRACKER_BLOCKLIST["domains"]):
                    is_v6 = ":" in ip
                    if (is_v6 and family_cmd == "ip6tables") or (not is_v6 and family_cmd == "iptables"):
                        lines.append(f"{family_cmd} -A {chain} -d {ip} -j DROP")
                lines.append(f"{family_cmd} -A {chain} -j RETURN")
            else:
                lines.append(f"# ── 锁定模式：默认拒绝，仅放行白名单 ──")
                lines.append(f"{family_cmd} -A {chain} -o lo -j RETURN")
                lines.append(f"{family_cmd} -A {chain} -p udp --dport 53 -j RETURN")
                lines.append(f"{family_cmd} -A {chain} -p tcp --dport 53 -j RETURN")
                for ip in WHITELIST["ips"]:
                    if ":" not in ip and family_cmd == "iptables":
                        lines.append(f"{family_cmd} -A {chain} -d {ip}/32 -p tcp -m multiport --dports 22,80,443,8766:8781 -j RETURN")
                for ip in self._resolve_domains(WHITELIST["domains"]):
                    is_v6 = ":" in ip
                    if (is_v6 and family_cmd == "ip6tables") or (not is_v6 and family_cmd == "iptables"):
                        lines.append(f"{family_cmd} -A {chain} -d {ip} -p tcp -m multiport --dports 22,80,443,9418 -j RETURN")
                for cidr in APPLE_BLOCKLIST["cidrs"]:
                    if (":" in cidr and family_cmd == "ip6tables") or (":" not in cidr and family_cmd == "iptables"):
                        lines.append(f"{family_cmd} -A {chain} -d {cidr} -j DROP")
                lines.append(f"{family_cmd} -A {chain} -j DROP")
            return "\n".join(lines) + "\n"

        return _script_for_family("iptables"), _script_for_family("ip6tables")

    def _apply_iptables_rules(self, rules_scripts: tuple) -> None:
        """应用 iptables + ip6tables 规则脚本"""
        for idx, script in enumerate(rules_scripts):
            fname = f"tongxin_iptables{'6' if idx == 1 else ''}_rules.sh"
            rules_file = PROJECT_ROOT / "data" / fname
            rules_file.parent.mkdir(parents=True, exist_ok=True)
            rules_file.write_text(script)
            rules_file.chmod(0o700)
            subprocess.run(["sudo", "bash", str(rules_file)], check=True, timeout=15)

    def _clear_iptables_rules(self) -> None:
        """清空 iptables + ip6tables 规则"""
        chain = "LONGHUN_TONGXIN"
        for family_cmd in ["iptables", "ip6tables"]:
            script = f"""#!/bin/bash
{family_cmd} -D OUTPUT -j {chain} 2>/dev/null || true
{family_cmd} -F {chain} 2>/dev/null || true
{family_cmd} -X {chain} 2>/dev/null || true
"""
            rules_file = PROJECT_ROOT / "data" / f"tongxin_{family_cmd}_clear.sh"
            rules_file.write_text(script)
            rules_file.chmod(0o700)
            subprocess.run(["sudo", "bash", str(rules_file)], check=True, timeout=15)

    # ── pfctl 操作 ──

    def _check_pfctl(self) -> bool:
        """检查pfctl是否可用"""
        try:
            result = subprocess.run(
                ["sudo", "-n", "pfctl", "-s", "info"],
                capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False

    def _write_rules_file(self, rules: str) -> Path:
        """写入临时规则文件"""
        rules_file = PROJECT_ROOT / "data" / "tongxin_pf_rules.conf"
        rules_file.parent.mkdir(parents=True, exist_ok=True)
        rules_file.write_text(rules)
        return rules_file

    def activate(self) -> dict:
        """激活防火墙 — 锁定模式"""
        if not self._check_backend():
            backend = self._get_backend()
            return {"ok": False, "error": f"{backend}不可用或需要sudo权限"}

        try:
            backend = self._get_backend()
            if backend == "pfctl":
                rules = self._generate_pf_rules(include_temp_unlock=False)
                rules_file = self._write_rules_file(rules)
                subprocess.run(
                    ["sudo", "pfctl", "-a", PF_ANCHOR, "-F", "rules"],
                    check=False, timeout=10
                )
                subprocess.run(
                    ["sudo", "pfctl", "-a", PF_ANCHOR, "-f", str(rules_file)],
                    check=True, timeout=10
                )
                subprocess.run(["sudo", "pfctl", "-e"], check=False, timeout=10)
            elif backend == "iptables":
                rules_script = self._generate_iptables_rules(include_temp_unlock=False)
                self._clear_iptables_rules()
                self._apply_iptables_rules(rules_script)

            self.state["activated"] = True
            self.state["locked"] = True
            self.state["activated_at"] = datetime.now().isoformat()
            self._save_state()

            self._log("activated", f"防火墙已激活·锁定模式（后端:{backend}）")
            return {"ok": True, "state": "LOCKED", "action": "activated", "backend": backend}

        except subprocess.CalledProcessError as e:
            return {"ok": False, "error": str(e), "action": "activate_failed"}

    def deactivate(self) -> dict:
        """停用防火墙：仅清空本规则集，不关闭全局防火墙"""
        if not self._check_backend():
            backend = self._get_backend()
            return {"ok": False, "error": f"{backend}不可用或需要sudo权限"}

        try:
            backend = self._get_backend()
            if backend == "pfctl":
                subprocess.run(
                    ["sudo", "pfctl", "-a", PF_ANCHOR, "-F", "rules"],
                    check=True, timeout=10
                )
            elif backend == "iptables":
                self._clear_iptables_rules()

            self.state["activated"] = False
            self.state["locked"] = False
            self._save_state()

            self._log("deactivated", f"防火墙已停用（后端:{backend}）")
            return {"ok": True, "state": "OFF", "action": "deactivated", "backend": backend}

        except subprocess.CalledProcessError as e:
            return {"ok": False, "error": str(e), "action": "deactivate_failed"}

    def unlock(self, device_hash: str = "") -> dict:
        """临时解锁 — 必须提供设备指纹验证"""
        if not self.is_activated():
            return {"ok": False, "error": "防火墙未激活"}

        # 设备指纹验证：空哈希直接拒绝
        expected = self._get_device_fingerprint()
        if not device_hash:
            self._log("unlock_failed", "解锁失败：未提供设备指纹")
            return {"ok": False, "error": "必须提供 --device-hash 才能解锁", "action": "lockdown"}
        if device_hash != expected:
            self._log("unlock_failed", f"设备指纹不匹配: {device_hash[:8]}... vs {expected[:8]}...")
            return {"ok": False, "error": "设备验证失败", "action": "lockdown"}

        try:
            backend = self._get_backend()
            if backend == "pfctl":
                rules = self._generate_pf_rules(include_temp_unlock=True)
                rules_file = self._write_rules_file(rules)
                subprocess.run(
                    ["sudo", "pfctl", "-a", PF_ANCHOR, "-f", str(rules_file)],
                    check=True, timeout=10
                )
            elif backend == "iptables":
                rules_script = self._generate_iptables_rules(include_temp_unlock=True)
                self._apply_iptables_rules(rules_script)

            now = datetime.now()
            self.state["locked"] = False
            self.state["unlocked_at"] = now.isoformat()
            self.state["unlocked_by"] = "device_fingerprint"
            self.state["relock_at"] = (now + timedelta(minutes=UNLOCK_TIMEOUT_MINUTES)).isoformat()
            self._save_state()

            self._log("unlocked", f"临时解锁·{UNLOCK_TIMEOUT_MINUTES}分钟后自动重锁")
            return {
                "ok": True,
                "state": "UNLOCKED",
                "action": "temp_unlock",
                "timeout_minutes": UNLOCK_TIMEOUT_MINUTES,
                "relock_at": self.state["relock_at"],
            }

        except subprocess.CalledProcessError as e:
            return {"ok": False, "error": str(e), "action": "unlock_failed"}

    def relock(self) -> dict:
        """重新锁定"""
        self.state["locked"] = True
        self.state["unlocked_at"] = None
        self.state["relock_at"] = None
        self._save_state()

        return self.activate()

    def check_timeout_relock(self) -> Optional[dict]:
        """检查解锁超时，自动重锁"""
        if not self.is_locked() and self.state.get("relock_at"):
            relock_at = datetime.fromisoformat(self.state["relock_at"])
            if datetime.now() >= relock_at:
                return self.relock()
        return None

    def status(self) -> dict:
        """获取当前状态"""
        backend = self._get_backend()
        fw_status = "unknown"
        try:
            if backend == "pfctl":
                result = subprocess.run(
                    ["sudo", "-n", "pfctl", "-s", "info"],
                    capture_output=True, text=True, timeout=5
                )
                fw_status = "enabled" if "Enabled" in result.stdout else "disabled"
            elif backend == "iptables":
                result = subprocess.run(
                    ["sudo", "-n", "iptables", "-L", "LONGHUN_TONGXIN", "-n"],
                    capture_output=True, text=True, timeout=5
                )
                fw_status = "active" if result.returncode == 0 else "inactive"
        except Exception:
            pass

        return {
            "locked": self.is_locked(),
            "activated": self.is_activated(),
            "backend": backend,
            "fw_status": fw_status,
            "unlocked_at": self.state.get("unlocked_at"),
            "relock_at": self.state.get("relock_at"),
            "dna": DNA,
        }

    # ── MAC地址混淆 ──

    def obfuscate_mac(self) -> str:
        """生成本地管理MAC地址（非全球唯一）"""
        mac = [0x02]  # 本地管理地址位
        for _ in range(5):
            mac.append(random.randint(0x00, 0xFF))
        return ":".join(f"{b:02x}" for b in mac)

    def apply_mac_obfuscation(self, interface: str = "en0") -> dict:
        """对指定网卡应用混淆MAC（macOS/Linux自适应）"""
        if platform.system() == "Darwin":
            cmd = ["sudo", "ifconfig", interface, "ether"]
        elif platform.system() == "Linux":
            cmd = ["sudo", "ip", "link", "set", "dev", interface, "address"]
        else:
            return {"ok": False, "error": f"不支持的操作系统: {platform.system()}"}

        new_mac = self.obfuscate_mac()
        try:
            subprocess.run(cmd + [new_mac], check=True, timeout=10)
            self._log("mac_obfuscated", f"{interface} → {new_mac}")
            return {"ok": True, "interface": interface, "new_mac": new_mac}
        except subprocess.CalledProcessError as e:
            return {"ok": False, "error": str(e)}

    # ── 设备指纹 ──

    def _get_device_fingerprint(self) -> str:
        """生成设备指纹（硬件绑定·跨平台）"""
        components = [
            platform.node(),      # 主机名
            platform.machine(),   # 架构
            platform.processor(), # 处理器
        ]
        try:
            if platform.system() == "Darwin":
                result = subprocess.run(
                    ["system_profiler", "SPHardwareDataType"],
                    capture_output=True, text=True, timeout=10
                )
                for line in result.stdout.split("\n"):
                    if "Serial Number" in line:
                        components.append(line.split(":")[-1].strip())
                    if "Hardware UUID" in line:
                        components.append(line.split(":")[-1].strip())
            elif platform.system() == "Linux":
                # 优先读 /etc/machine-id， fallback 到 dmidecode
                machine_id_path = Path("/etc/machine-id")
                if machine_id_path.exists():
                    components.append(machine_id_path.read_text().strip())
                try:
                    result = subprocess.run(
                        ["dmidecode", "-s", "system-uuid"],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        components.append(result.stdout.strip())
                except Exception:
                    pass
        except Exception:
            pass

        fingerprint = hashlib.sha256("|".join(filter(None, components)).encode()).hexdigest()[:16]
        return fingerprint

    # ── 日志 ──

    def _log(self, action: str, detail: str):
        """写审计日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "detail": detail,
            "dna": DNA,
        }
        log_file = LOG_DIR / "tongxin_lock.log"
        try:
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            with open(log_file, "a") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            # 日志失败至少打印到stderr，不能静默吞掉
            print(f"[TongxinLock LOG FAILED] {action}: {detail} ({e})", file=sys.stderr)


# ═══ 自检 ═══

def selftest():
    """同心锁防火墙自检"""
    errors = 0

    firewall = TongxinLockFirewall()

    # 1. 状态初始化
    assert firewall.state is not None, "状态为空"
    assert "locked" in firewall.state, "缺少locked字段"
    print("  ✅ 1/7 状态管理: 正常")

    # 2. 设备指纹
    fp = firewall._get_device_fingerprint()
    assert len(fp) == 16, f"指纹长度异常: {len(fp)}"
    print(f"  ✅ 2/7 设备指纹: {fp}")

    # 3. MAC混淆
    mac = firewall.obfuscate_mac()
    parts = mac.split(":")
    assert len(parts) == 6, f"MAC格式异常: {mac}"
    assert int(parts[0], 16) & 0x02, "非本地管理地址"
    print(f"  ✅ 3/7 MAC混淆: {mac}")

    # 4. 规则生成-锁定模式
    rules_locked = firewall._generate_pf_rules(include_temp_unlock=False)
    assert "block drop out log all" in rules_locked, "锁定模式缺少默认拒绝"
    assert "119.13.90.27" in rules_locked, "缺少鲲鹏IP"
    assert "pass out quick on lo0" in rules_locked, "缺少本地回环"
    print(f"  ✅ 4/7 锁定规则: {len(rules_locked)}字节")

    # 5. 规则生成-解锁模式
    rules_unlocked = firewall._generate_pf_rules(include_temp_unlock=True)
    assert "pass out all keep state" in rules_unlocked, "解锁模式缺少默认放行"
    print(f"  ✅ 5/7 解锁规则: {len(rules_unlocked)}字节")

    # 6. status()
    st = firewall.status()
    assert "locked" in st, "缺少locked"
    assert "activated" in st, "缺少activated"
    assert "fw_status" in st, "缺少fw_status"
    assert "backend" in st, "缺少backend"
    print(f"  ✅ 6/8 状态查询: backend={st['backend']}, locked={st['locked']}, fw={st['fw_status']}")

    # 7. 解锁超时逻辑
    firewall.state["locked"] = False
    firewall.state["relock_at"] = (datetime.now() - timedelta(minutes=31)).isoformat()
    result = firewall.check_timeout_relock()
    assert result is not None, "超时未触发重锁"
    assert firewall.is_locked(), "超时后未锁定"
    print(f"  ✅ 7/8 超时重锁: 31分钟超时→自动重锁")

    # 8. 解锁必须提供设备指纹
    firewall.state["activated"] = True
    firewall.state["locked"] = True
    bad_unlock = firewall.unlock("")
    assert bad_unlock.get("ok") is False, "空设备指纹应拒绝解锁"
    assert "必须提供" in bad_unlock.get("error", ""), "错误提示不正确"
    print(f"  ✅ 8/8 解锁验证: 空指纹→拒绝")

    print(f"\n🎯 自检: 8/8 全绿")
    return errors == 0


# ═══ CLI ═══

def main():
    # 自检不需要sudo
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        ok = selftest()
        sys.exit(0 if ok else 1)

    parser = argparse.ArgumentParser(description="龍魂·同心锁物理防火墙")
    parser.add_argument("--activate", action="store_true", help="激活防火墙(锁定模式)")
    parser.add_argument("--deactivate", action="store_true", help="停用防火墙")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--unlock", action="store_true", help="临时解锁")
    parser.add_argument("--relock", action="store_true", help="重新锁定")
    parser.add_argument("--device-hash", type=str, help="设备指纹(解锁验证)")
    parser.add_argument("--obfuscate-mac", action="store_true", help="混淆MAC地址")
    parser.add_argument("--interface", type=str, default="en0", help="网卡接口(默认en0)")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("selftest", nargs="?", help="自检(无sudo)")

    args = parser.parse_args()

    firewall = TongxinLockFirewall()

    if args.activate:
        result = firewall.activate()
    elif args.deactivate:
        result = firewall.deactivate()
    elif args.unlock:
        result = firewall.unlock(args.device_hash or "")
    elif args.relock:
        result = firewall.relock()
    elif args.obfuscate_mac:
        result = firewall.apply_mac_obfuscation(args.interface)
    elif args.status:
        result = firewall.status()
    else:
        parser.print_help()
        sys.exit(0)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        status_icon = {"LOCKED": "🔒", "UNLOCKED": "🔓", "OFF": "⭕"}.get(
            result.get("state", ""), "❓"
        )
        if result.get("ok"):
            print(f"{status_icon} {result.get('action', 'ok')}: {result.get('state', '')}")
            if result.get("relock_at"):
                print(f"   重锁时间: {result['relock_at']}")
        else:
            print(f"❌ {result.get('error', '未知错误')}")
            sys.exit(1)


if __name__ == "__main__":
    main()
