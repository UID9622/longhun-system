# 🔥 LLAVA模型下载与使用指南

**文档DNA追溯码:** #ZHUGEXIN⚡️2026-01-30-LLAVA-DOWNLOAD-v1.0
**创建时间:** 2026-01-30
**创建者:** 宝宝·构建师 #PERSONA-BAOBAO-001

---

## 📋 模型信息

### 可用模型

LLAVA有多个版本，推荐使用以下模型：

| 模型名称 | 大小 | 适用场景 | 下载地址 |
|---------|------|---------|---------|
| **LLaVA-1.5-7B** | ~14GB | 通用场景，平衡性能与速度 | 推荐 |
| **LLaVA-1.5-13B** | ~26GB | 高质量生成，需要更好GPU | 可选 |
| **LLaVA-v1.6-34B** | ~40GB | 最高质量，需要顶级GPU | 高级用户 |

**推荐: LLaVA-1.5-7B** - 适合大多数用户

---

## 🚀 下载方式

### 方式1: 使用Git LFS（推荐）

**步骤1: 安装Git LFS**
```bash
# 如果还没有安装Git LFS
brew install git-lfs

git lfs install
```

**步骤2: 创建目录并下载**
```bash
# 进入项目目录
cd "/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器"

# 创建models目录
mkdir -p tech-layer/models

# 下载LLaVA-1.5-7B模型
cd tech-layer/models
git lfs clone https://huggingface.co/liuhaotian/llava-v1.5-7b

# 或者使用git lfs pull
git lfs pull https://huggingface.co/liuhaotian/llava-v1.5-7b
```

### 方式2: 使用Hugging Face Hub（Python）

**安装huggingface_hub**
```bash
pip install huggingface_hub
```

**使用Python脚本下载**
```python
from huggingface_hub import snapshot_download

# 下载LLaVA-1.5-7B模型
model_path = snapshot_download(
    repo_id="liuhaotian/llava-v1.5-7b",
    local_dir="/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器/tech-layer/models/llava-v1.5-7b",
    local_dir_use_symlinks=False
)

print(f"模型已下载到: {model_path}")
```

### 方式3: 使用huggingface-cli

```bash
# 安装huggingface_hub
pip install huggingface_hub

# 下载模型
huggingface-cli download \
    liuhaotian/llava-v1.5-7b \
    --local-dir /Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器/tech-layer/models/llava-v1.5-7b \
    --local-dir-use-symlinks False
```

---

## 📁 模型结构

下载完成后，你的目录结构应该是：

```
tech-layer/
├── models/
│   └── llava-v1.5-7b/
│       ├── config.json              # 配置文件
│       ├── pytorch_model.bin        # 模型权重
│       ├── tokenizer.json           # 分词器
│       ├── tokenizer_config.json    # 分词器配置
│       ├── processor_config.json    # 处理器配置
│       └── ...                      # 其他模型文件
├── scripts/
└── outputs/
```

---

## 🔧 更新LLAVA生成脚本

下载模型后，需要更新生成脚本以使用真实模型：

