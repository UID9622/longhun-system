#!/usr/bin/env python3
#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-v5.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
                    龍魂 Kubernetes 控制器 v5.0
═══════════════════════════════════════════════════════════════════════════════
DNA          : #龍芯⚡️2026-06-19-LONGHUN-DEPLOY-v5.0
功能         : K8s資源管理 / 部署控制 / Service調度 / ConfigMap管理 / HPA策略
作者         : 龍魂体系-技能打包专家
协议         : 君子協議 — 非惡意、非濫用、可審計
三色審計     : 🟢 安全通過 / 🟡 警告需審 / 🔴 阻塞風險
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import json
import time
import logging
import subprocess
import tempfile
from datetime import datetime, timezone
from enum import Enum, auto
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any

# 全局常數
DNA標識 = "#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-v5.0"
安全通過 = "🟢"
警告需審 = "🟡"
阻塞風險 = "🔴"
龍印標記 = "🐉"


class K8s資源類型(Enum):
    DEPLOYMENT = "deployment"
    SERVICE = "service"
    CONFIGMAP = "configmap"
    SECRET = "secret"
    INGRESS = "ingress"
    HPA = "horizontalpodautoscaler"
    NAMESPACE = "namespace"


@dataclass
class K8s資源狀態:
    資源名稱: str = ""
    資源類型: str = ""
    命名空間: str = ""
    就緒副本: int = 0
    期望副本: int = 0
    可用副本: int = 0
    運行狀態: str = ""
    創建時間: str = ""
    標籤: Dict[str, Any] = field(default_factory=dict)
    事件: List[str] = field(default_factory=list)
    DNA追溯: str = DNA標識


