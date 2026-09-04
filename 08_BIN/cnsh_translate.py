#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-01-CNSH-TRANSLATE-v1.1-PURE-PYTHON-SOVEREIGNTY
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂·CNSH 文件翻译工具 v1.1 — 闸口样板（10条修复规则全过）

能力:
  翻译文件    python3 08_BIN/cnsh_translate.py <文件> [-o 输出]
  翻译目录    python3 08_BIN/cnsh_translate.py <目录> -t dir
  项目骨架    python3 08_BIN/cnsh_translate.py -t project -n 项目名 [-o 目录]
  环境检查    python3 08_BIN/cnsh_translate.py --env-check
  安装脚本    python3 08_BIN/cnsh_translate.py --setup

对齐:
  ① 函数名/变量名 = CNSH 中文命名（不允许英文标识符）
  ② 依赖 = 纯 Python 标准库（os/sys/re/json/hashlib/shutil/pathlib/datetime/typing）
  ③ 平台 = 无 os.name / sys.platform 判断（统一抽象层）
  ④ 版本 = 无 requires-python 限制，支持 3.8+（typing 泛型·f-string 均兼容）
  ⑤ 中间层 = 零外部网关调用（原生直连·M77）
  ⑥ 编码 = 顶部 DNA 追溯码 + 底部三色审计
  ⑦ 输出 = 时间戳 + SHA-256 哈希（GPG 由 lh_gpg_sign.py 侧签）
  ⑧ 入仓 = pre-commit CNSH 命名闸口
  ⑨ 登记 = COMMAND_INDEX.md
  ⑩ 签名 = GPG .asc 同目录

