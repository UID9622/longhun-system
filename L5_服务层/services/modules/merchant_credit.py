# -*- coding: utf-8 -*-
"""
龍魂民生 · 商家信用查询

查询商家底细(统一社会信用代码/经营状态/诉讼/失信)。
当前诚实降级: 国家企业信用信息公示系统需联网+认证，默认不联网；
返回占位结构 + 🟡 提示"建议人工核验/联网查询"。
DNA #龍魂⚡️丙午·辛未·MERCHANT-v1
"""

import re


def _credit_code(text: str) -> str:
    m = re.search(r"统一社会信用代码[：:：]?\s*([0-9A-HJ-NPQRTUWXY]{18})", text)
    return m.group(1) if m else ""


def query(name: str = "", contract_text: str = "") -> dict[str, Any]:
    """查询商家信用。降级: 不联网，仅抽取合同内信用代码。"""
    code = _credit_code(contract_text) if contract_text else ""
    return {
        "capability": "degraded",
        "tier": "🟡推演(未联网)",
        "merchant": name or "（未提供）",
        "credit_code": code or "（合同未载/需联网核查）",
        "status": "未知(需国家企业信用信息公示系统核验)",
        "litigations": "未知",
        "dishonest": "未知",
        "complaints": "未知",
        "risk_rating": "未知",
        "notes": "联网工商核查默认不启用(数据主权)；建议人工登录公示系统核验经营状态与失信记录",
    }


if __name__ == "__main__":
    print(query("某装修公司", "统一社会信用代码：91110108MA01ABC23D"))
