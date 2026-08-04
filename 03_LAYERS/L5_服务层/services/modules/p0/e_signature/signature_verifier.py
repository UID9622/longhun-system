#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
龍魂P0 · 数字签名验证（PKCS7/CMS · PDF内嵌签名）

能力:
  - 真实: 调用系统 openssl `smime -verify` 验证 PKCS7/CMS 签名（RSA/ECDSA 等）
  - 国密: 调用 gmssl 命令验证 SM2 签名（若系统有 gmssl 命令）
  - 真实: 提取 PDF 内嵌签名容器（/pdf 关键字搜索 Contents）
返回: {"capability","tier","algo","hash_algo","signed_by","verified","signed_data_hash","notes"}
DNA #龍魂⚡️丙午·辛未·P0-SIG-v1
"""

import subprocess
import hashlib
import tempfile
import os
import re


def _have(cmd):
    try:
        subprocess.run([cmd, "version"], capture_output=True, timeout=10,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def verify_pkcs7(p7_der: bytes, data_bytes: bytes = None, cert_pem: bytes = None,
                 sm2: bool = False) -> dict[str, Any]:
    """验证 PKCS7/CMS 签名。"""
    res = {"capability": "real", "tier": "🔴红线", "verified": False,
           "algo": "SM2" if sm2 else "RSA/ECDSA", "hash_algo": "",
           "signed_by": "", "signed_data_hash": "", "notes": ""}
    bin_name = "gmssl" if (sm2 and _have("gmssl")) else "openssl"
    try:
        with tempfile.NamedTemporaryFile(suffix=".p7", delete=False) as f:
            f.write(p7_der); p7 = f.name
        cmd = [bin_name, "smime", "-verify", "-in", p7, "-noverify"]
        files = []
        if data_bytes is not None:
            tf = tempfile.NamedTemporaryFile(delete=False); tf.write(data_bytes); tf.close()
            cmd += ["-content", tf.name]; files.append(tf.name)
        if cert_pem is not None:
            cf = tempfile.NamedTemporaryFile(suffix=".pem", delete=False)
            cf.write(cert_pem); cf.close()
            cmd += ["-signer", cf.name]; files.append(cf.name)
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        res["verified"] = out.returncode == 0
        res["tier"] = "🟢真实(验签通过)" if res["verified"] else "🔴红线(验签失败)"
        res["notes"] = (out.stdout.strip() or out.stderr.strip())[:500]
        for p in [p7] + files:
            os.unlink(p)
    except Exception as e:
        res["notes"] = f"签名验证执行异常: {e}"
    return res


def extract_pdf_signatures(pdf_bytes: bytes) -> list[Any]:
    """从 PDF 抽取内嵌签名容器(返回原始 DER/PEM 字节列表)。"""
    sigs = []
    try:
        text = pdf_bytes.decode("latin-1", errors="ignore")
        for m in re.finditer(r"/Type\s*/Sig\b", text):
            # 粗略定位 Contents 十六进制串
            seg = text[m.end():m.end()+2000]
            cm = re.search(r"/Contents\s*<([0-9A-Fa-f]+)>", seg)
            if cm:
                raw = bytes.fromhex(cm.group(1))
                sigs.append(raw)
    except Exception:
        pass
    return sigs


def verify_pdf_signature(pdf_bytes: bytes, cert_pem: bytes = None) -> dict[str, Any]:
    """验证 PDF 首个内嵌签名（若能抽取）。"""
    sigs = extract_pdf_signatures(pdf_bytes)
    if not sigs:
        return {"capability": "real", "tier": "🟡推演(无签名)",
                "verified": False, "notes": "未在PDF中检出内嵌签名容器(/Sig/Contents)"}
    return verify_pkcs7(sigs[0], data_bytes=pdf_bytes, cert_pem=cert_pem)
