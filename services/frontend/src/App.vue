<script setup lang="ts">
  import { useWebApp } from "vue-tg";
  import { useRouter } from "vue-router";

  const { initDataUnsafe, close } = useWebApp();
  const user = initDataUnsafe.user || null;

  if (user == null) {
    const router = useRouter();
    router.push(`/notg`)
  }
</script>

<template>
    <router-view />
</template>

<style scoped>
/* Styles global */
</style>