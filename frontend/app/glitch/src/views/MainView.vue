<script setup lang="ts">
import { onMounted, ref } from 'vue'

import type { UserCreate } from '@/types/User'

import useUserStore from '@/stores/UserStore'
import CreateAdministratorDialog from '@/components/dialog/CreateAdministratorDialog.vue'

const store_user = useUserStore()

const dialog_admin_create = ref()

onMounted(async () => {
  await store_user.fetchUsers()
  if (store_user.users.length === 0) {
    dialog_admin_create.value?.open()
  }
})

const handleCreate = async (data: UserCreate) => {
  await store_user.createUser(data)
  await store_user.login({
    user: data.user,
    password: data.password
  })
  dialog_admin_create.value?.close()
}
</script>

<template>
  <v-main>
    <v-row justify="center" class="mt-13 mx-auto">
      <v-col cols="auto">
        <v-card class="card">
          <v-card-title>
            <v-icon class="icon">mdi-checkbox-multiple-blank-circle</v-icon>
            <span class="title">Release</span>
          </v-card-title>
          <v-card-text class="detail">...</v-card-text>
        </v-card>
      </v-col>

      <v-col cols="auto">
        <v-card class="card">
          <v-card-title>
            <v-icon class="icon">mdi-help</v-icon>
            <span class="title">How to use</span>
          </v-card-title>
          <v-card-text class="detail">...</v-card-text>
        </v-card>
      </v-col>

      <v-col cols="auto">
        <v-card class="card">
          <v-card-title>
            <v-icon class="icon">mdi-spider</v-icon>
            <span class="title">Bug & Request</span>
          </v-card-title>
          <v-card-text class="detail">...</v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-main>

  <CreateAdministratorDialog ref="dialog_admin_create" @submit="handleCreate" />
</template>

<style scoped>
.card {
  width: 400px;
  background-color: #000000;
}

.icon {
  color: #cfcfcf;
  font-size: 26px;
}

.title {
  color: #cfcfcf;
  font-weight: 900;
  margin-left: 16px;
}

.detail {
  color: #cfcfcf;
  padding: 20px 40px;
}
</style>
