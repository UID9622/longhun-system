#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH字体引擎·统一管理系统
DNA追溯码: #龍芯⚡️2026-02-09-CNSH-ENGINE-MANAGER-v1.0
创建者: 诸葛鑫（Lucky）｜UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import json
import os
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod


# =====================================================
# 第一部分：引擎基类（所有引擎的父类）
# =====================================================

class CNSH引擎基类_UID9622(ABC):
    """CNSH引擎基类 - 所有CNSH引擎都应该继承这个类"""
    
    def __init__(self):
        self.字元集_cnsh9622 = {}
        self.审计结果_cnsh9622 = {}
        self.工程信息_cnsh9622 = {}
        self.版本号_cnsh9622 = "0.0.0"
        self.引擎名称_cnsh9622 = "基础引擎"
    
    @abstractmethod
    def 载入_cnsh数据_cnsh龍魂_v1(self, 路径_cnsh9622: str):
        """载入CNSH数据文件（必须实现）"""
        pass
    
    @abstractmethod
    def 执行三色审计_cnsh龍魂_v1(self):
        """执行三色审计（必须实现）"""
        pass
    
    @abstractmethod
    def 执行渲染_cnsh龍魂_v1(self, 输出目录_cnsh9622: str):
        """执行渲染（必须实现）"""
        pass
    
    def 获取版本_cnsh9622(self) -> str:
        """获取引擎版本"""
        return self.版本号_cnsh9622
    
    def 获取引擎名称_cnsh9622(self) -> str:
        """获取引擎名称"""
        return self.引擎名称_cnsh9622
    
    def 获取工程信息_cnsh9622(self) -> Dict:
        """获取工程信息"""
        return self.工程信息_cnsh9622


# =====================================================
# 第二部分：V0001 基础引擎
# =====================================================

class CNSH基础引擎_V0001_UID9622(CNSH引擎基类_UID9622):
    """V0001 基础引擎"""
    
    def __init__(self):
        super().__init__()
        self.版本号_cnsh9622 = "0.0.1"
        self.引擎名称_cnsh9622 = "基础引擎"
    
    def 载入_cnsh数据_cnsh龍魂_v1(self, 路径_cnsh9622: str):
        with open(路径_cnsh9622, "r", encoding="utf-8") as f:
            数据 = json.load(f)
        self.字元集_cnsh9622 = 数据["字符集_cnsh9622"]
        print(f"✅ [{self.引擎名称_cnsh9622}] 加载字元集: {list(self.字元集_cnsh9622.keys())}")
    
    def 执行三色审计_cnsh龍魂_v1(self):
        """基础引擎没有审计功能"""
        print(f"⚠️ [{self.引擎名称_cnsh9622}] 基础版无审计功能")
    
    def 输出SVG_cnsh龍魂_v1(self, 字符: str, 输出路径_cnsh9622: str):
        if 字符 not in self.字元集_cnsh9622:
            print(f"❌ 字符不存在: {字符}")
            return
        
        笔画 = self.字元集_cnsh9622[字符]["笔画路径_cnsh9622"]
        路径 = ""
        当前点 = None
        
        for 动作 in 笔画:
            if 动作["类型"] == "移动到":
                x, y = 动作["坐标"]
                路径 += f"M {x} {y} "
                当前点 = (x, y)
            elif 动作["类型"] == "直线段":
                x, y = 动作["终点"]
                路径 += f"L {x} {y} "
                当前点 = (x, y)
            elif 动作["类型"] == "三次曲线":
                P1, P2, P3 = 动作["控制点"]
                路径 += f"C {P1[0]} {P1[1]}, {P2[0]} {P2[1]}, {P3[0]} {P3[1]} "
                当前点 = P3
        
        svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <rect width="100%" height="100%" fill="white"/>
  <path d="{路径}" fill="none" stroke="black" stroke-width="8" 
        stroke-linecap="round" stroke-linejoin="round"/>
  <text x="10" y="20" font-size="12" fill="#aaa">V0001 - {字符}</text>
