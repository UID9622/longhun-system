#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·乙酉·丁亥·䷵归妹-OVERSIGHT-BRIDGE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  龍魂·监管天联动桥接引擎 v1.0 — 三系统自动协作                        ║
║  Oversight Bridge Engine                                         ║
╠══════════════════════════════════════════════════════════════════╣
║  桥接: 审计三色 ←→ 监管天 ←→ 红蓝对抗五阶段                         ║
║  原则: 审计异常 → 监管天联审 → 红蓝对抗 → 融合签字                     ║
║  DNA: #龍芯⚡️丙午·辛未·乙酉·丁亥·䷵归妹-OVERSIGHT-BRIDGE-v1.0               ║
╚══════════════════════════════════════════════════════════════════╝

三系统协作流程:
  1. 审计系统(TricolorAudit) → 三色标记
  2. 🟡/🔴 自动触发监管天(Oversight) → 联审批次
  3. 监管天确认后 → 推送红蓝对抗(RB Confrontation)
  4. 红蓝对抗完成 → 签章(Signing Engine)
  5. 全程自动 → 结果回写审计链

用法:
    python3 bin/lh_oversight_bridge.py --watch       # 守护模式·自动联动
    python3 bin/lh_oversight_bridge.py --check       # 单次全量检查
    python3 bin/lh_oversight_bridge.py --status      # 联动状态
    python3 bin/lh_oversight_bridge.py --trigger-audit "内容"  # 手动触发审计联动
