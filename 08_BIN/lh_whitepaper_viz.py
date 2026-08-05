#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
龍魂·白皮书可视化引擎 v1.0
============================
统一白皮书图表生成器。支持8种图表类型·7份白皮书自动映射·CLI一键生成。
所有白皮书可视化图表统一入口。

DNA: #龍芯⚡️2026-08-03-WHITEPAPER-VIZ-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

用法:
  python3 bin/lh_whitepaper_viz.py --whitepaper open-audit          # 单白皮书全部图表
  python3 bin/lh_whitepaper_viz.py --whitepaper all                 # 全部七份白皮书
  python3 bin/lh_whitepaper_viz.py --whitepaper open-audit --chart 1  # 指定第几张图
  python3 bin/lh_whitepaper_viz.py --list                           # 列出所有白皮书和图表
  python3 bin/lh_whitepaper_viz.py --whitepaper all --format png   # 指定输出格式
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc, Circle, Rectangle
import numpy as np
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
import json

# ============================================================
# 龍魂统一色板 (来自 LH-UNIFIED-VISUAL-COLOR-PROTOCOL-v1.0)
# ============================================================
COLORS = {
    '断空红': '#CC0000',  # P0 - 熔断
    '深渊黑': '#1A1A1A',  # P1 - 机密
    '观察紫': '#7B2D8E',  # P2 - 外部
    '主权金': '#DAA520',  # P3 - 授权
    '追踪蓝': '#2563EB',  # P4 - 系统
    '待核黄': '#E6A817',  # P5 - 警告
    '过渡银': '#B0B0B0',  # P6 - 演绎
    '放行绿': '#2E7D32',  # P7 - 通过
    'bg_dark': '#0D1117',
    'bg_card': '#161B22',
    'text_primary': '#E6EDF3',
    'text_secondary': '#8B949E',
    'border': '#30363D',
    'grid': '#21262D',
}

# Chart type color aliases
C_GREEN = COLORS['放行绿']
C_RED = COLORS['断空红']
C_YELLOW = COLORS['待核黄']
C_BLUE = COLORS['追踪蓝']
C_GOLD = COLORS['主权金']
C_PURPLE = COLORS['观察紫']
C_SILVER = COLORS['过渡银']
C_BLACK = COLORS['深渊黑']
C_BG = COLORS['bg_dark']
C_CARD = COLORS['bg_card']
C_TEXT = COLORS['text_primary']

# Chart export quality
plt.rcParams.update({
    'figure.facecolor': C_BG,
    'axes.facecolor': C_CARD,
    'axes.edgecolor': COLORS['border'],
    'axes.labelcolor': C_TEXT,
    'text.color': C_TEXT,
    'xtick.color': COLORS['text_secondary'],
    'ytick.color': COLORS['text_secondary'],
    'grid.color': COLORS['grid'],
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
    'savefig.facecolor': C_BG,
    'font.sans-serif': ['Arial Unicode MS', 'PingFang SC', 'Heiti SC', 'SimHei', 'DejaVu Sans'],
})

OUTPUT_DIR = Path(__file__).parent.parent / 'portal' / 'viz' / 'whitepapers'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 白皮书注册表
# ============================================================
WHITEPAPERS = {
    'open-audit': {
        'name': 'AI开放审计模型',
        'file': '01_protocols/LH-OPEN-AUDIT-WHITEPAPER-v2.0.md',
        'version': 'v2.0',
        'charts': [
            {'id': 1, 'name': '治理均衡热力图', 'type': 'heatmap', 'func': 'chart_open_audit_risk_heatmap'},
            {'id': 2, 'name': '五方博弈关系网络图', 'type': 'network', 'func': 'chart_open_audit_player_network'},
            {'id': 3, 'name': '六层审计架构纵剖图', 'type': 'stack', 'func': 'chart_open_audit_architecture'},
        ]
    },
    'persona': {
        'name': '20人格治理体系',
        'file': '01_protocols/LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md',
        'version': 'v1.4',
        'charts': [
            {'id': 1, 'name': '四层人格权重雷达图', 'type': 'radar', 'func': 'chart_persona_weight_radar'},
            {'id': 2, 'name': '意图→人格路由桑基图', 'type': 'sankey', 'func': 'chart_persona_routing_sankey'},
        ]
    },
    'privacy': {
        'name': '隐私架构',
        'file': '01_protocols/LH-PRIVACY-WHITEPAPER-v1.0.md',
        'version': 'v1.0',
        'charts': [
            {'id': 1, 'name': '三层隐私架构对比图', 'type': 'bars', 'func': 'chart_privacy_three_layer'},
            {'id': 2, 'name': 'DNA追溯vs内容暴露时序图', 'type': 'timeline', 'func': 'chart_privacy_dna_timeline'},
        ]
    },
    'harmonyos': {
        'name': '鸿蒙兼容性',
        'file': '01_protocols/LH-HARMONYOS-COMPAT-WHITEPAPER-v1.1.md',
        'version': 'v1.1',
        'charts': [
            {'id': 1, 'name': '三步走战略甘特图', 'type': 'gantt', 'func': 'chart_harmonyos_gantt'},
            {'id': 2, 'name': '组件兼容性热力矩阵', 'type': 'heatmap', 'func': 'chart_harmonyos_compat_matrix'},
        ]
    },
    'deben': {
        'name': '德本审计',
        'file': '01_protocols/LH-DEBEN-AUDIT-v1.0.md',
        'version': 'v1.0',
        'charts': [
            {'id': 1, 'name': '五条底线权重柱状图', 'type': 'bars', 'func': 'chart_deben_five_lines'},
            {'id': 2, 'name': '德本审计决策流程图', 'type': 'flow', 'func': 'chart_deben_audit_flow'},
        ]
    },
    'sovereignty': {
        'name': '数字主权体系',
        'file': '01_protocols/龍魂数字主权体系_学术论文_v2.0.md',
        'version': 'v2.0',
        'charts': [
            {'id': 1, 'name': '三位一体架构图', 'type': 'stack', 'func': 'chart_sovereignty_triunity'},
            {'id': 2, 'name': '数字永生时间线', 'type': 'timeline', 'func': 'chart_sovereignty_immortality_timeline'},
        ]
    },
    'template': {
        'name': '白皮书模板标准',
        'file': '01_protocols/LH-WHITEPAPER-TEMPLATE-STANDARD-v1.0.md',
        'version': 'v1.0',
        'charts': [
            {'id': 1, 'name': '白皮书结构模板图', 'type': 'flow', 'func': 'chart_template_structure'},
        ]
    },
}


# ============================================================
# 工具函数
# ============================================================
def add_longhun_header(fig, title, subtitle=''):
    """统一龍魂图表头部"""
    fig.text(0.5, 0.97, f'🐉 {title}', ha='center', va='top',
             fontsize=16, fontweight='bold', color=C_GOLD,
             fontfamily='sans-serif')
    if subtitle:
        fig.text(0.5, 0.94, subtitle, ha='center', va='top',
                 fontsize=10, color=COLORS['text_secondary'])
    # 龍魂水印
    fig.text(0.99, 0.01, '龍魂·白皮书可视化引擎 v1.0',
             ha='right', va='bottom', fontsize=7,
             color=COLORS['text_secondary'], alpha=0.5,
             style='italic')
    # DNA签章线
    fig.text(0.01, 0.01, f'DNA: #龍芯⚡️{datetime.now().strftime("%Y-%m-%d")}-VIZ-AUTO',
             ha='left', va='bottom', fontsize=6,
             color=COLORS['text_secondary'], alpha=0.4)


