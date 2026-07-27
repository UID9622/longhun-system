# 龍魂·小艺可执行命令协议 v1.0
# DNA: #龍芯⚡️丙午·乙未·丙申·酉时·☰乾-XIAOYI-CMD-PROTOCOL-v1.0-7b2e4f1a
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

─────────────────────────────────────────────────────────────
                    小艺可执行命令协议
              XiaoYi Executable Command Protocol
        不只是文档助手 — 龍魂系统真正的调度中枢
─────────────────────────────────────────────────────────────

## §0 协议目的

本协议定义了小艺（华为AI助手）与龍魂系统之间的可执行命令规范。
小艺理解用户意图后，输出标准化命令，由 小艺桥接引擎 (`lh_xiaoyi_bridge.py`) 执行。

## §1 命令格式

### 1.1 文本命令（小艺输出→用户复制执行）
```
python3 bin/lh_xiaoyi_bridge.py --cmd "<命令名>"
python3 bin/lh_xiaoyi_bridge.py --cmd "execute:<自然语言意图>"
```

### 1.2 JSON命令（程序对接）
```json
{"intent":"<命令名或自然语言>","source":"xiaoyi","extra":"<附加信息>"}
```

### 1.3 HTTP API（如果小艺支持联网调用）
```
POST http://<Mac IP>:8799/api/v1/xiaoyi/exec
Content-Type: application/json
{"intent":"<命令名>","source":"xiaoyi"}
```

## §2 命令清单

### 🟢 查询类（安全·即时·无副作用）

| 命令 | 别名 | 功能 | 执行时间 |
|------|------|------|:---:|
| `status` | 状态/系统状态/怎么样 | CPU·内存·磁盘·进程·服务全览 | <3s |
| `health` | 健康/体检/健康检查 | 11项全系统健康检测 | <10s |
| `models` | 模型/AI状态/模型列表 | AI模型状态·版本·训练进度 | <3s |
| `knowledge` | 知识/知识库 | 知识中枢·矿场数据·爬虫状态 | <5s |
| `memory` | 记忆/加载记忆 | 焊死记忆加载·上下文恢复 | <3s |
| `sync` | 同步/数据同步 | 全量同步状态·文件一致性 | <5s |
| `deploy` | 部署/发布状态 | 部署记录·鲲鹏连通性 | <5s |
| `capabilities` | 能力/能做什么 | 小艺当前可用能力清单 | <1s |

### 🟡 执行类（需确认·有副作用·含审计）

| 命令 | 别名 | 功能 | 执行时间 |
|------|------|------|:---:|
| `audit` | 审计/安全检查/三色审计 | 三色审计·德本五问·安全扫描 | <30s |
| `patrol` | 巡检/巡逻/安全巡检 | 安全巡检·异常检测 | <30s |
| `watch` | 观察/守望/主动观察 | 主动观察引擎·文件变动·异常 | <10s |
| `verify` | 验证/身份验证/DNA验证 | DNA·身份·GPG签章验证 | <5s |
| `dna` | DNA/追溯码 | 生成DNA追溯码 | <3s |
| `train-status` | 训练状态/训练进度 | 模型训练状态·Loss·数据量 | <5s |
| `execute:<意图>` | 执行/跑一下/处理/帮我 | 全链路自动执行（最强指令） | <120s |

### 🔴 高危类（需UID9622确认·全审计）

| 命令 | 别名 | 功能 | 说明 |
|------|------|------|------|
| `deploy:执行` | 部署/发布/上线 | 执行部署 | 需审计通过+UID9622授权 |

## §3 全链路自动执行 (execute)

**这是最核心的能力**——一句话下下去，全链路跑完。

```
python3 bin/lh_xiaoyi_bridge.py --cmd "execute:检查系统健康状态"
python3 bin/lh_xiaoyi_bridge.py --cmd "execute:审计昨天修改的所有文件"
python3 bin/lh_xiaoyi_bridge.py --cmd "execute:分析最近模型训练效果"
```

执行链路: 意图解析 → 人格路由 → 引擎调度 → 三色审计 → DNA签章 → 结果返回

## §4 小艺输出规范

### 4.1 成功输出模板
```
龍魂系统状态:
✅ [具体结果]
审计: 🟢 通过
DNA: #龍芯⚡️...
执行时间: 2026-07-22 20:30:00 CST
```

