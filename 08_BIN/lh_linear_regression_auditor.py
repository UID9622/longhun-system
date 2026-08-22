#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 线性回归体检器 v1.1
DNA: #龍芯⚡️丙午·乙未·癸酉·酉时·䷒临-LINEAR-REGRESSION-AUDITOR-v1.1-8F2E1A6D
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

基于 CSDN 文章《线性回归没你想的那么简单：R²虚高、P值误用》落地的自动化体检工具。

核心能力：
  - 对任意 CSV 数据集或 sklearn diabetes 数据集跑线性回归
  - 输出 R² / Adj.R² / 测试集 R²
  - 用 statsmodels 输出每个特征的系数、P值、显著性
  - 自动检测 R² 虚高：往模型里塞随机噪声特征，看训练 R² 是否上涨而测试 R² 是否下跌
  - 生成三色审计报告（绿/黄/红）
  - 一键生成 CSDN 博文 Markdown 素材

用法：
  # 使用 sklearn diabetes 数据集做演示
  python3 bin/lh_linear_regression_auditor.py --demo

  # 生成示例 CSV 数据练手
  python3 bin/lh_linear_regression_auditor.py --example-csv data/my_data.csv

  # 对自己的 CSV 文件体检
  python3 bin/lh_linear_regression_auditor.py --csv data/my_data.csv --target y

  # 体检 + 生成 CSDN 博文素材
  python3 bin/lh_linear_regression_auditor.py --csv data/my_data.csv --target y --csdn

v1.1 更新 (2026-07-28 · DeepSeek 建议优化):
  - CSV 不存在时给出友好提示 + 3种解决路径
  - 新增 --example-csv 自动生成带噪声特征的示例数据
  - 新增 --csdn 一键生成 Markdown 博文素材
  - 改进 CSV 读取错误提示（空文件/编码问题/列名不存在）
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore", category=FutureWarning)

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·乙未·癸酉·酉时·䷒临-LINEAR-REGRESSION-AUDITOR-v1.1-8F2E1A6D"
SCHEMA_VERSION = "1.0.0"

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "data" / "audit" / "linear_regression"
DEFAULT_REPORT_FILE = OUTPUT_DIR / "lr_audit_report.json"


def _now() -> str:
    return datetime.now(CST).isoformat()


def _log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴", "SKIP": "⏭️", "AUDIT": "🔍"}
    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] {markers.get(level, 'ℹ️')} {msg}")


def adj_r2(r2: float, n: int, k: int) -> float:
    """计算调整后 R²"""
    if n - k - 1 <= 0:
        return float("nan")
    return 1 - (1 - r2) * (n - 1) / (n - k - 1)


def load_data(csv_path: Optional[Path] = None, target_col: Optional[str] = None) -> Tuple[pd.DataFrame, pd.Series]:
    """加载数据：CSV 或 demo 数据集"""
    if csv_path:
        if not csv_path.exists():
            _log(f"文件不存在: {csv_path}", "ERROR")
            print(f"\n  💡 找不到你的 CSV 文件。")
            print(f"  请检查路径是否正确。")
            print(f"  示例用法:")
            print(f"    python3 bin/lh_linear_regression_auditor.py --csv data/your_file.csv --target y")
            print(f"\n  或先生成一份示例数据练手:")
            print(f"    python3 bin/lh_linear_regression_auditor.py --example-csv data/my_data.csv")
            print(f"\n  或直接用糖尿病数据集体验:")
            print(f"    python3 bin/lh_linear_regression_auditor.py --demo\n")
            sys.exit(1)

        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            _log(f"无法读取 CSV: {e}", "ERROR")
            print(f"\n  💡 CSV 文件读取出错，请确认:")
            print(f"  - 文件编码是 UTF-8")
            print(f"  - 文件内容未被其他程序占用")
            print(f"  - 列名没有特殊字符\n")
            sys.exit(1)

        if df.empty:
            _log("CSV 文件为空", "ERROR")
            sys.exit(1)

        if target_col not in df.columns:
            _log(f"目标列 '{target_col}' 不存在于 CSV 中", "ERROR")
            avail = ", ".join(df.columns[:10])
            if len(df.columns) > 10:
                avail += f" ... (共 {len(df.columns)} 列)"
            print(f"\n  💡 CSV 中的列名: {avail}")
            print(f"  你指定的目标列是: '{target_col}'")
            print(f"  请用 --target 指定正确的列名\n")
            sys.exit(1)

        y = df[target_col]
        X = df.drop(columns=[target_col])
        # 只保留数值列
        X = X.select_dtypes(include=[np.number])
        if X.shape[1] == 0:
            _log("没有可用的数值特征列（需要数值类型）", "ERROR")
            print(f"\n  💡 去掉目标列后，CSV 中没有发现数值类型的列。")
            print(f"  线性回归只能处理数值特征，请检查你的数据。\n")
            sys.exit(1)
        return X, y

    # demo 模式：diabetes 数据集
    data = load_diabetes()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target, name="progression")
    return X, y


