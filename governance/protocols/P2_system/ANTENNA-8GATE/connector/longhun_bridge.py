#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷇比-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# ============================================================
# 龍魂 · longhun 模型对接桥
# 功能：蚁触神经网 + 五行调度器 → Ollama longhun:latest
# DNA：#龍芯⚡️丙午·癸未·壬戌·丙午·䷀乾为天-LONGHUN-BRIDGE-v5.0
# ============================================================

import sys, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'core'))
sys.path.insert(0, os.path.join(BASE, 'scheduler'))

import numpy as np
import json
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

from antenna_mesh import AntennaMesh, Bagua, PheromonePacket
from wuxing_scheduler import WuxingScheduler, WuxingTask, Wuxing


@dataclass
class LonghunMessage:
    role: str  # system / user / assistant
    content: str
    timestamp: float = 0.0
    dna_trace: str = ""


class LonghunBridge:
    """
    longhun 模型推理桥
    路径：用户输入 → 五行调度 → 蚁触路由 → Ollama API → 返回 + DNA追溯
    """
    def __init__(self, ollama_host: str = "http://localhost:11434",
                 model_name: str = "longhun-v4.1.1-bind:latest",
                 use_antenna: bool = True,
                 use_wuxing: bool = True):
        self.ollama_host = ollama_host
        self.model_name = model_name
        self.use_antenna = use_antenna
        self.use_wuxing = use_wuxing

        self.mesh = AntennaMesh(nodes_per_bagua=4, dim=512) if use_antenna else None
        self.scheduler = WuxingScheduler() if use_wuxing else None

        self.history: List[LonghunMessage] = []
        self.total_requests = 0
        self.total_latency = 0.0
        self.total_tokens = 0

    def _text_to_vector(self, text: str) -> np.ndarray:
        chars = [ord(c) % 256 for c in text[:512]]
        vec = np.zeros(512)
        vec[:len(chars)] = np.array(chars) / 255.0
        return vec

    def _vector_to_bagua(self, vec: np.ndarray) -> Bagua:
        energy = np.sum(vec.reshape(8, 64), axis=1)
        idx = np.argmax(energy)
        return list(Bagua)[idx]

    def _detect_wuxing(self, text: str) -> Wuxing:
        keywords = {
            Wuxing.木: ['过滤', '清洗', '安全', '防护', '解毒'],
            Wuxing.火: ['调度', '紧急', '优先', '快速'],
            Wuxing.土: ['转化', '兼容', '格式', '翻译', '适配'],
            Wuxing.金: ['输入', '输出', 'IO', '网络', '传输'],
            Wuxing.水: ['存储', '记忆', '持久', '保存', '缓存']
        }
        scores = {w: sum(1 for k in words if k in text) for w, words in keywords.items()}
        return max(scores, key=scores.get)

    def chat(self, user_input: str, system_prompt: str = "") -> Dict[str, Any]:
        start_time = time.time()
        self.total_requests += 1

        input_vec = self._text_to_vector(user_input)

        if self.use_wuxing and self.scheduler:
            wx = self._detect_wuxing(user_input)
            task = WuxingTask(
                task_id=f"req-{self.total_requests:06d}",
                wuxing=wx,
                priority=0 if any(k in user_input for k in ['安全', '主权', 'P0']) else 1,
                payload=input_vec
            )
            self.scheduler.submit(task)

        antenna_stats = {}
        if self.use_antenna and self.mesh:
            target_bagua = self._vector_to_bagua(input_vec)
            routed_vec, antenna_stats = self.mesh.inference(input_vec, target_bagua)
        else:
            antenna_stats = {'enabled': False}

        # Ollama API call (fallback to local processing if unavailable)
        try:
            import requests
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            for msg in self.history[-10:]:
                messages.append({"role": msg.role, "content": msg.content})
            messages.append({"role": "user", "content": user_input})

            response = requests.post(
                f"{self.ollama_host}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": 2048}
                },
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            assistant_content = result.get("message", {}).get("content", "")
        except Exception as e:
            assistant_content = f"[龍魂桥接·Ollama未就绪] {str(e)}"

        latency = time.time() - start_time
        self.total_latency += latency

        dna = self._generate_dna(user_input, assistant_content, latency)

        self.history.append(LonghunMessage("user", user_input, time.time(), dna))
        self.history.append(LonghunMessage("assistant", assistant_content, time.time(), dna))

        return {
            "content": assistant_content,
            "dna_trace": dna,
            "latency_ms": round(latency * 1000, 2),
            "model": self.model_name,
            "antenna_stats": antenna_stats,
            "wuxing": self._detect_wuxing(user_input).name if self.use_wuxing else "disabled",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def _generate_dna(self, input_text: str, output_text: str, latency: float) -> str:
        hash_input = hash(input_text + output_text) % 100000000
        timestamp = time.strftime("%y%m%d%H%M%S")
        return f"#龍芯⚡️丙午·癸未·壬戌·乾为天-LONGHUN-{timestamp}-{hash_input:08X}-v5.0"

    def get_stats(self) -> Dict[str, Any]:
        avg_latency = self.total_latency / max(self.total_requests, 1)
        return {
            "total_requests": self.total_requests,
            "avg_latency_ms": round(avg_latency * 1000, 2),
            "model": self.model_name,
            "antenna_enabled": self.use_antenna,
            "wuxing_enabled": self.use_wuxing,
            "history_length": len(self.history),
            "scheduler_balance": self.scheduler.get_balance_report() if self.scheduler else None
        }

    def clear_history(self):
        self.history.clear()


# ============================================================
# 自测
# ============================================================
if __name__ == "__main__":
    bridge = LonghunBridge()
    print("龍魂桥接器启动")
    print(f"模型：{bridge.model_name}")
    print(f"蚁触神经网：{'启用' if bridge.use_antenna else '禁用'}")
    print(f"五行调度器：{'启用' if bridge.use_wuxing else '禁用'}")

    test_input = "测试：龍魂系统状态检查"
    result = bridge.chat(test_input, system_prompt="你是龍魂系统助手，UID9622专属。")
    print(f"\n输入：{test_input}")
    print(f"DNA：{result['dna_trace']}")
    print(f"延迟：{result['latency_ms']} ms")
    print(f"五行：{result['wuxing']}")
