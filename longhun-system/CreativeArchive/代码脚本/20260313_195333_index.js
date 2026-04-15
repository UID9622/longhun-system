import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import en from './locales/en.json'
import zh from './locales/zh.json'

// List of supported languages
const availableLocales = ['en', 'zh']
  
// Auto-detect user language preference
const browserLocale = (navigator.language || navigator.userLanguage).substring(0, 2)
const defaultLocale = availableLocales.includes(browserLocale) ? browserLocale : 'en'

// Resource configuration
const resources = {
  en: {
    translation: en
  },
  zh: {
    translation: zh
  }
}

// i18n configuration
i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: defaultLocale,
    fallbackLng: 'en', // Fallback language
    interpolation: {
      escapeValue: false, // React already escapes XSS
    },
    debug: false, // Disable debug in production
    react: {
      useSuspense: false, // Don't use Suspense
      bindI18n: 'languageChanged', // Re-render when language changes
      bindStore: 'added removed', // Re-render when store changes
      transEmptyNodeValue: '', // Empty node value
      transKeepBasicHtmlNodesFor: ['br', 'strong', 'i'] // Keep these HTML nodes
    }
  })

// Custom utility functions
export const i18nNext = i18n

// Language switch function
export const changeLanguage = (lng) => {
  if (availableLocales.includes(lng)) {
    i18n.changeLanguage(lng)
    localStorage.setItem('i18nextLng', lng)
    return true
  }
  return false
}

// Get current language
export const getCurrentLanguage = () => {
  return i18n.language
}

// Get list of supported languages
export const getAvailableLanguages = () => {
  return availableLocales
}

// Custom React hook wrapper
import { useTranslation as useTranslationBase } from 'react-i18next'

// Enhanced useTranslation hook
export const useTranslation = (ns) => {
  const { t, i18n, ready } = useTranslationBase(ns)
  
  const changeLang = (lng) => changeLanguage(lng)
  
  return {
    t,
    i18n,
    ready,
    changeLang,
    currentLanguage: i18n.language,
    availableLanguages: availableLocales,
    isLoading: !ready
  }
}

// React Context Provider
import React, { createContext, useContext, useEffect, useState } from 'react'

const I18nContext = createContext()

export const I18nProvider = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState(i18n.language)
  const [isLoading, setIsLoading] = useState(false)
  
  useEffect(() => {
    const handleLanguageChanged = (lng) => {
      setCurrentLanguage(lng)
    }
    
    i18n.on('languageChanged', handleLanguageChanged)
    
    return () => {
      i18n.off('languageChanged', handleLanguageChanged)
    }
  }, [])
  
  const switchLanguage = async (lng) => {
    if (lng === currentLanguage) return true
    
    setIsLoading(true)
    try {
      await i18n.changeLanguage(lng)
      return true
    } catch (error) {
      console.error('Failed to switch language:', error)
      return false
    } finally {
      setIsLoading(false)
    }
  }
  
  return (
    <I18nContext.Provider value={{
      currentLanguage,
      isLoading,
      availableLocales,
      switchLanguage,
      t: (key, options) => i18n.t(key, options)
    }}>
      {children}
    </I18nContext.Provider>
  )
}

export const useI18nContext = () => {
  const context = useContext(I18nContext)
  if (!context) {
    throw new Error('useI18nContext must be used within I18nProvider')
  }
  return context
}

// Language selector component
export function LanguageSelector({ className = '' }) {
  const { currentLanguage, switchLanguage, availableLocales, isLoading } = useI18nContext()
  
  const languageOptions = [
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'zh', name: 'Chinese', flag: '🇨🇳' }
  ]
  
  return (
    <select
      className={className}
      value={currentLanguage}
      onChange={(e) => switchLanguage(e.target.value)}
      disabled={isLoading}
    >
      {languageOptions.map((lang) => (
        <option key={lang.code} value={lang.code}>
          {lang.flag} {lang.name}
        </option>
      ))}
    </select>
  )
}

export default i18n