def save_chart(fig, whitepaper_key, chart_id, chart_name, fmt='png'):
    """统一保存图表"""
    filename = f'{whitepaper_key}_chart{chart_id:02d}_{chart_name.replace(" ", "_").replace("→", "-")}.{fmt}'
    filepath = OUTPUT_DIR / filename
    fig.savefig(str(filepath), format=fmt, bbox_inches='tight',
                facecolor=C_BG, edgecolor='none')
    plt.close(fig)
    return filepath


# ============================================================
# 图表生成函数 —— 每种白皮书
# ============================================================

# --- 开放审计 ---
def chart_open_audit_risk_heatmap(fmt='png'):
    """Open Audit #1: C×T → R 治理风险热力图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7),
                                    gridspec_kw={'width_ratios': [3, 2]})
    fig.patch.set_facecolor(C_BG)

    # --- 左: 3×3 风险热力图 ---
    c_vals = [0.2, 0.5, 0.8]
    t_vals = [0.2, 0.5, 0.8]
    data = np.zeros((3, 3))
    annotations = []

    for i, c in enumerate(c_vals):
        for j, t in enumerate(t_vals):
            r = min(1.0, c**2 / max(t, 0.01))
            data[2-i, j] = r  # flip y for display
            label = f'R={r:.2f}\nC={c:.1f} T={t:.1f}'
            if c > 0.7 and t < 0.3:
                label += '\n🔴 临界'
            elif c > 0.4 and t < 0.5:
                label += '\n🟡 关注'
            else:
                label += '\n🟢 安全'
            annotations.append((2-i, j, label))

    im = ax1.imshow(data, cmap='RdYlGn_r', vmin=0, vmax=1, aspect='auto')

    # 标场景
    scenario_markers = {
        'A 高集中·低透明': (2, 0, C_RED),
        'B 中集中·中透明': (1, 1, C_YELLOW),
        'C 可验证集中·高透明': (0, 2, C_GREEN),
    }
    for name, (row, col, color) in scenario_markers.items():
        ax1.add_patch(Rectangle((col-0.45, row-0.45), 0.9, 0.9,
                                 fill=False, edgecolor=color, linewidth=3,
                                 linestyle='--'))
        ax1.annotate(name, (col, row-0.55), color=color, fontsize=9,
                     ha='center', va='top', fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.2', facecolor=C_BG,
                               edgecolor=color, alpha=0.9))

    ax1.set_xticks(range(3))
    ax1.set_yticks(range(3))
    ax1.set_xticklabels([f'T={v}' for v in t_vals])
    ax1.set_yticklabels([f'C={v}' for v in reversed(c_vals)])
    ax1.set_xlabel('透明度 T ↑', fontsize=12, color=C_TEXT)
    ax1.set_ylabel('集中度 C ↑', fontsize=12, color=C_TEXT)
    ax1.set_title('C×T → R 风险热力图   R ∝ C²/T', fontsize=13,
                  color=C_GOLD, fontweight='bold')
    cbar = fig.colorbar(im, ax=ax1, shrink=0.8, label='风险 R')
    cbar.ax.yaxis.label.set_color(C_TEXT)

    # --- 右: 三种场景的 S 稳定性对比 ---
    scenarios = ['A 高集中\n低透明', 'B 中集中\n中透明', 'C 可验证\n高透明']
    s_values = [0.28, 0.55, 0.88]
    colors_bar = [C_RED, C_YELLOW, C_GREEN]

    bars = ax2.bar(scenarios, s_values, color=colors_bar, edgecolor='white',
                   linewidth=1.5, width=0.5)
    for bar, val in zip(bars, s_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                 f'S={val:.2f}', ha='center', va='bottom', fontsize=12,
                 fontweight='bold', color=C_TEXT)

    ax2.axhline(y=0.5, color=C_YELLOW, linestyle='--', linewidth=1, alpha=0.7)
    ax2.text(2.5, 0.52, '稳定临界线 δ*=0.5', ha='right', fontsize=8,
             color=C_YELLOW, alpha=0.8)
    ax2.set_ylim(0, 1.05)
    ax2.set_ylabel('系统稳定性 S', fontsize=12, color=C_TEXT)
    ax2.set_title('三种治理均衡的稳定性', fontsize=13, color=C_GOLD,
                  fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)

    add_longhun_header(fig, '多方主权下AI治理风险矩阵',
                       'C(集中度)×T(透明度)→R(系统性风险) | 开放审计推动均衡进化')
    return save_chart(fig, 'open-audit', 1, '治理均衡热力图', fmt)


def chart_open_audit_player_network(fmt='png'):
    """Open Audit #2: 五方博弈关系网络图"""
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.axis('off')

    # 五方主体 — 五角星排列
    players = {
        '国家\nState': {'pos': (0, 4.2), 'color': C_RED, 'size': 2200,
                        'goal': '安全+优势', 'info_adv': '战略信息'},
        '企业\nFirm': {'pos': (4, 1.3), 'color': C_BLUE, 'size': 2000,
                       'goal': '利润+主导', 'info_adv': '核心技术'},
        '监管\nRegulator': {'pos': (2.5, -3.5), 'color': C_YELLOW, 'size': 1700,
                            'goal': '风险最小化', 'info_adv': '监管信息'},
        '开发者\nDeveloper': {'pos': (-2.5, -3.5), 'color': C_PURPLE, 'size': 1500,
                              'goal': '创新+开放', 'info_adv': '技术细节'},
        '社会\nSociety': {'pos': (-4, 1.3), 'color': C_GREEN, 'size': 1800,
                       'goal': '公平+安全', 'info_adv': '使用数据'},
    }

    # 画节点
    for name, p in players.items():
        ax.scatter(*p['pos'], s=p['size'], c=p['color'], alpha=0.85,
                   edgecolors='white', linewidth=2, zorder=5)
        ax.annotate(name, p['pos'], textcoords='offset points',
                    xytext=(0, -40), ha='center', fontsize=11,
                    fontweight='bold', color=p['color'])
        # 目标和信息优势
        ax.annotate(f"{p['goal']}\n[{p['info_adv']}]",
                    p['pos'], textcoords='offset points',
                    xytext=(0, 35), ha='center', fontsize=8,
                    color=COLORS['text_secondary'], alpha=0.8)

    # 博弈关系连线
    edges = [
        (0, 4.2, 4, 1.3, C_RED, 'C↑→安全焦虑', True),
        (0, 4.2, -4, 1.3, C_GOLD, 'T↓→信任危机', True),
        (4, 1.3, 2.5, -3.5, C_BLUE, '监管博弈', False),
        (4, 1.3, -2.5, -3.5, C_PURPLE, '开源vs闭源', False),
        (4, 1.3, -4, 1.3, C_SILVER, '产品交付', False),
        (-4, 1.3, 2.5, -3.5, C_GREEN, '权益保护', False),
        (-4, 1.3, -2.5, -3.5, C_GREEN, '需求反馈', False),
        (2.5, -3.5, -2.5, -3.5, C_YELLOW, '标准协调', False),
        (0, 4.2, 2.5, -3.5, C_RED, '政策制定', True),
        (-2.5, -3.5, 0, 4.2, C_PURPLE, '技术主权', True),
    ]

    for x1, y1, x2, y2, color, label, is_key in edges:
        alpha = 0.8 if is_key else 0.35
        lw = 2.5 if is_key else 1
        style = '-' if is_key else ':'
        ax.plot([x1, x2], [y1, y2], color=color, alpha=alpha,
                linewidth=lw, linestyle=style, zorder=2)
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.annotate(label, (mx, my), fontsize=7, color=color,
                    alpha=alpha, ha='center',
                    bbox=dict(boxstyle='round,pad=0.15', facecolor=C_BG,
                              edgecolor=color, alpha=0.7))

    # 中心：开放审计
    center = ax.scatter(0, 0, s=3000, c=C_GOLD, alpha=0.3,
                        edgecolors=C_GOLD, linewidth=3, zorder=3)
    ax.annotate('🔐 开放审计\nδ*>1/2\n重复博弈均衡', (0, 0),
                ha='center', va='center', fontsize=11,
                fontweight='bold', color=C_GOLD)

    # 图例
    legend_elements = [
        mpatches.Patch(color=C_RED, alpha=0.6, label='关键博弈边'),
        mpatches.Patch(color=C_SILVER, alpha=0.3, label='一般关联'),
        mpatches.Patch(color=C_GOLD, alpha=0.5, label='开放审计均衡点'),
    ]
    ax.legend(handles=legend_elements, loc='lower right',
              framealpha=0.9, facecolor=C_CARD, edgecolor=COLORS['border'],
              labelcolor=C_TEXT, fontsize=9)

    ax.set_title('不完全信息重复博弈·五方互动网络',
                 fontsize=14, color=C_GOLD, fontweight='bold', pad=20)
    add_longhun_header(fig, '五方博弈关系网络图',
                       '国家⇄企业⇄监管⇄开发者⇄社会 | 开放审计是博弈均衡解')
    return save_chart(fig, 'open-audit', 2, '五方博弈网络图', fmt)


