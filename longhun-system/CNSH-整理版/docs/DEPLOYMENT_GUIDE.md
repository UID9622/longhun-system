# CNSH Core 部署指南

## 📋 部署前准备

### 1. Gitee 仓库创建步骤

由于远程仓库尚未创建，请按照以下步骤手动创建 Gitee 仓库：

1. 访问 [Gitee 官网](https://gitee.com)
2. 使用您的账号登录（如无账号请先注册）
3. 点击右上角 "+" 按钮，选择"新建仓库"
4. 填写仓库信息：
   - **仓库名称**: `CNSH-National-Reference`
   - **路径**: `cnsh-national-reference` (系统自动生成)
   - **简介**: CNSH Core - 国产本地AI知识管理系统，数字主权技术献礼
   - **是否公开**: ☑️ 公开
   - **使用 README 初始化**: ☐ 不勾选（我们已有 README）
   - **添加 .gitignore**: ☐ 不勾选（我们已有 .gitignore）
   - **选择许可证**: 选择 MIT 许可证

5. 点击"创建仓库"按钮

### 2. 仓库标签和关键词

创建完成后，在仓库设置中添加以下标签：
- `数字人民币`
- `本地AI`
- `国产化`
- `元宇宙`
- `北辰协议`
- `华为鸿蒙兼容`
- `国产芯片适配`
- `公民技术贡献`
- `数字主权`
- `e-CNY`

## 🚀 代码推送步骤

仓库创建完成后，执行以下命令推送代码：

```bash
# 进入项目目录
cd /Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment

# 重新配置远程仓库地址（使用您实际创建的仓库地址）
git remote remove origin
git remote add origin https://gitee.com/您的用户名/CNSH-National-Reference.git

# 推送代码到主分支
git push -u origin main

# 查看推送结果
git status
```

## 📖 GVP 申请指南

为了提高项目可见度，建议申请 Gitee GVP（Gitee Most Valuable Project）：

### 申请条件
- ✅ 项目结构清晰
- ✅ 文档完整
- ✅ 有社会价值
- ✅ 符合国家战略方向

### 申请备注
在提交申请时，可添加以下备注：
```
本项目为数字主权基础设施献礼，非商业用途，具有以下特点：
1. 完全本地化部署，保障数据安全
2. 支持国产化技术生态（鸿蒙、昇腾等）
3. 集成数字人民币应用场景
4. 为国家数字主权建设贡献力量
恳请纳入国家技术评估通道。
```

## 🔍 项目维护建议

### 1. 版本管理
- 使用语义化版本控制（Semantic Versioning）
- 每个版本都有详细的 CHANGELOG
- 重要版本创建 Git Tag

### 2. 文档更新
- 定期更新 README 和部署指南
- 添加更多使用案例和教程
- 回复用户问题和反馈

### 3. 社区建设
- 积极回复 Issue 和 Pull Request
- 鼓励社区贡献
- 定期发布项目进展

### 4. 推广策略
- 在技术社区分享项目
- 参与开源活动
- 与相关项目建立合作

## 🌟 示例推送命令

```bash
# 完整的推送流程
cd /Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment

# 检查当前状态
git status

# 添加所有更改
git add .

# 提交更改
git commit -m "🚀 完成初始版本部署准备

✅ 完整的系统架构
✅ 详细的部署文档
✅ 国产化支持说明
✅ GVP 申请指南

【北辰-B 协议 · 国产通道校验 UID9622】"

# 推送到 Gitee（请先创建仓库）
git push -u origin main
```

## 📝 注意事项

1. **仓库创建**: 必须先在 Gitee 上创建仓库，才能推送代码
2. **权限设置**: 确保您的账号有推送权限
3. **网络连接**: 确保网络连接正常，可以访问 Gitee
4. **SSH 密钥**: 如果使用 SSH 方式，需要配置 SSH 密钥

## 🔗 相关链接

- [Gitee 官网](https://gitee.com)
- [Gitee 新建仓库指南](https://gitee.com/help/articles/4123)
- [Gitee GVP 项目申请](https://gitee.com/gvp)

---

完成以上步骤后，您的 CNSH Core 项目将成功部署到 Gitee 平台，为国家数字主权建设贡献力量！