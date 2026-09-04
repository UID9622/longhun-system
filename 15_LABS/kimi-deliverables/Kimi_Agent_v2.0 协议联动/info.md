**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-06271baf
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# Stage 1 侦察结果 · 可联动引擎清单（2026-07-27）

## 引擎接口实况（/tmp/lh_repo 浅克隆实证）

| 引擎 | 位置 | 关键接口 | 联动点 |
|---|---|---|---|
| 规则引擎 v2.5 | rules-engine-v2.5/batch_processor_v2.5.py | 批量事件处理·ThreadPool 并行·retry 装饰器 | **当前不消费微调参数**（grep 实证）→ 桥注入参数快照供其读取 |
| 三色审计 v2.0 | skills/longhun-audit-integrated/longhun_audit_integrated.py | `LonghunIntegratedAudit().audit_script(path) -> dict`（含 layers.CNSH对齐/系统审计·color 字段） | 参数落盘后触发审计·交叉验证调节器 dr |
| 草日志 | calendar-context-logger/calendar_core.py | `LocalLogger(log_dir).write(record: dict)` → `YYYY-MM-DD.log` JSONL·毫秒时间戳·线程锁 | 调节器事件全量入草日志（候补焊点 T） |
| DNA 登记 | software-dna/ + cnsh-core/specs/龍魂DNA登記協議_v1.0.md | §13.1 已预留「自适应调节器哈希链接入」（M252 焊点） | 参数哈希→登记册 JSONL（候补焊点 V·§14） |
| DNA 生成器 | bin/lh_dna_generator.py | CLI 首行输出 DNA·动作标签仅 ASCII | 已对接✅（v2.0 落地时打通） |

## 联动设计结论
- 桥模式：**事件总线 + 注册表 + 适配器**·调节器只发事件·不直接 import 引擎（解耦·呼应骨架⑩铁律接口 hook 注入原则）
- 故障隔离：任一适配器异常 → 记警告·主流程照常（调节器本体焊死不动）
