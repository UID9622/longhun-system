#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·明夷-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""Voice generation service using Fish Audio UID9622 voice clone / edge-tts / longhun_senses / system TTS fallback."""

import asyncio
import hashlib
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

from config import get_settings

# 引入 Fish Audio 真声桥接（与 wechat_public_account 平级的 integrations/fish_audio/）
_FISH_AUDIO_DIR = Path(__file__).resolve().parents[2] / "fish_audio"
if str(_FISH_AUDIO_DIR) not in sys.path:
    sys.path.insert(0, str(_FISH_AUDIO_DIR))

try:
    from fish_audio_bridge import LongHunFishAudioBridge
except Exception as _fish_err:
    LongHunFishAudioBridge = None

# XTTS v2 本地真声配置
_VOICE_TWIN_DIR = Path("/Users/zuimeidedeyihan/longhun-system/voice-twin")
_XTTS_REFERENCE = _VOICE_TWIN_DIR / "voice_dataset" / "reference_optimized.wav"
_XTTS_ENV = _VOICE_TWIN_DIR / ".venv-tts"
_XTTS_PYTHON = _XTTS_ENV / "bin" / "python3"
_XTTS_CLI = _VOICE_TWIN_DIR / "voice_clone_trainer.py"


def _xtts_available() -> bool:
    return _XTTS_PYTHON.exists() and _XTTS_CLI.exists() and _XTTS_REFERENCE.exists()


