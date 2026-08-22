#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂插件沙箱 · 插件加载器 v1.1
DNA: #龍芯⚡️2026-08-22-PLUGIN-LOADER-v1.1
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

v1.1 安全加固（P77 实测五洞全开后的补丁）：
  1. import 守卫：插件禁止 import core / sandbox_runtime / bin / subprocess /
     socket / ctypes / multiprocessing / pickle / pty / resource 等
     黑名单模块（meta_path finder + __import__ 包装 + os 危险函数 stub +
     builtins 危险入口 stub），并从 sys.path 摘除项目根，防止绕道 import。
  2. 插件文件 sha256 哈希校验：plugin.json 可声明 files 映射，加载时校验，
     防篡改（被外部改过 → 拒绝加载并审计 🔴）。
  3. 加载失败原因记录，不再吞异常。
"""

import json
import hashlib
import os
import sys
import types
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass, field

# 模块加载时捕获安全引用（import 守卫安装后 builtins.open/exec 等会被替换，
# 本模块必须用这些安全引用读写文件/执行插件代码）
_safe_open = open
_safe_exec = exec
_safe_compile = compile

# ---------------------------------------------------------------------------
# import 守卫（只对插件生效 · 子进程生命周期内不还原 · 见 runner 说明）
# ---------------------------------------------------------------------------

# 无条件禁止 import 的顶层模块（含其子模块）
IMPORT_BLOCKLIST = {
    "core", "sandbox_runtime", "bin", "08_BIN",          # 项目核心
    "subprocess", "socket", "ctypes", "multiprocessing",  # 系统逃逸
    "pickle", "pty", "resource", "pdb", "code",           # 序列化/调试/资源
    "fcntl", "mmap", "shelve",                             # 底层文件/序列化
    "inspect", "importlib",                                # 反射/动态加载
    "http.server", "urllib.request", "requests",           # 网络（走 net.* 能力）
    "shutil", "glob", "tempfile",                          # 文件系统（走 fs.* 能力）
}

# os 模块中被替换为拒绝桩的危险函数（纯逃逸/破坏类）
# 注意：stat/lstat/mkdir/listdir 等不能 patch —— pathlib._NormalAccessor 虽在
# import 时绑定引用，但 os.path.realpath 等会运行时空查 os，误伤 fs 能力。
_OS_DANGEROUS = (
    "system", "popen", "fork", "forkpty", "execv", "execve", "execvp",
    "execl", "execlp", "execvpe", "spawnv", "spawnve", "spawnl",
    "spawnle", "spawnlp", "spawnlpe", "remove", "rmdir", "unlink",
    "rename", "replace", "chmod", "chown", "chdir", "kill", "killpg",
    "setuid", "setgid", "setgroups", "chroot", "mknod", "mkfifo",
    "link", "symlink", "truncate", "sendfile",
)

# builtins 中被替换为拒绝桩的危险入口（文件/代码执行走能力 API）
_BUILTINS_DANGEROUS = ("open", "exec", "eval", "compile", "input", "__import__")


def _denied(*args, **kwargs):
    raise PermissionError("[沙箱] 该操作已被能力门控禁止，请走 SandboxAPI 申请对应能力")


class _ImportGuardFinder:
    """meta_path finder · 命中黑名单顶层模块直接拒绝"""

    def __init__(self, blocklist):
        self._blocklist = blocklist

    def find_spec(self, fullname, path=None, target=None):
        root = fullname.split(".")[0]
        if root in self._blocklist:
            # name 属性必须带：否则 import 机制会把 ImportError 当作
            # "找不到模块"吞掉继续找下一个 finder（实测会绕过守卫）
            raise ImportError(f"[沙箱] 插件禁止 import {fullname}", name=fullname)
        return None  # 未命中则交给后续 finder


def install_import_guard() -> None:
    """在插件模块 exec 前安装 import 守卫（子进程内一次安装 · 不还原）"""
    import builtins

    # 1. meta_path finder：拦 core / subprocess 等
    sys.meta_path.insert(0, _ImportGuardFinder(IMPORT_BLOCKLIST))

    # 2. 包装 __import__：拦显式 __import__("core") 调用
    _orig_import = builtins.__import__

    def _guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
        root = name.split(".")[0]
        if root in IMPORT_BLOCKLIST:
            raise ImportError(f"[沙箱] 插件禁止 import {name}")
        return _orig_import(name, globals, locals, fromlist, level)

    builtins.__import__ = _guarded_import

    # 3. os 危险函数替换为拒绝桩
    os_mod = __import__("os")
    for name in _OS_DANGEROUS:
        if hasattr(os_mod, name):
            setattr(os_mod, name, _denied)

    # 4. builtins 危险入口替换为拒绝桩
    for name in _BUILTINS_DANGEROUS:
        setattr(builtins, name, _denied)


def strip_project_root_from_path() -> None:
    """从 sys.path 摘除项目根，插件无法通过路径 import core/sandbox_runtime"""
    root = str(Path(__file__).resolve().parent.parent)
    sys.path[:] = [p for p in sys.path if p and os.path.abspath(p) != root]


# ---------------------------------------------------------------------------
# 插件清单
# ---------------------------------------------------------------------------

@dataclass
class PluginManifest:
    """插件元数据"""
    id: str
    name: str
    version: str
    description: str
    author: str
    capabilities: List[str] = field(default_factory=list)
    entry: str = "main.py"
    timeout: int = 30
    files: dict = field(default_factory=dict)  # {相对路径: sha256} 可选防篡改声明


class PluginLoader:
    """插件加载器 · 每个插件必须有 plugin.json · 严格限制上下文"""

    PLUGINS_ROOT = Path(__file__).resolve().parent.parent / "plugins"
    _last_error: Optional[str] = None  # 最近一次加载失败原因（供审计）

    @classmethod
    def get_plugin_path(cls, plugin_id: str) -> Path:
        return cls.PLUGINS_ROOT / plugin_id

    @classmethod
    def load_manifest(cls, plugin_id: str) -> Optional[PluginManifest]:
        cls._last_error = None
        plugin_path = cls.get_plugin_path(plugin_id)
        manifest_path = plugin_path / "plugin.json"
        if not manifest_path.exists():
            cls._last_error = f"清单不存在: {manifest_path}"
            return None
        try:
            with _safe_open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            timeout = data.get("timeout", 30)
            try:
                timeout = max(1, int(timeout))
            except (TypeError, ValueError):
                timeout = 30
            return PluginManifest(
                id=data.get("id", plugin_id),
                name=data.get("name", plugin_id),
                version=data.get("version", "0.0.1"),
                description=data.get("description", ""),
                author=data.get("author", "unknown"),
                capabilities=data.get("capabilities", []),
                entry=data.get("entry", "main.py"),
                timeout=timeout,
                files=data.get("files", {}))
        except Exception as e:
            cls._last_error = f"清单解析失败: {e}"
            return None

    @classmethod
    def verify_files_integrity(cls, plugin_id: str,
                               manifest: PluginManifest) -> Optional[str]:
        """校验插件文件 sha256（manifest.files 声明了才校验）· 返回失败原因"""
        if not manifest.files:
            return None
        plugin_path = cls.get_plugin_path(plugin_id)
        for rel, expected in manifest.files.items():
            target = plugin_path / rel
            if not target.exists():
                return f"文件缺失(防篡改): {rel}"
            try:
                actual = hashlib.sha256(target.read_bytes()).hexdigest()
            except Exception as e:
                return f"文件读取失败(防篡改): {rel}: {e}"
            if actual.lower() != str(expected).lower():
                return f"文件哈希不符(防篡改): {rel}"
        return None

    @classmethod
    def load_plugin_module(cls, plugin_id: str):
        """加载插件入口模块（严格限制上下文 + import 守卫）"""
        plugin_path = cls.get_plugin_path(plugin_id)
        manifest = cls.load_manifest(plugin_id)
        if manifest is None:
            raise ValueError(f"无法加载插件清单 {plugin_id}: {cls._last_error}")

        integrity_error = cls.verify_files_integrity(plugin_id, manifest)
        if integrity_error is not None:
            raise ValueError(integrity_error)

        entry_path = plugin_path / manifest.entry
        if not entry_path.exists():
            raise FileNotFoundError(f"插件入口文件不存在: {entry_path}")

        # 1. 用安全引用读取插件源码（guard 装好后 builtins.open 会被替换，
        #    不能依赖 importlib loader 读文件）
        try:
            with _safe_open(entry_path, "r", encoding="utf-8") as f:
                source = f.read()
        except Exception as e:
            raise ValueError(f"插件源码读取失败: {entry_path}: {e}")

        # 2. 摘除项目根路径：插件 import core / sandbox_runtime 将直接失败
        strip_project_root_from_path()
        # 3. 只留插件自身目录可被 import
        sys.path.insert(0, str(plugin_path))
        # 4. 安装 import 守卫：黑名单模块 + os/builtins 危险入口
        install_import_guard()

        # 5. 编译并执行插件源码（_safe_compile/_safe_exec 为 guard 前的安全引用）
        module = types.ModuleType(f"plugin_{plugin_id}")
        module.__file__ = str(entry_path)
        module.__package__ = None
        try:
            code = _safe_compile(source, str(entry_path), "exec")
            _safe_exec(code, module.__dict__)
        except PermissionError as e:
            raise PermissionError(f"[沙箱] 插件源码执行被拒: {e}")
        return module, manifest
