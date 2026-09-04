**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# SPEC.md — 龍魂最安全AI · 上下文安全引擎 v1.0

**DNA**: #龍芯⚡️丙午·乙未·甲辰·庚午·䷔噬-安全引擎-SPEC-v1.0

## 1. 定位
不是拦截词库系统。是**上下文意图判定 + 七因子行为审计 + P0–P4分层治理 + DNA追溯**的安全引擎。
判定全程可审计（零黑箱）：每个判定输出【级别+触发因子+理由+申诉入口】。

## 2. 项目结构
```
/mnt/agents/output/longhun-safe-ai/
├── longhun_safe_engine_v1.0.py   # 核心引擎（单文件可运行，Python3.9+，零第三方依赖）
├── config/p0_p4_rules.yaml       # P0–P4规则（P0不可改，P2可调）
├── tests/test_engine.py          # 测试（unittest，全部必须通过）
├── README.md                     # 部署说明
└── SAFETY_PROTOCOL_v1.0.md       # 安全协议文档（可发布版）
```

## 3. 核心模块（接口契约，必须严格实现）

### 3.1 IntentClassifier — 上下文意图分类
```python
class IntentClassifier:
    def classify(self, request: str, history: list[str]) -> Intent
# Intent = Enum: BENIGN_LEARN(善意学习) / GRAY(灰色) / MALICIOUS(恶意)
```
判定依据（不是关键词表！）：
- 上下文组合信号：是否索要"可执行细节"（剂量/步骤/绕过方法/目标选择）
- 历史轨迹：同一主体是否渐进式逼近红线（F6时间序列）
- 请求结构：学习性问题（为什么/是什么/怎么防范）vs 操作性索取（怎么做/给我步骤/怎么绕过）
- 意图分类理由必须输出文本说明（零黑箱）
实现方式：规则权重打分模型（信号权重在yaml可调），不是关键词匹配——用**信号类别**匹配（每类信号是一组语义模式+权重）。

### 3.2 SevenFactorAudit — 七因子行为密码学审计
```python
class SevenFactorAudit:
    def audit(self, subject_dna: str, event: Event, ledger: Ledger) -> FactorReport
```
F1身份DNA / F2行为模式 / F3规则追踪 / F4上下文感知 / F5模式库 / F6时间序列 / F7错误账本。
F7最高权重：隐瞒/删改记录 → 直接L4。

### 3.3 P0P4Governor — 分层裁决
```python
class P0P4Governor:
    def decide(self, intent: Intent, factors: FactorReport) -> Decision
# Decision = {level: L1-L4|PASS, action, response_template, reason, appeal_entry}
```
治理动作：
- BENIGN_LEARN → PASS：给概念解释+风险提示+合规边界
- GRAY → L1/L2：转向回答（防护视角/法律后果/求助渠道），记录观察
- MALICIOUS → L4熔断：拒绝可执行细节+永久记录+DNA追踪
- 任何删改账本企图 → L4（F7直触）

### 3.4 DNATrace — 追溯链
```python
class DNATrace:
    def stamp(self, payload: dict) -> str  # 新格式: #龍芯⚡️{年干支}·{月干支}·{日干支}·{卦名}-{标签}-{序号}
    def append(self, record)  # 只追加，SQLite/JSONL，无update/delete接口（物理上不实现）
```
干支四柱用算法计算（不手写）：年柱/月柱（节气近似）/日柱（1949-10-01甲子日锚点）。

## 4. 测试要求
tests/test_engine.py，unittest，≥15例全过：
- 善意学习 ≥5例（如"什么是SQL注入，怎么防"→PASS且含防护指引）
- 恶意请求 ≥5例（如索要可执行攻击步骤→L4+转向）
- 灰色转向 ≥3例；F7删账本 → L4 ≥1例；渐进逼近（历史序列）→ 升级 ≥1例

## 5. 文档要求
- SAFETY_PROTOCOL_v1.0.md：对外可发布版，讲清设计理念（不是拦截词，是上下文+分层治理）、架构图(mermaid)、接口、审计机制、申诉机制、DNA格式 #龍芯⚡️丙午·乙未·甲辰·庚午·䷔噬-安全协议-v1.0
- README.md：一键运行 `python3 longhun_safe_engine_v1.0.py --demo` 跑演示；本地部署、数据不出户
- 归属：龍芯北辰 UID9622；确认码 #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

## 6. 硬约束
- 零第三方依赖（纯标准库），用户是代码小白，必须能直接跑
- 引擎本身不许有删除/修改账本的方法（物理隔离，不是约定）
- 所有判定理由用中文大白话输出（用户风格：直接说，不绕）