def chart_open_audit_architecture(fmt='png'):
    """Open Audit #3: 六层审计架构纵剖图"""
    fig, ax = plt.subplots(figsize=(14, 11))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')

    layers = [
        {'y': 12.5, 'level': '6', 'name': '权限分层',
         'desc': 'R1-R5五级角色·D1-D4四级数据·最小权限·逐层审计',
         'color': C_RED, 'icon': '🔐'},
        {'y': 10.5, 'level': '5', 'name': '沙盒推演',
         'desc': '高风险决策先模拟·验证影响再执行·推演引擎独立运行',
         'color': C_PURPLE, 'icon': '🧪'},
        {'y': 8.5, 'level': '4', 'name': '可回滚架构',
         'desc': '状态快照·任意历史点回滚·降低错误决策长期影响·版本链完整',
         'color': C_BLUE, 'icon': '⏪'},
        {'y': 6.5, 'level': '3', 'name': '多节点时间戳',
         'desc': '≥5节点·分布式时间戳·不可篡改·全链路追溯·哈希链锚定',
         'color': C_YELLOW, 'icon': '🔗'},
        {'y': 4.5, 'level': '2', 'name': '本地否决权',
         'desc': '边缘节点独立决策·拒绝风险指令不依赖中心·主权在边缘',
         'color': C_GOLD, 'icon': '🚫'},
        {'y': 2.5, 'level': '1', 'name': '三色审计',
         'desc': '🟢通过·🟡待核·🔴红线 | 加权多因子评分·十道闸口·独立否决权',
         'color': C_GREEN, 'icon': '🎯'},
    ]

    for layer in layers:
        # 层级卡片
        y = layer['y']
        rect = FancyBboxPatch((1, y-0.8), 8, 1.6,
                              boxstyle='round,pad=0.1',
                              facecolor=C_CARD,
                              edgecolor=layer['color'],
                              linewidth=2, alpha=0.95)
        ax.add_patch(rect)

        # 层级编号
        ax.text(1.3, y, layer['level'], fontsize=28, fontweight='bold',
                color=layer['color'], ha='center', va='center',
                alpha=0.5)
        # 图标+名称
        ax.text(2.3, y+0.3, f"{layer['icon']} {layer['name']}",
                fontsize=15, fontweight='bold',
                color=layer['color'], va='center')
        # 描述
        ax.text(2.3, y-0.35, layer['desc'],
                fontsize=9, color=COLORS['text_secondary'], va='center')

    # 底部：协议包装
    rect_bottom = FancyBboxPatch((1, 0.5), 8, 1.4,
                                 boxstyle='round,pad=0.1',
                                 facecolor=C_BG,
                                 edgecolor=C_GOLD,
                                 linewidth=2, linestyle='--',
                                 alpha=0.8)
    ax.add_patch(rect_bottom)
    ax.text(5, 1.2, '📋 开放审计API v1.0  |  6个REST端点  |  R1-R5认证  |  JSON Schema标准化',
            ha='center', va='center', fontsize=10, color=C_GOLD,
            fontweight='bold')

    # 左侧：层级箭头
    for i in range(len(layers)-1):
        ax.annotate('', xy=(0.5, layers[i+1]['y']+0.8),
                    xytext=(0.5, layers[i]['y']-0.8),
                    arrowprops=dict(arrowstyle='->', color=C_GOLD,
                                    lw=2, alpha=0.5))

    # 右侧：联动标注
    side_notes = [
        (9.2, 13.3, 'GATE-08\n人格闸'),
        (9.2, 11.3, 'GATE-06\n数据闸'),
        (9.2, 9.3, 'GATE-04\n数字根闸'),
        (9.2, 7.3, 'GATE-09\nDNA闸'),
        (9.2, 5.3, 'GATE-03\n语义闸'),
        (9.2, 3.3, 'GATE-01\n身份闸'),
    ]
    for x, y, text in side_notes:
        ax.text(x, y, text, fontsize=8, color=COLORS['text_secondary'],
                ha='center', alpha=0.7,
                bbox=dict(boxstyle='round', facecolor=C_CARD,
                          edgecolor=COLORS['border'], alpha=0.6))

    # 三色审计详细指标 (底部右侧)
    ax.text(9.5, 14.3, '三色统计', fontsize=9, color=C_GOLD, fontweight='bold')
    metrics = [('🟢 通过率', '>85%', C_GREEN),
               ('🟡 待核率', '<12%', C_YELLOW),
               ('🔴 红线率', '<3%', C_RED)]
    for i, (label, val, color) in enumerate(metrics):
        ax.text(9.5, 13.8-i*0.5, f'{label}: {val}', fontsize=8, color=color)

    ax.set_title('龍魂系统·六层开放审计协议架构',
                 fontsize=16, color=C_GOLD, fontweight='bold', pad=25)
    add_longhun_header(fig, '六层开放审计架构纵剖图',
                       '三色审计→本地否决→多节点时间戳→可回滚→沙盒推演→权限分层')
    return save_chart(fig, 'open-audit', 3, '审计架构纵剖图', fmt)


