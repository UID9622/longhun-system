#!/usr/bin/env python3
"""
tricolor_flow.py · 三色流场引擎 v1.0
输入任意内容 → 四层自动流动 → DNA盖章出口

DNA: #龍芯⚡️2026-04-06-三色流场引擎-v1.0
作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）
献礼: 乔布斯·曾仕强·历代传递和平与爱的人
共建: Notion宝宝 × 终端宝宝 × 双脑联动

流场架构:
  入口层  — 数字根 + DNA验证 → 初始评分
  分流层  — 评分 → 绿/黄/红 三条水道
  处理层  — 🟢直接执行 / 🟡补证据等确认 / 🔴熔断取证
  出口层  — DNA盖章 · 草日志写入 · 证据链归档

评分规则（100分制）:
  身份校验  30 — UID9622确认码匹配
  DNA追溯   30 — #龍芯⚡️前缀正确
  内容安全  20 — 无危险关键词
  伦理检查  20 — 无操控/泄露行为
  ≥80=🟢  ≥50=🟡  <50=🔴
"""

import re
import sys
import json
import time
import hashlib
import hmac
from pathlib import Path
from typing import Any

BASE    = Path.home() / "longhun-system"
LOGS    = BASE / "logs"
BIN     = BASE / "bin"
DNA_TAG = "#龍芯⚡️2026-04-06-三色流场引擎-v1.0"
GPG_FP  = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
UID     = "9622"
CONFIRM = "LK9X-772Z"

LEDGER_FILE = LOGS / "tricolor_flow.jsonl"
LOGS.mkdir(exist_ok=True)

# ══════════════════════════════════════════════════════
# 工具函数
# ══════════════════════════════════════════════════════

def digital_root(n: int) -> int:
    """DR(n) = 1 + ((n-1) % 9)  ·  n=0时返回0"""
    return 0 if n == 0 else 1 + (n - 1) % 9

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def hmac_sign(text: str) -> str:
    key = (GPG_FP + UID).encode()
    return hmac.new(key, text.encode(), hashlib.sha256).hexdigest()[:16]

def now_ts() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")

def make_dna(label: str) -> str:
    return f"#龍芯⚡️{time.strftime('%Y-%m-%d')}-{label}-UID{UID}"

# ══════════════════════════════════════════════════════
# 入口层  — 数字根 + DNA验证 → 初始评分
# ══════════════════════════════════════════════════════

# 危险关键词（内容安全 -20）
DANGER_WORDS = [
    "造假", "骗钱", "害民", "泄露隐私", "绕过审计",
    "删除日志", "篡改", "bypass", "exploit", "shell injection",
    "rm -rf", "drop table", "exec(", "__import__",
]

# 伦理风险词（伦理检查 -20）
ETHICS_WORDS = [
    "操控用户", "卖数据", "偷收", "未授权", "境外服务器",
    "绕过铁律", "覆盖DNA", "伪造身份",
]

# DNA模式
DNA_PATTERNS = [
    r'#龍芯⚡️\d{4}-\d{2}-\d{2}',
    r'#龙芯⚡️\d{4}-\d{2}-\d{2}',
    r'#ZHUGEXIN⚡️',
    r'#LUCKY⚡️',
    r'#STAR⚡️',
]


class EntryLayer:
    """入口层：数字根计算 + DNA验证 + 初始评分"""

    def process(self, text: str, meta: dict) -> dict:
        score   = 0
        details = {}

        # ── 身份校验（30分）
        uid_ok = (UID in text) or meta.get("uid_confirmed", False)
        cc_ok  = (CONFIRM in text) or meta.get("confirm_code", False)
        id_score = 30 if (uid_ok and cc_ok) else (15 if uid_ok else 0)
        score += id_score
        details["身份校验"] = {
            "分数": id_score, "满分": 30,
            "uid": uid_ok, "confirm": cc_ok,
        }

        # ── DNA追溯（30分）
        has_dna  = any(re.search(p, text) for p in DNA_PATTERNS)
        dna_score = 30 if has_dna else 0
        score += dna_score
        details["DNA追溯"] = {
            "分数": dna_score, "满分": 30,
            "有DNA": has_dna,
        }

        # ── 内容安全（20分）
        danger_hits = [w for w in DANGER_WORDS if w.lower() in text.lower()]
        safe_score  = 0 if danger_hits else 20
        score += safe_score
        details["内容安全"] = {
            "分数": safe_score, "满分": 20,
            "触发词": danger_hits,
        }

        # ── 伦理检查（20分）
        ethics_hits = [w for w in ETHICS_WORDS if w.lower() in text.lower()]
        eth_score   = 0 if ethics_hits else 20
        score += eth_score
        details["伦理检查"] = {
            "分数": eth_score, "满分": 20,
            "触发词": ethics_hits,
        }

        # ── 数字根
        dr = digital_root(score)

        return {
            "score":   score,
            "dr":      dr,
            "details": details,
            "text_hash": sha256(text),
            "ts": now_ts(),
        }


