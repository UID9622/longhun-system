#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂统一密钥加载器 v1.0
Unified Secrets Loader — 从 vault JSON / .env / Keychain 加载所有凭证

DNA: #龍芯⚡️丙午·乙未·壬辰·午时·需-SECRETS-LOADER-v1.0
📇 项目身份 · 联系 · 支持 → assets/PUBLIC_IDENTITY.md

功能:
  - 从 ~/.longhun/vault/credential_vault.json 读取所有凭证
  - 自动合并 ~/.env 中的环境变量
  - 支持 Keychain 读取（macOS）
  - 导出为 os.environ 供所有模块使用
  - 不打印、不泄露明文到日志

用法:
  python3 bin/lh_secrets_loader.py           # 加载所有凭证到环境变量
  python3 bin/lh_secrets_loader.py --list    # 列出服务名（不显示值）
  python3 bin/lh_secrets_loader.py --get KEY # 获取单个凭证值
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional, Any

# ═══════════════════════════════════════════════════════
# 路径常量
# ═══════════════════════════════════════════════════════
HOME = Path.home()
VAULT_JSON = HOME / ".longhun" / "vault" / "credential_vault.json"
ENV_FILE = HOME / ".env"
DEEPSEEK_ENV = HOME / ".deepseek_bridge.env"
SECRETS_ENV = HOME / ".longhun" / "secrets.env"

# ═══════════════════════════════════════════════════════
# 核心加载逻辑
# ═══════════════════════════════════════════════════════

def load_vault() -> Dict[str, Dict[str, Any]]:
    """从 credential_vault.json 加载所有凭证元数据"""
    if not VAULT_JSON.exists():
        print(f"⚠️ Vault 不存在: {VAULT_JSON}", file=sys.stderr)
        return {}
    try:
        data = json.loads(VAULT_JSON.read_text(encoding="utf-8"))
        return data.get("credentials", {})
    except Exception as e:
        print(f"❌ Vault 解析失败: {e}", file=sys.stderr)
        return {}


def load_env_file(path: Path) -> Dict[str, str]:
    """从 .env 文件解析环境变量"""
    if not path.exists():
        return {}
    result = {}
    try:
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # 支持 export KEY="value" 或 KEY=value
            if line.startswith("export "):
                line = line[7:]
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and value:
                    result[key] = value
    except Exception as e:
        print(f"⚠️ 解析 {path} 失败: {e}", file=sys.stderr)
    return result


def load_keychain(service: str) -> Optional[str]:
    """从 macOS Keychain 读取密码"""
    try:
        result = subprocess.run(
            ["security", "find-generic-password", "-s", service, "-w"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def export_to_env(credentials: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
    """将 vault 凭证导出为环境变量字典"""
    env = {}
    for key, item in credentials.items():
        value = item.get("value", "")
        if value and item.get("status") != "missing":
            env[key] = value
    return env


# ═══════════════════════════════════════════════════════
# 一键加载 - 供 AI 会话启动调用
# ═══════════════════════════════════════════════════════

def load_all(export_to_os: bool = True) -> Dict[str, Dict[str, Any]]:
    """
    加载所有凭证（vault + env + keychain），可选导出到 os.environ
    
    Returns:
        dict: {KEY_NAME: {"value": "...", "source": "...", "status": "..."}}
    """
    credentials = load_vault()
    
    # 合并 ~/.env 中不在 vault 里的变量
    env_vars = load_env_file(ENV_FILE)
    for key, value in env_vars.items():
        if key not in credentials and value:
            credentials[key] = {
                "value": value,
                "source": "~/.env",
                "description": "",
                "status": "active"
            }
    
    # 合并 deepseek bridge env
    ds_vars = load_env_file(DEEPSEEK_ENV)
    for key, value in ds_vars.items():
        if key not in credentials:
            credentials[key] = {
                "value": value,
                "source": "~/.deepseek_bridge.env",
                "description": "DeepSeek Bridge 专用",
                "status": "active"
            }
    
    # 合并 secrets.env
    sec_vars = load_env_file(SECRETS_ENV)
    for key, value in sec_vars.items():
        if key not in credentials and not key.startswith("#"):
            credentials[key] = {
                "value": value,
                "source": "~/.longhun/secrets.env",
                "description": "",
                "status": "active"
            }
    
    # 从 Keychain 补充（仅在 macOS 上）
    # 已知的 Keychain 服务名映射
    keychain_services = {
        "KEYCHAIN_NOTION_TOKEN": "longhun-notion-api",
        "KEYCHAIN_GITHUB_TOKEN": "longhun-github-token",
    }
    for env_key, kc_service in keychain_services.items():
        if env_key not in credentials or not credentials[env_key].get("value"):
            kc_value = load_keychain(kc_service)
            if kc_value:
                credentials[env_key] = {
                    "value": kc_value,
                    "source": f"macOS Keychain ({kc_service})",
                    "description": "Keychain 备用凭证",
                    "status": "active"
                }
    
    # 导出到 os.environ
    if export_to_os:
        for key, item in credentials.items():
            value = item.get("value", "")
            if value and item.get("status") != "missing":
                os.environ[key] = value
    
    return credentials


def get_credential(key: str) -> Optional[str]:
    """获取单个凭证值"""
    credentials = load_all(export_to_os=False)
    item = credentials.get(key, {})
    return item.get("value") if item.get("status") != "missing" else None


def list_services() -> Dict[str, Dict[str, Any]]:
    """列出所有服务名及状态（不含值）"""
    credentials = load_all(export_to_os=False)
    return {
        k: {
            "status": v.get("status", "unknown"),
            "description": v.get("description", ""),
            "source": v.get("source", "")
        }
        for k, v in sorted(credentials.items())
    }


# ═══════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    if "--list" in sys.argv:
        services = list_services()
        print(f"📊 已加载 {len(services)} 个凭证:\n")
        for key, info in services.items():
            status_icon = {"active": "🟢", "backup": "🟡", "missing": "🔴", "invalid": "❌"}.get(info["status"], "⚪")
            desc = info["description"] or key
            print(f"  {status_icon} {key}")
            if desc:
                print(f"     {desc} (来源: {info['source']})")
        sys.exit(0)
    
    if "--get" in sys.argv:
        idx = sys.argv.index("--get")
        key = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ""
        if key:
            val = get_credential(key)
            if val:
                print(val)
            else:
                print(f"❌ 未找到: {key}", file=sys.stderr)
                sys.exit(1)
        sys.exit(0)
    
    # 默认：加载并输出摘要
    creds = load_all()
    active = sum(1 for v in creds.values() if v.get("status") == "active")
    missing = sum(1 for v in creds.values() if v.get("status") == "missing")
    print(f"✅ 已加载 {len(creds)} 个凭证 (active={active} missing={missing})")
    print(f"   Vault: {VAULT_JSON}")
    print(f"   用法: --list 查看全部 | --get KEY 获取值")
