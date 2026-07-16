# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-ENGINE-FOUNDATION_WRAPPERS-FILE1-v1.0-2
# 君子協議: 本文件受龍魂DNA追溯保護

"""
龍魂底座 API 封裝層
將 longhun-audit-integrated、longhun-shield、cnsh-aligner、instruction-protocol
封裝為 control-panel 可調用的 API。
"""
import json
import re
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[2]
SHIELD_DIR = ROOT / "skills" / "longhun-shield"
if str(SHIELD_DIR) not in sys.path:
    sys.path.insert(0, str(SHIELD_DIR))


def _run(cmd: List[str], cwd: Path = None, input_text: str | None = None, timeout: int = 60) -> Dict[str, Any]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd or ROOT),
            input=input_text,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"returncode": -1, "stdout": "", "stderr": "timeout"}
    except Exception as e:
        return {"returncode": -1, "stdout": "", "stderr": str(e)}


def _extract_json(text: str) -> Any:
    """從 stdout 中提取最後一個 JSON 對象"""
    try:
        # 找最後一個 `{` 開始的區塊
        matches = list(re.finditer(r'\{', text))
        for m in reversed(matches):
            try:
                return json.loads(text[m.start():])
            except Exception:
                continue
    except Exception:
        pass
    return None


def run_integrated_audit(mode: str = "system", target_file: str | None = None) -> Dict[str, Any]:
    """調用 longhun_audit_integrated.py"""
    cwd = ROOT / "skills" / "longhun-audit-integrated"
    cmd = [sys.executable, "longhun_audit_integrated.py", f"--{mode}"]
    if target_file and mode == "script":
        cmd.extend(["--file", target_file])
    result = _run(cmd, cwd=cwd)
    data = _extract_json(result["stdout"])
    return {
        "mode": mode,
        "json": data,
        "raw_stdout": result["stdout"][:2000],
        "raw_stderr": result["stderr"][:500],
    }


def run_shield(action: str, file_name: str, options: List[str] = None) -> Dict[str, Any]:
    """調用 longhun_shield_cli.py"""
    cwd = ROOT / "skills" / "longhun-shield"
    cmd = [sys.executable, "longhun_shield_cli.py", action, file_name]
    if options:
        cmd.extend(options)
    result = _run(cmd, cwd=cwd)
    return {
        "action": action,
        "file": file_name,
        "stdout": result["stdout"][:3000],
        "stderr": result["stderr"][:500],
    }


def run_cnsh_align(input_text: str, context: str = "stdin") -> Dict[str, Any]:
    """調用 cnsh_aligner.py"""
    cwd = ROOT / "skills" / "cnsh-aligner"
    result = _run([sys.executable, "cnsh_aligner.py"], cwd=cwd, input_text=input_text)
    return {
        "context": context,
        "stdout": result["stdout"][:3000],
        "stderr": result["stderr"][:500],
    }


def run_script_manager() -> Dict[str, Any]:
    """調用 script_manager.py"""
    cwd = ROOT / "skills" / "cnsh-aligner"
    result = _run([sys.executable, "script_manager.py"], cwd=cwd)
    return {
        "stdout": result["stdout"][:3000],
        "stderr": result["stderr"][:500],
    }


def run_foundation(action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """統一調度所有底座能力"""
    try:
        if action == "shield.check":
            return run_shield("check", payload.get("file", "shield_test_example.py"), payload.get("options", []))
        if action == "shield.analyze":
            return run_shield("analyze", payload.get("file", "shield_test_example.py"), payload.get("options", []))
        if action == "shield.validate":
            return run_shield("validate", payload.get("file", "shield_test_example.py"), payload.get("options", []))
        if action == "cnsh.align":
            return run_cnsh_align(payload.get("text", ""), payload.get("context", "stdin"))
        if action == "cnsh.script-manager":
            return run_script_manager()
        if action == "audit.integrated":
            return run_integrated_audit(payload.get("mode", "system"), payload.get("file"))
        if action == "instruction.execute":
            return run_instruction(payload.get("instruction", ""))
        return {"status": "error", "error": f"unknown foundation action: {action}"}
    except Exception as e:
        return {"status": "error", "error": str(e), "trace": traceback.format_exc()}


def run_instruction(instruction: str) -> Dict[str, Any]:
    """解析並執行 @shield.check file 類指令"""
    from longhun_shield_instruction_protocol import InstructionSyntax

    try:
        inst_id, params = InstructionSyntax.parse(instruction)
    except Exception as e:
        return {"status": "error", "error": f"parse failed: {e}"}

    if inst_id == "shield.check":
        file_name = params.get("file", "shield_test_example.py")
        return {"status": "ok", "instruction": instruction, "result": run_shield("check", file_name)}
    if inst_id == "shield.analyze":
        file_name = params.get("file", "shield_test_example.py")
        return {"status": "ok", "instruction": instruction, "result": run_shield("analyze", file_name)}
    if inst_id == "shield.validate":
        file_name = params.get("file", "shield_test_example.py")
        return {"status": "ok", "instruction": instruction, "result": run_shield("validate", file_name)}

    return {"status": "ok", "instruction": instruction, "parsed": {"id": inst_id, "params": params}}
