<script setup lang="ts">
import { onMounted, ref } from 'vue'

import type { User, UserCreate, UserUpdate } from '@/types/User'

import useUserStore from '@/stores/UserStore'
import CreateUserDialog from '@/components/dialog/CreateUserDialog.vue'
import UpdateUserDialog from '@/components/dialog/UpdateUserDialog.vue'

const headers = [
  { title: 'ID', width: '50px' },
  { title: 'USER', width: '200px' },
  { title: 'NAME', width: '200px' },
  { title: 'IS ADMIN', width: '100px' },
  { title: '', width: '140px' }
]

const store_user = useUserStore()

const dialog_user_create = ref()
const dialog_user_update = ref()

onMounted(() => {
  store_user.fetchUsers()
})

const openCreateUserDialog = () => {
  dialog_user_create.value?.open()
}

const openUpdateUserDialog = (data: User) => {
  dialog_user_update.value?.open(data)
}

const handleCreate = async (data: UserCreate) => {
  await store_user.createUser(data)
  dialog_user_create.value?.close()
}

const handleUpdate = async (data: UserUpdate) => {
  await store_user.updateUser(data)
  dialog_user_update.value?.close()
}

const handleDelete = async (data: UserUpdate) => {
  await store_user.deleteUser(data.rid)
  dialog_user_update.value?.close()
}
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <v-btn
        width="150px"
        color="addButton"
        prepend-icon="mdi-plus-circle"
        @click="openCreateUserDialog"
      >
        User
      </v-btn>

      <v-data-table class="bg-black" :items="store_user.users" :headers="headers">
        <template v-slot:item="{ item }">
          <tr>
            <td>{{ item.rid }}</td>
            <td>{{ item.user }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.is_admin ? 'True' : 'False' }}</td>
            <td>
              <v-btn
                size="small"
                prepend-icon="mdi-pencil"
                variant="outlined"
                @click="openUpdateUserDialog(item)"
              >
                UPDATE
              </v-btn>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-sheet>
  </v-main>

  <CreateUserDialog ref="dialog_user_create" @submit="handleCreate" />
  <UpdateUserDialog ref="dialog_user_update" @submit="handleUpdate" @delete="handleDelete" />
</template>

<style scoped>
@import '@/assets/main.css';
</style>
