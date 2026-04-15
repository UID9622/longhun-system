#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂清道夫守护进程
定时扫描所有注册DNA，发现盗窃立即通知

DNA追溯码: #龍芯⚡️2026-03-20-SWEEPER-DAEMON
"""

import requests
import time
import json
from datetime import datetime
from typing import List

API_BASE = "http://127.0.0.1:9622"

# 要监控的DNA列表（核心概念）
MONITORED_DNA_PREFIXES = [
    "龍魂系统",
    "DNA追溯",
    "TIER_0-3",
    "P0++",
    "道德经81",
    "易经64",
    "七维权重",
    "IW-ECB",
    "规则钩子",
    "清道夫",
    "CNSH",
    "哈希证据链",
    "对峙证据",
    "STAR-MEMORY",
    "端-端加密",
]

class SweeperDaemon:
    """清道夫守护进程"""
    
    def __init__(self, scan_interval: int = 3600):
        self.scan_interval = scan_interval  # 默认1小时扫描一次
        self.api_base = API_BASE
        self.scan_count = 0
        self.theft_detected_count = 0
    
    def get_all_registered_dna(self) -> List[dict]:
        """获取所有已注册的DNA"""
        try:
            # 通过查询证据链获取所有DNA
            response = requests.get(f"{self.api_base}/audit/blacklist", timeout=10)
            if response.status_code == 200:
                return response.json().get("blacklist", [])
        except Exception as e:
            print(f"获取DNA列表失败: {e}")
        return []
    
    def scan_dna(self, dna_code: str) -> dict:
        """扫描单个DNA"""
        try:
            response = requests.post(
                f"{self.api_base}/sweeper/scan",
                json={
                    "dna_code": dna_code,
                    "engines": ["baidu", "bing"]
                },
                timeout=30
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def run_single_scan(self):
        """执行一次完整扫描"""
        self.scan_count += 1
        print(f"\n{'='*60}")
        print(f"清道夫扫描 #{self.scan_count}")
        print(f"时间: {datetime.now().isoformat()}")
        print(f"{'='*60}")
        
        # 这里简化处理，实际应该从数据库读取所有DNA
        # 现在用测试DNA
        test_dnas = [
            "#龍芯⚡️2026-03-05-BUILD-GUIDE-FOR-AI",
            "#龍芯⚡️2026-03-09-RESOURCE-INVENTORY",
            "#龍芯⚡️2026-03-09-RULE-COVERAGE-CHECK",
            "#龍芯⚡️2026-03-09-RULE-HOOKS-DESIGN",
        ]
        
        for dna in test_dnas:
            print(f"\n扫描: {dna}")
            result = self.scan_dna(dna)
            
            if result.get("theft_detected"):
                self.theft_detected_count += 1
                print(f"🚨 发现盗窃! 结果数: {result.get('total_findings', 0)}")
                for engine in result.get("engines_scanned", []):
                    if engine.get("has_results"):
                        print(f"   - {engine['engine']}: {engine.get('url', 'N/A')[:60]}...")
            else:
                print(f"✅ 未发现异常")
        
        print(f"\n扫描完成: 发现{self.theft_detected_count}次盗窃")
    
    def run_forever(self):
        """持续运行守护进程"""
        print("=" * 60)
        print("龍魂清道夫守护进程启动")
        print(f"扫描间隔: {self.scan_interval}秒")
        print(f"API地址: {self.api_base}")
        print("=" * 60)
        
        while True:
            try:
                self.run_single_scan()
                print(f"\n下次扫描: {self.scan_interval}秒后")
                time.sleep(self.scan_interval)
            except KeyboardInterrupt:
                print("\n守护进程已停止")
                break
            except Exception as e:
                print(f"扫描出错: {e}")
                time.sleep(60)  # 出错后1分钟重试

if __name__ == "__main__":
    import sys
    
    # 支持命令行参数设置扫描间隔
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 3600
    
    daemon = SweeperDaemon(scan_interval=interval)
    daemon.run_forever()
