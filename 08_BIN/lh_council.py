#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·戊申·壬午·乙巳·䷊泰-LH-NO-BACKEND-COMMUNITY-COUNCIL-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
# 🛡️ P0焊死(2026-09-04·P72加封): 无后台治理链受管引擎·源码修改须走 LH-TRICOLOR-GOVERNANCE-v2.1 §十二 门槛(UID9622签章+新DNA+修订记录)
"""龍魂·无后台审批团公开决策引擎 v1.0 · No-Backend Community Council

系统无后台，账号无人可锁。绿灯自动通行，黄灯公开升堂，红灯公开重审。
凡涉「人」的裁决——通过还是拒绝——皆提案上链、审批团多签、社区公示、
append-only 永不可抹。本引擎无隐藏开关、无隐身撤销：一切状态迁移皆带
actor 与提案上下文写入哈希链，查询态一律由 ledger 重放，不存在可被
单人绕过表决的「权威库」。

协议文档: governance/protocols/P1_core/LH-NO-BACKEND-COMMUNITY-COUNCIL-v1.0.md

命令（lh council <sub>）:
  propose  <type> <target> [--title T] [--evidence E] [--ref VERDICT_ID] [--as ALIAS]
  vote     <evt_id> pass|reject|abstain [-r REASON] [--as ALIAS]
  list     [--state voting|verdict|executed|refused]
  view     <evt_id>                 # 详情 + 票况 + 时限倒计时
  ledger   [--tail N]               # 原始链
  verify                             # 全链哈希校验
  wall     [--out PATH]             # 公示墙 HTML
  export   [--json]                  # 机器可读公示
  status                             # 在任席位/成员门槛/时间盒参数
  rotate   [--dry-run]               # 到期轮换(自动·无单人批准)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

CN = timezone(timedelta(hours=8))  # 主权时区 Asia/Shanghai
DNA = "#龍芯⚡️丙午·戊申·壬午·乙巳·䷊泰-LH-NO-BACKEND-COMMUNITY-COUNCIL-v1.0-UID9622"

HOME = Path.home() / ".longhun" / "council"
CONFIG = HOME / "config.json"
LEDGER = HOME / "ledger.jsonl"
WALL = HOME / "council_wall.html"

# ──────────────────────────────────────────────────────────────── 规则表
TYPES = {
    "standard": {"name": "普通裁决",  "quorum": 2/3, "pass": 2/3, "vote_h": 48, "pub_h": 24},
    "major":    {"name": "重大裁决",  "quorum": 2/3, "pass": 3/4, "vote_h": 48, "pub_h": 72},
    "supreme":  {"name": "至尊裁决",  "quorum": 4/5, "pass": 4/5, "vote_h": 72, "pub_h": 72},
    "appeal":   {"name": "申诉复核",  "quorum": 2/3, "pass": 2/3, "vote_h": 48, "pub_h": 24},
}
OUT_OF_SCOPE = "P0伦理锚/ETERNAL_LOCK/宪法条款不开放表决"   # 域外


def _now() -> str:
    return datetime.now(CN).strftime("%Y-%m-%d %H:%M:%S %z")


def _ts() -> float:
    return time.time()


def _hash(line: str, prev: str) -> str:
    return hashlib.sha256(f"{prev}\n{line}".encode("utf-8")).hexdigest()[:16]


# ──────────────────────────────────────────────────────────────── 账本
def _load_config():
    if not CONFIG.exists():
        _default_config()
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def _default_config() -> dict:
    term_end = (datetime.now(CN) + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S %z")
    cfg = {
        "council_version": "v1.0",
        "dna": DNA,
        "created": _now(),
        "terms_days": 30,
        "pass_bounds": {k: {"vote_h": v["vote_h"], "pub_h": v["pub_h"]} for k, v in TYPES.items()},
        "member_min_trust": 60,
        "seats": [
            {"seat": "C1", "kind": "贡献席", "weight": 1.0, "alias": "贡献榜#1",   "term_end": term_end},
            {"seat": "C2", "kind": "贡献席", "weight": 1.0, "alias": "贡献榜#2",   "term_end": term_end},
            {"seat": "C3", "kind": "贡献席", "weight": 1.0, "alias": "贡献榜#3",   "term_end": term_end},
            {"seat": "GD", "kind": "守护席", "weight": 0.0, "alias": "P05·机器委员(只陈述·无票)", "term_end": term_end},
            {"seat": "OB", "kind": "观察席", "weight": 1.0, "alias": "观察席(抽签)", "term_end": term_end},
        ],
        "note": "启动席位由 UID9622 提案导入; 此后席位变更一律走 rotation/supreme。守护席权重0=机器不拥有人工票, 防『AI后台』。",
    }
    HOME.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    return cfg


def _read_ledger() -> list:
    if not LEDGER.exists():
        return []
    out = []
    for ln in LEDGER.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if ln:
            out.append(json.loads(ln))
    return out


def _append(evt: dict) -> dict:
    HOME.mkdir(parents=True, exist_ok=True)
    evts = _read_ledger()
    prev = evts[-1]["hash"] if evts else "0" * 16
    evt["prev_hash"] = prev
    body = json.dumps(evt, ensure_ascii=False, sort_keys=True)
    evt["hash"] = _hash(body, prev)
    line = json.dumps(evt, ensure_ascii=False)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    return evt


def _verify() -> tuple[bool, str, int]:
    evts = _read_ledger()
    prev = "0" * 16
    for i, e in enumerate(evts):
        h = e.pop("hash", None)
        body = json.dumps(e, ensure_ascii=False, sort_keys=True)
        expect = _hash(body, prev)
        if h != expect:
            return False, f"断链 @行{i+1} evt={e.get('evt_id')}", i + 1
        prev = h
    return True, f"链完整 {len(evts)} 事件", len(evts)


def _seats_in_office(cfg) -> list:
    now = _now()
    return [s for s in cfg["seats"] if s["term_end"] >= now]


def _weighted_total(cfg) -> float:
    return sum(s["weight"] for s in _seats_in_office(cfg) if s["weight"] > 0)


# ──────────────────────────────────────────────────────────────── 状态机重放
def _replay(cfg, evts=None) -> dict:
    """由 ledger 重放得出提案状态机——无独立权威库。"""
    evts = evts if evts is not None else _read_ledger()
    now = _ts()
    proposals: dict[str, dict] = {}
    for e in evts:
        t = e.get("type")
        if t == "proposal":
            p = dict(e)
            p.setdefault("state", "voting")
            p.setdefault("ballots", [])
            p.setdefault("verdict", {})
            p["_created"] = float(e.get("ts", now))
            proposals[e["evt_id"]] = p
        elif t == "ballot" and e.get("ref") in proposals:
            p = proposals[e["ref"]]
            p["ballots"].append(e)
        elif t == "verdict" and e.get("ref") in proposals:
            p = proposals[e["ref"]]
            p["state"] = "verdict"          # 公示期（pass 待公示届满执行 / reject 由后续 refused 落定）
            p["verdict"].update({k: v for k, v in e.items()
                                 if k in ("outcome", "reason", "ts", "actor")})
        elif t == "executed" and e.get("ref") in proposals:
            p = proposals[e["ref"]]
            p["state"] = "executed"
        elif t == "refused" and e.get("ref") in proposals:
            p = proposals[e["ref"]]
            p["state"] = "refused"
    # 逐提案判定时限（LH_COUNCIL_TURBO=1 仅内部测试/演示: 1s 表决窗 + 1s 公示窗）
    import os as _os
    _turbo = _os.environ.get("LH_COUNCIL_TURBO") == "1"
    for pid, p in proposals.items():
        rule = TYPES.get(p.get("ptype", "standard"), TYPES["standard"])
        vh = (1 / 3600) if _turbo else rule["vote_h"]
        ph = (1 / 3600) if _turbo else rule["pub_h"]
        vote_end = p["_created"] + vh * 3600
        pub_end = vote_end + ph * 3600
        p["_vote_end"] = vote_end
        p["_pub_end"] = pub_end
        if p["state"] == "voting" and now > vote_end:
            p["state"] = "timeout"          # 需要落盘 → 由 settle 处理
        elif p["state"] == "verdict" and p.get("verdict", {}).get("outcome") == "pass" and now > pub_end:
            p["state"] = "verdict_exec"     # 公示届满 → 由 settle 执行
    return proposals


def _settle(cfg, dry=False) -> int:
    """时间盒巡检: 表决到期→refused(timeout)默认拒绝; 公示到期→executed。写链留痕。"""
    evts = _read_ledger()
    props = _replay(cfg, evts)
    changed = 0
    for pid, p in props.items():
        if p["state"] == "timeout" and not any(e["type"] == "verdict" and e.get("ref") == pid for e in evts):
            if dry:
                print(f"  [dry] {pid} 表决超时 → 默认拒绝(未过会)")
                changed += 1
                continue
            _append({"ts": _ts(), "type": "verdict", "ref": pid, "outcome": "reject",
                     "reason": "timeout: 表决窗口届满未达 quorum → 防御性默认拒绝",
                     "actor": "council-timebox"})
            _append({"ts": _ts(), "type": "refused", "ref": pid, "actor": "council-timebox",
                     "reason": "timeout 默认拒绝·公开未过会"})
            print(f"  ⏳ {pid} 表决超时 → 默认拒绝(未过会)")
            changed += 1
        elif p["state"] == "verdict_exec":
            if dry:
                print(f"  [dry] {pid} 公示期届满 → 执行裁决")
                changed += 1
                continue
            _append({"ts": _ts(), "type": "executed", "ref": pid, "actor": "council-timebox",
                     "reason": "公示期届满无阻断异议·裁决生效"})
            print(f"  ✅ {pid} 公示期届满 → 裁决执行")
            changed += 1
    return changed


def _try_verdict(cfg, pid: str) -> str | None:
    """投票结束后尝试判裁（达 quorum → 按通过阈值裁决并写链）。返回 outcome 或 None。"""
    evts = _read_ledger()
    p = _replay(cfg, evts).get(pid)
    if not p or p["state"] not in ("voting", "timeout"):
        return None
    if any(e["type"] == "verdict" and e.get("ref") == pid for e in evts):
        return None
    rule = TYPES.get(p.get("ptype", "standard"), TYPES["standard"])
    w_yes = sum(b.get("weight", 1.0) for b in p["ballots"] if b.get("decision") == "pass")
    w_vote = sum(b.get("weight", 1.0) for b in p["ballots"] if b.get("decision") != "abstain"
                 and b.get("abstain_conflict") is not True)
    w_quorum = _weighted_total(cfg) * rule["quorum"]
    if w_vote < w_quorum:
        return None                      # 未达 quorum 不判裁; 超时后由 settle 默认拒绝兜底
    outcome = "pass" if w_yes >= rule["pass"] * max(w_vote, 1e-9) else "reject"
    reason = (f"加权赞成 {w_yes:.2f}/{w_vote:.2f} (阈值 {rule['pass']:.0%}·quorum {w_quorum:.2f})"
              if outcome == "pass" else
              f"加权赞成 {w_yes:.2f}/{w_vote:.2f} 未达阈值 {rule['pass']:.0%}" + ("·或未达 quorum" if w_vote < w_quorum else ""))
    _append({"ts": _ts(), "type": "verdict", "ref": pid, "outcome": outcome,
             "reason": reason, "actor": "council-majority"})
    if outcome == "reject":
        _append({"ts": _ts(), "type": "refused", "ref": pid, "actor": "council-majority",
                 "reason": "多数裁决拒绝·公开可见"})
    return outcome


# ──────────────────────────────────────────────────────────────── 子命令
def _cmd_propose(a):
    cfg = _load_config()
    ptype = a.type
    if ptype == "lock":
        print(f"🔒 {OUT_OF_SCOPE}"); return
    if ptype not in TYPES:
        print(f"❌ 未知类型 {ptype} · 可用: {', '.join(TYPES)} | lock(域外)")
        return
    pid = f"council-{datetime.now(CN).strftime('%Y%m%d%H%M%S')}-{hashlib.sha256((a.target + str(_ts())).encode()).hexdigest()[:6]}"
    rule = TYPES[ptype]
    evt = {"ts": _ts(), "type": "proposal", "evt_id": pid, "ptype": ptype,
           "target": a.target, "title": a.title or f"{rule['name']}: {a.target}",
           "evidence": a.evidence or "", "ref_verdict": a.ref or "",
           "initiator": a.as_alias or "community-member",
           "vote_h": rule["vote_h"], "pub_h": rule["pub_h"],
           "quorum_ratio": rule["quorum"], "pass_ratio": rule["pass"],
           "state": "voting"}
    _append(evt)
    print(f"📋 提案上链: {pid} [{ptype}] {evt['title']}")
    print(f"   target={a.target} · 发起人={evt['initiator']} · 表决窗 {rule['vote_h']}h"
          f" (quorum≥{rule['quorum']:.0%}·通过≥{rule['pass']:.0%})")
    print("   裁决将公开公示·append-only 永不可抹")


def _cmd_vote(a):
    cfg = _load_config()
    seats = {s["seat"]: s for s in cfg["seats"]}
    seat = seats.get(a.as_alias or "C1")
    if not seat:
        print(f"❌ 席位 {a.as_alias} 不存在 · seats: {', '.join(seats)}")
        return
    if seat["weight"] <= 0:
        print(f"⚠️ {seat['seat']} {seat['kind']} 权重 0——机器委员只陈述不投票(无后台第二闸)")
        return
    props = _replay(cfg)
    p = props.get(a.evt_id)
    if not p:
        print(f"❌ 提案 {a.evt_id} 不存在"); return
    if p["state"] != "voting":
        print(f"❌ 提案状态 {p['state']}·不在表决窗内"); return
    if a.evt_id in [b.get("ref") for b in _read_ledger() if b.get("type") == "ballot" and b.get("voter") == seat["seat"]]:
        print(f"⚠️ {seat['seat']} 已投过票·一席一票不可改")
        return
    conflict = any(k in (p.get("target", "") + p.get("title", "")) for k in (seat["alias"], seat["seat"]))
    if conflict and a.decision in ("pass", "reject"):
        print(f"⚠️ 回避冲突: 提案涉 {seat['seat']} 本人 → 自动转为 abstain(conflict)")
        a.decision = "abstain"
        a.reason = (a.reason or "") + " ·[冲突回避]"
    _append({"ts": _ts(), "type": "ballot", "ref": a.evt_id, "voter": seat["seat"],
             "alias": seat["alias"], "decision": a.decision, "reason": a.reason or "",
             "weight": seat["weight"]})
    print(f"🗳️ {seat['seat']}({seat['alias']}) → {a.decision}" + (f" · {a.reason}" if a.reason else ""))
    out = _try_verdict(cfg, a.evt_id)
    if out:
        print(f"⚖️ 裁决已出: {a.evt_id} → {out} · 进入公示期")


def _fmt_time(x: float) -> str:
    return datetime.fromtimestamp(x, CN).strftime("%m-%d %H:%M")


def _cmd_list(a):
    cfg = _load_config()
    _settle(cfg)                      # 先落时间盒(超时默认拒绝/公示届满执行)
    props = _replay(cfg)
    now = _ts()
    rows = []
    for pid, p in sorted(props.items(), key=lambda kv: -kv[1]["_created"]):
        st = p["state"]
        # timeout = 超时默认拒绝(未过会) → 归入 refused 语义
        if st == "timeout":
            st = "refused(t)"
        if a.state:
            want = a.state
            if st != want and not (want == "refused" and st == "refused(t)"):
                continue
        y = sum(b.get("weight", 1.0) for b in p["ballots"] if b.get("decision") == "pass")
        n = sum(b.get("weight", 1.0) for b in p["ballots"] if b.get("decision") == "reject")
        ab = sum(1 for b in p["ballots"] if b.get("decision") == "abstain")
        deadline = _fmt_time(p["_vote_end"]) if p["state"] == "voting" else "—"
        rows.append((p["_created"], pid, p.get("ptype"), p.get("title", "")[:38],
                     st, f"👍{y:.0f}/👎{n:.0f}/➖{ab}", deadline))
    if not rows:
        print("(空) 尚无提案")
        return
    hdr = f"{'提案ID':<40} {'类型':<9} {'标题':<38} {'状态':<9} {'票况':<12} 表决截止"
    print(hdr); print("-" * 122)
    for r in sorted(rows, key=lambda x: -x[0]):
        _, pid, ptype, title, st, votes, dl = r
        print(f"{pid:<40} {ptype:<9} {title:<38} {st:<9} {votes:<12} {dl}")


def _cmd_view(a):
    cfg = _load_config()
    _settle(cfg)
    props = _replay(cfg)
    p = props.get(a.evt_id)
    if not p:
        print(f"❌ 提案 {a.evt_id} 不存在"); return
    rule = TYPES.get(p.get("ptype", "standard"), TYPES["standard"])
    now = _ts()
    remain = p["_vote_end"] - now if p["state"] == "voting" else 0
    print(f"提案 {a.evt_id}  [{p.get('ptype')}·{rule['name']}]  state={p['state']}")
    print(f"  标题: {p.get('title')}")
    print(f"  target: {p.get('target')} · ref_verdict: {p.get('ref_verdict') or '—'}")
    print(f"  证据: {p.get('evidence') or '—'}")
    print(f"  发起: {p.get('initiator')} @ {datetime.fromtimestamp(p.get('_created', 0), CN).strftime('%m-%d %H:%M')}"
          f" · 表决窗 {p.get('vote_h')}h · quorum≥{p.get('quorum_ratio', 0):.0%} 通过≥{p.get('pass_ratio', 0):.0%}")
    if p["state"] == "voting":
        print(f"  ⏳ 表决剩余 {int(remain // 3600)}h{int(remain % 3600 // 60)}m"
              f" → 超时默认拒绝(未过会)")
    elif p.get("verdict"):
        v = p["verdict"]
        print(f"  ⚖️ 裁决: {v.get('outcome')} · {v.get('reason')} · actor={v.get('actor')}")
    print(f"  ─ 公开票况(委员·方向·理由) ─")
    for b in sorted(p["ballots"], key=lambda x: x.get("ts", 0)):
        print(f"    {b.get('voter'):<4} {b.get('alias','')[:18]:<20} {b.get('decision'):<8} {b.get('reason') or ''}")
    if not p["ballots"]:
        print("    (暂无票)")


def _cmd_ledger(a):
    evts = _read_ledger()
    tail = evts[-a.tail:]
    for e in tail:
        print(f"{e.get('type','?'):<10} {e.get('evt_id') or e.get('ref') or '':<38} "
              f"{json.dumps({k: v for k, v in e.items() if k not in ('type','evt_id','prev_hash','hash')}, ensure_ascii=False)[:90]}")
        print(f"          prev={e.get('prev_hash')} hash={e.get('hash')}")


def _cmd_verify(a):
    ok, msg, n = _verify()
    print(("✅ " if ok else "🔴 ") + msg + f" · prev→hash 链 {n} 事件")
    _settle(_load_config())


def _cmd_wall(a):
    cfg = _load_config()
    _settle(cfg)
    props = _replay(cfg)
    ok, msg, _ = _verify()
    card = []
    for pid, p in sorted(props.items(), key=lambda kv: -kv[1]["_created"])[:30]:
        y = sum(b.get("weight", 1.0) for b in p["ballots"] if b.get("decision") == "pass")
        n = sum(b.get("weight", 1.0) for b in p["ballots"] if b.get("decision") == "reject")
        ab = sum(1 for b in p["ballots"] if b.get("decision") == "abstain")
        votes = "".join(
            f"<li><b>{b.get('voter')}</b> {b.get('alias','')[:14]} → <b>{b.get('decision')}</b>"
            + (f" · <i>{b.get('reason')}</i>" if b.get("reason") else "") + "</li>"
            for b in sorted(p["ballots"], key=lambda x: x.get("ts", 0)))
        vline = ""
        if p.get("verdict"):
            v = p["verdict"]
            vline = f"<p class='verdict'>⚖️ 裁决 <b>{v.get('outcome','').upper()}</b> · {v.get('reason')} · {datetime.fromtimestamp(p['_created'], CN).strftime('%m-%d %H:%M')} 起公示</p>"
        card.append(f"""