def generate_example_csv(output_path: Path, random_state: int = 42) -> Path:
    """生成一份示例 CSV 数据，用于快速体验工具"""
    rng = np.random.RandomState(random_state)
    n = 50
    X1 = rng.randn(n) * 10 + 50
    X2 = rng.randn(n) * 5 + 25
    noise = rng.randn(n) * 3
    Y = 2.5 * X1 + 1.8 * X2 + noise + 10

    # 故意加一个不显著的噪声特征
    X3_noise = rng.randn(n) * 7

    df = pd.DataFrame({
        "height": X1.round(2),
        "weight": X2.round(2),
        "noise_feature": X3_noise.round(2),
        "score": Y.round(2),
    })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    _log(f"示例 CSV 已生成: {output_path} ({n} 行 x {len(df.columns)} 列)", "OK")
    print(f"\n  📊 数据说明:")
    print(f"  - height: 身高 (显著特征)")
    print(f"  - weight: 体重 (显著特征)")
    print(f"  - noise_feature: 纯噪声 (故意不显著，帮你发现 P值 的妙用)")
    print(f"  - score: 综合评分 = 2.5*身高 + 1.8*体重 + 噪声 (目标列)")
    print(f"\n  接下来用这个 CSV 跑审器:")
    print(f"    python3 bin/lh_linear_regression_auditor.py --csv {output_path} --target score\n")
    return output_path


