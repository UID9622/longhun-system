#!/bin/bash

# CNSH Core 最终推送脚本
# 请先在 Gitee 上创建仓库后再执行此脚本

echo "=========================================="
echo "CNSH Core - 国产本地AI知识管理系统"
echo "=========================================="
echo ""
echo "重要提示：请先在 Gitee 上创建仓库后再执行此脚本！"
echo "1. 访问 https://gitee.com"
echo "2. 登录并点击 '+' → '新建仓库'"
echo "3. 仓库名称：CNSH-National-Reference"
echo "4. 设为公开仓库，不初始化 README"
echo ""

# 询问用户是否已创建仓库
read -p "是否已在 Gitee 上创建仓库？(y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "请先在 Gitee 上创建仓库，然后再执行此脚本。"
    exit 1
fi

# 获取用户名
echo ""
read -p "请输入您的 Gitee 用户名: " username

if [ -z "$username" ]; then
    echo "错误：用户名不能为空"
    exit 1
fi

# 进入项目目录
cd "$(dirname "$0")"

echo ""
echo "=========================================="
echo "当前项目状态："
echo "=========================================="
git status

echo ""
echo "=========================================="
echo "提交历史："
echo "=========================================="
git log --oneline

echo ""
echo "=========================================="
echo "配置远程仓库地址："
echo "=========================================="

# 删除旧的远程仓库配置
git remote remove origin

# 添加新的远程仓库地址
git remote add origin https://gitee.com/$username/CNSH-National-Reference.git

echo "远程仓库地址已配置为：https://gitee.com/$username/CNSH-National-Reference.git"

echo ""
echo "=========================================="
echo "推送代码到 Gitee..."
echo "=========================================="

# 推送代码
if git push -u origin main; then
    echo ""
    echo "✅ 代码推送成功！"
    echo ""
    echo "=========================================="
    echo "创建版本标签..."
    echo "=========================================="
    
    # 创建版本标签
    git tag -a v1.0.0 -m "CNSH Core v1.0.0 - 初始发布版本"
    git push origin v1.0.0
    
    echo "✅ 版本标签创建成功！"
    echo ""
    echo "=========================================="
    echo "🎉 恭喜！CNSH Core 已成功部署到 Gitee！"
    echo "=========================================="
    echo ""
    echo "📋 接下来建议您："
    echo "1. 访问您的仓库：https://gitee.com/$username/CNSH-National-Reference"
    echo "2. 添加仓库封面和描述"
    echo "3. 设置关键词标签：数字人民币, 本地AI, 国产化, 元宇宙, 北辰协议"
    echo "4. 申请 Gitee GVP 项目"
    echo "5. 在社区分享您的项目"
    echo ""
    echo "为国家数字主权建设贡献力量！🇨🇳"
    echo ""
    echo "【北辰-B 协议 · 国产通道校验 UID9622】"
else
    echo ""
    echo "❌ 推送失败！请检查："
    echo "1. 网络连接是否正常"
    echo "2. 仓库地址是否正确"
    echo "3. 是否有推送权限"
    echo ""
    echo "请参考 PUSH_COMMANDS.md 文件进行手动推送。"
    exit 1
fi