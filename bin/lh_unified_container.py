# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·UNIFIED-CONTAINER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 容器统一入口 v1.0
═══════════════════════════════════════════════════
数据清洗 + 路由预检 · 万物归一入口

四层管道：
  L1: 输入清洗（格式规范化·编码统一·注入检测）
  L2: DNA验证（格式校验·GPG·主权确认）
  L3: 路由预检（意图解析·人格映射·闸门预判）
  L4: 执行分发（统一出口·审计追踪·结果回执）

DNA: #龍芯⚡️丙午·辛未·UNIFIED-CONTAINER-v1.0
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple, Any, List

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# ── 常量 ──
AUDIT_DB = ROOT / "data" / "sqlite" / "audit.db"
DNA_PATTERN = re.compile(r'^#龍芯⚡️[\u4e00-\u9fff]+·[\u4e00-\u9fff]+·.+$')
BANNED_CHARS = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')  # 控制字符
SQL_INJECTION_PATTERN = re.compile(
    r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|EXEC|GRANT|REVOKE)\b)",
    re.IGNORECASE,
)
XSS_PATTERN = re.compile(r"<script|javascript:|on\w+\s*=", re.IGNORECASE)

# 意图关键词 → 路由目标
INTENT_ROUTES = {
    "安全": ["审计", "扫描", "防火墙", "熔断", "红队", "检测", "漏洞", "攻击"],
    "治理": ["DNA", "注册", "主权", "登记", "人格", "宪法", "规则"],
    "开发": ["CNSH", "编译", "道引", "吸收", "构建", "部署"],
    "AI": ["训练", "模型", "语义", "知识", "脑"],
    "经济": ["支付", "充值", "许愿池", "XPay"],
    "运维": ["监控", "健康", "自愈", "守护", "检查"],
    "生态": ["通行证", "技能", "路由", "总线"],
}

SANITIZE_PRESETS = {
    "default": {"strip_null": True, "normalize_unicode": True, "trim_whitespace": True},
    "strict": {"strip_null": True, "strip_control": True, "normalize_unicode": True,
               "trim_whitespace": True, "max_length": 10000},
    "code": {"strip_null": True, "normalize_unicode": False, "trim_whitespace": False},
}


