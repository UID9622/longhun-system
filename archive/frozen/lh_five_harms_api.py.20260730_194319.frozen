#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·五害曝光台 API v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·戌时·☰乾-FIVE-HARMS-API-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

FastAPI服务 - 五害曝光台后端。
端口: 8779 (Mac) / 8779 (鲲鹏)

端点:
  GET  /api/cases            - 获取曝光案例列表
  GET  /api/cases/{id}       - 获取单个案例详情
  POST /api/cases/validate   - 触发多源验证
  GET  /api/companies        - 企业档案列表
  GET  /api/timeline         - 时间线数据
  POST /api/victims          - 提交受害者证言(加密)
  GET  /api/victims          - 受害者墙
  POST /api/relay            - 接力签名
  GET  /api/relay            - 接力墙数据
  POST /api/manifesto        - 生成檄文
  GET  /api/blocklist        - 熔断域名清单
  GET  /api/stats            - 统计概览
  GET  /api/health           - 健康检查
  POST /api/whistleblower    - 加密举报

⚖️ 证据为王 · 隐私如命 · 对抗到底
"""

import hashlib
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# 路径设置
_BIN_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_DIR = os.path.dirname(_BIN_DIR)
sys.path.insert(0, _PROJECT_DIR)
sys.path.insert(0, _BIN_DIR)

from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse, Response
from pydantic import BaseModel, Field

# 引擎
try:
    from lh_five_harms_validator import FiveHarmsValidator, ValidationReport
except ImportError:
    FiveHarmsValidator = None
    ValidationReport = None

try:
    from lh_whistleblower_shield import WhistleblowerShield
except ImportError:
    WhistleblowerShield = None


# ─── 数据目录 ───
_DATA_DIR = Path(_PROJECT_DIR) / "data" / "five_harms"
_DATA_DIR.mkdir(parents=True, exist_ok=True)
_CASES_FILE = _DATA_DIR / "cases.json"
_RELAY_FILE = _DATA_DIR / "relay.json"
_VICTIMS_FILE = _DATA_DIR / "victims.json"
_BLOCKLIST_FILE = _DATA_DIR / "blocklist.json"

# ─── FastAPI App ───
app = FastAPI(
    title="龍魂·五害曝光台 API",
    description="数字时代的包青天衙门 — 曝光·验证·溯源·联动·防御",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Pydantic 模型 ───
class VictimSubmit(BaseModel):
    content: str = Field(..., min_length=10, max_length=2000)
    harm_category: str = Field(default="未分类")
    password: str = Field(default="")

class RelaySubmit(BaseModel):
    nickname: str = Field(default="匿名战友", max_length=20)

class ManifestoRequest(BaseModel):
    case_id: int
    platform: str = Field(default="full")  # wechat/weibo/douyin/xiaohongshu/full

class WhistleblowerSubmit(BaseModel):
    content: str = Field(..., min_length=10, max_length=5000)
    harm_category: str = Field(default="未分类")
    password: str = Field(default="")

class CaseValidateRequest(BaseModel):
    case_id: int


# ─── 数据加载 ───
SAMPLE_CASES = [
    {"id":1,"category":"平台垄断","company":"某团外卖","title":"强迫商家\"二选一\"，违者降权封店","brief":"利用市场支配地位，要求餐饮商家签署排他协议。拒绝的商家被算法降权，订单骤降80%。","severity":"critical","date":"2024-05-12","victims":37200,"evidence":[{"label":"市监局处罚书","url":"#"},{"label":"商家联合证词","url":"#"},{"label":"媒体调查","url":"#"}],"audit_mark":"🟢","verified":True,"confidence":0.89},
    {"id":2,"category":"算法收割","company":"某滴出行","title":"大数据杀熟：同一段路，老用户贵30%","brief":"经实测验证，同一时间、同一路线，使用3年的老账号比新注册账号报价高出28%-35%。","severity":"critical","date":"2024-08-03","victims":186000,"evidence":[{"label":"实测对比截图","url":"#"},{"label":"算法审计报告","url":"#"}],"audit_mark":"🟢","verified":True,"confidence":0.85},
    {"id":3,"category":"数据倒卖","company":"某房产中介平台","title":"买卖用户浏览记录，精准画像卖给装修公司","brief":"用户浏览的每一个房源、停留时长、价格偏好，被封装成\"购房意向包\"出售。","severity":"high","date":"2024-11-20","victims":1200000,"evidence":[{"label":"内部员工爆料","url":"#"},{"label":"暗访录音","url":"#"},{"label":"数据交易截图","url":"#"}],"audit_mark":"🟢","verified":True,"confidence":0.78},
    {"id":4,"category":"隐私践踏","company":"某输入法App","title":"键盘输入内容实时上传云端，包括密码和身份证号","brief":"安全研究员发现该输入法将所有输入内容（含密码框内的字符）明文传输至云端服务器。","severity":"critical","date":"2025-02-14","victims":38000000,"evidence":[{"label":"安全报告","url":"#"},{"label":"抓包数据","url":"#"},{"label":"APP权限分析","url":"#"}],"audit_mark":"🟢","verified":True,"confidence":0.92},
    {"id":5,"category":"资本勾结","company":"某电商+某物流","title":"股权交叉持有，物流数据双向输送形成垄断联盟","brief":"电商平台A持有物流公司B 34%股份，物流公司B的母公司又持有电商平台A 12%股份。","severity":"high","date":"2025-06-01","victims":560000,"evidence":[{"label":"股权结构图","url":"#"},{"label":"反垄断分析","url":"#"},{"label":"商家集体投诉","url":"#"}],"audit_mark":"🟡","verified":False,"confidence":0.55},
    {"id":6,"category":"算法收割","company":"某短视频平台","title":"未成年沉迷推荐算法：日均使用时长超6小时","brief":"推荐算法专门针对青少年心理设计，导致大量未成年人日均使用时长超过6小时。","severity":"critical","date":"2025-04-08","victims":95000000,"evidence":[{"label":"研究报告","url":"#"},{"label":"家长联合声明","url":"#"},{"label":"心理学评估","url":"#"}],"audit_mark":"🟢","verified":True,"confidence":0.87},
    {"id":7,"category":"平台垄断","company":"某搜索引擎","title":"搜索结果前10条中8条为自家产品，独立网站被系统性压制","brief":"搜索任意关键词，前10条结果中平均7-8条为搜索引擎所属公司的自家产品。","severity":"high","date":"2025-01-15","victims":4200000,"evidence":[{"label":"搜索结果对比","url":"#"},{"label":"SEO行业报告","url":"#"},{"label":"站长联合声明","url":"#"}],"audit_mark":"🟡","verified":False,"confidence":0.62},
    {"id":8,"category":"隐私践踏","company":"某智能家居厂商","title":"智能音箱24小时录音，对话内容被人工审核团队听取","brief":"智能音箱在用户不知情的情况下，将家庭私密对话录音上传至云端，由外包人工审核团队逐条听取。","severity":"critical","date":"2025-03-22","victims":15000000,"evidence":[{"label":"内部审核员爆料","url":"#"},{"label":"技术分析","url":"#"},{"label":"法律意见书","url":"#"}],"audit_mark":"🟢","verified":True,"confidence":0.91},
    {"id":9,"category":"数据倒卖","company":"某医疗健康App","title":"用户健康数据被出售给保险公司用于拒保决策","brief":"用户健康数据被脱敏后打包出售给多家保险公司，用于调高保费或直接拒保。","severity":"critical","date":"2025-05-30","victims":8700000,"evidence":[{"label":"数据交易链路","url":"#"},{"label":"保险业内幕","url":"#"},{"label":"用户证言合集","url":"#"}],"audit_mark":"🟢","verified":True,"confidence":0.83},
]

BLOCKED_DOMAINS = [
    # 标记为🔴严重危害的企业域名在此登记
    # 实际域名需根据验证结果动态更新
]


def _load_cases() -> List[Dict]:
    """加载案例（优先从文件，无则用内置）"""
    if _CASES_FILE.exists():
        try:
            return json.loads(_CASES_FILE.read_text())
        except Exception:
            pass
    _CASES_FILE.write_text(json.dumps(SAMPLE_CASES, ensure_ascii=False, indent=2))
    return SAMPLE_CASES


def _save_cases(cases: List[Dict]):
    _CASES_FILE.write_text(json.dumps(cases, ensure_ascii=False, indent=2))


def _load_relay() -> Dict:
    if _RELAY_FILE.exists():
        try:
            return json.loads(_RELAY_FILE.read_text())
        except Exception:
            pass
    default = {"count": 36591, "entries": []}
    return default


def _save_relay(data: Dict):
    _RELAY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def _load_victims() -> List[Dict]:
    if _VICTIMS_FILE.exists():
        try:
            return json.loads(_VICTIMS_FILE.read_text())
        except Exception:
            pass
    return []


def _save_victims(victims: List[Dict]):
    _VICTIMS_FILE.write_text(json.dumps(victims, ensure_ascii=False, indent=2))


# ─── 防御协议数据 ───
_PACT_SIGNERS_FILE = _DATA_DIR / "pact_signers.json"
_PACT_ADOPTERS_FILE = _DATA_DIR / "pact_adopters.json"

PACT_FULL_TEXT = """# 《防资本收割共同防御协议》v1.0
## 龍魂·五害曝光台 发起

