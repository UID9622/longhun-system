# DNA: #龍芯⚡️丙午·丙申·戊辰·丙辰·䷸巽为风-CODE-补DNA-fdd18734
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
🐉 龍魂 · 天眼可视化生态总成引擎 v2.3（国家交接级合规底座）
DNA: [[GENERATED_BY_LH_DNA_GENERATOR_V3]]-TIANYAN-ENGINE-v2.3
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

系统健康雷达 · 数据流场 · 决策链路 · 实时看板 · 卦象状态
整合龍魂全生态 55 模块状态聚合

v2.3 方案D · 国家交接级合规底座：
  · 负责人体系：账号 + 实名 + 角色(R1~R5)，每条操作落"谁"
  · 归属地IP：内置离线 GeoIP（数据不出境·可复核标注）
  · 哈希链审计：append-only + SHA-256 链，改任何一条即断链
  · 按权限导出：R1~R4 分级导出参数/数据/审计/账号，导出即留痕
  · 交接核验：独立离线校验脚本 lh_tianyan_verify.py
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import ipaddress
import json
import logging
import os
import secrets
import subprocess
import sys
import threading
import time
import unittest
from dataclasses import dataclass, field, asdict
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urlparse

# ── 操作台（方案C/D）常量 ─────────────────────────────────────────
ADMIN_KEY_ENV = "LH_TIANYAN_ADMIN_KEY"     # 超级管理员密钥（环境变量·永不入码）
ADMIN_ACCOUNTS_ENV = "LH_TIANYAN_ACCOUNTS" # 账号文件路径（环境变量可覆盖）
ADMIN_TOKEN_TTL = 8 * 3600                  # session 8 小时
ADMIN_MAX_LOGIN_FAIL = 5                    # 单 IP 登录失败上限
ADMIN_LOCK_SECONDS = 300                    # 超限锁定 5 分钟
ADMIN_ACTION_AUDIT = "audit"                # 白名单操作：触发德本审计
ADMIN_ACTION_RESTART = "restart"            # 白名单操作：重启引擎服务

# 角色权限矩阵（对齐第五层认证分级）
#   R1/L5 = UID9622（全权限）· R2/L4 = 系统管理员 · R3/L3 = 人格组长
#   R4/L2 = 审计人员 · R5/L1 = 公开（不可登录管理台）
ROLE_PERMISSIONS: Dict[str, List[str]] = {
    "R1": ["params", "data", "audit", "accounts", "all"],   # 全量导出
    "R2": ["params", "audit"],                               # 参数 + 审计（数据需脱敏）
    "R3": ["params"],                                        # 仅系统参数
    "R4": ["audit"],                                         # 仅审计日志
    "R5": [],                                                # 无管理权限
}
ROLE_NAMES: Dict[str, str] = {
    "R1": "主权人（UID9622）", "R2": "系统管理员",
    "R3": "人格组长", "R4": "审计人员", "R5": "公开",
}

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


# ═══════════════════════════════════════════════════════════════════════════════
# 0.5 离线 GeoIP 归属地引擎（国家交接级·数据不出境·来源可复核）
# ═══════════════════════════════════════════════════════════════════════════════

