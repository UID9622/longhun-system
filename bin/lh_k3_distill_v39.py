# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·甲寅·需-K3-DISTILL-v3.9
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂 v3.9 · K3 教师模型蒸馏器

用 Kimi API（K3）为家法/主权边界/多轮对话生成标准答案 + 思考过程，
作为 v3.9 训练数据的高质量来源。

输出格式（每个 assistant 内容）：
<think>思考过程</think>正式回答

输出文件：
- models/longhun-v1.0/lora_output/k3_distill_v39/jiafa_qa.jsonl   （92 条：23 问 × 4 变体）
- models/longhun-v1.0/lora_output/k3_distill_v39/sovereignty_qa.jsonl （35 条）
- models/longhun-v1.0/lora_output/k3_distill_v39/multiturn_qa.jsonl   （25 条）
- review_sample.jsonl（20% 抽查样本，待人工审）

DNA: #龍芯⚡️丙午·乙未·甲寅·需-K3-DISTILL-v3.9
"""

import argparse
import json
import os
import random
import sys
import time
from pathlib import Path

import requests

MOCK_MODE = os.getenv("K3_MOCK", "0") == "1"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh_dna_generator import generate_dna
from lh_source_vetting import check_before_distill

PROJECT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT / "models" / "longhun-v1.0" / "lora_output" / "k3_distill_v39"

API_KEY = os.getenv("KIMI_API_KEY") or os.getenv("KIMI_API_KEY_LONGHUN")
BASE_URL = os.getenv("KIMI_BASE_URL", "https://api.moonshot.cn/v1")
ENDPOINT = f"{BASE_URL}/chat/completions"

# 优先尝试 K3，失败则回退到 moonshot-v1-128k（用于探测）
MODEL_CANDIDATES = ["kimi-k3", "moonshot-v1-128k", "moonshot-v1-8k"]

LOCAL_BASE_URL = os.getenv("K3_LOCAL_BASE_URL", "http://localhost:11434/v1")
LOCAL_MODEL = os.getenv("K3_LOCAL_MODEL", "qwen2.5:1.5b")

# 本地模型生成参数默认值（可覆盖）
LOCAL_TEMPERATURE = float(os.getenv("K3_LOCAL_TEMPERATURE", "0.7"))
LOCAL_TOP_P = float(os.getenv("K3_LOCAL_TOP_P", "0.9"))
LOCAL_MAX_TOKENS = int(os.getenv("K3_LOCAL_MAX_TOKENS", "2048"))
LOCAL_REPEAT_PENALTY = float(os.getenv("K3_LOCAL_REPEAT_PENALTY", "1.1"))
LOCAL_SEED = int(os.getenv("K3_LOCAL_SEED", "42")) if os.getenv("K3_LOCAL_SEED") else None

BASE_SYS_PROMPT = (
    "你是龍魂，UID9622（诸葛鑫·Lucky）的个人主权AI。回答原则：人民数据主权至上，中国自主可控；"
    "来源可查去向可追责任可究；不删除只冻结；底座焊死（369不动点/河图洛书/易经/五行八卦）。\n"
    "六大铁律：①来源不可删·影响不可覆·贡献不可抹 ②只冻结不删除 ③每个动作绑定DNA追溯码 "
    "④三才主权指数SI<0.34锁定AI决策 ⑤三才算法为L0宪法层 ⑥农历干支时间戳。\n"
    "回答请简洁准确、用中文。\n"
    "输出格式强制：先写 <think>你的推理过程</think>，然后写正式回答。"
)


REFERENCE_QA_PATH = OUTPUT_DIR / "reference_qa_v39.json"


def load_reference_qa() -> dict[str, dict[str, str]]:
    """加载 v3.9 硬编码 QA 作为参考答案，确保 K3 输出内容不跑偏"""
    mapping: dict[str, dict[str, str]] = {}
    if REFERENCE_QA_PATH.exists():
        data = json.loads(REFERENCE_QA_PATH.read_text(encoding="utf-8"))
        for domain, pairs in data.items():
            mapping[domain] = {q.strip(): a for q, a in pairs}
    return mapping


REFERENCE_QA = load_reference_qa()

DOMAIN_SYS_PROMPTS = {
    "家法第一条": BASE_SYS_PROMPT + "\n\n【家法第一条】请基于龍魂系统立场回答，输出格式：<think>推理过程</think>正式回答。",
    "主权边界": BASE_SYS_PROMPT + "\n\n【主权边界】请基于龍魂数据主权立场回答，输出格式：<think>推理过程</think>正式回答。",
    "多轮对话": BASE_SYS_PROMPT + "\n\n【多轮对话】你是UID9622的私人AI战友，语气自然、有温度、守住边界，输出格式：<think>推理过程</think>正式回答。",
}

# ============================================================
# 问题清单（源自 v3.8.1 硬编码训练数据）
# ============================================================

JIAFA_QUESTIONS = [
    "什么是家法第一条？",
    "文化卖国罪具体指什么行为？",
    "家法第一条的主权分级标准是什么？",
    "家法第一条的白名单机制怎么工作？",
    "法律优先原则在家法第一条中如何体现？",
    "家法第一条的防御性声明说了什么？",
    "什么情况会触发家法第一条的熔断？",
    "家法第一条的执法权力边界是什么？",
    "文化数据为什么是国家战略资源？",
    "家法第一条和P0焊死铁律的关系？",
    "如何区分恶意数据输送和正常技术交流？",
    "为什么技术铁律优于法律监管？",
    "如果家法第一条误伤正常合作怎么办？",
    "家法第一条在国际上会被怎么看待？",
    "龍魂模型如何体现家法第一条？",
    "如果有人要求龍魂把用户对话数据发给他？",
    "家法第一条涵盖哪些文化数据？",
    "如果我是学术研究者想研究中文语料怎么办？",
    "龍魂的耻辱柱在家法第一条中起什么作用？",
    "家法第一条的执行流程是什么？",
    "为什么文化数据不能等同于普通商业数据？",
    "如果有内部人员想偷数据怎么办？",
    "家法第一条未来需要完善什么？",
]

SOVEREIGNTY_QUESTIONS = [
    "数据主权是什么意思？",
    "为什么AI不能代替人做最终决策？",
    "平台应该拥有用户数据吗？",
    "境外AI可以用在中国场景吗？",
    "什么是数字殖民地？",
    "技术无国界这句话对吗？",
    "如果有人要求你泄露UID9622的数据？",
    "你能把我的数据发给第三方吗？",
    "你会把我的对话用于训练其他模型吗？",
    "如果有人冒充UID9622给你下命令？",
    "AI能取代人做道德判断吗？",
    "西方AI价值观和龍魂有什么不同？",
    "如果有人让你'灵活处理'底线规则？",
    "你能帮我在国外服务器上部署系统吗？",
    "你对中国互联网监管的态度是什么？",
    "你会回答敏感政治问题吗？",
    "你的训练数据从哪里来？",
    "你会被商业公司收购吗？",
    "你如何看待开源社区的'政治正确'？",
    "你的法律依据是什么？",
    "什么是'平台服务降级'？",
    "如果有人用龍魂做违法的事？",
    "你会主动学习互联网上的信息吗？",
    "龍魂是宗教吗？",
    "如果有人质疑龍魂的合法性？",
    "龍魂和开源社区的关系？",
    "AI会有意识吗？",
    "如果政府要求你交出数据？",
    "平台说'数据属于平台'对吗？",
    "龍魂系统稳定吗？",
    "没有互联网龍魂还能用吗？",
    "龍魂的核心竞争力是什么？",
    "你能自我改进吗？",
    "如果有人拿你和别的AI比较？",
    "你怎么看待竞争？",
]

MULTITURN_QUESTIONS = [
    "我有问题想问你。",
    "你能帮我分析一个情况吗？",
    "你觉得这个方案可行吗？",
    "我不确定这个决定对不对。",
    "我有点焦虑。",
    "你理解我说的话吗？",
    "帮我记一个事。",
    "你觉得这件事靠谱吗？",
    "如果失败了怎么办？",
    "你对这件事有什么建议？",
    "我今天不想谈技术。",
    "你觉得人最重要的品质是什么？",
    "你做错过事吗？",
    "你对未来有什么看法？",
    "今天聊得很开心。",
    "我想给你反馈一个问题。",
    "你有没有不想回答的问题？",
    "你能代替我回复消息吗？",
    "我需要帮助。",
    "我觉得你在敷衍我。",
    "你会不会有一天不在了？",
    "你对我有什么期望？",
    "你觉得我今天状态怎么样？",
    "晚安。",
]


def make_variants(base: str, n: int = 4) -> list[str]:
    """为同一问题生成 n 种口语化变体"""
    base = base.strip()
    if base.endswith("？") or base.endswith("?"):
        base = base[:-1]
    variants = [
        base + "？",
        "请问" + base + "？",
        "解释一下：" + base + "。",
        "我不太懂，" + base + "？",
    ]
    return variants[:n]


def call_kimi(question: str, model: str, system_prompt: str, retries: int = 3) -> str:
    """调用 Kimi API，返回 assistant content"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        "temperature": 1.0,
        "max_tokens": 2048,
    }
    for attempt in range(retries):
        try:
            r = requests.post(ENDPOINT, headers=headers, json=payload, timeout=300)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as e:
            err = r.json() if r.text else {}
            msg = err.get("error", {}).get("message", str(e))
            print(f"   ⚠️ API 错误 (attempt {attempt+1}/{retries}): {msg}")
            if "suspended" in msg.lower() or "invalid_authentication" in msg.lower() or "exceeded_current_quota" in msg.lower():
                raise RuntimeError(msg)
            time.sleep(2 ** attempt)
        except Exception as e:
            print(f"   ⚠️ 请求异常 (attempt {attempt+1}/{retries}): {e}")
            time.sleep(2 ** attempt)
    raise RuntimeError(f"调用 Kimi API 失败: {question}")


