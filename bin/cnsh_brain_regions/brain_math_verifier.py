# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-BRAIN_MATH_VERIFIER-v1.0-7faa687e
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
B5 · 数学验证脑区 → P06 数学大师
====================================
复杂度分析（时间/空间/圈）· 公式验证 · 数值稳定性 · 算法模式识别 · 优化建议。

DNA: #龙芯⚡️丙午·丙申·丙辰·未时·需-BRAIN-B5-MATH-VERIFIER-v1.1
升级: v1.1 — 圈复杂度 + 算法模式识别 + 数值稳定性 + 分治/二分检测
"""

import re
import math
import ast
from typing import Dict, Any, List, Tuple, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# 1. 代码结构特征提取
# ═══════════════════════════════════════════════════════════════════════════════

def _get_indent(line: str) -> int:
    """获取行缩进（空行返回-1）"""
    if not line.strip():
        return -1
    return len(line) - len(line.lstrip())


def _build_indent_stack(lines: List[str]) -> List[int]:
    """构建缩进层级栈，识别真正的嵌套"""
    stack_depth = 0
    prev_indent = 0
    depths = []
    for line in lines:
        indent = _get_indent(line)
        if indent < 0:
            depths.append(stack_depth)
            continue
        if indent > prev_indent:
            stack_depth += 1
        elif indent < prev_indent:
            stack_depth = max(0, stack_depth - 1)
        depths.append(stack_depth)
        prev_indent = max(indent, 0)
    return depths


def _count_control_structures(code: str) -> Dict[str, int]:
    """统计控制结构"""
    patterns = {
        "for_loops": r'\bfor\s+\w+\s+in\b',
        "while_loops": r'\bwhile\s+',
        "if_branches": r'\bif\s+',
        "elif_branches": r'\belif\s+',
        "else_branches": r'\belse\s*:',
        "try_blocks": r'\btry\s*:',
        "except_blocks": r'\bexcept',
        "with_blocks": r'\bwith\s+',
        "comprehensions": r'\bfor\s+\w+\s+in\b[^:]*\]',
    }
    counts = {}
    for name, pat in patterns.items():
        counts[name] = len(re.findall(pat, code))
    return counts


# ═══════════════════════════════════════════════════════════════════════════════
# 2. 圈复杂度 (Cyclomatic Complexity, McCabe)
# ═══════════════════════════════════════════════════════════════════════════════

def cyclomatic_complexity(code: str) -> Dict[str, Any]:
    """计算圈复杂度 M = E - N + 2P"""
    lines = code.split('\n')
    # 决策点统计
    decision_points = 1  # 基线 = 1
    decision_patterns = [
        r'\bif\b', r'\belif\b', r'\bfor\b', r'\bwhile\b',
        r'\band\b(?!\s*_)', r'\bor\b(?!\s*_)',  # 逻辑运算符
        r'\bexcept\b', r'\bwith\b', r'\bassert\b',
        r'\bcase\b',  # match-case
    ]
    for pat in decision_patterns:
        decision_points += len(re.findall(pat, code))

    # 分级
    if decision_points <= 10:
        level = "简单"
        color = "🟢"
    elif decision_points <= 20:
        level = "中等"
        color = "🟡"
    elif decision_points <= 50:
        level = "复杂"
        color = "🟡"
    else:
        level = "极其复杂"
        color = "🔴"

    return {
        "value": decision_points,
        "level": level,
        "color": color,
        "risk": "高" if decision_points > 20 else "中" if decision_points > 10 else "低"
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 3. 时间复杂度分析（模式识别法）
# ═══════════════════════════════════════════════════════════════════════════════

# 算法模式 → 复杂度映射
ALGO_PATTERNS: List[Tuple[str, str, str, List[str]]] = [
    # (复杂度, 中文名, 说明, 特征模式)
    ("O(1)", "常量", "常数时间", [
        "hash_table", "dict", "HashMap", "set", "lookup",
    ]),
    ("O(log n)", "对数", "二分/分治", [
        r"\bmid\s*=", r"\bmiddle\s*=", r"\blow\s*=", r"\bhigh\s*=",
        r"//\s*2", r"/\s*2\b", r">>\s*1", r"divide", r"conquer",
        r"left\s*=", r"right\s*=", r"\bpivot\s*=",
    ]),
    ("O(n log n)", "线性对数", "排序/归并", [
        r"\.sort\(", r"sorted\(", r"merge", r"quicksort", r"heapsort",
        r"timsort", r"mergesort",
    ]),
    ("O(n)", "线性", "单层遍历", [
        r"\bfor\s+\w+\s+in\s+range", r"\bfor\s+\w+\s+in\s+\w+",
        r"\bwhile\s+\w+\s*[<>=!]",
    ]),
    ("O(n²)", "平方", "嵌套遍历", [
        # 双嵌套 + 无分治特征 → O(n²)
    ]),
    ("O(n³)", "立方", "三重嵌套", [
        # 三嵌套
    ]),
    ("O(2^n)", "指数", "递归/回溯", [
        r"\brecursion\b", r"\bbacktrack", r"\bdfs\b", r"\bfibonacci\b",
        r"permute", r"combinations",
    ]),
    ("O(n!)", "阶乘", "全排列", [
        r"permutations", r"all_permutations", r"旅行商", r"tsp",
    ]),
]


def _detect_binary_search(code: str) -> bool:
    """检测二分搜索模式：mid = (low+high)//2"""
    has_mid = bool(re.search(r'\bmid\s*=\s*\(?\s*\w+\s*\+\s*\w+\s*\)?\s*//\s*2', code))
    has_while_low_high = bool(re.search(r'\bwhile\s+\w+\s*[<>=]+\s*\w+', code))
    return has_mid and has_while_low_high


