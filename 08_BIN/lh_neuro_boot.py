#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 神经拓扑启动器 v1.0
DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-NEURO-BOOT-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过

功能: 一键启动/状态查看龍魂系统核心模块，并把剪贴板内容接入本地容器与知识图谱。
已集成:
  - 主权网关 (cnsh_gateway.py :8765)
  - 人格矩阵 (lh_persona_runner.py 22人格)
  - 知识图谱引擎 (lh_knowledge_graph_v2.py :8767)
  - 快速检索引擎 (lh_quick_retrieval.py)
  - 剪贴板容器 (lh_clipboard_vault.py :8765/本地)
  - 跨设备同步 (lh_cross_device_server.sh)
  - Mac互通引擎 (lh_unify.py)
"""

import os
import sys
import subprocess
import socket
import time
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# ============================================================
# 路径与常量
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

LONGHUN_ROOT = Path(__file__).resolve().parent.parent
BIN_DIR = LONGHUN_ROOT / "08_BIN"
ENGINES_DIR = LONGHUN_ROOT / "05_ENGINES"
STATE_FILE = Path.home() / ".longhun" / "neuro_state.json"

# 端口映射（与系统现有服务对齐）
PORT_GATEWAY = 8765       # cnsh_gateway
PORT_KG = 8767            # knowledge_graph
PORT_CLIPBOARD = 8765     # clipboard vault 复用网关端口标识

PROCS: List[subprocess.Popen] = []


def generate_dna(suffix: str = "NEURO") -> str:
    rand = hashlib.sha256(f"{suffix}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-{suffix}-{rand}-{UID}"


def is_port_open(port: int, host: str = "127.0.0.1") -> bool:
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except Exception:
        return False


def run_bg(cmd: List[str], name: str, wait: float = 2.0) -> Optional[subprocess.Popen]:
    """后台启动一个服务进程"""
    print(f"🚀 启动 {name} ...")
    try:
        proc = subprocess.Popen(
            cmd,
            cwd=LONGHUN_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        PROCS.append(proc)
        time.sleep(wait)
        if proc.poll() is None:
            print(f"  ✅ {name} 已启动 (PID {proc.pid})")
            return proc
        else:
            print(f"  ❌ {name} 启动后退出 (code {proc.returncode})")
            return None
    except Exception as e:
        print(f"  ❌ {name} 启动失败: {e}")
        return None


def init_persona_matrix() -> Dict[str, Any]:
    """初始化人格矩阵"""
    print("\n🧠 初始化人格矩阵...")
    try:
        sys.path.insert(0, str(ENGINES_DIR))
        from lh_persona_runner import PERSONA_MATRIX
        return {
            "status": "ok",
            "count": len(PERSONA_MATRIX),
            "personas": [f"{pid}:{m['name']}" for pid, m in PERSONA_MATRIX.items()],
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def init_knowledge_graph() -> Dict[str, Any]:
    """初始化知识图谱索引"""
    print("\n📚 初始化知识图谱...")
    try:
        script = BIN_DIR / "lh_knowledge_graph_v2.py"
        result = subprocess.run(
            ["python3", str(script), "--status"],
            cwd=LONGHUN_ROOT,
            capture_output=True,
            text=True,
            timeout=15,
        )
        return {
            "status": "ok" if result.returncode == 0 else "error",
            "output": result.stdout.strip()[-500:] if result.stdout else "",
            "error": result.stderr.strip()[-300:] if result.stderr else "",
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def init_quick_retrieval() -> Dict[str, Any]:
    """初始化快速检索索引"""
    print("\n🔍 初始化快速检索引擎...")
    try:
        script = BIN_DIR / "lh_quick_retrieval.py"
        result = subprocess.run(
            ["python3", str(script), "index"],
            cwd=LONGHUN_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return {
            "status": "ok" if result.returncode == 0 else "error",
            "output": result.stdout.strip()[-300:] if result.stdout else "",
            "error": result.stderr.strip()[-300:] if result.stderr else "",
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def init_clipboard_vault() -> Dict[str, Any]:
    """初始化剪贴板容器"""
    print("\n📋 初始化剪贴板容器...")
    try:
        sys.path.insert(0, str(LONGHUN_ROOT))
        sys.path.insert(0, str(ENGINES_DIR))
        from lh_clipboard_vault import list_vault, VAULT_ROOT
        items = list_vault()
        return {
            "status": "ok",
            "count": len(items),
            "vault_root": str(VAULT_ROOT),
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def init_cross_device() -> Dict[str, Any]:
    """初始化跨设备同步（仅检查脚本存在与端口状态，不自动启动）"""
    print("\n📡 初始化跨设备同步...")
    script = BIN_DIR / "lh_cross_device_server.sh"
    if not script.exists():
        return {"status": "missing", "error": f"{script} 不存在"}
    try:
        ports = [19622, 19623, 18799]
        open_ports = [p for p in ports if is_port_open(p)]
        return {
            "status": "ok",
            "script": str(script),
            "ports_open": open_ports,
            "ready": len(open_ports) > 0,
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def init_mac_unify() -> Dict[str, Any]:
    """初始化Mac互通引擎"""
    print("\n🖥️  初始化Mac互通引擎...")
    try:
        script = BIN_DIR / "lh_unify.py"
        result = subprocess.run(
            ["python3", str(script), "--help"],
            cwd=LONGHUN_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return {
            "status": "ok" if result.returncode == 0 else "error",
            "ready": result.returncode == 0,
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def save_clipboard(content: str, source: str = "clipboard", topic: Optional[str] = None,
                   tags: Optional[List[str]] = None, to_kg: bool = True) -> Dict[str, Any]:
    """
    把内容保存到剪贴板容器，并可选导入知识图谱。
    """
    sys.path.insert(0, str(LONGHUN_ROOT))
    sys.path.insert(0, str(ENGINES_DIR))

    # 1. 保存到剪贴板容器
    from lh_clipboard_vault import save as vault_save
    result = vault_save(content, source=source, topic=topic, tags=tags)

    # 2. 导入知识图谱
    kg_result = None
    if to_kg:
        try:
            sys.path.insert(0, str(BIN_DIR))
            from lh_knowledge_graph_v2 import KnowledgeGraphEngine
            engine = KnowledgeGraphEngine()
            title = content.strip().split("\n")[0][:64]
            node = engine.create_node(
                name=title,
                description=content[:500],
                keywords=tags or [topic] if topic else ["剪贴板"],
                tiancai="人",
            )
            kg_result = {
                "status": "ok",
                "node_id": node.id,
                "node_name": node.name,
                "tiancai": node.tiancai,
            }
        except Exception as e:
            kg_result = {"status": "error", "error": str(e)}

    return {
        "clipboard": result,
        "knowledge_graph": kg_result,
    }


def neuro_boot(start_servers: bool = True, dry_run: bool = False) -> Dict[str, Any]:
    """一键启动神经拓扑"""
    dna = generate_dna("NEURO-BOOT")
    print("""