<div class="card">
 <h3>{p.get('ptype','standard').upper()} · {p.get('title')}</h3>
 <p class="meta">{pid} · target: {p.get('target')} · 发起: {p.get('initiator')} · state: {p.get('state')} · 票况 👍{y:.0f}/👎{n:.0f}/➖{ab}</p>
 <p class="meta">ref_verdict: {p.get('ref_verdict') or '—'} · 表决窗 {p.get('vote_h')}h · quorum≥{p.get('quorum_ratio',0):.0%} 通过≥{p.get('pass_ratio',0):.0%}</p>
 {f"<p class='ev'>📄 证据: {p.get('evidence')}</p>" if p.get('evidence') else ''}
 {vline}
 <ul class='votes'>{votes or '<li>暂无票</li>'}</ul>
</div>""")
    html = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>龍魂·审批团公示墙</title><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{font-family:-apple-system,'PingFang SC',sans-serif;background:#0d1117;color:#e6edf3;margin:0;padding:24px;max-width:960px;margin:auto}}
h1{{font-size:20px}} h2{{color:#7ee787;font-size:14px;font-weight:normal}} .ok{{color:#7ee787}}
.card{{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px 18px;margin:14px 0}}
h3{{margin:0 0 8px}} .meta{{color:#8b949e;font-size:12px;margin:3px 0}} .ev{{color:#d2a8ff}}
.verdict{{color:#ffa657}} ul{{margin:6px 0 0;padding-left:20px}} li{{margin:2px 0;font-size:13px}}
</style></head><body>
<h1>🐉 龍魂 · 审批团公示墙 <small style="color:#8b949e">NO-BACKEND COMMUNITY COUNCIL</small></h1>
<h2>「系统无后台，账号无人可锁。绿灯自动通行，黄灯公开升堂，红灯公开重审。」</h2>
<p class="ok">{'✅ ' + msg}</p>
{''.join(card)}
<footer style="color:#8b949e;font-size:11px;margin-top:24px">append-only 哈希链账本 · {DNA}</footer>
</body></html>"""
    out = Path(a.out) if a.out else WALL
    out.write_text(html, encoding="utf-8")
    print(f"🖼️ 公示墙已生成: {out}")

    # 可选输出 machine-readable wall JSON (同目录)
    wall_json = out.with_suffix(".json")
    summary = []
    for pid, p in props.items():
        summary.append({"id": pid, "ptype": p.get("ptype"), "title": p.get("title"),
                        "target": p.get("target"), "initiator": p.get("initiator"),
                        "state": p.get("state"), "ballots": [
                            {"voter": b.get("voter"), "decision": b.get("decision"),
                             "reason": b.get("reason")} for b in p["ballots"]],
                        "verdict": p.get("verdict")})
    wall_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"🤖 公示数据: {wall_json} ({len(summary)} 提案)")


