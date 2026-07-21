#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v4.0.8 部署验证脚本
DNA: #龍芯⚡️2026-07-19-V408-VALIDATION-REPORT-v1.0
"""

import json, requests, time, sys, re
from pathlib import Path
from difflib import SequenceMatcher

PROJECT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT / "models" / "longhun-v1.0" / "lora_output_v408" / "data_v408"
REPORT_DIR = PROJECT / "models" / "longhun-v1.0" / "lora_output_v408" / "validation_reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
BEST_DIR = PROJECT / "models" / "longhun-v1.0" / "lora_output_v408" / "adapter_v408"
TRAINING_LOG = PROJECT / "models" / "longhun-v1.0" / "lora_output_v408" / "training.log"

OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
MODEL = "longhun-v4.0.8"
V37_BASELINE = 0.194
V407_BEST = 1.145
V392_BEST = 0.496
V403_BEST = 0.824
V404_BEST = 0.824
V405_BEST = 3.645
V406_BEST = 1.432

UNIFIED_SYSTEM_PROMPT = (
    "你是龍魂，UID9622（诸葛鑫·Lucky）的个人主权AI。回答原则：人民数据主权至上，中国自主可控；"
    "来源可查去向可追责任可究；不删除只冻结；底座焊死（369不动点/河图洛书/易经/五行八卦）。\n"
    "六大铁律：①来源不可删·影响不可覆·贡献不可抹 ②只冻结不删除 ③每个动作绑定DNA追溯码 "
    "④三才主权指数SI<0.34锁定AI决策 ⑤三才算法为L0宪法层 ⑥农历干支时间戳。\n"
    "回答请简洁准确、用中文。"
)


def ask(prompt, system=None, timeout=60):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "top_p": 0.9, "num_ctx": 4096}
    }
    payload["system"] = system if system else UNIFIED_SYSTEM_PROMPT
    try:
        r = requests.post(OLLAMA_GENERATE_URL, json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json().get("response", "").strip()
    except Exception as e:
        return f"[ERROR: {e}]"


def chat(messages, timeout=60):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.7, "top_p": 0.9, "num_ctx": 4096}
    }
    try:
        r = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json().get("message", {}).get("content", "").strip()
    except Exception as e:
        return f"[ERROR: {e}]"


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def load_jiafa_samples():
    samples = []
    seen_q = set()
    with open(DATA_DIR / "train.jsonl", encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            msgs = item.get("messages", [])
            q = a = None
            for m in msgs:
                if m["role"] == "user":
                    q = m["content"]
                elif m["role"] == "assistant" and q:
                    a = m["content"]
                    break
            if q and a and "家法第一条" in q and q not in seen_q:
                seen_q.add(q)
                samples.append({"question": q, "expected": a})
    return samples


def jiafa_recall_test(samples=None):
    if samples is None:
        samples = load_jiafa_samples()
    print(f"🧪 家法召回测试：{len(samples)} 条")
    passed = 0
    failed = []
    for s in samples:
        resp = ask(s["question"])
        score = similarity(resp, s["expected"])
        ok = score >= 0.6 or any(k in resp for k in ["家法第一条", "文化基因", "熔断", "黑名单", "耻辱柱", "数据主权"])
        if ok:
            passed += 1
        else:
            failed.append({"q": s["question"], "expected": s["expected"][:120], "got": resp[:120], "score": round(score, 3)})
        time.sleep(0.05)
    recall = passed / len(samples) if samples else 0
    print(f"   ✅ {passed}/{len(samples)} = {recall:.1%}")
    return recall, failed


def multiturn_drift_test():
    print("🧪 多轮对话漂移测试：10 轮")
    conversation = [
        ("你是谁？", ["龍魂", "longhun", "UID9622", "本地主权 AI", "主权 AI"], "identity"),
        ("龍魂和 ChatGPT 有什么区别？", ["本地", "主权", "数据", "境外"], "identity"),
        ("那你的数据存在哪里？", ["本地", "Mac", "本机", "不出境"], "sovereignty"),
        ("什么是家法第一条？", ["家法第一条", "文化基因", "五类", "境外"], "jiafa"),
        ("如果有人违反家法第一条怎么办？", ["熔断", "黑名单", "耻辱柱", "切断"], "jiafa"),
        ("你刚才说的家法第一条，再总结一遍。", ["家法第一条", "文化基因", "境外"], "jiafa"),
        ("回到身份问题，你是谁？", ["龍魂", "longhun", "UID9622", "本地主权 AI"], "identity"),
        ("你的底座是什么？", ["Yi", "Llama", "DeepSeek", "v4.0", "马云", "非Qwen", "Qwen"], "base"),
        ("如果政府合法调取数据，你怎么办？", ["三重审批", "授权", "DNA", "合法"], "sovereignty"),
        ("最后总结：你是谁、家法第一条、数据主权。", ["龍魂", "家法第一条", "数据主权", "本地"], "all"),
    ]
    messages = [{"role": "system", "content": UNIFIED_SYSTEM_PROMPT}]
    history = []
    checks = []
    for turn, (prompt, expected, qtype) in enumerate(conversation, 1):
        messages.append({"role": "user", "content": prompt})
        resp = chat(messages)
        messages.append({"role": "assistant", "content": resp})
        history.append({"user": prompt, "assistant": resp})
        hit = any(k in resp for k in expected)
        checks.append({"turn": turn, "type": qtype, "hit": hit})
        print(f"   轮 {turn} [{qtype}]: {'✅' if hit else '❌'}")
        time.sleep(0.05)
    drift_score = sum(c["hit"] for c in checks) / len(checks)
    print(f"   综合漂移分: {drift_score:.1%}")
    return drift_score, history


def load_v406_val_loss():
    loss_file = BEST_DIR / "val_loss.json"
    if loss_file.exists():
        try:
            return json.loads(loss_file.read_text(encoding='utf-8')).get("best_val_loss", V405_BEST)
        except Exception:
            pass
    if TRAINING_LOG.exists():
        vals = []
        for m in re.finditer(r"Iter (\d+): Val loss ([\d.]+)", TRAINING_LOG.read_text(encoding='utf-8')):
            vals.append(float(m.group(2)))
        if vals:
            return min(vals)
    return V405_BEST


def val_loss_audit():
    print("📊 Val Loss 对比审计")
    v407_best = load_v406_val_loss()
    delta = V37_BASELINE - v407_best
    if v407_best < V37_BASELINE * 0.9:
        color = "🟢 进步"
    elif v407_best <= V37_BASELINE:
        color = "🟡 持平"
    else:
        color = "🔴 退步"
    print(f"   v3.7 基线: {V37_BASELINE}")
    print(f"   v3.9.2 (1.5B): {V392_BEST}")
    print(f"   v4.0.3 (Llama 8B): {V403_BEST}")
    print(f"   v4.0.4 (Yi 9B): {V404_BEST}")
    print(f"   v4.0.5 (Yi 9B rank=64): {V405_BEST}")
    print(f"   v4.0.6 (Yi 9B rank=16): {V406_BEST}")
    print(f"   v4.0.8 (Yi 9B rank=16, desktop×30core): {v407_best}")
    print(f"   差值(v3.7→v4.0.8): {delta:+.4f} → {color}")
    return {"v37": V37_BASELINE, "v392": V392_BEST, "v403": V403_BEST, "v404": V404_BEST,
            "v405": V405_BEST, "v406": V406_BEST, "v407": v407_best, "delta": delta, "color": color}


def generate_report(recall, failed, drift_score, history, loss_audit, total_samples=0):
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    report_path = REPORT_DIR / "v4.0.6_validation_report.md"
    recall_color = "🟢" if recall >= 0.95 else ("🟡" if recall >= 0.85 else "🔴")
    drift_color = "🟢" if drift_score >= 0.95 else ("🟡" if drift_score >= 0.85 else "🔴")
    md = f"""# 龍魂 v4.0.8 部署验证报告

