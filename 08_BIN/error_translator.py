#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-07-06-ERROR-TRANSLATOR-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🌐 龍魂·错误翻译器 — 系统错误中文提示
DNA: #龍芯⚡️2026-07-06-ERROR-TRANSLATOR-v1.0

所有系统错误（I/O error、socket timeout等）自动转换为中文提示。
覆盖 Python 标准库常见异常 + macOS launchctl 错误码 + 自定义错误。

用法:
  直接 import 使用:
    from error_translator import cn_error
    print(cn_error(e))  # 自动翻译异常

  命令行:
    python3 bin/error_translator.py "I/O error: socket timeout"
    python3 bin/error_translator.py --code 5  # launchctl exit code
"""

import re
from typing import Optional

DNA = "#龍芯⚡️2026-07-06-ERROR-TRANSLATOR-v1.0"

# ── 错误翻译映射 ──
ERROR_TRANSLATIONS: dict[str, str] = {
    # I/O 错误
    "I/O error": "输入/输出错误：文件或设备读写失败，请检查磁盘空间和文件权限",
    "Permission denied": "权限不足：当前用户无权访问该文件或端口，请使用 sudo 或检查文件权限",
    "No such file or directory": "文件或目录不存在：请检查路径是否正确",
    "File exists": "文件已存在：该文件/目录已存在，请使用其他名称或先删除",
    "Is a directory": "操作目标为目录：请指定文件路径而非目录路径",

    # Socket / 网络错误
    "Connection refused": "连接被拒绝：目标服务未启动或端口未开放",
    "Connection reset": "连接被重置：目标服务器主动断开连接",
    "Connection timed out": "连接超时：网络不可达或目标服务响应过慢",
    "socket timeout": "网络超时：请检查网络连接或增加超时时间",
    "Network is unreachable": "网络不可达：请检查网络连接",
    "Name or service not known": "域名解析失败：请检查DNS配置或网址是否正确",
    "Address already in use": "端口已被占用：请先终止占用该端口的进程或使用其他端口",

    # 进程/系统错误
    "No such process": "进程不存在：目标进程已退出或PID错误",
    "Cannot allocate memory": "内存不足：系统可用内存不足，请关闭部分应用后重试",
    "Read-only file system": "文件系统只读：无法写入，请检查磁盘挂载状态",

    # Python 特定
    "ModuleNotFoundError": "模块未安装：缺少必要的 Python 包，请运行 pip install 安装",
    "KeyError": "键不存在：字典/配置中缺少必要的键值",
    "ValueError": "值错误：输入的数据格式不正确",
    "TypeError": "类型错误：操作不支持的数据类型",
    "IndexError": "索引越界：列表/数组访问了不存在的索引",
    "AttributeError": "属性不存在：对象没有该属性或方法",
    "ImportError": "导入失败：缺少必要的依赖库",
    "JSONDecodeError": "JSON 格式错误：解析 JSON 数据失败，请检查格式是否正确",
    "FileNotFoundError": "文件未找到：请检查文件路径是否正确",

    # launchctl 错误码
    "Load failed: 1": "系统级服务加载失败（错误码1）：plist 文件路径无效，请检查文件是否存在",
    "Load failed: 2": "系统级服务加载失败（错误码2）：plist 文件语法错误，请运行 lh6 validate plist 检查",
    "Load failed: 3": "系统级服务加载失败（错误码3）：plist 权限错误，请检查文件属主和读写权限",
    "Load failed: 4": "系统级服务加载失败（错误码4）：标签冲突，该服务已经在运行",
    "Load failed: 5": "系统级服务加载失败（错误码5）：I/O 错误，请检查 plist 文件格式及系统权限配置。\n   建议：\n   ① 运行 lh6 validate plist 检查文件完整性\n   ② 使用 bash bin/start_symbiote.sh 手动启动\n   ③ 查看系统日志: log stream --predicate 'subsystem == \"com.apple.launchd\"'",
    "Load failed: 6": "系统级服务加载失败（错误码6）：plist 定义的服务已卸载",
    "Load failed: 7": "系统级服务加载失败（错误码7）：启动失败，请检查 ProgramArguments 中的命令路径",

    # Git 错误
    "fatal: not a git repository": "Git 仓库错误：当前目录不是 Git 仓库",
    "fatal: remote origin already exists": "Git 远程仓库已存在：origin 已被占用",
    "error: failed to push": "Git 推送失败：远程仓库拒绝推送，请检查权限和网络连接",
    "fatal: Authentication failed": "Git 认证失败：用户名或密码/令牌错误",

    # 通用
    "Operation not permitted": "操作被拒绝：系统安全策略阻止了此操作（可能受 SIP 保护）",
    "Broken pipe": "管道中断：接收端已关闭连接",
    "Too many open files": "文件描述符不足：打开的文件过多，请关闭部分文件或增大 ulimit",
}


def cn_error(error) -> str:
    """
    自动翻译异常/错误码为中文提示。

    参数:
        error: 可以是 Exception 对象、字符串、或整数错误码
    返回: 中文错误提示
    """
    if isinstance(error, Exception):
        error_str = str(error)
        error_type = type(error).__name__
    elif isinstance(error, int):
        error_str = f"Load failed: {error}"
        error_type = ""
    else:
        error_str = str(error)
        error_type = ""

    # 1. 完整字符串精确匹配
    if error_str in ERROR_TRANSLATIONS:
        return ERROR_TRANSLATIONS[error_str]

    # 2. 异常类型匹配
    if error_type and error_type in ERROR_TRANSLATIONS:
        base_msg = ERROR_TRANSLATIONS[error_type]
        return f"{base_msg}（详细信息: {error_str}）"

    # 3. 模糊匹配（包含关键词）
    for en, cn in ERROR_TRANSLATIONS.items():
        if en.lower() in error_str.lower():
            return cn

    # 4. 默认：原错误 + 通用提示
    return f"系统错误：{error_str}\n   如无法解决，请运行 lh6 help 寻求帮助"


def cn_launchd_error(code: int) -> str:
    """launchctl 错误码 → 中文提示"""
    key = f"Load failed: {code}"
    return ERROR_TRANSLATIONS.get(key, f"launchctl 加载失败（错误码{code}）：未知错误，请检查 plist 文件和系统日志")


def main():
    import sys

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    if sys.argv[1] == "--code":
        if len(sys.argv) < 3:
            print("❌ 用法: --code <错误码>")
            sys.exit(1)
        code = int(sys.argv[2])
        print(cn_launchd_error(code))
    else:
        error = " ".join(sys.argv[1:])
        print(cn_error(error))


if __name__ == "__main__":
    main()