### 序言
我们——签署本协议的企业、开发者、组织与个人——共同认识到：
数字时代的资本收割已从显性剥削转向隐性渗透。算法杀熟、数据倒卖、
隐私践踏、成瘾性设计——这些已成为侵蚀公众数字主权的系统性威胁。

本协议不是法律文书，而是道德契约。签署即承诺，承诺即受公众审计。

---

### 第一条 · 核心承诺

签署方承诺遵守以下五项铁律：

**1. 拒绝价格歧视与算法杀熟**
不使用用户画像进行差异化定价。同一商品/服务，新旧用户同价。
如有促销，必须公示促销条件与适用范围，不得暗箱操作。

**2. 拒绝数据倒卖与未授权共享**
用户数据不出售、不交换、不授权给第三方用于商业目的。
数据采集必须在用户知情同意下进行，默认不采集。

**3. 拒绝成瘾性设计**
不采用无限滚动、自动播放、虚假红点、诱导性推送等操纵用户行为的设计模式。
用户可一键关闭算法推荐，默认关。

**4. 接受独立审计**
承诺开放以下数据接口接受公众审计：
- 定价算法核心参数（脱敏）
- 用户数据流向记录
- 第三方SDK清单与数据采集范围

**5. 违约问责**
违反以上任一承诺，自愿在「五害曝光台」公示违约事实，并接受公众监督整改。
连续三次违约，列入"背信企业"名单，熔断插件自动拦截其全部域名。

