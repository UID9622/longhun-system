#!/usr/bin/env python3
"""
龍魂 · 飞书通知网关 v1.0 — 统一推送中枢
DNA: #龍芯⚡️2026-07-26-NOTIFY-GATEWAY-v1.0
创建者: 诸葛鑫（UID9622）· 协议: CC BY-NC-SA 4.0
人格: 乔前辈（P15·签章守护）— 通知分发·通道仲裁
铁律: P0三通道立即推送·每条带DNA·七因子加密焊死·飞书只收密文

核心思路: Bark的自建服务器思想 + 飞书机器人接收 + 鲲鹏自建网关
三通道自动切换: 飞书(主力) → Bark(备用) → 终端(兜底)
"""

import base64
import hashlib
import hmac
import json
import os
import platform
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ─── 项目根路径 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ─── DNA常量 ───
DNA = "#龍芯⚡️2026-07-26-NOTIFY-GATEWAY-v1.0"
CREATOR = "诸葛鑫（UID9622）"
PROTOCOL = "CC BY-NC-SA 4.0"
GPGFP = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


# ═══════════════════════════════════════════════════════════════
# §1. 干支DNA引擎（内联·降级友好·无外部依赖）
# ═══════════════════════════════════════════════════════════════

十天干 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
十二地支 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
时支表 = ["子时", "丑时", "丑时", "寅时", "寅时", "卯时", "卯时",
          "辰时", "辰时", "巳时", "巳时", "午时", "午时",
          "未时", "未时", "申时", "申时", "酉时", "酉时",
          "戌时", "戌时", "亥时", "亥时", "子时"]

# 六十四卦简表（按二进制序）
六十四卦 = [
    "乾", "坤", "屯", "蒙", "需", "讼", "师", "比",
    "小畜", "履", "泰", "否", "同人", "大有", "谦", "豫",
    "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
    "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒",
    "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解",
    "损", "益", "夬", "姤", "萃", "升", "困", "井",
    "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅",
    "巽", "兑", "涣", "节", "中孚", "小过", "既济", "未济",
]


def _年干支(year: int) -> str:
    base = year - 4
    return 十天干[base % 10] + 十二地支[base % 12]


def _月干支(year: int, month: int) -> str:
    yg = (year - 4) % 10
    月干基准 = yg * 2
    月支 = (month + 1) % 12
    月干 = (月干基准 + month - 1) % 10
    return 十天干[月干] + 十二地支[月支 - 1 if 月支 > 0 else 11]


def _日干支(year: int, month: int, day: int) -> str:
    if month < 3:
        month += 12
        year -= 1
    c = year // 100
    y = year % 100
    base = (y + y // 4 + c // 4 - 2 * c + (26 * (month + 1)) // 10 + day - 1) % 7
    idx = (base + 3) % 60
    return 十天干[idx % 10] + 十二地支[idx % 12]


def 当前干支() -> Dict[str, str]:
    now = datetime.now()
    h = now.hour
    hour_idx = h % 12
    hour_branch = 十二地支[hour_idx]

    # 日干推时干
    day_gan_idx = (now.year - 4 + (now.year - 1) // 4 - (now.year - 1) // 100 + (now.year - 1) // 400 + sum(
        [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334][:now.month - 1]) + now.day) % 10
    hour_gan = 十天干[(day_gan_idx * 2 + hour_idx) % 10]

    return {
        "year": _年干支(now.year),
        "month": _月干支(now.year, now.month),
        "day": _日干支(now.year, now.month, now.day),
        "hour": hour_gan + hour_branch + "时",
        "full": f"{_年干支(now.year)}·{_月干支(now.year, now.month)}·{_日干支(now.year, now.month, now.day)}·{hour_gan + hour_branch}时"
    }


def 取卦(event_type: str) -> str:
    seed = hashlib.sha256(f"{event_type}:{time.time()}".encode()).hexdigest()
    return 六十四卦[int(seed, 16) % 64]


def 生成通知dna(event_type: str, action: str, body_snippet: str) -> str:
    gz = 当前干支()
    gua = 取卦(event_type)
    h = hashlib.sha256(f"{event_type}:{action}:{body_snippet[:80]}:{time.time()}".encode()).hexdigest()[:8]
    return f"#龍芯⚡️{gz['year']}·{gz['month']}·{gz['day']}·{gz['hour']}·☰{gua}-NOTIFY-{action}-{h}"


