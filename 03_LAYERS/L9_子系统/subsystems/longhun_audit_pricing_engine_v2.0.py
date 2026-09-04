#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂审计定价引擎 v2.0 + 支付网关 + 投资池
DNA: #龍芯⚡️丙午·甲午·乙亥·壬午·䷚颐-LONGHUN-PRICING-ENGINE-v2.0-UID9622
归属: 龍魂系统 · UID9622
原则:
  - 定价稳定、可预期：地板/天花板/日变更限速，不随情绪乱变
  - 基数大、现金流厚：订阅 + 阶梯用量 + 企业定制
  - 成本透明、利润可投：每笔审计计算真实成本，结余进入投资池
  - 主权归人民：所有资金流 DNA 可追溯，用户数据不出境

相对 v1.0 的升级：
  1. 持久化：用户/订单/交易/审计记录全部落盘
  2. 订阅生命周期：月费、续费、到期降级、自动扣费
  3. 稳定动态定价： floor/cap/阶梯/日变更限速
  4. 成本模型：计算每次审计的算力/存储/模型成本
  5. 投资池：可投资结余单独记账
  6. 支付 webhook：支持支付宝/微信/数字人民币回调结构
  7. DNA 追溯：每笔交易、每次审计都有 DNA 码
  8. 财务看板：MRR、ARPU、保本点、投资池余额
