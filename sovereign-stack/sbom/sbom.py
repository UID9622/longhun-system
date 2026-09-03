#!/usr/bin/env python3
"""
🐉 龍魂主权技术栈·SBOM 生成器 v1.0
原则：所有依赖可申报可复核·零黑箱·供应链可追溯
支持：requirements.txt / package.json / go.mod
输出：SPDX-Lite 简化格式 JSON
DNA: #龍芯⚡️2026-08-31-SBOM-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: MulanPSL v2（工程实现层）
"""

import re
import json
import sys
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def parse_requirements(text: str) -> list:
    deps = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name = re.split(r"[<>=!~;\s]", line)[0]
        ver_match = re.search(r"([<>=!~]+)\s*([\w.\-]+)", line)
        deps.append({
            "name": name,
            "version": ver_match.group(2) if ver_match else "unpinned",
            "constraint": ver_match.group(1) if ver_match else "",
            "license": "unknown",
        })
    return deps


def parse_package_json(text: str) -> list:
    try:
        data = json.loads(text)
    except Exception:
        return []
    deps = {}
    deps.update(data.get("dependencies", {}))
    deps.update(data.get("devDependencies", {}))
    return [{"name": k, "version": v.lstrip("^~"), "constraint": v,
             "license": "unknown"} for k, v in deps.items()]


def parse_go_mod(text: str) -> list:
    deps = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("require (") or line == "require":
            continue
        m = re.match(r"^([\w.\-]+/[\w.\-]+(?:/[\w.\-]+)?)\s+(v[\w.\-]+)", line)
        if m:
            deps.append({"name": m.group(1), "version": m.group(2),
                         "constraint": "exact", "license": "unknown"})
    return deps


def generate_sbom(manifest_text: str, kind: str) -> dict:
    parsers = {
        "pypi": parse_requirements,
        "npm":  parse_package_json,
        "go":   parse_go_mod,
    }
    parser = parsers.get(kind, parse_requirements)
    deps = parser(manifest_text)

    sbom = {
        "spdxVersion": "SPDX-2.3-Lite",
        "dataLicense": "CC0-1.0",
        "name": "longhun-sovereign-stack",
        "documentNamespace": f"sovereign-stack-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "creationInfo": {
            "created": datetime.now().isoformat(),
            "creator": "Person: 诸葛鑫 (UID9622)",
            "comment": "龍魂主权技术栈·依赖物料清单·零黑箱可复核",
        },
        "packages": deps,
        "packageCount": len(deps),
        "dna": "#龍芯⚡️2026-08-31-SBOM-UID9622",
        "tricolor": "🟢",
    }
    return sbom


@app.route("/sbom/generate", methods=["POST"])
def generate():
    data = request.json or {}
    text = data.get("manifest", "")
    kind = data.get("kind", "pypi")
    if not text:
        return jsonify({"error": "manifest is empty"}), 400
    return jsonify(generate_sbom(text, kind))


@app.route("/sbom/health")
def health():
    return jsonify({"status": "healthy", "service": "longhun-sbom",
                    "version": "1.0", "tricolor": "🟢"})


if __name__ == "__main__":
    # 命令行模式：python3 sbom.py requirements.txt [kind]
    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
        kind = sys.argv[2] if len(sys.argv) > 2 else "pypi"
        if p.exists():
            sbom = generate_sbom(
                p.read_text(encoding="utf-8", errors="ignore"), kind)
            print(json.dumps(sbom, indent=2, ensure_ascii=False))
        else:
            print(f"❌ 文件不存在: {p}")
        sys.exit(0)
    print("📦 SBOM 服务启动（随依赖隔离同驻或独立 :5002）")
    app.run(host="127.0.0.1", port=5002, debug=False)
