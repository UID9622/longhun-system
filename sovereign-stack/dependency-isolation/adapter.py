#!/usr/bin/env python3
"""
🐉 龍魂主权技术栈·依赖隔离适配层 v1.0
原则：能标准库不三方·三方必锁版本·来源可校验·供应链可追溯
端口：5001
DNA: #龍芯⚡️2026-08-31-DEPENDENCY-ISOLATION-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: MulanPSL v2（工程实现层）
"""

import re
import json
import sys
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 国内镜像源优先（人民币主权·自主可控）
PREFERRED_MIRRORS = {
    "pypi": "https://pypi.tuna.tsinghua.edu.cn/simple",
    "npm":  "https://registry.npmmirror.com",
    "go":   "https://goproxy.cn",
}

# 已知供应链风险模式
RISK_PATTERNS = [
    {"pattern": r">=",  "label": "未锁定精确版本", "level": "🟡",
     "advice": "建议锁定精确版本，防供应链投毒"},
    {"pattern": r"^\s*-e\s+git", "label": "直接从 git 安装", "level": "🟡",
     "advice": "git 依赖建议固定 commit"},
    {"pattern": r"^\s*-i\s+|^\s*--index", "label": "自定义索引源", "level": "🟡",
     "advice": "自定义索引源需人工确认可信"},
]

# 国产/自主可控优先白名单（域名）
DOMESTIC_HOSTS = [
    "pypi.tuna.tsinghua.edu.cn", "mirrors.aliyun.com",
    "mirrors.huaweicloud.com", "registry.npmmirror.com",
    "goproxy.cn", "gitee.com",
]


def parse_requirements(text: str) -> list:
    """解析 requirements.txt，返回依赖清单"""
    deps = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name = re.split(r"[<>=!~;\s]", line)[0]
        spec = re.findall(r"[<>=!~]+\s*[\w.\-*]+", line)
        deps.append({"name": name, "spec": " ".join(spec)})
    return deps


def check_dependencies(manifest_text: str, kind: str = "pypi") -> dict:
    """对依赖清单做隔离与供应链检查"""
    deps = parse_requirements(manifest_text)
    findings = []

    for dep in deps:
        # 无任何版本约束 = 风险
        if not dep["spec"]:
            findings.append({
                "dep": dep["name"],
                "level": "🔴",
                "label": "未指定版本",
                "advice": "必须锁定版本，否则依赖漂移+供应链风险",
            })
        else:
            for r in RISK_PATTERNS:
                if re.search(r["pattern"], " ".join(dep["spec"]), re.I):
                    findings.append({
                        "dep": dep["name"],
                        "level": r["level"],
                        "label": r["label"],
                        "advice": r["advice"],
                    })

    # 汇总三色
    red   = [f for f in findings if f["level"] == "🔴"]
    yello = [f for f in findings if f["level"] == "🟡"]
    green = [f for f in findings if f["level"] == "🟢"]

    return {
        "total_deps": len(deps),
        "findings": findings,
        "summary": {
            "🔴": len(red), "🟡": len(yello), "🟢": len(green),
        },
        "preferred_mirror": PREFERRED_MIRRORS.get(kind, PREFERRED_MIRRORS["pypi"]),
        "principle": "能标准库不三方·三方必锁版本·镜像走国内·来源可追溯",
        "dna": "#龍芯⚡️2026-08-31-DEP-CHECK-UID9622",
        "tricolor": "🔴" if red else ("🟡" if yello else "🟢"),
    }


@app.route("/adapter/check", methods=["POST"])
def check():
    """检查依赖清单（requirements.txt / package.json 文本）"""
    data = request.json or {}
    text = data.get("manifest", "")
    kind = data.get("kind", "pypi")
    if not text:
        return jsonify({"error": "manifest is empty", "tricolor": "🔴"}), 400
    return jsonify(check_dependencies(text, kind))


@app.route("/adapter/mirrors")
def mirrors():
    """返回推荐镜像源（国产优先）"""
    return jsonify({
        "mirrors": PREFERRED_MIRRORS,
        "note": "国内镜像优先·境外源仅作降级",
        "dna": "#龍芯⚡️2026-08-31-DEP-MIRRORS-UID9622",
        "tricolor": "🟢",
    })


@app.route("/adapter/health")
def health():
    return jsonify({"status": "healthy", "service": "longhun-dependency-isolation",
                    "port": 5001, "version": "1.0", "tricolor": "🟢"})


if __name__ == "__main__":
    # 命令行模式：python3 adapter.py requirements.txt
    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
        if p.exists():
            result = check_dependencies(p.read_text(encoding="utf-8", errors="ignore"))
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"❌ 文件不存在: {p}")
        sys.exit(0)
    print("🔒 依赖隔离适配层启动在 :5001")
    app.run(host="127.0.0.1", port=5001, debug=False)
