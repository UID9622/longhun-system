#!/bin/bash
# 龍魂快捷命令 v4.1
# DNA: #龍芯⚡️丙午·乙申·甲寅·庚午·隨-ALIASES-v4.1
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 来源: 龍魂系统/快捷命令/aliases_v4.0.sh → 吸收对齐+路径标准化
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 路径已对齐至 longhun-system

# 对齐说明：
# - LONGHUN_HOME 从 龍魂系统 → longhun-system 标准路径
# - 账本路径从 ~/.龍魂/ → longhun-system/audit/rule_ledger.jsonl
# - Python导入路径由包路径调整为直接引用

export LONGHUN_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="$LONGHUN_HOME:$PYTHONPATH"

# 加账: 记录事件并执行规则判定
加账() {
    python3 << PYTHON_EOF
import sys
sys.path.insert(0, "$LONGHUN_HOME")
from engines.lh_rule_engine_v4 import 规则引擎, 事件

引擎 = 规则引擎()

编号 = input("事件编号 (EVT-YYYYMMDD-NNN): ").strip() or "EVT-" + __import__('datetime').datetime.now().strftime("%Y%m%d-001")
人物 = input("人物名称: ").strip() or "测试"
行为 = input("行为描述: ").strip() or "测试行为"
犯错 = input("是否犯错? (y/n): ").lower() == 'y'
自扛 = input("是否自扛责任? (y/n): ").lower() == 'y' if 犯错 else False
立正 = input("批评时立正? (y/n): ").lower() == 'y' if 犯错 else False
威胁 = input("包含威胁? (y/n): ").lower() == 'y'
补救 = input("主动补救? (y/n): ").lower() == 'y'

记录 = 事件(
    编号=编号,
    人物=人物,
    行为=行为,
    犯错=犯错,
    自扛=自扛,
    立正=立正,
    威胁=威胁,
    补救=补救
)

结果 = 引擎.执行(记录)

print("\n" + "="*60)
print(f"DNA: {结果['DNA']}")
print(f"状态: {结果['状态']}")
print(f"分数: {结果['分数']}/100")
print(f"规则: {结果['判定结果']['规则匹配']}")
print("="*60)
PYTHON_EOF
}

# 查账: 查询账本
查账() {
    python3 << PYTHON_EOF
import sys
sys.path.insert(0, "$LONGHUN_HOME")
from engines.lh_rule_engine_v4 import 规则引擎

引擎 = 规则引擎()
记录 = 引擎.查询账本()

if not 记录:
    print("账本为空")
else:
    for 项 in 记录[-10:]:
        事件 = 项['事件']
        判定 = 项['判定']
        print(f"  {事件['人物']:8s} | {事件['行为'][:30]:30s} | {判定['分数']:3d}分 | {判定['状态']}")
PYTHON_EOF
}

export -f 加账
export -f 查账

echo "龍魂快捷命令 v4.1 已加载 | 加账 / 查账"
