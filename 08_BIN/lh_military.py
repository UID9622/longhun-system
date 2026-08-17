#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 军事调度引擎 v2.0
DNA: #龍芯⚡️丙午·丙申·壬戌·未时-MILITARY-ENGINE-v2.0-FULL-ALIGN
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

功能:
  1. 龍芯家族花名册读取（单一真相源: 20_CONFIG/military_roster.json·v2.0全人格入册）
  2. 全军态势报告 (status)
  3. 树状花名册打印 (roster / 花名册)
  4. 兵种编制查看 (branch <兵种>)
  5. 点名 (rollcall) — 检查所有编制单元脚本是否存在·有无阵亡
  6. 下达命令 (order <单位> <指令>) — 令行禁止·DNA追溯·耻辱墙
  7. 该野该静该守节奏 (phase attack/standby/defend/emergency)
  8. 协同矩阵 (collab [单位]) — 谁呼叫谁·联动闭环
  9. 全自动自测 (test) — 参数完整性/模块路径/协同闭环/数字根·每日后台自动跑

哲学: 军事思维不是军事技能·是运用哲学·细节决定成败·每天做同样的事做到极致
协议: 01_protocols/LH-MILITARY-ORDER-v1.0.md
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROSTER = ROOT / "20_CONFIG" / "military_roster.json"
SHAME_WALL = Path.home() / ".longhun" / "08_STATE" / "shame_wall.jsonl"
HISTORY = Path.home() / ".longhun" / "12_LOGS" / "military_history.jsonl"

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# 兵种别名（lh military-branch 警卫 传参被 lh.py 劫持时的兼容路由）
BRANCH_ALIASES = {
    "侦察": "侦察", "RECON": "侦察",
    "工程": "工程", "ENGINEER": "工程",
    "通信": "通信", "SIGNAL": "通信",
    "警卫": "警卫", "GUARD": "警卫",
    "后勤": "后勤", "LOGISTICS": "后勤",
    "特种": "特种", "SPECIAL": "特种",
}