def generate_csdn_markdown(report: Dict[str, Any]) -> str:
    """将审计报告转为 CSDN 博文 Markdown 素材"""
    diag = report["diagnosis"]
    ev = report["model_eval"]
    noise = report["noise_experiment"]
    sm = report["statsmodels"]
    pv = report["pvalue_features"]

    lines = []
    lines.append(f"# 🧪 线性回归体检报告：用龍魂审计器给 {report['dataset']} 做了一次「R² 照妖镜」\n")
    lines.append(f"> 🐉 工具: 龍魂 · 线性回归体检器 v1.1")
    lines.append(f"> 📅 生成时间: {report['generated_at']}")
    lines.append(f"> 🔗 开源: [GitHub](https://github.com/uid9622/longhun-system)\n")

    # 结论先行
    lines.append("---\n")
    lines.append("## 一、结论：{0}\n".format(
        "🟢 模型指标良好" if diag["overall"] == "green"
        else "🟡 模型可用但需优化" if diag["overall"] == "yellow"
        else "🔴 模型存在明显问题，不建议直接上线"
    ))

    # 数据概况
    lines.append("---\n")
    lines.append("## 二、数据概况\n")
    lines.append(f"| 指标 | 值 |")
    lines.append(f"|:---|---:|")
    lines.append(f"| 样本数 | {ev['n_train'] + ev['n_test']} |")
    lines.append(f"| 特征数 | {ev['n_features']} |")
    lines.append(f"| 训练集 | {ev['n_train']} 条 |")
    lines.append(f"| 测试集 | {ev['n_test']} 条 |")

    # R² 对比
    lines.append("\n---\n")
    lines.append("## 三、R² 核心指标\n")
    lines.append(f"| 指标 | 值 |")
    lines.append(f"|:---|---:|")
    lines.append(f"| 训练集 R² | **{ev['train_r2']}** |")
    lines.append(f"| 训练集 Adj.R² | {ev['train_adj_r2']} |")
    lines.append(f"| 测试集 R² | {ev['test_r2']} |")
    gap = ev["train_r2"] - ev["test_r2"]
    lines.append(f"| 训练/测试差距 | {gap:.4f} {'⚠️ 过拟合风险' if gap > 0.05 else '✅ 正常'} |")

    # statsmodels
    if sm.get("available"):
        lines.append("\n---\n")
        lines.append("## 四、统计检验（statsmodels）\n")
        lines.append(f"| 统计量 | 值 |")
        lines.append(f"|:---|---:|")
        lines.append(f"| F 统计量 | {sm.get('f_statistic', 'N/A')} |")
        lines.append(f"| AIC | {sm.get('aic', 'N/A')} |")
        lines.append(f"| BIC | {sm.get('bic', 'N/A')} |")

        lines.append("\n### 特征显著性（P < 0.05 为显著）\n")
        lines.append("| 特征 | 系数 | P值 | 是否显著 |")
        lines.append("|:---|:---:|:---:|:---:|")
        for f in pv:
            icon = "✅" if f["significant"] == "significant" else "❌"
            lines.append(f"| {f['feature']} | {f['coef']:.4f} | {f['p_value']:.6f} | {icon} |")

    # R² 虚高实验
    lines.append("\n---\n")
    lines.append("## 五、R² 虚高检测实验 🔥\n")
    lines.append("> **往模型里塞纯随机噪声特征，看 R² 怎么变。这是识别「特征工程水分」的杀手锏。**\n")
    lines.append("| 噪声特征数 | 总特征数 | 训练 R² | 训练 Adj.R² | 测试 R² |")
    lines.append("|:---:|:---:|:---:|:---:|:---:|")
    for r in noise:
        lines.append(f"| {r['noise_features']} | {r['total_features']} | {r['train_r2']} | {r['train_adj_r2']} | {r['test_r2']} |")

    if len(noise) >= 2:
        baseline = noise[0]
        max_n = noise[-1]
        train_gain = max_n["train_r2"] - baseline["train_r2"]
        test_loss = baseline["test_r2"] - max_n["test_r2"]
        lines.append(f"\n**关键发现**: 加入 {max_n['noise_features']} 列纯噪声后：")
        lines.append(f"- 训练 R² 从 {baseline['train_r2']} 涨到 {max_n['train_r2']}（+{train_gain:.4f}）📈")
        lines.append(f"- 测试 R² 从 {baseline['test_r2']} 跌到 {max_n['test_r2']}（-{test_loss:.4f}）📉")
        if train_gain > 0.03:
            lines.append(f"- ⚠️ **结论: R² 被噪声严重污染**，不能只看 R²，必须配合 Adj.R² 和测试集指标")
        else:
            lines.append(f"- ✅ 模型对噪声不敏感，指标相对稳健")

    # 诊断
    if diag["issues"]:
        lines.append("\n---\n")
        lines.append("## 六、🔴 严重问题\n")
        for issue in diag["issues"]:
            lines.append(f"- **{issue['type']}**: {issue['message']}")
            lines.append(f"  > 💡 {issue['suggestion']}\n")

    if diag["warnings"]:
        lines.append("\n---\n")
        lines.append("## 七、🟡 警告\n")
        for w in diag["warnings"]:
            lines.append(f"- **{w['type']}**: {w['message']}")
            lines.append(f"  > 💡 {w['suggestion']}\n")

    if diag["ok"]:
        lines.append("\n---\n")
        lines.append("## 八、🟢 健康项\n")
        for item in diag["ok"]:
            lines.append(f"- ✅ {item}")

    lines.append("\n---\n")
    lines.append("## 九、关于这个工具\n")
    lines.append("> 🐉 **龍魂 · 线性回归体检器** 是一个开源的主权 AI 审计工具。")
    lines.append("> 地址: `longhun-system/bin/lh_linear_regression_auditor.py`")
    lines.append("> 协议: CC BY-NC-SA 4.0\n")
    lines.append(f"> DNA: `{report['dna']}`\n")

    return "\n".join(lines)


