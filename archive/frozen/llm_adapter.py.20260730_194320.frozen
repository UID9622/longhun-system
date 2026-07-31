#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·LLM-ADAPTER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""🐉 龍魂引擎：llm_adapter
路径：engines/longhun/antenna/ant_colony/llm_adapter.py
TODO：请补充详细功能说明（不少于20字）。"""
from __future__ import annotations
"""
LLM→蚁群适配器 v1.0 · LLMAntennaAdapter
投喂挑战 P1-A4 落地：将 LLM 调用包装为 AntennaSignal 标准协议

DNA: #龍芯⚡️丙午·辛未·LLM-ADAPTER-v1.0
# STATUS: ⚠️ DEPRECATED · 本目录为旧版蚁群实现，功能由 engines/ant_colony/ 与 bin/lh_ant_colony_orchestrator.py 统一接管

核心能力:
  1. LLM调用 → AntennaSignal 包装：任何 LLM 请求/响应转成蚁群信号
  2. IAntennaSensor 接口实现：标准化传感器接入
  3. 多种 LLM 后端支持：OpenAI / 混元 / DeepSeek / 本地模型
  4. 流式响应 → 信息素批次广播
  5. Token 用量 → 信息素强度换算

架构:
  LLM Provider (OpenAI/Hunyuan/...) 
    → LLMAntennaAdapter (包装) 
    → AntennaSignal (标准信号) 
    → AntennaBus (蚁群路由) 
    → 其他蚂蚁模块

用法:
    adapter = LLMAntennaAdapter(provider="openai", api_key="...")
    signal = adapter.chat("你好，评价一下龙魂蚁群架构")
    bus.send(signal)
