#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·壬戌·亥时·䷬萃-AUDIT-BACKLOG-CLASSIFIER-v1.0-UID9622-2970C690
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂 · 审计积压批量归类脚本 v1.0

功能:
  1. 扫描 07_AUDIT/ 下所有待审审计日志
  2. 按 DNA/CONFIRM/内容规则自动分类
  3. 按风险等级分桶 (🔴/🟡/🟢)
  4. 自动标记可批量处理的 🟢 记录
  5. 导出待人工复核 CSV 清单
  6. 生成 JSON + Markdown 汇总报告

用法:
  python3 08_BIN/lh_audit_backlog_classifier.py
  python3 08_BIN/lh_audit_backlog_classifier.py --dry-run
  python3 08_BIN/lh_audit_backlog_classifier.py --auto-green
  python3 08_BIN/lh_audit_backlog_classifier.py --export-csv
  python3 08_BIN/lh_audit_backlog_classifier.py --selftest

流程图:
```mermaid
flowchart TD
    A["📂 扫描审计日志<br/>JSON/JSONL/LOG"] --> B["🔍 自动分类<br/>DNA/CONFIRM/内容规则"]
    B --> C{"风险等级<br/>🔴/🟡/🟢"}
    C -->|🟢 自动处理| D["✅ 标记已处理"]
    C -->|🟡 待复核| E["📋 导出CSV清单"]
    C -->|🔴 紧急| F["🚨 优先处理队列"]
    D --> G["📊 生成报告<br/>JSON+Markdown+CSV"]
    E --> G
    F --> G
```

协议: CC BY-NC-SA 4.0 (思想层) · MulanPSL v2 (工程层)

完整文档: 01_protocols/LH-AUDIT-BACKLOG-CLASSIFIER-v1.0.md
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

# 让导入能找到 core.longhun_core.dna_trace
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.longhun_core.dna_trace import generate_dna

# ═══════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT_DIR = PROJECT_ROOT / "07_AUDIT"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "07_AUDIT" / "reports"
CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# DNA 格式正则（新格式：#龍芯⚡️天干地支·...-模块-动作-哈希8）
DNA_NEW_RE = re.compile(r'#龍芯⚡️[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]·.*-.*-.*-[0-9A-F]{8}')
DNA_ANY_RE = re.compile(r'#龍芯⚡️\S+')
DNA_OLD_DATE_RE = re.compile(r'#龍芯⚡️\d{8}')
DNA_OLD_ISO_RE = re.compile(r'#龍芯⚡️\d{4}-\d{2}-\d{2}')


# ═══════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════
@dataclass
class AuditRecord:
    id: str
    timestamp: str
    dna: str
    content: str
    source: str
    status: str
    violation_type: str = ""
    severity: str = "🟡"
    auto_fix: bool = False
    batch_key: str = ""
    human_review_needed: bool = True
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ═══════════════════════════════════════════════════════
# 违规类型规则
# ═══════════════════════════════════════════════════════
CONTENT_RULES = [
    {
        "key": "duplicate",
        "name": "重复记录",
        "patterns": [r"\bDUPLICATE\b", r"重复记录", r"duplicate_record"],
        "severity": "🟢",
        "auto_fix": True,
        "description": "重复的审计记录，可去重",
    },
    {
        "key": "expired",
        "name": "过期记录",
        "patterns": [r"\bEXPIRED\b", r"过期记录", r"expired_record"],
        "severity": "🟢",
        "auto_fix": True,
        "description": "已过期无需处理的记录",
    },
    {
        "key": "timestamp_invalid",
        "name": "时间戳异常",
        "patterns": [r"时间戳.*?异常", r"timestamp.*?invalid", r"timestamp.*?tampered"],
        "severity": "🔴",
        "auto_fix": False,
        "description": "时间戳存在篡改或异常",
    },
    {
        "key": "broken_chain",
        "name": "来源链断裂",
        "patterns": [r"来源链.*?断裂", r"chain.*?broken", r"provenance.*?fail"],
        "severity": "🔴",
        "auto_fix": False,
        "description": "来源链完整性校验失败",
    },
    {
        "key": "sig_invalid",
        "name": "行为签名异常",
        "patterns": [r"行为签名.*?异常", r"behavior.*?proof.*?fail", r"signature.*?invalid"],
        "severity": "🔴",
        "auto_fix": False,
        "description": "行为密码学签名校验失败",
    },
    {
        "key": "old_protocol",
        "name": "旧版协议",
        "patterns": [r"旧版协议", r"legacy_protocol", r"protocol_v1\.[0-3]"],
        "severity": "🟡",
        "auto_fix": False,
        "description": "基于旧版本协议的记录，需要迁移",
    },
]


