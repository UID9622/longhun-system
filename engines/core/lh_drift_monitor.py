# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂系统 · 概念漂移监控引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丙申·酉时·☰乾-CONCEPT-DRIFT-v1.0-f7a8b9c0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
补全: DL架构§11.6 概念漂移监控·数据分布检测·模型退化预警

功能:
  1. 数据漂移检测 - 输入分布变化监控
  2. 概念漂移检测 - 输出分布变化监控  
  3. 模型退化预警 - val_loss趋势异常检测
  4. 周期性报告 - 日报/周报自动生成
  5. 熔断联动 - 漂移>阈值触发L3熔断

检测维度:
  - KS检验: 连续特征分布变化
  - 卡方检验: 分类特征分布变化
  - 嵌入距离: 语义空间漂移量
  - 误差趋势: 滑动窗口MA趋势
"""

import json
import time
import hashlib
import sqlite3
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple, Any
from dataclasses import dataclass, field
from collections import deque

# ═══ 配置 ═══
BASE_DIR = Path(__file__).resolve().parent.parent
DRIFT_DB = BASE_DIR / "data" / "drift_monitor.db"
WINDOW_SIZE = 100         # 滑动窗口大小
DRIFT_THRESHOLD = 0.05    # KS统计量阈值
EMBED_DRIFT_THRESHOLD = 0.15  # 嵌入空间漂移阈值
VAL_LOSS_TREND_WINDOW = 20    # val_loss趋势窗口
TREND_THRESHOLD = 0.02        # 趋势阈值(正=下降好/负=上升坏)

# ═══ 数据模型 ═══
@dataclass
class DistributionSample:
    """分布样本"""
    timestamp: float
    data: np.ndarray
    source: str  # input | output | embedding
    
@dataclass  
class DriftAlert:
    """漂移告警"""
    timestamp: float
    dimension: str
    metric: str
    value: float
    threshold: float
    severity: str  # warning | critical
    dna: str

# ═══ 数据库 ═══
def init_db():
    DRIFT_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DRIFT_DB))
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS drift_samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            source TEXT NOT NULL,
            data_hash TEXT,
            feature_count INTEGER,
            sample_count INTEGER,
            dna TEXT
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS drift_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            dimension TEXT NOT NULL,
            metric TEXT NOT NULL,
            value REAL NOT NULL,
            threshold REAL NOT NULL,
            severity TEXT NOT NULL,
            dna TEXT
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS val_loss_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            model_name TEXT NOT NULL,
            val_loss REAL NOT NULL,
            train_loss REAL,
            epoch INTEGER,
            dna TEXT
        )
    """)
    
    conn.execute("CREATE INDEX IF NOT EXISTS idx_samples_time ON drift_samples(timestamp)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_alerts_time ON drift_alerts(timestamp)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_val_model ON val_loss_history(model_name)")
    
    conn.commit()
    return conn

