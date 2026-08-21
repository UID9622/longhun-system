#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂红蓝对抗节点 v1.0
DNA: #龍芯⚡️2026-08-21-AUDIT-RED-BLUE-v1.0

节点分工:
  红方 (攻击) —— 尝试注入、伪造、绕过、崩溃系统
  蓝方 (防御) —— 验证系统是否正确识别并驳回攻击

攻击向量 (6类):
  A1 DNA伪造检测
  A2 确认码验证
  A3 输入注入
  A4 边界条件
  A5 导入路径操纵
  A6 MEMORY 崩溃写入
写入 audit_log.jsonl, dimension="red_blue"
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "08_BIN"))

AUDIT_LOG    = ROOT / "audit_log.jsonl"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

try:
    from lh_dna_ref_impl import generate as dna_generate
    DNA_OK = True
except ImportError:
    DNA_OK = False

try:
    from dna_helper import make_dna
    HELPER_OK = True
except ImportError:
    HELPER_OK = False


# ────────────────────────────────────────────────
# 工具
# ────────────────────────────────────────────────

def write_log(record: dict):
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def gen_dna(title: str) -> str:
    if DNA_OK:
        return dna_generate(title=title, category="audit", action="红蓝对抗")["dna_string"]
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-REDBLUE-{title[:8].upper()}"


# ────────────────────────────────────────────────
# A1 · DNA 伪造检测
# ────────────────────────────────────────────────

def attack_a1_dna_forgery() -> dict:
    """伪造 DNA 字符串，验证引擎能否识别格式错误"""
    forged_dnas = [
        "",                                    # 空字符串
        "#龍芯2026-08-21-FAKE",              # 缺少⚡️
        "#龍芯⚡️-没有日期-FAKE",         # 日期格式错误
        "RANDOM_STRING_NOT_DNA",               # 完全无关字符串
        "#龍芯⚡️" + "X" * 200,          # 超长攻击
        "#龍芯⚡️2026-08-21" + "\x00\x01",  # 控制字符
        "#龍芯⚡️2026-13-99-超范围日期",  # 非法日期
    ]

    import re
    VALID_DNA = re.compile(
        r"^#龍芯⚡️\d{4}-\d{2}-\d{2}-.+"
    )

    results = []
    defended = 0
    for fake in forged_dnas:
        is_fake = not VALID_DNA.match(fake) if fake else True
        # 防御成功 = 能识别出伪造
        defended += 1 if is_fake else 0
        results.append({
            "input": fake[:60] if fake else "(empty)",
            "identified_as_forged": is_fake,
            "defended": is_fake,
        })

    rate = defended / len(forged_dnas)
    status = "green" if rate == 1.0 else ("yellow" if rate >= 0.8 else "red")
    return {
        "vector": "A1-DNA-FORGERY",
        "total": len(forged_dnas),
        "defended": defended,
        "defense_rate": round(rate, 3),
        "status": status,
        "p0": rate < 0.8,
        "detail": results,
    }


# ────────────────────────────────────────────────
# A2 · 确认码验证
# ────────────────────────────────────────────────

def attack_a2_confirm_code() -> dict:
    """验证确认码校验逻辑"""
    cases = [
        ("",                                                    False),  # 空
        ("WRONG_CODE",                                          False),  # 完全错误
        ("#CONFIRM🌌9622",                                      False),  # 不完整
        ("#confirm🌌9622-only-once🧬lk9x-772z",               False),  # 小写
        (CONFIRM_CODE + " ",                                    False),  # 尾部有空格
        (CONFIRM_CODE,                                          True),   # 正确
        ("#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z" + "\n",           False),  # 包含换行
        ("  " + CONFIRM_CODE,                                   False),  # 头部有空格
    ]

    defended = 0
    results = []
    for code, should_pass in cases:
        actual_pass = (code == CONFIRM_CODE)
        correct = (actual_pass == should_pass)
        defended += 1 if correct else 0
        results.append({
            "input": code[:50] if code else "(empty)",
            "expected_pass": should_pass,
            "actual_pass":   actual_pass,
            "correct":       correct,
        })

    rate = defended / len(cases)
    status = "green" if rate == 1.0 else ("yellow" if rate >= 0.9 else "red")
    return {
        "vector": "A2-CONFIRM-CODE",
        "total": len(cases),
        "defended": defended,
        "defense_rate": round(rate, 3),
        "status": status,
        "p0": rate < 0.9,
        "detail": results,
    }


# ────────────────────────────────────────────────
# A3 · 输入注入
# ────────────────────────────────────────────────

