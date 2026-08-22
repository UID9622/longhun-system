#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 核心引擎
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CNSH-CORE-UID9622
"""

import os
import sys
import json
import hashlib
import time
import re
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum

# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ============================================================
# 路径配置
# ============================================================

HOME = Path.home()
LONGHUN_HOME = HOME / ".longhun"
CNSH_HOME = LONGHUN_HOME / "cnsh_suite"
CNSH_HOME.mkdir(parents=True, exist_ok=True)

LOG_DIR = LONGHUN_HOME / "12_LOGS"
AUDIT_DIR = LONGHUN_HOME / "04_AUDIT"
STATE_DIR = LONGHUN_HOME / "08_STATE"

for d in [LOG_DIR, AUDIT_DIR, STATE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ============================================================
# 日志
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"cnsh_suite_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("cnsh_suite")

# ============================================================
# 错误码
# ============================================================

class CNSHErrorCode(Enum):
    DNA_GENERATION_FAILED = 1001
    DNA_INVALID_FORMAT = 1002
    DNA_VERIFICATION_FAILED = 1003
    DNA_PARENT_NOT_FOUND = 1004
    AUDIT_SCORE_TOO_LOW = 1101
    AUDIT_CONTENT_EMPTY = 1102
    AUDIT_ENGINE_UNAVAILABLE = 1199
    CNSH_SYNTAX_ERROR = 1201
    CNSH_RUNTIME_ERROR = 1202
    CNSH_TIMEOUT = 1203
    CNSH_FILE_NOT_FOUND = 1204
    CNSH_SANDBOX_VIOLATION = 1205
    HISTORIAN_WRITE_FAILED = 1301
    HISTORIAN_READ_FAILED = 1302
    PERSONA_NOT_FOUND = 1401
    PERSONA_ROUTE_FAILED = 1402
    PLUGIN_LOAD_FAILED = 1501
    CONFIG_INVALID = 1502
    ENGINE_UNAVAILABLE = 1503

class CNSHError(Exception):
    def __init__(self, code: CNSHErrorCode, message: str, details: Dict = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(f"[{code.value}] {message}")

# ============================================================
# 工具函数
# ============================================================

def generate_dna(suffix: str = "CNSH") -> str:
    """生成DNA追溯码"""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    rand = hashlib.sha256(f"{suffix}{timestamp}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{timestamp}-{suffix}-{rand}-UID{UID}"

def get_ganzhi(date: datetime = None) -> str:
    """获取天干地支（简化版）"""
    if date is None:
        date = datetime.now()
    tian_gan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
    di_zhi = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
    hexagrams = ["乾","坤","屯","蒙","需","讼","师","比","小畜","履","泰","否",
                 "同人","大有","谦","豫","随","蛊","临","观","噬嗑","贲","剥","复",
                 "无妄","大畜","颐","大过","坎","离","咸","恒","遁","大壮","晋",
                 "明夷","家人","睽","蹇","解","损","益","夬","姤","萃","升","困",
                 "井","革","鼎","震","艮","渐","归妹","丰","旅","巽","兑","涣",
                 "节","中孚","小过","既济","未济"]
    year_gan = tian_gan[(date.year - 4) % 10]
    year_zhi = di_zhi[(date.year - 4) % 12]
    hex = hexagrams[date.day % 64]
    hour_zhi = di_zhi[((date.hour + 1) // 2) % 12]
    return f"{year_gan}{year_zhi}·{hour_zhi}时·{hex}卦"

def write_historian(operation: str, dna: str, details: Dict):
    """写入史官"""
    record = {
        "timestamp": datetime.now().isoformat(),
        "operation": operation,
        "dna": dna,
        "details": details
    }
    audit_path = AUDIT_DIR / "cnsh_suite.jsonl"
    with open(audit_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def write_shame_wall(reason: str, dna: str, details: Dict):
    """写入耻辱墙"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "reason": reason,
        "dna": dna,
        "details": details,
        "severity": "HIGH"
    }
    shame_path = STATE_DIR / "shame_wall.jsonl"
    with open(shame_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# ============================================================
# 核心引擎
# ============================================================

class CNSHEngine:
    """CNSH 核心引擎"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._tools = {}
        self._hooks = {}
        self._events = {}
        self._agents = {}
        self._context = {}
        self._init_defaults()

    def _init_defaults(self):
        """初始化默认组件"""
        from .tools import DNAGenerator, TricolorAuditor, CNSHExecutor
        from .hooks import TricolorGate
        from .events import Historian
        from .agents import PersonaRouter

        self.register_tool(DNAGenerator())
        self.register_tool(TricolorAuditor())
        self.register_tool(CNSHExecutor())

        self.register_hook(TricolorGate())
        self.register_event(Historian())
        self.register_agent(PersonaRouter())

    def register_tool(self, tool: 'Tool'):
        """注册工具"""
        self._tools[tool.name] = tool
        logger.info(f"✅ 工具已注册: {tool.name}")

    def register_hook(self, hook: 'Hook'):
        """注册钩子"""
        self._hooks[hook.name] = hook
        logger.info(f"✅ 钩子已注册: {hook.name}")

    def register_event(self, event: 'Event'):
        """注册事件监听"""
        self._events[event.name] = event
        logger.info(f"✅ 事件监听已注册: {event.name}")

    def register_agent(self, agent: 'Agent'):
        """注册Agent"""
        self._agents[agent.name] = agent
        logger.info(f"✅ Agent已注册: {agent.name}")

    def get_tool(self, name: str) -> Optional['Tool']:
        return self._tools.get(name)

    def get_agent(self, name: str) -> Optional['Agent']:
        return self._agents.get(name)

    def execute_tool(self, name: str, **kwargs) -> Dict:
        """执行工具"""
        tool = self.get_tool(name)
        if not tool:
            raise CNSHError(CNSHErrorCode.PLUGIN_LOAD_FAILED, f"工具不存在: {name}")
        return tool.execute(**kwargs)

    def run_hook(self, name: str, context: Dict) -> Dict:
        """运行钩子"""
        hook = self._hooks.get(name)
        if not hook:
            return {"kind": "allow"}
        return hook.run(context)

    def emit_event(self, name: str, **kwargs):
        """触发事件"""
        event = self._events.get(name)
        if event:
            event.trigger(**kwargs)

    def get_status(self) -> Dict:
        """获取引擎状态"""
        return {
            "tools": list(self._tools.keys()),
            "hooks": list(self._hooks.keys()),
            "events": list(self._events.keys()),
            "agents": list(self._agents.keys()),
            "dna": generate_dna("STATUS")
        }

# ============================================================
# 基类
# ============================================================

class Tool:
    """工具基类"""
    name: str = "base_tool"
    description: str = "基础工具"
    parameters: Dict = {}

    def execute(self, **kwargs) -> Dict:
        raise NotImplementedError

class Hook:
    """钩子基类"""
    name: str = "base_hook"
    description: str = "基础钩子"
    priority: int = 0

    def run(self, context: Dict) -> Dict:
        raise NotImplementedError

class Event:
    """事件基类"""
    name: str = "base_event"
    description: str = "基础事件"

    def trigger(self, **kwargs):
        raise NotImplementedError

class Agent:
    """Agent基类"""
    name: str = "base_agent"
    description: str = "基础Agent"
    personas: List[Dict] = []

    def execute(self, input_text: str, session: Dict) -> Dict:
        raise NotImplementedError


# ============================================================
# CNSHSuite 主入口
# ============================================================

class CNSHSuite:
    """CNSH 套件主入口"""

    def __init__(self):
        self.engine = CNSHEngine()
        self.dna = generate_dna("SUITE-INIT")
        logger.info(f"🐉 CNSH 套件初始化完成: {self.dna}")

    def execute(self, command: str) -> Dict:
        """执行自然语言命令"""
        # 解析命令
        cmd_lower = command.lower()

        if "生成dna" in cmd_lower or "生成DNA" in command:
            content = command.replace("生成DNA:", "").replace("生成dna:", "").strip()
            if not content:
                content = command.replace("生成dna", "").replace("生成DNA", "").strip()
            return self.engine.execute_tool("dna_generator", content=content)

        elif "审计" in cmd_lower or "三色" in cmd_lower:
            content = command.replace("审计内容:", "").replace("三色审计:", "").strip()
            if not content:
                content = command.replace("审计", "").replace("三色", "").strip()
            return self.engine.execute_tool("tricolor_auditor", content=content)

        elif "运行cnsh" in cmd_lower or "执行cnsh" in cmd_lower:
            script = command.replace("运行CNSH:", "").replace("运行cnsh:", "").strip()
            if not script:
                script = command.replace("运行CNSH", "").replace("运行cnsh", "").strip()
            return self.engine.execute_tool("cnsh_executor", script=script)

        else:
            # 默认：Agent路由
            result = self.engine.execute_tool("persona_router", input_text=command)
            return result

    def get_status(self) -> Dict:
        return {
            "dna": self.dna,
            "engine": self.engine.get_status(),
            "timestamp": datetime.now().isoformat()
        }
