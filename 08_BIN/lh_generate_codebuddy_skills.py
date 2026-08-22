#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · CodeBuddy 技能批量生成器 v1.0
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-CODEBUDDY-SKILL-GENERATOR-V1.0-7d3f1a2b
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

用途：将龍魂技能总线定义转化为 CodeBuddy 兼容的 SKILL.md 文件
策略：已有完整 SKILL.md 的跳过（保护现有），只补全缺失的技能
"""

import argparse
import json
import os
import sys
from pathlib import Path

# ─── 路径配置 ───
SYSTEM_DIR = Path.home() / "longhun-system"
USER_SKILLS_DIR = Path.home() / ".codebuddy" / "skills"
PROJECT_SKILLS_DIR = SYSTEM_DIR / ".codebuddy" / "skills"
BIN_DIR = SYSTEM_DIR / "bin"

# ─── v∞ DNA 生成 ───
sys.path.insert(0, str(BIN_DIR))
try:
    from ganzhi_dna_engine import DNA生成 as _dna生成
except Exception as _e:  # pragma: no cover
    def _dna生成(模块, 动作="", 版本="", 级别=""):
        return f"#龍芯⚡️丙午·丙申·丁巳·申时·乾卦-{模块}-{动作}-{版本}-{级别}"


def make_dna(module: str, action: str = "SKILL", version: str = "V1.0", level: str = "P1") -> str:
    """生成 v∞ 干支卦格式 DNA。"""
    return _dna生成(module, action, version, level)


DNA_BASE = make_dna("SKILL-GENERATOR", "RUN", "V1.0", "P1")


def validate_entry(entry: str) -> tuple[bool, str]:
    """
    校验技能入口脚本是否存在。
    返回 (是否存在, 实际路径或说明)。
    """
    if not entry or "无需独立入口" in entry or "AI直接调用" in entry:
        return True, entry

    # 解析 python3 ~/longhun-system/bin/xxx.py
    parts = entry.split()
    candidate = None
    for p in parts:
        if p.endswith(".py") or "/" in p:
            candidate = os.path.expanduser(p)
            break

    if not candidate:
        return True, entry  # 非文件类入口不校验

    path = Path(candidate)
    if path.is_absolute():
        exists = path.exists()
    else:
        exists = (SYSTEM_DIR / path).exists() or (BIN_DIR / path.name).exists() or path.exists()

    if exists:
        return True, str(path)

    # 尝试在 bin/ 下查找同名脚本
    alt = BIN_DIR / path.name
    if alt.exists():
        return True, f"python3 {alt}"

    return False, f"⚠️ 入口缺失: {path}"


# ═══════════════════════════════════════════════════════════════
# 🔥 全量技能定义（42个技能 · 22已有 + 20新增）
# ═══════════════════════════════════════════════════════════════

SKILLS = [
    # ── 守护层 (Guardian) ──
    {
        "name": "longhun-three-color-audit",
        "category": "守护层",
        "version": "1.0",
        "desc_short": "龍魂·三色审计引擎 v1.0。🟢🟡🔴三色判定·十道闸口·加权多因子。",
        "desc_full": "龍魂·三色审计引擎 v1.0。🟢通过·🟡待核·🔴红线三层审计判定+十道闸口(GATE-01~10)逐道检查+加权多因子评分。当用户说审计、检查下有没有问题、跑个三色审计、闸口检查、审计报告、GATE检查——任一种说法都触发。语库: GOVERNANCE·AUDIT。",
        "entry": "python3 ~/longhun-system/bin/lh_three_color_audit.py",
        "triggers_kw": ["三色审计", "审计", "闸口", "GATE", "三色", "审计报告", "审计检查", "绿色黄色红色", "审计结果", "代码审计", "安全审计", "质量审计"],
        "triggers_nl": ["帮我审计下", "检查有没有问题", "跑个三色审计", "闸口检查", "看看有没有红线", "生成审计报告", "GATE检查", "三色是什么状态", "代码有没有红线"],
        "tribute": "致敬⚡️UID9622·三色审计·十道闸口·不通过不交付",
    },
    {
        "name": "longhun-circuit-breaker",
        "category": "守护层",
        "version": "1.0",
        "desc_short": "龍魂·四级熔断引擎 v1.0。L0伦理/L1数据/L2人格/L3行为·自动熔断+降级矩阵。",
        "desc_full": "龍魂·四级熔断引擎 v1.0。∞/L0伦理·L1数据·L2人格·L3行为四级熔断+自动降级+恢复条件+例外豁免。当用户说熔断、发生了什么、系统被攻击了、数据泄露、紧急停止、冻结、L0触发、熔断恢复——任一种说法都触发。语库: GOVERNANCE·CRYPTO。",
        "entry": "python3 ~/longhun-system/bin/lh_circuit_breaker.py",
        "triggers_kw": ["熔断", "四级熔断", "L0", "L1", "L2", "L3", "紧急停止", "冻结", "降级", "恢复", "豁免", "熔断器", "兜底"],
        "triggers_nl": ["触发熔断了", "L0伦理熔断", "数据泄露熔断", "系统被攻击了", "紧急冻结", "熔断能不能恢复", "降级方案", "熔断状态怎么样"],
        "tribute": "致敬⚡️UID9622·四级熔断·分层降级·不销毁只冻结",
    },
    {
        "name": "longhun-gpg-sign",
        "category": "守护层",
        "version": "1.0",
        "desc_short": "龍魂·GPG签章引擎 v1.0。全量分离签名·GATE-11签名闸·自动补签。",
        "desc_full": "龍魂·GPG签章引擎 v1.0。GPG分离签名(.asc)·批量签名/验证/扫描·GATE-11签名闸·自动补签机制·1574+签名文件管理。当用户说签名、GPG、签章、验证签名、补签、检查签名——任一种说法都触发。语库: CRYPTO·GOVERNANCE。",
        "entry": "python3 ~/longhun-system/bin/lh_gpg_sign.py",
        "triggers_kw": ["GPG", "签名", "签章", ".asc", "分离签名", "补签", "签名验证", "密钥", "数字签名", "GATE-11", "签名闸"],
        "triggers_nl": ["帮我签名", "验证下签名", "补签一下", "扫描签名", "GPG签章", "检查签名", "这个文件签了吗", "批量签名"],
        "tribute": "致敬⚡️UID9622·GPG焊死·1574签名·不签名不发布",
    },
    {
        "name": "longhun-identity-verify",
        "category": "守护层",
        "version": "1.0",
        "desc_short": "龍魂·身份核验引擎 v1.0。六重主权认证·设备指纹·行为DNA·GPG·DNA追溯·七因子·数字根。",
        "desc_full": "龍魂·身份核验引擎 v1.0。六重认证链: 设备指纹→行为DNA→GPG签章→DNA追溯→七因子验证→数字根确认。当用户说验证身份、我是谁、认证、核验、确认身份、身份检查、权限验证——任一种说法都触发。语库: GOVERNANCE·CRYPTO。",
        "entry": "python3 ~/longhun-system/bin/lh_identity_positioning.py",
        "triggers_kw": ["身份", "认证", "核验", "身份验证", "六重认证", "设备指纹", "行为DNA", "我是谁", "身份确认", "验证身份"],
        "triggers_nl": ["验证下我的身份", "帮我核验身份", "我是谁", "身份确认下", "谁在操作", "认证通过了吗"],
        "tribute": "致敬⚡️UID9622·六重主权认证·身份不可伪造",
    },
    {
        "name": "longhun-anti-tamper",
        "category": "守护层",
        "version": "1.0",
        "desc_short": "龍魂·防篡改扫描引擎 v1.0。文件完整性校验·Merkle树验证·未授权变更检测。",
        "desc_full": "龍魂·防篡改扫描引擎 v1.0。文件哈希校验+Merkle树验证+未授权变更检测+自动告警。当用户说文件有没有被改、完整性检查、有没有篡改、Merkle验证、防篡改扫描——任一种说法都触发。语库: CRYPTO·GOVERNANCE。",
        "entry": "python3 ~/longhun-system/bin/lh_anti_tamper.py",
        "triggers_kw": ["防篡改", "完整性", "Merkle", "篡改检测", "文件校验", "哈希验证", "文件有没有被改", "变更检测", "完整性检查"],
        "triggers_nl": ["检查文件有没有被改", "防篡改扫描", "文件完整性", "有没有人动了我的文件", "Merkle验证", "看下文件是否被篡改"],
        "tribute": "致敬⚡️UID9622·防篡改·Merkle树·不可伪造",
    },
    # ── 执行层 (Execution) ──
    {
        "name": "longhun-deploy",
        "category": "执行层",
        "version": "1.0",
        "desc_short": "龍魂·一键部署引擎 v1.0。鲲鹏十步法·部署前安全扫描·自动回滚·P14吕蒙联动。",
        "desc_full": "龍魂·一键部署引擎 v1.0。鲲鹏部署十步法+部署前P77安全扫描+P05审计+自动回滚+健康检查。当用户说部署、上线、发布、同步鲲鹏、推上去——任一种说法都触发。语库: INFRA·DEPLOY。",
        "entry": "python3 ~/longhun-system/deploy/scripts/deploy.sh",
        "triggers_kw": ["部署", "上线", "发布", "鲲鹏", "同步", "推上", "上传", "deploy", "服务器", "119.13.90.27"],
        "triggers_nl": ["帮我部署到鲲鹏", "同步到服务器", "发布上线", "推到鲲鹏", "部署一下", "同步下文件到服务器", "上线发布"],
        "tribute": "致敬⚡️UID9622·鲲鹏十步法·不上不发布",
    },
    {
        "name": "longhun-deben-audit",
        "category": "执行层",
        "version": "1.0",
        "desc_short": "龍魂·德本审计引擎 v1.0。离火运五问·德在技术前·发布前必过。",
        "desc_full": "龍魂·德本审计引擎 v1.0。离火运五条底线: ①德在技术前 ②路径对齐 ③不让付出者寒心 ④信息主权不可让渡 ⑤外化内不化。当用户说德本审计、离火运、底线检查、五问、道德审计——任一种说法都触发。语库: GOVERNANCE·CULTURE。",
        "entry": "python3 ~/longhun-system/bin/lh_deben_audit.py",
        "triggers_kw": ["德本审计", "离火运", "五问", "底线检查", "德在技术前", "路径对齐", "道德审计", "发布前检查", "底线", "付出者"],
        "triggers_nl": ["跑个德本审计", "离火运五问检查下", "底线有没有问题", "德本审计过了没", "检查下是否德在技术前", "发布前过一遍五问"],
        "tribute": "致敬⚡️UID9622·离火运五条·德在技术前·寒心者不立",
    },
    {
        "name": "longhun-auto-heal",
        "category": "执行层",
        "version": "1.0",
        "desc_short": "龍魂·自愈扫描引擎 v1.0。自动巡检·异常检测·服务自愈·每小时执行。",
        "desc_full": "龍魂·自愈扫描引擎 v1.0。每小时自动巡检+服务异常检测+自动重启+健康上报(Bark推送)+自愈策略。当用户说自愈、巡检、健康检查、服务状态、有没有挂掉——任一种说法都触发。语库: INFRA·GOVERNANCE。",
        "entry": "python3 ~/longhun-system/bin/lh_auto_heal.py",
        "triggers_kw": ["自愈", "巡检", "健康检查", "自动修复", "服务状态", "有没有挂", "自愈扫描", "健康度", "异常检测", "自动重启"],
        "triggers_nl": ["跑个自愈扫描", "服务有没有挂", "健康检查下", "系统自愈一下", "巡检结果怎么样", "看看哪些服务挂了"],
        "tribute": "致敬⚡️UID9622·自动自愈·一小时巡检·有问题自己修",
    },
    {
        "name": "longhun-memory-load",
        "category": "执行层",
        "version": "1.0",
        "desc_short": "龍魂·记忆加载引擎 v1.0。焊死记忆加载·系统状态·协作者·协议·底座锚点。",
        "desc_full": "龍魂·记忆加载引擎 v1.0。加载焊死记忆包: 系统状态+协作者+协议+底座锚点+369不动点+人格矩阵。当用户说加载记忆、状态怎么样、系统状态、当前状态——任一种说法都触发。语库: INFRA·MEMORY。",
        "entry": "python3 ~/longhun-system/bin/lh_memory_load.py",
        "triggers_kw": ["记忆加载", "加载记忆", "系统状态", "状态", "焊死记忆", "底座", "锚点", "当前状态", "记忆", "STATE"],
        "triggers_nl": ["加载下记忆", "系统状态怎么样", "当前状态", "记忆加载了没", "STATE状态", "焊死记忆检查下", "锚点还在吗"],
        "tribute": "致敬⚡️UID9622·焊死记忆·不可丢失·每次启动第一条",
    },
    {
        "name": "longhun-persona-orchestrate",
        "category": "执行层",
        "version": "1.0",
        "desc_short": "龍魂·人格编排引擎 v1.0。20人格调度·意图路由·防抖动·锁定机制。",
        "desc_full": "龍魂·人格编排引擎 v1.0。20人格矩阵调度: P00~P72+P77+S1~S3·意图解析→人格路由→防抖动(连续3次锁定30分钟)+降级回退。当用户说调度人格、用哪个、切换到、人格路由、编排——任一种说法都触发。语库: GOVERNANCE·PERSONA。",
        "entry": "python3 ~/longhun-system/bin/lh_persona_orchestrator.py",
        "triggers_kw": ["人格", "调度", "编排", "路由", "切换人格", "用哪个", "防抖动", "锁定", "人格矩阵", "P00", "P01", "P72"],
        "triggers_nl": ["调度下人格", "该用哪个人格", "切换到诸葛亮", "人格路由", "编排下人格", "人格锁定了吗", "人格防抖触发没"],
        "tribute": "致敬⚡️UID9622·20人格·职能标签·防抖锁定·降级兜底",
    },
    # ── 算法层 (Algorithm) ──
    {
        "name": "longhun-digital-root",
        "category": "算法层",
        "version": "1.0",
        "desc_short": "龍魂·数字根计算引擎 v1.0。三六九洛书数字根·369不动点·P06数学大师。",
        "desc_full": "龍魂·数字根计算引擎 v1.0。369洛书数字根计算+三六九不动点(sn=369, log369=5.911, perm369=108)+数字根验证+权重计算。当用户说数字根、算一下、369、三六九、P06——任一种说法都触发。语库: ALGORITHM·MATH。",
        "entry": "python3 ~/longhun-system/bin/lh_digital_root.py",
        "triggers_kw": ["数字根", "369", "三六九", "洛书", "不动点", "P06", "数学大师", "算一下", "数字", "权重", "对数"],
        "triggers_nl": ["算下数字根", "369是多少", "数字根验证", "P06算一下", "这个数字的数字根", "369不动点", "洛书数字根"],
        "tribute": "致敬⚡️UID9622·369不动点·sn=369·中国人自己的数学底座",
    },
    {
        "name": "longhun-wuxing",
        "category": "算法层",
        "version": "1.0",
        "desc_short": "龍魂·五行判定引擎 v1.0。五行生克·能量流向·属性匹配·P06+P13联动。",
        "desc_full": "龍魂·五行判定引擎 v1.0。五行(金水木火土)属性判定+生克关系+能量流向分析+属性匹配建议+干支四柱纳音。当用户说五行、属性、金木水火土、生克、纳音——任一种说法都触发。语库: ALGORITHM·CULTURE。",
        "entry": "python3 ~/longhun-system/bin/lh_wuxing_engine.py",
        "triggers_kw": ["五行", "金木水火土", "生克", "属性", "纳音", "干支", "天干", "地支", "五行属性", "五行分析"],
        "triggers_nl": ["五行属什么", "帮我判定五行", "金木水火土怎么看", "生克关系", "五行分析下", "纳音是什么", "天干地支五行"],
        "tribute": "致敬⚡️UID9622·五行生克·中华算法·不可替换",
    },
    {
        "name": "longhun-dao-de-jing",
        "category": "算法层",
        "version": "1.0",
        "desc_short": "龍魂·道德经锚点引擎 v1.0。81章道德经·算法锚定·哲学计算化。",
        "desc_full": "龍魂·道德经锚点引擎 v1.0。81章道德经原文+算法锚定点+哲学概念可计算化+与十维同演联动。当用户说道德经、老子、道可道、无为、上善若水——任一种说法都触发。语库: CULTURE·PHILOSOPHY。",
        "entry": "python3 ~/longhun-system/bin/lh_dao_de_jing_anchor.py",
        "triggers_kw": ["道德经", "老子", "道可道", "无为", "上善若水", "道教", "道家思想", "道德", "德", "道", "自然"],
        "triggers_nl": ["道德经怎么说", "老子这句话什么意思", "道可道非常道", "从道德经角度分析", "无为而治", "上善若水什么意思"],
        "tribute": "致敬⚡️UID9622·道德经81章·中华哲学原生锚点",
    },
    # ── 安全层 (Security) ──
    {
        "name": "longhun-vuln-detect",
        "category": "安全层",
        "version": "1.0",
        "desc_short": "龍魂·漏洞检测引擎 v1.0。代码漏洞扫描·依赖CVE检查·P77联动。",
        "desc_full": "龍魂·漏洞检测引擎 v1.0。代码级漏洞扫描(SQL注入/XSS/CSRF/路径穿越)+依赖CVE数据库检查+P77黑天使联动。当用户说漏洞检测、安全扫描、CVE、有没有漏洞——任一种说法都触发。语库: SECURITY·CRYPTO。",
        "entry": "python3 ~/longhun-system/bin/lh_vuln_detect.py",
        "triggers_kw": ["漏洞", "CVE", "扫描", "漏洞检测", "SQL注入", "XSS", "CSRF", "路径穿越", "安全扫描", "依赖检查"],
        "triggers_nl": ["扫描下漏洞", "有没有已知CVE", "代码有没有漏洞", "安全扫描下", "依赖有没有漏洞", "检查下安全问题"],
        "tribute": "致敬⚡️UID9622·漏洞检测·只扫自己的系统",
    },
    {
        "name": "longhun-ai-model",
        "category": "安全层",
        "version": "1.0",
        "desc_short": "龍魂·AI模型调用网关 v1.0。Ollama本地+混元/DeepSeek云端·省电路由·流式输出。",
        "desc_full": "龍魂·AI模型调用网关 v1.0。统一AI调用入口: Ollama本地模型(省电)+云端(混元/DeepSeek)·智能路由·流式输出·文本生成·图片生成。当用户说调用AI模型、用混元、用DeepSeek、文本生成、图片生成——任一种说法都触发。语库: AI·INFRA。",
        "entry": "python3 ~/longhun-system/bin/lh_ai_gateway.py",
        "triggers_kw": ["AI模型", "混元", "DeepSeek", "Ollama", "模型调用", "文本生成", "流式输出", "AI网关", "选模型", "图片生成"],
        "triggers_nl": ["调用AI模型", "用混元生成", "DeepSeek分析下", "Ollama跑一下", "选哪个模型好", "流式输出", "AI生成"],
        "tribute": "致敬⚡️UID9622·AI网关·省电路由·本地优先",
    },
    # ── 经济层 (Economy) ──
    {
        "name": "longhun-trust-score",
        "category": "经济层",
        "version": "1.0",
        "desc_short": "龍魂·信任积分引擎 v1.0。三分桶·场景矩阵判定·贡献公证·P20。",
        "desc_full": "龍魂·信任积分引擎 v1.0。P20贡献公证官·三分桶(技术/社区/创作)·场景矩阵判定·信任积分计算·政审·国资判定。当用户说积分、信任分、贡献、功德、公证——任一种说法都触发。语库: GOVERNANCE·ECONOMY。",
        "entry": "python3 ~/longhun-system/bin/lh_trust_score.py",
        "triggers_kw": ["积分", "信任分", "贡献", "功德", "公证", "政审", "国资", "三分桶", "P20", "场景判定"],
        "triggers_nl": ["我的信任积分多少", "算下积分", "贡献公证下", "查看功德值", "信任分怎么算", "贡献值多少", "三分桶分配"],
        "tribute": "致敬⚡️UID9622·信任积分·三分桶·贡献公证",
    },
    {
        "name": "longhun-xpay",
        "category": "经济层",
        "version": "1.0",
        "desc_short": "龍魂·经济引擎 v1.0。许愿池·XPay支付·多币种·经济核算·P07管仲。",
        "desc_full": "龍魂·经济引擎 v1.0。许愿池(众筹/打赏)·XPay支付网关·多币种支持·经济核算·资源优化·ROI分析。当用户说许愿池、支付、打赏、经济、成本、预算——任一种说法都触发。语库: ECONOMY·PAYMENT。",
        "entry": "python3 ~/longhun-system/bin/lh_xpay_engine.py",
        "triggers_kw": ["许愿池", "支付", "打赏", "经济", "成本", "预算", "XPay", "多币种", "核算", "ROI", "P07"],
        "triggers_nl": ["许愿池怎么用", "经济核算下", "成本分析", "预算够不够", "打赏功能", "XPay支付", "ROI分析", "资源优化"],
        "tribute": "致敬⚡️UID9622·许愿池·经济引擎·资源优化",
    },
    # ── 工具层 (Tools) ──
    {
        "name": "longhun-cnsh-translate",
        "category": "工具层",
        "version": "1.0",
        "desc_short": "龍魂·CNSH代码翻译引擎 v1.0。中文神经符号混合语言·AST解析·Python互译。",
        "desc_full": "龍魂·CNSH代码翻译引擎 v1.0。中华自主编程语言CNSH: 中文→Python翻译+AST解析+语法高亮+错误诊断+命名规范(繁体「龍」永存)。当用户说CNSH、翻译代码、中文编程、CNSH语法——任一种说法都触发。语库: LANGUAGE·CULTURE。",
        "entry": "python3 ~/longhun-system/bin/lh_cnsh_translate.py",
        "triggers_kw": ["CNSH", "中文编程", "翻译代码", "中文代码", "AST", "语法", "神经符号", "命名规范", "繁体龍", "语言翻译"],
        "triggers_nl": ["翻译这段CNSH代码", "CNSH怎么写", "中文编程翻译", "CNSH语法是什么", "帮我翻译成Python", "AST解析下"],
        "tribute": "致敬⚡️UID9622·CNSH·中国人自己的编程语言·繁体龍永存",
    },
    {
        "name": "longhun-search",
        "category": "工具层",
        "version": "1.0",
        "desc_short": "龍魂·多源搜索引擎 v1.0。Bing搜索·结果缓存·来源审计·端口9631。",
        "desc_full": "龍魂·多源搜索引擎 v1.0。Bing多源搜索+深度页面提取+搜索结果缓存+来源审计(P05审核)+端口9631。当用户说搜索、查一下、搜一下、找资料——任一种说法都触发。语库: SEARCH·TOOL。",
        "entry": "python3 ~/longhun-system/bin/lh_search_engine.py",
        "triggers_kw": ["搜索", "搜", "查", "找资料", "Bing", "搜索引擎", "9631", "搜索缓存", "来源审计"],
        "triggers_nl": ["帮我搜索下", "查一下这个", "搜一下相关信息", "找找资料", "搜索引擎搜下", "搜Bing", "有没有缓存的搜索结果"],
        "tribute": "致敬⚡️UID9622·搜索引擎·来源审计·不搜隐私",
    },
    # ── 总控 (Orchestrator) ──
    {
        "name": "longhun-orchestrator",
        "category": "总控层",
        "version": "1.0",
        "desc_short": "龍魂·总控指挥台 v1.0。全局调度·42技能路由·Kimi技能协同·意图分发。",
        "desc_full": "龍魂·总控指挥台 v1.0。42龍魂技能+CodeBuddy内置技能统一调度: 意图解析→技能匹配→协同调用→结果汇总→审计签章。当用户说龍魂指挥、总控、全局调度、用什么技能、技能列表——任一种说法都触发。语库: GOVERNANCE·ORCHESTRATOR。",
        "entry": "无需独立入口·AI直接调用",
        "triggers_kw": ["总控", "指挥", "调度", "全局", "龍魂指挥", "技能列表", "有什么技能", "用哪个技能", "编排", "协同", "42技能"],
        "triggers_nl": ["龍魂指挥台", "总控调度", "全局调度下", "我们现在有什么技能", "有哪些龍魂技能", "帮我看下技能列表", "用哪个技能能解决", "42个技能分别是什么"],
        "tribute": "致敬⚡️UID9622·42技能总控·意图解析·统一调度",
        "is_orchestrator": True,
    },
]

# ═══════════════════════════════════════════════════════════════
# 技能文件生成逻辑
# ═══════════════════════════════════════════════════════════════

def generate_skill_md(skill):
    """生成 SKILL.md 内容"""
    name = skill["name"]
    version = skill["version"]
    desc_short = skill["desc_short"]
    desc_full = skill["desc_full"]
    entry = skill["entry"]
    triggers_kw = skill.get("triggers_kw", [])
    triggers_nl = skill.get("triggers_nl", [])
    category = skill.get("category", "未分类")
    tribute = skill.get("tribute", f"致敬⚡️UID9622·{name}")
    is_orch = skill.get("is_orchestrator", False)

    # 校验入口
    entry_ok, entry_info = validate_entry(entry)
    if entry_ok:
        final_entry = entry_info
        entry_status = ""
    else:
        final_entry = "# 规划中: " + entry_info
        entry_status = f"\n> {entry_info}"

    # 生成 v∞ DNA
    module_tag = name.replace("longhun-", "").replace("-", "_").upper()
    skill_dna = make_dna(f"SKILL-{module_tag}", "DEF", f"V{version}", "P1")

    # 生成 YAML 前置
    kw_yaml = "\n".join([f"    - {k}" for k in triggers_kw])
    nl_yaml = "\n".join([f"    - \"{n}\"" for n in triggers_nl])

    yaml_block = f"""---
