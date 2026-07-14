"""语音合成示例 — 不同人格不同音色

⚠️ 语音合成仍为 Preview，需对接 XTTS-v2 引擎后可用。
"""

from longhun.voice import PersonaVoice

pv = PersonaVoice()

# P02 龍芯 — 干练干脆
pv.set_persona("P02")
print(f"[P02 龍芯] 音高={pv.set_persona('P02').pitch} 语速={pv.set_persona('P02').speed} 风格={pv.set_persona('P02').style}")

# P00 文心 — 沉稳厚重
print(f"[P00 文心] 音高={pv.set_persona('P00').pitch} 语速={pv.set_persona('P00').speed} 风格={pv.set_persona('P00').style}")

# P05 上帝之眼 — 冷峻精准
print(f"[P05 上帝之眼] 音高={pv.set_persona('P05').pitch} 语速={pv.set_persona('P05').speed} 风格={pv.set_persona('P05').style}")

# 宝宝 — 温暖柔和
print(f"[宝宝] 音高={pv.set_persona('宝宝').pitch} 语速={pv.set_persona('宝宝').speed} 风格={pv.set_persona('宝宝').style}")

# TTS 合成（Preview·需XTTS-v2）
try:
    result = pv.speak("系统安全检查完毕。")
    print(f"合成: {result.duration:.1f}s | {result.format}")
except NotImplementedError:
    print("TTS 引擎待对接（XTTS-v2），音色配置已就绪。")
