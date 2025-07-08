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

    <!-- Main content -->
    <div class="flex-1 overflow-y-auto pb-24">

      <div class="px-8 pb-2">
        <div class="max-w-2xl mx-auto bg-white rounded-sm shadow-md px-4 py-2 flex items-center">
          <template v-if="!loading && note">
            <div class="flex-1 text-center px-2">
              <div class="uppercase tracking-wide text-xs text-violet-500 font-medium break-words">
                Тип записки: {{ note.type === 'link' ? 'ссылка 🔗' : 'текст 💬' }}
              </div>
            </div>
          </template>
          <template v-else-if="loading">
            <div class="flex-1 text-center px-2">
              <div class="uppercase tracking-wide text-xs text-gray-600 font-medium break-words">
                Загрузка...
              </div>
            </div>
          </template>
        </div>
      </div>

        <!-- Название -->
        <div class="px-8 pb-4">
          <div class="max-w-2xl mx-auto bg-white rounded-sm shadow-md px-4 py-3 flex items-center">
            <template v-if="!loading && note">
              <div class="w-4 flex justify-center">
                <span class="text-violet-500">📝</span>
              </div>
              <div class="flex-1 text-center px-2">
                <div class="uppercase tracking-wide text-sm text-gray-600 font-medium break-words">
                  {{ note.name }}
                </div>
              </div>
              <div class="w-4 flex justify-center">
                <span class="text-violet-500">📝</span>
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

      <!-- Note content -->
      <template v-if="!loading && note">
        <!-- Тип -->
        <!-- Контент -->
        <div class="px-8 pb-4">
          <div class="max-w-2xl mx-auto bg-white rounded-sm shadow-md px-4 py-3 flex items-center">
            <div class="flex-1 px-2">
              <template v-if="note.type === 'link'">
                <div class="mb-2 uppercase tracking-wide text-xs text-violet-500 font-medium break-words">
                  Ссылка внутри записки
                </div>
                <a
                  :href="note.link"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="mb-5 inline-block text-violet-600 hover:text-violet-800 font-semibold break-words"
                >
                  ▶️ {{ parsedDomain }}...
                </a>
              </template>
              <div class="mb-2 uppercase tracking-wide text-xs text-violet-500 font-medium break-words">
                Описание внутри записки
              </div>
              <div class="uppercase tracking-wide text-sm text-gray-600 font-medium break-words whitespace-pre-wrap">
                {{ note.text }}
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- Footer -->
    <footer class="fixed bottom-0 left-0 w-full bg-white border-t border-gray-200 shadow-md flex justify-around items-center py-2 z-50">
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { computed } from 'vue'

const router = useRouter()
const route = useRoute()

const note = ref<any | null>(null)
const loading = ref(true)

const parsedDomain = computed(() => {
  if (!note.value?.link) return ''
  try {
    const url = new URL(note.value.link)
    return url.hostname.replace(/^www\./, '') // без www
  } catch (err) {
    return '' // если это невалидный URL
  }
})

const noteId = route.params.note_id

const fetchNote = async () => {
  try {
    const response = await axios.get(`/api/notes/${noteId}`)
    note.value = response.data
  } catch (err) {
    console.error('Ошибка при загрузке записки:', err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchNote)
</script>
