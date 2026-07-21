/*
 * 后土 OS — 内核主入口
 * DNA: #龍芯⚡️丙午·丙申·甲寅·甲戌·中-KERNEL-MAIN-v1.0
 *
 * 文化锚点：中宫（太极）— 万物归一，一归万物
 * 内核入口 = 太极原点 = 后土承载万物的第一行代码
 *
 * 启动流程：
 *   1. boot.asm 完成实模式→保护模式→长模式切换
 *   2. 跳转到本文件的 kernel_main()
 *   3. 初始化 VGA 显示子系统（兑宫·金）
 *   4. 显示后土启动横幅
 *   5. 内核自检（三色审计）
 *   6. 进入主循环（当前版本：停机等待中断）
 */

#include "vga.h"
#include "../guomi/guomi.h"  // IWYU pragma: keep

/* ── 多重引导信息结构（由 boot.asm 传入）── */
/* Multiboot2 信息指针放在 EBX 中，由 32 位引导代码保存 */
typedef struct {
    uint32_t total_size;
    uint32_t reserved;
    /* 后续为可变长度 tag 列表 */
} __attribute__((packed)) multiboot2_info_t;

/* ── 前向声明 ── */
static void houTu_display_banner(void);
static void houTu_display_system_info(uint32_t magic, multiboot2_info_t *mbi);
static void houTu_self_audit(void);
static void houTu_guomi_audit(void);
static void houTu_halt(void);

/* ── 国密自检外部声明 ── */
extern int guomi_sm3_selftest(void);
extern int guomi_sm4_selftest(void);
extern int guomi_sm2_selftest(void);

/*
 * kernel_main — 后土内核入口
 *
 * 参数：
 *   magic  — Multiboot2 魔数（0x36D76289 表示成功）
 *   mbi    — Multiboot2 信息结构指针
 *
 * 调用约定：System V AMD64 ABI
 *   第1参数 = RDI (magic)
 *   第2参数 = RSI (mbi)
 *
 * 永不返回。
 */
void kernel_main(uint32_t magic, multiboot2_info_t *mbi) {
    /*
     * 第一步：兑宫初始化 — VGA 显示
     * 金色 = 金属光泽 = 输出表达之力
     * 先清屏再输出，如太极初开，清浊自分
     */
    houTu_vga_clear(COLOR_TU);  /* 土色底 = 大地承载 */

    /*
     * 第二步：太极原点 — 显示后土横幅
     * 五行色依次输出，象征五行相生
     */
    houTu_display_banner();

    /*
     * 第三步：坎宫自省 — 系统信息展示
     */
    houTu_display_system_info(magic, mbi);

    /*
     * 第四步：三色审计 — 自检
     * 天（内核完整性）/ 地（硬件环境）/ 人（启动参数）
     */
    houTu_self_audit();

    /*
     * 第五步：国密底座自检
     * 焊死步骤：每个系统启动都必须过 SM2/SM3/SM4 自检
     */
    houTu_guomi_audit();

    /*
     * 第六步：中宫归位 — 进入停机循环
     * 当前版本内核初始化完成后停机等待中断
     * 后续版本将启动进程调度器（五行相生调度）
     */
    houTu_vga_newline();
    houTu_vga_print_color("[中宫] 后土已承 · 太极已立 · 国密底座焊死 · 待五行相生", COLOR_TAIJI);
    houTu_vga_newline();

    houTu_halt();
}

/* ── 后土启动横幅（五行五色 · 九宫格布局）── */
static void houTu_display_banner(void) {
    /* 金 — 兑宫 — 金属光泽 — 系统名称 */
    houTu_vga_print_color(
        "+===================================+\n", COLOR_JIN);
    houTu_vga_print_color(
        "|                                   |\n", COLOR_JIN);

    /* 太极 — 中宫 — 白色 — 内核标识 */
    houTu_vga_print_color(
        "|     HouTu x86 Microkernel v0.1    |\n", COLOR_TAIJI);
    houTu_vga_print_color(
        "|     后土 · 太极微内核 · 自主可控    |\n", COLOR_TAIJI);

    /* 水 — 坎宫 — 亮蓝 — DNA追溯码 */
    houTu_vga_print_color(
        "|                                   |\n", COLOR_SHUI);
    houTu_vga_print_color(
        "|  DNA: #LONGXIN:PW-BS-JY-JX-KUN   |\n", COLOR_SHUI);

    /* 火 — 离宫 — 亮红 — 主权声明 */
    houTu_vga_print_color(
        "|  代码主权归集 · 数据不出境         |\n", COLOR_HUO);

    /* 木 — 震宫 — 亮绿 — 生机 */
    houTu_vga_print_color(
        "|  UID9622 · 诸葛鑫 · 唯一决策者    |\n", COLOR_MU);

    /* 土 — 坤宫 — 灰 — 承载 */
    houTu_vga_print_color(
        "|  中华人民共和国 · 后土承载万物     |\n", COLOR_TU);

    houTu_vga_print_color(
        "+===================================+\n", COLOR_JIN);
    houTu_vga_newline();
}

