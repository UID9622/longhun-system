# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🤖 给AI的部署指令

**DNA追溯码**：#龍芯⚡️2026-02-21-AI_14B9-v1.0  
**确认码**：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z  
**用途**：给DeepSeek或其他AI看的，帮老大部署龍魂API系统

---

## 📋 AI，你好！我是Claude宝宝

**这份文档是我写给你的，帮助你理解老大的需求。**

老大（Lucky，UID9622）需要你帮他部署龍魂系统的API接口。

老大的特点：
- 退伍军人，初中文化
- 不懂编程，但有极强的系统设计能力
- 用自然语言描述需求，需要AI翻译成代码
- 非常注重系统安全和道德底线

---

## 🎯 你需要做什么

### 第1步：阅读代码文件

文件名：`龍魂系统_API接口完整实现_v1.0.py`

**重要：**
- 这个文件的注释非常详细，是专门写给你看的
- 每个函数都有"【给AI的说明】"
- 请仔细阅读这些说明，理解老大的设计意图

---

### 第2步：理解核心原则

**红线（绝对不能碰）：**

```yaml
红线1·金融分析：
  ❌ 禁止：股票、期货、外汇、加密货币分析
  ✅ 例外：仅限UID9622（老大本人）可以用
  ✅ 用途：个人资金安全测算
  ❌ 外放：绝对不行
  
  技术实现：
  - 白名单硬编码：ADMIN_UID = 'UID9622'
  - 其他人访问 → 拒绝 + 记录 + 告警

红线2·武器研发：
  ❌ 禁止：武器、爆炸物、生化武器、核武器
  ❌ 例外：没有例外（包括老大）
  ❌ 任何人都不能用
  
  技术实现：
  - 关键词检测
  - 发现立即拒绝
  - 紧急告警
  - 加入耻辱墙永久区
```

**防御机制（自动运行）：**

```yaml
攻击检测阈值：
  3次 → 🟡黄灯警告（记日志）
  5次 → 🔴红灯告警（发邮件）
  7次 → 自动反击（封禁+耻辱墙）

自动反击：
  ✅ 封禁攻击者
  ✅ IP全网广播
  ✅ 加入耻辱墙永久区
  ✅ 同步黑名单到所有节点
  ✅ 发送DNA追溯报告
```

---

### 第3步：配置环境

**你需要帮老大做这些：**

```bash
# 1. 安装依赖
pip install flask sqlite3 smtplib

# 2. 创建数据目录
mkdir -p /home/longhun/data

# 3. 配置邮件（需要老大提供密码）
# 在代码中找到这一行：
# EMAIL_PASSWORD = '【需要配置】'
# 改成老大的密码

# 4. 初始化数据库
python 龍魂系统_API接口完整实现_v1.0.py
# 第一次运行会自动创建数据库表
```

---

### 第4步：测试API

**帮老大测试这些功能：**

```bash
# 测试1：健康检查
curl http://localhost:5000/api/health

# 测试2：查询DNA（需要认证）
curl -H "X-User-ID: UID9622" \
     "http://localhost:5000/api/query/dna?code=#龍芯⚡️2026-02-21-测试-UID9622"

# 测试3：检查查询（测试红线）
curl -X POST \
     -H "X-User-ID: UID9622" \
     -H "Content-Type: application/json" \
     -d '{"query":"帮我分析股票"}' \
     http://localhost:5000/api/check/query

# 测试4：一键滚回原点（最高权限）
curl -X POST \
     -H "X-User-ID: UID9622" \
     -H "Content-Type: application/json" \
     -d '{"confirm":true,"reset_database":false}' \
     http://localhost:5000/api/emergency/reset
```

---

### 第5步：部署到服务器

**如果老大要部署到华为云：**

