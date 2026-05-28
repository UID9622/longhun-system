"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
longhun_logger.py  —  龍魂統一日志系統·DNA追蹤·三色審計
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copyright © 2026 UID9622 諸葛鑫（龍芯北辰）
Licensed under the Apache License, Version 2.0

作者：UID9622 諸葛鑫（龍芯北辰）
創作地：中華人民共和國
GPG指紋：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理論指導：曾仕強老師（永恆顯示）
DNA追蹤碼：#龍芯⚡️2026-05-28-LONGHUN-LOGGER-v1.0
確認碼：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

共建致謝：
  Claude (Anthropic PBC) · 技術協作與代碼共創
  Notion · 知識底座與結構化存儲
  沒有你們，就沒有龍魂系統的一切。

獻禮：新中國成立77週年（1949-2026）· 丙午馬年

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

統一日志系統，提供：
  ✅ DNA追蹤：每條日志自動生成DNA追蹤碼
  ✅ 三色審計：自動計算dr值，分類為🟢🟡🔴
  ✅ JSONL輸出：機器可讀的結構化日志
  ✅ 控制台友好：人工可讀的彩色輸出
  ✅ 系統集成：與龍魂現有審計基礎設施無縫協作

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Any, Dict
from zoneinfo import ZoneInfo


# ─────────────────────────────────────────────────────────
# DNA 追蹤碼生成
# ─────────────────────────────────────────────────────────

def generate_dna(
    module: str,
    content: str = "",
    version: str = "v1.0"
) -> str:
    """
    生成龍魂DNA追蹤碼。

    格式：#龍芯⚡️{YYYY-MM-DD}-{MODULE}-{version}-{hash6}

    Args:
        module: 模塊名稱（e.g., "LOGGER", "AUDIT-CHECK"）
        content: 內容文本（用於生成哈希）
        version: 版本號（e.g., "v1.0"）

    Returns:
        DNA追蹤碼字符串
    """
    # 獲取北京時區當前時間
    beijing_tz = ZoneInfo("Asia/Shanghai")
    now = datetime.now(beijing_tz)

    # 組合內容以生成哈希
    hash_input = f"{module}{content}{now.isoformat()}".encode("utf-8")
    hash_hex = hashlib.sha256(hash_input).hexdigest()[:6].upper()

    # 構造DNA字符串
    date_str = now.strftime("%Y-%m-%d")
    dna = f"#龍芯⚡️{date_str}-{module}-{version}-{hash_hex}"

    return dna


# ─────────────────────────────────────────────────────────
# 三色審計·dr值計算與分類
# ─────────────────────────────────────────────────────────

def calculate_dr(content: str) -> int:
    """
    計算數字根(Digital Root)。
    用於龍魂三色審計分類。

    dr = (content_hash % 256) % 9 + 1
    結果範圍：1-9

    Args:
        content: 待審計內容

    Returns:
        dr值（1-9）
    """
    if not content:
        return 5  # 默認中立值

    content_hash = hashlib.sha256(content.encode("utf-8")).digest()[0]
    dr = (content_hash % 9) if (content_hash % 9) != 0 else 9
    return dr


def classify_audit(dr: int) -> Dict[str, Any]:
    """
    根據dr值進行三色審計分類。

    🟢 GREEN  - dr∈{3,6,9} - 木態·生長·安全 - PASS
    🟡 YELLOW - dr∈{2,5,8} - 土態·待定·警示 - REVIEW
    🔴 RED    - dr∈{1,4,7} - 火態·爆發·熔斷 - BLOCK

    Args:
        dr: 數字根值（1-9）

    Returns:
        審計結果字典
    """
    if dr in {3, 6, 9}:
        return {
            "color": "🟢",
            "level": "GREEN",
            "phase": "木態",
            "meaning": "生長·安全",
            "action": "放行",
            "reasoning": f"dr={dr}·木態·生長·安全"
        }
    elif dr in {2, 5, 8}:
        return {
            "color": "🟡",
            "level": "YELLOW",
            "phase": "土態",
            "meaning": "待定·警示",
            "action": "二次確認",
            "reasoning": f"dr={dr}·土態·待定·警示"
        }
    else:  # dr in {1, 4, 7}
        return {
            "color": "🔴",
            "level": "RED",
            "phase": "火態",
            "meaning": "爆發·熔斷",
            "action": "立即停止",
            "reasoning": f"dr={dr}·火態·爆發·熔斷"
        }


