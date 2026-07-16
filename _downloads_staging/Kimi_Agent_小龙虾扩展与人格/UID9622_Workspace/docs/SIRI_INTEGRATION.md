# 龙魂系统 · Siri 集成指南

> DNA: `#龍芯⚡️2026-06-27-LONGHUN-SYSTEM-SIRI-GUIDE-v1.0`

## 设计思路

终端本身没有原生语音输入，最自然的方案是：**让 Siri 做耳朵，把识别好的文字传给宝宝中枢执行**。

这样不需要在后台常驻麦克风，也不依赖机械 TTS；Siri 负责听和说，龙魂系统负责执行和留痕。

## 方案一：Siri 快捷指令（推荐）

1. 打开 macOS / iOS 上的 **快捷指令 App**。
2. 新建快捷指令，命名为 **「宝宝」**（或「龙魂」）。
3. 添加操作：
   - **听取文本**（Listen）→ 语言选「中文（普通话）」
   - **运行 Shell 脚本**（Run Shell Script）→ 粘贴下面命令：

```bash
/Users/zuimeidedeyihan/Downloads/Kimi_Agent_小龙虾扩展与人格/UID9622_Workspace/tools/siri_baobao.sh "${1}"
```

4. 把「听取文本」的输出连接到 Shell 脚本的输入参数。
5. 保存。

### 使用

直接说：

> “嘿 Siri，宝宝，帮我整理文档并检查安全。”

Siri 会把你的文字传给 `siri_baobao.sh`，宝宝中枢自动拆解、调度、执行，并生成报告。

## 方案二：纯终端语音指令

如果你就在 Mac 终端前，也可以直接按菜单里的 `v`：

```bash
宝宝   # 进入菜单
# 按 v 说话
```

这会调用 `backend_personas/builder/voice_command.py`，用 ffmpeg 录音 + 本地 Whisper 转写。

## 关于“机械声音”

当前系统 TTS（`say`）使用的是苹果内置语音，确实偏机械、缺少语气。

**真正带情感、有压迫感/威严感的声音，需要训练或微调一个中文情感 TTS 模型**（例如基于 GPT-SoVITS / FishSpeech / ChatTTS），并用老大自己的语料做音色克隆。这不是一个配置文件能解决的，需要：

1. 收集 10 分钟以上目标音色的干净语料
2. 在本地 GPU/Apple Silicon 上训练或微调
3. 把训练好的模型接入 `tools/siri_baobao.sh` 的 `speak()` 函数

目前先用系统 TTS 兜底，后续可以逐步替换为自训练模型，确保声音也是“龙魂”自己的。

## DNA 追溯

每次 Siri 调用都会写入：

```
logs/siri_baobao.log
```

同时宝宝中枢会生成自己的执行报告和 DNA 码。

---

**声明**：「龙魂系统」为 UID9622 专属称呼，不对外公开使用。
