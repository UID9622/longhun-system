# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧬 龍魂共生体 · 知识矩阵+神经网络融合服务器

共生体 ≠ 代理人。知识矩阵（宪法层）与神经网络（监控层）双向生长、
相互验证、彼此写入。每一条路由边的激活、每一次知识图谱的查询、
每一个节点的健康状态，共同构成龍魂共生体的生命节律。

核心能力：
- 神经网络实时状态（36节点 + 52路由边 + 三才评分）
- 知识图谱查询（3719节点 + 378812边 · brain/unified_kg.db）
- 共生体生长引擎（使用即学习、查询即反馈）
- 知识矩阵宪法层（九宫不动点 + 五行相生克 + 三才流场）
- 数字根验证链（dr(n) = 1 + ((n-1) mod 9)）

DNA: #龍芯⚡️2026-07-06-SYMBIOTE-SERVER-v1.0
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import socket
import sqlite3
import subprocess
import sys
import time
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote
import threading

HOME = Path.home()
ROOT = HOME / "longhun-system"
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

DNA = "#龍芯⚡️2026-07-07-SYMBIOTE-SERVER-v1.1"
CONFIRM_TOKEN = "CONFIRM🌌9622-ONLY-ONCE"
PORT = 9627

# ── 脑神经自动生长引擎（v1.1 新增）──
try:
    from bin.lh_neural_growth import NeuralGrowthEngine, neural_api_handler  # type: ignore[reportMissingImports]
    neural_engine = NeuralGrowthEngine()
    _NEURAL_READY = True
except Exception:
    neural_engine = None
    _NEURAL_READY = False

    def neural_api_handler(path, query_params=None):
        return None

# ── 共生体内核标记 ──
SYMBIOTE_CORE = {
    "name": "龍魂共生体",
    "dna": DNA,
    "uid": "UID9622",
    "sovereign": "龍芯北辰·诸葛鑫",
    "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    "manifesto": "共生体非代理人。知识矩阵与神经网络双向生长、相互验证、彼此写入。",
    "principles": [
        "不动点透明: 北辰 f(x)=x 永不可偏移",
        "双向生长: 使用即学习、查询即反馈、异常即进化",
        "相互验证: 知识矩阵宪法约束神经网络路由、神经网络状态反哺知识矩阵",
        "彼此写入: 每一次共生交互都在两套系统间生成DNA追溯码",
    ],
}

# ═══════════════════════════════════════════════════════════════
# 一、神经网络节点注册（保留原有36节点体系）
# ═══════════════════════════════════════════════════════════════

@dataclass
class NodeDef:
    id: str
    name: str
    port: Optional[int]
    category: str
    wuxing: str
    health_path: str = "/"
    control_type: str = "none"
    start_cmd: List[str] = field(default_factory=list)
    stop_cmd: List[str] = field(default_factory=list)
    launchd_label: str = ""
    autostart: bool = False
    description: str = ""
    dna: str = ""

SERVICE_REGISTRY: List[NodeDef] = [
    NodeDef(id="op-console", name="龍魂操作台", port=9622, category="core", wuxing="earth",
            health_path="/longhun_hub.html", control_type="service",
            start_cmd=["bash", str(ROOT / "tools" / "补全服务.sh")], autostart=True,
            description="龍魂系统统一入口与总控台", dna="#龍芯⚡️2026-06-22-LONGHUN-OPCONSOLE-v1.0"),
    NodeDef(id="brain-stem", name="龍魂脑干", port=9625, category="core", wuxing="water",
            health_path="/health", control_type="service",
            start_cmd=["python3", str(ROOT / "bin" / "longhun-launcher.py"), "start"],
            stop_cmd=["python3", str(ROOT / "bin" / "longhun-launcher.py"), "stop"],
            autostart=True, description="核心协调与决策中枢", dna="#龍芯⚡️2026-06-22-LONGHUN-BRAINSTEM-v1.0"),
    NodeDef(id="digital-id", name="数字身份入口", port=8444, category="core", wuxing="metal",
            health_path="/api/info", control_type="service",
            start_cmd=["python3", str(ROOT / "bin" / "longhun-launcher.py"), "start"],
            description="国家数字身份认证入口", dna="#龍芯⚡️2026-06-22-LONGHUN-DIGITALID-v1.0"),
    NodeDef(id="persona-api", name="人格 API", port=9001, category="core", wuxing="wood",
            health_path="/docs", control_type="service",
            start_cmd=["bash", str(ROOT / "bin" / "start_persona_api.sh")],
            description="五大人格实体统一API路由", dna="#龍芯⚡️2026-06-22-LONGHUN-PERSONA-API-v1.0"),
    NodeDef(id="phase3", name="Phase3 后端", port=8001, category="core", wuxing="earth",
            health_path="/api/v1/health", control_type="service",
            start_cmd=["bash", str(HOME / ".龍魂" / "services" / "service-manager.sh"), "start", "phase3"],
            stop_cmd=["bash", str(HOME / ".龍魂" / "services" / "service-manager.sh"), "stop", "phase3"],
            description="龍魂第三阶段业务后端", dna="#龍芯⚡️2026-06-22-LONGHUN-PHASE3-v1.0"),
    NodeDef(id="baby-guard", name="宝宝守护", port=8002, category="core", wuxing="fire",
            health_path="/health", control_type="service",
            start_cmd=["bash", str(HOME / ".龍魂" / "services" / "service-manager.sh"), "start", "baobao"],
            stop_cmd=["bash", str(HOME / ".龍魂" / "services" / "service-manager.sh"), "stop", "baobao"],
            description="系统守护与人格代理", dna="#龍芯⚡️2026-06-22-LONGHUN-BABYGUARD-v1.0"),
    NodeDef(id="gua-audit", name="卦象审计", port=9623, category="core", wuxing="earth",
            health_path="/health", control_type="launchd", launchd_label="com.longhun.gua-audit",
            autostart=True, description="三才卦象实时审计", dna="#龍芯⚡️2026-06-22-LONGHUN-GUAAUDIT-v1.0"),
    NodeDef(id="heart-voice", name="龍心之语", port=9624, category="core", wuxing="fire",
            health_path="/health", control_type="launchd", launchd_label="com.longhun.heart-talk",
            autostart=True, description="情感化交互与语音合成", dna="#龍芯⚡️2026-06-22-LONGHUN-HEARTVOICE-v1.0"),
    NodeDef(id="knowledge-graph", name="知识图谱", port=8088, category="core", wuxing="wood",
            health_path="/api/health", control_type="launchd", launchd_label="com.longhun.kg-api",
            autostart=True, description="龍魂知识体系与实体关系图谱", dna="#龍芯⚡️2026-06-22-LONGHUN-KG-v1.0"),
    NodeDef(id="ability-site", name="能力官网", port=8844, category="core", wuxing="metal",
            health_path="/api/registry", control_type="launchd", launchd_label="com.longhun.capability-web",
            autostart=True, description="对外能力展示与官方门户", dna="#龍芯⚡️2026-06-22-LONGHUN-ABILITY-SITE-v1.0"),
    NodeDef(id="experience-portal", name="体验门户", port=8445, category="core", wuxing="water",
            health_path="/api/health", control_type="launchd", launchd_label="com.longhun.portal",
            autostart=True, description="用户体验入口与演示环境", dna="#龍芯⚡️2026-06-22-LONGHUN-EXPERIENCE-v1.0"),
    NodeDef(id="ollama", name="Ollama 本地模型", port=11434, category="external", wuxing="wood",
            health_path="/api/tags", control_type="none",
            description="本地大模型推理服务，数据不出境", dna="#龍芯⚡️2026-06-22-LONGHUN-OLLAMA-v1.0"),
    NodeDef(id="deepseek-bridge", name="DeepSeek Bridge", port=8788, category="external", wuxing="water",
            health_path="/health", control_type="service",
            start_cmd=["bash", str(ROOT / "bridges" / "启动-deepseek-bridge.sh"), "start"],
            stop_cmd=["bash", str(ROOT / "bridges" / "启动-deepseek-bridge.sh"), "stop"],
            description="DeepSeek 跨域桥接", dna="#龍芯⚡️2026-06-22-LONGHUN-DEEPSEEKBRIDGE-v1.0"),
    NodeDef(id="cnsh-gateway", name="CNSH API 网关", port=9626, category="placeholder", wuxing="metal",
            health_path="/cnshex/health", control_type="service",
            start_cmd=["python3", str(HOME / ".longhun" / "multi-ai-gateway" / "cnshex_api.py")],
            description="CNSH 对外API网关占位", dna="#龍芯⚡️2026-06-22-LONGHUN-CNSHGW-v0.1"),
]