</svg>"""
        
        with open(输出路径_cnsh9622, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"✅ [{self.引擎名称_cnsh9622}] {字符} → {输出路径_cnsh9622}")
    
    def 执行渲染_cnsh龍魂_v1(self, 输出目录_cnsh9622: str):
        os.makedirs(输出目录_cnsh9622, exist_ok=True)
        for 字符 in self.字元集_cnsh9622:
            输出路径 = os.path.join(输出目录_cnsh9622, f"CNSH_{字符}_v0001.svg")
            self.输出SVG_cnsh龍魂_v1(字符, 输出路径)


# =====================================================
# 第三部分：V0002 批量引擎
# =====================================================

class CNSH批量引擎_V0002_UID9622(CNSH引擎基类_UID9622):
    """V0002 批量引擎"""
    
    def __init__(self):
        super().__init__()
        self.版本号_cnsh9622 = "0.0.2"
        self.引擎名称_cnsh9622 = "批量引擎"
    
    def 载入_cnsh数据_cnsh龍魂_v1(self, 路径_cnsh9622: str):
        with open(路径_cnsh9622, "r", encoding="utf-8") as f:
            数据 = json.load(f)
        self.字元集_cnsh9622 = 数据["字符集_cnsh9622"]
        print(f"✅ [{self.引擎名称_cnsh9622}] 已加载 {len(self.字元集_cnsh9622)} 个字元")
    
    def 执行三色审计_cnsh龍魂_v1(self):
        print(f"⚠️ [{self.引擎名称_cnsh9622}] 批量版无审计功能")
    
    def 执行渲染_cnsh龍魂_v1(self, 输出目录_cnsh9622: str):
        print(f"\n🎯 [{self.引擎名称_cnsh9622}] 开始批量渲染...")
        os.makedirs(输出目录_cnsh9622, exist_ok=True)
        
        for i, 字符 in enumerate(self.字元集_cnsh9622, 1):
            笔画 = self.字元集_cnsh9622[字符]["笔画路径_cnsh9622"]
            路径 = ""
            当前点 = None
            
            for 动作 in 笔画:
                if 动作["类型"] == "移动到":
                    x, y = 动作["坐标"]
                    路径 += f"M {x} {y} "
                    当前点 = (x, y)
                elif 动作["类型"] == "直线段":
                    x, y = 动作["终点"]
                    路径 += f"L {x} {y} "
                    当前点 = (x, y)
                elif 动作["类型"] == "三次曲线":
                    P1, P2, P3 = 动作["控制点"]
                    路径 += f"C {P1[0]} {P1[1]}, {P2[0]} {P2[1]}, {P3[0]} {P3[1]} "
                    当前点 = P3
            
            svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <rect width="100%" height="100%" fill="white"/>
  <path d="{路径}" fill="none" stroke="black" stroke-width="8" 
        stroke-linecap="round" stroke-linejoin="round"/>
  <text x="10" y="20" font-size="12" fill="#aaa">V0002 - {字符}</text>
</svg>"""
            
            输出路径 = os.path.join(输出目录_cnsh9622, f"CNSH_{字符}_v0002.svg")
            with open(输出路径, "w", encoding="utf-8") as f:
                f.write(svg)
            
            print(f"  [{i}/{len(self.字元集_cnsh9622)}] ✅ {字符} → {输出路径}")
        
        print(f"🎉 [{self.引擎名称_cnsh9622}] 批量渲染完成！")


# =====================================================
# 第四部分：V0003 审计引擎
# =====================================================