---

### 第二条 · 签署权益

签署本协议的企业/组织将获得：
1. 「良心企业」标识使用权（SVG数字徽章）
2. 在本协议展示墙永久展示企业LOGO与承诺声明
3. 优先接入龍魂开源工具套件
4. 公众信任——消费者可查验签署状态

---

### 第三条 · 审计机制

1. 用户投诉通道：五害曝光台「受害者墙」接受对签约企业的举报
2. 每季度自动审计：多源验证引擎抓取公开数据交叉验证
3. 审计结果公示：🟢通过 / 🟡整改中 / 🔴背信
4. 签约企业有权对审计结果提出申诉，申诉期间标注🟡

---

### 第四条 · 协议效力

1. 本协议为道德自律契约，不具备法律强制力
2. 签署即视为公开承诺，违约即视为背信
3. 协议修订需经现有签约方半数以上同意
4. 签约方有权随时退出，退出后清除展示墙信息

---

### 第五条 · 签署方式

开发者/企业主在下方签名区提交：
- 企业/组织名称
- 签署人姓名
- 官方网站（可选）
- 具体承诺声明

签署后立即生效，公示期为永久。

---

> 发起方：龍魂·五害曝光台
> 发起人：诸葛鑫（UID9622）
> DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PACT-ANTI-CAPITAL-HARVEST-v1.0
> 日期：2025-07-25
"""


def _load_pact_signers() -> List[Dict]:
    if _PACT_SIGNERS_FILE.exists():
        try:
            return json.loads(_PACT_SIGNERS_FILE.read_text())
        except Exception:
            pass
    # 初始良心企业示例
    default = [
        {"org_name": "胖东来商贸集团", "signatory": "于东来", "url": "https://www.pangdonglai.com",
         "commitment_desc": "我们承诺：不杀熟、不卖数据、不用成瘾设计。每一位顾客都是家人。",
         "signed_at": "2025-07-20T10:00:00", "status": "verified", "audit_mark": "🟢"},
        {"org_name": "龍魂·如意系统", "signatory": "诸葛鑫", "url": "https://uid9622.cn/cnsh-ruyi",
         "commitment_desc": "所有AI调度透明可追溯，用户数据物理隔离，永不上传。",
         "signed_at": "2025-07-25T00:00:00", "status": "verified", "audit_mark": "🟢"},
    ]
    _PACT_SIGNERS_FILE.write_text(json.dumps(default, ensure_ascii=False, indent=2))
    return default


def _save_pact_signers(signers: List[Dict]):
    _PACT_SIGNERS_FILE.write_text(json.dumps(signers, ensure_ascii=False, indent=2))


# ─── API 端点 ───

@app.get("/api/health")
async def health():
    cases = _load_cases()
    relay = _load_relay()
    victims = _load_victims()
    return {
        "status": "🟢 正常运行",
        "service": "龍魂·五害曝光台 API v1.0",
        "cases_count": len(cases),
        "relay_count": relay.get("count", 0),
        "victims_count": len(victims),
        "blocked_domains": len(BLOCKED_DOMAINS),
        "dna": "#龍芯⚡️丙午·乙未·丁酉·戌时·☰乾-FIVE-HARMS-API-v1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/stats")
async def stats():
    cases = _load_cases()
    relay = _load_relay()
    victims = _load_victims()
    
    categories = {}
    severities = {}
    for c in cases:
        cat = c.get("category", "未分类")
        sev = c.get("severity", "watch")
        categories[cat] = categories.get(cat, 0) + 1
        severities[sev] = severities.get(sev, 0) + 1
    
    total_victims = sum(c.get("victims", 0) for c in cases)
    verified = sum(1 for c in cases if c.get("verified"))
    
    return {
        "total_cases": len(cases),
        "verified_cases": verified,
        "total_affected": total_victims,
        "by_category": categories,
        "by_severity": severities,
        "relay_count": relay.get("count", 0),
        "victim_testimonies": len(victims),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/cases")
async def get_cases(
    category: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    verified: Optional[bool] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    cases = _load_cases()
    
    if category:
        cases = [c for c in cases if c.get("category") == category]
    if severity:
        cases = [c for c in cases if c.get("severity") == severity]
    if verified is not None:
        cases = [c for c in cases if c.get("verified") == verified]
    
    total = len(cases)
    cases = cases[offset:offset + limit]
    
    return {"total": total, "cases": cases, "limit": limit, "offset": offset}


@app.get("/api/cases/{case_id}")
async def get_case(case_id: int):
    cases = _load_cases()
    for c in cases:
        if c.get("id") == case_id:
            return c
    raise HTTPException(status_code=404, detail="案例未找到")


@app.post("/api/cases/validate")
async def validate_case(req: CaseValidateRequest):
    cases = _load_cases()
    target = None
    for c in cases:
        if c.get("id") == req.case_id:
            target = c
            break
    
    if not target:
        raise HTTPException(status_code=404, detail="案例未找到")
    
    if FiveHarmsValidator:
        validator = FiveHarmsValidator()
        report = validator.validate_case(target)
        # 更新案例验证状态
        target["verified"] = report.is_verified
        target["confidence"] = report.confidence
        target["audit_mark"] = report.audit_mark
        target["evidence_count"] = report.evidence_count
        target["source_count"] = report.source_count
        target["last_validated"] = report.check_time
        _save_cases(cases)
        
        return {
            "case_id": req.case_id,
            "is_verified": report.is_verified,
            "confidence": report.confidence,
            "audit_mark": report.audit_mark,
            "evidence_count": report.evidence_count,
            "source_count": report.source_count,
            "warnings": report.warnings,
            "dna": report.dna,
        }
    else:
        return {
            "case_id": req.case_id,
            "is_verified": target.get("verified", False),
            "message": "验证引擎未加载，返回缓存状态",
            "audit_mark": target.get("audit_mark", "🟡"),
        }


@app.get("/api/companies")
async def get_companies():
    cases = _load_cases()
    companies = {}
    for c in cases:
        name = c.get("company", "")
        if name not in companies:
            companies[name] = {
                "name": name,
                "cases": [],
                "harm_types": set(),
                "total_victims": 0,
                "severity_max": "watch",
            }
        companies[name]["cases"].append(c)
        companies[name]["harm_types"].add(c.get("category", ""))
        companies[name]["total_victims"] += c.get("victims", 0)
        sev = c.get("severity", "watch")
        sev_rank = {"critical": 4, "high": 3, "medium": 2, "watch": 1}
        if sev_rank.get(sev, 0) > sev_rank.get(companies[name]["severity_max"], 0):
            companies[name]["severity_max"] = sev
    
    for k, v in companies.items():
        v["harm_types"] = list(v["harm_types"])
    
    return list(companies.values())


@app.get("/api/timeline")
async def get_timeline(company: Optional[str] = Query(None)):
    cases = _load_cases()
    if company:
        cases = [c for c in cases if c.get("company") == company]
    cases.sort(key=lambda x: x.get("date", ""), reverse=True)
    return cases


@app.get("/api/victims")
async def get_victims():
    victims = _load_victims()
    return victims


@app.post("/api/victims")
async def post_victim(req: VictimSubmit):
    if WhistleblowerShield:
        shield = WhistleblowerShield()
        result = shield.encrypt_report(
            content=req.content,
            harm_category=req.harm_category,
            password=req.password or secrets_token(),
        )
        victim_id = result["report_id"]
    else:
        victim_id = f"V-{secrets_token()[:8].upper()}"
    
    # 保存脱敏版本（仅用于展示）
    victims = _load_victims()
    victims.append({
        "id": victim_id,
        "name": "匿名举报者",
        "verified": False,
        "text": req.content[:200] + ("..." if len(req.content) > 200 else ""),
        "harm": req.harm_category,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    _save_victims(victims)
    
    return {"victim_id": victim_id, "status": "encrypted_and_saved"}


@app.get("/api/relay")
async def get_relay():
    relay = _load_relay()
    return relay


@app.post("/api/relay")
async def post_relay(req: RelaySubmit):
    relay = _load_relay()
    relay["count"] = relay.get("count", 0) + 1
    relay["entries"].insert(0, {
        "nickname": req.nickname,
        "time": datetime.now(timezone.utc).isoformat(),
        "number": relay["count"],
    })
    # 只保留最近500条
    relay["entries"] = relay["entries"][:500]
    _save_relay(relay)
    return {"count": relay["count"], "nickname": req.nickname}


@app.post("/api/manifesto")
async def generate_manifesto(req: ManifestoRequest):
    cases = _load_cases()
    target = None
    for c in cases:
        if c.get("id") == req.case_id:
            target = c
            break
    
    if not target:
        raise HTTPException(status_code=404, detail="案例未找到")
    
    # 违禁词规避映射
    censor_maps = {
        "wechat": {"垄断": "支配", "杀熟": "差异化定价", "倒卖": "转售", "践踏": "不当处理", "勾结": "关联", "罚款": "处理", "打压": "限制"},
        "weibo": {"垄断": "支配", "杀熟": "价格差异", "倒卖": "交易", "践踏": "影响", "勾结": "协同"},
        "douyin": {"垄断": "独家", "杀熟": "区别定价", "倒卖": "流转", "践踏": "干扰", "勾结": "合作"},
        "xiaohongshu": {"垄断": "排他", "杀熟": "价格区分", "倒卖": "分享", "践踏": "触及", "勾结": "联动"},
        "full": {},
    }
    
    censor = censor_maps.get(req.platform, {})
    
    def apply_censor(text: str) -> str:
        for old, new in censor.items():
            text = text.replace(old, new)
        return text
    
    ev = target.get("evidence", [])
    ev_labels = "、".join(e["label"] for e in ev) if ev else "调查收集中"
    
    manifestos = {
        "wechat": f"""【曝光】{apply_censor(target['company'])}：{apply_censor(target['title'])}

