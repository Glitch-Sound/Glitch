import { defineStore } from 'pinia'

import type { User, UserCreate, UserUpdate, Login } from '@/types/User'

import UserService from '@/services/UserService'
import { saveLoginUser, loadLoginUser } from '@/stores/LocalStorage'

const service_user = new UserService()

const useUserStore = defineStore('user', {
  state: () => ({
    users: [] as Array<User>,
    users_project: {} as Record<number, User[]>,
    login_user: loadLoginUser() as User | null
  }),
  actions: {
    async fetchUsers() {
      this.users = await service_user.getUsers()
    },
    async createUser(user: UserCreate): Promise<User> {
      const result = await service_user.createUser(user)
      await this.fetchUsers()
      return result
    },
    async updateUser(user: UserUpdate): Promise<User> {
      const result = await service_user.updateUser(user)
      await this.fetchUsers()
      return result
    },
    async deleteUser(rid: number): Promise<void> {
      const result = await service_user.deleteUser(rid)
      await this.fetchUsers()
      return result
    },
    async login(user: Login): Promise<User> {
      const result = await service_user.login(user)
      this.login_user = result
      saveLoginUser(result)
      return result
    },
    async fetchMembers(id_project: number) {
      const members = await service_user.getMembers(id_project)
      this.users_project = {
        ...this.users_project,
        [id_project]: members
      }
    },
    async createMembers(id_project: number, targets: UserCreate[]): Promise<User[]> {
      const result = await service_user.createMembers(id_project, targets)
      await this.fetchUsers()
      return result
    }
  }
})

export default useUserStore
