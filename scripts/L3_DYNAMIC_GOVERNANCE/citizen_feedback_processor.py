# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-SCRIPT-CITIZEN_FEEDBACK_PROCESSOR-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂公民反馈处理器 L3 v1.0

动态治理级别 (priority=0.85)
特性: 处理老百姓的声音，按规则优化系统

处理：
- 用户反馈
- 问题报告
- 改进建议
- 投诉

DNA: #龍芯⚇️2026-06-07-CITIZEN-FEEDBACK-PROCESSOR-L3-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
UID: 9622

理论指导: 曾仕强老师 - 民为贵，社稷次之，君为轻
献礼: 献给龍魂 - 老百姓的声音就是系统的方向盘
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))

from dna import DNAVerifier
from logger import get_logger
from config import get_config


class CitizenFeedbackProcessor:
    """
    公民反馈处理器 - 倾听人民的声音

    意图: 没有反馈的系统迟早会僵化
    承诺: 每一条反馈都被认真对待
    """

    # 反馈类型
    FEEDBACK_TYPES = {
        "bug": {"name": "缺陷", "priority": 0.95},
        "improvement": {"name": "改进建议", "priority": 0.70},
        "feature_request": {"name": "功能请求", "priority": 0.60},
        "complaint": {"name": "投诉", "priority": 0.85},
        "praise": {"name": "表扬", "priority": 0.50},
    }

    def __init__(self):
        """初始化反馈处理器"""
        self.logger = get_logger()
        self.config = get_config()
        self.dna = DNAVerifier.generate("CITIZEN-FEEDBACK-PROCESSOR", "L3")
        self.feedback_queue = []
        self.processed_feedback = []

    def submit_feedback(
        self,
        feedback_type: str,
        content: str,
        submitter: str = "anonymous",
        context: Dict = None
    ) -> Dict:
        """
        提交反馈

        意图: 降低反馈的门槛，让每个人都能发声
        """
        if feedback_type not in self.FEEDBACK_TYPES:
            self.logger.log_error(
                "INVALID_FEEDBACK_TYPE",
                f"未知反馈类型: {feedback_type}",
                self.dna
            )
            return {"success": False, "error": "Unknown feedback type"}

        feedback_entry = {
            "id": len(self.feedback_queue) + 1,
            "type": feedback_type,
            "priority": self.FEEDBACK_TYPES[feedback_type]["priority"],
            "content": content,
            "submitter": submitter,
            "submitted_at": datetime.now().isoformat(),
            "status": "submitted",
            "context": context or {},
            "dna": self.dna,
        }

        self.feedback_queue.append(feedback_entry)

        self.logger.log_operation(
            "L3",
            "feedback_submitted",
            self.dna,
            {
                "feedback_id": feedback_entry["id"],
                "type": feedback_type,
                "submitter": submitter,
            }
        )

        return {
            "success": True,
            "feedback_id": feedback_entry["id"],
            "message": "反馈已提交，感谢您的声音"
        }

    def process_feedback(self, feedback_id: int) -> Dict:
        """
        处理反馈

        意图: 不是收集反馈，而是真的改进
        """
        # 查找反馈
        feedback = None
        for f in self.feedback_queue:
            if f["id"] == feedback_id:
                feedback = f
                break

        if not feedback:
            return {"success": False, "error": "Feedback not found"}

        feedback["status"] = "processing"
        feedback["processed_at"] = datetime.now().isoformat()

        # 根据反馈类型处理
        if feedback["type"] == "bug":
            # 缺陷：立即标记为需要修复
            feedback["action"] = "create_issue"
            feedback["priority_level"] = "high"

        elif feedback["type"] == "improvement":
            # 改进建议：评估贡献值
            feedback["action"] = "evaluate_contribution"
            feedback["priority_level"] = "medium"

        elif feedback["type"] == "complaint":
            # 投诉：立即升级
            feedback["action"] = "escalate_to_maintainer"
            feedback["priority_level"] = "high"

        else:
            feedback["action"] = "archive"
            feedback["priority_level"] = "low"

        feedback["status"] = "processed"

        self.processed_feedback.append(feedback)

        self.logger.log_decision(
            "L3",
            f"feedback_processed_{feedback['type']}",
            f"行动: {feedback['action']}",
            self.dna
        )

        return {
            "success": True,
            "feedback_id": feedback_id,
            "action": feedback["action"],
            "message": f"反馈已处理: {feedback['action']}"
        }

    def get_feedback_stats(self) -> Dict:
        """
        获取反馈统计

        意图: 显示系统的反馈处理能力
        """
        stats = {
            "total_feedback": len(self.feedback_queue) + len(self.processed_feedback),
            "pending": len(self.feedback_queue),
            "processed": len(self.processed_feedback),
            "by_type": {},
        }

        all_feedback = self.feedback_queue + self.processed_feedback

        for feedback in all_feedback:
            ftype = feedback["type"]
            if ftype not in stats["by_type"]:
                stats["by_type"][ftype] = 0
            stats["by_type"][ftype] += 1

        return stats

    def generate_feedback_report(self) -> str:
        """
        生成反馈报告

        意图: 透明地显示人民的声音
        """
        stats = self.get_feedback_stats()

        report = f"""
{'='*60}
龍魂公民反馈报告
{'='*60}

统计时间: {datetime.now().isoformat()}
DNA: {self.dna}

反馈总数: {stats['total_feedback']}
  - 待处理: {stats['pending']}
  - 已处理: {stats['processed']}

反馈类型分布:
"""

        for ftype, count in stats["by_type"].items():
            type_name = self.FEEDBACK_TYPES.get(ftype, {}).get("name", ftype)
            report += f"\n  - {type_name}: {count}"

        report += f"\n\n最近提交的反馈:\n"

        for feedback in self.feedback_queue[-5:]:  # 显示最近 5 条
            report += f"""
  ID: {feedback['id']} | 类型: {self.FEEDBACK_TYPES[feedback['type']]['name']}
  提交者: {feedback['submitter']} | 时间: {feedback['submitted_at']}
  内容: {feedback['content'][:50]}...
"""

        report += f"\n{'='*60}\n"

        return report


if __name__ == "__main__":
    processor = CitizenFeedbackProcessor()

    print("🐉 龍魂公民反馈处理器 L3 v1.0")
    print("=" * 60)

    # 测试：提交反馈
    result = processor.submit_feedback(
        "bug",
        "系统在某些情况下会崩溃",
        "老李",
        {"os": "Linux", "version": "1.0"}
    )
    print(f"\n提交反馈: {'✅ 成功' if result['success'] else '❌ 失败'}")

    # 测试：处理反馈
    if result['success']:
        process_result = processor.process_feedback(result['feedback_id'])
        print(f"处理反馈: {process_result['action']}")

    print("\n" + processor.generate_feedback_report())
