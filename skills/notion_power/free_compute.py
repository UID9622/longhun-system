#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notion 免费算力 · 四用法落地
DNA: #龍芯⚡2026-05-19-NOTION-FREE-COMPUTE-v1.0

原则: Notion 只存/展示 · 计算在本机 Python · 0 LLM · 0 美金
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import date, datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO = Path(__file__).resolve().parents[2]
_SKILLS = _REPO / "skills"
if str(_SKILLS) not in sys.path:
    sys.path.insert(0, str(_SKILLS))

NOTION_VERSION = "2022-06-28"
TZ7 = timezone(timedelta(hours=7))


def _load_config() -> Dict[str, Any]:
    cfg: Dict[str, Any] = {
        "export_dir": "数据/notion_export",
        "local": {
            "dict_json": "data/tongxinyi_dict.json",
            "execute_trace": "日志/execute_trace.jsonl",
            "identity_audit": "日志/identity_audit.jsonl",
        },
        "databases": {},
    }
    for name in ("config.json", "config/notion_power.json"):
        p = _REPO / name
        if not p.exists():
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if name == "config.json":
                if data.get("notion_token") and "你的" not in str(data.get("notion_token", "")):
                    cfg["notion_token"] = data["notion_token"]
                if data.get("notion_database_id"):
                    cfg.setdefault("databases", {})["tongxinyi_dict"] = data["notion_database_id"]
            else:
                cfg.update({k: data[k] if k in data else cfg.get(k) for k in data})
                if "databases" in data:
                    cfg["databases"] = {**cfg.get("databases", {}), **data["databases"]}
                if "local" in data:
                    cfg["local"] = {**cfg.get("local", {}), **data["local"]}
        except (json.JSONDecodeError, OSError):
            pass
    token = os.environ.get("NOTION_TOKEN") or cfg.get("notion_token", "")
    cfg["notion_token"] = token
    return cfg


def _export_dir(cfg: Dict[str, Any]) -> Path:
    d = _REPO / cfg.get("export_dir", "数据/notion_export")
    d.mkdir(parents=True, exist_ok=True)
    return d


def _token_ok(cfg: Dict[str, Any]) -> bool:
    t = (cfg.get("notion_token") or "").strip()
    return bool(t) and "你的" not in t and t.startswith("secret_")


def _notion_request(cfg: Dict[str, Any], method: str, path: str, body: Optional[dict] = None) -> dict:
    url = f"https://api.notion.com/v1{path}"
    headers = {
        "Authorization": f"Bearer {cfg['notion_token']}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Notion API {e.code}: {err[:500]}") from e


# ── 用法 1 · 通心译字典 ─────────────────────────────────────────
def cmd_dict_export(cfg: Dict[str, Any], push: bool) -> Path:
    from on_translate.tongxinyi import TongxinYi

    dict_path = _REPO / cfg["local"]["dict_json"]
    t = TongxinYi(str(dict_path) if dict_path.exists() else None)
    rows = t.export_for_notion()
    stamp = date.today().isoformat()
    out = _export_dir(cfg)
    csv_path = out / f"tongxinyi_{stamp}.csv"
    md_path = out / f"tongxinyi_{stamp}.md"
    json_path = out / f"tongxinyi_{stamp}.json"

    fields = ["Chinese", "Context", "释义", "English", "Totem", "Warning"]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})

    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# 通心译字典 · Notion 导入 · {stamp}",
        "",
        "Notion → 新建 Database → 导入 CSV → 选 `tongxinyi_{}.csv`".format(stamp),
        "",
        "| Chinese | Context | 释义 | English | Totem | Warning |",
        "|---------|---------|------|---------|-------|---------|",
    ]
    for row in rows[:200]:
        lines.append(
            "| {Chinese} | {Context} | {释义} | {English} | {Totem} | {Warning} |".format(
                **{k: str(row.get(k, "")).replace("|", "\\|") for k in fields}
            )
        )
    if len(rows) > 200:
        lines.append(f"\n… 共 {len(rows)} 行 · 完整数据见 CSV/JSON")
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"🟢 用法1 · 导出 {len(rows)} 行")
    print(f"   CSV  → {csv_path}")
    print(f"   MD   → {md_path}")
    print(f"   JSON → {json_path}")

    db_id = (cfg.get("databases") or {}).get("tongxinyi_dict", "")
    if push and _token_ok(cfg) and db_id:
        pushed = _push_dict_to_notion(cfg, db_id, rows)
        print(f"   API  → 已推送 {pushed} 条到 Notion database")
    elif push:
        print("   🟡 API 跳过: 在 config.json 填 notion_token + notion_database_id，或 config/notion_power.json")
    else:
        print("   💡 手动: Notion 导入 CSV · 本机查询仍用 data/tongxinyi_dict.json（不调 API）")
    return csv_path