name: {name}
description: {desc_full}
license: MIT
allowed-tools:
- python
metadata:
  version: '{version}'
  dna: '{skill_dna}'
  tribute: '#{tribute}'
  id: {name}
  entry: {final_entry}
  entry_valid: {entry_ok}
  trigger:
    keywords:
{kw_yaml}
    natural_phrases:
{nl_yaml}
  category: longhun
  workspace: /Users/zuimeidedeyihan/longhun-system
---"""

    # 如果是总控技能，生成特殊正文
    if is_orch:
        body = f"""
# 🐉 龍魂·总控指挥台 v{version}

**DNA**: `{skill_dna}`
**定位**: 42技能统一入口·意图解析·协同调度{entry_status}

---

## 🔥 核心职责

| 职责 | 说明 |
|:---|:---|
| **意图解析** | 理解用户自然语言→映射到最佳技能组合 |
| **技能路由** | 从42个龍魂技能中选择最合适的 |
| **协同调用** | 多技能联动（如审计+签章+归档） |
| **Kimi协同** | 龍魂技能不足时→调用CodeBuddy内置技能(Kimi 266+技能) |
| **结果审计** | 输出前过GATE-01~11，自动签章 |

---

## 📊 42技能全景

### 守护层 (6技能)
| 技能 | 一句话 |
|:---|:---|
| longhun-three-color-audit | 三色审计·十道闸口 |
| longhun-circuit-breaker | 四级熔断·降级矩阵 |
| longhun-gpg-sign | GPG签章·自动补签 |
| longhun-identity-verify | 六重身份核验 |
| longhun-anti-tamper | 防篡改扫描 |
| — | longhun-code-security* 代码安全审计 |

