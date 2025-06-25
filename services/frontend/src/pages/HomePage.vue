<template>
  <div class="h-[100dvh] flex flex-col relative">
    <!-- Main content -->
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
            Enter one of the available rooms and start noting private or with your friends 🤝
          </p>
        </div>
      </div>
    </div>

    <div class="px-8 py-2">
      <div class="max-w-2xl mx-auto bg-white rounded-sm shadow-md">
        <div class="p-6 text-center">
          <div class="uppercase tracking-wide text-sm text-violet-500 font-medium mb-4">
            This is a Homepage! You can:
          </div>
          <button @click="" class="my-2 w-full text-gray-600 bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 hover:brightness-105 rounded-lg text-sm py-2.5 text-center">
            Enter private Room
          </button>
          <button @click="" class="my-2 w-full text-gray-600 bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 hover:brightness-105 rounded-lg text-sm py-2.5 text-center">
            See shared Rooms
          </button>
        </div>
      </div>
    </div>
    <div class="px-8 py-2">
      <div class="max-w-2xl mx-auto bg-white rounded-sm shadow-md">
        <div class="p-6 text-center">
          <div class="uppercase tracking-wide text-sm text-violet-500 font-medium mb-4">
            Wait! You can also:
          </div>
          <button @click="" class="w-full text-white bg-gradient-to-r from-green-500 via-green-500 to-green-500 hover:brightness-105 rounded-lg text-sm py-2.5 text-center">
            Invite your friends to Collaborate!
          </button>
        </div>
      </div>
    </div>

    <!-- Footer navigation -->
    <footer
      class="fixed bottom-0 left-0 w-full bg-white border-t border-gray-200 shadow-md flex justify-around items-center py-2 z-50"
    >
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
import { useRouter } from 'vue-router'
const router = useRouter()
</script>