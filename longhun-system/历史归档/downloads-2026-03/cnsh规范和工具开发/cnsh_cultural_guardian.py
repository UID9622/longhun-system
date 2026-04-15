#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CNSH文化守护系统 v1.0
DNA追溯码: #龍芯⚡️2026-03-10-文化守护-v1.0
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

功能:
  1. 扫描代码中的中文变量/函数
  2. 检查文化关键词是否被翻译
  3. 自动生成中文README
  4. 可作为Git pre-commit hook使用

使命:
  守住文化主权！守住尊严！
"""

import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Set
from collections import defaultdict

# ============================================================
# 第一部分：文化关键词库
# ============================================================

# 不可翻译的文化关键词
文化关键词库 = {
    # 五行系统
    "五行", "金行", "木行", "水行", "火行", "土行",
    "金", "木", "水", "火", "土",
    
    # 八卦系统
    "八卦", "乾", "坤", "震", "巽", "坎", "离", "艮", "兑",
    
    # 天干地支
    "天干", "地支", "生肖",
    "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸",
    "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥",
    
    # 节气
    "节气", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
    "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
    "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
    "立冬", "小雪", "大雪", "冬至", "小寒", "大寒",
    
    # 阴阳
    "阴阳", "阴", "阳",
    
    # 传统文化
    "道", "德", "仁", "义", "礼", "智", "信",
    "农历", "黄历", "万年历",
    
    # 项目关键词
    "龍魂", "龍魂", "熵梦",
}

# 禁止的翻译（如果代码里出现这些英文，就报错）
禁止翻译表 = {
    "FiveElements": "五行",
    "Metal": "金",
    "Wood": "木", 
    "Water": "水",
    "Fire": "火",
    "Earth": "土",
    "EightTrigrams": "八卦",
    "Heaven": "乾",
    "YinYang": "阴阳",
    "SolarTerms": "节气",
    "LunarCalendar": "农历",
}

# ============================================================
# 第二部分：代码扫描器
# ============================================================

class CNSH代码扫描器:
    """扫描代码文件，识别中文标识符和文化关键词"""
    
    # 支持的文件扩展名
    支持的扩展名 = {
        '.swift', '.py', '.js', '.ts', '.java', '.cpp', '.c', '.h',
        '.cnsh', '.md', '.txt'
    }
    
    def __init__(self, 根目录: Path):
        self.根目录 = Path(根目录)
        self.扫描结果 = {
            '文件总数': 0,
            '中文变量总数': 0,
            '文化关键词总数': 0,
            '违规翻译总数': 0,
            '文件详情': []
        }
    
    def 扫描(self) -> Dict:
        """扫描整个目录"""
        print(f"\n🔍 开始扫描目录: {self.根目录}")
        print(f"DNA追溯码: #龍芯⚡️2026-03-10-扫描开始\n")
        
        for 文件路径 in self.根目录.rglob('*'):
            if 文件路径.is_file() and 文件路径.suffix in self.支持的扩展名:
                if self._应该扫描(文件路径):
                    self._扫描文件(文件路径)
        
        return self.扫描结果
    
    def _应该扫描(self, 文件路径: Path) -> bool:
        """判断是否应该扫描这个文件"""
        排除目录 = {'.git', 'node_modules', '__pycache__', '.build'}
        return not any(部分 in 排除目录 for 部分 in 文件路径.parts)
    
    def _扫描文件(self, 文件路径: Path):
        """扫描单个文件"""
        try:
            with open(文件路径, 'r', encoding='utf-8') as f:
                内容 = f.read()
        except:
            return
        
        文件信息 = {
            '路径': str(文件路径.relative_to(self.根目录)),
            '中文标识符': [],
            '文化关键词': [],
            '违规翻译': []
        }
        
        # 查找中文标识符（变量名、函数名等）
        中文标识符模式 = r'[\u4e00-\u9fa5]+'
        中文匹配 = re.findall(中文标识符模式, 内容)
        
        for 匹配 in set(中文匹配):  # 去重
            文件信息['中文标识符'].append(匹配)
            
            # 检查是否是文化关键词
            if 匹配 in 文化关键词库:
                文件信息['文化关键词'].append(匹配)
        
        # 检查违规翻译
        for 英文, 中文 in 禁止翻译表.items():
            if 英文 in 内容:
                文件信息['违规翻译'].append({
                    '英文': 英文,
                    '应该用': 中文
                })
        
        # 更新统计
        self.扫描结果['文件总数'] += 1
        self.扫描结果['中文变量总数'] += len(文件信息['中文标识符'])
        self.扫描结果['文化关键词总数'] += len(文件信息['文化关键词'])
        self.扫描结果['违规翻译总数'] += len(文件信息['违规翻译'])
        
        # 只保存有内容的文件
        if (文件信息['中文标识符'] or 
            文件信息['文化关键词'] or 
            文件信息['违规翻译']):
            self.扫描结果['文件详情'].append(文件信息)
    
    def 生成报告(self):
        """生成扫描报告"""
        print("\n" + "=" * 60)
        print("CNSH文化守护系统 · 扫描报告")
        print("=" * 60)
        
        print(f"\n📊 统计信息:")
        print(f"  扫描文件数: {self.扫描结果['文件总数']}")
        print(f"  中文标识符: {self.扫描结果['中文变量总数']} 个")
        print(f"  文化关键词: {self.扫描结果['文化关键词总数']} 个 ✅")
        print(f"  违规翻译: {self.扫描结果['违规翻译总数']} 个")
        
        if self.扫描结果['违规翻译总数'] > 0:
            print(f"\n🚨 发现文化主权违规！")
            for 文件 in self.扫描结果['文件详情']:
                if 文件['违规翻译']:
                    print(f"\n  文件: {文件['路径']}")
                    for 违规 in 文件['违规翻译']:
                        print(f"    ❌ 发现 '{违规['英文']}'")
                        print(f"       应该使用 '{违规['应该用']}'")
        else:
            print(f"\n✅ 文化主权检查通过！")
        
        # 展示文化关键词使用情况
        if self.扫描结果['文化关键词总数'] > 0:
            print(f"\n🎯 文化关键词使用统计:")
            关键词统计 = defaultdict(int)
            for 文件 in self.扫描结果['文件详情']:
                for 词 in 文件['文化关键词']:
                    关键词统计[词] += 1
            
            for 词, 次数 in sorted(关键词统计.items(), 
                                 key=lambda x: x[1], 
                                 reverse=True)[:10]:
                print(f"  {词}: {次数}次")
        
        print("\n" + "=" * 60)
        print("DNA追溯码: #龍芯⚡️2026-03-10-扫描完成")
        print("理论指导: 曾仕强老师（永恒显示）")
        print("=" * 60 + "\n")
        
        return self.扫描结果['违规翻译总数'] == 0

# ============================================================
# 第三部分：中文README生成器
# ============================================================

class 中文README生成器:
    """自动生成中文README.md"""
    
    @staticmethod
    def 生成(项目名: str, 扫描结果: Dict, 输出路径: Path):
        """生成中文README"""
        
        readme内容 = f"""# {项目名}