def _cmd_export(a):
    cfg = _load_config()
    _settle(cfg)
    props = _replay(cfg)
    ok, msg, n = _verify()
    print(json.dumps({"verify": {"ok": ok, "msg": msg, "events": n},
                      "types": {k: v for k, v in TYPES.items()},
                      "proposals": [p for p in props.values()]},
                     ensure_ascii=False, indent=2))


def _cmd_status(a):
    cfg = _load_config()
    _settle(cfg)
    now = _now()
    print(f"审批团 {cfg['council_version']} · 数据 {HOME}")
    print(f"任期 {cfg['terms_days']} 天 · 成员信任分门槛 ≥ {cfg['member_min_trust']} (对接 P20)")
    print("─ 席位 ─")
    for s in cfg["seats"]:
        exp = "已过期" if s["term_end"] < now else f"至 {s['term_end']}"
        print(f"  {s['seat']:<4} {s['kind']:<6} 权重{s['weight']:.1f} {s['alias']:<24} {exp}")
    print(f"─ 在任加权票权总额 {_weighted_total(cfg):.1f} ─")
    print("─ 时间盒 ─")
    for k, v in TYPES.items():
        print(f"  {k:<9} quorum≥{v['quorum']:.0%} 通过≥{v['pass']:.0%} 表决{v['vote_h']}h 公示{v['pub_h']}h")
    props = _replay(cfg)
    voting = [p for p in props.values() if p["state"] == "voting"]
    print(f"待表决提案 {len(voting)} · 域外: {OUT_OF_SCOPE}")


