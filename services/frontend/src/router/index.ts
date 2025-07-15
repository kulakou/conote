import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import NotFromTelegramPage from '@/pages/NotFromTelegramPage.vue'
import WelcomePage from '@/pages/WelcomePage.vue'
import WelcomeEnterCodePage from '@/pages/WelcomeEnterCodePage.vue'
import { useTelegramUserStore } from '@/stores/telegramUser'
import AllRoomsPage from "../pages/AllRoomsPage.vue";
import RoomPage from "../pages/RoomPage.vue";
import NotePage from "../pages/NotePage.vue";
import CreateRoomPage from "../pages/CreateRoomPage.vue";
import CreateNotePage from "../pages/CreateNotePage.vue";
import EditRoomPage from "../pages/EditRoomPage.vue";
import EditNotePage from "../pages/EditNotePage.vue";
import JoinRoomPage from "../pages/JoinRoomPage.vue";
import ShareAppPage from "../pages/ShareAppPage.vue";

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/welcome', name: 'welcome', component: WelcomePage },
  { path: '/welcome/code', name: 'welcome_code', component: WelcomeEnterCodePage },
  { path: '/home', name: 'home', component: HomePage },
  { path: '/rooms/all', name: 'all_rooms', component: AllRoomsPage },
  { path: '/rooms/join', name: 'rooms_join_page', component: JoinRoomPage },
  { path: '/rooms/:room_id', name: 'room_page', component: RoomPage },
  { path: '/rooms/:room_id/edit', name: 'edit_room_page', component: EditRoomPage },
  { path: '/rooms/:room_id/notes/:note_id', name: 'note_page', component: NotePage },
  { path: '/rooms/:room_id/notes/:note_id/edit', name: 'edit_note_page', component: EditNotePage },
  { path: '/rooms/:room_id/notes/create', name: 'create_note_page', component: CreateNotePage },
  { path: '/rooms/create', name: 'create_room_page', component: CreateRoomPage },
  { path: '/notg', name: 'notg', component: NotFromTelegramPage },
  { path: '/share', name: 'share_page', component: ShareAppPage },
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
