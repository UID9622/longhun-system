# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 Agent 编排器 v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
P1 · 技能自动发现 · 事件路由 · 多 Agent 协作
DNA: #龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-AGENT-ORCHESTRATOR-v1.0-UID9622
"""

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import yaml

# ─── 常量 ───
HOME = Path.home()
LONGHUN_DIR = HOME / ".longhun"
ORCH_DIR = LONGHUN_DIR / "agent_orchestrator"
SKILL_INDEX = ORCH_DIR / "skill_index.json"
ROUTE_LOG = ORCH_DIR / "route_log.jsonl"
PERSONA_REGISTRY = Path(__file__).resolve().parent / "persona_registry.json"

SKILL_PATHS = [
    HOME / ".kimi-code" / "skills",
    HOME / ".agents" / "skills",
]

# ─── 工具函数 ───
def ensure_dirs():
    ORCH_DIR.mkdir(parents=True, exist_ok=True)


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def load_json(path: Path) -> Any:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: Any):
    ensure_dirs()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def append_jsonl(path: Path, data: dict):
    ensure_dirs()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def parse_skill_md(path: Path) -> dict | None:
    """解析 SKILL.md 的 YAML frontmatter"""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if not text.startswith("---"):
            return None
        parts = text.split("---", 2)
        if len(parts) < 3:
            return None
        meta = yaml.safe_load(parts[1]) or {}
        if not isinstance(meta, dict):
            return None
        return {
            "id": meta.get("id") or meta.get("name") or path.parent.name,
            "name": meta.get("name", path.parent.name),
            "description": meta.get("description", ""),
            "category": meta.get("metadata", {}).get("category", ""),
            "keywords": _extract_keywords(meta),
            "path": str(path.parent),
            "skill_file": str(path),
            "scope": _detect_scope(path),
            "discovered_at": now_iso(),
        }
    except Exception as e:
        return {
            "id": path.parent.name,
            "name": path.parent.name,
            "description": f"解析失败: {e}",
            "category": "unknown",
            "keywords": [],
            "path": str(path.parent),
            "skill_file": str(path),
            "scope": "local",
            "discovered_at": now_iso(),
            "parse_error": str(e),
        }


def _extract_keywords(meta: dict) -> list:
    keys = []
    for k in ["trigger_keywords", "keywords", "triggers"]:
        v = meta.get(k) or meta.get("metadata", {}).get(k)
        if v:
            if isinstance(v, list):
                keys.extend(v)
            elif isinstance(v, str):
                keys.append(v)
    # 从 name / description 提取候选词
    text = f"{meta.get('name','')} {meta.get('description','')}"
    # 保留 4 字以上中文词或 3 字母以上英文词
    cn = re.findall(r"[\u4e00-\u9fff]{2,}", text)
    en = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}", text)
    keys.extend(cn)
    keys.extend(en)
    return list(dict.fromkeys([k.strip() for k in keys if k.strip()]))[:120]


def _detect_scope(path: Path) -> str:
    p = str(path)
    if ".agents/skills" in p:
        return "agent"
    if ".kimi-code/skills" in p:
        return "kimi"
    return "local"


def load_personas() -> list:
    data = load_json(PERSONA_REGISTRY)
    return data.get("personas", [])


def load_skill_index() -> dict:
    return load_json(SKILL_INDEX)


# ─── 子命令实现 ───
def cmd_discover(args):
    """扫描技能目录，生成索引"""
    ensure_dirs()
    skills = []
    for base in SKILL_PATHS:
        if not base.exists():
            continue
        for skill_dir in sorted(base.iterdir()):
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                info = parse_skill_md(skill_md)
                if info:
                    skills.append(info)
    index = {
        "version": "1.0",
        "dna": "#龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-SKILL-INDEX-v1.0-UID9622",
        "generated_at": now_iso(),
        "total": len(skills),
        "sources": [str(p) for p in SKILL_PATHS],
        "skills": skills,
    }
    save_json(SKILL_INDEX, index)
    print(f"🐉 技能自动发现完成")
    print(f"   扫描路径: {len(SKILL_PATHS)} 个")
    print(f"   发现技能: {len(skills)} 个")
    print(f"   索引落盘: {SKILL_INDEX}")
    if args.json:
        print(json.dumps(index, ensure_ascii=False, indent=2))
    return 0


def cmd_list(args):
    """列出已发现技能"""
    index = load_skill_index()
    skills = index.get("skills", [])
    if args.scope:
        skills = [s for s in skills if s.get("scope") == args.scope]
    if args.keyword:
        skills = [s for s in skills if args.keyword.lower() in json.dumps(s, ensure_ascii=False).lower()]
    print(f"🐉 已发现技能 ({len(skills)} 个)")
    for s in skills[: args.limit]:
        print(f"  · {s.get('id')} [{s.get('scope')}] {s.get('category')}")
        print(f"    {s.get('description', '')[:80]}...")
    return 0


def cmd_route(args):
    """将输入路由到最佳技能和人格"""
    index = load_skill_index()
    personas = load_personas()
    text = args.text or " ".join(args.extra or [])
    if not text:
        print("❌ 请提供 --text 或位置参数")
        return 1

    matches = _match_skills(index.get("skills", []), text)
    persona_matches = _match_personas(personas, text)

    result = {
        "timestamp": now_iso(),
        "input": text,
        "top_skills": matches[:5],
        "top_personas": persona_matches[:3],
        "recommended_action": _recommend(matches, persona_matches),
    }
    append_jsonl(ROUTE_LOG, result)

    print(f"🐉 路由结果")
    print(f"   输入: {text[:80]}")
    print(f"   推荐动作: {result['recommended_action']}")
    print(f"   匹配技能 Top{len(result['top_skills'])}:")
    for m in result["top_skills"]:
        print(f"      · {m['id']} (score={m['score']:.2f}) [{m['scope']}]")
    print(f"   匹配人格 Top{len(result['top_personas'])}:")
    for m in result["top_personas"]:
        print(f"      · {m['ipa']} {m['name']} (score={m['score']:.2f}) · {m['func']}")
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _match_skills(skills: list, text: str) -> list:
    text_lower = text.lower()
    scored = []
    for s in skills:
        score = 0.0
        desc = f"{s.get('description', '')} {s.get('category', '')}"
        # 关键词命中
        for kw in s.get("keywords", []):
            kwl = kw.lower()
            if kwl in text_lower:
                score += 2.0 if len(kwl) >= 4 else 1.0
        # 描述语义模糊匹配
        for word in re.findall(r"[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}", text):
            if word.lower() in desc.lower():
                score += 0.5
        if score > 0:
            scored.append({**s, "score": round(score, 2)})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored


def _match_personas(personas: list, text: str) -> list:
    text_lower = text.lower()
    scored = []
    # 人格分组关键词映射
    group_hints = {
        "战略组": ["战略", "规划", "统筹", "推演", "路径", "决策", "布局"],
        "执行组": ["执行", "代码", "部署", "写", "实现", "落地", "构建", "开发", "脚本"],
        "守护组": ["守护", "审计", "合规", "铁律", "法律", "审判", "规则", "监督"],
        "文化组": ["文化", "历史", "文明", "存档", "翻译", "语义", "伦理", "价值观"],
        "安全组": ["安全", "防御", "攻击", "渗透", "红队", "漏洞", "加密", "保护"],
        "子系统": ["系统", "模块", "引擎", "框架", "总线"],
        "合规组": ["合规", "法律", "监管", "制裁", "隐私", "gdpr"],
        "文明组": ["文明", "历史", "档案", "存证", "敦煌", "丝绸之路"],
        "实验组": ["实验", "沙盒", "测试", "混沌"],
    }
    for p in personas:
        score = 0.0
        name = p.get("name", "")
        func = p.get("func", "")
        group = p.get("group", "")
        protocol = p.get("protocol", "")
        corpus = f"{name} {func} {group} {protocol}".lower()
        # 直接命中人格名或功能词
        for word in re.findall(r"[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}", text):
            wl = word.lower()
            if wl in name.lower() or wl in func.lower():
                score += 2.0
            elif wl in corpus:
                score += 0.5
        # 分组暗示
        for g, hints in group_hints.items():
            if group == g or g in corpus:
                for h in hints:
                    if h in text_lower:
                        score += 1.0
        if score > 0:
            scored.append({**p, "score": round(score, 2)})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored


def _recommend(skills: list, personas: list) -> str:
    if not skills:
        return "无匹配技能，建议人工介入或扩充索引"
    top_skill = skills[0]
    top_persona = personas[0] if personas else None
    if top_persona:
        return f"触发 {top_persona['ipa']} {top_persona['name']} 调用 {top_skill['id']}"
    return f"触发 {top_skill['id']}（未匹配到人格）"


def cmd_run(args):
    """执行推荐技能（治理流水线包装）"""
    index = load_skill_index()
    skills = index.get("skills", [])
    matches = _match_skills(skills, args.text)
    if not matches:
        print(f"❌ 未找到匹配技能: {args.text}")
        return 1
    target = matches[0]
    print(f"🐉 将执行技能: {target['id']}")
    print(f"   路径: {target['path']}")
    print(f"   描述: {target['description'][:100]}...")

    # v1: 优先调用 skill 目录下的 scripts/run.py 或 scripts/<id>.py
    scripts_dir = Path(target["path"]) / "scripts"
    candidates = []
    if scripts_dir.exists():
        candidates = list(scripts_dir.glob("*.py"))
    if candidates:
        script = str(candidates[0])
        cmd = f"python3 {script}"
        if args.args:
            cmd += " " + " ".join(args.args)
    else:
        # fallback: 通过 Skill 工具调用（仅记录建议）
        cmd = f"echo '建议调用 Skill: {target['id']}'"

    # 包装为治理流水线执行
    gov_cmd = [
        sys.executable, str(Path(__file__).resolve().parent / "lh_governed_exec.py"),
        "--cmd", cmd,
        "--desc", f"Agent编排器触发: {target['id']} - {args.text}",
        "--uid", args.uid or "UID9622",
        "--topic", "skill.execution",
    ]
    if args.dry_run:
        print(f"   [dry-run] {' '.join(gov_cmd)}")
        return 0
    return subprocess.call(gov_cmd)


def cmd_listen(args):
    """监听事件总线，自动路由"""
    print(f"🐉 Agent 编排器监听模式启动 (topic={args.topic}, interval={args.interval}s)")
    print("   按 Ctrl+C 停止")
    bus_script = Path(__file__).resolve().parent / "lh_event_bus.py"

    # 先注册订阅
    sub_result = subprocess.run(
        [sys.executable, str(bus_script), "subscribe", "--skill", args.subscriber,
         "--topic", args.topic, "--type", "*"],
        capture_output=True, text=True, encoding="utf-8", errors="ignore"
    )
    if sub_result.returncode == 0:
        print(f"   订阅已注册: {args.subscriber} / {args.topic}")

    while True:
        try:
            # 消费事件（JSON 模式）
            result = subprocess.run(
                [sys.executable, str(bus_script), "consume", "--skill", args.subscriber,
                 "--limit", str(args.limit), "--json"],
                capture_output=True, text=True, encoding="utf-8", errors="ignore"
            )
            if result.returncode == 0 and result.stdout.strip():
                try:
                    data = json.loads(result.stdout.strip())
                    if isinstance(data, list):
                        for ev in data:
                            _handle_event(ev)
                    elif isinstance(data, dict) and "error" in data:
                        pass  # 无订阅等错误，静默
                except json.JSONDecodeError:
                    if result.stdout.strip():
                        print(result.stdout.strip())
            time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n👋 监听停止")
            break
    return 0


def _handle_event(ev: dict):
    topic = ev.get("topic", "")
    payload = ev.get("payload", {})
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            pass
    text = ""
    if isinstance(payload, dict):
        text = payload.get("text") or payload.get("query") or ""
    if not text:
        text = json.dumps(payload, ensure_ascii=False)
    print(f"\n📥 收到事件 #{ev.get('id')} topic={topic}")
    print(f"   payload: {text[:120]}")
    # 自动路由
    index = load_skill_index()
    matches = _match_skills(index.get("skills", []), text)
    if matches:
        top = matches[0]
        print(f"   🤖 自动路由 → {top['id']} (score={top['score']:.2f})")
        append_jsonl(ROUTE_LOG, {
            "timestamp": now_iso(),
            "event_id": ev.get("id"),
            "topic": topic,
            "routed_to": top["id"],
            "score": top["score"],
            "auto": True,
        })
    else:
        print(f"   ⚠️ 无匹配技能，事件挂起")


def cmd_stats(args):
    """统计索引与路由日志"""
    index = load_skill_index()
    total_skills = len(index.get("skills", []))
    scope_counts = {}
    for s in index.get("skills", []):
        scope_counts[s.get("scope", "unknown")] = scope_counts.get(s.get("scope", "unknown"), 0) + 1
    route_count = 0
    if ROUTE_LOG.exists():
        with open(ROUTE_LOG, "r", encoding="utf-8") as f:
            route_count = sum(1 for _ in f)
    stats = {
        "timestamp": now_iso(),
        "total_skills": total_skills,
        "scope_counts": scope_counts,
        "total_routes": route_count,
        "index_path": str(SKILL_INDEX),
        "route_log": str(ROUTE_LOG),
    }
    print(f"🐉 Agent 编排器统计")
    print(f"   技能总数: {total_skills}")
    print(f"   分域统计: {scope_counts}")
    print(f"   路由次数: {route_count}")
    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    return 0


# ─── CLI ───
def build_parser():
    p = argparse.ArgumentParser(description="🐉 龍魂 Agent 编排器 v1.0")
    sub = p.add_subparsers(dest="command")

    d = sub.add_parser("discover", help="扫描技能目录并生成索引")
    d.add_argument("--json", action="store_true", help="输出完整 JSON")

    l = sub.add_parser("list", help="列出已发现技能")
    l.add_argument("--scope", help="按 scope 过滤: kimi/agent/local")
    l.add_argument("--keyword", help="关键词过滤")
    l.add_argument("--limit", type=int, default=50)

    r = sub.add_parser("route", help="将输入路由到技能和人格")
    r.add_argument("--text", help="输入文本")
    r.add_argument("extra", nargs="*", help="位置参数文本")
    r.add_argument("--json", action="store_true", help="输出 JSON")

    run = sub.add_parser("run", help="执行推荐技能")
    run.add_argument("text", help="触发文本")
    run.add_argument("args", nargs="*", help="传给技能的额外参数")
    run.add_argument("--uid", default="UID9622", help="执行主体 UID")
    run.add_argument("--dry-run", action="store_true", help="只打印不执行")

    listen = sub.add_parser("listen", help="监听事件总线并自动路由")
    listen.add_argument("--topic", default="#", help="订阅 topic")
    listen.add_argument("--subscriber", default="agent-orchestrator", help="订阅者 ID")
    listen.add_argument("--interval", type=int, default=5, help="轮询间隔秒")
    listen.add_argument("--limit", type=int, default=10, help="单次消费条数")

    s = sub.add_parser("stats", help="统计索引与路由日志")
    s.add_argument("--json", action="store_true", help="输出 JSON")

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0
    ensure_dirs()
    handlers = {
        "discover": cmd_discover,
        "list": cmd_list,
        "route": cmd_route,
        "run": cmd_run,
        "listen": cmd_listen,
        "stats": cmd_stats,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
