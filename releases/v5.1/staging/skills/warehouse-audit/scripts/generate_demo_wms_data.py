#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════════════════
# 龍魂体系 · WMS 演示数据生成器
# DNA: #龍芯⚡️2026-06-16-DEMO-WMS-DATA-v1.0
# ═══════════════════════════════════════════════════════════════════════════════

"""
生成用于仓储AI检查引擎的演示 WMS 数据。

支持格式：
    - JSON 文件（嵌套对象）
    - CSV 文件目录（inventory.csv / orders.csv / operations.csv / warehouse_metrics.csv）
    - SQLite 数据库（wms_metrics.db）

运行后会在指定目录下生成 demo 数据，供 audit_engine.py 的 --wms-data 参数使用。

用法：
    python generate_demo_wms_data.py --output ./demo_wms_data
"""

import argparse
import csv
import json
import os
import sqlite3


# 演示指标：数值设计为“整体良好、局部待优化”，可跑出 60-90 分综合得分
DEMO指标 = {
    "inventory_diff_rate": 0.0008,      # 0.08%，优于 0.1% 目标
    "scan_success_rate": 0.996,          # 99.6%，优于 99.5% 目标
    "daily_orders": 120000,              # 日均 12 万单，优于 10 万目标
    "query_p95_ms": 400,                 # P95 400ms，优于 500ms 目标
    "picking_steps": 2.8,                # 拣货 2.8 步，优于 3 步目标
    "return_cycle_hours": 20,            # 退货 20 小时，优于 24 小时目标
    "batch_trace_ratio": 0.97,           # 批次追溯 97%，优于 95% 目标
    "training_hours": 3.5,               # 培训 3.5 小时，优于 4 小时目标
    "offline_supported": True,           # 支持离线
    "failover_seconds": 45,              # 主备切换 45 秒，优于 60 秒目标
    "fire_safety_score": 94,             # 消防 94 分
    "5s_score": 90,                      # 5S 90 分
}

# 中文别名，用于验证字段名多语言兼容性
DEMO指标中文 = {
    "库存差异率": 0.0008,
    "扫码成功率": 0.996,
    "日均订单量": 120000,
    "查询P95延迟": 400,
    "拣货步数": 2.8,
    "退货处理周期": 20,
    "批次追溯比例": 0.97,
    "培训时长": 3.5,
    "离线支持": True,
    "切换时长": 45,
    "消防安全得分": 94,
    "5S得分": 90,
}


def 生成JSON(输出目录: str) -> str:
    路径 = os.path.join(输出目录, "demo_wms.json")
    with open(路径, "w", encoding="utf-8") as f:
        json.dump(DEMO指标, f, ensure_ascii=False, indent=2)
    return 路径


def 生成CSV目录(输出目录: str) -> str:
    目录 = os.path.join(输出目录, "demo_wms_csv")
    os.makedirs(目录, exist_ok=True)

    # inventory.csv：库存相关指标
    inventory_path = os.path.join(目录, "inventory.csv")
    with open(inventory_path, "w", encoding="utf-8-sig", newline="") as f:
        写入器 = csv.DictWriter(f, fieldnames=["inventory_diff_rate", "batch_trace_ratio"])
        写入器.writeheader()
        写入器.writerow({
            "inventory_diff_rate": DEMO指标["inventory_diff_rate"],
            "batch_trace_ratio": DEMO指标["batch_trace_ratio"]
        })

    # orders.csv：订单相关指标
    orders_path = os.path.join(目录, "orders.csv")
    with open(orders_path, "w", encoding="utf-8-sig", newline="") as f:
        写入器 = csv.DictWriter(f, fieldnames=["daily_orders", "return_cycle_hours"])
        写入器.writeheader()
        写入器.writerow({
            "daily_orders": DEMO指标["daily_orders"],
            "return_cycle_hours": DEMO指标["return_cycle_hours"]
        })

    # operations.csv：作业效率相关指标
    operations_path = os.path.join(目录, "operations.csv")
    with open(operations_path, "w", encoding="utf-8-sig", newline="") as f:
        写入器 = csv.DictWriter(f, fieldnames=["scan_success_rate", "picking_steps", "training_hours", "offline_supported"])
        写入器.writeheader()
        写入器.writerow({
            "scan_success_rate": DEMO指标["scan_success_rate"],
            "picking_steps": DEMO指标["picking_steps"],
            "training_hours": DEMO指标["training_hours"],
            "offline_supported": "是" if DEMO指标["offline_supported"] else "否"
        })

    # warehouse_metrics.csv：性能与合规相关指标
    metrics_path = os.path.join(目录, "warehouse_metrics.csv")
    with open(metrics_path, "w", encoding="utf-8-sig", newline="") as f:
        写入器 = csv.DictWriter(f, fieldnames=["query_p95_ms", "failover_seconds", "fire_safety_score", "5s_score"])
        写入器.writeheader()
        写入器.writerow({
            "query_p95_ms": DEMO指标["query_p95_ms"],
            "failover_seconds": DEMO指标["failover_seconds"],
            "fire_safety_score": DEMO指标["fire_safety_score"],
            "5s_score": DEMO指标["5s_score"]
        })

    return 目录


