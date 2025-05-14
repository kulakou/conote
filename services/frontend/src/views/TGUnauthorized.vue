<script setup lang="ts">
  import HomeCard from "../components/HomeCard.vue";
  import AboutLine from "../components/AboutLine.vue";
</script>

<template>
  <div class="grid h-screen grid-rows-3">
    <div class="px-8 py-4">
      <HomeCard />
    </div>
    <div class="px-8 my-auto text-center">
      <p>CoNote application currently supports only Telegram MiniApp usage</p><br>
      <p>Please, use our telegram bot</p>
      <p><b>@conote_bot</b></p>
    </div>
    <div class="px-8 pb-8 mt-auto">
      <AboutLine />
    </div>
  </div>
</template>

<style scoped></style>