### 执行层 (8技能)
| 技能 | 一句话 |
|:---|:---|
| longhun-deploy | 一键部署·鲲鹏十步法 |
| longhun-deben-audit | 德本审计·离火运五问 |
| longhun-auto-heal | 自愈扫描·自动巡检 |
| longhun-memory-load | 记忆加载·焊死状态 |
| longhun-persona-orchestrate | 人格编排·20人格调度 |
| — | longhun-active-observer* 主动观察引擎 |
| — | longhun-dna-engine* DNA追溯·签名 |
| — | longhun-knowledge-cards* 知识卡片索引 |

### 算法层 (5技能)
| 技能 | 一句话 |
|:---|:---|
| longhun-digital-root | 数字根·369不动点 |
| longhun-wuxing | 五行判定·生克关系 |
| longhun-dao-de-jing | 道德经81章锚定 |
| — | longhun-bagua-router* 64卦路由 |
| — | longhun-philosophy* 十维同演引擎 |

### 安全层 (6技能)
| 技能 | 一句话 |
|:---|:---|
| longhun-vuln-detect | 漏洞检测·CVE扫描 |
| longhun-ai-model | AI模型调用网关 |
| — | longhun-black-angel* 红蓝对抗 |
| — | longhun-sovereign-gateway* 主权API网关 |
| — | longhun-anxiety-detector* PUA话术检测 |
| — | longhun-robot-score* 反图灵检测 |

