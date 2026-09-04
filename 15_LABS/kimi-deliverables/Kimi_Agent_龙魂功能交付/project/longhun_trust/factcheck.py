# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-8e01a846
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""龍魂信任核心 · 事实校验引擎（三级纠正 + 熔断）。

任何时间/身份/数字类输入必须先验证再使用；不一致必须主动发起纠正；
纠正全程留痕。矛盾计数存内存并落盘 <LONGHUN_HOME>/08_STATE/factcheck_state.json。
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Any

from .audit import AuditLog
from .dna import generate_dna
from .exceptions import CircuitBreakerTripped

DEFAULT_IDENTITY_REGISTRY: dict[str, int] = {"UID9622": 0}
"""默认身份注册表：创始人 UID9622 为 L0。"""


class CorrectionLevel(Enum):
    """纠正级别。"""

    LIGHT = "light"  # 格式/拼写类：自动修正 + 通知
    STANDARD = "standard"  # 事实性数值/时间/身份不一致：给纠正提议，待用户确认
    SEVERE = "severe"  # 身份仿冒/广泛矛盾：熔断冻结


@dataclass
class CheckResult:
    """一次事实校验的结果。"""

    valid: bool
    claim: Any
    actual: Any
    status: str
    level: CorrectionLevel | None
    message: str
    dna: str
    timestamp: str


