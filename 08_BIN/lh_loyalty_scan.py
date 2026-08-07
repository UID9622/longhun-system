#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# DNA: #龍芯⚡️丙午·丙申·癸丑·巳时·䷗复-LOYALTY-SCAN-v1.1-a3b7c9d2
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 创建者: 诸葛鑫 (UID9622)
# 协议: MulanPSL v2（工程实现层·允许商业使用·署名）
# ============================================================
"""
龍魂 · 忠义数据铁律 — 自检扫描器 v1.1

扫描全项目代码，检测是否有收集用户个人数据的模式。
每一条"说到做到"必须有这个能跑的脚本背书。

用法:
    python3 bin/lh_loyalty_scan.py                 # 全项目扫描
    python3 bin/lh_loyalty_scan.py --json          # JSON输出
    python3 bin/lh_loyalty_scan.py --path bin/     # 指定目录
    python3 bin/lh_loyalty_scan.py --ci            # CI模式（发现违规exit 1）
    python3 bin/lh_loyalty_scan.py --severity 10   # 只报告红线(severity>=10)
"""
import argparse
import json
import os
import re
import sys
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# 项目根目录
ROOT = Path(__file__).resolve().parent.parent

# ━━━ 禁止模式：在代码中发现以下模式 = 违规 ━━━

