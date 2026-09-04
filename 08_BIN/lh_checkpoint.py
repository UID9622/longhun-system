#!/usr/bin/env python3
# 🛡️ P0焊死(2026-09-04·P72加封): 任务断点引擎·源码修改须走三色治理v2.1 §十二门槛
# DNA: #龍芯⚡️2026-09-04-TASK-CHECKPOINT-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂·任务断点恢复 v1.0 — lh checkpoint save|list|resume|done|drop
需求2: 任务中断自动记断点(执行到哪/已产出什么/下一步)·下次从中断处续(老大 2026-09-04 指令)。
数据: ~/.longhun/checkpoints/<任务名>.json
用法(AI 在任务里程碑/中断前调用):
  lh checkpoint save <任务名> [--step "已完成步骤摘要"] [--next "下一步"]
                     [--artifacts "产出文件1,文件2"] [--ctx "上下文要点/决策"] [--name 别名]
  lh checkpoint list [--all]          → 列出断点(默认只看未完成)
  lh checkpoint resume <任务名>       → 从中断处继续(打印全文·计数+1)
  lh checkpoint done <任务名>         → 标记完成
  lh checkpoint drop <任务名> [--force] → 删除断点
自动接线(lh.py): 会话有 running/pending 断点时 status 摘要会提醒续接。
"""
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

CP_DIR = Path.home() / ".longhun" / "checkpoints"


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _path(name: str) -> Path:
    safe = name.replace("/", "_").replace(" ", "_")[:60]
    return CP_DIR / f"{safe}.json"


def cmd_save(argv: list) -> int:
    name = ""
    step = nxt = artifacts = ctx = ""
    i = 0
    while i < len(argv):
        a = argv[i]
        if not a.startswith("-") and not name:
            name = a
        elif a == "--step" and i + 1 < len(argv):
            step, i = argv[i + 1], i + 2
        elif a == "--next" and i + 1 < len(argv):
            nxt, i = argv[i + 1], i + 2
        elif a == "--artifacts" and i + 1 < len(argv):
            artifacts, i = argv[i + 1], i + 2
        elif a == "--ctx" and i + 1 < len(argv):
            ctx, i = argv[i + 1], i + 2
        else:
            i += 1
    if not name:
        print("  ❌ 用法: lh checkpoint save <任务名> [--step ...] [--next ...] [--artifacts ...] [--ctx ...]")
        return 1
    CP_DIR.mkdir(parents=True, exist_ok=True)
    fp = _path(name)
    old = {}
    if fp.exists():
        try:
            old = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            old = {}
    done_steps = old.get("done_steps", [])
    if step and (not done_steps or done_steps[-1] != step):
        done_steps.append(step)
    data = {
        "name": name,
        "status": old.get("status", "pending"),
        "done_steps": done_steps,
        "next_step": nxt or old.get("next_step", ""),
        "artifacts": artifacts or old.get("artifacts", ""),
        "ctx": ctx or old.get("ctx", ""),
        "created_at": old.get("created_at", _now()),
        "updated_at": _now(),
        "resume_count": old.get("resume_count", 0),
        "done_at": old.get("done_at", ""),
    }
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✅ 断点已保存: {name} ({data['status']}·已完成 {len(done_steps)} 步)")
    if nxt:
        print(f"  📍 下一步: {nxt}")
    return 0


def cmd_list(all_flag: bool = False) -> int:
    if not CP_DIR.exists():
        print("  ℹ️  无任何断点 (lh checkpoint save <任务名> 创建)")
        return 0
    files = sorted(CP_DIR.glob("*.json"))
    rows = []
    for f in files:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        rows.append(d)
    if not all_flag:
        rows = [d for d in rows if d.get("status") != "done"]
    print(f"🐉 任务断点({'全部' if all_flag else '未完成'}·{len(rows)}个)\n" + "=" * 46)
    for d in rows:
        mark = {"done": "✅", "running": "▶️", "pending": "⏸️"}.get(d.get("status"), "⏸️")
        done_n = len(d.get("done_steps", []))
        print(f"  {mark} {d['name']} · {done_n}步 · 更新{d.get('updated_at','')[:16]}")
        if d.get("next_step"):
            print(f"      📍 {d['next_step'][:80]}")
    return 0


def cmd_resume(name: str) -> int:
    fp = _path(name)
    if not fp.exists():
        print(f"  ❌ 无此断点: {name} (lh checkpoint list 查看)")
        return 1
    d = json.loads(fp.read_text(encoding="utf-8"))
    d["status"] = "running"
    d["resume_count"] = int(d.get("resume_count", 0)) + 1
    d["updated_at"] = _now()
    fp.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"🐉 断点续接: {name} (第{d['resume_count']}次 resume)\n" + "=" * 46)
    if d.get("done_steps"):
        print("  ✅ 已执行:")
        for s in d["done_steps"]:
            print(f"     · {s[:100]}")
    if d.get("next_step"):
        print(f"  📍 下一步(接着干): {d['next_step']}")
    if d.get("artifacts"):
        print(f"  📦 已产出: {d['artifacts']}")
    if d.get("ctx"):
        print(f"  🧠 上下文: {d['ctx'][:200]}")
    return 0


def cmd_done(name: str) -> int:
    fp = _path(name)
    if not fp.exists():
        print(f"  ❌ 无此断点: {name}")
        return 1
    d = json.loads(fp.read_text(encoding="utf-8"))
    d["status"] = "done"
    d["done_at"] = _now()
    d["updated_at"] = _now()
    fp.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✅ 断点已完结: {name}")
    return 0


def cmd_drop(argv: list) -> int:
    name = next((a for a in argv if not a.startswith("-")), "")
    if not name:
        print("  ❌ 用法: lh checkpoint drop <任务名> [--force]")
        return 1
    fp = _path(name)
    if not fp.exists():
        print(f"  ❌ 无此断点: {name}")
        return 1
    if "--force" not in argv:
        print(f"  ⚠️ 确认删除断点 {name}? 加 --force 确认")
        return 1
    fp.unlink()
    print(f"  ✅ 断点已删除: {name}")
    return 0


def main() -> int:
    argv = sys.argv[1:] or ["list"]
    cmd = argv[0]
    rest = argv[1:]
    if cmd == "save":
        return cmd_save(rest)
    if cmd == "list":
        return cmd_list("--all" in rest)
    if cmd == "resume":
        name = next((a for a in rest if not a.startswith("-")), "")
        return cmd_resume(name) if name else (print("  ❌ 用法: lh checkpoint resume <任务名>"), 1)[1]
    if cmd == "done":
        name = next((a for a in rest if not a.startswith("-")), "")
        return cmd_done(name) if name else (print("  ❌ 用法: lh checkpoint done <任务名>"), 1)[1]
    if cmd == "drop":
        return cmd_drop(rest)
    print("用法: lh checkpoint save|list [--all]|resume|done|drop <任务名> [--force]")
    return 1


if __name__ == "__main__":
    sys.exit(main())
