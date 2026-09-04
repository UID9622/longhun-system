#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA追溯: #ZHUGEXIN⚡️20260302-CNSH-DNA_GENERATOR-PY-v0.1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 镜像来源: https://gitee.com/uid9622/cnsh/raw/main/core/identity/dna_generator.py
"""
CNSH DNA生成器 - 基于可扩展分类体系的DNA确认码生成工具
"""

import hashlib
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any

class CNSHDNAGenerator:
    def __init__(self):
        self.content_types = self._load_content_types()
        self.regions = self._load_regions()
        
    def _load_content_types(self) -> Dict[str, str]:
        return {
            "ID": "创意想法", "ME": "方法论", "AL": "算法", "CD": "代码",
            "DE": "设计", "DO": "文档", "DT": "数据", "TL": "工具",
            "RE": "研究", "MU": "音乐", "VI": "视频", "IM": "图片",
            "GM": "游戏", "BM": "商业模式", "HW": "硬件", "OT": "其他"
        }
    
    def _load_regions(self) -> Dict[str, str]:
        return {
            "CN": "中国大陆", "HK": "香港", "TW": "台湾", "MO": "澳门",
            "US": "美国", "JP": "日本", "KR": "韩国", "UK": "英国",
            "DE": "德国", "FR": "法国", "IN": "印度",
            "GL": "全球", "VX": "虚拟", "OP": "开源", "AC": "学术",
            "BS": "商业", "PR": "个人", "ED": "教育"
        }
    
    def generate_dna_code(self, content_type: str, region: str, content: str, 
                        author: str, version: str = "v1.0") -> Dict[str, Any]:
        validation_result = self._validate_input(content_type, region, content, author, version)
        if not validation_result["valid"]:
            return {"success": False, "error": validation_result["error"]}
        
        year = datetime.now().strftime("%Y")
        base_code = f"ZHUGEXIN⚡️{year}-{content_type}-{region}-{content}-{author}-{version}"
        checksum = hashlib.sha256(base_code.encode()).hexdigest()[:4].upper()
        full_code = f"#{base_code}-{checksum}"
        
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
    
    def _validate_input(self, content_type, region, content, author, version) -> Dict[str, Any]:
        if content_type not in self.content_types:
            return {"valid": False, "error": f"无效的创作类型: {content_type}"}
        if region not in self.regions:
            return {"valid": False, "error": f"无效的区域代码: {region}"}
        if len(content) < 3 or len(content) > 20:
            return {"valid": False, "error": "内容描述长度必须在3-20字符之间"}
        if not re.match(r'^[\w\u4e00-\u9fff]+$', content):
            return {"valid": False, "error": "内容描述只能包含中文字符、英文字母、数字、下划线"}
        if len(author) < 3 or len(author) > 10:
            return {"valid": False, "error": "作者标识长度必须在3-10字符之间"}
        if not re.match(r'^v\d+\.\d+$', version):
            return {"valid": False, "error": "版本格式必须为 vX.Y"}
        return {"valid": True}
    
    def verify_dna_code(self, dna_code: str) -> Dict[str, Any]:
        if not dna_code.startswith("#ZHUGEXIN⚡️"):
            return {"valid": False, "error": "DNA码格式错误：必须以#ZHUGEXIN⚡️开头"}
        parts = dna_code[1:].split('-')
        if len(parts) < 7:
            return {"valid": False, "error": "DNA码格式错误：部分不足"}
        year, content_type, region = parts[1], parts[2], parts[3]
        content_parts = parts[4:-2]
        content = '-'.join(content_parts)
        author = parts[-2]
        version_and_checksum = parts[-1]
        
        base_without_checksum = f"ZHUGEXIN⚡️{year}-{content_type}-{region}-{content}-{author}-{version_and_checksum.rsplit('-',1)[0]}"
        provided_checksum = version_and_checksum.rsplit('-', 1)[-1] if '-' in version_and_checksum else version_and_checksum
        expected_checksum = hashlib.sha256(base_without_checksum.encode()).hexdigest()[:4].upper()
        
        is_valid = provided_checksum == expected_checksum
        return {
            "valid": is_valid,
            "message": "校验成功" if is_valid else "校验失败：DNA码可能被篡改",
            "components": {
                "year": year, "content_type": content_type,
                "content_type_name": self.content_types.get(content_type, "未知"),
                "region": region, "region_name": self.regions.get(region, "未知"),
                "content": content, "author": author,
                "provided_checksum": provided_checksum,
                "expected_checksum": expected_checksum
            }
        }
    
    def list_content_types(self) -> List[Dict]:
        return [{"code": code, "name": name} for code, name in self.content_types.items()]
    
    def list_regions(self) -> List[Dict]:
        return [{"code": code, "name": name} for code, name in self.regions.items()]
    
    def generate_batch(self, items: List[Dict]) -> List[Dict]:
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


if __name__ == "__main__":
    generator = CNSHDNAGenerator()
    print("🧬 CNSH DNA生成器")
    print("=" * 40)
    types = generator.list_content_types()
    print("可用创作类型：")
    for type_info in types:
        print(f"  {type_info['code']}: {type_info['name']}")
    print("\n可用区域代码：")
    regions = generator.list_regions()
    for region_info in regions:
        print(f"  {region_info['code']}: {region_info['name']}")
    result = generator.generate_dna_code("ID", "CN", "测试DNA生成", "UID9622", "v1.0")
    print(f"\n测试生成:\n  {result['dna_code']}")
