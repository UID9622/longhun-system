#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂真声 · Fish Audio 语音克隆桥接

功能：
1. 使用 UID9622 参考音频在 Fish Audio 云端创建声音模型
2. 通过模型 ID 生成 UID9622 本人音色的 TTS 音频
3. 供微信公众号播报、龍魂真声控制台等模块调用

DNA: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-LONGHUN-FISH-AUDIO-BRIDGE-v1.0
"""

import json
import os
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional, Any


class LongHunFishAudioBridge:
    """Fish Audio TTS 桥接：让微信公众号播报收不到奶狗音，只放 UID9622 真声。"""

    API_BASE = "https://api.fish.audio"

    def __init__(
        self,
        reference_audio: Optional, Any[Path] = None,
        model_id_file: Optional, Any[Path] = None,
        output_dir: Optional, Any[Path] = None,
    ):
        self.api_key = self._load_api_key()

        # 默认使用 voice-twin 已经准备好的优化参考音
        self.reference_audio = Path(
            reference_audio
            or Path.home() / "longhun-system" / "voice-twin" / "voice_dataset" / "reference_optimized.wav"
        )

        self.model_id_file = Path(
            model_id_file
            or Path.home() / "longhun-system" / "integrations" / "fish_audio" / "voice_model_id.json"
        )

        self.output_dir = Path(
            output_dir
            or Path.home() / "longhun-system" / "integrations" / "fish_audio" / "output"
        )
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_api_key(self) -> Optional, Any[str]:
        """从环境变量或 secrets.env 读取 API key。"""
        key = os.getenv("FISH_AUDIO_API_KEY")
        if key:
            return key

        # 兼容 Claude 之前写的 secrets.env 格式
        secrets_paths = [
            Path.home() / ".longhun" / "secrets.env",
            Path.home() / "longhun-system" / "引擎" / ".env",
        ]
        for p in secrets_paths:
            if p.exists():
                for line in p.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line.startswith("FISH_AUDIO_API_KEY=") or line.startswith("export FISH_AUDIO_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        return None

    def health_check(self) -> dict[str, Any]:
        """返回当前状态。"""
        return {
            "api_key_configured": bool(self.api_key),
            "reference_audio_exists": self.reference_audio.exists(),
            "reference_audio_path": str(self.reference_audio),
            "model_id": self.get_model_id(),
            "output_dir": str(self.output_dir),
        }

    def get_model_id(self) -> Optional, Any[str]:
        """读取本地保存的 model_id。"""
        if self.model_id_file.exists():
            try:
                data = json.loads(self.model_id_file.read_text(encoding="utf-8"))
                return data.get("model_id")
            except Exception:
                return None
        return None

    def save_model_id(self, model_id: str) -> None:
        """持久化 model_id，避免每次重新创建。"""
        self.model_id_file.write_text(
            json.dumps(
                {
                    "model_id": model_id,
                    "created_at": datetime.now().isoformat(),
                    "reference_audio": str(self.reference_audio),
                    "dna": "#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-LONGHUN-FISH-AUDIO-BRIDGE-v1.0",
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def create_voice_model(
        self,
        name: str = "龍魂-UID9622-真声",
        description: str = "UID9622 / 龍芯北辰本人音色，用于微信公众号播报与龍魂系统语音交互",
    ) -> Optional, Any[str]:
        """上传参考音频，创建云端声音模型。返回 model_id。"""
        if not self.api_key:
            raise RuntimeError("未配置 FISH_AUDIO_API_KEY")
        if not self.reference_audio.exists():
            raise RuntimeError(f"参考音频不存在: {self.reference_audio}")

        print(f"🎙️ 正在 Fish Audio 创建声音模型: {name}")
        print(f"   参考音频: {self.reference_audio}")

        with open(self.reference_audio, "rb") as f:
            files = {"voices": (self.reference_audio.name, f, "audio/wav")}
            data = {
                "type": "tts",
                "title": name,
                "description": description,
                "visibility": "private",
                "train_mode": "fast",
            }
            resp = requests.post(
                f"{self.API_BASE}/model",
                headers={"Authorization": f"Bearer {self.api_key}"},
                data=data,
                files=files,
                timeout=120,
            )

        if resp.status_code == 200:
            result = resp.json()
            model_id = result.get("_id")
            if model_id:
                self.save_model_id(model_id)
                print(f"✅ 模型创建成功: {model_id}")
                return model_id
            else:
                print(f"⚠️ 响应中无 _id: {result}")
                return None
        else:
            raise RuntimeError(f"Fish Audio 创建模型失败: {resp.status_code} {resp.text}")

    def text_to_speech(
        self,
        text: str,
        output_file: Optional, Any[Path] = None,
        model_id: Optional, Any[str] = None,
        timeout: int = 120,
    ) -> Path:
        """用 UID9622 声音模型生成语音。"""
        if not self.api_key:
            raise RuntimeError("未配置 FISH_AUDIO_API_KEY")

        use_model_id = model_id or self.get_model_id()
        if not use_model_id:
            raise RuntimeError("没有可用 model_id，请先调用 create_voice_model()")

        if output_file is None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"tts_uid9622_{ts}.mp3"
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "text": text,
            "reference_id": use_model_id,
            "format": "mp3",
            "mp3_bitrate": 128,
        }

        resp = requests.post(
            f"{self.API_BASE}/v1/tts",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=timeout,
        )

        if resp.status_code == 200:
            output_file.write_bytes(resp.content)
            print(f"✅ 已生成 UID9622 真声: {output_file}")
            return output_file
        else:
            raise RuntimeError(f"Fish Audio TTS 失败: {resp.status_code} {resp.text}")


if __name__ == "__main__":
    import sys

    bridge = LongHunFishAudioBridge()

    if len(sys.argv) < 2:
        print(json.dumps(bridge.health_check(), ensure_ascii=False, indent=2))
    elif sys.argv[1] == "create":
        bridge.create_voice_model()
    elif sys.argv[1] == "speak":
        text = " ".join(sys.argv[2:])
        bridge.text_to_speech(text)
    else:
        print("用法: python fish_audio_bridge.py [create|speak '文字']")
