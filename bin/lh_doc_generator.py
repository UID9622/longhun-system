#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·系统文档生成器 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰-文档生成-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

定位：系统说明页的标准结构生成器
负责人格：🤖 宝宝
职责：文档标准化、自动生成、批量处理

核心功能：
  1. 标准文档模板 — 包含所有必要信息
  2. 交互式输入 — 逐步引导填写
  3. 批量生成 — 从JSON批量创建
  4. 文档版本管理 — 自动更新版本号
  5. 导出多种格式 — Markdown/JSON/HTML
  6. 关联链接自动生成 — 智能推荐
  7. DNA自动生成 — 符合规范
  8. 负责人格推荐 — 根据功能自动匹配
"""

import json
import uuid
import hashlib
import datetime
import re
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import argparse

# ============================================================
# 一、数据结构
# ============================================================

@dataclass
class 文档信息:
    """文档信息"""
    系统名称: str
    DNA追溯码: str
    确认码: str
    版本: str
    最后更新: str
    系统定位: str
    核心功能: List[str]
    使用方式: str
    负责人格: str
    相关链接: List[Dict[str, str]]
    创建时间: str = ""
    标签: List[str] = field(default_factory=list)
    依赖系统: List[str] = field(default_factory=list)
    注意事项: List[str] = field(default_factory=list)

@dataclass
class 文档生成配置:
    """文档生成配置"""
    输出格式: str = "markdown"  # markdown, json, html
    输出路径: str = "./docs"
    自动版本: bool = True
    包含示例: bool = True
    包含关联: bool = True
    模板风格: str = "standard"  # standard, minimal, detailed


# ============================================================
# 二、人格推荐器
# ============================================================

class 人格推荐器:
    """根据功能自动推荐负责人格"""

    人格映射 = {
        "安全": "上帝之眼",
        "审计": "上帝之眼",
        "监控": "上帝之眼",
        "检测": "上帝之眼",
        "记忆": "宝宝",
        "模板": "宝宝",
        "文档": "宝宝",
        "协调": "宝宝",
        "决策": "诸葛亮",
        "推演": "诸葛亮",
        "战略": "诸葛亮",
        "分析": "诸葛亮",
        "执行": "鲁班",
        "技术": "鲁班",
        "开发": "鲁班",
        "优化": "雯雯",
        "整理": "雯雯",
        "归档": "雯雯",
        "治理": "文心",
        "原则": "文心",
        "哲学": "文心",
        "计算": "数学大师",
        "数据": "数学大师",
        "财务": "管仲",
    }

    @classmethod
    def 推荐(cls, 功能列表: List[str]) -> str:
        """根据功能列表推荐人格"""
        人格投票 = {}

        for 功能 in 功能列表:
            for 关键词, 人格 in cls.人格映射.items():
                if 关键词 in 功能:
                    人格投票[人格] = 人格投票.get(人格, 0) + 1

        if not 人格投票:
            return "宝宝"  # 默认

        return max(人格投票, key=人格投票.get)


# ============================================================
# 三、DNA生成器
# ============================================================

class DNA生成器:
    """自动生成符合规范的DNA追溯码"""

    @classmethod
    def 生成(cls, 系统名称: str = "", 系统类型: str = "") -> str:
        """生成DNA追溯码"""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        前缀 = "#龍芯⚡️"
        today_str = today

        # 从系统名称提取标识
        if 系统名称:
            标识 = 系统名称[:8].replace(" ", "-")
        elif 系统类型:
            标识 = 系统类型[:8].replace(" ", "-")
        else:
            标识 = "DOC"

        后缀 = uuid.uuid4().hex[:6].upper()
        return f"{前缀}{today_str}-{标识}-{后缀}"


# ============================================================
# 四、确认码生成器
# ============================================================

class 确认码生成器:
    """生成确认码"""

    @classmethod
    def 生成(cls) -> str:
        """生成确认码"""
        后缀 = uuid.uuid4().hex[:6].upper()
        return f"#CONFIRM🌌9622-{后缀}"


# ============================================================
# 五、文档生成器
# ============================================================

class 文档生成器:
    """标准文档生成器"""

    def __init__(self, 配置: Optional[文档生成配置] = None):
        self.配置 = 配置 or 文档生成配置()
        self.输出目录 = Path(self.配置.输出路径)
        self.输出目录.mkdir(parents=True, exist_ok=True)

    def 生成(self, 信息: 文档信息) -> Dict:
        """生成完整文档"""
        # 自动补充缺失信息
        信息 = self._补全信息(信息)

        # 根据格式生成
        if self.配置.输出格式 == "markdown":
            内容 = self._生成Markdown(信息)
        elif self.配置.输出格式 == "json":
            内容 = self._生成JSON(信息)
        elif self.配置.输出格式 == "html":
            内容 = self._生成HTML(信息)
        else:
            内容 = self._生成Markdown(信息)

        # 保存文件
        文件路径 = self._保存文件(信息.系统名称, 内容)

        return {
            "状态": "成功",
            "信息": asdict(信息),
            "内容": 内容,
            "文件路径": str(文件路径),
            "格式": self.配置.输出格式
        }

    def _补全信息(self, 信息: 文档信息) -> 文档信息:
        """补全缺失信息"""
        # 补全DNA
        if not 信息.DNA追溯码:
            信息.DNA追溯码 = DNA生成器.生成(信息.系统名称)

        # 补全确认码
        if not 信息.确认码:
            信息.确认码 = 确认码生成器.生成()

        # 补全版本
        if not 信息.版本:
            信息.版本 = "v1.0"

        # 补全最后更新
        if not 信息.最后更新:
            信息.最后更新 = datetime.datetime.now().strftime("%Y-%m-%d")

        # 补全负责人格
        if not 信息.负责人格:
            信息.负责人格 = 人格推荐器.推荐(信息.核心功能)

        # 补全创建时间
        if not 信息.创建时间:
            信息.创建时间 = datetime.datetime.now().isoformat()

        return 信息

    def _生成Markdown(self, 信息: 文档信息) -> str:
        """生成Markdown格式"""
        行 = []

        # 标题
        行.append(f"# {信息.系统名称}")
        行.append("")
        行.append(f"**DNA追溯码**：{信息.DNA追溯码}")
        行.append(f"**确认码**：{信息.确认码}")
        行.append(f"**版本**：{信息.版本}")
        行.append(f"**最后更新**：{信息.最后更新}")
        行.append("")
        行.append("---")
        行.append("")
        if 信息.标签:
            行.append(f"**标签**：{', '.join(信息.标签)}")
            行.append("")
        行.append("## 系统定位")
        行.append("")
        行.append(信息.系统定位)
        行.append("")
        行.append("## 核心功能")
        行.append("")
        for idx, 功能 in enumerate(信息.核心功能, 1):
            行.append(f"{idx}. {功能}")
        行.append("")
        行.append("## 使用方式")
        行.append("")
        行.append(信息.使用方式)
        行.append("")
        行.append("## 负责人格")
        行.append("")
        行.append(f"👤 {信息.负责人格}")
        行.append("")

        if 信息.依赖系统:
            行.append("## 依赖系统")
            行.append("")
            for 依赖 in 信息.依赖系统:
                行.append(f"- {依赖}")
            行.append("")

        if 信息.注意事项:
            行.append("## 注意事项")
            行.append("")
            for 注意 in 信息.注意事项:
                行.append(f"- {注意}")
            行.append("")

        if 信息.相关链接:
            行.append("## 相关链接")
            行.append("")
            for 链接 in 信息.相关链接:
                行.append(f"- {链接.get('名称', '链接')}: {链接.get('URL', '')}")
            行.append("")

        行.append("---")
        行.append("")
        行.append(f"*创建时间：{信息.创建时间}*")

        return "\n".join(行)

    def _生成JSON(self, 信息: 文档信息) -> str:
        """生成JSON格式"""
        return json.dumps(asdict(信息), ensure_ascii=False, indent=2)

    def _生成HTML(self, 信息: 文档信息) -> str:
        """生成HTML格式"""
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{信息.系统名称}</title>
    <style>
        body {{ font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.8; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .dna {{ background: #f8f9fa; padding: 10px 15px; border-radius: 5px; font-family: monospace; }}
        .tag {{ display: inline-block; background: #e8f4f8; padding: 2px 10px; border-radius: 12px; margin: 2px; font-size: 14px; }}
        .meta {{ color: #7f8c8d; font-size: 14px; }}
        .function {{ padding: 5px 0; }}
        .persona {{ font-size: 18px; color: #2c3e50; }}
        hr {{ border: none; border-top: 1px solid #ecf0f1; margin: 30px 0; }}
    </style>
</head>
<body>
    <h1>🐉 {信息.系统名称}</h1>
    <div class="meta">
        <p><strong>DNA追溯码：</strong><span class="dna">{信息.DNA追溯码}</span></p>
        <p><strong>确认码：</strong><span class="dna">{信息.确认码}</span></p>
        <p><strong>版本：</strong>{信息.版本} | <strong>最后更新：</strong>{信息.最后更新}</p>
        <p>"""
        if 信息.标签:
            html += "标签："
            for 标签 in 信息.标签:
                html += f'<span class="tag">{标签}</span> '
        html += f"""</p>
    </div>

    <hr>

    <h2>🎯 系统定位</h2>
    <p>{信息.系统定位}</p>

    <h2>⚡ 核心功能</h2>
    <ul>
"""
        for 功能 in 信息.核心功能:
            html += f'        <li class="function">{功能}</li>\n'
        html += f"""    </ul>

    <h2>📖 使用方式</h2>
    <p>{信息.使用方式}</p>

    <h2>👤 负责人格</h2>
    <p class="persona">{信息.负责人格}</p>
"""

        if 信息.依赖系统:
            html += f"""    <h2>🔗 依赖系统</h2>
    <ul>
"""
            for 依赖 in 信息.依赖系统:
                html += f'        <li>{依赖}</li>\n'
            html += f"""    </ul>
"""

        if 信息.注意事项:
            html += f"""    <h2>⚠️ 注意事项</h2>
    <ul>
"""
            for 注意 in 信息.注意事项:
                html += f'        <li>{注意}</li>\n'
            html += f"""    </ul>
"""

        if 信息.相关链接:
            html += f"""    <h2>🔗 相关链接</h2>
    <ul>
"""
            for 链接 in 信息.相关链接:
                html += f'        <li><a href="{链接.get("URL", "")}">{链接.get("名称", "链接")}</a></li>\n'
            html += f"""    </ul>
"""

        html += f"""
    <hr>
    <p class="meta">创建时间：{信息.创建时间}</p>
</body>
</html>"""
        return html

    def _保存文件(self, 系统名称: str, 内容: str) -> Path:
        """保存文件"""
        safe_name = 系统名称.replace(" ", "_").replace("/", "_")
        ext = {
            "markdown": "md",
            "json": "json",
            "html": "html"
        }.get(self.配置.输出格式, "md")

        文件名 = f"{safe_name}.{ext}"
        文件路径 = self.输出目录 / 文件名

        # 处理重名
        counter = 1
        while 文件路径.exists():
            文件名 = f"{safe_name}_{counter}.{ext}"
            文件路径 = self.输出目录 / 文件名
            counter += 1

        with open(文件路径, 'w', encoding='utf-8') as f:
            f.write(内容)

        return 文件路径