"""

import argparse
import hashlib
import json
import os
import secrets
import sys
import threading
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# 引入 DNA 與語義引擎
sys.path.insert(0, str(Path.home() / "longhun-system" / "scripts"))
try:
    from 龍魂DNA主權引擎 import DnaSovereigntyEngine
except Exception:
    DnaSovereigntyEngine = None
try:
    from 龍魂語義歸一化閘門 import KnowledgeBaseGate
except Exception:
    KnowledgeBaseGate = None


# ---------- 路徑配置 ----------
ENGINE_DIR = Path.home() / ".龍魂" / "pricing_engine_v2"
CONFIG_PATH = ENGINE_DIR / "config.json"
USERS_PATH = ENGINE_DIR / "users.json"
ORDERS_PATH = ENGINE_DIR / "orders.jsonl"
TRANSACTIONS_PATH = ENGINE_DIR / "transactions.jsonl"
AUDIT_RECORDS_PATH = ENGINE_DIR / "audit_records.jsonl"
PRICING_STATE_PATH = ENGINE_DIR / "pricing_state.json"

DNA_PREFIX = "#龍芯⚡️"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _dna(event: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    rand = secrets.token_hex(4).upper()
    return f"{DNA_PREFIX}{ts}-PRICING-{event}-{rand}"


def _ensure_dir() -> None:
    ENGINE_DIR.mkdir(parents=True, exist_ok=True)


# ---------- 數據持久化 ----------
class AtomicJsonStore:
    """線程安全的 JSON 原子寫入"""

    def __init__(self, path: Path):
        self.path = path
        self.lock = threading.Lock()
        _ensure_dir()

    def load(self, default: Any) -> Any:
        with self.lock:
            if not self.path.exists():
                return default
            try:
                return json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                return default

    def save(self, data: Any) -> None:
        with self.lock:
            tmp = self.path.with_suffix(".tmp")
            tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            tmp.replace(self.path)


class JsonlStore:
    """線程安全的 JSONL 追加"""


    def append(self, record: dict[str, Any]) -> None:
        with self.lock:
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def load(self, limit: int = 0) -> List[dict[str, Any]]:
        records = []
        if not self.path.exists():
            return records
        with self.lock:
            with self.path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        records.append(json.loads(line))
                    except Exception:
                        continue
        if limit > 0:
            return records[-limit:]
        return records


# ---------- 配置 ----------
@dataclass
class 定价配置:
    脱氧核糖核酸锚定: str = "#龍芯⚡️丙午·甲午·乙亥·壬午·䷚颐-LONGHUN-PRICING-ENGINE-v2.0-UID9622"
    主人标识: str = "UID9622"

    # 基础定价
    基础单价: float = 0.01
    最低单价: float = 0.005
    最高单价: float = 0.05
    单日最大调价幅度: float = 0.10

    # 阶梯用量折扣（当月累计审计次数）
    阶梯折扣: List[Dict[str, Any]] = field(default_factory=lambda: [
        {"threshold": 0, "discount": 0.0},
        {"threshold": 1000, "discount": 0.10},
        {"threshold": 10000, "discount": 0.20},
        {"threshold": 100000, "discount": 0.35},
    ])

    # 月费套餐
    套餐: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "个人体验级": {"月费": 0.0, "免费次数": 0, "超出单价": 0.01, "人数限制": 1, "含报告": False},
        "轻度使用级": {"月费": 9.9, "免费次数": 100, "超出单价": 0.01, "人数限制": 1, "含报告": False},
        "高频使用级": {"月费": 99.0, "免费次数": 999999, "超出单价": 0.0, "人数限制": 5, "含报告": False},
        "专业团队级": {"月费": 599.0, "免费次数": 999999, "超出单价": 0.0, "人数限制": 20, "含报告": True},
        "生态共建级": {"月费": 0.0, "免费次数": 999999, "超出单价": 0.0, "人数限制": 999999, "含报告": True, "定制": True},
    })

    # 成本模型（元/次审计）
    单次算力成本: float = 0.002
    单次存储成本: float = 0.0005
    单次模型成本: float = 0.001
    单次带宽成本: float = 0.0003

    # 固定成本
    服务器月成本: float = 300.0
    保底储备比例: float = 0.30
    投资池分配比例: float = 0.70

    # 动态定价触发阈值（活跃用户数）
    活跃用户少于100调价幅度: float = 0.20
    活跃用户少于50调价幅度: float = 0.50
    活跃用户大于500调价幅度: float = -0.20
    活跃用户大于2000调价幅度: float = -0.40

    # 支付
    默认支付通道: str = "支付宝"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "定价配置":
        return cls(**d)


class 配置存儲:
    def __init__(self):
        self.store = AtomicJsonStore(CONFIG_PATH)

    def load(self) -> 定价配置:
        data = self.store.load(None)
        if data is None:
            cfg = 定价配置()
            self.save(cfg)
            return cfg
        return 定价配置.from_dict(data)

    def save(self, cfg: 定价配置) -> None:
        self.store.save(cfg.to_dict())


# ---------- 用户等级 ----------
class 用户等级(Enum):
    个人体验级 = "个人体验级"
    轻度使用级 = "轻度使用级"
    高频使用级 = "高频使用级"
    专业团队级 = "专业团队级"
    生态共建级 = "生态共建级"


@dataclass
class 用户账户:
    用户标识: str
    等级: str = "个人体验级"
    余额: float = 0.0
    本月已用次数: int = 0
    本月免费次数已用: int = 0
    注册时间: str = field(default_factory=_now)
    订阅开始时间: str = ""
    订阅到期时间: str = ""
    最后审计时间: str = ""
    累计审计次数: int = 0
    累计消费金额: float = 0.0
    累计支付金额: float = 0.0
    自定义单价: float = 0.0
    团队人数: int = 1
    状态: str = "active"
    脱氧核糖核酸: str = field(default_factory=lambda: _dna("USER-REGISTER"))


    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "用户账户":
        return cls(**d)


class 用户庫:
    def __init__(self):
        self.store = AtomicJsonStore(USERS_PATH)
        self.lock = threading.Lock()

    def load_all(self) -> Dict[str, 用户账户]:
        data = self.store.load({})
        return {uid: 用户账户.from_dict(info) for uid, info in data.items()}

    def save_all(self, users: Dict[str, 用户账户]) -> None:
        self.store.save({uid: u.to_dict() for uid, u in users.items()})

    def get(self, users: Dict[str, 用户账户], 用户标识: str) -> 用户账户:
        if 用户标识 not in users:
            users[用户标识] = 用户账户(用户标识=用户标识)
        return users[用户标识]


# ---------- 订阅管理 ----------
class 订阅管理器:
    def __init__(self, cfg: 定价配置):
        self.cfg = cfg

    def 月费(self, 等级: str) -> float:
        return self.cfg.套餐.get(等级, {}).get("月费", 0.0)

    def 是否订阅有效(self, user: 用户账户) -> bool:
        if not user.订阅到期时间:
            return user.等级 == "个人体验级"
        return datetime.fromisoformat(user.订阅到期时间) > datetime.now(timezone.utc)

    def 检查并续费(self, user: 用户账户) -> Dict[str, Any]:
        if user.等级 == "个人体验级":
            return {"成功": True, "动作": "无", "原因": "个人体验级无需续费"}
        if self.是否订阅有效(user):
            return {"成功": True, "动作": "无", "原因": "订阅仍有效"}
        费用 = self.月费(user.等级)
        if user.余额 >= 费用:
            user.余额 -= 费用
            user.订阅开始时间 = _now()
            user.订阅到期时间 = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
            user.本月已用次数 = 0
            user.本月免费次数已用 = 0
            return {"成功": True, "动作": "自动续费", "费用": 费用}
        # 余额不足 -> 降级到个人体验级
        user.等级 = "个人体验级"
        user.订阅到期时间 = ""
        user.本月已用次数 = 0
        user.本月免费次数已用 = 0
        return {"成功": True, "动作": "降级", "原因": "余额不足，已降级至个人体验级"}

    def 升级(self, user: 用户账户, 新等级: str) -> Dict[str, Any]:
        if 新等级 not in self.cfg.套餐:
            return {"成功": False, "原因": f"无效等级: {新等级}"}
        费用 = self.月费(新等级)
        if user.余额 < 费用:
            return {"成功": False, "原因": f"余额不足，需要 ¥{费用:.2f}"}
        user.余额 -= 费用
        user.等级 = 新等级
        user.订阅开始时间 = _now()
        user.订阅到期时间 = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
        user.本月已用次数 = 0
        user.本月免费次数已用 = 0
        return {"成功": True, "动作": "升级", "费用": 费用, "新等级": 新等级}


# ---------- 稳定动态定价 ----------
class 动态定价引擎:
    """稳定动态定价：地板/天花板/阶梯/日变更限速"""

    def __init__(self, cfg: 定价配置):
        self.cfg = cfg
        self.state_store = AtomicJsonStore(PRICING_STATE_PATH)
        self.state = self._load_state()

    def _load_state(self) -> dict[str, Any]:
        return self.state_store.load({
            "当前单价": self.cfg.基础单价,
            "最后调整日期": "",
            "价格历史": [],
        })

    def _save_state(self) -> None:
        self.state_store.save(self.state)

    def 当前单价(self) -> float:
        return float(self.state.get("当前单价", self.cfg.基础单价))

    def 计算动态单价(self, 当月活跃用户数: int) -> float:
        基础 = self.cfg.基础单价
        调整 = 0.0
        if 当月活跃用户数 < 50:
            调整 = self.cfg.活跃用户少于50调价幅度
        elif 当月活跃用户数 < 100:
            调整 = self.cfg.活跃用户少于100调价幅度
        elif 当月活跃用户数 >= 2000:
            调整 = self.cfg.活跃用户大于2000调价幅度
        elif 当月活跃用户数 >= 500:
            调整 = self.cfg.活跃用户大于500调价幅度

        当前 = self.当前单价()
        目标 = round(基础 * (1 + 调整), 4)

        # 日变更限速
        今天 = _today()
        if self.state.get("最后调整日期") == 今天:
            上限 = round(当前 * (1 + self.cfg.单日最大调价幅度), 4)
            下限 = round(当前 * (1 - self.cfg.单日最大调价幅度), 4)
            目标 = min(上限, max(下限, 目标))
        else:
            self.state["最后调整日期"] = 今天

        # floor / cap
        目标 = max(self.cfg.最低单价, min(self.cfg.最高单价, 目标))

        self.state["当前单价"] = 目标
        self.state.setdefault("价格历史", []).append({
            "时间": _now(),
            "活跃用户数": 当月活跃用户数,
            "调整": 调整,
            "新单价": 目标,
        })
        self._save_state()
        return 目标

    def 用户单次价格(self, user: 用户账户, 累计次数: int = 0) -> float:
        """结合套餐、阶梯折扣、自定义单价返回本次审计价格"""
        套餐 = self.cfg.套餐.get(user.等级, {})

        # 定制套餐
        if 套餐.get("定制"):
            return user.自定义单价

        # 免费额度内
        if user.本月已用次数 < 套餐.get("免费次数", 0):
            return 0.0

        # 超出按动态单价 + 阶梯折扣
        单价 = self.当前单价()
        折扣 = 0.0
        for tier in sorted(self.cfg.阶梯折扣, key=lambda x: x["threshold"], reverse=True):
            if 累计次数 >= tier["threshold"]:
                折扣 = tier["discount"]
                break
        return round(单价 * (1 - 折扣), 4)


# ---------- 成本模型 ----------
class 成本模型:

    def 单次审计成本(self) -> float:
        return round(
            self.cfg.单次算力成本
            + self.cfg.单次存储成本
            + self.cfg.单次模型成本
            + self.cfg.单次带宽成本,
            4,
        )

    def 分析(self, 当月审计次数: int, 当月收入: float) -> Dict[str, Any]:
        单次成本 = self.单次审计成本()
        变动成本 = 当月审计次数 * 单次成本
        总成本 = self.cfg.服务器月成本 + 变动成本
        毛利 = 当月收入 - 总成本
        保本次数 = int((self.cfg.服务器月成本 / (self.cfg.基础单价 - 单次成本)))
        return {
            "单次审计成本": 单次成本,
            "变动成本": round(变动成本, 2),
            "固定成本": round(self.cfg.服务器月成本, 2),
            "总成本": round(总成本, 2),
            "当月收入": round(当月收入, 2),
            "毛利": round(毛利, 2),
            "是否保本": 毛利 >= 0,
            "保本审计次数": 保本次数,
            "可投资结余": round(max(0, 毛利 * self.cfg.投资池分配比例), 2),
            "储备金": round(max(0, 毛利 * self.cfg.保底储备比例), 2),
        }


# ---------- 支付网关 ----------
class 支付网关:
    def __init__(self, cfg: 定价配置):
        self.cfg = cfg
        self.orders = JsonlStore(ORDERS_PATH)
        self.transactions = JsonlStore(TRANSACTIONS_PATH)

    def 创建订单(self, 用户标识: str, 金额: float, 商品描述: str, 支付通道: str = "") -> Dict[str, Any]:
        通道 = 支付通道 or self.cfg.默认支付通道
        订单号 = f"LH{int(time.time()*1000)}{hashlib.md5(f'{用户标识}{time.time()}'.encode()).hexdigest()[:6]}"
        订单 = {
            "订单号": 订单号,
            "用户标识": 用户标识,
            "金额": 金额,
            "商品描述": 商品描述,
            "支付通道": 通道,
            "状态": "待支付",
            "创建时间": _now(),
            "支付链接": "",
            "回调数据": {},
            "脱氧核糖核酸": _dna("ORDER"),
        }
        if 通道 == "支付宝":
            订单["支付链接"] = f"https://qr.alipay.com/_mock_{订单号}"
        elif 通道 == "微信支付":
            订单["支付链接"] = f"weixin://wxpay/_mock_{订单号}"
        elif 通道 == "数字人民币":
            订单["支付链接"] = f"dcep://_mock_{订单号}"
        else:
            订单["状态"] = "支付通道不支持"
        self.orders.append(订单)
        return 订单

    def 查询订单(self, 订单号: str) -> Optional[Dict[str, Any]]:
        for o in self.orders.load():
            if o.get("订单号") == 订单号:
                return o
        return None

    def 确认收款(self, 订单号: str, 回调数据: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        order = self.查询订单(订单号)
        if not order:
            return {"成功": False, "原因": "订单不存在"}
        if order["状态"] != "待支付":
            return {"成功": False, "原因": f"订单状态为 {order['状态']}"}
        order["状态"] = "已支付"
        order["支付时间"] = _now()
        if 回调数据:
            order["回调数据"] = 回调数据
        self.orders.append(order)
        return {"成功": True, "订单": order}

    def 退款(self, 订单号: str, 金额: Optional[float] = None) -> Dict[str, Any]:
        order = self.查询订单(订单号)
        if not order or order["状态"] != "已支付":
            return {"成功": False, "原因": "订单不存在或未支付"}
        退款金额 = 金额 or order["金额"]
        退款单 = {
            "退款单号": f"REF{订单号}",
            "原订单号": 订单号,
            "退款金额": 退款金额,
            "时间": _now(),
            "脱氧核糖核酸": _dna("REFUND"),
        }
        self.transactions.append(退款单)
        return {"成功": True, "退款": 退款单}

    def 处理Webhook(self, 通道: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """接入真实支付宝/微信/数字人民币回调的结构入口"""
        订单号 = payload.get("out_trade_no") or payload.get("订单号")
        if not 订单号:
            return {"成功": False, "原因": "缺少订单号"}
        return self.确认收款(订单号, {"通道": 通道, "payload": payload})


# ---------- 审计计费器 ----------
class 审计计费器:
    def __init__(self, cfg: 定价配置, 定价引擎: 动态定价引擎, 支付网关: 支付网关, 成本模型: 成本模型):
        self.cfg = cfg
        self.定价引擎 = 定价引擎
        self.支付网关 = 支付网关
        self.成本模型 = 成本模型
        self.records = JsonlStore(AUDIT_RECORDS_PATH)
        self.transactions = JsonlStore(TRANSACTIONS_PATH)

    def 执行审计(self, user: 用户账户, 审计内容: str, 审计来源: str = "api") -> Dict[str, Any]:
        # 续费/降级检查
        sub_mgr = 订阅管理器(self.cfg)
        sub_mgr.检查并续费(user)

        单价 = self.定价引擎.用户单次价格(user, user.累计审计次数)

        if user.余额 < 单价 and 单价 > 0:
            return {"成功": False, "原因": "余额不足", "当前余额": user.余额, "所需": 单价}

        if 单价 > 0:
            user.余额 -= 单价
            user.累计消费金额 += 单价
            self.transactions.append({
                "dna": _dna("AUDIT-CHARGE"),
                "时间": _now(),
                "用户标识": user.用户标识,
                "类型": "审计扣费",
                "金额": -单价,
                "余额": user.余额,
            })

        user.本月已用次数 += 1
        user.累计审计次数 += 1
        if 单价 == 0.0 and user.等级 != "个人体验级":
            user.本月免费次数已用 += 1
        user.最后审计时间 = _now()

        单次成本 = self.成本模型.单次审计成本()
        record = {
            "审计标识": _dna("AUDIT"),
            "用户标识": user.用户标识,
            "审计内容摘要": 审计内容[:100],
            "单价": 单价,
            "单次成本": 单次成本,
            "毛利": round(单价 - 单次成本, 4),
            "余额": user.余额,
            "来源": 审计来源,
            "时间": _now(),
        }
        self.records.append(record)

        return {
            "成功": True,
            "审计标识": record["审计标识"],
            "扣费": 单价,
            "单次成本": 单次成本,
            "余额": user.余额,
            "本月已用": user.本月已用次数,
        }


# ---------- 财务看板 ----------
class 财务看板:
    def __init__(self, cfg: 定价配置, 定价引擎: 动态定价引擎):
        self.cfg = cfg
        self.定价引擎 = 定价引擎
        self.users = 用户庫()
        self.orders = JsonlStore(ORDERS_PATH)
        self.records = JsonlStore(AUDIT_RECORDS_PATH)
        self.transactions = JsonlStore(TRANSACTIONS_PATH)
        self.cost = 成本模型(cfg)

    def 汇总(self) -> Dict[str, Any]:
        all_users = self.users.load_all()
        orders = self.orders.load()
        audit_records = self.records.load()

        付费用户数 = sum(1 for u in all_users.values() if u.累计支付金额 > 0)
        活跃订阅数 = sum(1 for u in all_users.values() if u.等级 != "个人体验级")
        总审计次数 = len(audit_records)
        总收入 = sum(o.get("金额", 0) for o in orders if o.get("状态") == "已支付")
        总余额 = sum(u.余额 for u in all_users.values())

        当月收入 = self._当月收入()
        成本分析 = self.cost.分析(len(self._当月审计()), 当月收入)

        mrr = sum(self.cfg.套餐.get(u.等级, {}).get("月费", 0) for u in all_users.values())
        arpu = round(总收入 / max(付费用户数, 1), 2)

        return {
            "总用户数": len(all_users),
            "付费用户数": 付费用户数,
            "活跃订阅数": 活跃订阅数,
            "总审计次数": 总审计次数,
            "总收入": round(总收入, 2),
            "用户总余额": round(总余额, 2),
            "MRR(月经常性收入)": round(mrr, 2),
            "ARPU(每用户平均收入)": arpu,
            "当前动态单价": self.定价引擎.当前单价(),
            "成本与利润": 成本分析,
            "投资池余额": self._投资池余额(),
        }

    def _当月审计(self) -> List[dict[str, Any]]:
        本月 = datetime.now(timezone.utc).strftime("%Y-%m")
        return [r for r in self.records.load() if r.get("时间", "").startswith(本月)]

    def _当月收入(self) -> float:
        本月 = datetime.now(timezone.utc).strftime("%Y-%m")
        return sum(
            o.get("金额", 0)
            for o in self.orders.load()
            if o.get("状态") == "已支付" and o.get("支付时间", "").startswith(本月)
        )

    def _投资池余额(self) -> float:
        # 简化：累计可投资结余 = 所有审计记录毛利 * 投资池比例 - 已转出（本demo不实现转出）
        毛利 = sum(r.get("毛利", 0) for r in self.records.load())
        return round(max(0, 毛利 * self.cfg.投资池分配比例), 2)


# ---------- 机器人接口 ----------
class 机器人定价接口:
    def __init__(self):
        self.cfg_store = 配置存儲()
        self.cfg = self.cfg_store.load()
        self.users = 用户庫()
        self.定价引擎 = 动态定价引擎(self.cfg)
        self.支付网关 = 支付网关(self.cfg)
        self.成本模型 = 成本模型(self.cfg)
        self.计费器 = 审计计费器(self.cfg, self.定价引擎, self.支付网关, self.成本模型)
        self.订阅管理 = 订阅管理器(self.cfg)
        self.财务 = 财务看板(self.cfg, self.定价引擎)
        self._user_cache: Dict[str, 用户账户] = {}
        self._cache_lock = threading.Lock()

    def _user(self, 用户标识: str) -> 用户账户:
        with self._cache_lock:
            if 用户标识 not in self._user_cache:
                all_users = self.users.load_all()
                self._user_cache = all_users
            return self.users.get(self._user_cache, 用户标识)

    def _persist(self) -> None:
        with self._cache_lock:
            self.users.save_all(self._user_cache)

    # ---- 命令 ----
    def 命令_价格(self, 用户标识: str) -> str:
        当前 = self.定价引擎.当前单价()
        lines = ["🐉 龍魂审计定价 v2.0"]
        for name, info in self.cfg.套餐.items():
            if info.get("定制"):
                lines.append(f"| {name} | 协商定制 | 不限次·含报告·大客户")
            else:
                lines.append(
                    f"| {name} | ¥{info['月费']}/月 | 免费{info['免费次数']}次 | 超出¥{info['超出单价']}/次 | 限{info['人数限制']}人"
                )
        lines.append(f"\n当前动态单价: ¥{当前}/次")
        lines.append(f"单价区间: ¥{self.cfg.最低单价} ~ ¥{self.cfg.最高单价}")
        lines.append(f"日调价限速: ±{self.cfg.单日最大调价幅度*100:.0f}%")
        return "\n".join(lines)

    def 命令_充值(self, 用户标识: str, 金额: float, 支付通道: str = "支付宝") -> str:
        订单 = self.支付网关.创建订单(用户标识, 金额, "账户充值", 支付通道)
        return f"""🐉 充值订单已创建