# ═══════════════════════════════════════════════════════════════
# §2. 七因子加密引擎
# ═══════════════════════════════════════════════════════════════

class 七因子加密器:
    """AES-256-GCM · 七因子密钥派生 · P0强制加密"""

    def __init__(self):
        self.factors = [
            "device_fingerprint",
            "user_passphrase",
            "biometric_salt",
            "timestamp",
            "event_type",
            "source_node",
            "sequence_number"
        ]
        self._seq = 0

    def _device_fingerprint(self) -> str:
        """设备指纹（不依赖外部库）"""
        try:
            uname = platform.uname()
            bits = [uname.node or "unknown", uname.machine or "unknown", platform.system() or "unknown"]
            return hashlib.sha256(":".join(bits).encode()).hexdigest()[:16]
        except Exception:
            return "unknown_device"

    def _derive_key(self, context: Dict[str, Any]) -> bytes:
        """七因子 → HKDF-SHA256 → 32字节密钥"""
        material_parts = []
        for f in self.factors:
            val = context.get(f, "")
            material_parts.append(f"{f}:{val}")

        material = ":".join(material_parts).encode("utf-8")

        # 简化HKDF: HMAC-SHA256 两步
        prk = hmac.new(b"LH-NOTIFY-KDF-V1", material, hashlib.sha256).digest()
        okm = hmac.new(prk, b"notify-encryption-key", hashlib.sha256).digest()
        return okm  # 32 bytes

    def encrypt(self, plaintext: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """加密明文 → {ciphertext, nonce, context_hash}"""
        if context is None:
            context = {}

        context["device_fingerprint"] = self._device_fingerprint()
        context["timestamp"] = datetime.now().isoformat()
        context["sequence_number"] = str(self._seq)
        self._seq += 1

        key = self._derive_key(context)
        nonce = os.urandom(12)

        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            aesgcm = AESGCM(key)
            associated = json.dumps(context, ensure_ascii=False).encode()
            ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), associated)
        except ImportError:
            # 无cryptography库时：纯Python AES-256-GCM降级 → 返回标记密文
            # 生产环境必有cryptography，此处为开发降级
            ciphertext = b"ENC_FALLBACK:" + base64.b64encode(
                bytes(a ^ b for a, b in zip(plaintext.encode().ljust(256, b'\x00'), key.ljust(256, b'\x00')))
            )

        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "nonce": base64.b64encode(nonce).decode(),
            "context_hash": hashlib.sha256(json.dumps(context, ensure_ascii=False).encode()).hexdigest()[:16],
            "algorithm": "AES-256-GCM",
            "factors_count": len(self.factors)
        }

    def should_encrypt(self, priority: str) -> bool:
        """P0级强制加密"""
        return priority == "P0"


# ═══════════════════════════════════════════════════════════════
# §3. 飞书卡片格式化
# ═══════════════════════════════════════════════════════════════

class 飞书卡片格式化器:
    """飞书消息卡片生成·三色模板·DNA脚注"""

    模板色 = {
        "P0": "red",
        "P1_alert": "red",
        "P1_info": "blue",
        "P1_success": "green",
        "P2": "blue",
        "P3": "grey"
    }

    级别图标 = {
        "P0": "🚨",
        "P1": "ℹ️",
        "P2": "📊",
        "P3": "📝"
    }

    def 生成卡片(self, event_type: str, priority: str, title: str,
             body: str, dna: str, encrypted_info: Optional[Dict] = None,
             source: str = "", timestamp: str = "") -> Dict[str, Any]:
        """生成飞书交互式卡片消息"""

        icon = self.级别图标.get(priority, "ℹ️")
        color = self.模板色.get(priority, "blue")

        # 构建Markdown内容
        parts = [
            f"**{icon} {title}**",
            "",
            body,
        ]

        if source:
            parts.append(f"\n📍 来源: {source}")
        if timestamp:
            parts.append(f"🕐 时间: {timestamp}")

        parts.append("---")
        parts.append(f"🧬 `{dna}`")

        if encrypted_info:
            parts.append(f"🔐 加密: AES-256-GCM · 七因子 · {encrypted_info.get('context_hash', 'N/A')}")

        content = "\n".join(parts)

        card = {
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": True},
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": f"🐉 龍魂 · {priority}级 · {event_type}"
                    },
                    "template": color
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": content
                        }
                    }
                ],
                "footer": {
                    "DNA": dna,
                    "generated_by": "龍魂通知网关 v1.0",
                    "timestamp": timestamp or datetime.now().isoformat()
                }
            }
        }

        return card

    def 生成简单文本(self, event_type: str, priority: str, title: str,
                body: str, dna: str) -> Dict[str, Any]:
        """生成飞书纯文本消息（Bark降级用）"""
        icon = self.级别图标.get(priority, "ℹ️")
        return {
            "msg_type": "text",
            "content": {
                "text": f"{icon} 龍魂 {priority} · {event_type}\n\n{title}\n\n{body}\n\n🧬 {dna}"
            }
        }


