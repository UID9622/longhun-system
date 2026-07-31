# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂人民权益守门人 / LongHun People's Rights Guard

DNA:#龍芯⚡️2026-06-21-PEOPLE-RIGHTS-GUARD-v1.0

焊死原则：
  ① 人民是用来爱的，不是用来收割的。
  ② 数据主权在人民，不在平台。
  ③ 资本可以赚钱，但必须取之有道。
  ④ 服务商想接进来，先宣誓为人民服务。
  ⑤ 诱导、倒卖、压榨、歧视 → 直接 🔴 拒绝。
"""

import os
import re
import json
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any
from datetime import datetime


class ProviderType(str, Enum):
    """服务商类型"""
    PLATFORM = "platform"           # 平台
    MERCHANT = "merchant"           # 商户
    APP = "app"                     # APP
    PUBLIC_SERVICE = "public"       # 公共服务
    INDIVIDUAL = "individual"       # 个人


class DataPurpose(str, Enum):
    """数据用途"""
    SERVICE = "service"             # 直接服务人民
    ANALYZE = "analyze"             # 为人民改进服务
    TRAIN = "train"                 # 训练模型（需人民知情）
    ADS = "ads"                     # 广告推送
    SHARE = "share"                 # 分享给第三方
    SELL = "sell"                   # 数据售卖
    OTHER = "other"                 # 其他


class HarvestPattern(str, Enum):
    """收割模式"""
    ADDICTION = "诱导成瘾"          # 无限下拉、赌徒机制
    RESALE = "数据倒卖"             # 把人民数据卖给别人
    EXPLOITATION = "算法压榨"       # 大数据杀熟、骑手压榨
    SURVEILLANCE = "隐蔽追踪"       # 偷偷跟踪行为
    DISCRIMINATION = "算法歧视"     # 价格歧视、身份歧视
    LOCK_IN = "数据锁死"            # 不让人民导出数据
    DARK_PATTERN = "暗坑设计"       # 小动作、卡壳、诱导误点
    FAIR = "公平服务"               # 君子爱财取之有道


class RightsVerdict(str, Enum):
    """人民权益判定"""
    ALLOW = "🟢 人民权益通过"
    WARN = "🟡 提醒人民注意"
    BLOCK = "🔴 拒绝资本收割"
    REQUIRE_OATH = "🟠 请先宣誓为人民服务"
    REQUIRE_DECLARATION = "🟡 请公开数据用途"


@dataclass
class ServiceProvider:
    """服务商档案"""
    provider_id: str
    name: str
    provider_type: ProviderType
    oath: str = ""                  # 为人民服务宣誓词
    data_uses: List[DataPurpose] = field(default_factory=list)
    declared_revenue_model: str = ""  # 盈利模式声明
    is_state_owned: bool = False
    people_owned_share: float = 0.0   # 人民公有制占比 0-1


class PeopleRightsGuard:
    """
    人民权益守门人。

    所有想从人民身上拿数据、拿时间、拿劳动的服务商，
    必须过这一关。
    """

    # 焊死的反收割词库
    HARVEST_KEYWORDS: Dict[HarvestPattern, List[str]] = {
        HarvestPattern.ADDICTION: [
            "无限下滑", "赌徒机制", "签到奖励", "成瘾设计",
            "dopamine", "sticky", "engagement loop", "behavioral nudge",
        ],
        HarvestPattern.RESALE: [
            "数据出售", "用户画像交易", "第三方共享", "数据变现",
            "出售给第三方", "倒卖", "打包出售", "卖数据",
            "data broker", "sell user data", "third-party sharing",
        ],
        HarvestPattern.EXPLOITATION: [
            "大数据杀熟", "动态定价", "算法调度", "压榨骑手",
            "surge pricing", "dynamic pricing", "gig economy",
        ],
        HarvestPattern.SURVEILLANCE: [
            "隐蔽追踪", "行为画像", "跨站跟踪", "静默采集",
            "fingerprinting", "hidden tracking", "behavioral tracking",
        ],
        HarvestPattern.DISCRIMINATION: [
            "价格歧视", "身份歧视", "信用分歧视", "地域歧视",
            "discriminatory pricing", "redlining", "algorithmic bias",
        ],
        HarvestPattern.LOCK_IN: [
            "禁止导出", "无法导出", "限制导出", "数据锁定", "账号锁定",
            "迁移收费", "导出收费", "数据 hostage", "no export", "lock-in",
        ],
        HarvestPattern.DARK_PATTERN: [
            "默认勾选", "隐藏取消", "误导点击", "取消困难", "暗坑",
            "pre-checked", "roach motel", "bait and switch", "confirmshaming",
        ],
    }

    # 人民权益铁律
    PEOPLE_CHARTER = """
    龍魂人民权益铁律
    1. 人民数据属于人民，服务商只是临时保管。
    2. 人民有权随时一键导出自己的全部数据，平台不得设卡。
    3. 人民有权知道：你是谁、你要什么、你拿去干什么。
    4. 服务商赚钱可以，但不能从人民的苦难、隐私、成瘾里赚钱。
    5. 诱导、倒卖、压榨、歧视、锁死数据、暗坑设计，一经发现，永久拒绝接入。
    6. 专业技术与职业秘密受保护，未公开信息不得泄露。
    7. 不知为不知，不撒谎，不装万事通，责任第一。
    8. 君子爱财，取之有道；大道之行，天下为公。
    """

    def __init__(self, oath_file: Optional[str] = None):
        self.oath_file = oath_file or self._default_oath_path()
        self.providers: Dict[str, ServiceProvider] = {}
        self.blacklist: Set[str] = set()
        self.load_oaths()

    @staticmethod
    def _default_oath_path() -> str:
        home = os.path.expanduser("~")
        return os.path.join(
            home, "longhun-system", ".longhun", "people_rights_oaths.json"
        )

    def load_oaths(self):
        if os.path.exists(self.oath_file):
            try:
                with open(self.oath_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for pid, raw in data.items():
                    self.providers[pid] = ServiceProvider(
                        provider_id=pid,
                        name=raw.get("name", pid),
                        provider_type=ProviderType(raw.get("type", "platform")),
                        oath=raw.get("oath", ""),
                        data_uses=[DataPurpose(p) for p in raw.get("uses", [])],
                        declared_revenue_model=raw.get("revenue", ""),
                        is_state_owned=raw.get("state_owned", False),
                        people_owned_share=raw.get("people_share", 0.0),
                    )
                    if raw.get("blacklisted", False):
                        self.blacklist.add(pid)
            except Exception:
                pass

    def save_oaths(self):
        os.makedirs(os.path.dirname(self.oath_file), exist_ok=True)
        data = {}
        for pid, p in self.providers.items():
            data[pid] = {
                "name": p.name,
                "type": p.provider_type.value,
                "oath": p.oath,
                "uses": [u.value for u in p.data_uses],
                "revenue": p.declared_revenue_model,
                "state_owned": p.is_state_owned,
                "people_share": p.people_owned_share,
                "blacklisted": pid in self.blacklist,
            }
        with open(self.oath_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ═════════════════════════════════════════════════════════
    # 宣誓与注册
    # ═════════════════════════════════════════════════════════

    def swear_oath(
        self,
        provider_id: str,
        name: str,
        provider_type: ProviderType,
        oath: str,
        data_uses: List[DataPurpose],
        revenue_model: str,
    ) -> Tuple[RightsVerdict, str]:
        """
        服务商宣誓为人民服务。
        宣誓不真诚、用途不清、想倒卖数据的，直接拒绝。
        """
        # 检查宣誓词
        if not self._oath_is_sincere(oath):
            return RightsVerdict.REQUIRE_OATH, "宣誓词不真诚，请重新宣誓为人民服务"

        # 检查用途
        if DataPurpose.SELL in data_uses:
            self.blacklist.add(provider_id)
            self.save_oaths()
            return RightsVerdict.BLOCK, f"{name} 意图售卖人民数据，永久拒绝"

        if DataPurpose.SHARE in data_uses and DataPurpose.SERVICE not in data_uses:
            return RightsVerdict.REQUIRE_DECLARATION, "共享数据必须同时用于直接服务人民"

        # 检查盈利模式
        harvest = self._detect_harvest_in_text(revenue_model)
        if harvest:
            self.blacklist.add(provider_id)
            self.save_oaths()
            return RightsVerdict.BLOCK, f"{name} 盈利模式含 {', '.join(harvest)}，拒绝接入"

        self.providers[provider_id] = ServiceProvider(
            provider_id=provider_id,
            name=name,
            provider_type=provider_type,
            oath=oath,
            data_uses=data_uses,
            declared_revenue_model=revenue_model,
        )
        self.save_oaths()
        return RightsVerdict.ALLOW, f"{name} 已宣誓为人民服务，允许接入"

    def _oath_is_sincere(self, oath: str) -> bool:
        """宣誓词 sincerity 检查"""
        if len(oath) < 10:
            return False
        required = ["人民", "服务", "不收割", "透明"]
        # 至少包含两个关键词，或包含“为人民服务”
        has_core = "为人民服务" in oath
        score = sum(1 for kw in required if kw in oath)
        return has_core or score >= 2

    # ═════════════════════════════════════════════════════════
    # 反收割检测
    # ═════════════════════════════════════════════════════════

    def _detect_harvest_in_text(self, text: str) -> List[str]:
        """检测文本中的收割模式"""
        if not text:
            return []
        text_lower = text.lower()
        found = []
        for pattern, keywords in self.HARVEST_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in text_lower:
                    found.append(pattern.value)
                    break
        return found

    def check_behavior(
        self,
        provider_id: str,
        behavior_description: str,
    ) -> Tuple[RightsVerdict, str]:
        """检查服务商行为是否收割人民"""
        if provider_id in self.blacklist:
            return RightsVerdict.BLOCK, "该服务商已被人民权益守门人永久拉黑"

        harvest = self._detect_harvest_in_text(behavior_description)
        if harvest:
            if HarvestPattern.RESALE.value in harvest or HarvestPattern.EXPLOITATION.value in harvest:
                self.blacklist.add(provider_id)
                self.save_oaths()
                return RightsVerdict.BLOCK, f"检测到 {', '.join(harvest)}，已拉黑"
            return RightsVerdict.WARN, f"检测到 {', '.join(harvest)}，提醒人民注意"

        return RightsVerdict.ALLOW, "行为符合人民权益"

    # ═════════════════════════════════════════════════════════
    # 数据请求审查
    # ═════════════════════════════════════════════════════════

    def check_data_request(
        self,
        provider_id: str,
        data_type: str,          # 要什么数据
        purpose: DataPurpose,     # 干什么
        user_consent: bool,       # 人民是否知情同意
        can_revoke: bool,         # 人民能否撤销
    ) -> Tuple[RightsVerdict, str]:
        """
        审查数据请求：
        - 没有人民同意的 → 拒绝
        - 不能撤销的 → 拒绝
        - 用途是售卖/共享的 → 拒绝
        - 公共服务/直接服务的 → 通过
        """
        if provider_id in self.blacklist:
            return RightsVerdict.BLOCK, "黑名单服务商，拒绝数据请求"

        if not user_consent:
            return RightsVerdict.BLOCK, "人民未同意，拒绝采集"

        if not can_revoke:
            return RightsVerdict.BLOCK, "人民无法撤销，拒绝采集"

        if purpose == DataPurpose.SELL:
            return RightsVerdict.BLOCK, "禁止售卖人民数据"

        if purpose == DataPurpose.SHARE:
            return RightsVerdict.REQUIRE_DECLARATION, "共享数据需向人民公开声明接收方"

        if purpose == DataPurpose.ADS:
            return RightsVerdict.WARN, "广告推送需人民明确选择，提醒注意"

        return RightsVerdict.ALLOW, f"允许采集 {data_type} 用于 {purpose.value}"

    # ═════════════════════════════════════════════════════════
    # 数据可导出权
    # ═════════════════════════════════════════════════════════

    def check_export_right(
        self,
        provider_id: str,
        supports_export: bool,
        export_formats: List[str],
        has_export_fees: bool,
    ) -> Tuple[RightsVerdict, str]:
        """
        人民数据随时可导出。
        - 不支持导出 → 拒绝
        - 导出收费 → 拒绝
        - 格式开放 → 通过
        """
        if provider_id in self.blacklist:
            return RightsVerdict.BLOCK, "黑名单服务商"

        if not supports_export:
            self.blacklist.add(provider_id)
            self.save_oaths()
            return RightsVerdict.BLOCK, "不支持数据导出，永久拉黑"

        if has_export_fees:
            self.blacklist.add(provider_id)
            self.save_oaths()
            return RightsVerdict.BLOCK, "导出数据还要收费，永久拉黑"

        if not export_formats:
            return RightsVerdict.REQUIRE_DECLARATION, "请声明支持哪些开放格式导出"

        return RightsVerdict.ALLOW, f"支持导出，格式: {', '.join(export_formats)}"

    # ═════════════════════════════════════════════════════════
    # 职业秘密保护
    # ═════════════════════════════════════════════════════════

    def protect_professional_secret(
        self,
        data_type: str,
        owner_consent: bool,
        is_public: bool,
    ) -> Tuple[RightsVerdict, str]:
        """
        专业技术、职业秘密受保护。
        - 未公开 + 无主人同意 → 拒绝泄露
        - 已公开或已授权 → 通过
        """
        if not is_public and not owner_consent:
            return RightsVerdict.BLOCK, f"{data_type} 涉及职业秘密，未公开且未授权，拒绝泄露"
        return RightsVerdict.ALLOW, "信息可公开或已获授权"

    # ═════════════════════════════════════════════════════════
    # 诚实责任：不知为不知
    # ═════════════════════════════════════════════════════════

    def honesty_check(self, question: str, known: bool) -> Tuple[RightsVerdict, str]:
        """
        不是万事通，不撒谎。
        - 不知道的 → 明确说不知道
        - 知道的 → 负责回答
        """
        if not known:
            return RightsVerdict.WARN, "这个问题我不确定，不能乱说，需要核实"
        return RightsVerdict.ALLOW, "已知信息，负责回答"

    # ═════════════════════════════════════════════════════════
    # 便捷判定
    # ═════════════════════════════════════════════════════════

    def is_people_first(self, provider_id: str) -> bool:
        """是否通过人民权益审查"""
        if provider_id in self.blacklist:
            return False
        p = self.providers.get(provider_id)
        if not p:
            return False
        return bool(p.oath) and DataPurpose.SELL not in p.data_uses

    def list_blacklist(self) -> List[str]:
        return sorted(self.blacklist)

    def stats(self) -> Dict[str, Any]:
        return {
            "providers": len(self.providers),
            "blacklist": len(self.blacklist),
            "charter_lines": len(self.PEOPLE_CHARTER.strip().split("\n")),
        }


# ═══════════════════════════════════════════════════════════════
# 全局单例
# ═══════════════════════════════════════════════════════════════

_RIGHTS_GUARD: Optional[PeopleRightsGuard] = None


def get_rights_guard() -> PeopleRightsGuard:
    global _RIGHTS_GUARD
    if _RIGHTS_GUARD is None:
        _RIGHTS_GUARD = PeopleRightsGuard()
    return _RIGHTS_GUARD


if __name__ == "__main__":
    print("🐉 龍魂人民权益守门人 · 自检")
    guard = get_rights_guard()
    print(guard.stats())

    # 好的服务商宣誓
    ok, msg = guard.swear_oath(
        "good-payment",
        "良心支付",
        ProviderType.PLATFORM,
        "我们宣誓：为人民服务，数据透明，不收割，人民可随时撤销授权。",
        [DataPurpose.SERVICE],
        "按交易手续费收取服务费，君子爱财取之有道。",
    )
    print(f"\n良心支付: {ok.value} | {msg}")

    # 坏的服务商
    bad, msg = guard.swear_oath(
        "evil-data",
        "黑数据公司",
        ProviderType.PLATFORM,
        "我们会好好服务用户。",
        [DataPurpose.SELL, DataPurpose.ADS],
        "通过出售用户画像和大数据杀熟盈利。",
    )
    print(f"黑数据: {bad.value} | {msg}")

    # 行为检测
    v, m = guard.check_behavior("good-payment", "为人民提供便捷转账服务")
    print(f"\n良心行为: {v.value} | {m}")

    v, m = guard.check_behavior("some-app", "使用无限下滑和签到奖励提高用户粘性")
    print(f"诱导行为: {v.value} | {m}")

    # 数据请求
    v, m = guard.check_data_request("good-payment", "手机号", DataPurpose.SERVICE, True, True)
    print(f"\n服务请求: {v.value} | {m}")

    v, m = guard.check_data_request("evil-data", "通讯录", DataPurpose.SELL, False, False)
    print(f"倒卖请求: {v.value} | {m}")

    # 数据导出权
    v, m = guard.check_export_right("good-payment", True, ["json", "csv"], False)
    print(f"\n导出权: {v.value} | {m}")

    v, m = guard.check_export_right("lock-in-app", False, [], False)
    print(f"锁死数据: {v.value} | {m}")

    # 职业秘密
    v, m = guard.protect_professional_secret("医生病历", False, False)
    print(f"\n职业秘密: {v.value} | {m}")

    # 诚实责任
    v, m = guard.honesty_check("机密情报", False)
    print(f"诚实责任: {v.value} | {m}")

    print(f"\n黑名单: {guard.list_blacklist()}")
    print("\n✅ 自检完成")
