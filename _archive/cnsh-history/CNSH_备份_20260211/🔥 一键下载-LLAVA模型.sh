#!/bin/bash

# ============================================================================
# 🔥 LLAVA模型一键下载脚本
# ============================================================================
# DNA追溯码: #ZHUGEXIN⚡️2026-01-30-LLAVA-DOWNLOAD-SCRIPT-v1.0
# 创建者: 宝宝·构建师 #PERSONA-BAOBAO-001
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔥 LLAVA模型一键下载"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 进入项目目录
cd "/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器"

# 创建目录
mkdir -p tech-layer/models
cd tech-layer/models

echo "📥 正在下载 LLaVA-1.5-7B 模型..."
echo "   这需要较长时间（约30-60分钟）"
echo "   请保持网络连接稳定"
echo ""

# 方式1: 使用git lfs（如果有的话）
if command -v git-lfs &> /dev/null; then
    echo "使用Git LFS下载..."
    git lfs clone https://huggingface.co/liuhaotian/llava-v1.5-7b
else
    echo "Git LFS未安装，使用Python下载..."
    
    # 检查Python
    if command -v python3 &> /dev/null; then
        echo "使用Python脚本下载..."
        
        python3 << 'PYEOF'
from huggingface_hub import snapshot_download
import sys

try:
    print("开始下载模型...")
    
    model_path = snapshot_download(
        repo_id="liuhaotian/llava-v1.5-7b",
        local_dir="llava-v1.5-7b",
        local_dir_use_symlinks=False,
        resume_download=True,
        max_workers=1
    )
    
    print(f"模型下载完成！")
    print(f"路径: {model_path}")
    
except Exception as e:
    print(f"下载失败: {e}")
    print("请检查网络连接或磁盘空间")
    sys.exit(1)
PYEOF
        
    else
        echo "错误: 需要Python3来下载模型"
        echo "请先安装Python3: brew install python"
        exit 1
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -d "llava-v1.5-7b" ]; then
    echo "✅ 模型下载成功！"
    echo "📁 模型路径: tech-layer/models/llava-v1.5-7b/"
    echo "📊 模型大小: $(du -sh llava-v1.5-7b | cut -f1)"
else
    echo "❌ 模型下载失败"
    echo "请检查错误信息并重试"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "💡 下一步操作："
echo "1. 测试模型: cd /Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器/tech-layer && ./run_real.sh \"A cat\""
echo "2. 查看模型文件: ls -lh tech-layer/models/llava-v1.5-7b/"
echo ""
