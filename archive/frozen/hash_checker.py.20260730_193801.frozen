# -*- coding: utf-8 -*-
"""
龍魂P0 · 照片原数据完整性哈希校验

能力: 真实(hashlib SHA-256)。
  原始照片哈希 vs 上传照片哈希: 一致=未篡改/或仅重压缩; 不一致=已篡改或压缩。
返回: {"capability","tier","sha256_original","sha256_upload","match","notes"}
DNA #龍魂⚡️丙午·辛未·P0-HASH-v1
"""

import hashlib


def sha256_file(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def compare(original_bytes: bytes, upload_bytes: bytes, tolerate_recompress: bool = True) -> dict[str, Any]:
    o = sha256_file(original_bytes)
    u = sha256_file(upload_bytes)
    match = (o == u)
    res = {
        "capability": "real",
        "sha256_original": o,
        "sha256_upload": u,
        "match": match,
        "tier": "🟢真实(哈希一致)" if match else "🟡推演(哈希不一致)",
        "notes": "",
    }
    if match:
        res["notes"] = "原始照片与上传照片SHA-256一致，未篡改"
    else:
        res["notes"] = ("哈希不一致：文件内容不同。" +
                        ("可能为重新压缩/转换格式所致，需结合ELA/CFA进一步判定是否篡改"
                         if tolerate_recompress else "判定为已篡改"))
        if not tolerate_recompress:
            res["tier"] = "🔴红线(哈希不一致·判定篡改)"
    return res