def fit_and_evaluate(X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test: pd.Series) -> Dict[str, Any]:
    """拟合模型并返回评估指标"""
    model = LinearRegression()
    model.fit(X_train, y_train)

    train_r2 = model.score(X_train, y_train)
    test_r2 = model.score(X_test, y_test)
    n_train, k = X_train.shape
    train_adj_r2 = adj_r2(train_r2, n_train, k)

    return {
        "train_r2": round(train_r2, 4),
        "test_r2": round(test_r2, 4),
        "train_adj_r2": round(train_adj_r2, 4),
        "n_features": k,
        "n_train": n_train,
        "n_test": len(X_test),
        "coef": {name: round(float(coef), 4) for name, coef in zip(X_train.columns, model.coef_)},
        "intercept": round(float(model.intercept_), 4),
    }


def statsmodels_summary(X_train: pd.DataFrame, y_train: pd.Series) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """用 statsmodels 输出 P值和完整统计量"""
    try:
        import statsmodels.api as sm
    except ImportError:
        _log("statsmodels 未安装，跳过 P值分析", "WARN")
        return {"available": False}, []

    X_sm = sm.add_constant(X_train)
    ols = sm.OLS(y_train, X_sm).fit()

    summary = {
        "available": True,
        "r2": round(ols.rsquared, 4),
        "adj_r2": round(ols.rsquared_adj, 4),
        "f_statistic": round(ols.fvalue, 4) if hasattr(ols, "fvalue") else None,
        "aic": round(ols.aic, 2) if hasattr(ols, "aic") else None,
        "bic": round(ols.bic, 2) if hasattr(ols, "bic") else None,
    }

    features = []
    for name, coef, pvalue in zip(X_sm.columns, ols.params, ols.pvalues):
        if name == "const":
            continue
        significant = "significant" if pvalue < 0.05 else "not_significant"
        features.append({
            "feature": name,
            "coef": round(float(coef), 4),
            "p_value": round(float(pvalue), 6),
            "significant": significant,
            "threshold": 0.05,
        })

    return summary, features


def noise_inflation_experiment(X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test: pd.Series,
                               noise_levels: List[int] = [0, 10, 30, 60],
                               random_state: int = 42) -> List[Dict[str, Any]]:
    """R² 虚高检测实验：往数据里加纯随机噪声特征"""
    rng = np.random.RandomState(random_state)
    max_noise = max(noise_levels)
    JTR = rng.randn(len(X_train), max_noise)
    JTE = rng.randn(len(X_test), max_noise)

    results = []
    for n_junk in noise_levels:
        Xtr_j = X_train.copy()
        Xte_j = X_test.copy()
        for i in range(n_junk):
            col_name = f"__noise_{i}"
            Xtr_j[col_name] = JTR[:, i]
            Xte_j[col_name] = JTE[:, i]

        model = LinearRegression()
        model.fit(Xtr_j, y_train)
        r2_train = model.score(Xtr_j, y_train)
        r2_test = model.score(Xte_j, y_test)
        adj_train = adj_r2(r2_train, len(Xtr_j), Xtr_j.shape[1])

        results.append({
            "noise_features": n_junk,
            "total_features": Xtr_j.shape[1],
            "train_r2": round(r2_train, 4),
            "train_adj_r2": round(adj_train, 4),
            "test_r2": round(r2_test, 4),
        })

    return results


