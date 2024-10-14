<script setup lang="ts">
import { onMounted } from 'vue'

import useProjectStore from '@/stores/ProjectStore'

const headers = [
  { title: 'ID', width: '50px' },
  { title: 'STATE', width: '100px' },
  { title: 'TITLE' },
  { title: 'START', width: '150px' },
  { title: 'END', width: '150px' },
  { title: 'USER', width: '150px' },
  { title: '', width: '140px' }
]

const store_project = useProjectStore()

onMounted(() => {
  store_project.fetchProjects()
})
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <v-btn width="150px" color="addButton" prepend-icon="mdi-plus-circle">Project</v-btn>

      <v-data-table class="bg-black" :items="store_project.projects" :headers="headers">
        <template v-slot:item="{ item }">
          <tr>
            <td>{{ item.id_project }}</td>
            <td>{{ item.state }}</td>
            <td>{{ item.title }}</td>
            <td>{{ item.project_datetime_start }}</td>
            <td>{{ item.project_datetime_end }}</td>
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
