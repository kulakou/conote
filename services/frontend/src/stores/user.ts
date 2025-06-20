import { defineStore } from 'pinia'
import { api } from '@/plugins/axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    tgUser: null as Telegram.WebAppUser | null,
    isNewUser: null as boolean | null,
    initialized: false,
  }),
  actions: {

    setTelegramUser(user: Telegram.WebAppUser) {
      this.tgUser = user
    },

    async checkIfUserExists() {
      if (!this.tgUser) return
      try {
        const res = await api.get(`/api/telegram_users/exists?tg_id=${this.tgUser.id}`)
        this.isNewUser = !res.data.data.exists
      } catch (err) {
        console.error('Failed to check user exists', err)
        this.isNewUser = true
      }
    },

    async registerUser(code = null) {
      if (!this.tgUser) return

      try {
        let data = {
          tg_id: this.tgUser.id,
          tg_username: this.tgUser.username
        }
        if (code !== null) {
          data.code = code
        }
        await api.post('/api/telegram_users/register', data)
        this.isNewUser = false
      } catch (error) {
        console.error('Registration failed', error)
        throw error
      }
    }
  }
})