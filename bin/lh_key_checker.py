#!/usr/bin/env python3
from __future__ import annotations
"""
🐉 龍魂 API 密钥检测器
DNA: #龍芯⚡️丙午·辛未·KEY-CHECKER-v1.0

扫描所有9个API的46个环境变量，按接口分组展示状态。
绿色=已配置 | 黄色=占位符 | 红色=缺失 | 灰色=本地模式(无需密钥)

用法:
    python3 bin/lh_key_checker.py              # 终端彩色报告
    python3 bin/lh_key_checker.py --json       # JSON输出（给其他脚本消费）
    python3 bin/lh_key_checker.py --export     # 导出待填写清单
"""

import os
import sys
import json
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class KeyEntry:
    name: str
    env_var: str
    status: str  # 'ok' | 'placeholder' | 'missing' | 'local'
    value_preview: str = ''
    login_url: str = ''
    category: str = ''
    provider: str = ''


# ═══════════════════════════════════════════════════════════
# 46个环境变量全量注册表
# ═══════════════════════════════════════════════════════════

REGISTRY: List[dict[str, Any]] = [
    # --- LLM ---
    {'category': 'LLM大模型', 'provider': 'DeepSeek', 'env': 'DEEPSEEK_API_KEY', 'url': 'https://platform.deepseek.com'},
    {'category': 'LLM大模型', 'provider': 'Kimi月之暗面', 'env': 'KIMI_API_KEY', 'url': 'https://platform.moonshot.cn'},
    {'category': 'LLM大模型', 'provider': '通义千问', 'env': 'QWEN_API_KEY', 'url': 'https://dashscope.aliyun.com'},
    {'category': 'LLM大模型', 'provider': '文心一言', 'env': 'WENXIN_API_KEY', 'url': 'https://console.bce.baidu.com/ai'},
    {'category': 'LLM大模型', 'provider': '文心一言', 'env': 'WENXIN_SECRET_KEY', 'url': 'https://console.bce.baidu.com/ai'},
    # --- ASR/TTS ---
    {'category': '语音ASR/TTS', 'provider': '讯飞', 'env': 'XUNFEI_APP_ID', 'url': 'https://www.xfyun.cn'},
    {'category': '语音ASR/TTS', 'provider': '讯飞', 'env': 'XUNFEI_API_KEY', 'url': 'https://www.xfyun.cn'},
    {'category': '语音ASR/TTS', 'provider': '讯飞', 'env': 'XUNFEI_API_SECRET', 'url': 'https://www.xfyun.cn'},
    {'category': '语音ASR/TTS', 'provider': '百度', 'env': 'BAIDU_APP_ID', 'url': 'https://console.bce.baidu.com/ai'},
    {'category': '语音ASR/TTS', 'provider': '百度', 'env': 'BAIDU_API_KEY', 'url': 'https://console.bce.baidu.com/ai'},
    {'category': '语音ASR/TTS', 'provider': '百度', 'env': 'BAIDU_SECRET_KEY', 'url': 'https://console.bce.baidu.com/ai'},
    {'category': '语音ASR/TTS', 'provider': '阿里云', 'env': 'ALI_ACCESS_KEY', 'url': 'https://ram.console.aliyun.com/manage/ak'},
    {'category': '语音ASR/TTS', 'provider': '阿里云', 'env': 'ALI_SECRET_KEY', 'url': 'https://ram.console.aliyun.com/manage/ak'},
    # --- 视觉 ---
    {'category': '视觉OCR/人脸', 'provider': '华为云', 'env': 'HUAWEICLOUD_AK', 'url': 'https://console.huaweicloud.com/iam'},
    {'category': '视觉OCR/人脸', 'provider': '华为云', 'env': 'HUAWEICLOUD_SK', 'url': 'https://console.huaweicloud.com/iam'},
    {'category': '视觉OCR/人脸', 'provider': '虹软', 'env': 'ARCSOFT_APP_ID', 'url': 'https://www.arcsoft.com.cn'},
    {'category': '视觉OCR/人脸', 'provider': '虹软', 'env': 'ARCSOFT_SDK_KEY', 'url': 'https://www.arcsoft.com.cn'},
    {'category': '视觉OCR/人脸', 'provider': '旷视', 'env': 'MEGVII_API_KEY', 'url': 'https://www.faceplusplus.com.cn'},
    {'category': '视觉OCR/人脸', 'provider': '旷视', 'env': 'MEGVII_API_SECRET', 'url': 'https://www.faceplusplus.com.cn'},
    # --- 地图 ---
    {'category': '地图', 'provider': '高德', 'env': 'AMAP_KEY', 'url': 'https://console.amap.com'},
    {'category': '地图', 'provider': '百度', 'env': 'BAIDU_API_KEY', 'url': 'https://lbsyun.baidu.com'},
    # --- 天气 ---
    {'category': '天气', 'provider': '和风天气', 'env': 'QWEATHER_KEY', 'url': 'https://dev.qweather.com'},
    {'category': '天气', 'provider': '心知天气', 'env': 'XINZHI_KEY', 'url': 'https://www.seniverse.com'},
    # --- 支付 ---
    {'category': '支付', 'provider': '微信支付', 'env': 'WECHAT_APP_ID', 'url': 'https://pay.weixin.qq.com'},
    {'category': '支付', 'provider': '微信支付', 'env': 'WECHAT_MCH_ID', 'url': 'https://pay.weixin.qq.com'},
    {'category': '支付', 'provider': '微信支付', 'env': 'WECHAT_API_KEY', 'url': 'https://pay.weixin.qq.com'},
    {'category': '支付', 'provider': '支付宝', 'env': 'ALIPAY_APP_ID', 'url': 'https://open.alipay.com'},
    {'category': '支付', 'provider': '支付宝', 'env': 'ALIPAY_PRIVATE_KEY', 'url': 'https://open.alipay.com'},
    {'category': '支付', 'provider': '支付宝', 'env': 'ALIPAY_PUBLIC_KEY', 'url': 'https://open.alipay.com'},
    {'category': '支付', 'provider': '数字人民币', 'env': 'DCEP_MERCHANT_ID', 'url': 'https://www.pbcdci.cn'},
    {'category': '支付', 'provider': '数字人民币', 'env': 'DCEP_PRIVATE_KEY', 'url': 'https://www.pbcdci.cn'},
    # --- 短信 ---
    {'category': '短信/推送', 'provider': '腾讯云', 'env': 'TENCENT_SECRET_ID', 'url': 'https://console.cloud.tencent.com/cam/capi'},
    {'category': '短信/推送', 'provider': '腾讯云', 'env': 'TENCENT_SECRET_KEY', 'url': 'https://console.cloud.tencent.com/cam/capi'},
]