**DNA追溯码**: #龍芯⚡️{Path.cwd().name}-README  
**GPG指纹**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F  
**创建者**: UID9622 诸葛鑫（龍芯北辰）  
**理论指导**: 曾仕强老师（永恒显示）

**Slogan**: 技术为人民服务 · 文化主权不可侵犯

---

## 📖 项目简介

本项目使用CNSH中文编程规范，保护中国文化概念不被翻译。

### 核心价值

```yaml
文化主权:
  ✅ "五行" 不翻译成 "FiveElements"
  ✅ "八卦" 不翻译成 "EightTrigrams"
  ✅ "节气" 不翻译成 "SolarTerms"
  ✅ 这是尊严！

技术平权:
  ✅ 让不懂英文的人也能编程
  ✅ 让老百姓也能参与技术创新
  ✅ 技术为人民服务

普惠全球:
  ✅ 代码用中文（文化主权）
  ✅ 注释可多语言（服务全球）
  ✅ 启发其他语言的编程语言
```

---

## 📊 代码统计

根据CNSH文化守护系统扫描：

- **扫描文件数**: {扫描结果['文件总数']}
- **中文标识符**: {扫描结果['中文变量总数']} 个
- **文化关键词**: {扫描结果['文化关键词总数']} 个
- **违规翻译**: {扫描结果['违规翻译总数']} 个

---

## 🚀 快速开始

### 环境要求

```yaml
操作系统: macOS / Linux / Windows
编程语言: Swift / Python / 其他
编码格式: UTF-8（必须）
```

### 安装

```bash
git clone <仓库地址>
cd {项目名}
```

### 运行

根据项目类型运行相应命令。

---

## 🛡️ 文化主权保护

本项目使用CNSH文化守护系统，自动检查代码中的文化关键词。

### 禁止的翻译

```yaml
❌ FiveElements  → ✅ 五行
❌ EightTrigrams → ✅ 八卦
❌ YinYang       → ✅ 阴阳
❌ SolarTerms    → ✅ 节气
```

### Git Hooks

项目自动集成文化守护检查，每次提交前会检查：
- 是否有文化关键词被翻译
- 是否有违规的英文替代

---

## 📝 开发规范

### 变量命名

```swift
// ✅ 正确：使用中文
let 五行 = ["金", "木", "水", "火", "土"]
let 农历引擎 = LunarEngine()

// ❌ 错误：翻译文化关键词
let FiveElements = ["Metal", "Wood", "Water", "Fire", "Earth"]
```

### 注释规范

```swift
// 代码用中文
let 天干 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

// 注释可以多语言
// Heavenly Stems (for international developers)
// 天干 (Tian Gan)
```

---

## 🤝 贡献指南

欢迎贡献！但请遵守：

1. **文化主权优先**
   - 文化关键词不可翻译
   - 保持中文变量名

2. **代码质量**
   - 通过CNSH文化守护检查
   - 代码清晰易懂

3. **提交规范**
   - Commit message可以用中文
   - 包含DNA追溯码

