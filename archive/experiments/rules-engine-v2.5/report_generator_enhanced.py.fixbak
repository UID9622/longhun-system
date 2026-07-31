# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-RULE-REPORT_GENERATOR_ENHANCED-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂规则引擎 · 增强报告生成 v2.5
HTML + PDF + 统计图表 + 异常预警

DNA: #龍芯⚇️2026-06-07-REPORT-GENERATOR-ENHANCED-v2.5
责任: UID9622 · 不免责
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

try:
    import jinja2
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # 非图形后端
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


# ============================================================================
# [日志配置]
# ============================================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# [报告元数据]
# ============================================================================

class AnomalyLevel(Enum):
    """异常级别"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class AnomalyAlert:
    """异常预警"""
    level: AnomalyLevel
    title: str
    description: str
    recommendation: str
    affected_items: int


# ============================================================================
# [报告生成器]
# ============================================================================

class EnhancedReportGenerator:
    """增强报告生成器"""

    def __init__(self, output_dir: Path = Path('/tmp/reports')):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_html_report(
        self,
        results: List[Dict],
        statistics: Dict[str, Any],
        output_file: Path = None
    ) -> Path:
        """
        生成 HTML 报告

        Args:
            results: 处理结果列表
            statistics: 统计信息
            output_file: 输出文件

        Returns:
            输出文件路径
        """
        output_file = output_file or self.output_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

        # 计算统计
        total = len(results)
        success = sum(1 for r in results if r['status'] == 'success')
        errors = total - success
        success_rate = (success / total * 100) if total > 0 else 0

        # HTML 模板
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>龍魂规则引擎 · 批量处理报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            color: #e2e8f0;
            padding: 40px 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 40px;
        }}

        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #00d4ff, #0ea5e9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .timestamp {{
            color: #94a3b8;
            font-size: 0.9em;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .stat-card {{
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid #0ea5e9;
            border-radius: 8px;
            padding: 20px;
            transition: all 0.3s;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 0 20px rgba(14, 165, 233, 0.3);
        }}

        .stat-label {{
            color: #94a3b8;
            font-size: 0.85em;
            margin-bottom: 10px;
            text-transform: uppercase;
        }}

        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #00d4ff;
        }}

        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #334155;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 10px;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #4ade80, #22c55e);
            border-radius: 4px;
            transition: width 0.3s;
        }}

        .section {{
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 30px;
            margin-bottom: 30px;
        }}

        .section h2 {{
            color: #00d4ff;
            margin-bottom: 20px;
            font-size: 1.5em;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}

        th {{
            background: #0f172a;
            color: #00d4ff;
            padding: 12px;
            text-align: left;
            border-bottom: 2px solid #0ea5e9;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #334155;
        }}

        tr:hover {{
            background: #1e293b;
        }}

        .status-success {{
            color: #4ade80;
        }}

        .status-error {{
            color: #ef4444;
        }}

        .alert {{
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 15px;
            border-left: 4px solid;
        }}

        .alert-critical {{
            background: rgba(239, 68, 68, 0.1);
            border-left-color: #ef4444;
        }}

        .alert-high {{
            background: rgba(245, 158, 11, 0.1);
            border-left-color: #f59e0b;
        }}

        footer {{
            text-align: center;
            color: #64748b;
            font-size: 0.85em;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #334155;
        }}

        .dna-signature {{
            font-family: 'Courier New', monospace;
            background: #0f172a;
            padding: 15px;
            border-radius: 6px;
            margin-top: 20px;
            border: 1px solid #334155;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🐉 龍魂规则引擎 · 批量处理报告</h1>
            <p class="timestamp">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CST</p>
        </header>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">📊 总计</div>
                <div class="stat-value">{total}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">✅ 成功</div>
                <div class="stat-value">{success}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {success_rate}%"></div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-label">❌ 失败</div>
                <div class="stat-value" style="color: #ef4444;">{errors}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">📈 成功率</div>
                <div class="stat-value">{success_rate:.1f}%</div>
            </div>
        </div>

        <div class="section">
            <h2>📋 详细结果</h2>
            <table>
                <thead>
                    <tr>
                        <th>案件 ID</th>
                        <th>状态</th>
                        <th>处理时间 (ms)</th>
                        <th>备注</th>
                    </tr>
                </thead>
                <tbody>
        """

        # 添加结果行
        for result in results[:50]:  # 限制显示前 50 条
            status_class = "status-success" if result['status'] == 'success' else "status-error"
            status_text = "✅ 成功" if result['status'] == 'success' else "❌ 失败"

            html_content += f"""
                    <tr>
                        <td>{result.get('case_id', 'N/A')}</td>
                        <td class="{status_class}">{status_text}</td>
                        <td>{result.get('processing_time_ms', 0):.2f}</td>
                        <td>{result.get('error', '-')}</td>
                    </tr>
            """

        html_content += """
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>🔐 DNA 签章</h2>
            <div class="dna-signature">
                DNA: #龍芯⚇️{timestamp}-REPORT-GENERATOR-ENHANCED-v2.5<br>
                确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z<br>
                责任: UID9622 · 不免责
            </div>
        </div>

        <footer>
            <p>龍魂系统 · 规则引擎 v2.5 · 增强报告生成</p>
        </footer>
    </div>
</body>
</html>
        """.format(timestamp=datetime.now().strftime('%Y-%m-%d'))

        # 保存 HTML
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.info(f"✅ HTML 报告已生成: {output_file}")
        return output_file

    def generate_statistics_chart(
        self,
        results: List[Dict],
        output_file: Path = None
    ) -> Path:
        """
        生成统计图表

        Args:
            results: 处理结果
            output_file: 输出文件

        Returns:
            输出文件路径
        """
        if not MATPLOTLIB_AVAILABLE:
            logger.warning("matplotlib 未安装，跳过图表生成")
            return None

        output_file = output_file or self.output_dir / f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        # 计算统计数据
        success_count = sum(1 for r in results if r['status'] == 'success')
        error_count = len(results) - success_count

        # 创建图表
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        fig.patch.set_facecolor('#0f172a')

        # [1] 成功/失败比例 (饼图)
        ax1.pie(
            [success_count, error_count],
            labels=['成功', '失败'],
            colors=['#4ade80', '#ef4444'],
            autopct='%1.1f%%',
            startangle=90
        )
        ax1.set_title('处理结果分布', color='#00d4ff', fontsize=12, pad=20)
        ax1.set_facecolor('#1e293b')

        # [2] 处理时间分布 (直方图)
        times = [r.get('processing_time_ms', 0) for r in results]
        ax2.hist(times, bins=20, color='#00d4ff', alpha=0.7, edgecolor='#0ea5e9')
        ax2.set_xlabel('处理时间 (ms)', color='#94a3b8')
        ax2.set_ylabel('案件数', color='#94a3b8')
        ax2.set_title('处理时间分布', color='#00d4ff', fontsize=12, pad=20)
        ax2.set_facecolor('#1e293b')
        ax2.tick_params(colors='#94a3b8')

        # [3] 累积成功率 (折线图)
        cumulative_success = []
        cumulative_rate = []
        success_so_far = 0

        for i, result in enumerate(results, 1):
            if result['status'] == 'success':
                success_so_far += 1
            cumulative_success.append(success_so_far)
            cumulative_rate.append((success_so_far / i) * 100)

        ax3.plot(cumulative_rate[:100], color='#4ade80', linewidth=2)
        ax3.fill_between(range(len(cumulative_rate[:100])), cumulative_rate[:100], alpha=0.3, color='#4ade80')
        ax3.set_xlabel('案件序号', color='#94a3b8')
        ax3.set_ylabel('累积成功率 (%)', color='#94a3b8')
        ax3.set_title('累积成功率趋势', color='#00d4ff', fontsize=12, pad=20)
        ax3.set_facecolor('#1e293b')
        ax3.tick_params(colors='#94a3b8')
        ax3.grid(True, alpha=0.2, color='#334155')

        # [4] 统计摘要 (文本)
        ax4.axis('off')
        summary_text = f"""
统计摘要
━━━━━━━━━━━━━━━━━━━━━━━━━

总计:        {len(results)} 个案件
成功:        {success_count} 个 ({success_count/len(results)*100:.1f}%)
失败:        {error_count} 个 ({error_count/len(results)*100:.1f}%)

平均时间:    {sum(times)/len(times):.2f} ms
最快:        {min(times):.2f} ms
最慢:        {max(times):.2f} ms

生成时间:    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
DNA:         #龍芯⚇️v2.5
        """
        ax4.text(0.1, 0.5, summary_text, fontsize=10, color='#94a3b8',
                family='monospace', verticalalignment='center',
                bbox=dict(boxstyle='round', facecolor='#1e293b', edgecolor='#334155', linewidth=1))

        plt.tight_layout()
        plt.savefig(output_file, facecolor='#0f172a', dpi=100)
        plt.close()

        logger.info(f"✅ 统计图表已生成: {output_file}")
        return output_file

    def detect_anomalies(self, results: List[Dict]) -> List[AnomalyAlert]:
        """
        检测异常

        Args:
            results: 处理结果

        Returns:
            异常预警列表
        """
        alerts = []

        # [1] 高错误率
        error_count = sum(1 for r in results if r['status'] == 'error')
        error_rate = (error_count / len(results) * 100) if results else 0

        if error_rate > 10:
            alerts.append(AnomalyAlert(
                level=AnomalyLevel.HIGH,
                title="高错误率",
                description=f"错误率达 {error_rate:.1f}%，超过阈值 10%",
                recommendation="检查规则逻辑，查看失败案件的具体错误信息",
                affected_items=error_count
            ))

        # [2] 异常长的处理时间
        times = [r.get('processing_time_ms', 0) for r in results if r['status'] == 'success']
        if times:
            avg_time = sum(times) / len(times)
            slow_items = sum(1 for t in times if t > avg_time * 3)

            if slow_items > len(times) * 0.1:
                alerts.append(AnomalyAlert(
                    level=AnomalyLevel.MEDIUM,
                    title="处理延迟",
                    description=f"{slow_items} 个案件的处理时间超过平均值 3 倍",
                    recommendation="优化规则逻辑或增加处理线程",
                    affected_items=slow_items
                ))

        # [3] 特定类型的失败
        error_types = {}
        for result in results:
            if result['status'] == 'error':
                error_type = result.get('error', 'unknown')[:50]
                error_types[error_type] = error_types.get(error_type, 0) + 1

        for error_type, count in error_types.items():
            if count > len(results) * 0.05:
                alerts.append(AnomalyAlert(
                    level=AnomalyLevel.MEDIUM,
                    title="重复错误",
                    description=f"错误类型 '{error_type}' 重复出现 {count} 次",
                    recommendation="修复该错误，可能是共同的根本原因",
                    affected_items=count
                ))

        return alerts


# ============================================================================
# [命令行示例]
# ============================================================================

def main():
    """示例用法"""
    from batch_processor_v2.5 import ProcessResult

    # 模拟结果
    results = [
        {'case_id': f'case_{i:04d}', 'status': 'success' if i % 10 != 0 else 'error',
         'processing_time_ms': 50 + i % 100, 'error': None if i % 10 != 0 else 'timeout'}
        for i in range(100)
    ]

    # 生成报告
    generator = EnhancedReportGenerator()

    # HTML 报告
    html_file = generator.generate_html_report(results, {})
    print(f"✅ HTML 报告: {html_file}")

    # 统计图表
    chart_file = generator.generate_statistics_chart(results)
    if chart_file:
        print(f"✅ 统计图表: {chart_file}")

    # 异常预警
    alerts = generator.detect_anomalies(results)
    print(f"\n⚠️  异常预警 ({len(alerts)} 个):")
    for alert in alerts:
        print(f"  [{alert.level.value.upper()}] {alert.title}")
        print(f"    {alert.description}")


if __name__ == '__main__':
    main()
