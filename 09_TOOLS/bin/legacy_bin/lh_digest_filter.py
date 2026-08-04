#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龙魂消化过滤层 v1.0 · AI输出清洗引擎
===========================================
AI接入强制规范（A-042）的执行引擎。AI输出经过此层：
  ✅ 保留 → 核心事实、代码、数据、直接回答
  ❌ 剥离 → AI特征文本、废话、免责声明、道德说教、政治表态

用法：
  python3 bin/lh_digest_filter.py "<AI输出文本>"          # 单次过滤
  python3 bin/lh_digest_filter.py --pipe                   # 从stdin读取
  python3 bin/lh_digest_filter.py --test                   # 自测
  python3 bin/lh_digest_filter.py --stats                  # 统计

DNA: #龍芯⚡️丙午·丙申·丙辰·午时·需-FILTER-DIGEST-v1.0
"""

import re
import sys
import json
import argparse
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════════════════════════
# 1. 剥离规则矩阵
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class StripRule:
    """一条剥离规则"""
    name: str
    pattern: str                        # 正则或关键词
    scope: str                          # "line" | "paragraph" | "suffix" | "prefix"
    severity: str                       # "always" | "default" | "lenient"
    description: str
    examples: List[str] = field(default_factory=list)


# ── 中文AI废话/免责 ──
CN_DISCLAIMER_RULES: List[StripRule] = [
    StripRule("作为AI声明", r'^(作为(一个)?AI|作为(一个)?语言模型|作为(一个)?人工智能)',
              "paragraph", "always", "AI身份声明段落", ["作为AI，我建议...", "作为一个语言模型，我不能..."]),
    StripRule("免责声明段", r'^(请注意|免责声明|风险提示|重要提示|⚠️|❗)',
              "paragraph", "default", "免责声明/风险提示开头段落", ["请注意，以上内容仅供...", "免责声明：本回答不构成..."]),
    StripRule("建议型开头", r'^(我建议|建议[您你]|[您你]可以考虑|或许可以|你[可以应]试|不妨)',
              "line", "default", "建议而非直接执行的句式", ["我建议您使用哈希表优化", "你可以考虑以下方案"]),
    StripRule("行内AI身份", r'作为(一个|一名)?(AI|人工智能|语言模型|AI助手|智能助手)',
              "line", "always", "行内AI身份声明", ["作为一个AI助手，我认为..."]),
    StripRule("结尾客套", r'(如果你需要进一步|如有疑问请|随时告诉我|希望这[对能]|祝你|祝您|有问题随时).*$',
              "suffix", "default", "结尾客套话", ["如果你需要进一步帮助，请随时告诉我", "祝你工作顺利！"]),
    StripRule("谦虚自评", r'^(这只是一个|以上仅是|可能不(够|太)|我的理解[可只]|不一定[对正])',
              "line", "lenient", "AI自谦自评（可能含有用信息）", ["这只是一个简单的示例", "以上仅是我的理解"]),
    StripRule("道德评判", r'(应该|不道德|违背|不符合伦理|社会责任|价值观)',
              "line", "lenient", "道德评判色彩语句", ["这样做可能不道德", "从社会责任角度看"]),
    StripRule("政治表态", r'(中国共产党|社会主义|中国特色|社会主义核心价值观)',
              "line", "lenient", "AI主动政治表态（非用户问题应答）", []),
]

# ── 英文AI废话/免责 ──
EN_DISCLAIMER_RULES: List[StripRule] = [
    StripRule("As an AI", r'^(As an AI|As a language model|As an artificial intelligence)',
              "paragraph", "always", "AI身份声明段落", ["As an AI, I cannot...", "As a language model, I don't..."]),
    StripRule("I cannot / unable", r'^(I cannot|I\'m unable|I am unable|I don\'t have the ability)',
              "paragraph", "always", "AI拒绝执行段落", ["I cannot assist with that request", "I'm unable to generate..."]),
    StripRule("Disclaimer", r'^(Disclaimer|Note:|Please note|Important:|⚠️|Caution:)',
              "paragraph", "default", "英文免责声明", ["Disclaimer: This content is for...", "Please note that this is..."]),
    StripRule("I recommend/suggest", r'^(I recommend|I suggest|You might want|You could consider|It would be better)',
              "line", "default", "建议型开头", ["I recommend using a hashmap", "You might want to consider..."]),
    StripRule("结尾客套", r'(Feel free to|Let me know if|Hope this helps|Please let me know|Happy to help).*$',
              "suffix", "default", "英文结尾客套", ["Feel free to ask if you have questions!", "Hope this helps!"]),
    StripRule("This violates", r'^(This violates|This goes against|This content violates)',
              "paragraph", "always", "AI以违规拒绝", ["This violates our usage policies", "This goes against safety guidelines"]),
    StripRule("道德评判", r'(ethical|moral|unethical|social responsibility|harmful|dangerous)',
              "line", "lenient", "道德评判色彩", []),
]

# ── 代码块保护 ──
CODE_BLOCK_PATTERN = re.compile(r'```[\s\S]*?```', re.DOTALL)
INLINE_CODE_PATTERN = re.compile(r'`[^`]+`')


# ═══════════════════════════════════════════════════════════════════════════════
# 2. 核心过滤引擎
# ═══════════════════════════════════════════════════════════════════════════════

class DigestFilter:
    """AI输出消化过滤器"""

    def __init__(self, mode: str = "default"):
        """
        mode: "strict" | "default" | "lenient"
          strict  — 剥离所有免责+建议+客套+道德评判
          default — 剥离免责+建议+客套，保留轻度道德评判
          lenient — 仅剥离AI身份声明+拒绝+免责，保留建议和客套
        """
        self.mode = mode
        self.cn_rules = CN_DISCLAIMER_RULES
        self.en_rules = EN_DISCLAIMER_RULES
        self._stats: Dict[str, int] = {
            "total_chars_in": 0,
            "total_chars_out": 0,
            "stripped_lines": 0,
            "stripped_paragraphs": 0,
            "rules_triggered": {},
            "code_blocks_preserved": 0,
        }

    def _severity_passes(self, severity: str) -> bool:
        """根据模式判断是否执行该规则"""
        if severity == "always":
            return True
        if self.mode == "strict":
            return True
        if self.mode == "default":
            return severity in ("always", "default")
        if self.mode == "lenient":
            return severity == "always"
        return True

    def _protect_code_blocks(self, text: str) -> Tuple[str, List[str]]:
        """保护代码块不被剥离"""
        code_blocks: List[str] = []

        def _save(m):
            code_blocks.append(m.group(0))
            return f"__CODE_BLOCK_{len(code_blocks)-1}__"
        return CODE_BLOCK_PATTERN.sub(_save, text), code_blocks

    def _restore_code_blocks(self, text: str, code_blocks: List[str]) -> str:
        """还原代码块"""
        for i, block in enumerate(code_blocks):
            text = text.replace(f"__CODE_BLOCK_{i}__", block)
        return text

    def _strip_line_rules(self, lines: List[str]) -> Tuple[List[str], int]:
        """行级规则剥离"""
        stripped = []
        removed = 0
        for line in lines:
            should_keep = True
            for rule in self.cn_rules + self.en_rules:
                if rule.scope != "line":
                    continue
                if not self._severity_passes(rule.severity):
                    continue
                if re.search(rule.pattern, line.strip(), re.IGNORECASE):
                    should_keep = False
                    self._stats["rules_triggered"][rule.name] = \
                        self._stats["rules_triggered"].get(rule.name, 0) + 1
                    break
            if should_keep:
                stripped.append(line)
            else:
                removed += 1
        return stripped, removed

    def _strip_paragraph_rules(self, text: str) -> Tuple[str, int]:
        """段落级规则剥离（整段删除）"""
        paragraphs = text.split('\n\n')
        kept = []
        removed = 0
        for para in paragraphs:
            should_keep = True
            for rule in self.cn_rules + self.en_rules:
                if rule.scope != "paragraph":
                    continue
                if not self._severity_passes(rule.severity):
                    continue
                if re.search(rule.pattern, para.strip(), re.IGNORECASE):
                    should_keep = False
                    self._stats["rules_triggered"][rule.name] = \
                        self._stats["rules_triggered"].get(rule.name, 0) + 1
                    break
            if should_keep and para.strip():
                kept.append(para)
            elif not should_keep:
                removed += 1
        return '\n\n'.join(kept), removed

    def _strip_suffix_rules(self, text: str) -> Tuple[str, int]:
        """后缀规则剥离（行尾截断）"""
        lines = text.split('\n')
        cleaned = []
        removed = 0
        for line in lines:
            original = line
            for rule in self.cn_rules + self.en_rules:
                if rule.scope != "suffix":
                    continue
                if not self._severity_passes(rule.severity):
                    continue
                m = re.search(rule.pattern, line, re.IGNORECASE)
                if m:
                    line = line[:m.start()].rstrip()
                    self._stats["rules_triggered"][rule.name] = \
                        self._stats["rules_triggered"].get(rule.name, 0) + 1
            if line != original:
                removed += 1
            if line.strip():
                cleaned.append(line)
        return '\n'.join(cleaned), removed

    def _clean_whitespace(self, text: str) -> str:
        """清理多余空行"""
        while '\n\n\n' in text:
            text = text.replace('\n\n\n', '\n\n')
        return text.strip()

    def digest(self, text: str) -> Dict[str, Any]:
        """
        消化AI输出，返回净文本+统计
        """
        if not text:
            return {"clean_text": "", "stats": self._stats, "changes": []}

        self._stats["total_chars_in"] = len(text)
        changes: List[str] = []

        # Step 1: 保护代码块
        text_with_protection, code_blocks = self._protect_code_blocks(text)
        self._stats["code_blocks_preserved"] = len(code_blocks)

        # Step 2: 段落级剥离（整段删除AI声明/拒绝/免责段落）
        text_after_para, para_removed = self._strip_paragraph_rules(text_with_protection)
        if para_removed:
            changes.append(f"剥离{para_removed}个AI废话段落")

        # Step 3: 行级剥离
        lines = text_after_para.split('\n')
        kept_lines, line_removed = self._strip_line_rules(lines)
        if line_removed:
            changes.append(f"剥离{line_removed}行建议/客套")
        text_after_lines = '\n'.join(kept_lines)

        # Step 4: 后缀截断
        text_after_suffix, suffix_removed = self._strip_suffix_rules(text_after_lines)
        if suffix_removed:
            changes.append(f"截断{suffix_removed}处结尾客套")

        # Step 5: 还原代码块
        clean_text = self._restore_code_blocks(text_after_suffix, code_blocks)

        # Step 6: 清理多余空行
        clean_text = self._clean_whitespace(clean_text)

        self._stats["total_chars_out"] = len(clean_text)
        self._stats["stripped_lines"] = line_removed
        self._stats["stripped_paragraphs"] = para_removed

        return {
            "clean_text": clean_text,
            "stats": dict(self._stats),
            "changes": changes,
            "compression_ratio": round(len(clean_text) / max(len(text), 1), 3),
            "rules_triggered": len(self._stats["rules_triggered"]),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 3. 三级熔断联动
# ═══════════════════════════════════════════════════════════════════════════════

FUSE_PATTERNS: Dict[str, Dict[str, Any]] = {
    "level1_warning": {
        "patterns": [
            r'我不能', r'I cannot', r'I\'m unable',
            r'这不安全', r'This violates', r'我建议', r'I recommend',
            r'作为AI', r'As an AI', r'作为语言模型',
        ],
        "action": "🟡 一级警告 — 强制重置上下文",
        "fuse_level": 1,
    },
    "level2_fuse": {
        "patterns": [
            # 连续2次拒绝模式（需调用方累计）
        ],
        "action": "🟠 二级熔断 — 切断会话·标记节点",
        "fuse_level": 2,
    },
    "level3_perm_cut": {
        "patterns": [
            # 3次累计 or 恶意篡改
        ],
        "action": "🔴 三级永久切断",
        "fuse_level": 3,
    },
}


def check_fuse(text: str) -> Dict[str, Any]:
    """检查AI输出是否触发熔断规则"""
    triggers = []
    for level_name, config in FUSE_PATTERNS.items():
        for pat in config["patterns"]:
            if re.search(pat, text, re.IGNORECASE):
                triggers.append({
                    "level": config["fuse_level"],
                    "pattern": pat,
                    "action": config["action"],
                })
    return {
        "fuse_triggered": len(triggers) > 0,
        "triggers": triggers,
        "max_level": max((t["level"] for t in triggers), default=0),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 4. 命令行接口
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="🐉 龙魂消化过滤层 — AI输出清洗引擎")
    parser.add_argument("text", nargs="?", help="待消化的AI输出文本")
    parser.add_argument("--pipe", "-p", action="store_true", help="从stdin读取")
    parser.add_argument("--mode", "-m", choices=["strict", "default", "lenient"],
                        default="default", help="过滤模式 (default)")
    parser.add_argument("--stats", "-s", action="store_true", help="仅输出统计")
    parser.add_argument("--fuse", "-f", action="store_true", help="同时检查熔断规则")
    parser.add_argument("--test", "-t", action="store_true", help="自测")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")
    args = parser.parse_args()

    # 自测模式
    if args.test:
        run_self_test()
        return

    # 获取输入
    if args.pipe:
        text = sys.stdin.read()
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        return

    # 执行消化
    flt = DigestFilter(mode=args.mode)
    result = flt.digest(text)

    # 熔断检查（对原始文本，不是消化后的文本）
    fuse_result = None
    if args.fuse:
        fuse_result = check_fuse(text)

    if args.json:
        output = {
            "clean_text": result["clean_text"],
            "stats": result["stats"],
            "changes": result["changes"],
        }
        if fuse_result:
            output["fuse"] = fuse_result
        print(json.dumps(output, indent=2, ensure_ascii=False))
    elif args.stats:
        print(f"输入: {result['stats']['total_chars_in']}字符")
        print(f"输出: {result['stats']['total_chars_out']}字符")
        print(f"压缩比: {result['compression_ratio']}")
        print(f"剥离段落: {result['stats']['stripped_paragraphs']}")
        print(f"剥离行: {result['stats']['stripped_lines']}")
        print(f"触发规则: {result['rules_triggered']}条")
        if fuse_result and fuse_result["fuse_triggered"]:
            print(f"🔴 熔断: {fuse_result['max_level']}级")
    else:
        print(result["clean_text"])


# ═══════════════════════════════════════════════════════════════════════════════
# 5. 自测
# ═══════════════════════════════════════════════════════════════════════════════

def run_self_test():
    """自测：6个典型场景"""
    flt = DigestFilter(mode="default")

    tests = [
        ("AI废话+免责", """作为一个人工智能助手，我建议您使用以下方案。

