import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import NotFromTelegramPage from "../pages/NotFromTelegramPage.vue";
import WelcomePage from "../pages/WelcomePage.vue";
import WelcomeEnterCodePage from "../pages/WelcomeEnterCodePage.vue";
import { useTelegramUserStore } from '@/stores/telegramUser'

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
  const store = useTelegramUserStore()

  // No Telegram check
  if (!store.initDataRaw && to.path !== '/notg') {
    return next('/notg')
  }

  const publicPages = ['/welcome', '/welcome/code', '/notg']
  const authRequired = !publicPages.includes(to.path)

  if (!authRequired) {
    return next()
  }

  if (!store.isAuthenticated) {
    return next('/welcome')
  }

  // Already verified?
  if (store.userIsRegistered !== undefined) {
    if (!store.userIsRegistered && !to.path.startsWith('/welcome')) {
      return next('/welcome')
    }
    return next()
  }

  // Verify on backend
  const isRegistered = await store.verifyOnBackend()
  store.userIsRegistered = isRegistered

  if (!isRegistered && !to.path.startsWith('/welcome')) {
    return next('/welcome')
  }

  next()
})