class CNSH审计引擎_V0003_UID9622(CNSH引擎基类_UID9622):
    """V0003 审计引擎"""
    
    def __init__(self):
        super().__init__()
        self.版本号_cnsh9622 = "0.0.3"
        self.引擎名称_cnsh9622 = "审计引擎"
    
    def 载入_cnsh数据_cnsh龍魂_v1(self, 路径_cnsh9622: str):
        with open(路径_cnsh9622, "r", encoding="utf-8") as f:
            数据 = json.load(f)
        self.字元集_cnsh9622 = 数据["字符集_cnsh9622"]
        self.审计结果_cnsh9622 = 数据.get("三色审计_cnsh9622", {})
        self.工程信息_cnsh9622 = {
            "工程名称": 数据.get("工程名称", "未命名"),
            "DNA追溯码": 数据.get("DNA追溯码", "无"),
            "阶段标识": 数据.get("阶段标识", "无")
        }
        print(f"✅ [{self.引擎名称_cnsh9622}] 已加载工程: {self.工程信息_cnsh9622['工程名称']}")
        print(f"   DNA: {self.工程信息_cnsh9622['DNA追溯码']}")
    
    def 执行三色审计_cnsh龍魂_v1(self):
        print(f"\n🎯 [{self.引擎名称_cnsh9622}] 开始执行三色审计...")
        审计通过 = True
        
        for 颜色, 审计项 in self.审计结果_cnsh9622.items():
            结果 = "✅" if 审计项["结果"] == "通过" else "❌"
            print(f"\n{结果} 【{颜色}色审计】")
            for 检查 in 审计项["检查项"]:
                print(f"   • {检查}")
            
            if 审计项["结果"] != "通过":
                审计通过 = False
        
        if not 审计通过:
            raise RuntimeError(f"❌ [{self.引擎名称_cnsh9622}] 三色审计未通过，拒绝渲染")
        
        print(f"\n🟢 [{self.引擎名称_cnsh9622}] 三色审计全部通过，准许渲染")
    
    def 执行渲染_cnsh龍魂_v1(self, 输出目录_cnsh9622: str):
        print(f"\n🎯 [{self.引擎名称_cnsh9622}] 开始渲染 {len(self.字元集_cnsh9622)} 个字元...")
        os.makedirs(输出目录_cnsh9622, exist_ok=True)
        
        for 字符 in self.字元集_cnsh9622:
            笔画 = self.字元集_cnsh9622[字符]["笔画路径_cnsh9622"]
            路径 = ""
            当前点 = None
            
            for 动作 in 笔画:
                if 动作["类型"] == "移动到":
                    x, y = 动作["坐标"]
                    路径 += f"M {x} {y} "
                    当前点 = (x, y)
                elif 动作["类型"] == "直线段":
                    x, y = 动作["终点"]
                    路径 += f"L {x} {y} "
                    当前点 = (x, y)
                elif 动作["类型"] == "三次曲线":
                    P1, P2, P3 = 动作["控制点"]
                    路径 += f"C {P1[0]} {P1[1]}, {P2[0]} {P2[1]}, {P3[0]} {P3[1]} "
                    当前点 = P3
            
            svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <rect width="100%" height="100%" fill="white"/>
  <path d="{路径}" fill="none" stroke="black" stroke-width="8" 
        stroke-linecap="round" stroke-linejoin="round"/>
  <text x="10" y="20" font-size="10" fill="#aaa">V0003 - {字符}</text>
  <text x="10" y="490" font-size="8" fill="#ddd">DNA: {self.工程信息_cnsh9622['DNA追溯码']}</text>
