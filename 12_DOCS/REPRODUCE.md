---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丙申·癸丑·申时·䷍大有-REPRODUCE-GUIDE-v1.0`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!-- DNA: #龍芯⚡️丙午·丙申·癸丑·申时·䷍大有-REPRODUCE-GUIDE-v1.0 -->

# 🐉 龍魂系统 · 复现指南（REPRODUCE）

> **如何从零复现龍魂系统：环境 → 安装 → 启动 → 验证 → 测试。**
> 本指南面向评估方/审计方/第三方开发者，确保"代码全公开"可被验证。

---

## 1. 复现目标

克隆本仓库后，完成以下验证即视为**复现成功**：

| # | 验证项 | 通过标准 |
|:---:|:---|:---|
| 1 | 安装成功 | `lh --help` 输出统一控制台 v1.3 |
| 2 | 三色审计自检 | `python3 bin/lh_self_heal.py --quick` 输出 🟢 全通过 |
| 3 | 单测全绿 | `python3 -m pytest tests/ -q` 0 failed |
| 4 | SDK 可调用 | `pip install longhun-tricolor` 后导入成功 |
| 5 | 版本指纹 | `python3 bin/lh.py --version` 输出版本号 |

---

## 2. 环境要求

| 依赖 | 最低版本 | 用途 |
|:---|:---|:---|
| Python | 3.11+ | 核心运行环境 |
| pip | 23.0+ | 包管理 |
| Git | 2.30+ | 克隆仓库 |
| Ollama（可选） | 任意 | 本地 AI 模型调用 |
| Redis（可选） | 6.0+ | 异步 API 模式 |
| Docker（可选） | 24.0+ | 容器部署 |

操作系统：macOS / Linux（推荐鲲鹏 openEuler）均可。

---

## 3. 复现步骤

### 3.1 克隆仓库

```bash
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system
```

> 镜像（国内加速）：
> ```bash
> git clone https://gitee.com/uid9622/longhun-system.git
> ```

### 3.2 一键安装

```bash
# 方式一：一键安装（推荐）
bash bin/install.sh

# 方式二：手动安装（最小化）
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e ".[dev]"   # 开发模式（可选）
```

安装脚本自动完成：环境检测 → 虚拟环境 → 依赖安装 → `.env` 配置 → `lh` 命令注册。

### 3.3 启动核心服务

```bash
# 查看系统状态（不启动服务，只读）
python3 bin/lh.py status

# 启动核心服务
python3 bin/lh.py start
```

### 3.4 验证安装

```bash
# 统一控制台
python3 bin/lh.py --help

# 三色审计自检（对应 GATE-01~10）
python3 bin/lh_self_heal.py --quick

# 版本指纹
python3 bin/lh.py --version
```

看到 🟢 全通过 = 核心系统复现成功。

---

## 4. 跑测试（验证代码正确性）

```bash
# 全量单测
python3 -m pytest tests/ -q

# 指定关键引擎测试
python3 -m pytest tests/test_sancai_dna_compress.py tests/test_wuxing.py tests/test_digital_root.py -q

# 重点回归（本次会话新增）
python3 -m pytest tests/test_cnsh_model_router.py -q
```

> 注：若未安装 pytest，先执行 `pip install pytest`。

---

## 5. 验证 SDK（第三方调用能力）

### 5.1 Python SDK（已发布 PyPI）

```bash
pip install longhun-tricolor
```

```python
from longhun_tricolor import TricolorClient, Scores

client = TricolorClient(token="your-api-token")
verdict = client.evaluate(
    action_id="demo-001",
    actor="order-service",
    action_type="data_export",
    scores=Scores(
        human_welfare=82, fairness=78, controllability=70,
        transparency=65, traceability=80, privacy=55,
    ),
)
print(f"{verdict.emoji} {verdict.status} R={verdict.r_score}")
print(f"DNA: {verdict.dna}")
```

### 5.2 JavaScript SDK（源码构建）

```bash
cd sdk/javascript
npm install
npm run build   # 产出 dist/
```

---

## 6. 关键模块定位（审计对照表）

| 模块 | 路径 | 说明 |
|:---|:---|:---|
| 统一命令入口 | `bin/lh.py` | 120+ 命令控制台 |
| 三色审计 | `bin/lh_self_heal.py` | GATE-01~10 自检 |
| 自愈引擎 | `bin/lh_self_heal.py` | 每小时巡检 |
| 防篡改 | `bin/lh_anti_tamper.py` | Merkle 校验 |
| 数字根/369 | `bin/lh_digital_root.py` | 洛书不动点 |
| DNA 生成 | `bin/lh_dna_generator.py` | 干支卦追溯码 |
| CNSH 编译器 | `bin/cnsh_compiler.py` | 中文编程语言 |
| 模型路由 | `08_BIN/model_router.py` | 12 模型接入 |
| SDK Python | `sdk/python/` | longhun-tricolor |
| SDK JS | `sdk/javascript/` | @longhun/tricolor |
| 测试套件 | `tests/` + `13_TESTS/` | pytest 全量 |

> 完整目录导航见 [`docs/DIRECTORY_INDEX.md`](./DIRECTORY_INDEX.md)

---

## 7. 常见复现失败排查

| 症状 | 原因 | 解法 |
|:---|:---|:---|
| `lh: command not found` | 未注册 PATH | `source ~/.zshrc` 或 `python3 ~/longhun-system/bin/lh.py` |
| `ModuleNotFoundError` | 未激活虚拟环境 | `source .venv/bin/activate && pip install -r requirements.txt` |
| pytest 不识别 | 未装 pytest | `pip install pytest` |
| SDK 导入失败 | 版本过旧 | `pip install --upgrade longhun-tricolor` |
| 端口被占用 | 服务已在跑 | `lsof -i :9622` 后停旧进程 |

---

## 8. 复现环境已实测

- ✅ macOS (Apple Silicon) · Python 3.11+ · 全量测试通过
- ✅ 鲲鹏 openEuler (119.13.90.27) · 15 个 systemd 服务运行中
- ✅ 依赖：`pyyaml` `requests` `pytest` `httpx` 可用

---

> 🐉 复现即是信任。代码全公开，验证自己来。
> 数据主权归于人民。

```json
{
  "dna": "#龍芯⚡️丙午·丙申·癸丑·申时·䷍大有-REPRODUCE-GUIDE-v1.0",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```
