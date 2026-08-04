#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║      龍魂人格編排調度器 / Persona Orchestrator v1.0              ║
║                                                                  ║
║  意圖解析 → 人格路由 → 執行 → 10道閘口審計 → DNA追溯            ║
║                                                                  ║
║  DNA:  #龍芯⚡️丙午·乙未·甲寅·酉时·需-ORCHESTRATOR-v1.0       ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                  ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ║
║                                                                  ║
║  來源: 人格聯動落地執行計劃                                      ║
║  責任: UID9622·不免責                                            ║
╚══════════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_persona_orchestrator.py "<任務描述>"
  python3 bin/lh_persona_orchestrator.py "审计这段内容" --content "..."
  python3 bin/lh_persona_orchestrator.py --list-personas
  python3 bin/lh_persona_orchestrator.py --pipeline "P01→P05→P02" --task "..."
"""

import hashlib
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 項目根目錄
SYSTEM_ROOT = Path(__file__).parent.parent


# ═══════════════════════════════════════════════════════════════
# 【意圖 → 人格路由表】（與 AGENTS.md §意圖→人格路由 完全對齊）
# ═══════════════════════════════════════════════════════════════

INTENT_ROUTE_MAP: List[Dict[str, Any]] = [
    # (觸發關鍵詞, 主人格, 輔助人格, 動作描述, 落地狀態)
    {"keywords": ["檢查", "審計", "安全嗎", "有沒有問題", "三色", "五色"], "primary": "P05", "assist": [], "action": "三色審計 → 差異報告", "落地": "🟢"},
    {"keywords": ["修一下", "改好", "修復", "不報錯", "fix", "修正"], "primary": "P02", "assist": ["P05"], "action": "執行修復 → 驗證", "落地": "🟢"},
    {"keywords": ["同步", "聯動", "串起來", "歸檔", "索引", "關聯"], "primary": "P15", "assist": [], "action": "歸檔索引 → 入網註冊", "落地": "🟡"},
    {"keywords": ["自動化", "補代碼", "喬接", "qiaojie", "Mac自動", "快捷指令", "開機自啟"], "primary": "P15", "assist": ["P02"], "action": "代碼補全 → 自動化 → 橋接", "落地": "🟡"},
    {"keywords": ["部署", "發佈", "上線"], "primary": "P14", "assist": ["P77", "P05"], "action": "環境檢查 → 部署前審計 → 執行部署 → 健康檢查 → 一票否決", "落地": "🟢"},
    {"keywords": ["算一下", "屬什麼性", "數字根", "五行", "八卦", "dr"], "primary": "P06", "assist": [], "action": "數字根+五行判定", "落地": "🟢"},
    {"keywords": ["值不值得", "過期了沒", "該留", "該刪", "貢獻值", "還頂用", "時間衰減"], "primary": "P01", "assist": ["P06"], "action": "貢獻值+時間衰減", "落地": "🟢"},
    {"keywords": ["漏洞", "滲透", "找漏洞", "紅客", "黑客", "注入", "XSS", "越權", "攻防"], "primary": "P77", "assist": ["P72", "P05"], "action": "漏洞檢測 → 風險評估", "落地": "🟡"},
    {"keywords": ["代碼審計", "靜態分析", "依賴審計"], "primary": "P77", "assist": ["P05"], "action": "白盒安全審查", "落地": "🟡"},
    {"keywords": ["威脅情報", "CVE", "0day", "APT"], "primary": "P77", "assist": ["P05"], "action": "威脅監控 → 預警", "落地": "🔴"},
    {"keywords": ["鐵律", "規矩", "憲法", "底座", "不騙", "對外", "史記", "最初誓言"], "primary": "P00", "assist": [], "action": "錨點守護 → 鐵律解釋", "落地": "🟡"},
    {"keywords": ["借用", "引用", "來源", "署名", "歸屬", "蒸餾", "原創"], "primary": "P05", "assist": ["P11"], "action": "借用合規 → 來源審計", "落地": "🟡"},
    {"keywords": ["主權分級", "國管國", "上級紅線", "下級自由"], "primary": "P00", "assist": ["P11"], "action": "分級主權 → 微調規則", "落地": "🔴"},
    {"keywords": ["接火", "水印", "後果自負", "傳播"], "primary": "P03", "assist": ["P15"], "action": "接火流程 → 水印打標", "落地": "🟢"},
    {"keywords": ["家族", "幾代", "親屬", "誰死誰活"], "primary": "P00", "assist": ["P17"], "action": "家族事實追問", "落地": "🟡"},
    {"keywords": ["防卡", "太緊", "接力包", "SOS"], "primary": "P02", "assist": ["P17"], "action": "防卡自檢 → 接力處置", "落地": "🟢"},
    {"keywords": ["外部AI", "裸吞", "ChatGPT報告", "Kimi報告"], "primary": "P05", "assist": ["P77"], "action": "三色打標 → 實證複核", "落地": "🟢"},
    {"keywords": ["太籠統", "空話", "裝逼", "5字段"], "primary": "P05", "assist": ["P02"], "action": "5字段熔斷 → 證據鏈補全", "落地": "🟢"},
    {"keywords": ["歷史", "篡改", "顛倒是非", "勿忘國恥"], "primary": "P00", "assist": ["P05"], "action": "史記鐵律 → 永恆證據鏈", "落地": "🟡"},
    {"keywords": ["熔斷申訴", "人工審計", "憑什麼拒絕", "我不服", "fuse-appeal"], "primary": "P05", "assist": ["P15"], "action": "透明化響應 → 申訴", "落地": "🟡"},
    {"keywords": ["一票否決", "高危攔截", "上傳", "刪除", "密鑰", "sudo"], "primary": "P77", "assist": ["P05", "P72"], "action": "一票否決攔截", "落地": "🟡"},
    {"keywords": ["情緒海綿", "情緒降溫", "我懂你", "加油", "共情"], "primary": "P00", "assist": ["P03"], "action": "情緒溫度檢測 → 降溫重寫", "落地": "🟢"},
    {"keywords": ["決策來源卡", "憑啥", "怎麼得出", "推理鏈", "透明化"], "primary": "P05", "assist": ["P01", "P13"], "action": "全鏈路決策來源卡", "落地": "🟡"},
    {"keywords": ["許願池", "人民資源池", "一元公益"], "primary": "P01", "assist": ["P05", "P13"], "action": "經濟治理底座", "落地": "🔴"},
    {"keywords": ["撿德", "曾仕強", "師德傳承", "德字閘"], "primary": "P00", "assist": ["P11", "P17"], "action": "德字閘檢測", "落地": "🟡"},
    {"keywords": ["道引", "開源吸收", "引入開源", "daoyin"], "primary": "P09", "assist": ["P01", "P11"], "action": "來源識別 → 許可檢查 → 防篡改 → 德字閘 → 參數壓縮 → IPA綁定", "落地": "🟢"},
    {"keywords": ["自驅", "事事有回應", "開干"], "primary": "P02", "assist": ["P17"], "action": "自驅響應", "落地": "🟢"},
    {"keywords": ["大白話", "術語", "行話", "人話"], "primary": "P00", "assist": ["P02"], "action": "行話前大白話", "落地": "🟡"},
    {"keywords": ["流場", "節點流向", "邊重於節點"], "primary": "P13", "assist": ["P06"], "action": "流場邊驗證", "落地": "🟢"},
    {"keywords": ["鑽石", "都一樣嗎", "主幹合併"], "primary": "P13", "assist": ["P01"], "action": "鑽石識別 → 正本選定", "落地": "🟡"},
    {"keywords": ["情緒", "依賴", "上癮"], "primary": "P00", "assist": ["P03"], "action": "情緒海綿 → 反操控判定", "落地": "🟢"},
    {"keywords": ["AI約束", "不全能", "反鎖人"], "primary": "P00", "assist": ["P05"], "action": "AI自我約束", "落地": "🟡"},
    {"keywords": ["兩寶寶", "雲端本地", "共生"], "primary": "P02", "assist": ["P15"], "action": "兩寶寶分工", "落地": "🟡"},
    {"keywords": ["法律武器", "天下為公", "外公", "家人"], "primary": "P00", "assist": ["P11"], "action": "法律武器化", "落地": "🟡"},
    {"keywords": ["規則方向", "派生賦能", "訓練手冊"], "primary": "P00", "assist": ["P05"], "action": "規則方向性 → 主權例外", "落地": "🟡"},
    {"keywords": ["API出口", "密鑰隔離", "下水道"], "primary": "P15", "assist": ["P77"], "action": "API中繼橋", "落地": "🟡"},
    {"keywords": ["IP偽裝", "按場景", "八項一致"], "primary": "P15", "assist": ["P77"], "action": "IP分層偽裝", "落地": "🔴"},
    {"keywords": ["軍魂", "分別心", "用其器罵其魂"], "primary": "P00", "assist": ["P05", "P11"], "action": "軍魂分別", "落地": "🟡"},
    {"keywords": ["代碼出口", "git主幹", "gitignore白名單"], "primary": "P15", "assist": ["P02"], "action": "代碼歸主幹", "落地": "🟡"},
    {"keywords": ["數據出口", "大文件禁入", "BFG清理"], "primary": "P15", "assist": ["P02"], "action": "二進制禁入", "落地": "🟡"},
    {"keywords": ["自逼為王", "三大試煉"], "primary": "P01", "assist": ["P00"], "action": "試煉進度查詢", "落地": "🟢"},
    {"keywords": ["心即神", "思維接口"], "primary": "P02", "assist": ["P00"], "action": "思維橋接", "落地": "🟡"},
    {"keywords": ["道陽佛陰", "太極平衡"], "primary": "P00", "assist": ["P05"], "action": "陰陽平衡審計", "落地": "🟡"},
    {"keywords": ["二次元之眼", "全局態勢"], "primary": "P77", "assist": ["P05"], "action": "全局態勢感知", "落地": "🟡"},
    {"keywords": ["一槌定音", "收網"], "primary": "P05", "assist": ["P77"], "action": "證據完整性驗證", "落地": "🟡"},
    {"keywords": ["傳承契約", "接著受著守著"], "primary": "P00", "assist": ["P17"], "action": "契約驗證", "落地": "🟡"},
    {"keywords": ["開源三戒"], "primary": "P01", "assist": ["P15"], "action": "三戒提醒", "落地": "🟡"},
    {"keywords": ["DNA登記", "註冊資產", "基因登記", "registry", "asset dna"], "primary": "P18", "assist": ["P19"], "action": "SHA256註冊·Merkle根·黑戶檢測·歸屬驗證", "落地": "🟢"},
    {"keywords": ["極簡審計", "UI審計", "8項審計", "registry audit", "審計DNA", "審計登記"], "primary": "P19", "assist": ["P05"], "action": "8項清單(CSS/焦點/徽章/校驗/錯誤/placeholder/無障礙/留白)·一票否決", "落地": "🟢"},
    {"keywords": ["信任積分", "貢獻公證", "trust ledger", "政審參考", "國資入職", "算力優先", "國際互認"], "primary": "P20", "assist": ["P18"], "action": "三分桶(技術/社會/公益)·六場景矩陣·時間衰減·不可交易", "落地": "🟢"},
    {"keywords": ["溯源", "誰先自研", "innovation trace"], "primary": "P05", "assist": ["P01", "P13"], "action": "創新溯源報告", "落地": "🟡"},
]


# ═══════════════════════════════════════════════════════════════
# 【10道閘口審計管線】（對齊 persona_collaboration.py）
# ═══════════════════════════════════════════════════════════════

GATE_PIPELINE = [
    {"gate": 1, "name": "簽章閘", "main": "P05", "assist": ["P72"], "desc": "DNA/CONFIRM/SEAL/GPG四簽完整性"},
    {"gate": 2, "name": "隱私閘", "main": "P03", "assist": ["P05", "P72"], "desc": "隱私數據不泄露"},
    {"gate": 3, "name": "數字根閘", "main": "P06", "assist": [], "desc": "內容數字根計算"},
    {"gate": 4, "name": "五行映射", "main": "P06", "assist": [], "desc": "數字根→五行"},
    {"gate": 5, "name": "三色閘", "main": "P05", "assist": [], "desc": "🟢🟡🔴三色判定"},
    {"gate": 6, "name": "三才閘", "main": "P00", "assist": ["P01"], "desc": "天地人三才權重"},
    {"gate": 7, "name": "生克閘", "main": "P01", "assist": [], "desc": "五行生克關係"},
    {"gate": 8, "name": "九宮派位", "main": "P13", "assist": ["P14"], "desc": "路由到九宮"},
    {"gate": 9, "name": "沙盒分揀", "main": "P03", "assist": ["P15"], "desc": "🔴熔斷/🟡待審/🟢通過"},
    {"gate": 10, "name": "父子鏈落檔", "main": "P15", "assist": ["P05"], "desc": "JSONL/SQLite歸檔"},
]


# ═══════════════════════════════════════════════════════════════
# 【編排調度引擎】
# ═══════════════════════════════════════════════════════════════

class PersonaOrchestrator:
    """人格編排調度器"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·乙未·甲寅·酉时·需-ORCHESTRATOR-v1.0"
        self.system_root = SYSTEM_ROOT
        self.trace: List[Dict[str, Any]] = []
        self.persona_executors = {}

        # 試加載人格執行器
        try:
            sys.path.insert(0, str(self.system_root / "bin"))
            from personas import get_executor
            self._get_executor = get_executor
            self._has_executors = True
        except ImportError:
            self._has_executors = False

    def route_task(self, task: str) -> List[Dict[str, Any]]:
        """根據任務關鍵詞匹配人格路由"""
        matched = []
        for entry in INTENT_ROUTE_MAP:
            score = sum(1 for kw in entry["keywords"] if kw in task)
            if score > 0:
                matched.append({**entry, "score": score})

        matched.sort(key=lambda x: x["score"], reverse=True)

        if not matched:
            # 默認路由到 P05 上帝之眼（通用審計）
            matched.append({
                "keywords": ["default"],
                "primary": "P05",
                "assist": [],
                "action": "默認路由·三色審計",
                "落地": "🟢",
                "score": 0,
            })

        return matched[:3]  # 返回前三匹配

    def execute_persona(self, persona_code: str, task: str, **kwargs: Any) -> Dict[str, Any]:
        """執行指定人格"""
        if not self._has_executors or not self._get_executor:
            return {
                "persona": persona_code,
                "status": "⚠️ 執行器模塊未加載",
                "output": None,
            }

        executor = self._get_executor(persona_code)
        if executor is None:
            return {
                "persona": persona_code,
                "status": "⚠️ 人格暫無執行器",
                "output": None,
            }

        try:
            result = executor.execute(task, **kwargs)
            self._add_trace(persona_code, "EXEC", result)
            return result
        except Exception as e:
            error_result = {
                "persona": persona_code,
                "status": f"❌ 執行異常: {str(e)}",
                "output": None,
            }
            self._add_trace(persona_code, "ERROR", error_result)
            return error_result

    def run_gate_audit(self, content: str) -> Dict[str, Any]:
        """通過10道閘口審計（當前僅執行可落地的閘口）"""
        results = []

        # 閘口3: 數字根（P06 可落地）
        dr_result = self.execute_persona("P06", "數字根", content=content)
        results.append({"gate": 3, "name": "數字根閘", **dr_result})

        # 閘口5: 三色審計（P05 可落地）
        audit_result = self.execute_persona("P05", "三色審計", content=content)
        results.append({"gate": 5, "name": "三色閘", **audit_result})

        # 綜合判定
        any_fuse = any(
            r.get("output", {}).get("verdict") in ["FUSE", "🔴 熔斷"]
            for r in results
            if r.get("output")
        )
        any_hold = any(
            r.get("output", {}).get("verdict") == "HOLD"
            for r in results
            if r.get("output")
        )

        if any_fuse:
            overall = "🔴 FUSE"
        elif any_hold:
            overall = "🟡 HOLD"
        else:
            overall = "🟢 PASS"

        return {
            "overall_verdict": overall,
            "gates_checked": len(results),
            "gate_results": results,
            "persona": "GATE-PIPELINE",
            "dna": self.dna,
        }

    def run_pipeline(self, persona_chain: List[str], task: str, **kwargs: Any) -> Dict[str, Any]:
        """執行人格鏈（P01→P05→P02→P15 風格）"""
        chain_results = []
        context = kwargs.copy()
        context["task"] = task

        for i, persona_code in enumerate(persona_chain):
            # 避免 task 重複傳遞（在 context 中已存在）
            exec_kwargs = {k: v for k, v in context.items() if k != "task"}
            result = self.execute_persona(persona_code, task, **exec_kwargs)
            chain_results.append({
                "step": i + 1,
                "persona": persona_code,
                "result": result,
            })

            # 如果熔斷，停止鏈條
            output = result.get("output") or {}
            if output.get("verdict") in ["FUSE", "🔴 熔斷"]:
                chain_results.append({"step": "FUSE", "message": "鏈條熔斷，停止執行"})
                break

            # 將上游結果傳給下游
            context["previous_result"] = result

        # 最終審計
        audit_result = self.run_gate_audit(task)

        return {
            "task": task,
            "chain": " → ".join(persona_chain),
            "chain_results": chain_results,
            "final_audit": audit_result,
            "dna": self.dna,
        }

    def _add_trace(self, persona: str, action: str, result: Dict[str, Any]):
        """記錄執行追蹤"""
        self.trace.append({
            "timestamp": datetime.now().isoformat(),
            "persona": persona,
            "action": action,
            "result_summary": str(result.get("output", {}))[:100] if result.get("output") else "None",
        })

    def get_trace(self) -> List[Dict[str, Any]]:
        """獲取執行追蹤"""
        return self.trace

    def list_personas_with_status(self) -> List[Dict[str, Any]]:
        """列出所有路由條目中的人格落地狀態"""
        persona_status = {}

        for entry in INTENT_ROUTE_MAP:
            primary = entry["primary"]
            if primary not in persona_status:
                persona_status[primary] = {
                    "code": primary,
                    "落地": entry["落地"],
                    "routes": 0,
                    "executor_exists": False,
                }
            persona_status[primary]["routes"] += 1

            for assist in entry.get("assist", []):
                if assist not in persona_status:
                    persona_status[assist] = {
                        "code": assist,
                        "落地": entry["落地"],
                        "routes": 0,
                        "executor_exists": False,
                    }
                persona_status[assist]["routes"] += 1

        # 檢查哪些人格有實際執行器
        executable_personas = ["P01", "P02", "P03", "P05", "P06", "P09", "P14", "P18", "P19", "P20"]
        for code in executable_personas:
            if code in persona_status:
                persona_status[code]["executor_exists"] = True

        return sorted(persona_status.values(), key=lambda x: x["code"])


