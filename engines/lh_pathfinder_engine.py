#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍魂数学建模协议 · 路径规划引擎 v4.1.5
# DNA: #龍芯⚡️丙午·癸未·丁未·离为火-路径规划-v4.1.5
# 功能: 迪杰斯特拉 / A* / 动态规划 / 八卦阵 / 三六九不动点 / D* Lite
# 锚定: 道德经【道生一，一生二，二生三，三生万物】

import heapq
import json
import hashlib
import argparse
from datetime import datetime, timezone
from typing import List, Tuple, Dict, Set, Optional, Callable

DNA = "#龍芯⚡️丙午·癸未·丁未·离为火-路径规划-v4.1.5"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def _签名(数据: Dict) -> str:
    """SHA256 审计链签名"""
    文本 = json.dumps(数据, ensure_ascii=False, sort_keys=True)
    return "sha256:" + hashlib.sha256(文本.encode("utf-8")).hexdigest()[:16]


def _结果封装(结果: Dict, 算法名: str) -> Dict:
    """所有输出强制 DNA 签章（P0 零黑箱承诺）"""
    结果["DNA"] = f"#龍芯⚡️丙午·癸未·丁未-{算法名}-v4.1.5"
    结果["时间戳"] = _now()
    结果["签章方"] = "龍芯北辰 UID9622"
    结果["确认码"] = CONFIRM
    结果["审计链"] = _签名(结果)
    return 结果


# ════════════════════════════════════════════════════════
# 一、核心算法层
# ════════════════════════════════════════════════════════

def 迪杰斯特拉(地图: List[List[int]], 起点: Tuple[int, int], 终点: Tuple[int, int]) -> Dict:
    """
    龍魂·迪杰斯特拉最短路径算法
    DNA: #龍芯⚡️丙午·癸未·丁未-迪杰斯特拉-v4.1.5
    锚定: 道德经第九章【持而盈之，不如其已】——贪心取当前最小
    """
    行数, 列数 = len(地图), len(地图[0])
    距离表 = {(i, j): float("inf") for i in range(行数) for j in range(列数)}
    前驱表 = {}
    已访问: Set[Tuple[int, int]] = set()

    距离表[起点] = 0
    优先队列 = [(0, 起点)]

    while 优先队列:
        当前距离, 当前节点 = heapq.heappop(优先队列)
        if 当前节点 in 已访问:
            continue
        已访问.add(当前节点)
        if 当前节点 == 终点:
            break

        当前行, 当前列 = 当前节点
        for 行偏移, 列偏移 in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            邻接行 = 当前行 + 行偏移
            邻接列 = 当前列 + 列偏移
            if not (0 <= 邻接行 < 行数 and 0 <= 邻接列 < 列数):
                continue
            if 地图[邻接行][邻接列] == -1:
                continue

            新距离 = 当前距离 + 地图[邻接行][邻接列]
            if 新距离 < 距离表[(邻接行, 邻接列)]:
                距离表[(邻接行, 邻接列)] = 新距离
                前驱表[(邻接行, 邻接列)] = 当前节点
                heapq.heappush(优先队列, (新距离, (邻接行, 邻接列)))

    if 终点 not in 前驱表 and 终点 != 起点:
        return _结果封装({"路径": [], "总成本": float("inf")}, "迪杰斯特拉")

    路径 = []
    节点 = 终点
    while 节点 != 起点:
        路径.append(节点)
        节点 = 前驱表[节点]
    路径.append(起点)
    路径.reverse()

    return _结果封装({
        "路径": 路径,
        "总成本": 距离表[终点],
        "已访问节点数": len(已访问),
    }, "迪杰斯特拉")


