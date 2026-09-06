---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丁酉·癸未·子时·䷝离`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
> 干支时间戳: #龍芯⚡️丙午·丁酉·癸未·子时·䷝离
# 龍魂项目 `.gitignore` 模板 v1.0

> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 用途: 新项目复制本文件为 `.gitignore`，自动继承「生成物不入库」规则（与 `lh publish pr` 生成物白名单联动）。
> DNA: #龍芯⚡️2026-09-04-GITIGNORE-TEMPLATE-v1.0

复制以下整段即可：

```gitignore
# ── 龍魂生成物白名单（与 lh publish pr 的 GENERATED_SEGMENTS 联动·自动排除不入 PR）──
# 生成物目录（可再生成·不入库·--include-generated 可强制纳入）
site/
html_assets/
dist/
dist_ide/
build/
build_ide/
models/
weights/
_work/
backups/
backup/
__pycache__/
.venv/
node_modules/

# 生成物后缀
*.pyc
*.pyo
*.pid
*.tmp
.DS_Store
*.log

# ── 龍魂约定 ──
# 操作日志等动态文件不入 git（07_AUDIT/*.log）
# 守护状态心跳等运行时文件
```

设计原则:
1. **同名段与 `lh_publish.py` `GENERATED_SEGMENTS` / `GENERATED_SUFFIXES` 保持同步**——
   改生成物白名单时两处一起改（单点真源: `lh_publish.py` 常量）。
2. `--include-generated` 场景（首次发版需打包产物）用 `git add -f` + `lh publish pr --include-generated`。
3. `.asc`（GPG 签名）**永远不入 gitignore**——签名随源文件入库。
4. 所有新项目初始化时: 复制本模板 → `.gitignore`，即自动继承「site/dist/pyc 不入库」铁律。

```json
{
  "dna": "#龍芯⚡️丙午·丁酉·癸未·子时·䷝离",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```