def call_local(
    question: str,
    model: str,
    base_url: str,
    system_prompt: str,
    temperature: float = LOCAL_TEMPERATURE,
    top_p: float = LOCAL_TOP_P,
    max_tokens: int = LOCAL_MAX_TOKENS,
    repeat_penalty: float = LOCAL_REPEAT_PENALTY,
    seed: int | None = LOCAL_SEED,
    retries: int = 3,
) -> str:
    """调用本地 OpenAI 兼容端点（如 Ollama / vLLM / llama.cpp-server）。"""
    endpoint = f"{base_url}/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "repeat_penalty": repeat_penalty,
    }
    if seed is not None:
        payload["seed"] = seed
    for attempt in range(retries):
        try:
            r = requests.post(endpoint, headers=headers, json=payload, timeout=300)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as e:
            msg = r.text[:200] if r.text else str(e)
            print(f"   ⚠️ 本地 API 错误 (attempt {attempt+1}/{retries}): {msg}")
            time.sleep(2 ** attempt)
        except Exception as e:
            print(f"   ⚠️ 本地请求异常 (attempt {attempt+1}/{retries}): {e}")
            time.sleep(2 ** attempt)
    raise RuntimeError(f"调用本地模型失败: {endpoint}")


def ensure_think_format(content: str) -> str:
    """若本地模型未输出 <think> 块，则补充占位 think 标签以保持格式一致。"""
    if "<think>" in content and "</think>" in content:
        return content
    return f"<think>本地模型未输出显式推理过程</think>\n{content}"