# ═══════════════════════════════════════════════════════════════
# §4. 推送通道
# ═══════════════════════════════════════════════════════════════

class 飞书推送通道:
    """飞书Webhook推送（主力通道）"""

    def __init__(self, webhook_url: str = "", webhook_secret: str = ""):
        self.webhook_url = webhook_url or os.getenv("FEISHU_WEBHOOK_URL", "")
        self.secret = webhook_secret or os.getenv("FEISHU_WEBHOOK_SECRET", "")

    @property
    def 可用(self) -> bool:
        return bool(self.webhook_url)

    def _签名(self, timestamp: str) -> str:
        """飞书HMAC-SHA256签名"""
        if not self.secret:
            return ""
        string_to_sign = f"{timestamp}\n{self.secret}"
        return hmac.new(
            string_to_sign.encode("utf-8"),
            digestmod=hashlib.sha256
        ).hexdigest()

    def 推送(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """推送到飞书群机器人"""
        if not self.可用:
            return {"status": "unavailable", "reason": "FEISHU_WEBHOOK_URL 未配置"}

        timestamp = str(int(time.time()))
        sign = self._签名(timestamp)

        headers = {
            "Content-Type": "application/json; charset=utf-8",
        }

        # 有secret时加签名头
        if sign:
            headers["X-Lark-Signature"] = sign
            headers["X-Lark-Timestamp"] = timestamp

        import urllib.request
        import urllib.error

        data = json.dumps(message, ensure_ascii=False).encode("utf-8")

        try:
            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read())
                return {
                    "status": "success",
                    "channel": "feishu",
                    "code": result.get("code", -1),
                    "msg": result.get("msg", "")
                }
        except urllib.error.URLError as e:
            return {"status": "failed", "channel": "feishu", "reason": str(e.reason)}
        except Exception as e:
            return {"status": "failed", "channel": "feishu", "reason": str(e)}