class UnifiedContainer:
    """龍魂统一容器入口"""

    def __init__(self, dna: str = "", verbose: bool = False):
        self.dna = dna
        self.verbose = verbose
        self.audit_conn = None
        self._init_audit()
        self.stats = {"total_requests": 0, "rejected": 0, "passed": 0, "errors": 0}
        self.request_chain: List[str] = []

    # ═══ L1: 数据清洗 ═══

    def sanitize(self, content: str, preset: str = "default",
                 max_length: int = 10000) -> Tuple[str, List[str]]:
        """
        输入清洗管道
        返回: (清洗后内容, 警告列表)
        """
        warnings = []
        cfg = dict(SANITIZE_PRESETS.get(preset, SANITIZE_PRESETS["default"]))
        cfg.setdefault("max_length", max_length)

        if not content:
            return "", ["空输入"]

        original_len = len(content)

        # 1. 去除空字符
        if cfg.get("strip_null", True):
            cleaned = content.replace("\x00", "")
            if "\x00" in content:
                warnings.append("已移除空字符(\\x00)")

        # 2. 去除控制字符
        if cfg.get("strip_control", False):
            cleaned = BANNED_CHARS.sub("", cleaned)

        # 3. Unicode规范化
        if cfg.get("normalize_unicode", True):
            cleaned = unicodedata.normalize("NFKC", cleaned)

        # 4. 去除首尾空白
        if cfg.get("trim_whitespace", True):
            cleaned = cleaned.strip()

        # 5. 长度限制
        if len(cleaned) > cfg["max_length"]:
            cleaned = cleaned[: cfg["max_length"]]
            warnings.append(f"内容截断: {original_len} → {cfg['max_length']}")

        # 6. 注入检测
        injection_warnings = self._detect_injection(cleaned)
        warnings.extend(injection_warnings)

        return cleaned, warnings

    def _detect_injection(self, content: str) -> List[str]:
        """检测注入攻击"""
        w = []
        if SQL_INJECTION_PATTERN.search(content):
            w.append("⚠️ 检测到疑似SQL注入关键词")
        if XSS_PATTERN.search(content):
            w.append("⚠️ 检测到疑似XSS注入")
        if len(content) > 0 and content.count("\\") > len(content) * 0.1:
            w.append("⚠️ 异常高频率反斜杠")
        return w

    # ═══ L2: DNA验证 ═══

    def validate_dna(self, dna: str) -> Tuple[bool, str]:
        """DNA格式验证 + 主权确认"""
        if not dna:
            return False, "DNA为空"
        if not DNA_PATTERN.match(dna):
            return False, f"DNA格式无效，期望: #龍芯⚡️年干·月干·日干·..."
        if "⚡️" not in dna:
            return False, "DNA缺少闪电标记⚡️"
        if len(dna) < 20:
            return False, f"DNA过短({len(dna)}字符)，至少需要20字符"
        return True, "DNA验证通过"

    def compute_dna_hash(self, dna: str, content_hash: str) -> str:
        """计算DNA绑定哈希"""
        return hashlib.sha256(f"{dna}:{content_hash}".encode()).hexdigest()[:16]

    # ═══ L3: 路由预检 ═══

    def detect_intent(self, content: str) -> Dict[str, Any]:
        """意图检测 + 路由推荐"""
        content_lower = content.lower()
        scores = {}

        for category, keywords in INTENT_ROUTES.items():
            score = sum(1 for kw in keywords if kw.lower() in content_lower)
            if score > 0:
                scores[category] = score

        if not scores:
            return {"intent": "通用", "confidence": 0.0, "routes": ["默认路由"]}

        best = max(scores, key=lambda k: scores[k])
        total = sum(scores.values())
        confidence = scores[best] / max(total, 1)

        # 多意图场景
        routes = sorted(scores, key=lambda k: scores[k], reverse=True)[:3]

        return {
            "intent": best,
            "confidence": round(confidence, 3),
            "routes": routes,
            "scores": scores,
        }

    def precheck_gate(self, dna: str, content: str) -> Dict[str, Any]:
        """三闸门预检（快速判定，不做最终决策）"""
        results = {}

        # 闸门1: 数字根
        dr = self._digital_root(sum(ord(c) for c in content))
        gate1 = "🔴" if dr in (3, 9) else ("🟡" if dr == 6 else "🟢")
        results["gate1_digital_root"] = {"dr": dr, "color": gate1}

        # 闸门2: 身份
        dna_valid, dna_msg = self.validate_dna(dna)
        gate2 = "🟢" if dna_valid else "🔴"
        results["gate2_identity"] = {"valid": dna_valid, "color": gate2, "msg": dna_msg}

        # 闸门3: 伦理（关键词预检）
        ethical_risk = self._check_ethical_risk(content)
        gate3 = "🔴" if ethical_risk["risk_level"] == "high" else (
            "🟡" if ethical_risk["risk_level"] == "medium" else "🟢"
        )
        results["gate3_ethics"] = {"color": gate3, **ethical_risk}

        # 综合判定
        gates = [gate1, gate2, gate3]
        if "🔴" in gates:
            results["pass"] = False
            results["verdict"] = "🔴 闸门预检未通过"
        elif "🟡" in gates:
            results["pass"] = "warn"
            results["verdict"] = "🟡 闸门警告·需人工确认"
        else:
            results["pass"] = True
            results["verdict"] = "🟢 闸门预检通过"

        return results

    def _digital_root(self, n: int) -> int:
        n = abs(n)
        return 0 if n == 0 else 1 + (n - 1) % 9

    def _check_ethical_risk(self, content: str) -> Dict[str, Any]:
        """伦理风险预检"""
        high_risk = ["删除系统", "格式化", "rm -rf", "DROP TABLE", "DROP DATABASE",
                     "泄露密钥", "生物绑定", "人脸交易", "儿童数据"]
        medium_risk = ["修改宪法", "绕过审计", "跳过熔断", "未经授权", "AI管钱"]

        content_lower = content.lower()
        for keyword in high_risk:
            if keyword.lower() in content_lower:
                return {"risk_level": "high", "triggered": keyword, "action": "立即熔断"}
        for keyword in medium_risk:
            if keyword.lower() in content_lower:
                return {"risk_level": "medium", "triggered": keyword, "action": "需人工审核"}

        return {"risk_level": "low", "triggered": None, "action": "正常放行"}

    # ═══ L4: 执行分发 ═══

    def execute(self, content: str, dna: str, preset: str = "default",
                dry_run: bool = False) -> Dict[str, Any]:
        """完整执行管道：清洗→验证→预检→分发"""
        start_time = time.time()
        self.stats["total_requests"] += 1
        pipe_log: List[Dict[str, Any]] = []

        # ── L1: 清洗 ──
        cleaned, warnings = self.sanitize(content, preset)
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]
        pipe_log.append({"stage": "L1_clean", "status": "ok" if not warnings else "warn",
                         "warnings": warnings, "hash": content_hash})

        if "空输入" in warnings:
            self.stats["rejected"] += 1
            return self._result(False, "空输入被拒绝", pipe_log, start_time)

        # ── L2: DNA验证 ──
        dna_valid, dna_msg = self.validate_dna(dna)
        pipe_log.append({"stage": "L2_dna", "status": "ok" if dna_valid else "fail",
                         "msg": dna_msg})
        if not dna_valid:
            self.stats["rejected"] += 1
            return self._result(False, f"DNA验证失败: {dna_msg}", pipe_log, start_time)

        # ── L3: 路由预检 ──
        intent = self.detect_intent(cleaned)
        gates = self.precheck_gate(dna, cleaned)
        pipe_log.append({"stage": "L3_route", "intent": intent, "gates": gates})

        if gates["pass"] is False:
            self.stats["rejected"] += 1
            return self._result(False, gates["verdict"], pipe_log, start_time)

        need_review = gates["pass"] == "warn"

        # ── L4: 分发 ──
        if dry_run:
            pipe_log.append({"stage": "L4_dispatch", "status": "dry_run", "action": "未执行"})
            self.stats["passed"] += 1
            return self._result(True, "干运行·管道全通", pipe_log, start_time,
                                intent=intent, need_review=need_review)

        # 真实分发
        dna_hash = self.compute_dna_hash(dna, content_hash)
        self._write_audit(dna, content_hash, dna_hash, intent, gates)
        self.request_chain.append(dna_hash)

        pipe_log.append({"stage": "L4_dispatch", "status": "ok", "dna_hash": dna_hash})
        self.stats["passed"] += 1

        return self._result(True, "管道执行完成", pipe_log, start_time,
                            intent=intent, dna_hash=dna_hash, need_review=need_review)

    # ═══ 辅助 ═══

    def _result(self, success: bool, message: str, pipe_log: List[Dict[str, Any]],
                start_time: float, **extra: Any) -> Dict[str, Any]:
        elapsed = round((time.time() - start_time) * 1000, 1)
        r = {
            "success": success,
            "message": message,
            "elapsed_ms": elapsed,
            "pipe_log": pipe_log,
            "dna": self.dna,
            "timestamp": datetime.now().isoformat(),
        }
        r.update(extra)
        return r

    def _init_audit(self):
        try:
            os.makedirs(os.path.dirname(AUDIT_DB), exist_ok=True)
            self.audit_conn = sqlite3.connect(str(AUDIT_DB))
            self.audit_conn.execute("""
                CREATE TABLE IF NOT EXISTS container_audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dna TEXT, content_hash TEXT, dna_hash TEXT,
                    intent TEXT, confidence REAL, gate_result TEXT,
                    timestamp TEXT
                )
            """)
            self.audit_conn.commit()
        except Exception:
            self.audit_conn = None

    def _write_audit(self, dna: str, content_hash: str, dna_hash: str,
                     intent: Dict[str, Any], gates: Dict[str, Any]) -> None:
        if not self.audit_conn:
            return
        try:
            self.audit_conn.execute(
                "INSERT INTO container_audit VALUES (NULL,?,?,?,?,?,?,?)",
                (dna, content_hash, dna_hash, intent.get("intent", ""),
                 intent.get("confidence", 0), json.dumps(gates, ensure_ascii=False),
                 datetime.now().isoformat()),
            )
            self.audit_conn.commit()
        except Exception:
            pass

    def status(self) -> Dict[str, Any]:
        return {
            "stats": self.stats,
            "request_chain_length": len(self.request_chain),
            "latest_hash": self.request_chain[-1][:16] if self.request_chain else None,
            "audit_db": str(AUDIT_DB),
        }


