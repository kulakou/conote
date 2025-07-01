import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import { router } from './router'
import { useTelegramUserStore } from '@/stores/telegramUser'

function getInitData(): string | null {
  if (!window.location.hash) return null
  const hash = window.location.hash.substring(1)
  const params = new URLSearchParams(hash)
  const tgWebAppDataEncoded = params.get('tgWebAppData')
  if (!tgWebAppDataEncoded) return null

  try {
    const once = decodeURIComponent(tgWebAppDataEncoded)
    const twice = decodeURIComponent(once)
    return twice
  } catch (e) {
    console.error('Ошибка декодирования tgWebAppData:', e)
    return null
  }
}

async function bootstrapApp() {
  const app = createApp(App)
  const pinia = createPinia()
  app.use(pinia)

  const store = useTelegramUserStore()

  const initData = getInitData()
  if (initData) {
    localStorage.setItem('tg_init_data', initData)
    store.setInitData(initData)
  } else {
    const saved = localStorage.getItem('tg_init_data')
    if (saved) {
      store.setInitData(saved)
    }
  }

  // 🛡️ Всегда проверяем на бэке при загрузке, независимо от источника initData
  if (store.initDataRaw) {
    const isRegistered = await store.verifyOnBackend()
    store.userIsRegistered = isRegistered
  }

  app.use(router)
  app.mount('#app')

  if (window.Telegram?.WebApp?.ready) {
    window.Telegram.WebApp.ready()
  }
}

bootstrapApp()
