"""
🐉 CNSH 语法高亮引擎测试 v1.0
DNA: #龍芯⚡️2026-08-31-CNSH-HIGHLIGHT-TEST-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "08_BIN"))

from cnsh_highlight import (
    DNA_PATTERN,
    highlight_ansi,
    highlight_html_fragment,
    highlight_html_page,
)


class TestHighlightANSI(unittest.TestCase):

    def test_dna_line_gold(self):
        out = highlight_ansi('// DNA: #龍芯⚡️2026-08-31-DEMO-v1.0-UID9622')
        self.assertIn('\033[1;93m', out)  # 金色加粗

    def test_var_and_number(self):
        out = highlight_ansi('$#money = 1000')
        self.assertIn('\033[96m#money', out)  # 变量青色
        self.assertIn('\033[92m1000', out)    # 数字亮绿

    def test_chinese_operator(self):
        out = highlight_ansi('$c = $a 加 $b')
        self.assertIn('加', out)

    def test_comment_gray(self):
        out = highlight_ansi('// 这是一行注释')
        self.assertIn('\033[90m', out)  # 注释灰

    def test_string_yellow(self):
        out = highlight_ansi('输出("你好")')
        self.assertIn('\033[93m', out)  # 字符串黄

    def test_block_comment_multi_line(self):
        out = highlight_ansi('/* 开头\n中间\n结束 */\n$x = 1')
        self.assertIn('\033[90m', out)


class TestHighlightHTML(unittest.TestCase):

    def test_fragment_structure(self):
        frag = highlight_html_fragment('$#x = 1')
        self.assertTrue(frag.startswith('<pre class="cnsh-code">'))
        self.assertIn('cnsh-var', frag)
        self.assertIn('cnsh-number', frag)

    def test_escaping(self):
        frag = highlight_html_fragment('$s = "<div>"')
        self.assertNotIn('<div>', frag)  # 已转义
        self.assertIn('&lt;div&gt;', frag)

    def test_page_full(self):
        page = highlight_html_page('$x = 1', '测试')
        self.assertIn('<html', page)
        self.assertIn('<style>', page)
        self.assertIn('LonghunFont', page)  # 字体引用

    def test_dna_pattern(self):
        self.assertTrue(DNA_PATTERN.search('#龍芯⚡️2026-08-31-A-v1.0-UID9622'))
        self.assertFalse(DNA_PATTERN.search('普通文本'))


if __name__ == '__main__':
    unittest.main()