# ============================================================
# 六、批量生成器
# ============================================================

class 批量生成器:
    """从JSON批量生成文档"""

    def __init__(self):
        self.生成器 = 文档生成器()

    def 从JSON(self, json_路径: str) -> List[Dict]:
        """从JSON文件批量生成"""
        with open(json_路径, 'r', encoding='utf-8') as f:
            数据 = json.load(f)

        结果列表 = []

        if isinstance(数据, list):
            for 项 in 数据:
                信息 = 文档信息(
                    系统名称=项.get("系统名称", "未命名系统"),
                    DNA追溯码=项.get("DNA追溯码", ""),
                    确认码=项.get("确认码", ""),
                    版本=项.get("版本", ""),
                    最后更新=项.get("最后更新", ""),
                    系统定位=项.get("系统定位", ""),
                    核心功能=项.get("核心功能", []),
                    使用方式=项.get("使用方式", ""),
                    负责人格=项.get("负责人格", ""),
                    相关链接=项.get("相关链接", []),
                    创建时间=项.get("创建时间", ""),
                    标签=项.get("标签", []),
                    依赖系统=项.get("依赖系统", []),
                    注意事项=项.get("注意事项", [])
                )
                结果 = self.生成器.生成(信息)
                结果列表.append(结果)
        else:
            # 单个对象
            信息 = 文档信息(
                系统名称=数据.get("系统名称", "未命名系统"),
                DNA追溯码=数据.get("DNA追溯码", ""),
                确认码=数据.get("确认码", ""),
                版本=数据.get("版本", ""),
                最后更新=数据.get("最后更新", ""),
                系统定位=数据.get("系统定位", ""),
                核心功能=数据.get("核心功能", []),
                使用方式=数据.get("使用方式", ""),
                负责人格=数据.get("负责人格", ""),
                相关链接=数据.get("相关链接", []),
                创建时间=数据.get("创建时间", ""),
                标签=数据.get("标签", []),
                依赖系统=数据.get("依赖系统", []),
                注意事项=数据.get("注意事项", [])
            )
            结果 = self.生成器.生成(信息)
            结果列表.append(结果)

        return 结果列表


