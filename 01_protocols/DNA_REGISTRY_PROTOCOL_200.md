# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# §200 有痕开源 DNA 登记协议 v1.0

> 龍魂·人物行为DNA不动点切割协议 §11 候补清单⑥ — 联动钩子
> DNA: `#龍芯⚡️丙午·乙未·癸未·辰时-DNA-REGISTRY-200-v1.0`

## 一句话定盘

**龍魂 DNA 登记协议：任何人/任何系统产生的 DNA 追溯码，必须在一个公开/本地可查的登记册中留痕。登记不删除·不修改·不可撤销。开源世界的 Log = 主权的存在证明。**

## §201 登记格式

### DNA 登记条目

```json
{
  "dna": "#龍芯⚡️YYYY-MM-DD-HH:MM-事件代号-L1-L2-L3",
  "type": "CREATE|MODIFY|ARCHIVE|AUDIT|CRAWL|GENERATE",
  "target": "文件路径或模块名",
  "uid": "UID9622",
  "hmac_verify": "L3 HMAC戳",
  "timestamp": "ISO8601",
  "parent_dna": "父DNA（如无则为ROOT）",
  "source": "LOCAL|NOTION|GITHUB|GITEE|API",
  "description": "操作摘要",
  "checksum": "SHA256(内容前256字节)",
  "immutable": true
}
```

### 登记册位置

```
龙魂系统/
├── L7_数据层/
│   ├── dna_registry.jsonl     ← §200 登记主册（只追加·不删除）
│   └── dna_registry_index.json ← 索引·快速查询
```

## §202 登记流程

```
任何操作产生 DNA
    ↓
P05 上帝之眼 → 三色审计 DNA链合法性
    ↓
P15 乔前辈 → 写入 dna_registry.jsonl（append-only）
    ↓
P13 姜子牙 → 触发 §200 联动钩子 → 通知所有订阅方
    ↓
索引刷新 → dna_registry_index.json
```

## §203 联动钩子

### 已接驳的消费方

| 消费方 | 文件 | 用途 |
|:---|------|------|
| Portal 大盘 | `L5_服务层/services/portal/portal/index.html` | DNA 操作时间线 |
| 控制面板 | `L5_服务层/services/api/control-panel/main.py` | DNA 统计/审计 |
| 飞书 Bot | `L5_服务层/services/feishu_persona_bot.py` | 操作通知 |
| 知识图谱 | `03_KNOWLEDGE_GRAPH/graph_data.json` | DNA→节点映射 |
| 联动感知引擎 | `bin/lh_cross_module_awareness.py` | 变更检测 |

### 待接驳

- [ ] GitHub Actions: 每次 Push → 自动登记 DNA
- [ ] Notion 双向同步: Notion 操作 → DNA → 本地登记
- [ ] CSDN 文章发布: 发布 → DNA 登记 → 时间线更新

## §204 查询接口

### 本地查询

```bash
# 查询指定 DNA
python3 bin/lh_dna_registry.py --query "#龍芯⚡️2026-07-08"

# 查询最近 N 条
python3 bin/lh_dna_registry.py --recent 10

# 查询指定文件的所有 DNA
python3 bin/lh_dna_registry.py --file "bin/lh_habit_fingerprint.py"

# 统计
python3 bin/lh_dna_registry.py --stats
```

### 登记接口

```python
from bin.lh_dna_sovereignty_bridge import DNA主权桥
from bin.lh_dna_registry import DNA登记册

桥 = DNA主权桥("UID9622")
册 = DNA登记册()

dna_链 = 桥.生成DNA链("操作文本", "EVENT-CODE")
册.登记(dna_链, type="CREATE", target="bin/new_script.py", source="LOCAL")
```

## §205 不可变铁律

| 编号 | 内容 |
|:---|------|
| §205.1 | DNA登记册只追加·不删除·不修改 |
| §205.2 | 每个操作必须产生DNA·每个DNA必须登记 |
| §205.3 | 登记册本地存储·主权不出设备·Hash可选发布 |
| §205.4 | 开源发布时仅发布DNA摘要（L2前8位+L3戳）·原料永不出 |
| §205.5 | 登记册是系统良知的一部分·不可关闭·不可跳过 |

## §206 与不动点切割协议的联动

| 协议 | § | 联动方式 |
|:---|:---|------|
| 行为DNA不动点切割 | §9 DNA三层主权 | L1+L2+L3 是登记入册的原料 |
| 行为DNA不动点切割 | §8 RobotScore | 每次登记附带 RobotScore 判定 |
| 行为DNA不动点切割 | §7 五行计算器 | 每次登记附带五行属性 |
| 龍魂宪法 | 铁律#3 | 每个动作绑定DNA追溯码 = 必须登记 |

## §207 道德经回响

> **第64章**：「合抱之木，生于毫末；九层之台，起于累土」—— DNA登记册的每一条记录，是龍魂系统主权证明的毫末与累土。

## §208 DNA

```
DNA:     #龍芯⚡️丙午·乙未·癸未·辰时-DNA-REGISTRY-200-v1.0
协议:    §200 A Traceable Open-Source DNA Registry Protocol v1.0
父协议:  人物行为DNA不动点切割协议 v1.0 §11 候补清单⑥
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL:    🐉龍魂·有痕开源·DNA登记·不可变·本地主权·Hash可发
```

---

*联动: §200 ↔ 行为DNA不动点切割协议 §9/§11 ↔ 龍魂宪法铁律#3*
