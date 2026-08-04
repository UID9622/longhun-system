#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""龍魂·训练语料构建器 — 从 data/training/ 全量抽取文本"""
import os, sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRAINING_DIR = ROOT / "data" / "training"
CORPUS_OUT = ROOT / "models" / "longhun-v1.0" / "training_corpus_v3.0.md"

TEXT_EXTS = {'.md', '.txt', '.py', '.js', '.ts', '.html', '.css', '.json', '.csv', 
             '.yaml', '.yml', '.toml', '.xml', '.sh', '.bash', '.zsh', '.cnsh',
             '.sql', '.r', '.java', '.go', '.rs', '.c', '.cpp', '.h', '.hpp'}
SKIP_DIRS = {'__pycache__', '.git', 'node_modules', 'venv', '.venv', 'dist', 'build',
             '.DS_Store', 'Photo Booth图库', 'Pixelmator Pro Sidecar Files'}

def extract_text_files(base_dir):
    files = []
    for root, dirs, filenames in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in TEXT_EXTS or fn.endswith('.textClipping'):
                files.append(os.path.join(root, fn))
    return files

def build_corpus():
    print("🐉 龍魂·语料构建器 v3.0")
    print(f"   扫描: {TRAINING_DIR}")
    
    all_files = extract_text_files(str(TRAINING_DIR))
    print(f"   找到 {len(all_files)} 个文本文件")
    
    # 去重 (同文件名只保留一个)
    seen = {}
    unique = []
    for f in sorted(all_files):
        name = os.path.basename(f)
        if name not in seen:
            seen[name] = f
            unique.append(f)
    
    print(f"   去重后: {len(unique)} 个文件")
    
    total_chars = 0
    with open(CORPUS_OUT, 'w', encoding='utf-8') as out:
        out.write("# 龍魂 v3.0 训练语料\n")
        out.write(f"# 构建时间: 丙午·乙申·己酉·亥时\n")
        out.write(f"# 源文件数: {len(unique)}\n\n")
        
        for fp in unique:
            rel = os.path.relpath(fp, str(TRAINING_DIR))
            try:
                with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                if len(content.strip()) < 10:
                    continue
                out.write(f"\n## FILE: {rel}\n\n")
                out.write(content)
                out.write("\n")
                total_chars += len(content)
            except Exception as e:
                print(f"   ⚠️ 跳过 {rel}: {e}")
    
    size_mb = os.path.getsize(CORPUS_OUT) / 1024 / 1024
    print(f"\n✅ 语料构建完成:")
    print(f"   {CORPUS_OUT}")
    print(f"   {size_mb:.1f} MB · {total_chars:,} 字符")
    return CORPUS_OUT

if __name__ == '__main__':
    build_corpus()
