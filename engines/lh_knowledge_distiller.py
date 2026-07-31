# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 统一知识蒸馏引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-KNOWLEDGE-DISTILLER-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

核心理念：
  别人的开源模型是大豆，我们是榨油厂。大豆是别人的，榨出来的油是自己的。
  只蒸馏公开可用的知识，纯本地处理，不上传云端。

蒸馏源:
  1. DeepSeek V3/R1 — 完全开源，直接本地MLX推理蒸馏
  2. Kimi K3 — 闭源，从对话历史间接蒸馏
  3. 小米 MiLM — 闭源，从对话历史间接蒸馏（预留）

四步蒸馏管线:
  侦察(scan) → 蒸馏(distill) → 炼化(refine) → 入库(merge)

铁律:
  - 只蒸馏公开可用的知识，不碰商业机密或私有数据
  - 所有蒸馏数据纯本地处理，不上传云端
  - 蒸馏后数据必须打DNA追溯码，标注来源模型
  - 质量闸门 ≥0.7 才入库

用法:
  python3 engines/lh_knowledge_distiller.py scan              # 侦察所有蒸馏源
  python3 engines/lh_knowledge_distiller.py distill --source deepseek  # 蒸馏DeepSeek
  python3 engines/lh_knowledge_distiller.py distill --source kimi      # 蒸馏Kimi
  python3 engines/lh_knowledge_distiller.py distill --source all       # 蒸馏全部
  python3 engines/lh_knowledge_distiller.py refine                    # 炼化入库
  python3 engines/lh_knowledge_distiller.py status                    # 蒸馏状态
  python3 engines/lh_knowledge_distiller.py report                    # 蒸馏报告
