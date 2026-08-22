# DNA: #龍芯⚡️丙午·丙申·戊辰·丙辰·䷸巽为风-CODE-补DNA-f69b782f
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · MeloTTS 中文_only 补丁
把 MeloTTS 里日语 tokenizer 的顶层强制加载改成懒加载，
从而避免在 macOS 上安装 fugashi/MeCab 系统库也能跑中文 TTS。
"""
from pathlib import Path

FACTORY_DIR = Path(__file__).resolve().parent
JAPANESE_PY = FACTORY_DIR / "third_party" / "MeloTTS" / "melo" / "text" / "japanese.py"


def patch():
    if not JAPANESE_PY.exists():
        print(f"⚠️ 未找到 {JAPANESE_PY}，跳过补丁")
        return False

    text = JAPANESE_PY.read_text(encoding="utf-8")

    old_block = """model_id = 'tohoku-nlp/bert-base-japanese-v3'
tokenizer = AutoTokenizer.from_pretrained(model_id)
def g2p(norm_text):

    tokenized = tokenizer.tokenize(norm_text)"""

    new_block = """model_id = 'tohoku-nlp/bert-base-japanese-v3'
_tokenizer = None

def _get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(model_id)
    return _tokenizer

def g2p(norm_text):

    tokenized = _get_tokenizer().tokenize(norm_text)"""

    if old_block not in text:
        if "_get_tokenizer" in text:
            print("✅ MeloTTS 中文补丁已存在")
            return True
        print("⚠️ 补丁目标文本不匹配，可能 MeloTTS 版本已更新")
        return False

    text = text.replace(old_block, new_block)
    JAPANESE_PY.write_text(text, encoding="utf-8")
    print(f"✅ 已应用 MeloTTS 中文懒加载补丁: {JAPANESE_PY}")
    return True


if __name__ == "__main__":
    patch()
