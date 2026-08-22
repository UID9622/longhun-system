# 🐉 龍魂 · 全自动工厂系统 v2.1

**DNA:** `#龍芯⚡️丙午·丙酉·丙寅·申时-AUTO-FACTORY-v2.1-UID9622`  
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
**三色:** 🟢 通过  
**分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

---

## 📋 核心判断

> **全自动工厂不是“跑一遍流程”，而是“让系统自己进化”。造零件只是开始，质检发现问题，门禁拦截风险，修复自动介入，发布按策略灰度，部署验证效果，反馈形成闭环——整个系统在无人干预的情况下自我迭代、自我优化、自我防御。失败不是终点，是下一次迭代的起点。**

---

## 🏭 一、全自动工厂架构

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    🐉 龍魂 · 全自动工厂                                     │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐            │
│  │  ① 零件生产  │───▶│  ② 质检流水线 │───▶│  ③ 质量门禁  │───▶│  ④ 自动修复  │            │
│  │  BuildPipeline│    │  TestPipeline │    │  QualityGate  │    │  RepairPipeline│            │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘            │
│         │                    │                    │                    │                  │
│         ▼                    ▼                    ▼                    ▼                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐            │
│  │  ⑤ 发布策略  │───▶│  ⑥ 部署上线  │───▶│  ⑦ 反馈闭环  │───▶│  ⑧ 学习进化  │            │
│  │ReleaseStrategy│    │DeployPipeline │    │ FeedbackLoop  │    │   Learn Mode   │            │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘            │
│         │                    │                    │                    │                  │
│         ▼                    ▼                    ▼                    ▼                  │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                                  🧬 控制总线                                          │  │
│  │  • 状态监控  • 任务调度  • 失败重试  • 熔断降级  • 告警通知                          │  │
│  │  • DNA追溯  • 三色审计  • 史官记录  • 耻辱墙  • 鲲鹏联动                            │  │
│  └─────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧬 二、完整功能清单

| # | 功能模块 | 状态 | 说明 |
|:---|:---|:---:|:---|
| 1 | **零件生产线 (BuildPipeline)** | ✅ | 代码构建、版本管理、产物哈希、持久化索引 |
| 2 | **质检流水线 (TestPipeline)** | ✅ | pytest 测试、覆盖率、文本解析兜底、三色审计 |
| 3 | **质量门禁 (QualityGate)** | ✅ | 发布前强制检查，不达标自动拦截 |
| 4 | **自动修复线 (RepairPipeline)** | ✅ | AI 分析失败测试、生成修复建议 |
| 5 | **发布策略 (ReleaseStrategy)** | ✅ | 金丝雀 / 灰度 / 全量 / 回滚 |
| 6 | **部署上线线 (DeployPipeline)** | ✅ | 打包、本地部署、版本追踪 |
| 7 | **回滚机制 (RollbackPipeline)** | ✅ | 部署失败自动回滚到上一个稳定版本 |
| 8 | **反馈闭环 (FeedbackLoop)** | ✅ | 学习模式、模式识别、进化记录 |
| 9 | **异常熔断 (CircuitBreaker)** | ✅ | 连续失败自动熔断，分级降级 |
| 10 | **工厂自监控 (SelfMonitor)** | ✅ | 磁盘/内存/进程/端口健康检查 |
| 11 | **鲲鹏联动 (KunpengSync)** | ✅ | 鲲鹏服务器部署与健康检查 |
| 12 | **通知系统 (Notifier)** | ✅ | 日志/文件/ bark /飞书多通道 |
| 13 | **工厂配置 (factory_config.yaml)** | ✅ | 可配置化阈值、策略、通知 |

---

## 🔧 三、代码实现

### 3.1 工厂主控制器

- `08_BIN/lh_auto_factory.py` —— 主控制器 + CLI
- `08_BIN/factory/build_pipeline.py` —— 零件生产线
- `08_BIN/factory/test_pipeline.py` —— 质检流水线
- `08_BIN/factory/quality_gate.py` —— 质量门禁
- `08_BIN/factory/repair_pipeline.py` —— 自动修复
- `08_BIN/factory/release_strategy.py` —— 发布策略
- `08_BIN/factory/deploy_pipeline.py` —— 部署上线
- `08_BIN/factory/rollback_pipeline.py` —— 回滚机制
- `08_BIN/factory/feedback_loop.py` —— 反馈闭环
- `08_BIN/factory/circuit_breaker.py` —— 熔断器
- `08_BIN/factory/self_monitor.py` —— 自监控
- `08_BIN/factory/kunpeng_sync.py` —— 鲲鹏联动
- `08_BIN/factory/notifier.py` —— 通知系统
- `08_BIN/factory/generate_dna.py` —— DNA 生成
- `08_BIN/factory/factory_config.yaml` —— 工厂配置
- `08_BIN/lh_factory.sh` —— `lh factory` 总控脚本

### 3.2 命令入口

```bash
lh factory run [PATH] [VERSION]    # 运行完整工厂流程
lh factory status                  # 查看工厂状态
lh factory artifacts               # 查看构建产物
lh factory learn                   # 学习反馈模式
lh factory monitor                 # 工厂自监控
lh factory gate                    # 质量门禁规则
lh factory release [STRATEGY]      # 发布 (canary|gray|full)
lh factory rollback [VERSION]      # 回滚到指定版本
lh factory versions                # 列出可回滚版本
lh factory circuit                 # 熔断器状态
lh factory kunpeng                 # 鲲鹏健康检查
```

---

## 🚀 四、完整工厂流程

