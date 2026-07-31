#!/usr/bin/env python3
#龍芯⚡️2026-07-06-BAGUA-ROUTER-v1.0-八卦相重为六十四卦
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║              龍魂 六十四卦路由表 v1.0                                       ║
║              64-Hexagram Routing Engine                                  ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️2026-07-06-BAGUA-ROUTER-v1.0-八卦相重为六十四卦               ║
║  哲学锚: 八卦相重为六十四卦·每卦对应一组命令逻辑                              ║
║  铁律: 所有命令必须归属且仅归属一个卦类                                       ║
╚══════════════════════════════════════════════════════════════════════════╝

架构：
  lh6 <卦类> <动作> [参数...] [--flags]

  卦类：乾/坤/震/巽/坎/离/艮/兑（八卦）
  动作：start/stop/status/list/show/audit...

基于"太极生两仪·两仪生四象·四象生八卦·八卦相重为六十四卦"的哲学模型。

用法:
    from bin.bagua_router import 六十四卦路由表, 执行命令, 注册命令
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union
from enum import Enum
from bin.hetu_luoshu_dna import 八卦映射, 河图洛书_DNA生成, 河图洛书_数字根


# ═══════════════════════════════════════════════════════════
# 命令定义数据结构
# ═══════════════════════════════════════════════════════════

class 命令权限(Enum):
    """命令权限级别"""
    ADMIN = "管理员"     # 需要管理员权限
    USER = "用户"        # 普通用户
    READONLY = "只读"    # 审计只读


@dataclass
class 路由命令:
    """单个路由命令定义"""
    名称: str                          # 动作名（如 start）
    描述: str                          # 中文描述
    处理器: Callable                   # 处理函数
    卦类: str                          # 所属卦类
    权限: 命令权限 = 命令权限.USER
    需要参数: bool = False
    DNA: str = ""                      # DNA追溯码
    权重: int = 60                     # 系统权重


# ═══════════════════════════════════════════════════════════
# 六十四卦路由表
# ═══════════════════════════════════════════════════════════

class 六十四卦路由表:
    """
    六十四卦路由表·八卦相重

    每个卦类作为一个命名空间，内部包含多个动作路由。
    卦象 × 动作 = 六十四卦方位的命令映射。

    结构:
        乾（天）：启动/初始化
        坤（地）：状态/查询
        震（雷）：审计/追溯
        巽（风）：安全/密钥
        坎（水）：主权/命名空间
        离（火）：技能/算法
        艮（山）：同步/配置
        兑（泽）：部署/发布
    """

    def __init__(self):
        self._路由: Dict[str, Dict[str, 路由命令]] = {
            卦名: {} for 卦名 in 八卦映射
        }
        self._全局命令: Dict[str, 路由命令] = {}  # 非八卦直连命令（兼容旧版）

    def 注册(self, 卦类: str, 动作: str, 处理器: Callable,
             描述: str = "", 权限: 命令权限 = 命令权限.USER,
             需要参数: bool = False) -> "六十四卦路由表":
        """
        注册一个命令到八卦路由表

        Args:
            卦类: 八卦之一（乾/坤/震/巽/坎/离/艮/兑）
            动作: 动词（start/stop/status...）
            处理器: 命令处理函数
            描述: 中文描述
            权限: 权限级别
            需要参数: 是否需要参数

        Returns:
            self（支持链式调用）

        Raises:
            ValueError: 卦类无效时
        """
        if 卦类 not in self._路由:
            raise ValueError(f"无效卦类「{卦类}」，必须是: {list(self._路由.keys())}")

        cmd = 路由命令(
            名称=动作,
            描述=描述,
            处理器=处理器,
            卦类=卦类,
            权限=权限,
            需要参数=需要参数,
            DNA=河图洛书_DNA生成(f"{卦类}.{动作}", "SYSTEM"),
        )
        self._路由[卦类][动作] = cmd
        return self

    def 注册全局(self, 名称: str, 处理器: Callable,
                 描述: str = "", 权限: 命令权限 = 命令权限.USER) -> "六十四卦路由表":
        """注册全局命令（非八卦直连，兼容旧版命令）"""
        cmd = 路由命令(
            名称=名称,
            描述=描述,
            处理器=处理器,
            卦类="全局",
            权限=权限,
            DNA=河图洛书_DNA生成(f"global.{名称}", "SYSTEM"),
        )
        self._全局命令[名称] = cmd
        return self

    def 查找(self, 卦类: str, 动作: str) -> Optional[路由命令]:
        """查找路由命令"""
        if 卦类 in self._路由 and 动作 in self._路由[卦类]:
            return self._路由[卦类][动作]
        # 尝试全局命令
        return self._全局命令.get(卦类) or self._全局命令.get(动作)

    def 执行(self, 卦类: str, 动作: str, 参数: Any = None) -> Any:
        """
        执行八卦路由命令

        Args:
            卦类: 八卦之一
            动作: 动词
            参数: 命令参数

        Returns:
            命令执行结果

        Raises:
            ValueError: 命令未找到时
        """
        cmd = self.查找(卦类, 动作)
        if cmd is None:
            # 尝试作为全局命令
            cmd = self._全局命令.get(卦类)
            if cmd:
                return cmd.处理器(动作, 参数)

            raise ValueError(
                f"六十四卦路由未找到：「{卦类}.{动作}」\n"
                f"可用卦类: {list(self._路由.keys())}\n"
                f"可用动作: {list(self._路由.get(卦类, {}).keys()) if 卦类 in self._路由 else '无'}"
            )

        # 生成审计DNA
        dna = 河图洛书_DNA生成(f"{卦类}.{动作}", "UID9622")

        # 执行
        try:
            result = cmd.处理器(参数)
            return {"status": "success", "dna": dna, "result": result}
        except Exception as e:
            return {"status": "error", "dna": dna, "error": str(e)}

    def 列出卦类(self, 卦类: str) -> List[Dict]:
        """列出指定卦类的所有命令"""
        if 卦类 not in self._路由:
            return []
        return [
            {
                "动作": cmd.名称,
                "描述": cmd.描述,
                "权限": cmd.权限.value,
                "DNA": cmd.DNA,
                "权重": cmd.权重,
            }
            for cmd in self._路由[卦类].values()
        ]

    def 列出全部(self) -> Dict[str, List[Dict]]:
        """列出所有卦类的命令"""
        return {
            卦类: self.列出卦类(卦类)
            for 卦类 in self._路由
        }

    def 全部命令列表(self) -> List[Dict]:
        """扁平化列出所有命令"""
        result = []
        for 卦类, commands in self._路由.items():
            卦 = 八卦映射.get(卦类)
            for cmd in commands.values():
                result.append({
                    "卦类": 卦类,
                    "符号": 卦.符号 if 卦 else "",
                    "象": 卦.象 if 卦 else "",
                    "五行": 卦.五行 if 卦 else "",
                    "动作": cmd.名称,
                    "描述": cmd.描述,
                    "DNA": cmd.DNA,
                    "权限": cmd.权限.value,
                })
        return result


