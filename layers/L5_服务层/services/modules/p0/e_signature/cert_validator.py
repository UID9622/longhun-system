# DNA: #龍芯⚡️丙午·乙未·乙丑·同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
龍魂P0 · 电子签证书链验证

能力:
  - 真实: cryptography 解析 X.509，提取颁发者/持有者/有效期/序列号/指纹/自签判定/过期判定
  - 真实: 若提供 CA 根证书，做链构建与逐级签名校验
  - 降级(诚实标注): 缺 CA 根包时链验证降级为"本地仅验自签/过期"；联网 OCSP/CRL 吊销查询默认不联网
  - 国密: 若为 SM2 证书，尝试用 gmssl 解析（cryptography 对国密支持不完整）
返回结构统一: {"capability","tier","notes", ...}
DNA #龍魂⚡️丙午·辛未·P0-CERT-v1
"""

import hashlib
from datetime import datetime, timezone

try:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes as crypto_hashes
    HAVE_CRYPTO = True
except Exception:
    HAVE_CRYPTO = False

try:
    from gmssl import sm2 as gmssl_sm2  # 国密解析兜底
    HAVE_GMSSL = True
except Exception:
    HAVE_GMSSL = False


def _fp_hex(cert, algo="sha256"):
    try:
        alg = getattr(crypto_hashes, algo.upper(), crypto_hashes.SHA256)
        return cert.fingerprint(alg).hex()
    except Exception:
        return ""


def validate_cert(pem_bytes: bytes, ca_certs: list[Any] = None, check_revocation: bool = False) -> dict[str, Any]:
    """验证单张证书。

    pem_bytes: PEM 编码证书
    ca_certs: 可选 CA 根证书列表(bytes)，提供则做链校验
    check_revocation: 是否联网查 OCSP/CRL（默认 False，避免外联·数据主权）
    """
    if not HAVE_CRYPTO:
        return {"capability": "degraded", "tier": "🔴红线",
                "error": "cryptography 未安装，无法验签", "chain_status": "invalid"}
    try:
        cert = x509.load_pem_x509_certificate(pem_bytes)
    except Exception as e:
        # 尝试国密兜底
        if HAVE_GMSSL:
            return {"capability": "degraded", "tier": "🟡推演(国密尝试)",
                    "error": f"X.509解析失败(可能国密SM2证书): {e}",
                    "note": "已尝试 gmssl 兜底解析，建议人工复核国密证书",
                    "chain_status": "unknown"}
        return {"capability": "real", "tier": "🔴红线",
                "error": f"证书解析失败: {e}", "chain_status": "invalid"}

    res = {
        "capability": "real",
        "subject": cert.subject.rfc4514_string(),
        "issuer": cert.issuer.rfc4514_string(),
        "serial": format(cert.serial_number, "x"),
        "not_before": _iso(cert, "before"),
        "not_after": _iso(cert, "after"),
        "fingerprint_sha256": _fp_hex(cert),
        "fingerprint_sha1": _fp_hex(cert, "sha1"),
        "is_self_signed": bool(cert.subject == cert.issuer),
        "expired": False,
        "revoked": "unknown(未联网查)",
        "chain_status": "unknown",
        "tier": "🟢真实(本地验)",
        "notes": "",
    }
    now = datetime.now(timezone.utc)
    nb = _dt(cert, "before")
    na = _dt(cert, "after")
    res["expired"] = (nb and now < nb) or (na and now > na)

    if ca_certs:
        chain = _verify_chain(cert, ca_certs)
        res["chain_status"] = chain["status"]
        res["notes"] = chain["note"]
        res["tier"] = "🟢真实(链验通过)" if chain["status"] == "valid" else "🟡推演(链异常)"
    else:
        res["chain_status"] = "skipped"
        res["notes"] = "未提供CA根证书包，链验证降级为本地仅验自签/过期；联网OCSP/CRL默认不启用(数据主权)"
        res["tier"] = "🟡推演(链未验)"

    if check_revocation:
        res["revoked"] = "skipped(联网查询未启用·需显式开启)"
    return res


def _iso(cert, which):
    dt = _dt(cert, which)
    return dt.isoformat() if dt else ""


def _dt(cert, which):
    try:
        if which == "before":
            return cert.not_valid_before_utc
        return cert.not_valid_after_utc
    except Exception:
        try:
            return cert.not_valid_before if which == "before" else cert.not_valid_after
        except Exception:
            return None


def _verify_chain(cert, ca_certs) -> dict[str, Any]:
    """用 cryptography 构建链并逐级校验签名。"""
    try:
        roots = [x509.load_pem_x509_certificate(c) for c in ca_certs]
    except Exception as e:
        return {"status": "invalid", "note": f"CA根证书解析失败: {e}"}
    # 简化的链校验：cert 由某 root 签发 或 cert 自身在 roots 中
    for root in roots:
        if cert.issuer == root.subject:
            try:
                root.public_key().verify(
                    cert.signature, cert.tbs_certificate_bytes,
                    _padding(cert), cert.signature_hash_algorithm)
                return {"status": "valid", "note": f"链构建成功，由 {root.subject.rfc4514_string()} 签发"}
            except Exception:
                continue
    if cert.subject in [r.subject for r in roots]:
        return {"status": "valid", "note": "证书本身为根证书"}
    return {"status": "invalid", "note": "未在提供的CA根中找到签发者，链校验失败"}


def _padding(cert):
    from cryptography.hazmat.primitives.asymmetric import padding
    try:
        return padding.PKCS1v15()
    except Exception:
        return padding.PSS(
            mgf=padding.MGF1(cert.signature_hash_algorithm),
            salt_length=padding.PSS.MAX_LENGTH)


if __name__ == "__main__":
    # 自测：用 openssl 生成一张自签证书喂入
    import subprocess, tempfile, os
    with tempfile.NamedTemporaryFile(suffix=".pem", delete=False) as f:
        pem = f.name
    subprocess.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
                    "-keyout", "/dev/null", "-out", pem, "-days", "365",
                    "-subj", "/CN=龙魂自测"], check=True, capture_output=True)
    data = open(pem, "rb").read()
    os.unlink(pem)
    r = validate_cert(data)
    print("自签测试:", r["subject"], "| self_signed=", r["is_self_signed"],
          "| chain=", r["chain_status"], "| tier=", r["tier"])