def 生成SQLite(输出目录: str) -> str:
    路径 = os.path.join(输出目录, "demo_wms.db")
    if os.path.exists(路径):
        os.remove(路径)

    conn = sqlite3.connect(路径)
    try:
        cursor = conn.cursor()
        # 单表多列：列名为指标名
        cursor.execute("""
            CREATE TABLE wms_metrics (
                inventory_diff_rate REAL,
                scan_success_rate REAL,
                daily_orders INTEGER,
                query_p95_ms INTEGER,
                picking_steps REAL,
                return_cycle_hours REAL,
                batch_trace_ratio REAL,
                training_hours REAL,
                offline_supported INTEGER,
                failover_seconds INTEGER,
                fire_safety_score REAL,
                "5s_score" REAL
            )
        """)
        cursor.execute("""
            INSERT INTO wms_metrics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            DEMO指标["inventory_diff_rate"],
            DEMO指标["scan_success_rate"],
            DEMO指标["daily_orders"],
            DEMO指标["query_p95_ms"],
            DEMO指标["picking_steps"],
            DEMO指标["return_cycle_hours"],
            DEMO指标["batch_trace_ratio"],
            DEMO指标["training_hours"],
            1 if DEMO指标["offline_supported"] else 0,
            DEMO指标["failover_seconds"],
            DEMO指标["fire_safety_score"],
            DEMO指标["5s_score"]
        ))

        # 额外创建 key-value 表，用于验证 metric_name/value 读取路径
        cursor.execute("""
            CREATE TABLE wms_metrics_kv (metric_name TEXT, metric_value TEXT)
        """)
        for 键, 值 in DEMO指标中文.items():
            cursor.execute("INSERT INTO wms_metrics_kv VALUES (?, ?)", (键, str(值)))

        conn.commit()
    finally:
        conn.close()
    return 路径


def 生成中文JSON(输出目录: str) -> str:
    路径 = os.path.join(输出目录, "demo_wms_zh.json")
    with open(路径, "w", encoding="utf-8") as f:
        json.dump(DEMO指标中文, f, ensure_ascii=False, indent=2)
    return 路径


def 主函数():
    解析器 = argparse.ArgumentParser(
        description="生成 WMS 演示数据",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python generate_demo_wms_data.py --output ./demo_wms_data
        """
    )
    解析器.add_argument("--output", default="./demo_wms_data", help="演示数据输出目录")
    参数 = 解析器.parse_args()

    os.makedirs(参数.output, exist_ok=True)

    json路径 = 生成JSON(参数.output)
    csv目录 = 生成CSV目录(参数.output)
    sqlite路径 = 生成SQLite(参数.output)
    zh_json路径 = 生成中文JSON(参数.output)

    print(f"✅ 演示数据已生成至: {参数.output}")
    print(f"   - JSON（英文）: {json路径}")
    print(f"   - JSON（中文）: {zh_json路径}")
    print(f"   - CSV 目录:     {csv目录}")
    print(f"   - SQLite:       {sqlite路径}")
    print("\n推荐验证命令：")
    print(f"   python audit_engine.py --system 'Demo仓' --version 'v1.0' --wms-data {json路径} --output ./report")
    print(f"   python audit_engine.py --system 'Demo仓' --version 'v1.0' --wms-data {csv目录} --output ./report")
    print(f"   python audit_engine.py --system 'Demo仓' --version 'v1.0' --wms-data {sqlite路径} --output ./report")
    print(f"   python audit_engine.py --system 'Demo仓' --version 'v1.0' --wms-data {zh_json路径} --output ./report")


if __name__ == "__main__":
    主函数()