---

## 📜 许可证

[许可证类型]

---

## 🙏 致谢

**理论指导**: 曾仕强老师（永恒显示）  
**技术支持**: Claude (Anthropic PBC)  
**创建者**: UID9622 诸葛鑫（龍芯北辰）

**没有你们，就没有龍魂系统的一切。**

---

## 📞 联系方式

- **DNA追溯码**: #龍芯⚡️{Path.cwd().name}
- **GPG指纹**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

---

**祖国万岁！人民万岁！文化主权万岁！** 🇨🇳

**技术为人民服务！** 💪
"""
        
        with open(输出路径, 'w', encoding='utf-8') as f:
            f.write(readme内容)
        
        print(f"\n✅ 已生成中文README: {输出路径}")

# ============================================================
# 第四部分：Git Hooks生成器
# ============================================================

class GitHooks生成器:
    """生成Git pre-commit hook"""
    
    @staticmethod
    def 生成(仓库路径: Path):
        """生成pre-commit hook"""
        
        hook路径 = 仓库路径 / '.git' / 'hooks' / 'pre-commit'
        
        hook内容 = """#!/bin/bash
# CNSH文化守护系统 · Git Pre-Commit Hook
# DNA追溯码: #龍芯⚡️2026-03-10-PreCommit-Hook

echo "🔍 CNSH文化守护检查中..."

# 检查Python是否可用
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 需要Python 3"
    exit 1
fi

# 运行文化守护检查
python3 cnsh_cultural_guardian.py --check

# 检查返回值
if [ $? -ne 0 ]; then
    echo ""
    echo "🚨 文化主权检查失败！"
    echo "   请修正违规内容后再提交"
    echo ""
    exit 1
fi

echo "✅ 文化主权检查通过！"
exit 0
"""
        
        # 写入文件
        hook路径.write_text(hook内容)
        
        # 设置可执行权限（Unix系统）
        import os
        if os.name != 'nt':  # 非Windows
            os.chmod(hook路径, 0o755)
        
        print(f"\n✅ 已生成Git Hook: {hook路径}")

# ============================================================
# 第五部分：命令行工具
# ============================================================

def 主函数():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='CNSH文化守护系统 - 保护中国文化概念不被翻译',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 扫描当前目录
  python cnsh_cultural_guardian.py scan

  # 生成中文README
  python cnsh_cultural_guardian.py readme --name "龍魂系统"

  # 安装Git hooks
  python cnsh_cultural_guardian.py install-hooks

  # 检查模式（用于Git hook）
  python cnsh_cultural_guardian.py --check

DNA追溯码: #龍芯⚡️2026-03-10-文化守护-v1.0
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）
        """
    )
    
    parser.add_argument(
        'command',
        choices=['scan', 'readme', 'install-hooks'],
        nargs='?',
        default='scan',
        help='命令：scan(扫描) / readme(生成README) / install-hooks(安装Git hooks)'
    )
    
    parser.add_argument(
        '--path',
        type=Path,
        default=Path.cwd(),
        help='扫描路径（默认：当前目录）'
    )
    
    parser.add_argument(
        '--name',
        type=str,
        default='项目名称',
        help='项目名称（用于生成README）'
    )
    
    parser.add_argument(
        '--check',
        action='store_true',
        help='检查模式（用于Git hook，发现违规返回非0）'
    )
    
    args = parser.parse_args()
    
    # 打印标题
    print("\n" + "=" * 60)
    print("CNSH文化守护系统 v1.0")
    print("DNA追溯码: #龍芯⚡️2026-03-10-文化守护-v1.0")
    print("创建者: UID9622 诸葛鑫（龍芯北辰）")
    print("理论指导: 曾仕强老师（永恒显示）")
    print("=" * 60)
    
    # 执行命令
    if args.check or args.command == 'scan':
        扫描器 = CNSH代码扫描器(args.path)
        扫描结果 = 扫描器.扫描()
        通过检查 = 扫描器.生成报告()
        
        if args.check and not 通过检查:
            sys.exit(1)
        
        # 保存扫描结果
        结果文件 = args.path / 'cnsh_scan_result.json'
        with open(结果文件, 'w', encoding='utf-8') as f:
            json.dump(扫描结果, f, ensure_ascii=False, indent=2)
        print(f"📝 扫描结果已保存: {结果文件}\n")
    
    elif args.command == 'readme':
        # 先扫描
        扫描器 = CNSH代码扫描器(args.path)
        扫描结果 = 扫描器.扫描()
        
        # 生成README
        生成器 = 中文README生成器()
        生成器.生成(args.name, 扫描结果, args.path / '说明.md')
        
        print("\n💡 提示: 主README已生成为'说明.md'")
        print("   可以创建README_EN.md作为英文版本\n")
    
    elif args.command == 'install-hooks':
        生成器 = GitHooks生成器()
        生成器.生成(args.path)
        print("\n💡 提示: Git hook已安装")
        print("   每次commit前会自动检查文化主权\n")

if __name__ == '__main__':
    主函数()
