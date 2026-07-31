# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 龍魂神经网络路由 · 实时状态总控

后端代理：聚合 longhun-system 所有节点的真实健康状态、PID、响应时间，
并暴露 start/stop 控制接口，供 3D 神经网络页面实时渲染。

DNA: #龍芯⚡️2026-07-05-LONGHUN-NEURAL-NETWORK-SERVER-v2.0
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote

HOME = Path.home()
ROOT = HOME / "longhun-system"
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

DNA = "#龍芯⚡️2026-07-05-LONGHUN-NEURAL-NETWORK-SERVER-v2.0"
CONFIRM_TOKEN = "CONFIRM🌌9622-ONLY-ONCE"
PORT = 9627


# ============================================================
# 一、节点注册表（不动点 + 核心服务 + 外部接口 + 守护进程 + 逻辑层）
# ============================================================

@dataclass
class NodeDef:
    id: str
    name: str
    port: Optional[int]
    category: str
    wuxing: str
    health_path: str = "/"
    control_type: str = "none"          # service | launchd | none
    start_cmd: List[str] = field(default_factory=list)
    stop_cmd: List[str] = field(default_factory=list)
    launchd_label: str = ""
    autostart: bool = False
    description: str = ""
    dna: str = ""


# 核心服务注册表（端口、健康路径、启动命令）
SERVICE_REGISTRY: List[NodeDef] = [
    NodeDef(
        id="op-console",
        name="龍魂操作台",
        port=9622,
        category="core",
        wuxing="earth",
        health_path="/longhun_hub.html",
        control_type="service",
        start_cmd=["bash", str(ROOT / "tools" / "补全服务.sh")],
        autostart=True,
        description="龍魂系统统一入口与总控台，承载所有子系统的调度与展示。",
        dna="#龍芯⚡️2026-06-22-LONGHUN-OPCONSOLE-v1.0",
    ),
    NodeDef(
        id="brain-stem",
        name="龍魂脑干",
        port=9625,
        category="core",
        wuxing="water",
        health_path="/health",
        control_type="service",
        start_cmd=["python3", str(ROOT / "bin" / "longhun-launcher.py"), "start"],
        stop_cmd=["python3", str(ROOT / "bin" / "longhun-launcher.py"), "stop"],
        autostart=True,
        description="核心协调与决策中枢，连接天地人三层。",
        dna="#龍芯⚡️2026-06-22-LONGHUN-BRAINSTEM-v1.0",
    ),
    NodeDef(
        id="digital-id",
        name="数字身份入口",
        port=8444,
        category="core",
        wuxing="metal",
        health_path="/api/info",
        control_type="service",
        start_cmd=["python3", str(ROOT / "bin" / "longhun-launcher.py"), "start"],
        description="国家数字身份认证入口，主权级身份校验。",
        dna="#龍芯⚡️2026-06-22-LONGHUN-DIGITALID-v1.0",
    ),
    NodeDef(
        id="persona-api",
        name="人格 API",
        port=9001,
        category="core",
        wuxing="wood",
        health_path="/docs",
        control_type="service",
        start_cmd=["bash", str(ROOT / "bin" / "start_persona_api.sh")],
        description="五大人格实体的统一 API 路由与调度。",
        dna="#龍芯⚡️2026-06-22-LONGHUN-PERSONA-API-v1.0",
    ),
    NodeDef(
        id="phase3",
        name="Phase3 后端",
        port=8001,
        category="core",
        wuxing="earth",
        health_path="/api/v1/health",
        control_type="service",
        start_cmd=["bash", str(HOME / ".龍魂" / "services" / "service-manager.sh"), "start", "phase3"],
        stop_cmd=["bash", str(HOME / ".龍魂" / "services" / "service-manager.sh"), "stop", "phase3"],
        description="龍魂第三阶段业务后端。",
        dna="#龍芯⚡️2026-06-22-LONGHUN-PHASE3-v1.0",
    ),
    NodeDef(
        id="baby-guard",
        name="宝宝守护",
        port=8002,
        category="core",
        wuxing="fire",
        health_path="/health",
        control_type="service",
        start_cmd=["bash", str(HOME / ".龍魂" / "services" / "service-manager.sh"), "start", "baobao"],
        stop_cmd=["bash", str(HOME / ".龍魂" / "services" / "service-manager.sh"), "stop", "baobao"],
        description="系统守护与人格代理的稳定运行保障。",
        dna="#龍芯⚡️2026-06-22-LONGHUN-BABYGUARD-v1.0",
    ),
    NodeDef(
        id="gua-audit",
        name="卦象审计",
        port=9623,
        category="core",
        wuxing="earth",
        health_path="/health",
        control_type="launchd",
        launchd_label="com.longhun.gua-audit",
        autostart=True,
        description="三才卦象实时审计与决策评分。",
        dna="#龍芯⚡️2026-06-22-LONGHUN-GUAAUDIT-v1.0",
    ),
    NodeDef(
        id="heart-voice",
        name="龍心之语",
        port=9624,
        category="core",
        wuxing="fire",
        health_path="/health",
        control_type="launchd",
        launchd_label="com.longhun.heart-talk",
        autostart=True,
        description="情感化交互与语音合成服务。",
        dna="#龍芯⚡️2026-06-22-LONGHUN-HEARTVOICE-v1.0",
    ),
    NodeDef(
        id="knowledge-graph",
        name="知识图谱",
        port=8088,
        category="core",
        wuxing="wood",
        health_path="/api/health",
        control_type="launchd",
        launchd_label="com.longhun.kg-api",
        autostart=True,
        description="龍魂知识体系与实体关系图谱服务。",
        dna="#龍芯⚡️2026-06-22-LONGHUN-KG-v1.0",
    ),
    NodeDef(
        id="ability-site",
        name="能力官网",
        port=8844,
        category="core",
        wuxing="metal",
        health_path="/api/registry",
        control_type="launchd",
        launchd_label="com.longhun.capability-web",
        autostart=True,
        description="对外能力展示与官方门户。",
        dna="#龍芯⚡️2026-06-22-LONGHUN-ABILITY-SITE-v1.0",
    ),
    NodeDef(
        id="experience-portal",
        name="体验门户",
        port=8445,
        category="core",
        wuxing="water",
        health_path="/api/health",
        control_type="launchd",
        launchd_label="com.longhun.portal",
        autostart=True,
        description="用户体验入口与演示环境。",
        dna="#龍芯⚡️2026-06-22-LONGHUN-EXPERIENCE-v1.0",
    ),
    NodeDef(
        id="ollama",
        name="Ollama 本地模型",
        port=11434,
        category="external",
        wuxing="wood",
        health_path="/api/tags",
        control_type="none",
        description="本地大模型推理服务，数据不出境。",
        dna="#龍芯⚡️2026-06-22-LONGHUN-OLLAMA-v1.0",
    ),
    NodeDef(
        id="deepseek-bridge",
        name="DeepSeek Bridge (M266)",
        port=8788,
        category="external",
        wuxing="water",
        health_path="/health",
        control_type="service",
        start_cmd=["bash", str(ROOT / "bridges" / "启动-deepseek-bridge.sh"), "start"],
        stop_cmd=["bash", str(ROOT / "bridges" / "启动-deepseek-bridge.sh"), "stop"],
        description="DeepSeek 跨域桥接，外部输入隔离审查。",
        dna="#龍芯⚡️2026-06-22-LONGHUN-DEEPSEEKBRIDGE-v1.0",
    ),
    NodeDef(
        id="cnsh-gateway",
        name="CNSH 外接/外调 API 网关",
        port=9626,
        category="placeholder",
        wuxing="metal",
        health_path="/cnshex/health",
        control_type="service",
        start_cmd=["python3", str(HOME / ".longhun" / "multi-ai-gateway" / "cnshex_api.py")],
        description="CNSH 对外 API 网关占位，待开发。",
        dna="#龍芯⚡️2026-06-22-LONGHUN-CNSHGW-v0.1",
    ),
]