### 语义层 (5技能)
| 技能 | 一句话 |
|:---|:---|
| — | longhun-semantic-parser* 语义解析·测谎 |
| — | longhun-semantic-drawers* 五层智能路由 |
| — | longhun-semantic-library* 语境语义库 |
| — | longhun-corpus-registry* 语库桥接器 |
| — | longhun-tongxinyi* 通心译 |

### 文化层 (4技能)
| 技能 | 一句话 |
|:---|:---|
| — | longhun-mind-link* 意念交流引擎 |
| — | longhun-longzhi-shou* 龍智守管家 |
| — | longhun-yijing* 易经起卦 |
| — | longhun-tongxin-ear* 通心耳 |

### 经济层 (2技能)
| 技能 | 一句话 |
|:---|:---|
| longhun-trust-score | 信任积分·三分桶 |
| longhun-xpay | 许愿池·支付网关 |

### 工具层 (4技能)
| 技能 | 一句话 |
|:---|:---|
| longhun-cnsh-translate | CNSH代码翻译 |
| longhun-search | 多源搜索引擎 |
| — | longhun-sandbox* 沙盒推演 |
| — | longhun-seamless-handoff* 无缝上下文接力 |

### 总控 (1)
| 技能 | 一句话 |
|:---|:---|
| **longhun-orchestrator** ← 当前 | **42技能总控·意图分发** |