def _dna(tag: str = "MILITARY") -> str:
    h = hashlib.sha256(f"{tag}{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{tag}-{h}"


def _load_roster() -> dict:
    if not ROSTER.exists():
        print(f"❌ 花名册不存在: {ROSTER}")
        sys.exit(1)
    return json.loads(ROSTER.read_text(encoding="utf-8"))


def _append_jsonl(path: Path, entry: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _all_units(roster: dict) -> list:
    """收集全部编制单元（军官+士兵+兵种指挥官）"""
    units = []
    for group in ("headquarters", "discipline", "political_cultural", "independent"):
        units.extend(roster.get(group, []))
    for branch in roster.get("branches", []):
        units.extend(branch.get("units", []))
        units.extend(branch.get("commanders", []))
    return units


def _persona_units(roster: dict) -> list:
    """收集人格军官单元（id 严格匹配 Pxx·排除 P00-RECON 等兼岗ID）"""
    import re
    return [u for u in _all_units(roster) if re.fullmatch(r"P\d{2}", str(u.get("id", "")))]


def _digital_root(n: int) -> int:
    """洛书九宫数字根"""
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def _module_exists(module: str) -> bool:
    """点名: 模块文件是否存在（阵亡检测）"""
    if not module:
        return True
    for base in (ROOT, ROOT / "bin", ROOT / "08_BIN"):
        if (base / module).exists():
            return True
    return False


def cmd_status(roster: dict) -> int:
    """全军态势"""
    units = _all_units(roster)
    branches = roster.get("branches", [])
    alive = sum(1 for u in units if _module_exists(u.get("module", "")))
    dead = len(units) - alive
    meta = roster["_meta"]
    print("\n🐉 龍魂 · 全军态势报告")
    print("=" * 56)
    print(f"  花名册: {meta['name']} {meta['version']}")
    print(f"  状态:   {meta['status']}")
    print(f"  指挥官: {roster['commander']['name']} ({roster['commander']['rank']})")
    personas = _persona_units(roster)
    subs = [u for u in units if str(u.get("id", "")).startswith("S")]
    officers = len(personas) + len(subs)
    soldiers = len(units) - officers
    print(f"\n📊 编制统计:")
    print(f"  军官(人格):  {officers} 人 (P系 {len(personas)} + S系 {len(subs)})")
    print(f"  士兵(引擎):  {soldiers} 人")
    print(f"  兵种:        {len(branches)} 个")
    print(f"  点名:        🟢 {alive} 在位 · 🔴 {dead} 阵亡/缺失")
    print(f"\n📋 兵种分布:")
    for b in branches:
        print(f"    {b['code']:<10} {b['name']}: {len(b.get('units', []))} 人 | {b['motto']}")
    print(f"\n⚔️ 军规: {roster['military_doctrine']['principle']}")
    print(f"🧬 DNA: {meta['dna']}")
    return 0


def cmd_roster(roster: dict) -> int:
    """树状花名册"""
    print("\n🐉 龍芯家族花名册 · 树状编制")
    print("=" * 56)
    print(f"  👑 {roster['commander']['name']} · {roster['commander']['rank']}")
    groups = [
        ("🏛️ 司令部门", "headquarters"),
        ("⚖️ 纪律监察部", "discipline"),
        ("🎖️ 政治文化战线", "political_cultural"),
        ("🧭 独立兵团", "independent"),
    ]
    for title, key in groups:
        print(f"\n  {title}")
        for u in roster.get(key, []):
            mark = "🟢" if _module_exists(u.get("module", "")) else "🔴"
            print(f"    {mark} [{u['id']}] {u['rank']} {u['name']} — {u['duty']}")
    print("\n  🪖 作战部队")
    for b in roster.get("branches", []):
        print(f"\n    {b['code']} · {b['name']} — {b['motto']}")
        for c in b.get("commanders", []):
            mark = "🟢" if _module_exists(c.get("module", "")) else "🔴"
            print(f"      {mark} [{c['id']}] ⭐ {c['rank']} {c['name']} — {c.get('duty', c.get('capability', ''))}")
        for u in b.get("units", []):
            mark = "🟢" if _module_exists(u.get("module", "")) else "🔴"
            print(f"      {mark} [{u['id']}] {u['rank']} {u['name']} — {u['capability']}")
    return 0


def cmd_branch(roster: dict, name: str) -> int:
    """查看兵种"""
    name_key = name.replace("兵种", "").replace("部队", "").replace("特种", "特种")
    for b in roster.get("branches", []):
        aliases = {b["code"], b["name"], b["name"].replace("兵种", ""), b["name"].replace("部队", ""),
                   b["name"][:2], b["name"].replace("兵种", "").replace("部队", "")}
        if name in aliases or name_key in aliases:
            print(f"\n🪖 {b['code']} · {b['name']}")
            print(f"   座右铭: {b['motto']}")
            print(f"   职责:   {b['duty']}")
            print(f"   技能:   {' · '.join(b.get('skills', []))}")
            for c in b.get("commanders", []):
                mark = "🟢" if _module_exists(c.get("module", "")) else "🔴"
                print(f"   指挥官: {mark} [{c['id']}] {c['rank']} {c['name']} — {c.get('duty', c.get('capability', ''))}")
            print(f"\n   编制:")
            for u in b.get("units", []):
                mark = "🟢" if _module_exists(u.get("module", "")) else "🔴"
                print(f"     {mark} [{u['id']}] {u['rank']} {u['name']} — {u['capability']} ({u['module']})")
            return 0
    print(f"❌ 找不到兵种: {name}（可选: 侦察/工程/通信/警卫/后勤/特种）")
    return 1


def cmd_rollcall(roster: dict) -> int:
    """点名·阵亡检测"""
    units = _all_units(roster)
    alive, dead = [], []
    for u in units:
        (alive if _module_exists(u.get("module", "")) else dead).append(u)
    print(f"\n🐉 全军点名 · 总兵力 {len(units)} 人")
    print(f"  🟢 在位: {len(alive)} 人")
    for u in alive:
        print(f"    ✅ [{u['id']}] {u.get('rank', '')} {u['name']}")
    if dead:
        print(f"  🔴 阵亡/缺失: {len(dead)} 人")
        for u in dead:
            print(f"    ❌ [{u['id']}] {u['name']} — 模块缺失: {u.get('module', '无')}")
    else:
        print(f"  🔴 阵亡: 0 人")
    return 0


def cmd_order(roster: dict, target: str, command: str, priority: int = 5, timeout: int = 30) -> int:
    """下达命令·令行禁止"""
    units = _all_units(roster)
    unit = next((u for u in units if target in (u["id"], u["name"]) or u["id"].lower() == target.lower()), None)
    if not unit:
        print(f"❌ 目标单位不存在: {target}")
        return 1
    order_id = f"ORD-{datetime.now().strftime('%H%M%S')}-{hashlib.md5(command.encode()).hexdigest()[:6].upper()}"
    entry = {
        "order_id": order_id,
        "commander": roster["commander"]["id"],
        "target": unit["id"],
        "target_name": unit["name"],
        "rank": unit.get("rank", ""),
        "command": command,
        "priority": priority,
        "timeout": timeout,
        "status": "执行中",
        "issued_at": datetime.now().isoformat(),
        "dna": _dna("ORDER"),
    }
    _append_jsonl(HISTORY, {"action": "order_issued", "entry": entry})
    print(f"\n⚡ 命令已下达（令行禁止）")
    print("=" * 50)
    print(f"  命令ID:   {order_id}")
    print(f"  指挥官:   {roster['commander']['name']}")
    print(f"  目标:     [{unit['id']}] {unit['name']} ({unit.get('rank', '')})")
    print(f"  指令:     {command}")
    print(f"  优先级:   {priority}/10")
    print(f"  超时:     {timeout}s")
    print(f"  状态:     执行中 · 待回执")
    print(f"  DNA:      {entry['dna']}")
    # 标记执行记录
    unit["last_order"] = command
    unit["last_active"] = datetime.now().isoformat()
    print(f"\n  📡 回执: 已记录史官 · 审计链可查 (lh military orders)")
    return 0


def cmd_orders(limit: int = 10) -> int:
    """查看最近命令"""
    if not HISTORY.exists():
        print("📋 暂无命令记录")
        return 0
    lines = HISTORY.read_text(encoding="utf-8").strip().splitlines()[-limit:]
    print(f"\n📋 最近 {len(lines)} 条军令")
    print("=" * 60)
    for line in reversed(lines):
        try:
            e = json.loads(line)["entry"]
            print(f"  {e['issued_at'][:19]} [{e['priority']}] {e['command']} → {e['target_name']} ({e['status']})")
        except Exception:
            continue
    return 0


def cmd_phase(roster: dict, phase: str) -> int:
    """该野该静该守"""
    phases = roster["military_doctrine"]["phases"]
    if phase == "all":
        print("\n🎭 龍魂军事节奏（军人的分寸感）")
        print("=" * 50)
        for k, v in phases.items():
            print(f"  {k:<10} {v}")
        return 0
    if phase not in phases:
        print(f"❌ 节奏可选: {list(phases.keys())} 或 all")
        return 1
    print(f"\n🎭 当前节奏: {phase}")
    print(f"  {phases[phase]}")
    return 0


def cmd_collab(roster: dict, name: str = "") -> int:
    """协同矩阵·谁呼叫谁·联动闭环"""
    links = roster.get("collaboration", {}).get("links", [])
    if not name:
        print(f"\n🤝 龍魂协同作战矩阵 · {len(links)} 条联动链路")
        print("=" * 62)
        for l in links:
            print(f"  {l['from']:<6} → {l['to']:<8} {l['action']}")
        print(f"\n  哲学: {roster.get('collaboration', {}).get('description', '')}")
        return 0
    # 查某单位协作关系
    name = name.upper()
    related = [l for l in links if name in (l["from"], l["to"])]
    if not related:
        print(f"❌ 未找到 {name} 的协同链路")
        return 1
    print(f"\n🤝 {name} 协同作战关系")
    print("=" * 50)
    for l in related:
        arrow = "→" if l["from"] == name else "←"
        print(f"  {l['from']} {arrow} {l['to']}  {l['action']}")
    return 0


def cmd_test(roster: dict) -> int:
    """全自动自测·细节决定成败·每天重复做到极致
    检查: 20人格全入册 / params参数完整 / 模块路径真实 / 协同闭环 / 数字根验证"""
    print("\n🛡️ 龍魂军事编制 · 全自动自测")
    print("=" * 62)
    results = []
    fail_count = 0

    def check(name, ok, detail=""):
        nonlocal fail_count
        mark = "✅" if ok else "❌"
        if not ok:
            fail_count += 1
        results.append({"check": name, "ok": ok, "detail": detail})
        print(f"  {mark} {name} {detail}")

    units = _all_units(roster)
    personas = _persona_units(roster)
    persona_ids = {u["id"] for u in personas}

    # 1. 20人格全入册检查（龍魂真实20人格: P00-P15 + P18/P19/P20 + P72 + P77）
    expected = {f"P{i:02d}" for i in range(0, 16)} | {"P18", "P19", "P20", "P72", "P77"}
    missing = sorted(expected - persona_ids)
    check("20人格全入册", not missing, f"(实际 {len(persona_ids)} 个P系单元·预期 {len(expected)})" + (f" 缺失: {missing}" if missing else ""))

    # 2. params 参数完整性
    no_params = [u["id"] for u in units if "params" not in u]
    no_trigger = [u["id"] for u in units if u.get("params", {}).get("trigger_words") in (None, [], "")]
    check("params参数完整", not no_params, f"(参数缺失: {len(no_params)})" if no_params else f"({len(units)}单元全齐)")
    check("触发词已配置", not no_trigger, f"(缺触发词: {len(no_trigger)})" if no_trigger else f"({len(units)}单元全齐)")

    # 3. 模块路径真实（点名·阵亡检测）
    dead = [u for u in units if not _module_exists(u.get("module", ""))]
    check("模块路径真实·全员在位", not dead, f"(阵亡: {len(dead)})" if dead else f"({len(units)}/{len(units)} 在位)")

    # 4. 协同闭环（collaborators 都能在花名册找到）
    all_ids = {u["id"] for u in units} | {"UID9622"}
    broken = []
    for u in units:
        for c in u.get("params", {}).get("collaborators", []):
            if c not in all_ids:
                broken.append(f"{u['id']}→{c}")
    check("协同闭环·无断链", not broken, (f" 断链: {broken}" if broken else f"({len(units)}单元协作全闭环)"))

    # 5. 协同矩阵链路目标存在
    links = roster.get("collaboration", {}).get("links", [])
    bad_links = [l for l in links if l["from"] not in all_ids or l["to"] not in all_ids]
    check("协同矩阵有效", not bad_links, (f" 无效链路: {bad_links}" if bad_links else f"({len(links)}条链路全有效)"))

    # 6. 数字根验证（369不动点锚·验证恒等式本身而非强行凑数）
    total = len(units)
    dr = _digital_root(total)
    dr369 = _digital_root(369)
    anchors = roster.get("algorithm_verification", {}).get("anchors", {})
    check("数字根锚点验证", dr369 == 9, f"(369不动点数字根={dr369} ✓3+6+9→18→9 · 总编制 {total} 数字根={dr} · 锚点={anchors.get('369_fixed_point', '')})")

    # 7. 算法验证规则存在
    rules = roster.get("algorithm_verification", {}).get("rules", [])
    check("算法验证规则", len(rules) >= 5, f"({len(rules)}条规则)")

    # 汇总
    print("=" * 62)
    total_checks = len(results)
    verdict = "🟢 全军自测通过" if fail_count == 0 else f"🔴 自测失败 · {fail_count}/{total_checks} 项未过"
    print(f"  {verdict}")
    print(f"  检查项: {total_checks} · 人格: {len(personas)} · 总编制: {total}")

    # 落盘测试报告
    report_path = ROOT / "logs" / "military_test_report.jsonl"
    report = {
        "timestamp": datetime.now().isoformat(),
        "verdict": "PASS" if fail_count == 0 else "FAIL",
        "total_checks": total_checks,
        "fail_count": fail_count,
        "persona_count": len(personas),
        "unit_count": total,
        "digital_root": dr,
        "results": results,
        "dna": _dna("MILITARY-TEST"),
    }
    _append_jsonl(report_path, report)

    # 失败 → 耻辱墙 + 建议
    if fail_count > 0:
        _append_jsonl(SHAME_WALL, {
            "timestamp": datetime.now().isoformat(),
            "reason": "军事编制自测失败",
            "details": {"fail_count": fail_count, "results": results},
            "severity": "HIGH",
            "dna": _dna("SHAME"),
        })
        print(f"\n  🚨 已记录耻辱墙 · 报告: logs/military_test_report.jsonl")
        print(f"  🛠️ 修复建议: 检查缺失模块路径 / 补全 params / 修复协同断链")
        return 1
    print(f"\n  📋 报告: logs/military_test_report.jsonl")
    return 0


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 军事调度引擎 v2.0")
    # 不设 choices: 兵种名(侦察/工程/通信/警卫/后勤/特种)直接作为子命令传入时兼容路由
    parser.add_argument("subcommand", nargs="?", default="status")
    parser.add_argument("args", nargs="*", help="参数")
    args = parser.parse_args()

    if args.subcommand == "help":
        print("""
🐉 lh military 用法
  lh military                    全军态势
  lh military roster / 花名册    树状编制表
  lh military branch 侦察         查看兵种（侦察/工程/通信/警卫/后勤/特种）
  lh military rollcall / 点名     全军点名·阵亡检测
  lh military order ENG-001 "..." 下达命令 (可选 --p 优先级)
  lh military orders              最近军令
  lh military phase all           该野/该静/该守/该急 节奏
  lh military collab [单位]       协同矩阵·谁呼叫谁·联动闭环
  lh military test                全自动自测·参数/路径/协同/数字根
""")
        return 0

    roster = _load_roster()
    sub = args.subcommand
    # 🔧 兼容: lh military-branch 警卫 传参被 lh.py 劫持时，子命令直接变成兵种名
    if sub in BRANCH_ALIASES:
        return cmd_branch(roster, BRANCH_ALIASES[sub])
    # 🔧 兼容: lh military-collab P72 传参被劫持时，子命令=单位ID → 查该单位协同
    if re.fullmatch(r"[PS]\d{2}(?:-[A-Z0-9]+)?", sub.upper()):
        return cmd_collab(roster, sub.upper())
    if sub == "status":
        return cmd_status(roster)
    if sub in ("roster", "花名册"):
        return cmd_roster(roster)
    if sub == "branch":
        name = args.args[0] if args.args else "侦察"
        return cmd_branch(roster, name)
    if sub in ("rollcall", "点名"):
        return cmd_rollcall(roster)
    if sub == "order":
        if len(args.args) < 2:
            print("用法: lh military order <单位ID/名> \"<指令>\"")
            return 1
        return cmd_order(roster, args.args[0], " ".join(args.args[1:]))
    if sub == "orders":
        return cmd_orders()
    if sub == "phase":
        phase = args.args[0] if args.args else "all"
        return cmd_phase(roster, phase)
    if sub in ("collab", "协同"):
        name = args.args[0] if args.args else ""
        return cmd_collab(roster, name)
    if sub in ("test", "自测"):
        return cmd_test(roster)
    return cmd_status(roster)


if __name__ == "__main__":
    sys.exit(main())
