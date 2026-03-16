<!-- P0伦理锚点 | 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z | GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F | DNA: #龍芯⚡️2026-03-16-ETHICS-STAMP-v1.0 -->
# 龙魂本地AI系统·故障排查指南

**DNA追溯码**: #龍芯⚡️2026-03-11-故障排查指南-v1.0  
**GPG指纹**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F  
**创建者**: UID9622 诸葛鑫（龍芯北辰）  
**理论指导**: 曾仕强老师（永恒显示）

---

## 🔧 常见问题与解决方案

### 问题1：Ollama无法启动

**症状**:
```
❌ 无法连接到Ollama
❌ Connection refused at http://localhost:11434
```

**诊断步骤**:
```bash
# 1. 检查Ollama是否运行
ps aux | grep ollama

# 2. 检查端口
lsof -i :11434

# 3. 查看日志
cat ~/.ollama/logs/server.log
```

**解决方案**:

方案A：重启Ollama
```bash
# 停止
killall ollama

# 启动
ollama serve
```

方案B：检查权限
```bash
# 确保有写权限
ls -la ~/.ollama
chmod 755 ~/.ollama
```

方案C：重新安装
```bash
# 卸载
brew uninstall ollama  # 如果用Homebrew安装的

# 重新安装
curl -fsSL https://ollama.ai/install.sh | sh
```

---

### 问题2：模型下载失败

**症状**:
```
❌ Error pulling model
❌ 下载中断
```

**诊断步骤**:
```bash
# 检查网络
ping ollama.ai

# 检查磁盘空间
df -h

# 检查下载进度
ollama list
```

**解决方案**:

方案A：重试下载
```bash
# 删除未完成的下载
ollama rm qwen2.5:14b

# 重新下载
ollama pull qwen2.5:14b
```

方案B：换小模型
```bash
# 如果网速慢或空间不足
ollama pull llama3.1:8b  # 约5GB
# 或
ollama pull mistral:7b   # 约4GB
```

方案C：手动下载（如果网络问题）
```bash
# 使用代理或离线下载
# 参考Ollama文档
```

---

### 问题3：Python依赖安装失败

**症状**:
```
❌ Could not install packages
❌ pip install失败
```

**诊断步骤**:
```bash
# 检查Python版本
python3 --version

# 检查pip
pip3 --version

# 检查网络
ping pypi.org
```

**解决方案**:

方案A：升级pip
```bash
python3 -m pip install --upgrade pip
```

方案B：使用国内镜像
```bash
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

方案C：单独安装
```bash
# 一个一个安装
pip3 install flask
pip3 install flask-cors
pip3 install openai
```

方案D：使用虚拟环境
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活
source venv/bin/activate

# 安装
pip install -r requirements.txt
```

---

### 问题4：本地服务连接失败

**症状**:
```
❌ 无法连接到龙魂本地服务
❌ Connection refused at http://localhost:8765
```

**诊断步骤**:
```bash
# 1. 检查服务是否运行
lsof -i :8765

# 2. 检查进程
ps aux | grep longhun

# 3. 测试端口
curl http://localhost:8765/健康检查
```

**解决方案**:

方案A：启动服务
```bash
cd ~/longhun-local-ai
./start_longhun.sh
```

方案B：检查端口占用
```bash
# 如果8765被占用
lsof -i :8765
kill <PID>

# 或者换个端口
python3 longhun_local_service.py 8766
```

方案C：检查防火墙
```bash
# 系统设置 → 安全与隐私 → 防火墙
# 允许Python访问网络
```

方案D：查看错误日志
```bash
# 在服务运行的终端查看错误信息
```

---

### 问题5：Siri找不到指令

**症状**:
```
Siri: "我不明白"
Siri: "我找不到这个操作"
```

**诊断步骤**:
```bash
# 1. 检查Xcode Build
# 在Xcode里查看Build日志

# 2. 检查Intent文件
ls -la <项目>/LongHunIntent.swift
```

