<script setup lang="ts">
import { onMounted } from 'vue'

import useUserStore from '@/stores/UserStore'

const headers = [
  { title: 'ID', width: '50px' },
  { title: 'USER', width: '200px' },
  { title: 'NAME', width: '200px' },
  { title: 'IS ADMIN', width: '100px' },
  { title: '', width: '140px' }
]

const store_user = useUserStore()

onMounted(() => {
  store_user.fetchUsers()
})
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <v-btn width="150px" color="addButton" prepend-icon="mdi-plus-circle">User</v-btn>

      <v-data-table class="bg-black" :items="store_user.users" :headers="headers">
        <template v-slot:item="{ item }">
          <tr>
            <td>{{ item.rid }}</td>
            <td>{{ item.user }}</td>
            <td>{{ item.name }}</td>
            <td>
              <v-btn size="small" prepend-icon="mdi-pencil" variant="outlined"> UPDATE </v-btn>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-sheet>
  </v-main>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