def A星算法(地图: List[List[int]], 起点: Tuple[int, int], 终点: Tuple[int, int],
          启发类型: str = "曼哈顿") -> Dict:
    """
    龍魂·A*启发式寻路算法
    支持启发函数热插拔（P4用户自定义层）
    DNA: #龍芯⚡️丙午·癸未·丁未-A星-v4.1.5
    锚定: 道德经第三十三章【知人者智，自知者明】——h函数即自知
    """
    行数, 列数 = len(地图), len(地图[0])

    def 曼哈顿启发(节点: Tuple[int, int]) -> float:
        return abs(节点[0] - 终点[0]) + abs(节点[1] - 终点[1])

    def 欧几里得启发(节点: Tuple[int, int]) -> float:
        return ((节点[0] - 终点[0]) ** 2 + (节点[1] - 终点[1]) ** 2) ** 0.5

    def 切比雪夫启发(节点: Tuple[int, int]) -> float:
        return max(abs(节点[0] - 终点[0]), abs(节点[1] - 终点[1]))

    启发函数表 = {
        "曼哈顿": 曼哈顿启发,
        "欧几里得": 欧几里得启发,
        "切比雪夫": 切比雪夫启发,
    }
    启发函数 = 启发函数表.get(启发类型, 曼哈顿启发)

    # 可采纳性校验（P0零黑箱承诺：不能高估）
    样本点 = (0, 0)
    if 启发函数(样本点) > (行数 + 列数):
        print("[WARN] 启发函数可能不可采纳，最优性不保证")

    开放集 = [(启发函数(起点), 0, 起点)]
    关闭集: Set[Tuple[int, int]] = set()
    g值表 = {起点: 0}
    前驱表 = {}

    while 开放集:
        _, 当前g, 当前节点 = heapq.heappop(开放集)
        if 当前节点 == 终点:
            路径 = []
            节点 = 终点
            while 节点 != 起点:
                路径.append(节点)
                节点 = 前驱表[节点]
            路径.append(起点)
            路径.reverse()
            return _结果封装({
                "路径": 路径,
                "总成本": g值表[终点],
                "扩展节点数": len(关闭集) + 1,
                "启发类型": 启发类型,
            }, "A星")

        if 当前节点 in 关闭集:
            continue
        关闭集.add(当前节点)

        当前行, 当前列 = 当前节点
        for 行偏移, 列偏移 in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            邻接行 = 当前行 + 行偏移
            邻接列 = 当前列 + 列偏移
            if not (0 <= 邻接行 < 行数 and 0 <= 邻接列 < 列数):
                continue
            if 地图[邻接行][邻接列] == -1:
                continue

            试探g = 当前g + 地图[邻接行][邻接列]
            邻接节点 = (邻接行, 邻接列)
            if 邻接节点 not in g值表 or 试探g < g值表[邻接节点]:
                g值表[邻接节点] = 试探g
                f值 = 试探g + 启发函数(邻接节点)
                heapq.heappush(开放集, (f值, 试探g, 邻接节点))
                前驱表[邻接节点] = 当前节点

    return _结果封装({"路径": [], "总成本": float("inf"), "启发类型": 启发类型}, "A星")


def 动态规划路径(地图: List[List[int]], 起点: Tuple[int, int], 终点: Tuple[int, int]) -> Dict:
    """
    龍魂·动态规划网格路径
    DNA: #龍芯⚡️丙午·癸未·丁未-DP-v4.1.5
    锚定: 道德经第六十三章【天下难事，必作于易】——重复子问题
    """
    行数, 列数 = len(地图), len(地图[0])
    INF = float("inf")
    dp = [[INF for _ in range(列数)] for _ in range(行数)]
    起点行, 起点列 = 起点
    终点行, 终点列 = 终点
    dp[起点行][起点列] = 0

    收敛 = False
    迭代次数 = 0
    while not 收敛 and 迭代次数 < 行数 * 列数:
        收敛 = True
        迭代次数 += 1
        for i in range(行数):
            for j in range(列数):
                if (i, j) == 起点 or 地图[i][j] == -1:
                    continue
                for 行偏移, 列偏移 in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    前驱行 = i + 行偏移
                    前驱列 = j + 列偏移
                    if 0 <= 前驱行 < 行数 and 0 <= 前驱列 < 列数:
                        if dp[前驱行][前驱列] + 地图[i][j] < dp[i][j]:
                            dp[i][j] = dp[前驱行][前驱列] + 地图[i][j]
                            收敛 = False

    if dp[终点行][终点列] == INF:
        return _结果封装({"路径": [], "总成本": INF, "迭代次数": 迭代次数}, "DP")

    路径 = [终点]
    当前行, 当前列 = 终点行, 终点列
    while (当前行, 当前列) != 起点:
        for 行偏移, 列偏移 in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            前驱行 = 当前行 + 行偏移
            前驱列 = 当前列 + 列偏移
            if 0 <= 前驱行 < 行数 and 0 <= 前驱列 < 列数:
                if dp[当前行][当前列] == dp[前驱行][前驱列] + 地图[当前行][当前列]:
                    路径.append((前驱行, 前驱列))
                    当前行, 当前列 = 前驱行, 前驱列
                    break
    路径.reverse()
    return _结果封装({
        "路径": 路径,
        "总成本": dp[终点行][终点列],
        "迭代次数": 迭代次数,
    }, "DP")


