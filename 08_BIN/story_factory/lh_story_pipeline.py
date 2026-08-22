#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍芯⚡️丙午·丙申·辛酉·午时·☰乾-STORY-PIPELINE-v1.0
"""
🐉 龍魂 · 故事流水线 v1.0
把角色卡、素材货架、语音引擎、视频引擎串成一条链。
输入: 剧本/分镜表 JSON
输出: 带 DNA 的音频、视频、合成清单
"""

import argparse
import json
import hashlib
import time
from pathlib import Path
from datetime import datetime

FACTORY_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = FACTORY_ROOT / "output" / "pipelines"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_dna(project: str = "PIPELINE") -> str:
    h = hashlib.sha256(f"{project}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{project}-{h}-UID9622"


def load_project(project: str) -> dict:
    project_dir = FACTORY_ROOT / "assets" / project
    meta_file = project_dir / "project.json"
    if not meta_file.exists():
        raise FileNotFoundError(f"项目不存在: {project}")
    with open(meta_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_character(project: str, code: str) -> dict:
    char_file = FACTORY_ROOT / "assets" / project / "characters" / f"{code}.json"
    if not char_file.exists():
        return {}
    with open(char_file, "r", encoding="utf-8") as f:
        return json.load(f)


def run_scene(scene: dict, project: str, backend_video: str = "ffmpeg", backend_voice: str = "system") -> dict:
    """
    运行一个场景镜头。
    scene = {
      "shot_code": "EP01-S01",
      "character": "HD-002",
      "asset": "ENV-02_老街雨夜.png",
      "line": "嘿，别再等了。",
      "action": "持刀站立，雨滴从帽檐滴落",
      "duration": 4
    }
    """
    from lh_video_engine import generate as video_generate
    from lh_voice_engine import synthesize as voice_synthesize
    from lh_watermark import add_watermark
    from lh_warehouse import get_asset_path

    shot_code = scene.get("shot_code", "SHOT")
    char_code = scene.get("character", "")
    char = load_character(project, char_code)
    persona = char.get("persona", char_code) if char else char_code

    # 1. 语音
    audio_path = None
    if scene.get("line"):
        audio_path = voice_synthesize(scene["line"], persona or "P-LH-001", backend_voice)

    # 2. 视频（基于场景图或角色图，优先从素材仓库查）
    video_path = None
    image_path = scene.get("asset", "")
    img_full = None
    if image_path:
        # 先当作编码查仓库索引
        img_full = get_asset_path(image_path)
        if not img_full or not img_full.exists():
            # 再当作相对路径查
            img_full = FACTORY_ROOT / "assets" / project / "scenes" / image_path
            if not img_full.exists():
                img_full = FACTORY_ROOT / "assets" / project / "characters" / image_path
    if img_full and img_full.exists():
        prompt = f"{scene.get('action','')}, {char_code}, 电影感镜头"
        video_path = video_generate(str(img_full), prompt, backend_video, scene.get("duration", 3), shot_code)

    # 3. 注入可见水印
    wm_path = None
    if video_path:
        wm_path = video_path.parent / f"{video_path.stem}_longhun{video_path.suffix}"
        # 视频水印需要单独处理，这里 placeholder
        wm_path = video_path

    result = {
        "shot_code": shot_code,
        "dna": generate_dna(shot_code),
        "character": char_code,
        "persona": persona,
        "line": scene.get("line", ""),
        "audio": str(audio_path) if audio_path else None,
        "video": str(video_path) if video_path else None,
        "watermarked": str(wm_path) if wm_path else None,
    }
    return result


def run_pipeline(project: str, script_file: str, backend_video: str = "ffmpeg", backend_voice: str = "system"):
    """运行完整分镜表。"""
    project_meta = load_project(project)
    with open(script_file, "r", encoding="utf-8") as f:
        script = json.load(f)

    pipeline_dna = generate_dna(project)
    results = []
    print(f"🎬 龍魂故事流水线启动")
    print(f"🧬 Pipeline DNA: {pipeline_dna}")
    print(f"📁 项目: {project}")
    print(f"🎞️ 场景数: {len(script.get('scenes', []))}")
    print("")

    for scene in script.get("scenes", []):
        res = run_scene(scene, project, backend_video, backend_voice)
        results.append(res)
        print("")

    # 保存清单
    manifest = {
        "dna": pipeline_dna,
        "project": project,
        "project_dna": project_meta.get("dna", ""),
        "script": script_file,
        "backends": {"video": backend_video, "voice": backend_voice},
        "shots": results,
        "created": datetime.now().isoformat(),
    }
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    manifest_path = OUTPUT_DIR / f"{project}_pipeline_{ts}.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"✅ 流水线完成，清单保存: {manifest_path}")
    return manifest


def main():
    parser = argparse.ArgumentParser(description="龍魂 · 故事流水线")
    parser.add_argument("--project", required=True, help="项目名")
    parser.add_argument("--script", required=True, help="分镜表 JSON 路径")
    parser.add_argument("--backend-video", default="ffmpeg", help="视频后端")
    parser.add_argument("--backend-voice", default="system", help="语音后端")
    args = parser.parse_args()

    run_pipeline(args.project, args.script, args.backend_video, args.backend_voice)


if __name__ == "__main__":
    main()
