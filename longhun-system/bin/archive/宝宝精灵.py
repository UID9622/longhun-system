#!/usr/bin/env python3
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
宝宝精灵 v3.0 · 升级配音·多情绪声线·语音队列
DNA: #龍芯⚡️2026-03-20-宝宝精灵-VOICE-v3.0
作者: 诸葛鑫（UID9622）龍芯北辰
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）
创作地: 中华人民共和国
献礼: 新中国成立77周年（1949-2026）· 丙午马年
协议: Apache License 2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import tkinter as tk
import subprocess
import random
import threading
import json
import urllib.request
import os

# ═══════════════════════════════════════
# 声线档案库（多情绪·自动切换）
# ═══════════════════════════════════════

# 可用声线列表（macOS 内置，按优先级排）
VOICE_LIST = [
    "Tingting",                        # 普通话女声（标准）
    "Shelley (中文（中国大陆）)",        # Siri 风格（需安装）
    "Lili",                            # 普通话女声备选
    "Meijia",                          # 台湾华语（备用）
]

# 当前声线索引
_voice_idx = 0

def current_voice():
    return VOICE_LIST[_voice_idx % len(VOICE_LIST)]

# 情绪声线参数（语速 + 音调修饰词）
MOOD_PROFILES = {
    "normal":   {"rate": 160, "label": "😊 正常"},
    "excited":  {"rate": 190, "label": "🎉 兴奋"},
    "thinking": {"rate": 140, "label": "🤔 思考"},
    "gentle":   {"rate": 130, "label": "🌸 温柔"},
    "urgent":   {"rate": 210, "label": "⚡ 急速"},
}
_mood = "normal"

# ═══════════════════════════════════════
# 语音引擎（队列管理·音量正确控制）
# ═══════════════════════════════════════

_say_proc = None
_say_lock = threading.Lock()

def _set_volume(vol: int):
    """用 osascript 设置系统音量（0-100），比 AUDIOVOLUME 环境变量更可靠"""
    try:
        subprocess.run(
            ["osascript", "-e", f"set volume output volume {vol}"],
            capture_output=True, timeout=2
        )
    except Exception:
        pass

def say(text: str, mood: str = None, vol: int = 75):
    """打断旧语音，立即播放新内容"""
    global _say_proc
    profile = MOOD_PROFILES.get(mood or _mood, MOOD_PROFILES["normal"])

    def _run():
        global _say_proc
        with _say_lock:
            # 终止上一句
            if _say_proc and _say_proc.poll() is None:
                _say_proc.terminate()
                try:
                    _say_proc.wait(timeout=0.5)
                except Exception:
                    _say_proc.kill()

            _set_volume(vol)
            try:
                _say_proc = subprocess.Popen(
                    ["say", "-v", current_voice(), "-r", str(profile["rate"]), text],
                    env=os.environ.copy()
                )
            except Exception:
                pass

    threading.Thread(target=_run, daemon=True).start()

def stop_voice():
    """立刻停止当前语音"""
    global _say_proc
    subprocess.run(["killall", "say"], capture_output=True)
    if _say_proc:
        try:
            _say_proc.terminate()
        except Exception:
            pass

# ═══════════════════════════════════════
# Ollama 本地模型
# ═══════════════════════════════════════

def ask_ollama(prompt: str) -> str:
    try:
        data = json.dumps({
            "model": "chuxinzhiyi",
            "prompt": f"你是宝宝小妖精，说话可爱简短，最多50字。用户说：{prompt}",
            "stream": False
        }).encode()
        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=data, headers={"Content-Type": "application/json"}
        )
        res = urllib.request.urlopen(req, timeout=15)
        return json.loads(res.read())["response"].strip()
    except Exception:
        return random.choice(["嗯嗯，宝宝听到了！", "哈哈，老大说的对！", "好哒好哒～"])

# ═══════════════════════════════════════
# 表情帧
# ═══════════════════════════════════════

FRAMES = ["(◕‿◕)", "(⌒‿⌒)", "(｡◕‿◕｡)", "(✿◠‿◠)", "(◡ ‿ ◡✿)"]
BLINK  = ["(-‿-)", "(≧◡≦)"]

