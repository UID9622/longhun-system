#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·申时·䷔噬嗑-SKILL-BIRTH-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·专家自进化·技能出生流水线 v1.0（北辰架构「专家自生长」最小实现）
读取自动学习场景报告(auto-learned) → 高价值场景生成技能草案 → 登记待审 → P13 审核 promote 生效。

用法:
  lh_skill_birth.py scan [--source <json>]      # 扫描场景→生成草案（幂等）
  lh_skill_birth.py list                        # 列出草案
  lh_skill_birth.py promote <name>              # 草案转正（入技能目录+注册）
  lh_skill_birth.py status                      # 流水线状态
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys

HOME = os.path.expanduser("~")
BASE = os.path.join(HOME, "longhun-system")
DEFAULT_SOURCE = os.path.join(BASE, "knowledge", "auto-learned", "scenarios", "scenario_reports.json")
DRAFTS_DIR = os.path.join(BASE, "skills", "skill-birth", "drafts")
SKILLS_DIR = os.path.join(BASE, ".codebuddy", "skills")
BIRTH_LOG = os.path.join(BASE, "logs", "skill_pipeline", "birth_log.jsonl")
REGISTRY = os.path.join(BASE, "logs", "skill_pipeline", "registry.json")

HEADER = (
    "# DNA: #龍芯⚡️丙午·丙申·申时·䷔噬嗑-SKILL-BIRTH-v1.0-UID9622\n"
    "# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰\n"
    "# License: MulanPSL v2\n"
)


def _today():
    return datetime.date.today().isoformat()


def _now():
    return datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def _slug_from(text):
    """从中文创新点提取技能 slug（取首段 4 汉字）"""
    m = re.search(r"[\u4e00-\u9fff]{2,6}", text or "")
    return m.group(0)[:4] if m else "skill"


def _gen_dna(slug):
    h = hashlib.sha256(f"{_now()}{slug}".encode()).hexdigest()[:8]
    return f"#龍芯⚡️{_today()}-SKILL-BIRTH-{slug}-{h}"


def _load_scenarios(source):
    with open(source, encoding="utf-8") as f:
        return json.load(f)


