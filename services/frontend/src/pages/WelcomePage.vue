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
        <button @click="handleRegister" class="w-full text-white bg-gradient-to-r from-green-500 via-green-500 to-green-500 hover:brightness-105 shadow-lg shadow-green-500/50 dark:shadow-lg dark:shadow-green-800/80 rounded-lg text-sm py-2.5 text-center">
          Start using CoNote
        </button>
        <button @click="handleEnterCodeRedir" class="mt-2 w-full text-white bg-gradient-to-r from-cyan-500 via-cyan-500 to-cyan-500 hover:brightness-105 shadow-lg shadow-cyan-500/50 dark:shadow-lg dark:shadow-cyan-800/80 rounded-lg text-sm px-5 py-2.5 text-center">
          Enter with shared code
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()

const handleRegister = () => {
  router.push('/home')
}

const handleEnterCodeRedir = () => {
  router.push('/welcome/code')
}
</script>