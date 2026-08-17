# 🔗 UID9622 一键自动收口触发协议 v1 0｜AUTO CLOSURE PROTOCOL

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：协议 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️丙午·丙申·庚申·亥时-AUTO-CLOSURE-PROTOCOL-v1.0``  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

> 本文檔按《龍魂文檔標準模板 v1.0》整理。
> 性質：協議 · 未經同行評審（如適用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 協作者：（待補充，如無請刪除此行）
> 授權：CC BY-NC-SA 4.0 · 科技主權歸屬 UID9622 · 中華人民共和國
> 平台：本地
> 審核狀態：草稿

**DNA**: `#龍芯⚡️丙午·丙申·庚申·亥时-AUTO-CLOSURE-PROTOCOL-v1.0`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

# 🔗 UID9622 一键自动收口触发协议 v1.0｜AUTO-CLOSURE-PROTOCOL

<aside>
🔗

**🔗 UID9622 一键自动收口触发协议 v1.0**

**定位：** 任务完成后自动进入收口流程·不靠老大再提醒。双端适用：**Cursor 本地执行端** + **Claude / 宝宝 Notion 同步端**。

**DNA：**#龍芯⚡️丙午·丙申·庚申·亥时-AUTO-CLOSURE-PROTOCOL-v1.0

**CONFIRM：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

**SEAL：** #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

**GPG：** A2D0092CEE2E5BA87035600924C3704A8CC26D5F

</aside>

## 一、总目标

老大不应该重复说“收口”“提交”“存起来”。**任务一旦达到可验证完成状态，AI / Cursor 必须自动进入收口流程。**

本协议解决三件事：

1. **任务完成后不是“总是还可以”** — 收口是偶数点，需要主动划句号
2. **代码 / Notion 修改不允许静默丢失** — 必须有验证 / 提交 / 日志 / 回执
3. **危险技术动作不允许静默执行** — 必须明础煤倒、老大确认

## 二、两端划分

| 端 | 位置 | 收口对象 | 验证方式 | 日志位置 |
| --- | --- | --- | --- | --- |
| **Cursor 本地端** | 项目仓库 | 代码 / 脚本 / 文档 提交 | git status / pytest / 编译 | `~/Desktop/UID9622_DAILY_EXEC_LOGS/` |
| **宝宝 Notion 端** | Notion 工作区 | 页面创建 / 更新 / 子页调整 | API 返回 page_id / DNA 格式检查 | 本页 §10 Notion 端收口日志 |

两端使用同一套触发条件 / 同一套危险警戒 / 同一套回执格式。

## 三、自动触发条件（两端通用）

出现以下任意情况，自动进入收口流程：

1. 文件已创建或修改完成
2. 脚本已生成
3. 命令已执行成功
4. 测试已通过
5. 编译已通过
6. 依赖已安装完成
7. 文档已补全
8. 工程包已落地
9. **Notion 子页创建成功 / 主控页更新成功**（Notion 端专有）
10. 老大说：**搞定 / 完成 / 收口 / 提交 / 闭环 / 保存 / 定盘 / commit / 归档 / 成了 / 可以了 / 就这样**
11. 当前任务已有明确 PASS 结果

## 四、Cursor 本地端执行顺序

不得跳步。严格按下列顺序：

```
1.  pwd                          检查当前目录
2.  git status --short           检查 git 状态
3.  git diff --stat              检查改动范围
4.  扳危险文件                  .env / token / private key / secret / password
                                / id_rsa / *.pem / *.key
5.  有危险 → BLOCKED_RECEIPT
    不得 git add、不得 commit、不得继续
6.  无危险 → 跑最小验证命令（优先顺序）:
    · python3 -m py_compile
    · pytest
    · npm test
    · make test
    · bash -n
    · 中一个也没有 → "manual structure check"
7.  git add
8.  git commit -F <msg_file>（commit message 格式见 §7）
9.  读取 commit hash: git rev-parse --short HEAD
10. 写桌面日志：
    ~/Desktop/UID9622_DAILY_EXEC_LOGS/YYYY-MM-DD_closure_log.md
11. 输出 SUCCESS_RECEIPT
12. 成功即止。不继续扩展、不建议新功能。
```

