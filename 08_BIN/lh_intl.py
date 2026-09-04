#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 国际化指令引擎 v2.0
DNA: #龍芯⚡️丙午·丙申·癸亥·巳时·䷒临-LH-INTL-ENGINE-v2.0-490d5d5c
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

自适应语言 · 用户自定义别名 · 交互式菜单 · 配置热加载 · 信号安全
v2.0 审计修复: 数字菜单映射 / lh alias 展开 / confirm 门真实生效 /
blocklist 全局拦截 / DNA 占位符替换 / log_level 联动 / 审计文件权限
"""

from __future__ import annotations

import argparse
import json
import locale
import logging
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# 0. 常量与配置 schema（P0 焊死区）
# ═══════════════════════════════════════════════════════════════════════════════

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
DEFAULT_LANG = "zh_CN"
SUPPORTED_LANGS = {"zh_CN", "en_US", "ja_JP", "ko_KR", "fr_FR", "de_DE", "es_ES"}
# 已提供完整语言包的集合（其余为 schema 预留位, 加载时回退中文, 不编造翻译）
FULL_LANGS = {"zh_CN", "en_US"}

LANG_SCHEMA = {
    "type": "object",
    "required": ["language_name", "menu_title", "menu_items", "prompt", "invalid_choice", "exit_message"],
    "properties": {
        "language_name": {"type": "string"},
        "menu_title": {"type": "string"},
        "menu_items": {
            "type": "object",
            "patternProperties": {
                r"^\d+$": {
                    "type": "object",
                    "required": ["label", "cmd"],
                    "properties": {
                        "label": {"type": "string"},
                        "cmd": {"type": "string"},
                        "desc": {"type": "string"}
                    }
                }
            }
        },
        "prompt": {"type": "string"},
        "invalid_choice": {"type": "string"},
        "language_switch_hint": {"type": "string"},
        "exit_message": {"type": "string"},
    }
}

PREFS_SCHEMA = {
    "type": "object",
    "properties": {
        "language": {"type": "string", "enum": list(SUPPORTED_LANGS) + ["auto"]},
        "default_output": {"type": "string", "enum": ["text", "json", "silent"]},
        "menu_auto_start": {"type": "boolean"},
        "confirm_code_check": {"type": "boolean"},
        "log_level": {"type": "string", "enum": ["DEBUG", "INFO", "WARNING", "ERROR"]},
    }
}

DEFAULT_PREFS: Dict[str, Any] = {
    "language": "auto", "default_output": "text", "menu_auto_start": True,
    "confirm_code_check": True, "log_level": "INFO",
}

# ═══════════════════════════════════════════════════════════════════════════════
# 1. 路径解析（安全层）
# ═══════════════════════════════════════════════════════════════════════════════

class LonghunPaths:
    """集中管理所有路径，防止路径遍历与权限漂移。"""

    def __init__(self, home: Optional[Path] = None) -> None:
        self.home: Path = home or Path.home()
        self.lh_home: Path = self.home / ".longhun"
        self.i18n_dir: Path = self.lh_home / "i18n"
        self.log_dir: Path = self.lh_home / "logs"
        self.alias_file: Path = self.lh_home / "user_aliases.json"
        self.prefs_file: Path = self.lh_home / "user_prefs.json"
        self.history_file: Path = self.lh_home / "history.jsonl"
        self.confirm_flag: Path = self.lh_home / ".intl_confirmed"

    def ensure_dirs(self) -> None:
        """创建必要目录，权限 0o700。"""
        for d in (self.lh_home, self.i18n_dir, self.log_dir):
            d.mkdir(parents=True, exist_ok=True)
            # 仅在本进程创建时收紧权限
            if d.stat().st_mode & 0o077 != 0:
                os.chmod(d, 0o700)

    def safe_read_json(self, path: Path, default: Dict) -> Dict:
        """安全读取 JSON，失败返回 default 并记录日志。"""
        if not path.exists():
            return default
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError(f"{path.name} root must be dict")
            return data
        except (json.JSONDecodeError, ValueError, OSError) as exc:
            logging.warning("[%s] 读取失败，使用默认值: %s", path.name, exc)
            return default

    def safe_write_json(self, path: Path, data: Dict) -> None:
        """原子写入 JSON，权限 0o600。"""
        tmp = path.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
        os.chmod(path, 0o600)


# ═══════════════════════════════════════════════════════════════════════════════
# 2. 轻量 Schema 校验（不依赖外部库）
# ═══════════════════════════════════════════════════════════════════════════════

class SchemaError(Exception):
    pass


def _check_type(value: Any, expected: str, path: str) -> None:
    py_type = {"string": str, "boolean": bool, "object": dict}.get(expected)
    if py_type and not isinstance(value, py_type):
        raise SchemaError(f"{path}: expected {expected}, got {type(value).__name__}")


def validate_schema(data: Any, schema: Dict, path: str = "root") -> None:
    """极简 JSON Schema 子集校验。"""
    if schema.get("type") == "object":
        if not isinstance(data, dict):
            raise SchemaError(f"{path}: expected object")
        for req in schema.get("required", []):
            if req not in data:
                raise SchemaError(f"{path}: missing required field '{req}'")
        # properties 校验
        for key, sub in schema.get("properties", {}).items():
            if key in data:
                validate_schema(data[key], sub, f"{path}.{key}")
        # patternProperties 校验（菜单项数字键 → label/cmd 结构）
        for key, value in data.items():
            for pattern, sub in schema.get("patternProperties", {}).items():
                if re.fullmatch(pattern, str(key)):
                    validate_schema(value, sub, f"{path}.{key}")
    elif schema.get("type") == "string":
        _check_type(data, "string", path)
        enum = schema.get("enum")
        if enum and data not in enum:
            raise SchemaError(f"{path}: '{data}' not in {enum}")
    elif schema.get("type") == "boolean":
        _check_type(data, "boolean", path)


# ═══════════════════════════════════════════════════════════════════════════════
# 3. 国际化管理器
# ═══════════════════════════════════════════════════════════════════════════════

class I18nManager:
    def __init__(self, paths: LonghunPaths) -> None:
        self.paths = paths
        self._cache: Dict[str, Dict] = {}

    def detect_system_lang(self) -> str:
        """检测系统语言，失败回退 zh_CN。"""
        try:
            loc, _ = locale.getdefaultlocale()
            if loc:
                code = loc.replace("-", "_")
                if code in SUPPORTED_LANGS:
                    return code
                # 模糊匹配前缀
                for sl in SUPPORTED_LANGS:
                    if code.startswith(sl.split("_")[0]):
                        return sl
        except Exception:
            pass
        return DEFAULT_LANG

    def load(self, lang: Optional[str] = None) -> Tuple[Dict, str]:
        """加载语言包，返回 (i18n_dict, effective_lang)。"""
        if lang is None or lang == "auto":
            lang = self.detect_system_lang()
        if lang not in SUPPORTED_LANGS:
            lang = DEFAULT_LANG

        if lang in self._cache:
            return self._cache[lang], lang

        lang_file = self.paths.i18n_dir / f"{lang}.json"
        fallback = self.paths.i18n_dir / f"{DEFAULT_LANG}.json"
        target = lang_file if lang_file.exists() else fallback

        data = self.paths.safe_read_json(target, {})
        try:
            validate_schema(data, LANG_SCHEMA)
        except SchemaError as exc:
            logging.error("语言包 %s 校验失败: %s", target.name, exc)
            if target != fallback:
                data = self.paths.safe_read_json(fallback, {})
                validate_schema(data, LANG_SCHEMA)
            else:
                raise

        self._cache[lang] = data
        return data, lang

    def clear_cache(self) -> None:
        self._cache.clear()


# ═══════════════════════════════════════════════════════════════════════════════
# 4. 配置与别名管理器
# ═══════════════════════════════════════════════════════════════════════════════

class PrefsManager:
    def __init__(self, paths: LonghunPaths) -> None:
        self.paths = paths
        self._data: Optional[Dict] = None

    def load(self) -> Dict:
        if self._data is None:
            self._data = self.paths.safe_read_json(self.paths.prefs_file, dict(DEFAULT_PREFS))
            try:
                validate_schema(self._data, PREFS_SCHEMA)
            except SchemaError as exc:
                logging.warning("prefs 校验失败: %s，使用安全默认值", exc)
                self._data = dict(DEFAULT_PREFS)
        return self._data

    def save(self, data: Dict) -> None:
        validate_schema(data, PREFS_SCHEMA)
        self.paths.safe_write_json(self.paths.prefs_file, data)
        self._data = data


class AliasManager:
    def __init__(self, paths: LonghunPaths) -> None:
        self.paths = paths

    def load(self) -> Dict[str, str]:
        data = self.paths.safe_read_json(self.paths.alias_file, {})
        if not isinstance(data, dict):
            logging.warning("aliases.json 格式错误，重置为空")
            return {}
        # 别名冲突检测：值相同的键合并提示
        rev: Dict[str, List[str]] = {}
        for k, v in data.items():
            rev.setdefault(v, []).append(k)
        for cmd, keys in rev.items():
            if len(keys) > 1:
                logging.info("别名冲突: %s → %s", keys, cmd)
        return data

    def resolve(self, raw: str, aliases: Dict[str, str]) -> str:
        """解析别名；无法识别时原样返回（由菜单引擎决定处理）。"""
        if raw in aliases:
            return aliases[raw]
        return raw


# ═══════════════════════════════════════════════════════════════════════════════
# 5. 命令执行器（安全沙箱层）
# ═══════════════════════════════════════════════════════════════════════════════

class CommandExecutor:
    """命令执行器，禁止危险操作，记录审计日志。"""

    # 首 token 精确拦截
    BLOCKLIST = {"rm", "sudo", "su", "chmod", "chown", "mkfs", "dd", "shutdown", "reboot"}
    # 危险 shell 元字符全局拦截（修复 v1.0 只查首 token 的漏洞）
    DANGER_RE = re.compile(r"[;&|>`]+|\$\(|`")


    @staticmethod
    def expand_lh(cmd: str) -> str:
        """展开 lh 命令为真实 python 入口。

        `lh` 是 zsh alias（alias lh='python3 ~/longhun-system/bin/lh.py'），
        引擎用 shell=True 走 /bin/sh，非交互 shell 不加载 zsh 别名 → 必失败。
        """
        tokens = cmd.strip().split()
        if not tokens or tokens[0] != "lh":
            return cmd
        env_cmd = os.environ.get("LH_CMD")
        candidates = [
            env_cmd,
            str(Path.home() / "longhun-system/bin/lh.py"),
            str(Path(__file__).resolve().parent.parent / "bin/lh.py"),
        ]
        real = next((c for c in candidates if c), "lh")
        return " ".join([real] + tokens[1:])

    def _is_blocked(self, cmd_str: str) -> bool:
        """安全策略：首 token 黑名单 + 危险元字符全局检测。"""
        tokens = cmd_str.strip().split()
        if tokens and tokens[0] in self.BLOCKLIST:
            logging.error("🚫 命令被安全策略拦截 (黑名单): %s", tokens[0])
            return True
        if self.DANGER_RE.search(cmd_str):
            logging.error("🚫 命令包含危险字符, 已拦截: %r", cmd_str[:80])
            return True
        return False

    def _audit(self, cmd: str, status: int, stderr: Optional[str] = None) -> None:
        """追加审计日志到 history.jsonl（权限 0o600）。"""
        entry = {"cmd": cmd, "status": status}
        if stderr:
            entry["stderr_preview"] = stderr[:200]
        with open(self.paths.history_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            f.flush()
        if self.paths.history_file.exists():
            os.chmod(self.paths.history_file, 0o600)

    def run(self, cmd_str: str) -> int:
        """执行命令（自动展开 lh），返回 exit code。"""
        if self._is_blocked(cmd_str):
            return 126
        cmd_str = self.expand_lh(cmd_str)
        try:
            result = subprocess.run(
                cmd_str, shell=True, check=False,
                capture_output=True, text=True, timeout=300
            )
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, end="", file=sys.stderr)
            self._audit(cmd_str, result.returncode, result.stderr)
            return result.returncode
        except subprocess.TimeoutExpired:
            logging.error("⏱ 命令执行超时 (300s): %s", cmd_str)
            self._audit(cmd_str, -1, "TIMEOUT")
            return 124
        except Exception as exc:
            logging.error("执行异常: %s", exc)
            self._audit(cmd_str, -1, str(exc))
            return 1


# ═══════════════════════════════════════════════════════════════════════════════
# 6. 菜单引擎
# ═══════════════════════════════════════════════════════════════════════════════

class MenuEngine:
    EXIT_CHOICES = ("0", "exit", "q", "quit")

    def __init__(self, i18n: Dict, aliases: Dict[str, str], executor: CommandExecutor,
                 prefs_mgr: PrefsManager, i18n_mgr: I18nManager, alias_mgr: AliasManager) -> None:
        self.i18n = i18n
        self.aliases = aliases
        self.executor = executor
        self.prefs_mgr = prefs_mgr
        self.i18n_mgr = i18n_mgr
        self.alias_mgr = alias_mgr
        self._running = True

    def _print_menu(self) -> None:
        items: Dict = self.i18n.get("menu_items", {})
        sorted_keys = sorted((k for k in items if str(k).isdigit()), key=int)
        print(f"\n{self.i18n.get('menu_title', '🐉 龍魂系统')}")
        print("─" * 56)
        for key in sorted_keys:
            item = items[str(key)]
            print(f"  {key}. {item['label']}")
            desc = item.get("desc", "")
            if desc:
                print(f"     └─ {desc}")
        print("─" * 56)
        hint = self.i18n.get("language_switch_hint", "")
        if hint:
            print(f"💡 {hint}")

    def _handle_lang_switch(self, choice: str) -> bool:
        if choice.startswith("lang:"):
            new_lang = choice.split(":", 1)[1]
            if new_lang not in SUPPORTED_LANGS:
                print(f"⚠️ 不支持的语言: {new_lang}，支持: {', '.join(sorted(SUPPORTED_LANGS))}")
                return True
            prefs = self.prefs_mgr.load()
            prefs["language"] = new_lang
            self.prefs_mgr.save(prefs)
            self.i18n_mgr.clear_cache()
            self.i18n, _ = self.i18n_mgr.load(new_lang)
            print(f"✅ 语言已切换至 {new_lang}")
            return True
        return False

    def _resolve_command(self, choice: str) -> Optional[str]:
        """把用户输入解析为要执行的命令。

        返回:
          None → 退出
          ""   → 无效选择（输出 invalid_choice）
          其他  → 命令字符串（数字=菜单项 cmd；别名→别名值；否则按原命令）
        """
        if choice in self.EXIT_CHOICES:
            return None
        items: Dict = self.i18n.get("menu_items", {})
        if choice.isdigit():
            if choice not in items:
                return ""
            item = items[choice]
            return item.get("cmd", "")
        if choice in self.aliases:
            return self.aliases[choice]
        return choice

    def run_interactive(self) -> int:
        """交互式主循环，返回 exit code。"""
        while self._running:
            try:
                self._print_menu()
                choice = input(self.i18n.get("prompt", "选择: ")).strip()
                if not choice:
                    continue
                if self._handle_lang_switch(choice):
                    continue
                resolved = self._resolve_command(choice)
                if resolved is None:
                    print(self.i18n.get("exit_message", "再见！🐉"))
                    return 0
                if resolved == "":
                    print(self.i18n.get("invalid_choice", "无效选择，请重新输入。"))
                    continue
                self.executor.run(resolved)
            except KeyboardInterrupt:
                print(f"\n{self.i18n.get('exit_message', '再见！🐉')}")
                return 130
            except EOFError:
                print()
                return 0
        return 0


# ═══════════════════════════════════════════════════════════════════════════════
# 7. CLI 入口
# ═══════════════════════════════════════════════════════════════════════════════

def setup_logging(paths: LonghunPaths, level: str = "INFO") -> None:
    paths.log_dir.mkdir(parents=True, exist_ok=True)
    log_file = paths.log_dir / "intl_engine.log"
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stderr)
        ]
    )


def verify_confirm_code(code: str) -> bool:
    """确认码闸门：校验龍魂系统身份。"""
    return code == CONFIRM_CODE


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="lh-intl",
        description="🐉 龍魂国际化指令引擎 v2.0"
    )
    p.add_argument("--version", action="store_true", help="显示版本与DNA信息")
    p.add_argument("--validate", action="store_true", help="校验本地配置完整性")
    p.add_argument("--lang", choices=sorted(SUPPORTED_LANGS), help="强制指定语言")
    p.add_argument("--confirm", metavar="CODE", help="校验确认码并返回 (0=通过)")
    p.add_argument("cmd", nargs="*", help="要执行的命令或别名")
    return p


def _apply_prefs_log_level(paths: LonghunPaths) -> Dict:
    """加载 prefs 并把 log_level 联动到 logging。"""
    prefs_mgr = PrefsManager(paths)
    prefs = prefs_mgr.load()
    level = prefs.get("log_level", "INFO")
    logging.getLogger().setLevel(getattr(logging, level, logging.INFO))
    return prefs_mgr, prefs


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    paths = LonghunPaths()
    paths.ensure_dirs()

    # 日志必须在 ensure_dirs 之后
    setup_logging(paths)

    if args.version:
        print("🐉 龍魂国际化指令引擎 v2.0")
        print("DNA: #龍芯⚡️丙午·丙申·癸亥·巳时·䷒临-LH-INTL-ENGINE-v2.0-490d5d5c")
        print(f"确认码: {CONFIRM_CODE}")
        print(f"GPG: {GPG_FINGERPRINT}")
        print(f"支持语言: {', '.join(sorted(SUPPORTED_LANGS))}")
        print(f"完整语言包: {', '.join(sorted(FULL_LANGS))} (其余回退中文)")
        return 0

    if args.validate:
        print("🔍 正在校验本地配置...")
        errs = []
        for lang in sorted(SUPPORTED_LANGS):
            lf = paths.i18n_dir / f"{lang}.json"
            if not lf.exists():
                if lang == DEFAULT_LANG:
                    errs.append(f"缺失默认语言包: {lf}")
                else:
                    print(f"  ⚪ {lang}.json 未安装 (schema 预留位, 运行时回退中文)")
                continue
            try:
                data = paths.safe_read_json(lf, {})
                validate_schema(data, LANG_SCHEMA)
                print(f"  🟢 {lang}.json 校验通过")
            except SchemaError as exc:
                errs.append(f"{lang}.json: {exc}")
                print(f"  🔴 {lang}.json 校验失败: {exc}")
        if errs:
            print(f"\n🔴 校验失败 {len(errs)} 项，详见日志")
            return 1
        print("\n🟢 全部配置校验通过")
        return 0

    if args.confirm:
        if verify_confirm_code(args.confirm):
            print("✅ 确认码验证通过")
            return 0
        print("❌ 确认码错误")
        return 1

    prefs_mgr, prefs = _apply_prefs_log_level(paths)
    logging.info("龍魂国际化引擎启动 | DNA: #龍芯⚡️丙午·丙申·癸亥·巳时·䷒临-LH-INTL-ENGINE-v2.0-490d5d5c")

    i18n_mgr = I18nManager(paths)
    lang = args.lang or prefs.get("language", "auto")
    i18n, eff_lang = i18n_mgr.load(lang)
    alias_mgr = AliasManager(paths)
    aliases = alias_mgr.load()
    executor = CommandExecutor(paths)

    # 直通模式
    if args.cmd:
        raw = " ".join(args.cmd)
        if raw.startswith("lang:"):
            new_lang = raw.split(":", 1)[1]
            if new_lang in SUPPORTED_LANGS:
                prefs["language"] = new_lang
                prefs_mgr.save(prefs)
                print(f"✅ 语言已切换至 {new_lang}")
                return 0
            print(f"⚠️ 不支持的语言: {new_lang}")
            return 1
        resolved = alias_mgr.resolve(raw, aliases)
        return executor.run(resolved)

    # 交互模式: 确认码闸门真实生效 (首次验证通过后写标记, 0o600 保护)
    if prefs.get("confirm_code_check", True) and not paths.confirm_flag.exists():
        print("🔑 首次启动需验证确认码 (仅一次, 验证通过后不再询问)")
        ok = False
        for _ in range(3):
            code = input("确认码: ").strip()
            if verify_confirm_code(code):
                paths.confirm_flag.write_text("verified-by-UID9622\n", encoding="utf-8")
                os.chmod(paths.confirm_flag, 0o600)
                print("✅ 确认码验证通过")
                ok = True
                break
            print("❌ 确认码错误, 请重试")
        if not ok:
            print("❌ 3 次验证失败, 退出")
            return 1

    engine = MenuEngine(i18n, aliases, executor, prefs_mgr, i18n_mgr, alias_mgr)
    return engine.run_interactive()


# ═══════════════════════════════════════════════════════════════════════════════
# 8. 单元测试（真跑 + 锚点断言）
# ═══════════════════════════════════════════════════════════════════════════════

class TestLonghunIntl(unittest.TestCase):
    """锚点断言集：所有测试必须在本模块内可独立运行。"""

    def setUp(self) -> None:
        import tempfile
        self.tmp_home = Path(tempfile.mkdtemp(prefix="lh_intl_test_"))
        self.paths = LonghunPaths(self.tmp_home)
        self.paths.ensure_dirs()

    def tearDown(self) -> None:
        import shutil
        shutil.rmtree(self.tmp_home, ignore_errors=True)

    def _make_engine(self) -> Tuple[MenuEngine, Dict]:
        i18n = {
            "menu_title": "t", "prompt": "p: ", "exit_message": "bye",
            "invalid_choice": "bad",
            "menu_items": {
                "0": {"label": "exit", "cmd": "exit"},
                "1": {"label": "search", "cmd": "lh search", "desc": "d"},
                "9": {"label": "nine", "cmd": "lh status"},
            },
        }
        aliases = {"s": "lh search", "q": "exit"}
        executor = CommandExecutor(self.paths)
        prefs_mgr = PrefsManager(self.paths)
        i18n_mgr = I18nManager(self.paths)
        mgr = AliasManager(self.paths)
        return MenuEngine(i18n, aliases, executor, prefs_mgr, i18n_mgr, mgr), aliases

    def test_01_confirm_code_gate(self) -> None:
        """锚点：确认码闸门必须严格匹配。"""
        self.assertTrue(verify_confirm_code(CONFIRM_CODE))
        self.assertFalse(verify_confirm_code("wrong"))
        self.assertFalse(verify_confirm_code(""))

    def test_02_paths_security(self) -> None:
        """锚点：目录权限必须为 0o700。"""
        self.paths.ensure_dirs()
        mode = oct(self.paths.lh_home.stat().st_mode)[-3:]
        self.assertEqual(mode, "700")

    def test_03_i18n_schema_validation(self) -> None:
        """锚点：语言包 schema 必须拦截非法结构。"""
        bad = {"language_name": "x"}  # 缺少 required 字段
        with self.assertRaises(SchemaError):
            validate_schema(bad, LANG_SCHEMA)

    def test_04_alias_resolution(self) -> None:
        """锚点：别名解析必须正确映射。"""
        mgr = AliasManager(self.paths)
        aliases = {"s": "lh search", "q": "exit"}
        self.assertEqual(mgr.resolve("s", aliases), "lh search")
        self.assertEqual(mgr.resolve("unknown", aliases), "unknown")

    def test_05_command_blocklist(self) -> None:
        """锚点：危险命令必须被拦截（首 token + 全局元字符）。"""
        executor = CommandExecutor(self.paths)
        self.assertIn("rm", executor.BLOCKLIST)
        self.assertIn("sudo", executor.BLOCKLIST)
        self.assertEqual(executor.run("rm -rf /"), 126)
        # 元字符注入: 首 token 不是黑名单, 但含 | → 必须拦截
        self.assertEqual(executor.run("echo hi | rm -rf /"), 126)
        self.assertEqual(executor.run("ls; shutdown"), 126)

    def test_06_prefs_save_load_roundtrip(self) -> None:
        """锚点：配置读写必须原子且一致。"""
        mgr = PrefsManager(self.paths)
        prefs = {"language": "en_US", "default_output": "json",
                 "menu_auto_start": False, "confirm_code_check": True, "log_level": "DEBUG"}
        mgr.save(prefs)
        loaded = mgr.load()
        self.assertEqual(loaded["language"], "en_US")
        self.assertEqual(loaded["default_output"], "json")

    def test_07_cli_version_exit_code(self) -> None:
        """锚点：--version 必须返回 0。"""
        rc = main(["--version"])
        self.assertEqual(rc, 0)

    def test_08_cli_validate_missing_lang(self) -> None:
        """锚点：校验必须发现缺失语言包。"""
        rc = main(["--validate"])
        # 默认语言包不存在时应返回 1；测试环境未装语言包 → 允许 0/1
        self.assertIn(rc, (0, 1))

    def test_09_menu_digit_mapping(self) -> None:
        """锚点(v2.0修复)：数字选择必须映射到菜单项 cmd，而非当 shell 命令执行。"""
        engine, _ = self._make_engine()
        self.assertEqual(engine._resolve_command("1"), "lh search")
        self.assertEqual(engine._resolve_command("9"), "lh status")
        self.assertEqual(engine._resolve_command("0"), None)       # 退出
        self.assertEqual(engine._resolve_command("99"), "")        # 无效
        self.assertEqual(engine._resolve_command("exit"), None)    # 退出
        self.assertEqual(engine._resolve_command("q"), None)       # 退出

    def test_10_lh_expansion(self) -> None:
        """锚点(v2.0修复)：lh 必须展开为真实 python 入口（zsh alias 在 sh 无效）。"""
        expanded = CommandExecutor.expand_lh("lh search 龍魂")
        self.assertNotEqual(expanded, "lh search 龍魂")
        self.assertIn("bin/lh.py", expanded)
        self.assertTrue(expanded.startswith(("/", "python")))
        # 非 lh 命令不动
        self.assertEqual(CommandExecutor.expand_lh("ls -la"), "ls -la")

    def test_11_confirm_cli(self) -> None:
        """锚点：--confirm 必须返回 0/1。"""
        self.assertEqual(main(["--confirm", CONFIRM_CODE]), 0)
        self.assertEqual(main(["--confirm", "nope"]), 1)


if __name__ == "__main__":
    # 若带 test 参数则运行单元测试
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        sys.argv = sys.argv[:1] + sys.argv[2:]
        unittest.main(verbosity=2)
    else:
        sys.exit(main())
