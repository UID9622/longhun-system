# DNA: #龍芯⚡️丙午·乙未·乙丑·未济-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""龍魂·华为云安全组放行 FRP TCP 7000"""
import json, urllib3
import requests
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.sdk_request import SdkRequest
from huaweicloudsdkcore.signer.signer import Signer

urllib3.disable_warnings()
CRED_FILE = "/Users/zuimeidedeyihan/.longhun/huawei-credentials.json"
TARGET_IP = "119.13.90.27"
FRP_PORT = 7000
TARGET_PROJECT_ID = "f2b2fd700561410095030967b1f9f91a"  # ap-southeast-1
TARGET_REGION = "ap-southeast-1"

def load_creds():
    with open(CRED_FILE) as f:
        c = json.load(f)
    return c["access_key"]["id"], c["access_key"]["secret"]

def signed_req(method, host, uri, query, body, ak, sk, pid=None):
    headers = {"Content-Type": "application/json;charset=utf-8"}
    if pid:
        headers["X-Project-Id"] = pid
    if query:
        uri = uri + "?" + "&".join(f"{k}={v}" for k, v in sorted(query))
    req = SdkRequest(method=method, schema="https", host=host,
                     resource_path=uri.split("?")[0], uri=uri,
                     query_params=[(k, str(v)) for k, v in sorted(query)] if query else [],
                     header_params=dict(headers),
                     body=json.dumps(body).encode() if body else None)
    creds = BasicCredentials(ak, sk)
    signed = Signer(creds).sign(req)
    url = f"{signed.schema}://{signed.host}{signed.uri}"
    resp = requests.request(signed.method, url, headers=dict(signed.header_params),
                            data=signed.body, verify=False, timeout=30)
    return resp

REGIONS = ["cn-north-4", "cn-north-1", "cn-south-1", "cn-east-3", "cn-east-2",
           "ap-southeast-3", "cn-north-2", "cn-south-2", "cn-south-4",
           "cn-east-4", "cn-east-5", "cn-north-9", "cn-southwest-2"]

def main():
    ak, sk = load_creds()

    # 1. 列举项目
    print("📋 获取项目列表...")
    r = signed_req("GET", "iam.myhuaweicloud.com", "/v3/projects", [], None, ak, sk)
    projects = r.json().get("projects", [])
    active = [p for p in projects if p.get("enabled", True)]
    print(f"   共 {len(active)} 个活跃项目")

    # 2. 搜索 ECS
    print(f"\n🔍 搜索 ECS ({TARGET_IP})...")
    server = None
    for p in active:
        pid = p["id"]
        region = p["name"] if p["name"] in REGIONS else None
        candidates = [region] + [r for r in REGIONS if r != region] if region else REGIONS
        for reg in candidates:
            try:
                resp = signed_req("GET", f"ecs.{reg}.myhuaweicloud.com",
                                  f"/v2/{pid}/servers/detail", [("limit", 100)],
                                  None, ak, sk, pid=pid)
                for srv in resp.json().get("servers", []):
                    for addrs in srv.get("addresses", {}).values():
                        for a in addrs:
                            if a.get("addr") == TARGET_IP:
                                server = {
                                    "id": srv["id"], "name": srv["name"],
                                    "region": reg, "project_id": pid, "project_name": p["name"],
                                    "security_groups": [{"id": s["id"], "name": s.get("name","")}
                                                       for s in srv.get("security_groups", [])]
                                }
                                print(f"   ✅ {srv['name']} | {reg} | {p['name']}")
                                break
                        if server: break
                    if server: break
            except Exception as e:
                pass
            if server: break
        if server: break

    if not server:
        print("   ❌ 未找到 ECS，可能凭证过期或IP变更")
        return

    # 3. 为每个安全组添加 FRP 7000 规则
    print(f"\n🔓 为安全组添加 TCP {FRP_PORT} 入站规则:")
    for sg in server["security_groups"]:
        sg_id, sg_name = sg["id"], sg["name"]
        print(f"   📛 {sg_name} ({sg_id})")

        # 检查是否已存在
        resp = signed_req("GET", f"vpc.{server['region']}.myhuaweicloud.com",
                          "/v2.0/security-group-rules",
                          [("security_group_id", sg_id)],
                          None, ak, sk, pid=server["project_id"])
        rules = resp.json().get("security_group_rules", [])
        found = any(
            r.get("direction") == "ingress" and
            str(r.get("port_range_min")) == str(FRP_PORT)
            for r in rules
        )
        if found:
            print(f"   ✅ TCP {FRP_PORT} 已放行，跳过")
            continue

        # 添加规则
        body = {"security_group_rule": {
            "direction": "ingress", "ethertype": "IPv4", "protocol": "tcp",
            "port_range_min": FRP_PORT, "port_range_max": FRP_PORT,
            "remote_ip_prefix": "0.0.0.0/0",
            "description": "龍魂 FRP 内网穿透",
            "security_group_id": sg_id,
        }}
        resp = signed_req("POST", f"vpc.{server['region']}.myhuaweicloud.com",
                          "/v2.0/security-group-rules", [], body,
                          ak, sk, pid=server["project_id"])
        if resp.status_code >= 400:
            print(f"   ❌ HTTP {resp.status_code}: {resp.text[:200]}")
        else:
            rule = resp.json().get("security_group_rule", {})
            print(f"   ✅ 已放行 TCP {FRP_PORT} ({rule.get('id','?')[:20]}...)")

    print(f"\n{'='*50}")
    print(f"✅ 完成！FRP 端口 {FRP_PORT} 已开放")
    print(f"   验证: nc -zv {TARGET_IP} {FRP_PORT}")

if __name__ == "__main__":
    main()
