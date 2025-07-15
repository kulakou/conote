<template>
  <div class="h-[100dvh] flex flex-col relative">
    <!-- Header -->
    <div class="px-8 py-4 pt-6">
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
    <template v-if="loading">
      <div class="px-8 pb-2">
        <div class="max-w-2xl mx-auto bg-white rounded-sm flex justify-center items-center min-h-[360px]">
          <svg
            class="animate-spin h-12 w-12 text-violet-500"
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
        </div>
      </div>
    </template>
    <template v-else>
      <!-- Заголовок -->
      <div class="px-8 pb-4">
        <div class="relative flex flex-col justify-center h-10 max-w-2xl mx-auto bg-white rounded-sm shadow-md px-4">
          <div class="text-center w-full">
            <div class="uppercase tracking-wide text-sm text-violet-500 font-medium truncate px-4">
              Редактирование комнаты
            </div>
          </div>
        </div>
      </div>
      <div class="px-8 pb-4 mb-2">
        <div class="text-center uppercase relative flex flex-col max-w-2xl mx-auto bg-white rounded-sm shadow-md px-6 py-2">
          <label class="block text-sm font-medium text-violet-600 mb-3">Имя комнаты</label>
          <input
              ref="inputEl"
              v-model="roomName"
              :disabled="loading"
              type="text"
              placeholder="Введи название комнаты"
              class="pl-3 text-left mb-6 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2 focus:outline-none focus:ring-2 focus:ring-violet-400"
              required
              @focus="inputFocused = true"
              @blur="inputFocused = false"
          />

          <label class="mb-3 block text-sm font-medium text-violet-600">Тип комнаты</label>
          <div class="relative">
            <select
                ref="selectEl"
                v-model="roomType"
                class="mb-6 rounded-lg block w-full bg-transparent placeholder:text-slate-400 text-slate-700 text-sm border border-slate-200 pl-3 pr-8 py-2 transition duration-300 ease focus:outline-none focus:border-slate-400 hover:border-slate-400 shadow-sm focus:shadow-md appearance-none cursor-pointer">
                <option value="shared">Публичная</option>
                <option value="single_seat">Приватная</option>
            </select>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.2" stroke="currentColor" class="h-5 w-5 ml-1 absolute top-2.5 right-2.5 text-slate-700">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15 12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9" />
            </svg>
          </div>
          <template v-if="roomType === 'shared'">
            <label class="block text-sm font-medium text-violet-600 mb-3">Код комнаты</label>
            <template v-if="!code">
              <button
                @click="generateCode"
                class="mb-2 flex justify-center items-center w-full text-white bg-gradient-to-r from-green-500 via-green-500 to-green-500 hover:brightness-105 rounded-lg text-sm py-2 text-center">
                  Сгенерировать код
              </button>
            </template>
            <template v-else>
              <input
                  disabled
                  v-model="code"
                  type="text"
                  class="bg-gray-200 pl-3 text-center mb-6 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2 focus:outline-none focus:ring-2 focus:ring-violet-400"
              />
            </template>
          </template>
        </div>
      </div>

      <!-- Кнопка: фиксирована над футером -->
      <div class="fixed bottom-24 left-0 w-full px-8 z-50">
        <div class="max-w-2xl mx-auto">
          <button
              v-show="!inputFocused"
              @click="submitRoom"
              :disabled="loading"
              class="flex justify-center items-center w-full text-white bg-gradient-to-r from-green-500 via-green-500 to-green-500 hover:brightness-105 rounded-lg text-sm py-2.5 text-center">
                Сохранить комнату
          </button>
          <p v-show="!inputFocused" v-if="error" class="text-sm text-red-500 mt-3 text-center">{{ error }}</p>
        </div>
      </div>
    </template>

    <!-- Footer -->
    <footer
      v-show="!inputFocused"
      class="fixed bottom-0 left-0 w-full bg-white border-t border-gray-200 shadow-md flex justify-around items-center py-2 px-24 z-40"
    >
      <button
        @click="router.push('/home')"
        class="mb-4 flex flex-col items-center text-violet-600 hover:text-violet-800 text-sm"
      >
        <img src="@/assets/home.png" alt="Home" class="h-8 w-8 m-2" />
      </button>
      <button
        @click="router.push(`/rooms/all`)"
        class="mb-4 flex flex-col items-center text-violet-600 hover:text-violet-800 text-sm"
      >
        <img src="@/assets/back.png" alt="Back" class="h-8 w-8 m-2" />
      </button>
    </footer>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTelegramUserStore } from '@/stores/telegramUser'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useTelegramUserStore()

const roomId = Number(route.params.room_id)

const code = ref(null)
const roomName = ref('')
const roomType = ref<'shared' | 'single_seat'>('shared')
const loading = ref(false)
const error = ref('')

const inputEl = ref<HTMLInputElement | null>(null)
const selectEl = ref<HTMLSelectElement | null>(null)
const inputFocused = ref(false)

const fetchRoom = async () => {
  loading.value = true
  try {
    const tgId = store.user?.id
    const response = await axios.get(`/api/rooms/${roomId}`, {
      params: { tg_id: tgId }
    })

    const room = response.data
    roomName.value = room.name
    roomType.value = room.type
    code.value = room.code
  } catch (err) {
    error.value = 'Ошибка при загрузке комнаты'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const submitRoom = async () => {
  error.value = ''
  if (!roomName.value.trim()) {
    error.value = 'Имя комнаты не может быть пустым'
    return
  }

  loading.value = true

  try {
    const tgId = store.user?.id
    if (!tgId) {
      error.value = 'Ошибка авторизации'
      loading.value = false
      return
    }

    await axios.put(`/api/rooms/${roomId}`, {
      name: roomName.value,
      type: roomType.value,
      code: roomType.value === 'shared' ? code.value : null
    }, {
      params: { tg_id: tgId }
    })

    router.push(`/rooms/all`)
  } catch (err: any) {
    if (err.response?.status === 403) {
      error.value = 'У тебя нет прав на изменение этой комнаты'
    } else {
      error.value = 'Не удалось обновить комнату. Попробуй позже.'
    }
    console.error(err)
  } finally {
    loading.value = false
  }
}

const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as Node
  if (
    (inputEl.value && inputEl.value.contains(target)) ||
    (selectEl.value && selectEl.value.contains(target))
  ) return

  setTimeout(() => {
    inputFocused.value = false
  }, 100)
}

const generateCode = async() => {
  loading.value = true
  try {
    const tgId = store.user?.id
    if (!tgId) {
      error.value = 'Ошибка авторизации'
      loading.value = false
      return
    }
    const response = await axios.get(`/api/rooms/code/generated`)
    if (!response.data) {
      alert("Произошла ошибка при генерации кода. Попробуй еще раз.")
    }
    else {
      code.value = response.data
      await axios.post(`/api/rooms/${roomId}/code`, {
        code: code.value
      }, {
        params: { tg_id: tgId }
      })
    }
  } catch (err) {
    error.value = 'Ошибка при загрузке нового кода'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRoom()
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
