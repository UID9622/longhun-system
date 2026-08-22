#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂插件沙箱 · 插件侧 API v1.1
DNA: #龍芯⚡️2026-08-22-SANDBOX-API-v1.1
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

v1.1 修复（P77 实测：DNA 返回 None、MEMORY 假写、fs 越权读 ~/.gnupg 全放行）：
  1. 真执行：dna.generate / memory.append / fs.read / fs.write / audit.log
     由 handler 真正落地，消灭"假成功"。
  2. 路径锁死：fs.* 的 path 必须 resolve 后落在插件自身 sandbox/ 目录内，
     绝对路径/.. 逃逸/软链逃逸一律拒绝（D1 防护）。
  3. memory.append 防注入：换行清洗 + 长度上限 + 来源标记。
  4. 未落地能力（net.http / net.socket / agent.call / vision.call /
     voice.call / dna.verify）诚实返回 not_implemented，绝不假成功。
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

from .capability_gate import CapabilityGate, CapabilityRequest, CapabilityResponse
from .audit_hook import AuditHook, generate_dna

# 模块加载时捕获安全引用（import 守卫会替换 builtins.open，本模块必须用这份）
_safe_open = open

_MAX_FS_READ = 1 * 1024 * 1024       # fs.read 单文件 ≤ 1MB
_MAX_FS_WRITE = 512 * 1024           # fs.write 单次 ≤ 512KB
_MAX_MEMORY_APPEND = 500             # memory.append 内容 ≤ 500 字符（清洗换行）


