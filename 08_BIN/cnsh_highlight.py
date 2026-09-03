#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 语法高亮引擎 v1.0
DNA: #龍芯⚡️2026-08-31-CNSH-HIGHLIGHT-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

深度集成: 复用 08_BIN/cnsh/lexer.py 的 CNSHLexer 词法（单一真相源），
按 token 类型做 ANSI 终端 / HTML 网页双输出高亮。
支持的呈现: 终端 `lh cnsh-highlight <文件>` · 网页 `<文件> --html` · 文档片段 `--fragment`

着色分层（与 editors/codebuddy/cnsh-syntax 的 tmLanguage 规则对齐）:
  DNA锚定=金色加粗 · 注释=灰 · 字符串=黄 · 数字=亮绿
  控制关键字=亮蓝 · 类型/系统常量=蓝 · 安全关键字=红
  内置函数=洋红 · 运算符=白 · 变量$=亮青 · 标识符=默认
"""

import argparse
import re
import sys
from pathlib import Path

# ── 关键字表（与 tmLanguage + 解释器语义对齐）──────────────────
KEYWORDS_CONTROL = (
    '定义', '函数', '返回', '如果', '否则如果', '否则', '循环', '当',
    '对于', '遍历', '中断', '继续', '导入', '导出', '模块', '变量',
    '常量', '结构体', '类型', '实现', '接口', '继承', '枚举', '使用',
)
KEYWORDS_TYPE = (
    '真', '假', '空', '整数', '浮点', '文本', '布尔', '列表',
    '字典', '集合', '元组', '字节', '文件', '输出',
)
KEYWORDS_SECURITY = (
    '熔断', '审计', '验证', '签名', '哈希', '加密', '解密', '脱敏',
    '隔离', '闸门', '一票否决', '三色', 'DNA检测', '伦理审计',
    '熔断检查', '日志记录', 'DNA追溯', '主权', '防篡改',
)
BUILTIN_FUNCS = (
    '打印', '输入', '输出', '长度', '类型', '范围', '排序', '映射', '过滤',
    '归约', '连接', '分割', '替换', '格式化', '读取文件', '写入文件',
    '发送请求', '解析JSON', '生成JSON', '哈希计算', '签名验证',
    '三色审计', '伦理检查', '闸门通行', '日志', '输出变量', '格式化输出',
)
SYSTEM_CONSTANTS = (
    'UID9622', '龍魂', 'CNSH', 'DNA', 'GPG', '锚定', '不动点', '河图',
    '洛书', '五行', '八卦', '太极', '三才', '四象', '天干', '地支', '干支',
)

DNA_PATTERN = re.compile(r'#龍芯⚡️[\u4e00-\u9fa5·䷀-䷿\-A-Za-z0-9._]+')


def _cls_set(*groups) -> frozenset:
    return frozenset(g for g in groups for g in g)


CLASSIFIED = {
    'kw': _cls_set(KEYWORDS_CONTROL, KEYWORDS_TYPE, KEYWORDS_SECURITY, SYSTEM_CONSTANTS),
    'func': frozenset(BUILTIN_FUNCS),
}


# ── ANSI 颜色表 ─────────────────────────────────────────────
ANSI = {
    'DNA':    '\033[1;93m',      # 金色加粗
    'COMMENT': '\033[90m',       # 灰
    'STRING': '\033[93m',        # 黄
    'NUMBER': '\033[92m',        # 亮绿
    'KEYWORD': '\033[1;94m',     # 亮蓝加粗
    'SECURITY': '\033[1;91m',    # 红加粗
    'FUNC':    '\033[95m',       # 洋红
    'OP':      '\033[97m',       # 白
    'VAR':     '\033[96m',       # 亮青
    'RESET':   '\033[0m',
}


def _classify(token) -> str:
    """token → 高亮类名"""
    t = token.type
    v = token.value
    if t in ('VAR',):
        return 'VAR'
    if t in ('STRING',):
        return 'STRING'
    if t in ('NUMBER',):
        return 'NUMBER'
    if t in ('IDENTIFIER',):
        if v in CLASSIFIED['func']:
            return 'FUNC'
        if v in KEYWORDS_SECURITY:
            return 'SECURITY'
        if v in CLASSIFIED['kw']:
            return 'KEYWORD'
        return 'IDENT'
    # 运算符（含中文运算符）
    if t in ('ASSIGN', 'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD', 'AND', 'OR', 'NOT',
             'EQ', 'NEQ', 'GT', 'LT', 'GTE', 'LTE', 'LPAREN', 'RPAREN',
             'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'COMMA', 'SEMICOLON',
             'DOT', 'COLON', 'BANG', 'AMP', 'PIPE', 'LT_ASCII', 'GT_ASCII',
             'SYMBOL'):
        return 'OP'
    return 'IDENT'


def _render_line_ansi(line: str, in_block: bool) -> tuple:
    """单行 ANSI 高亮。返回 (html片段, 是否仍处于块注释)"""
    if DNA_PATTERN.search(line):
        # 全行金色（DNA 锚定优先于一切）
        return ANSI['DNA'] + line + ANSI['RESET'], in_block

    if in_block:
        # 块注释中：整行灰（若含 */ 则出块）
        out = ANSI['COMMENT'] + line + ANSI['RESET']
        if '*/' in line:
            return out, False
        return out, True

    if line.lstrip().startswith('//'):
        return ANSI['COMMENT'] + line + ANSI['RESET'], in_block

    # 行内尾部注释切分
    code_part = line
    comment_part = None
    if '//' in line:
        code_part, comment_part = line.split('//', 1)
        comment_part = '//' + comment_part

    # 块注释起点
    block_started = False
    if '/*' in code_part:
        idx = code_part.index('/*')
        pre, rest = code_part[:idx], code_part[idx:]
        if '*/' in rest:
            post = rest.split('*/', 1)
            block_chunk = ANSI['COMMENT'] + post[0] + '*/' + ANSI['RESET']
            block_started = False
            mid = pre + block_chunk
            tail_code = post[1] if len(post) > 1 else ''
            code_part = mid + tail_code
        else:
            block_started = True
            mid = code_part[:idx]
            block_chunk = ANSI['COMMENT'] + rest + ANSI['RESET']
            code_part = mid + block_chunk

    out = _ansi_tokens(code_part)
    if comment_part:
        out += ANSI['COMMENT'] + comment_part + ANSI['RESET']
    return out, block_started or in_block


def _ansi_tokens(line: str) -> str:
    """用 CNSHLexer 对片段着色"""
    from cnsh.lexer import CNSHLexer
    lexer = CNSHLexer(line)
    parts = []
    for tok in lexer.tokenize():
        if tok.type == 'NEWLINE':
            continue
        cls = _classify(tok)
        parts.append(ANSI.get(cls, ANSI['RESET']) + tok.value + ANSI['RESET'])
    return ''.join(parts) if parts else line


def highlight_ansi(source: str) -> str:
    """整段 CNSH 源码 → ANSI 彩色文本"""
    lines = source.split('\n')
    in_block = False
    out = []
    for ln in lines:
        rendered, in_block = _render_line_ansi(ln, in_block)
        out.append(rendered)
    return '\n'.join(out)


# ── HTML 输出 ───────────────────────────────────────────────
HTML_CSS = """/* CNSH 语法高亮 · DNA: #龍芯⚡️2026-08-31-CNSH-HIGHLIGHT-v1.0-UID9622 */
.cnsh-code { font-family: 'LonghunFont', 'PingFang SC', 'Microsoft YaHei', monospace;
             font-size: 14px; line-height: 1.6; background: #0d1117;
             color: #e6edf3; padding: 16px; border-radius: 8px; overflow-x: auto; }
.cnsh-dna { color: #f0b429; font-weight: bold; }
.cnsh-comment { color: #8b949e; font-style: italic; }
.cnsh-string { color: #f2cc60; }
.cnsh-number { color: #7ee787; }
.cnsh-keyword { color: #58a6ff; font-weight: bold; }
.cnsh-security { color: #ff7b72; font-weight: bold; }
.cnsh-func { color: #d2a8ff; }
.cnsh-op { color: #c9d1d9; }
.cnsh-var { color: #79c0ff; }
.cnsh-ident { color: #e6edf3; }
"""

HTML_MAP = {
    'DNA': 'cnsh-dna', 'COMMENT': 'cnsh-comment', 'STRING': 'cnsh-string',
    'NUMBER': 'cnsh-number', 'KEYWORD': 'cnsh-keyword', 'SECURITY': 'cnsh-security',
    'FUNC': 'cnsh-func', 'OP': 'cnsh-op', 'VAR': 'cnsh-var', 'IDENT': 'cnsh-ident',
}


def _render_line_html(line: str, in_block: bool) -> tuple:
    """单行 HTML 高亮（转义+span）。返回 (片段, 块注释状态)"""
    if DNA_PATTERN.search(line):
        return '<span class="cnsh-dna">%s</span>' % _esc(line), in_block
    if in_block:
        out = '<span class="cnsh-comment">%s</span>' % _esc(line)
        return (out, False) if '*/' in line else (out, True)
    if line.lstrip().startswith('//'):
        return '<span class="cnsh-comment">%s</span>' % _esc(line), in_block

    code_part = line
    comment_part = None
    if '//' in line:
        code_part, comment_part = line.split('//', 1)
        comment_part = '//' + comment_part

    block_started = False
    if '/*' in code_part:
        idx = code_part.index('/*')
        pre, rest = code_part[:idx], code_part[idx:]
        if '*/' in rest:
            post = rest.split('*/', 1)
            block_chunk = '<span class="cnsh-comment">%s</span>' % _esc(post[0] + '*/')
            block_started = False
            code_part = pre + block_chunk + (post[1] if len(post) > 1 else '')
        else:
            block_started = True
            code_part = pre + '<span class="cnsh-comment">%s</span>' % _esc(rest)

    out = _html_tokens(code_part)
    if comment_part:
        out += '<span class="cnsh-comment">%s</span>' % _esc(comment_part)
    return out, block_started or in_block


def _esc(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _html_tokens(line: str) -> str:
    from cnsh.lexer import CNSHLexer
    lexer = CNSHLexer(line)
    parts = []
    for tok in lexer.tokenize():
        if tok.type == 'NEWLINE':
            continue
        cls = _classify(tok)
        cls_name = HTML_MAP.get(cls, 'cnsh-ident')
        parts.append('<span class="%s">%s</span>' % (cls_name, _esc(tok.value)))
    return ''.join(parts) if parts else _esc(line)


def highlight_html_fragment(source: str) -> str:
    """CNSH 源码 → <pre class="cnsh-code">HTML 片段（可嵌入任意网页）"""
    lines = source.split('\n')
    in_block = False
    out = []
    for ln in lines:
        rendered, in_block = _render_line_html(ln, in_block)
        out.append(rendered)
    return '<pre class="cnsh-code">' + '\n'.join(out) + '</pre>'


def highlight_html_page(source: str, title: str = 'CNSH 代码') -> str:
    """CNSH 源码 → 完整 HTML 页面（含字体引用）"""
    return (
        '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>%s</title>\n<style>%s</style>\n</head>\n<body style="margin:0;padding:16px;'
        'background:#0d1117;">\n%s\n</body>\n</html>\n'
    ) % (_esc(title), HTML_CSS, highlight_html_fragment(source))


# ── CLI ─────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        prog='lh cnsh-highlight',
        description='🐉 CNSH 语法高亮引擎 v1.0 · 复用 CNSHLexer 词法 · ANSI/HTML 双输出',
    )
    parser.add_argument('file', nargs='?', help='.cnsh 源码文件')
    parser.add_argument('--code', type=str, help='直接高亮代码字符串')
    parser.add_argument('--html', action='store_true', help='输出 HTML 片段')
    parser.add_argument('--page', action='store_true', help='输出完整 HTML 页面')
    parser.add_argument('--out', type=str, help='输出到文件（UTF-8）')
    parser.add_argument('--title', default='CNSH 代码', help='HTML 页面标题')
    args = parser.parse_args()

    if args.file:
        source = Path(args.file).read_text(encoding='utf-8')
    elif args.code:
        source = args.code
    else:
        source = sys.stdin.read()

    if args.page:
        result = highlight_html_page(source, args.title)
    elif args.html:
        result = highlight_html_fragment(source)
    else:
        result = highlight_ansi(source)

    if args.out:
        Path(args.out).write_text(result, encoding='utf-8')
        print(f'✅ 已写出: {args.out}')
    else:
        sys.stdout.write(result)
        sys.stdout.write('\n' if not result.endswith('\n') else '')


if __name__ == '__main__':
    main()