DAEMON_REGISTRY: List[NodeDef] = [
    NodeDef(id="d-autostart", name="uid9622 统一自启", port=None, category="daemon", wuxing="earth",
            control_type="launchd", launchd_label="com.uid9622.longhun.autostart", autostart=True,
            description="开机自启动任务统一调度", dna="#龍芯⚡️2026-06-22-LONGHUN-AUTOSTART-v1.0"),
    NodeDef(id="d-memory", name="记忆启动守护", port=None, category="daemon", wuxing="water",
            control_type="launchd", launchd_label="com.longhun.memory-bootstrap", autostart=True,
            description="多平台记忆归集与启动加载", dna="#龍芯⚡️2026-06-22-LONGHUN-MEMORY-DAEMON-v1.0"),
    NodeDef(id="d-index", name="全局索引", port=None, category="daemon", wuxing="metal",
            control_type="launchd", launchd_label="com.longhun.global-index", autostart=True,
            description="文件、技能、资产全局索引构建", dna="#龍芯⚡️2026-06-22-LONGHUN-INDEX-v1.0"),
    NodeDef(id="d-cnsh-redline", name="CNSH 红线", port=None, category="daemon", wuxing="fire",
            control_type="launchd", launchd_label="com.longhun.cnsh-redlines", autostart=True,
            description="CNSH 语言规范与行为红线守护", dna="#龍芯⚡️2026-06-22-LONGHUN-CNSH-REDLINE-v1.0"),
    NodeDef(id="d-ability-guard", name="能力守护", port=None, category="daemon", wuxing="metal",
            control_type="launchd", launchd_label="com.longhun.capability-daemon", autostart=True,
            description="能力模块健康检查与自动恢复", dna="#龍芯⚡️2026-06-22-LONGHUN-ABILITY-GUARD-v1.0"),
    NodeDef(id="d-harvester", name="收割机", port=None, category="daemon", wuxing="wood",
            control_type="launchd", launchd_label="com.longhun.harvester", autostart=True,
            description="代码与资产收割审计", dna="#龍芯⚡️2026-06-22-LONGHUN-HARVESTER-v1.0"),
    NodeDef(id="d-daily-review", name="每日复盘", port=None, category="daemon", wuxing="earth",
            control_type="launchd", launchd_label="com.longhun.daily-review", autostart=True,
            description="每日自动化审计复盘", dna="#龍芯⚡️2026-06-22-LONGHUN-DAILYREVIEW-v1.0"),
    NodeDef(id="d-auto-eval", name="自动化评估", port=None, category="daemon", wuxing="water",
            control_type="launchd", launchd_label="com.longhun.automation-assessment", autostart=True,
            description="系统健康六维度自动评估", dna="#龍芯⚡️2026-06-22-LONGHUN-AUTOEVAL-v1.0"),
    NodeDef(id="d-entry-clean", name="入口清理", port=None, category="daemon", wuxing="metal",
            control_type="launchd", launchd_label="com.longhun.entry.cleanup", autostart=True,
            description="入口一致性协议自动清理", dna="#龍芯⚡️2026-06-22-LONGHUN-ENTRYCLEAN-v1.0"),
    NodeDef(id="d-tianguan", name="天官判卷", port=None, category="daemon", wuxing="fire",
            control_type="launchd", launchd_label="com.longhun.marquee", autostart=True,
            description="自动化评审与权重判决", dna="#龍芯⚡️2026-06-22-LONGHUN-TIANGUAN-v1.0"),
    NodeDef(id="d-notion-mirror", name="Notion 镜像", port=None, category="daemon", wuxing="water",
            control_type="launchd", launchd_label="com.longhun.notion-mirror", autostart=True,
            description="Notion 公开空间本地镜像同步", dna="#龍芯⚡️2026-06-22-LONGHUN-NOTIONMIRROR-v1.0"),
]