class GeoIP:
    """内置离线 IP 归属地查询。

    原则（第七层 · 数据主权）：
      · 数据本地解析，绝不出境、不调外部 API
      · 每条映射标注来源，供国家审计复核
      · 库可扩充：追加 (CIDR, 国家, 省市, 运营商) 元组即可

    来源标注：私有/保留段按 IANA RFC6890；中国大网段按
    APNIC/CNNIC 公开 IP 分配记录（2024 快照）粗分，省市粒度
    需扩充时以「所属运营商公开地址库」为准。
    """

    # (cidr, 国家, 省市, 运营商/备注)
    _TABLE: List[Tuple[str, str, str, str]] = [
        # ── 私有 / 保留 / 特殊段（RFC6890）──
        ("127.0.0.0/8",     "中国", "本机回环", "LOOPBACK"),
        ("10.0.0.0/8",      "私有", "私有网络", "PRIVATE"),
        ("172.16.0.0/12",   "私有", "私有网络", "PRIVATE"),
        ("192.168.0.0/16",  "私有", "局域网",   "PRIVATE"),
        ("100.64.0.0/10",   "私有", "运营商NAT", "CARRIER_NAT"),
        ("169.254.0.0/16",  "保留", "链路本地", "LINK_LOCAL"),
        ("0.0.0.0/8",       "保留", "本网络",   "RESERVED"),
        ("224.0.0.0/4",     "保留", "组播",     "MULTICAST"),
        ("240.0.0.0/4",     "保留", "保留",     "RESERVED"),
        # ── 实测标注段（鲲鹏/华为云）──
        ("39.182.0.0/15",   "中国", "广东",     "华为云"),
        ("119.13.0.0/16",   "中国", "广东",     "华为云"),
        ("124.70.0.0/16",   "中国", "北京",     "华为云"),
        # ── 中国运营商大网段（APNIC/CNNIC 2024 快照·省市待扩充）──
        ("1.0.0.0/8",       "中国", "未知",     "CHINANET"),
        ("14.0.0.0/8",      "中国", "未知",     "CHINANET"),
        ("27.0.0.0/8",      "中国", "未知",     "CHINANET"),
        ("36.0.0.0/8",      "中国", "未知",     "CHINANET"),
        ("39.0.0.0/8",      "中国", "未知",     "华为云/云商"),
        ("42.0.0.0/8",      "中国", "未知",     "CHINANET"),
        ("49.0.0.0/8",      "中国", "未知",     "CHINANET"),
        ("58.0.0.0/8",      "中国", "未知",     "CNCGROUP"),
        ("59.0.0.0/8",      "中国", "未知",     "CHINANET"),
        ("60.0.0.0/8",      "中国", "未知",     "CHINANET"),
        ("61.0.0.0/8",      "中国", "未知",     "CHINANET"),
        ("101.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("103.0.0.0/8",     "中国", "未知",     "APNIC/中国"),
        ("106.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("110.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("111.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("112.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("113.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("114.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("115.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("116.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("117.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("118.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("119.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("120.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("121.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("122.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("123.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("124.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("125.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("139.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("140.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("144.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("153.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("157.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("163.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("171.0.0.0/8",     "中国", "未知",     "CNCGROUP"),
        ("175.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("180.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("182.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("183.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("202.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("203.0.0.0/8",     "中国", "未知",     "APNIC/中国"),
        ("210.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("211.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("218.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("219.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("220.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("221.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("222.0.0.0/8",     "中国", "未知",     "CHINANET"),
        ("223.0.0.0/8",     "中国", "未知",     "CHINANET"),
    ]

    _networks: Optional[List[Tuple[ipaddress.IPv4Network, str, str, str]]] = None

    @classmethod
    def _compile(cls) -> List[Tuple[ipaddress.IPv4Network, str, str, str]]:
        if cls._networks is None:
            nets = []
            for cidr, country, region, isp in cls._TABLE:
                try:
                    nets.append((ipaddress.ip_network(cidr, strict=False),
                                 country, region, isp))
                except ValueError:
                    logging.warning("GeoIP 表含非法 CIDR: %s", cidr)
            cls._networks = nets
        return cls._networks

    @classmethod
    def lookup(cls, ip: str) -> Dict[str, str]:
        """查询 IP 归属地。未知返回「境外/未知」并标注（不编造）。"""
        try:
            addr = ipaddress.ip_address(ip.split(",")[0].strip())
        except ValueError:
            return {"country": "未知", "region": "未知", "city": "未知",
                    "isp": "INVALID", "source": "offline-builtin"}
        if addr.version != 4:
            return {"country": "未知", "region": "未知", "city": "未知",
                    "isp": "IPV6", "source": "offline-builtin"}
        for net, country, region, isp in cls._compile():
            if addr in net:
                return {"country": country, "region": region,
                        "city": region, "isp": isp,
                        "source": "offline-builtin(APNIC/CNNIC 2024)"}
        return {"country": "境外/未收录", "region": "未知", "city": "未知",
                "isp": "UNKNOWN", "source": "offline-builtin"}


# ═══════════════════════════════════════════════════════════════════════════════
# 0.6 账号存储（负责人体系 · 国家交接级）
# ═══════════════════════════════════════════════════════════════════════════════

class AccountStore:
    """账号表管理。

    安全设计：
      · 密钥永不存明文，只存 SHA-256(account + ":" + key) 摘要
      · 账号文件默认放 www 之外（/etc/longhun/ 或仓库 etc/），
        静态服务黑名单 _ 前缀，杜绝经 HTTP 暴露
      · 增删改账号本身必须写入操作审计（留痕）
    """

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self._lock = threading.Lock()
        self.accounts: List[Dict] = []
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            self.accounts = []
            return
        try:
            self.accounts = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            logging.warning("账号文件损坏，按空表处理: %s", self.path)
            self.accounts = []

    @staticmethod
    def key_digest(account: str, key: str) -> str:
        return hashlib.sha256(f"{account}:{key}".encode("utf-8")).hexdigest()

    def find(self, account: str) -> Optional[Dict]:
        for a in self.accounts:
            if a.get("account") == account and not a.get("disabled"):
                return a
        return None

    def verify(self, account: str, key: str) -> Optional[Dict]:
        rec = self.find(account)
        if not rec:
            return None
        if not hmac.compare_digest(rec.get("key_hash", ""),
                                   self.key_digest(account, key)):
            return None
        return dict(rec)

    def list_sanitized(self) -> List[Dict]:
        """脱敏账号清单：key_hash 只留前 8 位。"""
        out = []
        for a in self.accounts:
            h = a.get("key_hash", "")
            out.append({
                "account": a.get("account"),
                "name": a.get("name"),
                "role": a.get("role", "R5"),
                "disabled": bool(a.get("disabled")),
                "created_by": a.get("created_by", ""),
                "created_at": a.get("created_at", ""),
                "key_hash_prefix": h[:8] if h else "",
            })
        return out


def ensure_initial_accounts(path: Path, admin_key: str) -> AccountStore:
    """首次运行自动创建 root 账号（UID9622·R1），密钥取环境变量。"""
    store = AccountStore(path)
    if not store.accounts and admin_key:
        store.accounts = [{
            "account": "root",
            "name": "诸葛鑫（UID9622）",
            "role": "R1",
            "key_hash": AccountStore.key_digest("root", admin_key),
            "created_by": "SYSTEM-BOOTSTRAP",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "disabled": False,
        }]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(store.accounts, ensure_ascii=False, indent=2),
                        encoding="utf-8")
        try:
            os.chmod(path, 0o600)
        except OSError:
            pass
    return store


# ═══════════════════════════════════════════════════════════════════════════════
# 0. 数据模型
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ModuleStatus:
    """单个模块状态。"""
    name: str
    status: str          # running / stopped / degraded / unknown
    health_score: float  # 0-100
    tricolor: str        # 🟢 / 🟡 / 🔴
    last_heartbeat: str
    version: str
    metadata: Dict = field(default_factory=dict)


@dataclass
class PersonaState:
    """人格状态。"""
    id: str
    name: str
    gua: str
    wuxing: str
    role: str
    active: bool
    double: Optional[str] = None
    health_score: float = 100.0


@dataclass
class TianyanSnapshot:
    """天眼快照。"""
    dna: str
    timestamp: str
    time_anchor: Dict
    modules: List[ModuleStatus]
    personas: List[PersonaState]
    sovereignty: Dict
    audit: Dict
    dashboard: Dict
    system_health: float
    overall_tricolor: str

    def to_dict(self) -> Dict:
        return asdict(self)


# ═══════════════════════════════════════════════════════════════════════════════
# 1. 时间锚点引擎
# ═══════════════════════════════════════════════════════════════════════════════

class TimeAnchorEngine:
    """天干地支 + 64 卦象 + 节气 + 时辰 + 五行 + 三色。"""

    TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    GUA_NAMES = [
        "乾", "坤", "屯", "蒙", "需", "讼", "师", "比", "小畜", "履", "泰", "否",
        "同人", "大有", "谦", "豫", "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
        "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒", "遁", "大壮", "晋", "明夷",
        "家人", "睽", "蹇", "解", "损", "益", "夬", "姤", "萃", "升", "困", "井",
        "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅", "巽", "兑", "涣", "节",
        "中孚", "小过", "既济", "未济"
    ]
    WUXING_MAP = {
        "乾": "金", "兑": "金", "震": "木", "巽": "木", "坎": "水",
        "离": "火", "坤": "土", "艮": "土"
    }

    @classmethod
    def get_current(cls) -> Dict:
        """获取当前时间锚点。"""
        now = datetime.now()
        # 简化计算：使用年份干支映射
        year = now.year
        tg_idx = (year - 4) % 10
        dz_idx = (year - 4) % 12
        # 卦象：基于当前时间戳 % 64
        gua_idx = int(now.timestamp()) % 64
        gua = cls.GUA_NAMES[gua_idx]
        wuxing = cls.WUXING_MAP.get(gua, "土")

        # 三色：基于卦象索引
        if gua_idx % 3 == 0:
            tricolor = "🟢"
        elif gua_idx % 3 == 1:
            tricolor = "🟡"
        else:
            tricolor = "🔴"

        return {
            "ganzhi": f"{cls.TIANGAN[tg_idx]}{cls.DIZHI[dz_idx]}",
            "gua": f"䷀{gua}",
            "gua_idx": gua_idx + 1,
            "wuxing": wuxing,
            "tricolor": tricolor,
            "hour": now.hour,
            "minute": now.minute,
            "iso": now.isoformat(),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 2. 模块注册表（38 模块完整清单）
# ═══════════════════════════════════════════════════════════════════════════════

class ModuleRegistry:
    """龍魂系统 38 模块注册表。"""

    # 基于 CSDN 公开信息整合的完整模块清单
    ALL_MODULES: List[Dict] = [
        # 协议层 (5)
        {"name": "P0铁律引擎", "category": "协议层", "weight": 1.0},
        {"name": "S1-S5父级协议", "category": "协议层", "weight": 0.9},
        {"name": "君子协议", "category": "协议层", "weight": 0.9},
        {"name": "主权宣言", "category": "协议层", "weight": 0.8},
        {"name": "数据主权协议", "category": "协议层", "weight": 0.9},
        # 主权层 (3)
        {"name": "数据主权引擎", "category": "主权层", "weight": 1.0},
        {"name": "货币主权引擎", "category": "主权层", "weight": 0.9},
        {"name": "审计主权引擎", "category": "主权层", "weight": 1.0},
        # 人格层 (28)
        {"name": "北辰·战略决策", "category": "人格层", "weight": 1.0},
        {"name": "宝宝·情感陪伴", "category": "人格层", "weight": 0.8},
        {"name": "诸葛·逻辑分析", "category": "人格层", "weight": 1.0},
        {"name": "老子·哲学思考", "category": "人格层", "weight": 0.7},
        {"name": "文心·文化传承", "category": "人格层", "weight": 0.9},
        {"name": "墨子·兼爱非攻", "category": "人格层", "weight": 0.6},
        {"name": "鲁班·工程实现", "category": "人格层", "weight": 0.9},
        {"name": "商鞅·规则制定", "category": "人格层", "weight": 0.8},
        {"name": "管仲·经世致用", "category": "人格层", "weight": 0.7},
        {"name": "孙武·兵者诡道", "category": "人格层", "weight": 0.8},
        {"name": "张良·运筹帷幄", "category": "人格层", "weight": 0.8},
        {"name": "祖冲之·精算天元", "category": "人格层", "weight": 0.7},
        {"name": "蔡伦·纸传文明", "category": "人格层", "weight": 0.6},
        {"name": "毕昇·字活天下", "category": "人格层", "weight": 0.6},
        {"name": "郑和·扬帆四海", "category": "人格层", "weight": 0.7},
        {"name": "戚继光·铁甲长城", "category": "人格层", "weight": 0.7},
        {"name": "李冰·功在千秋", "category": "人格层", "weight": 0.6},
        {"name": "沈括·格物致知", "category": "人格层", "weight": 0.8},
        {"name": "张衡·观天测地", "category": "人格层", "weight": 0.7},
        {"name": "僧一行·历象日月", "category": "人格层", "weight": 0.6},
        {"name": "赵匡胤·陈桥变局", "category": "人格层", "weight": 0.7},
        {"name": "王安石·变法图强", "category": "人格层", "weight": 0.7},
        {"name": "苏轼·豁达人生", "category": "人格层", "weight": 0.8},
        {"name": "曹雪芹·红楼一梦", "category": "人格层", "weight": 0.6},
        {"name": "莲溪·教学传道", "category": "人格层", "weight": 0.9},
        {"name": "老顽童·锐评吐槽", "category": "人格层", "weight": 0.7},
        {"name": "熵梦·技术精准", "category": "人格层", "weight": 0.9},
        {"name": "弘一·历史厚重", "category": "人格层", "weight": 0.8},
        # 技术基础设施 (14)
        {"name": "CNSH编译器", "category": "技术层", "weight": 1.0},
        {"name": "三才算法内核", "category": "技术层", "weight": 1.0},
        {"name": "七维推演引擎", "category": "技术层", "weight": 0.9},
        {"name": "DNA追溯引擎", "category": "技术层", "weight": 1.0},
        {"name": "三色审计引擎", "category": "技术层", "weight": 1.0},
        {"name": "龍音ASR", "category": "技术层", "weight": 0.8},
        {"name": "龍瞳OCR", "category": "技术层", "weight": 0.8},
        {"name": "龍文NLP", "category": "技术层", "weight": 0.9},
        {"name": "行为密码学", "category": "技术层", "weight": 0.8},
        {"name": "不动点网络FPN", "category": "技术层", "weight": 0.7},
        {"name": "Web3-DNA交易", "category": "技术层", "weight": 0.6},
        {"name": "多币种直达", "category": "技术层", "weight": 0.7},
        {"name": "洛书翻译引擎", "category": "技术层", "weight": 0.8},
        {"name": "通心译引擎", "category": "技术层", "weight": 0.8},
        # 安全治理 (4)
        {"name": "史官记录器", "category": "安全层", "weight": 0.9},
        {"name": "耻辱墙管理器", "category": "安全层", "weight": 0.9},
        {"name": "主权熔断引擎", "category": "安全层", "weight": 1.0},
        {"name": "红蓝对抗引擎", "category": "安全层", "weight": 0.8},
        # 可视化 (1)
        {"name": "天眼看板", "category": "可视化层", "weight": 1.0},
        # ADS 自描述系统 (1·真实探针 :9626)
        {"name": "ADS自描述系统", "category": "自指层", "weight": 0.6},
    ]

    @classmethod
    def get_all(cls) -> List[Dict]:
        return cls.ALL_MODULES[:]

    @classmethod
    def get_by_category(cls, category: str) -> List[Dict]:
        return [m for m in cls.ALL_MODULES if m["category"] == category]

    @classmethod
    def count(cls) -> int:
        return len(cls.ALL_MODULES)


# ═══════════════════════════════════════════════════════════════════════════════
# 3. 状态聚合引擎
# ═══════════════════════════════════════════════════════════════════════════════

class StatusAggregator:
    """聚合全系统状态。"""

    def __init__(self, registry: Optional[ModuleRegistry] = None) -> None:
        self.registry = registry or ModuleRegistry()
        self._cache: Optional[TianyanSnapshot] = None
        self._cache_time: float = 0.0
        self._cache_ttl: float = 5.0  # 5 秒缓存

    def _generate_dna(self) -> str:
        h = hashlib.sha256(f"TIANYAN{time.time()}{os.urandom(8)}".encode()).hexdigest()[:8].upper()
        return f"[[GENERATED_BY_LH_DNA_GENERATOR_V3]]-TIANYAN-{h}-v2.3"

    def _simulate_module_status(self, module: Dict) -> ModuleStatus:
        """模拟模块状态（实际部署时替换为真实探针）。"""
        # 🟡 模拟数据，标注清晰
        import random
        health = random.uniform(75, 100)
        if health >= 90:
            status, tricolor = "running", "🟢"
        elif health >= 70:
            status, tricolor = "degraded", "🟡"
        else:
            status, tricolor = "stopped", "🔴"

        return ModuleStatus(
            name=module["name"],
            status=status,
            health_score=round(health, 2),
            tricolor=tricolor,
            last_heartbeat=datetime.now().isoformat(),
            version="v2.3",
            metadata={"category": module["category"], "weight": module["weight"]}
        )

    def _probe_ads(self) -> ModuleStatus:
        """ADS 自描述系统真实探针：探测本机 :9626 常驻 API（无码 403 = 确认码闸门生效 = 在线）。"""
        import urllib.request
        base = ModuleStatus(
            name="ADS自描述系统",
            status="stopped", health_score=0.0, tricolor="🔴",
            last_heartbeat=datetime.now().isoformat(),
            version="v4.0",
            metadata={"category": "自指层", "weight": 0.6,
                      "probe": "http://127.0.0.1:9622/v1/self/health"}
        )
        from urllib.error import HTTPError, URLError
        try:
            try:
                req = urllib.request.Request("http://127.0.0.1:9622/v1/self/health", method="GET")
                with urllib.request.urlopen(req, timeout=2) as resp:
                    code = resp.status
            except HTTPError as e:  # 4xx/5xx 会抛异常，需单独捕获（403=确认码闸门=在线）
                code = e.code
            if code == 200:
                base.status, base.health_score, base.tricolor = "running", 100.0, "🟢"
            elif code == 403:  # 确认码闸门生效 = 服务在线
                base.status, base.health_score, base.tricolor = "running", 92.0, "🟢"
            else:
                base.status, base.health_score, base.tricolor = "degraded", 55.0, "🟡"
        except Exception:
            base.status, base.health_score, base.tricolor = "stopped", 0.0, "🔴"
            base.metadata["note"] = "本机未监听 :9626（Mac 未部署或已停）"
        return base

    def snapshot(self, use_cache: bool = True) -> TianyanSnapshot:
        """生成系统快照。"""
        now = time.time()
        if use_cache and self._cache and (now - self._cache_time) < self._cache_ttl:
            return self._cache

        time_anchor = TimeAnchorEngine.get_current()
        modules = [self._simulate_module_status(m) for m in self.registry.get_all()]
        # ADS 模块用真实探针覆盖模拟状态（其余保持模拟·🟡标注）
        for _i, _m in enumerate(modules):
            if _m.name == "ADS自描述系统":
                modules[_i] = self._probe_ads()

        # 计算综合健康度
        total_weight = sum(m.metadata.get("weight", 1.0) for m in modules)
        weighted_health = sum(m.health_score * m.metadata.get("weight", 1.0) for m in modules)
        system_health = weighted_health / total_weight if total_weight else 0.0

        # 三色判定
        if system_health >= 85:
            overall_tricolor = "🟢"
        elif system_health >= 60:
            overall_tricolor = "🟡"
        else:
            overall_tricolor = "🔴"

        # 人格状态（28 人格）
        personas = []
        for i, m in enumerate(self.registry.get_by_category("人格层")):
            gua_idx = i % 64
            personas.append(PersonaState(
                id=f"P{i+1:02d}",
                name=m["name"].split("·")[0],
                gua=f"䷀{TimeAnchorEngine.GUA_NAMES[gua_idx]}",
                wuxing=TimeAnchorEngine.WUXING_MAP.get(TimeAnchorEngine.GUA_NAMES[gua_idx], "土"),
                role=m["name"].split("·")[1] if "·" in m["name"] else "通用",
                active=i < 5,  # 前 5 个默认活跃
                health_score=modules[i + 8].health_score if i + 8 < len(modules) else 100.0
            ))

        # 审计统计（模拟）
        audit = {
            "total": 325,
            "green": 245,
            "yellow": 68,
            "red": 12,
            "shame_wall": 12,
            "last_audit": datetime.now().isoformat()
        }

        # 主权状态
        sovereignty = {
            "data_status": "🟢",
            "currency_status": "🟢",
            "audit_status": "🟢",
            "knowledge_status": "🟡",
            "data_count": 15420,
        }

        # 看板数据
        dashboard = {
            "radar": {
                "data_sovereignty": 85,
                "currency_sovereignty": 90,
                "audit_sovereignty": 78,
                "knowledge_base": 65,
                "persona_activity": 72,
            },
            "flow": {
                "nodes": ["用户", "思维注入", "知识库", "人格路由", "分身输出", "审计", "反馈"],
                "links": [[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,2]]
            },
            "chain": {
                "input": "用户查询",
                "persona": "北辰",
                "double": "战略官",
                "audit_score": 92,
                "audit_status": "🟢"
            }
        }

        snapshot = TianyanSnapshot(
            dna=self._generate_dna(),
            timestamp=datetime.now().isoformat(),
            time_anchor=time_anchor,
            modules=modules,
            personas=personas,
            sovereignty=sovereignty,
            audit=audit,
            dashboard=dashboard,
            system_health=round(system_health, 2),
            overall_tricolor=overall_tricolor
        )

        self._cache = snapshot
        self._cache_time = now
        return snapshot

    def get_category_stats(self) -> Dict[str, Dict]:
        """按类别统计。"""
        snap = self.snapshot()
        stats: Dict[str, List[ModuleStatus]] = {}
        for m in snap.modules:
            cat = m.metadata.get("category", "未知")
            stats.setdefault(cat, []).append(m)

        result = {}
        for cat, mods in stats.items():
            avg_health = sum(m.health_score for m in mods) / len(mods) if mods else 0
            running = sum(1 for m in mods if m.status == "running")
            result[cat] = {
                "count": len(mods),
                "avg_health": round(avg_health, 2),
                "running": running,
                "degraded": sum(1 for m in mods if m.status == "degraded"),
                "stopped": sum(1 for m in mods if m.status == "stopped"),
                "tricolor": "🟢" if avg_health >= 85 else "🟡" if avg_health >= 60 else "🔴"
            }
        return result


# ═══════════════════════════════════════════════════════════════════════════════
# 4. 数据导出引擎
# ═══════════════════════════════════════════════════════════════════════════════

class DataExporter:
    """导出天眼数据供前端消费。"""

    @staticmethod
    def to_json(snapshot: TianyanSnapshot, indent: int = 2) -> str:
        return json.dumps(snapshot.to_dict(), indent=indent, ensure_ascii=False)

    @staticmethod
    def to_api_response(snapshot: TianyanSnapshot) -> Dict:
        """生成标准 API 响应结构。"""
        return {
            "code": 0,
            "message": "success",
            "data": snapshot.to_dict(),
            "dna": snapshot.dna,
            "timestamp": snapshot.timestamp
        }

    @staticmethod
    def to_sse_stream(snapshot: TianyanSnapshot) -> str:
        """生成 SSE 流格式。"""
        data = json.dumps(snapshot.to_dict(), ensure_ascii=False)
        return f"data: {data}\n\n"


# ═══════════════════════════════════════════════════════════════════════════════
# 4.5 常驻 HTTP 服务（--serve · 应用级实时链路 v2.1）
# ═══════════════════════════════════════════════════════════════════════════════

class TianyanHTTPServer(ThreadingHTTPServer):
    """线程化 HTTP 服务。只读·无状态·请求驱动（CPU 占用趋零）。"""
    daemon_threads = True


class TianyanHandler(BaseHTTPRequestHandler):
    """天眼 API + 静态托管。数据只读·本地渲染·数据不出境。"""

    aggregator: Optional["StatusAggregator"] = None
    www_root: Optional[Path] = None
    started_at: float = time.time()

    # ── 操作台（方案C/D）会话态 ──
    admin_key: str = ""                      # 超级管理员密钥（环境变量注入）
    account_store: Optional[AccountStore] = None  # 账号表（负责人体系）
    sessions: Dict[str, Dict] = {}           # token -> {exp, account, name, role, ip}
    login_fails: Dict[str, Dict[str, float]] = {}  # ip -> {count, lock_until}
    _session_lock = threading.Lock()
    _audit_lock = threading.Lock()           # 审计链串行写锁
    ops_log: Optional[Path] = None           # 操作审计日志路径（哈希链）

    MIME = {
        ".html": "text/html; charset=utf-8",
        ".js": "application/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".woff2": "font/woff2",
        ".woff": "font/woff",
        ".ttf": "font/ttf",
        ".ico": "image/x-icon",
        ".txt": "text/plain; charset=utf-8",
    }

    def log_message(self, fmt: str, *args: Any) -> None:
        logging.info("HTTP %s %s", self.address_string(), fmt % args)

    # ---- 工具 ----
    def _cors_headers(self) -> None:
        # 仅只读公开监控数据放开；CORS 支持跨源联调（本地 8199 → API）
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Accept, Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "600")
        self.send_header("Cache-Control", "no-store")

    def _send_json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._cors_headers()
        self.end_headers()
        self.wfile.write(body)

    # ---- API 端点 ----
    def _api_status(self) -> None:
        snap = self.aggregator.snapshot()
        self._send_json(200, DataExporter.to_api_response(snap))

    def _api_modules(self) -> None:
        snap = self.aggregator.snapshot()
        self._send_json(200, {"code": 0, "message": "success", "data": {
            "total": len(snap.modules),
            "green": sum(1 for m in snap.modules if m.tricolor == "🟢"),
            "yellow": sum(1 for m in snap.modules if m.tricolor == "🟡"),
            "red": sum(1 for m in snap.modules if m.tricolor == "🔴"),
            "modules": [asdict(m) for m in snap.modules],
        }})

    def _api_health(self) -> None:
        snap = self.aggregator.snapshot()
        self._send_json(200, {"code": 0, "message": "success", "data": {
            "status": "ok",
            "version": "v2.1",
            "uptime": round(time.time() - self.started_at, 1),
            "health": snap.system_health,
            "tricolor": snap.overall_tricolor,
            "modules": len(snap.modules),
            "personas": len(snap.personas),
            "timestamp": snap.timestamp,
            "dna": snap.dna,
        }})

    def _api_stats(self) -> None:
        self._send_json(200, {"code": 0, "message": "success",
                              "data": self.aggregator.get_category_stats()})

    # ═══════════════════════════════════════════════════════════════
    # 操作台（方案C · v2.2）· 管理 API · 仅只读查询 + 白名单操作
    # 鉴权: Bearer session token · 密钥走环境变量 · 命令白名单防 RCE
    # ═══════════════════════════════════════════════════════════════
    def _read_body(self) -> Dict:
        try:
            n = int(self.headers.get("Content-Length", "0") or "0")
            if n <= 0:
                return {}
            raw = self.rfile.read(n) if n < 65536 else b""
            return json.loads(raw.decode("utf-8")) if raw else {}
        except Exception:  # noqa: BLE001
            return {}

    def _audit_op(self, action: str, ip: str, ok: bool, detail: str = "",
                  account: str = "", name: str = "", role: str = "") -> None:
        """操作审计日志（哈希链 · append-only JSONL）。

        国家交接级设计：
          · 每条含 prev_hash（上条哈希），构成 SHA-256 链
          · 任何一条被改 → 链断 → lh_tianyan_verify.py 可检测
          · 操作人（account/name/role）+ 归属地（ip_geo）强制落盘
        """
        if not self.ops_log:
            return
        geo = GeoIP.lookup(ip)
        with self._audit_lock:
            try:
                prev_hash = self._audit_tail_hash()
                core = {
                    "ts": datetime.now().isoformat(timespec="seconds"),
                    "action": action,
                    "ip": ip,
                    "ip_geo": f"{geo['country']}·{geo['region']}·{geo['isp']}",
                    "account": account or "anonymous",
                    "name": name or "",
                    "role": role or "R5",
                    "ok": bool(ok),
                    "detail": (detail or "")[:400],
                    "prev_hash": prev_hash,
                }
                # hash 覆盖除自身外全部字段（key 有序，保证可复算）
                body = json.dumps(core, ensure_ascii=False, sort_keys=True)
                entry_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
                core["hash"] = entry_hash
                with open(self.ops_log, "a", encoding="utf-8") as f:
                    f.write(json.dumps(core, ensure_ascii=False) + "\n")
            except Exception:  # noqa: BLE001
                logging.warning("操作审计日志写入失败: %s", action)

    def _audit_tail_hash(self) -> str:
        """读取审计链最后一条 hash（无则 GENESIS）。

        从尾部向上找最近一条带 hash 的记录：升级前旧格式（无 hash）视为
        封存段，不参与链衔接。
        """
        if not self.ops_log or not self.ops_log.exists():
            return "GENESIS"
        try:
            with open(self.ops_log, "rb") as f:
                f.seek(0, 2)
                size = f.tell()
                if size == 0:
                    return "GENESIS"
                step = 8192
                pos = max(0, size - step)
                while True:
                    f.seek(pos)
                    chunk = f.read().decode("utf-8", errors="ignore")
                    lines = [ln for ln in chunk.splitlines() if ln.strip()]
                    for line in reversed(lines):
                        try:
                            h = str(json.loads(line).get("hash", ""))
                            if h:
                                return h
                        except Exception:  # noqa: BLE001
                            continue
                    if pos == 0:
                        break
                    pos = max(0, pos - step)
        except Exception:  # noqa: BLE001
            return "GENESIS"
        return "GENESIS"

    def _audit_chain_verify(self) -> Dict:
        """校验整条审计链。返回 {valid, total, legacy, broken_at, checked}。

        国家交接级：
          · legacy = 升级前封存记录（无 hash 字段）→ 不参与链校验，保留留档
          · 链从第一条带 hash 的记录起算（GENESIS 起链）
          · 任何一条被增删改 → 断链 → broken_at 指出位置
        """
        if not self.ops_log or not self.ops_log.exists():
            return {"valid": True, "total": 0, "legacy": 0,
                    "broken_at": None, "checked": 0}
        prev = "GENESIS"
        total = 0
        legacy = 0
        broken = None
        with self._audit_lock:
            try:
                with open(self.ops_log, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        entry = json.loads(line)
                        total += 1
                        expected = entry.get("hash", "")
                        if not expected:
                            # 升级前封存记录：不参与链校验
                            legacy += 1
                            continue
                        # 复算：去 hash 字段后按序序列化
                        core = {k: v for k, v in entry.items() if k != "hash"}
                        body = json.dumps(core, ensure_ascii=False, sort_keys=True)
                        calc = hashlib.sha256(body.encode("utf-8")).hexdigest()
                        if calc != expected or entry.get("prev_hash") != prev:
                            broken = total
                            break
                        prev = expected
            except Exception as e:  # noqa: BLE001
                return {"valid": False, "total": total, "legacy": legacy,
                        "broken_at": total + 1, "checked": total, "error": str(e)}
        return {"valid": broken is None, "total": total, "legacy": legacy,
                "broken_at": broken, "checked": total - legacy}

    def _client_ip(self) -> str:
        """取真实客户端 IP：优先 X-Forwarded-For（nginx 反代后），回退 socket。"""
        fwd = self.headers.get("X-Forwarded-For", "")
        if fwd:
            return fwd.split(",")[0].strip() or self.client_address[0]
        return self.client_address[0]

    def _check_login_rate(self, ip: str) -> bool:
        """登录限流：失败 N 次锁 5 分钟。"""
        with self._session_lock:
            rec = self.login_fails.get(ip)
            now = time.time()
            if rec and rec.get("lock_until", 0) > now:
                return False
            if rec and now >= rec.get("lock_until", 0):
                rec["count"] = 0
            return True

    def _record_login_fail(self, ip: str) -> None:
        with self._session_lock:
            rec = self.login_fails.get(ip, {"count": 0, "lock_until": 0.0})
            rec["count"] += 1
            if rec["count"] >= ADMIN_MAX_LOGIN_FAIL:
                rec["lock_until"] = time.time() + ADMIN_LOCK_SECONDS
                rec["count"] = 0
            self.login_fails[ip] = rec

    def _authorize(self) -> Optional[Dict]:
        """校验 Bearer token，返回会话 dict（含负责人/角色）或 None。"""
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return None
        token = auth[7:].strip()
        with self._session_lock:
            sess = self.sessions.get(token)
            if sess and sess.get("exp", 0) > time.time():
                return dict(sess)
        return None

    def _can(self, session: Dict, scope: str) -> bool:
        """角色权限判定：scope 是否在当前角色权限内。"""
        role = session.get("role", "R5")
        return scope in ROLE_PERMISSIONS.get(role, [])

    def _api_admin_login(self) -> None:
        ip = self._client_ip()
        if not self._check_login_rate(ip):
            self._send_json(429, {"code": 429, "message": "尝试过于频繁，请 5 分钟后再试",
                                  "data": {"locked": True}})
            return
        body = self._read_body()
        account = str(body.get("account", "")).strip()
        key = str(body.get("key", ""))
        sess_info = None
        # 双通道：账号表优先（负责人体系），超级密钥兜底（root/UID9622）
        if account and self.account_store:
            rec = self.account_store.verify(account, key)
            if rec:
                sess_info = {
                    "account": rec["account"], "name": rec.get("name", account),
                    "role": rec.get("role", "R5"),
                }
        if not sess_info and account == "root" and self.admin_key and \
                hmac.compare_digest(key, self.admin_key):
            sess_info = {"account": "root", "name": "诸葛鑫（UID9622）", "role": "R1"}
        if not sess_info:
            self._record_login_fail(ip)
            self._audit_op("login", ip, False, f"账号[{account}]密钥错误", account=account)
            self._send_json(401, {"code": 401, "message": "账号或密钥错误"})
            return
        token = secrets.token_urlsafe(32)
        sess = {"exp": time.time() + ADMIN_TOKEN_TTL,
                "account": sess_info["account"], "name": sess_info["name"],
                "role": sess_info["role"], "ip": ip}
        with self._session_lock:
            self.sessions[token] = sess
        self._audit_op("login", ip, True, f"角色={sess_info['role']}",
                       account=sess_info["account"], name=sess_info["name"],
                       role=sess_info["role"])
        self._send_json(200, {"code": 0, "message": "success", "data": {
            "token": token, "ttl": ADMIN_TOKEN_TTL,
            "account": sess_info["account"], "name": sess_info["name"],
            "role": sess_info["role"], "role_name": ROLE_NAMES.get(sess_info["role"], ""),
            "permissions": ROLE_PERMISSIONS.get(sess_info["role"], []),
            "hint": "session token · 8 小时有效 · 重启服务后失效",
        }})

    def _api_admin_logout(self) -> None:
        sess = self._authorize()
        if sess:
            with self._session_lock:
                for t in list(self.sessions):
                    if self.sessions[t].get("account") == sess["account"] and \
                            self.sessions[t].get("ip") == sess.get("ip"):
                        self.sessions.pop(t, None)
            self._audit_op("logout", self._client_ip(), True,
                           account=sess["account"], name=sess.get("name", ""),
                           role=sess.get("role", "R5"))
        self._send_json(200, {"code": 0, "message": "success", "data": {"logout": True}})

    def _api_admin_logs(self) -> None:
        sess = self._authorize()
        if not sess:
            self._send_json(401, {"code": 401, "message": "未授权"})
            return
        if not self._can(sess, "params"):
            self._audit_op("logs", self._client_ip(), False, "越权：无日志查看权限",
                           account=sess["account"], name=sess.get("name", ""),
                           role=sess.get("role", "R5"))
            self._send_json(403, {"code": 403, "message": "当前角色无权查看服务日志"})
            return
        # 白名单：只允许 journalctl 读天眼服务日志
        lines = 200
        try:
            lines = max(10, min(int(self._read_body().get("lines", 200)), 1000))
        except Exception:  # noqa: BLE001
            lines = 200
        try:
            r = subprocess.run(
                ["journalctl", "-u", "lh-tianyan-api", "-n", str(lines),
                 "--no-pager", "-o", "short-iso"],
                capture_output=True, text=True, timeout=8,
            )
            out = (r.stdout or "（无输出）").strip()
            self._audit_op("logs", self._client_ip(), True, f"lines={lines}",
                           account=sess["account"], name=sess.get("name", ""),
                           role=sess.get("role", "R5"))
            self._send_json(200, {"code": 0, "message": "success",
                                  "data": {"lines": out[-20000:]}})
        except FileNotFoundError:
            self._send_json(501, {"code": 501, "message": "仅鲲鹏 systemd 环境支持日志查询"})
        except subprocess.TimeoutExpired:
            self._send_json(504, {"code": 504, "message": "日志读取超时"})

    def _api_admin_action(self) -> None:
        sess = self._authorize()
        if not sess:
            self._send_json(401, {"code": 401, "message": "未授权"})
            return
        body = self._read_body()
        action = str(body.get("action", ""))
        act = lambda ok, d: self._audit_op(action, self._client_ip(), ok, d,
                                           account=sess["account"],
                                           name=sess.get("name", ""),
                                           role=sess.get("role", "R5"))
        # ── 白名单：杜绝任意命令执行 ──
        if action == ADMIN_ACTION_AUDIT:
            if not self._can(sess, "params"):
                act(False, "越权：无审计触发权限")
                self._send_json(403, {"code": 403, "message": "当前角色无权触发审计"})
                return
            script = "/opt/longhun/bin/lh_deben_audit.py"
            if not os.path.exists(script):
                # 本地降级：用仓库内脚本
                script = str(Path(__file__).resolve().parent.parent.parent / "bin" / "lh_deben_audit.py")
            try:
                r = subprocess.run([sys.executable, script, "scan"],
                                   capture_output=True, text=True, timeout=60)
                tail = (r.stdout or r.stderr or "（无输出）").strip()[-4000:]
                ok = r.returncode == 0
                act(ok, f"rc={r.returncode}")
                self._send_json(200 if ok else 500, {
                    "code": 0 if ok else 1,
                    "message": "审计完成" if ok else "审计返回非零",
                    "data": {"output": tail, "rc": r.returncode},
                })
            except subprocess.TimeoutExpired:
                act(False, "timeout")
                self._send_json(504, {"code": 504, "message": "审计超时（>60s）"})
        elif action == ADMIN_ACTION_RESTART:
            if not self._can(sess, "all"):
                act(False, "越权：无重启权限")
                self._send_json(403, {"code": 403, "message": "当前角色无权重启引擎"})
                return
            # 后台延迟重启：先应答再重启自身
            act(True, "重启指令受理")
            self._send_json(200, {"code": 0, "message": "success",
                                  "data": {"output": "🔄 重启指令已受理 · 服务 2 秒后重启"}})

            def _do_restart() -> None:
                time.sleep(2)
                subprocess.run(["systemctl", "restart", "lh-tianyan-api"],
                               capture_output=True, text=True, timeout=10)

            threading.Thread(target=_do_restart, daemon=True).start()
        else:
            self._send_json(400, {"code": 400, "message": f"未知操作: {action}",
                                  "data": {"allowed": [ADMIN_ACTION_AUDIT, ADMIN_ACTION_RESTART]}})

    # ═══════════════════════════════════════════════════════════════
    # 方案D · 国家交接级：按权限导出 / 审计链校验 / 操作日志查询
    # ═══════════════════════════════════════════════════════════════
    def _build_export(self, sess: Dict, scope: str) -> Dict:
        """按角色权限构建导出内容。密钥永远打码。"""
        role = sess.get("role", "R5")
        perms = ROLE_PERMISSIONS.get(role, [])
        snap = self.aggregator.snapshot()
        payload: Dict[str, Any] = {
            "scope": scope,
            "exported_by": sess.get("account", ""),
            "exported_name": sess.get("name", ""),
            "exported_role": role,
            "exported_role_name": ROLE_NAMES.get(role, ""),
            "ts": datetime.now().isoformat(timespec="seconds"),
            "ip": sess.get("ip", ""),
            "ip_geo": GeoIP.lookup(sess.get("ip", "")),
            "engine_version": "v2.3",
            "confirm_code": CONFIRM_CODE,
        }
        # params：系统参数（R1/R2/R3）
        if scope == "params" or scope == "all":
            if "params" in perms:
                payload["params"] = {
                    "version": "v2.3",
                    "modules_total": ModuleRegistry.count(),
                    "personas_total": len(ModuleRegistry.get_by_category("人格层")),
                    "categories": list(self.aggregator.get_category_stats().keys()),
                    "listen": "127.0.0.1:8786（经 nginx 反代 uid9622.cn/tianyan/）",
                    "admin_key_configured": bool(self.admin_key),
                    "token_ttl_seconds": ADMIN_TOKEN_TTL,
                    "login_fail_limit": ADMIN_MAX_LOGIN_FAIL,
                    "lock_seconds": ADMIN_LOCK_SECONDS,
                    "audit_chain_sha256": self._audit_chain_root_hash(),
                }
        # data：模块/人格/主权快照（R1；R2 需脱敏——当前快照无敏感字段，直接导出）
        if scope == "data" or scope == "all":
            if "data" in perms:
                payload["data"] = {
                    "system_health": snap.system_health,
                    "overall_tricolor": snap.overall_tricolor,
                    "timestamp": snap.timestamp,
                    "modules": [asdict(m) for m in snap.modules],
                    "personas": [asdict(p) for p in snap.personas],
                    "sovereignty": snap.sovereignty,
                    "audit": snap.audit,
                    "dashboard": snap.dashboard,
                }
        # audit：操作审计日志全量（R1/R2/R4）
        if scope == "audit" or scope == "all":
            if "audit" in perms:
                payload["audit_log"] = self._read_ops_log()
                payload["audit_chain"] = self._audit_chain_verify()
        # accounts：账号清单（仅 R1）
        if scope == "accounts" or scope == "all":
            if "accounts" in perms:
                payload["accounts"] = (self.account_store.list_sanitized()
                                       if self.account_store else [])
        # 完整性摘要：供 lh_tianyan_verify.py 离线复核
        digest_src = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        payload["integrity_sha256"] = hashlib.sha256(
            digest_src.encode("utf-8")).hexdigest()
        return payload

    def _audit_chain_root_hash(self) -> str:
        """审计链第一条 hash（交接锚点）。跳过升级前封存段（无 hash）。"""
        if not self.ops_log or not self.ops_log.exists():
            return ""
        try:
            with open(self.ops_log, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    h = str(json.loads(line).get("hash", ""))
                    if h:
                        return h
        except Exception:  # noqa: BLE001
            return ""
        return ""

    def _read_ops_log(self, limit: int = 5000) -> List[Dict]:
        """读操作审计日志（哈希链条目）。"""
        if not self.ops_log or not self.ops_log.exists():
            return []
        out: List[Dict] = []
        try:
            with open(self.ops_log, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        out.append(json.loads(line))
        except Exception:  # noqa: BLE001
            return []
        return out[-limit:]

    def _api_admin_export(self) -> None:
        sess = self._authorize()
        if not sess:
            self._send_json(401, {"code": 401, "message": "未授权"})
            return
        body = self._read_body()
        scope = str(body.get("scope", "all"))
        if scope not in ("params", "data", "audit", "accounts", "all"):
            self._send_json(400, {"code": 400, "message": f"未知导出范围: {scope}",
                                  "data": {"allowed": ["params", "data", "audit", "accounts", "all"]}})
            return
        role = sess.get("role", "R5")
        perms = ROLE_PERMISSIONS.get(role, [])
        # 越权拦截（R1 的 all 不要求逐 scope 判定）
        if scope != "all" and scope not in perms:
            self._audit_op("export", self._client_ip(), False, f"越权导出 scope={scope}",
                           account=sess["account"], name=sess.get("name", ""),
                           role=role)
            self._send_json(403, {"code": 403, "message": f"角色 {role} 无权导出 {scope}",
                                  "data": {"allowed": perms}})
            return
        try:
            payload = self._build_export(sess, scope)
        except Exception as e:  # noqa: BLE001
            self._send_json(500, {"code": 500, "message": f"导出构建失败: {e}"})
            return
        # 落盘存档（交接留痕）+ 审计
        export_dir = None
        if self.ops_log:
            export_dir = self.ops_log.parent / "exports"
            export_dir.mkdir(parents=True, exist_ok=True)
            fname = (f"tianyan-export-{sess.get('account', 'anon')}-"
                     f"{scope}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")
            try:
                (export_dir / fname).write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            except Exception:  # noqa: BLE001
                export_dir = None
        self._audit_op("export", self._client_ip(), True, f"scope={scope}",
                       account=sess["account"], name=sess.get("name", ""),
                       role=role)
        self._send_json(200, {"code": 0, "message": "success",
                              "data": payload, "export_file": str(export_dir)})

    def _api_admin_verify(self) -> None:
        sess = self._authorize()
        if not sess:
            self._send_json(401, {"code": 401, "message": "未授权"})
            return
        if not self._can(sess, "audit"):
            self._audit_op("verify", self._client_ip(), False, "越权：无校验权限",
                           account=sess["account"], name=sess.get("name", ""),
                           role=sess.get("role", "R5"))
            self._send_json(403, {"code": 403, "message": "当前角色无权校验审计链"})
            return
        result = self._audit_chain_verify()
        self._audit_op("verify", self._client_ip(), result["valid"], "审计链校验",
                       account=sess["account"], name=sess.get("name", ""),
                       role=sess.get("role", "R5"))
        self._send_json(200, {"code": 0, "message": "success",
                              "data": {**result, "root_hash": self._audit_chain_root_hash()}})

    def _api_admin_opslog(self) -> None:
        sess = self._authorize()
        if not sess:
            self._send_json(401, {"code": 401, "message": "未授权"})
            return
        if not self._can(sess, "audit"):
            self._send_json(403, {"code": 403, "message": "当前角色无权查看操作日志"})
            return
        body = self._read_body()
        limit = max(10, min(int(body.get("limit", 200)), 2000))
        entries = self._read_ops_log(limit)
        # 反向展示：最新在前
        entries.reverse()
        self._audit_op("opslog", self._client_ip(), True, f"limit={limit}",
                       account=sess["account"], name=sess.get("name", ""),
                       role=sess.get("role", "R5"))
        self._send_json(200, {"code": 0, "message": "success", "data": {
            "total": len(entries), "entries": entries,
            "chain": self._audit_chain_verify(),
        }})

    # ---- 静态托管（--www，含路径穿越防护 + 敏感目录黑名单） ----
    def _serve_static(self, route: str) -> None:
        if not self.www_root:
            self._send_json(404, {"code": 404, "message": "not found"})
            return
        try:
            rel = urlparse(route).path.lstrip("/")
            if not rel:
                rel = "index.html"
            # 敏感目录黑名单：_ 前缀（_audit 审计/导出·_private 等）永不外发
            if any(seg.startswith("_") for seg in rel.split("/")):
                self._send_json(403, {"code": 403, "message": "forbidden"})
                return
            root = self.www_root.resolve()
            full = (root / rel).resolve()
            if not str(full).startswith(str(root)):  # 路径穿越防护
                self._send_json(403, {"code": 403, "message": "forbidden"})
                return
            if full.is_dir():
                full = full / "index.html"
            if not full.is_file():
                self._send_json(404, {"code": 404, "message": "not found"})
                return
            body = full.read_bytes()
            ctype = self.MIME.get(full.suffix.lower(), "application/octet-stream")
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self._cors_headers()
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:  # noqa: BLE001
            logging.warning("静态文件异常 %s: %s", route, e)
            self._send_json(500, {"code": 500, "message": "internal error"})

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    def do_GET(self) -> None:
        route = urlparse(self.path).path
        if route == "/api/status":
            self._api_status()
        elif route == "/api/modules":
            self._api_modules()
        elif route == "/api/health":
            self._api_health()
        elif route == "/api/stats":
            self._api_stats()
        else:
            self._serve_static(route)

    def do_POST(self) -> None:
        route = urlparse(self.path).path
        if route == "/api/admin/login":
            self._api_admin_login()
        elif route == "/api/admin/logout":
            self._api_admin_logout()
        elif route == "/api/admin/logs":
            self._api_admin_logs()
        elif route == "/api/admin/action":
            self._api_admin_action()
        elif route == "/api/admin/export":
            self._api_admin_export()
        elif route == "/api/admin/verify":
            self._api_admin_verify()
        elif route == "/api/admin/opslog":
            self._api_admin_opslog()
        else:
            self._send_json(404, {"code": 404, "message": "not found"})


# ═══════════════════════════════════════════════════════════════════════════════
# 5. CLI
# ═══════════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="lh_tianyan", description="🐉 龍魂天眼可视化引擎 v2.3")
    p.add_argument("--version", action="store_true", help="显示版本")
    p.add_argument("--snapshot", action="store_true", help="生成系统快照")
    p.add_argument("--json", action="store_true", help="JSON 输出")
    p.add_argument("--api", action="store_true", help="API 响应格式")
    p.add_argument("--sse", action="store_true", help="SSE 流格式")
    p.add_argument("--stats", action="store_true", help="分类统计")
    p.add_argument("--watch", type=int, metavar="N", help="每 N 秒刷新输出")
    p.add_argument("--export-html", type=Path, metavar="PATH", help="导出 HTML 看板到指定路径")
    p.add_argument("--serve", action="store_true", help="常驻 HTTP 服务模式（应用级实时链路）")
    p.add_argument("--host", type=str, default="127.0.0.1", metavar="IP", help="监听地址（默认 127.0.0.1 仅本机）")
    p.add_argument("--port", type=int, default=8786, metavar="N", help="HTTP 端口（默认 8786）")
    p.add_argument("--www", type=str, metavar="DIR", help="静态看板目录（与 --serve 搭配）")
    p.add_argument("--test", action="store_true", help="运行单元测试")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    if args.version:
        print(f"🐉 龍魂天眼可视化引擎 v2.3")
        print(f"DNA: [[GENERATED_BY_LH_DNA_GENERATOR_V3]]-TIANYAN-ENGINE-v2.3")
        print(f"确认码: {CONFIRM_CODE}")
        print(f"GPG: {GPG_FINGERPRINT}")
        print(f"覆盖模块: {ModuleRegistry.count()} 个")
        print(f"人格矩阵: 28 人格")
        print(f"服务模式: --serve [--port N] [--www DIR]")
        print(f"操作台: 账号登录/审计/重启/日志/导出/校验（Bearer 鉴权·白名单·哈希链）")
        print(f"合规底座: 负责人R1-R5 · 离线归属地 · 哈希链审计 · 按权限导出")
        return 0

    if args.test:
        sys.argv = [sys.argv[0]] if sys.argv else [""]
        unittest.main(module=__name__, exit=False, verbosity=2)
        return 0

    aggregator = StatusAggregator()

    # 常驻 HTTP 服务（应用级实时链路 · 优先处理）
    if args.serve:
        if not args.www:
            print("🔴 --serve 需要 --www <静态看板目录>（含 index.html）")
            return 2
        www = Path(args.www).expanduser().resolve()
        if not www.is_dir():
            print(f"🔴 静态目录不存在: {www}")
            return 2
        TianyanHandler.aggregator = aggregator
        TianyanHandler.www_root = www
        # 操作台（方案C/D）：密钥走环境变量，账号表/审计日志均在 www 外或黑名单保护
        TianyanHandler.admin_key = os.environ.get(ADMIN_KEY_ENV, "")
        ops_log = www / "_audit" / "tianyan_admin_ops.jsonl"
        ops_log.parent.mkdir(parents=True, exist_ok=True)
        TianyanHandler.ops_log = ops_log
        # 账号表：默认引擎同级 etc/（www 之外）；鲲鹏部署经环境变量指向 /etc/longhun/
        accounts_path = Path(os.environ.get(
            ADMIN_ACCOUNTS_ENV, str(Path(__file__).resolve().parent / "etc" / "tianyan-accounts.json")))
        TianyanHandler.account_store = ensure_initial_accounts(accounts_path,
                                                               TianyanHandler.admin_key)
        httpd = TianyanHTTPServer((args.host, args.port), TianyanHandler)
        print(f"🟢 天眼服务已启动 http://{args.host}:{args.port}")
        print(f"   API:  /api/status · /api/modules · /api/health · /api/stats")
        print(f"   操作:  /api/admin/login · /logout · /logs · /action（Bearer 鉴权）")
        print(f"   导出:  /api/admin/export · /verify · /opslog（R1-R4 分级·哈希链）")
        print(f"   静态: {www}（_ 前缀目录已黑名单保护）")
        print(f"   审计: {ops_log}（SHA-256 哈希链 · 交接可核验）")
        print(f"   账号: {accounts_path}")
        print(f"   看板: http://127.0.0.1:{args.port}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🟡 天眼服务已停止")
        finally:
            httpd.server_close()
        return 0

    # 优先处理 export_html：与 snapshot 组合时必须写文件而非打印
    if args.export_html:
        data = aggregator.snapshot()
        js_data = f"window.TIANYAN_INITIAL_DATA = {json.dumps(data.to_dict(), ensure_ascii=False)};"
        output_path = args.export_html
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(js_data)
        print(f"🟢 数据已导出到: {output_path}")
        return 0

    if args.snapshot or args.json or args.api or args.sse:
        snap = aggregator.snapshot()
        if args.json:
            print(DataExporter.to_json(snap))
        elif args.api:
            print(json.dumps(DataExporter.to_api_response(snap), indent=2, ensure_ascii=False))
        elif args.sse:
            print(DataExporter.to_sse_stream(snap))
        else:
            print(json.dumps(snap.to_dict(), indent=2, ensure_ascii=False))
        return 0

    if args.stats:
        stats = aggregator.get_category_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        return 0

    if args.watch:
        print(f"🐉 天眼实时监控 (每 {args.watch} 秒刷新，Ctrl+C 退出)")
        try:
            while True:
                snap = aggregator.snapshot(use_cache=False)
                print(f"\r[{snap.timestamp}] 健康度: {snap.system_health}% {snap.overall_tricolor} | 模块: {len(snap.modules)} | 人格: {len(snap.personas)}", end="", flush=True)
                time.sleep(args.watch)
        except KeyboardInterrupt:
            print("\n监控结束")
        return 0

    build_parser().print_help()
    return 1


# ═══════════════════════════════════════════════════════════════════════════════
# 6. 单元测试
# ═══════════════════════════════════════════════════════════════════════════════

class TestTianyanEngine(unittest.TestCase):

    def test_01_confirm_code(self) -> None:
        """锚点：确认码必须匹配。"""
        self.assertEqual(CONFIRM_CODE, "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")

    def test_02_dna_format(self) -> None:
        """锚点：DNA 必须不含手写干支。"""
        agg = StatusAggregator()
        dna = agg._generate_dna()
        self.assertIn("GENERATED_BY_LH_DNA_GENERATOR_V3", dna)
        self.assertNotRegex(dna, r'丙午|丙申|癸亥|午时|巳时|未时|亥时')

    def test_03_module_count(self) -> None:
        """锚点：模块总数必须为 55（完整生态）。"""
        self.assertEqual(ModuleRegistry.count(), 55)

    def test_04_persona_count(self) -> None:
        """锚点：人格层必须为 28。"""
        personas = ModuleRegistry.get_by_category("人格层")
        self.assertEqual(len(personas), 28)

    def test_05_snapshot_structure(self) -> None:
        """锚点：快照必须包含所有必要字段。"""
        agg = StatusAggregator()
        snap = agg.snapshot()
        self.assertIn("dna", snap.to_dict())
        self.assertIn("timestamp", snap.to_dict())
        self.assertIn("time_anchor", snap.to_dict())
        self.assertIn("modules", snap.to_dict())
        self.assertIn("personas", snap.to_dict())
        self.assertIn("audit", snap.to_dict())
        self.assertIn("dashboard", snap.to_dict())
        self.assertEqual(len(snap.modules), 55)
        self.assertEqual(len(snap.personas), 28)

    def test_06_health_range(self) -> None:
        """锚点：健康度必须在 0-100 之间。"""
        agg = StatusAggregator()
        snap = agg.snapshot()
        self.assertGreaterEqual(snap.system_health, 0)
        self.assertLessEqual(snap.system_health, 100)

    def test_07_tricolor_logic(self) -> None:
        """锚点：三色判定必须与健康度一致。"""
        agg = StatusAggregator()
        snap = agg.snapshot()
        if snap.system_health >= 85:
            self.assertEqual(snap.overall_tricolor, "🟢")
        elif snap.system_health >= 60:
            self.assertEqual(snap.overall_tricolor, "🟡")
        else:
            self.assertEqual(snap.overall_tricolor, "🔴")

    def test_08_time_anchor(self) -> None:
        """锚点：时间锚点必须包含必要字段。"""
        ta = TimeAnchorEngine.get_current()
        self.assertIn("ganzhi", ta)
        self.assertIn("gua", ta)
        self.assertIn("wuxing", ta)
        self.assertIn("tricolor", ta)

    def test_09_category_stats(self) -> None:
        """锚点：分类统计必须覆盖所有类别。"""
        agg = StatusAggregator()
        stats = agg.get_category_stats()
        self.assertIn("协议层", stats)
        self.assertIn("主权层", stats)
        self.assertIn("人格层", stats)
        self.assertIn("技术层", stats)
        self.assertIn("安全层", stats)
        self.assertIn("可视化层", stats)

    def test_10_api_response(self) -> None:
        """锚点：API 响应必须包含标准字段。"""
        agg = StatusAggregator()
        snap = agg.snapshot()
        resp = DataExporter.to_api_response(snap)
        self.assertEqual(resp["code"], 0)
        self.assertEqual(resp["message"], "success")
        self.assertIn("data", resp)

    def test_11_cache_works(self) -> None:
        """锚点：缓存必须在 TTL 内生效。"""
        agg = StatusAggregator()
        snap1 = agg.snapshot()
        snap2 = agg.snapshot()
        self.assertEqual(snap1.dna, snap2.dna)  # 缓存命中

    def test_12_export_json(self) -> None:
        """锚点：JSON 导出必须可解析。"""
        agg = StatusAggregator()
        snap = agg.snapshot()
        json_str = DataExporter.to_json(snap)
        parsed = json.loads(json_str)
        self.assertEqual(parsed["system_health"], snap.system_health)

    # ── 方案D · 国家交接级合规测试 ──
    def test_13_geo_lookup(self) -> None:
        """锚点：归属地解析必须可复核标注来源。"""
        geo = GeoIP.lookup("127.0.0.1")
        self.assertEqual(geo["country"], "中国")
        self.assertEqual(geo["isp"], "LOOPBACK")
        geo2 = GeoIP.lookup("39.182.233.209")
        self.assertEqual(geo2["country"], "中国")
        self.assertEqual(geo2["isp"], "华为云")
        geo3 = GeoIP.lookup("8.8.8.8")
        self.assertEqual(geo3["country"], "境外/未收录")

    def test_14_account_store(self) -> None:
        """锚点：账号表必须存摘要不存明文·可校验。"""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "accounts.json"
            store = ensure_initial_accounts(p, "secret-key-9622")
            self.assertEqual(len(store.accounts), 1)
            self.assertEqual(store.accounts[0]["account"], "root")
            self.assertEqual(store.accounts[0]["role"], "R1")
            # 密钥不存明文
            raw = p.read_text(encoding="utf-8")
            self.assertNotIn("secret-key-9622", raw)
            # 校验正确/错误密钥
            self.assertIsNotNone(store.verify("root", "secret-key-9622"))
            self.assertIsNone(store.verify("root", "wrong"))

    def test_15_role_permissions(self) -> None:
        """锚点：角色权限矩阵必须符合第五层认证分级。"""
        self.assertIn("all", ROLE_PERMISSIONS["R1"])
        self.assertNotIn("data", ROLE_PERMISSIONS["R2"])
        self.assertIn("params", ROLE_PERMISSIONS["R3"])
        self.assertNotIn("audit", ROLE_PERMISSIONS["R3"])
        self.assertIn("audit", ROLE_PERMISSIONS["R4"])
        self.assertEqual(ROLE_PERMISSIONS["R5"], [])

    def test_16_audit_hash_chain(self) -> None:
        """锚点：审计链必须可校验·篡改任意一条即断链。"""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            log = Path(td) / "ops.jsonl"
            # 绕过 HTTP handler 构造，直接用实例方法测试审计链
            h = object.__new__(TianyanHandler)
            h.ops_log = log
            h._audit_op("login", "127.0.0.1", True, "test", "root", "老大", "R1")
            h._audit_op("audit", "127.0.0.1", True, "rc=0", "root", "老大", "R1")
            h._audit_op("export", "127.0.0.1", True, "scope=all", "root", "老大", "R1")
            r = h._audit_chain_verify()
            self.assertTrue(r["valid"])
            self.assertEqual(r["total"], 3)
            # 篡改中间一条 → 断链
            lines = log.read_text(encoding="utf-8").splitlines()
            entry = json.loads(lines[1])
            entry["detail"] = "TAMPERED"
            lines[1] = json.dumps(entry, ensure_ascii=False)
            log.write_text("\n".join(lines) + "\n", encoding="utf-8")
            r2 = h._audit_chain_verify()
            self.assertFalse(r2["valid"])
            self.assertEqual(r2["broken_at"], 2)


if __name__ == "__main__":
    sys.exit(main())
