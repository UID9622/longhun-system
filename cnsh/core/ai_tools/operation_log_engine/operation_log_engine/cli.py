#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1296-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: cli.py | 标记时间: 2026-06-03T07:46:12+0800
# -*- coding: utf-8 -*-
"""
🧬 龍魂操作日记引擎 · cli.py

DNA:#龍芯⚡️丙午·癸巳·甲辰·庚午·䷑蛊-CLI-TOOL-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
责任: UID9622·不免责

命令行界面工具。提供 8 个核心命令供用户使用。
"""

import click
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# Add parent directory to path for imports
_parent_dir = str(Path(__file__).parent.parent)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from operation_log_engine.config import Config
from operation_log_engine.logging_config import logger_cli
from operation_log_engine.encryption_enforce import EncryptionEnforcer, EncryptedAPIResponse
from core.operation_ledger import OperationLedger
from core.dna_particle_generator import DNAParticleGenerator
from core.habit_fingerprint_manager import HabitFingerprintManager
from core.cross_device_identifier import CrossDeviceIdentifier
from core.sync_engine import SyncEngine
from core.multisig_gate import MultisigGate
from core.query_tool import QueryTool


# ==================== 辅助函数 ====================

def print_header(title: str) -> None:
    """打印标题栏"""
    click.echo()
    click.echo("=" * 60)
    click.echo(f"🧬 {title}")
    click.echo("=" * 60)


def print_success(message: str) -> None:
    """打印成功消息"""
    click.echo(click.style(f"✅ {message}", fg="green"))


def print_error(message: str) -> None:
    """打印错误消息"""
    click.echo(click.style(f"❌ {message}", fg="red"), err=True)


def print_warning(message: str) -> None:
    """打印警告消息"""
    click.echo(click.style(f"⚠️  {message}", fg="yellow"))


def print_info(message: str) -> None:
    """打印信息消息"""
    click.echo(click.style(f"ℹ️  {message}", fg="blue"))


def print_encrypted_signature(task_name: str) -> None:
    """打印加密签名"""
    signature = EncryptionEnforcer.create_signature(task_name)
    click.echo()
    click.echo("=" * 80)
    click.echo(click.style("🔐 加密签名验证", fg="cyan"))
    click.echo("=" * 80)
    click.echo(f"DNA:    {signature['dna']}")
    click.echo(f"CONFIRM: {signature['confirm']}")
    click.echo(f"主权人:  {signature['sovereignty']}")
    click.echo(f"GPG:    {signature['gpg_key_id']}")
    click.echo(f"时间:   {signature['timestamp']}")
    click.echo("=" * 80)


# ==================== 全局对象 ====================

@click.group()
@click.version_option(version="1.0.0", prog_name="龍魂操作日记引擎")
def main():
    """
    🧬 龍魂操作日记引擎 v1.0 · DNA认人·习惯识别

    完整的本地去中心化身份系统。记录操作·生成 DNA·识别用户·离线同步·完整审计。
    """
    # 验证配置
    if not Config.validate():
        print_error("配置验证失败")
        sys.exit(1)


# ==================== 命令 1: init ====================

@main.command()
@click.option("--force", is_flag=True, help="强制重新初始化 (会覆盖现有数据)")
def init(force: bool):
    """初始化龍魂系统"""
    print_header("初始化操作日记系统")

    try:
        # 检查是否已初始化
        if Config.LEDGER_FILE.exists() and not force:
            print_warning("系统已初始化。使用 --force 强制重新初始化")
            return

        # 初始化目录
        if not Config.init_directories():
            raise Exception("无法创建目录")

        # 初始化 OperationLedger
        ledger = OperationLedger()
        print_info("📝 初始化操作日记...")

        # 初始化习惯指纹管理器
        habits = HabitFingerprintManager()
        print_info("👤 初始化习惯指纹管理器...")
        # 建立初始基线
        baseline = habits.establish_baseline([])
        habits.save_baseline(baseline)

        # 初始化设备识别
        device = CrossDeviceIdentifier()
        device.register_device()
        print_info("🖥️  注册当前设备...")

        print_success("系统初始化完成!")
        print_info(f"数据目录: {Config.DATA_DIR}")
        logger_cli.info("系统初始化完成")

    except Exception as e:
        print_error(f"初始化失败: {e}")
        logger_cli.error(f"初始化失败: {e}", exc_info=True)
        sys.exit(1)


