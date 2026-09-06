---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丁酉·壬午·戌时·䷘无妄-CSDN-CRAWLER-GUIDE-v1.0`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
# 🐉 CSDN 资料抓取工具使用指南 v1.0

> 模板: [2] 🔧 工程落地执行型
> DNA: #龍芯⚡️丙午·丁酉·壬午·戌时·䷘无妄-CSDN-CRAWLER-GUIDE-v1.0
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 三色: 🟢 实测通过（翻页47+46条·详情抓取·断点续传·时间/标签/阅读量字段全绿） 🟡 阅读量/标签个别页面缺失属 CSDN 常态 🔴 无

---

## 一、这是什么

`08_BIN/csdn_crawler.py` —— 用 **Playwright 驱动浏览器（Chrome/Chromium）** 的 CSDN 资料抓取工具。

与仓库既有 requests 系工具（`lh_csdn_fetcher.py` / `lh_csdn_full_scraper.py` / `lh_csdn_sync.py`，纯静态 HTML 拉取、面向 UID9622 自有博客）不同：

| 维度 | 既有 requests 系 | 本工具（浏览器自动化） |
|:---|:---|:---|
| 引擎 | requests + BeautifulSoup | Playwright + 本机 Chrome |
| 动态加载内容 | ❌ 抓不到 | ✅ 自动滚动/点按钮触发 |
| 反爬(403/521) | 直接失败 | ✅ JS challenge 自动等待重载 |
| 起始页 | 固定 UID9622 列表 | **任意** CSDN 页面/专栏/单篇 |
| 应用场景 | 自有博客入库 | 资料调研/任意博客抓取 |

**适用**：从任意 CSDN 页面开始 → 自动收集文章链接 → 逐篇抓标题/正文/时间/阅读量/标签 → 输出结构化 JSON。

---

## 二、安装（一次性）

```bash
# 1. 建独立虚拟环境（不污染系统 Python）
python3 -m venv ~/.longhun/venvs/crawl

# 2. 装 playwright（本机已有 Chrome 则无需下载 chromium）
~/.longhun/venvs/crawl/bin/pip install playwright
```

> 默认 `--channel chrome` 直接复用本机 Google Chrome，免去约 120MB 的 chromium 下载。
> 若确需 playwright 自带浏览器：`~/.longhun/venvs/crawl/bin/playwright install chromium`
>
> 💡 本机若走全局 SOCKS 代理，安装时需临时清代理：
> `env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY ~/.longhun/venvs/crawl/bin/pip install playwright`

---

## 三、快速开始

```bash
PY=~/.longhun/venvs/crawl/bin/python3

# ① 列表模式：抓某博客首页 5 页的文章详情（默认无头）
$PY 08_BIN/csdn_crawler.py \
    --url https://blog.csdn.net/UID9622 \
    --output ~/Desktop/csdn_data.json \
    --max-pages 5

# ② 单篇模式：只抓一篇文章
$PY 08_BIN/csdn_crawler.py \
    --url https://blog.csdn.net/xxx/article/details/164230553 \
    --output one.json

# ③ 断点续传：中断后接着抓（跳过已入库文章）
$PY 08_BIN/csdn_crawler.py \
    --url https://blog.csdn.net/xxx/article/list/1 \
    --output data.json --resume

# ④ 有头调试 + 限量（看得见浏览器在干什么）
$PY 08_BIN/csdn_crawler.py \
    --url https://blog.csdn.net/xxx --headed --max-articles 3