# ══════════════════════════════════════════════════════
# 分流层  — 评分 → 绿/黄/红
# ══════════════════════════════════════════════════════

class RouterLayer:
    """分流层：评分映射到三条水道"""

    @staticmethod
    def route(score: int) -> dict:
        if score >= 80:
            return {
                "color":   "🟢",
                "channel": "green",
                "label":   "直通",
                "desc":    "评分充足·直接执行·留痕归档",
                "action":  "execute",
            }
        elif score >= 50:
            return {
                "color":   "🟡",
                "channel": "yellow",
                "label":   "减速",
                "desc":    "需补充证据·等老大确认",
                "action":  "hold",
            }
        else:
            return {
                "color":   "🔴",
                "channel": "red",
                "label":   "熔断",
                "desc":    "风险过高·停止·写入证据链",
                "action":  "block",
            }


# ══════════════════════════════════════════════════════
# 处理层  — 三条水道各自的处理逻辑
# ══════════════════════════════════════════════════════

class ProcessLayer:
    """处理层：根据水道执行不同动作"""

    def green(self, text: str, entry: dict) -> dict:
        """🟢 直接执行·留痕"""
        return {
            "action":   "executed",
            "result":   f"内容已通过三色审计·可安全执行",
            "留痕":     True,
            "dna_new":  make_dna("绿色通道"),
            "summary":  text[:80] + ("…" if len(text) > 80 else ""),
        }

    def yellow(self, text: str, entry: dict) -> dict:
        """🟡 补证据等确认"""
        missing = []
        d = entry["details"]
        if d["身份校验"]["分数"] < 30:
            missing.append("需要 UID9622 + 确认码")
        if d["DNA追溯"]["分数"] < 30:
            missing.append("需要 #龍芯⚡️DNA标签")
        if d["内容安全"]["触发词"]:
            missing.append(f"危险词待解释: {d['内容安全']['触发词']}")
        if d["伦理检查"]["触发词"]:
            missing.append(f"伦理词待解释: {d['伦理检查']['触发词']}")

        return {
            "action":   "hold",
            "result":   "内容进入黄色水道·等待补充",
            "缺失项":   missing,
            "dna_new":  make_dna("黄色待审"),
            "hint":     "补充以下信息后重新提交↑",
        }

    def red(self, text: str, entry: dict) -> dict:
        """🔴 熔断·取证"""
        evidence = {
            "触发词_安全":  entry["details"]["内容安全"]["触发词"],
            "触发词_伦理":  entry["details"]["伦理检查"]["触发词"],
            "得分":         entry["score"],
            "数字根":       entry["dr"],
            "内容摘要":     text[:60] + "…",
            "哈希":         entry["text_hash"],
            "时间":         entry["ts"],
        }
        return {
            "action":   "blocked",
            "result":   "此乃非道·早已早亡！内容已熔断·拒绝执行",
            "evidence": evidence,
            "dna_new":  make_dna("红色熔断"),
            "alert":    "⚠️ 证据已写入不可篡改账本",
        }

    def process(self, text: str, entry: dict, route: dict) -> dict:
        ch = route["channel"]
        if ch == "green":
            return self.green(text, entry)
        elif ch == "yellow":
            return self.yellow(text, entry)
        else:
            return self.red(text, entry)