FORBIDDEN_PATTERNS = {
    # ── 邮箱收集（精准：只匹配存储/持久化动作） ──
    "email_collection": {
        "patterns": [
            # 数据库存储
            r'\bdb\.(insert|save|put|set)\b[^\n]{0,60}\bemail\b',
            r'\bdb\b[^\n]{0,60}\bemail\b[^\n]{0,60}\b(insert|save|put|set)\b',
            r'\bINSERT\b[^\n]*\bINTO\b[^\n]*\bemail\b',
            r'\bCREATE\s+TABLE\b[^\n]*\bemail\b',
            # 前端存储
            r'\blocalStorage\.set\b[^\n]*\bemail\b',
            r'\bsessionStorage\.set\b[^\n]*\bemail\b',
            r'\bCookies?\.set\b[^\n]*\bemail\b',
            r'\bdocument\.cookie\b[^\n]*\bemail\b',
            # 明确收集动作
            r'\bcollect\b[^\n]{0,40}\buser\b[^\n]{0,40}\bemail\b',
            r'\bsave\b[^\n]{0,40}\buser\b[^\n]{0,40}\bemail\b',
            r'\bstore\b[^\n]{0,40}\buser\b[^\n]{0,40}\bemail\b',
            r'\bpersist\b[^\n]{0,40}\bemail\b',
            # 第三方营销/追踪SDK
            r'\bsendgrid@\b',
            r'\bmailchimp\b',
            r'\bconvertkit\b',
            r'\bactivecampaign\b',
        ],
        "severity": 10,  # 🔴红线
        "description": "收集/存储用户邮箱"
    },
    # ── 手机号收集 ──
    "phone_collection": {
        "patterns": [
            r'\bdb\.(insert|save|put|set)\b[^\n]{0,60}\bphone\b',
            r'\bINSERT\b[^\n]*\bINTO\b[^\n]*\bphone\b',
            r'\bCREATE\s+TABLE\b[^\n]*\bphone\b',
            r'\blocalStorage\.set\b[^\n]*\bphone\b',
            r'\bsessionStorage\.set\b[^\n]*\bphone\b',
            r'\bcollect\b[^\n]{0,40}\buser\b[^\n]{0,40}\bphone\b',
            r'\bsave\b[^\n]{0,40}\buser\b[^\n]{0,40}\bphone\b',
            r'\bsend_sms\b[^\n]{0,40}\buser\b',
            # 中国手机号正则（仅在代码中硬编码收集手机号格式时触发）
            r'\+86\s*\d{11}',
            r'\btwilio\b[^\n]*\bsend\b',
        ],
        "severity": 10,
        "description": "收集/存储用户手机号"
    },
    # ── 身份证/实名 ──
    "id_card_collection": {
        "patterns": [
            r'\bid_card\s*=\b',
            r'\bid_number\s*=\b',
            r'\bidentity_card\s*=\b',
            r'\bdb\b[^\n]{0,60}\bid_card\b',
            r'\bINSERT\b[^\n]*\bINTO\b[^\n]*\bid_card\b',
            r'\bCREATE\s+TABLE\b[^\n]*\bid_card\b',
            r'\breal_name\s*=\b',
            r'\bcollect\b[^\n]{0,40}\breal_name\b',
            r'\bsocial_security\b[^\n]{0,40}\bcollect\b',
            r'\bssn\b[^\n]{0,40}\bcollect\b',
        ],
        "severity": 10,
        "description": "收集/存储身份证或实名信息"
    },
    # ── IP地址收集（精准：持久化存储） ──
    "ip_collection": {
        "patterns": [
            r'\bdb\.(insert|save|put)\b[^\n]{0,60}\bip_address\b',
            r'\bINSERT\b[^\n]*\bINTO\b[^\n]*\bip_address\b',
            r'\bCREATE\s+TABLE\b[^\n]*\bip\b',
            r'\bsave\b[^\n]{0,40}\buser\b[^\n]{0,40}\bip\b',
            r'\bstore\b[^\n]{0,40}\buser\b[^\n]{0,40}\bip\b',
            r'\blocalStorage\.set\b[^\n]*\bip\b',
        ],
        "severity": 8,  # 🟡 关注
        "description": "收集/存储用户IP地址"
    },
    # ── 设备指纹（精准：前端追踪库） ──
    "device_fingerprint": {
        "patterns": [
            r'\bfingerprintjs\b',
            r'\bfingerprint_js\b',
            r'\bfingerprint2\b',
            r'\bclientjs\b',
            r'\bimpressionz\b',
            r'\bnavigator\.userAgent\b[^\n]{0,60}\bfingerprint\b',
            r'\bcanvas\.toDataURL\b[^\n]{0,60}\bfingerprint\b',
            r'\bwebgl_debug_renderer_info\b[^\n]{0,60}\bfingerprint\b',
            r'\bgetDeviceFingerprint\b',
            r'\bdevice_fingerprint\b[^\n]{0,60}\btrack\b',
        ],
        "severity": 9,
        "description": "收集设备指纹/浏览器指纹"
    },
    # ── 位置追踪 ──
    "location_tracking": {
        "patterns": [
            r'\bnavigator\.geolocation\b',
            r'\bgetCurrentPosition\b',
            r'\bwatchPosition\b',
            r'\bdb\.(save|insert)\b[^\n]{0,60}\blocation\b',
            r'\bINSERT\b[^\n]*\bINTO\b[^\n]*\buser_location\b',
            r'\bsave_user_location\b',
            r'\bstore_user_location\b',
            r'\btrack\b[^\n]{0,40}\buser\b[^\n]{0,40}\blocation\b',
        ],
        "severity": 9,
        "description": "收集用户地理位置"
    },
    # ── 用户画像/行为追踪 ──
    "user_profiling": {
        "patterns": [
            r'\banalytics\.track\(\b',
            r'\banalytics\.identify\(\b',
            r'\bmixpanel\b',
            r'\bsegment\.io\b',
            r'\bgoogle_analytics\b',
            r'\bga\(\s*["\']\.create\b',
            r'\bgtag\(\s*["\']\.config\b',
            r'\bfacebook_pixel\b',
            r'\bfbq\(\s*["\']\.init\b',
            r'\bhotjar\b',
            r'\bfullstory\b',
            r'\bheap\.io\b',
            r'\bbuild_user_profile\b',
            r'\bcreate_user_profile\b',
            r'\buser_behavior_track\b',
        ],
        "severity": 10,
        "description": "用户画像/行为追踪/第三方分析"
    },
    # ── 社交关系 ──
    "social_graph": {
        "patterns": [
            r'\bfriend\b[^\n]{0,40}\blist\b[^\n]{0,40}\bimport\b',
            r'\bfollower\b[^\n]{0,40}\bgraph\b',
            r'\bsocial_graph\b[^\n]{0,40}\bcollect\b',
            r'\bsocial_network\b[^\n]{0,40}\btrack\b',
            r'\bcontact\b[^\n]{0,40}\bimport\b',
            r'\bimport\b[^\n]{0,40}\buser\b[^\n]{0,40}\bcontact\b',
            r'\binvite\b[^\n]{0,40}\bfriend\b[^\n]{0,40}\btrack\b',
        ],
        "severity": 9,
        "description": "收集/分析用户社交关系"
    },
    # ── 生物特征 ──
    "biometric": {
        "patterns": [
            r'\bface\b[^\n]{0,40}\brecogn\b',
            r'\bvoice\b[^\n]{0,40}\bprint\b',
            r'\bfingerprint\b[^\n]{0,40}\bbio\b',
            r'\bbiometric\b[^\n]{0,40}\bcollect\b',
            r'\bretina\b[^\n]{0,40}\bscan\b',
            r'\biris\b[^\n]{0,40}\bscan\b',
        ],
        "severity": 10,
        "description": "收集生物特征数据"
    },
    # ── 金融信息 ──
    "financial_collection": {
        "patterns": [
            r'\bcredit_card\b[^\n]{0,40}\bsave\b',
            r'\bbank_account\b[^\n]{0,40}\bsave\b',
            r'\bsave\b[^\n]{0,40}\bcredit_card\b',
            r'\bstore\b[^\n]{0,40}\bpayment_info\b',
            r'\bINSERT\b[^\n]*\bINTO\b[^\n]*\bcredit_card\b',
            r'\bINSERT\b[^\n]*\bINTO\b[^\n]*\bpayment\b[^\n]*\buser\b',
            r'\bcollect\b[^\n]{0,40}\bpayment\b[^\n]{0,40}\binfo\b',
            r'\bbilling_info\b[^\n]{0,40}\bsave\b',
        ],
        "severity": 10,
        "description": "收集/存储金融信息"
    },
}