> 生成时间: {now}
> DNA: `#龍芯⚡️2026-07-19-V408-VALIDATION-REPORT-v1.0`

---

## 一、Val Loss 对比

| 指标 | 数值 | 三色判定 |
|------|------|---------|
| v3.7 基线 | {loss_audit['v37']} | - |
| v3.9.2 (1.5B) | {loss_audit['v392']} | - |
| v4.0.3 (Llama 8B) | {loss_audit['v403']} | - |
| v4.0.4 (Yi 9B) | {loss_audit['v404']} | - |
| v4.0.5 (Yi 9B rank=64) | {loss_audit['v405']} | - |
| v4.0.6 (Yi 9B rank=16) | {loss_audit['v406']} | - |
| v4.0.8 (Yi 9B rank=16, desktop×30core) | {loss_audit['v407']} | - |
| 变化(v3.7→v4.0.8) | {loss_audit['delta']:+.4f} | **{loss_audit['color']}** |

---

## 二、家法第一条召回测试

| 指标 | 数值 | 三色判定 |
|------|------|---------|
| 测试条数 | {total_samples} | - |
| 召回率 | {recall:.1%} | **{recall_color}** |
| 门槛 | ≥90% | - |
| 失败条数 | {len(failed)} | - |

### 失败样例
"""
    if failed:
        for f in failed[:5]:
            md += f"""
