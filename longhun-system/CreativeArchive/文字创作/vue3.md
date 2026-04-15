# Vue3 Internationalization Guide

Complete guide for implementing i18n in Vue3 applications using vue-i18n@9.

## Table of Contents

- [Installation](#installation)
- [Basic Setup](#basic-setup)
- [Composition API Usage](#composition-api-usage)
- [Options API Usage](#options-api-usage)
- [Template Usage](#template-usage)
- [Advanced Features](#advanced-features)
- [Lazy Loading](#lazy-loading)
- [Common Patterns](#common-patterns)

## Installation

```bash
npm install vue-i18n@latest
```

## Basic Setup

### Create i18n Instance

```javascript
// src/i18n/index.js
import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import zh from './locales/zh.json'

const i18n = createI18n({
  legacy: false, // Use Composition API mode
  locale: localStorage.getItem('locale') || 'en',
  fallbackLocale: 'en',
  messages: {
    en,
    zh
  },
  numberFormats: {
    en: {
      currency: {
        style: 'currency',
        currency: 'USD'
      }
    },
    zh: {
      currency: {
        style: 'currency',
        currency: 'CNY'
      }
    }
  },
  dateTimeFormats: {
    en: {
      short: {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      }
    },
    zh: {
      short: {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      }
    }
  }
})

export default i18n
```

### Register in App

```javascript
// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import i18n from './i18n'

const app = createApp(App)
app.use(i18n)
app.mount('#app')
```

## Composition API Usage

```vue
<script setup>
import { useI18n } from 'vue-i18n'

const { t, d, n, locale, availableLocales } = useI18n()

// Simple translation
const message = t('welcome')

// Translation with interpolation
const greeting = t('greeting', { name: 'John' })

// Date formatting
const formattedDate = d(new Date(), 'short')

// Number formatting
const price = n(99.99, 'currency')

// Change locale
const changeLanguage = (lang) => {
  locale.value = lang
  localStorage.setItem('locale', lang)
}

// Check available locales
console.log(availableLocales) // ['en', 'zh']
</script>
```

## Options API Usage

```vue
<script>
export default {
  computed: {
    // Access through $i18n
    currentLocale() {
      return this.$i18n.locale
    }
  },
  methods: {
    translate(key, params) {
      return this.$t(key, params)
    },
    changeLanguage(lang) {
      this.$i18n.locale = lang
    }
  }
}
</script>
```

## Template Usage

### Basic Translation

```vue
<template>
  <!-- Simple -->
  <h1>{{ $t('welcome') }}</h1>

  <!-- With interpolation -->
  <p>{{ $t('greeting', { name: userName }) }}</p>

  <!-- Pluralization -->
  <p>{{ $tn('apple', count, count) }}</p>

  <!-- Date formatting -->
  <span>{{ $d(new Date(), 'short') }}</span>

  <!-- Number formatting -->
  <span>{{ $n(price, 'currency') }}</span>
</template>
```

### v-t Directive

```vue
<template>
  <!-- Attribute binding -->
  <input v-t="{ path: 'placeholder.name' }" placeholder="" />

  <!-- With arguments -->
  <p v-t="{ path: 'message', args: { name: user.name } }"></p>
</template>
```

### Conditional Translation

```vue
<template>
  <div v-if="$i18n.locale === 'en'">
    <img src="/images/logo-en.png" alt="Logo">
  </div>
  <div v-else>
    <img src="/images/logo-zh.png" alt="Logo">
  </div>
</template>
```

## Advanced Features

### Pluralization

```json
// locales/en.json
{
  "apple": "no apples | one apple | {count} apples",
  "car": "no cars | one car | {count} cars"
}
```

```vue
<script setup>
import { useI18n } from 'vue-i18n'

const { tn } = useI18n()
const appleCount = ref(5)
const appleText = computed(() => tn('apple', appleCount.value, appleCount.value))
</script>
```

### Named Interpolation

```json
{
  "user_profile": "Profile of {name}, age {age}"
}
```

```vue
<script setup>
const { t } = useI18n()
const profile = t('user_profile', { name: 'Alice', age: 30 })
</script>
```

### List Interpolation

```json
{
  "items_list": "Items: {0}, {1}, and {2}"
}
```

```vue
<script setup>
const { t } = useI18n()
const list = t('items_list', ['Apple', 'Banana', 'Orange'])
</script>
```

### Rich Text/HTML

```vue
<template>
  <!-- Using v-html with caution -->
  <p v-html="$t('rich_content')"></p>
</template>

<script setup>
// Or use component-based approach
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const richContent = t('rich_content', {
  link: (text) => `<a href="/about">${text}</a>`
})
</script>
```

### Linked Messages

```json
{
  "message": "Hello!",
  "linked": "@:message"
}
```

## Lazy Loading

```javascript
// src/i18n/index.js
import { createI18n } from 'vue-i18n'

export const setupI18n = async () => {
  const locale = localStorage.getItem('locale') || 'en'

  const i18n = createI18n({
    legacy: false,
    locale: locale,
    fallbackLocale: 'en',
    messages: {
      en: await loadLocaleMessages('en'),
      [locale]: await loadLocaleMessages(locale)
    }
  })

  return i18n
}

async function loadLocaleMessages(locale) {
  if (locale === 'en') {
    return (await import('./locales/en.json')).default
  }
  return (await import(`./locales/${locale}.json`)).default
}

// In main.js
import { setupI18n } from './i18n'

setupI18n().then(i18n => {
  app.use(i18n)
  app.mount('#app')
})
```

### Dynamic Locale Switching

```vue
<script setup>
import { useI18n } from 'vue-i18n'

const { locale, loadLocaleMessages } = useI18n()

const changeLanguage = async (newLocale) => {
  // Load locale messages if not loaded
  if (!i18n.global.availableLocales.includes(newLocale)) {
    const messages = await import(`./locales/${newLocale}.json`)
    i18n.global.setLocaleMessage(newLocale, messages.default)
  }

  locale.value = newLocale
  localStorage.setItem('locale', newLocale)
}
</script>
```

## Common Patterns

### Feature-Based Namespace Structure

```
src/
├── i18n/
│   ├── index.js
│   └── locales/
│       ├── en.json
│       │   ├── common.json
│       │   ├── auth.json
│       │   ├── dashboard.json
│       │   └── settings.json
│       └── zh.json
│           ├── common.json
│           ├── auth.json
│           ├── dashboard.json
│       │   └── settings.json
```

### Shared Translations

```javascript
// src/i18n/index.js
import { createI18n } from 'vue-i18n'
import common from './locales/en/common.json'
import auth from './locales/en/auth.json'

const messages = {
  en: {
    common,
    auth
  }
}
```

```vue
<!-- Usage -->
<template>
  <button>{{ $t('common.save') }}</button>
  <button>{{ $t('auth.login') }}</button>
</template>
```

### Translation Function Wrapper

```javascript
// src/utils/i18n.js
import { i18n } from '@/i18n'

export const t = (key, params) => i18n.global.t(key, params)
export const d = (value, format) => i18n.global.d(value, format)
export const n = (value, format) => i18n.global.n(value, format)
```

### Validation with i18n

```javascript
// src/validations.js
import { t } from '@/utils/i18n'

export const required = (value) => {
  return !!value || t('validations.required')
}

export const email = (value) => {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return pattern.test(value) || t('validations.email')
}
```

### Route Meta with Translations

```javascript
// router/index.js
const routes = [
  {
    path: '/dashboard',
    name: 'dashboard',
    meta: {
      titleKey: 'routes.dashboard'
    }
  }
]

// In navigation component
<template>
  <router-link to="/dashboard">
    {{ $t($route.meta.titleKey) }}
  </router-link>
</template>
```

## Error Handling

### Missing Translation Handler

```javascript
const i18n = createI18n({
  missing: (locale, key) => {
    console.warn(`[i18n] Missing translation: ${key} for locale: ${locale}`)
    return key
  },
  fallbackRoot: true
})
```

### Translation Key Validation

```javascript
// src/utils/i18n-validator.js
import { i18n } from '@/i18n'

export function hasTranslation(key, locale = i18n.global.locale) {
  return i18n.global.te(key, locale)
}

// Usage
if (!hasTranslation('some.key')) {
  console.warn('Translation key missing')
}
```
