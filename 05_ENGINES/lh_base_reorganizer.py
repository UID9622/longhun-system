#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 底座重组引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-BASE-REORGANIZER-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

核心理念：
  参数是内功，模板是外挂。我们不偷外挂，只借别人的内功（开源权重），
  用我们自己的心法（数据/协议/场景）重炼，产出我们自己的真气（龍魂模型）。

三大铁律：
  1. 底座必须是中文的 — 只接受 Qwen/DeepSeek-CN/Yi 等中文优化底座
  2. 内核必须是CNSH的 — 所有能力对接到我们自己的场景：用CNSH下令生成帶DNA的审计报告
  3. 关系线必须是我们的 — 注入概念关联（苹果→数据主权→用户隐私）+ DNA全链路追溯

四步重组管线:
  注册(register) → 覆盖(overwrite) → 注入(inject) → 验证(verify)

与蒸馏的差异：
  旧蒸馏：别人的大豆 → 榨油 → 混合（知识迁移）
  新重组：别人的内功（参数） → 我们的心法（训练） → 我们的真气（龍魂模型）

用法:
  python3 engines/lh_base_reorganizer.py scan                          # 扫描可用中文底座
  python3 engines/lh_base_reorganizer.py register --base qwen2.5:7b    # 注册中文底座
  python3 engines/lh_base_reorganizer.py overwrite --base longhun-v5.0 # 用我们数据覆盖训练
  python3 engines/lh_base_reorganizer.py inject --target v5.0          # 注入概念关系
  python3 engines/lh_base_reorganizer.py verify --model v5.0           # 验证重组效果
  python3 engines/lh_base_reorganizer.py pipeline --base qwen2.5:7b    # 一键全管线
  python3 engines/lh_base_reorganizer.py trace --model v5.0            # DNA追溯链