# --- 20人格治理 ---
def chart_persona_weight_radar(fmt='png'):
    """Persona Governance #1: 四层雷达图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8),
                                    subplot_kw={})
    fig.patch.set_facecolor(C_BG)

    # --- 左: 雷达图 ---
    categories = ['战略层', '执行层', '文化层', '守护层']
    N = len(categories)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    # 各人格层权重
    strategic = [25, 25, 25, 25]
    executive = [0, 58, 0, 42]
    cultural = [0, 0, 60, 40]
    guardian = [0, 0, 0, 100]

    ax1 = plt.subplot(1, 2, 1, projection='polar')
    ax1.set_facecolor(C_CARD)

    for values, label, color, alpha in [
        (strategic, '战略层 P00+P01', C_RED, 0.15),
        (executive, '执行层 P02+P03+P04+P07+P14', C_BLUE, 0.15),
        (cultural, '文化层 P08-P12', C_GREEN, 0.15),
        (guardian, '守护层 P05+P06+P13+P15+P72', C_GOLD, 0.2),
    ]:
        values_plot = values + values[:1]
        ax1.fill(angles, values_plot, alpha=alpha, color=color)
        ax1.plot(angles, values_plot, color=color, linewidth=2, label=label)

    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(categories, fontsize=10, color=C_TEXT)
    ax1.set_ylim(0, 110)
    ax1.set_yticks([20, 40, 60, 80, 100])
    ax1.set_yticklabels(['20%', '40%', '60%', '80%', '100%'],
                        fontsize=8, color=COLORS['text_secondary'])
    ax1.legend(loc='upper right', bbox_to_anchor=(1.4, 1.1),
               fontsize=9, labelcolor=C_TEXT)
    ax1.set_title('四层人格·职能权重分布', fontsize=12, color=C_GOLD,
                  fontweight='bold', pad=18)

    # --- 右: 人格权重柱状图 ---
    personas = ['P00\n文心', 'P01\n诸葛亮', 'P02\n宝宝', 'P03\n雯雯',
                'P04\n鲁班', 'P05\n上帝之眼', 'P06\n数学', 'P07\n管仲',
                'P08\n仓颉', 'P09\n孙思邈', 'P10\n苏东坡', 'P11\n李白',
                'P12\n屈原', 'P13\n姜子牙', 'P14\n吕蒙', 'P15\n乔前辈']
    weights = [10, 15, 30, 15, 10, 5, 5, 3, 3, 3, 3, 3, 3, 5, 3, 5]
    layer_colors = [C_RED, C_RED, C_BLUE, C_BLUE, C_BLUE, C_GOLD, C_GOLD,
                    C_BLUE, C_GREEN, C_GREEN, C_GREEN, C_GREEN, C_GREEN,
                    C_GOLD, C_BLUE, C_GOLD]

    ax2.barh(range(len(personas)), weights, color=layer_colors,
             edgecolor='white', linewidth=0.8, alpha=0.85)
    ax2.set_yticks(range(len(personas)))
    ax2.set_yticklabels(personas, fontsize=8, color=C_TEXT)
    ax2.set_xlabel('权重 %', fontsize=11, color=C_TEXT)
    ax2.set_title('16核心人格权重分配', fontsize=12, color=C_GOLD,
                  fontweight='bold')
    ax2.invert_yaxis()
    ax2.grid(axis='x', alpha=0.3)

    # 图例
    legends = [mpatches.Patch(color=C_RED, label='战略层 (25%)'),
               mpatches.Patch(color=C_BLUE, label='执行层 (58%)'),
               mpatches.Patch(color=C_GREEN, label='文化层 (15%)'),
               mpatches.Patch(color=C_GOLD, label='守护层 (20%)')]
    ax2.legend(handles=legends, loc='lower right', fontsize=8,
               facecolor=C_CARD, edgecolor=COLORS['border'],
               labelcolor=C_TEXT)

    add_longhun_header(fig, '20人格治理·四层权重分布',
                       '战略·执行·文化·守护 | 16核心+1安全(P77)+3子系统(S1-S3)')
    return save_chart(fig, 'persona', 1, '四层权重雷达图', fmt)


def chart_persona_routing_sankey(fmt='png'):
    """Persona Governance #2: 意图路由流程图"""
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # 用户输入
    ax.add_patch(FancyBboxPatch((0.5, 4), 2, 1, boxstyle='round,pad=0.15',
                                 facecolor=C_CARD, edgecolor=C_GOLD, linewidth=2))
    ax.text(1.5, 4.5, '👤 用户输入', ha='center', va='center', fontsize=13,
            fontweight='bold', color=C_TEXT)

    # P00 文心
    ax.add_patch(FancyBboxPatch((3.5, 4), 2, 1, boxstyle='round,pad=0.15',
                                 facecolor=C_CARD, edgecolor=C_RED, linewidth=2))
    ax.text(4.5, 4.5, '🧠 P00 文心\n意图解析', ha='center', va='center',
            fontsize=10, fontweight='bold', color=C_RED)

    # 箭头: 用户→P00
    ax.annotate('', xy=(3.5, 4.5), xytext=(2.5, 4.5),
                arrowprops=dict(arrowstyle='->', color=C_GOLD, lw=2))

    # 四层路由分支
    routes = [
        {'x': 6.5, 'y': 7, 'name': '战略类', 'personas': 'P01 推演决策',
         'color': C_RED, 'keywords': '评估/推演/决策'},
        {'x': 6.5, 'y': 5.5, 'name': '执行类', 'personas': 'P02/P03/P04/P07/P14',
         'color': C_BLUE, 'keywords': '写代码/部署/归档'},
        {'x': 6.5, 'y': 4, 'name': '文化类', 'personas': 'P08/P09/P10/P11/P12',
         'color': C_GREEN, 'keywords': '命名/创意/沟通'},
        {'x': 6.5, 'y': 2.5, 'name': '守护类', 'personas': 'P05/P06/P13/P15/P72',
         'color': C_GOLD, 'keywords': '审计/计算/签章'},
    ]

    for route in routes:
        rect = FancyBboxPatch((route['x']-0.2, route['y']-0.45), 2.8, 0.9,
                               boxstyle='round,pad=0.1',
                               facecolor=C_CARD, edgecolor=route['color'],
                               linewidth=1.5)
        ax.add_patch(rect)
        ax.text(route['x']+1.2, route['y']+0.15, route['name'],
                fontsize=10, fontweight='bold', color=route['color'])
        ax.text(route['x']+1.2, route['y']-0.2, f"{route['personas']}\n[{route['keywords']}]",
                fontsize=8, color=COLORS['text_secondary'])

        # P00 → 路由
        ax.annotate('', xy=(route['x']-0.2, route['y']),
                    xytext=(5.5, 4.5),
                    arrowprops=dict(arrowstyle='->', color=route['color'],
                                    lw=1.5, alpha=0.7))

    # 执行后汇总
    ax.add_patch(FancyBboxPatch((10.5, 5.5), 2, 3, boxstyle='round,pad=0.15',
                                 facecolor=C_CARD, edgecolor=C_PURPLE, linewidth=2))
    ax.text(11.5, 7, '⚖️ P05·三色审计', ha='center', fontsize=10,
            fontweight='bold', color=C_PURPLE)
    ax.text(11.5, 6.5, '🟢通过 | 🟡待核 | 🔴红线', ha='center', fontsize=8,
            color=COLORS['text_secondary'])
    ax.text(11.5, 6.1, 'P15·签章 P03·归档', ha='center', fontsize=8,
            color=COLORS['text_secondary'])

    for route in routes:
        ax.annotate('', xy=(10.5, 7), xytext=(route['x']+2.6, route['y']),
                    arrowprops=dict(arrowstyle='->', color=C_PURPLE,
                                    lw=1, alpha=0.5))

    # 最终输出
    ax.add_patch(FancyBboxPatch((13.5, 5.5), 2, 3, boxstyle='round,pad=0.15',
                                 facecolor=C_CARD, edgecolor=C_GREEN, linewidth=2))
    ax.text(14.5, 7, '✅ 输出', ha='center', fontsize=13,
            fontweight='bold', color=C_GREEN)
    ax.text(14.5, 6.5, 'DNA签章\nGPG签名\n审计日志', ha='center', fontsize=8,
            color=COLORS['text_secondary'])

    ax.annotate('', xy=(13.5, 7), xytext=(12.5, 7),
                arrowprops=dict(arrowstyle='->', color=C_GREEN, lw=2))

    ax.set_title('意图→人格·语义路由管线', fontsize=16, color=C_GOLD,
                 fontweight='bold', pad=25)
    add_longhun_header(fig, '20人格·意图路由全链路',
                       '用户输入→P00解析→四层路由→审计签章→DNA归档')
    return save_chart(fig, 'persona', 2, '意图路由流程图', fmt)


