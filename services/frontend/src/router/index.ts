import { createRouter, createWebHistory } from 'vue-router';
import Welcome from "../views/Welcome.vue"
import WelcomeEnterCode from "../views/WelcomeEnterCode.vue"
import Home from "../views/Home.vue";
import TGUnauthorized from "../views/TGUnauthorized.vue";
import Base from "../views/Base.vue";

const routes = [
  { path: '/', component: Base },
  { path: '/welcome', component: Welcome },
  { path: '/welcome/code', component: WelcomeEnterCode },
  { path: '/home', component: Home },
  { path: '/notg', component: TGUnauthorized },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
