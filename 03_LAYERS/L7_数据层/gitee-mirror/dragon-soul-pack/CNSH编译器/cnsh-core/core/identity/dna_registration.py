#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA追溯: #ZHUGEXIN⚡️20260302-CNSH-DNA_REGISTRATION-PY-v0.1.0
# 作者: Lucky·UID9622 (諸葛鑫)
# GPG指紋: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 狀態: 演進中
# 镜像来源: https://gitee.com/uid9622/cnsh/raw/main/core/identity/dna_registration.py
"""
DNA码注册模块 - 集成Notion数据库
"""

from notion_client import Client
import os
import sys
from datetime import datetime
import hashlib

class DNARegistration:
    def __init__(self):
        self.notion = None
        self.dna_db_id = None
        self.init_client()
    
    def init_client(self):
        try:
            notion_token = os.getenv("NOTION_TOKEN")
            dna_db_id = os.getenv("DNA_DATABASE_ID")
            
            if not notion_token or not dna_db_id:
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
        try:
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
        try:
            response = self.notion.databases.query(
                database_id=self.dna_db_id,
                filter={"property": "DNA码", "title": {"equals": dna_code}}
            )
            return len(response.get("results", [])) > 0
        except Exception as e:
            print(f"❌ 检查DNA码失败: {e}")
            return False

if __name__ == "__main__":
    dr = DNARegistration()
    test_dna = "#CNSH-TEST-20251211-ARTICLE-CN-公正-P00-关系-情感-v1.0"
    result = dr.register_dna_code(test_dna, "test_user", "文章", "测试DNA码注册")
    if result:
        print("🎉 测试成功！DNA码已注册到Notion数据库")
    else:
        print("❌ 测试失败！请检查配置")
