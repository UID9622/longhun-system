# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DeepSeek 对话 · 开源/不开源边界

**DNA**: `#龍芯⚡️20260701052429041924-DEEPSEEK-OPENSOURCE-BOUNDARY-8A356AA4`

## 核心原则

> 开源的是方法论和工具，不是生产环境；
> 打包出来给人用是善意，但不必把家门钥匙和日记本一起捐出去。

## 可开源部分

- CNSH 协议、龍魂治理框架、DNA 追溯机制
- LU 压缩/还原、集思广益、工具集生态的通用实现
- 评估技能、审计技能的逻辑模板
- 本地控制接口的通用命令解析与权限等级设计
- `龍智守_config.example.json` 配置模板

## 坚决不公开部分

| 类型 | 示例 |
|---|---|
| 私有密钥 | Webhook URL + Secret、API Token |
| 个人路径 | `~/Downloads`、`~/.longhun`、`~/.uid9622` |
| 授权名单 | `authorized_users.json`、创始人 OpenID |
| 真实数据 | 评估报告、本地日志、运行实例输出 |
| 环境指纹 | 设备名、用户名、内部 IP |

## 打包前的净化清单

```bash
# 1. 扫描硬编码飞书链接
grep -R "open.feishu.cn" .

# 2. 扫描示例中的占位符是否被误替换为真实值
grep -R "YOUR_FEISHU_WEBHOOK" .

# 3. 确认 ~/.longhun/config/ 等私有目录在 .gitignore 中
cat .gitignore | grep -E "longhun|uid9622|config"

# 4. 只提交 example 配置，不提交真实配置
git status --short | grep -E "config\.json|authorized_users|tokens\.json"
```

## 对外声明模板

> 本项目开源的是通用框架和工具集；实际运行所需的私有配置（密钥、路径、授权数据）需用户自行提供，恕不包含在仓库中。

## 给 Kimi 的指令

- 任何帮助用户“准备开源”的动作，先跑上述净化扫描。
- 若用户要求把含敏感值的文件加入 git，必须明确拒绝并说明边界。
- 在代码/文档中引用飞书配置时，统一使用 `@@channel.feishu.*` 变量，不得写入真实 URL/Secret。
