**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 🐉 龍魂生态 · 全媒体播放器 v1.1

**DNA**: `#龍芯⚡️丙午·丙申·辛酉·酉时·䷦蹇-MEDIA-PLAYER-REFINE-V1.1-P0-714d6fd6`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**层级**: `L2_工具层`
**规范名**: `08_BIN/L2_工具_媒体播放器_☯UID9622·丙午·丙申·辛酉·丙申·䷉履.py`
**别名**: `bin/lh_media_player.py`

## 功能定位

兼容龍魂体系的全功能媒体播放器，支持本地视频播放、语音识别（ASR）、画面文字识别（OCR），并生成可嵌入网页的 Video.js 播放器页面。v1.1 在命令行接口、缓存机制、字幕精度、OCR 去噪、配置管理与可观测性上全面升级。

## 核心能力

| 能力 | 实现方式 | 兜底方案 |
|:---|:---|:---|
| 本地播放 | mpv / ffplay / vlc 自动选择 | 提示安装播放器 |
| 关键帧提取 | ffmpeg fps filter | 跳过帧提取 |
| 画面 OCR | tesseract `chi_sim+eng` | PaddleOCR |
| 语音 ASR | faster-whisper / openai-whisper Python | whisper CLI |
| 字幕生成 | 基于 ASR 段真实时间戳生成 WebVTT | 静态 HTML |
| 嵌入页面 | Video.js 8.6.1 + WebVTT 字幕 + 可点击文稿 | 静态 HTML |
| 批量处理 | 扫描目录内 mp4/mov/mkv/avi | 单文件处理 |
| 状态检查 | `status` 子命令检查 ffmpeg/whisper/播放器 | 终端提示 |
| 配置管理 | `~/.longhun/media_player.json` | 代码内置默认值 |
| 缓存复用 | 输出文件新于源视频时跳过，支持 `--force` | 重新处理 |

## 文件位置

- 核心脚本：`bin/lh_media_player.py`
- Web 播放器模板：`web_apps/longhun-media-player/index.html`
- 处理产物：`08_STATE/media_player/<视频名>/`
- 嵌入页面：`08_STATE/media_player/<视频名>.html`
- 审计日志：`04_AUDIT/media_player.jsonl`
- 测试文件：`08_BIN/test_L2_工具_媒体播放器.py`

## 依赖清单

- Python 3.10+
- ffmpeg / ffprobe
- mpv / ffplay / vlc（至少一个）
- tesseract + `chi_sim` / `eng` 语言包
- （可选）openai-whisper / faster-whisper / whisper CLI
- （可选）PaddleOCR

## 命令用法

```bash
# 播放
python3 bin/lh_media_player.py play ~/Movies/demo.mp4 --player mpv

# 语音识别
python3 bin/lh_media_player.py asr ~/Movies/demo.mp4 --model-size base --language zh

# 画面文字识别
python3 bin/lh_media_player.py ocr ~/Movies/demo.mp4 --interval 5

# 完整处理（ASR + OCR + 嵌入页）
python3 bin/lh_media_player.py process ~/Movies/demo.mp4 --interval 5 --force

# 批量处理目录
python3 bin/lh_media_player.py batch ~/Movies/ --interval 5 --output-dir /tmp/out

# 工具可用性检查
python3 bin/lh_media_player.py status

# 查看当前生效配置
python3 bin/lh_media_player.py config
```

### 全局选项

- `--config <path>`：指定配置文件路径（默认 `~/.longhun/media_player.json`）
- `--output-dir <dir>`：覆盖输出目录（默认 `08_STATE/media_player`）
- `--verbose` / `--debug`：启用 DEBUG 级日志

## 配置文件示例

`~/.longhun/media_player.json`：

```json
{
  "player": "mpv",
  "interval": 5.0,
  "model_size": "base",
  "language": "zh"
}
```

配置项会被 CLI 参数覆盖。

## v1.1 改进

1. **argparse 子命令化**：`play` / `asr` / `ocr` / `process` / `batch` / `status` / `config`，并保留原有命令语法兼容。
2. **缓存机制**：音频、转写文稿、OCR 结果、关键帧在输出文件新于源视频时自动复用，可通过 `--force` 强制重新处理。
3. **准确 WebVTT**：ASR 结果保留 `start` / `end` 时间戳，字幕按真实语音段落生成，不再平均切分视频时长。
4. **OCR 去噪**：跳过 `[画面未识别到文字]` 帧，并对连续相同文本去重，减少噪声。
5. **日志系统**：引入 Python `logging`，默认 INFO，支持 `--verbose` 输出 DEBUG。
6. **配置支持**：读取 `~/.longhun/media_player.json`，CLI 参数优先。
7. **状态检查**：`status` 子命令一键检查 ffmpeg、ffprobe、tesseract、whisper、mpv 等工具可用性。
8. **错误与提示**：更友好的用户错误信息与工具缺失提示。
9. **Web 模板增强**：文稿可点击跳转、搜索过滤、复制嵌入代码、空格播放/暂停、移动端响应式、DNA 与状态展示。

## 嵌入代码示例

```html
<iframe src="./demo.html" width="960" height="720" frameborder="0"></iframe>
```

## 三色审计

- 🟢 播放器调用成功
- 🟢 帧提取 / 音频提取成功或缓存命中
- 🟢 ASR/OCR 完成并生成嵌入页
- 🟢 审计日志写入 `04_AUDIT/media_player.jsonl`
- 🟢 v1.1 新增 `status` / `config` 子命令正常运行

## 关联知识

- `longhun-asr`: 龍音 ASR 中文优先识别
- `longhun-ocr`: 龍瞳 OCR 中文画面识别
- `longhun-cnsh`: CNSH 中文原生脚本
- `bin/ganzhi_dna_engine`: v∞ 干支卦 DNA 生成器
