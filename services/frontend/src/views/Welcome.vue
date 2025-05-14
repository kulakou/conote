<script setup lang="ts">
  import HomeCard from "../components/HomeCard.vue";
  import AboutLine from "../components/AboutLine.vue";
  import StartButtons from "../components/StartButtons.vue";
  import { useWebApp } from "vue-tg";

  const { initDataUnsafe, close } = useWebApp();
  const user = initDataUnsafe.user || "anon";
</script>

<template>
  <div class="grid h-screen grid-rows-3">
    <div class="px-8 py-4">
      <HomeCard />
    </div>
    <div class="px-8 my-auto">
      <StartButtons />
    </div>
    <div class="px-8 pb-8 mt-auto">
      <AboutLine />
    </div>
  </div>
</template>

<style scoped></style>