def _load_birth_log():
    if not os.path.exists(BIRTH_LOG):
        return []
    out = []
    with open(BIRTH_LOG, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return out


def _append_birth_log(entry):
    os.makedirs(os.path.dirname(BIRTH_LOG), exist_ok=True)
    with open(BIRTH_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _render_skill_md(sc, slug, dna):
    name = f"longhun-skill-{slug}"
    points = "\n".join(f"- {p}" for p in sc.get("innovation_points", []))
    linkage = "\n".join(f"- {l}" for l in sc.get("linkage_ways", []))
    risks = "\n".join(f"- {r}" for r in sc.get("risks", []))
    return (
        f"---\n"
        f"name: {name}\n"
        f"description: 龍魂自动学习沉淀技能（场景 {sc.get('dna', '')}）— {sc.get('innovation_points', [''])[0]}\n"
        f"license: MIT\n"
        f"metadata:\n"
        f"  version: '0.1'\n"
        f"  dna: '{dna}'\n"
        f"  id: '{slug}'\n"
        f"  entry: ''\n"
        f"  entry_valid: False\n"
        f"  trigger:\n"
        f"    keywords:\n"
        f"    - {slug}\n"
        f"  category: longhun\n"
        f"  workspace: {BASE}\n"
        f"---\n"
        f"{HEADER}\n"
        f"# {slug} · 技能草案（出生待审）\n\n"
        f"> 来源场景: {sc.get('dna', 'N/A')} · 预估 {sc.get('estimated_hours', '?')}h · 出生 {_today()}\n\n"
        f"## 创新点\n{points}\n\n"
        f"## 联动方式\n{linkage}\n\n"
        f"## 风险\n{risks}\n\n"
        f"## 状态\n- 出生: draft\n- 生效: 待 P13 封神榜审核 promote\n"
    )


def cmd_scan(source):
    scs = _load_scenarios(source)
    actionable = [s for s in scs if s.get("actionability")]
    log = _load_birth_log()
    existing = {e["slug"] for e in log if e.get("status") != "rejected"}
    created, skipped = 0, 0
    for sc in actionable:
        slug = _slug_from(sc.get("innovation_points", [""])[0])
        if slug in existing:
            skipped += 1
            continue
        dna = _gen_dna(slug)
        os.makedirs(DRAFTS_DIR, exist_ok=True)
        path = os.path.join(DRAFTS_DIR, f"{slug}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(_render_skill_md(sc, slug, dna))
        _append_birth_log({
            "slug": slug, "dna": dna, "source_dna": sc.get("dna"),
            "hours": sc.get("estimated_hours"), "status": "draft",
            "innovation_points": sc.get("innovation_points", []),
            "draft": path, "born": _now(),
        })
        existing.add(slug)
        created += 1
    print(f"🐉 技能出生扫描完成：场景 {len(scs)} · 可落地 {len(actionable)} · 新出生 {created} · 跳过(已存在) {skipped}")
    for e in _load_birth_log():
        if e["status"] == "draft":
            print(f"  🟡 {e['slug']}  draft  {e['draft']}  (~{e['hours']}h)")
    return 0


def cmd_list():
    log = _load_birth_log()
    if not log:
        print("（暂无出生记录）")
        return 0
    for e in log:
        mark = {"draft": "🟡", "promoted": "🟢", "rejected": "🔴"}.get(e["status"], "⚪")
        print(f"  {mark} {e['slug']}  {e['status']}  {e['dna']}  born={e.get('born', '?')}")
    return 0


def _gen_entry_script(slug, points):
    """技能转正时生成最小入口脚本（真实可执行，非摆设）"""
    entry = os.path.join(BASE, "bin", f"lh_skill_{slug}.py")
    if os.path.exists(entry):
        return entry
    body = (
        f"#!/usr/bin/env python3\n"
        f"# -*- coding: utf-8 -*-\n"
        f"# DNA: #龍芯⚡️{_today()}-SKILL-ENTRY-{slug}-{hashlib.sha256(slug.encode()).hexdigest()[:8]}\n"
        f"# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰\n"
        f"# License: MulanPSL v2\n"
        f'"""龍魂技能·{slug} 最小入口（自动出生·待增强）"""\n'
        f"import os\n"
        f'print(f"🐉 技能[{slug}]入口就绪 · 出生 {_today()}")\n'
        f'for p in {list(points[:3])}:\n'
        f'    print("  -", p)\n'
        f'print("  ⏳ 增强待定：联动/风险/闸门接入（P13 封神榜后续批注）")\n'
    )
    with open(entry, "w", encoding="utf-8") as f:
        f.write(body)
    return entry


def cmd_promote(name):
    log = _load_birth_log()
    entry = next((e for e in log if e["slug"] == name), None)
    if not entry:
        print(f"❌ 未找到技能 {name}（先 scan 出生）")
        return 1
    if entry["status"] == "promoted":
        print(f"⏭️ {name} 已是 promoted")
        return 0
    draft = entry["draft"]
    if not os.path.exists(draft):
        print(f"❌ 草案文件丢失: {draft}")
        return 1
    # 生成最小入口（真实可执行）
    points = entry.get("innovation_points", [])
    entry_py = _gen_entry_script(name, points)
    # 转正式目录
    target_dir = os.path.join(SKILLS_DIR, f"longhun-skill-{name}")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "SKILL.md")
    content = open(draft, encoding="utf-8").read()
    content = content.replace("  version: '0.1'", "  version: '1.0'")
    content = content.replace("  entry: ''", f"  entry: '{entry_py}'")
    content = content.replace("  entry_valid: False", "  entry_valid: True")
    content = content.replace("## 状态\n- 出生: draft\n- 生效: 待 P13 封神榜审核 promote\n",
                              "## 状态\n- 出生: draft → promoted\n- 生效: P13 审核放行 · {}\n".format(_now()))
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)
    # 更新注册表
    reg = {}
    if os.path.exists(REGISTRY):
        reg = json.load(open(REGISTRY, encoding="utf-8"))
    slug_upper = name.upper()
    reg[slug_upper] = {
        "name": slug_upper, "path": f".codebuddy/skills/longhun-skill-{name}/SKILL.md",
        "entry": entry_py, "version": "v1.0.0", "status": "published", "tricolor": "🟡",
        "updated": _now().replace(" ", "T") + "Z", "published": _now().replace(" ", "T") + "Z",
    }
    with open(REGISTRY, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
    # 更新出生日志
    entry["status"] = "promoted"
    entry["promoted"] = _now()
    entry["target"] = target
    entry["entry"] = entry_py
    with open(BIRTH_LOG, "w", encoding="utf-8") as f:
        for e in log:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"✅ {name} 已转正: {target}\n   ↳ 入口: {entry_py}（可执行）· 已注册 · 待 P05 三色审计")
    return 0


def cmd_status():
    log = _load_birth_log()
    draft = sum(1 for e in log if e["status"] == "draft")
    prom = sum(1 for e in log if e["status"] == "promoted")
    print(f"🐉 技能出生流水线 · 累计 {len(log)} · 🟡draft {draft} · 🟢promoted {prom}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="龍魂·专家自进化·技能出生流水线 v1.0")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("scan")
    s.add_argument("--source", default=DEFAULT_SOURCE)
    sub.add_parser("list")
    p = sub.add_parser("promote")
    p.add_argument("name")
    sub.add_parser("status")
    args = ap.parse_args()
    if args.cmd == "scan":
        return cmd_scan(args.source)
    if args.cmd == "list":
        return cmd_list()
    if args.cmd == "promote":
        return cmd_promote(args.name)
    if args.cmd == "status":
        return cmd_status()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
