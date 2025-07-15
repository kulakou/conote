<template>
  <div class="grid h-screen grid-rows-3">
    <!-- Header -->
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

    <!-- Main -->
    <div class="px-8 my-auto">
      <div class="flex max-w-2xl mx-auto flex-col items-center w-full">
        <!-- Заблоченный textarea -->
        <textarea
          class="w-full h-48 p-4 text-sm text-gray-700 bg-gray-100 rounded-lg resize-none border border-gray-300"
          readonly
        >
Привет друг, по-моему мы с тобой что-то забыли? Не уверен... 🧐
Присоединяйся ко мне в CoNote, заходи в комнату, и никакая идея больше не будет утеряна!

Ссылка на бота: @CoNote_bot
        </textarea>

        <!-- Кнопка скопировать -->
        <button
          v-show="!copied"
          @click="copyInviteText"
          class="mt-4 w-full text-white bg-gray-500 hover:brightness-105 rounded-lg text-sm py-2.5 text-center"
        >
          📋 Скопировать приглашение
        </button>
        <button
          v-show="copied"
          @click="copyInviteText"
          class="mt-4 w-full text-white bg-gray-500 hover:brightness-105 rounded-lg text-sm py-2.5 text-center"
        >
          📋 Приглашение скопировано!
        </button>
        <button @click="router.push('/')" class="text-gray-500 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 mt-2 me-2 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700 rounded-lg text-sm px-3 py-1.5 text-center">
          Назад
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const router = useRouter()

const copied = ref(false)

const inviteText = `Привет друг, по-моему мы с тобой что-то забыли? Не уверен... 🧐
Присоединяйся ко мне в CoNote, заходи в комнату, и никакая идея больше не будет утеряна!

Ссылка на бота: @CoNote_bot`

const copyInviteText = async () => {
  try {
    await navigator.clipboard.writeText(inviteText)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 3000)
  } catch (err) {
    alert('Не удалось скопировать текст. Скопируй его вручную.')
  }
}
</script>
