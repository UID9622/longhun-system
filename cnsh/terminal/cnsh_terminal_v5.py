#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷔噬嗑-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""#龍芯⚡️丙午·甲午·癸亥·戊午·䷚颐-CNSH-TERMINAL-FILE6-v5.0
# 🟢 审计通过: CNSH多语言编辑器终端v5.0 主程序
# 🔒 AI Truth Protocol: 所有声明均为真实
# 🤝 君子协议: CC BY-NC-SA 4.0 · UID9622 · 龍芯北辰 · 诸葛鑫

CNSH多语言编辑器终端v5.0 主程序入口
中文编程语言 · 繁体龍字永存 · 通心译翻译器 · 中央藏经阁

使用方式:
    python cnsh_terminal_v5.py [命令] [参数]

命令:
    gui              启动图形界面编辑器
    compile [文件]   编译.cnsh文件到C
    lex [文件]       执行词法分析
    parse [文件]     执行语法分析
    translate        启动翻译模式
    encrypt          启动加密模式
    audit            显示审计报告
    check [文件]     执行四层检查
    协议             显示龍魂系统使用协议
    version          显示版本信息
    help             显示帮助

示例:
    python cnsh_terminal_v5.py gui
    python cnsh_terminal_v5.py compile 示例.cnsh
    python cnsh_terminal_v5.py check 示例.cnsh
"""

import os
import sys
import json
import argparse

# 确保模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.lexer import Lexer
from modules.parser import Parser, 解析源代码
from modules.code_generator import CCodeGenerator, 生成C代码
from modules.translator import 通心译翻译器, 快速翻译
from modules.terminology_bank import 中央藏经阁
from modules.encryption import 点对点加密
from modules.circuit_breaker import 熔断机制
from modules.ai_timestamp import AI时间戳规范
from modules.four_layer_check import CNSH四层检查, 快速四层检查
from modules.audit_integration import 联动审计, 操作类型


# ========== 全局审计系统 ==========
审计系统 = 联动审计()

# DNA追溯码
DNA追溯 = "#龍芯⚡️丙午·甲午·癸亥·戊午·䷚颐-CNSH-TERMINAL-v5.0"
版本 = "5.0.0"
作者 = "龍芯北辰 · 诸葛鑫"
UID = "UID9622"
许可 = "CC BY-NC-SA 4.0"


def 打印标题():
    """打印程序标题"""
    标题 = f"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🐉 CNSH 多语言编辑器终端 v{版本}                           ║
║      Chinese Native Script Host Terminal                         ║
║                                                                  ║
║   {DNA追溯}                          ║
║                                                                  ║
║   中文编程语言 · 繁体龍字永存 · 通心译 · 中央藏经阁              ║
║   创始人: {UID} · {作者}                              ║
║   许可: {许可} (君子协议)                         ║
║   🔒 AI Truth Protocol: 所有声明均为真实                          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(标题)


def 打印版本信息():
    """打印版本信息"""
    打印标题()
    print(f"版本: {版本}")
    print(f"DNA追溯: {DNA追溯}")
    print(f"作者: {作者}")
    print(f"UID: {UID}")
    print(f"许可: {许可}")
    print(f"AI Truth Protocol: 已启用")
    print()


def 打印帮助信息():
    """打印帮助信息"""
    打印标题()
    print("""使用方式: python cnsh_terminal_v5.py [命令] [参数]

命令:
    gui                          启动图形界面编辑器 (tkinter)
    compile  <文件.cnsh>          编译CNSH文件到C
    lex      <文件.cnsh>          执行词法分析并显示Token
    parse    <文件.cnsh>          执行语法分析并显示AST
    check    <文件.cnsh>          执行四层检查
    translate <文本>              启动翻译模式
    encrypt  <文本>              加密文本
    decrypt  <密文>              解密文本
    audit                        显示审计报告
    协议                         显示龍魂系统使用协议（大白话）
    version                      显示版本信息
    help                         显示此帮助

示例:
    python cnsh_terminal_v5.py gui
    python cnsh_terminal_v5.py compile 示例.cnsh
    python cnsh_terminal_v5.py lex 示例.cnsh
    python cnsh_terminal_v5.py translate "Prompt Engineering"
    python cnsh_terminal_v5.py encrypt "敏感信息"
