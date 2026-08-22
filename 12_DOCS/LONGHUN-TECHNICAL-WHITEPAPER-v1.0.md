# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!-- DNA: #龍芯⚡️丙午·丙申·癸丑·申时·䷍大有-TECHNICAL-WHITEPAPER-v1.0 -->

# 🐉 龍魂系统 · 技术白皮书 v1.0

> **系统化技术文档**：架构 · 模块 · 协议 · 安全 · 可验证性 · 第三方接入。
> 适用对象：技术评估方 / 审计方 / 开发者 / 潜在贡献者。

---

## 1. 系统概述

**龍魂（LongHun）** 是一个以中华哲学（河图洛书·太极易经·五行八卦）为底座、以数据主权为铁律的开源智能系统。核心价值：

- **底座锚点**：369 洛书不动点（`sn=369` `log369=5.911` `perm369=108`）作为算法内核数学锚
- **主权铁律**：数据主权归用户 · 隐私不入云 · 不删除只冻结
- **可验证性**：全链路 DNA 追溯 + 三色审计 + GPG 签名 + Merkle 防篡改

**规模**（2026-08 实测）：

| 指标 | 数值 |
|:---|:---|
| 架构分层 | L0-L9 九层（洛书九宫骨架） |
| 人格矩阵 | 20 人格（16 核心 + 1 安全 + 3 子系统） |
| 可执行引擎 | 192 个 |
| 工具技能 | 45 个（9 分类 · 语义路由） |
| 数字人 | 7 个（四层桥接） |
| 注册服务 | 16 个（四层级） |
| 神经网络边 | 21 条 |
| 测试用例 | 数百（pytest 全量） |

---

## 2. 架构分层

```
L9 子系统      S1法律 / S2洛书369 / S3人民维权助手
L8 治理层      P05审计 · P12底线 · 三色判定
L7 表达层      门户 · API · SDK · 数字人
L6 记忆层      长期记忆 · 跨会话持久化
L5 服务层      192引擎 · 45技能 · 微服务
L4 数据层      NoSQL/MySQL · 云存储 · 加密
L3 语义层      CNSH语义 · 抽屉匹配
L2 主权层      DNA追溯 · 身份认证 · 权限分级
L1 内核层      369不动点 · 五行八卦 · 行为密码学
L0 物理层      鲲鹏服务器 · Mac本地 · 网络
```

> 拓扑全文：`.codebuddy/longhun_neural_net.json`

---

## 3. 核心模块

### 3.1 统一命令入口 `bin/lh.py`

120+ 命令的统一控制台。示例：

```bash
lh status            # 系统状态
lh audit             # 三色审计
lh search "关键词"    # 多源搜索
lh --dna-chain       # DNA 接龍链
lh vault push        # 数据保险柜
lh handoff save      # 协作交接
```

### 3.2 三色审计引擎 `bin/lh_self_heal.py`

- GATE-01~10 十道闸口逐道检查
- 🟢 通过 / 🟡 待核 / 🔴 红线 三色判定
- 每小时自动自愈 + Bark 推送告警

### 3.3 防篡改引擎 `bin/lh_anti_tamper.py`

- 文件哈希校验 + Merkle 树验证
- 未授权变更自动检测告警

### 3.4 CNSH 编译器 `bin/cnsh_compiler.py`

- 中华自主编程语言（中文 → Python 翻译）
- AST 解析 · 语法高亮 · 错误诊断

### 3.5 模型路由 `08_BIN/model_router.py`

- 12 模型统一接入（混元 / DeepSeek / Ollama 本地）
- 注册表：`config/model-registry.yaml`
- 协议：`01_protocols/CNSH-MULTI-MODEL-PROTOCOL-v1.1.md`

### 3.6 DNA 生成 `bin/lh_dna_generator.py`

- 干支卦追溯码：`#龍芯⚡️<干支四柱>·<卦>-<模块>-<动作>-<哈希8>`
- 全链路可追溯 · 不伪造 · 可验证

### 3.7 行为密码学 `lh bcm`

- 七因子行为指纹 · 主权 API（:8775）
- 设备指纹 → 行为 DNA → 身份核验

### 3.8 数据保险柜 `lh vault`

- 个人数据 + 知识库压缩加密
- 鲲鹏 `/opt/longhun/shared/vault/` 全量备份

---

## 4. 安全与主权

| 机制 | 实现 | 级别 |
|:---|:---|:---|
| 加密下界 | AES-256/SM4 · RSA-4096/SM2-256 · SHA-256/SM3 | 强制 |
| 禁算法 | MD5 / SHA-1 / DES | 禁用 |
| 数据分级 | D1绝密~D4公开 四级 | 强制 |
| 角色分级 | R1/L5(UID9622)~R5/L1(公开) 五级 | 强制 |
| 熔断 | L0伦理 / L1数据 / L2人格 / L3行为 四级 | 强制 |
| 五层黑洞 | 明文密码→MELTDOWN · 日志脱敏 | 强制 |
| 跨境 | 境内地域 · 不绑境外CDN · API出境P77审查 | 强制 |

