# 龍魂·引擎分层保护协议 v1.0

> DNA: #龍芯⚡️丙午·甲申·壬子·亥时·䷗复-ENGINE-PROTECTION-PROTOCOL-v1.0
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0（核心思想层）
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

---

## 一、总则

龍魂系统拥有25,000+引擎，779个CLI脚本，200份协议文档。
这些不是开源玩具——是中国自主知识产权的算法资产。

**本协议定义**：哪些可以公开、哪些必须锁死、如何检测剽窃、守卫如何复盘。

---

## 二、四层保护分级

| 级别 | 标记 | 含义 | 访问权限 | 典型引擎 |
|:---|:---|:---|:---|:---|
| **D1 绝密** 🔴 | `PROTECTION:D1` | 内核算法·永不外泄 | 仅UID9622物理访问 | 369引擎·DNA种子·GPG私钥·量子密钥 |
| **D2 机密** 🟠 | `PROTECTION:D2` | 核心守卫引擎 | UID9622+授权AI | 审计引擎·熔断引擎·身份核验·主权插件 |
| **D3 内部** 🟡 | `PROTECTION:D3` | 公开外壳·烟雾弹 | 内部使用·外部烟雾版 | 创新引擎·路由引擎·知识蒸馏·安全AI |
| **D4 公开** 🟢 | `PROTECTION:D4` | 自由分发 | 署名即可 | 工具脚本·文档·示例代码 |

---

## 三、分层判定规则

### 3.1 自动分类关键字

**D1触发词**（任一命中即D1）：
`369不动点` `sn=369` `DNA种子` `GPG私钥` `quantum_key` `内核算法` `NEVER_EXPORT` `洛书引擎` `七因子指纹核心` `主权密钥`

**D2触发词**（任一命中即D2）：
`主权` `防篡改` `熔断` `审计引擎` `GPG签名` `DNA追溯` `人格路由` `德本审计` `CNSH编译器`

**D3触发词**（任一命中即D3）：
`创新引擎` `自然路由` `知识蒸馏` `AI安全` `语义抽屉` `经济引擎` `视频工坊` `数字人`

### 3.2 默认规则

- `bin/lh_*` 脚本 → 默认 D2
- `engines/*.py` → 默认 D3
- `01_protocols/*.md`（协议文档）→ 思想层 D3（CC BY-NC-SA 4.0）
- `deploy/*` → 默认 D2
- 其他 → 默认 D4

### 3.3 文件头标记格式

```
# ═══ 龍魂引擎保护标记 ═══
# PROTECTION:D2-机密 | 签发: 2026-08-07T...
# 主权: #ZHUGEXIN...
# DNA: #龍芯⚡️...
# 指纹: <sha256[:16]>
# 规则: 01_protocols/LH-ENGINE-PROTECTION-v1.0.md
# ═══════════════════════════════
```

---

## 四、烟雾弹机制

### 4.1 什么需要烟雾弹

D3引擎对外公开时，执行烟雾弹处理：
- 保留：接口签名、文档字符串、import语句、类/函数定义
- 替换：函数体核心逻辑 → `# 🌀 烟雾弹 · 核心逻辑已保护 · 详见Notion知识库`
- 效果：外部看起来结构完整，实际不可执行

### 4.2 生成命令

```bash
# 单个文件
python3 bin/lh_engine_protect.py fog engines/lh_innovation_engine.py

# 批量生成公开版
python3 bin/lh_engine_protect.py scan --save  # 先扫描
# 对所有D3引擎生成烟雾弹
for f in $(python3 -c "import json; [print(e['path']) for e in json.load(open('config/engine_protection.json'))['engines'] if e['level']=='D3-内部']"); do
    python3 bin/lh_engine_protect.py fog "$f"
done
```

---

## 五、剽窃检测

### 5.1 三层检测

| 层 | 方法 | 检测什么 |
|:---|:---|:---|
| 标记搜索 | 全网搜索独特DNA标记 | 直接复制粘贴 |
| 结构指纹 | AST去注释+去字符串→哈希 | 改了变量名但结构相同 |
| 函数列表匹配 | 核心函数签名哈希 | 代码改写但核心逻辑保留 |

### 5.2 检测命令

