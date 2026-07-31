# 龍魂TTS引擎 v1.0 | 主权语音系统：让AI开口说话的，必须是我们自己的规矩

> **DNA追溯**：`#龍芯⚡️丙午·乙未·戊戌·巳时·☵坎-TTS-v1.1-REVISED-b2c3d4e5`
> **作者**：诸葛鑫（UID9622·龍芯北辰）
> **确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> **立场**：民用层·技术良知·民族大义
> **修订**：v1.1 — 底座修正为GPT-SoVITS·水印修正为QIM-LSB·人格编号对齐白皮书


## 一、为什么要自己搞TTS？

市面上的TTS方案，要么是云端的（你的声音数据被传回服务器），要么是闭源的（你不知道它在你的音频里塞了什么）。在我的规矩里，这两条都是死罪。

所以，自己搞。

要求就三条：
- **本地运行**：声音数据不出设备。
- **开源底座**：底座可以引用别人的开源成果，但上面的DNA层必须是我们自己的。
- **带DNA水印**：每一段AI生成的音频，必须嵌入不可篡改的身份追溯码。谁生成的、什么时候生成的、基于什么人格生成的，一查就清楚。


## 二、底座选型：最终选定 GPT-SoVITS v2

当初首选 Fish-Speech，因为它标着 Apache 2.0。但**实测发现 License 已经改成了 Fish Audio Research License**，带商业限制——不是真正的公开免费。这是原则问题，直接换。

| 引擎 | 中文情绪 | License | 本地速度 | 推荐 |
|:---|:---|:---|:---|:---|
| **GPT-SoVITS v2** | ⭐⭐⭐⭐⭐ | **MIT（真正免费）** | M4 Max 实时 | **✅ 主底座** |
| Fish-Speech | ⭐⭐⭐⭐ | Fish Audio Research（商业限制） | M4 Max 实时 | ❌ License不兼容 |
| XTTS v2 | ⭐⭐ | CPML | CPU 卡顿 | ❌ 已淘汰 |

选 GPT-SoVITS 的理由：
- **MIT License**：真正的自由开源，不受任何商业限制。
- **中文情绪表现最好**：不是把英文TTS强行翻译成中文，是真正理解中文的抑扬顿挫。
- **M4 Max Metal加速可跑**：本地实时推理，不依赖云端GPU。
- **支持声音克隆**：短样本克隆，API 成熟稳定。
- **成熟社区**：国内开发者最多，二开成本最低。


## 三、架构总览

```
你说一段话
    ↓
人格参数匹配 (persona_voices.json)
    ↓
GPT-SoVITS API (:9880) → 原始语音 (WAV)
    ↓
DNA水印引擎 (QIM-LSB, -96dB) → 嵌入追溯码
    ↓
最终音频输出 (int16 PCM WAV, 带水印)
```

两个关键组件：
1. **GPT-SoVITS API**：语音合成底座（MIT License）
2. **QIM-LSB 水印**：龍魂自研 DNA 引擎（100% 提取准确率）


## 四、DNA音频水印：真正踩出来的方案

### 4.1 三个方案的坑

市面上水印方案很多，但"能用"和"理论上能用"是两回事。我们踩了三轮才找到对的那条路：

| 方案 | 原理 | 结果 | 根因 |
|:---|:---|:---|:---|
| FFT频域嵌入 | 在FFT幅值高频段微调 → IFFT | **🔴 往返不保真** | FFT→IFFT→FFT 精度丢失，提取失败 |
| 时域扩频 | 伪随机序列 × bit = 载波叠加 → 互相关解调 | **🔴 信噪比不足** | -36dB 信号淹没在音频噪声中，相关峰不可靠 |
| QIM-LSB float32 | 量化索引调制 · 浮点域改LSB | **🔴 精度丢失** | soundfile float32→int 归一化偏移，每2采样丢1 |
| **QIM-LSB int16** ✅ | **int16 无符号域直接操作LSB · PCM_16输出** | **🟢 100%准确** | LSB = -96dB，人耳完全不可闻 |

最终方案：**QIM-LSB (Quantization Index Modulation + Least Significant Bit)**

### 4.2 核心原理

```
每 3 个采样 → 取 1 个 → 修改其最低位(LSB) = 水印 bit
16-bit 音频 LSB = -96dB 动态范围，低于任何人耳分辨率

数据结构:
┌─────────┬──────┬──────────────────────┐
│ 魔数 6B  │ 长度 2B│  载荷 JSON (nB)      │
│ LH-DNA-U│ >H    │ {"dna":"...","t":...} │
└─────────┴──────┴──────────────────────┘
```