# 守护进程注册表（launchd / 逻辑）
DAEMON_REGISTRY: List[NodeDef] = [
    NodeDef(id="d-autostart", name="uid9622 统一自启", port=None, category="daemon", wuxing="earth",
            control_type="launchd", launchd_label="com.uid9622.longhun.autostart", autostart=True,
            description="开机自启动任务统一调度。", dna="#龍芯⚡️2026-06-22-LONGHUN-AUTOSTART-v1.0"),
    NodeDef(id="d-memory", name="记忆启动守护", port=None, category="daemon", wuxing="water",
            control_type="launchd", launchd_label="com.longhun.memory-bootstrap", autostart=True,
            description="多平台记忆归集与启动加载。", dna="#龍芯⚡️2026-06-22-LONGHUN-MEMORY-DAEMON-v1.0"),
    NodeDef(id="d-index", name="全局索引", port=None, category="daemon", wuxing="metal",
            control_type="launchd", launchd_label="com.longhun.global-index", autostart=True,
            description="文件、技能、资产全局索引构建。", dna="#龍芯⚡️2026-06-22-LONGHUN-INDEX-v1.0"),
    NodeDef(id="d-cnsh-redline", name="CNSH 红线", port=None, category="daemon", wuxing="fire",
            control_type="launchd", launchd_label="com.longhun.cnsh-redlines", autostart=True,
            description="CNSH 语言规范与行为红线守护。", dna="#龍芯⚡️2026-06-22-LONGHUN-CNSH-REDLINE-v1.0"),
    NodeDef(id="d-ability-guard", name="能力守护", port=None, category="daemon", wuxing="metal",
            control_type="launchd", launchd_label="com.longhun.capability-daemon", autostart=True,
            description="能力模块健康检查与自动恢复。", dna="#龍芯⚡️2026-06-22-LONGHUN-ABILITY-GUARD-v1.0"),
    NodeDef(id="d-harvester", name="收割机", port=None, category="daemon", wuxing="wood",
            control_type="launchd", launchd_label="com.longhun.harvester", autostart=True,
            description="代码与资产收割审计。", dna="#龍芯⚡️2026-06-22-LONGHUN-HARVESTER-v1.0"),
    NodeDef(id="d-daily-review", name="每日复盘", port=None, category="daemon", wuxing="earth",
            control_type="launchd", launchd_label="com.longhun.daily-review", autostart=True,
            description="每日自动化审计复盘。", dna="#龍芯⚡️2026-06-22-LONGHUN-DAILYREVIEW-v1.0"),
    NodeDef(id="d-auto-eval", name="自动化评估", port=None, category="daemon", wuxing="water",
            control_type="launchd", launchd_label="com.longhun.automation-assessment", autostart=True,
            description="系统健康六维度自动评估。", dna="#龍芯⚡️2026-06-22-LONGHUN-AUTOEVAL-v1.0"),
    NodeDef(id="d-entry-clean", name="入口清理", port=None, category="daemon", wuxing="metal",
            control_type="launchd", launchd_label="com.longhun.entry.cleanup", autostart=True,
            description="入口一致性协议自动清理。", dna="#龍芯⚡️2026-06-22-LONGHUN-ENTRYCLEAN-v1.0"),
    NodeDef(id="d-tianguan", name="天官判卷", port=None, category="daemon", wuxing="fire",
            control_type="launchd", launchd_label="com.longhun.marquee", autostart=True,
            description="自动化评审与权重判决。", dna="#龍芯⚡️2026-06-22-LONGHUN-TIANGUAN-v1.0"),
    NodeDef(id="d-notion-mirror", name="Notion 瀏覽器鏡像", port=None, category="daemon", wuxing="water",
            control_type="launchd", launchd_label="com.longhun.notion-mirror", autostart=True,
            description="Notion 公开空间本地镜像同步。", dna="#龍芯⚡️2026-06-22-LONGHUN-NOTIONMIRROR-v1.0"),
]

