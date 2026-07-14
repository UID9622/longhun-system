#!/usr/bin/env python3
"""Interactive credential setup for Longhun WeChat integration."""

import getpass
from pathlib import Path


def prompt_credential(name: str, description: str, secret: bool = False) -> str:
    """Prompt user for a credential."""
    print(f"\n{name}: {description}")
    if secret:
        value = getpass.getpass(f"请输入 {name}（输入不可见）: ")
    else:
        value = input(f"请输入 {name}: ").strip()
    return value


def main():
    print("🐉 龍魂公众号智能内容中枢 - 凭证配置")
    print("=" * 50)
    print("以下信息将保存到 .env 文件，不会上传到任何服务器。")

    env_path = Path(__file__).parent / ".env"

    # Read existing if any
    existing = {}
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                existing[key.strip()] = value.strip()

    # WeChat credentials
    appid = prompt_credential(
        "WECHAT_APPID", "微信公众号的 AppID"
    ) or existing.get("WECHAT_APPID", "")
    appsecret = prompt_credential(
        "WECHAT_APPSECRET", "微信公众号的 AppSecret", secret=True
    ) or existing.get("WECHAT_APPSECRET", "")
    token = prompt_credential(
        "WECHAT_TOKEN", "服务器配置 Token（可选，接收消息推送时需要）"
    ) or existing.get("WECHAT_TOKEN", "")
    aes_key = prompt_credential(
        "WECHAT_ENCODING_AES_KEY", "消息加解密密钥（可选）", secret=True
    ) or existing.get("WECHAT_ENCODING_AES_KEY", "")

    # AI credentials
    print("\n--- AI 服务配置（可选，用于人格自动创作）---")
    kimi_key = prompt_credential(
        "KIMI_API_KEY", "Kimi API Key", secret=True
    ) or existing.get("KIMI_API_KEY", "")
    deepseek_key = prompt_credential(
        "DEEPSEEK_API_KEY", "DeepSeek API Key", secret=True
    ) or existing.get("DEEPSEEK_API_KEY", "")
    openai_key = prompt_credential(
        "OPENAI_API_KEY", "OpenAI API Key（用于 DALL-E 配图）", secret=True
    ) or existing.get("OPENAI_API_KEY", "")

    # Write .env
    env_content = f"""# 微信公众号配置（必填）
WECHAT_APPID={appid}
WECHAT_APPSECRET={appsecret}

# 服务器配置（可选）
WECHAT_TOKEN={token}
WECHAT_ENCODING_AES_KEY={aes_key}

# AI 服务配置（可选）
KIMI_API_KEY={kimi_key}
DEEPSEEK_API_KEY={deepseek_key}
OPENAI_API_KEY={openai_key}

# 龍魂系统路径
LONGHUN_SYSTEM_ROOT=~/longhun-system

# Web UI 配置
WEB_HOST=0.0.0.0
WEB_PORT=8443
"""

    env_path.write_text(env_content, encoding="utf-8")
    env_path.chmod(0o600)  # Restrict permissions

    print("\n" + "=" * 50)
    print("✅ 凭证已保存到 .env 文件")
    print(f"   路径: {env_path}")
    print("   权限: 已设置为仅所有者可读写")
    print("\n下一步：")
    print("  1. python cli.py config    # 检查配置")
    print("  2. python cli.py token     # 测试 token 获取")
    print("  3. python web_ui.py        # 启动 Web 操作台")
    print("\nDNA: #龍芯⚡️2026-06-25-LONGHUN-CREDENTIALS-SETUP-v1.0")


if __name__ == "__main__":
    main()
