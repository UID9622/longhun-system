#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 引擎状态同步器 v1.0
DNA: #龍芯⚡️丙午·乙未·乙未·申时·☰乾-NOTION-STATUS-SYNC-v1.0
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

同步引擎运行状态变更。监控引擎文件的修改时间、Git 状态、进程存活等，
将状态变更写回注册表，供 Notion 同步管道消费。

用法:
  python3 bin/lh_notion_status_sync.py              # 同步所有引擎状态
  python3 bin/lh_notion_status_sync.py --watch       # 增量监控模式
  python3 bin/lh_notion_status_sync.py --report      # 生成状态报告
  python3 bin/lh_notion_status_sync.py --check-alive # 检查服务进程存活
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·乙未·乙未·申时·☰乾-NOTION-STATUS-SYNC-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_FILE = ROOT / "data" / "notion_sync" / "engines" / "engine_registry_tagged.json"
FALLBACK_FILE = ROOT / "data" / "notion_sync" / "engines" / "engine_registry.json"
STATUS_FILE = ROOT / "data" / "notion_sync" / "engines" / "engine_status.json"
REPORT_FILE = ROOT / "data" / "notion_sync" / "engines" / "engine_status_report.md"

# ── 服务进程→引擎映射 ────────────────────────────────
KNOWN_SERVICES: Dict[str, str] = {
    "com.longhun.knowledge-hub": "lh_knowledge_hub",
    "com.longhun.observe": "lh_obs_engine",
    "com.longhun.autoheal": "lh_auto_heal",
    "com.longhun.gateway": "lh_api_gateway",
    "com.longhun.notion-sync": "lh_notion_sync",
    "com.longhun.team-orchestrator": "lh_team_orchestrator",
    "com.longhun.health-alert": "lh_health_alert",
    "com.longhun.immutable-history": "lh_immutable_history",
    "com.longhun.semantic-guard": "lh_sg_startup_guard",
    "com.longhun.guanlan": "lh_guanlan_api",
}

ENGINE_STATUSES = {
    "active": "活跃·正常运行",
    "stale": "停滞·超过30天未更新",
    "broken": "损坏·语法错误或无法导入",
    "untracked": "未跟踪·不在Git中",
    "new": "新增·首次发现",
    "deleted": "已删除·文件消失",
    "renamed": "已重命名·路径变更",
    "experimental": "实验性·标注实验",
    "deprecated": "已废弃·标注废弃",
    "archived": "已归档·冷数据",
}


def _now() -> str:
    return datetime.now(CST).isoformat()


def _log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴", "ALIVE": "💚", "DEAD": "💀"}
    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] {markers.get(level, 'ℹ️')} {msg}")


def _load_registry() -> Optional[Dict]:
    for f in (REGISTRY_FILE, FALLBACK_FILE):
        if f.exists():
            with open(f) as fh:
                return json.load(fh)
    return None


def _load_prev_status() -> Dict:
    if STATUS_FILE.exists():
        with open(STATUS_FILE) as f:
            return json.load(f)
    return {"dna": DNA, "engines": {}, "updated_at": None}


def _check_git_status() -> Dict[str, str]:
    """获取所有文件的 Git 状态"""
    git_status: Dict[str, str] = {}
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain"],
            capture_output=True, text=True, timeout=10,
        )
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            status_code = line[:2].strip()
            filepath = line[3:].strip()
            status_map = {
                "M": "modified",
                "A": "added",
                "D": "deleted",
                "R": "renamed",
                "C": "copied",
                "??": "untracked",
            }
            git_status[filepath] = status_map.get(status_code, "unknown")
    except Exception as e:
        _log(f"Git 状态检查失败: {e}", "WARN")
    return git_status


def _check_process_alive() -> Dict[str, bool]:
    """检查已知服务进程是否存活"""
    alive: Dict[str, bool] = {}

    # macOS launchd
    for label, engine_name in KNOWN_SERVICES.items():
        try:
            result = subprocess.run(
                ["launchctl", "print", f"gui/501/{label}"],
                capture_output=True, text=True, timeout=5,
            )
            # "state = running" 表示在跑
            alive[engine_name] = "state = running" in result.stdout
        except Exception:
            alive[engine_name] = False

    # 检查端口监听（鲲鹏服务也在这里检查）
    port_checks = {
        "lh_knowledge_hub_port": ("localhost", 8766),
        "lh_guanlan_api_port": ("localhost", 8770),
        "lh_team_orchestrator_port": ("localhost", 8781),
    }
    import socket
    for name, (host, port) in port_checks.items():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((host, port))
            s.close()
            name_short = name.replace("_port", "")
            alive[name_short] = True
        except Exception:
            pass

    return alive


