> **P0焊死**: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
# 🐉 龍芯·鲲鹏自动AI调取 SOP v1.0

> **DNA**: `#龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-KUNPENG-AUTO-AI-SOP-v1.0-UID9622`  
> **SEAL**: `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`  
> **GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

---

## 1. 一句话目标

你在 Mac 本地发一句自然语言指令，鲲鹏服务器上的 21 人格集群自动执行，并把结果返回给你。

## 2. 前置条件

| 项 | 状态 | 检查命令 |
|:---|:---|:---|
| 鲲鹏 SSH 密钥 | `~/.ssh/longhun_kunpeng_ed25519` | `lh-kunpeng check` |
| 鲲鹏 IP | `119.13.90.27` | 已硬编码 |
| 本地项目根目录 | `~/longhun-system` | 自动识别 |
| 本地命令入口 | `lh-kunpeng` / `lh-start` | 已安装到 `~/.local/bin` |

## 3. 常用启动指令（记不住就用这个）

```bash
# 进入交互式控制台（33个模块菜单）
lh-start

# 查看鲲鹏共生体状态
lh-start --kunpeng

# 全系统状态面板
lh-start --status

# 执行完整开机自启动（谨慎）
lh-start --all
```

## 4. 鲲鹏自动AI调取指令

```bash
# 状态/自检/同步
lh-kunpeng status      # 鲲鹏在线/人格/任务
lh-kunpeng check       # 完整自检
lh-kunpeng sync        # 同步最新代码到鲲鹏

# 下发一句话任务
lh-kunpeng task "评估当前系统状态"
lh-kunpeng task "推演下季度战略方向" --persona 诸葛亮

# 演示调度
lh-kunpeng demo

# 自动巡检（每隔 N 秒下发一次系统巡检）
lh-kunpeng monitor 3600   # 每小时一次
```

## 5. 在 `lh` 控制台里操作

```bash
lh
# 选择菜单 → 🚀 鲲鹏共生体
# 1 状态 / 2 自检 / 3 同步 / 4 下发任务 / 5 演示 / 6 自动巡检
```

## 6. 等效底层命令

```bash
# 状态
cd ~/longhun-system && python3 08_BIN/lh_agent_kunpeng.py status

# 同步
cd ~/longhun-system && python3 08_BIN/lh_agent_kunpeng.py sync

# 下发任务
cd ~/longhun-system && python3 08_BIN/lh_agent_kunpeng.py --task "指令"
```

## 7. 自动AI调取落地方式

### 7.1 单次手动调取
`lh-kunpeng task "你的指令"`

### 7.2 周期自动巡检
`lh-kunpeng monitor 3600`  
保持终端不关闭即可周期性下发。需要后台持久化时，可配合 `screen`/`tmux` 或 systemd timer。

### 7.3 接入 launchd/systemd（进阶）
如需 Mac 开机即启动周期巡检，可创建 launchd plist 调用 `lh-kunpeng monitor 3600`。

## 8. 故障排查

| 现象 | 处理 |
|:---|:---|
| 鲲鹏离线 | `lh-kunpeng check` 看 SSH 是否通 |
| 引擎未就绪 | `lh-kunpeng sync` 重新同步 |
| 任务返回失败 | 检查指令是否含特殊引号，用 `"` 包裹 |
| lh-kunpeng 找不到 | 确认 `~/.local/bin` 在 PATH 中 |

## 9. 安全声明

- 鲲鹏端任务通过 SSH 下发，不经过第三方 API。
- 所有任务返回带 DNA 戳和审计色，可溯源。
- 自动巡检默认任务为中性系统巡检，不会执行写操作。

---

🐉丙午·丙申·丁巳·戌时·䷖剥·🟡
