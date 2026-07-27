#!/usr/bin/env python3
# 龍芯⚡️丙午·丙申·丙辰·亥时·需-AUTO-HEAL-ENGINE-v1.0
"""
龍魂自动审计自愈引擎 v1.0

原则：
- 扫描 → 分级 → 自动修复 → 复验 → 留痕
- 🔴 严重: 自动立即修复（无人工等待）
- 🟡 中等: 自动修复 + 日志记录
- 🟢 低危: 标记 · 下迭代修

联动作战：
- 联动 lh_cross_module_awareness.py（扫描）
- 联动 lh_anti_tamper.py（防篡改）
- 联动 lh_unified_dna_registry.py（DNA追溯）
- 联动 lh_ecosystem_passport.py（服务注册）
"""

import json
import os
import sys
import subprocess
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Any

# ── 常量 ──
龍魂根 = Path(__file__).resolve().parent.parent
BIN目录 = 龍魂根 / "bin"
日志目录 = 龍魂根 / "logs" / "auto_heal"
DNA引擎路径 = BIN目录 / "lh_unified_dna_registry.py"
联动感知路径 = BIN目录 / "lh_cross_module_awareness.py"
防篡改路径 = BIN目录 / "lh_anti_tamper.py"

# 自愈修复记录
自愈记录路径 = Path.home() / ".龍魂" / "auto_heal" / "heal_log.jsonl"


def _确保目录():
    日志目录.mkdir(parents=True, exist_ok=True)
    自愈记录路径.parent.mkdir(parents=True, exist_ok=True)


def _现在时间() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _生成DNA(动作: str) -> str:
    h = hashlib.sha256(f"{动作}{_现在时间()}".encode()).hexdigest()[:8]
    return f"#龍芯⚡️丙午·丙申·丙辰·亥时·需-AUTOHEAL-{动作}-{h.upper()}"


def _记录自愈(动作: str, 目标: str, 结果: str, 详情: str = ""):
    _确保目录()
    记录 = {
        "时间": _现在时间(),
        "动作": 动作,
        "目标": 目标,
        "结果": 结果,
        "详情": 详情,
        "DNA": _生成DNA(动作),
    }
    with open(自愈记录路径, "a", encoding="utf-8") as f:
        f.write(json.dumps(记录, ensure_ascii=False) + "\n")


# ═══════════════════════════════════════════════════════════
# 第一道：语法体检
# ═══════════════════════════════════════════════════════════

def 语法体检() -> Tuple[List[str], List[str]]:
    """扫描所有 bin/*.py 语法，返回 (损坏文件, 警告文件)"""
    损坏 = []
    警告 = []
    
    py_files = sorted(BIN目录.glob("*.py"))
    
    for f in py_files:
        if f.name.startswith("_"):
            continue  # 跳过下划线私有文件
        
        try:
            import py_compile
            py_compile.compile(str(f), doraise=True)
        except py_compile.PyCompileError as e:
            损坏.append(f"{f.name}: {str(e)[:120]}")
        except Exception as e:
            警告.append(f"{f.name}: {str(e)[:120]}")
    
    return 损坏, 警告


def 修复语法(损坏文件: str) -> Tuple[bool, str]:
    """尝试自动修复语法错误"""
    fp = BIN目录 / 损坏文件.split(":")[0]
    if not fp.exists():
        return False, f"文件不存在: {fp}"
    
    content = fp.read_text(encoding="utf-8")
    修复说明 = ""
    
    # 修复1: shebang不在第一行
    if content.startswith("> ") or content.startswith("# "):
        lines = content.split("\n")
        # 找 shebang 行
        shebang_idx = -1
        for i, line in enumerate(lines[:5]):
            if line.startswith("#!/"):
                shebang_idx = i
                break
        if shebang_idx > 0:
            # 把 shebang 移到第一行
            shebang = lines.pop(shebang_idx)
            lines.insert(0, shebang)
            content = "\n".join(lines)
            修复说明 = "shebang移至第1行"
    
    # 写回
    fp.write_text(content, encoding="utf-8")
    
    # 验证
    try:
        import py_compile
        py_compile.compile(str(fp), doraise=True)
        return True, f"✅ {修复说明}" if 修复说明 else "✅ 已修复"
    except py_compile.PyCompileError as e:
        return False, f"❌ 修复失败: {str(e)[:100]}"


# ═══════════════════════════════════════════════════════════
# 第二道：权限体检
# ═══════════════════════════════════════════════════════════

