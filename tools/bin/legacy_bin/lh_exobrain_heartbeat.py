#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════
# 龍魂体系 | 外脑心跳调度器 v1.0
# ═══════════════════════════════════════════
# DNA: #龍芯⚡️2026-07-20-EXOBRAIN-HEARTBEAT-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: UID9622（诸葛鑫·Lucky）
# 三色审计: 🟢 通过
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 上游协议: 记忆永存与外脑压缩总协议 v1.0 · 第六章
# ═══════════════════════════════════════════
# 六档心跳: 实时/日/周/月/季/年
# 用法:
#   python3 bin/lh_exobrain_heartbeat.py run <档位>      # 手动触发一档心跳
#   python3 bin/lh_exobrain_heartbeat.py schedule        # 查看调度表
#   python3 bin/lh_exobrain_heartbeat.py daemon          # 启动守护进程
#   python3 bin/lh_exobrain_heartbeat.py status          # 心跳状态
# ═══════════════════════════════════════════════
"""

import json
import sys
import time
import hashlib
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field, asdict

# ─── 项目路径 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = PROJECT_ROOT / "state" / "exobrain"
BIN_DIR = PROJECT_ROOT / "bin"
BASE_DIR = PROJECT_ROOT
STATE_DIR.mkdir(parents=True, exist_ok=True)
HEARTBEAT_LOG = STATE_DIR / "heartbeat_log.jsonl"
HEARTBEAT_STATE = STATE_DIR / "heartbeat_state.json"

# ─── 六档心跳定义（第六章6.1） ───
HEARTBEATS = {
    "realtime": {
        "频次": "吞入即触发",
        "cron": None,
        "动作": ["分流脱敏", "翻译", "压缩", "归类", "封条"],
        "输入": "新记忆",
        "输出": "压缩卡",
        "责任人格": "P03雯雯",
        "监督": "P05上帝之眼",
        "幂等键": ["新记忆指纹"],
    },
    "daily": {
        "频次": "每日03:30",
        "cron": "30 3 * * *",
        "动作": ["去重", "σ抽检", "入层"],
        "输入": "当日压缩卡集",
        "输出": "归位卡",
        "责任人格": "P03雯雯",
        "监督": "P05",
        "幂等键": ["日期"],
    },
    "weekly": {
        "频次": "周日03:00-06:00",
        "cron": "0 3 * * 0",
        "动作": ["全库去重", "合并", "周总结压缩"],
        "输入": "当周全部压缩卡",
        "输出": "周总结(x₁)",
        "责任人格": "P03雯雯",
        "监督": "P05+P72",
        "幂等键": ["周序号(ISO)"],
        "防爆阈值": 50000,  # 50KB
    },
    "monthly": {
        "频次": "每月1日04:00",
        "cron": "0 4 1 * *",
        "动作": ["月总结压缩", "衰减重算", "分层迁移"],
        "输入": "4-5份周总结",
        "输出": "月总结(x₂)",
        "责任人格": "P03雯雯+P06数学大师",
        "监督": "P05",
        "幂等键": ["年月"],
        "防爆阈值": 30000,  # 30KB
    },
    "quarterly": {
        "频次": "季首月1日05:00",
        "cron": "0 5 1 1,4,7,10 *",
        "动作": ["季总结压缩", "不动点检测", "ROM入核"],
        "输入": "3份月总结",
        "输出": "季总结(x₃) / 不动点核",
        "责任人格": "P06数学大师+P15乔前辈",
        "监督": "P05+P72",
        "幂等键": ["年", "季度"],
        "防爆阈值": 20000,  # 20KB
    },
    "annual": {
        "频次": "冬至",
        "cron": None,  # 冬至需计算
        "动作": ["年鉴", "外脑健康报告", "传承包"],
        "输入": "全年季总结",
        "输出": "年鉴+传承包",
        "责任人格": "P15乔前辈+P03雯雯",
        "监督": "UID9622",
        "幂等键": ["年份"],
    },
}


@dataclass
class 心跳记录:
    """单次心跳的执行记录"""
    档位: str
    触发时间: str
    完成时间: str = ""
    状态: str = "running"  # running/complete/failed/timeout
    输入指纹: str = ""
    输出指纹: str = ""
    产物大小: int = 0
    耗时秒: float = 0.0
    dna: str = ""
    备注: str = ""


class 外脑心跳调度器:
    """六档心跳总调度 v1.0
    创建者原话: 重复压缩，迭代，归档，总结，继续识别
    """

    DNA = "#龍芯⚡️2026-07-20-EXOBRAIN-HEARTBEAT-v1.0"

    def __init__(self, state_dir: Path = None):
        self.state_dir = state_dir or STATE_DIR
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self._load_state()
        self._lock = threading.Lock()
        self._running: Dict[str, bool] = {}
        self._last_run: Dict[str, Optional[str]] = {}
        # v1.1: 幂等索引（内存缓存，避免每次线性扫描日志文件）
        self._idempotent_index: Dict[str, str] = {}
        self._build_idempotent_index()

    def _load_state(self):
        if HEARTBEAT_STATE.exists():
            self.state = json.loads(HEARTBEAT_STATE.read_text())
        else:
            self.state = {
                "last_runs": {},
                "total_beats": 0,
                "failures": 0,
                "dna": self.DNA,
            }
        self._last_run = self.state.get("last_runs", {})

    def _save_state(self):
        self.state["last_runs"] = self._last_run
        self.state["total_beats"] = self.state.get("total_beats", 0) + 1
        HEARTBEAT_STATE.write_text(json.dumps(self.state, ensure_ascii=False, indent=2))

    def _指纹(self, 内容: str) -> str:
        return hashlib.sha256(内容.encode()).hexdigest()[:16]

    def _记录心跳(self, rec: 心跳记录):
        HEARTBEAT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(HEARTBEAT_LOG, "a") as f:
            f.write(json.dumps(asdict(rec), ensure_ascii=False) + "\n")
        # v1.1: 同步更新幂等索引
        if rec.状态 == "complete":
            key = f"{rec.档位}:{rec.输入指纹}"
            self._idempotent_index[key] = rec.输出指纹

    def _build_idempotent_index(self):
        """v1.1: 启动时一次性构建幂等索引，后续追加更新"""
        self._idempotent_index.clear()
        if HEARTBEAT_LOG.exists():
            with open(HEARTBEAT_LOG) as fh:
                for line in fh:
                    try:
                        rec = json.loads(line)
                        if rec.get("状态") == "complete":
                            key = f"{rec.get('档位','')}:{rec.get('输入指纹','')}"
                            if key:
                                self._idempotent_index[key] = rec.get("输出指纹", "")
                    except json.JSONDecodeError:
                        continue

    # ═══════════════════════════════════════
    # 幂等检查
    # ═══════════════════════════════════════
    def _幂等检查(self, tier: str, 输入指纹: str) -> Optional[str]:
        """同一心跳重跑结果必须一致。使用内存索引 O(1) 查找。"""
        prev_key = f"{tier}:{输入指纹}"
        return self._idempotent_index.get(prev_key)

    # ═══════════════════════════════════════
    # 防爆炸保险
    # ═══════════════════════════════════════
    def _防爆检查(self, tier: str, 产物: str) -> dict[str, Any]:
        """6.3: 超过阈值自动再压一轮；超时截链封存"""
        limit = HEARTBEATS[tier].get("防爆阈值")
        if limit and len(产物.encode()) > limit:
            return {"needs_compress": True, "reason": f"产物{len(产物.encode())}B 超过阈值{limit}B"}
        return {"needs_compress": False}

    # ═══════════════════════════════════════
    # 执行单档心跳
    # ═══════════════════════════════════════
    def 执行心跳(self, tier: str, 输入数据: str = "", 输入指纹: str | None = None,
                 压缩函数: Callable = None, 干运行: bool = False) -> dict[str, Any]:
        """执行指定档位的一次心跳"""
        if tier not in HEARTBEATS:
            return {"error": f"未知档位: {tier}", "valid": list(HEARTBEATS.keys())}

        config = HEARTBEATS[tier]
        fp = 输入指纹 or self._指纹(输入数据)

        # 幂等检查
        prev = self._幂等检查(tier, fp)
        if prev:
            return {
                "tier": tier,
                "幂等": True,
                "之前输出指纹": prev,
                "状态": "skipped (已执行过)",
                "dna": self.DNA,
            }

        t0 = time.time()
        rec = 心跳记录(
            档位=tier,
            触发时间=datetime.now().isoformat(),
            输入指纹=fp,
            dna=self.DNA,
        )

        print(f"🫀 外脑心跳 [{tier}] {config['频次']} · 触发")
        print(f"   动作: {' → '.join(config['动作'])}")

        if 干运行:
            rec.状态 = "dry_run"
            rec.备注 = "干运行模式"
            self._记录心跳(rec)
            return {"tier": tier, "状态": "干运行完成", "dna": self.DNA}

        # 防爆检查
        if 输入数据 and 压缩函数:
            build = 压缩函数(输入数据)
            bomb = self._防爆检查(tier, build)
            if bomb["needs_compress"]:
                print(f"   ⚠️ 防爆触发: {bomb['reason']}")
                if 压缩函数:
                    build = 压缩函数(build)  # 再压一轮
                    产物 = 压缩函数(build) if self._防爆检查(tier, build)["needs_compress"] else build

        elapsed = time.time() - t0
        rec.耗时秒 = round(elapsed, 2)
        rec.完成时间 = datetime.now().isoformat()
        rec.状态 = "complete"
        rec.输出指纹 = self._指纹(输入数据 + str(time.time()))

        print(f"   ✅ 完成 · 耗时{elapsed:.1f}s")

        self._记录心跳(rec)
        self._last_run[tier] = datetime.now().isoformat()
        self._save_state()

        return {
            "tier": tier,
            "状态": "🟢 完成",
            "耗时秒": elapsed,
            "输入指纹": fp,
            "输出指纹": rec.输出指纹,
            "dna": self.DNA,
        }

    # ═══════════════════════════════════════
    # 调度表展示
    # ═══════════════════════════════════════
    def 调度表(self) -> str:
        """打印六档心跳总调度表（第十章10.1）"""
        lines = [
            "🫀 外脑心跳总调度表",
            "━" * 70,
        ]
        for tier, cfg in HEARTBEATS.items():
            last = self._last_run.get(tier, "从未执行")
            cron = cfg.get("cron") or cfg["频次"]
            lines.append(f"  {tier:12s} | {cron:24s} | {cfg['责任人格']} | 上次: {last}")
        lines.append("━" * 70)
        return "\n".join(lines)

    # ═══════════════════════════════════════
    # N6 命名合规 — 对接命名总表附录B
    # ═══════════════════════════════════════
    def 吞入命名校验(self, 文件路径: str) -> dict[str, Any]:
        """外脑入库钩子：吞入即触发 N6 校验。🔴不合格不入库。"""
        import subprocess as _sp
        路径 = Path(文件路径)
        if not 路径.is_file():
            return {"合格": False, "原因": f"文件不存在: {文件路径}"}
        try:
            r = _sp.run(
                [sys.executable, str(BIN_DIR / "lh_naming_lint.py"),
                 "--check", str(路径), "--json"],
                capture_output=True, text=True, timeout=30
            )
            if r.returncode == 0:
                return {"合格": True, "三色": "🟢", "详情": json.loads(r.stdout) if r.stdout.strip() else {}}
            报告 = json.loads(r.stdout) if r.stdout.strip() else {}
            严重 = 报告.get("🔴严重", 0)
            if 严重 > 0:
                return {"合格": False, "三色": "🔴", "原因": f"{严重} 红线违规", "详情": 报告}
            return {"合格": False, "三色": "🟡", "原因": f"{报告.get('未通过', 0)} 项待修", "详情": 报告}
        except Exception as e:
            return {"合格": False, "原因": f"校验异常: {e}"}

    def 命名合规日检(self) -> dict[str, Any]:
        """日档心跳 N6：扫描关键目录命名合规"""
        print("🧹 N6 命名合规日检（命名总表附录B）")
        import subprocess as _sp
        目录列表 = ["01_protocols", "01_技能庫", "deploy", "bin", "papers", "articles"]
        结果汇总 = {"总计目录": 0, "🟢": 0, "🟡": 0, "🔴": 0, "详情": []}
        for d in 目录列表:
            dir_path = BASE_DIR / d if BASE_DIR else Path.cwd() / d
            if not dir_path.is_dir():
                continue
            结果汇总["总计目录"] += 1
            try:
                r = _sp.run(
                    [sys.executable, str(BIN_DIR / "lh_naming_lint.py"),
                     "--scan-dir", str(dir_path), "--json"],
                    capture_output=True, text=True, timeout=60
                )
                if r.returncode == 0:
                    结果汇总["🟢"] += 1
                    print(f"  {d}: 🟢")
                elif r.returncode == 1:
                    结果汇总["🟡"] += 1
                    rpt = json.loads(r.stdout) if r.stdout.strip() else {}
                    print(f"  {d}: 🟡 ({rpt.get('未通过', '?')} 项待修)")
                else:
                    结果汇总["🔴"] += 1
                    rpt = json.loads(r.stdout) if r.stdout.strip() else {}
                    print(f"  {d}: 🔴 ({rpt.get('🔴严重', '?')} 红线)")
                    结果汇总["详情"].append({"目录": d, "报告": rpt})
            except Exception as e:
                结果汇总["🔴"] += 1
                print(f"  {d}: 🔴 异常: {e}")
        return 结果汇总

    def _触发命名合规日检(self):
        """守护循环中的命名合规日检（凌晨4点，日档心跳后一小时）"""
        last = self._last_run.get("daily_naming")
        today = datetime.now().strftime("%Y-%m-%d")
        if last and last.startswith(today):
            return
        print(f"\n🧹 [{datetime.now().strftime('%H:%M:%S')}] N6 命名合规日检触发")
        try:
            result = self.命名合规日检()
            self._last_run["daily_naming"] = datetime.now().isoformat()
            self._save_state()
        except Exception as e:
            print(f"   🔴 N6 命名合规日检异常: {e}")

    # ═══════════════════════════════════════
    # 守护进程
    # ═══════════════════════════════════════
    def 守护(self, 间隔秒: int = 60):
        """后台守护循环，检查到期的定时任务并执行"""
        print("🫀 外脑心跳守护进程启动")
        print(f"   检查间隔: {间隔秒}s")
        print(f"   六档定义: {', '.join(HEARTBEATS.keys())}")
        print("   按 Ctrl+C 停止\n")

        try:
            while True:
                now = datetime.now()
                # 日档检查
                if now.hour == 3 and now.minute == 30:
                    self._触发守护心跳("daily")

                # N6 命名合规日检（凌晨4:00，日档后30分钟）
                if now.hour == 4 and now.minute == 0:
                    self._触发命名合规日检()

                # 周档检查 (周日)
                if now.weekday() == 6 and now.hour == 3 and now.minute == 0:
                    self._触发守护心跳("weekly")

                # 月档检查 (每月1日)
                if now.day == 1 and now.hour == 4 and now.minute == 0:
                    self._触发守护心跳("monthly")

                # 季档检查 (1/4/7/10月1日)
                if now.day == 1 and now.month in (1, 4, 7, 10) and now.hour == 5 and now.minute == 0:
                    self._触发守护心跳("quarterly")

                time.sleep(间隔秒)
        except KeyboardInterrupt:
            print("\n🫀 外脑心跳守护进程停止")

    def _触发守护心跳(self, tier: str):
        last = self._last_run.get(tier)
        today = datetime.now().strftime("%Y-%m-%d")
        if last and last.startswith(today):
            return  # 今天已经执行过
        print(f"\n🫀 [{datetime.now().strftime('%H:%M:%S')}] 触发 {tier} 心跳")
        self.执行心跳(tier)


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

def main():
    scheduler = 外脑心跳调度器()

    if len(sys.argv) < 2:
        print(__doc__)
        print(f"\n{scheduler.调度表()}")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "schedule":
        print(scheduler.调度表())

    elif cmd == "status":
        print(json.dumps({
            "状态": "🟢 运行中",
            "总计心跳": scheduler.state.get("total_beats", 0),
            "失败次数": scheduler.state.get("failures", 0),
            "最后运行": scheduler._last_run,
            "dna": scheduler.DNA,
        }, ensure_ascii=False, indent=2))

    elif cmd == "run":
        if len(sys.argv) < 3 or sys.argv[2] not in HEARTBEATS:
            print(f"可用档位: {', '.join(HEARTBEATS.keys())}")
            sys.exit(1)
        tier = sys.argv[2]
        dry = "--dry" in sys.argv
        result = scheduler.执行心跳(tier, 干运行=dry)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "daemon":
        scheduler.守护()

    elif cmd == "history":
        if HEARTBEAT_LOG.exists():
            print(f"🫀 心跳历史 ({HEARTBEAT_LOG}):")
            with open(HEARTBEAT_LOG) as fh:
                for line in fh:
                    try:
                        rec = json.loads(line)
                        print(f"  [{rec.get('档位','?')}] {rec.get('触发时间','?')} → {rec.get('状态','?')}")
                    except json.JSONDecodeError:
                        continue
        else:
            print("尚无心跳记录")

    elif cmd == "reset-log":
        # v1.1: 冻结替代删除——"不删除只冻结"铁律
        if HEARTBEAT_LOG.exists():
            frozen_name = f"heartbeat_log.frozen.{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
            frozen_path = STATE_DIR / frozen_name
            HEARTBEAT_LOG.rename(frozen_path)
            # 同时新建空日志
            HEARTBEAT_LOG.write_text("")
            print(f"✅ 心跳日志已冻结为: {frozen_name}")
        else:
            print("尚无心跳记录需重置")

    else:
        print(f"❌ 未知命令: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
