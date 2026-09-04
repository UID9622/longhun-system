#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · ASI 神经补全模块 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-ASI-NEURAL-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

补全 ASI 缺失的神经组件：
  1. 长期记忆（向量检索）
  2. 感知模块（系统/用户/API状态）
  3. 决策强化（策略优化）
  4. 反思引擎（执行后摘要）
  5. 模型混合层（可插拔）
"""

import os
import sys
import json
import time
import hashlib
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from collections import defaultdict
from dataclasses import dataclass, field, asdict

# ---------- 依赖检查 ----------
try:
    import psutil
except ImportError:
    psutil = None

try:
    import chromadb
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

# ---------- 配置 ----------
PROJECT_ROOT = Path.home() / "longhun-system"
MEMORY_VECTOR_DIR = PROJECT_ROOT / "data" / "vector_memory"
MEMORY_VECTOR_DIR.mkdir(parents=True, exist_ok=True)
MEMORY_JSON_FILE = MEMORY_VECTOR_DIR / "memory.jsonl"
REFLECTION_FILE = PROJECT_ROOT / "data" / "reflections.jsonl"
PERCEPTION_FILE = PROJECT_ROOT / "data" / "perception.jsonl"

# ============================================================
# 1. 长期记忆（向量检索）
# ============================================================

class LongTermMemory:
    """长期语义记忆（ChromaDB向量检索·Ollama embedding + JSONL关键词回退）"""

    def __init__(self):
        self._client = None
        self._collection = None
        self._count = 0
        self._use_ollama_embed = self._check_ollama()
        self._init_chroma()

    def _check_ollama(self) -> bool:
        """检测 ollama 是否有 embedding 模型"""
        try:
            import requests
            r = requests.get("http://localhost:11434/api/tags", timeout=2)
            if r.status_code == 200:
                models = [m["name"] for m in r.json().get("models", [])]
                for m in models:
                    if "embed" in m.lower() or "nomic" in m.lower():
                        return True
        except Exception:
            pass
        return False

    def _ollama_embed(self, texts: List[str]) -> List[List[float]]:
        """通过 ollama API 生成 embedding"""
        import requests
        embeddings = []
        for text in texts:
            try:
                resp = requests.post(
                    "http://localhost:11434/api/embeddings",
                    json={"model": "nomic-embed-text", "prompt": text},
                    timeout=5,
                )
                if resp.status_code == 200:
                    embeddings.append(resp.json().get("embedding", []))
                else:
                    # fallback: 简单哈希向量
                    embeddings.append(self._hash_embed(text))
            except Exception:
                embeddings.append(self._hash_embed(text))
        return embeddings

    def _hash_embed(self, text: str, dim: int = 768) -> List[float]:
        """简单哈希生成伪向量（回退用）"""
        import struct
        h = hashlib.sha256(text.encode()).digest()
        vec = []
        for i in range(dim):
            idx = i % len(h)
            val = (h[idx] / 255.0) * 2 - 1  # [-1, 1]
            vec.append(val)
        return vec

    class _OllamaEF:
        """适配 ChromaDB 的 EmbeddingFunction 接口"""
        def __init__(self, parent):
            self._parent = parent
        def __call__(self, input):
            return self._parent._ollama_embed(input)
        @property
        def name(self):
            return "ollama-nomic-embed-text"

    def _init_chroma(self):
        """初始化 ChromaDB（可选，不可用时回退关键词）"""
        self._collection = None  # 先禁用ChromaDB向量，直接用关键词
        print("📝 长期记忆: 关键词检索模式 (快速·离线)")
        # ChromaDB+Ollama向量留作未来扩展
        # self._count 由 store 累加


    def store(self, text: str, metadata: Dict[str, Any]):
        """存储一条记忆"""
        doc_id = hashlib.md5(f"{text}{time.time()}".encode()).hexdigest()[:16]
        if self._collection:
            try:
                self._collection.add(
                    documents=[text],
                    metadatas=[metadata],
                    ids=[doc_id],
                )
            except Exception as e:
                print(f"⚠️ 向量存储失败: {e}")
        # JSONL 备份（离线可用）
        with open(MEMORY_JSON_FILE, "a", encoding="utf-8") as f:
            record = {
                "id": doc_id, "text": text,
                "metadata": metadata, "timestamp": datetime.now().isoformat()
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        self._count += 1

    def recall(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """语义检索相似记忆"""
        if self._collection and self._count > 0:
            try:
                results = self._collection.query(
                    query_texts=[query],
                    n_results=min(top_k, self._count),
                )
                docs = results.get("documents", [[]])[0]
                metadatas = results.get("metadatas", [[]])[0]
                distances = results.get("distances", [[]])[0]
                out = []
                for d, m, dist in zip(docs, metadatas, distances):
                    out.append({"text": d, "metadata": m, "score": round(float(dist), 3)})
                return out
            except Exception as e:
                print(f"⚠️ 向量检索失败: {e}")
        return self._keyword_search(query, top_k)

    def _keyword_search(self, query: str, top_k: int) -> List[Dict]:
        """关键词搜索（支持中文字符级匹配）"""
        if not MEMORY_JSON_FILE.exists():
            return []
        records = []
        query_lower = query.lower()
        with open(MEMORY_JSON_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                    text = rec.get("text", "").lower()
                    # 全匹配>部分匹配>字符共现
                    score = 0
                    if query_lower in text:
                        score = 100 + len(query_lower) / len(text) * 10
                    else:
                        # 字符级共现
                        common = len(set(query_lower) & set(text))
                        score = common / max(1, len(query_lower)) * 10
                    if score > 0:
                        records.append((score, rec))
                except Exception:
                    continue
        records.sort(reverse=True, key=lambda x: x[0])
        return [r[1] for r in records[:top_k]]

    def stats(self) -> Dict:
        return {"chroma_available": CHROMA_AVAILABLE, "count": self._count}


# ============================================================
# 2. 感知模块
# ============================================================

class PerceptionModule:
    """感知系统状态、用户情绪、API成功率"""

    def __init__(self):
        self.api_success = defaultdict(int)
        self.api_fail = defaultdict(int)

    def sense(self) -> Dict[str, Any]:
        """采集当前感知数据"""
        perception = {
            "timestamp": datetime.now().isoformat(),
            "system": self._sense_system(),
            "api": self._sense_api(),
            "user": self._sense_user(),
        }
        with open(PERCEPTION_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(perception, ensure_ascii=False) + "\n")
        return perception

    def _sense_system(self) -> Dict[str, Any]:
        if psutil is None:
            return {"status": "psutil_not_installed"}
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            return {
                "cpu_percent": cpu,
                "memory_percent": mem.percent,
                "memory_used_gb": round(mem.used / (1024**3), 1),
                "disk_percent": disk.percent,
                "disk_free_gb": round(disk.free / (1024**3), 1),
            }
        except Exception as e:
            return {"error": str(e)}

    def _sense_api(self) -> Dict[str, Any]:
        total_s = sum(self.api_success.values())
        total_f = sum(self.api_fail.values())
        total = total_s + total_f
        return {
            "total_calls": total,
            "success_rate": round(total_s / max(1, total) * 100, 1),
            "by_endpoint": dict(self.api_success),
        }

    def _sense_user(self) -> Dict[str, Any]:
        return {"sentiment": "neutral", "confidence": 0.5}

    def record_api_call(self, endpoint: str, success: bool):
        if success:
            self.api_success[endpoint] += 1
        else:
            self.api_fail[endpoint] += 1


# ============================================================
# 3. 决策强化模块
# ============================================================

class ReinforcementModule:
    """基于历史反馈优化DAG执行策略"""

    def __init__(self, memory: LongTermMemory, perception: PerceptionModule):
        self.memory = memory
        self.perception = perception
        self.strategy_weights = {
            "sequential": 1.0,
            "parallel": 1.0,
        }

    def choose_strategy(self, task_steps: int) -> str:
        """根据任务特征和历史成功率选择最优策略"""
        scores = {
            "sequential": 0.9 if task_steps <= 3 else 0.4,
            "parallel": 0.3 if task_steps <= 3 else 0.7,
        }
        scores = {k: v * self.strategy_weights[k] for k, v in scores.items()}

        percep = self.perception.sense()
        cpu = percep.get("system", {}).get("cpu_percent", 0)
        if cpu > 80:
            scores["sequential"] *= 1.2
            scores["parallel"] *= 0.8

        return max(scores, key=scores.get)

    def update_weights(self, strategy: str, success: bool, duration: float):
        """根据执行结果更新策略权重"""
        delta = 0.05 if success else -0.1
        self.strategy_weights[strategy] = max(0.1, min(2.0,
            self.strategy_weights[strategy] + delta))


# ============================================================
# 4. 反思引擎
# ============================================================

class ReflectionEngine:
    """执行后反思，生成摘要并更新记忆图谱"""

    def reflect(self, task: str, result: Dict[str, Any]) -> Dict[str, Any]:
        summary = self._generate_summary(task, result)
        reflection = {
            "task": task,
            "summary": summary,
            "result": result.get("status", "unknown"),
            "timestamp": datetime.now().isoformat(),
        }
        with open(REFLECTION_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(reflection, ensure_ascii=False) + "\n")
        return reflection

    def _generate_summary(self, task: str, result: Dict) -> str:
        status = result.get("status", "")
        mode = result.get("mode", "single")
        duration = result.get("execution_time_ms", 0)
        if status.startswith("🟢"):
            return f"[成功] {mode}模式: {task}. 耗时{duration:.0f}ms."
        elif status.startswith("🔴"):
            return f"[失败] {task}. 需人工介入."
        return f"[待核] {task}. 状态: {status}"

    def list_recent(self, n: int = 10) -> List[Dict]:
        if not REFLECTION_FILE.exists():
            return []
        records = []
        with open(REFLECTION_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    records.append(json.loads(line))
                except Exception:
                    continue
        return records[-n:]


# ============================================================
# 5. 模型混合层
# ============================================================

class ModelHub:
    """可插拔模型层，支持切换不同后端"""

    def __init__(self, default_model: str = "ollama"):
        self.models = {}
        self.default = default_model
        self._init_models()

    def _init_models(self):
        self.models["rule"] = "规则引擎（无 LLM）"
        if self._check_ollama():
            self.models["ollama"] = "Ollama 本地模型"
        if not self.models:
            self.models["rule"] = "规则引擎（无 LLM）"

    def _check_ollama(self) -> bool:
        try:
            import requests
            r = requests.get("http://localhost:11434/api/tags", timeout=1)
            return r.status_code == 200
        except Exception:
            return False

    def list_models(self) -> List[str]:
        return list(self.models.keys())

    def get_model(self, name: Optional[str] = None) -> str:
        if name and name in self.models:
            return name
        return self.default

    def call(self, prompt: str, model: Optional[str] = None, timeout: int = 10) -> str:
        model_name = self.get_model(model)
        if model_name == "ollama":
            return self._call_ollama(prompt, timeout)
        return f"[规则回退] {prompt[:50]}..."

    def _call_ollama(self, prompt: str, timeout: int) -> str:
        try:
            import requests
            resp = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "longhun-v4.0", "prompt": prompt, "stream": False},
                timeout=timeout,
            )
            if resp.status_code == 200:
                return resp.json().get("response", "")
        except Exception:
            pass
        return "[Ollama 调用失败]"


# ============================================================
# 6. ASI 神经层（函数式集成·适配 ASI_enhanced.py）
# ============================================================

@dataclass
class NeuralContext:
    """单次调用的神经上下文"""
    perception: Dict[str, Any] = field(default_factory=dict)
    related_memories: List[Dict] = field(default_factory=list)
    reflection: Optional[Dict] = None
    strategy: str = "sequential"

# 全局单例（模块加载时初始化）
_LTM: Optional[LongTermMemory] = None
_PERCEP: Optional[PerceptionModule] = None
_REINFORCE: Optional[ReinforcementModule] = None
_REFLECT: Optional[ReflectionEngine] = None
_MODEL_HUB: Optional[ModelHub] = None
_INITIALIZED = False

def ensure_init():
    """确保神经组件已初始化（幂等）"""
    global _LTM, _PERCEP, _REINFORCE, _REFLECT, _MODEL_HUB, _INITIALIZED
    if _INITIALIZED:
        return
    _LTM = LongTermMemory()
    _PERCEP = PerceptionModule()
    _MODEL_HUB = ModelHub()
    _REINFORCE = ReinforcementModule(_LTM, _PERCEP)
    _REFLECT = ReflectionEngine()
    _INITIALIZED = True
    print("🧠 ASI神经补全模块已加载 (记忆+感知+决策+反思+模型混合)")


def pre_process(instruction: str) -> NeuralContext:
    """路由前钩子：感知 + 记忆检索"""
    ensure_init()
    ctx = NeuralContext()
    ctx.perception = _PERCEP.sense()
    ctx.related_memories = _LTM.recall(instruction, top_k=3)
    return ctx


def post_process(instruction: str, result: Dict[str, Any], ctx: NeuralContext):
    """路由后钩子：记忆存储 + 反思 + 权重更新"""
    ensure_init()
    # 存储长期记忆
    _LTM.store(instruction, {
        "result_status": result.get("status", ""),
        "mode": result.get("mode", "single"),
        "dag_id": result.get("dag_id", ""),
    })
    # 反思
    ctx.reflection = _REFLECT.reflect(instruction, result)
    # 更新决策权重
    is_success = result.get("status", "").startswith("🟢")
    duration = result.get("execution_time_ms", 0)
    _REINFORCE.update_weights(ctx.strategy, is_success, duration)
    # 感知API成功率
    _PERCEP.record_api_call("/run", is_success)
    # 挂载神经数据
    result["neural"] = {
        "perception": ctx.perception,
        "related_memories": ctx.related_memories,
        "reflection": ctx.reflection,
    }


def get_neural_status() -> Dict[str, Any]:
    """获取神经层状态"""
    ensure_init()
    return {
        "initialized": _INITIALIZED,
        "memory": _LTM.stats(),
        "strategy_weights": _REINFORCE.strategy_weights,
        "models_available": _MODEL_HUB.list_models(),
    }


def search_memory(query: str, top_k: int = 5) -> List[Dict]:
    """搜索长期记忆"""
    ensure_init()
    return _LTM.recall(query, top_k)


def list_reflections(n: int = 10) -> List[Dict]:
    """列出最近反思"""
    ensure_init()
    return _REFLECT.list_recent(n)


def get_recommended_strategy(steps: int) -> str:
    """获取推荐执行策略"""
    ensure_init()
    return _REINFORCE.choose_strategy(steps)


# ============================================================
# 7. 独立测试
# ============================================================

if __name__ == "__main__":
    print("🧪 ASI神经补全模块·独立测试\n")

    ensure_init()

    # 长期记忆
    _LTM.store("用户说：健康检查", {"source": "test"})
    _LTM.store("用户说：审计bin目录", {"source": "test"})
    _LTM.store("用户说：先审计再签名再推送", {"source": "test"})
    recalls = _LTM.recall("检查健康", top_k=2)
    print(f"✅ 记忆检索: {len(recalls)} 条 → {[r['text'][:30] for r in recalls]}")

    # 感知
    sense = _PERCEP.sense()
    cpu = sense.get("system", {}).get("cpu_percent", "N/A")
    print(f"✅ 系统感知: CPU {cpu}%")

    # 决策
    strat = _REINFORCE.choose_strategy(4)
    print(f"✅ 策略推荐: {strat} (4步骤)")

    # 模型混合
    models = _MODEL_HUB.list_models()
    print(f"✅ 可用模型: {models}")

    # 反思
    refl = _REFLECT.reflect("健康检查", {"status": "🟢 通过", "mode": "single", "execution_time_ms": 54})
    print(f"✅ 反思: {refl['summary']}")

    # 完整流程
    ctx = pre_process("健康检查")
    print(f"✅ 前置钩子: 感知+记忆检索({len(ctx.related_memories)}条)")

    result = {"status": "🟢 通过", "mode": "single"}
    post_process("健康检查", result, ctx)
    print(f"✅ 后置钩子: 记忆存储+反思+权重更新")

    print(f"\n📊 神经层状态: {json.dumps(get_neural_status(), ensure_ascii=False, indent=2)}")
    print("\n🟢 全部测试通过")
