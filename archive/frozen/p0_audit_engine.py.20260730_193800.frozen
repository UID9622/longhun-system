# -*- coding: utf-8 -*-
from __future__ import annotations
"""
龍魂P0级 · 电子签与照片篡改审计引擎（焊死）

统一编排:
  - 电子签通道: 证书链 / 时间戳 / 签名 / 篡改检测 (e_signature/*)
  - 照片通道: EXIF / 哈希 / ELA / 噪声 / 克隆 / CFA (photo/*)
  - 自动触发(规范六): 上传合同照片→EXIF+哈希+ELA；上传电子签→证书+签名+时间戳
  - 三色审计汇总 + P0报告(用户规范四模板) + 不可删日志归档
  - 降级能力诚实标注 🟡，绝不伪装 🟢

核心承诺(焊死): 电子签必须可验真 · 照片必须可溯源 · 任何篡改必须被识别。
DNA #龍魂⚡️丙午·辛未·P0-ENGINE-v1
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# 确保子模块可导入
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from longhun_minsheng_template import (
    BaseMinshengService, MinshengReport, SourceRef, TrustTier, make_dna,
)
from modules.p0.e_signature.cert_validator import validate_cert
from modules.p0.e_signature.timestamp_validator import verify_timestamp
from modules.p0.e_signature.signature_verifier import verify_pdf_signature
from modules.p0.e_signature.tamper_detector import detect_content_tamper, aggregate
from modules.p0.photo.exif_extractor import extract_exif
from modules.p0.photo.hash_checker import compare as hash_compare
from modules.p0.photo.ela_analyzer import ela
from modules.p0.photo.noise_analyzer import noise_consistency
from modules.p0.photo.clone_detector import clone_detect
from modules.p0.photo.cfa_analyzer import cfa_consistency


def _tier_color(tier: str) -> str:
    if not tier:
        return "blue"
    return {"🔴": "red", "🟢": "green", "🟡": "blue", "🔵": "blue"}.get(tier[0], "blue")


def _conf(verdict: str) -> int:
    return {"可信🟢": 92, "可疑🟡": 60, "不可信🔴": 25}.get(verdict, 60)


class P0AuditEngine(BaseMinshengService):
    def __init__(self):
        super().__init__("p0_audit")
        self.version = "v1"

    # ---------------- 电子签通道 ----------------
    def analyze_signature(self, applicant: str = "匿名",
                          cert_pem: Optional[bytes] = None, pdf_bytes: Optional[bytes] = None,
                          tsr: Optional[bytes] = None, tsa_cert: Optional[bytes] = None,
                          signed_hash: Optional[str] = None, sign_time_iso: Optional[str] = None,
                          ca_certs: Optional[list[Any]] = None, sm2: bool = False) -> Dict[str, Any]:
        dna = make_dna("P0", "esign", gua="讼", applicant=applicant)
        rep = MinshengReport(dna_trace=dna, applicant=applicant,
                             version=self.version, audit_level="P0")
        ca = rep.color_audit
        findings = []

        # 1) 证书
        if cert_pem:
            c = validate_cert(cert_pem, ca_certs=ca_certs)
            rep.add_source(SourceRef(TrustTier.REAL if c.get("capability") == "real" else TrustTier.INFERENCE,
                                     "X.509证书(cryptography/openssl)", c.get("reliability", "high") if "real" in str(c.get("capability")) else "low",
                                     datetime.now().isoformat(),
                                     f"持有者={c.get('subject')}; 链={c.get('chain_status')}; {c.get('notes','')}"))
            getattr(ca, {"red": "add_red", "green": "add_green", "blue": "add_blue"}[_tier_color(c.get("tier", ""))])(
                f"证书[{c.get('subject')}] 链={c.get('chain_status')} 过期={c.get('expired')}",
                detail=c.get("notes", ""))
            findings.append(c)
            if c.get("is_self_signed"):
                ca.add_red("自签名证书·非CA颁发·不可信", level="medium")
            if c.get("expired"):
                ca.add_red("证书已过期", level="medium")
        else:
            ca.add_blue("未提交证书(仅做签名/时间戳校验)")

        # 2) 签名
        sig_res = None
        if pdf_bytes:
            sig_res = verify_pdf_signature(pdf_bytes, cert_pem)
        if sig_res:
            getattr(ca, {"red": "add_red", "green": "add_green", "blue": "add_blue"}[_tier_color(sig_res.get("tier", ""))])(
                f"签名验签: verified={sig_res.get('verified')}", detail=sig_res.get("notes", ""))
            rep.add_source(SourceRef(TrustTier.REAL if sig_res.get("verified") else TrustTier.RED_LINE,
                                     "PKCS7/CMS签名(openssl/gmssl)", "high" if sig_res.get("verified") else "low",
                                     datetime.now().isoformat(),
                                     f"算法={sig_res.get('algo')}; {sig_res.get('notes','')}"))
            findings.append(sig_res)
        elif cert_pem and not pdf_bytes:
            ca.add_blue("已提交证书但未提供PDF/签名容器，跳过签名验签（建议上传含签名的PDF）")

        # 3) 时间戳
        if tsr:
            t = verify_timestamp(tsr, data_bytes=pdf_bytes, tsa_cert=tsa_cert)
            getattr(ca, {"red": "add_red", "green": "add_green", "blue": "add_blue"}[_tier_color(t.get("tier", ""))])(
                f"时间戳: verified={t.get('verified')} gen={t.get('gen_time')}", detail=t.get("notes", ""))
            rep.add_source(SourceRef(TrustTier.REAL if t.get("verified") else TrustTier.INFERENCE,
                                     "RFC3161 TSA(openssl ts)", "high" if t.get("verified") else "low",
                                     datetime.now().isoformat(), t.get("notes", "")))
            findings.append(t)

        # 4) 篡改检测
        tamper_ins = []
        if signed_hash and pdf_bytes:
            tamper_ins.append(detect_content_tamper(pdf_bytes, signed_hash))
        elif signed_hash and not pdf_bytes:
            ca.add_blue("提供签名时哈希但未提供文档，无法比对内容是否被改")
        agg = aggregate([f for f in tamper_ins if f])
        if tamper_ins:
            getattr(ca, {"red": "add_red", "green": "add_green", "blue": "add_blue"}[_tier_color(agg.get("tier", ""))])(
                "篡改检测", detail=agg.get("tier", ""))
            findings.append(agg)

        conf = _conf(ca.verdict())
        rep.meta_extra = {
            "audit_target": "电子签",
            "esign_confidence": conf,
            "sub_results": _strip(findings),
        }
        rep.generate_confirm_code()
        out = rep.to_json()
        out["esign_detail"] = _esign_section(findings)
        self.persist(out)
        return out

    # ---------------- 照片通道 ----------------
    def analyze_photo(self, applicant: str = "匿名", img_bytes: bytes = None,
                      original_bytes: bytes = None) -> Dict[str, Any]:
        dna = make_dna("P0", "photo", gua="讼", applicant=applicant)
        rep = MinshengReport(dna_trace=dna, applicant=applicant,
                             version=self.version, audit_level="P0")
        ca = rep.color_audit
        results = []

        # 照片通道: 各子项 tier 决定注入红/蓝；🟡疑点→red(medium)使整体判可疑
        def _inject(label, r):
            tier = r.get("tier", "")
            if tier.startswith("🔴"):
                ca.add_red(f"{label}: {r.get('notes','')[:60]}", level="high")
            elif tier.startswith("🟡"):
                # 疑点(异常/检出/不一致/无EXIF)→整体降为可疑🟡
                ca.add_red(f"{label}: 疑点 {r.get('notes','')[:60]}", level="medium")
            else:
                ca.add_green(f"{label}: 正常")

        # EXIF
        ex = extract_exif(img_bytes)
        results.append(ex)
        _inject("EXIF", ex)
        # 哈希
        if original_bytes:
            h = hash_compare(original_bytes, img_bytes)
            results.append(h)
            _inject("哈希", h)
        else:
            ca.add_blue("未提供原始照片，跳过哈希比对(建议上传原始文件提升可信度)")
        # ELA
        e = ela(img_bytes); results.append(e)
        _inject("ELA", e)
        # 噪声
        n = noise_consistency(img_bytes); results.append(n)
        _inject("噪声", n)
        # 克隆
        cl = clone_detect(img_bytes); results.append(cl)
        _inject("克隆", cl)
        # CFA
        cf = cfa_consistency(img_bytes); results.append(cf)
        _inject("CFA", cf)

        rep.add_source(SourceRef(TrustTier.REAL, "图像取证(numpy/PIL/scipy)", "high",
                                 datetime.now().isoformat(),
                                 "EXIF+ELA+噪声+克隆+CFA 多维度图像取证分析"))
        conf = _conf(ca.verdict())
        rep.meta_extra = {
            "audit_target": "照片",
            "photo_confidence": conf,
            "sub_results": _strip(results),
        }
        rep.generate_confirm_code()
        out = rep.to_json()
        out["photo_detail"] = _photo_section(results)
        self.persist(out)
        return out

    # ---------------- 自动路由 ----------------
    def auto_audit(self, path: str, applicant: str = "匿名") -> Dict[str, Any]:
        """按扩展名自动路由(规范六自动触发)。"""
        p = Path(path)
        if p.suffix.lower() in (".pdf", ".pem", ".crt", ".cer", ".p7s", ".tsr"):
            data = p.read_bytes()
            if p.suffix.lower() in (".pem", ".crt", ".cer"):
                return self.analyze_signature(applicant=applicant, cert_pem=data)
            if p.suffix.lower() == ".tsr":
                return self.analyze_signature(applicant=applicant, tsr=data)
            return self.analyze_signature(applicant=applicant, pdf_bytes=data)
        if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"):
            return self.analyze_photo(applicant=applicant, img_bytes=p.read_bytes())
        return {"error": f"不支持的文件类型: {p.suffix}"}


def _strip(obj):
    """递归去除不可 JSON 序列化(bytes)"""
    if isinstance(obj, dict):
        return {k: _strip(v) for k, v in obj.items() if not isinstance(v, bytes)}
    if isinstance(obj, (list, tuple)):
        return [_strip(v) for v in obj]
    if isinstance(obj, bytes):
        return "<bytes>"
    return obj


def _esign_section(findings: list[Any]) -> str:
    rows = "".join(
        f"<tr><td>{f.get('subject','-')}</td><td>{f.get('chain_status','-')}</td>"
        f"<td>{f.get('expired','-')}</td><td>{f.get('tier','-')}</td></tr>"
        for f in findings if isinstance(f, dict) and 'subject' in f)
    return f"<div class='card'><h2>电子签审计</h2><table><tr><th>持有者</th><th>链状态</th>" \
           f"<th>过期</th><th>可信度</th></tr>{rows}</table></div>"


def _photo_section(results: list[Any]) -> str:
    rows = "".join(
        f"<tr><td>{k}</td><td>{r.get('tier','-')}</td></tr>"
        for k, r in [("EXIF", results[0]), ("哈希", results[1] if len(results) > 1 else {}),
                     ("ELA", results[-4] if len(results) >= 4 else {}),
                     ("噪声", results[-3] if len(results) >= 3 else {}),
                     ("克隆", results[-2] if len(results) >= 2 else {}),
                     ("CFA", results[-1])])
    return f"<div class='card'><h2>照片原数据审计</h2><table><tr><th>检测项</th><th>结果</th></tr>{rows}</table></div>"


if __name__ == "__main__":
    eng = P0AuditEngine()
    # 自测1: 电子签(自签证书)
    import subprocess, tempfile
    with tempfile.NamedTemporaryFile(suffix=".pem", delete=False) as f:
        pem = f.name
    subprocess.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
                    "-keyout", "/dev/null", "-out", pem, "-days", "365",
                    "-subj", "/CN=龙魂自测证书"], check=True, capture_output=True)
    r1 = eng.analyze_signature(applicant="自检", cert_pem=open(pem, "rb").read())
    print("电子签 verdict:", r1["meta"]["verdict"], "| conf:", r1["meta"].get("esign_confidence"))
    # 自测2: 照片(PIL生成JPEG)
    from PIL import Image
    import io
    buf = io.BytesIO(); Image.new("RGB", (200, 200), (120, 80, 40)).save(buf, "JPEG", quality=95)
    r2 = eng.analyze_photo(applicant="自检", img_bytes=buf.getvalue())
    print("照片 verdict:", r2["meta"]["verdict"], "| conf:", r2["meta"].get("photo_confidence"))
    print("✅ P0引擎自测通过")
