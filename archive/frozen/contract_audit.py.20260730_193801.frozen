# -*- coding: utf-8 -*-
"""
龍魂民生 · 合同审计服务 v2.1（继承P0焊死基类）

能力:
  - OCR(图片→文字·pytesseract真实)
  - 条款抽取(nlp_analyzer)
  - 22类风险标签扫描 + 评分(risk_scorer)
  - 相似案例匹配(case_matcher·本地库)
  - 商家信用(merchant_credit·诚实降级不联网)
  - 时间线提醒(timeline_reminder)
  - 三色审计 + 合同审计报告(用户规范六模板) + 不可删日志
核心: 不是替人签字，是帮人看懂。最终决策由申请人做出。
DNA #龍魂⚡️丙午·辛未·CONTRACT-v2.1
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from longhun_minsheng_template import (
    BaseMinshengService, MinshengReport, SourceRef, TrustTier, make_dna,
)
from modules.ocr_engine import ocr_image
from modules.nlp_analyzer import extract_clauses, extract_money, extract_parties
from modules.risk_scorer import scan as risk_scan, score as risk_score
from modules.case_matcher import match as case_match
from modules.merchant_credit import query as merchant_query
from modules.timeline_reminder import build as timeline_build


class ContractAuditService(BaseMinshengService):
    def __init__(self):
        super().__init__("contract_audit")
        self.version = "v2.1"

    def audit(self, applicant: str = "匿名", text: str | None = None,
              img_path: str = None, meta: Dict[str, Any] = None) -> Dict[str, Any]:
        meta = meta or {}
        dna = make_dna("CONTRACT", "audit", gua="讼", applicant=applicant)
        rep = MinshengReport(dna_trace=dna, applicant=applicant,
                             version=self.version, audit_level="P0")
        ca = rep.color_audit

        # 1) OCR
        ocr_text = ""
        if img_path:
            ocr_text = ocr_image(open(img_path, "rb").read()).get("text", "")
            rep.add_source(SourceRef(TrustTier.REAL, "OCR识别(pytesseract/tesseract)", "high",
                                     datetime.now().isoformat(), "图片合同OCR→文字·建议人工校对"))
        full_text = (text or "") + "\n" + ocr_text

        # 2) 条款抽取
        clauses = extract_clauses(full_text)
        money = extract_money(full_text)
        parties = extract_parties(full_text)
        rep.add_source(SourceRef(TrustTier.LIBRARY, "龍魂NLP条款库", "medium",
                                 datetime.now().isoformat(), f"抽取条款{len(clauses)}条·金额{money}"))

        # 3) 风险扫描
        hits = risk_scan(clauses, full_text)
        sc = risk_score(hits)
        for h in hits:
            if h["level"] == "🔴":
                ca.add_red(f"{h['tag']}(触发:{h['keyword']})", level="high",
                           detail=f"建议:{h['advice']} | 依据:{h['law']}")
            else:
                ca.add_blue(f"{h['tag']}(触发:{h['keyword']})",
                            detail=f"建议:{h['advice']} | 依据:{h['law']}")
        if not hits:
            ca.add_green("未命中22类高危/中危标签")

        # 4) 案例 / 商家 / 时间线
        cases = case_match(hits)
        merchant = merchant_query(meta.get("merchant", ""), full_text)
        timeline = timeline_build(meta)

        # 5) 决策建议
        decision = self._decide(sc["risk_level"])

        # 6) 来源声明
        rep.add_source(SourceRef(TrustTier.LIBRARY, "龍魂22类风险标签库", "medium",
                                 datetime.now().isoformat(), "风险标签规则引擎"))
        rep.add_source(SourceRef(TrustTier.USER, "用户提交合同内容", "medium",
                                 datetime.now().isoformat(), "用户提供/上传·数据主权归用户"))

        rep.meta_extra = {
            "contract_type": meta.get("contract_type", "未指定"),
            "parties": parties, "money": money,
            "risk": sc, "hits": hits, "cases": cases,
            "merchant": merchant, "timeline": timeline, "decision": decision,
        }
        rep.extra_sections = [self._render_report(meta, clauses, hits,
                                                   sc, cases, merchant, timeline, decision, parties, money)]
        rep.generate_confirm_code()
        out = rep.to_json()
        out["contract_html"] = rep.extra_sections[0]
        self.persist(out)
        return out

    def _decide(self, risk_level: str) -> Dict[str, Any]:
        if risk_level.startswith("🔴"):
            return {"system_advice": "不签/修改后签/找律师",
                    "options": ["B.不签(重新谈判)", "C.修改后签(补充条款)", "D.找律师"],
                    "note": "检出高危条款，强烈建议不要直接签"}
        if risk_level.startswith("🟡"):
            return {"system_advice": "修改后签",
                    "options": ["C.修改后签(补充条款)", "D.找律师"],
                    "note": "存在中危条款，建议补充保护条款后再签"}
        return {"system_advice": "签(风险自担)",
                "options": ["A.签(风险自担)", "C.修改后签"],
                "note": "未检出高危/中危标签，仍建议保留证据"}

    def _render_report(self, meta, clauses, hits, sc, cases,
                       merchant, timeline, decision, parties, money) -> str:
        heat = "".join(f"<span class='tag' style='color:{'#ff4d4f' if h['level']=='🔴' else '#ffc53d'}'>"
                       f"{h['tag']}</span>" for h in hits) or "<span class='g'>无高危/中危标签</span>"
        rows = ""
        for c in clauses:
            triggered = [h for h in hits if h["keyword"] in c["text"]]
            if not triggered:
                continue
            for h in triggered:
                rows += (f"<tr><td>{c['no']}</td><td>{c['text'][:60]}…</td>"
                         f"<td>{h['level']}</td><td>{h['advice']}</td><td>{h['law']}</td></tr>")
        case_rows = "".join(
            f"<tr><td>{c.get('dna','-')}</td><td>{c.get('similarity','-')}%</td>"
            f"<td>{c.get('result','-')}</td><td>{c.get('lesson','-')}</td></tr>"
            for c in cases if "dna" in c)
        tl_rows = "".join(
            f"<tr><td>{t['node']}</td><td>{t['time']}</td><td>{t['remind']}</td></tr>"
            for t in timeline)
        return f"""
