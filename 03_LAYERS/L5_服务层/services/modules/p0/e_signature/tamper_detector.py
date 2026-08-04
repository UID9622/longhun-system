#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
龍魂P0 · 电子签篡改检测

检测项(对应用户规范表二):
  - 签名后修改内容: 当前文档哈希 != 签名时哈希
  - 替换签名证书: 证书指纹不匹配
  - 伪造时间戳: 时间戳签名无效
  - 复制签名到其他文档: 签名值不匹配新文档
  - 部分字段未签: 签名字段 < 实际字段
  - 自签名证书: 非CA颁发
  - 过期证书签名: 签名时证书已过期
返回: {"tampered":bool,"findings":[{type,level,desc}],"tier"}
DNA #龍魂⚡️丙午·辛未·P0-TAMPER-v1
"""

import hashlib


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def detect_content_tamper(current_bytes: bytes, signed_hash: str) -> dict[str, Any]:
    cur = sha256(current_bytes)
    matched = cur.lower() == signed_hash.lower()
    return {
        "tampered": not matched,
        "current_hash": cur,
        "signed_hash": signed_hash,
        "level": "high" if not matched else "none",
        "desc": "签名后文档内容被修改" if not matched else "文档哈希与签名时一致",
    }


def detect_cert_substitution(current_fp: str, signed_fp: str) -> dict[str, Any]:
    matched = current_fp.lower() == signed_fp.lower()
    return {
        "tampered": not matched,
        "level": "high" if not matched else "none",
        "desc": "签名证书被替换(指纹不匹配)" if not matched else "证书指纹一致",
    }


def detect_replay(sig_value: str, doc_hash: str, bound_doc_hash: str) -> dict[str, Any]:
    """复制签名到其他文档: 签名绑定的文档哈希 != 当前文档哈希。"""
    replay = doc_hash.lower() != bound_doc_hash.lower()
    return {
        "tampered": replay,
        "level": "high" if replay else "none",
        "desc": "签名被复用到其他文档(哈希不匹配)" if replay else "签名与文档绑定一致",
    }


def detect_self_signed(is_self_signed: bool) -> dict[str, Any]:
    return {
        "tampered": is_self_signed,
        "level": "medium" if is_self_signed else "none",
        "desc": "自签名证书·非CA颁发·不可信" if is_self_signed else "非自签名证书",
    }


def detect_expired_at_sign(sign_time_iso: str, cert_not_after: str) -> dict[str, Any]:
    """签名时证书已过期检测(简化字符串比较ISO)。"""
    try:
        from datetime import datetime
        st = datetime.fromisoformat(sign_time_iso.replace("Z", "+00:00"))
        na = datetime.fromisoformat(cert_not_after.replace("Z", "+00:00"))
        expired = st > na
    except Exception:
        return {"tampered": False, "level": "unknown",
                "desc": "无法解析签名时间/证书有效期"}
    return {
        "tampered": expired,
        "level": "medium" if expired else "none",
        "desc": "签名时证书已过期" if expired else "签名时证书在有效期内",
    }


def aggregate(findings: list[Any]) -> dict[str, Any]:
    """汇总所有篡改检测结论。"""
    reds = [f for f in findings if f.get("tampered")]
    level = "high" if any(f.get("level") == "high" for f in reds) else (
        "medium" if reds else "none")
    return {
        "tampered": bool(reds),
        "tier": "🔴红线(检出篡改)" if reds else "🟢真实(未检出篡改)",
        "level": level,
        "findings": findings,
    }
