<script setup lang="ts">
import { useWebApp } from "vue-tg";

const { initDataUnsafe, close } = useWebApp();
const user = initDataUnsafe.user || "user";

</script>


<template>
    <div>Hello, {{ user }}!</div>
</template>
<style scoped></style>