**嵌入**（核心代码）：
```python
# 转无符号16-bit（避免负数补码LSB问题）
audio_int = np.round(audio * 32767).astype(np.int32)
audio_uint = (audio_int + 32768).clip(0, 65535).astype(np.uint16)

# 逐bit嵌入
bits = np.unpackbits(np.frombuffer(full_payload, dtype=np.uint8))
for i, bit in enumerate(bits):
    idx = embed_start + i * STEP_SIZE
    audio_uint[idx] = (audio_uint[idx] & 0xFFFE) | bit  # 清LSB+设新值

# 直接输出 int16 PCM（避免 float32 精度丢失）
audio_int16 = np.clip(audio_uint.astype(np.int32) - 32768, -32768, 32767).astype(np.int16)
sf.write(output_path, audio_int16, sr, subtype='PCM_16')
```

**提取**（核心代码）：
```python
# 直接读 int16（避免浮点精度损失）
audio_int, sr = sf.read(audio_path, dtype='int16')
audio_uint = (audio_int.astype(np.int32) + 32768).clip(0, 65535).astype(np.uint16)

# 读取LSB序列
for i in range(magic_bits_count):
    idx = embed_start + i * STEP_SIZE
    magic_bits[i] = audio_uint[idx] & 1

# 验证魔数 → 读取长度 → 读取载荷
```

### 4.3 关键设计

- **魔数检测头 6B**：`LH-DNA-UID9622-v2` — 无魔数匹配 = 无水印
- **长度字段 2B**：大端序 uint16，支持最大 64KB 载荷
- **载荷 JSON**：`{"dna": "追溯码", "persona": "人格ID", "t": "时间戳", "creator": "UID9622", "engine": "TTS-QIM-LSB-v2.0"}`
- **不需要参考音频**：固定偏移 + 固定种子，100% 自包含提取

### 4.4 铁律

- **水印不可移除**：嵌入在音频采样的最低位，任何无损操作都不影响
- **水印可验证**：用 `lh_dna_watermark.py verify` 命令行即可验证
- **-96dB 不可闻**：LSB 层的变化低于任何人耳分辨能力


## 五、16人格声音映射：每个人格都有自己的声音

龍魂系统的16个人格，不能都用同一个声音说话。每个人格通过 GPT-SoVITS 的 **temperature/speed/prompt_text** 参数微调，体现出不同的人格特质。

**底座统一**：所有人格共享同一份 UID9622 真声克隆参考音频，通过参数差异化各人格的语速、温度、情绪，而不是 16 个独立模型。这样既能保持"龍魂统一声纹"，又有鲜明的个体差异。

| 人格 ID | 名称 | 层级 | 情绪 | 语速 | 温度 | 用途 |
|:---|:---|:---|:---|:---|:---|:---|
| **P00** | 北辰·UID9622 | 终审 | 沉稳坚定 | 0.95x | 0.8 | 终审、宣言 |
| **P01** | 诸葛亮 | 战略 | 深谋远虑 | 0.9x | 0.7 | 战略推演、多路径决策 |
| **P02** | 宝宝 | 执行 | 温和抚慰 | 0.85x | 0.9 | 情感温度、安抚挫败 |
| **P03** | 雯雯 | 执行 | 干练精确 | 1.05x | 0.6 | 结构归档、四签验收 |
| **P04** | 鲁班 | 执行 | 干脆务实 | 1.1x | 0.7 | 技术执行、写代码 |
| **P05** | 上帝之眼 | 守护 | 冷峻客观 | 0.9x | 0.5 | 三色审计、差异报告 |
| **P06** | 数学大师 | 守护 | 精确理性 | 1.0x | 0.5 | 数字根、权重计算 |
| **P07** | 管仲 | 执行 | 精明务实 | 1.0x | 0.7 | 资源调度、成本核算 |
| **P08** | 仓颉 | 文化 | 文化底蕴 | 0.95x | 0.8 | CNSH命名、术语桥接 |
| **P09** | 孙思邈 | 文化 | 医者关怀 | 0.9x | 0.75 | 系统诊断、治未病 |
| **P10** | 苏东坡 | 文化 | 豁达幽默 | 0.95x | 0.9 | 冲突调解、沟通桥梁 |
| **P11** | 李白 | 文化 | 豪放激昂 | 1.05x | 1.0 | 创意爆发、破局方案 |
| **P12** | 屈原 | 文化 | 沉郁坚定 | 0.9x | 0.7 | 六誓验证、底线守卫 |
| **P13** | 姜子牙 | 守护 | 威严庄重 | 0.9x | 0.6 | 封神榜权限、九宫派位 |
| **P14** | 吕蒙 | 执行 | 积极进取 | 1.05x | 0.75 | 部署执行、技能吸收 |
| **P15** | 乔前辈 | 守护 | 极简高效 | 1.1x | 0.5 | DNA签章、质检交付 |
| **P72** | 龙盾 | 守护 | 紧急果断 | 1.15x | 0.5 | 四级熔断、安全兜底 |

