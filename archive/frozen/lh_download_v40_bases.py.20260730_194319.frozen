#!/usr/bin/env python3
#龍芯⚡️20260719002000000-V40-BASE-DOWNLOAD
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
v4.0 底座候选模型下载脚本
后台并行下载 3 个候选底座到 models/base_models_v4.0/
DNA: #龍芯⚡️20260719002000000-V40-BASE-DOWNLOAD
"""

import os, subprocess, json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

PROJECT = Path(__file__).resolve().parent.parent
BASE_DIR = PROJECT / "models" / "base_models_v4.0"
BASE_DIR.mkdir(parents=True, exist_ok=True)

CANDIDATES = [
    {
        "name": "DeepSeek-R1-Distill-Llama-8B",
        "repo": "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
        "license": "MIT",
        "size_gb": "~16GB (FP16)",
        "priority": 1,
    },
    {
        "name": "Meta-Llama-3.1-8B-Instruct",
        "repo": "meta-llama/Llama-3.1-8B-Instruct",
        "license": "Llama 3.1 Community License",
        "size_gb": "~16GB (FP16)",
        "priority": 2,
    },
    {
        "name": "Yi-1.5-9B-Chat",
        "repo": "01-ai/Yi-1.5-9B-Chat",
        "license": "Apache 2.0",
        "size_gb": "~18GB (FP16)",
        "priority": 3,
    },
]


def download_model(candidate):
    name = candidate["name"]
    repo = candidate["repo"]
    target = BASE_DIR / name
    target.mkdir(parents=True, exist_ok=True)
    
    print(f"📥 开始下载: {name} ({repo})")
    env = os.environ.copy()
    env["HF_ENDPOINT"] = "https://hf-mirror.com"
    try:
        result = subprocess.run(
            ["huggingface-cli", "download", repo, "--local-dir", str(target), "--local-dir-use-symlinks", "False"],
            capture_output=True, text=True, timeout=7200, env=env
        )
        if result.returncode == 0:
            print(f"✅ 完成: {name} → {target}")
            return {"name": name, "status": "success", "path": str(target)}
        else:
            print(f"❌ 失败: {name}\n{result.stderr[:500]}")
            return {"name": name, "status": "failed", "error": result.stderr[:500]}
    except Exception as e:
        print(f"❌ 异常: {name} → {e}")
        return {"name": name, "status": "error", "error": str(e)}


def main():
    print("=" * 60)
    print("🐉 v4.0 底座候选模型下载")
    print(f"   目标目录: {BASE_DIR}")
    print(f"   候选数量: {len(CANDIDATES)}")
    print("=" * 60)
    
    results = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(download_model, c): c for c in CANDIDATES}
        for future in as_completed(futures):
            results.append(future.result())
    
    report_path = BASE_DIR / "download_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print("✅ 下载任务完成")
    for r in results:
        print(f"   {r['name']}: {r['status']}")
    print(f"   报告: {report_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