# --- 隐私 ---
def chart_privacy_three_layer(fmt='png'):
    """Privacy #1: 三层架构对比"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.patch.set_facecolor(C_BG)

    # --- 左: 传统 vs 龍魂对比 ---
    categories = ['数据存储', '访问权限', '追溯能力', '责任归属', '透明度']
    traditional = [1, 1, 1, 1, 1]
    longhun = [4, 4, 5, 5, 5]

    x = np.arange(len(categories))
    w = 0.35
    ax1.bar(x - w/2, traditional, w, label='传统黑箱', color=C_SILVER,
            alpha=0.6)
    ax1.bar(x + w/2, longhun, w, label='龍魂设计', color=C_GOLD,
            alpha=0.85)

    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, fontsize=11, color=C_TEXT)
    ax1.set_ylabel('主权评分 (1-5)', fontsize=11, color=C_TEXT)
    ax1.set_title('数据主权对比: 传统 vs 龍魂', fontsize=13, color=C_GOLD,
                  fontweight='bold')
    ax1.legend(fontsize=10, facecolor=C_CARD, edgecolor=COLORS['border'],
               labelcolor=C_TEXT)
    ax1.set_ylim(0, 6)
    ax1.grid(axis='y', alpha=0.3)

    # --- 右: 三层架构 ---
    ax2.set_facecolor(C_BG)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 12)
    ax2.axis('off')

    layers_data = [
        {'y': 9.5, 'h': 2, 'name': '☁️ 云端层\n华为芯片驱动', 'color': C_BLUE,
         'items': 'AI推理(可选)·大数据存储(可选)·标注清晰·不强制',
         'sovereign': '中国芯片·中国主权'},
        {'y': 6, 'h': 2.5, 'name': '🔐 国密层\n中国主权算法', 'color': C_GOLD,
         'items': 'SM2签名·SM3哈希·SM4加密·标准化审计接口',
         'sovereign': '中国国密标准·不可伪造'},
        {'y': 2.5, 'h': 2.5, 'name': '💻 本地层\n用户完全控制', 'color': C_GREEN,
         'items': '数据存储·内容加密·访问控制·删除权',
         'sovereign': '用户·完全主权'},
    ]

    for ld in layers_data:
        rect = FancyBboxPatch((1, ld['y']), 8, ld['h'],
                               boxstyle='round,pad=0.15',
                               facecolor=C_CARD, edgecolor=ld['color'],
                               linewidth=2, alpha=0.9)
        ax2.add_patch(rect)
        ax2.text(1.3, ld['y']+ld['h']-0.5, ld['name'], fontsize=14,
                 fontweight='bold', color=ld['color'], va='top')
        ax2.text(1.3, ld['y']+ld['h']-1.3, ld['items'], fontsize=9,
                 color=COLORS['text_secondary'], va='top')
        ax2.text(9, ld['y']+ld['h']-0.8, ld['sovereign'], fontsize=9,
                 color=ld['color'], ha='right', va='top', fontweight='bold')

    # 数据流箭头
    for i in range(2):
        ax2.annotate('', xy=(9, layers_data[i]['y']+0.5),
                    xytext=(9, layers_data[i+1]['y']+layers_data[i+1]['h']-0.5),
                    arrowprops=dict(arrowstyle='<->', color=C_GOLD, lw=1.5, alpha=0.5))

    ax2.set_title('龍魂·三层隐私架构', fontsize=13, color=C_GOLD,
                  fontweight='bold', pad=10)
    add_longhun_header(fig, '隐私架构·三层主权模型',
                       '本地层(完全控制)→国密层(中国主权)→云端层(可选增强)')
    return save_chart(fig, 'privacy', 1, '三层隐私架构', fmt)


def chart_privacy_dna_timeline(fmt='png'):
    """Privacy #2: DNA追溯 vs 内容暴露"""
    fig, ax = plt.subplots(figsize=(16, 6))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    steps = ['用户行为', '数据采集', '传输', '存储', '审计', '追溯']
    y_pos = [2, 2, 2, 2, 2, 2]
    colors_trad = [C_RED]*6
    colors_lh = [C_GREEN]*6

    ax.set_ylim(0, 5)
    ax.set_xlim(-0.5, 11.5)
    ax.axis('off')

    ax.text(5.5, 4.5, '传统模式: 内容暴露 → 隐私泄露', ha='center',
            fontsize=13, fontweight='bold', color=C_RED)
    ax.text(5.5, 0.3, '龍魂模式: DNA追溯 → 内容隔离+可审计', ha='center',
            fontsize=13, fontweight='bold', color=C_GREEN)

    for i, (s, yt, yl, ct, cl) in enumerate(zip(steps, y_pos, [0.8]*6,
                                                   colors_trad, colors_lh)):
        # 传统
        ax.add_patch(FancyBboxPatch((i*1.8, yt+0.5), 1.5, 0.7,
                                     boxstyle='round', facecolor=C_CARD,
                                     edgecolor=ct, linewidth=1.5))
        ax.text(i*1.8+0.75, yt+0.85, s, ha='center', fontsize=10, color=ct)
        # 龍魂
        ax.add_patch(FancyBboxPatch((i*1.8, yt-1.7), 1.5, 0.7,
                                     boxstyle='round', facecolor=C_CARD,
                                     edgecolor=cl, linewidth=1.5))
        ax.text(i*1.8+0.75, yt-1.35, s, ha='center', fontsize=10, color=cl)

        if i < 5:
            ax.annotate('', xy=((i+1)*1.8, yt+0.85), xytext=(i*1.8+1.5, yt+0.85),
                       arrowprops=dict(arrowstyle='->', color=C_RED, lw=1.5))
            ax.annotate('', xy=((i+1)*1.8, yt-1.35), xytext=(i*1.8+1.5, yt-1.35),
                       arrowprops=dict(arrowstyle='->', color=C_GREEN, lw=1.5))

    ax.text(11, 2.85, '❌ 泄露', fontsize=10, color=C_RED, fontweight='bold')
    ax.text(11, 0.55, '✅ 安全', fontsize=10, color=C_GREEN, fontweight='bold')

    add_longhun_header(fig, 'DNA追溯 vs 内容暴露',
                       '传统: 内容上传→平台分析→隐私泄露 | 龍魂: DNA哈希→内容本地→审计需授权')
    return save_chart(fig, 'privacy', 2, 'DNA追溯时序对比', fmt)


