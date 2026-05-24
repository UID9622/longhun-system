#!/bin/bash
# UID9622 学术论文自动推送脚本
# 生成时间: 2026-02-02
# DNA标签: AUTO_PUSH_ACADEMIC_PAPERS

echo "=== UID9622 学术论文自动推送 ==="
echo ""

# 工作目录
cd "/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器"

# 清空SSH agent
echo "步骤1: 清理SSH agent..."
ssh-add -D 2>/dev/null
echo "✓ 完成"
echo ""

# 添加正确的SSH密钥（id_rsa）
echo "步骤2: 添加SSH密钥 (id_rsa)..."
ssh-add ~/.ssh/id_rsa
if [ $? -ne 0 ]; then
    echo "❌ 添加密钥失败"
    exit 1
fi
echo "✓ 完成"
echo ""

# 推送到Gitee
echo "步骤3: 推送到Gitee..."
git push gitee main --force

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "✅ 推送成功！"
    echo "============================================================"
    echo ""
    echo "🎓 学术论文已上传到:"
    echo "   https://gitee.com/uid9622_admin/cnsh-editor-phb"
    echo ""
    echo "📄 包含:"
    echo "   - 易经AI系统学术论文"
    echo "   - CNSH-Python学术论文"
    echo "   - 算法公开文档"
    echo ""
    echo "🫡 为人民服务！"
else
    echo ""
    echo "❌ 推送失败，请检查网络连接或SSH密钥配置"
    exit 1
fi