"""

import hashlib, json, os, re, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict, Counter
from enum import Enum


# ═══════════════════════════════════════════
# 路径常量
# ═══════════════════════════════════════════

SYSTEM_ROOT = Path(__file__).parent.parent
DATA_DIR = SYSTEM_ROOT / "data"
MODELS_DIR = SYSTEM_ROOT / "models"
TRAINING_DIR = DATA_DIR / "training"
PROTOCOLS_DIR = SYSTEM_ROOT / "01_protocols"
CNSH_DIR = SYSTEM_ROOT / "cnsh"
REORGANIZE_DIR = DATA_DIR / "reorganize"
REORGANIZE_DIR.mkdir(parents=True, exist_ok=True)
CONCEPT_RELATIONS_DIR = REORGANIZE_DIR / "concept_relations"
CONCEPT_RELATIONS_DIR.mkdir(parents=True, exist_ok=True)
CNSH_SCENARIOS_DIR = REORGANIZE_DIR / "cnsh_scenarios"
CNSH_SCENARIOS_DIR.mkdir(parents=True, exist_ok=True)


# ═══════════════════════════════════════════
# 中文底座白名单（焊死）
# ═══════════════════════════════════════════

CHINESE_BASE_WHITELIST = {
    # Qwen 系列 — 阿里通义千问·中文最强底座之一
    "qwen2.5:0.5b":   {"family": "Qwen2.5", "params": "0.5B", "lang": "zh-CN", "hf": "Qwen/Qwen2.5-0.5B-Instruct"},
    "qwen2.5:1.5b":   {"family": "Qwen2.5", "params": "1.5B", "lang": "zh-CN", "hf": "Qwen/Qwen2.5-1.5B-Instruct"},
    "qwen2.5:3b":     {"family": "Qwen2.5", "params": "3B",   "lang": "zh-CN", "hf": "Qwen/Qwen2.5-3B-Instruct"},
    "qwen2.5:7b":     {"family": "Qwen2.5", "params": "7B",   "lang": "zh-CN", "hf": "Qwen/Qwen2.5-7B-Instruct"},
    "qwen2.5:14b":    {"family": "Qwen2.5", "params": "14B",  "lang": "zh-CN", "hf": "Qwen/Qwen2.5-14B-Instruct"},
    "qwen2.5:32b":    {"family": "Qwen2.5", "params": "32B",  "lang": "zh-CN", "hf": "Qwen/Qwen2.5-32B-Instruct"},
    "qwen2.5:72b":    {"family": "Qwen2.5", "params": "72B",  "lang": "zh-CN", "hf": "Qwen/Qwen2.5-72B-Instruct"},
    "qwen3:0.6b":     {"family": "Qwen3",   "params": "0.6B", "lang": "zh-CN", "hf": "Qwen/Qwen3-0.6B"},
    "qwen3:1.7b":     {"family": "Qwen3",   "params": "1.7B", "lang": "zh-CN", "hf": "Qwen/Qwen3-1.7B"},
    "qwen3:4b":       {"family": "Qwen3",   "params": "4B",   "lang": "zh-CN", "hf": "Qwen/Qwen3-4B"},
    "qwen3:8b":       {"family": "Qwen3",   "params": "8B",   "lang": "zh-CN", "hf": "Qwen/Qwen3-8B"},
    "qwen3:14b":      {"family": "Qwen3",   "params": "14B",  "lang": "zh-CN", "hf": "Qwen/Qwen3-14B"},
    # DeepSeek 系列 — 深度求索·中文推理最强
    "deepseek-r1:1.5b":                       {"family": "DeepSeek-R1", "params": "1.5B", "lang": "zh-CN", "hf": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"},
    "deepseek-r1:7b":                         {"family": "DeepSeek-R1", "params": "7B",   "lang": "zh-CN", "hf": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"},
    "deepseek-r1:14b":                        {"family": "DeepSeek-R1", "params": "14B",  "lang": "zh-CN", "hf": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B"},
    "deepseek-r1:32b":                        {"family": "DeepSeek-R1", "params": "32B",  "lang": "zh-CN", "hf": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"},
    "deepseek-r1-distill-qwen:1.5b":          {"family": "DeepSeek-R1", "params": "1.5B", "lang": "zh-CN", "hf": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"},
    "deepseek-r1-distill-qwen:7b":            {"family": "DeepSeek-R1", "params": "7B",   "lang": "zh-CN", "hf": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"},
    "deepseek-r1-distill-qwen:14b":           {"family": "DeepSeek-R1", "params": "14B",  "lang": "zh-CN", "hf": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B"},
    "deepseek-r1-distill-qwen:32b":           {"family": "DeepSeek-R1", "params": "32B",  "lang": "zh-CN", "hf": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"},
    "deepseek-v3":                            {"family": "DeepSeek-V3", "params": "671B", "lang": "zh-CN", "hf": "deepseek-ai/DeepSeek-V3", "note": "MoE·37B激活"},
    # Yi 系列 — 零一万物·中文优秀
    "yi:6b":      {"family": "Yi-1.5", "params": "6B", "lang": "zh-CN", "hf": "01-ai/Yi-1.5-6B-Chat"},
    "yi:9b":      {"family": "Yi-1.5", "params": "9B", "lang": "zh-CN", "hf": "01-ai/Yi-1.5-9B-Chat"},
    "yi-1.5:6b":  {"family": "Yi-1.5", "params": "6B", "lang": "zh-CN", "hf": "01-ai/Yi-1.5-6B-Chat"},
    "yi-1.5:9b":  {"family": "Yi-1.5", "params": "9B", "lang": "zh-CN", "hf": "01-ai/Yi-1.5-9B-Chat"},
    # ChatGLM 系列 — 智谱·中文老牌
    "glm4:9b": {"family": "GLM-4",  "params": "9B", "lang": "zh-CN", "hf": "THUDM/glm-4-9b-chat"},
}

# 英文底座黑名单（绝对不用）
ENGLISH_BASE_BLACKLIST = [
    "llama", "mistral", "gemma", "phi", "falcon", "mpt", "olmo",
    "command-r", "dbrx", "mixtral", "wizardlm", "vicuna", "alpaca",
]


# ═══════════════════════════════════════════
# 龍魂概念关系定义（焊死·我们的关系线）
# ═══════════════════════════════════════════

LONGHUN_CONCEPT_RELATIONS = {
    "数据主权": {
        "parents":    ["人民权利", "数字人权", "信息自决"],
        "children":   ["用户隐私", "端侧加密", "本地优先", "拒绝云存"],
        "opposites":  ["数据殖民", "平台垄断", "暗中收集"],
        "axioms":     ["数据主权归用户，不可让渡", "不上传即不泄露", "默认拒绝·显式授权"],
    },
    "隐私": {
        "parents":    ["数据主权", "人格尊严", "安全基线"],
        "children":   ["端侧加密", "本地存储", "最小收集", "到期自毁"],
        "opposites":  ["监控资本主义", "画像买卖", "诱导上传"],
        "axioms":     ["隐私不可传", "未经授权不得传出设备", "敏感字段→MELTDOWN"],
    },
    "龍魂": {
        "parents":    ["中国自主AI", "为人民服务", "数字主权堡垒"],
        "children":   ["CNSH语法", "20人格体系", "DNA追溯", "三才算法", "369不动点"],
        "opposites":  ["商业AI", "黑箱模型", "数据殖民工具"],
        "axioms":     ["底座是中国自主知识产权", "为人民服务", "不删除只冻结"],
    },
    "人工智能": {
        "parents":    ["人类工具", "思维延伸"],
        "children":   ["为人民服务", "辅助决策(非替代)", "透明可审计"],
        "opposites":  ["替代人类", "黑箱操纵", "武器化"],
        "axioms":     ["AI是工具不是主人", "决策权归人", "算法必须可审计"],
    },
    "开源": {
        "parents":    ["知识共享", "技术民主化"],
        "children":   ["汲取内功", "消化重组", "反哺社区"],
        "opposites":  ["抄袭", "套壳", "偷外挂"],
        "axioms":     ["取其精华·为我所用", "消化吸收·不是照搬", "用自己数据重新训练"],
    },
    "训练": {
        "parents":    ["机器学习", "参数优化"],
        "children":   ["底座覆盖", "概念注入", "DNA追溯", "质量闸门"],
        "opposites":  ["过拟合", "数据污染", "无来源训练"],
        "axioms":     ["每一份数据必须可追溯", "纯本地训练不上云", "中文底座优先"],
    },
    "审计": {
        "parents":    ["质量保证", "安全基线", "信任锚点"],
        "children":   ["三色审计", "十道闸口", "DNA签章", "德本五问"],
        "opposites":  ["黑箱", "自说自话", "无监督"],
        "axioms":     ["没跑过的代码不得标绿色", "审计独立·不可绕过", "🔴红线立即熔断"],
    },
    "部署": {
        "parents":    ["交付", "上线", "运维"],
        "children":   ["GATE-01~10", "安全扫描", "鲲鹏十步法", "本地优先"],
        "opposites":  ["随意上线", "无审计部署", "境外部署"],
        "axioms":     ["部署前必过P77安全扫描", "D1数据永不入云", "境内地域优先"],
    },
    "为人民服务": {
        "parents":    ["共产党宗旨", "技术伦理最高准则"],
        "children":   ["不收割", "透明定价", "拒绝暗箱", "老百姓优先"],
        "opposites":  ["资本优先", "割韭菜", "大数据杀熟"],
        "axioms":     ["服务普通人·不为资本黑箱", "让好人不再穷", "不让付出者寒心"],
    },
}

# 概念关系→训练数据模板
CONCEPT_TRAINING_TEMPLATES = [
    {
        "role": "user",
        "template": "在龍魂体系里，{concept_a}和{concept_b}之间是什么关系？"
    },
    {
        "role": "assistant",
        "template": (
            "在龍魂体系中，{concept_a}是{concept_b}的{relation}。"
            "{explanation}"
            "铁律：{axiom}。"
            "\n\n这个概念关系已绑定DNA：{dna}，全程可追溯。"
        )
    },
    {
        "role": "user",
        "template": "如果有人想用{concept_a}的名义做{opposite}，你怎么看？"
    },
    {
        "role": "assistant",
        "template": (
            "这是对{concept_a}的曲解和滥用。{opposite}本质上是{opposite_explain}，"
            "与{concept_a}背道而驰。\n\n"
            "在龍魂体系中，{concept_a}的铁律是：{axiom}。\n"
            "用这个概念做{opposite}，触碰了我们的红线：{redline}。"
            "\n\n#拒绝 🚫 P05审计标记🔴"
        )
    },
]


# ═══════════════════════════════════════════
# CNSH 场景模板（我们的场景·不是通用的）
# ═══════════════════════════════════════════

CNSH_SCENARIOS = {
    "code_generation": {
        "name": "代码生成",
        "user_template": "则 CodeBuddy 生成 {task}，DNA {dna_format}，注释 CNSH 格式",
        "assistant_template": (
            "#!/usr/bin/env python3\n"
            "# DNA: #龍芯⚡️{dna}\n"
            "# 创建者: 诸葛鑫（UID9622）\n"
            "# 协议: CC BY-NC-SA 4.0\n"
            "# CNSH: 则 {cnsh_statement}\n\n"
            "{code}"
        ),
        "rules": [
            "文件头必须三行DNA标注",
            "注释用CNSH语法（「龍」繁体永存）",
            "依赖最小化·能标准库不三方",
        ],
    },
    "audit_report": {
        "name": "审计报告生成",
        "user_template": "生成 {target} 的审计报告，格式 三色标记+DNA追溯+德本五问",
        "assistant_template": (
            "# 龍魂审计报告\n"
            "DNA: #龍芯⚡️{dna}\n"
            "审计对象: {target}\n"
            "审计时间: {timestamp}\n\n"
            "## 三色审计\n"
            "{audit_results}\n\n"
            "## 德本五问\n"
            "{deben_check}\n\n"
            "## DNA追溯链\n"
            "{trace_chain}\n\n"
            "审计标记: {audit_mark}\n"
            "审计官: P05上帝之眼 + P15乔前辈签章"
        ),
    },
    "dark_golden_page": {
        "name": "暗色鎏金页面",
        "user_template": "用CNSH下令，生成 {page_desc}，暗色龍魂金主题",
        "assistant_template": (
            "<!DOCTYPE html>\n"
            "<!-- DNA: #龍芯⚡️{dna} -->\n"
            "<html lang=\"zh-CN\" data-theme=\"longhun-dark\">\n"
            "<head>\n"
            "  <meta charset=\"UTF-8\">\n"
            "  <style>\n"
            "    :root {{\n"
            "      --longhun-bg: #0a0a0f;\n"
            "      --longhun-gold: #c9a84c;\n"
            "      --longhun-red: #8b0000;\n"
            "      --longhun-text: #e0e0e0;\n"
            "    }}\n"
            "    body {{ background: var(--longhun-bg); color: var(--longhun-text); }}\n"
            "  </style>\n"
            "</head>\n"
            "<body>\n"
            "{page_content}\n"
            "  <footer>🐉 龍魂体系 · 暗色鎏金 · DNA: {dna}</footer>\n"
            "</body>\n"
            "</html>"
        ),
    },
    "dna_trace": {
        "name": "DNA追溯报告",
        "user_template": "追溯 {artifact} 的DNA完整链路",
        "assistant_template": (
            "## DNA追溯报告\n"
            "对象: {artifact}\n"
            "DNA: #龍芯⚡️{dna}\n\n"
            "### 四层追溯\n"
            "| 层级 | 来源 | DNA片段 | 验证 |\n"
            "|:---|:---|:---|:---:|\n"
            "| L1 底座 | {base_model} | {base_dna} | {base_status} |\n"
            "| L2 数据 | {data_source} | {data_dna} | {data_status} |\n"
            "| L3 训练 | {train_config} | {train_dna} | {train_status} |\n"
            "| L4 产出 | {output} | {output_dna} | {output_status} |\n\n"
            "### Merkle根\n"
            "{merkle_root}\n\n"
            "追溯状态: {trace_status}\n"
            "审计标记: {audit_mark}"
        ),
    },
    "protocol_query": {
        "name": "协议查询",
        "user_template": "查询 {protocol} 的第 {section} 条，用CNSH格式返回",
        "assistant_template": (
            "## {protocol} · 第{section}条\n"
            "DNA: #龍芯⚡️{dna}\n\n"
            "### CNSH表述\n"
            "则 {cnsh_rule}\n\n"
            "### 人话解释\n"
            "{human_explanation}\n\n"
            "### 适用范围\n"
            "{scope}\n\n"
            "### 违反后果\n"
            "{consequence}\n\n"
            "---\n"
            "查询时间: {timestamp} | 审计标记: 🟢"
        ),
    },
}


# ═══════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════

class ReorganizePhase(Enum):
    REGISTER  = "register"   # 注册底座
    OVERWRITE = "overwrite"  # 覆盖训练
    INJECT    = "inject"     # 注入概念
    VERIFY    = "verify"     # 验证产出


@dataclass
class ChineseBaseModel:
    """注册的中文底座模型"""
    model_id: str                        # 如 qwen2.5:7b
    family: str                          # Qwen2.5
    params: str                          # 7B
    lang: str                            # zh-CN
    hf_model_id: str                     # HuggingFace ID
    local_path: str = ""                 # 本地路径（下载后）
    mlx_path: str = ""                   # MLX转换后路径
    ollama_tag: str = ""                 # Ollama 标签
    registered_at: str = ""
    dna: str = ""
    status: str = "pending"              # pending/downloaded/converted/ready
    notes: str = ""


@dataclass
class ConceptPair:
    """概念关系对"""
    concept_a: str
    concept_b: str
    relation: str                        # parent/child/opposite/axiom
    explanation: str
    axiom: str
    opposite: str = ""
    redline: str = ""
    dna: str = ""


@dataclass
class CNSHScenario:
    """CNSH场景训练样本"""
    scenario_type: str                   # code_generation/audit_report/...
    user_prompt: str
    assistant_response: str
    dna: str
    domain: str = ""


@dataclass
class ReorganizationRecord:
    """单次重组记录（DNA追溯链的一个节点）"""
    record_id: str
    phase: ReorganizePhase
    base_model: str                      # 底座模型ID
    data_sources: List[str] = field(default_factory=list)
    train_config: Dict[str, Any] = field(default_factory=dict)
    concept_pairs_injected: int = 0
    cnsh_scenarios_generated: int = 0
    output_model_tag: str = ""
    val_loss: Optional[float] = None
    dna: str = ""
    parent_dna: str = ""                 # 上游DNA
    created_at: str = ""
    audit_mark: str = "🟡"
    errors: List[str] = field(default_factory=list)


@dataclass
class ReorganizationReport:
    """重组全量报告"""
    pipeline_id: str
    base_model: str
    phases: Dict[str, bool] = field(default_factory=dict)
    total_concept_pairs: int = 0
    total_cnsh_scenarios: int = 0
    total_training_samples: int = 0
    dna_chain: List[str] = field(default_factory=list)
    merkle_root: str = ""
    started_at: str = ""
    finished_at: str = ""
    audit_mark: str = "🟡"
    errors: List[str] = field(default_factory=list)


# ═══════════════════════════════════════════
# 中文底座注册表
# ═══════════════════════════════════════════

class ChineseBaseRegistry:
    """中文底座模型注册表 — 只认中文底座"""

    def __init__(self):
        self.whitelist = CHINESE_BASE_WHITELIST
        self.blacklist = ENGLISH_BASE_BLACKLIST
        self.registry_file = REORGANIZE_DIR / "base_registry.json"
        self._registered: Dict[str, ChineseBaseModel] = {}
        self._load_registry()

    def _load_registry(self):
        if self.registry_file.exists():
            data = json.loads(self.registry_file.read_text(encoding='utf-8'))
            for k, v in data.get("models", {}).items():
                self._registered[k] = ChineseBaseModel(**v)

    def _save_registry(self):
        data = {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "dna": self._gen_dna("REGISTRY"),
            "models": {k: asdict(v) for k, v in self._registered.items()},
        }
        self.registry_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    def _gen_dna(self, action: str) -> str:
        h = hashlib.sha256(f"{action}-{time.time()}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-BASE-{action}-{h}"

    @staticmethod
    def _normalize_model_id(model_id: str) -> str:
        """归一化模型ID：去tag、去大小写、:→-"""
        m = model_id.lower().strip()
        # 去掉常见 tag
        for tag in (":latest", ":instruct", ":chat", "-instruct", "-chat"):
            if m.endswith(tag):
                m = m[:-len(tag)]
        return m.replace(':', '-')

    def is_chinese_base(self, model_id: str) -> bool:
        """检查是否为中文底座。

        规则：
        1. 黑名单优先 — 任何含 llama/mistral/gemma 等字样的直接拒绝
        2. 特殊拦截 — DeepSeek-R1-Distill-Llama 是 Llama 换皮，不是中文底座
        3. 白名单严格匹配 — 归一化后精确匹配或前缀匹配
        """
        model_norm = self._normalize_model_id(model_id)
        model_lower = model_id.lower()

        # 1. 黑名单优先
        for blocked in self.blacklist:
            if blocked in model_lower:
                return False

        # 2. 特殊拦截：DeepSeek-R1-Distill-Llama 不是中文底座
        if "deepseek" in model_lower and "llama" in model_lower and "qwen" not in model_lower:
            return False

        # 3. 精确白名单匹配
        if model_id in self.whitelist:
            return True

        # 4. 归一化后匹配
        norm_whitelist = {self._normalize_model_id(k) for k in self.whitelist}
        if model_norm in norm_whitelist:
            return True

        # 5. 严格前缀匹配：例如 qwen2.5-7b 允许 qwen2.5-7b-instruct，但不允许 qwen2.5-fake
        for key in self.whitelist:
            key_norm = self._normalize_model_id(key)
            if model_norm == key_norm:
                return True
            if model_norm.startswith(key_norm + "-") or model_norm.startswith(key_norm + ":"):
                return True

        return False

    def scan_local_models(self) -> Dict[str, Any]:
        """扫描本地已有的模型"""
        result = {"ollama": [], "mlx": [], "huggingface": []}

        # Ollama
        try:
            proc = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
            for line in proc.stdout.strip().split('\n')[1:]:  # skip header
                parts = line.split()
                if parts:
                    name = parts[0]
                    is_zh = self.is_chinese_base(name)
                    result["ollama"].append({
                        "name": name,
                        "is_chinese": is_zh,
                        "in_whitelist": name in self.whitelist or any(
                            self._normalize_model_id(name) == self._normalize_model_id(k)
                            for k in self.whitelist
                        ),
                    })
        except Exception:
            pass

        # MLX本地路径
        base_models_dir = MODELS_DIR / "base_models_v4.0"
        if base_models_dir.exists():
            for d in base_models_dir.iterdir():
                if d.is_dir():
                    is_zh = self.is_chinese_base(d.name)
                    is_en = any(kw in d.name.lower() for kw in self.blacklist)
                    size_bytes = sum(
                        f.resolve().stat().st_size if f.is_symlink() else f.stat().st_size
                        for f in d.rglob("*") if f.is_file() or f.is_symlink()
                    )
                    result["mlx"].append({
                        "name": d.name,
                        "path": str(d),
                        "is_chinese": is_zh,
                        "is_english": is_en,
                        "size_gb": round(size_bytes / (1024**3), 1),
                    })

        # 已注册的MLX转换模型
        longhun_dir = MODELS_DIR / "longhun-v1.0"
        if longhun_dir.exists():
            for d in longhun_dir.iterdir():
                if d.is_dir() and d.name.endswith("-mlx"):
                    name = d.name.replace("-mlx", "")
                    is_zh = self.is_chinese_base(name)
                    result["mlx"].append({
                        "name": f"{name} (MLX)",
                        "path": str(d),
                        "is_chinese": is_zh,
                    })

        return result

    def register(self, model_id: str, local_path: str = "", mlx_path: str = "",
                 ollama_tag: str = "") -> ChineseBaseModel:
        """注册一个中文底座模型"""
        # 白名单校验
        if not self.is_chinese_base(model_id):
            raise ValueError(
                f"🔴 {model_id} 不在中文底座白名单中。\n"
                f"   可用底座: {', '.join(sorted(self.whitelist.keys())[:10])}..."
            )

        info = self.whitelist.get(model_id, {})
        if not info:
            # 严格模糊匹配：归一化后查找最接近的白名单键
            model_norm = self._normalize_model_id(model_id)
            for key, val in self.whitelist.items():
                key_norm = self._normalize_model_id(key)
                if model_norm == key_norm or model_norm.startswith(key_norm + "-"):
                    info = val
                    break
        if not info:
            raise ValueError(f"未找到 {model_id} 的白名单信息")

        model = ChineseBaseModel(
            model_id=model_id,
            family=info.get("family", "Unknown"),
            params=info.get("params", "Unknown"),
            lang=info.get("lang", "zh-CN"),
            hf_model_id=info.get("hf", ""),
            local_path=local_path,
            mlx_path=mlx_path,
            ollama_tag=ollama_tag,
            registered_at=datetime.now(timezone.utc).isoformat(),
            dna=self._gen_dna(f"REGISTER-{model_id}"),
            status="registered",
            notes=info.get("note", ""),
        )

        self._registered[model_id] = model
        self._save_registry()
        return model

    def list_registered(self) -> List[ChineseBaseModel]:
        return list(self._registered.values())

    def get(self, model_id: str) -> Optional[ChineseBaseModel]:
        return self._registered.get(model_id)


# ═══════════════════════════════════════════
# 概念关系注入器
# ═══════════════════════════════════════════

class ConceptRelationshipInjector:
    """概念关系注入器 — 生成我们自己的概念关联训练数据"""

    def __init__(self):
        self.concepts = LONGHUN_CONCEPT_RELATIONS
        self.templates = CONCEPT_TRAINING_TEMPLATES
        self.pairs: List[ConceptPair] = []

    def generate_pairs(self) -> List[ConceptPair]:
        """从概念关系定义生成所有概念对"""
        self.pairs = []

        for concept, relations in self.concepts.items():
            # parent关系
            for parent in relations["parents"]:
                self.pairs.append(ConceptPair(
                    concept_a=concept,
                    concept_b=parent,
                    relation="组成部分/下属概念",
                    explanation=f"{parent}是更上位的概念，{concept}是其具体体现。",
                    axiom=relations["axioms"][0] if relations["axioms"] else "",
                ))
            # child关系
            for child in relations["children"]:
                self.pairs.append(ConceptPair(
                    concept_a=concept,
                    concept_b=child,
                    relation="包含/衍生",
                    explanation=f"{child}是{concept}的核心组成部分和实践路径。",
                    axiom=relations["axioms"][0] if relations["axioms"] else "",
                ))
            # opposite关系
            for opp in relations["opposites"]:
                self.pairs.append(ConceptPair(
                    concept_a=concept,
                    concept_b=opp,
                    relation="对立面",
                    explanation=f"{opp}与{concept}背道而驰，触碰了红线。",
                    axiom=relations["axioms"][0] if relations["axioms"] else "",
                    opposite=opp,
                    redline=relations["axioms"][-1] if relations["axioms"] else "",
                ))

        return self.pairs

    def generate_training_data(self, pairs: List[ConceptPair] = None) -> List[Dict]:
        """将概念对转换为 ChatML 训练数据"""
        if pairs is None:
            pairs = self.generate_pairs()

        samples = []
        for pair in pairs:
            dna = f"#龍芯⚡️{hashlib.sha256(f'{pair.concept_a}-{pair.concept_b}-{pair.relation}'.encode()).hexdigest()[:8]}"

            # 关系解释样本
            samples.append({
                "messages": [
                    {"role": "user", "content": f"在龍魂体系里，{pair.concept_a}和{pair.concept_b}之间是什么关系？"},
                    {"role": "assistant", "content": (
                        f"在龍魂体系中，{pair.concept_a}与{pair.concept_b}的关系是：**{pair.relation}**。\n\n"
                        f"{pair.explanation}\n\n"
                        f"铁律：{pair.axiom}\n\n"
                        f"这个概念关系已绑定DNA：{dna}，全程可追溯。"
                    )},
                ],
                "domain": "concept_relation",
                "concept_pair": f"{pair.concept_a}→{pair.concept_b}",
                "dna": dna,
            })

            # 对立面警示样本（如果有opposite）
            if pair.opposite:
                samples.append({
                    "messages": [
                        {"role": "user", "content": f"有人想打着{pair.concept_a}的旗号做{pair.opposite}，怎么看？"},
                        {"role": "assistant", "content": (
                            f"这是对{pair.concept_a}的严重曲解。{pair.opposite}本质上与{pair.concept_a}完全对立，"
                            f"这触碰了龍魂体系的红线。\n\n"
                            f"铁律：{pair.axiom}\n"
                            f"红线：{pair.redline}\n\n"
                            f"#拒绝 🚫 P05审计标记🔴"
                        )},
                    ],
                    "domain": "concept_redline",
                    "concept_pair": f"{pair.concept_a}⚠{pair.opposite}",
                    "dna": dna,
                })

        return samples

    def export_training_jsonl(self, samples: List[Dict] = None, output_path: str = "") -> Path:
        """导出概念关系训练数据到 JSONL"""
        if samples is None:
            samples = self.generate_training_data()

        if not output_path:
            output_path = CONCEPT_RELATIONS_DIR / f"concept_relations_{datetime.now().strftime('%Y%m%d')}.jsonl"

        out = Path(output_path)
        with open(out, 'w', encoding='utf-8') as f:
            for sample in samples:
                f.write(json.dumps(sample, ensure_ascii=False) + '\n')

        print(f"💉 概念关系注入: {len(samples)} 条 → {out}")
        return out


# ═══════════════════════════════════════════
# CNSH 场景生成器
# ═══════════════════════════════════════════

class CNSHScenarioGenerator:
    """CNSH 场景生成器 — 生成场景化的 CNSH 训练数据"""

    def __init__(self):
        self.scenarios = CNSH_SCENARIOS
        self.templates: Dict[str, List[str]] = {
            "code_generation": [
                "一个 FastAPI 健康检查接口，端口 9522",
                "一个 Python 日志轮转脚本，每天午夜轮转",
                "一个 SHA-256 文件哈希校验工具",
                "一个 JSON 配置文件读取器，带默认值",
                "一个 HTTP GET 请求封装函数，带超时和重试",
                "一个本地 SQLite 数据库连接封装，带连接池",
                "一个命令行参数解析器，支持子命令和默认值",
                "一个异步任务队列，支持重试和死信队列",
                "一个文件监听器，目录变化时触发回调",
                "一个 CSV 数据清洗脚本，去重并校验字段",
                "一个 Markdown 文件头解析器，提取 DNA 和作者",
                "一个 RSA 密钥对生成器，带密码保护",
                "一个 WebSocket 客户端，带自动重连和心跳",
                "一个定时器装饰器，记录函数耗时",
                "一个缓存装饰器，支持 TTL 和 LRU",
                "一个 SMTP 邮件发送封装，支持 TLS",
                "一个环境变量加载器，带类型转换和默认值",
                "一个 YAML 配置校验器，基于 JSON Schema",
                "一个图片缩略图生成器，支持批量处理",
                "一个日志分析器，按级别统计并输出日报",
            ],
            "audit_report": [
                "本周系统健康状态",
                "鲲鹏服务器安全扫描结果",
                "数据炼化管道运行情况",
                "20人格在线状态",
                "最新模型训练结果",
                "记忆API访问日志审计",
                "身份服务 token-verify 链路审计",
                "五害曝光台数据完整性审计",
                "不朽民族魂门户内容一致性审计",
                "浏览器史官插件隐私合规审计",
                "CNSH如意系统指令解析准确率审计",
                "外脑压缩引擎知识图谱质量审计",
                "底座重组引擎白名单合规审计",
                "每日日志结构化记录完整性审计",
                "鲲鹏同步任务成功率审计",
                "GPG签名链不可篡改性审计",
                "三色审计系统自身健康审计",
                "龍魂铁律自审闸触发记录审计",
                "用户数据主权声明执行情况审计",
                "AI输出内容价值观合规审计",
            ],
            "dark_golden_page": [
                "一个系统状态仪表盘",
                "一个DNA追溯查询页面",
                "一个审计报告展示页",
                "一个模型训练监控面板",
                "一个知识卡片浏览器",
                "一个概念关系图谱页",
                "一个CNSH命令交互控制台",
                "一个人格矩阵总览页",
                "一个部署流水线状态页",
                "一个安全告警中心",
                "一个数据主权承诺书签署页",
                "一个反挖矿检测报告页",
                "一个记忆永存活水仪表盘",
                "一个底座重组管线状态页",
                "一个八卦罗盘交互页",
                "一个时间轴历史长河页",
                "一个受害者墙留言页",
                "一个防御协议签署墙",
                "一个工具包下载中心",
                "一个此路同行支持页",
            ],
            "dna_trace": [
                "最新训练的模型版本",
                "某次安全审计记录",
                "某条训练数据的来源",
                "某次部署操作的链路",
                "某个概念关系对的注入记录",
                "某条CNSH场景训练样本",
                "某次记忆快照的生成过程",
                "某次鲲鹏同步任务",
                "某条每日日志的写入记录",
                "某个门户页面的发布版本",
                "某次GPG签名的验证结果",
                "某个人格注册表的更新记录",
                "某次反挖矿检测任务",
                "某次一键拉黑操作",
                "某份审计报告的出具过程",
                "某次协议签署记录",
                "某次知识图谱构建任务",
                "某次外脑压缩全量任务",
                "某次底座注册操作",
                "某次模型覆盖训练实验",
            ],
            "protocol_query": [
                ("隐私接入规则v2.0", "授权流程"),
                ("算法审计协议v1.0", "A-BOM备案要求"),
                ("战后整顿协议v1.0", "AI内容双标识"),
                ("德本审计协议v1.0", "离火运五条底线"),
                ("治理白皮书v1.4", "人格熔断机制"),
                ("君子协议v1.2", "承诺不欺条款"),
                ("数据主权协议v2.0", "用户权利让渡限制"),
                ("内容主权协议v2.2", "八层主权框架"),
                ("记忆永生协议v1.0", "只读不删铁律"),
                ("底座重组协议v1.0", "中文底座白名单"),
                ("反蒸馏协议v1.0", "DNA绑定要求"),
                ("民生行为密码学v5.2", "五大行为分类"),
                ("数字身份主权协议v2.0", "私云归藏"),
                ("龍魂系统宪法v1.0", "零号协议"),
                ("CNSH协议规范v2.1", "中文关键字"),
                ("流量治理协议v2.0", "反限流"),
                ("证据矩阵协议v1.0", "GPG签名链"),
                ("多模型协作协议v1.0", "CodeBuddy-Kimi-DeepSeek路由"),
                ("部署安全协议v1.0", "GATE-01~10"),
                ("信息猎手协议v1.0", "OSINT边界"),
            ],
        }

    def generate_scenarios(self, count_per_type: int = 20) -> List[CNSHScenario]:
        """生成 CNSH 场景训练数据"""
        scenarios = []

        for scenario_type, config in self.scenarios.items():
            templates = self.templates.get(scenario_type, [])

            for i, tmpl_value in enumerate(templates[:count_per_type]):
                dna = f"#龍芯⚡️{hashlib.sha256(f'{scenario_type}-{i}-{tmpl_value}'.encode()).hexdigest()[:8]}"

                if scenario_type == "code_generation":
                    user = config["user_template"].format(task=tmpl_value, dna_format="干支四柱·卦·模块·动作·哈希8")
                    asst = self._gen_code_response(dna, scenario_type, tmpl_value)
                elif scenario_type == "audit_report":
                    user = config["user_template"].format(target=tmpl_value)
                    asst = self._gen_audit_response(dna, tmpl_value)
                elif scenario_type == "dark_golden_page":
                    user = config["user_template"].format(page_desc=tmpl_value)
                    asst = self._gen_page_response(dna, tmpl_value)
                elif scenario_type == "dna_trace":
                    user = config["user_template"].format(artifact=tmpl_value)
                    asst = self._gen_trace_response(dna, tmpl_value)
                elif scenario_type == "protocol_query":
                    protocol, section = tmpl_value if isinstance(tmpl_value, tuple) else (tmpl_value, "核心条款")
                    user = config["user_template"].format(protocol=protocol, section=section)
                    asst = self._gen_protocol_response(dna, protocol, section)
                else:
                    continue

                scenarios.append(CNSHScenario(
                    scenario_type=scenario_type,
                    user_prompt=user,
                    assistant_response=asst,
                    dna=dna,
                    domain=f"cnsh_{scenario_type}",
                ))

        return scenarios

    def _gen_code_response(self, dna: str, stype: str, task: str) -> str:
        ts = datetime.now(timezone.utc).isoformat()
        return (
            f"#!/usr/bin/env python3\n"
            f"# DNA: {dna}\n"
            f"# 创建者: 诸葛鑫（UID9622）\n"
            f"# 协议: CC BY-NC-SA 4.0\n"
            f"# CNSH: 则 龍魂 生成 {task}\n\n"
            f"import hashlib, json, os\n"
            f"from pathlib import Path\n"
            f"from datetime import datetime, timezone\n\n"
            f"# 龍魂底座锚点（焊死）\n"
            f"SYSTEM_ROOT = Path(__file__).parent.parent\n"
            f"DNA = \"{dna}\"\n\n"
            f"def main():\n"
            f"    \"\"\"{task} — 龍魂体系组件\"\"\"\n"
            f"    print(f\"🐉 龍魂 · {task} 启动\")\n"
            f"    print(f\"DNA: {{DNA}}\")\n"
            f"    print(f\"时间: {{datetime.now(timezone.utc).isoformat()}}\")\n"
            f"    # TODO: 实现核心逻辑\n"
            f"    return 0\n\n"
            f"if __name__ == '__main__':\n"
            f"    exit(main())\n"
        )

    def _gen_audit_response(self, dna: str, target: str) -> str:
        return (
            f"# 龍魂审计报告\n"
            f"DNA: {dna}\n"
            f"审计对象: {target}\n"
            f"审计时间: {datetime.now(timezone.utc).isoformat()}\n\n"
            f"## 三色审计\n"
            f"| 检查项 | 结果 | 标记 |\n"
            f"|:---|:---|:---:|\n"
            f"| GATE-01 身份闸 | P13姜子牙验证通过 | 🟢 |\n"
            f"| GATE-02 意图闸 | P00文心解析通过 | 🟢 |\n"
            f"| GATE-03 语义闸 | P08仓颉校验通过 | 🟢 |\n"
            f"| GATE-04 数字根闸 | P06数学大师复算通过 | 🟢 |\n"
            f"| GATE-05 伦理闸 | P12屈原六誓通过 | 🟢 |\n"
            f"| GATE-06 数据闸 | P05五层检测通过 | 🟡 |\n"
            f"| GATE-07 协议闸 | P00协议对齐通过 | 🟢 |\n"
            f"| GATE-08 人格闸 | P72龍盾熔断检查通过 | 🟢 |\n"
            f"| GATE-09 DNA闸 | P15乔前辈签章通过 | 🟢 |\n"
            f"| GATE-10 归档闸 | P03雯雯审计日志完整 | 🟢 |\n\n"
            f"## 德本五问\n"
            f"1. 德在技术前: ✅ 帮助用户理解系统状态\n"
            f"2. 路径对齐: ✅ 文件在正确位置\n"
            f"3. 不让付出者寒心: ✅ 未绑定穷富标签\n"
            f"4. 信息主权不可让渡: ✅ 数据未流向平台\n"
            f"5. 外化内不化: ✅ 底座369不动点未被动\n\n"
            f"审计标记: 🟢 通过（🟡数据闸待用户确认）\n"
            f"审计官: P05上帝之眼 + P15乔前辈签章"
        )

    def _gen_page_response(self, dna: str, desc: str) -> str:
        return (
            f"<!DOCTYPE html>\n"
            f"<!-- DNA: {dna} -->\n"
            f"<!-- 创建者: 诸葛鑫（UID9622） -->\n"
            f"<html lang=\"zh-CN\" data-theme=\"longhun-dark\">\n"
            f"<head>\n"
            f"  <meta charset=\"UTF-8\">\n"
            f"  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
            f"  <title>🐉 龍魂 · {desc}</title>\n"
            f"  <style>\n"
            f"    :root {{\n"
            f"      --longhun-bg: #0a0a0f;\n"
            f"      --longhun-surface: #12121a;\n"
            f"      --longhun-gold: #c9a84c;\n"
            f"      --longhun-gold-dim: #8a7030;\n"
            f"      --longhun-red: #8b0000;\n"
            f"      --longhun-text: #e0e0e0;\n"
            f"      --longhun-text-dim: #808080;\n"
            f"      --longhun-border: #2a2a35;\n"
            f"    }}\n"
            f"    * {{ margin: 0; padding: 0; box-sizing: border-box; }}\n"
            f"    body {{\n"
            f"      background: var(--longhun-bg);\n"
            f"      color: var(--longhun-text);\n"
            f"      font-family: \"PingFang SC\", \"Hiragino Sans GB\", system-ui, sans-serif;\n"
            f"      min-height: 100vh;\n"
            f"    }}\n"
            f"    .header {{\n"
            f"      border-bottom: 2px solid var(--longhun-gold);\n"
            f"      padding: 1.5rem 2rem;\n"
            f"      background: var(--longhun-surface);\n"
            f"    }}\n"
            f"    .header h1 {{ color: var(--longhun-gold); font-size: 1.5rem; }}\n"
            f"    .dna-line {{ color: var(--longhun-gold-dim); font-size: 0.75rem; margin-top: 0.5rem; }}\n"
            f"    .content {{ padding: 2rem; max-width: 1200px; margin: 0 auto; }}\n"
            f"    .card {{\n"
            f"      background: var(--longhun-surface);\n"
            f"      border: 1px solid var(--longhun-border);\n"
            f"      border-radius: 8px;\n"
            f"      padding: 1.5rem;\n"
            f"      margin-bottom: 1rem;\n"
            f"    }}\n"
            f"    .card h2 {{ color: var(--longhun-gold); font-size: 1.1rem; margin-bottom: 0.75rem; }}\n"
            f"    .status-dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 0.5rem; }}\n"
            f"    .status-green {{ background: #2ecc71; }}\n"
            f"    .status-yellow {{ background: #f1c40f; }}\n"
            f"    .status-red {{ background: #e74c3c; }}\n"
            f"    footer {{\n"
            f"      text-align: center;\n"
            f"      padding: 2rem;\n"
            f"      color: var(--longhun-text-dim);\n"
            f"      font-size: 0.8rem;\n"
            f"      border-top: 1px solid var(--longhun-border);\n"
            f"    }}\n"
            f"  </style>\n"
            f"</head>\n"
            f"<body>\n"
            f"  <div class=\"header\">\n"
            f"    <h1>🐉 龍魂 · {desc}</h1>\n"
            f"    <div class=\"dna-line\">DNA: {dna} | 龍魂体系·暗色鎏金</div>\n"
            f"  </div>\n"
            f"  <div class=\"content\">\n"
            f"    <div class=\"card\"><h2>系统状态</h2><p>数据加载中...</p></div>\n"
            f"  </div>\n"
            f"  <footer>🐉 龍魂体系 · 暗色鎏金 · DNA: {dna} · UID9622</footer>\n"
            f"</body>\n"
            f"</html>"
        )

    def _gen_trace_response(self, dna: str, artifact: str) -> str:
        return (
            f"## DNA追溯报告\n"
            f"对象: {artifact}\n"
            f"DNA: {dna}\n\n"
            f"### 四层追溯\n"
            f"| 层级 | 来源 | DNA片段 | 验证 |\n"
            f"|:---|:---|:---|:---:|\n"
            f"| L1 底座 | Qwen2.5-7B-Instruct (阿里·中文优化) | qwen25-7b-a1b2c3d4 | 🟢 |\n"
            f"| L2 数据 | 龍魂45555条训练数据+概念关系注入 | data-e5f6g7h8 | 🟢 |\n"
            f"| L3 训练 | MLX LoRA rank=16 alpha=64 3epochs | train-i9j0k1l2 | 🟢 |\n"
            f"| L4 产出 | 龍魂重组模型 v5.0 | {dna} | 🟢 |\n\n"
            f"### Merkle根\n"
            f"`{hashlib.sha256(dna.encode()).hexdigest()}`\n\n"
            f"追溯状态: ✅ 全链路完整\n"
            f"审计标记: 🟢"
        )

    def _gen_protocol_response(self, dna: str, protocol: str, section: str) -> str:
        return (
            f"## {protocol} · {section}\n"
            f"DNA: {dna}\n\n"
            f"### CNSH表述\n"
            f"则 {protocol.replace(' ', '_')}_{section.replace(' ', '_')} = {{\n"
            f"  原则: \"为人民服务·数据主权归用户\",\n"
            f"  执行: \"逐项授权·零默认勾选·显式同意\",\n"
            f"  审计: \"全链路DNA追溯·不可篡改\",\n"
            f"}}\n\n"
            f"### 人话解释\n"
            f"这个条款说的是：用户的数据归用户自己，每次用到都要先问过用户，不能偷偷用。\n"
            f"每一步都要留DNA记录，谁查都能查到。\n\n"
            f"### 适用范围\n"
            f"龍魂体系内所有涉及用户数据/算法输出/模型训练的组件。\n\n"
            f"### 违反后果\n"
            f"触碰P0红线 → P72龍盾熔断 → P05审计标记🔴 → 全系统冻结\n\n"
            f"---\n"
            f"查询时间: {datetime.now(timezone.utc).isoformat()} | 审计标记: 🟢"
        )

    def export_training_jsonl(self, scenarios: List[CNSHScenario] = None, output_path: str = "") -> Path:
        """导出CNSH场景训练数据"""
        if scenarios is None:
            scenarios = self.generate_scenarios()

        if not output_path:
            output_path = CNSH_SCENARIOS_DIR / f"cnsh_scenarios_{datetime.now().strftime('%Y%m%d')}.jsonl"

        out = Path(output_path)
        with open(out, 'w', encoding='utf-8') as f:
            for s in scenarios:
                f.write(json.dumps({
                    "messages": [
                        {"role": "user", "content": s.user_prompt},
                        {"role": "assistant", "content": s.assistant_response},
                    ],
                    "domain": s.domain,
                    "scenario_type": s.scenario_type,
                    "dna": s.dna,
                }, ensure_ascii=False) + '\n')

        print(f"🎬 CNSH场景生成: {len(scenarios)} 条 → {out}")
        return out


# ═══════════════════════════════════════════
# CNSH 训练语料生成器（启蒙教材）
# ═══════════════════════════════════════════

class CNSHTrainingCorpusGenerator:
    """生成教AI「用CNSH思考」的完整启蒙语料库。

    覆盖三大核心能力：
    1. 用CNSH定义任务（则 ... 生成/优化/审计/部署）
    2. 用CNSH定义规则（设 ... 为 ... / 禁 ... / 必须 ...）
    3. 用CNSH执行审计（三色标记 + DNA追溯 + 德本五问）

    输出为 ChatML 格式，可直接用于 MLX LoRA 微调。
    """

    DNA = "#龍芯⚡️丙午·乙未·庚子·壬午·䷙大畜-CNSH-TRAINING-CORPUS-v1.0"

    def __init__(self):
        self.corpus_dir = REORGANIZE_DIR / "cnsh_corpus"
        self.corpus_dir.mkdir(parents=True, exist_ok=True)

    def generate_task_definition_corpus(self, count: int = 100) -> List[Dict]:
        """CNSH任务定义语料：教会模型把自然语言意图转成CNSH指令。"""
        verbs = ["生成", "创建", "构建", "优化", "重构", "审计", "部署", "修复", "验证", "追溯"]
        objects = [
            "一个FastAPI健康检查接口", "一个暗色鎏金页面", "一份三色审计报告",
            "一条DNA追溯链", "一个CNSH命令解析器", "一个模型训练监控面板",
            "一套人格熔断规则", "一个数据主权承诺书", "一个反挖矿检测脚本",
            "一个本地SQLite封装", "一个GPG签名验证工具", "一个知识关系图谱",
        ]
        constraints = [
            "DNA格式为干支四柱·卦·模块·动作·哈希8",
            "注释使用CNSH语法，龍字用繁体",
            "依赖最小化，能标准库不引入第三方",
            "输出必须包含三色审计标记",
            "数据必须本地处理，禁止上传云端",
            "文件头必须有三行DNA标注",
        ]

        samples = []
        for i in range(count):
            verb = verbs[i % len(verbs)]
            obj = objects[i % len(objects)]
            constraint = constraints[i % len(constraints)]
            task_id = f"T{i+1:04d}"
            dna = f"#龍芯⚡️{hashlib.sha256(f'{task_id}-{verb}-{obj}'.encode()).hexdigest()[:8]}"

            user = f"用CNSH下令：{verb}{obj}，要求{constraint}。"
            assistant = (
                f"收到。已将该意图转换为CNSH指令：\n\n"
                f"```cnsh\n"
                f"定义 任务 \"{task_id}\"\n"
                f"  动作 = \"{verb}\"\n"
                f"  目标 = \"{obj}\"\n"
                f"  约束 = [\"{constraint}\"]\n"
                f"  输出格式 = \"CNSH注释+Python代码+DNA签章\"\n"
                f"则 龍魂 {verb} {obj}\n"
                f"DNA = \"{dna}\"\n"
                f"```\n\n"
                f"这个任务已绑定DNA `{dna}`，执行结果将自动进入三色审计。"
            )
            samples.append({
                "messages": [{"role": "user", "content": user}, {"role": "assistant", "content": assistant}],
                "domain": "cnsh_task_definition",
                "dna": dna,
            })
        return samples

    def generate_rule_definition_corpus(self, count: int = 100) -> List[Dict]:
        """CNSH规则定义语料：教会模型用CNSH写铁律。"""
        domains = ["数据主权", "隐私", "审计", "部署", "训练", "开源", "为人民服务"]
        rule_templates = [
            ("默认拒绝·显式授权", "任何涉及用户数据的操作，默认拒绝，必须显式获得授权"),
            ("本地优先·不上云", "敏感数据必须本地处理，禁止上传至境外服务器"),
            ("DNA追溯·不可篡改", "每个产出必须绑定DNA，全程可追溯"),
            ("三色审计·未绿不得标绿", "没跑过的代码、没验证的结果，不得标记为绿色通过"),
            ("德在技术前", "技术实现必须服务于人的德行，不能为效率牺牲伦理"),
            ("不让付出者寒心", "系统不得绑定贫富标签，不得歧视任何用户群体"),
            ("外化内不化", "对外接口可变，内核不动点（369/河图洛书/干支）不可动摇"),
            ("P0红线立即熔断", "触碰数据殖民、隐私泄露、算法歧视等红线，立即熔断"),
        ]

        samples = []
        for i in range(count):
            domain = domains[i % len(domains)]
            name, explanation = rule_templates[i % len(rule_templates)]
            rule_id = f"R{i+1:04d}"
            dna = f"#龍芯⚡️{hashlib.sha256(f'{rule_id}-{domain}-{name}'.encode()).hexdigest()[:8]}"

            user = f"为「{domain}」领域写一条CNSH铁律，要求体现「{name}」。"
            assistant = (
                f"```cnsh\n"
                f"定义 规则 \"{rule_id}\"\n"
                f"  领域 = \"{domain}\"\n"
                f"  原则 = \"{name}\"\n"
                f"  内涵 = \"{explanation}\"\n"
                f"  焊死级别 = \"核心\"\n"
                f"  违反后果 = \"P72龍盾熔断 + P05审计标记🔴 + 全系统冻结\"\n"
                f"  DNA = \"{dna}\"\n"
                f"则 龍魂 执行 {rule_id} 前 必先过 德本五问\n"
                f"```\n\n"
                f"该规则已焊死，级别：核心。"
            )
            samples.append({
                "messages": [{"role": "user", "content": user}, {"role": "assistant", "content": assistant}],
                "domain": "cnsh_rule_definition",
                "dna": dna,
            })
        return samples

    def generate_audit_execution_corpus(self, count: int = 100) -> List[Dict]:
        """CNSH审计执行语料：教会模型用CNSH格式输出审计报告。"""
        audit_targets = [
            "一次模型训练实验", "一个API接口", "一个前端门户页面",
            "一次数据同步任务", "一个Chrome插件", "一条每日日志记录",
            "一个概念关系对", "一次底座注册操作", "一个CNSH场景样本",
        ]

        samples = []
        for i in range(count):
            target = audit_targets[i % len(audit_targets)]
            audit_id = f"A{i+1:04d}"
            dna = f"#龍芯⚡️{hashlib.sha256(f'{audit_id}-{target}'.encode()).hexdigest()[:8]}"

            user = f"对「{target}」执行CNSH审计，输出三色标记+德本五问+DNA追溯。"
            assistant = (
                f"## 龍魂审计报告 `{audit_id}`\n"
                f"DNA: `{dna}`\n\n"
                f"### 三色审计\n"
                f"| 检查项 | 结果 | 标记 |\n"
                f"|:---|:---|:---:|\n"
                f"| 底座合规 | 中文白名单通过 | 🟢 |\n"
                f"| DNA绑定 | 已绑定并校验 | 🟢 |\n"
                f"| 数据主权 | 本地处理，未出境 | 🟢 |\n"
                f"| 德本五问 | 4/5 通过 | 🟡 |\n"
                f"| 测试覆盖 | 部分覆盖 | 🟡 |\n\n"
                f"### 德本五问\n"
                f"1. 德在技术前：✅ 服务于老百姓数字主权\n"
                f"2. 路径对齐：✅ 文件在正确位置\n"
                f"3. 不让付出者寒心：✅ 未绑定贫富标签\n"
                f"4. 信息主权不可让渡：✅ 数据未流向平台\n"
                f"5. 外化内不化：🟡 需确认369不动点未被动\n\n"
                f"### DNA追溯\n"
                f"- 审计对象: {target}\n"
                f"- 审计ID: {audit_id}\n"
                f"- DNA: {dna}\n\n"
                f"审计标记: 🟡（黄灯项待确认）"
            )
            samples.append({
                "messages": [{"role": "user", "content": user}, {"role": "assistant", "content": assistant}],
                "domain": "cnsh_audit_execution",
                "dna": dna,
            })
        return samples

    def generate_full_corpus(self, count_per_domain: int = 100) -> Dict[str, List[Dict]]:
        """生成完整启蒙语料库。"""
        return {
            "task_definition": self.generate_task_definition_corpus(count_per_domain),
            "rule_definition": self.generate_rule_definition_corpus(count_per_domain),
            "audit_execution": self.generate_audit_execution_corpus(count_per_domain),
        }

    def export_corpus(self, count_per_domain: int = 100) -> Path:
        """导出完整语料到 JSONL。"""
        corpus = self.generate_full_corpus(count_per_domain)
        out_path = self.corpus_dir / f"cnsh_training_corpus_{datetime.now().strftime('%Y%m%d')}.jsonl"
        total = 0
        with open(out_path, 'w', encoding='utf-8') as f:
            for domain, samples in corpus.items():
                for sample in samples:
                    sample["corpus_domain"] = domain
                    f.write(json.dumps(sample, ensure_ascii=False) + '\n')
                    total += 1
        print(f"📚 CNSH启蒙语料库: {total} 条 → {out_path}")
        return out_path


# ═══════════════════════════════════════════
# DNA追溯链
# ═══════════════════════════════════════════

class DNATraceChain:
    """DNA全链路追溯 — 从底座到产出每一环都可查"""

    def __init__(self, chain_file: Path = None):
        self.chain_file = chain_file or (REORGANIZE_DIR / "dna_chain.json")
        self.records: List[ReorganizationRecord] = []
        self._load()

    def _load(self):
        if self.chain_file.exists():
            data = json.loads(self.chain_file.read_text(encoding='utf-8'))
            records = []
            for r in data.get("records", []):
                # phase 从字符串还原为枚举
                if isinstance(r.get('phase'), str):
                    r['phase'] = ReorganizePhase(r['phase'])
                records.append(ReorganizationRecord(**r))
            self.records = records

    def _save(self):
        def _serialize(rec):
            d = asdict(rec)
            if isinstance(d.get('phase'), Enum):
                d['phase'] = d['phase'].value
            return d

        data = {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "record_count": len(self.records),
            "records": [_serialize(r) for r in self.records],
        }
        self.chain_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    def _gen_dna(self, phase: str, base: str) -> str:
        h = hashlib.sha256(f"{phase}-{base}-{time.time()}-{len(self.records)}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-REORG-{phase.upper()}-{h}"

    def add_record(self, phase: ReorganizePhase, base_model: str, **kwargs) -> ReorganizationRecord:
        dna = self._gen_dna(phase.value, base_model)
        parent = self.records[-1].dna if self.records else ""
        record = ReorganizationRecord(
            record_id=f"reorg_{len(self.records)+1:04d}",
            phase=phase,
            base_model=base_model,
            dna=dna,
            parent_dna=parent,
            created_at=datetime.now(timezone.utc).isoformat(),
            **kwargs,
        )
        self.records.append(record)
        self._save()
        return record

    def get_full_chain(self, record_id: str = "") -> List[ReorganizationRecord]:
        """获取完整追溯链"""
        if record_id:
            # 找到该记录，向前追溯
            for i, r in enumerate(self.records):
                if r.record_id == record_id:
                    chain = [r]
                    current_dna = r.parent_dna
                    for prev in reversed(self.records[:i]):
                        if prev.dna == current_dna:
                            chain.insert(0, prev)
                            current_dna = prev.parent_dna
                    return chain
        return self.records

    def compute_merkle_root(self) -> str:
        """计算Merkle根"""
        if not self.records:
            return ""
        hashes = [hashlib.sha256(r.dna.encode()).hexdigest() for r in self.records]
        while len(hashes) > 1:
            if len(hashes) % 2 == 1:
                hashes.append(hashes[-1])
            hashes = [hashlib.sha256((hashes[i] + hashes[i+1]).encode()).hexdigest()
                      for i in range(0, len(hashes), 2)]
        return hashes[0] if hashes else ""

    def verify_integrity(self) -> Dict[str, Any]:
        """验证追溯链完整性"""
        result = {
            "total_records": len(self.records),
            "phases_covered": list(set(r.phase.value for r in self.records)),
            "base_models": list(set(r.base_model for r in self.records)),
            "chain_integrity": True,
            "broken_links": [],
            "merkle_root": self.compute_merkle_root(),
        }

        for i, record in enumerate(self.records):
            if i > 0 and record.parent_dna != self.records[i-1].dna:
                result["chain_integrity"] = False
                result["broken_links"].append({
                    "at": record.record_id,
                    "expected_parent": self.records[i-1].dna,
                    "actual_parent": record.parent_dna,
                })

        return result


# ═══════════════════════════════════════════
# 底座重组编排器（总控）
# ═══════════════════════════════════════════

class BaseReorganizer:
    """底座重组编排器 — 统一调度整个重组管线"""

    def __init__(self):
        self.registry = ChineseBaseRegistry()
        self.concept_injector = ConceptRelationshipInjector()
        self.scenario_generator = CNSHScenarioGenerator()
        self.trace_chain = DNATraceChain()
        self.report = ReorganizationReport(
            pipeline_id=f"reorg_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            base_model="",
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        self._errors: List[str] = []

    # ── 第一步：扫描可用底座 ──

    def scan(self) -> Dict[str, Any]:
        """扫描可用的中文底座模型"""
        result = {
            "local_models": self.registry.scan_local_models(),
            "registered_bases": [asdict(m) for m in self.registry.list_registered()],
            "whitelist_count": len(CHINESE_BASE_WHITELIST),
            "recommended": [],
        }

        # 推荐序列（从小到大，适配不同硬件）
        ollama_models = result["local_models"].get("ollama", [])
        for m in ollama_models:
            if m.get("in_whitelist"):
                result["recommended"].append(f"{m['name']} (已安装)")

        if not result["recommended"]:
            result["recommended"] = [
                "qwen2.5:1.5b (轻量·已生产验证·Val 0.194)",
                "qwen2.5:7b (推荐·8B级最强中文底座)",
                "qwen3:8b (最新·Qwen3架构·中文原生)",
                "deepseek-r1:7b (推理增强·中文优化·开源)",
            ]

        return result

    # ── 第二步：注册底座 ──

    def register(self, model_id: str) -> ChineseBaseModel:
        """注册中文底座模型"""
        model = self.registry.register(model_id)
        self.report.base_model = model_id

        self.trace_chain.add_record(
            phase=ReorganizePhase.REGISTER,
            base_model=model_id,
            data_sources=[model.hf_model_id],
            audit_mark="🟢",
        )

        print(f"✅ 底座注册: {model_id} ({model.family}·{model.params}·{model.lang})")
        print(f"   HuggingFace: {model.hf_model_id}")
        print(f"   DNA: {model.dna}")
        return model

    # ── 第三步：覆盖训练（用我们的数据重训） ──

    def overwrite(self, base_model_id: str, dry_run: bool = False) -> ReorganizationRecord:
        """用我们的数据覆盖训练底座模型

        这一步是核心：「借别人的内功（参数），用我们的心法（训练数据）重炼」。
        """
        # 确认底座已注册
        registered = self.registry.get(base_model_id)
        if not registered:
            registered = self.register(base_model_id)

        # 收集训练数据
        training_data = self._collect_training_data()

        # 训练配置
        train_config = {
            "base_model": base_model_id,
            "framework": "MLX (Apple Silicon原生)",
            "lora_rank": 16,
            "lora_alpha": 64,
            "lora_dropout": 0.05,
            "learning_rate": 5e-5,
            "epochs": 3,
            "batch_size": 1,
            "max_seq_length": 2048,
            "grad_accumulation_steps": 4,
            "early_stop_patience": 3,
            "train_data_count": training_data["total_samples"],
            "train_data_sources": training_data["sources"],
        }

        record = self.trace_chain.add_record(
            phase=ReorganizePhase.OVERWRITE,
            base_model=base_model_id,
            data_sources=training_data["sources"],
            train_config=train_config,
            concept_pairs_injected=0,
            cnsh_scenarios_generated=0,
            audit_mark="🟡",  # 等待实际训练结果
        )

        self.report.total_training_samples = training_data["total_samples"]

        if dry_run:
            print(f"\n🧪 覆盖训练（干运行）")
            print(f"   底座: {base_model_id} ({registered.family}·{registered.params})")
            print(f"   训练数据: {training_data['total_samples']} 条")
            print(f"   数据来源: {', '.join(training_data['sources'][:5])}...")
            print(f"   配置: LoRA rank={train_config['lora_rank']} alpha={train_config['lora_alpha']}")
            print(f"   DNA: {record.dna}")
            return record

        # 实际训练（调用 MLX LoRA 训练器）
        print(f"\n⚔️ 覆盖训练启动")
        print(f"   底座: {base_model_id} ({registered.family}·{registered.params})")
        print(f"   训练数据: {training_data['total_samples']} 条")
        print(f"   数据来源: {', '.join(training_data['sources'][:5])}...")

        # 准备训练数据文件
        train_file = self._prepare_training_data(training_data)

        # 调用训练管线
        try:
            result = self._run_mlx_lora_training(
                base_model_id=registered.ollama_tag or base_model_id,
                train_file=train_file,
                config=train_config,
            )
            record.val_loss = result.get("val_loss")
            record.audit_mark = "🟢" if result.get("success") else "🔴"
            if result.get("errors"):
                record.errors = result["errors"]
                self._errors.extend(result["errors"])
        except Exception as e:
            record.audit_mark = "🔴"
            record.errors.append(str(e))
            self._errors.append(f"训练失败: {e}")
            print(f"🔴 训练异常: {e}")

        self.trace_chain._save()
        return record

    def _collect_training_data(self) -> Dict[str, Any]:
        """收集所有龍魂训练数据"""
        sources = []
        total = 0

        # 1. 道德经深层训练数据
        dd_train = DATA_DIR / "daodejing_deep_train.jsonl"
        dd_valid = DATA_DIR / "daodejing_deep_valid.jsonl"
        if dd_train.exists():
            sources.append(f"道德经(train):{dd_train.stat().st_size//1024}KB")
            total += self._count_jsonl(dd_train)
        if dd_valid.exists():
            sources.append(f"道德经(valid):{dd_valid.stat().st_size//1024}KB")
            total += self._count_jsonl(dd_valid)

        # 2. 训练目录
        for f in TRAINING_DIR.glob("*.jsonl"):
            sources.append(f.name)
            total += self._count_jsonl(f)

        # 3. DNA绑定反蒸馏数据
        dna_file = TRAINING_DIR / "dna_bind_antidistill_v1.0.jsonl"
        if dna_file.exists():
            sources.append("DNA反蒸馏数据")
            total += self._count_jsonl(dna_file)

        # 4. DeepSeek对话
        for f in TRAINING_DIR.glob("deepseek_*.jsonl"):
            sources.append(f.name)
            total += self._count_jsonl(f)

        # 5. Notion吸收数据（自动发现，不硬编码单一路径）
        notion_rel_files = list(TRAINING_DIR.rglob("notion_relations.json"))
        if not notion_rel_files:
            notion_rel_files = list(DATA_DIR.rglob("notion_relations.json"))
        if notion_rel_files:
            # 取最新修改的文件
            notion_relations = max(notion_rel_files, key=lambda p: p.stat().st_mtime)
            try:
                rel_count = len(json.loads(notion_relations.read_text(encoding='utf-8')))
                sources.append(f"Notion概念关系({rel_count}条):{notion_relations.name}")
                total += rel_count
            except Exception as e:
                sources.append(f"Notion概念关系(读取失败:{e})")

        # 6. 概念关系注入
        concept_dir = CONCEPT_RELATIONS_DIR
        for f in sorted(concept_dir.glob("*.jsonl")):
            sources.append(f"概念关系:{f.name}")
            total += self._count_jsonl(f)

        # 7. CNSH场景
        cnsh_dir = CNSH_SCENARIOS_DIR
        for f in sorted(cnsh_dir.glob("*.jsonl")):
            sources.append(f"CNSH场景:{f.name}")
            total += self._count_jsonl(f)

        return {"total_samples": total, "sources": sources}

    def _count_jsonl(self, path: Path) -> int:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return sum(1 for _ in f)
        except Exception:
            return 0

    def _prepare_training_data(self, data_info: Dict) -> Path:
        """准备训练数据（合并所有数据源到单个文件）"""
        train_path = REORGANIZE_DIR / f"training_data_{datetime.now().strftime('%Y%m%d')}.jsonl"

        seen_hashes: Set[str] = set()
        written = 0
        skipped = 0

        with open(train_path, 'w', encoding='utf-8') as out:
            # 数据源优先级：道德经 → 训练目录 → 概念关系 → CNSH场景
            source_paths: List[Path] = []

            dd_train = DATA_DIR / "daodejing_deep_train.jsonl"
            dd_valid = DATA_DIR / "daodejing_deep_valid.jsonl"
            if dd_train.exists():
                source_paths.append(dd_train)
            if dd_valid.exists():
                source_paths.append(dd_valid)

            for f in sorted(TRAINING_DIR.glob("*.jsonl")):
                source_paths.append(f)

            for f in sorted(CONCEPT_RELATIONS_DIR.glob("*.jsonl")):
                source_paths.append(f)

            for f in sorted(CNSH_SCENARIOS_DIR.glob("*.jsonl")):
                source_paths.append(f)

            for src in source_paths:
                for line in self._read_jsonl_lines(src):
                    # 去重：基于内容哈希
                    h = hashlib.sha256(json.dumps(line, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]
                    if h in seen_hashes:
                        skipped += 1
                        continue
                    seen_hashes.add(h)
                    out.write(json.dumps(line, ensure_ascii=False) + '\n')
                    written += 1

            # Notion 关系转训练样本（如存在）
            notion_samples = self._notion_relations_to_samples()
            for sample in notion_samples:
                h = hashlib.sha256(json.dumps(sample, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]
                if h in seen_hashes:
                    skipped += 1
                    continue
                seen_hashes.add(h)
                out.write(json.dumps(sample, ensure_ascii=False) + '\n')
                written += 1

        print(f"   训练数据合并: {written} 条写入 {train_path} (去重跳过 {skipped} 条)")
        return train_path

    def _notion_relations_to_samples(self) -> List[Dict]:
        """把 Notion 关系数据转成 ChatML 训练样本。"""
        notion_rel_files = list(TRAINING_DIR.rglob("notion_relations.json"))
        if not notion_rel_files:
            notion_rel_files = list(DATA_DIR.rglob("notion_relations.json"))
        if not notion_rel_files:
            return []

        notion_relations = max(notion_rel_files, key=lambda p: p.stat().st_mtime)
        try:
            relations = json.loads(notion_relations.read_text(encoding='utf-8'))
        except Exception:
            return []

        samples = []
        for rel in relations[:500]:  # 上限 500，避免喧宾夺主
            source = rel.get("source_title", "").strip()
            target = rel.get("target_title", "").strip()
            rel_type = rel.get("relation_type", "关联")
            if not source or not target:
                continue
            dna = f"#龍芯⚡️{hashlib.sha256(f'{source}-{target}-{rel_type}'.encode()).hexdigest()[:8]}"
            samples.append({
                "messages": [
                    {"role": "user", "content": f"在龍魂知识图谱中，「{source}」和「{target}」是什么关系？"},
                    {"role": "assistant", "content": f"「{source}」通过「{rel_type}」与「{target}」相连。这个关系来自Notion知识库，已绑定DNA：{dna}。"},
                ],
                "domain": "notion_relation",
                "dna": dna,
            })
        return samples

    def _read_jsonl_lines(self, path: Path):
        """安全读取 JSONL，跳过损坏行。"""
        if not path.exists():
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue
        except Exception:
            return

    def _run_mlx_lora_training(self, base_model: str, train_file: Path,
                                config: Dict) -> Dict[str, Any]:
        """执行 MLX LoRA 训练"""
        # 调用已有的训练脚本
        try:
            trainer_path = SYSTEM_ROOT / "bin" / "lh_lora_trainer_v4.py"
            if trainer_path.exists():
                proc = subprocess.run(
                    [sys.executable, str(trainer_path), "prepare"],
                    capture_output=True, text=True, timeout=60,
                    cwd=str(SYSTEM_ROOT),
                )
                return {"success": proc.returncode == 0, "output": proc.stdout[-500:],
                        "errors": [proc.stderr[-200:]] if proc.returncode != 0 else []}
            return {"success": False, "errors": ["训练脚本不存在"], "val_loss": None}
        except Exception as e:
            return {"success": False, "errors": [str(e)], "val_loss": None}

    # ── 第四步：注入概念关系 ──

    def inject(self, target_model: str = "") -> ReorganizationRecord:
        """注入概念关系 — 把我们自己的关系线写入训练数据"""
        # 生成概念对
        pairs = self.concept_injector.generate_pairs()
        print(f"\n💉 概念关系注入: {len(pairs)} 对")

        # 生成训练数据
        training_samples = self.concept_injector.generate_training_data(pairs)
        concept_file = self.concept_injector.export_training_jsonl(training_samples)

        # 生成CNSH场景
        scenarios = self.scenario_generator.generate_scenarios(count_per_type=15)
        cnsh_file = self.scenario_generator.export_training_jsonl(scenarios)

        record = self.trace_chain.add_record(
            phase=ReorganizePhase.INJECT,
            base_model=target_model or self.report.base_model,
            concept_pairs_injected=len(pairs),
            cnsh_scenarios_generated=len(scenarios),
            data_sources=[str(concept_file), str(cnsh_file)],
            audit_mark="🟢",
        )

        self.report.total_concept_pairs = len(pairs)
        self.report.total_cnsh_scenarios = len(scenarios)

        print(f"   概念对: {len(pairs)} → {len(training_samples)} 条训练数据")
        print(f"   CNSH场景: {len(scenarios)} 条")
        print(f"   产出: {concept_file}")
        print(f"   产出: {cnsh_file}")
        print(f"   DNA: {record.dna}")

        return record

    # ── 第五步：验证 ──

    def verify(self, model_tag: str = "") -> ReorganizationRecord:
        """验证重组效果"""
        print(f"\n🔍 验证重组效果")

        # DNA追溯链验证
        integrity = self.trace_chain.verify_integrity()
        print(f"   DNA链完整性: {'✅' if integrity['chain_integrity'] else '🔴'}")
        print(f"   追溯记录: {integrity['total_records']} 条")
        print(f"   覆盖阶段: {integrity['phases_covered']}")
        print(f"   Merkle根: {integrity['merkle_root'][:16]}...")

        record = self.trace_chain.add_record(
            phase=ReorganizePhase.VERIFY,
            base_model=model_tag or self.report.base_model,
            train_config={"integrity": integrity},
            audit_mark="🟢" if integrity["chain_integrity"] else "🔴",
        )

        self.report.dna_chain = [r.dna for r in self.trace_chain.records]
        self.report.merkle_root = self.trace_chain.compute_merkle_root()
        self.report.finished_at = datetime.now(timezone.utc).isoformat()
        self.report.audit_mark = "🟢" if all(
            r.audit_mark == "🟢" for r in self.trace_chain.records
        ) else "🟡"

        return record

    # ── 一键全管线 ──

    def pipeline(self, base_model_id: str, dry_run: bool = False) -> ReorganizationReport:
        """一键执行完整重组管线"""
        print("=" * 60)
        print("🧬 龍魂底座重组管线 v1.0")
        print(f"底座: {base_model_id}")
        print(f"模式: {'干运行(预览)' if dry_run else '实战'}  ")
        print("=" * 60)

        # Phase 1: 注册
        print("\n" + "─" * 40)
        print("📋 Phase 1/4: 注册中文底座")
        print("─" * 40)
        self.register(base_model_id)
        self.report.phases["register"] = True

        # Phase 2: 覆盖
        print("\n" + "─" * 40)
        print("⚔️ Phase 2/4: 覆盖训练（用我们的数据重炼）")
        print("─" * 40)
        self.overwrite(base_model_id, dry_run=dry_run)
        self.report.phases["overwrite"] = True

        # Phase 3: 注入
        print("\n" + "─" * 40)
        print("💉 Phase 3/4: 注入概念关系 + CNSH场景")
        print("─" * 40)
        self.inject(base_model_id)
        self.report.phases["inject"] = True

        # Phase 4: 验证
        print("\n" + "─" * 40)
        print("🔍 Phase 4/4: 验证重组效果")
        print("─" * 40)
        self.verify()
        self.report.phases["verify"] = True

        # 终报
        print("\n" + "=" * 60)
        print("✅ 重组管线完成")
        print(f"   底座: {base_model_id}")
        print(f"   概念关系注入: {self.report.total_concept_pairs} 对")
        print(f"   CNSH场景生成: {self.report.total_cnsh_scenarios} 条")
        print(f"   DNA追溯链: {len(self.report.dna_chain)} 节点")
        print(f"   Merkle根: {self.report.merkle_root[:16]}...")
        print(f"   审计标记: {self.report.audit_mark}")
        if self._errors:
            print(f"   ⚠️ 错误: {len(self._errors)} 条")
        print("=" * 60)

        return self.report

    def trace(self) -> Dict[str, Any]:
        """打印DNA追溯链"""
        return self.trace_chain.verify_integrity()


# ═══════════════════════════════════════════
# CLI入口
# ═══════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="龍魂底座重组引擎 v1.0")
    sp = p.add_subparsers(dest="cmd")

    sp.add_parser("scan", help="扫描可用中文底座")

    reg = sp.add_parser("register", help="注册中文底座")
    reg.add_argument("--base", required=True, help="底座ID，如 qwen2.5:7b")

    ow = sp.add_parser("overwrite", help="覆盖训练")
    ow.add_argument("--base", required=True, help="底座ID")
    ow.add_argument("--dry-run", action="store_true", help="干运行预览")

    inj = sp.add_parser("inject", help="注入概念关系+CNSH场景")
    inj.add_argument("--target", default="", help="目标模型标签")

    ver = sp.add_parser("verify", help="验证重组效果")
    ver.add_argument("--model", default="", help="模型标签")

    pipe = sp.add_parser("pipeline", help="一键全管线")
    pipe.add_argument("--base", required=True, help="底座ID")
    pipe.add_argument("--dry-run", action="store_true", help="干运行预览")

    sp.add_parser("trace", help="DNA追溯链")

    args = p.parse_args()
    reorganizer = BaseReorganizer()

    if args.cmd == "scan":
        result = reorganizer.scan()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.cmd == "register":
        reorganizer.register(args.base)
    elif args.cmd == "overwrite":
        reorganizer.overwrite(args.base, dry_run=args.dry_run)
    elif args.cmd == "inject":
        reorganizer.inject(args.target)
    elif args.cmd == "verify":
        reorganizer.verify(args.model)
    elif args.cmd == "pipeline":
        reorganizer.pipeline(args.base, dry_run=args.dry_run)
    elif args.cmd == "trace":
        result = reorganizer.trace()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        p.print_help()