</svg>"""
            
            输出路径 = os.path.join(输出目录_cnsh9622, f"CNSH_{字符}_v0003.svg")
            with open(输出路径, "w", encoding="utf-8") as f:
                f.write(svg)
            print(f"✅ {字符} → {输出路径}")
        
        print(f"\n🎉 [{self.引擎名称_cnsh9622}] 渲染完成！")


# =====================================================
# 第五部分：V0004 组合引擎
# =====================================================

class CNSH组合引擎_V0004_UID9622(CNSH引擎基类_UID9622):
    """V0004 组合引擎"""
    
    def __init__(self):
        super().__init__()
        self.版本号_cnsh9622 = "0.0.4"
        self.引擎名称_cnsh9622 = "组合引擎"
        self.组合规则_cnsh9622 = {}
    
    def 载入_cnsh数据_cnsh龍魂_v1(self, 路径_cnsh9622: str):
        with open(路径_cnsh9622, "r", encoding="utf-8") as f:
            数据 = json.load(f)
        self.字元集_cnsh9622 = 数据["字符集_cnsh9622"]
        self.组合规则_cnsh9622 = 数据.get("字元组合_cnsh9622", {})
        self.审计结果_cnsh9622 = 数据.get("三色审计_cnsh9622", {})
        self.工程信息_cnsh9622 = {
            "工程名称": 数据.get("工程名称"),
            "DNA追溯码": 数据.get("DNA追溯码"),
            "阶段标识": 数据.get("阶段标识")
        }
        print(f"✅ [{self.引擎名称_cnsh9622}] 已加载工程: {self.工程信息_cnsh9622['工程名称']}")
        print(f"   组合数量: {len(self.组合规则_cnsh9622)}")
    
    def 执行三色审计_cnsh龍魂_v1(self):
        if not self.审计结果_cnsh9622:
            print(f"⚠️ [{self.引擎名称_cnsh9622}] 无审计数据")
            return
        
        print(f"\n🎯 [{self.引擎名称_cnsh9622}] 开始执行三色审计...")
        审计通过 = True
        
        for 颜色, 审计项 in self.审计结果_cnsh9622.items():
            结果 = "✅" if 审计项["结果"] == "通过" else "❌"
            print(f"\n{结果} 【{颜色}色审计】")
            for 检查 in 审计项["检查项"]:
                print(f"   • {检查}")
            
            if 审计项["结果"] != "通过":
                审计通过 = False
        
        if not 审计通过:
            raise RuntimeError(f"❌ [{self.引擎名称_cnsh9622}] 三色审计未通过，禁止渲染")
        
        print(f"\n🟢 [{self.引擎名称_cnsh9622}] 三色审计全部通过，准许渲染")
    
    def 执行渲染_cnsh龍魂_v1(self, 输出目录_cnsh9622: str):
        print(f"\n🎯 [{self.引擎名称_cnsh9622}] 开始渲染 {len(self.组合规则_cnsh9622)} 个组合...")
        os.makedirs(输出目录_cnsh9622, exist_ok=True)
        
        for 组合名, 规则 in self.组合规则_cnsh9622.items():
            字元列表 = 规则["组成"]
            方向 = 规则["排布规则_cnsh9622"]["方向"]
            间距 = 规则["排布规则_cnsh9622"]["间距"]
            
            当前偏移 = 0
            总路径 = ""
            
            for 字元 in 字元列表:
                笔画 = self.字元集_cnsh9622[字元]["笔画路径_cnsh9622"]
                路径 = ""
                当前点 = None
                
                for 动作 in 笔画:
                    if 动作["类型"] == "移动到":
                        x, y = 动作["坐标"]
                        if 方向 == "横向":
                            x += 当前偏移
                        else:
                            y += 当前偏移
                        路径 += f"M {x} {y} "
                        当前点 = (x, y)
                    elif 动作["类型"] == "直线段":
                        x, y = 动作["终点"]
                        if 方向 == "横向":
                            x += 当前偏移
                        else:
                            y += 当前偏移
                        路径 += f"L {x} {y} "
                        当前点 = (x, y)
                    elif 动作["类型"] == "三次曲线":
                        P1, P2, P3 = 动作["控制点"]
                        if 方向 == "横向":
                            P1 = [P1[0] + 当前偏移, P1[1]]
                            P2 = [P2[0] + 当前偏移, P2[1]]
                            P3 = [P3[0] + 当前偏移, P3[1]]
                        else:
                            P1 = [P1[0], P1[1] + 当前偏移]
                            P2 = [P2[0], P2[1] + 当前偏移]
                            P3 = [P3[0], P3[1] + 当前偏移]
                        路径 += f"C {P1[0]} {P1[1]}, {P2[0]} {P2[1]}, {P3[0]} {P3[1]} "
                        当前点 = P3
                
                总路径 += 路径
                当前偏移 += 间距
            
            svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600">
  <rect width="100%" height="100%" fill="white"/>
  <path d="{总路径}" fill="none" stroke="black" stroke-width="8" 
        stroke-linecap="round" stroke-linejoin="round"/>
  <text x="10" y="20" font-size="12" fill="#aaa">V0004 - {组合名}</text>
</svg>"""
            
            输出路径 = os.path.join(输出目录_cnsh9622, f"CNSH_组合_{组合名}_v0004.svg")
            with open(输出路径, "w", encoding="utf-8") as f:
                f.write(svg)
            print(f"✅ {组合名} → {输出路径}")
        
        print(f"\n🎉 [{self.引擎名称_cnsh9622}] 组合渲染完成！")


