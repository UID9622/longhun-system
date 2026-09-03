#!/usr/bin/env python3
"""
🐉 龍魂主权技术栈·国产替代评估器 v1.0
原则：人民币主权·自主可控·能自建不申请·确需外部先国产
15条国产替代规则 · 逐条三色判定：🟢国产合规 / 🟡可替代待改进 / 🔴强制国产
DNA: #龍芯⚡️2026-08-31-EVALUATOR-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: MulanPSL v2（工程实现层）
"""

import re
import json
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ──────────────────────────────────────────
# 15条国产替代规则（人民币主权焊点 #IRON-YUAN-SOVEREIGNTY）
# ──────────────────────────────────────────
RULES = [
    {"id": "R01", "category": "API", "domestic": ["openai.tencent", "dashscope", "qianfan", "baidu", "volcengine", "doubao", "spark", "hunyuan", "wenxin", "zhipu", "bigmodel"],
     "foreign":  ["openai.com", "anthropic", "claude.ai", "api.gemini", "googleapis"],
     "note": "大模型/API：国产混元·通义·文心·豆包·智谱优先，OpenAI/Claude 强制国产"},
    {"id": "R02", "category": "云服务", "domestic": ["huaweicloud", "myhuaweicloud", "aliyuncs", "qcloud", "tencentcloud"],
     "foreign":  ["amazonaws", "azure", "cloud.google", "vercel", "netlify"],
     "note": "云主机：华为云/阿里云/腾讯云优先，AWS/Azure/GCP 强制国产"},
    {"id": "R03", "category": "数据库", "domestic": ["opengauss", "tidb", "oceanbase", "gaussdb", "dmdbms", "polardb", "doris"],
     "foreign":  ["oracle", "sqlserver", "mongodb.com", "aws-rds", "neon.tech"],
     "note": "数据库：openGauss/TiDB/OceanBase/GaussDB 优先"},
    {"id": "R04", "category": "对象存储", "domestic": ["obs", "myhuaweicloud.com", "cos.", "aliyuncs.com", "oss-"],
     "foreign":  ["s3.amazonaws", "s3.", "amazonaws", "storage.googleapis", "cloudflare-r2"],
     "note": "存储：OBS/COS/OSS 优先，S3 可替代"},
    {"id": "R05", "category": "搜索", "domestic": ["searxng", "baidu.com/s", "cn.bing", "bing.com"],
     "foreign":  ["google.com/search", "api.duckduckgo", "searchapi.io", "serpapi", "brave.com/search"],
     "note": "搜索：自建 SearXNG/百度/Bing 爬取，禁付费外部搜索 API（自建优先）"},
    {"id": "R06", "category": "地图", "domestic": ["amap.com", "lbs.amap", "api.map.baidu", "map.qq"],
     "foreign":  ["maps.google", "googleapis.com/maps", "mapbox"],
     "note": "地图：高德/百度/腾讯优先，Google Maps 强制国产"},
    {"id": "R07", "category": "支付", "domestic": ["alipay", "wechatpay", "wxpay", "tenpay"],
     "foreign":  ["stripe", "paypal", "square", "adyen"],
     "note": "支付：支付宝/微信支付/数字人民币优先"},
    {"id": "R08", "category": "推送", "domestic": ["jpush", "getui", "umeng"],
     "foreign":  ["fcm.googleapis", "apns", "onesignal", "pusher"],
     "note": "推送：极光/个推/友盟优先（境内业务强制）"},
    {"id": "R09", "category": "语音/OCR", "domestic": ["iflytek", "xfyun", "aip.baidubce", "aip.baidu"],
     "foreign":  ["speech.googleapis", "azure.microsoft.com", "aws.transcribe", "ocr.space"],
     "note": "语音/OCR：讯飞/百度优先"},
    {"id": "R10", "category": "代码托管", "domestic": ["gitee.com", "github.com"],
     "foreign":  ["gitlab.com", "bitbucket.org", "azure.devops"],
     "note": "托管：GitHub(主)/Gitee(镜像) 优先，境外 GitLab 可替代"},
    {"id": "R11", "category": "字体/前端资源", "domestic": ["fonts.loli.net", "cdn.bootcss", "lib.baomitu", "jsdelivr.net"],
     "foreign":  ["fonts.googleapis", "fonts.gstatic", "cdnjs.cloudflare", "unpkg.com"],
     "note": "字体/CDN：思源/本站自托管/国内镜像优先，Google Fonts 强制国产"},
    {"id": "R12", "category": "数据分析", "domestic": ["tongdun", "amap", "aliyun.com", "databricks"],
     "foreign":  ["google-analytics", "googletagmanager", "segment.com", "amplitude", "mixpanel"],
     "note": "分析：自建统计优先（龍魂=自研 bin/lh_search_engine.py），GA 强制国产"},
    {"id": "R13", "category": "邮件", "domestic": ["exmail.qq", "qiye.aliyun", "dm.aliyun"],
     "foreign":  ["gmail.com", "sendgrid", "mailgun", "postmark"],
     "note": "邮件：自建/腾讯企业邮/阿里企业邮优先"},
    {"id": "R14", "category": "CI/CD", "domestic": ["coding.net", "gitee.com"],
     "foreign":  ["github-actions", "circleci", "travis-ci", "gitlab-ci"],
     "note": "CI：腾讯 Coding/Gitee 优先；GitHub Actions 可接受（主仓托管在 GitHub）"},
    {"id": "R15", "category": "CDN/域名", "domestic": ["dnspod", "aliyun.com", "huaweicloud", "qcloud"],
     "foreign":  ["cloudflare", "akamai", "fastly", "route53", "awsdns"],
     "note": "CDN/解析：DNSPod/国内节点优先；Cloudflare 仅作境外加速降级"},
]


