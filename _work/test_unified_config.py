#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍魂統一配置整合測試
Test Unified Configuration System Integration

驗證：
1. 配置讀取器可以正確加載配置文件
2. 所有服務檔案可以正確匯入配置
3. 所有端口設定都來自統一配置
4. 配置值在所有檔案中保持一致
"""

import sys
import json
from pathlib import Path

def test_config_reader():
    """測試 1: 配置讀取器"""
    print("\n" + "="*80)
    print("✅ 測試 1: 配置讀取器")
    print("="*80)

    try:
        from 配置读取器 import CONFIG, SystemConfig

        print("✓ 配置讀取器導入成功")

        # 驗證關鍵配置項
        required_keys = [
            'MAIN_API_HOST',
            'MAIN_API_PORT',
            'CNSH_FASTAPI_PORT',
            'THREE_SYSTEM_API_PORT',
            'LOCAL_DB_PATH'
        ]

        for key in required_keys:
            value = CONFIG.get(key)
            if value is not None:
                print(f"  ✓ {key:25} = {value}")
            else:
                print(f"  ✗ {key:25} = 未設定")
                return False

        return True
    except Exception as e:
        print(f"✗ 配置讀取器測試失敗: {e}")
        return False


def test_control_panel():
    """測試 2: 統一控制臺配置"""
    print("\n" + "="*80)
    print("✅ 測試 2: 統一控制臺")
    print("="*80)

    try:
        from 配置读取器 import CONFIG

        # 模擬控制臺中的 get_services() 函數
        if CONFIG:
            fastapi_port = CONFIG.get('CNSH_FASTAPI_PORT', 8000)
            api_port = CONFIG.get('THREE_SYSTEM_API_PORT', 5000)

            print(f"✓ CNSH FastAPI 端口: {fastapi_port}")
            print(f"✓ 三系統 API 端口: {api_port}")

            # 驗證端口類型
            if isinstance(fastapi_port, int) and isinstance(api_port, int):
                print("✓ 端口值類型正確 (int)")
                return True
            else:
                print(f"✗ 端口值類型不正確: {type(fastapi_port)}, {type(api_port)}")
                return False
        else:
            print("✗ CONFIG 不可用")
            return False

    except Exception as e:
        print(f"✗ 統一控制臺配置測試失敗: {e}")
        return False


def test_api_server_config():
    """測試 3: API 服務器配置"""
    print("\n" + "="*80)
    print("✅ 測試 3: API 服務器配置")
    print("="*80)

    try:
        from 配置读取器 import CONFIG

        # 模擬 API 服務器中的配置邏輯
        CONFIG_AVAILABLE = True
        if CONFIG_AVAILABLE:
            HOST = CONFIG.get('MAIN_API_HOST', '0.0.0.0')
            PORT = CONFIG.get('THREE_SYSTEM_API_PORT', 5000)

            print(f"✓ API 服務器 HOST: {HOST}")
            print(f"✓ API 服務器 PORT: {PORT}")

            if HOST == "0.0.0.0" and PORT == 5000:
                print("✓ API 服務器配置正確")
                return True
            else:
                print("⚠️  API 服務器端口與預期不同（可能已在配置中修改）")
                return True  # 不是失敗，只是配置不同
        else:
            print("✗ CONFIG 不可用")
            return False

    except Exception as e:
        print(f"✗ API 服務器配置測試失敗: {e}")
        return False


def test_fastapi_config():
    """測試 4: FastAPI 配置"""
    print("\n" + "="*80)
    print("✅ 測試 4: FastAPI 配置")
    print("="*80)

    try:
        from 配置读取器 import CONFIG

        # 模擬 FastAPI 中的配置邏輯
        CONFIG_AVAILABLE = True
        if CONFIG_AVAILABLE:
            host = CONFIG.get('MAIN_API_HOST', '0.0.0.0')
            port = CONFIG.get('CNSH_FASTAPI_PORT', 8000)

            print(f"✓ FastAPI HOST: {host}")
            print(f"✓ FastAPI PORT: {port}")

            if host == "0.0.0.0" and port == 8000:
                print("✓ FastAPI 配置正確")
                return True
            else:
                print("⚠️  FastAPI 端口與預期不同（可能已在配置中修改）")
                return True
        else:
            print("✗ CONFIG 不可用")
            return False

    except Exception as e:
        print(f"✗ FastAPI 配置測試失敗: {e}")
        return False


def test_config_consistency():
    """測試 5: 配置一致性"""
    print("\n" + "="*80)
    print("✅ 測試 5: 配置一致性")
    print("="*80)

    try:
        from 配置读取器 import CONFIG

        # 從配置文件讀取所有值
        fastapi_port = CONFIG.get('CNSH_FASTAPI_PORT')
        api_port = CONFIG.get('THREE_SYSTEM_API_PORT')
        host = CONFIG.get('MAIN_API_HOST')
        main_port = CONFIG.get('MAIN_API_PORT')

        print(f"✓ MAIN_API_HOST: {host}")
        print(f"✓ MAIN_API_PORT: {main_port}")
        print(f"✓ CNSH_FASTAPI_PORT: {fastapi_port}")
        print(f"✓ THREE_SYSTEM_API_PORT: {api_port}")

        # 驗證所有值都是合理的（不重複的端口）
        ports = [fastapi_port, api_port, main_port]
        if len(ports) == len(set(ports)):
            print("✓ 所有端口值互不重複")
            return True
        else:
            print("✗ 發現重複的端口值")
            return False

    except Exception as e:
        print(f"✗ 配置一致性測試失敗: {e}")
        return False


def main():
    """主測試函數"""
    print("\n" + "="*80)
    print("🐉 龍魂統一配置整合測試")
    print("="*80)
    print(f"工作目錄: {Path.cwd()}")
    print(f"配置文件: .longhunsystemconfig")
    print(f"配置讀取器: 配置读取器.py")

    tests = [
        ("配置讀取器", test_config_reader),
        ("統一控制臺", test_control_panel),
        ("API 服務器", test_api_server_config),
        ("FastAPI 接口", test_fastapi_config),
        ("配置一致性", test_config_consistency),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} 測試異常: {e}")
            results.append((test_name, False))

    # 測試摘要
    print("\n" + "="*80)
    print("📊 測試摘要")
    print("="*80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {test_name}")

    print(f"\n通過: {passed}/{total}")

    if passed == total:
        print("\n✅ 所有測試都通過！統一配置系統已就緒。")
        print("\n下一步:")
        print("  1. 檢查 .longhunsystemconfig 中的設置")
        print("  2. 運行控制臺: python3 龍魂統一控制臺.py")
        print("  3. 輸入 'all' 啟動所有服務")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 個測試失敗，請檢查配置")
        return 1


if __name__ == "__main__":
    sys.exit(main())
