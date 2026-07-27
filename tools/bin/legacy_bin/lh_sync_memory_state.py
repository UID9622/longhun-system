#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·记忆状态同步器 v1.0
DNA: #龍芯⚡️2026-07-21-SYNC-MEMORY-STATE-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

职责: 将 STATE.md + 实时系统状态 → 更新 MEMORY.md 的实时状态快照
用法:
  python3 bin/lh_sync_memory_state.py              # 全量同步
  python3 bin/lh_sync_memory_state.py --live-only  # 只更新实时快照
  python3 bin/lh_sync_memory_state.py --dry-run    # 只报告，不改文件
  python3 bin/lh_sync_memory_state.py --json       # JSON输出
"""

import re, os, sys, json, subprocess, datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any

# ━━━ 路径 ━━━
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = PROJECT_ROOT / "STATE.md"
MEMORY_PATH = PROJECT_ROOT / ".codebuddy" / "memory" / "MEMORY.md"

# ━━━ 标记锚（用于定位MEMORY.md中的可更新区块）━━━
LIVE_SECTION_START = "<!-- LIVE_STATUS_START -->"
LIVE_SECTION_END = "<!-- LIVE_STATUS_END -->"
MODEL_SECTION_START = "<!-- MODEL_SYNC_START -->"
MODEL_SECTION_END = "<!-- MODEL_SYNC_END -->"

def shell(cmd: str) -> str:
    """执行命令，返回stdout，出错返回空串"""
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10).decode().strip()
    except Exception:
        return ""

# ══════════════════════════════════════════════════════════════
# 模块1: 解析STATE.md
# ══════════════════════════════════════════════════════════════

def parse_state_md() -> Dict[str, Any]:
    """解析STATE.md，提取关键状态变量"""
    if not STATE_PATH.exists():
        return {"error": "STATE.md not found"}
    
    content = STATE_PATH.read_text(encoding="utf-8")
    
    result = {
        "updated": "",
        "quick_status": {},
        "model_table": [],
        "infra": {},
        "todos": {"blocking": [], "in_progress": [], "completed": []},
    }
    
    # 提取更新日期
    m = re.search(r'更新:\s*([\d\-]+)', content)
    if m:
        result["updated"] = m.group(1)
    
    # 提取快速状态卡中的键值对
    in_quick = False
    header_skipped = False
    for line in content.split("\n"):
        if "快速状态卡" in line:
            in_quick = True
            continue
        if not in_quick:
            continue
        stripped = line.strip()
        if not stripped:
            continue  # 表格内空行不退出
        if not stripped.startswith("|"):
            in_quick = False
            continue
        if re.match(r'^\|[-:]+(\|[-:]+)*\|?$', stripped):
            header_skipped = True
            continue
        if not header_skipped:
            continue
        parts = [p.strip() for p in stripped.split("|") if p.strip()]
        if len(parts) >= 2:
            key = re.sub(r'[*🔥🥇🆕🔒✅🟡🔴❌]', '', parts[0]).strip()
            val = parts[1].strip()
            result["quick_status"][key] = val
    
    # 提取模型版本表
    in_model = False
    header_skipped = False
    for line in content.split("\n"):
        if "## 模型版本表" in line:
            in_model = True
            continue
        if not in_model:
            continue
        stripped = line.strip()
        if not stripped:
            continue  # 表格内空行不退出
        if not stripped.startswith("|"):
            in_model = False
            continue
        # 跳过分隔行 (|:---|... 或 |---|...)
        if re.match(r'^\|[-:]+(\|[-:]+)*\|?$', stripped):
            header_skipped = True
            continue
        if not header_skipped:
            # 表头行，跳过
            continue
        # 数据行
        parts = [p.strip() for p in stripped.split("|") if p.strip()]
        if len(parts) >= 5:
            result["model_table"].append({
                "version": parts[0],
                "base": parts[1],
                "val": parts[2],
                "train": parts[3],
                "iter": parts[4],
                "status": parts[5] if len(parts) > 5 else "",
            })
    
    # 提取待办
    section = None
    for line in content.split("\n"):
        if "### 🔴 阻塞" in line:
            section = "blocking"
            continue
        elif "### 🟡 进行中" in line:
            section = "in_progress"
            continue
        elif "### ✅ 已完成" in line:
            section = "completed"
            continue
        elif "### 📋 冻结" in line:
            section = None
            continue
        if section and line.strip().startswith("- ["):
            item = re.sub(r'-\s*\[.\]\s*', '', line.strip())
            result["todos"][section].append(item)
    
    return result

# ══════════════════════════════════════════════════════════════
# 模块2: 采集实时系统状态
# ══════════════════════════════════════════════════════════════

def collect_live_state() -> Dict[str, Any]:
    """采集当前系统实时状态"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ollama模型
    ollama_raw = shell("ollama list 2>/dev/null")
    ollama_models = []
    for line in ollama_raw.split("\n")[1:]:  # 跳过header
        if line.strip():
            parts = line.split()
            if len(parts) >= 3:
                ollama_models.append({
                    "name": parts[0],
                    "size": parts[2] + (" " + parts[3] if len(parts) > 3 and parts[3] in ["GB","MB","KB"] else ""),
                })
    
    # 找出active模型 (最近修改的)
    active_model = ollama_models[0]["name"] if ollama_models else "未知"
    
    # 磁盘
    disk_raw = shell("df -h / 2>/dev/null | tail -1")
    disk_parts = disk_raw.split()
    disk_info = {
        "total": disk_parts[1] if len(disk_parts) > 1 else "?",
        "used_pct": disk_parts[4] if len(disk_parts) > 4 else "?",
        "avail": disk_parts[3] if len(disk_parts) > 3 else "?",
    }
    
    # 电源
    batt_raw = shell("pmset -g batt 2>/dev/null | tail -1")
    ac_connected = "AC" in batt_raw or "charged" in batt_raw
    batt_pct = re.search(r'(\d+)%', batt_raw)
    power_status = f"{'🔌 AC' if ac_connected else '🔋 电池'}"
    if batt_pct:
        power_status += f" {batt_pct.group(1)}%"
    
    # Git状态
    git_staged = shell("cd '{0}' && git diff --cached --name-only 2>/dev/null | wc -l | tr -d ' '".format(PROJECT_ROOT))
    git_modified = shell("cd '{0}' && git diff --name-only 2>/dev/null | wc -l | tr -d ' '".format(PROJECT_ROOT))
    git_untracked = shell("cd '{0}' && git ls-files --others --exclude-standard 2>/dev/null | wc -l | tr -d ' '".format(PROJECT_ROOT))
    
    git_status = {
        "staged": int(git_staged) if git_staged.isdigit() else 0,
        "modified": int(git_modified) if git_modified.isdigit() else 0,
        "untracked": int(git_untracked) if git_untracked.isdigit() else 0,
    }
    
    # launchd服务（只统计龍魂相关的）
    lh_services = shell("launchctl list 2>/dev/null | grep -i longhun | wc -l | tr -d ' '")
    
    # 鲲鹏连通性
    kunpeng_raw = shell("ssh -o ConnectTimeout=3 -o BatchMode=yes root@119.13.90.27 'echo OK' 2>/dev/null")
    kunpeng_ok = kunpeng_raw == "OK"
    
    return {
        "timestamp": now,
        "power": power_status,
        "ac_connected": ac_connected,
        "disk": disk_info,
        "git": git_status,
        "ollama_models": len(ollama_models),
        "active_model": active_model,
        "launchd_lh_services": int(lh_services) if lh_services.isdigit() else 0,
        "kunpeng_connected": kunpeng_ok,
    }

