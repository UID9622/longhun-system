# ============================================================
# 龍魂 · ANTENNA-8GATE 五行调度器 v2.0
# DNA: #龍芯⚡️丙午·乙未·乙未·申时·☰乾-WUXING-SCHEDULER-V2-a1b2c3d4
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# ============================================================
"""
五行调度器 v2.0 — 升级版

v1.0 → v2.0 升级：
  1. 五行健康度闭环反馈：每一轮调度结束输出五行健康度报告
  2. 生克关系调度：相生（促进）→放行，相克（制约）→降速但不阻断
  3. 自动愈合：健康度<95%触发相生补偿，>105%触发相克制动
  4. 调度周期报告：JSON输出，可直接喂给可视化仪表盘

五行·五脏映射：
  木 → 肝 → 生发·创新任务（调度器启动/规律破坏后重建）
  火 → 心 → 推动·执行任务（高热任务·持续推动）
  土 → 脾 → 运化·数据处理（承上启下·转换搬运）
  金 → 肺 → 收敛·审计任务（截断不合格·只放行合格）
  水 → 肾 → 固本·安全任务（不动之动·兜底）

铁律：五行调度不是可选项，是强制项。任何任务先进八卦路由，再过五行调度。
"""

import sys, os
import time
import threading
import json
import hashlib
import copy
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import IntEnum
from collections import deque, OrderedDict
from queue import PriorityQueue


# ═══════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════

class Wuxing(IntEnum):
    """五行"""
    木 = 0  # 肝·生发
    火 = 1  # 心·推动
    土 = 2  # 脾·运化
    金 = 3  # 肺·收敛
    水 = 4  # 肾·固本


# 五行生克关系
WUXING_SHENG = {  # 相生：生我者 → 我
    Wuxing.木: Wuxing.水,  # 水生木
    Wuxing.火: Wuxing.木,  # 木生火
    Wuxing.土: Wuxing.火,  # 火生土
    Wuxing.金: Wuxing.土,  # 土生金
    Wuxing.水: Wuxing.金,  # 金生水
}

WUXING_KE = {  # 相克：克我者 → 我
    Wuxing.木: Wuxing.金,  # 金克木
    Wuxing.火: Wuxing.水,  # 水克火
    Wuxing.土: Wuxing.木,  # 木克土
    Wuxing.金: Wuxing.火,  # 火克金
    Wuxing.水: Wuxing.土,  # 土克水
}

# 反向：我生者
WUXING_I_SHENG = {v: k for k, v in WUXING_SHENG.items()}
# 反向：我克者
WUXING_I_KE = {v: k for k, v in WUXING_KE.items()}

WUXING_NAMES = {
    Wuxing.木: "木·肝",
    Wuxing.火: "火·心",
    Wuxing.土: "土·脾",
    Wuxing.金: "金·肺",
    Wuxing.水: "水·肾",
}

WUXING_DOMAINS = {
    Wuxing.木: "生发·创新",
    Wuxing.火: "推动·执行",
    Wuxing.土: "运化·数据处理",
    Wuxing.金: "收敛·审计",
    Wuxing.水: "固本·安全",
}

# 任务类型 → 五行映射
TASK_WUXING_MAP = {
    "创新": Wuxing.木, "创建": Wuxing.木, "启动": Wuxing.木, "生成": Wuxing.木,
    "执行": Wuxing.火, "推动": Wuxing.火, "部署": Wuxing.火, "运行": Wuxing.火,
    "数据处理": Wuxing.土, "转换": Wuxing.土, "搬运": Wuxing.土, "调度": Wuxing.土,
    "审计": Wuxing.金, "收敛": Wuxing.金, "验证": Wuxing.金, "检查": Wuxing.金,
    "安全": Wuxing.水, "固本": Wuxing.水, "兜底": Wuxing.水, "备份": Wuxing.水,
}


@dataclass
class WuxingTask:
    """五行任务"""
    task_id: str
    wuxing: Wuxing
    priority: int  # 0=P0最高 9=P9最低
    payload: Any
    created_at: float = field(default_factory=time.time)
    timeout_s: float = 30.0

    def __lt__(self, other):
        return self.priority < other.priority  # 小数值=高优先级


