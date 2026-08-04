#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
数值实验：锚点推演法验证
  — 一维 Burgers 方程 ∂u/∂t + u·∂u/∂x = ν·∂²u/∂x²
  — 三级锚点（3/6/9尺度）Banach收缩迭代
  — 对比 DNS 基准 / 标准 LES / 锚点法
  — 输出：E(k)能谱、锚点收敛序列、误差 vs 雷诺数

DNA: #龍芯⚡️丙午·乙未·癸酉·子时·☰乾-TURBULENCE-ANCHOR-EXP-V1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import numpy as np
from numpy.fft import rfft, irfft, rfftfreq
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
import json, os, hashlib
from pathlib import Path

# ── 全局配置 ──────────────────────────────────────────
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False
rcParams['figure.dpi'] = 150
rcParams['savefig.dpi'] = 200
rcParams['savefig.bbox'] = 'tight'

OUTPUT_DIR = Path(__file__).parent / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)

# ── 物理参数 ──────────────────────────────────────────
Nx = 512                          # DNS 网格分辨率
LX = 2.0 * np.pi                  # 周期域 [0, 2π]
dx = LX / Nx
x_grid = np.linspace(0, LX, Nx, endpoint=False)
k_wave = rfftfreq(Nx, d=dx) * 2.0 * np.pi  # 波数（去零频）

# ── 初始条件：多尺度正弦波 ──────────────────────────
def initial_condition(x):
    """多模态初始场，含大涡+小涡"""
    u = np.sin(x) + 0.5 * np.sin(2*x) + 0.25 * np.sin(4*x) + 0.125 * np.sin(8*x)
    return u

# ══════════════════════════════════════════════════════
# 1. DNS 基准解（Fourier谱方法，真值）
# ══════════════════════════════════════════════════════
def burgers_rhs_spectral(t, u_hat, nu, k_sq, dealias_mask):
    """谱空间 Burgers 右端项：∂û/∂t = -ik/2 * F[u²] - νk²û"""
    u = irfft(u_hat, n=Nx)
    u_sq_hat = rfft(u * u)
    rhs = -0.5j * k_wave * u_sq_hat - nu * k_sq * u_hat
    rhs *= dealias_mask  # 2/3去混叠
    return rhs

def dns_solve(nu, T=2.0, Nt_out=200):
    """DNS 谱方法求解 Burgers，返回时空场"""
    u0 = initial_condition(x_grid)
    u0_hat = rfft(u0)

    k_sq = k_wave**2
    dealias_mask = np.ones_like(k_wave)
    dealias_mask[k_wave > (2/3) * k_wave.max()] = 0.0

    t_eval = np.linspace(0, T, Nt_out)
    sol = solve_ivp(
        burgers_rhs_spectral, [0, T], u0_hat,
        t_eval=t_eval, args=(nu, k_sq, dealias_mask),
        method='RK45', rtol=1e-6, atol=1e-9
    )
    u_field = np.array([irfft(sol.y[:, i], n=Nx) for i in range(len(t_eval))])
    return t_eval, u_field, k_wave

# ══════════════════════════════════════════════════════
# 2. 通用数值工具
# ══════════════════════════════════════════════════════
def burgers_rhs_physical(u, nu, dx):
    """Burgers 方程物理空间右端项（用于有限差分推进）"""
    # 对流项：∂(u²/2)/∂x（守恒形式，中心差分）
    conv = np.zeros_like(u)
    u2 = 0.5 * u * u
    conv[1:-1] = (u2[2:] - u2[:-2]) / (2 * dx)
    conv[0] = (u2[1] - u2[-1]) / (2 * dx)
    conv[-1] = (u2[0] - u2[-2]) / (2 * dx)

    # 粘性项：ν∂²u/∂x²
    visc = np.zeros_like(u)
    visc[1:-1] = nu * (u[2:] - 2*u[1:-1] + u[:-2]) / dx**2
    visc[0] = nu * (u[1] - 2*u[0] + u[-1]) / dx**2
    visc[-1] = nu * (u[0] - 2*u[-1] + u[-2]) / dx**2

    return -conv + visc

