# 龍魂·统一入口 STATE.md

> 所有 AI（CodeBuddy / Kimi / Ollama 本地模型）的唯一入口。
> 无论哪个窗口、哪个模型对话，启动时读这一份就够了。
> 更新: 2026-07-21 · v1.3
> DNA: #龍芯⚡️20260721-STATE-UNIFIED-ENTRY-v1.3

---

## 快速状态卡（10秒速览）

| 项目 | 状态 |
|:---|:---:|
| v3.7 主力模型 | ✅ Val 0.194·1273条·生产 |
| v4.1.1 🥇 | ✅ Val 0.8097·iter 200·早停·Ollama已注册 |
| **v4.1.1-bind** 🧬 | ✅ Val 0.9659@iter150·早停@iter300·fused·GGUF·Ollama注册·3/3实测通过 |
| v4.0.8 黄金checkpoint | 🥇 Val 0.767·iter1900·封存 |
| v4.1.2 | 🔴 中断·Val 1.2457@iter50·不恢复 |
| P0++ 新协议 | ✅ DNA捆绑与蒸馏防御 v1.0·已落档 |
| DNA捆绑引擎 | ✅ `lh_dna_bind_defender.py`·12/12测试通过 |
| **电商信任重建协议** | ✅ `LH-ECOM-TRUST-REBUILD-v1.0.md`·已落档 |
| **电商信任数学引擎** | ✅ `lh_ecom_trust_engine.py`·12/12全绿 |
| 🔐 **GPG 数字指纹** | ✅ **已公开发布**·`portal/pgp/`·RSA-4096·2025-12-17 |
| 🔒 **安全加固 v1.0** | ✅ **7补丁焊死·6/6验证·0高危** |
| 🧬 **跨模块路由总线** 🔥 | ✅ `lh_cross_module_router.py`·10条回调链·12/12测试 |
| 📐 **黎曼三视角引擎** 🔥 | ✅ `lh_riemann_zeta_engine.py`·15/15·论文→引擎落地 |
| ⚖️ **责任塌缩引擎** 🔥 | ✅ `lh_responsibility_collapse_engine.py`·13/13·论文→引擎落地 |
| ☯️ **易经世界模型引擎** 🔥 | ✅ `lh_yijing_world_engine.py`·15/15·论文→引擎落地 |
| 🧪 **集成测试** 🔥 | ✅ `lh_system_integration_test.py`·30/30·全链路联通 |
| 📚 **学习融合总手册** 🔥 | ✅ `LH-LEARN-INTEGRATE-MANUAL-v1.0.2.md`·9节+附录B·12/12全绿 |
| 🛡️ **未成年守护引擎** 🔥 | ✅ `bin/lh_minor_guard_engine.py`·P0·17/17全绿·数学建模增补落档 |
| AC电源 | ❌ 断开·电池71% |
| 鲲鹏 (119.13.90.27) | 🟡 未连接 |
| 数据量 | 27,082条 (含DNA捆绑协议33条新增) |
| longhun-core仓库 | 🟡 82测试通过·未推送 |

---

## 当前变量（in-flight·改动时更新这里）

```yaml
model:
  active: longhun-v3.7          # 当前1.5B生产
  next: longhun-v4.1.1-bind      # 🧬DNA捆绑·Val 0.9659·fused·Ollama可用
  base: Yi-1.5-9B-Chat          # v4.1.x 底座
  framework: MLX (Apple Silicon)
  method: LoRA

training:
  v411_lr_peak: 1e-6            # v4.1.1
  v411_dropout: 0.15
  v411_batch: 2
  v411_warmup: 50
  v411_early_stop: patience 3, Val 0.8097 @iter 200
  v411_bind_best: Val 0.9659 @iter 150  # DNA捆绑协议注入·iter300早停
  v411_bind_lr: 1e-6
  v411_bind_dropout: 0.15
  v412_lr_peak: 1e-6            # v4.1.2 (中断)
  v412_dropout: 0.12
  v412_batch: 4
  v412_best: Val 1.2457 @iter 50

data:
  current: 1273条 v6.3 JSONL
  target: 5000+

infra:
  mac: AC disconnected·battery 71%·~1h remaining
  kunpeng: 119.13.90.27·SSH key ~/.ssh/longhun_kunpeng_ed25519
  domain: uid9622.cn (Let's Encrypt wildcard 7/17→10/15)
  launchd: 52 services
  systemd: 11 services
  ollama_models:
    - longhun-v4.1.1-bind (Yi-1.5-9B·17.7 GB·Val 0.9659·DNA捆绑)
    - longhun-v4.1.1 (Yi-1.5-9B·17.7 GB·Val 0.8097)
    - longhun-v4.1.0 (Yi-1.5-9B·17 GB·Val 0.786)

anchors:
  confirm_code: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  gpg: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
  uid: 9622
  sn369: 369
  creator: 诸葛鑫·Lucky·UID9622
```

---

## 模型版本表

