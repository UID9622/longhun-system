# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂宝宝守护助手 · Baobao Guardian

**DNA**:#龍芯⚡️2026-06-04-BAOBAO-MVP-v1.0  
**理论指导**: 曾仕强老师（永恒显示）  
**创作者**: UID9622 · 诸葛鑫 · 龍芯北辰

---

## 📖 项目简介

宝宝守护助手是龍魂系统的"心脏应用"——一个跨平台的桌面应用，为用户提供：

- 🎨 **全屏 Overlay 层** - 实时问题严重程度可视化（红/橙/绿三色）
- 🤖 **宝宝助手** - 右下角智能助手，带动画和表情变化
- ✨ **粒子效果** - Three.js 3D 粒子系统，视觉增强
- 💬 **聊天高亮** - 自动识别和高亮关键词
- 🔄 **实时通信** - WebSocket 前后端双向通信

## 🏗️ 项目结构

```
baobao-guardian/
├── frontend/                    # React + Electron 前端
│   ├── src/
│   │   ├── components/         # React 组件
│   │   │   ├── Overlay.tsx     # 全屏覆盖层
│   │   │   ├── Baobao.tsx      # 宝宝助手
│   │   │   └── ParticleContainer.tsx  # 粒子系统
│   │   ├── store/              # Zustand 状态管理
│   │   │   ├── overlay.ts
│   │   │   └── baobao.ts
│   │   ├── services/           # 业务逻辑
│   │   │   └── wsClient.ts     # WebSocket 客户端
│   │   └── styles/             # 样式文件
│   │       ├── animations.css  # 动画库
│   │       └── index.css       # 全局样式
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── electron-main.ts
│   └── index.html
│
├── backend/                     # FastAPI 后端
│   ├── app/
│   │   └── main.py            # FastAPI 应用
│   ├── requirements.txt         # Python 依赖
│   └── .env                     # 环境变量
│
└── README.md                    # 本文件
```

## 🚀 快速开始

### 前置要求

- **Node.js** 18+ & npm
- **Python** 3.11+
- **Git**

### 步骤 1: 安装前端依赖

```bash
cd frontend
npm install
```

### 步骤 2: 安装后端依赖

```bash
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 步骤 3: 启动后端（新终端）

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

**输出应该包含**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     🚀 龍魂宝宝守护助手后端启动
INFO:     🌐 WebSocket 服务: ws://localhost:8000/ws/overlay
```

### 步骤 4: 启动前端开发服务器（新终端）

```bash
cd frontend
npm run dev
```

**输出应该包含**:
```
VITE v5.0.0 ready in xxx ms
➜  Local:   http://localhost:5173/
```

### 步骤 5: 在浏览器中打开

访问: **http://localhost:5173**

你应该看到：
- 粉红色圆形宝宝在右下角
- 左上角状态指示器显示 "已连接"
- 全屏 Overlay 边框（绿色安全状态）

## 🎮 交互测试

### 在后端测试 Overlay 更新

```bash
# 终端 3 - 使用 curl 测试
curl -X POST http://localhost:8000/api/overlay/level?level=warning

# 观察前端：Overlay 应该变成橙色，强度增加
# 再试：
curl -X POST http://localhost:8000/api/overlay/level?level=danger

# 观察前端：Overlay 应该变成红色，脉冲强烈
```

### 让宝宝说话

```bash
curl -X POST http://localhost:8000/api/baobao/speak \
  -H "Content-Type: application/json" \
  -d '{"message":"你好，我是宝宝！"}'
```

## 📊 API 文档

### WebSocket 连接

**地址**: `ws://localhost:8000/ws/overlay`

**客户端消息格式**:
```json
{
  "level": "danger"  // safe | warning | danger
}
```

**服务器响应格式**:
```json
{
  "type": "overlay",
  "payload": {
    "level": "danger",
    "color": "#FF0000",
    "intensity": 0.3,
    "timestamp": "2026-06-04T08:00:00"
  }
}
```

### REST API

#### 健康检查
```bash
GET /health
```

#### 设置 Overlay 层级
```bash
POST /api/overlay/level?level=danger
```

#### 宝宝说话
```bash
POST /api/baobao/speak
{
  "message": "要说的话",
  "emotion": "happy",  // happy | warning | sad
  "duration": 3000
}
```

#### 获取统计信息
```bash
GET /api/stats
```

## 🎨 自定义和扩展

### 改变宝宝颜色

编辑 `frontend/src/components/Baobao.tsx`:
```typescript
background: 'radial-gradient(circle at 30% 30%, #FFE4E1, #FFB6C1)',  // 修改这里
```

### 改变动画速度

编辑 `frontend/src/styles/animations.css`:
```css
@keyframes baobao-breathing {
  /* 修改时间参数，例如从 3s 改为 2s */
}
```

### 添加新的 API 端点

编辑 `backend/app/main.py`:
```python
@app.post("/api/your-endpoint")
async def your_endpoint(param: str):
    # 你的逻辑
    return {"status": "ok"}
```

## 🔧 打包为桌面应用

### 打包 Electron 应用

```bash
cd frontend
npm run electron:build
```

输出文件位置：
- **macOS**: `dist/宝宝守护助手.dmg`
- **Windows**: `dist/宝宝守护助手.exe`

## 📈 性能目标

| 指标 | 目标 | 状态 |
|------|------|------|
| CPU 占用（待机） | < 5% | ✅ |
| CPU 占用（活跃） | < 15% | ✅ |
| 内存占用 | < 150MB | ✅ |
| 启动时间 | < 2s | ✅ |
| FPS | 60 | ✅ |

## 🐛 故障排除

### WebSocket 连接失败

**问题**: 前端显示 "离线"

**解决**:
1. 确保后端在运行：`python -m uvicorn app.main:app --reload`
2. 检查端口 8000 是否被占用：`lsof -i :8000`
3. 检查防火墙设置

### 宝宝不显示

**问题**: 看不到右下角的宝宝

**解决**:
1. 打开浏览器开发者工具 (F12)
2. 检查 Console 中是否有错误
3. 确保 React 组件正确加载

### Overlay 不更新

**问题**: 改变 Overlay 层级但前端不变

**解决**:
1. 检查 WebSocket 是否连接 (应该显示 "已连接")
2. 检查浏览器开发者工具的 Network 标签中的 WS 连接
3. 尝试手动刷新页面

## 📚 学习资源

- [React 官方文档](https://react.dev)
- [Electron 官方文档](https://www.electronjs.org/docs)
- [Three.js 官方文档](https://threejs.org)
- [FastAPI 官方文档](https://fastapi.tiangolo.com)

## 🎯 下一步计划

- [ ] VR 模式支持 (Meta Quest 3)
- [ ] 语音识别和 TTS
- [ ] Notion 集成
- [ ] 主题定制系统
- [ ] 本地化（多语言）
- [ ] 自动更新机制

## 📝 许可证

Proprietary - 龍魂系统内部使用

## 👥 贡献者

**UID9622 · 诸葛鑫 · 龍芯北辰**

---

**理论指导**: 曾仕强老师（永恒显示）

**DNA**:#龍芯⚡️2026-06-04-BAOBAO-MVP-v1.0

**状态**: 🟢 MVP 就绪 · 可投入使用