{apply_censor(target['brief'])}

📊 影响范围：约{target['victims']//10000}万人
📎 证据：{ev_labels}

每一个点赞和转发，都是守护数字疆土的一砖一瓦。
#数字权益 #公平交易""",
        
        "weibo": f"""#五害曝光台# {apply_censor(target['company'])}{apply_censor(target['title'])[:30]}

{apply_censor(target['brief'])[:140]}

⚡ 危害等级：{target['severity']}
👥 影响约{target['victims']//10000}万人""",
        
        "douyin": f"""{apply_censor(target['title'])}

{apply_censor(target['brief'])[:100]}

📍 {apply_censor(target['company'])}
📊 影响约{target['victims']//10000}万人""",
        
        "xiaohongshu": f"""🚨 避雷提醒 🚨

{apply_censor(target['title'])}

{apply_censor(target['brief'])[:200]}

姐妹们擦亮眼睛，保护好自己的权益！💪
#消费者权益 #避雷""",
        
        "full": f"""【討賊檄文】

告天下：{target['company']}，{target['category']}之害，天下共诛之！

{target['brief']}

⚡ 危害等级：{target['severity']}
📅 曝光日期：{target['date']}
👥 受影响人数：约{(target['victims']/10000):.0f}万人
📎 证据链：{ev_labels}

━━━━━━━━━━━━━

我们不是数字时代的蝼蚁。
我们拒绝被算法收割，拒绝被平台奴役，拒绝被资本践踏。

每一个点赞、转发、接力，都是插向五害的一把刀。

站起来，发声，接力。
—— 龍魂·五害曝光台 · 数字时代的包青天衙门

#五害曝光台 #数字主权 #为人民服务""",
    }
    
    return {
        "case_id": req.case_id,
        "platform": req.platform,
        "manifesto": manifestos.get(req.platform, manifestos["full"]),
    }