# =====================================================
# 第六部分：V0005 力度引擎
# =====================================================

class CNSH力度引擎_V0005_UID9622(CNSH引擎基类_UID9622):
    """V0005 力度引擎"""
    
    def __init__(self):
        super().__init__()
        self.版本号_cnsh9622 = "0.0.5"
        self.引擎名称_cnsh9622 = "力度引擎"
    
    def 载入_cnsh数据_cnsh龍魂_v1(self, 路径_cnsh9622: str):
        with open(路径_cnsh9622, "r", encoding="utf-8") as f:
            数据 = json.load(f)
        self.字元集_cnsh9622 = 数据["字符集_cnsh9622"]
        self.审计结果_cnsh9622 = 数据.get("三色审计_cnsh9622", {})
        self.工程信息_cnsh9622 = {
            "工程名称": 数据.get("工程名称"),
            "DNA追溯码": 数据.get("DNA追溯码"),
            "阶段标识": 数据.get("阶段标识")
        }
        print(f"✅ [{self.引擎名称_cnsh9622}] 已加载工程: {self.工程信息_cnsh9622['工程名称']}")
    
    def 执行三色审计_cnsh龍魂_v1(self):
        if not self.审计结果_cnsh9622:
            print(f"⚠️ [{self.引擎名称_cnsh9622}] 无审计数据")
            return
        
        print(f"\n🎯 [{self.引擎名称_cnsh9622}] 开始执行三色审计...")
        审计通过 = True
        
        for 颜色, 审计项 in self.审计结果_cnsh9622.items():
            结果 = "✅" if 审计项["结果"] == "通过" else "❌"
            print(f"\n{结果} 【{颜色}色审计】")
            for 检查 in 审计项["检查项"]:
                print(f"   • {检查}")
            
            if 审计项["结果"] != "通过":
                审计通过 = False
        
        if not 审计通过:
            raise RuntimeError(f"❌ [{self.引擎名称_cnsh9622}] 三色审计未通过，渲染被禁止")
        
        print(f"\n🟢 [{self.引擎名称_cnsh9622}] 三色审计全部通过，准许笔画力度渲染")
    
    def 执行渲染_cnsh龍魂_v1(self, 输出目录_cnsh9622: str):
        print(f"\n🎯 [{self.引擎名称_cnsh9622}] 开始笔画力度渲染...")
        os.makedirs(输出目录_cnsh9622, exist_ok=True)
        
        for 字元 in self.字元集_cnsh9622:
            笔画 = self.字元集_cnsh9622[字元]["笔画路径_cnsh9622"]
            svg片段 = []
            当前点 = None
            
            for 动作 in 笔画:
                if 动作["类型"] == "移动到":
                    x, y = 动作["坐标"]
                    当前点 = (x, y)
                
                elif 动作["类型"] == "直线段":
                    终点 = 动作["终点"]
                    力度 = 动作.get("力度", 12)
                    svg片段.append(
                        f'<path d="M {当前点[0]} {当前点[1]} L {终点[0]} {终点[1]}" '
                        f'fill="none" stroke="black" stroke-width="{力度}" '
                        f'stroke-linecap="round" stroke-linejoin="round"/>'
                    )
                    当前点 = 终点
                
                elif 动作["类型"] == "三次曲线":
                    P1, P2, P3 = 动作["控制点"]
                    力度 = 动作.get("力度", 12)
                    svg片段.append(
                        f'<path d="M {当前点[0]} {当前点[1]} '
                        f'C {P1[0]} {P1[1]}, {P2[0]} {P2[1]}, {P3[0]} {P3[1]}" '
                        f'fill="none" stroke="black" stroke-width="{力度}" '
                        f'stroke-linecap="round" stroke-linejoin="round"/>'
                    )
                    当前点 = P3
            
            svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <rect width="100%" height="100%" fill="white"/>
  {''.join(svg片段)}
  <text x="10" y="20" font-size="12" fill="#aaa">V0005 - {字元} (力度)</text>