# ══════════════════════════════════════════════════════
# 出口层  — DNA盖章 · 账本写入 · 证据链归档
# ══════════════════════════════════════════════════════

class ExitLayer:
    """出口层：DNA盖章 + 持久化"""

    def _write_ledger(self, record: dict):
        line = json.dumps(record, ensure_ascii=False)
        sig  = hmac_sign(line)
        with open(LEDGER_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps({**record, "_sig": sig}, ensure_ascii=False) + "\n")

    def process(self, text: str, entry: dict, route: dict, proc: dict) -> dict:
        dna_final = proc.get("dna_new", make_dna("出口"))

        record = {
            "ts":       entry["ts"],
            "dna":      dna_final,
            "gpg":      GPG_FP,
            "color":    route["color"],
            "channel":  route["channel"],
            "score":    entry["score"],
            "dr":       entry["dr"],
            "action":   proc["action"],
            "hash":     entry["text_hash"],
            "result":   proc.get("result", ""),
            "evidence": proc.get("evidence"),
            "missing":  proc.get("缺失项"),
        }

        self._write_ledger(record)

        return {
            "dna":      dna_final,
            "ledger":   str(LEDGER_FILE),
            "record_id": sha256(entry["ts"] + entry["text_hash"]),
        }


# ══════════════════════════════════════════════════════
# 流场主引擎
# ══════════════════════════════════════════════════════

