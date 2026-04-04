# GitCode & AtomGit 仓库创建指南

## 🔐 您的令牌
```
dAzAuJVzVFFZdntizR_cp7d7
```

## 📋 快速创建步骤

### 1. GitCode 平台
1. **访问**: https://gitcode.com
2. **登录**: 使用您的账户登录
3. **创建仓库**:
   - 点击右上角 "+" → "新建仓库"
   - 仓库名称: `ecny-global-system`
   - 描述: `ECNY数字货币全球系统 - 基于易经八卦架构的区块链金融平台`
   - 选择: `公开仓库`
   - ✅ 不要勾选"添加README.md"（我们已有完整代码）
   - 点击"创建"

### 2. AtomGit 平台
1. **访问**: https://atomgit.com
2. **登录**: 使用您的账户登录
3. **创建仓库**:
   - 点击 "+" → "新建仓库"
   - 仓库名称: `ecny-global-system`
   - 描述: `ECNY数字货币全球系统 - 甲骨文血脉安全锁 + 量子加密`
   - 选择: `公开仓库`
   - ✅ 不要添加初始文件
   - 点击"创建"

## 🚀 创建完成后推送

仓库创建完成后，运行自动推送脚本：

```bash
/Users/zuimeidedeyihan/LuckyCommandCenter/deploy-to-platforms.sh
```

或手动执行：

```bash
cd /Users/zuimeidedeyihan/LuckyCommandCenter/ecny-global-system

# 推送到 GitCode
git push gitcode main

# 推送到 AtomGit  
git push atomgit main
```

## 🔑 SSH 密钥配置（可选提高安全性）

如果需要使用SSH而非令牌，请将以下公钥添加到两个平台：

```bash
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCwTJkS4c1Cmsm1s2ciGZWSOyP1SxNugMN4tup5u8PKc8bnarmAXsSg9awR6omP7L810GMVKmI5enQIzneFQVV8xXR/L0GNtYFBWJx0loVTpfOxpIWOEAZvzadOk11lR7vPmPYIo4hnDswskxTyXTTGqC9E6FI/Dpt/Xt2puAiKGJy9NS1ULq1RblVU8gUXCV3zNyvqR0INGFLDxqi8UriBrrv/D8tOmgRNYsfgx3EnOniCmmR3JWy8eMqFH03u//w4SYWID88sK5v3dCI5nsyUvlh4Ye6wqPh3E1PfW7IGIz51YY2gHxUcXrrT3xBBy04AWIAT9wAVD66I3HlBaiv7mGOS8om1enNzOE1xVFtGJWgBLqMIsAaVKJuQCPM3zDw/fAtLD4LEWLRfIH1snFJ4/pAjU3kzY3egEhBtvy4FS1K1KeUET0Nc7xyjlhpbP6O9+7NZuH7jCH22VcjKvfvx+keNaGP4MoM1oKCDHh3WPBmx65ktQQuFYwREK465LY4zPvkkuaegbdFEcQrkLTfxO1uJjG8DFskoMY8Ry3lui1nOh+eqvJU5iL3ylugqxVGmrsGrS/oJUYvZl09MSeYDRN8Af5gCCgsYVwU5n+RiHF8tJhQtWiCeKVg+gN6i/4ACCcv8KsoBWOHi2za4bTNQoSCJFzRUTAlE3n71vqnmEw== lucky@uid9622.tech
```

## ✅ 验证发布

推送成功后，您的项目将在：
- GitCode: https://gitcode.com/uid9622/ecny-global-system
- AtomGit: https://atomgit.com/uid9622/ecny-global-system

## 📊 项目特性

🔐 **安全特性**:
- 甲骨文血脉安全锁系统
- 生物识别认证
- 量子加密算法
- RSA-4096位GPG签名

🏗️ **技术架构**:
- 前端: React + TypeScript + Ant Design
- 后端: FastAPI + Python  
- 八卦战略架构（乾坤震巽坎离艮兑）
- Docker容器化部署

📋 **核心功能**:
- 多国家数字货币接入
- 实时汇率监控
- 风险评估系统
- 龍魂数字身份认证

---
🔐 **签名**: 诸葛鑫 <uid9622@petalmail.com>  
📅 **创建时间**: 2025-12-22  
🌐 **项目**: ECNY Global Digital Currency System