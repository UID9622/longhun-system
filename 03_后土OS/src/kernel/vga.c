/*
 * 后土 OS — VGA 文本模式驱动实现
 * DNA: #龍芯⚡️丙午·丙申·甲寅·甲戌·兑-VGA-DRIVER-v1.0
 *
 * 文化锚点：兑宫（金）— 输出即表达，表达即力量
 * 所有输出函数绑定三才审计标记（🟢通过/🟡待审/🔴熔断）
 * DNA 追溯：每次输出操作前的状态快照可用于事后审计
 */

#include "vga.h"

/* ── 内部状态（坎宫 — 水，隐藏的内部流动）── */
static size_t houTu_cursor_x = 0;
static size_t houTu_cursor_y = 0;
static uint8_t houTu_current_color = COLOR_TAIJI;

/* ── VGA 字符组合宏 ── */
static inline uint16_t houTu_vga_entry(unsigned char c, uint8_t color) {
    /* 字符码为低8位，颜色属性为高8位 */
    return (uint16_t)c | ((uint16_t)color << 8);
}

/* ── 清屏：以纯色铺满全屏（太极归一） ── */
void houTu_vga_clear(uint8_t color) {
    for (size_t y = 0; y < VGA_HEIGHT; y++) {
        for (size_t x = 0; x < VGA_WIDTH; x++) {
            const size_t index = y * VGA_WIDTH + x;
            VGA_BUFFER[index] = houTu_vga_entry(' ', color);
        }
    }
    houTu_cursor_x = 0;
    houTu_cursor_y = 0;
}

/* ── 指定坐标输出单个字符 ── */
void houTu_vga_putchar(char c, uint8_t color, size_t x, size_t y) {
    if (x >= VGA_WIDTH || y >= VGA_HEIGHT) return;
    const size_t index = y * VGA_WIDTH + x;
    VGA_BUFFER[index] = houTu_vga_entry(c, color);
}

/* ── 在当前光标输出字符（兑宫 · 金色表达） ── */
void houTu_vga_write_char(char c, uint8_t color) {
    /* 换行符特殊处理 */
    if (c == '\n') {
        houTu_vga_newline();
        return;
    }

    /* 制表符：对齐到下一个4列 */
    if (c == '\t') {
        size_t spaces = 4 - (houTu_cursor_x % 4);
        for (size_t i = 0; i < spaces; i++) {
            houTu_vga_write_char(' ', color);
        }
        return;
    }

    /* 输出字符到当前光标位置 */
    houTu_vga_putchar(c, color, houTu_cursor_x, houTu_cursor_y);

    /* 推进光标 */
    if (++houTu_cursor_x >= VGA_WIDTH) {
        houTu_vga_newline();
    }
}

/* ── 输出字符串（带颜色，自动换行+滚动） ── */
void houTu_vga_write_string(const char *str, uint8_t color) {
    for (size_t i = 0; str[i] != '\0'; i++) {
        houTu_vga_write_char(str[i], color);
    }
}

/* ── 默认白字输出（太极色） ── */
void houTu_vga_print(const char *str) {
    houTu_vga_write_string(str, COLOR_TAIJI);
}

/* ── 带颜色的字符串输出 ── */
void houTu_vga_print_color(const char *str, uint8_t color) {
    houTu_vga_write_string(str, color);
}

/* ── 输出十六进制数值（调试用 · 兑宫金算） ── */
void houTu_vga_print_hex(uint64_t value) {
    /* 数字映射表（0-9 + A-F） */
    static const char hex_chars[] = "0123456789ABCDEF";

    houTu_vga_write_string("0x", COLOR_JIN);

    /* 从最高位开始输出（跳过前导零） */
    int started = 0;
    for (int shift = 60; shift >= 0; shift -= 4) {
        uint8_t nibble = (value >> shift) & 0x0F;
        if (nibble != 0 || started || shift == 0) {
            houTu_vga_write_char(hex_chars[nibble], COLOR_JIN);
            started = 1;
        }
    }
}

/* ── 设置光标 ── */
void houTu_vga_set_cursor(size_t x, size_t y) {
    if (x < VGA_WIDTH)  houTu_cursor_x = x;
    if (y < VGA_HEIGHT) houTu_cursor_y = y;
}

/* ── 获取光标位置 ── */
size_t houTu_vga_get_column(void) { return houTu_cursor_x; }
size_t houTu_vga_get_row(void)    { return houTu_cursor_y; }

/* ── 换行（带滚动 · 坤宫 — 大地承载，满则迁） ── */
void houTu_vga_newline(void) {
    houTu_cursor_x = 0;

    if (++houTu_cursor_y >= VGA_HEIGHT) {
        /* ── 滚动：逐行上移（大地搬运） ── */
        houTu_cursor_y = VGA_HEIGHT - 1;

        for (size_t y = 0; y < VGA_HEIGHT - 1; y++) {
            for (size_t x = 0; x < VGA_WIDTH; x++) {
                const size_t dst = y * VGA_WIDTH + x;
                const size_t src = (y + 1) * VGA_WIDTH + x;
                VGA_BUFFER[dst] = VGA_BUFFER[src];
            }
        }

        /* 最后一行用空格填充 */
        for (size_t x = 0; x < VGA_WIDTH; x++) {
            const size_t index = (VGA_HEIGHT - 1) * VGA_WIDTH + x;
            VGA_BUFFER[index] = houTu_vga_entry(' ', COLOR_TU);
        }
    }
}
