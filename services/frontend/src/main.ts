import { createApp } from "vue";
import App from "./App.vue";
import "./assets/styles/index.css";
import router from "./router";
import { VueTelegramPlugin } from "vue-tg";

const app = createApp(App);
app.use(router);
app.use(VueTelegramPlugin);
app.provide("BASE_SITE", "http://localhost:9000");
app.mount("#app");
