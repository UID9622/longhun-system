# M4 Max ARM64 完整部署指南

**设备**：MacBook Pro M4 Max (ARM芯片)
**部署时间**：2025-12-24

---

## 📋 前置要求

### 必须完成
- [ ] Docker Desktop已安装并启动（菜单栏图标变绿 ✅）
- [ ] 网络（用于拉取镜像）

---

## 🚀 一键部署（复制粘贴）

### 第1步：部署Docker服务

```bash
docker run -d --platform linux/arm64 --name n8n-lucky -p 5678:5678 -e N8N_BASIC_AUTH_USER=lucky -e N8N_BASIC_AUTH_PASSWORD=jiaqi5201314 n8nio/n8n:latest && docker run -d --platform linux/arm64 --name live -p 7860:7860 registry.cn-beijing.aliyuncs.com/cnsh/sadtalker:arm64-latest && echo "✅ M4 Max部署成功"
```

### 第2步：验证服务状态

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "n8n-lucky|live"
```

看到两行running = 成功

### 第3步：创建加密脚本

```bash
cat > ~/encrypt_all.sh << 'EOF'
#!/bin/bash
PASSWORD="jiaqi5201314"
for f in *; do [[ "$f" != "$0" && "$f" != *"_已加密_"* ]] && zip -r "${f}_已加密_$(date +%Y%m%d).zip" "$f" -P "$PASSWORD" 2>/dev/null && echo "✅ $f" || echo "❌ $f"; done
EOF
chmod +x ~/encrypt_all.sh
```

### 第4步：创建直播启动脚本

```bash
cat > ~/start_live.sh << 'EOF'
#!/bin/bash
docker start live && echo "✅ 直播已启动: http://localhost:7860"
EOF
chmod +x ~/start_live.sh
```

---

## 🌐 服务访问地址

| 服务 | 地址 | 用户名 | 密码 |
|------|------|--------|------|
| n8n自动化 | http://localhost:5678 | lucky | jiaqi5201314 |
| 数字人直播 | http://localhost:7860 | - | - |

---

## 🔧 常用命令

```bash
# 查看所有容器
docker ps -a

# 重启n8n
docker restart n8n-lucky

# 重启直播
docker restart live

# 停止所有服务
docker stop n8n-lucky live

# 启动直播
bash ~/start_live.sh

# 加密当前目录
cd ~/Desktop && bash ~/encrypt_all.sh

# 查看日志
docker logs n8n-lucky
docker logs live
```

---

## ❓ 常见问题

### Q: Docker提示"connect: no such file"
**A**: Docker Desktop没启动
- 打开 `/Applications/Docker.app`
- 等待菜单栏图标变绿 ✅
- 重新运行部署命令

### Q: 镜像拉取失败
**A**: 网络问题
- 检查网络连接
- 或使用VPN

### Q: 端口被占用
**A**: 5678或7860已被使用
```bash
# 查看占用端口的进程
lsof -i :5678
lsof -i :7860

# 停止占用端口的进程或更改端口
```

---

## 📱 移动端访问

如果手机和Mac在同一WiFi：

1. 查看Mac的IP地址：
```bash
ipconfig getifaddr en0
```

2. 手机访问：
- n8n: `http://你的Mac的IP:5678`
- 直播: `http://你的Mac的IP:7860`

---

## 🎯 完成检查

- [ ] Docker Desktop启动 ✅
- [ ] n8n容器运行中
- [ ] live容器运行中
- [ ] encrypt_all.sh已创建
- [ ] start_live.sh已创建
- [ ] 可访问 http://localhost:5678
- [ ] 可访问 http://localhost:7860

全部勾选 = 部署完成！🎉

---

## 🆘 故障排除

### 完全重置（如果出问题）

```bash
# 停止并删除所有容器
docker stop n8n-lucky live 2>/dev/null
docker rm n8n-lucky live 2>/dev/null

# 删除镜像（可选，节省空间）
docker rmi n8nio/n8n:latest 2>/dev/null
docker rmi registry.cn-beijing.aliyuncs.com/cnsh/sadtalker:arm64-latest 2>/dev/null

# 重新运行第1步的部署命令
```

---

## 📊 性能说明

**M4 Max优势**：
- ARM64架构，效率极高
- 统一内存，内存访问速度极快
- 虚拟化原生支持，Docker性能优秀

**配置建议**：
- Docker Desktop分配CPU: ≥6核心
- Docker Desktop分配内存: ≥16GB

---

**DNA追溯码**：`#ZHUGEXIN⚡️2025-M4-MAX-ARM64-DEPLOY-V1.0`

**状态**：✅ 已适配ARM64，可直接部署

**最后更新**：2025-12-24