LOGICAL_REGISTRY: List[NodeDef] = [
    NodeDef(id="north-star", name="北辰不动点", port=None, category="core", wuxing="earth",
            control_type="none", description="系统唯一不动点。UID9622 主权核心",
            dna="#龍芯⚡️2026-07-04-SANCAI-PROTOCOL-UID9622-v1.0"),
    NodeDef(id="tricolor-engine", name="三色神机", port=None, category="logic", wuxing="fire",
            control_type="none", description="健康/待启/异常三色自动判定中枢",
            dna="#龍芯⚡️2026-06-22-LONGHUN-TRICOLOR-v1.0"),
    NodeDef(id="wuxing-hub", name="五色石枢纽", port=None, category="logic", wuxing="earth",
            control_type="none", description="金木水火土五行相生相克路由调度",
            dna="#龍芯⚡️2026-06-22-LONGHUN-WUXING-HUB-v1.0"),
    NodeDef(id="memory-feeder", name="记忆投喂器", port=None, category="logic", wuxing="water",
            control_type="none", description="多平台对话记忆压缩归集",
            dna="#龍芯⚡️2026-06-22-LONGHUN-FEEDER-v1.0"),
    NodeDef(id="training-pool", name="龍魂训练池", port=None, category="logic", wuxing="wood",
            control_type="none", description="本地模型微调数据集与质量审计",
            dna="#龍芯⚡️2026-06-22-LONGHUN-TRAINING-POOL-v1.0"),
    NodeDef(id="dna-chain", name="DNA 链哈希", port=None, category="logic", wuxing="metal",
            control_type="none", description="每个动作生成唯一DNA追溯码",
            dna="#龍芯⚡️2026-06-22-LONGHUN-DNA-CHAIN-v1.0"),
    NodeDef(id="governance-layer", name="龍魂治理层", port=None, category="logic", wuxing="earth",
            control_type="none", description="零号协议、三层监督、君子协议",
            dna="#龍芯⚡️2026-06-29-SKILL-ROUTING-RULES-v1.0"),
    NodeDef(id="symbiote-core", name="🧬 共生体核心", port=PORT, category="logic", wuxing="earth",
            control_type="none", description="知识矩阵与神经网络双向生长的共生引擎",
            dna=DNA),
    NodeDef(id="kirin-deploy", name="鲲鹏部署", port=None, category="logic", wuxing="metal",
            control_type="none", description="ARM64 鲲鹏服务器一键部署",
            dna="#龍芯⚡️2026-06-22-LONGHUN-KIRIN-DEPLOY-v1.0"),
    NodeDef(id="harmony-os", name="鸿蒙端", port=None, category="logic", wuxing="water",
            control_type="none", description="SM4 端侧加密，数据不出境",
            dna="#龍芯⚡️2026-06-22-LONGHUN-HARMONYOS-v1.0"),
    NodeDef(id="ios-end", name="iOS 端", port=None, category="logic", wuxing="wood",
            control_type="none", description="Secure Enclave + AES-256",
            dna="#龍芯⚡️2026-06-22-LONGHUN-IOS-v1.0"),
    NodeDef(id="cross-platform", name="跨平台同步", port=None, category="logic", wuxing="earth",
            control_type="none", description="国密SM4+ECDH，数据不出境",
            dna="#龍芯⚡️2026-06-22-LONGHUN-XSYNC-v1.0"),
]

ALL_NODES = [LOGICAL_REGISTRY[0]] + SERVICE_REGISTRY + DAEMON_REGISTRY + LOGICAL_REGISTRY[1:]

