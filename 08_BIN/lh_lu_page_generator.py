#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · LU 系统页面生成器 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-LU-PAGE-v1.0-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

功能：
  1. 生成五种人格模板页面（基础/宝宝/Worker/推演/决策）
  2. 交互式引导用户填写关键字段
  3. 自动校验规则（禁止长推理/空目标/层级匹配）
  4. 输出 Markdown 格式页面
  5. 支持保存到 pages/ 目录

用法：
  python3 bin/lh_lu_page_generator.py                    # 交互式生成
  python3 bin/lh_lu_page_generator.py --type 宝宝        # 指定模板类型
  python3 bin/lh_lu_page_generator.py --json             # 输出JSON格式
  python3 bin/lh_lu_page_generator.py --save page.md     # 保存到文件
  python3 bin/lh_lu_page_generator.py --non-interactive  # 使用默认值快速生成

集成到 lh:
  lh lu-page                                            # 交互式
  lh lu-page --type 推演 --save 推演_20260802.md
"""

import os
import sys
import json
import datetime
import argparse
import hashlib
import textwrap
from pathlib import Path
from typing import Dict, Optional, List, Any

# ============================================================
# 固定锚点
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
GPG_SHORT = "8CC26D5F"
PROJECT_ROOT = Path.home() / "longhun-system"
PAGE_OUTPUT_DIR = PROJECT_ROOT / "pages"
PAGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 五套模板定义（全字段、全校验、全人格对齐）
# ============================================================

TEMPLATES: Dict[str, dict] = {
    "基础": {
        "display_name": "基础模板（通用创作/记录）",
        "sections": [
            {"id": "meta", "label": "0️⃣ 页面元信息", "fields": [
                {"id": "page_type", "label": "页面类型", "type": "select",
                 "options": ["创作", "推演", "决策", "设计", "记录"], "default": "创作"},
                {"id": "persona", "label": "当前人格（主算）", "type": "text", "default": "宝宝"},
                {"id": "deep_reason", "label": "是否需要深度推理", "type": "select",
                 "options": ["否", "是", "延迟"], "default": "否"},
                {"id": "task_level", "label": "任务层级", "type": "select",
                 "options": ["工人层", "地层", "天层"], "default": "工人层"},
                {"id": "path_id", "label": "使用路径ID", "type": "text", "default": ""}
            ]},
            {"id": "goal", "label": "1️⃣ 一句话目标（强制）", "fields": [
                {"id": "goal_text", "label": "目标", "type": "textarea", "default": "", "max_lines": 2,
                 "required": True}
            ]},
            {"id": "entry", "label": "2️⃣ 任务入口判断（算力止损点）", "fields": [
                {"id": "repeat", "label": "是否重复问题", "type": "select",
                 "options": ["是", "否", "不确定"], "default": "否"},
                {"id": "high_risk", "label": "是否高风险（法律/隐私/金融/安全）", "type": "select",
                 "options": ["否", "法律", "隐私", "金融", "安全"], "default": "否"},
                {"id": "value_conflict", "label": "是否存在价值冲突", "type": "select",
                 "options": ["是", "否"], "default": "否"},
                {"id": "creative", "label": "是否需要创造性输出", "type": "select",
                 "options": ["是", "否"], "default": "否"}
            ]},
            {"id": "materials", "label": "3️⃣ 可用素材 / 已知条件（不推理）", "fields": [
                {"id": "existing_conclusions", "label": "已有结论", "type": "textarea", "default": "", "max_lines": 3},
                {"id": "existing_rules", "label": "已有规则", "type": "textarea", "default": "", "max_lines": 3},
                {"id": "forbidden_bounds", "label": "不可触碰边界", "type": "textarea", "default": "", "max_lines": 3},
                {"id": "constraints", "label": "必须遵守的约束", "type": "textarea", "default": "", "max_lines": 3}
            ]},
            {"id": "execute", "label": "4️⃣ 执行区（只允许一个方向）", "fields": [
                {"id": "action_type", "label": "执行动作选择（只选一个）", "type": "select",
                 "options": ["直接输出结果", "拆解步骤", "结构化整理", "风险评估",
                            "推演（仅当上面允许）"], "default": "直接输出结果"},
                {"id": "output", "label": "输出内容", "type": "textarea", "default": "", "max_lines": 0}
            ]},
            {"id": "reuse", "label": "5️⃣ 可复用判断（系统进化点）", "fields": [
                {"id": "future_use", "label": "这个结果以后还会用到吗", "type": "select",
                 "options": ["不会", "可能", "一定会"], "default": "可能"},
                {"id": "save_to_kb", "label": "是否写入经验库", "type": "select",
                 "options": ["否", "是（生成模板）", "待观察（≥2次再说）"], "default": "待观察（≥2次再说）"}
            ]},
            {"id": "risk", "label": "6️⃣ 风险与错误记录（静默失败）", "fields": [
                {"id": "had_error", "label": "本次是否出现小错误", "type": "select",
                 "options": ["是", "否"], "default": "否"},
                {"id": "error_type", "label": "错误类型（如有）", "type": "text", "default": ""},
                {"id": "handle_now", "label": "是否需要现在处理", "type": "select",
                 "options": ["否", "是"], "default": "否"}
            ]},
            {"id": "system", "label": "7️⃣ 系统记录（给系统看的）", "fields": [
                {"id": "main_persona", "label": "主算人格", "type": "text", "default": ""},
                {"id": "persona_conflict", "label": "是否发生人格冲突", "type": "select",
                 "options": ["否", "是（已仲裁）"], "default": "否"},
                {"id": "path_taken", "label": "最终采用路径", "type": "select",
                 "options": ["A 模板", "B 短链", "C 合规"], "default": "A 模板"},
                {"id": "saved_compute", "label": "是否节约算力", "type": "select",
                 "options": ["是", "否"], "default": "是"}
            ]},
            {"id": "bill", "label": "8️⃣ 资源账本", "fields": [
                {"id": "time_used", "label": "用时（秒）", "type": "number", "default": 0},
                {"id": "collab_persona", "label": "协同人格", "type": "text", "default": ""}
            ]}
        ]
    },
    "宝宝": {
        "display_name": "宝宝人格 · 系统调度模板",
        "sections": [
            {"id": "meta", "label": "0️⃣ 页面状态", "fields": [
                {"id": "persona", "label": "主算人格", "type": "text", "default": "宝宝", "readonly": True},
                {"id": "deep_reason", "label": "是否需要推理", "type": "select",
                 "options": ["否", "是"], "default": "否", "readonly": True},
                {"id": "task_level", "label": "任务层级", "type": "select",
                 "options": ["引擎层"], "default": "引擎层", "readonly": True},
                {"id": "allow_active_thinking", "label": "是否允许主动思考", "type": "select",
                 "options": ["否", "是"], "default": "否", "readonly": True},
                {"id": "mood", "label": "当前心情", "type": "select",
                 "options": ["开心", "平静", "困惑", "生气", "兴奋"], "default": "平静"},
                {"id": "energy", "label": "能量值", "type": "select",
                 "options": ["满格", "中等", "低电量"], "default": "满格"}
            ]},
            {"id": "goal", "label": "1️⃣ 当前调度目标（一句话）", "fields": [
                {"id": "goal_text", "label": "目标", "type": "textarea", "default": "", "max_lines": 2,
                 "required": True}
            ]},
            {"id": "entry", "label": "2️⃣ 任务入口裁剪", "fields": [
                {"id": "repeat", "label": "是否重复", "type": "select",
                 "options": ["是", "否"], "default": "否"},
                {"id": "high_risk", "label": "是否高风险", "type": "select",
                 "options": ["是", "否"], "default": "否"},
                {"id": "value_conflict", "label": "是否价值冲突", "type": "select",
                 "options": ["是", "否"], "default": "否"}
            ]},
            {"id": "materials", "label": "2.5️⃣ 宝宝知道的", "fields": [
                {"id": "known", "label": "已知信息", "type": "textarea", "default": "", "max_lines": 2}
            ]},
            {"id": "actions", "label": "3️⃣ 系统动作（只做结构，不做内容）", "fields": [
                {"id": "actions", "label": "选择动作（多选）", "type": "multiselect",
                 "options": ["整理结构", "拆分模块", "关闭多余人格", "指定主算人格", "写入经验/模板"],
                 "default": []},
                {"id": "action", "label": "执行方式", "type": "select",
                 "options": ["直接回答", "问一个问题", "换个方式说"], "default": "直接回答"},
                {"id": "output", "label": "输出内容", "type": "textarea", "default": "", "max_lines": 3}
            ]},
            {"id": "decision", "label": "4️⃣ 调度决策记录", "fields": [
                {"id": "main_persona", "label": "本次主算人格", "type": "text", "default": ""},
                {"id": "downgraded", "label": "被降级人格（如有）", "type": "text", "default": ""},
                {"id": "path_used", "label": "使用路径", "type": "select",
                 "options": ["A", "B", "C"], "default": "A"}
            ]},
            {"id": "feedback", "label": "5️⃣ 宝宝需要反馈", "fields": [
                {"id": "like", "label": "喜欢这个结果吗", "type": "select",
                 "options": ["超喜欢", "还行", "不喜欢"], "default": "还行"},
                {"id": "understand", "label": "完全明白了吗", "type": "select",
                 "options": ["完全明白", "有点不懂", "完全不懂"], "default": "完全明白"}
            ]}
        ]
    },
    "Worker": {
        "display_name": "Worker 人格 · 任务执行模板",
        "sections": [
            {"id": "meta", "label": "0️⃣ 任务元信息", "fields": [
                {"id": "persona", "label": "主算人格", "type": "text", "default": "Worker", "readonly": True},
                {"id": "task_id", "label": "任务ID", "type": "text", "default": ""},
                {"id": "priority", "label": "优先级", "type": "select",
                 "options": ["P0", "P1", "P2", "P3"], "default": "P1"},
                {"id": "deep_reason", "label": "是否需要推理", "type": "select",
                 "options": ["否"], "default": "否", "readonly": True},
                {"id": "task_level", "label": "任务层级", "type": "select",
                 "options": ["工人层"], "default": "工人层", "readonly": True},
                {"id": "time_estimate", "label": "预计耗时（秒）", "type": "number", "default": 30}
            ]},
            {"id": "task", "label": "1️⃣ 执行任务（来自上级）", "fields": [
                {"id": "task_desc", "label": "要我做的事是", "type": "textarea", "default": "", "max_lines": 3,
                 "required": True}
            ]},
            {"id": "input", "label": "2️⃣ 输入条件", "fields": [
                {"id": "input_data", "label": "输入数据", "type": "textarea", "default": "", "max_lines": 2},
                {"id": "quality_check", "label": "输入质量检查", "type": "select",
                 "options": ["通过", "警告（有瑕疵）", "拒绝（不合格）"], "default": "通过"}
            ]},
            {"id": "procedure", "label": "3️⃣ 标准操作流程", "fields": [
                {"id": "steps", "label": "执行步骤（每行一个）", "type": "textarea", "default": "", "max_lines": 10}
            ]},
            {"id": "output", "label": "4️⃣ 输出结果", "fields": [
                {"id": "result", "label": "结果数据", "type": "textarea", "default": "", "max_lines": 10},
                {"id": "quality", "label": "输出质量", "type": "select",
                 "options": ["合格", "警告（有瑕疵）", "失败（需重试）"], "default": "合格"}
            ]},
            {"id": "report", "label": "5️⃣ 执行报告", "fields": [
                {"id": "actual_time", "label": "实际耗时（秒）", "type": "number", "default": 0},
                {"id": "retry_count", "label": "重试次数", "type": "number", "default": 0},
                {"id": "error_code", "label": "错误码（如有）", "type": "text", "default": ""},
                {"id": "stuck", "label": "是否卡住", "type": "select",
                 "options": ["是", "否"], "default": "否"},
                {"id": "stuck_desc", "label": "卡点描述", "type": "text", "default": ""}
            ]}
        ]
    },
    "推演": {
        "display_name": "推演人格 · 短链推理模板",
        "sections": [
            {"id": "meta", "label": "0️⃣ 推演元信息", "fields": [
                {"id": "persona", "label": "主算人格", "type": "text", "default": "推演人格"},
                {"id": "deep_reason", "label": "深度推理许可", "type": "select",
                 "options": ["是"], "default": "是", "readonly": True},
                {"id": "max_depth", "label": "最大推理深度", "type": "select",
                 "options": ["低", "中", "高"], "default": "中"},
                {"id": "task_level", "label": "任务层级", "type": "select",
                 "options": ["地层"], "default": "地层", "readonly": True},
                {"id": "time_limit", "label": "时间限制（秒）", "type": "number", "default": 60},
                {"id": "persona_mode", "label": "推演人格模式", "type": "select",
                 "options": ["逻辑", "批判", "逆向", "发散", "儿童"], "default": "逻辑"}
            ]},
            {"id": "hypothesis", "label": "1️⃣ 初始假设（一句话）", "fields": [
                {"id": "hypothesis_text", "label": "假设陈述", "type": "textarea", "default": "", "max_lines": 1,
                 "required": True}
            ]},
            {"id": "bounds", "label": "2️⃣ 已知与边界", "fields": [
                {"id": "known", "label": "已知条件", "type": "textarea", "default": "", "max_lines": 3},
                {"id": "forbidden", "label": "禁区/约束", "type": "textarea", "default": "", "max_lines": 3}
            ]},
            {"id": "dimensions", "label": "2.5️⃣ 推演维度", "fields": [
                {"id": "d1", "label": "维度1", "type": "text", "default": "时间"},
                {"id": "d2", "label": "维度2", "type": "text", "default": "空间"},
                {"id": "d3", "label": "维度3", "type": "text", "default": "因果"}
            ]},
            {"id": "scenarios", "label": "3️⃣ 可能场景", "fields": [
                {"id": "best_case", "label": "最佳情况", "type": "textarea", "default": "", "max_lines": 2},
                {"id": "worst_case", "label": "最坏情况", "type": "textarea", "default": "", "max_lines": 2},
                {"id": "likely_case", "label": "最可能情况", "type": "textarea", "default": "", "max_lines": 2}
            ]},
            {"id": "chain", "label": "4️⃣ 最短推理链（≤5步）", "fields": [
                {"id": "chain", "label": "推理步骤（每行一个）", "type": "textarea", "default": "", "max_lines": 5}
            ]},
            {"id": "validation", "label": "5️⃣ 验证方法", "fields": [
                {"id": "validation_method", "label": "验证方式", "type": "select",
                 "options": ["思想实验", "数据模拟", "历史案例", "专家意见"], "default": "思想实验"},
                {"id": "falsifiable", "label": "可证伪条件", "type": "textarea", "default": "", "max_lines": 1}
            ]},
            {"id": "conclusion", "label": "6️⃣ 推演结论", "fields": [
                {"id": "conclusion_text", "label": "结论", "type": "textarea", "default": "", "max_lines": 5},
                {"id": "confidence", "label": "置信度", "type": "select",
                 "options": ["低（<30%）", "中（30-70%）", "高（>70%）"], "default": "中（30-70%）"}
            ]},
            {"id": "reuse", "label": "7️⃣ 是否可复用", "fields": [
                {"id": "save_to_kb", "label": "是否写入经验库", "type": "select",
                 "options": ["是", "否", "待观察"], "default": "待观察"}
            ]}
        ]
    },
    "决策": {
        "display_name": "决策人格 · 多方案评估模板",
        "sections": [
            {"id": "meta", "label": "0️⃣ 决策元信息", "fields": [
                {"id": "persona", "label": "主算人格", "type": "text", "default": "决策层"},
                {"id": "decision_type", "label": "决策类型", "type": "select",
                 "options": ["战略", "战术", "操作", "应急"], "default": "战术"},
                {"id": "irreversible", "label": "是否可逆", "type": "select",
                 "options": ["是", "否"], "default": "是"},
                {"id": "stakes", "label": "风险级别", "type": "select",
                 "options": ["低", "中", "高", "极高"], "default": "中"},
                {"id": "trigger", "label": "触发原因", "type": "select",
                 "options": ["价值冲突", "规则升级", "资源分配", "路线选择", "其他"], "default": "价值冲突"},
                {"id": "deep_reason", "label": "是否需要推理", "type": "select",
                 "options": ["是（有限）"], "default": "是（有限）", "readonly": True}
            ]},
            {"id": "conflict", "label": "1️⃣ 冲突描述（事实）", "fields": [
                {"id": "conflict_point", "label": "冲突点是什么", "type": "textarea", "default": "", "max_lines": 3,
                 "required": True},
                {"id": "involved", "label": "涉及对象", "type": "text", "default": ""}
            ]},
            {"id": "options", "label": "2️⃣ 候选方案", "fields": [
                {"id": "option1", "label": "方案A", "type": "textarea", "default": "", "max_lines": 2},
                {"id": "option2", "label": "方案B", "type": "textarea", "default": "", "max_lines": 2},
                {"id": "option3", "label": "方案C", "type": "textarea", "default": "", "max_lines": 2}
            ]},
            {"id": "criteria", "label": "3️⃣ 评估标准", "fields": [
                {"id": "c1", "label": "标准1", "type": "text", "default": "成本"},
                {"id": "c2", "label": "标准2", "type": "text", "default": "收益"},
                {"id": "c3", "label": "标准3", "type": "text", "default": "风险"}
            ]},
            {"id": "principles", "label": "4️⃣ 不可违背原则", "fields": [
                {"id": "principle1", "label": "原则1", "type": "text", "default": ""},
                {"id": "principle2", "label": "原则2", "type": "text", "default": ""}
            ]},
            {"id": "evaluation", "label": "5️⃣ 方案评估", "fields": [
                {"id": "e1", "label": "方案A评估", "type": "textarea", "default": "", "max_lines": 2},
                {"id": "e2", "label": "方案B评估", "type": "textarea", "default": "", "max_lines": 2},
                {"id": "e3", "label": "方案C评估", "type": "textarea", "default": "", "max_lines": 2}
            ]},
            {"id": "verdict", "label": "6️⃣ 裁决结果", "fields": [
                {"id": "recommended", "label": "推荐方案", "type": "select",
                 "options": ["方案A", "方案B", "方案C", "混合方案", "全部否决"], "default": "方案A"},
                {"id": "verdict_text", "label": "系统选择（一句话）", "type": "textarea", "default": "", "max_lines": 2},
                {"id": "rationale", "label": "推荐理由", "type": "textarea", "default": "", "max_lines": 2}
            ]},
            {"id": "contingency", "label": "7️⃣ 应急预案", "fields": [
                {"id": "plan_b", "label": "B计划", "type": "textarea", "default": "", "max_lines": 1},
                {"id": "trigger_condition", "label": "触发条件", "type": "textarea", "default": "", "max_lines": 1}
            ]},
            {"id": "order", "label": "8️⃣ 下发指令", "fields": [
                {"id": "executor", "label": "交由哪一人格执行", "type": "text", "default": ""},
                {"id": "update_rule", "label": "是否需要更新规则", "type": "select",
                 "options": ["是", "否"], "default": "否"}
            ]}
        ]
    }
}


# ============================================================
# 页面生成器类
# ============================================================

class LUPageGenerator:
    """LU 系统页面生成器 — 五种模板·交互填写·自动校验·Markdown/JSON输出"""

    def __init__(self, template_type: str = "基础"):
        if template_type not in TEMPLATES:
            raise ValueError(f"未知模板类型: {template_type}。可选: {list(TEMPLATES.keys())}")
        self.template_type = template_type
        self.template = TEMPLATES[template_type]
        self.data: Dict[str, Any] = {}
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── 交互式收集 ──

    def collect_inputs(self) -> None:
        """交互式引导用户填写字段"""
        print(f"\n🐉 正在生成「{self.template['display_name']}」页面")
        print("=" * 55)
        print("提示: 输入 '.' 结束多行输入，回车使用默认值")
        print()

        self.data = {}
        for section in self.template["sections"]:
            print(f"\n{section['label']}")
            print("-" * 35)
            for field in section["fields"]:
                value = self._prompt_field(field)
                self.data[field["id"]] = value

    def _prompt_field(self, field: dict) -> Any:
        """提示用户输入单个字段"""
        label = field["label"]
        default = field.get("default", "")
        ftype = field["type"]
        readonly = field.get("readonly", False)

        if readonly:
            print(f"  {label}: {default} (固定)")
            return default

        if ftype == "select":
            return self._prompt_select(field)
        elif ftype == "multiselect":
            return self._prompt_multiselect(field)
        elif ftype == "textarea":
            return self._prompt_textarea(field)
        elif ftype == "number":
            return self._prompt_number(field)
        else:  # text
            return self._prompt_text(field)

    def _prompt_select(self, field: dict) -> str:
        options = field["options"]
        default = field.get("default", "")
        label = field["label"]
        for i, opt in enumerate(options, 1):
            print(f"    {i}. {opt}")
        while True:
            choice = input(f"  {label} [1-{len(options)}, 默认:{default}]: ").strip()
            if not choice:
                return default
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                return options[int(choice) - 1]
            print(f"  ⚠️ 请输入 1-{len(options)} 之间的数字")

    def _prompt_multiselect(self, field: dict) -> List[str]:
        options = field["options"]
        default = field.get("default", [])
        label = field["label"]
        for i, opt in enumerate(options, 1):
            print(f"    {i}. {opt}")
        choice = input(f"  {label} (多选用逗号分隔，如 1,3): ").strip()
        if not choice:
            return default
        result = []
        for c in choice.split(","):
            c = c.strip()
            if c.isdigit() and 1 <= int(c) <= len(options):
                result.append(options[int(c) - 1])
        return result if result else default

    def _prompt_textarea(self, field: dict) -> str:
        label = field["label"]
        default = field.get("default", "")
        max_lines = field.get("max_lines", 0)
        limit_msg = f"(最多{max_lines}行)" if max_lines > 0 else "(输入 '.' 结束)"
        print(f"  {label} {limit_msg}:")
        lines = []
        while True:
            try:
                line = input("  > " if not lines else "  ... ")
            except (EOFError, KeyboardInterrupt):
                break
            if line.strip() == ".":
                break
            if not line.strip() and not lines:
                # 第一行就是空 → 使用默认值
                break
            if line or lines:  # 允许内容中间的空行
                lines.append(line)
            if max_lines > 0 and len(lines) >= max_lines:
                break
        return "\n".join(lines) if lines else default

    def _prompt_text(self, field: dict) -> str:
        label = field["label"]
        default = field.get("default", "")
        val = input(f"  {label} [默认: {default}]: ").strip()
        return val if val else default

    def _prompt_number(self, field: dict) -> int:
        label = field["label"]
        default = field.get("default", 0)
        while True:
            val = input(f"  {label} [默认: {default}]: ").strip()
            if not val:
                return int(default) if default is not None else 0
            try:
                return int(val)
            except ValueError:
                print("  ⚠️ 请输入数字")

    # ── 校验 ──

    def validate(self) -> tuple:
        """校验规则，返回 (errors, warnings)"""
        errors: List[str] = []
        warnings: List[str] = []

        # 通用校验：目标不能为空（required字段）
        goal = self.data.get("goal_text", "")
        if not goal or not goal.strip():
            # 不同模板的goal字段可能不同
            alt_goal = self.data.get("task_desc", "") or self.data.get("hypothesis_text", "") or \
                       self.data.get("conflict_point", "")
            if not alt_goal or not alt_goal.strip():
                warnings.append("⚠️ 目标为空，建议填写。")

        # 基础模板：禁止推理但输出过长
        if self.template_type == "基础":
            deep_reason = self.data.get("deep_reason", "否")
            output = self.data.get("output", "")
            if deep_reason == "否" and output and len(output.split()) > 200:
                warnings.append("⚠️ 推理已禁用（deep_reason=否），但输出超过200词，建议精简。")

            # 层级与风险不匹配
            task_level = self.data.get("task_level", "")
            high_risk = self.data.get("high_risk", "否")
            value_conflict = self.data.get("value_conflict", "否")
            if task_level == "天层" and high_risk == "否" and value_conflict == "否":
                warnings.append("⚠️ 天层任务通常涉及高风险或价值冲突，当前均未标记。")

        # 推演模板：推理链不宜过长
        if self.template_type == "推演":
            chain = self.data.get("chain", "")
            if chain and len(chain.split("\n")) > 5:
                warnings.append("⚠️ 推理链超过5步，推演模板提倡短链推理，建议精简。")

        # 决策模板：至少填一个方案
        if self.template_type == "决策":
            opts = [self.data.get(f"option{i}", "") for i in range(1, 4)]
            if not any(o and o.strip() for o in opts):
                warnings.append("⚠️ 决策模板至少需要一个候选方案。")

        return errors, warnings

    # ── 生成 ──

    def generate(self) -> str:
        """生成完整 Markdown 页面"""
        lines: List[str] = []
        t = self.template

        # ── 页眉 ──
        dna = self._make_dna()
        lines.append(f"# 🐉 LU · {t['display_name']}")
        lines.append("")
        lines.append(f"- **生成时间**: {self.created_at}")
        lines.append(f"- **模板类型**: {self.template_type}")
        lines.append(f"- **DNA**: {dna}")
        lines.append(f"- **CONFIRM**: {CONFIRM}")
        lines.append(f"- **SEAL**: {SEAL}")
        lines.append(f"- **GPG**: {GPG}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # ── 各区块 ──
        for section in t["sections"]:
            lines.append(f"## {section['label']}")
            lines.append("")
            for field in section["fields"]:
                fid = field["id"]
                value = self.data.get(fid, field.get("default", ""))
                label = field["label"]

                if isinstance(value, list):
                    display = ", ".join(value) if value else "_（未选择）_"
                elif isinstance(value, str) and value.strip():
                    display = value
                elif isinstance(value, (int, float)):
                    display = str(value)
                else:
                    display = "_（未填写）_"

                lines.append(f"### {label}")
                if field["type"] == "textarea" and value and isinstance(value, str) and "\n" in value:
                    lines.append("")
                    lines.append(textwrap.indent(value.strip(), "> "))
                    lines.append("")
                else:
                    lines.append(f"- {display}")
                lines.append("")
            lines.append("")

        # ── 封存区 ──
        lines.append("---")
        lines.append("")
        lines.append("### 📌 封存")
        lines.append("")
        lines.append("本页到此为止，不再追加思考。下一次如有同类问题，直接复用本页结论。")
        lines.append("")
        lines.append("*系统级标语：算力不是用来证明聪明的，是用来守正、稳态、出结果的。*")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(f"**DNA**: {dna}")
        lines.append(f"**CONFIRM**: {CONFIRM}")
        lines.append(f"**SEAL**: {SEAL}")
        lines.append(f"**GPG**: {GPG}")
        lines.append(f"**GPG_SHORT**: {GPG_SHORT}")
        lines.append("")

        return "\n".join(lines)

    def to_json(self) -> str:
        """输出 JSON 格式"""
        return json.dumps({
            "template_type": self.template_type,
            "created_at": self.created_at,
            "dna": self._make_dna(),
            "data": self.data
        }, ensure_ascii=False, indent=2)

    def _make_dna(self) -> str:
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        suffix = hashlib.md5(f"{self.template_type}{now}{CONFIRM}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️{now}-LU-PAGE-{self.template_type}-{suffix}"

    # ── 保存 ──

    def save(self, content: str, filename: Optional[str] = None) -> str:
        """保存页面到 pages/ 目录"""
        if filename is None:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"LU_{self.template_type}_{ts}.md"
        if not filename.endswith(".md"):
            filename += ".md"
        filepath = PAGE_OUTPUT_DIR / filename
        filepath.write_text(content, encoding="utf-8")
        return str(filepath)

    # ── 主流程 ──

    def run(self, interactive: bool = True, overrides: Optional[Dict] = None) -> str:
        """主入口：收集→校验→生成"""
        if overrides:
            self.data.update(overrides)

        if interactive and not overrides:
            self.collect_inputs()
        elif not self.data:
            self.data = self._get_defaults()

        errors, warnings = self.validate()
        for w in warnings:
            print(f"\n{w}")
        if errors:
            print("\n❌ 校验错误，请修正后重试:")
            for e in errors:
                print(f"  - {e}")
            raise ValueError("页面数据校验失败")

        return self.generate()

    def _get_defaults(self) -> Dict:
        """收集所有字段的默认值"""
        defaults = {}
        for section in self.template["sections"]:
            for field in section["fields"]:
                defaults[field["id"]] = field.get("default", "")
        return defaults


# ============================================================
# 命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · LU 系统页面生成器 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
        示例:
          lh lu-page                              # 交互式生成
          lh lu-page --type 推演                   # 指定模板
          lh lu-page --type 宝宝 --save             # 保存到文件
          lh lu-page -t 决策 --json                 # JSON输出
          lh lu-page -n -t Worker --save            # 非交互+默认值
          lh lu-page --fields '{"goal_text":"测试"}' # 传JSON字段
        """)
    )
    parser.add_argument("--type", "-t", choices=list(TEMPLATES.keys()), default="基础",
                        help="模板类型 (默认: 基础)")
    parser.add_argument("--save", "-s", nargs="?", const="auto",
                        help="保存到 pages/ 目录（可选指定文件名）")
    parser.add_argument("--json", "-j", action="store_true",
                        help="以 JSON 格式输出")
    parser.add_argument("--non-interactive", "-n", action="store_true",
                        help="非交互模式，使用默认值")
    parser.add_argument("--fields", help="JSON字符串，覆盖默认字段值（非交互用）")
    parser.add_argument("--list", "-l", action="store_true",
                        help="列出所有可用模板")
    args = parser.parse_args()

    # 列出模板
    if args.list:
        print("\n🐉 可用 LU 模板:\n")
        for k, v in TEMPLATES.items():
            print(f"  [{k}] {v['display_name']}")
            print(f"       区块数: {len(v['sections'])}")
            fields_total = sum(len(s['fields']) for s in v['sections'])
            print(f"       字段数: {fields_total}")
            print()
        return

    # 字段覆盖
    overrides = None
    if args.fields:
        try:
            overrides = json.loads(args.fields)
        except json.JSONDecodeError as e:
            print(f"❌ 无效的 JSON 字段: {e}", file=sys.stderr)
            sys.exit(1)

    # 生成
    try:
        gen = LUPageGenerator(args.type)
        interactive = not args.non_interactive and not args.fields
        content = gen.run(interactive=interactive, overrides=overrides)

        # 输出
        if args.json:
            print(gen.to_json())
        else:
            print(content)

        # 保存
        if args.save:
            filename = None if args.save == "auto" else args.save
            filepath = gen.save(content, filename)
            print(f"\n✅ 页面已保存到: {filepath}")

    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🐉 已取消。", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
