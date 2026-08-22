# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂公众号智能内容中枢

## 功能定位

将龍魂系统的内容生产能力与微信公众号官方 API 打通，实现：

- 文章一键发布 / 草稿管理 / 素材管理
- AI 配图生成
- AI 语音朗读（TTS / Soul 情感语音）
- 多人格自动路由：不同内容由不同龍魂人格撰写/审核/发布
- Web 操作台 + 命令行双入口

## 目录结构

```
wechat_public_account/
├── config/              # 配置管理
├── core/                # 微信 API 核心封装
├── services/            # AI 配图、语音、人格服务
├── personas/            # 人格定义
├── static/              # Web 静态资源
├── templates/           # Web 模板
├── cli.py               # 命令行入口
├── web_ui.py            # Web 操作台入口
├── requirements.txt
└── README.md
```

## 配置方式

### 1. 环境变量（推荐）

```bash
export WECHAT_APPID="你的公众号 appid"
export WECHAT_APPSECRET="你的公众号 appsecret"
export WECHAT_TOKEN="你的服务器配置 Token（可选）"
export WECHAT_ENCODING_AES_KEY="消息加解密密钥（可选）"
export KIMI_API_KEY="Kimi API Key（用于 AI 生成）"
export DEEPSEEK_API_KEY="DeepSeek API Key（可选）"
```

### 2. 配置文件

方式一：交互式配置（推荐）

```bash
python3 setup_credentials.py
```

方式二：手动复制

```bash
cp config/.env.example .env
# 编辑 .env 填入真实信息
```

## 快速开始

### 安装依赖

```bash
cd ~/longhun-system/integrations/wechat_public_account
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 命令行使用

```bash
# 查看帮助
python cli.py --help

# 发布一篇文章
python cli.py article publish --title "根性治理论" --file ~/longhun-system/01_protocols/THESIS-ROOT-GOVERNANCE/FULL-THESIS.md

# 生成配图
python cli.py image generate --prompt "中国基层治理 三才三色" --output cover.png

# 生成语音
python cli.py voice generate --text "为人民服务不是可怜人" --output voice.mp3 --style educator

# 列出人格
python cli.py persona list

# 用人格写文章
python cli.py persona run --persona 龍芯侦察兵 --task "写一段关于评分恐怖主义的短文"
```

### Web 操作台

```bash
python web_ui.py
# 打开 http://localhost:8443
```

## 人格系统

人格定义在 `personas/personas.json` 中。默认人格包括：

- 龍芯侦察兵：外部情报、趋势洞察
- 龍芯上帝之眼：安全守护、全局监控
- 龍魂宝宝：系统构建、温和表达
- 雯雯：技术整理、文档输出
- 文心：同步官、双语转换

可通过 Web UI 或编辑 JSON 文件增删人格。

## 与龍魂系统的联动

- 文章源：自动读取 `~/longhun-system/01_protocols/` 下的协议和论文
- 语音：调用 `~/.longhun/scripts/longhun_senses/senses_cli.py`
- DNA 追溯：每次发布自动生成 `#龍芯⚡️...` DNA 码

## 注意事项

- 公众号 AppID/AppSecret 是敏感信息，不要提交到公开仓库
- access_token 有有效期，系统会自动缓存和刷新
- 发布前建议先用 `--draft` 生成草稿预览

---

**DNA**：`#龍芯⚡️丙午·甲午·庚午·壬午·䷳艮为山-LONGHUN-WECHAT-PUBLIC-ACCOUNT-INTEGRATION-v1.0`
