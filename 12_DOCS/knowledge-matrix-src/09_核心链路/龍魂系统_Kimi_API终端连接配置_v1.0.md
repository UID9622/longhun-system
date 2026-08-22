# 龍魂系统 Kimi API终端连接配置 v1.0

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技术文档 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-DOC-_KIMI_API_V1-0_1ECD-v1.0`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

<!--#龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-DOC-_KIMI_API_V1-0_1ECD-v1.0 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

╔══════════════════════════════════════════════════════════════════════════════╗
║           龍魂系统 · Kimi API 终端连接配置 v1.0                               ║
║           加工厂（Mac）直连 Kimi API                                        ║
║           DNA: #UID9622⚡️2026-06-13-KIMI-API-TERMINAL-v1.0                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
【API 配置】
Base URL: https://api.moonshot.cn/v1
API Key: [REDACTED_API_KEY_1]
模型: kimi-latest (或 kimi-k2-6, kimi-moonshot-v1-32k 等)
环境变量配置（Mac ~/.zshrc）:
─────────────────────────────
export KIMI_API_KEY="[REDACTED_API_KEY_1]"
export KIMI_BASE_URL="https://api.moonshot.cn/v1"
安全要求:
─────────
· API Key 仅存储于 Mac 本地环境变量，禁止写入代码/日志
· 加工完成后立即清除内存中的 API Key 缓存
· 大本营（华为手机）不持有 API Key，仅审批任务类型
═══════════════════════════════════════════════════════════════════════════════
【步骤一】测试连接（Mac终端直接执行）
═══════════════════════════════════════════════════════════════════════════════
$ curl -s -X POST https://api.moonshot.cn/v1/chat/completions     -H "Authorization: Bearer [REDACTED_API_KEY_1]"     -H "Content-Type: application/json"     -d '{
"model": "kimi-latest",
"messages": [
{"role": "system", "content": "你是龍魂系统加工厂AI，执行UID9622授权任务。"},
{"role": "user", "content": "测试连接，回复DNA签名格式。"}
],
"temperature": 0.3
}'
预期响应:
─────────
{
"id": "chatcmpl-xxx",
"object": "chat.completion",
"created": 1718000000,
"model": "kimi-latest",
"choices": [{
"index": 0,
"message": {
"role": "assistant",
"content": "#UID9622⚡️2026-06-13-TEST-CONNECT-v1.0\n连接正常，加工厂AI就绪。"
},
"finish_reason": "stop"
}]
}
═══════════════════════════════════════════════════════════════════════════════
【步骤二】Kimi CLI 完整脚本（Mac终端）
═══════════════════════════════════════════════════════════════════════════════
mkdir−p /longhun/factory/bin
 
 cd ~/longhun/factory/bin
$ cat > kimi-cli <<'CLIEOF'
#!/bin/bash
龍魂系统 · Kimi CLI 加工厂专用版
直连 Kimi API，所有任务需大本营审批
set -e
── 配置 ──
KIMI_API_KEY="[REDACTED_API_KEY_1]"
KIMI_BASE_URL="${KIMI_BASE_URL:-https://api.moonshot.cn/v1}"
CAMP_IP="${CAMP_IP:-192.168.1.100}"
SUB_KEY_FILE="${SUB_KEY_FILE:-~/longhun/factory/.sub_key}"
FACTORY_ID="${LONGHUN_FACTORY_ID:-FACT-01}"
── 颜色 ──
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'
── 函数 ──
function log_error() { echo -e "${RED}[FACTORY] 🔴 $1 ${NC}" >&2; }
function log_info() { echo -e "${GREEN}[FACTORY] 🟢 $1 ${NC}"; }
function log_warn() { echo -e "${YELLOW}[FACTORY] 🟡 $1 ${NC}"; }
function check_camp_auth() {
local task_type="$1"
local prompt_hash="$2"
plain
  if [ ! -f "${SUB_KEY_FILE}" ]; then
      log_error "子密钥缺失，向大本营申请..."
      curl -s -X POST "http://${CAMP_IP}:9622/api/factory/request_key"               -H "Content-Type: application/json"               -d "{"factory_id": "${FACTORY_ID}", "serial": "KVQQ7KLF76"}"
      log_warn "请在大本营（华为手机）审批子密钥申请"
      exit 1
  fi

  local SUB_KEY=$(cat "${SUB_KEY_FILE}")

  # 向大本营申请任务授权
  local auth_response=$(curl -s -X POST           "http://${CAMP_IP}:9622/api/factory/apply"           -H "Authorization: Bearer ${SUB_KEY}"           -H "Content-Type: application/json"           -d "{
          "task_type": "${task_type}",
          "prompt_hash": "${prompt_hash}",
          "factory_id": "${FACTORY_ID}"
      }")

  local action_token=$(echo "${auth_response}" | jq -r '.action_token // empty')
  local status=$(echo "${auth_response}" | jq -r '.status // "unknown"')

  if [ -z "${action_token}" ] || [ "${action_token}" == "null" ]; then
      log_error "大本营未授权，任务阻断"
      log_error "原因: $(echo "${auth_response}" | jq -r '.reason // "unknown"')"
      exit 1
  fi

  log_info "大本营授权通过，action_token: ${action_token:0:8}..."
  echo "${action_token}"
}
function kimi_api_call() {
local prompt="$1"
local system_prompt="$2"
plain
  local response=$(curl -s -X POST           "${KIMI_BASE_URL}/chat/completions"           -H "Authorization: Bearer ${KIMI_API_KEY}"           -H "Content-Type: application/json"           -d "{
          "model": "kimi-latest",
          "messages": [
              {"role": "system", "content": "${system_prompt}"},
              {"role": "user", "content": "${prompt}"}
          ],
          "temperature": 0.3,
          "max_tokens": 8192
      }")

  # 检查API错误
  local error_msg=$(echo "${response}" | jq -r '.error.message // empty')
  if [ -n "${error_msg}" ] && [ "${error_msg}" != "null" ]; then
      log_error "Kimi API 错误: ${error_msg}"
      exit 1
  fi

  echo "${response}" | jq -r '.choices[0].message.content'
}
function save_result() {
local content="$1"
local task_type="$2"
local timestamp=$(date +%Y%m%d_%H%M%S)
local filename="${task_type}_${timestamp}.md"
local filepath="~/longhun/factory/output/${filename}"
plain
  mkdir -p ~/longhun/factory/output
  echo "${content}" > "${filepath}"
  log_info "结果已保存: ${filepath}"
  echo "${filepath}"
}
── 主命令 ──
CMD="$1"
shift
case "${CMD}" in
      "task")
          # 通用任务
          local prompt="$*"
          local prompt_hash=$(echo -n "${prompt}" | sha256sum | cut -d' ' -f1)
plain
      log_info "任务类型: 通用"
      log_info "prompt_hash: ${prompt_hash:0:16}..."

      check_camp_auth "general" "${prompt_hash}"
      local result=$(kimi_api_call "${prompt}" "你是龍魂系统加工厂AI，执行UID9622授权任务。回答简洁、结构化、可执行。")

      echo "${result}"
      save_result "${result}" "task"
      ;;

  "matrix")
      # 矩阵生成任务
      local prompt="$*"
      local prompt_hash=$(echo -n "${prompt}" | sha256sum | cut -d' ' -f1)

      log_info "任务类型: 矩阵生成"
      log_info "prompt_hash: ${prompt_hash:0:16}..."

      check_camp_auth "matrix_generation" "${prompt_hash}"
      local result=$(kimi_api_call "${prompt}" "你是龍魂系统加工厂AI，专精接口契约矩阵生成。输出必须包含：模块定义、输入输出口、校验规则、失败策略、接口契约、DNA签名。格式严格结构化。")

      echo "${result}"
      save_result "${result}" "matrix"
      ;;

  "publish")
      # 仓库发布任务
      local prompt="$*"
      local prompt_hash=$(echo -n "${prompt}" | sha256sum | cut -d' ' -f1)

      log_info "任务类型: 仓库发布"
      log_info "prompt_hash: ${prompt_hash:0:16}..."

      check_camp_auth "repository_publish" "${prompt_hash}"
      local result=$(kimi_api_call "${prompt}" "你是龍魂系统加工厂AI，执行仓库发布任务。生成发布说明、版本更新日志、DNA签名。回答必须包含可直接执行的git命令。")

      echo "${result}"
      save_result "${result}" "publish"

      # 提交发布申请
      local SUB_KEY=$(cat "${SUB_KEY_FILE}" 2>/dev/null || echo "")
      local apply_response=$(curl -s -X POST               "http://${CAMP_IP}:9622/api/factory/apply"               -H "Authorization: Bearer ${SUB_KEY}"               -H "Content-Type: application/json"               -d "{
              "type": "publish",
              "target": "gitee",
              "files": ["$(ls ~/longhun/factory/output/*.md 2>/dev/null | head -1 | sed 's|/Users/[^/]*|~|')"],
              "justification": "Kimi任务执行结果，申请发布",
              "urgency": "normal"
          }")

      log_info "发布申请已提交: $(echo "${apply_response}" | jq -r '.status // "unknown"')"
      ;;

  "status")
      # 检查大本营状态
      log_info "检查大本营状态..."
      curl -s "http://${CAMP_IP}:9622/api/factory/status" | jq .
      ;;

  "test")
      # 测试API连接
      log_info "测试Kimi API连接..."
      local test_response=$(curl -s -X POST               "${KIMI_BASE_URL}/chat/completions"               -H "Authorization: Bearer ${KIMI_API_KEY}"               -H "Content-Type: application/json"               -d '{
              "model": "kimi-latest",
              "messages": [
                  {"role": "system", "content": "你是龍魂系统加工厂AI。"},
                  {"role": "user", "content": "回复DNA签名格式：#UID9622⚡️YYYYMMDD-TEST-CONNECT-v1.0"}
              ],
              "temperature": 0.3
          }')

      local test_content=$(echo "${test_response}" | jq -r '.choices[0].message.content // empty')
      if [ -n "${test_content}" ]; then
          log_info "API连接正常"
          echo "${test_content}"
      else
          log_error "API连接失败"
          echo "${test_response}" | jq .
          exit 1
      fi
      ;;

  *)
      echo "龍魂系统 · Kimi CLI 加工厂专用版"
      echo ""
      echo "用法: kimi-cli [command] [args...]"
      echo ""
      echo "命令:"
      echo "  task    <prompt>     通用任务执行（需大本营审批）"
      echo "  matrix  <prompt>     矩阵生成任务（需大本营审批）"
      echo "  publish <prompt>     仓库发布任务（需大本营审批）"
      echo "  status               检查大本营状态"
      echo "  test                 测试API连接"
      echo ""
      echo "环境变量:"
      echo "  KIMI_API_KEY         Kimi API密钥"
      echo "  CAMP_IP              大本营IP地址"
      echo "  SUB_KEY_FILE         子密钥文件路径"
      echo "  LONGHUN_FACTORY_ID   加工厂ID"
      echo ""
      echo "示例:"
      echo '  kimi-cli task "生成安全域接口契约矩阵"'
      echo '  kimi-cli matrix "MOD-SEC-01 身份鉴别模块"'
      echo '  kimi-cli publish "发布v4.2.0版本"'
      exit 1
      ;;
esac
CLIEOF
chmod+xkimi−cli
 
 sudo ln -s ~/longhun/factory/bin/kimi-cli /usr/local/bin/kimi-cli 2>/dev/null || true
═══════════════════════════════════════════════════════════════════════════════
【步骤三】快捷别名配置（Mac ~/.zshrc）
═══════════════════════════════════════════════════════════════════════════════
$ cat >> ~/.zshrc <<'ZSHRC'
龍魂系统 · 加工厂快捷命令
alias lh-task='kimi-cli task'
alias lh-matrix='kimi-cli matrix'
alias lh-publish='kimi-cli publish'
alias lh-status='kimi-cli status'
alias lh-test='kimi-cli test'
alias lh-camp='curl -s http://${CAMP_IP}:9622/api/factory/status | jq .'
五维人格矩阵快捷调用
alias lh-mil='kimi-cli task "[军事思维] "'
alias lh-his='kimi-cli task "[历史思维] "'
alias lh-phi='kimi-cli task "[哲学思维] "'
alias lh-eco='kimi-cli task "[经济思维] "'
alias lh-pol='kimi-cli task "[政治思维] "'
环境变量
export KIMI_API_KEY="[REDACTED_API_KEY_1]"
export KIMI_BASE_URL="https://api.moonshot.cn/v1"
export CAMP_IP="192.168.1.100"  # 修改为实际华为手机IP
export SUB_KEY_FILE="~/longhun/factory/.sub_key"
export LONGHUN_FACTORY_ID="FACT-01"
ZSHRC
$ source ~/.zshrc
═══════════════════════════════════════════════════════════════════════════════
【步骤四】验证测试（Mac终端）
═══════════════════════════════════════════════════════════════════════════════
测试1: API连接
───────────
$ lh-test
预期输出:
[FACTORY] 🟢 API连接正常
#UID9622⚡️2026-06-13-TEST-CONNECT-v1.0
测试2: 大本营状态
───────────────
$ lh-status
预期输出:
[FACTORY] 🟢 检查大本营状态...
{
"camp_status": "online",
"gate_state": "OPEN",
"battery": 85,
"factory_connected": true,
"sub_key_valid": true
}
测试3: 通用任务（需大本营审批）
──────────────────────────────
$ lh-task "生成MOD-SEC-01身份鉴别模块的接口契约"
预期输出:
[FACTORY] 🟢 任务类型: 通用
[FACTORY] 🟢 prompt_hash: a1b2c3d4...
[FACTORY] 🟢 大本营授权通过，action_token: xxxxxxxx...
[矩阵内容...]
[FACTORY] 🟢 结果已保存: ~/longhun/factory/output/task_20260613_111400.md
测试4: 矩阵生成（需大本营审批）
──────────────────────────────
$ lh-matrix "安全域 MOD-SEC-01 身份鉴别与访问控制"
预期输出:
[FACTORY] 🟢 任务类型: 矩阵生成
[FACTORY] 🟢 prompt_hash: e5f6g7h8...
[FACTORY] 🟢 大本营授权通过，action_token: yyyyyyyy...
[结构化矩阵内容...]
[FACTORY] 🟢 结果已保存: ~/longhun/factory/output/matrix_20260613_111400.md
测试5: 仓库发布（需大本营审批）
──────────────────────────────
$ lh-publish "发布v4.2.0版本，包含安全域矩阵"
预期输出:
[FACTORY] 🟢 任务类型: 仓库发布
[FACTORY] 🟢 prompt_hash: i9j0k1l2...
[FACTORY] 🟢 大本营授权通过，action_token: zzzzzzzz...
[发布说明内容...]
[FACTORY] 🟢 发布申请已提交: pending
═══════════════════════════════════════════════════════════════════════════════
【DNA签名】
═══════════════════════════════════════════════════════════════════════════════
#UID9622⚡️2026-06-13-KIMI-API-TERMINAL-v1.0
API: [REDACTED_API_KEY_1]
Base: https://api.moonshot.cn/v1
Model: kimi-latest
加工厂: FACT-01_KVQQ7KLF76
大本营: 华为手机
确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

═══════════════════════════════════════════════════════════════════════════════
【安全提示】
═══════════════════════════════════════════════════════════════════════════════
本文件中的 Kimi API Key 已被脱敏处理（替换为 [REDACTED_API_KEY_1]），
原因：仓库为开源/多设备同步场景，不宜硬编码真实密钥。
请按以下方式之一配置真实密钥：
1. Mac ~/.zshrc 中写入 export KIMI_API_KEY="sk-..."
2. 或 Mac 密钥链：security add-generic-password -s "kimi-api" -a "UID9622" -w "sk-..."
3. 大本营（华为手机）不持有 API Key，仅审批任务类型与目标
若需更新密钥，修改本地环境变量即可，无需再次提交本文件。


---

## 摘要

（请在此用不超过 256 字说明本文档的核心内容、性质与局限。）

## 关键词

（请列出 5–10 个关键词，中英文对照优先。）

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] （请填写）
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 诚实局限

1. （请列出本分析的第一条局限或不确定性。）
2. （请列出第二条。）
3. （请列出第三条。）

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |

## 分类标签

- 总纲模块：（请勾选，例如 #知识矩阵 #安全域）
- 对外状态：（请勾选，例如 #Gitee #GitHub #CSDN）
- 审计色：#黄色待审

## DNA 签名

```
#龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-DOC-_KIMI_API_V1-0_1ECD-v1.0
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