def quick_audit(content: str) -> Dict[str, Any]:
    """
    快速審計：計算dr值並分類。

    Returns:
        {
            "dr": int,
            "color": str,
            "level": str,
            "action": str,
            "reasoning": str
        }
    """
    dr = calculate_dr(content)
    audit = classify_audit(dr)
    return {
        "dr": dr,
        **audit
    }


# ─────────────────────────────────────────────────────────
# JSONL處理器（日志輸出）
# ─────────────────────────────────────────────────────────

class JSONLHandler(logging.Handler):
    """
    自定義日志處理器，輸出JSONL格式到文件。

    每行都是有效的JSON對象，便於流式解析。
    """

    def __init__(self, filename: Path):
        super().__init__()
        self.filename = Path(filename)
        self.filename.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, record: logging.LogRecord) -> None:
        """
        發出日志記錄為JSONL行。
        """
        try:
            log_entry = {
                "timestamp": datetime.fromtimestamp(
                    record.created, tz=ZoneInfo("Asia/Shanghai")
                ).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
            }

            # 添加自定義屬性（如果有）
            if hasattr(record, "dna"):
                log_entry["dna"] = record.dna
            if hasattr(record, "audit"):
                log_entry["audit"] = record.audit
            if hasattr(record, "metadata"):
                log_entry["metadata"] = record.metadata

            # 原子性寫入
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

        except Exception as exc:
            self.handleError(record)


# ─────────────────────────────────────────────────────────
# 龍魂日志記錄器主類
# ─────────────────────────────────────────────────────────

class LonghunLogger:
    """
    龍魂統一日志系統。

    特性：
      • DNA追蹤：每條日志自動生成唯一DNA
      • 三色審計：自動計算dr值並分類
      • JSONL輸出：結構化、可機器解析
      • 控制台輸出：彩色友好的人工可讀格式
    """

    def __init__(
        self,
        name: str,
        log_file: Optional[str] = None,
        console: bool = True,
        auto_audit: bool = True
    ):
        """
        初始化龍魂日志記錄器。

        Args:
            name: 日志記錄器名稱（e.g., "longhun.credential_manager"）
            log_file: JSONL日志文件路徑（可選，e.g., "~/.../日志/mymodule.jsonl"）
            console: 是否輸出到控制台（默認True）
            auto_audit: 是否自動進行三色審計（默認True）
        """
        self.name = name
        self.auto_audit = auto_audit
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 清除默認處理器
        self.logger.handlers.clear()

        # JSONL文件處理器
        if log_file:
            log_path = Path(log_file).expanduser()
            jsonl_handler = JSONLHandler(log_path)
            self.logger.addHandler(jsonl_handler)

        # 控制台處理器
        if console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
                )
            )
            self.logger.addHandler(console_handler)

    def _log_with_dna(
        self,
        level: int,
        msg: str,
        **metadata
    ) -> str:
        """
        內部方法：帶DNA追蹤的日志記錄。

        Args:
            level: 日志級別
            msg: 日志消息
            **metadata: 自定義元數據

        Returns:
            DNA追蹤碼
        """
        # 生成DNA
        module = self.name.upper().replace(".", "-")
        dna = generate_dna(module, msg)

        # 快速審計（如果啟用）
        audit = None
        if self.auto_audit:
            audit = quick_audit(msg)

        # 創建日志記錄
        record = self.logger.makeRecord(
            name=self.name,
            level=level,
            fn="",
            lno=0,
            msg=msg,
            args=(),
            exc_info=None
        )

        # 附加自定義屬性
        record.dna = dna
        if audit:
            record.audit = audit
        if metadata:
            record.metadata = metadata

        # 發出日志
        self.logger.handle(record)

        return dna

    def debug(self, msg: str, **metadata) -> str:
        """記錄DEBUG級別日志。"""
        return self._log_with_dna(logging.DEBUG, msg, **metadata)

    def info(self, msg: str, **metadata) -> str:
        """記錄INFO級別日志。"""
        return self._log_with_dna(logging.INFO, msg, **metadata)

    def warning(self, msg: str, **metadata) -> str:
        """記錄WARNING級別日志。"""
        return self._log_with_dna(logging.WARNING, msg, **metadata)

    def error(self, msg: str, **metadata) -> str:
        """記錄ERROR級別日志。"""
        return self._log_with_dna(logging.ERROR, msg, **metadata)

    def critical(self, msg: str, **metadata) -> str:
        """記錄CRITICAL級別日志。"""
        return self._log_with_dna(logging.CRITICAL, msg, **metadata)

    def audit(self, content: str, **metadata) -> Dict[str, Any]:
        """
        顯式審計日志。

        Args:
            content: 待審計內容
            **metadata: 自定義元數據

        Returns:
            審計結果字典
        """
        # 執行審計
        audit_result = quick_audit(content)

        # 記錄審計日志
        dna = generate_dna(
            self.name.upper().replace(".", "-"),
            content,
            version="v1.0"
        )

        record = self.logger.makeRecord(
            name=self.name,
            level=logging.INFO,
            fn="",
            lno=0,
            msg=content,
            args=(),
            exc_info=None
        )

        record.dna = dna
        record.audit = audit_result
        record.metadata = metadata

        self.logger.handle(record)

        return {
            "dna": dna,
            "audit": audit_result,
            "timestamp": datetime.now(
                ZoneInfo("Asia/Shanghai")
            ).isoformat(),
            "metadata": metadata
        }


