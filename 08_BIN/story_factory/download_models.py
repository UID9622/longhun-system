# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·戊辰·丙辰·䷸巽为风-CODE-补DNA-d4050649
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · ComfyUI 模型下载器（HF 镜像）
下载 SD 1.5 + AnimateDiff motion module，断点续传。
"""
import os
import sys
from pathlib import Path
from huggingface_hub import hf_hub_download

FACTORY_DIR = Path(__file__).resolve().parent
COMFY_DIR = FACTORY_DIR / "third_party" / "ComfyUI"
AD_DIR = COMFY_DIR / "custom_nodes" / "ComfyUI-AnimateDiff-Evolved"

# 固定输出位置
CHECKPOINT_DIR = COMFY_DIR / "models" / "checkpoints"
MOTION_DIR = AD_DIR / "models"

# 模型清单 (repo_id, filename, subfolder, output_dir)
MODELS = [
    # SD 1.5 基础模型 —— 轻量化 pruned EMA-only，约 4GB
    ("runwayml/stable-diffusion-v1-5", "v1-5-pruned-emaonly.ckpt", "", CHECKPOINT_DIR),
    # AnimateDiff SD1.5 v2 motion module，约 1.6GB
    ("guoyww/animatediff", "mm_sd_v15_v2.ckpt", "", MOTION_DIR),
]


def download(repo_id: str, filename: str, subfolder: str, local_dir: Path) -> Path:
    local_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
    print(f"📥 下载 {repo_id}/{subfolder}/{filename} -> {local_dir}")
    path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        subfolder=subfolder if subfolder else None,
        local_dir=str(local_dir),
        local_dir_use_symlinks=False,
        resume_download=True,
    )
    print(f"✅ 完成: {path}")
    return Path(path)


def main():
    print("🐉 龍魂 · ComfyUI 模型下载器")
    print(f"HF_ENDPOINT={os.environ.get('HF_ENDPOINT', 'https://hf-mirror.com')}")
    for repo_id, filename, subfolder, out_dir in MODELS:
        try:
            download(repo_id, filename, subfolder, out_dir)
        except Exception as e:
            print(f"❌ 失败 {repo_id}/{filename}: {e}")
            sys.exit(1)
    print("\n✅ 全部模型下载完成")


if __name__ == "__main__":
    main()