def diagnose(model_eval: Dict[str, Any], noise_results: List[Dict[str, Any]],
             pvalue_features: List[Dict[str, Any]]) -> Dict[str, Any]:
    """综合诊断，输出风险等级和建议"""
    issues = []
    warnings_list = []
    ok_items = []

    # 1. 训练/测试 R² 差距
    gap = model_eval["train_r2"] - model_eval["test_r2"]
    if gap > 0.15:
        issues.append({
            "severity": "high",
            "type": "overfitting_gap",
            "message": f"训练集 R² ({model_eval['train_r2']}) 比测试集 R² ({model_eval['test_r2']}) 高 {gap:.4f}，存在过拟合嫌疑",
            "suggestion": "减少特征数量、增加样本、或引入正则化（Ridge/Lasso）",
        })
    elif gap > 0.05:
        warnings_list.append({
            "severity": "medium",
            "type": "overfitting_gap",
            "message": f"训练/测试 R² 差距 {gap:.4f}，需关注",
            "suggestion": "检查是否特征过多或样本不足",
        })
    else:
        ok_items.append("训练/测试 R² 差距在合理范围内")

    # 2. R² 虚高检测
    if len(noise_results) >= 2:
        baseline = noise_results[0]
        max_noise = noise_results[-1]
        train_r2_gain = max_noise["train_r2"] - baseline["train_r2"]
        test_r2_loss = baseline["test_r2"] - max_noise["test_r2"]

        if train_r2_gain > 0.03 and test_r2_loss > 0.03:
            issues.append({
                "severity": "high",
                "type": "r2_inflation",
                "message": f"加入 {max_noise['noise_features']} 列噪声后，训练 R² 上涨 {train_r2_gain:.4f}，测试 R² 下跌 {test_r2_loss:.4f}",
                "suggestion": "R² 容易被噪声特征抬高，请优先参考 Adj.R² 和测试集指标；剔除 P值 > 0.05 的特征",
            })
        elif train_r2_gain > 0.01:
            warnings_list.append({
                "severity": "medium",
                "type": "r2_inflation",
                "message": f"加入噪声后训练 R² 上涨 {train_r2_gain:.4f}",
                "suggestion": "警惕用 R² 作为唯一评估指标",
            })
        else:
            ok_items.append("噪声特征没有显著抬高 R²，指标相对稳健")

    # 3. P值显著性
    if pvalue_features:
        insignificant = [f for f in pvalue_features if f["significant"] == "not_significant"]
        significant = [f for f in pvalue_features if f["significant"] == "significant"]
        if len(insignificant) / len(pvalue_features) > 0.5:
            issues.append({
                "severity": "high",
                "type": "insignificant_features",
                "message": f"{len(insignificant)}/{len(pvalue_features)} 个特征 P值 >= 0.05，不显著",
                "suggestion": "考虑剔除不显著特征，重新拟合模型",
            })
        elif insignificant:
            warnings_list.append({
                "severity": "low",
                "type": "insignificant_features",
                "message": f"{len(insignificant)} 个特征不显著: {', '.join(f['feature'] for f in insignificant[:3])}",
                "suggestion": "检查这些特征是否真的对目标有解释力",
            })
        else:
            ok_items.append("所有特征 P值 < 0.05，均显著")

    # 4. Adj.R² 与 R² 差距
    r2_adj_gap = model_eval["train_r2"] - model_eval["train_adj_r2"]
    if r2_adj_gap > 0.05:
        warnings_list.append({
            "severity": "medium",
            "type": "adj_r2_penalty",
            "message": f"R² ({model_eval['train_r2']}) 与 Adj.R² ({model_eval['train_adj_r2']}) 差距 {r2_adj_gap:.4f}",
            "suggestion": "特征数量相对样本可能过多，优先用 Adj.R² 评估",
        })
    else:
        ok_items.append("R² 与 Adj.R² 接近，特征惩罚不大")

    # 综合评级
    if issues:
        overall = "red"
        overall_text = "🔴 高风险：模型存在明显问题，不建议直接上线"
    elif warnings_list:
        overall = "yellow"
        overall_text = "🟡 中风险：模型可用但需优化"
    else:
        overall = "green"
        overall_text = "🟢 低风险：模型指标健康"

    return {
        "overall": overall,
        "overall_text": overall_text,
        "issues": issues,
        "warnings": warnings_list,
        "ok": ok_items,
    }


