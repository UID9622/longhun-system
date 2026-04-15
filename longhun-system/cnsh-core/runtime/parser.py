"""
CNSH Syntax Layer + Command Parser — L1 + L2
统一语法入口：所有操作必须经过此层，不允许绕过

语法规范：
  @DOMAIN:VERB  PARAMS{k=v, k2=v2}  FLAG[f1,f2]  EXT[ext.id]

规则：
  - @DOMAIN:VERB 必填，大小写不敏感（统一转大写）
  - PARAMS{} 可选，值可以是字符串/数字/布尔
  - FLAG[] 可选，逗号分隔的标志
  - EXT[] 可选，扩展ID（注册表查找用）
  - 顺序固定：@CMD → PARAMS → FLAG → EXT
  - 多余空格容忍
  - 值包含空格时用引号：PARAMS{title="龍魂系统 里程碑"}

Author: 诸葛鑫 (UID9622)
"""

import re
import time
from typing import Optional, Tuple
from .command import CNSHCommand, Domain

# ── 正则定义 ───────────────────────────────────────────────────────

# @DOMAIN:VERB
RE_CMD    = re.compile(r'@([A-Za-z][A-Za-z0-9_]*):([A-Za-z][A-Za-z0-9_]*)')

# PARAMS{...}
RE_PARAMS = re.compile(r'PARAMS\s*\{([^}]*)\}')

# FLAG[...]
RE_FLAGS  = re.compile(r'FLAG\s*\[([^\]]*)\]')

# EXT[...]
RE_EXT    = re.compile(r'EXT\s*\[([^\]]*)\]')

# 单个 k=v 解析（支持引号值）
RE_KV     = re.compile(r'(\w+)\s*=\s*(?:"([^"]*?)"|\'([^\']*?)\'|([^,}\s]+))')


# ── 类型转换 ───────────────────────────────────────────────────────

def _cast(val: str):
    """将字符串值智能转换为 Python 类型"""
    if val.lower() == 'true':  return True
    if val.lower() == 'false': return False
    if val.lower() in ('null', 'none', ''): return None
    try:
        if '.' in val: return float(val)
        return int(val)
    except ValueError:
        return val


# ── 解析器 ─────────────────────────────────────────────────────────

class CNSHParser:
    """
    L1 CNSH Syntax Layer + L2 Command Parser
    输入: 原始CNSH字符串
    输出: CNSHCommand 对象 或 ParseError
    """

    class ParseError(Exception):
        def __init__(self, msg: str, raw: str = ""):
            super().__init__(msg)
            self.raw = raw

    def parse(
        self,
        raw: str,
        user_id: str = "UID9622",
        session_id: str = "",
    ) -> CNSHCommand:
        """
        解析CNSH字符串 → CNSHCommand
        任何格式错误抛出 ParseError
        """
        text = raw.strip()

        if not text:
            raise self.ParseError("空指令", raw)

        if not text.startswith('@'):
            raise self.ParseError(
                f"CNSH语法错误：指令必须以 @DOMAIN:VERB 开头，收到: {text[:30]}",
                raw
            )

        # L1: 提取 @DOMAIN:VERB
        m = RE_CMD.search(text)
        if not m:
            raise self.ParseError(
                f"语法错误：无法解析 @DOMAIN:VERB，格式应为 @CALENDAR:ADD",
                raw
            )

        domain = m.group(1).upper()
        verb   = m.group(2).upper()

        # L2: 提取 PARAMS{}
        params = {}
        pm = RE_PARAMS.search(text)
        if pm:
            for kv in RE_KV.finditer(pm.group(1)):
                key = kv.group(1)
                val = kv.group(2) or kv.group(3) or kv.group(4) or ''
                params[key] = _cast(val)

        # L2: 提取 FLAG[]
        flags = []
        fm = RE_FLAGS.search(text)
        if fm:
            flags = [f.strip() for f in fm.group(1).split(',') if f.strip()]

        # L2: 提取 EXT[]
        ext_id = None
        em = RE_EXT.search(text)
        if em:
            ext_id = em.group(1).strip()

        return CNSHCommand(
            domain     = domain,
            verb       = verb,
            params     = params,
            flags      = flags,
            ext_id     = ext_id,
            raw        = raw,
            user_id    = user_id,
            session_id = session_id,
            timestamp  = time.time(),
        )

    def validate(self, cmd: CNSHCommand) -> Tuple[bool, str]:
        """
        基础语法校验（语义校验在后续层做）
        返回 (ok, reason)
        """
        if not cmd.domain:
            return False, "DOMAIN 不能为空"
        if not cmd.verb:
            return False, "VERB 不能为空"
        if len(cmd.domain) > 32:
            return False, f"DOMAIN 超长: {cmd.domain}"
        if len(cmd.verb) > 32:
            return False, f"VERB 超长: {cmd.verb}"
        return True, "OK"

    def format(self, cmd: CNSHCommand) -> str:
        """将 CNSHCommand 重新格式化为标准CNSH字符串"""
        parts = [f"@{cmd.domain}:{cmd.verb}"]
        if cmd.params:
            kv = ", ".join(
                f'{k}="{v}"' if isinstance(v, str) and ' ' in str(v)
                else f'{k}={v}'
                for k, v in cmd.params.items()
            )
            parts.append(f"PARAMS{{{kv}}}")
        if cmd.flags:
            parts.append(f"FLAG[{','.join(cmd.flags)}]")
        if cmd.ext_id:
            parts.append(f"EXT[{cmd.ext_id}]")
        return "  ".join(parts)


# ── 单例 ───────────────────────────────────────────────────────────

_parser = CNSHParser()

def parse(raw: str, user_id: str = "UID9622", session_id: str = "") -> CNSHCommand:
    """全局解析入口"""
    return _parser.parse(raw, user_id=user_id, session_id=session_id)

def parse_safe(raw: str, user_id: str = "UID9622") -> Tuple[Optional[CNSHCommand], Optional[str]]:
    """安全解析，不抛异常，返回 (cmd, error_msg)"""
    try:
        return _parser.parse(raw, user_id=user_id), None
    except CNSHParser.ParseError as e:
        return None, str(e)
