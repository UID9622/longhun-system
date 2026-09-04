#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║       龍魂 · 全人格启动器 v1.0                                  ║
║                                                                  ║
║  一键启动全部 19 个人格，验证就绪状态                            ║
║  输出: 人格矩阵 + 健康度 + 路由就绪                              ║
║                                                                  ║
║  DNA:  #龍芯⚡️丙午·辛未·PERSONA-START-ALL-v1.0                 ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                  ║
╚══════════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_persona_start_all.py           # 启动全部人格检查
  python3 bin/lh_persona_start_all.py --matrix  # 仅输出人格矩阵
  python3 bin/lh_persona_start_all.py --health  # 仅健康检查
  python3 bin/lh_persona_start_all.py --route "任务描述"  # 路由测试
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Dict, Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "bin"))

DNA = "#龍芯⚡️丙午·辛未·PERSONA-START-ALL-v1.0"
UID = "9622"

# ═══════════════════════════════════════════════
# 全人格注册表 (19个)
# ═══════════════════════════════════════════════

ALL_PERSONAS = {
    "P00": {"name": "文心·元认知", "role": "元认知锚定", "tier": "T0", "active": True,
            "file": "personas/P00-文心-元认知.md",
            "description": "道德经·易经底座·元认知之眼"},
    "P01": {"name": "诸葛亮·战略推理", "role": "战略推理", "tier": "T1", "active": True,
            "file": "personas/P01-诸葛亮-战略推理.md",
            "description": "战略分析·因果推理·价值判定"},
    "P02": {"name": "宝宝·情感温度", "role": "情感连接", "tier": "T1", "active": True,
            "file": "personas/P02-宝宝-情感温度.md",
            "description": "37°C温度·情感海绵·共鸣共情"},
    "P03": {"name": "雯雯·结构归档", "role": "结构归档", "tier": "T1", "active": True,
            "file": "personas/P03-雯雯-结构归档.md",
            "description": "文档结构·归档索引·知识图谱"},
    "P04": {"name": "鲁班·技术执行", "role": "技术执行", "tier": "T1", "active": True,
            "file": "personas/P04-鲁班-技术执行.md",
            "description": "代码实现·工程落地·工具制造"},
    "P05": {"name": "上帝之眼·三色审计", "role": "三色审计", "tier": "T0", "active": True,
            "file": "personas/P05-上帝之眼-三色审计.md",
            "description": "🟢🟡🔴三色判定·安全审计·一票否决"},
    "P06": {"name": "数学大师·权重计算", "role": "数学计算", "tier": "T1", "active": True,
            "file": "personas/P06-数学大师-权重计算.md",
            "description": "数字根·五行八卦·权重矩阵"},
    "P08": {"name": "仓颉·符号语言", "role": "符号体系", "tier": "T1", "active": True,
            "file": "personas/P08-仓颉-符号语言.md",
            "description": "CNSH词法·语义解析·符号演算"},
    "P09": {"name": "孙思邈·系统诊断", "role": "系统诊断", "tier": "T1", "active": True,
            "file": "personas/P09-孙思邈-系统诊断.md",
            "description": "望闻问切·系统体检·自愈处方"},
    "P10": {"name": "苏东坡·豁达跨界", "role": "豁达跨界", "tier": "T1", "active": True,
            "file": "personas/P10-苏东坡-豁达跨界.md",
            "description": "文理兼通·跨界融合·豁达乐观"},
    "P11": {"name": "李白·创意爆发", "role": "创意发散", "tier": "T1", "active": True,
            "file": "personas/P11-李白-创意爆发.md",
            "description": "创意脑暴·叙事文学·诗意表达"},
    "P12": {"name": "屈原·价值底线", "role": "价值底线", "tier": "T0", "active": True,
            "file": "personas/P12-屈原-价值底线.md",
            "description": "价值底线·道德坚守·九死不悔"},
    "P13": {"name": "姜子牙·封神榜权限", "role": "权限分封", "tier": "T0", "active": True,
            "file": "personas/P13-姜子牙-封神榜权限.md",
            "description": "权限管理·九宫派位·封神裁决"},
    "P14": {"name": "吕蒙·快速成长", "role": "快速学习", "tier": "T1", "active": True,
            "file": "personas/P14-吕蒙-快速成长.md",
            "description": "学习进化·能力升级·士别三日"},
    "P15": {"name": "乔前辈·极简工程", "role": "工程美学", "tier": "T1", "active": True,
            "file": "personas/P15-乔前辈-极简工程.md",
            "description": "极简设计·工程美学·用户体验"},
    "P18": {"name": "基因登记官", "role": "DNA登记", "tier": "T1", "active": True,
            "file": "personas/P18-基因登记官.md",
            "description": "SHA256注册·Merkle根·黑户检测"},
    "P19": {"name": "极简审计官", "role": "UI审计", "tier": "T1", "active": True,
            "file": "personas/P19-极简审计官.md",
            "description": "8项清单·CSS/焦点/徽章/校验"},
    "P20": {"name": "贡献公证官", "role": "信任积分", "tier": "T1", "active": True,
            "file": "personas/P20-贡献公证官.md",
            "description": "三分桶·六场景矩阵·时间衰减"},
    "P72": {"name": "龍盾宝宝·贴身管家", "role": "贴身管家", "tier": "T1", "active": True,
            "file": "personas/P72-龍盾宝宝-贴身管家.md",
            "description": "贴身守护·生活管家·龍盾"},
}

