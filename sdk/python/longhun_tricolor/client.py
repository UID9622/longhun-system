#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 🐉 龍魂·三色审计客户端
# DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-PYTHON-SDK-CLIENT-V1.0-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

"""
三色审计客户端 — 同步/异步双形态。
"""

import json
from typing import Optional, Dict, Any

import httpx

from .models import Scores, Verdict, EvidenceChain
from .exceptions import TricolorError, RedLineException, ReviewRequiredException


class TricolorClient:
    """三色审计同步客户端"""

    def __init__(
        self,
        base_url: str = "https://uid9622.cn/api/tricolor",
        token: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self._headers = {
            "Content-Type": "application/json",
        }
        if token:
            self._headers["Authorization"] = f"Bearer {token}"

    def evaluate(
        self,
        action_id: str,
        actor: str,
        action_type: str,
        scores: Optional[Scores] = None,
        description: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        locale: str = "zh-CN",
    ) -> Verdict:
        """执行三色判定"""
        payload = {
            "action_id": action_id,
            "actor": actor,
            "action_type": action_type,
            "locale": locale,
        }
        if scores:
            payload["scores"] = scores.to_dict()
        if description:
            payload["description"] = description
        if context:
            payload["context"] = context

        resp = httpx.post(
            f"{self.base_url}/v1/tricolor/evaluate",
            json=payload,
            headers=self._headers,
            timeout=self.timeout,
        )
        return self._handle_response(resp)

    def batch_evaluate(self, items: list) -> list:
        """批量判定"""
        resp = httpx.post(
            f"{self.base_url}/v1/tricolor/evaluate/batch",
            json={"items": items},
            headers=self._headers,
            timeout=self.timeout,
        )
        data = self._check_response(resp)
        return [Verdict.from_dict(v) for v in data.get("results", [])]

    def get_evidence(self, dna: str) -> EvidenceChain:
        """获取证据链"""
        resp = httpx.get(
            f"{self.base_url}/v1/tricolor/evidence/{dna}",
            headers=self._headers,
            timeout=self.timeout,
        )
        return EvidenceChain.from_dict(self._check_response(resp))

    def get_rules(self) -> dict:
        """获取规则集"""
        resp = httpx.get(
            f"{self.base_url}/v1/tricolor/rules",
            headers=self._headers,
            timeout=self.timeout,
        )
        return self._check_response(resp)

    def get_version(self) -> dict:
        """获取版本信息"""
        resp = httpx.get(
            f"{self.base_url}/v1/tricolor/version",
            timeout=self.timeout,
        )
        return self._check_response(resp)

    def _handle_response(self, resp) -> Verdict:
        data = self._check_response(resp)
        verdict = Verdict.from_dict(data)
        if verdict.status_code == "RED":
            raise RedLineException(verdict)
        if verdict.status_code == "YELLOW":
            raise ReviewRequiredException(verdict)
        return verdict

    def _check_response(self, resp):
        if resp.status_code >= 400:
            try:
                err = resp.json()
                raise TricolorError(
                    err.get("code", "TC-UNKNOWN"),
                    err.get("message", "未知错误"),
                    err.get("dna", ""),
                )
            except json.JSONDecodeError:
                raise TricolorError("TC-UNKNOWN", f"HTTP {resp.status_code}", "")
        return resp.json()


class AsyncTricolorClient:
    """三色审计异步客户端"""


    async def evaluate(
        self,
        action_id: str,
        actor: str,
        action_type: str,
        scores: Optional[Scores] = None,
        description: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        locale: str = "zh-CN",
    ) -> Verdict:
        """异步执行三色判定"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            payload = {
                "action_id": action_id,
                "actor": actor,
                "action_type": action_type,
                "locale": locale,
            }
            if scores:
                payload["scores"] = scores.to_dict()
            if description:
                payload["description"] = description
            if context:
                payload["context"] = context

            resp = await client.post(
                f"{self.base_url}/v1/tricolor/evaluate",
                json=payload,
                headers=self._headers,
            )
            data = self._check_response(resp)
            verdict = Verdict.from_dict(data)
            if verdict.status_code == "RED":
                raise RedLineException(verdict)
            if verdict.status_code == "YELLOW":
                raise ReviewRequiredException(verdict)
            return verdict

