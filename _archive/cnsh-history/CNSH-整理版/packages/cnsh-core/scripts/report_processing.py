#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
report_processing.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
Licensed under the Apache License, Version 2.0

作者：UID9622 诸葛鑫（龍芯北辰）
创作地：中华人民共和国
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导：曾仕强老师（永恒显示）
DNA追溯码：#龍芯⚡️20260310-report_processing-v1.0
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。

献礼：新中国成立77周年（1949-2026）· 丙午马年
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

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