> `*` = 预装技能（~/.codebuddy/skills/）。合计: 22预装 + 20新增 = **42技能**。

---

## 🎯 使用方式

```
用户: "帮我审计代码并部署到鲲鹏"
↓
总控解析:
  1. 代码审计 → longhun-code-security (审计)
  2. 三色审计 → longhun-three-color-audit (质量门)
  3. 安全扫描 → longhun-vuln-detect (漏洞)
  4. GPG签章 → longhun-gpg-sign (签名)
  5. 部署上线 → longhun-deploy (鲲鹏)
  6. 德本审计 → longhun-deben-audit (底线)
↓
结果汇总 → 审计签章 → 反馈用户
```

## 🔗 联动规则

- 部署前必过: deploy → vuln-detect → three-color-audit → gpg-sign → deben-audit
- 发布前必过: gpg-sign → three-color-audit → identity-verify
- 审计链路: 任意输出 → P05审计 → P15签章 → P03归档
- 熔断兜底: 任何红线 → circuit-breaker → P72龍盾

---
**DNA**: `{DNA_BASE}-ORCHESTRATOR-v{version}`
**三色**: 🟢 总控已就绪·42技能全景 🟡 新增技能待实测 🔴 无
"""
    else:
        # 普通技能正文
        body = f"""
