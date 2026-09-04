# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · 本地法律引擎

**DNA**: `#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-LONGHUN-LEGAL-ENGINE-v1.0`

> 让老百姓用大白话查法律，本地运行，不联网。

## 文件说明

- `laws.json` — 法律条文知识库（官方条文 + 大白话解释）
- `legal_engine.py` — 核心引擎，可被其他模块本地 import
- `api_server.py` — 本地 API 服务
- `启动法律引擎.sh` — 一键启动脚本

## 本地引用

```python
import sys
sys.path.insert(0, "/Users/zuimeidedeyihan/longhun-system/法律引擎")
from legal_engine import 解释问题

result = 解释问题("被公司辞退了能拿多少赔偿", 语气="大白话")
print(result["综合回答"])
```

## 启动 API 服务

```bash
bash 启动法律引擎.sh
```

浏览器/接口访问：
```bash
curl -X POST http://127.0.0.1:9634/query \
  -H "Content-Type: application/json" \
  -d '{"question":"物业强制人脸识别合法吗","tone":"大白话"}'
```

## 覆盖领域

- 劳动权益
- 消费者权益
- 个人信息与数据主权
- 租赁与住房
- 算法与反垄断
