#!/usr/bin/env python3
"""
CNSH DNA生成器
基于可扩展分类体系的DNA确认码生成工具
"""

import hashlib
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple

class CNSHDNAGenerator:
    """CNSH DNA生成器"""
    
    def __init__(self):
        """初始化生成器"""
        self.content_types = self._load_content_types()
        self.regions = self._load_regions()
        
    def _load_content_types(self) -> Dict[str, str]:
        """加载创作类型"""
        return {
            # 核心创作类型
            "ID": "创意想法",
            "ME": "方法论",
            "AL": "算法",
            "CD": "代码",
            "DE": "设计",
            "DO": "文档",
            "DT": "数据",
            "TL": "工具",
            
            # 扩展创作类型
            "RE": "研究",
            "MU": "音乐",
            "VI": "视频",
            "IM": "图片",
            "GM": "游戏",
            "BM": "商业模式",
            "HW": "硬件",
            "OT": "其他"
        }
    
    def _load_regions(self) -> Dict[str, str]:
        """加载区域代码"""
        return {
            # 中国地区
            "CN": "中国大陆",
            "HK": "香港",
            "TW": "台湾",
            "MO": "澳门",
            
            # 国际区域
            "US": "美国",
            "JP": "日本",
            "KR": "韩国",
            "UK": "英国",
            "DE": "德国",
            "FR": "法国",
            "IN": "印度",
            
            # 特殊区域
            "GL": "全球",
            "VX": "虚拟",
            "OP": "开源",
            "AC": "学术",
            "BS": "商业",
            "PR": "个人",
            "ED": "教育"
        }
    
    def generate_dna_code(self, content_type: str, region: str, content: str, 
                        author: str, version: str = "v1.0") -> Dict:
        """生成DNA确认码"""
        # 验证输入
        validation_result = self._validate_input(content_type, region, content, author, version)
        if not validation_result["valid"]:
            return {"success": False, "error": validation_result["error"]}
        
        # 构建基础部分
        year = datetime.now().strftime("%Y")
        base_code = f"ZHUGEXIN⚡️{year}-{content_type}-{region}-{content}-{author}-{version}"
        
        # 生成校验码
        checksum = hashlib.sha256(base_code.encode()).hexdigest()[:4].upper()
        
        # 组合完整DNA码
        full_code = f"#{base_code}-{checksum}"
        
        # 返回结果
        return {
            "success": True,
            "dna_code": full_code,
            "components": {
                "year": year,
                "content_type": content_type,
                "content_type_name": self.content_types.get(content_type, "未知"),
                "region": region,
                "region_name": self.regions.get(region, "未知"),
                "content": content,
                "author": author,
                "version": version,
                "checksum": checksum
            }
        }
    
    def _validate_input(self, content_type: str, region: str, content: str, 
                      author: str, version: str) -> Dict:
        """验证输入参数"""
        # 检查创作类型
        if content_type not in self.content_types:
            return {
                "valid": False,
                "error": f"无效的创作类型: {content_type}，请使用: {', '.join(self.content_types.keys())}"
            }
        
        # 检查区域代码
        if region not in self.regions:
            return {
                "valid": False,
                "error": f"无效的区域代码: {region}，请使用: {', '.join(self.regions.keys())}"
            }
        
        # 检查内容描述
        if len(content) < 3 or len(content) > 20:
            return {
                "valid": False,
                "error": "内容描述长度必须在3-20字符之间"
            }
        
        # 检查内容格式（只允许中文字符、英文字母、数字、下划线）
        if not re.match(r'^[\w\u4e00-\u9fff]+$', content):
            return {
                "valid": False,
                "error": "内容描述只能包含中文字符、英文字母、数字、下划线"
            }
        
        # 检查作者标识
        if len(author) < 3 or len(author) > 10:
            return {
                "valid": False,
                "error": "作者标识长度必须在3-10字符之间"
            }
        
        # 检查版本格式
        if not re.match(r'^v\d+\.\d+$', version):
            return {
                "valid": False,
                "error": "版本格式必须为 vX.Y (例如: v1.0)"
            }
        
        return {"valid": True}
    
    def verify_dna_code(self, dna_code: str) -> Dict:
        """验证DNA码的有效性"""
        # 检查格式
        if not dna_code.startswith("#龍芯⚡️"):
            return {"valid": False, "error": "DNA码格式错误：必须以#龍芯⚡️开头"}
        
        # 分解DNA码
        try:
            parts = dna_code[1:].split('-')  # 去掉#号
            if len(parts) < 7:
                return {"valid": False, "error": "DNA码格式错误：部分不足"}
            
            year = parts[1]
            content_type = parts[2]
            region = parts[3]
            # 内容可能包含多个连字符，需要特殊处理
            author_version_index = -2  # 版本位置
            content_parts = parts[4:author_version_index]
            content = '-'.join(content_parts)
            author = parts[-2]
            version = parts[-1]
            provided_checksum = parts[-1].split('-')[-1] if '-' in parts[-1] else None
            
            if not provided_checksum:
                return {"valid": False, "error": "DNA码格式错误：缺少校验码"}
            
            # 重新构建基础部分（不带校验码）
            base_without_checksum = f"ZHUGEXIN⚡️{year}-{content_type}-{region}-{content}-{author}-{version}"
            
            # 重新计算校验码
            expected_checksum = hashlib.sha256(base_without_checksum.encode()).hexdigest()[:4].upper()
            
            # 验证
            is_valid = provided_checksum == expected_checksum
            
            return {
                "valid": is_valid,
                "message": "校验成功" if is_valid else "校验失败：DNA码可能被篡改",
                "components": {
                    "year": year,
                    "content_type": content_type,
                    "content_type_name": self.content_types.get(content_type, "未知"),
                    "region": region,
                    "region_name": self.regions.get(region, "未知"),
                    "content": content,
                    "author": author,
                    "version": version,
                    "provided_checksum": provided_checksum,
                    "expected_checksum": expected_checksum
                }
            }
        
        except Exception as e:
            return {"valid": False, "error": f"验证失败: {str(e)}"}
    
    def list_content_types(self) -> List[Dict]:
        """列出所有创作类型"""
        return [
            {"code": code, "name": name}
            for code, name in self.content_types.items()
        ]
    
    def list_regions(self) -> List[Dict]:
        """列出所有区域"""
        return [
            {"code": code, "name": name}
            for code, name in self.regions.items()
        ]
    
    def suggest_content_type(self, description: str) -> List[str]:
        """根据描述建议创作类型"""
        description = description.lower()
        suggestions = []
        
        # 关键词映射
        keywords_map = {
            "创意": "ID", "想法": "ID", "点子": "ID",
            "方法": "ME", "流程": "ME", "机制": "ME",
            "算法": "AL", "公式": "AL", "逻辑": "AL",
            "代码": "CD", "程序": "CD", "脚本": "CD",
            "设计": "DE", "界面": "DE", "图形": "DE",
            "文档": "DO", "教程": "DO", "说明": "DO",
            "数据": "DT", "数据集": "DT", "样本": "DT",
            "工具": "TL", "软件": "TL", "插件": "TL"
        }
        
        for keyword, code in keywords_map.items():
            if keyword in description:
                if code not in suggestions:
                    suggestions.append(code)
        
        return suggestions if suggestions else ["ID"]  # 默认为创意
    
    def generate_batch(self, items: List[Dict]) -> List[Dict]:
        """批量生成DNA码"""
        results = []
        
        for item in items:
            result = self.generate_dna_code(
                content_type=item.get("content_type", "ID"),
                region=item.get("region", "CN"),
                content=item.get("content", "未命名"),
                author=item.get("author", "匿名"),
                version=item.get("version", "v1.0")
            )
            results.append(result)
        
        return results


