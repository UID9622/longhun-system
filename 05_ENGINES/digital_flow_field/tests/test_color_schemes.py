# 龍魂系统 · 工程实现层
# License: MulanPSL v2
# DNA: #龍芯⚡️丙午·癸未·甲申-DIGITAL-FLOW-FIELD-TEST-COLOR-v2.0-UID9622

import pytest

from flow_engine.color_schemes import get_color, list_schemes


def test_all_schemes_have_all_roots():
    schemes = list_schemes()
    assert "nine" in schemes
    assert "wuxing" in schemes
    assert "grayscale" in schemes
    for scheme in schemes:
        for root in range(1, 10):
            color = get_color(root, scheme)
            assert color.startswith("#")
            assert len(color) == 7


def test_invalid_root_fallback():
    assert get_color(0) == "#888888"
    assert get_color(10) == "#888888"
    assert get_color(-1) == "#888888"


def test_scheme_names_are_chinese():
    names = list_schemes()
    assert names["nine"] == "九色"
    assert names["wuxing"] == "五行"
    assert names["grayscale"] == "灰度"
