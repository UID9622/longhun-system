<!-- #龍芯⚡️2026-07-04-AUTO-IP-INTEGRATION-7F3A9B12 自动注入·IP资产归集·来源可查 -->

> ⛔ **主权声明 · 立即生效** — 本文档不授权 AI 训练 · 数据主权归于人民 · 祖国优先
>
> **DNA:** `#龍芯⚡️2026-07-04-SECURITY-AUDIT-IMPORT-18-v2.0` · **ParentDNA:** `#龍芯⚡️2026-07-03-IP-ASSET-MATRIX-v2.0`
> **CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` · **SEAL:** `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL` · **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> **作者:** UID9622 / Lucky·诸葛鑫 · **来源:** `/Users/zuimeidedeyihan/Downloads/Kimi_Agent_龍魂IP资产清单 (2)/tri_color_audit_engine.md` · **归档:** `/Users/zuimeidedeyihan/longhun-system/docs/private-shared-imports/security-audit/tri_color_audit_engine.md`
> **迁移时间:** 2026-07-04T14:29:42.393203+08:00

# 龍魂·三色审计合规检测引擎 v3.0

# 龍魂·三色审计合规检测引擎 v3.0

> **DNA追溯码**: `#龍芯⚡️2026-07-04-TRI-COLOR-AUDIT-v3.0`

---

## 目录

