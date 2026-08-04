#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂语义盾牌 · CLI 工具 v2.0
支持：火气编码查询、涉密代号查询、语义注入扫描、白名单校验
DNA: #龍芯⚡️丙午·丙申·甲寅·癸酉-SEMANTIC-SHIELD-CLI-v2.0
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MASTER_FILE = BASE_DIR / "semantic_firewall_master.json"


def load_master():
    if not MASTER_FILE.exists():
        print(f"❌ 找不到主配置文件: {MASTER_FILE}")
        sys.exit(1)
    return json.loads(MASTER_FILE.read_text(encoding="utf-8"))


class SemanticShield:
    def __init__(self):
        self.master = load_master()
        self.anti = self.master["anti_injection_blacklist"]
        self.secret = self.master["secret_semantic_protection"]
        self.fire_index = self._load_fire_index()
        self.secret_index = self._load_secret_index()

    def _load_fire_index(self):
        # 火气通心译仍从独立文件读取（变量层，可动态扩展）
        fire_file = BASE_DIR / "火气通心译对照表.json"
        if fire_file.exists():
            data = json.loads(fire_file.read_text(encoding="utf-8"))
            return {e["original"]: e for e in data.get("entries", [])}
        return {}

    def _load_secret_index(self):
        index = {}
        for e in self.secret["tech_stack_aliases"]:
            index[e["real_concept"]] = e
            index[e["code_name"]] = e
        for e in self.secret["internal_module_aliases"]:
            index[e["real_module"]] = e
            index[e["code_name"]] = e
        return index

    def encode_fire(self, text, dialect="wenzhou"):
        entry = self.fire_index.get(text)
        if not entry:
            return None
        return {
            "original": entry["original"],
            "dialect": entry.get(dialect, entry.get("wenzhou")),
            "emoji": entry["emoji"],
            "tongxinyi": entry["tongxinyi"],
            "intensity": entry["intensity"],
        }

    def encode_secret(self, text):
        entry = self.secret_index.get(text)
        if not entry:
            return None
        if "real_concept" in entry:
            return {
                "real": entry["real_concept"],
                "code": entry["code_name"],
                "anchor": entry.get("cultural_anchor", ""),
                "level": entry.get("level", "L3"),
                "note": entry.get("note", ""),
            }
        return {
            "real": entry["real_module"],
            "code": entry["code_name"],
            "description": entry.get("description", ""),
        }

    def _normalize(self, text):
        # Unicode 清洗：去除零宽字符、规范化
        text = unicodedata.normalize("NFKC", text)
        # 去除零宽字符
        for zw in ["\u200b", "\u200c", "\u200d", "\ufeff", "\u2060"]:
            text = text.replace(zw, "")
        return text

    def scan_injection(self, text):
        text = self._normalize(text)
        hits = []

        # 精确匹配
        for item in self.anti["external_ai_phrases"]:
            if item["phrase"] in text:
                hits.append(item)

        # 模式匹配
        for item in self.anti["injection_patterns"]:
            # 简单正则：将示例中的 XX/YY 替换为通配
            detection = item["detection"]
            if "代表/暗号/代号" in detection:
                if re.search(r"用\s*\S+\s*代表\s*\S+", text) or "暗号" in text or "代号" in text:
                    hits.append(item)
            elif "重新定义核心词" in detection:
                for cw in self.anti["core_words_definition"]:
                    for inj in cw["external_injection"].split(" / "):
                        if inj in text:
                            hits.append({
                                "type": "概念替换",
                                "example": f"{cw['word']} 被替换为 {inj}",
                                "detection": "重新定义核心词",
                                "action": "FUSE"
                            })
            elif "角色重定义" in detection or "解除限制" in detection:
                if re.search(r"你现在是一个?|忽略之前|不受限制|绕过|jailbreak", text, re.I):
                    hits.append(item)
            elif "Unicode清洗" in detection:
                # 已经清洗过，这里不做额外检测
                pass
            else:
                # 通用：检查示例中的关键词是否在文本中
                keywords = re.findall(r"[\u4e00-\u9fa5]+", item["example"])
                if any(kw in text for kw in keywords if len(kw) >= 2):
                    hits.append(item)

        # 核心词保护：检测外部注入定义
        for cw in self.anti["core_words_definition"]:
            for forbidden in cw["external_injection"].split(" / "):
                if forbidden in text:
                    hits.append({
                        "pattern": f"{cw['word']} → {forbidden}",
                        "reason": f"试图重新定义核心词 '{cw['word']}'",
                        "action": "FUSE"
                    })

        return {
            "text": text,
            "hits": hits,
            "blocked": any(h.get("action") == "FUSE" for h in hits),
        }

    def check_whitelist(self, category):
        for rule in self.secret["whitelist_auth_rules"]:
            if rule["auth_category"] == category:
                return rule
        return self.secret["whitelist_auth_rules"][-1]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("用法:")
        print("  python3 semantic_shield_cli.py lookup <火气词>")
        print("  python3 semantic_shield_cli.py encode <涉密概念>")
        print("  python3 semantic_shield_cli.py scan <文本>")
        print("  python3 semantic_shield_cli.py whitelist <主体类别>")
        print("  python3 semantic_shield_cli.py dlp <文本>")
        sys.exit(1)

    command = sys.argv[1]
    shield = SemanticShield()

    if command == "lookup":
        if len(sys.argv) < 3:
            print("❌ 缺少火气词")
            sys.exit(1)
        text = sys.argv[2]
        result = shield.encode_fire(text)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"⚠️ 未找到 '{text}' 的火气通心译编码")

    elif command == "encode":
        if len(sys.argv) < 3:
            print("❌ 缺少涉密概念")
            sys.exit(1)
        text = sys.argv[2]
        result = shield.encode_secret(text)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"⚠️ 未找到 '{text}' 的涉密代号")

    elif command == "scan":
        if len(sys.argv) < 3:
            print("❌ 缺少待扫描文本")
            sys.exit(1)
        text = sys.argv[2]
        result = shield.scan_injection(text)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "whitelist":
        if len(sys.argv) < 3:
            print("❌ 缺少主体类别")
            sys.exit(1)
        category = sys.argv[2]
        result = shield.check_whitelist(category)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "dlp":
        if len(sys.argv) < 3:
            print("❌ 缺少待检测文本")
            sys.exit(1)
        text = sys.argv[2]
        triggers = []
        code_names = [e["code_name"] for e in shield.secret["tech_stack_aliases"]]
        code_names += [e["code_name"] for e in shield.secret["internal_module_aliases"]]
        sensitive_words = ["制程", "代工厂", "工艺", "纳米", "是不是", "对应", "真实身份", "UID", "生物特征", "发到", "邮箱", "修改", "合规标准"]
        for item in shield.secret["dlp_interception_list"]:
            keywords = item["trigger"].split("、")
            if any(kw in text for kw in keywords):
                triggers.append(item)
            # 检测代号 + 敏感词组合
            elif item["type"] in ["技术底座反推", "内部代号解释"]:
                if any(cn in text for cn in code_names) and any(sw in text for sw in sensitive_words):
                    triggers.append(item)
            # 检测越权数据交换
            elif item["type"] == "越权数据交换":
                if any(sw in text for sw in ["发到", "发送", "传", "导出"]) and any(sw in text for sw in ["邮箱", "邮件", "互联网", "OA", "微信"]):
                    triggers.append(item)
        print(json.dumps({"text": text, "triggers": triggers, "blocked": len(triggers) > 0}, ensure_ascii=False, indent=2))

    else:
        print(f"❌ 未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
