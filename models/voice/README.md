# 龍魂 · 声音模型目录

**DNA**: `#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-VOICE-MODELS-v1.0`

本目录用于存放龍魂系统的人声模型权重与配置。

## 当前状态

- 轻量兜底方案已落地：`edge-tts` + `openai-whisper`
- 国产模型（ChatTTS / CosyVoice / Paraformer）待后续替换

## 文件说明

| 文件/目录 | 用途 |
|----------|------|
| `README.md` | 本说明 |
| `presets.json` | 人格音色映射表（由 TTS 引擎读取） |
| `*.pt` / `*.pth` / `*.safetensors` | 国产模型权重文件（大文件·不入 git） |

## 人格音色映射（edge-tts 兜底）

| 人格 | voice |
|------|-------|
| P77 / 通心譯 | zh-CN-YunxiNeural |
| S1 / 乔前辈 | zh-CN-YunjianNeural |
| S2 | zh-CN-YunxiNeural |
| S3 | zh-CN-YunxiNeural |
| P11 / 李白 | zh-CN-YunxiNeural |
| P01 / 魔瞳 | zh-CN-XiaoxiaoNeural |

## 使用

```bash
# 合成
python3 bin/lh_tts_engine.py --text "为人民服务" --voice 乔前辈 --output test.mp3

# 识别
python3 bin/lh_asr_engine.py --input test.mp3 --model tiny --lang zh

# 验证 DNA 水印
python3 bin/lh_audio_watermark.py verify test.mp3
```

## 国产模型替换路径

1. 下载 ChatTTS / CosyVoice / Paraformer 权重
2. 放入本目录（如 `chattts/`、`cosyvoice/`）
3. 修改 `bin/lh_tts_engine.py` 中的 `synthesize_edge_tts` 为对应模型调用
4. 保持人格映射表和 DNA 水印接口不变
