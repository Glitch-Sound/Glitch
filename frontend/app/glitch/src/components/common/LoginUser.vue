<script setup lang="ts">
import { ref } from 'vue'

import type { Login } from '@/types/User'

import useUserStore from '@/stores/UserStore'
import UserIcon from '@/components/common/UserIcon.vue'
import LoginDialog from '@/components/dialog/LoginDialog.vue'

const store_user = useUserStore()

const dialog_login = ref()

const openLoginDialog = () => {
  dialog_login.value?.open()
}

const handleLogin = async (data: Login) => {
  try {
    await store_user.login(data)
    dialog_login.value?.close()
  } catch (error) {
    console.log(error)
  }
}
</script>

<template>
  <div v-if="store_user.login_user == null">
    <v-btn variant="text" @click="openLoginDialog">Login</v-btn>
  </div>
  <div v-else>
    <div class="align-center d-flex">
      <span class="mr-1">
        {{ store_user.login_user.name }}
      </span>

      <v-btn icon size="x-small" @click="openLoginDialog">
        <UserIcon
          :rid_users="store_user.login_user.rid"
          :name="store_user.login_user.name"
          :size="24"
        />
      </v-btn>
    </div>
  </div>

  <LoginDialog ref="dialog_login" @submit="handleLogin" />
</template>

<style scoped></style>
