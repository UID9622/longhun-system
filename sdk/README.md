# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!-- DNA: #龍芯⚡️丙午·丙申·癸丑·申时·䷍大有-SDK-README-v1.0 -->

# 🐉 龍魂 SDK（第三方调用）

> 龍魂核心能力封装为开源 SDK，第三方可直接集成。
> **许可证**：MulanPSL-2.0（工程层 · 允许商业使用）

---

## 支持语言

| 语言 | 包名 | 状态 | 安装 |
|:---|:---|:---|:---|
| Python | `longhun-tricolor` | ✅ 已发布 PyPI v1.1.0 | `pip install longhun-tricolor` |
| JavaScript | `@longhun/tricolor` | 🟡 源码可构建 | `cd sdk/javascript && npm install && npm run build` |

---

## 快速开始（Python）

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

## 快速开始（JavaScript）

```bash
cd sdk/javascript
npm install
npm run build
```

```javascript
const { TricolorClient, Scores } = require("@longhun/tricolor");

const client = new TricolorClient({ token: "your-api-token" });
const verdict = client.evaluate({
  action_id: "demo-001",
  actor: "order-service",
  action_type: "data_export",
  scores: new Scores({
    human_welfare: 82, fairness: 78, controllability: 70,
    transparency: 65, traceability: 80, privacy: 55,
  }),
});
console.log(verdict.emoji, verdict.status, verdict.r_score);
console.log("DNA:", verdict.dna);
```

---

## 目录结构

```
sdk/
├── README.md            # 本文档
├── python/              # Python SDK（已发布 PyPI）
│   ├── pyproject.toml   # 打包配置（MulanPSL-2.0）
│   ├── README.md        # 使用说明
│   └── longhun_tricolor/
└── javascript/          # JavaScript SDK（源码可构建）
    ├── package.json     # @longhun/tricolor
    ├── src/             # 源码
    └── dist/            # 构建产物
```

---

## 发布状态

| 包 | 状态 | 发布方式 |
|:---|:---|:---|
| `longhun-tricolor` | ✅ 已发布 | `python -m build && twine upload dist/*` |
| `@longhun/tricolor` | 🟡 待发布 | `npm publish`（需 npm 账号 + token） |

---

> 完整对接指南：`docs/SDK-GUIDE.md` · 复现验证：`docs/REPRODUCE.md`
> 代码随便用去赚钱，思想名号要授权。