class VoiceService:
    """Generate voice/audio for articles."""

    VALID_STYLES = ["storyteller", "educator", "passionate", "calm", "default"]

    # 中文 edge-tts 音色映射：默认全部走成熟男声，避免“奶狗”感
    STYLE_VOICE_MAP = {
        "educator": "zh-CN-YunjianNeural",   # 沉稳男声，适合播报
        "storyteller": "zh-CN-YunhaoNeural",  # 叙述感男声
        "passionate": "zh-CN-YunxiNeural",    # 激情男声（可加速）
        "calm": "zh-CN-YunjianNeural",         # 冷静 = 稳重慢速
        "default": "zh-CN-YunjianNeural",      # 默认稳重男声
    }

    STYLE_RATE_MAP = {
        "educator": "-5%",
        "storyteller": "-10%",
        "passionate": "+10%",
        "calm": "-15%",
        "default": "-5%",
    }

    def __init__(self):
        self.settings = get_settings()
        self.cache_dir = self.settings.CACHE_DIR / "voices"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.senses_script = Path(
            "~/.longhun/scripts/longhun_senses/senses_cli.py"
        ).expanduser()

    def generate(
        self,
        text: str,
        output_path: Optional[str] = None,
        style: str = "educator",
        use_soul: bool = True,
    ) -> str:
        """Generate voice file from text.

        Priority:
          1) 本地 XTTS v2 UID9622 真声克隆（已验证可用，首选）
          2) Fish Audio UID9622 真声克隆（如果 model_id 已配置且网络通达）
          3) edge-tts 成熟中文男声（默认主路径）
          4) longhun_senses（ElevenLabs 等）
          5) 系统 say/tts
        """
        if style not in self.VALID_STYLES:
            style = "educator"

        if output_path is None:
            h = hashlib.md5(f"{text}-{time.time()}".encode()).hexdigest()[:8]
            output_path = str(self.cache_dir / f"voice_{h}.mp3")

        output_path = Path(output_path).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 0) 本地 XTTS v2 UID9622 真声克隆（彻底告别奶狗音）
        if _xtts_available() and self._try_xtts(text, output_path):
            return str(output_path)

        # 1) Fish Audio UID9622 真声克隆（云端，需网络通达）
        if LongHunFishAudioBridge and self._try_fish_audio(text, output_path):
            return str(output_path)

        # 2) edge-tts 成熟男声（微信播报主路径）
        if self._try_edge_tts(text, output_path, style):
            return str(output_path)

        # 2) 回退 longhun_senses（ElevenLabs 等）
        if self.senses_script.exists():
            if use_soul and self._try_soul(text, output_path, style):
                return str(output_path)
            if self._try_tts(text, output_path):
                return str(output_path)

        # 3) 最终回退系统 TTS
        if self._try_system_tts(text, output_path):
            return str(output_path)

        raise RuntimeError(
            "Could not generate voice. Please check Fish Audio / edge-tts / longhun_senses / system TTS."
        )

    def _try_fish_audio(self, text: str, output_path: Path) -> bool:
        """使用 Fish Audio UID9622 真声模型生成语音。网络不通或模型未配置时快速回退。"""
        if not LongHunFishAudioBridge:
            return False
        try:
            bridge = LongHunFishAudioBridge()
            if not bridge.get_model_id():
                return False
            bridge.text_to_speech(text[:2000], output_file=output_path, timeout=15)
            return output_path.exists() and output_path.stat().st_size > 0
        except Exception as e:
            print(f"Fish Audio 真声生成失败，回退 edge-tts: {e}")
            return False

    def _try_xtts(self, text: str, output_path: Path) -> bool:
        """使用本地 XTTS v2 + reference_optimized.wav 生成 UID9622 真声。"""
        if not _xtts_available():
            return False
        try:
            # XTTS 输出 wav，再转 mp3
            wav_path = output_path.with_suffix(".xtts.wav")
            env = os.environ.copy()
            env["COQUI_TOS_AGREED"] = "1"
            subprocess.run(
                [
                    str(_XTTS_PYTHON),
                    str(_XTTS_CLI),
                    "--test",
                    "--reference", str(_XTTS_REFERENCE),
                    "--text", text[:2000],
                ],
                cwd=str(_VOICE_TWIN_DIR),
                env=env,
                check=True,
                capture_output=True,
                text=True,
                timeout=180,
            )
            # 找到最新生成的 voice_clone_test_*.wav
            candidates = sorted(_VOICE_TWIN_DIR.glob("voice_clone_test_*.wav"), key=lambda p: p.stat().st_mtime)
            if not candidates:
                print("XTTS 未生成音频文件")
                return False
            wav_path = candidates[-1]
            # 转换为 mp3
            subprocess.run(
                ["ffmpeg", "-y", "-i", str(wav_path), "-ar", "44100", "-ac", "2", "-b:a", "192k", str(output_path)],
                check=True,
                capture_output=True,
                timeout=60,
            )
            return output_path.exists() and output_path.stat().st_size > 0
        except Exception as e:
            print(f"本地 XTTS 真声生成失败，回退 Fish Audio / edge-tts: {e}")
            return False

    def _try_edge_tts(self, text: str, output_path: Path, style: str) -> bool:
        """使用 edge-tts 生成成熟中文男声。优先用 Python 库，失败则调用已安装的 CLI。"""
        voice = self.STYLE_VOICE_MAP.get(style, "zh-CN-YunjianNeural")
        rate = self.STYLE_RATE_MAP.get(style, "-5%")

        # 路径 A：Python 库（如果当前环境已安装）
        try:
            import edge_tts

            communicate = edge_tts.Communicate(
                text=text[:2000],
                voice=voice,
                rate=rate,
                volume="+0%",
                pitch="+0Hz",
            )
            asyncio.run(communicate.save(str(output_path)))
            return output_path.exists() and output_path.stat().st_size > 0
        except Exception as e:
            print(f"edge-tts Python 库调用失败，尝试 CLI: {e}")

        # 路径 B：调用 voice-twin venv 里的 edge-tts CLI（免全局安装）
        edge_cli_candidates = [
            "/Users/zuimeidedeyihan/longhun-system/voice-twin/.venv-tts/bin/edge-tts",
            shutil.which("edge-tts"),
        ]
        edge_cli = next((c for c in edge_cli_candidates if c and Path(c).exists()), None)
        if not edge_cli:
            print("未找到 edge-tts CLI")
            return False

        try:
            subprocess.run(
                [
                    edge_cli,
                    "--voice", voice,
                    f"--rate={rate}",
                    "--text", text[:2000],
                    "--write-media", str(output_path),
                ],
                check=True,
                capture_output=True,
                text=True,
                timeout=120,
            )
            return output_path.exists() and output_path.stat().st_size > 0
        except Exception as e:
            print(f"edge-tts CLI 失败: {e}")
            return False

    def _try_soul(self, text: str, output_path: Path, style: str) -> bool:
        """Try longhun_senses soul command."""
        try:
            result = subprocess.run(
                [
                    "python3",
                    str(self.senses_script),
                    "soul",
                    text,
                    "--style",
                    style,
                    "--no-play",
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
            )
            # longhun_senses may output file path or save to default location
            if result.returncode == 0:
                # Try to find output file from stdout
                for line in result.stdout.splitlines():
                    line = line.strip()
                    if line.endswith((".mp3", ".wav", ".ogg")):
                        src = Path(line)
                        if src.exists():
                            shutil.copy2(src, output_path)
                            return True
                # Check common output locations
                candidates = list(Path("~/.longhun/senses/output").expanduser().glob("*.mp3"))
                if candidates:
                    shutil.copy2(max(candidates, key=lambda p: p.stat().st_mtime), output_path)
                    return True
            return False
        except Exception:
            return False

    def _try_tts(self, text: str, output_path: Path) -> bool:
        """Try longhun_senses tts command."""
        try:
            result = subprocess.run(
                ["python3", str(self.senses_script), "tts", text, "--no-play"],
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    line = line.strip()
                    if line.endswith((".mp3", ".wav", ".ogg")):
                        src = Path(line)
                        if src.exists():
                            shutil.copy2(src, output_path)
                            return True
                candidates = list(Path("~/.longhun/senses/output").expanduser().glob("*.mp3"))
                if candidates:
                    shutil.copy2(max(candidates, key=lambda p: p.stat().st_mtime), output_path)
                    return True
            return False
        except Exception:
            return False

    def _try_system_tts(self, text: str, output_path: Path) -> bool:
        """Fallback to macOS say command."""
        if shutil.which("say"):
            try:
                # macOS say outputs aiff by default
                aiff_path = output_path.with_suffix(".aiff")
                subprocess.run(
                    ["say", text, "-o", str(aiff_path)],
                    check=True,
                    timeout=60,
                )
                if aiff_path.exists():
                    # Convert to mp3 if ffmpeg available
                    if shutil.which("ffmpeg"):
                        mp3_path = output_path.with_suffix(".mp3")
                        subprocess.run(
                            [
                                "ffmpeg",
                                "-y",
                                "-i",
                                str(aiff_path),
                                "-ar",
                                "44100",
                                "-ac",
                                "2",
                                "-b:a",
                                "192k",
                                str(mp3_path),
                            ],
                            check=True,
                            timeout=60,
                        )
                        aiff_path.unlink()
                        return True
                    else:
                        # Keep aiff if no ffmpeg
                        return True
            except Exception:
                pass
        return False
