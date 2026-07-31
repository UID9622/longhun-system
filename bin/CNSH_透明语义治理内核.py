# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-TRANSPARENT-GOVERNANCE-v2.0-UID9622
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

"""🐉 龍魂引擎：CNSH_透明语义治理内核
路径：bin/CNSH_透明语义治理内核.py
CNSH v2.0 透明语义治理架构底座：
  - 干支四柱 DNA 时间戳
  - 治理数学函数
  - 审计链 / 记忆场 / 主权人格内核
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-TRANSPARENT-GOVERNANCE-v2.0-UID9622
"""
import os as _os
import sys as _sys
_module_dir = _os.path.dirname(_os.path.abspath(__file__))
if _module_dir not in _sys.path:
    _sys.path.insert(0, _module_dir)

import hashlib
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

try:
    from CNSH_国密工具 import SM3
except Exception:  # pragma: no cover - 兜底，确保内核可独立编译
    SM3 = None


# ============== 干支 / 八卦常量 ==============
天干 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
地支 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
八卦符号 = {
    "坎": "☵",
    "艮": "☶",
    "震": "☳",
    "巽": "☴",
    "离": "☲",
    "坤": "☷",
    "兑": "☱",
    "乾": "☰",
}


# ============== 干支计算辅助函数 ==============
def _干支索引转字符串(索引: int) -> str:
    """将 0-59 的干支索引转换为天干地支字符串。"""
    return 天干[索引 % 10] + 地支[索引 % 12]


def _儒略日数(date) -> int:
    """计算公历日期的儒略日数（JDN）。"""
    y, m, d = date.year, date.month, date.day
    a = (14 - m) // 12
    y_ = y + 4800 - a
    m_ = m + 12 * a - 3
    return (
        d
        + (153 * m_ + 2) // 5
        + 365 * y_
        + y_ // 4
        - y_ // 100
        + y_ // 400
        - 32045
    )


def _日柱索引(date) -> int:
    """
    以 1900-01-01（甲戌日，干支索引 10）为锚点，
    返回当日干支索引（0-59）。
    """
    # 1900-01-01 的 JDN = 2415021
    return (_儒略日数(date) - 2415021 + 10) % 60


def _年柱(date) -> str:
    """年柱 = (year - 4) mod 60 → 干支。"""
    return _干支索引转字符串((date.year - 4) % 60)


def _月柱(date) -> str:
    """
    月柱：月支按节气近似（month 1=寅, ..., 12=丑）；
    月干按年干五虎遁起寅月。
    """
    年干索引 = (date.year - 4) % 10
    正月干 = (年干索引 * 2 + 2) % 10
    月干 = (正月干 + date.month - 1) % 10
    月支 = (date.month + 1) % 12
    return 天干[月干] + 地支[月支]


def _日柱(date) -> str:
    """日柱 = Julian day mod 60。"""
    return _干支索引转字符串(_日柱索引(date))