def _detect_divide_conquer(code: str) -> bool:
    """检测分治模式：自身调用 + 分段处理"""
    has_recursive = bool(re.search(r'\b(\w+)\s*\(.*\).*\n.*\1\s*\(', code, re.DOTALL))
    has_partition = any(p in code for p in ["left", "right", "mid", "split", "partition", "分治"])
    return has_recursive and has_partition


def _detect_dp(code: str) -> bool:
    """检测动态规划：dp/table/memo + 递推"""
    dp_keywords = ["dp[", "memo[", "table[", "cache[", "f[", "opt[", "dp_table"]
    has_dp = any(kw in code for kw in dp_keywords)
    has_recurrence = bool(re.search(r'=\s*\w+\[\s*\w+\s*-\s*1\s*\]', code))
    return has_dp or has_recurrence


def analyze_complexity(code: str) -> Dict[str, Any]:
    """综合分析时间+空间复杂度（模式识别 + 结构分析）"""
    lines = [l for l in code.split('\n') if l.strip() and not l.strip().startswith(('#', '//'))]
    indent_depths = _build_indent_stack(code.split('\n'))

    # 缩进层级分析
    loop_lines = []
    loop_indices = []
    for i, line in enumerate(code.split('\n')):
        stripped = line.strip()
        if re.search(r'\b(for|while)\b', stripped) and not stripped.startswith(('#', '//')):
            loop_lines.append(stripped)
            loop_indices.append(i)

    loop_depths = [indent_depths[i] for i in loop_indices if i < len(indent_depths)]
    max_nesting = max(loop_depths) if loop_depths else 0
    nested_count = sum(1 for d in loop_depths if d >= 1)

    # 算法模式检测
    has_binary = _detect_binary_search(code)
    has_dc = _detect_divide_conquer(code)
    has_dp = _detect_dp(code)
    has_sort = bool(re.search(r'\.sort\(|sorted\(', code))

    # 递归自调用检测（排除def定义行本身）
    func_names = re.findall(r'\bdef\s+(\w+)\s*\(', code)
    recursive_funcs = []
    for fn in func_names:
        # 在非def行中搜索自调用
        for line in code.split('\n'):
            stripped = line.strip()
            if stripped.startswith(f'def {fn}'):
                continue  # 跳过定义行
            if re.search(r'\b' + re.escape(fn) + r'\s*\(', stripped):
                if fn not in recursive_funcs:
                    recursive_funcs.append(fn)
    has_recursive = bool(recursive_funcs)

    # ── 时间复杂度判定 ──
    if has_binary or (has_dc and max_nesting <= 1):
        big_o = "O(log n)"
        level = "对数"
        reason = "检测到二分搜索/分治模式"
    elif has_sort and max_nesting >= 2:
        big_o = "O(n log n)"
        level = "线性对数"
        reason = "排序算法 + 后续处理"
    elif has_sort:
        big_o = "O(n log n)"
        level = "线性对数"
        reason = "排序算法主导"
    elif max_nesting == 0 and not recursive_funcs:
        big_o = "O(1)"
        level = "常量"
        reason = "无循环/递归"
    elif max_nesting == 0 and recursive_funcs:
        if has_dc:
            big_o = "O(n log n)"
            level = "线性对数"
            reason = "分治递归"
        elif has_dp:
            big_o = "O(n)"
            level = "线性"
            reason = "动态规划(带记忆化)"
        else:
            big_o = "O(2^n)"
            level = "指数"
            reason = f"递归未优化({'+'.join(recursive_funcs)})"
    elif max_nesting == 1:
        if "while" in ' '.join(loop_lines) and any(kw in code for kw in ["n", "size", "length"]):
            big_o = "O(n)"
            level = "线性"
            reason = "单层变量循环"
        else:
            big_o = "O(n)"
            level = "线性"
            reason = "单层遍历"
    elif max_nesting == 2:
        if has_binary or has_dc:
            big_o = "O(n log n)"
            level = "线性对数"
            reason = "嵌套+分治(内层对数缩减)"
        else:
            big_o = "O(n²)"
            level = "平方"
            reason = "双层嵌套遍历"
    elif max_nesting == 3:
        big_o = "O(n³)"
        level = "立方"
        reason = "三层嵌套"
    elif max_nesting >= 4:
        big_o = "O(n^k)"
        level = f"{max_nesting}次方"
        reason = f"{max_nesting}层循环嵌套"

    # ── 空间复杂度判定 ──
    has_large_struct = bool(re.search(r'(list|dict|set|map)\s*\(|\[\s*\]\s*\*\s*|np\.zeros|np\.ones', code))
    has_aux = bool(re.search(r'\b(result|temp|buffer|cache|memo|dp|visited)\s*=', code))

    if recursive_funcs and has_aux:
        space = "O(n)"
        space_reason = "递归调用栈 + 辅助数据结构"
    elif recursive_funcs:
        space = "O(log n ~ n)"
        space_reason = "递归调用栈深度"
    elif has_large_struct or has_aux:
        space = "O(n)"
        space_reason = "辅助数据结构"
    else:
        space = "O(1)"
        space_reason = "常量额外空间"

    return {
        "time_big_o": big_o,
        "time_level": level,
        "time_reason": reason,
        "max_loop_nesting": max_nesting,
        "loop_count": len(loop_lines),
        "nested_loop_count": nested_count,
        "space_big_o": space,
        "space_reason": space_reason,
        "has_recursive": bool(recursive_funcs),
        "recursive_funcs": recursive_funcs,
        "has_binary_search": has_binary,
        "has_divide_conquer": has_dc,
        "has_dynamic_programming": has_dp,
        "has_sort": has_sort,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 4. 数值稳定性检测
# ═══════════════════════════════════════════════════════════════════════════════

def numerical_stability_check(code: str) -> Dict[str, Any]:
    """检测数值稳定性风险"""
    risks = []

    # 除零风险
    if re.search(r'/\s*0\b', code):
        risks.append({"type": "除零", "severity": "🔴", "message": "硬编码除零"})
    if re.search(r'/\s*\w+\s*$', code, re.MULTILINE):
        # 检测变量除数未保护
        div_lines = [l.strip() for l in code.split('\n') if '/' in l and '=' in l]
        for dl in div_lines:
            m = re.search(r'/\s*(\w+)', dl)
            if m:
                var = m.group(1)
                # 检查上方是否有 if var == 0 或 if var != 0
                if not re.search(rf'\bif\s+{var}\s*[!=]=\s*0', code) and \
                   not re.search(rf'\bassert\s+{var}\s*[!=]=\s*0', code) and \
                   not re.search(rf'\bmax\(\s*{var}', code) and \
                   var not in ('2', '1'):
                    risks.append({"type": "未防除零", "severity": "🟡", "message": f"变量 {var} 作除数未保护"})

    # NaN/Inf 检测
    has_nan_check = any(kw in code for kw in ["math.isnan", "np.isnan", "math.isinf", "np.isinf"])
    uses_float_ops = bool(re.search(r'\bfloat\b|np\.float|np\.divide|np\.log|np\.exp|np\.sqrt', code))
    if uses_float_ops and not has_nan_check:
        risks.append({"type": "未防NaN/Inf", "severity": "🟡", "message": "浮点运算未做NaN/Inf检查"})

    # 整数溢出（Python无关但提示）
    has_large_shift = bool(re.search(r'<<\s*(3[2-9]|[4-9]\d)', code))
    if has_large_shift:
        risks.append({"type": "可能溢出", "severity": "🟡", "message": "大位移操作可能越界"})

    # 精度丢失
    if re.search(r'==\s*\d+\.\d+', code):
        risks.append({"type": "浮点比较", "severity": "🟡", "message": "浮点数直接用==比较可能精度丢失，用abs(a-b)<epsilon"})

    # 大数阶乘/组合数
    if re.search(r'\b(math\.)?(factorial|comb|perm)\b', code):
        risks.append({"type": "大数计算", "severity": "🟡", "message": "阶乘/组合数增长极快，注意输入上限"})

    return {
        "risks": risks,
        "risk_count": len(risks),
        "has_critical": any(r["severity"] == "🔴" for r in risks),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 5. 优化建议生成
# ═══════════════════════════════════════════════════════════════════════════════

def generate_optimization_hints(complexity: Dict, stability: Dict, code: str) -> List[Dict[str, str]]:
    """综合生成优化建议"""
    hints = []

    # 时间复杂度建议
    if complexity["max_loop_nesting"] >= 3:
        hints.append({"level": "🔴", "category": "时间复杂度", "hint": "三层+嵌套循环 → 考虑降维：哈希表预计算或空间换时间"})
    elif complexity["max_loop_nesting"] == 2 and not complexity["has_divide_conquer"]:
        hints.append({"level": "🟡", "category": "时间复杂度", "hint": "O(n²)嵌套 → 检查是否能用哈希表/set降为O(n)"})

    if complexity["has_recursive"] and not complexity["has_dynamic_programming"]:
        hints.append({"level": "🟡", "category": "递归优化", "hint": "递归未记忆化 → 加 @lru_cache 或手动 memo 降为DP"})

    if complexity["time_big_o"] == "O(2^n)" and not complexity["has_dynamic_programming"]:
        hints.append({"level": "🔴", "category": "指数复杂度", "hint": "O(2^n) → 必须DP优化或用贪心/近似算法替代"})

    if complexity["time_big_o"] in ("O(n log n)",) and complexity["has_sort"] and complexity["max_loop_nesting"] <= 1:
        hints.append({"level": "🟢", "category": "复杂度良好", "hint": "O(n log n)排序后线扫 → 设计合理"})

    if complexity["time_big_o"] == "O(log n)":
        hints.append({"level": "🟢", "category": "最优复杂度", "hint": "O(log n)对数时间 → 高效"})

    # 空间优化
    if complexity["space_big_o"] == "O(n)" and complexity["max_loop_nesting"] >= 2:
        hints.append({"level": "🟡", "category": "空间换时间", "hint": "O(n)空间+O(n²)时间 → 可考虑多花空间换时间优化"})

    # 稳定性提示
    for risk in stability.get("risks", []):
        hints.append({"level": risk["severity"], "category": "数值稳定性", "hint": risk["message"]})

    # Python 特定优化
    if re.search(r'\bfor\s+\w+\s+in\s+range\(\s*len\(', code):
        hints.append({"level": "🟢", "category": "Python风格", "hint": "range(len(x)) → 用 enumerate(x) 更Pythonic"})
    if "list(" in code and "map(" in code:
        hints.append({"level": "🟢", "category": "Python风格", "hint": "list(map(f, x)) → [f(i) for i in x] 列表推导更快"})

    return hints


# ═══════════════════════════════════════════════════════════════════════════════
# 6. 主执行入口
# ═══════════════════════════════════════════════════════════════════════════════

def execute(code: str, features: Dict[str, Any], step: int, total: int) -> Dict[str, Any]:
    """
    B5 脑区执行入口
    返回: output_code, auto_activate, 分析结果
    """
    complexity = analyze_complexity(code)
    cyclomatic = cyclomatic_complexity(code)
    stability = numerical_stability_check(code)
    hints = generate_optimization_hints(complexity, stability, code)

    # 统计
    total_loops = complexity["loop_count"]
    has_issues = complexity["max_loop_nesting"] >= 2 or stability["risk_count"] > 0

    # 自动激活规则
    auto_activate = []
    if complexity["max_loop_nesting"] >= 2:
        auto_activate.append("B6")  # 高复杂度 → B6代码优化
    if stability["has_critical"]:
        auto_activate.append("B7")  # 数值红线 → B7质量审计

    # 生成人类可读摘要
    time_str = f"{complexity['time_big_o']}({complexity['time_level']})"
    space_str = complexity["space_big_o"]
    issue_count = len([h for h in hints if h["level"] in ("🔴", "🟡")])
    good_count = len([h for h in hints if h["level"] == "🟢"])

    message_parts = [f"B5: 时{time_str}·空{space_str}·圈{cyclomatic['value']}({cyclomatic['level']})"]
    if complexity["has_binary_search"]:
        message_parts.append("·二分")
    if complexity["has_divide_conquer"]:
        message_parts.append("·分治")
    if complexity["has_dynamic_programming"]:
        message_parts.append("·DP")
    if has_issues:
        message_parts.append(f"·{issue_count}条建议")
    if good_count:
        message_parts.append(f"·{good_count}条👌")

    return {
        "output_code": code,
        "auto_activate": auto_activate,
        "complexity": {
            "time": time_str,
            "time_big_o": complexity["time_big_o"],
            "time_level": complexity["time_level"],
            "time_reason": complexity["time_reason"],
            "space": space_str,
            "space_big_o": complexity["space_big_o"],
            "space_reason": complexity["space_reason"],
            "max_loop_nesting": complexity["max_loop_nesting"],
            "loop_count": total_loops,
            "nested_loop_count": complexity["nested_loop_count"],
        },
        "cyclomatic": cyclomatic,
        "patterns": {
            "binary_search": complexity["has_binary_search"],
            "divide_conquer": complexity["has_divide_conquer"],
            "dynamic_programming": complexity["has_dynamic_programming"],
            "sort": complexity["has_sort"],
            "recursive_funcs": complexity["recursive_funcs"],
        },
        "stability": {
            "risk_count": stability["risk_count"],
            "has_critical": stability["has_critical"],
            "risks": stability["risks"],
        },
        "optimization_hints": hints,
        "message": " · ".join(message_parts),
        "persona": "P06",
        "persona_name": "数学大师",
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 7. 自测
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    test_cases = [
        ("冒泡排序 O(n²)", """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
"""),
        ("二分搜索 O(log n)", """
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
"""),
        ("DP斐波那契 O(n)", """
def fib(n):
    dp = [0] * (n + 1)
    dp[0], dp[1] = 0, 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
"""),
        ("三重循环 O(n³)", """
def three_sum(nums):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    return [i, j, k]
    return []
"""),
        ("递归(无记忆化) O(2^n)", """
def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)
"""),
    ]

    import json
    for name, code in test_cases:
        r = execute(code, {}, 0, 0)
        print(f"\n{'='*60}")
        print(f"  📐 {name}")
        print(f"{'='*60}")
        print(f"  复杂度: {r['complexity']['time']} ({r['complexity']['time_reason']})")
        print(f"  空间:   {r['complexity']['space']} ({r['complexity']['space_reason']})")
        print(f"  圈复杂度: {r['cyclomatic']['value']} ({r['cyclomatic']['level']})")
        print(f"  模式: 二分={r['patterns']['binary_search']} 分治={r['patterns']['divide_conquer']} DP={r['patterns']['dynamic_programming']}")
        print(f"  数值风险: {r['stability']['risk_count']}个")
        for h in r['optimization_hints']:
            print(f"  {h['level']} [{h['category']}] {h['hint']}")
        print(f"  自动激活: {r['auto_activate']}")
        print(f"  摘要: {r['message']}")

    # 汇总
    passed = 0
    expected = {
        "冒泡排序 O(n²)": "O(n²)",
        "二分搜索 O(log n)": "O(log n)",
        "DP斐波那契 O(n)": "O(n)",
        "三重循环 O(n³)": "O(n³)",
        "递归(无记忆化) O(2^n)": "O(2^n)",
    }
    for name, code in test_cases:
        r = execute(code, {}, 0, 0)
        exp = expected[name]
        actual = r['complexity']['time_big_o']
        status = "✅" if actual == exp else "❌"
        if actual == exp:
            passed += 1
        print(f"  {status} {name}: 期望={exp} 实际={actual}")

    print(f"\n{'='*60}")
    print(f"  🧮 通过: {passed}/{len(test_cases)}")
    print(f"{'='*60}")