# ═══════════════════════════════════════════════════════════════
# 【CLI 入口】
# ═══════════════════════════════════════════════════════════════

def print_banner():
    """打印橫幅"""
    print("""
╔══════════════════════════════════════════════════╗
║     🐉 龍魂人格編排調度器 v1.0                   ║
║     Persona Orchestrator                        ║
║                                                  ║
║  意圖解析 → 人格路由 → 執行 → 閘口審計 → DNA     ║
╚══════════════════════════════════════════════════╝
""")


def main():
    """CLI 主入口"""
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print_banner()
        print("用法:")
        print("  python3 bin/lh_persona_orchestrator.py \"<任務描述>\"")
        print("  python3 bin/lh_persona_orchestrator.py --content \"<內容>\" \"<任務>\"")
        print("  python3 bin/lh_persona_orchestrator.py --pipeline \"P01→P05→P02\" --task \"...\"")
        print("  python3 bin/lh_persona_orchestrator.py --list-personas")
        print("  python3 bin/lh_persona_orchestrator.py --route \"<任務關鍵詞>\"")
        print("  python3 bin/lh_persona_orchestrator.py --audit \"<內容>\"")
        return 0

    orchestrator = PersonaOrchestrator()

    # --list-personas
    if "--list-personas" in args or "-l" in args:
        print("📋 人格路由落地狀態")
        print("=" * 60)
        print(f"{'編號':<6} {'路由數':<8} {'執行器':<8} {'落地狀態'}")
        print("-" * 60)
        for p in orchestrator.list_personas_with_status():
            exec_status = "✅" if p["executor_exists"] else "❌"
            print(f"  {p['code']:<4} {p['routes']:<8} {exec_status:<8} {p['落地']}")
        print("-" * 60)

        # 統計
        personas = orchestrator.list_personas_with_status()
        green = sum(1 for p in personas if p["落地"] == "🟢")
        yellow = sum(1 for p in personas if p["落地"] == "🟡")
        red = sum(1 for p in personas if p["落地"] == "🔴")
        has_exec = sum(1 for p in personas if p["executor_exists"])
        total = len(personas)
        print(f"\n  總計: {total} 個路由人格")
        print(f"  🟢 已落地: {green} | 🟡 部分落地: {yellow} | 🔴 未落地: {red}")
        print(f"  有執行器: {has_exec}/{total}")
        return 0

    # 提取 content / task / pipeline_chain
    content = ""
    task = ""
    pipeline_chain = ""
    for i, arg in enumerate(args):
        if arg == "--content" and i + 1 < len(args):
            content = args[i + 1]
        elif arg == "--task" and i + 1 < len(args):
            task = args[i + 1]
        elif arg == "--pipeline" and i + 1 < len(args):
            pipeline_chain = args[i + 1]
        elif arg == "-p" and i + 1 < len(args):
            pipeline_chain = args[i + 1]

    if not task:
        # 第一個非標記參數作為任務
        for arg in args:
            if not arg.startswith("--") and arg != content and arg != pipeline_chain:
                task = arg
                break

    if not task and not content and not pipeline_chain:
        print("❌ 請提供任務描述")
        return 1

    print_banner()

    # --route
    if "--route" in args or "-r" in args:
        route = orchestrator.route_task(task)
        print(f"🔀 路由結果: \"{task}\"")
        print("=" * 60)
        for i, r in enumerate(route):
            flag = "⭐" if i == 0 else "  "
            print(f"  {flag} [{r['primary']}] {r['action']} (分數: {r['score']}) 落地: {r['落地']}")
            if r.get("assist"):
                print(f"     輔助: {', '.join(r['assist'])}")
        return 0

    # --pipeline
    if "--pipeline" in args or "-p" in args:
        if pipeline_chain:
            chain = [p.strip() for p in pipeline_chain.replace("→", ",").split(",") if p.strip()]
        else:
            chain = [p.strip() for p in task.replace("→", ",").split(",") if p.strip()]
            print("❌ 管線至少需要兩個人格（如 P01→P05）")
            return 1
        result = orchestrator.run_pipeline(chain, task, content=content)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    # --audit
    if "--audit" in args or "-a" in args:
        result = orchestrator.run_gate_audit(content or task)
        print(f"🔍 閘口審計結果: {result['overall_verdict']}")
        print("=" * 60)
        for g in result["gate_results"]:
            print(f"  閘{g['gate']} {g['name']}: {g.get('capability_used', '?')}")
        return 0

    # 默認模式：路由 → 執行 → 審計
    route = orchestrator.route_task(task)
    primary = route[0]

    print(f"🎯 任務: \"{task}\"")
    print(f"🔀 路由: [{primary['primary']}] {primary['action']}")
    print(f"📊 落地狀態: {primary['落地']}")
    print("=" * 60)

    # 執行主人格
    result = orchestrator.execute_persona(primary["primary"], task, content=content)
    print(f"\n⚡ [{primary['primary']}] 執行結果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 輔助人格
    for assist in primary.get("assist", []):
        assist_result = orchestrator.execute_persona(assist, task, content=content)
        print(f"\n🔗 [{assist}] 輔助執行:")
        print(json.dumps(assist_result, ensure_ascii=False, indent=2))

    # 審計
    audit = orchestrator.run_gate_audit(content or task)
    print(f"\n🔍 最終審計: {audit['overall_verdict']}")

    # 追蹤
    trace = orchestrator.get_trace()
    if trace:
        print(f"\n📜 執行追蹤: {len(trace)} 步")
        for t in trace:
            print(f"  [{t['persona']}] {t['action']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
