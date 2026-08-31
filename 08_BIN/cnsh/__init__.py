# 🐉 CNSH 模块入口 v1.2
# DNA: #龍芯⚡️2026-08-31-CNSH-INIT-v1.2-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
from .lexer import CNSHLexer
from .var_env import CNSHVarEnv
from .interpreter import CNSHInterpreter
from .dna_verify import verify_dna_header, verify_dna_file, batch_verify

__version__ = '1.2'
__dna__ = '#龍芯⚡️2026-08-31-CNSH-INIT-v1.2-UID9622'
__all__ = ['CNSHLexer', 'CNSHVarEnv', 'CNSHInterpreter',
           'verify_dna_header', 'verify_dna_file', 'batch_verify']
