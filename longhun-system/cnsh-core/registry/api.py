"""
CNSH L3 Registry API — FastAPI 路由

挂载路径：/registry

端点：
  POST /registry/register              — 注册条目（私域/公域）
  POST /registry/ext                   — 注册扩展处理器（便捷）
  GET  /registry/lookup/ext/{ext_id}   — 查找扩展处理器
  GET  /registry/lookup/dna/{dna_code} — 按 DNA 码查找
  GET  /registry/boundary/{dna_code}   — 边界状态查询
  GET  /registry/chain/{dna_code}      — 链式追溯
  GET  /registry/extensions            — 列出所有扩展
  GET  /registry/public                — 列出公域条目
  GET  /registry/verify                — 链完整性验证

Author: 诸葛鑫 (UID9622)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from .boundary  import register_private, register_public, register_extension, check_boundary
from .store     import lookup_ext, lookup_dna, get_chain, list_public_entries, verify_chain, list_extensions, deactivate_entry
from .verify    import verify_entry_hash

router = APIRouter(prefix="/registry", tags=["L3-Registry"])


# ── 请求模型 ──────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    content:      str
    scope:        str  = "PUBLIC"
    owner_gpg:    str  = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    ext_id:       str  = ""
    ext_type:     str  = ""
    handler_path: str  = ""
    description:  str  = ""
    version:      str  = "1.0.0"
    skip_ethics:  bool = False


class ExtRegisterRequest(BaseModel):
    ext_id:       str
    handler_path: str
    ext_type:     str  = "PLUGIN"
    description:  str  = ""
    version:      str  = "1.0.0"
    scope:        str  = "PUBLIC"
    owner_gpg:    str  = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    skip_ethics:  bool = False


# ── 端点 ──────────────────────────────────────────────────────────

@router.post("/register")
def register(req: RegisterRequest):
    """注册新条目（私域 or 公域）"""
    scope = req.scope.upper()

    if scope == "PRIVATE":
        entry = register_private(
            content      = req.content,
            owner_gpg    = req.owner_gpg,
            ext_id       = req.ext_id,
            ext_type     = req.ext_type,
            handler_path = req.handler_path,
            description  = req.description,
            version      = req.version,
        )
        return {"status": "ok", "scope": "PRIVATE", "entry": entry.to_dict()}

    elif scope == "PUBLIC":
        entry, err = register_public(
            content      = req.content,
            owner_gpg    = req.owner_gpg,
            ext_id       = req.ext_id,
            ext_type     = req.ext_type,
            handler_path = req.handler_path,
            description  = req.description,
            version      = req.version,
            skip_ethics  = req.skip_ethics,
        )
        if err:
            raise HTTPException(status_code=403, detail=err)
        return {"status": "ok", "scope": "PUBLIC", "entry": entry.to_dict()}

    else:
        raise HTTPException(status_code=400, detail=f"无效scope: {scope}，必须是 PRIVATE 或 PUBLIC")


@router.post("/ext")
def register_ext(req: ExtRegisterRequest):
    """注册扩展处理器（EXT[ext_id] 路由用）"""
    entry, err = register_extension(
        ext_id       = req.ext_id,
        handler_path = req.handler_path,
        ext_type     = req.ext_type,
        description  = req.description,
        version      = req.version,
        scope        = req.scope,
        owner_gpg    = req.owner_gpg,
        skip_ethics  = req.skip_ethics,
    )
    if err:
        raise HTTPException(status_code=403, detail=err)
    return {"status": "ok", "entry": entry.to_dict()}


@router.get("/lookup/ext/{ext_id:path}")
def lookup_extension(ext_id: str):
    """查找扩展处理器"""
    entry = lookup_ext(ext_id)
    if not entry:
        raise HTTPException(status_code=404, detail=f"扩展未注册: {ext_id}")
    return {"found": True, "entry": entry.to_dict()}


@router.get("/lookup/dna/{dna_code:path}")
def lookup_by_dna(dna_code: str):
    """按 DNA 码查找条目"""
    entry = lookup_dna(dna_code)
    if not entry:
        raise HTTPException(status_code=404, detail=f"DNA未找到: {dna_code}")
    ok, msg = verify_entry_hash(entry)
    return {
        "found":       True,
        "integrity":   msg,
        "hash_ok":     ok,
        "entry":       entry.to_dict(),
    }


@router.get("/boundary/{dna_code:path}")
def boundary_check(dna_code: str):
    """私域/公域边界查询"""
    return check_boundary(dna_code)


@router.get("/chain/{dna_code:path}")
def chain_trace(dna_code: str, depth: int = 20):
    """链式追溯（从指定 DNA 向前）"""
    chain = get_chain(dna_code, max_depth=depth)
    return {
        "dna_code":  dna_code,
        "depth":     len(chain),
        "chain":     [e.to_dict() for e in chain],
    }


@router.get("/extensions")
def list_exts(ext_type: str = "", active_only: bool = True, limit: int = 100):
    """列出扩展注册表"""
    entries = list_extensions(ext_type=ext_type, active_only=active_only, limit=limit)
    return {
        "total":   len(entries),
        "entries": [e.to_dict() for e in entries],
    }


@router.get("/public")
def list_public(limit: int = 50):
    """列出最新公域条目"""
    entries = list_public_entries(limit=limit)
    return {"total": len(entries), "entries": [e.to_dict() for e in entries]}


@router.get("/verify")
def verify():
    """验证注册表链完整性"""
    return verify_chain()


@router.delete("/deactivate/{dna_code:path}")
def deactivate(dna_code: str):
    """停用条目（不删除，保留 DNA）"""
    ok = deactivate_entry(dna_code)
    if not ok:
        raise HTTPException(status_code=404, detail=f"DNA未找到或已停用: {dna_code}")
    return {"status": "ok", "deactivated": dna_code, "note": "条目已停用，DNA链保留"}