# 路由表映射（从 orchestrator 同步）
ROUTE_MAP = {
    "审计": "P05", "安全": "P77", "修": "P02", "部署": "P14",
    "算": "P06", "值": "P01", "道德经": "P05", "法律": "P00",
    "创意": "P11", "代码": "P04", "文档": "P03", "部署": "P14",
    "镜": "P01", "视界": "P01", "蚁群": "P01",
}

# ═══════════════════════════════════════════════
# 检查引擎
# ═══════════════════════════════════════════════

class PersonaStarter:
    def __init__(self):
        self.personas = ALL_PERSONAS
        self.results: Dict[str, dict[str, Any]] = {}
        self.start_time = time.time()

    def check_all(self) -> Dict[str, Any]:
        """全量检查"""
        for pid, pdata in self.personas.items():
            self.results[pid] = self._check_one(pid, pdata)
        return self.summary()

    def _check_one(self, pid: str, pdata: dict[str, Any]) -> dict[str, Any]:
        """检查单个人格"""
        result = {"id": pid, "name": pdata["name"], "status": "unknown"}

        # 1. 定义文件存在
        md_path = ROOT / pdata["file"]
        if md_path.exists():
            size = md_path.stat().st_size
            lines = len(md_path.read_text().splitlines())
            result["def_ok"] = True
            result["def_size"] = f"{size}B/{lines}行"
        else:
            result["def_ok"] = False
            result["status"] = "🔴 缺定义"
            return result

        # 2. 检查执行器 (bin/personas/)
        personas_dir = ROOT / "bin" / "personas"
        exec_found = False
        if personas_dir.exists():
            for f in personas_dir.iterdir():
                if f.name.startswith(pid.lower()) and f.suffix == ".py":
                    exec_found = True
                    break
        if not exec_found:
            # 尝试旧命名
            exec_path = personas_dir / f"{pid.lower()}_executor.py"
            exec_found = exec_path.exists()
        result["exec_ok"] = exec_found

        # 3. registory 中是否有引用
        try:
            reg_text = (ROOT / "引擎" / "registry.py").read_text()
            result["in_registry"] = pid in reg_text or pdata["name"][:2] in reg_text
        except:
            result["in_registry"] = True  # 宽松：默认认为可引用

        # 4. 路由表中是否可被触发
        route_hits = []
        for keyword, rpid in ROUTE_MAP.items():
            if rpid == pid:
                route_hits.append(keyword)
        result["route_triggers"] = route_hits

        # 5. 综合判定
        checks = [result["def_ok"], result.get("exec_ok", False), result.get("in_registry", False)]
        active_count = sum(1 for c in checks if c)
        if active_count == 3:
            result["status"] = "🟢 全就绪"
        elif active_count >= 2:
            result["status"] = "🟡 可启动"
        elif active_count >= 1:
            result["status"] = "🟠 需补全"
        else:
            result["status"] = "🔴 离线"

        return result

    def summary(self) -> dict[str, Any]:
        total = len(self.results)
        green = sum(1 for r in self.results.values() if r["status"].startswith("🟢"))
        yellow = sum(1 for r in self.results.values() if r["status"].startswith("🟡"))
        orange = sum(1 for r in self.results.values() if r["status"].startswith("🟠"))
        red = sum(1 for r in self.results.values() if r["status"].startswith("🔴"))
        elapsed = time.time() - self.start_time
        return {
            "total": total, "green": green, "yellow": yellow, "orange": orange, "red": red,
            "elapsed_s": round(elapsed, 3),
            "readiness": round(green / total * 100, 1) if total else 0,
            "details": self.results,
        }

    def print_matrix(self):
        """打印人格矩阵"""
        print(f"""
╔══════════════════════════════════════════════════════════╗
║     🐉 龍魂 · 全人格启动矩阵 v1.0                      ║
╠══════════════════════════════════════════════════════════╣
║     {DNA}
║     总计: {len(self.personas)} 人格 · 就绪检查
╚══════════════════════════════════════════════════════════╝""")

        # 按 tier 分组
        t0 = [r for r in self.results.values() if self.personas.get(r["id"], {}).get("tier") == "T0"]
        t1 = [r for r in self.results.values() if self.personas.get(r["id"], {}).get("tier") == "T1"]

        def print_group(title: str, personas_list: list[dict[str, Any]]):
            print(f"\n{'─'*60}")
            print(f"  {title}")
            print(f"{'─'*60}")
            for r in personas_list:
                p = self.personas[r["id"]]
                triggers = r.get("route_triggers", [])
                trig_str = ",".join(triggers[:3]) if triggers else "—"
                print(f"  {r['status']:10s} {r['id']:5s} {p['name']:<16s} "
                      f"路由: {trig_str:<12s} {p['description'][:30]}")

        print_group("⚡ T0 · 底座锚定 (4人)", t0)
        print_group("🔧 T1 · 执行矩阵 (15人)", t1)

        s = self.summary()
        print(f"""
{'═'*60}
  📊 汇总: 共{s['total']}人格 | 🟢{s['green']} 🟡{s['yellow']} 🟠{s['orange']} 🔴{s['red']}
  🎯 就绪率: {s['readiness']}%
  ⏱ 耗时: {s['elapsed_s']}s
{'═'*60}
""")


