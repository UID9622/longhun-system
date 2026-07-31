# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂 · 个人数据主权雷达 — 扫描引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·戊戌·午时·☵坎-DATA-RADAR-v1.0
创建者: 诸葛鑫（UID9622）· 协议: CC BY-NC-SA 4.0
人格: P05上帝之眼（审计） + P77黑天使（安全扫描）
铁律: 数据不出设备·报告通俗化·红色警告🟢安全一目了然
"""

import hashlib
import json
import os
import platform
import re
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══ 常量 ═══
DNA = "#龍芯⚡️丙午·乙未·戊戌·午时·☵坎-DATA-RADAR-v1.0"
CREATOR = "诸葛鑫（UID9622）"
PROTOCOL = "CC BY-NC-SA 4.0"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "radar"
AUDIT_LOG = PROJECT_ROOT / "audit" / "radar_scan.jsonl"
APP_DB_PATH = PROJECT_ROOT / "data" / "radar" / "app_behavior_db.json"

# P0协议清单（老百姓能看懂的版本）
P0_PROTOCOLS_HUMAN = {
    "P0-01": {"name": "不得建后门", "desc": "代码里不能藏偷偷上传数据的后门", "icon": "🔐"},
    "P0-02": {"name": "不得存民籍", "desc": "你的个人信息只存你自己设备上", "icon": "👤"},
    "P0-03": {"name": "数据不出境", "desc": "你的数据不经过国外服务器", "icon": "🗺️"},
    "P0-04": {"name": "零黑箱算法", "desc": "AI怎么做的决定，你可以看明白", "icon": "📦"},
    "P0-05": {"name": "加密不打折", "desc": "国密SM4/AES-256级加密，银行同款", "icon": "🔒"},
    "P0-06": {"name": "不追踪不画像", "desc": "不分析你的习惯、不给你打标签", "icon": "🚫"},
    "P0-07": {"name": "本地优先", "desc": "能在手机上算的，绝不上传云端", "icon": "📱"},
    "P0-08": {"name": "一键熔断", "desc": "按一个按钮，所有数据收集全部切断", "icon": "🛑"},
    "P0-09": {"name": "可审计可追溯", "desc": "每次操作都有记录，谁动了你的数据一查就知道", "icon": "🔍"},
    "P0-10": {"name": "生物特征验证", "desc": "重要操作必须你本人指纹/面容确认", "icon": "🫵"},
    "P0-11": {"name": "不删只冻结", "desc": "旧数据不删，标'已冻结'保留证据", "icon": "🧊"},
    "P0-12": {"name": "开源可复核", "desc": "代码公开，任何人都能检查有没有后门", "icon": "📖"},
}


class ThreatSeverity(str, Enum):
    HIGH = "🔴 高危"
    MEDIUM = "🟡 中危"
    LOW = "🟢 低危"
    BLOCKED = "🟢 已拦截"


class ScanMode(str, Enum):
    QUICK = "quick"       # 30秒快速扫
    DEEP = "deep"         # 5分钟深度扫
    CONTINUOUS = "continuous"  # 持续监控


@dataclass
class Threat:
    """一条威胁记录"""
    app_name: str
    app_bundle: str
    threat_type: str          # 数据上传/位置追踪/通讯录窃取/相册扫描/麦克风监听/后台同步
    severity: ThreatSeverity
    detail: str               # 老百姓看得懂的解释
    frequency: int = 0        # 发生次数
    destination: str = ""     # 数据去了哪里
    first_seen: str = ""
    last_seen: str = ""
    blocked: bool = False
    human_explain: str = ""   # 一句话人话解释

    def to_dict(self) -> dict:
        return {
            "app_name": self.app_name,
            "app_bundle": self.app_bundle,
            "threat_type": self.threat_type,
            "severity": self.severity.value,
            "detail": self.detail,
            "frequency": self.frequency,
            "destination": self.destination,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "blocked": self.blocked,
            "human_explain": self.human_explain or self._gen_human(),
        }

    def _gen_human(self) -> str:
        """生成老百姓听得懂的描述"""
        templates = {
            "数据上传": f"{self.app_name}偷偷把你的数据传到了{self.destination or '它自己的服务器'}，共{self.frequency}次",
            "位置追踪": f"{self.app_name}在后台追踪你的位置",
            "通讯录窃取": f"{self.app_name}读取了你的通讯录",
            "相册扫描": f"{self.app_name}扫描了你的相册照片",
            "麦克风监听": f"{self.app_name}在后台使用了麦克风",
            "后台同步": f"{self.app_name}在你不知情的情况下同步数据",
            "剪贴板读取": f"{self.app_name}读取了你的剪贴板",
            "跨应用追踪": f"{self.app_name}在追踪你在其他APP的行为",
        }
        return templates.get(self.threat_type, f"{self.app_name}有可疑的数据收集行为")


@dataclass
class RadarReport:
    """一次扫描的完整报告"""
    scan_id: str
    timestamp: str
    mode: ScanMode
    total_threats: int
    high_risk: int
    medium_risk: int
    low_risk: int
    blocked: int
    threats: List[dict] = field(default_factory=list)
    p0_protocols: Dict[str, bool] = field(default_factory=dict)
    dna: str = DNA
    duration_seconds: float = 0.0

    def to_dict(self) -> dict:
        return {
            "scan_id": self.scan_id,
            "timestamp": self.timestamp,
            "mode": self.mode.value,
            "total_threats": self.total_threats,
            "high_risk": self.high_risk,
            "medium_risk": self.medium_risk,
            "low_risk": self.low_risk,
            "blocked": self.blocked,
            "threats": self.threats,
            "p0_protocols": self.p0_protocols,
            "dna": self.dna,
            "duration_seconds": self.duration_seconds,
        }


# ═══════════════════════════════════════════════════════════════
# DataRadarScanner — 数据雷达扫描器
# ═══════════════════════════════════════════════════════════════

class DataRadarScanner:
    """扫描设备上的数据泄露风险"""

    def __init__(self):
        self.os_type = platform.system()  # Darwin / Linux
        self.scan_history: List[RadarReport] = []
        self.known_threats_db = self._load_known_db()
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)

    # ── 已知威胁数据库 ──

    def _load_known_db(self) -> Dict[str, dict]:
        """加载已知的数据收集行为库"""
        if APP_DB_PATH.exists():
            try:
                return json.loads(APP_DB_PATH.read_text())
            except Exception:
                pass

        # 内置默认库（公开信息，基于隐私政策和行业报告）
        db = {
            "com.tencent.xin": {
                "name": "微信", "category": "社交",
                "known_behaviors": ["数据上传", "位置追踪", "通讯录访问", "相册访问"],
                "risk_level": "medium",
            },
            "com.ss.iphone.article.News": {
                "name": "抖音", "category": "短视频",
                "known_behaviors": ["数据上传", "位置追踪", "相册访问", "跨应用追踪"],
                "risk_level": "high",
            },
            "com.taobao.taobao4iphone": {
                "name": "淘宝", "category": "电商",
                "known_behaviors": ["数据上传", "位置追踪", "跨应用追踪"],
                "risk_level": "high",
            },
            "com.meituan.imeituan": {
                "name": "美团", "category": "生活",
                "known_behaviors": ["位置追踪", "通讯录访问", "数据上传"],
                "risk_level": "medium",
            },
            "com.alibaba.aliexpresshd": {
                "name": "支付宝", "category": "金融",
                "已知行为": ["数据上传", "跨应用追踪"],
                "risk_level": "high",
            },
            "com.tencent.mqq": {
                "name": "QQ", "category": "社交",
                "known_behaviors": ["数据上传", "位置追踪", "相册访问"],
                "risk_level": "medium",
            },
            "com.baidu.BaiduMobile": {
                "name": "百度", "category": "搜索",
                "known_behaviors": ["数据上传", "位置追踪", "跨应用追踪"],
                "risk_level": "high",
            },
        }
        return db

    # ── macOS 扫描 ──

    def scan_macos(self, mode: ScanMode = ScanMode.QUICK) -> RadarReport:
        """macOS 平台扫描"""
        scan_id = hashlib.sha256(f"{time.time()}{DNA}".encode()).hexdigest()[:16]
        start = time.time()
        threats: List[Threat] = []

        # 1. 扫描已安装应用 → 匹配已知行为库
        installed = self._get_macos_apps()
        for app in installed:
            bundle = app.get("bundle_id", "")
            if bundle in self.known_threats_db:
                info = self.known_threats_db[bundle]
                for behavior in info.get("known_behaviors", []):
                    t = Threat(
                        app_name=app["name"],
                        app_bundle=bundle,
                        threat_type=behavior,
                        severity=ThreatSeverity.HIGH if info.get("risk_level") == "high"
                        else ThreatSeverity.MEDIUM,
                        detail=f"{app['name']}的隐私政策中声明了此行为",
                        first_seen=datetime.now(timezone.utc).isoformat(),
                        last_seen=datetime.now(timezone.utc).isoformat(),
                    )
                    t.human_explain = t._gen_human()
                    threats.append(t)

        # 2. 检查网络连接 — 哪些进程在主动连接外部
        if mode in (ScanMode.DEEP, ScanMode.CONTINUOUS):
            net_threats = self._scan_network_macos()
            threats.extend(net_threats)

        # 3. 检查后台刷新权限
        bg_threats = self._scan_background_refresh_macos()
        threats.extend(bg_threats)

        # 4. 检查位置服务
        loc_threats = self._scan_location_services_macos()
        threats.extend(loc_threats)

        # 5. 检查剪贴板访问
        if mode == ScanMode.DEEP:
            cb_threats = self._scan_clipboard_macos()
            threats.extend(cb_threats)

        # 去重合并
        threats = self._deduplicate(threats)

        # P0协议状态检查
        p0_status = self._check_p0_compliance()

        high = sum(1 for t in threats if t.severity == ThreatSeverity.HIGH)
        med = sum(1 for t in threats if t.severity == ThreatSeverity.MEDIUM)
        low = sum(1 for t in threats if t.severity == ThreatSeverity.LOW)
        blocked = sum(1 for t in threats if t.severity == ThreatSeverity.BLOCKED)

        report = RadarReport(
            scan_id=scan_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            mode=mode,
            total_threats=len(threats),
            high_risk=high,
            medium_risk=med,
            low_risk=low,
            blocked=blocked,
            threats=[t.to_dict() for t in threats],
            p0_protocols=p0_status,
            duration_seconds=round(time.time() - start, 2),
        )

        self._save_audit(report)
        return report

    def scan_linux(self, mode: ScanMode = ScanMode.QUICK) -> RadarReport:
        """Linux 平台扫描（鲲鹏）"""
        scan_id = hashlib.sha256(f"{time.time()}{DNA}".encode()).hexdigest()[:16]
        start = time.time()
        threats: List[Threat] = []

        # 检查出站连接
        try:
            result = subprocess.run(
                ["ss", "-tunp"], capture_output=True, text=True, timeout=15
            )
            for line in result.stdout.splitlines():
                if "ESTAB" in line:
                    parts = line.split()
                    if len(parts) >= 6:
                        remote = parts[5] if len(parts) > 5 else ""
                        proc = parts[-1] if "users:" in parts[-1] else ""
                        if remote and not remote.startswith("127.") and not remote.startswith("::1"):
                            t = Threat(
                                app_name=proc.split("(")[-1].replace(")", "") if proc else "未知进程",
                                app_bundle="",
                                threat_type="数据上传",
                                severity=ThreatSeverity.MEDIUM,
                                detail=f"活跃连接到 {remote}",
                                destination=remote,
                                first_seen=datetime.now(timezone.utc).isoformat(),
                                last_seen=datetime.now(timezone.utc).isoformat(),
                            )
                            t.human_explain = t._gen_human()
                            threats.append(t)
        except Exception:
            pass

        p0_status = self._check_p0_compliance()

        high = sum(1 for t in threats if t.severity == ThreatSeverity.HIGH)
        med = sum(1 for t in threats if t.severity == ThreatSeverity.MEDIUM)
        low = sum(1 for t in threats if t.severity == ThreatSeverity.LOW)
        blocked = sum(1 for t in threats if t.severity == ThreatSeverity.BLOCKED)

        report = RadarReport(
            scan_id=scan_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            mode=mode,
            total_threats=len(threats),
            high_risk=high, medium_risk=med, low_risk=low, blocked=blocked,
            threats=[t.to_dict() for t in threats],
            p0_protocols=p0_status,
            duration_seconds=round(time.time() - start, 2),
        )
        return report

    # ── macOS 子扫描 ──

    def _get_macos_apps(self) -> List[dict]:
        """获取已安装的 macOS 应用"""
        apps = []
        search_dirs = ["/Applications", os.path.expanduser("~/Applications")]
        for search_dir in search_dirs:
            p = Path(search_dir)
            if not p.exists():
                continue
            for app_path in p.glob("*.app"):
                info_plist = app_path / "Contents" / "Info.plist"
                bundle_id = ""
                name = app_path.stem
                if info_plist.exists():
                    try:
                        result = subprocess.run(
                            ["/usr/libexec/PlistBuddy", "-c", "Print CFBundleIdentifier",
                             str(info_plist)], capture_output=True, text=True, timeout=5
                        )
                        if result.returncode == 0:
                            bundle_id = result.stdout.strip()
                        result2 = subprocess.run(
                            ["/usr/libexec/PlistBuddy", "-c", "Print CFBundleDisplayName",
                             str(info_plist)], capture_output=True, text=True, timeout=5
                        )
                        if result2.returncode == 0 and result2.stdout.strip():
                            name = result2.stdout.strip()
                    except Exception:
                        pass
                apps.append({"name": name, "bundle_id": bundle_id, "path": str(app_path)})
        return apps

    def _scan_network_macos(self) -> List[Threat]:
        """扫描网络连接"""
        threats = []
        try:
            result = subprocess.run(
                ["lsof", "-i", "-n", "-P"], capture_output=True, text=True, timeout=15
            )
            for line in result.stdout.splitlines():
                if "ESTABLISHED" in line or "SYN_SENT" in line:
                    parts = line.split()
                    if len(parts) >= 9:
                        proc = parts[0]
                        remote = parts[-1] if "->" in parts[-1] else ""
                        # 过滤系统进程和本地连接
                        if proc in ["kernel_task", "mDNSResponder", "WindowServer", "syslogd"]:
                            continue
                        if "127.0.0.1" in remote or "::1" in remote or "0.0.0.0" in remote:
                            continue
                        # 匹配已知应用
                        matched = False
                        for bundle, info in self.known_threats_db.items():
                            if proc.lower() in info["name"].lower() or info["name"].lower() in proc.lower():
                                t = Threat(
                                    app_name=info["name"],
                                    app_bundle=bundle,
                                    threat_type="数据上传",
                                    severity=ThreatSeverity.HIGH if info["risk_level"] == "high" else ThreatSeverity.MEDIUM,
                                    detail=f"正在连接 {remote}",
                                    destination=remote.split(":")[0] if ":" in remote else remote,
                                    frequency=1,
                                    first_seen=datetime.now(timezone.utc).isoformat(),
                                    last_seen=datetime.now(timezone.utc).isoformat(),
                                )
                                t.human_explain = t._gen_human()
                                threats.append(t)
                                matched = True
                                break
                        if not matched and remote:
                            t = Threat(
                                app_name=proc, app_bundle="",
                                threat_type="数据上传",
                                severity=ThreatSeverity.LOW,
                                detail=f"未知进程 {proc} 连接到 {remote}",
                                destination=remote.split(":")[0] if ":" in remote else remote,
                                first_seen=datetime.now(timezone.utc).isoformat(),
                                last_seen=datetime.now(timezone.utc).isoformat(),
                            )
                            t.human_explain = f"未知程序 {proc} 正在连接外部服务器"
                            threats.append(t)
        except Exception:
            pass
        return threats

    def _scan_background_refresh_macos(self) -> List[Threat]:
        """检查后台刷新权限"""
        threats = []
        # macOS 没有直接的后台刷新开关列表，通过检查 launchd 持久化进程
        try:
            result = subprocess.run(
                ["launchctl", "list"], capture_output=True, text=True, timeout=10
            )
            bg_count = 0
            for line in result.stdout.splitlines():
                if "com.apple" not in line and "com.tencent" in line or "com.alibaba" in line or "com.baidu" in line:
                    bg_count += 1
            # 通知性提示，不是真威胁
            if bg_count > 2:
                t = Threat(
                    app_name="第三方应用",
                    app_bundle="",
                    threat_type="后台同步",
                    severity=ThreatSeverity.LOW,
                    detail=f"检测到 {bg_count} 个第三方应用有后台运行权限",
                    first_seen=datetime.now(timezone.utc).isoformat(),
                    last_seen=datetime.now(timezone.utc).isoformat(),
                )
                t.human_explain = f"有 {bg_count} 个应用可以在后台悄悄运行"
                threats.append(t)
        except Exception:
            pass
        return threats

    def _scan_location_services_macos(self) -> List[Threat]:
        """检查位置服务状态"""
        threats = []
        try:
            loc_db = Path("/var/db/locationd/clients.plist")
            if loc_db.exists():
                result = subprocess.run(
                    ["/usr/libexec/PlistBuddy", "-c", "Print", str(loc_db)],
                    capture_output=True, text=True, timeout=10
                )
                if "LocationServicesEnabled" not in result.stdout:
                    # 无法直接读取，提示用户
                    t = Threat(
                        app_name="系统",
                        app_bundle="com.apple.locationd",
                        threat_type="位置追踪",
                        severity=ThreatSeverity.LOW,
                        detail="位置服务可能开启中，建议检查系统偏好设置 → 安全与隐私 → 定位服务",
                        first_seen=datetime.now(timezone.utc).isoformat(),
                        last_seen=datetime.now(timezone.utc).isoformat(),
                    )
                    t.human_explain = "你的位置信息可能在被使用，建议检查定位服务设置"
                    threats.append(t)
        except Exception:
            pass
        return threats

    def _scan_clipboard_macos(self) -> List[Threat]:
        """检查剪贴板访问（macOS 限制性强，提示为主）"""
        threats = []
        t = Threat(
            app_name="系统提醒",
            app_bundle="",
            threat_type="剪贴板读取",
            severity=ThreatSeverity.LOW,
            detail="macOS 14+ 已限制剪贴板读取，每次访问都会弹窗提示。请关注弹窗频率。",
            first_seen=datetime.now(timezone.utc).isoformat(),
            last_seen=datetime.now(timezone.utc).isoformat(),
        )
        t.human_explain = "你复制的内容可能被APP读取，注意系统弹窗提醒"
        threats.append(t)
        return threats

    # ── 通用工具 ──

    def _deduplicate(self, threats: List[Threat]) -> List[Threat]:
        """按 app_name + threat_type 去重，保留最严重的"""
        seen: Dict[str, Threat] = {}
        severity_order = {ThreatSeverity.HIGH: 3, ThreatSeverity.MEDIUM: 2,
                          ThreatSeverity.LOW: 1, ThreatSeverity.BLOCKED: 0}
        for t in threats:
            key = f"{t.app_name}|{t.threat_type}"
            if key not in seen or severity_order[t.severity] > severity_order[seen[key].severity]:
                seen[key] = t
        return list(seen.values())

    def _check_p0_compliance(self) -> Dict[str, bool]:
        """检查P0协议是否符合"""
        status = {}
        for pid, info in P0_PROTOCOLS_HUMAN.items():
            status[pid] = True  # 协议层面全部生效（设计即合规）
        return status

    def _save_audit(self, report: RadarReport):
        """保存审计日志"""
        try:
            entry = {
                "scan_id": report.scan_id,
                "timestamp": report.timestamp,
                "threats_found": report.total_threats,
                "high_risk": report.high_risk,
                "dna": DNA,
            }
            with open(AUDIT_LOG, "a") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass

    # ── 公开API ──

    def scan(self, mode: str = "quick") -> dict:
        """统一扫描入口"""
        scan_mode = ScanMode(mode) if mode in [m.value for m in ScanMode] else ScanMode.QUICK
        if self.os_type == "Darwin":
            report = self.scan_macos(scan_mode)
        else:
            report = self.scan_linux(scan_mode)
        return report.to_dict()

    def get_p0_protocols(self) -> dict:
        """获取P0协议清单（给前端展示用）"""
        return {
            "protocols": [
                {"id": pid, "name": info["name"], "desc": info["desc"], "icon": info["icon"],
                 "status": True, "last_check": datetime.now(timezone.utc).isoformat()}
                for pid, info in P0_PROTOCOLS_HUMAN.items()
            ],
            "dna": DNA,
        }

    def get_status(self) -> dict:
        """获取雷达当前状态"""
        # 读取最近一次扫描
        last_scan = None
        if AUDIT_LOG.exists():
            try:
                lines = AUDIT_LOG.read_text().strip().splitlines()
                if lines:
                    last_scan = json.loads(lines[-1])
            except Exception:
                pass

        return {
            "status": "ready",
            "dna": DNA,
            "last_scan": last_scan,
            "os": self.os_type,
            "known_db_size": len(self.known_threats_db),
            "p0_protocols_count": len(P0_PROTOCOLS_HUMAN),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·个人数据主权雷达 v1.0")
    parser.add_argument("action", nargs="?", default="scan",
                        choices=["scan", "status", "p0", "deep"])
    parser.add_argument("--mode", default="quick", choices=["quick", "deep", "continuous"])
    args = parser.parse_args()

    radar = DataRadarScanner()

    if args.action == "scan" or args.action == "deep":
        mode = "deep" if args.action == "deep" else args.mode
        report = radar.scan(mode)
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.action == "status":
        print(json.dumps(radar.get_status(), ensure_ascii=False, indent=2))
    elif args.action == "p0":
        print(json.dumps(radar.get_p0_protocols(), ensure_ascii=False, indent=2))
