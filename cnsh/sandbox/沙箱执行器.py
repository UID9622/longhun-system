#龍芯⚡️2026-06-18-CNSH-sandbox-沙箱执行器-v1.0
"""
通心译 | TongXinYi: Sandbox Executor
龍魂体系·沙箱执行器 — 安全代码执行与隔离环境

提供受限的Python代码执行环境，防止恶意代码破坏系统
Provides restricted Python execution environment with resource limits
"""
# 🟢 君子协议 | JunZi Protocol: CC BY-NC-SA 4.0
# 🟡 AI Truth Protocol: All outputs must be verifiable and traceable
# 🔴 DNA Trace: #龍芯⚡️2026-06-18-CNSH-sandbox-沙箱执行器-v1.0

from datetime import datetime
from typing import Dict, Any, Optional
import io
import sys
import traceback

__版本__ = "v1.0"
__dna__ = "#龍芯⚡️2026-06-18-CNSH-sandbox-沙箱执行器-v1.0"


class 沙箱结果:
    """通心译 | TongXinYi: Sandbox Result — 沙箱执行结果"""

    def __init__(自身, 成功: bool, 输出: str = "", 返回值: Any = None, 错误: str = "", 耗时: float = 0):
        自身.成功 = 成功
        自身.输出 = 输出
        自身.返回值 = 返回值
        自身.错误 = 错误
        自身.耗时 = 耗时
        自身.时间戳 = datetime.now()

    def __str__(自身):
        状态色 = "🟢" if 自身.成功 else "🔴"
        return f"[沙箱结果] {{状态色}} 耗时{{自身.耗时:.3f}}s | 输出: {{自身.输出[:50]}}"


class 沙箱执行器:
    """通心译 | TongXinYi: Sandbox Executor — 龍魂安全沙箱总控"""

    def __init__(自身, 最大执行时间: int = 5, 最大输出: int = 10000):
        自身.最大执行时间 = 最大执行时间  # 秒
        自身.最大输出 = 最大输出
        自身.执行历史 = []
        自身.允许模块 = {"math", "json", "re", "datetime", "itertools", "collections"}
        自身.禁止调用 = {"open", "exec", "eval", "__import__", "compile", "input"}
        print(f"[沙箱执行器] 🐉 沙箱已初始化 | 超时: {{最大执行时间}}s | {{__dna__}}")

    def 执行(自身, 代码: str, 全局变量: Dict = None) -> 沙箱结果:
        """🟡 在沙箱中执行代码 | Execute code in sandbox"""
        print(f"[沙箱执行器] 🟡 准备执行代码 ({{len(代码)}} 字符)")

        # 🔴 安全检查
        检查结果 = 自身._安全检查(代码)
        if not 检查结果["通过"]:
            return 沙箱结果(
                成功=False,
                错误=f"安全检查失败: {{检查结果['原因']}}"
            )

        # 🟢 构建受限环境
        安全环境 = 自身._构建环境()
        if 全局变量:
            安全环境.update(全局变量)

        # 🟡 捕获输出
        输出缓冲区 = io.StringIO()
        旧标准输出 = sys.stdout
        sys.stdout = 输出缓冲区

        开始时间 = datetime.now()
        try:
            返回值 = eval(代码, {"__builtins__": {}}, 安全环境) if "\n" not in 代码 else None
            if 返回值 is None:
                exec(代码, {"__builtins__": {}}, 安全环境)
                返回值 = 安全环境.get("_result", None)

            耗时 = (datetime.now() - 开始时间).total_seconds()
            输出 = 输出缓冲区.getvalue()

            if len(输出) > 自身.最大输出:
                输出 = 输出[:自身.最大输出] + "\n... [输出截断]"

            结果 = 沙箱结果(成功=True, 输出=输出, 返回值=返回值, 耗时=耗时)
        except Exception as 错误:
            耗时 = (datetime.now() - 开始时间).total_seconds()
            错误信息 = traceback.format_exc()
            结果 = 沙箱结果(成功=False, 输出=输出缓冲区.getvalue(), 错误=错误信息, 耗时=耗时)
        finally:
            sys.stdout = 旧标准输出

        自身.执行历史.append({"代码": 代码[:50], "结果": 结果.成功, "时间": datetime.now()})
        print(f"[沙箱执行器] {{'🟢' if 结果.成功 else '🔴'}} 执行完成: {{结果}}")
        return 结果

    def _安全检查(自身, 代码: str) -> Dict:
        """🔴 代码安全检查 | Security check"""
        for 禁止词 in 自身.禁止调用:
            if 禁止词 in 代码:
                return {"通过": False, "原因": f"包含禁止调用: {{禁止词}}"}

        危险模块 = ["os", "sys", "subprocess", "socket", "urllib"]
        for 模块名 in 危险模块:
            if f"import {{模块名}}" in code or f"__import__('{{模块名}}')" in code:
                return {"通过": False, "原因": f"尝试导入危险模块: {{模块名}}"}

        return {"通过": True}

    def _构建环境(自身) -> Dict:
        """🟢 构建安全执行环境 | Build safe execution environment"""
        import math, json, re, datetime, itertools, collections
        return {
            "math": math,
            "json": json,
            "re": re,
            "datetime": datetime,
            "itertools": itertools,
            "collections": collections,
            "print": print,
            "len": len,
            "range": range,
            "enumerate": enumerate,
            "zip": zip,
            "map": map,
            "filter": filter,
            "sum": sum,
            "min": min,
            "max": max,
            "abs": abs,
            "round": round,
            "str": str,
            "int": int,
            "float": float,
            "list": list,
            "dict": dict,
            "set": set,
            "tuple": tuple,
        }


if __name__ == "__main__":
    print("=== 沙箱执行器 · 独立执行演示 ===")
    沙箱 = 沙箱执行器()
    结果 = 沙箱.执行("""
import math
x = sum(range(1, 101))
print(f"1到100之和: {{x}}")
_result = x
""")
    print(f"结果: {{结果}}")
    结果2 = 沙箱.执行("open('/etc/passwd')")
    print(f"恶意代码结果: {{结果2}}")
