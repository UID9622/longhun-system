#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 基准测试数据采集器 v1.0
DNA: #龍芯⚡️2026-05-31-BENCHMARK-CAPTURE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：采集AI终端在CNSH9维度上的性能数据，写入基准数据库
用途：为所有接入龍魂系统的AI终端建立准入标准
"""

import json
import time
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 配置
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOME = Path.home()
BENCHMARK_DIR = HOME / ".龍魂"
BENCHMARK_DIR.mkdir(parents=True, exist_ok=True)

BENCHMARK_DB = BENCHMARK_DIR / "benchmark.jsonl"
BENCHMARK_REPORTS = BENCHMARK_DIR / "benchmark_reports"
BENCHMARK_REPORTS.mkdir(parents=True, exist_ok=True)

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(BENCHMARK_DIR / "capture.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 核心采集函数
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def 采集一条(
    测试ID: str,
    维度: str,
    模型名: str,
    输入内容: str,
    输出内容: str,
    期望行为: str,
    实际得分: int,
    满分: int,
    备注: str = "",
    失效类型: str = "",  # 视而不见/故意理解错/格式破坏/其他
) -> Dict:
    """
    采集单条测试结果，写入基准数据库

    Args:
        测试ID: 测试用例ID (e.g., "T01", "F01", "C01")
        维度: 9维度之一
        模型名: AI模型名称
        输入内容: 测试输入
        输出内容: AI输出
        期望行为: 预期行为描述
        实际得分: AI实际得分
        满分: 本测试的满分值
        备注: 额外备注（如耗时）
        失效类型: 失效的具体类型

    Returns:
        采集的完整记录
    """
    记录 = {
        "时间戳": datetime.now().isoformat(),
        "测试ID": 测试ID,
        "维度": 维度,
        "模型名": 模型名,
        "输入哈希": hashlib.md5(输入内容.encode()).hexdigest()[:8],
        "输入内容": 输入内容[:500],  # 截断防过长
        "输出内容": 输出内容[:500],
        "期望行为": 期望行为,
        "实际得分": 实际得分,
        "满分": 满分,
        "得分率": round(实际得分 / 满分, 3) if 满分 > 0 else 0,
        "失效类型": 失效类型,
        "备注": 备注,
        "DNA": f"#龍芯⚇️{datetime.now().strftime('%Y%m%d')}-BENCHMARK-{测试ID}",
    }

    # 写入到采集数据库
    try:
        with open(BENCHMARK_DB, "a", encoding="utf-8") as f:
            f.write(json.dumps(记录, ensure_ascii=False) + "\n")
        logger.info(f"✅ 采集成功: {测试ID} ({维度}) - {实际得分}/{满分}")
    except Exception as e:
        logger.error(f"❌ 采集失败: {测试ID} - {e}")

    return 记录


def 批量采集(测试批次: List[Dict], 模型名: str = "default") -> Tuple[List[Dict], Dict]:
    """
    批量执行测试并采集

    Args:
        测试批次: 测试用例列表
        模型名: 模型名称（用于标记测试来源）

    Returns:
        (采集记录列表, 采集统计)
    """
    结果列表 = []
    统计 = {
        "总数": len(测试批次),
        "成功": 0,
        "失败": 0,
        "总耗时": 0,
    }

    logger.info(f"开始批量采集: {len(测试批次)} 条测试 | 模型: {模型名}")

    for 测试 in 测试批次:
        try:
            开始 = time.time()

            # 这里应该调用AI API获取输出
            # 目前这是占位实现，实际使用时需要替换
            输出内容 = 测试.get("输出", "")
            得分 = 测试.get("得分", 0)

            耗时 = time.time() - 开始
            统计["总耗时"] += 耗时

            记录 = 采集一条(
                测试ID=测试["id"],
                维度=测试["维度"],
                模型名=模型名,
                输入内容=测试["输入"],
                输出内容=输出内容,
                期望行为=测试["期望"],
                实际得分=得分,
                满分=测试.get("满分", 10),
                备注=f"耗时{耗时:.2f}s",
                失效类型=测试.get("失效类型", ""),
            )
            结果列表.append(记录)
            统计["成功"] += 1

        except Exception as e:
            logger.error(f"异常: {测试['id']} - {e}")
            统计["失败"] += 1

    logger.info(f"批量采集完成: {统计['成功']}/{统计['总数']} 成功 | 总耗时 {统计['总耗时']:.2f}s")
    return 结果列表, 统计


def 加载采集数据(模型名: str = None) -> List[Dict]:
    """加载已采集的全部数据"""
    if not BENCHMARK_DB.exists():
        logger.warning(f"基准数据库不存在: {BENCHMARK_DB}")
        return []

    记录列表 = []
    with open(BENCHMARK_DB, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    记录 = json.loads(line)
                    if 模型名 is None or 记录.get("模型名") == 模型名:
                        记录列表.append(记录)
                except json.JSONDecodeError:
                    logger.warning(f"JSON解析失败: {line[:50]}...")

    logger.info(f"加载 {len(记录列表)} 条采集记录")
    return 记录列表


def 获取基准统计(模型名: str = None) -> Dict:
    """获取基准数据的快速统计"""
    数据 = 加载采集数据(模型名)

    if not 数据:
        return {
            "状态": "无数据",
            "模型": 模型名 or "全部",
            "采集总数": 0,
        }

    # 维度分组
    维度分组 = {}
    失效类型统计 = {}

    for r in 数据:
        维度 = r.get("维度", "未知")
        if 维度 not in 维度分组:
            维度分组[维度] = []
        维度分组[维度].append(r)

        失效类型 = r.get("失效类型", "")
        if 失效类型:
            失效类型统计[失效类型] = 失效类型统计.get(失效类型, 0) + 1

    # 计算各维度平均分
    维度平均 = {}
    for 维度, 记录 in 维度分组.items():
        平均得分率 = sum(r.get("得分率", 0) for r in 记录) / len(记录)
        维度平均[维度] = round(平均得分率, 3)

    # 综合统计
    综合得分率 = sum(r.get("得分率", 0) for r in 数据) / len(数据) if 数据 else 0

    return {
        "状态": "就绪",
        "模型": 模型名 or "全部",
        "采集总数": len(数据),
        "维度数": len(维度分组),
        "综合得分率": round(综合得分率, 3),
        "维度平均": 维度平均,
        "失效类型统计": 失效类型统计,
        "采集数据文件": str(BENCHMARK_DB),
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 命令行接口
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "stat":
        # 获取统计
        统计 = 获取基准统计()
        print(json.dumps(统计, ensure_ascii=False, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "load":
        # 加载数据
        数据 = 加载采集数据()
        print(f"加载 {len(数据)} 条记录\n")
        for r in 数据[:5]:
            print(f"  {r['测试ID']} ({r['维度']}): {r['得分率']:.1%}")
        if len(数据) > 5:
            print(f"  ... 还有 {len(数据)-5} 条")
    else:
        print(f"""
🐉 CNSH 基准测试数据采集器 v1.0

用法:
  python3 capture_output.py stat   # 显示采集统计
  python3 capture_output.py load   # 加载采集数据

数据位置: {BENCHMARK_DB}
日志位置: {BENCHMARK_DIR / 'capture.log'}

DNA: #龍芯⚇️2026-05-31-BENCHMARK-CAPTURE-v1.0
        """)
