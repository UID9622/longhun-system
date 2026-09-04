#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍芯⚡️丙午·丙申·辛酉·巳时·☰乾-STORY-FACTORY-v1.0
"""
🐉 龍魂 · 故事工厂 v1.0
小说/剧本 → AI 连续剧资产流水线
核心能力:
  1. 角色卡管理（人脸不动点）
  2. 素材货架仓库（一物一码，终身复用）
  3. 人格声线管理（演员人格 + 导演人格）
  4. DNA/水印注入（龍魂主权标识）
  5. 生成任务编排（对接开源图像/视频/TTS工具）
"""

import argparse
import json
import hashlib
import time
from pathlib import Path
from datetime import datetime

FACTORY_ROOT = Path(__file__).resolve().parent
ASSETS_DIR = FACTORY_ROOT / "assets"
OUTPUT_DIR = FACTORY_ROOT / "output"
CONFIGS_DIR = FACTORY_ROOT / "configs"

for d in [ASSETS_DIR, OUTPUT_DIR, CONFIGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def generate_dna(topic: str = "STORY") -> str:
    h = hashlib.sha256(f"{topic}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{topic}-{h}-UID9622"


def cmd_init(args):
    """初始化故事工厂项目。"""
    project_dir = ASSETS_DIR / args.project
    (project_dir / "characters").mkdir(parents=True, exist_ok=True)
    (project_dir / "props").mkdir(parents=True, exist_ok=True)
    (project_dir / "scenes").mkdir(parents=True, exist_ok=True)
    (project_dir / "voices").mkdir(parents=True, exist_ok=True)
    meta = {
        "project": args.project,
        "dna": generate_dna("PROJECT"),
        "created": datetime.now().isoformat(),
        "status": "initialized",
    }
    with open(project_dir / "project.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"✅ 项目初始化完成: {project_dir}")
    print(f"🧬 DNA: {meta['dna']}")


def cmd_character(args):
    """创建/查看角色卡。"""
    project_dir = ASSETS_DIR / args.project
    char_file = project_dir / "characters" / f"{args.code}.json"
    if args.action == "create":
        data = {
            "code": args.code,
            "name": args.name or args.code,
            "role": args.role or "主角",
            "dna": generate_dna(f"CHAR-{args.code}"),
            "anchors": {
                "face": args.face or "",
                "height": args.height or "",
                "build": args.build or "",
                "age": args.age or "",
                "mark": args.mark or "",
                "costume": args.costume or "",
            },
            "persona": args.persona or "",
            "seed": args.seed or "",
            "created": datetime.now().isoformat(),
        }
        with open(char_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 角色卡创建: {args.code}")
        print(f"🧬 DNA: {data['dna']}")
    elif args.action == "list":
        chars = sorted((project_dir / "characters").glob("*.json"))
        print(f"🎭 项目 [{args.project}] 角色卡列表:")
        for c in chars:
            with open(c, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"  {data['code']:12s} {data['name']:16s} {data['role']}")
    elif args.action == "show":
        if not char_file.exists():
            print(f"❌ 角色卡不存在: {args.code}")
            return
        with open(char_file, "r", encoding="utf-8") as f:
            print(json.dumps(json.load(f), ensure_ascii=False, indent=2))


def cmd_asset(args):
    """素材货架管理。"""
    project_dir = ASSETS_DIR / args.project
    shelf_file = project_dir / "shelf.json"
    shelf = {}
    if shelf_file.exists():
        with open(shelf_file, "r", encoding="utf-8") as f:
            shelf = json.load(f)

    if args.action == "register":
        code = args.code
        shelf[code] = {
            "code": code,
            "category": args.category,
            "name": args.name,
            "path": args.path,
            "dna": generate_dna(f"ASSET-{code}"),
            "created": datetime.now().isoformat(),
        }
        with open(shelf_file, "w", encoding="utf-8") as f:
            json.dump(shelf, f, ensure_ascii=False, indent=2)
        print(f"✅ 素材入库: {code} ({args.category})")
        print(f"🧬 DNA: {shelf[code]['dna']}")
    elif args.action == "list":
        print(f"🗄️ 项目 [{args.project}] 素材货架:")
        for code, info in sorted(shelf.items()):
            print(f"  {code:20s} {info['category']:12s} {info['name']}")


def cmd_persona(args):
    """人格声线管理。"""
    persona_file = CONFIGS_DIR / "personas.json"
    personas = {}
    if persona_file.exists():
        with open(persona_file, "r", encoding="utf-8") as f:
            personas = json.load(f)

    if args.action == "list":
        print("🎙️ 已注册人格:")
        for k, v in sorted(personas.items()):
            print(f"  {k:20s} {v.get('type',''):10s} {v.get('desc','')}")
    elif args.action == "create":
        personas[args.code] = {
            "type": args.type,
            "desc": args.desc,
            "voice": args.voice or "",
            "style": args.style or "",
            "dna": generate_dna(f"PERSONA-{args.code}"),
        }
        with open(persona_file, "w", encoding="utf-8") as f:
            json.dump(personas, f, ensure_ascii=False, indent=2)
        print(f"✅ 人格创建: {args.code}")


def cmd_watermark(args):
    """给图片注入龍魂 DNA 水印。"""
    from PIL import Image, ImageDraw, ImageFont

    img_path = Path(args.input)
    out_path = Path(args.output) if args.output else OUTPUT_DIR / f"watermarked_{img_path.name}"
    img = Image.open(img_path).convert("RGBA")
    dna = args.dna or generate_dna("WM")

    # 可见水印
    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 24)
    except Exception:
        font = ImageFont.load_default()
    draw.text((20, img.height - 50), f"龍魂 · {dna}", fill=(255, 215, 0, 128), font=font)
    watermarked = Image.alpha_composite(img, txt)
    watermarked.convert("RGB").save(out_path)
    print(f"✅ 水印注入完成: {out_path}")
    print(f"🧬 DNA: {dna}")


def cmd_plan(args):
    """输出工具链安装与使用计划。"""
    plan = """
🐉 龍魂故事工厂 · 开源工具链计划
=====================================
1. 图像生成 + 角色一致性
   推荐: ComfyUI + IPAdapter FaceID Plus V2 / InstantID
   仓库: https://github.com/comfyanonymous/ComfyUI
   角色锁脸: 用角色卡中的 reference image 作为 IPAdapter 输入

2. 视频生成（图生视频）
   轻量: AnimateDiff / Stable Video Diffusion
   进阶: CogVideoX / HunyuanVideo
   仓库: https://github.com/guoyww/AnimateDiff

3. 语音合成 / 声音克隆
   中文首选: GPT-SoVITS (5秒样本即可克隆)
   仓库: https://github.com/RVC-Boss/GPT-SoVITS
   轻量备选: OpenVoice / F5-TTS

4. 水印 / 来源存证
   可见水印: 本模块已内置 (lh_story_factory.py watermark)
   不可见水印: stegano / WatermarkDM
   C2PA 元数据: https://github.com/contentauth/c2pa-python

5. 资产检索
   本模块用 JSON 索引 + 文件系统，一物一码。
   所有资产带 DNA 字段，可追溯。

6. 低算力原则
   - 720p 试播，1080p 定稿，高光镜头单独 4K
   - 角色锚点图生成一次，终身复用
   - 场景首件定调，不逐集重 roll
"""
    print(plan)


def main():
    parser = argparse.ArgumentParser(description="龍魂 · 故事工厂")
    sub = parser.add_subparsers(dest="command")

    p_init = sub.add_parser("init", help="初始化项目")
    p_init.add_argument("project", help="项目名")

    p_char = sub.add_parser("character", help="角色卡管理")
    p_char.add_argument("project", help="项目名")
    p_char.add_argument("action", choices=["create", "list", "show"])
    p_char.add_argument("--code", default="", help="角色编码")
    p_char.add_argument("--name", default="", help="角色名")
    p_char.add_argument("--role", default="", help="角色定位")
    p_char.add_argument("--face", default="", help="脸型锚点")
    p_char.add_argument("--height", default="", help="身高")
    p_char.add_argument("--build", default="", help="体型")
    p_char.add_argument("--age", default="", help="年龄感")
    p_char.add_argument("--mark", default="", help="标志物")
    p_char.add_argument("--costume", default="", help="服装")
    p_char.add_argument("--persona", default="", help="绑定人格编码")
    p_char.add_argument("--seed", default="", help="生成 seed")

    p_asset = sub.add_parser("asset", help="素材货架管理")
    p_asset.add_argument("project", help="项目名")
    p_asset.add_argument("action", choices=["register", "list"])
    p_asset.add_argument("--code", default="", help="素材编码")
    p_asset.add_argument("--category", default="", help="货架分类 A/B/C/D/E/F/G/H/S")
    p_asset.add_argument("--name", default="", help="素材名")
    p_asset.add_argument("--path", default="", help="文件路径")

    p_persona = sub.add_parser("persona", help="人格声线管理")
    p_persona.add_argument("action", choices=["list", "create"])
    p_persona.add_argument("--code", default="", help="人格编码")
    p_persona.add_argument("--type", default="actor", help="类型: actor/director/narrator")
    p_persona.add_argument("--desc", default="", help="描述")
    p_persona.add_argument("--voice", default="", help="声线ID/描述")
    p_persona.add_argument("--style", default="", help="风格参数")

    p_wm = sub.add_parser("watermark", help="注入龍魂水印")
    p_wm.add_argument("--input", required=True, help="输入图片")
    p_wm.add_argument("--output", default="", help="输出图片")
    p_wm.add_argument("--dna", default="", help="指定 DNA")

    p_plan = sub.add_parser("plan", help="输出工具链计划")

    args = parser.parse_args()
    if args.command == "init":
        cmd_init(args)
    elif args.command == "character":
        cmd_character(args)
    elif args.command == "asset":
        cmd_asset(args)
    elif args.command == "persona":
        cmd_persona(args)
    elif args.command == "watermark":
        cmd_watermark(args)
    elif args.command == "plan":
        cmd_plan(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