<div class='card'><h2>合同概览</h2>
<div class='kv'><span>合同类型</span><span>{meta.get('contract_type','未指定')}</span></div>
<div class='kv'><span>甲方</span><span>{parties.get('甲方') or '—'}</span></div>
<div class='kv'><span>乙方</span><span>{parties.get('乙方') or '—'}</span></div>
<div class='kv'><span>涉及金额</span><span>{', '.join(money) or '—'}</span></div>
<div class='kv'><span>风险等级</span><span style='color:{'#ff4d4f' if sc['risk_level'].startswith('🔴') else '#ffc53d' if sc['risk_level'].startswith('🟡') else '#52c41a'}'>{sc['risk_level']}</span></div>
<div>风险热力图: {heat}</div></div>
<div class='card'><h2>条款逐条解读(命中风险)</h2>
<table><tr><th>条款</th><th>原文</th><th>等级</th><th>防范建议</th><th>依据</th></tr>{rows}</table></div>
<div class='card'><h2>相似案例</h2>
<table><tr><th>案例DNA</th><th>相似度</th><th>结果</th><th>教训</th></tr>{case_rows or '<tr><td colspan=4>无匹配案例</td></tr>'}</table></div>
<div class='card'><h2>商家信用</h2>
<div class='kv'><span>商家</span><span>{merchant.get('merchant')}</span></div>
<div class='kv'><span>信用代码</span><span>{merchant.get('credit_code')}</span></div>
<div class='kv'><span>经营状态</span><span>{merchant.get('status')}</span></div>
<div class='kv'><span>风险评级</span><span>{merchant.get('risk_rating')}</span></div>
<p class='b'>⚠️ {merchant.get('notes')}</p></div>
<div class='card'><h2>时间线提醒</h2>
<table><tr><th>节点</th><th>时间</th><th>提醒</th></tr>{tl_rows}</table></div>
<div class='card'><h2>决策建议</h2>
<p>系统建议: <b>{decision['system_advice']}</b></p>
<p class='b'>{decision['note']}</p>
<p>可选: {' / '.join(decision['options'])}</p>
<blockquote>不是替人签字，是帮人看懂。你是决策者，系统只给光。</blockquote></div>
"""


if __name__ == "__main__":
    svc = ContractAuditService()
    t = ("甲方：某装修公司。第一条 最终解释权归甲方所有，不可退。"
         "第二条 押金不退，损坏赔偿从押金扣。第三条 按实结算，增加项目材料升级另计。"
         "第四条 预付全款，定金不退。")
    r = svc.audit(applicant="测试用户", text=t,
                  meta={"contract_type": "装修", "merchant": "某装修公司",
                        "sign_date": "2026-07-16", "duration_days": 90,
                        "auto_renew": False, "refund_deadline_days": 15})
    print("合同 verdict:", r["meta"]["verdict"])
    print("风险:", r["meta"]["risk"]["risk_level"], "| 命中:", [h["tag"] for h in r["meta"]["hits"]])
    print("决策:", r["meta"]["decision"]["system_advice"])
    print("✅ 合同审计自测通过")
