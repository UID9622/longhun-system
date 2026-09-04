#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 批量处理引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-BATCH-PROCESS-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  1. 批量视频水印嵌入 (可见/不可见/二维码)
  2. 批量印记生成 (从CSV/JSON导入)
  3. 批量声纹提取

用法：
  lh batch --mode watermark --input-dir ./videos/ --output-dir ./output/
  lh batch --mode imprint --csv data.csv
  lh batch --mode voiceprint --input-dir ./audio/
"""

import os
import sys
import json
import csv
import hashlib
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict
from datetime import datetime

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


class BatchProcessor:
    """批量处理调度器"""
    
    def __init__(self, input_dir: Path = None, output_dir: Path = None, log_file: Path = None):
        self.input_dir = input_dir
        self.output_dir = output_dir or Path.cwd() / "batch_output"
        self.log_file = log_file or self.output_dir / "batch.log"
        if self.output_dir:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = []
        self.errors = 0
        self.successes = 0

    def log(self, message: str):
        """写日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        print(entry, flush=True)
        if self.log_file.parent.exists():
            with open(self.log_file, 'a') as f:
                f.write(entry + "\n")

    def _run_script(self, script_name: str, args: List[str], timeout: int = 300) -> Dict:
        """运行单个脚本"""
        script_path = Path(__file__).resolve().parent / script_name
        cmd = [sys.executable, str(script_path)] + args
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return {
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip()[:500],
            }
        except subprocess.TimeoutExpired:
            return {"returncode": -1, "stdout": "", "stderr": f"超时 ({timeout}s)"}
        except Exception as e:
            return {"returncode": -1, "stdout": "", "stderr": str(e)}

    def process_watermark(self, mode: str = "visible") -> List[Dict]:
        """批量水印嵌入"""
        if not self.input_dir or not self.input_dir.exists():
            self.log(f"❌ 输入目录不存在: {self.input_dir}")
            return []

        video_exts = [".mp4", ".mov", ".avi", ".mkv"]
        videos = [f for f in self.input_dir.iterdir() if f.suffix.lower() in video_exts]
        self.log(f"📹 找到 {len(videos)} 个视频文件")

        script_map = {
            "visible": "lh_video_watermark.py",
            "invisible": "lh_dct_watermark.py",
            "qr": "lh_qr_code.py",
        }
        script = script_map.get(mode)
        if not script:
            self.log(f"❌ 未知水印模式: {mode} (可选: visible/invisible/qr)")
            return []

        for idx, video in enumerate(videos):
            dna = f"#龍芯⚡️BATCH-{hashlib.sha256(str(video).encode()).hexdigest()[:12]}"
            output = self.output_dir / f"{video.stem}_{mode}.mp4"

            self.log(f"[{idx+1}/{len(videos)}] {video.name} ...")

            if mode == "qr":
                args = ["embed", "--video", str(video), "--output", str(output), "--dna", dna]
            else:
                args = ["--video", str(video), "--output", str(output), "--dna", dna]

            run_result = self._run_script(script, args)
            entry = {
                "index": idx + 1,
                "video": str(video.name),
                "output": str(output.name),
                "dna": dna,
                "mode": mode,
            }

            if run_result["returncode"] == 0:
                self.successes += 1
                entry["status"] = "success"
                self.log(f"  ✅ {video.name}")
            else:
                self.errors += 1
                entry["status"] = "error"
                entry["error"] = run_result["stderr"][:200]
                self.log(f"  ❌ {video.name}: {run_result['stderr'][:100]}")

            self.results.append(entry)

        self.log(f"🏁 完成: {self.successes}成功 / {self.errors}失败 / {len(videos)}总计")
        return self.results

    def process_imprint_from_csv(self, csv_path: Path) -> List[Dict]:
        """从CSV批量生成印记"""
        if not csv_path.exists():
            self.log(f"❌ CSV文件不存在: {csv_path}")
            return []

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except Exception as e:
            self.log(f"❌ CSV读取失败: {e}")
            return []

        self.log(f"📋 CSV加载 {len(rows)} 行")

        for idx, row in enumerate(rows):
            name = row.get("name", "").strip()
            ipa = row.get("ipa", "").strip()
            face = row.get("face", "").strip()
            voice = row.get("voice", "").strip()

            if not name or not ipa:
                self.log(f"⚠️ [{idx+1}] 跳过空行: name={name} ipa={ipa}")
                continue

            args = ["create", "--name", name, "--ipa", ipa]
            if face:
                args.extend(["--face", face])
            if voice:
                args.extend(["--voice", voice])

            self.log(f"[{idx+1}/{len(rows)}] 创建印记: {ipa} ({name})")
            run_result = self._run_script("lh_digital_imprint.py", args, timeout=60)

            entry = {"ipa": ipa, "name": name, "index": idx + 1}
            if run_result["returncode"] == 0:
                self.successes += 1
                entry["status"] = "success"
                # 尝试解析输出的DNA
                try:
                    out_data = json.loads(run_result["stdout"])
                    entry["dna"] = out_data.get("dna", "")
                except json.JSONDecodeError:
                    pass
                self.log(f"  ✅ {ipa}")
            else:
                self.errors += 1
                entry["status"] = "error"
                entry["error"] = run_result["stderr"][:200]
                self.log(f"  ❌ {ipa}: {run_result['stderr'][:100]}")

            self.results.append(entry)

        self.log(f"🏁 印记批量完成: {self.successes}成功 / {self.errors}失败")
        return self.results

    def process_voiceprint(self) -> List[Dict]:
        """批量声纹提取"""
        if not self.input_dir or not self.input_dir.exists():
            self.log(f"❌ 输入目录不存在: {self.input_dir}")
            return []

        audio_exts = [".wav", ".mp3", ".m4a", ".flac", ".ogg"]
        audios = [f for f in self.input_dir.iterdir() if f.suffix.lower() in audio_exts]
        self.log(f"🎵 找到 {len(audios)} 个音频文件")

        for idx, audio in enumerate(audios):
            name = audio.stem
            self.log(f"[{idx+1}/{len(audios)}] 注册声纹: {name}")
            result = self._run_script("lh_voice_register.py", 
                                      ["register", "--audio", str(audio), "--name", name],
                                      timeout=60)
            entry = {"name": name, "audio": str(audio.name), "index": idx + 1}
            if result["returncode"] == 0:
                self.successes += 1
                entry["status"] = "success"
                self.log(f"  ✅ {name}")
            else:
                self.errors += 1
                entry["status"] = "error"
                entry["error"] = result["stderr"][:200]
                self.log(f"  ❌ {name}: {result['stderr'][:100]}")

            self.results.append(entry)

        self.log(f"🏁 声纹批量完成: {self.successes}成功 / {self.errors}失败")
        return self.results

    def summary(self) -> Dict:
        return {
            "total": len(self.results),
            "successes": self.successes,
            "errors": self.errors,
            "success_rate": f"{self.successes/max(len(self.results),1)*100:.1f}%",
            "log_file": str(self.log_file),
            "output_dir": str(self.output_dir),
        }


