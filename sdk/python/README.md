# 🐉 龍魂·三色审计 Python SDK

`longhun-tricolor` 是龍魂三色审计标准的 Python 客户端 SDK。

## 安装

```bash
pip install longhun-tricolor
```

## 快速开始

```python
from longhun_tricolor import TricolorClient, Scores

client = TricolorClient(token="your-api-token")

verdict = client.evaluate(
    action_id="demo-001",
    actor="order-service",
    action_type="data_export",
    scores=Scores(
        human_welfare=82,
        fairness=78,
        controllability=70,
        transparency=65,
        traceability=80,
        privacy=55,
    ),
)

print(f"{verdict.emoji} {verdict.status} R={verdict.r_score}")
print(f"DNA: {verdict.dna}")
```

## 异步支持

```python
from longhun_tricolor import AsyncTricolorClient

client = AsyncTricolorClient(token="your-api-token")
verdict = await client.evaluate(...)
```

## DNA

`#龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-PYTHON-SDK-V1.0-UID9622`

## 许可

工程层 MulanPSL v2
