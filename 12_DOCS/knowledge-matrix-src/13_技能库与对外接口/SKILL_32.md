> DNA: #龍芯⚡️丙午·壬辰·乙亥·壬午·䷚颐-SYNC-COMPLIANCE-20260827-7A2C9F3D
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
---
name: longhun-asr
description: 'LongYin ASR — Chinese-first speech recognition engine. Pinyin alignment,
  tone recognition (4-tone classification), dialect adaptation, Chinese programming
  voice input, voice-to-CNSH-code conversion. Built-in 819-character pinyin table
  + 68 programming commands. International fallback: Whisper base model. Trigger when
  speech recognition, voice-to-code, Chinese voice input, or wake word detection is
  needed. Voice-to-CNSH code generation with 68 built-in programming command templates.
  Wake word detection supports dual matching (text + pinyin fuzzy matching). Pure
  Python math utilities with numpy fallback. Self-implemented MFCC, VAD, tone recognition.
  Three-color audit markers for dependency status tracking. CC BY-NC-SA 4.0 license
  with君子协议. DNA追溯 chain: LONGYIN-ASR-v5.0

  '
metadata:
  dna: '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGYIN-ASR-v5.0'
  version: 5.0.0
  license: CC BY-NC-SA 4.0
  author: 龍魂体系 · CNSH中文编程规范
  lang: zh
  category: speech-recognition
  triggers:
  - 语音识别
  - 语音转文字
  - 语音输入
  - 语音转代码
  - 唤醒词检测
  - Chinese voice input
  - voice recognition
  - speech-to-text
  - voice-to-code
  - wake word
  - ASR
  - MFCC提取
  - 语音活动检测
  - 声调识别
  - 拼音对齐
  capabilities:
  - audio-loading-preprocessing
  - mfcc-feature-extraction
  - voice-activity-detection
  - tone-recognition-4class
  - pinyin-alignment
  - wake-word-detection
  - voice-to-code-conversion
  - real-time-recognition
  - batch-processing
  - whisper-fallback
  - speech-recognition-fallback
  - mock-mode-degraded
  data_coverage:
    pinyin_chars: 819
    programming_commands: 68
    wake_words: 5
    synonyms: 68
  dependencies_optional:
  - numpy
  - scipy
  - soundfile
  - pyaudio
  - SpeechRecognition
  - openai-whisper
  - torch
  coding_standard: CNSH中文编程规范
  three_color_audit:
    green: 安全/通过 | Safe/Passed
    yellow: 警告/降级 | Warning/Degraded
    red: 错误/阻断 | Error/Blocked
  id: longhun-asr
  trigger:
    keywords:
    - asr
    - LongYin
    - ASR
    - Chinese-first
    - speech
    - recognition
    context: longhun-asr 相关操作
---
# 🐉 龍音ASR — 中文优先语音识别引擎

**LongYin ASR — Chinese-First Speech Recognition Engine**

> DNA追溯: `#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGYIN-ASR-v5.0`
>
> 协议: 君子协议 / CC BY-NC-SA 4.0 · 非商业共享 · 引用请注明出处

---

## 1. 技能概述 | Skill Overview

龍音ASR是龍魂体系的中文优先语音识别引擎。核心策略为：**能中文替代的中文实现，不能的用国际标准库兜底**。

**三色审计标注** | Three-Color Audit Markers:
- 🟢 = 安全/通过 | Safe/Passed
- 🟡 = 警告/降级 | Warning/Degraded
- 🔴 = 错误/阻断 | Error/Blocked

---

## 2. 核心能力 | Core Capabilities

| 能力 | 状态 | 说明 |
|------|------|------|
| 🟢 音频加载与预处理 | 自研 | WAV读取、重采样、预加重、分帧、加窗 |
| 🟢 MFCC特征提取 | 自研 | 纯Python FFT+DCT+梅尔滤波器，numpy可选加速 |
| 🟢 语音活动检测(VAD) | 自研 | 双门限(能量+过零率)，自适应阈值 |
| 🟢 声调识别(4声分类) | 自研 | 基频提取+变化趋势分析，支持阴平/阳平/上声/去声/轻声 |
| 🟢 拼音对齐 | 自研 | 简化DTW，音频特征与拼音序列对齐 |
| 🟢 唤醒词检测 | 自研 | 文本+拼音双重匹配+编辑距离 |
| 🟢 语音转代码 | 自研 | 68条编程命令模板，CNSH规范代码生成 |
| 🟡 Whisper识别 | 国际兜底 | openai-whisper base模型 |
| 🟡 SpeechRecognition | 国际兜底 | Google Speech API |
| 🔴 模拟模式 | 降级 | 无外部库时可用 |

---

