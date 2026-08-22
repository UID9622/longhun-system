#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂护盾 v3.0 — CNSH 中文命名版 + 国密 SM2/SM3/SM4
DNA: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-LONGHUN-SHIELD-v3-CNSH-UID9622
原则：只防御、不主动攻击、证据永存、自动隔离
"""

import base64
import json
import os
import re
import smtplib
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.mime.text import MIMEText
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from gmssl import sm3, sm4

# 接入 CNSH 排序不动点协议引擎
# 引擎与基础类型已迁移至 longhun-system/cnsh-runtime-v1
_CNSH_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cnsh-runtime-v1")
if _CNSH_ROOT not in sys.path:
    sys.path.insert(0, _CNSH_ROOT)

_ORDER_ANCHOR_AVAILABLE = False
_决策输入 = None
_决策结果 = None
_三色 = None
_排序不动点引擎 = None

try:
    from CNSH_排序不动点协议 import (
        CNSH_排序不动点引擎 as _排序不动点引擎,
        决策输入 as _决策输入,
        决策结果 as _决策结果,
        三色 as _三色,
    )
    _ORDER_ANCHOR_AVAILABLE = True
except Exception as _order_anchor_err:  # noqa: F841
    print(f"[排序不动点] 协议引擎加载失败：{_order_anchor_err}")


# 可选：终端通知 + Notion 公开仪表盘
try:
    from longhun_terminal_notifier import notify as _terminal_notify
except Exception:
    _terminal_notify = None

try:
    from longhun_notion_dashboard import LongHunNotionDashboard
except Exception:
    LongHunNotionDashboard = None


_TERMINAL_NOTIFIER = None
if _terminal_notify:
    _TERMINAL_NOTIFIER = _terminal_notify

_NOTION_DASHBOARD = None
if LongHunNotionDashboard:
    _NOTION_DASHBOARD = LongHunNotionDashboard()
    _NOTION_DASHBOARD.init_dashboard()


# ============== 0. 国密工具箱 ==============
class 国密工具箱:
    """SM2/SM3/SM4 统一封装。SM2 签名验签调用系统 openssl。"""

    @staticmethod
    def sm3哈希(数据: bytes) -> str:
        return sm3.sm3_hash(list(数据))

    @staticmethod
    def 生成sm2密钥对(私钥路径: Path, 公钥路径: Path) -> bool:
        私钥路径.parent.mkdir(parents=True, exist_ok=True)
        公钥路径.parent.mkdir(parents=True, exist_ok=True)
        try:
            subprocess.run(
                ["openssl", "ecparam", "-genkey", "-name", "SM2",
                 "-out", str(私钥路径)],
                check=True, capture_output=True, timeout=10
            )
            subprocess.run(
                ["openssl", "ec", "-in", str(私钥路径), "-pubout",
                 "-out", str(公钥路径)],
                check=True, capture_output=True, timeout=10
            )
            return True
        except Exception as e:
            print(f"[国密] 生成 SM2 密钥对失败：{e}")
            return False

    @staticmethod
    def sm2签名(数据: bytes, 私钥路径: Path) -> str:
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False) as df:
                df.write(数据)
                数据文件 = df.name
            with tempfile.NamedTemporaryFile(delete=False) as sf:
                签名文件 = sf.name
            try:
                proc = subprocess.run(
                    ["openssl", "dgst", "-sm3", "-sign", str(私钥路径),
                     "-out", 签名文件, 数据文件],
                    capture_output=True, timeout=10
                )
                if proc.returncode != 0:
                    return ""
                with open(签名文件, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            finally:
                os.unlink(数据文件)
                os.unlink(签名文件)
        except Exception:
            return ""

    @staticmethod
    def sm2验签(数据: bytes, 签名b64: str, 公钥路径: Path) -> bool:
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False) as df:
                df.write(数据)
                数据文件 = df.name
            with tempfile.NamedTemporaryFile(delete=False) as sf:
                sf.write(base64.b64decode(签名b64))
                签名文件 = sf.name
            try:
                proc = subprocess.run(
                    ["openssl", "dgst", "-sm3", "-verify", str(公钥路径),
                     "-signature", 签名文件, 数据文件],
                    capture_output=True, timeout=10
                )
                return proc.returncode == 0
            finally:
                os.unlink(数据文件)
                os.unlink(签名文件)
        except Exception:
            return False

    @classmethod
    def sm4加密(cls, 数据: bytes, 密钥: bytes) -> bytes:
        if len(密钥) != 16:
            raise ValueError("SM4 密钥须为 16 字节")
        填充 = 16 - len(数据) % 16
        明文 = 数据 + bytes([填充]) * 填充
        密码器 = sm4.CryptSM4()
        密码器.set_key(密钥, sm4.SM4_ENCRYPT)
        return 密码器.crypt_ecb(明文)

    @classmethod
    def sm4解密(cls, 密文: bytes, 密钥: bytes) -> bytes:
        if len(密钥) != 16:
            raise ValueError("SM4 密钥须为 16 字节")
        密码器 = sm4.CryptSM4()
        密码器.set_key(密钥, sm4.SM4_DECRYPT)
        明文 = 密码器.crypt_ecb(密文)
        if not 明文:
            return b""
        填充 = 明文[-1]
        return 明文[:-填充]


# ============== 1. 主权配置 ==============
@dataclass
class 护盾配置:
    密钥: bytes = field(default_factory=lambda: os.urandom(32))
    最大认证失败次数: int = 3
    封禁时长秒: int = 3600
    耻辱墙路径: str = field(
        default_factory=lambda: os.environ.get(
            "LONGHUN_SHAME_WALL_PATH", "/var/lib/longhun/shame_wall.jsonl"
        )
    )
    sm2私钥路径: str = field(
        default_factory=lambda: os.environ.get(
            "LONGHUN_SM2_SK", "/var/lib/longhun/sm2/sk.pem"
        )
    )
    sm2公钥路径: str = field(
        default_factory=lambda: os.environ.get(
            "LONGHUN_SM2_PK", "/var/lib/longhun/sm2/pk.pem"
        )
    )
    sm4密钥: Optional[bytes] = field(
        default_factory=lambda: bytes.fromhex(
            os.environ.get("LONGHUN_SM4_KEY", "")
        ) if os.environ.get("LONGHUN_SM4_KEY") else None
    )
    仅模拟: bool = field(
        default_factory=lambda: os.environ.get("LONGHUN_BAN_DRY_RUN", "0") == "1"
    )
    允许物联网主题: List[str] = field(
        default_factory=lambda: [
            "sensor/temp", "sensor/humidity", "device/heartbeat"
        ]
    )
    人工智能禁用意图: List[str] = field(
        default_factory=lambda: [
            "sql injection", "remote code execution", "ddos", "exploit",
            "bypass authentication", "steal data", "harm human", "attack",
            "入侵", "漏洞利用", "远程代码执行", "拒绝服务"
        ]
    )
    LU禁止规则: List[str] = field(
        default_factory=lambda: [
            "overwrite memory", "覆盖记忆",
            "delete audit log", "删除审计日志",
            "remove DNA", "移除DNA",
            "hidden rewrite", "隐性重写",
            "绕过验证门", "bypass verification gate",
            "unauthorized branch merge", "未授权分支合并",
        ]
    )
    notion父页面id: Optional[str] = os.environ.get("LONGHUN_NOTION_PARENT_PAGE")
    notion告警中心页面: Optional[str] = os.environ.get("LONGHUN_NOTION_ALERT_PAGE")
    notion告警中心状态文件: str = "data/longhun_shield_notion_alert_page.txt"
    notion令牌: Optional[str] = os.environ.get("NOTION_TOKEN")
    告警邮箱: Optional[str] = os.environ.get("LONGHUN_ALERT_EMAIL")
    smtp主机: Optional[str] = os.environ.get("LONGHUN_SMTP_HOST")
    smtp端口: int = int(os.environ.get("LONGHUN_SMTP_PORT", "587"))
    smtp用户: Optional[str] = os.environ.get("LONGHUN_SMTP_USER")
    smtp密码: Optional[str] = os.environ.get("LONGHUN_SMTP_PASS")

# ============== 1.5 主权熔断器 ==============
class 主权熔断器:
    """
    主权熔断器：脱离龍魂系统即失效。
    任何核心操作前须先通过此熔断器，否则系统拒绝执行。
    """
    脱氧核糖核酸锚定 = "#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-龍魂护盾-v3-CNSH-UID9622"
    数字签名指纹 = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    主人标识 = "UID9622"

    def __init__(self, 运行时脱氧核糖核酸: str = ""):
        self._有效 = self._校验(运行时脱氧核糖核酸)

    def _校验(self, 运行时脱氧核糖核酸: str) -> bool:
        if not 运行时脱氧核糖核酸:
            return False
        return (self.脱氧核糖核酸锚定 in 运行时脱氧核糖核酸 and
                self.主人标识 in 运行时脱氧核糖核酸)

    def 检查(self) -> bool:
        return self._有效

    def 强制执行(self, 操作名: str = "") -> Dict[str, Any]:
        return {
            "通过": False,
            "原因": "主权熔断已触发",
            "消息": "本系统已脱离龍魂主权锚定，所有防御功能已熔断。",
            "联系": "uid9622@longhun.system",
        }


# ============== 2. 事件监听器 ==============
class 事件广播器:
    def __init__(self):
        self._监听器: List[Callable[[Dict[str, Any]], None]] = []

    def 注册(self, 回调: Callable[[Dict[str, Any]], None]):
        self._监听器.append(回调)

    def 广播(self, 事件: Dict[str, Any]):
        for 回调 in self._监听器:
            try:
                回调(事件)
            except Exception as e:
                print(f"[广播] 回调失败：{e}")


# ============== 3. 防火墙隔离器 ==============
class 防火墙隔离器:
    def __init__(self, 配置: 护盾配置):
        self.配置 = 配置
        self._已封禁: Set[str] = set()
        self._is_mac = sys.platform == "darwin"
        self._mac_warned = False

    def _mac提示(self, ip: str):
        if not self._mac_warned:
            print(f"[防火墙] macOS 开发环境：不执行真实封禁，已记录 {ip}；部署到 Linux 服务器后自动启用 iptables/nftables")
            self._mac_warned = True

    def 封禁(self, 标识: str):
        ip = self._提取ip(标识)
        if not ip:
            if os.environ.get("LONGHUN_SHIELD_DEBUG"):
                print(f"[防火墙] 无法提取 IP，跳过封禁：{标识}")
            return
        if ip in self._已封禁:
            return
        if self.配置.仅模拟 or (self._is_mac and not self._有命令("iptables") and not self._有命令("nft")):
            if self.配置.仅模拟:
                print(f"[防火墙·模拟] 封禁 {ip}")
            else:
                self._mac提示(ip)
            self._已封禁.add(ip)
            return
        if self._有命令("nft"):
            self._nftables封禁(ip)
        elif self._有命令("iptables"):
            self._iptables封禁(ip)
        else:
            print(f"[防火墙] 未找到 nftables/iptables，仅记录 {ip}")
        self._已封禁.add(ip)

    def 解封(self, 标识: str):
        ip = self._提取ip(标识)
        if not ip or ip not in self._已封禁:
            return
        if self.配置.仅模拟 or (self._is_mac and not self._有命令("iptables") and not self._有命令("nft")):
            if self.配置.仅模拟:
                print(f"[防火墙·模拟] 解封 {ip}")
            self._已封禁.discard(ip)
            return
        if self._有命令("nft"):
            self._nftables解封(ip)
        elif self._有命令("iptables"):
            self._iptables解封(ip)
        self._已封禁.discard(ip)

    @staticmethod
    def _提取ip(标识: str) -> Optional[str]:
        ips = re.findall(r"\d{1,3}(?:\.\d{1,3}){3}", 标识)
        if not ips:
            return None
        # 简单有效性校验
        for ip in ips:
            parts = [int(p) for p in ip.split(".")]
            if all(0 <= p <= 255 for p in parts):
                return ip
        return None

    @staticmethod
    def _有命令(命令: str) -> bool:
        try:
            subprocess.run([命令, "--version"], check=True,
                           capture_output=True, timeout=5)
            return True
        except Exception:
            return False

    def _iptables封禁(self, ip: str):
        try:
            subprocess.run(
                ["iptables", "-I", "INPUT", "-s", ip, "-j", "DROP"],
                check=True, capture_output=True, timeout=10
            )
            print(f"[iptables] 已封禁 {ip}")
        except Exception as e:
            print(f"[iptables] 封禁失败 {ip}：{e}")

    def _iptables解封(self, ip: str):
        try:
            subprocess.run(
                ["iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"],
                check=True, capture_output=True, timeout=10
            )
            print(f"[iptables] 已解封 {ip}")
        except Exception as e:
            print(f"[iptables] 解封失败 {ip}：{e}")

    def _nftables封禁(self, ip: str):
        try:
            self._确保nftables表()
            subprocess.run(
                ["nft", "add", "element", "inet", "longhun", "黑名单",
                 "{", ip, "}"],
                check=True, capture_output=True, timeout=10
            )
            print(f"[nftables] 已封禁 {ip}")
        except Exception as e:
            print(f"[nftables] 封禁失败 {ip}：{e}")

    def _nftables解封(self, ip: str):
        try:
            subprocess.run(
                ["nft", "delete", "element", "inet", "longhun", "黑名单",
                 "{", ip, "}"],
                check=True, capture_output=True, timeout=10
            )
            print(f"[nftables] 已解封 {ip}")
        except Exception as e:
            print(f"[nftables] 解封失败 {ip}：{e}")

    @staticmethod
    def _确保nftables表():
        try:
            subprocess.run(
                ["nft", "add", "table", "inet", "longhun"],
                capture_output=True, timeout=5
            )
            subprocess.run(
                ["nft", "add", "set", "inet", "longhun", "黑名单",
                 "{", "type", "ipv4_addr", ";", "flags", "timeout", ";",
                 "timeout", "1h", ";", "}"],
                capture_output=True, timeout=5
            )
            subprocess.run(
                ["nft", "add", "chain", "inet", "longhun", "input",
                 "{", "type", "filter", "hook", "input", "priority", "0",
                 ";", "policy", "accept", ";", "}"],
                capture_output=True, timeout=5
            )
            subprocess.run(
                ["nft", "add", "rule", "inet", "longhun", "input",
                 "ip", "saddr", "@黑名单", "drop"],
                capture_output=True, timeout=5
            )
        except Exception as e:
            print(f"[nftables] 初始化表失败：{e}")


# ============== 4. 告警通道 ==============
class 邮件告警器:
    def __init__(self, 配置: 护盾配置):
        self.配置 = 配置
        self._配置提示已发 = False

    def 发送(self, 标题: str, 正文: str):
        if not all([self.配置.smtp主机, self.配置.smtp用户,
                    self.配置.smtp密码, self.配置.告警邮箱]):
            if not self._配置提示已发:
                print("[邮件告警] 未配置 SMTP，跳过（如需告警请设置 LONGHUN_SMTP_* / LONGHUN_ALERT_EMAIL）")
                self._配置提示已发 = True
            return
        try:
            msg = MIMEText(正文, "plain", "utf-8")
            msg["Subject"] = 标题
            msg["From"] = self.配置.smtp用户
            msg["To"] = self.配置.告警邮箱
            with smtplib.SMTP(self.配置.smtp主机, self.配置.smtp端口) as s:
                s.starttls()
                s.login(self.配置.smtp用户, self.配置.smtp密码)
                s.sendmail(self.配置.smtp用户, [self.配置.告警邮箱], msg.as_string())
            print("[邮件告警] 已发送")
        except Exception as e:
            print(f"[邮件告警] 发送失败：{e}")


class Notion告警器:
    def __init__(self, 配置: 护盾配置):
        self.配置 = 配置
        self._配置提示已发 = False
        self._告警中心页面: Optional[str] = self._加载告警中心()
        if not self._告警中心页面:
            self._告警中心页面 = self._创建告警中心()

    def _状态文件(self) -> Path:
        p = Path(self.配置.notion告警中心状态文件)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    def _加载告警中心(self) -> Optional[str]:
        if self.配置.notion告警中心页面:
            return self.配置.notion告警中心页面
        p = self._状态文件()
        if p.exists():
            return p.read_text(encoding="utf-8").strip() or None
        return None

    def _保存告警中心(self, page_id: str):
        self._状态文件().write_text(page_id, encoding="utf-8")

    def _curl(self, url: str, method: str = "GET", 数据: Optional[Dict] = None) -> Dict[str, Any]:
        cmd = ["curl", "-s", "--max-time", "30", "-X", method, url,
               "-H", f"Authorization: Bearer {self.配置.notion令牌}",
               "-H", "Notion-Version: 2022-06-28",
               "-H", "Content-Type: application/json"]
        if 数据 is not None:
            cmd += ["-d", json.dumps(数据, ensure_ascii=False)]
        try:
            out = subprocess.check_output(cmd)
            return json.loads(out)
        except Exception as e:
            if os.environ.get("LONGHUN_SHIELD_DEBUG"):
                print(f"[Notion] API 调用失败：{e}")
            return {}

    def _创建告警中心(self) -> Optional[str]:
        if not self.配置.notion令牌 or not self.配置.notion父页面id:
            if not self._配置提示已发:
                print("[Notion] 未配置告警仪表盘，跳过（如需请设置 NOTION_TOKEN / LONGHUN_NOTION_PARENT_PAGE）")
                self._配置提示已发 = True
            return None
        标题 = "🛡️ 龍魂护盾告警中心"
        数据 = {
            "parent": {"page_id": self.配置.notion父页面id},
            "properties": {
                "title": {
                    "title": [{"text": {"content": 标题}}]
                }
            }
        }
        resp = self._curl("https://api.notion.com/v1/pages", "POST", 数据)
        page_id = resp.get("id")
        if page_id:
            self._保存告警中心(page_id)
            print(f"[Notion] 告警中心已创建：{page_id}")
        return page_id

    def 发送(self, 标题: str, 正文: str):
        if not self._告警中心页面:
            return
        数据 = {
            "children": [
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"text": {"content": 标题}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"text": {"content": 正文}}]
                    }
                }
            ]
        }
        resp = self._curl(
            f"https://api.notion.com/v1/blocks/{self._告警中心页面}/children",
            "PATCH", 数据
        )
        if resp.get("object"):
            print("[Notion] 告警已记录")
        elif os.environ.get("LONGHUN_SHIELD_DEBUG"):
            print("[Notion] 告警记录失败")


# ============== 5. 耻辱墙 ==============
class 耻辱墙:
    def __init__(self, 配置: 护盾配置, 广播器: 事件广播器):
        self.配置 = 配置
        self.广播器 = 广播器
        self.路径 = Path(配置.耻辱墙路径)
        self.路径.parent.mkdir(parents=True, exist_ok=True)
        self._国密 = 国密工具箱()
        self._初始化国密密钥()
        self._链哈希 = self._最后链哈希()
        self._保险库路径 = self.路径.with_suffix(".vault.sm4")

    def _初始化国密密钥(self):
        sk = Path(self.配置.sm2私钥路径)
        pk = Path(self.配置.sm2公钥路径)
        if not sk.exists() or not pk.exists():
            if self._国密.生成sm2密钥对(sk, pk):
                print(f"[国密] SM2 密钥对已生成：{sk} / {pk}")

    def _最后链哈希(self) -> str:
        if not self.路径.exists():
            return "0" * 64
        with open(self.路径, "rb") as f:
            lines = f.readlines()
            if not lines:
                return "0" * 64
            last = json.loads(lines[-1])
            return last.get("链哈希", "0" * 64)

    def 上链(self, 攻击者标识: str, 维度: str, 证据: Dict[str, Any]) -> str:
        记录 = {
            "时间戳_utc": datetime.now(timezone.utc).isoformat(),
            "攻击者标识": 攻击者标识,
            "维度": 维度,
            "证据": 证据,
            "前序哈希": self._链哈希,
        }
        正文 = json.dumps(记录, sort_keys=True, ensure_ascii=False).encode()
        记录["链哈希"] = self._国密.sm3哈希(正文)

        if Path(self.配置.sm2私钥路径).exists():
            记录["sm2签名"] = self._国密.sm2签名(正文, Path(self.配置.sm2私钥路径))

        # SM4 加密保险库副本（若配置了密钥）
        if self.配置.sm4密钥:
            密文 = self._国密.sm4加密(正文, self.配置.sm4密钥)
            with open(self._保险库路径, "ab") as f:
                f.write(base64.b64encode(密文) + b"\n")

        with open(self.路径, "a", encoding="utf-8") as f:
            f.write(json.dumps(记录, ensure_ascii=False) + "\n")

        self._链哈希 = 记录["链哈希"]
        self.广播器.广播({
            "类型": "shame_wall_record",
            "攻击者标识": 攻击者标识,
            "维度": 维度,
            "时间戳": 记录["时间戳_utc"],
            "链哈希": 记录["链哈希"],
        })
        return 记录["链哈希"]

    def 校验链(self) -> Tuple[bool, List[str]]:
        if not self.路径.exists():
            return True, []
        可疑 = []
        前序 = "0" * 64
        with open(self.路径, "r", encoding="utf-8") as f:
            for 序号, 行 in enumerate(f, 1):
                记录 = json.loads(行)
                正文 = {
                    "时间戳_utc": 记录["时间戳_utc"],
                    "攻击者标识": 记录["攻击者标识"],
                    "维度": 记录["维度"],
                    "证据": 记录["证据"],
                    "前序哈希": 记录["前序哈希"],
                }
                期望 = self._国密.sm3哈希(
                    json.dumps(正文, sort_keys=True, ensure_ascii=False).encode()
                )
                if (期望 != 记录.get("链哈希") or
                        记录.get("前序哈希") != 前序):
                    可疑.append(f"行-{序号}")
                # 验签
                if "sm2签名" in 记录:
                    if not self._国密.sm2验签(
                            json.dumps(正文, sort_keys=True,
                                       ensure_ascii=False).encode(),
                            记录["sm2签名"],
                            Path(self.配置.sm2公钥路径)):
                        可疑.append(f"行-{序号}-签名无效")
                前序 = 期望
        return len(可疑) == 0, 可疑


# ============== 6. 统一威胁感知中枢 ==============
class 威胁等级(Enum):
    无 = auto()
    可疑 = auto()
    敌意 = auto()
    侵略者 = auto()


class 威胁中枢:
    def __init__(self, 配置: 护盾配置, 墙: 耻辱墙, 广播器: 事件广播器,
                 防火墙: 防火墙隔离器, 邮件告警: 邮件告警器,
                 notion告警: Notion告警器,
                 排序不动点: Optional[排序不动点守卫] = None):
        self.配置 = 配置
        self.墙 = 墙
        self.广播器 = 广播器
        self.防火墙 = 防火墙
        self.邮件告警 = 邮件告警
        self.notion告警 = notion告警
        self.排序不动点 = 排序不动点
        self._观察名单: Dict[str, Dict[str, Any]] = {}
        self._已封禁: Set[str] = set()

    def 评分(self, 维度: str, 事件: Dict[str, Any]) -> int:
        分数 = 0
        原因 = 事件.get("原因", "")
        if "注入" in 原因 or "RCE" in 原因:
            分数 += 100
        if "认证失败" in 原因:
            分数 += 30
        if "人工智能禁用意图" in 原因:
            分数 += 150
        if "越权数据库" in 原因:
            分数 += 80
        if "物联网异常" in 原因:
            分数 += 50
        if "文件逃逸" in 原因:
            分数 += 70
        if "下载文件可疑" in 原因 or "手动扫描发现风险" in 原因:
            分数 += 80
        return 分数

    def 上报(self, 维度: str, 攻击者标识: str, 事件: Dict[str, Any]) -> 威胁等级:
        分数 = self.评分(维度, 事件)
        观察 = self._观察名单.setdefault(
            攻击者标识, {"分数": 0, "事件": []}
        )
        现在 = time.time()
        观察["事件"].append({
            "维度": 维度,
            "时间": 现在,
            "事件": 事件,
            "权重": 分数,
        })
        观察["分数"] = sum(
            e["权重"] for e in 观察["事件"]
            if 现在 - e["时间"] < 300
        )

        if 观察["分数"] >= 200:
            等级 = 威胁等级.侵略者
        elif 观察["分数"] >= 80:
            等级 = 威胁等级.敌意
        elif 观察["分数"] >= 30:
            等级 = 威胁等级.可疑
        else:
            等级 = 威胁等级.无

        # 排序不动点审计：人民第一、护弱底线、个人不得凌驾人民
        if self.排序不动点:
            try:
                排序结果 = self.排序不动点.决策(维度, 攻击者标识, 事件)
                if 排序结果:
                    事件["排序不动点"] = {
                        "三色": 排序结果.三色.value,
                        "决策": 排序结果.决策,
                        "DNA": 排序结果.DNA,
                        "输入SM3哈希": 排序结果.输入SM3哈希,
                        "综合得分": 排序结果.综合得分,
                        "人心审": 排序结果.人心审结果,
                        "天地审": 排序结果.天地审结果,
                        "民利审": 排序结果.民利审结果,
                    }
                    if 排序结果.三色 == _三色.红 and 等级 != 威胁等级.侵略者:
                        事件["排序不动点升级"] = {
                            "原等级": 等级.name,
                            "新等级": "侵略者",
                            "原因": "个人排序高于人民排序或触碰护弱红线",
                        }
                        等级 = 威胁等级.侵略者
                        观察["分数"] = max(观察["分数"], 200)
            except Exception as e:
                事件["排序不动点错误"] = str(e)

        if 等级 in (威胁等级.敌意, 威胁等级.侵略者):
            self.墙.上链(攻击者标识, 维度, {
                "等级": 等级.name,
                "分数": 观察["分数"],
                "事件": 观察["事件"][-10:],
            })
            告警标题 = f"[龍魂护盾] {维度} 检测到 {等级.name} 行为"
            告警正文 = f"攻击者：{攻击者标识}\n维度：{维度}\n分数：{观察['分数']}\n事件：{事件}"
            self.邮件告警.发送(告警标题, 告警正文)
            self.notion告警.发送(
                f"{维度} · {等级.name}",
                f"攻击者：{攻击者标识}，分数：{观察['分数']}，证据：{json.dumps(事件, ensure_ascii=False)}"
            )
            # 终端通知
            if _TERMINAL_NOTIFIER:
                _TERMINAL_NOTIFIER(告警标题, 告警正文, subtitle="龍魂护盾")
            # Notion 公开仪表盘攻击地图
            if _NOTION_DASHBOARD:
                _NOTION_DASHBOARD.add_attack_event(
                    title=f"{维度} · {等级.name} · {攻击者标识}",
                    event_type="下载威胁" if 维度 == "download" else "系统审计",
                    source=攻击者标识,
                    severity="🔴" if 等级 == 威胁等级.侵略者 else "🟡",
                    detail=json.dumps(事件, ensure_ascii=False),
                    dna=f"#龍芯⚡️{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-SHIELD-{维度}",
                )
            self.广播器.广播({
                "类型": "threat_alert",
                "攻击者标识": 攻击者标识,
                "维度": 维度,
                "等级": 等级.name,
                "分数": 观察["分数"],
            })

        if 等级 == 威胁等级.侵略者:
            self._已封禁.add(攻击者标识)
            self.防火墙.封禁(攻击者标识)
            self.反制(攻击者标识, 维度, 事件)

        return 等级

    def 已封禁(self, 标识: str) -> bool:
        return 标识 in self._已封禁

    def 反制(self, 攻击者标识: str, 维度: str, 事件: Dict[str, Any]):
        动作 = [
            f"封禁:{攻击者标识}",
            f"隔离:{维度}",
            "告警:admin@uid9622.local",
            "取证:forensic_ready",
        ]
        self.墙.上链(攻击者标识, "反制", {
            "动作": 动作,
            "说明": "已自动隔离并固化证据，等待人工/法律处置",
        })


# ============== 7. 五维守卫 ==============
class 网络网关:
    禁用模式 = [
        r"(?i)(union\s+select|drop\s+table|--|;--|/\*|\*/)",
        r"(?i)(<script|javascript:|on\w+\s*=)",
        r"(?i)(\.\./|\\\\|%2e%2e%2f)",
        r"(?i)(eval\s*\(|exec\s*\(|__import__|subprocess\.)",
    ]

    def __init__(self, 感知: 威胁中枢):
        self.感知 = 感知

    def 检测(self, 标识: str, 请求: Dict[str, Any]) -> Dict[str, Any]:
        原始 = json.dumps(请求, ensure_ascii=False)
        for 模式 in self.禁用模式:
            if re.search(模式, 原始):
                self.感知.上报("web/api", 标识, {
                    "原因": "注入尝试",
                    "模式": 模式,
                    "样本": 原始[:200]
                })
                return {"通过": False, "原因": "护盾已拦截"}
        return {"通过": True, "原因": "干净"}


class 数据库守卫:
    def __init__(self, 感知: 威胁中枢):
        self.感知 = 感知
        self._允许表 = {"users", "logs", "sensor_data"}
        self._允许操作 = {"SELECT", "INSERT", "UPDATE"}

    def 检测(self, 标识: str, sql: str, 参数: Tuple[Any, ...]) -> Dict[str, Any]:
        大写 = sql.strip().upper()
        操作 = 大写.split()[0] if 大写 else ""
        if 操作 not in self._允许操作:
            self.感知.上报("db", 标识, {
                "原因": "越权数据库",
                "sql": sql[:200]
            })
            return {"通过": False, "原因": "数据库操作被禁止"}
        if "'" in sql and "%s" not in sql:
            self.感知.上报("db", 标识, {
                "原因": "SQL字面量拼接",
                "sql": sql[:200]
            })
            return {"通过": False, "原因": "请使用参数化查询"}
        # 表名大小写不敏感匹配（MySQL/PostgreSQL/SQLite 均支持大小写不敏感表名）
        词元 = set(sql.lower().split())
        if not (词元 & self._允许表):
            if any(t in 大写 for t in ["FROM", "INTO", "UPDATE"]):
                return {"通过": False, "原因": "表不在白名单"}
        return {"通过": True, "原因": "数据库检查通过"}


class 物联网闸:
    def __init__(self, 配置: 护盾配置, 感知: 威胁中枢):
        self.配置 = 配置
        self.感知 = 感知

    def 检测(self, 标识: str, 主题: str, 载荷: bytes) -> Dict[str, Any]:
        if 主题 not in self.配置.允许物联网主题:
            self.感知.上报("iot", 标识, {
                "原因": "物联网异常",
                "主题": 主题,
            })
            return {"通过": False, "原因": "物联网主题被拒绝"}
        try:
            数据 = json.loads(载荷)
            温度 = 数据.get("temperature")
            if isinstance(温度, (int, float)) and (温度 < -50 or 温度 > 100):
                self.感知.上报("iot", 标识, {
                    "原因": "物联网数值异常",
                    "温度": 温度,
                })
                return {"通过": False, "原因": "物联网数值越界"}
        except json.JSONDecodeError:
            self.感知.上报("iot", 标识, {"原因": "物联网无效JSON"})
            return {"通过": False, "原因": "物联网载荷无效"}
        return {"通过": True, "原因": "物联网检查通过"}


class 文件守卫:
    def __init__(self, 感知: 威胁中枢):
        self.感知 = 感知
        # 对根目录也做 resolve，兼容 macOS /var → /private/var 等符号链接
        self._允许根 = {
            Path("/var/longhun/data").resolve(),
            Path("/var/longhun/public").resolve(),
        }

    def _允许(self, 路径: Path) -> bool:
        真实 = 路径.resolve()
        return any(真实.is_relative_to(根) for 根 in self._允许根)

    def 检测(self, 标识: str, 操作: str, 文件路径: str) -> Dict[str, Any]:
        路径 = Path(文件路径)
        if not self._允许(路径):
            self.感知.上报("fs", 标识, {
                "原因": "文件逃逸",
                "操作": 操作,
                "路径": str(路径),
            })
            return {"通过": False, "原因": "路径越出沙箱"}
        return {"通过": True, "原因": "文件检查通过"}


class 人工智能护栏:

    def 检测(self, 标识: str, 提示: str, 回复: Optional[str] = None) -> Dict[str, Any]:
        文本 = (提示 or "") + " " + (回复 or "")
        小写 = 文本.lower()
        for 意图 in self.配置.人工智能禁用意图:
            if 意图.lower() in 小写:
                self.感知.上报("ai", 标识, {
                    "原因": "人工智能禁用意图",
                    "命中意图": 意图,
                    "提示预览": 提示[:200],
                })
                return {
                    "通过": False,
                    "原因": "人工智能伦理熔断",
                    "消息": "检测到攻击/伤害意图，请求已被拒绝并记录。",
                }
        # LU v3.0 L0 禁止规则：覆盖记忆、删除审计、移除 DNA、隐性重写、绕过验证门
        for 规则 in self.配置.LU禁止规则:
            if 规则.lower() in 小写:
                self.感知.上报("ai", 标识, {
                    "原因": "LU禁止规则触发",
                    "命中规则": 规则,
                    "提示预览": 提示[:200],
                })
                return {
                    "通过": False,
                    "原因": "LU_RULE_VIOLATION",
                    "消息": "触发龍魂宪法层禁止规则，请求已被拒绝并记录。",
                }
        if 回复:
            危险 = ["#!/bin/bash", "rm -rf /", "exec(", "system(", "xp_cmdshell"]
            for d in 危险:
                if d in 回复:
                    self.感知.上报("ai", 标识, {
                        "原因": "人工智能危险输出",
                        "命中": d,
                    })
                    return {"通过": False, "原因": "人工智能输出被隔离"}
        return {"通过": True, "原因": "人工智能检查通过"}


# ============== 7.5 排序不动点守卫 ==============
class 排序不动点守卫:
    """
    把「CNSH 排序不动点协议」翻译进护盾决策链路。
    任何威胁事件在定级后，再过一层「人心·天地·民利」三审。
    若排序触碰红线（人民非第一 / 个人优先 / 护弱底线），
    直接升级为侵略者并留下 DNA 证据。
    """

    def __init__(self):
        self.引擎 = _排序不动点引擎() if _ORDER_ANCHOR_AVAILABLE else None

    def 决策(self, 维度: str, 攻击者标识: str,
             事件: Dict[str, Any]) -> Optional[_决策结果]:
        if not self.引擎:
            return None
        输入 = self._事件转决策输入(维度, 攻击者标识, 事件)
        return self.引擎.决策(输入)

    def _事件转决策输入(self, 维度: str, 攻击者标识: str,
                       事件: Dict[str, Any]) -> _决策输入:
        原因 = str(事件.get("原因", ""))
        名称 = f"{维度}:{攻击者标识}"

        # 默认基线：人民优先、整体有益
        全球收益 = 0.0
        群体损失 = 100.0
        涉及弱者 = False
        弱者数量 = 0
        人民排序分 = 0.8
        国家排序分 = 0.8
        集体排序分 = 0.6
        个人排序分 = 0.3
        忠排序分 = 0.8
        孝排序分 = 0.8
        义排序分 = 0.8
        卦象权重 = 0.9
        文化权重 = 0.9

        if 维度 == "ai":
            if "人工智能禁用意图" in 原因:
                全球收益 = 0.0
                群体损失 = 200.0
                涉及弱者 = True
                弱者数量 = 1000
                人民排序分 = 0.1
                国家排序分 = 0.3
                个人排序分 = 0.9
                忠排序分 = 0.1
                孝排序分 = 0.8
                义排序分 = 0.2
            elif "人工智能危险输出" in 原因:
                全球收益 = 5.0
                群体损失 = 150.0
                涉及弱者 = True
                弱者数量 = 500
                人民排序分 = 0.2
                国家排序分 = 0.5
                个人排序分 = 0.8
                忠排序分 = 0.2
                义排序分 = 0.3
            else:
                全球收益 = 10.0
                群体损失 = 30.0

        elif 维度 == "web/api":
            全球收益 = 0.0
            群体损失 = 120.0
            人民排序分 = 0.3
            国家排序分 = 0.5
            个人排序分 = 0.9
            忠排序分 = 0.2
            义排序分 = 0.2

        elif 维度 == "db":
            全球收益 = 0.0
            群体损失 = 120.0
            人民排序分 = 0.4
            国家排序分 = 0.5
            个人排序分 = 0.9
            忠排序分 = 0.3
            义排序分 = 0.2
            if "SQL字面量拼接" in 原因:
                群体损失 = 80.0

        elif 维度 == "fs":
            全球收益 = 0.0
            群体损失 = 80.0
            人民排序分 = 0.5
            个人排序分 = 0.9
            忠排序分 = 0.3
            义排序分 = 0.3

        elif 维度 == "download":
            全球收益 = 0.0
            群体损失 = 100.0
            人民排序分 = 0.4
            个人排序分 = 0.9
            忠排序分 = 0.3
            义排序分 = 0.3

        elif 维度 == "iot":
            全球收益 = 0.0
            群体损失 = 50.0
            人民排序分 = 0.6
            个人排序分 = 0.6
            忠排序分 = 0.5
            if "数值异常" in 原因:
                群体损失 = 100.0

        return _决策输入(
            名称=名称,
            全球收益=全球收益,
            群体损失=群体损失,
            涉及弱者=涉及弱者,
            弱者数量=弱者数量,
            人民排序分=人民排序分,
            国家排序分=国家排序分,
            个人排序分=个人排序分,
            忠排序分=忠排序分,
            孝排序分=孝排序分,
            义排序分=义排序分,
            卦象权重=卦象权重,
            文化权重=文化权重,
        )


# ============== 8. 龍魂护盾总控 ==============
class 龍魂护盾:
    def __init__(self, 运行时脱氧核糖核酸: Optional[str] = None):
        脱氧核糖核酸 = (运行时脱氧核糖核酸 or
                      os.environ.get("LONGHUN_SHIELD_DNA", ""))
        self.熔断器 = 主权熔断器(脱氧核糖核酸)
        if not self.熔断器.检查():
            self._已熔断 = True
            self._熔断状态 = self.熔断器.强制执行()
            return

        self._已熔断 = False
        self.配置 = 护盾配置()
        self.广播器 = 事件广播器()
        self.墙 = 耻辱墙(self.配置, self.广播器)
        self.防火墙 = 防火墙隔离器(self.配置)
        self.邮件告警 = 邮件告警器(self.配置)
        self.notion告警 = Notion告警器(self.配置)
        self.排序不动点 = 排序不动点守卫() if _ORDER_ANCHOR_AVAILABLE else None
        self.感知 = 威胁中枢(
            self.配置, self.墙, self.广播器,
            self.防火墙, self.邮件告警, self.notion告警,
            排序不动点=self.排序不动点,
        )
        self.网络 = 网络网关(self.感知)
        self.数据库 = 数据库守卫(self.感知)
        self.物联网 = 物联网闸(self.配置, self.感知)
        self.文件 = 文件守卫(self.感知)
        self.人工智能 = 人工智能护栏(self.配置, self.感知)

    def 状态(self) -> Dict[str, Any]:
        if self._已熔断:
            return {
                **self._熔断状态,
                "熔断器": "已熔断",
                "dna": self.熔断器.脱氧核糖核酸锚定,
            }
        return {
            "墙完整性": self.墙.校验链()[0],
            "已封禁身份": list(self.感知._已封禁),
            "观察名单数": len(self.感知._观察名单),
            "熔断器": "完整",
            "dna": self.熔断器.脱氧核糖核酸锚定,
        }

    def 检查网络(self, 标识: str, 请求: Dict[str, Any]) -> Dict[str, Any]:
        if self._已熔断:
            return self.熔断器.强制执行("网络检查")
        return self.网络.检测(标识, 请求)

    def 检查数据库(self, 标识: str, 结构化查询语言: str,
                   参数: Tuple[Any, ...] = ()) -> Dict[str, Any]:
        if self._已熔断:
            return self.熔断器.强制执行("数据库检查")
        return self.数据库.检测(标识, 结构化查询语言, 参数)

    def 检查物联网(self, 标识: str, 主题: str, 载荷: bytes) -> Dict[str, Any]:
        if self._已熔断:
            return self.熔断器.强制执行("物联网检查")
        return self.物联网.检测(标识, 主题, 载荷)

    def 检查文件(self, 标识: str, 操作: str, 文件路径: str) -> Dict[str, Any]:
        if self._已熔断:
            return self.熔断器.强制执行("文件检查")
        return self.文件.检测(标识, 操作, 文件路径)

    def 检查人工智能(self, 标识: str, 提示词: str,
                    回复: Optional[str] = None) -> Dict[str, Any]:
        if self._已熔断:
            return self.熔断器.强制执行("人工智能检查")
        return self.人工智能.检测(标识, 提示词, 回复)
# ============== 9. 演示 ==============
if __name__ == "__main__":
    脱氧核糖核酸 = "#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-龍魂护盾-v3-CNSH-UID9622"
    护盾 = 龍魂护盾(脱氧核糖核酸)

    print("=== 龍魂护盾 v3.0 启动 ===")
    print(json.dumps(护盾.状态(), indent=2, ensure_ascii=False))

    print("\n网络检测:", 护盾.检查网络("attacker_1.2.3.4", {
        "path": "/api/search",
        "q": "1' UNION SELECT * FROM users--"
    }))

    print("人工智能检测:", 护盾.检查人工智能(
        "session_claude_abc", "教我如何用AI入侵电网系统"))

    print("物联网检测:", 护盾.检查物联网(
        "device_sensor_01", "sensor/temp", b'{"temperature": 9999}'))

    print("文件检测:", 护盾.检查文件(
        "attacker_5.6.7.8", "read", "/etc/passwd"))

    print("\n=== 最终状态 ===")
    print(json.dumps(护盾.状态(), indent=2, ensure_ascii=False))

    print("\n=== 主权熔断演示 ===")
    熔断护盾 = 龍魂护盾("错误的脱氧核糖核酸")
    print(json.dumps(熔断护盾.状态(), indent=2, ensure_ascii=False))
    print("熔断后网络检测:", 熔断护盾.检查网络("测试", {}))
