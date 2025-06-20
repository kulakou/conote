// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import NotFromTelegramPage from "../pages/NotFromTelegramPage.vue";
import WelcomePage from "../pages/WelcomePage.vue";
import { useTelegram } from '@/plugins/telegram'
import { useUserStore } from '@/stores/user'
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

router.beforeEach(async (to, from, next) => {
  const { tg, user, init } = useTelegram()
  const store = useUserStore()

  if (!tg || !user) {
    if (to.path !== '/notg') return next('/notg')
    return next()
  }

  if (!store.initialized) {
    store.setTelegramUser(user)
    await store.checkIfUserExists()
    store.initialized = true
  }

  const isNew = store.isNewUser

  if (!isNew) {
    if (
        to.path === '/' ||
        to.path === '/notg' ||
        to.path === '/welcome' ||
        to.path === '/welcome/code'
    ) return next('/home')
  } else {
    if (
        to.path === '/' ||
        to.path === '/home' ||
        to.path === '/notg'
    ) return next('/welcome')
  }

  next()
})
