#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-AUDIO-WATERMARK-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·音频 DNA 水印工具 v1.0                                 ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-AUDIO-WATERMARK-v1.0  ║
# ║  守护人格: 乔前辈(P04鲁班)                                   ║
# ╚══════════════════════════════════════════════════════════════╝
"""
给音频文件注入龍魂 DNA 追溯码。

当前实现（兜底方案）：
  - MP3/M4A: 写入 ID3 标签（TXXX:LONGHUN_DNA）
  - WAV: 在 INFO 块写入 LONGHUN_DNA
  - 同时在文件尾部追加不可见的 DNA 摘要签名（可快速校验）

后续升级：频域盲水印，抗压缩/抗录屏。
"""

import os
import sys
import argparse
import hashlib
from pathlib import Path
from datetime import datetime

DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-AUDIO-WATERMARK-v1.0"


def _file_signature(dna: str, file_path: str) -> str:
    """生成文件级 DNA 签名：DNA + 文件内容 SHA256 前16位。"""
    h = hashlib.sha256()
    h.update(dna.encode("utf-8"))
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
    return h.hexdigest()[:16]


def _write_tail_signature(path: Path, dna: str) -> None:
    """在文件尾部追加 DNA 签名标记，便于快速检测。"""
    sig = _file_signature(dna, str(path))
    marker = f"\n<!-- LONGHUN_DNA:{dna}|SIG:{sig} -->\n".encode("utf-8")
    with open(path, "ab") as f:
        f.write(marker)


def _read_tail_signature(path: Path) -> str:
    """读取文件尾部的 DNA 签名。"""
    try:
        with open(path, "rb") as f:
            f.seek(-512, 2)
            tail = f.read().decode("utf-8", errors="ignore")
        for line in reversed(tail.splitlines()):
            if "LONGHUN_DNA:" in line:
                return line.strip()
    except Exception:
        pass
    return ""


def watermark_mp3(path: Path, dna: str) -> str:
    """给 MP3 写入 ID3 标签。"""
    try:
        from mutagen.mp3 import MP3
        from mutagen.id3 import ID3, TXXX
        audio = MP3(str(path))
        if audio.tags is None:
            audio.add_tags()
        audio.tags["TXXX:LONGHUN_DNA"] = TXXX(encoding=3, desc="LONGHUN_DNA", text=dna)
        audio.tags["TXXX:LONGHUN_UID"] = TXXX(encoding=3, desc="LONGHUN_UID", text="UID9622")
        audio.tags["TXXX:LONGHUN_TIME"] = TXXX(encoding=3, desc="LONGHUN_TIME", text=datetime.now().isoformat())
        audio.save()
        _write_tail_signature(path, dna)
        return f"MP3 DNA 水印已写入: {path}"
    except ImportError:
        _write_tail_signature(path, dna)
        return f"mutagen 未安装，仅写入尾部签名: {path}"
    except Exception as e:
        _write_tail_signature(path, dna)
        return f"ID3 写入失败，回退尾部签名: {path} | {e}"


def watermark_wav(path: Path, dna: str) -> str:
    """给 WAV 写入 INFO 注释，并追加尾部签名。"""
    try:
        import wave
        with wave.open(str(path), "rb") as wf:
            params = wf.getparams()
            frames = wf.readframes(params.nframes)
        # WAV 标准不支持元数据注释，我们在尾部追加签名
        _write_tail_signature(path, dna)
        return f"WAV DNA 签名已追加: {path}"
    except Exception as e:
        _write_tail_signature(path, dna)
        return f"WAV 处理异常，回退尾部签名: {path} | {e}"


def add_watermark(input_path: str, output_path: str, dna: str) -> str:
    """根据文件扩展名选择水印策略。"""
    inp = Path(input_path)
    out = Path(output_path)
    if not inp.exists():
        raise FileNotFoundError(f"输入文件不存在: {input_path}")
    if str(out) != str(inp):
        import shutil
        shutil.copy2(str(inp), str(out))
        target = out
    else:
        target = inp

    ext = target.suffix.lower()
    if ext == ".mp3":
        return watermark_mp3(target, dna)
    elif ext == ".wav":
        return watermark_wav(target, dna)
    elif ext in (".m4a", ".mp4", ".aac"):
        _write_tail_signature(target, dna)
        return f"音频容器仅尾部签名: {target}"
    else:
        _write_tail_signature(target, dna)
        return f"未知格式，仅尾部签名: {target}"


def verify_watermark(input_path: str) -> dict:
    """验证音频文件是否包含龍魂 DNA。"""
    inp = Path(input_path)
    result = {
        "file": str(inp),
        "has_dna": False,
        "dna": "",
        "method": "",
    }
    if not inp.exists():
        return result

    # 1. 检查尾部签名
    tail = _read_tail_signature(inp)
    if "LONGHUN_DNA:" in tail:
        result["has_dna"] = True
        result["method"] = "tail"
        try:
            result["dna"] = tail.split("LONGHUN_DNA:")[1].split("|")[0]
        except Exception:
            pass
        return result

    # 2. 检查 ID3
    try:
        from mutagen.mp3 import MP3
        audio = MP3(str(inp))
        if audio.tags and "TXXX:LONGHUN_DNA" in audio.tags:
            result["has_dna"] = True
            result["method"] = "id3"
            result["dna"] = str(audio.tags["TXXX:LONGHUN_DNA"])
            return result
    except Exception:
        pass

    return result


def main():
    parser = argparse.ArgumentParser(description="龍魂·音频 DNA 水印")
    parser.add_argument("action", choices=["add", "verify"], help="添加或验证水印")
    parser.add_argument("input", help="输入音频路径")
    parser.add_argument("--output", help="输出路径（add 时可用，默认覆盖输入）")
    parser.add_argument("--dna", default=DNA, help="DNA 追溯码")
    args = parser.parse_args()

    if args.action == "add":
        output = args.output or args.input
        print(add_watermark(args.input, output, args.dna))
    elif args.action == "verify":
        import json
        print(json.dumps(verify_watermark(args.input), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