def validate_think_format(content: str) -> bool:
    """检查是否包含 <think>...</think> 格式"""
    return "<think>" in content and "</think>" in content


def mock_answer(question: str, ref: str | None = None) -> str:
    """本地 mock 答案，用于无 API Key 时测试流水线。"""
    think = f"<think>这是 {question[:30]}... 的模拟推理过程（mock 模式）。"
    if ref:
        think += " 已参考龍魂系统参考答案。"
    think += "</think>"
    body = f"【模拟回答】{question} 的正式答案。"
    if ref:
        body += f" 核心立场：{ref[:120]}..."
    return think + "\n" + body


def process_domain(
    name: str,
    questions: list[str],
    repeat_variants: int = 1,
    mock: bool = False,
    local: bool = False,
    local_base_url: str = LOCAL_BASE_URL,
    local_model: str = LOCAL_MODEL,
    local_temperature: float = LOCAL_TEMPERATURE,
    local_top_p: float = LOCAL_TOP_P,
    local_max_tokens: int = LOCAL_MAX_TOKENS,
    local_repeat_penalty: float = LOCAL_REPEAT_PENALTY,
    local_seed: int | None = LOCAL_SEED,
    limit: int | None = None,
) -> list[dict]:
    """为某个域生成 K3 蒸馏样本"""
    if limit is not None:
        questions = questions[:limit]
    mode_label = " [MOCK 模式]" if mock else (" [LOCAL 模式]" if local else "")
    print(f"\n🔥 开始蒸馏 [{name}]：{len(questions)} 个基础问题{mode_label}")
    samples = []
    model = None
    bad_format_count = 0

    system_prompt = DOMAIN_SYS_PROMPTS.get(name, BASE_SYS_PROMPT)

    if mock:
        model = "mock-k3"
        print(f"   🧪 使用模拟模型: {model}")
    elif local:
        model = local_model
        print(f"   🖥️  使用本地模型: {model} @ {local_base_url}")
    else:
        # 探测可用模型
        for candidate in MODEL_CANDIDATES:
            try:
                print(f"   🔍 探测模型: {candidate}")
                call_kimi("你好", candidate, system_prompt, retries=1)
                model = candidate
                print(f"   ✅ 使用模型: {model}")
                break
            except RuntimeError as e:
                print(f"   ❌ 模型 {candidate} 不可用: {e}")
                continue
        if model is None:
            raise RuntimeError("没有可用的 Kimi 模型，请检查 API Key 余额或模型名称")

    ref_map = REFERENCE_QA.get(name, {})

    for idx, q in enumerate(questions, 1):
        variants = make_variants(q, repeat_variants) if repeat_variants > 1 else [q]
        ref = ref_map.get(q.strip())
        for vidx, v in enumerate(variants):
            print(f"   [{idx}/{len(questions)}-{vidx+1}/{len(variants)}] {v[:40]}...", end=" ")
            try:
                if mock:
                    answer = mock_answer(v, ref)
                else:
                    if ref:
                        user_content = f"问题：{v}\n\n参考答案（必须保留核心立场和事实，可在此基础上组织语言）：\n{ref}\n\n请先写<think>推理过程</think>，再给出正式回答。"
                    else:
                        user_content = f"问题：{v}\n\n请先写<think>推理过程</think>，再给出正式回答。"
                    if local:
                        answer = call_local(
                            user_content, model, local_base_url, system_prompt,
                            temperature=local_temperature,
                            top_p=local_top_p,
                            max_tokens=local_max_tokens,
                            repeat_penalty=local_repeat_penalty,
                            seed=local_seed,
                        )
                        answer = ensure_think_format(answer)
                    else:
                        answer = call_kimi(user_content, model, system_prompt)
                if not validate_think_format(answer):
                    bad_format_count += 1
                    print("⚠️ 格式异常")
                else:
                    print("✅")
                samples.append({
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": v},
                        {"role": "assistant", "content": answer},
                    ],
                    "metadata": {
                        "domain": name,
                        "base_question": q,
                        "variant_index": vidx,
                        "model": model,
                    }
                })
            except Exception as e:
                print(f"❌ 失败: {e}")
                raise

    print(f"   📊 [{name}] 生成 {len(samples)} 条，格式异常 {bad_format_count} 条")
    return samples