class FactCheckEngine:
    """事实校验引擎：三级纠正 + 矛盾计数熔断。"""

    def __init__(
        self,
        audit: AuditLog | None = None,
        breaker_threshold: int = 3,
    ) -> None:
        """初始化事实校验引擎。

        :param audit: 审计日志，默认 ``AuditLog("fact_check")``。
        :param breaker_threshold: 熔断阈值，同一字段矛盾计数达到即熔断。
        """
        self.audit: AuditLog = audit if audit is not None else AuditLog("fact_check")
        self.breaker_threshold: int = breaker_threshold
        self._state_dir: Path = (
            Path(os.environ.get("LONGHUN_HOME", Path.home() / ".longhun")) / "08_STATE"
        )
        self._state_path: Path = self._state_dir / "factcheck_state.json"
        self._counts: dict[str, int] = self._load_state()

    def _load_state(self) -> dict[str, int]:
        """从落盘状态文件读取矛盾计数。

        文件不存在 → 空表；文件损坏 → raise ValueError
        （绝不把坏文件静默视为空表，否则等于静默解冻熔断字段）。

        :return: 字段矛盾计数字典。
        :raises ValueError: 状态文件存在但无法解析为计数字典。
        """
        try:
            text = self._state_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return {}
        except OSError as exc:
            raise ValueError(f"factcheck 状态文件读取失败：{self._state_path}") from exc
        try:
            data = json.loads(text)
            if not isinstance(data, dict):
                raise ValueError("顶层不是字典")
            return {str(k): int(v) for k, v in data.items()}
        except (ValueError, TypeError) as exc:
            raise ValueError(
                f"factcheck 状态文件损坏：{self._state_path}（{exc}）"
            ) from exc

    def _reload_for_merge(self) -> dict[str, int]:
        """计数变更前 reload 磁盘状态（跨实例不丢更新），写路径 fail-closed。

        磁盘文件**存在但损坏** → 先写审计 ``STATE_CORRUPT_WRITE_REFUSED``
        再 raise ValueError：绝不把陈旧内存态回写落盘（那会把盘上更高的
        计数/熔断态洗掉）。内存保守态只允许用于只读查询（is_frozen），
        绝不允许进入写路径。文件不存在（全新）→ 正常初始化，不算损坏。

        :return: 磁盘上的计数字典。
        :raises ValueError: 状态文件存在但损坏，拒绝执行写路径。
        """
        try:
            return self._load_state()
        except ValueError as exc:
            self.audit.log(
                "STATE_CORRUPT_WRITE_REFUSED",
                {"reason": str(exc), "memory_counts": dict(self._counts)},
            )
            raise ValueError(
                f"factcheck 状态文件损坏，拒绝执行写路径（防止洗掉熔断态）："
                f"{self._state_path}"
            ) from exc

    def _save_state(self) -> None:
        """把矛盾计数落盘：临时文件 + os.replace 原子替换（容错：写失败不抛出）。"""
        try:
            self._state_dir.mkdir(parents=True, exist_ok=True)
            tmp_path = self._state_path.with_name(
                f"{self._state_path.name}.{os.getpid()}.tmp"
            )
            tmp_path.write_text(
                json.dumps(self._counts, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            os.replace(tmp_path, self._state_path)
        except OSError:
            pass

    def _bump(self, field_key: str) -> int:
        """字段矛盾计数 +1 并原子落盘；先 reload 磁盘合并，跨实例交替 bump 不丢更新。

        :param field_key: 字段键。
        :return: 增加后的计数。
        :raises ValueError: 状态文件存在但损坏（fail-closed，拒绝写入）。
        """
        disk = self._reload_for_merge()
        for key in set(disk) | set(self._counts):
            self._counts[key] = max(disk.get(key, 0), self._counts.get(key, 0))
        self._counts[field_key] = self._counts.get(field_key, 0) + 1
        self._save_state()
        return self._counts[field_key]

    def _make_result(
        self,
        valid: bool,
        claim: Any,
        actual: Any,
        status: str,
        level: CorrectionLevel | None,
        message: str,
    ) -> CheckResult:
        """构造 CheckResult，附带 DNA 追溯码与时间戳。"""
        return CheckResult(
            valid=valid,
            claim=claim,
            actual=actual,
            status=status,
            level=level,
            message=message,
            dna=generate_dna("FACTCHECK"),
            timestamp=datetime.now().isoformat(),
        )

    def validate_time_span(
        self,
        claim_years: int,
        start_year: int,
        reference: date | None = None,
    ) -> CheckResult:
        """校验时间跨度声称值。

        actual = reference.year - start_year。一致 → valid=True；
        不一致 → valid=False, level=STANDARD，写审计并计入该字段矛盾计数。

        :param claim_years: 声称的年数。
        :param start_year: 起始年份。
        :param reference: 参考日期，默认 date.today()（可注入便于测试）。
        :return: CheckResult。
        """
        ref = reference if reference is not None else date.today()
        actual = ref.year - start_year
        field_key = f"time_span:{start_year}"
        if claim_years == actual:
            return self._make_result(
                True,
                claim_years,
                actual,
                "🟢 一致",
                None,
                f"时间跨度一致：{actual} 年",
            )
        count = self._bump(field_key)
        self.audit.log(
            "FACT_MISMATCH",
            {
                "field": field_key,
                "claim": claim_years,
                "actual": actual,
                "level": CorrectionLevel.STANDARD.value,
                "contradiction_count": count,
            },
        )
        return self._make_result(
            False,
            claim_years,
            actual,
            "🟡 数据不一致",
            CorrectionLevel.STANDARD,
            f"实际应为 {actual} 年（声称 {claim_years} 年），请确认修正",
        )

    def validate_identity(
        self,
        subject: str,
        claimed_level: int,
        registry: dict[str, int] | None = None,
    ) -> CheckResult:
        """校验身份级别声称值。

        registry 默认 {"UID9622": 0}（创始人 L0）。一致 → valid=True；
        已知主体级别不符 → STANDARD；未知主体冒称 L0 → SEVERE + 触发熔断记录。

        :param subject: 主体标识。
        :param claimed_level: 声称的身份级别。
        :param registry: 身份注册表（主体 → 级别）。
        :return: CheckResult。
        """
        table = registry if registry is not None else dict(DEFAULT_IDENTITY_REGISTRY)
        field_key = f"identity:{subject}"
        if subject in table and table[subject] == claimed_level:
            return self._make_result(
                True,
                claimed_level,
                table[subject],
                "🟢 一致",
                None,
                f"身份一致：{subject} L{claimed_level}",
            )
        if subject not in table and claimed_level == 0:
            count = self._bump(field_key)
            # 身份仿冒 SEVERE：一次即冻结该字段（计数直接抬到熔断阈值）。
            if count < self.breaker_threshold:
                self._counts[field_key] = self.breaker_threshold
                self._save_state()
                count = self.breaker_threshold
            self.audit.log(
                "CIRCUIT_BREAKER",
                {
                    "field": field_key,
                    "subject": subject,
                    "claimed_level": claimed_level,
                    "level": CorrectionLevel.SEVERE.value,
                    "contradiction_count": count,
                },
            )
            return self._make_result(
                False,
                claimed_level,
                None,
                "🔴 身份仿冒风险",
                CorrectionLevel.SEVERE,
                f"未知主体 {subject} 冒称创始人 L0，已触发熔断记录",
            )
        actual_level = table.get(subject)
        count = self._bump(field_key)
        self.audit.log(
            "FACT_MISMATCH",
            {
                "field": field_key,
                "subject": subject,
                "claim": claimed_level,
                "actual": actual_level,
                "level": CorrectionLevel.STANDARD.value,
                "contradiction_count": count,
            },
        )
        return self._make_result(
            False,
            claimed_level,
            actual_level,
            "🟡 数据不一致",
            CorrectionLevel.STANDARD,
            f"身份级别不一致：{subject} 声称 L{claimed_level}，登记为 "
            f"{f'L{actual_level}' if actual_level is not None else '未知'}，请确认修正",
        )

    def confirm_correction(self, field_key: str, accepted: bool) -> dict:
        """用户确认/拒绝纠正提议；确认则清除该字段矛盾计数；写审计。

        :param field_key: 字段键。
        :param accepted: 用户是否接受纠正。
        :return: 处理记录字典。
        :raises ValueError: 状态文件存在但损坏（fail-closed，拒绝写入）。
        """
        disk = self._reload_for_merge()
        for key in set(disk) | set(self._counts):
            self._counts[key] = max(disk.get(key, 0), self._counts.get(key, 0))
        previous = self._counts.get(field_key, 0)
        if accepted:
            self._counts.pop(field_key, None)
            self._save_state()
        record = {
            "field_key": field_key,
            "accepted": accepted,
            "previous_count": previous,
            "cleared": bool(accepted and previous > 0),
            "contradiction_count": self._counts.get(field_key, 0),
            "timestamp": datetime.now().isoformat(),
            "dna": generate_dna("FACTCHECK"),
        }
        self.audit.log(
            "CORRECTION_CONFIRMED" if accepted else "CORRECTION_REJECTED",
            {
                "field_key": field_key,
                "accepted": accepted,
                "previous_count": previous,
                "contradiction_count": record["contradiction_count"],
            },
        )
        return record

    def is_frozen(self, field_key: str) -> bool:
        """判断字段是否已熔断：矛盾计数 >= breaker_threshold → True。

        :param field_key: 字段键。
        :return: 是否熔断。
        """
        return self._counts.get(field_key, 0) >= self.breaker_threshold

    def check_or_raise(self, field_key: str) -> None:
        """字段已熔断则抛出 CircuitBreakerTripped，否则静默通过。

        :param field_key: 字段键。
        :raises CircuitBreakerTripped: 字段已熔断。
        """
        if self.is_frozen(field_key):
            raise CircuitBreakerTripped(
                f"字段 {field_key} 矛盾计数已达熔断阈值 "
                f"{self.breaker_threshold}，停止使用并升级人工"
            )