def evaluate_text(text: str) -> dict:
    """对配置/代码/文档文本跑 15 条规则"""
    low = text.lower()
    results = []
    for rule in RULES:
        hit_domestic = [kw for kw in rule["domestic"] if kw in low]
        hit_foreign  = [kw for kw in rule["foreign"]  if kw in low]
        if hit_foreign and not hit_domestic:
            level = "🔴"
        elif hit_foreign and hit_domestic:
            level = "🟡"
        elif hit_domestic:
            level = "🟢"
        else:
            continue  # 未涉及该类别·跳过
        results.append({
            "id": rule["id"],
            "category": rule["category"],
            "level": level,
            "hit_domestic": hit_domestic,
            "hit_foreign": hit_foreign,
            "note": rule["note"],
        })

    red   = sum(1 for r in results if r["level"] == "🔴")
    yello = sum(1 for r in results if r["level"] == "🟡")
    green = sum(1 for r in results if r["level"] == "🟢")

    return {
        "rules_total": len(RULES),
        "rules_checked": len(results),
        "results": results,
        "summary": {"🔴": red, "🟡": yello, "🟢": green},
        "tricolor": "🔴" if red else ("🟡" if yello else "🟢"),
        "principle": "人民币主权·自主可控·能自建不申请·确需外部先国产",
        "dna": "#龍芯⚡️2026-08-31-EVALUATOR-UID9622",
    }


@app.route("/evaluator/scan", methods=["POST"])
def scan():
    """扫描一段文本（配置/代码/README）"""
    data = request.json or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "text is empty"}), 400
    return jsonify(evaluate_text(text))


@app.route("/evaluator/rules")
def rules():
    """返回 15 条规则清单"""
    return jsonify({"rules": RULES, "count": len(RULES),
                    "tricolor": "🟢",
                    "dna": "#龍芯⚡️2026-08-31-EVALUATOR-RULES-UID9622"})


@app.route("/evaluator/health")
def health():
    return jsonify({"status": "healthy", "service": "longhun-evaluator",
                    "version": "1.0", "tricolor": "🟢"})


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行模式：python3 evaluator.py <file>
        p = sys.argv[1]
        try:
            text = open(p, encoding="utf-8", errors="ignore").read()
            result = evaluate_text(text)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"❌ {e}")
        sys.exit(0)
    print("⚖️ 国产替代评估器启动 :5003")
    app.run(host="127.0.0.1", port=5003, debug=False)