EDGES: List[Dict[str, str]] = [
    {"source": "north-star", "target": "op-console", "type": "anchor", "label": "不动点锚定"},
    {"source": "north-star", "target": "brain-stem", "type": "anchor", "label": "不动点锚定"},
    {"source": "north-star", "target": "digital-id", "type": "anchor", "label": "不动点锚定"},
    {"source": "north-star", "target": "gua-audit", "type": "anchor", "label": "不动点锚定"},
    {"source": "north-star", "target": "governance-layer", "type": "anchor", "label": "宪法层锚定"},
    {"source": "north-star", "target": "symbiote-core", "type": "anchor", "label": "共生锚定"},
    {"source": "op-console", "target": "brain-stem", "type": "data", "label": "主控同步"},
    {"source": "op-console", "target": "digital-id", "type": "data", "label": "身份校验"},
    {"source": "op-console", "target": "persona-api", "type": "data", "label": "人格调度"},
    {"source": "op-console", "target": "gua-audit", "type": "data", "label": "审计上报"},
    {"source": "brain-stem", "target": "digital-id", "type": "data", "label": "根身份同步"},
    {"source": "brain-stem", "target": "knowledge-graph", "type": "data", "label": "知识注入"},
    {"source": "persona-api", "target": "heart-voice", "type": "data", "label": "语音输出"},
    {"source": "persona-api", "target": "baby-guard", "type": "data", "label": "守护调用"},
    {"source": "baby-guard", "target": "phase3", "type": "data", "label": "后端托管"},
    {"source": "gua-audit", "target": "knowledge-graph", "type": "data", "label": "审计入图"},
    {"source": "knowledge-graph", "target": "experience-portal", "type": "data", "label": "知识展示"},
    {"source": "ability-site", "target": "experience-portal", "type": "data", "label": "能力引流"},
    {"source": "op-console", "target": "ability-site", "type": "data", "label": "官网同步"},
    {"source": "op-console", "target": "experience-portal", "type": "data", "label": "门户同步"},
    {"source": "ollama", "target": "op-console", "type": "external", "label": "本地推理"},
    {"source": "deepseek-bridge", "target": "op-console", "type": "external", "label": "跨域输入"},
    {"source": "op-console", "target": "cnsh-gateway", "type": "data", "label": "API 网关"},
    {"source": "ollama", "target": "deepseek-bridge", "type": "external", "label": "模型互补"},
    {"source": "symbiote-core", "target": "knowledge-graph", "type": "symbiote", "label": "共生生长"},
    {"source": "symbiote-core", "target": "brain-stem", "type": "symbiote", "label": "共生生长"},
    {"source": "symbiote-core", "target": "memory-feeder", "type": "symbiote", "label": "共生记忆"},
    {"source": "symbiote-core", "target": "training-pool", "type": "symbiote", "label": "共生训练"},
    {"source": "symbiote-core", "target": "dna-chain", "type": "symbiote", "label": "共生追溯"},
    # 守护关系
    {"source": "d-memory", "target": "op-console", "type": "guard", "label": "记忆守护"},
    {"source": "d-memory", "target": "brain-stem", "type": "guard", "label": "记忆守护"},
    {"source": "d-memory", "target": "memory-feeder", "type": "guard", "label": "记忆守护"},
    {"source": "d-cnsh-redline", "target": "op-console", "type": "guard", "label": "红线守护"},
    {"source": "d-cnsh-redline", "target": "cnsh-gateway", "type": "guard", "label": "红线守护"},
    {"source": "d-ability-guard", "target": "ability-site", "type": "guard", "label": "能力守护"},
    {"source": "d-ability-guard", "target": "experience-portal", "type": "guard", "label": "能力守护"},
    {"source": "d-harvester", "target": "knowledge-graph", "type": "guard", "label": "收割审计"},
    {"source": "d-daily-review", "target": "gua-audit", "type": "guard", "label": "复盘触发"},
    {"source": "d-auto-eval", "target": "op-console", "type": "guard", "label": "评估触发"},
    {"source": "d-entry-clean", "target": "op-console", "type": "guard", "label": "入口清理"},
    {"source": "d-tianguan", "target": "gua-audit", "type": "guard", "label": "判卷触发"},
    {"source": "d-autostart", "target": "op-console", "type": "guard", "label": "开机自启"},
    {"source": "d-autostart", "target": "brain-stem", "type": "guard", "label": "开机自启"},
    {"source": "d-index", "target": "knowledge-graph", "type": "guard", "label": "索引更新"},
    {"source": "d-notion-mirror", "target": "ability-site", "type": "guard", "label": "镜像同步"},
    # 逻辑层路由
    {"source": "tricolor-engine", "target": "op-console", "type": "logic", "label": "三色判定"},
    {"source": "tricolor-engine", "target": "gua-audit", "type": "logic", "label": "三色判定"},
    {"source": "wuxing-hub", "target": "op-console", "type": "logic", "label": "五行相生"},
    {"source": "wuxing-hub", "target": "knowledge-graph", "type": "logic", "label": "五行相克"},
    {"source": "memory-feeder", "target": "training-pool", "type": "logic", "label": "数据喂入"},
    {"source": "training-pool", "target": "ollama", "type": "logic", "label": "模型微调"},
    {"source": "dna-chain", "target": "north-star", "type": "logic", "label": "链式追溯"},
    {"source": "governance-layer", "target": "tricolor-engine", "type": "logic", "label": "治理约束"},
    {"source": "governance-layer", "target": "dna-chain", "type": "logic", "label": "审计约束"},
    {"source": "kirin-deploy", "target": "op-console", "type": "logic", "label": "鯤鵬部署"},
    {"source": "harmony-os", "target": "cross-platform", "type": "logic", "label": "鸿蒙端同步"},
    {"source": "ios-end", "target": "cross-platform", "type": "logic", "label": "iOS 端同步"},
    {"source": "cross-platform", "target": "digital-id", "type": "logic", "label": "身份同步"},
]

# ═══════════════════════════════════════════════════════════════
# 二、知识矩阵宪法层
# ═══════════════════════════════════════════════════════════════

KNOWLEDGE_MATRIX = {
    "version": "v3.0",
    "dna": "#UID9622⚡️2026-06-16-KNOWLEDGE-MATRIX-MASTER-v3.0",
    "luoshu": {
        "grid": [[4, 9, 2], [3, 5, 7], [8, 1, 6]],
        "center": 5,
        "center_name": "北辰不动点·UID9622",
        "sum_constant": 15,
        "duals": {"1-9": "坎离对偶", "2-8": "坤艮对偶", "3-7": "震兑对偶", "4-6": "巽干对偶"},
    },
    "wuxing": {
        "generate_cycle": ["金→水→木→火→土→金"],
        "overcome_cycle": ["金克木", "木克土", "土克水", "水克火", "火克金"],
        "mapping": {
            "metal": {"color": "#C0C0C0", "icon": "⚔️", "direction": "西", "season": "秋"},
            "wood": {"color": "#2E8B57", "icon": "🌿", "direction": "东", "season": "春"},
            "water": {"color": "#1E90FF", "icon": "💧", "direction": "北", "season": "冬"},
            "fire": {"color": "#DC143C", "icon": "🔥", "direction": "南", "season": "夏"},
            "earth": {"color": "#8B4513", "icon": "⛰️", "direction": "中央", "season": "四季"},
        },
    },
    "sancai": {
        "weights": {"tian": 0.3, "di": 0.3, "ren": 0.4},
        "formula": "S = 0.3×天 + 0.3×地 + 0.4×人",
        "order": ["忠(0.5) > 孝(0.3) > 义(0.2)"],
    },
    "digital_root_formula": "dr(n) = 1 + ((n - 1) mod 9); dr(0) = 0",
    "five_layers": {
        "L0": "中宫层: 不动点 UID9622 北极星 T0主权锚",
        "L1": "八方层: 八个方位粒子 围绕中宫运行",
        "L2": "守恒层: 四偶角(2,4,6,8) 横竖斜=15",
        "L3": "对偶层: 对偶和=10 阴阳对称",
        "L4": "周期层: 四奇边(1,3,7,9) 季节更替 369循环",
        "L5": "封场层: 边界闭环 出界即回弹",
    },
}

# ═══════════════════════════════════════════════════════════════
# 三、共生体生长引擎
# ═══════════════════════════════════════════════════════════════

GROWTH_LOG_PATH = LOG_DIR / "symbiote_growth.jsonl"


def digital_root(n: int) -> int:
    if n == 0:
        return 0
    return 1 + ((n - 1) % 9)