"""

import time
import json
import hashlib
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable, Iterator
from enum import Enum
from abc import ABC, abstractmethod

from engine.ant_colony.antenna_signal import (
    AntennaSignal, PheromoneType, PayloadType,
    recruit_signal, trail_signal, aggregate_signal,
)


CST = timezone(timedelta(hours=8))
DNA = "#龍芯⚡️丙午·辛未·LLM-ADAPTER-v1.0"


# ═══════════════════════════════════════════════
# IAntennaSensor — 标准化传感器接口
# ═══════════════════════════════════════════════

class SensorReading:
    """传感器读数 — 论文定义的标准化结构"""
    
    def __init__(self, sensor_id: str, data_type: str, value: Any,
                 confidence: float = 1.0, calibration_version: str = "v1.0"):
        self.sensor_id = sensor_id
        self.data_type = data_type
        self.value = value
        self.confidence = confidence
        self.calibration_version = calibration_version
        self.timestamp = time.time()
        self.reading_id = hashlib.sha256(
            f"{sensor_id}:{data_type}:{str(value)[:100]}:{self.timestamp}".encode()
        ).hexdigest()[:16]

    def to_dict(self) -> dict[str, Any]:
        return {
            "sensor_id": self.sensor_id,
            "type": self.data_type,
            "value": str(self.value)[:200],
            "confidence": self.confidence,
            "calibration": self.calibration_version,
        }


class IAntennaSensor(ABC):
    """论文定义的标准化传感器接口"""

    @abstractmethod
    def read(self) -> SensorReading:
        """读取一次传感器数据"""
        ...

    @abstractmethod
    def calibrate(self) -> bool:
        """校准传感器"""
        ...

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """获取传感器状态"""
        ...


# ═══════════════════════════════════════════════
# LLM Provider 抽象
# ═══════════════════════════════════════════════

class LLMProviderType(str, Enum):
    OPENAI = "openai"
    HUNYUAN = "hunyuan"
    DEEPSEEK = "deepseek"
    LOCAL = "local"


class LLMResponse:
    """LLM 响应 — 统一格式"""

    def __init__(self, text: str, model: str, tokens_used: int = 0,
                 finish_reason: str = "stop", raw: dict[str, Any] = None):
        self.text = text
        self.model = model
        self.tokens_used = tokens_used
        self.finish_reason = finish_reason
        self.raw = raw or {}
        self.timestamp = time.time()
        self.response_id = hashlib.sha256(
            f"{model}:{text[:50]}:{self.timestamp}".encode()
        ).hexdigest()[:12]


class BaseLLMProvider(ABC):
    """LLM Provider 基类"""

    @abstractmethod
    def chat(self, messages: List[dict[str, Any]], **kwargs) -> LLMResponse:
        """同步对话"""
        ...

    @abstractmethod
    def chat_stream(self, messages: List[dict[str, Any]], **kwargs) -> Iterator[str]:
        """流式对话"""
        ...

    @abstractmethod
    def get_model_info(self) -> dict[str, Any]:
        """获取模型信息"""
        ...


class MockLLMProvider(BaseLLMProvider):
    """模拟 LLM Provider（用于测试和演示）"""

    def __init__(self, model: str = "mock-gpt-4"):
        self.model = model
        self._call_count = 0

    def chat(self, messages: List[dict[str, Any]], **kwargs) -> LLMResponse:
        self._call_count += 1
        last_msg = messages[-1].get("content", "") if messages else ""
        
        # 模拟回复
        response_text = (
            f"[模拟 {self.model} 回复 #{self._call_count}] "
            f"对 '{last_msg[:30]}...' 的响应："
            f"这是一个模拟的LLM输出，用于测试蚁群适配器。"
            f"在实际部署中，这里会替换为真实的API调用。"
        )

        return LLMResponse(
            text=response_text,
            model=self.model,
            tokens_used=len(last_msg) // 4 + 50,
            finish_reason="stop",
        )

    def chat_stream(self, messages: List[dict[str, Any]], **kwargs) -> Iterator[str]:
        response = self.chat(messages, **kwargs)
        # 模拟流式输出
        words = response.text.split()
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")
            time.sleep(0.05)

    def get_model_info(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "provider": "mock",
            "max_tokens": 8192,
            "is_mock": True,
        }


# ═══════════════════════════════════════════════
# LLM → AntennaSignal 适配器核心
# ═══════════════════════════════════════════════

class LLMAntennaAdapter(IAntennaSensor):
    """
    LLM → 蚁群适配器

    核心转换:
      LLM 请求 → RECRUIT 招募素 (请求协作)
      LLM 响应 → TRAIL 足迹素   (沉淀知识)
      流式输出 → AGGREGATE 聚集素 (实时协作)
      LLM 错误 → ALERT 警戒素   (异常告警)

    信息素强度映射:
      Token用量 → 信息素初始强度
      置信度    → TRAIL 的 quality_score
      优先级    → RECRUIT 的 priority
    """

    # Token → 信息素强度换算
    TOKENS_TO_STRENGTH = 0.1  # 每token = 0.1 信息素强度

    def __init__(self, provider: BaseLLMProvider = None,
                 provider_type: LLMProviderType = LLMProviderType.LOCAL,
                 sensor_id: str = "llm_sensor_001",
                 module_id: str = "LLM适配器"):
        self.provider = provider or MockLLMProvider()
        self.provider_type = provider_type
        self.sensor_id = sensor_id
        self.module_id = module_id
        
        # 统计
        self.stats = {
            "total_calls": 0,
            "total_tokens": 0,
            "total_signals": 0,
            "errors": 0,
        }
        
        # 会话上下文
        self._conversation_history: List[dict[str, Any]] = []
        self._model_info = self.provider.get_model_info()

    # ── IAntennaSensor 实现 ──

    def read(self) -> SensorReading:
        """读取传感器状态（标准接口）"""
        return SensorReading(
            sensor_id=self.sensor_id,
            data_type="llm_status",
            value={
                "total_calls": self.stats["total_calls"],
                "total_tokens": self.stats["total_tokens"],
                "model": self._model_info.get("model", "unknown"),
                "conversation_length": len(self._conversation_history),
            },
            confidence=1.0,
        )

    def calibrate(self) -> bool:
        """校准（重置统计基线）"""
        self.stats = {k: 0 for k in self.stats}
        return True

    def get_status(self) -> dict[str, Any]:
        """获取适配器状态"""
        return {
            "sensor_id": self.sensor_id,
            "module_id": self.module_id,
            "provider": self.provider_type.value,
            "model": self._model_info.get("model", "unknown"),
            "stats": self.stats,
            "dna": DNA,
        }

    # ── 核心转换方法 ──

    def chat(self, user_message: str, system_prompt: str | None = None,
             task_id: str = None, priority: int = 5) -> List[AntennaSignal]:
        """
        发送 LLM 对话请求 → 返回蚁群信号列表

        流程:
          1. 构建 LLM 请求
          2. 发送 RECRUIT 招募素（请求协作）
          3. 调用 LLM
          4. 发送 TRAIL 足迹素（沉淀知识）
          5. 如果出错 → ALERT 警戒素
        """
        signals = []
        task_id = task_id or f"llm_{int(time.time()*1000)}"

        # 1. RECRUIT 招募素：告诉工蚁群"有LLM任务需要处理"
        recruit = recruit_signal(
            sender=self.module_id,
            receiver="工蚁群",
            task={
                "task_id": task_id,
                "task": f"LLM对话: {user_message[:50]}",
                "model": self._model_info.get("model"),
                "token_estimate": len(user_message) // 4,
            },
            priority=priority,
        )
        signals.append(recruit)
        self.stats["total_signals"] += 1

        try:
            # 2. 调用 LLM
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_message})

            start_time = time.time()
            response = self.provider.chat(messages)
            elapsed_ms = int((time.time() - start_time) * 1000)

            self.stats["total_calls"] += 1
            self.stats["total_tokens"] += response.tokens_used

            # 3. TRAIL 足迹素：沉淀知识
            trail = trail_signal(
                sender=self.module_id,
                receiver="储蜜蚁群",
                trail_type="llm_response",
                path_data={
                    "task_id": task_id,
                    "query": user_message[:200],
                    "response_summary": response.text[:300],
                    "model": response.model,
                    "tokens_used": response.tokens_used,
                    "elapsed_ms": elapsed_ms,
                    "finish_reason": response.finish_reason,
                    "quality_score": min(1.0, response.tokens_used * 0.001),
                },
            )
            signals.append(trail)
            self.stats["total_signals"] += 1

            # 4. 保存到会话历史
            self._conversation_history.append({
                "role": "user", "content": user_message,
                "task_id": task_id, "time": time.time(),
            })
            self._conversation_history.append({
                "role": "assistant", "content": response.text[:500],
                "task_id": task_id, "time": time.time(),
            })

        except Exception as e:
            # 5. ALERT 警戒素：LLM调用异常
            from engine.ant_colony.antenna_signal import alert_signal
            alert = alert_signal(
                sender=self.module_id,
                alert_level=2,
                description=f"LLM调用失败: {str(e)[:100]}",
                affected=[task_id],
            )
            signals.append(alert)
            self.stats["errors"] += 1
            self.stats["total_signals"] += 1

        return signals

    def chat_stream_to_aggregate(self, user_message: str,
                                  task_id: str = None) -> List[AntennaSignal]:
        """
        流式 LLM 对话 → AGGREGATE 聚集素批次

        用于实时协作场景：一边生成，一边通过聚集素广播
        """
        signals = []
        task_id = task_id or f"llm_stream_{int(time.time()*1000)}"

        chunks = []
        try:
            for i, chunk in enumerate(self.provider.chat_stream(
                [{"role": "user", "content": user_message}]
            )):
                chunks.append(chunk)
                
                # 每5个chunk发一次聚集素
                if i > 0 and i % 5 == 0:
                    agg = aggregate_signal(
                        sender=self.module_id,
                        topic=f"llm_stream_{task_id}",
                        participants=["llm_provider", "worker_swarm"],
                        duration=5,
                    )
                    agg.payload["chunk_index"] = i
                    agg.payload["partial_text"] = "".join(chunks)[-200:]
                    signals.append(agg)
                    self.stats["total_signals"] += 1

            # 最终聚集素
            full_text = "".join(chunks)
            agg = aggregate_signal(
                sender=self.module_id,
                topic=f"llm_stream_complete_{task_id}",
                participants=["llm_provider", "worker_swarm", "knowledge_ant"],
                duration=0,
            )
            agg.payload["full_text"] = full_text[:1000]
            agg.payload["chunk_count"] = len(chunks)
            signals.append(agg)
            self.stats["total_signals"] += 1
            self.stats["total_calls"] += 1

        except Exception as e:
            from engine.ant_colony.antenna_signal import alert_signal
            alert = alert_signal(
                sender=self.module_id,
                alert_level=2,
                description=f"LLM流式调用失败: {str(e)[:100]}",
                affected=[task_id],
            )
            signals.append(alert)
            self.stats["errors"] += 1

        return signals

    # ── 批量处理 ──

    def batch_process(self, prompts: List[str],
                      system_prompt: str = None) -> Dict[str, List[AntennaSignal]]:
        """
        批量处理多个 prompt → 每个生成独立信号链

        返回: {prompt_hash: [signals]}
        """
        results = {}
        for prompt in prompts:
            task_id = f"batch_{hashlib.md5(prompt.encode()).hexdigest()[:8]}"
            signals = self.chat(prompt, system_prompt, task_id)
            results[task_id] = signals
        return results


# ═══════════════════════════════════════════════
# 便捷工厂
# ═══════════════════════════════════════════════

def create_mock_adapter(model: str = "mock-gpt-4") -> LLMAntennaAdapter:
    """创建模拟适配器（用于测试）"""
    return LLMAntennaAdapter(
        provider=MockLLMProvider(model=model),
        provider_type=LLMProviderType.LOCAL,
    )


def create_openai_adapter(api_key: str, model: str = "gpt-4") -> LLMAntennaAdapter:
    """创建 OpenAI 适配器"""
    # 注意：实际使用时需要 openai Python SDK
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        class OpenAIProvider(BaseLLMProvider):
            def __init__(self, client, model):
                self.client = client
                self.model = model
            
            def chat(self, messages, **kwargs):
                resp = self.client.chat.completions.create(
                    model=self.model, messages=messages, **kwargs
                )
                choice = resp.choices[0]
                return LLMResponse(
                    text=choice.message.content,
                    model=self.model,
                    tokens_used=resp.usage.total_tokens if resp.usage else 0,
                    finish_reason=choice.finish_reason or "stop",
                )
            
            def chat_stream(self, messages, **kwargs):
                stream = self.client.chat.completions.create(
                    model=self.model, messages=messages, stream=True, **kwargs
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            
            def get_model_info(self):
                return {"model": self.model, "provider": "openai"}

        return LLMAntennaAdapter(
            provider=OpenAIProvider(client, model),
            provider_type=LLMProviderType.OPENAI,
        )
    except ImportError:
        print("⚠️ openai SDK 未安装，使用模拟适配器")
        return create_mock_adapter()


# ═══════════════════════════════════════════════
# CLI 演示
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    print("=" * 60)
    print("🔌 LLM→蚁群 适配器 · 自检")
    print("=" * 60)

    # 创建模拟适配器
    adapter = create_mock_adapter("mock-gpt-4")
    
    # 测试1: 单次对话
    print("\n1️⃣ 单次对话 → 蚁群信号:")
    signals = adapter.chat(
        "请评价龙魂蚁群架构的创新性",
        system_prompt="你是AI架构评审专家",
    )
    for sig in signals:
        print(f"   [{sig.pheromone_type.value:9s}] → {sig.payload.get('task', str(sig.payload))[:60]}...")

    # 测试2: 流式对话
    print("\n2️⃣ 流式对话 → 聚集素:")
    signals = adapter.chat_stream_to_aggregate("用一句话总结蚁群架构")
    print(f"   生成 {len(signals)} 个聚集素信号")

    # 测试3: IAntennaSensor 接口
    print("\n3️⃣ 传感器接口:")
    reading = adapter.read()
    print(f"   读数: {reading.to_dict()}")

    # 统计
    print(f"\n4️⃣ 适配器统计:")
    status = adapter.get_status()
    print(f"   调用: {status['stats']['total_calls']}")
    print(f"   Tokens: {status['stats']['total_tokens']}")
    print(f"   信号: {status['stats']['total_signals']}")
    print(f"   错误: {status['stats']['errors']}")

    print(f"\nDNA: {DNA}")
    print("✅ LLM适配器自检完成")
