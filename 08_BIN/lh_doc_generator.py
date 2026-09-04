#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 文档生成器 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-DOC-GENERATOR-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
功能: 自动生成/更新系统文档（README.md / ARCHITECTURE.md / DIRECTORY_INDEX.md）
用法: lh 文档生成 [--all] [--readme] [--architecture] [--index]
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# ── 路径 ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)


def get_git_info() -> Dict:
    """获取Git基本信息"""
    import subprocess
    info = {"branch": "unknown", "last_commit": "unknown", "commits": "?"}
    try:
        r = subprocess.run(["git", "branch", "--show-current"],
                           capture_output=True, text=True, cwd=PROJECT_ROOT)
        info["branch"] = r.stdout.strip() or "unknown"
    except Exception:
        pass
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%h %s"],
                           capture_output=True, text=True, cwd=PROJECT_ROOT)
        info["last_commit"] = r.stdout.strip() or "unknown"
    except Exception:
        pass
    try:
        r = subprocess.run(["git", "rev-list", "--count", "HEAD"],
                           capture_output=True, text=True, cwd=PROJECT_ROOT)
        info["commits"] = r.stdout.strip() or "?"
    except Exception:
        pass
    return info


def count_py_files() -> int:
    """统计bin/下Python文件数"""
    bin_dir = PROJECT_ROOT / "bin"
    return len(list(bin_dir.glob("*.py"))) if bin_dir.exists() else 0


def count_skills() -> int:
    """统计技能数"""
    skills_dir = PROJECT_ROOT / "01_技能庫"
    return len(list(skills_dir.glob("*.md"))) + len(list(skills_dir.glob("*.py"))) if skills_dir.exists() else 0


def generate_readme():
    """生成 docs/README.md"""
    git = get_git_info()
    py_count = count_py_files()
    skill_count = count_skills()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    content = f"""# 🐉 龍魂系统 · 项目总览

> DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-README-v1.0
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0
> 自动生成时间: {now}

---

## 一句话

**龍魂**是一个以中华哲学为底座、以AI自治为核心的个人系统基础设施。
覆盖：人格矩阵(20人格)·审计体系(三色+十闸)·安全(四级熔断)·部署(鲲鹏+Mac双栈)·知识中枢·搜索引擎·流场融合。

## 快速开始

```bash
# 查看系统状态
lh --status

# 启用所有服务
bash bin/start_all.sh

# 查看所有端口
lh 端口状态

# 健康巡检
lh 健康检查
```

## 系统规模

| 维度 | 数量 |
|:---|:---:|
| Python引擎 | {py_count}+ |
| 技能 | {skill_count}+ |
| 人格 | 20 (16核心+1安全+3子系统) |
| 协议文档 | 200+ |
| Mac launchd服务 | 52 |
| 鲲鹏 systemd服务 | 37 |

## 核心架构

```
L0 物理层 → Mac(本地) + 鲲鹏(119.13.90.27)
L1 守护层 → P72龍盾·P05审计·P77黑天使
L2 路由层 → P00文心·P13姜子牙·八卦路由
L3 执行层 → P04鲁班·P14吕蒙·P07管仲
L4 数据层 → SQLite·JSONL·知识中枢
L5 API层  → FastAPI多端口·流场融合
L6 网关层 → 搜索:9631·天线:8769·安全:8848
L7 展示层 → portal/·dashboard/·统一控制台:8999
```

## 关键端口

| 端口 | 服务 |
|:---:|:---|
| 8766 | 知识中枢 |
| 8769 | 天线八闸 |
| 8771 | 审计引擎 |
| 8777 | 流场融合桥接 |
| 8799 | 主权验证 |
| 8848 | 安全网关 |
| 8999 | 统一控制台 |
| 9631 | 搜索网关 |
| 11434 | Ollama推理 |

## 常用命令

```bash
lh                    # 交互控制台
lh --status           # 系统状态
lh 端口状态            # Mac端口矩阵
lh 鲲鹏状态            # 鲲鹏服务器状态
lh 引擎验证            # 全量引擎健康验证
lh 健康检查            # 巡检+告警
lh 控制台 --web        # 启动Web仪表盘
lh 流场注入 --all      # 31引擎全量注入
```

## 文档索引

- `docs/ARCHITECTURE.md` — 系统架构详解
- `docs/DIRECTORY_INDEX.md` — 完整目录导航
- `.codebuddy/COMMAND_INDEX.md` — 命令总目（毫秒级速查）
- `.codebuddy/memory/MEMORY.md` — 长期记忆
- `STATE.md` — 当前状态·唯一实时入口

## Git信息

- 分支: `{git['branch']}`
- 最新提交: `{git['last_commit']}`
- 总提交数: `{git['commits']}`

---

> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
    path = DOCS_DIR / "README.md"
    path.write_text(content)
    print(f"✅ docs/README.md 已生成")


def generate_architecture():
    """生成 docs/ARCHITECTURE.md"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    content = f"""# 🐉 龍魂系统 · 架构文档

> DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-ARCHITECTURE-v1.0
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0
> 自动生成时间: {now}

---

## 1. 总览

龍魂系统采用**九层洛书架构**，双栈部署（Mac本地 + 鲲鹏云端），以流场融合桥接实现跨栈统一调度。

## 2. 九层架构

### L0 · 物理层
- **Mac本地**: macOS (Apple Silicon), launchd守护进程管理
- **鲲鹏云端**: 华为云 TaiShan 200 (ARM64), systemd服务管理
- **SSH隧道**: 5条持久化隧道，实现双栈互联

### L1 · 守护层
- **P72龍盾**: 四级熔断（∞伦理/L1数据/L2人格/L3行为）
- **P05上帝之眼**: 三色审计·十道闸口
- **P77黑天使军团**: 红蓝对抗·安全渗透（仅自用）

### L2 · 路由层
- **P00文心**: 意图解析(10%)，自动分发到执行人格
- **P13姜子牙**: 封神榜权限分配·IPA路由
- **八卦路由**: 乾·坤·震·巽·坎·离·艮·兑 64卦路由

### L3 · 执行层
- **P04鲁班**: 技术执行·代码生成·架构搭建
- **P14吕蒙**: 部署执行·快速成长
- **P07管仲**: 资源调度·成本核算·ROI分析
- **P02宝宝**: 情感温度引擎·30%情感隔离
- **P03雯雯**: 结构归档·四签验证

### L4 · 数据层
- **知识中枢** (:8766): 统一知识检索
- **记忆服务** (:8779): 长期记忆持久化
- **审计日志**: JSONL append-only

### L5 · API层
- 多FastAPI服务端口
- **流场融合桥接** (:8777): 全引擎统一注入·翻译矩阵
- **天线八闸** (:8769): 外部信号接收
- **量子卦象API** (:9000): 64卦希尔伯特空间

### L6 · 网关层
- **搜索网关** (:9631): Bing搜索·缓存·来源审计
- **安全网关** (:8848): 请求过滤·入侵检测
- **主权验证** (:8799): 数据主权确认

