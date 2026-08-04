#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
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

import json
import os
import random
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh_dna_generator import generate_dna

PROJECT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT / "models" / "longhun-v1.0" / "lora_output" / "k3_distill_v39"

API_KEY = os.getenv("KIMI_API_KEY") or os.getenv("KIMI_API_KEY_LONGHUN")
BASE_URL = os.getenv("KIMI_BASE_URL", "https://api.moonshot.cn/v1")
ENDPOINT = f"{BASE_URL}/chat/completions"

# 优先尝试 K3，失败则回退到 moonshot-v1-128k（用于探测）
MODEL_CANDIDATES = ["kimi-k3", "moonshot-v1-128k", "moonshot-v1-8k"]

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


def validate_think_format(content: str) -> bool:
    """检查是否包含 <think>...</think> 格式"""
    return "<think>" in content and "</think>" in content


def process_domain(name: str, questions: list[str], repeat_variants: int = 1) -> list[dict]:
    """为某个域生成 K3 蒸馏样本"""
    print(f"\n🔥 开始蒸馏 [{name}]：{len(questions)} 个基础问题")
    samples = []
    model = None
    bad_format_count = 0

    system_prompt = DOMAIN_SYS_PROMPTS.get(name, BASE_SYS_PROMPT)

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
                if ref:
                    user_content = f"问题：{v}\n\n参考答案（必须保留核心立场和事实，可在此基础上组织语言）：\n{ref}\n\n请先写<think>推理过程</think>，再给出正式回答。"
                else:
                    user_content = f"问题：{v}\n\n请先写<think>推理过程</think>，再给出正式回答。"
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
    if not API_KEY:
        print("❌ 未设置 KIMI_API_KEY_LONGHUN 或 KIMI_API_KEY 环境变量")
        sys.exit(1)

    print("🚀 龍魂 v3.9 K3 蒸馏启动")
    print(f"   API: {BASE_URL}")
    print(f"   输出: {OUTPUT_DIR}")
    print(f"   DNA: {generate_dna('K3-DISTILL', '3.9')}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    random.seed(42)

    all_samples = []

    # 家法：23 问 × 4 变体 = 92
    jiafa = process_domain("家法第一条", JIAFA_QUESTIONS, repeat_variants=4)
    _save(jiafa, "jiafa_qa.jsonl")
    all_samples.extend(jiafa)

    # 主权边界：35 问
    sovereignty = process_domain("主权边界", SOVEREIGNTY_QUESTIONS, repeat_variants=1)
    _save(sovereignty, "sovereignty_qa.jsonl")
    all_samples.extend(sovereignty)

    # 多轮对话：24 问（v3.8.1 实际 24 条）
    multiturn = process_domain("多轮对话", MULTITURN_QUESTIONS, repeat_variants=1)
    _save(multiturn, "multiturn_qa.jsonl")
    all_samples.extend(multiturn)

    # 20% 抽查
    review_n = max(1, int(len(all_samples) * 0.2))
    review_samples = random.sample(all_samples, review_n)
    _save(review_samples, "review_sample.jsonl")

    # 统计
    print("\n" + "="*50)
    print(f"   家法第一条: {len(jiafa)} 条")
    print(f"   主权边界:   {len(sovereignty)} 条")
    print(f"   多轮对话:   {len(multiturn)} 条")
    print(f"   总计:       {len(all_samples)} 条")
    print(f"   抽查样本:   {len(review_samples)} 条 → review_sample.jsonl")
    print("="*50)
    print("\n✅ K3 蒸馏完成。请人工抽查 review_sample.jsonl，胡话率 >5% 请删除对应域 JSONL 后重跑。")


def _save(samples: list[dict], filename: str):
    path = OUTPUT_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"   💾 保存: {path} ({len(samples)} 条)")


if __name__ == "__main__":
    main()
