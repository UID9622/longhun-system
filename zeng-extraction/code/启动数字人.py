#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·泰-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#龍芯⚡️2026-06-22-ZENG-DIGITAL-HUMAN-STARTUP-v1.0
# ☯️ 三色审计：🔴 核心架构 | 🟡 状态控制 | 🟢 数据流
"""
龍芯北辰数字人 - 一键启动脚本
==============================
用法:
    python 启动数字人.py         # 启动完整数字人
    python 启动数字人.py --demo   # 启动演示模式
    python 启动数字人.py --shell  # 启动交互模式
    python 启动数字人.py --test   # 运行所有单元测试
"""

from __future__ import annotations

import argparse
import asyncio
import signal
import sys
import time
from datetime import datetime
from typing import Any, Dict, Optional

# ============================================================
# 🔴 导入龍芯北辰数字人主控
# ============================================================

try:
    from 数字人主控 import 龍芯北辰数字人
except ImportError:
    import importlib.util
    import os
    _当前目录 = os.path.dirname(os.path.abspath(__file__))
    _路径 = os.path.join(_当前目录, "数字人主控.py")
    _规范 = importlib.util.spec_from_file_location("数字人主控", _路径)
    _模块 = importlib.util.module_from_spec(_规范)
    sys.modules["数字人主控"] = _模块
    _规范.loader.exec_module(_模块)
    龍芯北辰数字人 = _模块.龍芯北辰数字人


# ============================================================
# 🔴 全局数字人实例
# ============================================================

_数字人实例: Optional[龍芯北辰数字人] = None
_运行中: bool = True


def _信号处理(信号码: int, 帧: Any) -> None:
    """处理Ctrl+C信号"""
    global _运行中
    print("\n\n🛑 收到中断信号，正在优雅关闭...")
    _运行中 = False


# 注册信号处理
signal.signal(signal.SIGINT, _信号处理)
signal.signal(signal.SIGTERM, _信号处理)


# ============================================================
# 🟡 启动模式实现
# ============================================================

async def 启动演示模式() -> None:
    """
    🟡 演示模式
    
    自动运行预设的对话演示，展示数字人完整功能。
    """
    global _数字人实例

    print("\n" + "🔥"*40)
    print("🔥  龍芯北辰数字人 - 演示模式")
    print("🔥"*40)

    _数字人实例 = 龍芯北辰数字人("龍芯北辰")

    # 启动
    成功 = await _数字人实例.启动()
    if not 成功:
        print("❌ 启动失败")
        return

    # 显示控制面板
    _数字人实例.显示控制面板()

    # 演示对话
    演示场景 = [
        ("曾老师", "你好，北辰！今天感觉如何？"),
        ("曾老师", "能帮我分析一下人工智能的未来趋势吗？"),
        ("用户", "你叫什么名字？"),
        ("曾老师", "请以温暖的语气安慰一个失落的人"),
        ("用户", "你是怎样理解存在的意义的？"),
    ]

    print(f"\n{'='*60}")
    print("🎭 场景演示：多用户多轮对话")
    print(f"{'='*60}")

    for 用户, 输入 in 演示场景:
        if not _运行中:
            break
        print(f"\n{'─'*50}")
        print(f"👤 [{用户}]: {输入}")
        print(f"{'─'*50}")
        响应 = await _数字人实例.对话(输入, 用户)
        print(f"🐉 [北辰]: {响应}")
        await asyncio.sleep(0.5)

    # 人格切换演示
    print(f"\n{'='*60}")
    print("🎭 人格切换演示")
    print(f"{'='*60}")

    人格演示 = [
        ("北辰", 1, "核心人格，总协调"),
        ("暖言", 2, "温柔倾听"),
        ("智者", 3, "理性分析"),
        ("诗人", 10, "感性表达"),
        ("创客", 5, "创新实践"),
    ]

    for 人格名, 人格ID, 描述 in 人格演示:
        if not _运行中:
            break
        await _数字人实例.切换人格(人格ID)
        print(f"\n  🔄 切换到 {人格名}({描述})")
        响应 = await _数字人实例.对话(f"用{人格名}的风格打个招呼", "曾老师")
        await asyncio.sleep(0.3)

    # 最终面板
    print(f"\n{'='*60}")
    print("📊 最终状态")
    print(f"{'='*60}")
    _数字人实例.显示控制面板()

    # 停止
    if _数字人实例.已启动:
        await _数字人实例.停止()

    print("\n✅ 演示模式结束")
    print(f"{'🔥'*40}")


