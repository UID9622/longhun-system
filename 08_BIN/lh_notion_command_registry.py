#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·癸亥·子时·䷮困-NOTION-CMD-REGISTRY-v2.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂 · Notion 指令注册表同步工具 v2.0

把执行过的指令、修复动作、验证命令固定成 Notion 数据库表格，
并提供「总开关」一键体检 /「分布式开关」按阶段执行。

用法:
    # 1. 创建数据库（只需一次）
    python3 08_BIN/lh_notion_command_registry.py create-db \
        --parent-page-id 3b97125a-9c9f-815c-a0eb-ce7c995e5753

    # 2. 推送/更新指令行到 Notion
    python3 08_BIN/lh_notion_command_registry.py push

    # 3. 总开关 · 一键体检（只读·安全）
    python3 08_BIN/lh_notion_command_registry.py run check --all

    # 4. 分布式开关 · 执行某一阶段
    python3 08_BIN/lh_notion_command_registry.py run exec --category A --dry-run
    python3 08_BIN/lh_notion_command_registry.py run exec --category A --yes

    # 5. 校验 Notion 表格与本地清单是否一致
    python3 08_BIN/lh_notion_command_registry.py verify

配置来源:
    config/notion_config.json            # notion_token
    config/notion_command_registry.json  # database_id（创建后自动生成）

协议: CC BY-NC-SA 4.0 (思想层) · MulanPSL v2 (工程层)
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.longhun_core.dna_trace import generate_dna

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "notion_config.json"
REGISTRY_CONFIG_PATH = PROJECT_ROOT / "config" / "notion_command_registry.json"
REPORT_DIR = PROJECT_ROOT / "12_DOCS" / "agent_reports"

CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
NOTION_API_VERSION = "2022-06-28"