def _push_dict_to_notion(cfg: Dict[str, Any], database_id: str, rows: List[dict]) -> int:
    n = 0
    for row in rows:
        props = {
            "Chinese": {"title": [{"text": {"content": row.get("Chinese", "")[:2000]}}]},
            "Context": {"rich_text": [{"text": {"content": row.get("Context", "")}}]},
            "释义": {"rich_text": [{"text": {"content": row.get("释义", "")}}]},
            "English": {"rich_text": [{"text": {"content": row.get("English", "")}}]},
            "Totem": {"rich_text": [{"text": {"content": row.get("Totem", "")}}]},
            "Warning": {"rich_text": [{"text": {"content": row.get("Warning", "")}}]},
        }
        body = {"parent": {"database_id": database_id}, "properties": props}
        _notion_request(cfg, "POST", "/pages", body)
        n += 1
    return n


# ── 用法 2 · 执行日志看板 ─────────────────────────────────────────
def cmd_execute_board(cfg: Dict[str, Any], lines_n: int) -> Path:
    log_path = _REPO / cfg["local"]["execute_trace"]
    events: List[dict] = []
    if log_path.exists():
        for line in log_path.read_text(encoding="utf-8").splitlines()[-lines_n:]:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    colors = Counter()
    states = Counter()
    for ev in events:
        ar = ev.get("audit_result") or {}
        if isinstance(ar, dict) and ar.get("color"):
            colors[ar["color"]] += 1
        states[ev.get("state") or ev.get("event", "?")] += 1

    now = datetime.now(TZ7).strftime("%Y-%m-%d %H:%M %Z")
    stamp = date.today().isoformat()
    md = [
        f"# 龍魂执行看板 · {stamp}",
        f"",
        f"生成: {now} · 本机 `日志/execute_trace.jsonl` · **0 LLM**",
        f"",
        f"## 摘要",
        f"- 采样: 最近 **{len(events)}** 条",
        f"- 事件类型: {dict(states)}",
        f"- 五色分布: {dict(colors) if colors else '（无审计色·或日志为 enqueue 级）'}",
        f"",
        f"## 明细（最近 {min(20, len(events))} 条）",
        f"",
        "| 时间 | 事件 | 任务 | 状态 |",
        "|------|------|------|------|",
    ]
    for ev in events[-20:]:
        ts = ev.get("ts", ev.get("timestamp", ""))
        md.append(
            f"| {ts} | {ev.get('event','')} | {ev.get('task_name', ev.get('name',''))} | {ev.get('state','')} |"
        )
    md.append("")
    md.append("---")
    md.append("复制本页到 Notion 看板 · 或 `notion execute-board --push-page`（需 parent_page id）")

    out = _export_dir(cfg) / f"execute_board_{stamp}.md"
    out.write_text("\n".join(md), encoding="utf-8")
    print(f"🟢 用法2 · 执行看板 → {out}")
    return out


# ── 用法 3 · 身份审计链 ─────────────────────────────────────────
def cmd_identity_board(cfg: Dict[str, Any], lines_n: int, snapshot: bool) -> Path:
    log_path = _REPO / cfg["local"]["identity_audit"]
    log_path.parent.mkdir(parents=True, exist_ok=True)

    if snapshot:
        from on_identity.identity_verify import verify_identity, MASTER_CONFIRM, MASTER_GPG

        r = verify_identity(
            confirm_token=MASTER_CONFIRM,
            gpg_fp=MASTER_GPG,
            uid_claim="UID9622",
            text_to_check="龍魂小世界",
            behavior_samples=["短句", "跳跃", "CONFIRM"],
        )
        entry = {
            "ts": datetime.now(TZ7).isoformat(),
            "event": "snapshot",
            "is_valid": r.is_valid,
            "is_master": r.is_master,
            "score": r.score,
            "yaml": r.to_yaml(),
        }
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"🟢 已写入身份快照 → {log_path}")

    events: List[dict] = []
    if log_path.exists():
        for line in log_path.read_text(encoding="utf-8").splitlines()[-lines_n:]:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    stamp = date.today().isoformat()
    md = [
        f"# 身份审计链 · {stamp}",
        "",
        "永久档案 · 主控登录/拒绝/快照 · 复制到 Notion",
        "",
    ]
    for ev in events[-10:]:
        md.append(f"## {ev.get('ts', '')} · {ev.get('event', '')}")
        md.append(f"- valid={ev.get('is_valid')} master={ev.get('is_master')} score={ev.get('score')}")
        if ev.get("yaml"):
            md.append("```yaml")
            md.append(ev["yaml"])
            md.append("```")
        md.append("")

    if not events:
        md.append("（暂无留痕 · 运行 `notion identity-board --snapshot` 生成首条）")

    out = _export_dir(cfg) / f"identity_audit_{stamp}.md"
    out.write_text("\n".join(md), encoding="utf-8")
    print(f"🟢 用法3 · 身份审计 → {out}")
    return out


