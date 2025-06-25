import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import NotFromTelegramPage from "../pages/NotFromTelegramPage.vue";
import WelcomePage from "../pages/WelcomePage.vue";
import WelcomeEnterCodePage from "../pages/WelcomeEnterCodePage.vue";

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/welcome', name: 'welcome', component: WelcomePage },
  { path: '/welcome/code', name: 'welcome_code', component: WelcomeEnterCodePage },
  { path: '/home', name: 'home', component: HomePage },
  { path: '/notg', name: 'notg', component: NotFromTelegramPage },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})
