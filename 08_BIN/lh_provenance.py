#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·逻辑溯源引擎 (Logical Provenance Engine) v2.0
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
创建者: 诸葛鑫（UID9622）
协议: 思想层 CC BY-NC-SA 4.0（溯源标注体系）

功能: 三层溯源(哲学/数学/工程) + 原创/AI协作 · 置信度评级 · SHA-256内容校验
      注入/批量/校验/持久化(SQLite+JSON双轨) · 确认码闸门 · 可选GPG签名验证

融合: 复用 lh_dna_generator(标准干支四柱+卦) + lh_gpg_sign(系统签名引擎)
      + lh_time_engine(时间戳) · 全部 try/except 优雅降级 · 零三方依赖
DNA: #龍芯⚡️<运行时生成>-LOGICAL-PROVENANCE-v2.0-UID9622
"""

import os
import sys
import json
import hashlib
import hmac
import threading
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

UID = "9622"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
ENGINE_VERSION = "v2.0"
DEFAULT_DATA_DIR = "~/.longhun/provenance"

# 复用龍魂现有引擎（DNA + 时间戳 + GPG）· 优雅降级
_DNA_OK = _TIME_OK = _GPG_OK = False
try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from lh_dna_generator import generate as _dna_generate  # type: ignore
    _DNA_OK = True
except Exception:
    pass

try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from lh_time_engine import get_output_stamp as _lh_stamp  # type: ignore
    _TIME_OK = True
except Exception:
    pass

try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from lh_gpg_sign import sign_file as _gpg_sign_file, verify_file as _gpg_verify_file  # type: ignore
    _GPG_OK = True
except Exception:
    pass


def make_dna(action: str = "PROVENANCE", version: str = ENGINE_VERSION) -> str:
    """生成DNA：优先复用 lh_dna_generator 标准干支四柱+卦，失败本地兜底。"""
    if _DNA_OK:
        try:
            payload = _dna_generate(title=action, category="engine", action=action, actor="UID9622")
            return payload.dna_string
        except Exception:
            pass
    return f"#龍芯⚡️{datetime.now().isoformat()}·{action}·{version}·UID9622-FALLBACK"


def output_stamp() -> str:
    """输出时间戳（第十七层·优先复用 lh_time_engine，降级简单格式）"""
    if _TIME_OK:
        try:
            return _lh_stamp()
        except Exception:
            pass
    return f"🐉{datetime.now().strftime('%Y-%m-%d %H:%M')}"

# ════════════════════════════════════════════════════════════
# 溯源标注体系
# ════════════════════════════════════════════════════════════
CATEGORY_NAMES = {
    "philosophy": "📜 哲学层 inspired_by（我的世界观从哪来）",
    "mathematics": "🔢 数学层 derived_from（我的算法从哪来）",
    "engineering": "⚙️ 工程层 based_on（我的实现从哪来）",
    "original": "🐉 原创层 original（龍魂系统原创）",
    "ai_collaboration": "🤖 AI协作 ai_assisted（AI辅助生成记录）",
}


def _confidence_mark(conf: float) -> str:
    """置信度 → 三色标记"""
    return "🟢" if conf >= 0.9 else "🟡" if conf >= 0.7 else "🔴"


@dataclass
class SourceRecord:
    """单一来源记录"""
    category: str            # philosophy / mathematics / engineering / original / ai_collaboration
    source_name: str         # 来源名称
    reference: str           # 具体引用（章节/论文/版本）
    influence: str           # 对系统的影响描述
    confidence: float        # 置信度 0.0-1.0
    url: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)


# ════════════════════════════════════════════════════════════
# 龍魂核心模块溯源数据库（融合协议v2.0 + 龍魂现行模块）
# ════════════════════════════════════════════════════════════
PROVENANCE_DB: Dict[str, List[SourceRecord]] = {
    "三色审计引擎": [
        SourceRecord("mathematics", "Modulo 9 Digital Root", "dr(n) = 1 + ((n-1) mod 9)",
                     "三色分类核心计算", 1.0),
        SourceRecord("philosophy", "易经·系辞上", "第十二章：圣人立象以尽意",
                     "象征系统设计的底层哲学", 0.95),
        SourceRecord("original", "三色审计引擎", "UID9622·2025-01",
                     "核心治理机制，完全原创", 1.0),
    ],
    "DNA追溯链": [
        SourceRecord("mathematics", "SHA-256", "FIPS 180-4",
                     "哈希链不可篡改性", 1.0),
        SourceRecord("philosophy", "道德经·第二十五章", "独立而不改，周行而不殆",
                     "不动点哲学的东方表达", 0.90),
        SourceRecord("engineering", "Blockchain", "Bitcoin Whitepaper 2008",
                     "链式结构参考", 0.80),
        SourceRecord("original", "DNA追溯链", "UID9622·2025-01",
                     "干支+哈希的独创组合", 1.0),
    ],
    "24人格矩阵": [
        SourceRecord("philosophy", "荣格心理学", "The Archetypes and the Collective Unconscious (1959)",
                     "人格原型理论基础", 0.85),
        SourceRecord("philosophy", "易经·六十四卦", "六十四卦人格映射",
                     "东方人格分类体系", 0.90),
        SourceRecord("original", "24人格矩阵", "UID9622·2025-03",
                     "16人格扩展+8个特殊角色", 1.0),
    ],
    "主权网关": [
        SourceRecord("engineering", "Zero Trust Architecture", "NIST SP 800-207",
                     "永不信任，始终验证", 0.85),
        SourceRecord("philosophy", "中庸·第二章", "不偏之谓中，不易之谓庸",
                     "平衡决策逻辑", 0.80),
        SourceRecord("original", "主权网关", "UID9622·2025-02",
                     "统一接入控制，完全原创", 1.0),
    ],
    "不动点引擎": [
        SourceRecord("mathematics", "Banach Fixed Point Theorem",
                     "Sur les opérations dans les ensembles abstraits (1922)",
                     "压缩映射存在唯一不动点", 1.0),
        SourceRecord("mathematics", "Gödel's Incompleteness Theorems",
                     "On Formally Undecidable Propositions (1931)",
                     "自指边界的数学极限", 0.95),
        SourceRecord("philosophy", "道德经·第十六章", "致虚极，守静笃",
                     "系统根基稳定的东方表达", 0.85),
        SourceRecord("original", "不动点引擎", "UID9622·2025-04",
                     "收敛判定+动态调节", 1.0),
    ],
    "反馈闭环": [
        SourceRecord("mathematics", "Cybernetics", "Wiener·Cybernetics (1948)",
                     "反馈控制理论基础", 0.90),
        SourceRecord("philosophy", "易经·系辞下", "易穷则变，变则通，通则久",
                     "系统演化哲学", 0.90),
        SourceRecord("original", "反馈闭环", "UID9622·2025-05",
                     "感知→认知→修正→再感知", 1.0),
    ],
    # ── 龍魂融合新增（2026-08-20）──
    "ADS自描述系统": [
        SourceRecord("engineering", "Model Context Protocol", "MCP Spec v2024-11-05",
                     "上下文协议参考（四层认知自指设计）", 0.85),
        SourceRecord("philosophy", "道德经·第三十三章", "知人者智，自知者明",
                     "自描述/自指认知的东方哲学根", 0.90),
        SourceRecord("original", "ADS自描述系统", "UID9622·2026-08",
                     "四层递归自指认知+确认码闸门，原创", 1.0),
    ],
    "天眼生态看板": [
        SourceRecord("engineering", "REST API", "HTTP/1.1 RFC 9110",
                     "看板实时数据链路", 0.85),
        SourceRecord("original", "天眼生态看板", "UID9622·2026-08",
                     "三色相位聚合+真实探针，原创", 1.0),
    ],
    "逻辑溯源引擎": [
        SourceRecord("mathematics", "SHA-256", "FIPS 180-4",
                     "溯源记录内容校验", 1.0),
        SourceRecord("philosophy", "道德经·第六十四章", "合抱之木，生于毫末",
                     "每一条逻辑都有根的思想", 0.90),
        SourceRecord("engineering", "GPG", "RFC 4880",
                     "分离签名验证来源可信", 0.90),
        SourceRecord("original", "逻辑溯源引擎", "UID9622·2026-08",
                     "三层溯源+置信度评级+双轨持久化，原创", 1.0),
    ],
}


# ════════════════════════════════════════════════════════════
# 安全层（P0: 确认码闸门 + SHA-256 校验）
# ════════════════════════════════════════════════════════════
class SecurityLayer:
    """安全层 — 确认码闸门 · SHA-256 内容校验 · 审计日志"""

    def verify_confirm_code(self, code: str) -> bool:
        try:
            return hmac.compare_digest(code.encode("utf-8"), CONFIRM_CODE.encode("utf-8"))
        except Exception:
            return False

    def compute_checksum(self, content: str, algorithm: str = "sha256") -> str:
        if algorithm == "sha256":
            return hashlib.sha256(content.encode("utf-8")).hexdigest()
        raise ValueError(f"不支持的算法: {algorithm}")

    def verify_checksum(self, content: str, expected: str, algorithm: str = "sha256") -> bool:
        return hmac.compare_digest(self.compute_checksum(content, algorithm), expected)

    def audit_log(self, action: str, identity: str, result: str):
        try:
            log_dir = Path(DEFAULT_DATA_DIR).expanduser() / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            with open(log_dir / "provenance-audit.log", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now().isoformat()} | action={action} | identity={identity} | result={result}\n")
        except Exception:
            pass

# ════════════════════════════════════════════════════════════
# 持久化层（SQLite 主 + JSON 双轨 · 可GPG签名·可审计）
# ════════════════════════════════════════════════════════════
class PersistenceLayer:
    """持久化层 — SQLite 主库 + JSON 文件双轨（JSON 供 GPG 分离签名验证）"""

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir).expanduser()
        self.db_path = self.data_dir / "provenance.db"
        self.json_dir = self.data_dir / "json"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.json_dir.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        self._init_db()

    def _init_db(self):
        with self.lock:
            conn = sqlite3.connect(self.db_path, timeout=10)
            try:
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS provenance_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        module TEXT NOT NULL,
                        dna TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        checksum TEXT NOT NULL,
                        content TEXT NOT NULL,
                        status TEXT DEFAULT '🟢',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.execute("CREATE INDEX IF NOT EXISTS idx_module ON provenance_records(module)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_dna ON provenance_records(dna)")
                conn.commit()
            finally:
                conn.close()

    def save(self, record: Dict) -> Path:
        """保存记录：SQLite + JSON 双轨，返回 JSON 文件路径（供 GPG 签名）"""
        with self.lock:
            conn = sqlite3.connect(self.db_path, timeout=10)
            try:
                conn.execute("""
                    INSERT INTO provenance_records (module, dna, timestamp, checksum, content, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    record.get("module", ""),
                    record.get("dna", ""),
                    record.get("timestamp", datetime.now().isoformat()),
                    record.get("checksum", ""),
                    json.dumps(record, ensure_ascii=False),
                    record.get("status", "🟢"),
                ))
                conn.commit()
            finally:
                conn.close()
            safe = "".join(c for c in record.get("module", "module") if c.isalnum() or c in "_-")
            json_path = self.json_dir / f"{safe}.json"
            json_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        return json_path

    def load_by_module(self, module: str, limit: int = 100) -> List[Dict]:
        with self.lock:
            conn = sqlite3.connect(self.db_path, timeout=10)
            try:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    "SELECT * FROM provenance_records WHERE module = ? ORDER BY timestamp DESC LIMIT ?",
                    (module, limit))
                return [dict(row) for row in cursor.fetchall()]
            finally:
                conn.close()

    def load_all(self, limit: int = 1000) -> List[Dict]:
        with self.lock:
            conn = sqlite3.connect(self.db_path, timeout=10)
            try:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    "SELECT * FROM provenance_records ORDER BY timestamp DESC LIMIT ?", (limit,))
                return [dict(row) for row in cursor.fetchall()]
            finally:
                conn.close()

    def get_stats(self) -> Dict:
        with self.lock:
            conn = sqlite3.connect(self.db_path, timeout=10)
            try:
                total = conn.execute("SELECT COUNT(*) FROM provenance_records").fetchone()[0]
                modules = conn.execute("SELECT COUNT(DISTINCT module) FROM provenance_records").fetchone()[0]
                return {"total_records": total, "unique_modules": modules}
            finally:
                conn.close()

