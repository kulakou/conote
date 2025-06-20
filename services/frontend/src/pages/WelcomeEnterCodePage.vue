<template>
  <div class="grid h-screen grid-rows-3">
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
            It's so simple sharing notes 🥹
          </a>
          <p class="mt-2 text-sm text-slate-500">
            You're just a few steps away from collaborating with your Telegram friends 🤝
          </p>
        </div>
      </div>
    </div>
    <div class="px-8 my-auto">
      <div class="flex max-w-2xl mx-auto flex-col items-center">
        <div class="flex gap-2 m-4">
          <input
            v-for="(digit, index) in code"
            :key="index"
            v-model="code[index]"
            ref="inputRefs"
            type="text"
            maxlength="1"
            class="w-12 h-12 text-2xl text-center border-2 border-gray-300 rounded focus:outline-none focus:border-green-500"
            @input="handleInput(index)"
            @keydown.backspace.prevent="handleBackspace(index)"
          />
        </div>
        <button @click="handleRegistration" class="text-white bg-gradient-to-r from-green-500 to-green-500 hover:brightness-105 me-2 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700 rounded-lg text-sm px-3 py-1.5 text-center">
          Start with provided code
        </button>
        <button @click="handleBack" class="text-gray-500 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 me-2 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700 rounded-lg text-sm px-3 py-1.5 text-center">
          Go Back
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, reactive, watch, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { useUserStore } from '@/stores/user'

  const store = useUserStore()
  const router = useRouter()

  const handleBack = () => {
    router.push('/welcome')
  }

  const code = reactive(['', '', '', '', '', ''])
  const inputRefs = ref([])

  // focus на первой ячейке при загрузке
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

  const handleRegistration = async () => {
    if (!store.tgUser) return
    try {
      const code = checkIfComplete()
      if (code !== null) {
        await store.registerUser(code)
        router.push('/home')
      }
    } catch (error) {
      console.error('Ошибка при регистрации пользователя:', error)
    }
  }
</script>