def _check_syntax(filepath: Path) -> Tuple[bool, str]:
    """检查 Python 文件语法是否正确"""
    try:
        content = filepath.read_text(encoding="utf-8")
        import ast
        ast.parse(content)
        return True, ""
    except SyntaxError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)


def sync_all() -> Dict[str, Any]:
    """全量同步所有引擎状态"""
    registry = _load_registry()
    if not registry:
        _log("注册表不存在", "ERROR")
        return {"error": "registry not found"}

    prev_status = _load_prev_status()
    prev_engines = prev_status.get("engines", {})
    git_status = _check_git_status()
    process_alive = _check_process_alive()

    engines = registry.get("engines", [])
    status_list: List[Dict] = []
    stats = {"active": 0, "stale": 0, "broken": 0, "new": 0, "deleted": 0,
             "untracked": 0, "modified": 0, "experimental": 0, "deprecated": 0}

    STALE_DAYS = 30  # 超过30天未修改=停滞

    for eng in engines:
        filepath = ROOT / eng["path"]
        name = eng["name"]
        entry: Dict[str, Any] = {
            "name": name,
            "path": eng["path"],
            "previous_status": prev_engines.get(name, {}).get("status", "unknown"),
            "checked_at": _now(),
        }

        # 文件是否存在
        if not filepath.exists():
            entry["status"] = "deleted"
            entry["status_changed"] = entry["previous_status"] != "deleted"
            stats["deleted"] += 1
            status_list.append(entry)
            continue

        # 修改时间
        mtime = datetime.fromtimestamp(filepath.stat().st_mtime, tz=CST)
        days_since = (datetime.now(CST) - mtime).days
        entry["last_modified"] = mtime.isoformat()
        entry["days_since_modify"] = days_since

        # Git 状态
        rel = eng["path"]
        gs = git_status.get(rel, "")
        entry["git_status"] = gs

        # 判断状态
        if "experimental" in (eng.get("ops_tags") or []):
            entry["status"] = "experimental"
            stats["experimental"] += 1
        elif "deprecated" in (eng.get("ops_tags") or []):
            entry["status"] = "deprecated"
            stats["deprecated"] += 1
        elif gs == "untracked":
            entry["status"] = "untracked"
            stats["untracked"] += 1
        elif days_since > STALE_DAYS:
            entry["status"] = "stale"
            stats["stale"] += 1
        elif gs in ("modified", "added"):
            entry["status"] = "active"
            entry["modified"] = True
            stats["modified"] += 1
            stats["active"] += 1
        else:
            entry["status"] = "active"
            stats["active"] += 1

        # 语法检查（只对最近修改的）
        if days_since < 7 and filepath.suffix == ".py":
            ok, err = _check_syntax(filepath)
            if not ok:
                entry["status"] = "broken"
                entry["syntax_error"] = err
                stats["broken"] += 1
                if "active" in (entry.get("previous_status"), entry.get("status")):
                    stats["active"] = max(0, stats.get("active", 1) - 1)

        # 进程存活（仅已知服务）
        for svc_name in process_alive:
            if svc_name in name or name in svc_name:
                entry["process_alive"] = process_alive[svc_name]
                break

        entry["status_changed"] = entry["status"] != entry["previous_status"]
        if entry["status_changed"]:
            entry["previous_status_for_record"] = entry["previous_status"]

        status_list.append(entry)

    # 排序：broken > deleted > stale > 其他
    priority = {"broken": 0, "deleted": 1, "stale": 2, "deprecated": 3, "experimental": 4, "untracked": 5, "active": 6, "new": 7}
    status_list.sort(key=lambda s: (priority.get(s["status"], 99), s["name"]))

    result = {
        "dna": DNA,
        "version": "1.0",
        "updated_at": _now(),
        "stats": stats,
        "status_changes": [s for s in status_list if s.get("status_changed")],
        "engines": status_list,
    }

    # 保存
    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATUS_FILE, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    _log(f"状态同步完成: {len(status_list)} 引擎", "OK")

    return result


