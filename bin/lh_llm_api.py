#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍魂大模型统一接口 · 国产模型路由
# DNA: #龍芯⚡️丙午·辛未·LLM-ROUTER-v1.0

import os
import sys
import json
import hashlib
import argparse
import sqlite3
from datetime import datetime
from typing import Optional, Dict, Any

try:
    import requests
except ImportError:
    print("[龍魂LLM] ⚠️ 缺少 requests 库，请执行: pip3 install requests")
    sys.exit(1)


class LonghunLLM:
    """龍魂大模型统一接口"""

    MODELS = {
        'deepseek': {
            'name': 'DeepSeek-V3',
            'base_url': 'https://api.deepseek.com/v1',
            'env_key': 'DEEPSEEK_API_KEY',
            'priority': 1,
        },
        'kimi': {
            'name': 'Kimi K2.6',
            'base_url': 'https://api.moonshot.cn/v1',
            'env_key': 'KIMI_API_KEY',
            'priority': 2,
        },
        'qwen': {
            'name': '通义千问',
            'base_url': os.getenv('QWEN_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1'),
            'env_key': 'QWEN_API_KEY',
            'priority': 3,
        },
        'wenxin': {
            'name': '文心一言',
            'base_url': 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions',
            'env_key': 'WENXIN_API_KEY',
            'priority': 4,
        },
    }

    MODEL_IDS = {
        'deepseek': 'deepseek-chat',
        'kimi': 'moonshot-v1-8k',
        'qwen': 'qwen-plus',
        'wenxin': 'ernie-bot-4',
    }

    def __init__(self, dna: str, preferred: str = 'deepseek', audit_db: str = 'data/sqlite/audit.db'):
        self.dna = dna
        self.preferred = preferred
        self.audit_db = audit_db
        self.audit_log = []

        if not self._validate_dna(dna):
            raise ValueError("DNA格式无效，必须是 #龍芯⚡️... 格式")

    def _validate_dna(self, dna: str) -> bool:
        return dna.startswith('#龍芯⚡️') and len(dna) > 20

    def _hash_chain(self, content: str) -> str:
        return hashlib.sha256(f"{self.dna}:{content}".encode()).hexdigest()[:16]

    def _lunar_timestamp(self) -> str:
        return datetime.now().strftime('丙午·%m月%d日·%H:%M')

    def _audit(self, action: str, model: str, content: str):
        entry = {
            'dna': self.dna,
            'action': action,
            'model': model,
            'hash': self._hash_chain(content),
            'timestamp': self._lunar_timestamp(),
        }
        self.audit_log.append(entry)
        self._write_audit(entry)

    def _write_audit(self, entry: Dict[str, Any]):
        try:
            os.makedirs(os.path.dirname(self.audit_db), exist_ok=True)
            conn = sqlite3.connect(self.audit_db)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS llm_audit
                         (dna TEXT, action TEXT, model TEXT, hash TEXT, timestamp TEXT)''')
            c.execute('INSERT INTO llm_audit VALUES (?,?,?,?,?)',
                      (entry['dna'], entry['action'], entry['model'], entry['hash'], entry['timestamp']))
            conn.commit()
            conn.close()
        except Exception:
            pass

    def _resolve_model(self) -> tuple[Any, ...]:
        """解析可用模型，自动降级"""
        model_config = self.MODELS.get(self.preferred, self.MODELS['deepseek'])
        api_key = os.getenv(model_config['env_key'])

        if not api_key:
            for name, config in sorted(self.MODELS.items(), key=lambda x: x[1]['priority']):
                key = os.getenv(config['env_key'])
                if key:
                    model_config = config
                    self.preferred = name
                    api_key = key
                    print(f"[龍魂LLM] 降级到 {config['name']}")
                    break

        if not api_key:
            return None, None, None
        return model_config, api_key, self.MODEL_IDS.get(self.preferred, 'deepseek-chat')

    def chat(self, prompt: str, system: str = "你是龍魂系统助手") -> Dict[str, Any]:
        model_config, api_key, model_id = self._resolve_model()
        if not model_config:
            return {
                'success': False,
                'error': '没有可用的API密钥。请设置环境变量: DEEPSEEK_API_KEY / KIMI_API_KEY / QWEN_API_KEY / WENXIN_API_KEY',
                'dna': self.dna,
            }

        self._audit('chat', model_config['name'], prompt[:100])

        # HTTP头仅允许ASCII，DNA含中文需做安全映射
        dna_ascii = self._hash_chain(self.dna)
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-Longhun-DNA-Hash': dna_ascii,
            'X-Hash-Chain': self._hash_chain(prompt),
        }

        payload = {
            'model': model_id,
            'messages': [
                {'role': 'system', 'content': system},
                {'role': 'user', 'content': prompt},
            ],
            'temperature': 0.7,
            'max_tokens': 4096,
        }

        try:
            resp = requests.post(
                f"{model_config['base_url']}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30,
            )
            result = resp.json()

            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            self._audit('response', model_config['name'], content[:100])

            return {
                'success': True,
                'model': model_config['name'],
                'content': content,
                'dna': self.dna,
                'hash': self._hash_chain(content),
                'audit_id': len(self.audit_log),
            }

        except requests.exceptions.Timeout:
            self._audit('error', model_config['name'], 'timeout')
            return {'success': False, 'error': '请求超时', 'dna': self.dna}
        except Exception as e:
            self._audit('error', model_config['name'], str(e))
            return {'success': False, 'error': str(e), 'dna': self.dna}

    def list_models(self) -> Dict[str, Any]:
        models = []
        for key, cfg in sorted(self.MODELS.items(), key=lambda x: x[1]['priority']):
            available = bool(os.getenv(cfg['env_key']))
            models.append({
                'id': key,
                'name': cfg['name'],
                'priority': cfg['priority'],
                'available': available,
                'active': key == self.preferred,
            })
        return {'models': models, 'dna': self.dna}


def main():
    parser = argparse.ArgumentParser(description='龍魂大模型统一接口')
    parser.add_argument('--dna', required=True, help='DNA追溯码')
    parser.add_argument('--prompt', help='输入提示')
    parser.add_argument('--model', default='deepseek', help='首选模型 (deepseek/kimi/qwen/wenxin)')
    parser.add_argument('--system', default='你是龍魂系统助手', help='系统提示')
    parser.add_argument('--list', action='store_true', help='列出可用模型')
    parser.add_argument('--raw', action='store_true', help='仅输出模型回复内容')
    args = parser.parse_args()

    try:
        llm = LonghunLLM(args.dna, args.model)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    if args.list:
        info = llm.list_models()
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return 0

    if not args.prompt:
        print("❌ 需要 --prompt 参数", file=sys.stderr)
        return 1

    result = llm.chat(args.prompt, args.system)

    if args.raw:
        if result['success']:
            print(result['content'])
        else:
            print(f"❌ {result['error']}", file=sys.stderr)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
