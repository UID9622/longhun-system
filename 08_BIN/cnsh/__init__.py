# 🐉 CNSH 模块入口 v1.3
# DNA: #龍芯⚡️2026-08-31-CNSH-INIT-v1.3-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# v1.3 新增: DeepSeek 参考版 API 兼容层（CNSSHLexer 三S别名·eval_expr·OP_MAP）
from .lexer import CNSHLexer, CNSSHLexer, CNSHToken
from .var_env import CNSHVarEnv
from .interpreter import CNSHInterpreter
from .dna_verify import verify_dna_header, verify_dna_file, batch_verify

__version__ = '1.3'
__dna__ = '#龍芯⚡️2026-08-31-CNSH-INIT-v1.3-UID9622'
# CNSSHLexer = DeepSeek 参考版类名（三S）兼容别名，与 CNSHLexer 同一实现
__all__ = ['CNSHLexer', 'CNSSHLexer', 'CNSHVarEnv', 'CNSHInterpreter',
           'verify_dna_header', 'verify_dna_file', 'batch_verify']
