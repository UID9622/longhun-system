#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v4.0 底座候选模型下载脚本（ModelScope 魔搭 fallback）
当 HuggingFace / hf-mirror 不可用时使用，国内链路更稳。
DNA: #龍芯⚡️20260719003000000-V40-BASE-DOWNLOAD-MODELSCOPE
"""

import os, json
from pathlib import Path
from modelscope.hub.snapshot_download import snapshot_download

PROJECT = Path(__file__).resolve().parent.parent
BASE_DIR = PROJECT / "models" / "base_models_v4.0"
BASE_DIR.mkdir(parents=True, exist_ok=True)

# ModelScope 模型 ID 映射
CANDIDATES = [
    {
        "name": "DeepSeek-R1-Distill-Llama-8B",
        "model_id": "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
        "priority": 1,
    },
    {
        "name": "Meta-Llama-3.1-8B-Instruct",
        "model_id": "LLM-Research/Meta-Llama-3.1-8B-Instruct",
        "priority": 2,
    },
    {
        "name": "Yi-1.5-9B-Chat",
        "model_id": "01ai/Yi-1.5-9B-Chat",
        "priority": 3,
    },
]


def download_model(candidate):
    name = candidate["name"]
    model_id = candidate["model_id"]
    target = BASE_DIR / name
    
    print(f"📥 [ModelScope] 开始下载: {name} ({model_id})")
    try:
        path = snapshot_download(model_id, cache_dir=str(BASE_DIR / ".cache"))
        print(f"✅ [ModelScope] 完成: {name} → {path}")
        return {"name": name, "status": "success", "path": path}
    except Exception as e:
        print(f"❌ [ModelScope] 失败: {name} → {e}")
        return {"name": name, "status": "failed", "error": str(e)}


def main():
    print("=" * 60)
    print("🐉 v4.0 底座候选模型下载（ModelScope fallback）")
    print(f"   目标目录: {BASE_DIR}")
    print("=" * 60)
    
    results = []
    for c in sorted(CANDIDATES, key=lambda x: x["priority"]):
        results.append(download_model(c))
    
    report_path = BASE_DIR / "download_report_modelscope.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print("✅ ModelScope 下载任务完成")
    for r in results:
        print(f"   {r['name']}: {r['status']}")
    print(f"   报告: {report_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