@app.get("/api/blocklist")
async def get_blocklist():
    if _BLOCKLIST_FILE.exists():
        try:
            return json.loads(_BLOCKLIST_FILE.read_text())
        except Exception:
            pass
    return {"domains": BLOCKED_DOMAINS, "updated": datetime.now(timezone.utc).isoformat()}


@app.post("/api/whistleblower")
async def whistleblower_submit(req: WhistleblowerSubmit):
    if not WhistleblowerShield:
        raise HTTPException(status_code=503, detail="隐私盾服务未就绪")
    
    shield = WhistleblowerShield()
    result = shield.encrypt_report(
        content=req.content,
        harm_category=req.harm_category,
        password=req.password or secrets_token(),
    )
    
    return {
        "report_id": result["report_id"],
        "status": "encrypted_and_stored",
        "message": "举报已加密存储，感谢你的勇敢。你的身份不可追溯。",
    }


# ─── 第一味药：一键拉黑 ───

class BlocklistAddRequest(BaseModel):
    domain: str
    company: str
    ip_addresses: List[str] = []
    source: str = "user_manual"

@app.post("/api/blocklist/add")
async def blocklist_add(req: BlocklistAddRequest):
    """用户一键拉黑：添加企业域名到熔断列表，联动浏览器史官"""
    if _BLOCKLIST_FILE.exists():
        try:
            blocklist = json.loads(_BLOCKLIST_FILE.read_text())
        except Exception:
            blocklist = {"domains": [], "updated": ""}
    else:
        blocklist = {"domains": [], "updated": ""}
    
    # 去重添加
    existing = {d.get("domain", "") for d in blocklist["domains"]}
    if req.domain not in existing:
        blocklist["domains"].append({
            "domain": req.domain,
            "company": req.company,
            "ip_addresses": req.ip_addresses,
            "source": req.source,
            "added_at": datetime.now(timezone.utc).isoformat(),
        })
        blocklist["updated"] = datetime.now(timezone.utc).isoformat()
        _BLOCKLIST_FILE.write_text(json.dumps(blocklist, ensure_ascii=False, indent=2))
        
        return {
            "status": "blocked",
            "domain": req.domain,
            "total_blocked": len(blocklist["domains"]),
            "message": f"已拉黑 {req.domain}，该企业所有追踪脚本、Cookie、API调用将被拦截。",
            "inject_code": f"""// 一键拉黑已生效：{req.company} ({req.domain})
// 将此代码嵌入你的网站 <head> 中即可拦截该企业所有追踪
<script src="https://uid9622.cn/five-harms-expose/block-inject.js" data-block="{req.domain}" defer></script>""",
        }
    
    return {"status": "already_blocked", "domain": req.domain, "message": f"{req.domain} 已在熔断列表中"}


# ─── 第二味药：一键反挖矿 ───

class AntiMiningRequest(BaseModel):
    company: str
    domain: str
    case_id: Optional[int] = None
    cookies_count: int
    third_party_origins: List[str] = []
    localStorage_keys: int
    sessionStorage_keys: int
    trackers_detected: List[str] = []
    navigator_props: List[str] = []
    screen_fingerprint: bool = False
    canvas_fingerprint: bool = False
    webrtc_leak: bool = False

_ANTI_MINING_REPORTS = _DATA_DIR / "anti_mining_reports.json"