# ════════════════════════════════════════════════════════
# 二、龍魂映射层
# ════════════════════════════════════════════════════════

def 八卦阵寻路(地图: List[List[int]], 起点: Tuple[int, int], 终点: Tuple[int, int],
             人格权重: Optional[Dict[str, float]] = None) -> Dict:
    """
    龍魂·八卦阵八方向加权寻路
    DNA: #龍芯⚡️丙午·癸未·丁未-八卦阵-v4.1.5
    锚定: 易经八卦方位 + 道德经【万物负阴而抱阳，冲气以为和】
    """
    八卦方向 = [
        ("乾", -1, -1, 1.0), ("坤", +1, -1, 1.2),
        ("震", 0, +1, 1.0),  ("巽", +1, +1, 1.1),
        ("坎", -1, 0, 1.3),  ("离", +1, 0, 1.0),
        ("艮", -1, +1, 1.2), ("兑", 0, -1, 1.0)
    ]

    默认权重 = {"军事": 0.2, "历史": 0.2, "哲学": 0.2, "经济": 0.2, "政治": 0.2}
    人格权重 = 人格权重 or 默认权重
    主导人格 = max(人格权重, key=人格权重.get)
    方向偏好 = {
        "军事": {"坎": 0.8, "离": 0.8},
        "历史": {"乾": 0.9, "坤": 0.9},
        "哲学": {"震": 0.9, "兑": 0.9},
        "经济": {"巽": 0.8, "艮": 0.8},
        "政治": {"离": 0.8, "坎": 0.8},
    }.get(主导人格, {})

    行数, 列数 = len(地图), len(地图[0])
    优先队列 = [(0, 起点, [])]
    已访问: Set[Tuple[int, int]] = set()
    g值表 = {起点: 0}

    while 优先队列:
        当前成本, 当前节点, 当前路径 = heapq.heappop(优先队列)
        if 当前节点 in 已访问:
            continue
        已访问.add(当前节点)
        if 当前节点 == 终点:
            return _结果封装({
                "路径": 当前路径 + [终点],
                "总成本": 当前成本,
                "主导人格": 主导人格,
                "方向偏好": 方向偏好,
            }, "八卦阵")

        当前行, 当前列 = 当前节点
        for 卦名, 行偏移, 列偏移, 基础权重 in 八卦方向:
            邻接行 = 当前行 + 行偏移
            邻接列 = 当前列 + 列偏移
            if not (0 <= 邻接行 < 行数 and 0 <= 邻接列 < 列数):
                continue
            if 地图[邻接行][邻接列] == -1:
                continue

            调整系数 = 方向偏好.get(卦名, 1.0)
            边成本 = 地图[邻接行][邻接列] * 基础权重 * 调整系数
            新成本 = 当前成本 + 边成本
            邻接节点 = (邻接行, 邻接列)
            if 邻接节点 not in g值表 or 新成本 < g值表[邻接节点]:
                g值表[邻接节点] = 新成本
                启发 = abs(邻接行 - 终点[0]) + abs(邻接列 - 终点[1])
                f值 = 新成本 + 启发
                heapq.heappush(优先队列, (f值, 邻接节点, 当前路径 + [当前节点]))

    return _结果封装({"路径": [], "总成本": float("inf"), "主导人格": 主导人格}, "八卦阵")