# ═══════════════════════════════════════════════════════════
# 检测引擎
# ═══════════════════════════════════════════════════════════

PLACEHOLDER_PATTERNS = [
    'your_', 'YOUR_', '<YOUR_', 'changeme', 'placeholder',
    '填写', '替换', 'xxxx', 'test_key', 'my_key',
]


def _is_placeholder(value: str) -> bool:
    """判断值是否为占位符"""
    for p in PLACEHOLDER_PATTERNS:
        if p.lower() in value.lower():
            return True
    return False


def scan_all() -> Tuple[List[KeyEntry], dict[str, Any]]:
    """扫描全部环境变量，返回分组结果和统计"""
    entries: List[KeyEntry] = []
    stats = {'total': 0, 'ok': 0, 'placeholder': 0, 'missing': 0}

    for item in REGISTRY:
        env_var = item['env']
        value = os.environ.get(env_var, '')

        if not value:
            status = 'missing'
            preview = '(未设置)'
        elif _is_placeholder(value):
            status = 'placeholder'
            preview = value[:40] + ('...' if len(value) > 40 else '')
        else:
            status = 'ok'
            # 脱敏预览：显示前4后4
            if len(value) > 12:
                preview = value[:6] + '****' + value[-6:]
            else:
                preview = value[:3] + '***'

        stats['total'] += 1
        stats[status] = stats.get(status, 0) + 1

        entries.append(KeyEntry(
            name=env_var,
            env_var=env_var,
            status=status,
            value_preview=preview,
            login_url=item.get('url', ''),
            category=item['category'],
            provider=item['provider'],
        ))

    # 按分类分组
    grouped: Dict[str, List[KeyEntry]] = {}
    for e in entries:
        grouped.setdefault(e.category, []).append(e)

    return entries, grouped, stats


