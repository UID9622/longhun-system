#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 CSDN 文章智能审计器（接入 longhun-system 版）
Longhun CSDN Article Intelligence Auditor

功能：发布前自动审计内容质量、合规性、标签分类；
      识别用户危险/错误意图；从用户反馈中学习。
DNA: #龍芯⚡️2026-06-27-LONGHUN-CSDN-AUDITOR-v1.0
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_FEEDBACK_DIR = Path.home() / ".longhun" / "csdn_auditor"
DEFAULT_FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)


# ---------- 常量与规则 ----------

TEST_KEYWORDS = [
    "测试", "test", "草稿", "draft", "临时", "tmp", "示例", "sample",
    "试行", "演练", "不要发布", "勿发", "内部测试",
]

SENSITIVE_PATTERNS = {
    "手机号": r"\b1[3-9]\d{9}\b",
    "身份证": r"\b\d{17}[\dXx]\b",
    "银行卡": r"\b\d{16,19}\b",
    "GPG指纹": r"\b[A-F0-9]{40}\b",
    "本地路径": r"/Users/[a-zA-Z0-9_/-]+|/home/[a-zA-Z0-9_/-]+",
    "DNA码": r"#龍芯⚡️[^\s\n]+",
    "确认码": r"#CONFIRM[^\s\n]+",
}

SOVEREIGNTY_KEYWORDS = [
    "龍魂", "CNSH", "龍芯", "主权", "自主可控", "人民", "老百姓",
    "宪法", "君子协议", "DNA", "UID9622",
]

LOW_QUALITY_SIGNALS = [
    "无意义", "随便写写", "占位", "待补充", "TODO", "FIXME",
    "哈哈哈", "测试一下", "发着玩",
]

CATEGORY_KEYWORDS = {
    "人工智能": ["AI", "人工智能", "大模型", "LLM", "神经网络", "深度学习", "机器学习"],
    "技术治理": ["治理", "审计", "合规", "安全", "协议", "标准", "规范"],
    "数学": ["黎曼", "数论", "数学", "证明", "定理", "公式", "zeta"],
    "哲学文化": ["易经", "道德经", "五行", "三才", "洛书", "龍魂", "哲学"],
    "软件开发": ["Python", "代码", "开发", "程序", "接口", "API", "工程"],
    "社会观察": ["老百姓", "人民", "社会", "信任", "数字时代", "退伍军人"],
}

DEFAULT_TAGS = ["龍魂", "CNSH", "AI治理"]


class ArticleAuditResult:
    """文章审计结果"""

    def __init__(self):
        self.passed = False
        self.score = 0.0
        self.quality_score = 0.0
        self.compliance_score = 0.0
        self.sovereignty_score = 0.0
        self.recommended_tags: List[str] = []
        self.recommended_category = "软件开发"
        self.archive_folder = "未分类"
        self.issues: List[Dict[str, str]] = []
        self.sensitive_hits: List[Dict[str, str]] = []
        self.is_test = False
        self.is_low_quality = False
        self.summary = ""

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "score": round(self.score, 2),
            "quality_score": round(self.quality_score, 2),
            "compliance_score": round(self.compliance_score, 2),
            "sovereignty_score": round(self.sovereignty_score, 2),
            "recommended_tags": self.recommended_tags,
            "recommended_category": self.recommended_category,
            "archive_folder": self.archive_folder,
            "issues": self.issues,
            "sensitive_hits": self.sensitive_hits,
            "is_test": self.is_test,
            "is_low_quality": self.is_low_quality,
            "summary": self.summary,
        }


class IntentAuditResult:
    """用户意图审计结果"""

    def __init__(self):
        self.risk_level = "🟢 低风险"
        self.risk_score = 0
        self.block_reasons: List[str] = []
        self.warn_reasons: List[str] = []
        self.suggestion = ""
        self.requires_explicit_confirm = False

    def to_dict(self) -> dict:
        return {
            "risk_level": self.risk_level,
            "risk_score": self.risk_score,
            "block_reasons": self.block_reasons,
            "warn_reasons": self.warn_reasons,
            "suggestion": self.suggestion,
            "requires_explicit_confirm": self.requires_explicit_confirm,
        }


