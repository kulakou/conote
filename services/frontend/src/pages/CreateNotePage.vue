<template>
  <div class="flex flex-col h-screen relative overflow-hidden">
    <!-- Header -->
    <div class="px-8 py-4 pt-6 shrink-0 z-10 bg-white">
      <div class="flex max-w-2xl mx-auto bg-white rounded-sm shadow-md">
        <div class="w-1/12 flex-shrink-0">
          <img class="h-full w-20 object-cover" src="../assets/logo.png" alt="CoNote Logo" />
        </div>
        <div class="w-11/12 px-6 py-4">
          <div class="uppercase tracking-wide text-sm text-violet-500 font-medium">CoNote</div>
          <a href="#" class="text-lg tracking-tight font-medium text-black hover:underline block">
            Это так просто - делиться 🥹
          </a>
        </div>
      </div>
    </div>

    <!-- Scrollable Content (Заголовок + форма) -->
    <div class="flex-1 overflow-y-auto px-8 pb-40 pt-4"> <!-- важный отступ снизу (pb-40) -->
      <!-- Заголовок -->
      <div class="pb-4">
        <div class="relative flex flex-col justify-center h-10 max-w-2xl mx-auto bg-white rounded-sm shadow-md px-4">
          <div class="text-center w-full">
            <div class="uppercase tracking-wide text-sm text-violet-500 font-medium truncate px-4">
              Создание записки
            </div>
          </div>
        </div>
      </div>

      <!-- Форма -->
      <div class="text-center uppercase relative flex flex-col max-w-2xl mx-auto bg-white rounded-sm shadow-md px-6 py-3">
        <label class="block text-sm font-medium text-violet-600 mb-3">Название</label>
        <input
          v-model="noteName"
          :disabled="loading"
          placeholder="Введи название записки"
          class="resize-none pl-3 mb-2 text-left border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2 focus:outline-none focus:ring-2 focus:ring-violet-400"
          required
          @focus="inputFocused = true"
          @blur="inputFocused = false"
        />

        <label class="mb-3 block text-sm font-medium text-violet-600">Тип записки</label>
        <div class="relative">
          <select
              v-model="noteType"
              class="mb-4 rounded-lg block w-full bg-transparent placeholder:text-slate-400 text-slate-700 text-sm border border-slate-200 pl-3 pr-8 py-2 transition duration-300 ease focus:outline-none focus:border-slate-400 hover:border-slate-400 shadow-sm focus:shadow-md appearance-none cursor-pointer">
              <option value="text">Текстовая</option>
              <option value="link">Ссылочная</option>
          </select>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.2" stroke="currentColor" class="h-5 w-5 ml-1 absolute top-2.5 right-2.5 text-slate-700">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15 12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9" />
          </svg>
        </div>

        <template v-if="noteType === 'link'">
          <label class="block text-sm font-medium text-violet-600 mb-3">Ссылка</label>
          <input
              v-model="noteLink"
              :disabled="loading"
              type="text"
              placeholder="Вставь ссылку"
              class="pl-3 text-left mb-4 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2 focus:outline-none focus:ring-2 focus:ring-violet-400"
              required
              @focus="inputFocused = true"
              @blur="inputFocused = false"
          />
        </template>

        <label class="block text-sm font-medium text-violet-600 mb-3">Описание</label>
        <textarea
          v-model="noteText"
          :disabled="loading"
          placeholder="Введи описание записки"
          rows="4"
          class="h-16 resize-none pl-3 mb-2 text-left border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2 focus:outline-none focus:ring-2 focus:ring-violet-400"
          required
          @focus="inputFocused = true"
          @blur="inputFocused = false"
        />
      </div>
    </div>

    <!-- Кнопка: фиксирована над футером -->
    <div class="fixed bottom-24 left-0 w-full px-8 z-50">
      <div class="max-w-2xl mx-auto">
        <button
            v-show="!inputFocused"
            @click="submitNote"
            :disabled="loading"
            class="flex justify-center items-center w-full text-white bg-gradient-to-r from-green-500 via-green-500 to-green-500 hover:brightness-105 rounded-lg text-sm py-2.5 text-center">
            <template v-if="loading">
              <svg
                class="animate-spin h-5 w-5 text-white-500"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                ></circle>
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                ></path>
              </svg>
            </template>
            <template v-else>
              Создать записку
            </template>
        </button>
        <p v-show="!inputFocused" v-if="error" class="text-sm text-red-500 mt-3 text-center">{{ error }}</p>
      </div>
    </div>

    <!-- Footer -->
    <footer
      v-show="!inputFocused"
      class="fixed bottom-0 left-0 w-full bg-white border-t border-gray-200 shadow-md flex justify-around items-center py-2 z-40"
    >
      <button
        @click="router.push('/home')"
        class="mb-4 flex flex-col items-center text-violet-600 hover:text-violet-800 text-sm"
      >
        <img src="@/assets/home.png" alt="Home" class="h-8 w-8 m-2" />
      </button>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useTelegramUserStore } from '@/stores/telegramUser'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const store = useTelegramUserStore()

const noteText = ref('')
const noteName = ref('')
const noteLink = ref('')
const noteType = ref<'text' | 'link'>('text')
const loading = ref(false)
const error = ref('')

const inputFocused = ref(false)

// Получаем ID текущей комнаты из параметров URL
const roomId = Number(route.params.room_id)

const submitNote = async () => {
  error.value = ''
  loading.value = true

  try {
    const tgId = store.user?.id
    if (!tgId) {
      error.value = 'Ошибка авторизации'
      return
    }

    // Проверка обязательных полей
    if (!noteName.value.trim() || !noteText.value.trim() || (noteType.value === 'link' && !noteLink.value.trim())) {
      error.value = 'Заполни все поля'
      return
    }

    // Отправка POST-запроса на создание записки
    await axios.post('/api/notes', {
      name: noteName.value,
      text: noteText.value,
      link: noteLink.value,
      type: noteType.value,
      room_id: roomId,
      created_by: tgId
    })

    // После успешного создания — редирект в текущую комнату
    router.push(`/rooms/${roomId}`)
  } catch (err) {
    console.error(err)
    error.value = 'Не удалось создать записку. Попробуй позже.'
  } finally {
    loading.value = false
  }
}

const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as Node
  if (!(event.target as HTMLElement)?.closest('input, textarea, select')) {
    inputFocused.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