def classify_record(content: str, dna: str) -> Tuple[str, str, bool, str]:
    """
    对单条记录进行分类。
    返回: (违规类型, 严重程度, 是否自动修复, batch_key)
    """
    has_dna = bool(dna)
    has_confirm = CONFIRM_MARK in content

    # 🔴 缺少 DNA（最基础）
    if not has_dna:
        return "缺少DNA", "🔴", False, "missing_dna"

    # 🔴 缺少确认码
    if not has_confirm:
        return "缺少确认码", "🔴", False, "missing_confirm"

    # 内容关键词规则（业务状态优先于 DNA 格式瑕疵）
    for rule in CONTENT_RULES:
        for pat in rule["patterns"]:
            if re.search(pat, content, re.IGNORECASE):
                return rule["name"], rule["severity"], rule["auto_fix"], rule["key"]

    # 🟡 旧时间戳格式：YYYYMMDD 或 YYYY-MM-DD（无干支）
    if DNA_OLD_DATE_RE.search(dna) or DNA_OLD_ISO_RE.search(dna):
        return "旧时间戳格式", "🟡", False, "timestamp_old"

    # 🟡 手写干支或格式不规范
    if not DNA_NEW_RE.search(dna):
        return "手写干支或格式不规范", "🟡", False, "ganzhi_manual"

    # 🟢 正常记录
    return "正常", "🟢", True, "clean"


