# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🚀 龍魂宝宝守护助手 · 5分钟快速开始指南

**DNA**:#龍芯⚡️2026-06-04-QUICKSTART-v1.0  
**时间**: 5分钟即可看到运行中的应用

---

## 📋 检查清单

在开始前，请确认你已安装：

- ✅ Node.js 18+ (`node --version`)
- ✅ Python 3.11+ (`python3 --version`)
- ✅ npm (`npm --version`)

## 🎬 3 秒钟一键启动

### macOS / Linux

```bash
cd ~/longhun-system/baobao-guardian
./start.sh
```

### Windows

```bash
cd ~\longhun-system\baobao-guardian
start.bat
```

---

## ⏳ 自动化流程发生什么？

1. **后端启动** (30秒)
   - 创建 Python 虚拟环境
   - 安装 FastAPI、Uvicorn 等依赖
   - 启动 WebSocket 服务器 (Port 8000)

2. **前端启动** (30秒)
   - 安装 React、Three.js、Electron 等依赖
   - 启动 Vite 开发服务器 (Port 5173)
   - 自动在浏览器中打开

3. **完成** (1分钟内)
   - 看到粉红色的宝宝在右下角
   - Overlay 边框显示（绿色安全状态）
   - 左上角"已连接"状态指示

---

## 🌐 访问应用

启动完成后，打开浏览器访问：

- **应用首页**: http://localhost:5173
- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

---

## 🧪 快速测试

### 测试 1: 改变 Overlay 层级

在新终端中运行：

```bash
# 改为警告（橙色）
curl -X POST http://localhost:8000/api/overlay/level?level=warning

# 改为危险（红色）
curl -X POST http://localhost:8000/api/overlay/level?level=danger

# 回到安全（绿色）
curl -X POST http://localhost:8000/api/overlay/level?level=safe
```

**观察**: 前端的 Overlay 边框颜色和脉冲强度应该实时改变

### 测试 2: 让宝宝说话

```bash
curl -X POST http://localhost:8000/api/baobao/speak \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好！我是宝宝！",
    "emotion": "happy",
    "duration": 3000
  }'
```

**观察**: 右下角宝宝的气泡应该显示消息

### 测试 3: 宝宝反应

```bash
curl -X POST http://localhost:8000/api/baobao/react?emotion=warning
```

**观察**: 宝宝应该摇晃几次，表情改变

---

## 📊 验证系统状态

```bash
# 检查后端健康状态
curl http://localhost:8000/health

# 应该返回类似：
# {
#   "status": "healthy",
#   "connections": 1,
#   "overlay_state": { ... }
# }
```

---

## 🛑 停止服务

### 优雅停止（推荐）

在启动脚本的终端中按 `Ctrl+C`

### 强制停止

```bash
# macOS / Linux
kill $(lsof -t -i:8000)   # 杀死后端
kill $(lsof -t -i:5173)   # 杀死前端

# Windows
taskkill /PID <PID> /F
```

---

## 📁 项目结构概览

```
baobao-guardian/
├── frontend/          # React + Three.js 前端
├── backend/           # FastAPI 后端
├── README.md          # 完整文档
├── start.sh           # 自动启动脚本
├── start.bat          # Windows 启动脚本
└── QUICKSTART.md      # 本文档
```

---

## 🔧 常见问题排查

### Q: 后端无法启动

```
❌ 错误: Address already in use: 0.0.0.0:8000
```

**解决**: 端口被占用

```bash
# 查看谁在使用端口 8000
lsof -i :8000

# 杀死该进程
kill <PID>
```

### Q: 前端无法连接后端

**症状**: 左上角显示"离线"

**排查**:
1. 确保后端正在运行: `curl http://localhost:8000/health`
2. 检查防火墙是否允许端口 8000
3. 刷新浏览器
4. 检查浏览器开发工具 (F12) 的 Console 标签

### Q: npm install 很慢

**解决**: 使用阿里镜像加速（中国用户）

```bash
npm install -g cnpm --registry=https://registry.npmmirror.com
cd frontend
cnpm install
```

---

## 📈 下一步

### 自定义应用

编辑这些文件进行定制：

| 文件 | 用途 |
|------|------|
| `frontend/src/components/Baobao.tsx` | 改变宝宝的颜色/大小 |
| `frontend/src/styles/animations.css` | 调整动画速度 |
| `backend/app/main.py` | 添加新的 API 端点 |

### 打包为桌面应用

```bash
cd frontend
npm run electron:build
```

输出在 `dist/` 目录中

---

## 💡 技术栈速览

| 层 | 技术 | 版本 |
|----|------|------|
| 桌面 | Electron | 27+ |
| 前端 | React | 18 |
| 3D | Three.js | r161 |
| 构建 | Vite | 5.0 |
| 后端 | FastAPI | 0.104 |
| 通信 | WebSocket | 12.0 |

---

## 🎯 目标状态

启动成功后，你应该看到：

```
✅ 后端
   - Uvicorn 在 8000 运行
   - 日志显示 "🚀 龍魂宝宝守护助手后端启动"

✅ 前端
   - Vite 在 5173 运行
   - 自动打开浏览器
   - 粉红色圆形宝宝在右下角

✅ 通信
   - 左上角显示 "已连接"（绿色点）
   - Overlay 边框可见
   - 粒子效果正常流动
```

---

## 📞 获取帮助

1. **查看完整文档**: `cat README.md`
2. **检查日志**: 检查后端和前端窗口的日志输出
3. **API 文档**: 访问 http://localhost:8000/docs (Swagger UI)
4. **代码注释**: 所有核心文件都有中文注释

---

## ✨ 恭喜！

你现在已经运行了龍魂系统的心脏应用 🐉

**下一步探索**:
- 修改 `Overlay.tsx` 添加更多视觉效果
- 在 `main.py` 中添加新的 REST API
- 集成 Notion 数据库
- 实现语音识别

---

**DNA**:#龍芯⚡️2026-06-04-BAOBAO-MVP-v1.0  
**创作者**: UID9622 · 诸葛鑫 · 龍芯北辰  
**理论指导**: 曾仕强老师（永恒显示）
