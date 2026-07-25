# 龍魂·媒体主权标记协议 v1.0（视频水印 v3.0 更新）

**DNA:** `#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-MEDIA-SOVEREIGNTY-MARK-v1.0`

**确认码:**
```
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
```

---

## 一、协议目标

建立一套跨字体、图像、视频、音频、数字人的统一 DNA 主权标记系统，确保任何从龍魂生态产出的内容都携带**原生、抗洗、可追溯**的主权印记。

**核心原则：**
1. **原生内嵌**：标记是内容的一部分，不是后期贴上去的标签。
2. **多层级**：可见水印 + 隐写水印 + 频域水印，层层加固。
3. **DNA 追溯**：每个标记都带六层来源链 DNA。
4. **抗洗稿**：单一处理无法完全移除，需同时破坏多层才生效。

---

## 二、覆盖媒体类型

| 媒体 | 标记方式 | 提取方式 | 抗攻击能力 |
|:---|:---|:---|:---|
| **字体** | U+E200 龙纹缩微水印 + name 表 DNA | 校验 PUA 字形 + 读取 name 表 | 改文件名无法移除 |
| **图像** | LSB 最低有效位 + DCT 频域隐写 | 优先 LSB，失败 fallback DCT | 抗轻度压缩、裁剪 |
| **视频** | **帧级 DCT 扩频指纹（主）+ 音频轨 Patchwork 指纹（副）** | 优先帧级 DCT 投票提取，失败 fallback 音频 | 抗 H.264/H.265 重编码、录屏、AAC 压缩 |
| **音频** | 时域 LSB + 3 重复码（普通版）/ 频域 DSSS + 三频带副本（鲁棒版） | 3 取多数解码 / 相关检测 + 跨块投票 | 抗轻度裁剪、噪声 / 抗 AAC/MP3 压缩 |
| **数字人** | 复用图像/视频/音频标记 | 按输出格式对应提取 | 多层叠加 |

---

## 三、DNA 格式

```
#龍芯⚡️{干支}·☰乾-MEDIA-SOVEREIGNTY-MARK-v1.0-{media_type}-{owner}-{uniq}
```

示例：
```
#龍芯⚡️46·07·25·17时·☰乾-MEDIA-SOVEREIGNTY-MARK-v1.0-image-UID9622-A1B2C3D4
```

自定义 DNA 也允许，只要包含 `龍魂`、`DNA`、`UID`、`龍芯`、`LH-`、`MEDIA-MARK` 等任一关键字即可被识别。

---

## 四、CLI 使用

```bash
# 标记字体
python3 engines/lh_media_sovereignty_marker.py mark 龙魂字体-Regular.otf \
  --type font --dna "龍魂DNA#UID9622#FONT-001" --output 字体-已标记.otf

# 标记图像
python3 engines/lh_media_sovereignty_marker.py mark input.png \
  --type image --dna "龍魂DNA#UID9622#IMAGE-001" --output output.png

# 标记音频
python3 engines/lh_media_sovereignty_marker.py mark input.wav \
  --type audio --dna "龍魂DNA#UID9622#AUDIO-001" --output output.wav

# 标记视频（帧级 DCT 扩频指纹 + 音频轨指纹）
python3 engines/lh_media_sovereignty_marker.py mark input.mp4 \
  --type video --dna "龍魂DNA#UID9622#VIDEO-001" --output output.mp4

# 验证（自动识别类型）
python3 engines/lh_media_sovereignty_marker.py verify output.png
python3 engines/lh_media_sovereignty_marker.py verify output.wav
python3 engines/lh_media_sovereignty_marker.py verify 字体-已标记.otf
python3 engines/lh_media_sovereignty_marker.py verify output.mp4
```

---

## 五、集成到视频/数字人生产线

视频生产线 (`bin/lh_video_pipeline.py`) 已在 CLI 提供 `mark` 子命令，直接给成品视频注入 DNA：

```bash
python3 bin/lh_video_pipeline.py mark final_video.mp4 \
  --dna "#龍芯⚡️...VIDEO-001-UID9622"
```

等价 Python 调用：

```python
from engines.lh_media_sovereignty_marker import VideoMarker

VideoMarker(final_video_path).embed(
    dna='龍魂DNA#UID9622#VIDEO-001',
    output_path=watermarked_video_path
)
```

数字人图像帧应逐帧调用 `ImageMarker`。音频旁白应调用 `AudioMarker`。

线上验证入口：https://uid9622.cn/media-verify/

---

## 六、六层来源链

每条 DNA 标记必须包含：
1. **创作者**：UID9622 / 龍魂系统
2. **底座模型**：使用的中文底座名称
3. **训练数据**：数据批次 / 协议版本
4. **生成工具**：引擎名称与版本
5. **生成时间**：UTC + 干支时间戳
6. **验证入口**：https://uid9622.cn/dna/{dna_hash}

---

## 七、安全等级

| 等级 | 描述 |
|:---|:---|
| 🟢 公开 | 带水印，可公开传播，被洗稿后可追溯 |
| 🟡 内部 | 增加可见暗纹，限制内部流转 |
| 🔴 机密 | 多层水印 + GPG 签名，外泄即熔断 |

---

## 八、限制与演进

**v1.0 已知限制：**
- 视频返回的是 `LHAF-<hash>` 短指纹，不是完整 DNA。完整 DNA 需通过短指纹在记录/数据库中反查。
- 音频鲁棒水印对极低码率压缩（< 64kbps）可能失效，此时仍可由帧级 DCT 指纹兜底。
- 图像 DCT 层对强压缩（JPEG quality < 70）可能失效，LSB 层仍可工作。

**v3.0 已落地：**
- 视频帧级 DCT 扩频指纹：抗 H.264/H.265 重编码与录屏。
- 视频音频轨 Patchwork 指纹：作为第二重保险。
- 视频生产线 `mark` 子命令一键注入 DNA。
- 官网验证入口 `/media-verify/` 支持视频上传并返回 fingerprint。

**v1.1 规划：**
- 图像 Reed-Solomon 纠错
- 字体字形级微调水印

---

**龍魂字体 · 龍魂视频 · 龍魂语音 · 龍魂数字人——全部带签章，全部可追溯。**