# ══════════════════════════════════════════════════════════════
# 模块3: 更新MEMORY.md
# ══════════════════════════════════════════════════════════════

def build_live_section(live: Dict[str, Any], state: Dict[str, Any]) -> str:
    """构建实时状态快照区块"""
    lines = []
    lines.append(f"\n---\n\n## §LIVE. 实时状态快照")
    lines.append(f"> 最后同步: {live['timestamp']}")
    lines.append(f"> 来源: STATE.md + 系统实时采集")
    lines.append(f"")
    lines.append(f"| 项目 | 状态 |")
    lines.append(f"|:---|:---|")
    
    # 从STATE.md提取关键状态
    for k, v in state.get("quick_status", {}).items():
        if k and v:
            lines.append(f"| {k} | {v} |")
    
    # 补充实时系统状态
    lines.append(f"| 💻 电源 | {live['power']} |")
    lines.append(f"| 💾 磁盘 | {live['disk']['avail']} 可用 / {live['disk']['total']} ({live['disk']['used_pct']}) |")
    lines.append(f"| 🐙 Git | {live['git']['staged']}暂存 + {live['git']['modified']}修改 + {live['git']['untracked']}未跟踪 |")
    lines.append(f"| 🤖 Ollama模型 | {live['ollama_models']}个·激活: {live['active_model']} |")
    lines.append(f"| 🖥️ 鲲鹏(119.13.90.27) | {'🟢 连通' if live['kunpeng_connected'] else '🔴 不通'} |")
    lines.append(f"| ⚙️ launchd龍魂服务 | {live['launchd_lh_services']}个 |")
    lines.append(f"")
    
    return "\n".join(lines)

