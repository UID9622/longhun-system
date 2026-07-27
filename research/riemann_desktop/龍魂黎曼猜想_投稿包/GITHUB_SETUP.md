# GitHub 仓库发布步骤

本文件说明如何将这个投稿包发布为一个 GitHub 仓库。

## 第一步：在 GitHub 上创建仓库

1. 打开 https://github.com/new
2. 仓库名称建议：`riemann-hypothesis-dragonhood-framework`
3. 选择 **Public**（公开）或 **Private**（私有）
4. 不要勾选 "Initialize this repository with a README"（因为本文件夹已有 README.md）
5. 点击 **Create repository**

## 第二步：本地推送到 GitHub

在终端中执行：

```bash
cd "/Users/zuimeidedeyihan/Desktop/龍魂黎曼猜想_投稿包"
git init
git add .
git commit -m "Initial commit: 龍魂视角下的黎曼猜想观察性框架"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/riemann-hypothesis-dragonhood-framework.git
git push -u origin main
```

将 `YOUR_USERNAME` 替换为您的 GitHub 用户名。

## 第三步：完善仓库信息

1. 在 GitHub 仓库页面，点击右上角 **About** 旁边的齿轮图标
2. 添加描述：`An observational framework for the Riemann Hypothesis from a Dragonhood perspective.`
3. 添加 Topics：`riemann-hypothesis`, `number-theory`, `observational-framework`, `chinese-philosophy`
4. 保存

## 第四步：发布 Release（可选）

1. 在 GitHub 仓库页面，点击右侧 **Releases**
2. 点击 **Create a new release**
3. Tag version：`v1.0.0`
4. Release title：`Initial Release`
5. 内容可以复制 README 的摘要部分
6. 点击 **Publish release**

## 注意事项

- 请使用您自己的 GitHub 账号发布，不要用他人账号或假账号。
- 本仓库内容采用 CC BY-NC-SA 4.0 许可证，禁止商业用途。
- 对外宣传时，请始终说明这是"观察性框架"，不是证明。
