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
        </div>
      </div>

      <!-- Notes List -->
      <div class="px-8">
        <div class="max-w-2xl mx-auto bg-white rounded-sm shadow-md">
          <div class="p-6 text-center">
            <template v-if="!loading && totalNotes > 0">
              <div
                v-for="note in notes"
                :key="note.id"
                class="flex items-center justify-between my-2 w-full"
              >
                <!-- Кнопка перехода к записке -->
                <button
                  @click="router.push(`/rooms/${room.id}/notes/${note.id}`)"
                  class="flex items-center flex-grow bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 hover:brightness-105 rounded-lg text-sm text-gray-600 py-2.5 pl-3 pr-4 text-left overflow-hidden"
                >
                  <span class="mr-2">📝</span>
                  <span class="truncate block w-full">
                    {{ note.name }}
                  </span>
                </button>

                <button
                  @click="deleteNote(note.id)"
                  class="flex items-center justify-center text-red-600 rounded-lg pl-3 py-2"
                  title="Удалить записку"
                >
                  ⌫
                </button>
                <button
                  @click="router.push(`/rooms/${room.id}/notes/${note.id}/edit`)"
                  class="flex items-center justify-center text-red-600 rounded-lg pl-3 py-2"
                  title="Редактировать записку"
                >
                  ⋮
                </button>
              </div>
            </template>

            <template v-else-if="!loading && totalNotes === 0">
              <p class="text-slate-400">Список записок пуст</p>
            </template>

            <!-- Создание новой записки -->
            <template v-if="!loading">
              <button
                  @click="router.push(`/rooms/${room.id}/notes/create`)"
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
    <footer class="fixed bottom-0 left-0 w-full bg-white border-t border-gray-200 shadow-md flex justify-around items-center px-24 py-2 z-50">
      <button
        @click="router.push('/home')"
        class="mb-4 flex flex-col items-center text-violet-600 hover:text-violet-800 text-sm"
      >
        <img src="@/assets/home.png" alt="Home" class="h-8 w-8 m-2" />
      </button>
      <template v-if="room && room.type === 'single_seat_private'">
        <button
          @click="router.push('/home')"
          class="mb-4 flex flex-col items-center text-violet-600 hover:text-violet-800 text-sm"
        >
          <img src="@/assets/back.png" alt="Back" class="h-8 w-8 m-2" />
        </button>
      </template>
      <template v-else>
        <button
          @click="router.push('/rooms/all')"
          class="mb-4 flex flex-col items-center text-violet-600 hover:text-violet-800 text-sm"
        >
          <img src="@/assets/back.png" alt="Back" class="h-8 w-8 m-2" />
        </button>
      </template>
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

const deleteNote = async (noteId: number) => {
  const tgId = store.user?.id
  if (!tgId) return

  try {
    if (!confirm("Ты точно хочешь удалить записку?")) return

    loading.value = true
    await axios.delete(`/api/notes/${noteId}`, {
      params: { tg_id: tgId }
    })

    // Если после удаления записка — последняя на странице, и это была последняя страница, уходим назад
    if (notes.value.length === 1 && page.value > 1) {
      page.value--
    }

    await fetchNotes() // перезагружаем данные
  } catch (error) {
    console.error('Ошибка при удалении записки', error)
  }
  finally {
    loading.value = false
  }
}

onMounted(fetchNotes)
</script>
