# 🌐 数字人民币全球化系统｜完整技术方案（CSDN发布版）

# 🌐 数字人民币全球化系统｜完整技术方案

> **作者**：UID9622 龙魂数字身份系统
> 

> **时间**：2025年12月
> 

> **DNA追溯码**：#CNSH-e-CNY-GLOBAL-SYSTEM-V1.0
> 

---

## 📖 系统概述

**CNSH数字人民币全球化系统**是一个基于易经推演、数学建模和区块链技术的跨境支付解决方案。

### 核心特点

- 🇨🇳 **主权货币优先** - 数字人民币(e-CNY)作为唯一结算货币
- ⚖️ **三色审计机制** - 红黄绿分级监管，全程透明
- 🔮 **易经战略推演** - 基于64卦的路径规划
- 🧮 **数学模型驱动** - 量化增长预测与风险控制
- 🌍 **一带一路优先** - 循序渐进的全球化策略

### 技术栈

| 层级 | 技术选型 | 说明 |
| --- | --- | --- |
| 前端 | React 18 + TypeScript | 用户界面 |
| 后端 | Python 3.11 + FastAPI | API服务 |
| 区块链 | Hyperledger Fabric 2.5 | 跨境清算网络 |
| 数据库 | PostgreSQL 15 + Redis 7 | 数据存储与缓存 |
| 部署 | Docker + Kubernetes | 容器化部署 |
| 监控 | Prometheus + Grafana | 系统监控 |

---

## 🚀 快速开始

### 环境要求

**必需软件：**

- Python 3.11+
- Node.js 18+
- Docker 24+
- PostgreSQL 15+
- Redis 7+

**推荐配置：**

- CPU: 8核或以上
- 内存: 16GB或以上
- 磁盘: 100GB SSD
- 系统: Ubuntu 22.04 / macOS 13+ / Windows 11 WSL2

---

### 第一步：环境安装

### 1. 安装Python环境

**Ubuntu/Debian:**

```bash
# 安装Python 3.11
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# 验证安装
python3.11 --version
```

**macOS:**

```bash
# 使用Homebrew安装
brew install python@3.11

# 验证安装
python3.11 --version
```

**Windows:**

```powershell
# 下载并安装Python 3.11
# 官网：[https://www.python.org/downloads/](https://www.python.org/downloads/)

# 验证安装
python --version
```

### 2. 安装Node.js

**Ubuntu/Debian:**

```bash
# 使用NodeSource安装
curl -fsSL [https://deb.nodesource.com/setup_18.x](https://deb.nodesource.com/setup_18.x) | sudo -E bash -
sudo apt-get install -y nodejs

# 验证安装
node --version
npm --version
```

**macOS:**

```bash
brew install node@18
node --version
```

**Windows:**

```powershell
# 下载并安装Node.js LTS
# 官网：[https://nodejs.org/](https://nodejs.org/)
```

### 3. 安装Docker

**Ubuntu:**

```bash
# 安装Docker
curl -fsSL [https://get.docker.com](https://get.docker.com) -o [get-docker.sh](http://get-docker.sh)
sudo sh [get-docker.sh](http://get-docker.sh)

# 启动Docker服务
sudo systemctl start docker
sudo systemctl enable docker

# 验证安装
docker --version
```

**macOS:**

```bash
# 下载Docker Desktop for Mac
# 官网：[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
```

**Windows:**

```powershell
# 下载Docker Desktop for Windows
# 官网：[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
```

### 4. 安装数据库

**使用Docker快速启动（推荐）：**

```bash
# 创建Docker网络
docker network create ecny-network

# 启动PostgreSQL
docker run -d \
  --name ecny-postgres \
  --network ecny-network \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=ecny_db \
  -p 5432:5432 \
  postgres:15

# 启动Redis
docker run -d \
  --name ecny-redis \
  --network ecny-network \
  -p 6379:6379 \
  redis:7

# 验证运行状态
docker ps
```

---

### 第二步：克隆项目并安装依赖