# ════════════════════════════════════════════════════════════
# 核心引擎
# ════════════════════════════════════════════════════════════
class LogicalProvenanceEngine:
    """逻辑溯源引擎 v2.0 · 注入/批量/校验/报告/统计"""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir or os.environ.get("LONGHUN_PROV_DATA_DIR", DEFAULT_DATA_DIR)).expanduser()
        self.security = SecurityLayer()
        self.persistence = PersistenceLayer(self.data_dir)
        self.db = PROVENANCE_DB
        self.lock = threading.RLock()
        self.dna = make_dna("PROVENANCE-ENGINE", ENGINE_VERSION)

    def _confirm_required(self) -> bool:
        return os.environ.get("LONGHUN_PROV_CONFIRM", "1") != "0"

    def inject(self, module_name: str, confirm_code: str = "", gpg_sign: bool = False) -> Dict:
        """为模块注入逻辑溯源 · P0确认码闸门"""
        if self._confirm_required() and not self.security.verify_confirm_code(confirm_code):
            self.security.audit_log("inject", module_name, "REJECTED: invalid confirm code")
            return {"error": "确认码验证失败", "status": "🔴", "code": 403}

        with self.lock:
            sources = self.db.get(module_name, []) or self._fuzzy_match(module_name)
            record = {
                "module": module_name,
                "dna": make_dna(f"PROV-{module_name}", ENGINE_VERSION),
                "timestamp": datetime.now().isoformat(),
                "sources": [s.to_dict() for s in sources],
                "status": "🟢",
                "engine_version": ENGINE_VERSION,
            }
            probe = {k: v for k, v in record.items() if k != "checksum"}
            record["checksum"] = self.security.compute_checksum(
                json.dumps(probe, ensure_ascii=False, sort_keys=True))

            json_path = self.persistence.save(record)

            gpg_result = None
            if gpg_sign and _GPG_OK and json_path:
                try:
                    gpg_result = _gpg_sign_file(str(json_path), force=True)
                except Exception as e:
                    gpg_result = {"ok": False, "error": str(e)}

            self.security.audit_log("inject", module_name, "SUCCESS")
            record["gpg_signed"] = bool(gpg_result and gpg_result.get("status") == "ok")
            return record

    def _fuzzy_match(self, module_name: str) -> List[SourceRecord]:
        """模糊匹配模块名；无匹配自动标记原创(0.5·🟡待验)"""
        for key in self.db:
            if key in module_name or module_name in key:
                return self.db[key]
        return [SourceRecord("original", module_name, "UID9622·auto",
                             "自动标记为原创（无匹配来源·待核）", 0.5)]

    def batch_inject(self, directory: str, pattern: str = "*.py",
                     confirm_code: str = "", gpg_sign: bool = False,
                     limit: int = 500) -> List[Dict]:
        """批量注入目录下模块（限500防性能黑洞）"""
        results = []
        base = Path(directory)
        for file in list(base.rglob(pattern))[:limit]:
            module_name = file.stem
            results.append(self.inject(module_name, confirm_code, gpg_sign))
        return results

    def verify(self, module_name: str, expected_checksum: str = "",
               gpg: bool = False) -> Dict:
        """验证溯源记录完整性：SHA-256 自校验（可选外部期望值 + GPG 文件签名）"""
        records = self.persistence.load_by_module(module_name, limit=1)
        if not records:
            return {"verified": False, "reason": "无溯源记录", "status": "🔴"}

        record = json.loads(records[0]["content"])
        probe = {k: v for k, v in record.items() if k != "checksum"}
        content_json = json.dumps(probe, ensure_ascii=False, sort_keys=True)
        target = expected_checksum or record.get("checksum", "")

        ok = self.security.verify_checksum(content_json, target)
        result = {"verified": ok, "status": "🟢" if ok else "🔴"}
        if ok:
            result["dna"] = record.get("dna", "")
        else:
            result["reason"] = "校验和不匹配（内容可能被篡改）"

        if gpg and ok and _GPG_OK:
            safe = "".join(c for c in module_name if c.isalnum() or c in "_-")
            json_path = self.persistence.json_dir / f"{safe}.json"
            if json_path.exists():
                gv = _gpg_verify_file(str(json_path))
                result["gpg"] = gv
                result["gpg_verified"] = gv.get("status") == "verified"
        return result

    def list_modules(self) -> List[str]:
        return list(self.db.keys())

    def get_stats(self) -> Dict:
        db_stats = self.persistence.get_stats()
        return {
            "registered_modules": len(self.db),
            "persistence": db_stats,
            "engine_dna": self.dna,
            "dna_engine": "lh_dna_generator" if _DNA_OK else "fallback",
            "gpg_engine": "lh_gpg_sign" if _GPG_OK else "unavailable",
            "time_stamp": output_stamp(),
        }

    def generate_markdown(self, record: Dict) -> str:
        """生成 Markdown 溯源报告"""
        lines = [f"## 🧬 逻辑溯源 · {record['module']}", "",
                 f"**DNA:** `{record['dna']}`",
                 f"**时间:** {record['timestamp']}",
                 f"**校验和:** `{record.get('checksum', 'N/A')}`",
                 f"**引擎:** {record.get('engine_version', ENGINE_VERSION)}", ""]
        categories: Dict[str, List] = {}
        for src in record.get("sources", []):
            categories.setdefault(src.get("category", "unknown"), []).append(src)
        for cat, sources in categories.items():
            lines.append(f"### {CATEGORY_NAMES.get(cat, cat)}")
            lines.append("")
            for src in sources:
                lines.append(f"- **{src['source_name']}**")
                if src.get("reference"):
                    lines.append(f"  - 引用: `{src['reference']}`")
                lines.append(f"  - 影响: {src.get('influence', '')}")
                conf = float(src.get("confidence", 0))
                lines.append(f"  - 置信度: {_confidence_mark(conf)} {conf}")
                lines.append("")
        lines.append(f"---\n{output_stamp()}")
        return "\n".join(lines)

