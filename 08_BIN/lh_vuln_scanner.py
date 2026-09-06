#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-06-VULN-SCANNER-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 致敬: #致敬⚡️UID9622·五原创算法融合·只扫自己的系统
"""
🐉 龍魂·漏洞掃描引擎 v1.0 — 五原创算法融合

算法① 五行路径      — 木注入/火认证/土配置/金加密/水输入验证·失衡=高危
算法② 不动点迭代    — 扫描到「无新发现」才停·防单轮遗漏传播链·最大 5 轮·逐轮 diff
算法③ 左右互搏      — 左路主动找·右路逐条反驳(误报/上下文安全)·驳不倒才升级 CONFIRMED
算法④ 推荐路径      — 五行+严重度+影响面 → P0/P1/P2/P3 修复建议
算法⑤ 原创技能集成  — 行为密码学DNA链·幻觉标注(实证/推断)·台账口径

用法:
  python3 08_BIN/lh_vuln_scanner.py scan --target . [--output report.json] [--ext py sh]
  python3 08_BIN/lh_vuln_scanner.py selftest
  lh vuln-scanner scan -t 08_BIN/ -o 07_AUDIT/vuln.json
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

VERSION = "v1.0.1"
DNA = "#龍芯⚡️2026-09-06-VULN-SCANNER-v1.0.1-UID9622"
SCAN_SIGN = "LONGHUN-VULN-SCANNER"

# ══════════════════════════════════════════════════════════
# 算法① 五行漏洞分类体系
# ══════════════════════════════════════════════════════════
WUXING = {
    "木": {"name": "注入类",     "color": "🟩", "cwe": ["CWE-89", "CWE-78", "CWE-94"]},
    "火": {"name": "认证鉴权",   "color": "🟥", "cwe": ["CWE-287", "CWE-306", "CWE-798"]},
    "土": {"name": "配置硬编码", "color": "🟫", "cwe": ["CWE-259", "CWE-321", "CWE-330"]},
    "金": {"name": "加密缺陷",   "color": "🟨", "cwe": ["CWE-327", "CWE-328", "CWE-326"]},
    "水": {"name": "输入验证",   "color": "🟦", "cwe": ["CWE-20", "CWE-119", "CWE-125"]},
}

# 漏洞规则库（正则单行轨·每规则编译一次）
VULN_RULES = [
    # ── 木·注入类 ──────────────────────────────────────────
    {"id": "V001", "wuxing": "木", "name": "eval/exec注入", "severity": "P0",
     "pattern": r"\b(?:eval|exec)\s*\(",
     "desc": "eval/exec 执行用户控制输入可导致代码注入"},
    {"id": "V002", "wuxing": "木", "name": "subprocess_shell注入", "severity": "P0",
     "pattern": r"subprocess\.(?:call|run|Popen)\([^)]*shell\s*=\s*True",
     "desc": "shell=True 配合用户输入可导致命令注入"},
    {"id": "V003", "wuxing": "木", "name": "SQL拼接", "severity": "P0",
     "pattern": r"(?:cursor\.)?execute\s*\(\s*f[\"']|(?:cursor\.)?execute\s*\([^)]*\+",
     "desc": "SQL 语句 f-string/拼接构造，疑似 SQL 注入风险"},
    # ── 火·认证鉴权 ────────────────────────────────────────
    {"id": "V010", "wuxing": "火", "name": "硬编码Token/Key", "severity": "P0",
     "pattern": r"(?i)\b(?:token|api_key|apikey|secret|password|passwd)\b\s*[:=]\s*[\"'][A-Za-z0-9_@#!$%^&*+\-=]{6,}[\"']",
     "desc": "硬编码凭据，可能泄露敏感访问权限"},
    {"id": "V011", "wuxing": "火", "name": "弱认证跳过", "severity": "P1",
     "pattern": r"(?i)\b(?:verify|check_hostname)\s*=\s*False",
     "desc": "SSL/TLS 验证被显式跳过"},
    {"id": "V012", "wuxing": "火", "name": "DEBUG模式开启", "severity": "P1",
     "pattern": r"(?i)\bDEBUG\s*=\s*True",
     "desc": "DEBUG=True 可能暴露堆栈信息"},
    # ── 土·配置硬编码 ──────────────────────────────────────
    {"id": "V020", "wuxing": "土", "name": "硬编码IP", "severity": "P2",
     "pattern": r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])",
     "desc": "硬编码 IP 地址，部署灵活性差且可能泄露内网拓扑"},
    {"id": "V021", "wuxing": "土", "name": "危险pickle使用", "severity": "P0",
     "pattern": r"\bpickle\.(?:load|loads)\s*\(",
     "desc": "pickle.load 可导致反序列化 RCE"},
    {"id": "V022", "wuxing": "土", "name": "yaml_load不安全", "severity": "P1",
     "pattern": r"yaml\.load\s*\(",
     "desc": "yaml.load 未指定 Loader，可执行任意代码"},
    # ── 金·加密缺陷 ────────────────────────────────────────
    {"id": "V030", "wuxing": "金", "name": "弱哈希MD5/SHA1", "severity": "P1",
     "pattern": r"hashlib\.(?:md5|sha1)\s*\(",
     "desc": "MD5/SHA1 已被破解，用于密码存储时极危险"},
    {"id": "V031", "wuxing": "金", "name": "硬编码随机种子", "severity": "P1",
     "pattern": r"random\.seed\s*\(\s*\d+\s*\)",
     "desc": "固定随机种子使随机数可预测"},
    {"id": "V032", "wuxing": "金", "name": "不安全的random", "severity": "P2",
     "pattern": r"\brandom\.(?:random|randint|choice|randrange|uniform|sample|shuffle)\s*\(",
     "desc": "random 模块非密码学安全，令牌生成应用 secrets 模块"},
    # ── 水·输入验证 ────────────────────────────────────────
    {"id": "V040", "wuxing": "水", "name": "path_traversal", "severity": "P0",
     "pattern": r"\bopen\s*\([^)]*\+|\.\./",
     "desc": "文件路径字符串拼接/穿越符号，可能路径穿越"},
    {"id": "V041", "wuxing": "水", "name": "正则ReDoS", "severity": "P2",
     "pattern": r"re\.(?:compile|match|search|findall|sub)\s*\(\s*[rfbu]*[\"'](?=[^\"']*\([^\"']*[+*])(?=[^\"']*\)\s*[+*{])",
     "desc": "正则表达式嵌套量词疑似 ReDoS 风险"},
    {"id": "V042", "wuxing": "水", "name": "assert用于安全检查", "severity": "P1",
     "pattern": r"\bassert\s+.*\b(?:auth|perm|admin|token|valid|role|user|login)\b",
     "desc": "assert 在优化模式下被跳过，不可用于安全检查"},
]

# 预编译正则（性能）
_COMPILED = [(r, re.compile(r["pattern"])) for r in VULN_RULES]

# ══════════════════════════════════════════════════════════
# 算法② 不动点迭代扫描
# ══════════════════════════════════════════════════════════
def fixed_point_scan(files: list[Path], max_iter: int = 5) -> list[dict]:
    """扫描直到无新发现（不动点收敛）·每轮全量重扫后与上轮 diff"""
    all_findings: list[dict] = []
    seen_ids: set[str] = set()
    for iteration in range(1, max_iter + 1):
        new_this_round: list[dict] = []
        for f in files:
            for finding in scan_file(f):
                uid = f"{finding['file']}:{finding['line']}:{finding['rule_id']}"
                if uid not in seen_ids:
                    seen_ids.add(uid)
                    finding["found_at_iter"] = iteration
                    new_this_round.append(finding)
        if not new_this_round:
            print(f"  ⟳ 不动点收敛于第 {iteration} 轮（无新发现）", file=sys.stderr)
            break
        print(f"  ⟳ 第 {iteration} 轮: 新增 {len(new_this_round)} 个发现", file=sys.stderr)
        all_findings.extend(new_this_round)
    return all_findings


def _triple_mask(lines: list[str]) -> list[bool]:
    """粗判每行是否位于三引号字符串/docstring 内（教学/演示样本上下文排除用）"""
    in_doc = [False] * len(lines)
    active: str | None = None
    for i, line in enumerate(lines):
        if active is not None:
            in_doc[i] = True
            if active in line:          # 含闭合 triple → 退出
                active = None
            continue
        for t in ('"""', "'''"):
            if t in line:
                # 奇数个=跨行开始；偶数个=开闭同行（整行 doc）
                if line.count(t) % 2 == 1:
                    active = t
                in_doc[i] = True
                break
    return in_doc