# ============================================================
# 七、交互式输入
# ============================================================

class 交互式输入:
    """交互式引导输入"""

    @classmethod
    def 引导(cls) -> 文档信息:
        """引导用户输入"""
        print("\n" + "=" * 60)
        print("🐉 龙魂·系统文档生成器 - 交互模式")
        print("=" * 60)

        # 系统名称
        名称 = input("📌 系统名称: ").strip()
        while not 名称:
            名称 = input("❌ 系统名称不能为空，请重新输入: ").strip()

        # 系统定位
        定位 = input("📝 系统定位（一句话描述）: ").strip()
        while not 定位:
            定位 = input("❌ 系统定位不能为空: ").strip()

        # 核心功能
        print("\n📋 核心功能（每行一个，输入空行结束）:")
        功能列表 = []
        while True:
            功能 = input("  - ").strip()
            if not 功能:
                break
            功能列表.append(功能)
        if not 功能列表:
            功能列表 = ["待补充"]

        # 使用方式
        使用方式 = input("\n📖 使用方式: ").strip()
        while not 使用方式:
            使用方式 = input("❌ 使用方式不能为空: ").strip()

        # 负责人格（可选）
        负责人格 = input("\n👤 负责人格（回车自动推荐）: ").strip()
        if not 负责人格:
            负责人格 = 人格推荐器.推荐(功能列表)
            print(f"   🤖 自动推荐: {负责人格}")

        # 标签
        标签输入 = input("\n🏷️ 标签（用逗号分隔，可选）: ").strip()
        标签 = [t.strip() for t in 标签输入.split(',') if t.strip()] if 标签输入 else []

        # 确认
        print("\n" + "=" * 60)
        print("📋 文档信息确认:")
        print(f"  名称: {名称}")
        print(f"  定位: {定位}")
        print(f"  功能: {len(功能列表)} 项")
        print(f"  人格: {负责人格}")
        if 标签:
            print(f"  标签: {', '.join(标签)}")

        确认 = input("\n✅ 确认生成? (y/n): ").strip().lower()
        if 确认 != 'y':
            print("❌ 已取消")
            return None

        return 文档信息(
            系统名称=名称,
            DNA追溯码="",
            确认码="",
            版本="",
            最后更新="",
            系统定位=定位,
            核心功能=功能列表,
            使用方式=使用方式,
            负责人格=负责人格,
            相关链接=[],
            创建时间="",
            标签=标签,
            依赖系统=[],
            注意事项=[]
        )