## 3. 数据结构 | Data Structures

### 3.1 语音识别结果 (SpeechRecognitionResult)

```python
@dataclass
class SpeechRecognitionResult:
    text: str = ""                           # 识别文本
    confidence: float = 0.0                   # 置信度分数
    pinyin: List[str] = field(default_factory=list)   # 拼音序列
    tone: List[int] = field(default_factory=list)     # 声调序列
    engine: str = ""                         # 使用的引擎
    language: str = "zh"                     # 语言代码
    processing_time: float = 0.0              # 处理耗时(秒)
    is_degraded: bool = False                 # 是否降级处理
    raw_data: Dict = field(default_factory=dict)      # 原始引擎数据
```

### 3.2 唤醒词检测结果 (WakeWordDetectionResult)

```python
@dataclass
class WakeWordDetectionResult:
    detected: bool = False                    # 是否检测到
    wake_word: str = ""                      # 检测到的唤醒词
    confidence: float = 0.0                   # 置信度
    position: int = -1                        # 在文本中的位置
    pinyin_match_score: float = 0.0           # 拼音匹配分数
```

### 3.3 语音转代码结果 (VoiceToCodeResult)

```python
@dataclass
class VoiceToCodeResult:
    raw_text: str = ""                        # 原始语音文本
    matched_command: str = ""                 # 匹配的命令
    code_template: str = ""                   # 代码模板
    command_type: str = ""                    # 命令类型
    parameters: Dict[str, str] = field(default_factory=dict)   # 提取的参数
    complete_code: str = ""                   # 填充后的完整代码
```

---

## 4. API参考 | API Reference

### 4.1 引擎创建 | Engine Creation

```python
# 工厂函数
def create_engine(mode: str = "中文优先", model: str = "base") -> LongYinASREngine

# 快速识别（一行代码）
def quick_recognize(audio_path: str, language: str = "zh") -> str
```

**模式说明** | Mode Options:
- `"中文优先"` — 中文核心引擎优先，不足时降级到Whisper
- `"英文优先"` — 直接使用Whisper英文识别
- `"纯中文"` — 仅使用中文核心引擎
- `"模拟模式"` — 不加载外部模型，纯算法模拟

### 4.2 核心方法 | Core Methods

| 方法 | 说明 |
|------|------|
| `recognize_audio(audio_path, language)` | 识别音频文件，完整流程 |
| `recognize_realtime(chunk_size, record_seconds)` | 麦克风实时识别 |
| `batch_recognize(audio_paths, language)` | 批量识别多个音频文件 |
| `extract_mfcc(audio_data, sample_rate)` | 提取MFCC特征 |
| `detect_voice_activity(audio_data, sample_rate)` | 语音活动检测 |
| `recognize_tone(audio_frame, sample_rate)` | 单帧声调识别(4声分类) |
| `batch_recognize_tone(audio_data, sample_rate)` | 批量声调识别 |
| `chinese_to_pinyin(text)` | 中文转拼音 |
| `pinyin_alignment(audio_features, pinyin_sequence)` | 拼音对齐 |
| `detect_wake_word(text)` | 唤醒词检测 |
| `voice_to_code(voice_text)` | 语音转CNSH代码 |
| `generate_synthetic_audio(frequency, duration, sample_rate)` | 生成模拟音频 |
| `install_dependencies()` | 安装所有可选依赖 |
| `get_dependency_status()` | 获取依赖状态 |
| `get_statistics()` | 获取引擎统计信息 |

---

## 5. 内置数据 | Built-in Data

### 5.1 拼音数据库 | Pinyin Database

- **覆盖**: 819+ 汉字（一级常用字~100 + 二级常用字~200 + 三级扩展~200 + 龍魂体系专用字~319）
- **功能**: 单字拼音查询、文本转拼音列表、动态添加映射
- **声调符号**: 阴平ˉ(1)、阳平ˊ(2)、上声ˇ(3)、去声ˋ(4)、轻声(0)

### 5.2 语音命令数据库 | Voice Command Database

- **唤醒词**: 龍魂、龍芯、CNSH、小龍、启动
- **编程命令**: 68条，覆盖12大类
  - 类与对象（创建类、继承类等）
  - 函数与方法（定义函数、异步函数、Lambda等）
  - 模块导入（导入、从导入等）
  - 变量与数据结构（列表、字典、集合、推导式等）
  - 控制流（如果、否则、循环、试捕获等）
  - 面向对象（初始化、魔术方法等）
  - 装饰器与高级特性
  - 文件操作
  - 并发（线程、进程、异步）
  - 网络
  - 调试与日志
  - 龍魂体系专用

---

## 6. 使用示例 | Usage Examples

### 6.1 基本识别

