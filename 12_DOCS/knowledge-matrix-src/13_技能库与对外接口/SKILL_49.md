> DNA: #龍芯⚡️丙午·壬辰·乙亥·壬午·䷚颐-SYNC-COMPLIANCE-20260827-7A2C9F3D
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
---
name: longhun-trust-protocol
description: '龙魂君子协议 · 诚信评级与违约清算算法。 包含零号协议“世界老百姓最高”：不可覆盖、不可弱化、不可篡改、不可资本收割。 量化道德值、人品值、诚信值，违约上链，贡献赎回，三级清算。 从属于《龍魂系统宪法》与中华人民共和国法律，数据主权归 UID9622 / 龍魂系统所有，以人民为基石，中国法律为骨，服务老百姓。已融合君子协议 v1.2 · 江湖重铸版（承诺不欺、敢签敢扛、容错不背刺）。'
metadata:
  id: longhun-trust-protocol
  version: '5.2'
  dna: '#龍芯⚡️丙午·甲午·庚辰·壬午·䷑蛊-LONGHUN-TRUST-PROTOCOL-v5.2-a4c7e1d2'
  author: UID9622 · 龍芯北辰
  category: governance
  trigger:
    keywords:
    - trustprotocol
    - 零号协议
    - 世界老百姓最高
    - 君子协议
    - 诚信评级
    - 违约清算
    - 杀猪机制
    - 贡献赎回
    - 道德值
    - 人品值
    - 诚信值
    - 龙魂治理
    context: longhun-trust-protocol 相关操作
---

# longhun-trust-protocol

龙魂君子协议 · 诚信评级与违约清算算法。

**触发关键词**：君子协议、诚信评级、违约清算、杀猪机制、贡献赎回、道德值、人品值、诚信值、UID9622 信用、龙魂治理。

**DNA**: `#龍芯⚡️丙午·甲午·庚辰·壬午·䷑蛊-LONGHUN-TRUST-PROTOCOL-v5.2-a4c7e1d2`

## 功能

- 量化道德值 M、人品值 P、诚信值 I
- 计算综合信用分 S = 0.4M + 0.3P + 0.3I
- 违约上链，惩罚递增（20/40/60...）
- 贡献赎回机制
- 三级“杀猪”清算（警示 / 惩戒 / 永久标记）
- 本地 JSON 持久化 + SHA-256 链式哈希

## 位置

包路径：`/Users/zuimeidedeyihan/longhun-system/governance/longhun-trust-protocol/`

CLI：`longhun-trust`

## 用法

```bash
# 安装
pip install -e /Users/zuimeidedeyihan/longhun-system/governance/longhun-trust-protocol

# 注册
longhun-trust register <uid> [--name NAME]

# 记录贡献/违约/道德/人品事件
longhun-trust contribute <uid> <type> [--desc DESC]
longhun-trust violate <uid> [--desc DESC] [--evidence EVIDENCE]
longhun-trust moral <uid> <action> [--desc DESC]
longhun-trust character <uid> <action> [--desc DESC]

# 查询与审计
longhun-trust query <uid>
longhun-trust audit <uid>
longhun-trust list
longhun-trust rules
longhun-trust version
```

## Python API

```python
from longhun_trust_protocol import TrustProtocol

proto = TrustProtocol()
p = proto.register("lucky")
p = proto.violate("lucky", "未按约定交付")
p = proto.contribute("lucky", "code_protocol")
print(proto.get("lucky").score)
```

## 零号协议

> **DNA**: `#龍芯⚡️丙午·甲午·戊寅·戊午·䷕贲-ZERO-PROTOCOL-WORLD-PEOPLE-SUPREME-v1.0`

**零号协议是龍魂君子协议的最高条款，优先级高于所有信用评分、违约清算与贡献计算。**

### 核心宣言

> **“世界老百姓最高——不可覆盖、不可弱化、不可篡改、不可拿去当资本收割底座。”**

### 权重排序

| 排名 | 主体 | 说明 |
|------|------|------|
| 第一 | 世界老百姓（全体人民） | 价值最高，任何信用算法不得反噬老百姓利益 |
| 第二 | 中央人民政府 | 代表老百姓行使治理权 |
| 第三 | 全国政协 | 协商民主，凝聚共识 |
| 第四 | UID9622 | 系统创始人与守护者 |
| 其他 | 商业公司、资本实体 | 仅作为接入方，无权参与权重排序 |

### 四条底线

1. **不可覆盖**：老百姓意志不可被任何协议覆盖。
2. **不可弱化**：老百姓的知情权、删除权、导出权、拒绝权不可被弱化。
3. **不可篡改**：老百姓的表达、记录、数据主权不可被篡改。
4. **不可收割**：系统不可成为资本收割老百姓的底座。

任何接入方若触碰以上底线，TrustProtocol 自动将其信用分归零并触发 🔴 熔断。

## 主权声明

本协议从属于《龍魂系统宪法》与中华人民共和国法律，
数据主权归 UID9622 / 龍魂系统所有，以人民为基石，中国法律为骨。