订单号: {订单['订单号']}
金额: ¥{金额:.2f}
通道: {支付通道}
请支付: {订单['支付链接']}
支付后回复: 确认支付 {订单['订单号']}"""

    def 命令_确认支付(self, 用户标识: str, 订单号: str) -> str:
        r = self.支付网关.确认收款(订单号)
        if not r["成功"]:
            return f"🔴 {r['原因']}"
        订单 = r["订单"]
        user = self._user(用户标识)
        user.余额 += 订单["金额"]
        user.累计支付金额 += 订单["金额"]
        self._persist()
        return f"""🐉 充值成功
订单号: {订单号}
金额: ¥{订单['金额']:.2f}
当前余额: ¥{user.余额:.2f}
DNA: {订单['脱氧核糖核酸']}"""

    def 命令_余额(self, 用户标识: str) -> str:
        user = self._user(用户标识)
        return f"""🐉 账户余额
用户: {用户标识}
等级: {user.等级}
余额: ¥{user.余额:.2f}
本月已用: {user.本月已用次数} 次
累计审计: {user.累计审计次数} 次
累计消费: ¥{user.累计消费金额:.2f}
DNA: {user.脱氧核糖核酸}"""

    def 命令_升级(self, 用户标识: str, 目标等级: str) -> str:
        user = self._user(用户标识)
        r = self.订阅管理.升级(user, 目标等级)
        self._persist()
        if not r["成功"]:
            return f"🔴 {r['原因']}"
        return f"""🐉 升级成功