""")


def 读取文件(文件路径: str) -> str:
    """读取文件内容"""
    try:
        with open(文件路径, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"🔴 错误: 无法读取文件 '{文件路径}': {e}")
        sys.exit(1)


# ========== 命令处理函数 ==========

def 命令_gui(参数):
    """启动图形界面编辑器"""
    try:
        from modules.editor_ui import CNSH编辑器
        print("🟢 启动CNSH图形界面编辑器...")
        编辑器 = CNSH编辑器()
        编辑器.run()
    except ImportError as e:
        print(f"🔴 错误: 无法启动图形界面: {e}")
        print("🟡 提示: 请确保已安装 tkinter")
        sys.exit(1)


def 命令_compile(参数):
    """编译CNSH文件到C"""
    if not 参数.文件:
        print("🔴 错误: 请指定要编译的文件")
        sys.exit(1)

    文件路径 = 参数.文件[0]
    代码 = 读取文件(文件路径)

    print(f"🟢 正在编译: {文件路径}")
    print("=" * 60)

    try:
        AST = 解析源代码(代码)
        C代码 = 生成C代码(AST)

        # 保存C文件
        C文件路径 = 文件路径.replace(".cnsh", ".c")
        with open(C文件路径, 'w', encoding='utf-8') as f:
            f.write(C代码)

        print(C代码[:2000])  # 打印前2000字符
        if len(C代码) > 2000:
            print(f"... (共 {len(C代码)} 字符，完整代码已保存到 {C文件路径})")

        print(f"\n🟢 编译成功! C代码已保存: {C文件路径}")
        审计系统.成功(操作类型.编译, "终端", f"编译成功: {文件路径} → {C文件路径}")

    except Exception as e:
        print(f"🔴 编译失败: {e}")
        审计系统.错误(操作类型.编译, "终端", str(e))
        sys.exit(1)


def 命令_lex(参数):
    """词法分析"""
    if not 参数.文件:
        print("🔴 错误: 请指定要分析的文件")
        sys.exit(1)

    文件路径 = 参数.文件[0]
    代码 = 读取文件(文件路径)

    print(f"🟢 词法分析: {文件路径}")
    print("=" * 60)

    分析器 = Lexer(代码)
    标记列表 = 分析器.词法分析()

    print(f"Token总数: {len(标记列表)}")
    print("-" * 60)
    for i, 标记 in enumerate(标记列表[:50]):
        print(f"  [{i:4d}] {标记.类型.name:20s} '{标记.值}' (行{标记.行号}, 列{标记.列号})")
    if len(标记列表) > 50:
        print(f"  ... 共 {len(标记列表)} 个Token")

    # 审计结果
    审计 = 分析器.获取审计结果()
    print(f"\n{审计['状态']} 错误:{审计['错误数']} 警告:{审计['警告数']}")

    审计系统.成功(操作类型.编译, "词法分析", f"Token数: {len(标记列表)}")


def 命令_parse(参数):
    """语法分析"""
    if not 参数.文件:
        print("🔴 错误: 请指定要分析的文件")
        sys.exit(1)

    文件路径 = 参数.文件[0]
    代码 = 读取文件(文件路径)

    print(f"🟢 语法分析: {文件路径}")
    print("=" * 60)

    try:
        AST = 解析源代码(代码)
        print(f"🟢 语法分析成功")
        print(f"顶级声明数: {len(AST.声明列表)}")
        print("-" * 60)
        for i, 声明 in enumerate(AST.声明列表):
            print(f"  [{i}] {声明.转字符串()}")

        审计系统.成功(操作类型.编译, "语法分析", f"AST节点: {len(AST.声明列表)}")

    except Exception as e:
        print(f"🔴 语法分析失败: {e}")
        审计系统.错误(操作类型.编译, "语法分析", str(e))


def 命令_check(参数):
    """四层检查"""
    if not 参数.文件:
        print("🔴 错误: 请指定要检查的文件")
        sys.exit(1)

    文件路径 = 参数.文件[0]
    代码 = 读取文件(文件路径)

    print(f"🟢 四层检查: {文件路径}")
    print("=" * 60)

    结果 = 快速四层检查(代码)

    print(f"综合结果: {结果['状态']}")
    print(f"总错误: {结果['总错误数']} | 总警告: {结果['总警告数']}")
    print()

    for 层名 in ["L1字符层", "L2关键字层", "L3语法层", "L4语义层"]:
        层结果 = 结果[层名]
        状态 = "🟢" if 层结果["通过"] else "🔴"
        print(f"{状态} {层名}: 错误{层结果['错误数']} 警告{层结果['警告数']}")
        for 错误 in 层结果['错误列表'][:3]:
            print(f"   🔴 {错误}")
        for 警告 in 层结果['警告列表'][:3]:
            print(f"   🟡 {警告}")
        print()


def 命令_translate(参数):
    """翻译模式"""
    翻译器 = 通心译翻译器(启用藏经阁=False)

    if 参数.文件:
        文本 = " ".join(参数.文件)
        print(f"🟢 翻译: '{文本}'")
        print("=" * 60)
        结果 = 翻译器.智能翻译(文本)
        print(f"原文: {文本}")
        print(f"译文: {结果}")

        # 显示术语解释
        高亮 = 翻译器.高亮术语(文本)
        if 高亮:
            print("\n术语识别:")
            for h in 高亮:
                解释 = 翻译器.解释术语(h['术语'])
                if 解释:
                    print(f"  {h['术语']} → {h['翻译']}")
                    print(f"    分类: {解释['分类']}")
                    print(f"    说明: {解释['说明']}")
    else:
        # 交互式翻译模式
        print("🟢 通心译翻译器交互模式")
        print("=" * 60)
        print("输入文本进行翻译，输入 'quit' 退出")
        print("输入 'list' 查看全部术语")
        print()

        while True:
            文本 = input("通心译> ").strip()
            if 文本.lower() in ('quit', 'exit', 'q'):
                break
            if 文本.lower() == 'list':
                术语表 = 翻译器.获取全部术语()
                print(f"\n共 {len(术语表)} 个术语:")
                for en, cn in sorted(术语表.items()):
                    print(f"  {en} → {cn}")
                print()
                continue

            if 文本:
                结果 = 翻译器.智能翻译(文本)
                print(f"  译文: {结果}\n")


def 命令_encrypt(参数):
    """加密文本"""
    加密器 = 点对点加密()

    if 参数.文件:
        文本 = " ".join(参数.文件)
    else:
        文本 = input("输入要加密的文本: ")

    print("🟢 加密文本...")
    消息 = 加密器.加密消息(文本)

    if 消息:
        print(f"密文: {消息.密文[:80]}...")
        print(f"签名: {消息.签名[:40]}...")
        print(f"算法: {消息.算法}")
        print(f"时间: {消息.时间戳}")
        print(f"\n完整数据(保存此数据进行解密):")
        print(消息.序列化())
    else:
        print("🔴 加密失败")


def 命令_decrypt(参数):
    """解密文本"""
    加密器 = 点对点加密()

    if 参数.文件:
        密文JSON = " ".join(参数.文件)
    else:
        密文JSON = input("输入密文JSON: ")

    try:
        from modules.encryption import 加密消息
        消息 = 加密消息.反序列化(密文JSON)
        明文 = 加密器.解密消息(消息)

        if 明文:
            print(f"🟢 解密成功: {明文}")
        else:
            print("🔴 解密失败")
    except Exception as e:
        print(f"🔴 解密错误: {e}")


def 命令_协议(参数):
    """显示龍魂系统使用协议"""
    协议路径 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "龍魂协议.txt")
    try:
        with open(协议路径, 'r', encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        print(f"🔴 无法读取协议文件: {e}")


def 命令_audit(参数):
    """显示审计报告"""
    报告 = 审计系统.生成报告()
    print("=" * 60)
    print("联动审计报告")
    print("=" * 60)
    print(f"总记录数: {报告['总记录数']}")
    print(f"时间段: {报告['时间段']['起始']} → {报告['时间段']['结束']}")
    print()
    print("级别统计:")
    for 级别, 数量 in 报告['级别统计'].items():
        if 数量 > 0:
            print(f"  {级别}: {数量}")
    print()
    print("模块统计:")
    for 模块, 数量 in 报告['模块统计'].items():
        print(f"  {模块}: {数量}")
    print()


def 命令_version(参数):
    """版本信息"""
    打印版本信息()


def 命令_help(参数):
    """帮助信息"""
    打印帮助信息()


# ========== 主程序 ==========

def 主程序():
    """主程序入口"""
    解析器 = argparse.ArgumentParser(
        description='CNSH多语言编辑器终端v5.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{DNA追溯}
UID{UID} · {作者} · 龍芯北辰
CC BY-NC-SA 4.0 (君子协议)
"""
    )

    解析器.add_argument('命令', nargs='?',
                       choices=['gui', 'compile', 'lex', 'parse', 'check',
                               'translate', 'encrypt', 'decrypt', 'audit',
                               '协议', 'version', 'help'],
                       default='gui',
                       help='要执行的命令')
    解析器.add_argument('文件', nargs='*', help='输入文件路径')
    解析器.add_argument('--version', action='store_true', help='显示版本信息')

    参数 = 解析器.parse_args()

    if 参数.version:
        打印版本信息()
        return

    # 命令分发
    命令映射 = {
        'gui': 命令_gui,
        'compile': 命令_compile,
        'lex': 命令_lex,
        'parse': 命令_parse,
        'check': 命令_check,
        'translate': 命令_translate,
        'encrypt': 命令_encrypt,
        'decrypt': 命令_decrypt,
        'audit': 命令_audit,
        '协议': 命令_协议,
        'version': 命令_version,
        'help': 命令_help,
    }

    命令函数 = 命令映射.get(参数.命令, 命令_help)

    # 记录启动审计
    审计系统.成功(操作类型.运行, "终端",
                f"CNSH终端v{版本}启动，命令: {参数.命令}")

    命令函数(参数)


if __name__ == "__main__":
    主程序()
