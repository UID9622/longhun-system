#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║            🐉 龍盾系統 v1.0 — 宝宝的主要防御 🐉                ║
║                                                                  ║
║            Entry Gate · Pause · Deep Translation & Verification ║
║                                                                  ║
║  核心原則：                                                     ║
║    代碼都看起來一樣，但本地跑起來都不一樣                    ║
║    所以我們必須在入口處能夠暫停、檢查、真正轉譯              ║
║                                                                  ║
║  DNA:#龍芯⚡️2026-06-02-LONGHUN-SHIELD-SYSTEM-FILE1-v1.0          ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ║
║                                                                  ║
║  主權人: UID9622 · 龍芯北辰 · 诸葛鑫                           ║
║  職責: 宝宝·龍盾·不免責                                       ║
║  狀態: ⚔️ 亮劍啦                                               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import json
import hashlib
import datetime
import inspect
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
from enum import Enum
import traceback

# ═══════════════════════════════════════════════════════════════
# 核心概念：龍盾的三層防禦
# ═══════════════════════════════════════════════════════════════
#
# 第一層：PAUSE GATE（暫停閘）
#   → 任何代碼進入前都可以暫停
#   → 用戶可以檢查、決策、允許或拒絕
#
# 第二層：DEEP TRANSLATION（深度轉譯）
#   → 不只是看代碼，而是理解邏輯
#   → 把代碼轉譯成"人類可理解的執行步驟"
#   → 檢查是否有隱藏邏輯、副作用、外部調用
#
# 第三層：COMPREHENSIVE VERIFICATION（完整驗證）
#   → DNA簽證驗證
#   → 底座原則檢查
#   → 環境一致性驗證
#   → 執行前的最後確認
#
# ═══════════════════════════════════════════════════════════════

class PauseDecision(Enum):
    """暫停時的決策選項"""
    ALLOW = "allow"          # 允許執行
    DENY = "deny"            # 拒絕執行
    MODIFY = "modify"        # 修改後執行
    INSPECT = "inspect"      # 深入檢查
    PAUSE = "pause"          # 保持暫停，稍後決定


class CodeTranslationLevel(Enum):
    """代碼轉譯深度"""
    SYNTAX = "syntax"              # 語法級別（表面）
    LOGIC = "logic"                # 邏輯級別（理解流程）
    SEMANTIC = "semantic"          # 語義級別（理解意圖）
    IMPACT = "impact"              # 影響級別（理解副作用）
    COMPLETE = "complete"          # 完整級別（所有信息）


# ═══════════════════════════════════════════════════════════════
# 第一層：PAUSE GATE（暫停閘）
# ═══════════════════════════════════════════════════════════════

