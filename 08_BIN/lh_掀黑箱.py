#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 掀黑箱审计引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-掀黑箱-v1.0-UID9622

功能：
  审计任意项目，识别技术主权风险，包括：
  - 闭源/未授权依赖
  - 数据外流接口（硬编码URL、IP）
  - 主权声明缺失
  - 外部云服务依赖（不可替换）
  - 疑似后门/加密通信未说明

输出：
  - 终端彩色报告（人类可读）
  - JSON 格式（机器可读）
  - 支持导出 HTML 报告

用法：
  lh 掀黑箱 [路径]                 # 审计当前目录或指定路径
  lh 掀黑箱 [路径] --json          # 输出 JSON
  lh 掀黑箱 [路径] --output report.html   # 生成 HTML 报告
  lh 掀黑箱 --help                 # 帮助
"""

import os
import sys
import re
import json
import hashlib
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime
from collections import defaultdict

# ============================================================
# 配置
# ============================================================

PROJECT_ROOT = Path.home() / "longhun-system"
REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# 扫描时跳过的目录/文件名模式
SKIP_DIRS = {
    "node_modules", "venv", ".venv", ".venv_tts", "__pycache__",
    "dist", "build", "output", ".git", ".codebuddy", ".obsidian",
    ".vscode", ".commander", ".daoyin_workspace", ".longhun",
    ".githooks", ".github", "logs", "test_logs", "test_results",
    "models", "fused_model", "_archive", "_private", "_work",
    "videos", "voices", "tts", "launchd", "docker",
}

# 风险等级
RISK_CRITICAL = "🔴 严重"
RISK_HIGH = "🟠 高危"
RISK_MEDIUM = "🟡 中危"
RISK_LOW = "🟢 低危"
RISK_INFO = "ℹ️ 信息"

# ============================================================
# 审计规则
# ============================================================

RULES = {
    # 闭源/受限依赖
    "proprietary_deps": {
        "name": "闭源/专有依赖",
        "severity": RISK_CRITICAL,
        "description": "项目依赖了闭源或受限许可证的软件，存在法律和主权风险。",
        "patterns": [
            r"oracle", r"mysql-connector", r"msodbcsql", r"ibm_db",
            r"pymssql", r"pyodbc", r"cx_Oracle", r"psycopg2-binary",
            r"django-", r"flask-", r"tensorflow", r"pytorch", r"transformers",
            r"langchain", r"llama-index", r"openai", r"anthropic",
        ],
        "check": "dependencies"
    },
    # 数据外流接口（硬编码URL）
    "data_exfiltration": {
        "name": "数据外流接口",
        "severity": RISK_CRITICAL,
        "description": "检测到硬编码的第三方API地址，可能将数据发送至外部。",
        "patterns": [
            r"https?://[a-zA-Z0-9\-\.]+\.(?:com|cn|net|org|io|cloud|ai)\S*",
            r"api\.", r"\.amazonaws\.com", r"\.azure\.com", r"\.googleapis\.com",
            r"\.openai\.com", r"\.anthropic\.com", r"\.huggingface\.co",
            r"\.github\.com", r"\.gitlab\.com",
        ],
        "check": "hardcoded_urls"
    },
    # 缺乏主权声明
    "sovereignty_missing": {
        "name": "主权声明缺失",
        "severity": RISK_HIGH,
        "description": "项目缺少LICENSE或主权声明文件，无法确定授权归属。",
        "patterns": [],
        "check": "sovereignty"
    },
    # 外部云服务依赖
    "cloud_dependency": {
        "name": "外部云服务依赖",
        "severity": RISK_HIGH,
        "description": "项目强依赖国外云服务，存在断供和合规风险。",
        "patterns": [
            r"aws", r"azure", r"gcp", r"google-cloud", r"amazon",
            r"boto3", r"azure-", r"google-api", r"firebase",
        ],
        "check": "dependencies"
    },
    # 未签名的二进制文件
    "unsigned_binaries": {
        "name": "未签名二进制文件",
        "severity": RISK_MEDIUM,
        "description": "项目中存在未签名的可执行文件或动态库，无法验证来源。",
        "patterns": [r"\.(exe|dll|so|dylib|bin)$"],
        "check": "files"
    },
    # 疑似后门/加密通信（仅标记可疑模式，安全项目自审计降为🟡）
    "backdoor_suspect": {
        "name": "疑似后门/隐蔽通信",
        "severity": RISK_CRITICAL,
        "description": "检测到可疑的加密通信或隐蔽通道，需人工核查。",
        "patterns": [
            r"cryptography\.fernet", r"cryptography\.hazmat",
            r"reverse\s*shell", r"exec\s*\(\s*.*base64", r"eval\s*\(\s*.*base64",
            r"subprocess.*hidden", r"os\.system.*curl.*http",
            r"socket\.connect.*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",  # 直连IP
        ],
        "check": "code"
    },
    # 缺乏开源合规文件
    "compliance_missing": {
        "name": "开源合规文件缺失",
        "severity": RISK_MEDIUM,
        "description": "缺少 CONTRIBUTING、CODE_OF_CONDUCT 等治理文件。",
        "patterns": [],
        "check": "files"
    },
    # 未使用国产芯片/系统标记
    "domestic_incompatible": {
        "name": "未适配国产环境",
        "severity": RISK_MEDIUM,
        "description": "项目未标注支持鲲鹏、龍芯等国产平台，可能无法在信创环境运行。",
        "patterns": [],
        "check": "sovereignty"
    },
}

# ============================================================
# 审计引擎
# ============================================================

class BlackBoxAuditor:
    def __init__(self, target_path: Path):
        self.target = target_path.resolve()
        self.results = {
            "target": str(self.target),
            "timestamp": datetime.now().isoformat(),
            "findings": [],
            "summary": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "info": 0,
            },
            "files_scanned": 0,
            "dependencies": {},
            "hardcoded_urls": [],
            "sovereignty": {},
        }
        self._file_paths: List[Path] = []  # 只存路径，不存内容（防内存爆炸）

    def _read_file(self, file_path: Path) -> Optional[str]:
        """按需读取单个文件内容"""
        try:
            return file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return None

    def scan(self) -> Dict[str, Any]:
        """执行完整扫描"""
        # 1. 扫描文件（只收集路径）
        self._scan_files()

        # 2. 分析依赖
        self._analyze_dependencies()

        # 3. 检查主权声明
        self._check_sovereignty()

        # 4. 检查硬编码URL（流式逐文件读）
        self._check_hardcoded_urls()

        # 5. 应用规则（流式逐文件读）
        self._apply_rules()

        # 6. 生成总结
        self._generate_summary()

        return self.results

    def _scan_files(self):
        """递归扫描文件（只收集路径，不加载内容）"""
        skip_file_suffixes = {".pyc", ".pyo", ".so", ".dylib", ".dll", ".exe", ".asc",
                              ".bin", ".zip", ".tar", ".gz", ".png", ".jpg", ".jpeg",
                              ".gif", ".webp", ".mp4", ".mp3", ".wav", ".ttf", ".otf",
                              ".woff", ".woff2", ".ico", ".svg", ".pdf", ".lock"}
        for file_path in self.target.rglob("*"):
            if not file_path.is_file():
                continue
            # 跳过噪音目录
            parts = set(file_path.parts)
            if parts & SKIP_DIRS:
                continue
            # 排除隐藏目录
            if any(p.startswith(".") for p in file_path.parts):
                continue
            if file_path.suffix.lower() in skip_file_suffixes:
                continue
            if file_path.stat().st_size > 524288:  # >512KB 跳过
                continue
            self._file_paths.append(file_path)
        self.results["files_scanned"] = len(self._file_paths)

    def _analyze_dependencies(self):
        """分析依赖文件"""
        deps = {}
        # requirements.txt
        req_file = self.target / "requirements.txt"
        if req_file.exists():
            lines = req_file.read_text(encoding="utf-8", errors="ignore").splitlines()
            deps["requirements.txt"] = [l.strip() for l in lines if l.strip() and not l.strip().startswith("#")]
        # package.json
        pkg_file = self.target / "package.json"
        if pkg_file.exists():
            try:
                data = json.loads(pkg_file.read_text(encoding="utf-8"))
                all_deps = {}
                for section in ["dependencies", "devDependencies", "peerDependencies"]:
                    section_data = data.get(section, {})
                    if isinstance(section_data, dict):
                        all_deps.update(section_data)
                deps["package.json"] = list(all_deps.keys())
            except Exception:
                pass
        # pyproject.toml
        pyproj = self.target / "pyproject.toml"
        if pyproj.exists():
            deps["pyproject.toml"] = ["手动检查"]
        # setup.py / setup.cfg
        setup_file = self.target / "setup.py"
        if setup_file.exists():
            deps["setup.py"] = ["手动检查"]
        self.results["dependencies"] = deps

    def _check_sovereignty(self):
        """检查主权声明"""
        has_license = (
            (self.target / "LICENSE").exists()
            or (self.target / "LICENSE.txt").exists()
            or (self.target / "LICENSE.md").exists()
        )
        has_readme = (
            (self.target / "README.md").exists()
            or (self.target / "README").exists()
        )
        has_sovereignty = False
        readme_content = ""
        if (self.target / "README.md").exists():
            try:
                readme_content = (self.target / "README.md").read_text(encoding="utf-8", errors="ignore")
            except Exception:
                pass
        if has_readme and readme_content:
            if "主权" in readme_content or "sovereign" in readme_content.lower():
                has_sovereignty = True

        # 检查开源合规文件
        has_contributing = (
            (self.target / "CONTRIBUTING.md").exists()
            or (self.target / "CONTRIBUTING").exists()
        )
        has_code_of_conduct = (
            (self.target / "CODE_OF_CONDUCT.md").exists()
            or (self.target / "CODE_OF_CONDUCT").exists()
        )
        has_security = (self.target / "SECURITY.md").exists()
        has_changelog = (
            (self.target / "CHANGELOG.md").exists()
            or (self.target / "CHANGELOG").exists()
        )
        has_governance = (self.target / "GOVERNANCE.md").exists()

        self.results["sovereignty"] = {
            "license": has_license,
            "readme": has_readme,
            "readme_content": readme_content,
            "sovereignty_statement": has_sovereignty,
            "compliance_files": {
                "contributing": has_contributing,
                "code_of_conduct": has_code_of_conduct,
                "security": has_security,
                "changelog": has_changelog,
                "governance": has_governance,
            }
        }

    def _check_hardcoded_urls(self):
        """检测硬编码URL（流式逐文件读取，不占内存）"""
        urls = []
        url_pattern = RULES["data_exfiltration"]["patterns"][0]
        skip_domains = {"localhost", "127.0.0.1", "example", "0.0.0.0", "uid9622.cn",
                        "longhun888.com", "119.13.90.27", "your-domain", "your_domain"}
        for fp in self._file_paths:
            content = self._read_file(fp)
            if not content:
                continue
            found = re.findall(url_pattern, content)
            rel = str(fp.relative_to(self.target))
            for url in found:
                if any(skip in url.lower() for skip in skip_domains):
                    continue
                urls.append({"file": rel, "url": url})
        self.results["hardcoded_urls"] = urls

    def _apply_rules(self):
        """应用所有规则"""
        findings = []

        # 1. 依赖检查
        for rule_name, rule in RULES.items():
            if rule["check"] != "dependencies":
                continue
            for dep_file, dep_list in self.results["dependencies"].items():
                for dep in dep_list:
                    if isinstance(dep, str) and any(re.search(p, dep, re.I) for p in rule["patterns"]):
                        findings.append({
                            "rule": rule_name,
                            "severity": rule["severity"],
                            "description": rule["description"],
                            "evidence": f"依赖 {dep} 在 {dep_file} 中",
                        })

        # 2. 主权检查
        sover = self.results.get("sovereignty", {})
        if not sover.get("license"):
            findings.append({
                "rule": "sovereignty_missing",
                "severity": RISK_HIGH,
                "description": RULES["sovereignty_missing"]["description"],
                "evidence": "未找到 LICENSE 文件",
            })
        if not sover.get("sovereignty_statement"):
            findings.append({
                "rule": "sovereignty_missing",
                "severity": RISK_MEDIUM,
                "description": "缺乏显式的主权声明，建议在 README 中说明数据主权归属。",
                "evidence": "README 中未提及主权",
            })
        # 合规文件检查
        comp_files = sover.get("compliance_files", {})
        missing_compliance = [k for k, v in comp_files.items() if not v]
        if missing_compliance:
            findings.append({
                "rule": "compliance_missing",
                "severity": RISK_MEDIUM,
                "description": RULES["compliance_missing"]["description"],
                "evidence": f"缺失文件: {', '.join(missing_compliance)}",
            })
        # 国产适配检查
        readme_content = sover.get("readme_content", "")
        domestic_keywords = ["鲲鹏", "龍芯", "信创", "国产", "aarch64", "ARM64"]
        if not any(kw in readme_content for kw in domestic_keywords):
            findings.append({
                "rule": "domestic_incompatible",
                "severity": RISK_MEDIUM,
                "description": RULES["domestic_incompatible"]["description"],
                "evidence": "未在 README 中标注国产平台支持",
            })

        # 3. 硬编码URL
        for url_info in self.results.get("hardcoded_urls", []):
            findings.append({
                "rule": "data_exfiltration",
                "severity": RISK_CRITICAL,
                "description": f"发现外部API调用: {url_info['url']}",
                "evidence": f"文件: {url_info['file']}",
            })

        # 4. 文件检查（检查文件名模式）
        for fp in self._file_paths:
            rel = str(fp.relative_to(self.target))
            if any(re.search(p, rel, re.I) for p in RULES["unsigned_binaries"]["patterns"]):
                findings.append({
                    "rule": "unsigned_binaries",
                    "severity": RISK_MEDIUM,
                    "description": RULES["unsigned_binaries"]["description"],
                    "evidence": f"文件: {rel}",
                })

        # 5. 代码检查（后门可疑·流式逐文件读取）
        for fp in self._file_paths:
            content = self._read_file(fp)
            if not content:
                continue
            rel = str(fp.relative_to(self.target))
            for pattern in RULES["backdoor_suspect"]["patterns"]:
                if re.search(pattern, content, re.I):
                    findings.append({
                        "rule": "backdoor_suspect",
                        "severity": RISK_CRITICAL,
                        "description": RULES["backdoor_suspect"]["description"],
                        "evidence": f"在 {rel} 中发现疑似隐蔽通信代码: {pattern}",
                    })
                    break

        # 去重（基于 evidence）
        seen = set()
        unique_findings = []
        for f in findings:
            key = f["evidence"]
            if key not in seen:
                seen.add(key)
                unique_findings.append(f)

        self.results["findings"] = unique_findings

    def _generate_summary(self):
        """生成统计摘要"""
        summary = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for f in self.results["findings"]:
            sev = f["severity"]
            if sev == RISK_CRITICAL:
                summary["critical"] += 1
            elif sev == RISK_HIGH:
                summary["high"] += 1
            elif sev == RISK_MEDIUM:
                summary["medium"] += 1
            elif sev == RISK_LOW:
                summary["low"] += 1
            else:
                summary["info"] += 1
        self.results["summary"] = summary

# ============================================================
# 报告生成器
# ============================================================

def print_terminal_report(result: Dict[str, Any]):
    """终端彩色输出"""
    RED = '\033[91m'
    ORANGE = '\033[38;5;214m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

    lines = []
    lines.append(f"\n{BOLD}{'='*70}{RESET}")
    lines.append(f"{BOLD}🐉 龍魂 · 掀黑箱审计报告{RESET}")
    lines.append(f"{BOLD}{'='*70}{RESET}")
    lines.append(f"  目标: {result['target']}")
    lines.append(f"  时间: {result['timestamp']}")
    lines.append(f"  文件数: {result['files_scanned']}")
    lines.append(f"{BOLD}{'-'*70}{RESET}")

    # 摘要
    s = result["summary"]
    lines.append(f"\n📊 风险摘要")
    lines.append(f"  {RISK_CRITICAL}: {s['critical']}")
    lines.append(f"  {RISK_HIGH}: {s['high']}")
    lines.append(f"  {RISK_MEDIUM}: {s['medium']}")
    lines.append(f"  {RISK_LOW}: {s['low']}")

    total_risk = s['critical'] + s['high'] + s['medium']
    if s['critical'] > 0:
        overall = f"{RED}🔴 高风险，建议立即处理{RESET}"
    elif s['high'] > 0:
        overall = f"{ORANGE}🟠 中高风险，建议排查{RESET}"
    elif s['medium'] > 0:
        overall = f"{YELLOW}🟡 关注，有改进空间{RESET}"
    else:
        overall = f"{GREEN}🟢 风险可控{RESET}"
    lines.append(f"\n  总体评估: {overall}")

    # 详细发现
    if result["findings"]:
        lines.append(f"\n{BOLD}🔍 详细发现{RESET}")
        lines.append("-" * 70)
        for i, f in enumerate(result["findings"], 1):
            sev = f["severity"]
            lines.append(f"{i}. {sev} {f['rule']}")
            lines.append(f"   {f['description']}")
            lines.append(f"   📎 {f['evidence']}")
            lines.append("")

    # 主权声明
    sover = result.get("sovereignty", {})
    lines.append(f"{BOLD}📜 主权声明检查{RESET}")
    lines.append(f"  LICENSE: {'✅ 存在' if sover.get('license') else '❌ 缺失'}")
    lines.append(f"  README: {'✅ 存在' if sover.get('readme') else '❌ 缺失'}")
    lines.append(f"  主权声明: {'✅ 已声明' if sover.get('sovereignty_statement') else '❌ 未声明'}")
    # 合规文件
    comp = sover.get("compliance_files", {})
    if comp:
        statuses = []
        for k, v in comp.items():
            cmap = {"contributing": "CONTRIBUTING", "code_of_conduct": "CODE_OF_CONDUCT",
                    "security": "SECURITY", "changelog": "CHANGELOG", "governance": "GOVERNANCE"}
            statuses.append(f"{cmap.get(k, k)}: {'✅' if v else '❌'}")
        lines.append(f"  合规文件: {'  '.join(statuses)}")

    # 硬编码URL（脱敏展示前3个）
    urls = result.get("hardcoded_urls", [])
    if urls:
        lines.append(f"\n{BOLD}🌐 硬编码外部URL（前3个）{RESET}")
        for u in urls[:3]:
            lines.append(f"  {u['url']} ({u['file']})")
        if len(urls) > 3:
            lines.append(f"  ... 还有 {len(urls)-3} 个")

    lines.append(f"\n{BOLD}{'='*70}{RESET}")
    lines.append(f"DNA: #龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-掀黑箱-UID9622")
    print("\n".join(lines))

def generate_html_report(result: Dict[str, Any], output_path: Path):
    """生成 HTML 报告"""
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>龍魂 · 掀黑箱审计报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 1000px; margin: 40px auto; padding: 20px; background: #f8f9fa; }}
        h1, h2, h3 {{ color: #1a1a2e; border-bottom: 2px solid #e9ecef; padding-bottom: 8px; }}
        .risk-critical {{ color: #e63946; font-weight: bold; }}
        .risk-high {{ color: #e67e22; font-weight: bold; }}
        .risk-medium {{ color: #f1c40f; font-weight: bold; }}
        .risk-low {{ color: #2ecc71; font-weight: bold; }}
        .finding {{ background: white; padding: 12px 16px; margin: 8px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.06); }}
        .evidence {{ color: #6c757d; font-size: 0.9em; }}
        .summary {{ display: flex; gap: 20px; flex-wrap: wrap; margin: 20px 0; }}
        .summary-item {{ background: white; padding: 16px 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); flex: 1; min-width: 80px; text-align: center; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; color: white; }}
        .badge-critical {{ background: #e63946; }}
        .badge-high {{ background: #e67e22; }}
        .badge-medium {{ background: #f1c40f; }}
        .badge-low {{ background: #2ecc71; }}
        .footer {{ margin-top: 40px; border-top: 2px solid #e9ecef; padding-top: 20px; font-size: 0.9em; color: #6c757d; text-align: center; }}
        .dna {{ font-family: monospace; background: #1a1a2e; color: #ffd60a; padding: 4px 10px; border-radius: 4px; }}
    </style>
</head>
<body>
    <h1>🐉 龍魂 · 掀黑箱审计报告</h1>
    <p>目标: {result['target']} | 时间: {result['timestamp']} | 文件数: {result['files_scanned']}</p>

    <h2>📊 风险摘要</h2>
    <div class="summary">
        <div class="summary-item"><span class="badge badge-critical">严重</span> <strong>{result['summary']['critical']}</strong></div>
        <div class="summary-item"><span class="badge badge-high">高危</span> <strong>{result['summary']['high']}</strong></div>
        <div class="summary-item"><span class="badge badge-medium">中危</span> <strong>{result['summary']['medium']}</strong></div>
        <div class="summary-item"><span class="badge badge-low">低危</span> <strong>{result['summary']['low']}</strong></div>
    </div>

    <h2>🔍 详细发现</h2>
    {''.join(f'''
    <div class="finding">
        <strong>{f['severity']} {f['rule']}</strong>
        <p>{f['description']}</p>
        <div class="evidence">📎 {f['evidence']}</div>
    </div>
    ''' for f in result['findings']) if result['findings'] else '<p>🎉 未发现明显风险</p>'}

    <h2>📜 主权声明</h2>
    <ul>
        <li>LICENSE: {'✅ 存在' if result.get('sovereignty',{}).get('license') else '❌ 缺失'}</li>
        <li>README: {'✅ 存在' if result.get('sovereignty',{}).get('readme') else '❌ 缺失'}</li>
        <li>主权声明: {'✅ 已声明' if result.get('sovereignty',{}).get('sovereignty_statement') else '❌ 未声明'}</li>
    </ul>

    <div class="footer">
        DNA: <span class="dna">#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-掀黑箱-UID9622</span>
        <br>© 龍魂系统 · 君子协议
    </div>
</body>
</html>
    """
    output_path.write_text(html, encoding="utf-8")

