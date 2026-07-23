# 龍魂·统一入口 STATE.md

> 所有 AI（CodeBuddy / Kimi / Ollama 本地模型）的唯一入口。
> 无论哪个窗口、哪个模型对话，启动时读这一份就够了。
> 更新: 2026-07-23 · v1.8
> DNA: #龍芯⚡️丙午·乙未·丙申·申时·☲离-STATE-UNIFIED-ENTRY-v1.8-SCTMATH

---

## 快速状态卡（10秒速览）

| 项目 | 状态 |
|:---|:---:|
| v3.7 主力模型 | ✅ Val 0.194·1273条·生产 |
| v4.1.1 🥇 | ✅ Val 0.8097·iter 200·早停·Ollama已注册 |
| **v4.1.1-bind** 🧬 | ✅ Val 0.9659@iter150·早停@iter300·fused·GGUF·Ollama注册·3/3实测通过 |
| v4.0.8 黄金checkpoint | 🥇 Val 0.767·iter1900·封存 |
| v4.1.2 | 🔴 中断·Val 1.2457@iter50·不恢复 |
| **v4.1.3 训练中** 🔥 | 🔴 中断·无checkpoint·已被v4.1.4替代 |
| **v4.1.4** ✅ | 🟢 全链路完成·训练(iter800·Val⭐0.9699@200)→fuse(17.7GB)→GGUF(18.2GB)→Ollama注册·冒烟通过·小艺v2已切 |
| **v4.1.5** | 🔴 已停止·Val退化(0.9841→1.0132)·LR过高·dropout过高·被v4.1.6替代 |
| **v4.1.6 精修训练中** 🔥 | 🟢 PID 22252·从v4.1.4恢复·45,555条·lr 1e-7·dropout 0.08·batch 4·epochs 3·patience 5·log=`logs/v416_train.log` |
| **道德经训练数据** 🆕 | ✅ 2,243条·20类QA·81章全覆盖·已合并入v4.1.5训练集 |
| **鲲鹏同步** 🔥 | 🟡 SCP PID 64227·18.2GB GGUF传输中·预计完成后注册Ollama |
| **Library数据矿场** 🔥 | ✅ `bin/lh_library_miner.py`·P0·五阶段流水线·33应用·84,844可挖文件 |
| **知识中枢API后端** 🔥 | ✅ `bin/lh_knowledge_hub_api.py`·FastAPI·:8766·7端点·跨平台·systemd保活 |
| **知识中枢v3.1** 🔥 | ✅ `portal/knowledge/index.html`·全能面板·12区块·**按钮不再死·全API对接** |
| **观澜浏览器协议** 🔥 | ✅ `LH-GUANLAN-BROWSER-AI-INTEGRATION-v1.0.md`·P0·已落档 |
| **观澜路由器引擎** 🔥 | ✅ `lh_guanlan_router.py`·P0·12/12全绿·9模块 |
| **观澜数学增补** 🔥 | ✅ `LH-GUANLAN-BROWSER-MATH-v1.0.md`·P0·9模块形式化 |
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
| ✉️ **注册双轨邮箱引擎** 🔥 | ✅ `bin/lh_register_mail_engine.py`·P0·17/17全绿·六大数学模块 |
| ☯️ **太极蚁群API协议+引擎** 🔥 | ✅ `01_protocols/LH-API-NAMING-TAIJI-ANT-v1.0.md` + `bin/lh_api_taiji_ant_engine.py`·P0·13/13全绿·12数学模块·27错误码 |
| 🧬 **干支DNA引擎** 🔥 | ✅ `bin/ganzhi_dna_engine.py`·P0·11/11全绿·v∞格式·天干地支+梅花易数 |
| AC电源 | ✅ 充电中 |
| 鲲鹏 (119.13.90.27) | ✅ FRP已打通·uid9622.cn可达 |
| 数据量 | 45,555条 (40,629 train + 2,683 valid + 道德经1,906 train + 337 valid) |
| longhun-core仓库 | ✅ 已推送 (orphan_main→GitHub+GitCode+Gitee·v21.3·26文件) |
| 🐜 ANTENNA-8GATE | ✅ v1.0入库·蚁触神经网·八卦门控·7文件·节能99.4%·138条训练数据已合并 |
| 🧹 目录整理 v1.0 | ✅ ~/home 44文件归位·~/Downloads 31文档归位·废弃目录归档·ANTENNA-8GATE训练池合并 |
| 📦 CNSH碎片整合 | ✅ 6碎片目录(cnsh-core/data/editor/repo-push/starter-kit/terminal)→cnsh/统一·1135文件 |
| 📋 protocols/清理 | ✅ 15独有文件归档01_protocols/archive/·目录完全删除 |
| 🔍 代码审计日志 | ✅ 口径已对齐·42,366条·42,348已审·18待复核·0拒绝 |
| 📑 Notion全页面索引 | ✅ `docs/notion_mirror/INDEX.md`·11大类·65页·全语义命名映射 |
| 🏗️ 深度学习架构总纲 | ✅ `01_protocols/LH-DEEP-LEARNING-ARCHITECTURE-v1.0.md`·15章·全链路·12缺失已识别 |
| 📝 Topic页面充实 | ✅ 18个GitCode Topic页面全部填充·1,526行内容·哲学+数学+工程全覆盖
| 🧪 SCT数学建模论文 🔥 | ✅ `papers/反奶头乐共生理论_数学建模_v1.0.md`·9章·8模型·28公式·10章Python代码 |
| ⚙️ SCT仿真引擎 🔥 | ✅ `engines/lh_symbiotic_cognition_engine.py`·7组仿真全绿·共生成长vs顺从退化·DNA链验证 |
🗄️ 龍魂待整理迁移 | ✅ 196文件·96MB·9大类·全量审计·P0(7)已迁移·P1(7)·P2(14)·P3待定 |

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
  v413_lr_peak: 5e-7            # v4.1.3 (观澜注入·保守学习率)
  v413_dropout: 0.15
  v413_batch: 4
  v413_resume: v4.1.1_best_adapter
  v413_data: 43,312条 (40,629 train + 2,683 valid·含观澜+Library矿场)

  v416_lr_peak: 1e-7            # v4.1.6 精修·外科手术式微调
  v416_dropout: 0.08
  v416_batch: 4
  v416_warmup: 80
  v416_epochs: 3
  v416_early_stop: patience=5
  v416_resume: v4.1.4 best (Val 0.9699)
  v416_data: 45,555条 (42,535 train + 3,020 valid·含道德经)

