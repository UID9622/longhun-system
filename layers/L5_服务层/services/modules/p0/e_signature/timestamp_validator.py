# DNA: #龍芯⚡️丙午·乙未·乙丑·同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
龍魂P0 · 可信时间戳(TSA/RFC3161)验证

能力:
  - 真实: 用系统 openssl `ts -verify` 验证时间戳与文档哈希绑定关系（若提供 tsq/tsr + 原文）
  - 降级(诚实标注): 纯解析 TST 结构（无联网校验 TSA 证书链）时标 🟡；
                    联网查询 TSA 证书吊销默认不启用(数据主权)
返回: {"capability","tier","tier_ts","gen_time","policy","serial","accuracy","verified","notes"}
DNA #龍魂⚡️丙午·辛未·P0-TSA-v1
"""

import subprocess
import hashlib
import tempfile
import os
from typing import Optional, Any


def verify_timestamp(tsr_der: bytes, data_bytes: Optional, Any[bytes] = None, tsa_cert: Optional, Any[bytes] = None,
                     data_hash: Optional, Any[str] = None) -> dict[str, Any]:
    """验证 RFC3161 时间戳。

    tsr_der: 时间戳响应(DER/PEM)
    data_bytes: 被盖章的原始文档字节（用于比对哈希）
    tsa_cert: TSA 证书（用于 openssl 验签）
    data_hash: 直接提供 hex 哈希（与 data_bytes 二选一）
    """
    res = {"capability": "real", "tier": "🟡推演(本地结构)",
           "verified": False, "gen_time": "", "policy": "",
           "serial": "", "accuracy": "", "notes": ""}
    # 用 openssl 解析 TST 信息
    try:
        with tempfile.NamedTemporaryFile(suffix=".tsr", delete=False) as f:
            f.write(tsr_der); tsr = f.name
        out = subprocess.run(["openssl", "ts", "-reply", "-in", tsr, "-text"],
                             capture_output=True, text=True, timeout=30)
        txt = out.stdout + out.stderr
        # 提取关键字段
        import re
        m = re.search(r"Time Stamp:\s*(.+)", txt)
        if m: res["gen_time"] = m.group(1).strip()
        m = re.search(r"Policy OID:\s*(.+)", txt)
        if m: res["policy"] = m.group(1).strip()
        m = re.search(r"Serial number:\s*(.+)", txt)
        if m: res["serial"] = m.group(1).strip()
        m = re.search(r"Accuracy:\s*(.+)", txt)
        if m: res["accuracy"] = m.group(1).strip()
        os.unlink(tsr)
    except Exception as e:
        res["notes"] = f"openssl 解析时间戳失败(可能非标准TST): {e}"
        return res

    # 完整验签：需原文 + TSA证书
    if data_bytes and tsa_cert:
        try:
            with tempfile.NamedTemporaryFile(delete=False) as f:
                f.write(data_bytes); doc = f.name
            with tempfile.NamedTemporaryFile(suffix=".tsr", delete=False) as f:
                f.write(tsr_der); tsr = f.name
            with tempfile.NamedTemporaryFile(suffix=".pem", delete=False) as f:
                f.write(tsa_cert); tc = f.name
            out = subprocess.run(["openssl", "ts", "-verify", "-in", tsr,
                                  "-data", doc, "-CAfile", tc],
                                 capture_output=True, text=True, timeout=30)
            res["verified"] = out.returncode == 0
            res["tier"] = "🟢真实(TSA验签通过)" if res["verified"] else "🔴红线(TSA验签失败)"
            res["notes"] = out.stdout.strip() or out.stderr.strip()
            for p in (doc, tsr, tc):
                os.unlink(p)
        except Exception as e:
            res["notes"] = f"TSA验签执行异常: {e}（结构已解析，签名未验）"
    else:
        res["notes"] = ("仅做本地结构解析，未提供原文+TSA证书故未验签；"
                        "联网校验TSA证书链默认不启用(数据主权)")
    return res