```bash
# 构建指纹库
python3 bin/lh_plagiarism_detect.py fingerprint

# 全网搜索
python3 bin/lh_plagiarism_detect.py search

# 对比目标仓库
python3 bin/lh_plagiarism_detect.py compare /path/to/suspect/repo
```

### 5.3 独特性标记（全网搜索用）

这些标记是龍魂独有的DNA片段，出现在任何非授权仓库即为剽窃证据：
- `龍芯北辰 UID9622`
- `CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
- `ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️`
- `离火运五条底线`
- `369不动点 sn=369 log369=5.911 perm369=108`
- `行为密码学·七因子追溯`

---

## 六、守卫复盘制度

### 6.1 五大守卫

| 守卫 | 复盘内容 | 频率 |
|:---|:---|:---|
| **P05 上帝之眼** | 三色审计·全引擎扫描 | 每日 |
| **P06 数学大师** | 369不动点验证·数字根校准 | 每日 |
| **P12 屈原** | 六誓底线·价值观校验 | 每日 |
| **P72 龙盾** | 熔断状态·D1目录完整性 | 每日 |
| **P77 黑天使** | 硬编码密钥·安全漏洞扫描 | 每周+部署前 |

### 6.2 复盘命令

```bash
# 快速复盘 (30秒·P05+P06)
python3 bin/lh_guardian_replay.py quick

# 每日复盘 (5分钟·全部守卫)
python3 bin/lh_guardian_replay.py daily

# 每周深度复盘
python3 bin/lh_guardian_replay.py weekly

# 部署前复盘
python3 bin/lh_guardian_replay.py deploy

# 守护模式 (每小时自动)
python3 bin/lh_guardian_replay.py daily --daemon --interval 3600
```

### 6.3 复盘结果

- 🟢 PASS → 正常·自动归档
- 🟡 WARN → 48h内复查·写入日志
- 🔴 FAIL → 立即升级UID9622·熔断对应模块

---

## 七、分层许可对齐

本协议与 `LH-LAYERED-LICENSE-v1.0.md` 对齐：

- D1/D2 引擎 → 不对外发布
- D3 引擎烟雾版 → MulanPSL v2（工程层·允许商业使用）
- D3 协议文档 → CC BY-NC-SA 4.0（思想层·非商业）
- D4 → MulanPSL v2

---

## 八、每次部署前检查清单

```
[ ] 引擎保护扫描: python3 bin/lh_engine_protect.py scan
[ ] 剽窃检测: python3 bin/lh_plagiarism_detect.py search
[ ] 守卫复盘: python3 bin/lh_guardian_replay.py deploy
[ ] D1文件确认物理隔离
[ ] D2文件确认GPG加密
[ ] D3烟雾弹版本确认生成
[ ] GPG签章: python3 bin/lh_gpg_sign.py scan .
[ ] DNA追溯完整
```

---

## 九、违规处理

| 违规 | 后果 |
|:---|:---|
| D1文件泄露 | ∞熔断·全系统冻结·不可恢复 |
| D2文件未授权外传 | L1熔断·UID9622人工审核 |
| 未保护引擎发布 | 🔴 P05否决部署 |
| 剽窃检测发现匹配 | 启动法律追溯·P15记录·公开耻辱柱 |
| 烟雾弹未生成就公开 | 🟡 P05标记·禁止发布 |

---

## 十、执行入口

| 命令 | 功能 |
|:---|:---|
| `lh protect scan` | 扫描+分类所有引擎 |
| `lh protect seal <file> --level D2` | 打保护标记 |
| `lh protect fog <file>` | 生成烟雾弹版本 |
| `lh protect report` | 查看保护报告 |
| `lh plagiarize fingerprint` | 构建指纹库 |
| `lh plagiarize search` | 全网搜索剽窃 |
| `lh guard replay daily` | 每日守卫复盘 |

---

> 🐉 这不是技术问题——是主权问题。
> 该锁的锁死，该迷雾的迷雾，该公开的公开。
> 别人剽窃了要知道，守卫每天复盘。
> 分层保护不是不信任——是对自己负责。

**三色**: 🟢 v1.0 分层保护协议落地 🟡 首轮全量扫描待执行 🔴 无