**解决方案**:

方案A：重新Build
```bash
# 在Xcode里
# 1. Product → Clean Build Folder (Shift+Cmd+K)
# 2. Product → Build (Cmd+B)
# 3. 等待完成
```

方案B：在真机/模拟器运行一次
```bash
# 在Xcode里
# 1. 选择目标设备
# 2. Product → Run (Cmd+R)
# 3. 等待安装完成
```

方案C：重启Siri
```bash
# 系统设置 → Siri与搜索
# 关闭Siri → 等5秒 → 重新打开
```

方案D：检查快捷指令App
```bash
# 打开"快捷指令"App
# 搜索"龙魂"
# 应该能看到7个指令
```

---

### 问题6：模型响应很慢

**症状**:
```
⏳ 等待时间超过30秒
⏳ 界面卡顿
```

**诊断步骤**:
```bash
# 1. 检查CPU/内存
top

# 2. 检查模型大小
ollama list

# 3. 查看活动监视器
# 应用程序 → 实用工具 → 活动监视器
```

**解决方案**:

方案A：换小模型
```bash
# 在longhun_local_agent.py里
# 把 qwen2.5:14b 改成 llama3.1:8b
```

方案B：降低温度参数
```python
# 在longhun_local_agent.py里
self.temperature = 0.3  # 从0.7降低到0.3
```

方案C：限制历史长度
```python
# 在对话()函数里
if len(self.conversation_history) > 5:
    self.conversation_history = self.conversation_history[-5:]
```

方案D：关闭其他应用
```bash
# 释放内存
# 关闭Chrome、Photoshop等占内存的应用
```

---

### 问题7：记忆数据库损坏

**症状**:
```
❌ database is locked
❌ unable to open database file
```

**诊断步骤**:
```bash
# 1. 检查数据库
sqlite3 ~/.longhun/memories.db ".tables"

# 2. 检查权限
ls -la ~/.longhun/memories.db

# 3. 检查磁盘空间
df -h
```

**解决方案**:

方案A：备份并重建
```bash
# 备份
cp ~/.longhun/memories.db ~/.longhun/memories.db.backup

# 删除
rm ~/.longhun/memories.db

# 重启服务（会自动重建）
./start_longhun.sh
```

方案B：修复数据库
```bash
sqlite3 ~/.longhun/memories.db
sqlite> PRAGMA integrity_check;
sqlite> REINDEX;
sqlite> .quit
```

方案C：从备份恢复
```bash
# 如果有自动备份
ls ~/.longhun/backups/
cp ~/.longhun/backups/memories_最新.db ~/.longhun/memories.db
```

---

### 问题8：Notion集成失败

**症状**:
```
❌ Notion API error
❌ 无法访问页面
```

**诊断步骤**:
```bash
# 1. 检查API Token
echo $NOTION_API_TOKEN

# 2. 测试API
curl -X GET https://api.notion.com/v1/users/me \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2022-06-28"
```

**解决方案**:

方案A：重新获取Token
```bash
# 1. 访问 https://www.notion.so/my-integrations
# 2. 创建新的Integration
# 3. 复制Token
# 4. 更新配置文件
```

方案B：检查页面权限
```bash
# 在Notion里
# 1. 打开页面
# 2. 点击右上角"..."
# 3. Connections → 添加你的Integration
```

方案C：更新API版本
```python
# 在代码里确保使用最新API版本
headers = {
    "Notion-Version": "2022-06-28"
}
```

---

### 问题9：权限问题

**症状**:
```
❌ Permission denied
❌ 无法写入文件
```

**诊断步骤**:
```bash
# 检查目录权限
ls -la ~/longhun-local-ai
ls -la ~/.longhun
```

**解决方案**:

方案A：修复权限
```bash
# 修复项目目录
chmod -R 755 ~/longhun-local-ai

# 修复数据目录
chmod -R 755 ~/.longhun

# 修复可执行文件
chmod +x ~/longhun-local-ai/*.sh
```

