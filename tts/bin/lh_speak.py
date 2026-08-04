#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🗣️ 龍魂 TTS 主控引擎 v1.0

DNA: #龍芯⚡️丙午·乙未·己卯·巳时·☰乾-TTS-SPEAK-v1.0-c1d2e3f4
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

架构:
  GPT-SoVITS API (:9880) → 原始语音 → DNA水印嵌入 → 最终音频

底座: GPT-SoVITS v2 (MIT License · 真正免费开源)
人格: 16人格声音映射表 (tts/voices/persona_voices.json)

用法:
  python3 tts/bin/lh_speak.py --persona P00 --text "数据主权在人民手里"
  python3 tts/bin/lh_speak.py --persona P11 --text "这个方案气势磅礴！" --no-watermark
  python3 tts/bin/lh_speak.py --list  # 列出所有人格
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

CST = timezone(timedelta(hours=8))

# 路径
BASE_DIR = Path(__file__).resolve().parent.parent  # tts/
VOICES_CONFIG = BASE_DIR / "voices" / "persona_voices.json"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# GPT-SoVITS API
SOVITS_API = os.environ.get("SOVITS_API", "http://127.0.0.1:9880")

# DNA水印脚本
WATERMARK_SCRIPT = BASE_DIR / "bin" / "lh_dna_watermark.py"


