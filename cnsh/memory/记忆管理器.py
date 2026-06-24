#龍芯⚡️2026-06-18-CNSH-memory-记忆管理器-v1.0
"""
通心译 | TongXinYi: Memory Manager
龍魂体系·记忆管理器 — 短期记忆与长期记忆分层存储

支持工作记忆、情景记忆、语义记忆三层架构，带遗忘机制和检索增强
Supports working/episodic/semantic memory with forgetting and RAG
"""
# 🟢 君子协议 | JunZi Protocol: CC BY-NC-SA 4.0
# 🟡 AI Truth Protocol: All outputs must be verifiable and traceable
# 🔴 DNA Trace: #龍芯⚡️2026-06-18-CNSH-memory-记忆管理器-v1.0

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import hashlib

__版本__ = "v1.0"
__dna__ = "#龍芯⚡️2026-06-18-CNSH-memory-记忆管理器-v1.0"


class 记忆条目:
    """通心译 | TongXinYi: Memory Entry — 单条记忆记录"""

    def __init__(自身, 内容: str, 记忆类型: str = "情景", 权重: float = 1.0, 标签: list = None):
        自身.唯一ID = hashlib.md5(f"{{内容}}{{datetime.now()}}".encode()).hexdigest()[:12]
        自身.内容 = 内容
        自身.记忆类型 = 记忆类型  # 工作/情景/语义
        自身.权重 = 权重
        自身.标签 = 标签 or []
        自身.创建时间 = datetime.now()
        自身.最后访问 = datetime.now()
        自身.访问次数 = 0
        自身.已遗忘 = False

    def 记忆强度(自身) -> float:
        """🟡 计算当前记忆强度(随时间衰减) | Calculate memory strength"""
        时间差 = (datetime.now() - 自身.创建时间).total_seconds() / 3600  # 小时
        遗忘因子 = 0.9 ** 时间差
        强化因子 = min(自身.访问次数 * 0.1, 2.0)
        return 自身.权重 * 遗忘因子 * (1 + 强化因子)


class 记忆管理器:
    """通心译 | TongXinYi: Memory Manager — 龍魂三层记忆总控"""

    def __init__(自身, 最大记忆数=1000):
        自身.工作记忆 = []   # 🟢 短期、高频率访问
        自身.情景记忆 = []   # 🟡 经验、事件记录
        自身.语义记忆 = []   # 🔴 知识、概念、事实
        自身.最大记忆数 = 最大记忆数
        自身.遗忘阈值 = 0.1
        print(f"[记忆管理器] 🐉 记忆系统已初始化 | 最大: {{最大记忆数}} | {{__dna__}}")

    def 存储(自身, 内容: str, 记忆类型: str = "情景", 权重: float = 1.0, 标签: list = None):
        """🟢 存储新记忆 | Store new memory"""
        条目 = 记忆条目(内容, 记忆类型, 权重, 标签)

        if 记忆类型 == "工作":
            自身.工作记忆.append(条目)
            if len(自身.工作记忆) > 7:  # 🟡 工作记忆上限
                自身._归档到情景(自身.工作记忆.pop(0))
        elif 记忆类型 == "情景":
            自身.情景记忆.append(条目)
        else:
            自身.语义记忆.append(条目)

        自身._检查容量()
        print(f"[记忆管理器] 🟢 记忆已存储 [{{条目.唯一ID}}]: {{内容[:30]}}...")
        return 条目.唯一ID

    def 检索(自身, 查询: str, 记忆类型: str = None, 最大条数: int = 5) -> List[记忆条目]:
        """🟡 检索记忆 | Retrieve memories"""
        print(f"[记忆管理器] 🟡 检索记忆: {{查询}}")

        所有记忆 = []
        if 记忆类型 == "工作" or not 记忆类型:
            所有记忆.extend(自身.工作记忆)
        if 记忆类型 == "情景" or not 记忆类型:
            所有记忆.extend(自身.情景记忆)
        if 记忆类型 == "语义" or not 记忆类型:
            所有记忆.extend(自身.语义记忆)

        # 按相关性和记忆强度排序
        结果 = []
        for 条目 in 所有记忆:
            if 条目.已遗忘:
                continue
            相关性 = 自身._计算相关性(查询, 条目)
            强度 = 条目.记忆强度()
            if 相关性 > 0.3 or 强度 > 0.5:
                结果.append((条目, 相关性 * 强度))
                条目.访问次数 += 1
                条目.最后访问 = datetime.now()

        结果.sort(key=lambda x: x[1], reverse=True)
        print(f"[记忆管理器] 🟢 检索到 {{len(结果)}} 条相关记忆")
        return [条目 for 条目, _ in 结果[:最大条数]]

    def 执行遗忘(自身):
        """🔴 执行遗忘机制 | Run forgetting mechanism"""
        print("[记忆管理器] 🔴 执行遗忘检查...")
        遗忘数 = 0
        for 记忆列表 in [自身.工作记忆, 自身.情景记忆, 自身.语义记忆]:
            for 条目 in 记忆列表:
                if 条目.记忆强度() < 自身.遗忘阈值 and not 条目.已遗忘:
                    条目.已遗忘 = True
                    遗忘数 += 1
        print(f"[记忆管理器] 🔴 已遗忘 {{遗忘数}} 条记忆")

    def 获取统计(自身) -> Dict:
        """🟡 获取记忆统计 | Get memory statistics"""
        return {
            "工作记忆": len(自身.工作记忆),
            "情景记忆": len(自身.情景记忆),
            "语义记忆": len(自身.语义记忆),
            "总计": len(自身.工作记忆) + len(自身.情景记忆) + len(自身.语义记忆),
            "遗忘阈值": 自身.遗忘阈值
        }

    def _归档到情景(自身, 条目: 记忆条目):
        """🔴 将工作记忆归档到情景记忆 | Archive working memory to episodic"""
        条目.记忆类型 = "情景"
        自身.情景记忆.append(条目)
        print(f"[记忆管理器] 🔴 工作记忆归档到情景记忆: {{条目.唯一ID}}")

    def _检查容量(自身):
        """🔴 检查记忆容量 | Check memory capacity"""
        总数 = len(自身.工作记忆) + len(自身.情景记忆) + len(自身.语义记忆)
        if 总数 > 自身.最大记忆数:
            自身.执行遗忘()

    def _计算相关性(自身, 查询: str, 条目: 记忆条目) -> float:
        """🟡 计算查询与记忆的相关性 | Calculate relevance"""
        查询词 = set(查询.lower())
        内容词 = set(条目.内容.lower())
        交集 = 查询词 & 内容词
        并集 = 查询词 | 内容词
        return len(交集) / max(len(并集), 1)


if __name__ == "__main__":
    print("=== 记忆管理器 · 独立执行演示 ===")
    管理器 = 记忆管理器()
    管理器.存储("龍魂CNSH系统初始化完成", "情景", 标签=["系统", "启动"])
    管理器.存储("用户请求分析图像", "工作", 权重=1.5, 标签=["用户", "图像"])
    管理器.存储("图像识别引擎返回结果", "工作", 权重=1.2, 标签=["图像", "结果"])
    结果 = 管理器.检索("图像")
    for 条目 in 结果:
        print(f"  找到: {{条目.内容[:20]}} (强度: {{条目.记忆强度():.3f}})")
    print(f"统计: {{管理器.获取统计()}}")