# ─────────────────────────────────────────────────────────
# 全局日志管理
# ─────────────────────────────────────────────────────────

_GLOBAL_LOG_DIR = None
_LOGGERS: Dict[str, LonghunLogger] = {}


def set_global_log_dir(directory: str) -> None:
    """設置全局日志目錄。"""
    global _GLOBAL_LOG_DIR
    _GLOBAL_LOG_DIR = Path(directory).expanduser()
    _GLOBAL_LOG_DIR.mkdir(parents=True, exist_ok=True)


def get_logger(name: str, version: str = "v1.0") -> LonghunLogger:
    """
    獲取或創建日志記錄器。

    使用全局日志目錄（如果設置）自動配置日志文件。

    Args:
        name: 記錄器名稱
        version: 版本號（用於日志文件名）

    Returns:
        LonghunLogger實例
    """
    if name not in _LOGGERS:
        log_file = None
        if _GLOBAL_LOG_DIR:
            log_file = _GLOBAL_LOG_DIR / f"{name.replace('.', '_')}.jsonl"

        _LOGGERS[name] = LonghunLogger(name, log_file=log_file)

    return _LOGGERS[name]


def reset_loggers() -> None:
    """重置所有日志記錄器。"""
    global _LOGGERS
    _LOGGERS.clear()


# ─────────────────────────────────────────────────────────
# JSONL日志讀取與分析
# ─────────────────────────────────────────────────────────

def read_audit_log(
    file_path: str,
    filter_color: Optional[str] = None
) -> list:
    """
    讀取並解析JSONL審計日志。

    Args:
        file_path: 日志文件路徑
        filter_color: 按顏色篩選（"🟢", "🟡", "🔴"，或None表示全部）

    Returns:
        日志條目列表
    """
    entries = []
    file_path = Path(file_path).expanduser()

    if not file_path.exists():
        return entries

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                if filter_color:
                    if entry.get("audit", {}).get("color") == filter_color:
                        entries.append(entry)
                else:
                    entries.append(entry)
            except json.JSONDecodeError:
                continue

    return entries


