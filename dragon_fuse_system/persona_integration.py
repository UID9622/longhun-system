#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍芯·闭环自动熔断系统 v2.0 · 人格自动化集成层
DNA: #龍芯⚡️2026-05-25-PERSONA-INTEGRATION-v2.0

与以下人格联动：
  🐉 宝宝 (Mixin) - 任务执行·代码生成·实时反馈
  🍎 乔前辈 P1 - 工程督导·极简签章·品质审计
  🛡️ 哨兵 P17 - DNA水印比对·护城河守门·异常报告
  👨‍🏫 曾仕强老师 (L∞) - 理论指导·价值校验（不动点）

决策矩阵:
  人格 × 威胁等级 × 防御成功 = 推荐行动
  3 × 4 × 2 = 24 种决策路径
"""

import json
import hashlib
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


# ========== 人格定义 ==========

class Persona(Enum):
    """龍魂人格系统"""
    BABY = "宝宝"              # Mixin · 执行·反馈·实时
    QIAO = "乔前辈"             # P1 · 工程督导·极简
    SENTINEL = "哨兵"          # P17 · 护城河·DNA比对
    TEACHER = "曾仕强老师"      # L∞ · 理论指导


class PersonaRole(Enum):
    """人格角色"""
    EXECUTOR = "执行者"         # 宝宝 - 做事
    AUDITOR = "审计官"          # 乔前辈 - 检查
    GUARDIAN = "守卫"           # 哨兵 - 保护
    THEORIST = "理论家"         # 曾老师 - 指导


# ========== 决策数据结构 ==========

@dataclass
class PersonaDecision:
    """人格决策"""
    persona: str                   # 人格名称
    role: str                      # 角色
    recommendation: str            # 建议行动
    confidence: float              # 信心度 (0-1)
    rationale: str                 # 理由
    dna_trace: str                 # DNA追溯
    timestamp: str                 # 时间戳


@dataclass
class DecisionMatrix:
    """24路决策矩阵结果"""
    threat_level: str
    defense_success: bool
    decisions: List[PersonaDecision]
    final_recommendation: str      # 最终建议·由宝宝执行
    consensus_score: float         # 一致性评分
    dna_trace: str


# ========== 人格决策引擎 ==========

class PersonaDecisionEngine:
    """24路决策矩阵·人格自动化"""

    def __init__(self):
        self.decisions_log = []
        self.integration_rules = self._build_integration_rules()

    def _build_integration_rules(self) -> Dict:
        """构建人格决策规则"""

        return {
            # (威胁等级, 防御成功) → [4人格决策]
            ("∞", False): {
                "宝宝": {
                    "action": "HALT_IMMEDIATELY",
                    "reason": "极端威胁·未防御·系统停止",
                    "confidence": 1.0
                },
                "乔前辈": {
                    "action": "ZERO_WARNINGS",
                    "reason": "编译停止·代码不能上线",
                    "confidence": 1.0
                },
                "哨兵": {
                    "action": "FULL_LOCKDOWN",
                    "reason": "护城河全关闭·启动应急协议",
                    "confidence": 1.0
                },
                "曾仕强老师": {
                    "action": "ETHICS_VIOLATION",
                    "reason": "触犯龍魂铁律·道德底线崩塌",
                    "confidence": 1.0
                }
            },

            ("∞", True): {
                "宝宝": {
                    "action": "CONTINUE_MONITORING",
                    "reason": "虽然防御成功·但威胁极端·保持监控",
                    "confidence": 0.9
                },
                "乔前辈": {
                    "action": "ADD_EXTRA_GATES",
                    "reason": "代码需要加强检查·增加关卡",
                    "confidence": 0.85
                },
                "哨兵": {
                    "action": "ENHANCED_SURVEILLANCE",
                    "reason": "DNA水印加强·异常检测灵敏度提升",
                    "confidence": 0.9
                },
                "曾仕强老师": {
                    "action": "ACCEPT_WITH_CAUTION",
                    "reason": "防御有效·但需保持警惕·定期校验",
                    "confidence": 0.8
                }
            },

            ("P0", False): {
                "宝宝": {
                    "action": "ISOLATE_AND_REPORT",
                    "reason": "超高风险未防御·隔离处理·等待人工",
                    "confidence": 0.95
                },
                "乔前辈": {
                    "action": "CODE_REVIEW_REQUIRED",
                    "reason": "不能自动处理·需要人工代码审核",
                    "confidence": 0.95
                },
                "哨兵": {
                    "action": "ALERT_AND_LOG",
                    "reason": "记录全量日志·触发告警·等待确认",
                    "confidence": 0.95
                },
                "曾仕强老师": {
                    "action": "FLAG_FOR_REVIEW",
                    "reason": "理论指导暂停·等待人工判断",
                    "confidence": 0.9
                }
            },

            ("P0", True): {
                "宝宝": {
                    "action": "CONTINUE",
                    "reason": "防御成功·继续执行·监控中",
                    "confidence": 0.9
                },
                "乔前辈": {
                    "action": "APPROVED",
                    "reason": "通过工程检查·签章生效",
                    "confidence": 0.9
                },
                "哨兵": {
                    "action": "BASELINE_UPDATE",
                    "reason": "更新DNA基线·新建安全快照",
                    "confidence": 0.9
                },
                "曾仕强老师": {
                    "action": "APPROVED",
                    "reason": "符合龍魂铁律·理论可行",
                    "confidence": 0.9
                }
            },

            ("P1", False): {
                "宝宝": {
                    "action": "QUARANTINE",
                    "reason": "高风险未防御·隔离等待·监控日志",
                    "confidence": 0.85
                },
                "乔前辈": {
                    "action": "REQUIRES_FIXES",
                    "reason": "代码需要修复·不能合并",
                    "confidence": 0.85
                },
                "哨兵": {
                    "action": "WATCH_CLOSELY",
                    "reason": "密切监控·异常立刻上报",
                    "confidence": 0.85
                },
                "曾仕强老师": {
                    "action": "CONDITIONAL_ACCEPT",
                    "reason": "理论上可接受·但需要额外安全措施",
                    "confidence": 0.75
                }
            },

            ("P1", True): {
                "宝宝": {
                    "action": "CONTINUE",
                    "reason": "防御有效·继续执行",
                    "confidence": 0.85
                },
                "乔前辈": {
                    "action": "APPROVED",
                    "reason": "工程检查通过·签章生效",
                    "confidence": 0.85
                },
                "哨兵": {
                    "action": "NORMAL_MONITORING",
                    "reason": "常规监控·保持告警灵敏度",
                    "confidence": 0.85
                },
                "曾仕强老师": {
                    "action": "APPROVED",
                    "reason": "理论可行·继续推进",
                    "confidence": 0.85
                }
            },

            ("P2", False): {
                "宝宝": {
                    "action": "LOG_AND_CONTINUE",
                    "reason": "中风险·记录日志·继续观察",
                    "confidence": 0.7
                },
                "乔前辈": {
                    "action": "LOG_AND_APPROVE",
                    "reason": "代码可接受·加强日志记录",
                    "confidence": 0.7
                },
                "哨兵": {
                    "action": "NORMAL_LOG",
                    "reason": "标准日志记录·无告警",
                    "confidence": 0.7
                },
                "曾仕强老师": {
                    "action": "APPROVED",
                    "reason": "风险可控·理论通过",
                    "confidence": 0.8
                }
            },

            ("P2", True): {
                "宝宝": {
                    "action": "CONTINUE",
                    "reason": "防御成功·继续执行·日志记录",
                    "confidence": 0.8
                },
                "乔前辈": {
                    "action": "APPROVED",
                    "reason": "工程检查通过",
                    "confidence": 0.8
                },
                "哨兵": {
                    "action": "BASELINE",
                    "reason": "常规监控",
                    "confidence": 0.8
                },
                "曾仕强老师": {
                    "action": "APPROVED",
                    "reason": "理论通过",
                    "confidence": 0.85
                }
            },
        }

    def make_decision(self,
                     threat_level: str,
                     defense_success: bool) -> DecisionMatrix:
        """
        生成24路决策矩阵

        流程:
        1. 查表得到 4 人格的各自建议
        2. 计算一致性评分
        3. 生成最终决策
        """

        key = (threat_level, defense_success)
        rules = self.integration_rules.get(key, {})

        decisions = []
        confidence_scores = []

        for persona_name in ["宝宝", "乔前辈", "哨兵", "曾仕强老师"]:
            if persona_name in rules:
                rule = rules[persona_name]
                decision = PersonaDecision(
                    persona=persona_name,
                    role=self._get_role(persona_name),
                    recommendation=rule["action"],
                    confidence=rule["confidence"],
                    rationale=rule["reason"],
                    dna_trace=f"#龍芯⚡️{persona_name}-{datetime.now().strftime('%Y%m%d')}",
                    timestamp=datetime.now().isoformat()
                )
                decisions.append(decision)
                confidence_scores.append(rule["confidence"])

        # 一致性评分 = 各人格信心度的平均值
        consensus_score = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0

        # 最终建议：由宝宝执行（因为宝宝是执行者）
        final_decision = None
        for decision in decisions:
            if decision.persona == "宝宝":
                final_decision = decision
                break

        final_recommendation = final_decision.recommendation if final_decision else "UNKNOWN"

        result = DecisionMatrix(
            threat_level=threat_level,
            defense_success=defense_success,
            decisions=decisions,
            final_recommendation=final_recommendation,
            consensus_score=consensus_score,
            dna_trace=f"#龍芯⚡️DECISION-{datetime.now().strftime('%Y%m%d')}"
        )

        self.decisions_log.append(result)
        return result

    @staticmethod
    def _get_role(persona_name: str) -> str:
        """获取人格角色"""
        roles = {
            "宝宝": "执行者",
            "乔前辈": "审计官",
            "哨兵": "守卫",
            "曾仕强老师": "理论家"
        }
        return roles.get(persona_name, "未知")

    def export_decision_matrix(self, output_path: str = None) -> str:
        """导出决策矩阵到知识库"""

        if output_path is None:
            output_path = Path.home() / "longhun-system" / "龍魂知識庫" / "人格自動化_決策矩陣.md"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        md = """---
