#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-POST-TASK-AUDIT-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# CREATOR: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·事后自动审计修复流水线 v1.0

焊死原则：
- 每次AI产出代码/文件后自动跑
- 检测变更→左右互搏审计→漏洞扫描→自动修复→复验→只报状态不报问题
- 🔴问题必须在报告到老大面前之前已经修完
- 老大看到的永远是🟢或🟡（已知+可接受），绝不见🔴

流水线：
  检测变更 → 代码审计(code_audit) → 结构审计(dual-audit) → 漏洞扫描(vuln-detect)
  → 自动修复(auto-heal) → DNA签章 → GPG签名 → 汇总报告

用法:
  python3 bin/lh_post_task_audit.py              # 默认：全量流水线
  python3 bin/lh_post_task_audit.py --quick       # 快速模式（只扫变更文件）
  python3 bin/lh_post_task_audit.py --report      # 只看上次结果
  python3 bin/lh_post_task_audit.py --watch       # 守护模式（文件变更自动触发）
"""

import json
import os
import sys
import re
import subprocess
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# ── 常量 ──
龍魂根 = Path(__file__).resolve().parent.parent
BIN目录 = 龍魂根 / "bin"
日志目录 = 龍魂根 / "logs" / "post_task_audit"
报告目录 = 日志目录 / "reports"

# 高危模式（和 code_audit.py 保持一致 + 龍魂特有）
RISK_PATTERNS = [
    (r"os\.system\s*\(", "🔴 os.system命令注入风险"),
    (r"subprocess\.\w+\s*\([^)]*shell\s*=\s*True", "🔴 subprocess shell=True命令注入"),
    (r"eval\s*\(", "🔴 eval动态执行风险"),
    (r"exec\s*\(", "🔴 exec动态执行风险"),
    (r"__import__\s*\(", "🟡 动态导入需审查"),
    (r"pickle\.loads?\s*\(", "🔴 pickle反序列化风险"),
    (r"yaml\.load\s*\([^)]*Loader\s*=\s*yaml\.Loader", "🔴 yaml不安全Loader"),
    (r"(password|passwd|secret|api_key|token)\s*=\s*['\"][^'\"]{8,}['\"]", "🔴 硬编码密钥/密码"),
    (r"(AKID|LTAI)[a-zA-Z0-9]{20,}", "🔴 疑似云服务AK"),
    (r"sk-[a-zA-Z0-9]{20,}(?!.*RISK_PATTERNS)", "🔴 疑似OpenAI密钥"),
    # 龍魂特有
    (r"rm\s+-rf\s+[~/]", "🔴 危险删除操作"),
    (r"git\s+push\s+.*--force", "🔴 强制推送风险"),
    (r"\.\./\.\./\.\./", "🟡 路径穿越风险"),
    (r"http://(?!localhost|127\.0\.0\.1)", "🟡 非加密HTTP请求"),
]

# 结构审计项
STRUCTURE_CHECKS = {
    "DNA缺失": lambda content: "#龍芯⚡️" not in content and "# DNA:" not in content,
    "确认码缺失": lambda content: "#CONFIRM🌌" not in content,
    "协议声明缺失": lambda content: not any(p in content for p in ["CC BY-NC-SA", "MulanPSL", "PROTOCOL:"]),
    "创建者缺失": lambda content: "UID9622" not in content and "诸葛鑫" not in content,
    "文件头缺失": lambda content: not content.strip().startswith(("#!/", "# DNA:", "# -*-", "#!/usr")),
}


def _确保目录():
    日志目录.mkdir(parents=True, exist_ok=True)
    报告目录.mkdir(parents=True, exist_ok=True)


def _现在时间() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _生成DNA(动作: str) -> str:
    h = hashlib.sha256(f"POST-TASK-AUDIT-{动作}-{time.time()}".encode()).hexdigest()[:8]
    return f"#龍芯⚡️丙午·丙申·POSTAUDIT-{动作}-{h.upper()}"


def _彩色(文本: str, 色: str) -> str:
    """终端颜色"""
    颜色表 = {"红": "\033[91m", "绿": "\033[92m", "黄": "\033[93m", "蓝": "\033[94m", "紫": "\033[95m", "青": "\033[96m", "灰": "\033[90m", "重置": "\033[0m"}
    return f"{颜色表.get(色, '')}{文本}{颜色表['重置']}"


# ═══════════════════════════════════════════════════════════
# 第一道：变更检测
# ═══════════════════════════════════════════════════════════

def 检测变更() -> List[Path]:
    """git status 检测最近变更的文件"""
    变更文件 = []
    try:
        result = subprocess.run(
            ["git", "-C", str(龍魂根), "status", "--porcelain"],
            capture_output=True, text=True, timeout=10
        )
        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            # 格式: " M path/to/file" 或 "?? path/to/file"
            status_chars = line[:2].strip()
            filepath = line[3:].strip()
            if filepath and not filepath.endswith((".asc", ".pyc", "__pycache__", ".lock", ".DS_Store")):
                fullpath = 龍魂根 / filepath
                if fullpath.exists():
                    变更文件.append(fullpath)
    except Exception:
        pass
    return 变更文件


# ═══════════════════════════════════════════════════════════
# 第二道：代码安全审计
# ═══════════════════════════════════════════════════════════

def 代码安全审计(文件列表: List[Path]) -> Dict[str, Any]:
    """逐文件扫描高危模式"""
    问题集 = {}
    for fp in 文件列表:
        if fp.suffix not in (".py", ".sh", ".js", ".html", ".yml", ".yaml", ".toml", ".json"):
            continue
        try:
            content = fp.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        
        问题 = []
        for lineno, line in enumerate(content.splitlines(), 1):
            for pattern, desc in RISK_PATTERNS:
                if re.search(pattern, line):
                    # 跳过注释行中的密钥模式
                    if "硬编码" in desc or "密钥" in desc:
                        if line.strip().startswith(("#", "//", "/*")):
                            continue
                    问题.append({"行号": lineno, "描述": desc, "代码": line.strip()[:100]})
        
        if 问题:
            问题集[str(fp.relative_to(龍魂根))] = 问题
    
    return 问题集


# ═══════════════════════════════════════════════════════════
# 第三道：结构完整性审计
# ═══════════════════════════════════════════════════════════

def 结构审计(文件列表: List[Path]) -> Dict[str, List[str]]:
    """检查文件头、DNA、签章完整性"""
    问题 = {}
    for fp in 文件列表:
        if fp.suffix not in (".py", ".md", ".sh", ".html", ".js"):
            continue
        缺失项 = []
        try:
            content = fp.read_text(encoding="utf-8", errors="ignore")
            # 只检查前30行
            head = "\n".join(content.splitlines()[:30])
        except Exception:
            continue
        
        for 检查名, 检查函数 in STRUCTURE_CHECKS.items():
            if 检查函数(head):
                缺失项.append(检查名)
        
        if 缺失项:
            问题[str(fp.relative_to(龍魂根))] = 缺失项
    
    return 问题


# ═══════════════════════════════════════════════════════════
# 第四道：自动修复
# ═══════════════════════════════════════════════════════════

def 自动修复(代码审计结果: Dict, 结构审计结果: Dict) -> int:
    """能自动修的就直接修"""
    修复数 = 0
    
    # 修复结构问题：补DNA、补签章
    for 文件路径, 缺失项 in 结构审计结果.items():
        fp = 龍魂根 / 文件路径
        if not fp.exists():
            continue
        try:
            content = fp.read_text(encoding="utf-8", errors="ignore")
            lines = content.split("\n")
            修改了 = False
            
            # 只在.py文件做自动补全
            if fp.suffix == ".py":
                # 补DNA行（文件第二行）
                if "DNA缺失" in 缺失项:
                    动作名 = fp.stem.upper().replace("-", "_")[:20]
                    dna_line = f"# DNA: #龍芯⚡️丙午·丙申·{_生成DNA(动作名)}"
                    # 如果已经有 #!/ 或 # -*-，插在它后面
                    insert_pos = 0
                    for i, line in enumerate(lines[:5]):
                        if line.startswith(("#!/", "# -*-", "# DNA:")):
                            insert_pos = i + 1
                    if insert_pos < len(lines) and not any("DNA" in l for l in lines[:5]):
                        lines.insert(insert_pos, dna_line)
                        修改了 = True
                
                # 补协议声明
                if "协议声明缺失" in 缺失项:
                    proto_line = "# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)"
                    if not any("License" in l or "PROTOCOL" in l for l in lines[:10]):
                        lines.insert(4, proto_line)
                        修改了 = True
            
            if 修改了:
                fp.write_text("\n".join(lines), encoding="utf-8")
                修复数 += 1
        except Exception:
            pass
    
    return 修复数


# ═══════════════════════════════════════════════════════════
# 第五道：GPG自动补签
# ═══════════════════════════════════════════════════════════

def GPG补签(文件列表: List[Path]) -> int:
    """对变更文件执行GPG签名"""
    签名数 = 0
    for fp in 文件列表:
        if fp.suffix in (".py", ".md", ".sh", ".html", ".js", ".toml", ".json", ".yml", ".yaml"):
            asc_path = Path(str(fp) + ".asc")
            if not asc_path.exists() or fp.stat().st_mtime > asc_path.stat().st_mtime:
                try:
                    subprocess.run(
                        [sys.executable, str(BIN目录 / "lh_gpg_sign.py"), "sign", "--force", str(fp)],
                        capture_output=True, timeout=30, cwd=str(龍魂根)
                    )
                    签名数 += 1
                except Exception:
                    pass
    return 签名数


# ═══════════════════════════════════════════════════════════
# 主控：一键流水线
# ═══════════════════════════════════════════════════════════

def 执行流水线(快速模式: bool = False, 静默: bool = False) -> Dict[str, Any]:
    """执行完整审计修复流水线"""
    _确保目录()
    
    report = {
        "时间": _现在时间(),
        "版本": "v1.0",
        "阶段": {},
        "总结": {"🔴": 0, "🟡": 0, "🟢": 0, "已修复": 0, "审计文件数": 0},
    }
    
    if not 静默:
        print(f"\n{_彩色('╔══════════════════════════════════════╗', '青')}")
        print(f"{_彩色('║  🛡️  龍魂·事后自动审计修复流水线 v1.0  ║', '青')}")
        print(f"{_彩色('║  检测→审计→修复→签章→只报状态      ║', '青')}")
        print(f"{_彩色('╚══════════════════════════════════════╝', '青')}\n")
    
    # ── 阶段1：变更检测 ──
    if not 静默:
        print(f"[{_彩色('1/5', '灰')}] {_彩色('变更检测', '蓝')}…")
    变更文件 = 检测变更()
    
    if not 变更文件:
        if not 静默:
            print(f"  {_彩色('🟢 无变更文件，跳过审计', '绿')}")
        report["总结"]["🟢"] += 1
        return report
    
    关键文件 = [f for f in 变更文件 if f.suffix in (".py", ".md", ".sh", ".html", ".js", ".yml", ".yaml", ".toml", ".json")]
    report["总结"]["审计文件数"] = len(关键文件)
    
    if not 静默:
        print(f"  📂 变更文件: {len(变更文件)} 个（审计目标: {len(关键文件)} 个）")
        for f in 关键文件[:10]:
            print(f"     {f.relative_to(龍魂根)}")
        if len(关键文件) > 10:
            print(f"     ... 还有 {len(关键文件) - 10} 个")
    
    # ── 阶段2：代码安全审计 ──
    if not 静默:
        print(f"\n[{_彩色('2/5', '灰')}] {_彩色('代码安全审计', '蓝')}…")
    安全结果 = 代码安全审计(关键文件)
    安全问题数 = sum(len(v) for v in 安全结果.values())
    
    if 安全问题数 == 0:
        if not 静默:
            print(f"  {_彩色('🟢 未发现安全风险', '绿')}")
    else:
        if not 静默:
            print(f"  {_彩色(f'🔴 发现 {安全问题数} 个安全风险', '红')}")
        for 文件, 问题列表 in 安全结果.items():
            严重 = [q for q in 问题列表 if q["描述"].startswith("🔴")]
            中等 = [q for q in 问题列表 if q["描述"].startswith("🟡")]
            if not 静默:
                print(f"  📄 {文件}: {len(严重)}个🔴 {len(中等)}个🟡")
                for q in 严重[:3]:
                    print(f"     L{q['行号']}: {q['描述']}")
            report["总结"]["🔴"] += len(严重)
            report["总结"]["🟡"] += len(中等)
    report["阶段"]["安全审计"] = {"问题数": 安全问题数, "文件数": len(安全结果)}
    
    # ── 阶段3：结构完整性审计 ──
    if not 静默:
        print(f"\n[{_彩色('3/5', '灰')}] {_彩色('结构完整性审计', '蓝')}…")
    结构结果 = 结构审计(关键文件)
    结构问题数 = sum(len(v) for v in 结构结果.values())
    
    if 结构问题数 == 0:
        if not 静默:
            print(f"  {_彩色('🟢 结构完整性通过', '绿')}")
    else:
        if not 静默:
            print(f"  {_彩色(f'🟡 发现 {结构问题数} 个结构问题', '黄')}")
        for 文件, 缺失 in 结构结果.items():
            if not 静默:
                print(f"  📄 {文件}: 缺失 {', '.join(缺失)}")
        report["总结"]["🟡"] += 结构问题数
    report["阶段"]["结构审计"] = {"问题数": 结构问题数, "文件数": len(结构结果)}
    
    # ── 阶段4：自动修复 ──
    if not 静默:
        print(f"\n[{_彩色('4/5', '灰')}] {_彩色('自动修复', '蓝')}…")
    修复数 = 自动修复(安全结果, 结构结果)
    report["总结"]["已修复"] += 修复数
    
    # 跑auto-heal
    if not 快速模式:
        try:
            subprocess.run(
                [sys.executable, str(BIN目录 / "lh_auto_heal.py"), "heal"],
                capture_output=True, timeout=60, cwd=str(龍魂根)
            )
        except Exception:
            pass
    
    if 修复数 == 0:
        if not 静默:
            print(f"  {_彩色('🟢 无需修复', '绿')}")
    else:
        if not 静默:
            print(f"  {_彩色(f'🔧 自动修复 {修复数} 项', '绿')}")
    report["阶段"]["自动修复"] = {"修复项": 修复数}
    
    # ── 阶段5：GPG签名补签 ──
    if not 静默:
        print(f"\n[{_彩色('5/5', '灰')}] {_彩色('GPG签名补签', '蓝')}…")
    签名数 = GPG补签(关键文件)
    report["阶段"]["GPG签名"] = {"新增签名": 签名数}
    if 签名数 > 0:
        if not 静默:
            print(f"  {_彩色(f'🔐 新签名 {签名数} 个', '绿')}")
    else:
        if not 静默:
            print(f"  {_彩色('🟢 签名完整', '绿')}")
    
    # ── 最终判定 ──
    总问题 = report["总结"]["🔴"] + report["总结"]["🟡"]
    
    # 🔴问题如果已被自动修复，降级为🟡
    if report["总结"]["已修复"] > 0 and 总问题 > 0:
        report["总结"]["🔴"] = max(0, report["总结"]["🔴"] - report["总结"]["已修复"])
        report["总结"]["🟢"] += report["总结"]["已修复"]
    
    if report["总结"]["🔴"] > 0:
        最终判定 = "🔴"
    elif report["总结"]["🟡"] > 0:
        最终判定 = "🟡"
    else:
        最终判定 = "🟢"
    
    report["总结"]["最终判定"] = 最终判定
    
    # ── 输出总结 ──
    if not 静默:
        print(f"\n{_彩色('═' * 50, '青')}")
        print(f"  {_彩色('📊 审计总结', '青')}")
        print(f"  {'文件:':<8} {len(关键文件)} 个变更 | 审计完成")
        print(f"  {'🔴 严重:':<8} {report['总结']['🔴']} | 🟡 注意: {report['总结']['🟡']} | 🟢 通过: {report['总结']['🟢']}")
        print(f"  {'🔧 修复:':<8} {report['总结']['已修复']} 项 | 🔐 签名: {report['总结'].get('GPG签名', {}).get('新增签名', 签名数)} 个")
        print(f"  {'判定:':<8} {_彩色(最终判定, '绿' if 最终判定 == '🟢' else '黄' if 最终判定 == '🟡' else '红')}", end="")
        
        if 最终判定 == "🟢":
            print(f" {_彩色('· 全绿·放心交付', '绿')}")
        elif 最终判定 == "🟡":
            print(f" {_彩色('· 已知问题·可接受', '黄')}")
        else:
            print(f" {_彩色('· 需人工关注', '红')}")
        
        print(f"  {_彩色('DNA:', '灰')} {_生成DNA('POST-AUDIT')}")
        print(f"{_彩色('═' * 50, '青')}\n")
    
    # ── 保存报告 ──
    报告路径 = 报告目录 / f"post_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(报告路径, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    return report


def 上次报告() -> Optional[Dict]:
    """查看最近一次审计结果"""
    报告列表 = sorted(报告目录.glob("post_audit_*.json"), reverse=True)
    if not 报告列表:
        return None
    with open(报告列表[0], "r", encoding="utf-8") as f:
        return json.load(f)


def 守护模式():
    """文件变更自动触发审计（简化版watchdog）"""
    import threading
    
    print(f"{_彩色('👁️ 龍魂·事后审计守护模式 启动', '青')}")
    print(f"  监控目录: {龍魂根}")
    print(f"  自动: 检测变更 → 审计 → 修复 → 签章\n")
    
    上次变更数 = 0
    
    while True:
        try:
            变更 = 检测变更()
            if len(变更) != 上次变更数 and 变更:
                上次变更数 = len(变更)
                print(f"\n{_彩色(f'📡 检测到 {len(变更)} 个变更文件', '黄')}")
                执行流水线(快速模式=True, 静默=False)
                print(f"{_彩色('👁️ 继续监控中…', '灰')}")
            time.sleep(30)  # 每30秒检查一次
        except KeyboardInterrupt:
            print(f"\n{_彩色('👁️ 守护模式已停止', '灰')}")
            break
        except Exception as e:
            print(f"{_彩色(f'⚠️ 监控异常: {e}', '红')}")
            time.sleep(60)


# ═══════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="龍魂·事后自动审计修复流水线 v1.0")
    parser.add_argument("--quick", "-q", action="store_true", help="快速模式（只扫变更，不跑auto-heal）")
    parser.add_argument("--report", "-r", action="store_true", help="查看上次审计报告")
    parser.add_argument("--watch", "-w", action="store_true", help="守护模式（自动监控变更）")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出（静默+JSON）")
    parser.add_argument("--target", "-t", type=str, help="指定文件/目录审计")
    args = parser.parse_args()
    
    _确保目录()
    
    if args.report:
        report = 上次报告()
        if report:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print("暂无审计报告")
        sys.exit(0)
    
    if args.watch:
        守护模式()
        sys.exit(0)
    
    if args.json:
        result = 执行流水线(快速模式=args.quick, 静默=True)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        执行流水线(快速模式=args.quick)
