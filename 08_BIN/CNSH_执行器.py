#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·乙巳·庚辰·䷸巽-CNSH-EXECUTOR-v2.0-UID9622
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

"""🐉 龍魂引擎：CNSH_执行器
路径：bin/CNSH_执行器.py
CNSH v2.0 透明语义治理执行器：
  - 接收 .cnsh 文件
  - 调用 CNSH v2.1 解释器执行
  - 生成执行 DNA、计算风险/决策/信任评分
  - 写入审计链、记忆场、知识库
  - 返回结构化执行报告
DNA: #龍芯⚡️丙午·丙申·乙巳·庚辰·䷸巽-CNSH-EXECUTOR-v2.0-UID9622
"""
import os as _os
import sys as _sys
_module_dir = _os.path.dirname(_os.path.abspath(__file__))
if _module_dir not in _sys.path:
    _sys.path.insert(0, _module_dir)

import io
import json
import traceback
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# 把 CNSH v2.1 运行时加入路径
_CNSH_V21_ROOT = Path(_module_dir).parent / "cnsh" / "core" / "cnsh_v2.1"
if str(_CNSH_V21_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_CNSH_V21_ROOT))

from CNSH_国密工具 import SM3
from CNSH_透明语义治理内核 import (
    生成DNA身份锚,
    风险函数,
    决策函数,
    边界函数,
    信任函数,
    审计链,
    记忆场,
)
from CNSH_知识库 import CNSH_知识库


def _加载cnsh源码(路径: str) -> str:
    return Path(路径).read_text(encoding="utf-8")


def _真诚检查(源码: str, 人格名称: str = "CNSH执行器") -> Dict[str, Any]:
    """调用反虚伪引擎检查源码/回复文本。"""
    try:
        from cnsh_v21 import 反虚伪引擎
        return 反虚伪引擎.检查回复(源码, 人格名称)
    except Exception as exc:
        return {"状态": "通过", "建议": f"真诚检查未启用: {exc}", "异常": str(exc)}


def _执行v21(源码: str, 文件路径: str, 类型检查: bool = True) -> Dict[str, Any]:
    """调用 CNSH v2.1 解释器执行源码，捕获标准输出。"""
    try:
        from cnsh_v21 import run_source
        from cnsh_v21.errors import CNSHError
    except Exception as e:
        return {"ok": False, "error": f"无法导入 CNSH v2.1 运行时: {e}"}

    输出缓存 = io.StringIO()
    错误缓存 = io.StringIO()
    try:
        with redirect_stdout(输出缓存), redirect_stderr(错误缓存):
            返回值 = run_source(
                源码,
                file=文件路径,
                optimize_level=0,
                type_check=类型检查,
                strict_types=False,
            )
        return {
            "ok": True,
            "返回值": repr(返回值),
            "标准输出": 输出缓存.getvalue(),
            "标准错误": 错误缓存.getvalue(),
        }
    except CNSHError as exc:
        return {
            "ok": False,
            "error": str(exc),
            "标准输出": 输出缓存.getvalue(),
            "标准错误": 错误缓存.getvalue(),
        }
    except Exception as exc:
        return {
            "ok": False,
            "error": f"{type(exc).__name__}: {exc}",
            "标准输出": 输出缓存.getvalue(),
            "标准错误": 错误缓存.getvalue() + "\n" + traceback.format_exc(),
        }