def main():
    parser = argparse.ArgumentParser(description="龍魂 · 批量处理引擎")
    parser.add_argument("--mode", required=True,
                        choices=["watermark", "imprint", "voiceprint"],
                        help="处理模式")
    parser.add_argument("--input-dir", type=Path, help="输入目录 (watermark/voiceprint模式)")
    parser.add_argument("--output-dir", type=Path, help="输出目录")
    parser.add_argument("--csv", type=Path, help="CSV文件路径 (imprint模式)")
    parser.add_argument("--watermark-type", default="visible",
                        choices=["visible", "invisible", "qr"],
                        help="水印类型 (默认visible)")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    processor = BatchProcessor(
        input_dir=args.input_dir,
        output_dir=args.output_dir
    )

    if args.mode == "watermark":
        if not args.input_dir or not args.output_dir:
            print("错误：watermark模式需要 --input-dir 和 --output-dir")
            sys.exit(1)
        processor.process_watermark(args.watermark_type)

    elif args.mode == "imprint":
        if not args.csv:
            print("错误：imprint模式需要 --csv")
            sys.exit(1)
        processor.process_imprint_from_csv(args.csv)

    elif args.mode == "voiceprint":
        if not args.input_dir:
            print("错误：voiceprint模式需要 --input-dir")
            sys.exit(1)
        processor.process_voiceprint()

    summary = processor.summary()
    if args.json:
        print(json.dumps({
            "summary": summary,
            "results": processor.results
        }, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