| 版本 | 底模 | Val | Train | iter | 状态 |
|:---|:---|:---:|:---:|:---:|:---|
| v3.7 🔥 | Qwen2.5-1.5B | 0.194 | — | — | ✅ 主力 |
| v4.1.1 🥇 | Yi-1.5-9B | **0.8097** | — | 200 | ✅ 早停·Ollama |
| **v4.1.1-bind** 🧬 | Yi-1.5-9B | **0.9659** | — | 300 | ✅ 早停·fused·Ollama·3/3通过 |
| v4.0.8 🥇 | Yi-1.5-9B | 0.767 | — | 1900 | 🥇 黄金 |
| v4.1.2 | Yi-1.5-9B | 1.2457 | — | 50 | 🔴 中断 |
| v4.0.9 | Yi-1.5-9B | 1.002 | 0.654 | 5600 | 🔴 停训 |
| v4.1.0 | Yi-1.5-9B | 0.786 | — | 250 | 🟡 早停 |
| v3.0 | Qwen2.5-1.5B | 0.029 | — | — | 回退 |

---

## 格式 & 命名规范（焊死）

```
DNA:         #龍芯⚡️YYYYMMDD-MODULE-VERSION-STATUS-HASH8
版本号:      模型 longhun-v{major}.{minor}.{patch}
             协议 LH-{NAME}-v{major}.{minor}.md
             数据 v{major}.{minor}
脚本前缀:    lh_ (所有龍魂脚本)
路径:       所有产出入 longhun-system/ 对应子目录
             禁入 ~/Downloads /tmp /Desktop
```

---

## 焊死锚点（不可变）

```
确认码:   #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:      A2D0092CEE2E5BA87035600924C3704A8CC26D5F
UID:      9622 (诸葛鑫·Lucky·唯一决策者)
369:      sn=369, log369=5.911, perm369=108
人格:     20人格矩阵 (16核心 P00-P72 + P77安全 + S1-S3子系统)
```

---

## 待办

### 🔴 阻塞
- [ ] 插AC电源
- [ ] 数据扩增 1273→5000+
- [ ] 鲲鹏部署脚本
- [ ] Mac→鲲鹏网络打通

### 🟡 进行中
- [ ] v4.1.1-bind 训练中·PID 10289·注入DNA捆绑协议知识
- [ ] longhun-core 推送远端
- [ ] 道德经深层训练数据

### ✅ 已完成 (7/21)
- [x] v4.1.1 训练完成·fuse·GGUF→Ollama (Val 0.8097·10/10实测通过)
- [x] v4.1.2 停止·识别为劣化 (Val 1.2457 vs v4.1.1 0.8097)
- [x] DNA捆绑与蒸馏防御协议v1.0落档 P0++
- [x] lh_dna_bind_defender.py 防御引擎 12/12测试通过
- [x] DNA捆绑协议训练数据33条生成+并入总库
- [x] lh_lora_trainer_v411_bind.py 训练脚本就绪
- [x] 电商信任重建协议 v1.0 落档 `01_protocols/LH-ECOM-TRUST-REBUILD-v1.0.md`
- [x] 电商信任数学建模引擎 `bin/lh_ecom_trust_engine.py` 12/12全绿
- [x] 电商信任数学论文 `papers/LH-ECOM-TRUST-MATH-MODEL-v1.0.1.md` 4定理证明
- [x] 全系统复盘：黎曼/责任塌缩/易经世界 3论文→引擎落地
- [x] 跨模块路由总线 `bin/lh_cross_module_router.py` 10条回调链·12/12
- [x] 全系统集成测试 `bin/lh_system_integration_test.py` 30/30·85/85全绿
- [x] 学习融合总手册 v1.0.2 落档 `01_protocols/LH-LEARN-INTEGRATE-MANUAL-v1.0.2.md`·12/12全绿
- [x] **未成年守护引擎** `bin/lh_minor_guard_engine.py`·P0·17/17全绿·归一化半群+组合判定格+EWMA低通滤波+三视角融合+误报约束

### 📋 冻结
- 数字人民币/多币种 (金融红线)
- EUV光刻机 (需国家认证)
- longhun888.com 建站

---

## 更深上下文 → 读这些

| 想了解 | 读这个文件 |
|:---|:---|
| 记忆外脑协议·压缩引擎·心跳·生命周期 | `01_protocols/LH-MEMORY-ETERNITY-EXOBRAIN-v1.0.md` |
| 完整训练日志/checkpoint路径/知识摄入详情 | `.codebuddy/memory/CODEBUDDY_KIMI_SHARED.md` |
| 长期记忆/基础设施/引擎列表/项目历史 | `.codebuddy/memory/MEMORY.md` |
| 今日操作日志 | `.codebuddy/memory/YYYY-MM-DD.md` |
| 人格治理/审计/熔断/认证体系 | `01_protocols/LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md` |
| 系统拓扑/架构/引擎/技能 | `.codebuddy/longhun_neural_net.json` |
| 德本审计五条底线 | `01_protocols/LH-DEBEN-AUDIT-v1.0.md` |

---

## 更新规则

- 模型状态/变量变更 → 立即更新本文件 §快速状态卡 + §当前变量
- 待办变化 → 更新 §待办
- 锚点/格式规范 → 极少变动·变更需UID9622确认
- 每日操作细节 → 写入 `.codebuddy/memory/YYYY-MM-DD.md`，不写入本文件

---

> v1.0 · 2026-07-20 · 统一入口
> 从哪进的都读这一份 → 所有AI对齐
> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