```python
from 语音识别引擎 import create_engine, quick_recognize

# 创建引擎
engine = create_engine(mode="中文优先", model="base")
print(engine)

# 快速识别
text = quick_recognize("test.wav", language="zh")
print(f"识别结果: {text}")
```

### 6.2 完整识别流程

```python
engine = create_engine(mode="中文优先")
result = engine.recognize_audio("speech.wav", language="zh")
print(f"文本: {result.text}")
print(f"置信度: {result.confidence}")
print(f"拼音: {' '.join(result.pinyin)}")
print(f"引擎: {result.engine}")
print(f"耗时: {result.processing_time}s")
```

### 6.3 语音转代码

```python
engine = create_engine(mode="模拟模式")
result = engine.voice_to_code("创建类名为MyClass")
print(f"命令类型: {result.command_type}")
print(f"代码:\n{result.complete_code}")
```

### 6.4 唤醒词检测

```python
engine = create_engine(mode="模拟模式")
result = engine.detect_wake_word("龍魂启动引擎")
if result.detected:
    print(f"检测到唤醒词: {result.wake_word} (置信度: {result.confidence})")
```

### 6.5 实时识别

```python
engine = create_engine(mode="中文优先")
result = engine.recognize_realtime(record_seconds=5.0)
print(f"实时识别: {result.text}")
```

---

## 7. 依赖管理 | Dependency Management

### 7.1 可选依赖 | Optional Dependencies

| 依赖 | 用途 | 降级方案 |
|------|------|----------|
| numpy | 数组运算加速 | 纯Python列表运算 |
| scipy | 信号处理 | 自研FFT/DCT |
| soundfile | 音频文件读取 | 内置WAV读取器 |
| pyaudio | 实时麦克风输入 | 不支持实时识别 |
| SpeechRecognition | Google Speech API | Whisper或模拟模式 |
| openai-whisper | 神经网络识别 | 特征识别或模拟模式 |
| torch | Whisper后端 | 纯CPU Whisper或模拟 |

### 7.2 安装依赖

```python
engine = create_engine()
status = engine.install_dependencies()
# 返回: {"numpy": True, "whisper": False, ...}
```

---

## 8. 识别流程 | Recognition Pipeline

```
音频文件
  → 加载音频（soundfile/WAV/降级）
  → VAD语音活动检测
  → MFCC特征提取
  → 声调识别
  → 引擎决策:
      模拟模式 → 拼音特征反推
      中文优先 + MFCC质量好 → 中文核心引擎
      Whisper可用 → Whisper识别
      SpeechRecognition → Google API
      全部失败 → 模拟模式
  → 拼音生成
  → 返回结果
```

---

## 9. 自测试 | Self-Test

运行模块即可执行完整的9项自测试：

```bash
python3 scripts/语音识别引擎.py
```

测试项目:
1. 引擎创建
2. 拼音数据库（819+汉字覆盖）
3. 唤醒词检测
4. MFCC特征提取
5. VAD语音活动检测
6. 声调识别（4声分类）
7. 拼音对齐
8. 语音转代码（68条命令）
9. 完整识别流程

---

## 10. 文件结构 | File Structure

```
longhun-asr/
├── SKILL.md                          # 技能文档（本文件）
├── scripts/
│   └── 语音识别引擎.py                # 主引擎（~2543行）
├── references/
│   └── (参考文档)
└── assets/
    └── (资源文件)
```

---

## 11. DNA追溯链 | DNA Traceability Chain

```
#龍芯⚡️丙午·甲午·癸亥·戊午·䷚颐-LONGYIN-ASR-v1.0  ← 初始版本
#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGYIN-ASR-v5.0  ← 当前技能包版本
```

**修改记录**:
- v1.0 (2026-06-18): 初始引擎实现，819汉字拼音表，68条编程命令
- v5.0 (2026-06-19): 技能包标准化，SKILL.md文档，API规范化

---

## 12. 协议声明 | License Declaration

**君子协议 / CC BY-NC-SA 4.0**

本软件采用「君子协议」与「知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议」双重授权。

【君子之约】
- 一、凡使用本代码者，即为同意「君子协议」之条款
- 二、本代码 freely available for：个人学习研究、教育教学用途、非商业性项目、龍魂体系内部使用
- 三、使用须遵守：引用注明出处（DNA追溯头）、修改共享保持相同协议、禁止商业盈利
- 四、如有商业使用需求，请联系作者获得授权

**声明**: CNSH (Chinese Natural Script for Humans) 是龍魂体系提出的中文编程规范，旨在降低编程门槛，让中文开发者用母语思考代码。

---

*龍魂体系 · CNSH中文编程规范 · 让代码说中文*