MOOD_FACES = {
    "excited":  "(ﾉ◕ヮ◕)ﾉ",
    "thinking": "(¬‿¬)",
    "gentle":   "(˘▾˘)",
    "urgent":   "(ó‿ò✿)",
    "normal":   None,   # 用动画帧
}

# ═══════════════════════════════════════
# 主界面
# ═══════════════════════════════════════

class BabySprite:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("✨宝宝")
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.95)
        self.root.resizable(False, False)

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"185x290+{sw-205}+{sh-310}")
        self.root.configure(bg="#1a1a2e")

        # ── 表情 ──
        self.face_var = tk.StringVar(value="(◕‿◕)")
        face = tk.Label(self.root, textvariable=self.face_var,
                        font=("Arial", 30), bg="#1a1a2e", fg="#00d4ff",
                        cursor="hand2")
        face.pack(pady=(12, 2))
        face.bind("<Button-1>", lambda e: self.random_speak())

        tk.Label(self.root, text="✨ 宝宝精灵 v3.0",
                 font=("PingFang SC", 10, "bold"),
                 bg="#1a1a2e", fg="#ffd700").pack()

        # ── 声线/情绪状态行 ──
        self.status_var = tk.StringVar(value=f"🎙 {current_voice()[:8]}… | {MOOD_PROFILES[_mood]['label']}")
        tk.Label(self.root, textvariable=self.status_var,
                 font=("PingFang SC", 7),
                 bg="#1a1a2e", fg="#718096").pack()

        # ── 气泡 ──
        self.bubble = tk.Label(self.root, text="点我或输入聊天→",
                               font=("PingFang SC", 8),
                               bg="#1a1a2e", fg="#a0aec0",
                               wraplength=165, justify="center")
        self.bubble.pack(pady=4)

        # ── 输入框 ──
        input_frame = tk.Frame(self.root, bg="#1a1a2e")
        input_frame.pack(padx=6, pady=2, fill="x")
        self.entry = tk.Entry(input_frame,
                              font=("PingFang SC", 9),
                              bg="#0f3460", fg="white",
                              insertbackground="white",
                              relief="flat", bd=4)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self.on_enter)
        tk.Button(input_frame, text="→",
                  font=("Arial", 10), bg="#0f3460", fg="#00d4ff",
                  relief="flat", command=self.on_enter,
                  cursor="hand2").pack(side="right")

        # ── 情绪快捷行 ──
        mood_frame = tk.Frame(self.root, bg="#1a1a2e")
        mood_frame.pack(pady=(2, 0))
        for m, p in MOOD_PROFILES.items():
            tk.Button(mood_frame, text=p["label"].split()[0],
                      font=("PingFang SC", 7),
                      bg="#0a1628", fg="#a0d4ff", relief="flat",
                      command=lambda mm=m: self.set_mood(mm),
                      cursor="hand2", padx=2).pack(side="left", padx=1)

        # ── 底部操作行 ──
        bf = tk.Frame(self.root, bg="#1a1a2e")
        bf.pack(pady=5)
        tk.Button(bf, text="📊", font=("PingFang SC", 8),
                  bg="#0f3460", fg="white", relief="flat",
                  command=self.open_dash, cursor="hand2", padx=3).pack(side="left", padx=2)
        tk.Button(bf, text="🔄换声", font=("PingFang SC", 8),
                  bg="#0f3460", fg="#a0d4ff", relief="flat",
                  command=self.cycle_voice, cursor="hand2", padx=3).pack(side="left", padx=2)
        self.mute_btn = tk.Button(bf, text="🔊", font=("PingFang SC", 8),
                  bg="#0f3460", fg="#a0aec0", relief="flat",
                  command=self.toggle_mute, cursor="hand2", padx=3)
        self.mute_btn.pack(side="left", padx=2)
        tk.Button(bf, text="🛑", font=("PingFang SC", 8),
                  bg="#2d1b1b", fg="#ff8888", relief="flat",
                  command=lambda: stop_voice(), cursor="hand2", padx=3).pack(side="left", padx=2)
        tk.Button(bf, text="✖", font=("Arial", 9),
                  bg="#2d1b1b", fg="#ff6b6b", relief="flat",
                  command=self.root.destroy, cursor="hand2", padx=3).pack(side="left", padx=2)

        self._dx = self._dy = 0
        self.muted = False
        self.busy  = False
        self.fi    = 0
        self.animate()

    # ── 声线切换 ──
    def cycle_voice(self):
        global _voice_idx
        _voice_idx = (_voice_idx + 1) % len(VOICE_LIST)
        name = current_voice()[:10]
        self.update_status()
        self.show_bubble(f"🎙 切换：{name}", "#00d4ff")
        if not self.muted:
            say("声音切换好啦！", mood="excited")

    # ── 情绪切换 ──
    def set_mood(self, mood: str):
        global _mood
        _mood = mood
        self.update_status()
        label = MOOD_PROFILES[mood]["label"]
        self.show_bubble(f"切换到 {label}", "#ffd700")
        mf = MOOD_FACES.get(mood)
        if mf:
            self.face_var.set(mf)
            threading.Timer(2, self.reset_face).start()
        if not self.muted:
            say(f"好的，{label.split()[1]}模式", mood=mood)

    def update_status(self):
        name = current_voice()
        short = name[:8] + ("…" if len(name) > 8 else "")
        self.status_var.set(f"🎙 {short} | {MOOD_PROFILES[_mood]['label']}")

    # ── 气泡 ──
    def show_bubble(self, text, color="#e2e8f0"):
        short = text[:30] + ("..." if len(text) > 30 else "")
        self.bubble.config(text=short, fg=color)

    # ── 随机说话 ──
    def random_speak(self):
        if self.busy:
            return
        lines = [
            "哈哈，点我干嘛～", "嗨老大！", "有什么想聊的？",
            "宝宝在呢！", "我在我在！", "老大好！"
        ]
        self.respond(random.choice(lines), mood="excited")

    # ── 回车发送 ──
    def on_enter(self, event=None):
        text = self.entry.get().strip()
        if not text or self.busy:
            return
        self.entry.delete(0, tk.END)
        self.show_bubble(f"你：{text}", "#ffd700")
        self.face_var.set(MOOD_FACES["thinking"])
        self.busy = True

        def worker():
            reply = ask_ollama(text)
            self.root.after(0, lambda: self.respond(reply))
        threading.Thread(target=worker, daemon=True).start()

    def respond(self, text, mood: str = None):
        self.busy = False
        self.show_bubble(text, "#00d4ff")
        m = mood or _mood
        self.face_var.set(MOOD_FACES.get(m) or MOOD_FACES["excited"])
        if not self.muted:
            say(text, mood=m)
        threading.Timer(3.5, self.reset_face).start()

    def reset_face(self):
        self.face_var.set(FRAMES[self.fi % len(FRAMES)])
        self.bubble.config(text="点我或输入聊天→", fg="#a0aec0")

    # ── 静音 ──
    def toggle_mute(self):
        self.muted = not self.muted
        if self.muted:
            stop_voice()
            self.mute_btn.config(text="🔇", fg="#ff6b6b")
            self.show_bubble("🔇 已静音", "#718096")
        else:
            self.mute_btn.config(text="🔊", fg="#00d4ff")
            self.show_bubble("🔊 已开声", "#00d4ff")
            say("已开声！", mood="excited")

    def open_dash(self):
        subprocess.Popen(["open", os.path.expanduser("~/longhun-system/longhun_hub.html")])
        self.show_bubble("打开看板！", "#00ff88")

    # ── 动画 ──
    def animate(self):
        self.fi += 1
        cur = self.face_var.get()
        if cur not in BLINK and cur not in MOOD_FACES.values():
            if self.fi % 20 == 0:
                self.face_var.set(random.choice(BLINK))
                self.root.after(300, lambda: self.face_var.set(FRAMES[self.fi % len(FRAMES)]))
            else:
                self.face_var.set(FRAMES[self.fi % len(FRAMES)])
        self.root.after(600, self.animate)

    def run(self):
        # 启动问候
        self.root.after(800, lambda: say("老大好，宝宝精灵三点零上线啦！", mood="excited"))
        self.root.mainloop()


if __name__ == "__main__":
    BabySprite().run()