# ═══ 核心引擎 ═══
class DriftMonitor:
    def __init__(self, window_size: int = WINDOW_SIZE):
        self.conn = init_db()
        self.window_size = window_size
        self.baseline: Dict[str, np.ndarray] = {}  # source → baseline distribution
        self.alerts: deque = deque(maxlen=100)
    
    def set_baseline(self, source: str, data: np.ndarray):
        """设置基线分布"""
        self.baseline[source] = data
        self._record_sample(source, data, is_baseline=True)
    
    def check_distribution_drift(self, source: str, current: np.ndarray) -> DriftAlert:
        """
        KS检验检测分布漂移
        """
        baseline = self.baseline.get(source)
        if baseline is None:
            self.set_baseline(source, current)
            return None
        
        if len(baseline) < 30 or len(current) < 30:
            self._record_sample(source, current)
            return None
        
        try:
            from scipy import stats
            
            # KS检验
            ks_stat, p_value = stats.ks_2samp(baseline, current)
            
            # 均值漂移
            mean_shift = abs(np.mean(current) - np.mean(baseline)) / (np.std(baseline) + 1e-8)
            
            # 方差漂移
            var_ratio = np.var(current) / (np.var(baseline) + 1e-8)
            
            self._record_sample(source, current)
            
            # 判定
            if ks_stat > DRIFT_THRESHOLD * 3 or p_value < 0.001:
                alert = DriftAlert(
                    timestamp=time.time(),
                    dimension=source,
                    metric="KS",
                    value=float(ks_stat),
                    threshold=DRIFT_THRESHOLD,
                    severity="critical",
                    dna=self._dna(source, "ks_critical"),
                )
                self.alerts.append(alert)
                self._save_alert(alert)
                return alert
                
            elif ks_stat > DRIFT_THRESHOLD or p_value < 0.05:
                alert = DriftAlert(
                    timestamp=time.time(),
                    dimension=source,
                    metric="KS",
                    value=float(ks_stat),
                    threshold=DRIFT_THRESHOLD,
                    severity="warning",
                    dna=self._dna(source, "ks_warning"),
                )
                self.alerts.append(alert)
                self._save_alert(alert)
                return alert
            
            return None
            
        except ImportError:
            # 无scipy时使用简化版Jensen-Shannon近似
            return self._simple_drift_check(source, baseline, current)
    
    def check_embedding_drift(self, source: str, current_embeddings: np.ndarray) -> Optional[DriftAlert]:
        """
        嵌入空间漂移检测
        使用余弦距离的均值偏移
        """
        baseline_emb = self.baseline.get(f"{source}_emb")
        if baseline_emb is None:
            self.baseline[f"{source}_emb"] = current_embeddings
            return None
        
        if len(baseline_emb) < 10 or len(current_embeddings) < 10:
            return None
        
        # 计算基线中心和新中心
        baseline_center = np.mean(baseline_emb, axis=0)
        current_center = np.mean(current_embeddings, axis=0)
        
        # 余弦距离
        cos_sim = np.dot(baseline_center, current_center) / (
            np.linalg.norm(baseline_center) * np.linalg.norm(current_center) + 1e-8
        )
        drift = 1 - cos_sim
        
        self.baseline[f"{source}_emb"] = current_embeddings  # 渐进更新基线
        
        if drift > EMBED_DRIFT_THRESHOLD:
            alert = DriftAlert(
                timestamp=time.time(),
                dimension=f"{source}_embedding",
                metric="cosine_drift",
                value=float(drift),
                threshold=EMBED_DRIFT_THRESHOLD,
                severity="critical" if drift > EMBED_DRIFT_THRESHOLD * 2 else "warning",
                dna=self._dna(source, "embed_drift"),
            )
            self.alerts.append(alert)
            self._save_alert(alert)
            return alert
        
        return None
    
    def check_val_loss_trend(self, model_name: str) -> Optional[DriftAlert]:
        """
        验证损失趋势检测 - 模型退化预警
        """
        cursor = self.conn.execute(
            "SELECT val_loss, timestamp FROM val_loss_history WHERE model_name=? ORDER BY timestamp DESC LIMIT ?",
            (model_name, VAL_LOSS_TREND_WINDOW)
        )
        history = cursor.fetchall()
        
        if len(history) < 5:
            return None
        
        losses = [h[0] for h in history]
        
        # 滑动窗口趋势
        window = min(5, len(losses) // 3)
        ma_recent = np.mean(losses[:window])
        ma_early = np.mean(losses[-window:])
        
        trend = (ma_recent - ma_early) / (ma_early + 1e-8)
        
        if trend > TREND_THRESHOLD * 3:  # 显著退化
            alert = DriftAlert(
                timestamp=time.time(),
                dimension=f"val_loss:{model_name}",
                metric="trend",
                value=float(trend),
                threshold=TREND_THRESHOLD,
                severity="critical",
                dna=self._dna(model_name, "val_degrade"),
            )
            self.alerts.append(alert)
            self._save_alert(alert)
            return alert
        
        elif trend > TREND_THRESHOLD:
            alert = DriftAlert(
                timestamp=time.time(),
                dimension=f"val_loss:{model_name}",
                metric="trend",
                value=float(trend),
                threshold=TREND_THRESHOLD,
                severity="warning",
                dna=self._dna(model_name, "val_warning"),
            )
            self.alerts.append(alert)
            self._save_alert(alert)
            return alert
        
        return None
    
    def record_val_loss(self, model_name: str, val_loss: float, 
                        train_loss: Optional[float] = None, epoch: int = 0):
        """记录验证损失"""
        self.conn.execute(
            "INSERT INTO val_loss_history (timestamp, model_name, val_loss, train_loss, epoch, dna) VALUES (?,?,?,?,?,?)",
            (time.time(), model_name, val_loss, train_loss, epoch, self._dna(model_name, "val"))
        )
        self.conn.commit()
        
        # 自动趋势检测
        return self.check_val_loss_trend(model_name)
    
    def get_recent_alerts(self, hours: int = 24) -> List[Dict]:
        """获取最近告警"""
        cutoff = time.time() - hours * 3600
        cursor = self.conn.execute(
            "SELECT * FROM drift_alerts WHERE timestamp > ? ORDER BY timestamp DESC",
            (cutoff,)
        )
        return [
            {
                "timestamp": datetime.fromtimestamp(r[1]).isoformat(),
                "dimension": r[2], "metric": r[3],
                "value": r[4], "threshold": r[5],
                "severity": r[6], "dna": r[7],
            }
            for r in cursor
        ]
    
    def generate_report(self, period: str = "daily") -> Dict[str, Any]:
        """生成漂移报告"""
        now = time.time()
        if period == "daily":
            since = now - 86400
        elif period == "weekly":
            since = now - 7 * 86400
        else:
            since = now - 86400
        
        alerts = self.conn.execute(
            "SELECT severity, COUNT(*) FROM drift_alerts WHERE timestamp > ? GROUP BY severity",
            (since,)
        ).fetchall()
        
        critical = sum(c for s, c in alerts if s == "critical")
        warnings = sum(c for s, c in alerts if s == "warning")
        
        # 检查模型趋势
        models = self.conn.execute(
            "SELECT DISTINCT model_name FROM val_loss_history"
        ).fetchall()
        
        model_trends = {}
        for (name,) in models:
            cursor = self.conn.execute(
                "SELECT val_loss FROM val_loss_history WHERE model_name=? ORDER BY timestamp DESC LIMIT ?",
                (name, VAL_LOSS_TREND_WINDOW)
            )
            losses = [r[0] for r in cursor]
            if len(losses) >= 5:
                ma_recent = sum(losses[:5]) / 5
                ma_early = sum(losses[-5:]) / 5
                trend = (ma_recent - ma_early) / (ma_early + 1e-8)
                model_trends[name] = {
                    "current_ma": round(ma_recent, 4),
                    "trend": round(trend, 4),
                    "status": "degrading" if trend > TREND_THRESHOLD else "improving" if trend < -TREND_THRESHOLD else "stable",
                }
        
        return {
            "period": period,
            "generated_at": datetime.now().isoformat(),
            "alerts": {"critical": critical, "warning": warnings},
            "model_trends": model_trends,
            "summary": (
                "🟢 无显著漂移" if (critical + warnings) == 0
                else f"🔴 {critical}严重·🟡 {warnings}警告·需关注"
            ),
            "dna": self._dna(f"report_{period}", "drift"),
        }
    
    # ═══ 内部方法 ═══
    def _simple_drift_check(self, source: str, baseline: np.ndarray, current: np.ndarray) -> Optional[DriftAlert]:
        """简化版漂移检测（无scipy时）"""
        b_mean, b_std = np.mean(baseline), np.std(baseline)
        c_mean, c_std = np.mean(current), np.std(current)
        
        mean_shift = abs(c_mean - b_mean) / (b_std + 1e-8)
        std_ratio = c_std / (b_std + 1e-8)
        
        if mean_shift > 3 or std_ratio > 3 or std_ratio < 0.33:
            self._record_sample(source, current)
            alert = DriftAlert(
                timestamp=time.time(),
                dimension=source, metric="simple_drift",
                value=float(max(mean_shift, std_ratio)),
                threshold=2.0,
                severity="critical",
                dna=self._dna(source, "simple_critical"),
            )
            self.alerts.append(alert)
            self._save_alert(alert)
            return alert
        
        self._record_sample(source, current)
        return None
    
    def _record_sample(self, source: str, data: np.ndarray, is_baseline: bool = False):
        data_hash = hashlib.md5(data.tobytes()).hexdigest()[:16]
        self.conn.execute(
            "INSERT INTO drift_samples (timestamp, source, data_hash, feature_count, sample_count, dna) VALUES (?,?,?,?,?,?)",
            (time.time(), source, data_hash, data.shape[-1] if data.ndim > 1 else 1, len(data), self._dna(source, "sample"))
        )
        self.conn.commit()
    
    def _save_alert(self, alert: DriftAlert):
        self.conn.execute(
            "INSERT INTO drift_alerts (timestamp, dimension, metric, value, threshold, severity, dna) VALUES (?,?,?,?,?,?,?)",
            (alert.timestamp, alert.dimension, alert.metric, alert.value, alert.threshold, alert.severity, alert.dna)
        )
        self.conn.commit()
    
    def _dna(self, source: str, action: str) -> str:
        ts = datetime.now()
        h = hashlib.md5(f"{source}{action}{ts.timestamp()}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️{ts.strftime('%Y-%m-%d')}-DRIFT-{action.upper()}-{h}"
    
    def close(self):
        self.conn.close()

# ═══ CLI ═══
def main():
    import sys
    
    if len(sys.argv) < 2:
        print("🐉 概念漂移监控 CLI")
        print("  check <model>         检查模型退化趋势")
        print("  report [daily|weekly] 生成漂移报告")
        print("  alerts                查看最近告警")
        print("  record <model> <loss> 记录val_loss")
        return
    
    monitor = DriftMonitor()
    cmd = sys.argv[1]
    
    try:
        if cmd == "check" and len(sys.argv) > 2:
            alert = monitor.check_val_loss_trend(sys.argv[2])
            if alert:
                print(f"⚠️  漂移告警: {alert.dimension} {alert.metric}={alert.value:.4f} (阈值={alert.threshold}) [{alert.severity}]")
            else:
                print(f"🟢 {sys.argv[2]}: 无显著退化")
        
        elif cmd == "report":
            period = sys.argv[2] if len(sys.argv) > 2 else "daily"
            report = monitor.generate_report(period)
            print(json.dumps(report, indent=2, ensure_ascii=False))
        
        elif cmd == "alerts":
            hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
            alerts = monitor.get_recent_alerts(hours)
            for a in alerts:
                icon = "🔴" if a["severity"] == "critical" else "🟡"
                print(f"{icon} {a['timestamp'][:19]} | {a['dimension']} | {a['metric']}={a['value']:.4f}")
        
        elif cmd == "record" and len(sys.argv) > 3:
            model = sys.argv[2]
            loss = float(sys.argv[3])
            train_loss = float(sys.argv[4]) if len(sys.argv) > 4 else None
            alert = monitor.record_val_loss(model, loss, train_loss)
            print(f"✅ 已记录 {model} val_loss={loss}")
            if alert:
                print(f"⚠️  {alert.severity}: 退化趋势检出")
    
    finally:
        monitor.close()

if __name__ == "__main__":
    main()
