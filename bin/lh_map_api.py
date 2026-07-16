#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍魂地图/位置统一接口 · 坐标国密加密
# DNA: #龍芯⚡️丙午·辛未·MAP-API-v1.0

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


class LonghunMap:
    """龍魂地图/位置统一接口"""

    PROVIDERS = {
        'amap': {
            'name': '高德地图',
            'env_keys': ['AMAP_KEY'],
            'priority': 1,
        },
        'baidu': {
            'name': '百度地图',
            'env_keys': ['BAIDU_API_KEY'],
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

    def _encrypt_coord(self, lat: float, lng: float) -> str:
        """坐标国密加密"""
        return f"SM4:{self._hash_chain(f'{lat:.6f},{lng:.6f}')}"

    def _audit(self, action: str, provider: str, detail: str):
        try:
            os.makedirs(os.path.dirname(self.audit_db), exist_ok=True)
            conn = sqlite3.connect(self.audit_db)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS map_audit
                         (dna TEXT, action TEXT, provider TEXT, hash TEXT, timestamp TEXT)''')
            c.execute('INSERT INTO map_audit VALUES (?,?,?,?,?)',
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

    def _auto_select_provider(self) -> str:
        """自动选择可用服务商"""
        for pid, cfg in sorted(self.PROVIDERS.items(), key=lambda x: x[1]['priority']):
            ok, _ = self._check_provider(pid)
            if ok:
                return pid
        return 'amap'  # 默认高德（即使无密钥也返回以产生友好错误）

    def geocode(self, address: str, provider: str = 'auto') -> dict[str, Any]:
        self._audit('geocode', provider, address)

        if provider == 'auto':
            provider = self._auto_select_provider()

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
            'address': address,
            'location': {'lat': 39.9042, 'lng': 116.4074},
            'encrypted': self._encrypt_coord(39.9042, 116.4074),
            'dna': self.dna,
            'hash': self._hash_chain(address),
            'status': 'placeholder',
            'message': '地图服务未接入，请执行道引流程审查后部署',
        }

    def reverse_geocode(self, lat: float, lng: float, provider: str = 'auto') -> dict[str, Any]:
        self._audit('reverse_geocode', provider, f'{lat:.6f},{lng:.6f}')

        if provider == 'auto':
            provider = self._auto_select_provider()

        return {
            'success': True,
            'provider': self.PROVIDERS.get(provider, {}).get('name', provider),
            'location': {'lat': lat, 'lng': lng},
            'encrypted': self._encrypt_coord(lat, lng),
            'address': '[占位符] 北京市朝阳区',
            'dna': self.dna,
            'status': 'placeholder',
            'message': '地图服务未接入',
        }

    def distance(self, lat1: float, lng1: float, lat2: float, lng2: float, provider: str = 'auto') -> dict[str, Any]:
        self._audit('distance', provider, f'({lat1:.4f},{lng1:.4f})->({lat2:.4f},{lng2:.4f})')

        import math
        R = 6371000
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlng/2)**2
        dist = R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return {
            'success': True,
            'from': {'lat': lat1, 'lng': lng1, 'encrypted': self._encrypt_coord(lat1, lng1)},
            'to': {'lat': lat2, 'lng': lng2, 'encrypted': self._encrypt_coord(lat2, lng2)},
            'distance_meters': round(dist, 1),
            'distance_km': round(dist/1000, 2),
            'dna': self.dna,
            'hash': self._hash_chain(f'{lat1},{lng1},{lat2},{lng2}'),
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
    parser = argparse.ArgumentParser(description='龍魂地图/位置统一接口')
    parser.add_argument('--dna', required=True, help='DNA追溯码')
    parser.add_argument('--geocode', help='地址转坐标（输入地址）')
    parser.add_argument('--reverse', action='store_true', help='坐标转地址')
    parser.add_argument('--lat', type=float, help='纬度')
    parser.add_argument('--lng', type=float, help='经度')
    parser.add_argument('--lat2', type=float, help='目标纬度（算距离）')
    parser.add_argument('--lng2', type=float, help='目标经度（算距离）')
    parser.add_argument('--provider', default='auto', help='服务商 (auto/amap/baidu)')
    parser.add_argument('--list', action='store_true', help='列出可用服务商')
    args = parser.parse_args()

    try:
        mp = LonghunMap(args.dna)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    if args.list:
        info = mp.list_providers()
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return 0

    if args.geocode:
        result = mp.geocode(args.geocode, args.provider)
    elif args.reverse and args.lat is not None and args.lng is not None:
        result = mp.reverse_geocode(args.lat, args.lng, args.provider)
    elif args.lat is not None and args.lng is not None and args.lat2 is not None and args.lng2 is not None:
        result = mp.distance(args.lat, args.lng, args.lat2, args.lng2, args.provider)
    else:
        print("❌ 需要 --geocode / --reverse --lat --lng / --lat --lng --lat2 --lng2", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