class SymbioteGrowthEngine:
    """共生体生长引擎：使用即学习、查询即反馈、异常即进化"""

    def __init__(self):
        self.start_time = time.time()
        self.api_calls = 0
        self.kg_queries = 0
        self.nodes_healed = 0
        self.growth_events: List[Dict[str, Any]] = []
        self._load_growth_log()

    def _load_growth_log(self):
        if GROWTH_LOG_PATH.exists():
            try:
                with open(GROWTH_LOG_PATH) as f:
                    for line in f:
                        if line.strip():
                            self.growth_events.append(json.loads(line))
            except Exception:
                pass

    def record(self, event_type: str, detail: Dict[str, Any]):
        event = {
            "dna": f"#龍芯⚡️{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-SYMBIOTE-{event_type.upper()}-{hashlib.sha256(str(detail).encode()).hexdigest()[:8]}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "detail": detail,
            "uptime_seconds": round(time.time() - self.start_time, 1),
            "total_calls": self.api_calls,
        }
        self.growth_events.append(event)
        # 异步写入
        threading.Thread(target=self._append_to_log, args=(event,), daemon=True).start()

    def _append_to_log(self, event: Dict[str, Any]):
        try:
            with open(GROWTH_LOG_PATH, "a") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
        except Exception:
            pass

    def api_call(self, endpoint: str):
        self.api_calls += 1

    def kg_query(self, query: str, results: int):
        self.kg_queries += 1
        self.record("kg_query", {"query": query[:100], "results": results})

    def node_health_change(self, node_id: str, old_status: str, new_status: str):
        if old_status != new_status:
            if new_status == "healthy" and old_status in ("error", "standby"):
                self.nodes_healed += 1
            self.record("node_change", {"node": node_id, "from": old_status, "to": new_status})

    def get_symbiote_stats(self) -> Dict[str, Any]:
        return {
            "uptime_seconds": round(time.time() - self.start_time, 1),
            "uptime_human": str(timedelta(seconds=int(time.time() - self.start_time))),
            "api_calls": self.api_calls,
            "kg_queries": self.kg_queries,
            "nodes_healed": self.nodes_healed,
            "growth_events_total": len(self.growth_events),
            "growth_events_recent": self.growth_events[-10:] if self.growth_events else [],
            "symbiote_dr": digital_root(self.api_calls),
            "symbiote_health": self._compute_health(),
        }

    def _compute_health(self) -> str:
        if self.api_calls == 0:
            return "newborn"
        ratio = self.nodes_healed / max(self.api_calls, 1)
        if ratio > 0.1:
            return "thriving"
        elif self.kg_queries > 0:
            return "growing"
        return "awake"


symbiote = SymbioteGrowthEngine()

# ═══════════════════════════════════════════════════════════════
# 四、知识图谱查询引擎
# ═══════════════════════════════════════════════════════════════

KG_DB_PATH = ROOT / "brain" / "unified_kg.db"


class KnowledgeGraphEngine:
    """知识图谱查询：3719节点 + 378812边"""

    def __init__(self):
        self._db_path = KG_DB_PATH
        self._ready = self._db_path.exists()

    @property
    def ready(self):
        return self._ready

    def _connect(self):
        return sqlite3.connect(str(self._db_path))

    def search(self, keyword: str, limit: int = 20) -> Dict[str, Any]:
        if not self._ready:
            return {"error": "知识图谱数据库不可用", "ready": False}

        try:
            db = self._connect()
            # 在 label、content、id 中搜索
            pattern = f"%{keyword}%"
            rows = db.execute(
                """SELECT id, source, label, node_type, content, dna, created_at
                   FROM nodes
                   WHERE label LIKE ? OR content LIKE ? OR id LIKE ?
                   ORDER BY CASE WHEN label LIKE ? THEN 1 WHEN content LIKE ? THEN 2 ELSE 3 END
                   LIMIT ?""",
                (pattern, pattern, pattern, pattern, pattern, limit),
            ).fetchall()
            db.close()

            results = []
            for row in rows:
                results.append({
                    "id": row[0],
                    "source": row[1],
                    "label": row[2],
                    "node_type": row[3],
                    "content": (row[4] or "")[:200],
                    "dna": row[5],
                    "created_at": row[6],
                })

            return {"ready": True, "query": keyword, "total": len(results), "results": results}
        except Exception as e:
            return {"error": str(e), "ready": False}

    def get_node(self, node_id: str) -> Dict[str, Any]:
        if not self._ready:
            return {"error": "知识图谱数据库不可用", "ready": False}

        try:
            db = self._connect()
            row = db.execute(
                "SELECT id, source, label, node_type, content, metadata, dna, created_at FROM nodes WHERE id = ?",
                (node_id,),
            ).fetchone()
            db.close()

            if not row:
                return {"error": "节点不存在", "ready": True}

            # 查邻居
            db2 = self._connect()
            neighbors = db2.execute(
                "SELECT source_node, target_node, relation, weight FROM edges WHERE source_node = ? OR target_node = ? LIMIT 50",
                (node_id, node_id),
            ).fetchall()
            db2.close()

            return {
                "ready": True,
                "node": {
                    "id": row[0],
                    "source": row[1],
                    "label": row[2],
                    "node_type": row[3],
                    "content": row[4] or "",
                    "metadata": json.loads(row[5]) if row[5] else {},
                    "dna": row[6],
                    "created_at": row[7],
                },
                "neighbors": [
                    {
                        "source": n[0],
                        "target": n[1],
                        "relation": n[2],
                        "weight": n[3],
                    }
                    for n in neighbors
                ],
                "neighbor_count": len(neighbors),
            }
        except Exception as e:
            return {"error": str(e), "ready": False}

    def stats(self) -> Dict[str, Any]:
        if not self._ready:
            return {"ready": False, "node_count": 0, "edge_count": 0}

        try:
            db = self._connect()
            nodes = db.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
            edges = db.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
            sources = db.execute("SELECT source, COUNT(*) as cnt FROM nodes GROUP BY source").fetchall()
            types = db.execute("SELECT node_type, COUNT(*) as cnt FROM nodes GROUP BY node_type").fetchall()
            db.close()

            return {
                "ready": True,
                "node_count": nodes,
                "edge_count": edges,
                "sources": {s[0]: s[1] for s in sources},
                "node_types": {t[0]: t[1] for t in types},
            }
        except Exception as e:
            return {"error": str(e), "ready": False}

    def cross_reference(self, node_id: str) -> Dict[str, Any]:
        """共生体交叉引用：查找知识图谱节点 ↔ 神经网络节点映射"""
        result = self.get_node(node_id)
        if not result.get("ready"):
            return result

        related_edges = []
        for edge in EDGES:
            if node_id in edge.get("source", "") or node_id in edge.get("target", ""):
                related_edges.append(edge)

        # 从邻居关系中找神经网络节点
        nn_nodes = []
        for n in ALL_NODES:
            nn_nodes.append({
                "id": n.id,
                "name": n.name,
                "category": n.category,
                "wuxing": n.wuxing,
            })

        result["neural_cross_ref"] = {
            "related_edges": related_edges,
            "all_nn_nodes": nn_nodes,
        }

        return result