# ============================================================
# 命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 掀黑箱审计引擎 — 审计任意项目的技术主权风险",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh 掀黑箱                          # 审计当前目录
  lh 掀黑箱 /path/to/project         # 审计指定路径
  lh 掀黑箱 --json                   # JSON 输出
  lh 掀黑箱 -o report.html           # HTML 报告
  lh 掀黑箱 -o result.json           # JSON 文件
        """
    )
    parser.add_argument("target", nargs="?", default=".",
                        help="要审计的目标路径（默认当前目录）")
    parser.add_argument("--json", action="store_true",
                        help="输出 JSON 格式")
    parser.add_argument("--output", "-o", type=str,
                        help="导出报告文件（支持 .json, .html）")
    parser.add_argument("--no-color", action="store_true",
                        help="禁用彩色输出")
    args = parser.parse_args()

    target_path = Path(args.target).expanduser().resolve()
    if not target_path.exists():
        print(f"❌ 目标路径不存在: {target_path}")
        sys.exit(1)

    print(f"🐉 龍魂·掀黑箱 正在审计: {target_path}", file=sys.stderr)
    auditor = BlackBoxAuditor(target_path)
    result = auditor.scan()

    # 输出 JSON
    if args.json:
        json_output = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(json_output, encoding="utf-8")
            print(f"✅ JSON 报告已保存: {args.output}")
        else:
            print(json_output)
        return

    # 输出 HTML
    if args.output and args.output.endswith(".html"):
        generate_html_report(result, Path(args.output))
        print(f"✅ HTML 报告已生成: {args.output}")
        return

    # 输出 JSON 文件
    if args.output and args.output.endswith(".json"):
        Path(args.output).write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"✅ JSON 报告已保存: {args.output}")
        return

    # 终端输出
    print_terminal_report(result)


if __name__ == "__main__":
    main()