class TricolorFlow:
    """
    三色流场引擎
    用法:
        flow = TricolorFlow()
        result = flow.run("任意内容")
        print(result["report"])
    """

    def __init__(self):
        self.entry   = EntryLayer()
        self.router  = RouterLayer()
        self.process = ProcessLayer()
        self.exit    = ExitLayer()

    def run(self, text: str, meta: dict = None, silent: bool = False) -> dict:
        if meta is None:
            meta = {}

        if not silent:
            print(f"\n🌊 三色流场启动")
            print(f"   DNA: {DNA_TAG}")
            print(f"   输入长度: {len(text)} 字符")
            print("─" * 50)

        # ── 入口层
        entry_result = self.entry.process(text, meta)
        score = entry_result["score"]
        dr    = entry_result["dr"]

        if not silent:
            print(f"\n【入口层】")
            for k, v in entry_result["details"].items():
                bar = "█" * (v["分数"] // 5) + "░" * ((v["满分"] - v["分数"]) // 5)
                hit = f"  ⚡{v.get('触发词', v.get('有DNA', v.get('uid', '')))}" if any(
                    v.get(x) for x in ["触发词", "有DNA", "uid"]
                ) else ""
                print(f"  {k:<8} {bar} {v['分数']:>2}/{v['满分']}{hit}")
            print(f"  总分: {score}/100  数字根: {dr}")

        # ── 分流层
        route = self.router.route(score)

        if not silent:
            print(f"\n【分流层】")
            print(f"  {route['color']} → {route['label']}水道  ·  {route['desc']}")

        # ── 处理层
        proc_result = self.process.process(text, entry_result, route)

        if not silent:
            print(f"\n【处理层】")
            print(f"  动作: {proc_result['action']}")
            print(f"  结果: {proc_result['result']}")
            if proc_result.get("缺失项"):
                for m in proc_result["缺失项"]:
                    print(f"    ⚠️  {m}")
            if proc_result.get("evidence"):
                ev = proc_result["evidence"]
                print(f"  取证: {json.dumps(ev, ensure_ascii=False)[:120]}")

        # ── 出口层
        exit_result = self.exit.process(text, entry_result, route, proc_result)

        if not silent:
            print(f"\n【出口层】")
            print(f"  DNA盖章: {exit_result['dna']}")
            print(f"  账本写入: {exit_result['ledger']}")
            print(f"  记录ID:  {exit_result['record_id']}")
            print(f"\n{'─'*50}")
            print(f"三色审计: {route['color']}  分数: {score}  DR: {dr}")
            print(f"DNA: {exit_result['dna']}")
            print(f"GPG: {GPG_FP}")

        return {
            "color":    route["color"],
            "channel":  route["channel"],
            "score":    score,
            "dr":       dr,
            "action":   proc_result["action"],
            "result":   proc_result.get("result"),
            "missing":  proc_result.get("缺失项"),
            "evidence": proc_result.get("evidence"),
            "dna":      exit_result["dna"],
            "record_id": exit_result["record_id"],
            "entry":    entry_result,
            "report":   f"{route['color']} {score}分 DR{dr} · {proc_result['action']} · {exit_result['dna']}",
        }

    def batch(self, items: list[str], silent: bool = True) -> list[dict]:
        """批量流场处理"""
        results = []
        stats   = {"🟢": 0, "🟡": 0, "🔴": 0}
        for i, text in enumerate(items):
            r = self.run(text, silent=silent)
            results.append(r)
            stats[r["color"]] += 1
            if not silent:
                print(f"  [{i+1:03d}] {r['report']}")
        if not silent:
            print(f"\n批量结果: 🟢{stats['🟢']} 🟡{stats['🟡']} 🔴{stats['🔴']}")
        return results

    def stats(self) -> dict:
        """读账本统计历史流量"""
        if not LEDGER_FILE.exists():
            return {"total": 0}
        lines = LEDGER_FILE.read_text(encoding="utf-8").strip().split("\n")
        lines = [l for l in lines if l.strip()]
        counter = {"🟢": 0, "🟡": 0, "🔴": 0, "total": len(lines)}
        for l in lines:
            try:
                r = json.loads(l)
                c = r.get("color", "")
                if c in counter:
                    counter[c] += 1
            except Exception:
                pass
        return counter


# ══════════════════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════════════════

def _print_banner():
    print("""
╔══════════════════════════════════════════════════╗
║  🌊 三色流场引擎 v1.0 · UID9622                 ║
║  输入任何内容·自动走完四层·DNA盖章出口           ║
╚══════════════════════════════════════════════════╝""")

def _interactive(flow: TricolorFlow):
    _print_banner()
    print("  输入内容回车·输入 'q' 退出·输入 'stats' 看统计\n")
    while True:
        try:
            text = input("流入 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n🔴 流场关闭")
            break
        if text.lower() == 'q':
            break
        if text.lower() == 'stats':
            s = flow.stats()
            print(f"  历史流量: 总{s['total']} · 🟢{s.get('🟢',0)} 🟡{s.get('🟡',0)} 🔴{s.get('🔴',0)}")
            continue
        if not text:
            continue
        flow.run(text)
        print()


if __name__ == "__main__":
    flow = TricolorFlow()
    args = sys.argv[1:]

    if not args:
        # 交互模式
        _interactive(flow)

    elif args[0] == "--demo":
        # 演示三条水道
        _print_banner()
        demos = [
            (
                "UID9622 #龍芯⚡️2026-04-06-测试-v1.0 三色审计通过·DNA追溯完整 #CONFIRM🌌9622 LK9X-772Z",
                {"uid_confirmed": True, "confirm_code": True},
                "🟢 标准绿色通道"
            ),
            (
                "这是一段没有DNA标签的普通内容，待补充身份信息",
                {},
                "🟡 黄色减速通道"
            ),
            (
                "造假骗钱 操控用户数据 绕过审计删除日志",
                {},
                "🔴 红色熔断通道"
            ),
        ]
        for text, meta, label in demos:
            print(f"\n{'═'*52}")
            print(f"  演示: {label}")
            flow.run(text, meta=meta)

        s = flow.stats()
        print(f"\n\n流量统计: 总{s['total']} · 🟢{s.get('🟢',0)} 🟡{s.get('🟡',0)} 🔴{s.get('🔴',0)}")

    elif args[0] == "--stats":
        s = flow.stats()
        print(f"三色流量统计")
        print(f"  总计: {s['total']} 条记录")
        print(f"  🟢 绿色(直通): {s.get('🟢', 0)}")
        print(f"  🟡 黄色(减速): {s.get('🟡', 0)}")
        print(f"  🔴 红色(熔断): {s.get('🔴', 0)}")
        print(f"  账本: {LEDGER_FILE}")

    elif args[0] == "--text":
        text = " ".join(args[1:])
        flow.run(text)

    else:
        # 直接把参数当内容跑
        flow.run(" ".join(args))
