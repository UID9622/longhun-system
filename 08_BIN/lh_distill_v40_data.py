#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·辛亥·申时·☰乾-V40-DISTILL-OLLAMA
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂v4.0 · 知识蒸馏数据生成 (Ollama版)
老师: longhun-v3.8-expanded (Ollama)
学生: Llama-3.1-8B
输出: Llama-3.1 chat template格式训练数据

用法: python3 bin/lh_distill_v40_data.py [--limit N] [--temp 0.1] [--workers 4]

DNA: #龍芯⚡️丙午·乙未·辛亥·申时·☰乾-V40-DISTILL-OLLAMA
"""

import json, sys, time, argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request, urllib.error

PROJECT = Path.home() / "longhun-system"
MODEL_DIR = PROJECT / "models" / "longhun-v1.0"
DATA_IN = MODEL_DIR / "lora_output" / "data_v38_expanded" / "train.jsonl"
DATA_OUT = MODEL_DIR / "lora_output" / "data_v40_distill"
OLLAMA_URL = "http://localhost:11434/api/generate"
TEACHER_MODEL = "longhun-v3.8-expanded"

DATA_OUT.mkdir(parents=True, exist_ok=True)

# ── 帮助函数 ──
def log(msg): print(f"[龍魂·蒸馏] {msg}", flush=True)
def ok(msg): print(f"  ✅ {msg}", flush=True)
def warn(msg): print(f"  ⚠️ {msg}", flush=True)

# ── 解析参数 ──
parser = argparse.ArgumentParser()
parser.add_argument("--limit", type=int, default=0, help="限制条数(0=全部)")
parser.add_argument("--temp", type=float, default=0.1, help="温度")
parser.add_argument("--workers", type=int, default=4, help="并发数")
parser.add_argument("--max-tokens", type=int, default=512)
args = parser.parse_args()

# ── 单条蒸馏函数 ──
def distill_one(item):
    """用老师模型生成回答，返回Llama格式数据"""
    messages = item["messages"]
    metadata = item.get("metadata", {})
    domain = metadata.get("domain", "unknown")

    # 提取 system + user
    system_msg = ""
    user_msgs = []
    for m in messages:
        if m["role"] == "system":
            system_msg = m["content"]
        elif m["role"] == "user":
            user_msgs.append(m["content"])

    if not user_msgs:
        return None

    # 构建 Qwen chat prompt（老师模型用Qwen格式）
    prompt = ""
    if system_msg:
        prompt += f"<|im_start|>system\n{system_msg}\n<|im_end|>\n"
    prompt += f"<|im_start|>user\n{user_msgs[-1]}\n<|im_end|>\n"
    prompt += "<|im_start|>assistant\n"

    # 调用Ollama
    payload = json.dumps({
        "model": TEACHER_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": args.temp,
            "num_predict": args.max_tokens,
        }
    }).encode("utf-8")

    try:
        req = urllib.request.Request(OLLAMA_URL, data=payload,
            headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read().decode("utf-8"))
        response = result.get("response", "").strip()
    except Exception as e:
        return {"error": str(e), "domain": domain}

    if not response or len(response) < 10:
        return {"error": "response too short", "domain": domain}

    # 构建 Llama-3.1 格式
    llama_msgs = []
    if system_msg:
        llama_msgs.append({"role": "system", "content": system_msg})
    llama_msgs.append({"role": "user", "content": user_msgs[-1]})
    llama_msgs.append({"role": "assistant", "content": response})

    return {
        "messages": llama_msgs,
        "metadata": {
            "domain": domain,
            "source": "v40_distill_ollama",
            "teacher": TEACHER_MODEL,
            "temp": args.temp,
        }
    }

# ── 主流程 ──
def main():
    if not DATA_IN.exists():
        print(f"❌ 训练数据不存在: {DATA_IN}")
        sys.exit(1)

    with open(DATA_IN) as f:
        raw_items = []
        for line in f:
            line = line.strip()
            if not line: continue
            try:
                item = json.loads(line)
                if "messages" in item:
                    raw_items.append(item)
            except: pass

    total = len(raw_items)
    log(f"训练数据: {total} 条")
    if args.limit > 0:
        raw_items = raw_items[:args.limit]
        total = len(raw_items)
        log(f"限制到 {total} 条")

    log(f"开始蒸馏 · 老师={TEACHER_MODEL} · temp={args.temp} · workers={args.workers}")
    log(f"预计时间: ~{total / 50 * args.workers / args.workers:.0f}分钟 ({total}条)")

    t0 = time.time()
    results = []
    fail_count = 0

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(distill_one, item): i for i, item in enumerate(raw_items)}

        for future in as_completed(futures):
            idx = futures[future]
            try:
                result = future.result()
                if result is None:
                    fail_count += 1
                elif "error" in result:
                    fail_count += 1
                else:
                    results.append((idx, result))
            except Exception as e:
                fail_count += 1

            done = len(results) + fail_count
            if done % 50 == 0 or done == total:
                elapsed = time.time() - t0
                speed = done / elapsed * 60 if elapsed > 0 else 0
                eta = (total - done) / speed if speed > 0 else 0
                log(f"进度: {done}/{total} · {speed:.0f}条/分 · 剩余 {eta:.0f}分")

    # 按原始顺序排列
    results.sort(key=lambda x: x[0])
    distill_data = [r[1] for r in results]

    # 9:1 分割
    split = max(1, int(len(distill_data) * 0.9))
    train_data = distill_data[:split]
    valid_data = distill_data[split:]

    for name, data in [("train.jsonl", train_data), ("valid.jsonl", valid_data)]:
        path = DATA_OUT / name
        with open(path, 'w') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

    # 统计
    domain_counts = {}
    for item in distill_data:
        d = item["metadata"]["domain"]
        domain_counts[d] = domain_counts.get(d, 0) + 1

    elapsed = time.time() - t0
    log("=" * 50)
    log(f"蒸馏完成！耗时 {elapsed/60:.1f} 分钟")
    log(f"成功: {len(distill_data)} · 失败: {fail_count}")
    log(f"train={len(train_data)}, valid={len(valid_data)}")
    log(f"领域分布:")
    for d, c in sorted(domain_counts.items(), key=lambda x: -x[1]):
        print(f"  {d}: {c}条")
    log(f"输出: {DATA_OUT}")
    ok("蒸馏数据生成完成 ✅")

if __name__ == "__main__":
    main()
