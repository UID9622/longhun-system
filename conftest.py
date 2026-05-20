# pytest · 将包名 cnsh 映射到目录 CNSH（大小写目录名与 import 对齐）
from __future__ import annotations

import sys
import types
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_CNSH = _ROOT / "CNSH"

if _CNSH.is_dir() and "cnsh" not in sys.modules:
    pkg = types.ModuleType("cnsh")
    pkg.__path__ = [str(_CNSH)]
    pkg.__package__ = "cnsh"
    pkg.__file__ = str(_CNSH / "__init__.py")
    sys.modules["cnsh"] = pkg