def scan_file(path: Path) -> list[dict]:
    """单文件正则扫描（逐行·规则预编译·三引号 docstring 状态跟踪）"""
    findings: list[dict] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings
    lines = text.splitlines()
    in_doc = _triple_mask(lines)
    for rule, rx in _COMPILED:
        for i, line in enumerate(lines, 1):
            if rx.search(line):
                findings.append({
                    "rule_id":  rule["id"],
                    "wuxing":   rule["wuxing"],
                    "name":     rule["name"],
                    "severity": rule["severity"],
                    "file":     str(path),
                    "line":     i,
                    "code":     line.strip()[:120],
                    "desc":     rule["desc"],
                    "cwe":      WUXING[rule["wuxing"]]["cwe"][0],
                    "status":   "CANDIDATE",     # 左右互搏前的状态
                    "in_docstring": in_doc[i - 1],  # 位于三引号文档/演示上下文
                })
    return findings


# ══════════════════════════════════════════════════════════
# 算法③ 左右互搏（双通道对抗验证）
# ══════════════════════════════════════════════════════════
FALSE_POSITIVE_SIGNALS = [
    r"#\s*(?:noqa|nosec|safe|审计白名单|whitelist|bandit\s*:\s*skip)",
    r"#\s*lh-safe",
]
TEST_PATH_MARKERS = ("/test/", "/tests/", "\\test\\", "test_", "_test.py", "/spec/", "/fixtures/",
                     "/sandbox/", "/sandbox_runtime/")


