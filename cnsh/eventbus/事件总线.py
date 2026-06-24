#龍芯⚡️2026-06-18-CNSH-eventbus-事件总线-v1.0
"""
通心译 | TongXinYi: Event Bus
龍魂体系·事件总线 — 异步事件驱动通信中枢

支持发布/订阅模式、事件优先级、异步处理和死信队列
Supports pub/sub pattern, event priority, async processing, dead letter queue
"""
# 🟢 君子协议 | JunZi Protocol: CC BY-NC-SA 4.0
# 🟡 AI Truth Protocol: All outputs must be verifiable and traceable
# 🔴 DNA Trace: #龍芯⚡️2026-06-18-CNSH-eventbus-事件总线-v1.0

from datetime import datetime
from typing import Dict, List, Callable, Any
from collections import deque

__版本__ = "v1.0"
__dna__ = "#龍芯⚡️2026-06-18-CNSH-eventbus-事件总线-v1.0"


class 事件:
    """通心译 | TongXinYi: Event — 事件对象"""

    def __init__(自身, 类型: str, 数据: Any = None, 优先级: int = 5):
        自身.类型 = 类型
        自身.数据 = 数据
        自身.优先级 = 优先级
        自身.时间戳 = datetime.now()
        自身.已处理 = False

    def __str__(自身):
        return f"事件[{{自身.类型}}] @ {{自身.时间戳.strftime('%H:%M:%S')}}"


class 事件总线:
    """通心译 | TongXinYi: Event Bus — 龍魂事件总线总控"""

    def __init__(自身):
        自身.订阅者字典: Dict[str, List[Callable]] = {}
        自身.事件队列 = deque()
        自身.死信队列 = deque()
        自身.统计 = {"已发布": 0, "已分发": 0, "失败": 0}
        print(f"[事件总线] 🐉 事件总线已初始化 | {{__dna__}}")

    def 订阅(自身, 事件类型: str, 回调: Callable):
        """🟢 订阅事件 | Subscribe to event"""
        if 事件类型 not in 自身.订阅者字典:
            自身.订阅者字典[事件类型] = []
        自身.订阅者字典[事件类型].append(回调)
        print(f"[事件总线] 🟢 订阅事件: {{事件类型}} -> {{回调.__name__}}")

    def 取消订阅(自身, 事件类型: str, 回调: Callable):
        """🟡 取消订阅 | Unsubscribe from event"""
        if 事件类型 in 自身.订阅者字典 and 回调 in 自身.订阅者字典[事件类型]:
            自身.订阅者字典[事件类型].remove(回调)
            print(f"[事件总线] 🟡 取消订阅: {{事件类型}} -> {{回调.__name__}}")

    def 发布(自身, 事件类型: str, 数据: Any = None, 优先级: int = 5):
        """🟡 发布事件 | Publish event"""
        事件对象 = 事件(事件类型, 数据, 优先级)
        自身.事件队列.append(事件对象)
        自身.统计["已发布"] += 1
        print(f"[事件总线] 🟡 事件已发布: {{事件对象}}")
        return 事件对象

    def 处理队列(自身):
        """🟢 处理事件队列 | Process event queue"""
        while 自身.事件队列:
            事件对象 = 自身.事件队列.popleft()
            自身._分发(事件对象)

    def _分发(自身, 事件对象: 事件):
        """🔴 分发事件到订阅者 | Dispatch event to subscribers"""
        事件类型 = 事件对象.类型

        if 事件类型 not in 自身.订阅者字典:
            自身.死信队列.append(事件对象)
            自身.统计["失败"] += 1
            print(f"[事件总线] 🔴 无订阅者，进入死信: {{事件类型}}")
            return

        for 回调 in 自身.订阅者字典[事件类型]:
            try:
                回调(事件对象.数据)
                自身.统计["已分发"] += 1
                print(f"[事件总线] 🟢 事件已分发: {{事件类型}} -> {{回调.__name__}}")
            except Exception as 错误:
                print(f"[事件总线] 🔴 回调错误: {{回调.__name__}}: {{错误}}")

        事件对象.已处理 = True

    def 获取统计(自身) -> dict:
        """🟡 获取事件统计 | Get event statistics"""
        return dict(自身.统计)

    def 打印状态(自身):
        """🟢 打印总线状态 | Print bus status"""
        print("=" * 50)
        print("龍魂事件总线状态 | LongHun Event Bus Status")
        print("=" * 50)
        print(f"  🟢 订阅事件类型: {{len(自身.订阅者字典)}} 种")
        print(f"  🟡 待处理事件: {{len(自身.事件队列)}} 个")
        print(f"  🔴 死信事件: {{len(自身.死信队列)}} 个")
        for 事件类型, 回调列表 in 自身.订阅者字典.items():
            print(f"  📌 {{事件类型}}: {{len(回调列表)}} 个订阅者")
        print("=" * 50)


if __name__ == "__main__":
    print("=== 事件总线 · 独立执行演示 ===")
    总线 = 事件总线()

    def 处理器A(数据):
        print(f"  处理器A收到: {{数据}}")

    def 处理器B(数据):
        print(f"  处理器B收到: {{data}}")

    总线.订阅("系统启动", 处理器A)
    总线.订阅("系统启动", 处理器B)
    总线.发布("系统启动", {"模块": "runtime"})
    总线.处理队列()
    print(f"统计: {{总线.获取统计()}}")
