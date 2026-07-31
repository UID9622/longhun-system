#龍芯⚡️2026-06-18-CNSH-hooks-钩子管理器-v1.0
"""
通心译 | TongXinYi: Hook Manager
龍魂体系·生命周期钩子管理器 — 系统各阶段钩子注册与执行

支持多种钩子点：系统启动前、启动后、关闭前、关闭后、配置变更等
Supports multiple hook points: pre_start, post_start, pre_stop, post_stop, config_change
"""
# 🟢 君子协议 | JunZi Protocol: CC BY-NC-SA 4.0
# 🟡 AI Truth Protocol: All outputs must be verifiable and traceable
# 🔴 DNA Trace: #龍芯⚡️2026-06-18-CNSH-hooks-钩子管理器-v1.0

from datetime import datetime
from typing import Any, Dict, List, Callable

__版本__ = "v1.0"
__dna__ = "#龍芯⚡️2026-06-18-CNSH-hooks-钩子管理器-v1.0"


class 钩子类型:
    """通心译 | TongXinYi: Hook Types — 预定义钩子类型常量"""
    系统启动前 = "pre_start"
    系统启动后 = "post_start"
    系统关闭前 = "pre_stop"
    系统关闭后 = "post_stop"
    配置变更 = "config_change"
    模块加载 = "module_load"
    审计触发 = "audit_trigger"
    错误发生 = "error_occurred"


class 钩子记录:
    """通心译 | TongXinYi: Hook Record — 钩子执行记录"""

    def __init__(自身, 钩子名: str, 处理器: Callable):
        自身.钩子名 = 钩子名
        自身.处理器 = 处理器
        自身.调用次数 = 0
        自身.上次调用 = None
        自身.是否启用 = True


class 钩子管理器:
    """通心译 | TongXinYi: Hook Manager — 龍魂生命周期钩子总控"""

    def __init__(自身):
        自身.钩子字典: Dict[str, List[钩子记录]] = {}
        自身.执行历史 = []
        print(f"[钩子管理器] 🐉 钩子管理器已初始化 | {{__dna__}}")

    def 注册钩子(自身, 钩子类型: str, 处理器: Callable, 覆盖: bool = False):
        """🟢 注册生命周期钩子 | Register a lifecycle hook"""
        if 钩子类型 not in 自身.钩子字典:
            自身.钩子字典[钩子类型] = []

        if 覆盖:
            自身.钩子字典[钩子类型] = []

        记录 = 钩子记录(钩子类型, 处理器)
        自身.钩子字典[钩子类型].append(记录)
        print(f"[钩子管理器] 🟢 注册钩子: {{钩子类型}} -> {{处理器.__name__}}")

    def 注销钩子(自身, 钩子类型: str, 处理器: Callable):
        """🟡 注销生命周期钩子 | Unregister a lifecycle hook"""
        if 钩子类型 in 自身.钩子字典:
            自身.钩子字典[钩子类型] = [
                r for r in 自身.钩子字典[钩子类型] if r.处理器 != 处理器
            ]
            print(f"[钩子管理器] 🟡 注销钩子: {{钩子类型}} -> {{处理器.__name__}}")

    def 执行钩子(自身, 钩子类型: str, 数据=None) -> List[Any]:
        """🟡 执行指定类型的所有钩子 | Execute all hooks of given type"""
        结果列表 = []

        if 钩子类型 not in 自身.钩子字典:
            return 结果列表

        print(f"[钩子管理器] 🟡 执行钩子: {{钩子类型}} ({{len(自身.钩子字典[钩子类型])}} 个)")

        for 记录 in 自身.钩子字典[钩子类型]:
            if not 记录.是否启用:
                continue
            try:
                结果 = 记录.处理器(数据)
                记录.调用次数 += 1
                记录.上次调用 = datetime.now()
                结果列表.append(结果)
                print(f"[钩子管理器] 🟢 钩子执行成功: {{记录.处理器.__name__}}")
            except Exception as 错误:
                print(f"[钩子管理器] 🔴 钩子执行失败: {{记录.处理器.__name__}}: {{错误}}")

        自身.执行历史.append({"类型": 钩子类型, "时间": datetime.now(), "结果数": len(结果列表)})
        return 结果列表

    def 获取钩子列表(自身) -> List[str]:
        """🟢 获取已注册的所有钩子类型 | Get all registered hook types"""
        return list(自身.钩子字典.keys())

    def 打印钩子表(自身):
        """🟢 打印当前钩子注册表 | Print current hook registry"""
        print("=" * 50)
        print("龍魂钩子注册表 | LongHun Hook Registry")
        print("=" * 50)
        for 钩子类型, 记录列表 in 自身.钩子字典.items():
            for 记录 in 记录列表:
                状态色 = "🟢" if 记录.是否启用 else "🟡"
                print(f"  {{状态色}} {{钩子类型:20s}} -> {{记录.处理器.__name__:20s}} (已调用{{记录.调用次数}}次)")
        print("=" * 50)


if __name__ == "__main__":
    print("=== 钩子管理器 · 独立执行演示 ===")
    管理器 = 钩子管理器()

    def 启动日志(数据):
        print(f"  [钩子] 记录启动日志: {{数据}}")
        return "done"

    def 检查更新(数据):
        print(f"  [钩子] 检查更新...")
        return "checked"

    管理器.注册钩子(钩子类型.系统启动后, 启动日志)
    管理器.注册钩子(钩子类型.系统启动后, 检查更新)
    管理器.打印钩子表()
    管理器.执行钩子(钩子类型.系统启动后, {"模块": "runtime"})
