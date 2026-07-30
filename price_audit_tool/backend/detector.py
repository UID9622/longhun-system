"""
价格异常检测引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·辛亥·巳时·☰乾-PRICE-DETECTOR-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
算法透明度声明 (A-BOM)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
目标函数: 检测电商平台可能的大数据杀熟行为
输入特征: 价格、时间、用户类型、商品ID
用户影响: 帮助消费者识别异常定价，维护公平交易
申诉通道: https://uid9622.cn 或项目issue
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

四层检测策略:
  L1 - IQR异常值检测（箱线图法）: 检测价格是否处于统计异常区间
  L2 - 用户分组差异检测: 比较不同用户类型看到的价格差异
  L3 - 时间序列异常: 检测短期内价格剧烈波动
  L4 - 综合杀熟评分: 加权综合判定
"""

import statistics
import math
from datetime import datetime
from typing import Any

# ─── L1: IQR异常值检测（箱线图法） ───

def _iqr_outliers(prices: list[float]) -> list[dict]:
    """IQR方法检测统计异常值。
    
    标准: 超出 [Q1 - 1.5*IQR, Q3 + 1.5*IQR] 视为异常
          超出 [Q1 - 3*IQR, Q3 + 3*IQR] 视为极端异常
    阈值来源: Tukey's fences (John Tukey, 1977)
    """
    if len(prices) < 4:
        return []
    
    sorted_prices = sorted(prices)
    n = len(sorted_prices)
    q1 = statistics.median(sorted_prices[:n // 2])
    q3 = statistics.median(sorted_prices[(n + 1) // 2:])
    iqr = q3 - q1
    
    if iqr == 0:
        return []
    
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    extreme_lower = q1 - 3.0 * iqr
    extreme_upper = q3 + 3.0 * iqr
    
    outliers = []
    for i, p in enumerate(prices):
        if p < extreme_lower or p > extreme_upper:
            outliers.append({
                "index": i, "price": p,
                "type": "极端异常", "severity": "high",
                "deviation": round(p - statistics.mean(prices), 2)
            })
        elif p < lower_fence or p > upper_fence:
            outliers.append({
                "index": i, "price": p,
                "type": "温和异常", "severity": "medium",
                "deviation": round(p - statistics.mean(prices), 2)
            })
    
    return outliers


# ─── L2: 用户分组差异检测 ───

def _group_price_diff(groups: dict[str, list[float]]) -> dict:
    """比较不同用户分组的价格差异。
    
    检测逻辑: 如果同一商品不同用户类型看到的价格均值差异 > 阈值，
    可能是杀熟信号。阈值设为 5%（可配置）。
    """
    if len(groups) < 2:
        return {"suspicious": False, "reason": "只有一组数据，无法比较"}
    
    group_stats = {}
    for name, prices in groups.items():
        if not prices:
            continue
        group_stats[name] = {
            "mean": round(statistics.mean(prices), 2),
            "median": round(statistics.median(prices), 2),
            "min": min(prices), "max": max(prices),
            "count": len(prices)
        }
    
    # 找出最高和最低均价的组
    max_group = max(group_stats.items(), key=lambda x: x[1]["mean"])
    min_group = min(group_stats.items(), key=lambda x: x[1]["mean"])
    
    diff_pct = round((max_group[1]["mean"] - min_group[1]["mean"]) / min_group[1]["mean"] * 100, 1)
    
    suspicious = diff_pct > 5.0  # 差异超过5%标记可疑
    extreme = diff_pct > 15.0    # 差异超过15%标记严重
    
    return {
        "suspicious": suspicious,
        "extreme": extreme,
        "max_diff_pct": diff_pct,
        "higher_group": max_group[0],
        "higher_mean": max_group[1]["mean"],
        "lower_group": min_group[0],
        "lower_mean": min_group[1]["mean"],
        "group_stats": group_stats,
        "verdict": (
            "🔴 严重可疑: 不同用户组价格差异超过15%" if extreme
            else "🟡 可疑: 不同用户组价格差异超过5%" if suspicious
            else "🟢 正常: 不同用户组价格差异在合理范围"
        )
    }


# ─── L3: 时间序列异常检测 ───

def _time_series_anomaly(prices_with_time: list[dict]) -> list[dict]:
    """检测时间序列中的异常价格波动。
    
    使用简单移动平均(SMA) + 标准差法。
    窗口大小 = min(5, len(data)//2)
    异常标准: 偏离SMA超过2个标准差
    """
    if len(prices_with_time) < 3:
        return []
    
    prices = [d["price"] for d in prices_with_time]
    times = [d.get("time", f"t{i}") for i, d in enumerate(prices_with_time)]
    
    anomalies = []
    window = min(5, max(3, len(prices) // 2))
    
    for i in range(window, len(prices)):
        slice_ = prices[i - window:i]
        sma = statistics.mean(slice_)
        std = statistics.stdev(slice_) if len(slice_) > 1 else 0.01
        
        # 标准差接近0时，用均值的5%作为基准偏差（至少0.01）
        if std < 0.001:
            std = max(sma * 0.05, 0.01)
        
        z_score = abs(prices[i] - sma) / std
        if z_score > 2.0:
                anomalies.append({
                    "index": i, "time": times[i], "price": prices[i],
                    "sma": round(sma, 2), "z_score": round(z_score, 2),
                    "direction": "up" if prices[i] > sma else "down"
                })
    
    return anomalies


# ─── L4: 综合杀熟评分 ───

def _composite_score(
    iqr_outliers: list, group_diff: dict, time_anomalies: list,
    price_count: int
) -> dict:
    """加权综合评分: 0-100分，分数越高越可疑。
    
    权重分配:
      - IQR异常: 25分
      - 分组差异: 35分（核心指标）
      - 时间波动: 25分
      - 数据充分度: 15分
    """
    score = 0.0
    
    # IQR异常得分 (max 25)
    if iqr_outliers:
        high_count = sum(1 for o in iqr_outliers if o["severity"] == "high")
        mid_count = sum(1 for o in iqr_outliers if o["severity"] == "medium")
        score += min(25, high_count * 15 + mid_count * 5)
    
    # 分组差异得分 (max 35)
    if group_diff.get("suspicious"):
        diff_pct = group_diff.get("max_diff_pct", 0)
        score += min(35, diff_pct * 1.5)
    
    # 时间异常得分 (max 25)
    if time_anomalies:
        score += min(25, len(time_anomalies) * 8)
    
    # 数据充分度 (max 15)
    score += min(15, price_count * 0.5)
    
    score = round(min(100, score), 1)
    
    if score >= 70:
        level, emoji, advice = "严重可疑", "🔴", "强烈建议截图留证，向12315或平台投诉"
    elif score >= 40:
        level, emoji, advice = "中度可疑", "🟡", "建议继续观察，对比其他平台价格"
    elif score >= 15:
        level, emoji, advice = "轻微可疑", "🟢", "当前数据量有限，建议多收集数据后重新检测"
    else:
        level, emoji, advice = "未检出异常", "🟢", "当前数据未发现明显异常定价"
    
    return {
        "score": score, "level": level, "emoji": emoji, "advice": advice,
        "breakdown": {
            "iqr_score": round(min(25, sum(o["severity"] == "high" for o in iqr_outliers) * 15 + sum(o["severity"] == "medium" for o in iqr_outliers) * 5), 1),
            "group_diff_score": round(min(35, group_diff.get("max_diff_pct", 0) * 1.5), 1),
            "time_score": round(min(25, len(time_anomalies) * 8), 1),
            "data_score": round(min(15, price_count * 0.5), 1)
        }
    }


# ─── 主检测入口 ───

def detect_price_anomaly(
    prices: list[float],
    groups: dict[str, list[float]] | None = None,
    timeseries: list[dict] | None = None
) -> dict[str, Any]:
    """
    价格异常检测主函数。
    
    参数:
        prices: 所有价格列表（必需）
        groups: 按用户类型分组的价格，如 {"新用户":[9.9,10.0], "老用户":[12.0,12.5]}
        timeseries: 带时间戳的价格序列，如 [{"time":"2026-07-28 10:00","price":9.9}, ...]
    
    返回:
        完整审计报告 dict
    """
    if not prices:
        return {"error": "价格数据为空", "suspicious": False}
    
    results: dict[str, Any] = {
        "audit_time": datetime.now().isoformat(),
        "data_summary": {
            "total_records": len(prices),
            "mean": round(statistics.mean(prices), 2),
            "median": round(statistics.median(prices), 2),
            "min": min(prices),
            "max": max(prices),
            "variance": round(statistics.variance(prices), 2) if len(prices) > 1 else 0
        }
    }
    
    # L1: IQR检测
    iqr_result = _iqr_outliers(prices)
    results["iqr_analysis"] = {
        "method": "Tukey's IQR Fences",
        "outliers_count": len(iqr_result),
        "outliers": iqr_result,
        "verdict": f"{'🔴 检测到' if iqr_result else '🟢 未检测到'}统计异常值"
    }
    
    # L2: 分组差异
    if groups:
        group_result = _group_price_diff(groups)
        results["group_analysis"] = group_result
    else:
        results["group_analysis"] = {
            "suspicious": False,
            "verdict": "⚠️ 未提供分组数据，跳过分组差异检测",
            "tip": "提供不同用户类型（新用户/老用户/VIP等）的价格对比，可以更准确检测杀熟"
        }
    
    # L3: 时间序列
    if timeseries:
        time_result = _time_series_anomaly(timeseries)
        results["timeseries_analysis"] = {
            "method": "滑动平均+Z-Score (window=5, threshold=2σ)",
            "anomalies_count": len(time_result),
            "anomalies": time_result,
            "verdict": f"{'🔴 检测到' if time_result else '🟢 未检测到'}时间序列异常"
        }
    else:
        results["timeseries_analysis"] = {
            "anomalies_count": 0,
            "verdict": "⚠️ 未提供时间序列数据，跳过时序检测"
        }
    
    # L4: 综合评分
    composite = _composite_score(
        iqr_result,
        results.get("group_analysis", {}),
        results.get("timeseries_analysis", {}).get("anomalies", []),
        len(prices)
    )
    results["composite_assessment"] = composite
    
    # 最终判定
    results["suspicious"] = composite["score"] >= 40
    results["verdict"] = f"{composite['emoji']} {composite['level']}: 杀熟评分 {composite['score']}/100"
    
    return results


# ─── 快捷方法 ───

def quick_check(prices: list[float]) -> dict:
    """最简调用：只传价格列表即可。"""
    return detect_price_anomaly(prices)


def check_with_groups(prices: list[float], groups: dict[str, list[float]]) -> dict:
    """带分组的价格审计。"""
    return detect_price_anomaly(prices, groups=groups)


def check_full(prices: list[float], groups: dict[str, list[float]],
               timeseries: list[dict]) -> dict:
    """完整审计（价格+分组+时间序列）。"""
    return detect_price_anomaly(prices, groups=groups, timeseries=timeseries)
