#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸丑·申时·大有-lh-CONSOLE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
#龍芯⚡️丙午·丙申·癸丑·申时·大有-lh-CONSOLE-v1.0
lh — 龍魂统一交互控制台
一个命令进入，按数字操作，不需要记任何命令。

用法:
    lh                  # 进入交互控制台
    lh --quick audit    # 快速跳转到某个模块
    lh --dashboard      # 直接显示人格仪表盘
"""

import os, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# ===== 常量 =====
VERSION = "v1.0"
DNA = "#龍芯⚡️丙午·丙申·癸丑·申时·大有-lh-CONSOLE-v1.0"

# ===== 功能模块定义（分组+描述）=====
MODULES = {
    "🚀 引擎 & 通道": {
        "desc": "AI引擎内核、飞书/微信/Web通道、语义路由",
        "items": [
            {"id": "1", "label": "启动全部通道", "cmd": "python3 引擎/launcher.py --all", "desc": "飞书+微信+Web三个通道同时启动"},
            {"id": "2", "label": "启动Web通道", "cmd": "python3 引擎/launcher.py --web", "desc": "仅启动Web通道(含Widget前端) :9639"},
            {"id": "3", "label": "启动飞书通道", "cmd": "python3 引擎/launcher.py --feishu", "desc": "飞书机器人 :9637"},
            {"id": "4", "label": "引擎健康检查", "cmd": "python3 引擎/launcher.py --health", "desc": "检查所有通道是否在线"},
            {"id": "5", "label": "CLI交互模式", "cmd": "python3 引擎/launcher.py --cli", "desc": "命令行直接对话模式"},
            {"id": "6", "label": "语义路由测试", "cmd": "python3 bin/semantic_parser.py --interactive", "desc": "测试中文/英文语义解析"},
            {"id": "7", "label": "人格编排调度", "cmd": "python3 bin/lh_persona_orchestrator.py --interactive", "desc": "按任务自动分发到对应人格"},
        ]
    },
    "🛡️ 安全 & 审计": {
        "desc": "五色审计、防篡改、一票否决、熔断申诉",
        "items": [
            {"id": "1", "label": "全系统安全巡检", "cmd": "python3 bin/lh_full_system_audit.py", "desc": "一键触发全系统安全扫描"},
            {"id": "2", "label": "三色代码审计", "cmd": "echo '输入要审计的文件路径:' && read fp && python3 -c \"from bin.code_audit import scan; scan('\\$fp')\"", "desc": "审计单个代码文件安全"},
            {"id": "3", "label": "防篡改扫描", "cmd": "echo '输入文本:' && read txt && python3 bin/lh_anti_tamper.py scan \"\\$txt\"", "desc": "外部AI内容熔断检查"},
            {"id": "4", "label": "一票否决查询", "cmd": "python3 bin/lh_fuse_response.py --list", "desc": "查看所有熔断规则"},
            {"id": "5", "label": "熔断申诉", "cmd": "python3 bin/lh_fuse_appeal.py --interactive", "desc": "对熔断判定提出申诉"},
            {"id": "6", "label": "算法审计", "cmd": "python3 bin/lh_algorithm_audit.py", "desc": "审计算法公平性和偏差"},
            {"id": "7", "label": "双重审计引擎", "cmd": "python3 bin/lh_dual_audit_engine.py", "desc": "并行审计提高覆盖"},
            {"id": "8", "label": "🛡️ 上下文安全引擎", "cmd": "python3 bin/lh_safeai.py --inspect \"什么是SQL注入？怎么防范？\"", "desc": "意图分类+七因子审计+P0-P4分层熔断（safe-ai v1.0）"},
            {"id": "9", "label": "⚖️ 公正总裁/审计员", "cmd": "python3 bin/lh_judge.py --content \"请裁决以下争议...\"", "desc": "调用鲲鹏 longhun-judge 模型做公正裁决与三色审计"},
            {"id": "10", "label": "🔄 序列执行引擎", "cmd": "echo '输入待审计文本:' && read txt && python3 bin/lh_seq.py --text \"\\$txt\"", "desc": "SafeAI→KFPP→CSDN→公正总裁 流水线审计"},
        ]
    },
    "🧠 人格 & AI": {
        "desc": "人格查询、编排、记忆、训练、模型评估",
        "items": [
            {"id": "1", "label": "人格列表 & 状态", "cmd": "python3 bin/lh_persona_orchestrator.py --list-personas", "desc": "查看所有人格及落地状态"},
            {"id": "2", "label": "人格健康度报告", "cmd": "python3 bin/lh_persona_report.py", "desc": "各人格活跃度/贡献统计"},
            {"id": "3", "label": "记忆加载", "cmd": "python3 bin/lh_memory_load.py", "desc": "加载用户记忆和上下文"},
            {"id": "4", "label": "记忆管理", "cmd": "python3 bin/lh_memory.py --menu", "desc": "记忆增删改查"},
            {"id": "5", "label": "千问幻觉评分", "cmd": "python3 bin/lh_qwen_hallucination_scorer.py", "desc": "评估AI输出幻觉程度"},
            {"id": "6", "label": "AI防炒作检测", "cmd": "python3 bin/lh_ai_anti_hype.py", "desc": "检测AI相关内容的炒作成分"},
            {"id": "7", "label": "文化觉醒引擎", "cmd": "python3 bin/lh_cultural_awakening.py", "desc": "中华文化内容觉醒检测"},
        ]
    },
    "🧬 DNA & 追溯": {
        "desc": "DNA生成、验证、注册、创新溯源",
        "items": [
            {"id": "1", "label": "生成DNA追溯码", "cmd": "echo '输入内容:' && read txt && python3 bin/hetu_luoshu_dna.py \"\\$txt\"", "desc": "为文本/代码/决策生成DNA"},
            {"id": "2", "label": "统一DNA登记", "cmd": "python3 bin/lh_unified_dna_registry.py --menu", "desc": "物理+虚拟资产统一登记"},
            {"id": "3", "label": "DNA审计验证", "cmd": "python3 bin/lh_unified_dna_audit.py", "desc": "验证DNA登记册完整性"},
            {"id": "4", "label": "创新溯源查询", "cmd": "python3 bin/lh_innovation_tracer.py --menu", "desc": "查谁先自研的某项技术"},
            {"id": "5", "label": "DNA唯一性守卫", "cmd": "python3 bin/lh_dna_uniqueness_guard.py", "desc": "防止DNA重复/冲突"},
            {"id": "6", "label": "DNA登记修复", "cmd": "python3 bin/lh_registry_extend.py", "desc": "批量修复DNA登记问题"},
        ]
    },
    "📊 检测 & 分析": {
        "desc": "水军检测、行为指纹、机器人评分、情绪分析",
        "items": [
            {"id": "1", "label": "水军检测", "cmd": "python3 bin/lh_water_army_detect.py", "desc": "检测文本是否为水军生成"},
            {"id": "2", "label": "行为指纹", "cmd": "python3 bin/lh_habit_fingerprint.py", "desc": "用户行为指纹采集分析"},
            {"id": "3", "label": "机器人评分", "cmd": "python3 bin/lh_robot_score.py", "desc": "判断内容是否AI生成(RobotScore)"},
            {"id": "4", "label": "行为基准测试", "cmd": "python3 bin/lh_behavioral_benchmark.py", "desc": "校准机器人检测模型"},
            {"id": "5", "label": "行为加密验证", "cmd": "python3 bin/lh_behavioral_crypto_verifier.py", "desc": "加密验证行为数据完整性"},
            {"id": "6", "label": "情绪海绵", "cmd": "echo '输入文本:' && read txt && python3 -c \"from bin.emotion_absorber import detect; print(detect('\\$txt'))\"", "desc": "情绪温度检测+降温"},
            {"id": "7", "label": "水军引擎(v2)", "cmd": "python3 bin/lh_behavioral_water_army_engine.py", "desc": "高级水军团伙检测引擎"},
        ]
    },
    "🔗 同步 & 集成": {
        "desc": "Git同步、Notion同步、道引吸收、跨模块联动",
        "items": [
            {"id": "1", "label": "全量Git推送", "cmd": "python3 bin/lh_auto_cannon.py", "desc": "一键同步到GitHub+Gitee+GitCode"},
            {"id": "2", "label": "Notion知识同步", "cmd": "python3 brain_notion_sync.py", "desc": "双向同步本地↔Notion"},
            {"id": "3", "label": "龍魂道引·开源吸收", "cmd": "python3 bin/lh_daoyin.py --menu", "desc": "吸收外部开源代码入系统"},
            {"id": "4", "label": "跨模块联动感知", "cmd": "python3 bin/lh_cross_module_awareness.py", "desc": "变更影响链路分析"},
            {"id": "5", "label": "Claude桥接", "cmd": "python3 bin/lh_claude_bridge.py", "desc": "连接Claude API"},
            {"id": "6", "label": "守恒自动收口", "cmd": "python3 bin/lh_auto_shouheng.py", "desc": "窗口污染检测→新开会话"},
            {"id": "7", "label": "Gitee批量验证", "cmd": "python3 bin/lh_gitee_verify_batch.py", "desc": "批量检查Gitee仓库状态"},
        ]
    },
    "🐜 蚁群 & 涌现": {
        "desc": "蚁群运行时、涌现度量、信息素监控、触角总线",
        "items": [
            {"id": "1", "label": "蚁群仪表盘", "cmd": "python3 bin/lh_ant_colony_daemon.py dashboard", "desc": "实时蚁群状态·涌现E值·种群分布·信息素浓度"},
            {"id": "2", "label": "蚁群HTTP服务", "cmd": "python3 bin/lh_ant_colony_daemon.py serve", "desc": "启动HTTP服务 :9677 提供仪表盘/健康检查/指标"},
            {"id": "3", "label": "蚁群守护进程", "cmd": "python3 bin/lh_ant_colony_daemon.py start", "desc": "后台持续运行蚁群引擎"},
            {"id": "4", "label": "蚁群状态查询", "cmd": "python3 bin/lh_ant_colony_daemon.py status", "desc": "查看蚁群守护进程运行状态"},
            {"id": "5", "label": "蚁群完整指标", "cmd": "python3 bin/lh_ant_colony_daemon.py metrics", "desc": "输出完整 JSON 指标（涌现/信息素/信号/种群）"},
            {"id": "6", "label": "蚁群健康检查", "cmd": "python3 bin/lh_ant_colony_daemon.py health", "desc": "蚁群健康检查 (JSON)"},
            {"id": "7", "label": "蚁群集成测试", "cmd": "python3 engine/ant_colony/integration_test.py", "desc": "7场景集成测试（论文5+融合2）"},
        ]
    },
    "⚙️ 系统 & 运维": {
        "desc": "系统评估、自助修复、定时任务、服务管理",
        "items": [
            {"id": "1", "label": "系统健康评估", "cmd": "python3 bin/lh_system_eval.py", "desc": "全面系统健康评分"},
            {"id": "2", "label": "自助修复", "cmd": "python3 bin/lh_self-heal.py", "desc": "自动检测并修复常见问题"},
            {"id": "3", "label": "定时任务管理", "cmd": "python3 bin/lh_auto_shouheng.py --cron", "desc": "查看/管理定时任务"},
            {"id": "4", "label": "守护进程(v2)", "cmd": "python3 bin/lh_guardian_v2.py", "desc": "系统守护进程管理"},
            {"id": "5", "label": "桌面菜单", "cmd": "cat cnsh/terminal/desktop-menu.json | python3 -m json.tool", "desc": "查看macOS右键菜单配置"},
        ]
    },
    "🌐 外部 & 网络": {
        "desc": "API网关、爬虫治理、本地AI中继、浏览器守护",
        "items": [
            {"id": "1", "label": "AI API网关", "cmd": "python3 bin/lh_ai_gateway.py", "desc": "统一AI模型调用网关"},
            {"id": "2", "label": "本地AI中继", "cmd": "python3 bin/lh_local_ai_relay.py", "desc": "本地Ollama中继代理"},
            {"id": "3", "label": "爬虫治理", "cmd": "python3 bin/lh_crawl_governor.py", "desc": "管理网络爬虫行为"},
            {"id": "4", "label": "浏览器守护", "cmd": "python3 bin/lh_browser_daemon.py", "desc": "浏览器自动化守护进程"},
            {"id": "5", "label": "平台封锁日志", "cmd": "python3 bin/lh_platform_block_logger.py", "desc": "记录平台审查/封锁行为"},
            {"id": "6", "label": "Web3 DNA市场", "cmd": "python3 bin/lh_web3_dna_market_engine.py", "desc": "去中心化DNA资产市场"},
        ]
    },
    "📝 文档 & 知识": {
        "desc": "知识图谱、文档生成、语料构建、站点生成",
        "items": [
            {"id": "1", "label": "知识爬取", "cmd": "python3 bin/lh_knowledge_crawler.py", "desc": "爬取并结构化外部知识"},
            {"id": "2", "label": "训练语料构建", "cmd": "python3 bin/lh_build_training_corpus.py", "desc": "从知识库构建训练数据"},
            {"id": "3", "label": "静态站点生成", "cmd": "python3 bin/lh_site_gen.py", "desc": "从Markdown生成文档网站"},
            {"id": "4", "label": "消化过滤器", "cmd": "python3 bin/lh_digest_filter.py", "desc": "信息消化优先级排序"},
            {"id": "5", "label": "语义上下文引擎", "cmd": "python3 bin/lh_semantic_context_engine.py", "desc": "上下文中提取语义关系"},
            {"id": "6", "label": "反假货检测", "cmd": "python3 bin/lh_anti_counterfeit.py", "desc": "检测仿冒/抄袭内容"},
        ]
    },
    "🌌 璇玑·记忆推演": {
        "desc": "四象闭环·七因子双轨·16人格推演·三六九验真·DNA烙印",
        "items": [
            {"id": "1", "label": "璇玑推演", "cmd": "python3 engines/lh_xuanji_engine.py", "desc": "互动推演·输入问题即可得到溯源+人格推演+验真+烙印"},
            {"id": "2", "label": "深度推演", "cmd": "python3 engines/lh_xuanji_engine.py --deep", "desc": "深度推演·全16人格+更多记忆"},
            {"id": "3", "label": "璇玑状态", "cmd": "python3 engines/lh_xuanji_engine.py --status", "desc": "查看引擎状态·索引·信任分"},
            {"id": "4", "label": "重建索引", "cmd": "python3 engines/lh_xuanji_engine.py --rebuild-index", "desc": "强制重建向量索引"},
        ]
    },
}

# ===== 人格卡片 =====
PERSONAS = {
    "P00": {"name": "文心", "emoji": "📜", "role": "铁律守护者", "status": "🟡", "desc": "锚点守护→铁律解释→永恒锁验证。底座不可变。"},
    "P01": {"name": "诸葛亮", "emoji": "🦅", "role": "决策参谋", "status": "🟢", "desc": "贡献值评估+时间衰减+该留该删判断。"},
    "P02": {"name": "龍芯", "emoji": "🐉", "role": "执行修复", "status": "🟢", "desc": "写代码、修bug、验证跑通。执行引擎。"},
    "P03": {"name": "墨子", "emoji": "⚖️", "role": "公证验真", "status": "🟡", "desc": "接火流程→水印打标→留痕。兼爱非攻。"},
    "P05": {"name": "上帝之眼", "emoji": "👁️", "role": "审计检查", "status": "🟢", "desc": "三色审计→差异报告→DNA生成。全局感知。"},
    "P06": {"name": "数学大师", "emoji": "🔢", "role": "数字根+五行", "status": "🟢", "desc": "数字根+五行八卦+河图洛书计算。"},
    "P11": {"name": "韩非", "emoji": "⚡", "role": "法家规则", "status": "🟡", "desc": "分级主权→借用合规→来源审计。"},
    "P13": {"name": "姜子牙", "emoji": "🎣", "role": "编排调度", "status": "🟡", "desc": "任务入队→五色审计→派发/阻断/重试。"},
    "P14": {"name": "吕蒙", "emoji": "🚢", "role": "部署上线", "status": "🔴", "desc": "部署管理（+一票否决拦截）。"},
    "P15": {"name": "乔前辈", "emoji": "🍎", "role": "自动化桥接", "status": "🟡", "desc": "代码补全→极简自动化→跨生态桥接。"},
    "P77": {"name": "黑天使军团", "emoji": "🛡️", "role": "安全漏洞", "status": "🟡", "desc": "漏洞检测→风险评估→自动修复。攻防一体。"},
}

# ===== 引擎能力 =====
ENGINE_CAPS = [
    ("系统状态", "P02", "系统状态 / 怎么样"),
    ("人格查询", "P05", "人格 P01 / top5 / 健康度"),
    ("安全审计", "P77", "安全检查 / 审计一下"),
    ("五行数字根", "P06", "算一下 369 / 属什么"),
    ("路由查找", "P13", "节点在哪 IPA-001"),
    ("DNA追溯", "P05", "查DNA / 验证DNA"),
    ("道德经", "P05", "上善若水 / 第X章"),
    ("流场协同", "P13", "看看协同场 / 怎么分工"),
    ("贡献值评估", "P01", "该留该删 / 还顶用吗"),
    ("熔断查询", "P05", "申诉 / 凭什么拒绝"),
    ("璇玑推演", "P01+P06", "璇玑 / 推演 / 追溯"),
    ("帮助", "P02", "帮助 / 怎么用"),
]

def clear_screen():
    try:
        os.system('clear' if os.name == 'posix' else 'cls')
    except Exception:
        print("\n" * 3)

def _term_width():
    try:
        return os.get_terminal_size().columns
    except Exception:
        return 80

def print_header():
    w = _term_width()
    print(f"\n{'='*min(w,100)}")
    print(f"  🐉  龍魂统一控制台 {VERSION}")
    print(f"  📍 UID9622 · 诸葛鑫 · Lucky")
    print(f"  🧬 {DNA}")
    print(f"  📦 已注册能力: {len(ENGINE_CAPS)}项 · 人格: {len(PERSONAS)}个 · 命令: 103+")
    print(f"{'='*min(w,100)}")

def print_menu():
    print(f"\n  📋 功能模块（输入数字进入）：\n")
    categories = list(MODULES.keys())
    for i, cat in enumerate(categories, 1):
        m = MODULES[cat]
        print(f"  [{i}] {cat}")
        print(f"      {m['desc']}")
    print(f"\n  [P] 人格仪表盘 — 查看所有人格能力+联动关系")
    print(f"  [E] 引擎能力表 — 查看引擎11项能力+触发词")
    print(f"  [W] Web操作台 — 打开可视化网页后台（点一点就能操作）")
    print(f"  [H] 帮助 + 快捷命令")
    print(f"  [Q] 退出")
    print()

def print_persona_dashboard():
    clear_screen()
    print_header()
    print(f"\n  🧠 人格仪表盘（落地状态: 🟢=已落地 🟡=部分落地 🔴=未落地）\n")
    print(f"  {'ID':<6}{'姓名':<12}{'角色':<12}{'状态':<6}能力描述")
    print(f"  {'-'*80}")
    for pid, p in PERSONAS.items():
        print(f"  {pid:<6}{p['emoji']} {p['name']:<9}{p['role']:<12}{p['status']:<6}{p['desc']}")

    print(f"\n  🔗 人格联动关系：")
    print(f"  ┌─────────────────────────────────────────────────────────────┐")
    print(f"  │  P00 文心 ←→ P05 上帝之眼  → 铁律解释 + 审计验证          │")
    print(f"  │  P01 诸葛 ←→ P06 数学大师 → 决策 + 数字根计算             │")
    print(f"  │  P02 龍芯 ←→ P15 乔前辈   → 执行修复 + 自动化桥接         │")
    print(f"  │  P05 上帝 ←→ P77 黑天使   → 审计扫描 + 漏洞修复           │")
    print(f"  │  P13 姜尚 ←→ P01 诸葛     → 任务编排 + 决策评估           │")
    print(f"  │  P11 韩非 ←→ P00 文心     → 规则判定 + 铁律锚定           │")
    print(f"  └─────────────────────────────────────────────────────────────┘")

    print(f"\n  📊 意图→人格路由速查：")
    routes = [
        ("检查/审计/安全吗", "P05 上帝之眼", "三色审计"),
        ("修一下/改好", "P02 龍芯", "执行修复"),
        ("算一下/属什么性", "P06 数学大师", "数字根+五行"),
        ("值不值得/过期了没", "P01 诸葛亮", "贡献值+时间衰减"),
        ("自动化/乔接", "P15 乔前辈", "极简自动化"),
        ("同步/联动", "P13 姜子牙", "归档索引"),
        ("漏洞/渗透", "P77 黑天使", "漏洞检测"),
        ("铁律/规矩/宪法", "P00 文心", "锚点守护"),
        ("心情/难过/太棒了", "P00+P03", "情绪海绵"),
    ]
    for intent, persona, action in routes:
        print(f"  \"{intent}\" → {persona} ({action})")

    input(f"\n  ⏎ 按回车返回主菜单...")

def print_engine_caps():
    clear_screen()
    print_header()
    print(f"\n  🚀 引擎已注册能力（共{len(ENGINE_CAPS)}项）\n")
    print(f"  {'#':<4}{'能力':<16}{'人格':<8}触发词")
    print(f"  {'-'*70}")
    for i, (cap, persona, triggers) in enumerate(ENGINE_CAPS, 1):
        print(f"  {i:<4}{cap:<16}{persona:<8}{triggers}")

    print(f"\n  🌐 通道状态：")
    print(f"  ┌──────────┬───────┬─────────────────────────┐")
    print(f"  │ 通道     │ 端口   │ 状态                    │")
    print(f"  ├──────────┼───────┼─────────────────────────┤")
    print(f"  │ 🐦 飞书  │ :9637 │ python3 引擎/launcher.py --feishu │")
    print(f"  │ 💬 微信  │ :9638 │ python3 引擎/launcher.py --wechat │")
    print(f"  │ 🌐 Web   │ :9639 │ python3 引擎/launcher.py --web    │")
    print(f"  │ 💻 CLI   │ 终端   │ python3 引擎/launcher.py --cli    │")
    print(f"  └──────────┴───────┴─────────────────────────┘")

    input(f"\n  ⏎ 按回车返回主菜单...")

def print_help():
    clear_screen()
    print_header()
    print(f"""
  🆘 帮助 & 快捷命令

  日常最常用的几个命令：

    lh                  → 进入这个控制台（终端版）
    lh --console        → 启动可视化Web操作台（网页版·点一点就能操作）
    lh --dashboard      → 直接看人格仪表盘
    lh --engine         → 直接看引擎能力
    lh --audit          → 一键全系统安全审计
    lh --push           → 一键推送全部远端仓库
    lh --health         → 引擎+通道健康检查
    lh --personas       → 人格列表+状态
    lh "查一下语义抽屉"  → 自然语言路由，自动触发相关引擎
    lh ask "人参的功效" → 同上（显式自然语言入口）
    lh analyze "..."    → 自动意图分析（dry-run，只看不执行）
    lh run "..."        → 自动意图分析 + 自动执行引擎/人格/动作
    lh chat             → 对话模式，每句输入自动分析触发
    lh auto             → 剪贴板守护，复制粘贴自动触发

  不用记命令：输入 lh 然后按数字就行。
  也可以直接说人话：lh "去年318路上的事" 会自动调用璇玑推演。
  所有功能都有描述，看到啥选啥。

  💡 新功能：在 lh 主菜单按 [W] 一键打开可视化网页后台
    或者直接执行: lh --console / lh-console / 操作台

  常见问题：
  Q: 某个模块怎么用？
  A: 进对应分类，选定后会显示执行的命令和说明。

  Q: 怎么知道人格是做什么的？
  A: 主菜单按 [P] 进入人格仪表盘。

  Q: 怎么可视化操作？
  A: 主菜单按 [W] 打开Web操作台，浏览器里点一点就行。

  Q: 端口冲突怎么办？
  A: 引擎通道默认用 :9637-:9639，冲突时自动找下一个可用端口。

  Q: 怎么加新功能？
  A: 编辑 bin/lh.py，在 MODULES 字典加条目即可。