def 权限体检() -> List[str]:
    """检查所有 bin/*.py 是否有执行权限"""
    缺失权限 = []
    for f in sorted(BIN目录.glob("*.py")):
        if not os.access(str(f), os.X_OK):
            缺失权限.append(f.name)
    return 缺失权限


def 修复权限(文件列表: List[str]) -> int:
    """批量赋予执行权限"""
    修复数 = 0
    for fn in 文件列表:
        fp = BIN目录 / fn
        if fp.exists():
            os.chmod(str(fp), 0o755)
            修复数 += 1
    return 修复数


# ═══════════════════════════════════════════════════════════
# 第三道：联动感知扫描
# ═══════════════════════════════════════════════════════════

def 联动扫描() -> Dict[str, Any]:
    """运行 lh_cross_module_awareness.py 获取扫描结果"""
    try:
        result = subprocess.run(
            [sys.executable, str(联动感知路径)],
            capture_output=True, text=True, timeout=60
        )
        output = result.stdout + result.stderr
        
        # 解析结果
        report = {
            "健康度": 0,
            "🔴严重": [],
            "🟡中等": [],
            "🟢低危": [],
        }
        
        for line in output.split("\n"):
            if "健康度:" in line:
                try:
                    report["健康度"] = int(line.split("/")[0].split(":")[-1].strip())
                except Exception:
                    pass
            elif "🔴" in line:
                report["🔴严重"].append(line.strip())
            elif "🟡" in line and "修复" in line:
                report["🟡中等"].append(line.strip())
            elif "🟢" in line:
                report["🟢低危"].append(line.strip())
        
        return report
    except Exception as e:
        return {"错误": str(e)}


# ═══════════════════════════════════════════════════════════
# 第四道：空文件/重复目录检查
# ═══════════════════════════════════════════════════════════

def 结构体检() -> Dict[str, List[str]]:
    """检查项目结构异常"""
    问题 = {"空文件": [], "重复目录": [], "孤立模块": []}
    
    # 检查空文件
    for f in BIN目录.glob("*.py"):
        try:
            if f.stat().st_size == 0:
                问题["空文件"].append(str(f.relative_to(龍魂根)))
        except (FileNotFoundError, OSError):
            pass  # 文件在 glob 和 stat 之间被删除/断开，跳过
    
    # 检查重复目录
    重复对 = [
        ("integrated_modules", "integrated-modules"),
    ]
    for a, b in 重复对:
        if (龍魂根 / a).exists() and (龍魂根 / b).exists():
            问题["重复目录"].append(f"{a} ↔ {b}")
    
    return 问题


# ═══════════════════════════════════════════════════════════
# 主控：一键自检自愈
# ═══════════════════════════════════════════════════════════

