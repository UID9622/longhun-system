"""WeChat Official Account API client with token caching."""

import json
import time
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from config import get_settings


class WeChatClient:
    """Client for WeChat Official Account APIs."""

    BASE_URL = "https://api.weixin.qq.com/cgi-bin"

    def __init__(self):
        self.settings = get_settings()
        self.appid = self.settings.WECHAT_APPID
        self.appsecret = self.settings.WECHAT_APPSECRET
        self.cache_dir = self.settings.CACHE_DIR
        self.token_file = self.cache_dir / "access_token.json"

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a request to WeChat API."""
        url = f"{self.BASE_URL}{endpoint}"
        if params is None:
            params = {}

        if method.upper() == "GET":
            response = requests.get(url, params=params, timeout=30)
        elif method.upper() == "POST":
            if files:
                response = requests.post(url, params=params, files=files, timeout=60)
            elif data is not None:
                response = requests.post(
                    url,
                    params=params,
                    data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    timeout=30,
                )
            else:
                response = requests.post(url, params=params, timeout=30)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        result = response.json()

        if "errcode" in result and result["errcode"] != 0:
            raise WeChatAPIError(
                errcode=result.get("errcode"),
                errmsg=result.get("errmsg", "Unknown error"),
                response=result,
            )

        return result

    def get_access_token(self, force_refresh: bool = False) -> str:
        """Get cached or fresh access token."""
        if not force_refresh and self.token_file.exists():
            try:
                cached = json.loads(self.token_file.read_text(encoding="utf-8"))
                expires_at = cached.get("expires_at", 0)
                if time.time() < expires_at - 300:  # Refresh 5 min before expiry
                    return cached["access_token"]
            except (json.JSONDecodeError, KeyError):
                pass

        if not self.appid or not self.appsecret:
            raise ValueError("WECHAT_APPID and WECHAT_APPSECRET must be set")

        result = self._request(
            "GET",
            "/token",
            params={
                "grant_type": "client_credential",
                "appid": self.appid,
                "secret": self.appsecret,
            },
        )

        token = result["access_token"]
        expires_in = result.get("expires_in", 7200)

        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.token_file.write_text(
            json.dumps(
                {
                    "access_token": token,
                    "expires_at": time.time() + expires_in,
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return token

    def clear_token_cache(self):
        """Clear cached access token."""
        if self.token_file.exists():
            self.token_file.unlink()

    def get_api_quota(self) -> Dict[str, Any]:
        """Get current API quota information."""
        token = self.get_access_token()
        return self._request(
            "POST",
            "/quota/get",
            params={"access_token": token},
            data={"cgi_path": "/draft/add"},
        )


class WeChatAPIError(Exception):
    """Raised when WeChat API returns an error."""

    def __init__(self, errcode: int, errmsg: str, response: Dict[str, Any]):
        self.errcode = errcode
        self.errmsg = errmsg
        self.response = response
        super().__init__(f"WeChat API Error {errcode}: {errmsg}")
