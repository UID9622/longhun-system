"""
🐉 龍魂主权技术栈 · 统一 SDK v1.0
一个包装齐：DNA追溯 + 三色审计 + 15条国产替代规则 + CNSH桥
一个账号 = 龍魂生态全部服务（人格工具 + 知识库 + 搜索 + API）
零三方依赖 · 即装即用

DNA: #龍芯⚡️2026-08-31-LONGHUN-SDK-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

__version__ = "1.0.0"
__dna__ = "#龍芯⚡️2026-08-31-LONGHUN-SDK-V1.0-UID9622"
__author__ = "诸葛鑫 | UID9622 · 龍芯北辰"
__license__ = "MulanPSL v2"

from .dna import generate_dna, dna_stamp
from .tricolor import audit, tricolor_status
from .evaluator import scan_text, RULES

__all__ = [
    "__version__", "__dna__", "__author__", "__license__",
    "generate_dna", "dna_stamp",
    "audit", "tricolor_status",
    "scan_text", "RULES",
]