class CSDNAuditor:
    """CSDN 同步智能审计器"""

    def __init__(self, module_dir: Optional[Path] = None):
        self.module_dir = module_dir or DEFAULT_FEEDBACK_DIR
        self.module_dir.mkdir(parents=True, exist_ok=True)
        self.feedback_path = self.module_dir / "feedback_store.jsonl"
        self.feedback: List[dict] = self._load_feedback()

    # ---------- 反馈学习 ----------

    def _load_feedback(self) -> List[dict]:
        feedback = []
        if self.feedback_path.exists():
            try:
                with open(self.feedback_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            feedback.append(json.loads(line))
            except Exception:
                pass
        return feedback

    def record_feedback(
        self,
        article_id: str,
        action: str,
        original: dict,
        corrected: dict,
        reason: str = "",
    ):
        """记录用户修正，用于学习"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "article_id": article_id,
            "action": action,
            "original": original,
            "corrected": corrected,
            "reason": reason,
        }
        self.feedback.append(record)
        with open(self.feedback_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def get_learned_tags(self, title: str, content: str) -> List[str]:
        """从反馈中学习用户偏好的标签"""
        candidates = []
        for fb in self.feedback:
            if fb.get("action") in ("tag_correction", "correction") and fb.get("corrected"):
                fb_title = fb.get("original", {}).get("title", "")
                similarity = self._text_similarity(title, fb_title)
                if similarity > 0.5:
                    candidates.append((similarity, fb["corrected"]))
        if not candidates:
            return []
        candidates.sort(reverse=True, key=lambda x: x[0])
        return candidates[0][1].get("tags", [])

    def get_learned_category(self, title: str, content: str) -> Optional[str]:
        """从反馈中学习用户偏好的分类"""
        candidates = []
        for fb in self.feedback:
            if fb.get("action") in ("category_correction", "correction") and fb.get("corrected"):
                fb_title = fb.get("original", {}).get("title", "")
                similarity = self._text_similarity(title, fb_title)
                if similarity > 0.5:
                    candidates.append((similarity, fb["corrected"]))
        if not candidates:
            return None
        candidates.sort(reverse=True, key=lambda x: x[0])
        return candidates[0][1].get("category")

    @staticmethod
    def _text_similarity(a: str, b: str) -> float:
        """简单的 Jaccard 相似度"""
        set_a = set(a.lower())
        set_b = set(b.lower())
        if not set_a or not set_b:
            return 0.0
        return len(set_a & set_b) / len(set_a | set_b)

    # ---------- 文章审计 ----------

    def audit_article(
        self,
        title: str,
        content: str,
        existing_tags: Optional[List[str]] = None,
        existing_category: Optional[str] = None,
    ) -> ArticleAuditResult:
        """对文章进行发布前审计"""
        result = ArticleAuditResult()
        full_text = f"{title}\n{content}"

        # 1. 测试性检测
        result.is_test = self._detect_test_article(title, content)
        if result.is_test:
            result.issues.append({
                "level": "🔴",
                "type": "测试性内容",
                "message": "标题或正文含测试/草稿关键词，疑似非正式内容。",
            })

        # 2. 低质量检测
        result.is_low_quality = self._detect_low_quality(title, content)
        if result.is_low_quality:
            result.issues.append({
                "level": "🔴",
                "type": "低质量内容",
                "message": "内容含低质量信号或字数过少。",
            })

        # 3. 敏感信息扫描
        result.sensitive_hits = self._scan_sensitive(full_text)
        for hit in result.sensitive_hits:
            result.issues.append({
                "level": "🟡",
                "type": f"敏感信息: {hit['type']}",
                "message": f"发现 {hit['count']} 处，示例: {hit['example']}",
            })

        # 4. 质量评分
        result.quality_score = self._quality_score(title, content, result)

        # 5. 合规评分
        result.compliance_score = self._compliance_score(title, content, result)

        # 6. 主权评分
        result.sovereignty_score = self._sovereignty_score(title, content)

        # 7. 综合评分
        result.score = round(
            result.quality_score * 0.4
            + result.compliance_score * 0.3
            + result.sovereignty_score * 0.3,
            2,
        )

        # 8. 自动推荐标签和分类
        result.recommended_tags = self._recommend_tags(title, content, existing_tags)
        result.recommended_category = self._recommend_category(title, content, existing_category)
        result.archive_folder = self._recommend_archive_folder(result.recommended_category, title)

        # 9. 是否通过
        if result.is_test or result.is_low_quality:
            result.passed = False
        elif result.score < 40:
            result.passed = False
        else:
            result.passed = True

        # 10. 生成总结
        result.summary = self._generate_summary(result)
        return result

    def _detect_test_article(self, title: str, content: str) -> bool:
        title = title or ""
        content = content or ""
        # 如果 content 是文件路径，只取文件名，避免目录名含 test 误伤
        if "/" in content or "\\" in content:
            content = content.split("/")[-1].split("\\")[-1]
        text = f"{title} {content[:500]}".lower()
        return any(kw.lower() in text for kw in TEST_KEYWORDS)

    def _detect_low_quality(self, title: str, content: str) -> bool:
        content = content or ""
        if len(content.strip()) < 100:
            return True
        text_lower = content.lower()
        return any(sig.lower() in text_lower for sig in LOW_QUALITY_SIGNALS)

    def _scan_sensitive(self, text: str) -> List[Dict[str, str]]:
        hits = []
        for name, pattern in SENSITIVE_PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                hits.append({
                    "type": name,
                    "count": len(matches),
                    "example": matches[0][:50] if isinstance(matches[0], str) else str(matches[0])[:50],
                })
        return hits

    def _quality_score(self, title: str, content: str, result: ArticleAuditResult) -> float:
        content = content or ""
        score = 60.0
        # 字数加分
        word_count = len(content)
        if word_count > 500:
            score += 15
        if word_count > 2000:
            score += 10
        # 结构加分
        if re.search(r"#{2,3}\s+", content):
            score += 10
        # 图片/链接加分
        if re.search(r"!\[|https?://", content):
            score += 5
        # 低质量扣分
        if result.is_low_quality:
            score -= 40
        if result.is_test:
            score -= 30
        return max(0.0, min(100.0, score))

    def _compliance_score(self, title: str, content: str, result: ArticleAuditResult) -> float:
        score = 80.0
        # 敏感信息扣分
        for hit in result.sensitive_hits:
            if hit["type"] in ("身份证", "银行卡", "手机号"):
                score -= 30
            elif hit["type"] == "DNA码":
                score -= 10
            elif hit["type"] == "本地路径":
                score -= 15
            else:
                score -= 10
        # 标题合规
        if len(title) < 5:
            score -= 20
        return max(0.0, min(100.0, score))

    def _sovereignty_score(self, title: str, content: str) -> float:
        full_text = f"{title} {content}"
        score = 50.0
        for kw in SOVEREIGNTY_KEYWORDS:
            if kw in full_text:
                score += 5
                if score >= 100:
                    break
        # 如果标题含龍魂/CNSH/龍芯，额外加分
        if any(kw in title for kw in ["龍魂", "CNSH", "龍芯"]):
            score += 15
        return max(0.0, min(100.0, score))

    def _recommend_tags(self, title: str, content: str, existing_tags: Optional[List[str]]) -> List[str]:
        full_text = f"{title} {content}".lower()
        tags = set(existing_tags or [])
        # 基于分类关键词推荐
        for cat, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in full_text:
                    tags.add(cat)
                    break
        # 基于反馈学习
        learned = self.get_learned_tags(title, content)
        for t in learned:
            tags.add(t)
        # 默认兜底
        if not tags:
            tags = set(DEFAULT_TAGS)
        return sorted(list(tags))[:8]

    def _recommend_category(self, title: str, content: str, existing_category: Optional[str]) -> str:
        if existing_category and existing_category != "软件开发":
            return existing_category
        # 优先使用反馈中学到的分类
        learned = self.get_learned_category(title, content)
        if learned:
            return learned
        full_text = f"{title} {content}".lower()
        scores = {}
        for cat, keywords in CATEGORY_KEYWORDS.items():
            scores[cat] = sum(1 for kw in keywords if kw.lower() in full_text)
        if scores:
            best = max(scores, key=scores.get)
            if scores[best] > 0:
                return best
        return "软件开发"

    def _recommend_archive_folder(self, category: str, title: str) -> str:
        # 按分类分装，若分类太泛再按标题首字/年份
        folder = category
        # 简单处理：若标题含年份
        m = re.search(r"20\d{2}", title)
        if m:
            folder = f"{category}/{m.group(0)}"
        return folder

    def _generate_summary(self, result: ArticleAuditResult) -> str:
        if result.is_test:
            return f"🔴 拦截：疑似测试/草稿内容，综合得分 {result.score}。"
        if result.is_low_quality:
            return f"🔴 拦截：低质量内容，综合得分 {result.score}。"
        if result.score < 40:
            return f"🔴 拦截：综合得分 {result.score} 低于发布阈值 40。"
        if result.sensitive_hits:
            return f"🟡 待审：综合得分 {result.score}，但含敏感信息 {len(result.sensitive_hits)} 处，建议处理后再发。"
        return f"🟢 通过：综合得分 {result.score}，推荐分类「{result.recommended_category}」，推荐标签 {result.recommended_tags}。"

    # ---------- 意图审计 ----------

    def audit_intent(self, text: str, intent: str, params: dict) -> IntentAuditResult:
        """审计用户意图是否存在风险"""
        result = IntentAuditResult()
        lowered = text.lower()

        # 危险：删除全部/所有
        if intent == "delete_article" and self._match_any(lowered, ["全部", "所有", "所有文章", "all", "everything"]):
            result.block_reasons.append("检测到“删除全部/所有”意图，这是高危险操作，已阻止。")
            result.risk_score += 90

        # 危险：发布测试/草稿（只检查标题和文件名，避免目录/口语误伤）
        if intent in ("publish_article", "update_article"):
            import os as _os
            title = params.get("title", "") or ""
            file_path = params.get("file_path", "") or ""
            file_name = _os.path.basename(file_path) if file_path else ""
            if self._detect_test_article(title, file_name):
                result.warn_reasons.append("标题或文件名含测试/草稿关键词，请确认是否为正式内容。")
                result.risk_score += 60

        # 风险：无明确目标
        if intent == "delete_article" and not params.get("article_id") and not params.get("title"):
            result.block_reasons.append("未识别到要删除的文章 ID 或标题，无法执行删除。")
            result.risk_score += 80

        # 风险：批量操作未明确
        if self._match_any(lowered, ["批量", "全部同步", "所有文件", "整个目录"]) and not params.get("directory"):
            result.warn_reasons.append("批量操作范围未明确，请确认具体目录。")
            result.risk_score += 40

        # 确定风险等级
        if result.block_reasons or result.risk_score >= 80:
            result.risk_level = "🔴 高风险"
            result.requires_explicit_confirm = True
        elif result.risk_score >= 40:
            result.risk_level = "🟡 中风险"
            result.requires_explicit_confirm = True
        else:
            result.risk_level = "🟢 低风险"

        if result.block_reasons:
            result.suggestion = "操作已被拦截。请明确具体目标后重试。"
        elif result.warn_reasons:
            result.suggestion = "操作有风险，请确认后再执行。"
        else:
            result.suggestion = "意图正常，可执行。"

        return result

    @staticmethod
    def _match_any(text: str, keywords: List[str]) -> bool:
        return any(kw in text for kw in keywords)

    def audit_text(self, text: str, title: str = "") -> dict:
        """便捷接口：直接审计任意文本，返回字典"""
        # 尝试从 text 第一行提取标题
        if not title and text:
            first = text.splitlines()[0].strip()
            if first.startswith("#"):
                title = first.lstrip("# ").strip()
            else:
                title = first[:60]
        result = self.audit_article(title=title, content=text)
        return result.to_dict()


if __name__ == "__main__":
    auditor = CSDNAuditor()
    result = auditor.audit_article(
        title="龍魂系统：让老百姓在数字世界里挺直腰杆",
        content="# 龍魂系统\n\n这是一篇测试文章。",
    )
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
