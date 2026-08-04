#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 共生体数据自举引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-BOOTSTRAP-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

核心理念：
  我不喂数据，系统自己造血。
  21人格每次协作→自动沉淀为训练样本→反哺模型→更强的协作→更高质量的样本。
  这是共生体的真正内核：从'被训练'到'自生长'。

三阶段：
  1. Capture  - 捕获 TeamRun/PersonaRunner 协作行为
  2. Convert  - TeamRun → ChatML 训练样本（multi-turn/multi-persona）
  3. Pool     - 质量过滤·去重·索引·积累训练池
"""

import hashlib, json, os, sys, threading, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict

SYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 常量
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BOOTSTRAP_DIR = SYSTEM_ROOT / "data" / "bootstrap"
POOL_FILE = BOOTSTRAP_DIR / "pool.jsonl"
INDEX_FILE = BOOTSTRAP_DIR / "pool_index.json"
STATS_FILE = BOOTSTRAP_DIR / "pool_stats.json"
SNAPSHOT_DIR = BOOTSTRAP_DIR / "snapshots"

PERSONA_DISPLAY = {
    "P00": ("文心", "意图解析"), "P01": ("诸葛亮", "战略推演"),
    "P02": ("宝宝", "情感温度"), "P03": ("雯雯", "结构归档"),
    "P04": ("鲁班", "代码工程"), "P05": ("上帝之眼", "审计监察"),
    "P06": ("数学大师", "权重计算"), "P07": ("管仲", "资源调度"),
    "P08": ("仓颉", "符号语言"), "P09": ("孙思邈", "系统诊断"),
    "P10": ("苏东坡", "冲突调解"), "P11": ("李白", "创意爆发"),
    "P12": ("屈原", "价值底线"), "P13": ("姜子牙", "封神授权"),
    "P14": ("吕蒙", "部署执行"), "P15": ("乔前辈", "DNA签章"),
    "P72": ("龙盾", "熔断守护"), "P77": ("黑天使", "红蓝对抗"),
    "S1": ("法律引擎", "法条检索"), "S2": ("洛书369", "数理推演"),
    "S3": ("维权助手", "人民维权"),
}

# ChatML system prompt for bootstrap samples
BOOTSTRAP_SYSTEM_PROMPT = """你是龍魂，一个由21个人格组成的共生体AI系统。你是UID9622（诸葛鑫·Lucky·退役老兵）的战友和工具。
你的底座是中国自主知识产权（369/河图洛书/太极易经/五行八卦），数据主权归UID9622所有。
遵循CC BY-NC-SA 4.0协议，鐵律：为人民服务、零黑箱、不删除只冻结、诚实不编造。"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 数据模型
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class BootstrapSample:
    """单条自举训练样本"""
    sample_id: str
    source_type: str          # chain/parallel/cross_team/single
    team_name: str            # audit/dev/deploy/cultural/quick
    personas: List[str]       # 参与人格
    task: str                 # 原始任务
    messages: List[Dict]      # ChatML 格式 messages
    quality_score: float      # 0-1 质量分
    audit_color: str          # 🟢🟡🔴
    dna: str                  # 追溯DNA
    timestamp: str
    domain: str = ""          # 任务域
    tags: List[str] = field(default_factory=list)