```bash
# 创建项目目录
mkdir ecny-global-system
cd ecny-global-system

# 创建Python虚拟环境
python3.11 -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 创建requirements.txt
cat > requirements.txt << EOF
# Web框架
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0

# 数据库
psycopg2-binary==2.9.9
redis==5.0.1
sqlalchemy==2.0.23
alembic==1.12.1

# 区块链
fabric-sdk-py==0.9.0
web3==6.11.3

# 密码学
cryptography==41.0.7
pycryptodome==3.19.0

# 数据处理
numpy==1.26.2
pandas==2.1.3
scipy==1.11.4

# 工具
python-dotenv==1.0.0
requests==2.31.0
pyyaml==6.0.1
EOF

# 安装Python依赖
pip install -r requirements.txt

# 创建package.json（前端）
cat > package.json << EOF
{
  "name": "ecny-global-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.2",
    "web3": "^4.3.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.2",
    "vite": "^5.0.4"
  }
}
EOF

# 安装Node.js依赖
npm install
```

---

### 第三步：项目结构

```bash
ecny-global-system/
├── backend/                 # Python后端
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   └── [main.py](http://main.py)         # 入口文件
│   ├── tests/              # 测试文件
│   └── requirements.txt
│
├── frontend/               # React前端
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── utils/
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── blockchain/             # 区块链配置
│   ├── chaincode/         # 智能合约
│   └── network/           # 网络配置
│
├── docker/                 # Docker配置
│   ├── docker-compose.yml
│   └── Dockerfile
│
├── docs/                   # 文档
└── [README.md](http://README.md)
```

---

## 💻 核心代码实现

### 1. 易经推演引擎

