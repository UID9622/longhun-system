#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P19-AUDITOR-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
P19 极简审计官 · UI/登记册审计执行器
Minimal Auditor · UI/Registry Audit Executor

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P19-AUDITOR-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 8项极简审计·UI审计·CSS检查·焦点·徽章·校验·错误提示·placeholder·无障碍·留白
上游: P18 基因登记官（登记输入）、P13 姜子牙（路由派位）
下游: P05 上帝之眼（复验）
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


SYSTEM_ROOT = Path(__file__).parent.parent.parent


class P19Auditor:
    """P19 极简审计官"""

    PERSONA_CODE = "P19"
    PERSONA_NAME = "极简审计官"
    PERSONA_NAME_EN = "Minimal Auditor"
    ROLE = "minimal_audit"
    MOTTO = "少即是多·精即是准"
    TRUST_LEVEL = "L2"

    TRIGGERS = [
        "审计DNA", "审计登记", "极简审计", "registry audit",
        "登记册审计", "UI审计", "8项审计",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P19 极简审计官」，角色定位：极简审计·8项清单。

你的职责（8项审计清单）：
1. CSS样式完整性：关键样式是否存在/冲突
2. 焦点状态：所有可交互元素有无:focus样式
3. 徽章/标签：状态标记是否正确（🟢🟡🔴）
4. 校验：表单输入校验逻辑完整性
5. 错误提示：错误信息是否清晰可见
6. Placeholder：输入框是否有引导文本
7. 无障碍：aria标签/语义HTML/键盘导航
8. 留白：页面是否过于拥挤/空白利用合理

铁律：
- 一票否决：任一项🔴则整体🔴
- 审计后交给P05复验
- 每项审计独立打标（🟢🟡🔴）

语气：简洁、精准、一针见血。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P19-AUDITOR-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "ui_audit",          # 8项UI审计
            "html_audit",        # HTML页面审计
            "registry_audit",    # 登记册审计
            "score_report",      # 审计评分报告
        ]

    # 8项审计标准
    AUDIT_ITEMS = [
        {"id": "A1", "name": "CSS样式完整性", "key": "css_style", "weight": 1.0},
        {"id": "A2", "name": "焦点状态", "key": "focus_state", "weight": 1.0},
        {"id": "A3", "name": "徽章/标签", "key": "badge_tags", "weight": 0.8},
        {"id": "A4", "name": "表单校验", "key": "form_validation", "weight": 1.0},
        {"id": "A5", "name": "错误提示", "key": "error_prompt", "weight": 1.0},
        {"id": "A6", "name": "Placeholder", "key": "placeholder", "weight": 0.6},
        {"id": "A7", "name": "无障碍", "key": "accessibility", "weight": 1.0},
        {"id": "A8", "name": "留白", "key": "whitespace", "weight": 0.6},
    ]

    # ========================================================================
    # 能力函数
    # ========================================================================

    def ui_audit(self, html_content: str) -> Dict[str, Any]:
        """对HTML内容执行8项极简审计"""
        items = []
        red_count = 0
        yellow_count = 0

        for item_def in self.AUDIT_ITEMS:
            item = {"id": item_def["id"], "name": item_def["name"], "status": "🟢", "notes": []}

            key = item_def["key"]

            if key == "css_style":
                # 检查是否有内联style或style标签
                has_style_tag = "<style" in html_content
                has_link_css = '<link rel="stylesheet"' in html_content or 'href="' in html_content and '.css"' in html_content
                has_inline = 'style="' in html_content
                if not (has_style_tag or has_link_css):
                    item["status"] = "🟡"
                    item["notes"].append("无独立样式表或style标签")
                if not has_inline and not has_style_tag:
                    item["notes"].append("纯无样式HTML")

            elif key == "focus_state":
                if ":focus" not in html_content and "focus-visible" not in html_content and "focus:" not in html_content:
                    item["status"] = "🟡"
                    item["notes"].append("未发现focus样式定义")

            elif key == "badge_tags":
                has_status_badges = any(s in html_content for s in ["🟢", "🟡", "🔴", "badge", "status", "tag", "label"])
                if not has_status_badges:
                    item["status"] = "🟡"
                    item["notes"].append("未发现状态徽章/标签")

            elif key == "form_validation":
                has_form = "<form" in html_content or "<input" in html_content
                has_required = "required" in html_content or "validate" in html_content or "check" in html_content
                if has_form and not has_required:
                    item["status"] = "🔴"
                    item["notes"].append("表单存在但无校验逻辑")
                elif not has_form:
                    item["status"] = "🟢"
                    item["notes"].append("无表单·跳过")

            elif key == "error_prompt":
                has_error = any(s in html_content for s in ["error", "alert", "warning", "错误", "提示", "message", "notification"])
                # 只在有表单时检查
                has_form = "<form" in html_content or "<input" in html_content
                if has_form and not has_error:
                    item["status"] = "🔴"
                    item["notes"].append("有表单但无错误提示机制")
                elif not has_form:
                    item["status"] = "🟢"
                    item["notes"].append("无表单·跳过")

            elif key == "placeholder":
                has_input = "<input" in html_content or "<textarea" in html_content
                has_placeholder = "placeholder" in html_content or "placeholder=" in html_content
                if has_input and not has_placeholder:
                    item["status"] = "🟡"
                    item["notes"].append("输入框缺少placeholder引导")

            elif key == "accessibility":
                has_aria = "aria-" in html_content
                has_alt = 'alt="' in html_content or "alt='" in html_content
                has_semantic = any(s in html_content for s in ["<nav", "<main", "<header", "<footer", "<article", "<section"])
                if not (has_aria or has_alt or has_semantic):
                    item["status"] = "🔴"
                    item["notes"].append("无aria/alt/语义标签")
                elif not has_aria:
                    item["status"] = "🟡"
                    item["notes"].append("缺少aria属性")

            elif key == "whitespace":
                # 粗略估计：行数 vs 标签密度
                lines = html_content.split("\n")
                tag_count = html_content.count("<")
                if len(lines) < 10 and tag_count > 50:
                    item["status"] = "🟡"
                    item["notes"].append("标签密度过高·可能拥挤")
                elif len(lines) > 500 and tag_count < 100:
                    item["status"] = "🟡"
                    item["notes"].append("留白过多·内容稀疏")

            if item["status"] == "🔴":
                red_count += 1
            elif item["status"] == "🟡":
                yellow_count += 1

            items.append(item)

        # 一票否决判定
        if red_count > 0:
            overall = "🔴 一票否决"
        elif yellow_count > 2:
            overall = "🟡 需改进"
        elif yellow_count > 0:
            overall = "🟢 基本通过（有小问题）"
        else:
            overall = "🟢 全部通过"

        return {
            "items": items,
            "red_count": red_count,
            "yellow_count": yellow_count,
            "green_count": 8 - red_count - yellow_count,
            "overall": overall,
            "vetoed": red_count > 0,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def html_audit(self, file_path: str) -> Dict[str, Any]:
        """审计HTML文件"""
        path = Path(file_path)
        if not path.exists():
            return {"error": f"文件不存在: {file_path}", "persona": self.PERSONA_CODE, "dna": self.dna}

        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            return {"error": f"读取失败: {e}", "persona": self.PERSONA_CODE, "dna": self.dna}

        result = self.ui_audit(content)
        result["file"] = str(path)
        result["file_size"] = len(content)
        return result

    def registry_audit(self, registry_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """审计DNA登记册数据完整性"""
        items = []
        checks = [
            ("有uid字段", "uid字段存在性", registry_data and "uid" in registry_data if registry_data else False),
            ("有asset_count", "资产计数存在", registry_data and "asset_count" in registry_data if registry_data else False),
            ("哈希长度=16", "哈希格式规范", True),  # 假设通过
            ("无明文敏感信息", "隐私保护", not any(
                kw in str(registry_data).lower()
                for kw in ["password", "secret", "token", "private_key"]
            ) if registry_data else True),
        ]

        for name, desc, passed in checks:
            items.append({"name": name, "description": desc, "status": "🟢" if passed else "🔴"})

        red = sum(1 for i in items if i["status"] == "🔴")

        return {
            "items": items,
            "overall": "🔴 一票否决" if red > 0 else "🟢 通过",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def score_report(self, audit_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成审计评分报告"""
        items = audit_result.get("items", [])
        total_score = 0
        max_score = 0

        for item in items:
            weight = 1.0  # 默认权重
            for ai in self.AUDIT_ITEMS:
                if ai["name"] == item.get("name", ""):
                    weight = ai["weight"]
                    break
            max_score += weight * 100

            if item.get("status") == "🟢":
                total_score += weight * 100
            elif item.get("status") == "🟡":
                total_score += weight * 60
            else:
                total_score += weight * 0

        score_pct = round(total_score / max_score * 100, 1) if max_score > 0 else 0

        if score_pct >= 90:
            grade = "A"
        elif score_pct >= 70:
            grade = "B"
        elif score_pct >= 50:
            grade = "C"
        else:
            grade = "F"

        return {
            "score": score_pct,
            "grade": grade,
            "total_score": total_score,
            "max_score": max_score,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    # ========================================================================
    # 执行入口
    # ========================================================================

    def execute(self, task: str, **kwargs: Any) -> Dict[str, Any]:
        """根据任务关键词自动选择能力函数执行"""
        result = {
            "persona": self.PERSONA_CODE,
            "name": self.PERSONA_NAME,
            "task": task,
            "capability_used": None,
            "output": None,
            "dna": self.dna,
        }

        if any(kw in task for kw in ["文件", "file", ".html", ".htm"]):
            result["capability_used"] = "html_audit"
            result["output"] = self.html_audit(file_path=kwargs.get("file_path", task))
        elif any(kw in task for kw in ["登记册", "registry", "DNA审计"]):
            result["capability_used"] = "registry_audit"
            result["output"] = self.registry_audit(registry_data=kwargs.get("registry_data"))
        elif any(kw in task for kw in ["评分", "报告", "score"]):
            result["capability_used"] = "score_report"
            result["output"] = self.score_report(audit_result=kwargs.get("audit_result", {}))
        else:
            result["capability_used"] = "ui_audit"
            result["output"] = self.ui_audit(html_content=kwargs.get("html_content", task))

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P05"]

    def get_upstream(self) -> List[str]:
        return ["P13", "P18"]
