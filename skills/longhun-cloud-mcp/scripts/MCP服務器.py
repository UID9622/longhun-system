# DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-739c08c8
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

"""
龍魂 MCP 服務器 v5.0
Longhun MCP Server

FastMCP 集成 + 工具定義 + Dockerfile 自動生成 + 配置管理 + Skill 發現與調用
支持龍魂體系 14 個技能的 MCP 協議暴露，統一工具註冊中心

DNA: #龍芯⚡️2026-06-19-LONGHUN-MCP-v5.0
協議: 君子協議·不免責
作者: UID9622
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
import time
import traceback
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

# ──────────────────────────────────────────────
# 全局配置
# ──────────────────────────────────────────────
服務配置 = {
    "服務名稱": "longhun-mcp-server",
    "版本": "5.0.0",
    "端口": int(os.environ.get("MCP_PORT", 8443)),
    "主機": os.environ.get("MCP_HOST", "0.0.0.0"),
    "API前綴": "/mcp",
    "調試模式": os.environ.get("MCP_DEBUG", "false").lower() == "true",
    "日誌級別": os.environ.get("MCP_LOG_LEVEL", "INFO"),
    "DNA": "#龍芯⚡️2026-06-19-LONGHUN-MCP-v5.0",
    "技能目錄": os.environ.get("SKILL_DIR", "/mnt/agents/output/longhun-v5-skills"),
    "最大並發": int(os.environ.get("MCP_MAX_CONCURRENT", 100)),
    "請求超時": int(os.environ.get("MCP_REQUEST_TIMEOUT", 30)),
    "啟用審計": os.environ.get("MCP_AUDIT", "true").lower() == "true",
    "啟用DNA追溯": True,
}

# ──────────────────────────────────────────────
# 三色審計系統
# ──────────────────────────────────────────────
class 審計級別(Enum):
    """三色審計級別"""
    信息 = "🟢"    # 綠色 - 正常操作
    警告 = "🟡"    # 黃色 - 需要注意
    錯誤 = "🔴"    # 紅色 - 嚴重事件
    致命 = "💀"    # 黑色 - 致命錯誤


class 三色審計器:
    """三色審計日誌系統 — 🟢🟡🔴"""

    def __init__(self):
        self.審計記錄: List[Dict[str, Any]] = []
        self.統計 = {
            "🟢信息": 0,
            "🟡警告": 0,
            "🔴錯誤": 0,
            "💀致命": 0,
            "總計": 0,
        }
        self._初始化日誌()

    def _初始化日誌(self):
        """初始化 Python logging"""
        logging.basicConfig(
            level=getattr(logging, 服務配置["日誌級別"]),
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.StreamHandler(sys.stdout),
            ]
        )
        self.日誌器 = logging.getLogger("龍魂MCP")

    def 記錄(self, 級別: 審計級別, 模塊: str, 消息: str, 詳情: Dict = None):
        """記錄一條審計日誌"""
        時間戳 = datetime.now().isoformat()
        記錄項 = {
            "時間戳": 時間戳,
            "級別": 級別.value,
            "級別名": 級別.name,
            "模塊": 模塊,
            "消息": 消息,
            "詳情": 詳情 or {},
            "DNA": 服務配置["DNA"],
        }
        self.審計記錄.append(記錄項)
        self.統計[級別.value + 級別.name] += 1
        self.統計["總計"] += 1

        # 同時輸出到 Python logging
        日誌消息 = f"[{級別.value}{級別.name}] [{模塊}] {消息}"
        if 級別 == 審計級別.信息:
            self.日誌器.info(日誌消息)
        elif 級別 == 審計級別.警告:
            self.日誌器.warning(日誌消息)
        elif 級別 == 審計級別.錯誤:
            self.日誌器.error(日誌消息)
        elif 級別 == 審計級別.致命:
            self.日誌器.critical(日誌消息)

    def 信息(self, 模塊: str, 消息: str, 詳情: Dict = None):
        """記錄信息級日誌 🟢"""
        self.記錄(審計級別.信息, 模塊, 消息, 詳情)

    def 警告(self, 模塊: str, 消息: str, 詳情: Dict = None):
        """記錄警告級日誌 🟡"""
        self.記錄(審計級別.警告, 模塊, 消息, 詳情)

    def 錯誤(self, 模塊: str, 消息: str, 詳情: Dict = None):
        """記錄錯誤級日誌 🔴"""
        self.記錄(審計級別.錯誤, 模塊, 消息, 詳情)

    def 致命(self, 模塊: str, 消息: str, 詳情: Dict = None):
        """記錄致命級日誌 💀"""
        self.記錄(審計級別.致命, 模塊, 消息, 詳情)

    def 獲取報告(self, 限制: int = 100) -> Dict:
        """獲取審計報告"""
        return {
            "統計": self.統計,
            "記錄數": len(self.審計記錄),
            "最近記錄": self.審計記錄[-限制:] if self.審計記錄 else [],
            "DNA": 服務配置["DNA"],
        }

    def 導出日誌(self, 文件路徑: str) -> bool:
        """導出審計日誌到文件"""
        try:
            with open(文件路徑, "w", encoding="utf-8") as 文件:
                json.dump(self.審計記錄, 文件, indent=2, ensure_ascii=False)
            return True
        except Exception as 異常:
            self.錯誤("審計導出", f"導出失敗: {str(異常)}")
            return False


# 全局審計器實例
審計 = 三色審計器()


# ──────────────────────────────────────────────
# DNA 追溯系統
# ──────────────────────────────────────────────
class DNAT追溯器:
    """DNA 追溯鏈管理器"""

    def __init__(self):
        self.追溯鏈: List[Dict] = []
        self.當前節點 = 0
        self._初始化根節點()

    def _初始化根節點(self):
        """初始化根 DNA 節點"""
        根節點 = {
            "節點ID": 0,
            "時間戳": datetime.now().isoformat(),
            "DNA": 服務配置["DNA"],
            "操作": "MCP服務器初始化",
            "父節點": None,
            "簽章": self._生成簽章(服務配置["DNA"], "初始化"),
        }
        self.追溯鏈.append(根節點)
        self.當前節點 = 0

    def _生成簽章(self, DNA: str, 操作: str) -> str:
        """生成節點簽章"""
        import hashlib
        數據 = f"{DNA}:{操作}:{datetime.now().isoformat()}:{服務配置['版本']}"
        return hashlib.sha256(數據.encode("utf-8")).hexdigest()[:16]

    def 添加節點(self, 操作: str, 元數據: Dict = None) -> Dict:
        """添加新的 DNA 追溯節點"""
        self.當前節點 += 1
        節點 = {
            "節點ID": self.當前節點,
            "時間戳": datetime.now().isoformat(),
            "DNA": 服務配置["DNA"],
            "操作": 操作,
            "父節點": self.當前節點 - 1,
            "元數據": 元據 or {},
            "簽章": self._生成簽章(服務配置["DNA"], 操作),
        }
        self.追溯鏈.append(節點)
        審計.信息("DNA追溯", f"節點 #{self.當前節點}: {操作}", {"簽章": 節點["簽章"]})
        return 節點

    def 獲取鏈(self) -> List[Dict]:
        """獲取完整追溯鏈"""
        return self.追溯鏈.copy()

    def 驗證鏈(self) -> bool:
        """驗證追溯鏈完整性"""
        for i, 節點 in enumerate(self.追溯鏈):
            if i == 0:
                if 節點["父節點"] is not None:
                    審計.錯誤("DNA驗證", f"根節點父節點不為空")
                    return False
            else:
                if 節點["父節點"] != i - 1:
                    審計.錯誤("DNA驗證", f"節點 #{i} 父節點鏈接斷裂")
                    return False
        審計.信息("DNA驗證", f"追溯鏈驗證通過，共 {len(self.追溯鏈)} 個節點")
        return True

    def 獲取當前DNA(self) -> str:
        """獲取當前 DNA 標記"""
        return f"{服務配置['DNA']}-NODE{self.當前節點}"


# 全局 DNA 追溯器實例
追溯器 = DNAT追溯器()


# ──────────────────────────────────────────────
# 工具定義數據模型
# ──────────────────────────────────────────────
class 工具參數:
    """工具參數定義"""

    def __init__(self, 名稱: str, 類型: str, 描述: str, 必需: bool = True, 默認值: Any = None):
        self.名稱 = 名稱
        self.類型 = 類型
        self.描述 = 描述
        self.必需 = 必需
        self.默認值 = 默認值

    def to_dict(self) -> Dict:
        return {
            "名稱": self.名稱,
            "類型": self.類型,
            "描述": self.描述,
            "必需": self.必需,
            "默認值": self.默認值,
        }


class 工具定義:
    """MCP 工具定義"""

    def __init__(
        self,
        名稱: str,
        描述: str,
        參數: List[工具參數] = None,
        處理函數: Callable = None,
        分類: str = "general",
        標籤: List[str] = None,
    ):
        self.名稱 = 名稱
        self.描述 = 描述
        self.參數 = 參數 or []
        self.處理函數 = 處理函數
        self.分類 = 分類
        self.標籤 = 標籤 or []
        self.創建時間 = datetime.now().isoformat()
        self.調用次數 = 0
        self.DNA = f"{服務配置['DNA']}-TOOL-{名稱}"

    def to_dict(self) -> Dict:
        return {
            "名稱": self.名稱,
            "描述": self.描述,
            "參數": [p.to_dict() for p in self.參數],
            "分類": self.分類,
            "標籤": self.標籤,
            "創建時間": self.創建時間,
            "調用次數": self.調用次數,
            "DNA": self.DNA,
        }

    def to_mcp_schema(self) -> Dict:
        """轉換為 MCP Schema 格式"""
        屬性 = {}
        必需列表 = []
        for 參數 in self.參數:
            屬性[參數.名稱] = {
                "type": 參數.類型,
                "description": 參數.描述,
            }
            if 參數.必需:
                必需列表.append(參數.名稱)

        return {
            "name": self.名稱,
            "description": self.描述,
            "parameters": {
                "type": "object",
                "properties": 屬性,
                "required": 必需列表,
            },
        }


# ──────────────────────────────────────────────
# Skill 發現與註冊中心
# ──────────────────────────────────────────────
class 技能註冊中心:
    """龍魂 Skill 統一註冊中心"""

    def __init__(self):
        self.工具表: Dict[str, 工具定義] = {}
        self.技能表: Dict[str, Dict] = {}
        self.資源表: Dict[str, Dict] = {}
        self.初始化內建技能()

    def 註冊工具(self, 工具: 工具定義) -> bool:
        """註冊一個 MCP 工具"""
        if 工具.名稱 in self.工具表:
            審計.警告("註冊中心", f"工具 '{工具.名稱}' 已存在，將覆蓋")
        self.工具表[工具.名稱] = 工具
        審計.信息("註冊中心", f"工具已註冊: {工具.名稱}", {"分類": 工具.分類})
        追溯器.添加節點(f"註冊工具: {工具.名稱}", {"分類": 工具.分類})
        return True

    def 註銷工具(self, 名稱: str) -> bool:
        """註銷一個 MCP 工具"""
        if 名稱 not in self.工具表:
            審計.警告("註冊中心", f"工具 '{名稱}' 不存在")
            return False
        del self.工具表[名稱]
        審計.信息("註冊中心", f"工具已註銷: {名稱}")
        return True

    def 獲取工具(self, 名稱: str) -> Optional[工具定義]:
        """獲取工具定義"""
        return self.工具表.get(名稱)

    def 列出工具(self, 分類: str = None) -> List[Dict]:
        """列出所有工具"""
        工具列表 = []
        for 名稱, 工具 in self.工具表.items():
            if 分類 is None or 工具.分類 == 分類:
                工具列表.append(工具.to_dict())
        return 工具列表

    def 獲取MCP工具列表(self) -> List[Dict]:
        """獲取 MCP 格式的工具列表"""
        return [工具.to_mcp_schema() for 工具 in self.工具表.values()]

    def 調用工具(self, 名稱: str, 參數: Dict = None) -> Dict:
        """調用一個工具"""
        工具 = self.工具表.get(名稱)
        if not 工具:
            審計.錯誤("工具調用", f"工具 '{名稱}' 未找到")
            return {
                "狀態": "錯誤",
                "錯誤": f"工具 '{名稱}' 不存在",
                "DNA": 服務配置["DNA"],
            }

        開始時間 = time.time()
        工具.調用次數 += 1

        try:
            if 工具.處理函數:
                結果 = 工具.處理函數(**(參數 or {}))
            else:
                結果 = {"狀態": "成功", "消息": f"工具 '{名稱}' 已執行（無處理函數）"}

            耗時 = round((time.time() - 開始時間) * 1000, 2)
            審計.信息("工具調用", f"工具 '{名稱}' 調用成功，耗時 {耗時}ms")
            追溯器.添加節點(f"調用工具: {名稱}", {"耗時ms": 耗時})

            if isinstance(結果, dict):
                結果["_dna"] = 服務配置["DNA"]
                結果["_elapsed_ms"] = 耗時
            return 結果

        except Exception as 異常:
            耗時 = round((time.time() - 開始時間) * 1000, 2)
            錯誤信息 = traceback.format_exc()
            審計.錯誤("工具調用", f"工具 '{名稱}' 調用失敗: {str(異常)}", {"耗時ms": 耗時})
            return {
                "狀態": "錯誤",
                "錯誤": str(異常),
                "詳情": 錯誤信息 if 服務配置["調試模式"] else None,
                "DNA": 服務配置["DNA"],
                "耗時ms": 耗時,
            }

    def 註冊技能(self, 技能ID: str, 元數據: Dict):
        """註冊一個龍魂 Skill"""
        self.技能表[技能ID] = {
            **元數據,
            "註冊時間": datetime.now().isoformat(),
            "DNA": f"{服務配置['DNA']}-SKILL-{技能ID}",
        }
        審計.信息("技能註冊", f"Skill '{技能ID}' 已註冊")

    def 發現技能(self) -> List[Dict]:
        """發現所有已註冊的 Skill"""
        return list(self.技能表.values())

    def 註冊資源(self, URI: str, 名稱: str, 類型: str = "text/plain", 內容: str = ""):
        """註冊一個 MCP 資源"""
        self.資源表[URI] = {
            "URI": URI,
            "名稱": 名稱,
            "類型": 類型,
            "內容": 內容,
            "註冊時間": datetime.now().isoformat(),
        }
        審計.信息("資源註冊", f"資源 '{URI}' 已註冊")

    def 獲取資源(self, URI: str) -> Optional[Dict]:
        """獲取資源"""
        return self.資源表.get(URI)

    def 初始化內建技能(self):
        """初始化龍魂體系 14 個內建技能"""
        龍魂技能列表 = [
            {
                "ID": "algorithmic-art",
                "名稱": "算法藝術生成器",
                "描述": "Perlin噪聲·Flow Field·粒子系統·實時控制",
                "類型": "visualization",
                "分類": "creative",
            },
            {
                "ID": "brand-guidelines",
                "名稱": "品牌規範設計器",
                "描述": "品牌色彩·字體規範·視覺元素·設計規範",
                "類型": "visualization",
                "分類": "creative",
            },
            {
                "ID": "canvas-design",
                "名稱": "畫布設計工作室",
                "描述": "Canvas繪畫·圖層系統·濾鏡效果·實時渲染",
                "類型": "visualization",
                "分類": "creative",
            },
            {
                "ID": "doc-coauthoring",
                "名稱": "文檔協作編輯",
                "描述": "實時編輯·版本控制·評論系統·權限管理",
                "類型": "collaboration",
                "分類": "productivity",
            },
            {
                "ID": "internal-comms",
                "名稱": "內部通訊",
                "描述": "消息通知·任務分配·進度追蹤·團隊協作",
                "類型": "communication",
                "分類": "productivity",
            },
            {
                "ID": "mcp-builder",
                "名稱": "MCP構建器",
                "描述": "FastMCP集成·自動代碼生成·Docker支持",
                "類型": "code-generation",
                "分類": "devops",
            },
            {
                "ID": "skill-creator",
                "名稱": "Skill創建器",
                "描述": "模板生成·框架搭建·配置向導·驗證檢查",
                "類型": "code-generation",
                "分類": "devops",
            },
            {
                "ID": "slack-gif-creator",
                "名稱": "Slack GIF創建器",
                "描述": "GIF動畫生成·Slack發送·自動化流程",
                "類型": "automation",
                "分類": "productivity",
            },
            {
                "ID": "theme-factory",
                "名稱": "主題工廠",
                "描述": "色彩系統·字體組合·主題導出·CSS生成",
                "類型": "code-generation",
                "分類": "creative",
            },
            {
                "ID": "web-artifacts-builder",
                "名稱": "Web構件構建器",
                "描述": "React組件·HTML模板·CSS框架·即時預覽",
                "類型": "code-generation",
                "分類": "devops",
            },
            {
                "ID": "longhun-asr",
                "名稱": "龍魂語音識別",
                "描述": "語音轉文字·多語言支持·實時識別·批量處理",
                "類型": "ai",
                "分類": "intelligence",
            },
            {
                "ID": "longhun-ocr",
                "名稱": "龍魂文字識別",
                "描述": "圖像轉文字·多語言OCR·表格識別·文檔結構化",
                "類型": "ai",
                "分類": "intelligence",
            },
            {
                "ID": "longhun-nlp",
                "名稱": "龍魂自然語言處理",
                "描述": "文本分析·情感分析·實體識別·摘要生成",
                "類型": "ai",
                "分類": "intelligence",
            },
            {
                "ID": "longhun-finance",
                "名稱": "龍魂金融分析",
                "描述": "財務數據·報表生成·趨勢分析·風險評估",
                "類型": "analytics",
                "分類": "business",
            },
        ]

        for 技能 in 龍魂技能列表:
            self.註冊技能(技能["ID"], 技能)

        審計.信息("註冊中心", f"已初始化 {len(龍魂技能列表)} 個內建技能")
        追溯器.添加節點("初始化內建技能", {"數量": len(龍魂技能列表)})


# 全局註冊中心實例
註冊中心 = 技能註冊中心()


# ──────────────────────────────────────────────
# Dockerfile 自動生成器
# ──────────────────────────────────────────────
class Docker文件生成器:
    """Dockerfile 自動生成器"""

    def __init__(self):
        self.模板庫 = {
            "python": self._python模板,
            "node": self._node模板,
            "go": self._go模板,
            "rust": self._rust模板,
            "java": self._java模板,
        }

    def _python模板(self, 配置: Dict) -> str:
        """Python 項目 Dockerfile 模板"""
        基礎鏡像 = 配置.get("基礎鏡像", "python:3.11-slim")
        工作目錄 = 配置.get("工作目錄", "/app")
        端口 = 配置.get("端口", 8000)
        啟動命令 = 配置.get("啟動命令", "python server.py")
        依賴文件 = 配置.get("依賴文件", "requirements.txt")
        安裝命令 = 配置.get("安裝命令", f"pip install --no-cache-dir -r {依賴文件}")
        額外步驟 = 配置.get("額外步驟", "")
        健康檢查 = 配置.get("健康檢查", f"HEALTHCHECK --interval=30s --timeout=5s --retries=3 \\\n  CMD curl -f http://localhost:{端口}/health || exit 1")

        return f"""# 龍魂 MCP 服務 Dockerfile