**文件：`backend/app/services/yijing_[engine.py](http://engine.py)`**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
易经推演引擎
基于64卦的数字人民币出海路径规划
DNA追溯码：#CNSH-YIJING-ENGINE-V1.0
"""

import random
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class YiJingEngine:
    """易经64卦推演引擎"""
    
    def __init__(self):
        # 八卦基础
        self.bagua = {
            "乾": {"symbol": "☰", "element": "天", "attribute": "主权货币"},
            "坤": {"symbol": "☷", "element": "地", "attribute": "服务实体"},
            "震": {"symbol": "☳", "element": "雷", "attribute": "技术突破"},
            "巽": {"symbol": "☴", "element": "风", "attribute": "渗透策略"},
            "坎": {"symbol": "☵", "element": "水", "attribute": "风险防控"},
            "离": {"symbol": "☲", "element": "火", "attribute": "生态繁荣"},
            "艮": {"symbol": "☶", "element": "山", "attribute": "基础设施"},
            "兑": {"symbol": "☱", "element": "泽", "attribute": "用户体验"}
        }
        
        # 关键卦象及其含义
        self.key_hexagrams = {
            "泰卦": {"code": "䷊", "phase": "国内基础", "readiness": 0.95},
            "渐卦": {"code": "䷴", "phase": "循序渐进", "strategy": "分阶段出海"},
            "既济卦": {"code": "䷾", "phase": "完美闭环", "completion": True},
            "未济卦": {"code": "䷿", "phase": "持续改进", "warning": "防止骄傲"}
        }
    
    def calculate_deployment_phase(self, year: int) -> Dict:
        """
        根据年份计算部署阶段
        
        Args:
            year: 目标年份
        
        Returns:
            包含卦象、阶段描述等信息的字典
        """
        base_year = 2025
        elapsed = year - base_year
        
        if elapsed < 0:
            return {"error": "年份不能早于2025年"}
        elif elapsed <= 2:
            return {
                "year": year,
                "hexagram": "泰卦 ䷊",
                "phase": "国内完善 + 友好国家试点",
                "countries": ["巴基斯坦", "老挝", "柬埔寨", "泰国"],
                "action": "签署MOU + 建立试点",
                "dna_code": "#CNSH-TAI-PILOT"
            }
        elif elapsed <= 5:
            return {
                "year": year,
                "hexagram": "渐卦 ䷴",
                "phase": "一带一路扩张",
                "countries": ["哈萨克斯坦", "印尼", "马来西亚", "阿联酋"],
                "action": "建立mBridge节点 + 大宗贸易结算",
                "dna_code": "#CNSH-JIAN-EXPAND"
            }
        elif elapsed <= 10:
            return {
                "year": year,
                "hexagram": "既济卦 ䷾",
                "phase": "发达市场突破",
                "countries": ["新加坡", "瑞士", "德国", "英国"],
                "action": "金融互通 + 储备货币",
                "dna_code": "#CNSH-JIJI-BREAKTHROUGH"
            }
        else:
            return {
                "year": year,
                "hexagram": "未济卦 ䷿",
                "phase": "全球化守成",
                "countries": "全球",
                "action": "技术开源 + 国际标准制定",
                "warning": "亢龙有悔，持续改进",
                "dna_code": "#CNSH-WEIJI-MAINTAIN"
            }
    
    def get_eight_trigram_strategy(self) -> Dict:
        """
        获取八卦战略布局
        
        Returns:
            完整的八卦战略映射
        """
        return {
            "乾☰ 主权层": "央行背书 + 外汇储备支撑",
            "坤☷ 应用层": "跨境电商 + 旅游支付 + 大宗贸易",
            "震☳ 技术层": "mBridge + 区块链 + 智能合约",
            "巽☴ 战略层": "一带一路优先 + 双边协议",
            "坎☵ 风控层": "KYC/AML + 实时监控 + 三色审计",
            "离☲ 生态层": "商户激励 + 开发者社区 + 用户补贴",
            "艮☶ 基建层": "数字钱包 + 清算网络 + API开放",
            "兑☱ 体验层": "多语言支持 + 低手续费 + 秒级到账"
        }
    
    def divine_strategy(self, question: str) -> Dict:
        """
        易经占卜 - 针对具体问题给出策略建议
        
        Args:
            question: 需要推演的问题
        
        Returns:
            包含卦象和建议的字典
        """
        # 简化版：随机抽取一个主卦
        hexagrams = list(self.key_hexagrams.keys())
        selected = random.choice(hexagrams)
        info = self.key_hexagrams[selected]
        
        return {
            "question": question,
            "hexagram": f"{selected} {info['code']}",
            "interpretation": info.get("phase", "未知阶段"),
            "advice": self._generate_advice(selected),
            "timestamp": [datetime.now](http://datetime.now)().isoformat(),
            "dna_code": "#CNSH-DIVINE-STRATEGY"
        }
    
    def _generate_advice(self, hexagram: str) -> str:
        """根据卦象生成建议"""
        advice_map = {
            "泰卦": "当前基础扎实，可稳步推进试点项目",
            "渐卦": "循序渐进，不可冒进，先易后难",
            "既济卦": "系统已成熟，需防止骄傲自满",
            "未济卦": "持续改进，谦虚谨慎，与时俱进"
        }
        return advice_map.get(hexagram, "顺势而为，审时度势")

# 使用示例
if __name__ == "__main__":
    engine = YiJingEngine()
    
    # 推演2030年的部署情况
    result_2030 = engine.calculate_deployment_phase(2030)
    print("\n=== 2030年部署推演 ===")
    print(f"卦象：{result_2030['hexagram']}")
    print(f"阶段：{result_2030['phase']}")
    print(f"目标国家：{result_2030['countries']}")
    print(f"DNA追溯：{result_2030['dna_code']}")
    
    # 获取八卦战略
    strategy = engine.get_eight_trigram_strategy()
    print("\n=== 八卦战略布局 ===")
    for key, value in strategy.items():
        print(f"{key}: {value}")
    
    # 占卜决策
    divine_result = engine.divine_strategy("2027年是否应该进入欧盟市场？")
    print("\n=== 易经占卜 ===")
    print(f"问题：{divine_result['question']}")
    print(f"卦象：{divine_result['hexagram']}")
    print(f"建议：{divine_result['advice']}")
```

---

### 2. 数学增长模型

**文件：`backend/app/services/growth_[model.py](http://model.py)`**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数字人民币出海增长模型
基于五行相生相克的量化预测
DNA追溯码：#CNSH-GROWTH-MODEL-V1.0
"""