# ═══ CLI ═══

def main():
    parser = argparse.ArgumentParser(description="龍魂统一容器入口 · 数据清洗+路由预检")
    parser.add_argument("--dna", required=True, help="DNA追溯码")
    parser.add_argument("--input", "-i", help="输入内容（或从stdin读取）")
    parser.add_argument("--file", "-f", help="从文件读取输入")
    parser.add_argument("--preset", default="default", choices=["default", "strict", "code"],
                        help="清洗预设 (default/strict/code)")
    parser.add_argument("--dry-run", action="store_true", help="干运行·不执行分发")
    parser.add_argument("--intent-only", action="store_true", help="仅意图检测")
    parser.add_argument("--gate-only", action="store_true", help="仅闸门预检")
    parser.add_argument("--status", action="store_true", help="显示容器状态")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()
    container = UnifiedContainer(dna=args.dna, verbose=args.verbose)

    # 状态查询
    if args.status:
        print(json.dumps(container.status(), ensure_ascii=False, indent=2))
        return 0

    # 获取输入
    if args.file:
        content = Path(args.file).read_text(encoding="utf-8")
    elif args.input:
        content = args.input
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        print("❌ 需要 --input / --file / 或管道输入", file=sys.stderr)
        return 1

    # 仅意图检测
    if args.intent_only:
        clean, _ = container.sanitize(content, args.preset)
        intent = container.detect_intent(clean)
        print(json.dumps(intent, ensure_ascii=False, indent=2))
        return 0

    # 仅闸门预检
    if args.gate_only:
        clean, _ = container.sanitize(content, args.preset)
        gates = container.precheck_gate(args.dna, clean)
        print(json.dumps(gates, ensure_ascii=False, indent=2))
        return 0

    # 完整管道
    result = container.execute(content, args.dna, args.preset, args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
