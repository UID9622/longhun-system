#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂 DNA 協議 · Secret Guard v1.0
敏感信息檢測與脫敏系統

DNA:#龍芯⚡️2026-06-07-SECRET-GUARD-v1.0
責任: UID9622 · 不免責
"""

import re
import logging
from pathlib import Path
from typing import List, Dict, Set, Optional
from dataclasses import dataclass
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        return iterable


# ============================================================================
# [日誌配置]
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# [敏感信息類型]
# ============================================================================

class SecretType(Enum):
    """敏感信息類型枚舉"""
    API_KEY = "api_key"
    AWS_KEY = "aws_key"
    GITHUB_TOKEN = "github_token"
    PRIVATE_KEY = "private_key"
    PASSWORD = "password"
    ENV_VAR = "env_var"
    DATABASE_URL = "database_url"
    SLACK_TOKEN = "slack_token"
    JWT_TOKEN = "jwt_token"
    GENERIC_SECRET = "generic_secret"


# ============================================================================
# [敏感信息檢測模式]
# ============================================================================

DETECTION_PATTERNS = {
    SecretType.API_KEY: re.compile(
        r'(api[_-]?key|apikey|api_token)\s*[:=]\s*["\']?[a-zA-Z0-9_\-]{20,}',
        re.IGNORECASE
    ),
    SecretType.AWS_KEY: re.compile(
        r'AKIA[0-9A-Z]{16}'
    ),
    SecretType.GITHUB_TOKEN: re.compile(
        r'ghp_[a-zA-Z0-9]{36}|gho_[a-zA-Z0-9]{36}|ghu_[a-zA-Z0-9]{36}'
    ),
    SecretType.PRIVATE_KEY: re.compile(
        r'-----BEGIN\s+(RSA|DSA|EC|OPENSSH)\s+PRIVATE\s+KEY[^-]*-----'
    ),
    SecretType.PASSWORD: re.compile(
        r'(password|passwd|pwd)\s*[:=]\s*["\']?[^\s"\']{8,}',
        re.IGNORECASE
    ),
    SecretType.ENV_VAR: re.compile(
        r'(SECRET|TOKEN|PRIVATE|KEY|CREDENTIAL)\s*[:=]',
        re.IGNORECASE
    ),
    SecretType.DATABASE_URL: re.compile(
        r'(mongodb|postgresql|mysql|redis)://[^\s]{10,}'
    ),
    SecretType.SLACK_TOKEN: re.compile(
        r'xox[baprs]-[0-9]{10,13}-[0-9]{10,13}[-a-zA-Z0-9]{24,34}'
    ),
    SecretType.JWT_TOKEN: re.compile(
        r'eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+'
    ),
}


# ============================================================================
# [數據結構]
# ============================================================================

@dataclass
class SecretFinding:
    """敏感信息發現記錄"""
    file_path: str
    line_number: int
    secret_type: SecretType
    found_value: str
    redacted_value: str
    severity: str = "HIGH"
    context: str = None

    def to_dict(self) -> Dict:
        return {
            'file_path': self.file_path,
            'line_number': self.line_number,
            'secret_type': self.secret_type.value,
            'found_value': '***REDACTED***',  # 不保存實際值
            'redacted_value': self.redacted_value,
            'severity': self.severity,
            'context': self.context
        }


# ============================================================================
# [Secret Guard 實現]
# ============================================================================

class SecretGuard:
    """敏感信息檢測和脫敏系統"""

    # 需要跳過的文件/目錄
    SKIP_PATTERNS = {
        '.git',
        '.env',
        '__pycache__',
        'node_modules',
        '.venv',
        'venv',
        '.idea',
        '.vscode',
        'dist',
        'build',
        '.next',
        '.cache',
        '.pytest_cache',
        '*.pyc',
        '*.pyo',
        '.DS_Store',
        'Thumbs.db'
    }

    # 信任的文件擴展名 (這些文件中的匹配可能是誤報)
    TRUSTED_EXTENSIONS = {
        '.md',
        '.txt',
        '.json',
        '.yaml',
        '.yml',
        '.xml',
    }

    @staticmethod
    def redact(text: str, keep_chars: int = 4) -> str:
        """
        脫敏敏感信息

        保留首尾若干字符，中間用 *** 替代

        Args:
            text: 要脫敏的文本
            keep_chars: 保留的首尾字符數

        Returns:
            脫敏後的文本
        """
        if len(text) <= keep_chars * 2:
            return '***REDACTED***'

        return text[:keep_chars] + '***REDACTED***' + text[-keep_chars:]

    @staticmethod
    def should_skip(filepath: Path) -> bool:
        """
        判斷是否應該跳過文件

        Args:
            filepath: 文件路徑

        Returns:
            是否跳過
        """
        # 檢查目錄名
        for skip_pattern in SecretGuard.SKIP_PATTERNS:
            if skip_pattern.replace('*', '') in filepath.parts:
                return True

        # 檢查文件擴展名
        if filepath.suffix in SecretGuard.TRUSTED_EXTENSIONS:
            return True

        return False

    @classmethod
    def scan_file(cls, filepath: Path) -> List[SecretFinding]:
        """
        掃描單個文件中的敏感信息

        Args:
            filepath: 文件路徑

        Returns:
            發現列表
        """
        findings: List[SecretFinding] = []

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_no, line in enumerate(f, 1):
                    # 跳過註釋行
                    stripped_line = line.strip()
                    if stripped_line.startswith('#') or stripped_line.startswith('//'):
                        continue

                    # 檢查每個模式
                    for secret_type, pattern in DETECTION_PATTERNS.items():
                        matches = pattern.finditer(line)

                        for match in matches:
                            found_value = match.group()
                            redacted_value = cls.redact(found_value)

                            # 提取上下文 (前後各 20 個字符)
                            start = max(0, match.start() - 20)
                            end = min(len(line), match.end() + 20)
                            context = line[start:end].strip()

                            findings.append(SecretFinding(
                                file_path=str(filepath),
                                line_number=line_no,
                                secret_type=secret_type,
                                found_value=found_value,
                                redacted_value=redacted_value,
                                context=context
                            ))

        except Exception as e:
            logger.error(f"掃描文件 {filepath} 時發生錯誤: {e}")
            findings.append(SecretFinding(
                file_path=str(filepath),
                line_number=0,
                secret_type=SecretType.GENERIC_SECRET,
                found_value='ERROR',
                redacted_value='***SCAN_ERROR***',
                severity='MEDIUM',
                context=str(e)
            ))

        return findings

    @classmethod
    def scan_directory(
        cls,
        root_path: Path,
        max_workers: int = 4,
        show_progress: bool = True
    ) -> List[SecretFinding]:
        """
        遞歸掃描目錄

        Args:
            root_path: 根目錄路徑
            max_workers: 最大線程數
            show_progress: 是否顯示進度條

        Returns:
            所有發現
        """
        logger.info(f"開始掃描目錄: {root_path}")

        # 收集所有文件
        all_files = []
        for filepath in root_path.rglob('*'):
            if filepath.is_file() and not cls.should_skip(filepath):
                all_files.append(filepath)

        logger.info(f"找到 {len(all_files)} 個文件待掃描")

        all_findings: List[SecretFinding] = []

        # 並行掃描文件
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(cls.scan_file, filepath): filepath
                for filepath in all_files
            }

            # 進度條
            iterator = as_completed(futures)
            if show_progress:
                iterator = tqdm(iterator, total=len(all_files), desc="掃描進度")

            # 收集結果
            for future in iterator:
                try:
                    findings = future.result()
                    all_findings.extend(findings)
                except Exception as e:
                    filepath = futures[future]
                    logger.error(f"掃描文件 {filepath} 時發生異常: {e}")

        logger.info(f"掃描完成，發現 {len(all_findings)} 個敏感信息")

        return all_findings

    @classmethod
    def generate_report(
        cls,
        findings: List[SecretFinding],
        output_file: Optional[Path] = None
    ) -> Dict:
        """
        生成掃描報告

        Args:
            findings: 發現列表
            output_file: 輸出文件路徑 (可選)

        Returns:
            報告字典
        """
        # 統計
        total = len(findings)
        by_type = {}
        by_severity = {}

        for finding in findings:
            # 按類型統計
            type_key = finding.secret_type.value
            by_type[type_key] = by_type.get(type_key, 0) + 1

            # 按嚴重性統計
            severity = finding.severity
            by_severity[severity] = by_severity.get(severity, 0) + 1

        report = {
            'summary': {
                'total_findings': total,
                'by_type': by_type,
                'by_severity': by_severity
            },
            'findings': [f.to_dict() for f in findings],
            'risk_level': cls._assess_risk(total, by_severity)
        }

        # 保存報告
        if output_file:
            import json
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"報告已保存: {output_file}")

        return report

    @staticmethod
    def _assess_risk(total: int, by_severity: Dict[str, int]) -> str:
        """
        評估風險級別

        Args:
            total: 總發現數
            by_severity: 按嚴重性分組

        Returns:
            風險級別 ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'NONE')
        """
        if by_severity.get('HIGH', 0) > 5 or by_severity.get('CRITICAL', 0) > 0:
            return 'CRITICAL'
        elif total > 10:
            return 'HIGH'
        elif total > 5:
            return 'MEDIUM'
        elif total > 0:
            return 'LOW'
        else:
            return 'NONE'


# ============================================================================
# [命令行界面]
# ============================================================================

def main():
    """命令行入口"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description='龍魂 DNA 協議 · Secret Guard - 敏感信息檢測'
    )
    parser.add_argument('path', help='要掃描的文件或目錄')
    parser.add_argument('-o', '--output', help='輸出報告文件')
    parser.add_argument('-w', '--workers', type=int, default=4, help='並行線程數')
    parser.add_argument('--no-progress', action='store_true', help='隱藏進度條')

    args = parser.parse_args()

    scan_path = Path(args.path)

    if not scan_path.exists():
        print(f"❌ 路徑不存在: {scan_path}")
        sys.exit(1)

    # 執行掃描
    output_file = Path(args.output) if args.output else None

    if scan_path.is_file():
        # 掃描單個文件
        findings = SecretGuard.scan_file(scan_path)
    else:
        # 掃描整個目錄
        findings = SecretGuard.scan_directory(
            scan_path,
            max_workers=args.workers,
            show_progress=not args.no_progress
        )

    # 生成報告
    report = SecretGuard.generate_report(findings, output_file)

    # 打印摘要
    print("\n" + "=" * 70)
    print("🔐 Secret Guard 掃描完成")
    print("=" * 70)
    print(f"📊 統計信息:")
    print(f"  總發現數:  {report['summary']['total_findings']}")
    print(f"  風險級別:  {report['risk_level']}")

    if report['summary']['by_type']:
        print(f"\n  按類型分組:")
        for secret_type, count in report['summary']['by_type'].items():
            print(f"    - {secret_type}: {count}")

    if report['summary']['by_severity']:
        print(f"\n  按嚴重性分組:")
        for severity, count in report['summary']['by_severity'].items():
            print(f"    - {severity}: {count}")

    if output_file:
        print(f"\n💾 報告已保存: {output_file}")

    print("=" * 70)

    # 如果有發現，返回非零退出碼
    sys.exit(0 if report['summary']['total_findings'] == 0 else 1)


if __name__ == '__main__':
    main()