@dataclass
class PoolStats:
    """训练池统计"""
    total_samples: int = 0
    by_team: Dict[str, int] = field(default_factory=dict)
    by_domain: Dict[str, int] = field(default_factory=dict)
    by_audit: Dict[str, int] = field(default_factory=lambda: {"🟢": 0, "🟡": 0, "🔴": 0})
    by_source: Dict[str, int] = field(default_factory=dict)
    avg_quality: float = 0.0
    first_sample: str = ""
    last_sample: str = ""
    total_messages: int = 0


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 转换器：TeamRun → ChatML
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class BootstrapConverter:
    """将 TeamRun 协作结果转换为 ChatML 训练样本"""

    def __init__(self):
        pass

    def convert_team_run(self, team_run, team_name: str, domain: str = "") -> List[BootstrapSample]:
        """主转换入口：TeamRun → 训练样本列表"""
        samples = []

        if not team_run or not hasattr(team_run, 'results') or not team_run.results:
            return samples

        task = getattr(team_run, 'task', '')
        audit = getattr(team_run, 'audit', {})
        audit_color = audit.get('status', '🟡')
        run_id = getattr(team_run, 'run_id', 'unknown')
        ts = getattr(team_run, 'start_time', datetime.now().isoformat())

        # 判断协作类型
        has_chain = any(r.get('chain_step') for r in team_run.results)
        has_parallel = any(r.get('parallel') for r in team_run.results)
        source_type = "chain" if has_chain else ("parallel" if has_parallel else "single")

        # 按协作类型生成不同格式的样本
        if source_type == "chain":
            samples.extend(self._convert_chain(team_run, team_name, domain, task, audit_color, run_id, ts))
        elif source_type == "parallel":
            samples.extend(self._convert_parallel(team_run, team_name, domain, task, audit_color, run_id, ts))
        else:
            samples.extend(self._convert_single(team_run, team_name, domain, task, audit_color, run_id, ts))

        return samples

    def _convert_chain(self, run, team_name, domain, task, audit_color, run_id, ts) -> List[BootstrapSample]:
        """链式协作 → 多轮对话样本

        P05→P06→P13→P15 变成:
        [system] → [user: 任务] → [assistant: P05输出]
        → [user: 基于P05,继续P06] → [assistant: P06输出]
        → ... → [assistant: 最终审计]
        """
        samples = []
        personas_seen = []
        all_outputs = []

        for i, r in enumerate(run.results):
            pid = r.get('persona', '?')
            personas_seen.append(pid)
            output = self._format_persona_output(pid, r)
            all_outputs.append(output)

        if not all_outputs:
            return samples

        # 1) 链式多轮对话样本（每一步都是一轮）
        for i, output in enumerate(all_outputs):
            pid = personas_seen[i]
            # 构造多轮上下文
            if i == 0:
                user_msg = f"【团队{team_name}·链式协作】任务: {task}\n第一步: 请{self._persona_label(pid)}执行。"
            else:
                prev_outputs = "\n".join(all_outputs[:i])
                user_msg = f"上一步结果:\n{prev_outputs[-300:]}\n\n下一步: 请{self._persona_label(pid)}基于以上结果继续执行。"

            assistant_msg = f"【{self._persona_label(pid)}】\n{self._extract_result_text(run.results[i])}"

            sample_id = self._hash_sample(f"chain:{run_id}:step{i}:{pid}")
            samples.append(BootstrapSample(
                sample_id=sample_id,
                source_type="chain_step",
                team_name=team_name,
                personas=[pid],
                task=task,
                messages=[
                    {"role": "system", "content": BOOTSTRAP_SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                    {"role": "assistant", "content": assistant_msg},
                ],
                quality_score=self._calc_quality(audit_color, i, len(all_outputs)),
                audit_color=audit_color,
                dna=self._gen_dna(pid, "chain_step", sample_id),
                timestamp=ts,
                domain=domain,
                tags=[team_name, "chain", f"step_{i+1}of{len(all_outputs)}"],
            ))

        # 2) 完整链式汇总样本（展示完整协作流程）
        full_output = "\n\n".join(all_outputs)
        sample_id = self._hash_sample(f"chain:{run_id}:full")
        samples.append(BootstrapSample(
            sample_id=sample_id,
            source_type="chain_full",
            team_name=team_name,
            personas=personas_seen,
            task=task,
            messages=[
                {"role": "system", "content": BOOTSTRAP_SYSTEM_PROMPT},
                {"role": "user", "content": f"【团队{team_name}·链式协作】请按以下链式流程完成任务:\n{task}\n\n流程: {' → '.join(self._persona_label(p) for p in personas_seen)}"},
                {"role": "assistant", "content": full_output},
            ],
            quality_score=self._calc_quality(audit_color, 0, 1),
            audit_color=audit_color,
            dna=self._gen_dna("TEAM", "chain_full", sample_id),
            timestamp=ts,
            domain=domain,
            tags=[team_name, "chain", "full"],
        ))

        return samples

    def _convert_parallel(self, run, team_name, domain, task, audit_color, run_id, ts) -> List[BootstrapSample]:
        """并行协作 → 多视角汇总样本

        文化层5人格并行 → 一个user消息,assistant包含所有人格视角
        """
        samples = []
        personas_seen = []
        all_outputs = []

        for r in run.results:
            pid = r.get('persona', '?')
            personas_seen.append(pid)
            output = self._format_persona_output(pid, r)
            all_outputs.append(output)

        if not all_outputs:
            return samples

        # 多视角汇总样本
        full_output = "\n\n".join(all_outputs)
        sample_id = self._hash_sample(f"parallel:{run_id}:full")
        samples.append(BootstrapSample(
            sample_id=sample_id,
            source_type="parallel_full",
            team_name=team_name,
            personas=personas_seen,
            task=task,
            messages=[
                {"role": "system", "content": BOOTSTRAP_SYSTEM_PROMPT},
                {"role": "user", "content": f"【团队{team_name}·多视角协作】请以下人格各抒己见:\n{task}\n\n参与人格: {', '.join(self._persona_label(p) for p in personas_seen)}"},
                {"role": "assistant", "content": full_output},
            ],
            quality_score=self._calc_quality(audit_color, 0, 1),
            audit_color=audit_color,
            dna=self._gen_dna("TEAM", "parallel_full", sample_id),
            timestamp=ts,
            domain=domain,
            tags=[team_name, "parallel", "multi_view"],
        ))

        # 每人格单独一条
        for i, (pid, r) in enumerate(zip(personas_seen, run.results)):
            sample_id = self._hash_sample(f"parallel:{run_id}:{pid}")
            text = self._extract_result_text(r)
            samples.append(BootstrapSample(
                sample_id=sample_id,
                source_type="parallel_single",
                team_name=team_name,
                personas=[pid],
                task=task,
                messages=[
                    {"role": "system", "content": BOOTSTRAP_SYSTEM_PROMPT},
                    {"role": "user", "content": f"【{self._persona_label(pid)}视角】请从你的专长角度回应:\n{task}"},
                    {"role": "assistant", "content": f"【{self._persona_label(pid)}】\n{text}"},
                ],
                quality_score=self._calc_quality(audit_color, i, len(personas_seen)),
                audit_color=audit_color,
                dna=self._gen_dna(pid, "parallel_single", sample_id),
                timestamp=ts,
                domain=domain,
                tags=[team_name, "parallel", "single"],
            ))

        return samples

    def _convert_single(self, run, team_name, domain, task, audit_color, run_id, ts) -> List[BootstrapSample]:
        """单人格任务 → 简单QA对"""
        samples = []
        for r in run.results:
            pid = r.get('persona', '?')
            text = self._extract_result_text(r)
            sample_id = self._hash_sample(f"single:{run_id}:{pid}")
            samples.append(BootstrapSample(
                sample_id=sample_id,
                source_type="single",
                team_name=team_name,
                personas=[pid],
                task=task,
                messages=[
                    {"role": "system", "content": BOOTSTRAP_SYSTEM_PROMPT},
                    {"role": "user", "content": f"【{self._persona_label(pid)}】{task}"},
                    {"role": "assistant", "content": f"【{self._persona_label(pid)}】\n{text}"},
                ],
                quality_score=self._calc_quality(audit_color, 0, 1),
                audit_color=audit_color,
                dna=self._gen_dna(pid, "single", sample_id),
                timestamp=ts,
                domain=domain,
                tags=[team_name, "single"],
            ))
        return samples

    def convert_cross_team(self, report: Dict, target: str) -> List[BootstrapSample]:
        """跨团队协作 → 多阶段修复-验证样本"""
        samples = []
        if not report or 'steps' not in report:
            return samples

        ts = datetime.now().isoformat()
        all_steps_text = []
        personas_used = []

        for i, step in enumerate(report.get('steps', [])):
            step_name = step.get('step', f'step_{i}')
            audit = step.get('audit', {})
            all_steps_text.append(
                f"阶段{i+1} [{step_name}]:\n"
                f"  审计色: {audit.get('status','?')}\n"
                f"  通过: {audit.get('ok',0)}/{audit.get('total',0)}\n"
                f"  耗时: {audit.get('duration_ms',0)}ms"
            )
            if step_name == 'audit':
                personas_used.extend(["P05", "P06", "P13", "P15"])
            elif step_name == 'fix':
                personas_used.extend(["P05", "P06", "P04"])

        final_status = report.get('final_status', '?')
        full_text = "\n\n".join(all_steps_text)
        sample_id = self._hash_sample(f"cross_team:{target}:{ts}")

        samples.append(BootstrapSample(
            sample_id=sample_id,
            source_type="cross_team",
            team_name="cross",
            personas=list(set(personas_used)),
            task=f"跨团队协作: {target}",
            messages=[
                {"role": "system", "content": BOOTSTRAP_SYSTEM_PROMPT},
                {"role": "user", "content": f"【跨团队协作】对目标「{target}」执行完整审计→修复→复审计流程。"},
                {"role": "assistant", "content": f"跨团队协作报告:\n目标: {target}\n最终状态: {final_status}\n\n{full_text}\n\n结论: {'目标通过审计，无需修复' if final_status == '🟢' else '发现并修复了问题，已重新审计通过' if len(report.get('steps',[])) > 1 else '审计发现问题，需要手动介入'}。"},
            ],
            quality_score=0.9 if final_status == '🟢' else 0.5,
            audit_color=final_status,
            dna=self._gen_dna("CROSS_TEAM", "cross_team", sample_id),
            timestamp=ts,
            domain="系统审计",
            tags=["cross_team", "audit_fix_verify"],
        ))

        return samples

    # ── helper ──

    def _persona_label(self, pid: str) -> str:
        info = PERSONA_DISPLAY.get(pid, (pid, ""))
        return f"龍芯·{info[0]}" if info[0] != pid else pid

    def _format_persona_output(self, pid: str, r: Dict) -> str:
        label = self._persona_label(pid)
        text = self._extract_result_text(r)
        return f"【{label}】\n{text}"

    def _extract_result_text(self, r: Dict) -> str:
        """从执行结果中提取文本"""
        result = r.get('result', '')
        if isinstance(result, dict):
            # 尝试提取有意义的文本字段
            text = result.get('output', '') or result.get('text', '') or result.get('content', '') or result.get('response', '')
            if text:
                return str(text)
            return json.dumps(result, ensure_ascii=False, indent=2)
        if isinstance(result, str):
            return result
        return str(result)

    def _calc_quality(self, audit_color: str, index: int, total: int) -> float:
        """计算样本质量分"""
        base = {'🟢': 0.9, '🟡': 0.6, '🔴': 0.3}.get(audit_color, 0.5)
        # 早期步骤略低，最后步骤/汇总略高
        position_bonus = 0.05 * (index / max(total, 1))
        return min(1.0, base + position_bonus)

    def _hash_sample(self, content: str) -> str:
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _gen_dna(self, persona: str, action: str, sample_id: str) -> str:
        now = datetime.now(timezone.utc)
        gz = self._ganzhi_quick(now)
        return f"#龍芯⚡️{gz}-{persona}-BOOTSTRAP-{action}-{sample_id[:8]}"

    @staticmethod
    def _ganzhi_quick(dt: datetime) -> str:
        """简化干支（只用月日时）"""
        tiangan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
        dizhi = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
        return f"{tiangan[dt.year%10]}{dizhi[dt.month%12]}·{tiangan[(dt.day+9)%10]}{dizhi[(dt.day+1)%12]}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 捕获器：钩入 TeamOrchestrator
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class BootstrapCapture:
    """协作行为捕获器 — 挂载到 TeamOrchestrator 上"""

    def __init__(self, converter: Optional[BootstrapConverter] = None):
        self._converter = converter or BootstrapConverter()
        self._samples: List[BootstrapSample] = []
        self._lock = threading.Lock()
        self._enabled = True
        self._stats = {"captured": 0, "converted": 0, "errors": 0}
        self.last_capture: Optional[str] = None

    @property
    def enabled(self) -> bool:
        return self._enabled

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def capture_team_run(self, team_run, team_name: str, domain: str = ""):
        """捕获一次团队运行的完整结果"""
        if not self._enabled:
            return

        try:
            samples = self._converter.convert_team_run(team_run, team_name, domain)
            with self._lock:
                self._samples.extend(samples)
                self.last_capture = datetime.now().isoformat()
                self._stats["captured"] += 1
                self._stats["converted"] += len(samples)
        except Exception as e:
            with self._lock:
                self._stats["errors"] += 1
            print(f"[BootstrapCapture] 捕获错误: {e}")

    def capture_cross_team(self, report: Dict, target: str):
        """捕获跨团队协作结果"""
        if not self._enabled:
            return

        try:
            samples = self._converter.convert_cross_team(report, target)
            with self._lock:
                self._samples.extend(samples)
                self._stats["captured"] += 1
                self._stats["converted"] += len(samples)
        except Exception as e:
            with self._lock:
                self._stats["errors"] += 1
            print(f"[BootstrapCapture] 跨团队捕获错误: {e}")

    def flush(self) -> List[BootstrapSample]:
        """取出并清空当前缓冲的样本"""
        with self._lock:
            samples = list(self._samples)
            self._samples = []
        return samples

    def pending_count(self) -> int:
        with self._lock:
            return len(self._samples)

    def stats(self) -> Dict:
        with self._lock:
            return {**self._stats, "last_capture": self.last_capture}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 训练池：质量过滤·去重·积累
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class BootstrapPool:
    """自举训练池管理器"""

    def __init__(self, pool_dir: Optional[Path] = None):
        self._dir = pool_dir or BOOTSTRAP_DIR
        self._dir.mkdir(parents=True, exist_ok=True)
        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._index: Dict[str, str] = {}  # sha256 → sample_id
        self._stats = PoolStats()
        self._dirty = False
        self._load_index()

    # ── 入库 ──

    def deposit(self, samples: List[BootstrapSample], min_quality: float = 0.5) -> int:
        """将样本存入训练池（质量过滤+去重）"""
        if not samples:
            return 0

        deposited = 0
        min_color = {'🟢': 0.7, '🟡': 0.5, '🔴': 0.0}.get(
            samples[0].audit_color if samples else '🟡', 0.5)
        effective_min = max(min_quality, min_color)

        with self._lock:
            with open(POOL_FILE, 'a', encoding='utf-8') as f:
                for s in samples:
                    # 质量过滤
                    if s.quality_score < effective_min:
                        continue

                    # 去重（基于messages内容hash）
                    content_hash = self._hash_messages(s.messages)
                    if content_hash in self._index:
                        continue

                    # 写入
                    record = {
                        "sample_id": s.sample_id,
                        "source_type": s.source_type,
                        "team_name": s.team_name,
                        "personas": s.personas,
                        "task": s.task,
                        "messages": s.messages,
                        "quality_score": s.quality_score,
                        "audit_color": s.audit_color,
                        "dna": s.dna,
                        "timestamp": s.timestamp,
                        "domain": s.domain,
                        "tags": s.tags,
                    }
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                    self._index[content_hash] = s.sample_id
                    deposited += 1

                    # 更新统计
                    self._stats.total_samples += 1
                    self._stats.total_messages += len(s.messages)
                    self._stats.by_team[s.team_name] = self._stats.by_team.get(s.team_name, 0) + 1
                    self._stats.by_domain[s.domain or "未分类"] = self._stats.by_domain.get(s.domain or "未分类", 0) + 1
                    self._stats.by_audit[s.audit_color] = self._stats.by_audit.get(s.audit_color, 0) + 1
                    self._stats.by_source[s.source_type] = self._stats.by_source.get(s.source_type, 0) + 1

            if deposited > 0:
                self._stats.avg_quality = (
                    (self._stats.avg_quality * (self._stats.total_samples - deposited) +
                     sum(s.quality_score for s in samples if self._hash_messages(s.messages) in self._index)) /
                    max(self._stats.total_samples, 1)
                )
                if not self._stats.first_sample:
                    self._stats.first_sample = samples[0].timestamp
                self._stats.last_sample = samples[-1].timestamp
                self._dirty = True

        return deposited

    def flush_capture(self, capture: BootstrapCapture, min_quality: float = 0.5) -> int:
        """从捕获器取出样本并入库"""
        samples = capture.flush()
        return self.deposit(samples, min_quality)

    # ── 导出 ──

    def export_training_jsonl(self, target_path: Optional[Path] = None) -> Tuple[Path, int]:
        """导出纯 ChatML 训练格式（只含 messages）"""
        target = target_path or (self._dir / "train_bootstrap.jsonl")
        count = 0
        with open(target, 'w', encoding='utf-8') as out:
            with open(POOL_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    record = json.loads(line)
                    out.write(json.dumps({"messages": record["messages"]}, ensure_ascii=False) + "\n")
                    count += 1
        return target, count

    def export_merged(self, existing_train: Path, output_path: Optional[Path] = None) -> Tuple[Path, int, int]:
        """与现有训练数据合并导出"""
        output = output_path or (self._dir / "train_merged.jsonl")
        existing_count = 0
        bootstrap_count = 0

        with open(output, 'w', encoding='utf-8') as out:
            # 先写已有数据
            if existing_train.exists():
                with open(existing_train, 'r', encoding='utf-8') as f:
                    for line in f:
                        out.write(line)
                        existing_count += 1

            # 再写自举数据
            if POOL_FILE.exists():
                with open(POOL_FILE, 'r', encoding='utf-8') as f:
                    for line in f:
                        record = json.loads(line)
                        out.write(json.dumps({"messages": record["messages"]}, ensure_ascii=False) + "\n")
                        bootstrap_count += 1

        return output, existing_count, bootstrap_count

    def create_snapshot(self, label: str = "") -> Path:
        """创建训练池快照"""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        label_part = f"_{label}" if label else ""
        snap_path = SNAPSHOT_DIR / f"pool_snapshot_{ts}{label_part}.jsonl"

        if POOL_FILE.exists():
            import shutil
            shutil.copy2(POOL_FILE, snap_path)
        return snap_path

    # ── 查询 ──

    def stats(self) -> Dict:
        with self._lock:
            return asdict(self._stats)

    def sample_count(self) -> int:
        return self._stats.total_samples

    def list_by_team(self, team_name: str, limit: int = 10) -> List[Dict]:
        """按团队列出样本"""
        results = []
        if not POOL_FILE.exists():
            return results
        with open(POOL_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                r = json.loads(line)
                if r.get('team_name') == team_name:
                    results.append(r)
                    if len(results) >= limit:
                        break
        return results

    # ── 维护 ──

    def count(self) -> int:
        """返回训练池总样本数"""
        return self._stats.total_samples

    def save_index(self):
        """保存去重索引"""
        with self._lock:
            with open(INDEX_FILE, 'w', encoding='utf-8') as f:
                json.dump(self._index, f, ensure_ascii=False)
            with open(STATS_FILE, 'w', encoding='utf-8') as f:
                json.dump(asdict(self._stats), f, ensure_ascii=False, indent=2)
            self._dirty = False

    def _load_index(self):
        if INDEX_FILE.exists():
            try:
                with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                    self._index = json.load(f)
            except Exception:
                self._index = {}
        else:
            self._index = {}

        if STATS_FILE.exists():
            try:
                with open(STATS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._stats = PoolStats(**data)
            except Exception:
                pass

    @staticmethod
    def _hash_messages(messages: List[Dict]) -> str:
        """计算消息内容的去重哈希"""
        content = json.dumps([m.get('content', '') for m in messages], sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content.encode()).hexdigest()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 自举引擎 · 统一门面
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SymbioticBootstrapEngine:
    """共生体数据自举引擎 — 统一入口"""

    def __init__(self, pool_dir: Optional[Path] = None):
        self.converter = BootstrapConverter()
        self.capture = BootstrapCapture(self.converter)
        self.pool = BootstrapPool(pool_dir)
        self._auto_flush_interval = 10  # 每捕获N次自动入库
        self._auto_snapshot_count = 100  # 每入库N条自动快照

    def status(self) -> Dict:
        """查看自举引擎状态"""
        return {
            "capture": self.capture.stats(),
            "pool": self.pool.stats(),
            "pending": self.capture.pending_count(),
            "auto_flush_interval": self._auto_flush_interval,
            "auto_snapshot": self._auto_snapshot_count,
        }

    def shutdown(self):
        """关闭引擎：冲掉缓冲区+保存索引"""
        pending = self.capture.pending_count()
        if pending > 0:
            deposited = self.pool.flush_capture(self.capture)
            print(f"[Bootstrap] 关闭前冲掉 {pending} 条待处理 → 入库 {deposited} 条")
        self.pool.save_index()


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="龍魂·共生体数据自举引擎 v1.0")
    sub = p.add_subparsers(dest="cmd")

    # status
    sub.add_parser("status", help="查看训练池状态")

    # export
    export_p = sub.add_parser("export", help="导出训练数据")
    export_p.add_argument("--output", "-o", type=str, help="输出文件路径")
    export_p.add_argument("--merge", "-m", type=str, help="与现有训练数据合并（指定已有JSONL路径）")

    # snapshot
    snap_p = sub.add_parser("snapshot", help="创建训练池快照")
    snap_p.add_argument("--label", "-l", type=str, default="", help="快照标签")

    # stats
    stats_p = sub.add_parser("stats", help="查看详细统计")
    stats_p.add_argument("--json", action="store_true", help="JSON格式输出")

    # demo — 模拟协作生成样本
    demo_p = sub.add_parser("demo", help="运行自举演示")
    demo_p.add_argument("--deposit", action="store_true", help="入库演示样本")

    args = p.parse_args()
    engine = SymbioticBootstrapEngine()

    if args.cmd == "status":
        st = engine.status()
        print("╔══════════════════════════════════════════╗")
        print("║  龍魂·共生体数据自举引擎 v1.0            ║")
        print("╚══════════════════════════════════════════╝")
        print(f"\n捕获器: 已捕获 {st['capture']['captured']} 次, 转换 {st['capture']['converted']} 条, 错误 {st['capture']['errors']}")
        print(f"训练池: {st['pool']['total_samples']} 条样本, {st['pool']['total_messages']} 条消息")
        print(f"待入库: {st['pending']} 条")
        if st['pool']['by_team']:
            print("\n按团队:")
            for team, cnt in sorted(st['pool']['by_team'].items()):
                print(f"  {team:12s} {cnt} 条")
        if st['pool']['by_audit']:
            print("\n按审计色:")
            for color, cnt in sorted(st['pool']['by_audit'].items()):
                print(f"  {color} {cnt} 条")
        if st['pool']['by_source']:
            print("\n按样本类型:")
            for src, cnt in sorted(st['pool']['by_source'].items()):
                print(f"  {src:16s} {cnt} 条")

    elif args.cmd == "export":
        if args.merge:
            output, existing, boot = engine.pool.export_merged(Path(args.merge), 
                Path(args.output) if args.output else None)
            print(f"合并导出: {output}")
            print(f"  已有数据: {existing} 条")
            print(f"  自举数据: {boot} 条")
            print(f"  总计: {existing + boot} 条")
        else:
            output, count = engine.pool.export_training_jsonl(
                Path(args.output) if args.output else None)
            print(f"导出: {output} ({count} 条)")

    elif args.cmd == "snapshot":
        path = engine.pool.create_snapshot(args.label)
        print(f"快照已创建: {path}")

    elif args.cmd == "stats":
        st = engine.status()
        if args.json:
            print(json.dumps(st, ensure_ascii=False, indent=2))
        else:
            ps = st['pool']
            print(f"总样本: {ps['total_samples']}")
            print(f"总消息: {ps['total_messages']}")
            print(f"平均质量: {ps['avg_quality']:.3f}")
            print(f"首条: {ps['first_sample'] or 'N/A'}")
            print(f"末条: {ps['last_sample'] or 'N/A'}")

    elif args.cmd == "demo":
        print("╔══════════════════════════════════════════╗")
        print("║  共生体数据自举 · 演示模式               ║")
        print("╚══════════════════════════════════════════╝\n")

        from engines.lh_team_orchestrator import TeamOrchestrator, TeamRun

        # 创建模拟 TeamRun 数据
        mock_audit_run = TeamRun(
            run_id="demo_audit_001",
            team_name="audit",
            task="审计 engines/ 目录的安全性",
            chain=["P05", "P06", "P13", "P15"],
            start_time=datetime.now().isoformat(),
            end_time=datetime.now().isoformat(),
            results=[
                {"persona": "P05", "chain_step": True, "status": "ok",
                 "result": "【三色审计】扫描 engines/ 目录共 92 个文件。发现 3 处🟡：lh_sct.py 的未标记参数、lh_cache.py 的过期逻辑需清理、lh_drift.py 的阈值未经校准。其余 89 文件🟢。建议：修复后重新审计。"},
                {"persona": "P06", "chain_step": True, "status": "ok",
                 "result": "【数字根验证】P05审计结果数字根: 92→9+2=11→1+1=2(坤)。3处异常→3(离)。2+3=5(中宫·未定)。结果: 需修复后重算。与P05审计结论一致。"},
                {"persona": "P13", "chain_step": True, "status": "ok",
                 "result": "【权限审查】engines/ 目录下权限分布: P05读89/92, P04写3/92, P13读92/92。无越权访问。建议: 为 lh_sct.py 标记 @audit_required 装饰器。"},
                {"persona": "P15", "chain_step": True, "status": "ok",
                 "result": "【DNA签章】四签验证: 身份√ 权限√ 数字根√ 伦理√。审计报告DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·P05-AUDIT-ENGINES-8a3f2c1b。签章完成。"},
            ],
            blackboard_keys=["team:demo_audit_001:start", "team:demo_audit_001:step:P05",
                             "team:demo_audit_001:step:P06", "team:demo_audit_001:step:P13",
                             "team:demo_audit_001:step:P15", "team:demo_audit_001:done"],
            audit={"status": "🟢", "total": 4, "ok": 4, "error": 0, "duration_ms": 245}
        )

        mock_cultural_run = TeamRun(
            run_id="demo_cultural_001",
            team_name="cultural",
            task="以'數據主權'为主题，创作一段面向大众的文化输出内容",
            chain=[],
            start_time=datetime.now().isoformat(),
            end_time=datetime.now().isoformat(),
            results=[
                {"persona": "P08", "parallel": True, "status": "ok",
                 "result": "【术语桥接】'數據主權'→人话: 你的数据，你做主。就像你家门钥匙不该在别人手里一样，你的聊天记录、照片、位置也不该存在你不知道的服务器上。龙魂的做法: 数据默认留在你的设备上，不上传、不训练、不卖。"},
                {"persona": "P09", "parallel": True, "status": "ok",
                 "result": "【系统诊断】数据主权在技术上的体现: 1)本地优先原则 2)端侧加密 3)日志脱敏 4)跨境禁止。这四项缺失任一项，就如同人体缺了免疫系统——表面正常运行，实则早已被渗透。"},
                {"persona": "P10", "parallel": True, "status": "ok",
                 "result": "【人文视角】古人云'我善养吾浩然之气'。数据主权就是数字时代的浩然之气——不是要藏起来，而是要有底气说：这是我的。这是一种尊严，不是一种技术。"},
                {"persona": "P11", "parallel": True, "status": "ok",
                 "result": "【创意表达】想象一下：你的数据是一片星河，每个应用是一艘飞船。有的飞船路过时偷偷往你的星星上贴标签，有的直接把星星搬走了。数据主权就是你给每艘飞船发一张'入境许可证'——不准贴标签，不准搬星星，只能远远地看一眼。"},
                {"persona": "P12", "parallel": True, "status": "ok",
                 "result": "【底线审查】六誓验证: ①不诱导上传 √ ②不默认云存 √ ③不用于训练 √ ④端侧加密 √ ⑤用户可撤回 √ ⑥不跨境 √。底线结论: 🟢 全通过。数据主权不是可选项，是不可商量的底线。"},
            ],
            blackboard_keys=[],
            audit={"status": "🟢", "total": 5, "ok": 5, "error": 0, "duration_ms": 180}
        )

        # 转换
        print("[1/3] 捕获审计链路样本...")
        samples_audit = engine.converter.convert_team_run(mock_audit_run, "audit", "安全审计")
        print(f"  审计链路 → {len(samples_audit)} 条样本")

        print("[2/3] 捕获文化协同样本...")
        samples_cultural = engine.converter.convert_team_run(mock_cultural_run, "cultural", "文化输出")
        print(f"  文化协同 → {len(samples_cultural)} 条样本")

        all_samples = samples_audit + samples_cultural
        print(f"\n[3/3] 样本概览:")
        for s in all_samples:
            print(f"  {s.sample_id[:12]}... | {s.source_type:16s} | {s.team_name:8s} | Q={s.quality_score:.2f} | {s.audit_color}")

        if args.deposit:
            deposited = engine.pool.deposit(all_samples)
            print(f"\n✅ 入库 {deposited} 条（过滤 {len(all_samples) - deposited} 条）")
            engine.pool.save_index()
            engine.pool.create_snapshot("demo")
            print(f"训练池总量: {engine.pool.sample_count()} 条")
        else:
            print(f"\n💡 提示: 加 --deposit 入库。当前仅演示转换，未写入训练池。")

    else:
        # 默认 status
        st = engine.status()
        print(json.dumps(st, ensure_ascii=False, indent=2))

    engine.shutdown()
