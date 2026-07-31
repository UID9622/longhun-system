# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek-V3 工具调用 + 龙魂审计集成
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-DeepSeek-tools-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List
from deepseek_api import DeepSeekClient


class DeepSeekAudited:
    """带龙魂审计的DeepSeek调用"""

    def __init__(self, client: DeepSeekClient = None):
        self.client = client or DeepSeekClient()
        self.audit_log = []

    def _generate_dna(self, content: str) -> str:
        """生成DNA签章"""
        hash_val = hashlib.sha256(content.encode()).hexdigest()[:8]
        return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-DeepSeek-{hash_val}"

    def _audit(self, action: str, input_data: Any, output_data: Any):
        """审计记录"""
        self.audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "input": str(input_data)[:500],
            "output": str(output_data)[:500],
            "dna": self._generate_dna(str(output_data))
        })

    def query_with_audit(
        self,
        prompt: str,
        system_prompt: str = "你是龙魂系统助手，回答直接真实。",
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """带审计的查询"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        try:
            response = self.client.chat(messages, temperature, max_tokens)
            content = response['choices'][0]['message']['content']

            self._audit("query", prompt, content)

            return {
                "content": content,
                "dna": self._generate_dna(content),
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
        except Exception as e:
            self._audit("query_error", prompt, str(e))
            return {
                "content": None,
                "error": str(e),
                "status": "error"
            }

    def stream_with_audit(
        self,
        prompt: str,
        system_prompt: str = "你是龙魂系统助手，回答直接真实。"
    ):
        """流式查询（带审计）"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        full_content = []
        for chunk in self.client.chat_stream(messages):
            full_content.append(chunk)
            yield chunk

        content = "".join(full_content)
        self._audit("stream", prompt, content)

    def get_audit_log(self) -> List[Dict]:
        """获取审计日志"""
        return self.audit_log


# ---------- 使用示例 ----------
if __name__ == "__main__":
    # 带审计的查询
    audited = DeepSeekAudited()
    result = audited.query_with_audit("DeepSeek-V3的MoE架构有什么优势？")
    print(f"回答: {result['content']}")
    print(f"DNA: {result['dna']}")

    # 查看审计日志
    print(f"\n审计日志: {len(audited.get_audit_log())} 条")
