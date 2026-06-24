#龍芯⚡️2026-06-18-CNSH-adapters-接口适配器-v1.0
"""
通心译 | TongXinYi: Interface Adapter
龍魂体系·接口适配器 — 外部系统与龍魂核心的统一适配层

将不同外部接口统一转换为CNSH内部标准格式，实现无缝集成
Unifies external interfaces into CNSH internal standard format for seamless integration
"""
# 🟢 君子协议 | JunZi Protocol: CC BY-NC-SA 4.0
# 🟡 AI Truth Protocol: All outputs must be verifiable and traceable
# 🔴 DNA Trace: #龍芯⚡️2026-06-18-CNSH-adapters-接口适配器-v1.0

from datetime import datetime
from typing import Dict, Any, Callable, List

__版本__ = "v1.0"
__dna__ = "#龍芯⚡️2026-06-18-CNSH-adapters-接口适配器-v1.0"


class 接口适配器:
    """通心译 | TongXinYi: Interface Adapter — 龍魂统一接口适配总控"""

    def __init__(自身):
        自身.适配器字典 = {}
        自身.转换记录 = []
        自身.失败计数 = 0
        print(f"[接口适配器] 🐉 接口适配器已初始化 | {{__dna__}}")

    def 注册适配器(自身, 源格式: str, 目标格式: str, 转换函数: Callable) -> str:
        """🟢 注册格式转换适配器 | Register format conversion adapter"""
        适配器ID = f"{{源格式}}_to_{{目标格式}}"
        自身.适配器字典[适配器ID] = {
            "ID": 适配器ID,
            "源格式": 源格式,
            "目标格式": 目标格式,
            "转换函数": 转换函数,
            "注册时间": datetime.now(),
            "调用次数": 0
        }
        print(f"[接口适配器] 🟢 适配器已注册: {{源格式}} -> {{目标格式}}")
        return 适配器ID

    def 转换(自身, 数据: Any, 源格式: str, 目标格式: str) -> Any:
        """🟡 执行格式转换 | Execute format conversion"""
        适配器ID = f"{{源格式}}_to_{{目标格式}}"

        if 适配器ID not in 自身.适配器字典:
            # 🟡 尝试通用适配
            结果 = 自身._通用转换(数据, 源格式, 目标格式)
            if 结果 is not None:
                return 结果

            print(f"[接口适配器] 🔴 未找到适配器: {{适配器ID}}")
            自身.失败计数 += 1
            return None

        适配器 = 自身.适配器字典[适配器ID]
        try:
            结果 = 适配器["转换函数"](数据)
            适配器["调用次数"] += 1
            自身.转换记录.append({
                "时间": datetime.now(),
                "适配器": 适配器ID,
                "数据大小": len(str(数据))
            })
            print(f"[接口适配器] 🟢 转换成功: {{源格式}} -> {{目标格式}}")
            return 结果
        except Exception as 错误:
            自身.失败计数 += 1
            print(f"[接口适配器] 🔴 转换失败: {{错误}}")
            return None

    def _通用转换(自身, 数据: Any, 源格式: str, 目标格式: str) -> Any:
        """🟡 通用转换规则 | Generic conversion rules"""
        # JSON ↔ Dict 转换
        if 源格式 == "json" and 目标格式 == "dict":
            import json
            return json.loads(数据)
        elif 源格式 == "dict" and 目标格式 == "json":
            import json
            return json.dumps(数据, ensure_ascii=False)
        # String ↔ Bytes 转换
        elif 源格式 == "str" and 目标格式 == "bytes":
            return 数据.encode("utf-8")
        elif 源格式 == "bytes" and 目标格式 == "str":
            return 数据.decode("utf-8")
        return None

    def 获取适配器列表(自身) -> List[Dict]:
        """🟢 获取所有注册适配器 | Get all registered adapters"""
        return list(自身.适配器字典.values())

    def 打印适配器表(自身):
        """🟢 打印适配器注册表 | Print adapter registry"""
        print("=" * 50)
        print("接口适配器注册表 | Interface Adapter Registry")
        print("=" * 50)
        for 适配器 in 自身.适配器字典.values():
            print(f"  🟢 {{适配器['源格式']:10s}} -> {{适配器['目标格式']:10s}} | "
                  f"调用{{适配器['调用次数']}}次")
        print("=" * 50)

    def 获取统计(自身) -> Dict:
        """🟡 获取适配器统计 | Get adapter statistics"""
        return {
            "注册适配器": len(自身.适配器字典),
            "转换次数": len(自身.转换记录),
            "失败次数": 自身.失败计数,
            "成功率": f"{{(1 - 自身.失败计数/max(len(自身.转换记录)+自身.失败计数,1))*100:.1f}}%"
        }


if __name__ == "__main__":
    print("=== 接口适配器 · 独立执行演示 ===")
    适配器 = 接口适配器()

    def 自定义转换(数据):
        return {"转换后": 数据, "时间": str(datetime.now())}

    适配器.注册适配器("notion", "cnsh", 自定义转换)
    结果 = 适配器.转换({"page": "test"}, "notion", "cnsh")
    print(f"转换结果: {{结果}}")

    # 测试通用转换
    json数据 = '{"龍魂": "CNSH"}'
    dict数据 = 适配器.转换(json数据, "json", "dict")
    print(f"JSON转Dict: {{dict数据}}")

    适配器.打印适配器表()
    print(f"统计: {{适配器.获取统计()}}")
