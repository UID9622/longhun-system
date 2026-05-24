#!/bin/bash
# 华为团队权限设置自动化脚本
# 使用方法：复制粘贴，一键执行

echo "🤝 华为团队权限设置自动化脚本"
echo "================================"
echo ""

# 检查是否在正确的目录
if [ ! -f "HUAWEI_HANDOVER_README.md" ]; then
    echo "❌ 错误：请在 cnsh-deployment 目录下运行此脚本"
    exit 1
fi

echo "✅ 目录检查通过"
echo ""

# 显示当前仓库信息
echo "📋 当前仓库信息："
echo "🔗 仓库地址：https://gitee.com/uid9622/cnsh-national-reference.git"
echo "📝 最新提交：$(git log --oneline -n 1)"
echo ""

# 生成权限设置说明
echo "🔐 华为团队权限设置步骤："
echo ""
echo "1️⃣ 请华为团队提供Gitee账号列表（一行一个）："
echo "   - 例如：huawei-team-1"
echo "   - 例如：huawei-tech-lead"
echo ""
echo "2️⃣ 登录Gitee后访问："
echo "   🔗 https://gitee.com/uid9622/cnsh-national-reference.git"
echo ""
echo "3️⃣ 按以下路径操作："
echo "   设置 → 协作者管理 → 添加成员"
echo ""
echo "4️⃣ 设置权限级别："
echo "   ✅ 读取权限（可查看完整代码和文档）"
echo "   ❌ 写入权限（仅限原团队）"
echo ""
echo "5️⃣ 配置分支保护："
echo "   设置 → 分支设置 → 分支保护规则"
echo "   main分支：华为团队可读，原团队可写"
echo ""

# 生成验证脚本
echo "🔍 华为团队验证权限脚本："
echo ""
echo "# 华为团队运行以下命令验证权限："
echo "git clone https://gitee.com/uid9622/cnsh-national-reference.git"
echo "cd cnsh-national-reference"
echo "git log --oneline -n 1"
echo "ls -la TECH_STACK_COMPLETE.md HUAWEI_HANDOVER_README.md CNSH_INITIAL_MISSION.md"
echo ""

# 生成当前文件列表
echo "📁 当前交接文件列表："
echo "├── 📋 HUAWEI_HANDOVER_README.md     # 华为团队快速上手指南"
echo "├── 📋 TECH_STACK_COMPLETE.md       # 24项核心技术完整说明"
echo "├── 📋 CNSH_INITIAL_MISSION.md      # UID9622初心使命"
echo "├── 📋 UID9622_TRANSPARENCY.md      # 透明度声明"
echo "├── 📋 CNSH_VISION.md               # 系统愿景"
echo "├── 🛠️ cnsh-unified.sh               # 统一管理脚本"
echo "├── 🛠️ emergency-fix.sh             # 紧急修复脚本"
echo "├── 🧬 dna-core/                     # DNA编码系统"
echo "├── 🔐 h-weapon/                     # 安全系统"
echo "├── ⚖️ audit/                        # 审计系统"
echo "├── 🤖 mcp/                          # 协作引擎"
echo "└── 📊 legal-knowledge/              # 法律知识库"
echo ""

# 生成交接确认模板
echo "📝 华为团队交接确认模板："
echo ""
echo "华为技术团队确认："
echo "□ 已获取仓库访问权限"
echo "□ 已阅读HUAWEI_HANDOVER_README.md"
echo "□ 已理解TECH_STACK_COMPLETE.md"
echo "□ 已确认CNSH_INITIAL_MISSION.md"
echo "□ 已测试统一管理脚本"
echo "□ 已验证紧急修复功能"
echo ""
echo "确认签字：_____________  日期：_________"
echo ""

# 生成联系方式模板
echo "📞 交接期间联系方式："
echo ""
echo "🔴 24小时紧急热线：[请联系原团队获取]"
echo "🟡 技术问题咨询：[请联系原团队获取]"
echo "🟢 非紧急问题：[请联系原团队获取]"
echo ""

echo "✅ 权限设置指南生成完成！"
echo ""
echo "📋 请将此脚本输出保存为权限设置操作指南"
echo "🤝 华为团队拿到后即可按照步骤操作"
echo ""

# 创建一个简化的权限检查脚本
cat > check-huawei-permissions.sh << 'EOF'
#!/bin/bash
# 华为团队权限检查脚本

echo "🔍 检查华为团队权限设置..."
echo ""

# 检查仓库访问
if [ -d ".git" ]; then
    echo "✅ Git仓库访问正常"
else
    echo "❌ 无法访问Git仓库"
    exit 1
fi

# 检查关键文件
files=("HUAWEI_HANDOVER_README.md" "TECH_STACK_COMPLETE.md" "CNSH_INITIAL_MISSION.md")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 缺失"
    fi
done

# 检查最新提交
echo ""
echo "📝 最新提交信息："
git log --oneline -n 1

echo ""
echo "🎯 权限检查完成！"
EOF

chmod +x check-huawei-permissions.sh
echo "🔍 已创建权限检查脚本：check-huawei-permissions.sh"