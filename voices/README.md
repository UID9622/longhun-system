# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 · 声音资产目录

**DNA**: `#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-VOICES-v1.0`

本目录统一管理龍魂系统所有的人声相关资产与历史代码。

## 目录结构

| 子目录 | 来源 | 状态 | 说明 |
|--------|------|------|------|
| `voice_dna_v1/` | 原 `voice-dna/` | 已归档 | 声音 DNA 锚定、数字人格、验证工具 |
| `voice_twin_v1/` | 原 `voice-twin/` | 已归档 | 声音克隆、TTS 输出、风格配置文件 |
| `presets/` | 新建 | 活跃 | 人格音色预设（TTS/ASR 引擎读取） |

## 主线入口

- TTS 合成：`bin/lh_tts_engine.py`
- ASR 识别：`bin/lh_asr_engine.py`
- 音频水印：`bin/lh_audio_watermark.py`
- 声音参数引擎：`engines/lh_voice_engine.py`

## 历史资产说明

- `voice_dna_v1/` 中的独立 web_api.py / cli.py 目前为历史实现，后续逐步合并到 `bin/lh_tts_engine.py` 与 `bin/lh_asr_engine.py`。
- `voice_twin_v1/` 中的 `tts_outputs/` 与 `style_profile.json` 为历史训练产物，保留供后续分析。