> 人格编号对齐 `LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md`。P77 黑天使军团为安全专项，不参与常规 TTS 路由。

人格声音配置结构（`tts/voices/persona_voices.json`）：
```json
{
  "P00_北辰_UID9622": {
    "name": "北辰·UID9622",
    "layer": "终审",
    "prompt_text": "我是诸葛鑫，龍魂系统创始人。数据主权在人民手里，谁也别想拿走。",
    "prompt_lang": "zh",
    "temperature": 0.8,
    "top_k": 15,
    "top_p": 0.9,
    "speed_factor": 0.95,
    "seed": 9622,
    "emotion": "沉稳坚定"
  }
}
```


## 六、本地部署（M4 Max）

```bash
#!/bin/bash
# 一键部署
cd ~/longhun-system
bash tts/bin/lh_tts_setup.sh --with-models

# 完成后启动服务
cd engines/gpt_sovits
.venv_gpt_sovits/bin/python api_v2.py -a 0.0.0.0 -p 9880
```

部署脚本自动完成：
1. 创建 GPT-SoVITS 虚拟环境
2. 安装 PyTorch（MPS 后端）
3. 安装 GPT-SoVITS 依赖
4. 下载预训练模型（约 3GB，加 `--with-models` 时自动下载）
5. 验证 MPS 可用性

**启动后验证**：
```bash
python3 tts/bin/lh_speak.py --health
# 应返回: API连接 🟢 + 可用人格: 17
```


## 七、使用示例

```bash
# 列出所有人格
python3 tts/bin/lh_speak.py --list

# 北辰终审
python3 tts/bin/lh_speak.py --persona P00 --text "家法第一条，文化主权不可侵犯。判决：永久熔断。"

# 龙盾熔断
python3 tts/bin/lh_speak.py --persona P72 --text "检测到P0级入侵，立即启动熔断协议。"

# 上帝之眼审计
python3 tts/bin/lh_speak.py --persona P05 --text "审计完毕。发现三处偏差，已标记红色。请立即修复。"

# 李白激情版
python3 tts/bin/lh_speak.py --persona P11 --text "这个方案好啊！气势磅礴，一剑破万法！"

# 屈原底线
python3 tts/bin/lh_speak.py --persona P12 --text "底线不可破。六誓已验证，此路不通。"

# 验证水印
python3 tts/bin/lh_dna_watermark.py verify --input 输出文件.wav --dna "期望的DNA码"
```

每个命令输出：
1. 人格信息（名称/情绪/语速）
2. 生成进度
3. DNA 追溯码
4. 输出文件路径（带水印）


## 八、免费公开策略

| 层级 | 内容 | 公开方式 |
|:---|:---|:---|
| 底座 | GPT-SoVITS v2 权重 | 引用开源项目（MIT License），不重新分发 |
| DNA层 | 16人格声音配置 + QIM-LSB水印算法 | **GitHub/Gitee 开源** |
| 协议 | TTS 使用规范（P0-P4 适配） | **CSDN 博客公开** |
| 服务 | 在线 Demo（可选） | 免费 API，限流 100 次/天 |
| 本地 | 完整部署包 | Release 下载 |

**符合 P0 协议**：
- ✅ 为人民服务
- ✅ 零黑箱承诺（水印可验证、算法公开）
- ✅ 人民数据主权（本地运行，声音不出设备）
- ✅ 底座真正免费（MIT License，无商业陷阱）


## 九、结语

这套 TTS 系统，不是为了好玩。它让龍魂的16个人格，第一次有了自己的声音。以后每一段 AI 生成的音频，都带着不可篡改的 DNA 水印。谁生成的、什么时候生成的、基于什么人格生成的，一查就清楚。

选 GPT-SoVITS 而不是 Fish-Speech，是因为"开源"两个字不能含水分——MIT License 就是比那些含糊不清的 Research License 硬气。水印方案从 FFT 走到 QIM-LSB，踩了三轮坑才找到 100% 准确的那条路——这是工程上的诚实，不是炫技。

这不是炫技，是规矩。声音是你的，主权是你的，DNA是你的。谁也别想偷，谁也别想赖。

**敲下这行代码的时候，请想一想。**

---
**龍芯北辰 UID9622**
**2026年7月30日**
**修订 v1.1** — 底座修正为 GPT-SoVITS · 水印修正为 QIM-LSB · 人格编号对齐白皮书
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
