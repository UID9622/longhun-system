#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·系统安全加固引擎 v1.0 — P0++焊死 — 每次启动自动运行
────────────────────────────────────────────
DNA: #龍芯⚡️2026-07-21-SYSTEM-HARDENER-V1.0-P0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能:
  1. 扫描全系统危险调用 (shell=True/os.popen/eval/exec)
  2. 检测凭据泄露 (硬编码密钥/密码/Token)
  3. 验证.gitignore完整性
  4. 审计安全封装器是否被绕过
  5. 检查CREDENTIAL_REGISTRY脱敏状态

用法:
  python3 bin/lh_system_hardener.py scan     # 审计扫描
  python3 bin/lh_system_hardener.py patch    # 自动修复（仅安全操作）
  python3 bin/lh_system_hardener.py validate # 验证所有补丁状态
────────────────────────────────────────────────
"""

import sys
import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Set, Tuple

# ═══════════════════════════════════════════
PROJECT = Path(__file__).resolve().parents[1]
DNA = '#龍芯⚡️2026-07-21-SYSTEM-HARDENER-V1.0-P0'

# ═══════════════════════════════════════════
# 检测规则
# ═══════════════════════════════════════════

# 危险函数模式
DANGEROUS_CALLS = [
    (r'\bshell\s*=\s*True\b', 'subprocess(shell=True)', '🔴', '命令注入入口'),
    (r'\bos\.popen\s*\(', 'os.popen()', '🔴', '命令注入入口'),
    (r'\beval\s*\(\s*', 'eval()', '🔴', '代码注入入口'),
    (r'\bexec\s*\(\s*', 'exec()', '🔴', '代码注入入口'),
    (r'\bsubprocess\.call\s*\(.*shell\s*=', 'subprocess.call(shell=)', '🟡', '可疑子进程'),
    (r'\bos\.system\s*\(', 'os.system()', '🔴', '命令注入入口'),
]

# 凭据泄漏模式
CREDENTIAL_LEAK = [
    (r'(?:password|passwd|secret)\s*[:=]\s*["\'](?!SHA256|HASH[:=]|已脱敏|\*{3}MELTDOWN|example|placeholder|your-|changeme)[^\'"]{4,}', '明文密码', '🔴'),
    (r'(?:api_?key|token|sk-)[\s:=]*["\'](?!SHA256|HASH|已脱敏|example|placeholder)[^\'"]{8,}', '明文API Key/Token', '🔴'),
    (r'ghp_[A-Za-z0-9]{36}', 'GitHub PAT', '🔴'),
    (r'glpat-[A-Za-z0-9_-]{20,}', 'GitLab PAT', '🔴'),
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key', '🔴'),
    (r'(?<!\d)1[3-9]\d{9}(?!\d)', '中国手机号', '🟡'),  # 仅告警，需要人工确认是否是合理使用
    (r'-----BEGIN\s+(RSA|EC|DSA|OPENSSH)\s+PRIVATE\s+KEY', '私钥明文', '🔴 L1'),
]

# 文件扩展名扫描范围
SCAN_EXTS = {'.py', '.sh', '.json', '.yaml', '.yml', '.toml', '.conf', '.cfg', '.env', '.ini'}

# 排除目录
EXCLUDE_DIRS = {
    'node_modules', 'venv', '__pycache__', '.git', '.codebuddy',
    'models', 'logs', 'backups', '_archive', 'tombstone_vault',
    'vector_db', 'data/sources', 'releases', 'dist', '.cursor',
    'container_data', 'logging_backup', 'var',
}

# 必须存在于.gitignore的模式
REQUIRED_GITIGNORE = [
    '*.env', '*.pem', '*.key', '*.p12', '*.pfx',
    'id_rsa*', 'id_ed25519*', '*private*', '*secret*',
    '*credential*', '*password*', '_private/', 'vault/',
]


class SystemHardener:
    """系统安全加固引擎"""

    def __init__(self):
        self.issues: List[Dict] = []
        self.stats = {'scanned_files': 0, 'issues': 0, 'fixed': 0}

    def _should_scan(self, fpath: Path) -> bool:
        """判断文件是否需要扫描"""
        if fpath.suffix not in SCAN_EXTS:
            return False
        rel = str(fpath.relative_to(PROJECT))
        for excl in EXCLUDE_DIRS:
            if excl in rel:
                return False
        # 跳过二进制/大文件/损坏的软链接
        try:
            if fpath.stat().st_size > 1_000_000:  # 1MB
                return False
        except (FileNotFoundError, PermissionError):
            return False
        return True

    def scan_dangerous_calls(self) -> List[Dict]:
        """扫描危险函数调用"""
        findings = []
        for pyfile in PROJECT.rglob('*.py'):
            if not self._should_scan(pyfile):
                continue
            self.stats['scanned_files'] += 1
            try:
                content = pyfile.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue

            rel_path = str(pyfile.relative_to(PROJECT))
            for pattern, name, severity, desc in DANGEROUS_CALLS:
                for m in re.finditer(pattern, content):
                    line_no = content[:m.start()].count('\n') + 1
                    line = content.split('\n')[line_no - 1].strip()[:120]
                    # 跳过注释和字符串内的防模式引用
                    code_before = content[:m.start()].split('\n')[-1]
                    if code_before.strip().startswith('#'):
                        continue
                    findings.append({
                        'file': rel_path, 'line': line_no, 'code': line,
                        'pattern': name, 'severity': severity, 'desc': desc,
                    })

        return findings

    def scan_credential_leaks(self) -> List[Dict]:
        """扫描凭据泄漏"""
        findings = []
        # 只检查非bin/目录的json/yaml等配置文件
        for ext in {'.json', '.yaml', '.yml', '.toml', '.conf', '.cfg', '.env', '.ini'}:
            for cfgfile in PROJECT.rglob(f'*{ext}'):
                if not self._should_scan(cfgfile):
                    continue
                try:
                    content = cfgfile.read_text(encoding='utf-8', errors='ignore')
                except Exception:
                    continue
                rel_path = str(cfgfile.relative_to(PROJECT))

                for pattern, name, severity in CREDENTIAL_LEAK:
                    for m in re.finditer(pattern, content):
                        line_no = content[:m.start()].count('\n') + 1
                        # 特殊处理手机号：仅在配置文件中告警
                        if '手机号' in name and ext not in {'.json', '.yaml', '.yml', '.toml', '.env', '.cfg', '.ini'}:
                            continue
                        findings.append({
                            'file': rel_path, 'line': line_no,
                            'pattern': name, 'severity': severity,
                            'match': m.group()[:40].replace('\n', ''),
                        })

        # 单独检查 CREDENTIAL_REGISTRY.json 是否脱敏
        cred_file = PROJECT / 'config' / 'CREDENTIAL_REGISTRY.json'
        if cred_file.exists():
            try:
                cred_content = cred_file.read_text()
            except Exception:
                cred_content = ''
            if re.search(r'1[3-9]\d{9}', cred_content):
                findings.append({
                    'file': 'config/CREDENTIAL_REGISTRY.json',
                    'line': 0, 'pattern': '未脱敏手机号',
                    'severity': '🔴', 'match': 'CREDENTIAL_REGISTRY.json 包含明文手机号',
                })
            if re.search(r'(HPUAS|LTAI|AKIA)[A-Z0-9]{16,}', cred_content):
                findings.append({
                    'file': 'config/CREDENTIAL_REGISTRY.json',
                    'line': 0, 'pattern': '未脱敏AK ID',
                    'severity': '🔴', 'match': 'CREDENTIAL_REGISTRY.json 包含明文AK ID',
                })

        return findings

    def scan_gitignore(self) -> List[Dict]:
        """验证 .gitignore 完整性"""
        findings = []
        gitignore = PROJECT / '.gitignore'
        if not gitignore.exists():
            return [{'file': '.gitignore', 'severity': '🔴', 'pattern': 'MISSING', 'desc': '.gitignore 不存在'}]

        content_lines = set(
            line.strip() for line in gitignore.read_text().split('\n')
            if line.strip() and not line.strip().startswith('#')
        )

        for required in REQUIRED_GITIGNORE:
            found = any(
                req_line == required
                or re.fullmatch(required.replace('*', '.*'), req_line)
                for req_line in content_lines
            )
            if not found:
                findings.append({
                    'file': '.gitignore',
                    'severity': '🟡',
                    'pattern': 'MISSING_RULE',
                    'desc': f'缺少关键规则: {required}',
                })

        return findings

    def scan_shell_bypass(self) -> List[Dict]:
        """检测安全封装器是否被绕过（直接使用subprocess.run而不导入safe_run）"""
        findings = []
        for pyfile in PROJECT.rglob('*.py'):
            if not self._should_scan(pyfile):
                continue
            rel = str(pyfile.relative_to(PROJECT))
            # 跳过安全封装器自身
            if 'lh_secure_subprocess' in rel or 'lh_system_hardener' in rel:
                continue

            try:
                content = pyfile.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue

            has_shell_true = re.search(r'\bshell\s*=\s*True\b', content)
            has_safe_import = 'lh_secure_subprocess' in content

            if has_shell_true and not has_safe_import:
                line_no = content[:has_shell_true.start()].count('\n') + 1
                findings.append({
                    'file': rel, 'line': line_no,
                    'severity': '🔴', 'pattern': 'SHELL_BYPASS',
                    'desc': '发现 shell=True 但未导入安全封装器',
                })

        return findings

    def run_scan(self) -> Dict:
        """执行全量扫描"""
        all_findings = {
            'dangerous_calls': self.scan_dangerous_calls(),
            'credential_leaks': self.scan_credential_leaks(),
            'gitignore_gaps': self.scan_gitignore(),
            'shell_bypass': self.scan_shell_bypass(),
        }

        total_issues = sum(len(v) for v in all_findings.values())
        self.stats['issues'] = total_issues

        return {
            'dna': DNA,
            'scan_time': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'stats': {
                'scanned_files': self.stats['scanned_files'],
                'total_issues': total_issues,
                'by_category': {k: len(v) for k, v in all_findings.items()},
            },
            'findings': all_findings,
            'status': '🔴 CRITICAL' if total_issues > 0 else '🟢 CLEAN',
        }

    def auto_patch(self) -> Dict:
        """自动修复（仅安全操作）"""
        fixed = []

        # 1. 确保 .gitignore 关键规则存在
        gitignore = PROJECT / '.gitignore'
        if gitignore.exists():
            content = gitignore.read_text()
            new_rules = []
            for rule in REQUIRED_GITIGNORE:
                if rule not in content:
                    new_rules.append(rule)
            if new_rules:
                gitignore.write_text(
                    content.rstrip() + '\n\n# 🔒 安全加固自动添加\n' + '\n'.join(new_rules) + '\n'
                )
                fixed.append(f'gitignore: added {len(new_rules)} security rules')

        # 2. 确保 logs/ 目录存在（用于审计日志）
        (PROJECT / 'logs').mkdir(parents=True, exist_ok=True)

        # 3. 确保 _private/ 目录存在（用于敏感数据隔离）
        (PROJECT / '_private').mkdir(parents=True, exist_ok=True)

        self.stats['fixed'] = len(fixed)
        return {
            'dna': DNA,
            'fixed': fixed,
            'fixed_count': len(fixed),
        }


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print(f'用法: python3 {sys.argv[0]} scan|patch|validate')
        sys.exit(1)

    cmd = sys.argv[1]
    h = SystemHardener()

    if cmd == 'scan':
        result = h.run_scan()
        print(f'\n═══════════════════════════════════════')
        print(f'  🔍 龍魂·系统安全审计')
        print(f'  DNA: {DNA}')
        print(f'═══════════════════════════════════════')
        print(f'  扫描文件: {result["stats"]["scanned_files"]}')
        print(f'  发现问题: {result["stats"]["total_issues"]}')
        print(f'  状态: {result["status"]}')
        print(f'═══════════════════════════════════════\n')

        for cat, items in result['findings'].items():
            if items:
                print(f'── {cat} ({len(items)}) ──')
                for item in items[:15]:  # 最多显示15条
                    sev = item.get('severity', '🟡')
                    f = item.get('file', '?')
                    ln = item.get('line', 0)
                    p = item.get('pattern', item.get('desc', ''))
                    print(f'  {sev} {f}:{ln} | {p}')
                if len(items) > 15:
                    print(f'  ... 另外 {len(items)-15} 条（详见JSON输出）')
                print()

        # JSON 完整输出
        json_output = PROJECT / 'logs' / 'security_scan.json'
        json_output.parent.mkdir(parents=True, exist_ok=True)
        json_output.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        print(f'完整报告: {json_output}')

    elif cmd == 'patch':
        result = h.auto_patch()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == 'validate':
        # 验证关键补丁是否生效
        checks = {}

        # 检查 CREDENTIAL_REGISTRY 脱敏
        cred_file = PROJECT / 'config' / 'CREDENTIAL_REGISTRY.json'
        if cred_file.exists():
            cred = cred_file.read_text()
            has_phone = bool(re.search(r'(?<!\d)1[3-9]\d{9}(?!\d)', cred))
            has_akid = bool(re.search(r'(HPUAS|LTAI|AKIA)[A-Z0-9]{16,}', cred))
            checks['PII脱敏'] = not has_phone and not has_akid

        # 检查安全封装器存在
        checks['安全子进程封装器'] = (PROJECT / 'bin' / 'lh_secure_subprocess.py').exists()

        # 检查本加固器存在
        checks['系统加固引擎'] = (PROJECT / 'bin' / 'lh_system_hardener.py').exists()

        # 检查.gitignore
        gi = PROJECT / '.gitignore'
        if gi.exists():
            content = gi.read_text()
            checks['gitignore(env)'] = '*.env' in content
            checks['gitignore(pem)'] = '*.pem' in content
            checks['gitignore(key)'] = '*.key' in content

        all_ok = all(checks.values())
        print(json.dumps({
            'dna': DNA,
            'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'status': '🟢 全部通过' if all_ok else '🟡 存在问题',
            'checks': checks,
            'passed': sum(1 for v in checks.values() if v),
            'total': len(checks),
        }, ensure_ascii=False, indent=2))
        sys.exit(0 if all_ok else 1)

    else:
        print(f'未知命令: {cmd}')
        sys.exit(1)


if __name__ == '__main__':
    main()
