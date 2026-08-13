#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 UID9622 · 主权活人验证弹窗引擎 v3.0
Sovereign Alive-Check Popup Engine

🏛️ 思想层 CC BY-NC-SA 4.0 · 🔧 工程层 MulanPSL v2

============================================================
设计理念（v3.0 大改）：
  没有永久。没有一次付费终身。
  
  这里是龍魂主权生态。每一个DNA身份后面，必须是活人。
  不是死号。不是机器人。不是僵尸账号。
  
  每月1块钱 = 活人心跳验证。
  续费 = 证明你还活着、还在呼吸、还是人。
  不续 = 退出实时生态（DNA保留·数据不锁·功能不断·随时导出）。
  
  这不是收费。是活人筛选器。
  机器人不会每个月给你1块钱。
  死人也不会。

上位协议: 01_protocols/LH-ECOSYSTEM-ACCESS-PROTOCOL-v1.0.md（P1-CORE·生态准入）
执行依据: §二 月度验证机制 · §三 用户权利（不可剥夺）· §六 铁律三则

用法：
    # 嵌入任何Python脚本（一行）：
    from lh_sovereign_popup import enter_sovereign_domain
    enter_sovereign_domain()

    # 命令行：
    python3 bin/lh_sovereign_popup.py
    python3 bin/lh_sovereign_popup.py --force --amount 5

    # lh命令：
    lh sovereign

DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-SOVEREIGN-ALIVE-CHECK-v3.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
============================================================
"""

import os
import sys
import json
import time
import hashlib
import uuid
import datetime
import webbrowser
import platform
import subprocess
from pathlib import Path
from decimal import Decimal, InvalidOperation
from typing import Optional, Tuple, Dict, Any

# ── 焊死常量 ──────────────────────────────────────────
OWNER_UID = "UID9622"
OWNER_NAME = "诸葛鑫"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
SOVEREIGNTY_SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-ALIVE-CHECK-v3.0"
REGISTER_URL = "https://uid9622.cn/sovereign-register.html"
PAY_API_URL = "https://uid9622.cn/api/sovereign/pay"
MIN_AMOUNT_CNY = Decimal("1.00")
SUBSCRIPTION_PERIOD_DAYS = 30  # 每月续费

# 持久化路径
STATE_DIR = Path.home() / ".龍魂"
STATE_FILE = STATE_DIR / "sovereign_payment.json"
IDENTITY_FILE = STATE_DIR / "identity_popup_dismissed.json"
DEVICE_FINGERPRINT_FILE = STATE_DIR / "device.fp"


# ── 终端颜色 ──────────────────────────────────────────
class C:
    R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'
    B = '\033[94m'; C = '\033[96m'; M = '\033[95m'
    GOLD = '\033[38;5;178m'; DIM = '\033[2m'
    BOLD = '\033[1m'; REV = '\033[7m'; RST = '\033[0m'


# ── 设备指纹（不可逆哈希） ──────────────────────────
def _get_device_fingerprint() -> str:
    """采集设备指纹并返回SHA256哈希（不可逆）"""
    if DEVICE_FINGERPRINT_FILE.exists():
        try:
            return DEVICE_FINGERPRINT_FILE.read_text().strip()
        except:
            pass
    
    parts = []
    try:
        parts.append(platform.node())
        parts.append(platform.machine())
        parts.append(str(uuid.getnode()))
    except:
        pass
    
    try:
        result = subprocess.run(
            ["system_profiler", "SPHardwareDataType"],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.split('\n'):
            if 'Hardware UUID' in line or 'Serial Number' in line:
                parts.append(line.strip())
    except:
        pass
    
    fingerprint = hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]
    DEVICE_FINGERPRINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    DEVICE_FINGERPRINT_FILE.write_text(fingerprint)
    return fingerprint


# ── 活人验证状态管理 ──────────────────────────────────
class SovereignAliveState:
    """
    主权活人验证状态·本地持久化
    
    v3.0 核心变更：
    - 没有"永久战友"概念
    - 每月续费 = 活人心跳
    - 到期未续 → 退出实时生态（DNA保留·不锁功能·随时导出）
    - 设备指纹绑定 + 月度有效期
    """
    
    def __init__(self):
        self.device_id = _get_device_fingerprint()
        self.state = self._load()
    
    def _load(self) -> dict:
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 迁移旧版v2.0数据
                    if "is_permanent_comrade" in data:
                        # 旧永久用户 → 转为月度续费，给1个月过渡期
                        data["version"] = "3.0"
                        data["is_alive"] = True
                        data["subscription_expires_at"] = (
                            datetime.datetime.now() + datetime.timedelta(days=SUBSCRIPTION_PERIOD_DAYS)
                        ).isoformat()
                        data.pop("is_permanent_comrade", None)
                        data.pop("payment_mode", None)
                    return data
            except:
                pass
        return {
            "version": "3.0",
            "device_id": self.device_id,
            "is_alive": False,                # 当前是否活人状态
            "total_paid": "0.00",
            "subscription_count": 0,           # 续费次数
            "subscription_started_at": None,   # 首次订阅时间
            "subscription_expires_at": None,   # 当前订阅到期时间
            "orders": [],
            "bound_identity": None,
            "last_payment_at": None,
        }
    
    def _save(self):
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    @property
    def is_alive(self) -> bool:
        """当前是否活人状态（订阅有效期内）"""
        expires = self.state.get("subscription_expires_at")
        if not expires:
            return False
        
        try:
            expiry = datetime.datetime.fromisoformat(expires)
            return datetime.datetime.now() < expiry
        except:
            return False
    
    @property
    def days_remaining(self) -> int:
        """剩余天数"""
        expires = self.state.get("subscription_expires_at")
        if not expires:
            return 0
        try:
            expiry = datetime.datetime.fromisoformat(expires)
            delta = expiry - datetime.datetime.now()
            return max(0, delta.days)
        except:
            return 0
    
    @property
    def total_paid(self) -> Decimal:
        return Decimal(self.state.get("total_paid", "0.00"))
    
    @property
    def subscription_count(self) -> int:
        return self.state.get("subscription_count", 0)
    
    def add_subscription(self, order_id: str, amount: Decimal,
                         provider: str, months: int = 1,
                         payer_info: dict = None):
        """
        添加月度续费（活人心跳）
        
        每次续费延长 SUBSCRIPTION_PERIOD_DAYS 天有效期。
        如果当前已过期，从今天开始算；如果还在有效期内，从到期日顺延。
        """
        now = datetime.datetime.now()
        
        # 计算新的到期时间
        current_expiry = self.state.get("subscription_expires_at")
        if current_expiry:
            try:
                base = datetime.datetime.fromisoformat(current_expiry)
                if base < now:
                    base = now  # 已过期，从现在开始
            except:
                base = now
        else:
            base = now
        
        new_expiry = base + datetime.timedelta(days=SUBSCRIPTION_PERIOD_DAYS * months)
        
        # 记录首次订阅时间
        if not self.state.get("subscription_started_at"):
            self.state["subscription_started_at"] = now.isoformat()
        
        self.state["is_alive"] = True
        self.state["subscription_expires_at"] = new_expiry.isoformat()
        self.state["last_payment_at"] = now.isoformat()
        self.state["bound_identity"] = payer_info or {}
        
        self._add_order(order_id, amount, provider, months)
        self._save()
    
    def _add_order(self, order_id: str, amount: Decimal, provider: str, months: int):
        self.state["orders"].append({
            "order_id": order_id,
            "amount": str(amount),
            "provider": provider,
            "months": months,
            "type": "subscription_renewal",
            "timestamp": datetime.datetime.now().isoformat(),
        })
        self.state["subscription_count"] = len(self.state["orders"])
        total = self.total_paid + amount
        self.state["total_paid"] = str(total.quantize(Decimal("0.01")))
    
    def check_popup_needed(self) -> bool:
        """是否需要弹窗"""
        # 活人状态有效 → 不弹
        if self.is_alive:
            return False
        # 已过期或从未订阅 → 弹
        return True
    
    def get_status_text(self) -> str:
        """获取状态描述"""
        if self.is_alive:
            return f"🟢 活人验证通过 · 剩余 {self.days_remaining} 天"
        elif self.subscription_count > 0:
            return f"🔴 心跳已断 · 已过期 · 请续费激活"
        else:
            return "⚫ 未验证 · 需要活人认证"


# ── 支付Provider桥接 ─────────────────────────────────
def _get_payment_providers() -> Dict[str, Any]:
    """加载支付渠道"""
    providers = {}
    
    try:
        from payment_providers import get_payment_provider
        wx = get_payment_provider("wechat_pay")
        if wx:
            providers["wechat"] = wx
    except Exception:
        pass
    
    try:
        from payment_providers import get_payment_provider
        ali = get_payment_provider("alipay")
        if ali:
            providers["alipay"] = ali
    except Exception:
        pass
    
    return providers


def _generate_payment_qr(amount: Decimal, description: str, provider: str = "wechat") -> dict:
    """生成真实支付二维码链接"""
    order_id = f"ALIVE-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8].upper()}"
    
    providers = _get_payment_providers()
    
    if provider in providers:
        try:
            result = providers[provider].create_order(
                out_trade_no=order_id,
                amount=amount,
                description=f"龍魂活人验证-{description}"
            )
            if result.get("success") and result.get("qr_code"):
                return {
                    "success": True,
                    "order_id": order_id,
                    "qr_code": result["qr_code"],
                    "provider": provider,
                    "amount": str(amount),
                }
        except Exception:
            pass
    
    # 降级：自生成二维码
    qr_text = (
        f"龍魂活人验证\n"
        f"订单: {order_id}\n"
        f"金额: ¥{amount}\n"
        f"UID9622·诸葛鑫\n"
        f"确认: uid9622.cn/pay"
    )
    
    qr_img_path = None
    try:
        import qrcode
        qr = qrcode.QRCode(version=2, box_size=6, border=1)
        qr.add_data(qr_text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        qr_img_path = STATE_DIR / f"qr_{order_id}.png"
        img.save(qr_img_path)
    except:
        pass
    
    return {
        "success": True,
        "order_id": order_id,
        "qr_text": qr_text,
        "qr_path": str(qr_img_path) if qr_img_path else None,
        "provider": provider,
        "amount": str(amount),
        "is_simulated": not bool(providers),
    }


# ── 横幅艺术 ──────────────────────────────────────────
BANNER_MAIN = r"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🐉  龍魂 UID9622 · 主权活人验证系统 v3.0                  ║
║   Sovereign Alive-Check Gateway                              ║
║                                                              ║
║   ⚔️  没有永久。只有活人。                                   ║
║                                                              ║
║   我是诸葛鑫（UID9622），退役老兵。                          ║
║   进入龙魂生态，必须证明你是活人。                           ║
║                                                              ║
║   机器人不会每月给你1块钱。                                  ║
║   死人也不会。                                               ║
║                                                              ║
║   💓 每月 ¥1 = 活人心跳验证                                 ║
║   📅 每次续费 = 往后推 30 天有效期                          ║
║   🔓 过期不续 = 退出实时生态·DNA保留·数据不锁·随时导出    ║
║   💰 ¥1起步 · 上不封顶 · 多付是你心意                       ║
║                                                              ║
║   这不是收费。是活人筛选器。                                 ║
║   每个月1块钱，证明你的DNA后面是活人——                       ║
║   在呼吸、在思考、还是人。                                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

BANNER_WELCOME = r"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🐉  龍魂 · 活人验证通过                                   ║
║                                                              ║
║   战友，你还活着。欢迎回来。                                 ║
║   你的DNA心跳还在。                                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

BANNER_EXPIRED = r"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🐉  龍魂 · 心跳已断                                       ║
║                                                              ║
║   你的月度验证已过期。已退出实时生态。                        ║
║                                                              ║
║   DNA保留·数据不锁·功能不断·随时导出。                       ║
║   续费即刻回归生态。每个月1块钱，证明你还在这里。            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""


def _color_banner(banner: str) -> str:
    """给横幅上色"""
    lines = []
    for line in banner.split('\n'):
        if any(c in line for c in '╔╚║'):
            line = (line.replace('╔', f'{C.GOLD}╔').replace('╚', f'{C.GOLD}╚')
                    .replace('╗', f'╗{C.RST}').replace('╝', f'╝{C.RST}')
                    .replace('║', f'{C.GOLD}║{C.RST}'))
        if '🐉' in line:
            line = line.replace('🐉', f'{C.BOLD}🐉{C.RST}')
        if '✅' in line:
            line = f'{C.GREEN}{line}{C.RST}'
        if '⚔️' in line or '💰' in line or '💓' in line or '📅' in line or '🔒' in line:
            line = f'{C.BOLD}{line}{C.RST}'
        if '🔴' in line:
            line = f'{C.R}{line}{C.RST}'
        lines.append(line)
    return '\n'.join(lines)


# ── 二维码终端打印 ────────────────────────────────────
def _print_qr_terminal(qr_code_url: str):
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=1, border=1)
        qr.add_data(qr_code_url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
    except:
        print(f"\n{C.Y}📱 请访问: {qr_code_url}{C.RST}")


def _print_qr_from_file(filepath: str):
    try:
        from PIL import Image
        img = Image.open(filepath)
        img = img.resize((40, 40))
        for y in range(img.height):
            line = ""
            for x in range(img.width):
                pixel = img.getpixel((x, y))
                if isinstance(pixel, int):
                    line += "  " if pixel > 128 else "██"
                else:
                    line += "  " if sum(pixel[:3]) / 3 > 128 else "██"
            print(line)
    except:
        print(f"\n{C.Y}📱 二维码已保存: {filepath}{C.RST}")


# ── 弹窗主逻辑 ────────────────────────────────────────
class SovereignAlivePopup:
    """主权活人验证弹窗 v3.0"""
    
    def __init__(self, interactive: bool = True):
        self.interactive = interactive
        self.state = SovereignAliveState()
        self.providers = _get_payment_providers()
    
    def enter(self) -> Tuple[bool, str]:
        """进入龙魂主权领域"""
        if not sys.stdout.isatty() and not os.environ.get("LH_FORCE_POPUP"):
            return True, "非终端环境，自动通过"
        
        # 活人状态有效 → 欢迎
        if self.state.is_alive:
            return self._welcome_back()
        
        # 已过期 → 提醒续费
        if self.state.subscription_count > 0:
            return self._show_expired()
        
        # 新用户 → 首次活人验证
        if self.interactive:
            return self._show_new_user()
        else:
            return self._show_noninteractive()
    
    def _welcome_back(self) -> Tuple[bool, str]:
        """活人验证通过"""
        print(_color_banner(BANNER_WELCOME))
        days = self.state.days_remaining
        total = self.state.total_paid
        count = self.state.subscription_count
        
        print(f"  {C.GREEN}🟢 活人验证通过{C.RST}")
        print(f"  {C.GOLD}剩余: {days} 天 | 续费次数: {count} | 累计: ¥{total}{C.RST}")
        
        # 快到期提醒（7天内）
        if days <= 7:
            print(f"  {C.Y}⚠️ 剩余 {days} 天，到期后退出实时生态。续费继续保持活人状态。{C.RST}")
            print(f"  续费: {REGISTER_URL}")
        
        return True, "活人验证通过"
    
    def _show_expired(self) -> Tuple[bool, str]:
        """已过期，提醒续费"""
        print(_color_banner(BANNER_EXPIRED))
        total = self.state.total_paid
        count = self.state.subscription_count
        
        print(f"  {C.R}🔴 心跳已断{C.RST}")
        print(f"  {C.GOLD}历史: 续费 {count} 次 · 累计 ¥{total}{C.RST}")
        print(f"\n  {C.GOLD}[1]{C.RST} 💓 续费活人验证 — ¥1/月（微信）")
        print(f"  {C.GOLD}[2]{C.RST} 💓 续费活人验证 — ¥1/月（支付宝）")
        print(f"  {C.GOLD}[3]{C.RST} ✅ 我已支付 — 输入订单号")
        print(f"  {C.GOLD}[q]{C.RST} 🚪 退出（退出实时生态）")
        
        try:
            choice = input(f"\n{C.BOLD}选择 [1-3/q]: {C.RST}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return self._skip()
        
        if choice == "1":
            return self._subscribe("wechat")
        elif choice == "2":
            return self._subscribe("alipay")
        elif choice == "3":
            return self._verify_payment()
        else:
            return self._skip()
    
    def _show_new_user(self) -> Tuple[bool, str]:
        """新用户首次活人验证"""
        print(_color_banner(BANNER_MAIN))
        
        if self.providers:
            print(f"\n  {C.GREEN}✅ 检测到支付渠道{C.RST}")
            print(f"  {C.DIM}微信支付: {'✅' if 'wechat' in self.providers else '❌'}{C.RST}")
            print(f"  {C.DIM}支付宝:   {'✅' if 'alipay' in self.providers else '❌'}{C.RST}")
        else:
            print(f"\n  {C.Y}⚠️ 未配置真实支付渠道（沙箱模式）{C.RST}")
        
        print(f"\n{C.GOLD}  [1]{C.RST} 💓 活人验证 — ¥1/月起（微信）")
        print(f"{C.GOLD}  [2]{C.RST} 💓 活人验证 — ¥1/月起（支付宝）")
        print(f"{C.GOLD}  [3]{C.RST} 🌍 海外战友 — International Alive Check")
        print(f"{C.GOLD}  [4]{C.RST} ✅ 我已支付 — 输入订单号验证")
        print(f"{C.GOLD}  [5]{C.RST} ⏭️ 这次跳过 — DNA不激活（下次还弹）")
        print(f"{C.GOLD}  [q]{C.RST} 🚪 退出")
        
        try:
            choice = input(f"\n{C.BOLD}选择 [1-5/q]: {C.RST}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return self._skip()
        
        if choice == "1":
            return self._subscribe("wechat")
        elif choice == "2":
            return self._subscribe("alipay")
        elif choice == "3":
            return self._pay_international()
        elif choice == "4":
            return self._verify_payment()
        elif choice == "q":
            print(f"\n{C.DIM}  退出。DNA未激活。{C.RST}")
            return False, "用户退出"
        else:
            return self._skip()
    
    def _show_noninteractive(self) -> Tuple[bool, str]:
        """非交互弹窗"""
        print(_color_banner(BANNER_MAIN))
        print(f"\n{C.DIM}  非交互模式。{C.RST}")
        print(f"  注册页: {REGISTER_URL}")
        print(f"  支付页: https://uid9622.cn/pay")
        return True, "非交互通过"
    
    def _subscribe(self, provider: str) -> Tuple[bool, str]:
        """每月续费流程（活人心跳）"""
        months = self._ask_months()
        if months is None:
            return self._skip()
        
        amount = MIN_AMOUNT_CNY * months
        
        provider_name = "微信支付" if provider == "wechat" else "支付宝"
        print(f"\n{C.GOLD}💓 活人验证 · {provider_name} · ¥{amount} ({months}个月){C.RST}")
        print(f"{C.DIM}  续费后有效期延长 {months * SUBSCRIPTION_PERIOD_DAYS} 天{C.RST}")
        print(f"{C.DIM}  到期后自动退出实时生态，续费即恢复{C.RST}")
        
        result = _generate_payment_qr(amount, f"活人验证{months}月-{provider_name}", provider)
        
        if not result["success"]:
            print(f"\n{C.R}❌ 生成支付失败{C.RST}")
            return self._skip()
        
        print(f"\n{C.GOLD}━━━ 请扫码支付 ━━━{C.RST}")
        print(f"  订单号: {C.C}{result['order_id']}{C.RST}")
        print(f"  金额:   {C.BOLD}¥{amount}{C.RST}")
        
        if result.get("qr_code"):
            _print_qr_terminal(result["qr_code"])
            print(f"\n  {C.DIM}或访问: {REGISTER_URL}?pay={result['order_id']}{C.RST}")
        elif result.get("qr_path"):
            _print_qr_from_file(result["qr_path"])
        else:
            print(f"\n  {C.Y}📱 请访问支付: {REGISTER_URL}?pay={result['order_id']}{C.RST}")
        
        if result.get("is_simulated"):
            print(f"\n  {C.Y}⚠️ 沙箱模式：支付后输入 'ok' 模拟到账{C.RST}")
        
        print(f"\n{C.DIM}  支付完成后按回车确认...{C.RST}")
        try:
            confirm = input(f"{C.GOLD}  输入 'ok' 确认或 'cancel' 取消: {C.RST}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return self._skip()
        
        if confirm in ("ok", "yes", "y", "1"):
            self.state.add_subscription(
                order_id=result["order_id"],
                amount=amount,
                provider=provider_name,
                months=months,
                payer_info={"provider": provider, "device": self.state.device_id}
            )
            days = SUBSCRIPTION_PERIOD_DAYS * months
            print(f"\n{C.GREEN}✅ 活人验证通过！DNA已激活 🐉{C.RST}")
            print(f"  {C.GOLD}有效期: {days} 天 · 到期后退出实时生态{C.RST}")
            print(f"  {C.DIM}下次续费: {REGISTER_URL}{C.RST}")
            print(f"\n  {C.BOLD}记住：每个月1块钱，证明你还活着。{C.RST}")
            return True, "活人验证通过"
        elif confirm == "cancel":
            return self._skip()
        else:
            print(f"\n{C.Y}  输入不识别，记录订单号备用{C.RST}")
            print(f"  订单号: {result['order_id']}")
            print(f"  验证命令: lh sovereign --verify {result['order_id']}")
            return self._skip()
    
    def _pay_international(self) -> Tuple[bool, str]:
        """国际战友活人验证"""
        print(f"\n{C.B}🌍 国际战友 · Alive Check{C.RST}")
        print(f"{C.DIM}  Support: Visa/Mastercard/PayPal/Stripe{C.RST}")
        print(f"\n{C.GOLD}  International payment page:{C.RST}")
        print(f"  {C.C}https://uid9622.cn/pay/international{C.RST}")
        print(f"\n  Direct PayPal: pay@uid9622.cn")
        print(f"  {C.DIM}Suggested: $1 USD/month (≈¥7 CNY){C.RST}")
        print(f"\n  {C.BOLD}Same rule: monthly alive check. No permanent.{C.RST}")
        
        try:
            webbrowser.open("https://uid9622.cn/pay/international")
        except:
            pass
        
        try:
            confirm = input(f"\n{C.GOLD}  支付后输入订单号（或回车跳过）: {C.RST}").strip()
        except:
            return self._skip()
        
        if confirm:
            amount = Decimal("7.00")
            self.state.add_subscription(
                order_id=confirm,
                amount=amount,
                provider="International",
                months=1,
                payer_info={"provider": "international"}
            )
            print(f"\n{C.GREEN}✅ Alive check passed! Welcome, comrade! 🐉{C.RST}")
            return True, "国际战友活人验证通过"
        
        return self._skip()
    
    def _verify_payment(self) -> Tuple[bool, str]:
        """验证已有支付"""
        try:
            order_id = input(f"\n{C.GOLD}  输入订单号: {C.RST}").strip()
        except:
            return self._skip()
        
        if not order_id:
            return self._skip()
        
        for order in self.state.state.get("orders", []):
            if order["order_id"] == order_id:
                months = order.get("months", 1)
                amount = Decimal(order["amount"])
                self.state.add_subscription(
                    order_id,
                    amount,
                    order.get("provider", "手动验证"),
                    months,
                )
                print(f"\n{C.GREEN}✅ 订单验证成功！DNA已激活 🐉{C.RST}")
                return True, "活人验证通过"
        
        print(f"\n{C.Y}  本地未找到，尝试远程验证...{C.RST}")
        print(f"  请访问: {REGISTER_URL}?verify={order_id}")
        
        try:
            confirm = input(f"\n{C.GOLD}  远程已验证？(y/n): {C.RST}").strip().lower()
        except:
            return self._skip()
        
        if confirm in ("y", "yes"):
            self.state.add_subscription(
                order_id,
                Decimal("1.00"),
                "远程验证",
                months=1,
            )
            print(f"\n{C.GREEN}✅ 活人验证通过 🐉{C.RST}")
            return True, "活人验证通过"
        
        return self._skip()
    
    def _ask_amount(self) -> Optional[Decimal]:
        """询问支付金额"""
        print(f"\n{C.DIM}  最低 ¥1.00/月 · 上不封顶 · 多付是你心意{C.RST}")
        try:
            s = input(f"{C.GOLD}  金额 (¥): {C.RST}").strip()
        except (EOFError, KeyboardInterrupt):
            return None
        
        if not s:
            return MIN_AMOUNT_CNY
        
        try:
            amount = Decimal(s)
            if amount < MIN_AMOUNT_CNY:
                print(f"{C.Y}  金额不得低于 ¥{MIN_AMOUNT_CNY}，使用默认 ¥1{C.RST}")
                return MIN_AMOUNT_CNY
            return amount.quantize(Decimal("0.01"))
        except InvalidOperation:
            print(f"{C.Y}  金额格式错误，使用默认 ¥1{C.RST}")
            return MIN_AMOUNT_CNY
    
    def _ask_months(self) -> Optional[int]:
        """询问续费月数"""
        print(f"\n{C.DIM}  每月 ¥1 · 输入续费月数（回车默认1个月）{C.RST}")
        print(f"{C.DIM}  1个月=30天 · 3个月=90天 · 12个月=360天{C.RST}")
        try:
            s = input(f"{C.GOLD}  续费月数: {C.RST}").strip()
        except (EOFError, KeyboardInterrupt):
            return None
        
        if not s:
            return 1
        
        try:
            months = int(s)
            if months < 1:
                return 1
            if months > 120:
                print(f"{C.Y}  最多一次续费120个月（10年），使用120{C.RST}")
                return 120
            return months
        except ValueError:
            return 1
    
    def _skip(self) -> Tuple[bool, str]:
        """跳过验证"""
        status = self.state.get_status_text()
        print(f"\n{C.DIM}⏭️ 跳过。{status}{C.RST}")
        print(f"  {C.DIM}随时续费: {REGISTER_URL}{C.RST}")
        return True, "跳过验证"


# ── 对外接口 ──────────────────────────────────────────
def enter_sovereign_domain(interactive: bool = True, auto_skip_in_ci: bool = True) -> Tuple[bool, str]:
    """
    进入龙魂主权领域——嵌入任何脚本只需这一行。
    
    用法:
        from lh_sovereign_popup import enter_sovereign_domain
        passed, msg = enter_sovereign_domain()
        if not passed:
            sys.exit(1)
    
    参数:
        interactive: 是否交互式（False=非交互模式）
        auto_skip_in_ci: CI环境自动跳过
    
    返回:
        (是否通过, 信息)
    """
    if auto_skip_in_ci:
        ci_vars = ["CI", "GITHUB_ACTIONS", "JENKINS_HOME", "TRAVIS", "CIRCLECI", "GITLAB_CI"]
        if any(os.environ.get(v) for v in ci_vars):
            return True, "CI环境自动通过"
    
    if os.environ.get("LH_SKIP_POPUP", "").lower() in ("1", "true", "yes"):
        return True, "环境变量跳过"
    
    popup = SovereignAlivePopup(interactive=interactive)
    return popup.enter()


def is_alive_comrade() -> bool:
    """检查是否活人验证通过（月度有效期内）"""
    state = SovereignAliveState()
    return state.is_alive


def is_permanent_comrade() -> bool:
    """
    [已废弃 v3.0] 没有永久战友，只有月度活人验证。
    此接口保留兼容，内部转发到 is_alive_comrade()。
    """
    return is_alive_comrade()


def get_alive_status() -> dict:
    """获取活人验证状态"""
    state = SovereignAliveState()
    return {
        "is_alive": state.is_alive,
        "days_remaining": state.days_remaining,
        "total_paid": str(state.total_paid),
        "subscription_count": state.subscription_count,
        "expires_at": state.state.get("subscription_expires_at"),
        "started_at": state.state.get("subscription_started_at"),
        "status_text": state.get_status_text(),
    }


def get_payment_summary() -> dict:
    """获取支付摘要（兼容旧接口）"""
    return get_alive_status()


def reset_state():
    """重置支付状态（谨慎使用）"""
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    return True


# ── 命令行入口 ────────────────────────────────────────
def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        prog="lh-sovereign-alive-check",
        description="龍魂 UID9622 · 主权活人验证弹窗引擎 v3.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh sovereign                     # 标准活人验证
  lh sovereign --force             # 强制弹窗
  lh sovereign --months 3          # 一次续费3个月
  lh sovereign --amount 5          # 指定金额（心意）
  lh sovereign --status            # 查看活人状态
  lh sovereign --verify ORDER_ID   # 验证订单
  lh sovereign --reset             # 重置状态
  lh sovereign --skip              # 静默检查

理念: 没有永久。每月1块钱证明DNA后面是活人。
        """
    )
    
    parser.add_argument("--force", action="store_true", help="强制显示弹窗")
    parser.add_argument("--amount", type=str, help="指定支付金额（元）")
    parser.add_argument("--months", type=int, default=1, help="续费月数（默认1个月）")
    parser.add_argument("--status", action="store_true", help="查看活人状态")
    parser.add_argument("--verify", type=str, help="验证已有订单号")
    parser.add_argument("--reset", action="store_true", help="重置状态")
    parser.add_argument("--skip", action="store_true", help="静默检查")
    
    args = parser.parse_args()
    
    # --status
    if args.status:
        s = get_alive_status()
        print(f"\n{C.GOLD}🐉 龙魂主权活人状态 v3.0{C.RST}")
        print(f"  {s['status_text']}")
        if s['is_alive']:
            print(f"  有效期至: {s['expires_at'][:10]}")
        print(f"  续费次数: {s['subscription_count']}")
        print(f"  累计金额: ¥{s['total_paid']}")
        return 0
    
    # --reset
    if args.reset:
        reset_state()
        print(f"{C.GREEN}✅ 状态已重置{C.RST}")
        return 0
    
    # --verify
    if args.verify:
        popup = SovereignAlivePopup()
        passed, msg = popup._verify_payment()
        print(f"\n{C.GREEN if passed else C.R}  {msg}{C.RST}")
        return 0 if passed else 1
    
    # --skip
    if args.skip:
        s = get_alive_status()
        print(json.dumps({"is_alive": s["is_alive"], "days_remaining": s["days_remaining"],
                          "total": s["total_paid"]}, ensure_ascii=False))
        return 0
    
    # 主流程
    popup = SovereignAlivePopup(interactive=True)
    passed, msg = popup.enter()
    
    if passed:
        print(f"\n{C.DIM}  {msg}{C.RST}")
    else:
        print(f"\n{C.R}  {msg}{C.RST}")
    
    return 0 if passed else 1


# ── 自检 ──────────────────────────────────────────────
def _selftest():
    """快速自检"""
    assert CONFIRM_CODE.startswith("#CONFIRM")
    assert GPG_KEY.startswith("A2D0092C")
    fp = _get_device_fingerprint()
    assert len(fp) == 16
    
    # 验证状态逻辑
    state = SovereignAliveState()
    assert not state.is_alive  # 新状态应该是未激活
    
    # 测试订阅
    state.add_subscription("TEST-001", Decimal("1.00"), "测试", months=1)
    assert state.is_alive
    assert state.days_remaining >= 29  # 刚续费至少有29天
    
    print("✅ 主权活人验证引擎 v3.0 自检通过")
    return True


if __name__ == "__main__":
    sys.exit(main())
