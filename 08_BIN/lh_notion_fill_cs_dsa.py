#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LH_NOTION_FILL_CS_DS-47B470C2
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍芯⚡️丙午·丙申·辛酉·未时·☰乾-NOTION-CS-DSA-FILL-v1.0
"""
🐉 龍魂 · 计算机科学知识库填充（数据结构与算法轻量版）

向 Notion 数据库「计算机科学知识库」批量写入经典数据结构与算法条目。
"""

import json
import hashlib
import time
from datetime import datetime
from pathlib import Path

import requests


NOTION_VERSION = "2022-06-28"
API_BASE = "https://api.notion.com/v1"
DB_ID = "3367125a9c9f808a9692f0c6752e92fa"


def get_token() -> str:
    cfg_path = Path(__file__).resolve().parent.parent / "config" / "notion_config.json"
    data = json.load(open(cfg_path, encoding="utf-8"))
    return data.get("notion_token") or data.get("token")


def headers() -> dict:
    return {
        "Authorization": f"Bearer {get_token()}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def guard(text: str) -> str:
    return text.replace("龙", "龍")


def dna(name: str) -> str:
    h = hashlib.md5(f"{name}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-CS-DSA-{h}-UID9622"


def rich_text(text: str):
    return {"rich_text": [{"text": {"content": guard(text)}}]}


def title(text: str):
    return {"title": [{"text": {"content": guard(text)}}]}


def select(name: str):
    return {"select": {"name": name}}


def status(name: str):
    return {"status": {"name": name}}


def multi_select(names: list):
    return {"multi_select": [{"name": n} for n in names]}


def number(val: float):
    return {"number": val}


DSA_TOPICS = [
    {
        "name": "数组 (Array)",
        "desc": "一组相同类型元素按连续内存地址存储的线性数据结构。支持 O(1) 随机访问，但插入/删除中间元素需要 O(n) 移动。是所有高级数据结构的基础。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L1 入门",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["基础理论", "编程语言"],
        "use_tags": ["🔢 数学/公式", "⚙️ 系统/底层"],
        "scenes": ["所有编程", "算法分析", "系统设计"],
        "hours": 2,
        "code": "# Python 数组操作示例\narr = [1, 2, 3, 4, 5]\narr.append(6)      # O(1) 均摊\narr.insert(2, 99)  # O(n)\nprint(arr[3])      # O(1) 访问",
        "formula": "访问: O(1) | 搜索: O(n) | 插入/删除: O(n)",
        "misconception": "数组和列表在 Python 中概念常被混淆；Python list 是动态数组，不是链表。",
    },
    {
        "name": "链表 (Linked List)",
        "desc": "由节点组成的线性数据结构，每个节点包含数据域和指向下一个节点的指针。支持 O(1) 头插/头删，但不支持随机访问。常用于实现队列、栈和图的邻接表。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L1 入门",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["基础理论", "编程语言"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["所有编程", "算法分析", "内存调试"],
        "hours": 3,
        "code": "class Node:\n    def __init__(self, val):\n        self.val = val\n        self.next = None\n\n# 头插法\nhead = Node(1)\nnew = Node(0)\nnew.next = head\nhead = new  # O(1)",
        "formula": "访问: O(n) | 插入/删除(已知节点): O(1) | 搜索: O(n)",
        "misconception": "链表并非总是比数组快；缓存局部性差，实际遍历效率常低于数组。",
    },
    {
        "name": "栈 (Stack)",
        "desc": "后进先出（LIFO）的线性数据结构。只允许在栈顶进行 push 和 pop 操作。广泛应用于函数调用栈、表达式求值、括号匹配、DFS 深度优先搜索等场景。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L1 入门",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["基础理论", "编程语言"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["所有编程", "算法分析", "代码审查"],
        "hours": 2,
        "code": "stack = []\nstack.append(1)  # push\nstack.append(2)\ntop = stack[-1]  # peek\nstack.pop()      # pop O(1)",
        "formula": "push/pop/peek: O(1)",
        "misconception": "栈不是只能递归替代；合理用栈可避免递归栈溢出。",
    },
    {
        "name": "队列 (Queue)",
        "desc": "先进先出（FIFO）的线性数据结构。在队尾入队，在队头出队。常用于 BFS 广度优先搜索、任务调度、消息队列、缓存实现等。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L1 入门",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["基础理论", "编程语言"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["BFS", "任务调度", "消息队列", "高并发后端"],
        "hours": 2,
        "code": "from collections import deque\nq = deque()\nq.append(1)   # enqueue\nq.append(2)\nfront = q[0]  # peek\nq.popleft()   # dequeue O(1)",
        "formula": "enqueue/dequeue/peek: O(1)",
        "misconception": "普通 list 做队列出队是 O(n)；应使用 deque。",
    },
    {
        "name": "哈希表 (Hash Table)",
        "desc": "通过哈希函数将键映射到桶中，实现平均 O(1) 的插入、删除和查找。冲突解决策略包括链地址法和开放寻址法。是现代编程语言字典/Map 的底层实现。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L1-L2",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["基础理论", "编程语言"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["所有编程", "数据库", "缓存", "系统设计"],
        "hours": 4,
        "code": "# Python dict 即哈希表\nd = {}\nd['key'] = 'value'\nprint(d.get('key'))  # O(1) 平均\n\n# 自定义哈希思路\nhash_val = hash('key') % 16  # 映射到 16 个桶",
        "formula": "平均: 插入/删除/查找 O(1) | 最坏: O(n)",
        "misconception": "哈希表不是绝对 O(1)；恶意构造冲突或扩容时会退化。",
    },
    {
        "name": "二分查找 (Binary Search)",
        "desc": "在有序数组上通过每次排除一半元素来快速定位目标。核心思想是维护搜索区间 [left, right]，根据中间值与目标的大小关系缩小范围。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L1 入门",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["基础理论"],
        "use_tags": ["🔢 数学/公式"],
        "scenes": ["算法分析", "面试", "数据库", "性能优化"],
        "hours": 3,
        "code": "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1",
        "formula": "时间: O(log n) | 空间: O(1)",
        "misconception": "二分查找不仅用于数组；任何具有单调性的解空间都可用。",
    },
    {
        "name": "冒泡排序 (Bubble Sort)",
        "desc": "最简单的比较排序算法之一。反复遍历数组，相邻元素两两比较并交换，使较大元素逐渐冒泡到末尾。主要用于教学理解排序思想，实际很少使用。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L1 入门",
        "priority": "P2-了解",
        "core": "⚪ 暂不需要",
        "tags": ["基础理论"],
        "use_tags": ["🔢 数学/公式"],
        "scenes": ["学习/复习", "面试"],
        "hours": 1,
        "code": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr",
        "formula": "时间: O(n²) | 空间: O(1) | 稳定排序",
        "misconception": "冒泡排序因名字常被误认为高效；实际生产环境几乎不用。",
    },
    {
        "name": "快速排序 (Quick Sort)",
        "desc": "基于分治思想的高效排序算法。选择基准值 pivot，将数组划分为小于 pivot 和大于 pivot 的两部分，递归排序。平均性能极好，是实际应用最广泛的排序算法之一。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L1-L2",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["基础理论"],
        "use_tags": ["🔢 数学/公式", "⚙️ 系统/底层"],
        "scenes": ["算法分析", "面试", "性能优化", "所有编程"],
        "hours": 4,
        "code": "def quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr)//2]\n    left = [x for x in arr if x < pivot]\n    mid = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quick_sort(left) + mid + quick_sort(right)",
        "formula": "平均: O(n log n) | 最坏: O(n²) | 空间: O(log n)",
        "misconception": "快速排序不是稳定排序；需要稳定性时应选归并排序。",
    },
    {
        "name": "归并排序 (Merge Sort)",
        "desc": "经典的分治稳定排序算法。将数组递归分成两半分别排序，然后合并两个有序数组。常用于链表排序、外部排序和需要稳定性的场景。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L1-L2",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["基础理论"],
        "use_tags": ["🔢 数学/公式"],
        "scenes": ["算法分析", "面试", "外部排序"],
        "hours": 3,
        "code": "def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)\n\ndef merge(a, b):\n    res = []\n    i = j = 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]:\n            res.append(a[i]); i += 1\n        else:\n            res.append(b[j]); j += 1\n    return res + a[i:] + b[j:]",
        "formula": "时间: O(n log n) | 空间: O(n) | 稳定排序",
        "misconception": "归并排序空间复杂度不是 O(1)；需要额外数组。",
    },
    {
        "name": "二叉树 (Binary Tree)",
        "desc": "每个节点最多有两个子节点的树形数据结构。是二叉搜索树、堆、AVL 树、红黑树等高级结构的基础。遍历方式包括前序、中序、后序和层序。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L1-L2",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["基础理论"],
        "use_tags": ["🔢 数学/公式"],
        "scenes": ["算法分析", "面试", "数据库", "系统设计"],
        "hours": 4,
        "code": "class TreeNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.left = None\n        self.right = None\n\n# 中序遍历\ndef inorder(root):\n    if root:\n        inorder(root.left)\n        print(root.val)\n        inorder(root.right)",
        "formula": "遍历: O(n) | 空间: O(h)，h 为树高",
        "misconception": "二叉树不等同于二叉搜索树；普通二叉树无顺序要求。",
    },
    {
        "name": "二叉搜索树 (Binary Search Tree)",
        "desc": "一种有序二叉树，左子树所有节点值小于根，右子树所有节点值大于根。支持动态查找、插入和删除，但不平衡时会退化为链表。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L2 进阶",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["基础理论"],
        "use_tags": ["🔢 数学/公式"],
        "scenes": ["算法分析", "面试", "数据库索引"],
        "hours": 4,
        "code": "def search(root, target):\n    if not root or root.val == target:\n        return root\n    if target < root.val:\n        return search(root.left, target)\n    return search(root.right, target)",
        "formula": "平均: O(log n) | 最坏(退化): O(n)",
        "misconception": "普通 BST 不能保证 O(log n)；平衡树如 AVL/红黑树才能保证。",
    },
    {
        "name": "堆 (Heap / Priority Queue)",
        "desc": "一种特殊的完全二叉树，分为最大堆和最小堆。堆顶元素总是最大/最小值。常用于实现优先队列、Top-K 问题、堆排序和图算法中的 Dijkstra。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L2 进阶",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["基础理论"],
        "use_tags": ["🔢 数学/公式"],
        "scenes": ["算法分析", "面试", "性能优化", "Top-K"],
        "hours": 4,
        "code": "import heapq\n\n# 最小堆\nh = []\nheapq.heappush(h, 3)\nheapq.heappush(h, 1)\nheapq.heappush(h, 2)\nprint(heapq.heappop(h))  # 1",
        "formula": "插入/删除: O(log n) | 查询堆顶: O(1) | 建堆: O(n)",
        "misconception": "堆不是有序数组；只保证堆顶极值，不保证全局有序。",
    },
    {
        "name": "图的邻接表表示 (Graph Adjacency List)",
        "desc": "图的一种高效存储方式，为每个顶点维护一个邻居列表。适合稀疏图，空间复杂度为 O(V+E)。是 BFS、DFS、Dijkstra、拓扑排序等图算法的基础。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L2 进阶",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["基础理论"],
        "use_tags": ["🔢 数学/公式"],
        "scenes": ["算法分析", "面试", "社交网络", "路由算法"],
        "hours": 3,
        "code": "# 无向图邻接表\ngraph = {\n    0: [1, 2],\n    1: [0, 2],\n    2: [0, 1, 3],\n    3: [2]\n}",
        "formula": "空间: O(V+E) | 查询边: O(deg(v))",
        "misconception": "邻接表不是唯一图表示；稠密图更适合邻接矩阵。",
    },
    {
        "name": "BFS 广度优先搜索",
        "desc": "从起点出发，按层次逐层访问所有可达节点的图遍历算法。使用队列实现，常用于最短路径（无权图）、连通性检测、拓扑排序和层次遍历。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L1-L2",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["基础理论"],
        "use_tags": ["🔢 数学/公式"],
        "scenes": ["算法分析", "面试", "BFS", "最短路径"],
        "hours": 4,
        "code": "from collections import deque\n\ndef bfs(graph, start):\n    visited = set([start])\n    q = deque([start])\n    while q:\n        u = q.popleft()\n        for v in graph[u]:\n            if v not in visited:\n                visited.add(v)\n                q.append(v)\n    return visited",
        "formula": "时间: O(V+E) | 空间: O(V)",
        "misconception": "BFS 只在无权图中保证最短路径；带权图需用 Dijkstra。",
    },
    {
        "name": "DFS 深度优先搜索",
        "desc": "从起点出发，沿着一条路径尽可能深入，到达尽头后回溯。使用栈（递归或显式栈）实现。常用于连通分量、环检测、拓扑排序和全排列/组合问题。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L1-L2",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["基础理论"],
        "use_tags": ["🔢 数学/公式"],
        "scenes": ["算法分析", "面试", "回溯", "连通分量"],
        "hours": 4,
        "code": "def dfs(graph, start, visited=None):\n    if visited is None:\n        visited = set()\n    visited.add(start)\n    for v in graph[start]:\n        if v not in visited:\n            dfs(graph, v, visited)\n    return visited",
        "formula": "时间: O(V+E) | 空间: O(V)",
        "misconception": "DFS 不一定用递归；显式栈可避免递归深度限制和栈溢出。",
    },
    {
        "name": "动态规划 (Dynamic Programming)",
        "desc": "通过将复杂问题分解为相互重叠的子问题，并缓存子问题解来避免重复计算。关键步骤：定义状态、状态转移方程、初始条件和遍历顺序。常用于最优化问题。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L2 进阶",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["基础理论"],
        "use_tags": ["🔢 数学/公式"],
        "scenes": ["算法分析", "面试", "最优化", "所有编程"],
        "hours": 8,
        "code": "# 斐波那契 DP\ndef fib(n):\n    if n <= 1:\n        return n\n    dp = [0] * (n + 1)\n    dp[1] = 1\n    for i in range(2, n + 1):\n        dp[i] = dp[i-1] + dp[i-2]\n    return dp[n]",
        "formula": "时间/空间取决于状态数和转移；通常优于暴力指数级",
        "misconception": "DP 不是记忆化搜索的专利；自底向上迭代也常更高效。",
    },
    {
        "name": "贪心算法 (Greedy Algorithm)",
        "desc": "在每一步选择当前看起来最优的局部决策，希望最终得到全局最优解。适用于具有贪心选择性质和最优子结构的问题，如活动选择、霍夫曼编码、最小生成树 Kruskal。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L2 进阶",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["基础理论"],
        "use_tags": ["🔢 数学/公式"],
        "scenes": ["算法分析", "面试", "最优化", "调度"],
        "hours": 4,
        "code": "# 活动选择问题（按结束时间排序，选最早结束且不冲突的）\ndef activity_selection(activities):\n    activities.sort(key=lambda x: x[1])\n    selected = [activities[0]]\n    for s, e in activities[1:]:\n        if s >= selected[-1][1]:\n            selected.append((s, e))\n    return selected",
        "formula": "时间: 通常 O(n log n)（排序主导）",
        "misconception": "贪心不总能得到全局最优；必须先证明贪心选择性质。",
    },
    {
        "name": "Dijkstra 最短路径算法",
        "desc": "用于求解带权有向图中单源最短路径的经典算法。基于贪心策略，每次选择当前距离源点最近的未确定顶点，并松弛其邻居。要求边权非负。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L2-L3",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["基础理论"],
        "use_tags": ["🔢 数学/公式"],
        "scenes": ["算法分析", "面试", "路由算法", "地图导航"],
        "hours": 5,
        "code": "import heapq\n\ndef dijkstra(graph, start):\n    dist = {v: float('inf') for v in graph}\n    dist[start] = 0\n    pq = [(0, start)]\n    while pq:\n        d, u = heapq.heappop(pq)\n        if d > dist[u]:\n            continue\n        for v, w in graph[u]:\n            if dist[u] + w < dist[v]:\n                dist[v] = dist[u] + w\n                heapq.heappush(pq, (dist[v], v))\n    return dist",
        "formula": "时间: O((V+E) log V) | 空间: O(V)",
        "misconception": "Dijkstra 不能处理负权边；负权边需用 Bellman-Ford。",
    },
    {
        "name": "递归与分治 (Recursion & Divide-and-Conquer)",
        "desc": "递归是函数调用自身的编程技巧；分治是将问题分解为独立子问题、分别求解再合并结果的思想。二者结合构成了归并排序、快速排序、二分查找等经典算法。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L1-L2",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["基础理论", "编程语言"],
        "use_tags": ["🔢 数学/公式"],
        "scenes": ["算法分析", "面试", "所有编程"],
        "hours": 4,
        "code": "# 递归求阶乘\ndef factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\n# 分治：归并排序、快速排序",
        "formula": "递归深度决定栈空间；分治时间通常可用主定理分析",
        "misconception": "递归不是效率低的原因；尾递归和记忆化可大幅优化。",
    },
    {
        "name": "时间复杂度与大 O 表示法",
        "desc": "描述算法运行时间随输入规模增长的趋势。大 O 忽略常数和低阶项，关注最坏情况下算法性能的上界。是衡量算法效率和选择实现方案的核心工具。",
        "category": "基础理论",
        "subcategory": "计算机科学基础",
        "difficulty": "L1 入门",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["基础理论"],
        "use_tags": ["🔢 数学/公式"],
        "scenes": ["算法分析", "面试", "性能优化", "所有编程"],
        "hours": 3,
        "code": "# 常见复杂度示例\n# O(1): arr[0]\n# O(log n): 二分查找\n# O(n): 线性扫描\n# O(n log n): 快速排序\n# O(n²): 冒泡排序",
        "formula": "O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ)",
        "misconception": "大 O 不是实际运行时间，而是增长趋势；小数据量时 O(n²) 可能比 O(n log n) 更快。",
    },
]


def create_page(topic: dict) -> dict:
    properties = {
        "知识点名称": title(topic["name"]),
        "描述": rich_text(topic["desc"]),
        "分类": select(topic["category"]),
        "子分类": select(topic["subcategory"]),
        "学习优先级": select(topic["priority"]),
        "难度等级": select(topic["difficulty"]),
        "是否核心": select(topic["core"]),
        "标签": multi_select(topic["tags"]),
        "用途标签": multi_select(topic["use_tags"]),
        "应用场景": multi_select(topic["scenes"]),
        "预计学习时长（小时）": number(topic["hours"]),
        "PY代码示例": rich_text(topic["code"]),
        "核心公式": rich_text(topic["formula"]),
        "常见误区": rich_text(topic["misconception"]),
        "DNA追溯": rich_text(dna(topic["name"])),
        "来源/参考": rich_text("龍魂系统 · 计算机科学知识库填充脚本 v1.0"),
        "关联知识点": rich_text("数组, 链表, 栈, 队列, 哈希表, 排序, 图, 树, 动态规划, 贪心"),
        "关键词索引": multi_select(["算法", "数据结构", "复杂度", "计算机基础"]),
        "学习状态": status("未开始"),
        "掌握程度": select("未掌握"),
    }
    return {
        "parent": {"database_id": DB_ID},
        "properties": properties,
    }


def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🐉 开始向 Notion 写入 {len(DSA_TOPICS)} 条数据结构与算法知识点...")

    created = 0
    failed = 0
    for topic in DSA_TOPICS:
        payload = create_page(topic)
        r = requests.post(f"{API_BASE}/pages", headers=headers(), json=payload)
        if r.status_code == 200:
            created += 1
            print(f"  ✅ {topic['name']}")
        else:
            failed += 1
            print(f"  ❌ {topic['name']}: {r.status_code} {r.text[:100]}")
        time.sleep(0.3)

    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ 完成: {created} 条成功, {failed} 条失败")


if __name__ == "__main__":
    main()
