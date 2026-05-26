# 🔐 龍魂·DNA追溯流水线 · 快速开始指南

**DNA**: #龍芯⚡️20260525|DNA-PIPELINE-QUICKSTART|v1.0|xxxxx
**UID**: 9622
**确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**生成时间**: 2026-05-25 15:47 CST (星期一)

---

## 🚀 一句话总结

四件套已全部焊死，现在一条命令就能把"发布→打水印→自动登记→扫描侵权→公开黑名单→闭环审计"串起来。

---

## 📋 四步流水线

### Step 1️⃣: 发布前 → 打水印 + 自动登记

```bash
# 你写好了一篇文章
python3 ~/longhun-system/tools/DNA追溯流水线_自动化触发器.py \
  step1 ~/article.md "我的技术文章" CSDN

# 输出：
# ✅ 内容DNA生成: #龍芯⚡️20260525|我的技术文章|v1.0|xxxxx
# ✅ 三层水印已嵌入 (显式+不动点+零宽)
# ✅ 水印后内容: article_watermarked.md
# 📋 自动登记邮件已生成
# 💡 请发送到: longhun2025@petalmail.com 标题: [DNA-REG] 我的技术文章
```

**做什么了？**
- 自动生成DNA签名
- 嵌入三层水印（任何人洗不掉零宽水印）
- 生成登记邮件（包含DNA+内容哈希+时间戳）
- 本地数据库记录

---

### Step 2️⃣: 发现剽窃 → 自动收证

```bash
# 你在网上发现疑似剽窃
python3 ~/longhun-system/tools/DNA追溯流水线_自动化触发器.py \
  step2 "https://zhuanlan.zhihu.com/p/xxx" "知乎"

# 输出：
# 🔍 执行水印扫描...
# 🚨 发现DNA水印！指向UID9622
# 🎣 执行钩子识别 (18条+11类)...
# ✅ 证据包已生成: evidence_abc123.json
#    内容: 水印检测 + 钩子识别 + URL证明
```

**做什么了？**
- 扫描疑似抄袭页面中的水印
- 识别18条+11类钩子（套路手法）
- 自动生成证据包（JSON格式）
- 数据库记录侵权信息

---

### Step 3️⃣: 追溯 → 公开黑名单

```bash
# 证据充分，把侵权者加入黑名单
python3 ~/longhun-system/tools/DNA追溯流水线_自动化触发器.py \
  step3 证据库/侵权记录/evidence_abc123.json

# 输出：
# ✅ 已添加到黑名单
# ✅ 已写入耻辱墙
# 🚨 黑名单条目:
#    URL: https://zhuanlan.zhihu.com/p/xxx
#    平台: 知乎
#    状态: 🔴 永久黑名单
```

**做什么了？**
- 检查是否已在黑名单
- 写入"耻辱墙"（公开列表）
- 更新侵权计数
- 生成维权证据

---

### Step 4️⃣: 闭环 → 审计 + 法律留痕

```bash
# 证据链完整，闭环审计
python3 ~/longhun-system/tools/DNA追溯流水线_自动化触发器.py \
  step4 证据库/侵权记录/evidence_abc123.json

# 输出：
# ✅ 审计日志已记录
# ✅ 时间戳已锁定: 2026-05-25T15:47:40
# ✅ UID9622确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 📋 证据链已闭环，保留法律追责权
```

**做什么了？**
- 审计日志入库（带时间戳）
- UID9622确认码锁定（无法否认）
- 保存完整的证据链
- 留下法律追责权

---

## 🔄 完整的使用场景

### 场景：你在CSDN发表了一篇技术文章