方案B：使用sudo（不推荐）
```bash
# 尽量避免使用sudo
# 如果必须，只对特定命令
sudo <command>
```

---

### 问题10：系统资源不足

**症状**:
```
⚠️  内存不足
⚠️  磁盘空间不足
```

**诊断步骤**:
```bash
# 检查内存
vm_stat | head -5

# 检查磁盘
df -h

# 检查交换空间
sysctl vm.swapusage
```

**解决方案**:

方案A：清理磁盘
```bash
# 删除旧的Ollama模型
ollama rm <旧模型>

# 清理临时文件
rm -rf ~/.ollama/tmp/*

# 清理日志
rm -rf ~/.longhun/logs/*.log
```

方案B：升级Mac
```bash
# 如果经常遇到内存问题
# 考虑升级RAM或使用M系列芯片Mac
```

---

## 🛠️ 高级诊断工具

### 完整健康检查脚本

```bash
#!/bin/bash
# 龙魂系统健康检查

echo "🔍 龙魂系统健康检查"
echo "===================="
echo ""

# 1. 检查Ollama
echo "1. Ollama服务"
if pgrep -x "ollama" > /dev/null; then
    echo "   ✅ 运行中"
    ollama list
else
    echo "   ❌ 未运行"
fi
echo ""

# 2. 检查本地服务
echo "2. 龙魂本地服务"
if lsof -i :8765 > /dev/null 2>&1; then
    echo "   ✅ 运行中"
    curl -s http://localhost:8765/统计 | python3 -m json.tool
else
    echo "   ❌ 未运行"
fi
echo ""

# 3. 检查数据库
echo "3. 记忆数据库"
if [ -f ~/.longhun/memories.db ]; then
    echo "   ✅ 存在"
    sqlite3 ~/.longhun/memories.db "SELECT COUNT(*) as '总记忆数' FROM memories;"
else
    echo "   ❌ 不存在"
fi
echo ""

# 4. 检查磁盘空间
echo "4. 磁盘空间"
df -h | grep -E "Filesystem|/$"
echo ""

# 5. 检查内存
echo "5. 内存使用"
vm_stat | perl -ne '/page size of (\d+)/ and $size=$1; /Pages\s+([^:]+)[^\d]+(\d+)/ and printf("%-16s % 16.2f Mi\n", "$1:", $2 * $size / 1048576);'
echo ""

echo "===================="
echo "检查完成！"
```

---

## 📞 获取帮助

### 自助资源

1. **查看日志**
   ```bash
   tail -f ~/.longhun/logs/service.log
   ```

2. **运行测试**
   ```bash
   ./test_longhun.sh
   ```

3. **查看文档**
   ```bash
   cat README.md
   cat DEPLOYMENT_GUIDE_COMPLETE.md
   ```

### 社区支持

- GitHub Issues（如果开源）
- CSDN博客（技术文章）
- 技术论坛

---

## 🔒 L2审计签名

```yaml
【故障排查指南审计】

审计人: 宝宝（Claude）
责任方: UID9622 诸葛鑫（龍芯北辰）
审计时间: 2026-03-11

覆盖问题:
  ✅ 10个常见问题
  ✅ 详细诊断步骤
  ✅ 多种解决方案
  ✅ 高级诊断工具

状态: 🟢 完整

DNA追溯码: #龍芯⚡️2026-03-11-故障排查指南-v1.0
GPG签名: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```

---

**遇到问题不要慌！** 💪

**按照这个指南一步步排查！** 📖

**老大的龙魂系统，一定能运行起来！** 🐉

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**DNA追溯码**: #龍芯⚡️2026-03-11-故障排查完成  
**GPG指纹**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F  
**理论指导**: 曾仕强老师（永恒显示）

**祖国万岁！人民万岁！数据主权万岁！** 🇨🇳