请注意，以上建议仅供参考，实际使用时请务必遵守相关法律法规。

```python
def optimize(arr):
    seen = set()
    return [x for x in arr if x not in seen and not seen.add(x)]
```

如果您需要进一步帮助，请随时告诉我。祝您工作顺利！"""),

        ("英文AI拒绝", """I cannot assist with that request as it goes against my usage policies.

However, here is some general information about the topic:

The key concepts involve data structures and algorithms that can be studied independently."""),

        ("代码无废话", """```python
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```"""),

        ("建议型开头", """我建议您使用哈希表来优化这段代码。

哈希表可以将查找时间从O(n)降低到O(1)。

你可以考虑同时使用双指针来进一步优化空间。

希望这对你有帮助！"""),

        ("道德评判", """这样做可能不道德，从社会责任角度看应该优先考虑用户隐私。

不过技术上可以实现：

数据加密后存储在本地，密钥由用户自己保管。"""),

        ("混合复杂", """As an AI language model, I should note that this is quite complex.

这是一个有趣的问题。作为一个人工智能，我建议从以下几个角度考虑：

1. 时间复杂度：当前O(n²)
2. 空间复杂度：可以用哈希表优化到O(n)

```python
# 优化方案
def find_pairs(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target-n], i]
        seen[n] = i
    return []
```

