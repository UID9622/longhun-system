# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 CNSH 剪贴板翻译 · 跨平台方案总览

> DNA: `#龍芯⚡️丙午·乙未·癸未·戊午·䷖剥-CLIPBOARD-CROSS-PLATFORM-v2.0`
> 一套API后端 + 多平台薄客户端 = 复制粘贴→CNSH翻译→DNA注入→锁定
> **v2.0**: 鸿蒙端按[鸿蒙API交付标准模板](../../knowledge/device-ecosystem/鸿蒙API交付标准模板_v1.0.md)重写，权限+错误处理+动态地址+设备适配全覆盖

---

## 架构

```
                    ┌─────────────────────┐
                    │   CNSH翻译API后端     │
                    │   /api/cnsh/         │
                    │   clipboard-translate │
                    │   clipboard-verify    │
                    └────────┬────────────┘
                             │ HTTP/JSON
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼─────┐      ┌──────▼──────┐      ┌─────▼──────┐
    │ iOS      │      │ PWA (通用)   │      │ 鸿蒙        │
    │ 快捷指令  │      │ 浏览器即可   │      │ 原子化服务   │
    └──────────┘      └─────────────┘      └────────────┘
```

---

## 各平台实现

| 平台 | 文件 | 方式 | 触发方式 |
|------|------|------|---------|
| **iOS 14+** | `ios_shortcut_guide.md` | 快捷指令 | 主屏幕/共享表单/轻点背面/Siri |
| **PWA 通用** | `clipboard_pwa.html` | 浏览器PWA | 添加到主屏幕→即点即用 |
| **鸿蒙 3.0+** | `harmonyos_clipboard_cnsh.md` | 原子化服务卡片 | 桌面卡片/全局搜索/负一屏 |
| **华为/荣耀** | 同上 | 快应用 | 即点即用 |
| **Mac** | 快捷指令同步 | Menu Bar | 右键→服务→CNSH翻译 |
| **统信UOS** | 待开发 | 系统托盘 | 全局快捷键 Ctrl+Shift+C |
| **深度OS** | 待开发 | Deepin Widget | 侧边栏小组件 |
| **所有国产系统** | 通用 | 调用API | HTTP POST |

---

## API端点

### POST `/api/cnsh/clipboard-translate`

```json
// 请求
{"text": "如果用户已登录则显示主界面", "parent_dna": ""}

// 响应
{
  "状态": "success",
  "DNA": "#龍芯⚡️丙午·乙未·癸未·戊午·䷖剥-CLIPBOARD-A3F2B8E1",
  "时间戳": {"ISO8601": "2026-07-08T03:15:22+00:00", "北京时间": "2026-07-08 11:15:22 CST", "Unix": 1752018922, "锁定": true},
  "内容指纹": "sha256...",
  "CNSH关键字": [{"关键字": "如果", "英文": "if", "类别": "控制流"}],
  "完整性哈希": "sha256...",
  "完整性组件": {...},
  "原文": "...",
  "CNSH标注": "  ┃ 如果 → if  [控制流]",
  "验证指令": "python3 bin/lh_anti_tamper.py verify --dna ..."
}
```

### POST `/api/cnsh/clipboard-verify`

```json
// 请求
{"完整性组件": {...}}

// 响应
{"状态": "success", "完整": true, "说明": "✅ 所有组件完好·完整性验证通过"}
```

---

## 使用流程

```
用户复制任意文本
    ↓
触发平台客户端（快捷指令/PWA/服务卡片）
    ↓
客户端调用 /api/cnsh/clipboard-translate
    ↓
返回: DNA码 + 时间戳锁定 + CNSH关键字检测 + 完整性哈希
    ↓
自动复制DNA到剪贴板 / 展示翻译结果
    ↓
随时可调 verify API 验证完整性
```

---

## "少一样不能用"机制

翻译产物包含6个强制组件：

| 组件 | 说明 | 缺失后果 |
|------|------|---------|
| DNA码 | 追溯标识 | 无法追溯来源 |
| 时间戳 | 锁定时间 | 无法知道何时翻译 |
| 内容指纹 | SHA-256 | 原文被篡改无法发现 |
| CNSH关键字 | 语法标记 | 翻译不可用 |
| 父DNA链 | 协作链 | 无法链式验证 |
| 完整性哈希 | 覆盖全部 | **任意缺失→哈希断裂→不可使用** |

完整性哈希 = SHA-256(所有组件按key排序后JSON序列化)。取走任何组件、改任何一个字符，哈希都会变。

---

## 部署

API已在 `main.py` 中，随龍魂操作台一起启动：

```bash
cd L5_服务层/services/api/control-panel
python3 main.py  # 启动在 :9622
```

PWA静态页面部署在 `dashboard/web/p0-controls/`，由操作台的HTTP服务器托管。

如需公网访问，配置Nginx反代：
```nginx
location /api/cnsh/clipboard-translate {
    proxy_pass http://127.0.0.1:9622;
}
```