def generate_report(status: Dict[str, Any]) -> str:
    """生成 Markdown 状态报告"""
    stats = status["stats"]
    changes = status.get("status_changes", [])
    broken = [s for s in status["engines"] if s["status"] == "broken"]
    stale = [s for s in status["engines"] if s["status"] == "stale"]
    deleted = [s for s in status["engines"] if s["status"] == "deleted"]

    now_dt = datetime.now(CST)
    md = f"""# 龍魂引擎状态报告

> DNA: {DNA}
> 生成时间: {status['updated_at']}
> 检查范围: {len(status['engines'])} 个引擎

## 总览

| 状态 | 数量 | 占比 |
|:---|:---:|:---:|
"""
    total = len(status["engines"])
    for key, label in [
        ("active", "🟢 活跃"), ("stale", "🟡 停滞"), ("broken", "🔴 损坏"),
        ("new", "🆕 新增"), ("deleted", "💀 删除"), ("experimental", "🧪 实验性"),
        ("deprecated", "🗑️ 废弃"), ("untracked", "❓ 未跟踪"), ("modified", "✏️ 已修改"),
    ]:
        cnt = stats.get(key, 0)
        if cnt > 0:
            md += f"| {label} | {cnt} | {cnt*100//max(total,1)}% |\n"

    if broken:
        md += f"\n## 🔴 损坏的引擎 ({len(broken)})\n\n| 名称 | 路径 | 错误 |\n|:---|:---|:---|\n"
        for b in broken[:20]:
            err = b.get("syntax_error", "?")[:60]
            md += f"| `{b['name']}` | {b['path']} | {err} |\n"

    if deleted:
        md += f"\n## 💀 已删除的文件 ({len(deleted)})\n\n"
        for d in deleted:
            md += f"- `{d['name']}` → {d['path']}\n"

    if stale:
        md += f"\n## 🟡 停滞的引擎 ({len(stale)})  (>30天未修改)\n\n| 名称 | 最后修改 | 天数 |\n|:---|:---|:---:|\n"
        for s in stale[:20]:
            md += f"| `{s['name']}` | {s.get('last_modified','?')[:10]} | {s.get('days_since_modify','?')} |\n"

    if changes:
        md += f"\n## 🔄 状态变更 ({len(changes)})\n\n| 名称 | 旧状态 | 新状态 |\n|:---|:---|:---|\n"
        for c in changes[:30]:
            md += f"| `{c['name']}` | {c.get('previous_status_for_record','?')} → | {c['status']} |\n"

    md += f"\n---\n> 自动生成 {_now()} · 下次检查建议 24h 后\n"

    return md


def _now_fmt() -> str:
    return datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")


# ── 入口 ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="龍魂 Notion 引擎状态同步器")
    parser.add_argument("--watch", action="store_true", help="增量监控模式（只检测变更）")
    parser.add_argument("--report", action="store_true", help="生成状态报告")
    parser.add_argument("--check-alive", action="store_true", help="仅检查进程存活")
    args = parser.parse_args()

    print(f"\n{DNA}")
    print(f"{CONFIRM}\n")

    if args.check_alive:
        alive = _check_process_alive()
        _log("进程存活检查:")
        for name, is_alive in sorted(alive.items()):
            marker = "ALIVE" if is_alive else "DEAD"
            _log(f"  {name:32s} {'运行中' if is_alive else '未运行'}", marker)
        up = sum(1 for v in alive.values() if v)
        _log(f"汇总: {up}/{len(alive)} 服务运行中", "OK")
        return

    if args.watch:
        _log("增量监控模式（检测变更）...")
        # 运行发现器的 diff 模式
        result = subprocess.run(
            ["python3", str(ROOT / "bin" / "lh_notion_engine_discovery.py"), "--diff", "--no-save"],
            capture_output=True, text=True, timeout=120,
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return

    status = sync_all()
    stats = status["stats"]

    print(f"\n📊 引擎状态总览 ({status['updated_at']})")
    print(f"  🟢 活跃:  {stats.get('active', 0)}")
    print(f"  🟡 停滞:  {stats.get('stale', 0)}")
    print(f"  🔴 损坏:  {stats.get('broken', 0)}")
    print(f"  💀 删除:  {stats.get('deleted', 0)}")
    print(f"  ✏️  修改:  {stats.get('modified', 0)}")
    print(f"  🧪 实验:  {stats.get('experimental', 0)}")
    print(f"  🗑️  废弃:  {stats.get('deprecated', 0)}")
    print(f"  ❓ 未跟踪: {stats.get('untracked', 0)}")

    changes = status.get("status_changes", [])
    if changes:
        print(f"\n🔄 状态变更 ({len(changes)}):")
        for c in changes[:10]:
            print(f"  {c['name']:24s} {c.get('previous_status_for_record','?'):>10s} → {c['status']}")

    if stats.get("broken", 0) > 0:
        _log(f"警告: {stats['broken']} 个引擎损坏！", "WARN")
    if stats.get("deleted", 0) > 0:
        _log(f"警告: {stats['deleted']} 个文件已删除！", "WARN")

    if args.report:
        report = generate_report(status)
        REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_FILE, "w") as f:
            f.write(report)
        _log(f"状态报告已保存: {REPORT_FILE}", "OK")

    _log("完成", "OK")


if __name__ == "__main__":
    main()
