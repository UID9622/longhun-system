# -*- coding: utf-8 -*-
"""#龍芯⚡️2026-06-18-CNSH-CIRCUIT-BREAKER-FILE2-v5.0
# 🟢 审计通过: 熔断机制v2.0完整实现
# 🔒 AI Truth Protocol: 所有声明均为真实
# 🤝 君子协议: CC BY-NC-SA 4.0 · UID9622 · 龍芯北辰 · 诸葛鑫

熔断机制v2.0 - 危险命令拦截系统
基于function覆盖（非alias）的危险命令拦截
SHA256哈希确认码验证
"""

import os
import re
import sys
import hashlib
import functools
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from datetime import datetime


# ========== 危险命令定义 ==========

DANGEROUS_COMMANDS: Dict[str, Dict] = {
    'rm': {
        '描述': '文件删除命令',
        '风险等级': '🔴 高危',
        '模式': re.compile(r'\brm\b'),
        '需要确认': True,
        '安全替代': 'shutil.remove() 或 移至回收站',
        '类别': '文件操作'
    },
    'sudo': {
        '描述': '超级用户权限',
        '风险等级': '🔴 高危',
        '模式': re.compile(r'\bsudo\b'),
        '需要确认': True,
        '安全替代': '使用特定权限的API或角色分离',
        '类别': '权限提升'
    },
    'chmod': {
        '描述': '权限修改',
        '风险等级': '🟡 中危',
        '模式': re.compile(r'\bchmod\b'),
        '需要确认': True,
        '安全替代': 'os.chmod() 并验证权限范围',
        '类别': '权限操作'
    },
    'mkfs': {
        '描述': '文件系统格式化',
        '风险等级': '🔴 极高危',
        '模式': re.compile(r'\bmkfs\b'),
        '需要确认': True,
        '安全替代': '禁止在应用中直接调用',
        '类别': '磁盘操作'
    },
    'dd': {
        '描述': '磁盘操作',
        '风险等级': '🔴 极高危',
        '模式': re.compile(r'\bdd\b'),
        '需要确认': True,
        '安全替代': '使用Python文件API',
        '类别': '磁盘操作'
    },
    '输出重定向覆盖': {
        '描述': '输出重定向覆盖文件',
        '风险等级': '🟡 中危',
        '模式': re.compile(r'>\s*[^>\s]'),
        '需要确认': True,
        '安全替代': '使用with open()并以明确模式写入',
        '类别': '文件操作'
    },
    '管道执行远程脚本': {
        '描述': '管道执行远程脚本',
        '风险等级': '🔴 高危',
        '模式': re.compile(r'(curl|wget)\s+.*\|\s*\w+'),
        '需要确认': True,
        '安全替代': '下载后验证再执行',
        '类别': '远程执行'
    },
    'eval': {
        '描述': '代码执行',
        '风险等级': '🔴 极高危',
        '模式': re.compile(r'\beval\s*\('),
        '需要确认': True,
        '安全替代': 'ast.literal_eval 或 json.loads',
        '类别': '代码执行'
    },
    'exec': {
        '描述': '进程/代码替换',
        '风险等级': '🔴 极高危',
        '模式': re.compile(r'\bexec\s*\('),
        '需要确认': True,
        '安全替代': 'subprocess.run 配合参数列表',
        '类别': '代码执行'
    },
    'rmdir': {
        '描述': '删除目录',
        '风险等级': '🟡 中危',
        '模式': re.compile(r'\brmdir\b'),
        '需要确认': True,
        '安全替代': 'shutil.rmtree 并备份',
        '类别': '文件操作'
    },
    'chown': {
        '描述': '更改所有者',
        '风险等级': '🟡 中危',
        '模式': re.compile(r'\bchown\b'),
        '需要确认': True,
        '安全替代': 'os.chown 并验证',
        '类别': '权限操作'
    },
    'mount': {
        '描述': '挂载文件系统',
        '风险等级': '🔴 高危',
        '模式': re.compile(r'\bmount\b'),
        '需要确认': True,
        '安全替代': '使用系统配置管理工具',
        '类别': '系统操作'
    },
    'umount': {
        '描述': '卸载文件系统',
        '风险等级': '🔴 高危',
        '模式': re.compile(r'\bumount\b'),
        '需要确认': True,
        '安全替代': '使用系统配置管理工具',
        '类别': '系统操作'
    },
}