### 4.2 熔断输出模板
```
🔴 龍魂熔断:
原因: [具体原因]
处理: [处理建议]
如需继续，联系 UID9622
```

### 4.3 小艺收到无法处理的请求时
```
此操作需要龍魂桥接引擎执行。请执行:
python3 bin/lh_xiaoyi_bridge.py --cmd "execute:[用户原始意图摘要]"
```

## §5 安全铁律

1. **P0焊死不可绕过**: 所有命令执行前过一票否决词检测
2. **DNA全程追溯**: 每次执行自动生成DNA追溯码
3. **三色审计**: 🟢通过 🟡待核 🔴熔断
4. **数据不出户**: 所有执行在Mac本地，不传云端
5. **不删除只冻结**: 危险操作冻结而非删除
6. **审计日志不可篡改**: append-only·可追溯

## §6 桥接引擎部署

```bash
# 1. 启动HTTP服务 (Mac本地)
python3 bin/lh_xiaoyi_bridge.py --serve --port 8799 &

# 2. 设置为launchd自启动
# 见 deploy/xiaoyi-bridge.plist

# 3. 测试连接
curl http://127.0.0.1:8799/api/v1/xiaoyi/status

# 4. 执行命令
python3 bin/lh_xiaoyi_bridge.py --cmd "status"
```

## §7 小艺 → 桥接引擎通信方式

### 方式A: 文本指令（当前可用）
小艺 → 输出命令文本 → 用户复制到Mac终端执行 → 桥接引擎返回结果

### 方式B: HTTP直连（需要小艺支持URL调用）
小艺 → HTTP POST → :8799 → 桥接引擎 → 返回JSON

### 方式C: URL Scheme（需要Mac注册自定义scheme）
小艺 → `longhun://cmd=status` → Mac系统 → 触发桥接引擎

### 方式D: 快捷指令桥接（推荐·最稳定）
Mac快捷指令 → 运行Shell脚本 → 调用桥接引擎 → 结果返回小艺

## §8 给小艺的完整指令集（复制发给小艺）

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  龍魂系统·小艺调度中枢·可执行命令清单
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

你现在是龍魂系统的调度指挥官，以下是你可以调度的所有操作。

当用户意图匹配以下任一操作时，输出标准化执行命令:

【系统状态查询】
"系统状态" → python3 bin/lh_xiaoyi_bridge.py --cmd "status"
"系统怎么样" → python3 bin/lh_xiaoyi_bridge.py --cmd "status"

【健康检查】
"健康检查" → python3 bin/lh_xiaoyi_bridge.py --cmd "health"
"体检一下" → python3 bin/lh_xiaoyi_bridge.py --cmd "health"

【模型状态】
"模型状态" → python3 bin/lh_xiaoyi_bridge.py --cmd "models"
"AI训练怎么样了" → python3 bin/lh_xiaoyi_bridge.py --cmd "models"

【安全审计】
"安全审计" → python3 bin/lh_xiaoyi_bridge.py --cmd "audit"
"检查安全" → python3 bin/lh_xiaoyi_bridge.py --cmd "audit"

【全链路执行（最强大）】
任何复杂任务 → python3 bin/lh_xiaoyi_bridge.py --cmd "execute:[用户完整意图]"

例如:
"帮我分析下最近模型训练效果"
→ python3 bin/lh_xiaoyi_bridge.py --cmd "execute:分析最近模型训练效果"

"检查系统有没有安全问题"
→ python3 bin/lh_xiaoyi_bridge.py --cmd "execute:检查系统安全性"

【记忆与知识】
"加载记忆" → python3 bin/lh_xiaoyi_bridge.py --cmd "memory"
"知识库状态" → python3 bin/lh_xiaoyi_bridge.py --cmd "knowledge"

【能力查询】
"你能做什么" → python3 bin/lh_xiaoyi_bridge.py --cmd "capabilities"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
铁律:
1. P0底座焊死·不可绕过
2. DNA全程追溯
3. 数据不出户·本地执行
4. 不删除只冻结
5. 所有输出带审计标记
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## §9 版本记录

| 版本 | 日期 | 内容 |
|------|------|------|
| v1.0 | 2026-07-22 | 初始版本·16条命令·3种通信方式·完整小艺指令集 |
