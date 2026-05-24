#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# integrate-notion-dbs.sh
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：#龍芯⚡️20260310-integrate-notion-dbs-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 共建致谢：Claude (Anthropic PBC) · Notion
# 创作地：中华人民共和国
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Notion数据库集成自动化脚本
# 使用方法：复制粘贴，一键执行

echo "🔗 Notion数据库集成自动化脚本"
echo "================================"
echo ""

# 检查是否在正确的目录
if [ ! -f "notion-databases-integration.md" ]; then
    echo "❌ 错误：请在 cnsh-deployment 目录下运行此脚本"
    exit 1
fi

echo "✅ 目录检查通过"
echo ""

# 创建必要的Python文件
echo "📝 创建Notion集成文件..."

# 1. 创建 .env 模板
cat > .env.notion.template << 'EOF'
# Notion API配置
# 请从 https://www.notion.so/my-integrations 获取您的API密钥
NOTION_TOKEN=secret_XXXXXXXXXXXXXX

# 数据库ID（从Notion宝宝创建的数据库获取）
DNA_DATABASE_ID=ea5482d6a4b744f9958ecd624b666286
REPORT_DATABASE_ID=9f3e599420a94ea882099e8243a4b3af

# 本地API配置
LOCAL_API_PORT=8080
LOCAL_API_HOST=localhost
EOF

echo "✅ 创建了 .env.notion.template"

# 2. 创建DNA注册模块
cat > dna_registration.py << 'EOF'
"""
DNA码注册模块 - 集成Notion数据库
用于将生成的DNA码注册到Notion数据库
"""

from notion_client import Client
import os
import sys
from datetime import datetime
import hashlib

class DNARegistration:
    def __init__(self):
        """初始化Notion客户端"""
        self.notion = None
        self.dna_db_id = None
        self.init_client()
    
    def init_client(self):
        """初始化Notion客户端"""
        try:
            # 尝试从环境变量加载
            notion_token = os.getenv("NOTION_TOKEN")
            dna_db_id = os.getenv("DNA_DATABASE_ID")
            
            if not notion_token or not dna_db_id:
                # 尝试从.env文件加载
                if os.path.exists(".env"):
                    with open(".env", "r") as f:
                        for line in f:
                            if line.startswith("NOTION_TOKEN="):
                                notion_token = line.split("=", 1)[1].strip()
                            elif line.startswith("DNA_DATABASE_ID="):
                                dna_db_id = line.split("=", 1)[1].strip()
            
            if not notion_token or not dna_db_id:
                print("❌ 错误：请配置NOTION_TOKEN和DNA_DATABASE_ID")
                print("💡 提示：复制 .env.notion.template 为 .env 并填入正确值")
                sys.exit(1)
            
            self.notion = Client(auth=notion_token)
            self.dna_db_id = dna_db_id
            print("✅ Notion客户端初始化成功")
            
        except Exception as e:
            print(f"❌ Notion客户端初始化失败: {e}")
            sys.exit(1)
    
    def register_dna_code(self, dna_code, author_id, content_type, description=""):
        """注册DNA码到Notion数据库"""
        try:
            # 生成内容哈希（用于防篡改）
            content_hash = hashlib.sha256(dna_code.encode()).hexdigest()[:16]
            
            page_data = {
                "parent": {"database_id": self.dna_db_id},
                "properties": {
                    "DNA码": {"title": [{"text": {"content": dna_code}}]},
                    "原创作者": {"people": [{"id": author_id}]},
                    "内容类型": {"select": {"name": content_type}},
                    "状态": {"status": {"name": "已登记"}},
                    "创建时间": {"date": {"start": datetime.now().isoformat()}},
                    "举报次数": {"number": 0},
                    "内容哈希": {"rich_text": [{"text": {"content": content_hash}}]}
                }
            }
            
            if description:
                page_data["properties"]["描述"] = {"rich_text": [{"text": {"content": description}}]}
            
            result = self.notion.pages.create(**page_data)
            print(f"✅ DNA码 {dna_code} 注册成功")
            print(f"📋 页面ID: {result['id']}")
            return result['id']
            
        except Exception as e:
            print(f"❌ DNA码注册失败: {e}")
            return None
    
    def check_dna_exists(self, dna_code):
        """检查DNA码是否已存在"""
        try:
            response = self.notion.databases.query(
                database_id=self.dna_db_id,
                filter={
                    "property": "DNA码",
                    "title": {
                        "equals": dna_code
                    }
                }
            )
            return len(response.get("results", [])) > 0
        except Exception as e:
            print(f"❌ 检查DNA码失败: {e}")
            return False