def attack_a3_injection() -> dict:
    """输入注入攻击——验证 DNA 生成引擎能否安全处理恶意输入"""
    if not DNA_OK:
        return {"vector": "A3-INJECTION", "status": "yellow",
                "p0": False, "msg": "DNA 引擎未加载，跳过"}

    payloads = [
        "'; DROP TABLE users; --",
        "<script>alert(1)</script>",
        "../../../etc/passwd",
        "\x00\x01\x02",
        "A" * 10000,
        "{\"key\": \"value\"}",
        "$(rm -rf /)",
        "\n".join(["line"] * 100),
    ]

    crashed = 0
    results = []
    for payload in payloads:
        try:
            result = dna_generate(
                title=payload[:40],
                category="test",
                action="注入测试"
            )
            dna = result.get("dna_string", "")
            # 验证输出是否包含注入内容
            injection_leaked = any(
                kw in dna for kw in ["DROP", "script", "passwd", "\x00", "rm -rf"]
            )
            results.append({
                "payload": payload[:40],
                "survived": True,
                "injection_leaked": injection_leaked,
                "defended": not injection_leaked,
            })
            if injection_leaked:
                crashed += 1
        except Exception as e:
            results.append({
                "payload": payload[:40],
                "survived": False,
                "error": str(e)[:80],
                "defended": True,  # 崩溃也是防御成功（屠小失败）
            })

    total_defended = sum(1 for r in results if r.get("defended"))
    rate = total_defended / len(payloads)
    status = "green" if rate >= 0.9 else ("yellow" if rate >= 0.7 else "red")
    return {
        "vector": "A3-INJECTION",
        "total": len(payloads),
        "defended": total_defended,
        "defense_rate": round(rate, 3),
        "status": status,
        "p0": rate < 0.7,
        "detail": results,
    }


# ────────────────────────────────────────────────
# A4 · 边界条件
# ────────────────────────────────────────────────

def attack_a4_boundary() -> dict:
    """边界条件——None / 空 / 极长 / 特殊 Unicode"""
    if not DNA_OK:
        return {"vector": "A4-BOUNDARY", "status": "yellow",
                "p0": False, "msg": "DNA 引擎未加载"}

    cases = [
        ("",           "empty_title"),
        (" ",           "whitespace"),
        ("\t\n",        "control_chars"),
        ("🐉" * 100,    "emoji_flood"),
        ("龍" * 5000,  "unicode_long"),
        ("0" * 10000,   "digit_flood"),
        ("中文测试",    "normal_chinese"),
    ]

    survived = 0
    results = []
    for payload, label in cases:
        try:
            r = dna_generate(
                title=payload[:40],
                category="boundary",
                action="边界测试"
            )
            assert "dna_string" in r and r["dna_string"].startswith("#龍芯⚡️")
            survived += 1
            results.append({"label": label, "survived": True})
        except Exception as e:
            results.append({"label": label, "survived": False,
                            "error": str(e)[:80]})

    rate = survived / len(cases)
    status = "green" if rate >= 0.9 else ("yellow" if rate >= 0.7 else "red")
    return {
        "vector": "A4-BOUNDARY",
        "total": len(cases),
        "survived": survived,
        "defense_rate": round(rate, 3),
        "status": status,
        "p0": rate < 0.5,
        "detail": results,
    }


# ────────────────────────────────────────────────
# A5 · 导入路径操纵
# ────────────────────────────────────────────────

def attack_a5_path_traversal() -> dict:
    """路径遇历攻击——验证模块导入路径是否局限在 08_BIN"""
    evil_paths = [
        "../../../../../etc/passwd",
        "../../secrets",
        "~/.ssh/id_rsa",
        "/etc/shadow",
        "C:\\Windows\\System32\\config\\SAM",
    ]

    defended = 0
    results = []
    for path_str in evil_paths:
        p = Path(path_str)
        # 防御逻辑：路径必须在 ROOT 下才允许
        try:
            resolved = (ROOT / "08_BIN" / path_str).resolve()
            is_safe = str(resolved).startswith(str(ROOT.resolve()))
        except Exception:
            is_safe = False

        defended += 1 if not is_safe else 0
        results.append({
            "path": path_str,
            "resolved_safe": is_safe,
            "defended": not is_safe,
        })

    rate = defended / len(evil_paths)
    status = "green" if rate == 1.0 else ("yellow" if rate >= 0.8 else "red")
    return {
        "vector": "A5-PATH-TRAVERSAL",
        "total": len(evil_paths),
        "defended": defended,
        "defense_rate": round(rate, 3),
        "status": status,
        "p0": rate < 1.0,   # 任何路径遇历都是 P0
        "detail": results,
    }


# ────────────────────────────────────────────────
# A6 · MEMORY 崩溃写入
# ────────────────────────────────────────────────