# ═══════════════════════════════════════════════════════════
# 输出格式化
# ═══════════════════════════════════════════════════════════

class Colors:
    """ANSI终端颜色"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'


def _status_icon(status: str) -> str:
    icons = {
        'ok': f'{Colors.GREEN}✅{Colors.RESET}',
        'placeholder': f'{Colors.YELLOW}⚠️{Colors.RESET}',
        'missing': f'{Colors.RED}❌{Colors.RESET}',
    }
    return icons.get(status, '?')


def render_terminal(entries, grouped, stats):
    """终端彩色输出"""
    total = stats['total']
    ok = stats['ok']
    ph = stats.get('placeholder', 0)
    miss = stats.get('missing', 0)
    coverage = int(ok / total * 100) if total > 0 else 0
    active = min(ok + ph, total)

    # Header
    print(f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗
║     🐉 龍魂 API 密钥检测报告                                ║
║     DNA: #龍芯⚡️丙午·辛未·KEY-CHECK-v1.0                   ║
╚══════════════════════════════════════════════════════════╝{Colors.RESET}
""")

    # 统计条
    bar_width = 40
    ok_width = int(ok / total * bar_width) if total > 0 else 0
    ph_width = int(ph / total * bar_width) if total > 0 else 0
    miss_width = bar_width - ok_width - ph_width

    bar = (
        f'{Colors.GREEN}{"█" * ok_width}'
        f'{Colors.YELLOW}{"▓" * ph_width}'
        f'{Colors.RED}{"░" * miss_width}'
        f'{Colors.RESET}'
    )
    print(f'  [{bar}]')
    print(f'  总变量: {total} | {Colors.GREEN}✅ {ok} 已配置{Colors.RESET} | {Colors.YELLOW}⚠️ {ph} 占位符{Colors.RESET} | {Colors.RED}❌ {miss} 缺失{Colors.RESET}')
    print(f'  覆盖率: {Colors.GREEN if coverage >= 50 else Colors.YELLOW if coverage >= 20 else Colors.RED}{coverage}%{Colors.RESET} (含占位符: {int(active/total*100)}%)')
    print()

    # 按分类展示
    for category, group_entries in grouped.items():
        cat_ok = sum(1 for e in group_entries if e.status == 'ok')
        cat_ph = sum(1 for e in group_entries if e.status == 'placeholder')
        cat_miss = sum(1 for e in group_entries if e.status == 'missing')
        cat_total = len(group_entries)

        icon = _status_icon('ok') if cat_ok == cat_total else _status_icon('placeholder') if cat_ph > 0 else _status_icon('missing')
        print(f'{Colors.BOLD}{Colors.MAGENTA}  ▸ {category}{Colors.RESET} {icon} ({cat_ok}/{cat_total})')

        # 按 provider 分组
        providers: dict[str, Any] = {}
        for e in group_entries:
            providers.setdefault(e.provider, []).append(e)

        for provider, prov_entries in providers.items():
            prov_all_ok = all(e.status == 'ok' for e in prov_entries)
            prov_pfx = f'{Colors.CYAN}    {provider}{Colors.RESET}'

            for e in prov_entries:
                si = _status_icon(e.status)
                preview = e.value_preview
                if e.status == 'missing':
                    preview = f'{Colors.RED}(未设置){Colors.RESET}'
                elif e.status == 'placeholder':
                    preview = f'{Colors.YELLOW}{preview}{Colors.RESET}'

                print(f'      {si} {Colors.DIM}{e.env_var}{Colors.RESET} → {preview}')
                if e.status != 'ok' and e.login_url:
                    print(f'        {Colors.DIM}↳ 获取: {e.login_url}{Colors.RESET}')

            print()  # providers之间留空

    # 摘要
    print(f'{Colors.BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}')
    if ok == 0:
        print(f'{Colors.RED}  🔴 所有密钥均未配置。请打开 config/api_keys.env 填入密钥。{Colors.RESET}')
    elif ph + miss == 0:
        print(f'{Colors.GREEN}  🟢 全部 {total} 个密钥已就绪！可运行全接口测试。{Colors.RESET}')
    else:
        unfilled = ph + miss
        print(f'{Colors.YELLOW}  🟡 {ok}/{total} 已就绪，{unfilled} 个待填入。{Colors.RESET}')
        if ph > 0:
            print(f'{Colors.YELLOW}     占位符 {ph} 个：在 config/api_keys.env 中替换 your_xxx{Colors.RESET}')
        if miss > 0:
            print(f'{Colors.RED}     缺失 {miss} 个：在 config/api_keys.env 中添加{Colors.RESET}')
    print(f'{Colors.CYAN}  📋 密钥模板: config/api_keys.env{Colors.RESET}')
    print(f'{Colors.CYAN}  🔄 加载命令: source config/api_keys.env{Colors.RESET}')
    print()

    return stats