# 交互式命令行界面
def interactive_mode():
    """交互式命令行模式"""
    generator = CNSHDNAGenerator()
    
    print("🧬 CNSH DNA生成器 - 交互式模式")
    print("=" * 40)
    
    while True:
        print("\n请选择操作：")
        print("1. 生成单个DNA码")
        print("2. 验证DNA码")
        print("3. 查看创作类型")
        print("4. 查看区域代码")
        print("5. 批量生成")
        print("6. 退出")
        
        choice = input("\n请输入选项 [1-6]: ").strip()
        
        if choice == "1":
            single_generation(generator)
        elif choice == "2":
            verify_code(generator)
        elif choice == "3":
            list_types(generator)
        elif choice == "4":
            list_regions(generator)
        elif choice == "5":
            batch_generation(generator)
        elif choice == "6":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选项，请重新输入。")


def single_generation(generator):
    """单个DNA码生成"""
    print("\n🧬 生成DNA确认码")
    print("-" * 20)
    
    # 显示创作类型
    types = generator.list_content_types()
    print("\n可用创作类型：")
    for type_info in types:
        print(f"  {type_info['code']}: {type_info['name']}")
    
    # 获取输入
    content_type = input("\n请输入创作类型代码: ").strip().upper()
    region = input("请输入区域代码 [默认CN]: ").strip().upper() or "CN"
    content = input("请输入内容描述 (3-20字符): ").strip()
    author = input("请输入作者标识 (3-10字符): ").strip()
    version = input("请输入版本号 [默认v1.0]: ").strip() or "v1.0"
    
    # 生成DNA码
    result = generator.generate_dna_code(content_type, region, content, author, version)
    
    if result["success"]:
        print("\n✅ DNA码生成成功！")
        print(f"🧬 DNA码: {result['dna_code']}")
        print("\n📋 解析信息：")
        for key, value in result["components"].items():
            print(f"  {key}: {value}")
    else:
        print(f"\n❌ DNA码生成失败: {result['error']}")


