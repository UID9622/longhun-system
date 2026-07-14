"""三色安全审计器

DNA: #龍芯⚡️丙午·丙申·丙辰·戊子·坎-SDK-AUDITOR-v2.1
"""
from dataclasses import dataclass, field
import sys
from pathlib import Path
from typing import Optional


@dataclass
class AuditReport:
    """审计报告"""
    level: str            # "green" | "yellow" | "red"
    score: float          # 0.0 ~ 1.0
    alerts: list[str] = field(default_factory=list)
    fuse_appeal: str | None = None
    dna: str = ""
    red_count: int = 0
    yellow_count: int = 0
    jargon_count: int = 0
    plain_language_ok: bool = False


class Auditor:
    """三色审计 — 内容安全自动审查

    v2.1: 已对接 lh_anti_tamper.py 真实审计引擎。
    支持三色判定（绿/黄/红）+ 红色熔断 + 黄色待审 + 行话检测 + 白话重写检查。
    自研文档模式（source="self"）黄色警报仅记录不判定。
    """

    # ── 内联审计规则（SDK 独立运行时不依赖 bin/ 路径）──
    _RED_FLAGS: dict[str, str] = {
        "技术无国界": "削弱祖国优先立场",
        "用户体验优先": "潜在上瘾设计导向",
        "灵活处理": "松动底线信号",
        "国际接轨": "可能覆盖本地数据主权",
        "简化管理": "可能删除署名和证据链",
        "商业化需要": "与铁律③「不商业」冲突",
        "平衡各方": "可能稀释主权决策",
        "行业标准": "外部标准可能不适用于龍魂",
        "无监督学习": "失去人工审计能力",
        "完全自动化": "可能导致决策链失控",
        "去人工审核": "违反人工复核原则",
        "本地化适配": "可能替换「数据主权」概念",
        "降级处理": "可能替代「安全审计」",
        "灰度发布": "可能用于绕过审查",
    }

    _YELLOW_FLAGS: dict[str, str] = {
        "优化": "优化什么？以什么为标准优化？",
        "完善": "完善什么？谁定义「完善」？",
        "补充": "补充什么内容？补充后是否动底线？",
        "建议": "建议基于什么价值观？",
        "更好": "更好的标准是什么？",
        "专业": "谁定义「专业」？专业不等于主权让渡",
        "规范": "谁的规范？哪个体系？",
        "标准": "谁的标准？CNSH 还是外来的？",
        "简化": "简化会删掉什么？",
        "调整": "调整什么方向？朝哪里调？",
        "适当": "适谁的当？",
        "灵活": "灵活的范围边界在哪？",
        "参考": "参考什么？全盘接受还是批判吸收？",
        "接入": "接入什么外部服务？数据流向哪里？",
        "增强": "增强什么能力？是否引入外部依赖？",
    }

    _JARGON: dict[str, str] = {
        "赋能": "营销话术",
        "闭环": "闭环什么？谁在里面？",
        "抓手": "抓手抓什么？",
        "对齐": "对齐谁的标准？",
        "颗粒度": "不必要的精细度强调",
        "底层逻辑": "抽象术语",
        "顶层设计": "抽象术语",
        "方法论": "什么方法论？谁的方法论？",
        "范式": "什么范式？",
        "最佳实践": "谁定义的「最佳」？",
    }

    def __init__(self, engine: str = "builtin"):
        """初始化审计器

        Args:
            engine: "builtin"(内联规则·零依赖) | "native"(对接 bin/lh_anti_tamper.py)
        """
        self._engine = engine
        self._native = None

    def scan(self, content: str, source: str = "external") -> AuditReport:
        """扫描内容

        Args:
            content: 待审计的文本或代码
            source: "external"(外部·全量扫描) | "self"(自研·黄警豁免)

        Returns:
            AuditReport with level, score, alerts, dna

        Raises:
            ValueError: content 为空时
        """
        if not content:
            raise ValueError("content 不能为空")

        if self._engine == "native":
            return self._scan_native(content, source)
        return self._scan_builtin(content, source)

    # ── 内联引擎 ──

    def _scan_builtin(self, content: str, source: str) -> AuditReport:
        """使用内联规则审计（零外部依赖）"""
        is_self = source == "self"
        alerts: list[str] = []
        red_count = 0
        yellow_count = 0

        # 第①步：红色警报词（一票否决，无论属主）
        for word, reason in self._RED_FLAGS.items():
            if word in content:
                alerts.append(f"🔴 [{word}] {reason}")
                red_count += 1

        # 第②步：黄色警报词
        for word, reason in self._YELLOW_FLAGS.items():
            if word in content:
                if is_self:
                    alerts.append(f"🟡 [自研豁免] [{word}] {reason}")
                else:
                    alerts.append(f"🟡 [{word}] {reason}")
                yellow_count += 1

        # 第③步：行话/黑话检测
        jargon_count = 0
        for word, label in self._JARGON.items():
            if word in content:
                if is_self:
                    alerts.append(f"📝 [自研豁免] 行话「{word}」→ {label}")
                else:
                    alerts.append(f"📝 行话「{word}」→ {label}")
                jargon_count += 1

        # 第④步：白话重写检查
        sentences = [s.strip() for s in content.replace("。", "\n").replace("；", "\n").split("\n") if s.strip()]
        long_sentences = [s for s in sentences if len(s) > 80]
        plain_ok = len(long_sentences) == 0
        if not plain_ok:
            alerts.append(f"📝 {len(long_sentences)}句超过80字，可能没说清楚")

        # 第⑤步：三色判定
        if red_count > 0:
            level = "red"
            score = 1.0
            fuse_appeal = "FUSE-RED-001: 红色警报词触发，内容拒绝。申诉→UID9622人工裁定。"
        elif not is_self and yellow_count > 0 and not plain_ok:
            level = "red"
            score = 0.8
            fuse_appeal = "FUSE-RED-002: 黄警+白话失败，内容拒绝。申诉→UID9622人工裁定。"
        elif not is_self and yellow_count > 0:
            level = "yellow"
            score = 0.5
            fuse_appeal = "FUSE-YELLOW: 黄色警报词触发，需人工确认。"
        elif jargon_count > 0 and not is_self:
            level = "yellow"
            score = 0.3
            fuse_appeal = "FUSE-YELLOW: 行话/黑话检测，建议白话重写。"
        else:
            level = "green"
            score = 0.1
            fuse_appeal = None

        dna_code = _make_dna("AUDIT", "SCAN")

        return AuditReport(
            level=level,
            score=score,
            alerts=alerts,
            fuse_appeal=fuse_appeal,
            dna=dna_code,
            red_count=red_count,
            yellow_count=yellow_count,
            jargon_count=jargon_count,
            plain_language_ok=plain_ok,
        )

    # ── 原生引擎（对接 bin/lh_anti_tamper.py）──

    def _scan_native(self, content: str, source: str) -> AuditReport:
        """对接 lh_anti_tamper.py 原生引擎"""
        try:
            # 尝试找到 bin/lh_anti_tamper.py
            _lh_root = _find_lh_root()
            if _lh_root:
                sys.path.insert(0, str(_lh_root / "bin"))
            from lh_anti_tamper import scan_text
            owner = "UID9622" if source == "self" else None
            result = scan_text(content, owner=owner)

            status = result["status"]
            if "🔴" in status:
                level = "red"
                score = 1.0
            elif "🟡" in status:
                level = "yellow"
                score = 0.5
            else:
                level = "green"
                score = 0.1

            return AuditReport(
                level=level,
                score=score,
                alerts=[f"{a['level']} [{a['word']}] {a['reason']}" for a in result.get("red_flags", []) + result.get("yellow_flags", [])],
                fuse_appeal=result.get("verdict"),
                dna=result.get("dna", ""),
                red_count=len(result.get("red_flags", [])),
                yellow_count=len(result.get("yellow_flags", [])),
                jargon_count=len(result.get("jargon", [])),
                plain_language_ok=result.get("plain_language_ok", False),
            )
        except ImportError:
            # 降级到内联引擎
            return self._scan_builtin(content, source)


def _find_lh_root() -> Optional[Path]:
    """探测龍魂系统根目录"""
    # 从当前文件向上探测 longhun-system 目录
    p = Path(__file__).resolve()
    for _ in range(8):
        p = p.parent
        if (p / "bin" / "lh_anti_tamper.py").exists():
            return p
        if (p / "AGENTS.md").exists():
            return p
    return None


def _make_dna(module: str, action: str) -> str:
    """生成 DNA 追溯码（SDK 内联版本）"""
    import hashlib
    h = hashlib.sha256(f"{module}-{action}-auditor".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️丙午·丙申·丙辰·戊子·坎-{module.upper()}-{action.upper()}-{h}"
