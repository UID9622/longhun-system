#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  龍魂·联动桥 lh_tuner_bridge v1.0                            ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F               ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ║
║  责任: UID9622·不免责                                        ║
╚══════════════════════════════════════════════════════════════╝

架构：事件总线 + 注册表 + 适配器（四适配器内嵌单文件·避免碎片）
  ① 调节器只发事件·不直接 import 引擎（解耦·铁律接口 hook 注入原则）
  ② 桥与适配器全部 fail-isolated：任何异常只记状态·绝不抛回调节器
  ③ DNA 一律走 bin/lh_dna_generator.py·禁止手写干支（缺席用占位）
  ④ 零第三方依赖（纯标准库）
  ⑤ emit 超时用 ThreadPoolExecutor future.result(timeout)·超时记 🔴 不抛异常

事件契约（SPEC §二·焊死）：
  TUNE_SIMULATED 模拟微调完成 | TUNE_APPLIED 落盘微调完成
  TUNE_MELTDOWN  红线熔断     | TUNE_ROLLBACK 回滚完成
  TUNE_AUDIT     审计报告生成
"""

import json
import hashlib
import os
import sys
import subprocess
import importlib.util
from concurrent.futures import ThreadPoolExecutor, TimeoutError as 未来超时
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# ═══════════════════════════════════════════════════════════════
# 〇、常量 · 事件类型 + 默认注册表（SPEC §二/§三·焊死）
# ═══════════════════════════════════════════════════════════════

TUNE_SIMULATED = "TUNE_SIMULATED"   # 模拟微调完成
TUNE_APPLIED   = "TUNE_APPLIED"     # 落盘微调完成
TUNE_MELTDOWN  = "TUNE_MELTDOWN"    # 红线熔断（dr∈{3,9}）
TUNE_ROLLBACK  = "TUNE_ROLLBACK"    # 回滚完成
TUNE_AUDIT     = "TUNE_AUDIT"       # 审计报告生成

默认注册表: dict = {
    "版本": "1.0",
    "引擎": {
        "rules_engine": {"开关": True, "超时秒": 5,
                         "快照路径": "~/.龍魂/引擎態/rules_engine_params.json"},
        "audit":        {"开关": True, "超时秒": 10,
                         "审计模块路径": "skills/longhun-audit-integrated/longhun_audit_integrated.py",
                         "仓库根": ""},
        "caolog":       {"开关": True, "超时秒": 3,
                         "草日誌目录": "~/.龍魂/草日誌"},
        "dna_registry": {"开关": True, "超时秒": 3,
                         "登记册": "~/.龍魂/DNA登記冊.jsonl"},
    },
}

# 事件载荷 schema 默认（SPEC §二·缺失键补默认）
默认数据摘要: dict = {"甩锅率": 0.0, "自扛率": 0.0, "没立正率": 0.0,
                     "威胁率": 0.0, "补救率": 0.0, "惯犯率": 0.0}


def _现在毫秒() -> str:
    """ISO8601 毫秒时间戳"""
    return datetime.now().isoformat(timespec="milliseconds")


def _生成DNA(动作标签: str, 版本: str = "1.0") -> str:
    """
    DNA 一律以本地生成器为准·禁止手写伪造（SPEC 铁律③）。
    依次在 桥所在目录../bin/ 与 ~/.龍魂/bin/ 查找 lh_dna_generator.py，
    生成器 CLI 首行为 DNA 本体；任何失败 → 返回待校正占位 DNA（SPEC 允许占位）。
    """
    候选路径 = [
        Path(__file__).resolve().parent.parent / "bin" / "lh_dna_generator.py",
        Path(os.path.expanduser("~/.龍魂/bin/lh_dna_generator.py")),
    ]
    for 路径 in 候选路径:
        if not 路径.is_file():
            continue
        try:
            结果 = subprocess.run(
                [sys.executable, str(路径), 动作标签, 版本],
                capture_output=True, text=True, timeout=5,
            )
            if 结果.returncode == 0 and 结果.stdout.strip():
                首行 = 结果.stdout.strip().splitlines()[0].strip()
                if 首行.startswith("#龍芯⚡️"):
                    return 首行
        except Exception:
            # ── 超时/执行异常 → 尝试下一个候选 ──
            continue
    return f"#龍芯⚡️待生成器校正-{动作标签}-{版本}"

# ═══════════════════════════════════════════════════════════════
# 一、适配器基类（SPEC §四·方法签名焊死）
# ═══════════════════════════════════════════════════════════════

class 适配器基类:
    """全部适配器 fail-isolated：receive 自身吞异常·只回状态 dict"""

    名称: str = "base"

    def __init__(self, 配置: dict):
        self.配置: dict = 配置 or {}

    def receive(self, 事件: dict) -> dict:
        """返回 {"状态":"🟢|🟡|🔴","说明":str}·子类实现并自吞异常"""
        raise NotImplementedError

    # ── 状态简写 ──
    def _通过(self, 说明: str) -> dict:
        return {"状态": "🟢", "说明": 说明}

    def _跳过(self, 说明: str) -> dict:
        return {"状态": "🟡", "说明": 说明}

    def _失败(self, 说明: str) -> dict:
        return {"状态": "🔴", "说明": 说明}

# ═══════════════════════════════════════════════════════════════
# 二、适配器 A · RulesEngineAdapter（规则引擎联动）
# ═══════════════════════════════════════════════════════════════

class RulesEngineAdapter(适配器基类):
    """
    TUNE_APPLIED  → 从 ~/.龍魂/微調參數.json 现读参数·写快照供规则引擎消费
    TUNE_MELTDOWN → 快照同目录写 rules_engine.LOCK.json（从严模式信号）
    TUNE_ROLLBACK → 若 LOCK 存在则写 {"锁定":false,...} 解除
    """

    名称 = "rules_engine"

    _快照参数字段 = ("自扛加分", "逃避扣分", "没立正扣分",
                     "补救加分", "惯犯扣分", "惯犯触发次数")

    def _快照路径(self) -> Path:
        return Path(os.path.expanduser(
            self.配置.get("快照路径", "~/.龍魂/引擎態/rules_engine_params.json")))

    def _锁路径(self) -> Path:
        return self._快照路径().parent / "rules_engine.LOCK.json"

    def receive(self, 事件: dict) -> dict:
        try:
            类型 = 事件.get("事件", "")
            if 类型 == TUNE_APPLIED:
                return self._写快照(事件)
            if 类型 == TUNE_MELTDOWN:
                return self._写锁(事件)
            if 类型 == TUNE_ROLLBACK:
                return self._解锁(事件)
            return self._跳过(f"事件 {类型 or '?'} 不消费·跳过")
        except Exception as e:
            return self._失败(f"异常已隔离: {e}")

    def _写快照(self, 事件: dict) -> dict:
        # 快照须从参数文件现读·不从事件载荷猜（SPEC §四-A）
        参数路径 = Path(os.path.expanduser("~/.龍魂/微調參數.json"))
        if not 参数路径.is_file():
            return self._失败(f"参数文件缺席: {参数路径}")
        with open(参数路径, "r", encoding="utf-8") as f:
            全量 = json.load(f)
        快照 = {
            "更新时间": _现在毫秒(),
            "参数哈希": 事件.get("参数哈希", ""),
            "父哈希": 事件.get("父哈希", ""),
            "三色": 事件.get("三色", "🟡"),
            "dr": 事件.get("dr", 6),
            "参数": {k: 全量.get(k) for k in self._快照参数字段},
        }
        路径 = self._快照路径()
        路径.parent.mkdir(parents=True, exist_ok=True)
        with open(路径, "w", encoding="utf-8") as f:
            json.dump(快照, f, ensure_ascii=False, indent=2)
        return self._通过(f"参数快照已写: {路径}")

    def _写锁(self, 事件: dict) -> dict:
        锁 = {
            "锁定": True,
            "原因": 事件.get("原因", "红线熔断·规则引擎从严模式"),
            "dr": 事件.get("dr", 9),
            "时间戳": _现在毫秒(),
        }
        路径 = self._锁路径()
        路径.parent.mkdir(parents=True, exist_ok=True)
        with open(路径, "w", encoding="utf-8") as f:
            json.dump(锁, f, ensure_ascii=False, indent=2)
        return self._通过(f"从严 LOCK 已写: {路径}")

    def _解锁(self, 事件: dict) -> dict:
        路径 = self._锁路径()
        if not 路径.is_file():
            return self._跳过("无 LOCK·无需解除")
        锁 = {
            "锁定": False,
            "原因": 事件.get("原因", "回滚完成·解除从严模式"),
            "dr": 事件.get("dr", 7),
            "时间戳": _现在毫秒(),
        }
        with open(路径, "w", encoding="utf-8") as f:
            json.dump(锁, f, ensure_ascii=False, indent=2)
        return self._通过(f"LOCK 已解除: {路径}")

# ═══════════════════════════════════════════════════════════════
# 三、适配器 B · AuditAdapter（三色审计联动）
# ═══════════════════════════════════════════════════════════════

class AuditAdapter(适配器基类):
    """
    仅收 TUNE_APPLIED / TUNE_ROLLBACK。
    懒加载 审计模块（仓库根 + 相对路径）·调 audit_script 取 color·
    与调节器 dr 交叉验证写 audit_crosscheck.json。
    模块缺席/异常 → 🟡 跳过·绝不失败。
    """

    名称 = "audit"

    def receive(self, 事件: dict) -> dict:
        try:
            类型 = 事件.get("事件", "")
            if 类型 not in (TUNE_APPLIED, TUNE_ROLLBACK):
                return self._跳过(f"事件 {类型 or '?'} 不消费·跳过")
            仓库根 = self.配置.get("仓库根", "")
            if not 仓库根:
                return self._跳过("仓库根未配置·跳过审计交叉验证")
            模块路径 = Path(os.path.expanduser(仓库根)) / self.配置.get(
                "审计模块路径", "skills/longhun-audit-integrated/longhun_audit_integrated.py")
            if not 模块路径.is_file():
                return self._跳过(f"审计模块缺席: {模块路径}")
            try:
                spec = importlib.util.spec_from_file_location(
                    "longhun_audit_integrated", 模块路径)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                参数JSON路径 = os.path.expanduser("~/.龍魂/微調參數.json")
                报告 = mod.LonghunIntegratedAudit().audit_script(参数JSON路径)
                审计color = 报告.get("color", "")
            except Exception as e:
                return self._跳过(f"审计模块调用失败·跳过: {e}")
            # ── 交叉验证：调节器 dr ↔ 审计 color ──
            dr = 事件.get("dr", 7)
            调节器色 = "🔴" if dr in (3, 9) else ("🟡" if dr == 6 else "🟢")
            交叉 = {
                "调节器dr": dr,
                "审计color": 审计color,
                "一致": (审计color == 调节器色),
                "时间戳": _现在毫秒(),
            }
            路径 = Path(os.path.expanduser("~/.龍魂/引擎態/audit_crosscheck.json"))
            路径.parent.mkdir(parents=True, exist_ok=True)
            with open(路径, "w", encoding="utf-8") as f:
                json.dump(交叉, f, ensure_ascii=False, indent=2)
            return self._通过(
                f"交叉验证已写: {路径}·dr={dr}↔{审计color}·一致={交叉['一致']}")
        except Exception as e:
            return self._失败(f"异常已隔离: {e}")

# ═══════════════════════════════════════════════════════════════
# 四、适配器 C · CaoLogAdapter（草日志联动·对齐 LocalLogger 格式）
# ═══════════════════════════════════════════════════════════════

class CaoLogAdapter(适配器基类):
    """
    收全部 5 类事件 → 草日誌目录/YYYY-MM-DD.log（JSONL 追加）。
    文件名与 LocalLogger 一致（YYYY-MM-DD.log）·无需 import 该引擎。
    """

    名称 = "caolog"

    def receive(self, 事件: dict) -> dict:
        try:
            类型 = 事件.get("事件", "")
            目录 = Path(os.path.expanduser(
                self.配置.get("草日誌目录", "~/.龍魂/草日誌")))
            目录.mkdir(parents=True, exist_ok=True)
            路径 = 目录 / f"{datetime.now().strftime('%Y-%m-%d')}.log"
            调整记录 = 事件.get("调整记录") or []
            记录 = {
                "时间戳": 事件.get("时间戳", _现在毫秒()),
                "类型": f"tuner.{类型.lower()}",
                "系统": "自适应调节器v2.0",
                "DNA": 事件.get("DNA", ""),
                "三色": 事件.get("三色", "🟡"),
                "dr": 事件.get("dr", 6),
                "参数哈希": 事件.get("参数哈希", ""),
                "父哈希": 事件.get("父哈希", ""),
                "摘要": 调整记录[0] if 调整记录 else 事件.get("状态", 类型),
            }
            with open(路径, "a", encoding="utf-8") as f:
                f.write(json.dumps(记录, ensure_ascii=False) + "\n")
            return self._通过(f"草日志已记: {路径.name}·{记录['类型']}")
        except Exception as e:
            return self._失败(f"异常已隔离: {e}")

# ═══════════════════════════════════════════════════════════════
# 五、适配器 D · DNARegistryAdapter（DNA 登记联动·§14 条款）
# ═══════════════════════════════════════════════════════════════

class DNARegistryAdapter(适配器基类):
    """
    收 TUNE_APPLIED / TUNE_ROLLBACK / TUNE_MELTDOWN →
    登记册 JSONL 追加·链式存根 = sha256(父哈希+参数哈希+DNA)[:16]·可复算。
    """

    名称 = "dna_registry"

    条款 = "§14 自适应调节器哈希链"

    def receive(self, 事件: dict) -> dict:
        try:
            类型 = 事件.get("事件", "")
            if 类型 not in (TUNE_APPLIED, TUNE_ROLLBACK, TUNE_MELTDOWN):
                return self._跳过(f"事件 {类型 or '?'} 不消费·跳过")
            父哈希 = 事件.get("父哈希", "")
            参数哈希 = 事件.get("参数哈希", "")
            DNA = 事件.get("DNA", "")
            链式存根 = hashlib.sha256(
                (父哈希 + 参数哈希 + DNA).encode("utf-8")).hexdigest()[:16]
            登记 = {
                "登记时间": _现在毫秒(),
                "DNA": DNA,
                "事件": 类型,
                "参数哈希": 参数哈希,
                "父哈希": 父哈希,
                "链式存根": 链式存根,
                "条款": self.条款,
            }
            路径 = Path(os.path.expanduser(
                self.配置.get("登记册", "~/.龍魂/DNA登記冊.jsonl")))
            路径.parent.mkdir(parents=True, exist_ok=True)
            with open(路径, "a", encoding="utf-8") as f:
                f.write(json.dumps(登记, ensure_ascii=False) + "\n")
            return self._通过(f"§14 登记完成: {路径.name}·存根 {链式存根}")
        except Exception as e:
            return self._失败(f"异常已隔离: {e}")

# ═══════════════════════════════════════════════════════════════
# 六、桥本体 · 事件总线 + 注册表加载 + 适配器调度（SPEC §五·焊死）
# ═══════════════════════════════════════════════════════════════

class 联动桥:
    """
    emit：补齐事件契约字段 → 逐适配器分发
      （signal.alarm 不可用·用 ThreadPoolExecutor + future.result(timeout) 实现超时）
    返回各适配器结果 [{"适配器","状态","说明"}]·永不抛异常
    """

    适配器类表: Dict[str, type] = {
        "rules_engine": RulesEngineAdapter,
        "audit": AuditAdapter,
        "caolog": CaoLogAdapter,
        "dna_registry": DNARegistryAdapter,
    }

    def __init__(self, 注册表路径: str = "~/.龍魂/聯動註冊表.json"):
        self.注册表路径 = Path(os.path.expanduser(注册表路径))
        self.注册表: dict = self._加载注册表()
        # ── 按注册表实例化适配器（配置原样注入·开关/超时留在调度层判定） ──
        self.适配器: List[适配器基类] = []
        引擎配置 = self.注册表.get("引擎", {})
        for 键, 类 in self.适配器类表.items():
            self.适配器.append(类(引擎配置.get(键, {})))

    # ── 注册表（SPEC §三：缺席 → 自动写默认值再使用） ──

    def _加载注册表(self) -> dict:
        if not self.注册表路径.is_file():
            注册表 = deepcopy(默认注册表)
            try:
                self.注册表路径.parent.mkdir(parents=True, exist_ok=True)
                with open(self.注册表路径, "w", encoding="utf-8") as f:
                    json.dump(注册表, f, ensure_ascii=False, indent=2)
            except Exception:
                # ── 写不进也用默认·fail-isolated ──
                pass
            return 注册表
        try:
            with open(self.注册表路径, "r", encoding="utf-8") as f:
                注册表 = json.load(f)
            if not isinstance(注册表, dict) or "引擎" not in 注册表:
                raise ValueError("注册表结构缺 引擎 段")
            return 注册表
        except Exception:
            # ── 损坏 → 回退默认·不抛 ──
            return deepcopy(默认注册表)

    # ── 事件组装（SPEC §二·缺失键补默认） ──

    def _组装事件(self, 事件类型: str, 载荷: dict) -> dict:
        事件 = dict(载荷 or {})
        事件["事件"] = 事件类型
        事件.setdefault("时间戳", _现在毫秒())
        if not 事件.get("DNA"):
            事件["DNA"] = _生成DNA(f"TUNE-{事件类型.replace('TUNE_', '')}")
        事件.setdefault("三色", "🟡")
        事件.setdefault("dr", 6)
        事件.setdefault("参数哈希", "")
        事件.setdefault("父哈希", "")
        事件.setdefault("调整数", 0)
        事件.setdefault("调整记录", [])
        事件.setdefault("数据摘要", dict(默认数据摘要))
        事件.setdefault("趋势", {})
        事件["来源"] = "自适应调节器v2.0"
        return 事件

    # ── 发射（永不抛异常） ──

    def emit(self, 事件类型: str, 载荷: dict) -> List[dict]:
        结果: List[dict] = []
        try:
            事件 = self._组装事件(事件类型, 载荷)
        except Exception as e:
            # ── 组装都失败也用最小事件继续分发·fail-isolated ──
            事件 = {"事件": 事件类型, "时间戳": _现在毫秒(),
                    "DNA": "", "三色": "🟡", "dr": 6,
                    "参数哈希": "", "父哈希": "", "调整数": 0,
                    "调整记录": [], "数据摘要": dict(默认数据摘要),
                    "趋势": {}, "来源": "自适应调节器v2.0",
                    "组装异常": str(e)}
        引擎配置 = self.注册表.get("引擎", {})
        执行器 = ThreadPoolExecutor(max_workers=max(1, len(self.适配器)))
        try:
            待发: List[tuple] = []
            for 适配器 in self.适配器:
                配置 = 引擎配置.get(适配器.名称, {})
                if not 配置.get("开关", True):
                    结果.append({"适配器": 适配器.名称, "状态": "🟡",
                                 "说明": "注册表开关关闭·未分发"})
                    continue
                超时秒 = float(配置.get("超时秒", 5))
                待发.append((适配器, 执行器.submit(适配器.receive, 事件), 超时秒))
            for 适配器, 未来, 超时秒 in 待发:
                try:
                    回执 = 未来.result(timeout=超时秒)
                    结果.append({
                        "适配器": 适配器.名称,
                        "状态": 回执.get("状态", "🟡"),
                        "说明": 回执.get("说明", ""),
                    })
                except 未来超时:
                    # ── 超时记 🔴·不抛异常 ──
                    结果.append({"适配器": 适配器.名称, "状态": "🔴",
                                 "说明": f"超时（>{超时秒:g}s)·已隔离"})
                except Exception as e:
                    结果.append({"适配器": 适配器.名称, "状态": "🔴",
                                 "说明": f"异常已隔离: {e}"})
        except Exception as e:
            结果.append({"适配器": "桥本体", "状态": "🔴",
                         "说明": f"调度异常已隔离: {e}"})
        finally:
            # ── wait=False：卡死的适配器线程不得拖住调节器主流程 ──
            执行器.shutdown(wait=False)
        return 结果

    # ── 自检（SPEC §五：每适配器发 TUNE_AUDIT 测试事件·返回结果表） ──

    def 自检(self) -> List[dict]:
        return self.emit(TUNE_AUDIT, {"状态": "🟢 联动桥自检测试事件"})

# ═══════════════════════════════════════════════════════════════
# 七、模块级单例 · 取桥()（SPEC §五·焊死）
# ═══════════════════════════════════════════════════════════════

_单例桥: "联动桥 | None" = None


def 取桥() -> 联动桥:
    """模块级单例·供调节器 hook 调用"""
    global _单例桥
    if _单例桥 is None:
        _单例桥 = 联动桥()
    return _单例桥
