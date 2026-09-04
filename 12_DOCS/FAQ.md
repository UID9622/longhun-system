# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 常见问题

> DNA: `#龍芯⚡️丙午·乙未·丙午·甲午·䷳艮为山-FAQ-v1.0-UID9622`
> 最后更新: 2026-07-31

---

## 快速索引

- [安装相关](#安装相关)
- [使用相关](#使用相关)
- [君子协议相关](#君子协议相关)
- [API相关](#api相关)
- [安全相关](#安全相关)
- [贡献相关](#贡献相关)
- [哲学相关](#哲学相关)

---

## 安装相关

### Q: 最低配置要求？
- Python 3.11+，2GB RAM，1GB 磁盘
- 推荐: Python 3.12，8GB RAM（跑模型时需要）

### Q: 支持什么操作系统？
- ✅ macOS（开发主力）
- ✅ Linux / Ubuntu / Debian
- ✅ 鲲鹏 ARM 服务器
- ⚠️ Windows（部分功能支持，见[安装指南](../INSTALL.md)）

### Q: 需要联网吗？
大部分功能可离线使用。使用搜索引擎或鲲鹏API时需要联网。

### Q: 安装失败怎么办？
1. 确认 Python >= 3.11：`python3 --version`
2. 尝试虚拟环境：`python3 -m venv .venv && source .venv/bin/activate`
3. 查看详细错误并提交 [Issue](https://github.com/UID9622/longhun-system/issues)

---

## 使用相关

### Q: 怎么注册/登录？
不需要注册。龍魂系统核心是本地软件，不设账号体系。
如需使用API服务，可设置 `LH_API_KEY` 环境变量进行认证。

### Q: 怎么查看省电积分？
```bash
# 本地API
curl http://localhost:9622/stats
# 鲲鹏API
curl https://uid9622.cn/stats
```

### Q: 支持的触发词有哪些？
```bash
lh --trigger list
# 或 API
curl http://localhost:9622/triggers
```

### Q: 如何备份数据？
```bash
# 备份记忆数据
cp -r ~/.longhun/ ~/backup/longhun-$(date +%Y%m%d)/
# 备份项目配置
cp .env ~/backup/
```

### Q: "lh: command not found"？
```bash
# 重新注册别名
echo 'alias lh="python3 ~/longhun-system/bin/lh.py"' >> ~/.zshrc
source ~/.zshrc
```

---

## 君子协议相关

### Q: 君子协议是什么？
君子协议是龍魂社区的伦理契约。核心：不商业化、数据主权归用户、算法透明。

详见 [GENTLEMANS_PROTOCOL.md](../GENTLEMANS_PROTOCOL.md)。

### Q: 怎么签署君子协议？
使用龍魂系统即视为默示签署。
显式签署：`lh gentleman register --name "你的名字"`

### Q: 违反协议的后果？
- 🟡 轻微：提醒纠正
- 🟠 中度：耻辱柱记录 + 公开通报
- 🔴 严重：永久封禁 + 法律追诉

### Q: 如何举报违规？
- GitHub Issues: 标记 `[违规举报]`
- 加密邮件: `security@uid9622.cn`（GPG: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`）

---

## API相关

### Q: API是免费的吗？
非商业用途免费。商业使用需联系授权。

### Q: 支持什么协议？
HTTPS REST API，JSON格式。有 OpenAPI 3.0 规范文档。

### Q: API调用有限制吗？
目前无速率限制。请合理使用。滥用可能被限制。

### Q: 异步模式怎么用？
```bash
# 提交异步任务
curl -X POST http://localhost:9622/run \
  -H "Content-Type: application/json" \
  -d '{"trigger":"健康检查","async_mode":true}'
# 返回 task_id，轮询
curl http://localhost:9622/task/{task_id}
```
需 Redis 支持。

---

## 安全相关

### Q: 我的数据安全吗？
龍魂系统优先本地运行，数据在你的设备上。API传输使用 HTTPS 加密。详见 [PRIVACY_POLICY.md](../PRIVACY_POLICY.md)。

### Q: 如何报告安全漏洞？
请勿在公开Issue中报告安全漏洞。发送至：
- `security@uid9622.cn`（GPG加密）
- 详见 [SECURITY.md](../SECURITY.md)

### Q: 什么是三色审计？
🟢通过 · 🟡待核实 · 🔴红线。所有代码和内容产出都必须经过三色判定。

### Q: DNA追溯码是什么？
每个操作/文件的不可篡改身份码，格式：
`#龍芯⚡️<干支四柱>·<卦>-<模块>-<动作>-<哈希8>`

---

## 贡献相关

### Q: 如何贡献代码？
1. Fork 本仓库
2. 签署君子协议
3. 创建分支 → 提交代码 → 发起 PR
4. 通过三色审计

详见 [CONTRIBUTING.md](../CONTRIBUTING.md)。

### Q: 代码规范？
- PEP8 风格
- 类型注解（Python 3.11+）
- DNA注释（每个文件头三行）
- 详细要求见 CONTRIBUTING.md

### Q: 可以提 Feature Request 吗？
可以！在 [Discussions](https://github.com/UID9622/longhun-system/discussions) 提出。

---

## 哲学相关

### Q: 为什么叫"龍魂"？
龍 = 中华文明图腾，魂 = 精神内核。系统承载着"技术服务于中国人民"的精神。

### Q: "省电"是什么意思？
大模型推理一个任务需 2-10 秒，耗电很高。龍魂系统用确定性脚本执行替代，省电率 99.98%。

### Q: 为什么用易经/369/五行？
不是玄学，是数学锚点。易经64卦是离散决策空间的完备划分；369源自洛书九宫；五行为多维分类框架。

### Q: "外化内不化"是什么？
外表适应变化，内心坚守底线。技术可以迭代，但数据主权、为人民服务的原则不变。

---

> 🐉 **问得越多，理解越深。欢迎继续提问。**