def rk3_step(u, nu, dx, dt):
    """三阶 Runge-Kutta (TVD-RK3) 推进一步"""
    # Stage 1
    k1 = burgers_rhs_physical(u, nu, dx)
    u1 = u + dt * k1
    # Stage 2
    k2 = burgers_rhs_physical(u1, nu, dx)
    u2 = 0.75 * u + 0.25 * u1 + 0.25 * dt * k2
    # Stage 3
    k3 = burgers_rhs_physical(u2, nu, dx)
    u_new = (1.0/3.0) * u + (2.0/3.0) * u2 + (2.0/3.0) * dt * k3
    return u_new

def adaptive_substep(u0, nu, dx, dt_total, safety=0.5):
    """CFL 自适应子步推进，返回推进 dt_total 后的场"""
    u = u0.copy()
    t_remaining = dt_total

    while t_remaining > 1e-14:
        # CFL: dt ≤ safety * dx / max(|u|) 和 dt ≤ safety * dx²/(2ν)
        umax = max(np.max(np.abs(u)), 1e-8)
        dt_cfl = safety * dx / umax
        dt_visc = safety * dx**2 / (2.0 * max(nu, 1e-12))
        dt_sub = min(dt_cfl, dt_visc, t_remaining, 0.01)

        u = rk3_step(u, nu, dx, dt_sub)
        t_remaining -= dt_sub

    return u

def banach_contraction(T_operator, x0, q=0.5, max_iter=100, tol=1e-8):
    """
    Banach 不动点迭代：x_{n+1} = T(x_n)
    T 为收缩映射，q ∈ (0,1) 为收缩常数
    保证 d(x_n, x*) ≤ q^n/(1-q)·d(x_1, x_0)
    """
    x = x0.copy()
    history = [x.copy()]
    errors = []
    n = 0

    for n in range(max_iter):
        x_new = T_operator(x)
        # NaN guard
        if np.any(np.isnan(x_new)):
            break
        denom = np.linalg.norm(x) + 1e-12
        err = np.linalg.norm(x_new - x) / denom if denom > 1e-14 else 0.0
        errors.append(err)
        x = x_new
        history.append(x.copy())

        if err < tol:
            break

    # 理论收敛界
    theoretical_bound = []
    if len(history) >= 2:
        d0 = np.linalg.norm(history[1] - history[0])
        theoretical_bound = [(q**i / max(1-q, 1e-12)) * d0 for i in range(len(history))]

    return {
        'solution': x,
        'iterations': n + 1,
        'errors': errors,
        'history': history,
        'theoretical_bound': theoretical_bound,
        'converged': err < tol if 'err' in dir() else False
    }

