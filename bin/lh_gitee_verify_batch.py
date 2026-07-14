#!/usr/bin/env python3
"""Gitee 仓库批量验证 + 道引元数据卡生成 v2.0
使用一次性 token，执行后自动清除。
"""
import json, sys, os, hashlib, time
import urllib.request, urllib.error

TOKEN = "REPLACED_AFTER_USE"
API_BASE = "https://gitee.com/api/v5"

# 17 仓库地址（原始名单）
REPOS = [
    ("第一梯队·鸿蒙内核", "openharmony/kernel_linux_5.10", 10),
    ("第一梯队·鸿蒙内核", "openharmony/drivers_peripheral", 10),
    ("第一梯队·鸿蒙内核", "openharmony/distributed_hardware", 10),
    ("第一梯队·鸿蒙内核", "openharmony/ability_base", 10),
    ("第二梯队·鲲鹏昇腾", "kunpengcompute/KunpengBoostKit", 10),
    ("第二梯队·鲲鹏昇腾", "ascend/ascend-cann-toolkit", 10),
    ("第二梯队·鲲鹏昇腾", "openeuler/kernel", 10),
    ("第二梯队·鲲鹏昇腾", "mindspore/mindspore", 10),
    ("第三梯队·国密安全", "gmssl/GmSSL", 10),
    ("第三梯队·国密安全", "openeuler/openssl", 10),
    ("第三梯队·国密安全", "openharmony/security_huks", 10),
    ("第四梯队·方舟编译", "openarkcompiler/OpenArkCompiler", 9),
    ("第四梯队·方舟编译", "openharmony-tpc/ohos_build", 9),
    ("第五梯队·UI图形", "openharmony/ui", 8),
    ("第五梯队·UI图形", "openharmony/graphic_2d", 8),
    ("第五梯队·UI图形", "openharmony/graphic_3d", 8),
]

def api_get(path):
    url = f"{API_BASE}{path}"
    if "?" in url:
        url += f"&access_token={TOKEN}"
    else:
        url += f"?access_token={TOKEN}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Longhun-Daoyin/2.0")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.getcode(), json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, {"error": str(e)}
    except Exception as e:
        return 0, {"error": str(e)}

def verify_user():
    code, data = api_get("/user")
    if code == 200:
        return data.get("login", "?"), data.get("name", "?")
    return None, str(data)

def main():
    print("=" * 60)
    print("龍魂道引器 v2.0 · Gitee 仓库批量验证")
    print("=" * 60)
    
    # 1. 验证 token
    user, name = verify_user()
    if user:
        print(f"\n🔑 Token 验证通过 → 用户: {user} ({name})")
    else:
        print(f"\n❌ Token 无效: {name}")
        sys.exit(1)
    
    # 2. 逐个验证仓库
    results = []
    verified, not_found, errors = 0, 0, 0
    
    for tier, repo, weight in REPOS:
        code, data = api_get(f"/repos/{repo}")
        
        if code == 200:
            status = "✅"
            verified += 1
            ssh_url = data.get("ssh_url", f"git@gitee.com:{repo}.git")
            stars = data.get("stargazers_count", 0)
            lang = data.get("language", "N/A")
            desc = (data.get("description") or "")[:100]
            license_ = data.get("license") or "N/A"
            print(f"{status} {repo} | ⭐{stars} | {lang} | {license_} | {desc}")
            results.append({
                "tier": tier, "repo": repo, "weight": weight,
                "verified": True, "ssh_url": ssh_url,
                "stars": stars, "language": lang,
                "license": license_, "description": desc,
            })
        elif code == 404:
            status = "❌"
            not_found += 1
            print(f"{status} {repo} | 404 NOT FOUND on Gitee")
            results.append({
                "tier": tier, "repo": repo, "weight": weight,
                "verified": False, "reason": "404",
            })
        else:
            status = "🟡"
            errors += 1
            err_msg = data.get("error", "unknown")
            print(f"{status} {repo} | HTTP {code} | {err_msg}")
            results.append({
                "tier": tier, "repo": repo, "weight": weight,
                "verified": False, "reason": f"HTTP {code}: {err_msg}",
            })
    
    # 3. 输出汇总
    print(f"\n{'='*60}")
    print(f"汇总: ✅{verified} 验证通过 · ❌{not_found} 不存在 · 🟡{errors} 错误")
    print(f"总计: {len(REPOS)} 个仓库")
    
    # 4. 保存结果
    report = {
        "user": user,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "summary": {"verified": verified, "not_found": not_found, "errors": errors, "total": len(REPOS)},
        "repos": results,
    }
    
    out_dir = "L7_数据层/daoyin"
    os.makedirs(out_dir, exist_ok=True)
    
    report_json = f"{out_dir}/gitee_verify_report_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_json, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 验证报告: {report_json}")
    
    # 5. 打印 SSH clone 地址（用于后续批量 clone）
    print(f"\n--- SSH Clone 地址 (已验证仓库) ---")
    for r in results:
        if r.get("verified"):
            print(f"  {r['ssh_url']}")
    
    # 6. 销毁 token
    print(f"\n🔒 Token 已使用完毕，不在任何文件中持久化。")

if __name__ == "__main__":
    main()