def load_personas() -> dict:
    with open(VOICES_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_dna(persona_id: str, text: str) -> str:
    """生成DNA追溯码"""
    now = datetime.now(CST)
    text_hash = hashlib.sha256(text.encode()).hexdigest()[:8]
    return f"#龍芯⚡️{now.strftime('%Y%m%d-%H%M%S')}-TTS-{persona_id}-{text_hash}"


def call_sovits_api(config: dict, text: str) -> bytes:
    """
    调用 GPT-SoVITS API 生成语音
    
    Args:
        config: 人格配置
        text: 合成文本
    
    Returns:
        原始音频字节 (WAV)
    """
    payload = {
        "text": text,
        "text_lang": "zh",
        "ref_audio_path": str(Path(config["ref_audio_path"]).resolve()),
        "prompt_text": config["prompt_text"],
        "prompt_lang": config["prompt_lang"],
        "temperature": config.get("temperature", 0.8),
        "top_k": config.get("top_k", 15),
        "top_p": config.get("top_p", 0.9),
        "speed_factor": config.get("speed_factor", 1.0),
        "seed": config.get("seed", 9622),
        "text_split_method": "cut5",
        "batch_size": 1,
        "streaming_mode": False,
    }
    
    req = urllib.request.Request(
        f"{SOVITS_API}/tts",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            if resp.status == 200:
                return resp.read()
            else:
                error = json.loads(resp.read())
                raise RuntimeError(f"GPT-SoVITS API 错误: {error}")
    except urllib.error.URLError as e:
        raise ConnectionError(
            f"❌ 无法连接 GPT-SoVITS API ({SOVITS_API})\n"
            f"   请先启动: cd engines/gpt_sovits && .venv_gpt_sovits/bin/python api_v2.py -a 0.0.0.0 -p 9880"
        ) from e


def speak(persona_id: str, text: str, watermark: bool = True,
          output_path: str = "", verbose: bool = False) -> str:
    """
    人格语音合成
    
    Args:
        persona_id: 人格ID (P00-P72)
        text: 合成文本
        watermark: 是否嵌入DNA水印
        output_path: 输出路径（默认自动生成）
        verbose: 详细输出
    
    Returns:
        输出文件路径
    """
    data = load_personas()
    personas = data["personas"]
    
    if persona_id not in personas:
        available = ", ".join(personas.keys())
        raise ValueError(f"未知人格: {persona_id}\n可用: {available}")
    
    config = personas[persona_id]
    dna = generate_dna(persona_id, text)
    
    if verbose:
        print(f"🎙️ 人格: {config['name']} ({persona_id})")
        print(f"🎭 情绪: {config['emotion']}")
        print(f"📝 文本: {text[:60]}{'...' if len(text) > 60 else ''}")
        print(f"🧬 DNA: {dna}")
        print(f"⏳ 调用 GPT-SoVITS...")
    
    # Step 1: 调用 GPT-SoVITS 生成原始语音
    raw_audio = call_sovits_api(config, text)
    
    # Step 2: 保存原始音频
    timestamp = datetime.now(CST).strftime("%Y%m%d_%H%M%S")
    raw_path = str(OUTPUT_DIR / f"{persona_id}_{timestamp}_raw.wav")
    with open(raw_path, "wb") as f:
        f.write(raw_audio)
    
    if verbose:
        print(f"📁 原始: {raw_path} ({len(raw_audio)} bytes)")
    
    # Step 3: 嵌入DNA水印
    if watermark:
        final_path = output_path or str(OUTPUT_DIR / f"{persona_id}_{timestamp}.wav")
        
        # 用 subprocess 调用水印脚本
        cmd = [
            sys.executable, str(WATERMARK_SCRIPT), "embed",
            "--input", raw_path,
            "--dna", dna,
            "--persona", persona_id,
            "--output", final_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"⚠️ 水印嵌入失败，使用原始文件: {result.stderr}")
            final_path = raw_path
        else:
            if verbose:
                print(result.stdout.strip())
            # 清理原始文件
            os.remove(raw_path)
    else:
        final_path = raw_path
    
    if verbose:
        file_size = os.path.getsize(final_path)
        print(f"\n✅ 完成: {final_path} ({file_size/1024:.1f} KB)")
    
    return final_path


def list_personas():
    """列出所有人格"""
    data = load_personas()
    print(f"\n🧬 龍魂TTS · {data['_meta']['engine']}")
    print(f"   底座: {data['_meta']['engine']}")
    print(f"   参考音: {data['_meta']['reference_audio']}")
    print(f"\n{'ID':<12} {'名称':<16} {'层级':<6} {'情绪':<12} {'语速':<6} {'温度':<6}")
    print("-" * 72)
    
    for pid, cfg in data["personas"].items():
        print(
            f"{pid:<12} {cfg['name']:<16} {cfg['layer']:<6} "
            f"{cfg['emotion']:<12} {cfg['speed_factor']:<6.2f} {cfg['temperature']:<6.2f}"
        )
    
    print(f"\n共 {len(data['personas'])} 个人格\n")


def health_check() -> dict:
    """检查 GPT-SoVITS 服务状态"""
    status = {"api": SOVITS_API, "connected": False, "personas": 0}
    
    try:
        req = urllib.request.Request(f"{SOVITS_API}/control", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            status["connected"] = resp.status == 200
    except Exception:
        pass
    
    if status["connected"]:
        data = load_personas()
        status["personas"] = len(data["personas"])
    
    return status


def main():
    parser = argparse.ArgumentParser(
        description="🗣️ 龍魂 TTS 主控引擎 v1.0 · GPT-SoVITS 底座",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --persona P00 --text "数据主权在人民手里"
  %(prog)s --persona P11 --text "这个方案气势磅礴！"
  %(prog)s --persona P72 --text "检测到威胁，立即熔断！"
  %(prog)s --list
  %(prog)s --health
        """
    )
    parser.add_argument("--persona", default="", help="人格ID (P00-P72)")
    parser.add_argument("--text", default="", help="合成文本")
    parser.add_argument("--no-watermark", action="store_true", help="禁用DNA水印")
    parser.add_argument("--output", default="", help="输出路径")
    parser.add_argument("--list", action="store_true", help="列出所有人格")
    parser.add_argument("--health", action="store_true", help="检查服务状态")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    if args.list:
        list_personas()
        return
    
    if args.health:
        status = health_check()
        print(f"API: {status['api']}")
        print(f"连接: {'🟢' if status['connected'] else '🔴'}")
        if status["connected"]:
            print(f"可用人格: {status['personas']}")
        else:
            print("❌ GPT-SoVITS 未启动")
            print("   启动命令: cd engines/gpt_sovits && .venv_gpt_sovits/bin/python api_v2.py -a 0.0.0.0 -p 9880")
        return
    
    if not args.persona or not args.text:
        parser.print_help()
        return
    
    try:
        result = speak(
            persona_id=args.persona,
            text=args.text,
            watermark=not args.no_watermark,
            output_path=args.output,
            verbose=args.verbose or True,
        )
        print(f"\n📁 {result}")
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
