import type { User } from '@/types/User'

const STORAGE_EXPIRATION_TIME = 12 * 60 * 60 * 1000

const STORAGE_KEY_LOGIN_USER = 'login_user'
const STORAGE_KEY_SELECTED_ID_PROJECT = 'selected_id_project'

export function saveLoginUser(user: User | null) {
  if (user) {
    const data = {
      user,
      timestamp: new Date().getTime()
    }
    localStorage.setItem(STORAGE_KEY_LOGIN_USER, JSON.stringify(data))
  } else {
    localStorage.removeItem(STORAGE_KEY_LOGIN_USER)
  }
}

export function loadLoginUser(): User | null {
  const dataString = localStorage.getItem(STORAGE_KEY_LOGIN_USER)
  if (dataString) {
    const data = JSON.parse(dataString)
    const currentTime = new Date().getTime()

    if (currentTime - data.timestamp > STORAGE_EXPIRATION_TIME) {
      localStorage.removeItem(STORAGE_KEY_LOGIN_USER)
      return null
    }
    return data.user as User
  }
  return null
}

export function saveSelectedProjectID(selected_id_project: number | null) {
  if (selected_id_project) {
    const data = {
      selected_id_project,
      timestamp: new Date().getTime()
    }
    localStorage.setItem(STORAGE_KEY_SELECTED_ID_PROJECT, JSON.stringify(data))
  } else {
    localStorage.removeItem(STORAGE_KEY_SELECTED_ID_PROJECT)
  }
}

export function loadSelectedProjectID(): number | null {
  const dataString = localStorage.getItem(STORAGE_KEY_SELECTED_ID_PROJECT)
  if (dataString) {
    const data = JSON.parse(dataString)
    const currentTime = new Date().getTime()

    if (currentTime - data.timestamp > STORAGE_EXPIRATION_TIME) {
      localStorage.removeItem(STORAGE_KEY_SELECTED_ID_PROJECT)
      return null
    }
    return data.selected_id_project as number
  }
  return null
}