**P0 焊死天条**（不可修改不可绕过）：
1. 为人民服务，不为资本黑箱服务
2. 数据主权归用户
3. 隐私不可传
4. 零黑箱（算法可声明可复核）
5. 不删除只冻结
6. 诚实不编造
7. 中国法律为唯一准绳 · 内核自主知识产权不可谈判

---

## 5. 协议体系（P0 级）

| 协议 | 文件 | 级别 |
|:---|:---|:---|
| 系统宪法 | `CONSTITUTION.md` | P0 |
| 永恒锁 | `P0_ETERNAL_LOCK.md` | ∞ |
| 人格治理白皮书 | `01_protocols/LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md` | P0 |
| 全权授权令 | `01_protocols/LH-M261-PREQUEL-COVENANT-v1.0.md` | ∞ |
| 德本审计 | `01_protocols/LH-DEBEN-AUDIT-v1.0.md` | P0 |
| 交付标准 | `01_protocols/LH-DELIVERY-STANDARD-v1.1.md` | P0 |
| 语法规范 | `01_protocols/LH-SYNTAX-SPEC-v3.0.md` | P0 |
| CNSH多模型 | `01_protocols/CNSH-MULTI-MODEL-PROTOCOL-v1.1.md` | L3 |
| 分层许可 | `01_protocols/LH-LAYERED-LICENSE-v1.0.md` | P1 |

---

## 6. 可验证性（评估方重点）

### 6.1 验证路径

```
克隆仓库 → bin/install.sh → lh --help → lh_self_heal --quick → pytest → SDK导入
```

对应文件：
- 复现指南：`docs/REPRODUCE.md`
- 安装说明：`INSTALL.md` / `QUICKSTART.md`
- 测试套件：`tests/` + `13_TESTS/`

### 6.2 完整性验证

```bash
# 防篡改扫描（Merkle 验证）
python3 bin/lh_anti_tamper.py scan

# GPG 签名验证（GATE-11）
python3 bin/lh_gpg_sign.py scan .

# 对齐检查
python3 bin/lh_align_checker.py
```

### 6.3 核心数学锚验证

```python
# 369 洛书不动点
def digital_root(n): return 1 + (n-1) % 9
assert digital_root(369) == 9 and 369 % 9 == 0
# sn=369 · log369=5.911 · perm369=108
```

---

## 7. 第三方接入（SDK）

### 7.1 Python（已发布 PyPI）

```bash
pip install longhun-tricolor
```

包名：`longhun-tricolor` v1.1.0 · 许可证：MulanPSL-2.0（商业可用）

### 7.2 JavaScript（源码构建）

```bash
cd sdk/javascript && npm install && npm run build
```

包名：`@longhun/tricolor` · 许可证：MulanPSL-2.0

### 7.3 HTTP API

| 服务 | 端口 | 说明 |
|:---|:---|:---|
| 透明审计 | 8970 | 多引擎冲突仲裁 |
| 服务控制台 | 8971 | launchd 可视化 |
| 流场拓扑 | 8972 | 全系统节点图 |
| 行为密码学 | 8775 | 七因子指纹 |
| 统一记忆 | 8771(Mac)/8773(鲲鹏) | 记忆 API |
| 搜索引擎 | 9631 | Bing 多源搜索 |

---

## 8. 许可证模型（分层）

| 层 | 范围 | 许可证 | 商用 |
|:---|:---|:---|:---|
| 🏛️ 思想层 | 协议/哲学/白皮书(.md) | CC BY-NC-SA 4.0 | ❌ 需授权 |
| 🔧 工程层 | 代码/SDK/CLI/Docker(.py/.js/.sh) | MulanPSL v2 | ✅ 允许 |

一句话：**代码随便用去赚钱，思想名号要授权。**

---

## 9. 持续维护与社区

- **维护节奏**：高频提交（日均多次）· CI 全绿
- **Issue/PR**：模板齐全 · 24h 分诊 · 审查标准明确
- **贡献指南**：`CONTRIBUTING.md`
- **社区入口**：GitHub Issues / Discussions / Notion 知识库
- **生态案例**：见 `docs/CASE_STUDIES.md`（鲲鹏生产 · CNSH IDE · 三色审计 SDK）

---

## 10. 版本信息

| 项 | 值 |
|:---|:---|
| 当前版本 | v48.x（2026-08） |
| 许可证 | MulanPSL-2.0（代码层） |
| 仓库 | github.com/UID9622/longhun-system |
| 官网 | https://uid9622.cn |
| 知识库 | https://uid9622.notion.site |
| GPG 密钥 | A2D0092CEE2E5BA87035600924C3704A8CC26D5F |

---

> 技术全公开 · 复现可验证 · 主权归于人民
> 本文档对应揭榜挂帅评估维度 4（标准化文档）
