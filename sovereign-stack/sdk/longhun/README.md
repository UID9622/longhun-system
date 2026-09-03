# 🐉 longhun · 龍魂统一 SDK

**一个账号 = 龍魂生态全部服务。** 人格工具 + 知识库 + 搜索 + API，统一调用、统一 DNA 追溯、统一三色审计、统一按量计费（CNY·个人每月 1 万次免费）。

- DNA: `#龍芯⚡️2026-08-31-LONGHUN-SDK-V1.0-UID9622`
- 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
- License: MulanPSL v2（可商业使用·需署名·勿删 DNA 追溯码）

## 安装

```bash
pip install longhun
```

零三方依赖 · Python ≥3.8 · 即装即用。

## 3 行代码快速开始

```python
import longhun
from longhun import generate_dna, audit, scan_text

dna = generate_dna("MY-APP")          # 🧬 打 DNA 追溯码
audit("my-app", "started", "🟢")      # 📝 记三色审计日志
print(scan_text("openai.com"))        # ⚖️ 15条国产替代扫描 → R01 🔴
```

## 统一 CLI

```bash
longhun version
longhun dna stamp --module MY-APP
longhun audit requirements.txt        # 15条国产替代规则扫描
longhun audit summary                 # 三色审计汇总
longhun tricolor audit pay order_001 🟢
longhun cnsh run hello.cnsh           # CNSH 运行桥
```

## 能力清单

| 模块 | 能力 | 对应 sovereign-stack |
| --- | --- | --- |
| `longhun.dna` | DNA 追溯码生成 | `dna/dna_middleware.py` |
| `longhun.tricolor` | 三色审计（sqlite·append-only） | `dna/tricolor_audit.py` |
| `longhun.evaluator` | 15条国产替代规则（人民币主权） | `evaluator/evaluator.py` |
| `longhun.cnsh` | CNSH 运行桥（本机解释器） | `08_BIN/cnsh/` |

## 发布（维护者用）

```bash
pip install build
python -m build
twine upload dist/*
```

## 关联

- 统一入口: https://github.com/UID9622/sovereign-stack
- 主权技术栈全模块: api-gateway / pricing / search-engine / dna / sbom / dependency-isolation / terraform-huawei
- 定价: 个人 1 万次免费/月 · 超出 ¥0.0001/次 · 开源项目免费