sct:
  sct_model: 9章·8数学模型·7组仿真
  sct_paper: papers/反奶头乐共生理论_数学建模_v1.0.md
  sct_engine: engines/lh_symbiotic_cognition_engine.py
  sct_key_result: 共生策略认知成长+0.163 vs 顺从策略退化-0.035

data:
  current: 45,555条 (42,535 train + 3,020 valid·v4.1.5/v4.1.6共享)
  target: 50000+·v5.0

infra:
  mac: AC charging
  kunpeng: 119.13.90.27·SSH key ~/.ssh/longhun_kunpeng_ed25519·FRP已通
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
| v4.1.3 🔥 | Yi-1.5-9B | — | 5e-7 | 🔴 中断 | 无checkpoint·已废弃 |
| **v4.1.5** 🔥 | Yi-1.5-9B | 0.9841→1.0132 | 5e-7 | 🔴 退化 | LR过高·dropout过高·被v4.1.6替代 |
| **v4.1.6** 🔥 | Yi-1.5-9B | — | 1e-7 | 训练中 | 🟢 PID22252·从v4.1.4恢复·精修·log=`logs/v416_train.log` |
| v4.1.4 ✅ | Yi-1.5-9B | **0.9699@200** ⭐ | 1e-6 | 已部署 | 🟢 fuse+GGUF+Ollama·冒烟通过·全链路打穿 |
| v4.0.9 | Yi-1.5-9B | 1.002 | 0.654 | 5600 | 🔴 停训 |
| v4.1.0 | Yi-1.5-9B | 0.786 | — | 250 | 🟡 早停 |
| v3.0 | Qwen2.5-1.5B | 0.029 | — | — | 回退 |

