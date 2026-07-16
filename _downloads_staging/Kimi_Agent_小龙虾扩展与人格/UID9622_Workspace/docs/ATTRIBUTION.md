# 龙魂系统 · 外部参考与开源贡献登记

> **声明**：「龙魂系统」为 UID9622 专属称呼，不对外公开使用。  
> DNA: `#龍芯⚡️2026-06-27-LONGHUN-SYSTEM-ATTRIBUTION-v1.0`

## 登记原则

1. **凡引用必登记**：代码、算法、数据、思路，只要来自外部，全部写进来。
2. **只吸收干净开源**：优先使用为人民服务的宽松许可证项目。
3. **改动必说明**：龙魂系统对外部项目做了什么修改、为什么改。
4. **贡献必回馈**：每个外部项目对应 `data/contributors.json` 中的贡献分。

---

## 当前已引用项目

### 1. OpenAI Whisper

- **用途**：本地语音转文字（`backend_personas/builder/voice_command.py`）
- **来源**：https://github.com/openai/whisper
- **许可证**：MIT
- **使用方式**：本地运行 `tiny` 模型，不上传音频
- **龙魂改动**：封装为龙魂语音指令入口，加入 DNA 追溯与三色审计
- **贡献分**：15（基础 5 + 代码引用 10）

### 2. FFmpeg

- **用途**：麦克风音频录制（`backend_personas/builder/voice_command.py`）
- **来源**：https://ffmpeg.org
- **许可证**：LGPL/GPL（龙魂仅使用命令行调用，不链接库）
- **使用方式**：通过 `ffmpeg -f avfoundation` 录制 WAV
- **龙魂改动**：无，仅作为系统工具调用
- **贡献分**：8（基础 5 + 代码引用 3）

### 3. Plotly.js

- **用途**：三维仪表盘渲染（`backend_personas/core/dashboard.py`）
- **来源**：https://github.com/plotly/plotly.js
- **许可证**：MIT
- **使用方式**：通过 CDN 加载，本地数据渲染
- **龙魂改动**：完全自定义青铜/金镶玉/玄黑/朱砂主题与龙纹元素
- **贡献分**：10（基础 5 + 代码引用 5）

### 4. Coqui TTS / XTTS v2（已接入）

- **用途**：本地中文语音克隆播报（`backend_personas/baobao/audio_engine/xtts_server.py`、`tools/baobao_speak.sh`、`tools/siri_baobao.sh`）
- **来源**：https://github.com/coqui-ai/TTS
- **许可证**：MPL-2.0 / Coqui Public Model License（以仓库实际为准）
- **使用方式**：本地 XTTS v2 模型，支持双音色：内置女声 speaker 用于助手「宝宝」，UID9622 本人参考音用于内容播报
- **龙魂改动**：自研龍魂语音合成服务，模型本地常驻内存，双 profile 路由，加入 DNA 追溯与错误回退
- **贡献分**：15（基础 5 + 代码引用 10）

### 5. ChatTTS（备选）

- **预期用途**：中文情感 TTS 基座（威严/沉稳/压迫感等情感风格补充）
- **来源**：https://github.com/2noise/ChatTTS
- **许可证**：BSD-3-Clause（以仓库实际为准）
- **使用方式**：本地推理，替换机械 TTS
- **龙魂改动**：已准备 `backend_personas/baobao/audio_engine/chattts_tts.py` 与 `tools/install_chattts.sh`；网络恢复后安装并接入
- **贡献分**：13（基础 5 + 代码引用 8）

### 6. GPT-SoVITS（规划中）

- **预期用途**：专属音色克隆深度 fine-tune
- **来源**：https://github.com/RVC-Boss/GPT-SoVITS
- **许可证**：MIT（以仓库实际为准）
- **使用方式**：本地训练与推理
- **龙魂改动**：待接入；计划用本地语料做深度音色克隆
- **贡献分**：待定

---

## 龍魂原生能力

以下能力不依赖外部项目，属于龙魂系统自主创新：

- 三色审计体系
- DNA 追溯码生成与校验
- 六层来源链 / 通心译
- 洛书 369 / 数字根 / 八卦权重
- CNSH 中文命名规范
- 龍魂人格矩阵与路由调度
- 龍魂视觉生成引擎（SVG 纹样/色彩/图腾）

---

## 更新记录

| 时间 | 更新人 | 内容 |
|------|--------|------|
| 2026-06-27 | 宝宝·系统中枢 | 初版登记 |
| 2026-06-27 | 宝宝·系统中枢 | 新增 XTTS v2 克隆语音、ChatTTS 备选、龍魂视觉引擎 |
