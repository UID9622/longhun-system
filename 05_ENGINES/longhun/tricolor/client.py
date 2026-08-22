# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 🐉 龍魂·三色审计 HTTP客户端 v1.1
# DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-TRICOLOR-CLIENT-v1.1-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

"""三色审计远程API客户端（直连API形态）。

Example:
    client = TricolorClient(token="...", base_url="https://uid9622.cn/api/tricolor")
    verdict = client.evaluate(
        action_id="demo-001",
        actor="order-service",
        action_type="data_export",
        scores={"humanWelfare": 82, "fairness": 78, "controllability": 70,
                "transparency": 65, "traceability": 80, "privacy": 55},
    )
    if verdict.status_code == "RED":
        raise FuseBreaker(verdict.dna)
"""

import json
import urllib.request
import urllib.error
from typing import Optional, List, Dict, Any
from dataclasses import asdict

from .engine import (
    ENGINE_VERSION, CONTRACT_VERSION,
    EvaluateRequest, Scores, Verdict, AuditRecord,
)


class TricolorError(Exception):
    """三色审计API错误。"""
    def __init__(self, code: str, message: str, dna: str = ""):
        self.code = code
        self.message = message
        self.dna = dna
        super().__init__(f"[{code}] {message}")


class TricolorClient:
    """三色审计远程HTTP客户端。

    Args:
        token: Bearer认证Token
        base_url: 服务端地址
        timeout: 请求超时（秒）
    """

    def __init__(self, token: str = "", base_url: str = "http://localhost:9622/tricolor",
                 timeout: int = 10):
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, method: str, path: str, body: Optional[Dict] = None,
                 headers: Optional[Dict] = None) -> Dict[str, Any]:
        """发送HTTP请求。"""
        url = f"{self.base_url}{path}"
        hdrs = {"Content-Type": "application/json; charset=utf-8"}
        if self.token:
            hdrs["Authorization"] = f"Bearer {self.token}"
        if headers:
            hdrs.update(headers)

        data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body else None
        req = urllib.request.Request(url, data=data, headers=hdrs, method=method)

        try:
            resp = urllib.request.urlopen(req, timeout=self.timeout)
            return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            try:
                err = json.loads(err_body)
                raise TricolorError(err.get("code", "TC-5000"), err.get("message", str(e)))
            except json.JSONDecodeError:
                raise TricolorError("TC-5000", err_body or str(e))

    # ── API端点 ──

    def evaluate(self, action_id: str, actor: str, action_type: str,
                 scores: Optional[Dict[str, float]] = None,
                 description: str = "", context: Optional[Dict] = None,
                 locale: str = "zh-CN") -> Verdict:
        """提交三色判定。"""
        body: Dict[str, Any] = {
            "action_id": action_id,
            "actor": actor,
            "action_type": action_type,
            "locale": locale,
        }
        if description:
            body["description"] = description
        if scores:
            body["scores"] = scores
        if context:
            body["context"] = context

        result = self._request("POST", "/v1/tricolor/evaluate", body)
        return Verdict(**result)

    def evaluate_batch(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量判定（≤100条/次）。"""
        return self._request("POST", "/v1/tricolor/evaluate/batch", {"items": items})

    def get_rules(self) -> Dict[str, Any]:
        """获取当前规则集。"""
        return self._request("GET", "/v1/tricolor/rules")

    def get_evidence(self, dna: str, gpg_signature: str = "") -> Dict[str, Any]:
        """按DNA调取证链。"""
        headers = {}
        if gpg_signature:
            headers["X-GPG-Signature"] = gpg_signature
        from urllib.parse import quote
        return self._request("GET", f"/v1/tricolor/evidence/{quote(dna, safe='')}", headers=headers)

    def get_report(self, period: str = "daily", fmt: str = "json") -> Dict[str, Any]:
        """生成审计报告。"""
        return self._request("GET", f"/v1/tricolor/report?period={period}&format={fmt}")

    def register_webhook(self, url: str, events: List[str], secret: str) -> Dict[str, Any]:
        """注册Webhook回调。"""
        return self._request("POST", "/v1/tricolor/webhook", {
            "url": url, "events": events, "secret": secret,
        })

    def unregister_webhook(self) -> None:
        """注销Webhook回调。"""
        self._request("DELETE", "/v1/tricolor/webhook")

    def run_conformance(self, endpoint: str = "", suite: str = "full") -> Dict[str, Any]:
        """运行一致性自测。"""
        return self._request("POST", "/v1/tricolor/conformance", {
            "endpoint": endpoint, "suite": suite,
        })

    def get_version(self) -> Dict[str, Any]:
        """获取引擎与契约版本。"""
        return self._request("GET", "/v1/tricolor/version")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 本地模拟服务（用于离线开发/测试）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from .engine import TricolorEngine

class LocalTricolorServer:
    """本地嵌入式引擎（B形态：内网/数据敏感场景）。"""

    def __init__(self):
        self.engine = TricolorEngine()
        self._audit_log: List[AuditRecord] = []

    def evaluate(self, request: EvaluateRequest) -> Verdict:
        verdict = self.engine.evaluate(request)
        record = self.engine.to_audit_record(verdict)
        self._audit_log.append(record)
        return verdict

    def dump_audit_log(self) -> str:
        return "\n".join(r.to_jsonl() for r in self._audit_log)
