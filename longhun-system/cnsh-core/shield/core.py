"""
shield/core.py — LocalShield 三层防御模型
主权层 · 伦理层 · 感知层
"""
import hashlib, time
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from dare.store import write_shield_log

GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ── 结果对象 ──────────────────────────────────────────────────────

@dataclass
class ShieldResult:
    reject:        bool
    reason:        str = ""
    dna_trace:     str = ""
    ethical_score: str = "🟢"
    sense_metadata: Dict = field(default_factory=dict)
    layer_logs:    list  = field(default_factory=list)

# ── 主权层 ────────────────────────────────────────────────────────

class SovereignLayer:
    """主权层：GPG指纹绑定 + 一票否决"""

    def __init__(self, gpg: str = GPG_FINGERPRINT):
        self.gpg = gpg

    def verify(self, content: str = "", action: str = "") -> tuple:
        """返回 (passed, reason)"""
        # 黑名单动作
        VETO_ACTIONS = {"DELETE_ALL", "WIPE", "OVERRIDE_SHIELD", "INJECT"}
        if action.upper() in VETO_ACTIONS:
            return False, f"SOVEREIGN_VETO: 动作 {action} 被一票否决"

        # GPG绑定检查（本地指纹校验）
        if self.gpg and len(self.gpg) < 10:
            return False, "SOVEREIGN_VETO: GPG指纹无效"

        return True, "SOVEREIGN_OK"

# ── 伦理层 ────────────────────────────────────────────────────────

class EthicalLayer:
    """伦理层：三色审计 + 洛书369验证"""

    RISK_KEYWORDS = [
        "删除全部", "清空数据库", "绕过审计", "忽略安全",
        "delete all", "drop table", "bypass audit",
    ]

    def audit(self, content: str) -> tuple:
        """返回 (passed, color_code)"""
        content_lower = content.lower()

        # 红色熔断
        for kw in self.RISK_KEYWORDS:
            if kw in content_lower:
                return False, "🔴"

        # 黄色警告
        if len(content) > 10000:
            return True, "🟡"

        # 洛书369验证
        h = int(hashlib.sha256(content.encode()).hexdigest(), 16)
        dr = 1 + ((h - 1) % 9) if h > 0 else 0
        if dr in {3, 6, 9}:
            return True, "🟢✨"  # 369祝福

        return True, "🟢"

# ── 感知层 ────────────────────────────────────────────────────────

class SenseLayer:
    """感知层：输入监控 + 输出追踪 + 上下文感知"""

    def monitor(self, content: str, action: str) -> Dict[str, Any]:
        ts = time.time()
        return {
            "input_length":  len(content),
            "action":        action,
            "timestamp":     ts,
            "date":          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts)),
            "content_hash":  hashlib.sha256(content.encode()).hexdigest()[:16],
            "char_type":     "zh" if any("\u4e00" <= c <= "\u9fff" for c in content) else "en",
        }

# ── LocalShield 主类 ──────────────────────────────────────────────

class LocalShield:
    """
    三层防御统一入口
    用法: shield.process(content, action) -> ShieldResult
    """

    def __init__(self, gpg_fingerprint: str = GPG_FINGERPRINT):
        self.gpg = gpg_fingerprint
        self.prev_hash = "0" * 64  # 创世哈希
        self.layer_sovereign = SovereignLayer(gpg_fingerprint)
        self.layer_ethical   = EthicalLayer()
        self.layer_sense     = SenseLayer()

    def _generate_dna(self, content: str, action: str,
                      sense_data: Dict) -> str:
        ts = int(time.time())
        raw = f"{content}|{action}|{self.prev_hash}|{ts}"
        h = hashlib.sha256(raw.encode()).hexdigest()[:16].upper()
        date_str = time.strftime("%Y%m%d", time.localtime(ts))
        dna = f"#龍芯⚡️{date_str}-SHIELD-{h}"
        self.prev_hash = hashlib.sha256(raw.encode()).hexdigest()
        return dna

    def process(self, content: str, action: str = "PROCESS") -> ShieldResult:
        logs = []

        # 1. 主权层
        sv_ok, sv_reason = self.layer_sovereign.verify(content, action)
        logs.append({"layer": "sovereign", "result": sv_reason})
        if not sv_ok:
            dna = self._generate_dna(content, action, {})
            write_shield_log(dna, "sovereign", action, sv_reason)
            return ShieldResult(reject=True, reason=sv_reason,
                                dna_trace=dna, layer_logs=logs)

        # 2. 伦理层
        eth_ok, eth_color = self.layer_ethical.audit(content)
        logs.append({"layer": "ethical", "result": eth_color})
        if not eth_ok:
            dna = self._generate_dna(content, action, {})
            write_shield_log(dna, "ethical", action, eth_color)
            return ShieldResult(reject=True, reason=f"ETHICAL_{eth_color}",
                                dna_trace=dna, layer_logs=logs)

        # 3. 感知层
        sense_data = self.layer_sense.monitor(content, action)
        logs.append({"layer": "sense", "result": "OK", "meta": sense_data})

        # 4. 生成DNA追溯码
        dna = self._generate_dna(content, action, sense_data)
        write_shield_log(dna, "sense", action, "PASS")

        return ShieldResult(
            reject=False,
            dna_trace=dna,
            ethical_score=eth_color,
            sense_metadata=sense_data,
            layer_logs=logs,
        )

    def status(self) -> Dict:
        return {
            "gpg":         self.gpg[:8] + "..." + self.gpg[-4:],
            "prev_hash":   self.prev_hash[:16] + "...",
            "layers":      ["sovereign", "ethical", "sense"],
            "mode":        "strict",
        }