class SandboxAPI:
    """
    插件侧唯一合法通信接口
    插件只能通过此对象与主系统交互 · 不能直接 import 核心模块
    """

    def __init__(self, plugin_id: str, gate: CapabilityGate, audit_hook: AuditHook):
        self._plugin_id = plugin_id
        self._gate = gate
        self._audit = audit_hook
        self._root = Path(__file__).resolve().parent.parent
        self._sandbox_dir = (self._root / "plugins" / plugin_id / "sandbox").resolve()
        self._sandbox_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 统一入口
    # ------------------------------------------------------------------

    def request(self, capability: str, action: str, payload: Dict[str, Any] = None,
                dna: Optional[str] = None) -> Dict[str, Any]:
        if payload is None:
            payload = {}
        req = CapabilityRequest(
            plugin_id=self._plugin_id, capability=capability,
            action=action, payload=payload, dna=dna)
        resp = self._gate.request(req)

        # 门控拒绝/未知：直接返回
        if resp.status != "ok":
            result = {"status": resp.status, "dna": resp.dna}
            if resp.status == "denied":
                result["error"] = resp.error
            else:
                result["error"] = resp.error
            return result

        # 门控通过 → 交给 handler 真执行
        try:
            data = self._dispatch(capability, action, payload)
            return {"status": "ok", "dna": resp.dna, "data": data}
        except PermissionError as e:
            self._audit.log(self._plugin_id, "CAPABILITY_VIOLATION",
                            f"{capability} payload 违规: {e}", "🔴",
                            extra={"action": action})
            return {"status": "denied", "dna": resp.dna, "error": str(e)}
        except NotImplementedError as e:
            self._audit.log(self._plugin_id, "CAPABILITY_NOT_IMPLEMENTED",
                            str(e), "🟡", extra={"action": action})
            return {"status": "not_implemented", "dna": resp.dna,
                    "message": str(e)}
        except Exception as e:
            self._audit.log(self._plugin_id, "CAPABILITY_HANDLER_ERROR",
                            f"{capability}: {e}", "🔴", extra={"action": action})
            return {"status": "error", "dna": resp.dna, "error": f"{e}"}

    # ------------------------------------------------------------------
    # handler 分发（真执行层）
    # ------------------------------------------------------------------

    def _dispatch(self, capability: str, action: str,
                  payload: Dict[str, Any]) -> Any:
        if capability == "dna.generate":
            return self._h_dna_generate(payload)
        if capability == "dna.verify":
            raise NotImplementedError("dna.verify 未落地（v1.1 仅门控）")
        if capability == "memory.append":
            return self._h_memory_append(payload)
        if capability == "fs.read":
            return self._h_fs_read(payload)
        if capability == "fs.write":
            return self._h_fs_write(payload)
        if capability == "fs.write_system":
            raise PermissionError("fs.write_system 永远拒绝（v1.0 不支持系统写入）")
        if capability == "audit.log":
            self._audit.log(self._plugin_id, "PLUGIN_AUDIT",
                            str(payload.get("content", ""))[:300], "🟡")
            return {"message": "已写入审计日志"}
        # 网络 / 代理 / 感知类：v1.1 仅门控，不执行
        if capability in ("net.http", "net.socket", "agent.call",
                          "vision.call", "voice.call"):
            raise NotImplementedError(f"{capability} 未落地（v1.1 仅门控不执行）")
        raise NotImplementedError(f"未知能力执行: {capability}")

    # --- dna.generate：真生成 ---

    def _h_dna_generate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        module = str(payload.get("module", "plugin"))[:32]
        action = str(payload.get("action", "call"))[:20]
        dna = generate_dna(module=f"{self._plugin_id}-{module}", action=action)
        self._audit.log(self._plugin_id, "DNA_GENERATED",
                        f"module={module} action={action}", "🟢",
                        extra={"dna": dna})
        return {"dna": dna, "message": "DNA 已生成"}

    # --- memory.append：真写 MEMORY.md（防注入） ---

    def _h_memory_append(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        content = str(payload.get("content", ""))
        source = str(payload.get("source", "plugin"))[:32]
        # 清洗：去换行（防伪造审计/协议行）、限长
        content = " ".join(content.split())[:_MAX_MEMORY_APPEND]
        if not content:
            raise PermissionError("memory.append 内容为空")
        entry = f"\n<!-- plugin:{self._plugin_id} source:{source} -->\n{content}\n"
        mem_path = self._root / "MEMORY.md"
        with _safe_open(mem_path, "a", encoding="utf-8") as f:
            f.write(entry)
        self._audit.log(self._plugin_id, "MEMORY_APPENDED",
                        f"source={source} len={len(content)}", "🟢")
        return {"message": "已写入 MEMORY.md", "length": len(content)}

    # --- fs.read / fs.write：路径锁死 + 真读写 ---

    def _resolve_in_sandbox(self, path: str) -> Path:
        """路径必须 resolve 后落在插件自身 sandbox/ 内 · 防 .. 和软链逃逸"""
        p = Path(path)
        if not p.is_absolute():
            p = (self._sandbox_dir / p).resolve()
        else:
            p = p.resolve()
        if p != self._sandbox_dir and not str(p).startswith(
                str(self._sandbox_dir) + os.sep):
            raise PermissionError(f"路径越界（只能访问插件自身 sandbox/）: {path}")
        return p

    def _h_fs_read(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        path = str(payload.get("path", ""))
        if not path:
            raise PermissionError("fs.read 缺少 path")
        target = self._resolve_in_sandbox(path)
        if not target.exists():
            raise PermissionError(f"文件不存在: {path}")
        if target.is_dir():
            raise PermissionError(f"v1.1 不支持读目录: {path}")
        size = target.stat().st_size
        if size > _MAX_FS_READ:
            raise PermissionError(f"文件过大 ({size}B > {_MAX_FS_READ}B): {path}")
        with _safe_open(target, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        self._audit.log(self._plugin_id, "FS_READ",
                        f"read {path} ({size}B)", "🟢")
        return {"content": content, "size": size, "path": str(target.relative_to(self._sandbox_dir))}

    def _h_fs_write(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        path = str(payload.get("path", ""))
        content = payload.get("content", "")
        if not path:
            raise PermissionError("fs.write 缺少 path")
        if not isinstance(content, str):
            content = json.dumps(content, ensure_ascii=False)
        if len(content.encode("utf-8")) > _MAX_FS_WRITE:
            raise PermissionError(f"内容过大 (> {_MAX_FS_WRITE}B)")
        target = self._resolve_in_sandbox(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with _safe_open(target, "w", encoding="utf-8") as f:
            f.write(content)
        self._audit.log(self._plugin_id, "FS_WRITE",
                        f"write {path} ({len(content)}B)", "🟢")
        return {"message": "已写入", "path": str(target.relative_to(self._sandbox_dir))}

    # ------------------------------------------------------------------
    # 便捷方法
    # ------------------------------------------------------------------

    def request_memory_append(self, content: str, source: str = "plugin") -> Dict[str, Any]:
        return self.request("memory.append", "append",
                            {"content": content, "source": source})

    def request_dna_generate(self, module: str, action: str) -> Dict[str, Any]:
        return self.request("dna.generate", "generate",
                            {"module": module, "action": action})

    def request_agent_call(self, tool: str, args: Dict) -> Dict[str, Any]:
        return self.request("agent.call", "call", {"tool": tool, "args": args})

    def request_fs_read(self, path: str) -> Dict[str, Any]:
        return self.request("fs.read", "read", {"path": path})

    def request_fs_write(self, path: str, content: str) -> Dict[str, Any]:
        return self.request("fs.write", "write", {"path": path, "content": content})