# ── 用法 4 · Kanban 拉取 / 回写 ─────────────────────────────────
def cmd_kanban_pull(cfg: Dict[str, Any], out_json: Optional[Path]) -> Path:
    db_id = (cfg.get("databases") or {}).get("kanban_tasks", "")
    stamp = date.today().isoformat()
    out = out_json or (_export_dir(cfg) / f"kanban_tasks_{stamp}.json")

    if not _token_ok(cfg) or not db_id:
        # 离线模板
        template = {
            "_hint": "填 config/notion_power.json → databases.kanban_tasks + notion_token 后重跑",
            "dna": "#龍芯⚡2026-05-19-KANBAN-DEMO-v1.0",
            "tasks": [
                {
                    "id": "local-demo-1",
                    "name": "示例任务",
                    "dna": "#龍芯⚡2026-05-19-KANBAN-DEMO-v1.0",
                    "factors": {
                        "sharpness": 0.3,
                        "long_term": 0.3,
                        "density": 0.2,
                        "absence": 0.7,
                        "pleasing": 0.6,
                    },
                    "context": {},
                    "triadic": {"heaven": 0.8, "earth": 0.8, "human": 0.8},
                }
            ],
        }
        out.write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"🟡 用法4 · 无 API · 已写离线模板 → {out}")
        return out

    body = {"page_size": 50}
    data = _notion_request(cfg, "POST", f"/databases/{db_id}/query", body)
    tasks = []
    for page in data.get("results", []):
        props = page.get("properties", {})
        title = ""
        for v in props.values():
            if v.get("type") == "title" and v.get("title"):
                title = v["title"][0].get("plain_text", "")
                break
        tasks.append(
            {
                "notion_page_id": page["id"],
                "name": title or "untitled",
                "factors": {},
                "context": {"notion_url": page.get("url", "")},
            }
        )
    payload = {"pulled_at": datetime.now(TZ7).isoformat(), "tasks": tasks}
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"🟢 用法4 · 拉取 {len(tasks)} 张卡片 → {out}")
    return out


def cmd_kanban_run(cfg: Dict[str, Any], tasks_file: Path) -> None:
    from on_execute.execute_router import ExecuteRouter, Task
    from dna_gate import require_dna

    data = json.loads(tasks_file.read_text(encoding="utf-8"))
    router = ExecuteRouter()
    for i, item in enumerate(data.get("tasks", [])):
        ctx = dict(item.get("context") or {})
        if not ctx.get("dna"):
            ctx["dna"] = item.get("dna") or data.get("dna")
        gate = require_dna(ctx, actor=f"kanban:{i}")
        if not gate.ok:
            print(f"🔴 任务 {i} 拒绝: {gate.reason}")
            continue
        item["context"] = ctx
        tid = item.get("id") or item.get("notion_page_id") or f"kn-{i}"
        router.enqueue(
            Task(
                id=str(tid),
                name=item.get("name", "notion-task"),
                factors=item.get("factors") or {
                    "sharpness": 0.3,
                    "long_term": 0.3,
                    "density": 0.2,
                    "absence": 0.7,
                    "pleasing": 0.6,
                },
                context=item.get("context") or {},
                triadic=item.get("triadic"),
            )
        )
    while router.queue:
        router.execute_one()
    print(f"🟢 Kanban 执行完成 · history={len(router.history)} · 留痕见日志/execute_trace.jsonl")


def cmd_all_export(cfg: Dict[str, Any]) -> None:
    cmd_dict_export(cfg, push=False)
    print()
    cmd_execute_board(cfg, 50)
    print()
    cmd_identity_board(cfg, 20, snapshot=True)
    print()
    cmd_kanban_pull(cfg, None)
    print()
    print("🐉 四用法导出完成 · 见 数据/notion_export/ · 0 LLM · 0 美金")


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Notion 免费算力 · 本机算·Notion存")
    sub = p.add_subparsers(dest="cmd", required=True)

    d1 = sub.add_parser("dict-export", help="用法1·通心译→CSV/MD")
    d1.add_argument("--push", action="store_true", help="token+database_id 齐全时 API 推送")

    d2 = sub.add_parser("execute-board", help="用法2·执行日志看板 MD")
    d2.add_argument("--lines", type=int, default=50)

    d3 = sub.add_parser("identity-board", help="用法3·身份审计 MD")
    d3.add_argument("--lines", type=int, default=20)
    d3.add_argument("--snapshot", action="store_true", help="先打一条本机快照")

    d4 = sub.add_parser("kanban-pull", help="用法4·拉任务 JSON")
    d4.add_argument("-o", "--output", type=Path, default=None)

    d5 = sub.add_parser("kanban-run", help="用法4·跑 kanban JSON 任务")
    d5.add_argument("tasks_file", type=Path)

    sub.add_parser("all", help="用法1-4 一次导出（不 push）")

    args = p.parse_args(argv)
    cfg = _load_config()

    if args.cmd == "dict-export":
        cmd_dict_export(cfg, args.push)
    elif args.cmd == "execute-board":
        cmd_execute_board(cfg, args.lines)
    elif args.cmd == "identity-board":
        cmd_identity_board(cfg, args.lines, args.snapshot)
    elif args.cmd == "kanban-pull":
        cmd_kanban_pull(cfg, args.output)
    elif args.cmd == "kanban-run":
        cmd_kanban_run(cfg, args.tasks_file)
    elif args.cmd == "all":
        cmd_all_export(cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
