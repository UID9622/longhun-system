#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
test-notion-integration.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
Licensed under the Apache License, Version 2.0

作者：UID9622 诸葛鑫（龍芯北辰）
创作地：中华人民共和国
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导：曾仕强老师（永恒显示）
DNA追溯码：#龍芯⚡️20260310-test-notion-integration-v1.0
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。

献礼：新中国成立77周年（1949-2026）· 丙午马年
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

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
