# React Internationalization Guide

Complete guide for implementing i18n in React applications using react-i18next.

## Table of Contents

- [Installation](#installation)
- [Basic Setup](#basic-setup)
- [Using the Hook](#using-the-hook)
- [Using the Trans Component](#using-the-trans-component)
- [Interpolation](#interpolation)
- [Plurals](#plurals)
- [Namespaces](#namespaces)
- [Advanced Features](#advanced-features)
- [Common Patterns](#common-patterns)

## Installation

```bash
npm install i18next react-i18next i18next-browser-languagedetector
```

## Basic Setup

### Initialize i18next

```javascript
// src/i18n/config.js
import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'
import en from './locales/en.json'
import zh from './locales/zh.json'

const resources = {
  en: {
    translation: en
  },
  zh: {
    translation: zh
  }
}

i18n
  .use(LanguageDetector) // Detect user language
  .use(initReactI18next) // Pass i18n instance to react-i18next
  .init({
    resources,
    fallbackLng: 'en',
    lng: localStorage.getItem('locale') || 'en',
    debug: false,
    interpolation: {
      escapeValue: false // React already escapes
    },
    detection: {
      order: ['localStorage', 'navigator'],
      caches: ['localStorage']
    }
  })

export default i18n
```

### Import in App Entry

```javascript
// src/index.js or src/main.jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './i18n/config' // Import i18n config

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

## Using the Hook

### Basic Usage

```jsx
import { useTranslation } from 'react-i18next'

function Greeting() {
  const { t, i18n } = useTranslation()

  return (
    <div>
      <h1>{t('welcome')}</h1>
      <button onClick={() => i18n.changeLanguage('zh')}>
        Switch to Chinese
      </button>
      <button onClick={() => i18n.changeLanguage('en')}>
        Switch to English
      </button>
    </div>
  )
}
```

### Access Current Language

```jsx
function LanguageInfo() {
  const { i18n } = useTranslation()

  return (
    <p>Current language: {i18n.language}</p>
  )
}
```

### Get All Available Languages

```jsx
function LanguageSelector() {
  const { i18n } = useTranslation()

  return (
    <select onChange={(e) => i18n.changeLanguage(e.target.value)}>
      {i18n.languages.map(lang => (
        <option key={lang} value={lang}>
          {lang.toUpperCase()}
        </option>
      ))}
    </select>
  )
}
```

## Using the Trans Component

The `<Trans>` component is useful for translations with HTML or React components:

```jsx
import { Trans } from 'react-i18next'

function Welcome() {
  return (
    <Trans i18nKey="welcome_message">
      Welcome to <strong>Our App</strong>, {{ name }}!
    </Trans>
  )
}
```

With translation:

```json
{
  "welcome_message": "Welcome to <1>Our App</1>, {{name}}!"
}
```

## Interpolation

### Basic Interpolation

```json
{
  "greeting": "Hello, {{name}}!",
  "order_summary": "You have {{count}} items in your cart"
}
```

```jsx
const { t } = useTranslation()
const greeting = t('greeting', { name: 'John' })
const summary = t('order_summary', { count: 5 })
```

### HTML in Interpolation

```jsx
function Profile() {
  const { t } = useTranslation()

  return (
    <Trans
      i18nKey="profile_link"
      components={[<a href="/profile" className="link" />]}
      values={{ name: 'John' }}
    >
      View <0>{{ name }}</0>'s profile
    </Trans>
  )
}
```

```json
{
  "profile_link": "View <0>{{ name }}</0>'s profile"
}
```

## Plurals

### Basic Pluralization

```json
{
  "apple_one": "one apple",
  "apple_other": "{{count}} apples"
}
```

```jsx
function FruitCounter({ count }) {
  const { t } = useTranslation()

  return (
    <p>{t('apple', { count })}</p>
  )
}
```

### Explicit Plural Keys

```json
{
  "item": "item",
  "item_plural": "items"
}
```

### Complex Plurals (with suffixes)

For languages with more complex plural rules:

```json
{
  "message": "You have {{count}} message",
  "message_plural": "You have {{count}} messages",
  "message_inclusive": "You have {{count}} messages (including this one)"
}
```

## Namespaces

### Multiple Namespaces

```javascript
// src/i18n/config.js
const resources = {
  en: {
    translation: require('./locales/en/translation.json'),
    common: require('./locales/en/common.json'),
    dashboard: require('./locales/en/dashboard.json')
  },
  zh: {
    translation: require('./locales/zh/translation.json'),
    common: require('./locales/zh/common.json'),
    dashboard: require('./locales/zh/dashboard.json')
  }
}
```

### Using Specific Namespace

```jsx
// Load specific namespace
function Dashboard() {
  const { t } = useTranslation('dashboard')

  return <h1>{t('title')}</h1>
}
```

```jsx
// Load multiple namespaces
function Dashboard() {
  const { t } = useTranslation(['dashboard', 'common'])

  return (
    <div>
      <h1>{t('dashboard:title')}</h1>
      <button>{t('common:save')}</button>
    </div>
  )
}
```

## Advanced Features

### Context

```json
{
  "friend": "A friend",
  "friend_male": "A boyfriend",
  "friend_female": "A girlfriend"
}
```

```jsx
function Friend({ gender }) {
  const { t } = useTranslation()

  return <p>{t('friend', { context: gender })}</p>
}
```

### Dates and Numbers

```jsx
import { useTranslation } from 'react-i18next'

function DateFormatter({ date }) {
  const { i18n } = useTranslation()

  const formatted = new Intl.DateTimeFormat(i18n.language, {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)

  return <span>{formatted}</span>
}

function Currency({ amount }) {
  const { i18n } = useTranslation()

  const formatted = new Intl.NumberFormat(i18n.language, {
    style: 'currency',
    currency: i18n.language === 'zh' ? 'CNY' : 'USD'
  }).format(amount)

  return <span>{formatted}</span>
}
```

### Lazy Loading Namespaces

```jsx
import { useTranslation } from 'react-i18next'

function Dashboard() {
  const { t, ready } = useTranslation('dashboard', { useSuspense: false })

  if (!ready) {
    return <div>Loading...</div>
  }

  return <h1>{t('title')}</h1>
}
```

### Custom Translation Function

```jsx
import { useTranslation } from 'react-i18next'

function useCustomTranslation() {
  const { t } = useTranslation()

  return {
    translateWithDefault: (key, defaultValue, params = {}) => {
      return t(key, params) || defaultValue
    }
  }
}

// Usage
function Component() {
  const { translateWithDefault } = useCustomTranslation()
  const text = translateWithDefault('missing.key', 'Default Text')
  return <p>{text}</p>
}
```

## Common Patterns

### Language Switcher Component

```jsx
import { useTranslation } from 'react-i18next'

function LanguageSwitcher() {
  const { i18n } = useTranslation()

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'zh', name: '中文' }
  ]

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng)
    localStorage.setItem('locale', lng)
  }

  return (
    <div className="language-switcher">
      {languages.map(lang => (
        <button
          key={lang.code}
          onClick={() => changeLanguage(lang.code)}
          className={i18n.language === lang.code ? 'active' : ''}
        >
          {lang.name}
        </button>
      ))}
    </div>
  )
}
```

### Form Validation with i18n

```jsx
import { useTranslation } from 'react-i18next'

function useFormValidation() {
  const { t } = useTranslation('validation')

  const validateEmail = (email) => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return pattern.test(email) ? null : t('errors.invalid_email')
  }

  const validateRequired = (value) => {
    return value ? null : t('errors.required')
  }

  return { validateEmail, validateRequired }
}

// Usage
function LoginForm() {
  const { t } = useTranslation()
  const { validateEmail, validateRequired } = useFormValidation()
  const [errors, setErrors] = useState({})

  const handleSubmit = (e) => {
    e.preventDefault()
    const emailError = validateEmail(email)
    const passwordError = validateRequired(password)

    setErrors({
      email: emailError,
      password: passwordError
    })
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" placeholder={t('email')} />
      {errors.email && <span className="error">{errors.email}</span>}
      <input type="password" placeholder={t('password')} />
      {errors.password && <span className="error">{errors.password}</span>}
    </form>
  )
}
```

### Route-Based Translations

```jsx
import { useTranslation } from 'react-i18next'

function Breadcrumbs({ routes }) {
  const { t } = useTranslation()

  return (
    <nav>
      {routes.map(route => (
        <span key={route.path}>
          {t(`routes.${route.name}`)}
        </span>
      ))}
    </nav>
  )
}
```

```json
{
  "routes": {
    "home": "Home",
    "dashboard": "Dashboard",
    "settings": "Settings"
  }
}
```

### Provider with Default Namespace

```jsx
import { I18nextProvider } from 'react-i18next'
import i18n from './i18n/config'

function App() {
  return (
    <I18nextProvider i18n={i18n} defaultNS="translation">
      <MainApp />
    </I18nextProvider>
  )
}
```

### SSR (Server-Side Rendering)

```javascript
// For Next.js or other SSR frameworks
import { useSSR } from 'react-i18next'

import { initReactI18next } from 'react-i18next'
import i18n from './i18n/config'

i18n.init({
  ...config,
  react: {
    useSuspense: false
  }
})

// In your page
function Page() {
  useSSR(i18n, 'en')
  // ... rest of component
}
```

### SEO with i18n

```jsx
import { useTranslation } from 'react-i18next'
import { Helmet } from 'react-helmet'

function SEO({ title, description }) {
  const { t, i18n } = useTranslation()

  return (
    <Helmet
      htmlAttributes={{ lang: i18n.language }}
      title={t(title)}
      meta={[
        {
          name: 'description',
          content: t(description)
        }
      ]}
    />
  )
}
```

## Error Handling

### Missing Key Handler

```javascript
i18n.init({
  ...config,
  saveMissing: true,
  missingKeyHandler: (lng, ns, key) => {
    console.warn(`Missing translation: ${key} for language: ${lng}`)
  }
})
```

### Fallback Translations

```javascript
i18n.init({
  ...config,
  fallbackNS: 'translation',
  debug: true
})
```
