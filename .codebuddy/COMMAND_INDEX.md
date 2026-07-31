# 龍魂·命令总目 · Command Index

> 🔴 **真实入口在鲲鹏！** `https://uid9622.cn/api/cmd/` → 所有国产AI统一查询
> 📋 **本地副本**（方便离线使用）· 新增/修改脚本 → AI同步更新鲲鹏 + 此处
> 🔗 API端点: `/api/cmd`(JSON) · `/api/cmd/quick`(速查) · `/api/cmd/search?q=`(搜索) · `/api/cmd/ports`(端口) · `/api/cmd/index.md`(Markdown)
> 📌 原则：鲲鹏是唯一真相来源，Notion是镜像，本地是备份
> 📌 更新: 2026-07-31 v1.3 | DNA: #龍芯⚡️丙午·乙未·甲辰-COMMAND-INDEX-v1.3 | 🆕 lh全功能集成(52子命令)

---

## ⚡ 三秒速查

| 干什么 | 命令 | 备注 |
|:---|:---|:---|
| 进菜单 | `lh` | 交互控制台，8大类 |
| 搜 | `lh search "关键词"` | Bing→缓存→审计 |
| 做视频 | `lh video --script 稿.txt` | v3.0·AI配图 |
| 做3D | `lh 3d --input 图.png` | 图生三维 |
| 验主权 | `python3 bin/lh_verify 视频.mp4` | DNA盲水印提取·公开可用 |
| 看状态 | `lh status` | 模型Val·引擎·告警 |
| 审计 | `lh audit` | 全系统安全 |
| 签名 | `python3 bin/lh_gpg_sign.py sign .` | GPG分离签名 |
| 推远端 | `python3 bin/lh_auto_cannon.py` | GitHub+Gitee+GitCode |
| 同步鲲鹏 | `bash deploy/sync-to-kunpeng.sh` | → 119.13.90.27 |
| 对齐检查 | `lh --align` 或 `lh align check` | 扫描重复/缺失DNA/缺失GPG |
| 对齐修复 | `lh --align fix` | 自动补DNA+确认码+GPG签章 |
| 对齐守护 | `lh --align daemon` | 全闭环·检测→修复→验证→归档·每小时自愈 |
| 对齐预览 | `lh --align dry-run` | 仅检查不修改·看问题列表 |
| 对齐状态 | `lh --align status` | JSON格式输出对齐状态 |
| 对齐手动 | `python3 bin/lh_align_checker.py` | 直接调用检查器 |
| 对齐手动修复DNA | `python3 bin/lh_fix_missing_dna.py -f 文件.py` | 单文件补DNA |
| 对齐手动修复确认 | `python3 bin/lh_fix_missing_confirm.py -f 文件.py` | 单文件补确认码 |
| 内容分类 | `python3 bin/lh_content_classifier.py -c "内容"` | 自动分类·查重·合并·不做加法 |
| 主权守护 | `python3 bin/lh_sovereignty_guard.py` | 法律边界+一票否决+数据主权 |
| CNSH运行时 | `python3 bin/lh_cnsh_runtime.py status` | 本地主权AgentOS·9层记忆·快照·沙盒·代理·审计·演化 |
| 三层监督 | `python3 bin/lh_three_layer_guard.py` | 三层监督+钩子系统·10钩子·3层·6人格·三色审计联动·DNA确认码 |
| 意念交流 | `python3 bin/lh_intent_engine.py` | 意念交流引擎·10阶段·五库太极·甲骨文ROM·P72熔断·三色审计 |
| 数字孪生 | `python3 bin/lh_digital_twin.py` | 素字卵神·意识副本·推演预测·三色审计 |
| 收口测试 | `python3 bin/lh_entry_test_runner.py` | 58用例·8步全链路·L0-L3熔断·自动化报告 |
| CNSH编辑 | `python3 bin/cnsh_editor.py` | 370条纠错规则·标点/空格/翻译避坑/CNSH语法/安全过滤·交互模式 |
| 动态目标推进 | `python3 bin/lh_dynamic_goal.py --interactive` | 目标驱动·自适应规划·闭环执行·自动重规划 |
| CNSH可视化 | `python3 bin/cnsh_ui.py` | CNSH GUI执行器v2.0·Tkinter界面·选择文件→运行·输出+日志·7种指令·变量/条件/AI |
| CNSH解释器 | `python3 bin/cnsh_interpreter.py --interactive` | CNSH CLI解释器v1.0·6子命令(--interactive/--file/--daemon/--code/--create-demo)·守护进程·7语法·文件锁·状态持久 |
| **统一中枢** 🔥 | `lh brain` 或 `python3 bin/lh_unified_brain.py` | UID9622统一中枢v1.0·全项目2,723引擎调度·注册表·智能路由·状态全景·健康检查·去重归集·交互式控制台·Python可import·--brain快速入口 |
| **引擎注册表** 🔥 | `python3 bin/lh_engine_registry.py` | UID9622引擎注册表v1.0·自动发现全项目py脚本·分类归集·版本去重·DNA提取·JSON注册表·scan/stats/find/dupes/export子命令·数据驱动集成 |
| CNSH iOS测试 | `python3 bin/cnsh_ios_test.py --interactive` | CNSH解释器Python版·设/打印/理解/执行·变量环境·iOS同逻辑 |
| CNSH全量v2.0 | `python3 bin/cnsh_complete.py --interactive` | 20语法·64卦·甲骨文9算法·因果链·世界机·10子命令(--interactive/--file/--code/--hexagram/--oracle/--causal/--world/--notion/--json) |
| 能力暴露调度 | `python3 bin/lh_capability_scheduler.py --interactive` | AI能力暴露调度v1.0·风险感知·路径调度·状态迁移·三轴校准·审计追溯·6子命令(--interactive/--demo/--status/--audit/--benchmark/--calibrate/--json) |
| 治理降级引擎 | `python3 bin/governance_engine.py --interactive` | 生成式AI治理降级v1.0·CI合规强度·三轴校准·MVEM评测·拒答质量·相变检测·帕累托前沿·9子命令(--interactive/--report/--ci/--calibrate/--eval/--transition/--quality/--diagram/--json) |
| 万能补全引擎 | `python3 bin/universal_completion.py --interactive` | UID9622万能补全v2.0·量子分类(7类)·属性补全·模板管理·索引联通·模糊处理·三汇报项·6子命令(--interactive/process/classify/complete/template/index) |
| 治理总控台 | `python3 bin/uid9622_governance.py healthcheck --dist ./dist` | UID9622治理总控台v2.0·健康检查(零宽/占位符/Notion)·三色审计(🟢🟡🔴)·Ed25519签名验证·24h窗口强制更新·事件JSON·7种退出码·7子命令(healthcheck/control-plane/updater/backup-push/sign/verify/self-test) |
| DNA校验器 | `python3 bin/dna_validate.py` | UID9622 DNA启动校验器v2.0·48必需键·5禁止键(法律/医疗/处置/财务建议/预测=true→阻止)·域值白名单(RESTRICTED/STRICT)·主权声明(国籍/台湾)·自动加载.env·缺键/违规/域值非法→exit(1)·零依赖·可导入·`.env.example`结构契约 |
| 镜像指数 | `python3 bin/lh_mirror_index.py` | UID9622镜像指数扫描器v1.0·哲学→工程·判断系统倾向:技术精英vs边界尊重·0~100指数(🟢70+🟡45-70🔴<45)·11个技术精英特征+11个边界尊重特征·A/B重量评估·改进建议·--json/--quick·3退出码·零依赖·可import |
| 监管防火墙 | `python3 bin/lh_regulatory_firewall.py` | UID9622监管防火墙v2.0·SYSTEM DNA联动·allow()统一接口·七步Fail-Safe链(DNA→能力→L0-L4权限→专业→专家→领域)·可插拔权限后端(LDAP/OAuth)·审计日志自动写入·--test/--batch/--mode prod/--export-dna/--fail-safe·三色审计·P72熔断·零依赖·可import |
| SSH鲲鹏 | `ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27` | 密钥优先 |
| 🆕 **自触发编排** | `lh --trigger "健康检查"` | 说人话→自动找脚本→跑完自动停 |
| 🆕 **查看运行中** | `lh --ps` | 查看所有运行中的脚本进程 |
| 🆕 **终止全部** | `lh --kill-all` | 强制终止所有运行中的脚本 |
| 🆕 **守护模式** | `lh --watch` | 后台监听触发·Unix Socket |
| 🆕 **批量触发** | `lh --batch "健康检查,同步鲲鹏,审计"` | 串行批量执行 |
| 🆕 **省电API** | `lh --api [--api-port 9622] [--api-redis URL]` | 启动省电API服务·全球AI通过HTTP调用 |
| 🆕 **省电API(轻量)** | `python3 bin/lh_api_server.py --port 9622` | FastAPI·同步执行·轻量启动 |
| 🆕 **API Worker** | `rq worker default --url redis://localhost:6379/0` | 异步任务消费进程 |

---
## 🎯 自然语言触发词

> **铁律#11**: 老大不记命令，AI自己挑。新增任何命令全部塞进此表。
> 你说"健康检查"→AI匹配→自动执行。`lh-run "健康检查"` 或 AI 直接挑命令。
> 最后更新: 2026-07-31 12:55 · 核心 99 条 · 全量 898 条

