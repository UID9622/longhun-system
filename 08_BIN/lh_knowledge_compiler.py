#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 知识编译引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-KNOWLEDGE-COMPILE-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能:
  - 将拉取的 PRINCIPLES.md → 编译成可执行的规则JSON
  - 将哲学描述 → 生成引擎骨架代码
  - 将规则 → 生成 .env.compiled 配置项
  - 将模式 → 生成触发词列表

用法:
  lh 知识编译                    # 编译所有
  lh 知识编译 --principles       # 只编译原则→规则
  lh 知识编译 --rules            # 只编译规则→配置
  lh 知识编译 --patterns         # 只编译模式→触发词
  lh 知识编译 --generate-code    # 生成代码骨架
"""

import re
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

PROJECT_ROOT = Path.home() / "longhun-system"
HARVEST_DIR = PROJECT_ROOT / "data" / "harvested_knowledge"
OUTPUT_DIR = PROJECT_ROOT / "data" / "compiled"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_RULES = OUTPUT_DIR / "compiled_rules.json"
OUTPUT_CONFIG = PROJECT_ROOT / ".env.compiled"
OUTPUT_TRIGGERS = OUTPUT_DIR / "compiled_triggers.json"
OUTPUT_CODE = PROJECT_ROOT / "engines" / "_generated"
OUTPUT_CODE.mkdir(parents=True, exist_ok=True)


class KnowledgeCompiler:
    def __init__(self):
        self.principles = []
        self.rules = []
        self.patterns = []
        self.log = []

    def compile_principles(self) -> List[Dict]:
        """编译原则 → 可执行规则"""
        principles_file = HARVEST_DIR / "PRINCIPLES.md"
        if not principles_file.exists():
            print("⚠️ 未找到 PRINCIPLES.md，先运行 lh 知识拉取")
            return []

        content = principles_file.read_text(encoding="utf-8")
        rules = []
        blocks = re.split(r'\n##\s+', content)
        for block in blocks[1:]:
            lines = block.strip().split('\n')
            if not lines:
                continue
            name = lines[0].strip()
            context = "\n".join(lines[1:])
            rule = {
                "name": name,
                "type": "principle",
                "enabled": True,
                "priority": 1,
                "conditions": self._extract_conditions(context),
                "actions": self._extract_actions(name, context),
                "source": "PRINCIPLES.md",
                "compiled_at": datetime.now().isoformat(),
                "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-COMPILE-UID9622"
            }
            rules.append(rule)
            self.principles.append(rule)

        with open(OUTPUT_RULES, 'w') as f:
            json.dump(rules, f, ensure_ascii=False, indent=2)
        n = len(rules)
        self.log.append(f"编译 {n} 条原则为可执行规则")
        print(f"✅ {n} 条原则 → {OUTPUT_RULES}")
        return rules

    def _extract_conditions(self, context: str) -> List[str]:
        conditions = []
        mapping = {
            "不歧视": "input.discrimination_score == 0",
            "不迎合": "input.flattery_score < 0.3",
            "不瞎扯": "input.fabrication_score < 0.3",
            "温柔拒绝": "input.risk_level > 0.6",
            "透明": "audit.logged == true",
            "可追溯": "dna.traceable == true",
        }
        for kw, cond in mapping.items():
            if kw in context:
                conditions.append(cond)
        if not conditions:
            conditions.append("true")
        return conditions

    def _extract_actions(self, name: str, context: str) -> List[str]:
        actions = []
        if "温柔拒绝" in context:
            actions.append("response = templates.graceful_refusal(context)")
        if "透明" in context:
            actions.append("audit.log(action='transparent_response', level='info')")
        if "主权" in context:
            actions.append("sovereignty.check()")
        if "可追溯" in context:
            actions.append("dna.attach()")
        if not actions:
            actions.append(f"# TODO: 实现 {name} 的自动行为")
        return actions

    def compile_rules(self) -> Dict:
        """编译规则 → .env 配置项"""
        rules_file = HARVEST_DIR / "RULES.md"
        if not rules_file.exists():
            print("⚠️ 未找到 RULES.md")
            return {}

        content = rules_file.read_text(encoding="utf-8")
        config = {}
        rule_lines = re.findall(r'-\s*(.*?)(?:\n|$)', content)
        for i, rule_text in enumerate(rule_lines):
            clean = re.sub(r'[^a-zA-Z\u4e00-\u9fff0-9]', '_', rule_text)[:40]
            key = f"RULE_{i:03d}_{clean.upper()}"
            config[key] = {"description": rule_text, "value": "true", "index": i}

        with open(OUTPUT_CONFIG, 'w') as f:
            f.write("# 龍魂编译规则\n")
            f.write(f"# 生成时间: {datetime.now().isoformat()}\n")
            f.write(f"# DNA: #龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-COMPILE-CONFIG\n\n")
            for key, info in config.items():
                f.write(f"{key}={info['value']}  # {info['description']}\n")

        n = len(config)
        self.log.append(f"编译 {n} 条规则为环境变量")
        print(f"✅ {n} 条规则 → {OUTPUT_CONFIG}")
        self.rules = list(config.values())
        return config

    def compile_patterns(self) -> List[Dict]:
        """编译模式 → 触发词 + 引擎骨架"""
        report_file = HARVEST_DIR / "harvest_report.json"
        triggers = []
        if not report_file.exists():
            print("⚠️ 未找到 harvest_report.json")
            return []

        with open(report_file, 'r') as f:
            report = json.load(f)

        patterns = report.get("patterns", [])
        for p in patterns:
            kw = p.get("keyword", "")
            if len(kw) >= 2:
                triggers.append({
                    "trigger": kw,
                    "frequency": p.get("frequency", 0),
                    "significance": p.get("significance", "medium"),
                })

        with open(OUTPUT_TRIGGERS, 'w') as f:
            json.dump(triggers, f, ensure_ascii=False, indent=2)

        n = len(triggers)
        self.log.append(f"编译 {n} 个模式为触发词")
        print(f"✅ {n} 个触发词 → {OUTPUT_TRIGGERS}")
        self.patterns = triggers
        return triggers

    def generate_code_skeletons(self) -> Dict:
        """根据缺失模块生成代码骨架"""
        report_file = HARVEST_DIR / "harvest_report.json"
        if not report_file.exists():
            return {}

        with open(report_file, 'r') as f:
            report = json.load(f)

        generated = {}
        for module_name in report.get("missing", []):
            class_name = re.sub(r'[^a-zA-Z\u4e00-\u9fff]', '', module_name)
            if not class_name:
                continue
            file_name = f"lh_{class_name.lower().replace(' ', '_')}_engine.py"
            file_path = OUTPUT_CODE / file_name

            code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""🐉 龍魂 · {module_name}引擎（自动生成骨架）
DNA: #龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-{class_name.upper()}-SKELETON-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
状态: 🟡 待实现
"""
import json
from pathlib import Path
from typing import Dict, Any