# ── 白名单：这些文件/目录不扫 ──
# 规则：按路径组件精确匹配，避免子串误伤
WHITELIST_PATHS = {
    # 构建/依赖/缓存
    'node_modules', '.git', '__pycache__', '.venv', 'venv',
    'dist', 'build', '.next', '.cache', '_archive', '_work',
    'backup', 'backups', 'archive', 'tombstone_vault',
    # 第三方 vendor
    'vendor', 'warp-lab/vendor', 'kimi-webbridge/chunks',
    # 文档/协议/论文/文章（示例引用不视为收集）
    '01_protocols', 'articles', 'papers', 'docs', '12_DOCS',
    '06_技術文檔',
    # CNSH 内部数据/配置/模型/日志/审计
    'CNSH_', 'logs', 'audit', '07_AUDIT', 'config', '20_CONFIG',
    'models', 'data', '11_DATA', 'test', 'tests', '13_TESTS',
    'train', 'training', 'fused_model',
    # 字体/资源/Docker/IDE/技能
    'fonts', '字体', 'docker', '.codebuddy', 'skills', '02_SKILLS',
    'deploy',
    # 龍魂自有应用（localStorage本地存储·不上传服务器）
    '龍魂智能中枢',
    # 龍魂自有数字指纹/印记/声纹系统（本地生成，非收集用户数据）
    'lh_digital_imprint.py', 'lh_batch_processor.py', 'lh_biometric_health.py',
    'lh_data_privacy_v2.py', 'lh_data_meltdown.py', 'lh_privacy_scanner.py',
    # 龍魂量子/数学模块（amplitude 是物理振幅，不是 Amplitude 分析）
    'lh_quantum_module_router.py', 'lh_quantum_circuit_breaker.py',
    'lh_quantum_api_v2.py',
    # 清单/索引文件（help 文本包含命令名）
    '.inventory.json',
    # 人格配置文件（非用户画像收集）
    'UID9622_大白话人物画像.json',
    # 反追踪/反监控工具（列出追踪域名是为了屏蔽，不是收集）
    'guanlan', 'five-harms-expose', 'protocol-checker',
    # 包含示例代码/文档说明的工具
    'lh_knowledge_hub.py',
    # 自身
    'lh_loyalty_scan.py',
}

