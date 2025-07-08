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

    <div class="px-8 pb-2">
      <div class="relative flex flex-col justify-center h-14 max-w-2xl mx-auto bg-white rounded-sm shadow-md px-4 py-2">
        <template v-if="rooms && totalRooms > 0">
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
        <template v-if="rooms">
          <div class="text-center w-full">
            <div class="uppercase tracking-wide text-sm text-violet-500 font-medium truncate px-4">
              Доступные комнаты
            </div>
            <template v-if="totalRooms > 0">
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

    <div class="px-8 py-2">
      <div class="max-w-2xl mx-auto bg-white rounded-sm shadow-md">
        <div class="px-6 py-3 text-center">
          <template v-if="rooms.length > 0">
            <div
              v-for="room in rooms"
              :key="room.id"
              class="flex items-center justify-between my-2 w-full"
            >
              <!-- Кнопка перехода в комнату -->
              <button
                @click="router.push(`/rooms/${room.id}`)"
                class="flex items-center flex-grow bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 hover:brightness-105 rounded-lg text-sm text-gray-600 py-2.5 pl-3 pr-4 text-left overflow-hidden"
              >
                <span class="mr-2">🚪</span>
                <span class="truncate block w-full">
                  {{ room.name }}
                </span>
              </button>

              <!-- Кнопка удаления -->
              <button
                @click="leaveRoom(room.id)"
                class="ml-2 flex items-center justify-center text-red-600 rounded-lg p-2"
                title="Покинуть комнату"
              >
                🗑️
              </button>
            </div>
            <button @click="router.push('/rooms/create')" class="my-1 mt-3 w-full text-white bg-gradient-to-r from-green-500 to-green-500 hover:brightness-105 rounded-lg text-sm py-2.5 text-center">
              Создать новую комнату
            </button>
            <button class="w-full text-white bg-gradient-to-r from-green-500 to-green-500 hover:brightness-105 rounded-lg text-sm py-2.5 text-center">
              Присоединиться к комнате по коду
            </button>
          </template>

          <template v-else-if="!loading">
            <p class="text-slate-400 my-12">Пока что у тебя нет комнат 💤</p>
            <button @click="router.push('/rooms/create')" class="my-1 mt-3 w-full text-white bg-gradient-to-r from-green-500 to-green-500 hover:brightness-105 rounded-lg text-sm py-2.5 text-center">
              Создать новую комнату
            </button>
            <button class="w-full text-white bg-gradient-to-r from-green-500 to-green-500 hover:brightness-105 rounded-lg text-sm py-2.5 text-center">
              Присоединиться к комнате по коду
            </button>
          </template>

          <template v-else>
            <div class="flex justify-center items-center py-4">
              <svg
                class="animate-spin h-6 w-6 text-violet-500"
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
          </template>
        </div>
      </div>
    </div>

    <!-- Footer navigation -->
    <footer
      class="fixed bottom-0 left-0 w-full bg-white border-t border-gray-200 shadow-md flex justify-around items-center py-2 z-50"
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
  import { ref, onMounted, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import { useTelegramUserStore } from '@/stores/telegramUser'
  import axios from 'axios'

  const router = useRouter()
  const store = useTelegramUserStore()

  const rooms = ref<any[]>([])
  const loading = ref(true)

  const page = ref(1)
  const pageSize = 5
  const totalRooms = ref(0)
  const totalPages = computed(() => Math.ceil(totalRooms.value / pageSize))

  const fetchRooms = async () => {
    try {
      const tgId = store.user?.id
      const response = await axios.get(`/api/rooms`, {
        params: {
          tg_id: tgId,
          page: page.value,
          page_size: pageSize
        }
      })
      rooms.value = response.data.rooms
      totalRooms.value = response.data.total_rooms || 0
    } catch (err) {
      console.error('Ошибка при загрузке комнаты', err)
    } finally {
      loading.value = false
    }
  }

  const nextPage = () => {
    if (page.value < totalPages.value) {
      page.value++
      fetchRooms()
    }
  }

  const prevPage = () => {
    if (page.value > 1) {
      page.value--
      fetchRooms()
    }
  }

  const leaveRoom = async (roomId: number) => {
    const confirmed = confirm('Ты точно хочешь покинуть эту комнату?')
    if (!confirmed) return

    const tgId = store.user?.id
    if (!tgId) return

    try {
      await axios.delete(`/api/rooms/${roomId}/leave`, {
        params: { tg_id: tgId }
      })

      // Если после удаления последняя комната — и это последняя страница, идем назад
      if (rooms.value.length === 1 && page.value > 1) {
        page.value--
      }

      await fetchRooms()
    } catch (err) {
      console.error('Ошибка при выходе из комнаты', err)
    }
  }


  onMounted(fetchRooms)
</script>