# 自動生成於 {datetime.now().isoformat()}
# DNA: {服務配置['DNA']}

FROM {基礎鏡像}

# 設置工作目錄
WORKDIR {工作目錄}

# 安裝系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \\
    curl ca-certificates && \\
    rm -rf /var/lib/apt/lists/*

# 複製依賴文件
COPY {依賴文件} .

# 安裝 Python 依賴
RUN {安裝命令}

{額外步驟}

# 複製應用代碼
COPY . .

# 健康檢查
{健康檢查}

# 暴露端口
EXPOSE {端口}

# 啟動命令
CMD ["{啟動命令.split()[0]}", "{啟動命令.split()[1] if len(啟動命令.split()) > 1 else ''}"]

# 標籤
LABEL maintainer="UID9622"
LABEL version="{服務配置['版本']}"
LABEL dna="{服務配置['DNA']}"
"""

    def _node模板(self, 配置: Dict) -> str:
        """Node.js 項目 Dockerfile 模板"""
        return f"""# 龍魂 Node.js 服務 Dockerfile
FROM node:18-slim

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE {配置.get('端口', 3000)}

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \\
  CMD curl -f http://localhost:{配置.get('端口', 3000)}/health || exit 1

CMD ["node", "{配置.get('入口', 'index.js')}"]

LABEL dna="{服務配置['DNA']}"
"""

    def _go模板(self, 配置: Dict) -> str:
        """Go 項目 Dockerfile 模板"""
        return f"""# 龍魂 Go 服務 Dockerfile
FROM golang:1.21-alpine AS builder

WORKDIR /build
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o app {配置.get('入口', 'main.go')}

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/

COPY --from=builder /build/app .

EXPOSE {配置.get('端口', 8080)}

CMD ["./app"]

LABEL dna="{服務配置['DNA']}"
"""

    def _rust模板(self, 配置: Dict) -> str:
        """Rust 項目 Dockerfile 模板"""
        return f"""# 龍魂 Rust 服務 Dockerfile
FROM rust:1.70-slim AS builder

WORKDIR /usr/src/app
COPY Cargo.toml Cargo.lock ./
COPY src ./src

RUN cargo build --release

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/src/app/target/release/{配置.get('項目名', 'app')} /usr/local/bin/app

EXPOSE {配置.get('端口', 8080)}

CMD ["app"]

LABEL dna="{服務配置['DNA']}"
"""

    def _java模板(self, 配置: Dict) -> str:
        """Java 項目 Dockerfile 模板"""
        return f"""# 龍魂 Java 服務 Dockerfile
FROM eclipse-temurin:17-jdk-alpine AS builder

WORKDIR /app
COPY . .
RUN ./mvnw clean package -DskipTests

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

COPY --from=builder /app/target/*.jar app.jar

EXPOSE {配置.get('端口', 8080)}

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \\
  CMD wget --quiet --tries=1 --spider http://localhost:{配置.get('端口', 8080)}/health || exit 1

ENTRYPOINT ["java", "-jar", "app.jar"]

LABEL dna="{服務配置['DNA']}"
"""

    def 生成(self, 語言: str = "python", 配置: Dict = None) -> str:
        """生成 Dockerfile"""
        配置 = 配置 or {}
        生成器 = self.模板庫.get(語言)
        if not 生成器:
            審計.錯誤("Docker生成", f"不支持的語言: {語言}")
            raise ValueError(f"不支持的語言: {語言}，支持: {list(self.模板庫.keys())}")

        內容 = 生成器(配置)
        審計.信息("Docker生成", f"已生成 {語言} 的 Dockerfile")
        追溯器.添加節點(f"生成Dockerfile: {語言}")
        return 內容

    def 生成Compose(self, 服務列表: List[Dict] = None) -> str:
        """生成 docker-compose.yml"""
        服務列表 = 服務列表 or [
            {
                "名稱": "mcp-server",
                "鏡像": "longhun-mcp-server:latest",
                "端口": "8443:8443",
                "環境": {"MCP_PORT": "8443", "MCP_DEBUG": "false"},
            }
        ]

        服務定義 = ""
        for 服務 in 服務列表:
            環境變量 = "\n".join([f"      - {k}={v}" for k, v in 服務.get("環境", {}).items()])
            服務定義 += f"""
  {服務['名稱']}:
    image: {服務['鏡像']}
    ports:
      - "{服務['端口']}"
    environment:
{環境變量}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:{服務.get('內部端口', 8443)}/health"]
      interval: 30s
      timeout: 5s
      retries: 3
"""

        return f"""# 龍魂 MCP 服務 Docker Compose
# 自動生成於 {datetime.now().isoformat()}
# DNA: {服務配置['DNA']}

version: "3.8"

services:
{服務定義}

networks:
  default:
    name: longhun-mcp-network

volumes:
  mcp-data:
    driver: local
"""


# 全局 Dockerfile 生成器實例
Docker生成器 = Docker文件生成器()


# ──────────────────────────────────────────────
# 配置管理器
# ──────────────────────────────────────────────
class 配置管理器:
    """MCP 配置管理器"""

    def __init__(self, 配置路徑: str = None):
        self.配置路徑 = 配置路徑 or os.path.join(
            服務配置["技能目錄"], "..", "mcp_config.json"
        )
        self.運行時配置 = {}
        self.加載配置()

    def 加載配置(self) -> Dict:
        """從文件加載配置"""
        if os.path.exists(self.配置路徑):
            try:
                with open(self.配置路徑, "r", encoding="utf-8") as 文件:
                    self.運行時配置 = json.load(文件)
                審計.信息("配置管理", f"配置已加載: {self.配置路徑}")
            except Exception as 異常:
                審計.錯誤("配置管理", f"配置加載失敗: {str(異常)}")
                self.運行時配置 = self._默認配置()
        else:
            self.運行時配置 = self._默認配置()
            self.保存配置()
        return self.運行時配置

    def _默認配置(self) -> Dict:
        """生成默認配置"""
        return {
            "服務名稱": 服務配置["服務名稱"],
            "版本": 服務配置["版本"],
            "DNA": 服務配置["DNA"],
            "工具註冊表": [],
            "技能發現": {"自動發現": True, "掃描間隔": 60},
            "審計": {"啟用": True, "保留天數": 30},
            "安全": {
                "認證": False,
                "令牌有效期": 3600,
                "速率限制": 100,
            },
            "生成": {
                "Dockerfile": {"默認語言": "python"},
                "Compose": {"包含健康檢查": True},
            },
            "創建時間": datetime.now().isoformat(),
        }

    def 保存配置(self) -> bool:
        """保存配置到文件"""
        try:
            os.makedirs(os.path.dirname(self.配置路徑), exist_ok=True)
            with open(self.配置路徑, "w", encoding="utf-8") as 文件:
                json.dump(self.運行時配置, 文件, indent=2, ensure_ascii=False)
            審計.信息("配置管理", f"配置已保存: {self.配置路徑}")
            return True
        except Exception as 異常:
            審計.錯誤("配置管理", f"配置保存失敗: {str(異常)}")
            return False

    def 獲取(self, 鍵: str, 默認值=None):
        """獲取配置項"""
        return self.運行時配置.get(鍵, 默認值)

    def 設置(self, 鍵: str, 值: Any):
        """設置配置項"""
        self.運行時配置[鍵] = 值
        審計.信息("配置管理", f"配置已更新: {鍵}")

    def 獲取全部(self) -> Dict:
        """獲取全部配置"""
        return self.運行時配置.copy()


# 全局配置管理器實例
配置 = 配置管理器()


# ──────────────────────────────────────────────
# 內建工具處理函數
# ──────────────────────────────────────────────
def 工具_執行技能(技能ID: str = "", 參數: Dict = None) -> Dict:
    """執行龍魂技能"""
    參數 = 參數 or {}
    審計.信息("技能執行", f"執行技能: {技能ID}", 參數)
    return {
        "狀態": "成功",
        "技能ID": 技能ID,
        "參數": 參數,
        "結果": f"技能 '{技能ID}' 執行完成",
        "時間戳": datetime.now().isoformat(),
    }


def 工具_查詢DNA(查詢: str = "") -> Dict:
    """查詢 DNA 鏈信息"""
    鏈 = 追溯器.獲取鏈()
    return {
        "狀態": "成功",
        "DNA": 追溯器.獲取當前DNA(),
        "查詢": 查詢,
        "節點數": len(鏈),
        "追溯鏈": 鏈 if not 查詢 else [n for n in 鏈 if 查詢 in str(n)],
        "驗證結果": 追溯器.驗證鏈(),
    }


def 工具_獲取狀態() -> Dict:
    """獲取系統狀態"""
    return {
        "狀態": "運行中",
        "服務名稱": 服務配置["服務名稱"],
        "版本": 服務配置["版本"],
        "DNA": 服務配置["DNA"],
        "運行時間": datetime.now().isoformat(),
        "工具數": len(註冊中心.工具表),
        "技能數": len(註冊中心.技能表),
        "資源數": len(註冊中心.資源表),
        "審計統計": 審計.統計,
    }


def 工具_列出技能(分類: str = "", 類型: str = "") -> Dict:
    """列出所有龍魂技能"""
    技能列表 = 註冊中心.發現技能()
    if 分類:
        技能列表 = [s for s in 技能列表 if s.get("分類") == 分類]
    if 類型:
        技能列表 = [s for s in 技能列表 if s.get("類型") == 類型]
    return {
        "狀態": "成功",
        "總數": len(技能列表),
        "技能": 技能列表,
    }


def 工具_生成Dockerfile(語言: str = "python", 項目配置: Dict = None) -> Dict:
    """自動生成 Dockerfile"""
    項目配置 = 項目配置 or {}
    try:
        內容 = Docker生成器.生成(語言, 項目配置)
        return {
            "狀態": "成功",
            "語言": 語言,
            "Dockerfile": 內容,
            "提示": f"已生成 {語言} Dockerfile，請複製內容保存到項目根目錄",
        }
    except Exception as 異常:
        return {"狀態": "錯誤", "錯誤": str(異常)}


def 工具_生成Compose(服務列表: List[Dict] = None) -> Dict:
    """自動生成 docker-compose.yml"""
    try:
        內容 = Docker生成器.生成Compose(服務列表)
        return {
            "狀態": "成功",
            "docker_compose_yml": 內容,
            "提示": "已生成 docker-compose.yml，請複製內容保存到項目根目錄",
        }
    except Exception as 異常:
        return {"狀態": "錯誤", "錯誤": str(異常)}


def 工具_註冊工具(名稱: str = "", 描述: str = "", 參數定義: List[Dict] = None) -> Dict:
    """動態註冊一個 MCP 工具"""
    參數定義 = 參數定義 or []
    if not 名稱 or not 描述:
        return {"狀態": "錯誤", "錯誤": "名稱和描述不能為空"}

    參數列表 = []
    for p in 參數定義:
        參數列表.append(工具參數(
            名稱=p.get("名稱", "param"),
            類型=p.get("類型", "string"),
            描述=p.get("描述", ""),
            必需=p.get("必需", True),
        ))

    工具 = 工具定義(
        名稱=名稱,
        描述=描述,
        參數=參數列表,
        分類="dynamic",
    )
    註冊中心.註冊工具(工具)
    return {"狀態": "成功", "工具": 工具.to_dict()}


def 工具_獲取審計日誌(限制: int = 100, 級別: str = "") -> Dict:
    """獲取三色審計日誌"""
    報告 = 審計.獲取報告(限制)
    if 級別:
        報告["最近記錄"] = [r for r in 報告["最近記錄"] if r["級別名"] == 級別]
    return {"狀態": "成功", **報告}


def 工具_健康檢查() -> Dict:
    """MCP 服務健康檢查"""
    return {
        "狀態": "健康",
        "服務": 服務配置["服務名稱"],
        "版本": 服務配置["版本"],
        "DNA": 服務配置["DNA"],
        "時間戳": datetime.now().isoformat(),
        "組件": {
            "註冊中心": "正常" if len(註冊中心.工具表) > 0 else "警告",
            "審計系統": "正常",
            "DNA追溯": "正常" if 追溯器.驗證鏈() else "異常",
        },
    }


def 工具_調用MCP(工具名: str = "", 工具參數: Dict = None) -> Dict:
    """調用已註冊的 MCP 工具"""
    if not 工具名:
        return {"狀態": "錯誤", "錯誤": "工具名不能為空"}
    return 註冊中心.調用工具(工具名, 工具參數 or {})


def 工具_發現資源(前綴: str = "") -> Dict:
    """發現所有 MCP 資源"""
    資源列表 = []
    for URI, 資源 in 註冊中心.資源表.items():
        if not 前綴 or URI.startswith(前綴):
            資源列表.append(資源)
    return {
        "狀態": "成功",
        "總數": len(資源列表),
        "資源": 資源列表,
    }


# ──────────────────────────────────────────────
# FastMCP 服務器框架
# ──────────────────────────────────────────────
class MCP服務器:
    """龍魂 FastMCP 服務器"""

    def __init__(self):
        self.啟動時間 = time.time()
        self.運行中 = False
        self.應用 = None
        審計.信息("MCP服務器", "服務器初始化完成")
        追溯器.添加節點("MCP服務器創建")

    def 註冊內建工具(self):
        """註冊所有內建工具"""
        內建工具 = [
            工具定義(
                名稱="execute-skill",
                描述="執行龍魂體系中的技能，支持所有 14 個內建技能",
                參數=[
                    工具參數("技能ID", "string", "技能標識符，如 algorithmic-art", True),
                    工具參數("參數", "object", "技能執行參數", False, {}),
                ],
                處理函數=工具_執行技能,
                分類="core",
                標籤=["skill", "execution"],
            ),
            工具定義(
                名稱="query-dna",
                描述="查詢 DNA 追溯鏈信息，驗證追溯鏈完整性",
                參數=[
                    工具參數("查詢", "string", "查詢關鍵詞，留空返回全部", False, ""),
                ],
                處理函數=工具_查詢DNA,
                分類="core",
                標籤=["dna", "traceability"],
            ),
            工具定義(
                名稱="get-status",
                描述="獲取 MCP 服務器運行狀態，包括工具數、技能數、審計統計",
                參數=[],
                處理函數=工具_獲取狀態,
                分類="core",
                標籤=["status", "monitoring"],
            ),
            工具定義(
                名稱="list-skills",
                描述="列出所有龍魂技能，支持按分類和類型篩選",
                參數=[
                    工具參數("分類", "string", "篩選分類，如 creative/devops/ai", False, ""),
                    工具參數("類型", "string", "篩選類型，如 visualization/code-generation", False, ""),
                ],
                處理函數=工具_列出技能,
                分類="discovery",
                標籤=["skill", "discovery", "list"],
            ),
            工具定義(
                名稱="generate-dockerfile",
                描述="自動生成 Dockerfile，支持 Python/Node/Go/Rust/Java 五種語言",
                參數=[
                    工具參數("語言", "string", "項目語言: python/node/go/rust/java", False, "python"),
                    工具參數("項目配置", "object", "項目配置選項", False, {}),
                ],
                處理函數=工具_生成Dockerfile,
                分類="generation",
                標籤=["docker", "dockerfile", "generate"],
            ),
            工具定義(
                名稱="generate-compose",
                描述="自動生成 docker-compose.yml，支持多服務編排",
                參數=[
                    工具參數("服務列表", "array", "服務配置列表", False, None),
                ],
                處理函數=工具_生成Compose,
                分類="generation",
                標籤=["docker", "compose", "orchestration"],
            ),
            工具定義(
                名稱="register-tool",
                描述="動態註冊一個新的 MCP 工具到註冊中心",
                參數=[
                    工具參數("名稱", "string", "工具名稱，必須唯一", True),
                    工具參數("描述", "string", "工具描述", True),
                    工具參數("參數定義", "array", "參數定義列表", False, []),
                ],
                處理函數=工具_註冊工具,
                分類="management",
                標籤=["tool", "register", "dynamic"],
            ),
            工具定義(
                名稱="get-audit-logs",
                描述="獲取三色審計日誌，支持按級別篩選",
                參數=[
                    工具參數("限制", "integer", "返回記錄數限制", False, 100),
                    工具參數("級別", "string", "篩選級別: 信息/警告/錯誤", False, ""),
                ],
                處理函數=工具_獲取審計日誌,
                分類="audit",
                標籤=["audit", "logs", "monitoring"],
            ),
            工具定義(
                名稱="health-check",
                描述="MCP 服務健康檢查，返回組件狀態",
                參數=[],
                處理函數=工具_健康檢查,
                分類="core",
                標籤=["health", "check"],
            ),
            工具定義(
                名稱="call-mcp",
                描述="調用已註冊的 MCP 工具，通用調用接口",
                參數=[
                    工具參數("工具名", "string", "要調用的工具名稱", True),
                    工具參數("工具參數", "object", "工具調用參數", False, {}),
                ],
                處理函數=工具_調用MCP,
                分類="core",
                標籤=["mcp", "call", "invoke"],
            ),
            工具定義(
                名稱="discover-resources",
                描述="發現所有已註冊的 MCP 資源",
                參數=[
                    工具參數("前綴", "string", "URI 前綴篩選", False, ""),
                ],
                處理函數=工具_發現資源,
                分類="discovery",
                標籤=["resource", "discovery"],
            ),
        ]

        for 工具 in 內建工具:
            註冊中心.註冊工具(工具)

        # 註冊內建資源
        註冊中心.註冊資源(
            URI="dna://chain",
            名稱="DNA追溯鏈",
            類型="application/json",
            內容=json.dumps(追溯器.獲取鏈(), ensure_ascii=False),
        )
        註冊中心.註冊資源(
            URI="skills://list",
            名稱="技能列表",
            類型="application/json",
            內容=json.dumps(註冊中心.發現技能(), ensure_ascii=False),
        )
        註冊中心.註冊資源(
            URI="tools://registry",
            名稱="工具註冊表",
            類型="application/json",
            內容=json.dumps(註冊中心.列出工具(), ensure_ascii=False),
        )
        註冊中心.註冊資源(
            URI="audit://logs",
            名稱="審計日誌",
            類型="application/json",
            內容="",
        )
        註冊中心.註冊資源(
            URI="config://current",
            名稱="當前配置",
            類型="application/json",
            內容=json.dumps(配置.獲取全部(), ensure_ascii=False),
        )

        審計.信息("MCP服務器", f"已註冊 {len(內建工具)} 個內建工具和 5 個資源")
        追溯器.添加節點("註冊內建工具", {"工具數": len(內建工具)})

    def 構建HTTP服務器(self):
        """構建 HTTP 服務器（無外部依賴模式）"""
        from http.server import HTTPServer, BaseHTTPRequestHandler
        import urllib.parse

        服務器實例 = self

        class MCP請求處理器(BaseHTTPRequestHandler):
            """MCP HTTP 請求處理器"""

            def _發送JSON(self, 數據: Dict, 狀態碼: int = 200):
                """發送 JSON 響應"""
                self.send_response(狀態碼)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("X-Longhun-DNA", 服務配置["DNA"])
                self.send_header("X-MCP-Version", 服務配置["版本"])
                self.end_headers()
                self.wfile.write(json.dumps(數據, indent=2, ensure_ascii=False).encode("utf-8"))

            def _讀取JSON(self) -> Dict:
                """讀取請求 JSON 體"""
                長度 = int(self.headers.get("Content-Length", 0))
                if 長度 > 0:
                    數據 = self.rfile.read(長度).decode("utf-8")
                    return json.loads(數據)
                return {}

            def _解析查詢(self) -> Dict:
                """解析 URL 查詢參數"""
                解析 = urllib.parse.urlparse(self.path)
                return dict(urllib.parse.parse_qsl(解析.query))

            def do_GET(self):
                """處理 GET 請求"""
                路徑 = urllib.parse.urlparse(self.path).path
                查詢 = self._解析查詢()

                try:
                    if 路徑 == "/health" or 路徑 == f"{服務配置['API前綴']}/health":
                        self._發送JSON(工具_健康檢查())

                    elif 路徑 == f"{服務配置['API前綴']}/tools":
                        self._發送JSON({
                            "狀態": "成功",
                            "工具": 註冊中心.獲取MCP工具列表(),
                        })

                    elif 路徑 == f"{服務配置['API前綴']}/skills":
                        結果 = 工具_列出技能(
                            分類=查詢.get("分類", ""),
                            類型=查詢.get("類型", ""),
                        )
                        self._發送JSON(結果)

                    elif 路徑 == f"{服務配置['API前綴']}/dna":
                        self._發送JSON(工具_查詢DNA(查詢.get("查詢", "")))

                    elif 路徑 == f"{服務配置['API前綴']}/status":
                        self._發送JSON(工具_獲取狀態())

                    elif 路徑 == f"{服務配置['API前綴']}/audit/logs":
                        結果 = 工具_獲取審計日誌(
                            限制=int(查詢.get("限制", 100)),
                            級別=查詢.get("級別", ""),
                        )
                        self._發送JSON(結果)

                    elif 路徑 == f"{服務配置['API前綴']}/resources":
                        結果 = 工具_發現資源(查詢.get("前綴", ""))
                        self._發送JSON(結果)

                    elif 路徑 == f"{服務配置['API前綴']}":
                        self._發送JSON({
                            "服務": 服務配置["服務名稱"],
                            "版本": 服務配置["版本"],
                            "DNA": 服務配置["DNA"],
                            "端點": {
                                "健康檢查": f"GET {服務配置['API前綴']}/health",
                                "工具列表": f"GET {服務配置['API前綴']}/tools",
                                "技能列表": f"GET {服務配置['API前綴']}/skills",
                                "DNA追溯": f"GET {服務配置['API前綴']}/dna",
                                "狀態": f"GET {服務配置['API前綴']}/status",
                                "審計日誌": f"GET {服務配置['API前綴']}/audit/logs",
                                "資源發現": f"GET {服務配置['API前綴']}/resources",
                                "工具調用": f"POST {服務配置['API前綴']}/call",
                            },
                        })

                    else:
                        self._發送JSON({
                            "狀態": "錯誤",
                            "錯誤": f"路徑未找到: {路徑}",
                            "可用端點": [
                                "/mcp/",
                                "/mcp/health",
                                "/mcp/tools",
                                "/mcp/skills",
                                "/mcp/dna",
                                "/mcp/status",
                                "/mcp/audit/logs",
                                "/mcp/resources",
                                "/mcp/call",
                            ],
                        }, 404)

                except Exception as 異常:
                    審計.錯誤("HTTP-GET", f"請求處理錯誤: {str(異常)}")
                    self._發送JSON({
                        "狀態": "錯誤",
                        "錯誤": str(異常),
                    }, 500)

            def do_POST(self):
                """處理 POST 請求"""
                路徑 = urllib.parse.urlparse(self.path).path
                請求體 = self._讀取JSON()

                try:
                    if 路徑 == f"{服務配置['API前綴']}/call":
                        結果 = 註冊中心.調用工具(
                            請求體.get("工具名", ""),
                            請求體.get("工具參數", {}),
                        )
                        self._發送JSON(結果)

                    elif 路徑 == f"{服務配置['API前綴']}/tools/register":
                        結果 = 工具_註冊工具(
                            名稱=請求體.get("名稱", ""),
                            描述=請求體.get("描述", ""),
                            參數定義=請求體.get("參數定義", []),
                        )
                        self._發送JSON(結果)

                    elif 路徑 == f"{服務配置['API前綴']}/dockerfile":
                        結果 = 工具_生成Dockerfile(
                            語言=請求體.get("語言", "python"),
                            項目配置=請求體.get("項目配置", {}),
                        )
                        self._發送JSON(結果)

                    elif 路徑 == f"{服務配置['API前綴']}/compose":
                        結果 = 工具_生成Compose(請求體.get("服務列表"))
                        self._發送JSON(結果)

                    else:
                        self._發送JSON({
                            "狀態": "錯誤",
                            "錯誤": f"POST 路徑未找到: {路徑}",
                        }, 404)

                except Exception as 異常:
                    審計.錯誤("HTTP-POST", f"請求處理錯誤: {str(異常)}")
                    self._發送JSON({
                        "狀態": "錯誤",
                        "錯誤": str(異常),
                    }, 500)

            def log_message(self, format, *args):
                """自定義日誌輸出"""
                審計.信息("HTTP", f"{self.address_string()} - {format % args}")

        return HTTPServer, MCP請求處理器

    def 啟動(self):
        """啟動 MCP 服務器"""
        審計.信息("MCP服務器", "=" * 50)
        審計.信息("MCP服務器", "龍魂 MCP 服務器啟動中...")
        審計.信息("MCP服務器", f"版本: {服務配置['版本']}")
        審計.信息("MCP服務器", f"DNA: {服務配置['DNA']}")

        # 註冊內建工具
        self.註冊內建工具()

        # 構建 HTTP 服務器
        HTTPServer, 處理器 = self.構建HTTP服務器()

        服務地址 = (服務配置["主機"], 服務配置["端口"])
        httpd = HTTPServer(服務地址, 處理器)

        審計.信息("MCP服務器", f"服務器已啟動: http://{服務配置['主機']}:{服務配置['端口']}{服務配置['API前綴']}/")
        審計.信息("MCP服務器", "=" * 50)
        追溯器.添加節點("MCP服務器啟動", {"地址": f"{服務配置['主機']}:{服務配置['端口']}"})

        self.運行中 = True
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            審計.信息("MCP服務器", "收到中斷信號，正在關閉...")
        finally:
            httpd.server_close()
            self.運行中 = False
            審計.信息("MCP服務器", "服務器已關閉")
            追溯器.添加節點("MCP服務器關閉")


# ──────────────────────────────────────────────
# FastMCP 適配器（可選，當 fastmcp 可用時）
# ──────────────────────────────────────────────
class FastMCP適配器:
    """FastMCP 框架適配器"""

    def __init__(self, 服務器: MCP服務器):
        self.服務器 = 服務器
        self.mcp服務器 = None

    def 初始化(self):
        """初始化 FastMCP 服務器"""
        try:
            from fastmcp import FastMCP

            self.mcp服務器 = FastMCP(服務配置["服務名稱"])

            # 將註冊中心的工具轉換為 FastMCP 工具
            for 名稱, 工具 in 註冊中心.工具表.items():
                self._註冊FastMCP工具(工具)

            審計.信息("FastMCP", "FastMCP 適配器初始化完成")
            return True

        except ImportError:
            審計.警告("FastMCP", "fastmcp 未安裝，使用內建 HTTP 服務器")
            return False

    def _註冊FastMCP工具(self, 工具: 工具定義):
        """註冊工具到 FastMCP"""
        # 動態創建處理函數
        def 處理函數(**kwargs):
            return 註冊中心.調用工具(工具.名稱, kwargs)

        # 使用 FastMCP 的工具註冊
        if self.mcp服務器:
            self.mcp服務器.tool(name=工具.名稱, description=工具.描述)(處理函數)
            審計.信息("FastMCP", f"工具已註冊: {工具.名稱}")

    def 啟動(self):
        """啟動 FastMCP 服務器"""
        if self.mcp服務器:
            審計.信息("FastMCP", "啟動 FastMCP 服務器...")
            # FastMCP 的啟動方式取決於版本
            # 這裡提供通用的 SSE/Stdio 支持
            追溯器.添加節點("FastMCP啟動")


# ──────────────────────────────────────────────
# 主入口
# ──────────────────────────────────────────────
def 主函數():
    """主入口函數"""
    print("🐉 龍魂 MCP 服務器 v5.0")
    print(f"DNA: {服務配置['DNA']}")
    print("=" * 50)

    # 創建並啟動服務器
    服務器 = MCP服務器()

    # 嘗試 FastMCP 適配器
    適配器 = FastMCP適配器(服務器)
    if not 適配器.初始化():
        # 回退到內建 HTTP 服務器
        審計.信息("系統", "使用內建 HTTP 服務器")

    服務器.啟動()


if __name__ == "__main__":
    主函數()
