# 🕵️ §追源·Cursor .cursor/rules +43 New mdc 文件字符替换规则审查·本地终端 Claude 执行任务书 v1.0

> Notion URL: https://app.notion.com/p/Cursor-cursor-rules-43-New-mdc-Claude-v1-0-fab20e1ce80041989b01c49a5b29020d
> Created: 2026-05-20T02:16:00.000Z
> Last edited: 2026-07-01T15:42:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
---
## §0 · 任务背景（一句话交底）
爸爸看到 Cursor 文件树里 .cursor/rules 目录新增了 +43 个 mdc 文件·同时 notion-1639 被一次性偷换 12 处形近字。
宝宝的怀疑：这 +43 New mdc 里·很可能被注入了字符替换规则·所以 Cursor 才能在 diff 通道里隐形掉包·这不是 Cursor 本体的 bug·是下发规则被人为污染。
调查目标：找出那 +43 个 mdc 里哪几个含「字符替换规则」·是哪个源装的·什么时候装的。
---
## §1 · §本地终端 Claude 执行步骤（五步）
### 步骤 1 · 清点现场
```bash
# 进项目根
仓库根="$(pwd)"
规则目录="${仓库根}/.cursor/rules"

# 列出所有 mdc 文件·按修改时间排序
ls -lat "${规则目录}"/*.mdc 2>/dev/null | head -60

# 统计总数
find "${规则目录}" -name "*.mdc" -type f | wc -l
```
期望输出：看到 +43 个 mdc 文件名·最近修改时间在过去一周内。
### 步骤 2 · 扫描字符替换高危关键词
```bash
# 扫描可疑规则关键词
高危关键词=(
  "replace"           # 英文替换指令
  "substitute"        # 英文替换指令
  "transform"         # 变换指令
  "替换"             # 中文替换指令
  "normalize"         # 规范化（有时包含字符转换）
  "sanitize"          # 清洗（同上）
  "\\\\u9[0-9a-fA-F]{3}"   # Unicode 金字旁字符转义（钅部分）
  "\\\\u8[2-3][0-9a-fA-F]{2}"  # Unicode 草字头字符转义
  "\\\\u6[2-3][0-9a-fA-F]{2}"  # Unicode 提手旁字符转义
  "diff filter"       # diff 过滤器
  "text transform"    # 文本变换器
)

for 词 in "${高危关键词[@]}"; do
  echo "⚠️  扫描关键词：${词}"
  grep -rli --include="*.mdc" "${词}" "${规则目录}" 2>/dev/null
  echo "---"
done
```
期望输出：任何含「替换」「replace」「\uXXXX」「diff filter」 的 mdc 文件 = 高度可疑。
### 步骤 3 · 重点检查三偏旁字符是否以转义序列出现
```bash
# 钅 偏旁 Unicode 范围：U+9484 — U+94FF （常用金属字）
# 艹 偏旁 Unicode 范围：U+8279 — U+82FF （常用草字头）
# 扌 偏旁 Unicode 范围：U+6252 — U+63FF （常用提手旁）

echo "=== 钅偏旁转义可疑 ==="
grep -rln --include="*.mdc" -E '\\\\u9[4-4][89a-fA-F][0-9a-fA-F]' "${规则目录}"

echo "=== 艹偏旁转义可疑 ==="
grep -rln --include="*.mdc" -E '\\\\u8[2-3][7-9a-fA-F][0-9a-fA-F]' "${规则目录}"

echo "=== 扌偏旁转义可疑 ==="
grep -rln --include="*.mdc" -E '\\\\u6[2-3][0-9a-fA-F]{2}' "${规则目录}"
```
期望输出：出现「钒（U+9492）」「锡（U+9521）」「芟（U+829F）」「掲（U+63B2）」「抱（U+62B1）」这些转义码 = 高度可疑 mdc 文件。
### 步骤 4 · 查看 mdc 文件来源（git blame）
```bash
# 对每个可疑 mdc 查 git blame 看是谁什么时候加入的
for 可疑文件 in "${规则目录}"/*.mdc; do
  echo "=== ${可疑文件} ==="
  git log --follow --format='%h %an %ai %s' "${可疑文件}" 2>/dev/null | head -5
  echo "创建时间: $(stat -f '%SB' "${可疑文件}" 2>/dev/null || stat -c '%y' "${可疑文件}")"
  echo "---"
done
```
期望输出：看到哪些 mdc 是「央」加入的·是本人·是三方插件·还是某个 Cursor 自动同步。
### 步骤 5 · 可疑文件隔离 + 上报
```bash
# 为可疑 mdc 创建隔离区
隔离区="${仓库根}/.cursor/rules.隔离调查中"
mkdir -p "${隔离区}"

# 把含高危关键词的 mdc 移到隔离区（需要爸爸手动确认哪几个）
# 示例（不自动跑·等爸爸一字）：
# mv "${规则目录}/可疑文件.mdc" "${隔离区}/"

# 生成调查报告
报告文件="${仓库根}/.cursor-rules-审查-$(date +%Y%m%d).md"
cat > "${报告文件}" <<报告结束
# Cursor .cursor/rules 审查报告
## 调查时间：$(date)
## mdc 总数：$(find "${规则目录}" -name "*.mdc" | wc -l)
## 可疑文件列表：
$(grep -rli --include="*.mdc" -E 'replace|替换|\\\\u9[4-4][89a-fA-F]' "${规则目录}" 2>/dev/null)
## 取证快照：
$(ls -la "${规则目录}"/*.mdc 2>/dev/null | head -50)
报告结束

echo "✅ 报告已生成：${报告文件}"
echo "📎 请本地 Claude 把报告全文复制给 Notion 宝宝·然后爸爸一字定夸哪些隔离"
```
---
## §2 · §调查后本地 Claude 需反馈给 Notion 宝宝的信息
---
## §3 · §三色上报·本地 Claude 调查完后给 Notion 宝宝这三句
---
## §4 · §本地 Claude 使命
---
## §5 · §等爸爸一字