# ════════════════════════════════════════════════════════════
# CLI 入口
# ════════════════════════════════════════════════════════════
def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="🐉 龍魂·逻辑溯源引擎 (LPE) v2.0")
    ap.add_argument("--inject", "-i", type=str, help="注入单个模块")
    ap.add_argument("--batch", "-b", type=str, help="批量注入目录")
    ap.add_argument("--pattern", type=str, default="*.py", help="批量匹配模式")
    ap.add_argument("--limit", type=int, default=500, help="批量上限(防黑洞)")
    ap.add_argument("--verify", "-v", type=str, help="验证模块完整性")
    ap.add_argument("--checksum", type=str, default="", help="期望校验和(默认用库内最新)")
    ap.add_argument("--gpg", action="store_true", help="verify时校验JSON双轨GPG签名")
    ap.add_argument("--gpg-sign", action="store_true", help="inject时对JSON双轨做GPG分离签名")
    ap.add_argument("--list", "-l", action="store_true", help="列出所有模块")
    ap.add_argument("--stats", "-s", action="store_true", help="统计信息")
    ap.add_argument("--json", "-j", action="store_true", help="JSON输出")
    ap.add_argument("--confirm-code", type=str, default="", help="确认码(P0闸门·CLI默认内置)")
    ap.add_argument("--data-dir", type=str, default="", help="数据目录(默认~/.longhun/provenance)")
    args = ap.parse_args(argv)

    engine = LogicalProvenanceEngine(args.data_dir or None)
    confirm = args.confirm_code or CONFIRM_CODE

    if args.list:
        modules = engine.list_modules()
        print(f"🐉 已注册溯源模块 ({len(modules)}):")
        for m in modules:
            print(f"  · {m}")
        return 0

    if args.stats:
        s = engine.get_stats()
        if args.json:
            print(json.dumps(s, indent=2, ensure_ascii=False))
        else:
            print("📊 逻辑溯源统计:")
            print(f"  注册模块: {s['registered_modules']}")
            print(f"  持久化记录: {s['persistence']['total_records']}")
            print(f"  唯一模块: {s['persistence']['unique_modules']}")
            print(f"  DNA引擎: {s['dna_engine']} · GPG引擎: {s['gpg_engine']}")
            print(f"  引擎DNA: {s['engine_dna']}")
        return 0

    if args.inject:
        r = engine.inject(args.inject, confirm, gpg_sign=args.gpg or args.gpg_sign)
        if "error" in r:
            print(f"🔴 错误: {r['error']}")
            return 1
        if args.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            print(engine.generate_markdown(r))
        return 0

    if args.batch:
        rs = engine.batch_inject(args.batch, args.pattern, confirm,
                                 gpg_sign=args.gpg or args.gpg_sign, limit=args.limit)
        ok = sum(1 for r in rs if "error" not in r)
        print(f"📦 批量注入: {ok}/{len(rs)} 成功")
        for r in rs:
            print(f"  {r.get('status', '🔴')} {r.get('module', 'unknown')}")
        return 0

    if args.verify:
        r = engine.verify(args.verify, args.checksum, gpg=args.gpg)
        if args.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            mark = "🟢" if r.get("verified") else "🔴"
            print(f"{mark} {args.verify}: {r.get('reason', '完整')}"
                  + (f" · GPG:{r['gpg_verified']}" if "gpg_verified" in r else ""))
        return 0 if r.get("verified") else 1

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