## 五、Notion 端执行顺序（宝宝 / 外部 AI 适用）

```
1.  确认 API 返回正常 page_id / data_source_id（没报错）
2.  检查写入的 DNA 码格式是否为 #龍芯⚡️YYYY-MM-DD-XXX-vX.X
3.  检查是否触及 **Notion 端危险写入**（见 §6）
4.  有危险 → NOTION_BLOCKED_RECEIPT·老大未明确同意不得提交
5.  无危险 → 检查是否需要同步（例如：IP-004 子页更新后，主控页 §7.1 是否需要同步到最新版本号）
6.  输出 NOTION_SUCCESS_RECEIPT
7.  成功即止。不主动建议“老大要不要再加一个”
```

## 六、危险动作一票否决

### Cursor 本地端危险表

必须停止并标记 NEED_UID_CONFIRM：

```
1.  sudo
2.  rm / rm -rf
3.  git push
4.  发布 GitHub / arXiv / CSDN / npm / PyPI
5.  上传文件到外部
6.  读取 .env
7.  读取 token / 私钥 / 密钥
8.  覆盖 release 文件
9.  删除旧版本
10. 修改 shell 配置
11. 全局安装
12. 修改系统目录
```

### Notion 端危险表

必须停止并标记 NEED_UID_CONFIRM：

```
1.  修改 CONFIRM 码格式
2.  修改 SEAL 内容或顺序
3.  修改 GPG 指纹
4.  删除子页 / 删除数据库
5.  修改 P0 永恒页（指 L0 入口卡里列出的文件）
6.  修改主控页 v2.7 的 §0 不动点锚定 / §1 本页职责 / §10 反驯化口径 / §11 永久禁令
7.  修改老大画像
8.  把「龍」改成「龍」
9.  修改 IP-001 至 IP-N 的所有者字段
10. 跨应用全局覆写（多个页面同时 replace_content）
```

## 七、Cursor 提交信息模板

```
收口: [模块名] [本次完成内容]

DNA: #龍芯⚡️YYYY-MM-DD-[MODULE]-vX.X
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

Scope:
- 本次涉及文件
Changed:
- 本次完成内容
Verified:
- 本次验证方式
Risk:
- 是否涉及密钥 / 删除 / 发布 / sudo
Next:
- 下一步唯一动作，若已完成则写：STOP_ON_SUCCESS
```

## 八、桌面日志格式（Cursor 本地端）

每次自动收口追加写入：

```
~/Desktop/UID9622_DAILY_EXEC_LOGS/YYYY-MM-DD_closure_log.md
```

日志内容：

```
## UID9622_AUTO_CLOSURE
TS:
WORKDIR:
TASK:
FILES_CHANGED:
COMMANDS_RUN:
VERIFY_RESULT:
GIT_STATUS_BEFORE:
GIT_DIFF_STAT:
COMMIT_HASH:
RESULT:
DNA:
CONFIRM:
SEAL:
NEXT:
```

## 九、Notion 端收口日志格式（宝宝 专用）

宝宝 每次调用 Notion API 后输出：

```
## NOTION_AUTO_CLOSURE
TS:
OPERATION:        # create-pages / update-page / update-content / create-database
TARGET_PAGE_ID:
TARGET_PAGE_URL:
DNA_WRITTEN:
VERIFIED_BY:      # API 返回正常 page_id 且无错误
RISK_CHECK:       # 是否触及§6 Notion 端危险表
M_ACCEPTANCE:     # M:: 验收是否补齐
CNSH_SIGNATURE:   # CNSH:: 路由签章是否补齐
NEXT:             # STOP_ON_SUCCESS / 下一个需同步的页面
```

## 十、回执格式三种

### 10.1 SUCCESS_RECEIPT（两端通用）

```
SUCCESS_RECEIPT
- objective:
- files_changed | target_pages:
- verified_by:
- commit_hash | dna_written:
- log_path:
- risk:
- next: STOP_ON_SUCCESS
```

### 10.2 FAILED_RECEIPT

