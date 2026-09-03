#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 · ASI神经网初始化 v1.0
DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-ASI-BOOT-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过

功能: ASI神经网初始化 - 连接所有人格、Agent、知识图谱、剪贴板容器，生成统一状态报告。
"""

import json
import time
import hashlib
import socket
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# ============================================================
# 路径与常量
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

LONGHUN_ROOT = Path(__file__).resolve().parent.parent
ENGINES_DIR = LONGHUN_ROOT / "05_ENGINES"
BIN_DIR = LONGHUN_ROOT / "08_BIN"
STATE_FILE = Path.home() / ".longhun" / "asi_state.json"


def generate_dna(suffix: str = "ASI") -> str:
    rand = hashlib.sha256(f"{suffix}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-{suffix}-{rand}-{UID}"


def is_port_open(port: int, host: str = "127.0.0.1") -> bool:
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except (OSError, socket.timeout):
        return False


class ASINetwork:
    """ASI神经网 - 超级智能体协调层"""

    def __init__(self):
        self.dna = generate_dna("ASI-NET")
        self.personas = self._load_personas()
        self.agent_status = self._load_agent_status()
        self.knowledge = self._load_knowledge()
        self.clipboard = self._load_clipboard()
        self.servers = self._check_servers()
        self.status = "🟢 运行中"

    def _load_personas(self) -> List[Dict[str, Any]]:
        """加载人格矩阵"""
        try:
            import sys
            sys.path.insert(0, str(ENGINES_DIR))
            from lh_persona_runner import PERSONA_MATRIX
            return [
                {"id": pid, "name": meta["name"], "layer": meta["layer"], "role": meta["role"]}
                for pid, meta in PERSONA_MATRIX.items()
            ]
        except Exception as e:
            print(f"⚠️ 人格加载失败: {e}")
            return []

    def _load_agent_status(self) -> Dict[str, Any]:
        """加载Agent执行器状态"""
        try:
            import sys
            sys.path.insert(0, str(ENGINES_DIR))
            from lh_agent_executor import AgentExecutor
            agent = AgentExecutor()
            return agent.status()
        except Exception as e:
            return {"error": str(e)}

    def _load_knowledge(self) -> Dict[str, Any]:
        """加载知识图谱统计"""
        try:
            from pathlib import Path
            kg_dir = Path.home() / ".longhun" / "knowledge_graph"
            index_file = kg_dir / "knowledge_index.json"
            if index_file.exists():
                with open(index_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return {
                        "total_nodes": data.get("total_nodes", 0),
                        "total_relations": data.get("total_relations", 0),
                        "index_file": str(index_file),
                    }
            # 退而统计 nodes 目录
            nodes_dir = kg_dir / "nodes"
            count = len(list(nodes_dir.glob("*.json"))) if nodes_dir.exists() else 0
            return {"total_nodes": count, "index_file": None}
        except Exception as e:
            return {"error": str(e)}

    def _load_clipboard(self) -> Dict[str, Any]:
        """加载剪贴板容器统计"""
        try:
            import sys
            sys.path.insert(0, str(ENGINES_DIR))
            from lh_clipboard_vault import list_vault
            items = list_vault()
            return {"count": len(items)}
        except Exception as e:
            return {"error": str(e)}

    def _check_servers(self) -> Dict[str, Any]:
        """检查核心服务端口"""
        return {
            "cnsh_gateway": {"port": 8765, "open": is_port_open(8765)},
            "knowledge_graph": {"port": 8767, "open": is_port_open(8767)},
        }

    def status_report(self) -> Dict[str, Any]:
        """生成ASI状态报告"""
        return {
            "dna": self.dna,
            "status": self.status,
            "timestamp": datetime.now().isoformat(),
            "personas": len(self.personas),
            "persona_layers": self._count_layers(),
            "knowledge": self.knowledge,
            "clipboard": self.clipboard,
            "agent": self.agent_status,
            "servers": self.servers,
        }

    def _count_layers(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for p in self.personas:
            layer = p.get("layer", "unknown")
            counts[layer] = counts.get(layer, 0) + 1
        return counts


def asi_boot(json_mode: bool = False) -> Dict[str, Any]:
    if not json_mode:
        print("""
╔══════════════════════════════════════════════════════════════╗
║  🧬 龍魂 · ASI神经网初始化                                  ║
╚══════════════════════════════════════════════════════════════╝
        """)

    asi = ASINetwork()
    report = asi.status_report()

    if json_mode:
        return report

    print(f"🧬 ASI DNA: {report['dna']}")
    print(f"📊 状态: {report['status']}")
    print(f"🕐 时间: {report['timestamp']}")
    print(f"🧠 人格数: {report['personas']}")
    print(f"   分层统计: {report['persona_layers']}")
    print(f"📚 知识节点: {report['knowledge'].get('total_nodes', 'N/A')}")
    print(f"📋 剪贴板条目: {report['clipboard'].get('count', 'N/A')}")
    print(f"🤖 Agent任务统计: {report['agent']}")
    print("\n📡 核心服务端口:")
    for name, info in report["servers"].items():
        icon = "🟢" if info["open"] else "🔴"
        print(f"  {icon} {name:20s} :{info['port']} {'运行中' if info['open'] else '未运行'}")

    # 保存ASI状态
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n✅ ASI状态已保存: {STATE_FILE}")
    return report


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · ASI神经网初始化")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    report = asi_boot(json_mode=args.json)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