# 逻辑层节点（真实存在的能力/模块，未必是常驻进程）
LOGICAL_REGISTRY: List[NodeDef] = [
    NodeDef(id="north-star", name="北辰不动点", port=None, category="core", wuxing="earth",
            control_type="none",
            description="系统唯一不动点。UID9622 主权核心、三才算法宪法层 f(x)=x 的通过状态。",
            dna="#龍芯⚡️2026-07-04-SANCAI-PROTOCOL-UID9622-v1.0"),
    NodeDef(id="tricolor-engine", name="三色神机", port=None, category="logic", wuxing="fire",
            control_type="none",
            description="健康/待启/异常三色自动判定中枢。",
            dna="#龍芯⚡️2026-06-22-LONGHUN-TRICOLOR-v1.0"),
    NodeDef(id="wuxing-hub", name="五色石枢纽", port=None, category="logic", wuxing="earth",
            control_type="none",
            description="金木水火土五行相生相克路由调度。",
            dna="#龍芯⚡️2026-06-22-LONGHUN-WUXING-HUB-v1.0"),
    NodeDef(id="memory-feeder", name="记忆投喂器", port=None, category="logic", wuxing="water",
            control_type="none",
            description="多平台对话记忆压缩、归集、喂入训练池。",
            dna="#龍芯⚡️2026-06-22-LONGHUN-FEEDER-v1.0"),
    NodeDef(id="training-pool", name="龍魂训练池", port=None, category="logic", wuxing="wood",
            control_type="none",
            description="本地模型微调数据集与质量审计。",
            dna="#龍芯⚡️2026-06-22-LONGHUN-TRAINING-POOL-v1.0"),
    NodeDef(id="dna-chain", name="DNA 链哈希", port=None, category="logic", wuxing="metal",
            control_type="none",
            description="每个动作生成唯一 DNA 追溯码，链式哈希不可篡改。",
            dna="#龍芯⚡️2026-06-22-LONGHUN-DNA-CHAIN-v1.0"),
    NodeDef(id="governance-layer", name="龍魂治理层", port=None, category="logic", wuxing="earth",
            control_type="none",
            description="零号协议、三层监督、君子协议、行为熔断。",
            dna="#龍芯⚡️2026-06-29-SKILL-ROUTING-RULES-v1.0"),
    NodeDef(id="kirin-deploy", name="鲲鹏部署", port=None, category="logic", wuxing="metal",
            control_type="none",
            description="ARM64 鲲鹏服务器一键蓝绿部署。",
            dna="#龍芯⚡️2026-06-22-LONGHUN-KIRIN-DEPLOY-v1.0"),
    NodeDef(id="harmony-os", name="鸿蒙端", port=None, category="logic", wuxing="water",
            control_type="none",
            description="数据根留中国，SM4 端侧加密，RdbObserver 毫秒级监听。",
            dna="#龍芯⚡️2026-06-22-LONGHUN-HARMONYOS-v1.0"),
    NodeDef(id="ios-end", name="iOS 端", port=None, category="logic", wuxing="wood",
            control_type="none",
            description="CoreData 本地存储 + AES-256 端侧加密 + Secure Enclave。",
            dna="#龍芯⚡️2026-06-22-LONGHUN-IOS-v1.0"),
    NodeDef(id="cross-platform", name="跨平台同步", port=None, category="logic", wuxing="earth",
            control_type="none",
            description="iOS 与鸿蒙本地网络直连，国密 SM4 + ECDH，数据不出境。",
            dna="#龍芯⚡️2026-06-22-LONGHUN-XSYNC-v1.0"),
]