# ═══════════════════════════════════════════════════════
# 主处理器
# ═══════════════════════════════════════════════════════
class AuditBacklogClassifier:
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.records: List[AuditRecord] = []
        self.stats = {
            "total_scanned": 0,
            "pending": 0,
            "already_resolved": 0,
            "by_severity": Counter(),
            "by_violation_type": Counter(),
            "by_batch_key": Counter(),
            "auto_resolvable": 0,
            "human_review_needed": 0,
        }
        self.dna = generate_dna("AUDIT-BACKLOG-CLASSIFIER", "UID9622")

    def scan(self) -> int:
        if not self.input_dir.exists():
            print(f"❌ 输入目录不存在: {self.input_dir}", file=sys.stderr)
            return 0

        files = []
        for ext in ["*.json", "*.jsonl", "*.log"]:
            files.extend(self.input_dir.rglob(ext))

        # 排除报告输出目录、签名文件、stdout 捕获日志（非结构化审计记录）
        files = [
            f for f in files
            if "reports" not in f.parts
            and not f.name.endswith(".asc")
            and not f.name.endswith(".stdout.log")
        ]

        if not files:
            print(f"⚠️ 未找到审计日志文件: {self.input_dir}", file=sys.stderr)
            return 0

        print(f"📂 扫描 {len(files)} 个文件...")
        for file_path in files:
            try:
                self._process_file(file_path)
            except Exception as e:
                print(f"  ⚠️ 读取 {file_path} 失败: {e}", file=sys.stderr)

        self.stats["pending"] = len(self.records)
        print(f"✅ 扫描完成: {self.stats['total_scanned']} 条记录，待审 {self.stats['pending']} 条")
        return self.stats["pending"]

    def _process_file(self, file_path: Path):
        if file_path.suffix == ".json":
            data = json.loads(file_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                for item in data:
                    self._process_item(item, file_path)
            elif isinstance(data, dict):
                self._process_item(data, file_path)
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        item = json.loads(line)
                        self._process_item(item, file_path)
                    except json.JSONDecodeError:
                        self._process_text_line(line, file_path)

    def _process_item(self, item: Dict[str, Any], file_path: Path):
        self.stats["total_scanned"] += 1
        status = item.get("status", item.get("state", "pending"))
        if status not in ("pending", "待审", "open"):
            self.stats["already_resolved"] += 1
            return

        content = json.dumps(item, ensure_ascii=False)
        dna = item.get("dna", item.get("DNA", ""))
        timestamp = item.get("timestamp", item.get("ts", item.get("time", "")))
        record_id = item.get("id", item.get("ID", hashlib.md5(content.encode()).hexdigest()[:12]))

        violation_type, severity, auto_fix, batch_key = classify_record(content, dna)

        record = AuditRecord(
            id=f"{file_path.stem}-{record_id}",
            timestamp=timestamp,
            dna=dna,
            content=content[:400],
            source=str(file_path.relative_to(PROJECT_ROOT)),
            status=status,
            violation_type=violation_type,
            severity=severity,
            auto_fix=auto_fix,
            batch_key=batch_key,
            human_review_needed=not auto_fix,
        )
        self._add_record(record)

    def _process_text_line(self, line: str, file_path: Path):
        self.stats["total_scanned"] += 1
        dna_match = DNA_ANY_RE.search(line)
        dna = dna_match.group(0) if dna_match else ""
        violation_type, severity, auto_fix, batch_key = classify_record(line, dna)

        record = AuditRecord(
            id=f"{file_path.stem}-{hashlib.md5(line.encode()).hexdigest()[:12]}",
            timestamp=datetime.now().isoformat(),
            dna=dna,
            content=line[:400],
            source=str(file_path.relative_to(PROJECT_ROOT)),
            status="pending",
            violation_type=violation_type,
            severity=severity,
            auto_fix=auto_fix,
            batch_key=batch_key,
            human_review_needed=not auto_fix,
        )
        self._add_record(record)

    def _add_record(self, record: AuditRecord):
        self.records.append(record)
        self.stats["by_severity"][record.severity] += 1
        self.stats["by_violation_type"][record.violation_type] += 1
        self.stats["by_batch_key"][record.batch_key] += 1
        if record.auto_fix:
            self.stats["auto_resolvable"] += 1
        else:
            self.stats["human_review_needed"] += 1

    def auto_resolve_green(self, dry_run: bool = False) -> int:
        count = 0
        for record in self.records:
            if record.severity == "🟢" and record.auto_fix and record.violation_type == "正常":
                if not dry_run:
                    record.status = "resolved"
                    record.notes = "自动标记已处理 (批量归类)"
                count += 1
        action = "将自动标记" if dry_run else "已自动标记"
        print(f"✅ {action} {count} 条🟢记录为已处理")
        return count

    def export_human_review_csv(self, output_path: Path, dry_run: bool = False) -> int:
        human_records = [r for r in self.records if r.human_review_needed]
        if not human_records:
            print("🎉 没有需要人工复核的记录")
            return 0

        if dry_run:
            print(f"[dry-run] 将导出 {len(human_records)} 条待复核记录到: {output_path}")
            return len(human_records)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "时间戳", "严重程度", "违规类型", "批次Key", "DNA(前40字符)", "来源文件", "备注"])
            for r in human_records:
                writer.writerow([
                    r.id,
                    r.timestamp[:19] if r.timestamp else "",
                    r.severity,
                    r.violation_type,
                    r.batch_key,
                    r.dna[:40] if r.dna else "",
                    r.source,
                    r.notes or "",
                ])
        print(f"📤 导出 {len(human_records)} 条待复核记录到: {output_path}")
        return len(human_records)

    def generate_report(self) -> Dict[str, Any]:
        report = {
            "dna": self.dna,
            "confirm": CONFIRM_MARK,
            "generated_at": datetime.now().isoformat(),
            "input_dir": str(self.input_dir),
            "summary": {
                "total_scanned": self.stats["total_scanned"],
                "pending": self.stats["pending"],
                "already_resolved": self.stats["already_resolved"],
                "by_severity": dict(self.stats["by_severity"]),
                "by_violation_type": dict(self.stats["by_violation_type"]),
                "by_batch_key": dict(self.stats["by_batch_key"]),
                "auto_resolvable": self.stats["auto_resolvable"],
                "human_review_needed": self.stats["human_review_needed"],
            },
            "records": [r.to_dict() for r in self.records],
        }
        return report

    def export_json_report(self, output_path: Path, dry_run: bool = False) -> Path:
        report = self.generate_report()
        if dry_run:
            print(f"[dry-run] 将生成 JSON 报告: {output_path}")
            return output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"📄 JSON报告: {output_path}")
        return output_path

    def export_markdown_report(self, output_path: Path, dry_run: bool = False) -> Path:
        s = self.stats
        md = f"""# 🐉 龍魂 · 审计积压分类报告

**DNA:** `{self.dna}`  
**确认码:** `{CONFIRM_MARK}`  
**生成时间:** {datetime.now().isoformat()}  
**输入目录:** `{self.input_dir}`

---

## 📊 总览

| 指标 | 数量 |
|:---|---:|
| 扫描记录总数 | **{s['total_scanned']}** |
| 待审记录 | **{s['pending']}** |
| 已自动/已处理 | **{s['already_resolved']}** |
| 🔴 严重违规 | **{s['by_severity'].get('🔴', 0)}** |
| 🟡 待人工复核 | **{s['by_severity'].get('🟡', 0)}** |
| 🟢 可自动处理 | **{s['auto_resolvable']}** |

---

## 🔍 按违规类型分布

| 违规类型 | 数量 | 严重程度 |
|:---|---:|:---:|
"""
        for vtype, count in s["by_violation_type"].most_common():
            sev = "🔴" if vtype in ("缺少DNA", "缺少确认码", "时间戳异常", "来源链断裂", "行为签名异常") else "🟡"
            if vtype in ("正常", "重复记录", "过期记录"):
                sev = "🟢"
            md += f"| {vtype} | {count} | {sev} |\n"

        md += f"""
---

## 📂 按批次分桶

| 批次Key | 数量 |
|:---|---:|
"""
        for key, count in s["by_batch_key"].most_common():
            md += f"| {key} | {count} |\n"

        md += f"""
---

## 🎯 下一步建议

1. **🟢 自动处理**: {s['auto_resolvable']} 条可批量标记为已处理
2. **🟡 人工复核**: {s['by_severity'].get('🟡', 0)} 条需要人工审查
3. **🔴 紧急处理**: {s['by_severity'].get('🔴', 0)} 条需要立即处理

---

## 🚀 常用命令

```bash
# 干跑（不修改数据）
python3 08_BIN/lh_audit_backlog_classifier.py --dry-run

# 自动标记绿色记录
python3 08_BIN/lh_audit_backlog_classifier.py --auto-green

# 导出待复核清单
python3 08_BIN/lh_audit_backlog_classifier.py --export-csv
```

---

**DNA:** `{self.dna}`  
**确认码:** `{CONFIRM_MARK}`
"""
        if dry_run:
            print(f"[dry-run] 将生成 Markdown 报告: {output_path}")
            return output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(md, encoding="utf-8")
        print(f"📄 Markdown报告: {output_path}")
        return output_path

    def print_summary(self):
        s = self.stats
        print("\n" + "=" * 70)
        print("🐉 审计积压分类报告")
        print("=" * 70)
        print(f"DNA: {self.dna}")
        print(f"确认码: {CONFIRM_MARK}")
        print("-" * 70)
        print(f"扫描记录总数: {s['total_scanned']}")
        print(f"  待审: {s['pending']}")
        print(f"  已处理: {s['already_resolved']}")
        print(f"  🔴 严重: {s['by_severity'].get('🔴', 0)}")
        print(f"  🟡 待审: {s['by_severity'].get('🟡', 0)}")
        print(f"  🟢 自动可处理: {s['auto_resolvable']}")
        print("-" * 70)
        print("按违规类型分布:")
        for vtype, count in s["by_violation_type"].most_common():
            print(f"  {vtype}: {count}")
        print("=" * 70)


