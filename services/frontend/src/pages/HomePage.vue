<template>
  <div class="h-[100dvh] flex flex-col relative">
    <!-- Main content -->
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
    <div class="px-8 py-2">
      <div class="max-w-2xl mx-auto bg-white rounded-sm shadow-md">
        <div class="p-6 text-center">
          <div class="uppercase tracking-wide text-sm text-violet-500 font-medium mb-4">
            Привет, <a class="text-red-500">{{ store.user.first_name }}</a>! Ты можешь:
          </div>
          <button @click="router.push(`/rooms/private?${store.user?.id}`)" class="my-2 w-full text-gray-600 bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 hover:brightness-105 rounded-lg text-sm py-2.5 text-center">
            Войти в личную комнату
          </button>
          <button @click="router.push('/rooms/all')" class="my-2 w-full text-gray-600 bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 hover:brightness-105 rounded-lg text-sm py-2.5 text-center">
            Просмотреть остальные комнаты
          </button>
        </div>
      </div>
    </div>
    <div class="px-8 py-2">
      <div class="max-w-2xl mx-auto bg-white rounded-sm shadow-md">
        <div class="p-6 text-center">
          <div class="uppercase tracking-wide text-sm text-violet-500 font-medium mb-4">
            Подожди! Не забудь:
          </div>
          <button @click="router.push('/share')" class="w-full text-white bg-gradient-to-r from-green-500 via-green-500 to-green-500 hover:brightness-105 rounded-lg text-sm py-2.5 text-center">
            Пригласить своих друзей в CoNote!
          </button>
        </div>
      </div>
    </div>

    <!-- Footer navigation -->
    <footer
      class="fixed bottom-0 left-0 w-full bg-white border-t border-gray-200 shadow-md flex justify-around items-center px-24 py-2 z-50"
    >
      <button
        @click="router.push('/home')"
        class="mb-4 flex flex-col items-center text-violet-600 hover:text-violet-800 text-sm"
      >
        <img src="@/assets/home.png" alt="Home" class="h-8 w-8 m-2" />
      </button>
      <button
        @click=""
        class="mb-4 opacity-25 flex flex-col items-center text-violet-600 hover:text-violet-800 text-sm"
      >
        <img src="@/assets/back.png" alt="Back" class="h-8 w-8 m-2" />
      </button>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useTelegramUserStore } from '@/stores/telegramUser'

const router = useRouter()
const store = useTelegramUserStore()
</script>