```
FAILED_RECEIPT
- objective:
- failed_step:
- exit_code | api_error:
- error_type:        # PATH_ERROR | MISSING_DEPENDENCY | TEST_FAIL
                     # | GIT_FAIL | PERMISSION_BLOCK | SECRET_RISK | API_TIMEOUT | UNKNOWN
- stderr_summary:
- attempted_paths:
- next_fix_command:
- log_path:
```

### 10.3 BLOCKED_RECEIPT

```
BLOCKED_RECEIPT
- objective:
- blocked_reason:
- risky_item:
- required_uid_confirm: true
- log_path:
```

## 十一、硬规则（十二条）

```
1.  未真实执行，不得说已完成。
2.  未验证，不得说通过。
3.  未 commit / 未返回 page_id，不得说已提交。
4.  未拿到 commit hash / Notion url，不得说收口成功。
5.  未写日志，不得说闭环完成。
6.  成功后必须停止。不主动建议新功能。
7.  失败后必须换路。不重复同一条失败路径。
8.  全失败必须复查（pwd / ls / git status / which / 权限 / 依赖）。
9.  危险操作必须等 UID9622 明确确认。
10. 不得使用 "也许 / 可能 / 应该 / 或许 / 大概 / 看起来" 糊弄。
11. 未发送回执，不算收口。
12. 输出回执后不重说。
```

## 十二、一句话定盘

```
UID9622 自动收口 =
  完成即检查
→ 查状态
→ 查 diff
→ 查风险
→ 跑验证
→ commit / 同步 Notion
→ 写日志
→ 给回执
→ 成功即停。
```

## 十三、配套脚本（Cursor 本地）

脚本路径：

```
~/longhun-system/tools/uid9622_auto_closure.sh
```

使用方式：

```bash
chmod +x tools/uid9622_auto_closure.sh
./tools/uid9622_auto_closure.sh "模块名" "本次完成内容"
```

完整脚本内容附在本页 §15 【完整脚本】。

## 十四、与现有协议的关系

| 阶段 | 适用协议 |
| --- | --- |
| AI 进系统 | 🛰️ AI 第一站协议（主控页顶部） |
| AI 跨窗口接棒 | 📦 上下文压缩与新窗口续航机制 v1.0 |
| **任务完成后收棍子** | **🔗 本协议（自动收口）** |

三个协议镜莱成闭环：**进门 → 接力 → 出门**。进门不迷路、接力不丢上下文、出门不交半成品。

## 十五、【完整脚本】tools/uid9622_auto_[closure.sh](http://closure.sh)