def 一键自愈(自动修复: bool = True) -> Dict[str, Any]:
    """全系统扫描 + 自动修复"""
    _确保目录()
    
    report = {
        "时间": _现在时间(),
        "版本": "v1.0",
        "扫描": {},
        "修复": {},
        "总结": {"🔴": 0, "🟡": 0, "🟢": 0, "已修复": 0},
    }
    
    print("╔════════════════════════════════════════╗")
    print("║  🧬 龍魂自动审计自愈引擎 v1.0        ║")
    print("║  原则：扫描→分级→修复→复验→留痕     ║")
    print("╚════════════════════════════════════════╝")
    print()
    
    # ── 第一道：语法体检 ──
    print("【第一道】语法体检…")
    损坏, 警告 = 语法体检()
    report["扫描"]["语法"] = {"损坏": len(损坏), "警告": len(警告)}
    
    if 损坏:
        print(f"  🔴 发现 {len(损坏)} 个语法损坏文件")
        for b in 损坏[:5]:
            print(f"     {b}")
        if len(损坏) > 5:
            print(f"     ... 还有 {len(损坏)-5} 个")
        report["总结"]["🔴"] += len(损坏)
        
        if 自动修复:
            print(f"  🔧 自动修复中…")
            for b in 损坏:
                文件名 = b.split(":")[0]
                ok, msg = 修复语法(文件名)
                if ok:
                    report["总结"]["已修复"] += 1
                    _记录自愈("语法修复", 文件名, "✅", msg)
            print(f"  ✅ 修复完成")
    else:
        print("  🟢 所有文件语法通过")
    
    if 警告:
        for w in 警告:
            print(f"  🟡 {w}")
        report["总结"]["🟡"] += len(警告)
    
    # ── 第二道：权限体检 ──
    print()
    print("【第二道】权限体检…")
    缺权限 = 权限体检()
    report["扫描"]["权限"] = {"缺失": len(缺权限)}
    
    if 缺权限:
        print(f"  🟡 发现 {len(缺权限)} 个文件缺少执行权限")
        if 自动修复:
            修复数 = 修复权限(缺权限)
            report["总结"]["已修复"] += 修复数
            _记录自愈("权限修复", f"{修复数}个文件", "✅")
            print(f"  ✅ 已修复 {修复数} 个文件")
    else:
        print("  🟢 所有文件权限正常")
    
    # ── 第三道：联动感知 ──
    print()
    print("【第三道】联动感知扫描…")
    联动 = 联动扫描()
    report["扫描"]["联动"] = 联动.get("健康度", 0)
    
    if 联动.get("🔴严重"):
        print(f"  🔴 联动健康度: {联动.get('健康度', 0)}/100")
        for item in 联动["🔴严重"][:3]:
            print(f"     {item[:100]}")
        report["总结"]["🔴"] += len(联动["🔴严重"])
    else:
        print(f"  🟢 联动正常")
    
    if 联动.get("🟡中等"):
        report["总结"]["🟡"] += len(联动["🟡中等"])
    
    # ── 第四道：结构体检 ──
    print()
    print("【第四道】结构体检…")
    结构 = 结构体检()
    结构问题数 = sum(len(v) for v in 结构.values())
    report["扫描"]["结构"] = 结构问题数
    
    if 结构问题数 > 0:
        for 类别, items in 结构.items():
            if items:
                print(f"  🟡 {类别}: {len(items)}个")
                for item in items[:3]:
                    print(f"     {item}")
        report["总结"]["🟡"] += 结构问题数
    else:
        print("  🟢 结构正常")
    
    # ── 总结 ──
    print()
    print("═" * 40)
    print(f"  🔴 严重: {report['总结']['🔴']} | 🟡 中等: {report['总结']['🟡']} | 🟢 低危: {report['总结']['🟢']}")
    print(f"  🔧 已自动修复: {report['总结']['已修复']} 项")
    print(f"  📋 日志: {自愈记录路径}")
    print(f"  DNA: {_生成DNA('FULL-SCAN')}")
    
    # 保存报告
    报告路径 = 日志目录 / f"heal_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(报告路径, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  📄 报告: {报告路径}")
    print("═" * 40)
    
    return report


def 自愈历史(最近: int = 20) -> List[Dict]:
    """查看自愈历史"""
    if not 自愈记录路径.exists():
        return []
    记录 = []
    with open(自愈记录路径, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                记录.append(json.loads(line))
    return 记录[-最近:]


# ═══════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "scan":
            # 仅扫描不修复
            一键自愈(自动修复=False)
            
        elif cmd == "heal":
            # 扫描 + 自动修复
            一键自愈(自动修复=True)
            
        elif cmd == "history":
            # 查看历史
            history = 自愈历史()
            if history:
                for h in history:
                    print(f"[{h['时间'][:16]}] {h['动作']}: {h['目标']} → {h['结果']}")
            else:
                print("暂无自愈记录")
                
        elif cmd == "syntax":
            # 仅语法检查
            损坏, 警告 = 语法体检()
            print(f"语法检查: {len(损坏)}损坏, {len(警告)}警告")
            for b in 损坏:
                print(f"  🔴 {b}")
            for w in 警告:
                print(f"  🟡 {w}")
                
        elif cmd == "perm":
            # 仅权限检查
            缺 = 权限体检()
            print(f"权限检查: {len(缺)}缺少")
            for p in 缺:
                print(f"  🟡 {p}")
                
        elif cmd == "struct":
            # 仅结构检查
            s = 结构体检()
            for k, v in s.items():
                if v:
                    print(f"{k}:")
                    for item in v:
                        print(f"  - {item}")
                        
        else:
            print(f"用法: lh_auto_heal.py [scan|heal|history|syntax|perm|struct]")
            print(f"  scan   - 仅扫描不修复")
            print(f"  heal   - 全扫描 + 自动修复（默认）")
            print(f"  history - 自愈历史")
            print(f"  syntax - 仅语法检查")
            print(f"  perm   - 仅权限检查")
            print(f"  struct - 仅结构检查")
    else:
        # 默认：全扫描 + 自动修复
        一键自愈(自动修复=True)