新等级: {目标等级}
费用: ¥{r['费用']:.2f}
到期时间: {user.订阅到期时间[:10]}
余额: ¥{user.余额:.2f}"""

    def 命令_审计(self, 用户标识: str, 审计内容: str) -> str:
        user = self._user(用户标识)
        r = self.计费器.执行审计(user, 审计内容, "bot")
        self._persist()
        if not r["成功"]:
            return f"🔴 {r['原因']}\n余额: ¥{r['当前余额']:.2f} 所需: ¥{r['所需']:.2f}"
        return f"""🐉 审计完成
审计标识: {r['审计标识']}
扣费: ¥{r['扣费']:.2f}
单次成本: ¥{r['单次成本']:.2f}
余额: ¥{r['余额']:.2f}
本月已用: {r['本月已用']} 次"""

    def 命令_账单(self, 用户标识: str, 条数: int = 10) -> str:
        txs = [t for t in self.计费器.transactions.load() if t.get("用户标识") == 用户标识]
        lines = [f"🐉 最近 {min(条数, len(txs))} 条账单"]
        for t in reversed(txs[-条数:]):
            lines.append(f"- {t['时间'][:19]} {t['类型']} ¥{t['金额']:.2f} 余额¥{t['余额']:.2f}")
        return "\n".join(lines)

    def 命令_看板(self, 用户标识: str = "UID9622") -> str:
        # 仅创始人可查看全局财务
        if 用户标识 != self.cfg.主人标识:
            return "🔴 仅创始人可查看财务看板"
        s = self.财务.汇总()
        return f"""🐉 财务看板
