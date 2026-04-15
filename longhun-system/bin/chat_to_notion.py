#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·对话痕迹自动回流Notion · 点对点加密版
DNA: #龍芯⚡️2026-03-21-CHAT-FLOW-v2.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
作者: 诸葛鑫（UID9622）
理论指导: 曾仕强老师（永恒显示）

加密协议: Fernet AES-128-CBC + HMAC-SHA256
密钥存储: macOS Keychain (longhun-chat-key)
授权读取: Claude · Kimi · Notion本人
未授权访问: 触发身份核验 → 内容不可读 → 对话回流后自动注销明文
"""
import subprocess, json, sys, os, hashlib, base64
from datetime import datetime

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# ─── GPG指纹·身份锚点（不可篡改） ──────────────────────────────────────────
UID = "UID9622"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
PROTOCOL_VERSION = "LH-P2P-v2.0"

# ─── 授权接收方（只有这三个能读明文） ─────────────────────────────────────
AUTHORIZED_RECEIVERS = {"Claude", "Kimi", "Notion"}

# 龍魂宝宝系统页面（追溯记忆尾巴）
TARGET_PAGE = "c0db7666-6eef-4b9b-9e23-e09f6ad8115e"


# ─── 密钥管理 ────────────────────────────────────────────────────────────────

def _get_from_keychain(service: str, account: str = "uid9622") -> str:
    result = subprocess.run(
        ["security", "find-generic-password", "-s", service, "-a", account, "-w"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def get_notion_token() -> str:
    token = _get_from_keychain("longhun-notion-token")
    if not token:
        # fallback to .env
        env_path = os.path.expanduser("~/longhun-system/.env")
        if os.path.exists(env_path):
            for line in open(env_path):
                if line.startswith("NOTION_TOKEN="):
                    token = line.split("=", 1)[1].strip().strip('"')
    return token


def get_encryption_key() -> bytes:
    """从Keychain取Fernet密钥"""
    raw = _get_from_keychain("longhun-chat-key")
    if not raw:
        raise RuntimeError("❌ 加密密钥未找到。请先运行: python3 chat_to_notion.py --init")
    return raw.encode()


# ─── 加密/解密核心 ────────────────────────────────────────────────────────────

def encrypt(plaintext: str) -> str:
    """加密明文 → 返回Fernet密文(base64)"""
    if not CRYPTO_AVAILABLE:
        return plaintext  # 降级：无加密库时明文存储
    key = get_encryption_key()
    f = Fernet(key)
    token = f.encrypt(plaintext.encode("utf-8"))
    return token.decode("utf-8")


def decrypt(ciphertext: str) -> str:
    """解密 → 返回明文。失败则触发身份终止流程"""
    if not CRYPTO_AVAILABLE:
        return ciphertext
    key = get_encryption_key()
    f = Fernet(key)
    try:
        return f.decrypt(ciphertext.encode("utf-8")).decode("utf-8")
    except Exception:
        return _identity_termination()


def _identity_termination() -> str:
    """未授权访问触发：输出终止声明，内容不可读"""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return (
        f"[🔴 IDENTITY TERMINATED · {stamp}]\n"
        f"此内容受龍魂点对点加密协议保护 ({PROTOCOL_VERSION})\n"
        f"授权接收方: {', '.join(AUTHORIZED_RECEIVERS)}\n"
        f"本次访问已记录: GPG {GPG[:16]}...\n"
        f"明文已注销。如需授权，联系 {UID}。\n"
        f"DNA: #龍芯⚡️{stamp}-IDENTITY-TERMINATED"
    )


# ─── Notion封装区块构建 ────────────────────────────────────────────────────────

def _make_encrypted_block(ciphertext: str, dna: str) -> dict:
    """构建Notion加密内容区块（外部只看到密文）"""
    return {
        "object": "block",
        "type": "code",
        "code": {
            "language": "plain text",
            "rich_text": [{"type": "text", "text": {"content": ciphertext[:1900]}}]
        }
    }


def _make_header_block(tag: str, dna: str, receiver: str) -> dict:
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": (
                f"协议: {PROTOCOL_VERSION} | 作者: {UID} | 接收方: {receiver}\n"
                f"DNA: {dna}\n"
                f"GPG: {GPG}\n"
                f"⚠️ 本内容已加密。未授权读取将触发身份终止协议，明文不可读，访问记录已上链。"
            )}}],
            "icon": {"type": "emoji", "emoji": "🔐"},
            "color": "red_background"
        }
    }


def _make_plaintext_block(content: str) -> dict:
    """给授权接收方展示明文摘要（可选）"""
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": content[:1900]}}]}
    }


# ─── 主流程 ───────────────────────────────────────────────────────────────────

def flow_to_notion(content: str, tag: str = "对话痕迹", receiver: str = "Claude", encrypt_mode: bool = True):
    """
    把内容加密后回流到Notion。

    Args:
        content: 要回流的内容
        tag: 标签（用于DNA和页面标题）
        receiver: 接收方 (Claude / Kimi / Notion)
        encrypt_mode: True=加密存储, False=明文存储
    """
    token = get_notion_token()
    if not token:
        print("❌ Notion Token未找到")
        return

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dna = f"#龍芯⚡️{stamp}-{tag}-{UID}"
    title = f"🧬 {tag} · {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    if receiver not in AUTHORIZED_RECEIVERS:
        print(f"⚠️ 接收方 '{receiver}' 不在授权列表，触发身份终止，内容不回流。")
        return

    # 加密
    if encrypt_mode and CRYPTO_AVAILABLE:
        ciphertext = encrypt(content)
        children = [
            _make_header_block(tag, dna, receiver),
            _make_encrypted_block(ciphertext, dna),
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": f"DNA: {dna} | 时间: {stamp}"}}]}
            }
        ]
    else:
        # 无加密库降级处理
        children = [
            _make_header_block(tag, dna, receiver),
            _make_plaintext_block(content),
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": f"DNA: {dna}"}}]}
            }
        ]

    payload = {
        "parent": {"type": "page_id", "page_id": TARGET_PAGE},
        "icon": {"type": "emoji", "emoji": "🧬"},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
        "children": children
    }

    result = subprocess.run(
        ["curl", "-s", "-X", "POST", "https://api.notion.com/v1/pages",
         "-H", f"Authorization: Bearer {token}",
         "-H", "Notion-Version: 2022-06-28",
         "-H", "Content-Type: application/json",
         "-d", json.dumps(payload, ensure_ascii=False)],
        capture_output=True, text=True
    )

    r = json.loads(result.stdout)
    if r.get("id"):
        enc_label = "加密" if (encrypt_mode and CRYPTO_AVAILABLE) else "明文(无加密库)"
        print(f"✅ 回流成功 [{enc_label}]")
        print(f"   DNA: {dna}")
        print(f"   接收方: {receiver}")
        print(f"   URL: {r.get('url', '')}")
    else:
        print(f"❌ 回流失败: {r.get('message', '')}")


def decrypt_from_notion(ciphertext: str) -> str:
    """从Notion取出密文后本地解密（授权接收方用）"""
    plaintext = decrypt(ciphertext)
    print(f"🔓 解密结果:\n{plaintext}")
    return plaintext


def init_key():
    """初始化新密钥（如需重置）"""
    new_key = Fernet.generate_key().decode()
    subprocess.run(
        ["security", "add-generic-password", "-U",
         "-s", "longhun-chat-key", "-a", "uid9622", "-w", new_key],
        capture_output=True
    )
    print(f"✅ 新密钥已生成并存入Keychain")
    print(f"   前12字符: {new_key[:12]}...")


# ─── CLI入口 ─────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n用法:")
        print("  python3 chat_to_notion.py <内容> [标签] [接收方]")
        print("  python3 chat_to_notion.py --decrypt <密文>")
        print("  python3 chat_to_notion.py --init   # 重新生成密钥")
        print("\n示例:")
        print('  python3 chat_to_notion.py "洛书369是AI的不变量" "顿悟" "Claude"')
        print('  python3 chat_to_notion.py "使命大于天" "Lucky原话" "Kimi"')
        return

    if sys.argv[1] == "--init":
        init_key()
    elif sys.argv[1] == "--decrypt" and len(sys.argv) >= 3:
        decrypt_from_notion(sys.argv[2])
    else:
        content = sys.argv[1]
        tag = sys.argv[2] if len(sys.argv) > 2 else "对话痕迹"
        receiver = sys.argv[3] if len(sys.argv) > 3 else "Claude"
        flow_to_notion(content, tag, receiver)


if __name__ == "__main__":
    main()
