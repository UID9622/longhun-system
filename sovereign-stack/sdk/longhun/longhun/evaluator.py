"""
🐉 15条国产替代规则评估器 v1.0
人民币主权 · 自主可控 · 能自建不申请 · 确需外部先国产
逐条三色判定：🟢国产合规 / 🟡可替代待改进 / 🔴强制国产

DNA: #龍芯⚡️2026-08-31-LONGHUN-EVALUATOR-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

# ──────────────────────────────────────────
# 15条国产替代规则（人民币主权焊点 #IRON-YUAN-SOVEREIGNTY）
# ──────────────────────────────────────────
RULES = [
    {"id": "R01", "category": "大模型/API", "domestic": ["hunyuan", "dashscope", "qianfan", "wenxin", "doubao", "volcengine", "zhipu", "bigmodel", "spark"],
     "foreign":  ["openai.com", "anthropic", "claude.ai", "api.gemini", "googleapis"],
     "note": "混元/通义/文心/豆包/智谱优先，OpenAI/Claude 强制国产"},
    {"id": "R02", "category": "云服务", "domestic": ["huaweicloud", "myhuaweicloud", "aliyuncs", "qcloud", "tencentcloud"],
     "foreign":  ["amazonaws", "azure", "cloud.google", "vercel", "netlify"],
     "note": "华为云/阿里云/腾讯云优先，AWS/Azure 强制国产"},
    {"id": "R03", "category": "数据库", "domestic": ["opengauss", "tidb", "oceanbase", "gaussdb", "dmdbms", "polardb", "doris"],
     "foreign":  ["oracle", "sqlserver", "mongodb.com", "neon.tech"],
     "note": "openGauss/TiDB/OceanBase/GaussDB 优先"},
    {"id": "R04", "category": "对象存储", "domestic": ["obs", "cos.", "oss-", "myhuaweicloud"],
     "foreign":  ["s3.amazonaws", "storage.googleapis", "cloudflare-r2"],
     "note": "OBS/COS/OSS 优先，S3 可替代"},
    {"id": "R05", "category": "搜索", "domestic": ["searxng", "baidu.com/s", "cn.bing", "bing.com"],
     "foreign":  ["google.com/search", "api.duckduckgo", "serpapi", "brave.com/search"],
     "note": "自建 SearXNG/百度/Bing 优先，禁付费外部搜索 API"},
    {"id": "R06", "category": "地图", "domestic": ["amap.com", "lbs.amap", "api.map.baidu", "map.qq"],
     "foreign":  ["maps.google", "mapbox"],
     "note": "高德/百度/腾讯地图优先，Google Maps 强制国产"},
    {"id": "R07", "category": "支付", "domestic": ["alipay", "wechatpay", "wxpay", "tenpay"],
     "foreign":  ["stripe", "paypal", "adyen"],
     "note": "支付宝/微信支付/数字人民币优先"},
    {"id": "R08", "category": "推送", "domestic": ["jpush", "getui", "umeng"],
     "foreign":  ["fcm.googleapis", "apns", "onesignal"],
     "note": "极光/个推/友盟优先（境内业务强制）"},
    {"id": "R09", "category": "语音/OCR", "domestic": ["iflytek", "xfyun", "aip.baidubce"],
     "foreign":  ["speech.googleapis", "aws.transcribe", "ocr.space"],
     "note": "讯飞/百度优先"},
    {"id": "R10", "category": "代码托管", "domestic": ["gitee.com"],
     "foreign":  ["gitlab.com", "bitbucket.org"],
     "note": "GitHub(主)/Gitee(镜像) 优先，境外 GitLab 可替代"},
    {"id": "R11", "category": "字体/前端资源", "domestic": ["fonts.loli.net", "cdn.bootcss", "lib.baomitu"],
     "foreign":  ["fonts.googleapis", "fonts.gstatic", "cdnjs.cloudflare", "unpkg.com"],
     "note": "思源/自托管/国内镜像优先，Google Fonts 强制国产"},
    {"id": "R12", "category": "数据分析", "domestic": ["aliyun", "umeng"],
     "foreign":  ["google-analytics", "googletagmanager", "segment.com", "amplitude", "mixpanel"],
     "note": "自建统计优先，GA 强制国产"},
    {"id": "R13", "category": "邮件", "domestic": ["exmail.qq", "qiye.aliyun"],
     "foreign":  ["gmail.com", "sendgrid", "mailgun"],
     "note": "自建/腾讯企业邮/阿里企业邮优先"},
    {"id": "R14", "category": "CI/CD", "domestic": ["coding.net"],
     "foreign":  ["github-actions", "circleci", "travis-ci", "gitlab-ci"],
     "note": "腾讯 Coding 优先；GitHub Actions 可接受（主仓托管在 GitHub）"},
    {"id": "R15", "category": "CDN/域名", "domestic": ["dnspod", "qcloud", "aliyun.com"],
     "foreign":  ["cloudflare", "akamai", "fastly", "route53"],
     "note": "DNSPod/国内节点优先；Cloudflare 仅作境外降级"},
]


def scan_text(text: str) -> dict:
    """对配置/代码/文档文本跑 15 条规则"""
    low = (text or "").lower()
    results = []
    for rule in RULES:
        hit_domestic = [kw for kw in rule["domestic"] if kw in low]
        hit_foreign = [kw for kw in rule["foreign"] if kw in low]
        if hit_foreign and not hit_domestic:
            level = "🔴"
        elif hit_foreign and hit_domestic:
            level = "🟡"
        elif hit_domestic:
            level = "🟢"
        else:
            continue
        results.append({
            "id": rule["id"], "category": rule["category"], "level": level,
            "hit_domestic": hit_domestic, "hit_foreign": hit_foreign,
            "note": rule["note"],
        })
    red = sum(1 for r in results if r["level"] == "🔴")
    yello = sum(1 for r in results if r["level"] == "🟡")
    green = sum(1 for r in results if r["level"] == "🟢")
    return {
        "rules_checked": len(results),
        "results": results,
        "summary": {"🔴": red, "🟡": yello, "🟢": green},
        "tricolor": "🔴" if red else ("🟡" if yello else "🟢"),
        "principle": "人民币主权·自主可控·能自建不申请·确需外部先国产",
    }


def scan_file(path: str) -> dict:
    with open(path, encoding="utf-8", errors="ignore") as f:
        return scan_text(f.read())
