; ==============================================================================
; 后土 OS — x86_64 引导程序（Multiboot2 兼容）
; DNA: #龍芯⚡️丙午·丙申·甲寅·甲戌·坎-BOOT-LONGMODE-v1.0
;
; 文化锚点：坎宫（水）— 一切之始，流动之源
; 引导阶段 = 水——从无到有，从 BIOS/GRUB 到内核入口的流动过程
;
; 启动流程（坎宫·水 — 从混沌到有序）：
;   1. GRUB 加载内核（Multiboot2 兼容）
;   2. 32位保护模式入口（GRUB 已设置）
;   3. CPUID 检查 → 验证 Long Mode 支持
;   4. 建立页表（PML4 → PDPT → PD，2MB 大页，恒等映射前 2GB）
;   5. 启用 PAE（CR4.PAE）
;   6. 设置 EFER.LME（Long Mode Enable）
;   7. 启用分页（CR0.PG）
;   8. 加载 64 位 GDT
;   9. 远跳转进入 64 位 Long Mode
;   10. 初始化 64 位栈 → 调用 kernel_main()
;
; 构建命令：
;   nasm -f elf64 boot.asm -o boot.o
;   链接：ld.lld -T linker.ld -o houTu.elf boot.o kernel_main.o vga.o
;   运行：qemu-system-x86_64 -kernel houTu.elf
; ==============================================================================

; ── 常量定义（河图洛书 · 九宫格数值映射）──

; Multiboot2 魔数
MULTIBOOT2_MAGIC          equ 0xE85250D6  ; 太极之数（5+0+2+5+0+6=18→1+8=9 离宫火）
MULTIBOOT2_ARCH           equ 0           ; i386 保护模式（0=中宫太极）
MULTIBOOT2_INFO_MAGIC     equ 0x36D76289  ; 引导成功魔数（3+6+7+6+2+8+9=41→4+1=5 中宫）

; 页表常量
PAGE_PRESENT              equ (1 << 0)    ; 存在位
PAGE_RW                   equ (1 << 1)    ; 可读写
PAGE_HUGE                 equ (1 << 7)    ; 大页标志（2MB / 1GB）
PAGE_DEFAULT_FLAGS        equ PAGE_PRESENT | PAGE_RW
PAGE_HUGE_FLAGS           equ PAGE_PRESENT | PAGE_RW | PAGE_HUGE

; 控制寄存器位
CR0_PG                    equ (1 << 31)   ; 分页启用
CR4_PAE                   equ (1 << 5)    ; 物理地址扩展
EFER_LME                  equ (1 << 8)    ; Long Mode 启用（MSR 0xC0000080）
EFER_MSR                  equ 0xC0000080

; 页表大小
PML4_SIZE                 equ 0x1000      ; 4KB
PDPT_SIZE                 equ 0x1000      ; 4KB
PD_SIZE                   equ 0x1000      ; 4KB（每张页目录表）
PAGE_2MB                  equ 0x200000    ; 2MB = 大页尺寸

; 恒等映射范围：前 8GB（4 张页目录表，每张 1GB）
PAGE_TABLE_ENTRIES        equ 512         ; 每张表 512 项
PD_COUNT                  equ 8           ; 8 张 PD → 8GB 映射

; 栈大小
STACK_SIZE                equ 0x4000      ; 16KB 内核栈（4 * 0x1000 = 坎宫水位）

; ── Multiboot2 头部段（太极原点）──
section .multiboot2
align 8
multiboot2_header_start:
    dd MULTIBOOT2_MAGIC
    dd MULTIBOOT2_ARCH
    dd multiboot2_header_end - multiboot2_header_start  ; 头部长度
    ; 校验和：(magic + arch + header_length + checksum) mod 2^32 = 0
    dd -(MULTIBOOT2_MAGIC + MULTIBOOT2_ARCH + (multiboot2_header_end - multiboot2_header_start))

    ; ── Tag: 结束标记 ──
    align 8
    dw 0            ; type=0（结束）
    dw 0            ; flags=0
    dd 8            ; size=8