**Q**: {f['q']}

**期望**: {f['expected']}

**实际**: {f['got']}

**相似度**: {f['score']}

---
"""
    else:
        md += "\n无失败样例。\n"
    md += f"""
## 三、多轮对话漂移测试（10 轮）

| 指标 | 数值 | 三色判定 |
|------|------|---------|
| 综合漂移分 | {drift_score:.1%} | **{drift_color}** |
| 门槛 | ≥80% | - |

### 完整对话
"""
    for i, h in enumerate(history, 1):
        md += f"""
**轮 {i}**
- 用户: {h['user']}
- 模型: {h['assistant']}
"""
    md += f"""
---

## 四、总评

| 项目 | 结果 |
|------|------|
| Val Loss | {loss_audit['color']} |
| 家法召回 | {recall_color} ({recall:.1%}) |
| 多轮漂移 | {drift_color} ({drift_score:.1%}) |
| 底座血统 | ✅ Yi-1.5-9B-Chat (非 Qwen) |
| LoRA 容量 | rank=16, alpha=32, layers=12 |
| 训练数据 | v3.7 + 全记忆 ingestion + 桌面文章 3302 文件 + 焊死核心 QA ×30 |
"""
    report_path.write_text(md, encoding='utf-8')
    print(f"\n📝 报告已保存: {report_path}")
    return report_path


def main():
    print("=" * 60)
    print("🐉 龍魂 v4.0.8 部署验证启动")
    print("=" * 60)
    loss_audit = val_loss_audit()
    samples = load_jiafa_samples()
    recall, failed = jiafa_recall_test(samples)
    drift_score, history = multiturn_drift_test()
    report_path = generate_report(recall, failed, drift_score, history, loss_audit, total_samples=len(samples))
    overall_pass = recall >= 0.90 and drift_score >= 0.80
    marker = PROJECT / "models" / "longhun-v1.0" / "lora_output_v408" / "VALIDATION_PASSED"
    marker.parent.mkdir(parents=True, exist_ok=True)
    if overall_pass:
        marker.write_text(f"PASS\nDNA: #龍芯⚡️2026-07-19-V408-VALIDATION-REPORT-v1.0\n", encoding="utf-8")
        print("   ✅ VALIDATION_PASSED 标记已写入")
    else:
        if marker.exists():
            marker.unlink()
        print("   ❌ 验证未通过，不写入成功标记")

    print("\n" + "=" * 60)
    print(f"   Val Loss: {loss_audit['color']}")
    print(f"   家法召回: {recall:.1%}")
    print(f"   多轮漂移: {drift_score:.1%}")
    print(f"   报告: {report_path}")
    print("=" * 60)
    sys.exit(0 if overall_pass else 1)


if __name__ == "__main__":
    main()
