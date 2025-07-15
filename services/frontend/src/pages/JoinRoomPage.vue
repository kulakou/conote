<template>
  <div class="h-[100dvh] flex flex-col relative mt-2">
    <div class="px-8 py-4">
      <div class="flex max-w-2xl mx-auto bg-white rounded-sm shadow-md">
        <div class="w-1/12 flex-shrink-0">
          <img class="h-full w-20 object-cover" src="../assets/logo.png" alt="CoNote Logo" />
        </div>
        <div class="w-11/12 px-6 py-4">
          <div class="uppercase tracking-wide text-sm text-violet-500 font-medium">CoNote</div>
          <a href="#" class="text-lg tracking-tight font-medium text-black hover:underline block">
            Это так просто - делиться 🥹
          </a>
          <p class="mt-2 text-sm text-slate-500">
            Ты в паре шагов от того чтобы начать делиться записками с твоими друзьями прямо в Telegram 🤝
          </p>
        </div>
      </div>
      <div class="flex max-w-2xl mx-auto mt-10 flex-col items-center">
        <div class="flex gap-2 m-4">
          <input
            @paste="handlePaste"
            v-for="(digit, index) in code"
            :key="index"
            v-model="code[index]"
            ref="inputRefs"
            type="text"
            inputmode="numeric"
            pattern="[0-9]*"
            maxlength="1"
            class="w-10 h-12 text-2xl text-center border-2 border-gray-300 rounded focus:outline-none focus:border-green-500"
            @input="handleInput(index)"
            @keydown.backspace.prevent="handleBackspace(index)"
          />
        </div>
        <button @click="handleJoin" class="text-white bg-gradient-to-r from-green-500 to-green-500 hover:brightness-105 me-2 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700 rounded-lg text-sm px-3 py-1.5 text-center">
          Присоединиться к комнате
        </button>
        <button @click="router.push('/rooms/all')" class="text-gray-500 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 me-2 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700 rounded-lg text-sm px-3 py-1.5 text-center">
          Назад
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, reactive, watch, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { useTelegramUserStore } from '@/stores/telegramUser'
  import axios from "axios";

  const router = useRouter()
  const store = useTelegramUserStore()

  const loading = ref(false)
  const error = ref('')

  const code = reactive(['', '', '', '', '', ''])
  const inputRefs = ref([])

  onMounted(() => {
    inputRefs.value[0]?.focus()
  })


  function handleInput(index) {
    const current = code[index]
    if (current.length > 1) {
      code[index] = current.slice(-1)
    }

    if (code[index] && index < code.length - 1) {
      inputRefs.value[index + 1]?.focus()
    }
  }

  function handleBackspace(index) {
    if (code[index] === '') {
      if (index > 0) {
        inputRefs.value[index - 1]?.focus()
        code[index - 1] = ''
      }
    } else {
      code[index] = ''
    }
  }

  function checkIfComplete() {
    if (code.every((digit) => digit !== '')) {
      const fullCode = code.join('')
      return fullCode
    }
    return null
  }

  const handleJoin = async () => {
    const code = checkIfComplete()
    if (code !== null) {
      try {
        const tgId = store.user?.id
        if (!tgId) {
          loading.value = false
          return
        }
        const res = await axios.post(`/api/rooms/join`, {
          code: code
        }, {
          params: { tg_id: tgId }
        })
        router.push('/rooms/all')
      } catch (err) {
        const message = err.response?.data?.detail
        alert(message)
        inputRefs.value[5]?.focus()
        console.error(err)
      } finally {
        loading.value = false
      }
    }
  }

  function handlePaste(event: ClipboardEvent) {
    event.preventDefault()
    const pasted = event.clipboardData?.getData('text') ?? ''
    const digits = pasted.replace(/\D/g, '').slice(0, code.length) // только цифры

    for (let i = 0; i < code.length; i++) {
      code[i] = digits[i] ?? ''
    }

    // Фокус на следующую пустую ячейку или на последнюю
    const nextIndex = digits.length < code.length ? digits.length : code.length - 1
    inputRefs.value[nextIndex]?.focus()
  }
</script>