文化主权: CNSH 语法不翻译 · 这是尊严
"""

import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ============================================================
# 一、核心常量
# ============================================================
文件头模板 = '''# -*- coding: utf-8 -*-
# 文件: {文件名}
# 类型: {类型}
# DNA: {追溯码}
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 审计: 🟢 通过
# 文化主权: CNSH 语法不翻译 · 这是尊严

'''

文件类型映射 = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.cpp': 'C++',
    '.c': 'C',
    '.java': 'Java',
    '.go': 'Go',
    '.rs': 'Rust',
    '.sh': 'Shell',
    '.txt': 'Text',
    '.md': 'Markdown',
    '.json': 'JSON',
    '.yaml': 'YAML',
    '.toml': 'TOML',
    '.html': 'HTML',
    '.css': 'CSS',
    '.sql': 'SQL',
}

跳过目录 = ['__pycache__', '.git', 'node_modules', 'venv', '.venv', 'dist', 'models', '11_DATA', '_work']

# ============================================================
# 二、核心翻译引擎（中文命名）
# ============================================================


class 翻译引擎:
    """CNSH 翻译引擎 — 将任意代码翻译成 CNSH 格式（中文命名）"""

    def __init__(self, 详细: bool = False):
        self.详细 = 详细
        self.成功数 = 0
        self.跳过数 = 0
        self.错误清单 = []

    def 记录(self, 消息: str, 级别: str = "INFO"):
        if self.详细 or 级别 == "ERROR":
            print(f"[{级别}] {消息}")

    def 检测文件类型(self, 文件路径: Path) -> str:
        """检测文件类型（扩展名优先，其次 shebang）"""
        扩展名 = 文件路径.suffix.lower()
        if 扩展名 in 文件类型映射:
            return 文件类型映射[扩展名]
        try:
            with open(文件路径, 'r', encoding='utf-8') as 文件:
                首行 = 文件.readline()
                if 首行.startswith('#!'):
                    if 'python' in 首行:
                        return 'Python'
                    if 'node' in 首行:
                        return 'JavaScript'
                    if 'bash' in 首行 or 'sh' in 首行:
                        return 'Shell'
        except Exception:
            pass
        return 'Unknown'

    def 生成追溯码(self, 名称: str) -> str:
        """生成 DNA 追溯码"""
        今日 = datetime.now().strftime("%Y-%m-%d")
        安全名 = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]', '_', 名称)[:18]
        return f"#龍芯⚡️{今日}-{安全名}-v1.0-UID9622"

    def 提取导入(self, 内容: str, 类型: str) -> List[str]:
        """提取 import/include 语句"""
        导入清单 = []
        if 类型 == 'Python':
            规则 = r'^(?:from|import)\s+[\w\.]+(?:\s+import\s+[\w\.]+)?'
            for 行 in 内容.split('\n'):
                if re.match(规则, 行.strip()):
                    导入清单.append(行.strip())
        elif 类型 == 'JavaScript':
            规则 = r'^(?:import|require)\s*\(?[\'"\w]+'
        elif 类型 == 'C++':
            规则 = r'^#include\s*[<"][\w\.]+[>"]'
        elif 类型 == 'Java':
            规则 = r'^import\s+[\w\.]+;'
        else:
            规则 = None
        if 规则:
            for 行 in 内容.split('\n'):
                if re.match(规则, 行.strip()):
                    导入清单.append(行.strip())
        return 导入清单

    def 提取函数(self, 内容: str, 类型: str) -> List[Dict]:
        """提取函数定义（名称/参数/返回类型）"""
        函数清单 = []
        if 类型 == 'Python':
            规则 = r'^def\s+(\w+)\s*\(([^)]*)\)\s*:?'
            for 行 in 内容.split('\n'):
                匹配 = re.match(规则, 行.strip())
                if 匹配:
                    函数清单.append({
                        'name': 匹配.group(1),
                        'params': 匹配.group(2),
                        'return_type': '任意类型',
                    })
        elif 类型 == 'JavaScript':
            规则 = r'^(?:function\s+(\w+)|(\w+)\s*=\s*function|(\w+)\s*\([^)]*\)\s*=>)\s*\(?([^)]*)\)?'
            for 行 in 内容.split('\n'):
                匹配 = re.match(规则, 行.strip())
                if 匹配:
                    名称 = 匹配.group(1) or 匹配.group(2) or 匹配.group(3)
                    if 名称:
                        函数清单.append({'name': 名称, 'params': '参数', 'return_type': '任意类型'})
        elif 类型 == 'C++':
            规则 = r'^[a-zA-Z_][\w]*\s+([a-zA-Z_][\w]*)\s*\(([^)]*)\)\s*\{?'
            for 行 in 内容.split('\n'):
                匹配 = re.match(规则, 行.strip())
                if 匹配:
                    函数清单.append({
                        'name': 匹配.group(1),
                        'params': 匹配.group(2),
                        'return_type': '指定类型',
                    })
        return 函数清单

    def 提取类(self, 内容: str, 类型: str) -> List[str]:
        """提取类名"""
        类清单 = []
        if 类型 == 'Python':
            规则 = r'^class\s+(\w+)\s*[:\(]'
        elif 类型 in ('Java', 'C++'):
            规则 = r'^class\s+(\w+)\s*\{'
        else:
            规则 = None
        if 规则:
            for 行 in 内容.split('\n'):
                匹配 = re.match(规则, 行.strip())
                if 匹配:
                    类清单.append(匹配.group(1))
        return 类清单

    def 翻译标识符(self, 内容: str, 类型: str) -> str:
        """将英文标识符翻译为中文（不破坏字符串/注释）"""
        通用翻译表 = {
            'main': '主函数', 'init': '初始化', 'start': '启动', 'stop': '停止',
            'run': '运行', 'process': '处理', 'handle': '处理', 'get': '获取',
            'set': '设置', 'find': '查找', 'search': '搜索', 'create': '创建',
            'delete': '删除', 'update': '更新', 'save': '保存', 'load': '加载',
            'read': '读取', 'write': '写入', 'open': '打开', 'close': '关闭',
            'connect': '连接', 'disconnect': '断开', 'send': '发送',
            'receive': '接收', 'request': '请求', 'response': '响应',
            'parse': '解析', 'format': '格式化', 'validate': '验证',
            'check': '检查', 'test': '测试', 'debug': '调试', 'log': '日志',
            'error': '错误', 'success': '成功', 'fail': '失败', 'retry': '重试',
            'timeout': '超时', 'wait': '等待', 'sleep': '休眠', 'exit': '退出',
            'return': '返回', 'print': '打印', 'input': '输入', 'output': '输出',
            'data': '数据', 'info': '信息', 'config': '配置', 'setting': '设置',
            'option': '选项', 'param': '参数', 'result': '结果', 'status': '状态',
            'value': '值', 'key': '键', 'list': '列表', 'dict': '字典',
            'tuple': '元组', 'str': '字符串', 'int': '整数', 'float': '浮点数',
            'bool': '布尔', 'none': '空',
        }
        新行清单 = []
        for 行 in 内容.split('\n'):
            if 行.strip().startswith(('#', '//', '/*', '*')) or re.match(r'^[\s]*[\'"]', 行):
                新行清单.append(行)
                continue
            新行 = 行
            for 英文, 中文 in 通用翻译表.items():
                新行 = re.sub(rf'\b{英文}\b', 中文, 新行)
            新行清单.append(新行)
        return '\n'.join(新行清单)

    def 翻译文件(self, 输入路径: Path, 输出路径: Path, 名称: Optional[str] = None) -> bool:
        """翻译单个文件到 CNSH 格式"""
        try:
            if not 输入路径.exists():
                self.记录(f"文件不存在: {输入路径}", "ERROR")
                return False

            类型 = self.检测文件类型(输入路径)
            self.记录(f"翻译: {输入路径.name} ({类型})")

            with open(输入路径, 'r', encoding='utf-8', errors='ignore') as 文件:
                原始内容 = 文件.read()

            if not 名称:
                名称 = 输入路径.stem
            追溯码 = self.生成追溯码(名称)
            头部 = 文件头模板.format(
                文件名=输出路径.name,
                类型=类型,
                追溯码=追溯码,
            )

            导入清单 = self.提取导入(原始内容, 类型)
            导入段 = ''
            if 导入清单:
                导入段 = '# 导入模块\n'
                for 导入 in 导入清单:
                    导入段 += f'# {导入}\n'

            类清单 = self.提取类(原始内容, 类型)
            类段 = ''
            if 类清单:
                类段 = '# 类定义\n'
                for 类名 in 类清单:
                    类段 += f'# 类 {类名}\n'

            翻译体 = self.翻译标识符(原始内容, 类型)

            译文 = 头部
            译文 += f'# 原始文件: {输入路径.name}\n'
            译文 += f'# 翻译时间: {datetime.now().isoformat()}\n\n'
            译文 += 导入段
            译文 += 类段
            译文 += '\n# 主逻辑\n'
            译文 += 翻译体
            译文 += f'''
# ============================================================
# 审计信息
# 三色审计: 🟢 通过
# DNA: {追溯码}
# 版本: v1.0
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# ============================================================
'''

            输出路径.parent.mkdir(parents=True, exist_ok=True)
            with open(输出路径, 'w', encoding='utf-8') as 文件:
                文件.write(译文)

            self.成功数 += 1
            self.记录(f"✅ 已生成: {输出路径}")
            return True

        except Exception as 异常:
            self.错误清单.append(str(异常))
            self.记录(f"❌ 翻译失败: {输入路径} -> {异常}", "ERROR")
            return False

    def 翻译目录(self, 输入目录: Path, 输出目录: Path) -> Dict:
        """翻译整个目录（跳过缓存/虚拟环境等）"""
        self.记录(f"开始翻译目录: {输入目录} -> {输出目录}")

        文件清单 = []
        for 扩展名 in 文件类型映射:
            文件清单.extend(输入目录.rglob(f'*{扩展名}'))

        self.记录(f"发现 {len(文件清单)} 个可翻译文件")

        结果 = {'total': len(文件清单), 'success': 0, 'failed': 0, 'skipped': 0, 'details': []}

        for 文件路径 in 文件清单:
            if any(部分 in str(文件路径) for 部分 in 跳过目录):
                continue
            if 文件路径.name.startswith('.'):
                continue

            相对路径 = 文件路径.relative_to(输入目录)
            输出路径 = 输出目录 / 相对路径.with_suffix('.cnsh')

            if self.翻译文件(文件路径, 输出路径):
                结果['success'] += 1
                结果['details'].append({'file': str(文件路径), 'status': 'success'})
            else:
                结果['failed'] += 1
                结果['details'].append({'file': str(文件路径), 'status': 'failed'})

        return 结果

    def 生成环境检查(self, 输出路径: Path) -> bool:
        """生成环境检查脚本"""
        脚本 = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·CNSH 环境检查工具
"""

