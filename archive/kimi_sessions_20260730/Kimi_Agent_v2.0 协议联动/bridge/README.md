# 龍魂·联动桥 lh_tuner_bridge v1.0

- **DNA**: 由 bin/lh_dna_generator.py 生成·禁止手写（本文件不伪造干支）
- **GPG**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
- **CONFIRM**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
- **SEAL**: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
- **责任**: UID9622·不免责

## 架构

事件总线 + 注册表 + 适配器（单文件 `lh_tuner_bridge.py`·四适配器内嵌）。
调节器只发事件、不直接 import 引擎（解耦·铁律接口 hook 注入原则）；
桥与适配器全部 **fail-isolated**：任何异常只记状态、绝不抛回调节器，
调节器核心逻辑一行不改，仅在 4 个发射点追加 hook 调用。

```
自适应调节器_v2.0.py ──_发射联动()──▶ 联动桥.emit(事件类型, 载荷)
                                          │ 补齐事件契约字段（SPEC §二）
                                          ▼
                              ┌──── ThreadPoolExecutor + 超时 ────┐
                              ▼          ▼          ▼          ▼
                       RulesEngine  AuditAdapter  CaoLog    DNARegistry
                       Adapter                              Adapter
```

事件类型（焊死）：`TUNE_SIMULATED` / `TUNE_APPLIED` / `TUNE_MELTDOWN` /
`TUNE_ROLLBACK` / `TUNE_AUDIT`。

## 注册表 `~/.龍魂/聯動註冊表.json`

注册表缺席时桥自动写入默认值再使用。每引擎三要素：`开关` / `超时秒` / 各自路径
（快照路径、审计模块路径+仓库根、草日誌目录、登记册）。开关关闭的适配器不分发；
超时经 `future.result(timeout)` 实现，超时记 🔴、不抛异常。

## 四适配器

| 适配器 | 消费事件 | 动作 |
|---|---|---|
| RulesEngineAdapter | APPLIED / MELTDOWN / ROLLBACK | 从 `~/.龍魂/微調參數.json` 现读参数写快照 `引擎態/rules_engine_params.json`；熔断写 `rules_engine.LOCK.json`（从严信号）；回滚解除 LOCK |
| AuditAdapter | APPLIED / ROLLBACK | 懒加载三色审计模块取 color，与调节器 dr 交叉验证写 `引擎態/audit_crosscheck.json`；仓库根为空/模块缺席 → 🟡 跳过绝不失败 |
| CaoLogAdapter | 全部 5 类 | `草日誌/YYYY-MM-DD.log` JSONL 追加（格式对齐 LocalLogger·无需 import） |
| DNARegistryAdapter | APPLIED / ROLLBACK / MELTDOWN | `DNA登記冊.jsonl` 追加 §14 条款记录·链式存根 `sha256(父哈希+参数哈希+DNA)[:16]` 可复算 |

## 联动验证方法

```bash
# ① 自检：打印注册表 + 四适配器自检表（audit 仓库根为空返回 🟡 属正常）
python3 自适应调节器_v2.0.py --link-status

# ② 全链路：造数 → 落盘微调
python3 自适应调节器_v2.0.py --demo-data 40 --seed 1
python3 自适应调节器_v2.0.py --apply
# 验证：~/.龍魂/引擎態/rules_engine_params.json 存在且参数值正确
#       ~/.龍魂/草日誌/当日.log 有 tuner.tune_applied
#       ~/.龍魂/DNA登記冊.jsonl 有 §14 记录·链式存根可复算

# ③ 熔断/回滚：LOCK 生成 → 回滚后 LOCK 解除
# ④ 故障隔离：把注册表某适配器路径改坏 → emit 回该适配器 🟡/🔴·调节器主流程 exit 0
```