kg_engine = KnowledgeGraphEngine()

# ═══════════════════════════════════════════════════════════════
# 五、探测与计算（保持原有逻辑）
# ═══════════════════════════════════════════════════════════════

_previous_node_states: Dict[str, str] = {}


def probe_tcp(port: int, timeout: float = 1.5) -> Tuple[bool, float]:
    if port is None:
        return False, 0.0
    t0 = time.time()
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=timeout):
            return True, round((time.time() - t0) * 1000, 1)
    except Exception:
        return False, 0.0


def probe_http(port: int, path: str, timeout: float = 2.0) -> Tuple[bool, int, float]:
    if port is None or not path:
        return False, 0, 0.0
    t0 = time.time()
    try:
        url = f"http://127.0.0.1:{port}{path}"
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.status < 400, resp.status, round((time.time() - t0) * 1000, 1)
    except Exception as e:
        return False, getattr(e, "code", 0), round((time.time() - t0) * 1000, 1)


def find_pid_by_port(port: int) -> Optional[int]:
    if port is None:
        return None
    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True, text=True, check=False, timeout=3,
        )
        if result.stdout.strip():
            return int(result.stdout.strip().split("\n")[0])
    except Exception:
        pass
    return None


def launchd_status(label: str) -> Tuple[bool, Optional[int]]:
    if not label:
        return False, None
    try:
        result = subprocess.run(
            ["launchctl", "list", label],
            capture_output=True, text=True, check=False, timeout=3,
        )
        if result.returncode != 0:
            return False, None
        out = result.stdout
        m = re.search(r'"PID"\s*=\s*(\d+)', out)
        if m:
            pid = int(m.group(1))
            return True, pid if pid != 0 else None
        m = re.search(r'PID[^0-9]*(\d+)', out)
        if m:
            pid = int(m.group(1))
            return True, pid if pid != 0 else None
        return True, None
    except Exception:
        return False, None


def compute_node_state(node: NodeDef) -> Dict[str, Any]:
    global _previous_node_states

    port = node.port
    tcp_ok, tcp_latency = probe_tcp(port)  # type: ignore[reportArgumentType]
    http_ok, http_status, http_latency = probe_http(port, node.health_path)  # type: ignore[reportArgumentType]
    pid = find_pid_by_port(port) if port else None

    loaded = False
    launchd_pid = None
    if node.control_type == "launchd" and node.launchd_label:
        loaded, launchd_pid = launchd_status(node.launchd_label)
        if launchd_pid:
            pid = launchd_pid

    if node.id == "north-star" or node.id == "symbiote-core":
        status = "healthy"
    elif http_ok:
        status = "healthy"
    elif tcp_ok:
        status = "standby"
    elif node.control_type == "launchd":
        if loaded and pid:
            status = "healthy"
        elif loaded:
            status = "standby"
        else:
            status = "error"
    elif node.category == "placeholder":
        status = "standby"
    elif node.category == "logic":
        status = "healthy" if node.id == "north-star" else "standby"
    elif node.control_type == "none" and node.port is None:
        status = "standby"
    else:
        status = "error"

    # 共生体引擎：检测状态变化
    prev = _previous_node_states.get(node.id, "")
    if prev and prev != status:
        symbiote.node_health_change(node.id, prev, status)
    _previous_node_states[node.id] = status

    # 天
    if http_ok:
        tian = 1.0
    elif tcp_ok:
        tian = 0.75
    elif loaded and pid:
        tian = 0.85
    elif loaded:
        tian = 0.65
    elif node.category == "logic":
        tian = 0.85 if node.id in ("north-star", "symbiote-core") else 0.6
    elif node.control_type == "none" and node.port is None:
        tian = 0.5
    else:
        tian = 0.2

    # 地
    if pid:
        di = 1.0
    elif tcp_ok:
        di = 0.85
    elif loaded:
        di = 0.75
    elif node.category == "placeholder":
        di = 0.5
    elif node.category == "logic":
        di = 0.85 if node.id in ("north-star", "symbiote-core") else 0.6
    else:
        di = 0.2

    # 人
    if node.id in ("north-star", "symbiote-core"):
        ren = 1.0
    elif node.autostart:
        ren = 1.0
    elif node.control_type == "service":
        ren = 0.75
    elif node.control_type == "launchd":
        ren = 0.8
    elif node.category == "placeholder":
        ren = 0.45
    elif node.category == "logic":
        ren = 0.9
    else:
        ren = 0.5

    sancai = 0.3 * tian + 0.3 * di + 0.4 * ren
    dr_input = port if port else len(node.id)
    dr = digital_root(dr_input)

    formula = f"S = 0.3×{tian:.2f} + 0.3×{di:.2f} + 0.4×{ren:.2f} = {sancai:.3f}"

    return {
        "id": node.id,
        "name": node.name,
        "port": port,
        "category": node.category,
        "wuxing": node.wuxing,
        "status": status,
        "tcp_ok": tcp_ok,
        "http_ok": http_ok,
        "http_status": http_status,
        "latency_ms": http_latency if http_latency else tcp_latency,
        "pid": pid,
        "launchd_loaded": loaded,
        "launchd_label": node.launchd_label,
        "control_type": node.control_type,
        "autostart": node.autostart,
        "tian": round(tian, 3),
        "di": round(di, 3),
        "ren": round(ren, 3),
        "sancai": round(sancai, 3),
        "dr": dr,
        "formula": formula,
        "description": node.description,
        "dna": node.dna,
        "start_cmd": node.start_cmd,
        "stop_cmd": node.stop_cmd,
    }


