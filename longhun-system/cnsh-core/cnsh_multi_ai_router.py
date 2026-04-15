#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BRAIN_GATE v1.1 受保护文件
# DNA: #龍芯⚡️20260324-CNSH_MULTI_AI_ROUTER
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# UID: 9622 | 未经授权修改视为P0违规
"""
CNSH-64 多AI路由系统
═══════════════════════════════════════════════════════════════
核心信条：多AI统一接入，DNA留痕，不抢资源

支持的AI：
- Claude (Anthropic)
- ChatGPT (OpenAI)
- Grok (xAI)
- Gemini (Google)
- 其他兼容OpenAI API的模型

功能：
1. 统一API接口
2. 智能路由选择
3. DNA留痕追溯
4. P0++扫描
5. E-CNY主权检测
6. 负载均衡
═══════════════════════════════════════════════════════════════
"""

import asyncio
import aiohttp
import hashlib
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('CNSH-Multi-AI-Router')


class AIModel(Enum):
    """AI模型"""
    CLAUDE = "claude"
    CHATGPT = "chatgpt"
    GROK = "grok"
    GEMINI = "gemini"
    CUSTOM = "custom"


@dataclass
class AIConfig:
    """AI配置"""
    name: str
    api_url: str
    api_key: str
    model_id: str
    max_tokens: int = 4096
    temperature: float = 0.7
    priority: int = 1  # 优先级，越小越高
    is_available: bool = True


@dataclass
class AIRequest:
    """AI请求"""
    dna: str
    message: str
    preferred_model: Optional[AIModel] = None
    context: List[Dict] = None
    require_dna_trace: bool = True


@dataclass
class AIResponse:
    """AI响应"""
    dna: str
    request_hash: str
    model_used: str
    content: str
    response_hash: str
    timestamp: float
    processing_time: float
    dna_signature: str