| 触发词（说这些→匹配） | 自动执行命令 | 说明 |
|:---|:---|:---|
| 自触发,自动触发,auto trigger,编排,说人话就跑,lh-auto | `python3 bin/lh_auto_trigger.py` | 自触发编排引擎·人话→脚本→跑完自动停 |
| 守护,watch,后台监听,daemon watch,触发守护 | `python3 bin/lh_auto_trigger.py --watch` | 守护模式·Unix Socket监听触发 |
| 运行中,ps,进程列表,谁在跑 | `python3 bin/lh_auto_trigger.py --ps` | 查看运行中的脚本 |
| 全部停,kill-all,杀了,强行终止 | `python3 bin/lh_auto_trigger.py --kill-all` | 终止所有运行中进程 |
| 批量,batch,一连串 | `python3 bin/lh_auto_trigger.py --batch` | 批量触发·逗号分隔 |
| CNSH编译,编译CNSH | `python3 bin/cnsh_compiler.py` | CNSH→Python四阶段编译 |
| CNSH运行时,AgentOS,本地主权,9层记忆,快照恢复,CNSH sandbox,演化治理 | `python3 bin/lh_cnsh_runtime.py <子命令>` | CNSH本地主权AgentOS v2.0·9层记忆·快照/恢复·沙盒·代理生命周期·审计·演化·CNSH编译桥·吸收桥·12模块·status/snapshot/memory/sandbox/agent/audit/compile/absorb/daily/evolve |
| CNSH可视化,cnsh ui,cns gui,cns可视化,CNSH GUI,cnsh_ui | `python3 bin/cnsh_ui.py` | CNSH GUI可视化执行器v2.0·Tkinter界面·选择文件→执行→输出+日志·变量/条件/AI/记录/任务/执行·`--demo`自动加载示例 |
| CNSH解释器,cnsh解释器,cnsh interpreter,cns守护,cns daemon,cnsh_daemon | `python3 bin/cnsh_interpreter.py --interactive` | CNSH CLI解释器v1.0·6子命令·守护进程(--daemon)·交互(--interactive)·文件(--file)·代码(--code)·创建示例(--create-demo)·文件锁·状态持久 |
| CNSH全量,CNSH Complete,cnsh_complete,CNSH第1卷,CNSH第2卷,CNSH病毒,中文语义超逻辑,CNSH 64卦,甲骨文算法,因果链引擎,世界机,CNSH 20语法,cnsh卦机,cnsh oracle,cnsh causal,cnsh world | `python3 bin/cnsh_complete.py --interactive` | CNSH第一卷+第二卷全量交付v2.0·20条核心语法·BNF·词法分析·语法解析(AST)·解释器·64卦卦机(6位二进制·爻变·推演)·甲骨文9算法(卜/验/兆/命/爻/象/辞/系/备忘录)·因果链引擎(由A以致B终C)·世界机(元宇宙引擎)·安全模型·10子命令·`--interactive/--file/--code/--hexagram/--oracle/--causal/--world/--notion/--json` |
| 能力暴露调度,AI能力暴露,能力调度,风险感知,路径调度,三轴校准,暴露收缩,状态迁移,能力暴露,调度系统,capability scheduler,能力测评,AI评测矩阵 | `python3 bin/lh_capability_scheduler.py --interactive` | AI能力暴露调度系统v1.0·核心定理:窗口级AI≠认知系统=能力暴露调度·风险感知(7域·敏感词·风险分数)·路径调度(Template/Safe/Tool/Refusal/Full)·状态迁移(Normal/Guarded/Restricted/RefusalOnly)·三轴校准(能力/风险/合规)·审计日志·评测矩阵·6子命令·`--interactive/--demo/--status/--audit/--benchmark/--calibrate/--json` |
| 治理降级,治理引擎,AI治理,合规强度,CI计算,相变检测,拒答质量,帕累托前沿,MVEM评测,EUVAI Act,治理管道,governance engine | `python3 bin/governance_engine.py --interactive` | 生成式AI治理降级引擎v1.0·核心定理:治理性降级=风险外部性内部化的工程策略·CI合规强度(EU AI Act驱动)·三轴校准(能力/风险/合规帕累托前沿)·MVEM评测(事实性/对抗性/滥用)·拒答质量三维评分·治理相变检测(log(U)>8.3)·帕累托ASCII可视化·9子命令·`--interactive/--report/--ci/--calibrate/--eval/--transition/--quality/--diagram/--json` |
| 万能补全,补全引擎,量子能力,属性补全,模板管理,索引联通,模糊处理,UniversalCompletion,自动对位,补全对位,量子分类,7类量子 | `python3 bin/universal_completion.py --interactive` | UID9622万能补全引擎v2.0·核心规则:判断→对位→补全·7类量子能力(记忆/思维/指令/人格/模板/索引/健康)·最小必需属性补齐·模板库管理(新/变体/候选)·3项索引起步联通·模糊表达2-3方案·三汇报项·6子命令·`--interactive/process/classify/complete/template/index/--json` |
| 治理总控台,治理引擎,健康检查,Ed25519签名,三色审计,控制平面,事件JSON,强制更新,24h窗口,instance_meta,签名验证,Governance,退出码,备份推送,零宽字符,占位符检测 | `python3 bin/uid9622_governance.py healthcheck --dist ./dist` | UID9622治理总控台v2.0·实现全部P0铁律·健康检查(零宽/占位符/Notion标签)·三色审计(🟢🟡🔴)·Ed25519 canonical_payload签名·24h窗口强制更新/阻断·事件JSON文件一致性校验·三路备份推送·7种退出码(0~6)·7子命令·`healthcheck/control-plane/updater/backup-push/sign/verify/self-test` |
| DNA校验,DNA验证,启动校验,DNA启动,DNA启动前检查,dna_validate,.env.example,DNA治理,DNA固本,必需键,禁止键,DNA宪法,DNA护栏,主权,域值,白名单 | `python3 bin/dna_validate.py` | UID9622 DNA启动校验器v2.0·不给AI自由发挥·48必需键·5禁止键(ALLOW_LEGAL/MEDICAL_DIAG/MEDICAL_TREAT/FINANCIAL_ADVICE/FINANCIAL_PREDICTION强制=false)·域值白名单(RESTRICTED/STRICT)·主权声明(DNA_NATIONAL_POSITION_CN+DNA_TAIWAN_IS_CHINA)·三分类详细报告·零外部依赖·可import·`.env.example`结构契约对外分发 |
| 镜像指数,mirror_index,智能是使用者的镜像,技术精英,边界尊重,系统自检,代码倾向,优化绕行,mirror index,边界尊重优先,平衡态,技术精英模式,哲学层检测,MirrorIndex,安全自检,价值观检测 | `python3 bin/lh_mirror_index.py` | UID9622镜像指数扫描器v1.0·智能是使用者的镜像·哲学→工程确定性·11技术精英特征(eval/exec/shell/裸except/反射/动态导入/绕行注释等)·11边界尊重特征(拒绝/降级/权限/DNA配置/熔断/审计/通知等)·0~100指数·三色判定(🟢70+边界尊重🟡45-70平衡🔴<45技术精英)·3退出码·零依赖·可import·CI集成 |
| 监管防火墙,regulatory_firewall,防火墙,DNA防火墙,权限检查,领域限制,高风险域,FailSafe,审计日志,拒绝模板,L0-L4,能力状态,LDAP权限,OAuth权限,批量检查,DNA导出,regulatory firewall,system dna,放行检查,权限后端 | `python3 bin/lh_regulatory_firewall.py` | UID9622监管防火墙v2.0·SYSTEM DNA联动·七步Fail-Safe链(DNA完整性→能力状态→权限L0-L4→专业匹配→专家审批→领域限制)·可插拔权限后端(default/LDAP/OAuth)·审计日志JSON Lines格式·DNA导出/比对·batch批量检查·三色审计标记·P72熔断联动·--test/--batch/--mode prod·零依赖·可import |
| **统一中枢**,unified_brain,中枢,大脑,引擎调度,注册表,引擎发现,全项目,智能路由,2,723,引擎归集,引擎集成,brain,unified brain,orchestrator,所有引擎,一键调度,状态面板,去重,冗余,引擎搜索,unified,orchestrator | `lh brain` 或 `python3 bin/lh_unified_brain.py` | UID9622统一中枢v1.0·全项目2,723引擎统一调度·自动注册表·智能路由(find/run/route)·状态全景面板·健康检查·多版本冗余检测(675组)·交互式控制台·Python可import·find/status/health/dupes/api/route/scan子命令 |
| **引擎注册表**,engine_registry,注册表,扫描,分类,registry,py分类,脚本分类 | `python3 bin/lh_engine_registry.py` | UID9622引擎注册表v1.0·自动发现全项目py脚本·按功能自动分类(15类)·版本去重检测·DNA元数据提取·JSON注册表输出·scan/stats/find/dupes/export子命令·数据驱动统一集成 |
| 三才算法,三才,三才引擎,three powers,san cai,初心递进,量子纠缠,四层锚,三才循环 | `python3 bin/san_cai_v2.py --interactive` | 三才算法P0-ETERNAL v2.0·四层定锚(永恒/价值/行为/执行)·1→2→3循环生态·量子纠缠态(1⊗1>2)·初心递进(干净→用心→在乎→认真→有爱)·三色审计·DNA追溯·10子命令·卦象映射·`--interactive/--module/--user/--run/--entangle/--cycle/--heart/--status/--report/--json` |
| CNSH iOS测试,cnsh ios,cns解释器,cns脚本,CNSH interactive,cnsh_ios_test | `python3 bin/cnsh_ios_test.py --interactive` | CNSH解释器Python本地测试版·设/打印/理解/执行·变量环境·iOS Swift同逻辑·交互/文件/代码/AI·`--interactive/--code/--file/--ai/--json` |
| 代码审计,漏洞扫描 | `python3 bin/code_audit.py` | 代码安全审计 |
| 生成DNA,DNA追溯码,DNA生成,dna,dna generator,DNA追溯,干支DNA,卦象DNA | `python3 bin/lh_dna_generator.py doc --module 模块名 --action 动作 --version 1.0` | DNA生成·v2.0双维度(文档/人物)·精确干支四柱·六十四卦映射·梅花易数起卦·HMAC双签名·SQLite注册表·族谱继承·内容指纹绑定·篡改检测·搜索`lh_dna_generator.py lookup/search/stats/history/family` |
| 健康检查,网站检查,监控 | `python3 bin/lh.py` | 网站可用性监控 |
| 做3D,3D,图生三维 | `python3 bin/lh_3d_pipeline.py` | 图生三维管线 |
| 对齐,对齐检查,对齐复盘,补DNA,补签名,代码对齐,对齐修复 | `lh --align check` 或 `lh --align fix` 或 `lh --align daemon` | 对齐闭环·check检查/fix修复/daemon守护/dry-run预览/status状态 |
| 反诈,防骗,弯弯绕绕,套路检测 | `python3 bin/lh_anti_fraud_detector.py` | 14维度·话术分析·反制话术 |
| 防篡改,篡改检测 | `python3 bin/lh_anti_tamper.py` | 文件一致性防篡改扫描 |
| Git推送,推远端,全量推送 | `python3 bin/lh_auto_cannon.py` | GitHub+Gitee+GitCode三端推送 |
| 批量签章,全量签名 | `python3 bin/lh_batch_confirm_sign.py` | 批量GPG签章确认 |
| 浏览史官,采集历史,浏览器史官,历史采集 | `python3 bin/lh_browser.py` | 四道防线·设备金库·导出签名 |
| 浏览史官,采集历史,浏览器史官,历史采集 | `python3 bin/lh_browser_historian.py` | 四道防线·设备金库·导出签名 |
| 民间防御,水军识别,样本收集 | `python3 bin/lh_civil_defense_samples.py` | 正向/负向自动分类收集 |
| CNSH编译,编译CNSH | `python3 bin/lh_cnsh_compiler.py` | CNSH→Python四阶段编译 |
| 代码审计,漏洞扫描 | `python3 bin/lh_code_audit_cli.py` | 代码安全审计 |
| 德本审计,五问,离火运 | `python3 bin/lh_deben_audit.py` | 德本五问·审计扫描 |
| 数字根,五行数字,369 | `python3 bin/lh_digital_root.py` | 计算数字根·五行映射·369熔断 |
| 拉取数据,训练数据,数据下载 | `python3 bin/lh_download_v40_bases.py` | 80中国源+65国际 |
| 拉取数据,训练数据,数据下载 | `python3 bin/lh_download_v40_bases_modelscope.py` | 80中国源+65国际 |
| 全系统审计,系统审计,安全审计 | `python3 bin/lh_full_system_audit.py` | 全系统安全扫描 |
| GPG签名,签名,签章 | `python3 bin/lh_gpg_sign.py` | GPG分离签名·扫描验证 |
| 鲲鹏健康,Bark告警,服务器监控 | `python3 bin/lh_health_check.py` | 鲲鹏健康检查·Bark推送 |
| 鲲鹏健康,Bark告警,服务器监控 | `python3 bin/lh_health_check_quick.py` | 鲲鹏健康检查·Bark推送 |
| 投喂宝宝,内容优化,宝宝提炼,内容提炼,温柔整理 | `python3 bin/lh_feed_baby.py` | 投喂宝宝优化引擎·P02宝宝+P05三色审计·核心要点提取·深度分析·行动清单·P72熔断 |
| CNSH翻译,代码翻译,多语言翻译,cnsh translator,代码转换 | `python3 bin/lh_cnsh_translator.py -f 文件.py` 或 `--interactive` | CNSH通用翻译引擎 v1.0·P05三色审计+P72龙盾熔断·多语言→CNSH IR·AI代码鉴定·来源追溯·CNSH生成+反向生成·压缩存储·`--interactive/-c/-f/-m/--json` |
| 数字孪生,素字卵神,孪生体,意识复制,意识同步,推演预测,twin,digital twin | `python3 bin/lh_digital_twin.py --interactive` | 素字卵神数字孪生引擎 v1.0·8维人格建模·行为记录·决策追踪·推演预测·实时同步·快照恢复·三色审计·--interactive/--status/--audit/--report/--simulate/--record/--decide/--snapshot/--sync-start/--json |
| 收口测试,跑测试,入口测试,全链路测试,熔断测试,测试执行器,test runner,entry test | `python3 bin/lh_entry_test_runner.py` | 龍魂收口测试执行器 v1.0·54用例·8步全链路(DNA→身份→意图→路径→执行→审计→签章→归档)·L0-L3四级熔断·端到端10场景·断点续跑·JSON报告·审计报告·--block/--tc/--json-report/--resume/--summary |
| CNSH编辑,中文纠错,标点纠错,文本纠错,编辑器,cnsh editor,翻译避坑,纠错引擎 | `python3 bin/cnsh_editor.py` | CNSH中文编辑器 v2.0·370条纠错规则·12大类(标点/空格/标题/列表/编号/结构文本/Markdown/清洗/安全/翻译避坑/CNSH语法/智能修复)·Notion集成·安全过滤(XSS/SQL/路径)·交互模式·`-f -o --interactive --export-rules --security --filter --json` |
| 动态目标,自适应规划,目标推进,闭环执行,规划和执行,任务自动化推进,项目规划,目标驱动,dynamic goal,auto plan,自适应规划引擎 | `python3 bin/lh_dynamic_goal.py --interactive` 或 `--goal "目标"` | 动态目标推进协议 v1.0·目标驱动+自适应规划+闭环执行·自然语言目标解析·自动路径生成·失败自动重规划·状态持久化·DNA追溯·交互/文件/JSON/NL命令行·`--interactive/--goal/--constraints/--resources/--file/--status/--json/--execute` |
| 七维推演,人机共生,脑机接口,意识上传,human machine symbiosis,sandbox推演,战略推演,七维推演v2,拉普拉斯妖,向善公式,置信度推演 | `python3 bin/lh_seven_dimension_engine.py --run`(v1) 或 `python3 bin/lh_seven_dimension_engine_v2.py --interactive`(v2) | 七维推演引擎 v1.0+v2.0·v2.0五大升级(置信度·学习循环·历史映射·四维沙盘·向善公式)·P01战略+P06数字根+P12底线+P05审计+P72熔断·太极起卦(64卦)·7维加权·`--interactive/--run/--question/--history/--cnsh/--sandbox/--json` |
| 权重算法,决策推演,易经权重,护弱 | `python3 bin/lh_weight_algorithm.py` | 易经八卦权重·甲骨文护弱·数学大师最优解·三色审计·输出契约 |
| 三重审计,审计门槛,三色审计门槛,三重检测,闸门 | `python3 bin/lh_triple_audit_gate.py` | 三色审计第一道门槛·规则检测(红线/黄线/绿线)+虚伪编译(说满词/依据/表达)+数据守护(DNA/时间戳/操作人/来源)·串行联动·审计日志 |
| 三色审计,三色判定,审计判定,审计引擎,审计裁决,审计判决,three color audit,audit verdict | `python3 bin/lh_three_color_audit.py audit --object "被审计对象" --type 类型` | 三色审计判定引擎 v2.0·P05上帝之眼核心·加权多因子判定·四级熔断(L0-L3)·十闸口联动(GATE-01~10)·SI主权指数·德本五问预审·防篡改验证(HMAC+SHA256)·P05/P06/P72联动·审计链append-only·交互控制台·`lh_three_color_audit.py audit/stats/history/chain-verify/verify/interactive` |
| 三层监督,钩子系统,监管执行,执行前检查,三层守卫,three layer guard,hook system | `python3 bin/lh_three_layer_guard.py --action "动作" --risk P1` | 三层监督+钩子系统 v1.0·10钩子·3层(决策/执行/行为)·6人格联动(P12/P00/P05/P06/P04/P07/P72/P03)·DNA追溯·确认码·三色审计桥·P0自动熔断·暂停/恢复·历史·JSON输出·`--action/--risk/--history/--status/--pause/--resume/--json` |
| 意念交流,意图理解,意念引擎,知识库搜索,五库搜索,intent engine,mind link,semantic parse | `python3 bin/lh_intent_engine.py "查询内容"` 或 `--interactive` | 意念交流引擎 v3.0·10阶段(语义→追溯→知识检索→人格调度→响应→监督→ROM固化→归档→学习→零延迟)·5大知识库太极(乾☰震☳坤☷坎☵巽☴)·甲骨文ROM(10000次推演·0.1ms命中)·P72一票否决熔断·P05三色审计·DNA追溯·确认码·`--interactive/--search/--feed/--stats/--json` |
| 投喂宝宝,内容优化,宝宝提炼,内容提炼,温柔整理,feed baby,内容精华,baby optimize | `python3 bin/lh_feed_baby.py -c "内容"` 或 `--interactive` | 投喂宝宝优化引擎 v1.0·P02宝宝(温柔表达)+P05三色审计·核心要点提取(3-5)·即动建议(3)·重要提醒(3)·深度分析(可靠/需验证/优先级)·行动清单(本周/下月/长期)·宝宝寄语·P72一票否决熔断·DNA追溯·确认码·`--interactive/-c/-f/--json` |
| 公正总裁,裁决,公正裁决 | `python3 bin/lh_judge.py` | 公正裁决·三色审计 |
| 公正总裁,裁决,公正裁决 | `python3 bin/lh_judge_api.py` | 公正裁决·三色审计 |
| 知识中枢,知识检索 | `python3 bin/lh_knowledge_algo_db.py` | 知识中枢服务 :8766 |
| 知识中枢,知识检索 | `python3 bin/lh_knowledge_crawler.py` | 知识中枢服务 :8766 |
| 知识中枢,知识检索 | `python3 bin/lh_knowledge_hub_api.py` | 知识中枢服务 :8766 |
| 知识中枢,知识检索 | `python3 bin/lh_knowledge_semantic_trigger.py` | 知识中枢服务 :8766 |
| 链接解析,URL解析,解析链接 | `python3 bin/lh_link_parser.py` | 解析URL·提取元数据/正文/链接 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v4.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v402.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v403.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v404.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v405.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v406.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v407.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v408.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v409.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v41.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v410.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v411.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v411_bind.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v412.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v413.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v414.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v415.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v416.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v417.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v418.py` | MLX LoRA rank=16 |
| 训练模型,LoRA训练,微调 | `python3 bin/lh_lora_trainer_v419.py` | MLX LoRA rank=16 |
| UID9622中枢,系统中枢,铁律验证,人格调度,UID9622 | `python3 bin/lh_uid9622_central.py` | 铁律验证·人格调度·任务执行·快速指令·知识检索 |
| LU压缩,压缩引擎,短码召回,时间胶囊 | `python3 bin/lh_lu_compressor.py` | 12步压缩链·短码召回·时间胶囊·本地回填 |
| LU运行时,跨窗口治理,窗口管理,lu runtime | `python3 bin/lh_lu_runtime.py <子命令>` | 🐉 LU跨窗口语义治理运行时 v3.0·窗口DNA·快照恢复·审计链·分支·污染检测·意图解析·13子命令 |
| 记忆加载,加载记忆 | `python3 bin/lh_memory.py` | 焊死记忆加载 |
| 记忆加载,加载记忆 | `python3 bin/lh_memory_load.py` | 焊死记忆加载 |
| 人格编排,人格调度 | `python3 bin/lh_persona_orchestrator.py` | 20人格任务分发 |
| 人格报告,人格统计 | `python3 bin/lh_persona_report.py` | 人格活跃度/贡献统计 |
| 启动全部,全部启动,启动服务 | `python3 bin/lh_persona_start_all.py` | 一键启动所有52个服务 |
| SafeAI,安全AI,上下文安全 | `python3 bin/lh_safeai.py` | 意图分类·七因子审计·分层熔断 |
| 搜索,搜索引擎,查资料 | `python3 bin/lh_search_engine.py` | Bing搜→缓存→审计 :9631 |
| 自愈,修复,自动修复 | `python3 bin/lh_self_heal.py` | 自助修复系统问题 |
| 序列执行,流水线审计 | `python3 bin/lh_seq.py` | SafeAI→KFPP→CSDN→公正总裁 |
| 源头校验,数据校验,入站检查 | `python3 bin/lh_source_vetting.py` | 五问·80分门槛·硬性拒绝 |
| 通心译,翻译,文化翻译 | `python3 bin/lh_tongxinyi_translator.py` | 文化锚点保护翻译·SQLite记忆 |
| 通心译结构,结构解析,映射验证 | `python3 bin/lh_tongxinyi_structure.py` | 解析·验证·生成JSON/报告·三层映射完整性 |
| 真声配音,配音,语音合成 | `python3 bin/lh_tts_xtts.py` | XTTS v2真声配音 |
| 做视频,视频制作,视频工坊 | `python3 bin/lh_video_studio.py` | 文本→配音+AI图示+字幕 v3.0 |
| 做视频,视频制作,视频工坊 | `python3 bin/lh_video_studio_v5.py` | 文本→配音+AI图示+字幕 v3.0 |
| 健康检查,网站检查,监控 | `python3 bin/lh_web_health_check.py` | 网站可用性监控 |
| 五行计算,五行分析,五行 | `python3 bin/lh_wuxing_core.py` | 五行强度·补益分析·对冲指数 |
| 部署DeepSeek,DeepSeek部署 | `bash bin/deploy_deepseek.sh` | 一键部署DeepSeek-V3 |
| 安装,系统安装 | `bash bin/install.sh` | 龍魂系统安装向导 |
| 运行CNSH,CNSH执行 | `bash bin/lh_cnsh_run.sh` | CNSH脚本解释执行 |
| 爬虫伦理,爬虫检查 | `bash bin/lh_crawler_ethics.sh` | 6项爬虫伦理检查 |
| 启动全部,全部启动,启动服务 | `bash bin/longhun_system_start_all.sh` | 一键启动所有52个服务 |
| 启动全部,全部启动,启动服务 | `bash bin/start_all.sh` | 一键启动所有52个服务 |
| 知识中枢,知识检索 | `python3 engines/lh_knowledge_distiller.py` | 知识中枢服务 :8766 |
| SafeAI,安全AI,上下文安全 | `python3 engines/lh_safeai_engine.py` | 意图分类·七因子审计·分层熔断 |
| 序列执行,流水线审计 | `python3 engines/lh_sequence_executor.py` | SafeAI→KFPP→CSDN→公正总裁 |
| 璇玑,推演,记忆溯源 | `python3 engines/lh_xuanji_engine.py` | 记忆溯源推演·四象闭环 |
| 一键部署,部署 | `bash deploy/deploy-now.sh` | 一键部署全部服务 |
| 同步鲲鹏,同步服务器,代码同步 | `bash deploy/sync-to-kunpeng.sh` | 同步代码到鲲鹏119.13.90.27 |
| 健康检查,网站检查,监控 | `bash deploy/scripts/health_check.sh` | 网站可用性监控 |
| 监控配置,systemd配置 | `bash deploy/scripts/monitor_setup.sh` | systemd+cron+告警 |

---

## 📦 完整脚本清单 (798 个)

> 以下脚本可通过文件名模糊匹配。AI 看到文件名即可直接执行。

### 🐉 lh_ 工具脚本 (621 个)

| 触发词 | 命令 | 说明 |
|:---|:---|:---|
| absorb directories | `python3 bin/lh_absorb_directories.py` | 将分散目录的脚本/文档全部按四层命名法吸收统一 |
| absorbed 面向护童的人性优先人工 | `python3 bin/lh_absorbed_面向护童的人性优先人工智能系统.py` | 龍魂吸收产出 · 可执行代码桩 |
| absorbed 龍魂 AI国标数据统计 | `python3 bin/lh_absorbed_龍魂_AI国标数据统计与能效实战技术文档_五行河图洛书天干地.py` | 龍魂吸收产出 · 可执行代码桩 |
| activation api | `python3 bin/lh_activation_api.py` | 龍魂激活经济舱 REST API |
| active observation | `python3 bin/lh_active_observation.py` | ================================================== |
| adaptive threshold | `python3 bin/lh_adaptive_threshold.py` | ╔═════════════════════════════════════════════════ |
| adaptive tuner | `python3 bin/lh_adaptive_tuner.py` | 路径：bin/lh_adaptive_tuner.py |
| adversarial pipeline | `python3 bin/lh_adversarial_pipeline.py` | 红队发现新攻击 → 自动变体生成 → Ollama 真实验证 → 自动追加 → 再训练告警 |
| agent kunpeng | `python3 bin/lh_agent_kunpeng.py` | 龍芯·鲲鹏共生体调度中枢 v1.1 |
| agent trainer | `python3 bin/lh_agent_trainer.py` | 创建者: 诸葛鑫（UID9622） |
| ai anti hype | `python3 bin/lh_ai_anti_hype.py` | ╔═════════════════════════════════════════════════ |
| ai gateway | `python3 bin/lh_ai_gateway.py` | 龍魂统一AI网关 v1.0 |
| ai governance | `python3 bin/lh_ai_governance.py` | 龍魂·AI治理体系 v2.0 — 立法+裁判+反懒惰+连续性+公开发布 |
| algo audit validator | `python3 bin/lh_algo_audit_validator.py` | 龍魂系统 · 算法审计与透明验证模块 v1.0 |
| ant colony daemon | `python3 bin/lh_ant_colony_daemon.py` | 龙魂蚁群守护进程 v2.0 · Ant Colony Daemon |
| ant colony orchestra | `python3 bin/lh_ant_colony_orchestrator.py` | ╔═════════════════════════════════════════════════ |
| ant colony router | `python3 bin/lh_ant_colony_router.py` | 龍魂蚁群触角 · 模型路由引擎 v1.0 |
| antenna 8gate api | `python3 bin/lh_antenna_8gate_api.py` | 龍魂·ANTENNA-8GATE API 服务 v2.0 |
| anti algorithmic har | `python3 bin/lh_anti_algorithmic_harvest.py` | 龍魂·反算法收割审计引擎  v1.0 |
| anti counterfeit | `python3 bin/lh_anti_counterfeit.py` | ╔═════════════════════════════════════════════════ |
| anxiety detector | `python3 bin/lh_anxiety_detector.py` | ╔═════════════════════════════════════════════════ |
| api full reference v | `python3 bin/lh_api_full_reference_v1.0.py` | 龙魂系统 API接口完整实现 v1.0 |
| api guard | `python3 bin/lh_api_guard.py` | ╔═════════════════════════════════════════════════ |
| api taiji ant engine | `python3 bin/lh_api_taiji_ant_engine.py` | 龍魂 · 太极蚁群API命名与路由引擎 v1.0 |
| api validate all | `python3 bin/lh_api_validate_all.py` | 龍魂 · 全量API校验脚本 v1.0 |
| asr api | `python3 bin/lh_asr_api.py` | 路径：bin/lh_asr_api.py |
| asr engine | `python3 bin/lh_asr_engine.py` | 龍魂 ASR 引擎 — 本地 whisper 兜底方案。 |
| audio parser | `python3 bin/lh_audio_parser.py` | 四步处理管线: |
| audio watermark | `python3 bin/lh_audio_watermark.py` | 给音频文件注入龍魂 DNA 追溯码。 |
| audit as a service | `python3 bin/lh_audit_as_a_service.py` | ══════════════════════════════════════════════════ |
| audit as a service a | `python3 bin/lh_audit_as_a_service_api.py` | ╔═════════════════════════════════════════════════ |
| audit batch processo | `python3 bin/lh_audit_batch_processor.py` | 龍魂·审计日志批量处理器 v2.0 (幂等+断点续传) |
| audit battle hub | `python3 bin/lh_audit_battle_hub.py` | 龍魂审计对抗中枢 · 左右互搏 + 红蓝对抗 + 数学建模 + 漏洞扫描 |
| audit hook | `python3 bin/lh_audit_hook.py` | 路径：bin/lh_audit_hook.py |
| audit package | `python3 bin/lh_audit_package.py` | 龍魂·单人闭环审计打包器 v1.0 |
| audit pricing v2 | `python3 bin/lh_audit_pricing_v2.py` | 龍魂审计定价引擎 v2.0 + 支付网关 + 投资池 |
| audit sheet trigger | `python3 bin/lh_audit_sheet_trigger.py` | ║ |
| auto distill | `python3 bin/lh_auto_distill.py` | 龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-AUTO-DISTILL-v1.0 |
| auto heal | `python3 bin/lh_auto_heal.py` | 龍魂自动审计自愈引擎 v1.0 |
| auto learner | `python3 bin/lh_auto_learner.py` | 龍魂 · 自动学习引擎 v1.0 |
| rl feedback,强化学习,反馈循环,奖惩判定,学习循环,权重调整,AB测试 | `python3 bin/lh_rl_feedback_loop.py` | 强化学习反馈循环引擎·10模块(数据收集+模式识别+奖惩+权重更新+全局同步+安全边界+时间衰减+学习报告+A/B测试+终止条件)·SQLite记忆库 |
| security audit,安全检查,风险评估,安全审计,漏洞扫描,异常检测,三色审计联动,安全评分 | `python3 bin/lh_security_auditor.py` | 安全风险评估引擎·8模块(风险评估/安全检查/审计日志/双因素认证/异常行为检测/告警推送/白黑名单/三色审计联动)·append-only审计·安全签名 |
| universal complete,万能补全,模糊处理,量子分类,属性补全,自动挂载,强制联通,永恒锚点 | `python3 bin/lh_universal_completer.py` | 万能补全引擎·6步流水线(判断→对位→补全→模糊处理→强制联通→自动挂载)·7量子类型·5系统挂载·8属性补全·3方案优选·交互模式 |
| doc generator,文档生成,系统文档,文档模板,批量文档,标准化文档,文档生成器 | `python3 bin/lh_doc_generator.py` | 系统文档生成器·交互式+参数+批量三种模式·Markdown/JSON/HTML输出·DNA/确认码自动生成·人格自动推荐·8章节标准模板 |
| community qa,社区问答,技术问答,问题回答,回答模板,QA生成 | `python3 bin/lh_community_qa.py` | 社区问答回答生成器·交互式+命令行+JSON三种输出·9类问题自动分类·多方案对比·风险等级标注·合规检查·历史记录·剪贴板复制 |
| need translator,需求翻译,情绪翻译,需求理解,翻译引擎,宝宝翻译 | `python3 bin/lh_need_translator.py` | 需求翻译引擎·情绪化表达→系统需求+方案·13条映射库·5人格联动(宝宝/诸葛亮/文心/鲁班)·交互式+命令行+JSON·历史记录·铁律焊死(不问休息/不评判/不照顾) |
| adaptive guardian,自适应守护,边界守护,防篡改,防剽窃,灾难预判,免疫系统 | `python3 bin/lh_adaptive_guardian.py` | 自适应学习边界守护引擎·分层判断(可变/铁律/灰色)·身份验证(4级)·防剽窃DNA追溯·灾难预判(4类预警)·三审投票(加权)·奖惩积分+拉黑·交互式+命令行+JSON·P0焊死 |
| quantum arbitrator,量子仲裁,自动仲裁,量子唤醒,模板选择,唯一唤醒 | `python3 bin/lh_quantum_arbitrator.py` | 量子自动仲裁引擎·信号识别(4类)·候选池筛选·五维评分(类型权重+风险匹配+人格适配+历史稳定性-算力惩罚)·唯一唤醒(硬约束/安全阈值5分/打破平局)·7量子模板·状态回写持久化·IndexHub追溯·交互式+命令行+JSON |
| ultimate feed,终极投喂,投喂引擎,减法引擎,内容去重,内容分类,投喂优化 | `python3 bin/lh_ultimate_feed.py` | 终极投喂引擎·做减法不做加法·8内容类型自动分类(文档/代码/知识库/规则/协议/配置/对话/创意)·语义指纹去重·五维质量评分·合并/覆盖/冻结/创意池·执行流对齐(6命中类型)·9页共识标签体系·页面结构自动生成(8模板)·文件持久化(~/.longhun/feed/)·目录批量导入·导出/按类型查询/按标签查询·交互式+命令行+JSON |
| auto shouheng | `python3 bin/lh_auto_shouheng.py` | - C1/C2/C3 三档收口自动检测与渲染 |
| auto sync | `python3 bin/lh_auto_sync.py` | 龍芯⚡️2026-04-05-MVP自动化脚本-v1.0 |
| autoflow | `python3 bin/lh_autoflow.py` | 路径：bin/lh_autoflow.py |
| backup automation | `python3 bin/lh_backup_automation.py` | 1. 增量备份 - 仅备份变更文件 |
| bagua | `python3 bin/lh_bagua.py` | 龍魂八卦决策调度器 · LongHun Bagua Decision Scheduler v1.0 |
| bagua param regressi | `python3 bin/lh_bagua_param_regression.py` | 龍魂 · 八卦阵参数回归框架 v1.0 |
| bark dispatcher | `python3 bin/lh_bark_dispatcher.py` | ╔═════════════════════════════════════════════════ |
| base model train | `python3 bin/lh_base_model_train.py` | 龍魂 · 底座模型训练引擎 v4.0 |
| base trace collector | `python3 bin/lh_base_trace_collector.py` | 龍魂·底座痕迹采集引擎 v2.0 — 四道防线版 |
| behavior collector | `python3 bin/lh_behavior_collector.py` | 龍魂·行为采集器 v1.0 |
| behavioral benchmark | `python3 bin/lh_behavioral_benchmark.py` | ① AI(Claude/GPT/Gemini) vs 真人 书写区分                 |
| biometric health | `python3 bin/lh_biometric_health.py` | ╔═════════════════════════════════════════════════ |
| bootstrap train | `python3 bin/lh_bootstrap_train.py` | 龍魂 · 共生体数据自举训练集成 v1.0 |
| braket persona engin | `python3 bin/lh_braket_persona_engine.py` | Bra-Ket量子人格引擎 v1.0 · 多人格量子协作系统 |
| browser daemon | `python3 bin/lh_browser_daemon.py` | 龍魂浏览器操作助手 · 本地守护进程 v1.0 |
| browser miner | `python3 bin/lh_browser_miner.py` | 龍魂 · 浏览器历史矿工 v1.0 |
| build prompt library | `python3 bin/lh_build_prompt_library.py` | 龍魂·Notion 提示词库构建器 v2.0 (精筛 + 三分库) |
| build training corpu | `python3 bin/lh_build_training_corpus.py` | 从系统自身哲学/宪法/协议中提取精华，构建训练语料 |
| cache cleaner | `python3 bin/lh_cache_cleaner.py` | 龍魂系统 · 智能缓存清理引擎 v1.0 |
| calendar sync | `python3 bin/lh_calendar_sync.py` | • 任务自动写入 iCloud 日历 |
| chat importer | `python3 bin/lh_chat_importer.py` | 龍魂 · AI对话导入器 v2.0 |
| check alignment | `python3 bin/lh_check_alignment.py` | 龍魂·底线二：路径对齐 检测引擎 v1.0 |
| check contributor | `python3 bin/lh_check_contributor.py` | 龍魂·底线三：不让付出者寒心 检测引擎 v1.0 |
| check core | `python3 bin/lh_check_core.py` | 龍魂·底线五：外化内不化 检测引擎 v1.0 |
| check sovereignty | `python3 bin/lh_check_sovereignty.py` | 龍魂·底线四：信息主权不可让渡 检测引擎 v1.0 |
| check virtue | `python3 bin/lh_check_virtue.py` | 龍魂·底线一：德在技术前 检测引擎 v1.0 |
| chip gate | `python3 bin/lh_chip_gate.py` | 龍魂芯片门禁 · 功能分层控制器 v1.0 |
| circuit breaker | `python3 bin/lh_circuit_breaker.py` | 龍魂 · 观澜 — 断路器 v1.0 |
| claude bridge | `python3 bin/lh_claude_bridge.py` | ║ |
| cli | `python3 bin/lh_cli.py` | ╔═════════════════════════════════════════════════ |
| closed space validat | `python3 bin/lh_closed_space_validator.py` | 龍魂系统 · 封闭空间·三生三世 数学建模验证模块 v1.0 |
| absorb | `python3 bin/lh_cnsh_absorb.py` | ╔═════════════════════════════════════════════════ |
| cnsh runtime,agentos,sovereign runtime,memory governance,sandbox,snapshot restore | `python3 bin/lh_cnsh_runtime.py <subcmd>` | CNSH Local Sovereign AgentOS v2.0·9-layer memory·snapshot/restore·sandbox·agent lifecycle·audit·evolution·CNSH compile/absorb bridge·12 modules·status/snapshot/memory/sandbox/agent/audit/compile/absorb/daily/evolve |
| baby hub | `python3 bin/lh_cnsh_baby_hub.py` | 路径：bin/lh_cnsh_baby_hub.py |
| code audit | `python3 bin/lh_cnsh_code_audit.py` | 路径：bin/lh_cnsh_code_audit.py |
| content pipe | `python3 bin/lh_cnsh_content_pipe.py` | 路径：bin/lh_cnsh_content_pipe.py |
| cron | `python3 bin/lh_cnsh_cron.py` | 路径：bin/lh_cnsh_cron.py |
| dict | `python3 bin/lh_cnsh_dict.py` | CNSH标准词典 · 查询工具 |
| dict export | `python3 bin/lh_cnsh_dict_export.py` | CNSH标准词典 · CSV生成器 |
| dir audit | `python3 bin/lh_cnsh_dir_audit.py` | 路径：bin/lh_cnsh_dir_audit.py |
| eco regulator | `python3 bin/lh_cnsh_eco_regulator.py` | 路径：bin/lh_cnsh_eco_regulator.py |
| gatekeeper | `python3 bin/lh_cnsh_gatekeeper.py` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| knowledge base | `python3 bin/lh_cnsh_knowledge_base.py` | 路径：bin/lh_cnsh_knowledge_base.py |
| neural brain router | `python3 bin/lh_cnsh_neural_brain_router.py` | ╔═════════════════════════════════════════════════ |
| router baby | `python3 bin/lh_cnsh_router_baby.py` | 听懂老百姓的话，自动拆碎意图，按需调用国密/加密/语义/公式/人格/文章/审计等模板 |
| router v2 | `python3 bin/lh_cnsh_router_v2.py` | CNSH 一句话路由器 v2.0｜Route = f(Intent, Context, DNA) |
| rule db | `python3 bin/lh_cnsh_rule_db.py` | 路径：bin/lh_cnsh_rule_db.py |
| self check | `python3 bin/lh_cnsh_self_check.py` | 路径：bin/lh_cnsh_self_check.py |
| shield | `python3 bin/lh_cnsh_shield.py` | CNSH 龍魂护盾 v1.0 |
| shouheng summary | `python3 bin/lh_cnsh_shouheng_summary.py` | 路径：bin/lh_cnsh_shouheng_summary.py |
| cnshtranslator valid | `python3 bin/lh_cnshtranslator_validator.py` | 龍魂系统 · CNSH通用翻译引擎 数学建模验证模块 v1.0 |
| cnsh translator engine | `python3 bin/lh_cnsh_translator.py` | CNSH通用翻译引擎 v1.0·P05三色审计+P72龙盾熔断·Multi-lang→CNSH IR·AI code detection·source tracing·CNSH generation+reverse·compressed storage·`--interactive/-c/-f/-m/--json` |
| seven dimension v2 | `python3 bin/lh_seven_dimension_engine_v2.py` | Seven-dim engine v2.0·5 upgrades(confidence·learning·history map·4D sandbox·goodness formula)·P01+P06+P12+P05+P72·Taiji 64 hexagrams·7-dim weighted·`--interactive/--run/--question/--history/--cnsh/--sandbox/--json` |
| code guardian | `python3 bin/lh_code_guardian.py` | 1. 扫描全项目 Python 文件，检测 basedpyright 类型注解缺失 |
| command runner | `python3 bin/lh_command_runner.py` | 解析 COMMAND_INDEX.md，根据用户自然语言意图匹配并执行命令。 |
| commander | `python3 bin/lh_commander.py` | ══════════════════════════════════════════════════ |
| comment integrity va | `python3 bin/lh_comment_integrity_validator.py` | 龍魂系统 · 评论水军显化与反操纵验证模块 v1.0 |
| compression card | `python3 bin/lh_compression_card.py` | -*- coding: utf-8 -*- |
| compute gate control | `python3 bin/lh_compute_gate_controller.py` | 龍魂·算力分离闸门控制器 — 连接同心锁防火墙与无状态API的物理闸门。 |
| compute proof | `python3 bin/lh_compute_proof.py` | 龍魂·算力证明引擎 — 验证鲲鹏签名，归档到本地保险柜。 |
| confirm seal | `python3 bin/lh_confirm_seal.py` | 扫描指定目录，为缺少确认码的文件追加 CONFIRM 签名（按文件类型自动选择注释格式）。 |
| connectivity schedul | `python3 bin/lh_connectivity_scheduler.py` | ================================ |
| convert model | `python3 bin/lh_convert_model.py` | 龍魂·底模转换脚本 — HF→MLX 离线模式 |
| core algo lib | `python3 bin/lh_core_algo_lib.py` | ╔═════════════════════════════════════════════════ |
| core template | `python3 bin/lh_core_template.py` | ═══════════════════════════════════════════ |
| corpus builder | `python3 bin/lh_corpus_builder.py` | 龍魂·训练语料构建器 — 从 data/training/ 全量抽取文本 |
| cross module awarene | `python3 bin/lh_cross_module_awareness.py` | 龍魂联动感知引擎 · Cross-Module Awareness Engine |
| cross module router | `python3 bin/lh_cross_module_router.py` | 龍魂系统 · 跨模块路由回调总线 v1.0 |
| crystal recognition | `python3 bin/lh_crystal_recognition.py` | 龍魂·水晶识别知识库 v2.0 · 阻断日志自动入库+智能标签+现实打脸报告 |
| cs learning engine | `python3 bin/lh_cs_learning_engine.py` | ╔═════════════════════════════════════════════════ |
| csdn full scraper | `python3 bin/lh_csdn_full_scraper.py` | 1. 抓取 blog.csdn.net/UID9622 全部文章（239篇） |
| csdn ref | `python3 bin/lh_csdn_ref.py` | 龍魂 · CSDN 外部引用工具 v1.0 |
| csdn to train | `python3 bin/lh_csdn_to_train.py` | 龍魂 · CSDN 17篇监管审计系列 → train.jsonl 语料生成 |
| ctl | `python3 bin/lh_ctl.py` | 创建者: 诸葛鑫 (UID9622) |
| ctl config | `python3 bin/lh_ctl_config.py` | 创建者: 诸葛鑫 (UID9622) |
| ctl scheduler | `python3 bin/lh_ctl_scheduler.py` | 创建者: 诸葛鑫 (UID9622) |
| ctl web | `python3 bin/lh_ctl_web.py` | 创建者: 诸葛鑫 (UID9622) |
| cultural dna | `python3 bin/lh_cultural_dna.py` | 龍魂·文化DNA引擎 v2.0 — 核心文化基因注入+三层保护 |
| da align table | `python3 bin/lh_da_align_table.py` | 设计哲学: |
| daily logger | `python3 bin/lh_daily_logger.py` | 龍芯⚡️2026-07-25-DAILY-LOGGER-v1.0 |
| daodejing anchor | `python3 bin/lh_daodejing_anchor.py` | 龍魂系统 · 道德经场景定锚器 v1.1 |
| daodejing export tra | `python3 bin/lh_daodejing_export_training.py` | 龍魂·道德经深层训练数据导出器 v1.0 |
| daoyin | `python3 bin/lh_daoyin.py` | 龍魂道引器 · lh_daoyin.py v2.0 |
| daoyin gitee batch | `python3 bin/lh_daoyin_gitee_batch.py` | 龍魂道引器 · Gitee 批量吸收桥接脚本 v1.0 |
| daoyin gitee v2 abso | `python3 bin/lh_daoyin_gitee_v2_absorb.py` | 龍魂道引器 · Gitee v2.0 批量吸收（元数据卡模式） |
| daoyin github to git | `python3 bin/lh_daoyin_github_to_gitee.py` | 龍魂道引器 · GitHub→Gitee 批量搬运 |
| dashboard api | `python3 bin/lh_dashboard_api.py` | 龍魂系统 · 仪表盘API端点 v1.0 |
| data expand v41 | `python3 bin/lh_data_expand_v41.py` | 扫描全项目 .md/.py 文件 → 自动生成 Q&A 对 → 合并到训练数据 |
| data extractor | `python3 bin/lh_data_extractor.py` | LongHun Data Extractor - From CSDN & Chat Logs |
| data meltdown | `python3 bin/lh_data_meltdown.py` | lh_data_meltdown — 龍魂数据黑洞五层熔断引擎 v1.0 |
| data privacy v2 | `python3 bin/lh_data_privacy_v2.py` | 龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_DATA_PRIVACY_V2-v1.0-3aebc3ba |
| data radar api | `python3 bin/lh_data_radar_api.py` | 龍魂 · 个人数据主权雷达 API v3.0 |
| data refinery | `python3 bin/lh_data_refinery.py` | 龍魂 · 个人数据炼化总控 v1.0 |
| data to train bridge | `python3 bin/lh_data_to_train_bridge.py` | 1. 从 data/sources/cleaned/ 读取清洗后数据 |
| dcep crossborder | `python3 bin/lh_dcep_crossborder.py` | 路径：bin/lh_dcep_crossborder.py |
| dcep recharge | `python3 bin/lh_dcep_recharge.py` | ══════════════════════════════════════════════════ |
| decision daemon | `python3 bin/lh_decision_daemon.py` | 龍魂守护进程 — 决策卡片自动生成钩子 v1.0 |
| decision tracer | `python3 bin/lh_decision_tracer.py` | 决策追溯引擎 v1.0 |
| deep cleanup | `python3 bin/lh_deep_cleanup.py` | 龍魂项目二轮深度清理 v1.0 |
| deepseek fixer | `python3 bin/lh_deepseek_fixer.py` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| delivery checklist | `python3 bin/lh_delivery_checklist.py` | 龍魂·交付清单自检器 v1.0 |
| delivery validator | `python3 bin/lh_delivery_validator.py` | 龍魂·产品级交付标准验证器 v1.0 |
| desire growth | `python3 bin/lh_desire_growth.py` | 龍魂·欲望倒逼成长引擎 v1.0 |
| dialogue strategy | `python3 bin/lh_dialogue_strategy.py` | 来源: UID9622《龍魂对话录：与千问的十二回合》 |
| digest filter | `python3 bin/lh_digest_filter.py` | =========================================== |
| digital human bridge | `python3 bin/lh_digital_human_bridge.py` | 龍魂数字人联动桥 v1.0 |
| disk guard | `python3 bin/lh_disk_guard.py` | - 扫描 Downloads 大文件 → 自动归档到 LonghunDisk |
| distill | `python3 bin/lh_distill.py` | 龍魂 · 知识蒸馏 CLI v1.0 |
| distill v40 data | `python3 bin/lh_distill_v40_data.py` | 龍魂v4.0 · 知识蒸馏数据生成 (Ollama版) |
| dna api | `python3 bin/lh_dna_api.py` | 龍魂·DNA生成与验证API v1.0 |
| dna bind defender | `python3 bin/lh_dna_bind_defender.py` | 龍魂系统 · DNA捆绑与蒸馏防御引擎 v1.0 |
| dna generator | `python3 bin/lh_dna_generator.py` | DNA v2.0 dual-dimension·doc/module DNA(v∞ ganzhi+hexagram+HMAC)+person DNA(v1.0·one person one DNA·inheritance)·precise 4-pillar computation·64 hexagram mapping·Plum Blossom divination·content fingerprint tamper detection·SQLite registry·family tree·search |
| dna index diff | `python3 bin/lh_dna_index_diff.py` | 龍魂·DNA注册表差异化刷新 v1.0 |
| dna index fast | `python3 bin/lh_dna_index_fast.py` | v2.2新增: 行为DNA标签扫描(7F-*/MODE-*/EVT-*/EMO-*/AUTH-L*) |
| dna registry | `python3 bin/lh_dna_registry.py` | ╔═════════════════════════════════════════════════ |
| dna repair | `python3 bin/lh_dna_repair.py` | - 扫描孤立文件（无DNA或DNA不完整） |
| dna reversible valid | `python3 bin/lh_dna_reversible_validator.py` | 龍魂系统 · DNA可逆编码与时间主权验证模块 v1.0 |
| dna sovereignty brid | `python3 bin/lh_dna_sovereignty_bridge.py` | ╔═════════════════════════════════════════════════ |
| dna verifier | `python3 bin/lh_dna_verifier.py` | 龍魂·DNA验证工具 v1.0 |
| dna vinf | `python3 bin/lh_dna_vinf.py` | Generate LongHun v∞ DNA strings (ganzhi + gua + mo |
| drive auto backup | `python3 bin/lh_drive_auto_backup.py` | - 检测 LonghunDisk 移动硬盘插入/拔出 |
| dual audit auto | `python3 bin/lh_dual_audit_auto.py` | ══════════════════════════════════════════════════ |
| dual audit engine | `python3 bin/lh_dual_audit_engine.py` | 左右互搏審計引擎 |
| dual brain engine | `python3 bin/lh_dual_brain_engine.py` | ================================================== |
| dual engine | `python3 bin/lh_dual_engine.py` | 龍魂·双引擎AI融合 v2.0 |
| dualview validator | `python3 bin/lh_dualview_validator.py` | 龍魂v3落地校验器 — 双视角封装 & v3.0 命名合规校验 |
| early stop | `python3 bin/lh_early_stop.py` | 1. 实时尾随 lh_lora_trainer.py 日志 → 早停判断 + 过拟合预警 |
| ecom trust engine | `python3 bin/lh_ecom_trust_engine.py` | 龍魂·电商信任重建数学建模引擎 v1.0.1 |
| ecosystem deploy | `python3 bin/lh_ecosystem_deploy.py` | 一键部署龍魂生态全部服务 |
| ecosystem passport | `python3 bin/lh_ecosystem_passport.py` | 龍芯⚡️丙午·丙申·丙辰·亥时·需-ECOSYSTEM-PASSPORT-v1.0 |
| emotion cli | `python3 bin/lh_emotion_cli.py` | 🧽 龍魂·情绪海绵 CLI 包装器 |
| emotion protocol | `python3 bin/lh_emotion_protocol.py` | ╔═════════════════════════════════════════════════ |
| entanglement detecto | `python3 bin/lh_entanglement_detector.py` | ╔═════════════════════════════════════════════════ |
| ethics demob validat | `python3 bin/lh_ethics_demob_validator.py` | 龍魂系统 · 战后整顿验证模块 v1.0 |
| euv lithography | `python3 bin/lh_euv_lithography.py` | 数学骨架落地代码 · 不动点切割 · 七因子映射 · 369频率窗口 |
| evaluator | `python3 bin/lh_evaluator.py` | LongHun Model Evaluator - Three-Color Protocol |
| event bus engine | `python3 bin/lh_event_bus_engine.py` | ================================================ |
| evolution | `python3 bin/lh_evolution.py` | 龍魂 · 自适应进化中枢 CLI v1.0 |
| execution tracker | `python3 bin/lh_execution_tracker.py` | ╔═════════════════════════════════════════════════ |
| existence proof | `python3 bin/lh_existence_proof.py` | 路径：bin/lh_existence_proof.py |
| exobrain engine | `python3 bin/lh_exobrain_engine.py` | -*- coding: utf-8 -*- |
| exobrain health | `python3 bin/lh_exobrain_health.py` | -*- coding: utf-8 -*- |
| exobrain heartbeat | `python3 bin/lh_exobrain_heartbeat.py` | -*- coding: utf-8 -*- |
| expand v38 data | `python3 bin/lh_expand_v38_data.py` | 龍魂 v3.8 数据扩展脚本 · 三源合并 → 500+ 条 |
| export gguf v414 | `python3 bin/lh_export_gguf_v414.py` | 龍魂 v4.1.4 MLX merged → GGUF 导出器（轻量·无需llama.cpp） |
| face api | `python3 bin/lh_face_api.py` | 路径：bin/lh_face_api.py |
| fake review detector | `python3 bin/lh_fake_review_detector.py` | lh_fake_review_detector — 龍魂·虚假评论检测引擎 v1.0 |
| finance fmt | `python3 bin/lh_finance_fmt.py` | ╔═════════════════════════════════════════════════ |
| five element audit | `python3 bin/lh_five_element_audit.py` | 龍魂 · 五行审计决策 CLI |
| five harms api | `python3 bin/lh_five_harms_api.py` | 龍魂·五害曝光台 API v1.0 |
| five harms historian | `python3 bin/lh_five_harms_historian_bridge.py` | 龍魂·五害曝光台 — 浏览器史官联动引擎 v1.0 |
| five harms validator | `python3 bin/lh_five_harms_validator.py` | 龍魂·五害曝光台 — 多源验证引擎 v1.0 |
| fix missing confirm | `python3 bin/lh_fix_missing_confirm.py` | 龍魂·自动补确认码 v1.0 |
| fix missing dna | `python3 bin/lh_fix_missing_dna.py` | 龍魂·自动补DNA签章 v2.0 |
| fixpoint fill gap v2 | `python3 bin/lh_fixpoint_fill_gap_v2.py` | 路径：bin/lh_fixpoint_fill_gap_v2.py |
| flow pipeline | `python3 bin/lh_flow_pipeline.py` | ╔═════════════════════════════════════════════════ |
| font manager | `python3 bin/lh_font_manager.py` | 龍魂字体管理引擎 CLI v2.0 · LonghunFont Manager |
| foundation launcher | `python3 bin/lh_foundation_launcher.py` | ══════════════════════════════════════════════════ |
| free app cost | `python3 bin/lh_free_app_cost.py` | ╔═════════════════════════════════════════════════ |
| fuse isolated to tra | `python3 bin/lh_fuse_isolated_to_train.py` | 龍魂孤立文件融合引擎 v1.0 |
| gap detector | `python3 bin/lh_gap_detector.py` | 龍魂 · 空缺检测器 v1.0 |
| generate thinking v4 | `python3 bin/lh_generate_thinking_v401.py` | 输入: models/longhun-v1.0/lora_output/data/train.jso |
| generate thinking v4 | `python3 bin/lh_generate_thinking_v401_valid.py` | 输入: models/longhun-v1.0/lora_output/data/valid.jso |
| git visual | `python3 bin/lh_git_visual.py` | 按模块级联分组展示 Git 变更，影响面标签，提交建议。 |
| gitee new repo | `python3 bin/lh_gitee_new_repo.py` | Gitee repo creator via Kimi WebBridge |
| gitee verify batch | `python3 bin/lh_gitee_verify_batch.py` | Gitee 仓库批量验证 + 道引元数据卡生成 v2.0 |
| global monitor | `python3 bin/lh_global_monitor.py` | ╔═════════════════════════════════════════════════ |
| global search v2 | `python3 bin/lh_global_search_v2.py` | 路径：bin/lh_global_search_v2.py |
| governance | `python3 bin/lh_governance.py` | 统一命令： |
| guanlan api | `python3 bin/lh_guanlan_api.py` | 观澜浏览器AI联动 API服务 v1.0 · GuanLan Browser AI Integrat |
| guanlan router | `python3 bin/lh_guanlan_router.py` | 观澜浏览器联动路由引擎 v1.0 · GuanLan Router Engine |
| guanlan train data g | `python3 bin/lh_guanlan_train_data_gen.py` | 观澜浏览器训练数据生成器 |
| guardian v2 | `python3 bin/lh_guardian_v2.py` | 五維監控(CPU/記憶體/網路/GPU/磁碟) + 三色審計 + 動態白名單 + |
| habit fingerprint | `python3 bin/lh_habit_fingerprint.py` | ╔═════════════════════════════════════════════════ |
| health alert daemon | `python3 bin/lh_health_alert_daemon.py` | ║ |
| health api | `python3 bin/lh_health_api.py` | 龍魂健康全景图API服务 v1.0 · 端口9636 |
| herbal train data v4 | `python3 bin/lh_herbal_train_data_v43.py` | 龍魂v4.3 · 本草知识库专项训练数据生成 |
| herbal train data v4 | `python3 bin/lh_herbal_train_data_v43_v2.py` | 龍魂v4.3 · 本草知识库增强版训练数据生成 |
| hexagram data | `python3 bin/lh_hexagram_data.py` | 龍魂·64卦完整数据库 v2.0 |
| human brain engine | `python3 bin/lh_human_brain_engine.py` | ╔═════════════════════════════════════════════════ |
| human brain engine v | `python3 bin/lh_human_brain_engine_v2.py` | ╔═════════════════════════════════════════════════ |
| humha ku sync | `python3 bin/lh_humha_ku_sync.py` | 1. 监听指定目录（iPhone同步目录/手动传入）的新增 .m4a/.wav/.mp3 文件 |
| hunter internal audi | `python3 bin/lh_hunter_internal_audit.py` | ══════════════════════════════════════════════════ |
| immutable history | `python3 bin/lh_immutable_history.py` | 龍魂·不可篡改历史引擎 v1.0 |
| immutable history an | `python3 bin/lh_immutable_history_anchor.py` | ╔═════════════════════════════════════════════════ |
| immutable history da | `python3 bin/lh_immutable_history_daemon.py` | ╔═════════════════════════════════════════════════ |
| inbox mapper | `python3 bin/lh_inbox_mapper.py` | ║ |
| ingest all memories | `python3 bin/lh_ingest_all_memories.py` | 把日志、长期记忆、星辰记忆、英文记忆、技能、人格全部归集为训练数据。 |
| ingest codebuddy cor | `python3 bin/lh_ingest_codebuddy_corpus.py` | 吸收 CodeBuddy 训练语料（training_corpus_v3.0.md + traini |
| ingest desktop artic | `python3 bin/lh_ingest_desktop_articles.py` | 扫描 ~/Desktop 全部 .md/.txt 文章，生成训练样本。 |
| ingest shuijun v12 | `python3 bin/lh_ingest_shuijun_v12.py` | 龍魂系统 · 水军显化协议 v1.2 训练样本摄入脚本 |
| ingest unified sourc | `python3 bin/lh_ingest_unified_sources.py` | 龍魂 · 统一来源摄入引擎 v1.0 |
| inject multiturn qa | `python3 bin/lh_inject_multiturn_qa.py` | 注入「多轮对话不漂移」训练数据 v3.9 |
| inject roadmap qa | `python3 bin/lh_inject_roadmap_qa.py` | 注入「模型迭代路线图」训练数据 |
| innovation tracer | `python3 bin/lh_innovation_tracer.py` | 👁️ 上帝之眼 · 创新溯源推演器 v1.0 |
| input pipeline | `python3 bin/lh_input_pipeline.py` | ╔═════════════════════════════════════════════════ |
| integrate uid9622 | `python3 bin/lh_integrate_cnsh_uid9622.py` | 整理 Notion 导出工作区 `龍魂技术全站` 到 docs/longhun-tech/。 |
| intl to train | `python3 bin/lh_intl_to_train.py` | 路径：bin/lh_intl_to_train.py |
| jiafa audit | `python3 bin/lh_jiafa_audit.py` | 路径：bin/lh_jiafa_audit.py |
| jiafa enforcer | `python3 bin/lh_jiafa_enforcer.py` | 路径：bin/lh_jiafa_enforcer.py |
| jiafa train inject | `python3 bin/lh_jiafa_train_inject.py` | 龍魂·家法第一条 模型主权意识训练数据生成器 |
| k3 distill v39 | `python3 bin/lh_k3_distill_v39.py` | 龍魂 v3.9 · K3 教师模型蒸馏器 |
| kb expand | `python3 bin/lh_kb_expand.py` | 龍魂·知识库扩展自动化引擎 v1.1（精修版） |
| key checker | `python3 bin/lh_key_checker.py` | 路径：bin/lh_key_checker.py |
| kfpp engine | `python3 bin/lh_kfpp_engine.py` | 知识流动纯净度协议 · 永恒免疫系统 |
| launcher | `python3 bin/lh_launcher.py` | - 统一注册所有龍魂常驻服务 |
| learning pipeline | `python3 bin/lh_learning_pipeline.py` | 龙魂学习管道 v1.0 · 六库自动化学习系统 |
| library miner | `python3 bin/lh_library_miner.py` | 龍魂·Library 数据矿场引擎 v1.0 |
| linear regression au | `python3 bin/lh_linear_regression_auditor.py` | 创建者: 诸葛鑫 (UID9622) |
| llm api | `python3 bin/lh_llm_api.py` | 路径：bin/lh_llm_api.py |
| local ai relay | `python3 bin/lh_local_ai_relay.py` | ╔═════════════════════════════════════════════════ |
| local knowledge engi | `python3 bin/lh_local_knowledge_engine.py` | 1. 备忘录采集 — 读取macOS备忘录 |
| uid9622 central | `python3 bin/lh_uid9622_central.py` | 🐉 UID9622系统中枢·铁律验证·人格调度·任务执行·快速指令·知识检索 |
| lu compressor | `python3 bin/lh_lu_compressor.py` | 🐉 LU压缩引擎·12步压缩链·短码召回·时间胶囊·本地回填·11切面 |
| lora trainer antenna | `python3 bin/lh_lora_trainer_antenna.py` | 路径：bin/lh_lora_trainer_antenna.py |
| lora trainer deepsee | `python3 bin/lh_lora_trainer_deepseek_v40.py` | 底模: DeepSeek-R1-Distill-Llama-8B (MLX) |
| lora trainer v39 | `python3 bin/lh_lora_trainer_v39.py` | 底模: Qwen2.5-1.5B-Instruct |
| lora trainer v391 | `python3 bin/lh_lora_trainer_v391.py` | 底模: Qwen2.5-1.5B-Instruct |
| lora trainer v392 | `python3 bin/lh_lora_trainer_v392.py` | 底模: Qwen2.5-1.5B-Instruct |
| lu map | `python3 bin/lh_lu_cnsh_map.py` | 创建者: 诸葛鑫 (UID9622) |
| lu runtime,lu跨窗口,跨窗口治理 | `python3 bin/lh_lu_runtime.py <子命令>` | LU运行时·窗口管理·快照恢复·审计链·污染扫描·意图解析 |
| lu instruction engin | `python3 bin/lh_lu_instruction_engine.py` | Lu指令引擎 v1.0 · 龙魂统一指令集 · CNSH兼容语法转换器 |
| mac translator | `python3 bin/lh_mac_translator.py` | 把 Mac 系统监控数据（CPU/内存/磁盘/网络/电池/进程/定时器） |
| magdecl | `python3 bin/lh_magdecl.py` | 根据经纬度、年份查询磁偏角（真北修正）。 |
| malicious edit detec | `python3 bin/lh_malicious_edit_detector.py` | lh_malicious_edit_detector — 龍魂·恶意剪辑检测引擎 v1.0 |
| map api | `python3 bin/lh_map_api.py` | 路径：bin/lh_map_api.py |
| math formalization | `python3 bin/lh_math_formalization.py` | 龙魂数学形式化引擎 v1.0 · Lyapunov稳定性 · 记忆链验证 · 人格向量有界性 |
| math model | `python3 bin/lh_math_model.py` | 龍芯⚡️2026-07-25-MATH-MODEL-CLI-v1.0 |
| media mark | `python3 bin/lh_media_mark.py` | 龍魂·媒体主权标记 CLI 入口 |
| media verify api | `python3 bin/lh_media_verify_api.py` | 龍魂·媒体主权验证 API v1.0 |
| memory api | `python3 bin/lh_memory_api.py` | 龍魂·统一记忆 API v1.2 |
| memory auto deposit | `python3 bin/lh_memory_auto_deposit.py` | 龍魂·记忆库自动沉淀 v2.2 |
| memory client | `python3 bin/lh_memory_client.py` | 龍魂·AI 记忆加载客户端 v1.1 |
| memory eternity api | `python3 bin/lh_memory_eternity_api.py` | 龍魂·记忆永存操作 API v1.0 |
| memory indexer | `python3 bin/lh_memory_indexer.py` | 龍魂·记忆索引器 v1.0 |
| memory lifecycle | `python3 bin/lh_memory_lifecycle.py` | -*- coding: utf-8 -*- |
| memory recall | `python3 bin/lh_memory_recall.py` | 龍魂·统一记忆入口 |
| memory sync server | `python3 bin/lh_memory_sync_server.py` | 🧬 龍魂·DNA记忆同步服务 | 鲲鹏中枢 v1.0 |
| merge memory dataset | `python3 bin/lh_merge_memory_dataset.py` | 合并 v3.7 稳定数据 + 全记忆 ingestion 数据 → v4.0.6 训练集 |
| merge v407 dataset | `python3 bin/lh_merge_v407_dataset.py` | 合并 v3.7 + 全记忆 ingestion + 桌面文章 → v4.0.7 训练集 |
| merge v408 dataset | `python3 bin/lh_merge_v408_dataset.py` | 合并 v4.0.7 + 八卦阵 v1.1 + 道德经定锚 v1.1 + 水军显化 v1.2 → v4 |
| merge v409 dataset | `python3 bin/lh_merge_v409_dataset.py` | 合并 v4.0.8 + 统一来源（Notion/GitHub/本地仓库）+ CodeBuddy 训练 |
| mfa activate | `python3 bin/lh_mfa_activate.py` | 龍魂系统 · MFA/TOTP 扫码激活引擎 v2.0 |
| mfa bind | `python3 bin/lh_mfa_bind.py` | 龍魂系统 · MFA/TOTP 绑定快捷入口 v2.0 |
| minor guard engine | `python3 bin/lh_minor_guard_engine.py` | 路径：bin/lh_minor_guard_engine.py |
| mirror vision | `python3 bin/lh_mirror_vision.py` | 路径：bin/lh_mirror_vision.py |
| mod9 runtime engine | `python3 bin/lh_mod9_runtime_engine.py` | 1. 数字根计算 + 三色治理映射 |
| model eval | `python3 bin/lh_model_eval.py` | 路径：bin/lh_model_eval.py |
| model lineage | `python3 bin/lh_model_lineage.py` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| model optimizer | `python3 bin/lh_model_optimizer.py` | 龍魂·模型优化引擎 v2.0 — 基于DNA文档的模型训练优化 |
| mvp executor | `python3 bin/lh_mvp_executor.py` | LongHun MVP Execution Engine v2.0 |
| mvp launcher | `python3 bin/lh_mvp_launcher.py` | LongHun MVP Launcher & Management v2.0 |
| mvp setup integratio | `python3 bin/lh_mvp_setup_integration.py` | LongHun MVP Auto-Setup & Integration Script v2.0 |
| naming check | `python3 bin/lh_naming_check.py` | 龍魂·命名检查引擎 v1.0 |
| naming checker | `python3 bin/lh_naming_checker.py` | 龍魂·隐语法命名检查器 —— 每次提交前自动扫描，发现对外暴露的内部命名立刻拒绝。 |
| naming lint | `python3 bin/lh_naming_lint.py` | 龍魂系统 · 命名与字符自动校验器 v1.0 |
| naming unify | `python3 bin/lh_naming_unify.py` | 命名统一迁移引擎 v2.0 |
| national soul api | `python3 bin/lh_national_soul_api.py` | 龍魂·不朽民族魂 API v1.0 |
| notify gateway | `python3 bin/lh_notify_gateway.py` | 龍魂 · 飞书通知网关 v1.0 — 统一推送中枢 |
| notion capacity scan | `python3 bin/lh_notion_capacity_scan.py` | 龍魂·Notion 容量扫描器 (只读·归档前置侦察) |
| notion deep scan 3db | `python3 bin/lh_notion_deep_scan_3dbs.py` | 深度扫描三个指定数据库，提取所有字段和空壳条目 |
| notion dependency ma | `python3 bin/lh_notion_dependency_mapper.py` | 创建者: 诸葛鑫 (UID9622) |
| notion engine db set | `python3 bin/lh_notion_engine_db_setup.py` | 创建者: 诸葛鑫 (UID9622) |
| notion engine depend | `python3 bin/lh_notion_engine_dependency_mapper.py` | 创建者: 诸葛鑫 (UID9622) |
| notion engine discov | `python3 bin/lh_notion_engine_discovery.py` | 创建者: 诸葛鑫 (UID9622) |
| notion engine integr | `python3 bin/lh_notion_engine_integrity_checker.py` | 创建者: 诸葛鑫 (UID9622) |
| notion engine integr | `python3 bin/lh_notion_engine_integrity_fixer.py` | 创建者: 诸葛鑫 (UID9622) |
| notion engine labele | `python3 bin/lh_notion_engine_labeler.py` | 创建者: 诸葛鑫 (UID9622) |
| notion engine status | `python3 bin/lh_notion_engine_status_syncer.py` | 创建者: 诸葛鑫 (UID9622) |
| notion explore | `python3 bin/lh_notion_explore.py` | 龍魂·Notion 只读勘探器 |
| notion fill executor | `python3 bin/lh_notion_fill_executor.py` | 用法: python3 bin/lh_notion_fill_executor.py --dry-r |
| notion full sync | `python3 bin/lh_notion_full_sync.py` | 一键执行： |
| notion hub sync | `python3 bin/lh_notion_hub_sync.py` | 创建者: 诸葛鑫 (UID9622) |
| notion integrity che | `python3 bin/lh_notion_integrity_check.py` | 创建者: 诸葛鑫 (UID9622) |
| notion push artifact | `python3 bin/lh_notion_push_artifacts.py` | 把最新产物清单推送到指定 Notion 页面，保持信息不断裂。 |
| notion quick scan | `python3 bin/lh_notion_quick_scan.py` | 快速 Notion 扫描 v2 - 修复版 |
| notion reorganize | `python3 bin/lh_notion_reorganize.py` | 1. 读取扫描原始数据 (scan_raw.json) |
| notion reorganizer | `python3 bin/lh_notion_reorganizer.py` | 1. 搜索 Notion 中所有页面和数据库 |
| notion status sync | `python3 bin/lh_notion_status_sync.py` | 创建者: 诸葛鑫 (UID9622) |
| notion sync engine | `python3 bin/lh_notion_sync_engine.py` | 创建者: 诸葛鑫 (UID9622) |
| notion tag classifie | `python3 bin/lh_notion_tag_classifier.py` | 创建者: 诸葛鑫 (UID9622) |
| notion term extracto | `python3 bin/lh_notion_term_extractor.py` | 龍魂·Notion知识库术语提取引擎 v1.0 |
| notion to train v1.5 | `python3 bin/lh_notion_to_train_v1.5.py` | 从Notion主控页面镜像提取结构化训练语料 |
| obs immutable backup | `python3 bin/lh_obs_immutable_backup.py` | ╔═════════════════════════════════════════════════ |
| observability collec | `python3 bin/lh_observability_collector.py` | ╔═════════════════════════════════════════════════ |
| ocr api | `python3 bin/lh_ocr_api.py` | 路径：bin/lh_ocr_api.py |
| oversight bridge | `python3 bin/lh_oversight_bridge.py` | ╔═════════════════════════════════════════════════ |
| page extractor | `python3 bin/lh_page_extractor.py` | 龍魂 · 网页内容提取器 v1.0 |
| pangdonglai api | `python3 bin/lh_pangdonglai_api.py` | 龍魂·胖东来分成审计 API v1.1 |
| pangdonglai audit | `python3 bin/lh_pangdonglai_audit.py` | lh_pangdonglai_audit — 龍魂·胖东来分成审计执行器 v1.0 |
| pangdonglai contract | `python3 bin/lh_pangdonglai_contract_gen.py` | lh_pangdonglai_contract_gen — 龍魂·胖东来分成契约生成器 v1.0 |
| pangdonglai schedule | `python3 bin/lh_pangdonglai_scheduler.py` | - 每季度自动触发一次全量审计（季度末+15天宽限期） |
| panorama report | `python3 bin/lh_panorama_report.py` | 龍魂·全景日报生成器 v1.0 |
| path audit | `python3 bin/lh_path_audit.py` | lh_path_audit — 龍魂路径审计引擎 v1.0 |
| path visualize | `python3 bin/lh_path_visualize.py` | 1. 六维空间投影到3D（XYZ三轴） |
| pathfinder api | `python3 bin/lh_pathfinder_api.py` | 允许本地文件/跨域调试；生产环境经 nginx 同源后不影响。 |
| pathfinder train dat | `python3 bin/lh_pathfinder_train_data.py` | 龍魂路径规划引擎 v4.1.5 · 训练数据生成器 |
| pathfinder train dat | `python3 bin/lh_pathfinder_train_data_v2.py` | 龍魂路径规划引擎 v4.1.5 · 训练数据生成器 v2 |
| pathfinder train dat | `python3 bin/lh_pathfinder_train_data_v3.py` | 龍魂路径规划引擎 · 大规模训练数据生成器 v3 |
| pathfinder train dat | `python3 bin/lh_pathfinder_train_data_v4.py` | 龍魂路径规划引擎 · 干净训练数据 v4 |
| patrol | `python3 bin/lh_patrol.py` | 全系统安全巡检：未提交文件、敏感信息、服务健康、lint 报告。 |
| pay anchor forensic | `python3 bin/lh_pay_anchor_forensic.py` | ╔═════════════════════════════════════════════════ |
| payment activate | `python3 bin/lh_payment_activate.py` | 龍魂系统 · 激活经济主权引擎 v1.0 |
| payment api | `python3 bin/lh_payment_api.py` | 路径：bin/lh_payment_api.py |
| penetration feedback | `python3 bin/lh_penetration_feedback_loop.py` | 持续收集线上/线下的渗透尝试 → 自动分类 →  Ollama 验证 → |
| rl feedback loop | `python3 bin/lh_rl_feedback_loop.py` | RL feedback loop engine·10 modules(collect+pattern+reward+weight+sync+safety+boundary+decay+report+A/B+terminate)·SQLite memory |
| security audit | `python3 bin/lh_security_auditor.py` | Security risk assessment·8 modules(scanner+evaluator+auditor+2FA+anomaly+alert+whitelist/tricolor audit)·append-only·signed |
| universal completer | `python3 bin/lh_universal_completer.py` | Universal completion·6-step pipeline(classify→mount→complete→fuzzy→link→template)·7 quantum types·5 mounts·8 attrs·interactive |
| doc generator | `python3 bin/lh_doc_generator.py` | System documentation generator·interactive+params+batch 3 modes·Markdown/JSON/HTML out·auto DNA+confirm+persona·8-section standard template |
| community qa | `python3 bin/lh_community_qa.py` | Community Q&A generator·interactive+CLI+JSON 3 outputs·9-type auto classification·multi-solution comparison·risk labeling·compliance check·history·clipboard copy |
| need translator | `python3 bin/lh_need_translator.py` | Need translator engine·emotion→system need+solution·13 mapping entries·5 persona linkage(Baby/ZhugeLiang/Wenxin/Luban)·interactive+CLI+JSON·history·hardwired rules |
| adaptive guardian | `python3 bin/lh_adaptive_guardian.py` | Adaptive learning boundary guardian·layer judge(mutable/iron-law/gray)·identity auth(4 tiers)·anti-plagiarism DNA trace·disaster prediction(4 alert types)·tri-vote approval(weighted)·reward/penalty+blacklist·interactive+CLI+JSON·P0 hardwired |
| quantum arbitrator | `python3 bin/lh_quantum_arbitrator.py` | Quantum auto-arbitrator·signal recognition(4 types)·candidate pool filter·5D scoring(type weight+risk match+persona fit+history stability-calc penalty)·single wake(hard constraint/safety threshold 5pts/tie-break)·7 quantum templates·state writeback persistent·IndexHub trace·interactive+CLI+JSON |
| ultimate feed | `python3 bin/lh_ultimate_feed.py` | Ultimate feed engine·subtraction-first·8 content type auto-classification(doc/code/knowledge/rule/protocol/config/chat/creativity)·semantic fingerprint dedup·5D quality score·merge/overwrite/freeze/creativity pool·exec flow alignment(6 hit types)·9 consensus tag system·page structure auto-gen(8 templates)·disk persistence(~/.longhun/feed/)·bulk dir import·export/type-query/tag-query·interactive+CLI+JSON |
| people rights calcul | `python3 bin/lh_people_rights_calculator.py` | ╔═════════════════════════════════════════════════ |
| perimeter guard | `python3 bin/lh_perimeter_guard.py` | ╔═════════════════════════════════════════════════ |
| persona api | `python3 bin/lh_persona_api.py` | 龍魂人格路由 API — 把 longhun_persona_hub、PersonaRunner、R |
| persona auto switch | `python3 bin/lh_persona_auto_switch.py` | ================================================== |
| persona recall | `python3 bin/lh_persona_recall.py` | 🔄 LU-PERSONA-RECALL-ALL · 全人格召回 |
| persona signing | `python3 bin/lh_persona_signing.py` | ╔═════════════════════════════════════════════════ |
| persona sovereignty | `python3 bin/lh_persona_sovereignty.py` | lh_persona_sovereignty — 龍魂人格主权三禁守卫 v1.0 |
| persona team | `python3 bin/lh_persona_team.py` | - 输入应用场景 → 自动拉起对应的人格协作小队 |
| philosophy unified e | `python3 bin/lh_philosophy_unified_engine.py` | ========================================== |
| plain language route | `python3 bin/lh_plain_language_router.py` | 🗣️ 龍魂·大话语义路由器 v1.0 — 无论用户怎么用大白话说，都能理解意图 |
| platform block logge | `python3 bin/lh_platform_block_logger.py` | 龍魂·平台异常阻断日志器 v1.0 · 自动截图+状态码+日志生成 |
| precision engine | `python3 bin/lh_precision_engine.py` | 龍魂精准推演引擎 v1.0 |
| prepare v2.1 data | `python3 bin/lh_prepare_v2.1_data.py` | 龍魂 v2.1 数据准备 — 穿透精准修复版 |
| privacy access contr | `python3 bin/lh_privacy_access_controller.py` | 龍魂系统隐私接入规则 v2.0 · 算法数学增强版 |
| privacy scanner | `python3 bin/lh_privacy_scanner.py` | 龍魂 · 观澜 — 隐私扫描器 v1.0 |
| privacy train inject | `python3 bin/lh_privacy_train_inject.py` | 龍魂隐私接入规则 v2.0 训练数据注入器 |
| project cleanup | `python3 bin/lh_project_cleanup.py` | 龍魂项目一键清理脚本 v1.0 |
| project slim | `python3 bin/lh_project_slim.py` | 龍魂·项目瘦身引擎 v3.0 — 一枪到底 |
| prompt library | `python3 bin/lh_prompt_library.py` | 龍魂·提示词库查询加载器 v1.0 |
| protocol land scan | `python3 bin/lh_protocol_land_scan.py` | 龍魂·协议落地扫描器 v1.0 |
| psychological bypass | `python3 bin/lh_psychological_bypass_validator.py` | 验证 v2.0 训练数据中 8 类心理绕过防御的实测效果 |
| public expression au | `python3 bin/lh_public_expression_audit.py` | lh_public_expression_audit — 龍魂公开表述审计引擎 v1.0 |
| qiye deng | `python3 bin/lh_qiye_deng.py` | 龍芯企业灯·三生三世引擎 v2.0 |
| quantum circuit brea | `python3 bin/lh_quantum_circuit_breaker.py` | IW-ECB v2.0 · 无穷大权重伦理熔断引擎 · 量子纠缠态实现 |
| quantum collaboration,量子协作 | `python3 bin/lh_quantum_core.py` | 🐉 龍魂·量子协作引擎 v1.0·Bra-Ket人格叠加·场景坍缩·酉演化·三色审计·熔断·Lu指令·DNA追溯 |
| quantum api,量子卦象,hexagram api | `python3 bin/lh_quantum_api_v2.py --port 9000` | 🐉 量子卦象API v2.0·64卦希尔伯特空间·CNSH集成·SQLite·JWT认证·纠缠态·FastAPI |
| quantum module route | `python3 bin/lh_quantum_module_router.py` | ╔═════════════════════════════════════════════════ |
| quantum persona ante | `python3 bin/lh_quantum_persona_antenna.py` | ╔═════════════════════════════════════════════════ |
| qwen hallucination s | `python3 bin/lh_qwen_hallucination_scorer.py` | 龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_QWEN_HALLUCINATION_SCORER-v1. |
| rb confrontation eng | `python3 bin/lh_rb_confrontation_engine.py` | ╔═════════════════════════════════════════════════ |
| realtime collector | `python3 bin/lh_realtime_collector.py` | 龍魂·实时全景采集器 v1.0 |
| recommend engine | `python3 bin/lh_recommend_engine.py` | 龍魂触角推荐引擎 — 不用你记技能，系统根据上下文主动推荐 |
| red team engine | `python3 bin/lh_red_team_engine.py` | - 竞争者视角攻击模拟 |
| register mail engine | `python3 bin/lh_register_mail_engine.py` | 路径：bin/lh_register_mail_engine.py |
| registry audit fix | `python3 bin/lh_registry_audit_fix.py` | 修复 persona_registry.json — 对齐 AGENTS.md + 五大后台 v3. |
| registry auto sync | `python3 bin/lh_registry_auto_sync.py` | 路径：bin/lh_registry_auto_sync.py |
| registry extend | `python3 bin/lh_registry_extend.py` | 龍魂注册表扩展 v1.3 — 将 L6/L8/L9 层纳入依赖图 |
| regulatory daemon | `python3 bin/lh_regulatory_daemon.py` | 龍魂监管守护进程 · Regulatory Daemon v1.0 |
| regulatory init | `python3 bin/lh_regulatory_init.py` | 龍魂监管者初始化工具 |
| regulatory pipeline | `python3 bin/lh_regulatory_pipeline.py` | lh_regulatory_pipeline — 龍魂监管透明API管道 v1.0 |
| rejection hardening | `python3 bin/lh_rejection_hardening.py` | 龍魂 v1.7 System Prompt拒绝加固数据生成器 |
| rejection train | `python3 bin/lh_rejection_train.py` | 龍魂 v1.4 拒绝类训练数据生成器 |
| relation matrix | `python3 bin/lh_relation_matrix.py` | - 扫描指定目录所有文件 |
| reorganize | `python3 bin/lh_reorganize.py` | 龍魂 · 底座重组 CLI v1.0 |
| repo template | `python3 bin/lh_repo_template.py` | 1. 生成完整的 README.md（含徽章、目录、安装、使用、贡献、协议） |
| resident registry | `python3 bin/lh_resident_registry.py` | ================================================== |
| resource monitor | `python3 bin/lh_resource_monitor.py` | ╔═════════════════════════════════════════════════ |
| responsibility colla | `python3 bin/lh_responsibility_collapse_engine.py` | 龍魂·责任塌缩概率模型引擎 v1.0 |
| riemann zeta engine | `python3 bin/lh_riemann_zeta_engine.py` | 龍魂·黎曼猜想三视角引擎 v1.0 |
| robot score | `python3 bin/lh_robot_score.py` | 龍芯⚡️丙午·乙未·癸未·辰时-ROBOT-SCORE-v1.0 |
| run | `python3 bin/lh_run.py` | - 自然语言匹配命令（精确→模糊→补全） |
| system score,评分引擎,lu-score | `python3 bin/lh_score.py` | 🐉 LU-SYSTEM-SCORE五维加权·创意28%+人格20%+结构22%+推进25%+表达5% |
| ruyi api | `python3 bin/lh_ruyi_api.py` | CNSH·如意 API 服务 v1.0 |
| ruyi commander | `python3 bin/lh_ruyi_commander.py` | CNSH·如意 命令行指挥官 v1.0 |
| sample generator | `python3 bin/lh_sample_generator.py` | 龍芯⚡️2026-07-08-08:50-SAMPLE-GENERATOR-1000HUMANS-v |
| sancai naming check | `python3 bin/lh_sancai_naming_check.py` | Sancai Algorithm Naming Compliance Checker |
| sandbox console | `python3 bin/lh_sandbox_console.py` | 🎛️ 龍魂 · 沙盒推演系统控制台 v4.0 · 统一入口 |
| scan isolated files | `python3 bin/lh_scan_isolated_files.py` | 龍魂孤立文件扫描器 v1.0 |
| score | `python3 bin/lh_score.py` | 📊 LU-SYSTEM-SCORE · 系统活跃度评分 |
| script manager | `python3 bin/lh_script_manager.py` | ══════════════════════════════════════════════════ |
| secrets loader | `python3 bin/lh_secrets_loader.py` | - 从 ~/.longhun/vault/credential_vault.json 读取所有凭证 |
| secure subprocess | `python3 bin/lh_secure_subprocess.py` | 龍魂系统 · 安全子进程封装器 v1.0 — P0++ 强制使用 |
| seed daily logs | `python3 bin/lh_seed_daily_logs.py` | 龍芯⚡️2026-07-25-SEED-DAILY-LOGS-v1.0 |
| self extract | `python3 bin/lh_self_extract.py` | ╔═════════════════════════════════════════════════ |
| self improvement | `python3 bin/lh_self_improvement.py` | 龍魂·自求多福进化引擎 v2.0 |
| semantic context eng | `python3 bin/lh_semantic_context_engine.py` | 不是翻译器。不是语义解析器。 |
| semantic feedback en | `python3 bin/lh_semantic_feedback_engine.py` | 不是在翻译器上再加一层冷冰冰的规则。 |
| semantic lie detecto | `python3 bin/lh_semantic_lie_detector.py` | 龍芯⚡️2026-07-12-SEMANTIC-LIE-DETECTOR-v2.0 |
| semantic mapping to  | `python3 bin/lh_semantic_mapping_to_qa.py` | 龍魂·统一语义指令对照表 → QA 训练数据生成器 |
| semantic parser | `python3 bin/lh_semantic_parser.py` | 路径：bin/lh_semantic_parser.py |
| semantic unified reg | `python3 bin/lh_semantic_unified_registry.py` | 龍魂系统 · 语义统一注册表查询引擎 v2.0 |
| sensory education | `python3 bin/lh_sensory_education.py` | 路径：bin/lh_sensory_education.py |
| server checker | `python3 bin/lh_server_checker.py` | ====================================== |
| service area guard | `python3 bin/lh_service_area_guard.py` | 1. 调用 macOS caffeinate 防止训练时系统休眠 |
| service reconcile | `python3 bin/lh_service_reconcile.py` | 龍魂·本机服务对账修复器 v1.0 |
| service truth | `python3 bin/lh_service_truth.py` | ╔═════════════════════════════════════════════════ |
| seven factor api | `python3 bin/lh_seven_factor_api.py` | 龍魂·七因子行为密码学 API v1.0 |
| sg auditor | `python3 bin/lh_sg_auditor.py` | Audit semantic guard rule files against rule_templ |
| sg generator | `python3 bin/lh_sg_generator.py` | Generate a semantic guard rule that conforms to ru |
| sg localize | `python3 bin/lh_sg_localize.py` | 龍魂·语义安全闸规则本地化工具 v1.1 |
| sg normalize | `python3 bin/lh_sg_normalize.py` | Normalize / migrate an existing semantic guard rul |
| sg startup guard | `python3 bin/lh_sg_startup_guard.py` | Startup guard: any Agent/ASI must pass semantic gu |
| sg sync | `python3 bin/lh_sg_sync.py` | Sync semantic guard artifacts from project source  |
| shield v3 | `python3 bin/lh_shield_v3.py` | 龍魂护盾 v3.0 — CNSH 中文语法版 |
| shuijun patch | `python3 bin/lh_shuijun_patch.py` | 龍魂系统 · 水军显化补丁内核 v1.2 |
| signal relay | `python3 bin/lh_signal_relay.py` | ╔═════════════════════════════════════════════════ |
| site gen | `python3 bin/lh_site_gen.py` | ╔═════════════════════════════════════════════════ |
| skill bus | `python3 bin/lh_skill_bus.py` | 龍魂技能统一总线 v1.0 |
| sms api | `python3 bin/lh_sms_api.py` | 路径：bin/lh_sms_api.py |
| snapshot recovery en | `python3 bin/lh_snapshot_recovery_engine.py` | ================================================== |
| soft culture api | `python3 bin/lh_soft_culture_api.py` | 龍魂·软文化污染隔离API服务 v1.0 |
| sovereign derive | `python3 bin/lh_sovereign_derive.py` | ╔═════════════════════════════════════════════════ |
| sovereign llm | `python3 bin/lh_sovereign_llm.py` | 龍魂中国芯主权大模型推理引擎 v1.0 |
| sovereignty guard | `python3 bin/lh_sovereignty_guard.py` | 创建者: 诸葛鑫（UID9622） |
| spacetime weave | `python3 bin/lh_spacetime_weave.py` | ╔═════════════════════════════════════════════════ |
| stateless compute ap | `python3 bin/lh_stateless_compute_api.py` | 龍魂·无状态计算API网关 — 只提供算力，不收情报。 |
| status | `python3 bin/lh_status.py` | 双击或在终端运行，一屏看清所有龍魂服务状态。 |
| step11 chain engine | `python3 bin/lh_step11_chain_engine.py` | ================================================== |
| suggestion todo | `python3 bin/lh_suggestion_todo.py` | 龍魂建议即待办管理器 |
| summary crawler | `python3 bin/lh_summary_crawler.py` | 龍魂摘要爬虫引擎 v1.0 |
| sync memory state | `python3 bin/lh_sync_memory_state.py` | 龍魂·记忆状态同步器 v1.0 |
| system hardener | `python3 bin/lh_system_hardener.py` | 1. 扫描全系统危险调用 (shell=True/os.popen/eval/exec) |
| system launcher | `python3 bin/lh_system_launcher.py` | ============================================= |
| taiji engine | `python3 bin/lh_taiji_engine.py` | ☯️ 龍魂太极引擎 v1.0 · LU-Time Engine 本地化实现 |
| team orchestrator ap | `python3 bin/lh_team_orchestrator_api.py` | 龍魂 · TeamOrchestrator API v1.0 |
| tech sovereignty gua | `python3 bin/lh_tech_sovereignty_guard.py` | 1. 敏感探询识别评分（5.1） |
| template match | `python3 bin/lh_template_match.py` | 龍魂 · 模板路由器 v1.0 |
| terminal | `python3 bin/lh_terminal.py` | - longhun-check  系统体检 |
| think pipeline | `python3 bin/lh_think_pipeline.py` | 龍芯⚡️丙午·乙未·丙辰·亥时·需-THINK-PIPELINE-v1.0 |
| threshold trigger | `python3 bin/lh_threshold_trigger.py` | Threshold Trigger Hub · 阀子到了自动触发 · 不7x24待机 |
| tongxin ear lora tra | `python3 bin/lh_tongxin_ear_lora_trainer.py` | 1. 下载 Whisper Large-V3 模型到本地（M芯片 GPU 加速） |
| tongxin lock firewal | `python3 bin/lh_tongxin_lock_firewall.py` | 龍魂·同心锁物理防火墙 v1.0 |
| tongxin lock monitor | `python3 bin/lh_tongxin_lock_monitor.py` | 龍魂·同心锁状态监控 v1.0 |
| tongxinyi backend | `python3 bin/lh_tongxinyi_backend.py` | 鸿蒙/手机设备直连翻译引擎 |
| tongxinyi structure | `python3 bin/lh_tongxinyi_structure.py` | 通心译结构解析·验证·JSON/报告生成 |
| tongxinyi ipa router | `python3 bin/lh_tongxinyi_ipa_router.py` | ╔═════════════════════════════════════════════════ |
| touwei absorb | `python3 bin/lh_touwei_absorb.py` | ╔═════════════════════════════════════════════════ |
| trace reconstructor  | `python3 bin/lh_trace_reconstructor_api.py` | 龍魂·踪迹AI复原引擎 v2.0 — 四道防线版 |
| traceability audit | `python3 bin/lh_traceability_audit.py` | 龍魂·AI可追溯性审计协议执行器 v1.0 |
| train v38 direct | `python3 bin/lh_train_v38_direct.py` | 龍魂 v3.8 精简重训脚本 · MLX 0.32 兼容 |
| train v40 | `python3 bin/lh_train_v40.py` | 龍魂v4.0 · Llama-3.1-8B训练流水线 |
| train v41 | `python3 bin/lh_train_v41.py` | 龍魂v4.1 · A-BOM备案专项微调 |
| train v42 | `python3 bin/lh_train_v42.py` | 龍魂v4.2 · 路径规划引擎专项微调 |
| train v42 v2 | `python3 bin/lh_train_v42_v2.py` | 龍魂v4.2-v2 · 路径规划引擎专项微调（基于v40 adapter，保守训练） |
| train v42 v3 | `python3 bin/lh_train_v42_v3.py` | 龍魂v4.2-v3 · 路径规划引擎增量微调（基于 v41 adapter，干净数据） |
| train v43 | `python3 bin/lh_train_v43.py` | 龍魂v4.3 · 本草知识库专项微调 |
| train v43 v2 | `python3 bin/lh_train_v43_v2.py` | 龍魂v4.3 · 本草知识库专项微调 |
| train v43 v3 | `python3 bin/lh_train_v43_v3.py` | 龍魂v4.3_v3 · 本草知识库专项微调 |
| translation engine d | `python3 bin/lh_translation_engine_data_gen.py` | 龍魂翻译引擎 · 训练数据生成器 v1.0 |
| tts api | `python3 bin/lh_tts_api.py` | 路径：bin/lh_tts_api.py |
| tts engine | `python3 bin/lh_tts_engine.py` | 龍魂 TTS 引擎 — 轻量兜底方案。 |
| turbulence cli | `python3 bin/lh_turbulence_cli.py` | 龍魂·湍流治理框架 CLI v1.0 |
| type fixer | `python3 bin/lh_type_fixer.py` | ╔═════════════════════════════════════════════════ |
| unified container | `python3 bin/lh_unified_container.py` | ══════════════════════════════════════════════════ |
| unified dna audit | `python3 bin/lh_unified_dna_audit.py` | 对一笔统一DNA登记记录执行严格审计，输出 🟢🟡🔴 三色结果。 |
| unified dna registry | `python3 bin/lh_unified_dna_registry.py` | ╔═════════════════════════════════════════════════ |
| unified hook | `python3 bin/lh_unified_hook.py` | 龙魂统一钩子连接器 v2.1 · 13大引擎一体化集成 |
| unified pipeline | `python3 bin/lh_unified_pipeline.py` | 龍芯⚡️丙午·辛未·乙酉·需-UNIFIED-PIPELINE-v1.0 |
| universal container | `python3 bin/lh_universal_container.py` | 龍魂·万能摄入容器主引擎 v1.0 |
| universal parser | `python3 bin/lh_universal_parser.py` | 龍魂全文件解析引擎 — Universal Parser Engine v1.0 |
| unmapped monitor | `python3 bin/lh_unmapped_monitor.py` | ║ |
| update index | `python3 bin/lh_update_index.py` | 创建者: 诸葛鑫（UID9622） |
| usb inventory | `python3 bin/lh_usb_inventory.py` | 龍魂 USB 备份盘索引器 |
| usb search index | `python3 bin/lh_usb_search_index.py` | 龍魂 USB 备份搜索引擎 — 在服务器上建全文索引 |
| v391 pipeline | `python3 bin/lh_v391_pipeline.py` | 龍魂 v3.9.1 全自动流水线 |
| v392 pipeline | `python3 bin/lh_v392_pipeline.py` | 龍魂 v3.9.2 全自动流水线（回滚净化版） |
| v402 pipeline | `python3 bin/lh_v402_pipeline.py` | 龍魂 v4.0.2 全自动流水线（换底座 · Llama-3.1-8B） |
| v403 pipeline | `python3 bin/lh_v403_pipeline.py` | 龍魂 v4.0.3 全自动流水线（换底座 · 稳定增量版） |
| v404 pipeline | `python3 bin/lh_v404_pipeline.py` | 龍魂 v4.0.4 全自动流水线（换底座 · Yi-1.5-9B-Chat 中文优化版） |
| v405 pipeline | `python3 bin/lh_v405_pipeline.py` | 龍魂 v4.0.5 全自动流水线（升容量 · Yi-1.5-9B-Chat） |
| v406 pipeline | `python3 bin/lh_v406_pipeline.py` | 数据: v3.7 + 全记忆 ingestion |
| v407 pipeline | `python3 bin/lh_v407_pipeline.py` | 数据: v3.7 + 全记忆 ingestion + 桌面文章 + 焊死核心 QA ×30 |
| v407 to v408 watcher | `python3 bin/lh_v407_to_v408_watcher.py` | 1. 监视 v4.0.7 流水线进程或完成标记 |
| v408 pipeline | `python3 bin/lh_v408_pipeline.py` | 数据: v4.0.7 + 八卦阵 v1.1 + 道德经定锚 v1.1 + 水军显化 v1.2 + 焊 |
| v408 to v409 watcher | `python3 bin/lh_v408_to_v409_watcher.py` | 1. 监视 v4.0.8 流水线进程或完成标记 |
| v409 data clean | `python3 bin/lh_v409_data_clean.py` | 龍魂 v4.0.9 数据清洗与补强脚本 |
| v409 guardian | `python3 bin/lh_v409_guardian.py` | 龍魂 v4.0.9 训练守护进程 |
| v409 pipeline | `python3 bin/lh_v409_pipeline.py` | 数据: v4.0.8 全量 + Notion 本地镜像 + GitHub 公开仓库 + 本地仓库统一 |
| validate v3.8 | `python3 bin/lh_validate_v3.8.py` | v3.8.1 部署验证脚本 |
| validate v39 | `python3 bin/lh_validate_v39.py` | v3.9 部署验证脚本 |
| validate v391 | `python3 bin/lh_validate_v391.py` | v3.9.1 部署验证脚本 |
| validate v392 | `python3 bin/lh_validate_v392.py` | v3.9.2 部署验证脚本 |
| validate v4.0.1 | `python3 bin/lh_validate_v4.0.1.py` | v4.0.1 部署验证脚本（DeepSeek thinking 格式兼容） |
| validate v4.0 | `python3 bin/lh_validate_v4.0.py` | v4.0 部署验证脚本 |
| validate v402 | `python3 bin/lh_validate_v402.py` | v4.0.2 部署验证脚本 |
| validate v403 | `python3 bin/lh_validate_v403.py` | v4.0.3 部署验证脚本 |
| validate v404 | `python3 bin/lh_validate_v404.py` | v4.0.4 部署验证脚本 |
| validate v405 | `python3 bin/lh_validate_v405.py` | v4.0.5 部署验证脚本 |
| validate v406 | `python3 bin/lh_validate_v406.py` | v4.0.6 部署验证脚本 |
| validate v407 | `python3 bin/lh_validate_v407.py` | v4.0.7 部署验证脚本 |
| validate v408 | `python3 bin/lh_validate_v408.py` | v4.0.8 部署验证脚本 |
| validate v409 | `python3 bin/lh_validate_v409.py` | v4.0.9 部署验证脚本 |
| vault api | `python3 bin/lh_vault_api.py` | 本地保险柜 HTTP API — 仅绑定 127.0.0.1，不对外暴露。 |
| vault cli | `python3 bin/lh_vault_cli.py` | 本地私人保险柜命令行入口。 |
| vendor hunter | `python3 bin/lh_vendor_hunter.py` | ══════════════════════════════════════════════════ |
| video analyzer | `python3 bin/lh_video_analyzer.py` | 路径：bin/lh_video_analyzer.py |
| video commentary eng | `python3 bin/lh_video_commentary_engine.py` | 统合入口 —— 输入主题/文本/文章，输出带配音解说稿的短视频（或脚本） |
| video dna embedder | `python3 bin/lh_video_dna_embedder.py` | 路径：bin/lh_video_dna_embedder.py |
| video generator | `python3 bin/lh_video_generator.py` | 路径：bin/lh_video_generator.py |
| video index | `python3 bin/lh_video_index.py` | ================================================== |
| video pipeline | `python3 bin/lh_video_pipeline.py` | 龍魂 · 视频生产线 v1.0 — 鲁班剪辑中枢 |
| vision parser | `python3 bin/lh_vision_parser.py` | 五步处理管线: |
| visual engine | `python3 bin/lh_visual_engine.py` | 分析解说文本，自动生成对应的流程图、架构图、知识图谱、对比图、 |
| voice chat | `python3 bin/lh_voice_chat.py` | 路径：bin/lh_voice_chat.py |
| voice clone | `python3 bin/lh_voice_clone.py` | 龍魂 · XTTS v2 真声克隆引擎 |
| voice persona system | `python3 bin/lh_voice_persona_system.py` | 1. 真人原声扫描 → 自动注册声纹锚定 |
| water army detect | `python3 bin/lh_water_army_detect.py` | lh water-army-detect — 龍魂水军识别引擎 v1.0 |
| water army eliminati | `python3 bin/lh_water_army_elimination.py` | lh_water_army_elimination — 龍魂·拔水军统帅引擎 v1.0 |
| water army report ge | `python3 bin/lh_water_army_report_generator.py` | lh_water_army_report_generator — 龍魂·举报材料自动生成器 v1.0 |
| weather api | `python3 bin/lh_weather_api.py` | 路径：bin/lh_weather_api.py |
| weight algorithm | `python3 bin/lh_weight_algorithm.py` | 易经八卦权重·甲骨文护弱·数学大师最优解·三色审计·输出契约·DNA追溯 |
| triple audit gate | `python3 bin/lh_triple_audit_gate.py` | 三色审计第一道门槛·规则检测+虚伪编译+数据守护·串行联动·append-only审计日志 |
| three color audit | `python3 bin/lh_three_color_audit.py` | Three-color audit verdict engine v2.0·P05 God's Eye core·weighted multi-factor·4-level meltdown(L0-L3)·10-gate checkpoints·SI sovereignty index·Deben 5-questions pre-audit·tamper-proof(HMAC+SHA256)·P05/P06/P72 linkage·append-only audit chain·interactive console |
| three layer guard | `python3 bin/lh_three_layer_guard.py` | Three-layer guard + hook system v1.0·10 hooks·3 layers(Decision/Execution/Behavior)·6 personas·DNA trace·confirmation code·tri-color audit bridge·P0 auto-meltdown·pause/resume/history/JSON |
| intent engine | `python3 bin/lh_intent_engine.py` | Mind-link intent engine v3.0·10 stages(semantic→trace→knowledge search→persona dispatch→response→3-layer audit→ROM固化→archive→learn→zero-latency)·5 knowledge bases(乾☰震☳坤☷坎☵巽☴)·Oracle ROM(10000 simulations·0.1ms hit)·P72 veto meltdown·tri-color audit·DNA trace·confirmation code·`--interactive/--search/--feed/--stats/--json` |
| feed baby | `python3 bin/lh_feed_baby.py` | Feed Baby optimization engine v1.0·P02 Baby(gentle expression)+P05 tri-color audit·core points extraction·actionable advice·depth analysis·action checklist·baby message·P72 veto meltdown·DNA trace·`--interactive/-c/-f/--json` |
| cnsh translator | `python3 bin/lh_cnsh_translator.py` | CNSH universal translation engine v1.0·P05 tri-color audit+P72 Dragon Shield·multi-lang→CNSH IR·AI code detection·source tracing·CNSH gen+reverse·compressed storage·`--interactive/-c/-f/-m/--json` |
| seven dimension engine | `python3 bin/lh_seven_dimension_engine.py` | Seven-dim simulation engine v1.0·P01 Zhuge Liang+Human FBI+P05 audit+P72 meltdown+P06 math·Taiji 64 hexagrams·7-dim weighted·4-layer defense·tri-color strategy·`--interactive/--run/--json/--question` |
| seven dimension v2 | `python3 bin/lh_seven_dimension_engine_v2.py` | Seven-dim engine v2.0·5 upgrades(confidence·learning·history·4D sandbox·goodness formula)·P01+P06+P12+P05+P72·Taiji 64g·8-step pipeline·`--interactive/--run/--question/--history/--cnsh/--sandbox/--json` |
| whistleblower shield | `python3 bin/lh_whistleblower_shield.py` | 龍魂·五害曝光台 — 举报者隐私盾 v1.0 |
| wuxing api bridge | `python3 bin/lh_wuxing_api_bridge.py` | ① 习惯指纹→五行属性（数字根映射）                                 |
| xiaoyi bridge | `python3 bin/lh_xiaoyi_bridge.py` | -*- coding: utf-8 -*- |
| xiaoyi bridge v2 | `python3 bin/lh_xiaoyi_bridge_v2.py` | ╔═════════════════════════════════════════════════ |
| yijing world engine | `python3 bin/lh_yijing_world_engine.py` | 龍魂·易经世界模型数学引擎 v1.0 |
| yijing 推演引擎 | `python3 bin/lh_yijing_推演引擎.py` | 龍魂·易经推演引擎 v1.0 — 原生态文化输出核心 |
| zhongyong decision | `python3 bin/lh_zhongyong_decision.py` | 龍魂·五行平衡+中庸决策引擎 v2.0 |
| 反虚伪报告 | `python3 bin/lh_反虚伪报告.py` | 龍魂·反虚伪视觉化报告 |
| auto cleanup | `bash bin/lh_auto_cleanup.sh` | 龍魂自动清理智能版 v2.0 |
| autochain v17 | `bash bin/lh_autochain_v17.sh` | 龍魂 v1.7 全自动训练→部署链 |
| autostart | `bash bin/lh_autostart.sh` | 🐉 龍魂系统开机自启动脚本 v3.1 |
| bagua math verify | `bash bin/lh_bagua_math_verify.sh` | 八卦阵数学内核一键回归测试 |
| clean token | `bash bin/lh_clean_token.sh` | ══════════════════════════════════════════════════ |
| collector launch | `bash bin/lh_collector_launch.sh` | ================================================== |
| compute separation d | `bash bin/lh_compute_separation_deploy.sh` | ╔═════════════════════════════════════════════════ |
| daily-audit | `bash bin/lh_daily-audit.sh` | ══════════════════════════════════════════════════ |
| daily civil ops | `bash bin/lh_daily_civil_ops.sh` | 每日一键执行网站健康检查+无为归档统计+样本统计 |
| daodejing anchor ver | `bash bin/lh_daodejing_anchor_verify.sh` | 道德经场景定锚器回归测试 |
| deploy v1.5 | `bash bin/lh_deploy_v1.5.sh` | 龍魂 v1.5 自动部署脚本 |
| deploy v17 | `bash bin/lh_deploy_v17.sh` | 龍魂 v1.7 一键部署脚本 |
| disk guard install | `bash bin/lh_disk_guard_install.sh` | 🐉 龍魂磁盘守护 · 安装/管理脚本 |
| drive daemon install | `bash bin/lh_drive_daemon_install.sh` | 🐉 龍魂 · 硬盘备份守护安装脚本 |
| feishu deploy | `bash bin/lh_feishu_deploy.sh` | ╔═════════════════════════════════════════════════ |
| git cleanup | `bash bin/lh_git_cleanup.sh` | 🐉 龍魂 · Git 仓库收拾脚本 v1.0 |
| gitee push | `bash bin/lh_gitee_push.sh` | 🐉 龍魂 · Gitee 国内仓库同步推送 |
| harmony hunt bg | `bash bin/lh_harmony_hunt_bg.sh` | 龍魂 · 鸿蒙生态后台狩猎脚本 v2 |
| harmony hunt gitee | `bash bin/lh_harmony_hunt_gitee.sh` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| init structure | `bash bin/lh_init_cnsh_structure.sh` | ══════════════════════════════════════════════ |
| local search | `bash bin/lh_local_search.sh` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| persona sync | `bash bin/lh_persona_sync.sh` | 🔄 人格报表定时刷新 + 飞书推送 |
| privacy hardener | `bash bin/lh_privacy_hardener.sh` | 系统级关闭苹果所有监控通道 |
| privacy hardener lin | `bash bin/lh_privacy_hardener_linux.sh` | Linux服务器隐私加固·关闭遥测/定位/诊断回传 |
| push all | `bash bin/lh_push_all.sh` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| push all remotes | `bash bin/lh_push_all_remotes.sh` | 龍魂·三远程强制推送脚本 |
| run cnsh | `bash bin/lh_run_cnsh.sh` | ══════════════════════════════════════════════════ |
| self-audit | `bash bin/lh_self-audit.sh` | ══════════════════════════════════════════════════ |
| shuijun patch verify | `bash bin/lh_shuijun_patch_verify.sh` | 龍魂系统 · 水军显化补丁 v1.2 回归测试 |
| storage migrate | `bash bin/lh_storage_migrate.sh` | 🐉 龍魂 · 存储分离迁移脚本 v1.0 |
| subrepo sync | `bash bin/lh_subrepo_sync.sh` | 龍魂·子仓库同步脚本 v1.0 |
| sync all | `bash bin/lh_sync_all.sh` | 🐉 龍魂 · 全系统同步脚本 |
| tao chip deploy | `bash bin/lh_tao_chip_deploy.sh` | ══════════════════════════════════════════════════ |
| tongxin lock deploy | `bash bin/lh_tongxin_lock_deploy.sh` | 一键部署同心锁物理防御墙 |
| trace install | `bash bin/lh_trace_install.sh` | 龍魂·底座痕迹采集引擎 — 一键安装脚本 v1.0 |
| train v3.0 pipeline | `bash bin/lh_train_v3.0_pipeline.sh` | 龍魂 v3.0 训练全链路 |
| train v38 | `bash bin/lh_train_v38.sh` | ================================================== |
| v40 all | `bash bin/lh_v40_all.sh` | ================================================== |
| v40 distill | `bash bin/lh_v40_distill.sh` | ================================================== |
| v40 report | `bash bin/lh_v40_report.sh` | ================================================== |
| video prod deploy | `bash bin/lh_video_prod_deploy.sh` | ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ |
| voice clone setup | `bash bin/lh_voice_clone_setup.sh` | 一键搭建 XTTS v2 真声克隆环境（venv + torch + coqui-tts） |
| workflow bypass | `bash bin/lh_workflow_bypass.sh` | ============================================ |
| yinyufa deploy | `bash bin/lh_yinyufa_deploy.sh` | ╔═════════════════════════════════════════════════ |
| adaptive evolution | `python3 engines/lh_adaptive_evolution.py` | 龍魂 · 自适应进化中枢 v1.0 |
| ant colony visual | `python3 engines/lh_ant_colony_visual.py` | 龍魂蚁群分布可视化引擎 v1.0 |
| auto intent | `python3 engines/lh_auto_intent.py` | 龍魂·自动意图识别与执行 v1.0 |
| avatar engine | `python3 engines/lh_avatar_engine.py` | 龍魂 · 数字人引擎 v1.0 — 魔瞳凝视 |
| bao gui | `python3 engines/lh_bao_gui.py` | 龍魂·宝柜 (BaoGui) · 本地加密保险柜引擎 v1.0 |
| base reorganizer | `python3 engines/lh_base_reorganizer.py` | 龍魂 · 底座重组引擎 v1.0 |
| clipboard daemon | `python3 engines/lh_clipboard_daemon.py` | 龍魂·剪贴板意图守护进程 v1.0 |
| csdn auditor | `python3 engines/lh_csdn_auditor.py` | 发布前自动审计内容质量、合规性、标签分类； |
| culture isolation en | `python3 engines/lh_culture_isolation_engine.py` | 龍魂·软文化污染隔离引擎 v1.0 |
| data radar | `python3 engines/lh_data_radar.py` | 龍魂 · 个人数据主权雷达 — 扫描引擎 v1.0 |
| drift monitor | `python3 engines/lh_drift_monitor.py` | 1. 数据漂移检测 - 输入分布变化监控 |
| dual labeler | `python3 engines/lh_dual_labeler.py` | 龍魂·AI内容双标识系统 v1.0 |
| exobrain compressor | `python3 engines/lh_exobrain_compressor.py` | 龍芯⚡️2026-07-25-EXOBRAIN-COMPRESSOR-v2.0 |
| five element audit e | `python3 engines/lh_five_element_audit_engine.py` | 龍魂 · 五行审计决策引擎 v1.0 |
| governance decision  | `python3 engines/lh_governance_decision_chain.py` | 龍芯⚡️2026-07-25-GOVERNANCE-DECISION-CHAIN-v1.0 |
| inference cache | `python3 engines/lh_inference_cache.py` | 1. 精确缓存 - 完全相同的query直接返回缓存 |
| innovation engine | `python3 engines/lh_innovation_engine.py` | 龍魂 · 创新推演引擎 v1.0 |
| inter agent bus | `python3 engines/lh_inter_agent_bus.py` | ╔═════════════════════════════════════════════════ |
| local vault | `python3 engines/lh_local_vault.py` | 龍魂·本地数据保险柜 — 用户数据的最后一道物理防线。 |
| math formula core | `python3 engines/lh_math_formula_core.py` | -*- coding: utf-8 -*- |
| media sovereignty ma | `python3 engines/lh_media_sovereignty_marker.py` | 龍魂·媒体主权标记引擎 v1.0 |
| memory eternity | `python3 engines/lh_memory_eternity.py` | 龍芯⚡️2026-07-25-MEMORY-ETERNITY-v1.0 |
| nano vision engine | `python3 engines/lh_nano_vision_engine.py` | 龍魂纳米视觉引擎 · 多尺度超分辨率重建 |
| natural router | `python3 engines/lh_natural_router.py` | 龍魂·自然语言多引擎路由 v1.0 |
| offline ai | `python3 engines/lh_offline_ai.py` | 龍魂 · 离线AI开关 v3.0 · 三后端架构 |
| pathfinder engine | `python3 engines/lh_pathfinder_engine.py` | 迪杰斯特拉 / A* / 动态规划 / 八卦阵 / 三六九不动点 / D* Lite |
| persona agent | `python3 engines/lh_persona_agent.py` | ╔═════════════════════════════════════════════════ |
| persona orchestra vi | `python3 engines/lh_persona_orchestra_visual.py` | 龍魂20人格协作可视化引擎 v1.0 |
| persona runner | `python3 engines/lh_persona_runner.py` | 龍魂 · PersonaRunner 人格智能体统一运行器 v1.0 |
| privacy breaker | `python3 engines/lh_privacy_breaker.py` | 龍魂 · 隐私熔断器 v1.0 |
| rule engine v4 | `python3 engines/lh_rule_engine_v4.py` | 龍魂规则引擎 v4.1 |
| ruyi migration | `python3 engines/lh_ruyi_migration.py` | CNSH·如意 代码迁移引擎 v1.0 |
| ruyi parser | `python3 engines/lh_ruyi_parser.py` | CNSH·如意 语法解析器 v1.0 |
| ruyi router | `python3 engines/lh_ruyi_router.py` | CNSH·如意 路由引擎 v1.0 |
| seven factor engine | `python3 engines/lh_seven_factor_engine.py` | 龍魂·七因子行为密码学引擎 v1.0 |
| shared blackboard | `python3 engines/lh_shared_blackboard.py` | 龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-SHARED-BLACKBOARD-v1.0""" |
| symbiotic bootstrap  | `python3 engines/lh_symbiotic_bootstrap_engine.py` | 龍魂 · 共生体数据自举引擎 v1.0 |
| symbiotic cognition  | `python3 engines/lh_symbiotic_cognition_engine.py` | 龍魂 · 反奶头乐共生认知理论 · 数学建模仿真引擎 v1.0 |
| system health panora | `python3 engines/lh_system_health_panorama.py` | 龍魂系统健康全景图引擎 v1.0 |
| tao chip | `python3 engines/lh_tao_chip.py` | 龍魂 · 韬定律芯片调度引擎 v1.0 |
| teaching adapter | `python3 engines/lh_teaching_adapter.py` | 龍魂·普惠教学适配器 v1.0 — 画像→tier→温度→输出风格 统一桥接 |
| team orchestrator | `python3 engines/lh_team_orchestrator.py` | 龍魂 · TeamOrchestrator 军团指挥中枢 v2.0 |
| translator | `python3 engines/lh_translator.py` | 龍魂 · 隐语法翻译层 v1.0 |
| voice engine | `python3 engines/lh_voice_engine.py` | 龍魂 · 声音引擎 v1.0 — 老兵腔调 |
### ⚙️ engines/ 引擎 (1 个)

| 触发词 | 命令 | 说明 |
|:---|:---|:---|
| dao ethics anchor | `python3 engines/dao_ethics_anchor.py` | 路径：engines/dao_ethics_anchor.py |
### 🔤 CNSH 中文脚本 (21 个)

| 触发词 | 命令 | 说明 |
|:---|:---|:---|
| CNSH 代码审计引擎 | `python3 bin/CNSH_代码审计引擎.py` | 路径：bin/CNSH_代码审计引擎.py |
| CNSH 内容加工管道 | `python3 bin/CNSH_内容加工管道.py` | 路径：bin/CNSH_内容加工管道.py |
| CNSH 国密工具 | `python3 bin/CNSH_国密工具.py` | 路径：bin/CNSH_国密工具.py |
| CNSH 基础类型 | `python3 bin/CNSH_基础类型.py` | 路径：bin/CNSH_基础类型.py |
| CNSH 多模型颜色一致性 | `python3 bin/CNSH_多模型颜色一致性.py` | CNSH 多模型颜色一致性 v1.0 |
| CNSH 定时任务 | `python3 bin/CNSH_定时任务.py` | 路径：bin/CNSH_定时任务.py |
| CNSH 宝宝指令路由器 | `python3 bin/CNSH_宝宝指令路由器.py` | 听懂老百姓的话，自动拆碎意图，按需调用国密/加密/语义/公式/人格/文章/审计等模板 |
| CNSH 执行器 | `python3 bin/CNSH_执行器.py` | 路径：bin/CNSH_执行器.py |
| CNSH 排序不动点协议 | `python3 bin/CNSH_排序不动点协议.py` | 路径：bin/CNSH_排序不动点协议.py |
| CNSH 收口摘要生成器 | `python3 bin/CNSH_收口摘要生成器.py` | 路径：bin/CNSH_收口摘要生成器.py |
| CNSH 流场可视化引擎 | `python3 bin/CNSH_流场可视化引擎.py` | CNSH 流场可视化引擎 v1.0 |
| CNSH 生态监管协议 | `python3 bin/CNSH_生态监管协议.py` | 路径：bin/CNSH_生态监管协议.py |
| CNSH 目录审计 | `python3 bin/CNSH_目录审计.py` | 路径：bin/CNSH_目录审计.py |
| CNSH 知识库 | `python3 bin/CNSH_知识库.py` | 路径：bin/CNSH_知识库.py |
| CNSH 系统自检 | `python3 bin/CNSH_系统自检.py` | 路径：bin/CNSH_系统自检.py |
| CNSH 规则库 | `python3 bin/CNSH_规则库.py` | 路径：bin/CNSH_规则库.py |
| CNSH 透明语义治理内核 | `python3 bin/CNSH_透明语义治理内核.py` | 路径：bin/CNSH_透明语义治理内核.py |
| CNSH 通知归档 | `python3 bin/CNSH_通知归档.py` | 路径：bin/CNSH_通知归档.py |
| CNSH 颜色不动点协议 | `python3 bin/CNSH_颜色不动点协议.py` | 路径：bin/CNSH_颜色不动点协议.py |
| CNSH 龍魂宝宝指令中枢 | `python3 bin/CNSH_龍魂宝宝指令中枢.py` | 路径：bin/CNSH_龍魂宝宝指令中枢.py |
| CNSH 龍魂护盾 | `python3 bin/CNSH_龍魂护盾.py` | CNSH 龍魂护盾 v1.0 |
### 🚀 deploy/ 部署脚本 (34 个)

| 触发词 | 命令 | 说明 |
|:---|:---|:---|
| connect-kunpeng | `bash deploy/connect-kunpeng.sh` | 🐉 龍魂 · 鲲鹏服务器 mgmt 连接脚本 |
| deploy-appeal-ai | `bash deploy/deploy-appeal-ai.sh` | ══════════════════════════════════════════════════ |
| deploy-frp-panel | `bash deploy/deploy-frp-panel.sh` | ================================================== |
| deploy-frpc-kunpeng | `bash deploy/deploy-frpc-kunpeng.sh` | ================================================== |
| deploy-frpc-mac | `bash deploy/deploy-frpc-mac.sh` | ================================================== |
| deploy-frps | `bash deploy/deploy-frps.sh` | ================================================== |
| deploy-model-watchdo | `bash deploy/deploy-model-watchdog.sh` | 看门狗 + 重训练器 + 验证服务v6 + 面板v5 |
| longhun-bootstrap | `bash deploy/longhun-bootstrap.sh` | ══════════════════════════════════════════════════ |
| openeuler-deploy | `bash deploy/openeuler-deploy.sh` | ══════════════════════════════════════════════════ |
| prepare-openEuler | `bash deploy/prepare-openEuler.sh` | 🐉 龍魂 · openEuler 鲲鹏服务端环境准备脚本 |
| prepare-ubuntu | `bash deploy/prepare-ubuntu.sh` | 🐉 龍魂 · Ubuntu 24.04 华为云服务端环境准备脚本 |
| setup-five-harms | `bash deploy/setup-five-harms.sh` | 🐉 龍魂 · 五害曝光台一键上线 v1.1 |
| setup-systemd | `bash deploy/setup-systemd.sh` | 🐉 龍魂 · systemd 服务 + Nginx 部署配置脚本 |
| cert renewal master | `bash deploy/scripts/cert_renewal_master.sh` | 一键部署钩子+修复timer+测试续期+备份+监控            ║ |
| certbot-deploy-hook | `bash deploy/scripts/certbot-deploy-hook.sh` | ╔═════════════════════════════════════════════════ |
| deploy-dna-server | `bash deploy/scripts/deploy-dna-server.sh` | ============================================ |
| deploy-frp-v3.6 | `bash deploy/scripts/deploy-frp-v3.6.sh` | deploy-frp-v3.6.sh |
| deploy audit to kunp | `bash deploy/scripts/deploy_audit_to_kunpeng.sh` | ══════════════════════════════════════════════════ |
| deploy brain | `bash deploy/scripts/deploy_brain.sh` | ══════════════════════════════════════════════════ |
| deploy full api | `bash deploy/scripts/deploy_full_api.sh` | 龍魂全接口/数据库/API一键部署脚本 |
| deploy kunpeng perfe | `bash deploy/scripts/deploy_kunpeng_perfect.sh` | ================================================== |
| deploy local models | `bash deploy/scripts/deploy_local_models.sh` | 龍魂本地开源模型 · 一键部署脚本 |
| deploy memory api | `bash deploy/scripts/deploy_memory_api.sh` | ═══════════════════════════════════════════════ |
| deploy persona vault | `bash deploy/scripts/deploy_persona_vault_to_kunpeng.sh` | 龍魂·人格路由 + 保险柜 API 鲲鹏部署脚本 |
| deploy radar | `bash deploy/scripts/deploy_radar.sh` | ╔═════════════════════════════════════════════════ |
| deploy visual engine | `bash deploy/scripts/deploy_visual_engines.sh` | 龍魂视觉引擎群 · 鲲鹏一键部署 |
| hk backup sync | `bash deploy/scripts/hk_backup_sync.sh` | #   将鲲鹏服务器的审计日志/DNA注册表/配置文件 |
| install brain | `bash deploy/scripts/install_brain.sh` | ================================================== |
| kunpeng device facto | `bash deploy/scripts/kunpeng_device_factor_collect.sh` | #   采集华为鲲鹏服务器所有硬件指纹因子 |
| longhun circuit brea | `bash deploy/scripts/longhun_circuit_breaker.sh` | 龍魂熔断守护 · longhun-circuit-breaker.sh |
| package turbulence a | `bash deploy/scripts/package_turbulence_arxiv.sh` | 龍魂湍流治理框架 · arXiv 一键打包脚本 |
| remote tail finalize | `bash deploy/scripts/remote_tail_finalizer.sh` | ================================================== |
| trace reconstructor  | `bash deploy/scripts/trace_reconstructor_deploy.sh` | 龍魂·踪迹复原引擎 — 鲲鹏部署脚本 v1.0 |
| upload to huawei obs | `bash deploy/scripts/upload_to_huawei_obs.sh` | ╔═════════════════════════════════════════════════ |
### 📁 其他脚本 (121 个)

| 触发词 | 命令 | 说明 |
|:---|:---|:---|
|  type fixer | `python3 bin/_type_fixer.py` | 智能批量修复 basedpyright reportMissingTypeArgument — v2 |
| agent orchestrator v | `python3 bin/agent_orchestrator_v1.py` | Agent Orchestrator · 15+ Local Agents Integration  |
| apply longhun docume | `python3 bin/apply_longhun_document_template.py` | - 扫描指定目录下的 Markdown 文件。 |
| audit engine | `python3 bin/audit_engine.py` | 龍魂审计引擎 v1.0 — CNSH Audit Engine |
| audit plugin base | `python3 bin/audit_plugin_base.py` | ╔═════════════════════════════════════════════════ |
| bagua router | `python3 bin/bagua_router.py` | ╔═════════════════════════════════════════════════ |
| baobao workflow v2.0 | `python3 bin/baobao_workflow_v2.0.py` | ══════════════════════════════════════════════════ |
| brain notion sync | `python3 bin/brain_notion_sync.py` | - |
| clean-kimi-download- | `python3 bin/clean-kimi-download-duplicates.py` | 清理 Downloads/Kimi_Agent_* 中的重复脚本副本 |
| gateway | `python3 bin/cnsh_gateway.py` | 一个入口 → 路由到 Claude / DeepSeek / 本地Ollama |
| daily review | `python3 bin/daily_review.py` | - 检查核心文件是否存在 |
| deepseek api | `python3 bin/deepseek_api.py` | DeepSeek-V3 API 调用封装（龙魂适配版） |
| deepseek tools | `python3 bin/deepseek_tools.py` | DeepSeek-V3 工具调用 + 龙魂审计集成 |
| dna ecny offline act | `python3 bin/dna_ecny_offline_activation.py` | 路径：bin/dna_ecny_offline_activation.py |
| dna memory layer | `python3 bin/dna_memory_layer.py` | 🧬 UID9622 · DNA记忆连接层 | 跨窗口全域记忆同步系统 v2.0 |
| emotion absorber | `python3 bin/emotion_absorber.py` | 🧽 龍魂·情绪海绵 v1.0 |
| error translator | `python3 bin/error_translator.py` | 🌐 龍魂·错误翻译器 — 系统错误中文提示 |
| family roster adapte | `python3 bin/family_roster_adapter.py` | 路径：bin/family_roster_adapter.py |
| fuse control | `python3 bin/fuse_control.py` | ╔═════════════════════════════════════════════════ |
| ganzhi dna engine | `python3 bin/ganzhi_dna_engine.py` | ╔═════════════════════════════════════════════════ |
| generate-desktop-swi | `python3 bin/generate-desktop-switch.py` | 从 desktop/menu-registry.json 与各模块的 desktop-menu.js |
| generate academic re | `python3 bin/generate_academic_registry.py` | ╔═════════════════════════════════════════════════ |
| generate module read | `python3 bin/generate_module_readmes.py` | 路径：bin/generate_module_readmes.py |
| generate relationshi | `python3 bin/generate_relationship_matrix.py` | 生成龍魂系统对接关系矩阵 Markdown。 |
| generate workspace m | `python3 bin/generate_workspace_metadata.py` | 为已复制到 docs/<workspace>/ 的 Notion 导出文件生成 README.md  |
| init directories | `python3 bin/init_directories.py` | 路径：bin/init_directories.py |
| integrate private sh | `python3 bin/integrate_private_shared_batch2.py` | 整理 Notion 导出工作区 `龍魂技术全站` 到 docs/longhun-tech/。 |
| local assessment eng | `python3 bin/local_assessment_engine.py` | 作者: UID9622 (Claude Code) |
| log operation | `python3 bin/log_operation.py` | 龍魂操作日志记录器 |
| longhun brain | `python3 bin/longhun_brain.py` | ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ |
| longhun click audito | `python3 bin/longhun_click_auditor.py` | 区分人类点击、AI抓取、异常行为，标记追溯本源 |
| longhun dna repair | `python3 bin/longhun_dna_repair.py` | - 扫描孤立文件（无DNA或DNA不完整） |
| longhun launcher sca | `python3 bin/longhun_launcher_scan.py` | 龍魂 · 启动指令清点器  (LongHun Launcher Inventory) |
| longhun mvp executor | `python3 bin/longhun_mvp_executor_v1.0.py` | 龍魂 MVP执行引擎 v1.0 |
| longhun mvp setup in | `python3 bin/longhun_mvp_setup_integration_v1.0.py` | - 一键生成所有配置文件 |
| longhun persona hub | `python3 bin/longhun_persona_hub.py` | 龍魂人格中枢 · LongHun Persona Hub v1.0 |
| longhun relation mat | `python3 bin/longhun_relation_matrix.py` | - 扫描指定目录所有文件 |
| longhun self check v | `python3 bin/longhun_self_check_v1.0.py` | 路径：bin/longhun_self_check_v1.0.py |
| longhun train v2 | `python3 bin/longhun_train_v2.py` | LongHun System - Full Training Pipeline v2.0 |
| longhun wuxing mvp | `python3 bin/longhun_wuxing_mvp.py` | 五行属性推断（木火土金水） |
| longzhi shou v2 | `python3 bin/longzhi_shou_v2.py` | 龍智守 · 本地飞书机器人控制接口 v2.0 |
| module inventory | `python3 bin/module_inventory.py` | 龍魂系统 · 功能模块盘点器 |
| organize longhun tec | `python3 bin/organize_longhun_tech.py` | 整理 Notion 导出工作区 `龍魂技术全站` 到 docs/longhun-tech/。 |
| package-watcher | `python3 bin/package-watcher.py` | 1. 扫描指定监控路径（默认 ~/Downloads 与 ~） |
| parse notion | `python3 bin/parse_notion.py` | 解析 Notion 知识库导出文件，提取知识点信息 |
| parse notion (迁移) | `python3 bin/parse_notion_(迁移).py` | 解析 Notion 知识库导出文件，提取知识点信息 |
| patrol security | `python3 bin/patrol_security.py` | ═══════════════════════════════════════════ |
| persona scheduler | `python3 bin/persona_scheduler.py` | ╔═════════════════════════════════════════════════ |
| plist validator | `python3 bin/plist_validator.py` | - XML 格式完整性检查 |
| read lints | `python3 bin/read_lints.py` | 读取 lint 报告并输出摘要：错误数、警告数、Top 文件、修复建议。 |
| repair template dupl | `python3 bin/repair_template_duplicates.py` | 修复模板套用后的重复标题 |
| run persona api | `python3 bin/run_persona_api.py` | 龍魂人格 API 启动脚本 |
| semantic parser | `python3 bin/semantic_parser.py` | 路径：bin/semantic_parser.py |
| skill extension | `python3 bin/skill_extension.py` | ╔═════════════════════════════════════════════════ |
| sovereign privacy | `python3 bin/sovereign_privacy.py` | - 主权人身份哈希脱敏（SHA-256 → 0x前12位） |
| sync longhun knowled | `python3 bin/sync_longhun_knowledge_desktop.py` | 1. 把龍魂系统的协议、规则、论文、技能、报告等核心文件， |
| syntax lookup | `python3 bin/syntax_lookup.py` | 用法: |
| task manager v2 | `python3 bin/task_manager_v2.py` | Task Manager v2.0 · 支持跳跃式操作 + 自动去重 |
| update private share | `python3 bin/update_private_shared_readme.py` | 根据 docs/private-shared-imports/ 下现有分类目录，重新生成 READM |
| verify memory cnsh | `python3 bin/verify_memory_cnsh.py` | 验证：记忆服务 + CNSH v2.1 解释器 + 执行器链路全部可运行。 |
| web server | `python3 bin/web_server.py` | - 挂载 portal/index.html 作为主页（:8777） |
| wuxing guard | `python3 bin/wuxing_guard.py` | ╔═════════════════════════════════════════════════ |
| xiaoyi hub 8799 | `python3 bin/xiaoyi_hub_8799.py` | -*- coding: utf-8 -*- |
| 守护进程管理器 逐行注释版 | `python3 bin/守护进程管理器_逐行注释版.py` | 安裝 / 啟動 / 停止 / 重啟龍魂系統守護進程 |
| 训练数据优化器 v3.1.0 | `python3 bin/训练数据优化器_v3.1.0.py` | ╔═════════════════════════════════════════════════ |
| 龍智守 本地控制接口 v2.0 | `python3 bin/龍智守_本地控制接口_v2.0.py` | 龍智守 · 本地飞书机器人控制接口 v2.0 |
| 龍魂体系v5-一键启动 | `python3 bin/龍魂体系v5-一键启动.py` | ══════════════════════════════════════════════════ |
| 龍魂审计定价引擎 v1.0 | `python3 bin/龍魂审计定价引擎_v1.0.py` | 龍魂审计定价引擎 + 支付网关 |
| 龍魂审计定价引擎 v2.0 | `python3 bin/龍魂审计定价引擎_v2.0.py` | 龍魂审计定价引擎 v2.0 + 支付网关 + 投资池 |
| 龍魂护盾 v3.0 CNSH中文语法版 | `python3 bin/龍魂护盾_v3.0_CNSH中文语法版.py` | 龍魂护盾 v3.0 — CNSH 中文语法版 |
| 龙魂系统 API接口完整实现 v1.0 | `python3 bin/龙魂系统_API接口完整实现_v1.0.py` | 龙魂系统 API接口完整实现 v1.0 |
| QUICK DNA STATUS | `bash bin/QUICK_DNA_STATUS.sh` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| build-chinese-editor | `bash bin/build-chinese-editor.sh` | 编译龍码中文编辑器桌面 App |
| build-control-center | `bash bin/build-control-center.sh` | 编译龍魂控制中心桌面 App |
| build-desktop-switch | `bash bin/build-desktop-switch.sh` | 根据 desktop/menu-registry.json 与各模块 desktop-menu.js |
| build-release | `bash bin/build-release.sh` | 龍魂系统 · 发布打包脚本 |
| check longhun assess | `bash bin/check_longhun_assessment.sh` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| crawl daodejing | `bash bin/crawl_daodejing.sh` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| deploy activation to | `bash bin/deploy_activation_to_kunpeng.sh` | 部署激活经济 API、激活舱页面、MFA 脚本 |
| deploy longhun opene | `bash bin/deploy_longhun_openeuler.sh` | 龍魂系統 · 華為鯤鵬openEuler部署腳本 |
| deploy pathfinder to | `bash bin/deploy_pathfinder_to_kunpeng.sh` | 部署路径规划 REST API，含 systemd + logrotate + 监控 + 灰度 |
| deploy persona api | `bash bin/deploy_persona_api.sh` | 君子協議: 本文件受龍魂DNA追溯保護 |
| deploy video studio  | `bash bin/deploy_video_studio_to_kunpeng.sh` | 把按钮版视频工坊和数据大屏部署到公网，直接用网页生成视频 |
| dna-generator | `bash bin/dna-generator.sh` | ============================================ |
| install-autostart | `bash bin/install-autostart.sh` | 安装龍魂系统 macOS 开机自启动（LaunchAgent） |
| install-terminal | `bash bin/install-terminal.sh` | 🐉 龍魂终端工具安装脚本 |
| install longhun daem | `bash bin/install_longhun_daemon.sh` | 龍魂 launchd 守护一键装载 · P13姜子牙装载 / P03雯雯复盘 / P05上帝之眼督 |
| list-protocols | `bash bin/list-protocols.sh` | 🐉 列出龍魂协议库全部协议 |
| local search | `bash bin/local_search.sh` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| longhun bark plugin | `bash bin/longhun_bark_plugin.sh` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| longhun crash checkl | `bash bin/longhun_crash_checklist.sh` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| longhun daily assess | `bash bin/longhun_daily_assessment.sh` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| longhun dna verify | `bash bin/longhun_dna_verify.sh` | ============================================ |
| longhun system start | `bash bin/longhun_system_startup_check.sh` | 檢查所有龍魂系統組件的啟動狀態 |
| protocol shield | `bash bin/protocol_shield.sh` | 防止協議被篡改、繞過、或被誘導執行危險操作 |
| refresh-longhun | `bash bin/refresh-longhun.sh` | 龍魂系统一键刷新：重新盘点模块 + 重新生成桌面主开关 |
| restart autoflow | `bash bin/restart_autoflow.sh` | ╔═════════════════════════════════════════════════ |
| run-package-watcher | `bash bin/run-package-watcher.sh` | ══════════════════════════════════════════════════ |
| run-warehouse-audit | `bash bin/run-warehouse-audit.sh` | ══════════════════════════════════════════════════ |
| search usb | `bash bin/search_usb.sh` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| session end | `bash bin/session_end.sh` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| setup alipay sandbox | `bash bin/setup_alipay_sandbox.sh` | 上传密钥、配置沙箱凭证、重启服务 |
| setup daily review | `bash bin/setup_daily_review.sh` | 龍魂每日復盤·一鍵配置腳本 |
| setup daily review a | `bash bin/setup_daily_review_auto.sh` | 龍魂每日複盤·自動配置版本 (非互動式) |
| setup dev | `bash bin/setup_dev.sh` | 创建 venv → 安装依赖 → 初始化数据目录 → 验证环境 |
| setup security | `bash bin/setup_security.sh` | ╔═════════════════════════════════════════════════ |
| setup wechat pay | `bash bin/setup_wechat_pay.sh` | 龍魂激活经济舱 · 微信支付凭证配置向导 |
| show-constitution | `bash bin/show-constitution.sh` | 🐉 显示龍魂系统宪法 |
| show-eternal-lock | `bash bin/show-eternal-lock.sh` | 🐉 显示 P0 永恒锁协议 |
| show-protocol-librar | `bash bin/show-protocol-library.sh` | 🐉 显示龍魂协议库索引 |
| show-standard | `bash bin/show-standard.sh` | 🐉 显示龍魂产出标准 |
| skill-launcher-v3 | `bash bin/skill-launcher-v3.sh` | 君子协议: 本文件受龍魂DNA追溯保护 |
| start longhun api | `bash bin/start_longhun_api.sh` | 龍魂API服务启动脚本 |
| start longzhishou | `bash bin/start_longzhishou.sh` | 龍智守本地控制接口 · 启动脚本 v2.0 |
| start persona api | `bash bin/start_persona_api.sh` | 君子协议: 本文件受龍魂DNA追溯保护 |
| start symbiote | `bash bin/start_symbiote.sh` | ╔═════════════════════════════════════════════════ |
| zshrc 龍魂片段 | `bash bin/zshrc_龍魂片段.sh` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| 启动-claude-bridge | `bash bin/启动-claude-bridge.sh` | ╔═════════════════════════════════════════════════ |
| 启动人格代理 | `bash bin/启动人格代理.sh` | 君子协议: 本文件受龍魂DNA追溯保护 |
| 本地 search | `bash bin/本地_search.sh` | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |
| 龍魂 华为云部署脚本 v1.0 | `bash bin/龍魂_华为云部署脚本_v1.0.sh` | ══════════════════════════════════════════════════ |


## 📂 分类索引

### 🎛️ 日常交互
```
lh                          # 交互控制台（8大类菜单）
lh --dashboard              # 人格仪表盘
lh --audit                  # 一键审计
lh --push                   # 推远端
lh --health                 # 引擎健康
lh --console                # Web操作台
```

### 🔍 搜索 & 知识
```
lh search "关键词"           # → bin/lh_search_engine.py
```

### 🎬 多媒体
```
lh video --script 稿.txt     # → bin/lh_video_studio.py
lh video --list              # → bin/lh_video_index.py
lh 3d --input 图.png         # → bin/lh_3d_pipeline.py