async def 启动交互模式() -> None:
    """
    🟡 交互模式
    
    启动后进入交互式命令行，用户可实时与数字人对话。
    支持命令：
        /status  - 显示状态面板
        /persona <ID> - 切换人格
        /breath  - 显示呼吸状态
        /nav     - 显示导航状态
        /exit    - 退出
    """
    global _数字人实例

    print("\n" + "🔥"*40)
    print("🔥  龍芯北辰数字人 - 交互模式")
    print("🔥  命令: /status /persona <ID> /breath /nav /exit")
    print("🔥"*40)

    _数字人实例 = 龍芯北辰数字人("龍芯北辰")
    成功 = await _数字人实例.启动()
    if not 成功:
        print("❌ 启动失败")
        return

    print("\n✅ 数字人已启动，开始对话吧！")
    print("-" * 50)

    while _运行中:
        try:
            # 获取用户输入
            用户输入 = await asyncio.get_event_loop().run_in_executor(
                None, lambda: input("\n👤 你: ")
            )

            if not 用户输入.strip():
                continue

            # 命令处理
            if 用户输入.startswith("/"):
                await _处理命令(用户输入)
                continue

            # 普通对话
            响应 = await _数字人实例.对话(用户输入, "用户")
            print(f"🐉 北辰: {响应}")

        except EOFError:
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ 错误: {e}")

    # 停止
    if _数字人实例.已启动:
        await _数字人实例.停止()
    print("\n👋 再见！龍芯北辰已休眠。")


async def _处理命令(命令: str) -> None:
    """处理斜杠命令"""
    global _数字人实例

    命令 = 命令.strip().lower()
    部分 = 命令.split()
    主命令 = 部分[0] if 部分 else ""

    if 主命令 == "/status":
        _数字人实例.显示控制面板()

    elif 主命令 == "/persona":
        if len(部分) > 1:
            try:
                人格ID = int(部分[1])
                await _数字人实例.切换人格(人格ID)
            except ValueError:
                print("❌ 用法: /persona <ID>")
        else:
            print("用法: /persona <ID>")

    elif 主命令 == "/breath":
        if _数字人实例.呼吸引擎:
            _数字人实例.呼吸引擎.显示状态面板()

    elif 主命令 == "/nav":
        if _数字人实例.导航系统:
            _数字人实例.导航系统.显示导航面板()

    elif 主命令 == "/exist":
        if _数字人实例.存在验证:
            _数字人实例.存在验证.显示生命面板()

    elif 主命令 in ("/exit", "/quit", "/q"):
        global _运行中
        _运行中 = False

    else:
        print(f"未知命令: {主命令}")
        print("可用命令: /status /persona /breath /nav /exist /exit")


