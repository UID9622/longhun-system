# DNA: #龍芯⚡️丙午·丙申·甲子·甲戌·䷍大有-CODE-补DNA-d0331ca0
"""龍魂信任核心 · DNA 生成与确认码闸门。

铁律：永不手写干支/卦名。生成器不可用时一律使用日期占位标签兜底。
"""

from __future__ import annotations

import hmac
import os
import re
import subprocess
from datetime import date
from pathlib import Path

from .exceptions import ConfirmCodeError

CONFIRM_CODE: str = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
"""确认码：破坏性操作（回滚/覆盖/清除）必须过闸门。"""

GPG_FINGERPRINT: str = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
"""GPG 指纹（仅作元数据展示）。"""

DNA_PLACEHOLDER_TAG: str = "【干支待本地生成器校准】"
"""DNA 占位标签：生成器不可用时兜底，绝不手写干支。"""

_GENERATOR_TIMEOUT_SECONDS: int = 5
"""外部 DNA 生成器子进程超时（秒）。"""


def _normalize_action_tag(action_tag: str) -> str:
    """规范化动作标签：统一大写，连续空白转 '-'。

    :param action_tag: 原始动作标签。
    :return: 规范化后的标签。
    """
    return re.sub(r"\s+", "-", action_tag.strip()).upper()


def _find_generator() -> Path | None:
    """按优先级查找本地 DNA 生成器脚本。

    优先级：$LONGHUN_DNA_GENERATOR → ./bin/lh_dna_generator.py →
    ~/longhun-system/bin/lh_dna_generator.py。

    :return: 找到则返回脚本路径，否则 None。
    """
    candidates: list[Path] = []
    env_path = os.environ.get("LONGHUN_DNA_GENERATOR")
    if env_path:
        candidates.append(Path(env_path))
    candidates.append(Path("bin") / "lh_dna_generator.py")
    candidates.append(Path.home() / "longhun-system" / "bin" / "lh_dna_generator.py")
    for candidate in candidates:
        try:
            if candidate.is_file():
                return candidate
        except OSError:
            continue
    return None


def generate_dna(action_tag: str, version: str = "v1.0") -> str:
    """生成追溯码（DNA）。

    找到本地生成器则以子进程调用
    ``python3 <gen> --action <tag> --version <ver>``，取 stdout 首行，
    校验非空且以 '#龍芯' 开头；失败/超时(5s)一律兜底为日期占位串，
    永不手写干支。

    :param action_tag: 动作标签（统一 upper，空白转 '-'）。
    :param version: 版本标签，默认 "v1.0"。
    :return: DNA 追溯码字符串。
    """
    tag = _normalize_action_tag(action_tag)
    generator = _find_generator()
    if generator is not None:
        try:
            proc = subprocess.run(
                ["python3", str(generator), "--action", tag, "--version", version],
                capture_output=True,
                text=True,
                timeout=_GENERATOR_TIMEOUT_SECONDS,
                check=False,
            )
            lines = proc.stdout.splitlines()
            first_line = lines[0].strip() if lines else ""
            if proc.returncode == 0 and first_line.startswith("#龍芯"):
                return first_line
        except (subprocess.TimeoutExpired, OSError):
            pass
    return f"#龍芯⚡️{date.today().isoformat()}-{tag}-{version}-{DNA_PLACEHOLDER_TAG}"


def verify_confirm_code(code: str) -> None:
    """校验确认码；不匹配即抛出 ConfirmCodeError。

    比较使用 hmac.compare_digest，防时序侧信道。

    :param code: 待校验的确认码。
    :raises ConfirmCodeError: 确认码不匹配。
    """
    if not hmac.compare_digest(
        code.encode("utf-8"), CONFIRM_CODE.encode("utf-8")
    ):
        raise ConfirmCodeError("确认码错误：破坏性操作（回滚/覆盖/清除）被拒绝")
