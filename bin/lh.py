# DNA: #龍芯⚡️丙午·乙未·乙丑·小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
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

import json, os, sys, time, shlex, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "bin"))  # bin/ 优先，确保 lh_lifecycle 等模块可导入
sys.path.insert(0, str(ROOT))

# ===== 常量 =====
VERSION = "v1.0"
DNA = "#龍芯⚡️丙午·丙申·癸丑·申时·大有-lh-CONSOLE-v1.0"

# ===== 功能模块定义（分组+描述）=====
MODULES = {
    "🧠 统一中枢 · 2,723引擎调度": {
        "desc": "全项目引擎注册表·智能路由·状态全景·去重归集",
        "items": [
            {"id": "1", "label": "🧠 进入统一中枢控制台", "cmd": "python3 bin/lh_unified_brain.py", "desc": "交互式控制台·全引擎调度·一步到位"},
            {"id": "2", "label": "📊 全系统状态面板", "cmd": "python3 bin/lh_unified_brain.py status", "desc": "2,723脚本·109万行代码·一键全景"},
            {"id": "3", "label": "🔍 搜索引擎", "cmd": "python3 bin/lh_unified_brain.py find", "desc": "按关键词搜索任意引擎（lh brain find <关键词>）"},
            {"id": "4", "label": "🧭 智能意图路由", "cmd": "python3 bin/lh_unified_brain.py route", "desc": "自然语言描述意图→自动匹配引擎（lh brain route <意图>）"},
            {"id": "5", "label": "🏥 健康检查", "cmd": "python3 bin/lh_unified_brain.py health", "desc": "DNA签名率·冗余检测·API端口冲突"},
            {"id": "6", "label": "🔄 冗余检测", "cmd": "python3 bin/lh_unified_brain.py dupes", "desc": "检测多版本重复脚本（675组）"},
            {"id": "7", "label": "🔄 重新扫描注册表", "cmd": "python3 bin/lh_unified_brain.py scan", "desc": "强制重新扫描全项目注册引擎"},
        ]
    },
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
        "desc": "五色审计、防篡改、一票否决、熔断申诉、主权守护",
        "items": [
            {"id": "1", "label": "🔴🐉 主权守护验证", "cmd": "python3 bin/lh_sovereignty_guard.py validate", "desc": "法律边界+一票否决+数据主权三合一验证"},
            {"id": "2", "label": "🐉 主权守护状态", "cmd": "python3 bin/lh_sovereignty_guard.py status", "desc": "查看主权宪法·否决权·数据主权状态"},
            {"id": "3", "label": "🐉 主权操作检查", "cmd": "python3 bin/lh_sovereignty_guard.py check \"操作描述\" --context '{}'", "desc": "检查任意操作是否符合法律边界+数据主权"},
            {"id": "4", "label": "🔴 激活一票否决", "cmd": "python3 bin/lh_sovereignty_guard.py veto activate --reason \"维护\"", "desc": "冻结所有系统操作（仅UID9622可执行）"},
            {"id": "5", "label": "全系统安全巡检", "cmd": "python3 bin/lh_full_system_audit.py", "desc": "一键触发全系统安全扫描"},
            {"id": "6", "label": "三色代码审计", "cmd": "python3 bin/lh_code_audit_cli.py", "desc": "审计单个代码文件安全（交互式输入路径）"},
            {"id": "7", "label": "防篡改扫描", "cmd": "python3 bin/lh_anti_tamper.py scan", "desc": "外部AI内容熔断检查（交互式输入文本）"},
            {"id": "8", "label": "一票否决查询", "cmd": "python3 bin/lh_fuse_response.py --list", "desc": "查看所有熔断规则"},
            {"id": "9", "label": "熔断申诉", "cmd": "python3 bin/lh_fuse_appeal.py --interactive", "desc": "对熔断判定提出申诉"},
            {"id": "10", "label": "算法审计", "cmd": "python3 bin/lh_algorithm_audit.py", "desc": "审计算法公平性和偏差"},
            {"id": "11", "label": "双重审计引擎", "cmd": "python3 bin/lh_dual_audit_engine.py", "desc": "并行审计提高覆盖"},
            {"id": "12", "label": "🛡️ 上下文安全引擎", "cmd": "python3 bin/lh_safeai.py --inspect \"什么是SQL注入？怎么防范？\"", "desc": "意图分类+七因子审计+P0-P4分层熔断（safe-ai v1.0）"},
            {"id": "13", "label": "⚖️ 公正总裁/审计员", "cmd": "python3 bin/lh_judge.py --content \"请裁决以下争议...\"", "desc": "调用鲲鹏 longhun-judge 模型做公正裁决与三色审计"},
            {"id": "14", "label": "🔄 序列执行引擎", "cmd": "python3 bin/lh_seq.py", "desc": "SafeAI→KFPP→CSDN→公正总裁 流水线审计（交互式输入文本）"},
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
            {"id": "1", "label": "生成DNA追溯码", "cmd": "python3 bin/hetu_luoshu_dna.py dr", "desc": "为文本/代码/决策生成DNA（交互式输入文本）"},
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
            {"id": "6", "label": "情绪海绵", "cmd": "python3 bin/lh_emotion_cli.py", "desc": "情绪温度检测+降温（交互式输入文本）"},
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
        subprocess.run(['clear'] if os.name == 'posix' else ['cls'], check=False)
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
    print(f"  📦 已注册能力: {len(ENGINE_CAPS)}项 · 人格: {len(PERSONAS)}个 · 命令: 120+")
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

def _run_fixed_cmd(cmd: str):
    """执行固定命令（无用户输入），全部走 subprocess.run(shell=False)。"""
    # 特殊处理：cat file | python3 -m json.tool 这类固定管道
    if cmd.startswith("cat ") and "| python3 -m json.tool" in cmd:
        file_part = cmd[4:].split("|", 1)[0].strip()
        try:
            path = ROOT / file_part
            data = json.loads(path.read_text(encoding="utf-8"))
            print(json.dumps(data, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"  ⚠️ 读取或解析 JSON 失败: {e}", file=sys.stderr)
        return

    try:
        args = shlex.split(cmd)
    except Exception:
        args = cmd.split()
    if not args:
        return
    subprocess.run(args, cwd=str(ROOT), check=False)


# ===== 子命令调度表（一行一个新功能）=====
# 格式: flag_name → (script, emoji, description, [default_args], [smart_default])
# smart_default: 当用户传自由文本时自动插入的子命令（如 search engine 需要 "search" 子命令）
SUB_DISPATCH = {
    'search':               ('lh_search_engine.py',           '🔍', '搜索引擎', [], 'search'),
    'video':                ('lh_video_studio.py',            '🎬', '视频工坊'),
    'pipeline_3d':           ('lh_3d_pipeline.py',             '🎨', '3D管线'),
    'browser':              ('lh_browser_historian.py',       '📖', '浏览器史官'),
    'cnsh':                 ('cnsh_compiler.py',              '🀄', 'CNSH编译器'),
    'cnsh_runtime':         ('lh_cnsh_runtime.py',            '⚡', 'CNSH运行时', [], 'status'),
    'cnsh_complete':        ('cnsh_complete.py',              '☯️', 'CNSH完整版', [], '--interactive'),
    'cnsh_editor':          ('cnsh_editor.py',                '✏️', 'CNSH编辑器'),
    'cnsh_translator':      ('lh_cnsh_translator.py',         '🌐', 'CNSH翻译', [], '--interactive'),
    'cnsh_ui':              ('cnsh_ui.py',                    '🖥️', 'CNSH UI'),
    'seven_dimension':      ('lh_seven_dimension_engine_v2.py','🌌', '七维推演引擎', [], '--interactive'),
    'three_color':          ('lh_three_color_audit.py',       '🔴', '三色审计引擎', [], 'audit'),
    'regulatory':           ('lh_regulatory_firewall.py',     '🔥', '监管防火墙'),
    'governance':           ('governance_engine.py',           '⚖️', '治理降级引擎', [], '--interactive'),
    'governance_check':     ('uid9622_governance.py',          '🏛️', '治理总控台'),
    'entry_test':           ('lh_entry_test_runner.py',       '🧪', '入口测试执行器'),
    'digital_twin':         ('lh_digital_twin.py',            '👥', '数字孪生体', [], '--status'),
    'feed_baby':            ('lh_feed_baby.py',               '🍼', '投喂宝宝优化'),
    'intent':               ('lh_intent_engine.py',           '🧿', '意念交流引擎', [], '--interactive'),
    'dynamic_goal':         ('lh_dynamic_goal.py',            '🎯', '动态目标引擎', [], '--interactive'),
    'capability':           ('lh_capability_scheduler.py',    '📋', '能力调度器', [], '--interactive'),
    'universal_completion': ('universal_completion.py',       '🔮', '万能补全引擎', [], '--interactive'),
    'mirror_index':         ('lh_mirror_index.py',            '🪞', '镜像指数扫描'),
    'dna_validate':         ('dna_validate.py',               '🧬', 'DNA校验器'),
    'triple_audit':         ('lh_triple_audit_gate.py',       '🚦', '三重审计闸'),
    'weight':               ('lh_weight_algorithm.py',        '⚖️', '权重算法'),
    'tongxinyi':            ('lh_tongxinyi_translator.py',    '💬', '通心译翻译'),
    'san_cai':              ('san_cai_v2.py',                 '☯️', '三才算法', [], '--interactive'),
    'ant_colony':           ('lh_ant_colony_daemon.py',       '🐜', '蚁群引擎'),
    'update':               ('lh_engine_registry.py',         '🔄', '更新引擎索引', ['scan']),
    'status':               ('lh_unified_brain.py',           '📊', '全系统状态', ['status']),
}


def _run_subcommand(script_name: str, extra_args: list = None, emoji: str = '🚀', label: str = '',
                    smart_default: str = ''):
    """统一子命令执行器
    - 如果 extra_args 不为空且第一个参数不是 -(flags)，且定义了 smart_default → 自动插入默认子命令
    """
    script_path = ROOT / "bin" / script_name
    print_header()
    if label:
        print(f"\n  {emoji} {label}")
    args_list = [sys.executable, str(script_path)]

    if extra_args:
        # 智能插入：第一个参数不是 flag 且设有 smart_default
        if smart_default and extra_args and not extra_args[0].startswith('-'):
            args_list.append(smart_default)
        args_list.extend(extra_args)
    subprocess.run(args_list, cwd=str(ROOT), check=False)


def _run_interactive_item(item: dict):
    """执行需要交互式用户输入的菜单项，杜绝 shell 拼接。"""
    label = item["label"]

    if label == "三色代码审计":
        fp = input("  输入要审计的文件路径: ").strip()
        if not fp:
            print("  ⏭️ 已跳过")
            return
        subprocess.run([
            "python3", str(ROOT / "bin" / "lh_code_audit_cli.py"), "--path", fp
        ], cwd=str(ROOT), check=False)
        return

    if label == "情绪海绵":
        txt = input("  输入文本: ").strip()
        if not txt:
            print("  ⏭️ 已跳过")
            return
        subprocess.run([
            "python3", str(ROOT / "bin" / "lh_emotion_cli.py"), "--text", txt
        ], cwd=str(ROOT), check=False)
        return

    if label == "🔄 序列执行引擎":
        txt = input("  输入待审计文本: ").strip()
        if not txt:
            print("  ⏭️ 已跳过")
            return
        subprocess.run([
            "python3", str(ROOT / "bin" / "lh_seq.py"), "--text", txt
        ], cwd=str(ROOT), check=False)
        return

    if label == "防篡改扫描":
        txt = input("  输入文本: ").strip()
        if not txt:
            print("  ⏭️ 已跳过")
            return
        subprocess.run([
            "python3", str(ROOT / "bin" / "lh_anti_tamper.py"), "scan", "--", txt
        ], cwd=str(ROOT), check=False)
        return

    if label == "生成DNA追溯码":
        txt = input("  输入内容: ").strip()
        if not txt:
            print("  ⏭️ 已跳过")
            return
        subprocess.run([
            "python3", str(ROOT / "bin" / "hetu_luoshu_dna.py"), "dr", "--", txt
        ], cwd=str(ROOT), check=False)
        return

    # 其他未识别的交互项，按固定命令执行
    _run_fixed_cmd(item["cmd"])


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
                    _run_interactive_item(item)
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
    parser.add_argument('--sovereignty', type=str, nargs='*',
                        help='主权守护引擎 (validate/status/check ""/veto activate/deactivate)')
    parser.add_argument('--align', type=str, nargs='*',
                        help='对齐闭环 (check/fix/status/daemon/dry-run)')
    parser.add_argument('--run', nargs=argparse.REMAINDER, help='自然语言执行命令 (lh --run "健康检查" --dry-run)')
    parser.add_argument('--complete', type=str, help='命令自动补全 (lh --complete "部")')
    parser.add_argument('--repo', nargs=argparse.REMAINDER, help='开源项目模板生成 (lh --repo 或 lh --repo --dry-run 或 lh --repo -o ~/my-project)')
    parser.add_argument('--dna', nargs=argparse.REMAINDER, help='DNA生成与管理 (lh --dna generate/lookup/inherit/family/verify/stats)')
    parser.add_argument('--know', nargs=argparse.REMAINDER, help='本地知识引擎 (lh --know scan/search/convert/status)')
    parser.add_argument('--agent', nargs=argparse.REMAINDER, help='智能体训练 (lh --agent process/interactive/train/status)')
    parser.add_argument('--lu', nargs=argparse.REMAINDER, help='LU压缩引擎 (lh --lu compress/recall/align/index/shortcodes)')
    parser.add_argument('--central', nargs=argparse.REMAINDER, help='UID9622中枢引擎 (lh --central status/task/command/verify/query)')
    parser.add_argument('--brain', nargs=argparse.REMAINDER, help='统一中枢 (lh --brain status/find/run/health/dupes/route)')
    # === 自触发编排引擎 ===
    parser.add_argument('--trigger', metavar='QUERY', type=str, help='自触发编排 (lh --trigger "健康检查") — 说人话→自动找脚本→跑完自动停')
    parser.add_argument('--watch', action='store_true', help='自触发守护模式 (lh --watch) — 后台监听触发')
    parser.add_argument('--watch-daemon', dest='watch_daemon', action='store_true', help='后台守护 (lh --watch-daemon) — 双fork后台')
    parser.add_argument('--ps', action='store_true', help='查看运行中的脚本 (lh --ps)')
    parser.add_argument('--kill-all', dest='kill_all', action='store_true', help='强制终止所有运行中的脚本 (lh --kill-all)')
    parser.add_argument('--batch', type=str, help='批量触发 (lh --batch "健康检查,同步鲲鹏,审计")')
    # === 省电 API 服务 ===
    parser.add_argument('--api', action='store_true', help='启动省电 API 服务 (lh --api) — 全球AI通过HTTP调用')
    parser.add_argument('--api-port', type=int, default=9622, help='API端口 (默认 9622)')
    parser.add_argument('--api-redis', type=str, default='', help='API Redis URL（异步模式）')
    parser.add_argument('--api-key', type=str, default='', help='API认证密钥')
    # === 盘点/省电/语音/启动全部 ===
    parser.add_argument('--inventory', action='store_true', help='功能盘点器 (lh --inventory) — 生成 .inventory.json + 功能清单.md')
    parser.add_argument('--energy', nargs=argparse.REMAINDER, help='省电监控器 (lh --energy 或 lh --energy --watch 仪表盘)')
    parser.add_argument('--voice', nargs=argparse.REMAINDER, help='语音网关 (lh --voice 或 lh --voice --text 文本模式)')
    parser.add_argument('--start-all', dest='start_all', action='store_true', help='一键启动全部服务 (lh --start-all)')
    parser.add_argument('--compare', nargs=argparse.REMAINDER, help='模式对比器 (lh --compare 或 lh --compare --md/--html/--all)')
    # === 调度表子命令（统一处理） ===
    parser.add_argument('--search', nargs=argparse.REMAINDER, help='搜索引擎 (lh --search "关键词")')
    parser.add_argument('--video', nargs=argparse.REMAINDER, help='视频工坊 (lh --video --script 稿.txt)')
    parser.add_argument('--pipeline-3d', '--3d', dest='pipeline_3d', nargs=argparse.REMAINDER, help='3D管线 (lh --3d)')
    parser.add_argument('--browser', nargs=argparse.REMAINDER, help='浏览器史官 (lh --browser collect/search/validate/status)')
    parser.add_argument('--cnsh', nargs=argparse.REMAINDER, help='CNSH编译器 (lh --cnsh -i test.cnsh --run)')
    parser.add_argument('--cnsh-runtime', dest='cnsh_runtime', nargs=argparse.REMAINDER, help='CNSH运行时 (lh --cnsh-runtime status)')
    parser.add_argument('--cnsh-complete', dest='cnsh_complete', nargs=argparse.REMAINDER, help='CNSH完整版 (lh --cnsh-complete --interactive)')
    parser.add_argument('--cnsh-editor', dest='cnsh_editor', nargs=argparse.REMAINDER, help='CNSH编辑器 (lh --cnsh-editor -f input.txt)')
    parser.add_argument('--cnsh-translator', dest='cnsh_translator', nargs=argparse.REMAINDER, help='CNSH翻译 (lh --cnsh-translator -f test.py)')
    parser.add_argument('--cnsh-ui', dest='cnsh_ui', nargs=argparse.REMAINDER, help='CNSH UI (lh --cnsh-ui)')
    parser.add_argument('--seven-dimension', dest='seven_dimension', nargs=argparse.REMAINDER, help='七维推演 (lh --seven-dimension --interactive)')
    parser.add_argument('--three-color', dest='three_color', nargs=argparse.REMAINDER, help='三色审计 (lh --three-color audit --object "...")')
    parser.add_argument('--regulatory', nargs=argparse.REMAINDER, help='监管防火墙 (lh --regulatory --test)')
    parser.add_argument('--governance', nargs=argparse.REMAINDER, help='治理引擎 (lh --governance --interactive)')
    parser.add_argument('--governance-check', dest='governance_check', nargs=argparse.REMAINDER, help='治理总控 (lh --governance-check healthcheck)')
    parser.add_argument('--entry-test', dest='entry_test', nargs=argparse.REMAINDER, help='入口测试 (lh --entry-test)')
    parser.add_argument('--digital-twin', dest='digital_twin', nargs=argparse.REMAINDER, help='数字孪生 (lh --digital-twin --status)')
    parser.add_argument('--feed-baby', dest='feed_baby', nargs=argparse.REMAINDER, help='投喂宝宝 (lh --feed-baby -c "内容")')
    parser.add_argument('--intent', nargs=argparse.REMAINDER, help='意念引擎 (lh --intent --interactive)')
    parser.add_argument('--dynamic-goal', dest='dynamic_goal', nargs=argparse.REMAINDER, help='动态目标 (lh --dynamic-goal --interactive)')
    parser.add_argument('--capability', nargs=argparse.REMAINDER, help='能力调度 (lh --capability --interactive)')
    parser.add_argument('--universal-completion', dest='universal_completion', nargs=argparse.REMAINDER, help='万能补全 (lh --universal-completion --interactive)')
    parser.add_argument('--mirror-index', dest='mirror_index', nargs=argparse.REMAINDER, help='镜像指数 (lh --mirror-index)')
    parser.add_argument('--dna-validate', dest='dna_validate', nargs=argparse.REMAINDER, help='DNA校验 (lh --dna-validate)')
    parser.add_argument('--triple-audit', dest='triple_audit', nargs=argparse.REMAINDER, help='三重审计闸 (lh --triple-audit --all)')
    parser.add_argument('--weight', nargs=argparse.REMAINDER, help='权重算法 (lh --weight --all)')
    parser.add_argument('--tongxinyi', nargs=argparse.REMAINDER, help='通心译翻译 (lh --tongxinyi "文本")')
    parser.add_argument('--san-cai', dest='san_cai', nargs=argparse.REMAINDER, help='三才算法 (lh --san-cai --interactive)')
    parser.add_argument('--ant-colony', dest='ant_colony', nargs=argparse.REMAINDER, help='蚁群引擎 (lh --ant-colony dashboard)')
    parser.add_argument('--status', nargs=argparse.REMAINDER, help='全系统状态 (lh --status)')
    parser.add_argument('--update', nargs=argparse.REMAINDER, help='更新引擎索引 (lh --update 或 lh --update scan)')
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
        subprocess.run(["python3", str(ROOT / "bin" / "lh_full_system_audit.py")], cwd=str(ROOT), check=False)
        return
    if args.push:
        print_header()
        print("\n  🚀 一键推送全部远端仓库...\n")
        subprocess.run(["python3", str(ROOT / "bin" / "lh_auto_cannon.py")], cwd=str(ROOT), check=False)
        return
    if args.xuanji is not None:
        print_header()
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
    if args.sovereignty is not None:
        print_header()
        sov_path = ROOT / "bin" / "lh_sovereignty_guard.py"
        sov_args = args.sovereignty if args.sovereignty else []
        if not sov_args or sov_args[0] == "validate":
            subprocess.run(["python3", str(sov_path), "validate"])
        elif sov_args[0] == "status":
            subprocess.run(["python3", str(sov_path), "status"])
        elif sov_args[0] == "check":
            print(f"\n  🐉 主权检查: {' '.join(sov_args[1:])}\n")
            subprocess.run(["python3", str(sov_path), "check"] + sov_args[1:])
        elif sov_args[0] == "veto":
            subprocess.run(["python3", str(sov_path), "veto"] + sov_args[1:])
        else:
            print(f"  未知主权子命令: {sov_args[0]}")
            subprocess.run(["python3", str(sov_path), "--help"])
        return
    if args.align is not None:
        print_header()
        align_args = args.align if args.align else ["check"]
        subcmd = align_args[0] if align_args else "check"
        align_checker = ROOT / "bin" / "lh_align_checker.py"
        align_daemon = ROOT / "bin" / "lh_auto_align_daemon.py"
        if subcmd == "fix":
            print("\n  🔧 对齐修复（自动补DNA+确认码+GPG）...\n")
            subprocess.run(["python3", str(align_daemon)], cwd=str(ROOT))
        elif subcmd == "daemon":
            print("\n  🔄 对齐闭环守护（自动修复+归档+通知）...\n")
            subprocess.run(["python3", str(align_daemon)], cwd=str(ROOT))
        elif subcmd == "dry-run":
            print("\n  👁️ 对齐扫描（仅查看·不修改）...\n")
            subprocess.run(["python3", str(align_daemon), "--dry-run"], cwd=str(ROOT))
        elif subcmd == "status":
            print("\n  📊 对齐状态...\n")
            subprocess.run(["python3", str(align_checker), "--json"], cwd=str(ROOT))
        else:  # check or default
            print("\n  🔍 对齐检查（扫描重复/缺失DNA/GPG）...\n")
            subprocess.run(["python3", str(align_checker)], cwd=str(ROOT))
        return
    if args.brain is not None:
        brain_path = ROOT / "bin" / "lh_unified_brain.py"
        brain_args = list(args.brain) if args.brain else ["interactive"]
        subprocess.run([sys.executable, str(brain_path)] + brain_args, cwd=str(ROOT))
        return
    if args.run is not None:
        run_path = ROOT / "bin" / "lh_run.py"
        run_args = list(args.run) if args.run else []
        if not run_args:
            query = input("  🚀 要做什么？").strip()
            run_args = [query] if query else []
        # 🔥 补全模式：--run --complete → 直接显示匹配列表，不执行
        if run_args and run_args[0] == "--complete":
            complete_arg = run_args[1] if len(run_args) > 1 else ""
            subprocess.run(["python3", str(run_path), "--complete", complete_arg])
            return
        print_header()
        if run_args:
            print(f"\n  🚀 自然语言执行: {' '.join(run_args)}\n")
            subprocess.run(["python3", str(run_path)] + run_args)
        else:
            subprocess.run(["python3", str(run_path), "--help"])
        return
    if args.complete:
        run_path = ROOT / "bin" / "lh_run.py"
        subprocess.run(["python3", str(run_path), "--complete", args.complete])
        return
    if args.repo is not None:
        print_header()
        repo_path = ROOT / "bin" / "lh_repo_template.py"
        repo_args = list(args.repo) if args.repo else []
        print(f"\n  🐉 开源项目模板生成器\n")
        subprocess.run(["python3", str(repo_path)] + repo_args)
        return
    if args.dna is not None:
        print_header()
        dna_path = ROOT / "bin" / "lh_dna_generator.py"
        dna_args = list(args.dna) if args.dna else []
        print(f"\n  🧬 龍魂DNA生成器\n")
        subprocess.run(["python3", str(dna_path)] + dna_args)
        return
    if args.know is not None:
        print_header()
        know_path = ROOT / "bin" / "lh_local_knowledge_engine.py"
        know_args = list(args.know) if args.know else ["status"]
        print(f"\n  📚 龍魂·本地知识引擎\n")
        subprocess.run(["python3", str(know_path)] + know_args)
        return
    if args.agent is not None:
        print_header()
        agent_path = ROOT / "bin" / "lh_agent_trainer.py"
        agent_args = list(args.agent) if args.agent else ["status"]
        print(f"\n  🧠 龍魂·智能体训练框架\n")
        subprocess.run(["python3", str(agent_path)] + agent_args)
        return
    if args.lu is not None:
        print_header()
        lu_path = ROOT / "bin" / "lh_lu_compressor.py"
        lu_args = list(args.lu) if args.lu else ["shortcodes"]
        print(f"\n  🐉 龍魂·LU压缩引擎\n")
        subprocess.run(["python3", str(lu_path)] + lu_args)
        return
    if args.central is not None:
        print_header()
        central_path = ROOT / "bin" / "lh_uid9622_central.py"
        central_args = list(args.central) if args.central else ["--status"]
        # 简写映射: status→--status, tasks→--tasks, commands→--commands
        shortcut_map = {"status": "--status", "tasks": "--tasks", "commands": "--commands"}
        mapped = [shortcut_map.get(a, a) for a in central_args]
        print(f"\n  🐉 UID9622 系统中枢引擎\n")
        subprocess.run(["python3", str(central_path)] + mapped)
        return

    # === 自触发编排引擎 ===
    if args.ps:
        print_header()
        print("\n  📊 运行中的脚本\n")
        from lh_lifecycle import ps_list
        ps_list()
        return

    if args.kill_all:
        print_header()
        print("\n  💀 强制终止所有运行中的脚本...\n")
        from lh_lifecycle import stop_running
        kill_count = stop_running()
        print(f"\n  🛑 已终止 {kill_count} 个进程")
        return

    if args.watch or args.watch_daemon:
        print_header()
        print("\n  🐉 启动自触发守护模式...\n")
        trigger_args = [sys.executable, str(ROOT / "bin" / "lh_auto_trigger.py"), "--watch"]
        if args.watch_daemon:
            trigger_args.append("--daemon")
        subprocess.run(trigger_args, cwd=str(ROOT))
        return

    if args.trigger:
        query = args.trigger
        trigger_script = ROOT / "bin" / "lh_auto_trigger.py"
        trigger_cmd = [sys.executable, str(trigger_script), query]
        print_header()
        print(f"\n  🎯 自触发: {query}\n")
        subprocess.run(trigger_cmd, cwd=str(ROOT))
        return

    if args.batch:
        batch_script = ROOT / "bin" / "lh_auto_trigger.py"
        batch_cmd = [sys.executable, str(batch_script), "--batch", args.batch]
        print_header()
        print(f"\n  📦 批量触发: {args.batch}\n")
        subprocess.run(batch_cmd, cwd=str(ROOT))
        return

    # === 省电 API 服务 ===
    if args.api:
        api_script = ROOT / "bin" / "lh_api_server.py"
        api_cmd = [sys.executable, str(api_script), "--port", str(args.api_port)]
        if args.api_redis:
            api_cmd += ["--redis", args.api_redis]
        if args.api_key:
            api_cmd += ["--api-key", args.api_key]
        print_header()
        print(f"\n  🐉 启动省电 API 服务: http://0.0.0.0:{args.api_port}\n")
        subprocess.run(api_cmd, cwd=str(ROOT))
        return

    # === 模式对比器 ===
    if args.compare is not None:
        print_header()
        compare_args = list(args.compare) if args.compare else []
        cmd = [sys.executable, str(ROOT / "bin" / "模式对比.py")] + compare_args
        subprocess.run(cmd, cwd=str(ROOT))
        return

    # === 盘点器 ===
    if args.inventory:
        print_header()
        print("\n  📋 龍魂功能盘点...\n")
        subprocess.run([sys.executable, str(ROOT / "bin" / "lh_inventory.py")], cwd=str(ROOT))
        return

    # === 省电监控器 ===
    if args.energy is not None:
        print_header()
        energy_args = list(args.energy) if args.energy else []
        cmd = [sys.executable, str(ROOT / "bin" / "lh_energy_monitor.py")] + energy_args
        subprocess.run(cmd, cwd=str(ROOT))
        return

    # === 语音网关 ===
    if args.voice is not None:
        print_header()
        voice_args = list(args.voice) if args.voice else []
        cmd = [sys.executable, str(ROOT / "bin" / "lh_voice_gateway.py")] + voice_args
        subprocess.run(cmd, cwd=str(ROOT))
        return

    # === 一键启动全部服务 ===
    if args.start_all:
        print_header()
        print("\n  🐉 启动所有龙魂服务...\n")
        # 启动 API 服务
        print("  📡 启动省电 API (端口 9622)...")
        subprocess.Popen(
            [sys.executable, str(ROOT / "bin" / "lh_api_server.py"), "--port", "9622"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        # 启动省电监控（后台）
        print("  ⚡ 启动省电监控...")
        subprocess.Popen(
            [sys.executable, str(ROOT / "bin" / "lh_energy_monitor.py"), "--log"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        print("\n  ✅ 全部服务已启动")
        print("     API: http://localhost:9622")
        print("     API 文档: http://localhost:9622/docs")
        print("     使用 'lh --energy' 查看省电报告\n")
        return

    # === 调度表子命令统一处理（30+ 引擎一行处理） ===
    for flag, info in SUB_DISPATCH.items():
        script, emoji, desc = info[0], info[1], info[2]
        default_args = info[3] if len(info) > 3 else []
        smart_default = info[4] if len(info) > 4 else ''
        attr = flag.replace('-', '_')
        val = getattr(args, attr, None)
        if val is not None:
            extra = list(val) if val else list(default_args)
            _run_subcommand(script, extra, emoji, desc, smart_default)
            return

    if args.health:
        print_header()
        print("\n  💓 引擎健康检查...\n")
        subprocess.run(["python3", "引擎/launcher.py", "--health"], cwd=str(ROOT), check=False)
        return
    if args.console:
        print_header()
        print("\n  🖥️ 正在启动 Web 可视化操作台...")
        print("     浏览器打开: http://127.0.0.1:9622/static/index.html")
        try:
            subprocess.Popen(['python3', str(ROOT / 'control-panel' / 'main.py')],
                cwd=str(ROOT / 'control-panel'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1.5)
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
            'sovereignty': '🛡️ 安全 & 审计',
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
                subprocess.Popen(['python3', str(ROOT / 'control-panel' / 'main.py')],
                    cwd=str(ROOT / 'control-panel'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(1)
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
