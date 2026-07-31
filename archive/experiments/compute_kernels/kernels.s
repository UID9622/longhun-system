# ============================================================
# 🐉 龍魂计算内核 · x86-64 SIMD 汇编
# 神经网络推理原语: SiLU / RMS Norm / Linear / RoPE / 统计约束
# DNA: #龍芯⚡️2026-07-13-COMPUTE-KERNELS-v1.0
# ============================================================

.intel_syntax noprefix

.section __TEXT,__const
.align 16
one:        .float 1.0
eps:        .float 1e-6
abs_mask:   .long 0x7fffffff, 0x7fffffff, 0x7fffffff, 0x7fffffff

.text
.globl _lh_silu
.globl _lh_rms_norm
.globl _lh_linear
.globl _lh_apply_rope
.globl _lh_apply_stat_constraint

# ============================================================
# lh_silu: SiLU 激活 x / (1 + exp(-x))
# 输入: xmm0 = x
# 返回: xmm0 = silu(x)
# ============================================================
_lh_silu:
    sub     rsp, 24
    movaps  [rsp], xmm0
    movaps  xmm1, xmm0
    pxor    xmm2, xmm2
    subss   xmm2, xmm1
    movaps  xmm0, xmm2
    call    _expf
    addss   xmm0, [rip + one]
    movaps  xmm1, [rsp]
    divss   xmm1, xmm0
    movaps  xmm0, xmm1
    add     rsp, 24
    ret

# ============================================================
# lh_rms_norm: RMS 归一化
# rdi=out, rsi=x, rdx=weight, ecx=n
# out = (x / rms(x)) * weight
# ============================================================
_lh_rms_norm:
    push    rbx
    push    r12
    mov     r12d, ecx
    vxorps  ymm0, ymm0, ymm0
    xor     eax, eax
.L_rms_sum:
    cmp     eax, r12d
    jge     .L_rms_calc
    vmovups ymm1, [rsi + rax*4]
    vfmadd231ps ymm0, ymm1, ymm1
    add     eax, 8
    jmp     .L_rms_sum
.L_rms_calc:
    vextractf128 xmm1, ymm0, 1
    vaddps  xmm0, xmm0, xmm1
    vhaddps xmm0, xmm0, xmm0
    vhaddps xmm0, xmm0, xmm0
    vcvtsi2ss xmm1, xmm1, r12d
    vdivss  xmm0, xmm0, xmm1
    vaddss  xmm0, xmm0, [rip + eps]
    vsqrtss xmm0, xmm0, xmm0
    vmovss  xmm1, [rip + one]
    vdivss  xmm1, xmm1, xmm0
    vbroadcastss ymm2, xmm1
    xor     eax, eax
.L_rms_apply:
    cmp     eax, r12d
    jge     .L_rms_done
    vmovups ymm0, [rsi + rax*4]
    vmulps  ymm0, ymm0, ymm2
    vmovups ymm1, [rdx + rax*4]
    vmulps  ymm0, ymm0, ymm1
    vmovups [rdi + rax*4], ymm0
    add     eax, 8
    jmp     .L_rms_apply
.L_rms_done:
    pop     r12
    pop     rbx
    ret

# ============================================================
# lh_linear: 矩阵向量乘法 (64维 AVX 展开)
# rdi=x, rsi=w, rdx=out, ecx=in_dim, r8d=out_dim
# ============================================================
_lh_linear:
    push    rbx
    push    r12
    push    r13
    push    r14
    mov     r12d, r8d
    mov     r13d, ecx
    shr     ecx, 3
    xor     ebx, ebx
.L_lin_outer:
    cmp     ebx, r12d
    jge     .L_lin_done
    vxorps  ymm0, ymm0, ymm0
    xor     eax, eax
    mov     r9d, ecx
.L_lin_inner:
    cmp     r9d, 0
    jle     .L_lin_tail
    vmovups ymm1, [rsi + rax*4]
    vmovups ymm2, [rdi + rax*4]
    vfmadd231ps ymm0, ymm1, ymm2
    add     eax, 8
    dec     r9d
    jmp     .L_lin_inner
.L_lin_tail:
    mov     r10d, r13d
    and     r10d, 7
    jz      .L_lin_store
.L_lin_tail_loop:
    vmovss  xmm1, [rsi + rax*4]
    vmulss  xmm1, xmm1, [rdi + rax*4]
    vaddss  xmm0, xmm0, xmm1
    inc     eax
    dec     r10d
    jnz     .L_lin_tail_loop