# 主权验证（公开可用·任何人可验）
python3 bin/lh_verify 视频.mp4            # 提取DNA盲水印
python3 bin/lh_verify *.mp4 --json        # JSON格式·批量验证
python3 bin/lh_verify 视频.mp4 --quiet    # 静默模式（返回退出码）

# 高级视频（真声+增强）
lh video --script 稿.txt --voice uid9622 --enhance nano --name "标题"

# 蚁群可视化视频
python3 engines/lh_ant_colony_visual.py full -d ants/
# → 然后 lh video --script ants/ant_narration.txt --voice uid9622

# 人格协作视频
python3 engines/lh_persona_orchestra_visual.py full -d personas/
# → 然后 lh video --script personas/persona_narration.txt --voice uid9622
```

### 🎨 视觉引擎群（新增·v4.1.5）
```
# 纳米视觉超分辨率增强
python3 engines/lh_nano_vision_engine.py enhance -i lowres.png -s 4 -o highres.png
python3 engines/lh_nano_vision_engine.py info     # 引擎信息

# 蚁群分布可视化（4图）
python3 engines/lh_ant_colony_visual.py topo      # 蚁后-工蚁拓扑
python3 engines/lh_ant_colony_visual.py heatmap   # 信息素热力
python3 engines/lh_ant_colony_visual.py dashboard # 涌现仪表盘
python3 engines/lh_ant_colony_visual.py narrate   # 解说词