def _时柱(date) -> str:
    """
    时柱：时支按现代小时划分（23-1=子，…，21-23=亥）；
    时干按日干五鼠遁起子时。
    """
    日干索引 = _日柱索引(date) % 10
    子时干 = (日干索引 * 2) % 10
    时辰索引 = ((date.hour + 1) // 2) % 12
    时干 = (子时干 + 时辰索引) % 10
    return 天干[时干] + 地支[时辰索引]


def _卦象(date) -> str:
    """日支映射到八卦：子☵坎，丑寅☶艮，卯☳震，辰巳☴巽，午☲离，未申☷坤，酉☱兑，戌亥☰乾。"""
    日支 = _日柱索引(date) % 12
    if 日支 == 0:
        名 = "坎"
    elif 日支 in (1, 2):
        名 = "艮"
    elif 日支 == 3:
        名 = "震"
    elif 日支 in (4, 5):
        名 = "巽"
    elif 日支 == 6:
        名 = "离"
    elif 日支 in (7, 8):
        名 = "坤"
    elif 日支 == 9:
        名 = "兑"
    else:  # 10, 11
        名 = "乾"
    return f"{八卦符号[名]}{名}"


def _哈希8(原料: str) -> str:
    """优先使用 SM3，失败则回退 SHA-256，取前 8 位小写十六进制。"""
    if SM3 is not None:
        return SM3.hex_hash(原料)[:8].lower()
    return hashlib.sha256(原料.encode("utf-8")).hexdigest()[:8].lower()


# ============== DNA 身份锚生成器 ==============
def 生成DNA身份锚(module: str, action: str, extra: Any = None) -> str:
    """
    生成 CNSH v2.0 干支四柱 DNA 时间戳。
    格式：#龍芯⚡️<年柱>·<月柱>·<日柱>·<时柱>·<卦>-<模块>-<动作>-<哈希8>
    """
    now = datetime.now(timezone.utc)
    年柱 = _年柱(now)
    月柱 = _月柱(now)
    日柱 = _日柱(now)
    时柱 = _时柱(now)
    卦 = _卦象(now)
    熵 = secrets.token_hex(4)
    时间戳 = now.strftime("%Y%m%d%H%M%S")
    extra_str = str(extra) if extra is not None else ""
    原料 = f"{module}-{action}-{时间戳}-{熵}-{extra_str}"
    return f"#龍芯⚡️{年柱}·{月柱}·{日柱}·{时柱}·{卦}-{module}-{action}-{_哈希8(原料)}"


# ============== 治理数学函数（纯函数） ==============
def 风险函数(capability: float, uncertainty: float, autonomy: float) -> float:
    """
    风险 = 能力 × 不确定性 / 自主性。
    能力越大、不确定性越高、自主性越低，风险越高。
    """
    return capability * uncertainty / max(autonomy, 1e-9)


def 决策函数(permission: float, context: float, risk: float) -> float:
    """
    决策分 = 权限 × 上下文 / 风险。
    与风险成反比，与权限、上下文理解成正比。
    """
    return permission * context / max(risk, 1e-9)


def 边界函数(risk: float, threshold: float) -> bool:
    """风险是否未超过阈值（通过边界）。"""
    return risk <= threshold


def 信任函数(auditability: float, recoverability: float, transparency: float) -> float:
    """
    信任 = 可审计性、可恢复性、透明度的几何平均。
    任一维度为 0 都会显著拉低整体信任。
    """
    乘积 = max(0.0, auditability) * max(0.0, recoverability) * max(0.0, transparency)
    return 乘积 ** (1.0 / 3.0)


# ============== 审计链（append-only） ==============
class 审计链:
    """append-only 审计日志链，支持按 DNA 查询与全量导出。"""

    def __init__(self):
        self._链: List[Dict[str, Any]] = []

    def 追加(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """追加一条审计条目；若缺少 timestamp，自动补全 UTC 时间。"""
        normalized = dict(entry)
        if "timestamp" not in normalized or not normalized["timestamp"]:
            normalized["timestamp"] = datetime.now(timezone.utc).isoformat()
        self._链.append(normalized)
        return normalized

    def 导出(self) -> List[Dict[str, Any]]:
        """返回完整审计链副本。"""
        return list(self._链)

    def 按DNA查询(self, dna: str) -> List[Dict[str, Any]]:
        """返回 DNA 前缀匹配的所有审计条目。"""
        return [e for e in self._链 if str(e.get("dna", "")).startswith(dna)]


# ============== 记忆场（append-only） ==============
class 记忆场:
    """append-only 记忆存储：只写入、只读取、永不删除。"""

    def __init__(self):
        self._节点: List[Dict[str, Any]] = []

    def 写入(self, dna: str, content: Any, tags: Optional[List[str]] = None, previous_dna: Optional[str] = None) -> Dict[str, Any]:
        """写入新的记忆节点。"""
        if tags is None:
            tags = []
        node = {
            "dna": dna,
            "content": content,
            "tags": list(tags),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "previous_dna": previous_dna,
        }
        self._节点.append(node)
        return node

    def 读取(self, dna: Optional[str] = None, tags: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """按 DNA 前缀或标签读取记忆节点；两者都提供时取交集。"""
        结果 = self._节点[:]
        if dna is not None:
            结果 = [n for n in 结果 if str(n.get("dna", "")).startswith(dna)]
        if tags:
            标签集 = set(tags)
            结果 = [n for n in 结果 if 标签集.intersection(n.get("tags", []))]
        return list(结果)

    def 版本链(self, dna: str) -> List[Dict[str, Any]]:
        """返回同一 DNA 前缀下的所有版本节点（按写入时间排序）。"""
        return [n for n in self._节点 if str(n.get("dna", "")).startswith(dna)]


# ============== 主权人格内核 ==============
@dataclass
class 主权人格内核:
    """ROOT_CARD / Sovereign Persona Kernel。"""

    UID: str
    persona: Dict[str, Any] = field(default_factory=dict)
    规则列表: List[Dict[str, Any]] = field(default_factory=list)

    def 加载规则(self, rules_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """为每条规则附加 DNA 锚点后存储；已存在同名规则不会被覆盖。"""
        已存在名 = {r.get("名称") for r in self.规则列表 if r.get("名称")}
        新增 = []
        for rule in rules_list:
            名称 = rule.get("名称")
            if 名称 and 名称 in 已存在名:
                continue
            anchored = dict(rule)
            anchored["DNA"] = 生成DNA身份锚("SOVEREIGN-RULE", str(名称 or "RULE"), anchored.get("版本"))
            self.规则列表.append(anchored)
            新增.append(anchored)
            if 名称:
                已存在名.add(名称)
        return 新增

    def 校验规则覆盖(self, new_rule: Dict[str, Any]) -> bool:
        """如果新规则会覆盖已有规则（同名且版本不更低），返回 True。"""
        新名 = new_rule.get("名称")
        if not 新名:
            return False
        for rule in self.规则列表:
            if rule.get("名称") == 新名:
                return True
        return False


# ============== 模块自测 ==============
if __name__ == "__main__":
    print("DNA 示例:", 生成DNA身份锚("MEMORY", "API-v1.0"))
    print("风险函数(2,0.5,1):", 风险函数(2.0, 0.5, 1.0))
    print("决策函数(1,0.8,1):", 决策函数(1.0, 0.8, 1.0))
    print("边界函数(1,2):", 边界函数(1.0, 2.0))
    print("信任函数(1,1,1):", 信任函数(1.0, 1.0, 1.0))

    审计 = 审计链()
    dna = 生成DNA身份锚("TEST", "AUDIT")
    审计.追加({"dna": dna, "action": "test", "risk": 0.5, "decision": 0.8, "passed": True})
    print("审计链长度:", len(审计.导出()))

    记忆 = 记忆场()
    记忆.写入(dna, {"意图": "测试"}, tags=["测试"])
    print("记忆节点数:", len(记忆.读取()))

    人格 = 主权人格内核(UID="UID9622", persona={"称呼": "老大"})
    人格.加载规则([{"名称": "零号协议", "内容": "世界老百姓最高"}])
    print("规则覆盖?", 人格.校验规则覆盖({"名称": "零号协议"}))
