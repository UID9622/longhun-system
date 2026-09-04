"""
🐉 CNSH 运行桥 v1.0
统一入口：longhun cnsh run <file.cnsh>
本机有 CNSH 运行时 → 直接调用（08_BIN/cnsh/interpreter.py 或 cnsh 命令）
没有 → 清晰提示安装路径（零黑箱）

DNA: #龍芯⚡️2026-08-31-LONGHUN-CNSH-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# 已知的 CNSH 解释器路径（按优先级）
CANDIDATES = [
    os.environ.get("LONGHUN_CNSH_PATH", ""),
    str(Path.home() / "longhun-system/08_BIN/cnsh/interpreter.py"),
    str(Path.home() / "longhun-system/bin/lh.py"),
]


def _find_interpreter():
    for cand in CANDIDATES:
        if cand and Path(cand).exists():
            return cand
    if shutil.which("cnsh"):
        return "cnsh"
    return None


def run_cnsh(file_or_code, use_code: bool = False) -> dict:
    """运行 CNSH 文件或内联代码"""
    interpreter = _find_interpreter()
    if not interpreter:
        return {
            "ok": False,
            "error": (
                "未找到 CNSH 运行时。请任选其一：\n"
                "  1) 安装: pip install cnsh-suite\n"
                "  2) 设置: export LONGHUN_CNSH_PATH=/path/to/cnsh/interpreter.py\n"
                "  3) 克隆: https://github.com/UID9622/CNSH"
            ),
        }
    cmd = [sys.executable, interpreter, "--code", file_or_code] if use_code \
        else [sys.executable, interpreter, file_or_code]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return {
            "ok": proc.returncode == 0,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "exit_code": proc.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "CNSH 运行超时（30s）"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
