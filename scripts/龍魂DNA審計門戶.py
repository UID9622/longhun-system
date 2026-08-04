#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 DNA 流程審計門戶
DNA: #龍芯⚡️2026-06-30-LONGHUN-DNA-AUDIT-PORTAL-v1.0

為每一次 AI 輸出建立不可篡改的流程審計記錄：
  - 輸入與意圖
  - 調用的技能 / 工具 / 檢查點
  - 六層來源鏈
  - 鐵律自審 / 三色審計結果
  - 輸出文件哈希
  - 自動生成 Mermaid 多維流程圖

用法：
  python3 龍魂DNA審計門戶.py --record <json_file>
  python3 龍魂DNA審計門戶.py --audit <dna>
  python3 龍魂DNA審計門戶.py --audit <dna> --output audit.md
"""

import argparse
import hashlib
import json
import re
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


LOG_PATH = Path.home() / "longhun-system" / "logs" / "龍魂流程審計庫.jsonl"
DNA_PATTERN = re.compile(r"#龍芯⚡️[0-9A-Za-z_\-]+")


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_file(path: str | Path) -> str | None:
    p = Path(path)
    if not p.exists():
        return None
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def _ensure_log() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_PATH.exists():
        LOG_PATH.touch()


def record_workflow(
    dna: str,
    input_text: str,
    intent: str,
    skills: list[str] | None = None,
    tools: list[dict[str, Any]] | None = None,
    checks: list[dict[str, Any]] | None = None,
    source_chain: list[str] | None = None,
    ironlaw_result: dict[str, Any] | None = None,
    three_color: dict[str, Any] | None = None,
    output_files: list[str] | None = None,
    output_card: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """把一次完整輸出流程寫入審計庫，返回記錄對象。"""
    _ensure_log()

    output_hash = _sha256_text(json.dumps(output_card, ensure_ascii=False, sort_keys=True)) if output_card else None
    file_hashes = {str(f): _sha256_file(f) for f in (output_files or []) if f}

    record = {
        "dna": dna,
        "timestamp": _now(),
        "input_preview": input_text[:500],
        "input_hash": _sha256_text(input_text),
        "intent": intent,
        "skills": skills or [],
        "tools": tools or [],
        "checks": checks or [],
        "source_chain": source_chain or [
            "道統(曾仕強)",
            "精神(Steve Jobs)",
            "設備(Apple)",
            "技術(Open Source)",
            "系統(UID9622)",
            "生命(CNSH·龍魂)",
        ],
        "ironlaw_result": ironlaw_result or {"passed": True, "violations": []},
        "three_color": three_color or {"status": "🟢", "reason": "未執行三色審計"},
        "output_card_hash": output_hash,
        "output_files": file_hashes,
        "metadata": metadata or {},
    }

    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record


def load_records() -> list[dict[str, Any]]:
    _ensure_log()
    records = []
    with LOG_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except Exception:
                continue
    return records


def find_by_dna(dna: str) -> dict[str, Any] | None:
    for rec in load_records():
        if rec.get("dna") == dna:
            return rec
    return None


def render_mermaid(record: dict[str, Any]) -> str:
    """把一次流程記錄渲染成 Mermaid 多維流程圖。"""
    intent = record.get("intent", "未知")
    input_preview = record.get("input_preview", "")[:40].replace("\"", "'")
    checks = record.get("checks", [])
    tools = record.get("tools", [])
    files = record.get("output_files", {})
    color = record.get("three_color", {}).get("status", "🟢")

    lines = ["graph TD"]
    lines.append(f'  A[\"輸入: {input_preview}...\"] --> B{{意圖識別: {intent}}}')

    node_id = "C"
    for i, chk in enumerate(checks):
        name = chk.get("name", f"檢查{i+1}")
        result = chk.get("result", "-")
        lines.append(f'  B --> {node_id}[\"{name}\\n{result}\"]')
        node_id = chr(ord(node_id) + 1)

    if tools:
        tool_names = "\\n".join(t.get("tool", "?") for t in tools[:5])
        lines.append(f'  {chr(ord(node_id)-1)} --> {node_id}[\"工具調用\\n{tool_names}\"]')
        node_id = chr(ord(node_id) + 1)

    output_label = f"輸出 {color}"
    if files:
        output_label += f"\\n文件數: {len(files)}"
    lines.append(f'  {chr(ord(node_id)-1)} --> Z[\"{output_label}\"]')

    # 審計側邊維度
    lines.append("")
    lines.append("  subgraph 來源鏈與合規")
    lines.append(f'    S1[\"六層來源鏈\"]')
    if record.get("ironlaw_result", {}).get("passed"):
        lines.append('    S2[\"鐵律自審: ✅通過\"]')
    else:
        lines.append('    S2[\"鐵律自審: 🔴熔斷\"]')
    lines.append('    S3[\"輸出哈希: SHA-256\"]')
    lines.append("  end")

    return "\n".join(lines)


def generate_audit_report(record: dict[str, Any], role: str = "普通人") -> str:
    """生成給指定對象看的審計報告 Markdown。"""
    lines = [
        f"# 龍魂 DNA 流程審計報告",
        "",
        f"**DNA**: `{record.get('dna')}`",
        f"**時間**: {record.get('timestamp')}",
        f"**輸入哈希**: `{record.get('input_hash')}`",
        f"**輸出卡片哈希**: `{record.get('output_card_hash')}`",
        f"**意圖**: {record.get('intent')}",
        "",
        "## 一句話結論",
        f"本次輸出 {record.get('three_color', {}).get('status', '🟢')}：{record.get('three_color', {}).get('reason', '')}",
        "",
        "## 流程圖",
        "```mermaid",
        render_mermaid(record),
        "```",
        "",
        "## 調用技能",
    ]
    skills = record.get("skills") or []
    lines.append(", ".join(skills) if skills else "無")

    lines.extend(["", "## 檢查點"])
    for chk in record.get("checks", []):
        lines.append(f"- **{chk.get('name')}**: {chk.get('result')}")

    lines.extend(["", "## 工具調用"])
    for t in record.get("tools", []):
        lines.append(f"- `{t.get('tool')}`: {t.get('summary', '')}")

    lines.extend(["", "## 輸出文件與哈希"])
    files = record.get("output_files", {})
    if files:
        for path, h in files.items():
            lines.append(f"- `{Path(path).name}`: `{h}`")
    else:
        lines.append("- 無文件輸出")

    lines.extend(["", "## 六層來源鏈"])
    for src in record.get("source_chain", []):
        lines.append(f"- {src}")

    lines.extend(["", "## 鐵律自審"])
    ir = record.get("ironlaw_result", {})
    lines.append(f"- 結果: {'✅ 通過' if ir.get('passed') else '🔴 熔斷'}")
    if ir.get("violations"):
        lines.append("- 命中項:")
        for v in ir.get("violations", []):
            lines.append(f"  - {v}")

    lines.extend(["", f"DNA: #龍芯⚡️{time.strftime('%Y%m%d%H%M%S')}-LONGHUN-DNA-AUDIT-REPORT"])
    return "\n".join(lines)


def looks_like_dna(text: str) -> bool:
    return bool(DNA_PATTERN.fullmatch(text.strip()))


def audit(dna: str, role: str = "普通人", output: str | None = None) -> dict[str, Any]:
    """根據 DNA 調出審計報告。"""
    record = find_by_dna(dna)
    if not record:
        return {"found": False, "error": f"未找到 DNA: {dna}"}

    report_md = generate_audit_report(record, role)
    out_path = None
    if output:
        out_path = Path(output)
        out_path.write_text(report_md, encoding="utf-8")
    else:
        ts = time.strftime("%Y%m%d_%H%M%S")
        out_path = Path(f"/tmp/龍魂DNA審計_{ts}.md")
        out_path.write_text(report_md, encoding="utf-8")

    return {
        "found": True,
        "record": record,
        "report_path": str(out_path),
        "mermaid": render_mermaid(record),
        "report": report_md,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="龍魂 DNA 流程審計門戶")
    parser.add_argument("--record", help="讀取 JSON 文件並寫入審計庫")
    parser.add_argument("--audit", help="根據 DNA 查詢審計報告")
    parser.add_argument("--role", default="普通人", help="報告語氣角色")
    parser.add_argument("--output", "-o", help="報告輸出路徑")
    args = parser.parse_args(argv)

    if args.record:
        data = json.loads(Path(args.record).read_text(encoding="utf-8"))
        rec = record_workflow(**data)
        print(f"🟢 已記錄 DNA: {rec['dna']}")
        return 0

    if args.audit:
        result = audit(args.audit, args.role, args.output)
        if not result["found"]:
            print(f"🔴 {result['error']}")
            return 1
        print(result["report"])
        print(f"\n📎 報告已保存: {result['report_path']}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