def verify_code(generator):
    """验证DNA码"""
    print("\n🔍 验证DNA码")
    print("-" * 15)
    
    dna_code = input("请输入DNA码: ").strip()
    result = generator.verify_dna_code(dna_code)
    
    if result["valid"]:
        print("\n✅ DNA码验证成功！")
        print(f"📝 {result['message']}")
        print("\n📋 解析信息：")
        for key, value in result["components"].items():
            print(f"  {key}: {value}")
    else:
        print(f"\n❌ DNA码验证失败: {result['error']}")


def list_types(generator):
    """显示创作类型"""
    print("\n📋 可用创作类型")
    print("-" * 15)
    
    types = generator.list_content_types()
    for type_info in types:
        print(f"  {type_info['code']:2s}: {type_info['name']}")


def list_regions(generator):
    """显示区域代码"""
    print("\n🌍 可用区域代码")
    print("-" * 15)
    
    regions = generator.list_regions()
    for region_info in regions:
        print(f"  {region_info['code']:2s}: {region_info['name']}")


def batch_generation(generator):
    """批量生成"""
    print("\n📦 批量生成DNA码")
    print("-" * 18)
    
    print("请输入批量数据 (JSON格式):")
    print('示例: [{"content": "投票系统", "author": "user1"}, {"content": "推荐算法", "author": "user2"}]')
    
    try:
        json_input = input("\n请输入JSON数据: ").strip()
        items = json.loads(json_input)
        
        results = generator.generate_batch(items)
        
        print("\n📦 批量生成结果：")
        for i, result in enumerate(results, 1):
            if result["success"]:
                print(f"  {i}. ✅ {result['dna_code']}")
            else:
                print(f"  {i}. ❌ {result['error']}")
    
    except json.JSONDecodeError:
        print("❌ JSON格式错误，请检查输入")
    except Exception as e:
        print(f"❌ 批量生成失败: {str(e)}")


if __name__ == "__main__":
    interactive_mode()