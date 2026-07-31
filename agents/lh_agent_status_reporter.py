# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂智能体编排层 · 状态上报与三才审计报告

聚合 L1 守护进程、L2 技能、L3 人格矩阵，输出：
- 天（系统/路由/人格完整性）
- 地（本地数据/守护/安全状态）
- 人（任务/审计/交互活跃度）

DNA: #龍芯⚡️2026-06-26-LONGHUN-AGENT-STATUS-REPORTER-v1.0
"""

import argparse
import datetime
import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

DNA = "#龍芯⚡️2026-06-26-LONGHUN-AGENT-STATUS-REPORTER-v1.0"
VERSION = "1.0.0"

AGENTS_HOME = Path.home() / "longhun-system" / "agents"
REPORT_DIR = AGENTS_HOME / "reports"
DAEMON_LOG_DIR = AGENTS_HOME / "daemon_logs"
MANIFEST_PATH = AGENTS_HOME / "manifest.json"
AUDIT_LOG_PATH = Path.home() / ".longhun" / "agents" / "orchestrator_audit.jsonl"
EMPOWER_HEALTH_URL = "http://127.0.0.1:9622/health"

os.makedirs(REPORT_DIR, exist_ok=True)


def now_iso() -> str:
    return datetime.datetime.now().isoformat()


def read_json(path: Path, default: Any = None) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default if default is not None else {}


def digital_root(n: int) -> int:
    """数字根：反复求各位和直到个位数。"""
    if n <= 0:
        return 0
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def tri_color(score: float) -> str:
    if score >= 0.7:
        return "🟢 绿色通行"
    if score >= 0.4:
        return "🟡 黄色待审"
    return "🔴 红色告警"


def check_empower_health() -> Dict[str, Any]:
    try:
        with urllib.request.urlopen(EMPOWER_HEALTH_URL, timeout=2) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {"ok": True, "data": data}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def load_manifest_stats() -> Dict[str, Any]:
    manifest = read_json(MANIFEST_PATH, {})
    agents = manifest.get("agents", [])
    layers = {}
    for a in agents:
        layers[a.get("layer", "unknown")] = layers.get(a.get("layer", "unknown"), 0) + 1
    return {
        "total_agents": len(agents),
        "layers": layers,
        "zeng71_count": layers.get("L3", 0),
        "manifest_version": manifest.get("version", "unknown"),
        "manifest_dna": manifest.get("dna", ""),
    }


def load_daemon_status() -> Dict[str, Any]:
    from agent_daemon import _read_pid, _is_alive
    pid = _read_pid()
    alive = bool(pid and _is_alive(pid))
    state = read_json(AGENTS_HOME / "daemon_state.json", {})
    heartbeat = read_json(DAEMON_LOG_DIR / "heartbeat.json", {})
    agents = heartbeat.get("agents", [])
    running_agents = sum(1 for a in agents if a.get("state") in ("idle", "running"))
    error_agents = sum(1 for a in agents if a.get("state") == "error")
    last_beat = heartbeat.get("timestamp")
    beat_age_sec = None
    if last_beat:
        try:
            beat_age_sec = (datetime.datetime.now() - datetime.datetime.fromisoformat(last_beat)).total_seconds()
        except Exception:
            pass
    return {
        "running": alive,
        "pid": pid,
        "version": state.get("version", "unknown"),
        "started_at": state.get("started_at"),
        "agents_count": len(agents),
        "healthy_agents": running_agents,
        "error_agents": error_agents,
        "last_heartbeat": last_beat,
        "heartbeat_age_sec": beat_age_sec,
    }


def load_guardian_audit() -> Dict[str, Any]:
    return read_json(DAEMON_LOG_DIR / "guardian_audit.json", {
        "sensitive_file_count": 0,
        "suspicious_snippet_count": 0,
        "audit_color": "🟢",
    })


def load_orchestrator_audit() -> Dict[str, Any]:
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    total = 0
    today_count = 0
    if AUDIT_LOG_PATH.exists():
        try:
            with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    total += 1
                    try:
                        entry = json.loads(line)
                        ts = entry.get("timestamp", "")
                        if today in ts:
                            today_count += 1
                    except Exception:
                        pass
        except Exception:
            pass
    return {"total_entries": total, "today_entries": today_count}


def load_eco_status() -> Dict[str, Any]:
    try:
        from agent_eco_adapter import eco_status
        data = eco_status()
        st = data.get("status", {})
        return {
            "available": True,
            "agent_total": st.get("智能體總數", 0),
            "ready": st.get("就緒數", 0),
            "system_score": st.get("系統評分", 0.0),
            "dna_integrity": st.get("DNA完整性", False),
        }
    except Exception as e:
        return {"available": False, "error": str(e)}


def compute_sancai(manifest: Dict, daemon: Dict, guardian: Dict,
                   audit: Dict, eco: Dict, empower: Dict) -> Dict[str, Any]:
    # 天：系统完整性 / 路由 / L3 人格 / eco / empower
    heaven = 0.0
    if manifest.get("zeng71_count", 0) >= 71:
        heaven += 0.4
    elif manifest.get("zeng71_count", 0) >= 50:
        heaven += 0.25
    if manifest.get("total_agents", 0) >= 80:
        heaven += 0.2
    if eco.get("available") and eco.get("dna_integrity"):
        heaven += 0.2
    if empower.get("ok"):
        heaven += 0.2
    heaven = min(1.0, heaven)

    # 地：守护进程 / 安全 / 数据新鲜度
    earth = 0.0
    if daemon.get("running"):
        earth += 0.35
    healthy = daemon.get("healthy_agents", 0)
    if healthy >= 5:
        earth += 0.25
    elif healthy >= 3:
        earth += 0.15
    age = daemon.get("heartbeat_age_sec")
    if age is not None and age < 600:
        earth += 0.2
    guard_color = guardian.get("audit_color", "🟢")
    if "🟢" in guard_color:
        earth += 0.2
    elif "🟡" in guard_color:
        earth += 0.1
    earth = min(1.0, earth)

    # 人：审计活跃度 / 任务 / 交互
    human = 0.0
    today = audit.get("today_entries", 0)
    if today >= 5:
        human += 0.4
    elif today >= 1:
        human += 0.2
    total = audit.get("total_entries", 0)
    if total >= 10:
        human += 0.2
    if eco.get("available"):
        human += 0.2
    if empower.get("ok"):
        human += 0.2
    human = min(1.0, human)

    overall = round((heaven + earth + human) / 3, 3)
    dr = digital_root(int(round(overall * 100, 0)))
    return {
        "heaven": round(heaven, 3),
        "earth": round(earth, 3),
        "human": round(human, 3),
        "overall": overall,
        "digital_root": dr,
        "color": tri_color(overall),
    }


def generate_report() -> Dict[str, Any]:
    manifest = load_manifest_stats()
    daemon = load_daemon_status()
    guardian = load_guardian_audit()
    audit = load_orchestrator_audit()
    eco = load_eco_status()
    empower = check_empower_health()
    sancai = compute_sancai(manifest, daemon, guardian, audit, eco, empower)

    report = {
        "report_dna": DNA,
        "version": VERSION,
        "generated_at": now_iso(),
        "manifest": manifest,
        "daemon": daemon,
        "guardian": guardian,
        "orchestrator_audit": audit,
        "agent_eco": eco,
        "empower_engine": empower,
        "sancai": sancai,
    }

    # 写入 JSON 摘要
    json_path = REPORT_DIR / "latest_sancai_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # 写入 Markdown 报告
    md_path = REPORT_DIR / f"sancai_audit_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    md_lines = [
        "# 龍魂智能体 · 三才审计报告",
        "",
        f"**生成时间**: {report['generated_at']}",
        f"**DNA**: {DNA}",
        f"**版本**: {VERSION}",
        "",
        "## 一、三才总览",
        "",
        f"| 维度 | 得分 | 说明 |",
        f"|------|------|------|",
        f"| 天（系统/路由/人格） | {sancai['heaven']:.3f} | 人格矩阵完整度、路由引擎、技能健康 |",
        f"| 地（守护/数据/安全） | {sancai['earth']:.3f} | L1 守护进程、安全审计、数据新鲜度 |",
        f"| 人（任务/审计/交互） | {sancai['human']:.3f} | 编排器审计、任务调度、人机交互 |",
        "",
        f"**综合评分**: {sancai['overall']:.3f}",
        f"**数字根**: dr={sancai['digital_root']}",
        f"**三色状态**: {sancai['color']}",
        "",
        "## 二、注册表状态",
        "",
        f"- 智能体总数: {manifest['total_agents']}",
        f"- 分层统计: {manifest['layers']}",
        f"- 曾老师 71 人格矩阵: {'✅ 已完整接入' if manifest['zeng71_count'] >= 71 else '⚠️ 未完整'} ({manifest['zeng71_count']} 个)",
        f"- Manifest 版本: {manifest['manifest_version']}",
        "",
        "## 三、L1 守护进程状态",
        "",
        f"- 运行状态: {'🟢 运行中' if daemon['running'] else '🔴 未运行'}",
        f"- PID: {daemon.get('pid') or 'N/A'}",
        f"- 版本: {daemon['version']}",
        f"- 常驻人格数: {daemon['agents_count']}",
        f"- 健康人格数: {daemon['healthy_agents']}",
        f"- 异常人格数: {daemon['error_agents']}",
        f"- 最新心跳: {daemon.get('last_heartbeat') or 'N/A'}",
        f"- 心跳年龄: {daemon.get('heartbeat_age_sec')} 秒" if daemon.get('heartbeat_age_sec') is not None else "",
        "",
        "### 各人格状态",
        "",
        "| ID | 名称 | 状态 |",
        "|----|------|------|",
    ]
    for a in daemon.get("agents", []):
        md_lines.append(f"| {a.get('id')} | {a.get('name')} | {a.get('state')} |")
    md_lines += [
        "",
        "## 四、安全审计（上帝之眼）",
        "",
        f"- 敏感文件数: {guardian.get('sensitive_file_count', 0)}",
        f"- 可疑内容片段数: {guardian.get('suspicious_snippet_count', 0)}",
        f"- 审计色: {guardian.get('audit_color', 'N/A')}",
        "",
        "## 五、编排器审计",
        "",
        f"- 审计日志总条目: {audit['total_entries']}",
        f"- 今日条目: {audit['today_entries']}",
        "",
        "## 六、技能与路由",
        "",
        f"- agent-eco 可用: {'✅' if eco.get('available') else '❌'}",
        f"- agent-eco 系统评分: {eco.get('system_score', 'N/A')}",
        f"- empower-engine 健康: {'✅' if empower.get('ok') else '❌'}",
        "",
        "---",
        "*本报告由龍魂智能体编排层自动生成，数据全部本地存储，不上传。*",
    ]
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    return report, json_path, md_path


def main():
    parser = argparse.ArgumentParser(description="龍魂智能体三才审计报告")
    parser.add_argument("--json", action="store_true", help="仅输出 JSON 摘要")
    args = parser.parse_args()

    report, json_path, md_path = generate_report()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"🐉 三才审计报告已生成")
        print(f"   JSON: {json_path}")
        print(f"   Markdown: {md_path}")
        sc = report["sancai"]
        print(f"   综合评分: {sc['overall']:.3f} | 数字根 dr={sc['digital_root']} | {sc['color']}")


if __name__ == "__main__":
    main()