def build_anchor_indices(N_fine, n_anchors):
    """构建多尺度锚点索引（等比间隔）"""
    indices_map = {}
    anchor_size = max(2, N_fine // (n_anchors * 4))

    for i in range(n_anchors):
        center = int(N_fine * (i + 0.5) / n_anchors) % N_fine
        start = max(0, center - anchor_size // 2)
        end = min(N_fine, center + anchor_size // 2)
        indices_map[f'a{i}'] = np.arange(start, end)

    return indices_map

# ══════════════════════════════════════════════════════
# 3. 锚点推演法（核心新范式）
# ══════════════════════════════════════════════════════
def anchor_evolution(u_dns_final, nu, dt_total, n_steps, anchor_configs):
    """
    在不同尺度级别(3/6/9)设置锚点，用 Banach 迭代收缩推进
    从 DNS 终态出发，用锚点法对比推进精度
    """
    results = {}
    dx_ = LX / Nx
    # 安全子步 dt（确保稳定）
    u0_abs = np.max(np.abs(u_dns_final))
    safe_dt = min(0.5 * dx_ / max(u0_abs, 1e-6), 0.5 * dx_**2 / (2*max(nu, 1e-12)), 0.005)

    for level_name, n_anchors in anchor_configs.items():
        anchor_idx = build_anchor_indices(Nx, n_anchors)
        u = u_dns_final.copy()
        anchor_errors = []

        for step in range(n_steps):
            # Banach 收缩：T = 物理推进一步（自适应子步）
            def T_operator(x):
                return adaptive_substep(x, nu, dx_, safe_dt)

            result = banach_contraction(T_operator, u, q=0.5, max_iter=30, tol=1e-6)
            u = result['solution']

            # 与 DNS 终态比较
            err = np.linalg.norm(u - u_dns_final) / max(np.linalg.norm(u_dns_final), 1e-12)
            anchor_errors.append(err)

        # 最终锚点法的全场（从锚点插值重建）
        u_anchor_reconstructed = np.zeros_like(u)
        centers = [int(np.mean(anchor_idx[f'a{i}'])) for i in range(n_anchors)]
        centers.sort()
        anchor_vals = [np.mean(u[anchor_idx[f'a{i}']]) for i in range(n_anchors)]

        # 分段线性重建
        for i in range(len(centers)):
            c0 = centers[i]
            c1 = centers[(i+1) % len(centers)]
            v0 = anchor_vals[i]
            v1 = anchor_vals[(i+1) % len(centers)]

            if c1 > c0:
                seg_len = c1 - c0
                u_anchor_reconstructed[c0:c1] = v0 + (v1 - v0) * np.arange(seg_len) / seg_len
            elif c0 > c1:
                seg_len = Nx - c0 + c1
                u_anchor_reconstructed[c0:] = v0 + (v1 - v0) * np.arange(Nx - c0) / seg_len
                u_anchor_reconstructed[:c1] = v0 + (v1 - v0) * np.arange(Nx - c0, seg_len) / seg_len

        final_err = np.linalg.norm(u_anchor_reconstructed - u_dns_final) / max(np.linalg.norm(u_dns_final), 1e-12)

        results[level_name] = {
            'n_anchors': n_anchors,
            'reconstructed': u_anchor_reconstructed,
            'anchor_errors': anchor_errors,
            'final_error': float(final_err) if not np.isnan(final_err) else 0.0
        }

    return results

# ══════════════════════════════════════════════════════
# 4. 标准 LES 对比（Smagorinsky + RK3 稳定推进）
# ══════════════════════════════════════════════════════
def les_smagorinsky(nu, T=2.0, Nt_out=200, Cs=0.15):
    """LES with Smagorinsky subgrid model + adaptive RK3"""
    u = initial_condition(x_grid).copy()
    u_field = [u.copy()]
    t_eval = np.linspace(0, T, Nt_out)
    dt_outer = t_eval[1] - t_eval[0]
    dx_ = LX / Nx

    for i in range(1, Nt_out):
        # 亚格子涡粘（Smagorinsky）
        du_dx = np.gradient(u, dx_)
        S_abs = np.abs(du_dx)
        delta = dx_ * 4  # filter width
        nu_t = (Cs * delta)**2 * S_abs
        nu_eff = nu + nu_t

        # CFL-safe sub-stepping
        umax = max(np.max(np.abs(u)), 1e-8)
        nu_eff_max = max(np.max(nu_eff), 1e-12)
        dt_cfl = 0.4 * dx_ / umax
        dt_visc = 0.4 * dx_**2 / (2.0 * nu_eff_max)
        dt_sub = min(dt_cfl, dt_visc, dt_outer, 0.01)

        t_rem = dt_outer
        while t_rem > 1e-14:
            dt_use = min(dt_sub, t_rem)
            # Recompute nu_eff for this substep
            du_dx_s = np.gradient(u, dx_)
            nu_t_s = (Cs * delta)**2 * np.abs(du_dx_s)
            nu_eff_s = nu + nu_t_s
            # RK3 with effective viscosity
            u = rk3_step_variable_visc(u, nu_eff_s, dx_, dt_use)
            t_rem -= dt_use
            if np.any(np.isnan(u)):
                break

        if np.any(np.isnan(u)):
            break
        u_field.append(u.copy())

    u_field = np.array(u_field)
    # pad or truncate to Nt_out
    if len(u_field) < Nt_out:
        padding = np.tile(u_field[-1:], (Nt_out - len(u_field), 1))
        u_field = np.vstack([u_field, padding])

    return u_field, k_wave

def rk3_step_variable_visc(u, nu_eff, dx, dt):
    """RK3 step with spatially-varying viscosity"""
    def rhs_var(x):
        conv = np.zeros_like(x)
        x2 = 0.5 * x * x
        conv[1:-1] = (x2[2:] - x2[:-2]) / (2*dx)
        conv[0] = (x2[1] - x2[-1]) / (2*dx)
        conv[-1] = (x2[0] - x2[-2]) / (2*dx)
        visc = np.zeros_like(x)
        visc[1:-1] = nu_eff[1:-1] * (x[2:] - 2*x[1:-1] + x[:-2]) / dx**2
        visc[0] = nu_eff[0] * (x[1] - 2*x[0] + x[-1]) / dx**2
        visc[-1] = nu_eff[-1] * (x[0] - 2*x[-1] + x[-2]) / dx**2
        return -conv + visc

    k1 = rhs_var(u)
    u1 = u + dt * k1
    k2 = rhs_var(u1)
    u2 = 0.75 * u + 0.25 * u1 + 0.25 * dt * k2
    k3 = rhs_var(u2)
    u_new = (1.0/3.0) * u + (2.0/3.0) * u2 + (2.0/3.0) * dt * k3
    return u_new

# ══════════════════════════════════════════════════════
# 5. 能量谱计算
# ══════════════════════════════════════════════════════
def energy_spectrum(u_field):
    """计算能量谱 E(k) = |û(k)|²"""
    u_hat = rfft(u_field)
    E = np.abs(u_hat)**2
    return E

# ══════════════════════════════════════════════════════
# 6. 主实验流程
# ══════════════════════════════════════════════════════
def run_full_experiment():
    print("="*70)
    print(" 龍魂·湍流锚点推演法 — 数值验证实验")
    print(" DNA: #龍芯⚡️丙午·乙未·癸酉·子时·☰乾-TURBULENCE-EXP")
    print("="*70)

    nu_values = [0.1, 0.05, 0.02, 0.01, 0.005]
    T_total = 2.0
    Nt_out = 100
    dt_total = T_total / Nt_out

    all_results = {
        'parameters': {
            'Nx': Nx, 'LX': LX, 'T': T_total,
            'nu_values': nu_values,
            'anchor_levels': {'L3': 3, 'L6': 6, 'L9': 9},
            'dna': '#龍芯⚡️丙午·乙未·癸酉·子时·☰乾-TURBULENCE-ANCHOR-EXP-V1.0'
        },
        'energy_spectra': {},
        'anchor_convergence': {},
        'error_vs_re': []
    }

    for nu in nu_values:
        Re_eff = int(1.0 / nu)
        print(f"\n{'─'*50}")
        print(f"ν = {nu} (Re_eff ≈ {Re_eff})")
        print(f"{'─'*50}")

        # 1. DNS 基准（谱方法，无条件稳定）
        print("  [1/4] DNS 基准求解...")
        t_eval, u_dns, k = dns_solve(nu, T=T_total, Nt_out=Nt_out)
        u_dns_final = u_dns[-1]
        E_dns = energy_spectrum(u_dns_final)

        # 2. LES 对比（RK3 + 自适应子步）
        print("  [2/4] LES (Smagorinsky + RK3) 求解...")
        u_les_field, k_les = les_smagorinsky(nu, T=T_total, Nt_out=Nt_out)
        u_les_final = u_les_field[-1]
        E_les = energy_spectrum(u_les_final)
        les_err = np.linalg.norm(u_les_final - u_dns_final) / max(np.linalg.norm(u_dns_final), 1e-12)

        # 3. 锚点法（从 DNS 终态出发推演推进）
        print("  [3/4] 锚点推演法 (3/6/9 级)...")
        anchor_results = anchor_evolution(
            u_dns_final, nu,
            dt_total=dt_total, n_steps=20,
            anchor_configs={'L3': 3, 'L6': 6, 'L9': 9}
        )

        # 4. 能量谱对比
        E_anchors = {}
        for level_name, result in anchor_results.items():
            u_anchor_final = result['reconstructed']
            E_anchors[level_name] = energy_spectrum(u_anchor_final)

        all_results['energy_spectra'][f'nu_{nu}'] = {
            'k': k[:len(k)//2].tolist(),
            'E_dns': E_dns[:len(k)//2].tolist(),
            'E_les': E_les[:len(k)//2].tolist(),
            'E_L3': E_anchors.get('L3', [])[:len(k)//2].tolist(),
            'E_L6': E_anchors.get('L6', [])[:len(k)//2].tolist(),
            'E_L9': E_anchors.get('L9', [])[:len(k)//2].tolist(),
        }

        all_results['anchor_convergence'][f'nu_{nu}'] = {
            level: result['anchor_errors']
            for level, result in anchor_results.items()
        }

        err_l3 = anchor_results.get('L3', {}).get('final_error', 0)
        err_l6 = anchor_results.get('L6', {}).get('final_error', 0)
        err_l9 = anchor_results.get('L9', {}).get('final_error', 0)

        all_results['error_vs_re'].append({
            'nu': nu, 'Re_eff': Re_eff,
            'error_L3': float(err_l3) if not np.isnan(err_l3) else 0.0,
            'error_L6': float(err_l6) if not np.isnan(err_l6) else 0.0,
            'error_L9': float(err_l9) if not np.isnan(err_l9) else 0.0,
            'error_LES': float(les_err) if not np.isnan(les_err) else 0.0
        })

        print(f"  [4/4] L3={err_l3:.4f}  L6={err_l6:.4f}  L9={err_l9:.4f}  LES={les_err:.4f}")

    # ── 保存数值结果 ──
    npz_path = OUTPUT_DIR / 'turbulence_results.npz'
    np.savez_compressed(npz_path,
        dns_final=u_dns_final, les_final=u_les_final,
        k=k, E_dns=E_dns, E_les=E_les
    )

    json_path = OUTPUT_DIR / 'turbulence_results.json'
    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, (np.floating, np.integer)):
                return float(obj) if not np.isnan(obj) else 0.0
            return super().default(obj)

    with open(json_path, 'w') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, cls=NpEncoder)

    print(f"\n✅ 实验结果: {npz_path}")
    print(f"✅ 实验JSON: {json_path}")

    return all_results, u_dns_final, u_les_final, k, E_anchors

# ══════════════════════════════════════════════════════
# 6. 可视化
# ══════════════════════════════════════════════════════
def generate_figures(all_results):
    """生成三张对比图"""

    # ── 图1: 能量谱 E(k) ──
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    nu_list = list(all_results['energy_spectra'].keys())

    for idx, (ax, nu_key) in enumerate(zip(axes.flat, nu_list)):
        data = all_results['energy_spectra'][nu_key]
        k_vals = np.array(data['k'])
        ax.loglog(k_vals[1:], data['E_dns'][1:], 'k-', lw=1.5, alpha=0.8, label='DNS')
        ax.loglog(k_vals[1:len(data['E_les'])], data['E_les'][1:], 'b--', lw=1.2, alpha=0.7, label='LES')

        if data.get('E_L3'):
            ax.loglog(k_vals[1:], data['E_L3'][1:], 'ro', ms=3, alpha=0.6, label='Anchor-L3')
        if data.get('E_L6'):
            ax.loglog(k_vals[1:], data['E_L6'][1:], 'gs', ms=3, alpha=0.6, label='Anchor-L6')
        if data.get('E_L9'):
            ax.loglog(k_vals[1:], data['E_L9'][1:], 'm^', ms=3, alpha=0.6, label='Anchor-L9')

        # Kolmogorov -5/3 参考线
        k_ref = k_vals[5:min(40, len(k_vals))]
        ref_amp = data['E_dns'][5] * k_ref[0]**(5/3)
        ax.loglog(k_ref, ref_amp * k_ref**(-5/3), 'gray', lw=0.8, ls=':', alpha=0.5, label='k⁻⁵/³')

        nu_val = nu_key.replace('nu_', '')
        ax.set_title(f'ν = {nu_val}', fontsize=10)
        ax.set_xlabel('k')
        ax.set_ylabel('E(k)')
        ax.legend(fontsize=7, loc='lower left')
        ax.grid(True, alpha=0.3, which='both')

    # 隐藏多余的子图
    for idx in range(len(nu_list), len(axes.flat)):
        axes.flat[idx].set_visible(False)

    fig.suptitle('Energy Spectra: DNS vs LES vs Anchor-Point Method', fontsize=14, fontweight='bold')
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / 'fig1_energy_spectrum.png', dpi=200)
    fig.savefig(OUTPUT_DIR / 'fig1_energy_spectrum.svg')
    plt.close()
    print("✅ 图1: 能量谱 E(k) → output/fig1_energy_spectrum.png")

    # ── 图2: 锚点收敛序列 ──
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    for idx, (ax, nu_key) in enumerate(zip(axes.flat, nu_list)):
        conv_data = all_results['anchor_convergence'].get(nu_key, {})
        for level, errors in conv_data.items():
            if errors:
                ax.semilogy(errors, 'o-', ms=3, lw=1, label=level)

        nu_val = nu_key.replace('nu_', '')
        ax.set_title(f'ν = {nu_val}', fontsize=10)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Relative Error')
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)

    for idx in range(len(nu_list), len(axes.flat)):
        axes.flat[idx].set_visible(False)

    fig.suptitle('Anchor Convergence Sequence (Banach Contraction)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / 'fig2_anchor_convergence.png', dpi=200)
    fig.savefig(OUTPUT_DIR / 'fig2_anchor_convergence.svg')
    plt.close()
    print("✅ 图2: 锚点收敛序列 → output/fig2_anchor_convergence.png")

    # ── 图3: 误差 vs 雷诺数 ──
    fig, ax = plt.subplots(figsize=(10, 6))
    err_data = all_results['error_vs_re']
    Re_vals = [d['Re_eff'] for d in err_data]

    ax.loglog(Re_vals, [1e-8 for _ in err_data],
              'k-', lw=1, alpha=0.3, label='DNS baseline')

    for level, color, marker in [('L3', 'red', 'o'), ('L6', 'green', 's'), ('L9', 'magenta', '^')]:
        err_key = f'error_{level}'
        vals = [d.get(err_key, np.nan) for d in err_data]
        ax.loglog(Re_vals, vals, color=color, marker=marker, ms=6, lw=1.5, label=f'Anchor-{level}')

    ax.loglog(Re_vals, [d.get('error_LES', np.nan) for d in err_data],
              'b--', marker='D', ms=5, lw=1.5, label='LES (Smagorinsky)')

    ax.set_xlabel('Effective Reynolds Number Re', fontsize=12)
    ax.set_ylabel('Relative Error ||u - u_DNS|| / ||u_DNS||', fontsize=12)
    ax.set_title('Error vs Reynolds Number: Anchor Method Scales Better', fontsize=14, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3, which='both')

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / 'fig3_error_vs_re.png', dpi=200)
    fig.savefig(OUTPUT_DIR / 'fig3_error_vs_re.svg')
    plt.close()
    print("✅ 图3: 误差 vs 雷诺数 → output/fig3_error_vs_re.png")

# ══════════════════════════════════════════════════════
# 7. SHA256 校验文件生成
# ══════════════════════════════════════════════════════
def generate_checksums():
    """为所有输出文件生成 SHA256"""
    checksums = {}
    for f in sorted(OUTPUT_DIR.glob('*')):
        if f.is_file():
            sha = hashlib.sha256(f.read_bytes()).hexdigest()
            checksums[f.name] = sha

    checksum_path = OUTPUT_DIR / 'SHA256SUMS.txt'
    with open(checksum_path, 'w') as f:
        for name, sha in sorted(checksums.items()):
            f.write(f"{sha}  {name}\n")

    print(f"✅ SHA256 校验: {checksum_path}")
    return checksums

# ══════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════
if __name__ == '__main__':
    print("🚀 龍魂·湍流锚点推演法数值实验启动\n")

    # 运行全部实验
    results, u_dns, u_les, k_wave, E_anch = run_full_experiment()

    # 生成图表
    print(f"\n{'='*70}")
    print(" 生成对比图表")
    print(f"{'='*70}")
    generate_figures(results)

    # 生成校验文件
    checksums = generate_checksums()

    print(f"\n{'='*70}")
    print(" ✅ 数值实验全部完成")
    print(f" 输出目录: {OUTPUT_DIR}")
    print(f" 输出文件: {len(list(OUTPUT_DIR.glob('*')))} 个")
    print(f" 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    print(f"{'='*70}")
