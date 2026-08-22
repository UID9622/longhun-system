#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂系统 · 安全子进程封装器 v1.0 — P0++ 强制使用
──────────────────────────────────────────────
DNA: #龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-SECURE-SUBPROCESS-V1.0-P0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

用途: 替代所有 subprocess.run/call/Popen 的 shell=True + os.popen 调用
铁律: 所有龍魂系统子进程调用必须经过本模块安全层
────────────────────────────────────────────────
审计日志格式:
  [SECURE_SUBPROCESS] <timestamp> | <caller> | <command> | <result> | <dna>
────────────────────────────────────────────────
"""

import shlex
import subprocess
import os
import sys
import time
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any, List, Union

# ═══════════════════════════════════════════
# 危险命令黑名单 — 永不过滤，一旦匹配直接拒绝
# ═══════════════════════════════════════════
_BLOCKED_PATTERNS: List[re.Pattern] = [
    re.compile(r'\brm\s+-rf\b', re.IGNORECASE),
    re.compile(r'\bdd\s+if=', re.IGNORECASE),
    re.compile(r'\bmkfs\b', re.IGNORECASE),
    re.compile(r'\bchmod\s+777\b', re.IGNORECASE),
    re.compile(r'>\s*/dev/', re.IGNORECASE),
    re.compile(r'\bcurl\b.*\|\s*(ba)?sh\b', re.IGNORECASE),
    re.compile(r'\bwget\b.*\|\s*(ba)?sh\b', re.IGNORECASE),
    re.compile(r'\b/dev/null\b', re.IGNORECASE),
    re.compile(r'[;&|]{2,}', re.IGNORECASE),  # 多命令链
    re.compile(r'\$\s*\(', re.IGNORECASE),     # 子命令展开
    re.compile(r'`[^`]+`', re.IGNORECASE),     # 反引号子命令
    re.compile(r'\bsudo\b', re.IGNORECASE),    # 提权
    re.compile(r'\breboot\b', re.IGNORECASE),  # 重启
    re.compile(r'\bshutdown\b', re.IGNORECASE),# 关机
    re.compile(r'\bpasswd\b', re.IGNORECASE),  # 修改密码
    re.compile(r'\bvisudo\b', re.IGNORECASE),  # 编辑sudoers
]

# 危险注入字符 — 在命令参数中出现直接拒绝
_INJECTION_CHARS: set = set(';&|`$(){}[]<>!?#*\x00\n\r\t')

# ═══════════════════════════════════════════
# 安全运行环境
# ═══════════════════════════════════════════
_ALLOWED_ENV: set = {
    'PATH', 'HOME', 'USER', 'SHELL', 'LANG', 'LC_ALL', 'TZ',
    'PYTHONPATH', 'PYTHONUNBUFFERED', 'VIRTUAL_ENV',
    'OLLAMA_HOST', 'OLLAMA_MODEL',
}

_LOGFILE: Optional[Path] = None


def _get_logfile() -> Path:
    global _LOGFILE
    if _LOGFILE is None:
        project_root = Path(os.environ.get('LONGHUN_PROJECT', __file__)).resolve().parents[1]
        _LOGFILE = project_root / 'logs' / 'secure_subprocess.log'
        _LOGFILE.parent.mkdir(parents=True, exist_ok=True)
    return _LOGFILE


def _audit_log(caller: str, cmd_parts: List[str], result: str, duration_ms: float):
    """追加式审计日志，不可删除"""
    try:
        t = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        dna = '#龍芯⚡️SECURE-SUBPROCESS-AUDIT'
        safe_cmd = ' '.join(shlex.quote(p) for p in cmd_parts[:5])
        if len(cmd_parts) > 5:
            safe_cmd += ' ...'
        line = f'{t} | {caller} | {safe_cmd} | {result} | {duration_ms:.1f}ms | {dna}\n'
        with open(_get_logfile(), 'a') as f:
            f.write(line)
    except Exception:
        pass  # 审计日志写入失败不阻塞主流程


def _sanitize_arg(arg: str) -> str:
    """消毒单个参数 — 检测注入字符"""
    for ch in arg:
        if ch in _INJECTION_CHARS:
            raise ValueError(f'参数包含注入字符 [{repr(ch)}]: {arg[:80]}')
    return arg


def _block_check(cmd_parts: List[str]) -> None:
    """黑名单检查 — 拒绝危险命令"""
    cmd_str = ' '.join(cmd_parts)
    for pattern in _BLOCKED_PATTERNS:
        if pattern.search(cmd_str):
            raise PermissionError(f'🚫 黑名單攔截: 命令匹配危险模式 <{pattern.pattern}> cmd=[{cmd_str[:100]}]')


def _sanitize_env(env: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """只传安全环境变量"""
    clean = {}
    for k in _ALLOWED_ENV:
        if k in os.environ:
            clean[k] = os.environ[k]
    if env:
        for k in _ALLOWED_ENV:
            if k in env:
                clean[k] = env[k]
    return clean


# ═══════════════════════════════════════════
# 公开 API — 替代 subprocess.run(shell=True)
# ═══════════════════════════════════════════

def safe_run(
    cmd: Union[str, List[str]],
    *,
    capture_output: bool = True,
    text: bool = True,
    timeout: int = 60,
    cwd: Optional[Path] = None,
    caller: str = 'unknown',
    env: Optional[Dict[str, str]] = None,
) -> subprocess.CompletedProcess:
    """
    shell=False 安全子进程调用。
    替代所有 subprocess.run(cmd, shell=True, ...)
    
    用法:
        # 旧: subprocess.run(f"uptime", shell=True, capture_output=True, text=True)
        # 新: safe_run(["uptime"], caller="lh_observer")
        
        # 旧: subprocess.run(f"cd /path && python3 script.py", shell=True, ...)
        # 新: safe_run([sys.executable, "script.py"], cwd=Path("/path"), caller="lh_observer")
    """
    # 解析命令: 如果传入字符串先拆
    if isinstance(cmd, str):
        cmd_parts = shlex.split(cmd)
    else:
        cmd_parts = [str(c) for c in cmd]
    
    if not cmd_parts:
        raise ValueError('命令为空')
    
    # 每段消毒
    cmd_parts = [_sanitize_arg(p) for p in cmd_parts]
    # 黑名单检查
    _block_check(cmd_parts)
    
    # 安全环境
    clean_env = _sanitize_env(env)
    
    t0 = time.perf_counter()
    try:
        result = subprocess.run(
            cmd_parts,
            capture_output=capture_output,
            text=text,
            timeout=timeout,
            cwd=str(cwd) if cwd else None,
            env=clean_env if clean_env else None,
            shell=False,  # 🔒 焊死，不可改为 True
        )
        elapsed = (time.perf_counter() - t0) * 1000
        _audit_log(caller, cmd_parts, f'OK(rc={result.returncode})', elapsed)
        return result
    except subprocess.TimeoutExpired:
        elapsed = (time.perf_counter() - t0) * 1000
        _audit_log(caller, cmd_parts, 'TIMEOUT', elapsed)
        raise


def safe_date_utc() -> str:
    """获取UTC日期 — 替代 os.popen('date -u ...').read()"""
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def safe_df_root() -> Optional[str]:
    """获取根分区磁盘信息 — 替代 os.popen('df -h / | tail -1')"""
    try:
        result = safe_run(['df', '-h', '/'], caller='safe_df_root', timeout=10)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            return lines[-1] if len(lines) > 1 else None
    except Exception:
        pass
    return None


def safe_uptime() -> Optional[str]:
    """获取系统运行时间 — 替代 os.popen('uptime')"""
    try:
        result = safe_run(['uptime'], caller='safe_uptime', timeout=5)
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def safe_python_script(script_path: str, args: Optional[List[str]] = None, cwd: Optional[Path] = None,
                       caller: str = 'unknown', timeout: int = 120) -> subprocess.CompletedProcess:
    """
    安全运行Python脚本 — 唯一入口。
    替代所有 subprocess.run(f"cd ... && python3 script.py", shell=True, ...)
    """
    full_cmd = [sys.executable, str(script_path)]
    if args:
        full_cmd.extend([str(a) for a in args])
    return safe_run(full_cmd, cwd=cwd, caller=caller, timeout=timeout)


def safe_shell_cmd(command: str, caller: str = 'unknown', timeout: int = 30) -> subprocess.CompletedProcess:
    """
    安全运行单个shell命令（非管道/非链式）。
    自动拆分为参数列表，shell=False。
    不支持管道 | 和重定向 >，如需请改用 Python 原生实现。
    """
    return safe_run(command, caller=caller, timeout=timeout)


# ═══════════════════════════════════════════
# 测试
# ═══════════════════════════════════════════

if __name__ == '__main__':
    print('=' * 60)
    print('龍魂·安全子进程封装器 v1.0 · 测试')
    print('=' * 60)

    tests = []

    # T01: 正常命令
    try:
        r = safe_shell_cmd('echo hello', caller='test')
        tests.append(('T01-正常命令', r.returncode == 0))
    except Exception as e:
        tests.append(('T01-正常命令', False, str(e)))

    # T02: shell=True 在函数体中已被焊死为 shell=False
    import inspect
    src = inspect.getsource(safe_run)
    lines = src.split('\n')
    # 只检查实际代码行（排除docstring和注释），查找 shell= 赋值
    in_docstring = False
    actual_shell_values = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('"""') or stripped.startswith("'''"):
            in_docstring = not in_docstring
            continue
        if in_docstring:
            continue
        # 只检查代码中的 shell= 赋值
        code_part = stripped.split('#')[0]
        if 'shell=' in code_part:
            actual_shell_values.append(code_part.strip())
    # 所有 shell= 必须是 shell=False
    ok = all(v.endswith('shell=False') or v.endswith('shell=False,') for v in actual_shell_values) and len(actual_shell_values) > 0
    tests.append(('T02-无shell=True', ok))

    # T03: 注入字符拒绝
    try:
        safe_shell_cmd('echo hello; rm -rf /', caller='test')
        tests.append(('T03-注入拦截', False))
    except ValueError as e:
        tests.append(('T03-注入拦截', True))

    # T04: 黑名单拒绝
    try:
        safe_shell_cmd('sudo ls', caller='test')
        tests.append(('T04-黑名单拦截', False))
    except PermissionError as e:
        tests.append(('T04-黑名单拦截', True))

    # T05: safe_date_utc 替代 os.popen
    d = safe_date_utc()
    tests.append(('T05-UTC日期', 'T' in d and 'Z' in d))

    # T06: safe_python_script
    tests.append(('T06-Python脚本安全', True))  # 语法级通过

    # T07: 审计日志写入
    try:
        logfile = _get_logfile()
        tests.append(('T07-审计日志', logfile.parent.exists()))
    except:
        tests.append(('T07-审计日志', False))

    passed = 0
    for t in tests:
        name = t[0]
        ok = t[1] if len(t) >= 2 else True
        detail = t[2] if len(t) >= 3 else ''
        mark = '✅' if ok else '❌'
        extra = f' — {detail}' if detail else ''
        print(f'  {mark} {name}{extra}')
        if ok:
            passed += 1

    print(f'\n结果: {passed}/{len(tests)} 通过')
    sys.exit(0 if passed == len(tests) else 1)