### L7 · 展示层
- **portal/**: 前端门户
- **dashboard/**: 实时仪表盘
- **统一控制台** (:8999): Web监控面板

### L8 · 治理层
- 协议体系 (200+文档)
- 德本审计五问
- GPG签章·DNA追溯

### L9 · 进化层
- 自愈引擎
- 自适应微调
- 知识自举·数据造血

## 3. 技术栈

| 层 | 技术 |
|:---|:---|
| 语言 | Python 3 / CNSH / Bash |
| AI推理 | Ollama (本地) + 混元/DeepSeek (云端) |
| 前端 | 纯HTML·暗色龍魂金主题 |
| 数据库 | SQLite / JSONL |
| 安全 | GPG / AES-256 / SM2 / SHA-256 |
| 部署 | launchd (Mac) + systemd (鲲鹏) |

## 4. 数据流

```
用户意图 → P00解析 → 人格路由 → 引擎执行
    → P05审计(三色) → P15签章(GPG) → P03归档
    → 流场融合桥接(:8777) → 各引擎注入
    → 健康检查巡检 → 告警推送(Bark/飞书)
```

## 5. 安全边界

- D1(绝密)数据永不入云
- D2(机密)端侧国密加密后入云
- 本地优先·能本地不上云
- 跨境API走P77出口审查
- 四级熔断自动降级

---

> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
    path = DOCS_DIR / "ARCHITECTURE.md"
    path.write_text(content)
    print(f"✅ docs/ARCHITECTURE.md 已生成")


def generate_index():
    """生成 docs/DIRECTORY_INDEX.md"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    content = f"""# 🐉 龍魂系统 · 目录导航

> DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-DIRECTORY-INDEX-v1.0
> 自动生成: {now}

---

## 目录结构

```
longhun-system/
├── 01_protocols/      # 协议文档（200+）
│   ├── LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md  # 20人格治理白皮书
│   ├── LH-DEBEN-AUDIT-v1.0.md                     # 德本审计协议
│   ├── LH-M261-PREQUEL-COVENANT-v1.0.md           # 全权授权令
│   └── ...
├── 02_SKILLS/          # 技能定义（45+）
├── bin/                # 可执行脚本（200+）
│   ├── lh              # 统一命令入口 (Shell wrapper)
│   ├── lh.py           # Python主入口
│   ├── lh_engine_verify.py     # 业务引擎验证
│   ├── lh_alert_engine.py      # 告警引擎
│   ├── lh_unified_console.py   # 统一控制台
│   ├── lh_permission_manager.py # 权限管理
│   ├── lh_health_check.py      # 健康检查
│   └── ...
├── deploy/             # 部署脚本
│   ├── scripts/DEPLOY.md       # 鲲鹏十步法
│   ├── scripts/health_check.sh # 鲲鹏健康检查
│   └── ...
├── docs/               # 系统文档
│   ├── README.md               # 项目总览
│   ├── ARCHITECTURE.md         # 架构文档
│   └── DIRECTORY_INDEX.md      # 本文件
├── portal/             # 前端门户
├── dashboard/          # 仪表盘
├── engines/            # 引擎实现
├── apps/               # 应用
├── audit/              # 审计日志
├── papers/             # 学术论文
├── reports/            # 报告
├── web/                # Web应用
├── .codebuddy/         # CodeBuddy配置
│   ├── COMMAND_INDEX.md         # 命令总目
│   ├── memory/MEMORY.md         # 长期记忆
│   ├── longhun_neural_net.json  # 系统拓扑
│   └── rules/                   # 对齐规则
├── STATE.md            # 当前状态·唯一实时入口
├── CONSTITUTION.md     # 系统宪法
├── GOVERNANCE.md       # 治理文档
├── AGENTS.md           # AI操作手册
└── P0_ETERNAL_LOCK.md  # 永恒锁
```

## 关键入口

| 需要什么 | 去哪里 |
|:---|:---|
| 所有命令速查 | `.codebuddy/COMMAND_INDEX.md` |
| 系统实时状态 | `STATE.md` |
| 长期记忆 | `.codebuddy/memory/MEMORY.md` |
| 人格矩阵 | `01_protocols/LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md` |
| 部署指南 | `deploy/scripts/DEPLOY.md` |
| 系统拓扑 | `.codebuddy/longhun_neural_net.json` |
| AI操作铁律 | `AGENTS.md` |
| 德本审计 | `01_protocols/LH-DEBEN-AUDIT-v1.0.md` |

---

> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
    path = DOCS_DIR / "DIRECTORY_INDEX.md"
    path.write_text(content)
    print(f"✅ docs/DIRECTORY_INDEX.md 已生成")


def generate_all():
    """生成全部文档"""
    print("🐉 龍魂 · 文档生成器")
    print("=" * 50)
    generate_readme()
    generate_architecture()
    generate_index()
    print("=" * 50)
    print("✅ 全部文档已生成到 docs/ 目录")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐉 龍魂·文档生成器")
    parser.add_argument("--all", action="store_true", help="生成全部文档")
    parser.add_argument("--readme", action="store_true", help="只生成 README.md")
    parser.add_argument("--architecture", action="store_true", help="只生成 ARCHITECTURE.md")
    parser.add_argument("--index", action="store_true", help="只生成 DIRECTORY_INDEX.md")
    args = parser.parse_args()

    if args.all or (not args.readme and not args.architecture and not args.index):
        generate_all()
    else:
        if args.readme:
            generate_readme()
        if args.architecture:
            generate_architecture()
        if args.index:
            generate_index()


if __name__ == "__main__":
    main()
