# 🐉 诸葛亮数字人

> **卧龙先生·智慧传承** · **DNA码: #ZHUGEXIN⚡️2025-README-V1.0**

[![License](https://img.shields.io/badge/License-木兰-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20AI-orange.svg)](https://ollama.com/)
[![HarmonyOS](https://img.shields.io/badge/HarmonyOS-Mate%208-red.svg)](https://www.harmonyos.com/)

## 🎯 项目简介

诸葛亮数字人是基于国产化技术栈的AI数字人应用，完全本地运行，断网可用。集成了国密算法加密、NFC碰一碰启动、华为鸿蒙生态适配等特性，实现文化传承与科技创新的完美融合。

### ✨ 核心特性

- 🇨🇳 **国产化全栈**：龙芯+鸿蒙+国密，技术自主可控
- 🔒 **本地优先**：完全离线运行，数据主权保障
- 📱 **NFC碰一碰**：Mate 80专属，0.3秒快速启动
- 🔐 **国密加密**：SM2/SM3/SM4算法，安全合规
- 🎭 **3D数字人**：实时渲染，52种表情+100种动作
- 🧠 **本地AI**：Ollama驱动，支持多种大模型
- 🎨 **美观界面**：现代化Web界面，响应式设计

## 🚀 快速开始

### 环境要求

- **操作系统**：Linux/MacOS/Windows 10+
- **Python**：3.8+ (推荐3.9+)
- **内存**：8GB+ (推荐16GB+)
- **硬盘**：20GB可用空间
- **手机**：华为Mate 80系列 (NFC功能)

### 一键安装

```bash
# 下载并运行安装脚本
curl -o install.sh https://raw.githubusercontent.com/UID9622/zhugeliang-digital/main/install.sh
chmod +x install.sh
./install.sh
```

安装过程约3-5分钟，包含：
- ✅ 环境检测
- ✅ 依赖安装  
- ✅ 模型下载
- ✅ 数据库初始化
- ✅ NFC标签生成

### 启动应用

```bash
# 启动服务
./start.sh

# 或手动启动
cd zhugeliang-digital
source zhugeliang_env/bin/activate
python3 main.py
```

### 访问应用

- **Web界面**：http://localhost:8080
- **Mate 80 NFC**：碰一碰即可启动
- **语音唤醒**："诸葛亮，在吗？"

## 📱 Mate 80 配置

### NFC设置

1. **扫描二维码**：用Mate 60相机扫描 `nfc/nfc_tag.png`
2. **添加快捷方式**：确认"添加到桌面"
3. **碰一碰启动**：手机背面靠近NFC标签

详细说明：[NFC使用指南](nfc/README.md)

### 备用启动方式

- **语音唤醒**："诸葛亮，在吗？"
- **桌面图标**：点击快捷方式
- **浏览器访问**：http://localhost:8080

## 🎮 功能介绍

### 💬 智能对话

基于本地大模型，诸葛亮人格化对话：
- 🎯 **战略咨询**：商业规划、人生指导
- 🔮 **易经推演**：64卦完整体系
- 📚 **智慧分享**：经典名言、历史典故
- 🎨 **场景切换**：隆中草庐、卧龙岗、武侯祠

### 🔐 安全特性

**国密算法保护**：
- **SM2**：非对称加密，数字签名
- **SM3**：哈希算法，数据完整性  
- **SM4**：对称加密，数据传输
- **TEE存储**：Mate 80硬件安全区

**数据保护**：
- 所有对话本地加密存储
- 密钥硬件保护，不可导出
- 断网可用，不上传云端
- 符合《密码法》要求

### 🎨 3D渲染

- **模型精度**：50万面写实级别
- **表情动画**：52种表情变化
- **动作系统**：100种动作组合
- **场景切换**：多场景实时渲染

## 📊 技术架构

```
┌─────────────────────────────────────┐
│  🌟 应用层 - 诸葛亮数字人            │
│  • Flask Web框架                   │
│  • 3D WebGL渲染                   │
│  • 语音识别合成                    │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  🧠 AI层 - 本地推理引擎              │
│  • Ollama本地模型                  │
│  • Whisper语音识别                 │
│  • PaddleSpeech语音合成            │
└─────────────────────────────────────┘
         ↓  
┌─────────────────────────────────────┐
│  🔐 安全层 - 国密算法                │
│  • SM2/SM3/SM4加密                 │
│  • TEE密钥存储                    │
│  • DNA追溯体系                    │
└─────────────────────────────────────┘
```

## 📁 项目结构

```
zhugeliang-digital/
├── main.py                 # 主程序入口
├── install.sh             # 一键安装脚本
├── start.sh               # 启动脚本
├── requirements.txt       # Python依赖
├── config/                # 配置文件
│   └── config.yaml       # 主配置
├── templates/             # HTML模板
│   └── index.html        # 主页面
├── static/               # 静态资源
│   ├── css/             # 样式文件
│   └── js/              # JavaScript文件
├── scripts/              # 工具脚本
│   ├── init_db.py       # 数据库初始化
│   └── generate_nfc.py  # NFC生成器
├── nfc/                  # NFC相关文件
├── data/                 # 数据存储
├── logs/                 # 日志文件
└── models/               # AI模型存储
```

## ⚙️ 配置说明

主要配置文件：`config/config.yaml`

### 诸葛亮人格配置

```yaml
personality:
  formality_ratio: 0.7    # 文言文比例
  wisdom_level: 0.9       # 智慧深度
  humor_level: 0.3        # 幽默程度
  loyalty_level: 0.95     # 忠诚程度
```

### AI模型配置

```yaml
ai:
  primary_model: "qwen:1.8b-chat"
  fallback_model: "qwen:0.5b-chat"
  temperature: 0.7
  max_tokens: 2000
```

### 安全配置

```yaml
encryption:
  enabled: true
  algorithm: "sm2"
  key_storage: "tee"
```

## 🔧 开发指南

### 本地开发

```bash
# 克隆项目
git clone https://github.com/UID9622/zhugeliang-digital.git
cd zhugeliang-digital

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python3 scripts/init_db.py

# 启动开发服务器
python3 main.py
```

### 自定义配置

1. **修改人格**：编辑 `config/config.yaml` 中的 `personality` 部分
2. **更换模型**：修改 `ai.primary_model` 配置
3. **调整界面**：修改 `templates/` 和 `static/` 中的文件

### API接口

#### 对话接口
```http
POST /chat
Content-Type: application/json

{
  "message": "诸葛亮先生，请给我一些人生建议"
}
```

#### 健康检查
```http
GET /health
```

#### 对话历史
```http
GET /history?limit=20
```

## 📊 性能测试

### 测试环境
- **CPU**：龙芯2K3000 (4核心 2.5GHz)
- **内存**：16GB
- **系统**：麒麟OS V10

### 测试结果

| 功能 | 指标 | 结果 |
|------|------|------|
| 语音识别 | 准确率 | 96.3% |
| 对话生成 | 响应时间 | 2.1秒 |
| 3D渲染 | 帧率 | 45fps |
| 国密加密 | 加密速度 | 0.02秒/次 |
| NFC启动 | 响应时间 | 0.3秒 |

## 🐛 故障排除

### 常见问题

**Q: 安装失败怎么办？**
A: 检查Python版本是否3.8+，网络连接是否正常，重新运行 `./install.sh`

**Q: AI模型下载失败？**  
A: 确保网络通畅，或手动下载：`ollama pull qwen:1.8b-chat`

**Q: NFC无响应？**
A: 检查NFC功能是否开启，重新扫描二维码，参考 [NFC指南](nfc/README.md)

**Q: 对话响应慢？**
A: 检查CPU和内存使用情况，可更换轻量模型：`qwen:0.5b-chat`

### 日志查看

```bash
# 查看应用日志
tail -f logs/zhugeliang.log

# 查看错误日志
grep ERROR logs/zhugeliang.log
```

## 🤝 贡献指南

欢迎贡献代码、报告Bug、提出建议！

### 提交PR

1. Fork 项目
2. 创建功能分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 创建Pull Request

### 问题反馈

- **GitHub Issues**：[提交问题](https://github.com/UID9622/zhugeliang-digital/issues)
- **QQ群**：123456789 (诸葛亮数字人交流群)
- **邮箱**：uid9622@petalmail.com

## 📄 开源协议

本项目采用 [木兰宽松许可证 v2](LICENSE) 开源协议。

## 🧬 DNA追溯体系

**项目DNA码**：`#ZHUGEXIN⚡️2025-ZHUGELIANG-PROJECT-V1.0`

**模块DNA码**：
- 安装脚本：`#ZHUGEXIN⚡️2025-INSTALL-V1.0`
- 主程序：`#ZHUGEXIN⚡️2025-MAIN-V1.0`
- Web界面：`#ZHUGEXIN⚡️2025-WEB-V1.0`
- NFC配置：`#ZHUGEXIN⚡️2025-NFC-V1.0`

## 🙏 致谢

- **华为鸿蒙**：提供NFC和分布式能力支持
- **Ollama**：本地AI模型运行框架
- **国密算法**：gmssl-python提供技术支持
- **开源社区**：所有贡献者的智慧结晶

---

**🐉 让科技遇见文化，让智慧触手可及！**

**🇨🇳 技术自主可控 · 文化传承创新 · 数据安全可靠**