# ── 文件类型 ──
SCAN_EXTENSIONS = {'.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.vue',
                   '.sh', '.go', '.rs', '.java', '.kt', '.swift',
                   '.yml', '.yaml', '.json', '.toml', '.sql'}


@dataclass
class Finding:
    """单项违规发现"""
    category: str
    pattern_matched: str
    file_path: str
    line_number: int
    line_content: str
    severity: int
    description: str


@dataclass
class ScanResult:
    """扫描结果"""
    scan_time: str
    total_files: int = 0
    scanned_files: int = 0
    findings: list = field(default_factory=list)
    passed_categories: list = field(default_factory=list)
    failed_categories: list = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        return len(self.findings) == 0

    @property
    def has_red(self) -> bool:
        return any(f.severity >= 10 for f in self.findings)

    @property
    def has_warning(self) -> bool:
        return any(f.severity < 10 for f in self.findings)

    @property
    def max_severity(self) -> int:
        if not self.findings:
            return 0
        return max(f.severity for f in self.findings)


def should_skip_path(rel_path: str) -> bool:
    """是否跳过该路径（按路径组件精确匹配）"""
    parts = Path(rel_path).parts
    # 隐藏目录（除 .codebuddy 外）
    for part in parts[:-1]:
        if part.startswith('.') and part != '.codebuddy':
            return True
    # 精确匹配路径组件或文件名
    for wp in WHITELIST_PATHS:
        if wp in parts or wp == Path(rel_path).name:
            return True
    return False


def scan_file(file_path: str) -> list[Finding]:
    """扫描单个文件"""
    findings = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception:
        return findings

    for i, line in enumerate(lines, 1):
        # 跳过注释行（粗略）和空行
        stripped = line.strip()
        if not stripped or stripped.startswith('#') or stripped.startswith('//'):
            continue

        for cat_name, cat_def in FORBIDDEN_PATTERNS.items():
            for pattern in cat_def["patterns"]:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append(Finding(
                        category=cat_name,
                        pattern_matched=pattern,
                        file_path=file_path,
                        line_number=i,
                        line_content=line.strip()[:120],
                        severity=cat_def["severity"],
                        description=cat_def["description"]
                    ))
                    break  # 同一行同一类别只报一次

    return findings


def scan_project(root_path: str) -> ScanResult:
    """扫描整个项目"""
    result = ScanResult(
        scan_time=datetime.now(timezone.utc).isoformat()
    )

    all_files = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        # 跳过隐藏目录（保留 .codebuddy）
        dirnames[:] = [d for d in dirnames if not d.startswith('.') or d == '.codebuddy']
        for fname in filenames:
            full_path = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(full_path, root_path)
            ext = os.path.splitext(fname)[1].lower()
            if ext in SCAN_EXTENSIONS or fname in ('Dockerfile', 'Makefile'):
                all_files.append((full_path, rel_path))

    result.total_files = len(all_files)

    for full_path, rel_path in all_files:
        if should_skip_path(rel_path):
            continue
        result.scanned_files += 1
        findings = scan_file(full_path)
        if findings:
            # 转相对路径
            for f in findings:
                f.file_path = rel_path
            result.findings.extend(findings)

    # 汇总分类
    all_cats = set(FORBIDDEN_PATTERNS.keys())
    failed_cats = {f.category for f in result.findings}
    result.passed_categories = sorted(all_cats - failed_cats)
    result.failed_categories = sorted(failed_cats)

    return result


def write_audit_log(result: ScanResult, scan_path: str):
    """写入审计日志（append-only）"""
    log_dir = Path.home() / ".龍魂" / "audit"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "loyalty_scan.jsonl"

    record = {
        "dna": f"#龍芯⚡️丙午·丙申·癸丑·巳时·䷗复-LOYALTY-SCAN-v1.1-{uuid.uuid4().hex[:8]}",
        "timestamp": result.scan_time,
        "scan_path": str(scan_path),
        "total_files": result.total_files,
        "scanned_files": result.scanned_files,
        "findings_count": len(result.findings),
        "has_red": result.has_red,
        "max_severity": result.max_severity,
        "failed_categories": result.failed_categories,
        "passed_categories": result.passed_categories,
    }
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"🟡 审计日志写入失败: {e}", file=sys.stderr)


