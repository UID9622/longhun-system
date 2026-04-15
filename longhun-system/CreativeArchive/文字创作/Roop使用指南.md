# 🎭 龍魂系统·Roop专业换脸工具·使用指南

**DNA追溯码**: #龍芯⚡️2026-02-23-Roop使用指南-v1.0  
**创建者**: 龍芯北辰｜UID9622

---

## 🚀 最简单的安装方法（推荐）

**第一步：安装Roop**

```bash
# 在Mac终端运行
pip3 install roop
```

**第二步：下载模型文件**

Roop需要一个人脸识别模型文件，第一次运行会自动下载，但如果下载慢，可以手动下载：

```bash
# 创建模型文件夹
mkdir -p ~/.insightface/models/buffalo_l

# 模型会自动下载，如果失败：
# 手动下载地址：https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip
# 下载后解压到 ~/.insightface/models/buffalo_l/ 文件夹
```

---

## 🎬 使用方法（超级简单）

**一行命令搞定：**

```bash
roop -s 人脸照片.jpg -t 原视频.mp4 -o 换脸后.mp4
```

**参数说明：**
- `-s`：Source（源），就是你的人脸照片
- `-t`：Target（目标），就是要换脸的视频
- `-o`：Output（输出），换脸后的视频保存位置

---

## 📝 完整示例

**老大只需要：**

```bash
# 1. 准备两个文件
#    我的脸.jpg  ← 老大的照片
#    原视频.mp4  ← 要换脸的视频

# 2. 在Mac终端运行一行命令
roop -s 我的脸.jpg -t 原视频.mp4 -o 我换脸后的视频.mp4

# 3. 等它跑完（可能需要几分钟）

# 4. 看结果：我换脸后的视频.mp4
```

---

## 🎯 高级玩法

**只换某一个人的脸（多人视频）：**

```bash
# 如果视频里有多个人，但只想换其中一个人的脸
# Roop会自动检测最清晰的那张脸进行替换
# 如果要更精确控制，可以用 --frame-processor 参数
```

**提升画质：**

```bash
roop -s 我的脸.jpg -t 原视频.mp4 -o 高清.mp4 --execution-provider cuda
# 如果Mac有GPU，加上这个参数会更快更清晰
```

**只处理前100帧（测试用）：**

```bash
roop -s 我的脸.jpg -t 原视频.mp4 -o 测试.mp4 --max-frames 100
```

---

## 💡 实用技巧

**技巧1：人脸照片的选择**
- ✅ 正面清晰照片效果最好
- ✅ 光线充足、五官清楚
- ❌ 避免侧脸、模糊、太暗的照片

**技巧2：视频选择**
- ✅ 人物正面出镜效果最好
- ✅ 画面稳定、清晰度高
- ❌ 避免剧烈晃动、逆光的视频

**技巧3：加速处理**
```bash
# 如果视频很长，可以先降低分辨率测试效果
# 满意后再用原分辨率处理

# 先用低分辨率测试
ffmpeg -i 原视频.mp4 -vf scale=640:-1 低分辨率.mp4
roop -s 我的脸.jpg -t 低分辨率.mp4 -o 测试.mp4

# 效果满意后，处理原视频
roop -s 我的脸.jpg -t 原视频.mp4 -o 最终版.mp4
```

---

## 🔧 常见问题

**问题1：提示找不到roop命令**

```bash
# 解决方法：确认pip3安装路径在环境变量里
which roop

# 如果找不到，手动运行：
python3 -m roop -s 我的脸.jpg -t 原视频.mp4 -o 输出.mp4
```

**问题2：速度太慢**

```bash
# Mac可能不支持GPU加速，只能用CPU
# 解决方法：
# 1. 先用低分辨率视频测试
# 2. 或者只处理关键片段
# 3. 或者用Windows/Linux+GPU的机器跑
```

**问题3：效果不满意**

```bash
# 可能原因：
# - 人脸照片角度不对
# - 原视频人脸太小或太模糊
# - 光线差异太大

# 解决方法：
# - 换一张更清晰、角度更正的照片
# - 选择人物更大、更清晰的视频
```

---

## 🎪 更多好玩的工具

**如果Roop不够用，还可以试试：**

**1. DeepFaceLab（最专业）**
```bash
# 下载地址：https://github.com/iperov/DeepFaceLab
# 功能最全，但需要训练，比较复杂
# 适合：对效果要求极高，愿意花时间学习
```

**2. FaceSwap（开源）**
```bash
# 下载地址：https://github.com/deepfakes/faceswap
# 完全开源，功能强大
# 适合：喜欢折腾，想深度定制
```

**3. Wav2Lip（对嘴型）**
```bash
# 下载地址：https://github.com/Rudrabha/Wav2Lip
# 不是换脸，是让视频人物对口型
# 适合：做配音视频，让口型和声音对上
```

---

## 🐉 龍魂版·一键脚本

**老大如果嫌麻烦，宝宝给你准备了一键脚本：**

```bash
#!/bin/bash
# 龍魂换脸一键脚本

echo "🎭 龍魂换脸工具启动！"

# 检查是否安装roop
if ! command -v roop &> /dev/null; then
    echo "❌ 还没安装roop，正在安装..."
    pip3 install roop
fi

# 检查文件夹
mkdir -p 人脸 视频 输出

# 找人脸照片
人脸=$(ls 人脸/*.{jpg,jpeg,png} 2>/dev/null | head -1)
if [ -z "$人脸" ]; then
    echo "❌ 没找到人脸照片！请放照片到 人脸/ 文件夹"
    exit 1
fi

# 找视频
视频=$(ls 视频/*.{mp4,avi,mov} 2>/dev/null | head -1)
if [ -z "$视频" ]; then
    echo "❌ 没找到视频！请放视频到 视频/ 文件夹"
    exit 1
fi

# 生成输出文件名
时间=$(date +%Y%m%d_%H%M%S)
输出="输出/换脸_${时间}.mp4"

echo "✅ 找到人脸：$人脸"
echo "✅ 找到视频：$视频"
echo "⏳ 开始换脸..."

# 运行roop
roop -s "$人脸" -t "$视频" -o "$输出"

echo "✅ 完成！文件在：$输出"
```

**保存为 `一键换脸.sh`，然后：**

```bash
chmod +x 一键换脸.sh
./一键换脸.sh
```

---

**DNA追溯码**: #龍芯⚡️2026-02-23-Roop使用指南-v1.0  
**创建者**: 龍芯北辰｜UID9622  
**北辰老兵致敬！** 🫡🇨🇳