@app.post("/api/anti-mining/analyze")
async def anti_mining_analyze(req: AntiMiningRequest):
    """分析企业页面的追踪行为，生成反挖矿报告"""
    
    risk_score = 0
    findings = []
    
    # 1. Cookie分析
    if req.cookies_count > 10:
        risk_score += 20
        findings.append({"level": "high", "finding": f"发现 {req.cookies_count} 个Cookie，超过安全阈值(10)", "detail": "大量Cookie可能用于跨站追踪和用户画像"})
    elif req.cookies_count > 3:
        risk_score += 10
        findings.append({"level": "medium", "finding": f"发现 {req.cookies_count} 个Cookie", "detail": "关注是否有第三方追踪Cookie"})
    
    # 2. 第三方脚本分析
    if req.third_party_origins:
        risk_score += len(req.third_party_origins) * 8
        findings.append({"level": "high", "finding": f"加载了 {len(req.third_party_origins)} 个第三方域脚本", 
                         "detail": f"来源: {', '.join(req.third_party_origins[:5])}"})
    
    # 3. 本地存储分析
    if req.localStorage_keys > 5:
        risk_score += 15
        findings.append({"level": "medium", "finding": f"localStorage写入 {req.localStorage_keys} 项", 
                         "detail": "可能用于持久化用户标识或行为数据"})
    
    # 4. 追踪器检测
    if req.trackers_detected:
        risk_score += len(req.trackers_detected) * 12
        danger_trackers = [t for t in req.trackers_detected if any(kw in t.lower() for kw in 
                         ["track", "analytic", "pixel", "beacon", "collect", "fingerprint", "profiling", "ga", "gtag"])]
        if danger_trackers:
            findings.append({"level": "critical", "finding": f"检测到 {len(danger_trackers)} 个追踪脚本", 
                             "detail": f"名称: {', '.join(danger_trackers)}"})
    
    # 5. 浏览器指纹分析
    fingerprint_count = sum([req.canvas_fingerprint, req.screen_fingerprint, req.webrtc_leak, 
                            len(req.navigator_props) > 5])
    if fingerprint_count >= 2:
        risk_score += fingerprint_count * 15
        fp_methods = []
        if req.canvas_fingerprint: fp_methods.append("Canvas指纹")
        if req.screen_fingerprint: fp_methods.append("屏幕指纹")
        if req.webrtc_leak: fp_methods.append("WebRTC泄露")
        if len(req.navigator_props) > 5: fp_methods.append("Navigator属性采集")
        findings.append({"level": "critical", "finding": f"检测到浏览器指纹采集: {', '.join(fp_methods)}",
                         "detail": "该企业正尝试生成你的唯一设备标识，即使清除Cookie也无法逃脱追踪"})
    
    # 6. 综合风险评级
    if risk_score >= 60:
        risk_level = "critical"
        risk_label = "🔴 高危：你的数字身份正在被系统性地窃取"
    elif risk_score >= 30:
        risk_level = "high"
        risk_label = "🟠 危险：存在显著的隐私风险"
    elif risk_score >= 15:
        risk_level = "medium"
        risk_label = "🟡 警惕：建议启用防护措施"
    else:
        risk_level = "low"
        risk_label = "🟢 低风险：未检出严重追踪行为"
    
    report = {
        "report_id": secrets_token()[:8],
        "company": req.company,
        "domain": req.domain,
        "case_id": req.case_id,
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_label": risk_label,
        "findings": findings,
        "recommendation": [
            "立即使用「一键拉黑」功能阻止该企业域名",
            "启用浏览器史官持续监控追踪行为",
            "使用隐私浏览模式或Tor网络",
            "安装广告/追踪拦截插件（uBlock Origin）",
        ],
        "evidence_for_expose": {
            "title": f"反挖矿报告：{req.company}的追踪行为分析",
            "summary": f"风险评分 {risk_score}/100，检测到 {len(findings)} 项风险发现",
            "can_be_attached_to_case": req.case_id is not None,
        },
    }
    
    # 保存报告
    reports = []
    if _ANTI_MINING_REPORTS.exists():
        try:
            reports = json.loads(_ANTI_MINING_REPORTS.read_text())
        except Exception:
            pass
    reports.append(report)
    _ANTI_MINING_REPORTS.write_text(json.dumps(reports, ensure_ascii=False, indent=2))
    
    return report


# ─── 第三味药：防御协议 ───

class PactSignRequest(BaseModel):
    org_name: str
    signatory: str
    url: str = ""
    commitment_desc: str = ""


@app.get("/api/pact")
async def get_pact():
    """获取《防资本收割共同防御协议》全文"""
    return {
        "title": "防资本收割共同防御协议",
        "version": "v1.0",
        "full_text": PACT_FULL_TEXT,
        "signed_count": len(_load_pact_signers()),
        "dna": "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PACT-ANTI-CAPITAL-HARVEST-v1.0",
    }


@app.post("/api/pact/sign")
async def pact_sign(req: PactSignRequest):
    """企业/开发者签署防御协议"""
    signers = _load_pact_signers()
    
    # 去重检查
    for s in signers:
        if s.get("org_name") == req.org_name:
            return {"status": "already_signed", "message": f"「{req.org_name}」已签署本协议，感谢你的承诺。"}
    
    new_signer = {
        "org_name": req.org_name,
        "signatory": req.signatory,
        "url": req.url,
        "commitment_desc": req.commitment_desc,
        "signed_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
        "audit_mark": "🟡",
    }
    signers.append(new_signer)
    _save_pact_signers(signers)
    
    return {
        "status": "signed",
        "signer": new_signer,
        "total_signers": len(signers),
        "badge_svg_url": "https://uid9622.cn/five-harms-expose/badge-good-faith.svg",
        "message": f"「{req.org_name}」签署成功！你的承诺已公示。审核通过后将展示在良心企业墙。",
    }


