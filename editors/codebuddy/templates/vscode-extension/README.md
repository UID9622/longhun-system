# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 VS Code 扩展 · 标准模板

> 所有龍魂 VS Code 扩展必须按此模板结构创建
> DNA: `#龍芯⚡️丙午·辛未·VSCE-TEMPLATE-v1.0`

## 目录结构

```
longhun-{name}/
├── package.json          # 核心元数据（按模板填）
├── README.md             # 功能说明（按模板填）
├── CHANGELOG.md          # 更新日志
├── tsconfig.json         # TypeScript 配置
├── .vscodeignore         # 打包排除
├── LICENSE               # CC-BY-NC-SA-4.0
├── CONTRIBUTORS.md       # 贡献者
├── CONTRIBUTING.md       # 贡献指南
├── images/
│   ├── icon.png          # 128x128 龍魂红 #c41e3a
│   ├── icon.svg          # 矢量图标
│   └── badge-*.png       # 徽章
├── src/
│   └── extension.ts      # 扩展入口
└── out/
    └── extension.js      # 编译输出
```

## package.json 必填字段清单

| 字段 | 类型 | 必须 | 说明 |
|------|------|:---:|------|
| `name` | string | ✅ | `longhun-{功能}` 格式 |
| `displayName` | string | ✅ | 龍魂开头，中文 |
| `description` | string | ✅ | 一句话功能，中英文皆可 |
| `version` | string | ✅ | 语义版本 `x.y.z` |
| `publisher` | string | ✅ | 固定 `uid9622` |
| `icon` | string | ✅ | `images/icon.png` |
| `engines.vscode` | string | ✅ | `^1.80.0` |
| `categories` | array | ✅ | `["Other", "SCM"/"Linters"/...]` |
| `activationEvents` | array | ✅ | 至少 `onStartupFinished` |
| `main` | string | ✅ | `./out/extension.js` |
| `contributes.commands` | array | ✅ | 至少 1 个命令 |
| `keywords` | array | ✅ | 龍魂, longhun, CNSH, uid9622 |
| `repository` | object | ✅ | GitHub 仓库地址 |
| `license` | string | ✅ | CC-BY-NC-SA-4.0 |
| `galleryBanner` | object | ✅ | 暗色主题 `#0a0514` |

## 快速创建新扩展

```bash
# 从模板生成新扩展
cd editors/codebuddy/
cp -r templates/vscode-extension longhun-NEW-NAME
cd longhun-NEW-NAME

# 替换占位符
NAME="新扩展名称"
DIR="longhun-new-dir"
sed -i '' "s/EXTENSION-NAME/NEW-NAME/g" package.json
sed -i '' "s/EXTENSION-DIR/NEW-DIR/g" package.json
sed -i '' "s/龍魂扩展名/龍魂${NAME}/g" package.json
sed -i '' "s/EXTENSION-NAME/NEW-NAME/g" README.md
sed -i '' "s/龍魂\[扩展名\]/龍魂${NAME}/g" README.md

# 安装依赖
npm install

# 编译
npm run compile

# 打包 VSIX
npx vsce package --out ../dist/
```

## 打包 & 安装

```bash
# 打包单个
cd longhun-xxx && npx vsce package --out ../dist/

# 批量打包
cd editors/codebuddy/
for dir in longhun-*/; do
  cd "$dir" && npx vsce package --out ../dist/ && cd ..
done

# 安装
code --install-extension dist/longhun-xxx-1.0.0.vsix
```

## 设计规范

| 项目 | 值 |
|------|-----|
| 主色 | 龍魂金 `#D4AF37` |
| 辅助色 | 龍魂红 `#c41e3a` |
| 背景色 | 龍魂暗 `#0a0514` |
| 图标尺寸 | 128x128 PNG |
| 图标风格 | 龍纹+主题符号 |
| 命令前缀 | `龍魂: ` |
| 命令ID前缀 | `longhun-{ext}:` |
