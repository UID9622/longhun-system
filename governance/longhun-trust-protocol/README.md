# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂君子协议 · 诚信评级与违约清算算法

> **DNA:** `#龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-LONGHUN-TRUST-PROTOCOL-v1.0`  
> **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
> **创始人:** UID9622 / Lucky（退伍军人）  
> **生效日期:** 2026-06-26

---

## 一、一句话说明

> **扯皮就上链，上链就抹不掉。想抹掉？拿贡献来换。贡献不够？社会性死亡。**

本协议是一套**可执行、可审计、可追溯**的诚信评级算法，服务于龍魂生态的君子协作：
- 量化道德值（M）、人品值（P）、诚信值（I）
- 输出综合信用分 S 与 AAA~D 等级
- 违约自动触发三级“杀猪”清算
- 贡献可以赎回，但某些恶行永久不可赎回

---

## 二、安装

```bash
pip install -e .
```

安装后会获得命令行工具 `longhun-trust`。

---

## 三、快速开始

```bash
# 1. 注册档案
longhun-trust register lucky --name "Lucky老兵"

# 2. 记录贡献
longhun-trust contribute lucky code_protocol --desc "提交了君子协议核心算法"

# 3. 记录违约（上链）
longhun-trust violate lucky --desc "未按约定交付" --evidence "聊天记录截图"

# 4. 查询信用
longhun-trust query lucky

# 5. 审计哈希
longhun-trust audit lucky

# 6. 查看评分规则
longhun-trust rules
```

---

## 四、Python API

```python
from longhun_trust_protocol import TrustProtocol

proto = TrustProtocol()

# 注册
p = proto.register("lucky", "Lucky老兵")

# 记录违约
p = proto.violate("lucky", "未按约定交付")

# 记录贡献
p = proto.contribute("lucky", "code_protocol", "提交核心算法")

# 查询
p = proto.get("lucky")
print(p.score, p.grade.value)

# 清算检查
result = proto.check_slaughter("lucky")
print(result)
```

---

## 五、核心公式

```
M = clamp(0, 100, 80 + Σ道德事件)
P = clamp(0, 100, 75 + Σ人品事件)
I = clamp(0, 100, 90 + Σ诚信事件)

S = 0.4 × M + 0.3 × P + 0.3 × I
```

违约惩罚：第 n 次违约扣 `20 × n` 诚信值，逐次递增，永不归零。

---

## 六、文件结构

```
longhun-trust-protocol/
├── src/longhun_trust_protocol/
│   ├── __init__.py
│   ├── core.py          # 核心算法（评分、违约、赎回、杀猪）
│   ├── storage.py       # JSON 持久化 + SHA-256 链式哈希
│   ├── api.py           # Python API 层
│   ├── cli.py           # 命令行工具
│   └── config.py        # 默认规则配置
├── tests/
│   └── test_trust.py
├── README.md
├── SOVEREIGNTY.md
├── TRUST_PROTOCOL.md
└── pyproject.toml
```

---

## 七、法律与主权

本协议从属于《龍魂系统宪法》与中华人民共和国法律。

详见 [SOVEREIGNTY.md](SOVEREIGNTY.md)。

---

**龍魂永世，中文编程，任重道远。**