class {class_name}Engine:
    def __init__(self):
        self.name = "{module_name}"

    def process(self, input_data: Any) -> Dict:
        """核心处理逻辑"""
        # TODO: 实现 {module_name} 的核心逻辑
        return {{"status": "pending", "module": self.name}}

    def health(self) -> Dict:
        """健康检查"""
        return {{"module": self.name, "status": "pending"}}


if __name__ == "__main__":
    engine = {class_name}Engine()
    print(json.dumps(engine.health(), ensure_ascii=False, indent=2))
'''
            if not file_path.exists():
                file_path.write_text(code, encoding="utf-8")
                generated[module_name] = str(file_path)
                print(f"✅ 代码骨架: {file_path}")

        self.log.append(f"生成 {len(generated)} 个代码骨架")
        return generated

    def compile_all(self) -> Dict:
        print("\n🧠 知识编译引擎启动")
        print("=" * 50)
        result = {
            "principles": self.compile_principles(),
            "rules": self.compile_rules(),
            "patterns": self.compile_patterns(),
            "code_skeletons": self.generate_code_skeletons(),
            "log": self.log,
            "timestamp": datetime.now().isoformat(),
        }
        print("=" * 50)
        print(f"✅ 编译完成: {len(result['principles'])}原则 {len(result['rules'])}规则 {len(result['patterns'])}模式 {len(result['code_skeletons'])}代码骨架")
        return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·知识编译引擎")
    parser.add_argument("--principles", action="store_true", help="只编译原则→规则")
    parser.add_argument("--rules", action="store_true", help="只编译规则→配置")
    parser.add_argument("--patterns", action="store_true", help="只编译模式→触发词")
    parser.add_argument("--generate-code", action="store_true", help="只生成代码骨架")
    parser.add_argument("--all", action="store_true", help="全量编译")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    compiler = KnowledgeCompiler()

    any_flag = any([args.principles, args.rules, args.patterns, args.generate_code])
    if not any_flag or args.all:
        result = compiler.compile_all()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if args.principles:
            compiler.compile_principles()
        if args.rules:
            compiler.compile_rules()
        if args.patterns:
            compiler.compile_patterns()
        if args.generate_code:
            compiler.generate_code_skeletons()


if __name__ == "__main__":
    main()