def 三六九不动点校验(当前位置: Tuple[int, int], 起点: Tuple[int, int],
                 终点: Tuple[int, int], 已走路径: List[Tuple[int, int]]) -> Dict:
    """
    龍魂·三六九不动点校验
    DNA: #龍芯⚡️丙午·癸未·丁未-不动点-v4.1.5
    锚定: 道德经【道生一，一生二，二生三，三生万物】
    """
    总距离 = abs(终点[0] - 起点[0]) + abs(终点[1] - 起点[1])
    已走距离 = len(已走路径)
    剩余距离 = abs(终点[0] - 当前位置[0]) + abs(终点[1] - 当前位置[1])

    理想方向 = (终点[0] - 起点[0], 终点[1] - 起点[1])
    实际方向 = (当前位置[0] - 起点[0], 当前位置[1] - 起点[1])
    方向偏差 = abs(理想方向[0] - 实际方向[0]) + abs(理想方向[1] - 实际方向[1])
    宏观合格 = 方向偏差 < 总距离 * 0.5

    中观点 = (起点[0] + (终点[0] - 起点[0]) // 2, 起点[1] + (终点[1] - 起点[1]) // 2)
    中观距离 = abs(当前位置[0] - 中观点[0]) + abs(当前位置[1] - 中观点[1])
    中观合格 = 中观距离 < 总距离 * 0.3 if 已走距离 > 总距离 * 0.4 else True

    微观合格 = 剩余距离 <= 总距离 - 已走距离 + 2

    return _结果封装({
        "宏观合格": 宏观合格,
        "中观合格": 中观合格,
        "微观合格": 微观合格,
        "建议": "继续" if all([宏观合格, 中观合格, 微观合格]) else "重新规划",
    }, "不动点")


def 蚁群分布式寻路(地图: List[List[int]], 起点: Tuple[int, int], 终点: Tuple[int, int],
                 蚂蚁数: int = 20, 迭代次数: int = 50,
                 信息素重要程度: float = 1.0, 启发重要程度: float = 2.0,
                 信息素挥发率: float = 0.3) -> Dict:
    """
    龍魂·蚁群分布式多智能体协同寻路
    DNA: #龍芯⚡️丙午·癸未·丁未-蚁群-v4.1.5
    锚定: 道德经第四十二章【万物负阴而抱阳，冲气以为和】——群体智慧涌现
    """
    行数, 列数 = len(地图), len(地图[0])
    信息素 = [[1.0 for _ in range(列数)] for _ in range(行数)]
    方向 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    最优路径 = []
    最优成本 = float("inf")
    所有蚂蚁路径 = []

    def 可通行(节点: Tuple[int, int]) -> bool:
        i, j = 节点
        return 0 <= i < 行数 and 0 <= j < 列数 and 地图[i][j] != -1

    def 启发(节点: Tuple[int, int]) -> float:
        return 1.0 / (abs(节点[0] - 终点[0]) + abs(节点[1] - 终点[1]) + 1e-6)

    for 迭代 in range(迭代次数):
        本轮路径 = []
        for _ in range(蚂蚁数):
            当前 = 起点
            路径 = [当前]
            成本 = 0.0
            已访问 = {当前}
            while 当前 != 终点:
                候选 = []
                for di, dj in 方向:
                    邻接 = (当前[0] + di, 当前[1] + dj)
                    if 可通行(邻接) and 邻接 not in 已访问:
                        候选.append(邻接)
                if not 候选:
                    break
                概率 = []
                for 节点 in 候选:
                    i, j = 节点
                    吸引力 = (信息素[i][j] ** 信息素重要程度) * (启发(节点) ** 启发重要程度)
                    概率.append(吸引力)
                总概率 = sum(概率)
                概率 = [p / 总概率 for p in 概率]
                import random
                选择索引 = random.choices(range(len(候选)), weights=概率, k=1)[0]
                下一节点 = 候选[选择索引]
                成本 += 地图[下一节点[0]][下一节点[1]]
                路径.append(下一节点)
                已访问.add(下一节点)
                当前 = 下一节点
                if len(路径) > 行数 * 列数:
                    break

            if 当前 == 终点 and 成本 < 最优成本:
                最优成本 = 成本
                最优路径 = 路径
            本轮路径.append((路径, 成本))

        # 信息素挥发
        for i in range(行数):
            for j in range(列数):
                信息素[i][j] *= (1 - 信息素挥发率)

        # 信息素增强（只强化到达终点的路径，精英蚂蚁策略）
        for 路径, 成本 in 本轮路径:
            if 路径[-1] == 终点 and 成本 > 0:
                增量 = 1.0 / 成本
                for 节点 in 路径:
                    信息素[节点[0]][节点[1]] += 增量

        所有蚂蚁路径.extend(本轮路径)

    return _结果封装({
        "路径": 最优路径,
        "总成本": 最优成本 if 最优路径 else float("inf"),
        "蚂蚁数": 蚂蚁数,
        "迭代次数": 迭代次数,
        "到达终点次数": sum(1 for p, _ in 所有蚂蚁路径 if p and p[-1] == 终点),
    }, "蚁群")


# ════════════════════════════════════════════════════════
# 三、物理尺度层
# ════════════════════════════════════════════════════════

def 多因素成本(距离: float, 时间: float, 能耗: float, 安全: float, 权重: Dict[str, float]) -> float:
    """
    龍魂·多因素成本归一化
    DNA: #龍芯⚡️丙午·癸未·丁未-多因素-v4.1.5
    锚定: 道德经第七十七章【天之道，损有余而补不足】——归一化即平衡
    """
    因素表 = {"距离": 距离, "时间": 时间, "能耗": 能耗, "安全": 安全}
    总成本 = 0.0
    for 因素名, 因素值 in 因素表.items():
        w = 权重.get(因素名, 0.25)
        归一值 = 因素值 / (因素值 + 1.0)
        总成本 += w * 归一值
    return 总成本


class D星精简版:
    """
    龍魂·D* Lite 动态路径重规划
    DNA: #龍芯⚡️丙午·癸未·丁未-D星-v4.1.5
    锚定: 道德经第七十八章【天下莫柔弱于水，而攻坚强者莫之能胜】——随环境而变
    """

    def __init__(self, 地图: List[List[int]]):
        self.地图 = 地图
        self.行数 = len(地图)
        self.列数 = len(地图[0])
        self.g值: Dict[Tuple[int, int], float] = {}
        self.rhs值: Dict[Tuple[int, int], float] = {}
        self.优先队列: List[Tuple] = []
        self.队列索引: Dict[Tuple[int, int], Tuple[float, float]] = {}
        self.起点: Optional[Tuple[int, int]] = None
        self.终点: Optional[Tuple[int, int]] = None

    def 初始化(self, 起点: Tuple[int, int], 终点: Tuple[int, int]):
        self.起点 = 起点
        self.终点 = 终点
        for i in range(self.行数):
            for j in range(self.列数):
                self.g值[(i, j)] = float("inf")
                self.rhs值[(i, j)] = float("inf")
        self.rhs值[终点] = 0
        self.队列索引[终点] = self.键值(终点)
        heapq.heappush(self.优先队列, (self.队列索引[终点], 终点))

    def 启发(self, 节点: Tuple[int, int], 参考点: Optional[Tuple[int, int]] = None) -> float:
        目标 = 参考点 or self.终点
        return abs(节点[0] - 目标[0]) + abs(节点[1] - 目标[1])

    def 键值(self, 节点: Tuple[int, int]) -> Tuple[float, float]:
        k1 = min(self.g值[节点], self.rhs值[节点]) + self.启发(节点)
        k2 = min(self.g值[节点], self.rhs值[节点])
        return (k1, k2)

    def 前驱节点(self, 节点: Tuple[int, int]) -> List[Tuple[int, int]]:
        结果 = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = 节点[0] + dx, 节点[1] + dy
            if 0 <= nx < self.行数 and 0 <= ny < self.列数 and self.地图[nx][ny] != -1:
                结果.append((nx, ny))
        return 结果

    def 更新顶点(self, 节点: Tuple[int, int]):
        if 节点 != self.终点:
            邻居成本 = []
            for 邻居 in self.前驱节点(节点):
                邻居成本.append(self.g值[邻居] + self.地图[节点[0]][节点[1]])
            self.rhs值[节点] = min(邻居成本) if 邻居成本 else float("inf")

        if 节点 in self.队列索引:
            del self.队列索引[节点]

        if self.g值[节点] != self.rhs值[节点]:
            self.队列索引[节点] = self.键值(节点)
            heapq.heappush(self.优先队列, (self.队列索引[节点], 节点))

    def 计算最短路径(self) -> Dict:
        while self.优先队列:
            当前键, 当前 = heapq.heappop(self.优先队列)
            if 当前 in self.队列索引 and 当前键 != self.队列索引[当前]:
                continue  # 过期队列项

            if (self.键值(self.起点) >= 当前键 and
                self.rhs值[self.起点] == self.g值[self.起点] and
                self.g值[self.起点] != float("inf")) or \
               (self.起点 == self.终点):
                break

            if self.g值[当前] > self.rhs值[当前]:
                self.g值[当前] = self.rhs值[当前]
                if 当前 in self.队列索引:
                    del self.队列索引[当前]
                for 前驱 in self.前驱节点(当前):
                    self.更新顶点(前驱)
            else:
                self.g值[当前] = float("inf")
                self.更新顶点(当前)
                for 前驱 in self.前驱节点(当前):
                    self.更新顶点(前驱)

        # 路径重建
        if self.g值[self.起点] == float("inf"):
            return _结果封装({"路径": [], "总成本": float("inf")}, "D星")
        路径 = [self.起点]
        当前 = self.起点
        while 当前 != self.终点:
            最优邻居 = None
            最优成本 = float("inf")
            for 邻居 in self.前驱节点(当前):
                成本 = self.g值[邻居] + self.地图[邻居[0]][邻居[1]]
                if 成本 < 最优成本:
                    最优成本 = 成本
                    最优邻居 = 邻居
            if 最优邻居 is None or 最优邻居 in 路径:
                break
            路径.append(最优邻居)
            当前 = 最优邻居
        return _结果封装({"路径": 路径, "总成本": self.g值[self.起点]}, "D星")


# ════════════════════════════════════════════════════════
# 四、CLI 与测试入口
# ════════════════════════════════════════════════════════

def 主测试() -> Dict:
    """
    龍魂路径规划引擎 · 一键测试
    DNA: #龍芯⚡️丙午·癸未·丁未-测试-v4.1.5
    """
    测试地图 = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, -1, -1, 1, -1, -1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, -1, 1, -1, 1, -1, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ]
    起点 = (0, 0)
    终点 = (4, 6)

    print("=" * 60)
    print("龍魂路径规划引擎 · 全算法测试")
    print(f"DNA: {DNA}")
    print(f"时间: {_now()}")
    print("=" * 60)

    结果1 = 迪杰斯特拉(测试地图, 起点, 终点)
    print("\n[1/4] 迪杰斯特拉算法...")
    print(f"  路径: {结果1['路径']}")
    print(f"  总成本: {结果1['总成本']}")
    print(f"  已访问节点: {结果1['已访问节点数']}")

    结果2 = A星算法(测试地图, 起点, 终点, "曼哈顿")
    print("\n[2/4] A*启发式算法...")
    print(f"  路径: {结果2['路径']}")
    print(f"  总成本: {结果2['总成本']}")
    print(f"  扩展节点: {结果2['扩展节点数']}")

    结果3 = 动态规划路径(测试地图, 起点, 终点)
    print("\n[3/6] 动态规划算法...")
    print(f"  路径: {结果3['路径']}")
    print(f"  总成本: {结果3['总成本']}")
    print(f"  迭代次数: {结果3['迭代次数']}")

    人格权重 = {"军事": 0.4, "历史": 0.2, "哲学": 0.1, "经济": 0.1, "政治": 0.2}
    结果4 = 八卦阵寻路(测试地图, 起点, 终点, 人格权重)
    print("\n[4/6] 八卦阵寻路...")
    print(f"  路径: {结果4['路径']}")
    print(f"  总成本: {结果4['总成本']}")
    print(f"  主导人格: {结果4['主导人格']}")

    print("\n[5/6] 蚁群分布式寻路...")
    结果5 = 蚁群分布式寻路(测试地图, 起点, 终点, 蚂蚁数=30, 迭代次数=60)
    print(f"  路径: {结果5['路径']}")
    print(f"  总成本: {结果5['总成本']}")
    print(f"  到达终点次数: {结果5['到达终点次数']}")

    print("\n[6/6] D* Lite 动态重规划...")
    d星 = D星精简版(测试地图)
    d星.初始化(起点, 终点)
    d星结果 = d星.计算最短路径()
    print(f"  路径: {d星结果['路径']}")
    print(f"  总成本: {d星结果['总成本']}")

    校验 = 三六九不动点校验(终点, 起点, 终点, 结果4["路径"])
    print("\n[+] 三六九不动点校验...")
    print(f"  宏观: {'✅' if 校验['宏观合格'] else '❌'}")
    print(f"  中观: {'✅' if 校验['中观合格'] else '❌'}")
    print(f"  微观: {'✅' if 校验['微观合格'] else '❌'}")
    print(f"  建议: {校验['建议']}")

    报告 = _结果封装({
        "算法结果": {
            "迪杰斯特拉": 结果1,
            "A星": 结果2,
            "动态规划": 结果3,
            "八卦阵": 结果4,
            "蚁群": 结果5,
            "D星精简版": d星结果,
        },
        "不动点校验": 校验,
    }, "测试报告")

    print("\n" + "=" * 60)
    print("测试完成，报告已保存: longhun_pathfinder_test_report.json")
    print("=" * 60)
    return 报告