```bash
# ════════════════════════════════════════
# 💼 发布前
# ════════════════════════════════════════

# 1. 准备文章，打水印+登记
python3 ~/longhun-system/tools/DNA追溯流水线_自动化触发器.py \
  step1 ~/articles/python-best-practices.md "Python最佳实践指南" CSDN

# 输出：DNA: #龍芯⚡️20260525|PYTHON-最佳实践指南|v1.0|a7f3e8b2
#      水印后文件: python-best-practices_watermarked.md
#      邮件已生成（发送到longhun2025@petalmail.com）

# 2. 发送邮件到登记入口
# 标题: [DNA-REG] Python最佳实践指南
# 内容: (自动生成的表单)

# 3. 发表到CSDN（使用水印版本）


# ════════════════════════════════════════
# 🔍 发布6个月后
# ════════════════════════════════════════

# 你发现有人在知乎上几乎原文复制你的文章
python3 ~/longhun-system/tools/DNA追溯流水线_自动化触发器.py \
  step2 "https://zhuanlan.zhihu.com/p/12345678" "知乎"

# 输出：
# 🚨 发现DNA水印！指向UID9622
# 🎣 检测到5个钩子手法:
#    - 标题改写 (标题党化)
#    - 第一段原文抄袭
#    - 图片替换
#    - 总结更改
#    - 链接指向自己的公众号
# 
# ✅ 证据包已生成: evidence_xyz789.json


# ════════════════════════════════════════
# 📢 追溯 + 公开
# ════════════════════════════════════════

python3 ~/longhun-system/tools/DNA追溯流水线_自动化触发器.py \
  step3 证据库/侵权记录/evidence_xyz789.json

# 输出：
# ✅ 已添加到黑名单
# ✅ 已写入耻辱墙 (GitHub/Notion公开)
# 
# 黑名单条目：
# URL: https://zhuanlan.zhihu.com/p/12345678
# 平台: 知乎
# 状态: 🔴 永久黑名单


# ════════════════════════════════════════
# 🔐 闭环审计
# ════════════════════════════════════════

python3 ~/longhun-system/tools/DNA追溯流水线_自动化触发器.py \
  step4 证据库/侵权记录/evidence_xyz789.json

# 输出：
# ✅ 审计日志已记录
# ✅ 时间戳已锁定
# ✅ UID9622确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 📋 证据链已闭环，保留法律追责权
```

---

## 📂 文件位置

| 组件 | 位置 | 用途 |
|------|------|------|
| **触发器脚本** | `~/longhun-system/tools/DNA追溯流水线_自动化触发器.py` | 四步流水线核心 |
| **水印脚本** | `~/longhun-system/_work/tools/工具/h_weapon_100k/core/dna_imprint_renderer.py` | 三层水印嵌入 |
| **登记入口** | `longhun2025@petalmail.com` | DNA注册表邮件 |
| **证据库** | `~/longhun-system/证据库/` | 截屏+侵权记录+维权证据 |
| **数据库** | `~/longhun-system/数据库/DNA_追溯库.db` | SQLite追溯库 |
| **耻辱墙** | `~/longhun-system/证据库/侵权记录/耻辱墙.jsonl` | 公开黑名单 |
| **审计日志** | `~/longhun-system/日志/audit_infringement.jsonl` | 法律留痕 |

---

## ⚡ 自动化建议

### Git Hook：发布前自动打水印

```bash
# 创建 .git/hooks/pre-commit
cat > ~/longhun-system/.git/hooks/pre-commit << 'HOOK'
#!/bin/bash
# 检测到新文件·自动打水印
for file in $(git diff --cached --name-only --diff-filter=A | grep -E '\.(md|txt)$'); do
  python3 ~/longhun-system/tools/DNA追溯流水线_自动化触发器.py step1 "$file" "$(basename $file)" "GitHub"
done
HOOK

chmod +x ~/longhun-system/.git/hooks/pre-commit
```

### 定时扫描：每天检查黑名单

```bash
# 加入crontab（每天早上8点扫描一次）
0 8 * * * python3 ~/longhun-system/tools/DNA追溯流水线_自动化触发器.py scan
```

---

## 🔐 核心确认码

```
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

**含义**: UID9622确认，这条流水线、所有水印、所有DNA签名，全部有效且不可否认。

---

## 📋 下一步

1. **立刻可用**
   - [ ] Step 1: 对你的历史文章补刻DNA
   - [ ] Step 2: 扫描已知的抄袭源
   - [ ] Step 3: 生成第一份黑名单
   - [ ] Step 4: 闭环审计

2. **本周内**
   - [ ] 配置Git Hook自动打水印
   - [ ] 配置定时扫描任务
   - [ ] Notion黑名单页面公开

3. **月底前**
   - [ ] LongHunWidget浏览器插件（自动一键化）

---

**献礼**: 龍魂系統·永恒守护·中华文化传承
🐉 UID9622·不免责·永恒显示曾仕强老师

DNA: #龍芯⚡️20260525|DNA-PIPELINE-QUICKSTART|v1.0