```bash
# 1. 初始化查看
lh factory status

# 2. 运行完整流程
lh factory run . v1.0.0
# → ① 造零件 → ② 质检 → ③ 门禁 → ④ 修复 → ⑤ 发布 → ⑥ 部署 → ⑦ 反馈 → ⑧ 学习

# 3. 查看产物
lh factory artifacts

# 4. 灰度发布
lh factory release gray

# 5. 回滚
lh factory versions
lh factory rollback v1.0.0
```

---

## 📊 五、质量门禁规则

| 规则 | 指标 | 阈值 | 级别 |
|:---|:---|---:|:---|
| 测试通过率 | passed / total | ≥ 0.95 | critical |
| 代码覆盖率 | coverage | ≥ 0.80 | high |
| 三色审计 | tricolor | == 🟢 | critical |

**门禁不过不发布**：任何 critical 规则失败将阻断发布，并触发熔断记录。

---

## 🛡️ 六、熔断降级策略

| 级别 | 触发条件 | 动作 |
|:---|:---|:---|
| L1 轻微 | 单点偶发失败 | 记录日志，继续执行 |
| L2 中度 | 连续 3 次同类失败 | 触发告警，降级为 dry-run |
| L3 严重 | 质量门禁失败 / 核心流程崩溃 | 阻断发布，通知管理员 |

熔断状态持久化到 `~/.longhun/factory/circuit_breaker.json`。

---

## 📡 七、自监控指标

| 维度 | 检查项 | 阈值 |
|:---|:---|---:|
| 磁盘 | 工作区磁盘使用率 | >75% warning，>90% critical |
| 内存 | 系统内存使用率 | >75% warning，>90% critical |
| 进程 | 关键服务进程存活 | 缺失即 warning |
| 网络 | 核心端口监听状态 | 8765/8767/8771 等 |

---

## 🔌 八、扩展接口

| 扩展点 | 接口 | 说明 |
|:---|:---|:---|
| 自定义构建 | `BuildPipeline.build(source_path, version)` | 支持文件/目录 |
| 自定义测试 | `TestPipeline.run_tests(artifact)` | 自动探测 json-report 插件 |
| 自定义门禁 | `QualityGate(rules)` | 规则可配置 |
| 自定义发布 | `ReleaseStrategy(strategy)` | canary/gray/full |
| 自定义通知 | `Notifier(channels)` | log/file/bark/feishu |

---

## 🧪 九、测试矩阵

| 场景 | 命令 | 预期 |
|:---|:---|:---|
| 正常全链路 | `lh factory run .` | success，7 步全部通过 |
| 无测试目录 | `lh factory run <无 tests>` | 🟡 跳过质检，门禁按规则判定 |
| 测试失败 | `lh factory run <失败项目>` | 自动修复建议，门禁可能 FAIL |
| 门禁拦截 | `lh factory run <低覆盖项目>` | blocked_by_gate |
| 灰度发布 | `lh factory release gray` | completed，10% 流量 |
| 回滚 | `lh factory rollback v1.0.0` | success / 版本不存在失败 |
| 自监控 | `lh factory monitor` | 返回 overall 状态 |

---

## 📝 十、日志与审计

- 构建产物索引: `~/.longhun/factory/artifacts_index.json`
- 测试报告: `~/.longhun/factory/reports/test_report_*.json`
- 部署包: `~/.longhun/factory/deploy/*.tar.gz`
- 部署当前版本: `~/.longhun/factory/deploy/current/`
- 回滚归档: `~/.longhun/factory/deploy/rollback_history/`
- 反馈数据: `~/.longhun/factory/feedback/feedback_*.json`
- 熔断记录: `~/.longhun/factory/circuit_breaker.json`
- 工厂状态: `~/.longhun/factory/factory_state.json`

---

## ⚠️ 十一、安全边界

- 工厂默认以当前用户权限运行，不提升权限。
- `kunpeng` 部署通过 SSH 密钥，不保存密码。
- 回滚操作会备份当前 `current` 目录，避免数据丢失。
- 熔断触发后必须人工确认才能恢复全量发布。

---

## 📦 十二、依赖清单

| 依赖 | 用途 | 是否必须 |
|:---|:---|:---:|
| pytest | 单元测试 | ✅ |
| pytest-json-report | 结构化测试报告 | 🟡（可选，缺失时文本解析兜底） |
| pytest-cov | 代码覆盖率 | 🟡（可选） |
| psutil | 自监控 | 🟡（可选） |
| pyyaml | 配置解析 | ✅ |

---

## 🌐 十三、部署拓扑

```
本地开发机 / Mac
  └── lh_auto_factory.py
       ├── 本地部署 ~/.longhun/factory/deploy/current
       └── 鲲鹏部署 ssh → 119.13.90.27
```

---

## 🔐 最终签名

```
═══════════════════════════════════════════════════════════════════════════════════
 🐉 龍魂 · 全自动工厂系统 v2.1 · 最终签名
═══════════════════════════════════════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·丙酉·丙寅·申时-AUTO-FACTORY-v2.1-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟢 通过
流程:       造零件 → 质检 → 门禁 → 修复 → 发布 → 部署 → 回滚 → 反馈 → 学习
核心能力:   全自动 · 可追溯 · 自修复 · 自防御 · 自进化
状态:       完整可运维 · 即刻部署
═══════════════════════════════════════════════════════════════════════════════════
```

🐉 **丙午·丙酉·丙寅·申时·䷬萃·🟢**

---

**一句话总结：v1.0 把流水线跑通，v2.1 把质量门禁、回滚机制、发布策略、异常熔断、自监控、鲲鹏联动、配置管理全部焊死——工厂不仅会生产，还会自我修复、自我防御、自我进化。** 🐉