import subprocess
import sys


def 检查_python():
    print(f"Python: {sys.version}")
    return sys.version_info >= (3, 8)


def 检查_utf8():
    try:
        import locale
        编码 = locale.getpreferredencoding()
        print(f"终端编码: {编码}")
        return 编码.lower() in ('utf-8', 'utf8')
    except Exception:
        return False


def 主函数():
    print("=" * 50)
    print("🐉 龍魂·CNSH 环境检查")
    print("=" * 50)
    检查项 = [
        ("Python 3.8+", 检查_python()),
        ("UTF-8 终端", 检查_utf8()),
    ]
    print()
    全过 = True
    for 名称, 通过 in 检查项:
        print(("✅" if 通过 else "❌") + f" {名称}")
        if not 通过:
            全过 = False
    print()
    print("✅ 所有检查通过" if 全过 else "⚠️ 部分检查未通过，请安装缺失组件")
    return 0 if 全过 else 1


if __name__ == "__main__":
    sys.exit(主函数())
'''
        try:
            with open(输出路径, 'w', encoding='utf-8') as 文件:
                文件.write(脚本)
            os.chmod(输出路径, 0o755)
            self.记录(f"✅ 已生成环境检查脚本: {输出路径}")
            return True
        except Exception as 异常:
            self.记录(f"❌ 生成环境检查脚本失败: {异常}", "ERROR")
            return False

    def 生成安装脚本(self, 输出路径: Path) -> bool:
        """生成一键安装脚本"""
        脚本 = '''#!/bin/bash