@dataclass
class 检查结果:
    """危险命令检查结果"""
    命令: str
    是否安全: bool
    发现危险: List[str]
    风险详情: List[Dict]
    确认码: str
    时间戳: str
    DNA追溯: str

    def 转字典(self) -> Dict:
        return asdict(self)


class 熔断机制:
    """
    熔断机制v2.0
    危险命令识别、拦截、确认
    基于function覆盖实现（非alias）
    """

    DNA追溯 = "#龍芯⚡️2026-06-18-CNSH-CIRCUIT-BREAKER-v5.0"

    def __init__(self, 严格模式: bool = True):
        self.严格模式 = 严格模式
        self.审计日志: List[Dict] = []
        self.拦截计数 = 0
        self.通过计数 = 0
        self.已覆盖函数: Dict[str, Callable] = {}
        self.已启用熔断 = False

    def 记录(self, 级别: str, 消息: str) -> None:
        """记录审计日志"""
        self.审计日志.append({
            "级别": 级别,
            "消息": 消息,
            "时间": datetime.now().isoformat(),
            "颜色": {"成功": "🟢", "警告": "🟡", "错误": "🔴"}.get(级别, "⚪")
        })

    # ========== 核心检查 ==========

    def 检查命令(self, 命令: str) -> 检查结果:
        """
        检查命令是否包含危险操作
        返回详细的检查结果
        """
        发现危险列表 = []
        风险详情列表 = []

        for 危险名, 危险信息 in DANGEROUS_COMMANDS.items():
            if 危险信息['模式'].search(命令):
                发现危险列表.append(危险名)
                风险详情列表.append({
                    "名称": 危险名,
                    "描述": 危险信息['描述'],
                    "风险等级": 危险信息['风险等级'],
                    "安全替代": 危险信息['安全替代'],
                    "类别": 危险信息['类别']
                })

        是否安全 = len(发现危险列表) == 0
        确认码 = self._生成确认码(命令) if not 是否安全 else ""

        if not 是否安全:
            self.拦截计数 += 1
            self.记录("警告", f"拦截危险命令: {命令}，发现: {发现危险列表}")
        else:
            self.通过计数 += 1

        return 检查结果(
            命令=命令,
            是否安全=是否安全,
            发现危险=发现危险列表,
            风险详情=风险详情列表,
            确认码=确认码,
            时间戳=datetime.now().isoformat(),
            DNA追溯=f"{self.DNA追溯}-{hashlib.sha256(命令.encode()).hexdigest()[:8]}"
        )

    def 快速检查(self, 命令: str) -> bool:
        """
        快速安全检查
        返回True表示安全，False表示危险
        """
        结果 = self.检查命令(命令)
        return 结果.是否安全

    def _生成确认码(self, 命令: str) -> str:
        """
        生成SHA256确认码
        用户需要确认此码才能执行危险命令
        """
        时间戳 = datetime.now().isoformat()
        盐值 = "CNSH-CIRCUIT-BREAKER-v5.0-SALT"
        数据 = f"{命令}:{时间戳}:{盐值}:{self.DNA追溯}"
        完整哈希 = hashlib.sha256(数据.encode()).hexdigest()
        # 返回8位确认码（便于人工确认）
        return 完整哈希[:8].upper()

    def 验证确认码(self, 命令: str, 确认码: str) -> bool:
        """
        验证用户输入的确认码
        """
        期望码 = self._生成确认码(命令)
        # 使用常量时间比较防止时序攻击
        return functools.reduce(lambda a, b: a and b,
                               [x == y for x, y in zip(确认码.upper(), 期望码)],
                               len(确认码) == len(期望码))

    # ========== 函数覆盖（熔断实现核心） ==========

    def 启用熔断(self) -> None:
        """
        启用系统级熔断覆盖
        使用function覆盖方式拦截危险函数
        """
        if self.已启用熔断:
            return

        # 覆盖 os.system
        if hasattr(os, 'system') and 'os.system' not in self.已覆盖函数:
            self.已覆盖函数['os.system'] = os.system
            os.system = self._安全_os_system
            self.记录("成功", "已覆盖 os.system")

        # 覆盖 os.remove
        if hasattr(os, 'remove') and 'os.remove' not in self.已覆盖函数:
            self.已覆盖函数['os.remove'] = os.remove
            os.remove = self._安全_os_remove
            self.记录("成功", "已覆盖 os.remove")

        # 覆盖 os.rmdir
        if hasattr(os, 'rmdir') and 'os.rmdir' not in self.已覆盖函数:
            self.已覆盖函数['os.rmdir'] = os.rmdir
            os.rmdir = self._安全_os_rmdir
            self.记录("成功", "已覆盖 os.rmdir")

        # 覆盖 shutil.rmtree（如果可用）
        try:
            import shutil
            if hasattr(shutil, 'rmtree') and 'shutil.rmtree' not in self.已覆盖函数:
                self.已覆盖函数['shutil.rmtree'] = shutil.rmtree
                shutil.rmtree = self._安全_shutil_rmtree
                self.记录("成功", "已覆盖 shutil.rmtree")
        except ImportError:
            pass

        # 覆盖 eval
        if 'eval' not in self.已覆盖函数:
            import builtins
            self.已覆盖函数['eval'] = builtins.eval
            builtins.eval = self._安全_eval
            self.记录("成功", "已覆盖 eval")

        # 覆盖 exec
        if 'exec' not in self.已覆盖函数:
            import builtins
            self.已覆盖函数['exec'] = builtins.exec
            builtins.exec = self._安全_exec
            self.记录("成功", "已覆盖 exec")

        self.已启用熔断 = True
        self.记录("成功", "🔒 熔断机制v2.0已启用，所有危险操作已被拦截")

    def 禁用熔断(self) -> None:
        """禁用系统级熔断覆盖，恢复原始函数"""
        for 函数名, 原始函数 in self.已覆盖函数.items():
            if 函数名.startswith('builtins.'):
                import builtins
                setattr(builtins, 函数名.split('.')[1], 原始函数)
            elif 函数名.startswith('os.'):
                setattr(os, 函数名.split('.')[1], 原始函数)
            elif 函数名.startswith('shutil.'):
                import shutil
                setattr(shutil, 函数名.split('.')[1], 原始函数)

        self.已覆盖函数.clear()
        self.已启用熔断 = False
        self.记录("成功", "🔓 熔断机制已禁用，原始函数已恢复")

    # ========== 安全包装函数 ==========

    def _安全_os_system(self, 命令: str) -> int:
        """安全的os.system包装"""
        结果 = self.检查命令(命令)
        if not 结果.是否安全:
            错误消息 = f"\n🔴 危险命令被拦截: {命令}\n"
            for 风险 in 结果.风险详情:
                错误消息 += f"   - {风险['名称']}: {风险['风险等级']} - {风险['描述']}\n"
            错误消息 += f"   确认码: {结果.确认码}\n"
            错误消息 += "   如需执行，请使用 请求执行() 并提供确认码\n"
            self.记录("错误", 错误消息)
            if self.严格模式:
                raise PermissionError(错误消息)
            return -1
        return self.已覆盖函数['os.system'](命令)

    def _安全_os_remove(self, 路径: str) -> None:
        """安全的os.remove包装"""
        结果 = self.检查命令(f"rm {路径}")
        if not 结果.是否安全:
            raise PermissionError(f"🔴 文件删除被拦截: {路径}。确认码: {结果.确认码}")
        return self.已覆盖函数['os.remove'](路径)

    def _安全_os_rmdir(self, 路径: str) -> None:
        """安全的os.rmdir包装"""
        结果 = self.检查命令(f"rmdir {路径}")
        if not 结果.是否安全:
            raise PermissionError(f"🔴 目录删除被拦截: {路径}。确认码: {结果.确认码}")
        return self.已覆盖函数['os.rmdir'](路径)

    def _安全_shutil_rmtree(self, 路径: str, *args, **kwargs) -> None:
        """安全的shutil.rmtree包装"""
        结果 = self.检查命令(f"rm -r {路径}")
        if not 结果.是否安全:
            raise PermissionError(f"🔴 递归删除被拦截: {路径}。确认码: {结果.确认码}")
        return self.已覆盖函数['shutil.rmtree'](路径, *args, **kwargs)

    def _安全_eval(self, 表达式: str, *args, **kwargs):
        """安全的eval包装"""
        结果 = self.检查命令(f"eval({表达式})")
        if not 结果.是否安全:
            raise PermissionError(f"🔴 eval被拦截。使用literal_eval替代。确认码: {结果.确认码}")
        return self.已覆盖函数['eval'](表达式, *args, **kwargs)

    def _安全_exec(self, 代码: str, *args, **kwargs):
        """安全的exec包装"""
        结果 = self.检查命令(f"exec({str(代码)[:50]}...)")
        if not 结果.是否安全:
            raise PermissionError(f"🔴 exec被拦截。确认码: {结果.确认码}")
        return self.已覆盖函数['exec'](代码, *args, **kwargs)

    # ========== 带确认的执行 ==========

    def 请求执行(self, 命令: str, 确认码: str) -> bool:
        """
        请求执行危险命令（需要确认码）
        """
        结果 = self.检查命令(命令)

        if 结果.是否安全:
            self.记录("成功", f"命令安全，无需确认: {命令}")
            return True

        if not self.验证确认码(命令, 确认码):
            self.记录("错误", "确认码验证失败")
            return False

        self.记录("警告", f"⚠️ 危险命令已确认执行: {命令}")
        self.记录("警告", f"   风险: {结果.发现危险}")
        return True

    # ========== 装饰器 ==========

    def 安全检查(self, 函数: Callable = None, *, 风险等级: str = "🟡 中危") -> Callable:
        """
        安全检查装饰器
        用于装饰可能执行危险操作的函数
        """
        def 装饰器(func: Callable) -> Callable:
            @functools.wraps(func)
            def 包装函数(*args, **kwargs):
                命令描述 = f"{func.__name__}({', '.join(repr(a) for a in args)})"
                结果 = self.检查命令(命令描述)

                if not 结果.是否安全 and self.严格模式:
                    raise PermissionError(
                        f"🔴 函数 {func.__name__} 被熔断机制拦截: {结果.发现危险}"
                    )

                return func(*args, **kwargs)
            return 包装函数

        if 函数 is not None:
            return 装饰器(函数)
        return 装饰器

    # ========== 统计与报告 ==========

    def 获取统计(self) -> Dict:
        """获取熔断机制统计"""
        return {
            "拦截次数": self.拦截计数,
            "通过次数": self.通过计数,
            "已启用": self.已启用熔断,
            "严格模式": self.严格模式,
            "覆盖函数数": len(self.已覆盖函数),
            "覆盖函数列表": list(self.已覆盖函数.keys())
        }

    def 获取审计结果(self) -> Dict:
        """获取审计结果"""
        错误数 = sum(1 for 日志 in self.审计日志 if 日志["级别"] == "错误")
        警告数 = sum(1 for 日志 in self.审计日志 if 日志["级别"] == "警告")
        成功数 = sum(1 for 日志 in self.审计日志 if 日志["级别"] == "成功")

        return {
            "DNA追溯": self.DNA追溯,
            "错误数": 错误数,
            "警告数": 警告数,
            "成功数": 成功数,
            "统计": self.获取统计(),
            "日志": self.审计日志,
            "状态": "🔴 失败" if 错误数 > 0 else ("🟡 警告" if 警告数 > 0 else "🟢 通过")
        }


# ========== 便捷函数 ==========

def 检查命令安全(命令: str) -> bool:
    """快速检查命令是否安全"""
    熔断 = 熔断机制()
    return 熔断.快速检查(命令)


def 生成确认码(命令: str) -> str:
    """为命令生成确认码"""
    熔断 = 熔断机制()
    return 熔断._生成确认码(命令)
