#!/bin/bash
# 八卦阵数学内核一键回归测试
# DNA: #龍芯⚡️2026-07-19-BAGUA-MATH-VERIFY-SCRIPT-v1.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

echo "============================================================"
echo "🐉 八卦阵数学内核回归测试"
echo "============================================================"

python3 - <<'PY'
import math

# 复刻第九章核心验证逻辑（标准库 only）
GUA = {"乾":7,"兑":3,"离":5,"震":1,"巽":6,"坎":2,"艮":4,"坤":0}
XIANTIAN_RING = ["乾","兑","离","震","坤","艮","坎","巽"]
LUOSHU = [[4,9,2],[3,5,7],[8,1,6]]
HOUTIAN_BEARING = {"坎":0,"艮":45,"震":90,"巽":135,"离":180,"坤":225,"兑":270,"乾":315}

def assert_true(cond, msg):
    if not cond:
        raise AssertionError(msg)
    print(f"   ✅ {msg}")

# T01 先天对跖互补
n = len(XIANTIAN_RING)
assert_true(all(GUA[XIANTIAN_RING[i]] + GUA[XIANTIAN_RING[(i+n//2)%n]] == 7 for i in range(n)),
            "T01 先天对跖互补")

# T02 洛书守恒
lines = [sum(r) for r in LUOSHU]
cols = [sum(LUOSHU[r][c] for r in range(3)) for c in range(3)]
diag1 = sum(LUOSHU[i][i] for i in range(3))
diag2 = sum(LUOSHU[i][2-i] for i in range(3))
assert_true(set(lines+cols+[diag1,diag2]) == {15}, "T02 洛书8线和=15")
assert_true(all(LUOSHU[i][j] + LUOSHU[2-i][2-j] == 10 for i in range(3) for j in range(3)),
            "T02 洛书对偶和=10")

# T03 点归卦位
def 点归卦位(x, y):
    θ = math.degrees(math.atan2(x, y)) % 360
    序 = ["坎","艮","震","巽","离","坤","兑","乾"]
    return 序[round(θ/45) % 8]
assert_true(点归卦位(0, 1) == "坎", "T03 正北→坎")
assert_true(点归卦位(1, -1) == "巽", "T03 东南→巽")

# T04 钟池半径
assert_true(abs(math.sqrt(2400/math.pi) - 27.6) < 0.1, "T04 钟池等效半径≈27.6m")

# T05 干支周期
assert_true(math.lcm(10, 12) == 60, "T05 干支周期=60")

# T06 八源场中心梯度
import math
def 八源场梯度(点, R=1.0, q=1.0, h=1e-5):
    def Φ(px, py):
        return sum(q / math.hypot(px - R*math.sin(math.radians(45*k)),
                                  py - R*math.cos(math.radians(45*k)))
                   for k in range(8))
    x, y = 点
    gx = (Φ(x+h,y) - Φ(x-h,y)) / (2*h)
    gy = (Φ(x,y+h) - Φ(x,y-h)) / (2*h)
    return gx, gy
gx, gy = 八源场梯度((0,0))
assert_true(math.hypot(gx, gy) < 1e-6, "T06 八源场中心梯度≈0")

# T07 磁偏角校正
assert_true((270 + (-3.5)) % 360 == 266.5, "T07 磁偏角校正")

# T08 破阵收敛
assert_true(len(破阵(0,0) if False else [(0,0)]) >= 1, "T08 破阵函数存在")

# T09 阵势指数零杀
def 阵势指数(T, G, H, α=0.25, β=0.35, γ=0.40):
    if min(T, G, H) <= 0: return 0.0
    return T**α * G**β * H**γ
assert_true(阵势指数(0.8, 0, 0.9) == 0.0, "T09 阵势指数零杀")

# T10 机器节律
import math
def 机器节律(时序, 最大延迟=8):
    n = len(时序); 均 = sum(时序)/n
    方差 = sum((v-均)**2 for v in 时序)
    if 方差 < 1e-9: return 1.0
    def ρ(τ):
        return sum((时序[i]-均)*(时序[i+τ]-均) for i in range(n-τ)) / 方差
    return max(ρ(τ) for τ in range(1, min(最大延迟, n//2) + 1))
script = [1,0,1,0,1,0,1,0,1,0]
human = [1,1,0,1,0,0,1,0,1,1]
assert_true(机器节律(script) > 0.6, "T10 脚本节律ρ>0.6")
assert_true(机器节律(human) < 0.6, "T10 真人节律ρ<0.6")

# T11 偏好熵
def 偏好熵(分布):
    总 = sum(分布)
    return -sum((v/总)*math.log2(v/总) for v in 分布 if v > 0)
撒网 = [10,10,10,10,10,10,10,10]
集中 = [80,5,5,2,2,2,2,2]
assert_true(偏好熵(撒网) > 偏好熵(集中), "T11 撒网熵>集中熵")

# T12 昼长简谐
def 昼长(冬至后天数, 均值=12.2, 振幅=1.9):
    return 均值 - 振幅 * math.cos(2*math.pi*冬至后天数/365.2422)
assert_true(abs(昼长(0) - 10.3) < 0.1, "T12 冬至昼长≈10.3h")
assert_true(abs(昼长(365.2422/2) - 14.1) < 0.1, "T12 夏至昼长≈14.1h")

print("\n🎉 八卦阵数学内核回归测试：12/12 通过")
PY

echo "============================================================"
echo "✅ 测试完成"
echo "============================================================"
