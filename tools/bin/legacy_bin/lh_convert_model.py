#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""龍魂·底模转换脚本 — HF→MLX 离线模式"""
import os, sys, time
os.environ["HF_HUB_OFFLINE"] = "1"  # 强制离线，不从网络下载

print(">>> 底模转换: Qwen2.5-1.5B-Instruct → MLX (离线模式)")
start = time.time()

from mlx_lm import convert

# 先确保目标目录不存在
import shutil
target = "models/longhun-v1.0/base_model"
if os.path.exists(target):
    shutil.rmtree(target)
    print(f"   已清除旧目录: {target}")

print("   开始转换...")
convert("Qwen/Qwen2.5-1.5B-Instruct", mlx_path=target, quantize=False)
print(f"   ✅ 转换完成 ({time.time()-start:.1f}s)")
print(f"   输出: {target}")
