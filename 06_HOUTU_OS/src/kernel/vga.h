/*
 * 后土 OS — VGA 文本模式驱动头文件
 * DNA: #龍芯⚡️丙午·丙申·甲寅·甲戌·兑-VGA-HEADER-v1.0
 *
 * 文化锚点：兑宫（金）— 输出表达之力
 * VGA 文本模式：80列 × 25行，显存基址 0xB8000
 * 每字符 2 字节：[字符码(1B)][属性(1B)]
 *
 * 颜色属性（低4位前景 + 高4位背景）：
 *   0=黑 1=蓝 2=绿 3=青 4=红 5=紫 6=棕 7=灰
 *   8=暗灰 9=亮蓝 A=亮绿 B=亮青 C=亮红 D=亮紫 E=黄 F=白
 */

#ifndef HOUTU_VGA_H
#define HOUTU_VGA_H

#include <stddef.h>
#include <stdint.h>

/* 九宫格方向对应的VGA颜色 */
#define COLOR_JIN 0x0E  /* 金(兑) — 黄字黑底 — 金属光泽 */
#define COLOR_SHUI 0x09 /* 水(坎) — 亮蓝字黑底 — 水之深沉 */
#define COLOR_MU 0x0A   /* 木(震巽) — 亮绿字黑底 — 木之生机 */
#define COLOR_HUO 0x0C  /* 火(离) — 亮红字黑底 — 火之热烈 */
#define COLOR_TU 0x07   /* 土(坤艮) — 灰字黑底 — 土之厚重 */
#define COLOR_TAIJI 0x0F /* 太极(中) — 白字黑底 — 阴阳合一 */

/* VGA 文本模式常量 */
#define VGA_WIDTH  80
#define VGA_HEIGHT 25
#define VGA_BUFFER ((uint16_t *)0xB8000)

/* ── 函数声明 ── */

/* 清屏 — 以指定颜色填充全屏空格 */
void houTu_vga_clear(uint8_t color);

/* 在指定位置输出字符 */
void houTu_vga_putchar(char c, uint8_t color, size_t x, size_t y);

/* 在当前光标位置输出字符（自动推进光标） */
void houTu_vga_write_char(char c, uint8_t color);

/* 输出字符串（自动换行 + 滚动） */
void houTu_vga_write_string(const char *str, uint8_t color);

/* 输出以 null 结尾的字符串 */
void houTu_vga_print(const char *str);

/* 输出带五行颜色的字符串 */
void houTu_vga_print_color(const char *str, uint8_t color);

/* 输出十六进制数值（调试用） */
void houTu_vga_print_hex(uint64_t value);

/* 设置光标位置 */
void houTu_vga_set_cursor(size_t x, size_t y);

/* 获取当前光标列 */
size_t houTu_vga_get_column(void);

/* 获取当前光标行 */
size_t houTu_vga_get_row(void);

/* 换行（带滚动） */
void houTu_vga_newline(void);

#endif /* HOUTU_VGA_H */