class 龍魂K8s控制器:
    """
    龍魂 Kubernetes 控制器
    封裝常用 K8s 操作，提供部署管理、服務調度、配置管理等功能
    """

    def __init__(self, 命名空間: str = "longhun", 上下文: str = ""):
        self.命名空間 = 命名空間
        self.上下文 = 上下文
        self.基礎命令 = ["kubectl"]
        if 上下文:
            self.基礎命令.extend(["--context", 上下文])
        self._初始化日誌()
        self._驗證連接()

    def _初始化日誌(self):
        logging.basicConfig(
            level=logging.INFO,
            format=f'{龍印標記} [%(asctime)s] %(levelname)s — %(message)s'
        )
        self.日誌 = logging.getLogger("K8s控制器")

    def _驗證連接(self):
        """驗證 K8s 集群連接"""
        結果 = self._執行(["version", "--client"])
        if 結果["返回碼"] != 0:
            raise RuntimeError("kubectl 未配置或無法連接集群")

        結果 = self._執行(["cluster-info"])
        if 結果["返回碼"] == 0:
            self.日誌.info(f"{安全通過} K8s 集群連接正常")
        else:
            self.日誌.warning(f"{警告需審} K8s 集群連接異常")

    # ═══════════════════════════════════════════════════════════════════════════
    # 核心命令執行
    # ═══════════════════════════════════════════════════════════════════════════

    def _執行(self, 參數: List[str], 超時: int = 60) -> Dict[str, Any]:
        """執行 kubectl 命令"""
        命令 = self.基礎命令 + 參數
        try:
            結果 = subprocess.run(
                命令, capture_output=True, text=True,
                timeout=超時, encoding="utf-8"
            )
            return {
                "返回碼": 結果.returncode,
                "stdout": 結果.stdout,
                "stderr": 結果.stderr,
                "命令": " ".join(命令)
            }
        except subprocess.TimeoutExpired:
            return {"返回碼": -1, "stdout": "", "stderr": f"超時({超時}s)"}
        except FileNotFoundError:
            return {"返回碼": -1, "stdout": "", "stderr": "kubectl 未安裝"}

    # ═══════════════════════════════════════════════════════════════════════════
    # 命名空間管理
    # ═══════════════════════════════════════════════════════════════════════════

    def 創建命名空間(self, 名稱: str = "", 標籤: Dict[str, Any] = None) -> Dict[str, Any]:
        """創建命名空間"""
        名稱 = 名稱 or self.命名空間
        標籤 = 標籤 or {"app.kubernetes.io/managed-by": "longhun-deploy"}

        # 檢查是否已存在
        結果 = self._執行(["get", "namespace", 名稱, "--ignore-not-found"])
        if 名稱 in 結果.get("stdout", ""):
            self.日誌.info(f"{安全通過} 命名空間 '{名稱}' 已存在")
            return {"狀態": "exists", "名稱": 名稱}

        標籤參數 = []
        for 鍵, 值 in 標籤.items():
            標籤參數.extend(["--label", f"{鍵}={值}"])

        結果 = self._執行(["create", "namespace", 名稱] + 標籤參數)
        if 結果["返回碼"] == 0:
            self.日誌.info(f"{安全通過} 命名空間 '{名稱}' 創建成功")
            return {"狀態": "created", "名稱": 名稱}
        else:
            self.日誌.error(f"{阻塞風險} 命名空間創建失敗: {結果['stderr']}")
            return {"狀態": "failed", "錯誤": 結果["stderr"]}

    # ═══════════════════════════════════════════════════════════════════════════
    # Deployment 管理
    # ═══════════════════════════════════════════════════════════════════════════

    def 創建部署(self, 名稱: str, 鏡像: str, 版本標籤: str = "v1",
                 副本數: int = 3, 端口: int = 8080,
                 資源限制: Dict[str, Any] = None, 環境變量: Dict[str, Any] = None,
                 健康檢查路徑: str = "/health") -> Dict[str, Any]:
        """創建 Deployment 資源"""

        資源限制 = 資源限制 or {"cpu": "500m", "memory": "512Mi"}
        環境變量 = 環境變量 or {}

        清單 = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": 名稱,
                "namespace": self.命名空間,
                "labels": {
                    "app": 名稱,
                    "version": 版本標籤,
                    "longhun.dna": DNA標識
                }
            },
            "spec": {
                "replicas": 副本數,
                "selector": {
                    "matchLabels": {"app": 名稱, "version": 版本標籤}
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": 名稱,
                            "version": 版本標籤,
                            "longhun.dna": DNA標識
                        }
                    },
                    "spec": {
                        "containers": [{
                            "name": 名稱,
                            "image": 鏡像,
                            "ports": [{"containerPort": 端口}],
                            "resources": {
                                "limits": 資源限制,
                                "requests": {
                                    "cpu": 資源限制.get("cpu", "100m"),
                                    "memory": 資源限制.get("memory", "128Mi")
                                }
                            },
                            "livenessProbe": {
                                "httpGet": {"path": 健康檢查路徑, "port": 端口},
                                "initialDelaySeconds": 30,
                                "periodSeconds": 10
                            },
                            "readinessProbe": {
                                "httpGet": {"path": "/ready", "port": 端口},
                                "initialDelaySeconds": 5,
                                "periodSeconds": 5
                            },
                            "env": [
                                {"name": 鍵, "value": 值}
                                for 鍵, 值 in 環境變量.items()
                            ]
                        }]
                    }
                }
            }
        }

        return self._應用清單(清單, f"Deployment/{名稱}")

    def 更新鏡像(self, 部署名: str, 新鏡像: str) -> Dict[str, Any]:
        """更新 Deployment 鏡像"""
        結果 = self._執行([
            "set", "image", f"deployment/{部署名}",
            f"{部署名}={新鏡像}",
            "-n", self.命名空間,
            "--record"
        ])

        if 結果["返回碼"] == 0:
            self.日誌.info(f"{安全通過} 鏡像更新成功: {新鏡像}")
            return {"狀態": "updated", "鏡像": 新鏡像}
        else:
            self.日誌.error(f"{阻塞風險} 鏡像更新失敗: {結果['stderr']}")
            return {"狀態": "failed", "錯誤": 結果["stderr"]}

    def 縮放副本(self, 部署名: str, 副本數: int) -> Dict[str, Any]:
        """縮放 Deployment 副本數"""
        結果 = self._執行([
            "scale", "deployment", 部署名,
            "--replicas", str(副本數),
            "-n", self.命名空間
        ])

        if 結果["返回碼"] == 0:
            self.日誌.info(f"{安全通過} 副本縮放至 {副本數}")
            return {"狀態": "scaled", "副本數": 副本數}
        else:
            return {"狀態": "failed", "錯誤": 結果["stderr"]}

    def 獲取部署狀態(self, 部署名: str) -> K8s資源狀態:
        """獲取 Deployment 狀態"""
        結果 = self._執行([
            "get", "deployment", 部署名,
            "-n", self.命名空間,
            "-o", "json"
        ])

        if 結果["返回碼"] != 0:
            return K8s資源狀態(資源名稱=部署名, 運行狀態="not_found")

        數據 = json.loads(結果["stdout"])
        狀態數據 = 數據.get("status", {})

        return K8s資源狀態(
            資源名稱=部署名,
            資源類型="deployment",
            命名空間=self.命名空間,
            就緒副本=狀態數據.get("readyReplicas", 0),
            期望副本=狀態數據.get("replicas", 0),
            可用副本=狀態數據.get("availableReplicas", 0),
            運行狀態="running" if 狀態數據.get("readyReplicas", 0) > 0 else "pending",
            創建時間=數據.get("metadata", {}).get("creationTimestamp", ""),
            標籤=數據.get("metadata", {}).get("labels", {})
        )

    def 等待就緒(self, 部署名: str, 超時秒: int = 300) -> bool:
        """等待 Deployment 完全就緒"""
        self.日誌.info(f"⏳ 等待 {部署名} 就緒 (超時: {超時秒}s)")
        開始 = time.time()

        while time.time() - 開始 < 超時秒:
            結果 = self._執行([
                "rollout", "status",
                f"deployment/{部署名}",
                "-n", self.命名空間,
                "--timeout", "5s"
            ])
            if 結果["返回碼"] == 0:
                self.日誌.info(f"{安全通過} {部署名} 已就緒")
                return True
            time.sleep(5)

        self.日誌.warning(f"{阻塞風險} 等待 {部署名} 就緒超時")
        return False

    # ═══════════════════════════════════════════════════════════════════════════
    # Service 管理
    # ═══════════════════════════════════════════════════════════════════════════

    def 創建服務(self, 名稱: str, 選擇器: Dict[str, Any], 端口映射: List[Dict],
                 類型: str = "ClusterIP") -> Dict[str, Any]:
        """創建 Service 資源"""
        清單 = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": 名稱,
                "namespace": self.命名空間,
                "labels": {"longhun.dna": DNA標識}
            },
            "spec": {
                "type": 類型,
                "selector": 選擇器,
                "ports": 端口映射
            }
        }
        return self._應用清單(清單, f"Service/{名稱}")

    def 更新服務選擇器(self, 服務名: str, 新選擇器: Dict[str, Any]) -> Dict[str, Any]:
        """更新 Service 的標籤選擇器（用於藍綠切換）"""
        選擇器JSON = json.dumps({"spec": {"selector": 新選擇器}})

        結果 = self._執行([
            "patch", "service", 服務名,
            "-n", self.命名空間,
            "--type=merge",
            "-p", 選擇器JSON
        ])

        if 結果["返回碼"] == 0:
            self.日誌.info(f"{安全通過} Service '{服務名}' 選擇器已更新")
            return {"狀態": "patched", "選擇器": 新選擇器}
        else:
            self.日誌.error(f"{阻塞風險} Service 更新失敗: {結果['stderr']}")
            return {"狀態": "failed", "錯誤": 結果["stderr"]}

    # ═══════════════════════════════════════════════════════════════════════════
    # ConfigMap / Secret 管理
    # ═══════════════════════════════════════════════════════════════════════════

    def 創建配置映射(self, 名稱: str, 數據: Dict[str, Any]) -> Dict[str, Any]:
        """創建 ConfigMap"""
        清單 = {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "name": 名稱,
                "namespace": self.命名空間,
                "labels": {"longhun.dna": DNA標識}
            },
            "data": 數據
        }
        return self._應用清單(清單, f"ConfigMap/{名稱}")

    def 創建密鑰(self, 名稱: str, 字符串數據: Dict[str, Any]) -> Dict[str, Any]:
        """創建 Secret"""
        import base64
        編碼數據 = {
            鍵: base64.b64encode(值.encode()).decode()
            for 鍵, 值 in 字符串數據.items()
        }

        清單 = {
            "apiVersion": "v1",
            "kind": "Secret",
            "metadata": {
                "name": 名稱,
                "namespace": self.命名空間,
                "labels": {"longhun.dna": DNA標識}
            },
            "type": "Opaque",
            "data": 編碼數據
        }
        return self._應用清單(清單, f"Secret/{名稱}")

    # ═══════════════════════════════════════════════════════════════════════════
    # HPA 自動伸縮
    # ═══════════════════════════════════════════════════════════════════════════

    def 創建HPA(self, 部署名: str, 最小副本: int = 2, 最大副本: int = 10,
                CPU目標: int = 70, 內存目標: int = 80) -> Dict[str, Any]:
        """創建 HorizontalPodAutoscaler"""
        清單 = {
            "apiVersion": "autoscaling/v2",
            "kind": "HorizontalPodAutoscaler",
            "metadata": {
                "name": f"{部署名}-hpa",
                "namespace": self.命名空間,
                "labels": {"longhun.dna": DNA標識}
            },
            "spec": {
                "scaleTargetRef": {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "name": 部署名
                },
                "minReplicas": 最小副本,
                "maxReplicas": 最大副本,
                "metrics": [
                    {
                        "type": "Resource",
                        "resource": {
                            "name": "cpu",
                            "target": {
                                "type": "Utilization",
                                "averageUtilization": CPU目標
                            }
                        }
                    },
                    {
                        "type": "Resource",
                        "resource": {
                            "name": "memory",
                            "target": {
                                "type": "Utilization",
                                "averageUtilization": 內存目標
                            }
                        }
                    }
                ]
            }
        }
        return self._應用清單(清單, f"HPA/{部署名}-hpa")

    # ═══════════════════════════════════════════════════════════════════════════
    # Ingress 管理
    # ═══════════════════════════════════════════════════════════════════════════

    def 創建入口(self, 名稱: str, 主機: str, 服務名: str,
                 服務端口: int = 80, 路徑: str = "/") -> Dict[str, Any]:
        """創建 Ingress 資源"""
        清單 = {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "Ingress",
            "metadata": {
                "name": 名稱,
                "namespace": self.命名空間,
                "annotations": {
                    "nginx.ingress.kubernetes.io/rewrite-target": "/",
                    "longhun.dna": DNA標識
                }
            },
            "spec": {
                "rules": [{
                    "host": 主機,
                    "http": {
                        "paths": [{
                            "path": 路徑,
                            "pathType": "Prefix",
                            "backend": {
                                "service": {
                                    "name": 服務名,
                                    "port": {"number": 服務端口}
                                }
                            }
                        }]
                    }
                }]
            }
        }
        return self._應用清單(清單, f"Ingress/{名稱}")

    # ═══════════════════════════════════════════════════════════════════════════
    # 藍綠部署支持
    # ═══════════════════════════════════════════════════════════════════════════

    def 獲取藍綠狀態(self, 應用名: str) -> Dict[str, Any]:
        """獲取藍綠雙環境狀態"""
        狀態 = {"blue": None, "green": None, "active": "unknown"}

        for 顏色 in ["blue", "green"]:
            部署名 = f"{應用名}-{顏色}"
            結果 = self._執行([
                "get", "deployment", 部署名,
                "-n", self.命名空間,
                "-o", "json",
                "--ignore-not-found"
            ])
            if 結果["返回碼"] == 0 and 結果["stdout"]:
                數據 = json.loads(結果["stdout"])
                狀態[顏色] = {
                    "副本": 數據.get("status", {}).get("replicas", 0),
                    "就緒": 數據.get("status", {}).get("readyReplicas", 0),
                    "鏡像": 數據.get("spec", {}).get("template", {})
                                      .get("spec", {}).get("containers", [{}])[0]
                                      .get("image", "unknown")
                }

        # 判斷哪個環境活躍
        服務結果 = self._執行([
            "get", "service", 應用名,
            "-n", self.命名空間,
            "-o", "json",
            "--ignore-not-found"
        ])
        if 服務結果["返回碼"] == 0 and 服務結果["stdout"]:
            服務數據 = json.loads(服務結果["stdout"])
            選擇器 = 服務數據.get("spec", {}).get("selector", {})
            狀態["active"] = 選擇器.get("version", "unknown")

        return 狀態

    def 執行藍綠切換(self, 應用名: str, 目標版本: str = "green") -> Dict[str, Any]:
        """執行藍綠環境切換"""
        self.日誌.info(f"{龍印標記} 藍綠切換: {應用名} → {目標版本}")

        # 1. 確保目標環境運行
        目標部署 = f"{應用名}-{目標版本}"
        源版本 = "blue" if 目標版本 == "green" else "green"
        源部署 = f"{應用名}-{源版本}"

        縮放結果 = self.縮放副本(目標部署, 3)
        if 縮放結果["狀態"] != "scaled":
            return {"狀態": "failed", "錯誤": "無法啟動目標環境"}

        # 2. 等待目標就緒
        if not self.等待就緒(目標部署, 超時秒=120):
            return {"狀態": "failed", "錯誤": "目標環境啟動超時"}

        # 3. 切換 Service 選擇器
        服務更新 = self.更新服務選擇器(
            應用名,
            {"app": 應用名, "version": 目標版本}
        )

        if 服務更新["狀態"] != "patched":
            return {"狀態": "failed", "錯誤": "Service 切換失敗"}

        # 4. 縮減源環境
        self.縮放副本(源部署, 0)

        self.日誌.info(f"{安全通過} 藍綠切換完成: {源版本} → {目標版本}")
        return {
            "狀態": "success",
            "源版本": 源版本,
            "目標版本": 目標版本,
            "切換時間": datetime.now(timezone.utc).isoformat()
        }

    # ═══════════════════════════════════════════════════════════════════════════
    # 輔助方法
    # ═══════════════════════════════════════════════════════════════════════════

    def _應用清單(self, 清單: Dict[str, Any], 描述: str) -> Dict[str, Any]:
        """應用 K8s 清單"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as 臨時文件:
            json.dump(清單, 臨時文件)
            臨時路徑 = 臨時文件.name

        try:
            結果 = self._執行(["apply", "-f", 臨時路徑])
            if 結果["返回碼"] == 0:
                self.日誌.info(f"{安全通過} {描述} 應用成功")
                return {"狀態": "applied", "資源": 描述}
            else:
                self.日誌.error(f"{阻塞風險} {描述} 應用失敗: {結果['stderr']}")
                return {"狀態": "failed", "錯誤": 結果["stderr"]}
        finally:
            os.unlink(臨時路徑)

    def 獲取日誌(self, 資源名: str, 資源類型: str = "deployment",
                 行數: int = 100, 跟隨: bool = False) -> Dict[str, Any]:
        """獲取資源日誌"""
        命令 = ["logs", f"{資源類型}/{資源名}", "-n", self.命名空間, "--tail", str(行數)]
        if 跟隨:
            命令.append("-f")

        結果 = self._執行(命令, 超時=300 if 跟隨 else 60)
        return {
            "日誌": 結果["stdout"],
            "狀態": "success" if 結果["返回碼"] == 0 else "failed"
        }

    def 獲取事件(self, 資源名: str = "", 資源類型: str = "") -> List[str]:
        """獲取命名空間事件"""
        命令 = ["get", "events", "-n", self.命名空間, "--sort-by=.lastTimestamp"]
        if 資源名:
            命令.extend(["--field-selector", f"involvedObject.name={資源名}"])

        結果 = self._執行(命令)
        if 結果["返回碼"] == 0:
            return 結果["stdout"].strip().split("\n")
        return []

    def 刪除資源(self, 名稱: str, 資源類型: str = "deployment") -> Dict[str, Any]:
        """刪除 K8s 資源"""
        結果 = self._執行(["delete", 資源類型, 名稱, "-n", self.命名空間])
        if 結果["返回碼"] == 0:
            self.日誌.info(f"{安全通過} {資源類型}/{名稱} 已刪除")
            return {"狀態": "deleted"}
        return {"狀態": "failed", "錯誤": 結果["stderr"]}


# ═══════════════════════════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════════════════════════

def 主函數():
    import argparse

    解析器 = argparse.ArgumentParser(description="龍魂 Kubernetes 控制器")
    解析器.add_argument("--namespace", default="longhun", help="命名空間")
    解析器.add_argument("--context", default="", help="K8s 上下文")
    解析器.add_argument("--create-ns", action="store_true", help="創建命名空間")
    解析器.add_argument("--deploy", action="store_true", help="創建部署")
    解析器.add_argument("--app", default="longhun-app", help="應用名稱")
    解析器.add_argument("--image", default="", help="容器鏡像")
    解析器.add_argument("--replicas", type=int, default=3, help="副本數")
    解析器.add_argument("--status", action="store_true", help="獲取狀態")
    解析器.add_argument("--blue-green-status", action="store_true", help="獲取藍綠狀態")
    解析器.add_argument("--switch", choices=["blue", "green"], help="藍綠切換")

    參數 = 解析器.parse_args()

    控制器 = 龍魂K8s控制器(
        命名空間=參數.namespace,
        上下文=參數.context
    )

    if 參數.create_ns:
        結果 = 控制器.創建命名空間()
        print(json.dumps(結果, ensure_ascii=False, indent=2))

    elif 參數.deploy:
        if not 參數.image:
            print("錯誤: --image 參數必填")
            sys.exit(1)
        結果 = 控制器.創建部署(
            名稱=參數.app,
            鏡像=參數.image,
            副本數=參數.replicas
        )
        print(json.dumps(結果, ensure_ascii=False, indent=2))

    elif 參數.status:
        狀態 = 控制器.獲取部署狀態(參數.app)
        print(json.dumps(asdict(狀態), ensure_ascii=False, indent=2))

    elif 參數.blue_green_status:
        狀態 = 控制器.獲取藍綠狀態(參數.app)
        print(json.dumps(狀態, ensure_ascii=False, indent=2))

    elif 參數.switch:
        結果 = 控制器.執行藍綠切換(參數.app, 參數.switch)
        print(json.dumps(結果, ensure_ascii=False, indent=2))

    else:
        解析器.print_help()


if __name__ == "__main__":
    主函數()