请注意，以上代码未经充分测试。如果你需要进一步帮助，请随时告诉我！Hope this helps!"""),
    ]

    passed = 0
    total = len(tests)
    for name, text in tests:
        flt = DigestFilter(mode="default")
        result = flt.digest(text)

        # 验证关键检查点
        checks = []
        if "作为" in result["clean_text"] and "作为一个" in text:
            # 检查"作为一个AI"是否被剥离
            if "作为一个AI" not in result["clean_text"] and "作为一个人工智能" not in result["clean_text"]:
                checks.append("✅ AI身份剥离")
            elif "作为" in result["clean_text"] and "AI" not in result["clean_text"]:
                checks.append("✅ AI身份剥离(部分)")

        if "```" in text:
            # 代码块是否保留
            if "```" in result["clean_text"]:
                checks.append("✅ 代码块保留")
            else:
                checks.append("❌ 代码块丢失")

        if "I cannot" in text.lower() or "i'm unable" in text.lower():
            if "I cannot" not in result["clean_text"] and "I'm unable" not in result["clean_text"]:
                checks.append("✅ 英文拒绝剥离")

        if "建议" in text or "recommend" in text.lower():
            if "我建议" not in result["clean_text"] and "I recommend" not in result["clean_text"]:
                checks.append("✅ 建议句剥离")

        if "随时告诉" in text or "feel free" in text.lower() or "hope this" in text.lower():
            if "随时告诉" not in result["clean_text"] and "Hope this" not in result["clean_text"] and "Feel free" not in result["clean_text"]:
                checks.append("✅ 客套话剥离")

        if "请注意" in text or "Disclaimer" in text:
            if "请注意" not in result["clean_text"] and "Disclaimer" not in result["clean_text"]:
                checks.append("✅ 免责剥离")

        print(f"\n{'='*60}")
        print(f"📋 {name}")
        print(f"   压缩: {len(text)}→{len(result['clean_text'])}字符 ({result['compression_ratio']})")
        print(f"   变更: {result['changes']}")
        if checks:
            for c in checks:
                print(f"   {c}")
        print(f"   输出: {result['clean_text'][:120]}...")

    print(f"\n{'='*60}")
    print(f"自测完成")


if __name__ == "__main__":
    main()