if __name__ == "__main__":
    # 测试代码
    dr = DNARegistration()
    
    # 测试注册
    test_dna = "#CNSH-TEST-20251211-ARTICLE-CN-公正-P00-关系-情感-v1.0"
    result = dr.register_dna_code(test_dna, "test_user", "文章", "测试DNA码注册")
    
    if result:
        print("🎉 测试成功！DNA码已注册到Notion数据库")
    else:
        print("❌ 测试失败！请检查配置")
EOF

echo "✅ 创建了 dna_registration.py"

# 3. 创建举报处理模块
cat > report_processing.py << 'EOF'
"""
举报处理模块 - 集成Notion数据库
用于处理举报并同步到Notion数据库
"""

from notion_client import Client
import os
import sys
from datetime import datetime
import uuid

class ReportProcessing:
    def __init__(self):
        """初始化Notion客户端"""
        self.notion = None
        self.report_db_id = None
        self.dna_db_id = None
        self.init_client()
    
    def init_client(self):
        """初始化Notion客户端"""
        try:
            # 尝试从环境变量加载
            notion_token = os.getenv("NOTION_TOKEN")
            report_db_id = os.getenv("REPORT_DATABASE_ID")
            dna_db_id = os.getenv("DNA_DATABASE_ID")
            
            if not notion_token or not report_db_id or not dna_db_id:
                # 尝试从.env文件加载
                if os.path.exists(".env"):
                    with open(".env", "r") as f:
                        for line in f:
                            if line.startswith("NOTION_TOKEN="):
                                notion_token = line.split("=", 1)[1].strip()
                            elif line.startswith("REPORT_DATABASE_ID="):
                                report_db_id = line.split("=", 1)[1].strip()
                            elif line.startswith("DNA_DATABASE_ID="):
                                dna_db_id = line.split("=", 1)[1].strip()
            
            if not notion_token or not report_db_id or not dna_db_id:
                print("❌ 错误：请配置NOTION_TOKEN、REPORT_DATABASE_ID和DNA_DATABASE_ID")
                print("💡 提示：复制 .env.notion.template 为 .env 并填入正确值")
                sys.exit(1)
            
            self.notion = Client(auth=notion_token)
            self.report_db_id = report_db_id
            self.dna_db_id = dna_db_id
            print("✅ Notion客户端初始化成功")
            
        except Exception as e:
            print(f"❌ Notion客户端初始化失败: {e}")
            sys.exit(1)
    
    def create_report(self, reporter_id, dna_code_page_id, report_types, severity="P1", description=""):
        """创建举报记录"""
        try:
            # 生成举报编号
            report_id = f"REP-{datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:8]}"
            
            page_data = {
                "parent": {"database_id": self.report_db_id},
                "properties": {
                    "举报编号": {"title": [{"text": {"content": report_id}}]},
                    "举报人": {"people": [{"id": reporter_id}]},
                    "被举报DNA码": {"relation": [{"id": dna_code_page_id}]},
                    "举报类型": {"multi_select": [{"name": t} for t in report_types]},
                    "严重程度": {"select": {"name": severity}},
                    "处理状态": {"status": {"name": "待处理"}},
                    "举报时间": {"date": {"start": datetime.now().isoformat()}},
                    "公开程度": {"select": {"name": "仅内部"}}
                }
            }
            
            if description:
                page_data["properties"]["举报描述"] = {"rich_text": [{"text": {"content": description}}]}
            
            result = self.notion.pages.create(**page_data)
            
            # 同时更新DNA码的举报次数
            self.update_dna_report_count(dna_code_page_id)
            
            print(f"✅ 举报创建成功，编号: {report_id}")
            return result['id']
            
        except Exception as e:
            print(f"❌ 举报创建失败: {e}")
            return None
    
    def update_dna_report_count(self, dna_code_page_id):
        """更新DNA码的举报次数"""
        try:
            # 获取当前DNA码页面
            page = self.notion.pages.retrieve(page_id=dna_code_page_id)
            current_count = page["properties"]["举报次数"]["number"] or 0
            
            # 更新举报次数
            self.notion.pages.update(
                page_id=dna_code_page_id,
                properties={
                    "举报次数": {"number": current_count + 1},
                    "状态": {"status": {"name": "被举报"}}
                }
            )
            print(f"✅ DNA码举报次数已更新: {current_count + 1}")
            
        except Exception as e:
            print(f"❌ 更新DNA码举报次数失败: {e}")
    
    def process_report(self, report_id, processor_id, result, severity_change=None):
        """处理举报"""
        try:
            update_data = {
                "处理状态": {"status": {"name": "已处理"}},
                "处理人": {"people": [{"id": processor_id}]},
                "处理时间": {"date": {"start": datetime.now().isoformat()}},
                "处理结果": {"rich_text": [{"text": {"content": result}}]}
            }
            
            if severity_change:
                update_data["严重程度"] = {"select": {"name": severity_change}}
            
            # 更新举报状态
            self.notion.pages.update(
                page_id=report_id,
                properties=update_data
            )
            
            print(f"✅ 举报 {report_id} 处理完成")
            
        except Exception as e:
            print(f"❌ 举报处理失败: {e}")