ALL_NODES: List[NodeDef] = [LOGICAL_REGISTRY[0]] + SERVICE_REGISTRY + DAEMON_REGISTRY + LOGICAL_REGISTRY[1:]

# 路由边：source -> target -> (type, label)
EDGES: List[Dict[str, str]] = [
    # 北辰不动点锚定
    {"source": "north-star", "target": "op-console", "type": "anchor", "label": "不动点锚定"},
    {"source": "north-star", "target": "brain-stem", "type": "anchor", "label": "不动点锚定"},
    {"source": "north-star", "target": "digital-id", "type": "anchor", "label": "不动点锚定"},
    {"source": "north-star", "target": "gua-audit", "type": "anchor", "label": "不动点锚定"},
    {"source": "north-star", "target": "governance-layer", "type": "anchor", "label": "宪法层锚定"},

    # 核心层互联
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

    # 外部接口
    {"source": "ollama", "target": "op-console", "type": "external", "label": "本地推理"},
    {"source": "deepseek-bridge", "target": "op-console", "type": "external", "label": "跨域输入"},
    {"source": "op-console", "target": "cnsh-gateway", "type": "data", "label": "API 网关"},
    {"source": "ollama", "target": "deepseek-bridge", "type": "external", "label": "模型互补"},

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


# ============================================================
# 二、探测与计算
# ============================================================

def digital_root(n: int) -> int:
    if n == 0:
        return 0
    return 1 + ((n - 1) % 9)


def probe_tcp(port: int, timeout: float = 1.5) -> Tuple[bool, float]:
    """TCP 端口连通性探测，返回 (ok, latency_ms)"""
    if port is None:
        return False, 0.0
    t0 = time.time()
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=timeout):
            return True, round((time.time() - t0) * 1000, 1)
    except Exception:
        return False, 0.0


def probe_http(port: int, path: str, timeout: float = 2.0) -> Tuple[bool, int, float]:
    """HTTP 健康检查，返回 (ok, status, latency_ms)"""
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
            capture_output=True,
            text=True,
            check=False,
            timeout=3,
        )
        if result.stdout.strip():
            return int(result.stdout.strip().split("\n")[0])
    except Exception:
        pass
    return None