.L_lin_store:
    vextractf128 xmm1, ymm0, 1
    vaddps  xmm0, xmm0, xmm1
    vhaddps xmm0, xmm0, xmm0
    vhaddps xmm0, xmm0, xmm0
    vmovss  [rdx + rbx*4], xmm0
    lea     rsi, [rsi + r13*4]     # 步进 in_dim*4 字节到下一行权重
    inc     ebx
    jmp     .L_lin_outer
.L_lin_done:
    pop     r14
    pop     r13
    pop     r12
    pop     rbx
    ret

# ============================================================
# lh_apply_rope: 旋转位置编码 (2D RoPE)
# rdi=x(in-place), rsi=cos, rdx=sin, ecx=dim
# ============================================================
_lh_apply_rope:
    push    rbx
    push    r12
    shr     ecx, 1
    mov     r12d, ecx               # r12d = half_dim (循环计数)
    shl     ecx, 2                   # ecx = half_dim * 4 (字节偏移)
    xor     ebx, ebx
.L_rope_loop:
    cmp     ebx, r12d
    jge     .L_rope_done
    lea     r10, [rdi + rcx]         # r10 = &x[half_dim]
    vmovss  xmm0, [rdi + rbx*4]     # x[i]
    vmovss  xmm1, [r10 + rbx*4]     # x[i + half_dim]
    vmulss  xmm2, xmm0, [rsi + rbx*4]
    vmulss  xmm3, xmm1, [rdx + rbx*4]
    vsubss  xmm2, xmm2, xmm3
    vmulss  xmm3, xmm0, [rdx + rbx*4]
    vmulss  xmm4, xmm1, [rsi + rbx*4]
    vaddss  xmm3, xmm3, xmm4
    vmovss  [rdi + rbx*4], xmm2
    vmovss  [r10 + rbx*4], xmm3
    inc     ebx
    jmp     .L_rope_loop
.L_rope_done:
    pop     r12
    pop     rbx
    ret

# ============================================================
# lh_apply_stat_constraint: 自适应统计约束
# rdi=x, esi=size, rdx=mean, rcx=std
# xmm0=gamma, xmm1=k, xmm2=max_norm, xmm3=min_norm
# ============================================================
_lh_apply_stat_constraint:
    push    rbp
    mov     rbp, rsp
    push    rbx
    push    r12
    push    r13
    push    r14
    push    r15
    mov     r12, rdi
    mov     r13d, esi
    mov     r14, rdx
    mov     r15, rcx
    vxorps  ymm4, ymm4, ymm4
    xor     ebx, ebx
.L_stc_norm:
    cmp     ebx, r13d
    jge     .L_stc_norm_done
    vmovss  xmm5, [r12 + rbx*4]
    vmulss  xmm5, xmm5, xmm5
    vaddss  xmm4, xmm4, xmm5
    inc     ebx
    jmp     .L_stc_norm
.L_stc_norm_done:
    vsqrtss xmm12, xmm4, xmm4
    vmovss  xmm13, [r14]
    vmovss  xmm14, [r15]
    vmulss  xmm5, xmm0, xmm13
    vmovss  xmm6, [rip + one]
    vsubss  xmm6, xmm6, xmm0
    vmulss  xmm6, xmm6, xmm12
    vaddss  xmm5, xmm5, xmm6
    vmovss  [r14], xmm5
    vsubss  xmm7, xmm12, xmm13
    vandps  xmm7, xmm7, [rip + abs_mask]
    vmulss  xmm8, xmm0, xmm14
    vmulss  xmm7, xmm7, xmm6
    vaddss  xmm7, xmm8, xmm7
    vmovss  [r15], xmm7
    vmulss  xmm9, xmm1, xmm7
    vaddss  xmm10, xmm5, xmm9
    vcomiss xmm12, xmm10
    jbe     .L_stc_max
    vdivss  xmm11, xmm10, xmm12
    xor     ebx, ebx
.L_stc_scale:
    cmp     ebx, r13d
    jge     .L_stc_max
    vmovss  xmm5, [r12 + rbx*4]
    vmulss  xmm5, xmm5, xmm11
    vmovss  [r12 + rbx*4], xmm5
    inc     ebx
    jmp     .L_stc_scale
.L_stc_max:
    vcomiss xmm12, xmm2
    jbe     .L_stc_done
    vdivss  xmm11, xmm2, xmm12
    xor     ebx, ebx
.L_stc_scale2:
    cmp     ebx, r13d
    jge     .L_stc_done
    vmovss  xmm5, [r12 + rbx*4]
    vmulss  xmm5, xmm5, xmm11
    vmovss  [r12 + rbx*4], xmm5
    inc     ebx
    jmp     .L_stc_scale2
.L_stc_done:
    pop     r15
    pop     r14
    pop     r13
    pop     r12
    pop     rbx
    pop     rbp
    ret