def update_memory_md(live: Dict[str, Any], state: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
    """更新MEMORY.md的实时状态区块"""
    if not MEMORY_PATH.exists():
        return {"error": "MEMORY.md not found", "path": str(MEMORY_PATH)}
    
    content = MEMORY_PATH.read_text(encoding="utf-8")
    
    # 更新版本头部的时间戳
    today = datetime.date.today().strftime("%Y-%m-%d")
    content = re.sub(
        r'更新: \d{4}-\d{2}-\d{2}',
        f'更新: {today}',
        content
    )
    
    # 检查是否已有LIVE区块
    if LIVE_SECTION_START in content:
        # 替换已有区块
        pattern = re.compile(
            re.escape(LIVE_SECTION_START) + r'.*?' + re.escape(LIVE_SECTION_END),
            re.DOTALL
        )
        new_section = LIVE_SECTION_START + "\n" + build_live_section(live, state) + "\n" + LIVE_SECTION_END
        content = pattern.sub(new_section, content)
    else:
        # 在文件末尾追加
        new_section = LIVE_SECTION_START + "\n" + build_live_section(live, state) + "\n" + LIVE_SECTION_END
        content = content.rstrip() + "\n" + new_section + "\n"
    
    result = {
        "updated": True,
        "path": str(MEMORY_PATH),
        "timestamp": live["timestamp"],
        "dry_run": dry_run,
    }
    
    if not dry_run:
        MEMORY_PATH.write_text(content, encoding="utf-8")
        result["written"] = True
    
    return result

# ══════════════════════════════════════════════════════════════
# 模块4: 对比STATE.md与MEMORY.md模型表的差异
# ══════════════════════════════════════════════════════════════

def diff_model_tables(state: Dict[str, Any]) -> List[str]:
    """对比STATE.md模型表与MEMORY.md §6的差异，返回差异行"""
    diffs = []
    state_models = {m["version"]: m for m in state.get("model_table", [])}
    
    if not MEMORY_PATH.exists():
        diffs.append("MEMORY.md 不存在，跳过模型表对比")
        return diffs
    
    memory_content = MEMORY_PATH.read_text(encoding="utf-8")
    
    # 解析MEMORY.md §6模型表
    in_table = False
    header_skipped = False
    mem_models = {}
    for line in memory_content.split("\n"):
        if "## §6. 模型一览" in line:
            in_table = True
            continue
        if not in_table:
            continue
        stripped = line.strip()
        if not stripped:
            continue  # 表格内空行不退出
        if not stripped.startswith("|"):
            in_table = False
            continue
        if re.match(r'^\|[-:]+(\|[-:]+)*\|?$', stripped):
            header_skipped = True
            continue
        if not header_skipped:
            continue
        parts = [p.strip() for p in stripped.split("|") if p.strip()]
        if len(parts) >= 2:
            ver_raw = parts[0]
            ver = re.sub(r'[*🔥🥇🆕🔒✅🟡🔴]', '', ver_raw).strip()
            status_raw = parts[-1] if parts else ""
            mem_models[ver] = status_raw
    
    # 对比
    for ver, sm in state_models.items():
        raw_ver = re.sub(r'[*🔥🥇🆕🔒✅🟡🔴]', '', ver).strip()
        mem_status = mem_models.get(raw_ver, "")
        state_status = sm.get("status", "")
        if raw_ver not in mem_models:
            diffs.append(f"➕ STATE.md有但MEMORY.md缺失: {ver} ({state_status})")
        # 不判断状态差异（格式可能不同），只判断存在性
    
    return diffs

# ══════════════════════════════════════════════════════════════
# 主入口
# ══════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·记忆状态同步器")
    parser.add_argument("--dry-run", action="store_true", help="只报告，不改文件")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--live-only", action="store_true", help="只更新实时快照（不动其他区块）")
    parser.add_argument("--diff", action="store_true", help="只对比STATE.md与MEMORY.md模型表差异")
    args = parser.parse_args()
    
    # 解析STATE.md
    state = parse_state_md()
    if "error" in state:
        print(f"❌ {state['error']}")
        sys.exit(1)
    
    # 采集实时状态
    live = collect_live_state()
    
    # 仅对比模式
    if args.diff:
        diffs = diff_model_tables(state)
        if args.json:
            print(json.dumps({"diffs": diffs, "state_models": len(state["model_table"])}, ensure_ascii=False, indent=2))
        else:
            print(f"🧬 STATE.md模型: {len(state['model_table'])}个")
            print(f"📋 差异: {len(diffs)}条")
            for d in diffs:
                print(f"  {d}")
        return
    
    # 全量或live-only
    result = update_memory_md(live, state, dry_run=args.dry_run)
    
    if args.json:
        output = {
            "state_updated": state["updated"],
            "live": live,
            "result": result,
            "model_diffs": diff_model_tables(state),
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"🔄 龍魂·记忆状态同步器 v1.0")
        print(f"━━━━━━━━━━━━━━━━━━━━")
        print(f"📅 STATE.md 更新: {state['updated']}")
        print(f"⚡ 快速状态卡: {len(state['quick_status'])}项")
        print(f"🤖 STATE模型表: {len(state['model_table'])}个模型")
        print(f"")
        print(f"💻 实时系统状态:")
        print(f"  电源: {live['power']}")
        print(f"  磁盘: {live['disk']['avail']} 可用 / {live['disk']['total']} ({live['disk']['used_pct']})")
        print(f"  Ollama: {live['ollama_models']}个模型 · 激活: {live['active_model']}")
        print(f"  鲲鹏: {'🟢 连通' if live['kunpeng_connected'] else '🔴 不通'}")
        print(f"  Git: {live['git']['staged']}暂存 + {live['git']['modified']}修改 + {live['git']['untracked']}未跟踪")
        print(f"")
        
        if args.dry_run:
            print(f"🔍 [DRY-RUN] 未实际写入文件")
        else:
            print(f"✅ 实时快照已写入 MEMORY.md")
        
        # 差异报告
        diffs = diff_model_tables(state)
        if diffs:
            print(f"\n⚠️ STATE.md与MEMORY.md模型表差异 ({len(diffs)}条):")
            for d in diffs:
                print(f"  {d}")

if __name__ == "__main__":
    main()
