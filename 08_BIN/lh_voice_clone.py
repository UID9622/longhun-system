# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-ac48a48e
#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · XTTS v2 真声克隆引擎
============================
基于 Coqui TTS XTTS v2，用 UID9622 真人声音样本（31分钟口语）克隆的数字人语音引擎。

DNA: #龍芯⚡️丙午-乙巳-2026-07-29-VOICE-CLONE-ENGINE-v2.0-合成
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

用法:
  python3 bin/lh_voice_clone.py "要合成的话" --output output.wav
  python3 bin/lh_voice_clone.py --script 解说稿.txt --output-dir audio/
  python3 bin/lh_voice_clone.py --test
  python3 bin/lh_voice_clone.py --server  # 启动HTTP API (端口 9623)

环境:
  首次运行前执行: bash bin/lh_voice_clone_setup.sh
  XTTS v2 模型首次加载自动下载到 ~/.local/share/tts/
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

# ---- 常量 ----
PROJECT_ROOT = Path(__file__).resolve().parent.parent
VENV_PYTHON = PROJECT_ROOT / ".venv_tts" / "bin" / "python3"
REFERENCE_WAV = PROJECT_ROOT / "docs" / "reference_optimized.wav"
VOICE_TWIN_DIR = PROJECT_ROOT / "voices" / "voice_twin_v1"
TTS_OUTPUT_DIR = VOICE_TWIN_DIR / "tts_outputs"
STYLE_PROFILE = VOICE_TWIN_DIR / "style_profile.json"

TTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# UID9622 声音特征（从 style_profile.json + 实机测试提取）
VOICE_PROFILE = {
    "name": "UID9622·诸葛鑫",
    "engine": "xtts-v2",
    "reference_wav": str(REFERENCE_WAV),
    "language": "zh",
    "speaker": "uid9622",
    "style": {
        "pitch": "medium-low",        # 退伍军人·沉稳有力
        "speed": "1.0",                # 正常语速
        "emotion": "firm",             # 坚定
        "energy": 0.72,                # 中高强度
        "clarity": "clean",            # 干净利落
    },
    "catchphrases": ["是不是", "对不对", "嘛", "对吧", "就问你"],
    "ideal_for": [
        "视频解说·龍魂系统介绍",
        "知识科普·芯片/密码学/CNSH",
        "战术分析·战友对话风格",
        "技术教程·干净有力不啰嗦",
    ]
}


def _xtts_generate_in_venv(text: str, output_path: str, language: str = "zh") -> dict:
    """在 .venv_tts 中调用 XTTS v2 合成语音。"""
    if not VENV_PYTHON.exists():
        raise RuntimeError(
            f"XTTS venv 未安装: {VENV_PYTHON}\n"
            f"请先运行: bash bin/lh_voice_clone_setup.sh"
        )

    if not REFERENCE_WAV.exists():
        raise FileNotFoundError(f"参考音频不存在: {REFERENCE_WAV}")

    code = f"""
import os, sys, json
os.environ['COQUI_TOS_AGREED'] = '1'
from pathlib import Path
from TTS.api import TTS

ref = Path('{REFERENCE_WAV}')
out = Path('{output_path}')
out.parent.mkdir(parents=True, exist_ok=True)

tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2', gpu=False)
tts.tts_to_file(
    text='''{text}''',
    speaker_wav=str(ref),
    language='{language}',
    file_path=str(out)
)
print(json.dumps({{"status": "ok", "path": str(out), "size": out.stat().st_size}}))
"""

    result = subprocess.run(
        [str(VENV_PYTHON), "-u", "-c", code],  # -u 无缓冲输出
        capture_output=True, text=True,
        timeout=600,  # 10分钟超时（首次加载模型+合成需要时间）
        cwd=str(PROJECT_ROOT),
        env={**os.environ, "PYTHONUNBUFFERED": "1"},
    )

    if result.returncode != 0:
        stderr = result.stderr[-500:] if len(result.stderr) > 500 else result.stderr
        raise RuntimeError(f"XTTS 合成失败:\n{stderr}")

    # 解析输出
    for line in result.stdout.strip().split("\n"):
        if line.startswith("{"):
            return json.loads(line)

    return {"status": "ok", "path": output_path}


def generate(text: str, output: str = None, language: str = "zh") -> str:
    """
    合成单条语音。

    Args:
        text: 要合成的文本
        output: 输出文件路径（默认自动生成到 tts_outputs/）
        language: 语言代码 (zh/en)

    Returns:
        输出 WAV 文件路径
    """
    if output is None:
        timestamp = int(time.time())
        safe_name = text[:30].replace(" ", "_").replace("/", "_")
        output = str(TTS_OUTPUT_DIR / f"tts_xtts_{safe_name}_{timestamp}.wav")

    print(f"🎙️ UID9622 真声合成中...")
    print(f"   文本: {text[:60]}{'...' if len(text) > 60 else ''}")

    result = _xtts_generate_in_venv(text, output, language)
    size_kb = Path(output).stat().st_size / 1024 if Path(output).exists() else 0

    print(f"✅ 语音: {output} ({size_kb:.1f} KB)")
    return output