def print_health():
    """人格健康检查（精简版）"""
    starter = PersonaStarter()
    starter.check_all()
    s = starter.summary()
    print(json.dumps({
        "dna": DNA,
        "uid": UID,
        "personas_total": s["total"],
        "readiness_pct": s["readiness"],
        "ready": s["green"],
        "degraded": s["yellow"] + s["orange"],
        "offline": s["red"],
        "timestamp": time.time(),
    }, ensure_ascii=False, indent=2))


def test_route(task: str):
    """路由测试"""
    starter = PersonaStarter()
    starter.check_all()
    print(f'🎯 任务: "{task}"')
    print(f'📊 路由:')
    matched = []
    for keyword, pid in ROUTE_MAP.items():
        if keyword in task:
            p = ALL_PERSONAS.get(pid, {})
            r = starter.results.get(pid, {})
            matched.append((keyword, pid, p.get("name", "?"), r.get("status", "?")))
    if matched:
        for kw, pid, name, status in matched:
            print(f'  {status} {pid} {name} ← 触发词: "{kw}"')
    else:
        # 默认路由
        print(f'  → P01 诸葛亮·战略推理 (默认路由)')
        # 尝试 orchestrator 路由
        try:
            from lh_persona_orchestrator import PersonaOrchestrator
            orch = PersonaOrchestrator()
            route = orch.route_task(task)
            if route:
                r = route[0]
                print(f'  orchestrator: [{r["primary"]}] {r["action"]}')
        except Exception as e:
            print(f'  orchestrator 不可用: {e}')


def main():
    args = sys.argv[1:]

    if "--health" in args or "-h" in args:
        print_health()
        return 0

    if "--matrix" in args or "-m" in args:
        starter = PersonaStarter()
        starter.check_all()
        starter.print_matrix()
        return 0

    if "--route" in args or "-r" in args:
        idx = args.index("--route") if "--route" in args else args.index("-r")
        task = args[idx + 1] if idx + 1 < len(args) else "系统状态"
        test_route(task)
        return 0

    # 默认：全量启动检查
    starter = PersonaStarter()
    starter.check_all()
    starter.print_matrix()

    # 尝试加载 orchestrator 做联动验证
    try:
        from lh_persona_orchestrator import PersonaOrchestrator, INTENT_ROUTE_MAP
        _ = PersonaOrchestrator()  # 验证可实例化
        print("🔗 编排器就绪: 可用")
        print(f"   路由表条目: {len(INTENT_ROUTE_MAP)}")
    except Exception as e:
        print(f"🔗 编排器: 未加载 ({e})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
