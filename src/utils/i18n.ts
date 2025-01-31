import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import enTranslations from '../../public/locales/en/translation.json';
import swTranslations from '../../public/locales/sw/translation.json';

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: enTranslations },
    sw: { translation: swTranslations },
  },
  lng: 'en',
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
});

export default i18n;