def print_report(report: Dict[str, Any]):
    """终端友好报告"""
    print("\n" + "=" * 60)
    print(f"  线性回归体检报告 · {report['generated_at']}")
    print(f"  数据集: {report['dataset']}")
    print(f"  目标列: {report['target']}")
    print("=" * 60)

    diag = report["diagnosis"]
    print(f"\n{diag['overall_text']}")

    print("\n📊 基础指标:")
    ev = report["model_eval"]
    print(f"  训练集 R²:     {ev['train_r2']}")
    print(f"  训练集 Adj.R²: {ev['train_adj_r2']}")
    print(f"  测试集 R²:     {ev['test_r2']}")
    print(f"  特征数:        {ev['n_features']}")
    print(f"  训练样本:      {ev['n_train']}  测试样本: {ev['n_test']}")

    if report["statsmodels"]["available"]:
        print(f"\n📈 statsmodels 统计量:")
        smr = report["statsmodels"]
        print(f"  R²:      {smr['r2']}")
        print(f"  Adj.R²:  {smr['adj_r2']}")
        print(f"  F统计量: {smr['f_statistic']}")
        print(f"  AIC:     {smr['aic']}  BIC: {smr['bic']}")

        print(f"\n🔬 特征显著性 (P < 0.05 为显著):")
        for f in report["pvalue_features"]:
            marker = "✅" if f["significant"] == "significant" else "❌"
            print(f"  {marker} {f['feature']:20s} coef={f['coef']:10.4f}  P={f['p_value']:.6f}")

    print(f"\n🧪 R² 虚高检测实验（加入随机噪声特征）:")
    print(f"{'噪声特征数':>10s} {'总特征数':>10s} {'训练R²':>10s} {'训练Adj.R²':>12s} {'测试R²':>10s}")
    for r in report["noise_experiment"]:
        print(f"{r['noise_features']:>10d} {r['total_features']:>10d} {r['train_r2']:>10.4f} {r['train_adj_r2']:>12.4f} {r['test_r2']:>10.4f}")

    if diag["issues"]:
        print(f"\n🔴 严重问题:")
        for issue in diag["issues"]:
            print(f"  • {issue['message']}")
            print(f"    建议: {issue['suggestion']}")

    if diag["warnings"]:
        print(f"\n🟡 警告:")
        for w in diag["warnings"]:
            print(f"  • {w['message']}")
            print(f"    建议: {w['suggestion']}")

    if diag["ok"]:
        print(f"\n🟢 健康项:")
        for item in diag["ok"]:
            print(f"  • {item}")

    print(f"\n📁 完整报告: {report['report_file']}")