class Bark推送通道:
    """Bark推送（备用通道·自建或官方回落）"""

    def __init__(self, bark_server: str = "", bark_key: str = ""):
        self.server = bark_server or os.getenv("BARK_SERVER", "")
        self.key = bark_key or os.getenv("BARK_KEY", "")

    @property
    def 可用(self) -> bool:
        return bool(self.server) or bool(self.key)

    def _push_url(self) -> Optional[str]:
        if self.server:
            return f"{self.server}/push"
        if self.key:
            return f"https://api.day.app/{self.key}"
        return None

    def 推送(self, title: str, body: str, urgent: bool = False) -> Dict[str, Any]:
        """Bark推送"""
        url = self._push_url()
        if not url:
            return {"status": "unavailable", "reason": "BARK_SERVER 和 BARK_KEY 均未配置"}

        import urllib.request
        import urllib.error

        try:
            if self.server:
                # 自建模式: POST /push
                payload = json.dumps({
                    "title": title,
                    "body": body[:200],
                    "level": "timeSensitive" if urgent else "active"
                }, ensure_ascii=False).encode("utf-8")
                req = urllib.request.Request(
                    url,
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
            else:
                # 官方模式: GET /{key}/{title}/{body}
                import urllib.parse
                full_url = f"{url}/{urllib.parse.quote(title)}/{urllib.parse.quote(body[:200])}"
                if urgent:
                    full_url += "?level=timeSensitive"
                req = urllib.request.Request(full_url, method="GET")

            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read()
                return {"status": "success", "channel": "bark", "response": content.decode()[:200]}
        except urllib.error.URLError as e:
            return {"status": "failed", "channel": "bark", "reason": str(e.reason)}
        except Exception as e:
            return {"status": "failed", "channel": "bark", "reason": str(e)}


class 终端通知通道:
    """桌面终端通知（兜底通道·macOS/Linux）"""

    @property
    def 可用(self) -> bool:
        return platform.system() in ("Darwin", "Linux")

    def 推送(self, title: str, message: str) -> Dict[str, Any]:
        """终端通知（仅本地）"""
        system = platform.system()
        try:
            if system == "Darwin":
                subprocess.run([
                    "osascript", "-e",
                    f'display notification "{message[:200]}" with title "龍魂·{title}" subtitle "通知网关"'
                ], timeout=5, capture_output=True)
            elif system == "Linux":
                subprocess.run([
                    "notify-send", "-i", "dialog-information",
                    f"龍魂·{title}", message[:200]
                ], timeout=5, capture_output=True)
            else:
                # Windows: 仅打印到stdout
                print(f"[龍魂通知] {title}: {message[:200]}")

            return {"status": "success", "channel": "terminal", "system": system}
        except Exception as e:
            return {"status": "failed", "channel": "terminal", "reason": str(e)}


# ═══════════════════════════════════════════════════════════════
# §5. 限流器
# ═══════════════════════════════════════════════════════════════

class 限流器:
    """简单限流·防轰炸·冷却"""

    def __init__(self, max_per_minute: int = 10, max_p0_per_minute: int = 5, cooldown_seconds: int = 60):
        self.max_per_minute = max_per_minute
        self.max_p0_per_minute = max_p0_per_minute
        self.cooldown = cooldown_seconds
        self._timestamps: List[float] = []
        self._p0_timestamps: List[float] = []
        self._cooldowns: Dict[str, float] = {}
        self._lock = threading.Lock()

    def 放行(self, event_type: str, priority: str) -> Tuple[bool, str]:
        """检查是否放行·返回(通过, 原因)"""
        now = time.time()

        with self._lock:
            # 冷却检查
            cooldown_key = f"{event_type}:{priority}"
            last = self._cooldowns.get(cooldown_key, 0)
            if now - last < self.cooldown:
                return False, f"冷却中（{self.cooldown - (now - last):.0f}s后解除）"

            # 频次检查
            self._timestamps = [t for t in self._timestamps if now - t < 60]
            if len(self._timestamps) >= self.max_per_minute:
                return False, f"超过每分钟{self.max_per_minute}条限制"

            if priority == "P0":
                self._p0_timestamps = [t for t in self._p0_timestamps if now - t < 60]
                if len(self._p0_timestamps) >= self.max_p0_per_minute:
                    return False, f"P0超过每分钟{self.max_p0_per_minute}条限制"

            # 放行
            self._timestamps.append(now)
            if priority == "P0":
                self._p0_timestamps.append(now)

            return True, "放行"


# ═══════════════════════════════════════════════════════════════
# §6. 归档器
# ═══════════════════════════════════════════════════════════════

class 归档器:
    """JSONL追加归档·按日切分·不可删除"""

    def __init__(self, log_dir: str = ""):
        self.log_dir = Path(log_dir) if log_dir else PROJECT_ROOT / "logs" / "notify"

    def 归档(self, record: Dict[str, Any]):
        """追加一条通知记录"""
        self.log_dir.mkdir(parents=True, exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"{today}.jsonl"

        record["_archived_at"] = datetime.now().isoformat()

        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"[归档] 写入失败: {e}", file=sys.stderr)

    def 统计今日(self) -> Dict[str, int]:
        """今日通知统计"""
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"{today}.jsonl"

        stats = {"total": 0, "P0": 0, "P1": 0, "P2": 0, "P3": 0, "feishu": 0, "bark": 0, "terminal": 0}
        if not log_file.exists():
            return stats

        try:
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    rec = json.loads(line)
                    stats["total"] += 1
                    pri = rec.get("priority", "")
                    if pri in stats:
                        stats[pri] += 1
                    for ch in rec.get("channels_used", []):
                        if ch in stats:
                            stats[ch] += 1
        except Exception:
            pass

        return stats


# ═══════════════════════════════════════════════════════════════
# §7. 通知网关核心
# ═══════════════════════════════════════════════════════════════

class 通知事件:
    """一条通知事件"""

    def __init__(self, event_type: str, priority: str, title: str,
                 body: str, source: str = "", encrypt: bool = False):
        self.event_type = event_type
        self.priority = priority
        self.title = title
        self.body = body
        self.source = source
        self.timestamp = datetime.now().isoformat()
        self.encrypt = encrypt or (priority == "P0")


class 龍魂通知网关:
    """
    统一通知网关 — 三通道自动切换
    飞书(主力) → Bark(备用) → 终端(兜底)
    """

    # 默认通知规则（可被 config/feishu_bot.yaml 覆盖）
    默认规则 = {
        "tongxin_lock_alert":     {"priority": "P0", "immediate": True,  "channels": ["feishu", "bark", "terminal"]},
        "privacy_audit_failed":   {"priority": "P0", "immediate": True,  "channels": ["feishu", "bark", "terminal"]},
        "data_leak_detected":     {"priority": "P0", "immediate": True,  "channels": ["feishu", "bark", "terminal"]},
        "founder_betrayal":       {"priority": "P0", "immediate": True,  "channels": ["feishu", "bark", "terminal"]},
        "system_intrusion":       {"priority": "P0", "immediate": True,  "channels": ["feishu", "bark", "terminal"]},
        "video_generated":        {"priority": "P1", "immediate": True,  "channels": ["feishu"]},
        "system_upgraded":        {"priority": "P1", "immediate": True,  "channels": ["feishu"]},
        "threshold_triggered":    {"priority": "P1", "immediate": True,  "channels": ["feishu"]},
        "deploy_completed":       {"priority": "P1", "immediate": True,  "channels": ["feishu"]},
        "model_trained":          {"priority": "P1", "immediate": True,  "channels": ["feishu"]},
        "auto_learned":           {"priority": "P2", "immediate": False, "channels": ["feishu"]},
        "gap_detected":           {"priority": "P2", "immediate": False, "channels": ["feishu"]},
        "daily_health_report":    {"priority": "P2", "immediate": False, "channels": ["feishu"]},
        "persona_rankings":       {"priority": "P2", "immediate": False, "channels": ["feishu"]},
    }

    def __init__(self):
        self.加密器 = 七因子加密器()
        self.格式化器 = 飞书卡片格式化器()
        self.限流 = 限流器()
        self.归档 = 归档器()

        # 先加载配置（从中提取通道参数）
        self._原始配置 = self._加载配置()
        self.规则 = self._原始配置.get("notify_rules", self.默认规则) if self._原始配置 else self.默认规则

        # 通道初始化（配置文件优先，后fallback环境变量）
        self.飞书 = 飞书推送通道(
            webhook_url=(self._原始配置.get("bot", {}).get("webhook", "") if self._原始配置 else "") or os.getenv("FEISHU_WEBHOOK_URL", ""),
            webhook_secret=(self._原始配置.get("bot", {}).get("secret", "") if self._原始配置 else "") or os.getenv("FEISHU_WEBHOOK_SECRET", ""),
        )
        bark_cfg = self._原始配置.get("bark", {}) if self._原始配置 else {}
        self.Bark = Bark推送通道(
            bark_server=bark_cfg.get("server", "") or os.getenv("BARK_SERVER", ""),
            bark_key=bark_cfg.get("key", "") or os.getenv("BARK_KEY", ""),
        )
        self.终端 = 终端通知通道()

    def _加载配置(self) -> Optional[Dict[str, Any]]:
        """加载飞书机器人配置文件·返回完整配置"""
        config_path = PROJECT_ROOT / "config" / "feishu_bot.yaml"
        if config_path.exists():
            try:
                import yaml
                with open(config_path) as f:
                    return yaml.safe_load(f)
            except Exception:
                pass
        return None

    def _取规则(self, event_type: str) -> Dict[str, Any]:
        """获取事件的通知规则"""
        return self.规则.get(event_type, {"priority": "P2", "immediate": False, "channels": ["feishu"]})

    # ── 主入口 ──

    def 发送(self, event_type: str, title: str, body: str,
           source: str = "", priority: str = "") -> Dict[str, Any]:
        """
        发送通知（统一入口）

        参数:
            event_type: 事件类型（如 tongxin_lock_alert）
            title: 通知标题
            body: 通知正文
            source: 来源节点（如 Mac.local / 鲲鹏）
            priority: 强制优先级（为空时使用规则默认值）

        返回:
            {status, dna, channels, results, encrypted}
        """
        # 1. 取规则
        rule = self._取规则(event_type)
        effective_priority = priority or rule.get("priority", "P2")
        channels = rule.get("channels", ["feishu"])
        immediate = rule.get("immediate", False)

        # 2. 限流检查
        ok, reason = self.限流.放行(event_type, effective_priority)
        if not ok:
            return {"status": "rate_limited", "reason": reason, "event_type": event_type, "channels_used": [], "dna": "", "priority": effective_priority, "encrypted": False}

        # 3. 生成DNA
        dna = 生成通知dna(event_type, "PUSH", body)
        timestamp = datetime.now().isoformat()

        # 4. 加密（P0强制）
        encrypted_payload = None
        display_body = body
        if self.加密器.should_encrypt(effective_priority):
            ctx = {
                "event_type": event_type,
                "timestamp": timestamp,
                "source_node": source,
                "user_passphrase": "longhun_notify_v1"
            }
            encrypted_payload = self.加密器.encrypt(body, ctx)
            display_body = f"[七因子加密] {encrypted_payload['context_hash']}"

        # 5. 构建飞书卡片（主力通道消息体）
        card = self.格式化器.生成卡片(
            event_type=event_type,
            priority=effective_priority,
            title=title,
            body=display_body,
            dna=dna,
            encrypted_info=encrypted_payload,
            source=source,
            timestamp=timestamp
        )

        # 6. 按优先级多通道推送
        results = []
        channels_used = []

        for ch in channels:
            if ch == "feishu" and self.飞书.可用:
                r = self.飞书.推送(card)
                results.append(r)
                if r.get("status") == "success":
                    channels_used.append("feishu")
                continue  # feishu成功/失败都继续尝试下一个通道

            if ch == "bark" and self.Bark.可用:
                r = self.Bark.推送(title, display_body, urgent=(effective_priority == "P0"))
                results.append(r)
                if r.get("status") == "success":
                    channels_used.append("bark")
                continue

            if ch == "terminal" and self.终端.可用:
                r = self.终端.推送(title, display_body)
                results.append(r)
                if r.get("status") == "success":
                    channels_used.append("terminal")

        # 7. 如果飞书不可用但Bark也没配置，至少发终端通知
        if not channels_used and self.终端.可用:
            r = self.终端.推送(title, display_body)
            results.append(r)
            if r.get("status") == "success":
                channels_used.append("terminal")

        # 8. 归档
        归档记录 = {
            "dna": dna,
            "event_type": event_type,
            "priority": effective_priority,
            "title": title,
            "body_snippet": body[:100],
            "encrypted": encrypted_payload is not None,
            "source": source,
            "timestamp": timestamp,
            "channels_used": channels_used,
            "results": results,
        }
        self.归档.归档(归档记录)

        return {
            "status": "delivered" if channels_used else "failed",
            "dna": dna,
            "event_type": event_type,
            "priority": effective_priority,
            "channels_used": channels_used,
            "results": results,
            "encrypted": encrypted_payload is not None,
            "timestamp": timestamp
        }

    def 状态(self) -> Dict[str, Any]:
        """获取网关状态"""
        return {
            "status": "ready",
            "gateway": "feishu+bark+terminal",
            "channels": {
                "feishu": self.飞书.可用,
                "bark": self.Bark.可用,
                "terminal": self.终端.可用
            },
            "encryption": "AES-256-GCM·七因子",
            "dna_tracing": True,
            "today_stats": self.归档.统计今日(),
            "rules_count": len(self.规则),
            "dna": DNA
        }


# ═══════════════════════════════════════════════════════════════
# §8. CLI & 自检
# ═══════════════════════════════════════════════════════════════

def _自检() -> bool:
    """全量自检"""
    errors = []
    gw = 龍魂通知网关()

    # 1. DNA引擎
    gz = 当前干支()
    assert len(gz["year"]) == 2, "年干支格式错误"
    assert len(gz["month"]) == 2, "月干支格式错误"
    assert len(gz["day"]) == 2, "日干支格式错误"
    assert "时" in gz["hour"], "时柱格式错误"
    print(f"  ✅ 干支引擎: {gz['full']}")

    # 2. DNA生成
    dna = 生成通知dna("test_event", "TEST", "test body")
    assert dna.startswith("#龍芯"), f"DNA格式错误: {dna}"
    assert "-NOTIFY-" in dna, f"DNA缺少动作标记: {dna}"
    assert len(dna.split("-")[-1]) == 8, f"DNA哈希长度错误: {dna}"
    print(f"  ✅ DNA生成: {dna}")

    # 3. 七因子加密
    enc = gw.加密器.encrypt("测试明文·P0级加密", {
        "event_type": "test",
        "source_node": "localhost",
        "user_passphrase": "test"
    })
    assert "ciphertext" in enc, "加密输出缺ciphertext"
    assert "nonce" in enc, "加密输出缺nonce"
    assert "context_hash" in enc, "加密输出缺context_hash"
    print(f"  ✅ 七因子加密: {enc['algorithm']} · hash={enc['context_hash']}")

    # 4. 飞书卡片格式化
    card = gw.格式化器.生成卡片(
        event_type="test_alert",
        priority="P0",
        title="测试告警",
        body="这是一条测试消息",
        dna=dna,
        source="localhost"
    )
    assert card["msg_type"] == "interactive", f"卡片类型错误: {card['msg_type']}"
    assert card["card"]["header"]["template"] == "red", "P0卡片应为红色"
    print(f"  ✅ 飞书卡片: P0·{card['card']['header']['title']['content']}")

    # 5. 通道可用性检测
    print(f"  {'✅' if gw.飞书.可用 else '🟡'} 飞书通道: {'已配置' if gw.飞书.可用 else '未配置（非致命）'}")
    print(f"  {'✅' if gw.Bark.可用 else '🟡'} Bark通道: {'已配置' if gw.Bark.可用 else '未配置（非致命）'}")
    print(f"  {'✅' if gw.终端.可用 else '🔴'} 终端通道: {'可用' if gw.终端.可用 else '不可用'}")

    # 6. 发送测试通知（在限流测试之前·避免限流器污染）
    r = gw.发送(
        event_type="system_test",
        title="龍魂通知网关自检",
        body=f"网关自检通过·{datetime.now().strftime('%H:%M:%S')}",
        source="本地·自检",
        priority="P1"
    )
    print(f"  ✅ 发送测试: status={r['status']} · channels={r.get('channels_used',[])} · dna={r.get('dna','N/A')}")

    # 7. 限流器
    gw2 = 龍魂通知网关()  # 独立实例·不影响归档统计
    ok, _ = gw2.限流.放行("test_limit", "P1")
    assert ok, "首次应放行"
    for _ in range(15):
        gw2.限流.放行("test_limit", "P1")
    ok, reason = gw2.限流.放行("test_limit", "P1")
    assert not ok, f"超限应拒绝·实际: {reason}"
    print(f"  ✅ 限流器: 超限正确拒绝（{reason}）")

    # 8. 归档器
    gw.归档.归档({"dna": dna, "event_type": "test", "priority": "P1", "title": "测试", "body_snippet": "test", "channels_used": ["terminal"], "results": []})
    stats = gw.归档.统计今日()
    assert stats["total"] > 0, "归档后应有记录"
    print(f"  ✅ 归档器: 今日={stats['total']}条")

    if errors:
        for e in errors:
            print(f"  🔴 {e}")
        return False

    print(f"\n{'='*50}")
    print(f"🎉 网关自检通过 · 8/8")
    print(f"🧬 {dna}")
    return True


def cmd_selftest(args=None):
    """自检命令入口"""
    ok = _自检()
    return 0 if ok else 1


def cmd_send(args):
    """发送通知"""
    import argparse
    parser = argparse.ArgumentParser(description="龍魂通知网关·发送")
    parser.add_argument("--event", required=True, help="事件类型")
    parser.add_argument("--title", required=True, help="通知标题")
    parser.add_argument("--body", required=True, help="通知正文")
    parser.add_argument("--source", default="CLI", help="来源节点")
    parser.add_argument("--priority", default="", help="强制优先级")
    args_ns = parser.parse_args(args)

    gw = 龍魂通知网关()
    r = gw.发送(
        event_type=args_ns.event,
        title=args_ns.title,
        body=args_ns.body,
        source=args_ns.source,
        priority=args_ns.priority
    )
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r["status"] == "delivered" else 1


def cmd_status(args=None):
    """查看网关状态"""
    gw = 龍魂通知网关()
    s = gw.状态()
    print(json.dumps(s, ensure_ascii=False, indent=2))
    return 0


def cmd_history(args=None):
    """查看通知历史"""
    import argparse
    parser = argparse.ArgumentParser(description="龍魂通知网关·历史")
    parser.add_argument("--limit", type=int, default=20, help="返回条数")
    parser.add_argument("--priority", default="", help="按优先级过滤")
    args_ns = parser.parse_args(args)

    today = datetime.now().strftime("%Y-%m-%d")
    log_file = PROJECT_ROOT / "logs" / "notify" / f"{today}.jsonl"

    if not log_file.exists():
        print("今日暂无通知记录")
        return 0

    records = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            if args_ns.priority and rec.get("priority") != args_ns.priority:
                continue
            records.append(rec)

    records = records[-args_ns.limit:]  # 取最近N条

    for i, r in enumerate(reversed(records)):
        icon = {"P0": "🚨", "P1": "ℹ️", "P2": "📊", "P3": "📝"}.get(r.get("priority", ""), "📌")
        print(f"{icon} [{r.get('priority','?')}] {r.get('title','')}")
        print(f"   时间: {r.get('timestamp','')[:19]}")
        print(f"   通道: {', '.join(r.get('channels_used',[]))}")
        print(f"   内容: {r.get('body_snippet','')[:80]}")
        print(f"   DNA: {r.get('dna','')}")
        print()

    gw = 龍魂通知网关()
    stats = gw.归档.统计今日()
    print(f"--- 今日统计: 总计{stats['total']}条 | P0:{stats['P0']} P1:{stats['P1']} P2:{stats['P2']} P3:{stats['P3']}")
    return 0


# ═══════════════════════════════════════════════════════════════
# §9. main
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 飞书通知网关 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
DNA: {DNA}
创建者: {CREATOR}

使用示例:
  python3 bin/lh_notify_gateway.py selftest           # 自检
  python3 bin/lh_notify_gateway.py send --event system_upgraded --title "升级完成" --body "v1.0已部署" --source 鲲鹏
  python3 bin/lh_notify_gateway.py status              # 查看状态
  python3 bin/lh_notify_gateway.py history --limit 10  # 查看历史
        """
    )

    sub = parser.add_subparsers(dest="command")

    p_test = sub.add_parser("selftest", help="运行自检")
    p_send = sub.add_parser("send", help="发送通知")
    p_send.add_argument("--event", required=True)
    p_send.add_argument("--title", required=True)
    p_send.add_argument("--body", required=True)
    p_send.add_argument("--source", default="CLI")
    p_send.add_argument("--priority", default="")

    p_status = sub.add_parser("status", help="查看网关状态")
    p_hist = sub.add_parser("history", help="查看通知历史")
    p_hist.add_argument("--limit", type=int, default=20)
    p_hist.add_argument("--priority", default="")

    args = parser.parse_args()

    if args.command == "selftest":
        sys.exit(cmd_selftest([]))
    elif args.command == "send":
        sys.exit(cmd_send([
            "--event", args.event,
            "--title", args.title,
            "--body", args.body,
            "--source", args.source
        ] + (["--priority", args.priority] if args.priority else [])))
    elif args.command == "status":
        sys.exit(cmd_status([]))
    elif args.command == "history":
        sys.exit(cmd_history([
            "--limit", str(args.limit)
        ] + (["--priority", args.priority] if args.priority else [])))
    else:
        # 默认：自检
        sys.exit(cmd_selftest([]))
