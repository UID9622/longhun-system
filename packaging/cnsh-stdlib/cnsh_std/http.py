#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·丁酉·乙酉·午时·䷾既济-CNSH-STD-HTTP-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
CNSH 标准库 · http —— 网络请求（urllib 原生 · 默认禁代理直连防 socks 劫持）
"""
import json as _json
import urllib.request as _ur
import urllib.error as _ue

_UA = "cnsh-stdlib/1.0 (CNSH; UID9622; longhun)"


def _opener(timeout: float):
    # 默认禁用环境代理（龍魂铁律：直连优先，防 socks5h 劫持）
    return _ur.build_opener(_ur.ProxyHandler({}))


def get(url: str, headers: dict = None, timeout: float = 15.0) -> dict:
    """GET 请求 → {status, headers, body, error}"""
    req = _ur.Request(url, headers={"User-Agent": _UA, **(headers or {})})
    try:
        with _opener(timeout).open(req, timeout=timeout) as r:
            return {"status": r.status, "headers": dict(r.headers),
                    "body": r.read().decode("utf-8", "replace"), "error": None}
    except _ue.HTTPError as e:
        return {"status": e.code, "headers": dict(e.headers),
                "body": e.read().decode("utf-8", "replace"), "error": f"HTTP {e.code}"}
    except Exception as e:
        return {"status": None, "headers": {}, "body": "", "error": str(e)}


def post(url: str, data=None, json=None, headers: dict = None, timeout: float = 15.0) -> dict:
    """POST 请求（json 自动序列化）→ {status, body, error}"""
    body = None
    hdrs = {"User-Agent": _UA}
    if json is not None:
        body = _json.dumps(json, ensure_ascii=False).encode("utf-8")
        hdrs["Content-Type"] = "application/json; charset=utf-8"
    elif data is not None:
        body = data if isinstance(data, bytes) else str(data).encode("utf-8")
    req = _ur.Request(url, data=body, headers={**hdrs, **(headers or {})}, method="POST")
    try:
        with _opener(timeout).open(req, timeout=timeout) as r:
            return {"status": r.status, "headers": dict(r.headers),
                    "body": r.read().decode("utf-8", "replace"), "error": None}
    except _ue.HTTPError as e:
        return {"status": e.code, "headers": dict(e.headers),
                "body": e.read().decode("utf-8", "replace"), "error": f"HTTP {e.code}"}
    except Exception as e:
        return {"status": None, "headers": {}, "body": "", "error": str(e)}


def get_json(url: str, timeout: float = 15.0):
    """GET + JSON 解析"""
    r = get(url, timeout=timeout)
    if r["error"]:
        return r
    try:
        r["data"] = _json.loads(r["body"])
    except Exception as e:
        r["error"] = f"JSON 解析失败: {e}"
    return r
