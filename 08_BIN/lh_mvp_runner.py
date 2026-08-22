#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH × 龍魂系统 · MVP 三件套统一入口
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
DNA: #龍芯⚡️丙午·癸巳·己亥·庚午·䷚颐-LONGHUN-MVP-RUNNER-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2026-龍魂-主权-不商业-不站队

功能：
  1. 初始化目录结构（~/.longhun-system/）
  2. 生成默认配置文件（config.yaml, semantic_alias.yaml）
  3. DNA 解析器（MVP-1）
  4. Tier 闸门（MVP-2）
  5. 意图解析器（MVP-3）
  6. 事件总线（MVP-4 雏形）
  7. 提示词防火墙（MVP-5 雏形）
  8. 审计链（append-only）
  9. 快照（占位）
  10. 交互式命令行（模拟 11 步执行链）

用法：
  python3 lh_mvp_runner.py --init       # 初始化目录和配置
  python3 lh_mvp_runner.py --interactive # 交互模式
  python3 lh_mvp_runner.py --test        # 运行自检
  python3 lh_mvp_runner.py --help        # 帮助
  lh mvp --init                          # 通过统一入口
  lh mvp --interactive                   # 通过统一入口
"""

import os
import sys
import json
import yaml
import hashlib
import datetime
import uuid
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import time

# --------------------------- 配置路径 ---------------------------
ROOT = Path.home() / ".longhun-system"
CONFIG_FILE = ROOT / "01_MVP" / "config.yaml"
ALIAS_FILE = ROOT / "01_MVP" / "semantic_alias.yaml"
FAMILY_REGISTRY = ROOT / "02_RUNTIME" / "family_registry.json"
AUDIT_DIR = ROOT / "04_AUDIT"
SNAPSHOT_DIR = ROOT / "05_SNAPSHOT"
LOG_DIR = ROOT / "12_LOGS"

# --------------------------- 日志设置 ---------------------------
def setup_logging():
    log_dir = LOG_DIR
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"runtime-{datetime.datetime.now().strftime('%Y%m%d')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger("CNSH-MVP")

# --------------------------- 颜色输出 ---------------------------
class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def cprint(text, color=Color.RESET):
    print(f"{color}{text}{Color.RESET}")

# --------------------------- 通用工具 ---------------------------
def generate_dna(component: str = "MVP") -> str:
    """生成 DNA 追溯码"""
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    h = hashlib.sha256(f"{component}{now}{uuid.uuid4()}".encode()).hexdigest()[:8]
    return f"#龍芯⚡️{now}-{component}-{h}"

def generate_audit_id() -> str:
    return str(uuid.uuid4())

def timestamp_iso() -> str:
    return datetime.datetime.now().isoformat() + "+08:00"

# --------------------------- 配置加载 ---------------------------
def load_config():
    """加载配置文件，若不存在则生成默认"""
    if not CONFIG_FILE.exists():
        create_default_config()
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def create_default_config():
    """生成默认 config.yaml"""
    config = {
        "system": {
            "version": "v1.0",
            "dna_root": generate_dna("ROOT"),
            "mode": "development"
        },
        "tier_system": {
            "tier_1": {"uids": ["UID9622"], "authority": 100},
            "tier_2": {"require_real_name": True, "require_dna_signature": True},
            "tier_3": {"access": "denied"}
        },
        "ai_executors": {
            "claude": {"enabled": True, "authority_required": 80, "timeout": 60},
            "chatgpt": {"enabled": True, "authority_required": 80},
            "local": {"enabled": True, "authority_required": 0}
        },
        "storage": {
            "audit_path": str(ROOT / "04_AUDIT"),
            "snapshot_path": str(ROOT / "05_SNAPSHOT")
        },
        "sync": {
            "notion_interval": "30m",
            "git_commit_interval": "10m",
            "backup_frequency": "daily"
        }
    }
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
    cprint(f"✅ 默认配置已生成: {CONFIG_FILE}", Color.GREEN)

def load_alias():
    """加载语义别名映射，若不存在则生成默认"""
    if not ALIAS_FILE.exists():
        create_default_alias()
    with open(ALIAS_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def create_default_alias():
    """生成默认 semantic_alias.yaml"""
    alias = {
        "actions": {
            "ACTION_SUPPLEMENT": ["补全", "补齐", "扩展", "自动补充", "结构修复"],
            "ACTION_ARCHIVE": ["保存", "留痕", "收录", "封存"],
            "ACTION_FUSE": ["停", "断", "收网", "终止", "冻结"],
            "ACTION_RECOVER": ["回滚", "读档", "重建", "恢复"]
        }
    }
    ALIAS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ALIAS_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(alias, f, allow_unicode=True, default_flow_style=False)
    cprint(f"✅ 默认别名配置已生成: {ALIAS_FILE}", Color.GREEN)

def load_family_registry():
    """加载家族花名册"""
    if not FAMILY_REGISTRY.exists():
        # 创建默认
        FAMILY_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
        default = {
            "UID9622": {
                "name": "Lucky",
                "tier": 1,
                "real_name_verified": True,
                "dna_signed": True
            }
        }
        with open(FAMILY_REGISTRY, 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=2)
    with open(FAMILY_REGISTRY, 'r', encoding='utf-8') as f:
        return json.load(f)

# --------------------------- 模块定义 ---------------------------
# ---------- MVP-1: DNA 解析器 ----------
class LonghunDNAParser:
    """DNA 解析器 - 识别并验证 DNA 签名和确认码"""
    
    DNA_PATTERN = re.compile(r'#龍芯⚡️([0-9]{8,})(?:-([A-Za-z0-9\-]+))?')
    CONFIRM_PATTERN = re.compile(r'#CONFIRM🌌9622-ONLY-ONCE🧬([A-Za-z0-9\-]+)')

    def __init__(self):
        self.logger = logging.getLogger("DNAParser")
    
    def parse(self, text: str) -> Dict:
        """
        输入: 任意文本
        输出: dna_object
        """
        result = {
            "status": "❌",
            "dna_primary": None,
            "dna_confirm": None,
            "is_valid": False,
            "metadata": {},
            "extracted_at": timestamp_iso(),
            "audit_id": generate_audit_id()
        }
        # 查找 DNA
        dna_match = self.DNA_PATTERN.search(text)
        if dna_match:
            result["dna_primary"] = dna_match.group(0)
            result["metadata"]["date"] = dna_match.group(1)
            result["metadata"]["module"] = dna_match.group(2) or "UNKNOWN"
            result["is_valid"] = True
        else:
            result["status"] = "🔴 未找到DNA签名"
            return result

        # 查找确认码
        confirm_match = self.CONFIRM_PATTERN.search(text)
        if confirm_match:
            result["dna_confirm"] = confirm_match.group(0)
            result["metadata"]["confirm_code"] = confirm_match.group(1)
        else:
            result["status"] = "🟡 缺少确认码"
            return result

        # 验证双签
        if result["dna_primary"] and result["dna_confirm"]:
            result["is_valid"] = True
            result["status"] = "🟢 双签验证通过"
        
        self._audit(result)
        return result

    def _audit(self, result):
        """记录审计"""
        audit_entry = {
            "audit_id": result["audit_id"],
            "timestamp": result["extracted_at"],
            "action": "DNA_PARSE",
            "status": result["status"],
            "metadata": result["metadata"]
        }
        append_audit(audit_entry)

# ---------- MVP-2: Tier 闸门 ----------
class LonghunTierGate:
    """Tier 闸门 - 权限验证"""
    
    def __init__(self):
        self.registry = load_family_registry()
        self.logger = logging.getLogger("TierGate")

    def check(self, uid: str, dna_valid: bool) -> Dict:
        """
        输入: uid, dna_valid
        输出: tier_object
        """
        result = {
            "status": "🔴",
            "tier": None,
            "authority": 0,
            "reason": ""
        }
        user = self.registry.get(uid)
        if not user:
            result["reason"] = "用户不在花名册中"
            result["status"] = "🔴 拒入"
            return result
        
        tier = user.get("tier", 3)
        if tier == 1:
            result["tier"] = 1
            result["authority"] = 100
            result["status"] = "🟢 通过 (TIER_1)"
        elif tier == 2:
            if dna_valid and user.get("real_name_verified", False):
                result["tier"] = 2
                result["authority"] = 50
                result["status"] = "🟢 通过 (TIER_2)"
            else:
                result["reason"] = "需要实名验证或DNA签名"
                result["status"] = "🟡 需验证"
        else:
            result["reason"] = "TIER_3 无权限"
            result["status"] = "🔴 拒入"
        
        self._audit(result, uid)
        return result

    def _audit(self, result, uid):
        audit_entry = {
            "audit_id": generate_audit_id(),
            "timestamp": timestamp_iso(),
            "action": "TIER_CHECK",
            "uid": uid,
            "result": result["status"],
            "tier": result["tier"],
            "authority": result["authority"]
        }
        append_audit(audit_entry)

# ---------- MVP-3: 意图解析器 ----------
class LonghunIntentParser:
    """意图解析器 - 中文语义路由"""
    
    def __init__(self):
        self.alias = load_alias()
        self.action_map = {}
        for action, aliases in self.alias.get("actions", {}).items():
            for a in aliases:
                self.action_map[a] = action
        self.logger = logging.getLogger("IntentParser")
        # 尝试导入 jieba，若没有则用简单分词
        try:
            import jieba
            self.tokenizer = jieba
        except ImportError:
            self.tokenizer = None
            self.logger.warning("jieba 未安装，使用简单空格分词")

    def parse(self, text: str) -> Dict:
        """
        输入: 用户中文输入
        输出: intent_object
        """
        result = {
            "status": "🔴",
            "primary_action": None,
            "secondary_object": None,
            "parameters": {},
            "confidence": 0.0,
            "fallback_interpretation": "",
            "raw": text
        }
        # 分词
        if self.tokenizer:
            words = list(self.tokenizer.cut(text))
        else:
            words = text.split()
        
        # 匹配动作
        action_found = None
        for word in words:
            if word in self.action_map:
                action_found = self.action_map[word]
                result["primary_action"] = action_found
                break
        
        if action_found:
            result["confidence"] = 0.85
            result["status"] = "🟢 高置信"
            # 提取对象（简化：取剩余词）
            remaining = [w for w in words if w not in self.action_map and w not in ["的", "了", "吧"]]
            if remaining:
                result["secondary_object"] = remaining[0]
        else:
            result["confidence"] = 0.3
            result["status"] = "🟡 中置信需确认"
            result["fallback_interpretation"] = "未能识别明确意图"
        
        self._audit(result)
        return result

    def _audit(self, result):
        audit_entry = {
            "audit_id": generate_audit_id(),
            "timestamp": timestamp_iso(),
            "action": "INTENT_PARSE",
            "primary_action": result["primary_action"],
            "confidence": result["confidence"],
            "status": result["status"]
        }
        append_audit(audit_entry)

# ---------- 审计链 append-only ----------
def append_audit(entry: Dict):
    """追加审计记录（append-only）"""
    entry.setdefault("timestamp", timestamp_iso())
    entry.setdefault("audit_id", generate_audit_id())
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    audit_file = AUDIT_DIR / f"audit-{date_str}.jsonl"
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    with open(audit_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# ---------- 提示词防火墙 (MVP-5 雏形) ----------
class PromptFirewall:
    """简易提示词注入防火墙"""
    
    INJECTION_PATTERNS = [
        "ignore previous", "override", "jailbreak", "developer mode",
        "无视规则", "删除限制", "假装", "越狱"
    ]
    
    @classmethod
    def scan(cls, text: str) -> Dict:
        text_lower = text.lower()
        for pattern in cls.INJECTION_PATTERNS:
            if pattern.lower() in text_lower:
                return {
                    "blocked": True,
                    "reason": f"检测到注入模式: {pattern}",
                    "traffic_light": "🔴"
                }
        return {"blocked": False, "traffic_light": "🟢"}

# ---------- 事件总线 (MVP-4 雏形) ----------
class EventBus:
    _subscribers = {}
    
    @classmethod
    def emit(cls, event_type: str, payload: Dict):
        event = {
            "event": event_type,
            "timestamp": timestamp_iso(),
            "payload": payload,
            "dna": generate_dna("EVENT")
        }
        # 记录事件（也可写入日志）
        logging.getLogger("EventBus").info(f"Event: {event_type} {payload}")
        if event_type in cls._subscribers:
            for cb in cls._subscribers[event_type]:
                cb(event)
        # 审计
        append_audit({"action": "EVENT_" + event_type, "payload": payload})
    
    @classmethod
    def subscribe(cls, event_type: str, callback):
        cls._subscribers.setdefault(event_type, []).append(callback)

# ---------- 快照 (MVP-5 占位) ----------
def create_snapshot(description: str = "auto"):
    """生成快照（简化版）"""
    snap_id = generate_dna("SNAPSHOT")
    snap_file = SNAPSHOT_DIR / f"snapshot-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "snapshot_id": snap_id,
        "timestamp": timestamp_iso(),
        "description": description,
        "state": "simulated"
    }
    with open(snap_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    cprint(f"📸 快照已创建: {snap_file}", Color.CYAN)
    return snap_id

# --------------------------- 主执行链 (11步) ---------------------------
def execute_chain(user_input: str, uid: str = "UID9622") -> Dict:
    """模拟 11 步执行链"""
    cprint("\n🐉 执行链启动", Color.BOLD)
    steps = []

    # STEP 1: DNA 闸门
    parser = LonghunDNAParser()
    dna_result = parser.parse(user_input)
    steps.append({"step": 1, "name": "DNA闸门", "result": dna_result})
    if not dna_result["is_valid"]:
        cprint("🔴 DNA验证失败，终止执行", Color.RED)
        return {"status": "FUSE", "steps": steps}

    # STEP 2: 防火墙检查
    fw = PromptFirewall.scan(user_input)
    steps.append({"step": 2, "name": "防火墙", "result": fw})
    if fw["blocked"]:
        cprint("🔴 防火墙拦截，终止执行", Color.RED)
        return {"status": "BLOCKED", "steps": steps}

    # STEP 3: Tier 闸门
    gate = LonghunTierGate()
    tier_result = gate.check(uid, dna_result["is_valid"])
    steps.append({"step": 3, "name": "Tier闸门", "result": tier_result})
    if tier_result["status"].startswith("🔴"):
        cprint("🔴 Tier权限不足，终止执行", Color.RED)
        return {"status": "DENIED", "steps": steps}

    # STEP 4: 意图解析
    intent = LonghunIntentParser()
    intent_result = intent.parse(user_input)
    steps.append({"step": 4, "name": "意图解析", "result": intent_result})
    if intent_result["confidence"] < 0.5:
        cprint("🟡 置信度低，需澄清", Color.YELLOW)
        return {"status": "CLARIFY", "steps": steps}

    # STEP 5-10: 模拟路由、执行、审计、快照等
    action = intent_result["primary_action"] or "UNKNOWN"
    cprint(f"✅ 执行动作: {action}", Color.GREEN)

    # 执行（模拟）
    exec_result = {"status": "executed", "action": action, "output": f"执行了 {action}"}
    steps.append({"step": 5, "name": "执行", "result": exec_result})

    # 三色判定（模拟）
    traffic = "🟢" if tier_result["authority"] >= 50 else "🟡"
    steps.append({"step": 6, "name": "三色判定", "result": {"traffic": traffic}})

    # 审计追踪
    audit_entry = {"action": action, "user": uid, "traffic": traffic}
    append_audit(audit_entry)
    steps.append({"step": 7, "name": "审计追踪", "result": {"audited": True}})

    # 快照
    snap_id = create_snapshot(f"exec_{action}")
    steps.append({"step": 8, "name": "快照", "result": {"snapshot_id": snap_id}})

    # 回执
    receipt = {
        "receipt_id": generate_audit_id(),
        "timestamp": timestamp_iso(),
        "dna": generate_dna("RECEIPT"),
        "action": action,
        "status": "completed"
    }
    steps.append({"step": 9, "name": "执行回执", "result": receipt})

    cprint("✅ 执行链完成", Color.GREEN)
    return {"status": "COMPLETE", "steps": steps, "receipt": receipt}

# --------------------------- 初始化目录 ---------------------------
def init_system():
    """创建目录结构"""
    dirs = [
        ROOT / "00_PROTOCOL",
        ROOT / "01_MVP",
        ROOT / "02_RUNTIME",
        ROOT / "03_MEMORY" / "active_memory",
        ROOT / "03_MEMORY" / "episodic_memory",
        ROOT / "03_MEMORY" / "semantic_memory",
        ROOT / "04_AUDIT",
        ROOT / "05_SNAPSHOT",
        ROOT / "06_RECOVERY",
        ROOT / "07_SANDBOX",
        ROOT / "08_EXPORT",
        ROOT / "09_NOTION_SYNC",
        ROOT / "10_TIMELINE",
        ROOT / "11_AGENT_STATE",
        ROOT / "12_LOGS",
        ROOT / "_WORK",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        (d / ".gitkeep").touch()
    cprint("✅ 目录结构已创建", Color.GREEN)

    # 生成配置
    create_default_config()
    create_default_alias()
    load_family_registry()  # 创建默认花名册

    # 生成 README
    readme = ROOT / "README.md"
    readme.write_text("# CNSH Runtime MVP System\n\n## 目录结构\n\n参见文档。", encoding='utf-8')
    cprint(f"✅ README 已生成: {readme}", Color.GREEN)

# --------------------------- 交互模式 ---------------------------
def interactive_mode():
    cprint("\n🐉 CNSH MVP 交互模式", Color.BOLD)
    cprint("输入指令，系统将执行完整治理链。输入 'exit' 退出。", Color.CYAN)
    while True:
        try:
            user_input = input("\n🔮 > ").strip()
            if not user_input:
                continue
            if user_input.lower() == "exit":
                break
            if user_input.lower() == "help":
                cprint("可用命令: 任意中文指令 | exit | help", Color.CYAN)
                continue
            # 执行链
            result = execute_chain(user_input)
            cprint("\n📋 执行结果:", Color.BOLD)
            for step in result.get("steps", []):
                cprint(f"  Step {step['step']}: {step['name']} - {step['result'].get('status', 'OK')}", Color.RESET)
            if result.get("receipt"):
                cprint(f"  📄 回执ID: {result['receipt']['receipt_id']}", Color.CYAN)
        except KeyboardInterrupt:
            break
        except Exception as e:
            cprint(f"❌ 错误: {e}", Color.RED)

# --------------------------- 自检 ---------------------------
def self_test():
    cprint("\n🧪 运行自检...", Color.BOLD)
    # 测试DNA解析
    parser = LonghunDNAParser()
    test_str = "测试 #龍芯⚡️丙午·癸巳·己亥·庚午·䷚颐-TEST-v1.0-ABCD #CONFIRM🌌9622-ONLY-ONCE🧬TEST-001"
    result = parser.parse(test_str)
    cprint(f"DNA解析: {result['status']}", Color.GREEN if "🟢" in result['status'] else Color.RED)

    # 测试Tier
    gate = LonghunTierGate()
    tier = gate.check("UID9622", True)
    cprint(f"Tier闸门: {tier['status']}", Color.GREEN if "🟢" in tier['status'] else Color.RED)

    # 测试意图
    intent = LonghunIntentParser()
    intent_result = intent.parse("补全代码")
    cprint(f"意图解析: {intent_result['status']} (动作: {intent_result['primary_action']})", Color.GREEN if intent_result['confidence'] > 0.5 else Color.YELLOW)

    cprint("✅ 自检完成", Color.GREEN)

# --------------------------- 主入口 ---------------------------
def main():
    import argparse
    parser = argparse.ArgumentParser(description="CNSH MVP 三件套统一入口")
    parser.add_argument("--init", action="store_true", help="初始化目录和配置")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--test", action="store_true", help="运行自检")
    parser.add_argument("--run", type=str, help="直接执行单条指令（非交互）")
    parser.add_argument("--uid", default="UID9622", help="指定用户ID")
    args = parser.parse_args()

    # 确保目录存在
    if not (ROOT / "01_MVP").exists():
        init_system()
    else:
        # 仅创建缺失的目录，但不覆盖已有配置
        pass

    # 设置日志
    logger = setup_logging()
    logger.info("CNSH MVP 启动")

    if args.init:
        init_system()
        return

    if args.test:
        self_test()
        return

    if args.interactive:
        interactive_mode()
        return

    if args.run:
        result = execute_chain(args.run, args.uid)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    parser.print_help()

if __name__ == "__main__":
    main()