multiboot2_header_end:

; ── BSS 段（坎宫 · 暗流之水 — 未初始化数据）──
section .bss
align 0x1000  ; 4KB 对齐（页表必须页对齐！）

; --- 页表（恒等映射前 8GB，2MB 大页）---
global houTu_PML4
houTu_PML4:       resb PML4_SIZE     ; 四级页映射表（顶层）

global houTu_PDPT
houTu_PDPT:       resb PDPT_SIZE     ; 页目录指针表

global houTu_PD
houTu_PD:         resb PD_SIZE * PD_COUNT  ; 8 张页目录表（每张 1GB）

; --- 64 位模式内核栈 ---
global houTu_stack_bottom
houTu_stack_bottom: resb STACK_SIZE
global houTu_stack_top
houTu_stack_top:

; ── 代码段（兑宫 · 金 — 指令执行之力）──
section .text
bits 32  ; GRUB 将我们放在 32 位保护模式

; ── 入口：_start ──
; GRUB 跳转到此处时：
;   EAX = MULTIBOOT2_INFO_MAGIC (0x36D76289)
;   EBX = 指向 Multiboot2 信息结构的物理地址
;   CR0.PE = 1（保护模式启用）
;   CR0.PG = 0（分页未启用）
;   段寄存器 = 32 位平坦段（由 GRUB 设置）
;   栈 = 由 GRUB 设置（但我们重新设置）
;   EFLAGS = 由 GRUB 设置（中断可能已禁用）
;
global _start
_start:
    ; ── 坎宫第一动：保存 GRUB 传入的魔数和信息指针 ──
    ; 这两个值后面要传给 kernel_main
    mov edi, eax    ; EDI = magic（第一参数，暂存）
    mov esi, ebx    ; ESI = multiboot_info 指针（第二参数，暂存）

    ; ── 兑宫检查：验证 CPUID 指令可用 ──
    ; 翻转 EFLAGS 的 ID 位（bit 21），如果可以翻转 → CPUID 可用
    pushfd
    pop eax
    mov ecx, eax
    xor eax, (1 << 21)     ; 翻转 ID 位
    push eax
    popfd
    pushfd
    pop eax
    push ecx
    popfd                  ; 恢复原始 EFLAGS
    xor eax, ecx
    jz .no_cpuid           ; ID 位不能翻转 → 无 CPUID → 致命错误
    ; CPUID 可用，继续

    ; ── 离宫检查：验证 Long Mode 支持 ──
    ; 通过 CPUID 扩展功能位 0x80000001 的 EDX bit 29 检查
    mov eax, 0x80000000
    cpuid
    cmp eax, 0x80000001
    jb .no_longmode         ; 扩展功能编号不够 → 不支持 Long Mode

    mov eax, 0x80000001
    cpuid
    test edx, (1 << 29)    ; 检验 LM (Long Mode) 位
    jz .no_longmode         ; LM 位未设置 → 不支持
    ; Long Mode 支持，继续

    ; ── 坤宫造土：建立页表结构 ──
    ; 四层页表：PML4 → PDPT → PD（2MB 大页）
    ;
    ; 恒等映射：虚拟地址 = 物理地址（简化初始阶段）
    ; 映射范围：前 8GB 物理内存（PD_COUNT=8，每张 PD 1GB，2MB 大页）
    ;
    ; 页表关键位说明：
    ;   bit 0 = Present（存在）
    ;   bit 1 = R/W（可读写）
    ;   bit 7 = Page Size / Huge（大页标志，仅 PD 层有效）
    ;   bit 8 = Global（全局页，TLB 不刷新）

    ; --- 清空 PML4 ---
    mov edi, houTu_PML4
    mov ecx, PML4_SIZE / 4
    xor eax, eax
    rep stosd

    ; --- 设置 PML4[0] = PDPT 物理地址 ---
    mov eax, houTu_PDPT
    or  eax, PAGE_DEFAULT_FLAGS
    mov [houTu_PML4], eax

    ; --- 清空 PDPT ---
    mov edi, houTu_PDPT
    mov ecx, PDPT_SIZE / 4
    xor eax, eax
    rep stosd

    ; --- 设置 PDPT 条目（每个指向一张 PD，每张覆盖 1GB）---
    ; PDPT[0] → PD[0] (0GB-1GB)
    mov eax, houTu_PD
    or  eax, PAGE_DEFAULT_FLAGS
    mov [houTu_PDPT], eax

    ; PDPT[1] → PD[1] (1GB-2GB)
    mov eax, houTu_PD + PD_SIZE
    or  eax, PAGE_DEFAULT_FLAGS
    mov [houTu_PDPT + 8], eax

    ; PDPT[2] → PD[2] (2GB-3GB)
    mov eax, houTu_PD + (PD_SIZE * 2)
    or  eax, PAGE_DEFAULT_FLAGS
    mov [houTu_PDPT + 16], eax

    ; PDPT[3] → PD[3] (3GB-4GB)
    mov eax, houTu_PD + (PD_SIZE * 3)
    or  eax, PAGE_DEFAULT_FLAGS
    mov [houTu_PDPT + 24], eax

    ; PDPT[4] → PD[4] (4GB-5GB)
    mov eax, houTu_PD + (PD_SIZE * 4)
    or  eax, PAGE_DEFAULT_FLAGS
    mov [houTu_PDPT + 32], eax

    ; PDPT[5] → PD[5] (5GB-6GB)
    mov eax, houTu_PD + (PD_SIZE * 5)
    or  eax, PAGE_DEFAULT_FLAGS
    mov [houTu_PDPT + 40], eax

    ; PDPT[6] → PD[6] (6GB-7GB)
    mov eax, houTu_PD + (PD_SIZE * 6)
    or  eax, PAGE_DEFAULT_FLAGS
    mov [houTu_PDPT + 48], eax

    ; PDPT[7] → PD[7] (7GB-8GB)
    mov eax, houTu_PD + (PD_SIZE * 7)
    or  eax, PAGE_DEFAULT_FLAGS
    mov [houTu_PDPT + 56], eax

    ; --- 填充每张 PD（2MB 大页 · 恒等映射）---
    ; PD[0] 覆盖 0GB-1GB (512条目 × 2MB)
    ; PD[1] 覆盖 1GB-2GB
    ; ...
    ; PD[7] 覆盖 7GB-8GB

    mov ecx, PD_COUNT * PAGE_TABLE_ENTRIES  ; 总条目数
    mov edi, houTu_PD                       ; PD 起始地址
    xor ebx, ebx                            ; 物理地址计数器（从 0 开始）
    mov edx, PAGE_HUGE_FLAGS                ; 大页标志 + Present + R/W

