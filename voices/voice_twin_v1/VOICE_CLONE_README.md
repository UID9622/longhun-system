# 龍魂真声 · 语音克隆训练说明

DNA: #龍芯⚡️2026-06-25-VOICE-CLONE-UID9622-README

## 伦理边界

- **仅使用 UID9622 本人录音训练**，已排除包含他人对话的 `20260620 221423-E7210E2A.m4a`。
- 不克隆曾仕强老师或其他任何人的声音；知识库仅用于智慧解读。

## 已完成的准备工作

```bash
cd /Users/zuimeidedeyihan/longhun-system/voice-twin
python3 voice_clone_trainer.py --prepare
```

生成产物：

- `voice_dataset/wav/`：24kHz 单声道 WAV（约 31 分钟有效音源）
- `voice_dataset/chunks/`：按静音切分后的短片段
- `voice_dataset/reference.wav`：6 秒初始参考音
- `voice_dataset/reference_optimized.wav`：24 秒优化参考音（响度归一化 + 高通滤波 + 多段拼接）
- `voice_dataset/manifest.json`：数据集清单

## 环境安装（已完成）

在隔离环境 `.venv-tts` 中：

```bash
python3.11 -m venv .venv-tts --system-site-packages
source .venv-tts/bin/activate
pip install TTS transformers==4.33.3 soundfile moviepy fastapi uvicorn \
            -i https://pypi.tuna.tsinghua.edu.cn/simple
```

> 注意：TTS 0.22.0 默认会从 HuggingFace 下载 XTTS-v2，国内环境建议先把模型文件放到：
> `~/Library/Application Support/tts/tts_models--multilingual--multi-dataset--xtts_v2/`
> 里面包含 `model.pth`、`config.json`、`vocab.json`、`speakers_xtts.pth`、`hash.md5`。

## 优化参考音

```bash
python3 voice_clone_trainer.py --optimize-reference
```

这会从所有录音里挑出最长的干净片段，拼接成约 20 秒的 `reference_optimized.wav`，比 6 秒初始参考音更稳。

## 运行 XTTS v2 零样本克隆测试

```bash
cd /Users/zuimeidedeyihan/longhun-system/voice-twin
source .venv-tts/bin/activate
python3 voice_clone_trainer.py --test --text "你好，这里是 UID9622 的龍魂真声。"
```

```bash
# 用优化参考音生成更 UID9622 风格的测试
python3 voice_clone_trainer.py --test \
  --reference voice_dataset/reference_optimized.wav \
  --text "我跟你说，做人呐，别管别人怎么看，对不对？把自己的事做好，老天自有安排。"
```

输出示例：`voice_clone_test_HHMMSS.wav`

## 已生成音频

- `voice_clone_test_003020.wav` —— 第一版克隆测试
- `voice_clone_test_013651.wav` —— 优化参考音后的第二版测试
- `tts_preview_...wav` —— Web UI 实时克隆输出

## 接入浏览器控制台

浏览器 UI 已新增：

- `/api/sage` 圣贤对话
- `/api/export-wechat` 视频号/抖音导出
- `/api/tts` 优先使用 XTTS v2 克隆声音，未就绪时回退 Mac 系统 `say`

启动控制台：

```bash
source .venv-tts/bin/activate
python3 voice_twin_server.py
```

然后打开 http://localhost:9623

## 已生成文件

- `voice_clone_test_003020.wav` —— 首次成功克隆测试音频
- `tts_preview_你好_龍魂真声克隆测试.wav` —— Web UI 克隆 TTS 输出

## 后续优化方向

1. 对 `reference.wav` 做音量归一化（ffmpeg `loudnorm`）。
2. 用 faster-whisper 对 chunks 做时间戳对齐，生成训练对 `(audio, text)`。
3. 在 GPU 服务器上 fine-tune XTTS/GPT-SoVITS，把 31 分钟数据真正炼成 UID9622 音色。
4. 把训练好的模型路径写回 `voice_twin_server.py`，让 Web UI 直接输出克隆语音。