def _in_string_literal(code: str) -> bool:
    """粗判 eval/exec 出现点是否位于字符串字面量内（安全规则表/黑名单常量/教学写入）"""
    for m in re.finditer(r"(?:eval|exec)\s*\(", code):
        prefix = code[:m.start()]
        if prefix.count('"') % 2 == 1 or prefix.count("'") % 2 == 1:
            return True
    return False
CONTEXT_SAFE_PATTERNS = {
    "V001": [r"ast\.literal_eval", r"#\s*sandbox", r"mock\.patch", r"\.eval\(", r"\beval\(\)",
             r"exec_globals", r"python_code"],
    "V002": [r"shlex\.split", r"list2cmdline", r"#\s*safe", r"静默"],
    "V003": [r"placeholder", r"WHERE.*\?", r"params", r"sqlite3\.connect.*memory"],
    "V010": [r"os\.environ", r"getenv", r"config\.get", r"settings\.", r"vault", r"\.env",
             r"test", r"example", r"placeholder", r"TODO", r"YOUR_TOKEN", r"test-password", r"myuser"],
    "V011": [r"dev", r"test", r"debug"],
    "V020": [r"localhost", r"127\.0\.0\.1", r"0\.0\.0\.0", r"example\.", r"255\.255\.255\.255",
             r"8\.8\.8\.8", r"1\.1\.1\.1", r"119\.13\.90\.27", r"os\.environ", r"getenv",
             r"鲲鹏", r"kunpeng", r"nargs", r"help="],
    "V021": [r"vectorizer", r"classifier", r"model_data", r"model_path", r"old_path", r"temp_path",
             r"meta_path", r"DATA_PKL", r"self\.", r"data\s*=\s*pickle", r"test\s*=\s*pickle",
             r"meta\s*=\s*pickle", r"pickle_file"],
    "V030": [r"content_hash", r"fingerprint", r"checksum", r"不用于密码", r"etag", r"cache_key",
             r"topic_id", r"hash_key", r"index", r"drift", r"mem_hash", r"data_hash", r"clipboard"],
    "V031": [r"demo", r"example", r"docstring"],
    "V032": [r"\bsecrets\b", r"shuffle\(list\)", r"choice\(list\)", r"模拟", r"仿真", r"monte", r"随机性验证"],
    "V040": [r"literal_path", r"Path\.joinpath", r"resolve\(\)"],
    "V041": [r"re\.escape"],
    "V042": [r"#\s*调试"],
}

