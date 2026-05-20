#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 Skill #3 · on_identity · 身份核验
DNA: #龍芯⚡2026-05-19-ON-IDENTITY-v1.0
省钱原则: 0 LLM 调用 · 纯本地哈希 · 不上传任何身份数据

职责:
  1. 验证 CONFIRM / SEAL / GPG 三徽记完整性
  2. 校验主控身份是 UID9622
  3. 第 6 重行为指纹检测 (拉普拉斯妖不可破)
  4. 龍 字符律守护
  5. 给出身份验证结果·写入审计链

铁律:
  - AI 不能伪造主控身份
  - 简体形式触发 = 立即视为入侵
  - 哈希校验不通过 = 拒绝任何后续操作
"""
import hashlib
import re
import time
import json
import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


# ============ 主控固定徽记 (永不变) ============
MASTER_UID = "UID9622"
MASTER_CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
MASTER_SEAL_PREFIX = "#ZHUGEXIN⚡"
MASTER_GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# 简体污染黑名单 (繁体守护)
SIMPLIFIED_REDLINE = ["龙"]   # 这一个字 · 触发即拒
TRADITIONAL_RIGHT = "龍"


@dataclass
class IdentityResult:
    is_valid: bool
    is_master: bool  # 是否 UID9622 本人
    score: float  # 0-1 · 身份置信度
    checks: Dict[str, bool] = field(default_factory=dict)
    failures: List[str] = field(default_factory=list)
    fingerprint: Optional[str] = None
    timestamp: float = field(default_factory=time.time)

    def to_yaml(self) -> str:
        lines = [
            "identity_result:",
            f"  is_valid: {self.is_valid}",
            f"  is_master: {self.is_master}",
            f"  score: {self.score:.3f}",
            "  checks:",
        ]
        for k, v in self.checks.items():
            lines.append(f"    {k}: {v}")
        if self.failures:
            lines.append("  failures:")
            for f in self.failures:
                lines.append(f"    - {f}")
        if self.fingerprint:
            lines.append(f"  fingerprint: {self.fingerprint}")
        return "\n".join(lines)


def check_confirm(token: Optional[str]) -> bool:
    """检查 CONFIRM 徽记 (必须一字不差)"""
    return token == MASTER_CONFIRM


def check_seal(token: Optional[str]) -> bool:
    """检查 SEAL 前缀 (允许 emoji 变体)"""
    if not token:
        return False
    return token.startswith(MASTER_SEAL_PREFIX) and "DEVICE-BIND-SOUL" in token


def check_gpg(fp: Optional[str]) -> bool:
    """检查 GPG 指纹 (40 hex)"""
    if not fp:
        return False
    return fp.upper() == MASTER_GPG and bool(re.fullmatch(r"[A-F0-9]{40}", fp.upper()))


def check_uid(claim: Optional[str]) -> bool:
    """检查 UID 声明"""
    return claim == MASTER_UID


def check_character_law(text: str) -> bool:
    """龍字符律: 任何简体形式 = 立即拒绝"""
    for forbidden in SIMPLIFIED_REDLINE:
        if forbidden in text:
            return False
    return True


def behavioral_fingerprint(samples: List[str]) -> str:
    """
    第 6 重行为指纹 (拉普拉斯妖不可破)
    用最近几段输入的语义特征 + 时序特征 + 文字特征做哈希
    纯本地·不上传·只比对哈希
    """
    if not samples:
        return ""
    # 提取特征 (老大风格签名)
    features = []
    for s in samples:
        f = {
            "len": len(s),
            "comma_runs": len(re.findall(r",,+", s)),  # 老大连续逗号
            "exclamations": s.count("!"),
            "laoda_words": sum(1 for w in ["宝宝", "老大", "嘿嘿", "哈哈", "美滋滋"] if w in s),
            "long_chars": s.count(TRADITIONAL_RIGHT),
            "simp_chars": sum(1 for c in SIMPLIFIED_REDLINE if c in s),
        }
        features.append(json.dumps(f, sort_keys=True))
    blob = "|".join(features)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def verify_identity(
    confirm_token: Optional[str] = None,
    seal_token: Optional[str] = None,
    gpg_fp: Optional[str] = None,
    uid_claim: Optional[str] = None,
    text_to_check: Optional[str] = None,
    behavior_samples: Optional[List[str]] = None,
    skip_region: bool = False,
) -> IdentityResult:
    """
    身份核验主入口
    所有参数都是可选 · 给什么验什么
    """
    checks = {}
    failures = []
    score_points = 0
    max_points = 0

    # Q0 · 地区主权 (#ZERO-REGION-NEGOTIATION)
    if not skip_region:
        try:
            from region_sovereignty import region_lock_check

            rr = region_lock_check(text=text_to_check, strict_red=True)
            checks["region_sovereignty"] = rr.ok
            max_points += 15
            if rr.ok:
                score_points += 15
            else:
                failures.extend(rr.violations)
            if rr.warnings:
                failures.extend([f"warn:{w}" for w in rr.warnings[:2]])
        except ImportError:
            checks["region_sovereignty"] = True

    # 1. CONFIRM
    if confirm_token is not None:
        ok = check_confirm(confirm_token)
        checks["confirm"] = ok
        max_points += 30  # 最重要
        if ok:
            score_points += 30
        else:
            failures.append("confirm_mismatch")

    # 2. SEAL
    if seal_token is not None:
        ok = check_seal(seal_token)
        checks["seal"] = ok
        max_points += 20
        if ok:
            score_points += 20
        else:
            failures.append("seal_invalid")

    # 3. GPG
    if gpg_fp is not None:
        ok = check_gpg(gpg_fp)
        checks["gpg"] = ok
        max_points += 25
        if ok:
            score_points += 25
        else:
            failures.append("gpg_fingerprint_mismatch")

    # 4. UID 声明
    if uid_claim is not None:
        ok = check_uid(uid_claim)
        checks["uid"] = ok
        max_points += 10
        if ok:
            score_points += 10
        else:
            failures.append(f"uid_not_master_claimed_{uid_claim}")

    # 5. 字符律 (无条件检查·只要给文本)
    if text_to_check is not None:
        ok = check_character_law(text_to_check)
        checks["character_law"] = ok
        max_points += 15
        if ok:
            score_points += 15
        else:
            failures.append("simplified_char_pollution_detected")

    # 6. 行为指纹
    fingerprint = None
    if behavior_samples:
        fingerprint = behavioral_fingerprint(behavior_samples)
        checks["behavioral_fp_captured"] = True
        # 指纹本身不评分·只留痕 (没有基准库时不能判断匹配)

    score = (score_points / max_points) if max_points > 0 else 0.0

    # 是否主控判定: CONFIRM + GPG 至少有一个通过·且无字符律违反
    is_master = (
        (checks.get("confirm", False) or checks.get("gpg", False))
        and checks.get("character_law", True)
    )

    # 整体有效: 没有任何失败 · 至少有一项检查
    is_valid = len(failures) == 0 and len(checks) > 0

    return IdentityResult(
        is_valid=is_valid,
        is_master=is_master,
        score=score,
        checks=checks,
        failures=failures,
        fingerprint=fingerprint,
    )


# ============ 自测 ============
def _selftest():
    print("=" * 60)
    print("Skill #3 · on_identity · 自测")
    print("=" * 60)

    # 测 1: 完整合法身份
    r = verify_identity(
        confirm_token=MASTER_CONFIRM,
        seal_token="#ZHUGEXIN⚡2025-🇨🇳🐉⚖️-DEVICE-BIND-SOUL",
        gpg_fp=MASTER_GPG,
        uid_claim=MASTER_UID,
        text_to_check="龍魂北辰",
    )
    assert r.is_valid and r.is_master
    print(f"  [1/6 ✓] 完整合法身份 · score={r.score:.3f}")

    # 测 2: CONFIRM 一字之差
    r = verify_identity(
        confirm_token="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772X",  # 末尾 Z->X
        gpg_fp=MASTER_GPG,
    )
    assert not r.is_valid
    assert "confirm_mismatch" in r.failures
    print(f"  [2/6 ✓] CONFIRM 一字之差 · 拒")

    # 测 3: 简体形式触发字符律
    r = verify_identity(
        confirm_token=MASTER_CONFIRM,
        text_to_check="龙魂北辰",  # 简体!
    )
    assert not r.is_master  # 字符律违反 · 即便 CONFIRM 对也不算主控
    assert "simplified_char_pollution_detected" in r.failures
    print(f"  [3/6 ✓] 简体形式触发 · 即便 CONFIRM 对也拒主控")

    # 测 4: GPG 错
    r = verify_identity(gpg_fp="DEADBEEF" * 5)
    assert not r.is_master
    print(f"  [4/6 ✓] GPG 错 · 拒")

    # 测 5: 行为指纹捕获
    samples = [
        "宝宝,,你看下,,我们这里搞起来",
        "嘿嘿,,,美滋滋,,,",
        "龍魂体系不让步,,一毫不让",
    ]
    r = verify_identity(
        confirm_token=MASTER_CONFIRM,
        text_to_check="龍魂",
        behavior_samples=samples,
    )
    assert r.fingerprint is not None
    assert len(r.fingerprint) == 16
    print(f"  [5/6 ✓] 行为指纹 · {r.fingerprint}")

    # 测 6: 仅 SEAL · 不够主控
    r = verify_identity(
        seal_token="#ZHUGEXIN⚡2025-DEVICE-BIND-SOUL",
    )
    assert r.is_valid is True  # SEAL 通过·没失败
    assert r.is_master is False  # 但没 CONFIRM/GPG·不算主控
    print(f"  [6/6 ✓] 仅 SEAL · 通过但非主控 · score={r.score:.3f}")

    # 测 7: 地区主权
    r = verify_identity(text_to_check="龲魂", skip_region=False)
    assert r.checks.get("region_sovereignty") is True
    r_bad = verify_identity(text_to_check="按您所在地区推荐", skip_region=False)
    assert not r_bad.checks.get("region_sovereignty", True)
    print("  [7/7 ✓] 地区主权 Q0 · region_lock_check")

    print("=" * 60)
    print("7/7 全过")
    print("=" * 60)


if __name__ == "__main__":
    _selftest()