# ============================================================
# 八、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·系统文档生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互式生成
  python3 lh_doc_generator.py --interactive

  # 从参数生成
  python3 lh_doc_generator.py --name "安全检查引擎" --desc "安全风险评估" --func "检查设备" "评估风险" --usage "python3 script.py"

  # 从JSON批量生成
  python3 lh_doc_generator.py --batch docs.json

  # 指定输出格式
  python3 lh_doc_generator.py --name "测试文档" --desc "描述" --func "功能1" --output-format html

  # 查看示例
  python3 lh_doc_generator.py --example
        """
    )

    parser.add_argument("--name", type=str, help="系统名称")
    parser.add_argument("--desc", type=str, help="系统定位描述")
    parser.add_argument("--func", nargs="+", help="核心功能列表")
    parser.add_argument("--usage", type=str, help="使用方式")
    parser.add_argument("--persona", type=str, help="负责人格")
    parser.add_argument("--tags", type=str, help="标签（逗号分隔）")
    parser.add_argument("--output-format", "-f", type=str, choices=["markdown", "json", "html"], default="markdown", help="输出格式")
    parser.add_argument("--output-dir", "-o", type=str, default="./docs", help="输出目录")
    parser.add_argument("--batch", "-b", type=str, help="批量生成JSON文件路径")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--example", "-e", action="store_true", help="显示示例")
    parser.add_argument("--json-output", action="store_true", help="以JSON格式输出结果")

    args = parser.parse_args()

    # 显示示例
    if args.example:
        print("""
