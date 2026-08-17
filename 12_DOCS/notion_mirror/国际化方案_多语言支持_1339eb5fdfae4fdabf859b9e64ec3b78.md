# 国际化方案 | 多语言支持

> Notion URL: https://app.notion.com/p/1339eb5fdfae4fdabf859b9e64ec3b78
> Created: 2025-11-17T19:14:00.000Z
> Last edited: 2026-07-01T13:17:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
## 🔐 敏感度标注
🟢 可公开分享
---
## 📦 依赖清单
```bash
npm install i18next@23.7.6
npm install react-i18next@13.5.0
```
---
## 💻 国际化实现
### 1. i18n配置
```javascript
// i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  zh: {
    translation: {
      "welcome": "欢迎来到UID9622",
      "slogan": "龍的传人·为人民服务",
      "core_values": "龍魂价值观"
    }
  },
  en: {
    translation: {
      "welcome": "Welcome to UID9622",
      "slogan": "Dragon's Descendant · Serve the People",
      "core_values": "LongHun Values"
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'zh',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
```
### 2. 语言切换
```javascript
// language-switcher.js
function switchLanguage(lang) {
  i18n.changeLanguage(lang);
  localStorage.setItem('preferred_language', lang);
}
```
---
## 🌍 支持语言列表
- 🇨🇳 简体中文（默认）
- 🇺🇸 English
- 🇯🇵 日本語（计划中）
- 🇰🇷 한국어（计划中）