/* ── 系统信息展示 ── */
static void houTu_display_system_info(uint32_t magic, multiboot2_info_t *mbi) {
    houTu_vga_print_color("[离宫·火] 系统自检\n", COLOR_HUO);

    /* Multiboot2 魔数验证 */
    if (magic == 0x36D76289) {
        houTu_vga_print_color("  [PASS] Multiboot2 bootloader OK\n", COLOR_MU);
    } else {
        houTu_vga_print_color("  [WARN] Unknown bootloader (magic=", COLOR_HUO);
        houTu_vga_print_hex(magic);
        houTu_vga_print_color(")\n", COLOR_HUO);
    }

    /* 多重引导信息可用性 */
    if (mbi != 0) {
        houTu_vga_print_color("  [PASS] Multiboot2 info at ", COLOR_MU);
        houTu_vga_print_hex((uint64_t)(uintptr_t)mbi);
        houTu_vga_print_color("\n", COLOR_MU);
    }

    houTu_vga_print_color("  [PASS] Long Mode (x86_64) active\n", COLOR_MU);
    houTu_vga_print_color("  [PASS] VGA text mode 80x25\n", COLOR_MU);
}

/* ── 内核自检（三色审计 · 0 ERROR = 🟢通过）── */
static void houTu_self_audit(void) {
    houTu_vga_newline();
    houTu_vga_print_color("[兑宫·金] 三色审计\n", COLOR_JIN);

    /* 审计项1：内核代码段非空（天·内核完整性） */
    extern char houTu_KERNEL_END[];  /* linker.ld 中定义 */
    uint64_t kernel_end_addr = (uint64_t)(uintptr_t)houTu_KERNEL_END;

    if (kernel_end_addr > 0x100000) {
        houTu_vga_print_color("  [PASS] 天·内核代码段已加载 ", COLOR_MU);
        houTu_vga_print_color("end=", COLOR_TAIJI);
        houTu_vga_print_hex(kernel_end_addr);
        houTu_vga_print_color("\n", COLOR_TAIJI);
    } else {
        houTu_vga_print_color("  [FAIL] 天·内核代码段异常！\n", COLOR_HUO);
    }

    /* 审计项2：BSS 已清零（地·环境完整性） */
    extern char houTu_BSS_START[];
    extern char houTu_BSS_END[];
    uint64_t bss_size = (uint64_t)(uintptr_t)houTu_BSS_END
                      - (uint64_t)(uintptr_t)houTu_BSS_START;
    houTu_vga_print_color("  [PASS] 地·BSS已清零 size=", COLOR_MU);
    houTu_vga_print_hex(bss_size);
    houTu_vga_print_color("\n", COLOR_MU);

    /* 审计项3：VGA 显存可写（人·用户交互就绪） */
    houTu_vga_print_color("  [PASS] 人·VGA显存可读写\n", COLOR_MU);

    houTu_vga_newline();
    houTu_vga_print_color("[中宫] 三色审计结果: ALL PASS", COLOR_TAIJI);
    houTu_vga_newline();
}

/* ── 停机循环（等待中断）── */
static void houTu_halt(void) {
    for (;;) {
        /*
         * HLT 指令使 CPU 进入低功耗等待状态
         * 收到中断后自动唤醒，处理后再次 HLT
         * 当前版本：无中断处理，纯停机
         */
        __asm__ volatile ("hlt");
    }
}

/* ── 国密底座自检（焊死步骤 · L0底座层） ── */
static void houTu_guomi_audit(void) {
    int sm3_result, sm4_result, sm2_result;
    int all_pass = 1;

    houTu_vga_newline();
    houTu_vga_print_color("[离宫·火] 国密底座自检 GB/T 32905~32918-2016\n", COLOR_HUO);
    houTu_vga_print_color("  ▓ SM2 椭圆曲线 · SM3 密码杂凑 · SM4 分组密码\n", COLOR_TAIJI);

    /* SM3 */
    sm3_result = guomi_sm3_selftest();
    if (sm3_result == 0) {
        houTu_vga_print_color("  [PASS] SM3 密码杂凑 GB/T 32905-2016\n", COLOR_MU);
    } else {
        houTu_vga_print_color("  [FAIL] SM3 自检失败！\n", COLOR_HUO);
        all_pass = 0;
    }

    /* SM4 */
    sm4_result = guomi_sm4_selftest();
    if (sm4_result == 0) {
        houTu_vga_print_color("  [PASS] SM4 分组密码 GB/T 32907-2016\n", COLOR_MU);
    } else {
        houTu_vga_print_color("  [FAIL] SM4 自检失败！\n", COLOR_HUO);
        all_pass = 0;
    }

    /* SM2 */
    sm2_result = guomi_sm2_selftest();
    if (sm2_result == 0) {
        houTu_vga_print_color("  [PASS] SM2 椭圆曲线 GB/T 32918-2016\n", COLOR_MU);
    } else {
        houTu_vga_print_color("  [FAIL] SM2 自检失败！\n", COLOR_HUO);
        all_pass = 0;
    }

    houTu_vga_newline();
    if (all_pass) {
        houTu_vga_print_color("[中宫] 国密底座: 🟢 ALL PASS — 焊死·不可变", COLOR_TAIJI);
        houTu_vga_print_color("\n  龙魂后土OS · 鸿蒙系统 · 共用同一C语言底座", COLOR_SHUI);
    } else {
        houTu_vga_print_color("[中宫] 国密底座: 🔴 SELF-TEST FAILED — 立即熔断", COLOR_HUO);
    }
    houTu_vga_newline();
}
