<template>
  <div class="grid h-screen grid-rows-3">
    <div class="px-8 py-4">
      <div class="flex max-w-2xl mx-auto bg-white rounded-sm shadow-md">
        <div class="w-1/12 flex-shrink-0">
          <img
            class="h-full w-20 object-cover"
            src="../assets/logo.png"
            alt="CoNote Logo"
          />
        </div>
        <div class="w-11/12 p-6">
          <div class="uppercase tracking-wide text-sm text-violet-500 font-medium">
            CoNote
          </div>
          <a
            href="#"
            class="text-lg tracking-tight font-medium text-black hover:underline block"
          >
            Это так просто - делиться 🥹
          </a>
          <p class="mt-2 text-sm text-slate-500">
            Ты в паре шагов от того чтобы начать делиться записками с твоими друзьями прямо в Telegram 🤝
          </p>
        </div>
      </div>
    </div>
    <div class="px-8 my-auto">
      <div class="flex max-w-2xl mx-auto flex-col items-center">
        <button @click="handleRegister" class="w-full text-white bg-gradient-to-r from-green-500 via-green-500 to-green-500 hover:brightness-105 shadow-lg shadow-green-500/50 dark:shadow-lg dark:shadow-green-800/80 rounded-lg text-sm py-2.5 text-center">
          Начать использовать CoNote
        </button>
        <button @click="handleEnterCodeRedir" class="mt-2 w-full text-white bg-gradient-to-r from-cyan-500 via-cyan-500 to-cyan-500 hover:brightness-105 shadow-lg shadow-cyan-500/50 dark:shadow-lg dark:shadow-cyan-800/80 rounded-lg text-sm px-5 py-2.5 text-center">
          Войти с помощью кода
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useTelegramUserStore } from '@/stores/telegramUser'

const router = useRouter()
const store = useTelegramUserStore()

const handleRegister = async () => {
  try {
    await store.registerUser()
    router.push('/home')
  } catch (error) {
    console.error('Ошибка при регистрации пользователя:', error)
  }
}

const handleEnterCodeRedir = () => {
  router.push('/welcome/code')
}
</script>