# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-075176ca
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · 渲染几何引擎 v1.0（Geometry + Rendering）

实时图形基础管线——3D三角形投影到2D屏幕逐像素着色。龍魂视角：
光栅化是「因势利导」——找最高效的近似方法，足够快、足够好就是成功。

核心公式:
  线性变换:  x' = Ax
  透视投影:  (x,y,z) → (x/z, y/z)
  光照模型:  I = kd(L·N) + ks(R·V)^n

知识卡: 渲染几何 · Geometry + Rendering（ID=107 · dr=8·土·艮宫 · 🔴底座）
常见误区: 以为渲染是纯美术活——实际是大量矩阵运算。
落地映射: 数字人 · 视觉 · Metal/OpenGL · 矩阵变换管线

DNA: #龍芯⚡️丙午·甲申·甲子·庚午·䷙大畜-RENDER-GEOMETRY-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）· 工程层 MulanPSL v2
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

用法:
  python3 bin/lh_render_geometry.py --transform "2,0,0;0,2,0;0,0,2" 1,1,1  # 矩阵×向量
  python3 bin/lh_render_geometry.py --project 1,2,5                          # 透视投影
  python3 bin/lh_render_geometry.py --lighting 0,0,1 0.5,0.5,0.707 0,0,-1   # 光照(L,N,V)
  python3 bin/lh_render_geometry.py --self-test
"""

import argparse
import math
import os
import sys


def _stamp() -> str:
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from lh_time_engine import get_output_stamp
        return get_output_stamp()
    except Exception:
        return "🐉[时间引擎不可用]"


# ---------- 向量与矩阵 ----------

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def norm(v):
    return math.sqrt(dot(v, v))


def normalize(v):
    n = norm(v)
    return tuple(x / n for x in v) if n > 0 else v


def transform(v, A):
    """线性变换: x' = Ax（A为行优先矩阵）"""
    return tuple(sum(row[i] * v[i] for i in range(len(v))) for row in A)


def project(v):
    """透视投影: (x,y,z) → (x/z, y/z, z)"""
    x, y, z = v
    if abs(z) < 1e-12:
        raise ZeroDivisionError("z≈0 无法投影(相机平面)")
    return (x / z, y / z, z)


def lighting(L, N, V, kd=0.8, ks=0.5, shininess=32.0):
    """Blinn-Phong简化光照: I = kd·(L·N) + ks·(R·V)^n
    L=光源方向 · N=法线 · V=视线方向 (均归一化)"""
    Ln, Nn, Vn = normalize(L), normalize(N), normalize(V)
    diff = max(dot(Ln, Nn), 0.0)
    # 反射方向 R = 2(N·L)N - L
    R = tuple(2 * diff * Nn[i] - Ln[i] for i in range(3))
    spec = max(dot(R, Vn), 0.0) ** shininess
    I = kd * diff + ks * spec
    return I, diff, spec


def self_test():
    ok = True
    # 1) 知识卡示例: 2倍缩放 (1,1,1)→(2,2,2)
    scale = [[2, 0, 0], [0, 2, 0], [0, 0, 2]]
    r = transform((1, 1, 1), scale)
    t1 = r == (2, 2, 2)
    ok &= t1
    print(f"[1] 缩放2x (1,1,1) → {r} {'✅' if t1 else '❌'}")
    # 2) 透视投影 (1,2,5) → (0.2, 0.4, 5)
    p = project((1, 2, 5))
    t2 = abs(p[0] - 0.2) < 1e-9 and abs(p[1] - 0.4) < 1e-9
    ok &= t2
    print(f"[2] 透视投影 (1,2,5) → ({p[0]:.4f}, {p[1]:.4f}) {'✅' if t2 else '❌'}")
    # 3) 光照: 光垂直照表面 → 漫反射最大
    _, diff, _ = lighting((0, 0, 1), (0, 0, 1), (0, 0, -1))
    t3 = diff > 0.999
    ok &= t3
    print(f"[3] 垂直光照 diff = {diff:.4f} (应为≈1) {'✅' if t3 else '❌'}")
    # 4) 背面光照=0（光在背面）
    _, diff2, _ = lighting((0, 0, -1), (0, 0, 1), (0, 0, -1))
    t4 = diff2 == 0.0
    ok &= t4
    print(f"[4] 背面光照 diff = {diff2:.4f} (应为0) {'✅' if t4 else '❌'}")
    # 5) 叉积: 右手系 i×j=k
    c = cross((1, 0, 0), (0, 1, 0))
    t5 = c == (0, 0, 1)
    ok &= t5
    print(f"[5] 叉积 i×j = {c} {'✅' if t5 else '❌'}")
    print(f"\n🐉 渲染几何自检: {'全绿 ✅' if ok else '有失败 ❌'}")
    return 0 if ok else 1


def _parse_mat(s):
    return [[float(v) for v in row.split(",")] for row in s.split(";")]


def main():
    ap = argparse.ArgumentParser(description="龍魂·渲染几何引擎 v1.0")
    ap.add_argument("--transform", nargs=2, help="矩阵×向量: '1,2;3,4' '1,1'")
    ap.add_argument("--project", help="透视投影: 逗号分隔3D向量")
    ap.add_argument("--lighting", nargs=3, help="光照: L N V (各3分量)")
    ap.add_argument("--self-test", action="store_true", help="自我验证")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(self_test())

    if args.transform:
        A = _parse_mat(args.transform[0])
        v = tuple(float(x) for x in args.transform[1].split(","))
        r = transform(v, A)
        print(f"A = {A}")
        print(f"v = {v} → v' = {tuple(round(x, 4) for x in r)}")
    elif args.project:
        v = tuple(float(x) for x in args.project.split(","))
        print(f"投影前: {v}")
        print(f"投影后: {tuple(round(x, 4) for x in project(v))}")
    elif args.lighting:
        L = tuple(float(x) for x in args.lighting[0].split(","))
        N = tuple(float(x) for x in args.lighting[1].split(","))
        V = tuple(float(x) for x in args.lighting[2].split(","))
        I, diff, spec = lighting(L, N, V)
        print(f"L = {L}\nN = {N}\nV = {V}")
        print(f"漫反射 kd(L·N) = {diff:.4f} · 高光 ks(R·V)^n = {spec:.4f}")
        print(f"光照强度 I = {I:.4f}")
    else:
        ap.print_help()
        return 1
    print(f"\n{_stamp()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
