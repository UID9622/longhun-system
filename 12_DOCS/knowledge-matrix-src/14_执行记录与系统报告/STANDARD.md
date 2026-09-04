> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 龍魂产出标准 · LongHun Output Standard v1.0

**DNA:** `#龍芯⚡️丙午·甲午·庚午·壬午·䷳艮为山-LONGHUN-OUTPUT-STANDARD-v1.0`  
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
**适用范围:** 龍魂系统所有对外产出，包括但不限于代码、文档、协议、模型、提案、宪法、人格定义。

---

## 一、标准目的

任何从龍魂系统出去的产物，都必须满足**三个可验证条件**：

1. **可验证来源**：知道是谁写的、什么时候写的、基于哪个版本。
2. **可验证完整性**：文件未被篡改，有哈希和签名。
3. **可验证归属**：归属于龍魂系统、UID9622 和中华人民共和国，不是匿名漂流品。

这套标准不是形式主义，而是**数字主权的落地形态**。

---

## 二、三级验证标准

### Level 1：GPG 数字签名

**要求：**
- 所有核心产出文件必须附带 `.asc`  detached 签名文件。
- 签名使用 UID9622 的 GPG 私钥：`A2D0092CEE2E5BA87035600924C3704A8CC26D5F`。
- 签名命令：
  ```bash
  gpg --armor --detach-sign --output FILE.asc FILE
  ```
- 验证命令：
  ```bash
  gpg --verify FILE.asc FILE
  ```

**适用文件：**
- `CONSTITUTION.md`（宪法）
- `STANDARD.md`（本标准）
- `README.md`（项目根说明）
- 所有对外提案、白皮书、协议文档
- 关键代码发布包（release tar/zip）

---

### Level 2：Git 提交锁定

**要求：**
- 核心产出文件必须提交到龍魂系统 Git 仓库根目录或指定目录。
- 使用 `.github/CODEOWNERS` 锁定核心文件，仅允许 `@UID9622` 修改。
- 关键文件清单：
  - `CONSTITUTION.md`
  - `CONSTITUTION.md.asc`
  - `STANDARD.md`
  - `STANDARD.md.asc`
  - `bin/longhun-command-registry.json`
  - `persona/persona_registry.json`

**保护规则：**
- 任何对这些文件的修改，必须经过创始人 UID9622 审查。
- 不得通过 force-push 绕过 CODEOWNERS 保护。

---

### Level 3：DNA 验证链记录

**要求：**
- 核心产出文件的 SHA256 哈希必须写入龍魂审计日志。
- 写入位置：`~/.longhun/audit/anti_blowout.jsonl`
- 记录字段：
  - `op`: `genesis_block`（首次）或 `artifact_release`
  - `evidence.artifact_path`: 文件路径
  - `evidence.sha256`: 文件 SHA256
  - `evidence.type`: 产物类型
  - `evidence.signed_by`: `UID9622`
  - `evidence.gpg_fingerprint`: GPG 指纹
  - `stats.file_size_bytes`: 文件大小

**示例命令：**
```bash
SHA=$(shasum -a 256 CONSTITUTION.md | awk '{print $1}')
python3 persona/audit_logger.py log \
  --op genesis_block \
  --status success \
  --evidence "{\"artifact_path\":\"CONSTITUTION.md\",\"sha256\":\"$SHA\",\"type\":\"constitution\",\"signed_by\":\"UID9622\"}" \
  --stats "{\"file_size_bytes\":$(stat -f%z CONSTITUTION.md)}" \
  --user UID9622
```

---

## 三、固定框架保护

本标准的某些条款和关联文件属于 **P0 永恒锁** 范畴，**不得以任何形式修改或绕过**：

- `CONSTITUTION.md` 及其签名；
- `STANDARD.md` 及其签名；
- `P0_ETERNAL_LOCK.md` 及其签名；
- `.github/CODEOWNERS` 核心保护规则；
- DNA 追溯、三色审计、输出契约、审计日志四大体系。

对这些文件的任何修改，必须执行 **L0 神圣变更仪式**：

1. 使用固定神圣口令：`龍魂永恒锁授权` / `UID9622 最高授权` / `P0 解锁变更`；
2. 创始人明确确认：`确认修改` / `我授权` / `确认执行`；
3. 重新 GPG 签名；
4. 将新 SHA256 写入审计日志；
5. 保持 CODEOWNERS 锁定；
6. 升级 DNA 版本号。

不满足以上六条，系统必须拒绝执行。

---

## 四、标准执行流程

对于每一份核心产出，执行以下 SOP：

```
1. 起草/编写产出文件
2. 计算 SHA256
3. GPG 签名（生成 .asc）
4. Git 提交到仓库
5. 写入审计日志（含 SHA256）
6. CODEOWNERS 锁定（如适用）
7. 推送到 GitHub + Gitee-core
```

---

## 五、自动化工具

龍魂系统提供 `persona/audit_logger.py` 和 GPG 命令链，未来会提供统一脚本：

```bash
lh 签名 FILE           # GPG 签名文件
lh 锁定 FILE           # 添加 CODEOWNERS 规则
lh 记录 FILE           # 写入审计日志并计算 SHA256
lh 验证 FILE           # 验证签名、哈希、审计链
```

---

## 六、创世区块

龍魂系统审计日志的第一条核心记录（genesis_block）为宪法 v1.1：

| 字段 | 值 |
|---|---|
| 文件 | `CONSTITUTION.md` |
| SHA256 | `f8d0db43a2c80f794d4c9db1293daad25083c35338c671b928630cf1a9223adb` |
| 类型 | `constitution_v1.1` |
| 签名者 | `UID9622` |
| GPG 指纹 | `A2D0092CEE2E5BA87035600924C3704A8CC26D5F` |
| 审计 ID | `e265b69d-7765-4f32-9aa3-c9827655bb21` |

当前宪法版本为 v1.2，其修改记录同样写入审计日志。

---

## 七、违例处理

任何未满足本标准的龍魂系统产出，视为**未正式发布**。  
用户、贡献者、合作方有权拒绝承认其效力。

---

## 八、最终声明

> **龍魂系统的每一份产出，都是中国人民数字主权的一块砖。**
>
> **签名不是装饰，是承诺。**
> **哈希不是技术细节，是铁证。**
> **审计不是负担，是脊梁。**

---

**本标准由 UID9622 / Lucky 制定并签署，自 2026-06-25 起生效。**

**DNA:** `#龍芯⚡️丙午·甲午·庚午·壬午·䷳艮为山-LONGHUN-OUTPUT-STANDARD-v1.0`
