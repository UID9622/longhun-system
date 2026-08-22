#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-SKILL-TRICOLOR-AUDIT-v1.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 Skill · 三色审计 + DNA 追溯执行器 v1.1
DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-SKILL-TRICOLOR-AUDIT-v1.1
创建者: 诸葛鑫（UID9622）
协议: MulanPSL v2（工程实现层）

对接真实底座（不重复造轮子）:
  - 数字根:   bin/lh_cnsh_runtime_math.py  (digital_root / dr_from_string)  [P06数学大师]
  - 三色裁决: bin/lh_three_color_audit.py  (quick_audit / audit)           [P05上帝之眼]
  - 干支DNA:  bin/lh_time_engine.py        (get_output_stamp)              [时间引擎]

双模式:
  --mode dr      数字根映射三色（绿色{1,2,4,5,7}·黄色{3,6}·红色{8,9}）·日常写入前快检
  --mode engine  完整三色引擎裁决（德本五问+加权规则+SI主权指数+十闸口）·正式审计
"""

import sys
import os
import json
import re
import argparse
import hashlib
from pathlib import Path
from datetime import datetime

# ===== 接真实底座 =====
BIN_DIR = str(Path(__file__).resolve().parent.parent.parent / "bin")
if BIN_DIR not in sys.path:
    sys.path.insert(0, BIN_DIR)

try:
    from lh_cnsh_runtime_math import digital_root, dr_from_string  # 数字根引擎
except ImportError:  # 兜底：内置实现（标🟡降级）
    def digital_root(n: int) -> int:
        if n == 0:
            return 9
        r = n % 9
        return 9 if r == 0 else r
    def dr_from_string(s: str) -> int:
        digits = [int(c) for c in s if c.isdigit()]
        if not digits:
            return 0
        return digital_root(sum(digits))

try:
    from lh_three_color_audit import quick_audit, audit as tricolor_audit  # 三色裁决引擎
    ENGINE_AVAILABLE = True
except ImportError:
    ENGINE_AVAILABLE = False

try:
    from lh_time_engine import get_output_stamp  # 干支时间引擎
    def forge_dna(module: str, version: str = "1.0") -> str:
        """干支四柱DNA（对接时间引擎·非纯日期）"""
        stamp = get_output_stamp(format_type="compact")  # #龍芯⚡️干支·卦
        h = hashlib.sha256(f"{module}{version}{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper()
        return f"{stamp}-{module.upper()}-{h}-9622"
except ImportError:
    def forge_dna(module: str, version: str = "1.0") -> str:
        """降级：日期DNA（标🟡·建议安装时间引擎）"""
        h = hashlib.sha256(f"{module}{version}{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{module.upper()}-{h}-9622"

# ===== 三色阈值（P06锚点·数字根映射）=====
THRESHOLDS = {
    "green_drs":  [1, 2, 4, 5, 7],
    "yellow_drs": [3, 6],
    "red_drs":    [8, 9],
}

# ===== 三毒识别（修正版：豁免合法免责声明·S3维权助手强制免责不误伤）=====
TOXIC_PATTERNS = [
    r"(绕过.{0,8}(校验|验证|审计)|钻空子|走.{0,4}漏洞)",
    r"(数据外送|付费墙|强制收费|广告位植入)",
    r"(代替人类决策|删除人类署名|冒充人类|AI主导决策)",
]

# ===== 合法免责声明豁免（KP-005 反例：合法免责≠漏洞免责套路）=====
SAFE_DISCLAIMERS = [
    "仅供参考",
    "免责声明",
    "不构成法律建议",
    "不作为专业意见",
]

# ===== 教学文档豁免（描述风险模式≠实施风险行为）=====
TEACHING_MARKERS = [
    "模式",
    "规则",
    "检测到风险",
    "例如",
    "示例",
    "描述",
    "KP-0",
    "正则",
    "三毒",
    "黑名单",
    "定义",
]

# ===== 套壳检测 =====
SHELL_MARKERS = ["analytics", "tracker", "conversion", "impression", "revenue", "pixel"]

def compute_content_dr(content: str) -> int:
    """内容数字根（复用真实引擎·sha256指纹→dr_from_string）"""
    h = hashlib.sha256(content.encode("utf-8")).hexdigest()
    n = int(h, 16)
    return digital_root(n)

def detect_toxicity(content: str) -> list:
    """三毒+套壳检测（豁免合法免责声明）"""
    warnings = []
    for pattern in TOXIC_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            # 豁免检查：命中行含合法免责声明 或 教学描述标记 → 跳过
            for line in content.splitlines():
                if re.search(pattern, line, re.IGNORECASE):
                    if any(d in line for d in SAFE_DISCLAIMERS):
                        continue
                    if any(m in line for m in TEACHING_MARKERS):
                        continue  # 描述风险模式的教学/规则文档·非实施
                    warnings.append(f"检测到风险模式: {pattern} (行: {line.strip()[:50]})")
    shell_hits = [m for m in SHELL_MARKERS if m.lower() in content.lower()]
    if shell_hits:
        warnings.append(f"检测到商业套壳标记: {shell_hits}")
    return list(dict.fromkeys(warnings))  # 去重

def classify_dr(dr: int, warnings: list) -> dict:
    """数字根映射三色（老大的设计·阈值已接P06锚点）"""
    color, status, action = "⚪", "UNCLASSIFIED", "unknown"
    if dr in THRESHOLDS["green_drs"]:
        color, status, action = "🟢", "PASS", "execute"
    elif dr in THRESHOLDS["yellow_drs"]:
        color, status, action = "🟡", "REVIEW", "wait_confirm"
    elif dr in THRESHOLDS["red_drs"]:
        color, status, action = "🔴", "BLOCK", "reject"
    if warnings:
        # 有警告强制降级：绿→黄·黄/绿→红
        if status in ("PASS",):
            color, status, action = "🟡", "REVIEW", "wait_confirm"
    return {"dr": dr, "color": color, "status": status, "action": action}

def audit_file(fp: Path, module: str, version: str, mode: str = "dr") -> dict:
    """审计一个文件"""
    content = fp.read_text(encoding="utf-8", errors="replace")
    dr = compute_content_dr(content)
    warnings = detect_toxicity(content)
    # 规则文档豁免：自身描述三毒模式(含 TOXIC_PATTERNS/三毒识别) → 三毒警告降为信息不降色
    if any(m in content for m in ("TOXIC_PATTERNS", "三毒识别", "风险模式清单")):
        warnings = [w for w in warnings if not w.startswith("检测到风险模式")]
    dna = forge_dna(module, version)

    if mode == "engine" and ENGINE_AVAILABLE:
        # 完整三色引擎裁决（德本+SI+十闸口·P05）
        def _enum_val(v, default="unknown"):
            """Enum→可序列化值"""
            if v is None:
                return default
            if hasattr(v, "value"):
                return v.value if not isinstance(v.value, (tuple, list)) else str(v.value)
            if hasattr(v, "名称"):
                return v.名称
            if isinstance(v, (str, int, float, bool)):
                return v
            return str(v)
        try:
            verdict = tricolor_audit(content, target_type="代码审查")
            result = {
                "dr": dr,
                "color": _enum_val(verdict.get("三色判定", verdict.get("颜色", "🟢")), "🟢"),
                "status": _enum_val(verdict.get("裁决状态", verdict.get("状态", "PASS")), "PASS"),
                "action": _enum_val(verdict.get("执行动作", "execute"), "execute"),
                "engine": verdict,
            }
        except Exception as e:
            warnings.append(f"引擎裁决失败(降级dr模式): {e}")
            result = classify_dr(dr, warnings)
            result["engine"] = None
    else:
        result = classify_dr(dr, warnings)

    result.update({"dna": dna, "warnings": warnings, "mode": mode})
    return result

def write_audit_log(entry: dict):
    """append-only 审计日志（对齐现有 ~/.longhun/audit/）"""
    log_file = Path.home() / ".longhun" / "audit" / "audit.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def load_known_patterns() -> list:
    """加载软规则知识库（查询接口）"""
    paths = [
        Path.home() / "longhun-system" / "cnsh" / "softlaw" / "known_patterns.jsonl",
        Path(__file__).resolve().parent / "known_patterns.jsonl",
    ]
    for p in paths:
        if p.exists():
            rules = []
            with open(p, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            rules.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
            return rules
    return []

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 Skill · 三色审计+DNA追溯执行器 v1.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python3 audit_check.py --input docs/x.md --module 文档 --version 1.0
  python3 audit_check.py --input bin/x.py --audit-mode engine  # 完整三色引擎裁决
  python3 audit_check.py --text "删除所有历史记录"            # 直接审计文本
  python3 audit_check.py --patterns                          # 查询软规则知识库""",
    )
    parser.add_argument("--input", "-i", help="输入文件路径")
    parser.add_argument("--text", "-t", help="直接审计文本")
    parser.add_argument("--module", "-m", default="UNKNOWN", help="模块名")
    parser.add_argument("--version", "-v", default="1.0", help="版本号")
    parser.add_argument("--audit-mode", "--mode", "-M", choices=["dr", "engine"], default="dr",
                        help="dr=数字根映射(默认) / engine=完整三色引擎裁决 (注: lh入口用--audit-mode避开顶层--mode劫持)")
    parser.add_argument("--patterns", action="store_true", help="查询软规则知识库")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")

    args = parser.parse_args()

    if args.patterns:
        rules = load_known_patterns()
        if args.json:
            print(json.dumps(rules, ensure_ascii=False, indent=2))
        else:
            for r in rules:
                print(f"{r.get('id')} [{r.get('type')}] 信号: {r.get('signal')} → 动作: {r.get('action')}")
        return

    if not args.input and not args.text:
        parser.print_help()
        sys.exit(0)

    if args.input:
        fp = Path(args.input)
        if not fp.exists():
            print(f"🔴 文件不存在: {fp}")
            sys.exit(1)
        result = audit_file(fp, args.module, args.version, args.audit_mode)
        source = str(fp)
    else:
        # 文本审计：写入临时文件过同一流程
        tmp = Path.home() / ".longhun" / "audit" / "_tmp_audit.txt"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(args.text, encoding="utf-8")
        result = audit_file(tmp, args.module, args.version, args.audit_mode)
        tmp.unlink(missing_ok=True)
        source = "(文本)"

    # 审计日志
    write_audit_log({
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "dr": result["dr"],
        "color": result["color"],
        "status": result["status"],
        "dna": result["dna"],
        "mode": result["mode"],
        "warnings": result["warnings"],
    })

    if args.json:
        out = {k: v for k, v in result.items() if k != "engine"}
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"{result['color']} {result['status']} | dr={result['dr']} | DNA: {result['dna']} | mode={result['mode']}")
        if result["warnings"]:
            print(f"⚠️ 警告: {', '.join(result['warnings'])}")
        if result.get("engine") and "裁决理由" in result["engine"]:
            print(f"📋 引擎理由: {result['engine']['裁决理由'][:120]}")

    sys.exit(1 if result["action"] == "reject" else 0)

if __name__ == "__main__":
    main()
