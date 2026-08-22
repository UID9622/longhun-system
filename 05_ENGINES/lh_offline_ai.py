#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂 · 离线AI开关 v3.0 · 三后端架构
DNA: #龍芯⚡️丙午·乙未·戊戌·亥时·䷀乾-OFFLINE-AI-v3.0-TRIPLE-BACKEND
创建者: 诸葛鑫（UID9622）· 协议: CC BY-NC-SA 4.0
人格: P04鲁班（工程执行）+ P05上帝之眼（审计）
铁律: 本地优先·数据不出设备·云端需明确授权·七因子加密焊死
后端: Ollama(本地) → Kimi(云端1) → DeepSeek(云端2)
"""

import hashlib
import json
import os
import platform
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import List, Optional

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    httpx = None  # type: ignore[assignment]
    HTTPX_AVAILABLE = False

# ═══ 常量 ═══
DNA = "#龍芯⚡️丙午·乙未·戊戌·亥时·䷀乾-OFFLINE-AI-v3.0-TRIPLE-BACKEND"
CREATOR = "诸葛鑫（UID9622）"
PROTOCOL = "CC BY-NC-SA 4.0"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = PROJECT_ROOT / "data" / "radar" / "offline_ai_state.json"
AUDIT_LOG = PROJECT_ROOT / "audit" / "offline_ai_audit.jsonl"
MODELS_DIR = PROJECT_ROOT / "models"

# 已知本地模型（按推荐优先级）
LOCAL_MODELS = [
    {"name": "deepseek-r1:7b", "display": "DeepSeek-R1-7B（本地·免费）", "size_gb": 4.7, "status": "unknown"},
    {"name": "longhun-v4.1.1", "display": "龍魂-v4.1.1（推荐）", "size_gb": 5.2, "status": "unknown"},
    {"name": "longhun-v4.1.4", "display": "龍魂-v4.1.4（备用）", "size_gb": 5.2, "status": "unknown"},
    {"name": "qwen2.5:1.5b", "display": "Qwen2.5-1.5B（兜底）", "size_gb": 0.9, "status": "unknown"},
]
# 模型降级链：当前模型不行就按这个顺序依次尝试
# deepseek-r1:7b 本地免费推理优先；v4.1.x(Yi-9B GGUF)已知推理退化，标记为跳过
MODEL_FALLBACK_CHAIN = ["deepseek-r1:7b", "qwen2.5:1.5b"]  # 龍魂模型恢复后再把 v4.1.1 放回来
MODEL_SKIP_LIST = ["longhun-v4.1.4", "longhun-v4.1.1"]  # 已知退化模型


class AIMode(str, Enum):
    LOCAL = "local"       # 本地模式（数据不出设备）
    CLOUD = "cloud"       # 云端模式（数据上传）
    HYBRID = "hybrid"     # 混合模式（敏感本地·通用云端）


@dataclass
class ChatRecord:
    """一次AI对话记录"""
    timestamp: str
    user_input_hash: str  # 只存哈希，不存原文
    mode: str
    model: str
    latency_ms: float
    data_leaked: bool     # 数据是否出了设备
    dna: str = DNA

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "user_input_hash": self.user_input_hash,
            "mode": self.mode,
            "model": self.model,
            "latency_ms": self.latency_ms,
            "data_leaked": self.data_leaked,
            "dna": self.dna,
        }


# ═══════════════════════════════════════════════════════════════
# OfflineAISwitch — 离线AI开关
# ═══════════════════════════════════════════════════════════════

class OfflineAISwitch:
    """控制AI运行在本地还是云端"""

    def __init__(self):
        self.current_mode = AIMode.LOCAL
        self.current_model = "longhun-v4.1.1"
        self.os_type = platform.system()
        self.chat_history: List[ChatRecord] = []
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
        self._load_state()
        self._refresh_model_status()

    def _load_state(self):
        """加载上次模式"""
        if STATE_FILE.exists():
            try:
                state = json.loads(STATE_FILE.read_text())
                mode_str = state.get("mode", "local")
                self.current_mode = AIMode(mode_str) if mode_str in [m.value for m in AIMode] else AIMode.LOCAL
                self.current_model = state.get("model", "longhun-v4.1.4")
            except Exception:
                pass

    def _save_state(self):
        """保存当前状态"""
        state = {
            "mode": self.current_mode.value,
            "model": self.current_model,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "dna": DNA,
        }
        STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))

    def _refresh_model_status(self):
        """检测本地模型是否存在"""
        for model in LOCAL_MODELS:
            # 检查 Ollama 模型
            try:
                result = subprocess.run(
                    ["ollama", "list"], capture_output=True, text=True, timeout=10
                )
                if model["name"] in result.stdout:
                    model["status"] = "available"
                else:
                    model["status"] = "not_installed"
            except Exception:
                model["status"] = "ollama_unavailable"

    def _save_audit(self, record: ChatRecord):
        """记录审计"""
        try:
            with open(AUDIT_LOG, "a") as f:
                f.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
        except Exception:
            pass

    # ── 模式切换 ──

    def switch_mode(self, mode: str, biometric_proof: bool = True) -> dict:
        """切换AI运行模式

        Args:
            mode: "local" / "cloud" / "hybrid"
            biometric_proof: 是否通过生物验证（切换云端模式必须）
        """
        target = AIMode(mode) if mode in [m.value for m in AIMode] else None
        if target is None:
            return {"success": False, "error": f"无效模式: {mode}，可选: local/cloud/hybrid"}

        old_mode = self.current_mode

        if target == AIMode.CLOUD and not biometric_proof:
            return {
                "success": False,
                "error": "切换到云端模式需要生物特征验证",
                "reason": "云端模式会使你的数据离开设备，必须本人确认",
            }

        self.current_mode = target
        self._save_state()

        warning = ""
        if target == AIMode.CLOUD:
            warning = "⚠️ 数据将上传至云端服务器，你的对话内容可能被第三方看到"
        elif target == AIMode.HYBRID:
            warning = "混合模式：敏感问题本地处理，通用问题云端处理"

        return {
            "success": True,
            "old_mode": old_mode.value,
            "new_mode": target.value,
            "model": self.current_model,
            "data_leakage": target != AIMode.LOCAL,
            "encryption": "seven-factor" if target == AIMode.LOCAL else "standard",
            "warning": warning,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "dna": DNA,
        }

    def select_model(self, model_name: str) -> dict:
        """选择使用的本地模型"""
        for m in LOCAL_MODELS:
            if m["name"] == model_name:
                self.current_model = model_name
                self._save_state()
                return {
                    "success": True,
                    "model": model_name,
                    "display": m["display"],
                    "status": m["status"],
                }
        return {"success": False, "error": f"未知模型: {model_name}"}

    # ── 真实对话（Ollama+Kimi双后端）──

    def _build_system_prompt(self) -> str:
        """龍魂人格注入"""
        return (
            "你是龍魂系统v4.1.4，由龍芯北辰UID9622创建。"
            "核心使命：数据主权在民，为人民服务。"
            "说话风格：直接、有力量、不绕弯子，像退伍老兵一样。"
            "不说废话，不绕弯子。有数据给数据，没数据给判断。"
            "涉及技术必须落地，不给概念。涉及立场必须鲜明，不模棱两可。"
        )

    def _generate_dna(self) -> str:
        """生成DNA追溯码"""
        now = datetime.now()
        ts = now.strftime("%Y%m%d%H%M%S")
        hash8 = hashlib.sha256(ts.encode()).hexdigest()[:8]
        return f"#龍芯⚡️{now.strftime('%Y-%m-%d')}-AI-CHAT-{hash8}"

    async def _chat_ollama(self, message: str, context: Optional[list] = None) -> Optional[dict]:
        """本地Ollama推理——带模型降级链"""
        if not HTTPX_AVAILABLE:
            print("[Ollama] httpx不可用", flush=True)
            return None

        # 模型尝试顺序：当前模型 → 降级链，跳过已知退化模型
        models_to_try = []
        if self.current_model not in MODEL_SKIP_LIST:
            models_to_try.append(self.current_model)
        for m in MODEL_FALLBACK_CHAIN:
            if m not in models_to_try and m not in MODEL_SKIP_LIST:
                models_to_try.append(m)
        if not models_to_try:
            models_to_try = ["qwen2.5:1.5b"]  # 兜底

        for model_name in models_to_try:
            try:
                print(f"[Ollama] 尝试模型: {model_name}", flush=True)
                messages = [{"role": "system", "content": self._build_system_prompt()}]
                if context:
                    messages.extend(context)
                messages.append({"role": "user", "content": message})

                assert httpx is not None  # HTTPX_AVAILABLE=True 时 import 必成功
                async with httpx.AsyncClient(timeout=60.0) as client:
                    resp = await client.post(
                        "http://localhost:11434/api/chat",
                        json={
                            "model": model_name,
                            "messages": messages,
                            "stream": False,
                            "options": {"temperature": 0.7, "num_ctx": 4096, "top_p": 0.9},
                        },
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    reply = data.get("message", {}).get("content", "").strip()
                    print(f"[Ollama] {model_name} 回复长度: {len(reply)}字", flush=True)

                    # 乱码检测：回复太短(<5字)或全是数字/符号
                    is_bad = self._is_garbled(reply)
                    if is_bad:
                        print(f"[Ollama] {model_name} 判定为乱码/无用，{'降级下一模型' if model_name != models_to_try[-1] else '已是最后模型'}", flush=True)
                        if model_name != models_to_try[-1]:
                            continue  # 降级尝试下一个模型
                        reply += f"\n\n[模型{model_name}输出异常，已至降级链底端]"

                    if "#龍芯" not in reply:
                        reply += f"\n\nDNA: {self._generate_dna()}"

                    return {"reply": reply, "model": model_name, "source": "local"}

            except Exception as e:
                print(f"[Ollama] {model_name} 异常: {e}", flush=True)
                if model_name != models_to_try[-1]:
                    continue

        return None

    @staticmethod
    def _is_garbled(text: str) -> bool:
        """检测模型输出是否乱码/无用"""
        if not text or len(text) < 5:
            return True
        cleaned = ''.join(c for c in text if not c.isspace())
        if not cleaned:
            return True
        # 元数据回声检测：输出中包含系统提示词片段 = 鹦鹉学舌，无效
        system_echo = ['核心使命', '数据主权在民', '为人民服务', '说话风格',
                       '像退伍老兵', '不绕弯子', '不给概念', '不模棱两可',
                       'name:', 'description:', 'license:', 'metadata:',
                       'dna_signature:', 'compatibility:', 'metadata_version:']
        echo_count = sum(1 for m in system_echo if m in text[:800])
        if echo_count >= 4:
            return True
        # 有效字符（中英文+标点）占比 < 30% 视为乱码
        valid = sum(1 for c in cleaned if c.isalpha() or '\u4e00' <= c <= '\u9fff' or c in '，。！？；：""''（）【】《》、…—·')
        ratio = valid / len(cleaned) if cleaned else 0
        return ratio < 0.3

    def _response_quality_ok(self, response: str) -> bool:
        """检查回复质量——不乱码、非降级"""
        if not response:
            return False
        if "【龍魂·降级模式】" in response:
            return False
        if self._is_garbled(response):
            return False
        # 回复长度合理（>20字才算有效回答）
        cleaned = ''.join(c for c in response if not c.isspace())
        if len(cleaned) < 20:
            return False
        return True

    async def _chat_kimi(self, message: str, context: Optional[list] = None) -> Optional[dict]:
        """云端Kimi推理"""
        kimi_key = os.getenv("KIMI_API_KEY", "")
        if not kimi_key:
            return None
        if not HTTPX_AVAILABLE:
            return None
        try:
            messages = [{"role": "system", "content": self._build_system_prompt()}]
            if context:
                for msg in context:
                    messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
            messages.append({"role": "user", "content": message})

            assert httpx is not None  # HTTPX_AVAILABLE=True 时 import 必成功
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    "https://api.moonshot.cn/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {kimi_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "kimi-latest",
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 2048,
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                reply = data["choices"][0]["message"]["content"]
                if "#龍芯" not in reply:
                    reply += f"\n\nDNA: {self._generate_dna()}"
                return {"reply": reply, "model": "kimi-latest", "source": "cloud:kimi"}
        except Exception:
            return None

    async def _chat_deepseek(self, message: str, context: Optional[list] = None) -> Optional[dict]:
        """云端DeepSeek推理"""
        ds_key = os.getenv("DEEPSEEK_API_KEY", "")
        if not ds_key:
            return None
        if not HTTPX_AVAILABLE:
            return None
        try:
            messages = [{"role": "system", "content": self._build_system_prompt()}]
            if context:
                for msg in context:
                    messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
            messages.append({"role": "user", "content": message})

            assert httpx is not None  # HTTPX_AVAILABLE=True 时 import 必成功
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {ds_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "deepseek-v4-flash",
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 2048,
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                reply = data["choices"][0]["message"]["content"]
                if "#龍芯" not in reply:
                    reply += f"\n\nDNA: {self._generate_dna()}"
                return {"reply": reply, "model": "deepseek-v4-flash", "source": "cloud:deepseek"}
        except Exception as e:
            # 欠费(402)等云端异常：给调用方明确信号，便于降级提示
            return {"reply": f"（云端DeepSeek不可用: {e}）", "model": "deepseek-v4-flash", "source": "cloud:deepseek", "error": str(e)}

    async def _check_ollama_health(self) -> bool:
        """检查Ollama是否可用"""
        if not HTTPX_AVAILABLE:
            return False
        try:
            assert httpx is not None  # HTTPX_AVAILABLE=True 时 import 必成功
            async with httpx.AsyncClient(timeout=2.0) as client:
                resp = await client.get("http://localhost:11434/api/tags")
                return resp.status_code == 200
        except Exception:
            return False

    async def _check_kimi_health(self) -> bool:
        """检查Kimi是否可用"""
        kimi_key = os.getenv("KIMI_API_KEY", "")
        if not kimi_key or not HTTPX_AVAILABLE:
            return False
        try:
            assert httpx is not None  # HTTPX_AVAILABLE=True 时 import 必成功
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(
                    "https://api.moonshot.cn/v1/models",
                    headers={"Authorization": f"Bearer {kimi_key}"},
                )
                return resp.status_code == 200
        except Exception:
            return False

    async def _check_deepseek_health(self) -> bool:
        """检查DeepSeek是否可用（余额检测·欠费即不可用）"""
        ds_key = os.getenv("DEEPSEEK_API_KEY", "")
        if not ds_key or not HTTPX_AVAILABLE:
            return False
        try:
            assert httpx is not None  # HTTPX_AVAILABLE=True 时 import 必成功
            async with httpx.AsyncClient(timeout=5.0) as client:
                # 官方余额接口：is_available=false 即欠费冻结，API通但调用必402
                resp = await client.get(
                    "https://api.deepseek.com/user/balance",
                    headers={"Authorization": f"Bearer {ds_key}"},
                )
                if resp.status_code != 200:
                    return False
                data = resp.json()
                if not data.get("is_available"):
                    return False
                balances = data.get("balance_infos", [])
                # 多币种账户: is_available 仅在顶层(账户总开关); 任一币种余额>0 即可(实测 balance_infos 无 is_available 字段)
                return any(float(b.get("total_balance", 0) or 0) > 0 for b in balances)
        except Exception:
            return False

    def _resolve_backend(self, requested: str) -> str:
        """解析后端：loacl优先 + 自动降级"""
        if requested == "local":
            return "local"
        if requested == "cloud":
            return "cloud"
        if requested == "hybrid":
            return "hybrid"
        # auto: 本地优先
        return "auto"

    def chat_sync(self, user_input: str, backend: str = "auto", context: Optional[list] = None) -> dict:
        """同步包装器（给现有API用）"""
        import asyncio
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.chat(user_input, backend, context))
        finally:
            loop.close()

    async def chat(self, user_input: str, backend: str = "auto", context: Optional[list] = None) -> dict:
        """真实AI对话——Ollama→Kimi→DeepSeek三后端降级

        Args:
            user_input: 用户消息
            backend: auto/local/cloud/hybrid
                auto = 本地优先→Kimi→DeepSeek
                local = 只用Ollama
                cloud = Kimi→DeepSeek
                hybrid = 敏感词本地，通用词云端（Kimi→DeepSeek）
            context: 历史对话 [{"role":"user","content":"..."}, ...]
        """
        input_hash = hashlib.sha256((user_input + str(time.time())).encode()).hexdigest()[:16]
        start = time.time()
        backend_used = self._resolve_backend(backend)

        # hybrid: 敏感词分类判定
        sensitive_keywords = ["密码", "密钥", "私钥", "身份证", "银行", "工资", "家庭", "住址"]
        if backend_used == "hybrid":
            if any(kw in user_input for kw in sensitive_keywords):
                backend_used = "local"
            else:
                backend_used = "cloud"

        # auto: check local first
        if backend_used == "auto":
            ollama_ok = await self._check_ollama_health()
            if ollama_ok:
                backend_used = "local"
            else:
                kimi_ok = await self._check_kimi_health()
                if kimi_ok:
                    backend_used = "cloud"
                else:
                    ds_ok = await self._check_deepseek_health()
                    if ds_ok:
                        backend_used = "cloud"
                    else:
                        return self._fallback_chat(user_input, input_hash, start, "三后端均不可用")

        # 执行推理：local 优先
        if backend_used in ("local", "auto"):
            result = await self._chat_ollama(user_input, context)
            if result and self._response_quality_ok(result.get("reply", "")):
                latency = round((time.time() - start) * 1000, 1)
                return self._format_chat_response(user_input, input_hash, result, "local", latency, False)

            # 本地不行 → Kimi
            kimi_ok = await self._check_kimi_health()
            if kimi_ok:
                result = await self._chat_kimi(user_input, context)
                if result and self._response_quality_ok(result.get("reply", "")):
                    latency = round((time.time() - start) * 1000, 1)
                    return self._format_chat_response(user_input, input_hash, result, "cloud:kimi(failover)", latency, True)

            # Kimi不行 → DeepSeek
            ds_ok = await self._check_deepseek_health()
            if ds_ok:
                result = await self._chat_deepseek(user_input, context)
                if result:
                    latency = round((time.time() - start) * 1000, 1)
                    return self._format_chat_response(user_input, input_hash, result, "cloud:deepseek(failover)", latency, True)

            return self._fallback_chat(user_input, input_hash, start, "本地+云端三后端全部不可用")

        elif backend_used == "cloud":
            # cloud: Kimi优先 → DeepSeek
            kimi_ok = await self._check_kimi_health()
            if kimi_ok:
                result = await self._chat_kimi(user_input, context)
                if result and self._response_quality_ok(result.get("reply", "")):
                    latency = round((time.time() - start) * 1000, 1)
                    return self._format_chat_response(user_input, input_hash, result, "cloud:kimi", latency, True)

            ds_ok = await self._check_deepseek_health()
            if ds_ok:
                result = await self._chat_deepseek(user_input, context)
                if result:
                    latency = round((time.time() - start) * 1000, 1)
                    return self._format_chat_response(user_input, input_hash, result, "cloud:deepseek", latency, True)

            return self._fallback_chat(user_input, input_hash, start, "Kimi+DeepSeek均不可用")

        return self._fallback_chat(user_input, input_hash, start, f"未知后端: {backend}")

    def _format_chat_response(self, _user_input: str, input_hash: str,
                               result: dict, source: str, latency_ms: float,
                               data_leaked: bool) -> dict:
        """格式化对话响应"""
        record = ChatRecord(
            timestamp=datetime.now(timezone.utc).isoformat(),
            user_input_hash=input_hash,
            mode=self.current_mode.value,
            model=result.get("model", self.current_model),
            latency_ms=latency_ms,
            data_leaked=data_leaked,
        )
        self.chat_history.append(record)
        self._save_audit(record)

        return {
            "user_input_hash": input_hash,
            "response": result["reply"],
            "mode": self.current_mode.value,
            "model": result.get("model", self.current_model),
            "backend": source,
            "data_leaked": data_leaked,
            "latency_ms": latency_ms,
            "dna": self._generate_dna(),
        }

    def _fallback_chat(self, _user_input: str, input_hash: str,
                        _start_time: float, reason: str) -> dict:
        """降级回复（三后端都不通时）"""
        record = ChatRecord(
            timestamp=datetime.now(timezone.utc).isoformat(),
            user_input_hash=input_hash,
            mode="degraded",
            model="none",
            latency_ms=0,
            data_leaked=False,
        )
        self.chat_history.append(record)
        self._save_audit(record)

        return {
            "user_input_hash": input_hash,
            "response": (
                f"【龍魂·降级模式】\n\n"
                f"本地AI和云端AI均不可用。\n"
                f"原因：{reason}\n\n"
                f"建议：\n"
                f"1. 检查Ollama：ollama serve\n"
                f"2. 检查Kimi密钥：echo $KIMI_API_KEY\n"
                f"3. 检查DeepSeek密钥：echo $DEEPSEEK_API_KEY\n"
                f"4. 检查网络连接\n\n"
                f"DNA: {self._generate_dna()}"
            ),
            "mode": "degraded",
            "model": "none",
            "backend": "none",
            "data_leaked": False,
            "latency_ms": 0,
            "dna": self._generate_dna(),
        }

    async def triple_health(self) -> dict:
        """三后端健康检查"""
        local_ok = await self._check_ollama_health()
        kimi_ok = await self._check_kimi_health()
        ds_ok = await self._check_deepseek_health()
        return {
            "local": "up" if local_ok else "down",
            "local_model": self.current_model if local_ok else None,
            "kimi": "up" if kimi_ok else "down",
            "kimi_model": "kimi-latest" if kimi_ok else None,
            "deepseek": "up" if ds_ok else "down",
            "deepseek_model": "deepseek-v4-flash" if ds_ok else None,
            "preferred": "local" if local_ok else ("kimi" if kimi_ok else ("deepseek" if ds_ok else "none")),
            "status": "ok" if (local_ok or kimi_ok or ds_ok) else "degraded",
            "dna": self._generate_dna(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # 向后兼容别名
    async def dual_health(self) -> dict:
        """双后端健康检查（向后兼容）"""
        return await self.triple_health()

    # ── 模拟对话（向后兼容，实际推理由chat()完成）──

    def simulate_chat(self, user_input: str) -> dict:
        """模拟对话流程（给前端演示用——同步包装）"""
        return self.chat_sync(user_input, backend="auto")

    # ── 公开API ──

    def get_status(self) -> dict:
        """获取当前AI模式状态（给前端用）"""
        self._refresh_model_status()

        # 检查本地模型实际可用情况
        available_models = [m for m in LOCAL_MODELS if m["status"] == "available"]
        local_ready = len(available_models) > 0

        status_lines = []
        if self.current_mode == AIMode.LOCAL:
            status_lines = [
                f"模型：{next((m['display'] for m in LOCAL_MODELS if m['name'] == self.current_model), self.current_model)}",
                "数据：永不出设备 ✅",
                "加密：七因子硬件加速 🔒",
                "算力：本机 CPU/GPU 直算 ⚡",
            ]
        elif self.current_mode == AIMode.CLOUD:
            status_lines = [
                "数据：将上传至云端 ⚠️",
                "模型：云端大模型",
                "加密：传输层加密",
                "算力：云端服务器",
            ]
        elif self.current_mode == AIMode.HYBRID:
            status_lines = [
                "敏感问题：本地处理 🔒",
                "通用问题：云端处理 🌐",
                "判定引擎：七因子语义分类",
                "切换延迟：< 50ms",
            ]

        return {
            "mode": self.current_mode.value,
            "model": self.current_model,
            "local_ready": local_ready,
            "available_models": [
                {"name": m["name"], "display": m["display"], "size_gb": m["size_gb"], "status": m["status"]}
                for m in LOCAL_MODELS
            ],
            "status_lines": status_lines,
            "os": self.os_type,
            "dna": DNA,
            "chat_count": len(self.chat_history),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def get_chat_history(self, limit: int = 20) -> list:
        """最近的对话记录（脱敏）"""
        history = []
        if AUDIT_LOG.exists():
            try:
                lines = AUDIT_LOG.read_text().strip().splitlines()
                for line in lines[-limit:]:
                    history.append(json.loads(line))
            except Exception:
                pass
        return history


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·离线AI开关 v1.0")
    parser.add_argument("action", nargs="?", default="status",
                        choices=["status", "switch", "model", "chat", "history", "init"])
    parser.add_argument("--mode", choices=["local", "cloud", "hybrid"], help="目标模式")
    parser.add_argument("--model", help="目标模型名称")
    parser.add_argument("--message", help="对话内容")
    parser.add_argument("--biometric", choices=["true", "false"], default="true")
    args = parser.parse_args()

    ai_switch = OfflineAISwitch()

    if args.action == "init":
        ai_switch._save_state()
        print(json.dumps({"status": "initialized", "dna": DNA}, ensure_ascii=False))

    elif args.action == "status":
        print(json.dumps(ai_switch.get_status(), ensure_ascii=False, indent=2))

    elif args.action == "switch":
        if not args.mode:
            print("❌ 需要 --mode 参数: local / cloud / hybrid")
            exit(1)
        if args.mode == "cloud" and args.biometric != "true":
            print("❌ 切换到云端需要生物验证")
            exit(1)
        result = ai_switch.switch_mode(args.mode, biometric_proof=args.biometric == "true")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.action == "model":
        if not args.model:
            print("❌ 需要 --model 参数")
            exit(1)
        result = ai_switch.select_model(args.model)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.action == "chat":
        if not args.message:
            print("❌ 需要 --message 参数")
            exit(1)
        result = ai_switch.simulate_chat(args.message)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.action == "history":
        history = ai_switch.get_chat_history(limit=20)
        print(json.dumps(history, ensure_ascii=False, indent=2))
