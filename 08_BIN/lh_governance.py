#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丁酉·辛巳·巳时·䷝离-LH-GOVERNANCE-v2.1-UID9622
# 龍魂 · 三色治理指挥层 v2.1（薄胶水 · 复用既有引擎 · M77 零重复开发）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: LH-TRICOLOR-GOVERNANCE-v2.1.md · 上层协议: LH-NO-BACKEND-COMMUNITY-COUNCIL-v1.0.md
# 🛡️ P0焊死(2026-09-04·P72加封): 治理链受管引擎·源码修改须走 LH-TRICOLOR-GOVERNANCE-v2.1 §十二 门槛(UID9622签章+新DNA+修订记录)
"""
lh gov — 三色治理指挥层
──────────────────────────────────────────────
status            查询系统/实体三色状态（聚合 health+council+耻辱墙）
propose <entity>  提议🟡(默认)/🔴 → 自动升堂 council 提案
vote <id>         转发审批团表决
audit <id>        完整证据链（提案视图 + 哈希链指引）
trace <id>        ledger 全事件链（含 prev/hash）
trust <uid>       信誉分+状态（正常/冻结/只读）
score <uid> [--dr]     贡献值+数字根审计标记（calc 语义）
score-log <uid>   贡献/信誉事件明细
score <uid> add <v> [--reason R]   记贡献事件（append-only）
check <uid>       投票资格门槛（贡献≥10·信誉≥60）
sync              扫 council ledger → 自动更新信誉（一致+1/不一致−2/连续±）·决策与声誉绑定
leaderboard       信誉+贡献排行前 20
redline [check <文本>]  红线库查看/文本命中检测（系统主权红线·非政治词表）
dashboard         Markdown 治理总览（含 DNA+GPG）
──────────────────────────────────────────────
数据: ~/.longhun/governance/  (red_rules.json / contribution.jsonl / reputation.jsonl / scores.json)
"""
import argparse, json, os, subprocess, sys
from datetime import datetime

HOME = os.path.expanduser("~/.longhun/governance")
COUNCIL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lh_council.py")
LEDGER = os.path.expanduser("~/.longhun/council/ledger.jsonl")
SHAME = os.path.expanduser("~/.longhun/shame_wall")

# ── 写死常量（协议 §4.2 · 不可运行时修改）─────────────────────────────
INIT_REPU = 100
VOTE_CORRECT = 1
VOTE_WRONG = -2
STREAK_5_CORRECT = 5
STREAK_5_WRONG = -10
APPEAL_ADOPTED = 3
FROZEN = 60      # < 60 禁止投票
READONLY = 40    # < 40 只读
CONTRIB_MIN = 10 # 参与资格

DNA = "#龍芯⚡️丙午·丁酉·辛巳·巳时·䷝离-LH-TRICOLOR-GOVERNANCE-v2.1-UID9622"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

os.makedirs(HOME, exist_ok=True)

def _ts():
    return datetime.now().timestamp()

def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def _f(t):  # 分数读取
    p = os.path.join(HOME, t + ".jsonl")
    out = []
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8"):
            ln = ln.strip()
            if ln:
                try: out.append(json.loads(ln))
                except Exception: pass
    return out