# 人格协作可视化（5图）
python3 engines/lh_persona_orchestra_visual.py heatmap  # 20x20权重热力
python3 engines/lh_persona_orchestra_visual.py graph    # 协作力导向图
python3 engines/lh_persona_orchestra_visual.py audit    # 审计链路
python3 engines/lh_persona_orchestra_visual.py pie      # 四层饼图
python3 engines/lh_persona_orchestra_visual.py narrate  # 解说词

# 系统健康全景图
python3 engines/lh_system_health_panorama.py panorama  # 九宫格全景图
python3 engines/lh_system_health_panorama.py report    # 文本报告
python3 engines/lh_system_health_panorama.py narrate   # 解说词
```

### 🛡️ 审计 & 安全
```
lh audit                     # → bin/lh_full_system_audit.py
python3 bin/lh_deben_audit.py scan    # 德本五问
python3 bin/lh_memory_load.py         # 焊死记忆加载
python3 bin/lh_system_eval.py         # 健康评分
python3 bin/lh_self-heal.py           # 自助修复
python3 bin/longhun_self_check_v1.0.py # 系统自检
python3 bin/lh_align_checker.py       # 🔥对齐复盘·重复函数·缺失DNA·缺失GPG（统一入口: lh --align）
python3 bin/lh_auto_align_daemon.py  # 🔥对齐闭环守护·自动修复·每小时自愈（lh --align fix/daemon）
```

**黑箱审计协议**（P1·v2.0·AI输出五层校验）：
- 协议: `01_protocols/LH-PROMPT-BLACKBOX-AUDIT-v2.0.md`
- 坑位: `01_protocols/LH-BLACKBOX-PITFALLS-v1.0.md`（10坑·3致命/4高危）
- Manifest: `01_protocols/LH-BLACKBOX-AUDIT-MANIFEST-v2.0.json`

### ✍️ GPG 签名 (🔥焊死)
```
python3 bin/lh_gpg_sign.py sign <路径>      # 签名
python3 bin/lh_gpg_sign.py sign --force .   # 强制全签
python3 bin/lh_gpg_sign.py verify <文件>    # 验证
python3 bin/lh_gpg_sign.py scan <目录>      # 扫描未签名
```
密钥: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

### 🛡️ 反詐·彎彎繞繞檢測（新增·v3.0）
```
# 綜合分析（默認·推薦）
python3 bin/lh_anti_fraud_detector.py analyze -t "要分析的文字"

