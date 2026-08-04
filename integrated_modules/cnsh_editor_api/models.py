#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH Editor API · Pydantic 模型
DNA: #龍芯⚡️2026-07-04-CNSH-API-MODELS-v1.0
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class CompileRequest(BaseModel):
    source: str = Field(..., description="CNSH 源代码", min_length=1)
    legacy: bool = Field(False, description="是否使用旧版正则翻译器")


class CompileResponse(BaseModel):
    success: bool
    python_code: Optional[str] = None
    message: str
    dna: str = "#龍芯⚡️2026-07-04-CNSH-API-v1.0"


class CheckRequest(BaseModel):
    source: str = Field(..., description="CNSH 源代码", min_length=1)


class CheckResponse(BaseModel):
    success: bool
    message: str


class RunRequest(BaseModel):
    source: str = Field(..., description="CNSH 源代码", min_length=1)
    legacy: bool = Field(False, description="是否使用旧版正则翻译器")
    timeout_ms: Optional[int] = Field(None, description="执行超时，默认取 tier 限制")


class RunResponse(BaseModel):
    success: bool
    stdout: str = ""
    stderr: str = ""
    namespace: Optional[Dict[str, Any]] = None
    message: str = ""


class TokenizeRequest(BaseModel):
    source: str = Field(..., description="CNSH 源代码", min_length=1)


class TokenInfo(BaseModel):
    type: str
    value: str
    line: int
    column: int


class TokenizeResponse(BaseModel):
    success: bool
    tokens: List[TokenInfo] = []
    message: str = ""


class TierInfo(BaseModel):
    name: str
    description: str
    max_source_chars: int
    max_execution_time_ms: int
    allow_file_io: bool
    allow_network: bool
    allow_advanced_features: bool


class HealthResponse(BaseModel):
    status: str
    tier: str
    version: str = "1.0.0"
    dna: str = "#龍芯⚡️2026-07-04-CNSH-API-v1.0"
