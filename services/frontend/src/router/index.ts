import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import NotFromTelegramPage from '@/pages/NotFromTelegramPage.vue'
import WelcomePage from '@/pages/WelcomePage.vue'
import WelcomeEnterCodePage from '@/pages/WelcomeEnterCodePage.vue'
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

router.beforeEach((to, from, next) => {
  const store = useTelegramUserStore()

  const publicPages = ['/welcome', '/welcome/code', '/notg']
  const authRequired = !publicPages.includes(to.path)

  // 1. Нет initData
  if (!store.initDataRaw && to.path !== '/notg') {
    return next('/notg')
  }

  // 2. Невалидный initData
  if (!store.initDataValid && to.path !== '/notg') {
    return next('/notg')
  }

  // 3. Для защищённых страниц
  if (authRequired) {
    if (!store.isAuthenticated && !to.path.startsWith('/welcome')) {
      return next('/welcome')
    }

    if (store.userIsRegistered === false && !['/welcome', '/welcome/code'].includes(to.path)) {
      return next('/welcome')
    }
  }

  next()
})
