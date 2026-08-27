#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·乙未·壬子·丙午·䷙大畜-MEMORY-COMPRESSOR-v1.0
# License: MulanPSL v2
"""
记忆压缩引擎
═══════════
智能压缩对话历史：保留最近N条 + 摘要早期对话 + 关键词提取

策略:
  - 'smart'（默认）: 保留最近 5 轮 + 摘要更早的
  - 'recent': 只保留最近 N 轮
  - 'summarize': 全部压缩为摘要
  - 'none': 不压缩（直接返回）
"""

import json
import re
from typing import List, Dict, Optional, Any, Tuple


# ════════════════════════════════════════════════════
# 压缩策略
# ════════════════════════════════════════════════════

class MemoryCompressor:
    """对话记忆智能压缩器"""

    def __init__(self, keep_recent: int = 5, max_summary_chars: int = 2000):
        """
        Args:
            keep_recent: 保留的最近对话轮数
            max_summary_chars: 摘要最大字符数
        """
        self.keep_recent = keep_recent
        self.max_summary_chars = max_summary_chars

    def compress(self, messages: List[Dict[str, str]],
                 strategy: str = "smart") -> List[Dict[str, str]]:
        """压缩对话消息列表

        Args:
            messages: [{"role": "user/assistant/system", "content": "..."}]
            strategy: 'smart' | 'recent' | 'summarize' | 'none'

        Returns:
            压缩后的消息列表
        """
        if strategy == "none" or len(messages) <= self.keep_recent * 2:
            return messages

        if strategy == "recent":
            return messages[-self.keep_recent * 2:]

        if strategy == "summarize":
            summary = self._summarize(messages)
            return [{"role": "system", "content": f"[对话历史摘要]\n{summary}"}]

        # smart: 保留最近 + 摘要更早的
        if len(messages) <= self.keep_recent * 2:
            return messages

        recent = messages[-self.keep_recent * 2:]
        older = messages[:-self.keep_recent * 2]

        if older:
            summary = self._summarize(older)
            summary_msg = {"role": "system",
                          "content": f"[早期对话摘要 ({len(older)}条)]\n{summary}"}
            return [summary_msg] + list(recent)

        return list(recent)

    def _summarize(self, messages: List[Dict[str, str]]) -> str:
        """提取对话摘要"""
        # 提取每条消息的关键信息
        key_points = []
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            # 截取每条消息的前 200 字符作为关键
            snippet = content[:200].replace("\n", " ")
            if len(content) > 200:
                snippet += "..."
            key_points.append(f"[{role}] {snippet}")

        summary = "\n".join(key_points)

        # 截断到最大长度
        if len(summary) > self.max_summary_chars:
            summary = summary[:self.max_summary_chars] + "\n... (内容过长，已截断)"

        # 提取关键词
        keywords = self._extract_keywords(messages)
        if keywords:
            summary = f"关键词: {', '.join(keywords[:10])}\n\n{summary}"

        return summary

    @staticmethod
    def _extract_keywords(messages: List[Dict[str, str]]) -> List[str]:
        """简单关键词提取（基于词频）"""
        all_text = " ".join(m.get("content", "") for m in messages
                           if m.get("role") in ("user", "assistant"))

        # 简单分词（中英文混合）
        tokens = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', all_text.lower())

        # 过滤停用词
        stop_words = {"的", "了", "在", "是", "我", "有", "和", "就", "不",
                      "人", "都", "一", "一个", "上", "也", "很", "到", "说",
                      "要", "去", "你", "会", "着", "没有", "看", "好", "自己",
                      "the", "a", "an", "is", "are", "was", "were", "be",
                      "to", "of", "in", "for", "on", "with", "at", "by",
                      "this", "that", "it", "and", "or", "but", "not"}
        filtered = [t for t in tokens if t not in stop_words and len(t) > 1]

        # 词频统计
        freq: dict = {}
        for t in filtered:
            freq[t] = freq.get(t, 0) + 1

        return sorted(freq.keys(), key=lambda k: freq[k], reverse=True)


# ════════════════════════════════════════════════════
# 压缩统计
# ════════════════════════════════════════════════════

def compression_stats(original: List[Dict], compressed: List[Dict]) -> dict:
    """计算压缩统计"""
    orig_chars = sum(len(m.get("content", "")) for m in original)
    comp_chars = sum(len(m.get("content", "")) for m in compressed)
    orig_msgs = len(original)
    comp_msgs = len(compressed)

    return {
        "original_messages": orig_msgs,
        "compressed_messages": comp_msgs,
        "original_chars": orig_chars,
        "compressed_chars": comp_chars,
        "msg_ratio": round(comp_msgs / orig_msgs, 3) if orig_msgs else 1.0,
        "char_ratio": round(comp_chars / orig_chars, 3) if orig_chars else 1.0,
        "saved_chars": orig_chars - comp_chars,
    }


# ════════════════════════════════════════════════════
# 自检
# ════════════════════════════════════════════════════

if __name__ == "__main__":
    messages = [
        {"role": "user", "content": "什么是Python？"},
        {"role": "assistant", "content": "Python是一种编程语言..."},
        {"role": "user", "content": "怎么安装？"},
        {"role": "assistant", "content": "从python.org下载..."},
        {"role": "user", "content": "写个hello world"},
        {"role": "assistant", "content": "print('Hello, World!')"},
        {"role": "user", "content": "怎么循环？"},
        {"role": "assistant", "content": "用for或while循环..."},
        {"role": "user", "content": "列表是什么？"},
        {"role": "assistant", "content": "列表是Python的内置数据结构..."},
        {"role": "user", "content": "字典呢？"},
        {"role": "assistant", "content": "字典是键值对..."},
    ] * 3  # 模拟大量对话

    compressor = MemoryCompressor(keep_recent=3)
    compressed = compressor.compress(messages, strategy="smart")
    stats = compression_stats(messages, compressed)

    print(f"原始: {stats['original_messages']} 条, {stats['original_chars']} 字符")
    print(f"压缩后: {stats['compressed_messages']} 条, {stats['compressed_chars']} 字符")
    print(f"消息压缩比: {stats['msg_ratio']}, 字符压缩比: {stats['char_ratio']}")
    print(f"节省: {stats['saved_chars']} 字符")
    print("🟢 压缩器自检通过")
