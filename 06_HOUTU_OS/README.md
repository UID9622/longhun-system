# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 后土 x86 操作系统 · 龍魂系统工程实现

> **DNA**: `#龍芯⚡️丙午·丙申·甲寅·甲戌·坤-HOUTU-OS-v1.0`
> **唯一决策者**: UID9622 (诸葛鑫·Lucky)
> **状态**: v0.1 — 太极微内核引导阶段完成

---

## 项目定位

「后土」是龍魂系统的 x86 自主可控操作系统内核。采用"太极微内核 + 五行服务域"架构，以 Multiboot2 标准引导，在 QEMU/实机上可验证运行。

**文化锚点**：后土承载万物 — 系统作为数字世界的坚实大地，承载上层应用与数据主权。

---

## 目录结构

```
03_后土OS/
├── docs/
│   ├── 01-需求文档.md              # 技术需求文档（宪法级）
│   └── 02-架构设计文档.md          # 架构设计文档（宪法级）
├── src/
│   ├── boot/
│   │   └── boot.asm               # 引导程序（Multiboot2 → Long Mode）
│   ├── kernel/
│   │   ├── vga.h                  # VGA 文本模式驱动头文件
│   │   ├── vga.c                  # VGA 文本模式驱动实现
│   │   └── kernel_main.c          # 内核主入口
│   └── linker.ld                  # 链接脚本（九宫格内存布局）
├── Makefile                        # 构建系统
├── test.sh                         # 自动化测试脚本
└── README.md                       # 本文件
```

---

## 构建与运行

### 前置依赖

| 工具 | macOS 安装 | 用途 |
|------|-----------|------|
| NASM | `brew install nasm` | x86 汇编器 |
| Clang | 系统自带 / `xcode-select --install` | C 编译器 |
| ld.lld | `brew install llvm` | ELF 链接器 |
| QEMU | `brew install qemu` | x86 虚拟机 |

> 所有工具均为开源/国产自主可控工具链，不依赖 GCC/GNU binutils。

### 构建

```bash
# 检查工具链
make check-tools

# 构建内核
make

# 直接运行（QEMU）
make run
```

### 预期输出

```
+===================================+
|                                   |
|     HouTu x86 Microkernel v0.1    |
|     后土 · 太极微内核 · 自主可控    |
|                                   |
|  DNA: #LONGXIN:PW-BS-JY-JX-KUN   |
|  代码主权归集 · 数据不出境         |
|  UID9622 · 诸葛鑫 · 唯一决策者    |
|  中华人民共和国 · 后土承载万物     |
+===================================+

[离宫·火] 系统自检
  [PASS] Multiboot2 bootloader OK
  [PASS] Multiboot2 info at 0x...
  [PASS] Long Mode (x86_64) active
  [PASS] VGA text mode 80x25

[兑宫·金] 三色审计
  [PASS] 天·内核代码段已加载 end=0x...
  [PASS] 地·BSS已清零 size=0x...
  [PASS] 人·VGA显存可读写

[中宫] 三色审计结果: ALL PASS

[中宫] 后土已承 · 太极已立 · 待五行相生
```

---

## 启动流程

```
BIOS / UEFI
  │
  ▼
GRUB2 (Multiboot2)
  │  加载 houTu.elf 到 1MB 物理地址
  │  切换到 32 位保护模式
  ▼
boot.asm:_start
  │  [坎宫] 保存 Multiboot2 magic + info 指针
  │  [兑宫] 验证 CPUID 指令可用
  │  [离宫] 验证 Long Mode 支持（CPUID 0x80000001）
  │  [坤宫] 建立页表（PML4→PDPT→PD，2MB大页，恒等映射前8GB）
  │  [乾坤] PAE + LME + PG → Long Mode
  │  [兑宫] 加载 64-bit GDT
  │  [太极] jmp 0x08:longmode_start
  ▼
boot.asm:longmode_start [64-bit]
  │  [离宫] 清段寄存器
  │  [坎宫] 设置 64 位栈
  │  [太极] call kernel_main
  ▼
kernel_main.c
  │  [兑宫] 初始化 VGA 显示
  │  [中宫] 显示后土横幅
  │  [离宫] 系统自检输出
  │  [兑宫] 三色审计
  │  [中宫] 后土已承 → HLT 停机循环
```

---

## 技术特性

| 特性 | 说明 |
|------|------|
| **架构** | x86_64 Long Mode，Multiboot2 标准引导 |
| **页表** | 四层页表（PML4→PDPT→PD），2MB 大页，恒等映射前 8GB |
| **工具链** | LLVM/Clang + NASM + ld.lld（零 GNU 依赖） |
| **引导** | GRUB2 Multiboot2 或 QEMU -kernel 直接加载 |
| **显示** | VGA 文本模式 80×25，五行五色输出方案 |
| **安全** | 三才审计（天/地/人），DNA 追溯码全链路覆盖 |
| **文化** | 九宫格内存布局、五行相生调度模型、太极 IPC 通道 |

---

## 下一步路线

- [ ] 中断系统（IDT 初始化 + 键盘中断处理）
- [ ] 物理内存管理器（九宫格分配算法）
- [ ] 五行相生进程调度器
- [ ] 太极 IPC 通信通道
- [ ] VESA 图形模式 + 中文渲染
- [ ] PCI/ACPI 设备枚举框架
- [ ] AHCI 存储驱动
- [ ] 用户态 libc-mini + CNSH Shell

---

## 宪法锚点

本项目严格遵循龍魂系统的所有 L0 宪法层锚点，包括但不限于：

- **A-003**：龍魂 = Dragon Soul = 文化主权
- **A-005**：河图洛书·易经·五行八卦 = 焊死
- **A-007**：每个动作绑定 DNA 追溯码
- **A-013**：国产系统交付标准
- **A-029**：物理虚拟统一 DNA 登记册
- **A-033**：涉密结界防护

---

> **来源可查 · 去向可追 · 责任可究**
>
> 🇨🇳 中华人民共和国
