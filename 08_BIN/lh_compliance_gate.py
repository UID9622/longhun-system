#!/usr/bin/env python3
# DNA: #龍芯⚡️2026-08-30-ASI-DISTILLER-L1-COMPLIANCE-GATE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · ASI 蒸馏器 L1 合规闸 v1.0
──────────────────────────────────────────────
定位: 蒸馏前强制合规检查 —— 只放行「有主且主在龍魂」的蒸馏源。

规则（对齐 LH-ASI-DISTILLER-DESIGN-v1.0 §三）:
  - 自有/许可/公有 → 🟢 放行
  - 非白名单许可/版权作品/商业闭源 → 🔴 拒绝（L1 数据熔断）

用法:
    python3 08_BIN/lh_compliance_gate.py --source self --license ""
    python3 08_BIN/lh_compliance_gate.py --source open --license MIT --url https://...
    python3 08_BIN/lh_compliance_gate.py --source copyright --text "全文超过引用阈值"
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── 白名单许可（Apache-2.0/MIT/BSD/MulanPSL/CC-BY 系） ──
WHITELIST_LICENSES = {
    "apache-2.0", "apache2", "apache",
    "mit", "bsd", "bsd-2-clause", "bsd-3-clause",
    "mulanpsl", "mulanpsl-1.0", "mulanpsl-2.0", "mulanpsl2",
    "cc-by", "cc-by-3.0", "cc-by-4.0", "cc-by-sa",
}

# ── 自有源类型 ──
SELF_SOURCES = {"self", "own", "internal", "龍魂", "自有"}

# ── 版权引用阈值（原文占比上限） ──
MAX_QUOTE_RATIO = 0.30

# ── 版权作品特征词（命中即拒） ──
COPYRIGHT_MARKERS = [
    "版权所有", "未经授权", "禁止转载", "©", "copyright",
    "本作品受版权保护", "不得复制", "商业授权",
]

AUDIT_LOG = Path("audit") / "distill_compliance_audit.jsonl"


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _norm_license(lic: str) -> str:
    return re.sub(r"[\s_\-\.]+", "-", (lic or "").strip().lower())


def _quote_ratio(text: str, sample_len: int = 2000) -> float:
    """估算文本中疑似原文引用的占比（启发式：引号块 + 版权标记行）。"""
    if not text:
        return 0.0
    quoted = 0
    # 中文引号对
    quoted += len(re.findall(r"「[^」]*」", text))
    quoted += len(re.findall(r"“[^”]*”", text)) * 2
    # 代码引用块
    quoted += len(re.findall(r"(?m)^(?:>|\s{4}).+", text))
    total_chars = max(len(text), 1)
    return min(1.0, quoted * 20.0 / total_chars)


def compliance_check(
    source: str = "self",
    license: str = "",
    url: str = "",
    text: str = "",
    title: str = "",
) -> dict:
    """核心合规判定。返回含 verdict/color/理由/evidence 的字典。"""
    src = (source or "").strip().lower()
    lic = _norm_license(license)

    evidence = {
        "source": src,
        "license": lic or "none",
        "url": url or "",
        "title": title or "",
        "ts": _now_utc(),
    }

    # 1. 自有源 → 直接放行
    if src in {s.lower() for s in SELF_SOURCES} or src in {"self", "own"}:
        return {
            "verdict": "pass", "color": "🟢", "reason": "自有源·直接放行",
            "evidence": evidence,
        }

    # 2. 版权标记检查（对非自有源）
    if text:
        low = text.lower()
        hits = [m for m in COPYRIGHT_MARKERS if m.lower() in low]
        if hits:
            return {
                "verdict": "reject", "color": "🔴",
                "reason": f"命中版权标记: {hits[:3]} · L1 数据熔断",
                "evidence": evidence,
            }

    # 3. 许可白名单
    if lic in WHITELIST_LICENSES:
        qr = _quote_ratio(text)
        if qr > MAX_QUOTE_RATIO:
            return {
                "verdict": "reject", "color": "🔴",
                "reason": f"引用占比 {qr:.0%} > 阈值 30% · 退回改写",
                "evidence": evidence,
            }
        return {
            "verdict": "pass", "color": "🟢",
            "reason": f"许可 {license} 在白名单 · 引用占比 {qr:.0%} 合规",
            "evidence": evidence,
        }

    # 4. 公有领域/政府公开数据
    if src in {"public", "public-domain", "gov", "government", "公有", "公有领域"}:
        return {
            "verdict": "pass", "color": "🟢", "reason": "公有领域/政府公开数据",
            "evidence": evidence,
        }

    # 5. 未知 → 拒绝（宁可错杀）
    return {
        "verdict": "reject", "color": "🔴",
        "reason": f"未知源类型 '{source}' 且无白名单许可 · 拒绝（缺 license）",
        "evidence": evidence,
    }


def _log(entry: dict) -> None:
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry["_id"] = hashlib.sha256(
        json.dumps(entry.get("evidence", {}), ensure_ascii=False).encode()
    ).hexdigest()[:16]
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main() -> None:
    p = argparse.ArgumentParser(prog="lh_compliance_gate", description="ASI 蒸馏器 L1 合规闸 v1.0")
    p.add_argument("--source", default="self", help="源类型: self/open/public/copyright")
    p.add_argument("--license", default="", help="许可标识, 如 MIT/Apache-2.0/MulanPSL-2.0")
    p.add_argument("--url", default="", help="来源链接")
    p.add_argument("--title", default="", help="素材标题")
    p.add_argument("--text", default="", help="待蒸馏文本（用于引用占比/版权检测）")
    p.add_argument("--no-log", action="store_true", help="不写审计日志")
    args = p.parse_args()

    result = compliance_check(
        source=args.source, license=args.license,
        url=args.url, text=args.text, title=args.title,
    )
    print(f"{result['color']} 蒸馏合规判定: {result['reason']}")
    print(json.dumps(result["evidence"], ensure_ascii=False, indent=2))
    if not args.no_log:
        _log(result)
        print(f"📄 已写入审计日志: {AUDIT_LOG}")


if __name__ == "__main__":
    main()