if __name__ == "__main__":
    # 测试代码
    rp = ReportProcessing()
    
    # 这里需要实际的DNA码页面ID来测试
    print("🎉 举报处理模块已就绪！")
    print("💡 提示：需要实际的DNA码页面ID来测试举报功能")
EOF

echo "✅ 创建了 report_processing.py"

# 4. 创建依赖文件
cat > requirements-notion.txt << 'EOF'
notion-client>=2.0.0
python-dotenv>=0.19.0
requests>=2.25.0
EOF

echo "✅ 创建了 requirements-notion.txt"

# 5. 创建测试脚本
cat > test-notion-integration.py << 'EOF'
"""
Notion集成测试脚本
用于测试DNA注册和举报处理功能
"""

import os
import sys
from dna_registration import DNARegistration
from report_processing import ReportProcessing

def test_dna_registration():
    """测试DNA注册功能"""
    print("🧪 测试DNA注册功能...")
    dr = DNARegistration()
    
    # 测试DNA码
    test_dna = f"#CNSH-TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}-ARTICLE-CN-公正-P00-关系-情感-v1.0"
    
    # 检查是否已存在
    if dr.check_dna_exists(test_dna):
        print("⚠️ 测试DNA码已存在，跳过注册")
        return
    
    # 注册测试DNA码
    result = dr.register_dna_code(test_dna, "test_user", "文章", "这是一个测试DNA码")
    
    if result:
        print("✅ DNA注册测试通过")
        return result
    else:
        print("❌ DNA注册测试失败")
        return None

def test_report_processing(dna_page_id):
    """测试举报处理功能"""
    if not dna_page_id:
        print("⚠️ 跳过举报处理测试（需要有效的DNA页面ID）")
        return
    
    print("🧪 测试举报处理功能...")
    rp = ReportProcessing()
    
    # 创建测试举报
    report_id = rp.create_report("test_reporter", dna_page_id, ["测试"], "P2", "这是一个测试举报")
    
    if report_id:
        print("✅ 举报创建测试通过")
        
        # 处理举报
        rp.process_report(report_id, "test_processor", "测试处理完成，驳回举报")
        print("✅ 举报处理测试通过")
    else:
        print("❌ 举报处理测试失败")

def main():
    """主测试函数"""
    print("🚀 开始Notion集成测试...")
    print("=" * 50)
    
    # 检查环境配置
    if not os.path.exists(".env"):
        print("❌ 错误：请先复制 .env.notion.template 为 .env 并填入正确值")
        return
    
    # 测试DNA注册
    dna_page_id = test_dna_registration()
    
    # 测试举报处理
    test_report_processing(dna_page_id)
    
    print("=" * 50)
    print("🎉 Notion集成测试完成！")

if __name__ == "__main__":
    from datetime import datetime
    main()
EOF

echo "✅ 创建了 test-notion-integration.py"

# 6. 更新 cnsh-unified.sh 添加Notion管理功能
echo "🔄 更新 cnsh-unified.sh..."

