import { defineStore } from 'pinia'
import axios from 'axios'

export interface TelegramUser {
  id: number
  first_name: string
  last_name?: string
  username?: string
  photo_url?: string
  language_code?: string
  is_premium?: boolean
  allows_write_to_pm?: boolean
}

interface TelegramInitData {
  user?: TelegramUser
  chat_instance?: string
  chat_type?: string
  auth_date?: string
  hash?: string
  [key: string]: any
}

export const useTelegramUserStore = defineStore('telegramUser', {
  state: () => ({
    initDataRaw: '',
    initDataParsed: {} as TelegramInitData,
  }),
  getters: {
    user: (state) => state.initDataParsed.user,
    isAuthenticated: (state) =>
      !!state.initDataParsed?.user?.id && !!state.initDataParsed?.hash,
  },
  actions: {
    setInitData(initData: string) {
      this.initDataRaw = initData
      try {
        const decoded = new URLSearchParams(initData)
        const parsed: TelegramInitData = {}

        for (const [key, value] of decoded.entries()) {
          if (key === 'user') {
            parsed.user = JSON.parse(value)
          } else {
            parsed[key] = value
          }
        }
        this.initDataParsed = parsed
      } catch (error) {
        console.error('Ошибка парсинга initData:', error)
      }
    },
    async verifyOnBackend(): Promise<boolean> {
      if (!this.initDataRaw) return false
      try {
        const res = await axios.post('/api/telegram_users/verify', {
          init_data: this.initDataRaw,
        })
        return res.data?.is_registered === true
      } catch (e) {
        console.error('Ошибка верификации Telegram:', e)
        return false
      }
    }
  },
})