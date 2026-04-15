#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 字体引擎管理器 - UID9622  
简化版 - 自动扫描并测试引擎
"""

import os
import sys
import importlib.util
from pathlib import Path

class CNSH引擎管理器_UID9622:
    """引擎管理器"""

    引擎映射 = {
        "批量版": "V0002",
        "审计版": "V0003",
        "组合": "V0004",
        "力度": "V0005",
        "侵蚀": "V0006",
        "重心": "V0007",
        "层级": "V0008",
        "纹理": "V0009",
        "排版": "V0010",
        "墨色": "V0011",
    }

    def __init__(self):
        self.引擎库 = {}
        self.扫描引擎()

    def 扫描引擎(self):
        """扫描并尝试加载所有引擎"""
        目录 = Path(__file__).parent
        print(f"🔍 扫描: {目录}\n")

        py_files = sorted(f for f in 目录.glob("*.py") if "管理器" not in f.name and "UID9622" in f.name)
        print(f"✓ 找到 {len(py_files)} 个引擎文件\n")

        for py_file in py_files:
            self._尝试加载引擎(py_file)

    def _尝试加载引擎(self, py_file):
        """尝试加载一个引擎文件"""
        文件名 = py_file.name
        版本 = "V0999"
        
        # 识别版本
        for 关键字, 版本号 in self.引擎映射.items():
            if 关键字 in 文件名:
                版本 = 版本号
                break

        try:
            spec = importlib.util.spec_from_file_location(
                文件名.replace('.py', ''),
                str(py_file)
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # 从模块中查找所有类
            类列表 = [name for name in dir(module) if "UID9622" in name and name[0].isupper()]
            
            if 类列表:
                类名 = 类列表[0]
                引擎类 = getattr(module, 类名)
                
                # 尝试实例化
                实例 = 引擎类()
                
                self.引擎库[版本] = {
                    "文件": 文件名,
                    "类": 类名,
                    "实例": 实例,
                    "状态": "✓"
                }
                print(f"✓ {版本}: {类名}")
                return
            else:
                print(f"✗ {版本}: 未找到引擎类 ({文件名})")

        except SyntaxError as e:
            print(f"✗ {版本}: 语法错误 ({e.lineno}) - {文件名}")
        except Exception as e:
            print(f"✗ {版本}: {str(e)[:60]} - {文件名}")

    def list(self):
        """列出所有引擎"""
        print("\n" + "="*60)
        print("📋 CNSH 字体引擎")
        print("="*60 + "\n")

        if not self.引擎库:
            print("❌ 没有找到任何可用引擎")
            return

        for 版本, 信息 in sorted(self.引擎库.items()):
            print(f"{版本}: {信息['类']} ({info['文件']})")

        print("\n" + "="*60)
        print(f"总计: {len(self.引擎库)} 个引擎")
        print("="*60 + "\n")

    def test(self):
        """测试所有引擎"""
        print("\n" + "="*60)
        print("🧪 引擎测试")
        print("="*60 + "\n")

        if not self.引擎库:
            print("❌ 没有可用引擎")
            return False

        成功 = 0
        失败 = 0

        for 版本, 信息 in sorted(self.引擎库.items()):
            try:
                实例 = 信息["实例"]
                方法 = ['载入', '执行', '输出SVG']
                有效 = sum(1 for m in 方法 if hasattr(实例, m))
                print(f"✓ {版本}: {有效}/3 方法")
                成功 += 1
            except Exception as e:
                print(f"✗ {版本}: {str(e)[:60]}")
                失败 += 1

        print("\n" + "="*60)
        print(f"测试完成: {成功} 通过, {失败} 失败")
        print("="*60 + "\n")

        return 失败 == 0


def main():
    管理器 = CNSH引擎管理器_UID9622()

    if len(sys.argv) < 2:
        管理器.list()
        return

    命令 = sys.argv[1].lower()

    if 命令 == 'list':
        管理器.list()
    elif 命令 == 'test':
        成功 = 管理器.test()
        sys.exit(0 if 成功 else 1)
    else:
        print(f"命令: {命令} (list/test)")


if __name__ == "__main__":
    main()
