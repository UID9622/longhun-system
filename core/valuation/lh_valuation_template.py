#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 估值报告模板引擎 v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
DNA: #龍芯⚡️丙午·丙申·丁巳·丙午·䷃蒙-VALUATION-TEMPLATE-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能:
  1. 读取 VALUATION-TEMPLATE.md 模板
  2. 读取 JSON 配置文件填充变量
  3. 支持 {{var}} / {{#if}} / {{#each}} 语法
  4. 输出完整估值报告 Markdown
  5. 可选联动 generate_excel.py 生成 Excel 模型

用法:
  # 用默认配置（v1.1）生成报告
  python3 core/valuation/lh_valuation_template.py

  # 用自定义配置生成
  python3 core/valuation/lh_valuation_template.py --config my-project.json

  # 同时生成 Excel 模型
  python3 core/valuation/lh_valuation_template.py --excel

  # 输出到指定路径
  python3 core/valuation/lh_valuation_template.py --output reports/my-valuation.md

  # 新建项目（交互式初始化配置）
  python3 core/valuation/lh_valuation_template.py --init

  # 集成 lh:
  #   lh valuation --config xxx.json
  #   lh valuation --init
  #   lh valuation --excel
"""

import os
import sys
import json
import re
import copy
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# ─── 路径常量 ───
ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATE_PATH = ROOT / "core" / "valuation" / "VALUATION-TEMPLATE.md"
DEFAULT_CONFIG = ROOT / "core" / "valuation" / "v1.1-config.json"
OUTPUT_DEFAULT = ROOT / "articles" / "估值报告-生成.md"


# ─── 轻量模板引擎 ───
class SimpleTemplate:
    """
    支持三种语法:
      {{VAR}}           → 简单变量替换
      {{#if VAR}}...{{/if}}        → 条件块
      {{#each LIST}}...{{/each}}   → 循环块(支持 {{INDEX}} / {{INDEX0}} / {{../VAR}})

    优化点:
      - 正则编译一次·复用
      - 循环块单层展开·配置层预渲染嵌套表格·避免递归爆炸
      - 空占位符统一清理
    """

    # 预编译正则（类级·所有实例共享）
    _RE_IF = re.compile(r'\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}', re.DOTALL)
    _RE_EACH = re.compile(r'\{\{#each\s+(\w+)\}\}(.*?)\{\{/each\}\}', re.DOTALL)
    _RE_VAR = re.compile(r'\{\{(\w+)\}\}')
    _RE_PARENT_VAR = re.compile(r'\{\{\.\./(\w+)\}\}')
    _RE_BLANK = re.compile(r'\{\{[^}]+\}\}')
    _RE_EMPTY_LINES = re.compile(r'\n{3,}')

    def render(self, template_str: str, data: dict) -> str:
        result = template_str

        # 1. 条件块
        result = self._RE_IF.sub(self._make_if_replacer(data), result)

        # 2. 循环块（单层·配置已扁平化）
        result = self._RE_EACH.sub(self._make_each_replacer(data), result)

        # 3. 简单变量
        result = self._RE_VAR.sub(self._make_var_replacer(data), result)

        # 4. 清理多余空行
        result = self._RE_EMPTY_LINES.sub('\n\n', result)
        return result

    @staticmethod
    def _make_if_replacer(data: dict):
        def replacer(m):
            var_name = m.group(1)
            block_content = m.group(2)
            if var_name in data and data[var_name]:
                return block_content
            return ''
        return replacer

    @staticmethod
    def _make_each_replacer(data: dict):
        def replacer(m):
            list_name = m.group(1)
            item_template = m.group(2)
            items = data.get(list_name, [])
            if not items:
                return ''

            rendered = []
            for idx, item in enumerate(items):
                rendered_item = item_template

                # 替换 item 内字符串变量
                for key, val in item.items():
                    if isinstance(val, str):
                        rendered_item = rendered_item.replace('{{' + key + '}}', val)

                # 索引
                rendered_item = rendered_item.replace('{{INDEX}}', str(idx + 1))
                rendered_item = rendered_item.replace('{{INDEX0}}', str(idx))

                # 父级变量引用 {{../VAR}}
                rendered_item = SimpleTemplate._RE_PARENT_VAR.sub(
                    lambda mm: str(data.get(mm.group(1), '')), rendered_item
                )

                # 清理未替换占位符
                rendered_item = SimpleTemplate._RE_BLANK.sub('', rendered_item)
                rendered.append(rendered_item)

            return ''.join(rendered)
        return replacer

    @staticmethod
    def _make_var_replacer(data: dict):
        def replacer(m):
            key = m.group(1)
            if key in data:
                val = data[key]
                if isinstance(val, (list, dict)):
                    return f'{{{{{key}}}}}'  # 未展开的列表/字典保持原样
                return str(val)
            return f'{{{{{key}}}}}'
        return replacer


# ─── CLI ───
def load_config(config_path):
    """加载 JSON 配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_config(config: dict, strict: bool = False) -> list:
    """
    校验配置完整性。
    strict=False 时只检查核心字段；strict=True 检查所有估值数字字段。
    返回问题列表（空列表=通过）。
    """
    issues = []

    required_top = [
        'PROJECT_NAME', 'VERSION', 'DNA_STAMP', 'AUTHOR', 'DATE',
        'VALUATION_SUBJECT', 'VALUATION_DATE', 'BOTTOM_LINE',
        'WEIGHTED_BENCHMARK', 'PERSON_YEARS',
        'SCENARIO_ULTRA_CONSERVATIVE', 'SCENARIO_CONSERVATIVE',
        'SCENARIO_REASONABLE', 'SCENARIO_OPTIMISTIC',
    ]
    for key in required_top:
        if key not in config or config[key] in (None, '', '待计算', '待定义'):
            issues.append(f"缺少或待填写核心字段: {key}")

    # 数组字段类型检查
    for arr_key in ['DIMENSIONS', 'DIMENSION_SCENARIO_BEHAVIOR', 'DIMENSION_DETAILS',
                    'SENSITIVITY_VARS', 'RISKS', 'MILESTONES', 'ASSUMPTIONS',
                    'BENCHMARKS', 'VERSION_HISTORY']:
        if arr_key in config and not isinstance(config[arr_key], list):
            issues.append(f"{arr_key} 应为列表")

    if strict:
        numeric_keys = [
            'SCENARIO_ULTRA_CONSERVATIVE', 'SCENARIO_CONSERVATIVE',
            'SCENARIO_REASONABLE', 'SCENARIO_OPTIMISTIC',
            'WEIGHTED_BENCHMARK_NUMERIC', 'W_ULTRA_CONSERVATIVE',
            'W_CONSERVATIVE', 'W_REASONABLE', 'W_OPTIMISTIC',
            'W_W1', 'W_W2', 'W_W3', 'W_W4',
            'W_C1', 'W_C2', 'W_C3', 'W_C4', 'W_TOTAL',
        ]
        for key in numeric_keys:
            if key in config:
                val = config[key]
                if isinstance(val, str):
                    val = val.replace(',', '').replace('万', '').replace('亿', '').strip()
                # 支持 "71%" / "5,325.8 ≈ 5,326" / "1,380万" / "0.53亿"
                if isinstance(val, str):
                    val = val.split()[0].replace(',', '').replace('万', '').replace('亿', '').strip()
                    if val.endswith('%'):
                        val = val[:-1]
                try:
                    float(val)
                except (ValueError, TypeError):
                    issues.append(f"数值字段无法解析: {key}={config[key]}")

    return issues


def generate_report(config, output_path):
    """填充模板，生成报告"""
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template_str = f.read()

    engine = SimpleTemplate()
    filled = engine.render(template_str, config)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(filled)

    return output


def run_excel_generator(config_path):
    """调用 generate_excel.py 生成 Excel 模型（传入对应配置）"""
    gen_script = ROOT / "core" / "valuation" / "generate_excel.py"
    if not gen_script.exists():
        return False, "", "generate_excel.py not found"

    cmd = [sys.executable, str(gen_script)]
    if config_path:
        cmd.extend(["--config", str(config_path)])
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr


def interactive_init():
    """交互式新建项目配置"""
    print("🐉 龍魂估值报告模板 · 项目初始化")
    print("=" * 50)

    config = copy.deepcopy(MINIMAL_CONFIG)

    config['PROJECT_NAME'] = input("项目名称: ").strip() or "未命名项目"
    config['AUTHOR'] = input("创建者（格式: 姓名（UID））: ").strip() or "待填写"
    config['VERSION'] = input("版本号 [v1.0]: ").strip() or "v1.0"
    config['DATE'] = input(f"日期 [{datetime.now().strftime('%Y-%m-%d')}]: ").strip() or datetime.now().strftime('%Y-%m-%d')
    config['VALUATION_SUBJECT'] = input("评估对象: ").strip() or config['PROJECT_NAME']

    # 人年
    py = input("总人年工作量 [20]: ").strip()
    if py.isdigit():
        config['PERSON_YEARS'] = int(py)
        config['SCENARIO_ULTRA_CONSERVATIVE'] = str(int(py) * 40)
        config['BOTTOM_LINE'] = f"{int(py) * 40}万"
    else:
        config['PERSON_YEARS'] = 20
        config['SCENARIO_ULTRA_CONSERVATIVE'] = "800"
        config['BOTTOM_LINE'] = "800万"

    config['SCENARIO_ULTRA_CONSERVATIVE_YI'] = f"{int(config['SCENARIO_ULTRA_CONSERVATIVE'])/10000:.2f}亿"

    # 维度选择
    print("\n估值维度（y/n）:")
    dims = []
    dim_map = {
        '技术资产': ('技术资产', 1380, 5520, 6900, 8280),
        '文化/品牌': ('文化主权', 0, 2070, 3450, 4140),
        '叙事/IP': ('战略叙事', 0, 1380, 3060, 4140),
        '生态潜力': ('生态潜力', 0, 2430, 3690, 5620),
    }
    for d in dim_map:
        ans = input(f"  包含「{d}」? [Y/n]: ").strip().lower()
        if ans != 'n':
            dims.append(d)
    config['DIMENSION_COUNT'] = str(len(dims)) if dims else '1'
    config['DIMENSION_LIST'] = '、'.join(dim_map[d][0] for d in dims)

    # 自动计算场景合计（基于所选维度）
    # 技术资产的极度保守用输入人年×40万/年；其他维度按预设系数
    tech_ultra = int(config['PERSON_YEARS']) * 40 if '技术资产' in dims else 0
    ultra = tech_ultra + sum(dim_map[d][1] for d in dims if d != '技术资产')
    conservative = tech_ultra + sum(dim_map[d][2] for d in dims if d != '技术资产')
    reasonable = tech_ultra + sum(dim_map[d][3] for d in dims if d != '技术资产')
    optimistic = tech_ultra + sum(dim_map[d][4] for d in dims if d != '技术资产')

    config['SCENARIO_ULTRA_CONSERVATIVE'] = f"{ultra:,}"
    config['SCENARIO_ULTRA_CONSERVATIVE_YI'] = f"{ultra/10000:.2f}亿"
    config['BOTTOM_LINE'] = f"{ultra}万"
    config['SCENARIO_CONSERVATIVE'] = f"{conservative:,}"
    config['SCENARIO_CONSERVATIVE_YI'] = f"{conservative/10000:.2f}亿"
    config['SCENARIO_REASONABLE'] = f"{reasonable:,}"
    config['SCENARIO_REASONABLE_YI'] = f"{reasonable/10000:.2f}亿"
    config['SCENARIO_OPTIMISTIC'] = f"{optimistic:,}"
    config['SCENARIO_OPTIMISTIC_YI'] = f"{optimistic/10000:.2f}亿"

    # 加权基准（默认权重 65/18/12/5%，可按需调整）
    weights = [0.65, 0.18, 0.12, 0.05]
    w_total = round(
        ultra * weights[0] +
        conservative * weights[1] +
        reasonable * weights[2] +
        optimistic * weights[3]
    )
    config['WEIGHTED_BENCHMARK_NUMERIC'] = f"{w_total:,}"
    config['WEIGHTED_BENCHMARK_YI'] = f"{w_total/10000:.2f}亿"
    config['WEIGHTED_BENCHMARK'] = f"{w_total:,}万 ≈ {w_total/10000:.2f}亿"
    config['WEIGHT_DISTRIBUTION'] = "65/18/12/5%"

    # 加权表字段
    config['W_ULTRA_CONSERVATIVE'] = f"{ultra:,}"
    config['W_CONSERVATIVE'] = f"{conservative:,}"
    config['W_REASONABLE'] = f"{reasonable:,}"
    config['W_OPTIMISTIC'] = f"{optimistic:,}"
    config['W_W1'] = "65%"
    config['W_W2'] = "18%"
    config['W_W3'] = "12%"
    config['W_W4'] = "5%"
    config['W_C1'] = f"{round(ultra * weights[0]):,}"
    config['W_C2'] = f"{round(conservative * weights[1]):,}"
    config['W_C3'] = f"{round(reasonable * weights[2]):,}"
    config['W_C4'] = f"{round(optimistic * weights[3]):,}"
    config['W_TOTAL'] = f"{w_total:,}"

    config['SENSITIVITY_BASE'] = f"{reasonable:,}万"
    config['PITCH_TEXT'] = (
        f"{config['PROJECT_NAME']}估值底线{config['BOTTOM_LINE']}"
        f"（{config['PERSON_YEARS']}人年市场重置成本·谁都能复算），"
        f"加权基准{config['WEIGHTED_BENCHMARK']}。"
        "具体估值由市场谈判决定。"
    )

    # 输出路径
    output_name = input(f"输出文件名 [估值报告-{config['PROJECT_NAME']}.md]: ").strip()
    if not output_name:
        output_name = f"估值报告-{config['PROJECT_NAME']}.md"

    config_path = ROOT / "core" / "valuation" / f"{config['PROJECT_NAME']}-config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 配置已保存: {config_path}")
    print(f"   下一步: python3 core/valuation/lh_valuation_template.py --config {config_path.name}")
    return config_path, output_name


# ─── 最小配置模板（供 --init 使用）───
MINIMAL_CONFIG = {
    "PROJECT_NAME": "未命名项目",
    "VERSION": "v1.0",
    "DNA_STAMP": "#龍芯⚡️待填写-VALUATION-v1.0",
    "AUTHOR": "待填写",
    "LICENSE": "CC BY-NC-SA 4.0（思想层）",
    "DATE": datetime.now().strftime("%Y-%m-%d"),
    "AUDIT_CHAIN": "待审计",
    "EXCEL_PATH": "core/valuation/valuation-model.xlsx",
    "EXCEL_SHEETS": "N",
    "EXCEL_VALIDATION": "待验证",
    "VALUATION_SUBJECT": "待定义",
    "VALUATION_DATE": datetime.now().strftime("%Y-%m-%d"),
    "VALUATION_METHODS": "成本法 + 收益法",
    "VALUATION_PURPOSE": "内部参考",
    "BOTTOM_LINE": "待计算",
    "WEIGHTED_BENCHMARK": "待计算",
    "PERSON_YEARS": "20",
    "SCENARIO_ULTRA_CONSERVATIVE": "待计算",
    "SCENARIO_ULTRA_CONSERVATIVE_YI": "待计算",
    "SCENARIO_CONSERVATIVE": "待计算",
    "SCENARIO_CONSERVATIVE_YI": "待计算",
    "SCENARIO_REASONABLE": "待计算",
    "SCENARIO_REASONABLE_YI": "待计算",
    "SCENARIO_OPTIMISTIC": "待计算",
    "SCENARIO_OPTIMISTIC_YI": "待计算",
    "WEIGHTED_BENCHMARK_NUMERIC": "待计算",
    "WEIGHTED_BENCHMARK_YI": "待计算",
    "WEIGHT_DISTRIBUTION": "待定义",
    "PITCH_TEXT": "待定义",
    "FIXES_SECTION": False,
    "FIXES_TITLE": "",
    "FIXES": [],
    "DIMENSION_COUNT": "4",
    "DIMENSION_LIST": "待定义",
    "DIMENSIONS": [],
    "DIMENSION_SCENARIO_BEHAVIOR": [],
    "DIMENSION_DETAILS": [],
    "W_ULTRA_CONSERVATIVE": "待计算",
    "W_CONSERVATIVE": "待计算",
    "W_REASONABLE": "待计算",
    "W_OPTIMISTIC": "待计算",
    "W_W1": "待定义",
    "W_W2": "待定义",
    "W_W3": "待定义",
    "W_W4": "待定义",
    "W_C1": "待计算",
    "W_C2": "待计算",
    "W_C3": "待计算",
    "W_C4": "待计算",
    "W_TOTAL": "待计算",
    "WEIGHT_RATIONALE": "待定义",
    "SENSITIVITY_BASE": "待计算",
    "SENSITIVITY_RANGE": "30%",
    "SENSITIVITY_VARS": [],
    "SENSITIVITY_NOTE": "待定义",
    "RISKS": [],
    "TOTAL_DISCOUNT_RATE": "待计算",
    "MILESTONES": [],
    "ASSUMPTIONS": [],
    "VALIDITY_PERIOD": "12个月",
    "EVALUATOR": "创始团队",
    "BENCHMARKS": [],
    "VERSION_HISTORY": [],
    "FOOTER_TEXT": "本报告基于公开模型生成·不可用于交易定价·融资请第三方评估",
    "CONFIRM_CODE": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "TRICOLOR_STATUS": "🟡 主观假设占比高·需第三方复核 🔴 不可用于交易定价",
    "CONFIG_PATH": "core/valuation/MINIMAL-config.json"
}


# ─── 入口 ───
def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂估值报告模板引擎 — 从模板+配置生成估值报告"
    )
    parser.add_argument(
        '--config', '-c',
        default=str(DEFAULT_CONFIG),
        help=f'配置文件路径 (默认: {DEFAULT_CONFIG})'
    )
    parser.add_argument(
        '--output', '-o',
        default=None,
        help='输出路径 (默认: articles/估值报告-生成.md)'
    )
    parser.add_argument(
        '--excel', '-e',
        action='store_true',
        help='同步生成 Excel 估值模型'
    )
    parser.add_argument(
        '--init', '-i',
        action='store_true',
        help='交互式新建项目配置'
    )
    parser.add_argument(
        '--list-configs', '-l',
        action='store_true',
        help='列出所有可用配置文件'
    )
    parser.add_argument(
        '--stamp',
        action='store_true',
        help='生成后输出时间戳（默认已开启）'
    )
    parser.add_argument(
        '--validate', '-V',
        action='store_true',
        help='仅校验配置文件·不生成报告'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='校验时启用严格模式（检查所有数值字段）'
    )

    args = parser.parse_args()

    # 交互式初始化
    if args.init:
        config_path, output_name = interactive_init()
        print(f"\n生成报告:")
        config = load_config(config_path)
        output_path = ROOT / "articles" / output_name
        result = generate_report(config, output_path)
        print(f"✅ 报告: {result}")
        _print_stamp()
        return 0

    # 列出配置
    if args.list_configs:
        val_dir = ROOT / "core" / "valuation"
        configs = list(val_dir.glob("*-config.json"))
        print("可用配置文件:")
        for c in configs:
            print(f"  {c.name}")
            if c == DEFAULT_CONFIG:
                print("    ↑ 默认")
        return 0

    # 加载配置
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"❌ 配置文件不存在: {config_path}")
        print(f"\n试试 --init 新建项目 或 --list-configs 查看已有配置")
        return 1

    config = load_config(config_path)

    # 配置校验
    issues = validate_config(config, strict=args.strict)
    if issues:
        print(f"❌ 配置校验失败 ({len(issues)} 项):")
        for issue in issues:
            print(f"   · {issue}")
        return 1

    if args.validate:
        print(f"✅ 配置校验通过: {config_path}")
        return 0

    # 输出路径
    output_path = args.output or ROOT / "articles" / f"估值报告-{config.get('PROJECT_NAME', '生成')}.md"

    # 生成报告
    result = generate_report(config, output_path)
    print(f"✅ 估值报告: {result}")
    print(f"   项目: {config.get('PROJECT_NAME', 'N/A')}")
    print(f"   版本: {config.get('VERSION', 'N/A')}")
    print(f"   底线: {config.get('BOTTOM_LINE', 'N/A')}")
    print(f"   加权基准: {config.get('WEIGHTED_BENCHMARK', 'N/A')}")

    # 同步生成 Excel
    if args.excel:
        print("\n📊 生成 Excel 模型...")
        ok, stdout, stderr = run_excel_generator(config_path)
        if ok:
            print("✅ Excel 模型已生成")
            if stdout.strip():
                print(stdout.strip())
        else:
            print(f"❌ Excel 生成失败: {stderr}")

    # 时间戳（默认输出·--stamp 保留以兼容旧调用）
    _print_stamp()

    return 0


def _print_stamp():
    """输出时间戳"""
    try:
        te = ROOT / "bin" / "lh_time_engine.py"
        if te.exists():
            r = subprocess.run(
                [sys.executable, str(te), '--stamp'],
                capture_output=True, text=True, timeout=5
            )
            if r.stdout.strip():
                print(f"\n{r.stdout.strip()}")
    except Exception:
        pass


if __name__ == '__main__':
    sys.exit(main())