def build_state() -> Dict[str, Any]:
    nodes = [compute_node_state(n) for n in ALL_NODES]
    healthy = sum(1 for n in nodes if n["status"] == "healthy")
    standby = sum(1 for n in nodes if n["status"] == "standby")
    error = sum(1 for n in nodes if n["status"] == "error")
    total = len(nodes)

    constitution_ok = all(
        n["status"] == "healthy"
        for n in nodes
        if n["id"] in ["north-star", "op-console", "brain-stem", "digital-id", "gua-audit", "symbiote-core"]
    )

    # 共生体健康补充：宪法层不通过时也判定共生体健康
    symbiote_health = symbiote._compute_health()

    # v1.1：加载脑神经引擎中已激活的DNA人格节点
    person_nodes = []
    if _NEURAL_READY and neural_engine:
        try:
            person_nodes = neural_engine.load_persons()
        except Exception:
            pass

    return {
        "dna": DNA,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "confirm_token": CONFIRM_TOKEN,
        "stats": {
            "total": total,
            "healthy": healthy,
            "standby": standby,
            "error": error,
            "health_rate": round(healthy / total * 100, 1) if total else 0,
            "constitution_ok": constitution_ok,
            "symbiote_health": symbiote_health,
            "person_nodes_count": len(person_nodes),
        },
        "nodes": nodes,
        "edges": EDGES,
        "symbiote": symbiote.get_symbiote_stats(),
        "knowledge_matrix": KNOWLEDGE_MATRIX,
        "kg_ready": kg_engine.ready,
        "neural": {
            "ready": _NEURAL_READY,
            "person_nodes": person_nodes,
        } if _NEURAL_READY else {"ready": False},
    }


# ═══════════════════════════════════════════════════════════════
# 六、控制接口
# ═══════════════════════════════════════════════════════════════

