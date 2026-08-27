# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# M75 · 龍魂全系统渲染变量环境 · AI 的眼睛 · 本地 + 鲲鹏双主权
"""render 包：CNSH 渲染指令 → 平台渲染 → {render.*} 变量环境 → DNA/审计/主权边界。"""

__version__ = "1.0.0"
__uid__ = "UID9622"

from .orchestrator import LHRenderOrchestrator
from .core.variables import RenderContext

__all__ = ["LHRenderOrchestrator", "RenderContext", "__version__", "__uid__"]