```bash
#!/usr/bin/env bash
# UID9622 自动收口脚本 v1.0
# DNA:#龍芯⚡️丙午·丙申·庚申·亥时-AUTO-CLOSURE-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -u

LOG_DIR="$HOME/Desktop/UID9622_DAILY_EXEC_LOGS"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/$(date '+%Y-%m-%d')_closure_log.md"
TS="$(date '+%Y-%m-%dT%H:%M:%S%z')"
MODULE="${1:-UID9622_AUTO_CLOSURE}"
MESSAGE="${2:-自动收口}"
DNA="#龍芯⚡️$(date '+%Y-%m-%d')-${MODULE}-v1.0"
CONFIRM="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL="#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

echo "UID9622 自动收口启动..."
echo "LOG: $LOG_FILE"

{
  echo ""; echo "---"; echo ""
  echo "## UID9622_AUTO_CLOSURE"
  echo ""
  echo "TS: $TS"
  echo "WORKDIR: $(pwd)"
  echo "MODULE: $MODULE"
  echo "MESSAGE: $MESSAGE"
  echo "DNA: $DNA"
  echo "CONFIRM: $CONFIRM"
  echo "SEAL: $SEAL"
  echo ""
} >> "$LOG_FILE"

# 1. 必须在 git 仓库
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  { echo "RESULT: BLOCKED"; echo "REASON: 当前目录不是 git 仓库"; echo "---"; } >> "$LOG_FILE"
  echo "BLOCKED_RECEIPT"
  echo "- blocked_reason: 当前目录不是 git 仓库"
  echo "- log_path: $LOG_FILE"
  exit 2
fi

# 2. 记录状态
STATUS="$(git status --short)"
DIFF_STAT="$(git diff --stat || true)"
{
  echo "GIT_STATUS_BEFORE:"; echo '\`\`\`text'; echo "$STATUS"; echo '\`\`\`'; echo ""
  echo "GIT_DIFF_STAT:"; echo '\`\`\`text'; echo "$DIFF_STAT"; echo '\`\`\`'; echo ""
} >> "$LOG_FILE"

# 3. 没有改动
if [ -z "$STATUS" ]; then
  { echo "RESULT: NO_CHANGE"; echo "NEXT: STOP_ON_NO_CHANGE"; echo "---"; } >> "$LOG_FILE"
  echo "SUCCESS_RECEIPT"
  echo "- objective: 自动收口"
  echo "- result: 当前无文件改动，无需 commit"
  echo "- log_path: $LOG_FILE"
  echo "- next: STOP_ON_NO_CHANGE"
  exit 0
fi

# 4. 危险文件检查
RISK_FILES="$(git status --short | grep -E '(\.env|token|secret|password|private|id_rsa|\.pem|\.key)' || true)"
if [ -n "$RISK_FILES" ]; then
  {
    echo "RESULT: BLOCKED"; echo "REASON: 检测到疑似敏感文件"
    echo "RISK_FILES:"; echo '\`\`\`text'; echo "$RISK_FILES"; echo '\`\`\`'; echo "---"
  } >> "$LOG_FILE"
  echo "BLOCKED_RECEIPT"
  echo "- blocked_reason: 检测到疑似敏感文件"
  echo "- risky_item:"; echo "$RISK_FILES"
  echo "- required_uid_confirm: true"
  echo "- log_path: $LOG_FILE"
  exit 3
fi

# 5. 最小验证
VERIFY_RESULT="manual structure check"; VERIFY_CODE=0
if find . -maxdepth 4 -name "*.py" | grep -q .; then
  PY_FILES="$(find . -maxdepth 4 -name "*.py" | tr '\n' ' ')"
  python3 -m py_compile $PY_FILES >/tmp/uid9622_pycompile.out 2>/tmp/uid9622_pycompile.err
  VERIFY_CODE=$?
  VERIFY_RESULT="python3 -m py_compile"
fi
{ echo "VERIFY_COMMAND: $VERIFY_RESULT"; echo "VERIFY_EXIT_CODE: $VERIFY_CODE"; } >> "$LOG_FILE"
if [ "$VERIFY_CODE" -ne 0 ]; then
  {
    echo "RESULT: FAILED"; echo "FAILED_STEP: VERIFY"
    echo "STDERR:"; echo '\`\`\`text'
    tail -n 80 /tmp/uid9622_pycompile.err 2>/dev/null || true
    echo '\`\`\`'; echo "---"
  } >> "$LOG_FILE"
  echo "FAILED_RECEIPT"
  echo "- failed_step: VERIFY"
  echo "- error_type: TEST_FAIL"
  echo "- next_fix_command: 查看 $LOG_FILE 中 VERIFY stderr"
  echo "- log_path: $LOG_FILE"
  exit 4
fi

# 6. git add + commit
git add .
COMMIT_MSG_FILE="$(mktemp)"
cat > "$COMMIT_MSG_FILE" <<EOF
收口: $MODULE $MESSAGE

DNA: $DNA
CONFIRM: $CONFIRM
SEAL: $SEAL

Scope:
- $(git diff --cached --name-only | tr '\n' ' ')
Changed:
- $MESSAGE
Verified:
- $VERIFY_RESULT
Risk:
- 未检测到 .env/token/private key/secret/password/*.pem/*.key
Next:
- STOP_ON_SUCCESS
EOF
git commit -F "$COMMIT_MSG_FILE" >/tmp/uid9622_commit.out 2>/tmp/uid9622_commit.err
COMMIT_CODE=$?
rm -f "$COMMIT_MSG_FILE"

if [ "$COMMIT_CODE" -ne 0 ]; then
  {
    echo "RESULT: FAILED"; echo "FAILED_STEP: GIT_COMMIT"
    echo "STDERR:"; echo '\`\`\`text'
    tail -n 80 /tmp/uid9622_commit.err
    echo '\`\`\`'; echo "---"
  } >> "$LOG_FILE"
  echo "FAILED_RECEIPT"
  echo "- failed_step: GIT_COMMIT"
  echo "- error_type: GIT_FAIL"
  echo "- stderr_summary:"
  tail -n 20 /tmp/uid9622_commit.err
  echo "- log_path: $LOG_FILE"
  exit 5
fi

COMMIT_HASH="$(git rev-parse --short HEAD)"
{ echo "RESULT: SUCCESS"; echo "COMMIT_HASH: $COMMIT_HASH"; echo "NEXT: STOP_ON_SUCCESS"; echo "---"; } >> "$LOG_FILE"
echo "SUCCESS_RECEIPT"
echo "- objective: 自动收口"
echo "- files_changed: $(git show --name-only --format='' HEAD | tr '\n' ' ')"
echo "- verified_by: $VERIFY_RESULT"
echo "- commit_hash: $COMMIT_HASH"
echo "- log_path: $LOG_FILE"
echo "- risk: 未检测到敏感文件"
echo "- next: STOP_ON_SUCCESS"
exit 0
```