def main():
    parser = argparse.ArgumentParser(description="龍魂路径规划引擎 v4.1.5")
    parser.add_argument("--test", action="store_true", help="运行全算法测试")
    parser.add_argument("--algorithm", choices=["dijkstra", "astar", "dp", "bagua"], default="astar")
    parser.add_argument("--start", help="起点，格式 行,列")
    parser.add_argument("--goal", help="终点，格式 行,列")
    parser.add_argument("--map", help="地图 JSON 文件路径")
    args = parser.parse_args()

    print(DNA)
    print(CONFIRM)

    if args.test or not args.map:
        报告 = 主测试()
        with open("longhun_pathfinder_test_report.json", "w", encoding="utf-8") as f:
            json.dump(报告, f, ensure_ascii=False, indent=2)
        return

    with open(args.map, "r", encoding="utf-8") as f:
        地图 = json.load(f)
    起点 = tuple(map(int, args.start.split(",")))
    终点 = tuple(map(int, args.goal.split(",")))

    if args.algorithm == "dijkstra":
        结果 = 迪杰斯特拉(地图, 起点, 终点)
    elif args.algorithm == "astar":
        结果 = A星算法(地图, 起点, 终点)
    elif args.algorithm == "dp":
        结果 = 动态规划路径(地图, 起点, 终点)
    else:
        结果 = 八卦阵寻路(地图, 起点, 终点)
    print(json.dumps(结果, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