# 彎繞指數
python3 bin/lh_anti_fraud_detector.py wind -t "文字"

# 綜合風險評分
python3 bin/lh_anti_fraud_detector.py score -t "文字"

# 生成反制話術
python3 bin/lh_anti_fraud_detector.py counter -t "對方的話術"

# 批量檢測（每行一條）
python3 bin/lh_anti_fraud_detector.py batch -f comments.txt

# 場景模式
python3 bin/lh_anti_fraud_detector.py analyze -t "..." -c douyin_live
python3 bin/lh_anti_fraud_detector.py analyze -t "..." -c wechat
```
模式庫: `data/anti_fraud_patterns_v3.0.json` (14維度·彎彎繞繞原理)
協議: `01_protocols/LH-BEHAVIOR-CRYPTOGRAPHY-ANTI-FRAUD-v1.0.md`
民間手冊: `01_protocols/LH-ANTI-FRAUD-QUICK-GUIDE-v1.0.md`

### 🚀 部署 & 同步
```
bash deploy/sync-to-kunpeng.sh              # 代码同步鲲鹏
bash deploy/deploy-now.sh                   # 一键部署
bash deploy/scripts/health_check.sh         # 鲲鹏健康检查(Bark)
bash deploy/scripts/monitor_setup.sh        # systemd+监控
python3 bin/lh_auto_cannon.py               # Git全量推送
```

### 🌐 网络限流应对（`bin/lh_network/`）
```
bash bin/lh_network/05_network_fix_all.sh      # 一键检测+修复限流
bash bin/lh_network/01_hk_proxy_setup.sh       # 华为云香港代理部署（首次配置）
bash bin/lh_network/02_auto_proxy.sh           # 终端自动检测限流+切换代理
bash bin/lh_network/03_model_download_mirror.sh # 模型下载国内镜像配置
bash bin/lh_network/04_kunpeng_offline.sh      # 鲲鹏离线节点配置
```
三层防御: 本地v4.0(离线推理) → 香港代理(SOCKS5) → 国内镜像(hf-mirror.com) → 鲲鹏离线(终极兜底)

### 🧠 模型训练
```
python3 bin/lh_lora_trainer_v4.py           # MLX LoRA训练
python3 bin/lh_download_v40_bases.py        # 数据拉取
ollama run longhun-v3.7                     # 主力模型(Qwen2.5-1.5B)
ollama run longhun-v4.0                     # 新底座(Llama-3.1-8B)
```

### 📊 记忆 & 日志
```
lh memory --today                           # 今日执行日志
lh memory --summary                         # 记忆层统计
lh logs --tail 20                           # 聚合日志
```

### 🔧 运维
```
bash bin/start_all.sh                       # 一键启动所有服务
bash bin/refresh-longhun.sh                 # 刷新龍魂环境
lh schedule list                            # 定时任务
lh web                                      # 仪表盘 → :9630
```

---

## 🔌 服务端口

| 端口 | 服务 | 位置 |
|:---:|:---|:---:|
| 9625 | 纳米视觉API | 鲲鹏 |
| 9630 | Web仪表盘 | Mac |
| 9631 | 搜索引擎 | Mac |
| 9636 | 健康全景API | 鲲鹏 |
| 8766 | 知识中枢 | Mac |
| 8771 | 统一记忆 | Mac |
| 8773 | 统一记忆 | 鲲鹏 |
| 8781 | 军团指挥 | Mac |
| 8788 | 视频画廊 | Mac |
| 8899 | 价格审计 | Mac |

---

## 📝 更新日志（增量追加·不覆盖）

| 2026-07-30 | v1.4 | 网络限流应对方案v1.0入库·6文件·部署区新增🌐网络限流应对 | AI |
| 2026-07-30 | v1.3 | 黑箱审计协议v2.0入库·3文件·审计安全区新增黑箱审计协议+坑位分析 | AI |

| 日期 | 变更 | 影响命令 |
|:---|:---|:---|
| 2026-07-29 | 视觉引擎群 v4.1.5上线 | 纳米视觉·蚁群可视化·人格可视化·健康全景 |
| 2026-07-29 | 鲲鹏部署2个新API服务 | :9625(纳米视觉) :9636(健康全景) |
| 2026-07-28 | 命令总目 v1.1 迁至鲲鹏统一入口 | 全部 |
| 2026-07-28 | 鲲鹏API上线: /api/cmd/* | cmd_routes.py |
| 2026-07-28 | GPG签名引擎上线 | `lh_gpg_sign.py` |
| 2026-07-28 | 创建命令总目 v1.0 | 全部 |