def generate_batch(script_file: str, output_dir: str = None, language: str = "zh") -> list:
    """
    批量合成脚本（每行一段）。

    Args:
        script_file: 解说稿文本文件（每行一段）
        output_dir: 输出目录
        language: 语言代码

    Returns:
        [(text, wav_path), ...]
    """
    script_path = Path(script_file)
    if not script_path.exists():
        raise FileNotFoundError(f"脚本不存在: {script_file}")

    out_dir = Path(output_dir) if output_dir else TTS_OUTPUT_DIR / f"batch_{script_path.stem}"
    out_dir.mkdir(parents=True, exist_ok=True)

    lines = []
    with open(script_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                lines.append(line)

    results = []
    total = len(lines)
    print(f"🎙️ 批量合成 {total} 段...")
    print(f"   参考语音: UID9622·诸葛鑫")

    for i, line in enumerate(lines, 1):
        out_path = str(out_dir / f"segment_{i:03d}.wav")
        try:
            generate(line, out_path, language)
            results.append((line, out_path))
            print(f"   [{i}/{total}] ✅")
        except Exception as e:
            print(f"   [{i}/{total}] ❌ {e}")
            results.append((line, None))

    success = sum(1 for _, p in results if p)
    print(f"\n✅ 完成: {success}/{total} 段")
    return results


def test():
    """生成测试语音，验证声音克隆效果。"""
    test_texts = [
        "你好，我是龍魂系统数字人。就问一句：AI是不是属于每一个人？",
        "说真的，写代码这么多年，我受够了。受够了那些动不动就说'技术无国界'的话。",
        "老子不跪。代码也不跪。龍魂系统，中国自主。",
        "我这里没有既要开源又要跪着求打赏那一套。代码写出来，大家直接用。",
    ]

    print("=" * 50)
    print("  龍魂 XTTS v2 · UID9622 真声克隆测试")
    print("=" * 50)
    print()

    for i, text in enumerate(test_texts, 1):
        out = str(TTS_OUTPUT_DIR / f"test_clone_{i:02d}.wav")
        if Path(out).exists():
            print(f"[{i}] ✅ 已存在: {out}")
            continue
        try:
            generate(text, out)
        except Exception as e:
            print(f"[{i}] ❌ 失败: {e}")

    print()
    print(f"📁 测试音频: {TTS_OUTPUT_DIR}/")
    print(f"   播放: afplay {TTS_OUTPUT_DIR}/test_clone_01.wav")
    return True


def server(host: str = "127.0.0.1", port: int = 9623):
    """启动 HTTP TTS API 服务。"""
    try:
        from fastapi import FastAPI
        from fastapi.responses import FileResponse
        import uvicorn
    except ImportError:
        print("需要安装: pip install fastapi uvicorn")
        return False

    app = FastAPI(title="龍魂 XTTS v2 · UID9622 真声 TTS API", version="2.0")

    @app.get("/health")
    async def health():
        return {"status": "ok", "voice": "uid9622-xtts-v2", "engine": "XTTS v2"}

    @app.post("/tts")
    async def tts(text: str, language: str = "zh"):
        out_path = str(TTS_OUTPUT_DIR / f"api_{int(time.time())}.wav")
        generate(text, out_path, language)
        return FileResponse(out_path, media_type="audio/wav")

    print(f"🎙️ UID9622 真声 TTS API: http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)


def info():
    """打印声音克隆系统信息。"""
    print(json.dumps(VOICE_PROFILE, ensure_ascii=False, indent=2))
    print()
    print(f"📁 参考音频: {REFERENCE_WAV} (存在: {REFERENCE_WAV.exists()})")
    print(f"📁 TTS输出:  {TTS_OUTPUT_DIR}")
    print(f"📁 环境Python: {VENV_PYTHON} (存在: {VENV_PYTHON.exists()})")


# ---- CLI ----
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="龍魂 XTTS v2 · UID9622 真声克隆引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_voice_clone.py "你好" --output test.wav
  python3 bin/lh_voice_clone.py --test
  python3 bin/lh_voice_clone.py --script 解说稿.txt
  python3 bin/lh_voice_clone.py --info
        """
    )
    parser.add_argument("text", nargs="?", help="要合成的文本")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--script", "-s", help="批量合成脚本文件")
    parser.add_argument("--output-dir", "-d", help="批量输出目录")
    parser.add_argument("--test", action="store_true", help="运行克隆效果测试")
    parser.add_argument("--server", action="store_true", help="启动 HTTP TTS API")
    parser.add_argument("--info", action="store_true", help="打印系统信息")
    parser.add_argument("--port", type=int, default=9623, help="API 端口 (默认 9623)")

    args = parser.parse_args()

    try:
        if args.test:
            test()
        elif args.server:
            server(port=args.port)
        elif args.info:
            info()
        elif args.script:
            generate_batch(args.script, args.output_dir)
        elif args.text:
            generate(args.text, args.output)
        else:
            parser.print_help()
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
