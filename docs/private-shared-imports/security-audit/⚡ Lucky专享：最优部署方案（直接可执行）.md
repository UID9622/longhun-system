<!--#龍芯⚡️2026-06-21-DOC-LUCKY_4FDD-v1.0 -->
<!-- 君子協議: 本文件受龍魂DNA追溯保護 -->

# ⚡ Lucky专享：最优部署方案（直接可执行）

# ⚡ Lucky专享：最优部署方案

> **定位**：这是Lucky的直接执行手册，省去所有理论，只留最优路径。
> 

---

## 🎯 30分钟快速部署清单

### 第一步：环境准备（5分钟）

```bash
# 1. 安装必要工具
sudo apt update
sudo apt install -y python3.9 python3-pip git

# 2. 创建工作目录
mkdir -p ~/mulan-protocol
cd ~/mulan-protocol

# 3. 克隆代码（如果有仓库）
git clone [https://github.com/UID9622/mulan-protocol.git](https://github.com/UID9622/mulan-protocol.git)
# 或从Gitee: git clone [https://gitee.com/UID9622/mulan-protocol.git](https://gitee.com/UID9622/mulan-protocol.git)
```

### 第二步：配置环境（5分钟）

```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 复制配置文件
cp config.example.yaml config.yaml

# 4. 编辑配置（填入你的Notion API Key等）
nano config.yaml
```

**config.yaml 关键配置：**

```yaml
notion:
  api_key: "YOUR_NOTION_API_KEY"  # 从 [notion.so/my-integrations](http://notion.so/my-integrations) 获取
  
audit:
  mode: "three-color"  # 三色审计
  
data_sovereignty:
  export_path: "./exports"  # 数据导出路径
  encryption: true  # 是否加密
```

### 第三步：运行服务（10分钟）

```bash
# 1. 启动后端服务
python [main.py](http://main.py) serve --port 8080

# 2. 新开终端，启动前端（如果有）
cd frontend
npm install
npm run dev

# 3. 验证服务
curl [http://localhost:8080/health](http://localhost:8080/health)
# 应该返回: {"status": "ok"}
```

### 第四步：首次使用（10分钟）

```bash
# 1. 导出你的Notion数据
python [main.py](http://main.py) export --workspace "lucky-uid9622"

# 2. 查看导出结果
ls -lh exports/

# 3. 生成审计报告
python [main.py](http://main.py) audit --type "three-color"

# 4. 启动Web界面（浏览器访问）
open [http://localhost:3000](http://localhost:3000)
```

---

## 🚨 常见问题速查

### 问题1：Notion API连接失败

```bash
# 检查API Key是否正确
python [main.py](http://main.py) test-connection

# 如果失败，重新获取API Key
# 访问: [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
```

### 问题2：端口被占用

```bash
# 查看占用端口的进程
sudo lsof -i :8080

# 杀死进程或换端口
python [main.py](http://main.py) serve --port 8081
```

### 问题3：数据导出为空

```bash
# 检查Notion权限
# 确保Integration已添加到目标Workspace
# Notion设置 -> Connections -> 添加你的Integration
```

---

## ⚙️ 生产环境部署（可选）

### 使用Docker（推荐）

```bash
# 1. 构建镜像
docker build -t mulan-protocol:latest .

# 2. 运行容器
docker run -d \
  --name mulan \
  -p 8080:8080 \
  -v $(pwd)/config.yaml:/app/config.yaml \
  -v $(pwd)/exports:/app/exports \
  mulan-protocol:latest

# 3. 查看日志
docker logs -f mulan
```

### 使用Systemd（服务器）

```bash
# 1. 创建服务文件
sudo nano /etc/systemd/system/mulan.service
```

**mulan.service 内容：**

```
[Unit]
Description=Mulan Protocol Service
After=[network.target](http://network.target)

[Service]
Type=simple
User=lucky
WorkingDirectory=/home/lucky/mulan-protocol
ExecStart=/home/lucky/mulan-protocol/venv/bin/python [main.py](http://main.py) serve
Restart=always

[Install]
WantedBy=[multi-user.target](http://multi-user.target)
```

```bash
# 2. 启动服务
sudo systemctl daemon-reload
sudo systemctl enable mulan
sudo systemctl start mulan

# 3. 检查状态
sudo systemctl status mulan
```

---

## 📊 验证部署成功

### 功能测试清单