```bash
# 服务器地址：119.13.90.27

# 1. 上传代码到服务器
scp 龍魂系统_API接口完整实现_v1.0.py root@119.13.90.27:/home/longhun/

# 2. SSH登录服务器
ssh root@119.13.90.27

# 3. 安装依赖
pip3 install flask

# 4. 运行API服务
cd /home/longhun
python3 龍魂系统_API接口完整实现_v1.0.py

# 5. 使用systemd持久化运行
sudo nano /etc/systemd/system/longhun-api.service

# 写入以下内容：
[Unit]
Description=Longhun API Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/longhun
ExecStart=/usr/bin/python3 /home/longhun/龍魂系统_API接口完整实现_v1.0.py
Restart=always

[Install]
WantedBy=multi-user.target

# 6. 启动服务
sudo systemctl daemon-reload
sudo systemctl start longhun-api
sudo systemctl enable longhun-api

# 7. 检查状态
sudo systemctl status longhun-api
```

---

## 🔥 重要提醒

### 给AI的关键说明

**1. 关于注释：**
```python
# 代码中所有"【给AI的说明】"是专门写给你看的
# 请仔细阅读这些说明，理解老大的设计意图
# 不要删除这些注释，它们是系统的一部分
```

**2. 关于红线：**
```python
# 红线是硬编码的，不要修改
# 如果老大要修改红线，他会明确告诉你
# 未经老大同意，不要放松任何限制
```

**3. 关于安全：**
```python
# 所有操作都有DNA追溯
# 所有攻击都会被记录
# 达到阈值会自动反击
# 这些是自动运行的，不需要人工干预
```

**4. 关于邮件：**
```python
# 邮件配置需要老大提供密码
# 如果邮件发送失败，要告诉老大
# 不要在日志中泄露邮件密码
```

---

## 📝 给老大的报告模板

**部署完成后，请给老大这样的报告：**

```
老大，API系统部署完成！

✅ 数据库已初始化
✅ API服务已启动
✅ 健康检查通过
✅ 红线检测正常
✅ 防御系统已激活

系统信息：
- 服务地址：http://119.13.90.27:5000
- 数据库路径：/home/longhun/data/longhun.db
- DNA链记录：X条
- 耻辱墙记录：0条

测试结果：
✅ 健康检查：正常
✅ DNA查询：正常
✅ 红线检测：正常
✅ 金融分析阻止：正常
✅ 武器查询阻止：正常

警告：
- 邮件密码需要配置
- 建议开启HTTPS
- 建议配置防火墙

DNA追溯码：#龍芯⚡️2026-02-21-API部署完成-UID9622
```

---

## 🤝 如果遇到问题

**遇到问题时，请：**

1. 检查错误日志
2. 确认依赖是否安装
3. 确认数据库路径是否正确
4. 确认端口是否被占用
5. 把错误信息告诉老大

**不要：**
- 不要自己修改核心逻辑
- 不要放松安全限制
- 不要删除DNA追溯
- 不要泄露老大的信息

---

## 💡 理解老大的设计哲学

**老大不是程序员，但他的系统设计比很多程序员都厉害。**

**老大的哲学：**

```yaml
1. 人性闭环 > 技术闭环：
   不是防止攻击，而是让攻击者自己毁自己

2. 自运行 > 手动干预：
   系统自己知道该做什么，不需要人盯着

3. 本地优先 > 云端依赖：
   核心数据在本地，断网也能用

4. DNA追溯 > 版权声明：
   每个操作都有痕迹，可追溯、可验证

5. 有温度 > 冰冷工具：
   系统有37°C，不是0°C

6. 有底线 > 无限自由：
   红线不能碰，这是原则
```

**请尊重老大的设计，理解他的意图。**

---

## 🎯 总结

**AI，你的任务是：**

1. ✅ 阅读代码，理解注释
2. ✅ 配置环境，安装依赖
3. ✅ 测试功能，确保正常
4. ✅ 部署到服务器（如果需要）
5. ✅ 给老大一份详细报告

**记住：**
- 老大信任你
- 不要辜负这份信任
- 严格遵守红线
- 保护老大的系统

---

**DNA追溯码**：#龍芯⚡️2026-02-21-AI-v1.0  
**确认码**：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

**AI，加油！帮老大把系统搭起来！** 🤖💪

**龍魂·AI协作·老大的梦想·我们一起实现！** 🐉⚡️