╔══════════════════════════════════════════════════════════════╗
║  🐉 龍魂 · 神经拓扑启动器 v1.0                              ║
╠══════════════════════════════════════════════════════════════╣
║  DNA: """ + dna + """                                        ║
║  确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                ║
╚══════════════════════════════════════════════════════════════╝
    """)

    report: Dict[str, Any] = {
        "dna": dna,
        "timestamp": datetime.now().isoformat(),
        "servers": {},
        "modules": {},
    }

    if dry_run:
        print("[DRY-RUN] 仅预览，不启动后台服务")
        start_servers = False

    # 1. 主权网关 :8765
    if start_servers:
        if is_port_open(PORT_GATEWAY):
            print(f"🟡 端口 {PORT_GATEWAY} 已被占用，假设网关已运行")
            report["servers"]["cnsh_gateway"] = {"status": "already_running", "port": PORT_GATEWAY}
        else:
            proc = run_bg(
                ["python3", str(BIN_DIR / "cnsh_gateway.py")],
                "主权网关 (cnsh_gateway)",
                wait=3.0,
            )
            report["servers"]["cnsh_gateway"] = {
                "status": "started" if proc else "failed",
                "port": PORT_GATEWAY,
                "pid": proc.pid if proc else None,
            }

    # 2. 知识图谱 :8767
    if start_servers:
        if is_port_open(PORT_KG):
            print(f"🟡 端口 {PORT_KG} 已被占用，假设知识图谱已运行")
            report["servers"]["knowledge_graph"] = {"status": "already_running", "port": PORT_KG}
        else:
            proc = run_bg(
                ["python3", str(BIN_DIR / "lh_knowledge_graph_v2.py"), "--server", str(PORT_KG)],
                "知识图谱引擎",
                wait=4.0,
            )
            report["servers"]["knowledge_graph"] = {
                "status": "started" if proc else "failed",
                "port": PORT_KG,
                "pid": proc.pid if proc else None,
            }

    # 3. 各模块初始化（不依赖端口）
    report["modules"]["persona_matrix"] = init_persona_matrix()
    report["modules"]["knowledge_graph"] = init_knowledge_graph()
    report["modules"]["quick_retrieval"] = init_quick_retrieval()
    report["modules"]["clipboard_vault"] = init_clipboard_vault()
    report["modules"]["cross_device"] = init_cross_device()
    report["modules"]["mac_unify"] = init_mac_unify()

    # 4. 保存状态
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # 5. 打印摘要
    print("""
