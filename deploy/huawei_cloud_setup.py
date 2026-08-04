#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·未济-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
🐉 龍魂 · 华为云一键配置 v5
SdkRequest + SDK Signer + requests 发送 = 完美组合
"""
import json, sys
import requests
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.sdk_request import SdkRequest
from huaweicloudsdkcore.signer.signer import Signer

CRED_FILE = "/Users/zuimeidedeyihan/.longhun/huawei-credentials.json"
TARGET_IP = "119.13.90.27"
PORT = 11434

def load():
    with open(CRED_FILE) as f:
        return json.load(f)

def signed_request(method, scheme, host, uri, query, headers, body, ak, sk):
    """构造 + 签名 + 发送"""
    if query:
        uri = uri + "?" + "&".join(f"{k}={v}" for k, v in sorted(query))
    req = SdkRequest(method=method, schema=scheme, host=host,
                     resource_path=uri.split("?")[0], uri=uri,
                     query_params=[(k, str(v)) for k, v in sorted(query)] if query else [],
                     header_params=dict(headers),
                     body=json.dumps(body).encode() if body else None)

    creds = BasicCredentials(ak, sk)
    signer = Signer(creds)
    signed = signer.sign(req)

    url = f"{signed.schema}://{signed.host}{signed.uri}"
    resp = requests.request(signed.method, url, headers=dict(signed.header_params),
                            data=signed.body, verify=False, timeout=30)
    if resp.status_code >= 400:
        return {"_error": resp.status_code, "_body": resp.text[:300]}
    return resp.json()

REGIONS = ["cn-north-4", "cn-north-1", "cn-south-1", "cn-east-3", "cn-east-2",
           "ap-southeast-3", "cn-north-2", "cn-south-2", "cn-south-4",
           "cn-east-4", "cn-east-5", "cn-north-9", "cn-southwest-2"]

def list_projects(ak, sk):
    h = {"Content-Type": "application/json;charset=utf-8"}
    r = signed_request("GET", "https", "iam.myhuaweicloud.com",
                       "/v3/projects", [], h, None, ak, sk)
    return [{"id": p["id"], "name": p["name"], "enabled": p.get("enabled", True)}
            for p in r.get("projects", [])]

def find_server(region, pid, ak, sk):
    host = f"ecs.{region}.myhuaweicloud.com"
    h = {"Content-Type": "application/json;charset=utf-8", "X-Project-Id": pid}
    r = signed_request("GET", "https", host,
                       f"/v2/{pid}/servers/detail", [("limit", 100)], h, None, ak, sk)
    if "_error" in r:
        return None
    for srv in r.get("servers", []):
        for addrs in srv.get("addresses", {}).values():
            for a in addrs:
                if a.get("addr") == TARGET_IP:
                    return {
                        "id": srv["id"], "name": srv["name"],
                        "flavor": srv["flavor"]["name"],
                        "security_groups": [{"id": s["id"], "name": s.get("name","")}
                                           for s in srv.get("security_groups", [])],
                        "volumes": srv.get("os-extended-volumes:volumes_attached", []),
                        "region": region, "project_id": pid,
                    }
    return None

def list_sg_rules(region, pid, ak, sk, sg_id):
    host = f"vpc.{region}.myhuaweicloud.com"
    h = {"Content-Type": "application/json;charset=utf-8", "X-Project-Id": pid}
    r = signed_request("GET", "https", host,
                       "/v2.0/security-group-rules", [("security_group_id", sg_id)],
                       h, None, ak, sk)
    return r.get("security_group_rules", [])

def add_sg_rule(region, pid, ak, sk, sg_id):
    host = f"vpc.{region}.myhuaweicloud.com"
    h = {"Content-Type": "application/json;charset=utf-8", "X-Project-Id": pid}
    body = {"security_group_rule": {
        "direction": "ingress", "ethertype": "IPv4", "protocol": "tcp",
        "port_range_min": PORT, "port_range_max": PORT,
        "remote_ip_prefix": "0.0.0.0/0",
        "description": "龍魂 Ollama API",
        "security_group_id": sg_id,
    }}
    return signed_request("POST", "https", host,
                          "/v2.0/security-group-rules", [], h, body, ak, sk)

def get_volumes(region, pid, ak, sk, server_id):
    host = f"evs.{region}.myhuaweicloud.com"
    h = {"Content-Type": "application/json;charset=utf-8", "X-Project-Id": pid}
    r = signed_request("GET", "https", host,
                       f"/v2/{pid}/os-vendor-volumes", [("server_id", server_id)],
                       h, None, ak, sk)
    return r.get("volumes", [])

def resize_volume(region, pid, ak, sk, vid, new_size):
    host = f"evs.{region}.myhuaweicloud.com"
    h = {"Content-Type": "application/json;charset=utf-8", "X-Project-Id": pid}
    body = {"os-extend": {"new_size": new_size}}
    return signed_request("POST", "https", host,
                          f"/v2/{pid}/os-vendor-volumes/{vid}/action",
                          [], h, body, ak, sk)


def main():
    creds = load()
    ak = creds["access_key"]["id"]
    sk = creds["access_key"]["secret"]
    requests.packages.urllib3.disable_warnings()

    print("=" * 58)
    print("🐉 龍魂 · 华为云一键配置 v5")
    print(f"   目标: {TARGET_IP}")
    print("=" * 58)

    # 1. 项目列表
    print("\n📋 获取项目列表...")
    projects = list_projects(ak, sk)
    active = [p for p in projects if p.get("enabled", True)]
    for p in active:
        print(f"   📂 {p['name']} ({p['id'][:24]}...)")

    # 2. 搜索 ECS
    print(f"\n🔍 搜索 ECS ({TARGET_IP})...")
    server = None
    errors = []
    for p in active:
        pid = p["id"]
        # 优先用项目名匹配的 region
        match_region = p["name"] if p["name"] in REGIONS else None
        try_regions = [match_region] + [r for r in REGIONS if r != match_region] if match_region else REGIONS
        for region in try_regions:
            try:
                srv = find_server(region, pid, ak, sk)
                if srv:
                    server = srv
                    print(f"   ✅ {srv['name']} | {region} | {p['name']} | {srv['flavor']}")
                    break
            except Exception as e:
                errors.append(f"{p['name']}/{region}: {e}")
        if server:
            break
    
    if not server:
        print(f"   尝试了多轮查询，均未找到")
        if errors:
            for e in errors[-5:]:
                print(f"   ⚠️ {e}")

    if not server:
        print("   ❌ 未找到 ECS。请确认凭证正确。")
        sys.exit(1)

    # 3. 安全组放行
    print(f"\n🔓 安全组 (放行 {PORT}):")
    for sg in server["security_groups"]:
        print(f"   📛 {sg['name']} ({sg['id']})")
        try:
            rules = list_sg_rules(server["region"], server["project_id"], ak, sk, sg["id"])
            found = any(r.get("direction") == "ingress" and r.get("port_range_min") == PORT for r in rules)
            if found:
                print(f"   ✅ 规则已存在")
                continue
            result = add_sg_rule(server["region"], server["project_id"], ak, sk, sg["id"])
            if "_error" in result:
                print(f"   ❌ HTTP {result['_error']}: {result.get('_body','')[:120]}")
            else:
                rule = result.get("security_group_rule", {})
                print(f"   ✅ 已放行 ({rule.get('id','?')})")
        except Exception as e:
            print(f"   ❌ {e}")

    # 4. 磁盘
    print("\n💾 磁盘:")
    try:
        vols = get_volumes(server["region"], server["project_id"], ak, sk, server["id"])
        for v in vols:
            sz = v.get("size", "?")
            f = "🔴" if isinstance(sz, int) and sz <= 40 else "🟢"
            bt = " (系统盘)" if v.get("bootable") == "true" else ""
            print(f"   {f} {v.get('name','?')} = {sz}GB {v.get('volume_type','?')}{bt}")
        sysv = next((v for v in vols if v.get("bootable") == "true"), vols[0] if vols else None)
        if sysv and isinstance(sysv.get("size"), int) and sysv["size"] <= 40:
            ns = 100
            print(f"\n   ⚠️ 仅 {sysv['size']}GB → 扩容至 {ns}GB...")
            result = resize_volume(server["region"], server["project_id"], ak, sk, sysv["id"], ns)
            if "_error" in result:
                print(f"   ❌ {result['_error']}: {result.get('_body','')[:120]}")
            else:
                print(f"   ✅ 已提交 (JobID: {result.get('job_id','?')})")
                print(f"   📋 扩完后 SSH: sudo growpart /dev/vda 1 && sudo resize2fs /dev/vda1")
    except Exception as e:
        print(f"   ❌ {e}")

    print("\n" + "=" * 58)
    print(f"✅ 完成！验证: curl http://{TARGET_IP}:{PORT}/api/tags")
    print("=" * 58)

if __name__ == "__main__":
    main()
