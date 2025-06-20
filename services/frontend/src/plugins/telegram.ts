let tg: any = null
let user: any = null

function getMockTelegram() {
  return {
    WebApp: {
      initDataUnsafe: {
        user: {
          id: 123456,
          username: 'bbtmdrew',
          first_name: 'Andrey'
        }
      },
      expand: () => {},
      ready: () => {}
    }
  }
}

export function useTelegram() {
  if (!tg) {
    tg = import.meta.env.DEV
      ? getMockTelegram().WebApp
      : window.Telegram?.WebApp

    user = tg?.initDataUnsafe?.user ?? null
  }

  // tg = window.Telegram?.WebApp
  // user = tg?.initDataUnsafe?.user ?? null

  const init = () => {
    tg?.expand?.()
    tg?.ready?.()
  }

  return { tg: tg, user: user, init }
}