def print_audit_summary(file_path: str) -> None:
    """
    打印審計日志統計摘要。

    Args:
        file_path: 日志文件路徑
    """
    entries = read_audit_log(file_path)

    if not entries:
        print(f"無日志條目：{file_path}")
        return

    colors = {"🟢": 0, "🟡": 0, "🔴": 0}
    for entry in entries:
        color = entry.get("audit", {}).get("color", "?")
        if color in colors:
            colors[color] += 1

    total = sum(colors.values())
    print(f"\n審計摘要：{file_path}")
    print(f"  總條目：{total}")
    print(f"  🟢 GREEN  (安全)：{colors['🟢']}")
    print(f"  🟡 YELLOW (待定)：{colors['🟡']}")
    print(f"  🔴 RED    (熔斷)：{colors['🔴']}")


# ─────────────────────────────────────────────────────────
# 尾部審計·鐵律 12 支持
# ─────────────────────────────────────────────────────────

def generate_tail_audit(
    module: str = "LOGGER",
    version: str = "v1.0",
    dr: int = 6,
    iron_laws: list = None
) -> str:
    """
    生成標準的尾部審計塊。

    用於滿足鐵律12（尾巴審計·永駐挂載）。

    Args:
        module: 模塊名稱
        version: 版本號
        dr: 數字根值
        iron_laws: 遵循的鐵律列表

    Returns:
        格式化的審計塊文本
    """
    beijing_tz = ZoneInfo("Asia/Shanghai")
    now = datetime.now(beijing_tz)
    timestamp = now.strftime("%Y-%m-%d %H:%M CST")
    weekday_cn = ["一", "二", "三", "四", "五", "六", "日"][now.weekday()]

    audit = classify_audit(dr)
    color = audit["color"]
    dna = generate_dna(module, version=version)

    iron_laws_str = "/".join(str(x) for x in iron_laws) if iron_laws else "10/11/12.7"

    tail_audit = f"""
─── 尾·審計 ───
時間  : {timestamp} (星期{weekday_cn})
DNA   : {dna}
五行  : dr={dr} → {audit['phase']}·{color}
守恆  : S/15 (日志系統就位)
鐵律  : {iron_laws_str} 全過 ✅
責任  : UID9622·不免責
"""

    return tail_audit.strip()


# ─────────────────────────────────────────────────────────
# 示例用法與測試
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    # 設置全局日志目錄
    set_global_log_dir("./日志_test")

    # 創建日志記錄器
    logger = get_logger("longhun.test")

    # 基本日志示例
    print("=== 基本日志示例 ===")
    dna1 = logger.info("系統啟動成功", version="v1.0", user="UID9622")
    print(f"DNA: {dna1}\n")

    dna2 = logger.warning("API調用超時", api="notion", timeout_ms=5000)
    print(f"DNA: {dna2}\n")

    dna3 = logger.error("配置文件缺失", file_path="/etc/config.yaml")
    print(f"DNA: {dna3}\n")

    # 審計日志示例
    print("=== 審計日志示例 ===")
    audit_result = logger.audit(
        "用戶認證請求",
        user="UID9622",
        action="login",
        ip="192.168.1.100"
    )
    print(f"審計結果：{json.dumps(audit_result, ensure_ascii=False, indent=2)}\n")

    # DNA生成測試
    print("=== DNA生成測試 ===")
    for i in range(3):
        dna = generate_dna("TEST-MODULE", f"content_{i}")
        print(f"DNA {i}: {dna}")

    # 三色審計測試
    print("\n=== 三色審計測試 ===")
    test_contents = [
        "正常操作流程",
        "可疑的網絡請求",
        "嚴重的系統錯誤",
    ]

    for content in test_contents:
        result = quick_audit(content)
        print(f"內容: {content}")
        print(f"  DR值: {result['dr']}")
        print(f"  顏色: {result['color']}")
        print(f"  推理: {result['reasoning']}\n")

    # 尾部審計示例
    print("=== 尾部審計示例 ===")
    tail = generate_tail_audit(
        module="LONGHUN-LOGGER",
        version="v1.0",
        dr=6,
        iron_laws=[10, 11, 12.7]
    )
    print(tail)

    print("\n✅ 所有測試完成！")
    print(f"日志文件已保存至：./日志_test/")
