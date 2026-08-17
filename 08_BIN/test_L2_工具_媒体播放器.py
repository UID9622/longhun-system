#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · 全媒体播放器 v1.1 测试
# 层级: L2_工具层
# DNA: #龍芯⚡️丙午·丙申·辛酉·酉时·䷱鼎-MEDIA-PLAYER-TEST-VERIFY-V1.1-P0-b0ef494e
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 通过
"""

import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

# 确保项目根目录在路径中（测试可从 08_BIN/ 直接运行）
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from bin.ganzhi_dna_engine import DNA生成, DNA解析
from bin import lh_media_player as mp


class TestMediaPlayerV11(unittest.TestCase):
    # --------------------------------------------------------
    # 1. DNA 生成格式
    # --------------------------------------------------------
    def test_dna_format(self):
        dna = DNA生成(
            模块="MEDIA-PLAYER",
            动作="TEST",
            版本="V1.1",
            级别="P0",
            内容锚点="media-player-unit-test",
        )
        self.assertTrue(dna.startswith("#龍芯⚡️"))
        parsed = DNA解析(dna)
        self.assertTrue(parsed["有效"], f"DNA 解析失败: {dna}")
        self.assertEqual(len(parsed["哈希8"]), 8)
        self.assertRegex(dna, r"#龍芯⚡️[^·]+·[^·]+·[^·]+·[^·]+·[^-]+-.+-[a-f0-9]{8}$")

    # --------------------------------------------------------
    # 2. argparse 命令行解析
    # --------------------------------------------------------
    def test_argparse_process(self):
        parser = mp.build_parser()
        args = parser.parse_args(["process", "demo.mp4", "--interval", "3", "--force", "--verbose"])
        self.assertEqual(args.command, "process")
        self.assertEqual(args.video, Path("demo.mp4"))
        self.assertEqual(args.interval, 3.0)
        self.assertTrue(args.force)
        self.assertTrue(args.verbose)

    def test_argparse_asr(self):
        parser = mp.build_parser()
        args = parser.parse_args(["asr", "~/Movies/a.mp4", "--model-size", "small", "--language", "en"])
        self.assertEqual(args.command, "asr")
        self.assertEqual(args.model_size, "small")
        self.assertEqual(args.language, "en")
        self.assertFalse(args.force)

    def test_argparse_batch(self):
        parser = mp.build_parser()
        args = parser.parse_args(["batch", "/data/videos", "--output-dir", "/tmp/out"])
        self.assertEqual(args.command, "batch")
        self.assertEqual(args.directory, Path("/data/videos"))
        self.assertEqual(args.output_dir, Path("/tmp/out"))

    def test_argparse_status(self):
        parser = mp.build_parser()
        args = parser.parse_args(["status"])
        self.assertEqual(args.command, "status")

    # --------------------------------------------------------
    # 3. WebVTT 生成
    # --------------------------------------------------------
    def test_generate_vtt(self):
        segments = [
            {"start": 1.0, "end": 4.0, "text": "第一段"},
            {"start": 5.5, "end": 8.2, "text": "第二段"},
        ]
        vtt = mp.generate_vtt(segments, duration=10.0)
        self.assertIn("WEBVTT", vtt)
        self.assertIn("00:00:01.000 --> 00:00:04.000", vtt)
        self.assertIn("00:00:05.500 --> 00:00:08.200", vtt)
        self.assertIn("第一段", vtt)
        self.assertIn("第二段", vtt)

    def test_generate_vtt_clamps_to_duration(self):
        segments = [{"start": 2.0, "end": 15.0, "text": "超出"}]
        vtt = mp.generate_vtt(segments, duration=10.0)
        self.assertIn("00:00:02.000 --> 00:00:10.000", vtt)

    # --------------------------------------------------------
    # 4. OCR 去重与跳过无文字帧
    # --------------------------------------------------------
    def test_filter_ocr_results(self):
        raw = [
            {"time": 0.0, "text": "龍魂"},
            {"time": 5.0, "text": "龍魂"},          # 连续重复 → 去重
            {"time": 10.0, "text": "[画面未识别到文字]"},  # 无文字 → 跳过
            {"time": 15.0, "text": "媒体播放器"},
            {"time": 20.0, "text": "龍魂"},          # 与上一条不同，保留
        ]
        filtered = mp.filter_ocr_results(raw)
        self.assertEqual(len(filtered), 3)
        self.assertEqual([r["text"] for r in filtered], ["龍魂", "媒体播放器", "龍魂"])

    # --------------------------------------------------------
    # 5. 配置加载
    # --------------------------------------------------------
    def test_load_config_defaults(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{}")
            path = Path(f.name)
        try:
            cfg = mp.load_config(path)
            self.assertEqual(cfg["player"], mp.DEFAULT_CONFIG["player"])
            self.assertEqual(cfg["interval"], 5.0)
            self.assertEqual(cfg["model_size"], "base")
            self.assertEqual(cfg["language"], "zh")
        finally:
            path.unlink()

    def test_load_config_merge(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"player": "mpv", "interval": 2.0, "model_size": "small"}, f)
            path = Path(f.name)
        try:
            cfg = mp.load_config(path)
            self.assertEqual(cfg["player"], "mpv")
            self.assertEqual(cfg["interval"], 2.0)
            self.assertEqual(cfg["model_size"], "small")
            self.assertEqual(cfg["language"], "zh")  # 默认值保留
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main(verbosity=2)
