import { createPinia } from "pinia";
import { createApp } from "vue";
import "./assets/styles/index.css";
import App from "./App.vue";
import router from "./router";
import { VueTelegramPlugin } from 'vue-tg'

const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(VueTelegramPlugin)
app.use(pinia)
app.mount("#app");