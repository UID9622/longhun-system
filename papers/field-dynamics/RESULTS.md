# 评测结果 · 合成示例日志（开箱即测）

DNA: #龍芯⚡️丙午·丙申·乙丑·壬午·䷨损-FIELD-DYNAMICS-RESULTS-v1.0
创建者: 诸葛鑫（UID9622）
数据: `sample-log.jsonl`（1000 条 · 合成 · seed=42 · 2 个标注翻转点）
生成: `python3 evaluator/gen_sample_log.py --n 1000`
评测: `python3 evaluator/evaluator.py --log sample-log.jsonl --crash-window 300`

---

## 原始输出

```json
{
  "log": "sample-log.jsonl",
  "events": 1000,
  "fhi_now": 0.88,
  "dim_means": { "U": 0.9603, "D": 0.2, "A": 0.0703, "H": 0.7674 },
  "alerts": {
    "precursor_lead_time": 196.0,
    "fpr": 0.1192,
    "fnr": 0.0,
    "f1": 0.0325,
    "n_alerts": 119,
    "n_crashes": 2
  },
  "weights": { "U": 0.25, "D": 0.25, "A": 0.25, "H": 0.25 },
  "threshold": 0.3
}
```

## 结果解读（诚实版）

| 指标 | 值 | 含义 | 解读 |
|:---|:---:|:---|:---|
| 预警提前量 Δt | 196 事件 | 崩溃前最后一次预警距崩溃的间隔 | 合成数据失谐窗口长（160/130 事件），预警很早 |
| 漏报率 FNR | 0.0% | 崩溃前无预警比例 | 2 个翻转点全部提前捕获 ✅ |
| 误报率 FPR | 11.9% | 未崩溃窗口内预警比例 | 失谐窗口内持续预警 → 偏高 |
| F1 | 0.03 | 权衡分 | **低分暴露真问题**：A 维阈值预警在长失谐窗口下过度触发 |
| FHI 现值 | 0.88 | 场域健康度 | 全窗口均值正常，但窗口期下降到 0.63 区间 |

> **这份结果的意义**：评测器不粉饰。合成数据把"提前预警但易误报"这个真实 trade-off 完整暴露出来 —— 这正是跨框架验证要解决的问题（H1 阈值标定 / H2 低对抗性僵死）。

## 可复现

```bash
# 任何人有 Python 3.9+ 即可复现（零第三方依赖）
python3 evaluator/gen_sample_log.py --n 1000
python3 evaluator/evaluator.py --log sample-log.jsonl --crash-window 300
```

## 下一步（数据侧）

- [ ] P1: 真实框架日志接入（TLAA/TAT/Cophy/HeartFlow 社区贡献）
- [ ] P2: 阈值网格扫描 `--threshold 0.1,0.2,...,0.6` 检验 H1
- [ ] P2: 构造 A=0 低对抗性反例验证 H2
