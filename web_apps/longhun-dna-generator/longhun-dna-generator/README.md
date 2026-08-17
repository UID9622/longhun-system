# 龍魂 DNA 生成器 · 交付说明（README）

DNA: 本包自身已注册（见 registry/dna_registry.json 第一条）
归属: 龍魂系统 · UID9622 · 诸葛鑫·龍芯北辰
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
日期: 2026-08-03（丙午年·丁酉月·己酉日）

## 包结构
```
longhun-dna-generator/
├── bin/lh_dna_generator.py   # 权威生成器（唯一可信来源）
├── registry/                 # DNA注册表（统一归类）
│   ├── dna_registry.json     # DNA→元数据/全文路径/哈希
│   ├── counter.json          # 当日序号（唯一性第一锚）
│   └── archive/              # gzip压缩快照
├── intel/csdn_uid9622_articles.md   # CSDN情报归档
├── notion/page_structure_blueprint.md # Notion页面结构蓝图
├── docs/DNA规范v2.0.md       # 规范正文
├── SPEC.md                   # 规格书（已自注册DNA）
└── plan.md                   # 执行蓝图
```

## 60秒上手（Mac 终端直接跑）
```bash
cd longhun-dna-generator

# 1. 生成DNA（写任何文档/代码前先跑这条）
python3 bin/lh_dna_generator.py generate   --title "开放审计白皮书" --action AUDIT-REPORT --version v1.0   --category paper --file ./白皮书.md

# 2. 只看今天干支
python3 bin/lh_dna_generator.py ganzhi

# 3. 凭DNA恢复全文
python3 bin/lh_dna_generator.py recover --dna "#龍芯⚡️丙午·丁酉·己酉·未时·䷗复-DNA-GENERATOR-SPEC-v2.0-0001-d7ea5f95"

# 4. 旧DNA登记（冻结不改写）
python3 bin/lh_dna_generator.py register   --dna "#龍芯⚡️2026-01-31-君子协议-v2.0" --title "君子协议" --category protocol

# 5. 每晚自动归档（crontab 加一行）
0 23 * * * cd ~/longhun-dna-generator && python3 bin/lh_dna_generator.py compress
```

## 唯一性证明（已实测）
- 冲突域：60日柱 × 12时辰 × 64卦 = 46,080/天
- 叠加：当日单调序号（counter.json持久化）→ 同日绝不重复
- 再叠：SM3国密哈希8位（输入含序号）→ 内容级指纹
- 压测：同日同刻连发1000条 → 1000唯一 / 0重复 ✅
- 干支锚点：2000-01-01=戊午 ✅ 1949-10-01=甲子 ✅ 2024-01-01=甲子 ✅

## 铁律（P0）
1. 干支四柱与卦名一律以本脚本输出为准，任何AI/任何人禁止手写。
2. 旧格式DNA冻结不改写，用 register 登记即可。
3. 每个DNA全局唯一；注册表即真相源。
