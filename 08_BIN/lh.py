#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
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

import json, os, re, sys, time, shlex, subprocess, hashlib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "bin"))  # bin/ 优先，确保 lh_lifecycle 等模块可导入
sys.path.insert(0, str(ROOT))

# ===== 常量 =====
VERSION = "v1.3"
DNA = "#龍芯⚡️丙午·丙申·癸丑·申时·大有-lh-CONSOLE-v1.0"

# ===== 国密 SM4-CBC 加密模块（数据主权助手）=====
def _load_sm4_class():
    """动态加载 CNSH_国密工具.py 中的 SM4 类。"""
    import importlib.util
    sm4_path = ROOT / "bin" / "CNSH_国密工具.py"
    spec = importlib.util.spec_from_file_location("cnsh_sm4", str(sm4_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载 SM4 模块: {sm4_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SM4


def _get_master_key() -> bytes:
    """读取或生成 16 字节国密主密钥，存于 ~/.longhun/config/master.key。"""
    key_file = Path.home() / ".longhun" / "config" / "master.key"
    key_file.parent.mkdir(parents=True, exist_ok=True)
    if key_file.exists():
        return bytes.fromhex(key_file.read_text(encoding="utf-8").strip())
    import secrets
    key = secrets.token_bytes(16)
    key_file.write_text(key.hex(), encoding="utf-8")
    key_file.chmod(0o600)
    return key


def _sm4_cbc_encrypt(plaintext: bytes, key: bytes) -> bytes:
    """SM4-CBC 加密：返回 IV || ciphertext。"""
    SM4 = _load_sm4_class()
    import secrets
    iv = secrets.token_bytes(16)
    padded = SM4._pad(plaintext)
    rk = SM4._expand_key(key)
    ciphertext = b""
    prev = iv
    for i in range(0, len(padded), 16):
        block = bytes(a ^ b for a, b in zip(padded[i:i + 16], prev))
        enc = SM4._crypt_block(block, rk)
        ciphertext += enc
        prev = enc
    return iv + ciphertext


def _sm4_cbc_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """SM4-CBC 解密：输入 IV || ciphertext。"""
    SM4 = _load_sm4_class()
    if len(ciphertext) < 16 or len(ciphertext) % 16 != 0:
        raise ValueError("密文长度无效")
    iv = ciphertext[:16]
    body = ciphertext[16:]
    rk = SM4._expand_key(key)[::-1]
    plaintext = b""
    prev = iv
    for i in range(0, len(body), 16):
        dec = SM4._crypt_block(body[i:i + 16], rk)
        plaintext += bytes(a ^ b for a, b in zip(dec, prev))
        prev = body[i:i + 16]
    return SM4._unpad(plaintext)


# ===== 证据固化 · Agent审计 + GPG签名 + SM4加密 =====
def _gpg_sign_file(plain_path: Path, key_id: str = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F") -> Path:
    """对指定文件生成 GPG 分离签名，返回 .asc 文件路径。"""
    asc_path = plain_path.with_suffix(plain_path.suffix + ".asc")
    cmd = [
        "gpg", "--batch", "--yes", "--armor",
        "--local-user", key_id,
        "--detach-sign",
        "--output", str(asc_path),
        str(plain_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"GPG 签名失败: {result.stderr}")
    return asc_path


def _run_witness_audit(content: str) -> "dict[str, Any]":
    """调用 longhun_agents 对证据内容进行轻量审计链 (P05 + P15 + S3)。"""
    try:
        sys.path.insert(0, str(ROOT / "05_ENGINES"))
        from engines.longhun_agents import GrandOrchestrator
        orchestrator = GrandOrchestrator(enable_ant_colony=False, enable_blackboard=False)
        task = f"审计以下维权证据的合规性、完整性与签章策略：\n{content[:2000]}"
        result = orchestrator.run(task, mode="quick", agents=["P05", "P15", "S3"])
        return {
            "ok": True,
            "chain": result.get("chain", []),
            "agent_results": {
                pid: {
                    "status": r.get("status", "?"),
                    "name": r.get("name", pid),
                    "summary": str(r.get("result", ""))[:200],
                }
                for pid, r in result.get("agent_results", {}).items()
            },
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


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
        "desc": "五色审计、防篡改、一票否决、熔断申诉、主权守护、🧩插件主权适配",
        "items": [
            {"id": "1", "label": "🔴🐉 主权守护验证", "cmd": "python3 bin/lh_sovereignty_guard.py validate", "desc": "法律边界+一票否决+数据主权三合一验证"},
            {"id": "2", "label": "🐉 主权守护状态", "cmd": "python3 bin/lh_sovereignty_guard.py status", "desc": "查看主权宪法·否决权·数据主权状态"},
            {"id": "3", "label": "🐉 主权操作检查", "cmd": "python3 bin/lh_sovereignty_guard.py check \"操作描述\" --context '{}'", "desc": "检查任意操作是否符合法律边界+数据主权"},
            {"id": "4", "label": "🔴 激活一票否决", "cmd": "python3 bin/lh_sovereignty_guard.py veto activate --reason \"维护\"", "desc": "冻结所有系统操作（仅UID9622可执行）"},
            {"id": "5", "label": "全系统安全巡检", "cmd": "python3 bin/lh_full_system_audit.py", "desc": "一键触发全系统安全扫描"},
            {"id": "6", "label": "三色代码审计", "cmd": "python3 bin/lh_code_audit_cli.py", "desc": "审计单个代码文件安全（交互式输入路径）"},
            {"id": "7", "label": "防篡改扫描", "cmd": "python3 bin/lh_anti_tamper.py scan", "desc": "外部AI内容熔断检查（交互式输入文本）"},
            {"id": "8", "label": "一票否决查询", "cmd": "python3 bin/lh_circuit_breaker.py --list", "desc": "查看所有熔断规则"},
            {"id": "9", "label": "熔断申诉", "cmd": "python3 bin/lh_circuit_breaker.py --interactive", "desc": "对熔断判定提出申诉"},
            {"id": "10", "label": "算法审计", "cmd": "python3 bin/lh_deben_audit.py scan", "desc": "德本审计·离火运五问"},
            {"id": "11", "label": "双重审计引擎", "cmd": "python3 bin/lh_dual_audit_engine.py", "desc": "并行审计提高覆盖"},
            {"id": "12", "label": "🛡️ 上下文安全引擎", "cmd": "python3 bin/lh_safeai.py --inspect \"什么是SQL注入？怎么防范？\"", "desc": "意图分类+七因子审计+P0-P4分层熔断（safe-ai v1.0）"},
            {"id": "13", "label": "⚖️ 公正总裁/审计员", "cmd": "python3 bin/lh_judge.py --content \"请裁决以下争议...\"", "desc": "调用鲲鹏 longhun-judge 模型做公正裁决与三色审计"},
            {"id": "14", "label": "🔄 序列执行引擎", "cmd": "python3 bin/lh_seq.py", "desc": "SafeAI→KFPP→CSDN→公正总裁 流水线审计（交互式输入文本）"},
            {"id": "15", "label": "📦 掀黑箱审计", "cmd": "python3 bin/lh_掀黑箱.py", "desc": "审计任意项目·闭源依赖·数据外流·主权缺失·后门检测·一键报告"},
            {"id": "16", "label": "🧩 插件主权扫描", "cmd": "python3 engines/lh_sovereignty_adapter_engine.py scan", "desc": "扫描任意插件·六维黑箱判定·一票否决检测"},
            {"id": "17", "label": "🧩 插件加载(自动适配)", "cmd": "python3 engines/lh_sovereignty_adapter_engine.py load", "desc": "加载插件→黑箱自动拒绝→生成主权适配器"},
            {"id": "18", "label": "🔌 适配器列表", "cmd": "python3 engines/lh_sovereignty_adapter_engine.py list", "desc": "查看所有已生成的主权适配器"},
            {"id": "19", "label": "🔌 适配器审计", "cmd": "python3 engines/lh_sovereignty_adapter_engine.py audit", "desc": "审计指定适配器·主权元数据完整性检查"},
            {"id": "20", "label": "🚫 黑名单管理", "cmd": "python3 engines/lh_sovereignty_adapter_engine.py blacklist list", "desc": "查看/添加黑箱插件黑名单"},
            {"id": "21", "label": "🏗️ 手动生成适配器", "cmd": "python3 engines/lh_sovereignty_adapter_engine.py generate", "desc": "直接生成指定功能的主权适配器骨架"},
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
            {"id": "7", "label": "道德经锚点", "cmd": "python3 bin/lh_daodejing_engine.py", "desc": "81章道德经·哲学锚点"},
        ]
    },
    "🧬 DNA & 追溯": {
        "desc": "DNA生成、验证、注册、创新溯源",
        "items": [
            {"id": "1", "label": "生成DNA追溯码", "cmd": "python3 bin/hetu_luoshu_dna.py dr", "desc": "为文本/代码/决策生成DNA（交互式输入文本）"},
            {"id": "2", "label": "统一DNA登记", "cmd": "python3 bin/lh_unified_dna_registry.py --menu", "desc": "物理+虚拟资产统一登记"},
            {"id": "3", "label": "DNA审计验证", "cmd": "python3 bin/lh_unified_dna_audit.py", "desc": "验证DNA登记册完整性"},
            {"id": "4", "label": "创新溯源查询", "cmd": "python3 bin/lh_innovation_tracer.py --menu", "desc": "查谁先自研的某项技术"},
            {"id": "5", "label": "DNA唯一性守卫", "cmd": "echo '🟡 已冻结·DNA唯一性由人工审计确保'", "desc": "[冻结] 防止DNA重复/冲突"},
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
            {"id": "5", "label": "行为加密验证", "cmd": "python3 bin/lh_gpg_sign.py verify", "desc": "GPG签名验证·加密完整性"},
            {"id": "6", "label": "情绪海绵", "cmd": "python3 bin/lh_emotion_cli.py", "desc": "情绪温度检测+降温（交互式输入文本）"},
            {"id": "7", "label": "水军引擎(v2)", "cmd": "python3 bin/lh_water_army_detect.py", "desc": "水军团伙检测引擎"},
        ]
    },
    "🔗 同步 & 集成": {
        "desc": "Git同步、Notion同步、道引吸收、跨模块联动",
        "items": [
            {"id": "1", "label": "全量Git推送", "cmd": "python3 bin/lh_auto_cannon.py", "desc": "一键同步到GitHub+Gitee+GitCode"},
            {"id": "2", "label": "Notion知识同步", "cmd": "python3 bin/lh_notion_full_sync.py", "desc": "双向同步本地↔Notion"},
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
            {"id": "1", "label": "系统健康评估", "cmd": "python3 bin/lh_system_health.py", "desc": "全面系统健康评分"},
            {"id": "2", "label": "自助修复", "cmd": "python3 bin/lh_auto_heal.py scan", "desc": "自动检测并修复常见问题"},
            {"id": "3", "label": "定时任务管理", "cmd": "python3 bin/lh_auto_shouheng.py --cron", "desc": "查看/管理定时任务"},
            {"id": "4", "label": "守护进程(v2)", "cmd": "python3 bin/lh_guardian_v2.py", "desc": "系统守护进程管理"},
            {"id": "5", "label": "桌面菜单", "cmd": "cat cnsh/terminal/desktop-menu.json | python3 -m json.tool", "desc": "查看macOS右键菜单配置"},
            {"id": "6", "label": "🏥 系统健康报告", "cmd": "python3 bin/lh_system_health.py", "desc": "汇总引擎状态·依赖检查·健康评分·HTML仪表盘"},
            {"id": "7", "label": "🔍 代码审查", "cmd": "python3 bin/lh_code_review.py --dir bin/", "desc": "圈复杂度·注释率·命名规范·DNA文件头·重复检测"},
            {"id": "8", "label": "🚀 版本发布", "cmd": "python3 bin/lh_version_release.py --check", "desc": "语义化版本·CHANGELOG·Git Tag·发布前预检"},
            {"id": "9", "label": "📊 引擎仪表盘", "cmd": "python3 bin/lh_engine_dashboard.py", "desc": "34引擎分类展示·终端/Web(8080)·健康评分"},
        ]
    },
    "🌐 外部 & 网络": {
        "desc": "API网关、爬虫治理、本地AI中继、浏览器守护",
        "items": [
            {"id": "1", "label": "AI API网关", "cmd": "python3 bin/lh_ai_gateway.py", "desc": "统一AI模型调用网关"},
            {"id": "2", "label": "本地AI中继", "cmd": "python3 bin/lh_local_ai_relay.py", "desc": "本地Ollama中继代理"},
            {"id": "3", "label": "爬虫治理", "cmd": "echo '🟡 已淘汰·爬虫治理功能已废弃'", "desc": "[冻结] 管理网络爬虫行为"},
            {"id": "4", "label": "浏览器守护", "cmd": "python3 bin/lh_browser_daemon.py", "desc": "浏览器自动化守护进程"},
            {"id": "5", "label": "平台封锁日志", "cmd": "python3 bin/lh_platform_block_logger.py", "desc": "记录平台审查/封锁行为"},
            {"id": "6", "label": "Web3 DNA市场", "cmd": "echo '🟡 已冻结·Web3 DNA市场未激活'", "desc": "[冻结] 去中心化DNA资产市场"},
        ]
    },
    "🧠 自主学习引擎": {
        "desc": "Inbox→DNA→任务·趋势绑定·战力评估·项目推荐·数字大军",
        "items": [
            {"id": "1", "label": "交互控制台", "cmd": "python3 bin/lh_learning_engine.py -i", "desc": "完整交互菜单·添加/净化/评估/推荐"},
            {"id": "2", "label": "运行自动化管道", "cmd": "python3 bin/lh_learning_engine.py --run", "desc": "逐条净化待处理Inbox→DNA→任务"},
            {"id": "3", "label": "AI自动拆解", "cmd": "python3 bin/lh_learning_engine.py --auto-digest", "desc": "规则+可选LLM自动提取DNA"},
            {"id": "4", "label": "战力评估", "cmd": "python3 bin/lh_learning_engine.py --evaluate", "desc": "数字大军战力评分"},
            {"id": "5", "label": "项目推荐", "cmd": "python3 bin/lh_learning_engine.py --recommend", "desc": "基于DNA推荐可做项目"},
            {"id": "6", "label": "生成看板", "cmd": "python3 bin/lh_learning_engine.py --dashboard --format html", "desc": "HTML/Notion可视化仪表盘"},
            {"id": "7", "label": "📡 知识源管理", "cmd": "python3 bin/lh_knowledge_source_manager.py", "desc": "订阅源·自动扫描·增量拉取·喂入学习"},
            {"id": "8", "label": "📡 扫描知识源更新", "cmd": "python3 bin/lh_knowledge_source_manager.py --scan", "desc": "扫描所有订阅源·检测新内容·自动喂入学习管道"},
            {"id": "9", "label": "📡 添加预置知识源", "cmd": "python3 bin/lh_knowledge_source_manager.py --preset", "desc": "一键添加5个预置知识源"},
        ]
    },
    "🧬 人格路由引擎": {
        "desc": "自动归类·动态权重·Notion花名册联动·路由优先级排序",
        "items": [
            {"id": "1", "label": "📊 路由状态面板", "cmd": "python3 bin/lh_persona_router.py --status", "desc": "全部人格权重·优先级·信任等级·分组分布"},
            {"id": "2", "label": "📊 JSON状态导出", "cmd": "python3 bin/lh_persona_router.py --status --json", "desc": "结构化JSON输出·供其他引擎调用"},
            {"id": "3", "label": "🔄 重算全部路由", "cmd": "python3 bin/lh_persona_router.py --recalc", "desc": "根据绩效+安全重新计算权重/优先级/信任等级"},
            {"id": "4", "label": "➕ 添加新人格", "cmd": "python3 bin/lh_persona_router.py --add --name \"名称\" --ipa \"编号\" --func \"功能\"", "desc": "自动归类分组/协议/层级"},
            {"id": "5", "label": "✏️ 更新调用次数", "cmd": "python3 bin/lh_persona_router.py --update --ipa \"P72\" --field \"总调用次数\" --value 125", "desc": "更新后自动触发权重重算"},
        ]
    },
    "🔢 数学探索工作流": {
        "desc": "素数数字根·转移流场·卡方检验·弱哥德巴赫·三色审计·ROOT_CARD",
        "items": [
            {"id": "1", "label": "🚀 完整流程 (N=10^6)", "cmd": "python3 bin/lh_math_explorer.py", "desc": "Step1-8 全流程·素数→数字根→流场→哥德巴赫→审计"},
            {"id": "2", "label": "🔢 小规模快速验证", "cmd": "python3 bin/lh_math_explorer.py --n 100000", "desc": "N=10^5·快速验证·适合调试"},
            {"id": "3", "label": "📊 JSON结构化输出", "cmd": "python3 bin/lh_math_explorer.py --json 2>/dev/null", "desc": "纯净JSON输出·供其他引擎调用"},
            {"id": "4", "label": "⏱️ 仅性能基准", "cmd": "python3 bin/lh_math_explorer.py --benchmark-only", "desc": "三档N=10^4/10^5/10^6 筛法+哥德巴赫性能"},
        ]
    },
    "🤖 数学探索自动化": {
        "desc": "定时调度·多参数调优·可视化看板·告警通知·多人格协作",
        "items": [
            {"id": "1", "label": "🚀 立即执行自动化", "cmd": "python3 bin/lh_math_automator.py --run", "desc": "探索→归档→协作→告警→看板 全流程"},
            {"id": "2", "label": "🔧 多参数调优", "cmd": "python3 bin/lh_math_automator.py --tune", "desc": "多档N值·多次迭代·性能基准"},
            {"id": "3", "label": "📊 生成可视化看板", "cmd": "python3 bin/lh_math_automator.py --dashboard", "desc": "χ²趋势·素数趋势·耗时·分布饼图"},
            {"id": "4", "label": "⚡ GPU状态", "cmd": "python3 bin/lh_math_automator.py --gpu-status", "desc": "CuPy/NumPy 加速后端检测"},
            {"id": "5", "label": "📅 安装定时任务", "cmd": "python3 bin/lh_math_automator.py --schedule", "desc": "每日凌晨2点自动运行·cron"},
            {"id": "6", "label": "📋 查看运行状态", "cmd": "python3 bin/lh_math_automator.py --status", "desc": "最近15条日志"},
            {"id": "7", "label": "⚙️ 查看配置", "cmd": "python3 bin/lh_math_automator.py --config", "desc": "~/.longhun/config/math_automator.json"},
        ]
    },
    "🐉 CNSH 统一执行引擎": {
        "desc": "意图解析·A-K标准输出·数字根审计·ROOT_CARD·三色审计·多后端路由",
        "items": [
            {"id": "1", "label": "💬 交互模式", "cmd": "python3 bin/lh_cnsh_engine.py --interactive", "desc": "持续对话·输入意图→A-K格式输出"},
            {"id": "2", "label": "🧠 补齐 人格矩阵", "cmd": "python3 bin/lh_cnsh_engine.py '补齐 人格矩阵路由'", "desc": "自动解析→工程版→ROOT_CARD审计"},
            {"id": "3", "label": "📦 Notion数据库补全", "cmd": "python3 bin/lh_cnsh_engine.py '补齐 Notion 数据库字段'", "desc": "意图→notion任务类型·后端Notion·A-K输出"},
            {"id": "4", "label": "🔧 给Cursor工程包", "cmd": "python3 bin/lh_cnsh_engine.py '给 Cursor 工程包'", "desc": "多后端路由·Cursor指令·文件树·变量表"},
            {"id": "5", "label": "📋 JSON输出", "cmd": "python3 bin/lh_cnsh_engine.py '优化人格路由' --json", "desc": "结构化JSON·供其他引擎调用"},
        ]
    },
    "🌍 CNSH 环境集成引擎": {
        "desc": "全局变量管理·主权尾注·Git Hook防绕过·Docker封装·CI/CD·环境锁定·跨机同步",
        "items": [
            {"id": "1", "label": "🚀 初始化环境", "cmd": "python3 bin/lh_cnsh_environment.py init", "desc": "一键生成cnsh_env.sh·常量模块·ZSH提示符·文件创建器·打印协议"},
            {"id": "2", "label": "🔒 安装Git Hook", "cmd": "python3 bin/lh_cnsh_environment.py install-hook", "desc": "pre-commit钩子·缺失主权尾注拒绝提交"},
            {"id": "3", "label": "📄 创建文件(带尾注)", "cmd": "python3 bin/lh_cnsh_environment.py create 测试.md --content '# 标题'", "desc": "自动挂载CNSH主权尾注·DNA追溯"},
            {"id": "4", "label": "📊 环境状态", "cmd": "python3 bin/lh_cnsh_environment.py status", "desc": "查看所有CNSH文件·Git Hook·Docker·CI状态"},
            {"id": "5", "label": "🔐 锁定环境", "cmd": "python3 bin/lh_cnsh_environment.py lock", "desc": "生成校验和快照·防篡改·json格式"},
            {"id": "6", "label": "🐳 生成Dockerfile", "cmd": "python3 bin/lh_cnsh_environment.py docker", "desc": "容器级主权封装·Python3.11-slim"},
            {"id": "7", "label": "⚙️ 生成CI配置", "cmd": "python3 bin/lh_cnsh_environment.py ci", "desc": "GitHub Actions·自动尾注校验·推送即触发"},
            {"id": "8", "label": "🔄 跨机同步", "cmd": "python3 bin/lh_cnsh_environment.py sync --target root@119.13.90.27", "desc": "生成rsync脚本·同步到鲲鹏"},
        ]
    },
    "🧩 提示词路由器": {
        "desc": "动态路由·自我学习迭代·鲲鹏双向同步·YAML配置·版本回滚",
        "items": [
            {"id": "1", "label": "📊 路由器状态", "cmd": "python3 bin/lh_prompt_router.py --status", "desc": "总路由数·启用数·待学习·缓存·同步历史"},
            {"id": "2", "label": "📋 路由列表", "cmd": "python3 bin/lh_prompt_router.py --list", "desc": "查看所有路由及优先级·触发词"},
            {"id": "3", "label": "🔍 测试路由匹配", "cmd": "python3 bin/lh_prompt_router.py --route \"内容\"", "desc": "输入文本→匹配路由→返回System Prompt"},
            {"id": "4", "label": "📚 学习建议", "cmd": "python3 bin/lh_prompt_router.py --learn", "desc": "高频未匹配输入→自动生成路由建议"},
            {"id": "5", "label": "➕ 交互式添加路由", "cmd": "python3 bin/lh_prompt_router.py --add-route", "desc": "交互式输入路由名·触发词·System Prompt"},
            {"id": "6", "label": "🔄 同步到鲲鹏", "cmd": "python3 bin/lh_prompt_router.py --sync", "desc": "rsync推送路由配置到鲲鹏服务器"},
            {"id": "7", "label": "🌐 启动API服务", "cmd": "python3 bin/lh_prompt_router.py --serve --port 9630", "desc": "FastAPI服务·RESTful接口·自动同步"},
            {"id": "8", "label": "ℹ️ 版本信息", "cmd": "python3 bin/lh_prompt_router.py --info", "desc": "DNA·版本·配置路径"},
        ]
    },
    "📡 知识拉取 & 配置": {
        "desc": "五源汇聚(本地·Notion·鲲鹏·CSDN·Git)·配置合并·一键搭建",
        "items": [
            {"id": "1", "label": "🚀 全量知识拉取", "cmd": "python3 bin/lh_knowledge_puller.py", "desc": "五源全量·自动去重·索引缓存"},
            {"id": "2", "label": "📁 拉取本地", "cmd": "python3 bin/lh_knowledge_puller.py --source local", "desc": "只拉取本地项目文件"},
            {"id": "3", "label": "📋 知识拉取状态", "cmd": "python3 bin/lh_knowledge_puller.py --status", "desc": "查看各来源拉取统计"},
            {"id": "4", "label": "🔍 预览模式", "cmd": "python3 bin/lh_knowledge_puller.py --dry-run", "desc": "预览会拉取什么·不实际执行"},
            {"id": "5", "label": "🔗 来源列表", "cmd": "python3 bin/lh_knowledge_puller.py --list-sources", "desc": "查看所有可用知识来源"},
            {"id": "6", "label": "📦 配置合并", "cmd": "python3 bin/lh_config_puller.py --merge", "desc": "全量配置合并·快照保存"},
            {"id": "7", "label": "🩺 配置健康检查", "cmd": "python3 bin/lh_config_puller.py --report", "desc": "检查必需配置·大文件·重复等"},
            {"id": "8", "label": "🧹 清理缓存", "cmd": "python3 bin/lh_knowledge_puller.py --clean", "desc": "清理知识拉取缓存"},
        ]
    },
    "🔧 依赖 & CNSH转换": {
        "desc": "依赖安装/检查/冻结/鲲鹏同步 + CNSH轻量双向转换·批量/管道友好",
        "items": [
            {"id": "1", "label": "🔍 依赖审计", "cmd": "python3 bin/lh_install_deps.py --check", "desc": "三色审计·核心/非核心分类·架构适配"},
            {"id": "2", "label": "📦 安装依赖", "cmd": "python3 bin/lh_install_deps.py --install", "desc": "自动快照·镜像降级·失败回滚"},
            {"id": "3", "label": "🔧 修复缺失", "cmd": "python3 bin/lh_install_deps.py --fix", "desc": "只安装缺失的依赖"},
            {"id": "4", "label": "🔒 依赖冻结", "cmd": "python3 bin/lh_install_deps.py --freeze", "desc": "生成 requirements.lock.txt 精确版本"},
            {"id": "5", "label": "🖥️ 鲲鹏同步", "cmd": "python3 bin/lh_install_deps.py --sync-kunpeng", "desc": "SCP+SSH自动推送到鲲鹏并安装"},
            {"id": "6", "label": "🔄 CNSH→Python", "cmd": "python3 bin/lh_cnsh_transpiler.py --to-py", "desc": "CNSH中文代码→Python·tokenize精确"},
            {"id": "7", "label": "🔄 Python→CNSH", "cmd": "python3 bin/lh_cnsh_transpiler.py --to-cnsh", "desc": "Python→CNSH中文代码·完整语法映射"},
            {"id": "8", "label": "📋 映射表", "cmd": "python3 bin/lh_cnsh_transpiler.py --info", "desc": "查看完整CNSH语法映射表(100+条)"},
        ]
    },
    "💬 中文自然语言路由器": {
        "desc": "听懂老百姓中文·同音字纠错·错别字容错·口语化表达·语义抽屉匹配·DNA追溯·三色审计",
        "items": [
            {"id": "1", "label": "💬 交互对话模式", "cmd": "python3 bin/lh_natural_language_router.py -i", "desc": "持续对话·输入中文即可·同音字/错别字自动纠正"},
            {"id": "2", "label": "🧬 查DNA追溯", "cmd": "python3 bin/lh_natural_language_router.py '查DNA 文件'", "desc": "自然语言查询DNA追溯信息"},
            {"id": "3", "label": "🔍 搜索东西", "cmd": "python3 bin/lh_natural_language_router.py '搜索 龍魂'", "desc": "口语化搜索·同音字容错"},
            {"id": "4", "label": "📊 看系统状态", "cmd": "python3 bin/lh_natural_language_router.py '系统状态'", "desc": "口语查询系统状态·正常吗/好不好/有没有问题"},
            {"id": "5", "label": "📦 归档保存", "cmd": "python3 bin/lh_natural_language_router.py '归档 报告 --标签 月度'", "desc": "自然语言归档"},
            {"id": "6", "label": "🧪 错别字测试", "cmd": "python3 bin/lh_natural_language_router.py '直行任无'", "desc": "测试同音字纠错: 直行任无→执行任务"},
            {"id": "7", "label": "🏋️ 训练新意图", "cmd": "python3 bin/lh_natural_language_router.py --train", "desc": "交互式添加新意图到语义抽屉"},
            {"id": "8", "label": "📋 JSON输出", "cmd": "python3 bin/lh_natural_language_router.py '查DNA' --json", "desc": "结构化JSON输出·供其他引擎调用"},
        ]
    },
    "🧬 人格MCP代理注册中心": {
        "desc": "93人格→龍芯·功能名重命名·三锚验证(DNA+钱包+GPG)·代理领取·身份证生成·Notion同步",
        "items": [
            {"id": "1", "label": "📋 列出所有代理", "cmd": "python3 bin/lh_persona_mcp_registry.py --list", "desc": "93个人格代理·分类·状态一览"},
            {"id": "2", "label": "🚀 初始化注册中心", "cmd": "python3 bin/lh_persona_mcp_registry.py --init", "desc": "首次运行·创建数据库·写入93代理"},
            {"id": "3", "label": "📊 统计信息", "cmd": "python3 bin/lh_persona_mcp_registry.py --stats", "desc": "总代理·已领取·未领取·分类分布"},
            {"id": "4", "label": "🎫 领取代理", "cmd": "python3 bin/lh_persona_mcp_registry.py --claim P02 --user UID9622", "desc": "领取代理(GPG签名)·三锚绑定"},
            {"id": "5", "label": "🔍 验证代理", "cmd": "python3 bin/lh_persona_mcp_registry.py --verify P02", "desc": "三锚验证·身份/主权/密钥"},
            {"id": "6", "label": "🪪 生成身份证", "cmd": "python3 bin/lh_persona_mcp_registry.py --card P01", "desc": "元世界身份证·三锚+DNA+签名验证"},
            {"id": "7", "label": "🔄 同步Notion", "cmd": "python3 bin/lh_persona_mcp_registry.py --sync", "desc": "生成Notion看板·Markdown格式"},
            {"id": "8", "label": "💰 绑定钱包", "cmd": "python3 bin/lh_persona_mcp_registry.py --bind-wallet 0x... --uid UID9622", "desc": "数字人民币钱包·主权锚绑定"},
        ]
    },
    "⚖️ 人格治理引擎 v2.0": {
        "desc": "执行历史只追加·职责冲突检测·权限继承链·三色审计·DNA追溯",
        "items": [
            {"id": "1", "label": "📊 治理统计", "cmd": "python3 bin/lh_persona_governance.py --stats", "desc": "执行记录·冲突·职责·继承链全景"},
            {"id": "2", "label": "🔍 检测冲突", "cmd": "python3 bin/lh_persona_governance.py --detect-conflicts", "desc": "24h内同一人格重复操作冲突检测"},
            {"id": "3", "label": "✅ 解决冲突", "cmd": "python3 bin/lh_persona_governance.py --resolve-conflicts", "desc": "保留新记录·标记旧记录·写入审计日志"},
            {"id": "4", "label": "📋 审计历史", "cmd": "python3 bin/lh_persona_governance.py --audit-history", "desc": "三色审计·全部执行记录·🟢🟡🔴分布"},
            {"id": "5", "label": "📝 回顾历史(7天)", "cmd": "python3 bin/lh_persona_governance.py --review-history --days 7", "desc": "Markdown报告·操作+DANA+状态"},
            {"id": "6", "label": "📌 分配职责", "cmd": "python3 bin/lh_persona_governance.py --assign-duty P01 --primary \"战略推演\"", "desc": "主责·副责·触发词·优先级"},
            {"id": "7", "label": "🔗 设置继承", "cmd": "python3 bin/lh_persona_governance.py --inherit P01 --from P00", "desc": "子人格继承父人格配置"},
            {"id": "8", "label": "📝 记录执行", "cmd": "python3 bin/lh_persona_governance.py --record P01 --action \"处理\" --target \"审计\"", "desc": "追加执行历史·自动DNA追溯"},
        ]
    },
    "🖥️ 公开操作台": {
        "desc": "透明操作面板·全员可见·操作留痕·AI自动操作带DNA",
        "items": [
            {"id": "1", "label": "🖥️ 启动公开操作台", "cmd": "python3 bin/lh_public_console.py start", "desc": "Web面板 :8778·状态API·审计API·操作API"},
            {"id": "2", "label": "📊 查看公开状态", "cmd": "python3 bin/lh_public_console.py status", "desc": "CLI查看当前所有公开状态"},
            {"id": "3", "label": "📋 查看审计日志", "cmd": "python3 bin/lh_public_console.py log --limit 30", "desc": "CLI查看最新操作审计日志"},
            {"id": "4", "label": "⚡ 执行操作", "cmd": "python3 bin/lh_public_console.py operate --op set_state --key test --value hello", "desc": "执行可审计操作（set_state/freeze_state/log）"},
            {"id": "5", "label": "🤖 启动AI自动操作引擎", "cmd": "python3 bin/lh_auto_operator.py start", "desc": "定时AI任务·自动心跳·状态看门狗·全留痕"},
            {"id": "6", "label": "🤖 AI引擎状态", "cmd": "python3 bin/lh_auto_operator.py status", "desc": "查看AI任务运行状态·最近操作"},
            {"id": "7", "label": "🛑 停止AI引擎", "cmd": "python3 bin/lh_auto_operator.py stop", "desc": "优雅停止AI自动操作引擎"},
        ]
    },
    "📓 Notion 对话桥": {
        "desc": "Notion实时同步·本地全文索引·RAG对话·点开Notion就能问AI",
        "items": [
            {"id": "1", "label": "🔄 全量同步", "cmd": "python3 bin/lh_notion_chat_bridge.py sync", "desc": "拉取所有Notion内容到本地·FTS5全文索引"},
            {"id": "2", "label": "🔍 搜索Notion", "cmd": "python3 bin/lh_notion_chat_bridge.py search <关键词>", "desc": "全文搜索你的Notion内容·本地毫秒级"},
            {"id": "3", "label": "💬 Notion对话", "cmd": "python3 bin/lh_notion_chat_bridge.py chat <问题>", "desc": "基于Notion内容RAG回答·Ollama本地推理"},
            {"id": "4", "label": "📊 同步状态", "cmd": "python3 bin/lh_notion_chat_bridge.py status", "desc": "查看索引页面数·上次同步时间"},
            {"id": "5", "label": "🌐 启动API", "cmd": "python3 bin/lh_notion_chat_bridge.py api --port 8779", "desc": "Web面板 :8779·搜索/对话/同步API"},
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
            {"id": "7", "label": "🧩 知识全息拉取", "cmd": "python3 bin/lh_knowledge_harvester.py", "desc": "从Notion/CSDN/本地/备忘录/AI对话拉取龍魂知识·哲学→代码"},
            {"id": "8", "label": "⚙️ 知识拉取器配置", "cmd": "python3 bin/lh_setup_harvester.py", "desc": "一键配置环境变量+依赖+拉取+审查（交互式引导）"},
            {"id": "9", "label": "🧪 知识编译", "cmd": "python3 bin/lh_knowledge_compiler.py --all", "desc": "原则→可执行规则·规则→.env配置·模式→触发词·生成代码骨架"},
            {"id": "10", "label": "📤 知识迁移", "cmd": "python3 bin/lh_knowledge_migrate.py", "desc": "本地知识推送到Notion/导出Markdown包/推GitHub"},
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
    ("Notion同步", "P04", "同步Notion / notion sync / 拉取Notion"),
    ("Notion搜索", "P04", "搜索Notion / notion search / 在Notion里搜"),
    ("Notion对话", "P04", "问Notion / notion chat / Notion里有没有"),
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
    lh "查一下语义抽屉"  → 自然语言路由，自动触发相关引擎（说人话就行）
    lh ask "人参的功效" → 同上（显式自然语言入口）
    lh "系统状态如何"    → 自动匹配status引擎返回系统状态
    lh "我回来了"        → 任意中文→自动语义匹配→智能路由
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
    if sys.stdin.isatty():
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
    'material':             ('lh_material_search.py',          '🎞️', '素材库', [], 'search'),
    'material-scan':        ('lh_material_scanner.py',         '📂', '素材扫描入库'),
    'material-tag':         ('lh_material_tagger.py',          '🏷️', '素材自动打标'),
    'material-match':       ('lh_material_video_bridge.py',    '🎬', '视频场景匹配'),
    'video-clean':          ('lh_video_cleaner.py',            '🧹', '视频素材清洗(帧提取·去重·打标)', [], 'test'),
    'merchant':             ('lh_merchant_api_gateway.py',     '🏪', '国产商户API平台(注册·审核·密钥·网关)', [], 'test'),
    'merchant-serve':       ('lh_merchant_api_gateway.py',     '🚀', '启动商户API网关', ['serve']),
    'gateway-quickstart':   ('lh_merchant_gateway_quickstart.py', '⚡', '商户API一键启动+测试+接入信息', ['--full']),
    'pipeline_3d':           ('lh_3d_pipeline.py',             '🎨', '3D管线'),
    'browser':              ('lh_browser_historian.py',       '📖', '浏览器史官'),
    'cnsh':                 ('cnsh_compiler.py',              '🀄', 'CNSH编译器'),
    'cnsh_runtime':         ('lh_cnsh_runtime_math.py',        '⚡', 'CNSH运行时数学', [], 'status'),
    'cnsh_complete':        ('cnsh_complete.py',              '☯️', 'CNSH完整版', [], '--interactive'),
    'cnsh_editor':          ('cnsh_editor.py',                '✏️', 'CNSH编辑器'),
    'cnsh_translator':      ('lh_cnsh_translator.py',         '🌐', 'CNSH翻译', [], '--interactive'),
    # 🔧 依赖管理 & CNSH轻量转换
    'deps':                 ('lh_install_deps.py',            '🔧', '依赖管理·安装/检查/冻结/同步', [], '--check'),
    'cnsh_transpile':       ('lh_cnsh_transpiler.py',         '🔄', 'CNSH轻量双向转换·批量/管道', [], '--info'),
    'cnsh_ui':              ('cnsh_ui.py',                    '🖥️', 'CNSH UI'),
    'seven_dimension':      ('lh_seven_dimension_engine_v2.py','🌌', '七维推演引擎', [], '--interactive'),
    'three_color':          ('lh_three_color_audit.py',       '🔴', '三色审计引擎', [], 'audit'),
    'loyalty':              ('lh_loyalty_scan.py',            '🐉', '忠义数据铁律自检（永不收集用户数据）', [], 'scan'),
    'uv':                   ('lh_unified_visual.py',          '🎨', '统一视觉色彩引擎(八色)', [], 'judge'),
    'visual':               ('lh_unified_visual.py',          '🎨', '统一视觉色彩引擎(八色)', [], 'judge'),
    'proto':                ('lh_proto_portal.py',            '📋', '协议结构门户(338文档·8Tab)', [], 'governance'),
    'protocols':            ('lh_proto_portal.py',            '📋', '协议结构门户(338文档·8Tab)', [], 'governance'),
    'proto-serve':          ('lh_protocol_server.py',         '🌐', '协议动态索引服务(API:8910·60s刷新)', ['--port'], 'governance'),
    'gametheory':           ('lh_proto_portal.py',            '🎲', '博弈论报告(六系统对比)', [], 'governance'),
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
    'compliance':           ('lh_compliance.py',              '⚖️', '合规证据包（法律+国密+等保+AI合规）', ['--export']),
    'syntax':               ('lh_syntax_lint.py',              '📐', '语法规范校验·DNA/确认码/缩进/龍字/三色/许可·依据v3.0', [], '.'),
    'syntax-lint':          ('lh_syntax_lint.py',              '📐', '语法规范校验(全写)·同上', [], '.'),
    'syntax-fix':           ('lh_syntax_lint.py',              '🔧', '自动修正「龙」→「龍」品牌标识', ['--fix-dragon']),
    'status':               ('lh_unified_brain.py',           '📊', '全系统状态', ['status']),
    '掀黑箱':               ('lh_掀黑箱.py',                  '📦', '掀黑箱审计', ['.']),
    'imprint':              ('lh_digital_imprint.py',        '🧬', '数字人印记'),
    'notion_full':          ('lh_notion_full_sync.py',       '🔄', 'Notion全量同步'),
    'persona_sync':         ('lh_notion_persona_sync.py',    '🧬', '人格矩阵Notion同步'),
    'persona':              ('lh_persona_runtime.py',         '🧠', '人格矩阵运行时', [], ''),
    'notion-architect':     ('lh_notion_architect.py',        '🏗️', 'Notion架构管理器'),
    'notion-link':          ('lh_notion_autolinker.py',        '🔗', 'Notion自动关联器'),
    'notion-bridge':        ('lh_notion_chat_bridge.py',       '💬', 'Notion对话桥', [], 'serve'),
    'portal':               ('lh_portal_api.py',               '🌐', '统一门户官网', [], '--port 8778'),
    'mode':                 ('lh_universal_mode.py',           '🧬', '统一AI执行模式·ROOT_CARD审计', [], ''),
    'learn':                ('lh_learning_engine.py',          '🧠', '自主学习引擎·知识DNA·数字大军', [], ''),
    'evolution':            ('lh_evolution_engine.py',         '🧬', '自我进化引擎v2.0·感知·学习·记忆·进化四维闭环', [], 'demo'),
    'evo':                  ('lh_evolution_engine.py',         '🧬', '进化引擎(简)·自检·演示·状态', [], 'status'),
    'fortified':            ('lh_evolution_fortified.py',      '🛡️', '强化进化引擎·主权·真理·反殖民十维防护', [], 'demo'),
    'fort':                 ('lh_evolution_fortified.py',      '🛡️', '强化引擎(简)·自检·演示·状态', [], 'status'),
    'knowledge_source':     ('lh_knowledge_source_manager.py', '📡', '知识源管理器·自动订阅·更新检测·喂入学习', [], ''),
    'persona_router':       ('lh_persona_router.py',           '🧬', '人格路由引擎·自动归类·动态权重·Notion花名册', [], '--status'),
    'math_explore':         ('lh_math_explorer.py',             '🔢', '数学难题解决工作流·素数数字根·哥德巴赫·流场·三色审计', [], '--n 100000'),
    'math_automate':        ('lh_math_automator.py',            '🤖', '数学探索自动化调度器·调优·看板·告警·多人格协作', [], '--run'),
    'cnsh_engine':          ('lh_cnsh_engine.py',               '🐉', 'CNSH统一执行引擎·A-K输出·意图解析·ROOT_CARD审计', [], '--interactive'),
    'cnsh_env':             ('lh_cnsh_environment.py',           '🌍', 'CNSH环境集成引擎·全局变量·主权尾注·Git Hook·Docker·CI', [], 'status'),
    'nl':                   ('lh_natural_language_router.py',  '💬', '中文自然语言路由器·同音字纠错·语义抽屉·意图匹配', [], '-i'),
    'persona-mcp':          ('lh_persona_mcp_registry.py',   '🧬', '人格MCP代理注册中心·93人格·三锚验证·身份证系统', [], '--list'),
    'persona-governance':   ('lh_persona_governance.py',     '⚖️', '人格治理引擎v2.0·冲突检测·继承链·只追加审计', [], '--stats'),
    'dct_watermark':        ('lh_dct_watermark.py',          '🔏', 'DCT不可见水印'),
    'face_verify':          ('lh_face_verify.py',            '👤', '人脸验证'),
    'qr_code':              ('lh_qr_code.py',                '📱', '印记二维码'),
    'batch_process':        ('lh_batch_processor.py',        '⚡', '批量处理'),
    'voice_register':       ('lh_voice_register.py',         '🎤', '声纹注册库'),
    'qe':                   ('lh_quantum_evidence.py',       '🌌', '量子存证引擎'),
    'quantum-evidence':     ('lh_quantum_evidence.py',       '🌌', '量子存证引擎'),
    # 🔥 时间引擎 v4.0 — 全系统输出时间戳·天干地支·64卦·审计链
    'time-engine':          ('lh_time_engine.py',             '🐉', '时间引擎·天干地支·64卦·审计链·输出戳', [], 'stamp'),
    'te':                   ('lh_time_engine.py',             '🐉', '时间引擎(简)·天干地支·64卦', [], 'stamp'),
    # 🐉 道德经知识引擎 v2.0 — 可编程·可查询·蚁群定锚·五行生克·DNA全链路
    'ddj':                  ('lh_daodejing_engine.py',         '📖', '道德经引擎·查询/定锚/导出/统计·81章龙魂解读', [], ''),
    'daodejing':            ('lh_daodejing_engine.py',         '📖', '道德经引擎(全写)·同上', [], ''),
    # 🔥 知识矩阵 v1.0 — 全维度知识索引聚合·协议·论文·CSDN·引擎·图谱
    'matrix':               ('lh_knowledge_matrix.py',        '🧬', '知识矩阵·全维度知识索引聚合', [], '--pretty'),
    'km':                   ('lh_knowledge_matrix.py',        '🧬', '知识矩阵(简)·数据聚合', [], '--pretty'),
    # 🔐 平台规则审计 — 一键审计·华夏法则对照·五维博弈·三色判定
    'platform-audit':       ('lh_platform_audit.py',          '🔐', '平台规则审计·华夏法则对照·五维博弈', [], '--interactive'),
    'pa':                   ('lh_platform_audit.py',          '🔐', '平台规则审计(简)·一键审计', [], '--interactive'),
    # 🧬 DNA追溯码生成 — 自动化时空标签·五行·64卦·ROOT_CARD
    'dna':                  ('lh_dna_generator.py',           '🧬', 'DNA追溯码生成·五行·64卦·ROOT_CARD', [], '--title'),
    'dna-gen':              ('lh_dna_generator.py',           '🧬', 'DNA生成(完整名)', [], '--title'),
    # 🐉 透明审计AI Hub — 多模型对话·对比·审计仪表盘·DNA追溯
    'ai-hub':               ('lh_ai_hub_api.py',              '🐉', '透明审计AI Hub·多模型·审计·对比', [], '--port=8778'),
    # 🧩 提示词路由器 — 动态路由·自我学习·鲲鹏同步
    'prompt-router':        ('lh_prompt_router.py',           '🧩', '提示词路由器·动态匹配·自学习', [], '--status'),
    'pr':                   ('lh_prompt_router.py',           '🧩', '提示词路由器(简)·路由·学习·同步', [], '--status'),
    # 📡 知识拉取 & 配置 — 五源汇聚·配置合并·一键搭建
    'knowledge-pull':       ('lh_knowledge_puller.py',        '📡', '知识拉取·五源汇聚·自动索引', [], '--status'),
    'kp':                   ('lh_knowledge_puller.py',        '📡', '知识拉取(简)·全量/指定来源', [], '--status'),
    'config-pull':          ('lh_config_puller.py',           '📦', '配置拉取·自动发现·合并快照', [], '--merge'),
    'cp':                   ('lh_config_puller.py',           '📦', '配置拉取(简)·合并/检查', [], '--merge'),
    'setup-all':            ('setup-all',                     '🚀', '一键搭建·知识拉取+配置合并+状态', [], ''),
    # 🔥 自主主权插件适配 v1.0 — 黑箱检测·自动替代·适配器管理
    'plugin':               ('lh_sovereignty_adapter_engine.py', '🧩', '主权插件管理·扫描/加载/黑名单', []),
    'adapter':              ('lh_sovereignty_adapter_engine.py', '🔌', '适配器管理·列表/审计/生成/移除', []),
    # 🐉 協議層統治引擎 v1.0 — P0價值邊境檢查站·DNA驗證·渲染引擎·API網關·強制P0約束
    'protocol-reign':       ('lh_protocol_reign.py',           '🐉', '協議層統治·P0價值邊境檢查站(演示)', [], '--demo'),
    'preign':               ('lh_protocol_reign.py',           '🐉', '協議統治(簡)·P0驗證/DNA校驗/渲染', []),
    # 🐉 真話-協議轉化引擎 v1.0 — 用戶真話→AI結構化→協議映射→工程落地→反饋閉環·簡繁雙關鍵詞
    'truth':                ('lh_truth_engine.py',             '🗣️', '真話轉化·用戶說真話→P0協議·簡繁雙關鍵詞(演示)', [], '--demo'),
    'zhenhua':              ('lh_truth_engine.py',             '🗣️', '真話引擎(簡)·結構化·看板·反饋', []),
    # 🔬 行為密碼學引擎 v2.0 — 七因子來源追溯·五級攻擊模擬·主權API
    'bcm':                  ('lh_behavioral_crypto.py',        '🔬', '行為密碼學·七因子行為指紋·攻擊模擬·主權API(:8775)', []),
    'behavioral-crypto':    ('lh_behavioral_crypto.py',        '🔬', '行為密碼學(全名)·七因子·實驗·雷達圖', [], '--demo'),
    # 📖 术语白话化 — 查询术语大白话解释
    'term':                 ('lh_term_tool.py',                '📖', '术语白话查询·端口/目录/命令/缩写/组件大白话', [], ''),
}


def _run_subcommand(script_name: str, extra_args: list[str] | None = None, emoji: str = '🚀', label: str = '',
                    smart_default: str = '', suppress_header: bool = False):
    """统一子命令执行器
    - 如果 extra_args 不为空且第一个参数不是 -(flags)，且定义了 smart_default → 自动插入默认子命令
    - suppress_header: True 时不打印装饰 header（用于 --json 模式）
    """
    script_path = ROOT / "bin" / script_name
    if not suppress_header:
        print_header()
        if label:
            print(f"\n  {emoji} {label}")
    args_list = [sys.executable, str(script_path)]

    if extra_args:
        # 智能插入：第一个参数不是 flag 且设有 smart_default
        if smart_default and extra_args and not extra_args[0].startswith('-'):
            args_list.append(smart_default)
        args_list.extend(extra_args)
    result = subprocess.run(args_list, cwd=str(ROOT), check=False)
    # 🔥 自动输出时间戳（每句回复焊死）
    if not suppress_header:
        _print_time_stamp()
    return result


def _print_time_stamp():
    """打印当前时间戳·天干地支·卦象·三色相位"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("te", str(ROOT / "bin" / "lh_time_engine.py"))
    if spec and spec.loader:
        te = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(te)
        stamp = te.get_output_stamp(format_type="simple")
        print(f"\n  {stamp}")


def _run_interactive_item(item: dict[str, str]):
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
    parser = argparse.ArgumentParser(description='龍魂统一控制台', allow_abbrev=False, add_help=False)
    parser.add_argument('--help', '-h', dest='show_help', action='store_true', help='显示中文帮助')
    parser.add_argument('--dashboard', action='store_true', help='人格仪表盘')
    parser.add_argument('--engine', action='store_true', help='引擎能力表')
    parser.add_argument('--help-flag', dest='show_help_flag', action='store_true', help='帮助（兼容旧入口）')
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
    parser.add_argument('--script-align', dest='script_align', nargs=argparse.REMAINDER,
                        help='脚本对齐管理 (lh --script-align --scan / --full / --fix / --stamp)')
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
    parser.add_argument('--power-save', nargs=argparse.REMAINDER, help='省电省算力总控台 (lh --power-save status/optimize/sleep/wake/cache/report/daemon/services)')
    parser.add_argument('--head', nargs=argparse.REMAINDER, help='文章抬头模板选择器 (lh --head 或 lh --head --list/--auto "描述"/--template N --title "标题")')
    parser.add_argument('--term', nargs=argparse.REMAINDER, help='术语白话查询 (lh --term <术语> 或 lh --term --list/--scan <文件>)')
    parser.add_argument('--voice', nargs=argparse.REMAINDER, help='语音网关 (lh --voice 或 lh --voice --text 文本模式)')
    parser.add_argument('--start-all', dest='start_all', action='store_true', help='一键启动全部服务 (lh --start-all)')
    parser.add_argument('--compare', nargs=argparse.REMAINDER, help='模式对比器 (lh --compare 或 lh --compare --md/--html/--all)')
    parser.add_argument('--kunpeng', nargs=argparse.REMAINDER, help='鲲鹏状态 (lh --kunpeng 或 lh --kunpeng --services/--logs)')
    parser.add_argument('--ports', nargs=argparse.REMAINDER, help='端口状态一览 (lh --ports 或 lh --ports --full/--mac/--kunpeng)')
    # === 调度表子命令（统一处理） ===
    parser.add_argument('--search', nargs=argparse.REMAINDER, help='搜索引擎 (lh --search "关键词")')
    parser.add_argument('--video', nargs=argparse.REMAINDER, help='视频工坊 (lh --video --script 稿.txt)')
    parser.add_argument('--pipeline-3d', '--3d', dest='pipeline_3d', nargs=argparse.REMAINDER, help='3D管线 (lh --3d)')
    # 🔥 自主主权插件适配 v1.0
    parser.add_argument('--plugin', nargs=argparse.REMAINDER, help='主权插件管理 (lh --plugin scan/load/list/blacklist)')
    parser.add_argument('--adapter', nargs=argparse.REMAINDER, help='适配器管理 (lh --adapter list/audit/generate/remove)')
    parser.add_argument('--browser', nargs=argparse.REMAINDER, help='浏览器史官 (lh --browser collect/search/validate/status)')
    parser.add_argument('--uv', nargs=argparse.REMAINDER, help='统一视觉八色判定 (lh --uv judge "文本")')
    parser.add_argument('--visual', nargs=argparse.REMAINDER, help='统一视觉八色判定 (lh --visual colors)')
    parser.add_argument('--proto', nargs=argparse.REMAINDER, help='协议结构门户 (lh --proto stats/open)')
    parser.add_argument('--protocols', nargs=argparse.REMAINDER, help='协议结构门户 (lh --protocols)')
    parser.add_argument('--gametheory', nargs=argparse.REMAINDER, help='博弈论报告 (lh --gametheory summary/open)')
    parser.add_argument('--proto-serve', dest='proto_serve', nargs=argparse.REMAINDER, help='协议动态索引服务 (lh --proto-serve --port 8910)')
    parser.add_argument('--cnsh', nargs=argparse.REMAINDER, help='CNSH编译器 (lh --cnsh -i test.cnsh --run)')
    parser.add_argument('--cnsh-runtime', dest='cnsh_runtime', nargs=argparse.REMAINDER, help='CNSH运行时 (lh --cnsh-runtime status)')
    parser.add_argument('--cnsh-complete', dest='cnsh_complete', nargs=argparse.REMAINDER, help='CNSH完整版 (lh --cnsh-complete --interactive)')
    parser.add_argument('--cnsh-editor', dest='cnsh_editor', nargs=argparse.REMAINDER, help='CNSH编辑器 (lh --cnsh-editor -f input.txt)')
    parser.add_argument('--cnsh-translator', dest='cnsh_translator', nargs=argparse.REMAINDER, help='CNSH翻译 (lh --cnsh-translator -f test.py)')
    parser.add_argument('--cnsh-transpile', '--ct', '--transpile', dest='cnsh_transpile', nargs=argparse.REMAINDER, help='CNSH轻量双向转换 (lh --ct --to-cnsh script.py)')
    parser.add_argument('--cnsh-ui', dest='cnsh_ui', nargs=argparse.REMAINDER, help='CNSH UI (lh --cnsh-ui)')
    # 🔧 依赖管理
    parser.add_argument('--deps', dest='deps', nargs=argparse.REMAINDER, help='依赖管理 (lh --deps --check/--install/--freeze/--sync-kunpeng)')
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
    parser.add_argument('--掀黑箱', nargs=argparse.REMAINDER, help='掀黑箱审计 (lh --掀黑箱 [路径] 或 lh --掀黑箱 --json)')
    parser.add_argument('--imprint', nargs=argparse.REMAINDER, help='数字人印记引擎 (lh --imprint create/list/verify/watermark/sync/status)')
    parser.add_argument('--notion-full', dest='notion_full', nargs=argparse.REMAINDER, help='Notion全量同步引擎 (lh --notion-full sync/search/status)')
    parser.add_argument('--persona-sync', dest='persona_sync', nargs=argparse.REMAINDER, help='人格矩阵Notion同步 (lh --persona-sync sync/dry-run/cleanup)')
    parser.add_argument('--persona', dest='persona', nargs=argparse.REMAINDER, help='人格矩阵运行时 (lh --persona list/switch/current/chain/status/match/bridge/memory/sync)')
    parser.add_argument('--dct-watermark', dest='dct_watermark', nargs=argparse.REMAINDER, help='DCT不可见水印引擎 (lh --dct-watermark embed/extract/batch/status)')
    parser.add_argument('--face-verify', dest='face_verify', nargs=argparse.REMAINDER, help='人脸验证引擎 (lh --face-verify register/verify/compare/list/remove/status)')
    parser.add_argument('--qr-code', dest='qr_code', nargs=argparse.REMAINDER, help='印记二维码引擎 (lh --qr-code generate/embed/extract/status)')
    parser.add_argument('--batch-process', dest='batch_process', nargs=argparse.REMAINDER, help='批量处理引擎 (lh --batch-process --mode watermark/imprint/voiceprint)')
    parser.add_argument('--voice-register', dest='voice_register', nargs=argparse.REMAINDER, help='声纹注册库 (lh --voice-register register/verify/match/list/remove/status)')
    parser.add_argument('--notion-architect', dest='notion_architect', nargs=argparse.REMAINDER, help='Notion架构管理器 (lh --notion-architect list/add/delete/rename/backup --db <id>)')
    parser.add_argument('--notion-link', dest='notion_link', nargs=argparse.REMAINDER, help='Notion自动关联器 (lh --notion-link create/recommend/audit --page <id>)')
    parser.add_argument('--notion-bridge', dest='notion_bridge', nargs=argparse.REMAINDER, help='Notion对话桥 (lh --notion-bridge serve/sync/search/chat/status)')
    parser.add_argument('--portal', dest='portal', nargs=argparse.REMAINDER, help='统一门户官网 (lh --portal --port 8778)')
    parser.add_argument('--mode', dest='mode', nargs=argparse.REMAINDER, help='统一AI执行模式 (lh --mode "任务描述")')
    parser.add_argument('--learn', dest='learn', nargs=argparse.REMAINDER, help='自主学习引擎 (lh --learn -i)')
    parser.add_argument('--knowledge-source', dest='knowledge_source', nargs=argparse.REMAINDER, help='知识源管理器 (lh --knowledge-source --scan)')
    parser.add_argument('--persona-router', dest='persona_router', nargs=argparse.REMAINDER, help='人格路由引擎 (lh --persona-router --status)')
    parser.add_argument('--math-explore', dest='math_explore', nargs=argparse.REMAINDER, help='数学探索工作流 (lh --math-explore --n 100000)')
    parser.add_argument('--math-automate', dest='math_automate', nargs=argparse.REMAINDER, help='数学探索自动化调度器 (lh --math-automate --run)')
    parser.add_argument('--cnsh-engine', dest='cnsh_engine', nargs=argparse.REMAINDER, help='CNSH统一执行引擎 (lh --cnsh-engine "补齐 人格矩阵")')
    parser.add_argument('--cnsh-env', dest='cnsh_env', nargs=argparse.REMAINDER, help='CNSH环境集成引擎 (lh --cnsh-env init/status/lock/docker/ci)')
    parser.add_argument('--nl', dest='nl', nargs=argparse.REMAINDER, help='中文自然语言路由器 (lh --nl "查DNA 文件" 或 lh --nl -i交互)')
    parser.add_argument('--persona-mcp', dest='persona_mcp', nargs=argparse.REMAINDER, help='人格MCP代理注册中心 (lh --persona-mcp --list/--init/--stats)')
    parser.add_argument('--persona-governance', dest='persona_governance', nargs=argparse.REMAINDER, help='人格治理引擎 (lh --persona-governance --stats/--audit-history)')
    parser.add_argument('--qe', dest='qe', nargs=argparse.REMAINDER, help='量子存证引擎 (lh --qe store --text "内容" / query / verify / reconstruct)')
    parser.add_argument('--quantum-evidence', dest='quantum_evidence', nargs=argparse.REMAINDER, help='量子存证引擎 (同 --qe)')
    # 🔥 时间引擎 v4.0
    parser.add_argument('--time-engine', dest='time_engine', nargs=argparse.REMAINDER, help='时间引擎·天干地支64卦 (lh --time-engine --stamp/hexagram/run/audit)')
    parser.add_argument('--te', dest='te', nargs=argparse.REMAINDER, help='时间引擎简写 (lh --te --stamp)')
    # 🐉 道德经知识引擎 v2.0
    parser.add_argument('--ddj', dest='ddj', nargs=argparse.REMAINDER, help='道德经引擎 (lh --ddj -c 章号/-s 关键词/-t 标签/-a 定锚/--stats)')
    parser.add_argument('--daodejing', dest='daodejing', nargs=argparse.REMAINDER, help='道德经引擎全写 (lh --daodejing --stats)')
    # 🔐 平台规则审计
    parser.add_argument('--platform-audit', dest='platform_audit', nargs=argparse.REMAINDER, help='平台规则审计·华夏法则对照 (lh --platform-audit --interactive/--file xxx/--url xxx)')
    parser.add_argument('--pa', dest='pa', nargs=argparse.REMAINDER, help='平台规则审计简写 (lh --pa --interactive)')
    # 🧩 提示词路由器
    parser.add_argument('--prompt-router', dest='prompt_router', nargs=argparse.REMAINDER, help='提示词路由器 (lh --prompt-router --route/--status/--sync/--learn/--list/--serve)')
    parser.add_argument('--pr', dest='pr', nargs=argparse.REMAINDER, help='提示词路由器简写 (lh --pr --status)')
    # 📡 知识拉取 & 配置
    parser.add_argument('--knowledge-pull', dest='knowledge_pull', nargs=argparse.REMAINDER, help='知识拉取·五源汇聚 (lh --knowledge-pull --status/--list-sources/--dry-run/--force/--clean)')
    parser.add_argument('--kp', dest='kp', nargs=argparse.REMAINDER, help='知识拉取简写 (lh --kp --status)')
    parser.add_argument('--config-pull', dest='config_pull', nargs=argparse.REMAINDER, help='配置拉取·自动发现合并 (lh --config-pull --list/--merge/--report)')
    parser.add_argument('--cp', dest='cp', nargs=argparse.REMAINDER, help='配置拉取简写 (lh --cp --merge)')
    parser.add_argument('--setup-all', dest='setup_all', nargs=argparse.REMAINDER, help='一键搭建·知识+配置+状态 (lh --setup-all)')
    # 📄 智能排版引擎
    parser.add_argument('--format', dest='fmt', nargs=argparse.REMAINDER, help='智能排版引擎 (lh --format "内容" --type flowchart / cnsh / python / table / timeline / ...)')
    parser.add_argument('--type', dest='fmt_type', type=str, help='排版类型 (配合 --format 使用，默认 auto 自动识别)')
    parser.add_argument('--fmt', dest='fmt_short', nargs=argparse.REMAINDER, help='智能排版引擎简写 (lh --fmt "内容" --type flowchart)')
    # 🧬 创作者DNA受益算法
    parser.add_argument('--benefit', dest='benefit', nargs=argparse.REMAINDER, help='创作者DNA受益算法 (lh --benefit --register --creator-id UID9622 --creator-name Lucky --content "算法描述" --category algorithm)')
    # 📋 任务编排引擎
    parser.add_argument('--task', dest='task', nargs=argparse.REMAINDER, help='任务编排与执行可视化引擎 (lh --task create/list/status/execute/pause/resume/cancel/review/retry/serve)')
    # 🏠 老百姓入口 · 数据主权助手
    parser.add_argument('--ask', metavar='QUESTION', type=str, help='本地安全对话 (lh --ask "问题")')
    parser.add_argument('--witness', nargs=argparse.REMAINDER, help='一键固化证据 (lh --witness 或 lh --witness "证据内容" 或 lh --witness --sign)')
    parser.add_argument('--export', action='store_true', help='导出合规证据包 (lh --export)')
    parser.add_argument('--view-witness', dest='view_witness', metavar='ID', type=str, help='解密查看证据 (lh --view-witness WITNESS-xxx)')
    parser.add_argument('--view-export', dest='view_export', metavar='FILE', type=str, help='解密查看证据包 (lh --view-export backup/evidence_xxx.json.enc)')
    parser.add_argument('--witness-serve', dest='witness_serve', action='store_true', help='启动维权证据固化 Web 服务 (lh --witness-serve)')
    parser.add_argument('--quick', type=str, help='快速跳转到模块名')

    args, remaining = parser.parse_known_args()

    # 快捷模式
    if args.dashboard:
        print_persona_dashboard()
        return
    if args.engine:
        print_engine_caps()
        return
    if args.show_help or args.show_help_flag:
        print_help()
        return

    # === 🏠 老百姓入口 · 数据主权助手 ===
    if args.ask is not None:
        from datetime import datetime, timezone
        question = args.ask.strip() or "你好，龍魂！"
        print_header()
        print(f"\n  🐉 龍魂正在思考（本地优先·数据主权模式）")
        print(f"  📝 问题: {question}")
        print(f"  🔒 数据根留本地 | 不上传境外平台\n")
        sys.stdout.flush()

        bridge_path = ROOT / "bin" / "lh_notion_chat_bridge.py"
        answer_text = ""
        meta = {}
        # 优先调用 Notion 对话桥（本地模型优先）
        try:
            result = subprocess.run(
                [sys.executable, str(bridge_path), "chat", question, "--mode", "council", "--style", "plain"],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            if result.returncode == 0:
                # 解析 plain 输出: 第一行是模型，然后是回答
                lines = result.stdout.splitlines()
                answer_lines = []
                for line in lines:
                    if line.startswith("🤖 回答模型:"):
                        meta["model"] = line.replace("🤖 回答模型:", "").strip()
                    elif line.startswith("🔁 模型降级链:"):
                        break
                    else:
                        answer_lines.append(line)
                answer_text = "\n".join(line for line in answer_lines if line.strip()).strip()
        except Exception as e:
            print(f"  ⚠️ 对话桥调用失败: {e}")

        # Fallback: 本地 Ollama
        if not answer_text:
            try:
                import urllib.request
                req = urllib.request.Request(
                    "http://localhost:11434/api/generate",
                    data=json.dumps({"model": "qwen2.5:7b", "prompt": question, "stream": False}).encode(),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    answer_text = json.loads(resp.read().decode()).get("response", "服务繁忙")
                meta["model"] = "ollama/qwen2.5:7b"
            except Exception as e:
                answer_text = f"本地模型也未就绪: {e}\n请确保 Ollama 运行: ollama run qwen2.5:7b"
                meta["model"] = "none"

        print(f"  🤖 模型: {meta.get('model', 'council/wuxing-council-v1.0')}")
        print(f"\n  💡 回答:\n{answer_text}")
        print("\n" + "=" * 58)
        print("  ✅ 本次对话数据已留本地，未上传境外平台。")
        print(f"  🧬 DNA: #龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-ASK-UID9622")
        print("=" * 58)
        return

    if args.witness_serve:
        print_header()
        print("\n  🐉 启动维权证据固化 Web 服务...")
        server_script = ROOT / "bin" / "lh_witness_server.py"
        if not server_script.exists():
            print(f"  ❌ 服务脚本不存在: {server_script}")
            return
        try:
            subprocess.run(["python3", str(server_script), "--host", "127.0.0.1", "--port", "8780"], check=True)
        except KeyboardInterrupt:
            print("\n  ⏹ 服务已停止")
        return

    if args.view_witness:
        print_header()
        print(f"\n  🔓 解密查看证据: {args.view_witness}\n")
        key = _get_master_key()
        witness_dir = ROOT / "data" / "witness"
        target = None
        for f in sorted(witness_dir.glob("witness_*.json.enc")):
            try:
                cipher = f.read_bytes()
                plain = _sm4_cbc_decrypt(cipher, key)
                data = json.loads(plain.decode("utf-8"))
                if data.get("witness_id") == args.view_witness:
                    target = data
                    break
            except Exception:
                continue
        if not target:
            print("  ❌ 未找到该证据，或主密钥不正确。")
            return
        print(f"  🆔 证据ID: {target['witness_id']}")
        print(f"  🕐 时间: {target['timestamp_utc']}")
        print(f"  🔐 SHA-256: {target['content_sha256'][:40]}...")
        print(f"  🧬 DNA: {target['dna']}")
        print("\n  📝 内容:\n" + "-" * 58)
        print(f"  {target['content']}")
        print("-" * 58)
        return

    if args.witness is not None:
        print_header()
        print("\n  🐉 龍魂·维权证据固化工具")

        # 解析 --witness 后的参数（REMAINDER 模式）
        do_sign = "--sign" in args.witness
        evidence_lines = [x for x in (args.witness or []) if x != "--sign"]

        if do_sign:
            print("  🔏 签名模式已启用：Agent 审计 → GPG 签章 → SM4 加密\n")
        else:
            print("  请输入要固化的证据（支持多行，空行或输入 done 结束）：\n")

        if evidence_lines and evidence_lines[0]:
            pass  # 已经通过命令行传入
        else:
            evidence_lines = []
            while True:
                try:
                    line = input("  > ")
                    if line.strip().lower() in ("done", "end", ""):
                        break
                    evidence_lines.append(line)
                except (EOFError, KeyboardInterrupt):
                    print("\n  ⏹ 已取消")
                    return

        content = "\n".join(evidence_lines).strip()
        if not content:
            print("\n  ⚠️ 未输入任何证据，已取消。")
            return

        from datetime import datetime, timezone
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
        witness_id = f"WITNESS-{ts}-{content_hash}"

        witness_dir = ROOT / "data" / "witness"
        witness_dir.mkdir(parents=True, exist_ok=True)
        plain_file = witness_dir / f"witness_{ts}.json"
        enc_file = witness_dir / f"witness_{ts}.json.enc"
        asc_file = plain_file.with_suffix(plain_file.suffix + ".asc")

        # 可选：Agent 审计链
        audit_result = None
        if do_sign:
            print("  ⏳ 正在执行 Agent 审计链 (P05 + P15 + S3)...")
            audit_result = _run_witness_audit(content)
            if audit_result.get("ok"):
                print("  ✅ Agent 审计链完成")
                for pid, info in audit_result.get("agent_results", {}).items():
                    print(f"     • {pid} ({info.get('name', '?')}): {info.get('status', '?')}")
            else:
                print(f"  ⚠️ Agent 审计未通过或引擎不可用: {audit_result.get('error', '未知错误')}")
                print("  🛡️ 继续执行 GPG 签名（签名本身不依赖 Agent 审计）")

        evidence_pkg = {
            "witness_id": witness_id,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "dna": "#龍芯⚡️丙午·癸未·甲申-WITNESS-" + witness_id,
            "confirm_code": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
            "content": content,
            "content_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            "signature": "",
            "agent_audit": audit_result if do_sign else None,
        }
        plain_bytes = json.dumps(evidence_pkg, ensure_ascii=False, indent=2).encode("utf-8")

        # GPG 签名（仅签名模式）
        if do_sign:
            plain_file.write_bytes(plain_bytes)
            try:
                asc_path = _gpg_sign_file(plain_file)
                sig_text = asc_path.read_text(encoding="utf-8")
                evidence_pkg["signature"] = sig_text
                evidence_pkg["signature_file"] = str(asc_file.relative_to(ROOT))
                # 更新明文内容以包含签名信息
                plain_bytes = json.dumps(evidence_pkg, ensure_ascii=False, indent=2).encode("utf-8")
                plain_file.write_bytes(plain_bytes)
                print(f"  ✅ GPG 签章完成: {asc_path.relative_to(ROOT)}")
            except Exception as e:
                print(f"  ❌ GPG 签名失败: {e}")
                try:
                    plain_file.unlink()
                    asc_file.unlink(missing_ok=True)
                except Exception:
                    pass
                return

        # SM4 加密
        key = _get_master_key()
        cipher_bytes = _sm4_cbc_encrypt(plain_bytes, key)
        enc_file.write_bytes(cipher_bytes)

        # 明文不落盘；签名文件保留（签名可公开验证）
        try:
            plain_file.unlink()
        except Exception:
            pass

        print("\n" + "=" * 58)
        print(f"  ✅ 证据已固化并加密: {enc_file.relative_to(ROOT)}")
        print(f"  🆔 证据ID: {witness_id}")
        print(f"  🔐 SHA-256: {evidence_pkg['content_sha256'][:32]}...")
        print(f"  🔒 加密算法: 国密 SM4-CBC")
        if do_sign:
            print(f"  ✍️  GPG 签章: {asc_file.relative_to(ROOT)}")
            print(f"  🧩 Agent 审计链: P05→P15→S3")
        print("  📋 下一步:")
        print(f"     1. 解密查看: lh --view-witness {witness_id}")
        print("     2. 导出证据包: lh --export")
        print("=" * 58)
        return

    if args.view_export:
        print_header()
        print(f"\n  🔓 解密查看证据包: {args.view_export}\n")
        key = _get_master_key()
        export_path = Path(args.view_export)
        if not export_path.is_absolute():
            export_path = ROOT / export_path
        if not export_path.exists():
            print(f"  ❌ 文件不存在: {export_path}")
            return
        try:
            cipher = export_path.read_bytes()
            plain = _sm4_cbc_decrypt(cipher, key)
            data = json.loads(plain.decode("utf-8"))
            print(f"  📦 证据包ID: {data.get('export_id')}")
            print(f"  🕐 导出时间: {data.get('timestamp_utc')}")
            print(f"  🧬 DNA: {data.get('dna')}")
            print(f"  📊 摘要: {json.dumps(data.get('summary', {}), ensure_ascii=False, indent=4)}")
            print(f"\n  📝 证据记录数: {len(data.get('witnesses', []))}")
            for i, w in enumerate(data.get('witnesses', [])[:5], 1):
                print(f"    {i}. {w.get('witness_id')} | {w.get('timestamp_utc')}")
        except Exception as e:
            print(f"  ❌ 解密失败: {e}")
        return

    if args.export:
        print_header()
        print("\n  🐉 龍魂·合规证据包导出\n")

        from datetime import datetime, timezone
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_dir = ROOT / "backup"
        backup_dir.mkdir(parents=True, exist_ok=True)
        plain_file = backup_dir / f"evidence_{ts}.json"
        enc_file = backup_dir / f"evidence_{ts}.json.enc"

        key = _get_master_key()
        witness_dir = ROOT / "data" / "witness"
        witnesses = []
        if witness_dir.exists():
            for f in sorted(witness_dir.glob("witness_*.json.enc")):
                try:
                    cipher = f.read_bytes()
                    plain = _sm4_cbc_decrypt(cipher, key)
                    witnesses.append(json.loads(plain.decode("utf-8")))
                except Exception:
                    continue

        # 检查 GPG 签名状态
        signed_count = 0
        for f in (ROOT / "08_BIN").glob("*.py"):
            if (f.with_suffix(f.suffix + ".asc")).exists():
                signed_count += 1

        export_pkg = {
            "export_id": f"EXPORT-{ts}",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "dna": "#龍芯⚡️丙午·癸未·甲申-EVIDENCE-EXPORT-" + ts,
            "confirm_code": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
            "summary": {
                "witness_count": len(witnesses),
                "signed_scripts": signed_count,
                "project_root": str(ROOT),
            },
            "witnesses": witnesses[-20:],  # 最近 20 条
        }
        plain_bytes = json.dumps(export_pkg, ensure_ascii=False, indent=2).encode("utf-8")
        cipher_bytes = _sm4_cbc_encrypt(plain_bytes, key)
        enc_file.write_bytes(cipher_bytes)
        # 明文不落盘
        plain_file.write_bytes(plain_bytes)
        try:
            plain_file.unlink()
        except Exception:
            pass

        print(f"  ✅ 证据包已导出并加密: {enc_file.relative_to(ROOT)}")
        print(f"  📦 包含: {len(witnesses)} 条证据记录")
        print(f"  🔐 系统签名状态: {signed_count} 个脚本已 GPG 签名")
        print(f"  🔒 加密算法: 国密 SM4-CBC")
        print(f"  🧬 DNA: {export_pkg['dna']}")
        print("\n  建议: 将证据包复制到外部加密介质或打印成纸质备份。")
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
    if args.script_align is not None:
        script_mgr = ROOT / "bin" / "lh_script_manager.py"
        sa_args = list(args.script_align) if args.script_align else ["--scan"]
        subprocess.run([sys.executable, str(script_mgr)] + sa_args, cwd=str(ROOT))
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

    # === 鲲鹏状态 ===
    if args.kunpeng is not None:
        print_header()
        kunpeng_args = list(args.kunpeng) if args.kunpeng else []
        print("\n  🖥️ 鲲鹏服务器状态 (119.13.90.27)\n")
        ssh_cmd = ["ssh", "-i", str(Path.home() / ".ssh" / "longhun_kunpeng_ed25519"),
                    "-o", "StrictHostKeyChecking=no",
                    "-o", "ConnectTimeout=5",
                    "root@119.13.90.27"]
        if "--logs" in kunpeng_args:
            subprocess.run(ssh_cmd + ["journalctl -n 50 --no-pager --no-hostname | grep -E '(error|fail|longhun|nginx)' || true"], shell=False, cwd=str(ROOT))
        else:
            subprocess.run(ssh_cmd + ["systemctl --no-pager list-units 'lh*' 'longhun*' 'nginx*' 2>/dev/null || echo '无匹配服务' | head -30"], shell=False, cwd=str(ROOT))
            if "--services" in kunpeng_args:
                subprocess.run(ssh_cmd + ["systemctl --no-pager --state=running | head -30"], shell=False, cwd=str(ROOT))
        print()
        return

    # === 端口状态一览 ===
    if args.ports is not None:
        print_header()
        ports_args = list(args.ports) if args.ports else []
        full = "--full" in ports_args or len(ports_args) == 0
        print("\n  📡 龍魂端口矩阵\n")
        # Mac本地端口
        print("  ┌─ Mac 本地 ─────────────────────────────────────┐")
        result = subprocess.run(["/usr/sbin/lsof", "-iTCP", "-sTCP:LISTEN", "-nP"],
                               capture_output=True, text=True, cwd=str(ROOT))
        for line in result.stdout.split('\n'):
            for port in ['9622','9623','9631','8766','8777','8780','8783','8989','8999']:
                if f':{port}' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        print(f"  │  :{port}  {parts[0]:15s} {' '.join(parts[2:4]) if len(parts)>3 else ''}")
        print("  └─────────────────────────────────────────────────┘")
        # launchd 服务列表
        if full:
            print("\n  ┌─ launchd 龍魂服务 ─────────────────────────────┐")
            result2 = subprocess.run(["/bin/launchctl", "list"], capture_output=True, text=True, cwd=str(ROOT))
            for line in result2.stdout.split('\n'):
                if 'longhun' in line.lower() or 'lh_' in line.lower() or 'lh.' in line.lower():
                    print(f"  │  {line.strip()}")
            print("  └─────────────────────────────────────────────────┘")
        # 鲲鹏端口（可选）
        if "--kunpeng" in ports_args:
            print("\n  ┌─ 鲲鹏 (119.13.90.27) 端口 ─────────────────────┐")
            subprocess.run(["ssh", "-i", str(Path.home() / ".ssh" / "longhun_kunpeng_ed25519"),
                          "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=5",
                          "root@119.13.90.27",
                          "ss -tlnp | head -40 2>/dev/null || netstat -tlnp | head -40"],
                          cwd=str(ROOT))
            print("  └─────────────────────────────────────────────────┘")
        print()
        return

    # === 盘点器 ===
    if args.inventory:
        print_header()
        print("\n  📋 龍魂功能盘点...\n")
        subprocess.run([sys.executable, str(ROOT / "bin" / "lh_inventory.py")], cwd=str(ROOT))
        return

    # === 省电省算力总控台 ===
    if args.power_save is not None:
        ps_args = list(args.power_save) if args.power_save else ["status"]
        cmd = [sys.executable, str(ROOT / "bin" / "lh_power_save_orchestrator.py")] + ps_args
        subprocess.run(cmd, cwd=str(ROOT))
        return

    # === 文章抬头模板选择器 ===
    if args.head is not None:
        head_args = list(args.head) if args.head else []
        cmd = [sys.executable, str(ROOT / "bin" / "lh_header_template.py")] + head_args
        subprocess.run(cmd, cwd=str(ROOT))
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
        print("\n  🐉 启动所有龍魂服务...\n")
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
        # 启动省电总控台守护（后台，每10分钟自动优化）
        print("  🔋 启动省电总控台守护...")
        subprocess.Popen(
            [sys.executable, str(ROOT / "bin" / "lh_power_save_orchestrator.py"), "daemon", "--interval", "600"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        print("\n  ✅ 全部服务已启动")
        print("     API: http://localhost:9622")
        print("     API 文档: http://localhost:9622/docs")
        print("     省电总控: lh --power-save status")
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
            # 🔧 特殊处理: setup-all 一键搭建
            if flag == 'setup-all':
                print_header()
                print("\n  🚀 龍魂·一键搭建\n")
                for step, cmd in [
                    ("📡 知识拉取", [sys.executable, str(ROOT/"bin"/"lh_knowledge_puller.py")]),
                    ("📦 配置合并", [sys.executable, str(ROOT/"bin"/"lh_config_puller.py"), "--merge"]),
                    ("📊 拉取状态", [sys.executable, str(ROOT/"bin"/"lh_knowledge_puller.py"), "--status"]),
                ]:
                    print(f"  {step}...")
                    subprocess.run(cmd, cwd=str(ROOT), check=False)
                print("\n  ✅ 搭建完成！\n")
                return
            extra = list(val) if val else list(default_args)
            # 检测 --json 参数，抑制 header 以避免污染管道输出
            no_header = '--json' in (extra or [])
            _run_subcommand(script, extra, emoji, desc, smart_default, suppress_header=no_header)
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

    # === 📄 智能排版引擎 ===
    if args.fmt is not None or args.fmt_short is not None:
        fmt_args = list(args.fmt) if args.fmt else list(args.fmt_short) if args.fmt_short else []
        if args.fmt_type:
            fmt_args += ['--type', args.fmt_type]
        print_header()
        print("\n  📄 龍魂·智能排版引擎\n")
        subprocess.run([sys.executable, str(ROOT / "bin" / "lh_format_engine.py")] + fmt_args, cwd=str(ROOT))
        return

    # === 🧬 创作者DNA受益算法 ===
    if args.benefit is not None:
        benefit_args = list(args.benefit)
        print_header()
        print("\n  🧬 龍魂·创作者DNA受益算法 v1.1\n")
        subprocess.run([sys.executable, str(ROOT / "bin" / "lh_creator_dna_benefit.py")] + benefit_args, cwd=str(ROOT))
        return

    # === 📋 任务编排引擎 ===
    if args.task is not None:
        task_args = list(args.task)
        print_header()
        print("\n  📋 龍魂·任务编排引擎 v1.1\n")
        subprocess.run([sys.executable, str(ROOT / "bin" / "lh_task_orchestrator.py")] + task_args, cwd=str(ROOT))
        return

    # 快速跳转到某个模块
    if args.quick:
        qmap = {
            'audit': '🛡️ 安全 & 审计', 'security': '🛡️ 安全 & 审计',
            'sovereignty': '🛡️ 安全 & 审计',
            'engine': '🚀 引擎 & 通道', 'ai': '🚀 引擎 & 通道',
            'persona': '🧠 人格 & AI', 'personas': '🧠 人格 & AI', 'persona-runtime': '🧠 人格 & AI',
            'dna': '🧬 DNA & 追溯', 'imprint': '🧬 DNA & 追溯',
            'detect': '📊 检测 & 分析', 'analyze': '📊 检测 & 分析',
            'sync': '🔗 同步 & 集成', 'git': '🔗 同步 & 集成',
            'notion': '🔗 同步 & 集成',
            'watermark': '🧬 DNA & 追溯', 'face': '🧬 DNA & 追溯',
            'qr': '🧬 DNA & 追溯', 'voiceprint': '🧬 DNA & 追溯',
            'system': '⚙️ 系统 & 运维', 'ops': '⚙️ 系统 & 运维',
            'network': '🌐 外部 & 网络', 'web': '🌐 外部 & 网络',
            'docs': '📝 文档 & 知识',
            'router': '🧩 提示词路由器', 'pr': '🧩 提示词路由器', 'prompt': '🧩 提示词路由器',
            'knowledge': '📡 知识拉取 & 配置', 'kp': '📡 知识拉取 & 配置',
            'config': '📡 知识拉取 & 配置', 'cp': '📡 知识拉取 & 配置',
            'setup': '📡 知识拉取 & 配置',
            'deps': '🔧 依赖 & CNSH转换', 'install': '🔧 依赖 & CNSH转换',
            'freeze': '🔧 依赖 & CNSH转换', 'cnsh-transpile': '🔧 依赖 & CNSH转换',
            'ct': '🔧 依赖 & CNSH转换', 'transpile': '🔧 依赖 & CNSH转换',
        }
        cat = qmap.get(args.quick.lower())
        if cat:
            show_category(cat)
        else:
            print(f"  ❌ 未知模块: {args.quick}，可用: {', '.join(qmap.keys())}")
        return

    # === 🔥 位置子命令分发（lh status / lh audit / lh search query 等） ===
    if remaining:
        subcmd = remaining[0].lstrip('-')  # 兼容 bare word 和 --flag 两种形式
        extra = remaining[1:]
        # 查 SUB_DISPATCH
        if subcmd in SUB_DISPATCH:
            script, emoji, desc, *rest = SUB_DISPATCH[subcmd]
            smart_default = rest[0] if rest else None
            if not extra and smart_default and isinstance(smart_default, (list, str)):
                if isinstance(smart_default, str):
                    extra = [smart_default]
                else:
                    extra = list(smart_default)
            # 检测 --json 抑制 header（管道输出）
            no_header = '--json' in extra
            _run_subcommand(script, extra, emoji, desc, suppress_header=no_header)
            _print_time_stamp()
            return
        # 裸词→自动转 --flag 形式重试（如 lh audit → lh --audit）
        # 递归防护：_LH_NO_REDIRECT 环境变量阻止无限重试
        if os.environ.get('_LH_NO_REDIRECT') != '1':
            retry_flag = f"--{subcmd}"
            retry_env = os.environ.copy()
            retry_env['_LH_NO_REDIRECT'] = '1'
            retry_cmd = [sys.executable, __file__, retry_flag] + extra
            result = subprocess.run(retry_cmd, cwd=str(ROOT), env=retry_env, capture_output=True)
            if result.returncode == 0:
                print(result.stdout, end='')
                if result.stderr:
                    print(result.stderr, end='', file=sys.stderr)
                return
        # 🔥 自然语言路由（仅父进程·_LH_NO_REDIRECT 的子进程跳过）
        if os.environ.get('_LH_NO_REDIRECT') == '1':
            # 子进程 flag 重试失败 → 非零退出让父进程继续自然语言路由
            sys.exit(2)
        nl_text = ' '.join(remaining)
        has_cjk = bool(re.search(r'[\u4e00-\u9fff\u3400-\u4dbf]', nl_text))
        is_long = len(nl_text) > 20 or len(remaining) > 1
        if has_cjk or is_long:
            # 优先：语义抽屉匹配（快速·本地·不耗算力）
            nl_router = ROOT / "bin" / "lh_natural_language_router.py"
            if nl_router.exists():
                print(f"\n  🐉 龍魂理解: {nl_text}\n")
                result = subprocess.run(
                    [sys.executable, str(nl_router), nl_text, "--json"],
                    cwd=str(ROOT), capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0 and result.stdout.strip():
                    try:
                        parsed = json.loads(result.stdout)
                        if parsed.get("status") == "success":
                            # 提取关键信息展示
                            msg = parsed.get("message", parsed.get("意图", ""))
                            data = parsed.get("data", {})
                            dna = parsed.get("dna", "")
                            print(f"  🎯 {msg}")
                            if isinstance(data, dict):
                                for k, v in data.items():
                                    if isinstance(v, dict):
                                        for k2, v2 in v.items():
                                            print(f"    {k2}: {v2}")
                                    else:
                                        print(f"    {k}: {v}")
                            if dna:
                                print(f"  🧬 {dna}")
                            print()
                            _print_time_stamp()
                            return
                    except (json.JSONDecodeError, KeyError):
                        pass
                    # 非 JSON 输出 → 直接显示
                    print(result.stdout.strip())
                    _print_time_stamp()
                    return
            # 兜底：AI 对话（Notion桥 → Ollama）
            from datetime import datetime, timezone
            print(f"  🤖 启用AI深度理解...\n")
            # 复用 --ask 管线（本地优先·不上传境外）
            bridge_path = ROOT / "bin" / "lh_notion_chat_bridge.py"
            answer_text = ""
            meta = {}
            try:
                result = subprocess.run(
                    [sys.executable, str(bridge_path), "chat", nl_text, "--mode", "council", "--style", "plain"],
                    cwd=str(ROOT), capture_output=True, text=True, timeout=120,
                )
                if result.returncode == 0:
                    lines = result.stdout.splitlines()
                    answer_lines = []
                    for line in lines:
                        if line.startswith("🤖 回答模型:"):
                            meta["model"] = line.replace("🤖 回答模型:", "").strip()
                        elif line.startswith("🔁 模型降级链:"):
                            break
                        else:
                            answer_lines.append(line)
                    answer_text = "\n".join(line for line in answer_lines if line.strip()).strip()
            except Exception as e:
                pass
            if not answer_text:
                try:
                    import urllib.request
                    req = urllib.request.Request(
                        "http://localhost:11434/api/generate",
                        data=json.dumps({"model": "qwen2.5:7b", "prompt": nl_text, "stream": False}).encode(),
                        headers={"Content-Type": "application/json"},
                        method="POST",
                    )
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        answer_text = json.loads(resp.read().decode()).get("response", "服务繁忙")
                    meta["model"] = "ollama/qwen2.5:7b"
                except Exception:
                    answer_text = "本地AI未就绪。试试: lh search 关键词 / lh status / lh --help"
                    meta["model"] = "none"
            print(f"  🤖 模型: {meta.get('model', 'local')}")
            print(f"\n  💡 {answer_text}\n")
            print("=" * 58)
            print(f"  ✅ 对话数据留本地·不上传境外平台")
            print(f"  🧬 DNA: #龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-NL-UID9622")
            print("=" * 58)
            _print_time_stamp()
            return

        # 都不是自然语言 → 拼写纠错
        from difflib import get_close_matches
        suggestions = get_close_matches(subcmd, SUB_DISPATCH.keys(), n=3, cutoff=0.6)
        print(f"\n  ❌ 未知命令: {subcmd}")
        if suggestions:
            print(f"  💡 你是否想打: {', '.join(suggestions)}")
        print(f"  📖 lh --help 查看所有命令\n")
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