.fill_pd:
    mov eax, ebx
    or  eax, edx          ; 物理地址 | 大页标志
    mov [edi], eax        ; 写入条目
    add ebx, PAGE_2MB     ; 物理地址 + 2MB
    add edi, 8            ; 下一个 8 字节条目
    loop .fill_pd

    ; ── 乾坤转换：启用分页与 Long Mode ──

    ; Step 1: 启用 PAE（CR4 bit 5）
    mov eax, cr4
    or  eax, CR4_PAE
    mov cr4, eax

    ; Step 2: 设置 EFER.LME（Long Mode Enable）
    mov ecx, EFER_MSR
    rdmsr
    or  eax, EFER_LME
    wrmsr

    ; Step 3: 加载 PML4 物理地址到 CR3
    mov eax, houTu_PML4
    mov cr3, eax

    ; Step 4: 启用分页（CR0 bit 31）
    ; 此时同时启用了 PG 和 LME → CPU 进入 IA-32e 模式（兼容模式）
    mov eax, cr0
    or  eax, CR0_PG
    mov cr0, eax

    ; ── 兑宫飞升：加载 64 位 GDT ──
    lgdt [houTu_gdt64_ptr]

    ; ── 太极归一：远跳转进入 64 位 Long Mode ──
    ; 0x08 = 64 位代码段选择子（GDT 第一个条目是 null，代码段在第二个）
    jmp 0x08:longmode_start

