#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 标准库注入器 — stdlib_injector.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DNA追溯码：#龍芯⚡️2026-03-22-CNSH-STDLIB-v1.0
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者：诸葛鑫（UID9622）
理论指导：曾仕强老师（永恒显示）
协议：Apache License 2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

功能：在 CNSH 生成的 C 代码头部注入标准库 C 实现，
      让 CNSH 内置函数（拼接/转文本/取长度等）真正可用。
"""

# ─────────────────────────────────────────────────────
# 标准库 C 实现（注入到每个编译输出的顶部）
# ─────────────────────────────────────────────────────

STDLIB_C_CODE = r"""
/* ═══════════════════════════════════════════════════
   CNSH 标准库 v1.0
   DNA: #龍芯⚡️2026-03-22-CNSH-STDLIB-v1.0
   UID: UID9622 | 创建者: 诸葛鑫
   ═══════════════════════════════════════════════════ */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>

/* ── 内存安全：字符串缓冲区 ── */
#define CNSH_BUF_SIZE 4096
static char __cnsh_str_buf[64][CNSH_BUF_SIZE];
static int  __cnsh_buf_idx = 0;

static char* __cnsh_next_buf() {
    __cnsh_buf_idx = (__cnsh_buf_idx + 1) % 64;
    __cnsh_str_buf[__cnsh_buf_idx][0] = '\0';
    return __cnsh_str_buf[__cnsh_buf_idx];
}

/* ── io 模块 ── */

/* 打印整数 */
void 打印整数(int n) {
    printf("%d\n", n);
}

/* 打印小数 */
void 打印小数(double d) {
    printf("%g\n", d);
}

/* 打印文本 */
void 打印文本(const char* s) {
    if (s) printf("%s\n", s);
    else   printf("\n");
}

/* 打印布尔 */
void 打印真假(bool b) {
    printf("%s\n", b ? "真" : "假");
}

/* ── string 模块 ── */

/* 拼接两个字符串 */
char* 拼接(const char* a, const char* b) {
    char* buf = __cnsh_next_buf();
    if (a) strncpy(buf, a, CNSH_BUF_SIZE - 1);
    if (b) strncat(buf, b, CNSH_BUF_SIZE - 1 - strlen(buf));
    return buf;
}

/* 整数转文本 */
char* 转文本(int n) {
    char* buf = __cnsh_next_buf();
    snprintf(buf, CNSH_BUF_SIZE, "%d", n);
    return buf;
}

/* 小数转文本 */
char* 小数转文本(double d) {
    char* buf = __cnsh_next_buf();
    snprintf(buf, CNSH_BUF_SIZE, "%g", d);
    return buf;
}

/* 取字符串长度 */
int 取长度(const char* s) {
    if (!s) return 0;
    return (int)strlen(s);
}

/* 截取字符串：从 start 开始取 len 个字节 */
char* 截取(const char* s, int start, int len) {
    char* buf = __cnsh_next_buf();
    if (!s || start < 0 || len <= 0) return buf;
    int slen = (int)strlen(s);
    if (start >= slen) return buf;
    int actual = (start + len > slen) ? slen - start : len;
    strncpy(buf, s + start, actual);
    buf[actual] = '\0';
    return buf;
}

/* ── math 模块 ── */

/* 绝对值 */
int 绝对值(int n) { return abs(n); }

/* 最大值 */
int 最大值(int a, int b) { return a > b ? a : b; }

/* 最小值 */
int 最小值(int a, int b) { return a < b ? a : b; }

/* 幂运算（整数） */
int 幂(int base, int exp) {
    int result = 1;
    for (int i = 0; i < exp; i++) result *= base;
    return result;
}

/* ── time 模块 ── */

/* 获取当前时间戳（秒） */
long 时间戳() {
    return (long)time(NULL);
}

/* ── system 模块 ── */

/* 退出程序 */
void 退出(int code) {
    exit(code);
}

/* ═══════════════════════════════════════════════════
   CNSH 标准库注入完成
   ═══════════════════════════════════════════════════ */
"""


def inject_stdlib(c_code: str) -> str:
    """
    将标准库 C 实现注入到编译输出的头部（在 #include 之后）。
    如果已经注入过，跳过。
    """
    if "CNSH 标准库 v1.0" in c_code:
        return c_code  # 已注入，跳过

    # 找到第一个空行（头部注释结束后）插入标准库
    lines = c_code.split('\n')
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith('#include'):
            insert_pos = i
            break

    # 跳过所有 #include 行
    while insert_pos < len(lines) and lines[insert_pos].startswith('#include'):
        insert_pos += 1

    lines.insert(insert_pos, STDLIB_C_CODE)
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────
# 标准库函数名映射表（CNSH → C 函数名）
# 用于语义检查和错误提示
# ─────────────────────────────────────────────────────

STDLIB_FUNCTIONS = {
    # io
    '打印整数':   {'params': ['int'],          'return': 'void'},
    '打印小数':   {'params': ['double'],        'return': 'void'},
    '打印文本':   {'params': ['char*'],         'return': 'void'},
    '打印真假':   {'params': ['bool'],          'return': 'void'},
    # string
    '拼接':       {'params': ['char*', 'char*'], 'return': 'char*'},
    '转文本':     {'params': ['int'],            'return': 'char*'},
    '小数转文本': {'params': ['double'],         'return': 'char*'},
    '取长度':     {'params': ['char*'],          'return': 'int'},
    '截取':       {'params': ['char*', 'int', 'int'], 'return': 'char*'},
    # math
    '绝对值':     {'params': ['int'],           'return': 'int'},
    '最大值':     {'params': ['int', 'int'],    'return': 'int'},
    '最小值':     {'params': ['int', 'int'],    'return': 'int'},
    '幂':         {'params': ['int', 'int'],    'return': 'int'},
    # time
    '时间戳':     {'params': [],               'return': 'long'},
    # system
    '退出':       {'params': ['int'],           'return': 'void'},
}
