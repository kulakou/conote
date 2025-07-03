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

    <!-- Room Info + Pagination -->
    <div class="px-8 pb-4">
      <div class="relative flex flex-col justify-center h-14 max-w-2xl mx-auto bg-white rounded-sm shadow-md px-4 py-2">
        <template v-if="room && totalNotes > 0">
          <!-- Стрелки -->
          <button
            class="absolute left-2 top-1/2 transform -translate-y-1/2 text-violet-500 hover:text-violet-700"
            @click="prevPage"
            v-show="page > 1"
          >
            ◀
          </button>
          <button
            class="absolute right-2 top-1/2 transform -translate-y-1/2 text-violet-500 hover:text-violet-700"
            @click="nextPage"
            v-show="page < totalPages"
          >
            ▶
          </button>
        </template>
        <template v-if="room">
          <!-- Название комнаты и пагинация -->
          <div class="text-center w-full">
            <div class="uppercase tracking-wide text-sm text-violet-500 font-medium truncate px-4" :title="`Комната: ${room.name}`">
              Комната: {{ room.name }}
            </div>
            <template v-if="totalNotes > 0">
              <div class="text-xs text-gray-500">
                Страница: {{ page }} из {{ totalPages }}
              </div>
            </template>
          </div>
        </template>

        <template v-else-if="loading">
          <div class="flex justify-center items-center h-full">
            <svg class="animate-spin h-6 w-6 text-violet-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
            </svg>
          </div>
        </template>
      </div>
    </div>

    <!-- Notes List -->
    <template v-if="!loading">
      <div class="px-8">
        <div class="max-w-2xl mx-auto bg-white rounded-sm shadow-md">
          <div class="p-6 text-center">
            <template v-if="!loading && totalNotes > 0">
              <button
                v-for="note in notes"
                :key="note.id"
                @click=""
                class="relative my-1.5 w-full text-gray-600 bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 hover:brightness-105 rounded-lg text-sm py-2.5 text-center"
              >
                <span class="absolute left-2 top-1/2 -translate-y-1/2">📝</span>
                <span class="block truncate px-12" :title="note.name">
                  {{ note.name }}
                </span>
              </button>
            </template>

            <template v-else-if="!loading && totalNotes === 0">
              <p class="text-slate-400">В этой комнате пока нет записок 💤</p>
            </template>

            <!-- Создание новой записки -->
            <template v-if="!loading">
              <button
                class="my-2 mt-5 w-full text-white bg-gradient-to-r from-green-500 to-green-500 hover:brightness-105 rounded-lg text-sm py-2.5 text-center"
              >
                Создать новую записку
              </button>
            </template>
          </div>
        </div>
      </div>
    </template>

    <!-- Footer -->
    <footer class="fixed bottom-2 left-0 w-full bg-white border-t border-gray-200 shadow-md flex justify-around items-center py-2 z-50">
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
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTelegramUserStore } from '@/stores/telegramUser'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useTelegramUserStore()

const room = ref<any | null>(null)
const notes = ref<any[]>([])
const loading = ref(true)

const page = ref(1)
const pageSize = 5
const totalNotes = ref(0)
const totalPages = computed(() => Math.ceil(totalNotes.value / pageSize))

const fetchNotes = async () => {
  try {
    const roomId = route.params.room_id
    const tgId = store.user?.id
    if (!roomId || !tgId) {
      return router.push('/home')
    }

    const response = await axios.get(`/api/rooms/${roomId}`, {
      params: {
        tg_id: tgId,
        page: page.value,
        page_size: pageSize
      }
    })

    room.value = response.data
    notes.value = response.data.notes
    totalNotes.value = response.data.total_notes || 0
  } catch (err) {
    console.error('Ошибка при загрузке комнаты', err)
  } finally {
    loading.value = false
  }
}

const nextPage = () => {
  if (page.value < totalPages.value) {
    page.value++
    fetchNotes()
  }
}

const prevPage = () => {
  if (page.value > 1) {
    page.value--
    fetchNotes()
  }
}

onMounted(fetchNotes)
</script>
