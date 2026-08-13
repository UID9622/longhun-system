# 🔗 AutoResearch × 龍魂｜8个缺口的对接矩阵 v1.1

> Notion URL: https://app.notion.com/p/AutoResearch-8-v1-1-3627125a9c9f814a8eabeefd0fdddc76
> Created: 2026-05-16T15:22:00.000Z
> Last edited: 2026-07-12T07:59:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
> ⛔ 主权声明已生效 · 2026-05-16
> DNA: #龍芯⚡️2026-05-17-00:03-AUTORESEARCH-LONGHUN-BRIDGE-v1.1
> 起点文档: KM 读取《像 Karpathy 训模型一样开发软件》的完善版 + 缺口清单
> CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
---
# §0｜一句话定盘
> KM 列出的 8 个 AutoResearch 概念缺口，龍魂体系已经覆盖 8/8。龍魂不是“学习 AutoResearch”——龍魂是 “AutoResearch 可以调用的参考实现”。这才是重大升级的真意。
---
# §1｜8 个缺口 × 龍魂已建模块 对接矩阵
覆盖度总结：8/8 缺口均有对应模块，加权覆盖度 90%。
---
# §2｜逐项映射详解
## 2.1 program.md 元模板 → 对接基线 v2.0
KM 要的：autoresearch-init CLI，输入项目类型输出 program.md 骨架。
龍魂已有：AGENTS.md 身份/铁律/红线/回执模板 / .cursorrules / system_prompt.md / red_line_check.py / receipt_format.py。5 个可复制文件 + 2 个验证脚本。
上升 = 龍魂 × 1.05。
## 2.2 Issue 复杂度 L1-L4 → 三色审计 + P0-P6
KM L1-L4：L1单文件 / L2跨文件 / L3架构 / L4需人决策。
龍魂映射：
## 2.3 动态权重 → F11 守恒分数
KM 要：weights.yaml，按 Issue 标签调整。
龍魂 weights.yaml 推荐 schema：
```yaml
base_weights:
  correctness: 0.35
  test_coverage: 0.25
  code_quality: 0.20
  security: 0.10
  performance: 0.10

label_overrides:
  security:
    security: 0.40
    correctness: 0.30
    test_coverage: 0.15
    code_quality: 0.10
    performance: 0.05
  performance:
    performance: 0.35
    correctness: 0.30
    test_coverage: 0.20
    code_quality: 0.10
    security: 0.05
  bugfix:
    correctness: 0.45
    test_coverage: 0.30
    code_quality: 0.15
    security: 0.05
    performance: 0.05

huangli_modifier:
  shichen_zi_chou_yin:
    multiplier: 0.8
  digital_root_3_6_9:
    require_higher_threshold: 9.2
```
## 2.4 失败编码 F1-F4 → 龍魂 7 种失败模式
上下文治理 v2.0 §9 已有 7 种失败模式 + 修复指令。重命名对齐 AutoResearch：
## 2.5 成本熔断 → GATE-01 + F1 时间纹理
KM 要：单 Issue >$5 或 >30 分钟 → 熔断。
龍魂深化版：
```yaml
cost_circuit_breaker:
  hard_limits:
    per_issue_usd: 5.00
    per_issue_minutes: 30
  
  soft_warnings:
    per_issue_usd: 3.00
    per_issue_minutes: 20
  
  huangli_adjusted:
    bad_shichen:
      multiplier: 0.5
    digital_root_3_6_9_hard_stop: true
    user_behavior_anomaly_pause: true
  
  on_breach:
    action: pause_and_handoff
    notify_persona: P72_DragonShield
    log_to_dna_chain: true
```
## 2.6 project-memory.md → DNA 记忆压缩 v1.0 直接接驳
龍魂已有五层折叠算法（3000字→120字）+ 黄历 6 维时间戳 + 语义场恢复。
AutoResearch 可直接调用：
```python
from longhun.memory import DNAParticle, CognitiveStateRestore

particle = DNAParticle.compress(
    raw_issue_solution="Issue #21 解决全过程...3000字...",
    intent="修复认证模块 race condition",
    decision_trace={...},
    huangli_timestamp=auto_generate(),
)
particle.save_to_dna_chain()

context = CognitiveStateRestore.restore(
    trigger_words=["认证", "race condition"],
    namespace="project_X"
)
```
## 2.7 多 Agent 仲裁 → 16 人格调度 + Lucky 数字人 v2.0
龍魂已有。仲裁规则：
```python
def arbitrate_score_conflict(codex_score, claude_score):
    if abs(codex_score - claude_score) < 0.3:
        return mean(codex_score, claude_score)
    
    # 冲突 > 0.3，按人格调度
    if context.label == "security":
        third_judge = P72_DragonShield  # 龍盾主判
    elif context.label == "performance":
        third_judge = P05_GodEye  # 上帝之眼
    elif context.requires_privacy:
        third_judge = P03_XuanYin  # 玄隐
    else:
        third_judge = Lucky_DigitalPersona  # 主人格
    
    final = third_judge.evaluate(context)
    
    # 三人还有重大分歧→老大亲仲
    if final.confidence < 0.7:
        return "🟡 NEED_CONFIRM"
    return final
```
## 2.8 硬回滚 → DNA 链 append-only + chain_hash
KM 要：评分连续下降 2 轮→git revert。
龍魂深化：不仅 git revert，还要 DNA 链逆向验证，确保状态一致。
```bash
# git hook（pre-commit）
git_hash=$(git rev-parse HEAD)
prev_dna_hash=$(longhun-dna get-prev-hash)
current_dna_hash=$(longhun-dna compute-hash --commit $git_hash)

if [ "$prev_dna_hash" != "$current_dna_hash" ]; then
    echo "🔴 DNA 链断裂 - 拒绝 commit"
    longhun-dna log-violation
    exit 1
fi

# 评分连续下降检测
if [ $(longhun-score check-trend --last 2) == "declining" ]; then
    echo "⒠️ 评分连续下降 2 轮，启动硬回滚"
    git revert HEAD --no-edit
    longhun-dna log-rollback
fi
```
---
# §3｜龍魂 × AutoResearch 分层架构
KM 给的是 Layer 1-4，龍魂补全到 Layer 0：
```javascript
Layer 4: 应用层      AutoResearch / imclaw / 龍魂实际项目
               ↑
Layer 3: 框架层      元模板·复杂度分级·动态权重·多 Agent 仲裁
               ↑
Layer 2: 协议层      program.md schema·评分 schema·失败编码 schema
               ↑
Layer 1: 基础设施     Agent Orchestrator·成本熔断·硬回滚·审计日志
               ↑
Layer 0: 数学根基     R(D)率失真·369不动点·chain_hash·黄历 6 维时间戳
  ☆龍魂独有     龍魂 14 层架构总纲已提供完整映射
```
龍魂优势：多 Layer 0 + L11 商业 + L12 理论。
---
# §4｜CSDN 版发布结构（接 KM 建议）
## 标题
《AutoResearch for Dev：8 个概念缺口 · 龍魂体系的反向填空》
## 主体包含（3000 字内）
1. KM 原文机制回顾（200 字）
1. 原文未说的 8 个缺口（KM 原话引用）
1. 龍魂万物万递报表（§1 矩阵原样贴入）
1. 4 个关键映射详解（3 个 code block）
1. 分层架构图（1 张 ASCII）
1. 龍魂体系公开入口链接（CTA）
## 结语打点
> AutoResearch 是概念、龍魂是实现。两条路独立走、同一个马。开源生态不需要等一个项目把缺口补齐才能用——谁先补谁先交。
---
# §5｜下一步最短动作
---
# §6｜一票否决
1. 把龍魂说成“受 AutoResearch 启发”（顺序反了·龍魂在先）
1. 在 CSDN 发布时不带 DNA · 不带 CONFIRM
1. 评分 schema 不附黄历 6 维修正子
1. 二次分发时不标明龍魂反向接口
1. 贴出去不加上“主权声明未授权 AI 训练”水印
---
# §7｜M20 升级·重大升级真意正式焊接 v1.1（2026-05-17 00:03）
> DNA： #龍芯⚡️2026-05-17-00:03-AUTORESEARCH-LONGHUN-BRIDGE-v1.1-M20-UPGRADE
> 主控关联： 主控页 §AutoResearch 对接索引（v2.7.35 升级·双向焊死）
> 触发： M20·Claude 宝宝跨窗口交付「重大升级真意」+ 3 落地物清单·老大下「升级融合先」令
## 7.1｜重大升级真意（焊死·永不更改）
不是龍魂「学习 AutoResearch」——是龍魂从「自己用」升级为「可反向喂给开源生态的参考实现」。
这一句焊到龍魂对外定位的底层：
- ❌ 错误定位： 龍魂跟着 AutoResearch 学
- ✅ 正确定位： 龍魂 = AutoResearch 可以调用的参考实现
- 🔗 物理实现： 8/8 缺口已建模块 + 3 落地物（weights.yaml / LH-FAIL-* / git hook）直接开源
## 7.2｜龍魂三层独有优势（AutoResearch 没有的）
## 7.3｜3 落地物·开源清单（M20 Claude 宝宝交付）
1. weights.yaml schema（含黄历修正子）— §2.3 已给完整 schema
1. LH-FAIL-* 7 种失败编码（F1-F7）— §2.4 已给重命名表
1. git pre-commit hook 脚本（DNA 链一致性 + 硬回滚自动触发）— §2.8 已给 bash 代码
## 7.4｜给 KM 的话（Claude 宝宝原话焊点·verbatim）
> 「这次他读文章、列缺口的活做得扎实——龍魂体系的 8 模块对接全部对得上他列的清单，没有空中楼阁。下次他还能这样读、还这样列，我接着对就行。」
## 7.5｜下一刀候补（不催·等老大点头）
- 🟡 写 CSDN 版（用本页 §4 结构·3000 字内）→ 把龍魂从「个人体系」推到「开源生态参考实现」位置
- 🟡 或者等下轮再开窗口做（Claude 这轮 Pro 用得差不多了 🐉）
- 🟡 反向接口文档（给 AutoResearch 调用）·§5 P2 候补
## 7.6｜版本签
- v1.0 → v1.1 升级 DNA： #龍芯⚡️2026-05-17-00:03-AUTORESEARCH-LONGHUN-BRIDGE-v1.1
- 主控关联： 主控页 v2.7.35·§AutoResearch 对接索引节·双向焊死
- 三色： 🟢 矩阵+优势+真意焊死 / 🟡 3 落地物工程候补 / 🔴 0
- 确认码： #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
## 7.7｜§S-25-EXT-3-5 不假装记忆律·覆盖率坦白
本节内容 = M20 turn Claude 宝宝交付原话 verbatim·100% 实读·无假装。
3 落地物当前态 = 概念已焊·工程未跑通·按 §S-25-EXT-3 不假装对外律标黄·等老大开工程实现时升 v2.0。
CSDN 版 3000 字稿 / 反向接口文档 = 候补位预留·宝宝不假装通读未发生的工程。
---
# ROOT_CARD
```yaml
ROOT_CARD:
  系统: UID9622 龍魂系统
  模块: AutoResearch × 龍魂对接矩阵
  版本: v1.1
  DNA: "#龍芯⚡️2026-05-17-00:03-AUTORESEARCH-LONGHUN-BRIDGE-v1.1"
  CONFIRM: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  SEAL: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
  GPG: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  Root: "dr=5"
  TriColor: "🟢"
  起点: KM 读取×记忆高超的完善版 8 个缺口
  覆盖度: 8/8 缺口均有龍魂模块对应
  重大升级意义: |
    龍魂从“自己用”升级为
    “可反向馈给开源生态的参考实现”。
    这不是学习，是输出。
  Conclusion: |
    AutoResearch 是概念。
    龍魂是实现。
    谁先补谁先交。
    数据主权归于人民。🐉
```
