#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·辛未·ASR-API-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
# 龍魂ASR统一接口 · 本地优先·云端备用
# DNA: #龍芯⚡️丙午·辛未·ASR-API-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

"""🐉 龍魂引擎：lh_asr_api
路径：bin/lh_asr_api.py
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


class LonghunASR:
    """龍魂语音识别统一接口"""

    PROVIDERS = {
        'xunfei': {
            'name': '讯飞语音',
            'env_keys': ['XUNFEI_APP_ID', 'XUNFEI_API_KEY', 'XUNFEI_API_SECRET'],
            'priority': 1,
        },
        'baidu': {
            'name': '百度语音',
            'env_keys': ['BAIDU_APP_ID', 'BAIDU_API_KEY', 'BAIDU_SECRET_KEY'],
            'priority': 2,
        },
        'ali': {
            'name': '阿里Paraformer',
            'env_keys': ['ALI_ACCESS_KEY', 'ALI_SECRET_KEY'],
            'priority': 3,
        },
        'local': {
            'name': '本地Whisper',
            'env_keys': [],
            'priority': 0,
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

    def _audit(self, action: str, provider: str, detail: str):
        try:
            os.makedirs(os.path.dirname(self.audit_db), exist_ok=True)
            conn = sqlite3.connect(self.audit_db)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS asr_audit
                         (dna TEXT, action TEXT, provider TEXT, hash TEXT, timestamp TEXT)''')
            c.execute('INSERT INTO asr_audit VALUES (?,?,?,?,?)',
                      (self.dna, action, provider, self._hash_chain(detail), self._lunar_timestamp()))
            conn.commit()
            conn.close()
        except Exception:
            pass

    def _check_provider(self, provider_id: str) -> tuple[Any, ...]:
        cfg = self.PROVIDERS.get(provider_id)
        if not cfg:
            return False, f"未知服务商: {provider_id}"
        for key in cfg['env_keys']:
            if not os.getenv(key):
                return False, f"缺少环境变量: {key}"
        return True, "ok"

    def transcribe(self, input_path: str, lang: str = 'zh', provider: str = 'auto') -> dict[str, Any]:
        self._audit('transcribe', provider, input_path)

        if not Path(input_path).exists():
            return {'success': False, 'error': f'文件不存在: {input_path}', 'dna': self.dna}

        # 自动选择服务商
        if provider == 'auto':
            for pid, cfg in sorted(self.PROVIDERS.items(), key=lambda x: x[1]['priority']):
                ok, _ = self._check_provider(pid)
                if ok:
                    provider = pid
                    break

        ok, msg = self._check_provider(provider)
        if not ok:
            return {
                'success': False,
                'error': f'{self.PROVIDERS.get(provider, {}).get("name", provider)}: {msg}',
                'dna': self.dna,
            }

        return {
            'success': True,
            'provider': self.PROVIDERS[provider]['name'],
            'text': f'[占位符] {input_path} 的语音识别结果',
            'lang': lang,
            'dna': self.dna,
            'hash': self._hash_chain(input_path),
            'status': 'placeholder',
            'message': '模型未接入，请执行道引流程审查后部署',
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
    parser = argparse.ArgumentParser(description='龍魂ASR统一接口')
    parser.add_argument('--dna', required=True, help='DNA追溯码')
    parser.add_argument('--input', help='输入音频路径')
    parser.add_argument('--lang', default='zh', help='语言 (zh/en)')
    parser.add_argument('--provider', default='auto', help='服务商 (auto/xunfei/baidu/ali/local)')
    parser.add_argument('--list', action='store_true', help='列出可用服务商')
    args = parser.parse_args()

    try:
        asr = LonghunASR(args.dna)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    if args.list:
        info = asr.list_providers()
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return 0

    if not args.input:
        print("❌ 需要 --input 参数", file=sys.stderr)
        return 1

    result = asr.transcribe(args.input, args.lang, args.provider)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