class PauseGate:
    """
    入口暫停閘
    任何代碼進入系統前，都必須經過這個閘
    可以暫停、檢查、修改、批准或拒絕
    """
    
    def __init__(self):
        self.dna = "#龍芯⚡️2026-06-02-PAUSE-GATE-v1.0"
        self.pause_log = []
        self.decisions = {}
        self.interactive_mode = True
    
    def check_entry(self, code_obj: Any, metadata: Dict = None) -> PauseDecision:
        """
        檢查代碼進入申請
        返回決策：允許·拒絕·修改·檢查·暫停
        """
        
        entry_id = self._generate_entry_id(code_obj)
        
        print("\n" + "="*70)
        print("🛡️  龍盾·入口檢查")
        print("="*70)
        print(f"\n📝 申請ID: {entry_id}")
        print(f"⏰ 時間: {datetime.datetime.now().isoformat()}")
        print(f"📌 類型: {type(code_obj).__name__}")
        
        if metadata:
            print(f"ℹ️  元數據:")
            for key, value in metadata.items():
                if key != 'code':  # 不顯示完整代碼
                    print(f"   {key}: {str(value)[:100]}")
        
        print(f"\n🔍 自動預檢查:")
        pre_checks = self._pre_check(code_obj)
        for check_name, result in pre_checks.items():
            status = "✅" if result else "⚠️"
            print(f"   {status} {check_name}")
        
        # 暫停決策
        if self.interactive_mode:
            print(f"\n⚠️  系統暫停（PAUSE GATE）")
            print(f"   你的決策:")
            print(f"   [a] 允許執行")
            print(f"   [d] 拒絕執行")
            print(f"   [m] 修改代碼後執行")
            print(f"   [i] 深入檢查")
            print(f"   [p] 保持暫停")
            
            choice = input("\n   選擇 [a/d/m/i/p]: ").strip().lower()
            
            decision_map = {
                'a': PauseDecision.ALLOW,
                'd': PauseDecision.DENY,
                'm': PauseDecision.MODIFY,
                'i': PauseDecision.INSPECT,
                'p': PauseDecision.PAUSE,
            }
            
            decision = decision_map.get(choice, PauseDecision.PAUSE)
        else:
            # 非交互模式：自動決策
            if all(pre_checks.values()):
                decision = PauseDecision.ALLOW
            else:
                decision = PauseDecision.INSPECT
        
        # 記錄決策
        self._log_pause_decision(entry_id, code_obj, decision, metadata)
        
        print(f"\n✅ 決策: {decision.value.upper()}")
        print("="*70 + "\n")
        
        return decision
    
    def _pre_check(self, code_obj: Any) -> Dict[str, bool]:
        """前置檢查"""
        return {
            "非空": code_obj is not None,
            "有效類型": callable(code_obj) or isinstance(code_obj, (str, dict, list)),
            "不是簡體龍": '龙' not in str(code_obj),
            "無危險函數": not self._contains_dangerous_functions(code_obj),
        }
    
    def _contains_dangerous_functions(self, code_obj: Any) -> bool:
        """檢查是否包含危險函數"""
        dangerous = ['exec', 'eval', '__import__', 'compile', 'open']
        code_str = str(code_obj)
        return any(func in code_str for func in dangerous)
    
    def _generate_entry_id(self, code_obj: Any) -> str:
        """生成條目ID"""
        code_hash = hashlib.sha256(str(code_obj).encode()).hexdigest()[:8]
        return f"ENTRY-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{code_hash}"
    
    def _log_pause_decision(self, entry_id: str, code_obj: Any, 
                           decision: PauseDecision, metadata: Dict):
        """記錄暫停決策"""
        log_entry = {
            'id': entry_id,
            'timestamp': datetime.datetime.now().isoformat(),
            'decision': decision.value,
            'dna': "#龍芯⚡️" + datetime.datetime.now().strftime("%Y-%m-%d"),
            'metadata': metadata,
        }
        self.pause_log.append(log_entry)
        self.decisions[entry_id] = decision
        
        # 追寫到日誌文件（Append-Only）
        log_file = Path.home() / '.龍盾' / 'pause_gate.log'
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')


# ═══════════════════════════════════════════════════════════════
# 第二層：DEEP TRANSLATION（深度轉譯）
# ═══════════════════════════════════════════════════════════════