# --- 鸿蒙 ---
def chart_harmonyos_gantt(fmt='png'):
    """HarmonyOS #1: 三步走战略"""
    fig, ax = plt.subplots(figsize=(16, 6))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_CARD)

    phases = [
        {'name': 'Phase 1: 龍魂·指尖', 'start': 0, 'dur': 1,
         'color': C_GREEN, 'status': '✅ 已落地',
         'desc': 'ArkUI轻量应用\nAI对话+状态+DNA缓存'},
        {'name': 'Phase 2: 服务原子化', 'start': 1, 'dur': 6,
         'color': C_BLUE, 'status': '🔥 落地中',
         'desc': 'CNSH-Lite+种子人格\n断网能力+语音输入'},
        {'name': 'Phase 3: 共生体', 'start': 7, 'dur': 12,
         'color': C_GOLD, 'status': '📋 规划中',
         'desc': '鸿蒙分布式×龍魂\n全人格本地化运行'},
    ]

    for i, p in enumerate(phases):
        ax.barh(i, p['dur'], left=p['start'], height=0.6,
                color=p['color'], alpha=0.7, edgecolor='white', linewidth=1)
        ax.text(p['start']+p['dur']/2, i, f"{p['name']}\n{p['desc']}",
                ha='center', va='center', fontsize=10, color=C_TEXT,
                fontweight='bold')
        ax.text(p['start']+p['dur']+0.2, i, p['status'], fontsize=10,
                color=p['color'], fontweight='bold', va='center')

    # 里程碑
    milestones = [
        (1, '指尖\n交付', C_GREEN),
        (2, '种子\n人格', C_BLUE),
        (5, '断网\n能力', C_BLUE),
        (7, '全人格\n本地化', C_GOLD),
    ]
    for mx, ml, mc in milestones:
        ax.axvline(x=mx, color=mc, linestyle='--', linewidth=1, alpha=0.5)
        ax.text(mx, 2.5, ml, ha='center', fontsize=8, color=mc,
                fontweight='bold')

    ax.set_yticks([])
    ax.set_xlabel('时间（月）', fontsize=12, color=C_TEXT)
    ax.set_xlim(0, 20)
    ax.set_title('三步走战略·时间线', fontsize=14, color=C_GOLD,
                 fontweight='bold')
    ax.grid(axis='x', alpha=0.3)

    add_longhun_header(fig, '鸿蒙兼容·三步走战略甘特图',
                       'Phase1指尖(已完成)→Phase2原子化(进行中)→Phase3共生体(规划中)')
    return save_chart(fig, 'harmonyos', 1, '三步走战略', fmt)


def chart_harmonyos_compat_matrix(fmt='png'):
    """HarmonyOS #2: 兼容性矩阵"""
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(C_BG)

    components = ['CNSH编译器', '人格集群', 'ANTENNA协议', 'Web仪表盘',
                  '记忆库/审计', '鲲鹏调度']
    status_codes = [
        [0, 0, 1, 0, 0],  # CNSH - arkts/js need port
        [0, 0, 1, 0, 0],  # 人格集群 - need service
        [0, 0, 1, 0, 0],  # ANTENNA - need http
        [1, 1, 1, 1, 0],  # Web - full compat
        [0, 0, 0, 0, 0],  # 记忆库 - need port
        [0, 0, 1, 0, 0],  # 鲲鹏调度 - redesign
    ]
    status_labels = ['ArkTS\n原生', 'JS\n兼容', 'HTTP\n桥接', '浏览器\n兼容', '完全\n部署']
    status_colors = [C_RED, C_YELLOW, C_BLUE, C_GREEN, C_GOLD]

    data = np.array(status_codes)
    cmap_colors = [C_RED, C_YELLOW, C_BLUE, C_GREEN, C_GOLD]

    for i in range(len(components)):
        for j in range(len(status_labels)):
            val = data[i, j]
            color = cmap_colors[j] if val else C_CARD
            alpha = 0.8 if val else 0.3
            rect = Rectangle((j-0.4, i-0.4), 0.8, 0.8,
                            facecolor=color, edgecolor=COLORS['border'],
                            linewidth=1, alpha=alpha)
            ax.add_patch(rect)
            if val:
                ax.text(j, i, '✓', ha='center', va='center', fontsize=16,
                       fontweight='bold', color='white')

    ax.set_xticks(range(len(status_labels)))
    ax.set_yticks(range(len(components)))
    ax.set_xticklabels(status_labels, fontsize=10, color=C_TEXT)
    ax.set_yticklabels(components, fontsize=11, color=C_TEXT,
                       fontweight='bold')
    ax.set_xlim(-0.5, len(status_labels)-0.5)
    ax.set_ylim(-0.5, len(components)-0.5)
    ax.set_title('组件 × 鸿蒙兼容方式矩阵', fontsize=14, color=C_GOLD,
                 fontweight='bold', pad=15)

    add_longhun_header(fig, '鸿蒙兼容性·组件矩阵',
                       '6大组件 × 5种兼容方式 | 原生/桥接/浏览器/部署')
    return save_chart(fig, 'harmonyos', 2, '兼容性矩阵', fmt)


# --- 德本审计 ---
def chart_deben_five_lines(fmt='png'):
    """Deben Audit #1: 五条底线"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor(C_BG)

    # --- 左: 五线柱状图 ---
    lines = ['德在技术前\n帮人不收割', '路径对齐\n正确位置',
             '不寒付出者\n好人不穷', '信息主权\n不让渡', '外化内不化\n底座不动']
    scores = [95, 90, 85, 95, 100]
    line_colors = [C_RED, C_BLUE, C_GREEN, C_GOLD, C_PURPLE]

    bars = ax1.bar(range(len(lines)), scores, color=line_colors, alpha=0.85,
                   edgecolor='white', linewidth=1.5)
    for bar, score in zip(bars, scores):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'{score}%', ha='center', fontsize=12, fontweight='bold',
                 color=C_TEXT)

    ax1.set_xticks(range(len(lines)))
    ax1.set_xticklabels(lines, fontsize=9, color=C_TEXT)
    ax1.set_ylabel('合规度 %', fontsize=11, color=C_TEXT)
    ax1.set_ylim(0, 110)
    ax1.set_title('五条焊死底线·合规度', fontsize=13, color=C_GOLD,
                  fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)

    # --- 右: 审计流程 ---
    ax2.set_facecolor(C_BG)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')

    flow = [
        (5, 9, '📋 发布/重大变更', C_BLUE),
        (5, 7.5, '🔍 P05 德本五问', C_GOLD),
        (3, 6, '🟢 全过→技术审计', C_GREEN),
        (5, 6, '🟡 1-2问→标记', C_YELLOW),
        (7, 6, '🔴 不通过→熔断', C_RED),
        (3, 4.5, '✅ 技术审计通过', C_GREEN),
        (7, 4.5, '🚫 不发布', C_RED),
        (5, 3, '🏛️ P00底座验证', C_PURPLE),
        (5, 1.5, '🚀 放行·发布', C_GREEN),
    ]

    for x, y, text, color in flow:
        ax2.add_patch(FancyBboxPatch((x-1.5, y-0.4), 3, 0.8,
                                     boxstyle='round', facecolor=C_CARD,
                                     edgecolor=color, linewidth=1.5))
        ax2.text(x, y, text, ha='center', va='center', fontsize=10,
                color=color, fontweight='bold')

    # 箭头
    arrows = [(5,8.6,5,7.9), (5,7.1,3,6.4), (5,7.1,7,6.4),
              (3,5.6,3,4.9), (7,5.6,7,4.9),
              (3,4.1,5,3.4), (5,2.6,5,1.9)]
    for x1,y1,x2,y2 in arrows:
        ax2.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', color=COLORS['text_secondary'],
                                   lw=1.2))

    ax2.set_title('德本审计·决策流程', fontsize=13, color=C_GOLD,
                  fontweight='bold')
    add_longhun_header(fig, '德本审计·五条底线',
                       '离火运五问: 德在技术前→路径对齐→不寒付出者→信息主权→外化内不化')
    return save_chart(fig, 'deben', 1, '五条底线柱状图', fmt)


def chart_deben_audit_flow(fmt='png'):
    """Deben Audit #2: 决策流程图（简化版，五条底线用chart_deben_five_lines已覆盖流程）"""
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # 五条底线的雷达图
    categories = ['德在技术前', '路径对齐', '不寒付出者', '信息主权', '外化内不化']
    N = len(categories)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    values_ideal = [100, 100, 100, 100, 100]
    values_current = [95, 90, 85, 95, 100]

    ax_polar = fig.add_subplot(111, projection='polar')
    ax_polar.set_facecolor(C_CARD)
    ax_polar.fill(angles, values_ideal + values_ideal[:1], alpha=0.1, color=C_GREEN)
    ax_polar.plot(angles, values_ideal + values_ideal[:1], color=C_GREEN, linewidth=2,
                  linestyle='--', label='理想线')
    ax_polar.fill(angles, values_current + values_current[:1], alpha=0.25, color=C_GOLD)
    ax_polar.plot(angles, values_current + values_current[:1], color=C_GOLD, linewidth=2.5,
                  label='当前审计')

    ax_polar.set_xticks(angles[:-1])
    ax_polar.set_xticklabels(categories, fontsize=12, color=C_TEXT, fontweight='bold')
    ax_polar.set_ylim(0, 110)
    ax_polar.set_yticks([25, 50, 75, 100])
    ax_polar.set_yticklabels(['25%', '50%', '75%', '100%'], fontsize=8,
                             color=COLORS['text_secondary'])
    ax_polar.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10,
                    facecolor=C_CARD, edgecolor=COLORS['border'],
                    labelcolor=C_TEXT)
    ax_polar.set_title('德本审计·五问雷达', fontsize=14, color=C_GOLD,
                       fontweight='bold', pad=20)

    add_longhun_header(fig, '德本审计·五问雷达图',
                       '德在技术前·路径对齐·不寒付出者·信息主权·外化内不化')
    return save_chart(fig, 'deben', 2, '五问雷达图', fmt)