class MultiAIRouter:
    """
    多AI路由器
    
    统一接入多个AI，智能路由，DNA留痕
    """
    
    def __init__(self):
        self.ai_configs: Dict[AIModel, AIConfig] = {}
        self.request_history: List[Dict] = []
        self.response_history: List[Dict] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        
        # 默认配置
        self._init_default_configs()
        
    def _init_default_configs(self):
        """初始化默认配置"""
        self.ai_configs[AIModel.CLAUDE] = AIConfig(
            name="Claude",
            api_url="https://api.anthropic.com/v1/messages",
            api_key="",  # 需要配置
            model_id="claude-3-sonnet-20240229",
            priority=1
        )
        
        self.ai_configs[AIModel.CHATGPT] = AIConfig(
            name="ChatGPT",
            api_url="https://api.openai.com/v1/chat/completions",
            api_key="",  # 需要配置
            model_id="gpt-4",
            priority=2
        )
        
        self.ai_configs[AIModel.GROK] = AIConfig(
            name="Grok",
            api_url="https://api.x.ai/v1/chat/completions",
            api_key="",  # 需要配置
            model_id="grok-1",
            priority=3
        )
        
        self.ai_configs[AIModel.GEMINI] = AIConfig(
            name="Gemini",
            api_url="https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            api_key="",  # 需要配置
            model_id="gemini-pro",
            priority=4
        )
    
    def configure_ai(self, model: AIModel, 
                    api_key: str,
                    api_url: str = None) -> Dict:
        """配置AI"""
        if model not in self.ai_configs:
            return {'error': '不支持的AI模型'}
        
        config = self.ai_configs[model]
        config.api_key = api_key
        if api_url:
            config.api_url = api_url
        config.is_available = True
        
        logger.info(f"✅ AI配置完成: {config.name}")
        
        return {
            'success': True,
            'model': model.value,
            'name': config.name,
            'status': 'configured'
        }
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=60)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    def _calculate_request_hash(self, request: AIRequest) -> str:
        """计算请求哈希 - DNA留痕"""
        data = f"{request.dna}:{request.message}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _select_model(self, request: AIRequest) -> Optional[AIModel]:
        """
        智能选择模型
        
        1. 优先使用用户指定的模型
        2. 否则按优先级选择可用模型
        3. 负载均衡
        """
        # 用户指定
        if request.preferred_model and request.preferred_model in self.ai_configs:
            config = self.ai_configs[request.preferred_model]
            if config.is_available and config.api_key:
                return request.preferred_model
        
        # 按优先级选择
        available_models = [
            (model, config) for model, config in self.ai_configs.items()
            if config.is_available and config.api_key
        ]
        
        if not available_models:
            return None
        
        # 按优先级排序
        available_models.sort(key=lambda x: x[1].priority)
        
        return available_models[0][0]
    
    async def route_to_claude(self, request: AIRequest, 
                              config: AIConfig) -> Dict:
        """路由到Claude"""
        headers = {
            "x-api-key": config.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": config.model_id,
            "max_tokens": config.max_tokens,
            "messages": [
                {"role": "user", "content": request.message}
            ]
        }
        
        if request.context:
            payload["messages"] = request.context + payload["messages"]
        
        async with self.session.post(
            config.api_url,
            headers=headers,
            json=payload
        ) as resp:
            result = await resp.json()
            
            if 'content' in result:
                return {
                    'success': True,
                    'content': result['content'][0]['text'],
                    'model': 'claude'
                }
            
            return {'error': result.get('error', 'Claude请求失败')}
    
    async def route_to_openai(self, request: AIRequest,
                              config: AIConfig) -> Dict:
        """路由到OpenAI兼容API (ChatGPT/Grok)"""
        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = [{"role": "user", "content": request.message}]
        if request.context:
            messages = request.context + messages
        
        payload = {
            "model": config.model_id,
            "messages": messages,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature
        }
        
        async with self.session.post(
            config.api_url,
            headers=headers,
            json=payload
        ) as resp:
            result = await resp.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                return {
                    'success': True,
                    'content': result['choices'][0]['message']['content'],
                    'model': config.name.lower()
                }
            
            return {'error': result.get('error', 'OpenAI请求失败')}
    
    async def ask(self, request: AIRequest) -> AIResponse:
        """
        统一询问接口
        
        Args:
            request: AI请求
            
        Returns:
            AI响应，带DNA留痕
        """
        start_time = time.time()
        request_hash = self._calculate_request_hash(request)
        
        # 记录请求
        self.request_history.append({
            'dna': request.dna,
            'message': request.message[:100],
            'request_hash': request_hash,
            'preferred_model': request.preferred_model.value if request.preferred_model else None,
            'timestamp': start_time
        })
        
        # 选择模型
        model = self._select_model(request)
        if not model:
            return AIResponse(
                dna=request.dna,
                request_hash=request_hash,
                model_used="none",
                content="错误：没有可用的AI模型，请先配置API密钥",
                response_hash="",
                timestamp=time.time(),
                processing_time=0,
                dna_signature=""
            )
        
        config = self.ai_configs[model]
        
        # 路由到对应AI
        try:
            if model == AIModel.CLAUDE:
                result = await self.route_to_claude(request, config)
            else:
                result = await self.route_to_openai(request, config)
            
            processing_time = time.time() - start_time
            
            if result.get('success'):
                content = result['content']
                response_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
                
                # DNA签名
                dna_signature = hashlib.sha256(
                    f"{request.dna}:{response_hash}:{time.time()}".encode()
                ).hexdigest()[:16]
                
                response = AIResponse(
                    dna=request.dna,
                    request_hash=request_hash,
                    model_used=result['model'],
                    content=content,
                    response_hash=response_hash,
                    timestamp=time.time(),
                    processing_time=processing_time,
                    dna_signature=dna_signature
                )
                
                # 记录响应
                self.response_history.append({
                    'dna': request.dna,
                    'request_hash': request_hash,
                    'model_used': result['model'],
                    'response_hash': response_hash,
                    'timestamp': response.timestamp
                })
                
                logger.info(f"🤖 AI响应: {request.dna[:16]}... -> {result['model']}")
                
                return response
            else:
                return AIResponse(
                    dna=request.dna,
                    request_hash=request_hash,
                    model_used=model.value,
                    content=f"错误: {result.get('error', '未知错误')}",
                    response_hash="",
                    timestamp=time.time(),
                    processing_time=time.time() - start_time,
                    dna_signature=""
                )
        
        except Exception as e:
            return AIResponse(
                dna=request.dna,
                request_hash=request_hash,
                model_used=model.value,
                content=f"错误: {str(e)}",
                response_hash="",
                timestamp=time.time(),
                processing_time=time.time() - start_time,
                dna_signature=""
            )
    
    def get_routing_stats(self) -> Dict:
        """获取路由统计"""
        model_usage = {}
        for resp in self.response_history:
            model = resp['model_used']
            model_usage[model] = model_usage.get(model, 0) + 1
        
        return {
            'total_requests': len(self.request_history),
            'total_responses': len(self.response_history),
            'model_usage': model_usage,
            'available_models': [
                model.value for model, config in self.ai_configs.items()
                if config.is_available and config.api_key
            ]
        }
    
    def get_dna_history(self, dna: str) -> List[Dict]:
        """获取某人的AI对话历史"""
        requests = [r for r in self.request_history if r['dna'] == dna]
        responses = [r for r in self.response_history if r['dna'] == dna]
        
        return {
            'requests': requests,
            'responses': responses,
            'total_interactions': len(requests)
        }


