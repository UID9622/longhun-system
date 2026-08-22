# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂·统一入口 STATE.md

> 所有 AI（CodeBuddy / Kimi / Ollama 本地模型）的唯一入口。
> 无论哪个窗口、哪个模型对话，启动时读这一份就够了。
> 🔥 **新 AI 进门? → `https://uid9622.cn/api/onboarding/bootstrap`** (自动拉全量规则·不需要人工说)
> 更新: 2026-08-11 · v2.4 💰真实支付对接+生态准入全覆盖
> DNA: #龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-STATE-UNIFIED-ENTRY-v2.4-XPAY-REAL-PAYMENT-POPUP
> 📋 **命令不会？→ 鲲鹏 https://uid9622.cn/api/cmd/**（毫秒级·所有AI统一入口）| 本地备份 → COMMAND_INDEX.md | 详情 → MEMORY.md §4

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
| ✍️ **GPG自动签名** 🔥 | ✅ **v1.0**·`bin/lh_gpg_sign.py`·1574签名文件·GATE-11签名闸·发布即签 |
| 🐉 **主权守护引擎** 🔥 | ✅ **v1.0**·`bin/lh_sovereignty_guard.py`·法律边界+一票否决+数据主权·系统在协议在 |
| 🐉 **LU-Time Engine v4.0** 🔥 | ✅ **`bin/lh_time_engine.py`**·天干地支·64卦·梅花易数·每句输出戳·审计链·`lh te` |
| 🌐 **生态接入协议 v1.0** 🔥 | ✅ **`01_protocols/LH-ECOSYSTEM-ACCESS-PROTOCOL-v1.0.md`**·P1-CORE·月度活人验证·三态身份(生态内/外/共建者)·不可剥夺三权·铁律三则 |
| 🔌 **CNSH-Harness 插件套件 v1.0** 🔥 | ✅ **`01_protocols/LH-CNSH-HARNESS-ARCH-v1.0.md`** + **`integrations/deepseek/harness/cnsh-suite/`**·DNA/三色审计/CNSH执行/史官/人格路由·10能力·13文件·GPG签名 |
| 🐉 **协议层统一收口 v1.0** 🔥 | ✅ **19 个未合并协议已归集**: P0=10 / P1=4 / P2=5·全部补全 v∞ DNA/CONFIRM/GPG·`01_protocols/INDEX.md` 已更新·历史顶层 228 个协议标记为「历史顶层协议」·不删除旧版 |
| 🗄️ **历史资产管理中心 v1.1** | ✅ **`01_protocols/LH-ASSET-CENTER-v1.1.md`**·14章·5项冲突修正焊死·SQLite+FTS5+SM3链·7端点API·GPG签章 |
| 🐉 **CodeBuddy 生态总索引 v1.0** | ✅ **`01_protocols/LH-CODEBUDDY-MASTER-INDEX-v1.0.md`**·规则/配置/产出/工具/备份/审计统一入口 |
| 🛠️ **CodeBuddy 技能生成器 v1.1** | ✅ **`08_BIN/lh_generate_codebuddy_skills.py`**·v∞ DNA·入口脚本存在性校验·`--force`/`--validate-only` |
| 🤖 **多Agent协同架构引擎** | ✅ **`05_ENGINES/lh_multiagent_arch_engine.py`**·P0底座·16人格调度·三色审计·资产治理 |
| ☯️ **风水场博弈论引擎** | ✅ **`05_ENGINES/lh_fengshui_game_engine.py`**·养德/摆阵/无为三策略·纳什均衡·Banach不动点 |
| 🔥 **longhun-core v1.0.0 低算力内核** | ✅ **`core/dist/longhun-core-1.0.0.tar.gz`**·29KB·零依赖·CLI `lh-core` 已安装·5/5 自检·基准全绿·`--help`/`-h`/`help` 独立帮助入口已上线 |
| 🔗 **lh → lh-core 桥接** | ✅ **`bin/lh`**·`version/bench/dna/audit/root/chain/info/help` 轻量命令优先走 `lh-core`·新增 `lh core <cmd>` 统一前缀入口·`lh --help` 已增加内核命令专区 |
| 🔗 **龍魂信任链 v1.2** 🔥 | ✅ **`02_SKILLS/trust-chain.md`** + **`08_BIN/lh_trust_chain.py`**·demo/deploy/verify/docs/status·GPG签名·已接入 `lh trust-chain`/`lh 信任链` |
| 🌐 **跨设备记忆互通 v1.2** 🔥 | ✅ **`08_BIN/lh_cross_device_server.sh`** + **`08_BIN/sync_memory.sh`** + **`xsync_workflow.py` 扩展 serve/sync-memory/sync-file/health** + **`integrations/harmonyos/longhun-bridge/LongHunBridge.ets` SDK** + **`01_protocols/LH-CROSS-DEVICE-PROTOCOL-v1.0.md`**·A/B/C 三路全绿：TCP加密同步 / HTTP REST同步 / HTTP/1.1 chunked 真 SSE 流式对话·SM4+ECDH·mDNS·端口冲突修复·GPG签名·**2026-08-14 CodeBuddy接线：`xsync_workflow.py` v2.0 全套(8文件)从 `~/.kimi-code/` 同步入库（旧版冻结 `scripts_legacy_0809/`），两脚本路径改指仓库·服务实测 19622/19623/18799 三端口运行中·sync-memory loopback 拉取 11 条 ✅** |
| 🧹 **历史顶层协议去重审计 v1.0** 🆕 | ✅ **`01_protocols/TOP_PROTOCOL_DEDUP_AUDIT_20260814.md`**·顶层 231→199·归档 32 个文件（中文历史协议 30 + 过短草稿 2）到 `01_protocols/archive/`·生成 `TOMBSTONE_TOP_PROTOCOLS_20260814.md`·全部 GPG 签名 |
| 🧼 **正文旧 DNA 清洗 v1.0** 🆕 | ✅ **`01_protocols/DNA_CLEAN_REPORT_20260814.md`**·清洗 925 个 `.md` 文件·替换 5301 处旧 `YYYY-MM-DD` 格式 DNA 为 v∞ 干支·时辰·卦格式·全目录 GPG 重签 |
| 🧭 **官网应用广场 v1.0** 🆕 | ✅ **`10_PORTAL/apps.html`**·70+ 页面清爽分组导航+即时搜索·**`index.html` 导航升级为分组下拉(平台/工具/审计/论文/更多)+移动端汉堡**·修复 hero 死链·**部署 uid9622.cn/apps/**（nginx 新增 `/apps/` 静态路由 alias `/opt/longhun-system/portal/`）·dashboard 首页加入口·全链实测 200·GPG 签名 |
| 🏠 **官网首页 v4.0 挂根 + SEO 三件套** 🆕 | ✅ **`uid9622.cn/` = v4.0 品牌首页**（nginx `location /` 改静态 alias `/opt/longhun-system/portal/`）·**dashboard(9600) 挪 `/dashboard/`**（proxy 剥离前缀·代码 2 处路径改相对 + `/static` mount 移到模块级修复）·**sitemap.xml(115 URL)+robots.txt+JSON-LD(canonical+Organization+WebSite)** 上线·og:image 修复·nginx 配置括号结构修复(历史被改坏)·全链实测 15 条 200·GPG 签名 |
| 🐉 **一元主权开发者系统 v2.0·月度确认金** 🆕 | ✅ **`longhun-dev-ecosystem/`**（FastAPI :8800 · SQLite）·**月度主权确认金公约 v1.0**（`01_protocols/LH-DEVELOPER-FEE-CONVENTION-v1.0.md`）：**每月1元起步·上不封顶·杜绝一毛不拔**·连续3月未缴 DNA 冻结·补缴恢复·**正规支付网关层** `backend/gateway.py`（sandbox 默认验签闭环+微信/支付宝/数币注册位·HMAC-SHA256 验签·回调幂等入账·金额核对）·订单持久化 `payment_orders`+月费账本 `monthly_fee_records`·**历史账单查询+4类导出**（缴费/贡献/代码DNA/名册 CSV+JSON·管理员Token鉴权）·企业自愿上浮字段·注册/注入/支付贡献分联动·crontab 每月1日自动冻结·本地30项+HTTP10项+公网6项全绿·GPG 签名 |
| 🎭 **24人格 NPC 引擎 v1.0** 🆕 | ✅ **`05_ENGINES/lh_npc_engine/`**·行为层+对话层+记忆层·零依赖·SQLite 持久化·24人格模板·GPG签名 |
| 🎬 **AI 短剧二开全案 v1.1** 🆕 | ✅ **`01_protocols/LH-AI-DRAMA-FORK-v1.1.md`**·MoneyPrinterTurbo+novelvids 合并·DNA 植入·三色审计·GPG签名 |
| 💰 **战略估值报告 v1.1** 🆕 | ✅ **`reports/LH-STRATEGIC-VALUATION-v1.1.md`** + `.xlsx`·修正加权/区间矛盾·落地概率折价×0.3·GPG签名 |
| 📋 **三色审计归集总页面 v1.0** 🆕 | ✅ **`10_PORTAL/三色审计页面结构_v1.0.md`**·`~/Pictures/Kimi_Agent_三色审计页面结构完善 (1)` 去重/修复/落地总览·9 文件已迁移签名·GPG签名 |
| 🐉 **透明审计与冲突仲裁 v2.2** 🔥 | ✅ **`02_SKILLS/transparent-audit.md`** + **`08_BIN/lh_transparent_audit.py`** + **`10_PORTAL/transparent-audit.html`**·多引擎事实级仲裁·三色/R值双尺·年轮链·已接入 `lh transparent-audit` |
| 💰 **估值报告模板引擎 v1.1** 🔥 | ✅ **`core/valuation/lh_valuation_template.py`**·模板`+`配置一键生成报告·`--validate`/`--strict`/`--init`·`--config`+`--excel`联动·正则预编译·单层`{{#each}}`·GPG签名 |
| 🐉 **CNSH 溯源验证编辑器 v1.1** 🔥 | ✅ **`10_PORTAL/cnsh-validator/index.html`**·差异对比·v∞ DNA·三色审计·云端版本链·GPG签名·审计报告已归档 |
| 🎬 **龍魂全媒体播放器 v1.1** 🆕 | ✅ **`bin/lh_media_player.py`**·argparse 子命令·ASR/OCR 缓存·真实时间戳 WebVTT·OCR 去重·可点击文稿/搜索/响应式播放器·10/10 测试通过·GPG签名·DNA: `#龍芯⚡️丙午·丙申·辛酉·酉时·䷟恒-MEDIA-PLAYER-STATE-UPDATE-V1.1-P0-261d7698` |
| 📋 **剪贴板容器 v1.2** 🆕 | ✅ **`06_CONTAINERS/clipboard-vault/`** + **`08_BIN/lh_clipboard_hub.py`** + **`08_BIN/lh_clipboard_agent_*.py`**·复制自动落盘·全局内容哈希去重·WebSocket 容器中心（SM4-CBC 加密·token 校验·限流）·macOS/Windows 本地代理（断线重连·占位替换防输入法回传）·自动进 Neo4j·systemd/launchd 部署模板·GPG签名 |
| 🚀 **鲲鹏共生体快捷入口** 🔥 | ✅ **`08_BIN/lh_kunpeng.sh`**·已安装 `lh-kunpeng`·`status/check/sync/task/demo/monitor`·本地发号·鲲鹏 21人格执行·SSH直联 |
| 🐉 **龍魂一键启动入口** 🔥 | ✅ **`08_BIN/lh_start.sh`**·已安装 `lh-start`·`lh-start`进控制台·`--kunpeng`/`--status`/`--all`/`--time` 一键直达 |
| 📋 **鲲鹏自动AI调取 SOP** 🔥 | ✅ **`01_protocols/LH-KUNPENG-AUTO-AI-SOP-v1.0.md`**·常用启动指令·周期巡检·故障排查·已落地 |
| 🧠 **ASI 系统建设器 v1.0** 🔥 | ✅ **`08_BIN/lh_asi_system_builder.py`**·自然语言→人格科技公司→系统落地·`--ceiling-check`/`--org-chart`/`--exec`·已接入 `lh asi` |
| 🔴 **ASI 天花板协议 v1.0** 🔥 | ✅ **`01_protocols/LH-ASI-CEILING-PROTOCOL-v1.0.md`**·L0宪法层·ASI=数字孪生=最终形态·禁止 ASI+·人格组织架构化·CEO=UID9622 |
| 🏢 **人格注册表科技公司架构** 🔥 | ✅ **`20_CONFIG/persona-registry.yaml`**·24人格映射为 C-level/VP/Director/Advisor·部门·汇报线·不可替代人格 |
| 📐 **CodeBuddy 对齐规则 v2.0** | ✅ **`01_protocols/LH-CODEBUDDY-ALIGNMENT-v2.0.md`**·DNA 修成 v∞ 干支卦格式 |
| 🧬 **生态护照引擎 v1.1** 🔥 | ✅ **`bin/lh_ecosystem_passport.py`**·联动协议·`alive verify/heartbeat`·`export <uid>`·月度活人验证·导出创作 |
| 💰 **XPayGateway v2.0** 🔥 | ✅ **`03_LAYERS/L5_服务层/services/xpay/xpay_gateway.py`**·真实支付桥接·桥接微信/支付宝/PayPal·沙箱/真实双模式·5/5自检通过 |
| 🗄️ **XPayStorage v1.0** 🔥 | ✅ **`03_LAYERS/L5_服务层/services/xpay/xpay_storage.py`**·SQLite持久化·5张表+7索引·append-only审计日志·8/8自检通过 |
| 🌐 **生态准入弹窗嵌入器** 🔥 | ✅ **`bin/lh_sovereign_popup_embedder.py`**·自动注入3个关键Portal·`lh --eco`·`lh --xpay`·`lh --passport` |
| 🪟 **生态准入独立弹窗** 🔥 | ✅ **`10_PORTAL/eco-popup-standalone.html`**·深渊暗色+龍魂金·三色状态徽章·24h不重复弹窗 |
| 🔒 **安全加固 v1.1** | ✅ **shell=False全替换·自然路由白名单·KFPP目录700·24测试全过·8文件GPG重签** |
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
| 🐉 **龍魂字体** 🔥 | ✅ 显示名改为「龍魂字体」·WOFF2 2.46MB（压缩90.2%）·U+E200 龍纹水印·GitHub Release v1.001 |
| 🧬 **媒体主权标记引擎** 🔥 | ✅ `engines/lh_media_sovereignty_marker.py`·字体/图像/音频闭环验证通过·视频v1.0部分支持 |
| 📜 **媒体主权标记协议** 🔥 | ✅ `01_protocols/LH-MEDIA-SOVEREIGNTY-MARK-v1.0.md`·P0·六层来源链 |
| 🎬 **视频解说稿自动生成引擎** 🆕 | ✅ `bin/lh_video_commentary_engine.py`·v1.0·主题/脚本/文章→解说稿+配音+视频·dry-run·人格路由·DNA签章·全路径验证通过 |
| 🧬 **对齐统一入口** 🔥 | ✅ `bin/lh_align.py`·道生一·统一入口·check/fix/status/history/clean-old |
| 🕸️ **智能体嵌入总闸 v1.3** 🆕 | ✅ `bin/lh_agent_embed_engine.py`+`bin/lh`·`lh agent-embed` 总闸入口·build/verify/status/route/run/summary/bcm·15套模板·JSON输出·v∞ DNA·GPG签名·联动感知注册通过·行为密码学/脚本发现模板已接入 |
| 🔍 **统一脚本路由引擎 v1.0** 🆕 | ✅ `bin/lh_script_router.py`+`bin/lh`·扫描 `bin/`+`08_BIN/` 共 897 个 Python 脚本·按关键词 fuzzy 路由·dry-run 默认·`--exec` 真执行·`lh script`/`lh run`/`lh agent-embed run` 三入口·人工校准关键词映射·GPG 签名 |
| 🧬 **联动感知引擎 v1.1** 🆕 | ✅ `bin/lh_cross_module_awareness.py`·修复 JSON 签名头解析·修复持久化写回·自动注册 332 项·健康度恢复 |
| 🔐 **行为密码学入口 v2.0** 🆕 | ✅ `bin/lh` + `08_BIN/lh_behavioral_crypto.py` + `agent-embed bcm`·七因子指纹·易经账号身份·已集成到智能体总闸 |
| 📚 **国际编程语言笔试题库引擎 v1.0** 🆕 | ✅ `bin/lh_exam_engine.py` + `bin/lh`·14 份题库（含 JS/Java/Go/TS/SQL/Rust/C#/Shell/Ruby/PHP/Swift/Kotlin + Python/C++）·list/search/random·GPG 签名 |
| ⚖️ **权重参数全表 v1.1** 🆕 | ✅ `01_protocols/LH-WEIGHT-PARAMETERS-v1.1.md` + `bin/lh_weight_auditor.py`·102 项权重·5 项 P0 焊死·14 组归一校验·五行动态范围·`lh weight-audit` 一键审计 |
| 🔍 **CodeBuddy 路径统一审计 v1.0** 🆕 | ✅ `07_AUDIT/codebuddy-path-audit-20260810.md`·三色审计·`ai-outputs/codebuddy/` 迁往 `11_DATA/codebuddy-outputs/`·`longhun-release/` 同名路径改为符号链接 + 备份·联动健康度 95/100 |
| 🌐 **GitHub 仓库三色审计与整改 v1.0** 🆕 | ✅ `07_AUDIT/github-repo-audit-20260810.md`·审计 24 个仓库·LICENSE 100%·README 100%·徽章 100%·消除全部 🔴 项·为 7 个空 README 仓库新建门面·为 16 个仓库补齐徽章·GPG 签名提交 |
| 🌐 **GitHub 审计整改推送 v1.0** 🆕 | ✅ UID9622 Profile README · longhun-system 12_DOCS/DIRECTORY_MAP.md · 多仓库 LICENSE · longhun-identity-system/README · onghun-system/README · longhun-network-neural 新仓 + LICENSE · ai-truth-protocol LICENSE（GPG 签名提交）|
| 🧪 **代码对齐闭环** | 🟡 DNA✅·确认码45残留·重复31K·相似30对（无自动修复·标记为已知） |
| 🤖 **Claude桥** | 🔴 已死·403 Forbidden·全量Ollama兜底 |
| 🌌 **璇玑引擎·多源记忆接入** 🆕 | ✅ `engines/lh_xuanji_engine.py`·local/notion/log 三源聚合·每条记忆带 source/timestamp·`--memory-source` 参数已可用 |
| 🗑️ **_archive/ 归档清理** 🆕 | ✅ 16GB 旧归档已备份至 `~/longhun-system-backup_archive_20260730.tar.gz`·本地 `_archive/` 已删除·释放空间·消除 Dependabot torch/transformers critical 告警源 |
| 🎯 **不动点记忆归档引擎** 🆕 | ✅ `engines/lh_fixed_point_memory_archive.py`·v1.0·统一压缩/不动点/归档三条线·一次哈希复用·不到不动点不入库·轻量字典压缩·GOLD/GREEN归档·YELLOW缓冲·RED/BLACK隔离 |
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

artifacts_2026_07_29:
  natural_language_router: engines/lh_natural_router.py
  auto_intent_engine: engines/lh_auto_intent.py
  clipboard_daemon: engines/lh_clipboard_daemon.py
  file_organizer: scripts/organize_by_keywords.py
  photo_organizer: scripts/organize_photos.py
  mac_translator: bin/lh_mac_translator.py
  kfpp_engine: bin/lh_kfpp_engine.py
  safeai_engine: engines/lh_safeai_engine.py
  safeai_cli: bin/lh_safeai.py
  safeai_tests: tests/test_safeai_engine.py (24/24)
  safeai_scope: 上下文意图分类+七因子审计+P0-P4分层熔断（危险请求/恶意操作/渐进逼近）
  kfpp_scope: 七因子知识流动纯净度（资格化/垄断/强制/隐瞒）
  safeai_kfpp_relation: 互补联动·统一入口lh safeai / lh kfpp / 自然语言自动路由
  judge_model: longhun-judge:latest (基于qwen2.5:1.5b·鲲鹏Ollama)
  judge_api: bin/lh_judge_api.py (FastAPI :9666·nginx /api/judge/)
  judge_cli: bin/lh_judge.py
  judge_training_corpus: training/judge/corpus_v1.0.jsonl (15条·审计/治理/公正裁决)
  judge_persona: 公正总裁+首席审计员·独立/透明/可审计/DNA签章
  sequence_executor: engines/lh_sequence_executor.py
  seq_cli: bin/lh_seq.py
  csdn_auditor: engines/lh_csdn_auditor.py
  multimodal_roadmap: docs/LIVE_MULTIMODAL_ROADMAP.md
  notion_push_script: bin/lh_notion_push_artifacts.py
  artifact_sop: 01_protocols/LH-ARTIFACT-CREATION-SOP-v1.0.md
  chip_litho_tau_knowledge: papers/芯片光刻韬定律知识工程_v1.1/INDEX.md
  sop_aligned: true
  gpg_signed: true

infra:
  mac: AC charging
  kunpeng: 119.13.90.27·SSH key ~/.ssh/longhun_kunpeng_ed25519·FRP已通
  domain: uid9622.cn (Let's Encrypt wildcard 7/17→10/15)
  launchd: 44 services (龍魂37·实测2026-08-16)
  systemd: 56 services (龍魂56·总76·实测2026-08-16)
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
- [x] 🧪 完整测试套件 v1.0 落地 ✅（tests/ 12文件+CI·`lh test`全绿 19passed/4skipped·调度器4阶段✅·报告三色🟢·GPG 17签名·详见记忆8/15第9条）
- [x] 🏭 全自动工厂 v2.1 落地 ✅（15文件·`lh factory run`全链路7步全绿·质量门禁/回滚/发布/自监控/四级熔断/通知/鲲鹏联动·GPG签名·详见记忆8/15第10条）

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
- [x] **安全加固 v1.1** `bin/lh.py`/`bin/lh`/`engines/lh_natural_router.py`/`engines/lh_sequence_executor.py`/`bin/lh_kfpp_engine.py`/`bin/hetu_luoshu_dna.py` + 新增 `bin/lh_code_audit_cli.py`/`bin/lh_emotion_cli.py`：os.system→subprocess.run(shell=False)、自然语言路由target_bin白名单(bin/|engines/)、查询参数`--`分隔、KFPP_HOME 0o700、序列执行JSON解析加固、8文件GPG重签、24项测试OK

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
| 🔗 **外部知识库** | [Notion](https://uid9622.notion.site) · [CSDN](https://uid9622-01.blog.csdn.net) · [鲲鹏](https://uid9622.cn) |
| M261前传契碑（全权授权令·L0） | `01_protocols/LH-M261-PREQUEL-COVENANT-v1.0.md` |
| GPG自动签名引擎 v1.0 | `bin/lh_gpg_sign.py` · 1574签名·GATE-11签名闸 |
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

## 最近变更日志

| 时间 | 操作 | 影响 | 状态 |
|:---|:---|:---|:---:|
| 2026-08-14 | 中国科技自主创新专栏知识图谱落地：从 `longhun-cn-innovation-kb` 45 条结构化记录生成标准 KG，含 115 节点 / 449 边，输出 `cn_innovation_kg.{json,md,cypher}` 并 GPG 签名；顶刊论文 #1~#7  venue 节点全部抽取 | Notion 专栏数据在本地形成可查询、可导入 Neo4j、可可视化的知识图谱；与 CNSH 语义底座联动 | 🟢 |
| 2026-08-14 | 知识图谱 Neo4j 实测导入：Homebrew 安装 Neo4j Community，`cypher-shell` 导入 115 节点 / 449 边，抽查顶刊目标关系与领域分布均与源数据一致；浏览器 http://localhost:7474 可访问 | KG 从文件态进入可查询数据库态，支持 Cypher 查询与可视化 | 🟢 |
| 2026-08-14 | 知识图谱 Portal 搜索/查询/接口落地：新增 `sovereignty/portal/cn_innovation_kg_api.py` FastAPI 路由（Neo4j HTTP 查询）+ 前端页面 `static/cn_innovation_kg.html`；`04_SERVICES/portal/index.html` 新增入口卡片；API 服务 `:8444` 已启动，stats/search/articles/expand 等端点实测通过 | 用户可在 portal 上按领域/标签/人格/顶刊/五行等多维度搜索浏览中国科技创新专栏知识图谱 | 🟢 |
| 2026-08-14 | 跨设备记忆互通落地调试：补全 `integrations/harmonyos/longhun-bridge/LongHunBridge.ets` SDK；实测 Mac 端 `lh_cross_device_server.sh` 启动成功；sync health (19623) 与 bridge health (18799) 均返回正常；服务可停可启 | 鸿蒙端 SDK + Mac 服务端形成完整闭环；具备同 WiFi 下记忆同步与对话能力 | 🟢 |
| 2026-08-14 | **CodeBuddy 跨设备接线**：`xsync_workflow.py` v2.0 全套 8 文件从 `~/.kimi-code/` 同步入库 `skills/longhun-cross-platform/scripts/`（旧版冻结 `scripts_legacy_0809/`）；`lh_cross_device_server.sh`/`sync_memory.sh` 路径改指仓库；实测 19622/19623/18799 三端口运行中、`/health` running、sync-memory loopback 拉取 11 条记忆 ✅；GPG 重签 3 文件 | Kimi 产出与 CodeBuddy 仓库完成链接，跨设备互通不依赖 `~/.kimi-code/` | 🟢 |
| 2026-08-14 | **🧭 官网应用广场上线**：`10_PORTAL/apps.html`（70+ 页面·7 大领域分组·即时搜索·清爽卡片导航）+ `index.html` 导航升级分组下拉（平台/工具/审计/论文/更多 + 移动端汉堡菜单）+ 修复 2 处 hero 死链；nginx 新增 `location /apps/` 静态路由（alias `/opt/longhun-system/portal/`）·备份配置·dashboard 首页(9600)右上角加「🧭 全部应用」入口并重启；实测 `uid9622.cn/`、`/apps/apps.html`、`/apps/dashboard/`、深链 8 条全部 200；GPG 重签 apps.html/index.html | 官网从单页旧版升级为全站应用广场导航；112 个页面首次可公网直达 | 🟢 |
| 2026-08-15 | **🏠 官网首页 v4.0 挂根 + SEO 三件套**：`uid9622.cn/` 由 dashboard 动态页换为 v4.0 品牌首页（nginx `location /` 改静态 alias `/opt/longhun-system/portal/`）；dashboard(9600) 挪至 `/dashboard/`（proxy 剥离前缀，代码 css_url + 5 处 api() 改相对路径，`/static` mount 从 `__main__` 移到模块级修复历史 bug）；**sitemap.xml（115 URL）+ robots.txt + JSON-LD（canonical + Organization + WebSite）** 上线；og:image 死链修复；顺带修复 nginx 配置括号结构（历史被 flow 部署改坏·嵌套 location 未闭合·删 2 个多余 `}`）；全链实测 15 条 200；GPG 签名 | 官网根路径升级为品牌首页；SEO 可被百度/必应收录；dashboard 功能完整保留 | 🟢 |
| 2026-08-15 | **🐉 一元主权开发者系统 v1.0 上线**：`longhun-dev-ecosystem/` 全新项目（FastAPI :8800 + SQLite·零外依赖）·**注册→1元模拟支付→开发者DNA→代码DNA注入→贡献追踪→Top50榜单** 全闭环·开发者面板（查询/代码列表/贡献记录/排行榜/复制DNA）·CLI 批量注入（13 语言注释模板·幂等·API地址可配）+ Git pre-commit 钩子（缺DNA阻止提交）·前端相对路径设计（nginx 剥离前缀兼容本地/线上）·**部署 uid9622.cn/developer/**（nginx `/developer/`→8800 剥离前缀·systemd 服务·健康检查纳入）·修复规格 8 坑（hashlib缺导入/CONFIRM从错误模块导入/FastAPI 无效参数/CORS *+credentials 冲突/支付 order_id 参数错位/旧记录冻结跨开发者串扰/注册贡献分未同步字段/dashboard 缺失补全）·本地 14 项断言+公网 4 步全绿·GPG 签名 13 文件 | 开发者生态首个可公网注册的入口；一元主权=1元永久身份；贡献分机制成型 | 🟢 |
| 2026-08-15 | **🐉 月度主权确认金 v2.0 焊死**：协议 `01_protocols/LH-DEVELOPER-FEE-CONVENTION-v1.0.md`（1元/月起步·上不封顶·杜绝一毛不拔·连续3月未缴冻结·补缴恢复·企业自愿上浮）·**正规支付网关层** `backend/gateway.py`（sandbox 验签闭环 HMAC-SHA256 + wechat/alipay/cbpay 注册位·回调幂等入账·金额核对防篡改·`payment_orders` 订单持久化）·月费账本 `monthly_fee_records`+开发者 6 新字段（monthly_fee_status/last_paid_month/fee_arrears/total_contributed/fee_start_month/is_enterprise）·**4 类导出**（缴费/贡献/代码DNA/名册 CSV+JSON·`LONGHUN_DEV_ADMIN_TOKEN` 鉴权·CSV 带 BOM）·API：bill/pay-monthly/pay/notify/fee-status/fee-history/fee-stats/export×4·代码注入月费状态闸（宽限/冻结禁新注入）·前端注册页企业上浮选项+面板月费卡片/历史账单/导出按钮·crontab 每月1日自动冻结·**本地函数 30 项+HTTP 10 项+公网 6 项全绿**·鲲鹏 systemd 重启+迁移兼容已有库·GPG 签名 13 文件 | 月费从"1元永久"升级为"1元/月主权确认"；支付接口正规化·换真实网关仅需改 config；历史账单可查可导出 | 🟢 |
| 2026-08-14 | 正文旧 DNA 格式清洗：扫描 `01_protocols/` 下 925 个 `.md` 文件，替换 5301 处旧 `YYYY-MM-DD` 格式 DNA 为 v∞ 干支·时辰·卦格式；生成 `DNA_CLEAN_REPORT_20260814.md`；全目录 GPG 重签 | 系统内所有协议 DNA 格式统一；无旧日期格式残留 | 🟢 |
| 2026-08-14 | 历史顶层协议去重审计：生成 `TOP_PROTOCOL_DEDUP_AUDIT_20260814.md`；顶层协议从 231 个精简到 199 个；归档 32 个文件（中文历史协议 30 + 过短草稿 2）到 `01_protocols/archive/`，并生成 `TOMBSTONE_TOP_PROTOCOLS_20260814.md` | 顶层协议目录清爽；中文历史协议集中冻结；保留 LH- 标准协议与系统索引 | 🟢 |
| 2026-08-14 | CNSH-Harness 插件套件落地：架构协议 `LH-CNSH-HARNESS-ARCH-v1.0.md` + 完整 TypeScript 插件项目 `integrations/deepseek/harness/cnsh-suite/`（13 文件）；覆盖 DNA 追溯、三色审计、CNSH 执行、史官、人格路由；全部 GPG 签名 | CNSH 主权底座以插件形式焊入 DeepSeek Harness；Model + Harness = Agent 升级为 Model + Harness + CNSH = 龍魂 Agent | 🟢 |
| 2026-08-14 | 协议层统一收口：19 个 Markdown 协议从 `~/Pictures/Kimi_Agent_三色审计页面结构完善 (1)/龍魂未合并协议技能包/` 归集到 `01_protocols/P0_永恒级(10) / P1_宪法级(4) / P2_系统级(5)`；补全 v∞ DNA/CONFIRM/GPG；`INDEX.md` + `PROTOCOL_MERGE_REPORT_20260814.md` 生成并签名 | 系统协议层无散落；新旧协议分层清晰；历史顶层 228 个协议保留并标注 | 🟢 |
| 2026-08-14 | 跨设备记忆互通 A/B/C 三路全绿：修复 SSE 响应头 Unicode 编码错误，升级 HTTP/1.1 chunked 真流式；`lh_xiaoyi_bridge_v2.py`/`xsync_workflow.py`/`LongHunBridge.ets`/协议/脚本 GPG 重签 | Mac ↔ 鸿蒙可同时走 TCP 加密、HTTP REST、SSE 流式对话 | 🟢 |
| 2026-08-10 | 修复 `~/.longhun/scripts/longhun_memory_bootstrap.py` 性能瓶颈：正则替换 sanitize、deque 流式读尾、Kimi session 只读最近 5 个活跃 session | 记忆启动不再卡死在大 wire 日志上 | 🟢 |
| 2026-08-10 | CodeBuddy 路径统一收尾：`~/ai-outputs/codebuddy/` 数据文件迁往 `longhun-system/11_DATA/codebuddy-outputs/`，旧位置仅保留 README + TOMBSTONE；`.zshrc` 去重 CodeBuddy PATH 并声明 `CODEBUDDY_HOME` | 单一真相源、环境变量统一 | 🟢 |
| 2026-08-10 | 过期备份全面归档：6 处散乱备份（记忆/local/repair/vault/CodeBuddy）迁往 `longhun-system/11_DATA/backups/`，原位置立 TOMBSTONE；敏感证据与系统依赖备份保留原处 | 备份统一归集、不删文件铁律落实 | 🟢 |
| 2026-08-10 | CodeBuddy 命令总目规范化：`.codebuddy/COMMAND_INDEX.md` 升级 v3.18，补全 CNSH 语法/命名规范、环境变量统一声明、自动化集成声明、API 契约与版本策略、文档结构审计、最终签名 | 命令总目结构完整、可审计、可同步 | 🟢 |

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