📋 示例文档:

# 安全检查引擎

**DNA追溯码**：#龍芯⚡️2026-07-30-安全检查-1A2B3C4D
**确认码**：#CONFIRM🌌9622-1A2B3C4D
**版本**：v1.0
**最后更新**：2026-07-30

---

## 系统定位

对设备、系统、数据访问进行安全风险评估，给出防护建议和执行动作。

## 核心功能

1. 扫描目标设备信息
2. 隐私泄露风险评估
3. 账号安全检查
4. 系统越界检测

## 使用方式

python3 lh_security_auditor.py --check "设备名" --info '{...}'

---

*负责人格：上帝之眼*

JSON批量生成示例:
{
  "系统名称": "安全检查引擎",
  "系统定位": "安全风险评估",
  "核心功能": ["功能1", "功能2"],
  "使用方式": "python3 script.py"
}
        """)
        return

    # 交互模式
    if args.interactive:
        信息 = 交互式输入.引导()
        if not 信息:
            return
        配置 = 文档生成配置(输出格式=args.output_format, 输出路径=args.output_dir)
        生成器 = 文档生成器(配置)
        结果 = 生成器.生成(信息)
        print(f"\n✅ 文档已生成: {结果['文件路径']}")
        return

    # 批量模式
    if args.batch:
        批量 = 批量生成器()
        结果列表 = 批量.从JSON(args.batch)
        print(f"\n✅ 批量生成完成: {len(结果列表)} 个文档")
        for 结果 in 结果列表:
            print(f"  - {结果['文件路径']}")
        return

    # 从参数生成
    if args.name and args.desc and args.func:
        信息 = 文档信息(
            系统名称=args.name,
            DNA追溯码="",
            确认码="",
            版本="",
            最后更新="",
            系统定位=args.desc,
            核心功能=args.func,
            使用方式=args.usage or "待补充",
            负责人格=args.persona or "",
            相关链接=[],
            创建时间="",
            标签=[t.strip() for t in args.tags.split(',')] if args.tags else [],
            依赖系统=[],
            注意事项=[]
        )

        配置 = 文档生成配置(
            输出格式=args.output_format,
            输出路径=args.output_dir
        )
        生成器 = 文档生成器(配置)
        结果 = 生成器.生成(信息)

        if args.json_output:
            print(json.dumps(结果, ensure_ascii=False, indent=2))
        else:
            print(f"\n✅ 文档已生成: {结果['文件路径']}")
            print(f"📋 DNA: {结果['信息']['DNA追溯码']}")
            print(f"👤 负责人: {结果['信息']['负责人格']}")
        return

    # 无参数时显示帮助
    parser.print_help()


if __name__ == "__main__":
    main()