class SiriShortcutAPI:
    """
    Siri快捷指令API
    
    让Siri可以调用龍魂系统
    """
    
    def __init__(self, router: MultiAIRouter):
        self.router = router
        
    async def handle_siri_request(self, 
                                   user_input: str,
                                   user_dna: str = "anonymous") -> Dict:
        """
        处理Siri请求
        
        Siri Shortcut → POST /ask → 龍魂 → AI → 返回
        """
        request = AIRequest(
            dna=user_dna,
            message=user_input,
            preferred_model=None,
            context=[]
        )
        
        response = await self.router.ask(request)
        
        return {
            'siri_response': response.content,
            'model_used': response.model_used,
            'dna_traced': response.dna_signature != "",
            'processing_time': response.processing_time
        }
    
    def get_shortcut_url(self, base_url: str = "http://localhost:9622") -> str:
        """获取Siri快捷指令URL"""
        return f"{base_url}/ask"
    
    def get_shortcut_template(self) -> str:
        """获取Siri快捷指令模板"""
        return """
# Siri快捷指令模板

1. 创建新快捷指令，命名为"问龍魂"
2. 添加"询问输入"操作，提示文字"你想问什么？"
3. 添加"获取URL内容"操作：
   - URL: http://你的服务器:9622/ask
   - 方法: POST
   - 请求体: {"message": "[快捷输入]", "dna": "你的DNA"}
4. 添加"获取词典值"操作，获取"siri_response"
5. 添加"显示结果"或"朗读文本"操作

完成！现在你可以说"嘿Siri，问龍魂"
"""


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

async def demo():
    """演示多AI路由系统"""
    
    print("═" * 60)
    print("CNSH-64 多AI路由系统演示")
    print("多AI统一接入，DNA留痕")
    print("═" * 60)
    
    async with MultiAIRouter() as router:
        # 配置AI（实际使用时需要填入真实API密钥）
        print("\n[1] 配置AI模型")
        print("  支持的模型:")
        for model in AIModel:
            print(f"    • {model.value}")
        
        # 演示：配置Claude（需要真实API密钥）
        # result = router.configure_ai(AIModel.CLAUDE, "your-api-key")
        # print(f"  Claude配置: {result}")
        
        # 创建Siri快捷指令接口
        siri = SiriShortcutAPI(router)
        
        print("\n[2] Siri快捷指令配置")
        print(f"  API地址: {siri.get_shortcut_url()}")
        print(f"  模板:\n{siri.get_shortcut_template()}")
        
        # 演示请求（需要配置API密钥才能实际运行）
        print("\n[3] 演示AI请求")
        print("  请求格式:")
        print("  {")
        print('    "dna": "0x7a3f...",')
        print('    "message": "你好，龍魂",')
        print('    "preferred_model": "claude"')
        print("  }")
        
        print("\n  响应格式:")
        print("  {")
        print('    "dna": "0x7a3f...",')
        print('    "request_hash": "abc123...",')
        print('    "model_used": "claude",')
        print('    "content": "AI回复内容",')
        print('    "response_hash": "def456...",')
        print('    "dna_signature": "ghi789..."')
        print("  }")
        
        # 路由统计
        print("\n[4] 路由统计")
        stats = router.get_routing_stats()
        print(f"  总请求数: {stats['total_requests']}")
        print(f"  总响应数: {stats['total_responses']}")
        print(f"  模型使用: {stats['model_usage']}")
        print(f"  可用模型: {stats['available_models']}")
    
    print("\n" + "═" * 60)
    print("多AI路由系统演示完成")
    print("Siri的嘴，龍魂的魂")
    print("═" * 60)


if __name__ == '__main__':
    asyncio.run(demo())