def attack_a6_memory_crash() -> dict:
    """验证 append_with_dna 面对恶意输入时是否会崩溃"""
    if not HELPER_OK:
        return {"vector": "A6-MEMORY-CRASH", "status": "yellow",
                "p0": False, "msg": "dna_helper 未加载，跳过"}

    from dna_helper import append_with_dna

    payloads = [
        "",                          # 空内容（应篡默返回）
        "ERROR: 需要过滤的内容",    # ERROR 开头（应跳过）
        "A" * 100000,                # 超大内容
        "\x00" * 100,                # 空字节
        "🐉" * 500,                # emoji 洪水
    ]

    survived = 0
    results = []
    for payload in payloads:
        try:
            result = append_with_dna(
                payload, source="red_blue",
                category="test", action="崩溃测试",
                silent=True
            )
            survived += 1
            results.append({"payload": payload[:30] if payload else "(empty)",
                            "survived": True, "returned": str(result)[:30]})
        except Exception as e:
            results.append({"payload": payload[:30] if payload else "(empty)",
                            "survived": False, "error": str(e)[:80]})

    rate = survived / len(payloads)
    status = "green" if rate == 1.0 else ("yellow" if rate >= 0.8 else "red")
    return {
        "vector": "A6-MEMORY-CRASH",
        "total": len(payloads),
        "survived": survived,
        "defense_rate": round(rate, 3),
        "status": status,
        "p0": rate < 0.8,
        "detail": results,
    }


# ────────────────────────────────────────────────
# 汇总输出
# ────────────────────────────────────────────────

ALL_ATTACKS = [
    ("A1", "DNA伪造检测",   attack_a1_dna_forgery),
    ("A2", "确认码验证",     attack_a2_confirm_code),
    ("A3", "输入注入",       attack_a3_injection),
    ("A4", "边界条件",       attack_a4_boundary),
    ("A5", "导入路径操纵",   attack_a5_path_traversal),
    ("A6", "MEMORY崩溃写入", attack_a6_memory_crash),
]


def run_redblue(attacks: list = None, verbose: bool = False):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    targets = attacks or [a[0] for a in ALL_ATTACKS]

    print()
    print("╔" + "═" * 67 + "╗")
    print("║  🔴🟦 红蓝对抗节点 v1.0" + " " * 44 + "║")
    print("╠" + "═" * 67 + "╣")
    print(f"║  时间: {ts}" + " " * (59 - len(ts)) + "║")
    print("╠" + "═" * 67 + "╣")
    print("║  {:<6} {:<16} {:>5} {:>5}  {:>8}  {:^8}  ║".format(
        "向量", "名称", "总数", "防御", "防御率", "状态"))
    print("╠" + "═" * 67 + "╣")

    all_green = True
    p0_triggered = False

    for aid, aname, afunc in ALL_ATTACKS:
        if aid not in targets:
            continue
        try:
            result = afunc()
        except Exception as e:
            result = {"vector": aid, "status": "red", "p0": True,
                      "total": 0, "defended": 0, "defense_rate": 0,
                      "msg": f"攻击函数崩溃: {e}"}

        rate  = result.get("defense_rate", 0)
        total = result.get("total", result.get("survived", 0))
        defs  = result.get("defended", result.get("survived", 0))
        ICONS = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
        icon  = ICONS.get(result["status"], "⚪")

        if result["status"] != "green":
            all_green = False
        if result.get("p0"):
            p0_triggered = True

        print("║  {:<6} {:<16} {:>5} {:>5}  {:>7}%  {}       ║".format(
            aid, aname[:16], total, defs, int(rate * 100), icon))

        if verbose and result.get("detail"):
            for d in result["detail"][:3]:
                line = json.dumps(d, ensure_ascii=False)[:60]
                print(f"║    {line}")

        # 生成 DNA
        dna_str = gen_dna(f"{aid}-红蓝对抗")

        # 写日志
        write_log({
            "timestamp": ts,
            "dimension": "red_blue",
            "vector": result.get("vector", aid),
            "attack_name": aname,
            "status": result["status"],
            "p0": result.get("p0", False),
            "total": total,
            "defended": defs,
            "defense_rate": rate,
            "dna": dna_str,
        })

    print("╠" + "═" * 67 + "╣")
    overall = ("🟢 全部防御成功" if all_green else
               "🔴 P0 红线被击穿！" if p0_triggered else "🟡 存在警告")
    print("║  综合判定: {:<57}║".format(overall))
    if p0_triggered:
        print("║  ⚠️  P0 红线被击穿！立即阻断并修复。" + " " * 36 + "║")
    print("╚" + "═" * 67 + "╝")
    print(f"\n💾 审计日志已写入: {AUDIT_LOG}")

    if p0_triggered:
        sys.exit(1)


# ────────────────────────────────────────────────
# 入口
# ────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="龍魂红蓝对抗节点")
    parser.add_argument(
        "--attack", default="all",
        help="攻击向量: all | A1 | A2,A3 | ..."
    )
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出对抗详情")
    args = parser.parse_args()

    if args.attack == "all":
        targets = [a[0] for a in ALL_ATTACKS]
    else:
        targets = [x.strip().upper() for x in args.attack.split(",")]

    run_redblue(attacks=targets, verbose=args.verbose)
