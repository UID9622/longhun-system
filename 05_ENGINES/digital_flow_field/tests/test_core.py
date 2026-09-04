# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍魂系统 · 工程实现层
# License: MulanPSL v2
# DNA: #龍芯⚡️丙午·癸未·甲申·庚午·䷙大畜-DIGITAL-FLOW-FIELD-TEST-CORE-v2.0-UID9622

import pytest

from flow_engine.core import (
    TextAnalysis,
    analyze_text,
    char_digital_root,
    distribution_to_csv_rows,
    generate_text_fingerprint,
    preprocess_text,
)


def test_char_digital_root_empty():
    assert char_digital_root("") == 0


def test_char_digital_root_ascii():
    # 'A' = 65 -> 6+5=11 -> 1+1=2
    assert char_digital_root("A") == 2
    # 'z' = 122 -> 1+2+2=5
    assert char_digital_root("z") == 5


def test_char_digital_root_chinese():
    # '道' = 36947 -> 3+6+9+4+7=29 -> 2+9=11 -> 1+1=2
    assert char_digital_root("道") == 2
    # '龍' = 40857 -> 4+0+8+5+7=24 -> 2+4=6
    assert char_digital_root("龍") == 6


def test_char_digital_root_emoji():
    # 常见 emoji 码点很大，但数字根一定在 1-9
    root = char_digital_root("🐉")
    assert 1 <= root <= 9


def test_preprocess_removes_control_chars():
    assert preprocess_text("a\x00b\u200bc") == "abc"


def test_preprocess_ignore_whitespace():
    assert preprocess_text("a b\t\nc", ignore_whitespace=True) == "abc"
    assert preprocess_text("a b\t\nc", ignore_whitespace=False) == "a b\t\nc"


def test_analyze_text_empty():
    result = analyze_text("")
    assert result.total == 0
    assert result.fingerprint == ""


def test_analyze_text_uniform_nine_roots():
    # 构造 1-9 各出现 10 次的文本
    text = "".join(chr(ord("0") + i) * 10 for i in range(1, 10))
    result = analyze_text(text)
    assert result.total == 90
    assert all(result.counts[i] == 10 for i in range(1, 10))
    assert result.chi2 < 1e-6
    assert result.is_random_like is True


def test_fingerprint_length_and_content():
    text = "ABC龍魂"
    fp = generate_text_fingerprint(text)
    assert len(fp) <= 500
    assert fp.isdigit()
    assert all("1" <= c <= "9" for c in fp)


def test_distribution_to_csv_rows():
    result = analyze_text("123456789")
    rows = distribution_to_csv_rows(result)
    assert rows[0] == ["数字根", "次数", "占比(%)"]
    assert len(rows) == 11  # 9 行数据 + 表头 + 合计