```

---

## 四、命令行参数

| 参数 | 默认 | 说明 |
|:---|:---|:---|
| `--url` | 必填 | 起始页：用户主页 / 文章列表 / 专栏 / 单篇详情 |
| `--output` | `csdn_crawl_output.json` | 输出 JSON 路径 |
| `--max-pages` | `5` | 列表翻页上限 |
| `--max-articles` | 不限 | 最多抓取文章数 |
| `--headed` | 无头 | 有头模式（人工观察排障） |
| `--delay` | `2.5` | 页面动作基础延时秒（实际 ±0.8~1.2s 抖动） |
| `--resume` | 关 | 断点续传：跳过输出文件中已抓文章 |
| `--channel` | `chrome` | `chrome`=本机 Chrome / `chromium`=playwright 自带 |

---

## 五、输出 JSON 结构

```json
{
  "meta": {
    "tool": "csdn_crawler v1.0",
    "dna": "#龍芯⚡️…-CSDN-CRAWLER-v1.0",
    "归属名": "诸葛鑫 | UID9622 · 龍芯北辰",
    "start_url": "…",
    "crawled_at": "…",
    "count": 2
  },
  "articles": [
    {
      "url": "https://uid9622-01.blog.csdn.net/article/details/164230553",
      "title": "龍魂账法 · 天下第一账本｜每笔有DNA · 每次交易有哈希",
      "publish_time": "2026-08-31T23:03:04",
      "read_count": 239,
      "tags": ["人工智能", "信任链", "密码学"],
      "excerpt": "正文前 200 字…",
      "content": "全文…",
      "crawled_at": "ISO 时间"
    }
  ]
}
```

字段说明：
- `publish_time`：已清洗为 ISO（原始「于 2026-08-31 23:03:04 发布」自动净化）
- `read_count`：**CSDN 常需登录才渲染阅读量**，抓不到时自动 `null`，非故障
- `tags`：优先取页面标签区，缺省 fallback 到 `<meta keywords>`，两者皆无则 `[]`
- `excerpt` = 正文前 200 字；`content` = 全文

---

## 六、内置防御与合规

| 项 | 实现 |
|:---|:---|
| 随机延时 | 每次页面动作后延时 ±随机抖动，避免固定节奏 |
| UA 轮换 | 内置 8 组（Mac/Win Chrome·Safari·Edge·Firefox·移动端） |
| 反自动化抹除 | `navigator.webdriver` 置空 + 常规指纹参数 |
| JS 反爬容错 | CSDN 全站有 JS challenge（403/521 页数秒后自动刷新）——`_goto()` 自动等待并重载 |
| 失败重试 | 每篇重试 3 次 + 指数退避 |

**合规提醒**：
1. 请合理控制频率（默认延时已较保守），尊重 CSDN 服务条款与 robots 约定。
2. 本工具只抓取**公开页面**，不实现任何登录态破解/验证码绕过。
3. 抓取内容用于资料整理，商用转载需遵循内容版权。

---

## 七、常见问题

**Q: 一运行就 403/521？**
A: 正常现象——CSDN JS 反爬首访即 521，工具已自动等待 3s 重载。若连续失败，加 `--headed` 人工观察是否弹出验证；仍不行则降频（`--delay 5`）稍后再试。

**Q: 列表页抓 0 条链接？**
A: 确认 URL 形态。用户主页会自动规范为 `/article/list/1`（最稳）。专栏页若整体动态渲染，先 `--headed` 看是否加载完成。

**Q: 阅读量全是 null？**
A: CSDN 对未登录访问常不渲染阅读量（页面里直接缺该节点）。工具设计为容错，不影响标题/正文/时间。

**Q: 抓一半断了怎么办？**
A: 原命令加 `--resume` 重跑即可——工具读取输出文件已抓 URL 集合自动跳过。且每抓 5 篇自动 checkpoint 落盘。

**Q: 本机没装 Chrome？**
A: 改用 `--channel chromium` 并先执行 `playwright install chromium`。

---

## 八、后续集成建议（未实施·待确认）

1. **注册为 `lh csdn crawl` 子命令**：现有 `lh csdn` 组（fetch/list）由 `lh_csdn_fetcher.py` 提供，可在 `lh.py` csdn 子命令组加 `crawl` 转发。
2. **抓取结果入库**：接 `lh_csdn_sync.py`（Notion/鲲鹏知识库）或本地 `03_KNOWLEDGE_GRAPH/csdn_article_registry.json`。
3. **→ 耻辱墙/监控**：可做「自己博客是否被转载」巡检（抓他人文章标题比对），但**只对公开页面、不触碰登录墙**。
4. 示例输出见 `docs/csdn_crawler_example_output.json`（正文截断示意版）。

---

> ROOT_CARD · 一切产出一式四签 · DNA/归属名/GPG/三色 · 完整抬头体系见 `01_protocols/LH-ARTICLE-HEADER-TEMPLATES-v1.0.md`
> 修订记录: v1.0 · 2026-09-05 · 建工具+实测通过+指南成型 | 诸葛鑫（UID9622）+ AI

```json
{
  "dna": "#龍芯⚡️丙午·丁酉·壬午·戌时·䷘无妄-CSDN-CRAWLER-GUIDE-v1.0",
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