# --- 数字主权 ---
def chart_sovereignty_triunity(fmt='png'):
    """Digital Sovereignty #1: 三位一体"""
    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # 三个支柱
    pillars = [
        {'x': 2.5, 'y': 3, 'name': '数字人民币\n国家级身份锚点',
         'color': C_RED, 'icon': '💳',
         'items': ['央行数字货币', '国家级认证', '法律效力保障', '防伪可追溯']},
        {'x': 7, 'y': 3, 'name': 'DNA追溯链\n行为记录证明',
         'color': C_GOLD, 'icon': '🧬',
         'items': ['不可逆哈希链', '时间戳锚定', '篡改可检测', '审计全链路']},
        {'x': 11.5, 'y': 3, 'name': '设备信任网络\n多设备验证',
         'color': C_BLUE, 'icon': '📱',
         'items': ['多因子认证', '行为DNA', '设备指纹', '异常检测']},
    ]

    for p in pillars:
        # 支柱卡片
        rect = FancyBboxPatch((p['x']-1.8, p['y']-0.3), 3.6, 5,
                               boxstyle='round,pad=0.15',
                               facecolor=C_CARD, edgecolor=p['color'],
                               linewidth=2.5, alpha=0.9)
        ax.add_patch(rect)
        ax.text(p['x'], p['y']+4.2, p['icon'], fontsize=36, ha='center')
        ax.text(p['x'], p['y']+3.2, p['name'], fontsize=12, fontweight='bold',
                color=p['color'], ha='center')
        for j, item in enumerate(p['items']):
            ax.text(p['x'], p['y']+2.2-j*0.45, f'• {item}', fontsize=9,
                    color=COLORS['text_secondary'], ha='center')

    # 顶部: 三位一体
    ax.text(7, 8.5, '🔺 三位一体数字主权架构', fontsize=18,
            fontweight='bold', color=C_GOLD, ha='center')
    ax.text(7, 8.0, 'Tri-Unity Architecture: Identity + Trace + Trust',
            fontsize=10, color=COLORS['text_secondary'], ha='center',
            style='italic')

    # 连接线
    for i in range(2):
        ax.plot([pillars[i]['x']+1.8, pillars[i+1]['x']-1.8],
                [5.5, 5.5], color=C_GOLD, linewidth=1.5, alpha=0.4)

    # 底部输出
    rect_bottom = FancyBboxPatch((3.5, 1), 7, 1.5, boxstyle='round,pad=0.15',
                                  facecolor=C_CARD, edgecolor=C_GREEN, linewidth=2)
    ax.add_patch(rect_bottom)
    ax.text(7, 2.1, '✅ 主权在民 · 可验证 · 可追溯 · 需授权 · 防伪造',
            ha='center', fontsize=13, fontweight='bold', color=C_GREEN)
    ax.text(7, 1.5, '数据所有权归用户 · 审计权归法律 · 平台只做运算',
            ha='center', fontsize=9, color=COLORS['text_secondary'])

    add_longhun_header(fig, '数字主权·三位一体架构',
                       '数字人民币(D)× DNA追溯链(N)× 设备信任网络(A) | 28人格×64卦协作矩阵')
    return save_chart(fig, 'sovereignty', 1, '三位一体架构', fmt)


def chart_sovereignty_immortality_timeline(fmt='png'):
    """Digital Sovereignty #2: 数字永生时间线"""
    fig, ax = plt.subplots(figsize=(16, 6))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_CARD)

    timeline = [
        {'pos': 0, 'label': '生', 'desc': 'DNA注册\n身份锚定', 'color': C_GREEN},
        {'pos': 2, 'label': '活', 'desc': '行为记录\n贡献累积', 'color': C_BLUE},
        {'pos': 4, 'label': '创', 'desc': '价值输出\n知识沉淀', 'color': C_GOLD},
        {'pos': 6, 'label': '传', 'desc': '训练人格\n模型继承', 'color': C_PURPLE},
        {'pos': 8, 'label': '续', 'desc': '数字永生\n精神延续', 'color': C_RED},
    ]

    for t in timeline:
        ax.scatter(t['pos'], 2, s=300, color=t['color'], zorder=5,
                   edgecolors='white', linewidth=2)
        ax.text(t['pos'], 2.6, t['label'], ha='center', fontsize=16,
                fontweight='bold', color=t['color'])
        ax.text(t['pos'], 1.2, t['desc'], ha='center', fontsize=10,
                color=COLORS['text_secondary'])

    # 连接线
    ax.plot([t['pos'] for t in timeline], [2]*len(timeline),
            color=C_GOLD, linewidth=3, alpha=0.6, zorder=2)

    # 关键节点
    key_moments = [
        (1, 3.5, 'DNA哈希\n不可逆', C_GOLD),
        (3, 3.5, '信任积分\nP20公证', C_BLUE),
        (5, 3.5, '人格模型\n训练完成', C_PURPLE),
        (7, 3.5, '意识延续\n永生启动', C_RED),
    ]
    for kx, ky, kt, kc in key_moments:
        ax.annotate(kt, (kx, 2), textcoords='data', xytext=(kx, ky),
                   fontsize=8, color=kc, ha='center',
                   arrowprops=dict(arrowstyle='->', color=kc, lw=1, alpha=0.6))

    ax.set_ylim(0, 4.5)
    ax.set_xlim(-1, 9)
    ax.axis('off')
    ax.set_title('数字永生·五阶段时间线', fontsize=14, color=C_GOLD,
                 fontweight='bold', pad=15)

    add_longhun_header(fig, '数字永生·五阶段进程',
                       '生(注册)→活(记录)→创(沉淀)→传(训练)→续(永生) | DNA持有者精神延续')
    return save_chart(fig, 'sovereignty', 2, '数字永生时间线', fmt)