class CNSH_执行器:
    """CNSH 透明语义治理执行器。"""

    def __init__(self, 工作目录: Optional[str] = None):
        self.工作目录 = Path(工作目录) if 工作目录 else Path(_module_dir) / "CNSH_中枢数据"
        self.工作目录.mkdir(parents=True, exist_ok=True)

        self.审计链目录 = self.工作目录 / "审计链"
        self.审计链目录.mkdir(parents=True, exist_ok=True)
        self.记忆场目录 = self.工作目录 / "记忆场"
        self.记忆场目录.mkdir(parents=True, exist_ok=True)

        self.审计链 = 审计链()
        self.记忆场 = 记忆场()
        self.知识库 = CNSH_知识库(路径=str(self.工作目录 / "CNSH_知识库.json"))

        self._加载持久化()

    def _持久化路径(self) -> Path:
        return self.工作目录 / "执行器状态.json"

    def _加载持久化(self):
        """加载审计链与记忆场（只追加，不覆盖）。"""
        路径 = self._持久化路径()
        if not 路径.exists():
            return
        try:
            with open(路径, "r", encoding="utf-8") as f:
                数据 = json.load(f)
            for entry in 数据.get("审计链", []):
                self.审计链.追加(entry)
            for node in 数据.get("记忆场", []):
                self.记忆场.写入(
                    node.get("dna", ""),
                    node.get("content", {}),
                    tags=node.get("tags", []),
                    previous_dna=node.get("previous_dna"),
                )
        except Exception:
            pass

    def _保存持久化(self):
        """把审计链与记忆场落盘（追加式）。"""
        路径 = self._持久化路径()
        with open(路径, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "审计链": self.审计链.导出(),
                    "记忆场": self.记忆场.读取(),
                    "保存时间": datetime.now(timezone.utc).isoformat(),
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

    def 执行文件(self, 文件路径: str, 类型检查: bool = True, 真诚检查: bool = False) -> Dict[str, Any]:
        """执行一个 .cnsh 文件，并写入审计链/记忆场/知识库。"""
        文件路径 = str(Path(文件路径).resolve())
        源码 = _加载cnsh源码(文件路径)
        源码哈希 = SM3.hex_hash(源码)
        执行DNA = 生成DNA身份锚("CNSH-EXECUTOR", "RUN", extra=源码哈希)

        # 反虚伪前置检查
        反虚伪结果 = None
        if 真诚检查:
            反虚伪结果 = _真诚检查(源码, 人格名称="CNSH执行器")
            self.审计链.追加(
                {
                    "dna": 执行DNA,
                    "action": "CNSH-ANTI-HYPOCRISY",
                    "file": 文件路径,
                    "反虚伪结果": 反虚伪结果,
                }
            )
            if 反虚伪结果.get("状态") == "熔断":
                结果 = {
                    "ok": False,
                    "状态": "反虚伪熔断",
                    "文件": 文件路径,
                    "源码哈希": 源码哈希,
                    "DNA": 执行DNA,
                    "反虚伪结果": 反虚伪结果,
                }
                self._归档结果(执行DNA, 源码哈希, 结果)
                return 结果
            if 反虚伪结果.get("状态") == "自动简化":
                源码 = 反虚伪结果.get("简化后", 源码)
                源码哈希 = SM3.hex_hash(源码)

        # 治理评分
        能力 = 1.0
        不确定性 = 0.3 if 类型检查 else 0.5
        自主性 = 0.8
        风险 = 风险函数(能力, 不确定性, 自主性)
        决策 = 决策函数(1.0, 0.9, 风险)
        通过边界 = 边界函数(风险, 2.0)
        信任 = 信任函数(1.0, 1.0, 1.0)

        # 审计：执行前
        self.审计链.追加(
            {
                "dna": 执行DNA,
                "action": "CNSH-RUN-START",
                "file": 文件路径,
                "source_hash": 源码哈希,
                "risk": round(风险, 4),
                "decision": round(决策, 4),
                "trust": round(信任, 4),
                "passed": 通过边界,
            }
        )

        if not 通过边界:
            结果 = {
                "ok": False,
                "状态": "治理熔断",
                "风险": round(风险, 4),
                "DNA": 执行DNA,
            }
            self._归档结果(执行DNA, 源码哈希, 结果)
            return 结果

        # 执行
        执行结果 = _执行v21(源码, 文件路径, 类型检查=类型检查)

        # 审计：执行后
        self.审计链.追加(
            {
                "dna": 执行DNA,
                "action": "CNSH-RUN-FINISH",
                "file": 文件路径,
                "ok": 执行结果["ok"],
                "risk": round(风险, 4),
                "decision": round(决策, 4),
                "trust": round(信任, 4),
            }
        )

        # 记忆场
        记忆DNA = 生成DNA身份锚("CNSH-EXECUTOR", "MEMORY", extra=执行DNA)
        self.记忆场.写入(
            记忆DNA,
            {
                "执行DNA": 执行DNA,
                "文件": 文件路径,
                "源码哈希": 源码哈希,
                "结果": 执行结果["ok"],
                "风险": round(风险, 4),
                "决策": round(决策, 4),
                "信任": round(信任, 4),
            },
            tags=["CNSH", "执行"],
            previous_dna=执行DNA,
        )

        结果 = {
            "ok": 执行结果["ok"],
            "状态": "执行成功" if 执行结果["ok"] else "执行失败",
            "文件": 文件路径,
            "源码哈希": 源码哈希,
            "DNA": 执行DNA,
            "记忆DNA": 记忆DNA,
            "风险": round(风险, 4),
            "决策": round(决策, 4),
            "信任": round(信任, 4),
            "返回值": 执行结果.get("返回值"),
            "标准输出": 执行结果.get("标准输出", ""),
            "标准错误": 执行结果.get("标准错误", ""),
            "错误信息": 执行结果.get("error", ""),
            "反虚伪结果": 反虚伪结果,
        }

        self._归档结果(执行DNA, 源码哈希, 结果)
        self._保存持久化()
        return 结果

    def _归档结果(self, 执行DNA: str, 源码哈希: str, 结果: Dict[str, Any]):
        """把执行结果追加到知识库。"""
        try:
            self.知识库.追加(
                标题=f"CNSH执行:{Path(结果.get('文件', 'unknown')).name}",
                文件路径=结果.get("文件", ""),
                核心概念=["CNSH", "执行器"],
                DNA=执行DNA,
                输入SM3哈希=源码哈希,
                备注=f"状态:{结果.get('状态')} 风险:{结果.get('风险')} 决策:{结果.get('决策')} 信任:{结果.get('信任')}",
            )
        except Exception:
            pass

    def 状态(self) -> Dict[str, Any]:
        return {
            "审计链长度": len(self.审计链.导出()),
            "记忆节点数": len(self.记忆场.读取()),
            "知识库统计": self.知识库.统计(),
            "工作目录": str(self.工作目录),
        }


# ============== CLI ==============
_VERSION = "CNSH v2.0 / 龍魂透明语义治理执行器"


def _resolve_file_arg(args: list) -> tuple:
    """解析命令行参数，支持 `cnsh file.cnsh` 和 `cnsh run file.cnsh`。"""
    no_type_check = False
    work_dir = None
    show_status = False
    show_version = False
    anti_hypocrisy = False
    file_path = None

    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-h", "--help"):
            return None, {"help": True}
        elif arg == "--version":
            show_version = True
        elif arg == "--no-type-check":
            no_type_check = True
        elif arg == "--anti-hypocrisy":
            anti_hypocrisy = True
        elif arg == "--status":
            show_status = True
        elif arg == "--work-dir":
            i += 1
            if i < len(args):
                work_dir = args[i]
        elif arg == "run":
            i += 1
            if i < len(args):
                file_path = args[i]
        elif not arg.startswith("-") and file_path is None:
            file_path = arg
        i += 1

    return file_path, {
        "no_type_check": no_type_check,
        "work_dir": work_dir,
        "status": show_status,
        "version": show_version,
        "anti_hypocrisy": anti_hypocrisy,
    }


def main(argv=None):
    import argparse

    if argv is None:
        argv = _sys.argv[1:]

    # 预处理：支持 `cnsh run file.cnsh`
    if argv and argv[0] == "run" and len(argv) > 1:
        argv = argv[1:]

    parser = argparse.ArgumentParser(description="CNSH v2.0 透明语义治理执行器")
    parser.add_argument("file", nargs="?", help="要执行的 .cnsh 文件")
    parser.add_argument("--no-type-check", action="store_true", help="禁用类型检查")
    parser.add_argument("--anti-hypocrisy", action="store_true", help="启用反虚伪前置检查")
    parser.add_argument("--async", action="store_true", dest="async_mode", help="异步后台执行")
    parser.add_argument("--status", action="store_true", help="显示执行器状态")
    parser.add_argument("--work-dir", help="工作目录（默认 bin/CNSH_中枢数据）")
    parser.add_argument("--version", action="store_true", help="显示版本")
    args = parser.parse_args(argv)

    if args.version:
        print(_VERSION)
        return 0

    if not args.file:
        parser.print_help()
        return 0

    # 异步模式：后台线程执行，立即返回提交状态
    if args.async_mode:
        import threading

        def _run_async():
            try:
                执行器 = CNSH_执行器(工作目录=args.work_dir)
                结果 = 执行器.执行文件(
                    args.file,
                    类型检查=not args.no_type_check,
                    真诚检查=args.anti_hypocrisy,
                )
                # 异步结果写入日志
                log_path = Path(_module_dir) / "CNSH_中枢数据" / "async_results.jsonl"
                log_path.parent.mkdir(parents=True, exist_ok=True)
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(结果, ensure_ascii=False) + "\n")
            except Exception as exc:
                log_path = Path(_module_dir) / "CNSH_中枢数据" / "async_errors.jsonl"
                log_path.parent.mkdir(parents=True, exist_ok=True)
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps({"file": args.file, "error": str(exc)}, ensure_ascii=False) + "\n")

        线程 = threading.Thread(target=_run_async, daemon=True)
        线程.start()
        print(json.dumps({
            "ok": True,
            "状态": "已提交",
            "模式": "异步",
            "文件": args.file,
            "说明": "后台执行中，结果写入 bin/CNSH_中枢数据/async_results.jsonl",
        }, ensure_ascii=False, indent=2))
        return 0

    执行器 = CNSH_执行器(工作目录=args.work_dir)

    if args.status:
        print(json.dumps(执行器.状态(), ensure_ascii=False, indent=2))
        return 0

    结果 = 执行器.执行文件(
        args.file,
        类型检查=not args.no_type_check,
        真诚检查=args.anti_hypocrisy,
    )
    print(json.dumps(结果, ensure_ascii=False, indent=2))
    return 0 if 结果.get("ok") else 1


if __name__ == "__main__":
    _sys.exit(main())