@dataclass
class OrganMetrics:
    """脏器指标"""
    wuxing: Wuxing
    health: float = 100.0  # 健康度 0-100-125
    processed: int = 0
    queued: int = 0
    dropped: int = 0
    total_latency_ms: float = 0.0
    last_heal_at: float = 0.0
    last_brake_at: float = 0.0

    @property
    def avg_latency_ms(self) -> float:
        if self.processed == 0:
            return 0.0
        return self.total_latency_ms / self.processed

    @property
    def status(self) -> str:
        if self.health >= 95:
            return "🟢 健康"
        elif self.health >= 80:
            return "🟡 亚健康"
        elif self.health >= 60:
            return "🟠 需调理"
        else:
            return "🔴 告急"


# ═══════════════════════════════════════
# 五行调度器 v2.0
# ═══════════════════════════════════════

class WuxingSchedulerV2:
    """
    五行调度器 v2.0
    
    五线并行调度，生克自动平衡。
    每轮调度结束输出五行健康度报告。
    """

    HEALTH_TARGET = 100.0     # 目标健康度
    HEALTH_UPPER = 105.0      # 过亢阈值（触发相克制动）
    HEALTH_LOWER = 95.0       # 虚衰阈值（触发相生补偿）
    HEALTH_CRITICAL = 60.0    # 危急阈值
    HEAL_RATE = 3.5           # 每轮自愈速率（上调以支持300+任务吞吐）
    BRAKE_RATE = 1.5          # 每轮制动速率

    def __init__(self):
        # 五脏器官
        self.organs: Dict[Wuxing, OrganMetrics] = {
            wx: OrganMetrics(wuxing=wx) for wx in Wuxing
        }

        # 各器官任务队列
        self.queues: Dict[Wuxing, PriorityQueue] = {
            wx: PriorityQueue() for wx in Wuxing
        }

        # 工作线程
        self.workers: Dict[Wuxing, threading.Thread] = {}
        self._stop_flags: Dict[Wuxing, threading.Event] = {
            wx: threading.Event() for wx in Wuxing
        }

        # 调度历史
        self.cycle_history: deque = deque(maxlen=100)
        self.total_processed = 0
        self.total_dropped = 0
        self._scheduler_lock = threading.RLock()
        self._running = False

        # 启动所有器官
        self.start_all()

    # ── 公共API ──

    def submit(self, task: WuxingTask) -> bool:
        """提交任务到对应脏器"""
        if task.wuxing not in self.queues:
            return False

        organ = self.organs[task.wuxing]
        with self._scheduler_lock:
            organ.queued += 1

        self.queues[task.wuxing].put(task)
        return True

    def submit_many(self, tasks: List[WuxingTask]) -> int:
        """批量提交"""
        count = 0
        for task in tasks:
            if self.submit(task):
                count += 1
        return count

    def route_to_wuxing(self, bagua_name: str, task_type: Optional[str] = None) -> Wuxing:
        """
        八卦 → 五行 映射
        
        八卦五行对应：
        乾兑 → 金 | 离 → 火 | 震巽 → 木 | 坎 → 水 | 坤艮 → 土
        """
        bagua_wuxing = {
            "乾": Wuxing.金, "兑": Wuxing.金,
            "离": Wuxing.火,
            "震": Wuxing.木, "巽": Wuxing.木,
            "坎": Wuxing.水,
            "坤": Wuxing.土, "艮": Wuxing.土,
        }
        
        # 有明确任务类型提示时优先用类型映射
        if task_type:
            for kw, wx in TASK_WUXING_MAP.items():
                if kw in task_type:
                    return wx
        
        return bagua_wuxing.get(bagua_name, Wuxing.土)

    def start_all(self):
        """启动全部五个器官工作线程"""
        for wx in Wuxing:
            self._stop_flags[wx].clear()
            t = threading.Thread(
                target=self._organ_worker,
                args=(wx,),
                name=f"wuxing-{WUXING_NAMES[wx]}",
                daemon=True
            )
            self.workers[wx] = t
            t.start()
        self._running = True

    def stop_all(self):
        """停止全部器官"""
        for wx in Wuxing:
            self._stop_flags[wx].set()
        for wx, t in self.workers.items():
            t.join(timeout=3.0)
        self._running = False

    def get_balance_report(self) -> Dict[str, Any]:
        """获取五行健康度报告（v2.0核心输出）"""
        with self._scheduler_lock:
            organs_report = {}
            health_values = []
            for wx in Wuxing:
                o = self.organs[wx]
                organs_report[WUXING_NAMES[wx]] = {
                    "wuxing": wx.name,
                    "domain": WUXING_DOMAINS[wx],
                    "health": round(o.health, 2),
                    "status": o.status,
                    "processed": o.processed,
                    "queued": o.queued,
                    "dropped": o.dropped,
                    "avg_latency_ms": round(o.avg_latency_ms, 4),
                }
                health_values.append(o.health)

            avg_health = sum(health_values) / 5
            imbalance = max(health_values) - min(health_values)

            # 判定整体状态
            if imbalance < 5:
                overall = "平衡"
            elif imbalance < 15:
                overall = "轻微失衡"
            elif imbalance < 30:
                overall = "中度失衡"
            else:
                overall = "严重失衡"

            # 生克建议
            shengke_advice = self._generate_shengke_advice()

            # 吞吐量统计
            total = self.total_processed + self.total_dropped
            throughput = self.total_processed / max(self._elapsed_seconds(), 0.001)

            return {
                "timestamp": time.time(),
                "overall_status": overall,
                "avg_health": round(avg_health, 2),
                "imbalance": round(imbalance, 2),
                "total_processed": self.total_processed,
                "total_dropped": self.total_dropped,
                "throughput_tasks_per_sec": round(throughput, 1),
                "organs": organs_report,
                "shengke_advice": shengke_advice,
                "dna": self._gen_dna(),
            }

    def get_health_json(self) -> str:
        """健康报告 JSON 输出"""
        return json.dumps(self.get_balance_report(), ensure_ascii=False, indent=2)

    # ── 内部引擎 ──

    def _organ_worker(self, wx: Wuxing):
        """脏器工作线程"""
        q = self.queues[wx]
        organ = self.organs[wx]
        stop = self._stop_flags[wx]

        while not stop.is_set():
            try:
                task: WuxingTask = q.get(timeout=0.5)
            except:
                # 空闲时自愈
                self._auto_heal(wx)
                continue

            t0 = time.time()
            processed = self._execute_task(task)
            latency_ms = (time.time() - t0) * 1000

            with self._scheduler_lock:
                if processed:
                    organ.processed += 1
                    organ.total_latency_ms += latency_ms
                    self.total_processed += 1
                    # 执行任务消耗一点健康（自然损耗，降低到0.02per/任务）
                    organ.health = max(60, organ.health - 0.02)
                else:
                    organ.dropped += 1
                    self.total_dropped += 1
                    organ.health = max(40, organ.health - 0.5)  # 丢弃任务损耗更大

                organ.queued = max(0, organ.queued - 1)

            # 每10次任务跑一次生克平衡
            if organ.processed % 10 == 0:
                self._balance_shengke()

    def _execute_task(self, task: WuxingTask) -> bool:
        """执行任务"""
        # 过载保护：健康度<60直接丢
        organ = self.organs[task.wuxing]
        if organ.health < self.HEALTH_CRITICAL:
            return False

        # 模拟 CPU 工作（可替换为真实任务执行器）
        load = max(1, task.priority + 1)
        time.sleep(0.001 * load)  # 1-10ms

        return True

    def _auto_heal(self, wx: Wuxing):
        """自然自愈：相生者补益"""
        organ = self.organs[wx]
        if organ.health < self.HEALTH_LOWER:
            # 找到生我者
            mother_wx = WUXING_SHENG[wx]
            mother = self.organs[mother_wx]
            # 相生补益
            organ.health = min(self.HEALTH_TARGET, organ.health + self.HEAL_RATE * 0.1)
            organ.last_heal_at = time.time()
            # 母脏消耗小量
            mother.health = max(60, mother.health - 0.02)

    def _balance_shengke(self):
        """一轮生克平衡"""
        for wx in Wuxing:
            organ = self.organs[wx]

            # 过亢 → 相克制动
            if organ.health > self.HEALTH_UPPER:
                ke_wx = WUXING_KE[wx]  # 克我者
                ke_organ = self.organs[ke_wx]
                organ.health -= self.BRAKE_RATE * 0.1
                ke_organ.health -= 0.1  # 克者也有消耗
                organ.last_brake_at = time.time()

            # 虚衰 → 相生补益
            elif organ.health < self.HEALTH_LOWER:
                sheng_wx = WUXING_SHENG[wx]  # 生我者
                organ.health += self.HEAL_RATE * 0.05
                organ.last_heal_at = time.time()

        # 边界钳制
        for wx in Wuxing:
            self.organs[wx].health = max(40, min(125, self.organs[wx].health))

    def _generate_shengke_advice(self) -> List[str]:
        """生成生克调理建议"""
        advice = []
        for wx in Wuxing:
            organ = self.organs[wx]
            name = WUXING_NAMES[wx]

            if organ.health > self.HEALTH_UPPER:
                ke_name = WUXING_NAMES[WUXING_KE[wx]]
                advice.append(f"{name}过亢({organ.health:.0f}%) → 建议加强{ke_name}制衡")

            elif organ.health < self.HEALTH_LOWER:
                sheng_name = WUXING_NAMES[WUXING_SHENG[wx]]
                advice.append(f"{name}虚衰({organ.health:.0f}%) → 建议{sheng_name}补益")

        return advice

    def _elapsed_seconds(self) -> float:
        """调度器运行时长"""
        organ = self.organs[Wuxing.火]  # 用火脏计时（最活跃）
        if organ.processed == 0:
            return 0.001
        return max(0.001, time.time() - organ.last_heal_at if organ.last_heal_at > 0 else time.time())

    def _gen_dna(self) -> str:
        """生成报告DNA"""
        h = hashlib.sha256(
            f"{time.time()}:{self.total_processed}:{self.total_dropped}".encode()
        ).hexdigest()[:8]
        return f"#龍芯⚡️☯-WUXING-REPORT-V2-{h}"


