#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂视频引擎 · 主编排器 v1.1
DNA: #龍芯⚡️2026-08-22-VIDEO-ENGINE-MAIN-v1.1
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
用法:
  python3 engine.py --script narration.txt --output my_video
  python3 engine.py --script narration.txt --output my_video --subtitle word --wav2lip_dir ~/Wav2Lip
修复记录 v1.1: 角色默认表情"认主"→"讲解"(与设计一致)·空解说稿保护·md5→sha256
"""

import argparse, json, hashlib, time, sys
from pathlib import Path
from datetime import datetime
from typing import Optional

from script_parser      import ScriptParser
from character_registry import CharacterRegistry, BEICHEN_PROFILE
from tts_pipeline       import TtsPipeline
from visual_track       import VisualTrack
from lip_sync           import LipSync
from subtitle_gen       import SubtitleGen
from timeline_composer  import TimelineComposer

BASE = Path.home() / "longhun-system" / "lh_video_engine"

class LhVideoEngine:
    """
    龍魂视频引擎 · 主编排器
    一次调用，不需调试
    """

    def __init__(self, output_name: str = "output",
                 wav2lip_dir: Optional[str] = None):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_dir  = BASE / "output" / f"{output_name}_{ts}"
        self.run_dir.mkdir(parents=True, exist_ok=True)

        # 初始化各模块
        self.char_reg   = CharacterRegistry(BASE / "characters")
        self.tts        = TtsPipeline(str(self.run_dir / "audio"))
        self.visual     = VisualTrack(
            str(self.run_dir / "frames"),
            str(self.run_dir / "videos"))
        self.lip        = LipSync(wav2lip_dir)
        self.composer   = TimelineComposer(str(self.run_dir / "final"))

        # 确保默认角色已注册
        if not self.char_reg.load("beichen"):
            self.char_reg.register(BEICHEN_PROFILE)

    def run(self, script: str,
            subtitle_mode: str = "sentence",
            output_name:   str = "final_output") -> str:
        """
        主流程: 解说稿 → 最终视频
        """
        ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        h  = hashlib.sha256(script[:50].encode()).hexdigest()[:8].upper()
        dna = f"#龍芯⚡️{ts}-ENGINE-RUN-{h}"
        print(f"龍魂视频引擎启动 | DNA: {dna}")
        print(f"输出目录: {self.run_dir}")

        # ① 剧本解析
        print("\n① 剧本解析...")
        timeline = ScriptParser.parse(script)
        (self.run_dir / "timeline.json").write_text(
            json.dumps(timeline, ensure_ascii=False, indent=2), "utf-8")
        segments = timeline["segments"]
        print(f"   共 {len(segments)} 个镜头 | 预估时长 {timeline['total_duration']:.1f}s")
        if not segments:
            raise ValueError("解说稿为空或无可识别句子")

        # ② TTS 全部 Segment
        print("\n② TTS 语音生成...")
        tts_results = self.tts.process_all(segments)

        # 计算时间轴偏移
        offsets = [0.0]
        for r in tts_results[:-1]:
            offsets.append(offsets[-1] + r["duration"])

        # ③ 字幕生成（.ass 外挂 + PNG 烧录两路）
        print("\n③ 字幕生成...")
        sub_dir = self.run_dir / "subtitles"
        sub_dir.mkdir(parents=True, exist_ok=True)
        sub_path = str(sub_dir / "subs.ass")
        SubtitleGen.generate_ass(tts_results, offsets, sub_path, subtitle_mode)
        sub_images = SubtitleGen.render_subtitle_pngs(
            tts_results, offsets, str(sub_dir), subtitle_mode)

        # ④ 画面轨道
        print("\n④ 画面轨道生成...")
        visual_videos = []
        for idx, (seg, tts_r) in enumerate(zip(segments, tts_results)):
            # 角色镜头赋予生成配置（Seed 随镜头索引抖动·保持不动点）
            char_cfg = None
            if seg.get("character"):
                char_cfg = self.char_reg.build_generation_config(
                    seg["character"],
                    expression=seg.get("expression", "讲解"),
                    shot_index=idx
                )
            vpath = self.visual.process_segment(seg, tts_r, char_cfg)
            visual_videos.append(vpath)

        # ⑤ 口型同步
        print("\n⑤ 口型同步...")
        final_videos = []
        for seg, tts_r, vpath in zip(segments, tts_results, visual_videos):
            lpath = str(Path(vpath).parent /
                        (Path(vpath).stem + "_lipsync.mp4"))
            out = self.lip.process_segment(seg, tts_r, vpath, lpath)
            final_videos.append(out)

        # ⑥ 对齐合成（字幕走 PNG overlay 烧录）
        print("\n⑥ 时间轴对齐合成...")
        final = self.composer.compose(
            tts_results, final_videos, sub_images, offsets, output_name)

        # 写入审计日志
        audit = {
            "dna":            dna,
            "timestamp":      datetime.now().isoformat(),
            "output":         final,
            "segments":       len(segments),
            "tri_color":      "🟢",
            "total_duration": sum(r["duration"] for r in tts_results),
        }
        (self.run_dir / "audit.json").write_text(
            json.dumps(audit, ensure_ascii=False, indent=2), "utf-8")
        print(f"\n🟢 审计记录→ {self.run_dir}/audit.json")
        return final

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="龍魂视频引擎 v1.0")
    parser.add_argument("--script",      required=True,  help="解说稿文本文件")
    parser.add_argument("--output",      default="output", help="输出文件名")
    parser.add_argument("--subtitle",    default="sentence",
                        choices=["sentence", "word"], help="字幕模式")
    parser.add_argument("--wav2lip_dir", default=None,    help="Wav2Lip 目录")
    args = parser.parse_args()

    script_text = open(args.script, "r", encoding="utf-8").read()
    engine = LhVideoEngine(output_name=args.output,
                           wav2lip_dir=args.wav2lip_dir)
    result = engine.run(script_text,
                        subtitle_mode=args.subtitle,
                        output_name=args.output)
    print(f"\n🎬 完成！视频已生成: {result}")
