# -*- coding: utf-8 -*-
"""
龍魂民生 · 合同时间线提醒

基于合同期限/自动续费/退款截止/诉讼时效生成提醒节点。
DNA #龍魂⚡️丙午·辛未·TIMELINE-v1
"""

from datetime import datetime, timedelta


def build(contract_meta: dict[str, Any]) -> list[Any]:
    """contract_meta: {sign_date, duration_days, auto_renew, refund_deadline_days,
    limitation_years}"""
    today = datetime.now()
    nodes = []
    sign = contract_meta.get("sign_date")
    if sign:
        try:
            sd = datetime.fromisoformat(sign)
        except Exception:
            sd = today
    else:
        sd = today

    dur = contract_meta.get("duration_days")
    if dur:
        exp = sd + timedelta(days=dur)
        nodes.append({"node": "合同到期", "time": exp.date().isoformat(),
                      "remind": "提前30天提醒是否续签"})
    if contract_meta.get("auto_renew"):
        nodes.append({"node": "自动续费", "time": (sd + timedelta(days=contract_meta.get("duration_days", 365))).date().isoformat(),
                      "remind": "提前7天提醒是否取消"})
    rd = contract_meta.get("refund_deadline_days")
    if rd:
        nodes.append({"node": "退款截止", "time": (sd + timedelta(days=rd)).date().isoformat(),
                      "remind": "提前15天提醒申请退款"})
    ly = contract_meta.get("limitation_years", 3)
    lim = sd + timedelta(days=ly * 365)
    nodes.append({"node": "诉讼时效", "time": lim.date().isoformat(),
                  "remind": "提前180天提醒起诉"})
    nodes.append({"node": "证据保存", "time": (today + timedelta(days=365)).date().isoformat(),
                  "remind": "每年提醒备份一次证据"})
    return nodes


if __name__ == "__main__":
    for n in build({"sign_date": "2026-07-16", "duration_days": 365, "auto_renew": True, "refund_deadline_days": 30}):
        print(n["node"], n["time"], n["remind"])