</svg>"""
            
            输出路径 = os.path.join(输出目录_cnsh9622, f"CNSH_{字元}_力度_v0005.svg")
            with open(输出路径, "w", encoding="utf-8") as f:
                f.write(svg)
            print(f"✅ {字元} (力度渲染) → {输出路径}")
        
        print(f"\n🎉 [{self.引擎名称_cnsh9622}] 笔画力度渲染完成！")


# =====================================================
# 第七部分：V0008 层级引擎
# =====================================================

class CNSH层级引擎_V0008_UID9622(CNSH引擎基类_UID9622):
    """V0008 层级引擎"""
    
    def __init__(self):
        super().__init__()
        self.版本号_cnsh9622 = "0.0.8"
        self.引擎名称_cnsh9622 = "层级引擎"
    
    def 载入_cnsh数据_cnsh龍魂_v1(self, 路径_cnsh9622: str):
        with open(路径_cnsh9622, "r", encoding="utf-8") as f:
            数据 = json.load(f)
        self.字元集_cnsh9622 = 数据["字符集_cnsh9622"]
        self.审计结果_cnsh9622 = 数据.get("三色审计_cnsh9622", {})
        self.工程信息_cnsh9622 = {
            "工程名称": 数据.get("工程名称"),
            "DNA追溯码": 数据.get("DNA追溯码"),
            "阶段标识": 数据.get("阶段标识")
        }
        print(f"✅ [{self.引擎名称_cnsh9622}] 已加载工程: {self.工程信息_cnsh9622['工程名称']}")
    
    def 执行三色审计_cnsh龍魂_v1(self):
        if not self.审计结果_cnsh9622:
            print(f"⚠️ [{self.引擎名称_cnsh9622}] 无审计数据")
            return
        
        print(f"\n🎯 [{self.引擎名称_cnsh9622}] 开始执行三色审计...")
        审计通过 = True
        
        for 颜色, 审计项 in self.审计结果_cnsh9622.items():
            结果 = "✅" if 审计项["结果"] == "通过" else "❌"
            print(f"\n{结果} 【{颜色}色审计】")
            for 检查 in 审计项["检查项"]:
                print(f"   • {检查}")
            
            if 审计项["结果"] != "通过":
                审计通过 = False
        
        if not 审计通过:
            raise RuntimeError(f"❌ [{self.引擎名称_cnsh9622}] 三色审计未通过，层级渲染被禁止")
        
        print(f"\n🟢 [{self.引擎名称_cnsh9622}] 三色审计全部通过，准许笔画层级渲染")
    
    def 棱角参数_cnsh9622(self, 类型: str):
        """将棱角类型映射到 SVG 属性"""
        if 类型 == "断锋":
            return "butt", "miter"
        elif 类型 == "锐角":
            return "square", "miter"
        else:  # 平锋
            return "round", "bevel"
    
    def 执行渲染_cnsh龍魂_v1(self, 输出目录_cnsh9622: str):
        print(f"\n🎯 [{self.引擎名称_cnsh9622}] 开始笔画层级渲染...")
        os.makedirs(输出目录_cnsh9622, exist_ok=True)
        
        for 字元 in self.字元集_cnsh9622:
            笔画列表 = self.字元集_cnsh9622[字元]["笔画路径_cnsh9622"]
            
            # 按层级排序笔画（低层级先绘制，高层级后绘制）
            笔画列表_排序 = sorted(笔画列表, key=lambda x: x.get("层级", 0))
            
            路径片段 = []
            当前点 = None
            
            for 动作 in 笔画列表_排序:
                if 动作["类型"] == "移动到":
                    当前点 = 动作["坐标"]
                
                elif 动作["类型"] == "直线段":
                    终点 = 动作["终点"]
                    力度 = 动作.get("力度", 12)
                    棱角 = 动作.get("棱角", "平锋")
                    停顿 = 动作.get("停顿", 0)
                    
                    透明度 = max(0.2, 1 - 停顿)
                    端点, 连接 = self.棱角参数_cnsh9622(棱角)
                    
                    路径片段.append(
                        f'<path d="M {当前点[0]} {当前点[1]} L {终点[0]} {终点[1]}" '
                        f'fill="none" stroke="black" stroke-width="{力度}" '
                        f'stroke-opacity="{透明度:.2f}" '
                        f'stroke-linecap="{端点}" stroke-linejoin="{连接}"/>'
                    )
                    当前点 = 终点
                
                elif 动作["类型"] == "三次曲线":
                    P1, P2, P3 = 动作["控制点"]
                    力度 = 动作.get("力度", 12)
                    棱角 = 动作.get("棱角", "平锋")
                    停顿 = 动作.get("停顿", 0)
                    
                    透明度 = max(0.2, 1 - 停顿)
                    端点, 连接 = self.棱角参数_cnsh9622(棱角)
                    
                    路径片段.append(
                        f'<path d="M {当前点[0]} {当前点[1]} '
                        f'C {P1[0]} {P1[1]}, {P2[0]} {P2[1]}, {P3[0]} {P3[1]}" '
                        f'fill="none" stroke="black" stroke-width="{力度}" '
                        f'stroke-opacity="{透明度:.2f}" '
                        f'stroke-linecap="{端点}" stroke-linejoin="{连接}"/>'
                    )
                    当前点 = P3
            
            svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <rect width="100%" height="100%" fill="white"/>
  {''.join(路径片段)}
  <text x="10" y="20" font-size="12" fill="#aaa">V0008 - {字元} (层级)</text>
  <text x="10" y="590" font-size="10" fill="#ddd">笔画按层级排序</text>
</svg>"""
            
            输出路径 = os.path.join(输出目录_cnsh9622, f"CNSH_{字元}_层级_v0008.svg")
            with open(输出路径, "w", encoding="utf-8") as f:
                f.write(svg)
            print(f"✅ {字元} (层级渲染) → {输出路径}")
        
        print(f"\n🎉 [{self.引擎名称_cnsh9622}] 笔画层级渲染完成！")