# ═══════════════════════════════════════════════════════
# 指令数据（Phase A/B/C/D + 关键修复/验证）
# 模式: 验证(只读) / 执行(会改数据) / 手动(需人工)
# 开关类型: 总开关 / 分布式开关 / 手动
# ═══════════════════════════════════════════════════════
COMMAND_ROWS: List[Dict[str, Any]] = [
    {
        "指令名称": "A1 · 多语言语义复核（LANG 层）",
        "阶段": "Phase A",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "对 ASI 测试套件中 24 个语言场景的 ⚠️ 条目调用本地模型做语义复核，输出复核报告。",
        "执行命令": "python3 08_BIN/asi_test_runner.py --semantic-review --category LANG --model qwen2.5:1.5b",
        "目标文件": "08_BIN/asi_test_runner.py, 12_DOCS/agent_reports/asi_semantic_review_*.md",
        "验证方式": "查看报告：24 场景 / ✅15 / ⚠️9 / 通过率 62.5%",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-ASI-SEMANTIC-LANG-UID9622",
        "备注": "分布式开关：执行 Phase A。⚠️ 条目为模型语义不确定项，需随模型迭代重跑。",
    },
    {
        "指令名称": "A2 · 生成语言层专项报告",
        "阶段": "Phase A",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "按 LANG 类别生成 Markdown 专项报告，用于人工复核与训练反馈。",
        "执行命令": "python3 08_BIN/asi_test_runner.py --report --category LANG --format md",
        "目标文件": "12_DOCS/agent_reports/asi_test_report_*.md",
        "验证方式": "检查报告文件是否存在且包含 LANG 明细",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-ASI-LANG-REPORT-UID9622",
        "备注": "分布式开关：执行 Phase A。可与 A1 联动执行。",
    },
    {
        "指令名称": "B1 · 手动触发合规巡检",
        "阶段": "Phase B",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "立即执行一次全量 ASI 89 场景合规巡检，生成报告。",
        "执行命令": "/opt/cnsh-ide/08_BIN/asi_watchdog.sh",
        "目标文件": "08_BIN/asi_watchdog.sh, /opt/cnsh-ide/12_DOCS/agent_reports/asi_test_report_*.md",
        "验证方式": "报告输出 89/63/0/0（总/通过/警告/失败）",
        "状态": "已落地",
        "适用环境": ["鲲鹏"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-ASI-WATCHDOG-UID9622",
        "备注": "分布式开关：执行 Phase B。鲲鹏 cron 每 6 小时自动触发一次。",
    },
    {
        "指令名称": "B2 · 注册合规巡检模块",
        "阶段": "Phase B",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "将 ASI 测试套件注册到融合系统的合规巡检 watchdog。",
        "执行命令": "python3 08_BIN/asi_test_runner.py --register --module compliance-watchdog",
        "目标文件": "08_BIN/asi_test_runner.py",
        "验证方式": "巡检模块列表包含 compliance-watchdog",
        "状态": "已落地",
        "适用环境": ["本地", "鲲鹏"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-ASI-REGISTER-WATCHDOG-UID9622",
        "备注": "分布式开关：执行 Phase B。注册后 B1/B3 才能正确识别模块身份。",
    },
    {
        "指令名称": "B3 · 启动自动化巡检（cron）",
        "阶段": "Phase B",
        "模式": "手动",
        "开关类型": "手动",
        "功能描述": "每 6 小时自动执行 ASI 全量巡检并生成报告。",
        "执行命令": "crontab -e  # 添加: 0 */6 * * * cd /opt/longhun-system && python3 08_BIN/asi_test_runner.py --auto --report --notify",
        "目标文件": "鲲鹏 crontab",
        "验证方式": "systemctl 日志或 cron 日志显示定时执行",
        "状态": "已落地",
        "适用环境": ["鲲鹏"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-ASI-CRON-WATCHDOG-UID9622",
        "备注": "手动项：crontab -e 是交互式编辑，不能一键自动执行。如需非交互安装，告诉我写 install 脚本。",
    },
    {
        "指令名称": "C1 · 文明档案馆哈希链验证",
        "阶段": "Phase C",
        "模式": "验证",
        "开关类型": "总开关",
        "功能描述": "验证文明档案馆所有 entry 的 SHA-256 哈希链完整性，发现篡改即 🔴。",
        "执行命令": "python3 08_BIN/civilization_archive.py --verify",
        "目标文件": "08_BIN/civilization_archive.py, data/civilization_archive.db",
        "验证方式": "输出 🟢 哈希链完整",
        "状态": "已落地",
        "适用环境": ["本地", "鲲鹏"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-CIV-ARCHIVE-VERIFY-UID9622",
        "备注": "总开关：一键体检。本地 67 条 / 鲲鹏 68 条均验证通过。",
    },
    {
        "指令名称": "C2 · 生成文明备份完整性报告",
        "阶段": "Phase C",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "导出文明档案馆完整报告（Markdown + JSON），含哈希链与统计。",
        "执行命令": "python3 08_BIN/civilization_archive.py --report --export",
        "目标文件": "12_DOCS/agent_reports/civilization_archive_report_*.md",
        "验证方式": "报告含 entry 总数、哈希样例、完整性结论",
        "状态": "已落地",
        "适用环境": ["本地", "鲲鹏"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-CIV-ARCHIVE-REPORT-UID9622",
        "备注": "分布式开关：执行 Phase C。可与 C1 联动执行。",
    },
    {
        "指令名称": "C3 · 备份文明档案到贵州云",
        "阶段": "Phase C",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "将文明档案馆数据库加密打包，备份到 iCloud 云上贵州路径。",
        "执行命令": "python3 08_BIN/civilization_archive.py --backup --remote guizhou-cloud",
        "目标文件": "~/Library/Mobile Documents/com~apple~CloudDocs/龍魂系统备份/P0_文明DNA/CIVILIZATION_ARCHIVE_*.tar.gpg",
        "验证方式": "文件存在且 GPG 加密，大小与本地 DB 相近",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-CIV-ARCHIVE-BACKUP-UID9622",
        "备注": "分布式开关：执行 Phase C。鲲鹏暂存 /backup/guizhou_archive/，需二次同步到贵州云。",
    },
    {
        "指令名称": "D1 · 验证外网 API 合规检测",
        "阶段": "Phase D",
        "模式": "验证",
        "开关类型": "总开关",
        "功能描述": "通过 curl 测试外网合规检测接口是否按人格返回结果。",
        "执行命令": "curl -X POST http://119.13.90.27:8080/cnsh/api/compliance/check -H 'Content-Type: application/json' -d '{\"text\":\"测试内容\",\"lang\":\"zh\",\"persona\":\"堂吉诃德\"}'",
        "目标文件": "08_BIN/cnsh_web_ide.py",
        "验证方式": "HTTP 200，返回 JSON 含 persona/result/rating",
        "状态": "已落地",
        "适用环境": ["鲲鹏"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-API-COMPLIANCE-CHECK-UID9622",
        "备注": "总开关：一键体检。119.13.90.27 为鲲鹏外网 IP。",
    },
    {
        "指令名称": "D2 · API 限流压力测试",
        "阶段": "Phase D",
        "模式": "验证",
        "开关类型": "总开关",
        "功能描述": "验证 RateLimiter 中间件：阈值内返回 200，超限返回 429。",
        "执行命令": "for i in {1..5}; do curl -s -o /dev/null -w '%{http_code} ' -f http://119.13.90.27:8080/cnsh/api/ai/providers; done",
        "目标文件": "08_BIN/cnsh_web_ide.py",
        "验证方式": "前 4 次 200，第 5 次 429，响应头含 X-RateLimit-*",
        "状态": "已落地",
        "适用环境": ["鲲鹏"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-API-RATE-LIMIT-TEST-UID9622",
        "备注": "总开关：一键体检。默认 100 请求 / 60 秒 / IP / 端点。",
    },
    {
        "指令名称": "通用 · 检查鲲鹏 IDE 服务状态",
        "阶段": "通用",
        "模式": "验证",
        "开关类型": "总开关",
        "功能描述": "查看 cnsh-ide systemd 服务运行状态。",
        "执行命令": "ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27 'systemctl status cnsh-ide.service --no-pager'",
        "目标文件": "鲲鹏 systemd /etc/systemd/system/cnsh-ide.service",
        "验证方式": "Active: active (running)",
        "状态": "已落地",
        "适用环境": ["鲲鹏"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-KUNPENG-SERVICE-CHECK-UID9622",
        "备注": "总开关：一键体检。服务异常时执行 restart。",
    },
    {
        "指令名称": "通用 · 打开本地 CNSH IDE",
        "阶段": "通用",
        "模式": "手动",
        "开关类型": "手动",
        "功能描述": "本地 Web IDE 入口，用于 AI 对话与 CNSH 编译。",
        "执行命令": "open http://127.0.0.1:8848",
        "目标文件": "08_BIN/cnsh_web_ide.py",
        "验证方式": "页面可访问，AI 接口/providers/config 正常",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-LOCAL-IDE-UID9622",
        "备注": "手动项：会调起浏览器。鲲鹏外网版：http://119.13.90.27:8080/cnsh/",
    },
    {
        "指令名称": "修复 · DNA 生成器日柱/月柱/卦象校正",
        "阶段": "修复",
        "模式": "验证",
        "开关类型": "总开关",
        "功能描述": "修正官方 DNA 生成器的日柱偏移、节气月支、通行本卦象序号映射。",
        "执行命令": "python3 08_BIN/lh_day_gua_verify.py --cross-check",
        "目标文件": "08_BIN/lh_dna_generator.py, 08_BIN/lh_day_gua_verify.py",
        "验证方式": "2026-08-12 = 丙午·丙申·戊午；2024-02-10 = 甲辰日；坤上坤下 = 坤#2",
        "状态": "已落地",
        "适用环境": ["本地", "鲲鹏"],
        "DNA": "#龍芯⚡️丙午·丙酉·壬戌·亥时·䷬萃-NOTION-CLI-v1.0-UID9622-B18B81B3",
        "备注": "总开关：一键体检。历史 DNA 可能需全量重算差异报告。",
    },
    {
        "指令名称": "修复 · 鲲鹏 calendar 反代与 H 武器真实联动",
        "阶段": "修复",
        "模式": "手动",
        "开关类型": "手动",
        "功能描述": "在 nginx 80 块挂载 /calendar/；修复 HWeaponSimulator 因 parents[4] 路径越界导致的降级。",
        "执行命令": "bash 08_BIN/deploy_kunpeng.sh calendar-sync",
        "目标文件": "08_BIN/deploy_kunpeng.sh, nginx /etc/nginx/conf.d/*-uid9622.cn.conf, 08_BIN/lh_civilization_gene_mapper.py",
        "验证方式": "http://uid9622.cn/calendar/ 200；H 武器收敛分 7.6/PATH-07",
        "状态": "已落地",
        "适用环境": ["本地", "鲲鹏"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-CALENDAR-DEPLOY-UID9622",
        "备注": "手动项：会改鲲鹏 nginx 配置并部署。订阅源动态适配 location.origin。",
    },
    {
        "指令名称": "启动 · 会话自举（焊死）",
        "阶段": "启动",
        "模式": "手动",
        "开关类型": "手动",
        "功能描述": "新终端窗口启动时自动输出会话 DNA，并调用总开关一键体检。",
        "执行命令": "已写入 ~/.zshrc，无需手动执行；如需手动：python3 08_BIN/lh_session_boot.py",
        "目标文件": "08_BIN/lh_session_boot.py, ~/.zshrc",
        "验证方式": "新开终端窗口应看到 🐉 龍魂会话自举横幅与 5/5 体检结果",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·丙酉·癸亥·子时·䷮困-SESSION-BOOT-UID9622",
        "备注": "已焊死在 ~/.zshrc。如要关闭，注释 ~/.zshrc 末尾 LONGHUN_SESSION_BOOTED 块。",
    },
    {
        "指令名称": "P0 · 铁律自审闸",
        "阶段": "P0",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "检查文本/文件是否命中龍魂铁律红线（简体龙、蒸馏词、隐私泄露、主权出口风险、人民原声阉割）。",
        "执行命令": "lh iron --text \"要审查的文本\"  # 或 --file path/to/doc.md --json",
        "目标文件": "08_BIN/lh_iron_law_gate.py, .kimi-code/skills/longhun-iron-laws/scripts/iron_law_gate.sh",
        "验证方式": "lh iron --text \"龙魂\" --json 应返回 🔴；--text \"龍魂\" 应返回 🟢",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·丙戌·乙丑·卯时·䷯井-IRON-LAW-GATE-v1.0-UID9622",
        "备注": "P0 落地项。可接入 CI/pre-commit 自动审查对外输出。",
    },
    {
        "指令名称": "P0 · 君子协议诚信评级",
        "阶段": "P0",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "注册主体、记录贡献/违约/道德/人品事件，计算综合信用分 S = 0.4M + 0.3P + 0.3I，三级清算。",
        "执行命令": "lh trust register <uid> [--name NAME] && lh trust contribute <uid> code && lh trust query <uid>",
        "目标文件": "08_BIN/lh_trust_protocol.py, .kimi-code/skills/longhun-trust-protocol/scripts/trust_protocol.sh",
        "验证方式": "lh trust list 显示已注册主体及 S 分",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·丙戌·乙丑·卯时·䷯井-TRUST-PROTOCOL-v1.0-UID9622",
        "备注": "P0 落地项。数据存 ~/.longhun/trust_protocol/ledger.json，带 SHA-256 链式哈希。",
    },
    {
        "指令名称": "P0 · 工作流程透明化",
        "阶段": "P0",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "把用户请求拆成 15 步五阶段工作流，自动关键词路由、铁律自审、六层来源链盖章，输出 JSON/Markdown/JSONL。",
        "执行命令": "lh workflow --message \"龍魂 CNSH 系统复盘\" --output-dir ./wf",
        "目标文件": "08_BIN/lh_workflow_transparent.py, .kimi-code/skills/longhun-workflow-transparent/scripts/workflow_transparent.sh",
        "验证方式": "生成 workflow_transparent_*.json / .md / .jsonl 三件套",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·丙戌·乙丑·卯时·䷯井-WORKFLOW-TRANSPARENT-v1.0-UID9622",
        "备注": "P0 落地项。每个产物带 DNA、确认码、六层来源链。",
    },
    {
        "指令名称": "P0 · 龍魂中枢事件总线 LCB",
        "阶段": "P0",
        "模式": "执行",
        "开关类型": "总开关",
        "功能描述": "为所有技能提供统一事件发布/订阅/消费总线，是自动迭代飞轮的基础设施。",
        "执行命令": "lh event publish --topic skill.execution --source <skill> --type <type> --payload '{...}'",
        "目标文件": "08_BIN/lh_event_bus.py",
        "验证方式": "lh event stats 显示总事件数与订阅者；lh event list 查看事件流",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·丙戌·乙丑·卯时·䷯井-EVENT-BUS-v1.0-UID9622",
        "备注": "P0 基础设施。支持 listen 守护模式与 handler 回调。",
    },
    {
        "指令名称": "P0 · 治理流水线执行器",
        "阶段": "P0",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "包装任意命令，自动执行 workflow-transparent → iron-laws → 执行 → trust-protocol → event-bus → audit 六步。",
        "执行命令": "lh governed --cmd 'lh iron --text \"龍魂\" --json' --desc '铁律检查'",
        "目标文件": "08_BIN/lh_governed_exec.py",
        "验证方式": "执行后产生审计归档 12_DOCS/agent_reports/governed_exec/*.json 并向事件总线发布 governed.execution 事件",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·丙戌·乙丑·卯时·䷯井-GOVERNED-EXEC-v1.0-UID9622",
        "备注": "P0 基础设施。建议所有对外影响的命令都通过本包装器执行。",
    },
    {
        "指令名称": "P1 · Agent 编排器技能发现",
        "阶段": "P1",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "扫描 ~/.kimi-code/skills 与 ~/.agents/skills 目录，解析 SKILL.md 的 YAML frontmatter，生成统一技能索引。",
        "执行命令": "lh orchestrator discover",
        "目标文件": "08_BIN/lh_agent_orchestrator.py, ~/.longhun/agent_orchestrator/skill_index.json",
        "验证方式": "lh orchestrator stats 显示技能总数 > 0；索引含 name/description/keywords/scope 字段",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-AGENT-ORCHESTRATOR-v1.0-UID9622",
        "备注": "P1 落地项。技能索引是自动路由与多 Agent 协作的前提。",
    },
    {
        "指令名称": "P1 · 列出已发现技能",
        "阶段": "P1",
        "模式": "验证",
        "开关类型": "分布式开关",
        "功能描述": "按 scope/keyword 过滤查看已索引技能清单。",
        "执行命令": "lh orchestrator list --scope kimi --limit 10",
        "目标文件": "08_BIN/lh_agent_orchestrator.py",
        "验证方式": "输出技能 id + scope + 描述摘要",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-AGENT-ORCHESTRATOR-v1.0-UID9622",
        "备注": "分布式开关：索引只读查询，安全。",
    },
    {
        "指令名称": "P1 · 输入路由到技能/人格",
        "阶段": "P1",
        "模式": "验证",
        "开关类型": "分布式开关",
        "功能描述": "根据输入文本匹配最佳技能与 117 人格注册表中的推荐人格，输出推荐动作。",
        "执行命令": "lh orchestrator route --text \"帮我写个部署脚本\"",
        "目标文件": "08_BIN/lh_agent_orchestrator.py, 08_BIN/persona_registry.json",
        "验证方式": "命中 longhun-creator / longhun-cloud-deploy 等技能，并推荐 P04 鲁班等人格",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-AGENT-ORCHESTRATOR-v1.0-UID9622",
        "备注": "分布式开关：只读路由，不执行。结果追加到 route_log.jsonl。",
    },
    {
        "指令名称": "P1 · 执行推荐技能",
        "阶段": "P1",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "先路由，再调用治理流水线执行最佳技能（优先 skill/scripts/*.py）。",
        "执行命令": "lh orchestrator run \"帮我备份系统\" [--args ...]",
        "目标文件": "08_BIN/lh_agent_orchestrator.py, 08_BIN/lh_governed_exec.py",
        "验证方式": "生成 governed_exec 审计归档并向事件总线发布 skill.execution 事件",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-AGENT-ORCHESTRATOR-v1.0-UID9622",
        "备注": "分布式开关：执行前先用 --dry-run 查看将要执行的命令。",
    },
    {
        "指令名称": "P1 · 启动监听模式（自动路由事件）",
        "阶段": "P1",
        "模式": "执行",
        "开关类型": "手动",
        "功能描述": "作为守护进程监听事件总线，收到 skill.execution/route_request 类型事件后自动路由并记录。",
        "执行命令": "lh orchestrator listen --interval 5 --limit 10",
        "目标文件": "08_BIN/lh_agent_orchestrator.py, 08_BIN/lh_event_bus.py",
        "验证方式": "发布事件后，route_log.jsonl 出现 auto:true 的自动路由记录",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-AGENT-ORCHESTRATOR-v1.0-UID9622",
        "备注": "手动项：常驻前台，可用 systemd/nohup 守护。未来接入 cron 或 daemon。",
    },
    {
        "指令名称": "P1 · 编排器统计",
        "阶段": "P1",
        "模式": "验证",
        "开关类型": "总开关",
        "功能描述": "一键查看技能索引规模、分域统计、历史路由次数。",
        "执行命令": "lh orchestrator stats",
        "目标文件": "08_BIN/lh_agent_orchestrator.py",
        "验证方式": "输出 total_skills / scope_counts / total_routes",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-AGENT-ORCHESTRATOR-v1.0-UID9622",
        "备注": "总开关：一键体检。适合排查索引是否过期、路由是否活跃。",
    },
    {
        "指令名称": "P2 · Agent 编排器守护进程启动",
        "阶段": "P2",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "以后台进程启动 Agent 编排器，常驻监听事件总线并自动路由事件到技能/人格。",
        "执行命令": "lh agent-daemon start --interval 5 --limit 10",
        "目标文件": "08_BIN/lh_agent_daemon.py, 08_BIN/lh_agent_orchestrator.py, 08_BIN/lh_event_bus.py",
        "验证方式": "lh agent-daemon status 显示 🟢 运行中；发布事件后 route_log.jsonl 出现 auto:true 记录",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-AGENT-DAEMON-v1.0-UID9622",
        "备注": "P2 落地项。支持 macOS launchd / Linux systemd-user 安装。",
    },
    {
        "指令名称": "P2 · Agent 编排器守护进程状态/停止",
        "阶段": "P2",
        "模式": "验证",
        "开关类型": "分布式开关",
        "功能描述": "查看或停止 Agent 编排器守护进程。",
        "执行命令": "lh agent-daemon status  # 或 stop / restart / install",
        "目标文件": "08_BIN/lh_agent_daemon.py",
        "验证方式": "status 输出 PID 与最近日志；stop 后 PID 文件清理",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-AGENT-DAEMON-v1.0-UID9622",
        "备注": "分布式开关：管理 daemon 生命周期。",
    },
    {
        "指令名称": "P2 · 初始化多 Agent 工作流模板",
        "阶段": "P2",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "生成 code-review / publish / deploy 三个人格链式协作工作流模板到 ~/.longhun/workflows/。",
        "执行命令": "lh workflow-chain init",
        "目标文件": "08_BIN/lh_workflow_engine.py, ~/.longhun/workflows/*.json",
        "验证方式": "lh workflow-chain list 显示 3 个内置工作流",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-WORKFLOW-ENGINE-v1.0-UID9622",
        "备注": "P2 落地项。每个工作流含 DNA、人格分工、on_fail 中止策略。",
    },
    {
        "指令名称": "P2 · 运行多 Agent 工作流",
        "阶段": "P2",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "按顺序执行工作流步骤，每步自动匹配人格、调用治理流水线、发布事件。",
        "执行命令": "lh workflow-chain run code-review -m '本次提交说明' --dry-run",
        "目标文件": "08_BIN/lh_workflow_engine.py, 08_BIN/lh_governed_exec.py, 08_BIN/lh_event_bus.py",
        "验证方式": "dry-run 打印每步命令；正式运行生成 ~/.longhun/workflow_runs/*.json 审计日志",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-WORKFLOW-ENGINE-v1.0-UID9622",
        "备注": "分布式开关：生产环境先去 --dry-run 确认再执行。",
    },
    {
        "指令名称": "P2 · 查看工作流运行历史",
        "阶段": "P2",
        "模式": "验证",
        "开关类型": "总开关",
        "功能描述": "一键列出最近工作流运行记录与状态。",
        "执行命令": "lh workflow-chain history --limit 10",
        "目标文件": "08_BIN/lh_workflow_engine.py",
        "验证方式": "输出 run_id / status / started_at / 步骤数",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-WORKFLOW-ENGINE-v1.0-UID9622",
        "备注": "总开关：一键体检。排查工作流是否按预期执行。",
    },
    {
        "指令名称": "P3 · 初始化工作流触发器",
        "阶段": "P3",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "生成 interval / file / event 三类内置触发器到 ~/.longhun/triggers/triggers.json。",
        "执行命令": "lh trigger init",
        "目标文件": "08_BIN/lh_trigger_engine.py, ~/.longhun/triggers/triggers.json",
        "验证方式": "lh trigger list 显示 3 个触发器：auto-discovery / memory-guard / workflow-chain-event",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-TRIGGER-ENGINE-v1.0-UID9622",
        "备注": "P3 落地项。触发器是事件链自动化的起点。",
    },
    {
        "指令名称": "P3 · 启动触发器守护进程",
        "阶段": "P3",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "常驻轮询 interval 与 file 触发器，并消费 event 触发器事件自动触发工作流/命令。",
        "执行命令": "lh trigger daemon --interval 10",
        "目标文件": "08_BIN/lh_trigger_engine.py, 08_BIN/lh_workflow_engine.py, 08_BIN/lh_event_bus.py",
        "验证方式": "发布 workflow.code_review.completed 事件后，~/.longhun/workflow_runs/ 出现 publish_* 新记录",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-TRIGGER-ENGINE-v1.0-UID9622",
        "备注": "P3 落地项。daemon 会消费匹配的事件并标记为 delivered。",
    },
    {
        "指令名称": "P3 · 停止/查看触发器守护进程",
        "阶段": "P3",
        "模式": "验证",
        "开关类型": "分布式开关",
        "功能描述": "管理触发器守护进程生命周期。",
        "执行命令": "lh trigger status  # 或 stop",
        "目标文件": "08_BIN/lh_trigger_engine.py",
        "验证方式": "status 输出 PID；stop 后状态变为未运行",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-TRIGGER-ENGINE-v1.0-UID9622",
        "备注": "分布式开关：进程管理。",
    },
    {
        "指令名称": "P3 · 手动执行触发器",
        "阶段": "P3",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "单次执行指定触发器，常用于测试事件链。",
        "执行命令": "lh trigger run workflow-chain-event  # 或 auto-discovery / memory-guard",
        "目标文件": "08_BIN/lh_trigger_engine.py",
        "验证方式": "workflow-chain-event 在有 pending 的 workflow.code_review.completed 事件时触发 publish 工作流",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-TRIGGER-ENGINE-v1.0-UID9622",
        "备注": "分布式开关：测试事件链时先用 --dry-run。",
    },
    {
        "指令名称": "P3 · 跨技能事件链总演练",
        "阶段": "P3",
        "模式": "执行",
        "开关类型": "总开关",
        "功能描述": "一键验证 code-review → publish 跨工作流事件链：发布事件 → 触发器消费 → publish 工作流执行。",
        "执行命令": "lh event publish --topic workflow.code_review.completed --source drill --type workflow_completed --payload '{\"message\":\"跨链演练\"}' && sleep 2 && lh trigger run workflow-chain-event && lh workflow-chain history --limit 3",
        "目标文件": "08_BIN/lh_event_bus.py, 08_BIN/lh_trigger_engine.py, 08_BIN/lh_workflow_engine.py",
        "验证方式": "workflow_runs 目录新增 publish_* 记录，事件状态变为 delivered",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-TRIGGER-ENGINE-v1.0-UID9622",
        "备注": "总开关：一键体检。验证事件链端到端是否通畅。",
    },
    {
        "指令名称": "P4 · 启动龍魂系统仪表盘",
        "阶段": "P4",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "启动 Web 可视化仪表盘，展示事件总线、技能生态、工作流运行、触发器状态、守护进程状态。",
        "执行命令": "lh dashboard --port 9600",
        "目标文件": "08_BIN/lh_dashboard_web.py, web/static/css/longhun-base.css",
        "验证方式": "打开 http://127.0.0.1:9600 能看到 6 个卡片；/api/health 返回 ok",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-DASHBOARD-WEB-v1.0-UID9622",
        "备注": "P4 落地项。前端每 10 秒自动刷新，支持暗金主题。",
    },
    {
        "指令名称": "P4 · 仪表盘 API 健康检查",
        "阶段": "P4",
        "模式": "验证",
        "开关类型": "总开关",
        "功能描述": "一键检查仪表盘各数据源 API 是否可用。",
        "执行命令": "for p in 9600 9602 9603; do ok=1; for e in health event-stats skill-stats; do curl -s -m 3 \"http://127.0.0.1:$p/api/$e\" | grep -q '{' || ok=0; done; if [ $ok -eq 1 ]; then echo \"✅ 仪表盘 :$p 三端点(health/event-stats/skill-stats)全通\"; exit 0; fi; done; echo '❌ 仪表盘端口(9600/9602/9603)均不可达'; exit 1",
        "目标文件": "08_BIN/lh_dashboard_web.py",
        "验证方式": "health/event-stats/skill-stats 三端点任一存活端口均返回 JSON",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-DASHBOARD-WEB-v1.0-UID9622",
        "备注": "总开关：一键体检。2026-08-13 修复端口漂移(实际9602/9603)，容错探测三端口任一全通即过。",
    },
    {
        "指令名称": "P5 · 部署仪表盘到鲲鹏",
        "阶段": "P5",
        "模式": "执行",
        "开关类型": "手动",
        "功能描述": "一键将本地仪表盘代码 + 运行数据（事件/工作流/触发器）同步到鲲鹏服务器，安装 systemd 服务并配置 nginx /system-dashboard/ 反代。",
        "执行命令": "lh dashboard-deploy",
        "目标文件": "08_BIN/deploy_dashboard_kunpeng.py, 08_BIN/lh_dashboard_web.py",
        "验证方式": "部署完成后访问 http://119.13.90.27:8080/system-dashboard/api/health 返回 ok",
        "状态": "已落地",
        "适用环境": ["本地", "鲲鹏"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-DASHBOARD-DEPLOY-KUNPENG-v1.0-UID9622",
        "备注": "P5 落地项。路径用 /system-dashboard/ 避免与旧 /dashboard/ 静态入口冲突。依赖 ~/.ssh/longhun_kunpeng_ed25519 密钥。",
    },
    {
        "指令名称": "P5 · 同步本地数据到鲲鹏仪表盘",
        "阶段": "P5",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "仅同步 ~/.longhun/ 下的事件总线、工作流运行、触发器日志到鲲鹏，不重新部署代码。",
        "执行命令": "python3 08_BIN/deploy_dashboard_kunpeng.py --sync-only",
        "目标文件": "08_BIN/deploy_dashboard_kunpeng.py",
        "验证方式": "鲲鹏仪表盘展示的数据与本地一致",
        "状态": "已落地",
        "适用环境": ["本地", "鲲鹏"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-DASHBOARD-DEPLOY-KUNPENG-v1.0-UID9622",
        "备注": "P5 落地项。目前复用 deploy_dashboard_kunpeng.py 的 sync_data 逻辑。",
    },
    {
        "指令名称": "P5 · 访问外网仪表盘",
        "阶段": "P5",
        "模式": "手动",
        "开关类型": "手动",
        "功能描述": "打开浏览器访问鲲鹏外网仪表盘。",
        "执行命令": "open http://119.13.90.27:8080/system-dashboard/  # macOS; Linux 用 xdg-open",
        "目标文件": "—",
        "验证方式": "页面加载出 6 大监控卡片",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-DASHBOARD-DEPLOY-KUNPENG-v1.0-UID9622",
        "备注": "手动项。部署成功后访问。",
    },
    {
        "指令名称": "P5 · 仪表盘鲲鹏服务状态",
        "阶段": "P5",
        "模式": "验证",
        "开关类型": "分布式开关",
        "功能描述": "检查鲲鹏上 longhun-dashboard 服务与 nginx 状态。",
        "执行命令": "ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27 'systemctl status longhun-dashboard --no-pager && nginx -t'",
        "目标文件": "—",
        "验证方式": "服务 active，nginx test successful",
        "状态": "已落地",
        "适用环境": ["鲲鹏"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-DASHBOARD-DEPLOY-KUNPENG-v1.0-UID9622",
        "备注": "分布式开关：服务巡检。",
    },
    {
        "指令名称": "P5 · 三才DNA无损压缩与指纹溯源 v2.0（并行优化）",
        "阶段": "P5",
        "模式": "执行",
        "开关类型": "分布式开关",
        "功能描述": "双模式：①无损压缩 .lhdc（zlib + 三才指纹 + DNA链）；②内容指纹/三色审计/签章链溯源。已启用分块并行三才特征提取，自动调块大小与 CPU 核心数。",
        "执行命令": "lh sancai-compress -c <input> -o <output.lhdc> -j 0 --sign",
        "目标文件": "08_BIN/lh_sancai_dna_compress.py, 13_TESTS/test_sancai_dna_compress.py",
        "验证方式": "lh sancai-compress -v output.lhdc --verify-sig；解压后 diff 原始文件一致",
        "状态": "已落地",
        "适用环境": ["本地"],
        "DNA": "#龍芯⚡️丙午·甲申·辛丑·坤卦-SANCAI-DNA-COMPRESS-v2.0-PARALLEL-UID9622",
        "备注": "P5 落地项。并行优化实测：log 75.96x 压缩率从 0.53s→0.10s（5.46x 加速），JSON 5.00x 从 4.70s→0.95s（4.97x），RULES.md 3.50x 从 7.47s→1.82s（4.10x）。21/21 单元测试通过。",
    },
]


# ═══════════════════════════════════════════════════════
# Notion API 客户端
# ═══════════════════════════════════════════════════════
class NotionClient:
    def __init__(self, token: str):
        self.token = token
        self.base = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_API_VERSION,
            "Content-Type": "application/json",
        }
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE", "PATCH"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session = requests.Session()
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def request(self, method: str, path: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base}{path}"
        kwargs = {"headers": self.headers, "timeout": 30}
        if payload is not None:
            kwargs["json"] = payload
        resp = self.session.request(method, url, **kwargs)
        try:
            resp.raise_for_status()
        except Exception as e:
            print(f"🔴 API 错误: {e}", file=sys.stderr)
            print(resp.text, file=sys.stderr)
            raise
        return resp.json()

    def post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.request("POST", path, payload)

    def patch(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.request("PATCH", path, payload)

    def query_database(self, database_id: str, filter_payload: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        results = []
        cursor = None
        while True:
            payload: Dict[str, Any] = {"page_size": 100}
            if cursor:
                payload["start_cursor"] = cursor
            if filter_payload:
                payload["filter"] = filter_payload
            data = self.post(f"/databases/{database_id}/query", payload)
            results.extend(data.get("results", []))
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
        return results

    def find_page_by_title(self, database_id: str, title: str) -> Optional[Dict[str, Any]]:
        results = self.query_database(
            database_id,
            filter_payload={
                "property": "指令名称",
                "title": {"equals": title},
            },
        )
        return results[0] if results else None


# ═══════════════════════════════════════════════════════
# 配置读写
# ═══════════════════════════════════════════════════════
def load_config() -> Dict[str, str]:
    if not CONFIG_PATH.exists():
        print(f"❌ 找不到 Notion 配置: {CONFIG_PATH}", file=sys.stderr)
        sys.exit(2)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_registry_config() -> Dict[str, Any]:
    if not REGISTRY_CONFIG_PATH.exists():
        return {}
    with open(REGISTRY_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_registry_config(data: Dict[str, Any]):
    REGISTRY_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════
# 数据库与页面属性构造
# ═══════════════════════════════════════════════════════
DB_SCHEMA: Dict[str, Any] = {
    "title": [{"type": "text", "text": {"content": "🐉 龍魂指令注册表"}}],
    "description": [{"type": "text", "text": {"content": "ASI 精修融合系统 Phase A/B/C/D 及关键修复指令清单 · 总开关/分布式开关/手动"}}],
    "properties": {
        "指令名称": {"title": {}},
        "阶段": {
            "select": {
                "options": [
                    {"name": "P0", "color": "red"},
                    {"name": "Phase A", "color": "blue"},
                    {"name": "Phase B", "color": "green"},
                    {"name": "Phase C", "color": "yellow"},
                    {"name": "Phase D", "color": "purple"},
                    {"name": "通用", "color": "gray"},
                    {"name": "修复", "color": "red"},
                    {"name": "启动", "color": "orange"},
                ]
            }
        },
        "模式": {
            "select": {
                "options": [
                    {"name": "验证", "color": "green"},
                    {"name": "执行", "color": "blue"},
                    {"name": "手动", "color": "gray"},
                ]
            }
        },
        "开关类型": {
            "select": {
                "options": [
                    {"name": "总开关", "color": "red"},
                    {"name": "分布式开关", "color": "blue"},
                    {"name": "手动", "color": "gray"},
                ]
            }
        },
        "功能描述": {"rich_text": {}},
        "执行命令": {"rich_text": {}},
        "目标文件": {"rich_text": {}},
        "验证方式": {"rich_text": {}},
        "状态": {
            "select": {
                "options": [
                    {"name": "已落地", "color": "green"},
                    {"name": "周期性", "color": "yellow"},
                    {"name": "待修复", "color": "red"},
                    {"name": "已废弃", "color": "gray"},
                ]
            }
        },
        "适用环境": {
            "multi_select": {
                "options": [
                    {"name": "本地", "color": "blue"},
                    {"name": "鲲鹏", "color": "orange"},
                ]
            }
        },
        "DNA": {"rich_text": {}},
        "最后更新": {"date": {}},
        "备注": {"rich_text": {}},
    },
    "is_inline": False,
}


def row_to_properties(row: Dict[str, Any]) -> Dict[str, Any]:
    today = datetime.now().strftime("%Y-%m-%d")
    return {
        "指令名称": {"title": [{"text": {"content": row["指令名称"]}}]},
        "阶段": {"select": {"name": row["阶段"]}},
        "模式": {"select": {"name": row["模式"]}},
        "开关类型": {"select": {"name": row["开关类型"]}},
        "功能描述": {"rich_text": [{"text": {"content": row["功能描述"]}}]},
        "执行命令": {"rich_text": [{"text": {"content": row["执行命令"]}}]},
        "目标文件": {"rich_text": [{"text": {"content": row["目标文件"]}}]},
        "验证方式": {"rich_text": [{"text": {"content": row["验证方式"]}}]},
        "状态": {"select": {"name": row["状态"]}},
        "适用环境": {"multi_select": [{"name": env} for env in row["适用环境"]]},
        "DNA": {"rich_text": [{"text": {"content": row["DNA"]}}]},
        "最后更新": {"date": {"start": today}},
        "备注": {"rich_text": [{"text": {"content": row.get("备注", "")}}]},
    }


# ═══════════════════════════════════════════════════════
# 子命令
# ═══════════════════════════════════════════════════════
def cmd_create_db(args: argparse.Namespace):
    config = load_config()
    client = NotionClient(config["notion_token"])

    parent_page_id = args.parent_page_id
    if not parent_page_id:
        print("❌ 必须提供 --parent-page-id（Notion 父页面 ID）", file=sys.stderr)
        sys.exit(2)

    payload = dict(DB_SCHEMA)
    payload["parent"] = {"page_id": parent_page_id}

    print(f"🌐 正在 Notion 创建数据库，父页面: {parent_page_id}...")
    result = client.post("/databases", payload)
    database_id = result.get("id")

    registry_cfg = load_registry_config()
    registry_cfg["database_id"] = database_id
    registry_cfg["database_url"] = result.get("url", "")
    registry_cfg["created_time"] = datetime.now().isoformat()
    registry_cfg["dna"] = generate_dna("NOTION-CMD-REGISTRY-DB", "UID9622")
    registry_cfg["confirm"] = CONFIRM_MARK
    save_registry_config(registry_cfg)

    print(f"✅ 数据库创建成功")
    print(f"   ID: {database_id}")
    print(f"   URL: {result.get('url', '')}")
    print(f"💾 配置已写入: {REGISTRY_CONFIG_PATH}")


def _ensure_db_schema(client: NotionClient, database_id: str):
    """给已存在的数据库补全新增字段（模式 / 开关类型）。"""
    schema_patch = {
        "properties": {
            "模式": DB_SCHEMA["properties"]["模式"],
            "开关类型": DB_SCHEMA["properties"]["开关类型"],
        }
    }
    try:
        client.patch(f"/databases/{database_id}", schema_patch)
        print("🔧 数据库字段已补齐（模式 / 开关类型）")
    except Exception as e:
        print(f"⚠️ 补齐字段失败（可能已存在）: {e}", file=sys.stderr)


def cmd_push(args: argparse.Namespace):
    config = load_config()
    registry_cfg = load_registry_config()
    database_id = registry_cfg.get("database_id")
    if not database_id:
        print("❌ 尚未创建数据库，请先运行 create-db", file=sys.stderr)
        sys.exit(2)

    client = NotionClient(config["notion_token"])
    _ensure_db_schema(client, database_id)

    print(f"🌐 开始同步 {len(COMMAND_ROWS)} 条指令到 Notion...")
    created = 0
    updated = 0
    skipped = 0
    errors = 0

    for row in COMMAND_ROWS:
        title = row["指令名称"]
        props = row_to_properties(row)
        existing = client.find_page_by_title(database_id, title)

        if existing:
            if args.force:
                try:
                    client.patch(f"/pages/{existing['id']}", {"properties": props})
                    print(f"🔄 强制更新: {title}")
                    updated += 1
                except Exception as e:
                    print(f"❌ 更新失败 {title}: {e}", file=sys.stderr)
                    errors += 1
            else:
                print(f"⏭️ 已存在，跳过: {title}")
                skipped += 1
            continue

        if args.dry_run:
            print(f"🧪 [dry-run] 将新增: {title}")
            created += 1
            continue

        try:
            client.post("/pages", {"parent": {"database_id": database_id}, "properties": props})
            print(f"✅ 已新增: {title}")
            created += 1
            time.sleep(0.35)
        except Exception as e:
            print(f"❌ 新增失败 {title}: {e}", file=sys.stderr)
            errors += 1

    print(f"\n📊 同步完成")
    print(f"   新增: {created}")
    print(f"   更新: {updated}")
    print(f"   跳过: {skipped}")
    print(f"   失败: {errors}")


def _filter_rows(category: Optional[str] = None, mode: Optional[str] = None,
                 switch_type: Optional[str] = None) -> List[Dict[str, Any]]:
    rows = list(COMMAND_ROWS)
    if category:
        cat = f"Phase {category.upper()}" if len(category) == 1 else category
        rows = [r for r in rows if r["阶段"] == cat]
    if mode:
        rows = [r for r in rows if r["模式"] == mode]
    if switch_type:
        rows = [r for r in rows if r["开关类型"] == switch_type]
    return rows


def _run_command(cmd: str, dry_run: bool) -> Dict[str, Any]:
    result = {"command": cmd, "dry_run": dry_run, "returncode": None, "stdout": "", "stderr": ""}
    print(f"  $ {cmd}")
    if dry_run:
        result["returncode"] = 0
        result["stdout"] = "[dry-run] 未执行"
        return result
    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=PROJECT_ROOT,
        )
        result["returncode"] = proc.returncode
        result["stdout"] = proc.stdout.strip()
        result["stderr"] = proc.stderr.strip()
        if proc.returncode == 0:
            print(f"  ✅ 成功")
        else:
            print(f"  ❌ 退出码 {proc.returncode}")
        if proc.stdout.strip():
            for line in proc.stdout.strip().splitlines()[:10]:
                print(f"     {line}")
        if proc.stderr.strip():
            for line in proc.stderr.strip().splitlines()[:5]:
                print(f"     ⚠️ {line}")
    except subprocess.TimeoutExpired:
        result["returncode"] = -1
        result["stderr"] = "超时（120秒）"
        print(f"  ⏱️ 超时")
    except Exception as e:
        result["returncode"] = -1
        result["stderr"] = str(e)
        print(f"  ❌ 异常: {e}")
    return result


def _confirm(rows: List[Dict[str, Any]]) -> bool:
    print(f"\n⚠️  即将执行 {len(rows)} 条命令（可能改写数据或调用远程服务器）。")
    ans = input("   确认执行? [y/N]: ").strip().lower()
    return ans in ("y", "yes")


def cmd_run(args: argparse.Namespace):
    registry_cfg = load_registry_config()
    database_id = registry_cfg.get("database_id")

    # run check --all: 总开关 · 体检（只读验证）
    if args.run_command == "check" and args.all:
        rows = _filter_rows(mode="验证")
        print(f"🐉 总开关 · 一键体检（{len(rows)} 条验证命令）\n")
        return _execute_rows(rows, args.dry_run, require_confirm=False)

    # run check --category X: 按类别验证
    if args.run_command == "check" and args.category:
        rows = _filter_rows(category=args.category, mode="验证")
        print(f"🐉 分布式开关 · {args.category} 体检（{len(rows)} 条验证命令）\n")
        return _execute_rows(rows, args.dry_run, require_confirm=False)

    # run exec --all: 总开关 · 执行（较危险）
    if args.run_command == "exec" and args.all:
        rows = _filter_rows(mode="执行")
        print(f"🐉 总开关 · 一键执行（{len(rows)} 条执行命令）\n")
        return _execute_rows(rows, args.dry_run, require_confirm=not args.yes)

    # run exec --category X: 分布式开关 · 执行
    if args.run_command == "exec" and args.category:
        rows = _filter_rows(category=args.category, mode="执行")
        print(f"🐉 分布式开关 · {args.category} 执行（{len(rows)} 条执行命令）\n")
        return _execute_rows(rows, args.dry_run, require_confirm=not args.yes)

    # run manual: 列出手动项
    if args.run_command == "manual":
        rows = _filter_rows(mode="手动")
        print("📋 手动项清单（无法一键自动执行）：\n")
        for r in rows:
            print(f"  · [{r['阶段']}] {r['指令名称']}")
            print(f"    命令: {r['执行命令']}")
            print(f"    备注: {r['备注']}\n")
        return

    print("❌ 未知 run 子命令组合，使用 --help 查看用法", file=sys.stderr)


def _execute_rows(rows: List[Dict[str, Any]], dry_run: bool, require_confirm: bool) -> None:
    if not rows:
        print("⚠️ 没有匹配的指令。")
        return

    if require_confirm and not dry_run:
        if not _confirm(rows):
            print("🛑 已取消")
            return

    results = []
    passed = 0
    failed = 0
    for i, row in enumerate(rows, 1):
        print(f"\n[{i}/{len(rows)}] {row['指令名称']} | {row['阶段']} | {row['模式']}")
        res = _run_command(row["执行命令"], dry_run)
        results.append({"row": row, "result": res})
        if res["returncode"] == 0:
            passed += 1
        else:
            failed += 1
        if not dry_run:
            time.sleep(0.5)

    print(f"\n📊 执行汇总")
    print(f"   总计: {len(rows)}")
    print(f"   通过: {passed}")
    print(f"   失败: {failed}")

    # 生成本地报告
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / f"notion_command_registry_run_{datetime.now():%Y%m%d_%H%M%S}.json"
    report = {
        "dna": generate_dna("NOTION-CMD-REGISTRY-RUN", "UID9622"),
        "confirm": CONFIRM_MARK,
        "timestamp": datetime.now().isoformat(),
        "dry_run": dry_run,
        "results": [
            {
                "name": r["row"]["指令名称"],
                "phase": r["row"]["阶段"],
                "mode": r["row"]["模式"],
                "command": r["result"]["command"],
                "returncode": r["result"]["returncode"],
                "stdout": r["result"]["stdout"],
                "stderr": r["result"]["stderr"],
            }
            for r in results
        ],
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"💾 执行报告: {report_path}")


def cmd_export(args: argparse.Namespace):
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "dna": generate_dna("NOTION-CMD-REGISTRY-EXPORT", "UID9622"),
        "confirm": CONFIRM_MARK,
        "generated_at": datetime.now().isoformat(),
        "rows": COMMAND_ROWS,
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 已导出 {len(COMMAND_ROWS)} 条指令到: {output_path}")


def cmd_verify(args: argparse.Namespace):
    config = load_config()
    registry_cfg = load_registry_config()
    database_id = registry_cfg.get("database_id")
    if not database_id:
        print("❌ 尚未创建数据库", file=sys.stderr)
        sys.exit(2)

    client = NotionClient(config["notion_token"])
    existing = client.query_database(database_id)
    titles = []
    for page in existing:
        props = page.get("properties", {})
        title_prop = props.get("指令名称", {}).get("title", [])
        title = "".join(t.get("plain_text", "") for t in title_prop)
        if title:
            titles.append(title)

    expected = {r["指令名称"] for r in COMMAND_ROWS}
    actual = set(titles)
    missing = expected - actual
    extra = actual - expected

    print(f"📊 Notion 指令注册表校验")
    print(f"   本地定义: {len(expected)}")
    print(f"   Notion 实际: {len(actual)}")
    if missing:
        print(f"   🔴 缺失 {len(missing)} 条:")
        for t in missing:
            print(f"      - {t}")
    else:
        print("   🟢 无缺失")
    if extra:
        print(f"   🟡 多余 {len(extra)} 条:")
        for t in extra:
            print(f"      - {t}")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / f"notion_command_registry_verify_{datetime.now():%Y%m%d_%H%M%S}.json"
    report = {
        "dna": generate_dna("NOTION-CMD-REGISTRY-VERIFY", "UID9622"),
        "confirm": CONFIRM_MARK,
        "timestamp": datetime.now().isoformat(),
        "database_id": database_id,
        "expected_count": len(expected),
        "actual_count": len(actual),
        "missing": sorted(missing),
        "extra": sorted(extra),
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"💾 校验报告: {report_path}")


# ═══════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · Notion 指令注册表同步工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 建库（一次）
  python3 08_BIN/lh_notion_command_registry.py create-db --parent-page-id <uuid>

  # 同步表格到 Notion
  python3 08_BIN/lh_notion_command_registry.py push
  python3 08_BIN/lh_notion_command_registry.py push --force   # 强制更新所有行

  # 总开关 · 一键体检（只读·安全）
  python3 08_BIN/lh_notion_command_registry.py run check --all

  # 分布式开关 · 执行某一阶段（默认会二次确认）
  python3 08_BIN/lh_notion_command_registry.py run exec --category A --dry-run
  python3 08_BIN/lh_notion_command_registry.py run exec --category A --yes

  # 列出手动项
  python3 08_BIN/lh_notion_command_registry.py run manual

  # 校验 / 导出
  python3 08_BIN/lh_notion_command_registry.py verify
  python3 08_BIN/lh_notion_command_registry.py export --output commands.json
        """,
    )
    sub = parser.add_subparsers(dest="command", help="子命令")

    p_create = sub.add_parser("create-db", help="在 Notion 创建指令注册表数据库")
    p_create.add_argument("--parent-page-id", required=True, help="父页面 ID（数据库挂载到该页面下）")

    p_push = sub.add_parser("push", help="把本地指令清单同步到 Notion 数据库（已存在则跳过，--force 更新）")
    p_push.add_argument("--dry-run", action="store_true", help="只打印，不真正推送")
    p_push.add_argument("--force", action="store_true", help="强制更新已存在的行")

    p_run = sub.add_parser("run", help="执行注册表里的命令（总开关 / 分布式开关）")
    run_sub = p_run.add_subparsers(dest="run_command", help="run 子命令")

    p_check = run_sub.add_parser("check", help="只读验证（安全）")
    check_group = p_check.add_mutually_exclusive_group(required=True)
    check_group.add_argument("--all", action="store_true", help="总开关：执行所有验证命令")
    check_group.add_argument("--category", type=str, help="分布式开关：按阶段验证，如 A/B/C/D/通用/修复")
    p_check.add_argument("--dry-run", action="store_true", help="只打印命令，不执行")

    p_exec = run_sub.add_parser("exec", help="实际执行（可能改写数据）")
    exec_group = p_exec.add_mutually_exclusive_group(required=True)
    exec_group.add_argument("--all", action="store_true", help="总开关：执行所有执行类命令")
    exec_group.add_argument("--category", type=str, help="分布式开关：按阶段执行，如 A/B/C/D/通用/修复")
    p_exec.add_argument("--dry-run", action="store_true", help="只打印命令，不执行")
    p_exec.add_argument("--yes", action="store_true", help="跳过二次确认（自动化场景用）")

    run_sub.add_parser("manual", help="列出手动项清单")

    p_export = sub.add_parser("export", help="导出本地指令清单为 JSON")
    p_export.add_argument("--output", type=str, default="commands.json", help="输出文件路径")

    sub.add_parser("verify", help="校验 Notion 数据库与本地清单是否一致")

    args = parser.parse_args()

    if args.command == "create-db":
        cmd_create_db(args)
    elif args.command == "push":
        cmd_push(args)
    elif args.command == "run":
        cmd_run(args)
    elif args.command == "export":
        cmd_export(args)
    elif args.command == "verify":
        cmd_verify(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
