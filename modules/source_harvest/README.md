# 龍魂·开源收割器 v1.0

**DNA**: `#龍芯⚡️2026-05-28-LONGHUN-AST-HARVEST-v1.0`

## 功能

从 GitHub 搜索并下载符合 MIT/Apache-2.0/BSD 协议的开源项目。

## 协议规则

**白名单**: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, Unlicense, CC0-1.0, 0BSD

**黑名单**: GPL, AGPL, LGPL, EUPL, MPL-2.0, OSL-3.0

## 使用

```bash
python3 longhun_harvest_v1.0.py --query "nlp" --lang python --max 10 --token YOUR_TOKEN
```

## 速率限制

- 无 Token: 60次/小时
- 有 Token: 5000次/小时
