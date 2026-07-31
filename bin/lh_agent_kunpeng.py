# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍芯·鲲鹏共生体调度中枢 v1.1
DNA: #龍芯⚡️丙午·乙未·丁酉·子时·☰乾-KUNPENG-AGENT-v1.1
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

CodeBuddy端常驻调度中枢——共生体的"嘴替+任务队列"。
接收老大一句话指令→分析路由→下发鲲鹏→收集结果→回报。

共生体：你在CodeBuddy发号，20个人格在鲲鹏冲锋。

v1.1: 同步自动mkdir·消locale警告·全链路LC_ALL=C
"""
import json, sys, os, subprocess, time, hashlib, uuid, tempfile
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
from enum import Enum

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 常量
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DNA = "#龍芯⚡️丙午·乙未·丁酉·子时·☰乾-KUNPENG-AGENT-v1.1"
版本 = "v1.1"

# 鲲鹏SSH配置
鲲鹏SSH = "ssh -i ~/.ssh/longhun_kunpeng_ed25519 -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@119.13.90.27"
鲲鹏工作目录 = "/opt/longhun-system"
鲲鹏集群引擎 = f"{鲲鹏工作目录}/engines/longhun/kunpeng_persona_cluster.py"
鲲鹏路由引擎 = f"{鲲鹏工作目录}/engines/collaboration/kunpeng_router.py"

# 本地路径
本地路由引擎 = Path(__file__).parent.parent / "engines" / "collaboration" / "kunpeng_router.py"
本地路由引擎 = str(本地路由引擎.resolve())
工作目录 = Path(__file__).parent.parent


class 任务状态(str, Enum):
    等待中 = "等待中"
    已路由 = "已路由"
    已下发 = "已下发"
    执行中 = "执行中"
    已完成 = "已完成"
    失败 = "失败"
    熔断 = "熔断"

class 审计色(str, Enum):
    PASS = "🟢通过"
    PENDING = "🟡待核"
    RED = "🔴红线"

class 成本层(str, Enum):
    本机 = "本机"
    鲲鹏 = "鲲鹏"
    云端API = "云端API"

@dataclass
class 调度任务:
    """调度中枢管理的任务"""
    id: str = ""
    dna: str = ""
    原始指令: str = ""
    路由结果: dict = field(default_factory=dict)
    状态: 任务状态 = 任务状态.等待中
    成本层: 成本层 = 成本层.鲲鹏
    审计色: 审计色 = 审计色.PENDING
    执行结果: dict = field(default_factory=dict)
    耗时秒: float = 0.0
    创建时间: str = ""
    完成时间: str = ""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 鲲鹏连通性检测
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def 检测鲲鹏连通() -> Tuple[bool, str]:
    """检测鲲鹏服务器是否可达（消locale警告）"""
    try:
        # LC_ALL=C 避免 setlocale 警告干扰
        结果 = subprocess.run(
            f"{鲲鹏SSH} 'export LC_ALL=C && echo ok && hostname && uptime'",
            shell=True, capture_output=True, text=True, timeout=15
        )
        if 结果.returncode == 0:
            return True, 结果.stdout.strip()
        return False, 结果.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "SSH超时"
    except Exception as e:
        return False, str(e)


def 检测鲲鹏引擎() -> Tuple[bool, str]:
    """检测鲲鹏端引擎是否就绪"""
    try:
        结果 = subprocess.run(
            f"{鲲鹏SSH} 'export LC_ALL=C && python3 {鲲鹏集群引擎} --status 2>/dev/null'",
            shell=True, capture_output=True, text=True, timeout=15
        )
        if 结果.returncode == 0:
            return True, 结果.stdout.strip()
        return False, 结果.stderr.strip()
    except Exception as e:
        return False, str(e)


def 同步代码到鲲鹏() -> Tuple[bool, str]:
    """将本地代码同步到鲲鹏（v1.1: 自动创建远端目录+消locale警告）"""
    try:
        # 同步引擎文件
        文件列表 = [
            "engines/longhun/kunpeng_persona_cluster.py",
            "engines/collaboration/kunpeng_router.py",
            "bin/lh_agent_kunpeng.py",
        ]
        
        # 1. 先创建所有需要的远端目录
        远端目录集 = set()
        for f in 文件列表:
            远端路径 = Path(f"{鲲鹏工作目录}/{f}")
            远端目录集.add(str(远端路径.parent))
        
        for 远端目录 in sorted(远端目录集):
            subprocess.run(
                f"{鲲鹏SSH} 'export LC_ALL=C && mkdir -p {远端目录}'",
                shell=True, capture_output=True, timeout=15
            )
        
        # 2. SCP同步文件
        results = []
        全部成功 = True
        for f in 文件列表:
            本地路径 = str(工作目录 / f)
            远端路径 = f"{鲲鹏工作目录}/{f}"
            
            # 检查本地文件是否存在
            if not Path(本地路径).exists():
                results.append(f"{f}: ⚠️ 本地不存在")
                全部成功 = False
                continue
            
            r = subprocess.run(
                f"scp -i ~/.ssh/longhun_kunpeng_ed25519 -o StrictHostKeyChecking=no "
                f"{本地路径} root@119.13.90.27:{远端路径}",
                shell=True, capture_output=True, text=True, timeout=30
            )
            results.append(f"{f}: {'✅' if r.returncode == 0 else '❌ ' + r.stderr.strip()[:60]}")
            if r.returncode != 0:
                全部成功 = False
        
        # 3. 消掉locale警告（安装中文locale）
        subprocess.run(
            f"{鲲鹏SSH} 'export LC_ALL=C && (locale-gen zh_CN.UTF-8 2>/dev/null || localedef -i zh_CN -f UTF-8 zh_CN.UTF-8 2>/dev/null || echo locale_skip)'",
            shell=True, capture_output=True, timeout=15
        )
        
        return 全部成功, "\n".join(results)
    except Exception as e:
        return False, str(e)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 任务分析（本地路由引擎集成）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def 本地路由(任务描述: str, 上下文: dict = None) -> dict:
    """调用本地路由引擎进行任务分析"""
    try:
        上下文 = 上下文 or {}
        结果 = subprocess.run(
            ["python3", 本地路由引擎, "--route", 任务描述, "--json"],
            capture_output=True, text=True, timeout=10,
            cwd=str(工作目录)
        )
        if 结果.returncode == 0:
            return json.loads(结果.stdout)
        return {"error": f"路由引擎返回码{结果.returncode}", "stderr": 结果.stderr}
    except Exception as e:
        return {"error": str(e)}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 任务下发（SSH到鲲鹏）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def 下发任务到鲲鹏(任务数据: dict) -> Tuple[bool, dict]:
    """通过SSH将任务下发到鲲鹏人格集群"""
    try:
        # 构建JSON任务负载
        负载 = json.dumps(任务数据, ensure_ascii=False)
        # 通过SSH传入集群引擎（消locale警告）
        命令 = f"{鲲鹏SSH} 'export LC_ALL=C && python3 {鲲鹏集群引擎} --task '\\''{负载}'\\'''"
        
        结果 = subprocess.run(命令, shell=True, capture_output=True, text=True, timeout=120)
        
        if 结果.returncode == 0:
            try:
                return True, json.loads(结果.stdout)
            except:
                return True, {"raw": 结果.stdout}
        return False, {"error": 结果.stderr}
    except subprocess.TimeoutExpired:
        return False, {"error": "任务超时"}
    except Exception as e:
        return False, {"error": str(e)}


def 下发批量任务到鲲鹏(任务列表: List[dict]) -> Tuple[bool, dict]:
    """通过SSH下发批量任务（JSON文件）"""
    try:
        # 写入临时JSON文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(任务列表, f, ensure_ascii=False)
            本地文件 = f.name
        
        # SCP到鲲鹏
        远端文件 = f"/tmp/kunpeng_tasks_{uuid.uuid4().hex[:8]}.json"
        scp结果 = subprocess.run(
            f"scp -i ~/.ssh/longhun_kunpeng_ed25519 -o StrictHostKeyChecking=no "
            f"{本地文件} root@119.13.90.27:{远端文件}",
            shell=True, capture_output=True, text=True, timeout=30
        )
        
        if scp结果.returncode != 0:
            return False, {"error": f"SCP失败: {scp结果.stderr}"}
        
        # 执行批量任务（消locale警告）
        命令 = f"{鲲鹏SSH} 'export LC_ALL=C && python3 {鲲鹏集群引擎} --json-in {远端文件}'"
        执行结果 = subprocess.run(命令, shell=True, capture_output=True, text=True, timeout=300)
        
        # 清理
        os.unlink(本地文件)
        subprocess.run(f"{鲲鹏SSH} 'rm -f {远端文件}'", shell=True, timeout=10)
        
        if 执行结果.returncode == 0:
            return True, json.loads(执行结果.stdout)
        return False, {"error": 执行结果.stderr}
    except Exception as e:
        return False, {"error": str(e)}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 调度中枢核心
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class 共生体调度中枢:
    """
    龍芯·鲲鹏共生体调度中枢
    
    职责：
    1. 接收老大一句话指令 (CodeBuddy→调度中枢)
    2. 本地路由分析 (调用路由引擎)
    3. 成本判定 (本机/鲲鹏/云端API)
    4. 下发鲲鹏执行 (SSH)
    5. 收集结果回报 (鲲鹏→CodeBuddy→老大)
    """
    
    def __init__(self):
        self.任务历史: List[调度任务] = []
        self.活跃任务: Dict[str, 调度任务] = {}
        self.鲲鹏在线: bool = False
        self.鲲鹏信息: str = ""
    
    def 启动自检(self) -> dict:
        """启动时检查所有依赖"""
        结果 = {
            "本地路由引擎": "✅" if Path(本地路由引擎).exists() else "❌",
            "本地集群引擎": "✅" if Path(str(工作目录 / "engines/longhun/kunpeng_persona_cluster.py")).exists() else "❌",
            "鲲鹏SSH": "⏳ 检查中...",
            "鲲鹏引擎": "⏳ 检查中...",
        }
        
        在线, 信息 = 检测鲲鹏连通()
        self.鲲鹏在线 = 在线
        self.鲲鹏信息 = 信息
        结果["鲲鹏SSH"] = f"{'✅' if 在线 else '❌'} {信息[:80]}"
        
        if 在线:
            ok, info = 检测鲲鹏引擎()
            结果["鲲鹏引擎"] = f"{'✅' if ok else '⚠️'} {info[:80]}"
        else:
            结果["鲲鹏引擎"] = "⏭ 鲲鹏不可达·跳过"
        
        结果["版本"] = 版本
        结果["DNA"] = DNA
        
        return 结果
    
    def 调度(self, 指令: str, 上下文: dict = None, 指定人格: str = None) -> dict:
        """
        🔥 核心调度方法——共生体一句话入口
        
        老大说一句话 → 这个函数搞定一切
        """
        开始 = time.time()
        上下文 = 上下文 or {}
        
        # 1. 创建任务
        任务 = 调度任务(
            id=str(uuid.uuid4())[:8],
            dna=self._生成DNA(指令),
            原始指令=指令,
            状态=任务状态.等待中,
            创建时间=datetime.now(timezone.utc).isoformat(),
        )
        
        # 2. 路由分析
        路由 = 本地路由(指令, 上下文)
        任务.路由结果 = 路由
        任务.状态 = 任务状态.已路由
        
        # 提取路由信息
        route_data = 路由.get("route", {})
        主人格 = route_data.get("primary", "龍芯·鲁班")
        副人格 = route_data.get("secondary", [])
        任务域 = route_data.get("domain", "")
        成本 = route_data.get("cost_tier", "鲲鹏")
        
        # 用户指定人格覆盖
        if 指定人格:
            主人格 = f"龍芯·{指定人格}" if not 指定人格.startswith("龍芯·") else 指定人格
        
        任务.成本层 = 成本层(成本) if 成本 in [e.value for e in 成本层] else 成本层.鲲鹏
        
        # 3. 成本判定
        if 任务.成本层 == 成本层.云端API:
            return {
                "task_id": 任务.id,
                "dna": 任务.dna,
                "status": "需审批",
                "message": "云端API需UID9622审批，已记录。请确认是否继续。",
                "cost": "云端API·需审批",
                "route": route_data,
            }
        
        if 任务.成本层 == 成本层.本机:
            # 本机执行（轻任务）
            任务.状态 = 任务状态.已完成
            任务.审计色 = 审计色.PASS
            任务.耗时秒 = time.time() - 开始
            任务.完成时间 = datetime.now(timezone.utc).isoformat()
            
            结果 = {
                "task_id": 任务.id,
                "dna": 任务.dna,
                "status": "本机完成",
                "route": route_data,
                "primary": 主人格,
                "output": f"[本机] {主人格}处理: {指令}",
                "duration_s": round(任务.耗时秒, 2),
                "cost": "本机·0元",
            }
            任务.执行结果 = 结果
            self.任务历史.append(任务)
            return 结果
        
        # 4. 下发鲲鹏
        任务.状态 = 任务状态.已下发
        self.活跃任务[任务.id] = 任务
        
        成功, 鲲鹏结果 = 下发任务到鲲鹏({
            "id": 任务.id,
            "dna": 任务.dna,
            "task": 指令,
            "primary": 主人格,
            "secondary": 副人格,
            "domain": 任务域,
            "cost_tier": 任务.成本层.value,
            "context": 上下文,
            "parallel": route_data.get("parallel", False),
            "confidence": route_data.get("confidence", 0.5),
        })
        
        if 成功:
            任务.状态 = 任务状态.已完成
            任务.审计色 = 审计色.PASS
        else:
            任务.状态 = 任务状态.失败
            任务.审计色 = 审计色.RED
        
        任务.耗时秒 = time.time() - 开始
        任务.完成时间 = datetime.now(timezone.utc).isoformat()
        任务.执行结果 = 鲲鹏结果 if 成功 else {"error": 鲲鹏结果}
        
        # 5. 清理
        if 任务.id in self.活跃任务:
            del self.活跃任务[任务.id]
        self.任务历史.append(任务)
        
        # 6. 构建回报
        return {
            "task_id": 任务.id,
            "dna": 任务.dna,
            "status": 任务.状态.value,
            "audit": 任务.审计色.value,
            "route": route_data,
            "primary": 主人格,
            "secondary": 副人格,
            "cost": f"{任务.成本层.value}·{'0元' if 任务.成本层 != 成本层.云端API else '需审批'}",
            "result": 任务.执行结果,
            "duration_s": round(任务.耗时秒, 2),
            "summary": self._生成摘要(任务),
        }
    
    def 批量调度(self, 指令列表: List[str], 上下文: dict = None) -> List[dict]:
        """批量任务调度——打包下发鲲鹏"""
        上下文 = 上下文 or {}
        任务数据列表 = []
        
        for 指令 in 指令列表:
            路由 = 本地路由(指令, 上下文)
            route_data = 路由.get("route", {})
            任务数据列表.append({
                "id": str(uuid.uuid4())[:8],
                "dna": self._生成DNA(指令),
                "task": 指令,
                "primary": route_data.get("primary", "龍芯·鲁班"),
                "secondary": route_data.get("secondary", []),
                "domain": route_data.get("domain", ""),
                "cost_tier": route_data.get("cost_tier", "鲲鹏"),
                "context": 上下文,
            })
        
        成功, 结果 = 下发批量任务到鲲鹏(任务数据列表)
        
        if 成功:
            return [{"task": t["task"], "result": r} for t, r in zip(任务数据列表, 结果)] if isinstance(结果, list) else [{"error": "结果格式异常"}]
        return [{"error": 结果}]
    
    def 状态摘要(self) -> dict:
        """返回调度中枢状态"""
        return {
            "版本": 版本,
            "DNA": DNA,
            "鲲鹏在线": self.鲲鹏在线,
            "鲲鹏信息": self.鲲鹏信息[:100] if self.鲲鹏信息 else "",
            "活跃任务": len(self.活跃任务),
            "历史任务": len(self.任务历史),
            "最近任务": [
                {
                    "id": t.id,
                    "task": t.原始指令[:60],
                    "status": t.状态.value,
                    "audit": t.审计色.value,
                    "persona": t.路由结果.get("route", {}).get("primary", ""),
                    "cost": t.成本层.value,
                    "duration_s": t.耗时秒,
                }
                for t in self.任务历史[-5:]
            ] if self.任务历史 else [],
        }
    
    def 同步部署(self) -> dict:
        """同步代码+引擎到鲲鹏"""
        成功, 结果 = 同步代码到鲲鹏()
        
        # 同步后验证
        if 成功:
            ok, info = 检测鲲鹏引擎()
            return {
                "sync": "✅ 成功",
                "details": 结果,
                "verify": f"{'✅' if ok else '❌'} {info[:100]}",
            }
        return {"sync": "❌ 失败", "error": 结果}
    
    def _生成DNA(self, 指令: str) -> str:
        时间戳 = datetime.now().strftime("%Y%m%d%H%M%S")
        哈希 = hashlib.blake2b(指令.encode(), digest_size=4).hexdigest()
        return f"#龍芯⚡️{时间戳}-KUNPENG-AGENT-{哈希}"
    
    def _生成摘要(self, 任务: 调度任务) -> str:
        主人格 = 任务.路由结果.get("route", {}).get("primary", "未知")
        域 = 任务.路由结果.get("route", {}).get("domain", "未知")
        return f"「{任务.原始指令[:40]}...」→ {主人格}({域})·{任务.状态.value}·{任务.成本层.value}:0元·{任务.耗时秒:.1f}s"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI 入口
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    import argparse
    p = argparse.ArgumentParser(
        description="龍芯·鲲鹏共生体调度中枢",
        epilog="你在CodeBuddy发号，20个人格在鲲鹏冲锋。"
    )
    p.add_argument("command", nargs="?", default="status",
                   choices=["status","check","sync","deploy","test","demo"],
                   help="命令: status/check/sync/deploy/test/demo")
    p.add_argument("--task", "-t", type=str, help="单任务调度")
    p.add_argument("--persona", "-p", type=str, help="指定人格")
    p.add_argument("--json", action="store_true", help="JSON输出")
    p.add_argument("--batch", type=str, help="批量任务JSON文件路径")
    
    args = p.parse_args()
    
    中枢 = 共生体调度中枢()
    
    if args.command == "check":
        自检 = 中枢.启动自检()
        if args.json:
            print(json.dumps(自检, ensure_ascii=False, indent=2))
        else:
            print("🐉 龍芯·共生体调度中枢 自检")
            print(f"   版本: {版本}")
            print(f"   DNA: {DNA}")
            for k, v in 自检.items():
                print(f"   {k}: {v}")
    
    elif args.command == "sync" or args.command == "deploy":
        print("📤 同步代码到鲲鹏...")
        结果 = 中枢.同步部署()
        if args.json:
            print(json.dumps(结果, ensure_ascii=False, indent=2))
        else:
            for k, v in 结果.items():
                print(f"   {k}: {v}")
    
    elif args.command == "test":
        print("🧪 运行调度中枢自测...")
        自检 = 中枢.启动自检()
        
        if 中枢.鲲鹏在线:
            测试指令 = ["检查系统状态", "评估训练计划", "安全扫描"]
            for 指令 in 测试指令:
                print(f"\n   调度: 「{指令}」")
                结果 = 中枢.调度(指令)
                if args.json:
                    print(f"     {json.dumps(结果, ensure_ascii=False)}")
                else:
                    print(f"     → {结果.get('primary','?')} | {结果.get('status','?')} | {结果.get('duration_s',0):.1f}s")
        else:
            # 鲲鹏不可达，仅跑路由
            print("   ⚠️ 鲲鹏不可达，仅测试本地路由")
            for 指令 in ["检查系统状态", "安全扫描", "写段代码"]:
                路由 = 本地路由(指令)
                route_data = 路由.get("route", {})
                print(f"   「{指令}」→ {route_data.get('primary','?')}")
        print("   ✅ 自测完成")
    
    elif args.command == "demo":
        print("🐉 龍芯·鲲鹏共生体调度中枢 v1.0")
        print(f"   DNA: {DNA}")
        print(f"   共生体宣言：你在CodeBuddy发号，20人格在鲲鹏冲锋。\n")
        
        自检 = 中枢.启动自检()
        for k, v in 自检.items():
            print(f"   {k}: {v}")
        
        if 中枢.鲲鹏在线:
            print(f"\n   🟢 鲲鹏在线，开始演示调度...")
            结果 = 中枢.调度("推演下季度战略方向", 指定人格="诸葛亮")
            if args.json:
                print(json.dumps(结果, ensure_ascii=False, indent=2))
            else:
                print(f"   调度结果: {结果.get('summary', '')}")
        else:
            print(f"\n   🟡 鲲鹏不可达，展示本地路由演示")
            for 指令 in ["战略推演", "代码开发", "安全审计"]:
                路由 = 本地路由(指令)
                route_data = 路由.get("route", {})
                print(f"   「{指令}」→ {route_data.get('primary')} | 成本:{route_data.get('cost_tier')} | 信:{route_data.get('confidence',0):.2f}")
    
    elif args.command == "status":
        状态 = 中枢.状态摘要()
        if args.json:
            print(json.dumps(状态, ensure_ascii=False, indent=2))
        else:
            print(f"🐉 龍芯·共生体调度中枢 v{状态['版本']}")
            print(f"   鲲鹏: {'🟢在线' if 状态['鲲鹏在线'] else '🔴离线'}")
            print(f"   活跃: {状态['活跃任务']} | 历史: {状态['历史任务']}")
            if 状态['最近任务']:
                print(f"   最近5次调度:")
                for t in 状态['最近任务']:
                    print(f"     {t['status']} {t['persona']} | {t['task'][:40]}... | {t['duration_s']:.1f}s {t['cost']}")
    
    # --task 模式
    if args.task:
        结果 = 中枢.调度(args.task, 指定人格=args.persona)
        if args.json:
            print(json.dumps(结果, ensure_ascii=False, indent=2))
        else:
            print(f"\n   调度结果:")
            print(f"   任务: {args.task}")
            print(f"   主: {结果.get('primary','?')} | 状态: {结果.get('status','?')}")
            print(f"   审计: {结果.get('audit','?')} | 成本: {结果.get('cost','?')}")
            print(f"   摘要: {结果.get('summary','?')}")


if __name__ == "__main__":
    main()
