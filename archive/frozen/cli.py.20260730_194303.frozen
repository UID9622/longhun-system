#龍芯⚡️2026-06-18-CNSH-CLI-v1.0
"""
通心译 | TongXinYi: CNSH Console Entry Point
龍魂体系·命令行入口 — `cnsh-launch` 控制台脚本

This module is the public console-script entry point for the packaged
CNSH runtime. It ensures the bundled CNSH tree is on `sys.path`, then
delegates to the original launcher.
"""
# 🟢 君子协议 | JunZi Protocol: CC BY-NC-SA 4.0
# 🟡 AI Truth Protocol: All outputs must be verifiable and traceable
# 🔴 DNA Trace: #龍芯⚡️2026-06-18-CNSH-CLI-v1.0

import os
import sys


def _ensure_cnsh_path():
    """Add the bundled CNSH root to sys.path so absolute imports work."""
    cnsh_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cnsh")
    if cnsh_root not in sys.path:
        sys.path.insert(0, cnsh_root)
    return cnsh_root


def main():
    """Public entry point for the `cnsh-launch` console script."""
    _ensure_cnsh_path()

    # Import the original launcher. Because the CNSH root is on sys.path,
    # absolute imports inside the launcher (e.g. `runtime.启动器`) resolve
    # to the bundled modules.
    try:
        import 启动龍魂体系
    except Exception as exc:  # pragma: no cover
        print(f"[cnsh-runtime] 🔴 启动入口导入失败: {exc}", file=sys.stderr)
        raise

    # The original launcher exposes `主函数()` as its interactive entry point.
    if hasattr(启动龍魂体系, "主函数"):
        启动龍魂体系.主函数()
    else:
        raise RuntimeError("启动龍魂体系.py does not expose 主函数()")


if __name__ == "__main__":
    main()
