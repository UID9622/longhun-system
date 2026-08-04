#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_DAOYIN_GITHUB_TO_GITEE-v1.0-5e7e7351
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""龍魂道引器 · GitHub→Gitee 批量搬运
6个仓库：GitHub clone → Gitee push → 元数据归档
铁律：A-028 龍魂道引 · 来源可查 · 入链不可覆
"""

import os
import subprocess
import json
import time
import sys
from pathlib import Path
from datetime import datetime

GIT = "/usr/bin/git"
WORKSPACE = Path("/Users/zuimeidedeyihan/longhun-system/.daoyin_workspace")
ARCHIVE_DIR = Path("/Users/zuimeidedeyihan/longhun-system/.daoyin_workspace/archive")
GITEE_OWNER = "uid9622_admin"
SSH_CMD = "ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15"

REPOS = [
    {
        "name": "distributed_hardware_fwk",
        "github": "git@github.com:openharmony/distributed_hardware_fwk.git",
        "gitee_remote": "gitee",
        "gitee_url": f"git@gitee.com:{GITEE_OWNER}/distributed_hardware_fwk.git",
        "tier": "第一梯队",
        "original_gitee": "openharmony/distributed_hardware",  # 404 的原地址
    },
    {
        "name": "ability_ability_base",
        "github": "git@github.com:openharmony/ability_ability_base.git",
        "gitee_remote": "gitee",
        "gitee_url": f"git@gitee.com:{GITEE_OWNER}/ability_ability_base.git",
        "tier": "第一梯队",
        "original_gitee": "openharmony/ability_base",
    },
    {
        "name": "GmSSL",
        "github": "git@github.com:guanzhi/GmSSL.git",
        "gitee_remote": "gitee",
        "gitee_url": f"git@gitee.com:{GITEE_OWNER}/GmSSL.git",
        "tier": "第三梯队",
        "original_gitee": "gmssl/GmSSL",
    },
    {
        "name": "build",
        "github": "git@github.com:openharmony/build.git",
        "gitee_remote": "gitee",
        "gitee_url": f"git@gitee.com:{GITEE_OWNER}/build.git",
        "tier": "第三梯队",
        "original_gitee": "openharmony-tpc/ohos_build",
    },
    {
        "name": "arkui_ui_lite",
        "github": "git@github.com:openharmony/arkui_ui_lite.git",
        "gitee_remote": "gitee",
        "gitee_url": f"git@gitee.com:{GITEE_OWNER}/arkui_ui_lite.git",
        "tier": "第三梯队",
        "original_gitee": "openharmony/ui",
    },
    {
        "name": "graphic_graphic_2d",
        "github": "git@github.com:openharmony/graphic_graphic_2d.git",
        "gitee_remote": "gitee",
        "gitee_url": f"git@gitee.com:{GITEE_OWNER}/graphic_graphic_2d.git",
        "tier": "第三梯队",
        "original_gitee": "openharmony/graphic_2d",
    },
]


def run(cmd, cwd=None, timeout=300):
    """运行命令，返回 (success, stdout, stderr)"""
    from lh_secure_subprocess import safe_run
    from pathlib import Path
    env = os.environ.copy()
    env["GIT_SSH_COMMAND"] = SSH_CMD
    try:
        result = safe_run(
            cmd, caller='lh_daoyin', timeout=timeout,
            cwd=Path(cwd) if cwd else None, env=env
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "TIMEOUT"
    except Exception as e:
        return False, "", str(e)


def main():
    os.makedirs(WORKSPACE, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    results = []
    started_at = datetime.now().isoformat()

    for i, repo in enumerate(REPOS, 1):
        name = repo["name"]
        github_url = repo["github"]
        gitee_url = repo["gitee_url"]
        tier = repo["tier"]
        original = repo["original_gitee"]

        print(f"\n{'='*60}")
        print(f"[{i}/6] {tier} · {name}")
        print(f"  来源: {github_url}")
        print(f"  目标: {gitee_url}")
        print(f"  原Gitee404: {original}")
        print(f"{'='*60}")

        local_path = WORKSPACE / name

        # Step 1: Clone from GitHub (shallow for speed)
        if local_path.exists():
            print(f"  ⏭️ 本地已有，跳过 clone: {local_path}")
        else:
            print(f"  📥 Clone from GitHub...")
            ok, out, err = run(
                f"{GIT} clone --depth=1 {github_url} {local_path}",
                timeout=600
            )
            if not ok:
                print(f"  ❌ Clone 失败: {err[:200]}")
                results.append({"repo": name, "status": "FAIL_CLONE", "error": err[:200]})
                continue
            print(f"  ✅ Clone 完成")

        # Step 2: Check if Gitee remote already exists, if not add
        ok, remotes, _ = run(f"{GIT} remote -v", cwd=local_path)
        if "gitee" not in remotes:
            ok, out, err = run(
                f"{GIT} remote add gitee {gitee_url}", cwd=local_path
            )
            if not ok and "already exists" not in err:
                print(f"  ⚠️ 添加 Gitee remote 失败: {err[:100]}")
        else:
            # Update if wrong URL
            ok, out, err = run(
                f"{GIT} remote set-url gitee {gitee_url}", cwd=local_path
            )

        # Step 3: Push to Gitee
        print(f"  📤 Push to Gitee...")
        ok, out, err = run(
            f"{GIT} push gitee HEAD:main --force 2>&1",
            cwd=local_path, timeout=600
        )
        if not ok:
            # Try master branch
            ok2, out2, err2 = run(
                f"{GIT} push gitee HEAD:master --force 2>&1",
                cwd=local_path, timeout=600
            )
            if ok2:
                print(f"  ✅ Push 完成 (master 分支)")
            else:
                print(f"  ❌ Push 失败: {err[:200]}")
                results.append({"repo": name, "status": "FAIL_PUSH", "error": err[:200]})
                continue
        else:
            print(f"  ✅ Push 完成 (main 分支)")

        # Step 4: Get size
        size_bytes = sum(f.stat().st_size for f in local_path.rglob('*') if f.is_file())
        size_mb = size_bytes / (1024 * 1024)

        # Step 5: Get commit info
        ok, commit_hash, _ = run(f"{GIT} rev-parse HEAD", cwd=local_path)
        hash_short = commit_hash[:12] if ok else "unknown"

        # Step 6: Archive metadata
        archive_entry = {
            "name": name,
            "tier": tier,
            "github_source": github_url,
            "gitee_target": f"https://gitee.com/{GITEE_OWNER}/{name}",
            "original_gitee_404": original,
            "commit_hash": hash_short,
            "size_mb": round(size_mb, 2),
            "absorbed_at": datetime.now().isoformat(),
            "absorbed_by": "UID9622",
            "daoyin_version": "2.0",
        }
        archive_file = ARCHIVE_DIR / f"{name}.json"
        with open(archive_file, 'w') as f:
            json.dump(archive_entry, f, ensure_ascii=False, indent=2)

        print(f"  📋 归档: {archive_file}")
        print(f"  📦 大小: {size_mb:.1f} MB | Commit: {hash_short}")

        results.append({
            "repo": name,
            "status": "OK",
            "size_mb": round(size_mb, 2),
            "commit": hash_short,
            "gitee_url": archive_entry["gitee_target"],
        })

    # Summary
    print(f"\n{'='*60}")
    print(f"📊 汇总报告 ({len(REPOS)} 仓库)")
    print(f"{'='*60}")
    ok_count = sum(1 for r in results if r["status"] == "OK")
    fail_count = len(results) - ok_count

    for r in results:
        status_icon = "✅" if r["status"] == "OK" else "❌"
        if r["status"] == "OK":
            print(f"  {status_icon} {r['repo']} | {r['size_mb']:.1f}MB | {r['gitee_url']}")
        else:
            print(f"  {status_icon} {r['repo']} | {r.get('error', 'unknown')[:80]}")

    print(f"\n  ✅ 成功: {ok_count} | ❌ 失败: {fail_count}")

    # Write summary
    summary = {
        "started_at": started_at,
        "completed_at": datetime.now().isoformat(),
        "total": len(REPOS),
        "ok": ok_count,
        "failed": fail_count,
        "repos": results,
    }
    with open(ARCHIVE_DIR / "_summary.json", 'w') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n📋 汇总归档: {ARCHIVE_DIR / '_summary.json'}")
    return ok_count == len(REPOS)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