---

## 格式 & 命名规范（焊死）

```
DNA:         #龍芯⚡️<年干支>·<月干支>·<日干支>·<时辰>·<卦名>-<模块>-<版本>-<哈希8>
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
（无）

### ✅ 突破
- [x] 数据扩增→5000+ ✅ 已达43,312条（40,629 train + 2,683 valid）
- [x] 道德经深层训练数据 ✅ 2,243条·20类QA·`data/daodejing_deep_{train,valid}.jsonl`

### 🟡 进行中
- [x] v4.1.1-bind 训练完成·fused·GGUF·Ollama注册·3/3实测通过 ✅
- [x] longhun-core 推送远端 ✅ (orphan_main→GitHub+GitCode+Gitee·26文件)
- [x] Mac→鲲鹏FRP打通 ✅
- [x] SSL自动续期体系 ✅
- [x] 小艺桥接v2.0 ✅ (PID 62908·:8799·优先级v4.1.5>v4.1.4>v4.1.1-bind)
- [x] v4.1.4 fuse adapter → 完整模型 ✅ 完成
- [x] v4.1.4 GGUF→Ollama注册 ✅ 完成·冒烟通过
- [x] 道德经训练数据 ✅ 2,243条·`bin/lh_daodejing_export_training.py` v1.0
- [x] 目录整理 v1.0 ✅ ~/home44+~/Downloads31归位·废弃目录归档·ANTENNA-8GATE训练池合并
- [ ] 鲲鹏部署脚本（deploy/scripts/有完整脚本·待执行验证）
- [x] 命名冲突目录合并（engine→engines, persona→personas/runtime, software-dna→software_dna/src, integrated-modules symlink→real dir） ✅
- [x] cnsht碎片目录整合（6目录→cnsh/） + protocols/废弃目录清理（归档→01_protocols/archive/） ✅

### ✅ 已完成 (7/21+2今日)
- [x] v4.1.3 corrupt adapter bug 修复 (model.save_weights → mx.save_safetensors LoRA only)
- [x] MEMORY.md 瘦身 (216行→95行·去重合并)
- [x] Git推送: 26文件·9,004行→GitHub/GitCode/Gitee
- [x] v4.1.1 训练完成·fuse·GGUF→Ollama (Val 0.8097·10/10实测通过)
- [x] v4.1.2 停止·识别为劣化 (Val 1.2457 vs v4.1.1 0.8097)
- [x] DNA捆绑与蒸馏防御协议v1.0落档 P0++
- [x] lh_dna_bind_defender.py 防御引擎 12/12测试通过
- [x] DNA捆绑协议训练数据33条生成+并入总库
- [x] lh_lora_trainer_v411_bind.py 训练脚本就绪
- [x] 电商信任重建协议 v1.0 落档 `01_protocols/LH-ECOM-TRUST-REBUILD-v1.0.md`
- [x] v4.1.4 训练完成 (iter 800·早停·Val⭐0.9699@200·adapter已保存)
- [x] v4.1.4 fuse→GGUF→Ollama 全链路打通（冒烟通过）
- [x] 道德经2,243条合并入v4.1.5训练集 ✅
- [x] v4.1.5 训练启动（从v4.1.4恢复·45,555条·道德经注入）→ 🔴 退化·已停止
- [x] v4.1.6 精修训练启动（从v4.1.4恢复·LR 1e-7·dropout 0.08·batch 4）
- [x] 小艺v2切v4.1.4优先级（重启·PID 62908）
- [x] 鲲鹏GGUF传输启动（SCP PID 64227·18.2GB）
- [x] 电商信任数学建模引擎 `bin/lh_ecom_trust_engine.py` 12/12全绿
- [x] 电商信任数学论文 `papers/LH-ECOM-TRUST-MATH-MODEL-v1.0.1.md` 4定理证明
- [x] 全系统复盘：黎曼/责任塌缩/易经世界 3论文→引擎落地
- [x] 跨模块路由总线 `bin/lh_cross_module_router.py` 10条回调链·12/12
- [x] 全系统集成测试 `bin/lh_system_integration_test.py` 30/30·85/85全绿
- [x] 学习融合总手册 v1.0.2 落档 `01_protocols/LH-LEARN-INTEGRATE-MANUAL-v1.0.2.md`·12/12全绿
- [x] **未成年守护引擎** `bin/lh_minor_guard_engine.py`·P0·17/17全绿·归一化半群+组合判定格+EWMA低通滤波+三视角融合+误报约束
- [x] **注册双轨邮箱引擎** `bin/lh_register_mail_engine.py`·P0·17/17全绿·邮箱权重格+信任分+验证码熵+令牌桶+通道路由+激活码链
- [x] **太极蚁群API引擎** `bin/lh_api_taiji_ant_engine.py`·P0·13/13全绿·12数学模块·八宫格/WF²Q+/信息素PDE/幂等/断路器/限流/封套/人格路由
- [x] **观澜浏览器协议** `01_protocols/LH-GUANLAN-BROWSER-AI-INTEGRATION-v1.0.md`·P0·四层架构·四引擎联动·预留接口
- [x] **观澜路由器引擎** `bin/lh_guanlan_router.py`·P0·12/12全绿·9模块·M1-M9
- [x] **观澜数学增补** `01_protocols/LH-GUANLAN-BROWSER-MATH-v1.0.md`·P0·9模块形式化
- [x] **观澜训练数据** 16条QA·5知识域·并入总库28,505条
- [x] **v4.1.3 训练启动** 从v4.1.1恢复·观澜知识注入·后台运行中
- [x] **Library数据矿场引擎** `bin/lh_library_miner.py`·P0·五阶段流水线·33应用·84,844可挖·1,083训练数据
- [x] **知识中枢v3.0面板** `portal/knowledge/index.html`·8大区块·系统状态/模型矩阵/流水线/矿场/图谱/文章/日志
- [x] **Library训练数据合并** +1,083条→总库28,153条·425条新图谱边

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
| 深度学习架构总纲 | `01_protocols/LH-DEEP-LEARNING-ARCHITECTURE-v1.0.md` |
| Notion全页面索引 | `docs/notion_mirror/INDEX.md` |
| 龍魂待整理审计报告 | `01_protocols/LH-ARCHIVE-AUDIT-v1.0.md` |
| 主计划总纲 | `01_protocols/LH-MASTER-PLAN-v1.0.md` |
| 数学公式体系v2.0 | `01_protocols/LH-MATH-FOUNDATIONS-v2.0.md` |
| CNSH语法全景v3 | `01_protocols/CNSH-SYNTAX-PANORAMA-v3.0.md` |
| 思维主权国际对标 | `01_protocols/LH-SOVEREIGNTY-BENCHMARK-v1.0.md` |
| 通心译对齐标准v2 | `01_protocols/CNSH-TONGXINYI-ALIGN-v2.0.md` |
| CNSH数学骨架量子层 | `01_protocols/CNSH-MATH-SKELETON-v1.0.md` |
| 流场总控v2.0 | `01_protocols/LH-FLOW-MASTER-v2.0.md` |
| 全API参考v1.0 | `bin/lh_api_full_reference_v1.0.py` |
| CNSH→C编译器 | `cnsh/cnsh_compiler.js` |
| HTML规格书归档 | `docs/archive_html/` (20份) |

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