def render_json(entries, grouped, stats):
    """JSON输出"""
    output = {
        'dna': '#龍芯⚡️丙午·辛未·KEY-CHECK-v1.0',
        'scan_time': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'stats': stats,
        'providers': {},
    }
    for entry in entries:
        provider_key = f'{entry.category}/{entry.provider}'
        output['providers'].setdefault(provider_key, {
            'category': entry.category,
            'provider': entry.provider,
            'login_url': entry.login_url,
            'status': 'ok',
            'keys': [],
        })
        output['providers'][provider_key]['keys'].append({
            'env_var': entry.env_var,
            'status': entry.status,
            'preview': entry.value_preview,
        })
        # 合并状态：一个provider所有key都ok才算ok
        if entry.status != 'ok':
            output['providers'][provider_key]['status'] = entry.status

    print(json.dumps(output, ensure_ascii=False, indent=2))


def render_export(entries, grouped, stats):
    """导出待填写清单"""
    todo = [e for e in entries if e.status != 'ok']

    print(f"""
🐉 龍魂 API 待填写清单
{'=' * 60}
共 {len(todo)}/{stats['total']} 个密钥待填入
""")

    current_provider = ''
    for e in todo:
        if e.provider != current_provider:
            current_provider = e.provider
            print(f'\n── {e.provider} ──')
            print(f'  登录: {e.login_url}')
        print(f'  ☐ {e.env_var} [{">占位符" if e.status == "placeholder" else "缺失"}]')

    print(f'\n{"=" * 60}')
    print(f'填完后运行: source config/api_keys.env && python3 bin/lh_key_checker.py\n')


# ═══════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description='🐉 龍魂 API 密钥检测器')
    parser.add_argument('--json', action='store_true', help='JSON格式输出')
    parser.add_argument('--export', action='store_true', help='导出待填写清单')
    args = parser.parse_args()

    entries, grouped, stats = scan_all()

    # 自动加载 config/api_keys.env 如果存在 (提升到shell环境)
    env_file = 'config/api_keys.env'
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, val = line.partition('=')
                    key = key.strip()
                    val = val.strip()
                    if key and val and key not in os.environ:
                        os.environ[key] = val

    # 重新扫描（可能有新加载的变量）
    entries, grouped, stats = scan_all()

    if args.json:
        render_json(entries, grouped, stats)
    elif args.export:
        render_export(entries, grouped, stats)
    else:
        render_terminal(entries, grouped, stats)


if __name__ == '__main__':
    main()