# ═══════════════════════════════════════════════════════════
# 全局单例
# ═══════════════════════════════════════════════════════════

# 六十四卦路由表全局实例
路由表 = 六十四卦路由表()


def 执行命令(卦类: str, 动作: str, 参数: Any = None) -> Any:
    """快捷执行函数"""
    return 路由表.执行(卦类, 动作, 参数)


def 注册命令(卦类: str, 动作: str, 处理器: Callable, 描述: str = "") -> 六十四卦路由表:
    """快捷注册函数"""
    return 路由表.注册(卦类, 动作, 处理器, 描述=描述)


# ═══════════════════════════════════════════════════════════
# 预置：八卦命令语义映射
# ═══════════════════════════════════════════════════════════

八卦命令语义 = {
    "乾": {
        "start": "启动系统核心服务",
        "init": "初始化系统环境",
        "boot": "系统引导启动",
        "stop": "停止系统服务",
        "restart": "重启系统服务",
    },
    "坤": {
        "status": "查询系统整体状态",
        "health": "系统健康检查",
        "info": "查看系统信息",
        "list": "列出资源列表",
    },
    "震": {
        "audit": "生成审计日志",
        "dna": "DNA追溯查询",
        "verify": "DNA验证",
        "history": "查看审计历史",
    },
    "巽": {
        "secure": "执行安全校验",
        "cert": "证书管理",
        "encrypt": "数据加密",
        "decrypt": "数据解密",
        "keygen": "密钥生成",
        "keycheck": "密钥检查",
    },
    "坎": {
        "domain": "管理命名空间",
        "ns": "命名空间操作",
        "register": "注册主权身份",
        "verify": "验证身份",
    },
    "离": {
        "skill": "调用扩展工具/技能",
        "algo": "调用预置算法",
        "run": "运行指定任务",
        "list": "列出可用技能/算法",
    },
    "艮": {
        "sync": "同步配置数据",
        "push": "推送更新",
        "pull": "拉取更新",
        "commit": "提交变更",
    },
    "兑": {
        "deploy": "部署服务版本",
        "rollback": "回滚到上一版本",
        "release": "发布版本",
        "validate": "校验部署配置",
    },
}


# ═══════════════════════════════════════════════════════════
# CLI 入口（用于测试和演示）
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("🐉 六十四卦路由表")
        print()
        print("用法:")
        print("  python3 bagua_router.py list              # 列出所有卦类命令语义")
        print("  python3 bagua_router.py show <卦类>       # 显示指定卦类命令")
        print("  python3 bagua_router.py route <卦类> <动作> # 查询路由")
        print()
        print("八卦: 乾·坤·震·巽·坎·离·艮·兑")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "list":
        print("🐉 六十四卦路由表·八卦命令语义")
        print("=" * 60)
        for 卦类, commands in 八卦命令语义.items():
            卦 = 八卦映射.get(卦类)
            if 卦:
                print(f"\n{卦.符号} {卦类}（{卦.象}·{卦.五行}·权重{卦.权重}）")
                print(f"   寓意: {卦.方位}")
                for 动作, 描述 in commands.items():
                    print(f"   ├─ {动作:<12} {描述}")

    elif cmd == "show" and len(sys.argv) >= 3:
        卦类 = sys.argv[2]
        if 卦类 in 八卦命令语义:
            卦 = 八卦映射[卦类]
            print(f"{卦.符号} {卦类}（{卦.象}·{卦.五行}）")
            for 动作, 描述 in 八卦命令语义[卦类].items():
                print(f"  lh6 {卦类} {动作:<12} {描述}")

            # 计算数字根示例
            dr = 河图洛书_数字根(卦类)
            print(f"\n  数字根: {dr}")
        else:
            print(f"未知卦类: {卦类}")

    elif cmd == "route" and len(sys.argv) >= 4:
        卦类 = sys.argv[2]
        动作 = sys.argv[3]
        cmd_info = 路由表.查找(卦类, 动作)
        if cmd_info:
            print(f"✅ 路由命中: lh6 {卦类} {动作}")
            print(f"   描述: {cmd_info.描述}")
            print(f"   权限: {cmd_info.权限.value}")
            print(f"   DNA:  {cmd_info.DNA}")
        else:
            print(f"❌ 路由未命中: lh6 {卦类} {动作}")

    else:
        print(f"未知命令: {cmd}")
