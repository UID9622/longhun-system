#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 技能调度器 v1.0
Skill Scheduler — 技能"遥控器"

核心思想（2026-08-16 老大定调）：
  技能用完就该"沉默"，下次用再"唤醒"——不常驻、不浪费电脑算力。
  技能本质是文件（.md/.skill/.json 定义），天生"用才读、读完释放"。
  本调度器负责：① 列出全部技能+活跃状态 ② 手动唤醒/休眠 ③ 标记自动休眠闲置技能。

用法:
  lh skill              # 等价 lh skill status
  lh skill list         # 列出全部技能+状态
  lh skill status       # 当前活跃技能
  lh skill wake <名>    # 唤醒技能（标记活跃）
  lh skill sleep <名>   # 休眠技能（标记休眠·释放）
  lh skill autosleep    # 自动休眠超过阈值未用的技能
  lh skill stats        # 调度统计（唤醒/休眠次数·CPU估算）

DNA: #龍芯⚡️丙午·丙申·壬戌·巳时-SKILL-SCHEDULER-v1.0
协议: CC BY-NC-SA 4.0（核心思想层）· 工程实现 MulanPSL v2
创建者: 诸葛鑫（UID9622）
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIRS = [
    ROOT / "skills",
    ROOT / "02_SKILLS",
    ROOT / "02_技能庫",
]
# bin/ 下的引擎脚本也算技能（lh_*.py 引擎），统一纳入调度
ENGINE_DIRS = [ROOT / "bin"]
STATE_FILE = Path.home() / ".longhun" / "skill_scheduler_state.json"

# 技能活跃状态的TTL（小时）：超过未使用自动休眠
DEFAULT_IDLE_TTL_HOURS = 24
# 常驻服务技能（保持活跃，勿休眠）—— 安全/守护类
ALWAYS_ON = {"防篡改", "自愈", "熔断", "审计", "时间戳", "GPG签章", "德本审计", "主动观察"}


def _load_state() -> Dict:
    """加载调度状态"""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "version": "1.0",
        "skills": {},      # 技能名 -> {status: active/sleep, last_use: ts, wake_count, sleep_count}
        "stats": {"total_wake": 0, "total_sleep": 0, "created": time.time()},
    }