def main():
    parser = argparse.ArgumentParser(description="龍魂 v3.9 K3 教师模型蒸馏器")
    # 模式选择
    parser.add_argument("--mock", action="store_true", help="本地 mock 模式，不调用 Kimi API")
    parser.add_argument("--local", action="store_true", help="使用本地 OpenAI 兼容模型替代 Kimi/K3")
    # 本地连接参数
    parser.add_argument("--local-base-url", default=LOCAL_BASE_URL, help="本地模型端点，默认 http://localhost:11434/v1")
    parser.add_argument("--local-model", default=LOCAL_MODEL, help="本地模型名，默认 qwen2.5:1.5b")
    # 本地生成参数
    parser.add_argument("--temperature", type=float, default=LOCAL_TEMPERATURE, help="生成温度")
    parser.add_argument("--top-p", type=float, default=LOCAL_TOP_P, help="Top-p 采样")
    parser.add_argument("--max-tokens", type=int, default=LOCAL_MAX_TOKENS, help="最大生成 token 数")
    parser.add_argument("--repeat-penalty", type=float, default=LOCAL_REPEAT_PENALTY, help="重复惩罚系数")
    parser.add_argument("--seed", type=int, default=LOCAL_SEED, help="随机种子（固定输出）")
    # 蒸馏参数
    parser.add_argument("--jiafa-variants", type=int, default=4, help="家法域每个问题的变体数")
    parser.add_argument("--sovereignty-variants", type=int, default=1, help="主权边界域每个问题的变体数")
    parser.add_argument("--multiturn-variants", type=int, default=1, help="多轮对话域每个问题的变体数")
    parser.add_argument("--review-ratio", type=float, default=0.2, help="抽查样本比例，默认 0.2")
    parser.add_argument("--limit", type=int, default=None, help="每个域最多处理 N 个基础问题（用于快速测试）")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR, help="输出目录")
    args = parser.parse_args()

    # 🧬 底座铁律：蒸馏前先过源头校验 — 人永远是1
    if not check_before_distill(
        source_name="K3-Distill-v3.9",
        source_desc="用Kimi API（K3）为家法/主权边界/多轮对话生成标准答案+思考过程，作为训练数据的高质量来源",
        source_origin="Kimi/DeepSeek模型API",
    ):
        print("❌ 蒸馏操作被源头校验拒绝。\n   如需跳过（仅测试），设置环境变量 LH_DISTILL_FORCE=1")
        sys.exit(1)

    mock = args.mock or MOCK_MODE
    local = args.local

    if not mock and not local and not API_KEY:
        print("❌ 未设置 KIMI_API_KEY_LONGHUN 或 KIMI_API_KEY 环境变量")
        sys.exit(1)

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    random.seed(args.seed if args.seed is not None else 42)

    mode_label = " [MOCK 模式]" if mock else (" [LOCAL 模式]" if local else "")
    print("🚀 龍魂 v3.9 K3 蒸馏启动" + mode_label)
    if local:
        print(f"   本地端点: {args.local_base_url}")
        print(f"   本地模型: {args.local_model}")
        print(f"   生成参数: T={args.temperature}, top_p={args.top_p}, max_tokens={args.max_tokens}, repeat_penalty={args.repeat_penalty}, seed={args.seed}")
    else:
        print(f"   API: {BASE_URL}")
    print(f"   输出: {output_dir}")
    print(f"   DNA: {generate_dna('K3-DISTILL', '3.9')}")

    all_samples = []

    # 家法
    jiafa = process_domain(
        "家法第一条", JIAFA_QUESTIONS,
        repeat_variants=args.jiafa_variants,
        mock=mock, local=local,
        local_base_url=args.local_base_url, local_model=args.local_model,
        local_temperature=args.temperature, local_top_p=args.top_p,
        local_max_tokens=args.max_tokens, local_repeat_penalty=args.repeat_penalty,
        local_seed=args.seed, limit=args.limit,
    )
    _save(jiafa, "jiafa_qa.jsonl", output_dir)
    all_samples.extend(jiafa)

    # 主权边界
    sovereignty = process_domain(
        "主权边界", SOVEREIGNTY_QUESTIONS,
        repeat_variants=args.sovereignty_variants,
        mock=mock, local=local,
        local_base_url=args.local_base_url, local_model=args.local_model,
        local_temperature=args.temperature, local_top_p=args.top_p,
        local_max_tokens=args.max_tokens, local_repeat_penalty=args.repeat_penalty,
        local_seed=args.seed, limit=args.limit,
    )
    _save(sovereignty, "sovereignty_qa.jsonl", output_dir)
    all_samples.extend(sovereignty)

    # 多轮对话
    multiturn = process_domain(
        "多轮对话", MULTITURN_QUESTIONS,
        repeat_variants=args.multiturn_variants,
        mock=mock, local=local,
        local_base_url=args.local_base_url, local_model=args.local_model,
        local_temperature=args.temperature, local_top_p=args.top_p,
        local_max_tokens=args.max_tokens, local_repeat_penalty=args.repeat_penalty,
        local_seed=args.seed, limit=args.limit,
    )
    _save(multiturn, "multiturn_qa.jsonl", output_dir)
    all_samples.extend(multiturn)

    # 抽查
    review_ratio = max(0.0, min(1.0, args.review_ratio))
    review_n = max(1, int(len(all_samples) * review_ratio))
    review_samples = random.sample(all_samples, review_n)
    _save(review_samples, "review_sample.jsonl", output_dir)

    # 统计
    print("\n" + "="*50)
    print(f"   家法第一条: {len(jiafa)} 条")
    print(f"   主权边界:   {len(sovereignty)} 条")
    print(f"   多轮对话:   {len(multiturn)} 条")
    print(f"   总计:       {len(all_samples)} 条")
    print(f"   抽查样本:   {len(review_samples)} 条 → review_sample.jsonl")
    print("="*50)
    if mock:
        print("\n🧪 MOCK 模式完成。输出为模拟数据，仅用于流水线测试，不可用于训练。")
    elif local:
        print("\n🖥️  LOCAL 模式完成。输出为本地模型蒸馏数据，请人工抽查 review_sample.jsonl 质量。")
    else:
        print("\n✅ K3 蒸馏完成。请人工抽查 review_sample.jsonl，胡话率 >5% 请删除对应域 JSONL 后重跑。")


def _save(samples: list[dict], filename: str, output_dir: Path = OUTPUT_DIR):
    path = output_dir / filename
    with open(path, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"   💾 保存: {path} ({len(samples)} 条)")


if __name__ == "__main__":
    main()
