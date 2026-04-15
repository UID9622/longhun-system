#!/usr/bin/env python3
"""
龍魂·网关测试脚本
DNA: #龍芯⚡️2026-04-06-test-gateway-fix-v1.1
修正: app.py路径=/chat · longhun_local_service=HTTPS:8765
"""
import urllib.request, urllib.error, json, ssl

# ── 忽略自签名证书（本地服务）──
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def test(label, url, data=None, method="GET"):
    try:
        body = json.dumps(data).encode() if data else None
        req  = urllib.request.Request(url, data=body,
               headers={"Content-Type": "application/json"} if body else {})
        from urllib.parse import quote
        if "://" in url:
            parts = url.split("/", 3)
            if len(parts) == 4:
                url = "/".join(parts[:3]) + "/" + quote(parts[3], safe="/?=&")
        resp = urllib.request.urlopen(url if not body else req, timeout=5, context=ctx) if not body else urllib.request.urlopen(req, timeout=5, context=ctx)
        print(f"  ✅ {label}: {resp.status}")
        print(f"     {resp.read(200).decode()[:120]}")
    except urllib.error.HTTPError as e:
        print(f"  ❌ {label}: HTTP {e.code}")
    except Exception as e:
        print(f"  ❌ {label}: {e}")

print("\n🐉 龍魂·网关联通测试\n")

# app.py :8000
test("app.py /chat (POST)",
     "http://127.0.0.1:8000/chat",
     {"messages": [{"role": "user", "content": "你好，27等于多少"}]})

test("app.py /health (GET)", "http://127.0.0.1:8000/health")

# longhun_local_service :8765 (HTTPS·自签名)
test("local_service / (GET)",      "https://127.0.0.1:8765/")
test("local_service 健康检查",     "https://127.0.0.1:8765/健康检查")
test("local_service 查询状态",     "https://127.0.0.1:8765/查询状态")
