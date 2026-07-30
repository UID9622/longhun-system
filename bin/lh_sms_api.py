#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·SMS-API-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
# 龍魂短信推送统一接口 · 审计留痕
# DNA: #龍芯⚡️丙午·辛未·SMS-API-v1.0

"""🐉 龍魂引擎：lh_sms_api
路径：bin/lh_sms_api.py
TODO：请补充详细功能说明（不少于20字）。"""
import os
import sys
import json
import hashlib
import argparse
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


class LonghunSMS:
    """龍魂短信推送统一接口"""

    PROVIDERS = {
        'aliyun': {
            'name': '阿里云短信',
            'env_keys': ['ALI_ACCESS_KEY', 'ALI_SECRET_KEY'],
            'priority': 1,
        },
        'tencent': {
            'name': '腾讯云短信',
            'env_keys': ['TENCENT_SECRET_ID', 'TENCENT_SECRET_KEY'],
            'priority': 2,
        },
    }

    def __init__(self, dna: str, audit_db: str = 'data/sqlite/audit.db'):
        self.dna = dna
        self.audit_db = audit_db
        if not self._validate_dna(dna):
            raise ValueError("DNA格式无效")

    def _validate_dna(self, dna: str) -> bool:
        return dna.startswith('#龍芯⚡️') and len(dna) > 20

    def _hash_chain(self, content: str) -> str:
        return hashlib.sha256(f"{self.dna}:{content}".encode()).hexdigest()[:16]

    def _lunar_timestamp(self) -> str:
        return datetime.now().strftime('丙午·%m月%d日·%H:%M')

    def _mask_phone(self, phone: str) -> str:
        if len(phone) >= 11:
            return phone[:3] + '****' + phone[-4:]
        return phone[:3] + '****'

    def _audit(self, action: str, provider: str, phone: str, detail: str):
        try:
            os.makedirs(os.path.dirname(self.audit_db), exist_ok=True)
            conn = sqlite3.connect(self.audit_db)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS sms_audit
                         (dna TEXT, action TEXT, provider TEXT, phone_masked TEXT, hash TEXT, timestamp TEXT)''')
            c.execute('INSERT INTO sms_audit VALUES (?,?,?,?,?,?)',
                      (self.dna, action, provider, self._mask_phone(phone),
                       self._hash_chain(detail), self._lunar_timestamp()))
            conn.commit()
            conn.close()
        except Exception:
            pass

    def _check_provider(self, provider: str) -> tuple[Any, ...]:
        cfg = self.PROVIDERS.get(provider)
        if not cfg:
            return False, f"未知服务商: {provider}"
        for key in cfg['env_keys']:
            if not os.getenv(key):
                return False, f"缺少环境变量: {key}"
        return True, "ok"

    def _auto_select_provider(self) -> str:
        """自动选择可用服务商"""
        for pid, cfg in sorted(self.PROVIDERS.items(), key=lambda x: x[1]['priority']):
            ok, _ = self._check_provider(pid)
            if ok:
                return pid
        return 'aliyun'  # 默认阿里云

    def send(self, phone: str, template_id: str, params: dict[str, Any] = None, provider: str = 'auto', sign_name: str = '龍魂系统') -> dict[str, Any]:
        if not phone or not phone.isdigit() or len(phone) < 11:
            return {'success': False, 'error': '手机号格式无效', 'dna': self.dna}

        if provider == 'auto':
            provider = self._auto_select_provider()

        ok, msg = self._check_provider(provider)
        if not ok:
            return {
                'success': False,
                'error': f'{self.PROVIDERS.get(provider, {}).get("name", provider)}: {msg}',
                'dna': self.dna,
            }

        self._audit('send', provider, phone, f"template:{template_id}")

        return {
            'success': True,
            'provider': self.PROVIDERS[provider]['name'],
            'phone': self._mask_phone(phone),
            'template_id': template_id,
            'sign_name': sign_name,
            'dna': self.dna,
            'hash': self._hash_chain(f"{phone}:{template_id}"),
            'status': 'placeholder',
            'message': '短信通道未接入，请执行道引流程审查后部署',
        }

    def list_providers(self) -> dict[str, Any]:
        providers = []
        for pid, cfg in sorted(self.PROVIDERS.items(), key=lambda x: x[1]['priority']):
            ok, msg = self._check_provider(pid)
            providers.append({
                'id': pid,
                'name': cfg['name'],
                'priority': cfg['priority'],
                'configured': ok,
                'message': '就绪' if ok else msg,
            })
        return {'providers': providers, 'dna': self.dna}


def main():
    parser = argparse.ArgumentParser(description='龍魂短信推送统一接口')
    parser.add_argument('--dna', required=True, help='DNA追溯码')
    parser.add_argument('--phone', help='手机号')
    parser.add_argument('--template', default='default', help='模板ID')
    parser.add_argument('--params', default='{}', help='模板参数JSON')
    parser.add_argument('--sign', default='龍魂系统', help='签名')
    parser.add_argument('--provider', default='auto', help='服务商 (auto/aliyun/tencent)')
    parser.add_argument('--list', action='store_true', help='列出可用服务商')
    args = parser.parse_args()

    try:
        sms = LonghunSMS(args.dna)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    if args.list:
        info = sms.list_providers()
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return 0

    if not args.phone:
        print("❌ 需要 --phone 参数", file=sys.stderr)
        return 1

    params = json.loads(args.params) if args.params else {}
    result = sms.send(args.phone, args.template, params, args.provider, args.sign)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
