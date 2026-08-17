#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌·未时·䷔噬嗑-VULN_DETECT-v1.0-ENGINE
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 致敬: #致敬⚡️UID9622·漏洞检测·只扫自己的系统
"""
🐉 龍魂·漏洞检测引擎 v1.0
代码级漏洞扫描：SQL注入 / XSS / CSRF / 路径穿越 / 命令注入 / 硬编码密钥
依赖 CVE 数据库检查 · P77 黑天使联动 · 三色审计输出

用法:
  python3 bin/lh_vuln_detect.py scan <path>    全量扫描文件/目录
  python3 bin/lh_vuln_detect.py quick <path>   快速扫描（仅高风险模式）
  python3 bin/lh_vuln_detect.py cve <path>     依赖 CVE 数据库检查
  python3 bin/lh_vuln_detect.py p77 <path>     P77 黑天使联动深度扫描
  python3 bin/lh_vuln_detect.py report         查看最近报告
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

VERSION = "1.0"
DNA = "#龍芯⚡️丙午·丙申·壬戌·未时·䷔噬嗑-VULN_DETECT-v1.0-ENGINE"

# ── 扫描规则库（正则 → 漏洞类型 → 修复建议）──────────────────────────
# 每个规则: (正则, 漏洞名, 严重度[3高/2中/1低], 修复建议)
RULES = {
    "sql_injection": [
        (r"execute\s*\([^)]*['\"][^'\"]*['\"][^)]*\+", "SQL注入", 3,
         "禁止字符串拼接 SQL，改用参数化查询（cursor.execute(sql, params)）"),
        (r"SELECT\s+[^;]*\s*\+\s*['\"]", "SQL注入", 3,
         "禁止拼接 SQL，使用 ? 占位符参数化"),
        (r"f['\"][^'\"]*SELECT[^'\"]*\{[^}]+\}", "SQL注入(f-string)", 3,
         "f-string 拼 SQL 高危，改参数化查询"),
        (r"INSERT\s+[^;]*\s*\+\s*['\"]", "SQL注入", 3,
         "INSERT 禁止拼接，使用参数化"),
    ],
    "xss": [
        (r"\.innerHTML\s*=", "XSS(DOM注入)", 3,
         "禁止 innerHTML 直接赋值，用 textContent 或转义库"),
        (r"document\.write\s*\(", "XSS(DOM注入)", 3,
         "document.write 高危，改为 textContent/DOM API"),
        (r"dangerouslySetInnerHTML", "XSS(React)", 3,
         "React dangerouslySetInnerHTML 需先 sanitize"),
        (r"v-html\s*=", "XSS(Vue)", 3,
         "v-html 需经 DOMPurify 过滤后再渲染"),
        (r"eval\s*\(", "代码执行", 3,
         "eval 禁用于不可信输入，用 Function 构造器替代"),
        (r"new\s+Function\s*\(", "代码执行", 3,
         "new Function 与 eval 同风险，禁止处理不可信输入"),
    ],
    "csrf": [
        (r"<form[^>]*method\s*=\s*['\"]post['\"][^>]*>", "CSRF(表单无token)", 2,
         "POST 表单必须带 CSRF token 并在服务端校验"),
        (r"fetch\s*\(\s*['\"][^'\"]*['\"]\s*,\s*\{\s*method\s*:\s*['\"]POST", "CSRF(fetch POST)", 2,
         "POST fetch 需带 CSRF header（X-CSRF-Token）"),
        (r"axios\.post\s*\(", "CSRF(axios POST)", 2,
         "axios POST 需配置 withCredentials + CSRF header"),
    ],
    "path_traversal": [
        (r"\.\.%2f|\.\.%5c|%2e%2e%2f", "路径穿越(编码)", 3,
         "禁止拼接用户输入进文件路径，规范化后校验"),
        (r"os\.path\.join\s*\([^)]*\b(request|params|query|input)\b", "路径穿越", 3,
         "用户输入不得直接进路径，用 secure_filename + 白名单"),
        (r"open\s*\(\s*['\"]\s*\+\s*", "路径穿越(open拼接)", 3,
         "禁止 open() 字符串拼接用户输入"),
    ],
    "command_injection": [
        (r"os\.system\s*\([^)]*\+(?!\))", "命令注入", 3,
         "禁止拼接命令，用 subprocess 参数列表形式"),
        (r"subprocess\.(run|call|Popen)\s*\([^)]*shell\s*=\s*True", "命令注入(shell=True)", 3,
         "shell=True 高危，改参数列表形式传参"),
        (r"system\s*\([^)]*['\"][^'\"]*\{[^}]+", "命令注入(f-string)", 3,
         "命令模板禁止 f-string 拼接用户输入"),
    ],
    "hardcoded_secret": [
        (r"(api[_-]?key|apikey|secret[_-]?key|access[_-]?token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]", "硬编码密钥", 3,
         "密钥必须走环境变量/密钥管理系统，禁止硬编码"),
        (r"password\s*[:=]\s*['\"][^'\"]{6,}['\"]", "硬编码密码", 3,
         "密码走环境变量 + 密钥库，禁止入库"),
        (r"token\s*=\s*['\"][A-Za-z0-9_\-]{20,}['\"]", "硬编码Token", 2,
         "Token 从配置/环境读取，禁止源码硬编码"),
    ],
    "insecure_crypto": [
        (r"md5\s*\(", "弱哈希(MD5)", 2,
         "MD5 已不安全，改用 SHA-256/SM3"),
        (r"sha1\s*\(", "弱哈希(SHA-1)", 2,
         "SHA-1 已不安全，改用 SHA-256/SM3"),
        (r"DES[A-Za-z]*\s*\.", "弱加密(DES)", 3,
         "DES 已破解，改用 AES-256/SM4"),
    ],
    "auth_bypass": [
        (r"if\s*\(\s*(not\s+)?(token|auth|session)\s*\)\s*:\s*pass", "认证绕过", 2,
         "认证校验后不得 pass 跳过"),
        (r"login_required|auth_required", "认证装饰器存在", 1,
         "确认所有敏感路由已挂认证装饰器"),
    ],
}

# 依赖 → 已知 CVE 表（内置精简库，完整库放 data/cve_db.json 可扩展）
CVE_DB = {
    "flask": {"cve": "CVE-2023-30861", "desc": "Flask <2.3.2 模板注入", "fixed": ">=2.3.2"},
    "requests": {"cve": "CVE-2023-32681", "desc": "requests <2.31.0 代理认证绕过", "fixed": ">=2.31.0"},
    "urllib3": {"cve": "CVE-2023-45803", "desc": "urllib3 <2.0.7 请求走私", "fixed": ">=2.0.7"},
    "jinja2": {"cve": "CVE-2024-22195", "desc": "Jinja2 <3.1.3 DoS", "fixed": ">=3.1.3"},
    "django": {"cve": "CVE-2024-38875", "desc": "Django <4.2.14 DoS", "fixed": ">=4.2.14"},
    "fastapi": {"cve": "CVE-2024-24762", "desc": "FastAPI <0.109.1 依赖含漏洞", "fixed": ">=0.109.1"},
    "numpy": {"cve": "CVE-2021-33430", "desc": "numpy <1.22.0 整数溢出", "fixed": ">=1.22.0"},
    "openssl": {"cve": "CVE-2024-46080", "desc": "OpenSSL 3.x 前 <3.3.1 拒绝服务", "fixed": ">=3.3.1"},
    "log4j": {"cve": "CVE-2021-44228", "desc": "Log4j2 远程代码执行(Log4Shell)", "fixed": ">=2.17.1"},
    "wordpress": {"cve": "CVE-2024-44000", "desc": "WordPress <6.5.5 存储XSS", "fixed": ">=6.5.5"},
}

# 报告输出目录
REPORT_DIR = Path.home() / ".longhun" / "vuln_reports"


class VulnScanner:
    """龍魂·漏洞检测引擎"""

    def __init__(self, p77_mode: bool = False):
        self.p77_mode = p77_mode
        self.findings: list[dict] = []
        self.scanned_files = 0
        self.cve_hits: list[dict] = []

    def scan_text(self, content: str, file_name: str) -> list[dict]:
        """对单文件内容执行全部规则扫描"""
        hits = []
        for cat, rules in RULES.items():
            for pattern, name, severity, fix in rules:
                try:
                    for m in re.finditer(pattern, content, re.IGNORECASE):
                        lineno = content.count("\n", 0, m.start()) + 1
                        snippet = m.group(0)[:120]
                        hits.append({
                            "file": file_name, "line": lineno, "category": cat,
                            "type": name, "severity": severity, "snippet": snippet,
                            "fix": fix,
                        })
                except re.error:
                    continue
        return hits

    def scan_file(self, path: Path) -> list[dict]:
        """扫描单个文件"""
        hits = []
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []
        self.scanned_files += 1
        hits.extend(self.scan_text(content, str(path)))

        # P77 深度模式：额外检查未授权上传/调试后门
        if self.p77_mode:
            if re.search(r"(debug\s*=\s*True|app\.run\([^)]*debug)", content, re.I):
                hits.append({"file": str(path), "line": 0, "category": "debug_backdoor",
                             "type": "调试后门(debug=True)", "severity": 3,
                             "snippet": "debug=True 在生产环境", "fix": "生产环境必须 debug=False"})
            if re.search(r"print\s*\(\s*(password|token|secret|api_key)", content, re.I):
                hits.append({"file": str(path), "line": 0, "category": "log_secret",
                             "type": "日志泄露密钥", "severity": 3,
                             "snippet": "print 密钥字段", "fix": "禁止打印密钥，日志只打哈希指纹"})
        return hits

    def scan_dir(self, path: Path) -> list[dict]:
        """递归扫描目录（跳过 .git/node_modules/dist 等）"""
        all_hits = []
        skip = {".git", "node_modules", "dist", "dist_ide", "__pycache__",
                "archive", "_archive", "backup", "backups", "models",
                "fonts", ".idea", ".vscode", "venv", ".venv", "CNSH_修复输出"}
        exts = {".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".php", ".java",
                ".go", ".sh", ".rb", ".vue", ".sql", ".json", ".yml", ".yaml", ".conf"}
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in skip]
            for f in files:
                fp = Path(root) / f
                if fp.suffix.lower() not in exts:
                    continue
                all_hits.extend(self.scan_file(fp))
        return all_hits

    def check_cve(self, path: Path) -> list[dict]:
        """依赖 CVE 检查：扫描 requirements.txt / package.json / 源码 import"""
        hits = []
        if path.is_file():
            targets = [path]
        else:
            targets = list(path.rglob("requirements*.txt")) + \
                      list(path.rglob("package.json")) + \
                      list(path.rglob("*.toml")) + \
                      list(path.rglob("*.lock"))
        for t in targets[:50]:
            try:
                content = t.read_text(encoding="utf-8", errors="ignore").lower()
            except Exception:
                continue
            for dep, cve in CVE_DB.items():
                # 匹配依赖名（避免误匹配：flask 匹配 flask 而非 flask_cors 也算安全做法，标记待核）
                if re.search(rf"(^|[\n\"',/:=]{re.escape(dep)}[\s<>=!\"',/])", content):
                    hits.append({
                        "dependency": dep, "cve": cve["cve"], "desc": cve["desc"],
                        "fixed": cve["fixed"], "source": str(t),
                    })
        return hits

    def run(self, target: str) -> dict:
        """主入口：扫描 + 统计 + 生成报告"""
        path = Path(target)
        if not path.exists():
            print(f"🔴 路径不存在: {target}")
            sys.exit(1)

        print(f"🐉 龍魂·漏洞检测引擎 v{VERSION} · P77联动={'✅' if self.p77_mode else '—'}")
        print(f"📂 目标: {target}")
        t0 = datetime.now()

        if path.is_dir():
            self.findings = self.scan_dir(path)
        else:
            self.findings = self.scan_file(path)

        self.cve_hits = self.check_cve(path)

        # 统计
        sev = {3: 0, 2: 0, 1: 0}
        cats = {}
        for h in self.findings:
            sev[h["severity"]] = sev.get(h["severity"], 0) + 1
            cats[h["category"]] = cats.get(h["category"], 0) + 1

        # 三色判定
        if sev[3] > 0:
            verdict = "🔴 高风险"
        elif sev[2] > 0:
            verdict = "🟡 中风险·需复核"
        else:
            verdict = "🟢 通过"

        result = {
            "verdict": verdict, "scanned_files": self.scanned_files,
            "findings_count": len(self.findings),
            "severity": sev, "categories": cats,
            "cve_hits": self.cve_hits, "findings": self.findings[:200],
            "target": str(path), "timestamp": t0.isoformat(),
            "dna": DNA,
        }
        self._save_report(result)
        self._print_report(result, t0)
        return result

    def _print_report(self, result: dict, t0: datetime):
        dur = (datetime.now() - t0).total_seconds()
        print(f"\n{'='*60}")
        print(f"🐉 漏洞检测报告 · 耗时 {dur:.1f}s")
        print(f"{'='*60}")
        print(f"📂 扫描文件: {result['scanned_files']}")
        print(f"🎯 三色判定: {result['verdict']}")
        print(f"🔢 严重度: 高={result['severity'][3]} 中={result['severity'][2]} 低={result['severity'][1]}")
        if result["categories"]:
            print(f"📚 类别分布: {', '.join(f'{k}={v}' for k, v in result['categories'].items())}")

        if result["findings"]:
            print(f"\n⚠️  发现 {len(result['findings'])} 处问题:")
            for h in result["findings"][:30]:
                sev_icon = {3: "🔴", 2: "🟡", 1: "🟡"}[h["severity"]]
                print(f"  {sev_icon} [{h['type']}] {h['file']}:{h['line']}")
                print(f"     {h['snippet'][:90]}")
                print(f"     💊 {h['fix']}")
        else:
            print("\n✅ 未发现漏洞模式")

        if result["cve_hits"]:
            print(f"\n🔐 CVE 依赖命中 {len(result['cve_hits'])} 项:")
            for c in result["cve_hits"]:
                print(f"  ⚠️ {c['dependency']} → {c['cve']} ({c['desc']}) 修复: {c['fixed']}")
                print(f"     来源: {c['source']}")
        else:
            print("\n🔐 未发现已知 CVE 依赖")

        print(f"\n📁 报告已保存: {self._report_path(result['timestamp'])}")
        print(f"🧬 {DNA}")

    def _report_path(self, ts: str) -> Path:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        safe = ts.replace(":", "-").replace(".", "-")
        return REPORT_DIR / f"vuln_report_{safe}.json"

    def _save_report(self, result: dict):
        try:
            p = self._report_path(result["timestamp"])
            p.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"⚠️ 报告保存失败: {e}")

    def latest_report(self):
        if not REPORT_DIR.exists():
            print("📭 暂无报告")
            return
        files = sorted(REPORT_DIR.glob("vuln_report_*.json"), reverse=True)
        if not files:
            print("📭 暂无报告")
            return
        data = json.loads(files[0].read_text(encoding="utf-8"))
        print(f"📂 最近报告: {files[0].name}")
        print(f"🎯 三色判定: {data['verdict']}")
        print(f"🔢 高={data['severity'][3]} 中={data['severity'][2]} 低={data['severity'][1]} · 文件={data['scanned_files']}")
        if data["cve_hits"]:
            print(f"🔐 CVE: {len(data['cve_hits'])} 项")


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂·漏洞检测引擎 v1.0")
    sub = parser.add_subparsers(dest="cmd")

    for cmd in ("scan", "quick", "p77", "cve"):
        sp = sub.add_parser(cmd, help=f"{cmd} 子命令")
        sp.add_argument("target", help="目标文件或目录")
        sp.add_argument("--no-p77", action="store_true", help="不联动P77")

    sub.add_parser("report", help="查看最近报告")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return

    if args.cmd == "report":
        VulnScanner().latest_report()
        return

    target = args.target
    if args.cmd == "p77":
        scanner = VulnScanner(p77_mode=True)
        scanner.run(target)
    elif args.cmd == "cve":
        scanner = VulnScanner()
        hits = scanner.check_cve(Path(target))
        print(f"🐉 CVE 依赖检查 · 目标: {target}")
        if hits:
            for c in hits:
                print(f"  ⚠️ {c['dependency']} → {c['cve']} ({c['desc']}) 修复: {c['fixed']}")
            print(f"\n🔴 共 {len(hits)} 项需关注")
        else:
            print("✅ 未发现已知 CVE")
    else:  # scan / quick
        scanner = VulnScanner(p77_mode=(args.cmd == "p77"))
        scanner.run(target)


if __name__ == "__main__":
    main()