# =====================================================
# 第八部分：引擎管理器（核心）
# =====================================================

class CNSH引擎管理器_UID9622:
    """CNSH引擎管理器 - 统一管理所有CNSH引擎"""
    
    def __init__(self):
        self.已注册引擎_cnsh9622: Dict[str, CNSH引擎基类_UID9622] = {}
        self.当前引擎_cnsh9622: Optional[CNSH引擎基类_UID9622] = None
        self.配置_cnsh9622 = {
            "默认引擎": "审计引擎",
            "自动审计": True,
            "输出根目录": "CNSH_输出"
        }
        
        # 自动注册所有引擎
        self._自动注册所有引擎_cnsh9622()
    
    def _自动注册所有引擎_cnsh9622(self):
        """自动注册所有引擎"""
        引擎列表 = [
            ("V0001_基础", CNSH基础引擎_V0001_UID9622()),
            ("V0002_批量", CNSH批量引擎_V0002_UID9622()),
            ("V0003_审计", CNSH审计引擎_V0003_UID9622()),
            ("V0004_组合", CNSH组合引擎_V0004_UID9622()),
            ("V0005_力度", CNSH力度引擎_V0005_UID9622()),
            ("V0008_层级", CNSH层级引擎_V0008_UID9622()),
        ]
        
        for 名称, 引擎 in 引擎列表:
            self.已注册引擎_cnsh9622[名称] = 引擎
    
    def 注册引擎_cnsh龍魂_v1(self, 引擎名称_cnsh9622: str, 引擎实例_cnsh9622: CNSH引擎基类_UID9622):
        """手动注册一个引擎"""
        self.已注册引擎_cnsh9622[引擎名称_cnsh9622] = 引擎实例_cnsh9622
        print(f"✅ 已注册引擎: {引擎名称_cnsh9622} (v{引擎实例_cnsh9622.获取版本_cnsh9622()})")
    
    def 切换引擎_cnsh龍魂_v1(self, 引擎名称_cnsh9622: str):
        """切换当前使用的引擎"""
        if 引擎名称_cnsh9622 not in self.已注册引擎_cnsh9622:
            raise ValueError(f"引擎不存在: {引擎名称_cnsh9622}")
        
        self.当前引擎_cnsh9622 = self.已注册引擎_cnsh9622[引擎名称_cnsh9622]
        print(f"✅ 已切换到引擎: {引擎名称_cnsh9622} (v{self.当前引擎_cnsh9622.获取版本_cnsh9622()})")
    
    def 列出所有引擎_cnsh龍魂_v1(self):
        """列出所有已注册的引擎"""
        print("\n" + "="*60)
        print("📦 CNSH字体引擎管理器 - 已注册引擎")
        print("="*60)
        
        for i, (名称, 引擎) in enumerate(self.已注册引擎_cnsh9622.items(), 1):
            版本 = 引擎.获取版本_cnsh9622()
            引擎名 = 引擎.获取引擎名称_cnsh9622()
            标记 = " ✨ (当前)" if 引擎 == self.当前引擎_cnsh9622 else ""
            print(f"  {i}. {名称} - {引擎名} (v{版本}){标记}")
        
        print("="*60 + "\n")
    
    def 执行渲染_cnsh龍魂_v1(
        self,
        cnsh文件路径_cnsh9622: str,
        引擎名称_cnsh9622: Optional[str] = None,
        输出目录_cnsh9622: Optional[str] = None
    ):
        """执行渲染任务"""
        # 选择引擎
        if 引擎名称_cnsh9622:
            self.切换引擎_cnsh龍魂_v1(引擎名称_cnsh9622)
        
        if not self.当前引擎_cnsh9622:
            # 如果没有当前引擎，切换到默认引擎
            self.切换引擎_cnsh龍魂_v1("V0003_审计")
        
        # 设置输出目录
        if not 输出目录_cnsh9622:
            引擎版本 = self.当前引擎_cnsh9622.获取版本_cnsh9622().replace(".", "_")
            输出目录_cnsh9622 = f"{self.配置_cnsh9622['输出根目录']}/v{引擎版本}"
        
        # 开始渲染
        print("\n" + "="*60)
        print("🎯 CNSH渲染任务开始")
        print("="*60)
        print(f"   引擎: {self.当前引擎_cnsh9622.获取引擎名称_cnsh9622()}")
        print(f"   版本: v{self.当前引擎_cnsh9622.获取版本_cnsh9622()}")
        print(f"   输入: {cnsh文件路径_cnsh9622}")
        print(f"   输出: {输出目录_cnsh9622}")
        print("="*60)
        
        # 1. 载入数据
        self.当前引擎_cnsh9622.载入_cnsh数据_cnsh龍魂_v1(cnsh文件路径_cnsh9622)
        
        # 2. 执行审计（如果配置了自动审计）
        if self.配置_cnsh9622["自动审计"]:
            try:
                self.当前引擎_cnsh9622.执行三色审计_cnsh龍魂_v1()
            except Exception as e:
                print(f"⚠️ 审计执行失败: {e}")
        
        # 3. 执行渲染
        self.当前引擎_cnsh9622.执行渲染_cnsh龍魂_v1(输出目录_cnsh9622)
        
        print("\n" + "="*60)
        print("🎉 CNSH渲染任务完成！")
        print("="*60 + "\n")