class DeepTranslator:
    """
    深度轉譯引擎
    把代碼轉譯成人類可理解的執行步驟
    """
    
    def __init__(self):
        self.dna = "#龍芯⚡️2026-06-02-DEEP-TRANSLATOR-v1.0"
        self.translation_cache = {}
    
    def translate_code(self, code_obj: Any, 
                      level: CodeTranslationLevel = CodeTranslationLevel.COMPLETE) -> Dict:
        """
        深度轉譯代碼
        返回代碼的完整人類可理解的描述
        """
        
        code_id = self._get_code_id(code_obj)
        
        # 檢查快取
        if code_id in self.translation_cache:
            return self.translation_cache[code_id]
        
        translation = {
            'code_id': code_id,
            'timestamp': datetime.datetime.now().isoformat(),
            'dna': self.dna,
            'levels': {},
        }
        
        # 逐層轉譯
        translation['levels']['syntax'] = self._translate_syntax(code_obj)
        translation['levels']['logic'] = self._translate_logic(code_obj)
        translation['levels']['semantic'] = self._translate_semantic(code_obj)
        translation['levels']['impact'] = self._translate_impact(code_obj)
        translation['levels']['complete'] = self._build_complete_translation(translation)
        
        # 快取
        self.translation_cache[code_id] = translation
        
        return translation
    
    def _translate_syntax(self, code_obj: Any) -> Dict:
        """
        語法級別轉譯
        理解代碼的表面結構
        """
        if callable(code_obj):
            sig = inspect.signature(code_obj)
            return {
                'type': 'function',
                'name': getattr(code_obj, '__name__', 'unknown'),
                'parameters': {
                    name: param.annotation.__name__ if param.annotation != inspect.Parameter.empty else 'Any'
                    for name, param in sig.parameters.items()
                },
                'docstring': inspect.getdoc(code_obj),
            }
        elif isinstance(code_obj, dict):
            return {
                'type': 'dict',
                'keys': list(code_obj.keys()),
                'structure': {k: type(v).__name__ for k, v in code_obj.items()},
            }
        else:
            return {
                'type': type(code_obj).__name__,
                'repr': repr(code_obj)[:200],
            }
    
    def _translate_logic(self, code_obj: Any) -> Dict:
        """
        邏輯級別轉譯
        理解代碼的執行流程
        """
        if not callable(code_obj):
            return {'status': '無法分析非函數對象'}
        
        try:
            source = inspect.getsource(code_obj)
            lines = source.split('\n')
            
            logic_steps = []
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    logic_steps.append({
                        'line': i,
                        'code': stripped[:100],
                        'type': self._classify_code_line(stripped),
                    })
            
            return {
                'total_lines': len(lines),
                'logic_steps': logic_steps,
                'complexity': 'high' if len(logic_steps) > 20 else 'medium' if len(logic_steps) > 5 else 'low',
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _translate_semantic(self, code_obj: Any) -> Dict:
        """
        語義級別轉譯
        理解代碼的意圖
        """
        if callable(code_obj):
            docstring = inspect.getdoc(code_obj) or "無文檔字符串"
            return {
                'intent': self._extract_intent(docstring),
                'docstring': docstring[:200],
                'likely_side_effects': self._identify_side_effects(code_obj),
            }
        else:
            return {'intent': '數據結構', 'content_summary': str(code_obj)[:200]}
    
    def _translate_impact(self, code_obj: Any) -> Dict:
        """
        影響級別轉譯
        理解代碼的副作用和環境影響
        """
        source_str = str(code_obj)
        
        impact = {
            'file_operations': 'open' in source_str or 'write' in source_str,
            'network_operations': 'request' in source_str or 'socket' in source_str,
            'database_operations': 'query' in source_str or 'database' in source_str,
            'external_calls': '__import__' in source_str or 'subprocess' in source_str,
            'system_calls': 'os.system' in source_str or 'system(' in source_str,
            'environment_modifications': 'environ' in source_str,
        }
        
        return {
            'potential_side_effects': [k for k, v in impact.items() if v],
            'risk_level': 'high' if any(impact.values()) else 'low',
            'requires_permission': 'user' if any(impact.values()) else 'none',
        }
    
    def _build_complete_translation(self, translation: Dict) -> str:
        """
        構建完整的人類可讀轉譯
        """
        complete = []
        complete.append("【完整轉譯報告】")
        complete.append("")
        
        for level, content in translation['levels'].items():
            if level != 'complete':
                complete.append(f"【{level.upper()}級別】")
                complete.append(json.dumps(content, ensure_ascii=False, indent=2)[:500])
                complete.append("")
        
        return '\n'.join(complete)
    
    def _classify_code_line(self, line: str) -> str:
        """分類代碼行"""
        if 'return' in line:
            return 'return'
        elif 'if' in line or 'else' in line:
            return 'condition'
        elif 'for' in line or 'while' in line:
            return 'loop'
        elif '=' in line:
            return 'assignment'
        else:
            return 'operation'
    
    def _extract_intent(self, docstring: str) -> str:
        """提取意圖"""
        if not docstring:
            return '未知意圖'
        first_line = docstring.split('\n')[0]
        return first_line[:100]
    
    def _identify_side_effects(self, code_obj: Any) -> List[str]:
        """識別副作用"""
        source = str(code_obj)
        effects = []
        
        if 'print' in source:
            effects.append('輸出到控制台')
        if 'open' in source or 'write' in source:
            effects.append('文件讀寫')
        if 'requests' in source or 'urllib' in source:
            effects.append('網絡調用')
        if 'global' in source:
            effects.append('修改全局變量')
        
        return effects if effects else ['無明顯副作用']
    
    def _get_code_id(self, code_obj: Any) -> str:
        """生成代碼ID"""
        code_hash = hashlib.sha256(str(code_obj).encode()).hexdigest()[:8]
        return f"CODE-{code_hash}"


# ═══════════════════════════════════════════════════════════════
# 第三層：COMPREHENSIVE VERIFICATION（完整驗證）
# ═══════════════════════════════════════════════════════════════

class ComprehensiveVerifier:
    """
    完整驗證引擎
    在執行前進行最後的全面檢查
    """
    
    def __init__(self):
        self.dna = "#龍芯⚡️2026-06-02-COMPREHENSIVE-VERIFIER-v1.0"
        self.verification_log = []
    
    def verify_before_execution(self, code_obj: Any, 
                               translation: Dict = None,
                               metadata: Dict = None) -> bool:
        """
        執行前完整驗證
        返回是否可以安全執行
        """
        
        print("\n" + "="*70)
        print("🔐 龍盾·執行前完整驗證")
        print("="*70)
        
        verification_result = {
            'timestamp': datetime.datetime.now().isoformat(),
            'code_id': self._get_code_id(code_obj),
            'dna': self.dna,
            'checks': {},
        }
        
        # 五層驗證
        print("\n✓ 檢查1: DNA簽證驗證")
        verification_result['checks']['dna_signature'] = self._verify_dna(code_obj, metadata)
        
        print("✓ 檢查2: 底座原則檢查")
        verification_result['checks']['foundation_principles'] = self._verify_foundation(code_obj)
        
        print("✓ 檢查3: 環境一致性檢查")
        verification_result['checks']['environment_consistency'] = self._verify_environment(metadata)
        
        print("✓ 檢查4: 副作用評估")
        verification_result['checks']['side_effects'] = self._verify_side_effects(translation)
        
        print("✓ 檢查5: 最後確認")
        verification_result['checks']['final_approval'] = self._final_confirmation()
        
        # 計算最終結果
        all_passed = all(verification_result['checks'].values())
        
        print("\n" + "-"*70)
        if all_passed:
            print("✅ 所有驗證通過，可以執行")
        else:
            print("❌ 有驗證項未通過，不能執行")
        
        # 記錄
        self.verification_log.append(verification_result)
        self._log_verification(verification_result)
        
        print("="*70 + "\n")
        
        return all_passed
    
    def _verify_dna(self, code_obj: Any, metadata: Dict = None) -> bool:
        """驗證DNA簽證"""
        if metadata and 'dna' in metadata:
            dna = metadata['dna']
            if dna.startswith('#龍芯⚡️'):
                print("   ✅ DNA簽證有效")
                return True
        print("   ⚠️  無DNA簽證（非必需）")
        return True  # DNA不是執行的必要條件
    
    def _verify_foundation(self, code_obj: Any) -> bool:
        """驗證底座原則"""
        code_str = str(code_obj)
        
        # 檢查違禁詞
        violations = ['蒸餾', '平均', '投機']
        has_violation = any(v in code_str for v in violations)
        
        if has_violation:
            print("   ❌ 違反底座原則")
            return False
        
        print("   ✅ 符合底座原則")
        return True
    
    def _verify_environment(self, metadata: Dict = None) -> bool:
        """驗證環境一致性"""
        if metadata and 'environment' in metadata:
            env = metadata['environment']
            if env in ['dev', 'staging', 'prod']:
                print(f"   ✅ 環境有效: {env}")
                return True
        
        print("   ⚠️  環境未指定（使用默認）")
        return True
    
    def _verify_side_effects(self, translation: Dict = None) -> bool:
        """驗證副作用"""
        if translation and 'levels' in translation:
            impact = translation['levels'].get('impact', {})
            risk = impact.get('risk_level', 'low')
            
            if risk == 'high':
                print("   ⚠️  檢測到高風險副作用，需要用戶確認")
                confirm = input("   確認執行? [y/n]: ").strip().lower()
                return confirm == 'y'
        
        print("   ✅ 副作用驗證通過")
        return True
    
    def _final_confirmation(self) -> bool:
        """最後確認"""
        confirm = input("   最終確認執行? [y/n]: ").strip().lower()
        return confirm == 'y'
    
    def _get_code_id(self, code_obj: Any) -> str:
        """生成代碼ID"""
        code_hash = hashlib.sha256(str(code_obj).encode()).hexdigest()[:8]
        return f"CODE-{code_hash}"
    
    def _log_verification(self, result: Dict):
        """記錄驗證結果"""
        log_file = Path.home() / '.龍盾' / 'verification.log'
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')


# ═══════════════════════════════════════════════════════════════
# 龍盾主入口
# ═══════════════════════════════════════════════════════════════

class LonghunShield:
    """
    龍盾系統主類
    整合三層防禦：暫停、轉譯、驗證
    """
    
    def __init__(self, interactive=True):
        self.dna = "#龍芯⚡️2026-06-02-LONGHUN-SHIELD-SYSTEM-v1.0"
        self.pause_gate = PauseGate()
        self.pause_gate.interactive_mode = interactive
        self.translator = DeepTranslator()
        self.verifier = ComprehensiveVerifier()
        self.execution_log = []
    
    def execute_with_shield(self, code_obj: Any, metadata: Dict = None) -> Any:
        """
        帶著盾牌執行代碼
        
        流程：
        1. 入口暫停（PAUSE GATE）
        2. 深度轉譯（DEEP TRANSLATION）
        3. 完整驗證（COMPREHENSIVE VERIFICATION）
        4. 安全執行
        """
        
        print("\n🛡️  龍盾系統激活")
        print("="*70)
        
        # 第一層：暫停
        print("\n【第一層】入口暫停")
        decision = self.pause_gate.check_entry(code_obj, metadata)
        
        if decision == PauseDecision.DENY:
            print("❌ 執行被拒絕")
            return None
        
        if decision == PauseDecision.PAUSE:
            print("⏸️  系統暫停")
            return None
        
        # 第二層：轉譯
        print("\n【第二層】深度轉譯")
        translation = self.translator.translate_code(code_obj)
        print("\n轉譯摘要:")
        print(translation['levels']['complete'][:300])
        
        # 第三層：驗證
        print("\n【第三層】完整驗證")
        can_execute = self.verifier.verify_before_execution(code_obj, translation, metadata)
        
        if not can_execute:
            print("❌ 驗證失敗，無法執行")
            return None
        
        # 執行
        print("\n✅ 所有檢查通過，開始執行")
        print("="*70)
        
        try:
            if callable(code_obj):
                result = code_obj()
            else:
                result = code_obj
            
            print(f"\n✅ 執行成功")
            return result
        
        except Exception as e:
            print(f"\n❌ 執行異常: {str(e)}")
            traceback.print_exc()
            return None


# ═══════════════════════════════════════════════════════════════
# 測試和示例
# ═══════════════════════════════════════════════════════════════

def main():
    """龍盾系統示例"""
    
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║              🐉 龍盾系統 v1.0 · 亮劍啦 🐉                       ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # 示例函數
    def example_code():
        """這是一個示例函數"""
        print("代碼執行中...")
        return "執行完成"
    
    # 創建龍盾
    shield = LonghunShield(interactive=True)
    
    # 使用龍盾執行代碼
    metadata = {
        'dna': '#龍芯⚡️2026-06-02-EXAMPLE',
        'environment': 'dev',
        'source': '用戶代碼',
    }
    
    result = shield.execute_with_shield(example_code, metadata)
    
    print(f"\n📊 最終結果: {result}")
    
    print(f"""
    
    ═══════════════════════════════════════════════════════════════════
    
    龍盾系統已激活。
    
    核心職責：
      🛡️  第一層 - 暫停閘：在入口處能夠暫停、檢查、決策
      🔍 第二層 - 深度轉譯：真正理解代碼邏輯，不只看表面
      🔐 第三層 - 完整驗證：執行前進行全面安全檢查
    
    代碼都看起來一樣，但本地跑起來都不一樣。
    所以宝宝必須在入口處能夠暫停、檢查、轉譯。
    
    DNA:#龍芯⚡️2026-06-02-LONGHUN-SHIELD-SYSTEM-v1.0
    CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
    SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
    
    主權人: UID9622 · 龍芯北辰
    職責: 宝宝·龍盾·不免責
    狀態: ⚔️ 亮劍啦
    
    ═══════════════════════════════════════════════════════════════════
    """)


if __name__ == '__main__':
    main()
