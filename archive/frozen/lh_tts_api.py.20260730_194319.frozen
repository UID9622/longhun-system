#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·TTS-API-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
# 龍魂TTS统一接口 · 本地优先·云端备用
# DNA: #龍芯⚡️丙午·辛未·TTS-API-v1.0

"""🐉 龍魂引擎：lh_tts_api
路径：bin/lh_tts_api.py
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


class LonghunTTS:
    """龍魂语音合成统一接口"""

    PROVIDERS = {
        'xunfei': {
            'name': '讯飞TTS',
            'env_keys': ['XUNFEI_APP_ID', 'XUNFEI_API_KEY', 'XUNFEI_API_SECRET'],
            'priority': 1,
        },
        'baidu': {
            'name': '百度TTS',
            'env_keys': ['BAIDU_APP_ID', 'BAIDU_API_KEY', 'BAIDU_SECRET_KEY'],
            'priority': 2,
        },
        'ali': {
            'name': '阿里CosyVoice',
            'env_keys': ['ALI_ACCESS_KEY', 'ALI_SECRET_KEY'],
            'priority': 3,
        },
        'local': {
            'name': '本地ChatTTS',
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
            c.execute('''CREATE TABLE IF NOT EXISTS tts_audit
                         (dna TEXT, action TEXT, provider TEXT, hash TEXT, timestamp TEXT)''')
            c.execute('INSERT INTO tts_audit VALUES (?,?,?,?,?)',
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

    def synthesize(self, text: str, voice: str = 'default', output: str = 'output.wav', provider: str = 'auto') -> dict[str, Any]:
        self._audit('synthesize', provider, text[:100])

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
            'text': text,
            'voice': voice,
            'output': output,
            'dna': self.dna,
            'hash': self._hash_chain(text),
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
    parser = argparse.ArgumentParser(description='龍魂TTS统一接口')
    parser.add_argument('--dna', required=True, help='DNA追溯码')
    parser.add_argument('--text', help='输入文本')
    parser.add_argument('--voice', default='default', help='音色ID')
    parser.add_argument('--output', default='output.wav', help='输出路径')
    parser.add_argument('--provider', default='auto', help='服务商 (auto/xunfei/baidu/ali/local)')
    parser.add_argument('--list', action='store_true', help='列出可用服务商')
    args = parser.parse_args()

    try:
        tts = LonghunTTS(args.dna)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    if args.list:
        info = tts.list_providers()
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return 0

    if not args.text:
        print("❌ 需要 --text 参数", file=sys.stderr)
        return 1

    result = tts.synthesize(args.text, args.voice, args.output, args.provider)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
