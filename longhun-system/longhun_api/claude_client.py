#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude调用龍魂API客户端
让本地Claude直接调用龍魂系统的全部功能

DNA追溯码: #龍芯⚡️2026-03-20-CLAUDE-CLIENT
"""

import requests
import json
from typing import Optional, List, Dict

API_BASE = "http://127.0.0.1:9622"

class LonghunClient:
    """龍魂系统客户端 - Claude专用"""
    
    def __init__(self, api_base: str = API_BASE):
        self.api_base = api_base
    
    # ========== 阳面操作 ==========
    
    def create_dna(self, concept_name: str, concept_type: str, 
                   content: str, metadata: Dict = None) -> Dict:
        """
        创建DNA - 概念确权
        使用场景: Claude生成新内容时立即确权
        """
        response = requests.post(
            f"{self.api_base}/yang/create",
            json={
                "concept_name": concept_name,
                "concept_type": concept_type,
                "content": content,
                "metadata": metadata or {}
            }
        )
        return response.json()
    
    def embed_dna(self, content: str, dna_code: str) -> Dict:
        """
        嵌入DNA水印 - 隐形保护
        使用场景: 输出内容前嵌入不可见水印
        """
        response = requests.post(
            f"{self.api_base}/yang/embed",
            json={
                "content": content,
                "dna_code": dna_code
            }
        )
        return response.json()
    
    # ========== 阴面操作 ==========
    
    def trace_dna(self, dna_code: str) -> Dict:
        """
        追踪DNA - 溯源确权
        使用场景: 验证内容原创性
        """
        response = requests.get(f"{self.api_base}/yin/trace/{dna_code}")
        return response.json()
    
    def extract_dna(self, content: str) -> Dict:
        """
        提取DNA - 检测窃取
        使用场景: 检查外部内容是否盗用
        """
        response = requests.post(
            f"{self.api_base}/yin/extract",
            json={"content": content}
        )
        return response.json()
    
    # ========== 清道夫 ==========
    
    def sweeper_scan(self, dna_code: str, engines: List[str] = None) -> Dict:
        """
        清道夫扫描 - 全网监控
        使用场景: 定期检查DNA是否被盗
        """
        response = requests.post(
            f"{self.api_base}/sweeper/scan",
            json={
                "dna_code": dna_code,
                "engines": engines or ["baidu", "bing"]
            }
        )
        return response.json()
    
    # ========== 微信通知 ==========
    
    def config_wechat(self, sendkey: str) -> Dict:
        """
        配置微信通知
        使用场景: 首次设置Server酱
        """
        response = requests.post(
            f"{self.api_base}/wechat/config",
            json={"sendkey": sendkey}
        )
        return response.json()
    
    def test_wechat(self) -> Dict:
        """测试微信通知"""
        response = requests.post(f"{self.api_base}/wechat/test")
        return response.json()
    
    # ========== 对峙模式 ==========
    
    def generate_confront(self, dna_code: str) -> Dict:
        """
        生成对峙证据包 - 法律武器
        使用场景: 发现盗窃后准备法律材料
        """
        response = requests.post(
            f"{self.api_base}/confront/generate",
            json={"dna_code": dna_code}
        )
        return response.json()
    
    def download_confront(self, package_id: str, save_path: str = None):
        """
        下载对峙证据包
        使用场景: 获取证据文件
        """
        response = requests.get(
            f"{self.api_base}/confront/download/{package_id}",
            stream=True
        )
        
        if save_path:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return {"success": True, "path": save_path}
        
        return response.json()
    
    # ========== 证据链 ==========
    
    def get_evidence_chain(self, dna_code: str) -> Dict:
        """
        获取完整证据链
        使用场景: 验证证据完整性
        """
        response = requests.get(f"{self.api_base}/evidence/chain/{dna_code}")
        return response.json()
    
    # ========== 黑名单 ==========
    
    def get_blacklist(self) -> Dict:
        """获取CNSH黑名单"""
        response = requests.get(f"{self.api_base}/audit/blacklist")
        return response.json()
    
    def add_blacklist(self, entity_name: str, entity_type: str,
                      violation_type: str, dna_codes: List[str]) -> Dict:
        """
        添加黑名单
        使用场景: 确认窃取行为后列入CNSH
        """
        response = requests.post(
            f"{self.api_base}/audit/add_blacklist",
            params={
                "entity_name": entity_name,
                "entity_type": entity_type,
                "violation_type": violation_type
            },
            json=dna_codes
        )
        return response.json()

# ========== Claude快捷调用函数 ==========

_client = None

def get_client() -> LonghunClient:
    """获取单例客户端"""
    global _client
    if _client is None:
        _client = LonghunClient()
    return _client

# 便捷函数
def dna_create(concept_name: str, content: str, concept_type: str = "concept") -> Dict:
    """快捷创建DNA"""
    return get_client().create_dna(concept_name, concept_type, content)

def dna_embed(content: str, dna_code: str) -> str:
    """快捷嵌入DNA，返回嵌入后的内容"""
    result = get_client().embed_dna(content, dna_code)
    return result.get("embedded_content", content)

def dna_trace(dna_code: str) -> Dict:
    """快捷追踪DNA"""
    return get_client().trace_dna(dna_code)

def dna_extract(content: str) -> List[str]:
    """快捷提取DNA，返回DNA列表"""
    result = get_client().extract_dna(content)
    return result.get("dna_codes", [])

def sweeper(dna_code: str) -> Dict:
    """快捷清道夫扫描"""
    return get_client().sweeper_scan(dna_code)

def confront(dna_code: str) -> Dict:
    """快捷生成对峙包"""
    return get_client().generate_confront(dna_code)

def evidence(dna_code: str) -> Dict:
    """快捷获取证据链"""
    return get_client().get_evidence_chain(dna_code)

# ========== 使用示例 ==========

if __name__ == "__main__":
    print("龍魂Claude客户端测试")
    print("=" * 50)
    
    client = get_client()
    
    # 测试1: 创建DNA
    print("\n[测试1] 创建DNA...")
    result = client.create_dna(
        concept_name="测试概念",
        concept_type="test",
        content="这是一个测试内容，用于验证DNA系统"
    )
    print(f"结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if result.get("success"):
        dna_code = result["dna_code"]
        
        # 测试2: 嵌入DNA
        print("\n[测试2] 嵌入DNA...")
        content = "这是需要保护的原创内容。"
        embed_result = client.embed_dna(content, dna_code)
        print(f"嵌入后长度: {embed_result.get('embedded_length')}")
        
        # 测试3: 追踪DNA
        print("\n[测试3] 追踪DNA...")
        trace_result = client.trace_dna(dna_code)
        print(f"概念名称: {trace_result.get('concept_name')}")
        
        # 测试4: 提取DNA
        print("\n[测试4] 提取DNA...")
        extract_result = client.extract_dna(embed_result.get("embedded_content", ""))
        print(f"提取到的DNA: {extract_result.get('dna_codes')}")
        
        # 测试5: 获取证据链
        print("\n[测试5] 获取证据链...")
        evidence_result = client.get_evidence_chain(dna_code)
        print(f"证据数量: {evidence_result.get('evidence_count')}")

"""
Claude使用说明:

1. 确保API服务器已启动: python3 main.py
2. 在Claude对话中导入: from claude_client import *
3. 使用便捷函数:
   - dna_create("概念名", "内容")  # 确权
   - dna_embed("内容", "DNA码")    # 嵌入水印
   - dna_trace("DNA码")            # 追踪
   - sweeper("DNA码")              # 扫描
   - confront("DNA码")             # 生成证据包
   - evidence("DNA码")             # 获取证据链
"""
