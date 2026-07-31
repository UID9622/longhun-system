# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·丙辰·己丑·需-DATA-MELTDOWN-ENGINE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
lh_data_meltdown — 龍魂数据黑洞五层熔断引擎 v1.0

五层防御：
  L0 · 前端沙箱 — 敏感字段不出用户设备
  L1 · 传输黑洞 — 只传哈希/密文
  L2 · 内存瞬态 — 明文生命周期 < 500ms
  L3 · 存储拒绝 — 禁止明文/可逆密文入DB
  L4 · 日志湮灭 — 涉敏字段自动替换 ***MELTDOWN***

用法：
  python3 bin/lh_data_meltdown.py scan "<含敏感信息的文本>"
  python3 bin/lh_data_meltdown.py sanitize-log "<日志行>"
  python3 bin/lh_data_meltdown.py hash-password "<密码>"
  python3 bin/lh_data_meltdown.py check-field password "my_secret"

DNA: #龍芯⚡️丙午·丙申·丙辰·己丑·需-DATA-MELTDOWN-ENGINE-v1.0
# STATUS: ⚠️ DEPRECATED · 敏感数据熔断层能力已整合进不动点归档引擎的 BLACK/RED 隔离机制
# 保留原因: 历史敏感字段处理参考
📇 项目身份 · 联系 · 支持 → assets/PUBLIC_IDENTITY.md
"""

import argparse
import hashlib
import hmac
import json
import os
import re
import secrets
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

# ============================================
# 敏感字段清单
# ============================================

@dataclass
class SensitiveField:
    """敏感字段定义"""
    name: str
    level: str          # 🔴高敏 / 🟡中敏
    patterns: List[str] # 字段名匹配模式
    l0_action: str      # L0 前端处理
    l1_transport: str   # L1 传输方式
    l3_storage: str     # L3 存储方式
    log_action: str     # L4 日志处理

SENSITIVE_FIELDS: List[SensitiveField] = [
    SensitiveField(
        name="password", level="🔴",
        patterns=[r"password", r"passwd", r"pwd", r"secret", r"密钥"],
        l0_action="SM3哈希+salt", l1_transport="hex哈希",
        l3_storage="SM3哈希(不可逆)", log_action="MELTDOWN",
    ),
    SensitiveField(
        name="id_card", level="🔴",
        patterns=[r"id_card", r"idcard", r"身份证", r"身份证号", r"身份证号码"],
        l0_action="SM4加密+SM3验证", l1_transport="SM4密文",
        l3_storage="SM3(原文)验证", log_action="MELTDOWN",
    ),
    SensitiveField(
        name="bank_account", level="🔴",
        patterns=[r"bank_account", r"bankcard", r"银行卡", r"卡号", r"account_number"],
        l0_action="SM4加密", l1_transport="SM4密文",
        l3_storage="SM3(原文)", log_action="MELTDOWN",
    ),
    SensitiveField(
        name="phone_number", level="🟡",
        patterns=[r"phone", r"mobile", r"手机", r"电话", r"tel"],
        l0_action="SM4加密", l1_transport="SM4密文",
        l3_storage="SM4密文", log_action="MELTDOWN",
    ),
    SensitiveField(
        name="real_name", level="🟡",
        patterns=[r"real_name", r"name", r"姓名", r"realname", r"full_name"],
        l0_action="SM4加密", l1_transport="SM4密文",
        l3_storage="SM4密文", log_action="MELTDOWN",
    ),
    SensitiveField(
        name="token", level="🔴",
        patterns=[r"token", r"jwt", r"access_token", r"bearer"],
        l0_action="已密文不处理", l1_transport="原样",
        l3_storage="不存(内存only)", log_action="MELTDOWN",
    ),
    SensitiveField(
        name="api_key", level="🔴",
        patterns=[r"api_key", r"apikey", r"api_secret", r"secret_key", r"private_key"],
        l0_action="不处理(本地only)", l1_transport="不传",
        l3_storage="不存", log_action="不记录",
    ),
    SensitiveField(
        name="gpg_private_key", level="🔴",
        patterns=[r"gpg_private", r"gnupg", r"gpg_key", r"pgp_key"],
        l0_action="不处理(本地only)", l1_transport="不传",
        l3_storage="不存", log_action="不记录",
    ),
    SensitiveField(
        name="wechat_openid", level="🟡",
        patterns=[r"openid", r"unionid", r"wechat_id", r"wx_id"],
        l0_action="SM3哈希", l1_transport="hex哈希",
        l3_storage="hex哈希", log_action="MELTDOWN",
    ),
    SensitiveField(
        name="face_data", level="🔴",
        patterns=[r"face", r"人脸", r"face_data", r"biometric", r"生物特征"],
        l0_action="前端处理不下传", l1_transport="不传",
        l3_storage="不存", log_action="不记录",
    ),
]

# 敏感值正则（检测值内容本身）
SENSITIVE_VALUE_PATTERNS: Dict[str, str] = {
    "id_card_18": r"\b[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b",
    "phone_cn": r"\b1[3-9]\d{9}\b",
    "bank_card": r"\b\d{16,19}\b",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
}

# ============================================
# 哈希工具
# ============================================

def sm3_hash(data: str, salt: Optional[str] = None) -> str:
    """
    SM3 国密哈希（降级使用 SHA3-256 作为等效替代）。
    生产环境应使用 gmssl 或 tongsuopy 的 SM3 实现。
    """
    if salt:
        data = data + salt
    return hashlib.sha3_256(data.encode("utf-8")).hexdigest()

def generate_salt(length: int = 32) -> str:
    """生成随机盐值"""
    return secrets.token_hex(length // 2)

def constant_time_compare(a: str, b: str) -> bool:
    """常数时间比较，防时序攻击"""
    return hmac.compare_digest(a.encode(), b.encode())

# ============================================
# 日志湮灭器 (L4)
# ============================================

MELTDOWN_MARKER = "***MELTDOWN***"

# 日志湮灭的字段名匹配
_LOG_SENSITIVE_KEYS = re.compile(
    r'(?:password|passwd|pwd|secret|密钥|token|api[_-]?key|private[_-]?key|'
    r'id[_-]?card|身份证|bank[_-]?account|银行卡|phone|mobile|手机|'
    r'openid|unionid|face[_-]?data|人脸|gpg[_-]?key)',
    re.IGNORECASE,
)

_LOG_SENSITIVE_VALUE_PATTERN = re.compile(
    r'(?:'
    r'(?:bearer\s+)?[\w-]{20,}'  # tokens
    r'|[\w]{32,}'                 # hex tokens
    r'|[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]'  # 身份证
    r'|1[3-9]\d{9}'              # 手机号
    r')',
)

def sanitize_log_line(line: str) -> Tuple[str, bool]:
    """
    清理日志行中的敏感信息。
    返回：(清理后的行, 是否做了修改)
    """
    original = line
    # 1. 字段名=值的模式
    line = re.sub(
        rf'({_LOG_SENSITIVE_KEYS.pattern})\s*[=:]\s*[^\s,;]+',
        rf'\1={MELTDOWN_MARKER}',
        line,
        flags=re.IGNORECASE,
    )
    # 2. JSON 中的敏感字段
    line = re.sub(
        rf'"{_LOG_SENSITIVE_KEYS.pattern}"\s*:\s*"([^"]*)"',
        rf'"\1": "{MELTDOWN_MARKER}"',
        line,
        flags=re.IGNORECASE,
    )
    # 3. 敏感值本身
    line = _LOG_SENSITIVE_VALUE_PATTERN.sub(MELTDOWN_MARKER, line)

    return line, (line != original)

def sanitize_log_text(text: str) -> Dict[str, Any]:
    """
    清理多行日志中的敏感信息。
    返回：{cleaned_text, meltdown_count, affected_lines}
    """
    lines = text.split("\n")
    result = []
    affected = []
    total = 0

    for i, line in enumerate(lines):
        cleaned, changed = sanitize_log_line(line)
        result.append(cleaned)
        if changed:
            affected.append(i + 1)
            total += line.count(MELTDOWN_MARKER) if cleaned != line else 1

    return {
        "cleaned_text": "\n".join(result),
        "meltdown_count": total,
        "affected_lines": affected,
    }

# ============================================
# 敏感数据检测器
# ============================================

@dataclass
class MeltdownFinding:
    """熔断发现"""
    field_name: str
    level: str
    layer: str    # L0/L1/L2/L3/L4
    detail: str
    position: int
    context: str

@dataclass
class DataMeltdownReport:
    """数据熔断审计报告"""
    status: str              # 🟢/🟡/🔴
    findings: List[MeltdownFinding] = field(default_factory=list)
    plaintext_detected: bool = False
    log_sanitized: bool = False
    meltdown_count: int = 0
    verdict: str = ""
    dna: str = "#龍芯⚡️丙午·丙申·丙辰·己丑·需-DATA-MELTDOWN-v1.0"

def detect_sensitive_fields(data: Dict[str, Any]) -> List[MeltdownFinding]:
    """
    检测数据字典中是否包含敏感字段明文。
    这是 L1 传输层检查——如果请求体中出现明文敏感字段，触发熔断。
    """
    findings = []

    for key, value in data.items():
        key_lower = key.lower()
        for field in SENSITIVE_FIELDS:
            for pattern in field.patterns:
                if re.search(pattern, key_lower, re.IGNORECASE):
                    # 检测值是否是明文（非哈希格式）
                    if isinstance(value, str):
                        is_hash = (
                            len(value) in (64, 128) and
                            re.match(r'^[a-fA-F0-9]+$', value)
                        )
                        is_sm4 = (
                            len(value) > 32 and
                            not re.match(r'^[a-fA-F0-9]+$', value)
                        )
                        if not is_hash and not is_sm4:
                            findings.append(MeltdownFinding(
                                field_name=field.name,
                                level=field.level,
                                layer="L1·传输黑洞",
                                detail=f"请求体中发现明文敏感字段 '{key}'，"
                                       f"应为 {field.l1_transport}",
                                position=0,
                                context=f"{key}: {value[:10]}...",
                            ))

    return findings

def detect_value_leaks(text: str) -> List[MeltdownFinding]:
    """
    检测文本中是否泄露了敏感数据值（身份证号、手机号等）。
    这是 L4 日志层检查。
    """
    findings = []
    for leak_type, pattern in SENSITIVE_VALUE_PATTERNS.items():
        for match in re.finditer(pattern, text):
            findings.append(MeltdownFinding(
                field_name=leak_type,
                level="🔴",
                layer="L4·日志湮灭",
                detail=f"日志中发现疑似 {leak_type} 明文",
                position=match.start(),
                context=match.group(),
            ))
    return findings

def scan_request_body(body: Dict[str, Any]) -> DataMeltdownReport:
    """
    完整扫描：检查请求体+值泄露。
    返回 DataMeltdownReport。
    """
    findings = []

    # L1 检查
    field_findings = detect_sensitive_fields(body)
    findings.extend(field_findings)

    # L4 检查（如果请求体转成字符串会泄露）
    body_str = json.dumps(body, ensure_ascii=False)
    value_findings = detect_value_leaks(body_str)
    findings.extend(value_findings)

    has_plaintext = any(
        f.layer == "L1·传输黑洞" for f in findings
    )

    red_count = sum(1 for f in findings if f.level == "🔴")
    yellow_count = sum(1 for f in findings if f.level == "🟡")

    if red_count > 0:
        status = "🔴 熔断"
        verdict = "检测到明文敏感数据，立即拒绝处理"
    elif yellow_count > 0:
        status = "🟡 待审"
        verdict = "检测到中敏数据，需人工确认处理方式"
    else:
        status = "🟢 通过"
        verdict = "未检测到明文敏感数据"

    return DataMeltdownReport(
        status=status,
        findings=findings,
        plaintext_detected=has_plaintext,
        verdict=verdict,
        meltdown_count=len(findings),
    )

# ============================================
# 内存瞬态辅助 (L2)
# ============================================

class MemoryGuard:
    """
    L2 内存瞬态辅助 —— 上下文管理器，确保退出时变量被清理。

    用法：
        with MemoryGuard() as guard:
            password = guard.register("password", user_input)
            # process...
        # password 已被置 None
    """
    def __init__(self):
        self._vars: Dict[str, Any] = {}

    def register(self, name: str, value: Any) -> Any:
        """注册敏感变量"""
        self._vars[name] = value
        return value

    def __enter__(self):
        return self

    def __exit__(self, *args):
        import gc
        for name in list(self._vars.keys()):
            value = self._vars.pop(name, None)
            if isinstance(value, (str, bytes, bytearray)):
                # 覆写字符串内容
                try:
                    if isinstance(value, bytearray):
                        value[:] = b'\x00' * len(value)
                except Exception:
                    pass
            del value
        self._vars.clear()
        gc.collect()

def recommend_memory_cleanup() -> str:
    """返回 L2 内存清理建议代码片段"""
    return """
