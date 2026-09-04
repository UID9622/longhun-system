# SPEC.md — 龍魂 DNA 生成器（lh_dna_generator.py）规格书

DNA: 待生成 · 归属: 龍魂系统 UID9622 · 诸葛鑫·龍芯北辰

## 1. 定位
龍魂系统全系统唯一 DNA 追溯码权威生成器。所有文档/代码/协议/报告的 DNA 一律以此脚本输出为准，禁止手写。

## 2. DNA 格式（现行规范 v2.0，2026-07-19 基线扩展）
```
#龍芯⚡️{年干支}·{月干支}·{日干支}·{时辰}·{卦符卦名}-{动作标签}-{版本}-{日序号}-{哈希8}
示例: #龍芯⚡️丙午·甲申·己卯·午时·䷀乾-AUDIT-REPORT-v1.0-0007-a3f9c21e
```
- 分隔符：干支四柱与卦名用 `·`，后续段用 `-`
- 旧格式（时间戳/年-月-日连字符）一律冻结不改写（P0：不删除只冻结）

## 3. 唯一性数学保证
冲突域 = 60(日柱) × 12(时辰) × 64(卦) = 46080 组合/天，仍可能撞车。
→ 叠加两道唯一锚：
1. **日序号**：registry/counter.json 持久化，按当日单调递增，0001 起，机器级不重复
2. **内容哈希8位**：SM3（国密，hashlib.new('sm3')，不可用则回退 SHA256）取前8位 hex
   哈希输入 = 标题+动作+版本+时间戳ISO+序号 → 同一输入永不复用
唯一性命题：同一天内序号唯一 ⟹ DNA 全局唯一。跨天日柱不同 ⟹ 天然不同。

## 4. 干支算法（修正上传稿错误）
- 年柱：(year-4)%10 / (year-4)%12（立春近似=公历年，注明）
- 月柱：五虎遁（甲己之年丙作首…），按公历月近似（节气精确版留升级口）
- 日柱：JDN 公式 idx = (JDN + 49) % 60，锚点 2000-01-01 = 戊午(54) ✅
  （上传稿以 1900-01-01 为庚子日，错误；实际为甲戌日，本版修正）
- 时辰：(hour+1)//2 % 12 → 子丑寅卯…

## 5. 卦名映射
hash 首字节 % 64 → 通行本(王弼序)64卦，符号 U+4DC0+i（䷀乾…䷿未济），确定性可复现。

## 6. 注册表（统一归类/拓展/压缩/恢复）
- registry/dna_registry.json：DNA → {title, action, version, category, file_path, sha256, created_iso, confirm_code}
- category 分类法（可拓展）：protocol/script/doc/paper/asset/log/intel/other
- recover 命令：DNA → 打印元数据 + 若 file_path 存在则输出全文
- compress 命令：registry 快照 gzip 归档至 registry/archive/
- 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬{随机8位}（生成时一并给出）

## 7. CLI 接口
```
python3 bin/lh_dna_generator.py generate --title T --action ACT --version v1.0 [--category c] [--file path] [--date YYYY-MM-DD]
python3 bin/lh_dna_generator.py verify --dna "..."
python3 bin/lh_dna_generator.py recover --dna "..."
python3 bin/lh_dna_generator.py register --dna "..." --file path --title T
python3 bin/lh_dna_generator.py list [--category c]
python3 bin/lh_dna_generator.py compress
python3 bin/lh_dna_generator.py ganzhi [--date YYYY-MM-DD]   # 仅查干支
```
默认日期=今天；registry 默认定位脚本上级目录 registry/，可用 --registry 覆盖。

## 8. 测试
- 干支锚点：2000-01-01=戊午、2026-08-03 输出稳定性
- 批量生成 1000 条：0 重复
- verify/recover/compress 闭环