# ═══════════════════════════════════════
# 自测试
# ═══════════════════════════════════════
if __name__ == "__main__":
    import numpy as np

    print("═" * 50)
    print("龍魂 · 五行调度器 v2.0 · 自检")
    print("═" * 50)

    scheduler = WuxingSchedulerV2()

    # 提交50个任务，均匀分布五行
    print("\n提交50个任务...")
    for i in range(50):
        wx = Wuxing(i % 5)
        task = WuxingTask(
            task_id=f"task-{i}",
            wuxing=wx,
            priority=i % 3,  # P0-P2
            payload=np.random.randn(128),
        )
        scheduler.submit(task)

    time.sleep(1.0)  # 等待处理

    # 输出健康报告
    report = scheduler.get_balance_report()
    print(f"\n📊 五行健康报告")
    print(f"══════════════════════════════════════════")
    print(f"整体状态: {report['overall_status']}")
    print(f"平均健康: {report['avg_health']}%")
    print(f"失衡度:   {report['imbalance']}")
    print(f"总处理:   {report['total_processed']}")
    print(f"总丢弃:   {report['total_dropped']}")
    print(f"吞吐量:   {report['throughput_tasks_per_sec']:.1f} 任务/秒")
    print()

    for name, stats in report['organs'].items():
        bar_len = int(stats['health'] / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(f"  {name:<10} [{bar}] {stats['health']:.1f}% {stats['status']}"
              f" | 处理{stats['processed']} 丢弃{stats['dropped']}"
              f" | 延迟{stats['avg_latency_ms']:.3f}ms")

    if report['shengke_advice']:
        print(f"\n💊 生克调理建议:")
        for a in report['shengke_advice']:
            print(f"  → {a}")

    scheduler.stop_all()

    # 验证：all health >= 95%
    all_healthy = all(s['health'] >= 95 for s in report['organs'].values())
    print(f"\n{'🟢 五行健康全部 >= 95%' if all_healthy else '🟡 部分脏器需调理'}")