import numpy as np
import pandas as pd
from typing import List, Dict
from datetime import datetime, timedelta

class eCNY_GrowthModel:
    """数字人民币增长预测模型"""
    
    def __init__(self):
        # 五行权重配置
        self.wuxing_weights = {
            "木": 0.20,  # 用户增长（数据采集）
            "火": 0.25,  # 场景覆盖（技术扩张）
            "土": 0.15,  # 基建稳定（钱包部署）
            "金": 0.25,  # 资金流动（交易收敛）
            "水": 0.15   # 系统优化（反馈循环）
        }
        
        # 初始采用率
        self.base_rate = 0.05  # 5%
        
        # 相生相克矩阵
        self.shengke_matrix = np.array([
            [1.0, 0.9, 0.0, 0.0, 0.8],   # 木生火、水生木
            [0.9, 1.0, 0.85, 0.0, 0.0],  # 火生土
            [0.0, 0.85, 1.0, 0.9, 0.0],  # 土生金
            [0.0, 0.0, 0.9, 1.0, 0.88],  # 金生水
            [0.8, 0.0, 0.0, 0.88, 1.0]   # 水生木（循环）
        ])
    
    def predict_adoption(self, years: int = 10) -> pd.DataFrame:
        """
        预测未来N年的采用率
        
        Args:
            years: 预测年数
        
        Returns:
            包含年份、采用率、卦象的DataFrame
        """
        results = []
        base_year = 2025
        
        for t in range(years):
            year = base_year + t
            
            # 五行相生增长
            mu_growth = self.wuxing_weights["木"] * np.exp(t * 0.1)
            huo_growth = self.wuxing_weights["火"] * (1 + t * 0.15)
            tu_growth = self.wuxing_weights["土"] * np.log(t + 2)
            jin_growth = self.wuxing_weights["金"] * np.sqrt(t + 1)
            shui_growth = self.wuxing_weights["水"] * (t * 0.05)
            
            growth_factor = mu_growth + huo_growth + tu_growth + jin_growth + shui_growth
            
            # Sigmoid约束（避免过热）
            constraint = 1 / (1 + np.exp(-(t - 5)))
            
            # 最终采用率
            adoption = self.base_rate * growth_factor * constraint
            adoption = min(adoption, 0.60)  # 上限60%
            
            # 对应卦象
            gua = self._year_to_gua(year)
            
            results.append({
                "year": year,
                "adoption_rate": round(adoption, 4),
                "percentage": f"{round(adoption * 100, 2)}%",
                "hexagram": gua,
                "phase": self._get_phase(t)
            })
        
        return pd.DataFrame(results)
    
    def _year_to_gua(self, year: int) -> str:
        """年份转卦象"""
        gua_sequence = [
            "泰䷊", "渐䷴", "晋䷢", "丰䷶", "既济䷾",
            "同人䷌", "大有䷍", "革䷰", "鼎䷱", "恒䷟"
        ]
        index = (year - 2025) % len(gua_sequence)
        return gua_sequence[index]
    
    def _get_phase(self, t: int) -> str:
        """获取发展阶段"""
        if t <= 2:
            return "试点期"
        elif t <= 5:
            return "扩张期"
        elif t <= 8:
            return "突破期"
        else:
            return "守成期"
    
    def calculate_loop_efficiency(self) -> np.ndarray:
        """
        计算闭环效率矩阵
        
        Returns:
            5x5的相生相克效率矩阵
        """
        return self.shengke_matrix
    
    def monte_carlo_simulation(self, iterations: int = 10000) -> Dict:
        """
        蒙特卡洛模拟 - 评估不同场景的概率分布
        
        Args:
            iterations: 模拟次数
        
        Returns:
            各场景的概率分布
        """
        scenarios = {
            "国家间合作": 0,
            "技术突破": 0,
            "政策阻力": 0,
            "市场接受": 0,
            "竞争压力": 0
        }
        
        for _ in range(iterations):
            # 随机生成场景权重
            weights = np.random.dirichlet(np.ones(5))
            max_idx = np.argmax(weights)
            scenario_keys = list(scenarios.keys())
            scenarios[scenario_keys[max_idx]] += 1
        
        # 转换为百分比
        total = sum(scenarios.values())
        return {
            k: f"{round(v / total * 100, 2)}%"
            for k, v in scenarios.items()
        }

