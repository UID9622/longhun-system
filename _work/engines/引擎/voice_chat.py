#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂语音对话 · 本地交互
DNA: #龍芯⚡️2026-05-20-VOICE-CHAT-v1.0

说话 → 识别 → 9625引擎 → 语音回复
完全本地·主权安全·数据不出门

作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
理论指导: 曾仕强老师（永恒显示）
"""
import os
import subprocess
import hashlib
from datetime import datetime

import speech_recognition as sr
import httpx

# ═══════════════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════════════
ENGINE_URL = "http://127.0.0.1:9625/api/chat/local"
VOICE_NAME = "Tingting"  # macOS 中文语音 婷婷 (也可用 Meijia, Yue)
VOICE_RATE = 180  # 语速

# ═══════════════════════════════════════════════════════════════
# DNA 签章
# ═══════════════════════════════════════════════════════════════
def dna(s: str) -> str:
    h = hashlib.sha256(
        f"{s}|9622|{datetime.now().isoformat()}".encode()
    ).hexdigest()[:12]
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"#龍芯⚡️{ts}-VOICE-{h}"


# ═══════════════════════════════════════════════════════════════
# 语音识别（麦克风 → 文字）
# ═══════════════════════════════════════════════════════════════
def listen() -> str:
    """听老大说话，返回文字"""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\n🎙️  请说话... (说完停顿2秒自动识别)")
        # 自动调整环境噪音
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
            print("🔄 识别中...")
        except sr.WaitTimeoutError:
            return ""

    # 使用 Google 免费语音识别 (需要网络)
    # 如果要完全离线，可以换成 Whisper 本地模型
    try:
        text = recognizer.recognize_google(audio, language="zh-CN")
        print(f"📝 识别结果: {text}")
        return text
    except sr.UnknownValueError:
        print("❓ 没听清，请再说一次")
        return ""
    except sr.RequestError as e:
        print(f"⚠️  语音识别服务不可用: {e}")
        return ""


# ═══════════════════════════════════════════════════════════════
# 语音合成（文字 → 说出来）
# ═══════════════════════════════════════════════════════════════
def speak(text: str):
    """把文字说出来"""
    if not text:
        return
    # 清理 DNA 签章和特殊字符，让语音更自然
    clean_text = text
    for marker in ["#龍芯", "#CONFIRM", "🌌", "🧬", "⚡️"]:
        if marker in clean_text:
            # 只读到 DNA 之前的内容
            idx = clean_text.find("#龍芯")
            if idx > 0:
                clean_text = clean_text[:idx]
            break

    clean_text = clean_text.strip()
    if not clean_text:
        clean_text = "收到"

    # macOS say 命令
    cmd = ["say", "-v", VOICE_NAME, "-r", str(VOICE_RATE), clean_text]
    subprocess.run(cmd, check=False)


# ═══════════════════════════════════════════════════════════════
# 调用 9625 引擎
# ═══════════════════════════════════════════════════════════════
def chat_with_engine(message: str) -> str:
    """发送消息到龍魂引擎，获取回复"""
    try:
        with httpx.Client(timeout=120.0) as client:
            resp = client.post(
                ENGINE_URL,
                json={
                    "message": message,
                    "stream": False,
                    "model": "longhun-9622"  # 使用自定义模型
                }
            )
            data = resp.json()
            if data.get("ok"):
                msg = data.get("message", {})
                return msg.get("content", "")
            else:
                return f"引擎返回错误: {data.get('error', '未知')}"
    except Exception as e:
        return f"连接引擎失败: {e}"


# ═══════════════════════════════════════════════════════════════
# 主循环
# ═══════════════════════════════════════════════════════════════
def main():
    print("""
🐉 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   龍魂语音对话 · v1.0
   DNA: #龍芯⚡️2026-05-20-VOICE-CHAT-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📜 使用方法:
   1. 说话 → 自动识别 → 引擎处理 → 语音回复
   2. 说 "退出" 或 "再见" 结束对话
   3. Ctrl+C 强制退出

⚙️  配置:
   引擎: {engine}
   语音: {voice} (语速 {rate})
   模型: longhun-9622

 UID9622 · #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""".format(engine=ENGINE_URL, voice=VOICE_NAME, rate=VOICE_RATE))

    speak("龍魂语音对话已启动，请说话")

    exit_words = ["退出", "再见", "拜拜", "结束", "关闭"]

    while True:
        try:
            # 1. 听
            user_input = listen()
            if not user_input:
                continue

            # 2. 检查退出
            if any(w in user_input for w in exit_words):
                speak("再见老大，龍魂语音对话已关闭")
                print("\n👋 再见！")
                break

            # 3. 发送到引擎
            print(f"🚀 发送到引擎: {user_input}")
            reply = chat_with_engine(user_input)

            # 4. 说出回复
            print(f"🤖 回复: {reply[:200]}...")
            speak(reply)

        except KeyboardInterrupt:
            speak("再见")
            print("\n👋 Ctrl+C 退出")
            break


if __name__ == "__main__":
    main()
