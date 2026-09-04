# SPEC — lh_math_explorer.py（龍魂·数学难题解决工作流 可执行实现）

## 模式
Mode B（单脚本工具）。

## 目标
将《龍魂·数学难题解决工作流》Step 1–8 落地为一个可运行、可复现、带审计输出的 Python 脚本，并产出解题报告。

## 文件
- `/mnt/agents/output/bin/lh_math_explorer.py` — 主脚本（唯一代码交付物）
- `/mnt/agents/output/lh_math_solve_report.md` — 解题报告（真实运行结果）

## 接口契约

### 核心函数
```python
def digital_root(n: int) -> int          # dr(n) = n - 9 * ((n - 1) // 9)
def sieve(limit: int) -> list[int]       # 埃氏筛，limit 以内全部素数；异常时回退内置小素数表并告警
def wuxing(dr: int) -> str               # 河图映射: 1,6→水; 2,7→火; 3,8→木; 4,9→金; 5→土
def transition_matrix(dr_seq) -> np.ndarray  # M[i][j] = count(i→j)/count(i)，行归一化
def chi_square(freq: dict) -> float      # H0: {1,2,4,5,7,8} 均匀 1/6
def goldbach_weak_check(n: int, prime_set, primes) -> tuple|None  # 返回 (p1,p2,p3) 或 None
def ganzhi(year, month, day) -> dict     # 干支四柱（年/月/日柱）算法生成，禁止手写
def hexagram(day_gz_index: int) -> str   # 64卦名（文王序），index = day_gz_index % 64
```

### 流程（对应工作流 Step）
1. **数据生成**: sieve(N)，打印素数个数；失败回退内置列表 + 🟡 告警
2. **数字根变换**: 全序列 dr；断言 {3,6,9} 仅出现在素数 3 本身
3. **频率统计**: count/freq 六个根值 + 五行分布表
4. **流场构建**: 6×6 转移矩阵（索引 [1,2,4,5,7,8]），特征值/主特征向量，平稳分布
5. **卡方检验**: df=5, α=0.05, 临界值 11.070；输出 χ² 与接受/拒绝
6. **弱哥德巴赫**: 遍历奇数 n=7..N（步长2）。优化路径：n-3 为偶数≥4，查强哥德巴赫分解 n-3=p+q → n=3+p+q；记录失败数与最大验证 n
7. **数学根审计**: dr(Σp) 与 dr(加权数字根和) 一致性校验；三色审计（🟢/🟡/🔴 逐条）
8. **ROOT_CARD**: 固定格式输出（见下），同时写入 `/mnt/agents/output/bin/ROOT_CARD_math_solve.txt`

### 性能基准
- N ∈ {10^4, 10^5, 10^6}：分别计时（筛法 / 哥德巴赫验证），报告峰值内存（tracemalloc）
- 固定 seed=9622，输出须完全可复现

### DNA 追溯码（新规范，2026-07-19 起）
格式: `#龍芯⚡️{年干支}·{月干支}·{日干支}·{卦名}-MATH-SOLVE-v2.0`
- 干支四柱用算法计算（基准日 1900-01-01 = 甲戌），禁止手写
- 卦名 = 文王六十四卦序[日柱干支序号 % 64]
- 报告中标注：以本地 bin/lh_dna_generator.py 输出为最终校正依据

## ROOT_CARD 格式
```
Root: dr=<审计根值>
Wuxing: <五行>
TriColor: <🟢/🟡>
DataLevel: L0_PUBLIC
PrivacyMode: normal
Retention: summary_only
TraceMode: chain
Route: [MATH-SOLVE-EXAMPLE]
Backend: python / jupyter / notion
Action: archive
DNA: <新规范DNA>
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```

## 报告结构（lh_math_solve_report.md）
1. 问题陈述 2. 工具与公式表 3. Step1–8 真实运行结果（数值、矩阵、χ²、失败数） 4. 性能基准表 5. Mermaid 流程图 6. 扩展方向 7. ROOT_CARD
