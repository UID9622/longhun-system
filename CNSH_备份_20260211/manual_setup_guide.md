# 网络优化与API集成完整指南

## 🌐 当前网络状况分析

### 你的设备配置：
- **苹果电脑** (macOS) - 主工作设备
- **Mate60手机** - 热点设备  
- **华为随行WiFi** - 主要网络设备
- **柬埔寨流量卡** - 备用网络
- **智谱AI API** - ✅ 已连接终端
- **华为云账户** - ✅ 已充值
- **Notion AI** - 🔄 待连接
- **Obsidian + Ollama** - ✅ 本地运行
- **HELM永久许可证** - ✅ 已有

### 🎯 网络优化建议

#### 方案1: 华为设备优化连接 ⭐推荐
```
Mate60 → 华为随行WiFi → 苹果电脑
```

**优势：**
- 华为设备间有专属优化协议
- 信号更稳定，延迟更低
- 自动负载均衡和故障切换

**设置步骤：**
1. 确保Mate60连接华为随行WiFi（5GHz频段优先）
2. Mate60开启个人热点
3. 苹果电脑连接Mate60热点
4. 在系统偏好设置中设置网络优先级

#### 方案2: 双网冗余配置
```
主网络：华为随行WiFi（通过Mate60）
备网络：柬埔寨流量卡（直插电脑）
```

**优势：**
- 网络冗余保护，降低断网风险
- 自动故障切换
- 根据网络质量智能选择

## 🔧 API集成配置

### 1. Notion AI API 连接