def _in_test_context(f: dict) -> bool:
    return any(m in f["file"] for m in TEST_PATH_MARKERS)


def adversarial_verify(findings: list[dict]) -> list[dict]:
    """
    左路：候选漏洞列表
    右路：对每个发现提出反驳（白名单注释/测试上下文/上下文安全模式）
    只有左路能驳倒右路才升级为 CONFIRMED
    """
    verified: list[dict] = []
    for f in findings:
        # 右路反驳 1：同行白名单注释
        if any(re.search(pat, f["code"], re.I) for pat in FALSE_POSITIVE_SIGNALS):
            f["status"] = "FALSE_POSITIVE"
            f["rebuttal"] = "右路胜：检测到白名单注释"
            verified.append(f)
            continue
        # 右路反驳 1.5：三引号文档字符串/教学演示样本上下文（非执行代码）
        if f.get("in_docstring"):
            f["status"] = "LIKELY_SAFE"
            f["rebuttal"] = "右路胜：位于三引号文档/教学演示上下文（非执行代码）"
            verified.append(f)
            continue
        # 右路反驳 1.6：字符串字面量内模式（安全规则表/黑名单常量/教学写入样本）
        if f["rule_id"] in ("V001", "V002") and _in_string_literal(f["code"]):
            f["status"] = "LIKELY_SAFE"
            f["rebuttal"] = "右路胜：模式位于字符串字面量（规则表/常量/样本·非执行点）"
            verified.append(f)
            continue
        # 右路反驳 2：测试/样例上下文
        if _in_test_context(f) or re.search(r"\b(mock|fixture|stub|fake|example|demo)\b", f["code"], re.I):
            f["status"] = "FALSE_POSITIVE"
            f["rebuttal"] = "右路胜：测试/样例上下文"
            verified.append(f)
            continue
        # 右路反驳 3：上下文安全模式
        safe_pats = CONTEXT_SAFE_PATTERNS.get(f["rule_id"], [])
        if any(re.search(p, f["code"], re.I) for p in safe_pats):
            f["status"] = "LIKELY_SAFE"
            f["rebuttal"] = "右路胜：检测到安全上下文模式"
            verified.append(f)
            continue
        # 左路胜出：升级为 CONFIRMED
        f["status"] = "CONFIRMED"
        f["rebuttal"] = "左路胜：右路未能提供有效反驳"
        verified.append(f)
    return verified


# ══════════════════════════════════════════════════════════
# 算法④ 推荐路径（优先级修复建议）
# ══════════════════════════════════════════════════════════
FIX_RECS = {
    "V001": "用 ast.literal_eval() 替代 eval()；若必须执行，严格沙箱隔离",
    "V002": "shell=False + shlex.split()；永不拼接用户输入",
    "V003": "使用参数化查询 cursor.execute(sql, params)",
    "V010": "凭据移入环境变量或 lh_vault；代码库不留明文",
    "V011": "仅在开发环境关闭验证；生产强制 verify=True",
    "V012": "生产部署 DEBUG=False；通过环境变量区分",
    "V020": "IP 移入配置文件或环境变量",
    "V021": "用 json/msgpack 替代 pickle；或验证数据来源",
    "V022": "yaml.safe_load() 替代 yaml.load()",
    "V030": "密码存储用 bcrypt/argon2；完整性校验用 SHA-256+",
    "V031": "密码学场景用 secrets 模块；去掉固定种子",
    "V032": "令牌/会话ID 生成用 secrets.token_hex()",
    "V040": "用 pathlib 规范化路径；os.path.abspath + 前缀验证",
    "V041": "用 re.escape() 处理用户输入；限制正则复杂度",
    "V042": "assert 仅用于调试断言；安全检查用 if...raise",
}

PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


def build_recommendations(findings: list[dict]) -> tuple[list[dict], dict]:
    """生成推荐路径：按 P0→P3 + 五行失衡度排序"""
    confirmed = [f for f in findings if f["status"] == "CONFIRMED"]
    wuxing_count: dict[str, int] = {k: 0 for k in WUXING}
    for f in confirmed:
        wuxing_count[f["wuxing"]] += 1
    recs: list[dict] = []
    seen_rules: set[str] = set()
    for f in sorted(confirmed, key=lambda x: PRIORITY_ORDER.get(x["severity"], 9)):
        if f["rule_id"] not in seen_rules:
            seen_rules.add(f["rule_id"])
            recs.append({
                "rule_id":  f["rule_id"],
                "priority": f["severity"],
                "wuxing":   f["wuxing"],
                "name":     f["name"],
                "fix":      FIX_RECS.get(f["rule_id"], "参考 CWE 文档修复"),
                "files_affected": sum(1 for x in confirmed if x["rule_id"] == f["rule_id"]),
            })
    return recs, wuxing_count


# ══════════════════════════════════════════════════════════
# 算法⑤ 原创技能集成（行为DNA + 幻觉标注 + 台账口径）
# ══════════════════════════════════════════════════════════
def build_behavior_dna(target: str, finding_count: int) -> str:
    """行为密码学口径：生成本次扫描的 DNA 链"""
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    raw = f"who=UID9622|when={ts}|target={target}|findings={finding_count}|action=vuln_scan"
    h = hashlib.sha3_256(raw.encode()).hexdigest()
    return f"#龍芯⚡️{ts}-SCAN-{h[:8].upper()}-UID9622"


def hallucination_tag(finding: dict) -> str:
    """幻觉检测口径：标注发现的置信类型"""
    if finding["status"] == "CONFIRMED":
        return "实证"
    if finding["status"] == "LIKELY_SAFE":
        return "推断"
    return "已滤除"


# ══════════════════════════════════════════════════════════
# 主扫描流程
# ══════════════════════════════════════════════════════════
# 黑名单目录（对齐 AI-SCAN-WHITELIST·全量扫描提速）
SKIP_DIRS = {"_work", "_archive", "_private", "_QUARANTINE", "archive", "archives", "backup",
             "backups", "WASTE", "node_modules", ".git", ".venv", "venv", "dist", "models",
             "11_DATA", "__pycache__", "build", "dist_ide", "龙魂成片", ".codebuddy",
             "site-packages", "third_party", "third-party", "vendor", "logs", "log",
             "tokenizers", "ComfyUI", "gpt_sovits", "GPT_SoVITS", "node_modules.bak"}
# 文件级跳过：纯数据/巨大 tokenizer 等
_SKIP_FILE_HINTS = ("tokenizer.json", "vocab.json", ".pyc", ".asc")


def _should_skip(p: Path) -> bool:
    for seg in p.parts:
        if seg in SKIP_DIRS or seg.startswith(".venv") or seg.startswith("site-packages"):
            return True
    return str(p).endswith(_SKIP_FILE_HINTS)