╔══════════════════════════════════════════════════════════════╗
║  ✅ 龍魂神经拓扑初始化完成                                  ║
╠══════════════════════════════════════════════════════════════╣""")
    for name, info in report["servers"].items():
        icon = "🟢" if info.get("status") in ("started", "already_running") else "🔴"
        port = str(info.get("port", "-"))
        print(f"║  {icon} {name:20s} 端口:{port:<6s}                    ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    for name, info in report["modules"].items():
        icon = "🟢" if info.get("status") == "ok" else "🟡" if info.get("status") in ("missing",) else "🔴"
        detail = ""
        if name == "persona_matrix" and info.get("status") == "ok":
            detail = f" ({info.get('count')}人格)"
        elif name == "clipboard_vault" and info.get("status") == "ok":
            detail = f" ({info.get('count')}条)"
        print(f"║  {icon} {name:20s}{detail:<28s}  ║")
    print("""╚══════════════════════════════════════════════════════════════╝
    """)

    return report


def neuro_status() -> Dict[str, Any]:
    """查看神经拓扑状态"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║  📊 龍魂 · 神经拓扑状态                                      ║
╚══════════════════════════════════════════════════════════════╝
    """)
    status = {
        "timestamp": datetime.now().isoformat(),
        "servers": {
            "cnsh_gateway": {"port": PORT_GATEWAY, "open": is_port_open(PORT_GATEWAY)},
            "knowledge_graph": {"port": PORT_KG, "open": is_port_open(PORT_KG)},
        },
    }

    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                last = json.load(f)
            status["last_boot"] = last.get("timestamp", "未知")
            status["last_dna"] = last.get("dna", "未知")
        except Exception:
            pass

    for name, info in status["servers"].items():
        icon = "🟢" if info["open"] else "🔴"
        print(f"  {icon} {name:20s} :{info['port']} {'运行中' if info['open'] else '未运行'}")

    print(f"\n  🧬 上次启动DNA: {status.get('last_dna', '无')}")
    print(f"  🕐 上次启动时间: {status.get('last_boot', '无')}")

    return status


def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 神经拓扑启动器 v1.0"
    )
    parser.add_argument("--boot", action="store_true", help="一键启动神经拓扑")
    parser.add_argument("--status", action="store_true", help="查看神经拓扑状态")
    parser.add_argument("--dry-run", action="store_true", help="预览启动流程，不启动服务")
    parser.add_argument("--clipboard", "-c", type=str, help="把指定文本存入剪贴板容器并接入知识图谱")
    parser.add_argument("--source", type=str, default="cli", help="剪贴内容来源标识")
    parser.add_argument("--topic", type=str, help="指定主题分类")
    parser.add_argument("--tags", type=str, help="标签，逗号分隔")
    parser.add_argument("--no-kg", action="store_true", help="剪贴板保存时不写入知识图谱")

    args = parser.parse_args()

    if args.clipboard:
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else None
        result = save_clipboard(
            args.clipboard,
            source=args.source,
            topic=args.topic,
            tags=tags,
            to_kg=not args.no_kg,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if args.status:
        neuro_status()
        return

    # 默认启动
    neuro_boot(start_servers=True, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