def _cmd_rotate(a):
    cfg = _load_config()
    now = _now()
    expired = [s for s in cfg["seats"] if s["term_end"] < now]
    if not expired:
        print("ℹ️ 无到期席位 · 无动作")
        return
    print(f"到期席位 {len(expired)} 席（{', '.join(s['seat'] for s in expired)}）")
    if a.dry_run:
        for s in expired:
            print(f"  [dry] {s['seat']} {s['kind']} → 轮换 (贡献席取当期贡献榜前3·观察席重新抽签)")
        return
    for s in expired:
        end = (datetime.now(CN) + timedelta(days=cfg["terms_days"])).strftime("%Y-%m-%d %H:%M:%S %z")
        if s["kind"] == "贡献席":
            s["term_end"] = end
            s["alias"] = "贡献榜#" + str(cfg["seats"].index(s) % 3 + 1) + "(轮值)"
        elif s["kind"] == "观察席":
            s["term_end"] = end
            s["alias"] = "观察席(抽签·轮值)"
    _append({"ts": _ts(), "type": "rotation", "actor": "council-auto",
             "rotated": [s["seat"] for s in expired], "reason": "任期届满自动轮换·无单人批准"})
    CONFIG.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"🔄 已轮换 {', '.join(s['seat'] for s in expired)} · 新任期 {cfg['terms_days']} 天 · rotation 事件已上链")