# ==================== 命令 2: record ====================

@main.command()
@click.argument("operation_type")
@click.option("--description", default="", help="操作描述")
@click.option("--device-id", default=None, help="设备 ID (默认自动检测)")
def record(operation_type: str, description: str, device_id: Optional[str]):
    """记录新操作"""
    print_header(f"记录操作: {operation_type}")

    try:
        ledger = OperationLedger()
        dna_gen = DNAParticleGenerator()
        habits = HabitFingerprintManager()
        device = CrossDeviceIdentifier()

        # 自动检测设备 ID
        if not device_id:
            device_id = device.get_device_id()

        # 记录操作
        print_info(f"📝 记录操作: {operation_type}")
        operation = ledger.append_operation(
            operation_type=operation_type,
            operation_name=operation_type,
            device_id=device_id,
            agent_type="CLI",
            input_text=description
        )

        operation_id = operation["operation_id"]
        print_success(f"操作已记录: {operation_id}")

        # 生成 DNA 粒子
        print_info("🧬 生成 DNA 粒子...")
        dna_particle = dna_gen.generate_from_record(operation)
        print_success(f"DNA 粒子已生成")

        # 更新习惯特征
        print_info("👤 更新习惯特征...")
        text_content = f"{operation_type} - {description}"
        habits.extract_habit_features(text_content)

        # 计算习惯信心度
        si_score, _ = habits.compute_habit_match(text_content)
        print_success(f"习惯信心度 (SI): {si_score:.2%}")

        # 打印结果
        click.echo()
        click.echo("操作记录:")
        click.echo(f"  ID: {operation_id}")
        click.echo(f"  类型: {operation_type}")
        click.echo(f"  设备: {device_id}")
        click.echo(f"  时间: {operation['timestamp']}")
        click.echo(f"  信心度: {si_score:.2%}")
        click.echo()

        logger_cli.info(f"操作已记录: {operation_id}")

    except Exception as e:
        print_error(f"记录失败: {e}")
        logger_cli.error(f"记录失败: {e}", exc_info=True)
        sys.exit(1)


# ==================== 命令 3: sync ====================

@main.command()
@click.option("--usb-path", default=None, help="USB 挂载路径")
@click.option("--merge-strategy", type=click.Choice(["overwrite", "merge", "manual"]), default="merge", help="合并策略")
def sync(usb_path: Optional[str], merge_strategy: str):
    """进行 USB 同步"""
    print_header("USB 同步操作")

    try:
        usb_path = usb_path or str(Config.USB_MOUNT_PATH)

        # 检查 USB 路径
        if not Path(usb_path).exists():
            print_warning(f"USB 路径不存在: {usb_path}")
            print_info("请确保 USB 已正确挂载")
            return

        # 初始化同步引擎
        sync_engine = SyncEngine()
        multisig = MultisigGate()

        print_info(f"📂 从 {usb_path} 同步...")

        # 执行同步
        sync_result = sync_engine.sync_from_usb(
            usb_path=usb_path,
            merge_strategy=merge_strategy
        )

        # 验证同步后的操作
        print_info("🔐 验证同步操作...")
        rejected_count = 0
        approved_count = 0

        for sync_op in sync_result.get("synced_operations", []):
            op_id = sync_op.get("operation_id")
            verify_result = multisig.verify_operation(
                operation=sync_op,
                device_seal=sync_op.get("device_seal", "")
            )
            if verify_result.verdict == "approved":
                approved_count += 1
            else:
                rejected_count += 1

        # 打印结果
        click.echo()
        click.echo("同步结果:")
        click.echo(f"  ✅ 通过验证: {approved_count}")
        if rejected_count > 0:
            click.echo(click.style(f"  ❌ 验证失败: {rejected_count}", fg="red"))
        click.echo()

        # 检查冲突
        conflicts = sync_result.get("conflicts", [])
        if conflicts:
            print_warning(f"检测到 {len(conflicts)} 个冲突")
            for conflict in conflicts[:5]:  # 只显示前 5 个
                click.echo(f"  - {conflict.get('type')}: {conflict.get('affected_op_id')}")

        print_success(f"同步完成! (已同步 {len(sync_result.get('synced_operations', []))} 个操作)")
        logger_cli.info(f"同步完成: {approved_count} 通过, {rejected_count} 失败")

    except Exception as e:
        print_error(f"同步失败: {e}")
        logger_cli.error(f"同步失败: {e}", exc_info=True)
        sys.exit(1)