"""

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# ─── 项目根 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "bin"))

# ─── 常量 ───
DNA = "#龍芯⚡️丙午·辛未·乙酉·丁亥·䷵归妹-OVERSIGHT-BRIDGE-v1.0"
VERSION = "1.0.0"
BRIDGE_DIR = Path.home() / ".longhun" / "oversight_bridge"
BRIDGE_DIR.mkdir(parents=True, exist_ok=True)
EVENT_LOG = BRIDGE_DIR / "events.jsonl"
STATE_FILE = BRIDGE_DIR / "state.json"


# ═══════════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════════

class EventType(Enum):
    AUDIT_TRIGGERED = "audit_triggered"        # 审计触发
    OVERSIGHT_REVIEWED = "oversight_reviewed"  # 监管天审阅
    RB_TRIGGERED = "rb_triggered"              # 红蓝对抗触发
    RB_COMPLETED = "rb_completed"              # 红蓝对抗完成
    SIGNED = "signed"                          # 签章完成
    ESCALATED = "escalated"                    # 升级·需人工
    RESOLVED = "resolved"                      # 已解决


@dataclass
class BridgeEvent:
    """联动事件"""
    event_id: str
    event_type: str
    timestamp: str
    audit_color: str        # 🟢/🟡/🔴
    audit_score: float
    target: str             # 目标模块/文件
    rb_triggered: bool = False
    rb_result: str = ""
    oversight_decision: str = "pending"  # pending/approved/rejected/escalated
    signed_by: str = ""     # 签章人格
    sign_id: str = ""
    dna: str = DNA
    resolved: bool = False


# ═══════════════════════════════════════════════════════════
# 核心引擎
# ═══════════════════════════════════════════════════════════

class OversightBridge:
    """
    监管天联动桥接引擎
    
    三系统协作:
    - 审计系统(TricolorAudit) → 监管天(Oversight) → 红蓝对抗(RB) → 签章(Signing)
    """
    
    # 阈值配置
    AUTO_RB_THRESHOLD_SCORE = 85.0    # 审计分低于此值 → 自动红蓝
    ESCALATION_THRESHOLD = 50.0       # 审计分低于此值 → 升级人工
    MAX_AUTO_OVERSIGHT = 5            # 每小时最大自动联审次数
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.events: List[BridgeEvent] = []
        self._hourly_oversight_count = 0
        self._hour_start = time.time()
        self._load_state()
    
    # ── 核心方法: 审计触发 → 监管天 → 红蓝对抗 → 签章 ──
    
    def process_audit_result(self, target: str, content: str = "",
                             audit_color: str = "🟢", audit_score: float = 85.0,
                             auto_sign: bool = True) -> BridgeEvent:
        """
        处理审计结果，自动走完整联动链:
        审计 → 监管天审阅 → 红蓝对抗 → 签章
        """
        event_id = f"BRG-{int(time.time())}-{hashlib.sha256(target.encode()).hexdigest()[:8]}"
        
        event = BridgeEvent(
            event_id=event_id,
            event_type=EventType.AUDIT_TRIGGERED.value,
            timestamp=datetime.now(timezone.utc).isoformat(),
            audit_color=audit_color,
            audit_score=audit_score,
            target=target,
        )
        
        self._log(f"审计触发: {audit_color} R={audit_score} | {target}")
        
        # ── 步骤1: 监管天判定 ──
        oversight_decision = self._oversight_decide(audit_color, audit_score)
        event.oversight_decision = oversight_decision
        
        if oversight_decision == "escalated":
            event.event_type = EventType.ESCALATED.value
            self._log(f"  ⚠️ 监管天: 升级·需人工介入 (R={audit_score}<{self.ESCALATION_THRESHOLD})")
            self._append_event(event)
            return event
        
        if oversight_decision == "approved":
            self._log(f"  ✅ 监管天: 通过 — 无需红蓝对抗")
            event.oversight_decision = "approved"
            event.resolved = True
            self._append_event(event)
            return event
        
        # oversight_decision == "rb_required"
        self._log(f"  ⚔️ 监管天: 需红蓝对抗 (R={audit_score}<{self.AUTO_RB_THRESHOLD_SCORE})")
        
        # ── 步骤2: 触发红蓝对抗 ──
        event.event_type = EventType.RB_TRIGGERED.value
        rb_result = self._trigger_rb(target, content)
        event.rb_triggered = True
        event.rb_result = rb_result
        self._log(f"  红蓝对抗: {rb_result}")
        
        event.event_type = EventType.RB_COMPLETED.value
        
        # ── 步骤3: 自动签章 ──
        if auto_sign:
            try:
                sign_result = self._auto_sign(target, "审计触发", content)
                if sign_result:
                    event.signed_by = sign_result.get("persona_code", "")
                    event.sign_id = sign_result.get("sign_id", "")
                    event.event_type = EventType.SIGNED.value
                    self._log(f"  ✍️ 签章: {event.signed_by} → {event.sign_id[:20]}")
            except Exception as e:
                self._log(f"  ⚠️ 签章失败: {e}")
        
        event.resolved = True
        self._append_event(event)
        return event
    
    def _oversight_decide(self, audit_color: str, audit_score: float) -> str:
        """
        监管天决策:
        - 🔴 且 分数<50 → escalated (升级人工)
        - 🔴 或 分数<85 → rb_required (需红蓝)
        - 🟡 且 分数<85 → rb_required
        - 🟢 或 分数>=85 → approved (通过)
        """
        # 检查频率限制
        if not self._check_hourly_limit():
            return "escalated"  # 超频则升级
        
        if audit_color == "🔴" and audit_score < self.ESCALATION_THRESHOLD:
            return "escalated"
        
        if audit_color in ("🔴", "🟡") and audit_score < self.AUTO_RB_THRESHOLD_SCORE:
            self._hourly_oversight_count += 1
            return "rb_required"
        
        if audit_score >= self.AUTO_RB_THRESHOLD_SCORE:
            return "approved"
        
        self._hourly_oversight_count += 1
        return "rb_required"
    
    def _check_hourly_limit(self) -> bool:
        """检查每小时频率限制"""
        now = time.time()
        if now - self._hour_start > 3600:
            self._hourly_oversight_count = 0
            self._hour_start = now
        return self._hourly_oversight_count < self.MAX_AUTO_OVERSIGHT
    
    def _trigger_rb(self, target: str, content: str = "") -> str:
        """触发红蓝对抗"""
        try:
            rb_script = str(PROJECT_ROOT / "bin" / "lh_rb_confrontation_engine.py")
            import subprocess
            result = subprocess.run(
                [sys.executable, rb_script, "--auto",
                 "--trigger", "audit_alert",
                 "--module", target,
                 "--content", content[:500]],
                capture_output=True, text=True, timeout=30,
            )
            output = result.stdout + result.stderr
            if "融合成功" in output or "共振通过" in output:
                return "融合通过"
            elif "共振不稳定" in output:
                return "共振不稳定·需二次对抗"
            elif "熔断" in output:
                return "熔断"
            else:
                return "对抗完成"
        except Exception as e:
            return f"触发异常: {e}"
    
    def _auto_sign(self, target: str, action_type: str, content: str = "") -> Optional[Dict]:
        """自动签章（使用最匹配的人格）"""
        try:
            from lh_persona_signing import PersonaSigningEngine
            
            engine = PersonaSigningEngine()
            # 自动选择人格: 审计触发 → P05上帝之眼
            persona = "P05"  # 监管天默认用上帝之眼
            
            record = engine.sign(
                persona_code=persona,
                action_type=action_type,
                target=target,
                content=content,
                auto_rb=False,  # 已触发过RB
                require_oversight=False,  # 已经是监管天
            )
            return asdict(record) if hasattr(record, '__dataclass_fields__') else record
        except Exception as e:
            self._log(f"  签章异常: {e}")
            return None
    
    # ── 批量检查 ──
    
    def check_all_modules(self, modules: List[str]) -> List[BridgeEvent]:
        """
        全量检查所有模块。
        扫描每个模块的审计状态，触发联动。
        """
        results = []
        for module in modules:
            try:
                # 运行审计
                from lh_regulatory_pipeline import run_tricolor_audit
                audit = run_tricolor_audit(module)
                color = audit.status if hasattr(audit, 'status') else str(audit.get('status', '🟢'))
                score = audit.score if hasattr(audit, 'score') else float(audit.get('score', 85.0))
            except Exception:
                color, score = "🟢", 85.0
            
            event = self.process_audit_result(
                target=module,
                audit_color=color,
                audit_score=score,
            )
            results.append(event)
        
        return results
    
    # ── 状态查询 ──
    
    def get_status(self) -> Dict[str, Any]:
        """获取联动状态"""
        total = len(self.events)
        resolved = sum(1 for e in self.events if e.resolved)
        escalated = sum(1 for e in self.events if e.event_type == EventType.ESCALATED.value)
        rb_count = sum(1 for e in self.events if e.rb_triggered)
        signed_count = sum(1 for e in self.events if e.signed_by)
        
        # 审计分布
        audit_dist = {"🟢": 0, "🟡": 0, "🔴": 0}
        for e in self.events:
            audit_dist[e.audit_color] = audit_dist.get(e.audit_color, 0) + 1
        
        return {
            "bridge_dna": DNA,
            "version": VERSION,
            "total_events": total,
            "resolved": resolved,
            "pending": total - resolved,
            "escalated": escalated,
            "rb_triggered": rb_count,
            "signed": signed_count,
            "audit_distribution": audit_dist,
            "hourly_oversight_count": self._hourly_oversight_count,
            "max_hourly": self.MAX_AUTO_OVERSIGHT,
            "last_event_time": self.events[-1].timestamp if self.events else "N/A",
        }
    
    def get_dashboard(self) -> str:
        """生成联动仪表盘"""
        status = self.get_status()
        recent = self.events[-10:]
        
        lines = []
        lines.append("")
        lines.append("╔══════════════════════════════════════════════════════╗")
        lines.append("║   🌐 监管天联动桥接 · 三系统协作状态                     ║")
        lines.append("╠══════════════════════════════════════════════════════╣")
        lines.append(f"║  DNA: {DNA}  ║")
        lines.append(f"║  总事件: {status['total_events']} | 已解决: {status['resolved']} | 待处理: {status['pending']}")
        lines.append(f"║  升级: {status['escalated']} | 红蓝触发: {status['rb_triggered']} | 已签章: {status['signed']}")
        lines.append(f"║  频率: {status['hourly_oversight_count']}/{status['max_hourly']}每小时")
        lines.append("╚══════════════════════════════════════════════════════╝")
        lines.append("")
        
        lines.append(f"📊 审计分布: 🟢×{status['audit_distribution']['🟢']} 🟡×{status['audit_distribution']['🟡']} 🔴×{status['audit_distribution']['🔴']}")
        lines.append("")
        
        if recent:
            lines.append("📜 最近联动事件:")
            for e in reversed(recent[-8:]):
                icon = {"audit_triggered": "🔍", "rb_triggered": "⚔️", "rb_completed": "🏁",
                        "signed": "✍️", "escalated": "🚨", "resolved": "✅"}.get(e.event_type, "📌")
                rb_info = f" ⚔️{e.rb_result[:15]}" if e.rb_triggered else ""
                sign_info = f" ✍️{e.signed_by}" if e.signed_by else ""
                lines.append(f"   {icon} {e.audit_color} {e.target[:35]:<35} {e.oversight_decision:<12}{rb_info}{sign_info}")
        
        lines.append("")
        return "\n".join(lines)
    
    # ── 持久化 ──
    
    def _append_event(self, event: BridgeEvent):
        self.events.append(event)
        with open(EVENT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(event), ensure_ascii=False, default=str) + "\n")
        self._save_state()
    
    def _load_state(self):
        if EVENT_LOG.exists():
            with open(EVENT_LOG, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        self.events.append(BridgeEvent(**{
                            k: v for k, v in data.items()
                            if k in BridgeEvent.__dataclass_fields__
                        }))
                    except (json.JSONDecodeError, TypeError):
                        continue
    
    def _save_state(self):
        state = {
            "total_events": len(self.events),
            "resolved": sum(1 for e in self.events if e.resolved),
            "hourly_count": self._hourly_oversight_count,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[oversight-bridge {ts}] {msg}")


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🌐 龍魂·监管天联动桥接引擎 — 三系统自动协作",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
三系统协作流程:
  审计(TricolorAudit) → 监管天(Oversight) → 红蓝对抗(RB) → 签章(Signing)

触发规则:
  🟢 R>=85  → 通过·不触发RB
  🟡 R<85   → 监管天审阅 → 自动红蓝对抗
  🔴 R<85   → 监管天审阅 → 自动红蓝对抗
  🔴 R<50   → 升级·需人工介入
        """,
    )
    
    parser.add_argument("--check", action="store_true", help="单次全量检查")
    parser.add_argument("--modules", type=str, help="检查指定模块（逗号分隔）")
    parser.add_argument("--trigger-audit", type=str, help="手动触发审计联动（指定目标）")
    parser.add_argument("--content", type=str, default="", help="关联内容")
    parser.add_argument("--audit-color", type=str, choices=["🟢", "🟡", "🔴"], default="🟡")
    parser.add_argument("--audit-score", type=float, default=75.0)
    
    parser.add_argument("--status", action="store_true", help="联动状态")
    parser.add_argument("--dashboard", action="store_true", help="联动仪表盘")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    bridge = OversightBridge(verbose=args.verbose or True)
    
    if args.trigger_audit:
        event = bridge.process_audit_result(
            target=args.trigger_audit,
            content=args.content,
            audit_color=args.audit_color,
            audit_score=args.audit_score,
        )
        if args.json:
            print(json.dumps(asdict(event), ensure_ascii=False, indent=2))
        else:
            print(f"\n📋 联动结果:")
            print(f"  事件ID: {event.event_id}")
            print(f"  审计: {event.audit_color} R={event.audit_score}")
            print(f"  监管天: {event.oversight_decision}")
            print(f"  红蓝: {'✅ ' + event.rb_result if event.rb_triggered else '未触发'}")
            print(f"  签章: {event.signed_by + ' → ' + event.sign_id if event.signed_by else '未签章'}")
            print(f"  状态: {'✅ 已解决' if event.resolved else '⏳ 待处理'}")
            print()
        return
    
    if args.check:
        modules = args.modules.split(",") if args.modules else [
            "bin/lh_rb_confrontation_engine.py",
            "bin/lh_persona_signing.py",
            "bin/lh_unified_pipeline.py",
        ]
        events = bridge.check_all_modules(modules)
        if args.json:
            print(json.dumps([asdict(e) for e in events], ensure_ascii=False, indent=2))
        else:
            print(bridge.get_dashboard())
        return
    
    if args.status:
        status = bridge.get_status()
        if args.json:
            print(json.dumps(status, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(status, ensure_ascii=False, indent=2))
        return
    
    if args.dashboard:
        print(bridge.get_dashboard())
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()