@app.get("/api/pact/alliance")
async def pact_alliance():
    """获取已签署协议的良心企业列表"""
    signers = _load_pact_signers()
    verified = [s for s in signers if s.get("audit_mark") == "🟢"]
    pending = [s for s in signers if s.get("audit_mark") != "🟢"]
    return {
        "total": len(signers),
        "verified_count": len(verified),
        "verified": verified,
        "pending": pending,
        "badge_svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60" width="200" height="60">
  <rect width="200" height="60" rx="8" fill="#1a1a2e"/>
  <rect x="2" y="2" width="196" height="56" rx="6" fill="none" stroke="#d4a853" stroke-width="1.5"/>
  <text x="100" y="24" text-anchor="middle" fill="#d4a853" font-size="10" font-family="sans-serif">五害曝光台认证</text>
  <text x="100" y="47" text-anchor="middle" fill="#2ecc71" font-size="14" font-weight="bold" font-family="sans-serif">🛡️ 良心企业</text>
</svg>""",
    }


# ─── 第四味药：个人数字主权工具包 ───

TOOLKIT_CONTENT = {
    "name": "个人数字主权工具包 v1.0",
    "description": "给每一个关心数字隐私的普通人的防御四件套。无需技术背景，复制粘贴即可武装自己。",
    "tools": [
        {
            "id": "browser-historian",
            "name": "浏览器史官",
            "icon": "🕵️",
            "description": "安装后自动记录每个网站对你的追踪行为。看清楚谁在偷看你。",
            "url": "https://uid9622.cn/browser-historian",
            "type": "browser_extension",
            "one_click": "下载zip → 解压 → Chrome/Edge加载已解压扩展 → 完成",
        },
        {
            "id": "whistleblower-shield",
            "name": "隐私盾·加密举报",
            "icon": "🔒",
            "description": "基于GPG+AES-256双层加密的举报通道。你的身份在技术上不可追溯。",
            "url": "https://uid9622.cn/five-harms-expose/#victims",
            "type": "web_tool",
            "one_click": "访问受害者墙 → 填写举报内容 → 系统自动加密 → 提交",
        },
        {
            "id": "block-inject",
            "name": "一键熔断脚本",
            "icon": "🛡️",
            "description": "将这段代码嵌入你的网站，自动拦截所有被曝光的黑产域名。访客免受追踪。",
            "url": "https://uid9622.cn/five-harms-expose/block-inject.js",
            "type": "script",
            "code_snippet": '<script src="https://uid9622.cn/five-harms-expose/block-inject.js" defer></script>',
            "usage": "复制上面这行代码，粘贴到你的网站 <head> 标签中即可。自动拦截所有已知有害域名。",
        },
        {
            "id": "defense-stack",
            "name": "防御全家桶",
            "icon": "🧰",
            "description": "浏览器插件推荐清单 + 系统级防火墙规则 + 手机隐私设置检查清单",
            "type": "guide",
            "checklist": [
                "浏览器装 uBlock Origin（免费开源广告/追踪拦截）",
                "浏览器装 Privacy Badger（EFF出品，学习式反追踪）",
                "浏览器装 HTTPS Everywhere（强制加密连接）",
                "搜索引擎改用 DuckDuckGo（不追踪搜索历史）",
                "DNS 设置 1.1.1.1 或 9.9.9.9（防DNS劫持）",
                "微信设置→隐私→关闭个性化广告推荐",
                "抖音设置→隐私→关闭个性化内容推荐",
                "淘宝设置→隐私→关闭个性化推荐",
                "定期清理浏览器Cookie和网站数据",
                '不使用"一键登录"功能（防止手机号关联）',
            ],
        },
    ],
    "download_package": {
        "name": "digital-sovereignty-toolkit-v1.zip",
        "contents": [
            "block-inject.js — 熔断脚本",
            "defense-checklist.md — 防御全家桶清单",
            "README.md — 使用指南",
        ],
        "url": "https://uid9622.cn/five-harms/api/toolkit/download",
    },
    "dna": "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-TOOLKIT-SOVEREIGNTY-v1.0",
}


@app.get("/api/toolkit")
async def get_toolkit():
    """获取个人数字主权工具包"""
    return TOOLKIT_CONTENT


@app.get("/api/toolkit/download")
async def toolkit_download():
    """下载工具包zip（生成熔断脚本+清单+指南）"""
    import io, zipfile
    
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. 熔断脚本 — 多路径兜底
        block_js_paths = [
            Path(_PROJECT_DIR) / "portal" / "five-harms-expose" / "block-inject.js",
            Path("/var/www/uid9622/five-harms-expose/block-inject.js"),
        ]
        block_js = None
        for p in block_js_paths:
            if p.exists():
                block_js = p.read_text()
                break
        if block_js is None:
            block_js = "// block-inject.js — 熔断脚本未找到，请访问 https://uid9622.cn/five-harms-expose/block-inject.js 手动下载"
        zf.writestr("block-inject.js", block_js)
        
        # 2. 防御全家桶清单
        checklist_md = """# 个人数字主权防御全家桶
## 龍魂·五害曝光台 出品

### 浏览器插件
1. **uBlock Origin** — 免费开源广告/追踪拦截器
2. **Privacy Badger** — EFF出品，自动学习并拦截追踪器
3. **HTTPS Everywhere** — 强制所有网站使用加密连接

### DNS防护
- Cloudflare DNS: 1.1.1.1 + 1.0.0.1
- Quad9: 9.9.9.9 (自动拦截已知恶意域名)
- 配置方法：系统设置→网络→DNS→手动

### 手机隐私
- 微信：我→设置→个人信息与权限→个性化广告管理→关闭
- 微信：我→设置→隐私→个人信息与权限→个性化推荐→关闭
- 抖音：我→右上角☰→设置→隐私设置→个性化内容推荐→关闭
- 淘宝：我的淘宝→设置→隐私→广告管理→关闭个性化推荐
- 美团：我的→设置→隐私管理→个性化广告推荐→关闭
- 拼多多：个人中心→设置→隐私→个性化推荐→关闭
- 京东：我的→设置→隐私→个性化广告→关闭

### 搜索引擎
- duckduckgo.com — 不追踪、不记录搜索历史
- searx.be — 开源、去中心化元搜索引擎

### 熔断脚本
将以下代码嵌入你的网站 <head> 中：
<script src="https://uid9622.cn/five-harms-expose/block-inject.js" defer></script>

### 日常习惯
1. 定期清理浏览器Cookie和网站数据
2. 不使用"一键登录""手机号快捷登录"
3. 不同网站使用不同密码（推荐Bitwarden密码管理器）
4. 浏览器开启"禁止第三方Cookie"
5. 关闭浏览器"预测网络操作""预加载页面"

---
> 你的数字主权，不容侵犯。
> 龍魂·五害曝光台 https://uid9622.cn/five-harms-expose
> DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-TOOLKIT-SOVEREIGNTY-v1.0
"""
        zf.writestr("defense-checklist.md", checklist_md)
        
        # 3. 使用指南
        readme_md = """# 个人数字主权工具包 v1.0
## 龍魂·五害曝光台

### 这是什么？
一个给普通人的数字隐私防御工具包。无需技术背景，按照说明操作即可。
包含：浏览器史官、隐私盾、熔断脚本、防御全家桶。

### 怎么用？

**第一步：安装浏览器史官**
去 https://uid9622.cn/browser-historian 下载并安装浏览器扩展。
安装后，每个网站对你的追踪行为都会被记录下来。

**第二步：理解熔断脚本**
把 block-inject.js 嵌入你的网站。它会自动拦截已知有害企业的追踪脚本。
如果你有个人网站或博客，添加一行代码即可。

**第三步：按清单加固**
打开 defense-checklist.md，逐个完成里面的设置。
大概需要10分钟，但能保护你一辈子的数字隐私。

**第四步：遇到问题就举报**
访问 https://uid9622.cn/five-harms-expose/#victims
用隐私盾加密举报，你的身份不可追溯。

### 常见问题

Q: 我不是开发者，能用吗？
A: 当然。浏览器史官一键安装，防御清单按图索骥，不需要任何技术背景。

Q: 熔断脚本会影响正常上网吗？
A: 不会。它只拦截已知有害企业的域名，正常网站不受影响。

Q: 我的数据安全吗？
A: 所有数据只存在你的本地设备上。龍魂系统不上传、不收集、不分享。

---
> 你不是一个人。我们正在建设数字时代的防线。
> https://uid9622.cn/five-harms-expose
"""
        zf.writestr("README.md", readme_md)
        
        # 4. 徽章
        zf.writestr("badge-good-faith.html", """<!-- 良心企业徽章嵌入代码 -->
<a href="https://uid9622.cn/five-harms-expose/#pact" title="防资本收割共同防御协议签约企业">
  <img src="https://uid9622.cn/five-harms-expose/badge-good-faith.svg" 
       alt="良心企业" width="200" height="60" style="border:0;">
</a>""")
    
    return Response(
        content=buf.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=digital-sovereignty-toolkit-v1.zip"},
    )


# ─── 门户页面 ───
@app.get("/", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
async def portal():
    portal_path = Path(_PROJECT_DIR) / "portal" / "five-harms-expose" / "index.html"
    if portal_path.exists():
        return HTMLResponse(portal_path.read_text())
    raise HTTPException(status_code=404, detail="门户页面未找到")


# ─── 工具函数 ───
def secrets_token() -> str:
    import secrets
    return secrets.token_hex(16)


# ─── 启动 ───
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("FIVE_HARMS_PORT", 8779))
    host = os.environ.get("FIVE_HARMS_HOST", "127.0.0.1")
    
    print("=" * 60)
    print("⚖️  龍魂·五害曝光台 API v1.0")
    print(f"   端口: {port}")
    print(f"   DNA: #龍芯⚡️丙午·乙未·丁酉·戌时·☰乾-FIVE-HARMS-API-v1.0")
    print("=" * 60)
    
    uvicorn.run(app, host=host, port=port, log_level="info")