# ==================== 命令 4: audit ====================

@main.command()
@click.option("--days", type=int, default=7, help="审计时间范围 (天)")
@click.option("--output", type=click.Path(), default=None, help="输出文件 (JSON)")
def audit(days: int, output: Optional[str]):
    """生成审计报告"""
    print_header(f"生成审计报告 ({days} 天)")

    try:
        tool = QueryTool()

        # 生成报告
        print_info(f"📊 生成审计报告...")
        report = tool.generate_audit_report(days=days)

        # 打印摘要
        click.echo()
        click.echo("审计摘要:")
        click.echo(f"  📝 操作数: {report['system_stats']['total_operations']}")
        click.echo(f"  🖥️  设备数: {report['system_stats']['total_devices']}")
        click.echo(f"  👤 习惯匹配: {report['system_stats']['avg_habit_match']:.2%}")

        # 合规性检查
        compliance = report.get("compliance", {})
        click.echo()
        click.echo("合规性检查:")
        click.echo(f"  {'✅' if compliance.get('hash_chain_verified') else '❌'} SHA-256 链完整性")
        click.echo(f"  {'✅' if compliance.get('no_duplicate_ids') else '❌'} ID 唯一性")
        click.echo(f"  {'✅' if compliance.get('timestamps_monotonic') else '❌'} 时间戳递增")

        # 安全警报
        alerts = report.get("security_alerts", [])
        if alerts:
            print_warning(f"安全警报: {len(alerts)} 个")

        # 同步统计
        sync_stats = report.get("sync_summary", {})
        if sync_stats.get("total_syncs", 0) > 0:
            success_rate = sync_stats.get("successful", 0) / sync_stats.get("total_syncs", 1)
            click.echo(f"  同步成功率: {success_rate:.2%}")

        click.echo()

        # 输出到文件
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print_success(f"报告已导出: {output_path}")

        print_success("审计报告完成!")
        logger_cli.info(f"审计报告生成完成 ({days} 天)")

    except Exception as e:
        print_error(f"审计失败: {e}")
        logger_cli.error(f"审计失败: {e}", exc_info=True)
        sys.exit(1)


# ==================== 命令 5: status ====================

@main.command()
def status():
    """显示系统状态"""
    print_header("系统状态")

    try:
        tool = QueryTool()
        habits = HabitFingerprintManager()

        # 获取系统统计
        stats = tool.get_system_stats()

        click.echo()
        click.echo("📊 系统统计:")
        click.echo(f"  📝 操作数: {stats['total_operations']}")
        click.echo(f"  🖥️  设备数: {stats['total_devices']}")
        click.echo(f"  👤 平均匹配度: {stats['avg_habit_match']:.2%}")

        # 操作类型分布
        op_types = stats.get('operation_types_distribution', {})
        if op_types:
            click.echo()
            click.echo("📋 操作类型分布:")
            for op_type, count in sorted(op_types.items(), key=lambda x: x[1], reverse=True):
                click.echo(f"  - {op_type}: {count}")

        # 同步统计
        sync_summary = stats.get('sync_summary', {})
        if sync_summary.get('total_syncs', 0) > 0:
            click.echo()
            click.echo("🔄 同步统计:")
            click.echo(f"  成功: {sync_summary['successful']}/{sync_summary['total_syncs']}")
            click.echo(f"  失败: {sync_summary.get('failed', 0)}")

        # 习惯分析
        click.echo()
        click.echo("👤 习惯分析:")
        habit_analysis = tool.analyze_habit_fingerprint()
        si = habit_analysis.get('confidence_metrics', {}).get('overall_si', 0)
        click.echo(f"  信心度 (SI): {si:.2%}")

        # 验证统计
        verifications = stats.get('verification_summary', {})
        if verifications:
            click.echo()
            click.echo("🔐 验证统计:")
            click.echo(f"  通过: {verifications.get('approved', 0)}")
            click.echo(f"  拒绝: {verifications.get('rejected', 0)}")

        click.echo()
        print_success("系统状态正常")
        print_encrypted_signature("system-status")
        logger_cli.info("系统状态查询完成")

    except Exception as e:
        print_error(f"状态查询失败: {e}")
        logger_cli.error(f"状态查询失败: {e}", exc_info=True)
        sys.exit(1)


