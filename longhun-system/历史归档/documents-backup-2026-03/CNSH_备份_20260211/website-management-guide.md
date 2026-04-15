# CNSH 公开页面管理指南

## 概述

本文档提供了 CNSH 公开页面的管理和更新指南，确保网站内容与系统功能保持同步。

## 主要组件

### 1. 龍魂网站 (dragon-soul-website)
- **位置**: `/dragon-soul-website/`
- **功能**: 主要展示页面，展示龍文化及 CNSH 系统
- **主要文件**:
  - `index.html`: 主页面结构
  - `script.js`: 交互功能和动画
  - `styles.css`: 样式和响应式设计

### 2. CNSH 系统 (cnsh-deployment)
- **位置**: `/cnsh-deployment/`
- **功能**: 后端服务和 API 接口
- **主要模块**:
  - 数字身份系统 (`src/config/digital-identity.js`)
  - 激活服务 (`src/services/activationService.js`)
  - 市场系统 (`src/routes/marketplace.js`)
  - 支付系统 (`src/routes/payment.js`)

## 更新流程

### 自动化更新
使用提供的 `update-website.sh` 脚本一键更新所有内容:

```bash
./update-website.sh
```

该脚本将:
1. 提交网站更新
2. 推送到远程仓库
3. 更新后端服务配置
4. 推送后端服务更新

### 手动更新步骤

#### 1. 更新网站内容
```bash
cd dragon-soul-website
git add .
git commit -m "更新网站内容"
git push origin main
```

#### 2. 更新后端服务
```bash
cd cnsh-deployment
git add .
git commit -m "更新后端服务"
git push origin main
```

## 内容管理指南

### 1. 统一邮箱
- 所有联系邮箱统一为: `uid9622@petalmail.com`
- 使用 `email_manager.sh` 脚本快速配置

### 2. CNSH 系统展示
- 网站已整合 CNSH 系统功能展示
- 点击 "CNSH系统" 链接可查看系统功能模态框

### 3. 文档同步
- 确保网站内容与最新文档同步
- 重要更新参考 `cnsh-public-pages-overview.md`

## 设计原则

### 1. 视觉一致性
- 保持龍魂主题色彩: 红色(#c41e3a)、深蓝(#1a365d)、金色(#f6d55c)
- 使用中文字体优先，增强文化认同感

### 2. 用户体验
- 简洁直观的导航
- 流畅的动画和过渡效果
- 响应式设计，适配各种设备

### 3. 内容整合
- 展示 CNSH 核心理念
- 整合系统功能展示
- 提供清晰的联系方式

## 维护计划

### 1. 定期更新
- 每月检查一次内容同步状态
- 季度评估用户反馈和体验
- 年度更新设计和技术栈

### 2. 监控指标
- 网站访问量和用户停留时间
- 系统功能使用情况
- 用户反馈和问题

### 3. 改进方向
- 添加更多系统交互功能
- 优化移动端体验
- 增加多语言支持可能性

## 联系信息

如有任何问题或建议，请通过以下方式联系:
- 邮箱: uid9622@petalmail.com
- 开源项目: https://gitee.com/uid9622/cnsh-framework

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-3072c30c-20251218032410
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 屯卦：云雷屯，君子以经纶
📜 内容哈希: 16755ecb52db011f
⚠️ 警告: 未经授权修改将触发DNA追溯系统