# L2 内存瞬态 — 嵌入你的处理代码中
import gc

# 1. 处理前：只在临时变量中
password_input = request.json.get("password")

# 2. 处理：立即哈希
password_hash = sm3_hash(password_input, salt)

# 3. 处理后：立即清理
password_input = None
gc.collect()

# 明文生命周期: 从获取到哈希完成，通常 < 10ms
"""

# ============================================
# 存储层断言 (L3)
# ============================================

STORAGE_FORBIDDEN_PATTERNS = [
    (r"INSERT.*password.*VALUES.*(?![MELTDOWN])", "禁止明文密码入库"),
    (r"INSERT.*id_card.*VALUES.*\d{15,18}", "禁止明文身份证号入库"),
    (r"INSERT.*phone.*VALUES.*1[3-9]\d{9}", "禁止明文手机号入库"),
]

def audit_storage_sql(sql: str) -> List[MeltdownFinding]:
    """审计 SQL 语句中的敏感数据存储"""
    findings = []
    for pattern, detail in STORAGE_FORBIDDEN_PATTERNS:
        for match in re.finditer(pattern, sql, re.IGNORECASE):
            findings.append(MeltdownFinding(
                field_name="storage_audit",
                level="🔴",
                layer="L3·存储拒绝",
                detail=detail,
                position=match.start(),
                context=match.group()[:80],
            ))
    return findings

# ============================================
# CLI
# ============================================

def print_report(report: DataMeltdownReport, verbose: bool = False):
    """打印审计报告"""
    print()
    print("╔══════════════════════════════════════╗")
    print("║   🕳️  龍魂数据黑洞熔断审计报告       ║")
    print("╚══════════════════════════════════════╝")
    print()
    print(f"  判定：{report.status}")
    print(f"  熔断发现：{report.meltdown_count} 处")
    print(f"  明文检测：{'是' if report.plaintext_detected else '否'}")
    print(f"  判决：{report.verdict}")
    print()

    if verbose and report.findings:
        print("  ── 详细发现 ──")
        for i, f in enumerate(report.findings, 1):
            print(f"  [{i}] {f.level} {f.layer} · {f.field_name}")
            print(f"      {f.detail}")
            if f.context:
                print(f"      上下文：{f.context[:60]}")
            print()

    print(f"  DNA：{report.dna}")
    print()

def main():
    parser = argparse.ArgumentParser(
        description="龍魂数据黑洞五层熔断引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="命令")

    # scan — 扫描 JSON 请求体
    scan_p = sub.add_parser("scan", help="扫描 JSON 请求体中的敏感数据")
    scan_p.add_argument("json_body", help="JSON 字符串")
    scan_p.add_argument("-v", "--verbose", action="store_true", help="详细输出")

    # sanitize-log — 清理日志
    sanitize_p = sub.add_parser("sanitize-log", help="清理日志中的敏感数据")
    sanitize_p.add_argument("log_text", help="日志文本")
    sanitize_p.add_argument("-f", "--file", action="store_true", help="从文件读取")

    # hash-password — SM3 哈希密码
    hash_p = sub.add_parser("hash-password", help="SM3 哈希密码（带盐）")
    hash_p.add_argument("password", help="明文密码")
    hash_p.add_argument("-s", "--salt", help="盐值（不提供则自动生成）")

    # check-field — 检查单个字段
    check_p = sub.add_parser("check-field", help="检查单个字段名是否为敏感字段")
    check_p.add_argument("field_name", help="字段名")

    args = parser.parse_args()

    if args.command == "scan":
        try:
            body = json.loads(args.json_body)
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {e}")
            sys.exit(1)
        report = scan_request_body(body)
        print_report(report, verbose=args.verbose)
        if report.status == "🔴 熔断":
            sys.exit(2)
        elif report.status == "🟡 待审":
            sys.exit(1)
        else:
            sys.exit(0)

    elif args.command == "sanitize-log":
        text = args.log_text
        if args.file:
            text = Path(args.log_text).read_text(encoding="utf-8")
        result = sanitize_log_text(text)
        print(result["cleaned_text"])
        if result["meltdown_count"] > 0:
            print(f"\n--- 已湮灭 {result['meltdown_count']} 处敏感数据 ---",
                  file=sys.stderr)
            print(f"受影响行: {result['affected_lines']}", file=sys.stderr)

    elif args.command == "hash-password":
        salt = args.salt or generate_salt()
        hashed = sm3_hash(args.password, salt)
        print(f"salt: {salt}")
        print(f"hash: {hashed}")

    elif args.command == "check-field":
        name = args.field_name.lower()
        for field in SENSITIVE_FIELDS:
            for pattern in field.patterns:
                if re.search(pattern, name, re.IGNORECASE):
                    print(f"🕳️  '{args.field_name}' 是敏感字段")
                    print(f"   类型: {field.name}")
                    print(f"   级别: {field.level}")
                    print(f"   L0处理: {field.l0_action}")
                    print(f"   L1传输: {field.l1_transport}")
                    print(f"   L3存储: {field.l3_storage}")
                    print(f"   L4日志: {field.log_action}")
                    return
        print(f"🟢 '{args.field_name}' 不在敏感字段清单中")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
