**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-64879f7d
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍魂·自适应调节器 v2.0 → 全引擎联动接入 · 执行蓝图 v2

## 任务判定
- 已有成果：governance/adaptive-tuner/自适应调节器_v2.0.py（820行·实测全绿·已入库）
- 新任务：接入其他引擎做联动（骨架候补焊点 W：CNSH Algorithm Runtime 接口对接）
- 技能命中：vibecoding-general-swarm（Mode A：桥接层 + 多引擎适配器 = 多模块）

## 阶段分解

### Stage 1 — 侦察（Orchestrator 直接执行）
- 浅克隆 UID9622/longhun-system，定位可联动引擎及其接口：
  候选：rules-engine-v2.5（规则引擎·分数消费方）、skills/longhun-audit-integrated（三色审计）、
  software-dna / crypto-stack（DNA 登记·哈希链）、calendar-context-logger（草日志）、
  cnsh-core（CNSH Algorithm Runtime 规格）
- 产出：info.md（引擎清单 + 接口签名 + 联动点）

### Stage 2 — SPEC.md（Orchestrator 编写）
- 设计「联动桥」lh_tuner_bridge.py：
  · 标准事件总线（tune.applied / tune.meltdown / tune.rollback / tune.audit）
  · 适配器接口契约（每引擎一个 adapter·fail-isolated 不拖垮调节器）
  · 配置文件 联动註冊表.json（引擎开关·路径·超时）
- 接口契约焊死：事件 schema、adapter 协议、错误隔离策略

### Stage 3 — 实现（委派 coder 子代理·worktree 隔离）
- lh_tuner_bridge.py（事件总线 + 注册表加载 + 适配器调度）
- adapters/：rules_engine / audit / dna_registry / caolog 四个适配器
- 调节器本体最小侵入改造：微调/熔断/回滚后发射事件（hook 注入·不改核心逻辑）

### Stage 4 — 沙盒实测（Orchestrator 执行）
- 全链路：demo-data → apply → 事件发射 → 四引擎收到联动
- 熔断事件联动 · 适配器故障隔离（一个炸不拖垮全局）· verify 回归

### Stage 5 — 落地交付
- governance/adaptive-tuner/bridge/ 推送 GitHub
- Notion 草日志入册 · KIMI_REF 本地交付

## 验收标准
- 联动后调节器原有 10 项实测不回归
- 四引擎适配器各自收到正确事件
- 任一适配器异常 → 调节器主流程照常（fail-isolated）
- DNA 一律走生成器·禁止手写