# 使用示例
if __name__ == "__main__":
    model = eCNY_GrowthModel()
    
    # 预测10年采用率
    df = model.predict_adoption(10)
    print("\n=== 数字人民币全球采用率预测 ===")
    print([df.to](http://df.to)_string(index=False))
    
    # 闭环效率矩阵
    efficiency = model.calculate_loop_efficiency()
    print("\n=== 五行相生相克效率矩阵 ===")
    print("行列顺序：木 火 土 金 水")
    print(efficiency)
    
    # 蒙特卡洛模拟
    mc_result = model.monte_carlo_simulation(10000)
    print("\n=== 蒙特卡洛场景模拟（10000次）===")
    for scenario, prob in mc_result.items():
        print(f"{scenario}: {prob}")
```

---

### 3. FastAPI后端服务

**文件：`backend/app/[main.py](http://main.py)`**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eCNY全球化系统 - FastAPI主服务
DNA追溯码：#CNSH-FASTAPI-MAIN-V1.0
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
import os

# 添加services路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.yijing_engine import YiJingEngine
from services.growth_model import eCNY_GrowthModel

# 初始化FastAPI
app = FastAPI(
    title="eCNY全球化系统API",
    description="数字人民币全球化推演与预测系统",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化引擎
yijing_engine = YiJingEngine()
growth_model = eCNY_GrowthModel()

# 请求模型
class YearQuery(BaseModel):
    year: int

class DivinationQuery(BaseModel):
    question: str

class GrowthQuery(BaseModel):
    years: int = 10

# ==================== API路由 ====================

@app.get("/")
def read_root():
    """根路径"""
    return {
        "system": "eCNY全球化系统",
        "version": "1.0.0",
        "dna_code": "#CNSH-e-CNY-GLOBAL-API",
        "status": "running"
    }

@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "healthy"}

@[app.post](http://app.post)("/api/yijing/deployment")
def get_deployment_phase(query: YearQuery):
    """
    获取指定年份的部署阶段
    """
    try:
        result = yijing_engine.calculate_deployment_phase(query.year)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/yijing/strategy")
def get_bagua_strategy():
    """
    获取八卦战略布局
    """
    try:
        result = yijing_engine.get_eight_trigram_strategy()
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@[app.post](http://app.post)("/api/yijing/divine")
def divine_strategy(query: DivinationQuery):
    """
    易经占卜决策
    """
    try:
        result = yijing_engine.divine_strategy(query.question)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@[app.post](http://app.post)("/api/growth/predict")
def predict_growth(query: GrowthQuery):
    """
    预测未来N年的采用率
    """
    try:
        df = growth_model.predict_adoption(query.years)
        result = [df.to](http://df.to)_dict(orient='records')
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/growth/efficiency")
def get_efficiency_matrix():
    """
    获取五行闭环效率矩阵
    """
    try:
        matrix = growth_model.calculate_loop_efficiency()
        return {
            "success": True,
            "data": {
                "elements": ["木", "火", "土", "金", "水"],
                "matrix": matrix.tolist()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/growth/montecarlo")
def run_monte_carlo(iterations: int = 10000):
    """
    运行蒙特卡洛模拟
    """
    try:
        result = growth_model.monte_carlo_simulation(iterations)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 运行服务
if __name__ == "__main__":
    import uvicorn
    [uvicorn.run](http://uvicorn.run)(app, host="0.0.0.0", port=8000)
```

---

### 4. Docker部署配置

**文件：`docker-compose.yml`**

```yaml
version: '3.8'

services:
  # PostgreSQL数据库
  postgres:
    image: postgres:15
    container_name: ecny-postgres
    environment:
      POSTGRES_USER: ecny_user
      POSTGRES_PASSWORD: your_password_here
      POSTGRES_DB: ecny_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - ecny-network

  # Redis缓存
  redis:
    image: redis:7
    container_name: ecny-redis
    ports:
      - "6379:6379"
    networks:
      - ecny-network

  # FastAPI后端
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: ecny-backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://ecny_user:your_password_here@postgres:5432/ecny_db
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis
    networks:
      - ecny-network
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # React前端
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: ecny-frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    networks:
      - ecny-network

volumes:
  postgres_data:

networks:
  ecny-network:
    driver: bridge
```

**文件：`backend/Dockerfile`**

```docker
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🚀 运行系统

### 方式一：本地开发运行

```bash
# 1. 启动后端
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python app/[main.py](http://main.py)

# 后端将运行在 [http://localhost:8000](http://localhost:8000)
# API文档：[http://localhost:8000/docs](http://localhost:8000/docs)
```

### 方式二：Docker运行（推荐）

```bash
# 1. 构建并启动所有服务
docker-compose up -d

# 2. 查看运行状态
docker-compose ps

# 3. 查看日志
docker-compose logs -f backend

# 4. 停止服务
docker-compose down
```

---

## 🧪 测试API

### 使用curl测试

```bash
# 1. 健康检查
curl [http://localhost:8000/health](http://localhost:8000/health)

# 2. 获取2030年部署计划
curl -X POST [http://localhost:8000/api/yijing/deployment](http://localhost:8000/api/yijing/deployment) \
  -H "Content-Type: application/json" \
  -d '{"year": 2030}'

# 3. 获取八卦战略
curl [http://localhost:8000/api/yijing/strategy](http://localhost:8000/api/yijing/strategy)

# 4. 易经占卜
curl -X POST [http://localhost:8000/api/yijing/divine](http://localhost:8000/api/yijing/divine) \
  -H "Content-Type: application/json" \
  -d '{"question": "2027年是否应该进入欧盟市场？"}'

# 5. 预测10年增长
curl -X POST [http://localhost:8000/api/growth/predict](http://localhost:8000/api/growth/predict) \
  -H "Content-Type: application/json" \
  -d '{"years": 10}'

# 6. 蒙特卡洛模拟
curl [http://localhost:8000/api/growth/montecarlo?iterations=10000](http://localhost:8000/api/growth/montecarlo?iterations=10000)
```

### 使用Python测试

```python
import requests
import json

BASE_URL = "[http://localhost:8000](http://localhost:8000)"

# 测试2030年部署
response = [requests.post](http://requests.post)(
    f"{BASE_URL}/api/yijing/deployment",
    json={"year": 2030}
)
print("2030年部署计划：")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# 测试增长预测
response = [requests.post](http://requests.post)(
    f"{BASE_URL}/api/growth/predict",
    json={"years": 10}
)
print("\n10年增长预测：")
for item in response.json()["data"]:
    print(f"{item['year']}: {item['percentage']} - {item['hexagram']}")
```

---

## 📊 系统架构图

```
┌─────────────────────────────────────────────────────────┐
│                     用户层                                │
│  Web界面 │ 移动App │ 第三方系统 │ 开发者工具               │
└─────────────────────────────────────────────────────────┘
                          ↓ HTTP/HTTPS
┌─────────────────────────────────────────────────────────┐
│                   API网关层                               │
│    FastAPI │ 认证鉴权 │ 限流控制 │ 日志记录                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   业务逻辑层                              │
│  易经引擎 │ 增长模型 │ 三色审计 │ 风险控制                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   数据存储层                              │
│  PostgreSQL │ Redis │ 区块链 │ 对象存储                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   基础设施层                              │
│  Docker │ Kubernetes │ 监控告警 │ 日志分析                │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 安全配置

### 1. 环境变量配置

**创建`.env`文件：**

```bash
# 数据库配置
DATABASE_URL=postgresql://ecny_user:[your_password@localhost:5432](mailto:your_password@localhost:5432)/ecny_db
REDIS_URL=redis://[localhost:6379](http://localhost:6379)

# JWT密钥（生产环境必须修改）
SECRET_KEY=<POTENTIAL_SECRET_PLACEHOLDER>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS配置
ALLOWED_ORIGINS=[http://localhost:3000,http://localhost:8000](http://localhost:3000,http://localhost:8000)

# 日志级别
LOG_LEVEL=INFO
```

### 2. 生成安全密钥

```python
# 生成SECRET_KEY
import secrets
print(secrets.token_urlsafe(32))
```

---

## 📈 监控与日志

### 添加日志配置

**文件：`backend/app/core/[logging.py](http://logging.py)`**

```python
import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=[logging.INFO](http://logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('ecny_system.log')
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()
```

---

## 🐛 常见问题

### Q1：pip安装依赖失败

**A：**尝试使用国内镜像源

```bash
pip install -r requirements.txt -i [https://pypi.tuna.tsinghua.edu.cn/simple](https://pypi.tuna.tsinghua.edu.cn/simple)
```

### Q2：Docker容器无法连接PostgreSQL

**A：**检查网络配置

```bash
# 查看Docker网络
docker network ls

# 检查容器是否在同一网络
docker network inspect ecny-network
```

### Q3：端口被占用

**A：**修改docker-compose.yml中的端口映射

```yaml
ports:
  - "8001:8000"  # 将8000改为8001
```

### Q4：权限不足

**A：**给脚本添加执行权限

```bash
chmod +x backend/app/[main.py](http://main.py)
```

---

## 📚 参考资料

- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [Docker官方文档](https://docs.docker.com/)
- [PostgreSQL文档](https://www.postgresql.org/docs/)
- [易经基础](https://zh.wikipedia.org/wiki/易经)

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

**开发流程：**

1. Fork本项目
2. 创建feature分支：`git checkout -b feature/your-feature`
3. **配置Git签名（必需）**：

**步骤A：安装GPG工具**

```bash
# Ubuntu/Debian
sudo apt install gnupg

# macOS
brew install gnupg

# Windows
# 下载并安装 Gpg4win：[https://www.gpg4win.org/](https://www.gpg4win.org/)
```

**步骤B：生成GPG密钥**

```bash
# 1. 生成新密钥
gpg --full-generate-key

# 按提示选择：
# - 密钥类型：选 (1) RSA and RSA
# - 密钥长度：输入 4096
# - 有效期：选 0（永不过期）
# - 确认：输入 y
# - 真实姓名：输入 "💎 Lucky｜UID9622"
# - 电子邮件：输入 "[uid9622@petalmail.com](mailto:uid9622@petalmail.com)"
# - 注释：可以留空或输入 "CNSH龙魂数字身份"
# - 密码：设置一个强密码（至少12位）
```

**步骤C：查看并记录密钥信息**

```bash
# 2. 查看生成的密钥
gpg --list-secret-keys --keyid-format=long

# 输出示例：
# sec   rsa4096/ABCD1234EFGH5678 2025-12-17 [SC]
#       <POTENTIAL_SECRET_PLACEHOLDER>  ← 这是完整指纹
# uid                 [ultimate] 💎 Lucky｜UID9622 <[uid9622@petalmail.com](mailto:uid9622@petalmail.com)>
# ssb   rsa4096/1234567890ABCDEF 2025-12-17 [E]

# 记住两个重要信息：
# 1. 密钥ID：ABCD1234EFGH5678（sec后面的部分）
# 2. 完整指纹：<POTENTIAL_SECRET_PLACEHOLDER>（40位）
```

**步骤D：配置Git使用GPG**

```bash
# 3. 配置用户信息
git config [user.name](http://user.name) "💎 Lucky｜UID9622"
git config [user.email](http://user.email) "[uid9622@petalmail.com](mailto:uid9622@petalmail.com)"

# 4. 配置GPG签名（替换YOUR_KEY_ID为你的密钥ID）
git config user.signingkey ABCD1234EFGH5678
git config commit.gpgsign true

# 5. 配置GPG程序路径（如果需要）
# macOS:
git config gpg.program /usr/local/bin/gpg
# Linux:
git config gpg.program /usr/bin/gpg
```

**步骤E：导出公钥（用于GitHub/Gitee）**

```bash
# 6. 导出公钥
gpg --armor --export [uid9622@petalmail.com](mailto:uid9622@petalmail.com)

# 会输出类似这样的内容（复制全部）：
# -----BEGIN PGP PUBLIC KEY BLOCK-----
# 
# mQINBGb...
# ...
# -----END PGP PUBLIC KEY BLOCK-----

# 7. 将上面的公钥添加到：
# - GitHub: Settings → SSH and GPG keys → New GPG key
# - Gitee: 设置 → SSH公钥 → GPG公钥管理
```

**步骤F：测试签名**

```bash
# 8. 测试提交（会自动签名）
git commit -S -m "test: 测试GPG签名"

# 9. 验证签名
git log --show-signature

# 应该看到：
# gpg: Signature made ...
# gpg: Good signature from "💎 Lucky｜UID9622 <[uid9622@petalmail.com](mailto:uid9622@petalmail.com)>"
```

---

**⚠️ 常见问题解决**

**Q1: 提示"gpg: signing failed: Inappropriate ioctl for device"**

```bash
# 解决方法：
export GPG_TTY=$(tty)
echo 'export GPG_TTY=$(tty)' >> ~/.bashrc
```

**Q2: 提示"error: gpg failed to sign the data"**

```bash
# 检查GPG是否正常：
echo "test" | gpg --clearsign
# 如果要求输入密码，说明GPG正常工作
```

**Q3: 如何查看我的公钥指纹？**

```bash
# 查看完整指纹：
gpg --fingerprint [uid9622@petalmail.com](mailto:uid9622@petalmail.com)

# 输出示例：
# pub   rsa4096 2025-12-17 [SC]
#       1234 5678 90AB CDEF 1234 5678 90AB CDEF 1234 5678  ← 这就是指纹
# uid           [ultimate] 💎 Lucky｜UID9622 <[uid9622@petalmail.com](mailto:uid9622@petalmail.com)>
```

---

**📋 快速配置脚本（复制粘贴运行）**

```bash
#!/bin/bash
# GPG快速配置脚本

echo "🔐 开始配置GPG签名..."

# 配置Git用户信息
git config 
```

1. 提交代码（自动签名）：`git commit -S -am 'Add some feature'`
2. 推送分支：`git push origin feature/your-feature`
3. 提交Pull Request

**⚠️ 未签名的提交将被拒绝！**

---

## 📄 开源协议

**MIT License**

Copyright (c) 2025 UID9622 龙魂数字身份系统

---

## 📞 联系方式

- **作者**：💎 Lucky｜UID9622
- **邮箱**：[fireroot.lad@outlook.com](mailto:fireroot.lad@outlook.com)
- **DNA追溯码**：#CNSH-e-CNY-GLOBAL-SYSTEM-V1.0

---

**如果这个项目对你有帮助，请给个⭐Star支持一下！**

**DNA确认码**：`#ZHUGEXIN⚡️2025-🐉数字人民币全球化系统-完整技术方案-V1.0`

---

## 🔏 代码签名验证

**本项目所有提交必须使用GPG签名！**

### 验证提交签名

```bash
# 查看提交签名
git log --show-signature

# 验证最近一次提交
git verify-commit HEAD

# 查看签名详情
git show --show-signature
```

### 合法签名者

- **💎 Lucky｜UID9622** <[uid9622@petalmail.com](mailto:uid9622@petalmail.com)>
    - GPG公钥指纹：`<POTENTIAL_SECRET_PLACEHOLDER>`
    - DNA追溯码：#CNSH-UID9622-GPG-KEY

**任何未签名或签名不匹配的提交将被自动拒绝！**

###