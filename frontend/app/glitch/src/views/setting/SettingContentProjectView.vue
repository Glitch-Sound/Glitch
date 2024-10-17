<script setup lang="ts">
import { onMounted, ref } from 'vue'

import type { Project, ProjectCreate, ProjectUpdate } from '@/types/Item'

import useProjectStore from '@/stores/ProjectStore'
import CreateProjectDialog from '@/components/dialog/CreateProjectDialog.vue'
import UpdateProjectDialog from '@/components/dialog/UpdateProjectDialog.vue'

const headers = [
  { title: 'ID', width: ' 50px' },
  { title: 'STATE', width: '100px' },
  { title: 'TITLE' },
  { title: 'START', width: '200px' },
  { title: 'END', width: '200px' },
  { title: 'USER', width: '200px' }
]

const store_project = useProjectStore()

const dialog_entry = ref()
const dialog_update = ref()

onMounted(() => {
  store_project.fetchProjects()
})

const openEntryDialog = () => {
  dialog_entry.value?.open()
}

const openUpdateDialog = (data: Project) => {
  dialog_update.value?.open(data)
}

const handleEntry = async (data: ProjectCreate) => {
  await store_project.createProject(data)
  dialog_entry.value?.close()
}

const handleUpdate = async (data: ProjectUpdate) => {
  await store_project.updateProject(data)
  dialog_update.value?.close()
}

const handleDelete = async (data: ProjectUpdate) => {
  await store_project.deleteProject(data.rid)
  dialog_update.value?.close()
}
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <v-btn
        width="150px"
        color="addButton"
        prepend-icon="mdi-plus-circle"
        @click="openEntryDialog"
      >
        Project
      </v-btn>

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
              <v-btn
                size="small"
                prepend-icon="mdi-pencil"
                variant="outlined"
                @click="openUpdateDialog(item)"
              >
                UPDATE
              </v-btn>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-sheet>
  </v-main>

  <CreateProjectDialog ref="dialog_entry" @submit="handleEntry" />
  <UpdateProjectDialog ref="dialog_update" @submit="handleUpdate" @delete="handleDelete" />
</template>

<style scoped>
@import '@/assets/main.css';
</style>
