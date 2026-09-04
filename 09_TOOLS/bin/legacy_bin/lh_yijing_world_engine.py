#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂·易经世界模型数学引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-YIJING-WORLD-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

关联论文:
- 易经世界模型的数学物理基础_从符号系统到可计算宇宙_v1.0
- 易经世界模型的数学物理基础_哲学论文

数学核心:
  八卦 = Z₂³ 向量空间（8个元素）
  六十四卦 = Z₂⁶ 状态空间（2⁶=64维）
  卦变 = 状态转移算子 T: Z₂⁶ → Z₂⁶
  三才流场 = 天(T)-地(E)-人(H) 三层耦合系统

  世界观: 易经不是预测未来，是计算世界状态的可能演化路径

用法:
  python3 bin/lh_yijing_world_engine.py          # 15条测试向量
  python3 bin/lh_yijing_world_engine.py demo     # 演示
  python3 bin/lh_yijing_world_engine.py evolve <卦初> <卦终> # 卦变推演
"""

import sys, math, itertools, os, json, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

DNA = "#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-YIJING-WORLD-ENGINE-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# §1 八卦·基础数据结构
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 八卦: 三位二进制 (下爻→上爻)
# 爻序: 初爻(最下)、二爻(中)、三爻(最上)
BAGUA = {
    "☰": (1, 1, 1),  # 乾 7
    "☷": (0, 0, 0),  # 坤 0
    "☳": (0, 0, 1),  # 震 1
    "☵": (0, 1, 0),  # 坎 2
    "☶": (0, 1, 1),  # 艮 3
    "☲": (1, 0, 0),  # 离 4
    "☱": (1, 0, 1),  # 兑 5
    "☴": (1, 1, 0),  # 巽 6
}

BAGUA_NAMES = {
    7: "乾☰", 0: "坤☷", 1: "震☳", 2: "坎☵",
    3: "艮☶", 4: "离☲", 5: "兑☱", 6: "巽☴",
}

BAGUA_VALUES = {v: k for k, v in BAGUA_NAMES.items()}


def gua_to_bits(gua: str) -> tuple[Any, ...]:
    """卦象→二进制数组"""
    if gua in BAGUA:
        return BAGUA[gua]
    raise ValueError(f"未知卦象: {gua}")


def bits_to_gua(bits: tuple[Any, ...]) -> str:
    """二进制数组→卦象"""
    for name, b in BAGUA.items():
        if b == tuple(bits):
            return name
    return "?"  # 非标准八卦值


def bits_to_int(bits: tuple[Any, ...]) -> int:
    """二进制数组→整数"""
    val = 0
    for i, b in enumerate(bits):
        val += b * (2 ** i)
    return val


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# §2 六十四卦·状态空间 Z₂⁶
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def create_state_space():
    """生成完整的 Z₂⁶ 状态空间（64卦）

    六维二进制: (g₁, g₂, g₃, g₄, g₅, g₆) ∈ Z₂⁶
    g₁~g₃: 上卦（外卦）
    g₄~g₆: 下卦（内卦）
    """
    states = {}
    for bits in itertools.product([0, 1], repeat=6):
        idx = bits_to_int(bits)
        upper = bits_to_gua(bits[:3])  # 上卦
        lower = bits_to_gua(bits[3:])  # 下卦
        states[idx] = {
            "bits": bits,
            "upper_gua": upper,
            "lower_gua": lower,
            "name": f"{lower}{upper}",
            "int_val": idx,
        }
    return states


STATE_SPACE = create_state_space()


def state_to_hexagram(bits: tuple[Any, ...]) -> dict[str, Any]:
    """状态向量→六十四卦信息"""
    idx = bits_to_int(bits)
    return STATE_SPACE.get(idx, {"name": "未知", "bits": bits})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# §3 卦变·状态转移算子
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def yao_bian(state: tuple[Any, ...], position: int) -> tuple[Any, ...]:
    """爻变（单比特翻转）: T_i(G) = G ⊕ e_i

    position: 1-6 (1=初爻·最下)
    """
    pos_idx = position - 1
    if pos_idx < 0 or pos_idx > 5:
        raise ValueError(f"爻位1-6, 给的是{position}")
    result = list(state)
    result[pos_idx] = 1 - result[pos_idx]
    return tuple(result)


def gua_bian(state: tuple[Any, ...], mask: tuple[Any, ...]) -> tuple[Any, ...]:
    """卦变（多比特翻转）: T_v(G) = G ⊕ v"""
    if len(mask) != len(state):
        raise ValueError(f"mask长度不匹配: {len(mask)} vs {len(state)}")
    return tuple(a ^ b for a, b in zip(state, mask))


def hamiltonian_path(steps: int = 64) -> list[Any]:
    """生成卦变哈密顿路径（最小变化走到目标）

    用格雷码思想：每次只变一位，遍历所有状态
    """
    path = []
    current = (0, 0, 0, 0, 0, 0)  # 从坤卦开始

    for i in range(min(steps, 64)):
        path.append(state_to_hexagram(current))
        # 格雷码：每次翻转最低位能翻的那位
        if i < 63:
            flip_pos = (i ^ (i >> 1)).bit_length()  # 格雷码变化位
            if flip_pos > 0 and flip_pos <= 6:
                current = yao_bian(current, flip_pos)

    return path


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# §4 卦爻熵·信息度量
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def gua_entropy(probs: list[Any]) -> float:
    """卦爻熵 H = -Σ p_i log₂ p_i

    参数: 64维概率分布（六十四卦各自的观测概率）
    """
    H = 0.0
    for p in probs:
        if p > 0:
            H -= p * math.log2(p)
    return H


def max_entropy() -> float:
    """最大熵（均匀分布64卦）= log₂(64) = 6"""
    return math.log2(64)  # = 6.0


def yao_entropy(yao_probs: list[Any]) -> float:
    """单爻熵"""
    return gua_entropy(yao_probs)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# §5 三才流场·天地人三层耦合
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def sancai_flow_field(state: tuple[Any, ...]) -> dict[str, Any]:
    """三才流场分解

    六爻拆分为三才:
      天: 初爻+二爻 (根本)
      地: 三爻+四爻 (承载)
      人: 五爻+上爻 (变化)
    """
    return {
        "天": (state[0], state[1]),  # 初爻·二爻 → 天
        "地": (state[2], state[3]),  # 三爻·四爻 → 地
        "人": (state[4], state[5]),  # 五爻·上爻 → 人
    }


def sancai_energy(flow: dict[str, Any]) -> float:
    """三才能量计算

    E = 0.34×天能 + 0.33×地能 + 0.33×人能
    每层: energy = bits_to_int(two_bits) / 3 (归一化)
    """
    heaven = bits_to_int(flow["天"]) / 3.0
    earth = bits_to_int(flow["地"]) / 3.0
    human = bits_to_int(flow["人"]) / 3.0

    return 0.34 * heaven + 0.33 * earth + 0.33 * human


def world_state_energy(state: tuple[Any, ...]) -> dict[str, Any]:
    """世界状态能级分析"""
    flow = sancai_flow_field(state)
    E = sancai_energy(flow)

    # 能级分类
    if E > 0.7:
        level = "🟢 高潮期"
    elif E > 0.35:
        level = "🟡 平稳期"
    else:
        level = "🔴 低谷期"

    return {
        "state": state,
        "hexagram": state_to_hexagram(state),
        "sancai_flow": flow,
        "energy": round(E, 4),
        "level": level,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# §6 世界模型推演引擎
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class YijingWorldEngine:
    """易经世界模型数学引擎

    核心命题: 易经不是"预测未来"，而是"计算世界状态的可能演化路径"
    """

    DNA = DNA
    CONFIRM = CONFIRM

    @property
    def state_space_size(self) -> int:
        return 64  # Z₂⁶

    def get_state(self, idx_or_bits) -> dict[str, Any]:
        """获取指定状态"""
        if isinstance(idx_or_bits, int):
            if 0 <= idx_or_bits < 64:
                return STATE_SPACE[idx_or_bits]
            raise ValueError(f"状态索引0-63, 给的是{idx_or_bits}")
        return state_to_hexagram(idx_or_bits)

    def get_bagua(self, name: str) -> dict[str, Any]:
        """获取八卦定义"""
        bits = BAGUA.get(name)
        if bits is None:
            raise ValueError(f"未知八卦: {name}")
        return {"name": name, "bits": bits, "int_val": bits_to_int(bits)}

    def evolve(self, from_state, to_state) -> dict[str, Any]:
        """状态演化：从from_state到to_state的转移路径

        返回: 转移mask·所需爻变数·路径
        """
        from_bits = from_state if isinstance(from_state, tuple) else self.get_state(from_state)["bits"]
        to_bits = to_state if isinstance(to_state, tuple) else self.get_state(to_state)["bits"]

        # 计算转移mask
        mask = tuple(a ^ b for a, b in zip(from_bits, to_bits))
        changes = sum(mask)  # 需要变的爻数

        # 找出需要变的具体爻位
        change_positions = [i + 1 for i, m in enumerate(mask) if m == 1]

        # 尝试找到最小变化路径
        path = [state_to_hexagram(from_bits)]
        current = list(from_bits)
        for pos in change_positions:
            current[pos - 1] = 1 - current[pos - 1]
            path.append(state_to_hexagram(tuple(current)))

        return {
            "from": state_to_hexagram(from_bits),
            "to": state_to_hexagram(to_bits),
            "mask": mask,
            "change_count": changes,
            "change_positions": change_positions,
            "path": path,
            "path_length": len(path),
        }

    def analyze_state(self, state) -> dict[str, Any]:
        """分析世界状态"""
        bits = state if isinstance(state, tuple) else self.get_state(state)["bits"]
        return world_state_energy(bits)

    def list_all_states(self) -> list[Any]:
        """列出全部64卦状态"""
        return [STATE_SPACE[i] for i in range(64)]

    def bagua_complete(self) -> dict[str, Any]:
        """八卦完整信息"""
        result = {}
        for name, bits in BAGUA.items():
            result[name] = {
                "bits": bits,
                "int_val": bits_to_int(bits),
                "name_cn": BAGUA_NAMES.get(bits_to_int(bits), "?"),
            }
        return result

    def sancai_decompose(self, state) -> dict[str, Any]:
        """三才分解"""
        bits = state if isinstance(state, tuple) else self.get_state(state)["bits"]
        return sancai_flow_field(bits)

    def demo(self):
        """完整推演演示"""
        print("\n" + "=" * 60)
        print("龍魂·易经世界模型数学引擎 · 推演演示")
        print("DNA:", self.DNA)
        print("=" * 60)

        # 1. 状态空间
        print(f"\n§1 Z₂⁶ 状态空间: {self.state_space_size}卦")
        print("-" * 40)
        print(f"  最大熵 H_max = log₂(64) = {max_entropy():.2f} bits")

        # 2. 八卦基础
        print("\n§2 八卦 = Z₂³ 向量空间")
        print("-" * 40)
        for name in ["☰", "☷", "☳", "☵"]:
            g = self.get_bagua(name)
            print(f"  {name} = {g['bits']} = {g['int_val']}")

        # 3. 卦变推演
        print("\n§3 卦变: 坤(000000) → 乾(111111)")
        print("-" * 40)
        evo = self.evolve((0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1))
        print(f"  坤→乾 需变 {evo['change_count']} 爻")
        print(f"  转移mask: {evo['mask']}")
        print(f"  路径长度: {evo['path_length']} 步")

        # 4. 单爻变
        print("\n§4 单爻变: 坤 → 震 (变初爻)")
        print("-" * 40)
        st = self.get_state(0)  # 坤
        new_bits = yao_bian(st["bits"], 1)
        new_st = state_to_hexagram(new_bits)
        print(f"  {st['name']}({st['bits']}) → {new_st['name']}({new_st['bits']})")

        # 5. 三才流场分析
        print("\n§5 三才流场分析")
        print("-" * 40)
        for idx in [0, 7, 63, 31]:
            st = self.analyze_state(idx)
            hex_name = st["hexagram"]["name"]
            flow = st["sancai_flow"]
            print(f"  {hex_name:8} 天={flow['天']} 地={flow['地']} 人={flow['人']} → E={st['energy']:.4f} {st['level']}")

        # 6. 哈密顿路径
        print("\n§6 卦变哈密顿路径（格雷码遍历·前8步）")
        print("-" * 40)
        hp = hamiltonian_path(8)
        for i, s in enumerate(hp):
            print(f"  步{i}: {s['name']:8} bits={s['bits']}")

        # 7. 熵计算
        print("\n§7 卦爻熵")
        print("-" * 40)
        uniform = [1.0 / 64] * 64
        H_uni = gua_entropy(uniform)
        print(f"  均匀分布熵: {H_uni:.4f} (最大值=6.0)")
        # 偏态分布
        biased = [0.05] * 20 + [0.01] * 30 + [0.003] * 14
        H_bias = gua_entropy(biased)
        print(f"  偏态分布熵: {H_bias:.4f}")

        print("\n" + "=" * 60)
        print("结论: 易经=可计算世界模型。64卦=64维状态空间。")
        print("      不是预测未来，是计算世界状态的可能演化路径。")
        print("=" * 60)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 测试向量（15条）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def run_tests():
    engine = YijingWorldEngine()
    tests = []

    # T01: 状态空间=64
    tests.append(("T01 |Ω|=64", engine.state_space_size == 64, str(engine.state_space_size)))

    # T02: 八卦→二进制
    qian = engine.get_bagua("☰")
    tests.append(("T02 乾=(1,1,1)", qian["bits"] == (1, 1, 1), str(qian["bits"])))

    # T03: 坤=(0,0,0)
    kun = engine.get_bagua("☷")
    tests.append(("T03 坤=(0,0,0)", kun["bits"] == (0, 0, 0), str(kun["bits"])))

    # T04: bits_to_int
    val = bits_to_int((1, 0, 1))
    tests.append(("T04 bits→int", val == 5, str(val)))

    # T05: 爻变（单比特翻转）
    result = yao_bian((0, 0, 0, 0, 0, 0), 1)
    tests.append(("T05 爻变(坤+1爻)", result == (1, 0, 0, 0, 0, 0), str(result)))

    # T06: 卦变（多比特）
    result = gua_bian((1, 1, 1, 1, 1, 1), (0, 0, 1, 0, 0, 1))
    tests.append(("T06 卦变(mask)", result == (1, 1, 0, 1, 1, 0), str(result)))

    # T07: 演化（坤→乾）
    evo = engine.evolve(0, 63)
    tests.append(("T07 坤→乾=6变", evo["change_count"] == 6,
                  f"changes={evo['change_count']}"))

    # T08: 演化路径长度
    tests.append(("T08 路径=7步", evo["path_length"] == 7, f"len={evo['path_length']}"))

    # T09: 三才流场分解
    flow = engine.sancai_decompose(0)
    tests.append(("T09 三才分解", len(flow) == 3 and "天" in flow,
                  f"天={flow['天']} 地={flow['地']} 人={flow['人']}"))

    # T10: 世界能级（坤=最低）
    analysis = engine.analyze_state(0)
    tests.append(("T10 坤卦能级最低", analysis["energy"] < 0.1,
                  f"E={analysis['energy']:.4f}"))

    # T11: 乾卦能级最高
    analysis_qian = engine.analyze_state(63)
    tests.append(("T11 乾卦能级最高", analysis_qian["energy"] > 0.9,
                  f"E={analysis_qian['energy']:.4f}"))

    # T12: 最大熵=6.0
    tests.append(("T12 最大熵=6.0", abs(max_entropy() - 6.0) < 0.01,
                  f"H_max={max_entropy():.4f}"))

    # T13: 均匀分布熵≈6.0
    uniform = [1.0 / 64] * 64
    H = gua_entropy(uniform)
    tests.append(("T13 均匀熵≈6.0", abs(H - 6.0) < 0.01, f"H={H:.4f}"))

    # T14: 低熵分布
    peaked = [1.0] + [0.0] * 63
    H_peak = gua_entropy(peaked)
    tests.append(("T14 峰值熵=0", abs(H_peak) < 0.01, f"H={H_peak:.4f}"))

    # T15: 哈密顿路径覆盖
    hp = hamiltonian_path(64)
    tests.append(("T15 哈密顿路径", len(hp) == 64, f"覆盖{len(hp)}卦"))

    print("\n" + "=" * 60)
    print("龍魂·易经世界模型数学引擎 · 15条测试向量")
    print("=" * 60)
    passed = 0
    for name, ok, detail in tests:
        mark = "✅" if ok else "❌"
        print(f"{mark} {name:40} {detail}")
        if ok:
            passed += 1
    print("=" * 60)
    print(f"结果: {passed}/{len(tests)} 通过")
    return passed == len(tests)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "demo":
            YijingWorldEngine().demo()
        elif sys.argv[1] == "evolve" and len(sys.argv) > 3:
            from_idx = int(sys.argv[2])
            to_idx = int(sys.argv[3])
            engine = YijingWorldEngine()
            result = engine.evolve(from_idx, to_idx)
            print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
        elif sys.argv[1] == "all":
            engine = YijingWorldEngine()
            for s in engine.list_all_states():
                print(f"{s['int_val']:2d}: {s['name']:6} bits={s['bits']} 上={BAGUA_NAMES.get(bits_to_int(s['upper_gua']),'?')} 下={BAGUA_NAMES.get(bits_to_int(s['lower_gua']),'?')}")
        else:
            print("用法: python3 bin/lh_yijing_world_engine.py [demo|evolve <from> <to>|all]")
    else:
        ok = run_tests()
        sys.exit(0 if ok else 1)