def _save_state(state: Dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def scan_skills() -> List[Dict]:
    """扫描全部技能定义文件"""
    found = {}
    for sdir in SKILL_DIRS:
        if not sdir.exists():
            continue
        for f in sorted(sdir.rglob("*")):
            if f.suffix.lower() not in (".md", ".skill", ".json"):
                continue
            # 跳过 __pycache__ 与索引文件
            if "__pycache__" in str(f) or f.name.startswith("__"):
                continue
            name = _skill_name(f)
            if not name:
                continue
            if name not in found:
                found[name] = {
                    "name": name,
                    "path": str(f.relative_to(ROOT)),
                    "kind": f.suffix.lstrip("."),
                    "size_kb": round(f.stat().st_size / 1024, 1),
                }
    # bin/ 下的 lh_*.py 引擎脚本也算技能（统一可调度）
    for edir in ENGINE_DIRS:
        if not edir.exists():
            continue
        for f in sorted(edir.glob("lh_*.py")):
            if f.name in ("lh.py", "lh_skill_scheduler.py"):
                continue
            name = _skill_name(f)
            if not name or name in found:
                continue
            found[name] = {
                "name": name,
                "path": str(f.relative_to(ROOT)),
                "kind": "engine",
                "size_kb": round(f.stat().st_size / 1024, 1),
            }
    return list(found.values())


def _skill_name(f: Path) -> str:
    """从文件名提取技能名"""
    name = f.stem
    # 去掉 lh_ / longhun- 前缀
    name = re.sub(r"^(lh_|longhun[-_])", "", name)
    # 去掉版本号后缀 v1.0 等
    name = re.sub(r"[-_]?v?\d+\.\d+.*$", "", name)
    name = name.replace("-", " ").replace("_", " ").strip()
    if not name or len(name) < 2:
        return ""
    return name


def _is_always_on(name: str) -> bool:
    for kw in ALWAYS_ON:
        if kw in name:
            return True
    return False


def cmd_status(state: Dict) -> int:
    """显示当前状态"""
    print("\n🐉 龍魂 · 技能调度器")
    print("=" * 56)
    active = [n for n, s in state["skills"].items() if s["status"] == "active"]
    sleep = [n for n, s in state["skills"].items() if s["status"] == "sleep"]
    print(f"  活跃技能: {len(active)} 个")
    for n in active[:15]:
        print(f"    ✅ {n}")
    if len(active) > 15:
        print(f"    ... 等 {len(active) - 15} 个")
    print(f"  休眠技能: {len(sleep)} 个")
    print(f"  累计唤醒 {state['stats']['total_wake']} 次 · 休眠 {state['stats']['total_sleep']} 次")
    print(f"  状态文件: {STATE_FILE}")
    print("  用法: lh skill wake <名> | lh skill sleep <名> | lh skill list")
    return 0


def cmd_list(state: Dict) -> int:
    """列出全部技能+状态"""
    skills = scan_skills()
    print("\n📋 技能清单 (扫描 %d 个技能文件)" % len(skills))
    print("=" * 72)
    print(f"{'技能名':<24} {'状态':<8} {'类型':<6} {'大小':<7} 路径")
    print("-" * 72)
    active_count = 0
    for s in skills:
        st = state["skills"].get(s["name"], {}).get("status", "sleep")
        if st == "active":
            active_count += 1
        mark = "✅活跃" if st == "active" else "💤休眠"
        print(f"{s['name'][:22]:<24} {mark:<8} {s['kind']:<6} {s['size_kb']:<7} {s['path']}")
    print("-" * 72)
    print(f"共 {len(skills)} 个 · 活跃 {active_count} · 休眠 {len(skills) - active_count}")
    print("💡 技能为文件·用才读·默认不占内存。活跃标记仅用于调度追踪。")
    return 0


def cmd_wake(state: Dict, names: List[str]) -> int:
    """唤醒技能"""
    if not names:
        print("❌ 请指定技能名: lh skill wake <技能名>")
        return 1
    now = time.time()
    ok = 0
    for name in names:
        # 模糊匹配
        candidates = [n for n in _all_skill_names() if name.lower() in n.lower()]
        if not candidates:
            print(f"  ❌ 未找到技能: {name}")
            continue
        for c in candidates:
            s = state["skills"].setdefault(
                c, {"status": "sleep", "last_use": 0, "wake_count": 0, "sleep_count": 0}
            )
            if s["status"] != "active":
                s["status"] = "active"
                s["wake_count"] += 1
                state["stats"]["total_wake"] += 1
                print(f"  ✅ 唤醒: {c}")
            else:
                print(f"  ⏭️ 已在活跃: {c}")
            s["last_use"] = now
            ok += 1
    _save_state(state)
    return 0 if ok else 1


def cmd_sleep(state: Dict, names: List[str]) -> int:
    """休眠技能"""
    if not names:
        print("❌ 请指定技能名: lh skill sleep <技能名>")
        return 1
    ok = 0
    for name in names:
        candidates = [n for n in _all_skill_names() if name.lower() in n.lower()]
        if not candidates:
            print(f"  ❌ 未找到技能: {name}")
            continue
        for c in candidates:
            if _is_always_on(c):
                print(f"  🔒 常驻技能不可休眠: {c}")
                continue
            s = state["skills"].setdefault(
                c, {"status": "sleep", "last_use": 0, "wake_count": 0, "sleep_count": 0}
            )
            if s["status"] != "sleep":
                s["status"] = "sleep"
                s["sleep_count"] += 1
                state["stats"]["total_sleep"] += 1
                print(f"  💤 休眠: {c}")
            else:
                print(f"  ⏭️ 已休眠: {c}")
            ok += 1
    _save_state(state)
    return 0 if ok else 1


def cmd_autosleep(state: Dict, ttl_hours: float = DEFAULT_IDLE_TTL_HOURS) -> int:
    """自动休眠闲置技能"""
    now = time.time()
    idle_count = 0
    for name, s in state["skills"].items():
        if s.get("status") != "active":
            continue
        if _is_always_on(name):
            continue
        last = s.get("last_use", 0)
        if last and (now - last) > ttl_hours * 3600:
            s["status"] = "sleep"
            s["sleep_count"] += 1
            state["stats"]["total_sleep"] += 1
            idle_count += 1
            print(f"  💤 自动休眠(闲置>{ttl_hours:.0f}h): {name}")
    _save_state(state)
    if idle_count:
        print(f"✅ 已自动休眠 {idle_count} 个闲置技能")
    else:
        print(f"✅ 无闲置技能（阈值 {ttl_hours:.0f}h）")
    return 0


def cmd_stats(state: Dict) -> int:
    """调度统计"""
    created = state["stats"].get("created", time.time())
    days = (time.time() - created) / 86400
    print("\n📊 技能调度统计")
    print("=" * 56)
    print(f"  调度器创建: {datetime.fromtimestamp(created).strftime('%Y-%m-%d')}")
    print(f"  已运行: {days:.1f} 天")
    print(f"  累计唤醒: {state['stats']['total_wake']} 次")
    print(f"  累计休眠: {state['stats']['total_sleep']} 次")
    print(f"  当前活跃: {sum(1 for s in state['skills'].values() if s['status']=='active')} 个")
    print(f"  当前休眠: {sum(1 for s in state['skills'].values() if s['status']=='sleep')} 个")
    print("  💡 技能为文件·用才读·不常驻不占内存")
    return 0


def _all_skill_names() -> List[str]:
    return [s["name"] for s in scan_skills()]


def main():
    args = sys.argv[1:]
    state = _load_state()

    if not args or args[0] in ("status", "-s"):
        return cmd_status(state)

    sub = args[0].lstrip("-")
    rest = args[1:]

    if sub in ("list", "ls", "-l"):
        return cmd_list(state)
    elif sub in ("wake", "on", "w"):
        return cmd_wake(state, rest)
    elif sub in ("sleep", "off", "s"):
        return cmd_sleep(state, rest)
    elif sub in ("autosleep", "auto"):
        ttl = float(rest[0]) if rest and rest[0].replace(".", "", 1).isdigit() else DEFAULT_IDLE_TTL_HOURS
        return cmd_autosleep(state, ttl)
    elif sub in ("stats", "stat"):
        return cmd_stats(state)
    elif sub in ("help", "-h", "--help"):
        print(__doc__)
        return 0
    else:
        print(f"❌ 未知子命令: {sub}")
        print(__doc__.split("用法:")[1].split("DNA:")[0].strip())
        return 1


if __name__ == "__main__":
    sys.exit(main())