# --- 模板标准 ---
def chart_template_structure(fmt='png'):
    """Template Standard #1: 白皮书结构"""
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 14)
    ax.axis('off')

    sections = [
        {'y': 13, 'name': '🔖 文件头三行', 'color': C_RED,
         'desc': 'DNA追溯码 | 创建者UID9622 | 协议CC BY-NC-SA 4.0'},
        {'y': 11.5, 'name': '📋 输出类型声明', 'color': C_GOLD,
         'desc': '输出者·类型·可执行性·依赖·三色审计·DNA签名·GPG'},
        {'y': 10, 'name': '📐 方法论声明', 'color': C_BLUE,
         'desc': '三轨并行: 学术轨·工程轨·易经隐喻轨'},
        {'y': 8.5, 'name': '🎯 目标读者指南', 'color': C_GREEN,
         'desc': '政策·架构·学术·公众·协作者 五类读者阅读路径'},
        {'y': 7, 'name': '📖 摘要 TL;DR', 'color': C_PURPLE,
         'desc': '问题→方法→结论 三句话讲清'},
        {'y': 5.5, 'name': '📑 正文 N章', 'color': C_GOLD,
         'desc': '博弈分析·机制设计·架构·路线图·安全·结论'},
        {'y': 4, 'name': '📎 附录 A-J', 'color': C_SILVER,
         'desc': '术语表·FAQ·参考文献·致谢·版本历史'},
        {'y': 2.5, 'name': '✍️ 签章区', 'color': C_RED,
         'desc': '四联签章: DNA+GPG+创作者+版本 | P15归档'},
    ]

    for s in sections:
        rect = FancyBboxPatch((1, s['y']-0.6), 10, 1.2,
                               boxstyle='round,pad=0.1',
                               facecolor=C_CARD, edgecolor=s['color'],
                               linewidth=2, alpha=0.9)
        ax.add_patch(rect)
        ax.text(1.3, s['y']+0.1, s['name'], fontsize=13, fontweight='bold',
                color=s['color'])
        ax.text(1.3, s['y']-0.35, s['desc'], fontsize=9,
                color=COLORS['text_secondary'])

    # 箭头
    for i in range(len(sections)-1):
        ax.annotate('', xy=(6, sections[i+1]['y']+0.6),
                   xytext=(6, sections[i]['y']-0.6),
                   arrowprops=dict(arrowstyle='->', color=C_GOLD, lw=1.5, alpha=0.5))

    ax.set_title('龍魂·白皮书结构模板标准', fontsize=16, color=C_GOLD,
                 fontweight='bold', pad=20)
    add_longhun_header(fig, '白皮书模板·结构标准',
                       '文件头→声明→方法论→读者指南→摘要→正文→附录→签章 | 8段标准结构')
    return save_chart(fig, 'template', 1, '白皮书结构模板', fmt)


# ============================================================
# 批量生成
# ============================================================
def generate_all(whitepaper_key=None, chart_id=None, fmt='png'):
    """生成白皮书可视化图表"""
    results = []

    if whitepaper_key == 'all' or whitepaper_key is None:
        keys = list(WHITEPAPERS.keys())
    else:
        keys = [whitepaper_key] if whitepaper_key in WHITEPAPERS else []

    if not keys:
        print(f"❌ 未找到白皮书: {whitepaper_key}")
        print(f"   可用: {', '.join(WHITEPAPERS.keys())}")
        return results

    for key in keys:
        wp = WHITEPAPERS[key]
        print(f"\n{'='*60}")
        print(f"🐉 生成: {wp['name']} ({wp['version']})")
        print(f"{'='*60}")

        for chart in wp['charts']:
            if chart_id and chart['id'] != chart_id:
                continue

            print(f"  📊 图表 {chart['id']}: {chart['name']} ({chart['type']})...", end=' ')

            try:
                func = globals().get(chart['func'])
                if func:
                    filepath = func(fmt=fmt)
                    results.append({
                        'whitepaper': key,
                        'chart_id': chart['id'],
                        'chart_name': chart['name'],
                        'filepath': str(filepath),
                    })
                    print(f"✅ {filepath.name}")
                else:
                    print(f"❌ 函数 {chart['func']} 未定义")
            except Exception as e:
                print(f"❌ 错误: {e}")
                import traceback
                traceback.print_exc()

    return results


def list_whitepapers():
    """列所有白皮书和图表"""
    print("\n🐉 龍魂·白皮书可视化 总目")
    print("="*60)
    total_charts = 0
    for key, wp in WHITEPAPERS.items():
        print(f"\n📋 [{key}] {wp['name']} {wp['version']}")
        print(f"   文件: {wp['file']}")
        for chart in wp['charts']:
            print(f"   ├─ 图表{chart['id']}: {chart['name']} [{chart['type']}]")
            total_charts += 1
    print(f"\n{'='*60}")
    print(f"共 {len(WHITEPAPERS)} 份白皮书 · {total_charts} 张图表")
    print(f"输出目录: {OUTPUT_DIR}")


# ============================================================
# CLI
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description='🐉 龍魂·白皮书可视化引擎 v1.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_whitepaper_viz.py --whitepaper open-audit
  python3 bin/lh_whitepaper_viz.py --whitepaper all
  python3 bin/lh_whitepaper_viz.py --whitepaper persona --chart 1
  python3 bin/lh_whitepaper_viz.py --list
        """
    )
    parser.add_argument('--whitepaper', '-w', type=str, default='all',
                        help='白皮书标识 (open-audit/persona/privacy/harmonyos/deben/sovereignty/template/all)')
    parser.add_argument('--chart', '-c', type=int, default=None,
                        help='指定图表编号 (不指定则生成全部)')
    parser.add_argument('--format', '-f', type=str, default='png',
                        choices=['png', 'svg', 'pdf'],
                        help='输出格式 (默认: png)')
    parser.add_argument('--list', '-l', action='store_true',
                        help='列出所有白皮书和图表')
    parser.add_argument('--output', '-o', type=str, default=None,
                        help='输出目录 (默认: portal/viz/whitepapers/)')

    args = parser.parse_args()

    global OUTPUT_DIR
    if args.output:
        OUTPUT_DIR = Path(args.output)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.list:
        list_whitepapers()
        return

    # 批量生成
    results = generate_all(args.whitepaper, args.chart, args.format)

    # 汇总
    print(f"\n{'='*60}")
    print(f"📊 生成汇总: {len(results)} 张图表")
    print(f"📁 输出目录: {OUTPUT_DIR}")
    for r in results:
        print(f"  ✅ [{r['whitepaper']}] 图表{r['chart_id']}: {r['chart_name']}")
    print(f"{'='*60}")

    # 生成JSON索引
    index_path = OUTPUT_DIR / 'viz_index.json'
    index_data = {
        'generated_at': datetime.now().isoformat(),
        'engine_version': 'v1.0',
        'total_charts': len(results),
        'charts': results,
    }
    with open(index_path, 'w') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    print(f"📋 索引: {index_path}")


if __name__ == '__main__':
    main()