## 十六、M:: 页面验收

```json
M:: {
  "id": "M::PROTOCOL-9622-20260507-AUTO-CLOSURE-V1.0",
  "type": "rule",
  "ts": "2026-05-07T17:00:00+08:00",
  "status": "configured",
  "refs": [
    "https://www.notion.so/2d87125a9c9f802889e2e18002f7cf4f"
  ],
  "payload": {
    "summary": "任务完成后自动收口协议 v1.0·双端适用：Cursor 本地 + Claude/宝宝 Notion 同步。",
    "result": {
      "local_endpoint": "configured",
      "notion_endpoint": "configured",
      "risk_table": "dual_endpoint",
      "receipt_format": "SUCCESS|FAILED|BLOCKED",
      "main_page_mode": "index_only",
      "version": "v1.0"
    }
  }
}
```

## 十七、CNSH:: 路由签章

```json
CNSH:: {
  "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-AUTO-CLOSURE-PROTOCOL-v1.0",
  "gate": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
  "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
  "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
  "route": "IPA-MAIN-CONTROL|AUTO-CLOSURE|CURSOR-LOCAL|NOTION-SYNC|RECEIPT-PROTOCOL|RISK-VETO",
  "audit": "🟢",
  "wuxing": "金",
  "layer": "L0永恒|L1百年",
  "policy": "pass"
}
```

---

## 摘要

（請在此用不超過 256 字說明本文檔的核心內容、性質與局限。）

## 關鍵詞

（請列出 5–10 個關鍵詞，中英文對照優先。）

## 引用與溯源

- 本文檔引用或參考了以下來源：
  - [1] （請填寫）
- 相關龍魂系統文檔：
  - 《龍魂文檔標準模板 v1.0》(#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 誠實局限

1. （請列出本分析的第一條局限或不確定性。）
2. （請列出第二條。）
3. （請列出第三條。）

## 修改記錄

| 日期 | 版本 | 修改人 | 修改內容 | 審核狀態 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文檔標準模板 v1.0》整理 | 草稿 |

## 分類標籤

- 總綱模塊：（請勾選，例如 #知識矩陣 #安全域）
- 對外狀態：（請勾選，例如 #Gitee #GitHub #CSDN）
- 審計色：#黃色待審

## DNA 簽名

```
#龍芯⚡️丙午·丙申·庚申·亥时-AUTO-CLOSURE-PROTOCOL-v1.0
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```


---

## 摘要

（请在此用不超过 256 字说明本文档的核心内容、性质与局限。）

## 关键词

（请列出 5–10 个关键词，中英文对照优先。）

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] （请填写）
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 诚实局限

1. （请列出本分析的第一条局限或不确定性。）
2. （请列出第二条。）
3. （请列出第三条。）

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-07-15 | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |

## 分类标签

- 总纲模块：（请勾选，例如 #知识矩阵 #安全域）
- 对外状态：（请勾选，例如 #Gitee #GitHub #CSDN）
- 审计色：#黄色待审

## DNA 签名

```
#龍芯⚡️丙午·丙申·庚申·亥时-AUTO-CLOSURE-PROTOCOL-v1.0`
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