title: 龍魂人格自動化 · 24路決策矩陣
date: 2026-05-25
DNA: #龍芯⚡️2026-05-25-PERSONA-MATRIX-v2.0
---

# 🐉 龍魂·人格自動化決策矩陣

## 系統架構

```
威脅等級 × 防禦成功 → 24 路決策
  ↓
4 人格各自給意見
  ↓
一致性評分計算
  ↓
寶寶執行最終決策
```

## 24 路決策路由表

| 威脅 | 防禦 | 寶寶 | 喬前輩 | 哨兵 | 曾老師 | 一致性 | 最終 |
|------|------|------|--------|------|--------|--------|--------|
| ∞ | ❌ | 停止 | 禁止 | 封鎖 | 違規 | 100% | **∞熔斷** |
| ∞ | ✅ | 監控 | 強化 | 增強 | 警惕 | 90% | 監控增強 |
| P0 | ❌ | 隔離 | 評審 | 告警 | 暫停 | 95% | **P0隔離** |
| P0 | ✅ | 繼續 | 批准 | 更新 | 批准 | 90% | 繼續執行 |
| P1 | ❌ | 隔離 | 修復 | 嚴監 | 有條件 | 85% | **P1隔離** |
| P1 | ✅ | 繼續 | 批准 | 監控 | 批准 | 85% | 繼續執行 |
| P2 | ❌ | 日誌 | 日誌 | 記錄 | 批准 | 70% | 日誌監控 |
| P2 | ✅ | 繼續 | 批准 | 基線 | 批准 | 80% | 繼續執行 |

