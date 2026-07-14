/*
 * 后土 OS 内核链接脚本
 * DNA: #龍芯⚡️丙午·丙申·甲寅·甲戌·坤-OS-LINKER-v1.0
 * 太极微内核 · 河图洛书九宫格内存布局
 *
 * 内存布局：
 *   - 内核代码段 (.text)    : 0x100000 (1MB) — 太极原点
 *   - 只读数据段 (.rodata)  : 紧随 .text
 *   - 数据段 (.data)        : 紧随 .rodata
 *   - BSS 段 (.bss)         : 紧随 .data，启动时清零
 *   - 内核栈               : 在 BSS 内分配 64KB
 *
 * 九宫格映射：
 *   4(巽)  9(离)  2(坤)
 *   3(震)  5(中)  7(兑)  ← 中宫为内核核心区
 *   8(艮)  1(坎)  6(乾)
 */

ENTRY(_start)

SECTIONS
{
    /* 太极原点：内核加载于 1MB 处（坎宫，水，内存之本） */
    . = 1M;

    /* ── 阳：代码段（兑宫，金，指令执行力）── */
    .text : ALIGN(4096)
    {
        *(.multiboot2)
        *(.text)
        *(.text.*)
    }

    /* ── 阴：只读数据段（坤宫，土，承载静态真理）── */
    .rodata : ALIGN(4096)
    {
        *(.rodata)
        *(.rodata.*)
    }

    /* ── 阳中之阴：初始化数据段（离宫，火，初始状态）── */
    .data : ALIGN(4096)
    {
        *(.data)
        *(.data.*)
    }

    /* ── 阴中之阳：BSS 段（坎宫，水，动态生长）── */
    .bss : ALIGN(4096)
    {
        *(COMMON)
        *(.bss)
        *(.bss.*)
    }

    /* 符号导出：BSS 起止地址（启动代码用于清零） */
    houTu_BSS_START = ADDR(.bss);
    houTu_BSS_END   = ADDR(.bss) + SIZEOF(.bss);

    /* 内核结束标记（用于内存管理器） */
    houTu_KERNEL_END = .;
}
