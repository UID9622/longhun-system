# CNSH L3 Extension Registry
# 私域/公域边界判定 + 扩展处理器注册表

from .entry    import RegistryEntry, Scope, ExtType
from .boundary import register_private, register_public, register_extension, check_boundary
from .store    import lookup_ext, lookup_dna, get_chain, verify_chain
from .verify   import verify_gpg_sig, verify_entry_hash
