<template>
  <div class="h-[100dvh] flex flex-col relative">
    <!-- Main content -->
    <div class="px-8 py-4">
      <div class="flex max-w-2xl mx-auto bg-white rounded-sm shadow-md">
        <div>
          <img
            class="h-full w-full object-cover"
            src="../assets/logo.svg"
            alt="CoNote Logo"
          />
        </div>
        <div class="p-6">
          <div class="uppercase tracking-wide text-sm text-violet-500 font-medium">
            CoNote
          </div>
          <a
            href="#"
            class="mt-1 text-lg tracking-tight font-medium text-black hover:underline"
          >
            Это так просто - делиться 🥹
          </a>
          <p class="mt-2 text-sm text-slate-500">
            Войди в одну из доступных комнат и начни вести записки для себя или делиться со своими друзьями 🤝
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
          <button @click="" class="my-2 w-full text-gray-600 bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 hover:brightness-105 rounded-lg text-sm py-2.5 text-center">
            Войти в личную комнату
          </button>
          <button @click="" class="my-2 w-full text-gray-600 bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 hover:brightness-105 rounded-lg text-sm py-2.5 text-center">
            Посмотреть все комнаты
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
          <button @click="" class="w-full text-white bg-gradient-to-r from-green-500 via-green-500 to-green-500 hover:brightness-105 rounded-lg text-sm py-2.5 text-center">
            Пригласить своих друзей в CoNote!
          </button>
        </div>
      </div>
    </div>

    <!-- Footer navigation -->
    <footer
      class="fixed bottom-0 left-0 w-full bg-white border-t border-gray-200 shadow-md flex justify-around items-center py-2 z-50"
    >
      <button
        @click="router.push('/home')"
        class="my-3 flex flex-col items-center text-violet-600 hover:text-violet-800 text-sm"
      >
        <img src="@/assets/home.png" alt="Home" class="h-8 w-8 m-2" />
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