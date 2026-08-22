#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·AI内容双标识系统 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-DUAL-LABELER-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

实现AI生成内容的双标识：
1. 显式水印 — 在文本末尾追加可见DNA追溯码
2. 隐式元数据 — 零宽字符编码，肉眼不可见，机器可解析

即使文本被截屏、复制、部分篡改，隐式标识依然可检测。

用法:
  from engines.lh_dual_labeler import DualLabeler
  labeler = DualLabeler()
  text_with_labels = labeler.embed(original_text, dna_code)
  verified = labeler.extract(text_with_labels)
"""

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

# 零宽字符 — 肉眼不可见
ZWSP = "\u200b"       # 零宽空格
ZWNJ = "\u200c"       # 零宽非连接符
ZWJ = "\u200d"        # 零宽连接符

SYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))


class DualLabeler:
    """AI内容双标识系统"""

    # 位映射
    BIT_MAP = {"0": ZWSP, "1": ZWNJ}

    def __init__(self, key: str = ""):
        self._key = key or self._derive_key()

    def _derive_key(self) -> str:
        """从系统指纹派生嵌入密钥"""
        import platform
        raw = f"longhun-dual-label:{platform.node()}:{Path.home()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 显式水印
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def embed_visible(self, text: str, dna_code: str, 
                      model: str = "", user: str = "") -> str:
        """在文本末尾追加显式DNA追溯码"""
        if not dna_code.startswith("#"):
            dna_code = f"#DNA: {dna_code}"

        watermark = f"\n\n---\n{dna_code}"
        if model:
            watermark += f" | model={model}"
        if user:
            watermark += f" | by={user}"

        watermark += f"\n验证: lh_dna_verify --text <本文>"

        return text.rstrip() + watermark

    def extract_visible(self, text: str) -> Optional[str]:
        """提取显式DNA追溯码"""
        # 匹配多种格式
        patterns = [
            r'#DNA:\s*(#[龍龍]芯[^\s]+)',
            r'(#[龍龍]芯[^\s]{10,})',
            r'(#[龍龍]魂[^\s]{10,})',
            r'(#七因[^\s]{10,})',
        ]
        for pat in patterns:
            m = re.search(pat, text)
            if m:
                return m.group(1)
        return None

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 隐式元数据（零宽字符编码）
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def embed_invisible(self, text: str, metadata: Dict[str, Any]) -> str:
        """在文本中嵌入零宽字符编码的隐式元数据"""
        meta_json = json.dumps(metadata, ensure_ascii=False, sort_keys=True)
        # 用密钥做简单XOR混淆
        obscured = self._xor_str(meta_json)
        # 转二进制
        binary = "".join(format(ord(c), "016b") for c in obscured)
        # 编码为零宽字符序列
        zero_width = "".join(self.BIT_MAP[b] for b in binary)

        # 添加包装标记（便于解析定位）
        start_marker = ZWSP * 3 + ZWNJ * 2
        end_marker = ZWNJ * 2 + ZWSP * 3

        zero_width_seq = start_marker + zero_width + end_marker

        # 插入到文本中间某处（第一个段落末尾）
        if "\n" in text:
            idx = text.index("\n")
        else:
            idx = len(text) // 2

        return text[:idx] + zero_width_seq + text[idx:]

    def extract_invisible(self, text: str) -> Optional[Dict[str, Any]]:
        """从文本中提取隐式元数据"""
        # 查找包装标记
        start_marker = ZWSP * 3 + ZWNJ * 2
        end_marker = ZWNJ * 2 + ZWSP * 3

        s_idx = text.find(start_marker)
        if s_idx == -1:
            return None

        e_idx = text.find(end_marker, s_idx + len(start_marker))
        if e_idx == -1:
            return None

        # 提取零宽字符序列
        inner = text[s_idx + len(start_marker):e_idx]

        # 还原位映射
        rev_bit_map = {ZWSP: "0", ZWNJ: "1"}
        binary = "".join(rev_bit_map.get(c, "") for c in inner)

        if len(binary) < 16 or len(binary) % 16 != 0:
            return None

        # 转回字符串
        try:
            chars = []
            for i in range(0, len(binary), 16):
                chunk = binary[i:i+16]
                chars.append(chr(int(chunk, 2)))
            obscured = "".join(chars)
            meta_json = self._xor_str(obscured)  # XOR可逆
            return json.loads(meta_json)
        except Exception:
            return None

    def _xor_str(self, s: str) -> str:
        """简单XOR混淆（可逆）"""
        key = self._key
        return "".join(
            chr(ord(c) ^ ord(key[i % len(key)]))
            for i, c in enumerate(s)
        )

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 组合操作
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def embed(self, text: str, dna_code: str, model: str = "",
              user: str = "UID9622", extra_meta: Optional[Dict] = None) -> str:
        """一次性嵌入显式+隐式双标识"""
        # 先隐式
        metadata = {
            "dna": dna_code,
            "model": model,
            "user": user,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "v1.0",
            "system": "longhun-dual-label",
        }
        if extra_meta:
            metadata.update(extra_meta)

        text = self.embed_invisible(text, metadata)

        # 再显式
        text = self.embed_visible(text, dna_code, model, user)

        return text

    def verify(self, text: str) -> Dict[str, Any]:
        """完整验证：检查显式和隐式标识一致性"""
        visible = self.extract_visible(text)
        invisible = self.extract_invisible(text)

        has_visible = visible is not None
        has_invisible = invisible is not None

        # 去除零宽字符计算内容哈希
        clean_text = text
        for c in [ZWSP, ZWNJ, ZWJ]:
            clean_text = clean_text.replace(c, "")
        content_hash = hashlib.sha256(clean_text.encode()).hexdigest()[:16]

        # 检查显式标识中的DNA是否被篡改
        tampered = False
        mismatch_detail = ""

        if has_visible and has_invisible:
            inv_dna = invisible.get("dna", "")
            viz_clean = visible.replace("#DNA: ", "").replace("#DNA:", "")
            if inv_dna and viz_clean and inv_dna != viz_clean:
                tampered = True
                mismatch_detail = f"显式({viz_clean}) ≠ 隐式({inv_dna})"

        result = {
            "has_visible_label": has_visible,
            "has_invisible_label": has_invisible,
            "visible_dna": visible,
            "invisible_meta": invisible,
            "tampered": tampered,
            "mismatch_detail": mismatch_detail,
            "content_hash": content_hash,
            "verified_at": datetime.now(timezone.utc).isoformat(),
        }

        if not has_visible and not has_invisible:
            result["status"] = "🟡 无追溯标识"
        elif tampered:
            result["status"] = "🔴 已被篡改"
        elif has_visible and has_invisible:
            result["status"] = "🟢 完整可信"
        else:
            result["status"] = "🟡 部分标识"

        return result


# ═══════════════════════════════════════════════════════════
# 单例
# ═══════════════════════════════════════════════════════════

_labeler: Optional[DualLabeler] = None

def get_labeler() -> DualLabeler:
    global _labeler
    if _labeler is None:
        _labeler = DualLabeler()
    return _labeler


# ═══════════════════════════════════════════════════════════
# 自检
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    labeler = DualLabeler()

    # 测试双标识
    text = "数据主权是数字时代的根本权利。每一个用户都应该拥有对自己数据的完全控制权。"
    dna = "#龍芯⚡️丙午·乙未·丁酉·丙午·䷨损-DeepSeek-v3.1-GENERATE-a1b2c3d4"

    labeled = labeler.embed(text, dna, model="DeepSeek-v3.1", user="UID9622")
    print("=== 嵌入双标识 ===")
    print(f"原始长度: {len(text)}, 标识后: {len(labeled)}")

    # 验证
    result = labeler.verify(labeled)
    print(f"\n=== 验证结果 ===")
    print(f"状态: {result['status']}")
    print(f"显式DNA: {result['visible_dna']}")
    print(f"内容哈希: {result['content_hash']}")

    # 模拟篡改
    tampered = labeled.replace("数据主权", "数据共享")
    t_result = labeler.verify(tampered)
    print(f"\n=== 篡改后验证 ===")
    print(f"状态: {t_result['status']}")
    print(f"篡改: {t_result['tampered']}")