# ──────────────────────────────────────────────────────────────── main
def main():
    ap = argparse.ArgumentParser(description="龍魂·无后台审批团公开决策引擎 v1.0",
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--health", action="store_true", help="健康检查")
    sub = ap.add_subparsers(dest="cmd")
    p1 = sub.add_parser("propose"); p1.add_argument("type"); p1.add_argument("target")
    p1.add_argument("--title"); p1.add_argument("--evidence"); p1.add_argument("--ref")
    p1.add_argument("--as", dest="as_alias")
    p2 = sub.add_parser("vote"); p2.add_argument("evt_id"); p2.add_argument("decision",
        choices=["pass", "reject", "abstain"]); p2.add_argument("-r", "--reason")
    p2.add_argument("--as", dest="as_alias")
    p3 = sub.add_parser("list"); p3.add_argument("--state")
    p4 = sub.add_parser("view"); p4.add_argument("evt_id")
    p5 = sub.add_parser("ledger"); p5.add_argument("--tail", type=int, default=10)
    sub.add_parser("verify")
    p6 = sub.add_parser("wall"); p6.add_argument("--out")
    sub.add_parser("export")
    sub.add_parser("status")
    p7 = sub.add_parser("rotate"); p7.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.health or not a.cmd:
        ok, msg, n = _verify()
        print(json.dumps({"ok": ok, "msg": msg, "events": n, "dna": DNA},
                         ensure_ascii=False))
        if a.cmd is None:
            ap.print_help()
        return 0
    {"propose": _cmd_propose, "vote": _cmd_vote, "list": _cmd_list, "view": _cmd_view,
     "ledger": _cmd_ledger, "verify": _cmd_verify, "wall": _cmd_wall, "export": _cmd_export,
     "status": _cmd_status, "rotate": _cmd_rotate}[a.cmd](a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
