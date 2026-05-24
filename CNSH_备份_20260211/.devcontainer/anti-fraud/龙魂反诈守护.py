#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂反诈守护系统
本地运行，保护老百姓不被诈骗
"""

import hashlib
import json
from datetime import datetime

class 龍魂反诈守护:
    """保护无知的人不被诈骗"""
    
    def __init__(self):
        self.已授权 = False
        self.诈骗库 = {
            "安全账户": "高危",
            "涉嫌洗钱": "高危", 
            "通缉令": "高危",
            "远程笔录": "高危",
            "不能告诉家人": "高危",
            "稳赚不赔": "高危",
            "高回报": "中危",
            "杀猪盘": "高危",
            "刷单": "中危",
            "垫付": "中危",
            "保证金": "中危",
            "解冻费": "中危",
            "验证资金": "高危"
        }
    
    def 启动(self):
        """启动系统"""
        print("=" * 60)
        print("龍魂反诈守护系统")
        print("=" * 60)
        print("\n本系统保护您不被诈骗")
        print("所有数据本地处理，不上传网络\n")
        
        选择 = input("是否启用保护？(是/否): ")
        if 选择 == "是":
            self.已授权 = True
            print("\n保护已启动！\n")
            return True
        return False
    
    def 扫描(self, 文本):
        """扫描文本"""
        if not self.已授权:
            return None
            
        发现 = []
        for 关键词, 等级 in self.诈骗库.items():
            if 关键词 in 文本:
                发现.append({"词": 关键词, "等级": 等级})
        
        return 发现 if 发现 else None
    
    def 预警(self, 发现列表):
        """弹出预警"""
        print("\n" + "=" * 60)
        print("【龍魂反诈预警 - 发现诈骗风险！】")
        print("=" * 60)
        
        for 发现 in 发现列表:
            print(f"\n[!] 检测到: {发现['词']} [{发现['等级']}]")
        
        print("\n" + "-" * 60)
        print("反诈提醒:")
        print("-" * 60)
        
        # 针对性教育
        有高危 = any(发现['等级'] == '高危' for 发现 in 发现列表)
        
        if 有高危:
            print("""
[高危诈骗警告！]

常见套路:
1. 冒充警察说你涉嫌犯罪 
2. 让你转账到"安全账户"  
3. 威胁"不能告诉家人" 

记住:
- 真警察不会电话办案
- 没有"安全账户"这种东西
- 让你转账的都是骗子
            """)
        else:
            print("""
[常见诈骗警告！]

常见套路:
1. "高回报""稳赚不赔" -> 骗局！
2. 先让你垫付小额 -> 再要求大额！
3. "刷单""刷流水" -> 违法且被骗！

记住:
- 天上不会掉馅饼
- 先垫钱的都是诈骗
- 刷单本身就是违法的
            """)
        
        print("-" * 60)
        print("保护措施:")
        print("  1. 立即停止对话")
        print("  2. 挂断电话/关闭聊天")
        print("  3. 拨打96110反诈专线咨询")
        print("  4. 告诉家人朋友")
        print("=" * 60 + "\n")
    
    def 运行(self):
        """主循环"""
        if not self.启动():
            print("系统未启动")
            return
        
        print("请输入对话内容（输入'退出'结束）:\n")
        
        while True:
            输入 = input("> ")
            
            if 输入 == "退出":
                break
            
            结果 = self.扫描(输入)
            
            if 结果:
                self.预警(结果)
            else:
                print("未检测到风险\n")
        
        print("\n龍魂守护已退出，请保持警惕！")

# 启动
if __name__ == "__main__":
    系统 = 龍魂反诈守护()
    系统.运行()