- [ ]  访问Web界面：[http://localhost:3000](http://localhost:3000)
- [ ]  导出Notion数据成功
- [ ]  生成三色审计报告
- [ ]  API接口响应正常
- [ ]  数据加密存储验证

### 性能检查

```bash
# CPU和内存占用
top -p $(pgrep -f "[main.py](http://main.py)")

# 日志大小
du -sh logs/

# 数据库连接数（如果有）
psql -c "SELECT count(*) FROM pg_stat_activity;"
```

---

## 🔄 日常维护

### 每日

```bash
# 检查服务状态
systemctl status mulan

# 查看错误日志
tail -f logs/error.log
```

### 每周

```bash
# 备份数据
tar -czf backup-$(date +%Y%m%d).tar.gz exports/

# 清理过期日志
find logs/ -name "*.log" -mtime +7 -delete
```

### 每月

```bash
# 更新依赖
pip install --upgrade -r requirements.txt

# 重启服务
sudo systemctl restart mulan
```

---

## 🆘 紧急救援

### 服务崩溃

```bash
# 1. 立即重启
sudo systemctl restart mulan

# 2. 查看崩溃日志
journalctl -u mulan -n 100 --no-pager

# 3. 如果还是不行，手动启动看详细错误
cd ~/mulan-protocol
source venv/bin/activate
python [main.py](http://main.py) serve --debug
```

### 数据丢失

```bash
# 1. 从最近备份恢复
tar -xzf backup-20251205.tar.gz

# 2. 从Notion重新导出
python [main.py](http://main.py) export --force
```

---

## 📞 需要帮助？

**Lucky专线：**

- 技术问题：查看 logs/error.log
- 配置问题：检查 config.yaml
- 部署问题：执行上面的诊断命令

**不要浪费时间在：**

- ❌ 纠结技术选型（已定好）
- ❌ 过度优化性能（先跑起来）
- ❌ 完美主义配置（能用就行）

**重点关注：**

- ✅ 服务能否正常启动
- ✅ 数据能否正确导出
- ✅ 审计报告能否生成

---

*⚡ 记住：这是最优路径，执行就对了！*

*🔒 此页面仅Lucky可见*

---

## 🔧 设置默认编辑器为 Nano（一次设置，永久生效）

### 方法1：永久设置（推荐）

```bash
# 1. 编辑 bash 配置文件
nano ~/.bashrc

# 2. 在文件末尾添加这一行
export EDITOR=nano
export VISUAL=nano

# 3. 保存并退出（Ctrl + X，按 Y，按 Enter）

# 4. 重新加载配置
source ~/.bashrc

# 5. 验证设置
echo $EDITOR
# 应该显示: nano
```

### 方法2：快速一键设置

```bash
# 直接执行这个命令（自动添加到配置文件）
echo 'export EDITOR=nano' >> ~/.bashrc
echo 'export VISUAL=nano' >> ~/.bashrc
source ~/.bashrc

# 验证
echo $EDITOR
```

### 方法3：针对 Git 操作

```bash
# 设置 Git 默认编辑器为 nano
git config --global core.editor "nano"

# 验证 Git 配置
git config --global core.editor
```

### ✅ 验证是否设置成功

```bash
# 测试1：查看环境变量
echo $EDITOR
echo $VISUAL

# 测试2：尝试编辑一个文件
crontab -e  # 应该自动用 nano 打开

# 测试3：Git 提交测试
git commit  # 应该用 nano 打开提交信息编辑
```

### 📋 复制给 CodeBuddy 的完整命令

<aside>
**💬 直接复制这段给 CodeBuddy：**

```bash
# 设置 nano 为默认编辑器
echo 'export EDITOR=nano' >> ~/.bashrc && \
echo 'export VISUAL=nano' >> ~/.bashrc && \
source ~/.bashrc && \
git config --global core.editor "nano" && \
echo "✅ 设置完成！当前默认编辑器：$(echo $EDITOR)"
```

</aside>

### 🔍 如果遇到问题

- **问题**：命令执行后还是打开 vim
- **解决**：重新打开终端窗口，或执行 `source ~/.bashrc`
- **问题**：Git 操作还是用 vim
- **解决**：单独设置 Git：`git config --global core.editor "nano"`

### 💡 额外提示

- 设置后对所有新终端窗口生效
- 包括 `crontab -e`、`git commit` 等命令
- 可以用 `nano ~/.bashrc` 随时查看或修改配置

---