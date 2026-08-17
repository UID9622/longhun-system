#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 🐉 龍魂·三色审计 异常定义
# DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-PYTHON-SDK-EXCEPTIONS-V1.0-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)


class TricolorError(Exception):
    """三色审计基础异常"""
    def __init__(self, code: str, message: str, dna: str = ""):
        self.code = code
        self.message = message
        self.dna = dna
        super().__init__(f"[{code}] {message}")


class RedLineException(Exception):
    """🔴 红线触发异常——操作被拒绝"""
    def __init__(self, verdict):
        self.verdict = verdict
        super().__init__(
            f"🔴 红线触发: {verdict.status} "
            f"(R={verdict.r_score}) DNA={verdict.dna}"
        )


class ReviewRequiredException(Exception):
    """🟡 待审查异常——需要人工复核"""
    def __init__(self, verdict):
        self.verdict = verdict
        super().__init__(
            f"🟡 需要审查: {verdict.status} "
            f"(R={verdict.r_score}) DNA={verdict.dna}"
        )
