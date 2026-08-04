#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# 龍魂天气/环境统一接口 · 缓存优先
# DNA: #龍芯⚡️丙午·辛未·WEATHER-API-v1.0

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


class LonghunWeather:
    """龍魂天气/环境统一接口"""

    PROVIDERS = {
        'qweather': {
            'name': '和风天气',
            'env_keys': ['QWEATHER_KEY'],
            'priority': 1,
        },
        'xinzhi': {
            'name': '心知天气',
            'env_keys': ['XINZHI_KEY'],
            'priority': 2,
        },
    }

    CACHE_DIR = 'data/cache/weather'
    CACHE_TTL = 1800  # 30分钟缓存

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

    def _get_cache(self, key: str) -> dict[str, Any]:
        try:
            cache_path = Path(self.CACHE_DIR) / f"{key}.json"
            if cache_path.exists():
                data = json.loads(cache_path.read_text())
                age = datetime.now().timestamp() - data.get('_cached_at', 0)
                if age < self.CACHE_TTL:
                    return data
        except Exception:
            pass
        return None

    def _set_cache(self, key: str, data: dict[str, Any]):
        try:
            os.makedirs(self.CACHE_DIR, exist_ok=True)
            data['_cached_at'] = datetime.now().timestamp()
            Path(self.CACHE_DIR, f"{key}.json").write_text(json.dumps(data, ensure_ascii=False))
        except Exception:
            pass

    def _audit(self, action: str, provider: str, detail: str):
        try:
            os.makedirs(os.path.dirname(self.audit_db), exist_ok=True)
            conn = sqlite3.connect(self.audit_db)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS weather_audit
                         (dna TEXT, action TEXT, provider TEXT, hash TEXT, timestamp TEXT)''')
            c.execute('INSERT INTO weather_audit VALUES (?,?,?,?,?)',
                      (self.dna, action, provider, self._hash_chain(detail), self._lunar_timestamp()))
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

    def now(self, city: str = '北京', provider: str = 'auto') -> dict[str, Any]:
        cache_key = f"now_{city}"
        cached = self._get_cache(cache_key)
        if cached:
            cached['from_cache'] = True
            return cached

        self._audit('now', provider, city)

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

        result = {
            'success': True,
            'provider': self.PROVIDERS[provider]['name'],
            'city': city,
            'temperature': 28,
            'humidity': 65,
            'wind': '东南风3级',
            'weather': '晴',
            'aqi': 45,
            'update_time': self._lunar_timestamp(),
            'dna': self.dna,
            'hash': self._hash_chain(city),
            'from_cache': False,
            'status': 'placeholder',
            'message': '天气服务未接入，请执行道引流程审查后部署',
        }

        self._set_cache(cache_key, result)
        return result

    def forecast(self, city: str = '北京', days: int = 3, provider: str = 'auto') -> dict[str, Any]:
        cache_key = f"forecast_{city}_{days}"
        cached = self._get_cache(cache_key)
        if cached:
            cached['from_cache'] = True
            return cached

        self._audit('forecast', provider, city)

        result = {
            'success': True,
            'city': city,
            'days': days,
            'forecast': [
                {'date': '07-14', 'high': 33, 'low': 24, 'weather': '晴'},
                {'date': '07-15', 'high': 31, 'low': 23, 'weather': '多云'},
                {'date': '07-16', 'high': 29, 'low': 22, 'weather': '小雨'},
            ][:days],
            'dna': self.dna,
            'hash': self._hash_chain(f"{city}:{days}"),
            'from_cache': False,
            'status': 'placeholder',
            'message': '天气服务未接入',
        }

        self._set_cache(cache_key, result)
        return result

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
    parser = argparse.ArgumentParser(description='龍魂天气/环境统一接口')
    parser.add_argument('--dna', required=True, help='DNA追溯码')
    parser.add_argument('--city', default='北京', help='城市')
    parser.add_argument('--days', type=int, default=3, help='预报天数')
    parser.add_argument('--forecast', action='store_true', help='天气预报')
    parser.add_argument('--provider', default='auto', help='服务商 (auto/qweather/xinzhi)')
    parser.add_argument('--list', action='store_true', help='列出可用服务商')
    args = parser.parse_args()

    try:
        weather = LonghunWeather(args.dna)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    if args.list:
        info = weather.list_providers()
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return 0

    if args.forecast:
        result = weather.forecast(args.city, args.days, args.provider)
    else:
        result = weather.now(args.city, args.provider)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