def selftest() -> bool:
    """自检：验证分类规则"""
    confirm = CONFIRM_MARK
    cases = [
        # 正常记录：新格式 DNA + CONFIRM
        (f"{{'dna':'#龍芯⚡️丙午·丙申·丁巳·恒卦-TEST-UID9622-A1B2C3D4','confirm':'{confirm}','status':'pending'}}", "正常", "🟢"),
        # 缺少 DNA
        ("{'status':'pending'}", "缺少DNA", "🔴"),
        # 旧时间戳格式：有 DNA 但无 CONFIRM → 优先报缺少确认码
        ("{'dna':'#龍芯⚡️20260811-OLD-UID9622','status':'pending'}", "缺少确认码", "🔴"),
        # 手写干支或格式不规范 + CONFIRM
        (f"{{'dna':'#龍芯⚡️foo-bar','confirm':'{confirm}','status':'pending'}}", "手写干支或格式不规范", "🟡"),
        # 重复记录 + CONFIRM
        (f"{{'dna':'#龍芯⚡️丙午·丙申·丁巳·恒卦-TEST-A1B2C3D4','confirm':'{confirm}','status':'pending','note':'DUPLICATE'}}", "重复记录", "🟢"),
    ]
    all_ok = True
    for content, expected_type, expected_sev in cases:
        dna_match = DNA_ANY_RE.search(content)
        dna = dna_match.group(0) if dna_match else ""
        vtype, sev, _, _ = classify_record(content, dna)
        ok = vtype == expected_type and sev == expected_sev
        icon = "🟢" if ok else "🔴"
        print(f"{icon} {expected_type}: got [{sev}] {vtype}")
        if not ok:
            all_ok = False
    return all_ok


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 审计积压批量归类脚本")
    parser.add_argument("--input", "-i", type=str, default=str(DEFAULT_INPUT_DIR),
                        help=f"审计日志目录 (默认: {DEFAULT_INPUT_DIR})")
    parser.add_argument("--output-dir", "-o", type=str, default=str(DEFAULT_OUTPUT_DIR),
                        help=f"报告输出目录 (默认: {DEFAULT_OUTPUT_DIR})")
    parser.add_argument("--report", "-r", action="store_true",
                        help="只生成报告，不修改记录")
    parser.add_argument("--auto-green", "-g", action="store_true",
                        help="自动标记🟢级记录为已处理")
    parser.add_argument("--export-csv", "-e", action="store_true",
                        help="导出待人工复核CSV清单")
    parser.add_argument("--dry-run", "-d", action="store_true",
                        help="干跑模式：不修改任何文件")
    parser.add_argument("--selftest", action="store_true",
                        help="运行自检")
    args = parser.parse_args()

    if args.selftest:
        ok = selftest()
        sys.exit(0 if ok else 1)

    input_dir = Path(args.input)
    output_dir = Path(args.output_dir)
    dry_run = args.dry_run or args.report

    classifier = AuditBacklogClassifier(input_dir, output_dir)
    total = classifier.scan()
    if total == 0:
        print("⚠️ 没有找到待审记录")
        return

    classifier.print_summary()

    if args.auto_green:
        classifier.auto_resolve_green(dry_run=dry_run)

    if args.export_csv or not dry_run:
        csv_path = output_dir / "human_review_list.csv"
        classifier.export_human_review_csv(csv_path, dry_run=dry_run)

    md_path = output_dir / "audit_summary.md"
    json_path = output_dir / "audit_summary.json"
    classifier.export_markdown_report(md_path, dry_run=dry_run)
    classifier.export_json_report(json_path, dry_run=dry_run)

    print(f"\n✅ 完成！输出目录: {output_dir}")
    print(f"🧬 DNA: {classifier.dna}")
    print(f"🔐 确认码: {CONFIRM_MARK}")


if __name__ == "__main__":
    main()