""")
    input(f"  ⏎ 按回车返回主菜单...")

def show_category(cat_name):
    """显示某个分类下的子菜单"""
    while True:
        clear_screen()
        print_header()
        cat = MODULES[cat_name]
        print(f"\n  📂 {cat_name}")
        print(f"  📝 {cat['desc']}\n")
        for item in cat['items']:
            print(f"  [{item['id']}] {item['label']}")
            print(f"      {item['desc']}")

        print(f"\n  [B] 返回主菜单")
        print(f"  [Q] 退出")

        choice = input(f"\n  🎯 选一个 > ").strip().lower()

        if choice == 'q':
            return 'quit'
        elif choice == 'b':
            return 'back'

        # 找到对应的命令
        for item in cat['items']:
            if item['id'] == choice:
                print(f"\n  ⚡ 执行: {item['label']}")
                print(f"  💻 命令: {item['cmd']}")
                print()
                yn = input("  确认执行? [Y/n] ").strip().lower()
                if yn in ('', 'y', 'yes'):
                    print(f"\n  {'='*60}")
                    os.system(f"cd {ROOT} && {item['cmd']}")
                    print(f"\n  {'='*60}")
                    print(f"  ✅ 执行完毕")
                else:
                    print("  ⏭️ 已跳过")
                input(f"\n  ⏎ 按回车继续...")
                break
        else:
            print(f"\n  ❌ 无效选择: {choice}")
            time.sleep(1)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='龍魂统一控制台')
    parser.add_argument('--dashboard', action='store_true', help='人格仪表盘')
    parser.add_argument('--engine', action='store_true', help='引擎能力表')
    parser.add_argument('--help-flag', dest='show_help', action='store_true', help='帮助')
    parser.add_argument('--personas', action='store_true', help='人格列表')
    parser.add_argument('--audit', action='store_true', help='一键全系统安全审计')
    parser.add_argument('--push', action='store_true', help='一键推送全部远端')
    parser.add_argument('--health', action='store_true', help='引擎健康检查')
    parser.add_argument('--console', action='store_true', help='启动可视化Web操作台')
    parser.add_argument('--xuanji', type=str, nargs='?', const='--status', 
                        help='璇玑记忆推演 (带参数=查询 / 无参数=状态)')
    parser.add_argument('--safeai', type=str, nargs='?', const='--status',
                        help='上下文安全引擎 (带参数=检测文本 / 无参数=状态)')
    parser.add_argument('--judge', type=str, nargs='?', const='--status',
                        help='公正总裁/审计员 (带参数=裁决内容 / 无参数=健康检查)')
    parser.add_argument('--seq', type=str, nargs='?', const='',
                        help='序列执行引擎 (带参数=审计文本 / 无参数=帮助)')
    parser.add_argument('--quick', type=str, help='快速跳转到模块名')

    args = parser.parse_args()

    # 快捷模式
    if args.dashboard:
        print_persona_dashboard()
        return
    if args.engine:
        print_engine_caps()
        return
    if args.show_help:
        print_help()
        return
    if args.personas:
        print_persona_dashboard()
        return
    if args.audit:
        print_header()
        print("\n  🛡️ 启动全系统安全审计...\n")
        os.system(f"cd {ROOT} && python3 bin/lh_full_system_audit.py")
        return
    if args.push:
        print_header()
        print("\n  🚀 一键推送全部远端仓库...\n")
        os.system(f"cd {ROOT} && python3 bin/lh_auto_cannon.py")
        return
    if args.xuanji is not None:
        print_header()
        import sys, subprocess
        xuanji_path = ROOT / "engines" / "lh_xuanji_engine.py"
        # 优先使用项目虚拟环境，确保 chromadb 等依赖可用
        venv_python = ROOT / ".venv" / "bin" / "python3"
        python_cmd = str(venv_python) if venv_python.exists() else "python3"
        if args.xuanji == '--status':
            print("\n  🌌 璇玑引擎状态\n")
            sys.stdout.flush()
            subprocess.run([python_cmd, str(xuanji_path), "--status"])
        else:
            query = args.xuanji
            print(f"\n  🌌 璇玑推演: {query}\n")
            sys.stdout.flush()
            subprocess.run([python_cmd, str(xuanji_path), query])
        return
    if args.safeai is not None:
        print_header()
        import sys, subprocess
        safeai_path = ROOT / "bin" / "lh_safeai.py"
        if args.safeai == '--status':
            print("\n  🛡️ 上下文安全引擎状态\n")
            sys.stdout.flush()
            subprocess.run(["python3", str(safeai_path), "--status"])
        else:
            query = args.safeai
            print(f"\n  🛡️ 上下文安全检测: {query}\n")
            sys.stdout.flush()
            subprocess.run(["python3", str(safeai_path), "--inspect", query])
        return
    if args.judge is not None:
        print_header()
        import sys, subprocess
        judge_path = ROOT / "bin" / "lh_judge.py"
        if args.judge == '--status':
            print("\n  ⚖️ 公正总裁/审计员 API 健康\n")
            sys.stdout.flush()
            subprocess.run(["python3", str(judge_path), "--health"])
        else:
            query = args.judge
            print(f"\n  ⚖️ 公正总裁裁决: {query}\n")
            sys.stdout.flush()
            subprocess.run(["python3", str(judge_path), "--content", query])
        return
    if args.seq is not None:
        print_header()
        import sys, subprocess
        seq_path = ROOT / "bin" / "lh_seq.py"
        if args.seq == '':
            print("\n  🔄 序列执行引擎\n")
            sys.stdout.flush()
            subprocess.run(["python3", str(seq_path), "--help"])
        else:
            query = args.seq
            print(f"\n  🔄 序列执行: {query}\n")
            sys.stdout.flush()
            subprocess.run(["python3", str(seq_path), "--text", query])
        return
    if args.health:
        print_header()
        print("\n  💓 引擎健康检查...\n")
        os.system(f"cd {ROOT} && python3 引擎/launcher.py --health")
        return
    if args.console:
        print_header()
        print("\n  🖥️ 正在启动 Web 可视化操作台...")
        print("     浏览器打开: http://127.0.0.1:9622/static/index.html")
        try:
            import subprocess
            subprocess.Popen(['python3', f'{ROOT}/control-panel/main.py'],
                cwd=f'{ROOT}/control-panel', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            import time; time.sleep(1.5)
            subprocess.Popen(['open', 'http://127.0.0.1:9622/static/index.html'])
            print("     ✅ 已打开浏览器\n")
        except Exception as e:
            print(f"     ⚠️ 自动打开失败: {e}")
            print(f"     请手动执行: python3 control-panel/main.py\n")
        return

    # 快速跳转到某个模块
    if args.quick:
        qmap = {
            'audit': '🛡️ 安全 & 审计', 'security': '🛡️ 安全 & 审计',
            'engine': '🚀 引擎 & 通道', 'ai': '🚀 引擎 & 通道',
            'persona': '🧠 人格 & AI', 'personas': '🧠 人格 & AI',
            'dna': '🧬 DNA & 追溯',
            'detect': '📊 检测 & 分析', 'analyze': '📊 检测 & 分析',
            'sync': '🔗 同步 & 集成', 'git': '🔗 同步 & 集成',
            'system': '⚙️ 系统 & 运维', 'ops': '⚙️ 系统 & 运维',
            'network': '🌐 外部 & 网络', 'web': '🌐 外部 & 网络',
            'docs': '📝 文档 & 知识',
        }
        cat = qmap.get(args.quick.lower())
        if cat:
            show_category(cat)
        else:
            print(f"  ❌ 未知模块: {args.quick}，可用: {', '.join(qmap.keys())}")
        return

    # 主循环
    while True:
        clear_screen()
        print_header()
        print_menu()

        choice = input("  🎯 输入数字/字母 > ").strip().lower()

        if choice == 'q':
            print("\n  👋 龍魂在，随时回来。")
            break
        elif choice == 'p':
            print_persona_dashboard()
        elif choice == 'e':
            print_engine_caps()
        elif choice == 'w':
            print(f"\n  🖥️ 正在启动 Web 操作台...")
            print(f"     浏览器打开: http://127.0.0.1:9622/static/index.html")
            print(f"     快捷命令: lh-console")
            try:
                import subprocess
                subprocess.Popen(['python3', f'{ROOT}/control-panel/main.py'],
                    cwd=f'{ROOT}/control-panel', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                import time; time.sleep(1)
                subprocess.Popen(['open', 'http://127.0.0.1:9622/static/index.html'])
                print(f"     ✅ 已打开浏览器")
            except Exception as e:
                print(f"     ⚠️ 自动打开失败: {e}")
                print(f"     请手动执行: lh-console")
        elif choice == 'h':
            print_help()
        elif choice.isdigit():
            idx = int(choice) - 1
            categories = list(MODULES.keys())
            if 0 <= idx < len(categories):
                result = show_category(categories[idx])
                if result == 'quit':
                    print("\n  👋 龍魂在，随时回来。")
                    break
            else:
                print(f"\n  ❌ 没有 {choice} 这个选项，请选 1-{len(categories)}")
                time.sleep(1)
        else:
            print(f"\n  ❌ 无效输入: {choice}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  👋 龍魂在，随时回来。")
    except EOFError:
        print("\n")