总用户数: {s['总用户数']}
付费用户数: {s['付费用户数']}
活跃订阅数: {s['活跃订阅数']}
总审计次数: {s['总审计次数']}
总收入: ¥{s['总收入']:.2f}
MRR: ¥{s['MRR(月经常性收入)']:.2f}
ARPU: ¥{s['ARPU(每用户平均收入)']:.2f}
当前动态单价: ¥{s['当前动态单价']:.4f}
投资池余额: ¥{s['投资池余额']:.2f}
保本点: {s['成本与利润']['保本审计次数']} 次/月
是否保本: {'✅' if s['成本与利润']['是否保本'] else '❌'}
可投资结余: ¥{s['成本与利润']['可投资结余']:.2f}"""


# ---------- CLI ----------
def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂审计定价引擎 v2.0")
    sub = parser.add_subparsers(dest="cmd")

    p_price = sub.add_parser("price", help="查看价格")
    p_price.add_argument("--user", default="UID9622")

    p_charge = sub.add_parser("charge", help="创建充值订单")
    p_charge.add_argument("--user", default="UID9622")
    p_charge.add_argument("--amount", type=float, default=100.0)
    p_charge.add_argument("--channel", default="支付宝")

    p_confirm = sub.add_parser("confirm", help="确认支付")
    p_confirm.add_argument("--user", default="UID9622")
    p_confirm.add_argument("--order", required=True)

    p_balance = sub.add_parser("balance", help="查询余额")
    p_balance.add_argument("--user", default="UID9622")

    p_upgrade = sub.add_parser("upgrade", help="升级套餐")
    p_upgrade.add_argument("--user", default="UID9622")
    p_upgrade.add_argument("--tier", default="轻度使用级")

    p_audit = sub.add_parser("audit", help="执行审计")
    p_audit.add_argument("--user", default="UID9622")
    p_audit.add_argument("--content", default="检测内容合规性")

    p_dashboard = sub.add_parser("dashboard", help="财务看板")
    p_dashboard.add_argument("--user", default="UID9622")

    p_dynamic = sub.add_parser("dynamic", help="调整动态单价")
    p_dynamic.add_argument("--active-users", type=int, default=1000)

    args = parser.parse_args()
    api = 机器人定价接口()

    if args.cmd == "price":
        print(api.命令_价格(args.user))
    elif args.cmd == "charge":
        print(api.命令_充值(args.user, args.amount, args.channel))
    elif args.cmd == "confirm":
        print(api.命令_确认支付(args.user, args.order))
    elif args.cmd == "balance":
        print(api.命令_余额(args.user))
    elif args.cmd == "upgrade":
        print(api.命令_升级(args.user, args.tier))
    elif args.cmd == "audit":
        print(api.命令_审计(args.user, args.content))
    elif args.cmd == "dashboard":
        print(api.命令_看板(args.user))
    elif args.cmd == "dynamic":
        price = api.定价引擎.计算动态单价(args.active_users)
        print(f"活跃用户数: {args.active_users} -> 动态单价: ¥{price:.4f}")
    else:
        parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
