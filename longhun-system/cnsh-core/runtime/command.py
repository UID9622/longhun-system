"""
CNSH Command Object — L2 Command Parser 输出结构
CNSHCommand 是整个执行链的数据载体

CNSH语法格式：
  @DOMAIN:VERB  PARAMS{key=value, key2=value2}  FLAG[flag1,flag2]  EXT[ext.id]

示例：
  @CALENDAR:ADD  PARAMS{title=会议, mood=激动, city=北京}
  @DNA:VERIFY    PARAMS{user=UID9622}
  @ALGO:RUN      PARAMS{name=fractal, depth=4}  EXT[algo.fractal]
  @AI:INFER      PARAMS{model=qwen}  FLAG[stream]  EXT[ai.local]
  @RISK:ASSESS   PARAMS{R=0.5, U=0.3, I=0.2}

Author: 诸葛鑫 (UID9622)
DNA: #LONGHUN⚡️2026-03-23-CNSH-PARSER-v1.0
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum
import time


# ── 已知的CNSH域 ─────────────────────────────────────────────────

class Domain(str, Enum):
    CALENDAR = "CALENDAR"   # 日历/时空胶囊
    DNA      = "DNA"        # DNA链操作
    RISK     = "RISK"       # 风险评估
    ETHICS   = "ETHICS"     # 伦理检查
    AUDIT    = "AUDIT"      # 三色审计
    ALGO     = "ALGO"       # 算法生态
    AI       = "AI"         # AI模型生态
    PLUGIN   = "PLUGIN"     # 工具插件
    NODE     = "NODE"       # 计算节点
    SYSTEM   = "SYSTEM"     # 系统操作
    UNKNOWN  = "UNKNOWN"    # 未注册域（允许扩展）


# ── 命令对象 ──────────────────────────────────────────────────────

@dataclass
class CNSHCommand:
    """
    CNSH命令对象 — 解析后的结构化表示
    整个执行链（L1→L8）围绕此对象传递
    """
    # 核心字段（解析自语法）
    domain:    str              # @DOMAIN 部分，大写
    verb:      str              # :VERB 部分，大写
    params:    dict             # PARAMS{...} 键值对
    flags:     list             # FLAG[...] 标志列表
    ext_id:    Optional[str]    # EXT[...] 扩展ID

    # 执行上下文（运行时填充）
    raw:          str   = ""            # 原始CNSH字符串
    user_id:      str   = "UID9622"
    session_id:   str   = ""
    timestamp:    float = field(default_factory=time.time)

    # 执行结果（流水线填充）
    policy:       str   = ""       # allow / require_confirm / block
    risk_score:   float = 0.0
    audit_color:  str   = ""       # 🟢🟡🔴
    ethics_pass:  bool  = True
    blocked_by:   list  = field(default_factory=list)
    dna_trace:    str   = ""
    output:       Any   = None
    error:        str   = ""

    @property
    def full_cmd(self) -> str:
        return f"@{self.domain}:{self.verb}"

    @property
    def is_blocked(self) -> bool:
        return self.policy == "block" or not self.ethics_pass

    def summary(self) -> str:
        p = ", ".join(f"{k}={v}" for k,v in self.params.items())
        f = f"  FLAG[{','.join(self.flags)}]" if self.flags else ""
        e = f"  EXT[{self.ext_id}]" if self.ext_id else ""
        return f"@{self.domain}:{self.verb}  PARAMS{{{p}}}{f}{e}"