# 🐉 龍魂·{name.replace("longhun-", "").replace("-", "·")}·{category}

**DNA**: `{skill_dna}`
**{tribute}**

---

## 触发时机

| 场景 | 动作 |
|:---|:---|
| 用户提到触发关键词 | 自动激活 |
| 通过总控路由调用 | longhun-orchestrator 调度 |

---

## 调用方式

```bash
cd ~/longhun-system
{final_entry}
```{entry_status}

---

## 触发关键词

{', '.join(triggers_kw[:8])}等

---

## 自然语言触发

- {chr(10) + '- '.join([''] + triggers_nl[:5])}

---

## 联动引擎

- P05三色审计（审计链路）
- P15签章（交付链路）
- P72龍盾（熔断兜底）
- longhun-orchestrator（总控调度）

---
**DNA**: `{skill_dna}`
"""

    return yaml_block + body


def check_existing_skill(name, force: bool = False):
    """检查技能是否已有完整 SKILL.md（用户级或项目级）"""
    locations = [
        ("用户级", USER_SKILLS_DIR / name),
        ("项目级", PROJECT_SKILLS_DIR / name),
    ]
    for loc_type, skill_dir in locations:
        if skill_dir.exists():
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                content = skill_md.read_text(encoding="utf-8")
                if "---" in content and "name:" in content and content.count("---") >= 2:
                    return {"exists": not force, "location": f"{loc_type}:{skill_dir}", "content": content}
    return {"exists": False, "location": None, "content": None}


def main():
    parser = argparse.ArgumentParser(description="龍魂 · CodeBuddy 技能批量生成器")
    parser.add_argument("--force", action="store_true", help="强制重生成已存在的 SKILL.md")
    parser.add_argument("--validate-only", action="store_true", help="仅校验入口脚本存在性，不写入文件")
    args = parser.parse_args()

    print("🐉 龍魂 · CodeBuddy 技能批量生成器 v1.1")
    print(f"   用户技能目录: {USER_SKILLS_DIR}")
    print(f"   项目技能目录: {PROJECT_SKILLS_DIR}")
    print(f"   技能总数: {len(SKILLS)}")
    print(f"   模式: {'仅校验' if args.validate_only else ('强制重生成' if args.force else '增量生成')}")
    print()

    if not args.validate_only:
        PROJECT_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    stats = {"skipped": 0, "created": 0, "errors": 0, "missing_entries": 0}
    existing_skills = []

    for skill in SKILLS:
        name = skill["name"]
        entry = skill.get("entry", "")
        entry_ok, entry_info = validate_entry(entry)
        if not entry_ok:
            stats["missing_entries"] += 1
            print(f"  ⚠️  {name}: {entry_info}")

        check = check_existing_skill(name, force=args.force)

        if check["exists"]:
            existing_skills.append({"name": name, "location": check["location"]})
            continue

        if args.validate_only:
            continue

        try:
            skill_dir = PROJECT_SKILLS_DIR / name
            skill_dir.mkdir(exist_ok=True)
            md_content = generate_skill_md(skill)
            (skill_dir / "SKILL.md").write_text(md_content, encoding="utf-8")
            print(f"  ✅ {'重生成' if args.force else '新建'} {name}/SKILL.md  ({skill['category']})")
            stats["created"] += 1
        except Exception as e:
            print(f"  ❌ {name} 创建失败: {e}")
            stats["errors"] += 1

    print(f"\n{'='*60}")
    print(f"📊 汇总:")
    print(f"   已有完整SKILL.md(跳过): {len(existing_skills)} 个")
    for s in existing_skills:
        print(f"     - {s['name']} ({s['location']})")
    print(f"   本次生成: {stats['created']} 个")
    print(f"   入口缺失: {stats['missing_entries']} 个")
    if stats["errors"]:
        print(f"   失败: {stats['errors']} 个")

    if not args.validate_only:
        print(f"\n📂 项目技能目录: {PROJECT_SKILLS_DIR}")
        print(f"   已加载的技能: {len(existing_skills)} (存在) + {stats['created']} (新生成) = {len(existing_skills) + stats['created']} 个")
        print(f"\n📌 下一步:")
        print(f"   - CodeBuddy 重启后自动加载")
        print(f"   - 问'龍魂有什么技能'验证")
        print(f"   - 问'龍魂指挥我该用哪个技能'测试总控路由")
        print(f"   - GPG签名: python3 bin/lh_gpg_sign.py sign .codebuddy/skills/")

    return 0


if __name__ == "__main__":
    sys.exit(main())