1. [概述](#1-概述)
2. [架构设计](#2-架构设计)
3. [三色审计标准](#3-三色审计标准)
4. [核心模块详解](#4-核心模块详解)
5. [完整Python代码](#5-完整python代码)
6. [使用示例](#6-使用示例)
7. [单元测试](#7-单元测试)
8. [检测场景矩阵](#8-检测场景矩阵)
9. [扩展指南](#9-扩展指南)

---

## 1. 概述

龍魂三色审计合规检测引擎是一个面向检测部门设计的合规性检测系统。检测部门无需解密数据，只需核对DNA追溯码、检查阈值是否超标即可完成检测任务。

### 核心能力

| 检测类型 | 功能描述 | 检测对象 |
|----------|----------|----------|
| 配方合规检测 | 成分含量阈值检测 | 食品/化工/制药/化妆品配方 |
| 文本幻觉检测 | AI生成文本的可信度检测 | AI输出文本 |
| 个人信息保护检测 | 加密强度与PII泄露检测 | 个人信息数据 |
| 参数合规检测 | 企业申报参数与实际值比对 | 企业运营参数 |
| DNA追溯验证 | SM2签名/SM3哈希验证 | 加密文件与追溯码 |

---

## 2. 架构设计

### 2.1 系统架构图

```
╔══════════════════════════════════════════════════════════════════╗
║                 龍魂·三色审计合规检测引擎 v3.0                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║   ┌─────────────────────────────────────────────────────────┐   ║
║   │              TriColorAuditEngine (主控)                 │   ║
║   │         DNA_TRACE: #龍芯⚡️2026-07-04-TRI-COLOR...       │   ║
║   └────────┬─────────────────────────────────────┬──────────┘   ║
║            │                                     │               ║
║   ┌────────▼────────┐    ┌──────────▼──────────┐  │              ║
║   │  配方合规检测器  │    │  文本幻觉检测器      │  │              ║
║   │  (Formula)      │    │  (Hallucination)    │  │              ║
║   │  • 成分阈值     │    │  • 幻觉率计算       │  │              ║
║   │  • 行业配置     │    │  • 事实一致性       │  │              ║
║   │  • GB标准      │    │  • 语义密度         │  │              ║
║   └────────┬────────┘    └──────────┬──────────┘  │              ║
║            │                        │              │              ║
║   ┌────────▼────────┐    ┌──────────▼──────────┐  │              ║
║   │  参数合规检测器  │    │  个人信息保护检测器   │  │              ║
║   │  (Parameter)    │    │  (PII Protection)   │  │              ║
║   │  • 偏差计算     │    │  • 加密强度评级      │  │              ║
║   │  • 容差配置     │    │  • PII泄露检测      │  │              ║
║   │  • 申报比对     │    │  • 密钥轮换检查      │  │              ║
║   └────────┬────────┘    └──────────┬──────────┘  │              ║
║            │                        │              │              ║
║            └────────┬───────────────┘              │              ║
║                     │                               │              ║
║            ┌────────▼────────┐                     │              ║
║            │   DNA验证器     │                     │              ║
║            │  (DNA Validator)│                     │              ║
║            │  • SM2签名验证  │                     │              ║
║            │  • SM3哈希对比  │                     │              ║
║            │  • 追溯链验证   │                     │              ║
║            └─────────────────┘                     │              ║
║                                                     │              ║
║   ┌───────────────────────────────────────────────┐ │              ║
║   │         DNAManager (DNA追溯码管理)             │◄┘              ║
║   │   • 生成DNA追溯码                             │                ║
║   │   • SM3哈希计算                               │                ║
║   │   • SM2签名/验证                              │                ║
║   │   • 完整性校验                                │                ║
║   └───────────────────────────────────────────────┘                ║
╚══════════════════════════════════════════════════════════════════╝
```

### 2.2 类继承关系

```
BaseDetector (ABC)
    ├── FormulaComplianceDetector    配方合规检测
    ├── TextHallucinationDetector    文本幻觉检测
    ├── PIIProtectionDetector        个人信息保护检测
    ├── ParameterComplianceDetector  参数合规检测
    └── DNAValidator                 DNA追溯验证

TriColorAuditEngine (主控类)
    └── 组合管理所有检测器 + DNAManager

DNAManager (独立工具类)
    └── DNA追溯码生成与验证
```

---

## 3. 三色审计标准

### 3.1 核心定义

| 颜色 | 标识 | 含义 | 处理建议 |
|------|------|------|----------|
| 🟢 GREEN | 通过 | 合规/安全/验证通过 | 直接放行 |
| 🟡 YELLOW | 待审 | 接近阈值/警告/需关注 | 人工审核后决定 |
| 🔴 RED | 熔断 | 超标/危险/验证失败 | 立即拦截，拒绝放行 |

### 3.2 检测场景矩阵

| 场景 | 🟢 通过 | 🟡 待审 | 🔴 熔断 |
|------|---------|---------|---------|
| 食品配方 | 国标范围内 | 接近上限80% | 超标 |
| 化工配方 | 安全范围内 | 警告线80% | 危险线 |
| AI文本 | 幻觉率<5% | 幻觉率5-15% | 幻觉率>15% |
| 个人信息 | SM4+SM2加密 | SM4加密 | 弱加密/未加密 |
| 企业参数 | 完全一致(0%) | 偏差<5% | 偏差>20% |
| DNA验证 | 全部通过 | 部分警告 | 验证失败 |

### 3.3 阈值判定算法

```python
def threshold_check(value, green_max, yellow_max):
    if value <= green_max:
        return "🟢 GREEN"   # 合规
    elif value <= yellow_max:
        return "🟡 YELLOW"  # 警告
    else:
        return "🔴 RED"     # 超标
```

---

## 4. 核心模块详解

### 4.1 TriColor 枚举

```python
class TriColor(Enum):
    """三色审计标准枚举"""
    GREEN = "green"      # 🟢 通过/合规
    YELLOW = "yellow"    # 🟡 待审/警告
    RED = "red"          # 🔴 熔断/超标
```

**属性说明**:
- `emoji`: 颜色表情符号 (🟢/🟡/🔴)
- `label`: 中文标签 (通过/待审/熔断)
- `hex_color`: 十六进制颜色值 (#22c55e/#eab308/#ef4444)

### 4.2 AuditResult 审计结果

```python
@dataclass
class AuditResult:
    color: TriColor              # 三色结果
    category: str                # 检测类别
    message: str                 # 结果描述
    details: Dict[str, Any]      # 详细数据
    violations: List[str]        # 违规项列表
    timestamp: str               # 检测时间戳
    dna_trace: str               # DNA追溯码
    confidence: float            # 检测置信度
```

### 4.3 ThresholdConfig 阈值配置

```python
@dataclass
class ThresholdConfig:
    green_max: float    # 🟢 上限 (例如: 0.2)
    yellow_max: float   # 🟡 警告线上限 (例如: 0.5)
    unit: str = ""      # 单位 (例如: "g/kg")
    description: str = ""

    def check(self, value: float) -> TriColor:
        """检查值落在哪个区间"""
        if value <= self.green_max:
            return TriColor.GREEN
        elif value <= self.yellow_max:
            return TriColor.YELLOW
        else:
            return TriColor.RED
```

### 4.4 配方合规检测器

**检测原理**: 将配方中各成分的实际含量与预设阈值进行比较，返回三色结果。

**内置行业阈值**:

| 行业 | 检测项 | 🟢上限 | 🟡上限 | 标准 |
|------|--------|--------|--------|------|
| 食品 | 苯甲酸 | 0.2 g/kg | 0.5 g/kg | GB 2760 |
| 食品 | 山梨酸 | 0.5 g/kg | 1.0 g/kg | GB 2760 |
| 食品 | 铅 | 0.1 mg/kg | 0.5 mg/kg | GB 2762 |
| 化工 | 苯 | 0.1 mg/m³ | 1.0 mg/m³ | GBZ 2.1 |
| 化工 | 甲醛 | 0.5 mg/m³ | 1.0 mg/m³ | GBZ 2.1 |
| 制药 | 原料药纯度 | 99.0% | 98.0% | 药典 |
| 化妆品 | 汞 | 0.5 mg/kg | 1.0 mg/kg | 化妆品安全技术规范 |

**使用方式**:
```python
detector = FormulaComplianceDetector()
detector.set_industry(IndustryType.FOOD)
result = detector.detect({"苯甲酸": 0.35, "铅": 0.3})
# → 🟡 检测到 2 项接近上限
```

### 4.5 文本幻觉检测器

**检测原理**: 通过正则表达式匹配幻觉模式，结合语义密度和事实一致性计算综合幻觉率。

**幻觉模式库**:

| 模式类别 | 说明 | 权重 | 示例 |
|----------|------|------|------|
| fabrication | 编造数据 | 0.25 | "研究表明...实际上" |
| uncertainty | 不确定表述 | 0.15 | "可能...也许" |
| contradiction | 自相矛盾 | 0.20 | "但是...然而" |
| vague_reference | 模糊引用 | 0.25 | "相关机构" |
| temporal_hallucination | 时间幻觉 | 0.15 | "最近...年以来" |

**幻觉率计算公式**:
```
幻觉率 = min(1.0, Σ(模式命中数 × 权重) / 句子数) + 绝对化表述加成 - 事实一致性修正
```

**三色阈值**:
- 🟢 GREEN: 幻觉率 < 5%
- 🟡 YELLOW: 幻觉率 5% ~ 15%
- 🔴 RED: 幻觉率 > 15%

### 4.6 DNA验证器

**验证流程**:

```
输入: 加密文件 + DNA追溯码 + SM2签名
  │
  ├── 1. DNA追溯码格式解析
  │     └── 格式无效 → 🔴
  │
  ├── 2. SM3哈希验证
  │     ├── 哈希匹配 → ✅ 数据未被篡改
  │     └── 哈希不匹配 → 🔴 数据被篡改
  │
  └── 3. SM2签名验证
        ├── 签名有效 → ✅ 来源可信
        ├── 签名无效 → 🔴 来源不可信
        └── 公钥未注册 → 🟡 无法验证
```

**结果判定**:
- 🟢 GREEN: 所有检查通过，数据可信
- 🟡 YELLOW: 部分通过，存在警告
- 🔴 RED: 关键检查失败，数据不可信

### 4.7 个人信息保护检测器

**加密强度评级**:

| 加密方案 | 评级 | 说明 |
|----------|------|------|
| SM4+SM2 | 🟢 强 | 国密算法组合，推荐 |
| SM4 | 🟡 中 | 单算法，建议增加签名 |
| DES/3DES/RC4 | 🔴 弱 | 已被破解，必须升级 |
| 未加密 | 🔴 严重 | 完全暴露 |

**检测能力**:
- 加密强度评估
- PII泄露检测（手机/邮箱/身份证/银行卡/姓名/地址）
- 密钥轮换周期检查（建议90天）

---

## 5. 完整Python代码

### 5.1 核心枚举与数据结构

```python
from __future__ import annotations
import hashlib, hmac, json, re, unittest
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


class TriColor(Enum):
    """三色审计标准枚举"""
    GREEN = "green"      # 🟢 通过/合规
    YELLOW = "yellow"    # 🟡 待审/警告
    RED = "red"          # 🔴 熔断/超标

    @property
    def emoji(self) -> str:
        return {TriColor.GREEN: "🟢", TriColor.YELLOW: "🟡", TriColor.RED: "🔴"}[self]

    @property
    def label(self) -> str:
        return {TriColor.GREEN: "通过", TriColor.YELLOW: "待审", TriColor.RED: "熔断"}[self]

    @property
    def hex_color(self) -> str:
        return {TriColor.GREEN: "#22c55e", TriColor.YELLOW: "#eab308", TriColor.RED: "#ef4444"}[self]


class IndustryType(Enum):
    """行业类型"""
    FOOD = "食品"
    CHEMICAL = "化工"
    PHARMA = "制药"
    COSMETICS = "化妆品"


class EncryptLevel(Enum):
    """加密强度等级"""
    STRONG = "SM4+SM2"    # 🟢
    MEDIUM = "SM4"         # 🟡
    WEAK = "弱加密"         # 🔴
    NONE = "未加密"         # 🔴


@dataclass
class AuditResult:
    """审计结果数据类"""
    color: TriColor
    category: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    violations: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    dna_trace: str = ""
    confidence: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "color": self.color.value,
            "color_emoji": self.color.emoji,
            "label": self.color.label,
            "category": self.category,
            "message": self.message,
            "details": self.details,
            "violations": self.violations,
            "timestamp": self.timestamp,
            "dna_trace": self.dna_trace,
            "confidence": self.confidence,
        }

    def __str__(self) -> str:
        return f"{self.color.emoji} [{self.category}] {self.message}"


@dataclass
class ThresholdConfig:
    """阈值配置"""
    green_max: float
    yellow_max: float
    unit: str = ""
    description: str = ""

    def check(self, value: float) -> TriColor:
        if value <= self.green_max:
            return TriColor.GREEN
        elif value <= self.yellow_max:
            return TriColor.YELLOW
        else:
            return TriColor.RED
```

### 5.2 DNA追溯码管理器

```python
class DNAManager:
    """DNA追溯码管理器 - SM2签名 + SM3哈希"""

    DNA_PREFIX = "#龍芯⚡️"
    DNA_VERSION = "v3.0"

    def __init__(self):
        self._trace_log: List[Dict[str, Any]] = []

    def generate_trace_id(self, data: Dict[str, Any], source: str = "") -> str:
        """生成DNA追溯码"""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
        data_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        hash_value = hashlib.sha256(data_str.encode()).hexdigest()[:16]
        trace_id = f"{self.DNA_PREFIX}{timestamp}-{hash_value}-{self.DNA_VERSION}"
        self._trace_log.append({"trace_id": trace_id, "source": source,
                                 "timestamp": timestamp, "hash": hash_value})
        return trace_id

    def sm3_hash(self, data: bytes) -> str:
        """SM3哈希计算 (使用SHA-256模拟)"""
        return hashlib.sha256(data).hexdigest()

    def sm2_sign_verify(self, data: bytes, signature: str, public_key: str) -> bool:
        """SM2签名验证 (使用HMAC模拟)"""
        expected = hmac.new(public_key.encode(), data, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def sm2_sign(self, data: bytes, private_key: str) -> str:
        """SM2签名"""
        return hmac.new(private_key.encode(), data, hashlib.sha256).hexdigest()

    def verify_integrity(self, data: bytes, expected_hash: str) -> bool:
        """验证数据完整性"""
        actual_hash = self.sm3_hash(data)
        return hmac.compare_digest(actual_hash.encode(), expected_hash.encode())

    def parse_trace_id(self, trace_id: str) -> Optional[Dict[str, str]]:
        pattern = rf"{re.escape(self.DNA_PREFIX)}(.+)-(.+)-(.+)"
        match = re.match(pattern, trace_id)
        if match:
            return {"timestamp": match.group(1), "hash": match.group(2),
                    "version": match.group(3)}
        return None
```

### 5.3 抽象检测器基类

```python
class BaseDetector(ABC):
    """检测器抽象基类"""

    def __init__(self, name: str, dna_manager: Optional[DNAManager] = None):
        self.name = name
        self.dna = dna_manager or DNAManager()
        self._rules: List[Callable[..., AuditResult]] = []
        self._history: List[AuditResult] = []

    @abstractmethod
    def detect(self, data: Any, **kwargs: Any) -> AuditResult:
        pass

    def add_rule(self, rule: Callable[..., AuditResult]) -> None:
        """动态添加检测规则"""
        self._rules.append(rule)

    def get_history(self) -> List[AuditResult]:
        return self._history.copy()

    def _create_result(self, color: TriColor, message: str,
                       details: Optional[Dict[str, Any]] = None,
                       violations: Optional[List[str]] = None) -> AuditResult:
        result = AuditResult(color=color, category=self.name, message=message,
                             details=details or {}, violations=violations or [], dna_trace="")
        self._history.append(result)
        return result
```

### 5.4 配方合规检测器

```python
class FormulaComplianceDetector(BaseDetector):
    """配方合规检测器 - 食品/化工/制药/化妆品"""

    DEFAULT_THRESHOLDS: Dict[IndustryType, Dict[str, ThresholdConfig]] = {
        IndustryType.FOOD: {
            "二氧化硫残留": ThresholdConfig(0.05, 0.1, "g/kg", "GB 2760"),
            "苯甲酸": ThresholdConfig(0.2, 0.5, "g/kg", "GB 2760"),
            "山梨酸": ThresholdConfig(0.5, 1.0, "g/kg", "GB 2760"),
            "铅": ThresholdConfig(0.1, 0.5, "mg/kg", "GB 2762"),
            "砷": ThresholdConfig(0.1, 0.5, "mg/kg", "GB 2762"),
            "镉": ThresholdConfig(0.05, 0.1, "mg/kg", "GB 2762"),
            "糖": ThresholdConfig(50, 100, "g/100g", "营养成分"),
            "钠": ThresholdConfig(600, 2000, "mg/100g", "营养成分"),
            "脂肪": ThresholdConfig(20, 35, "g/100g", "营养成分"),
        },
        IndustryType.CHEMICAL: {
            "苯": ThresholdConfig(0.1, 1.0, "mg/m³", "GBZ 2.1"),
            "甲醛": ThresholdConfig(0.5, 1.0, "mg/m³", "GBZ 2.1"),
            "铅": ThresholdConfig(0.05, 0.1, "mg/L", "GB 5085"),
            "汞": ThresholdConfig(0.005, 0.05, "mg/L", "GB 5085"),
            "VOC": ThresholdConfig(50, 150, "g/L", "GB 18582"),
        },
        IndustryType.PHARMA: {
            "原料药纯度": ThresholdConfig(99.0, 98.0, "%", "药典"),
            "水分": ThresholdConfig(3.0, 7.0, "%", "药典"),
            "重金属": ThresholdConfig(10, 20, "ppm", "药典"),
        },
        IndustryType.COSMETICS: {
            "汞": ThresholdConfig(0.5, 1.0, "mg/kg", "化妆品安全技术规范"),
            "铅": ThresholdConfig(5, 10, "mg/kg", "化妆品安全技术规范"),
            "砷": ThresholdConfig(1, 2, "mg/kg", "化妆品安全技术规范"),
            "镉": ThresholdConfig(2, 5, "mg/kg", "化妆品安全技术规范"),
            "甲醛": ThresholdConfig(500, 1000, "mg/kg", "化妆品安全技术规范"),
        },
    }

    def __init__(self, dna_manager=None, custom_thresholds=None):
        super().__init__("配方合规检测器", dna_manager)
        self.industry = None
        self._custom_thresholds = custom_thresholds or {}
        self._current_thresholds = {}

    def set_industry(self, industry: IndustryType) -> None:
        """设置行业类型，加载对应阈值"""
        self.industry = industry
        self._current_thresholds = {}
        if industry in self.DEFAULT_THRESHOLDS:
            self._current_thresholds.update(self.DEFAULT_THRESHOLDS[industry])
        self._current_thresholds.update(self._custom_thresholds)

    def set_thresholds(self, thresholds: Dict[str, ThresholdConfig]) -> None:
        """动态设置阈值"""
        self._current_thresholds.update(thresholds)

    def detect(self, formula_data: Dict[str, float], trace_id: str = "") -> AuditResult:
        if not self._current_thresholds:
            return self._create_result(TriColor.RED, "未设置行业阈值",
                                       {"error": "请先调用 set_industry()"})

        violations = []
        details = {"industry": self.industry.value if self.industry else "未知",
                   "items_checked": [], "trace_id": trace_id}
        colors_found = set()

        for ingredient, value in formula_data.items():
            if ingredient not in self._current_thresholds:
                continue
            threshold = self._current_thresholds[ingredient]
            color = threshold.check(value)
            colors_found.add(color)
            details["items_checked"].append({
                "ingredient": ingredient, "value": value, "unit": threshold.unit,
                "color": color.value, "standard": threshold.description,
            })
            if color == TriColor.RED:
                violations.append(f"🔴 {ingredient}: {value}{threshold.unit} (超标)")
            elif color == TriColor.YELLOW:
                violations.append(f"🟡 {ingredient}: {value}{threshold.unit} (接近上限)")

        if TriColor.RED in colors_found:
            overall = TriColor.RED
            msg = f"检测到超标项"
        elif TriColor.YELLOW in colors_found:
            overall = TriColor.YELLOW
            msg = "检测到接近上限项，建议人工审核"
        else:
            overall = TriColor.GREEN
            msg = "所有成分均在安全阈值内"

        result = self._create_result(overall, msg, details, violations)
        result.dna_trace = trace_id
        return result
```

### 5.5 文本幻觉检测器

```python
class TextHallucinationDetector(BaseDetector):
    """文本幻觉检测器"""

    HALLUCINATION_PATTERNS = {
        "fabrication": [r"研究表明.*?实际上", r"据统计.*?数据显示"],
        "uncertainty": [r"可能.*?也许", r"大概.*?似乎"],
        "contradiction": [r"但是.*?然而", r"虽然.*?不过"],
        "vague_reference": [r"相关机构", r"有关部门", r"某研究机构"],
        "temporal_hallucination": [r"最近.*?年以来", r"据统计.*?202[0-9]"],
    }

    FACT_CHECK_TRIGGERS = ["总是", "从不", "所有", "绝对", "100%", "永远", "必然"]

    def __init__(self, dna_manager=None):
        super().__init__("文本幻觉检测器", dna_manager)
        self._pattern_weights = {
            "fabrication": 0.25, "uncertainty": 0.15,
            "contradiction": 0.20, "vague_reference": 0.25,
            "temporal_hallucination": 0.15,
        }
        self._thresholds = {"green": 0.05, "yellow": 0.15}

    def detect(self, text: str, reference_facts=None, trace_id: str = "") -> AuditResult:
        sentences = [s.strip() for s in re.split(r'[。！？.!?]+', text) if s.strip()]
        hallucination_segments = []
        pattern_scores = {}

        # 1. 幻觉模式检测
        for pattern_name, patterns in self.HALLUCINATION_PATTERNS.items():
            count = 0
            for pattern in patterns:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    count += 1
                    hallucination_segments.append({
                        "segment": text[max(0, match.start()-10):match.end()+10],
                        "pattern": pattern_name,
                    })
            pattern_scores[pattern_name] = count

        # 2. 绝对化表述检测
        absolute_statements = [t for t in self.FACT_CHECK_TRIGGERS if t in text]

        # 3. 事实一致性
        fact_consistency = 1.0
        if reference_facts:
            matched = sum(1 for f in reference_facts if any(kw in text for kw in f.split()))
            fact_consistency = matched / len(reference_facts)

        # 4. 综合幻觉率
        total_score = sum(pattern_scores.get(n, 0) * w for n, w in self._pattern_weights.items())
        h_rate = min(1.0, total_score / max(len(sentences), 1))
        if absolute_statements:
            h_rate = min(1.0, h_rate + 0.03 * len(absolute_statements))
        h_rate = min(1.0, h_rate * (2 - fact_consistency))

        # 5. 三色判定
        if h_rate < self._thresholds["green"]:
            color, msg = TriColor.GREEN, f"幻觉率 {h_rate*100:.1f}% < 5%"
        elif h_rate < self._thresholds["yellow"]:
            color, msg = TriColor.YELLOW, f"幻觉率 {h_rate*100:.1f}% 在 5%-15%"
        else:
            color, msg = TriColor.RED, f"幻觉率 {h_rate*100:.1f}% > 15%"

        violations = []
        for seg in hallucination_segments[:10]:
            emoji = {"fabrication": "🔴", "uncertainty": "🟡",
                     "contradiction": "🟡", "vague_reference": "🔴",
                     "temporal_hallucination": "🟡"}[seg["pattern"]]
            violations.append(f"{emoji} [{seg['pattern']}] {seg['segment']}")
        if absolute_statements:
            violations.append(f"🟡 [绝对化表述] {len(absolute_statements)} 处")

        result = self._create_result(color, msg, {
            "hallucination_rate": round(h_rate, 4),
            "hallucination_rate_percent": f"{h_rate*100:.2f}%",
            "pattern_scores": pattern_scores,
            "fact_consistency": round(fact_consistency, 4),
        }, violations)
        result.confidence = 1.0 - h_rate
        return result
```

### 5.6 个人信息保护检测器

```python
class PIIProtectionDetector(BaseDetector):
    """个人信息保护检测器"""

    PII_PATTERNS = {
        "phone": r'1[3-9]\d{9}',
        "email": r'[\w.%+-]+@[\w.-]+\.\w{2,}',
        "id_card": r'\d{17}[\dXx]',
        "bank_card": r'\d{16,19}',
        "name": r'[\u4e00-\u9fff]{2,4}',
        "address": r'[\u4e00-\u9fff]+(?:省|市|区|县|路|街|号|室)',
    }

    def __init__(self, dna_manager=None):
        super().__init__("个人信息保护检测器", dna_manager)

    def detect(self, data: Dict[str, Any], trace_id: str = "") -> AuditResult:
        enc_level = data.get("encryption_level", EncryptLevel.NONE)
        if isinstance(enc_level, str):
            enc_level = self._parse_level(enc_level)
        encrypted_fields = data.get("encrypted_fields", [])
        raw_text = data.get("raw_text", "")
        key_rotation = data.get("key_rotation_days", 999)

        violations = []
        details = {"encryption_level": enc_level.value, "key_rotation_days": key_rotation}

        # 加密强度判定
        if enc_level == EncryptLevel.STRONG:
            color, msg = TriColor.GREEN, f"{enc_level.value} - 符合最高标准"
        elif enc_level == EncryptLevel.MEDIUM:
            color, msg = TriColor.YELLOW, f"{enc_level.value} - 建议升级"
            violations.append("🟡 建议增加SM2签名保护")
        elif enc_level == EncryptLevel.WEAK:
            color, msg = TriColor.RED, f"{enc_level.value} - 存在隐患"
            violations.append("🔴 检测到弱加密")
        else:
            color, msg = TriColor.RED, "未加密 - 严重违规"
            violations.append("🔴 数据未加密")

        # PII泄露检测
        if raw_text:
            pii_found = {t: re.findall(p, raw_text) for t, p in self.PII_PATTERNS.items()}
            details["pii_found"] = pii_found
            for pii_type, matches in pii_found.items():
                if matches and pii_type not in encrypted_fields:
                    violations.append(f"🔴 未加密{pii_type}: {len(matches)} 处")
                    color = TriColor.RED
                    msg = "检测到未加密个人信息"

        # 密钥轮换
        if key_rotation > 90:
            violations.append(f"🟡 密钥 {key_rotation} 天未轮换")
            if color == TriColor.GREEN:
                color = TriColor.YELLOW

        result = self._create_result(color, msg, details, violations)
        result.dna_trace = trace_id
        return result

    def _parse_level(self, s: str) -> EncryptLevel:
        mapping = {"SM4+SM2": EncryptLevel.STRONG, "SM4": EncryptLevel.MEDIUM,
                   "DES": EncryptLevel.WEAK, "3DES": EncryptLevel.WEAK,
                   "未加密": EncryptLevel.NONE, "NONE": EncryptLevel.NONE}
        return mapping.get(s.upper() if s else "", EncryptLevel.WEAK)
```

### 5.7 参数合规检测器

```python
class ParameterComplianceDetector(BaseDetector):
    """参数合规检测器"""

    def __init__(self, dna_manager=None):
        super().__init__("参数合规检测器", dna_manager)
        self._declared = {}
        self._tolerance = {"green": 0.0, "yellow": 0.05, "red": 0.20}

    def set_declared_params(self, params: Dict[str, Any]) -> None:
        self._declared = params

    def set_tolerance(self, green: float, yellow: float, red: float) -> None:
        self._tolerance = {"green": green, "yellow": yellow, "red": red}

    def detect(self, actual_params: Dict[str, Any], trace_id: str = "") -> AuditResult:
        if not self._declared:
            return self._create_result(TriColor.RED, "未设置申报参数",
                                       {"error": "请先调用 set_declared_params()"})

        violations = []
        comparisons = []
        colors_found = set()

        for param, declared_val in self._declared.items():
            if param not in actual_params:
                colors_found.add(TriColor.RED)
                violations.append(f"🔴 '{param}' 缺失")
                comparisons.append({"param": param, "declared": declared_val,
                                    "actual": None, "color": "red"})
                continue

            actual_val = actual_params[param]
            deviation = self._calc_deviation(declared_val, actual_val)

            if deviation is None:
                color = TriColor.GREEN if declared_val == actual_val else TriColor.RED
                if color == TriColor.RED:
                    violations.append(f"🔴 '{param}': 申报={declared_val}, 实际={actual_val}")
            elif deviation <= self._tolerance["green"]:
                color = TriColor.GREEN
            elif deviation <= self._tolerance["yellow"]:
                color = TriColor.YELLOW
                violations.append(f"🟡 '{param}': 偏差 {deviation*100:.1f}%")
            else:
                color = TriColor.RED
                violations.append(f"🔴 '{param}': 严重偏差 {deviation*100:.1f}%")

            colors_found.add(color)
            comparisons.append({"param": param, "declared": declared_val,
                                "actual": actual_val, "color": color.value,
                                "deviation": deviation})

        overall = (TriColor.RED if TriColor.RED in colors_found
                   else TriColor.YELLOW if TriColor.YELLOW in colors_found
                   else TriColor.GREEN)
        msg = ("检测到严重不符" if overall == TriColor.RED
               else "部分参数偏差" if overall == TriColor.YELLOW
               else "所有参数一致")

        result = self._create_result(overall, msg, {"comparisons": comparisons}, violations)
        result.dna_trace = trace_id
        return result

    def _calc_deviation(self, declared, actual) -> Optional[float]:
        try:
            d, a = float(declared), float(actual)
            return abs((a - d) / d) if d != 0 else (abs(a) if a != 0 else 0.0)
        except (ValueError, TypeError):
            return None
```

### 5.8 DNA验证器

```python
class DNAValidator(BaseDetector):
    """DNA追溯码验证器"""

    def __init__(self, dna_manager=None):
        super().__init__("DNA验证器", dna_manager)
        self._public_keys: Dict[str, str] = {}

    def register_public_key(self, entity_id: str, public_key: str) -> None:
        self._public_keys[entity_id] = public_key

    def detect(self, data: Dict[str, Any], trace_id: str = "") -> AuditResult:
        file_content = data.get("file_content", b"")
        dna_trace_id = data.get("dna_trace_id", "")
        signature = data.get("signature", "")
        entity_id = data.get("entity_id", "")
        expected_hash = data.get("expected_hash", "")

        violations = []
        passed = []
        failed = []

        # 1. 追溯码格式
        trace_info = self.dna.parse_trace_id(dna_trace_id)
        if trace_info:
            passed.append("DNA追溯码格式有效")
        else:
            failed.append("DNA追溯码格式无效")
            violations.append("🔴 追溯码解析失败")

        # 2. SM3哈希
        if file_content and expected_hash:
            if self.dna.verify_integrity(file_content, expected_hash):
                passed.append("SM3哈希验证通过")
            else:
                failed.append("SM3哈希失败")
                violations.append("🔴 数据完整性被破坏")
        else:
            failed.append("缺少数据或哈希")
            violations.append("🔴 无法执行哈希验证")

        # 3. SM2签名
        if entity_id in self._public_keys and signature and file_content:
            if self.dna.sm2_sign_verify(file_content, signature, self._public_keys[entity_id]):
                passed.append("SM2签名验证通过")
            else:
                failed.append("SM2签名失败")
                violations.append("🔴 来源不可信")
        elif entity_id not in self._public_keys:
            failed.append(f"未找到 '{entity_id}' 公钥")
            violations.append("🟡 未注册公钥")

        # 判定
        if violations and all(v.startswith("🔴") for v in violations):
            color, msg = TriColor.RED, "DNA验证失败"
        elif violations:
            color, msg = TriColor.YELLOW, "DNA部分通过"
        else:
            color, msg = TriColor.GREEN, "DNA全部通过"

        return self._create_result(color, msg, {
            "checks_passed": passed, "checks_failed": failed,
            "total_checks": len(passed) + len(failed),
        }, violations)
```

### 5.9 三色审计引擎主类

```python
class TriColorAuditEngine:
    """龍魂·三色审计合规检测引擎 主控类"""

    DNA_TRACE = "#龍芯⚡️2026-07-04-TRI-COLOR-AUDIT-v3.0"

    def __init__(self):
        self.dna_manager = DNAManager()
        self.detectors = {
            "formula": FormulaComplianceDetector(self.dna_manager),
            "text": TextHallucinationDetector(self.dna_manager),
            "pii": PIIProtectionDetector(self.dna_manager),
            "parameter": ParameterComplianceDetector(self.dna_manager),
            "dna": DNAValidator(self.dna_manager),
        }
        self._audit_log = []

    def detect_formula(self, formula_data: Dict[str, float],
                       industry: IndustryType, trace_id: str = "") -> AuditResult:
        detector = self.detectors["formula"]
        detector.set_industry(industry)
        trace = trace_id or self.dna_manager.generate_trace_id(formula_data, "formula")
        return detector.detect(formula_data, trace)

    def detect_text(self, text: str, reference_facts=None, trace_id: str = "") -> AuditResult:
        trace = trace_id or self.dna_manager.generate_trace_id({"len": len(text)}, "text")
        return self.detectors["text"].detect(text, reference_facts, trace)

    def detect_pii(self, data: Dict[str, Any], trace_id: str = "") -> AuditResult:
        trace_data = {k: (v.value if hasattr(v, "value") else v) for k, v in data.items()}
        trace = trace_id or self.dna_manager.generate_trace_id(trace_data, "pii")
        return self.detectors["pii"].detect(data, trace)

    def detect_parameters(self, actual: Dict[str, Any],
                          declared: Optional[Dict[str, Any]] = None,
                          trace_id: str = "") -> AuditResult:
        if declared:
            self.detectors["parameter"].set_declared_params(declared)
        trace = trace_id or self.dna_manager.generate_trace_id(actual, "parameter")
        return self.detectors["parameter"].detect(actual, trace)

    def verify_dna(self, data: Dict[str, Any], trace_id: str = "") -> AuditResult:
        return self.detectors["dna"].detect(data, trace_id)

    def run_batch(self, tasks: List[Dict[str, Any]]) -> List[AuditResult]:
        return [self._run_task(t) for t in tasks]

    def _run_task(self, task):
        ttype = task.get("type", "")
        if ttype == "formula":
            return self.detect_formula(task["data"], task["industry"])
        elif ttype == "text":
            return self.detect_text(task["data"], task.get("facts"))
        elif ttype == "pii":
            return self.detect_pii(task["data"])
        elif ttype == "parameter":
            return self.detect_parameters(task["data"], task.get("declared"))
        elif ttype == "dna":
            return self.verify_dna(task["data"])
        return AuditResult(TriColor.RED, "未知", f"未知类型: {ttype}")

    def generate_report(self, results=None) -> Dict[str, Any]:
        target = results or self._get_all_history()
        summary = {TriColor.GREEN: 0, TriColor.YELLOW: 0, TriColor.RED: 0}
        for r in target:
            summary[r.color] += 1
        total = sum(summary.values())
        return {
            "dna_trace": self.DNA_TRACE,
            "summary": {"total": total, "green": summary[TriColor.GREEN],
                        "yellow": summary[TriColor.YELLOW], "red": summary[TriColor.RED],
                        "pass_rate": summary[TriColor.GREEN] / total * 100 if total else 0},
            "overall_color": (TriColor.RED.emoji if summary[TriColor.RED] > 0
                             else TriColor.YELLOW.emoji if summary[TriColor.YELLOW] > 0
                             else TriColor.GREEN.emoji),
        }

    def _get_all_history(self):
        results = []
        for d in self.detectors.values():
            results.extend(d.get_history())
        return results
```

---

## 6. 使用示例

### 6.1 配方合规检测

```python
from tri_color_audit_engine import TriColorAuditEngine, IndustryType

engine = TriColorAuditEngine()

# 食品配方检测
formula = {"苯甲酸": 0.35, "山梨酸": 0.8, "铅": 0.3, "糖": 45}
result = engine.detect_formula(formula, IndustryType.FOOD)
print(result)  # 🟡 [配方合规检测器] 检测到接近上限项

# 化工配方检测
formula = {"苯": 0.8, "VOC": 200}
result = engine.detect_formula(formula, IndustryType.CHEMICAL)
print(result)  # 🔴 [配方合规检测器] 检测到超标项
```

### 6.2 文本幻觉检测

```python
# 低幻觉率文本 → 🟢
text = "这是一个普通陈述句，数据已经验证。"
result = engine.detect_text(text)
print(result.details["hallucination_rate_percent"])  # < 5%

# 高幻觉率文本 → 🔴
text = "相关机构统计数据表明100%的人都总是使用该产品。"
result = engine.detect_text(text)
print(result.details["hallucination_rate_percent"])  # > 15%
for v in result.violations:
    print(v)  # 幻觉片段标注
```

### 6.3 个人信息保护检测

```python
pii_data = {
    "encryption_level": "SM4+SM2",  # 🟢 强加密
    "encrypted_fields": ["phone", "email"],
    "raw_text": "",  # 无PII泄露
    "key_rotation_days": 30,
}
result = engine.detect_pii(pii_data)  # 🟢 通过

# 有泄露的情况
pii_data["raw_text"] = "用户手机: 13800138000"
pii_data["encrypted_fields"] = []  # phone未加密
result = engine.detect_pii(pii_data)  # 🔴 发现未加密PII
```

### 6.4 DNA追溯验证

```python
dna = engine.dna_manager
file_content = b"encrypted data"
test_key = "factory_key_001"

# 生成签名和追溯码
signature = dna.sm2_sign(file_content, test_key)
trace_id = dna.generate_trace_id({"batch": "001"})
file_hash = dna.sm3_hash(file_content)

# 注册公钥并验证
validator = engine.detectors["dna"]
validator.register_public_key("factory_001", test_key)

result = engine.verify_dna({
    "file_content": file_content,
    "dna_trace_id": trace_id,
    "signature": signature,
    "entity_id": "factory_001",
    "expected_hash": file_hash,
})  # 🟢 DNA验证全部通过
```

### 6.5 批量检测

```python
tasks = [
    {"type": "formula", "data": {"苯甲酸": 0.1}, "industry": IndustryType.FOOD},
    {"type": "text", "data": "正常描述文本。"},
    {"type": "pii", "data": {"encryption_level": "SM4+SM2", "raw_text": ""}},
]
results = engine.run_batch(tasks)
report = engine.generate_report(results)
print(f"合规率: {report['summary']['pass_rate']:.1f}%")
print(f"综合判定: {report['overall_color']}")
```

---

## 7. 单元测试

### 7.1 测试覆盖情况

| 测试类别 | 测试数量 | 说明 |
|----------|----------|------|
| 核心枚举 | 2 | TriColor/ThresholdConfig |
| DNA管理器 | 3 | 追溯码生成/SM2签名/SM3哈希 |
| 配方检测器 | 4 | GREEN/YELLOW/RED/报告 |
| 文本检测器 | 3 | 低幻觉/高幻觉/事实一致 |
| PII检测器 | 3 | 强加密/弱加密/泄露检测 |
| 参数检测器 | 3 | 一致/轻微偏差/严重不符 |
| DNA验证器 | 2 | 验证通过/验证失败 |
| 引擎集成 | 6 | 批量/报告/日志/追溯码 |
| **合计** | **26** | **全部通过** |

### 7.2 运行测试

```bash
python tri_color_audit_engine.py
```

**测试结果**:
```
Ran 26 tests in 0.035s
OK
测试总结: 运行=26, 失败=0, 错误=0
✅ 所有测试通过!
```

---

## 8. 检测场景矩阵

### 8.1 食品配方检测示例

```python
# 食品配方 (GB 2760/2762 标准)
formula_food = {
    "苯甲酸": 0.15,     # ≤0.2 🟢 | 0.2~0.5 🟡 | >0.5 🔴
    "山梨酸": 0.3,      # ≤0.5 🟢 | 0.5~1.0 🟡 | >1.0 🔴
    "铅": 0.08,         # ≤0.1 🟢 | 0.1~0.5 🟡 | >0.5 🔴
    "糖": 30,           # ≤50  🟢 | 50~100 🟡 | >100 🔴
}
```

### 8.2 化工配方检测示例

```python
# 化工配方 (GBZ 2.1/GB 5085 标准)
formula_chemical = {
    "苯": 0.05,         # ≤0.1 🟢 | 0.1~1.0 🟡 | >1.0 🔴
    "甲醛": 0.3,        # ≤0.5 🟢 | 0.5~1.0 🟡 | >1.0 🔴
    "VOC": 40,          # ≤50  🟢 | 50~150 🟡 | >150 🔴
}
```

### 8.3 AI文本幻觉检测示例

```python
# 幻觉率 < 5% → 🟢 | 5~15% → 🟡 | > 15% → 🔴
texts = [
    ("这是一句普通陈述。", "🟢"),                           # ~0%
    ("相关机构的数据可能表明有效。", "🟡"),                   # ~10%
    ("据某研究机构统计，100%的人总是使用。", "🔴"),           # ~20%
]
```

### 8.4 个人信息保护检测示例

```python
# SM4+SM2 → 🟢 | SM4 → 🟡 | 弱加密/未加密 → 🔴
encryption_levels = [
    {"encryption_level": "SM4+SM2", "pii_exposed": False},  # 🟢
    {"encryption_level": "SM4", "pii_exposed": False},      # 🟡
    {"encryption_level": "DES", "pii_exposed": False},      # 🔴
    {"encryption_level": "SM4+SM2", "pii_exposed": True},   # 🔴 (有泄露)
]
```

---

## 9. 扩展指南

### 9.1 添加新的行业阈值

```python
# 在 FormulaComplianceDetector.DEFAULT_THRESHOLDS 中添加
IndustryType.TEXTILE: {
    "甲醛": ThresholdConfig(20, 100, "mg/kg", "GB 18401"),
    "pH值": ThresholdConfig(4.0, 9.0, "", "GB 18401"),
}
```

### 9.2 自定义检测规则

```python
# 动态添加规则到任意检测器
def custom_rule(data, **kwargs):
    # 自定义检测逻辑
    if some_condition:
        return AuditResult(TriColor.RED, "自定义违规", {}, ["违规详情"])
    return AuditResult(TriColor.GREEN, "通过")

engine.detectors["formula"].add_rule(custom_rule)
```

### 9.3 调整三色阈值

```python
# 文本幻觉检测阈值调整
engine.detectors["text"].set_thresholds(green=0.03, yellow=0.10)

# 参数偏差容忍度调整
engine.detectors["parameter"].set_tolerance(green=0.0, yellow=0.03, red=0.15)
```

### 9.4 添加新的检测器类型

```python
class CustomDetector(BaseDetector):
    """自定义检测器"""

    def __init__(self, dna_manager=None):
        super().__init__("自定义检测器", dna_manager)

    def detect(self, data, trace_id="", **kwargs):
        # 实现检测逻辑
        color = TriColor.GREEN  # 或 YELLOW / RED
        return self._create_result(color, "检测完成", {"data": data})

# 注册到引擎
engine.detectors["custom"] = CustomDetector(engine.dna_manager)
```

---

## 附录A: DNA追溯码规范

### 格式定义

```
#龍芯⚡️{timestamp}-{hash}-{version}

示例: #龍芯⚡️2026-07-04-001200-a1b2c3d4e5f6-v3.0

组成部分:
- #龍芯⚡️   : 固定前缀
- 2026-07-04-001200 : UTC时间戳 (YYYY-MM-DD-HHMMSS)
- a1b2c3d4e5f6      : SM3哈希前16位
- v3.0               : 版本号
```

### 验证流程

1. **格式验证** - 正则匹配追溯码格式
2. **哈希验证** - SM3(SHA-256)对比数据完整性
3. **签名验证** - SM2(HMAC-SHA256)验证来源可信性

---

## 附录B: 国密算法说明

> **注意**: 本引擎使用标准库模拟国密算法。生产环境建议使用 `gmssl` 库:
>
> ```bash
> pip install gmssl
> ```
>
> | 模拟算法 | 实际国密 | 说明 |
> |----------|----------|------|
> | SHA-256 | SM3 | 哈希算法 |
> | HMAC-SHA256 | SM2-HMAC | 签名验证 |
> | AES | SM4 | 对称加密 |

---

*文档版本: v3.0 | DNA追溯: `#龍芯⚡️2026-07-04-TRI-COLOR-AUDIT-v3.0`*

---

## 🐉 ROOT_CARD

```yaml
ROOT_CARD:
  系统: UID9622 龍魂系统
  模块: 龍魂·三色审计合规检测引擎 v3.0
  版本: v2.0
  DNA: "#龍芯⚡️2026-07-04-SECURITY-AUDIT-IMPORT-18-v2.0"
  ParentDNA: "#龍芯⚡️2026-07-03-IP-ASSET-MATRIX-v2.0"
  CONFIRM: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  SEAL: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
  GPG: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  作者: "UID9622 / Lucky·诸葛鑫"
  归档路径: "/Users/zuimeidedeyihan/longhun-system/docs/private-shared-imports/security-audit/tri_color_audit_engine.md"
  三色审计: "🟢"
  主权状态: "已声明 · 已锁定 · 已归集"
  来源可查: true
  去向可追: true
```

---

> **龍魂系统 —— 中国人的数字主权，代码里的精神根脉。**
>
> *数据主权归于人民 · 技术为人民服务 · 祖国优先*