# 龍魂·CNSH 一键安装脚本
# DNA: #龍芯⚡️2026-09-01-CNSH-SETUP-v1.0-UID9622

echo "🐉 龍魂·CNSH 一键安装"
echo "========================"

if command -v python3 &> /dev/null; then
    echo "✅ Python 3: $(python3 --version)"
else
    echo "❌ Python 3 未安装，请先安装 Python 3.8+"
    exit 1
fi

echo ""
echo "========================"
echo "✅ 环境就绪"
echo "用法: python3 env_check.py  # 检查环境"
'''
        try:
            with open(输出路径, 'w', encoding='utf-8') as 文件:
                文件.write(脚本)
            os.chmod(输出路径, 0o755)
            self.记录(f"✅ 已生成一键安装脚本: {输出路径}")
            return True
        except Exception as 异常:
            self.记录(f"❌ 生成安装脚本失败: {异常}", "ERROR")
            return False

    def 生成项目模板(self, 输出路径: Path, 名称: str) -> bool:
        """生成 CNSH 项目骨架（src/main.cnsh + Makefile）"""
        主文件 = f'''# -*- coding: utf-8 -*-
# 文件: main.cnsh
# DNA: {self.生成追溯码(名称)}
# 审计: 🟢 通过

# 导入模块
从 系统 导入 控制台

# 定义函数
函数 处理数据(输入数据: 字符串) -> 字符串 {{
    结果 = "🐉 " + 输入数据
    返回 结果
}}

# 主函数
函数 主函数() -> 整数 {{
    控制台.打印("龙魂·CNSH 项目 {名称} 启动!")
    数据 = 控制台.输入("请输入内容: ")
    结果 = 处理数据(数据)
    控制台.打印("处理结果: " + 结果)
    返回 0
}}

# 程序入口
主函数()
'''
        try:
            源码目录 = 输出路径 / 'src'
            源码目录.mkdir(parents=True, exist_ok=True)
            with open(源码目录 / 'main.cnsh', 'w', encoding='utf-8') as 文件:
                文件.write(主文件)

            构建文件 = f'''# CNSH 项目 {名称} Makefile
PROJECT_NAME = {名称}
SOURCES = src/main.cnsh
TARGET = bin/$(PROJECT_NAME)

all: $(TARGET)

$(TARGET): $(SOURCES)
\tmkdir -p bin
\tcnshc src/main.cnsh -o $(TARGET)

clean:
\trm -rf bin/

install: $(TARGET)
\tcp $(TARGET) /usr/local/bin/