def main():
    parser = argparse.ArgumentParser(
        description="龍魂线性回归体检器 · 给线性回归做「R² 照妖镜」",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 %(prog)s --demo                          # 用糖尿病数据集演示
  python3 %(prog)s --example-csv data/my_data.csv  # 生成示例 CSV
  python3 %(prog)s --csv data/my_data.csv --target score --csdn  # 体检+博文素材
        """,
    )
    parser.add_argument("--demo", action="store_true", help="使用 sklearn diabetes 数据集演示")
    parser.add_argument("--csv", type=Path, help="输入 CSV 文件路径")
    parser.add_argument("--target", type=str, help="目标列名 (配合 --csv 使用)")
    parser.add_argument("--example-csv", type=Path, help="生成一份示例 CSV 数据 (用于练手)")
    parser.add_argument("--csdn", action="store_true", help="额外输出一份 Markdown 博文素材")
    parser.add_argument("--test-size", type=float, default=0.2, help="测试集比例 (默认 0.2)")
    parser.add_argument("--random-state", type=int, default=42, help="随机种子 (默认 42)")
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT_FILE, help="JSON 报告输出路径")
    args = parser.parse_args()

    print(f"\n{DNA}\n")

    # 示例 CSV 生成
    if args.example_csv:
        generate_example_csv(args.example_csv, random_state=args.random_state)
        return

    # 参数校验
    if not args.demo and not args.csv:
        parser.print_help()
        print("\n  💡 三种用法:")
        print("    1. 快速演示:    python3 bin/lh_linear_regression_auditor.py --demo")
        print("    2. 生成示例数据: python3 bin/lh_linear_regression_auditor.py --example-csv data/my_data.csv")
        print("    3. 体检你的数据: python3 bin/lh_linear_regression_auditor.py --csv your_file.csv --target y")
        sys.exit(1)

    if args.csv and not args.target:
        _log("使用 --csv 时必须指定 --target (目标列名)", "ERROR")
        print(f"\n  💡 示例: --csv {args.csv} --target 你的目标列名\n")
        sys.exit(1)

    # 加载数据
    if args.demo:
        _log("使用 diabetes 数据集（CSDN 文章同款）", "INFO")
        X, y = load_data()
        dataset_name = "sklearn_diabetes"
        target_name = "progression"
    else:
        _log(f"加载 CSV: {args.csv}", "INFO")
        X, y = load_data(args.csv, args.target)
        dataset_name = str(args.csv)
        target_name = args.target

    _log(f"样本数: {len(X)}  特征数: {X.shape[1]}", "INFO")

    # 划分数据
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=args.random_state
    )

    # 拟合与评估
    _log("拟合 LinearRegression...", "INFO")
    model_eval = fit_and_evaluate(X_train, X_test, y_train, y_test)

    # statsmodels P值
    _log("计算 P值...", "INFO")
    statsmodels_summary_dict, pvalue_features = statsmodels_summary(X_train, y_train)

    # R² 虚高实验
    _log("进行 R² 虚高检测实验...", "INFO")
    noise_results = noise_inflation_experiment(X_train, X_test, y_train, y_test, random_state=args.random_state)

    # 诊断
    diagnosis = diagnose(model_eval, noise_results, pvalue_features)

    # 生成报告
    report = {
        "dna": DNA,
        "version": SCHEMA_VERSION,
        "generated_at": _now(),
        "dataset": dataset_name,
        "target": target_name,
        "test_size": args.test_size,
        "random_state": args.random_state,
        "model_eval": model_eval,
        "statsmodels": statsmodels_summary_dict,
        "pvalue_features": pvalue_features,
        "noise_experiment": noise_results,
        "diagnosis": diagnosis,
        "report_file": str(args.output),
    }

    # 保存 JSON 报告
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    _log(f"JSON 报告已保存: {args.output}", "OK")

    # CSDN 博文素材
    if args.csdn:
        md_content = generate_csdn_markdown(report)
        md_path = args.output.with_suffix(".md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        _log(f"CSDN 博文素材已保存: {md_path}", "OK")

    # 终端报告
    print_report(report)

    # 提示
    if not args.csdn:
        print(f"\n  💡 想生成 CSDN 博文素材？加上 --csdn 参数即可。")

    _log("完成", "OK")


if __name__ == "__main__":
    main()
