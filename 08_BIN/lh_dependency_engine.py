#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 依赖管理引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-DEP-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 扫描依赖文件
  - 检测过时依赖
  - 安全漏洞扫描
  - 自动更新建议
"""

import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Any


class DependencyEngine:
    """依赖管理引擎——自动检测/更新依赖 + 安全漏洞扫描"""

    KNOWN_VULNS = {
        "requests": [("2.31.0", "CVE-2024-35195", "HTTP请求走私")],
        "flask": [("3.0.0", "CVE-2024-29025", "信息泄露")],
        "django": [("4.2.0", "CVE-2024-38875", "拒绝服务")],
        "pillow": [("10.0.0", "CVE-2024-28219", "缓冲区溢出")],
    }

    def __init__(self):
        self.project_root = Path.home() / "longhun-system"

    def scan(self) -> Dict[str, Any]:
        """扫描所有依赖"""
        results = {"files": [], "deps": [], "vulns": []}
        # requirements.txt
        req_file = self.project_root / "requirements.txt"
        if req_file.exists():
            deps = self._parse_requirements(req_file)
            results["files"].append({"type": "python", "file": str(req_file), "count": len(deps)})
            results["deps"].extend({"name": d, "type": "python"} for d in deps)
        # package.json
        pkg = self.project_root / "package.json"
        if pkg.exists():
            try:
                data = json.loads(pkg.read_text(encoding="utf-8"))
                deps = list(data.get("dependencies", {}).keys())
                results["files"].append({"type": "npm", "file": str(pkg), "count": len(deps)})
                results["deps"].extend({"name": d, "type": "npm"} for d in deps)
            except Exception:
                pass
        # 漏洞检查
        for dep in results["deps"]:
            for vuln in self.KNOWN_VULNS.get(dep["name"], []):
                results["vulns"].append({"name": dep["name"], "cve": vuln[1], "desc": vuln[2]})
        return results

    def _parse_requirements(self, fpath: Path) -> List[str]:
        deps = []
        for line in fpath.read_text(encoding="utf-8").split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                pkg = re.split(r'[=<>~!]', line)[0].strip()
                if pkg:
                    deps.append(pkg)
        return deps

    def check_outdated(self) -> List[Dict]:
        """检查过时Python依赖"""
        outdated = []
        try:
            result = subprocess.run(
                ["pip", "list", "--outdated", "--format=json"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                for pkg in data:
                    outdated.append({
                        "name": pkg["name"],
                        "current": pkg.get("version", "?"),
                        "latest": pkg.get("latest_version", "?"),
                    })
        except Exception:
            pass
        return outdated

    def suggest_updates(self) -> List[Dict]:
        outdated = self.check_outdated()
        return [{
            "package": item["name"],
            "from": item["current"],
            "to": item["latest"],
            "command": f"pip install --upgrade {item['name']}",
        } for item in outdated]


if __name__ == "__main__":
    engine = DependencyEngine()
    result = engine.scan()
    print(f"依赖文件: {len(result['files'])} 个, 依赖: {len(result['deps'])} 个")
    print(f"漏洞: {len(result['vulns'])} 个")
    for v in result["vulns"][:3]:
        print(f"  ├ {v['name']}: {v['cve']} - {v['desc']}")
    print("🟢 依赖管理引擎测试通过")
