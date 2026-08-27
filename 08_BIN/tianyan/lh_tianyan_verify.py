# DNA: #龍芯⚡️丙午·丙申·戊辰·丙辰·䷸巽为风-CODE-补DNA-edc277b9
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 天眼交接核验器 v1.0（国家交接级 · 独立离线校验）
DNA: [[GENERATED_BY_LH_DNA_GENERATOR_V3]]-TIANYAN-VERIFY-v1.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

用途（交接给国家/第三方审计时使用）：
  1. --ops <tianyan_admin_ops.jsonl>  校验操作审计哈希链完整性
     · 复算每条 SHA-256，逐条核对 prev_hash 衔接
     · 任何一条被增删改 → 报断链位置
  2. --export <tianyan-export-*.json>  校验导出包完整性
     · 重新计算 integrity_sha256 与包内声明比对
     · 展示导出人/角色/范围/归属地（元数据摘要）

不依赖引擎运行、不联网、只读，国家审计人员可直接执行。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def chain_verify(ops_path: Path) -> Dict:
    """校验操作审计哈希链。返回 {valid, total, legacy, broken_at, checked, error}。

    国家交接级：
      · legacy = 升级前封存记录（无 hash 字段）→ 不参与链校验，保留留档
      · 链从第一条带 hash 的记录起算（GENESIS 起链）
      · 任何一条被增删改 → 断链 → broken_at 指出位置
    """
    result: Dict = {"valid": False, "total": 0, "legacy": 0, "broken_at": None,
                    "checked": 0, "error": ""}
    if not ops_path.exists():
        result["error"] = f"审计日志不存在: {ops_path}"
        return result
    prev = "GENESIS"
    total = 0
    legacy = 0
    broken = None
    try:
        with open(ops_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError as e:
                    broken = total + 1
                    result["error"] = f"第{total+1}条 JSON 损坏: {e}"
                    break
                total += 1
                expected = str(entry.get("hash", ""))
                if not expected:
                    # 升级前封存记录：不参与链校验
                    legacy += 1
                    continue
                core = {k: v for k, v in entry.items() if k != "hash"}
                body = json.dumps(core, ensure_ascii=False, sort_keys=True)
                calc = hashlib.sha256(body.encode("utf-8")).hexdigest()
                if calc != expected or str(entry.get("prev_hash", "")) != prev:
                    broken = total
                    break
                prev = expected
    except Exception as e:  # noqa: BLE001
        result["error"] = str(e)
        result["total"] = total
        result["legacy"] = legacy
        result["checked"] = total
        return result
    result["valid"] = broken is None
    result["total"] = total
    result["legacy"] = legacy
    result["broken_at"] = broken
    result["checked"] = (total - legacy) if broken is None else (broken - legacy)
    return result


def export_verify(export_path: Path) -> Dict:
    """校验导出包完整性。返回 {valid, meta, declared_hash, calc_hash}。"""
    result: Dict = {"valid": False, "error": ""}
    if not export_path.exists():
        result["error"] = f"导出文件不存在: {export_path}"
        return result
    try:
        payload = json.loads(export_path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        result["error"] = f"导出文件解析失败: {e}"
        return result
    declared = payload.get("integrity_sha256", "")
    src = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    calc = hashlib.sha256(src.encode("utf-8")).hexdigest()
    result["valid"] = declared == calc
    result["declared_hash"] = declared
    result["calc_hash"] = calc
    result["meta"] = {
        "导出人账号": payload.get("exported_by", ""),
        "负责人": payload.get("exported_name", ""),
        "角色": payload.get("exported_role_name", payload.get("exported_role", "")),
        "导出范围": payload.get("scope", ""),
        "导出时间": payload.get("ts", ""),
        "操作IP": payload.get("ip", ""),
        "IP归属地": "·".join(str(v) for v in payload.get("ip_geo", {}).values()),
        "引擎版本": payload.get("engine_version", ""),
    }
    return result


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(
        prog="lh_tianyan_verify",
        description="🐉 龍魂天眼交接核验器（独立离线·只读·可交接）")
    p.add_argument("--ops", type=Path, metavar="FILE",
                   help="操作审计日志 tianyan_admin_ops.jsonl（校验哈希链）")
    p.add_argument("--export", type=Path, metavar="FILE",
                   help="导出包 tianyan-export-*.json（校验完整性）")
    p.add_argument("--version", action="store_true", help="显示版本")
    args = p.parse_args(argv)

    if args.version:
        print(f"🐉 龍魂天眼交接核验器 v1.0")
        print(f"确认码: {CONFIRM_CODE}")
        print(f"GPG: {GPG_FINGERPRINT}")
        return 0

    ok_all = True
    if args.ops:
        r = chain_verify(args.ops)
        print("══════ 操作审计哈希链核验 ══════")
        print(f"  文件: {args.ops}")
        print(f"  条目: {r['total']} 条")
        if r.get("legacy"):
            print(f"  🗂 封存段: {r['legacy']} 条（升级前记录·留档·不参与链校验）")
        if r["valid"]:
            print(f"  ✅ 校验通过：{r['checked']} 条哈希链完整衔接")
        else:
            ok_all = False
            print(f"  ❌ 校验失败：第 {r['broken_at']} 条断链")
            if r["error"]:
                print(f"  原因: {r['error']}")
        print()
    if args.export:
        r = export_verify(args.export)
        print("══════ 导出包完整性核验 ══════")
        print(f"  文件: {args.export}")
        if r.get("error"):
            ok_all = False
            print(f"  ❌ {r['error']}")
        else:
            for k, v in r["meta"].items():
                print(f"  {k}: {v}")
            print(f"  声明摘要: {r['declared_hash']}")
            print(f"  实算摘要: {r['calc_hash']}")
            if r["valid"]:
                print(f"  ✅ 完整性校验通过：内容与摘要一致，未被改动")
            else:
                ok_all = False
                print(f"  ❌ 完整性校验失败：内容与声明摘要不符，疑似被改动")
        print()
    if not args.ops and not args.export:
        p.print_help()
        return 1
    print("────────────────────────────")
    print(f"总判定: {'✅ 全绿 · 可交接' if ok_all else '❌ 存在异常 · 需人工复核'}")
    print(f"核验人: 国家/第三方审计（独立离线·数据不出境）")
    return 0 if ok_all else 2


if __name__ == "__main__":
    sys.exit(main())