"""

import hashlib, json, os, re, sys, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict, Counter


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 路径常量和全局配置
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SYSTEM_ROOT = Path(__file__).parent.parent
DATA_DIR = SYSTEM_ROOT / "data"
DISTILL_DIR = DATA_DIR / "distill"
DISTILL_DIR.mkdir(parents=True, exist_ok=True)
TRAINING_DATA_DIR = DATA_DIR / "training"
MODELS_DIR = SYSTEM_ROOT / "models"

# DeepSeek MLX 权重路径
DEEPSEEK_MLX_PATH = MODELS_DIR / "longhun-v1.0" / "deepseek-r1-distill-llama-8b-mlx"
DEEPSEEK_WEIGHTS_PATH = MODELS_DIR / "longhun-v1.0" / "DeepSeek-R1-Distill-Llama-8B"

# Kimi 对话路径
KIMI_CHATS_DIR = SYSTEM_ROOT / "knowledge" / "ai-chats" / "kimi"
# 小米预留
XIAOMI_CHATS_DIR = SYSTEM_ROOT / "knowledge" / "ai-chats" / "xiaomi"

# 质量闸门
QUALITY_GATE = 0.7
MIN_CONTENT_LENGTH = 80   # 回复最少字符数
MAX_SAMPLES_PER_SOURCE = 5000

# 蒸馏锚词库（用于质量评分和分类）
ANCHOR_WORDS = {
    "龍魂体系": ["龍魂", "CNSH", "UID9622", "诸葛鑫", "三才", "369", "河图洛书", "八卦", "五行为", "人格", "DNA追溯"],
    "安全审计": ["安全", "漏洞", "审计", "熔断", "渗透", "防火墙", "加密", "隐私"],
    "模型训练": ["模型", "训练", "MLX", "LoRA", "权重", "checkpoint", "微调", "推理"],
    "开发编程": ["代码", "函数", "API", "Python", "import", "class", "def", "算法"],
    "部署运维": ["部署", "服务器", "鲲鹏", "docker", "systemd", "launchd", "端口"],
    "哲学思维": ["哲学", "易经", "道德经", "太极", "阴阳", "五行", "天干地支", "卦"],
    "社会人文": ["人民", "中国", "法律", "公平", "底线", "价值观", "文化", "历史"],
}

# 推理链检测模式（DeepSeek R1 特有）
REASONING_PATTERNS = [
    r'思维链[：:]\s*(.+?)(?=\n\n|\Z)',
    r'推理过程[：:]\s*(.+?)(?=\n\n|\Z)',
    r'(?:首先|第一步|Step\s*1)[：:]\s*(.+)',
    r'(?:综上所述|因此|所以|总之)[，,]\s*(.+)',
    r'<think[^>]*>(.+?)</think>',
    r'理由[：:]\s*(.+?)(?=\n|$)',
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 数据结构
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class DistillSample:
    """单条蒸馏样本"""
    sample_id: str
    source: str                           # deepseek / kimi / xiaomi
    source_model: str                     # DeepSeek-R1 / Kimi-K3 / MiLM
    messages: List[Dict[str, str]]        # ChatML 格式
    reasoning_chain: str = ""             # 推理链（如有）
    quality_score: float = 0.5
    domain: str = ""
    original_hash: str = ""               # 来源哈希
    dna: str = ""
    extracted_at: str = ""
    tags: List[str] = field(default_factory=list)


@dataclass
class DistillReport:
    """蒸馏批次报告"""
    source: str
    batch_id: str
    total_candidates: int = 0
    passed_quality: int = 0
    after_dedup: int = 0
    domains: Dict[str, int] = field(default_factory=dict)
    avg_quality: float = 0.0
    reasoning_samples: int = 0
    dna: str = ""
    errors: List[str] = field(default_factory=list)
    started_at: str = ""
    finished_at: str = ""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SimHash 去重
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SimHasher:
    """64位 SimHash 去重器"""
    
    @staticmethod
    def hash(text: str) -> int:
        """对文本做 SimHash，返回 64 位整数"""
        if not text:
            return 0
        # 字符级 n-gram (1-3)
        grams = []
        chars = list(text)
        for n in (1, 2, 3):
            for i in range(len(chars) - n + 1):
                grams.append(''.join(chars[i:i+n]))
        
        v = [0] * 64
        for gram in grams:
            h = hashlib.md5(gram.encode()).digest()
            h_int = int.from_bytes(h[:8], 'big')
            for j in range(64):
                if (h_int >> j) & 1:
                    v[j] += 1
                else:
                    v[j] -= 1
        
        result = 0
        for j in range(64):
            if v[j] > 0:
                result |= (1 << j)
        return result & 0xFFFFFFFFFFFFFFFF

    @staticmethod
    def hamming_distance(a: int, b: int) -> int:
        x = a ^ b
        return x.bit_count()

    @staticmethod
    def is_duplicate(a: int, b: int, threshold: int = 3) -> bool:
        """汉明距离 ≤ threshold 视为重复"""
        return SimHasher.hamming_distance(a, b) <= threshold


class Deduplicator:
    """样本去重器"""
    
    def __init__(self):
        self.hashes: Set[int] = set()
        self.fingerprints: List[int] = []
    
    def dedup(self, samples: List[DistillSample]) -> List[DistillSample]:
        """去重：完全匹配 + SimHash 近似匹配"""
        unique = []
        seen_messages = set()
        
        for s in samples:
            # 1. 完全匹配检查
            content_key = hashlib.sha256(
                json.dumps(s.messages, ensure_ascii=False, sort_keys=True).encode()
            ).hexdigest()
            if content_key in seen_messages:
                continue
            seen_messages.add(content_key)
            
            # 2. SimHash 近似检查
            text = " ".join(m.get("content", "") for m in s.messages)
            sh = SimHasher.hash(text)
            is_dup = False
            for existing in self.hashes:
                if SimHasher.is_duplicate(sh, existing, threshold=3):
                    is_dup = True
                    break
            
            if is_dup:
                continue
            
            self.hashes.add(sh)
            unique.append(s)
        
        return unique


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DeepSeek 蒸馏器（直接 MLX 推理）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DeepSeekDistiller:
    """DeepSeek V3/R1 直接蒸馏
    
    策略：
    1. 加载本地 MLX 权重
    2. 用训练数据作为 prompt
    3. 让 DeepSeek 生成回复
    4. 提取推理链（R1 特有）
    5. 生成对比训练样本
    """
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
    
    def _load_model(self):
        """加载 MLX 模型（懒加载）"""
        if self.model_loaded:
            return
        
        mlx_path = str(DEEPSEEK_MLX_PATH) if DEEPSEEK_MLX_PATH.exists() else str(DEEPSEEK_WEIGHTS_PATH)
        
        try:
            import mlx.core as mx
            from mlx_lm import load, generate
            
            if DEEPSEEK_MLX_PATH.exists():
                print(f"🧠 加载 DeepSeek MLX 模型: {DEEPSEEK_MLX_PATH.name}")
                self.model, self.tokenizer = load(mlx_path)
            else:
                # 尝试从原始权重转换
                print(f"🧠 DeepSeek 权重路径: {mlx_path}")
                if DEEPSEEK_WEIGHTS_PATH.exists():
                    from mlx_lm import convert
                    print("🔄 转换为 MLX 格式...")
                    convert(DEEPSEEK_WEIGHTS_PATH, mlx_path=mlx_path)
                    self.model, self.tokenizer = load(mlx_path)
                else:
                    raise FileNotFoundError(f"DeepSeek 权重未找到: {mlx_path}")
            
            self.model_loaded = True
            print("✅ DeepSeek MLX 模型加载成功")
        except ImportError:
            print("⚠️ mlx/mlx_lm 未安装，将使用 API 回退方式")
            self.model_loaded = False
        except Exception as e:
            print(f"⚠️ 模型加载失败: {e}")
            self.model_loaded = False
    
    def _generate(self, prompt: str, max_tokens: int = 512) -> str:
        """生成 DeepSeek 回复"""
        if not self.model_loaded:
            return ""
        
        from mlx_lm import generate
        
        messages = [{"role": "user", "content": prompt}]
        prompt_text = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        
        response = generate(
            self.model, self.tokenizer,
            prompt=prompt_text,
            max_tokens=max_tokens,
            temp=0.7,
        )
        return response
    
    def extract_reasoning_chain(self, text: str) -> str:
        """从 DeepSeek R1 回复中提取推理链"""
        for pattern in REASONING_PATTERNS:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                chain = match.group(1).strip()
                if len(chain) > 20:
                    return chain
        
        # 兜底：查找推理指示词之后的文本块
        indicators = ["让我一步步思考", "分析如下", "推理:", "思考过程:"]
        for ind in indicators:
            idx = text.find(ind)
            if idx >= 0:
                tail = text[idx + len(ind):]
                # 取接下来500字符
                chain = tail[:500].strip()
                if len(chain) > 20:
                    return chain
        
        return ""
    
    def distill(self, max_samples: int = 500) -> Tuple[List[DistillSample], DistillReport]:
        """执行 DeepSeek 蒸馏"""
        self._load_model()
        
        report = DistillReport(
            source="deepseek",
            batch_id=f"ds_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        
        samples = []
        
        # 加载训练数据作为蒸馏 prompt
        training_files = sorted(TRAINING_DATA_DIR.glob("*.jsonl")) if TRAINING_DATA_DIR.exists() else []
        
        if not training_files:
            # 使用对话历史作为替代
            training_files = list((DATA_DIR / "raw_conversations").glob("*.jsonl"))
        
        if self.model_loaded and training_files:
            print(f"🔬 DeepSeek 蒸馏开始，候选数据: {len(training_files)} 文件")
            
            for tf in training_files[:3]:
                try:
                    with open(tf, 'r', encoding='utf-8') as f:
                        for line in f:
                            if len(samples) >= max_samples:
                                break
                            if not line.strip():
                                continue
                            
                            record = json.loads(line)
                            messages = record.get("messages", [])
                            if not messages:
                                continue
                            
                            # 取最后一条 user 消息作为 prompt
                            user_msgs = [m for m in messages if m.get("role") == "user"]
                            if not user_msgs:
                                continue
                            
                            prompt = user_msgs[-1].get("content", "")[:1000]
                            if len(prompt) < MIN_CONTENT_LENGTH:
                                continue
                            
                            # 生成 DeepSeek 回复
                            response = self._generate(prompt)
                            if not response or len(response) < MIN_CONTENT_LENGTH:
                                continue
                            
                            # 提取推理链
                            reasoning = self.extract_reasoning_chain(response)
                            
                            # 构建对比样本（原有回复 vs DeepSeek回复）
                            assistant_msgs = [m for m in messages if m.get("role") == "assistant"]
                            original_response = assistant_msgs[-1].get("content", "") if assistant_msgs else ""
                            
                            # 蒸馏样本包含原始问答 + DeepSeek 回答
                            sample_msgs = [
                                {"role": "system", "content": "你是龍魂AI助手。请基于以下问题给出专业、有深度的回答。"},
                                {"role": "user", "content": prompt},
                                {"role": "assistant", "content": response},
                            ]
                            
                            quality = self._score_quality(response, reasoning)
                            
                            if quality >= QUALITY_GATE:
                                sample = DistillSample(
                                    sample_id=f"ds_{hashlib.sha256(prompt.encode()).hexdigest()[:12]}",
                                    source="deepseek",
                                    source_model="DeepSeek-R1-Distill-Llama-8B",
                                    messages=sample_msgs,
                                    reasoning_chain=reasoning,
                                    quality_score=quality,
                                    domain=self._classify(prompt + response),
                                    original_hash=hashlib.sha256(original_response.encode()).hexdigest()[:16],
                                    extracted_at=datetime.now(timezone.utc).isoformat(),
                                    tags=["deepseek", "distill", "local-mlx"],
                                )
                                if reasoning:
                                    sample.tags.append("reasoning-chain")
                                samples.append(sample)
                                report.reasoning_samples += (1 if reasoning else 0)
                            report.total_candidates += 1
                            
                except Exception as e:
                    report.errors.append(f"{tf.name}: {e}")
        else:
            # 回退：从已有 DeepSeek 对话中提取
            print("🔬 DeepSeek 离线蒸馏模式（从已有对话提取）")
            samples = self._fallback_distill(max_samples, report)
            report.total_candidates = len(samples)
        
        # 质量闸门
        passed = [s for s in samples if s.quality_score >= QUALITY_GATE]
        report.passed_quality = len(passed)
        
        # 去重
        dedup = Deduplicator()
        unique = dedup.dedup(passed)
        report.after_dedup = len(unique)
        
        # 统计领域分布
        for s in unique:
            report.domains[s.domain] = report.domains.get(s.domain, 0) + 1
        
        report.avg_quality = sum(s.quality_score for s in unique) / max(len(unique), 1)
        report.finished_at = datetime.now(timezone.utc).isoformat()
        
        return unique, report
    
    def _fallback_distill(self, max_samples: int, report: DistillReport) -> List[DistillSample]:
        """离线模式：从已有 DeepSeek 对话导出提取高质量回复"""
        samples = []
        raw_conv = DATA_DIR / "raw_conversations"
        if not raw_conv.exists():
            return samples
        
        for jf in sorted(raw_conv.glob("*.jsonl")):
            try:
                with open(jf, 'r', encoding='utf-8') as f:
                    for line in f:
                        if len(samples) >= max_samples:
                            break
                        if not line.strip():
                            continue
                        record = json.loads(line)
                        messages = record.get("messages", [])
                        if len(messages) < 2:
                            continue
                        
                        # 提取高质量的 assistant 回复
                        assistant_msgs = [m for m in messages if m.get("role") == "assistant"]
                        for am in assistant_msgs:
                            content = am.get("content", "")
                            if len(content) < MIN_CONTENT_LENGTH:
                                continue
                            
                            quality = self._score_quality(content)
                            if quality < QUALITY_GATE:
                                continue
                            
                            user_msgs = [m for m in messages if m.get("role") == "user"]
                            prompt = user_msgs[0].get("content", "") if user_msgs else ""
                            
                            reasoning = self.extract_reasoning_chain(content)
                            
                            # 构建蒸馏样本
                            sample_msgs = [
                                {"role": "system", "content": "你是龍魂AI助手。"},
                                {"role": "user", "content": prompt[:1000]},
                                {"role": "assistant", "content": content[:2000]},
                            ]
                            
                            sample = DistillSample(
                                sample_id=f"ds_fb_{hashlib.sha256(content.encode()).hexdigest()[:12]}",
                                source="deepseek",
                                source_model="DeepSeek-Chat-Export",
                                messages=sample_msgs,
                                reasoning_chain=reasoning,
                                quality_score=quality,
                                domain=self._classify(content),
                                original_hash=hashlib.sha256(content.encode()).hexdigest()[:16],
                                extracted_at=datetime.now(timezone.utc).isoformat(),
                                tags=["deepseek", "fallback", "dialogue-extract"],
                            )
                            if reasoning:
                                sample.tags.append("reasoning-chain")
                                report.reasoning_samples += 1
                            samples.append(sample)
            except Exception as e:
                report.errors.append(f"fallback {jf.name}: {e}")
        
        return samples[:max_samples]
    
    def _score_quality(self, text: str, reasoning: str = "") -> float:
        """DeepSeek 回复质量评分"""
        score = 0.4
        if len(text) > 500:
            score += 0.15
        if len(text) > 1000:
            score += 0.1
        if reasoning:
            score += 0.2
        # 锚词匹配
        for domain_words in ANCHOR_WORDS.values():
            hits = sum(1 for w in domain_words if w in text)
            if hits >= 3:
                score += 0.1
                break
        # 结构性加分
        if re.search(r'(?:首先|其次|最后|第一|第二|第三)', text):
            score += 0.05
        if re.search(r'(?:综上所述|因此|所以|总之)', text):
            score += 0.05
        
        return min(score, 1.0)
    
    def _classify(self, text: str) -> str:
        """领域分类"""
        for domain, words in ANCHOR_WORDS.items():
            hits = sum(1 for w in words if w in text)
            if hits >= 2:
                return domain
        return "通用"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Kimi 蒸馏器（从对话历史间接蒸馏）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class KimiDistiller:
    """Kimi K3 间接蒸馏
    
    从 knowledge/ai-chats/kimi/ 和历史对话中提取高质量 Kimi 回复，
    转换为训练格式。
    """
    
    def __init__(self):
        pass
    
    def distill(self, max_samples: int = 500) -> Tuple[List[DistillSample], DistillReport]:
        report = DistillReport(
            source="kimi",
            batch_id=f"kimi_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        
        samples = []
        
        # 1. 从 Kimi JSON 对话提取
        if KIMI_CHATS_DIR.exists():
            json_sessions = self._from_json(max_samples)
            samples.extend(json_sessions)
            print(f"📄 Kimi JSON: {len(json_sessions)} 条")
        
        # 2. 从 Kimi 纯文本提取
        if KIMI_CHATS_DIR.exists():
            txt_sessions = self._from_text(max_samples - len(samples))
            samples.extend(txt_sessions)
            print(f"📝 Kimi TXT: {len(txt_sessions)} 条")
        
        # 3. 从 Chat Importer 的导出中提取（如果有）
        imported = self._from_chat_import(max_samples - len(samples))
        samples.extend(imported)
        if imported:
            print(f"📦 ChatImport: {len(imported)} 条")
        
        samples = samples[:max_samples]
        report.total_candidates = len(samples)
        
        # 质量闸门
        passed = [s for s in samples if s.quality_score >= QUALITY_GATE]
        report.passed_quality = len(passed)
        
        # 去重
        dedup = Deduplicator()
        unique = dedup.dedup(passed)
        report.after_dedup = len(unique)
        
        # 统计
        for s in unique:
            report.domains[s.domain] = report.domains.get(s.domain, 0) + 1
        report.avg_quality = sum(s.quality_score for s in unique) / max(len(unique), 1)
        report.finished_at = datetime.now(timezone.utc).isoformat()
        
        return unique, report
    
    def _from_json(self, max_n: int) -> List[DistillSample]:
        """从 Kimi JSON 对话中提取
        
        Kimi Web 导出 JSON 格式:
          [{"title": "...", "lines": N, "preview": "...", "content": "..."}]
        
        其中 content 包含完整的对话内容，格式为:
          标题
          [空行]
          用户消息（含参考链接）
          [UI元素: 复制/获取网页/编辑/分享]
          Kimi 回复
        """
        samples = []
        json_files = sorted(KIMI_CHATS_DIR.glob("*.json"), key=lambda f: f.stat().st_size, reverse=True)
        
        # UI干扰元素
        UI_NOISE = re.compile(
            r'\b(?:复制|编辑|分享|获取网页|新建会话|⌘\s*K|邀请有奖|抢会员权益|升级|已置顶|收起|查看全部)\b'
        )
        
        for jf in json_files[:5]:
            if len(samples) >= max_n:
                break
            try:
                data = json.loads(jf.read_text(encoding='utf-8'))
                
                if isinstance(data, list):
                    items = data
                elif isinstance(data, dict):
                    items = [data]
                else:
                    continue
                
                for item in items:
                    if len(samples) >= max_n:
                        break
                    
                    title = item.get("title", "")
                    content = item.get("content", "")
                    
                    if not content or len(content) < 200:
                        continue
                    
                    # 策略：将每个conversation切割为"用户问题 + Kimi回答"
                    # Kimi导出的content中，用户消息后通常跟着参考链接，然后是Kimi的回答
                    segments = self._split_kimi_web_content(content, title)
                    
                    for seg in segments:
                        if len(samples) >= max_n:
                            break
                        
                        user_part = seg.get("user", "")
                        kimi_part = seg.get("kimi", "")
                        
                        if not kimi_part or len(kimi_part) < MIN_CONTENT_LENGTH:
                            continue
                        
                        # 清理UI干扰
                        kimi_part = UI_NOISE.sub('', kimi_part).strip()
                        user_part = UI_NOISE.sub('', user_part).strip()
                        
                        if len(kimi_part) < MIN_CONTENT_LENGTH:
                            continue
                        
                        quality = self._score_kimi(kimi_part)
                        if quality < QUALITY_GATE:
                            continue
                        
                        sample_id = hashlib.sha256(kimi_part.encode()).hexdigest()[:12]
                        samples.append(DistillSample(
                            sample_id=f"kimi_{sample_id}",
                            source="kimi",
                            source_model="Kimi-K3",
                            messages=[
                                {"role": "user", "content": user_part[:1500] or title},
                                {"role": "assistant", "content": kimi_part[:3000]},
                            ],
                            quality_score=quality,
                            domain=self._classify(kimi_part),
                            original_hash=hashlib.sha256(kimi_part.encode()).hexdigest()[:16],
                            extracted_at=datetime.now(timezone.utc).isoformat(),
                            tags=["kimi", "k3", "web-export"],
                        ))
                        
            except Exception as e:
                if not hasattr(self, '_errors'):
                    self._errors = []
                self._errors.append(f"Kimi JSON {jf.name}: {e}")
        
        return samples
    
    def _split_kimi_web_content(self, content: str, title: str = "") -> List[Dict[str, str]]:
        """将 Kimi Web 导出内容切分为 用户问题+Kimi回答 片段
        
        Kimi导出内容特征:
        - 开头是用户输入（含参考URL）
        - 随后是UI标记（复制/获取网页等）
        - 之后是Kimi的完整回答
        - 可能有多个对话轮次
        """
        segments = []
        
        # 方式1: 按明显的对话分隔符切分
        # 两个连续换行+标题模式可能是新的对话
        split_pattern = r'\n{3,}(?=[^\s])'
        chunks = re.split(split_pattern, content)
        
        for chunk in chunks:
            chunk = chunk.strip()
            if len(chunk) < MIN_CONTENT_LENGTH:
                continue
            
            # 估算用户部分（前 ~20% 或最多500字符）和 Kimi 回复部分（剩余）
            lines = chunk.split('\n')
            clean_lines = [l for l in lines if l.strip() and not re.match(
                r'^\s*(?:复制|编辑|分享|获取网页|新建会话)$', l.strip()
            )]
            
            if len(clean_lines) < 3:
                continue
            
            # 用户部分：前几行 + 包含URL的行
            user_lines = []
            kimi_start_idx = 0
            
            # 找到URL所在行作为用户消息边界
            for i, line in enumerate(clean_lines[:20]):
                if 'http' in line or 'csdn.net' in line or 'blog.csdn' in line:
                    user_lines = clean_lines[:i+2]  # URL行及之前
                    kimi_start_idx = i + 2
                    break
            
            if not user_lines:
                # 兜底：前3行算用户，其余算Kimi
                user_lines = clean_lines[:3]
                kimi_start_idx = 3
            
            user_part = '\n'.join(user_lines).strip()
            kimi_part = '\n'.join(clean_lines[kimi_start_idx:]).strip()
            
            if len(kimi_part) < MIN_CONTENT_LENGTH:
                # 整段都当Kimi回复处理，用标题当user
                kimi_part = '\n'.join(clean_lines).strip()
                user_part = title
            
            if len(kimi_part) >= MIN_CONTENT_LENGTH:
                segments.append({"user": user_part, "kimi": kimi_part})
        
        return segments
    
    def _from_text(self, max_n: int) -> List[DistillSample]:
        """从 Kimi 纯文本导出中提取
        
        支持两种格式:
        1. Kimi Web full.txt - 对话列表 + 对话内容
        2. Kimi Code raw.txt - 终端日志，● 标记对话
        """
        samples = []
        txt_files = sorted(KIMI_CHATS_DIR.glob("*.txt"), key=lambda f: f.stat().st_size, reverse=True)
        
        for tf in txt_files[:3]:
            if len(samples) >= max_n:
                break
            try:
                text = tf.read_text(encoding='utf-8')
                
                # 检测格式
                if 'Kimi Code' in text[:500] or 'K2.' in text[:500] or 'MCP server' in text[:500]:
                    # Kimi Code 终端日志格式 - 使用 ● 标记解析
                    code_samples = self._parse_kimi_code_raw(text, max_n - len(samples))
                    samples.extend(code_samples)
                else:
                    # Kimi Web full.txt - 使用通用对话解析
                    turns = self._parse_kimi_text_dialogue(text)
                    
                    for i, turn in enumerate(turns):
                        if len(samples) >= max_n:
                            break
                        if turn["role"] != "assistant":
                            continue
                        content = turn["content"]
                        if len(content) < MIN_CONTENT_LENGTH:
                            continue
                        
                        quality = self._score_kimi(content)
                        if quality < QUALITY_GATE:
                            continue
                        
                        preceding = []
                        for j in range(max(0, i-3), i):
                            if turns[j]["role"] == "user":
                                preceding.append(turns[j]["content"])
                        context = "\n".join(preceding[-2:]) or "请回答以下问题"
                        
                        samples.append(DistillSample(
                            sample_id=f"kimi_txt_{hashlib.sha256(content.encode()).hexdigest()[:12]}",
                            source="kimi",
                            source_model="Kimi-K3",
                            messages=[
                                {"role": "user", "content": context[:1000]},
                                {"role": "assistant", "content": content[:2000]},
                            ],
                            quality_score=quality,
                            domain=self._classify(content),
                            original_hash=hashlib.sha256(content.encode()).hexdigest()[:16],
                            extracted_at=datetime.now(timezone.utc).isoformat(),
                            tags=["kimi", "k3", "text-extract"],
                        ))
                        samples.append(samples[-1])
                        
            except Exception as e:
                if not hasattr(self, '_errors'):
                    self._errors = []
                self._errors.append(f"Kimi TXT {tf.name}: {e}")
        
        return samples
    
    def _parse_kimi_code_raw(self, text: str, max_n: int) -> List[DistillSample]:
        """解析 Kimi Code 终端日志格式
        
        格式特征:
          ● User said "..." — 用户输入
          ● [response content] — Kimi 回复
          ● Used Skill/Bash/Read — 工具调用
          ✦/✨ — 系统消息
        """
        samples = []
        
        # 提取对话对：(用户消息, 后续的Kimi回复)
        # 模式: ● User said "..." 之后跟着 ● 非工具调用的回复
        
        user_blocks = re.split(r'●\s*User said\s*"([^"]*)"', text)
        # user_blocks = [before_first, user_msg_1, after_1, user_msg_2, after_2, ...]
        
        for i in range(1, len(user_blocks), 2):
            if len(samples) >= max_n:
                break
            
            user_msg = user_blocks[i].strip()
            kimi_block = user_blocks[i + 1] if i + 1 < len(user_blocks) else ""
            
            if not kimi_block:
                continue
            
            # 从 kimi_block 中提取第一个实质性回复（跳过工具调用）
            # 提取所有 ● 块
            dot_blocks = re.split(r'\n●\s+', kimi_block)
            
            kimi_response_parts = []
            for db in dot_blocks:
                db = db.strip()
                if not db:
                    continue
                # 跳过工具调用和内部思考
                if re.match(r'(?:Used |Activated|The skill|Now I need)', db):
                    continue
                # 收集实质性回复
                kimi_response_parts.append(db)
            
            kimi_response = '\n\n'.join(kimi_response_parts).strip()
            
            # 清理
            kimi_response = re.sub(r'\n\s*\.\.\.\s*\(\d+ more lines.*?\)', '', kimi_response)
            kimi_response = re.sub(r'\n(?:✦|✨|▶)\s.*', '', kimi_response)
            
            if len(kimi_response) < MIN_CONTENT_LENGTH:
                continue
            
            quality = self._score_kimi(kimi_response)
            if quality < QUALITY_GATE:
                continue
            
            samples.append(DistillSample(
                sample_id=f"kimi_code_{hashlib.sha256(kimi_response.encode()).hexdigest()[:12]}",
                source="kimi",
                source_model="Kimi-K2.7-Code",
                messages=[
                    {"role": "user", "content": user_msg[:1500]},
                    {"role": "assistant", "content": kimi_response[:3000]},
                ],
                quality_score=quality,
                domain=self._classify(kimi_response),
                original_hash=hashlib.sha256(kimi_response.encode()).hexdigest()[:16],
                extracted_at=datetime.now(timezone.utc).isoformat(),
                tags=["kimi", "k2.7-code", "terminal-log"],
            ))
        
        return samples
    
    def _from_chat_import(self, max_n: int) -> List[DistillSample]:
        """从 Chat Importer 导出中提取 Kimi 数据"""
        samples = []
        import_dir = DATA_DIR / "chat_import"
        if not import_dir.exists():
            return samples
        
        for jf in sorted(import_dir.glob("*.jsonl"), key=lambda f: f.stat().st_mtime, reverse=True)[:2]:
            if len(samples) >= max_n:
                break
            try:
                with open(jf, 'r', encoding='utf-8') as f:
                    for line in f:
                        if len(samples) >= max_n:
                            break
                        if not line.strip():
                            continue
                        record = json.loads(line)
                        meta = record.get("metadata", {})
                        if meta.get("source") != "kimi":
                            continue
                        
                        messages = record.get("messages", [])
                        if len(messages) < 2:
                            continue
                        
                        # 只取 assistant 回复
                        for msg in messages:
                            if msg.get("role") != "assistant":
                                continue
                            content = msg.get("content", "")
                            if len(content) < MIN_CONTENT_LENGTH:
                                continue
                            
                            quality = meta.get("quality", 0.5)
                            if quality < QUALITY_GATE:
                                continue
                            
                            user_msgs = [m for m in messages if m.get("role") == "user"]
                            context = user_msgs[0].get("content", "") if user_msgs else ""
                            
                            sample = DistillSample(
                                sample_id=f"kimi_ci_{hashlib.sha256(content.encode()).hexdigest()[:12]}",
                                source="kimi",
                                source_model="Kimi-K3",
                                messages=[
                                    {"role": "user", "content": context[:1000]},
                                    {"role": "assistant", "content": content[:2000]},
                                ],
                                quality_score=quality,
                                domain=self._classify(content),
                                original_hash=hashlib.sha256(content.encode()).hexdigest()[:16],
                                extracted_at=datetime.now(timezone.utc).isoformat(),
                                tags=["kimi", "k3", "chat-import"],
                            )
                            samples.append(sample)
            except Exception as e:
                if not hasattr(self, '_errors'):
                    self._errors = []
                self._errors.append(f"ChatImport {jf.name}: {e}")
        
        return samples
    
    def _extract_conversations(self, data: Any) -> List[List[Dict]]:
        """从各种 JSON 格式中提取对话列表"""
        conversations = []
        
        if isinstance(data, list):
            # 检查是否是直接的对话列表
            if data and isinstance(data[0], dict) and "role" in data[0]:
                conversations.append(data)
            else:
                conversations.append(data)
        elif isinstance(data, dict):
            # 嵌套格式
            for key in ("conversations", "messages", "chats", "data", "items"):
                if key in data and isinstance(data[key], list):
                    nested = self._extract_conversations(data[key])
                    conversations.extend(nested)
                    break
            else:
                # 格式: {id: {messages: [...]}}
                for v in data.values():
                    if isinstance(v, dict):
                        nested = self._extract_conversations(v)
                        conversations.extend(nested)
        
        return conversations
    
    def _get_context(self, conv: List[Dict], current: Dict) -> str:
        """获取当前回复的上下文"""
        ctx_parts = []
        for item in conv:
            if item is current:
                break
            role = item.get("role", "")
            if role in ("user", "human"):
                ctx_parts.append(str(item.get("content", "")))
        return "\n".join(ctx_parts[-3:]) or "请回答以下问题"
    
    def _parse_kimi_text_dialogue(self, text: str) -> List[Dict[str, str]]:
        """解析 Kimi 纯文本对话"""
        turns = []
        lines = text.split('\n')
        current_role = None
        current_content = []
        
        role_patterns = [
            (r'^(?:User|用户|Human|我|👤)\s*[：:]\s*(.+)', 'user'),
            (r'^(?:Kimi|AI|K|Assistant|助手|🤖)\s*[：:]\s*(.+)', 'assistant'),
        ]
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_role and current_content:
                    turns.append({"role": current_role, "content": '\n'.join(current_content)})
                    current_content = []
                continue
            
            matched = False
            for pattern, role in role_patterns:
                match = re.match(pattern, line)
                if match:
                    if current_role and current_content:
                        turns.append({"role": current_role, "content": '\n'.join(current_content)})
                    current_role = role
                    current_content = [match.group(1)]
                    matched = True
                    break
            
            if not matched and current_role:
                current_content.append(line)
        
        if current_role and current_content:
            turns.append({"role": current_role, "content": '\n'.join(current_content)})
        
        return turns
    
    def _score_kimi(self, text: str) -> float:
        """Kimi 回复质量评分"""
        score = 0.35
        if len(text) > 300:
            score += 0.1
        if len(text) > 800:
            score += 0.15
        if len(text) > 1500:
            score += 0.05
        # Kimi 擅长长推理
        if re.search(r'(?:首先|其次|最后|第一步|第二步|第三)', text):
            score += 0.1
        if re.search(r'(?:综上所述|因此|所以|总之|基于以上)', text):
            score += 0.1
        # 锚词
        for domain_words in ANCHOR_WORDS.values():
            hits = sum(1 for w in domain_words if w in text)
            if hits >= 3:
                score += 0.1
                break
        # 结构化内容加分
        if re.search(r'[#*\-]\s', text):
            score += 0.05
        return min(score, 1.0)
    
    def _classify(self, text: str) -> str:
        for domain, words in ANCHOR_WORDS.items():
            if sum(1 for w in words if w in text) >= 2:
                return domain
        return "通用"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 统一蒸馏编排器
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DistillOrchestrator:
    """统一知识蒸馏编排器
    
    协调 DeepSeek + Kimi + Xiaomi 三路蒸馏，
    统一质量闸门、DNA绑定、炼化入库。
    """
    
    def __init__(self):
        self.deepseek = DeepSeekDistiller()
        self.kimi = KimiDistiller()
        self.reports: Dict[str, DistillReport] = {}
        self.all_samples: List[DistillSample] = []
        self.output_dir = DISTILL_DIR
    
    def scan(self) -> Dict[str, Dict]:
        """侦察所有蒸馏源状态"""
        sources = {}
        
        # DeepSeek
        ds_status = "🔴 未找到"
        if DEEPSEEK_MLX_PATH.exists():
            ds_status = "🟢 MLX就绪"
        elif DEEPSEEK_WEIGHTS_PATH.exists():
            ds_size = sum(f.stat().st_size for f in DEEPSEEK_WEIGHTS_PATH.rglob("*") if f.is_file()) / (1024**3)
            ds_status = f"🟡 MLX待转换 ({ds_size:.1f}GB)"
        
        deepseek_conv = DATA_DIR / "raw_conversations"
        ds_conv_count = len(list(deepseek_conv.glob("*.jsonl"))) if deepseek_conv.exists() else 0
        
        sources["deepseek"] = {
            "weights": ds_status,
            "model": "DeepSeek-R1-Distill-Llama-8B",
            "params": "8B (distill), 原版671B MoE 37B激活",
            "open_source": True,
            "method": "MLX直接推理" if DEEPSEEK_MLX_PATH.exists() else "离线对话提取",
            "conversations": ds_conv_count,
        }
        
        # Kimi
        kimi_status = "🟢 可用" if KIMI_CHATS_DIR.exists() else "🔴 无数据"
        kimi_files = []
        if KIMI_CHATS_DIR.exists():
            kimi_files = sorted(KIMI_CHATS_DIR.glob("*"), key=lambda f: f.stat().st_size, reverse=True)
        kimi_size = sum(f.stat().st_size for f in kimi_files) / (1024*1024) if kimi_files else 0
        
        sources["kimi"] = {
            "path": str(KIMI_CHATS_DIR) if KIMI_CHATS_DIR.exists() else "",
            "status": kimi_status,
            "files": len(kimi_files),
            "size_mb": round(kimi_size, 1),
            "model": "Kimi K3 (~1T MoE)",
            "open_source": False,
            "method": "对话历史间接蒸馏",
        }
        
        # Xiaomi
        sources["xiaomi"] = {
            "status": "🔴 无数据" if not XIAOMI_CHATS_DIR.exists() else "🟡 预留",
            "model": "小米 MiLM (~13B)",
            "open_source": False,
            "method": "API对话导入（待实现）",
        }
        
        # 训练数据
        train_count = 0
        if TRAINING_DATA_DIR.exists():
            train_count = sum(1 for _ in TRAINING_DATA_DIR.glob("*.jsonl"))
        sources["training_data"] = {
            "path": str(TRAINING_DATA_DIR),
            "jsonl_files": train_count,
        }
        
        return sources
    
    def distill_source(self, source: str, max_samples: int = 500) -> Tuple[List[DistillSample], DistillReport]:
        """蒸馏单个源"""
        if source == "deepseek":
            samples, report = self.deepseek.distill(max_samples=max_samples)
        elif source == "kimi":
            samples, report = self.kimi.distill(max_samples=max_samples)
        else:
            raise ValueError(f"未知蒸馏源: {source}")
        
        # 绑定 DNA
        for s in samples:
            s.dna = self._gen_dna(s)
        
        self.reports[source] = report
        return samples, report
    
    def distill_all(self, max_per_source: int = 500) -> Dict[str, Tuple[List[DistillSample], DistillReport]]:
        """全源蒸馏"""
        results = {}
        for source in ("deepseek", "kimi"):
            print(f"\n{'='*50}")
            print(f"🔬 蒸馏 {source.upper()}...")
            print(f"{'='*50}")
            try:
                samples, report = self.distill_source(source, max_samples=max_per_source)
                results[source] = (samples, report)
                self.all_samples.extend(samples)
                print(f"  ✅ 候选: {report.total_candidates} | 过质量闸: {report.passed_quality} | 去重后: {report.after_dedup}")
            except Exception as e:
                print(f"  🔴 {source} 蒸馏失败: {e}")
                self.reports[source] = DistillReport(source=source, batch_id="", 
                                                      errors=[str(e)],
                                                      started_at=datetime.now(timezone.utc).isoformat())
        
        return results
    
    def refine_and_merge(self, quality_threshold: float = QUALITY_GATE) -> Dict:
        """炼化入库：将蒸馏样本统一过筛子、去重、打DNA、合并到训练数据
        
        顺序：
        1. 全局去重（跨源去重）
        2. 质量二次筛选
        3. 绑定 DNA
        4. 导出到 distill 目录
        5. 合并到训练集
        """
        result = {
            "action": "refine_and_merge",
            "total_raw": len(self.all_samples),
            "after_global_dedup": 0,
            "after_requality": 0,
            "exported": 0,
            "merged": 0,
            "errors": [],
        }
        
        if not self.all_samples:
            print("⚠️ 无蒸馏样本，跳过炼化")
            return result
        
        # 1. 全局去重
        dedup = Deduplicator()
        unique = dedup.dedup(self.all_samples)
        result["after_global_dedup"] = len(unique)
        print(f"🔍 全局去重: {len(self.all_samples)} → {len(unique)}")
        
        # 2. 质量二次筛选
        high_quality = [s for s in unique if s.quality_score >= quality_threshold]
        result["after_requality"] = len(high_quality)
        print(f"📊 质量二次筛选: {len(unique)} → {len(high_quality)} (≥{quality_threshold})")
        
        # 3. 确保 DNA
        for s in high_quality:
            if not s.dna:
                s.dna = self._gen_dna(s)
        
        # 4. 导出到 distill 目录
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        export_path = self.output_dir / f"distill_{timestamp}.jsonl"
        
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                for s in high_quality:
                    record = {
                        "messages": s.messages,
                        "metadata": {
                            "source": s.source,
                            "source_model": s.source_model,
                            "domain": s.domain,
                            "quality": round(s.quality_score, 3),
                            "reasoning_chain": s.reasoning_chain[:500] if s.reasoning_chain else "",
                            "dna": s.dna,
                            "extracted_at": s.extracted_at,
                            "tags": s.tags,
                            "distill_method": "knowledge-distiller-v1.0",
                        }
                    }
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
            result["exported"] = len(high_quality)
            print(f"📦 导出: {len(high_quality)} 条 → {export_path.name}")
        except Exception as e:
            result["errors"].append(f"export: {e}")
        
        # 5. 合并到训练集
        try:
            TRAINING_DATA_DIR.mkdir(parents=True, exist_ok=True)
            merged_path = TRAINING_DATA_DIR / f"distilled_{timestamp}.jsonl"
            
            # 复制到训练目录
            import shutil
            shutil.copy(export_path, merged_path)
            result["merged"] = len(high_quality)
            print(f"🔗 合并训练集: {merged_path.name}")
            
            # 更新训练集索引
            index_path = TRAINING_DATA_DIR / "distill_manifest.json"
            manifest = {}
            if index_path.exists():
                manifest = json.loads(index_path.read_text(encoding='utf-8'))
            
            manifest[timestamp] = {
                "file": f"distilled_{timestamp}.jsonl",
                "samples": len(high_quality),
                "sources": Counter(s.source for s in high_quality),
                "domains": Counter(s.domain for s in high_quality),
                "avg_quality": round(sum(s.quality_score for s in high_quality) / max(len(high_quality), 1), 3),
                "dna": f"#龍芯⚡️-DISTILL-BATCH-{timestamp}",
            }
            
            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
            
        except Exception as e:
            result["errors"].append(f"merge: {e}")
        
        return result
    
    def get_status(self) -> Dict:
        """获取蒸馏状态摘要"""
        distill_files = list(self.output_dir.glob("distill_*.jsonl")) if self.output_dir.exists() else []
        
        total_distilled = 0
        domains = Counter()
        for df in distill_files:
            try:
                with open(df, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            record = json.loads(line)
                            domain = record.get("metadata", {}).get("domain", "")
                            domains[domain] += 1
                            total_distilled += 1
            except:
                pass
        
        train_distilled = 0
        if TRAINING_DATA_DIR.exists():
            for tf in TRAINING_DATA_DIR.glob("distilled_*.jsonl"):
                try:
                    with open(tf, 'r', encoding='utf-8') as f:
                        train_distilled += sum(1 for _ in f)
                except:
                    pass
        
        return {
            "distill_dir": str(self.output_dir),
            "export_files": len(distill_files),
            "total_distilled": total_distilled,
            "train_merged": train_distilled,
            "domains": dict(domains.most_common()),
            "last_reports": {k: {
                "candidates": r.total_candidates,
                "passed": r.passed_quality,
                "final": r.after_dedup,
                "avg_quality": round(r.avg_quality, 3),
            } for k, r in self.reports.items()},
        }
    
    def print_report(self):
        """打印蒸馏摘要报告"""
        print(f"\n{'='*60}")
        print(f"🧬 龍魂·知识蒸馏报告")
        print(f"   时间: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"{'='*60}")
        
        for source, report in self.reports.items():
            print(f"\n📡 {source.upper()}:")
            print(f"   候选: {report.total_candidates}")
            print(f"   过质量闸(≥{QUALITY_GATE}): {report.passed_quality}")
            print(f"   去重后: {report.after_dedup}")
            print(f"   平均质量: {report.avg_quality:.3f}")
            print(f"   推理链: {report.reasoning_samples}")
            if report.domains:
                print(f"   领域: {dict(report.domains)}")
            if report.errors:
                print(f"   错误: {len(report.errors)}")
        
        # 汇总
        total = sum(r.after_dedup for r in self.reports.values())
        print(f"\n📊 总产出: {total} 条蒸馏样本")
        print(f"{'='*60}")
    
    def _gen_dna(self, sample: DistillSample) -> str:
        now = datetime.now(timezone.utc)
        tiangan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
        dizhi = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
        gz = f"{tiangan[now.year%10]}{dizhi[now.month%12]}·{tiangan[(now.day+9)%10]}{dizhi[(now.day+1)%12]}"
        sample_hash = hashlib.sha256(sample.sample_id.encode()).hexdigest()[:8]
        return f"#龍芯⚡️{gz}-DISTILL-{sample.source.upper()}-{sample_hash}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    import argparse
    p = argparse.ArgumentParser(description="龍魂·统一知识蒸馏引擎")
    sub = p.add_subparsers(dest="cmd")
    
    sub.add_parser("scan", help="侦察所有蒸馏源状态")
    
    dist_p = sub.add_parser("distill", help="执行蒸馏")
    dist_p.add_argument("--source", choices=["deepseek", "kimi", "all"],
                        default="all", help="蒸馏源")
    dist_p.add_argument("--max", type=int, default=500, help="每源最大样本数")
    dist_p.add_argument("--refine", action="store_true", help="蒸馏后立即炼化入库")
    
    refine_p = sub.add_parser("refine", help="炼化入库")
    refine_p.add_argument("--input", type=str, help="指定输入文件")
    refine_p.add_argument("--quality", type=float, default=QUALITY_GATE, help="质量阈值")
    
    sub.add_parser("status", help="蒸馏状态")
    sub.add_parser("report", help="蒸馏报告")
    
    args = p.parse_args()
    orch = DistillOrchestrator()
    
    if args.cmd == "scan":
        sources = orch.scan()
        print(f"\n{'='*50}")
        print("📡 知识蒸馏源侦察")
        print(f"{'='*50}")
        for name, info in sources.items():
            print(f"\n── {name} ──")
            for k, v in info.items():
                print(f"  {k}: {v}")
    
    elif args.cmd == "distill":
        if args.source == "all":
            orch.distill_all(max_per_source=args.max)
        else:
            orch.distill_source(args.source, max_samples=args.max)
        
        orch.print_report()
        
        if args.refine:
            print("\n🔧 炼化入库...")
            result = orch.refine_and_merge(quality_threshold=QUALITY_GATE)
            print(f"  去重后: {result['after_global_dedup']}")
            print(f"  质量二次筛选: {result['after_requality']}")
            print(f"  导出: {result['exported']} → {result.get('output','')}")
    
    elif args.cmd == "refine":
        result = orch.refine_and_merge(quality_threshold=args.quality)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.cmd == "status":
        status = orch.get_status()
        print(f"\n🧬 蒸馏状态")
        print(f"   蒸馏目录: {status['distill_dir']}")
        print(f"   导出文件: {status['export_files']}")
        print(f"   总蒸馏量: {status['total_distilled']}")
        print(f"   已入训练集: {status['train_merged']}")
        print(f"   领域分布: {status['domains']}")
    
    elif args.cmd == "report":
        orch.print_report()
    
    else:
        p.print_help()


if __name__ == "__main__":
    main()