# ==================== 命令 6: habits ====================

@main.command()
@click.option("--days", type=int, default=7, help="分析时间范围 (天)")
def habits(days: int):
    """分析习惯特征"""
    print_header(f"习惯特征分析 ({days} 天)")

    try:
        tool = QueryTool()
        habits_mgr = HabitFingerprintManager()

        # 获取习惯分析
        analysis = tool.analyze_habit_fingerprint()

        click.echo()
        click.echo("📊 习惯特征统计:")

        # 拼音错别字
        typos = analysis.get('typos', {})
        if typos:
            click.echo()
            click.echo("✏️  常见拼音错别字:")
            for typo, count in list(sorted(typos.items(), key=lambda x: x[1], reverse=True))[:5]:
                click.echo(f"  - {typo}: {count} 次")

        # 口头禅
        catchphrases = analysis.get('catchphrases', {})
        if catchphrases:
            click.echo()
            click.echo("🗣️  常用口头禅:")
            for phrase, count in list(sorted(catchphrases.items(), key=lambda x: x[1], reverse=True))[:5]:
                click.echo(f"  - {phrase}: {count} 次")

        # 多音字偏好
        polyphonic = analysis.get('polyphonic', {})
        if polyphonic:
            click.echo()
            click.echo("🔤 多音字偏好:")
            for char, pref in list(polyphonic.items())[:5]:
                click.echo(f"  - {char}: {pref}")

        # 信心度
        confidence = analysis.get('confidence_metrics', {})
        click.echo()
        click.echo("📈 信心度评分:")
        click.echo(f"  整体 SI: {confidence.get('overall_si', 0):.2%}")

        # 习惯趋势
        trend = tool.get_habit_trend(days=days)
        if trend:
            click.echo()
            click.echo(f"📉 {days} 天操作趋势:")
            for date, count in sorted(trend.items())[-7:]:
                bar = "█" * (count // 10)
                click.echo(f"  {date}: {bar} {count}")

        click.echo()
        print_success("习惯分析完成")
        logger_cli.info(f"习惯分析完成 ({days} 天)")

    except Exception as e:
        print_error(f"习惯分析失败: {e}")
        logger_cli.error(f"习惯分析失败: {e}", exc_info=True)
        sys.exit(1)


# ==================== 命令 7: config ====================

@main.command()
def config():
    """显示系统配置"""
    print_header("系统配置")
    Config.print_config()
    logger_cli.info("配置查询完成")


# ==================== 命令 8: version ====================

@main.command()
def version():
    """显示版本信息"""
    click.echo()
    click.echo("🧬 龍魂操作日记引擎")
    click.echo(f"版本: {Config.VERSION}")
    click.echo(f"DNA:#龍芯⚡️丙午·癸巳·甲辰·庚午·䷑蛊-CLI-TOOL-v1.0")
    click.echo(f"责任: UID9622·不免责")
    click.echo()
    logger_cli.info("版本查询")


# ==================== 入口点 ====================

if __name__ == "__main__":
    main()
