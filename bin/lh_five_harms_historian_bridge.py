# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·戌时·☰乾-HARMS-HISTORIAN-BRIDGE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·五害曝光台 — 浏览器史官联动引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·戌时·☰乾-HARMS-HISTORIAN-BRIDGE-v1.0

职能: 当用户访问被五害曝光台标记的企业网站时，浏览器史官自动弹出风险提示。
联动方式:
  1. 浏览器史官插件读取本引擎提供的风险域名清单
  2. 用户访问匹配域名时，弹出"龍魂·五害曝光台"风险提示卡片
  3. 提示卡片包含：企业名称、危害类型、曝光ID、证据链接
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

_PROJECT = Path(__file__).parent.parent
_DATA_DIR = _PROJECT / "data" / "five_harms"
_BLOCKLIST_FILE = _DATA_DIR / "blocklist.json"
_RISK_EXPORT_FILE = _PROJECT / "portal" / "browser-historian" / "five-harms-risk.json"


def generate_risk_database():
    """生成浏览器史官可读取的风险域名数据库"""
    cases_file = _DATA_DIR / "cases.json"
    
    if not cases_file.exists():
        # 使用默认数据
        cases = _get_default_cases()
    else:
        try:
            cases = json.loads(cases_file.read_text())
        except Exception:
            cases = _get_default_cases()
    
    # 只导出严重+高危案例
    risk_entries = []
    for case in cases:
        if case.get("severity") in ("critical", "high"):
            risk_entries.append({
                "company": case.get("company", ""),
                "title": case.get("title", ""),
                "category": case.get("category", ""),
                "severity": case.get("severity", ""),
                "case_id": case.get("id", ""),
                "evidence_count": len(case.get("evidence", [])),
                "victims": case.get("victims", 0),
                "domains": _infer_domains(case.get("company", "")),
            })
    
    export = {
        "version": "1.0",
        "generated": datetime.now(timezone.utc).isoformat(),
        "total_risks": len(risk_entries),
        "risks": risk_entries,
        "dna": "#龍芯⚡️丙午·乙未·丁酉·戌时·☰乾-HARMS-HISTORIAN-BRIDGE-v1.0",
    }
    
    _RISK_EXPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    _RISK_EXPORT_FILE.write_text(json.dumps(export, ensure_ascii=False, indent=2))
    
    print(f"✅ 风险数据库已生成: {_RISK_EXPORT_FILE}")
    print(f"   风险条目: {len(risk_entries)}")
    return export


def _infer_domains(company: str) -> List[str]:
    """从企业名称推断可能域名（占位·实际需对接DNS）"""
    # 这是一个占位实现，实际需要对接工商数据
    return []


def _get_default_cases() -> List[Dict]:
    return [
        {"id":1,"company":"某团外卖","title":"强迫商家二选一","category":"平台垄断","severity":"critical","victims":37200,"evidence":[{}]},
        {"id":2,"company":"某滴出行","title":"大数据杀熟","category":"算法收割","severity":"critical","victims":186000,"evidence":[{}]},
        {"id":4,"company":"某输入法App","title":"键盘输入实时上传云端","category":"隐私践踏","severity":"critical","victims":38000000,"evidence":[{}]},
        {"id":6,"company":"某短视频平台","title":"未成年沉迷推荐算法","category":"算法收割","severity":"critical","victims":95000000,"evidence":[{}]},
        {"id":8,"company":"某智能家居厂商","title":"智能音箱24小时录音","category":"隐私践踏","severity":"critical","victims":15000000,"evidence":[{}]},
        {"id":9,"company":"某医疗健康App","title":"用户健康数据被出售","category":"数据倒卖","severity":"critical","victims":8700000,"evidence":[{}]},
    ]


def get_risk_alert_html(case_id: int) -> str:
    """生成浏览器史官弹出卡片HTML"""
    cases_file = _DATA_DIR / "cases.json"
    cases = _get_default_cases()
    if cases_file.exists():
        try:
            cases = json.loads(cases_file.read_text())
        except Exception:
            pass
    
    target = None
    for c in cases:
        if c.get("id") == case_id:
            target = c
            break
    
    if not target:
        return ""
    
    severity_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "watch": "🔵"}
    
    return f"""
<div style="font-family:system-ui;background:#1a1a2e;color:#c8c8d4;border:1px solid #c9a84c;border-radius:12px;padding:20px;max-width:400px;">
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
    <span style="font-size:24px;">🛡️</span>
    <span style="color:#c9a84c;font-weight:700;font-size:16px;">龍魂·五害曝光台 风险提示</span>
  </div>
  <div style="background:rgba(229,83,75,0.1);border-radius:8px;padding:12px;margin-bottom:12px;">
    <div style="color:#e5534b;font-weight:700;font-size:14px;">{severity_emoji.get(target['severity'],'')} {target.get('category','')}</div>
    <div style="font-size:15px;margin-top:6px;color:#e8e8f0;">{target.get('title','')}</div>
  </div>
  <div style="font-size:13px;color:#6b6b7b;margin-bottom:12px;">
    👥 受影响约 {(target.get('victims',0)/10000):.0f} 万人
    📎 {len(target.get('evidence',[]))} 条证据链
  </div>
  <a href="https://uid9622.cn/five-harms-expose/#section-timeline" 
     style="display:block;text-align:center;padding:10px;background:#c9a84c;color:#000;border-radius:8px;text-decoration:none;font-weight:600;font-size:14px;">
    查看完整曝光 →
  </a>
</div>
"""


if __name__ == "__main__":
    export = generate_risk_database()