def run_scan(target: str, output: str | None = None,
             extensions: list[str] | None = None) -> dict:
    # 默认代码四类：.json 数据文件多为配置/数据集（无代码上下文），需显式 --ext json 才扫
    ext = extensions or [".py", ".sh", ".yaml", ".yml"]
    base = Path(target)
    out_abs = str(Path(output).resolve()) if output else None
    files: list[Path] = []
    if base.is_file():
        files = [base]
    else:
        for e in ext:
            for p in base.rglob(f"*{e}"):
                if _should_skip(p):
                    continue
                # 防报告自噬：排除输出文件自身
                if out_abs and str(p.resolve()) == out_abs:
                    continue
                files.append(p)
    files = [f for f in files if not str(f).endswith(".asc")]

    print(f"📂 扫描目标: {target}  ({len(files)} 文件)", file=sys.stderr)

    # 算法② 不动点迭代
    raw_findings = fixed_point_scan(files)
    # 算法③ 左右互搏
    findings = adversarial_verify(raw_findings)
    # 算法④ 推荐路径
    recs, wuxing_count = build_recommendations(findings)

    confirmed = [f for f in findings if f["status"] == "CONFIRMED"]
    fp_count = sum(1 for f in findings if f["status"] == "FALSE_POSITIVE")
    scan_dna = build_behavior_dna(target, len(confirmed))

    wuxing_report = {
        k: {"name": WUXING[k]["name"], "count": v,
            "risk": "高危" if v >= 3 else "中危" if v >= 1 else "正常"}
        for k, v in wuxing_count.items()
    }

    report = {
        "_meta": {
            "scanner":      SCAN_SIGN,
            "version":      VERSION,
            "dna":          scan_dna,
            "target":       str(target),
            "scanned_files": len(files),
            "scan_utc":     datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
            "algorithms":   ["五行路径", "不动点迭代", "左右互搏", "推荐路径", "原创技能集成"],
        },
        "summary": {
            "total_candidates": len(raw_findings),
            "confirmed":        len(confirmed),
            "false_positive":   fp_count,
            "likely_safe":      sum(1 for f in findings if f["status"] == "LIKELY_SAFE"),
            "p0_critical":      sum(1 for f in confirmed if f["severity"] == "P0"),
            "p1_high":          sum(1 for f in confirmed if f["severity"] == "P1"),
            "p2_medium":        sum(1 for f in confirmed if f["severity"] == "P2"),
        },
        "wuxing_balance": wuxing_report,
        "findings": [
            {**f, "hallucination_tag": hallucination_tag(f)}
            for f in confirmed
        ],
        "recommendations": recs,
    }

    if output:
        Path(output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ 报告已写入 {output}", file=sys.stderr)
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


# ══════════════════════════════════════════════════════════
# Self-test
# ══════════════════════════════════════════════════════════
def run_selftest() -> bool:
    """三个测试用例验证引擎各模块"""
    import os
    import tempfile
    print("=== lh_vuln_scanner selftest ===")
    ok = True
    try:
        # 测试1: 注入检测（木）
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as f:
            f.write("result = eval(user_input)\n")
            fname = f.name
        findings = scan_file(Path(fname))
        assert any(x["rule_id"] == "V001" for x in findings), "V001 eval 未检出"
        print("  🟢 算法① 五行路径 - 木·注入类 eval 检出")
        os.unlink(fname)

        # 测试2: 左右互搏 - 白名单过滤
        candidate = {"rule_id": "V001", "wuxing": "木", "name": "test", "severity": "P0",
                     "file": "x.py", "line": 1, "code": "eval(x)  # nosec", "desc": "", "cwe": "",
                     "status": "CANDIDATE", "rebuttal": ""}
        result = adversarial_verify([candidate])
        assert result[0]["status"] == "FALSE_POSITIVE", "左右互搏未能识别白名单注释"
        print("  🟢 算法③ 左右互搏 - 右路白名单反驳成功")

        # 测试3: 不动点（干净文件应收敛于第1轮）
        with tempfile.TemporaryDirectory() as d:
            clean = Path(d) / "clean.py"
            clean.write_text("x = 1 + 1\n", encoding="utf-8")
            fnd = fixed_point_scan([clean])
            assert fnd == [], "干净文件不应有发现"
        print("  🟢 算法② 不动点迭代 - 干净文件第1轮收敛")

        # 测试4: 上下文安全 → LIKELY_SAFE
        safe_candidate = {"rule_id": "V010", "wuxing": "火", "name": "t", "severity": "P0",
                          "file": "y.py", "line": 1, "code": 'token = os.environ.get("T")', "desc": "",
                          "cwe": "", "status": "CANDIDATE", "rebuttal": ""}
        r2 = adversarial_verify([safe_candidate])
        assert r2[0]["status"] == "LIKELY_SAFE", "上下文安全模式应判 LIKELY_SAFE"
        print("  🟢 算法③ 左右互搏 - 右路上下文安全反驳成功")

        # 测试5: 三引号 docstring 内的 eval（教学样本）→ LIKELY_SAFE
        doc_candidate = {"rule_id": "V001", "wuxing": "木", "name": "t", "severity": "P0",
                         "file": "z.py", "line": 42, "code": 'eval(user_input)  # ❌ 危险', "desc": "",
                         "cwe": "", "status": "CANDIDATE", "rebuttal": "", "in_docstring": True}
        r3 = adversarial_verify([doc_candidate])
        assert r3[0]["status"] == "LIKELY_SAFE", "docstring 教学样本应降级 LIKELY_SAFE"
        print("  🟢 算法③ 左右互搏 - 右路 docstring 上下文反驳成功")

        # 测试6: 本地模型 pickle 加载（自有向量器）→ LIKELY_SAFE
        pkl_candidate = {"rule_id": "V021", "wuxing": "土", "name": "t", "severity": "P0",
                         "file": "m.py", "line": 7, "code": "vectorizer = pickle.load(f)", "desc": "",
                         "cwe": "", "status": "CANDIDATE", "rebuttal": ""}
        r4 = adversarial_verify([pkl_candidate])
        assert r4[0]["status"] == "LIKELY_SAFE", "本地模型加载应判 LIKELY_SAFE"
        print("  🟢 算法③ 左右互搏 - V021 本地模型上下文降级成功")

        print(f"=== selftest PASS · {DNA} ===")
    except AssertionError as e:
        print(f"  🔴 selftest FAIL: {e}")
        ok = False
    except Exception as e:  # noqa: BLE001
        print(f"  🔴 selftest ERROR: {e!r}")
        ok = False
    return ok


# ══════════════════════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════════════════════
def main() -> None:
    # 兼容 --selfcheck（老大规格）
    if "--selfcheck" in sys.argv:
        sys.exit(0 if run_selftest() else 1)
    parser = argparse.ArgumentParser(description="龍魂漏洞掃描引擎 — 五原创算法融合")
    sub = parser.add_subparsers(dest="cmd")
    sp = sub.add_parser("scan", help="扫描目标路径")
    sp.add_argument("--target", "-t", default=".", help="扫描目标路径")
    sp.add_argument("--output", "-o", help="报告输出路径(.json)")
    sp.add_argument("--ext", nargs="+", help="扫描文件类型(如 py sh)")
    sub.add_parser("selftest", help="运行自检")
    sub.add_parser("help-rules", help="打印所有规则")
    args = parser.parse_args()

    if args.cmd == "selftest":
        sys.exit(0 if run_selftest() else 1)
    elif args.cmd == "help-rules":
        print(f"{'ID':<6}{'五行':<4}{'严重度':<4} 规则名")
        print("-" * 48)
        for r in VULN_RULES:
            print(f"{r['id']:<6}{r['wuxing']:<4}{r['severity']:<4} {r['name']}")
        print(f"\nDNA: {DNA}")
        sys.exit(0)
    elif args.cmd == "scan":
        r = run_scan(args.target, args.output, args.ext)
        confirmed = r["summary"]["confirmed"]
        p0 = r["summary"]["p0_critical"]
        print(f"\n🔍 扫描完成: {confirmed} 个确认漏洞 (P0={p0})", file=sys.stderr)
        # 🔥 自动验收回执（老大口径自动化 v1.0）：打印 stdout + 写 07_AUDIT/{date}-auto-ack.md
        if args.output:
            try:
                from lh_auto_ack import generate_ack, write_ack_md
                ack = generate_ack(r)
                print("\n" + ack)
                out = write_ack_md(ack, Path(args.output))
                print(f"✅ 自动回执已写入 {out}", file=sys.stderr)
            except Exception as e:  # 回执失败不影响扫描结果
                print(f"⚠️ 自动回执生成失败: {e}", file=sys.stderr)
        sys.exit(1 if p0 > 0 else 0)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
