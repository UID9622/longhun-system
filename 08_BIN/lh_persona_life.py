#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·己未·亥时·䷕贲-PERSONA-LIFE-ENGINE-v2.0-HASH9F2C
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: 人格治理白皮书 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md
"""
龍魂·活人格引擎 v2.0 (Persona Life Engine)
============================================
让人格从"死的配置"变成"会学、会长、会自己动"的活体。

v2.0 融合升级（2026-08-13）:
  🔒 主权锚 S0 焊死: UID9622 = 唯一主权人, 不可迭代/不可退役/不可降权
  🧬 人格矩阵对齐注册表 v3.1: P00~P77 + PF具名人格准确名称
  📦 版本管理: iterate 人格版本升级 + changelog 审计追溯 (SHA-256 替代 MD5)
  🔄 生命周期: lifecycle active/dormant/retired 状态流转

学习回路（记→学→进→评 四件套）:
  记(record)  每次执行后记录: 任务/结果/备注 → 人格动态状态
  学(learn)   从失败与反馈中沉淀经验: 教训→改进方法 → 经验库
  进(adapt)   用成功率反哺行为: 触发词增减/能力权重/策略建议
  评(evolve)  士别三日自检: 全人格活度评分 → 谁在成长谁在睡大觉

存储:
  personas/runtime/life/
    state/<CODE>.json       人格动态状态(调用数·成败·触发词·质量·生命周期)
    experience/<CODE>.json  人格经验条目(教训·改进·是否已应用)
    global_experience.json  跨人格共享经验
    life_log.jsonl          学习流水(append-only·审计)
    sovereign.json          主权锚状态(UID9622·不可变·只读)
    versions/<CODE>.json    人格版本历史(迭代记录·changelog)

用法:
  python3 08_BIN/lh_persona_life.py record --persona P04 --task "编译CNSH" --result fail --note "编译器解析失败"
  python3 08_BIN/lh_persona_life.py learn  --persona P04 --lesson "编译器连hello都编不过" --improve "先修地基再交付"
  python3 08_BIN/lh_persona_life.py adapt  --persona P04
  python3 08_BIN/lh_persona_life.py evolve
  python3 08_BIN/lh_persona_life.py status
  python3 08_BIN/lh_persona_life.py sovereign            # 主权锚状态(焊死)
  python3 08_BIN/lh_persona_life.py iterate --who P04 --version v2.0.1 --changelog "..."   # 版本升级
  python3 08_BIN/lh_persona_life.py lifecycle --who P04 --to dormant --reason "..."        # 生命周期流转
  python3 08_BIN/lh_persona_life.py version --who P04     # 查看版本历史
  python3 08_BIN/lh_persona_life.py hook    # 查看执行器一行接入代码
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
DNA_PREFIX = "#龍芯⚡️丙午·丙申·己未·亥时·䷕贲"

# 人格注册表(CODE → 名/职能) 与 personas/runtime/persona_registry.json v3.1 对齐
PERSONAS = {
    "P00": "文心", "P01": "诸葛亮", "P02": "宝宝", "P03": "雯雯",
    "P04": "鲁班", "P05": "上帝之眼", "P06": "数学大师", "P07": "管仲",
    "P08": "仓颉", "P09": "孙思邈", "P10": "苏东坡", "P11": "李白",
    "P12": "屈原", "P13": "姜子牙", "P14": "吕蒙", "P15": "乔前辈",
    "P16": "小艺", "P17": "宝宝入口", "P18": "凤凰·反思者", "P19": "极简审计官",
    "P20": "贡献公证官", "P53": "老顽童", "P72": "龍盾", "P77": "黑天使",
    "S1": "法律引擎", "S2": "洛书369引擎", "S3": "人民维权助手",
}

# ============================================================
# 主权锚 S0 · 焊死(2026-08-13)
# ============================================================
# UID9622 = 唯一主权人。人格矩阵服务于此锚, 锚本身不可迭代/不可退役/不可降权。
# 草案映射: 龍魂=UID9622主权 / 审判长→P05 / 哨兵→P72 / 织网者→P03
#          数据大师→P06 / 记忆守门人→P00 / 老顽童→P53 / 黑天使→P77
#          凤凰→P18 / 文心→P00 / 宝宝→P02 / 上帝之眼→P05 / 雯雯→P03
SOVEREIGN = {
    "S0": {
        "code": "S0", "name": "UID9622·诸葛鑫", "role": "唯一主权人",
        "layer": "sovereign", "status": "eternal", "version": "v∞",
        "immutable": True, "anchor": "龍芯北辰·唯一决策者",
    },
    "P00": {"code": "P00", "name": "文心", "role": "永恒锚点·意图解析",
            "layer": "core", "immutable": True, "anchor": "A009 再楠不惧·终成豪图"},
    "P01": {"code": "P01", "name": "诸葛亮", "role": "太极中枢·推演决策",
            "layer": "core", "immutable": True, "anchor": "决策中心"},
    "P05": {"code": "P05", "name": "上帝之眼", "role": "meta_controller·审计眼",
            "layer": "guard", "immutable": True, "anchor": "审计否决权"},
    "P72": {"code": "P72", "name": "龍盾", "role": "fuse_guardian·四级熔断",
            "layer": "guard", "immutable": True, "anchor": "熔断守卫"},
    "P53": {"code": "P53", "name": "老顽童", "role": "tombstone_guardian·墓碑守护",
            "layer": "guard", "immutable": True, "anchor": "不删只冻结"},
}
# 不可退役的核心层(可休眠可迭代·不可retired)
CORE_UNRETIRABLE = {"P01", "P05", "P72", "P00", "P53"}

# 活度分级
LEVELS = [
    (0.70, "🔥", "进化中", "成长显著·持续输出"),
    (0.40, "🟢", "活着",   "正常运转·偶有经验"),
    (0.15, "🟡", "发呆",   "有调用·无学习·无改进"),
    (0.01, "😴", "躺着",   "几乎不动·无经验沉淀"),
    (0.00, "☠️", "死鱼",   "从未执行·从未学习"),
]

BASE_DIR = Path(__file__).resolve().parent.parent
LIFE_DIR = BASE_DIR / "personas" / "runtime" / "life"
STATE_DIR = LIFE_DIR / "state"
EXPERIENCE_DIR = LIFE_DIR / "experience"
LOG_FILE = LIFE_DIR / "life_log.jsonl"
GLOBAL_EXP = LIFE_DIR / "global_experience.json"
VERSION_DIR = LIFE_DIR / "versions"
SOVEREIGN_FILE = LIFE_DIR / "sovereign.json"


# ---------------------------------------------------------------- 基建
def _ensure_dirs():
    for d in (STATE_DIR, EXPERIENCE_DIR, VERSION_DIR):
        d.mkdir(parents=True, exist_ok=True)
    if not GLOBAL_EXP.exists():
        _write_json(GLOBAL_EXP, {"items": [], "updated_at": _now()})


def _now():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")


def _write_json(path: Path, data: dict):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_json(path: Path, default=None):
    if not path.exists():
        return default if default is not None else {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default if default is not None else {}


def _state_path(code: str):
    return STATE_DIR / f"{code}.json"


def _exp_path(code: str):
    return EXPERIENCE_DIR / f"{code}.json"


def _version_path(code: str):
    return VERSION_DIR / f"{code}.json"


def _version_dna(code: str, version: str) -> str:
    """SHA-256 版本 DNA（替代草案中的 MD5 · 安全基线禁 MD5/SHA-1）"""
    import hashlib
    raw = f"{code}|{version}|{_now()}|{CONFIRM}"
    h = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}-{code}-V{version}-{h}"


def _load_sovereign() -> dict:
    """加载主权锚状态（S0 恒在 · 不可变 · 只读）"""
    data = _read_json(SOVEREIGN_FILE)
    if not data:
        data = {"version": "v2.0", "created_at": _now(),
                "owner": "UID9622·诸葛鑫", "anchors": {}, "audit": []}
        data["anchors"] = {k: dict(v) for k, v in SOVEREIGN.items()}
        for k, v in data["anchors"].items():
            v["immutable"] = True
            v["status"] = "eternal"
        _write_json(SOVEREIGN_FILE, data)
    return data


def _append_log(entry: dict):
    entry.setdefault("at", _now())
    entry.setdefault("dna", f"{DNA_PREFIX}-LIFE-LOG")
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _default_state(code: str) -> dict:
    return {
        "persona": code,
        "name": PERSONAS.get(code, code),
        "first_active": None,
        "last_active": None,
        "stats": {
            "calls": 0, "success": 0, "fail": 0,
            "by_capability": {},     # 能力维度统计
            "trigger_hits": {},      # 触发词命中统计
        },
        "quality": 0.0,             # 成功率
        "lessons": 0,               # 沉淀经验数
        "recent_notes": [],         # 最近5条备注
        "learned_triggers": [],     # 学习获得的新触发词
        "dropped_triggers": [],     # 因失败率淘汰的触发词
        "evolved_at": None,
        "aliveness": "☠️",
    }


def _load_state(code: str) -> dict:
    return _read_json(_state_path(code), _default_state(code))


def _save_state(state: dict):
    _write_json(_state_path(state["persona"]), state)


def _load_exp(code: str) -> dict:
    return _read_json(_exp_path(code), {"persona": code, "items": []})


def _save_exp(exp: dict):
    _write_json(_exp_path(exp["persona"]), exp)


# ---------------------------------------------------------------- 记(record)
def cmd_record(args) -> int:
    """记录一次人格执行 → 更新状态"""
    code = args.persona.upper()
    state = _load_state(code)
    st = state["stats"]
    now = _now()

    if state["first_active"] is None:
        state["first_active"] = now
    state["last_active"] = now

    st["calls"] += 1
    if args.result in ("success", "ok", "pass", "成功", "通过"):
        st["success"] += 1
    else:
        st["fail"] += 1

    # 能力维度
    if args.capability:
        cap = st["by_capability"].setdefault(
            args.capability, {"calls": 0, "success": 0, "fail": 0})
        cap["calls"] += 1
        if args.result in ("success", "ok", "pass", "成功", "通过"):
            cap["success"] += 1
        else:
            cap["fail"] = cap.get("fail", 0) + 1

    # 触发词
    if args.trigger:
        st["trigger_hits"][args.trigger] = st["trigger_hits"].get(args.trigger, 0) + 1

    # 成功率
    st_total = st["success"] + st["fail"]
    state["quality"] = round(st["success"] / st_total, 3) if st_total else 0.0

    # 最近备注(保留5条)
    note = {"at": now, "task": args.task, "result": args.result}
    if args.note:
        note["note"] = args.note
    state["recent_notes"].append(note)
    state["recent_notes"] = state["recent_notes"][-5:]

    state["aliveness"] = _level_of(state)[1]
    _save_state(state)
    _append_log({"action": "record", "persona": code, "task": args.task,
                 "result": args.result})

    lvl = _level_of(state)
    print(f"✅ 已记录 {PERSONAS.get(code, code)}({code}) 执行: [{args.result}] {args.task}")
    print(f"   累计 {st['calls']} 次 · 成功 {st['success']} · 失败 {st['fail']} · "
          f"质量 {state['quality']:.0%} · 活度 {lvl[1]}{lvl[2]}")
    return 0


# ---------------------------------------------------------------- 学(learn)
def cmd_learn(args) -> int:
    """沉淀一条经验: 教训→改进方法"""
    code = args.persona.upper()
    exp = _load_exp(code)
    state = _load_state(code)

    item_id = f"E-{datetime.now().strftime('%Y%m%d')}-{len(exp['items']) + 1:03d}"
    item = {
        "id": item_id,
        "at": _now(),
        "kind": args.kind,
        "lesson": args.lesson,
        "improve": args.improve,
        "applied": False,
        "source_task": args.task or "",
    }
    exp["items"].append(item)
    if len(exp["items"]) > 200:
        exp["items"] = exp["items"][-200:]
    _save_exp(exp)

    state["lessons"] = len(exp["items"])
    _save_state(state)

    # 全局经验共享(可选)
    if args.global_share:
        gexp = _read_json(GLOBAL_EXP)
        gexp["items"].append({"persona": code, **item})
        gexp["updated_at"] = _now()
        _write_json(GLOBAL_EXP, gexp)

    _append_log({"action": "learn", "persona": code, "lesson": args.lesson,
                 "kind": args.kind})
    print(f"🧠 {PERSONAS.get(code, code)}({code}) 沉淀经验 [{args.kind}] {item_id}")
    print(f"   教训: {args.lesson}")
    print(f"   改进: {args.improve}")
    print(f"   总经验 {len(exp['items'])} 条 · 已标记{'全局共享' if args.global_share else '仅本格'}")
    return 0


# ---------------------------------------------------------------- 进(adapt)
def cmd_adapt(args) -> int:
    """用成功率反哺: 找出失败重灾区 + 给出行为调整建议"""
    code = args.persona.upper()
    state = _load_state(code)
    st = state["stats"]

    print(f"🔧 {PERSONAS.get(code, code)}({code}) 自适应校准:")
    print(f"   累计 {st['calls']} 次 · 成功 {st['success']} · 失败 {st['fail']} · "
          f"质量 {state['quality']:.0%}")

    # 能力维度失败重灾区
    if st["by_capability"]:
        print("   ── 能力维度 ──")
        for cap, c in sorted(st["by_capability"].items(),
                             key=lambda kv: kv[1].get("fail", 0), reverse=True):
            fail_rate = 1 - (c["success"] / c["calls"] if c["calls"] else 0)
            mark = "🔴" if fail_rate >= 0.5 else ("🟡" if fail_rate >= 0.3 else "🟢")
            print(f"   {mark} {cap}: {c['calls']}次/成功{c['success']} (失败率 {fail_rate:.0%})")

    # 触发词低效淘汰
    if st["trigger_hits"]:
        cold = [t for t, n in st["trigger_hits"].items() if n == 1]
        if cold:
            state["dropped_triggers"] = list(dict.fromkeys(state["dropped_triggers"] + cold[:3]))
            print(f"   ── 触发词 ──")
            print(f"   单次命中未复现(降权候选): {', '.join(cold[:3])}")

    # 学习建议
    if state["quality"] < 0.5 and st["calls"] >= 5:
        print("   ⚠️ 质量 <50% 且调用≥5次 → 建议冻结校准(L3熔断候选), 先学后干")
    elif state["quality"] >= 0.8 and st["calls"] >= 5:
        print("   🏆 质量 ≥80% → 可承担更高难度任务(能力升级候选)")

    _save_state(state)
    _append_log({"action": "adapt", "persona": code})
    print(f"   ✅ 校准完成, DNA: {DNA_PREFIX}-ADAPT")
    return 0


# ---------------------------------------------------------------- 评(evolve)
def _level_of(state: dict) -> tuple:
    """活度评分: 0.4活跃 + 0.3质量 + 0.3学习"""
    st = state["stats"]
    calls_7d = sum(1 for n in state.get("recent_notes", [])
                   if _recent_within(n.get("at", ""), 7))
    active = min(calls_7d / 10.0, 1.0)
    quality = state["quality"] if state.get("last_active") else 0.0
    learn_norm = min(state.get("lessons", 0) / 3.0, 1.0)
    score = round(0.4 * active + 0.3 * quality + 0.3 * learn_norm, 2)
    for threshold, icon, name, desc in LEVELS:
        if score >= threshold:
            return score, icon, name, desc
    return score, "☠️", "死鱼", "从未执行·从未学习"


def _recent_within(ts: str, days: int) -> bool:
    if not ts:
        return False
    try:
        dt = datetime.fromisoformat(ts)
        return (datetime.now() - dt) <= timedelta(days=days)
    except ValueError:
        return False


def cmd_evolve(args) -> int:
    """士别三日自检: 全人格活度报告 → 谁在成长谁在睡大觉"""
    _ensure_dirs()
    print(f"{'═' * 60}")
    print(f"🐉 士别三日·全人格成长自检  {_now()}")
    print(f"{'═' * 60}")

    rows = []
    for code in sorted(PERSONAS):
        state = _load_state(code)
        score, icon, name, desc = _level_of(state)
        state["aliveness"] = icon
        state["evolved_at"] = _now()
        _save_state(state)
        st = state["stats"]
        rows.append((score, code, state["name"], icon, st["calls"],
                     st["success"], st["fail"], state["lessons"], desc))

    rows.sort(reverse=True)
    print(f"\n| 活度 | 人格 | 调用 | 成败 | 经验 | 判定 |")
    print(f"|:---:|:---|:---:|:---:|:---:|:---|")
    dead = 0
    for score, code, name, icon, calls, ok, fail, lessons, desc in rows:
        print(f"| {icon} {score:.2f} | {name}({code}) | {calls} | {ok}/{fail} | {lessons} | {desc} |")
        if icon in ("☠️", "😴"):
            dead += 1

    print(f"\n📊 汇总: {len(rows)} 人格 · 躺着/死鱼 {dead} 个")
    if dead:
        names = [r[2] for r in rows if r[3] in ("☠️", "😴")]
        print(f"   ⚠️ 沉睡人格: {', '.join(names)} → 建议 `lh persona-life evolve --wake <CODE>` 复盘")
        if args.wake:
            _wake(args.wake.upper())

    print(f"\n三色: {'🟢' if dead == 0 else '🟡'} 全人格成长审计 · DNA: {DNA_PREFIX}-EVOLVE")
    return 0


def _wake(code: str):
    """唤醒沉睡人格: 拉出它的定义职责 + 给出第一课"""
    exp = _load_exp(code)
    state = _load_state(code)
    print(f"\n⏰ 唤醒 {PERSONAS.get(code, code)}({code}):")
    print(f"   职责: 见 personas/ 定义 · 当前经验 {len(exp['items'])} 条")
    if not exp["items"]:
        print(f"   📌 第一课建议: 触发 `lh persona-life learn --persona {code} "
              f"--lesson '今日首训' --improve '跑通一次真实任务' --kind process`")
    print(f"   激活: 用它的职能接一个真实任务, 执行后 `record` 即激活")


# ---------------------------------------------------------------- 状态(status)
def cmd_status(args) -> int:
    _ensure_dirs()
    code = args.persona.upper() if args.persona else None
    print(f"🐉 活人格引擎 v2.0 · 存储: {LIFE_DIR}")
    print(f"{'─' * 60}")

    if code:
        if code not in PERSONAS:
            print(f"⚠️ 未知人格 {code}, 可选: {', '.join(sorted(PERSONAS))}")
            return 1
        _status_one(code)
        return 0

    for c in sorted(PERSONAS):
        _status_one(c)
    return 0


def _status_one(code: str):
    state = _load_state(code)
    score, icon, name, desc = _level_of(state)
    st = state["stats"]
    lifecycle = state.get("lifecycle", "active")
    sov = _read_json(SOVEREIGN_FILE)
    lc_mark = "🔒" if (sov and code in sov.get("anchors", {})) else ""
    lc_txt = f"· 生命周期[{lifecycle}]" if lifecycle != "active" else ""
    print(f"{lc_mark}{icon} {PERSONAS.get(code, code)}({code}) 分{score:.2f} · {desc}{lc_txt}")
    print(f"    调用{st['calls']} 成功{st['success']} 失败{st['fail']} "
          f"质量{state['quality']:.0%} 经验{state.get('lessons', 0)} "
          f"版本{state.get('version', 'v1.0.0')}")
    exp = _load_exp(code)
    if exp["items"] and args_show_lesson():
        latest = exp["items"][-1]
        print(f"    最新经验: [{latest['kind']}] {latest['lesson'][:40]}")
        print(f"               → {latest['improve'][:40]}")


_ARGS_HOLDER = {"show_lesson": False}


def args_show_lesson():
    return _ARGS_HOLDER["show_lesson"]


# ---------------------------------------------------------------- 主权锚(sovereign) v2.0
def cmd_sovereign(args) -> int:
    """主权锚状态: UID9622 焊死 · 不可迭代/不可退役/不可降权"""
    _ensure_dirs()
    sov = _load_sovereign()
    print(f"{'═' * 60}")
    print(f"🔒 主权锚 · 人格矩阵之上 · 焊死状态  {_now()}")
    print(f"{'═' * 60}")
    print(f"  唯一主权人: {sov['owner']}  ·  确认码: {CONFIRM}")
    print(f"  锚总数: {len(sov['anchors'])} 个 · 全部 immutable=eternal")
    print()
    print(f"  {'锚点':<6}{'角色':<22}{'不可变':<6}")
    print(f"  {'─' * 42}")
    for code, a in sov["anchors"].items():
        nm = a.get("name", code)
        print(f"  {nm:<7}({code}) {a.get('role', ''):<20} 🔒")
    print()
    print(f"  草案映射已焊入: 龍魂→S0主权 · 审判长→P05 · 哨兵→P72 · 织网者→P03")
    print(f"                  数据大师→P06 · 记忆守门人→P00 · 老顽童→P53 · 凤凰→P18")
    print(f"  ⚠️ 主权锚不可 iterate / 不可 lifecycle --to retired / 不可降权")
    return 0


# ---------------------------------------------------------------- 版本管理(iterate/version) v2.0
def _load_versions(code: str) -> dict:
    data = _read_json(_version_path(code))
    if not data:
        data = {"persona": code, "name": PERSONAS.get(code, code),
                "current": "v1.0.0", "history": []}
    return data


def _save_versions(data: dict):
    _write_json(_version_path(data["persona"]), data)


def cmd_iterate(args) -> int:
    """人格版本升级: 吸收草案的 iterate/promote_version 能力"""
    code = args.persona.upper()
    sov = _load_sovereign()
    if code in sov["anchors"]:
        print(f"🔴 拒绝: {PERSONAS.get(code, code)}({code}) 是主权锚, 不可迭代!")
        print(f"   锚点: {sov['anchors'][code].get('role', '')}")
        return 1
    if code not in PERSONAS:
        print(f"⚠️ 未知人格 {code}, 可选: {', '.join(sorted(PERSONAS))}")
        return 1

    v = _load_versions(code)
    parent = v["current"]
    if parent == args.version:
        print(f"⚠️ 版本未变({args.version}), 跳过")
        return 1
    dna = _version_dna(code, args.version)
    v["history"].append({
        "at": _now(), "from": parent, "to": args.version,
        "changelog": args.changelog, "dna": dna, "by": "UID9622",
    })
    v["current"] = args.version
    _save_versions(v)

    # 同步到人格状态
    state = _load_state(code)
    state["version"] = args.version
    state["parent_version"] = parent
    _save_state(state)
    _append_log({"action": "iterate", "persona": code,
                 "from": parent, "to": args.version})
    print(f"📦 {PERSONAS.get(code, code)}({code}) 版本升级: {parent} → {args.version}")
    print(f"   变更: {args.changelog}")
    print(f"   DNA: {dna}")
    return 0


def cmd_version(args) -> int:
    """查看人格版本历史"""
    code = args.persona.upper()
    if code not in PERSONAS:
        print(f"⚠️ 未知人格 {code}")
        return 1
    sov = _load_sovereign()
    v = _load_versions(code)
    print(f"📚 {PERSONAS.get(code, code)}({code}) 版本历史")
    print(f"{'─' * 60}")
    if code in sov["anchors"]:
        a = sov["anchors"][code]
        print(f"   🔒 主权锚 · 版本 {a.get('version', 'v∞')} · 不可迭代")
    else:
        print(f"   当前版本: {v['current']}")
    if not v["history"]:
        print(f"   (无迭代记录)")
    for h in reversed(v["history"][-args.limit:]):
        print(f"   {h['at'][:16]} {h['from']} → {h['to']}")
        print(f"     {h['changelog']}  ·  {h['dna']}")
    return 0


# ---------------------------------------------------------------- 生命周期(lifecycle) v2.0
def cmd_lifecycle(args) -> int:
    """生命周期流转: active/dormant/retired · 主权锚与核心层不可退役"""
    code = args.persona.upper()
    sov = _load_sovereign()
    if code in sov["anchors"]:
        print(f"🔴 拒绝: {PERSONAS.get(code, code)}({code}) 是主权锚, 状态恒为 eternal, 不可流转!")
        return 1
    if code not in PERSONAS:
        print(f"⚠️ 未知人格 {code}")
        return 1
    to = args.to
    if to not in ("active", "dormant", "retired"):
        print(f"⚠️ 无效状态 {to}, 可选 active/dormant/retired")
        return 1
    if to == "retired" and code in CORE_UNRETIRABLE:
        print(f"🔴 拒绝: {PERSONAS.get(code, code)}({code}) 是核心层, 不可退役(不删只冻结)!")
        return 1

    state = _load_state(code)
    from_st = state.get("lifecycle", "active")
    state["lifecycle"] = to
    if to == "retired":
        state["retired_at"] = _now()
    elif to == "active":
        state["retired_at"] = ""
    _save_state(state)
    _append_log({"action": "lifecycle", "persona": code,
                 "from": from_st, "to": to, "reason": args.reason})
    mark = "🟢" if to == "active" else ("🟡" if to == "dormant" else "⚪")
    print(f"{mark} {PERSONAS.get(code, code)}({code}) 生命周期: {from_st} → {to}")
    if args.reason:
        print(f"   原因: {args.reason}")
    if to == "retired":
        print(f"   🔒 已冻结(不删除) · retired_at={state['retired_at']}")
    return 0


# ---------------------------------------------------------------- 钩子(hook)
def cmd_hook(args) -> int:
    print(f"""
