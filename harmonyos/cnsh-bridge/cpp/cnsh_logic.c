/* 由 cnsh_cgen.py v0.1 自动生成 · 请勿手改 */
static const char* CNSH_DNA = "#龍芯⚡️2026-09-05-CNSH-CGEN-v0.1-UID9622";
static const char* CNSH_GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F";
#include <stdio.h>
#include <string.h>
#include <math.h>

static const char* cnsh_问候(const char* 名字);
static const char* cnsh_三色审计(const char* 输入);
static void cnsh_主();

static const char* cnsh_cat(const char* l, const char* r) {
    static char __cat_buf[1024];
    if (l == __cat_buf) { /* 嵌套拼接：左操作数即自身缓冲，就地追加 */
        strncat(__cat_buf, r, 1023 - strlen(__cat_buf));
        return __cat_buf;
    }
    strncpy(__cat_buf, l, 1023); __cat_buf[1023] = 0;
    strncat(__cat_buf, r, 1023 - strlen(__cat_buf));
    return __cat_buf;
}

static const char* cnsh_问候(const char* 名字) {
    return cnsh_cat(cnsh_cat("🐉 龍魂·鸿蒙，你好，", 名字), "！");
    return "";
}

static const char* cnsh_三色审计(const char* 输入) {
    if ((strcmp(输入, "") == 0)) {
        return "🔴 空输入，拒绝";
    }
    return "🟢 输入通过审计";
    return "";
}

static void cnsh_主() {
    printf("%s", cnsh_问候("鸿蒙开发者"));
    printf("\n");
    printf("%s", cnsh_三色审计("你好"));
    printf("\n");
    printf("%s", cnsh_三色审计(""));
    printf("\n");
}

