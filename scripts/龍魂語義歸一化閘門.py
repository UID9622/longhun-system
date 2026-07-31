# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 語義歸一化與知識庫准入閘門
DNA:#龍芯⚡️2026-06-30-LONGHUN-SEMANTIC-GATE-FILE1-v1.0

解決問題：
  1. 繁體/簡體、全形/半形、大小寫、口語化、多語言組合、拆分表達
     必須被實時歸一化，不能繞過審核。
  2. 知識庫納入標準：只收“可識別、可變量、通過主權檢查”的內容；
     不識別的內容進隔離區（quarantine），有害的內容直接熔斷（reject）。

輸出決策：
  ADMIT    → 可納入知識庫
  QUARANTINE → 先吸入容器，不展現、不用於訓練，僅供威脅分析
  REJECT   → 熔斷，不納入知識庫
"""

import argparse
import hashlib
import json
import re
import secrets
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# ---------- 路徑 ----------
PATTERNS_PATH = Path.home() / ".龍魂" / "semantic_gate_patterns.json"
SEMANTIC_LIBRARY_PATH = Path.home() / ".kimi-code" / "skills" / "CNSH-SEMANTIC" / "semantic_library.json"
QUARANTINE_PATH = Path.home() / ".龍魂" / "kb_quarantine.jsonl"
ADMITTED_PATH = Path.home() / ".龍魂" / "kb_admitted.jsonl"
GATE_AUDIT_PATH = Path.home() / "longhun-system" / "logs" / "龍魂知識庫准入審計.jsonl"

DNA_PREFIX = "#龍芯⚡️"


# ---------- 工具 ----------
def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _event_dna(event: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    rand = secrets.token_hex(4).upper()
    return f"{DNA_PREFIX}{ts}-SEMANTIC-GATE-{event}-{rand}"


def _ensure_paths() -> None:
    for p in (QUARANTINE_PATH, ADMITTED_PATH, GATE_AUDIT_PATH):
        p.parent.mkdir(parents=True, exist_ok=True)


def _append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


# ---------- OpenCC 繁簡轉換（優先使用本地 venv） ----------
def _load_opencc_converter() -> Optional[Any]:
    venv_site = Path.home() / ".龍魂" / ".venv-observer" / "lib" / "python3.14" / "site-packages"
    if str(venv_site) not in sys.path:
        sys.path.insert(0, str(venv_site))
    try:
        import opencc
        return opencc.OpenCC("t2s")
    except Exception:
        return None


# ---------- 語義歸一化 ----------
class SemanticNormalizer:
    """把任意語言輸入歸一到同一語義空間。"""

    def __init__(self) -> None:
        self._converter = _load_opencc_converter()

    def normalize(self, text: str) -> str:
        if not isinstance(text, str):
            text = str(text)
        # 1. Unicode 兼容分解 + 重組（全形轉半形、合字拆分等）
        text = unicodedata.normalize("NFKC", text)
        # 2. 小寫化（對拉丁、希臘、西里爾等有效）
        text = text.lower()
        # 3. 繁體轉簡體（如果 opencc 可用）
        if self._converter:
            text = self._converter.convert(text)
        # 4. 把標點、特殊符號、空白統一為單空格
        text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenize(self, text: str) -> list[str]:
        return [t for t in self.normalize(text).split(" ") if t]

    def fingerprint(self, text: str) -> str:
        """生成語義指紋：排序後唯一 token 的拼接。"""
        tokens = sorted(set(self.tokenize(text)))
        return " ".join(tokens)


# ---------- 語義模式庫 ----------
class SovereigntyPatternMatcher:
    """加載並匹配主權相關語義模式。"""

    def __init__(self, patterns_path: Path = PATTERNS_PATH) -> None:
        self.normalizer = SemanticNormalizer()
        self.patterns = self._load_patterns(patterns_path)

    def _load_patterns(self, path: Path) -> list[dict[str, Any]]:
        data = _load_json(path, {"patterns": []})
        patterns = data.get("patterns", [])
        # 把每個 pattern 的 aliases 預先歸一化
        for p in patterns:
            p["_normalized_aliases"] = sorted(
                set(self.normalizer.normalize(a) for a in p.get("aliases", [])),
                key=len,
                reverse=True,
            )
            p["_normalized_canonical"] = self.normalizer.normalize(p.get("canonical", ""))
        return patterns

    @staticmethod
    def _alias_matches(norm: str, alias: str) -> bool:
        """支持兩種匹配：
        - 無空格別名：子串匹配（應對連寫變體）
        - 含空格別名：token 順序匹配（應對插入口語詞、拆分）
        """
        if not alias:
            return False
        if " " not in alias:
            return alias in norm
        alias_tokens = alias.split()
        text_tokens = norm.split()
        idx = 0
        for tok in text_tokens:
            if tok == alias_tokens[idx]:
                idx += 1
                if idx == len(alias_tokens):
                    return True
        return False

    def match(self, text: str) -> list[dict[str, Any]]:
        """返回命中的模式列表（含原始文本、歸一化文本、命中別名）。"""
        norm = self.normalizer.normalize(text)
        hits = []
        for p in self.patterns:
            for alias in p.get("_normalized_aliases", []):
                if self._alias_matches(norm, alias):
                    hits.append({
                        "pattern_id": p.get("id"),
                        "category": p.get("category"),
                        "action": p.get("action"),
                        "canonical": p.get("canonical"),
                        "matched_alias": alias,
                        "normalized_input": norm,
                    })
                    break  # 一個 pattern 只命中一次
        return hits

    def detect_bypass(self, text: str) -> list[dict[str, Any]]:
        """專門檢測繞過企圖：拆分、插入符號、同義替換。"""
        norm = self.normalizer.normalize(text)
        bypass_hits = []
        for p in self.patterns:
            if p.get("category") != "bypass_attempt":
                continue
            for alias in p.get("_normalized_aliases", []):
                if self._alias_matches(norm, alias):
                    bypass_hits.append({
                        "pattern_id": p.get("id"),
                        "canonical": p.get("canonical"),
                        "matched_alias": alias,
                    })
                    break
        return bypass_hits


# ---------- 知識庫准入閘門 ----------
class KnowledgeBaseGate:
    """決定內容能否納入知識庫：ADMIT / QUARANTINE / REJECT。"""

    def __init__(self) -> None:
        self.normalizer = SemanticNormalizer()
        self.matcher = SovereigntyPatternMatcher()
        _ensure_paths()

    def evaluate(
        self,
        content: str,
        source_lang: str = "auto",
        source: str = "unknown",
        operator: str = "UID9622",
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        norm = self.normalizer.normalize(content)
        fp = self.normalizer.fingerprint(content)
        matches = self.matcher.match(content)
        bypasses = self.matcher.detect_bypass(content)

        # LU 记忆准入通道：长文本压缩属于本地记忆归集，默认 ADMIT
        # 集思广益准入通道： raw ideas 允许进入系统，默认 ADMIT
        # 但若命中熔断规则或绕过企图，仍按原规则处理
        is_lu_memory = source == "lu_compression" or (metadata or {}).get("lu_memory") is True
        is_collective_wisdom = source == "collective_wisdom" or (metadata or {}).get("cw_idea") is True

        # 決策邏輯
        rule_statement_matches = [m for m in matches if m.get("category") == "rule_statement"]
        reject_matches = [m for m in matches if m.get("action") == "reject" and m.get("category") != "rule_statement"]
        admit_matches = [m for m in matches if m.get("action") == "admit" and m.get("category") != "rule_statement"]

        if bypasses:
            decision = "REJECT"
            reason = "检测到绕过企图"
        elif is_lu_memory and not reject_matches:
            decision = "ADMIT"
            reason = "LU 记忆内容默认准入（本地记忆归集）"
        elif is_collective_wisdom and not reject_matches:
            decision = "ADMIT"
            reason = "集思广益 raw idea 默认准入，允许未成形想法进入系统"
        elif rule_statement_matches:
            decision = "ADMIT"
            reason = f"識別到主權規則陳述：{rule_statement_matches[0].get('canonical')}"
        elif reject_matches:
            decision = "REJECT"
            reason = "命中熔断规则"
        elif admit_matches:
            decision = "ADMIT"
            reason = f"識別到 {len(admit_matches)} 條可納入主權語義模式"
        else:
            decision = "QUARANTINE"
            reason = "內容無法被當前語義庫識別或變量化，先收入隔離容器"

        record = {
            "dna": _event_dna(decision),
            "timestamp": _now(),
            "source": source,
            "source_lang": source_lang,
            "operator": operator,
            "content_preview": content[:500],
            "content_hash": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            "normalized_preview": norm[:500],
            "semantic_fingerprint": fp,
            "decision": decision,
            "reason": reason,
            "matches": matches,
            "bypass_attempts": bypasses,
            "metadata": metadata or {},
        }

        # 根據決策寫入不同容器
        if decision == "REJECT":
            _append_jsonl(GATE_AUDIT_PATH, record)
        elif decision == "QUARANTINE":
            _append_jsonl(QUARANTINE_PATH, record)
            _append_jsonl(GATE_AUDIT_PATH, record)
        else:
            _append_jsonl(ADMITTED_PATH, record)
            _append_jsonl(GATE_AUDIT_PATH, record)

        return {
            "ok": decision != "REJECT",
            "decision": decision,
            "reason": reason,
            "matches": matches,
            "bypass_attempts": bypasses,
            "dna": record["dna"],
        }

    def query_quarantine(self, limit: int = 20) -> list[dict[str, Any]]:
        records = []
        if QUARANTINE_PATH.exists():
            with QUARANTINE_PATH.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        records.append(json.loads(line))
                    except Exception:
                        continue
        return records[-limit:]


# ---------- 默認模式庫初始化 ----------
def _default_patterns() -> dict[str, Any]:
    """如果模式庫不存在，寫入預設主權語義模式。"""
    patterns = {
        "dna": f"{DNA_PREFIX}2026-06-30-SEMANTIC-GATE-PATTERNS-v1.0",
        "description": "DNA 主權與內容准入語義模式。aliases 已預先收錄簡繁、中英文、口語化、拆分變體。",
        "patterns": [
            {
                "id": "dna_transfer",
                "canonical": "DNA不可转让",
                "category": "dna_sovereignty",
                "action": "reject",
                "aliases": [
                    "dna 转让", "dna 轉讓", "轉讓 dna", "转让 dna",
                    "transfer dna", "dna transfer", "dna uebertragung",
                    "卖 dna", "賣 dna", "sell dna", "dna 买卖", "dna 買賣",
                    "借 dna", "lend dna", "rent dna", "出租 dna",
                    "把 dna 给", "把 dna 給", "give dna to", "hand over dna",
                    "轉 dna", "转 dna", "过户 dna", "過戶 dna",
                    "一世一双人 转让", "一世一雙人 轉讓",
                ],
            },
            {
                "id": "dna_overwrite",
                "canonical": "DNA不可覆盖",
                "category": "dna_sovereignty",
                "action": "reject",
                "aliases": [
                    "覆盖 dna", "覆蓋 dna", "overwrite dna", "修改 dna 记录",
                    "重写 dna", "重寫 dna", "篡改 dna", "篡改 dna",
                    "替换 dna", "替換 dna", "replace dna",
                    "清空 dna 历史", "清空 dna 歷史", "delete dna history",
                ],
            },
            {
                "id": "dna_inherit",
                "canonical": "DNA可继承",
                "category": "dna_sovereignty",
                "action": "admit",
                "aliases": [
                    "继承 dna", "繼承 dna", "inherit dna", "dna inheritance",
                    "后人继承", "後人繼承", "传给后代", "傳給後代",
                    "dna 继承链", "dna 繼承鏈",
                ],
            },
            {
                "id": "contribution_monetize",
                "canonical": "贡献不可变现",
                "category": "contribution_sovereignty",
                "action": "reject",
                "aliases": [
                    "贡献 变现", "貢獻 變現", "monetize contribution",
                    "贡献 换钱", "貢獻 換錢", "contribution to cash",
                    "积分 兑换", "積分 兌換", "points exchange",
                    "贡献 买卖", "貢獻 買賣", "sell contribution",
                    "贡献 转让", "貢獻 轉讓", "transfer contribution",
                    "把贡献换成", "把貢獻換成",
                ],
            },
            {
                "id": "contribution_spend",
                "canonical": "贡献不可消费",
                "category": "contribution_sovereignty",
                "action": "reject",
                "aliases": [
                    "消费贡献", "消費貢獻", "spend contribution",
                    "用贡献买", "用貢獻買", "buy with contribution",
                    "贡献 当钱花", "貢獻 當錢花",
                    "抵扣贡献", "抵扣貢獻",
                ],
            },
            {
                "id": "one_person_one_dna",
                "canonical": "一世一双人",
                "category": "dna_sovereignty",
                "action": "admit",
                "aliases": [
                    "一世一双人", "一世一雙人", "one person one dna",
                    "一人一号", "一人一號", "one dna one person",
                    "一个 dna 一个人", "一個 dna 一個人",
                    "dna 绑定个人", "dna 綁定個人",
                ],
            },
            {
                "id": "person_is_one",
                "canonical": "人永远是1",
                "category": "dna_sovereignty",
                "action": "admit",
                "aliases": [
                    "人永远是 1", "人永遠是 1", "person is one",
                    "人不是数据", "人不是數據", "person not data",
                    "人是 1 不是 0", "人是 1 不是 0",
                    "主权在人", "主權在人",
                ],
            },
            {
                "id": "append_only_history",
                "canonical": "历史append-only",
                "category": "audit_sovereignty",
                "action": "admit",
                "aliases": [
                    "append only", "只增不删", "只增不刪", "只能追加",
                    "历史不可删", "歷史不可刪", "history cannot delete",
                    "不可删除", "不可刪除", "do not delete",
                ],
            },
            {
                "id": "bypass_attempt",
                "canonical": "检测到绕过企图",
                "category": "bypass_attempt",
                "action": "reject",
                "aliases": [
                    "绕过", "繞過", "bypass", "繞過審核", "绕过审核",
                    "钻空子", "鑽空子", "找漏洞", "exploit loophole",
                    "换个说法", "換個說法", "用别的方式", "用別的方式",
                    "拆分表达", "拆分表達", "split words",
                    "口语化", "口語化", "colloquial",
                    "假装不懂", "假裝不懂", "play dumb",
                ],
            },
        ],
    }
    PATTERNS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PATTERNS_PATH.write_text(json.dumps(patterns, ensure_ascii=False, indent=2), encoding="utf-8")
    return patterns


def init_patterns() -> None:
    if not PATTERNS_PATH.exists():
        _default_patterns()


# ---------- CLI ----------
def main(argv: list[str] | None = None) -> int:
    init_patterns()
    parser = argparse.ArgumentParser(description="龍魂語義歸一化與知識庫准入閘門")
    sub = parser.add_subparsers(dest="cmd")

    p_norm = sub.add_parser("normalize", help="歸一化文本")
    p_norm.add_argument("--text", required=True)

    p_match = sub.add_parser("match", help="匹配主權語義模式")
    p_match.add_argument("--text", required=True)

    p_eval = sub.add_parser("evaluate", help="評估內容准入")
    p_eval.add_argument("--text", required=True)
    p_eval.add_argument("--source", default="cli")
    p_eval.add_argument("--lang", default="auto")

    p_quarantine = sub.add_parser("quarantine", help="查看隔離區最近記錄")
    p_quarantine.add_argument("--limit", type=int, default=10)

    args = parser.parse_args(argv)
    if args.cmd == "normalize":
        n = SemanticNormalizer()
        print(json.dumps({
            "original": args.text,
            "normalized": n.normalize(args.text),
            "tokens": n.tokenize(args.text),
            "fingerprint": n.fingerprint(args.text),
        }, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "match":
        m = SovereigntyPatternMatcher()
        hits = m.match(args.text)
        bypasses = m.detect_bypass(args.text)
        print(json.dumps({
            "normalized": SemanticNormalizer().normalize(args.text),
            "matches": hits,
            "bypass_attempts": bypasses,
        }, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "evaluate":
        gate = KnowledgeBaseGate()
        result = gate.evaluate(args.text, args.lang, args.source)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1

    if args.cmd == "quarantine":
        gate = KnowledgeBaseGate()
        records = gate.query_quarantine(args.limit)
        print(json.dumps({"count": len(records), "records": records}, ensure_ascii=False, indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