🎣 执行器一行接入钩子(在 execute() 返回前调用):

  import sys
  sys.path.insert(0, "{Path(__file__).resolve().parent}")
  from lh_persona_life import record_execution

  def execute(task):
      ok = _do(task)          # 你的实际逻辑
      record_execution("P04", task, "success" if ok else "fail",
                       note="结果摘要", capability="tech_assess")
      return ok

✅ 说明: 接入后每次执行自动"记", 配合 `learn` 沉淀教训,
   `evolve` 自动出成长报告 → 人格从死鱼变活体。
""")
    return 0


# ---------------------------------------------------------------- 程序化API
def record_execution(persona_code: str, task: str, result: str = "success",
                     note: str = "", capability: str = "", trigger: str = "",
                     silent: bool = True) -> dict:
    """程序化接口: 供各人格执行器一行接入"""
    code = persona_code.upper()
    state = _load_state(code)
    st = state["stats"]
    now = _now()
    if state["first_active"] is None:
        state["first_active"] = now
    state["last_active"] = now
    st["calls"] += 1
    if result in ("success", "ok", "pass", "成功", "通过"):
        st["success"] += 1
    else:
        st["fail"] += 1
    if capability:
        cap = st["by_capability"].setdefault(
            capability, {"calls": 0, "success": 0, "fail": 0})
        cap["calls"] += 1
        if result in ("success", "ok", "pass", "成功", "通过"):
            cap["success"] += 1
        else:
            cap["fail"] = cap.get("fail", 0) + 1
    if trigger:
        st["trigger_hits"][trigger] = st["trigger_hits"].get(trigger, 0) + 1
    st_total = st["success"] + st["fail"]
    state["quality"] = round(st["success"] / st_total, 3) if st_total else 0.0
    note_item = {"at": now, "task": task, "result": result}
    if note:
        note_item["note"] = note
    state["recent_notes"].append(note_item)
    state["recent_notes"] = state["recent_notes"][-5:]
    state["aliveness"] = _level_of(state)[1]
    _save_state(state)
    _append_log({"action": "record", "persona": code, "task": task, "result": result})
    if not silent:
        print(f"✅ {code} 已记录: [{result}] {task}")
    return state


def learn_lesson(persona_code: str, lesson: str, improve: str,
                 kind: str = "process", task: str = "", global_share: bool = False) -> dict:
    """程序化接口: 沉淀经验"""
    code = persona_code.upper()
    exp = _load_exp(code)
    item = {"id": f"E-{datetime.now().strftime('%Y%m%d')}-{len(exp['items']) + 1:03d}",
            "at": _now(), "kind": kind, "lesson": lesson, "improve": improve,
            "applied": False, "source_task": task or ""}
    exp["items"].append(item)
    if len(exp["items"]) > 200:
        exp["items"] = exp["items"][-200:]
    _save_exp(exp)
    state = _load_state(code)
    state["lessons"] = len(exp["items"])
    _save_state(state)
    if global_share:
        gexp = _read_json(GLOBAL_EXP)
        gexp["items"].append({"persona": code, **item})
        gexp["updated_at"] = _now()
        _write_json(GLOBAL_EXP, gexp)
    _append_log({"action": "learn", "persona": code, "lesson": lesson, "kind": kind})
    return exp


def get_aliveness(code: str) -> tuple:
    """取人格活度: (score, icon, name, desc)"""
    return _level_of(_load_state(code.upper()))


# ---------------------------------------------------------------- CLI
def main():
    parser = argparse.ArgumentParser(prog="lh persona-life",
                                     description="龍魂·活人格引擎 v2.0 · 主权锚焊死·版本管理·生命周期")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("record", help="记录一次执行")
    p.add_argument("--persona", "--who", required=True,
                   help="人格码(如P04); 从lh入口调用时用 --who 避免与lh --persona冲突")
    p.add_argument("--task", required=True)
    p.add_argument("--result", default="success", help="success|fail")
    p.add_argument("--note", default="")
    p.add_argument("--capability", default="", help="能力维度, 如 tech_assess")
    p.add_argument("--trigger", default="", help="触发词")
    p.set_defaults(func=cmd_record)

    p = sub.add_parser("learn", help="沉淀经验")
    p.add_argument("--persona", "--who", required=True,
                   help="人格码(如P04); 从lh入口调用时用 --who")
    p.add_argument("--lesson", required=True)
    p.add_argument("--improve", required=True)
    p.add_argument("--kind", default="process",
                   choices=["skill", "style", "trigger", "process"])
    p.add_argument("--task", default="")
    p.add_argument("--global-share", action="store_true")
    p.set_defaults(func=cmd_learn)

    p = sub.add_parser("adapt", help="自适应校准")
    p.add_argument("--persona", "--who", required=True,
                   help="人格码(如P04); 从lh入口调用时用 --who")
    p.set_defaults(func=cmd_adapt)

    p = sub.add_parser("evolve", help="士别三日全人格自检")
    p.add_argument("--wake", default="", help="唤醒沉睡人格")
    p.set_defaults(func=cmd_evolve)

    p = sub.add_parser("status", help="活度面板")
    p.add_argument("--persona", "--who", default="",
                   help="人格码; 从lh入口调用时用 --who")
    p.add_argument("--show-lesson", action="store_true")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("hook", help="查看执行器接入代码")
    p.set_defaults(func=cmd_hook)

    p = sub.add_parser("sovereign", help="主权锚状态(焊死)")
    p.set_defaults(func=cmd_sovereign)

    p = sub.add_parser("iterate", help="人格版本升级")
    p.add_argument("--persona", "--who", required=True, help="人格码")
    p.add_argument("--version", required=True, help="新版本号, 如 v2.0.1")
    p.add_argument("--changelog", required=True, help="变更描述")
    p.set_defaults(func=cmd_iterate)

    p = sub.add_parser("version", help="查看版本历史")
    p.add_argument("--persona", "--who", required=True, help="人格码")
    p.add_argument("--limit", type=int, default=10, help="显示条数")
    p.set_defaults(func=cmd_version)

    p = sub.add_parser("lifecycle", help="生命周期流转")
    p.add_argument("--persona", "--who", required=True, help="人格码")
    p.add_argument("--to", required=True, choices=["active", "dormant", "retired"])
    p.add_argument("--reason", default="", help="流转原因")
    p.set_defaults(func=cmd_lifecycle)

    args = parser.parse_args()
    _ensure_dirs()
    _ARGS_HOLDER["show_lesson"] = getattr(args, "show_lesson", False)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