def execute_control(node_id: str, action: str) -> Dict[str, Any]:
    node = next((n for n in ALL_NODES if n.id == node_id), None)
    if not node:
        return {"ok": False, "error": "节点不存在"}
    if node.control_type == "none":
        return {"ok": False, "error": "该节点不可控"}

    try:
        if action == "start":
            if node.control_type == "launchd":
                cmd = ["launchctl", "start", node.launchd_label]
            elif node.start_cmd:
                cmd = node.start_cmd
            else:
                return {"ok": False, "error": "无启动命令"}
        elif action == "stop":
            if node.control_type == "launchd":
                cmd = ["launchctl", "stop", node.launchd_label]
            elif node.stop_cmd:
                cmd = node.stop_cmd
            elif node.port:
                pid = find_pid_by_port(node.port)
                if pid:
                    cmd = ["kill", "-TERM", str(pid)]
                else:
                    return {"ok": False, "error": "未找到进程"}
            else:
                return {"ok": False, "error": "无停止命令"}
        else:
            return {"ok": False, "error": "未知动作"}

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=str(ROOT))
        time.sleep(2)
        symbiote.record("control", {"node": node_id, "action": action, "rc": result.returncode})
        return {
            "ok": result.returncode == 0,
            "action": action,
            "node_id": node_id,
            "returncode": result.returncode,
            "stdout": result.stdout[-500:],
            "stderr": result.stderr[-500:],
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ═══════════════════════════════════════════════════════════════
# 七、HTTP 服务
# ═══════════════════════════════════════════════════════════════

HTML_PATH = ROOT / "web" / "longhun-neural-network-3d-v2.html"
SYMBIOTE_HTML_PATH = ROOT / "web" / "symbiote-dashboard.html"


class SymbioteHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _send_json(self, data: Dict[str, Any], code: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self):
        if HTML_PATH.exists():
            body = HTML_PATH.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self._send_json({"error": "HTML 文件不存在"}, 404)

    def _send_symbiote_html(self):
        if SYMBIOTE_HTML_PATH.exists():
            body = SYMBIOTE_HTML_PATH.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self._send_json({"error": "共生体仪表盘 HTML 不存在"}, 404)

    def _serve_static(self, rel_path: str):
        safe = unquote(rel_path).lstrip("/")
        if ".." in safe:
            self._send_json({"error": "Forbidden"}, 403)
            return
        target = ROOT / "web" / safe
        if not target.exists() or not target.is_file():
            self._send_json({"error": "Not found"}, 404)
            return
        content_type = "application/octet-stream"
        if safe.endswith(".js"):
            content_type = "application/javascript"
        elif safe.endswith(".html"):
            content_type = "text/html; charset=utf-8"
        elif safe.endswith(".css"):
            content_type = "text/css"
        body = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        # 共生体API记录
        symbiote.api_call(path)

        # ── 核心页面 ──
        if path in ["/", "/index.html"]:
            self._send_html()
        elif path == "/symbiote":
            self._send_symbiote_html()

        # ── 原有API ──
        elif path == "/api/state":
            self._send_json(build_state())
        elif path == "/api/status":
            state = build_state()
            self._send_json({
                "dna": state["dna"],
                "timestamp": state["timestamp"],
                "stats": state["stats"],
                "nodes": {n["id"]: n for n in state["nodes"]},
                "symbiote": state["symbiote"],
            })
        elif path == "/api/health":
            self._send_json({"ok": True, "dna": DNA, "port": PORT, "symbiote_core": SYMBIOTE_CORE})

        # ── 新增：共生体API ──
        elif path == "/api/symbiote":
            self._send_json({
                "core": SYMBIOTE_CORE,
                "stats": symbiote.get_symbiote_stats(),
                "knowledge_matrix": KNOWLEDGE_MATRIX,
                "kg_ready": kg_engine.ready,
                "neural_ready": _NEURAL_READY,
            })

        # ── 新增v1.1：脑神经API（DNA激活→神经生长）──
        elif path.startswith("/api/neural/"):
            qs = parse_qs(parsed.query)
            result = neural_api_handler(path, qs)
            if result is not None:
                self._send_json(result)
            else:
                self._send_json({"error": "未知的神经API端点"}, 404)

        elif path == "/api/symbiote/growth":
            self._send_json(symbiote.get_symbiote_stats())

        elif path == "/api/symbiote/manifesto":
            self._send_json(SYMBIOTE_CORE)

        # ── 新增：系统资源健康API ──
        elif path == "/api/symbiote/health-system":
            import psutil  # type: ignore[import-untyped]
            cpu = 0.0
            mem_total = 0
            mem_used = 0
            try:
                cpu = psutil.cpu_percent(interval=0.3)
                mem = psutil.virtual_memory()
                mem_total = mem.total
                mem_used = mem.used
            except Exception:
                pass
            import subprocess
            net_info = ""
            try:
                counts = subprocess.run(["lsof", "-iTCP", "-sTCP:LISTEN", "-P", "-n"],
                    capture_output=True, text=True, timeout=3)
                net_info = f"活跃监听端口: {len([l for l in counts.stdout.split(chr(10)) if l])-1}"
            except Exception:
                net_info = "不可用"
            self._send_json({
                "ok": True,
                "cpu_percent": cpu,
                "memory": {"total_mb": round(mem_total/1024/1024, 1), "used_mb": round(mem_used/1024/1024, 1)},
                "network": net_info,
                "pid": os.getpid(),
                "port": PORT,
                "dna": DNA,
            })

        # ── 新增：知识矩阵API ──
        elif path == "/api/knowledge-matrix":
            self._send_json(KNOWLEDGE_MATRIX)

        elif path == "/api/knowledge-matrix/luoshu":
            self._send_json(KNOWLEDGE_MATRIX["luoshu"])

        elif path == "/api/knowledge-matrix/wuxing":
            self._send_json(KNOWLEDGE_MATRIX["wuxing"])

        elif path == "/api/knowledge-matrix/sancai":
            self._send_json(KNOWLEDGE_MATRIX["sancai"])

        # ── 新增：知识图谱API ──
        elif path == "/api/kg/stats":
            self._send_json(kg_engine.stats())

        elif path == "/api/kg/search":
            qs = parse_qs(parsed.query)
            keyword = qs.get("q", [""])[0]
            limit = int(qs.get("limit", ["20"])[0])
            if not keyword:
                self._send_json({"error": "需要 q 参数"}, 400)
                return
            result = kg_engine.search(keyword, limit)
            symbiote.kg_query(keyword, result.get("total", 0))
            self._send_json(result)

        elif path == "/api/kg/node":
            qs = parse_qs(parsed.query)
            node_id = qs.get("id", [""])[0]
            if not node_id:
                self._send_json({"error": "需要 id 参数"}, 400)
                return
            self._send_json(kg_engine.get_node(node_id))

        elif path == "/api/kg/cross-ref":
            qs = parse_qs(parsed.query)
            node_id = qs.get("id", [""])[0]
            if not node_id:
                self._send_json({"error": "需要 id 参数"}, 400)
                return
            self._send_json(kg_engine.cross_reference(node_id))

        # ── 新增：数字根验证 ──
        elif path == "/api/verify/digital-root":
            qs = parse_qs(parsed.query)
            try:
                n = int(qs.get("n", ["0"])[0])
                self._send_json({"n": n, "dr": digital_root(n), "formula": f"dr({n}) = 1 + (({n} - 1) mod 9) = {digital_root(n)}"})
            except ValueError:
                self._send_json({"error": "n 必须是整数"}, 400)

        # ── 新增：网络全景视图 ──
        elif path == "/api/network-full":
            state = build_state()
            self._send_json({
                "dna": state["dna"],
                "timestamp": state["timestamp"],
                "stats": state["stats"],
                "nodes": state["nodes"],
                "edges": state["edges"],
                "symbiote": state["symbiote"],
                "knowledge_matrix": state["knowledge_matrix"],
                "kg_stats": kg_engine.stats() if kg_engine.ready else {"ready": False},
            })

        else:
            self._serve_static(path)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        symbiote.api_call(path)

        if path == "/api/control":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length).decode("utf-8")
                payload = json.loads(body)
                if payload.get("confirm") != CONFIRM_TOKEN:
                    self._send_json({"ok": False, "error": "确认码错误，操作被拒绝"}, 403)
                    return
                result = execute_control(payload.get("node_id", ""), payload.get("action", ""))
                self._send_json(result, 200 if result.get("ok") else 500)
            except Exception as e:
                self._send_json({"ok": False, "error": str(e)}, 500)

        elif path == "/api/symbiote/feed":
            """共生体投喂：外部知识注入"""
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length).decode("utf-8")
                payload = json.loads(body)
                detail = {
                    "source": payload.get("source", "external"),
                    "content_length": len(payload.get("content", "")),
                    "tags": payload.get("tags", []),
                }
                symbiote.record("symbiote_feed", detail)
                self._send_json({"ok": True, "dna": symbiote.growth_events[-1]["dna"] if symbiote.growth_events else DNA})
            except Exception as e:
                self._send_json({"ok": False, "error": str(e)}, 500)

        else:
            self._send_json({"error": "Not found"}, 404)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect(("127.0.0.1", PORT))
        print(f"🔴 端口 {PORT} 已被占用")
        sys.exit(1)
    except Exception:
        pass
    finally:
        s.close()

    server = HTTPServer(("127.0.0.1", PORT), SymbioteHandler)
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  🧬 龍魂共生体 · 知识矩阵+神经网络融合服务器          ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print(f"║  地址: http://127.0.0.1:{PORT}/                          ║")
    print(f"║  API:  http://127.0.0.1:{PORT}/api/state                ║")
    print(f"║  KG:   http://127.0.0.1:{PORT}/api/kg/search?q=龍魂     ║")
    print(f"║  矩阵: http://127.0.0.1:{PORT}/api/knowledge-matrix     ║")
    print(f"║  共生: http://127.0.0.1:{PORT}/api/symbiote             ║")
    print(f"║  脑神: http://127.0.0.1:{PORT}/api/neural/persons       ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print(f"║  知识图谱: {'🟢 ' + str(kg_engine.stats().get('node_count', 0)) + '节点' if kg_engine.ready else '🔴 未就绪'}                                   ║")
    if _NEURAL_READY and neural_engine:
        persons = neural_engine.load_persons()
        print(f"║  🧠 已激活DNA: {len(persons)} 个神经元                       ║")
    print(f"║  共生宣言: 共生体非代理人                                ║")
    print(f"║  DNA: {DNA}                                             ║")
    print("╚══════════════════════════════════════════════════════════╝")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 共生体服务器已停止")


if __name__ == "__main__":
    main()
