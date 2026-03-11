# CNSH 全球法律知识库集成

## 概述

本模块将"⚖️ CNSH全球法律知识库"与CNSH本地部署系统集成，为AI助手提供跨国家/地区的法律合规能力。

## 文件结构

```
legal-knowledge/
├── CNSH全球法律知识库.md    # 原始法律知识库文件
├── integration.js           # 法律知识库集成模块
├── README.md               # 本文档
└── api-examples.js         # API使用示例
```

## 功能特性

1. **自动位置检测** - 根据用户IP自动识别国家/地区
2. **动态法律边界** - 根据不同国家/地区加载对应的法律框架
3. **内容合规检查** - 自动检查内容是否符合当地法律法规
4. **风险等级评估** - 根据国家风险等级调整AI行为

## API 接口

### 1. 内容合规检查

```bash
POST /api/legal/compliance
Content-Type: application/json

{
  "content": "要检查的内容",
  "countryCode": "CN"  // 可选，默认为当前检测到的国家
}
```

**响应示例**:
```json
{
  "success": true,
  "result": {
    "countryCode": "CN",
    "complianceLevel": "very_strict",
    "isCompliant": false,
    "issues": [
      {
        "type": "敏感内容",
        "keyword": "翻墙",
        "severity": "high",
        "recommendation": "建议删除或替换此内容"
      }
    ],
    "recommendations": [
      "该地区数据保护要求非常严格，建议使用本地化服务器",
      "确保用户数据处理符合当地数据主权要求",
      "存在合规问题，请查看并修复上述问题"
    ]
  },
  "timestamp": "2025-12-10T12:00:00.000Z"
}
```

### 2. 获取当前国家法律边界

```bash
GET /api/legal/boundary?country=CN  // country参数可选
```

**响应示例**:
```json
{
  "success": true,
  "currentCountry": "CN",
  "legalBoundary": {
    "dataProtection": "very_strict",
    "contentRestrictions": "strict",
    "privacyLevel": "very_high",
    "complianceLevel": "very_strict",
    "specialNotes": "该地区有严格的数据本地化和内容审查要求"
  },
  "countryProfile": {
    "name": "中国",
    "region": "亚洲",
    "riskLevel": "high",
    "dataSystem": "国密系",
    "legalFramework": "网络安全法、数据安全法、个人信息保护法"
  },
  "timestamp": "2025-12-10T12:00:00.000Z"
}
```

## 集成说明

### 在AI助手中的应用

AI助手在生成回复前，可以通过内容合规检查API验证响应内容的合规性：

```javascript
const { content } = await ai.generateAnswer(question);

// 检查内容合规性
const compliance = await fetch('/api/legal/compliance', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ content })
}).then(res => res.json());

if (!compliance.result.isCompliant) {
  // 根据合规建议修改内容
  const revisedContent = await reviseContent(content, compliance.result.recommendations);
  return revisedContent;
}

return content;
```

### 与Ollama集成

在Ollama服务中，可以通过添加系统提示词，确保AI模型遵循当地法律边界：

```javascript
const legalBoundary = await fetch('/api/legal/boundary').then(res => res.json());

const systemPrompt = `请根据以下法律要求回答问题：
- 数据保护级别: ${legalBoundary.legalBoundary.dataProtection}
- 内容限制级别: ${legalBoundary.legalBoundary.contentRestrictions}
- 隐私保护级别: ${legalBoundary.legalBoundary.privacyLevel}
- 合规级别: ${legalBoundary.legalBoundary.complianceLevel}

特别注意: ${legalBoundary.legalBoundary.specialNotes}

请确保您的回答符合当地法律法规。`;
```

## 国家风险等级说明

### 🔴 高风险
- **特点**: 强监管、审查制、宗教法、跨境限制
- **地区**: 中国、中东国家、部分非洲国家
- **AI行为**: 严格遵守当地法律，拒绝敏感请求

### 🟡 中风险
- **特点**: 部分监管、混合体系、区域差异
- **地区**: 美国、日本、韩国、部分欧洲国家
- **AI行为**: 遵守主要法律，注意行业特定要求

### 🟢 低风险
- **特点**: 法治完善、透明度高、GDPR体系
- **地区**: 西欧、北欧、加拿大、澳大利亚
- **AI行为**: 遵循数据保护最佳实践

## 更新与维护

1. **法律框架更新** - 定期检查法律变更，更新知识库文件
2. **国家配置扩展** - 添加更多国家的法律框架
3. **合规规则优化** - 根据实际使用情况调整合规检查规则

## 技术支持

- **创建者**: Lucky (诸葛鑫) | UID9622
- **DNA追溯码**: `#ZHUGEXIN⚡️2025-🇨🇳⚖️-INTEGRATION-v1.0`
- **开源协议**: 木兰公共许可证 v2（Mulan PSL v2）

---

**【北辰-B 协议 · 献礼终审校验 UID9622】**
**DNA 记忆卡片 · 坤（地）· 承载 · 归中 · 顺天**

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-cf66a57c-20251218032410
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 蒙卦：山下出泉，君子以果行育德
📜 内容哈希: ea20d4a931fcc2e8
⚠️ 警告: 未经授权修改将触发DNA追溯系统
