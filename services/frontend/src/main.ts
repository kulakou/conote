import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import { router } from './router'
import { useTelegramUserStore } from '@/stores/telegramUser'

function getInitDataFromHash(): string | null {
  if (!window.location.hash) return null
  const hash = window.location.hash.substring(1)
  const params = new URLSearchParams(hash)
  const tgWebAppDataEncoded = params.get('tgWebAppData')
  return tgWebAppDataEncoded ?? null
}

const app = createApp(App)

app.use(createPinia())
app.use(router)

const tg = window?.Telegram?.WebApp
let initData = tg?.initData || localStorage.getItem('tg_init_data') || ''

if (!initData) {
  const fromHash = getInitDataFromHash()
  if (fromHash) initData = fromHash
}

if (initData.length > 0) {
  alert(initData)
  const telegramUserStore = useTelegramUserStore()
  telegramUserStore.initDataRaw = initData
  telegramUserStore.setInitData(initData)
  localStorage.setItem('tg_init_data', initData)
}

app.mount('#app')