#### 获取API密钥：
1. 登录 [Notion开发者页面](https://www.notion.so/my-integrations)
2. 点击"New Integration"
3. 填写基本信息：
   - Name: "Lucky Command Center"
   - Associated workspace: 选择你的工作区
   - Capabilities: 选择"Read content", "Update content", "Insert content"
4. 创建后复制"Internal Integration Token"

#### 配置步骤：
```bash
# 编辑环境变量文件
nano ~/.network_api_env

# 填入Notion API密钥
export NOTION_API_KEY="your_actual_notion_api_key_here"
export NOTION_BASE_URL="https://api.notion.com/v1"
export NOTION_VERSION="2022-06-28"

# 重新加载环境变量
source ~/.network_api_env
```

### 2. 华为云API配置

#### 服务推荐：
1. **ModelArts** - AI开发平台
   - 免费额度：每月100小时
   - 支持自然语言处理、图像识别等
   - 可与智谱AI形成互补

2. **对象存储OBS** - 云存储服务
   - 价格：¥0.12/GB/月
   - 免费额度：5GB存储
   - 适合数据备份和同步

#### 获取访问密钥：
1. 登录 [华为云控制台](https://console.huaweicloud.com)
2. 进入"统一身份认证 IAM"
3. 创建用户并授权
4. 获取Access Key ID和Secret Access Key

#### 配置命令：
```bash
# 华为云环境变量
export HUAWEI_AK="your_access_key_here"
export HUAWEI_SK="your_secret_key_here"
export HUAWEI_PROJECT_ID="your_project_id_here"
export HUAWEI_REGION="cn-north-4"
```

## 📱 具体操作步骤

### 步骤1: 网络连接优化

1. **连接华为随行WiFi到Mate60**
   - 在Mate60设置中搜索华为随行WiFi
   - 选择5GHz频段（信号更好）
   - 输入WiFi密码

2. **Mate60开启热点**
   - 设置 → 个人热点 → 开启
   - 设置热点密码（建议复杂密码）
   - 选择"WPA2个人"加密

3. **苹果电脑连接Mate60热点**
   - 点击WiFi图标选择Mate60热点
   - 输入密码连接
   - 在系统偏好设置中设置网络优先级

### 步骤2: API密钥配置

1. **获取并配置Notion API**
   ```bash
   # 测试Notion连接
   curl -H "Authorization: Bearer YOUR_NOTION_TOKEN" \
        -H "Notion-Version: 2022-06-28" \
        https://api.notion.com/v1/users/me
   ```

2. **配置华为云服务**
   ```bash
   # 测试华为云连接
   pip install huaweicloudsdkcore
   pip install huaweicloudsdkmodelarts
   ```

### 步骤3: 依赖包安装

```bash
# 更新pip
pip3 install --upgrade pip

# 安装核心依赖
pip3 install requests beautifulsoup4 pandas matplotlib
pip3 install notion-client zhipuai python-dotenv
pip3 install streamlit plotly dash networkx

# 验证安装
python3 -c "import requests, notion; print('✅ 核心依赖安装成功')"
```

## 🧪 测试验证

### API连接测试
```python
# 创建测试脚本 test_connections.py
import os
import requests
from pathlib import Path

# 加载环境变量
env_file = Path.home() / ".network_api_env"
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key.strip('"')] = value.strip('"')

def test_notion():
    """测试Notion API"""
    token = os.getenv("NOTION_API_KEY")
    if token and token != "your_notion_api_key_here":
        headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28"
        }
        response = requests.get("https://api.notion.com/v1/users/me", headers=headers)
        return response.status_code == 200
    return False

def test_ollama():
    """测试Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

# 运行测试
print("🧪 API连接测试")
print(f"Notion AI: {'✅' if test_notion() else '❌'}")
print(f"Ollama: {'✅' if test_ollama() else '❌'}")
```

### 网络性能测试
```bash
# 测试网络延迟和速度
ping -c 5 8.8.8.8
speedtest-cli  # 如果安装了speedtest

# 测试华为随行WiFi连接质量
ping -c 5 192.168.8.1  # 华为随行WiFi默认地址
```

## 🚀 快速启动脚本

创建一键启动脚本：
```bash
# 文件名: quick_start.sh
#!/bin/bash
echo "🚀 Lucky Command Center 快速启动"
echo "================================="

# 加载环境变量
source ~/.network_api_env

# 测试网络连接
echo "📡 测试网络连接..."
ping -c 3 google.com > /dev/null 2>&1
echo "外网连接: $([ $? -eq 0 ] && echo '✅' || echo '❌')"

# 测试API连接
echo "🧪 测试API连接..."
python3 test_connections.py

echo ""
echo "📱 网络状态检查:"
echo "• Mate60热点: $(networksetup -getairportnetwork en0 | awk -F': ' '{print $2}')"
echo "• 华为随行WiFi: $(ping -c 1 192.168.8.1 > /dev/null 2>&1 && echo '✅连接' || echo '❌断开')"

echo "✅ 系统就绪!"
```

## 📊 性能监控建议

### 网络监控
```bash
# 持续监控网络状态
watch -n 60 "ping -c 3 google.com && echo '网络正常'"
```

### API使用监控
- Notion API: 请求限制每秒3次
- 智谱AI: 根据套餐不同有限额
- 华为云: 按实际使用量计费

## 🎯 预期效果

配置完成后你将获得：
- **稳定的网络连接**：华为设备优化 + 双网冗余
- **完整的API集成**：Notion + 智谱 + 华为云 + Ollama
- **智能工作流**：本地AI + 云端AI互补
- **高效协作**：Obsidian + Notion + 各大AI服务

## 🛠️ 故障排除

### 网络问题
1. 重启所有设备
2. 检查信号强度
3. 尝试切换备用网络
4. 重置网络设置

### API问题
1. 检查API密钥有效性
2. 验证网络连接
3. 查看防火墙设置
4. 检查API使用配额

### 依赖问题
1. 更新pip到最新版本
2. 检查Python版本兼容性
3. 清理pip缓存：`pip cache purge`
4. 使用虚拟环境隔离依赖

---

**🎯 下一步行动清单：**

1. ✅ 环境变量文件已创建：`~/.network_api_env`
2. 🔄 获取Notion API密钥并填入配置文件
3. 🔄 配置华为云访问密钥
4. 🔄 优化网络连接：Mate60 → 华为随行WiFi → 苹果电脑
5. 🔄 运行测试脚本验证配置
6. 🔄 根据需要安装额外依赖包

**📞 如需帮助，请随时询问具体步骤的详细指导！**