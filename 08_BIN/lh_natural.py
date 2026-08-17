#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 自然语言意图引擎 v1.0

你说人话，AI自动执行。
集成：通心译、主权网关、浏览器控制、剪贴板、史官审计。

DNA: #龍芯⚡️丙午·丙申·庚申·亥时-NATURAL-ENGINE-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
"""

import os
import sys
import json
import subprocess
import time
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# ============================================================
# 项目路径
# ============================================================
PROJECT_DIR = Path.home() / "longhun-system"
BIN_DIR = PROJECT_DIR / "bin"
STATE_DIR = PROJECT_DIR / "08_STATE"
AUDIT_DIR = PROJECT_DIR / "04_AUDIT"
LOGS_DIR = PROJECT_DIR / "logs"

# 通心译技能路径
TONGXINYI_SKILL = Path.home() / ".kimi-code" / "skills" / "longhun-tongxinyi"
TONGXINYI_CLI = TONGXINYI_SKILL / "scripts" / "tongxin_cli.py"

# 史官审计文件
AUDIT_FILE = AUDIT_DIR / "natural_engine.jsonl"

# ============================================================
# DNA 与签名
# ============================================================
UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
DNA_PREFIX = "#龍芯⚡️"


def generate_dna(suffix: str = "") -> str:
    ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    rand = hashlib.sha256(f"{suffix}{ts}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{ts}-{suffix}-{UID}-{rand}"


# ============================================================
# 史官审计
# ============================================================
def record_audit(operation: str, detail: Any, status: str = "ok"):
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "dna": generate_dna("NATURAL-ENGINE"),
        "operation": operation,
        "detail": detail,
        "status": status,
    }
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ============================================================
# 通用 shell 执行
# ============================================================
def run_shell(cmd: str, timeout: int = 30) -> Dict[str, Any]:
    """执行 shell 命令，返回结构化结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "cmd": cmd,
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout", "cmd": cmd}
    except Exception as e:
        return {"ok": False, "error": str(e), "cmd": cmd}


def run_python(script: Path, args: List[str] = None, timeout: int = 60) -> Dict[str, Any]:
    """执行 Python 脚本"""
    if not script.exists():
        return {"ok": False, "error": f"脚本不存在: {script}"}
    cmd_parts = ["python3", str(script)] + (args or [])
    return run_shell(" ".join(cmd_parts), timeout=timeout)


# ============================================================
# 通心译集成（先翻译再执行）
# ============================================================
def tongxinyi_translate(text: str) -> Optional[Dict[str, Any]]:
    """调用通心译技能解析人话意图；不可用时返回 None"""
    if not TONGXINYI_CLI.exists():
        return None
    result = run_python(TONGXINYI_CLI, ["translate", text], timeout=15)
    if not result["ok"]:
        return None
    try:
        # 尝试解析 JSON 输出
        lines = result["stdout"].strip().splitlines()
        for line in reversed(lines):
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                return json.loads(line)
        return {"raw": result["stdout"], "source": "tongxinyi"}
    except Exception:
        return {"raw": result["stdout"], "source": "tongxinyi"}


# ============================================================
# 意图解析器
# ============================================================
class IntentParser:
    """把你说的人话转成可执行任务（内置兜底 + 通心译增强）"""

    PATTERNS = {
        "deploy_gateway": {
            "keywords": ["部署网关", "启动网关", "网关跑起来", " sovereignty", "搞通网关", "搞通", "gateway deploy", "启动主权网关", "重启网关"],
            "desc": "部署/重启主权网关",
        },
        "check_gateway": {
            "keywords": ["网关状态", "史官", "gateway status", "链路", "小艺", "audit"],
            "desc": "检查网关与史官",
        },
        "clean_ports": {
            "keywords": ["清理", "清掉", "端口", "占着", "释放", "kill port", "杀进程"],
            "desc": "清理端口占用",
        },
        "check_status": {
            "keywords": ["状态", "活着", "还在", "运行", "进程", "看看", "system status", "check"],
            "desc": "查看系统状态",
        },
        "browser_open": {
            "keywords": ["打开浏览器", "开chrome", "打开chrome", "browser open", "启动浏览器"],
            "desc": "打开浏览器",
        },
        "browser_close": {
            "keywords": ["关浏览器", "关闭chrome", "停浏览器", "browser close", "关掉浏览器"],
            "desc": "关闭浏览器",
        },
        "clipboard_status": {
            "keywords": ["剪贴板", "clipboard", "粘贴板"],
            "desc": "检查剪贴板服务",
        },
        "memory_check": {
            "keywords": ["记忆", "memory", "我的记忆", "回忆"],
            "desc": "检查记忆文件",
        },
        "help": {
            "keywords": ["帮助", "help", "怎么用", "能做什么"],
            "desc": "显示帮助",
        },
    }

    @classmethod
    def parse(cls, text: str) -> List[str]:
        text_lower = text.lower()
        tasks = []
        for task, cfg in cls.PATTERNS.items():
            for kw in cfg["keywords"]:
                if kw.lower() in text_lower:
                    tasks.append(task)
                    break
        return tasks