def _a(fn, e):  # append 事件
    with open(os.path.join(HOME, fn + ".jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")

def _load_scores():
    p = os.path.join(HOME, "scores.json")
    if os.path.exists(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception:
            return {}
    return {}

def _save_scores(d):
    with open(os.path.join(HOME, "scores.json"), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)

def dr(x):  # 数字根
    x = abs(int(x))
    while x >= 10:
        x = sum(int(c) for c in str(x))
    return x

def dr_channel(v):
    r = dr(v)
    if r in (1, 2, 4, 5, 7): return "🟢 green_fast"
    if r in (3, 6): return "🟡 yellow_review"
    return "⚠️ warning"

def repu_state(s):
    if s < READONLY: return "只读"
    if s < FROZEN: return "冻结(禁投票)"
    return "正常"

# ── status ───────────────────────────────────────────────────────────
def _cmd_status(a):
    print(f"龍魂·三色治理 v2.1 · system 状态")
    ok = True
    try:
        r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lh_health.py"), "--json"],
                           capture_output=True, text=True, timeout=30)
        try:
            h = json.loads(r.stdout); st = h.get("status") or h.get("ok")
            print(f"  🏥 health: {r.stdout.strip()[:120]}")
            if st is False or h.get("red"): ok = False
        except Exception:
            print(f"  🏥 health: {r.stdout.strip()[:120]}")
    except Exception as ex:
        ok = False
        print(f"  🏥 health: 不可达 ({ex})")
    voting = 0
    if os.path.exists(LEDGER):
        for ln in open(LEDGER, encoding="utf-8"):
            if "voting" in ln: voting += 1
    print(f"  ⚖️ council 表决中提案: {voting}")
    red = False
    recent_wall = 0
    if os.path.exists(SHAME):
        try:
            now = datetime.now().timestamp()
            for f in os.listdir(SHAME):
                fp = os.path.join(SHAME, f)
                if os.path.isfile(fp) and now - os.path.getmtime(fp) < 30 * 86400:
                    recent_wall += 1
            red = recent_wall > 0
        except Exception:
            pass
    print(f"  🏳️ 耻辱墙: 近30天 {recent_wall} 条记录{' (🔴关注)' if red else ' (正常)'}")
    if red:
        print("  🔴 system")
    elif voting:
        print("  🟡 system")
    elif ok:
        print("  🟢 system")
    else:
        print("  🟡 system")
    print(f"\nDNA {DNA}\nCONFIRM {CONFIRM}")

# ── council 转发 ─────────────────────────────────────────────────────
def _council(*args):
    r = subprocess.run([sys.executable, COUNCIL] + list(args), capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    return r.returncode

def _cmd_propose(a):
    # 🟡(默认) → standard；🔴 → major(解封/重审语义)
    ptype = "major" if a.color == "r" else "standard"
    print(f"⚖️ 三色治理 → 自动升堂审批团 ({'🔴重审(major≥3/4)' if a.color=='r' else '🟡裁决(standard≥2/3)'})")
    return _council("propose", ptype, a.entity, "--title",
                    f"[三色治理] {a.title}", "--as", a.as_alias or "C1")

def _cmd_vote(a):
    dec = "pass" if a.approve else ("reject" if a.reject else "abstain")
    args = ["vote", a.id, dec]
    if a.reason: args += ["-r", a.reason]
    if a.as_alias: args += ["--as", a.as_alias]
    return _council(*args)

def _cmd_audit(a):
    r = _council("view", a.id)
    if r == 0:
        print("\n🔎 证据链: 事件全部落 ~/.longhun/council/ledger.jsonl (append-only)")
        print("🔎 验链: lh council verify  ·  全链: lh council ledger")
    return r

def _cmd_trace(a):
    if not os.path.exists(LEDGER):
        print("账本不存在")
        return 1
    print(f"🔎 提案 {a.id} 决策链:")
    for ln in open(LEDGER, encoding="utf-8"):
        ln = ln.strip()
        if not ln: continue
        try: e = json.loads(ln)
        except Exception: continue
        if a.id not in ln: continue
        print(f"  {e.get('type','?'):<9} {datetime.fromtimestamp(e['ts']).strftime('%H:%M:%S'):<10} "
              f"prev={str(e.get('prev_hash',''))[:8]}→hash={str(e.get('hash',''))[:8]}  {str(e)[:100]}")
    return 0

# ── 分数与信誉 ───────────────────────────────────────────────────────
def _score_of(scores, uid):
    s = scores.setdefault(uid, {"contrib": 0, "repu": INIT_REPU, "streak": 0, "cont": 0})
    return s

def _cmd_score(a):
    if getattr(a, "add", None) is not None:
        ev = {"ts": _ts(), "uid": a.uid, "delta": a.add, "reason": a.reason or "", "dna": DNA}
        _a("contribution", ev)
        scores = _load_scores(); s = _score_of(scores, a.uid)
        s["contrib"] = max(0, s["contrib"] + a.add); _save_scores(scores)
        print(f"✅ 贡献 {a.uid}: +{a.add} → {s['contrib']} ({a.reason})")
        return 0
    scores = _load_scores(); s = _score_of(scores, a.uid)
    contrib = s["contrib"]; repu = s["repu"]
    if a.dr and contrib >= 100:
        ch = dr_channel(contrib)
        print(f"🧮 {a.uid}: 贡献={contrib} · dr({contrib})={dr(contrib)} → {ch} (里程碑审计标记·非阻断)")
    else:
        print(f"🧮 {a.uid}: 贡献={contrib} · 信誉={repu} [{repu_state(repu)}]")
    print(f"   资格: {'✅ 可参与' if contrib >= CONTRIB_MIN and repu >= FROZEN else '❌ 未达门槛'}"
          f" (贡献≥{CONTRIB_MIN}·信誉≥{FROZEN})")
    return 0

def _cmd_score_log(a):
    evs = [e for e in _f("contribution") if e.get("uid") == a.uid]
    if not evs:
        print(f"(空) {a.uid} 无贡献事件")
        return 0
    for e in evs:
        print(f"  {datetime.fromtimestamp(e['ts']).strftime('%Y-%m-%d %H:%M'):<20} "
              f"{'+' if e.get('delta',0)>=0 else ''}{e.get('delta',0):<5} {e.get('reason','')}")
    return 0

def _cmd_check(a):
    scores = _load_scores(); s = _score_of(scores, a.uid)
    c, r = s["contrib"], s["repu"]
    okk = c >= CONTRIB_MIN and r >= FROZEN
    print(f"{'✅' if okk else '❌'} {a.uid}: 贡献={c} 信誉={r} → {'过门槛·可上桌' if okk else '未达投票资格'}")
    return 0

def _cmd_trust(a):
    scores = _load_scores()
    if not scores:
        print("ℹ️ 尚无分数事件 · 跑一次 `lh gov sync` 从 council ledger 同步")
        return 0
    s = _score_of(scores, a.uid)
    print(f"🐉 信誉 {a.uid}: {s['repu']} [{repu_state(s['repu'])}] · 连续一致 {s['streak']} 次")
    evs = [e for e in _f("reputation") if e.get("uid") == a.uid]
    for e in evs[-8:]:
        print(f"  {datetime.fromtimestamp(e['ts']).strftime('%m-%d %H:%M'):<14} "
              f"{'+' if e.get('delta',0)>=0 else ''}{e.get('delta',0):<4} {e.get('reason','')}")
    return 0

def _cmd_sync(a):
    """扫 council ledger：ballet vs verdict → 一致+1/不一致−2 · 连续5次±bonus"""
    if not os.path.exists(LEDGER):
        print("council 账本不存在 · 无表决事件")
        return 0
    evts = []
    for ln in open(LEDGER, encoding="utf-8"):
        ln = ln.strip()
        if not ln: continue
        try: evts.append(json.loads(ln))
        except Exception: pass
    verdicts = {}
    for e in evts:
        if e.get("type") == "verdict":
            verdicts.setdefault(e.get("ref"), []).append(e.get("outcome"))
    done = set()
    p = os.path.join(HOME, "sync_processed.json")
    if os.path.exists(p):
        try: done = set(json.load(open(p)))
        except Exception: done = set()
    scores = _load_scores()
    n = 0
    for e in evts:
        if e.get("type") != "ballot": continue
        ref = e.get("ref"); uid = e.get("voter")
        key = f"{ref}|{uid}"
        if not ref or not uid or key in done: continue
        outs = verdicts.get(ref, [])
        if not outs: continue  # 未出裁的不计
        final = outs[-1]
        correct = (e.get("decision") == final) or (e.get("decision") == "pass" and final == "pass")
        s = _score_of(scores, uid)
        s["bad"] = s.get("bad", 0)
        if correct:
            s["repu"] = min(200, s["repu"] + VOTE_CORRECT)
            s["streak"] += 1; s["bad"] = 0
            bonus = 0; reason = "投票与裁决一致"
            if s["streak"] >= 5:
                bonus = STREAK_5_CORRECT; s["repu"] = min(200, s["repu"] + bonus)
                reason += f"+连续5次{bonus}"
        else:
            s["repu"] = max(READONLY - 5, s["repu"] + VOTE_WRONG)
            s["streak"] = 0; s["bad"] += 1
            bonus = 0; reason = "投票与裁决不一致"
            if s["bad"] >= 5:
                bonus = STREAK_5_WRONG; s["repu"] = max(READONLY - 5, s["repu"] + bonus)
                reason += f"+连续5次{bonus}"
        s["cont"] = s.get("cont", 0) + 1
        _a("reputation", {"ts": _ts(), "uid": uid, "delta": 0, "reason": reason,
                          "repu": s["repu"], "ref": ref, "dna": DNA})
        done.add(key); n += 1
    _save_scores(scores)
    json.dump(sorted(done), open(p, "w"))
    print(f"✅ sync 完成: 处理 {n} 条表决 · 信誉已按裁决一致性更新 (写死常量 +1/−2/连续±)")
    return 0

def _cmd_leaderboard(a):
    scores = _load_scores()
    if not scores:
        print("ℹ️ 无数据 · `lh gov sync` 或 `lh gov score <uid> add <v> --reason ...`")
        return 0
    rows = sorted(scores.items(), key=lambda kv: (-kv[1]["contrib"], -kv[1]["repu"]))
    print(f"{'用户':<16} {'贡献':<8} {'信誉':<8} 状态")
    for uid, s in rows[:20]:
        print(f"{uid:<16} {s['contrib']:<8} {s['repu']:<8} {repu_state(s['repu'])}")
    return 0

# ── 红线 ─────────────────────────────────────────────────────────────
def _load_rules():
    p = os.path.join(HOME, "red_rules.json")
    if not os.path.exists(p):
        return {"version": "0", "dna": DNA, "rules": []}
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return {"version": "0", "dna": DNA, "rules": []}

def _cmd_redline(a):
    rules = _load_rules()
    if not a.check:
        print(f"红线库 v{rules.get('version')} · {len(rules['rules'])} 条（系统主权红线·非政治词表）")
        for r in rules["rules"]:
            print(f"  {r['id']}  {r['desc']}")
        print(f"\n国家法律红线 → 语义审查+人工/仲裁裁决（不公开词表自动熔断·防误伤）")
        return 0
    text = " ".join(a.check)
    hit = [r for r in rules["rules"] if any(k in text for k in r.get("patterns", []))]
    if hit:
        for r in hit:
            print(f"🔴 命中 {r['id']} {r['desc']} → 记录耻辱墙 + 自动升堂解封提案(major≥3/4+公示72h)")
        return 2
    print("🟢 未命中系统主权红线")
    return 0

# ── dashboard ────────────────────────────────────────────────────────
def _cmd_dashboard(a):
    scores = _load_scores()
    rules = _load_rules()
    out = []
    out.append("# 🐉 龍魂·三色治理总览 v2.1")
    out.append("")
    out.append(f"- DNA: `{DNA}`")
    out.append(f"- GPG: `{GPG}`")
    out.append(f"- CONFIRM: `{CONFIRM}`")
    out.append(f"- 生成: {_now()} · [丙午·丁酉·辛巳·巳时·䷝离·🟢]")
    out.append("")
    out.append("## 三色状态")
    out.append("| 层 | 状态 | 执行 |")
    out.append("|---|:---:|---|")
    out.append("| 🟢 自动放行 | 机器 | `lh health` · 三色审计 (不可设前置人工审批) |")
    out.append("| 🟡 公开裁决 | 审批团5席 | `lh council` · quorum≥2/3 · 48h · 超时默认拒绝 |")
    out.append("| 🔴 主权红线 | 程序记录 | `lh gov redline` · 耻辱墙 + 公开重审(major≥3/4) |")
    out.append("")
    out.append("## 信誉/贡献榜 (前10)")
    out.append("| 用户 | 贡献 | 信誉 | 状态 |")
    out.append("|---|:---:|:---:|---|")
    rows = sorted(scores.items(), key=lambda kv: (-kv[1]["contrib"], -kv[1]["repu"]))[:10]
    for uid, s in rows:
        out.append(f"| {uid} | {s['contrib']} | {s['repu']} | {repu_state(s['repu'])} |")
    if not rows:
        out.append("| (空 · `lh gov sync` 同步) | | | |")
    out.append("")
    out.append(f"## 红线库 ({len(rules['rules'])} 条)")
    for r in rules["rules"]:
        out.append(f"- {r['id']} {r['desc']}")
    out.append("")
    out.append("> 凡涉「人」的裁决皆提案上链·审批团多签·社区公示·append-only 永不可抹。")
    out.append("> 篡改即断链 (`lh council verify`)")
    body = "\n".join(out)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(body)
        print(f"📊 已输出 {a.out}")
    else:
        print(body)
    return 0

def main():
    ap = argparse.ArgumentParser(description="龍魂·三色治理指挥层 v2.1（薄胶水·复用既有引擎）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("status", help="系统三色状态"); p1.set_defaults(fn=_cmd_status)
    p2 = sub.add_parser("propose", help="提议🟡/🔴 → 自动升堂 council")
    p2.add_argument("entity"); p2.add_argument("--color", choices=["y", "r"], default="y")
    p2.add_argument("--title", default="待公开裁决"); p2.add_argument("--as", dest="as_alias")
    p2.set_defaults(fn=_cmd_propose)
    p3 = sub.add_parser("vote", help="转发审批团表决")
    p3.add_argument("id"); p3.add_argument("--approve", action="store_true")
    p3.add_argument("--reject", action="store_true"); p3.add_argument("-r", "--reason")
    p3.add_argument("--as", dest="as_alias"); p3.set_defaults(fn=_cmd_vote)
    p4 = sub.add_parser("audit", help="提案完整证据链"); p4.add_argument("id"); p4.set_defaults(fn=_cmd_audit)
    p5 = sub.add_parser("trace", help="ledger 决策全链"); p5.add_argument("id"); p5.set_defaults(fn=_cmd_trace)
    p6 = sub.add_parser("score", help="贡献值 calc/登记(--add)")
    p6.add_argument("uid"); p6.add_argument("--add", type=int)
    p6.add_argument("--reason"); p6.add_argument("--dr", action="store_true"); p6.set_defaults(fn=_cmd_score)
    p7 = sub.add_parser("score-log", help="贡献事件明细"); p7.add_argument("uid"); p7.set_defaults(fn=_cmd_score_log)
    p8 = sub.add_parser("check", help="投票资格门槛"); p8.add_argument("uid"); p8.set_defaults(fn=_cmd_check)
    p9 = sub.add_parser("trust", help="信誉分+历史"); p9.add_argument("uid"); p9.set_defaults(fn=_cmd_trust)
    p10 = sub.add_parser("sync", help="扫 council ledger 自动更新信誉"); p10.set_defaults(fn=_cmd_sync)
    p11 = sub.add_parser("leaderboard", help="排行前20"); p11.set_defaults(fn=_cmd_leaderboard)
    p12 = sub.add_parser("redline", help="红线库查看/命中检测")
    p12.add_argument("check", nargs="*"); p12.set_defaults(fn=_cmd_redline)
    p13 = sub.add_parser("dashboard", help="Markdown 治理总览"); p13.add_argument("--out"); p13.set_defaults(fn=_cmd_dashboard)
    a = ap.parse_args()
    try:
        rc = a.fn(a)
    except KeyboardInterrupt:
        return 130
    return rc if isinstance(rc, int) else 0

if __name__ == "__main__":
    sys.exit(main())