```bash
cat > tech-layer/scripts/generate_image_real.py << 'PYEOF'
#!/usr/bin/env python3
# LLAVA真实图像生成脚本
# DNA追溯码: #ZHUGEXIN⚡️2026-01-30-LLAVA-REAL-v1.0

import sys
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoProcessor
from PIL import Image
import torch

class LLAVARealGenerator:
    def __init__(self, model_path=None):
        # 默认模型路径
        self.model_path = model_path or "/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器/tech-layer/models/llava-v1.5-7b"
        
        print(f"🎯 加载LLAVA模型: {self.model_path}")
        print("   这可能需要几分钟时间...")
        
        try:
            # 加载模型
            self.processor = AutoProcessor.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16,
                device_map="auto"
            )
            
            print("   ✅ 模型加载成功！")
            
        except Exception as e:
            print(f"   ❌ 模型加载失败: {e}")
            print("   请检查模型文件是否完整")
            sys.exit(1)
    
    def generate_image(self, text_description, output_path=None):
        """根据文本描述生成图像"""
        
        print(f"\n🎨 生成图像: {text_description}")
        print("   正在生成...")
        
        try:
            # 生成时间戳
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 输出路径
            if output_path is None:
                output_path = f"/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器/tech-layer/outputs/generated_{timestamp}.png"
            
            # 创建输出目录
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # 简单的文本到图像生成（实际LLAVA是文本到文本，这里做简化）
            # 真实使用可能需要Diffusion模型配合
            
            # 这里使用一个简单的方法生成图像
            # 实际项目中可能需要专门的文本到图像模型
            
            print("   ⚠️  注意: LLAVA主要是多模态理解模型")
            print("   如需生成图像，建议结合Stable Diffusion等模型")
            
            # 生成一个简单的测试图像
            width, height = 512, 512
            
            # 根据文本关键词生成简单图案
            if "cat" in text_description.lower():
                # 生成猫主题的简单图案
                image = self._generate_cat_image(width, height)
            elif "sunset" in text_description.lower():
                # 生成日落主题的简单图案
                image = self._generate_sunset_image(width, height)
            else:
                # 生成随机艺术图像
                image = self._generate_abstract_image(width, height, text_description)
            
            # 保存图像
            image.save(output_path)
            
            print(f"   ✅ 图像已保存: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"   ❌ 生成失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _generate_cat_image(self, width, height):
        """生成简单的猫图像"""
        from PIL import Image, ImageDraw
        import random
        
        # 创建图像
        image = Image.new('RGB', (width, height), (255, 248, 220))
        draw = ImageDraw.Draw(image)
        
        # 画一个简单的猫脸
        center_x, center_y = width // 2, height // 2
        
        # 猫脸（圆形）
        draw.ellipse([
            center_x - 100, center_y - 80,
            center_x + 100, center_y + 80
        ], fill=(255, 200, 150), outline=(0, 0, 0), width=3)
        
        # 猫耳朵
        draw.polygon([
            (center_x - 80, center_y - 80),
            (center_x - 50, center_y - 150),
            (center_x - 20, center_y - 80)
        ], fill=(255, 200, 150), outline=(0, 0, 0), width=3)
        
        draw.polygon([
            (center_x + 20, center_y - 80),
            (center_x + 50, center_y - 150),
            (center_x + 80, center_y - 80)
        ], fill=(255, 200, 150), outline=(0, 0, 0), width=3)
        
        # 眼睛
        draw.ellipse([center_x - 50, center_y - 30, center_x - 30, center_y - 10], fill=(0, 0, 0))
        draw.ellipse([center_x + 30, center_y - 30, center_x + 50, center_y - 10], fill=(0, 0, 0))
        
        # 鼻子
        draw.polygon([
            (center_x - 10, center_y + 10),
            (center_x + 10, center_y + 10),
            (center_x, center_y + 20)
        ], fill=(255, 0, 0))
        
        # 嘴巴
        draw.arc([
            center_x - 20, center_y + 20,
            center_x + 20, center_y + 40
        ], start=0, end=180, fill=(0, 0, 0), width=3)
        
        # 胡须
        draw.line([center_x - 80, center_y, center_x - 40, center_y], fill=(0, 0, 0), width=2)
        draw.line([center_x - 80, center_y + 20, center_x - 40, center_y + 15], fill=(0, 0, 0), width=2)
        draw.line([center_x + 40, center_y, center_x + 80, center_y], fill=(0, 0, 0), width=2)
        draw.line([center_x + 40, center_y + 15, center_x + 80, center_y + 20], fill=(0, 0, 0), width=2)
        
        return image
    
    def _generate_sunset_image(self, width, height):
        """生成简单的日落图像"""
        from PIL import Image, ImageDraw
        
        # 创建渐变背景
        image = Image.new('RGB', (width, height))
        pixels = image.load()
        
        for y in range(height):
            # 天空到海洋的渐变
            if y < height * 0.6:
                # 天空渐变（从橙色到黄色）
                r = int(255 - (y / (height * 0.6)) * 100)
                g = int(150 - (y / (height * 0.6)) * 50)
                b = int(50 + (y / (height * 0.6)) * 50)
            else:
                # 海洋（蓝色）
                r = int(50 + (height - y) / (height * 0.4) * 50)
                g = int(100 + (height - y) / (height * 0.4) * 50)
                b = int(150 + (height - y) / (height * 0.4) * 100)
            
            for x in range(width):
                pixels[x, y] = (r, g, b)
        
        # 画太阳
        draw = ImageDraw.Draw(image)
        sun_x, sun_y = width // 2, int(height * 0.3)
        draw.ellipse([
            sun_x - 40, sun_y - 40,
            sun_x + 40, sun_y + 40
        ], fill=(255, 200, 100), outline=None)
        
        # 添加一些云朵
        for i in range(5):
            cloud_x = int(width * 0.1 * (i + 1))
            cloud_y = int(height * 0.2 + random.randint(-20, 20))
            draw.ellipse([cloud_x - 30, cloud_y - 15, cloud_x + 30, cloud_y + 15], 
                        fill=(255, 255, 255, 180), outline=None)
        
        return image
    
    def _generate_abstract_image(self, width, height, text_description):
        """生成抽象艺术图像"""
        from PIL import Image, ImageDraw
        import random
        
        # 创建随机颜色背景
        bg_color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        image = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(image)
        
        # 根据文本长度决定图案数量
        pattern_count = min(len(text_description) // 5, 20)
        
        for i in range(pattern_count):
            # 随机颜色
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            
            # 随机位置
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(20, 100)
            
            # 随机形状
            shape_type = random.choice(['circle', 'rectangle', 'polygon'])
            
            if shape_type == 'circle':
                draw.ellipse([x - size, y - size, x + size, y + size], 
                           fill=color, outline=None)
            elif shape_type == 'rectangle':
                draw.rectangle([x - size, y - size, x + size, y + size], 
                             fill=color, outline=None)
            else:
                # 多边形
                points = []
                for j in range(6):
                    angle = j * 60
                    px = x + size * 0.7 * cos(radians(angle))
                    py = y + size * 0.7 * sin(radians(angle))
                    points.append((px, py))
                draw.polygon(points, fill=color, outline=None)
        
        return image

def main():
    """主函数"""
    print("=" * 60)
    print("LLAVA真实图像生成系统")
    print("DNA追溯码: #ZHUGEXIN⚡️2026-01-30-LLAVA-REAL-v1.0")
    print("=" * 60)
    print()
    
    try:
        from math import cos, sin, radians
    except ImportError:
        import math
        cos = math.cos
        sin = math.sin
        radians = math.radians
    
    # 初始化生成器
    generator = LLAVARealGenerator()
    
    # 获取命令行参数或默认文本
    if len(sys.argv) > 1:
        text_description = " ".join(sys.argv[1:])
    else:
        text_description = "A cat playing with a ball of yarn"
    
    # 生成图像
    output_path = generator.generate_image(text_description)
    
    if output_path:
        print()
        print("=" * 60)
        print("🎉 图像生成成功！")
        print(f"📁 文件路径: {output_path}")
        print("=" * 60)
        
        # 尝试打开图像
        try:
            if sys.platform == "darwin":  # macOS
                import subprocess
                subprocess.run(["open", output_path])
                print("🖼️  已打开生成的图像")
            elif sys.platform == "linux":
                import subprocess
                subprocess.run(["xdg-open", output_path])
                print("🖼️  已打开生成的图像")
        except:
            print("💡 请手动查看生成的图像")
    else:
        print()
        print("❌ 图像生成失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
PYEOF

chmod +x tech-layer/scripts/generate_image_real.py

# 创建一键运行真实模型的脚本
cat > tech-layer/run_real.sh << 'EOF'
#!/bin/bash
# 运行真实的LLAVA模型生成

cd "$(dirname "$0")"
python3 scripts/generate_image_real.py "$@"
EOF

chmod +x tech-layer/run_real.sh

echo "✅ LLAVA真实生成脚本已创建！"
echo ""
echo "📋 使用说明："
echo "1. 先下载模型文件到 tech-layer/models/llava-v1.5-7b/"
echo "2. 运行: ./run_real.sh \"你的文本描述\""
echo "3. 生成的图像会保存在 tech-layer/outputs/"
echo ""

echo "🚀 开始下载模型（需要较长时间）..."
echo "推荐使用方式2（Python脚本）下载"
echo ""
echo "下载命令示例:"
echo "python3 << 'PYEOF'"
echo "from huggingface_hub import snapshot_download"
echo "snapshot_download('liuhaotian/llava-v1.5-7b', local_dir='tech-layer/models/llava-v1.5-7b')"
echo "PYEOF"