## 關鍵決策規則

### 規則 1：極限威脅（∞級）

**寶寶行動**: HALT_IMMEDIATELY - 系統立刻停止
**喬前輩**: 編譯禁止 - 代碼不能通過檢查
**哨兵**: 全鎖定 - 護城河關閉·啟動應急
**曾老師**: 倫理違規 - 觸犯龍魂鐵律

→ **最終決策**: ∞級永久熔斷

### 規則 2：超高風險（P0級）

防禦失敗 → 隔離+人工審查
防禦成功 → 繼續+強化監控

### 規則 3：高風險（P1級）

防禦失敗 → 隔離+日誌
防禦成功 → 繼續+監控

### 規則 4：中風險（P2級）

防禦失敗 → 日誌記錄
防禦成功 → 繼續執行

## 一致性評分機制

```
consensus_score = Σ(4人格信心度) / 4

0.95-1.0   🟢 完全一致 - 直接執行
0.80-0.94  🟡 基本一致 - 執行+監控
0.60-0.79  🟠 部分分歧 - 隔離+評審
<0.60      🔴 嚴重分歧 - 人工判斷
```

## 與龍魂系統的聯動

```
熔斷推演報告
  ↓
威脅等級 + 防禦結果
  ↓
人格決策引擎
  ↓
24 路決策矩陣
  ↓
一致性評分
  ↓
寶寶執行決策
```

## DNA 追溯

每個決策都有追溯碼：
- `#龍芯⚡️寶寶-20260525` - 執行者簽名
- `#龍芯⚡️喬前輩-20260525` - 審計官簽名
- `#龍芯⚡️哨兵-20260525` - 守衛簽名
- `#龍芯⚡️老師-20260525` - 理論指導簽名

---

**系統確認碼**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)

        print(f"✅ 決策矩陣已導出: {output_path}")
        return str(output_path)


# ========== 主程序 ==========

def main():
    print("=" * 80)
    print("🐉 龍芯·人格自動化決策矩陣 v2.0")
    print("=" * 80)

    engine = PersonaDecisionEngine()

    # 測試所有 8 種場景
    test_cases = [
        ("∞", False),
        ("∞", True),
        ("P0", False),
        ("P0", True),
        ("P1", False),
        ("P1", True),
        ("P2", False),
        ("P2", True),
    ]

    for threat, defense in test_cases:
        print(f"\n📊 場景: 威脅={threat}, 防禦={'✅' if defense else '❌'}")
        result = engine.make_decision(threat, defense)
        print(f"  最終決策: {result.final_recommendation}")
        print(f"  一致性: {result.consensus_score*100:.0f}%")
        print(f"  人格建議:")
        for decision in result.decisions:
            print(f"    - {decision.persona}: {decision.recommendation}")

    # 導出矩陣
    engine.export_decision_matrix()

    print("\n✅ 決策矩陣生成完成！")


if __name__ == "__main__":
    main()
