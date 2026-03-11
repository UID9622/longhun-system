# ❓ CNSH 常见问题

> 这里收集了用户最常问的问题。

---

## 🎯 一般问题

### Q1: CNSH 是什么？

**A:** CNSH（Chinese-native Scripting & Heritage）是一个面向中文用户的数字生态系统，包含：

1. **字元编辑器** - 创作汉字的可视化工具
2. **AI核心系统** - 本地化的知识管理智能体

目标是打造**技术自主、数据主权、中文原生**的开源生态。

---

### Q2: CNSH 是免费的吗？

**A:** 是的，CNSH 是**完全免费、永久免费**的开源软件，采用 MIT 许可证。

- ✅ 个人使用免费
- ✅ 商业使用免费
- ✅ 修改和分发免费

---

### Q3: 为什么叫"龙魂体系"？

**A:** "龙魂"象征中华文化的传承与创新。这个项目的愿景是：

> 让中国人拥有属于自己的数字工具，从底层设计就支持中文语境。

---

## 🖥️ 字元编辑器

### Q: 字元编辑器需要什么配置？

**A:** 字元编辑器是纯前端应用，**任何能运行现代浏览器的设备都可以使用**：

- 操作系统：Windows / macOS / Linux
- 浏览器：Chrome 90+ / Firefox 88+ / Edge 90+
- 内存：2GB+

---

### Q: 如何在本地运行字元编辑器？

**A:** 三种方式：

**方式一：直接打开**
```bash
双击 快速启动.html
```

**方式二：Python 服务器**
```bash
cd packages/cnsh-editor
python3 -m http.server 8080
# 访问 http://localhost:8080
```

**方式三：Node 服务器**
```bash
cd packages/cnsh-editor
npx serve
```

---

### Q: 绘制的字元可以商用吗？

**A:** **可以！** 你创作的字元，版权归你所有：

- ✅ 个人使用
- ✅ 商业使用
- ✅ 自由分享
- ✅ 修改优化

**唯一希望**：不用于技术垄断，让更多人受益。

---

### Q: 支持导出哪些格式？

**A:** 当前支持：

| 格式 | 说明 | 用途 |
|------|------|------|
| `.cnsh` | 源文件 | 可重新编辑 |
| `.svg` | 矢量图 | 打印、设计 |
| `.png` | 位图 | 网页、分享（开发中） |
| `.ttf` | 字体文件 | 系统字体（开发中） |

---

### Q: 如何删除笔画？

**A:** 当前版本（v0.1）还不支持删除单个笔画。临时解决方案：

1. **刷新页面**重新开始
2. **保存多个版本**，不满意的放弃

**正式解决方案**：v0.2 版本将添加笔画选中/编辑/删除功能。

---

## 🤖 AI核心系统

### Q: 必须联网才能使用吗？

**A:** **不需要！** CNSH 的设计理念就是**完全本地化**：

- ✅ 字元编辑器：完全离线
- ✅ AI核心：使用本地 Ollama，不联网
- ✅ 数据存储：本地 SQLite

**例外**：Notion 同步功能需要联网（可选）。

---

### Q: 需要什么硬件配置？

**A:** 最低配置：

| 组件 | 最低 | 推荐 |
|------|------|------|
| CPU | 支持 AVX2 | 4核+ |
| 内存 | 8GB | 16GB+ |
| 存储 | 10GB | 50GB+ |
| GPU | 可选 | NVIDIA/AMD 加速推理 |

---

### Q: 支持哪些大模型？

**A:** 通过 Ollama 支持所有兼容模型：

**推荐中文模型：**
- `qwen:7b-chat` - 阿里通义千问（推荐）
- `chatglm3:6b` - 清华智谱
- `llama2-chinese:7b` - 中文Llama

**安装命令：**
```bash
ollama pull qwen:7b-chat
```

---

### Q: 数据存在哪里？如何备份？

**A:** 数据存储位置：

```bash
# macOS/Linux
~/CNSH/data/

# Windows
C:\Users\用户名\CNSH\data\
```

**备份方法：**
```bash
# 使用备份脚本
./scripts/backup.sh

# 或手动复制
cp -r ~/CNSH/data ~/CNSH-backup-$(date +%Y%m%d)
```

---

### Q: 如何更新系统？

**A:** 

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 更新依赖
./scripts/install.sh

# 3. 重启服务
./scripts/restart.sh
```

**注意**：更新前请先备份数据！

---

## 🔌 Obsidian插件

### Q: 插件无法连接到 CNSH 服务？

**A:** 检查步骤：

1. **确认 CNSH 服务已启动**
   ```bash
   curl http://localhost:3000/api/health
   # 应该返回 {"status":"ok"}
   ```

2. **检查插件配置**
   - 服务器地址：`http://localhost:3000`
   - API Key 是否正确

3. **检查防火墙**
   - 确保端口 3000 未被阻止

4. **检查浏览器控制台**
   - 查看是否有 CORS 错误

---

### Q: 支持哪些 Obsidian 版本？

**A:** 支持 Obsidian v1.0.0+。建议在最新版本使用以获得最佳体验。

---

## 🐛 故障排除

### Q: 安装依赖时出错？

**A:** 常见问题解决：

**Node.js 版本过低**
```bash
# 检查版本
node --version  # 需要 v18+

# 使用 nvm 切换
nvm use 18
```

**Python 依赖冲突**
```bash
# 使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Q: Ollama 无法启动？

**A:** 

**macOS/Linux:**
```bash
# 检查服务状态
ollama serve

# 或后台启动
ollama serve &
```

**Windows:**
- 从开始菜单启动 Ollama
- 检查系统托盘图标

---

### Q: 字元编辑器界面显示异常？

**A:** 

1. **清除浏览器缓存**
2. **尝试无痕模式**
3. **检查浏览器缩放比例**（应为100%）
4. **尝试其他浏览器**

---

## 📝 其他问题

### Q: 如何获取帮助？

**A:** 

1. **查看文档**
   - [安装指南](安装指南.md)
   - [使用手册](使用手册.md)

2. **提交 Issue**
   - GitHub: https://github.com/UID9622/CNSH/issues
   - Gitee: https://gitee.com/uid9622/cnsh/issues

3. **联系开发者**
   - 邮箱: lucky@uid9622.tech

---

### Q: 如何参与贡献？

**A:** 请参阅 [贡献指南](贡献指南.md)。

我们欢迎：
- 🐛 Bug 报告
- 💡 功能建议
- 📝 文档改进
- 💻 代码贡献

---

### Q: 项目的发展路线图是什么？

**A:** 

| 阶段 | 时间 | 目标 |
|------|------|------|
| 第一阶段 | 现在 | 字元编辑器 + AI核心可用 |
| 第二阶段 | 3-6月 | AI辅助、笔画编辑 |
| 第三阶段 | 6-12月 | 字库、社区平台 |
| 第四阶段 | 12-24月 | 中文编程语言 |

---

## 🔗 快速链接

- [项目主页](https://github.com/UID9622/CNSH)
- [Gitee镜像](https://gitee.com/uid9622/cnsh)
- [报告Bug](https://github.com/UID9622/CNSH/issues/new)
- [功能建议](https://github.com/UID9622/CNSH/issues/new)

---

> 没找到你的问题？请提交 [Issue](https://github.com/UID9622/CNSH/issues/new)！