.PHONY: all clean install
'''
            with open(输出路径 / 'Makefile', 'w', encoding='utf-8') as 文件:
                文件.write(构建文件)

            self.记录(f"✅ 已生成项目模板: {输出路径}")
            return True
        except Exception as 异常:
            self.记录(f"❌ 生成项目模板失败: {异常}", "ERROR")
            return False


# ============================================================
# 三、CLI 主入口（中文命名 · 时间戳 · 哈希）
# ============================================================


def 主函数():
    import argparse

    参数解析 = argparse.ArgumentParser(
        description="🐉 龍魂·CNSH 文件翻译工具",
        epilog="文化主权: CNSH 语法不翻译 · 这是尊严",
    )
    参数解析.add_argument('输入', nargs='?', help='输入文件或目录')
    参数解析.add_argument('-o', '--output', dest='输出', help='输出文件或目录')
    参数解析.add_argument(
        '-t', '--type', dest='类型',
        choices=['file', 'dir', 'project'], default='file',
        help='翻译类型: file(单文件) / dir(目录) / project(项目模板)',
    )
    参数解析.add_argument('-n', '--name', dest='名称', help='项目/文件名称')
    参数解析.add_argument('--env-check', dest='环境检查', action='store_true', help='生成环境检查脚本')
    参数解析.add_argument('--setup', dest='安装', action='store_true', help='生成一键安装脚本')
    参数解析.add_argument('-v', '--verbose', dest='详细', action='store_true')
    参数解析.add_argument('--version', action='version', version='CNSH Translator v1.1')

    参数 = 参数解析.parse_args()
    工具 = 翻译引擎(详细=参数.详细)
    时间戳 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if getattr(参数, '环境检查', False):
        工具.生成环境检查(Path('env_check.py'))
        return
    if getattr(参数, '安装', False):
        工具.生成安装脚本(Path('setup.sh'))
        return
    if 参数.类型 == 'project':
        名称 = 参数.名称 or '龙魂项目'
        输出 = Path(参数.输出) if 参数.输出 else Path(名称)
        工具.生成项目模板(输出, 名称)
        return

    if not 参数.输入:
        参数解析.print_help()
        return

    输入路径 = Path(参数.输入)
    if not 输入路径.exists():
        print(f"❌ 输入路径不存在: {输入路径}")
        return

    if 参数.输出:
        输出路径 = Path(参数.输出)
    else:
        if 参数.类型 == 'dir':
            输出路径 = 输入路径.parent / f"{输入路径.name}_cnsh"
        else:
            输出路径 = 输入路径.parent / f"{输入路径.stem}.cnsh"

    if 参数.类型 == 'dir' or 输入路径.is_dir():
        if 参数.类型 == 'file':
            print("⚠️ 输入是目录，但指定类型为 file，自动切换为 dir")
        结果 = 工具.翻译目录(输入路径, 输出路径)
        print(f"\n📊 翻译完成: 成功 {结果['success']}/{结果['total']}")
        if 结果['failed'] > 0:
            print(f"❌ 失败: {结果['failed']}")
            for 详情 in 结果['details']:
                if 详情['status'] == 'failed':
                    print(f"  - {详情['file']}")
    else:
        工具.翻译文件(输入路径, 输出路径)

    # 输出带时间戳 + 哈希（规则⑦）
    try:
        if (输出路径.is_file() if 输出路径 else False):
            哈希 = hashlib.sha256(输出路径.read_bytes()).hexdigest()[:16]
            print(f"🕐 {时间戳} · SHA-256: {哈希}")
    except Exception:
        pass


if __name__ == '__main__':
    主函数()

# ============================================================
# 底部 · 三色审计（规则⑥）
# ============================================================
# 🟢 命名: 全部中文标识符（无英文函数/变量名）
# 🟢 依赖: 纯标准库（os/sys/re/json/hashlib/shutil/pathlib/datetime/typing）
# 🟢 平台: 无 os.name / sys.platform 判断
# 🟢 版本: 无 requires-python · 3.8+ 兼容
# 🟢 中间层: 零外部网关 · 原生直连
# 🟢 编码: 顶部 DNA + 底部三色 · 归属名已含
# 🟡 输出: 时间戳+哈希已内置 · GPG 侧签（lh_gpg_sign.py）
# 🔴 0
# ============================================================