# ============================================================
# 任务执行器
# ============================================================
class TaskExecutor:
    """执行自然语言意图解析出来的任务"""

    # ---------- 网关相关 ----------
    @staticmethod
    def deploy_gateway():
        print("\n🚀 [部署网关] 执行 deploy_sovereign_gateway.sh ...")
        script = PROJECT_DIR / "deploy_sovereign_gateway.sh"
        if not script.exists():
            print("   ❌ 未找到 deploy_sovereign_gateway.sh")
            record_audit("deploy_gateway", {"error": "script_missing"}, "fail")
            return
        result = run_shell(f"bash {script}", timeout=120)
        print(result["stdout"])
        if result["stderr"]:
            print(result["stderr"])
        record_audit("deploy_gateway", {"ok": result["ok"]}, "ok" if result["ok"] else "fail")

    @staticmethod
    def check_gateway():
        print("\n📋 [网关+史官] 检查链路状态...")

        # 史官记录
        audit_path = AUDIT_DIR / "gateway_audit.jsonl"
        if audit_path.exists():
            lines = []
            with open(audit_path, "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip()]
            recent = lines[-10:] if len(lines) > 10 else lines
            print(f"✅ 网关史官记录: 共 {len(lines)} 条，最近 {len(recent)} 条")
            for line in recent:
                try:
                    data = json.loads(line)
                    ts = data.get("timestamp", "")[:19]
                    action = data.get("action", data.get("path", "操作"))
                    print(f"   - {ts} | {action}")
                except Exception:
                    pass
        else:
            print("⚠️ 网关史官记录暂未生成")

        # 自然语言引擎自身史官
        if AUDIT_FILE.exists():
            lines = []
            with open(AUDIT_FILE, "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip()]
            print(f"✅ 自然语言引擎史官: 共 {len(lines)} 条记录")
        else:
            print("⚠️ 自然语言引擎史官记录暂未生成")

        # 网关端口
        result = run_shell("lsof -i :8766")
        if result["stdout"]:
            print("✅ 主权网关(:8766) 正在运行")
            for line in result["stdout"].splitlines()[1:2]:
                print(f"   {line}")
        else:
            print("❌ 主权网关(:8766) 未运行")

        # 浏览器端口
        result = run_shell("lsof -i :9766")
        if result["stdout"]:
            print("✅ 浏览器服务(:9766) 正在运行")
        else:
            print("⚠️ 浏览器服务(:9766) 未运行")

        # Chrome 进程
        result = run_shell("pgrep -f 'Chrome' | head -3")
        if result["stdout"]:
            print(f"✅ Chrome 进程: {result['stdout'].replace(chr(10), ', ')}")
        else:
            print("⚠️ Chrome 未启动")

        record_audit("check_gateway", {"port_8766": bool(result["stdout"])}, "ok")

    # ---------- 端口清理 ----------
    @staticmethod
    def clean_ports():
        print("\n🧹 [清理] 释放端口...")
        freed = []
        for port in [8766, 8768, 9766]:
            # 先查出占用进程
            pid_result = run_shell(f"lsof -ti :{port}")
            if pid_result["stdout"]:
                pids = pid_result["stdout"].split()
                print(f"   端口 {port} 被 PID {', '.join(pids)} 占用")
                kill_result = run_shell(f"kill -9 {' '.join(pids)} 2>/dev/null || true")
                time.sleep(0.5)
                # 验证
                verify = run_shell(f"lsof -ti :{port}")
                if not verify["stdout"]:
                    freed.append(port)
                    print(f"   ✅ 端口 {port} 已释放")
                else:
                    print(f"   ❌ 端口 {port} 仍被占用")
            else:
                print(f"   ✅ 端口 {port} 空闲")
                freed.append(port)
        record_audit("clean_ports", {"freed": freed}, "ok")

    # ---------- 浏览器 ----------
    @staticmethod
    def browser_open():
        print("\n🌐 [打开浏览器] ...")
        script = BIN_DIR / "lh_browser_controller.py"
        if script.exists():
            result = run_python(script, ["open"], timeout=30)
            print(result["stdout"] or result["stderr"])
        else:
            print("   使用系统默认方式打开 Chrome")
            run_shell("open -a 'Google Chrome' --args --remote-debugging-port=9222")
        record_audit("browser_open", {}, "ok")

    @staticmethod
    def browser_close():
        print("\n🚫 [关闭浏览器] ...")
        script = BIN_DIR / "lh_browser_controller.py"
        if script.exists():
            result = run_python(script, ["close"], timeout=30)
            print(result["stdout"] or result["stderr"])
        else:
            run_shell("pkill -f 'Google Chrome' 2>/dev/null || true")
            run_shell("pkill -f 'playwright' 2>/dev/null || true")
            print("   ✅ 浏览器实例已停止")
        record_audit("browser_close", {}, "ok")

    # ---------- 剪贴板 ----------
    @staticmethod
    def clipboard_status():
        print("\n📋 [剪贴板服务] ...")
        script = BIN_DIR / "lh_clipboard_agent.py"
        if script.exists():
            result = run_python(script, ["status"], timeout=15)
            print(result["stdout"] or result["stderr"])
        else:
            print("   ⚠️ 未找到 lh_clipboard_agent.py")
        record_audit("clipboard_status", {}, "ok")

    # ---------- 记忆 ----------
    @staticmethod
    def memory_check():
        print("\n🧠 [记忆文件] ...")
        mem_path = Path.home() / ".longhun" / "memory" / "latest_digest.json"
        if mem_path.exists():
            with open(mem_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"✅ 记忆文件存在: {mem_path}")
            print(f"   DNA: {data.get('dna', 'N/A')}")
            print(f"   摘要: {data.get('digest', 'N/A')}")
            print(f"   时间: {data.get('timestamp', 'N/A')}")
        else:
            print("⚠️ 记忆文件不存在")
            # 自动生成一个
            bootstrap = PROJECT_DIR / "08_BIN" / "lh_memory_bootstrap.py"
            if bootstrap.exists():
                print("   尝试运行记忆启动器...")
                run_python(bootstrap, timeout=30)
        record_audit("memory_check", {"exists": mem_path.exists()}, "ok")

    # ---------- 系统状态 ----------
    @staticmethod
    def check_status():
        print("\n📊 [系统状态] ...")

        # 关键进程
        procs = [
            ("主权网关", "lh_sovereign_gateway.py", 8766),
            ("浏览器服务", "lh_browser_gateway.py", 9766),
            ("剪贴板中枢", "lh_clipboard_hub.py", None),
        ]
        for name, pattern, port in procs:
            result = run_shell(f"pgrep -f '{pattern}' | head -1")
            if result["stdout"]:
                print(f"   ✅ {name}: PID {result['stdout'].strip()}")
            else:
                print(f"   ⚠️ {name}: 未运行")

        # 关键目录
        for d in [STATE_DIR, AUDIT_DIR, LOGS_DIR]:
            print(f"   📁 {d.name}: {'存在' if d.exists() else '不存在'}")

        record_audit("check_status", {}, "ok")

    # ---------- 帮助 ----------
    @staticmethod
    def help():
        print("\n💡 你可以这样说：")
        print("   • 帮我把网关和小艺链路搞通，史官记录我要看一眼")
        print("   • 清理端口，把占着的服务释放掉")
        print("   • 打开浏览器 / 关闭浏览器")
        print("   • 看看剪贴板 / 我的记忆呢")
        print("   • 系统状态怎么样")


# ============================================================
# 自然语言主引擎
# ============================================================
class NaturalEngine:
    """自然语言意图引擎 - 你说人话，我干活"""

    def __init__(self):
        self.parser = IntentParser()
        self.executor = TaskExecutor()

    def understand(self, user_input: str) -> Dict[str, Any]:
        """理解人话：先通心译，再内置解析"""
        tx_result = tongxinyi_translate(user_input)
        built_in_tasks = self.parser.parse(user_input)

        # 如果通心译成功且给出了意图，合并使用
        tx_tasks = []
        if tx_result and isinstance(tx_result, dict):
            intent = tx_result.get("intent") or tx_result.get("骨架", {}).get("动作")
            if intent:
                tx_tasks.append(intent)

        # 去重合并：以内置为主，通心译为补充
        tasks = list(dict.fromkeys(built_in_tasks + tx_tasks))

        return {
            "raw": user_input,
            "tongxinyi": tx_result,
            "tasks": tasks if tasks else ["check_status"],
        }

    def run(self, user_input: str) -> str:
        print("\n" + "=" * 60)
        print("🐉 龍魂 · 自然语言意图引擎")
        print("=" * 60)

        understood = self.understand(user_input)
        tasks = understood["tasks"]

        print(f"💬 你说：{user_input}")
        if understood["tongxinyi"]:
            print("🧠 通心译已参与解析")
        print(f"📝 识别任务: {', '.join(tasks)}")
        print("-" * 60)

        for task in tasks:
            method = getattr(self.executor, task, None)
            if method:
                try:
                    method()
                except Exception as e:
                    print(f"   ❌ 任务 '{task}' 执行出错: {e}")
                    record_audit(task, {"error": str(e)}, "fail")
            else:
                print(f"⚠️ 任务 '{task}' 暂未实现")

        return "\n✅ 全部完成！你看哪一步有问题，我继续优化。"


# ============================================================
# 命令行接口
# ============================================================
def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║  🐉 龍魂 · 自然语言意图引擎 v1.0                            ║
║  你说人话，AI自动理解、自动执行、自动验证                   ║
║  DNA: #龍芯⚡️丙午·丙申·庚申·亥时-NATURAL-ENGINE-UID9622   ║
║  --------------------------------------------------        ║
║  示例:                                                    ║
║    "帮我把网关和小艺链路搞通，史官记录我要看一眼"          ║
║    "看看现在系统状态"                                     ║
║    "清理端口，重启浏览器服务"                             ║
╚══════════════════════════════════════════════════════════════╝
    """)

    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("💬 你想做什么？> ")

    engine = NaturalEngine()
    result = engine.run(user_input)
    print(result)


if __name__ == "__main__":
    main()