def launchd_status(label: str) -> Tuple[bool, Optional[int]]:
    """检查 launchd 任务是否加载/运行，返回 (loaded, pid)"""
    if not label:
        return False, None
    try:
        result = subprocess.run(
            ["launchctl", "list", label],
            capture_output=True,
            text=True,
            check=False,
            timeout=3,
        )
        if result.returncode != 0:
            return False, None
        out = result.stdout
        # 尝试解析 PID
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
    """基于真实探测计算节点状态、三才指数、数字根、公式。"""
    port = node.port
    tcp_ok, tcp_latency = probe_tcp(port)
    http_ok, http_status, http_latency = probe_http(port, node.health_path)
    pid = find_pid_by_port(port) if port else None

    loaded = False
    launchd_pid = None
    if node.control_type == "launchd" and node.launchd_label:
        loaded, launchd_pid = launchd_status(node.launchd_label)
        if launchd_pid:
            pid = launchd_pid

    # 三色状态
    if node.id == "north-star":
        status = "healthy"
    elif http_ok:
        status = "healthy"
    elif tcp_ok:
        status = "standby"  # 端口通但 HTTP 不健康
    elif node.control_type == "launchd":
        # launchd 守护：有 PID 则健康，已加载则待启，未加载则异常
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

    # 天：HTTP 响应质量 / 服务可达性
    if http_ok:
        tian = 1.0
    elif tcp_ok:
        tian = 0.75
    elif loaded and pid:
        tian = 0.85
    elif loaded:
        tian = 0.65
    elif node.category == "logic":
        tian = 0.85 if node.id == "north-star" else 0.6
    elif node.control_type == "none" and node.port is None:
        tian = 0.5
    else:
        tian = 0.2

    # 地：进程/端口存在性
    if pid:
        di = 1.0
    elif tcp_ok:
        di = 0.85
    elif loaded:
        di = 0.75
    elif node.category == "placeholder":
        di = 0.5
    elif node.category == "logic":
        di = 0.85 if node.id == "north-star" else 0.6
    else:
        di = 0.2

    # 人：用户依赖与自启动配置
    if node.id == "north-star":
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

    #  constitutional layer check
    constitution_ok = all(
        n["status"] == "healthy" for n in nodes
        if n["id"] in ["north-star", "op-console", "brain-stem", "digital-id", "gua-audit"]
    )

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
        },
        "nodes": nodes,
        "edges": EDGES,
    }


# ============================================================
# 三、控制接口
# ============================================================

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

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(ROOT),
        )
        # 给服务一点启动/停止时间
        time.sleep(2)
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


# ============================================================
# 四、HTTP 服务
# ============================================================

HTML_PATH = ROOT / "web" / "longhun-neural-network-3d-v2.html"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # 静默日志，减少噪音
        pass

    def _send_json(self, data: Dict, code: int = 200):
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

    def _serve_static(self, rel_path: str):
        """从 web 目录提供静态资源（three.js 等）。"""
        safe = unquote(rel_path).lstrip("/")
        # 禁止越界
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
        if path in ["/", "/index.html"]:
            self._send_html()
        elif path.startswith("/api/"):
            if path == "/api/state":
                self._send_json(build_state())
            elif path == "/api/status":
                state = build_state()
                self._send_json({
                    "dna": state["dna"],
                    "timestamp": state["timestamp"],
                    "stats": state["stats"],
                    "nodes": {n["id"]: n for n in state["nodes"]},
                })
            elif path == "/api/health":
                self._send_json({"ok": True, "dna": DNA, "port": PORT})
            else:
                self._send_json({"error": "Not found"}, 404)
        else:
            # 静态资源：three.js / 本地库 / assets 等
            self._serve_static(path)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/control":
            self._send_json({"error": "Not found"}, 404)
            return
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


def main():
    # 检查端口占用
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect(("127.0.0.1", PORT))
        print(f"🔴 端口 {PORT} 已被占用，无法启动神经网络状态总控")
        sys.exit(1)
    except Exception:
        pass
    finally:
        s.close()

    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"🧠 龍魂神经网络路由 · 实时状态总控已启动")
    print(f"   地址: http://127.0.0.1:{PORT}/")
    print(f"   API : http://127.0.0.1:{PORT}/api/state")
    print(f"   DNA : {DNA}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 神经网络状态总控已停止")


if __name__ == "__main__":
    main()