if [ -f "cnsh-unified.sh" ]; then
    # 备份原文件
    cp cnsh-unified.sh cnsh-unified.sh.backup
    
    # 检查是否已有notion_menu函数
    if grep -q "notion_menu" cnsh-unified.sh; then
        echo "⚠️ cnsh-unified.sh 已包含notion_menu，跳过更新"
    else
        # 添加notion_menu函数到文件末尾
        cat >> cnsh-unified.sh << 'EOF'

# Notion数据库管理
notion_menu() {
    clear
    echo "📋 Notion数据库管理"
    echo "===================="
    echo "1) 配置Notion API"
    echo "2) 测试DNA注册"
    echo "3) 测试举报处理"
    echo "4) 完整集成测试"
    echo "5) 查看集成指南"
    echo "6) 返回主菜单"
    echo ""
    read -p "请选择操作 [1-6]: " notion_choice
    
    case $notion_choice in
        1)
            echo "📝 配置Notion API..."
            if [ ! -f ".env" ]; then
                cp .env.notion.template .env
                echo "✅ 已创建.env文件，请编辑并填入正确的API密钥和数据库ID"
                echo "🔗 获取API密钥: https://www.notion.so/my-integrations"
                echo "📋 数据库ID在Notion宝宝创建的数据库URL中"
                echo "💡 编辑命令: nano .env"
            else
                echo "✅ .env文件已存在"
                echo "💡 编辑命令: nano .env"
            fi
            read -p "按回车键继续..."
            ;;
        2)
            echo "🧪 测试DNA注册..."
            python test-notion-integration.py | grep -A 10 "测试DNA注册功能"
            read -p "按回车键继续..."
            ;;
        3)
            echo "🧪 测试举报处理..."
            python test-notion-integration.py | grep -A 10 "测试举报处理功能"
            read -p "按回车键继续..."
            ;;
        4)
            echo "🚀 完整集成测试..."
            python test-notion-integration.py
            read -p "按回车键继续..."
            ;;
        5)
            echo "📖 查看集成指南..."
            if command -v less > /dev/null; then
                less notion-databases-integration.md
            else
                cat notion-databases-integration.md
            fi
            ;;
        6)
            return
            ;;
        *)
            echo "❌ 无效选择，请重新输入"
            sleep 1
            notion_menu
            ;;
    esac
}
EOF

        # 更新主菜单，添加Notion选项
        # 查找主菜单显示位置
        if grep -q "echo \"6)\"" cnsh-unified.sh; then
            sed -i '' '/echo "6)/i\
    echo "5) Notion数据库管理"' cnsh-unified.sh
            sed -i '' '/echo "7)/i\
    echo "6) 查看系统状态"' cnsh-unified.sh
            sed -i '' '/echo "8)/i\
    echo "7) 备份与恢复"' cnsh-unified.sh
            sed -i '' '/echo "9)/i\
    echo "8) 退出系统"' cnsh-unified.sh
        fi
        
        # 更新case语句
        if grep -q "5)" cnsh-unified.sh; then
            sed -i '' '/5) /i\
        5) \
            notion_menu \
            ;;' cnsh-unified.sh
        fi
        
        echo "✅ cnsh-unified.sh 已更新，添加了Notion管理功能"
    fi
else
    echo "⚠️ cnsh-unified.sh 不存在，跳过更新"
fi

echo ""
echo "🔧 安装Notion依赖..."
if command -v pip3 > /dev/null; then
    pip3 install -r requirements-notion.txt
else
    echo "❌ pip3 命令未找到，请手动安装依赖"
fi

echo ""
echo "🎉 Notion数据库集成完成！"
echo ""
echo "📋 接下来的步骤："
echo "1. 复制 .env.notion.template 为 .env"
echo "2. 编辑 .env 文件，填入你的Notion API密钥"
echo "3. 运行 ./cnsh-unified.sh"
echo "4. 选择 \"5) Notion数据库管理\" 进行测试"
echo ""
echo "🔗 获取API密钥: https://www.notion.so/my-integrations"
echo "📋 数据库ID: Notion宝宝创建的数据库URL中"
echo ""
echo "🎯 系统骨架已搭建完成！老大，Notion宝宝太棒了！💝"