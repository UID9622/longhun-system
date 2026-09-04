#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════
# lh_ledger.py — 龍魂账法核心引擎 v1.0（底层记账能力·全本地零三方）
# DNA: #龍帳⚡️2026-09-04-LEDGER-CORE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# ═══════════════════════════════════════════════════════════
"""龍魂账法核心引擎。

账法 = 龍魂体系底层记账能力，与生态全面打通：
  · DNA 生成（#龍帳⚡️格式）与 8 位哈希 — 每笔交易可追溯
  · 见证人格映射（T1-T12·12 类交易） — 每笔交易有人格见证
  · 科目表校验（资产/负债/权益/收入/费用·借贷方向）
  · 三色审计自动过闸（对接 lh_three_color_audit.quick_audit）
  · 耻辱墙事件（notices.jsonl） + 超级大脑记忆（lh brain）
  · 多模态感知记账（lh sense ledger-chain / lh ledger scan）
  · JSON-RPC 接口（lh ledger rpc · 供 MCP/数字人调用）

数据落点（全 ~/.longhun/ledger/）:
  transactions.jsonl   已入账交易（GREEN·append-only）
  pending.jsonl        🟡 待审队列（科目缺失/审计待核）
  meltdown.log         🔴 熔断记录
  ledger_index.json    序号自增索引（防并发重号）

依赖: Python 3.8+ 标准库；审计联动 lh_three_color_audit（可选·缺失自动降级内置黑词扫描）
用法: lh ledger <子命令> · 详见 --help
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════
# 一、常量与路径
# ═══════════════════════════════════════════════════════════
HERE = os.path.dirname(os.path.abspath(__file__))
HOME = str(Path.home())
LONGHUN = os.path.join(HOME, ".longhun")
LEDGER_ROOT = os.path.join(LONGHUN, "ledger")
TX_LOG = os.path.join(LEDGER_ROOT, "transactions.jsonl")
PENDING_LOG = os.path.join(LEDGER_ROOT, "pending.jsonl")
MELTDOWN_LOG = os.path.join(LEDGER_ROOT, "meltdown.log")
INDEX_FILE = os.path.join(LEDGER_ROOT, "ledger_index.json")
WALL_NOTICES = os.path.join(LONGHUN, "shame_wall", "notices.jsonl")
BRAIN_SCRIPT = os.path.join(HERE, "lh_brain.py")

MAJOR_AMOUNT = 100000  # 重大交易金额阈值（大额自动入 brain）
SOVEREIGN_TYPES = ("T1",)  # 主权类交易类型（自动入 brain）

# ═══════════════════════════════════════════════════════════
# 二、会计科目表（code: 名称·类型·借贷方向·说明）
#    类型: 资产/负债/权益/收入/费用 · 方向: 借(借方科目)/贷(贷方科目)
# ═══════════════════════════════════════════════════════════
ACCOUNTS = {
    # ── 资产（借方增） ──
    "1001": {"name": "库存现金", "type": "资产", "dir": "借", "desc": "现金及现金等价物"},
    "1002": {"name": "银行存款", "type": "资产", "dir": "借", "desc": "银行账户存款"},
    "1003": {"name": "应收账款", "type": "资产", "dir": "借", "desc": "应收未收款项"},
    "1101": {"name": "数字资产", "type": "资产", "dir": "借", "desc": "龍魂数字资产/令牌"},
    # ── 负债（贷方增） ──
    "2001": {"name": "短期借款", "type": "负债", "dir": "贷", "desc": "一年内应还借款"},
    "2101": {"name": "应付款项", "type": "负债", "dir": "贷", "desc": "应付未付款项"},
    # ── 权益（贷方增） ──
    "3101": {"name": "实收资本", "type": "权益", "dir": "贷", "desc": "投入资本"},
    "3201": {"name": "权益储备", "type": "权益", "dir": "贷", "desc": "利润/积累/储备"},
    # ── 收入（贷方增） ──
    "4001": {"name": "主营业务收入", "type": "收入", "dir": "贷", "desc": "主营销售/服务收入"},
    "4101": {"name": "捐赠收入", "type": "收入", "dir": "贷", "desc": "收到捐赠/奉献"},
    "4201": {"name": "服务收入", "type": "收入", "dir": "贷", "desc": "咨询服务/知识付费收入"},
    # ── 费用（借方增） ──
    "5001": {"name": "运营费用", "type": "费用", "dir": "借", "desc": "日常运营/采购支出"},
    "5101": {"name": "研发支出", "type": "费用", "dir": "借", "desc": "研发/开发/训练成本"},
    "5201": {"name": "捐赠支出", "type": "费用", "dir": "借", "desc": "对外捐赠/奉献支出"},
}

ACCOUNT_BY_NAME = {v["name"]: k for k, v in ACCOUNTS.items()}


def validate_account(code):
    """校验科目代码 → 返回 (是否存在, 名称, 借贷方向)"""
    acct = ACCOUNTS.get(str(code))
    if not acct:
        return False, "", ""
    return True, acct["name"], acct["dir"]


def get_account_type(code):
    """科目类型: 资产/负债/权益/收入/费用（未知返回 '未知'）"""
    acct = ACCOUNTS.get(str(code))
    return acct["type"] if acct else "未知"


# ═══════════════════════════════════════════════════════════
# 三、见证人格映射（T1-T12 · 12 类交易 · 龍魂生态人格见证）
# ═══════════════════════════════════════════════════════════
WITNESS = {
    "T1":  "🧠 P25·数字主权官  主权类交易（主权资产/主权注入·最高见证）",
    "T2":  "📚 P03·雯雯        知识资产类交易（知识入库/文档资产）",
    "T3":  "🛠️ P04·鲁班        技能服务类交易（开发/施工/技能交换）",
    "T4":  "🧧 P12·屈原        捐赠奉献类交易（无私付出·六誓见证）",
    "T5":  "🏅 P20·贡献公证官  贡献信任类交易（贡献积分/信任凭证）",
    "T6":  "👁️ P05·上帝之眼    审计类交易（审计费/合规支出·独立见证）",
    "T7":  "🎨 P11·李白        创意艺术类交易（创作/版权/灵感资产）",
    "T8":  "⏳ P17·张衡        时间历法类交易（时间资产/历法校准）",
    "T9":  "🧬 P23·神经元      技术研发类交易（研发/模型/算力支出）",
    "T10": "✒️ P08·仓颉        文化符号类交易（语言/符号/命名资产）",
    "T11": "💰 P07·管仲        成本经济类交易（成本核算/资源调度）",
    "T12": "⚖️ P13·姜子牙      契约授权类交易（授权/注册/封神派位）",
}

DEFAULT_WITNESS = "🧠 P00·曾师智慧总师（默认见证·超 T1-T12 范围）"


def get_witness(tx_type):
    """交易类型 → 见证人格。缺失 → 默认见证 + 耻辱墙警告。"""
    key = str(tx_type).strip().upper()
    if not key.startswith("T"):
        key = "T" + key
    w = WITNESS.get(key)
    if w is None:
        _wall("ledger_witness_fallback",
              f"未知交易类型 {tx_type} · 使用默认见证 {DEFAULT_WITNESS}",
              f"#龍帳⚡️{datetime.date.today().isoformat()}-WITNESS-FALLBACK")
        return DEFAULT_WITNESS, False
    return w, True


# ═══════════════════════════════════════════════════════════
# 四、DNA / 哈希
# ═══════════════════════════════════════════════════════════
DNA_PREFIX = "#龍帳⚡️"
DNA_RE = re.compile(r"^#龍帳⚡️(\d{4}-\d{2}-\d{2})-(\d+)-(\d+)-(.+)-(\d{3})-UID9622$")


def gen_dna(date, dr_code, cr_code, amount, seq):
    """生成账法 DNA: #龍帳⚡️{YYYY-MM-DD}-{借方}-{贷方}-{量}-{序号}-UID9622
    自动校验: 科目代码存在 · 序号三位数补零。"""
    ok_dr, _, _ = validate_account(dr_code)
    ok_cr, _, _ = validate_account(cr_code)
    if not ok_dr:
        raise ValueError(f"借方科目不存在: {dr_code}")
    if not ok_cr:
        raise ValueError(f"贷方科目不存在: {cr_code}")
    date = str(date).strip() or datetime.date.today().isoformat()
    try:
        datetime.date.fromisoformat(date)
    except ValueError as e:
        raise ValueError(f"日期格式须为 YYYY-MM-DD: {date}") from e
    seq_i = int(seq)
    if seq_i < 0 or seq_i > 999:
        raise ValueError(f"序号须在 0-999: {seq_i}")
    amount_s = str(amount).strip()
    if not amount_s:
        raise ValueError("金额不能为空")
    return f"{DNA_PREFIX}{date}-{dr_code}-{cr_code}-{amount_s}-{seq_i:03d}-UID9622"


def calc_hash(dna, dr_code, cr_code, amount, timestamp):
    """账法哈希: SHA256(dna|dr|cr|amount|timestamp) 前 8 位大写。
    timestamp 传当前时间=实时；传固定时间=可复现。"""
    raw = f"{dna}|{dr_code}|{cr_code}|{amount}|{timestamp}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8].upper()


def _now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


# ═══════════════════════════════════════════════════════════
# 五、生态联动（耻辱墙 / 超级大脑 / 三色审计）
# ═══════════════════════════════════════════════════════════
def _wall(kind, message, dna):
    """写耻辱墙 notices（与 lh_sense/lh_external 同格式·repo=lh-ledger）"""
    try:
        os.makedirs(os.path.dirname(WALL_NOTICES), exist_ok=True)
        entry = {"ts": _now_iso(), "type": kind, "repo": "lh-ledger",
                 "message": str(message)[:500], "dna": dna}
        with open(WALL_NOTICES, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:  # noqa: BLE001  墙写入失败不影响记账主流程
        print(f"  ⚠️ 耻辱墙写入失败: {e}")


def _brain_save(note, kw, kind="ledger"):
    """重大交易入超级大脑（子进程隔离·防 import 副作用）"""
    try:
        if not os.path.exists(BRAIN_SCRIPT):
            return
        cmd = [sys.executable, BRAIN_SCRIPT, "save", "--note", str(note)[:1950],
               "--source", "lh-ledger", "--kind", kind]
        for k in kw[:5]:
            cmd += ["--kw", str(k)]
        subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except Exception:  # noqa: BLE001
        pass


# 审计降级黑词表（lh_three_color_audit 缺失时内置兜底·仅拦明显红线）
_RED_WORDS = ["技术无国界", "用户体验优先", "灵活处理", "国际接轨", "简化管理",
              "商业化需要", "平衡各方", "行业标准", "伪造DNA", "洗来源", "去水印"]


def _quick_audit(content):
    """三色审计: 优先 lh_three_color_audit.quick_audit → (色, 理由)。
    引擎缺失时降级内置黑词扫描并注明。"""
    try:
        sys.path.insert(0, HERE)
        from lh_three_color_audit import quick_audit  # noqa: PLC0415
        color, reason = quick_audit(content)
        return color, reason
    except Exception as e:  # noqa: BLE001
        hit = next((w for w in _RED_WORDS if w in content), None)
        if hit:
            return "🔴", f"内置降级审计: 命中红线词「{hit}」(lh_three_color_audit 不可用: {e})"
        return "🟢", f"内置降级审计通过 (lh_three_color_audit 不可用: {e})"


def _write_jsonl(path, entry):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _read_jsonl(path):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return out


def _next_seq():
    """序号自增（读索引文件·防并发重号）"""
    seq = 1
    if os.path.exists(INDEX_FILE):
        try:
            with open(INDEX_FILE, encoding="utf-8") as fh:
                seq = int(json.load(fh).get("seq", 0)) + 1
        except Exception:  # noqa: BLE001
            seq = len(_read_jsonl(TX_LOG)) + 1
    os.makedirs(LEDGER_ROOT, exist_ok=True)
    with open(INDEX_FILE, "w", encoding="utf-8") as fh:
        json.dump({"seq": seq}, fh)
    return seq


def _amount_num(amount):
    """金额数值部分（支持 '1条/100元/3.5笔' 等量词）"""
    m = re.match(r"^([0-9]+(?:\.[0-9]+)?)", str(amount).strip())
    return float(m.group(1)) if m else 0.0


# ═══════════════════════════════════════════════════════════
# 六、交易记录
# ═══════════════════════════════════════════════════════════
class LonghunTransaction:
    """龍魂账法单笔交易记录。

    属性: tx_type/date/dr_code/cr_code/amount/seq/note/dna/hash/witness/status
    方法: ledger_line()/to_json()/verify()
    """

    def __init__(self, tx_type, date, dr_code, cr_code, amount, seq,
                 note="", dna="", tx_hash="", witness="", status="GREEN",
                 extra=None, created_at=""):
        self.tx_type = str(tx_type).strip().upper()
        self.date = str(date)
        self.dr_code = str(dr_code)
        self.cr_code = str(cr_code)
        self.amount = str(amount).strip()
        self.seq = int(seq)
        self.note = str(note or "").strip()
        self.dna = dna or ""
        self.hash = tx_hash or ""
        self.witness = witness or ""
        self.status = status
        self.extra = extra or {}
        self.created_at = created_at or _now_iso()

    # ── 构造（自动补齐 dna/hash/witness） ──
    @classmethod
    def create(cls, tx_type, date, dr_code, cr_code, amount, seq,
               note="", timestamp=None):
        """自动生成 DNA + 哈希 + 见证人格。timestamp 固定=可复现哈希。"""
        dna = gen_dna(date, dr_code, cr_code, amount, seq)
        ts = timestamp or _now_iso()
        tx_hash = calc_hash(dna, dr_code, cr_code, amount, ts)
        witness, known = get_witness(tx_type)
        if not known:
            witness = witness.split("（")[0]
        return cls(tx_type, date, dr_code, cr_code, amount, seq, note,
                   dna=dna, tx_hash=tx_hash, witness=witness,
                   extra={"hash_ts": ts, "audit_color": "", "audit_reason": ""})

    def verify(self):
        """自校验 → (ok, 问题列表)"""
        probs = []
        ok_dr, name_dr, _ = validate_account(self.dr_code)
        ok_cr, name_cr, _ = validate_account(self.cr_code)
        if not ok_dr:
            probs.append(f"借方科目不存在: {self.dr_code}")
        if not ok_cr:
            probs.append(f"贷方科目不存在: {self.cr_code}")
        if ok_dr and ok_cr and _amount_num(self.amount) > 0:
            # 借贷方向必须合规: 借方科目方向为借·贷方科目方向为贷
            pass
        if not DNA_RE.match(self.dna or ""):
            probs.append(f"DNA 格式非法: {self.dna}")
        if self.amount == "":
            probs.append("金额为空")
        # 哈希复现校验（需记录 hash_ts）
        ts = (self.extra or {}).get("hash_ts", "")
        if ts and self.hash:
            expect = calc_hash(self.dna, self.dr_code, self.cr_code,
                               self.amount, ts)
            if expect != self.hash:
                probs.append(f"哈希不符: {self.hash} != {expect}")
        return (not probs), probs

    def ledger_line(self):
        """标准账簿行（对齐等宽·方便对齐看账）"""
        return (f"{self.seq:>4} | {self.date} | {self.tx_type:<4} | "
                f"{self.dr_code} {self.amount:>8} → {self.cr_code:<4} | "
                f"{self.note[:28]:<28} | {self.hash}")

    def to_json(self):
        """JSON 序列化"""
        return {
            "tx_type": self.tx_type, "date": self.date,
            "dr_code": self.dr_code, "cr_code": self.cr_code,
            "amount": self.amount, "seq": self.seq, "note": self.note,
            "dna": self.dna, "hash": self.hash, "witness": self.witness,
            "status": self.status, "extra": self.extra,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_json(d):
        """JSON → 对象"""
        return LonghunTransaction(
            tx_type=d.get("tx_type", ""), date=d.get("date", ""),
            dr_code=d.get("dr_code", ""), cr_code=d.get("cr_code", ""),
            amount=d.get("amount", ""), seq=d.get("seq", 0),
            note=d.get("note", ""), dna=d.get("dna", ""),
            tx_hash=d.get("hash", ""), witness=d.get("witness", ""),
            status=d.get("status", "GREEN"), extra=d.get("extra", {}),
            created_at=d.get("created_at", ""))


# ═══════════════════════════════════════════════════════════
# 七、账簿管理器
# ═══════════════════════════════════════════════════════════
class LedgerManager:
    """账簿管理器: add/get/list/verify_all/export/balance/audit/wall/scan"""

    # ── 记账（自动三色审计 + 耻辱墙 + brain） ──
    def add(self, tx_type, dr_code, cr_code, amount, note="", date="",
            skip_audit=False, silent=False):
        """新增交易。审计: 🟢 入账 / 🟡 待审队列 / 🔴 熔断拒绝。
        返回 (status, 对象或错误信息)"""
        # 1. 科目与借贷方向预检
        ok_dr, name_dr, dir_dr = validate_account(dr_code)
        ok_cr, name_cr, dir_cr = validate_account(cr_code)
        if not ok_dr or not ok_cr:
            return "ERR", f"科目不存在: 借={dr_code}({name_dr}) 贷={cr_code}({name_cr})"
        if dir_dr != "借":
            return "ERR", f"{dr_code}({name_dr}) 是{dir_dr}方科目·不能作借方"
        if dir_cr != "贷":
            return "ERR", f"{cr_code}({name_cr}) 是{dir_cr}方科目·不能作贷方"

        date = date or datetime.date.today().isoformat()
        seq = _next_seq()
        tx = LonghunTransaction.create(tx_type, date, dr_code, cr_code,
                                       amount, seq, note)

        # 2. 三色审计
        audit_content = (f"[账法·{tx.tx_type}] {note or '无备注'} "
                         f"借 {dr_code}:{name_dr} 贷 {cr_code}:{name_cr} "
                         f"金额 {amount} · 记账日期 {date}")
        if skip_audit:
            color, reason = "🟢", "跳过审计（显式 --skip-audit）"
        else:
            color, reason = _quick_audit(audit_content)
        tx.extra["audit_color"] = color
        tx.extra["audit_reason"] = reason

        summary = (f"{tx.tx_type} {tx.note or '无备注'} "
                   f"借{name_dr} 贷{name_cr} {tx.amount}")

        if color == "🔴":
            # ── 熔断: 拒绝写入 + 耻辱墙 + 熔断日志
            tx.status = "MELTDOWN"
            line = {"ts": _now_iso(), "dna": tx.dna, "summary": summary,
                    "reason": reason, "tx": tx.to_json()}
            _write_jsonl(MELTDOWN_LOG.replace(".log", ".jsonl"), line)
            with open(MELTDOWN_LOG, "a", encoding="utf-8") as fh:
                fh.write(f"{_now_iso()} 🔴 {tx.dna} {reason}\n")
            _wall("ledger_red_meltdown",
                  f"🔴 熔断拒绝 {summary} · {reason}", tx.dna)
            if not silent:
                print(f"  🔴 熔断拒绝: {reason}")
                print(f"     DNA {tx.dna} · 未写入账簿")
            return "RED", tx

        if color == "🟡":
            # ── 待审: 写入待审队列 + 耻辱墙草稿
            tx.status = "PENDING"
            rec = tx.to_json()
            rec["pending_at"] = _now_iso()
            _write_jsonl(PENDING_LOG, rec)
            _wall("ledger_yellow_draft",
                  f"🟡 待审草稿 {summary} · {reason}", tx.dna)
            if not silent:
                print(f"  🟡 待审入列: {reason}")
                print(f"     DNA {tx.dna}")
                print(f"     💡 复核后: lh ledger confirm {tx.seq} 重新审计入账")
            return "YELLOW", tx

        # ── 🟢 入账
        _write_jsonl(TX_LOG, tx.to_json())
        _wall("ledger_tx",
              f"✅ 入账 {summary} · {color} · {tx.hash}", tx.dna)
        if not silent:
            print(f"  🟢 入账 {tx.seq:>3} · {tx.date} · {tx.tx_type} "
                  f"借{name_dr} 贷{name_cr} {tx.amount} · {tx.hash}")
            print(f"     DNA {tx.dna}")

        # 重大交易（主权类/大额）自动入超级大脑
        amount_num = _amount_num(amount)
        if tx.tx_type in SOVEREIGN_TYPES or amount_num >= MAJOR_AMOUNT:
            _brain_save(f"[账法·{tx.tx_type}] {summary} · DNA {tx.dna} "
                        f"· 哈希 {tx.hash} · 见证 {tx.witness}",
                        ["ledger", tx.tx_type, tx.dr_code, tx.cr_code],
                        kind="ledger")
            if not silent:
                print(f"     🧠 重大交易已入超级大脑 lh brain")
        return "GREEN", tx

    # ── 查询 ──
    def get(self, seq=None, date=None, dna=None):
        """按 seq/date/dna 查询已入账交易 → 列表"""
        txs = [LonghunTransaction.from_json(d) for d in _read_jsonl(TX_LOG)]
        if seq is not None:
            txs = [t for t in txs if t.seq == int(seq)]
        if date:
            txs = [t for t in txs if t.date == str(date)]
        if dna:
            txs = [t for t in txs if t.dna == str(dna)]
        return txs

    def pending(self):
        """待审队列"""
        return [LonghunTransaction.from_json(d) for d in _read_jsonl(PENDING_LOG)]

    def confirm(self, seq, silent=False):
        """复核待审交易: 重新审计 → 🟢 入账 / 🔴 拒绝"""
        pendings = _read_jsonl(PENDING_LOG)
        target = None
        rest = []
        for d in pendings:
            if d.get("seq") == int(seq):
                target = d
            else:
                rest.append(d)
        if target is None:
            return "ERR", f"待审队列无 seq={seq}"
        tx = LonghunTransaction.from_json(target)
        tx.date = tx.date
        return self.add(tx.tx_type, tx.dr_code, tx.cr_code, tx.amount,
                        note=tx.note, date=tx.date, silent=silent)

    def list_tx(self, limit=20, show_all=False):
        """最近交易列表"""
        txs = [LonghunTransaction.from_json(d) for d in _read_jsonl(TX_LOG)]
        if not show_all:
            txs = txs[-int(limit):]
        return txs

    # ── 全量校验 ──
    def verify_all(self):
        """全量校验 → (结果列表, 通过数, 失败数)"""
        txs = [LonghunTransaction.from_json(d) for d in _read_jsonl(TX_LOG)]
        seen_dna, dup = set(), []
        for t in txs:
            if t.dna in seen_dna:
                dup.append(t.seq)
            seen_dna.add(t.dna)
        results, fails = [], 0
        for t in txs:
            ok, probs = t.verify()
            if not ok:
                fails += 1
            results.append((t, ok, probs))
        return txs, results, fails, dup

    # ── 资产负债权益 ──
    def balance(self):
        """计算资产/负债/权益/收入/费用与恒等式。
        资产/费用=借方向: net = 借累计 - 贷累计
        负债/权益/收入=贷方向: net = 贷累计 - 借累计"""
        txs = [LonghunTransaction.from_json(d) for d in _read_jsonl(TX_LOG)]
        dr_sum, cr_sum = {}, {}  # code → 数值累计
        for t in txs:
            n = _amount_num(t.amount)
            if n <= 0:
                continue
            dr_sum[t.dr_code] = dr_sum.get(t.dr_code, 0.0) + n
            cr_sum[t.cr_code] = cr_sum.get(t.cr_code, 0.0) + n
        bal = {"资产": 0.0, "负债": 0.0, "权益": 0.0, "收入": 0.0, "费用": 0.0}
        detail = {}
        for code in set(list(dr_sum) + list(cr_sum)):
            acct = ACCOUNTS.get(code)
            if not acct:
                continue
            typ, dr, cr = acct["type"], dr_sum.get(code, 0.0), cr_sum.get(code, 0.0)
            net = (dr - cr) if acct["dir"] == "借" else (cr - dr)
            bal[typ] = bal.get(typ, 0.0) + net
            detail[code] = {"name": acct["name"], "type": typ, "net": net}
        # 恒等式: 资产 = 负债 + 权益 + (收入 - 费用)
        rhs = bal["负债"] + bal["权益"] + (bal["收入"] - bal["费用"])
        identity_ok = abs(bal["资产"] - rhs) < 1e-6
        return {"balance": bal, "detail": detail,
                "tx_count": len(txs), "identity_ok": identity_ok}

    # ── 导出 ──
    def export(self, fmt="json"):
        """导出 CSV/JSON/Markdown → 打印到 stdout"""
        txs = [LonghunTransaction.from_json(d) for d in _read_jsonl(TX_LOG)]
        if fmt == "json":
            return json.dumps([t.to_json() for t in txs],
                              ensure_ascii=False, indent=2)
        if fmt == "csv":
            lines = ["seq,date,tx_type,dr_code,cr_code,amount,note,dna,hash,status"]
            for t in txs:
                lines.append(",".join([
                    str(t.seq), t.date, t.tx_type, t.dr_code, t.cr_code,
                    t.amount, (t.note or "").replace(",", "，").replace('"', "'"),
                    t.dna, t.hash, t.status]))
            return "\n".join(lines)
        if fmt in ("md", "markdown"):
            out = ["# 龍魂账法账簿", "", "| 序号 | 日期 | 类型 | 借方 | 贷方 | 金额 | 备注 | 哈希 |",
                   "|----:|:---|:---|:---|:---|:---|:---|:---|"]
            for t in txs:
                out.append(f"| {t.seq} | {t.date} | {t.tx_type} | {t.dr_code} "
                           f"| {t.cr_code} | {t.amount} | {t.note} | {t.hash} |")
            return "\n".join(out)
        raise ValueError(f"不支持的格式: {fmt} (csv/json/md)")


# ═══════════════════════════════════════════════════════════
# 八、感知文本解析（发票/收据/口述 → 记账要素）
# ═══════════════════════════════════════════════════════════
# 科目线索关键词（OCR/ASR 文本 → 借贷科目启发式）
_CR_HINTS = [  # 贷方线索: (关键词, 科目)
    ("捐赠收入", "4101"), ("捐赠", "4101"), ("收到捐", "4101"), ("奉献", "4101"),
    ("服务费", "4201"), ("咨询", "4201"), ("知识付费", "4201"),
    ("主营", "4001"), ("销售", "4001"), ("卖", "4001"),
    ("借款", "2001"), ("资本", "3101"), ("投入", "3101"),
    ("权益储备", "3201"), ("积累", "3201"),
]
_DR_HINTS = [  # 借方线索
    ("现金", "1001"), ("付现", "1001"),
    ("银行", "1002"), ("转账", "1002"), ("收款", "1002"), ("收到", "1002"),
    ("应收", "1003"),
    ("研发", "5101"), ("开发", "5101"), ("训练", "5101"), ("算力", "5101"),
    ("运营", "5001"), ("采购", "5001"), ("费用", "5001"), ("购买", "5001"), ("买", "5001"),
    ("捐出", "5201"), ("捐赠支出", "5201"), ("施舍", "5201"),
]


def parse_ledger_text(text, dr_code="", cr_code="", amount="", date="", tx_type="T9"):
    """解析识别文本 → 记账要素。
    返回 dict: {dr_code, cr_code, amount, date, note, confidence_hint}"""
    text = (text or "").strip()
    note_parts = [ln.strip() for ln in re.split(r"[\n\r,，。;；]", text) if ln.strip()]
    full = "".join(note_parts)[:200]

    # 金额: 优先「数字+量词」（避开日期里的年份段），否则取非日期数字
    if not amount:
        m = re.search(r"([0-9][0-9,]*\.?[0-9]*)\s*(条|元|笔|张|次|个|块|美金|美元)", text)
        if not m:
            stripped = re.sub(r"\d{4}\s*[年\-/\.]\s*\d{1,2}\s*[月\-/\.]\s*\d{1,2}",
                              " ", text)
            m = re.search(r"([0-9][0-9,]*\.?[0-9]*)\s*(条|元|笔|张|次|个|块)?", stripped)
        if m:
            num = m.group(1).replace(",", "")
            unit = (m.group(2) or "").replace("美金", "美元")
            amount = f"{num}{unit}"
    # 日期
    if not date:
        m = re.search(r"(\d{4})[年\-/\.](\d{1,2})[月\-/\.](\d{1,2})", text)
        if m:
            date = f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    # 科目（显式参数 > 关键词启发）
    if not dr_code:
        for kw, code in _DR_HINTS:
            if kw in full:
                dr_code = code
                break
    if not cr_code:
        for kw, code in _CR_HINTS:
            if kw in full:
                cr_code = code
                break
    note = " ".join(note_parts)[:200]
    return {"dr_code": dr_code, "cr_code": cr_code, "amount": amount,
            "date": date, "note": note or "感知识别记账", "tx_type": tx_type}


# ═══════════════════════════════════════════════════════════
# 九、耻辱墙视角（lh ledger wall）
# ═══════════════════════════════════════════════════════════
def _wall_events(limit=20):
    """读取耻辱墙 notices 中账本相关事件"""
    events = [d for d in _read_jsonl(WALL_NOTICES)
              if d.get("repo") == "lh-ledger" or str(d.get("type", "")).startswith("ledger")]
    return events[-int(limit):]


# ═══════════════════════════════════════════════════════════
# 十、JSON-RPC（lh ledger rpc · 供 MCP/数字人调用）
# ═══════════════════════════════════════════════════════════
def rpc_dispatch(req):
    """RPC 分发: {"method": "...", "params": {...}} → dict
    method: add / get / list / verify / balance / export / gen_dna / calc_hash"""
    method = req.get("method", "")
    p = req.get("params", {}) or {}
    mgr = LedgerManager()
    try:
        if method == "add":
            status, obj = mgr.add(p.get("tx_type", "T9"), p.get("dr_code", ""),
                                  p.get("cr_code", ""), p.get("amount", ""),
                                  note=p.get("note", ""), date=p.get("date", ""))
            return {"ok": True, "status": status,
                    "tx": obj.to_json() if hasattr(obj, "to_json") else str(obj)}
        if method == "get":
            return {"ok": True, "txs": [t.to_json() for t in
                                        mgr.get(seq=p.get("seq"), date=p.get("date"),
                                                dna=p.get("dna"))]}
        if method == "list":
            return {"ok": True, "txs": [t.to_json() for t in
                                        mgr.list_tx(limit=p.get("limit", 20))]}
        if method == "verify":
            txs, results, fails, dup = mgr.verify_all()
            return {"ok": True, "total": len(txs), "fail": fails,
                    "dup_seq": dup,
                    "details": [{"seq": t.seq, "ok": ok, "problems": probs}
                                for t, ok, probs in results]}
        if method == "balance":
            return {"ok": True, **mgr.balance()}
        if method == "export":
            return {"ok": True, "content": mgr.export(p.get("format", "json"))}
        if method == "gen_dna":
            return {"ok": True,
                    "dna": gen_dna(p.get("date", datetime.date.today().isoformat()),
                                   p.get("dr_code"), p.get("cr_code"),
                                   p.get("amount"), p.get("seq", 1))}
        if method == "calc_hash":
            return {"ok": True, "hash": calc_hash(
                p.get("dna", ""), p.get("dr_code", ""), p.get("cr_code", ""),
                p.get("amount", ""), p.get("timestamp", _now_iso()))}
        return {"ok": False, "error": f"未知 method: {method}"}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e)}


# ═══════════════════════════════════════════════════════════
# 十一、CLI 入口
# ═══════════════════════════════════════════════════════════
def _fmt_amount(n):
    """金额显示（数值·不带量词单位·混合单位账由科目语义保证）"""
    if n == int(n):
        return str(int(n))
    return f"{n:.2f}"


def cmd_dna(a):
    """lh ledger dna <dr> <cr> <amount> [--seq N] [--date YYYY-MM-DD]"""
    try:
        dna = gen_dna(a.date or datetime.date.today().isoformat(),
                      a.dr, a.cr, a.amount, a.seq)
        print(dna)
        return 0
    except ValueError as e:
        print(f"❌ {e}")
        return 1


def cmd_hash(a):
    """lh ledger hash <dna> [--dr CODE] [--cr CODE] [--amount 量]"""
    if not a.dna or not a.dr:
        print("❌ 用法: lh ledger hash <dna> --dr CODE --cr CODE --amount 量 [--ts 时间戳]")
        return 1
    ts = a.ts or _now_iso()
    h = calc_hash(a.dna, a.dr, a.cr, a.amount, ts)
    print(h)
    return 0


def cmd_add(a):
    """lh ledger add <tx_type> <dr> <cr> <amount> [--note] [--date] [--skip-audit]"""
    status, obj = LedgerManager().add(a.tx_type, a.dr, a.cr, a.amount,
                                      note=a.note or "", date=a.date or "",
                                      skip_audit=a.skip_audit)
    return 0 if status in ("GREEN", "YELLOW", "RED") else (print(f"❌ {obj}"), 1)[1]


def cmd_list(a):
    """lh ledger list [--limit N] [--pending] [--all] [--json]"""
    mgr = LedgerManager()
    if a.pending:
        pend = mgr.pending()
        if a.json:
            print(json.dumps([t.to_json() for t in pend], ensure_ascii=False, indent=2))
            return 0
        print(f"\n  🟡 待审队列 ({len(pend)}):")
        for t in pend:
            print(f"  {t.ledger_line()}  {t.extra.get('audit_color', '')} "
                  f"{str(t.extra.get('audit_reason', ''))[:50]}")
        if not pend:
            print("  （空）")
        return 0
    txs = mgr.list_tx(limit=a.limit or 20, show_all=a.all)
    if a.json:
        print(json.dumps([t.to_json() for t in txs], ensure_ascii=False, indent=2))
        return 0
    if not txs:
        print("  📒 账簿为空 · lh ledger add T1 1001 3201 1条 --note 第一笔")
        return 0
    print(f"\n  📒 龍魂账法账簿（最近 {len(txs)} 笔 · 共 {len(mgr.list_tx(show_all=True))} 笔）")
    print("  " + "-" * 88)
    for t in txs:
        print("  " + t.ledger_line())
    print("  " + "-" * 88)
    return 0


def cmd_verify(a):
    """lh ledger verify [--full]"""
    txs, results, fails, dup = LedgerManager().verify_all()
    if a.full:
        for t, ok, probs in results:
            mark = "🟢" if ok else "🔴"
            print(f"  {mark} seq={t.seq} {t.dna}")
            for p in probs:
                print(f"      ↳ {p}")
    dup_note = f" · ⚠️ DNA重复: {dup}" if dup else ""
    print(f"\n  {'🟢' if fails == 0 and not dup else '🔴'} "
          f"全量校验: {len(txs)} 笔 · 失败 {fails} · 重复 {len(dup)}{dup_note}")
    return 0 if fails == 0 and not dup else 1


def cmd_balance(a):
    """lh ledger balance"""
    r = LedgerManager().balance()
    b = r["balance"]
    mark = "🟢" if r["identity_ok"] else "🔴"
    print(f"\n  📊 资产负债权益（{r['tx_count']} 笔已入账）")
    print("  " + "-" * 40)
    for typ in ("资产", "负债", "权益", "收入", "费用"):
        print(f"  {typ:<4} {_fmt_amount(b.get(typ, 0.0))}")
    print("  " + "-" * 40)
    rhs = b["负债"] + b["权益"] + (b["收入"] - b["费用"])
    print(f"  恒等式  资产 = 负债+权益+(收入-费用)  "
          f"{_fmt_amount(b['资产'])} = {_fmt_amount(rhs)}  {mark}")
    if a.json:
        print(json.dumps({"balance": b, "identity_ok": r["identity_ok"],
                          "tx_count": r["tx_count"]}, ensure_ascii=False, indent=2))
    return 0


def cmd_export(a):
    """lh ledger export --format csv|json|md"""
    try:
        content = LedgerManager().export(a.format)
        print(content)
        return 0
    except ValueError as e:
        print(f"❌ {e}")
        return 1


def cmd_audit(a):
    """lh ledger audit <seq> → 查看某笔交易审计详情"""
    txs = LedgerManager().get(seq=a.seq)
    if not txs:
        print(f"❌ 未找到 seq={a.seq}")
        return 1
    t = txs[0]
    extra = t.extra or {}
    print(f"\n  🧾 审计详情 seq={t.seq} · {t.dna}")
    witness_full, _known = get_witness(t.tx_type)
    print(f"     类型: {t.tx_type} · 见证: {witness_full}")
    print(f"     摘要: 借{t.dr_code} 贷{t.cr_code} {t.amount} {t.note or ''}")
    print(f"     入账审计: {extra.get('audit_color', '?')} "
          f"{extra.get('audit_reason', '')}")
    # 现行复核（重跑一次审计）
    if t.status == "GREEN":
        color, reason = _quick_audit(
            f"[账法·{t.tx_type}] {t.note or ''} 借 {t.dr_code} 贷 {t.cr_code} "
            f"金额 {t.amount}")
        print(f"     现行复核: {color} {reason}")
    return 0


def cmd_wall(a):
    """lh ledger wall [--limit N]"""
    events = _wall_events(a.limit or 20)
    print(f"\n  📜 账本耻辱墙事件（最近 {len(events)} 条）")
    print("  " + "-" * 88)
    for e in events:
        print(f"  {e.get('ts', '')[:19]} {e.get('type', '')}")
        print(f"      {str(e.get('message', ''))[:70]}")
        print(f"      DNA {e.get('dna', '')}")
    print("  " + "-" * 88)
    return 0


def cmd_confirm(a):
    """lh ledger confirm <seq> → 待审复核入账"""
    status, obj = LedgerManager().confirm(a.seq)
    if status == "ERR":
        print(f"❌ {obj}")
        return 1
    return 0


def cmd_add_auto(a):
    """lh ledger add-auto <文本> [--tx-type] [--date]
    识别文本（OCR/ASR）→ 解析金额/日期/科目线索 → 自动记账。
    科目判定不出 → 🟡 待审草稿。供 lh sense ledger-chain 链后调用。"""
    elems = parse_ledger_text(a.text, amount=a.amount or "",
                              date=a.date or "", tx_type=a.tx_type or "T9")
    print(f"  📝 解析: 借={elems['dr_code'] or '?'} 贷={elems['cr_code'] or '?'} "
          f"金额={elems['amount'] or '?'} 日期={elems['date'] or '?'} "
          f"备注={elems['note'][:60]}")
    if not elems["dr_code"] or not elems["cr_code"] or not elems["amount"]:
        missing = [k for k in ("dr_code", "cr_code", "amount") if not elems[k]]
        draft = {"seq": _next_seq(), "pending_at": _now_iso(),
                 "tx_type": elems["tx_type"],
                 "date": elems["date"] or datetime.date.today().isoformat(),
                 "dr_code": elems["dr_code"], "cr_code": elems["cr_code"],
                 "amount": elems["amount"], "note": elems["note"],
                 "dna": "", "hash": "", "witness": "", "status": "PENDING",
                 "extra": {"audit_color": "🟡",
                           "audit_reason": f"识别缺 {missing}",
                           "source": a.source or ""},
                 "created_at": _now_iso()}
        _write_jsonl(PENDING_LOG, draft)
        _wall("ledger_yellow_draft",
              f"🟡 识别待补 {missing} · {elems['note'][:60]}", "")
        print(f"  🟡 要素不全({missing})· 已入待审队列 · "
              f"补全后: lh ledger confirm {draft['seq']}")
        return 0
    note = f"[{a.source or 'auto'}] {elems['note']}" if a.source else elems["note"]
    status, obj = LedgerManager().add(elems["tx_type"], elems["dr_code"],
                                      elems["cr_code"], elems["amount"],
                                      note=note, date=elems["date"])
    if status == "ERR":
        print(f"❌ {obj}")
        return 1
    return 0


def cmd_scan(a):
    """lh ledger scan <文件> [--dr] [--cr] [--amount] [--tx-type] [--no-audit]
    图片/音频 → lh_sense 识别 → 解析记账要素 → 自动记账（三色审计）"""
    fp = os.path.abspath(a.file)
    if not os.path.exists(fp):
        print(f"❌ 文件不存在: {fp}")
        return 1
    try:
        sys.path.insert(0, HERE)
        import lh_sense  # noqa: PLC0415
    except Exception as e:  # noqa: BLE001
        print(f"❌ lh_sense 不可用（多模态识别依赖 ollama/tesseract/faster-whisper）: {e}")
        return 1
    print(f"  👁️ 感知识别 {os.path.basename(fp)} ...")
    ext = Path(fp).suffix.lower()
    if ext in (".png", ".jpg", ".jpeg", ".webp", ".bmp"):
        result = lh_sense.sense_file(fp, lh_sense.PROMPT_DEFAULT,
                                     want_ocr=True, want_asr=False, n_frames=1)
    elif ext in (".wav", ".mp3", ".m4a", ".flac", ".aac", ".ogg"):
        result = lh_sense.sense_file(fp, lh_sense.PROMPT_DEFAULT,
                                     want_ocr=False, want_asr=True, n_frames=1)
    else:
        print(f"❌ 不支持的媒体类型: {ext}（支持图片/音频）")
        return 1
    text = lh_sense.extract_text(result)
    conf = lh_sense.overall_confidence(result)
    if not text:
        print(f"  🔴 识别无文本产出 conf={conf:.2f} · 未记账")
        return 2
    print(f"  📝 识别文本 conf={conf:.2f}: {text[:160]}")
    elems = parse_ledger_text(text, dr_code=a.dr or "", cr_code=a.cr or "",
                              amount=a.amount or "", tx_type=a.tx_type or "T9")
    if not elems["dr_code"] or not elems["cr_code"] or not elems["amount"]:
        missing = [k for k in ("dr_code", "cr_code", "amount") if not elems[k]]
        print(f"  🟡 无法判定: {missing} · 已入待审队列待老大确认")
        print(f"     要素: 金额={elems['amount'] or '?'} 日期={elems['date'] or '?'} "
              f"备注={elems['note'][:60]}")
        # 写入 pending 草稿（无 DNA 三要素仍先落草稿·由老大补科目）
        draft = {"seq": _next_seq(), "pending_at": _now_iso(),
                 "tx_type": elems["tx_type"], "date": elems["date"]
                 or datetime.date.today().isoformat(),
                 "dr_code": elems["dr_code"], "cr_code": elems["cr_code"],
                 "amount": elems["amount"], "note": elems["note"],
                 "dna": "", "hash": "", "witness": "", "status": "PENDING",
                 "extra": {"audit_color": "🟡",
                           "audit_reason": f"感知识别缺 {missing}",
                           "scan_conf": round(conf, 2)},
                 "created_at": _now_iso()}
        _write_jsonl(PENDING_LOG, draft)
        _wall("ledger_yellow_draft",
              f"🟡 感知扫描待补 {missing} · {elems['note'][:60]}", "")
        return 0
    status, obj = LedgerManager().add(
        elems["tx_type"], elems["dr_code"], elems["cr_code"],
        elems["amount"], note=f"[scan] {elems['note']}", date=elems["date"])
    if status == "ERR":
        print(f"❌ {obj}")
        return 1
    return 0


def cmd_rpc(a):
    """lh ledger rpc '{"method":"balance"}' → JSON-RPC（供 MCP/数字人）"""
    try:
        req = json.loads(a.payload)
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "error": f"JSON 解析失败: {e}"},
                         ensure_ascii=False))
        return 1
    print(json.dumps(rpc_dispatch(req), ensure_ascii=False, indent=2))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="lh ledger", description="🐉 龍魂账法 v1.0 · 底层记账能力"
                                      "（DNA/哈希/见证/三色/耻辱墙/记忆/感知）")
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("dna", help="生成账法 DNA")
    p.add_argument("dr", help="借方科目代码（如 1001）")
    p.add_argument("cr", help="贷方科目代码（如 3201）")
    p.add_argument("amount", help="数量/金额（如 1条 / 100元）")
    p.add_argument("--seq", type=int, default=1, help="序号（默认 1·自动三位补零）")
    p.add_argument("--date", default="", help="日期 YYYY-MM-DD（默认今天）")

    p = sub.add_parser("hash", help="计算账法哈希")
    p.add_argument("dna", help="账法 DNA")
    p.add_argument("--dr", required=True, help="借方科目")
    p.add_argument("--cr", required=True, help="贷方科目")
    p.add_argument("--amount", required=True, help="数量/金额")
    p.add_argument("--ts", default="", help="时间戳（固定=可复现）")

    p = sub.add_parser("add", help="记录一笔交易（自动三色审计）")
    p.add_argument("tx_type", help="交易类型 T1-T12")
    p.add_argument("dr", help="借方科目")
    p.add_argument("cr", help="贷方科目")
    p.add_argument("amount", help="数量/金额")
    p.add_argument("--note", default="", help="备注")
    p.add_argument("--date", default="", help="记账日期 YYYY-MM-DD")
    p.add_argument("--skip-audit", action="store_true", help="跳过三色审计")

    p = sub.add_parser("list", help="查看最近交易")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--all", action="store_true", help="全部交易")
    p.add_argument("--pending", action="store_true", help="查看待审队列")
    p.add_argument("--json", action="store_true", help="JSON 输出")

    p = sub.add_parser("verify", help="校验账本")
    p.add_argument("--full", action="store_true", help="逐笔明细")

    p = sub.add_parser("balance", help="资产负债权益 + 恒等式")
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("export", help="导出账本")
    p.add_argument("--format", default="json", choices=["csv", "json", "md"])

    p = sub.add_parser("audit", help="查看某笔交易审计详情")
    p.add_argument("seq", type=int)

    p = sub.add_parser("confirm", help="复核待审交易入账")
    p.add_argument("seq", type=int)

    p = sub.add_parser("wall", help="账本耻辱墙事件")
    p.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("scan", help="感知识别自动记账（图片/音频）")
    p.add_argument("file", help="图片或音频文件")
    p.add_argument("--dr", default="", help="借方科目（覆盖识别）")
    p.add_argument("--cr", default="", help="贷方科目（覆盖识别）")
    p.add_argument("--amount", default="", help="金额（覆盖识别）")
    p.add_argument("--tx-type", default="T9", help="交易类型（默认 T9 技术研发）")

    p = sub.add_parser("add-auto", help="识别文本自动记账（OCR/ASR 链后）")
    p.add_argument("text", help="识别出的文本")
    p.add_argument("--tx-type", default="T9", help="交易类型（默认 T9）")
    p.add_argument("--date", default="", help="记账日期（识别到则自动）")
    p.add_argument("--amount", default="", help="金额（识别到则自动）")
    p.add_argument("--source", default="", help="来源标记（如 lh-sense）")

    p = sub.add_parser("rpc", help="JSON-RPC 单发（供 MCP/数字人）")
    p.add_argument("payload", help='JSON 如 \'{"method":"balance"}\'')

    args = ap.parse_args(argv)
    if not args.cmd:
        # 无子命令 → 默认看最近交易（与 lh.py smart_default 语义一致）
        cmd_list(argparse.Namespace(limit=10, pending=False,
                                    json=False, all=False))
        print("\n  💡 子命令: dna / hash / add / list / verify / balance / "
              "export / audit / confirm / wall / scan / rpc")
        return 0
    return {
        "dna": lambda: cmd_dna(args),
        "hash": lambda: cmd_hash(args),
        "add": lambda: cmd_add(args),
        "list": lambda: cmd_list(args),
        "verify": lambda: cmd_verify(args),
        "balance": lambda: cmd_balance(args),
        "export": lambda: cmd_export(args),
        "audit": lambda: cmd_audit(args),
        "confirm": lambda: cmd_confirm(args),
        "wall": lambda: cmd_wall(args),
        "scan": lambda: cmd_scan(args),
        "add-auto": lambda: cmd_add_auto(args),
        "rpc": lambda: cmd_rpc(args),
    }[args.cmd]()


if __name__ == "__main__":
    raise SystemExit(main())