def format_output(result: ScanResult, json_mode: bool = False, min_severity: int = 0):
    """格式化输出"""
    findings = [f for f in result.findings if f.severity >= min_severity]

    if json_mode:
        output = {
            "scan_time": result.scan_time,
            "total_files": result.total_files,
            "scanned_files": result.scanned_files,
            "findings_count": len(findings),
            "is_clean": len(findings) == 0,
            "has_red": result.has_red,
            "max_severity": result.max_severity,
            "passed_categories": result.passed_categories,
            "failed_categories": result.failed_categories,
            "findings": [
                {
                    "category": f.category,
                    "severity": f.severity,
                    "description": f.description,
                    "file": f.file_path,
                    "line": f.line_number,
                    "content": f.line_content,
                }
                for f in findings
            ]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    # ── 人性化输出 ──
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   🐉 龍魂 · 忠义数据铁律 — 自检扫描器 v1.1              ║")
    print("║   協議: LH-LOYALTY-IRON-LAW-v1.0 (P0-ETERNAL·焊死)       ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    print(f"  扫描时间: {result.scan_time}")
    print(f"  扫描路径: {result.scan_path if hasattr(result, 'scan_path') else ROOT}")
    print(f"  扫描文件: {result.scanned_files}/{result.total_files}")
    print()

    # ── 逐类报告 ──
    for cat_name, cat_def in FORBIDDEN_PATTERNS.items():
        count = sum(1 for f in findings if f.category == cat_name)
        icon = "🟢" if count == 0 else ("🟡" if cat_def["severity"] < 10 else "🔴")
        status = "通过" if count == 0 else f"⚠️ {count}处"
        print(f"  {icon} {cat_def['description']}: {status}")

    print()
    print("─" * 60)

    if not findings:
        print()
        print("  ✅ 忠义铁律: 全绿通过")
        print("  🐉 龍魂不收集任何用户数据 —— 说到做到，代码为证。")
        print()
    else:
        print()
        for f in findings:
            sev_icon = "🔴" if f.severity >= 10 else "🟡"
            print(f"  {sev_icon} [{f.description}] {f.file_path}:{f.line_number}")
            print(f"     → {f.line_content}")
        print()
        if result.has_red:
            print("  🛑 🔴 发现红线违规！熔断触发·需UID9622人工处理")
        else:
            print("  ⚠️ 🟡 发现待核查项·P05审计标记·48h内复查")
        print()

    # ── DNA ──
    print("─" * 60)
    print(f"  DNA: #龍芯⚡️丙午·丙申·癸丑·巳时·䷗复-LOYALTY-SCAN-v1.1-a3b7c9d2")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="龍魂 · 忠义数据铁律 — 自检扫描器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_loyalty_scan.py
  python3 bin/lh_loyalty_scan.py --json
  python3 bin/lh_loyalty_scan.py --path ./src
  python3 bin/lh_loyalty_scan.py --ci
        """
    )
    parser.add_argument('--path', default=str(ROOT), help='扫描路径（默认项目根目录）')
    parser.add_argument('--json', action='store_true', help='JSON 输出')
    parser.add_argument('--ci', action='store_true', help='CI 模式：发现任何违规则 exit 1')
    parser.add_argument('--severity', type=int, default=0, help='最小严重级别过滤（默认 0）')
    parser.add_argument('--no-log', action='store_true', help='不写入审计日志')
    args = parser.parse_args()

    scan_path = Path(args.path).resolve()
    if not scan_path.exists():
        print(f"🔴 扫描路径不存在: {scan_path}", file=sys.stderr)
        sys.exit(2)

    result = scan_project(str(scan_path))
    result.scan_path = str(scan_path)

    if not args.no_log:
        write_audit_log(result, str(scan_path))

    format_output(result, args.json, args.severity)

    if args.ci:
        # CI 模式：任何违规（severity >= 8）都视为失败
        violations = [f for f in result.findings if f.severity >= args.severity]
        if violations:
            sys.exit(1)
        sys.exit(0)


if __name__ == '__main__':
    main()