# =====================================================
# 第九部分：使用示例
# =====================================================

if __name__ == "__main__":
    # 创建管理器（自动注册所有引擎）
    管理器 = CNSH引擎管理器_UID9622()
    
    # 查看所有引擎
    管理器.列出所有引擎_cnsh龍魂_v1()
    
    print("💡 使用提示:")
    print("   1. 取消下面的注释来执行渲染")
    print("   2. 或者在代码中调用 管理器.执行渲染_cnsh龍魂_v1()")
    print("   3. 老大可以继续上传更多引擎，宝宝会统一整理！\n")
    
    # 使用示例1：使用默认引擎（审计引擎）
    # 管理器.执行渲染_cnsh龍魂_v1(
    #     cnsh文件路径_cnsh9622="demo_long.cnsh"
    # )
    
    # 使用示例2：指定引擎
    # 管理器.执行渲染_cnsh龍魂_v1(
    #     cnsh文件路径_cnsh9622="demo_long.cnsh",
    #     引擎名称_cnsh9622="V0005_力度"
    # )
    
    # 使用示例3：指定输出目录
    # 管理器.执行渲染_cnsh龍魂_v1(
    #     cnsh文件路径_cnsh9622="demo_long.cnsh",
    #     引擎名称_cnsh9622="V0008_层级",
    #     输出目录_cnsh9622="我的输出"
    # )
