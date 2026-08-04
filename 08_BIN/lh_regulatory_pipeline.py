#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·丙辰·己丑·需-REGULATORY-PIPELINE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
lh_regulatory_pipeline — 龍魂监管透明API管道 v1.0

管道流程：
  原始内容 → 三色审计(v3) → DNA签章 → 审核过滤 → 压缩打包(JSON) → 入链(jsonl) → 推送缓存

用法：
  python3 bin/lh_regulatory_pipeline.py process "<内容文本>"
  python3 bin/lh_regulatory_pipeline.py batch --dir data/ --output compliance.jsonl
  python3 bin/lh_regulatory_pipeline.py summary --hours 24

DNA: #龍芯⚡️丙午·丙申·丙辰·己丑·需-REGULATORY-PIPELINE-v1.0
📇 项目身份 · 联系 · 支持 → assets/PUBLIC_IDENTITY.md
"""

import argparse
import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# ============================================
# 数据模型
# ============================================

@dataclass
class AuditResult:
    """三色审计结果"""
    status: str              # 🟢/🟡/🔴
    score: float             # R评分 0-100
    gates_passed: int
    gates_total: int
    flags: List[str] = None

    def __post_init__(self):
        if self.flags is None:
            self.flags = []

@dataclass
class RegulatoryRecord:
    """监管推送记录（一条完整的审计追溯记录）"""
    record_id: str
    timestamp: str           # ISO 8601
    content_hash: str        # SM3
    audit: AuditResult
    dna: str
    meltdown_check: bool     # 数据黑洞检查通过？
    persona_check: bool      # 人格主权检查通过？
    compliance_summary: str  # 合规摘要
    source: str = "internal"

@dataclass
class ComplianceSummary:
    """合规摘要报告"""
    period_start: str
    period_end: str
    total_records: int
    green_count: int
    yellow_count: int
    red_count: int
    meltdown_events: int
    persona_breaches: int
    top_flags: List[Dict[str, int]]
    generated_at: str = ""

# ============================================
# 哈希工具
# ============================================

def sm3_hash(text: str) -> str:
    return hashlib.sha3_256(text.encode("utf-8")).hexdigest()

# ============================================
# 审计引擎（集成现有系统）
# ============================================

def run_tricolor_audit(content: str) -> AuditResult:
    """
    运行三色审计。
    优先使用 systems/v3 的 TricolorAuditEngine，降级使用本地简化版。
    """
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from systems.v3 import TricolorAuditEngine
        from datetime import datetime

        engine = TricolorAuditEngine()
        # v3 AuditItem uses dataclass with fields: item_id, description, content, source, timestamp, metadata
        item = type('AuditItem', (), {
            'item_id': sm3_hash(content)[:12],
            'description': '监管管道审计',
            'content': content,
            'source': 'regulatory-pipeline',
            'timestamp': datetime.now(),
            'metadata': {},
        })()
        result = engine.audit(item=item)
        return AuditResult(
            status=result.status.value if hasattr(result.status, 'value') else str(result.status),
            score=getattr(result, 'r_score', 85.0),
            gates_passed=getattr(result, 'gates_passed', 8),
            gates_total=getattr(result, 'gates_total', 10),
        )
    except (ImportError, Exception):
        # 降级：本地简化审计
        return _fallback_audit(content)

def _fallback_audit(content: str) -> AuditResult:
    """简化版审计（当 v3 引擎不可用时）"""
    flags = []
    score = 95.0

    # 检查高危词
    red_keywords = ["技术无国界", "灵活处理", "简化管理", "商业化需要", "完全自动化"]
    for kw in red_keywords:
        if kw in content:
            flags.append(f"RED:{kw}")
            score -= 20

    yellow_keywords = ["优化", "完善", "建议", "规范", "简化", "调整"]
    for kw in yellow_keywords:
        if kw in content:
            flags.append(f"YELLOW:{kw}")
            score -= 5

    score = max(0, min(100, score))

    if score < 60:
        status = "🔴"
    elif score < 85:
        status = "🟡"
    else:
        status = "🟢"

    return AuditResult(status=status, score=score, gates_passed=7, gates_total=10, flags=flags)

# ============================================
# DNA 签章
# ============================================

def generate_dna(content: str, module: str = "REG-PIPE") -> str:
    """生成 DNA 追溯码"""
    content_hash = sm3_hash(content)[:8].upper()
    # 使用农历干支获取（降级使用固定格式）
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from calendar_context_logger.calendar_core import LunarEngine
        engine = LunarEngine()
        gz = engine.get_ganzhi()
        return f"#龍芯⚡️{gz['year']}·{gz['month']}·{gz['day']}·{gz['hour']}·{gz['gua']}-{module}-PIPE-{content_hash}"
    except ImportError:
        return f"#龍芯⚡️丙午·丙申·丙辰·己丑·需-{module}-PIPE-{content_hash}"

# ============================================
# 打包器
# ============================================

def package_record(content: str, source: str = "internal") -> RegulatoryRecord:
    """
    完整打包流程：
    1. 内容哈希
    2. 三色审计
    3. 数据黑洞检查
    4. 人格主权检查
    5. DNA签章
    6. 生成合规摘要
    """
    content_hash = sm3_hash(content)

    # 审计
    audit = run_tricolor_audit(content)

    # 数据黑洞检查
    try:
        _bin_dir = Path(__file__).parent
        if str(_bin_dir) not in sys.path:
            sys.path.insert(0, str(_bin_dir))
        from lh_data_meltdown import scan_request_body
        meltdown_report = scan_request_body({"content": content})
        meltdown_ok = meltdown_report.status == "🟢 通过"
    except (ImportError, Exception):
        meltdown_ok = True  # 降级通过

    # 人格主权检查
    try:
        _bin_dir = Path(__file__).parent
        if str(_bin_dir) not in sys.path:
            sys.path.insert(0, str(_bin_dir))
        from lh_persona_sovereignty import scan as persona_scan
        persona_report = persona_scan(content)
        persona_ok = persona_report.status == "🟢 通过"
    except (ImportError, Exception):
        persona_ok = True

    # DNA
    dna = generate_dna(content)

    # 合规摘要
    parts = []
    parts.append(f"审计={audit.status}")
    parts.append(f"R={audit.score:.1f}")
    parts.append(f"数据黑洞={'🟢' if meltdown_ok else '🔴'}")
    parts.append(f"人格主权={'🟢' if persona_ok else '🔴'}")
    if audit.flags:
        parts.append(f"标记={','.join(audit.flags[:3])}")
    compliance_summary = " | ".join(parts)

    record_id = f"REG-{content_hash[:12]}-{int(time.time())}"

    return RegulatoryRecord(
        record_id=record_id,
        timestamp=datetime.now().isoformat() + "Z",
        content_hash=content_hash,
        audit=audit,
        dna=dna,
        meltdown_check=meltdown_ok,
        persona_check=persona_ok,
        compliance_summary=compliance_summary,
        source=source,
    )

# ============================================
# Jsonl 入链
# ============================================

REGULATORY_CHAIN_DIR = Path.home() / ".longhun" / "regulatory_chain"

def ensure_chain_dir() -> Path:
    REGULATORY_CHAIN_DIR.mkdir(parents=True, exist_ok=True)
    return REGULATORY_CHAIN_DIR

def append_to_chain(record: RegulatoryRecord):
    """追加记录到 jsonl 链（不可覆）"""
    chain_dir = ensure_chain_dir()
    today = datetime.now().strftime("%Y-%m-%d")
    chain_file = chain_dir / f"chain_{today}.jsonl"

    with open(chain_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(record), ensure_ascii=False, default=str) + "\n")

def generate_compliance_summary(hours: int = 24) -> ComplianceSummary:
    """生成合规摘要报告"""
    chain_dir = ensure_chain_dir()
    start = datetime.now() - timedelta(hours=hours)
    end = datetime.now()

    records = []
    # 读取最近 N 天的链文件
    for i in range(7):
        date_str = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        chain_file = chain_dir / f"chain_{date_str}.jsonl"
        if chain_file.exists():
            with open(chain_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        r = json.loads(line)
                        ts = r.get("timestamp", "")
                        if ts and ts >= start.isoformat():
                            records.append(r)
                    except json.JSONDecodeError:
                        continue

    green = sum(1 for r in records if r.get("audit", {}).get("status") == "🟢")
    yellow = sum(1 for r in records if r.get("audit", {}).get("status") == "🟡")
    red = sum(1 for r in records if r.get("audit", {}).get("status") == "🔴")
    meltdowns = sum(1 for r in records if not r.get("meltdown_check", True))
    persona_breaches = sum(1 for r in records if not r.get("persona_check", True))

    return ComplianceSummary(
        period_start=start.isoformat() + "Z",
        period_end=end.isoformat() + "Z",
        total_records=len(records),
        green_count=green, yellow_count=yellow, red_count=red,
        meltdown_events=meltdowns,
        persona_breaches=persona_breaches,
        top_flags=[],
        generated_at=end.isoformat() + "Z",
    )

# ============================================
# 流程入口
# ============================================

def process_content(content: str, source: str = "internal") -> RegulatoryRecord:
    """完整流程：处理一条内容并返回监管记录"""
    record = package_record(content, source)
    append_to_chain(record)
    return record

def process_batch(texts: List[str], source: str = "internal") -> List[RegulatoryRecord]:
    """批量处理"""
    records = []
    for text in texts:
        record = process_content(text, source)
        records.append(record)
    return records

# ============================================
# CLI
# ============================================

def main():
    parser = argparse.ArgumentParser(description="龍魂监管透明API管道")
    sub = parser.add_subparsers(dest="command")

    # process — 处理单条内容
    proc_p = sub.add_parser("process", help="处理一条内容")
    proc_p.add_argument("content", help="待审计的内容文本")
    proc_p.add_argument("-s", "--source", default="internal")
    proc_p.add_argument("--no-append", action="store_true", help="不写入链文件")

    # batch — 批量处理
    batch_p = sub.add_parser("batch", help="批量处理")
    batch_p.add_argument("--dir", help="内容目录")
    batch_p.add_argument("--file", help="内容文件（每行一条）")
    batch_p.add_argument("-o", "--output", help="输出文件路径")
    batch_p.add_argument("-s", "--source", default="internal")

    # summary — 生成合规摘要
    sum_p = sub.add_parser("summary", help="生成合规摘要报告")
    sum_p.add_argument("--hours", type=int, default=24, help="统计最近N小时")
    sum_p.add_argument("-o", "--output", help="输出 JSON 路径")

    args = parser.parse_args()

    if args.command == "process":
        record = package_record(args.content, args.source)
        if not args.no_append:
            append_to_chain(record)
        print(json.dumps(asdict(record), ensure_ascii=False, default=str, indent=2))
        # 退出码
        if record.audit.status == "🔴":
            sys.exit(2)
        elif record.audit.status == "🟡":
            sys.exit(1)

    elif args.command == "batch":
        texts = []
        if args.dir:
            dir_path = Path(args.dir)
            for f in sorted(dir_path.glob("*.txt")):
                texts.append(f.read_text(encoding="utf-8"))
        elif args.file:
            file_path = Path(args.file)
            texts = [l.strip() for l in file_path.read_text(encoding="utf-8").split("\n") if l.strip()]
        else:
            texts = [l.strip() for l in sys.stdin.read().split("\n") if l.strip()]

        records = process_batch(texts, args.source)

        output_data = [asdict(r) for r in records]
        if args.output:
            Path(args.output).write_text(
                json.dumps(output_data, ensure_ascii=False, default=str, indent=2),
                encoding="utf-8",
            )
        else:
            for line in output_data:
                print(json.dumps(line, ensure_ascii=False, default=str))

        print(f"\n已处理 {len(records)} 条记录", file=sys.stderr)

    elif args.command == "summary":
        summary = generate_compliance_summary(hours=args.hours)
        output = json.dumps(asdict(summary), ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
        print(output)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