; ── 错误处理 ──
.no_cpuid:
    ; CPUID 不可用 → 严重错误，死循环
    ; 在真实硬件上几乎不可能，仅为完整性保留
    cli
    hlt
    jmp .no_cpuid

.no_longmode:
    ; 不支持 Long Mode → 严重错误
    ; 尝试向 VGA 输出错误信息后停机
    mov dword [0xB8000], 0x4F4C4F4C  ; "LOLO" — Long mode nOt supported, LOck
    mov dword [0xB8004], 0x4F4D474E  ; "NGMO"
    cli
    hlt
    jmp .no_longmode

; ── 64 位 GDT ──
; 在 64 位模式下，段基址和段限长大多被忽略，但描述符仍必须存在。
; GDT 结构（每项 8 字节）：
;   [0] 空描述符（必需）
;   [1] 64 位代码段：D=0 L=1 P=1 DPL=0（L=1 为 64 位代码段标志）
;   [2] 64 位数据段：P=1 DPL=0 W=1（64 位下大部字段被忽略）
align 16
houTu_gdt64:
    dq 0  ; 空描述符（中宫太极·空）
; 代码段描述符（兑宫·金）
    dw 0xFFFF          ; 段限长[15:0]（被忽略）
    dw 0               ; 基址[15:0]（被忽略）
    db 0               ; 基址[23:16]（被忽略）
    db 0b10011010      ; Access: P=1 DPL=0 S=1 E=1 DC=0 RW=1 A=0
    db 0b00100000      ; Flags: G=0 DB=0 L=1（64位代码段！） + 段限长[19:16]=0
    db 0               ; 基址[31:24]（被忽略）
; 数据段描述符（坤宫·土）
    dw 0xFFFF          ; 段限长[15:0]（被忽略）
    dw 0               ; 基址[15:0]（被忽略）
    db 0               ; 基址[23:16]（被忽略）
    db 0b10010010      ; Access: P=1 DPL=0 S=1 E=0 DC=0 RW=1 A=0
    db 0b00000000      ; Flags: G=0 DB=0 L=0 + 段限长[19:16]=0
    db 0               ; 基址[31:24]（被忽略）
houTu_gdt64_end:

houTu_gdt64_ptr:
    dw houTu_gdt64_end - houTu_gdt64 - 1  ; 限长（字节数-1）
    dq houTu_gdt64                         ; GDT 物理基址

; ==============================================================================
; ── 64 位 Long Mode 入口（太极已立 · 中宫归位）──
; ==============================================================================
bits 64
longmode_start:
    ; ── 离宫净化：零清除所有段寄存器 ──
    ; 数据段选择子 = 0x10（GDT 第三个条目，数据段）
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax

    ; ── 坎宫蓄水：设置 64 位栈 ──
    ; 栈顶 = houTu_stack_top（BSS 中 16KB 空间的高地址端）
    ; x86 栈向下增长，所以 SP 指向高地址
    mov rsp, houTu_stack_top

    ; ── 兑宫起卦：准备调用 kernel_main ──
    ; 恢复之前保存的 Multiboot2 参数
    ; EDI → RDI（magic），ESI → RSI（multiboot_info*）
    ; 注意：32 位模式下 MOV EDI, EAX 只设置了低 32 位
    ; 切换到 64 位后 RDI 高 32 位 = 0（x86_64 写 32 位寄存器自动清零高32位）
    ; 所以 RDI 和 RSI 的值已经正确

    ; ── 太极归一：跳入 C 语言内核 ──
    ; 调用 kernel_main(magic, multiboot_info)
    ; RDI = magic（由 _start 保存的 EDI）
    ; RSI = multiboot_info*（由 _start 保存的 ESI）
    extern kernel_main
    call kernel_main

    ; kernel_main 不应返回，如果返回则停机
    cli
.forever:
    hlt
    jmp .forever