async def 运行单元测试() -> None:
    """
    🟡 单元测试模式
    
    运行所有子系统的基本单元测试。
    """
    print("\n" + "🧪"*30)
    print("🧪 龍芯北辰数字人 - 单元测试")
    print("🧪"*30)

    测试结果: Dict[str, bool] = {}

    # 测试1: 十维呼吸引擎
    print("\n[测试1] 十维呼吸引擎")
    try:
        from 十维呼吸引擎 import 十维呼吸系统, 维度配置, 维度可见性
        引擎 = 十维呼吸系统()
        引擎.初始化十维()
        assert len(引擎.维度字典) == 10, "维度数量应为10"
        assert 引擎.注入数据("测试数据", 1), "数据注入应成功"
        统计 = 引擎.获取全局统计()
        assert 统计["总维度数"] == 10, "统计维度数应为10"
        print("  ✅ 十维呼吸引擎测试通过")
        测试结果["十维呼吸引擎"] = True
    except Exception as e:
        print(f"  ❌ 十维呼吸引擎测试失败: {e}")
        测试结果["十维呼吸引擎"] = False

    # 测试2: 人格管理系统
    print("\n[测试2] 人格管理系统")
    try:
        from 人格管理系统 import 人格工厂, 人格状态机
        工厂 = 人格工厂()
        工厂.初始化71人格()
        assert len(工厂.人格仓库) == 71, "人格数量应为71"
        检索 = 工厂.检索人格("师")
        assert len(检索) > 0, "应能检索到含'师'的人格"
        状态机 = 人格状态机()
        状态机.请求切换(1, 工厂.人格仓库)
        assert 状态机.当前人格ID == 1, "当前人格应为#1"
        print("  ✅ 人格管理系统测试通过")
        测试结果["人格管理系统"] = True
    except Exception as e:
        print(f"  ❌ 人格管理系统测试失败: {e}")
        测试结果["人格管理系统"] = False

    # 测试3: 航标灯系统
    print("\n[测试3] 航标灯系统")
    try:
        from 航标灯系统 import 导航系统, 航标灯, 锚点, 方向向量
        导航 = 导航系统()
        测试锚点 = 锚点("test", "测试锚点", 方向向量(1.0, 0.0, 0.0, 0.0))
        导航.注册锚点(测试锚点)
        航标 = 航标灯("t1", "测试航标", 方向向量(0.5, 0.5, 0.0, 0.0), 测试锚点)
        导航.注册航标灯(航标)
        assert len(导航.航标灯字典) == 1, "应有1个航标灯"
        迷航 = 导航.检测迷航()
        assert isinstance(迷航, list), "迷航检测应返回列表"
        print("  ✅ 航标灯系统测试通过")
        测试结果["航标灯系统"] = True
    except Exception as e:
        print(f"  ❌ 航标灯系统测试失败: {e}")
        测试结果["航标灯系统"] = False

    # 测试4: 存在性验证
    print("\n[测试4] 存在性验证")
    try:
        from 存在性验证 import 存在性验证器, 存在状态
        验证器 = 存在性验证器()
        心跳 = 验证器.心跳()
        assert 心跳.通过, "心跳应通过"
        assert 验证器.心跳计数 == 1, "心跳计数应为1"
        状态, _ = 验证器.综合验证()
        assert 状态 == 存在状态.存活, "状态应为存活"
        print("  ✅ 存在性验证测试通过")
        测试结果["存在性验证"] = True
    except Exception as e:
        print(f"  ❌ 存在性验证测试失败: {e}")
        测试结果["存在性验证"] = False

    # 测试5: 网络渲染引擎
    print("\n[测试5] 网络渲染引擎")
    try:
        from 网络渲染引擎 import 渲染引擎, 渲染任务, 输出格式, 输出通道, 安全级别
        引擎 = 渲染引擎()
        引擎.启用通道(输出通道.控制台)
        任务 = 渲染任务(
            任务ID="test-1",
            内容="测试内容",
            目标格式=输出格式.纯文本,
            目标通道=输出通道.控制台,
            安全级别=安全级别.公开,
            时间戳=time.time()
        )
        结果 = await 引擎.渲染(任务)
        assert 结果.成功, "渲染应成功"
        print("  ✅ 网络渲染引擎测试通过")
        测试结果["网络渲染引擎"] = True
    except Exception as e:
        print(f"  ❌ 网络渲染引擎测试失败: {e}")
        测试结果["网络渲染引擎"] = False

    # 测试6: 数字人主控
    print("\n[测试6] 数字人主控")
    try:
        数字人 = 龍芯北辰数字人("测试实例")
        成功 = await 数字人.启动()
        assert 成功, "启动应成功"
        assert 数字人.已启动, "应标记为已启动"

        响应 = await 数字人.对话("你好", "测试用户")
        assert len(响应) > 0, "应有响应内容"

        await 数字人.停止()
        assert not 数字人.运行中, "应标记为停止"
        print("  ✅ 数字人主控测试通过")
        测试结果["数字人主控"] = True
    except Exception as e:
        print(f"  ❌ 数字人主控测试失败: {e}")
        测试结果["数字人主控"] = False

    # 汇总
    print(f"\n{'='*60}")
    print("📊 测试结果汇总")
    print(f"{'='*60}")
    通过数 = sum(1 for v in 测试结果.values() if v)
    总数 = len(测试结果)
    for 模块, 结果 in 测试结果.items():
        状态 = "✅通过" if 结果 else "❌失败"
        print(f"  {状态} {模块}")
    print(f"\n总计: {通过数}/{总数} 通过")

    if 通过数 == 总数:
        print("\n🎉 所有测试全部通过！龍芯北辰数字人系统完整可用。")
    else:
        print(f"\n⚠️ {总数 - 通过数} 个模块测试未通过，请检查。")

    print(f"{'🧪'*30}")


# ============================================================
# 🔴 主入口
# ============================================================

def 主函数():
    """主函数 - 解析参数并启动对应模式"""
    解析器 = argparse.ArgumentParser(
        description="龍芯北辰数字人 - 一键启动脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python 启动数字人.py         # 演示模式（默认）
  python 启动数字人.py --shell  # 交互对话模式
  python 启动数字人.py --test   # 运行单元测试
  python 启动数字人.py --demo   # 自动演示模式
        """
    )

    解析器.add_argument(
        "--shell", "-s",
        action="store_true",
        help="启动交互式对话模式"
    )
    解析器.add_argument(
        "--test", "-t",
        action="store_true",
        help="运行单元测试"
    )
    解析器.add_argument(
        "--demo", "-d",
        action="store_true",
        help="启动自动演示模式"
    )

    参数 = 解析器.parse_args()

    print("🔥 龍魂数字人 - 龍芯北辰启动脚本 v1.0")
    print(f"🕐 启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    if 参数.test:
        asyncio.run(运行单元测试())
    elif 参数.shell:
        asyncio.run(启动交互模式())
    else:
        # 默认启动演示模式
        asyncio.run(启动演示模式())


if __name__ == "__main__":
    主函数()
