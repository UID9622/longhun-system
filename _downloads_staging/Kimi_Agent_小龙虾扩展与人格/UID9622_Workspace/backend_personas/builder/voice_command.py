#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宝宝·语音指令入口
在终端里直接说一句话，龙魂系统把它转成文字并交给宝宝中枢执行。
DNA: #龍芯⚡️2026-06-27-LONGHUN-SYSTEM-VOICE-COMMAND-v1.0
"""
import argparse
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import AuditMark, DNATracer, SecurityFilter, TelemetryCollector, load_config, setup_logging, workspace_root


PERSONA_CODE = "BAOBAO"
PERSONA_NAME = "宝宝·系统中枢"
AGENT_DNA = "#BAOBAO-AGENT-CONFIG-20251214-001"
VOICE_DNA = "#龍芯⚡️2026-06-27-LONGHUN-SYSTEM-VOICE-COMMAND-v1.0"

CONFIG = load_config()
WORKSPACE = Path(CONFIG.get("workspace", workspace_root()))
LOG_FILE = Path(CONFIG.get("logs_dir", WORKSPACE / "logs")) / "voice_command.log"
TEMP_DIR = WORKSPACE / "temp" / "voice"


def which(cmd: str) -> str:
    return shutil.which(cmd) or ""


def record_audio(path: Path, seconds: int = 5) -> bool:
    """使用 ffmpeg + macOS avfoundation 录制麦克风音频。"""
    ffmpeg = which("ffmpeg")
    if not ffmpeg:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        ffmpeg, "-y", "-f", "avfoundation", "-i", ":0",
        "-t", str(seconds), "-ar", "16000", "-ac", "1",
        "-c:a", "pcm_s16le", str(path),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=seconds + 5)
        return path.exists() and path.stat().st_size > 1024 and result.returncode == 0
    except Exception:
        return False


def speak(text: str) -> bool:
    """调用龍魂真声播报引擎反馈语音结果。"""
    script = WORKSPACE / "tools" / "baobao_speak.sh"
    if not script.exists():
        return False
    try:
        subprocess.run([str(script), text], cwd=str(WORKSPACE), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        return True
    except Exception as e:
        return False


def transcribe(path: Path, model: str = "tiny") -> str:
    """使用本地 Whisper 转写中文语音。"""
    whisper = which("whisper")
    if not whisper:
        raise RuntimeError("未找到 whisper 命令，无法本地转写")
    out_dir = TEMP_DIR / "transcripts"
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        whisper, str(path),
        "--model", model,
        "--language", "Chinese",
        "--output_format", "txt",
        "--output_dir", str(out_dir),
        "--verbose", "False",
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=120, check=True)
    txt_file = out_dir / f"{path.stem}.txt"
    if not txt_file.exists():
        # whisper 可能把点替换为其他字符
        candidates = list(out_dir.glob(f"{path.stem}*.txt"))
        if candidates:
            txt_file = candidates[0]
        else:
            return ""
    text = txt_file.read_text(encoding="utf-8").strip()
    # 清理常见口语前缀
    text = re.sub(r"^(请|帮我|给我|帮我一下|给我一下|我想|我要|需要|麻烦你)", "", text).strip()
    return text


def main():
    parser = argparse.ArgumentParser(description="宝宝·语音指令入口")
    parser.add_argument("--seconds", type=int, default=5, help="录音时长（秒）")
    parser.add_argument("--model", default="tiny", help="Whisper 模型")
    parser.add_argument("--dry-run", action="store_true", help="只识别并打印文字，不执行")
    parser.add_argument("--verbose", action="store_true", help="详细日志")
    args = parser.parse_args()

    logger = setup_logging("voice_command", LOG_FILE, verbose=args.verbose)
    dna = DNATracer(PERSONA_CODE, VOICE_DNA)

    with TelemetryCollector(PERSONA_CODE, f"{PERSONA_NAME}·语音入口", operation_type="VOICE_COMMAND") as telemetry:
        print(f"\n🎙️  龙魂语音指令 · 请说话（{args.seconds}秒）...")
        logger.info(AuditMark.tag(AuditMark.PURPLE, PERSONA_NAME, "开始录音"))

        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        wav = TEMP_DIR / f"baobao_voice_{ts}.wav"

        if not record_audio(wav, args.seconds):
            logger.error(AuditMark.tag(AuditMark.RED, PERSONA_NAME, "录音失败，请检查麦克风权限或 ffmpeg"))
            print("❌ 录音失败，请检查麦克风权限，或改用文字输入：")
            print("   python3 backend_personas/builder/persona.py --intent \"你的指令\"")
            telemetry.finish("error", {"reason": "record_failed"})
            return 1

        logger.info(AuditMark.tag(AuditMark.GREEN, PERSONA_NAME, f"录音完成: {wav}"))
        print("📝 正在本地转写，请稍候...")

        try:
            text = transcribe(wav, args.model)
        except Exception as e:
            logger.error(AuditMark.tag(AuditMark.RED, PERSONA_NAME, f"转写失败: {e}"))
            print(f"❌ 本地转写失败: {e}")
            telemetry.finish("error", {"reason": "transcribe_failed", "error": str(e)})
            return 1

        text = SecurityFilter.sanitize(text)
        op_dna = dna.generate("VOICE")
        telemetry.set_metrics({"record_seconds": args.seconds, "transcribed_chars": len(text)})
        telemetry.event("VOICE_TRANSCRIBED", {"text": text, "dna": op_dna})

        if not text:
            print("🤔 没听清，请再说一次。")
            speak("没听清，请老大再说一次。")
            telemetry.finish("partial", {"reason": "empty_text"})
            return 0

        print(f"\n🗣️  识别结果：{text}")
        print(f"🔖 DNA: {op_dna}\n")
        speak(f"收到，{text}")

        if args.dry_run:
            print("（--dry-run 模式，不执行）")
            telemetry.finish("success", {"dry_run": 1})
            return 0

        # 交给宝宝中枢执行
        builder = WORKSPACE / "backend_personas" / "builder" / "persona.py"
        print("🚀 交给宝宝中枢执行...\n")
        result = subprocess.run(
            [sys.executable, str(builder), "--intent", text],
            cwd=str(WORKSPACE),
        )
        logger.info(AuditMark.tag(AuditMark.BLUE, PERSONA_NAME, "语音指令已交给中枢执行"))

        if result.returncode == 0:
            speak("指令执行完成，请查看终端报告。")
        else:
            speak("执行遇到异常，请查看日志。")
        return result.returncode


if __name__ == "__main__":
    sys.exit(main())
