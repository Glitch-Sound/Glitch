<script setup lang="ts">
import { onMounted, ref } from 'vue'

import type { Project, ProjectCreate, ProjectUpdate } from '@/types/Item'

import useProjectStore from '@/stores/ProjectStore'
import CreateProjectDialog from '@/components/dialog/CreateProjectDialog.vue'
import UpdateProjectDialog from '@/components/dialog/UpdateProjectDialog.vue'

const headers = [
  { title: 'ID', width: ' 50px' },
  { title: 'TITLE', width: '600px' },
  { title: 'START', width: '200px' },
  { title: 'END', width: '200px' },
  { title: 'USER', width: '200px' }
]

const store_project = useProjectStore()

const dialog_project_create = ref()
const dialog_project_update = ref()

onMounted(() => {
  store_project.fetchProjects()
})

const openCreateProjectDialog = () => {
  dialog_project_create.value?.open()
}

const openUpdateProjectDialog = (data: Project) => {
  dialog_project_update.value?.open(data)
}

const handleEntry = async (data: ProjectCreate) => {
  await store_project.createProject(data)
  dialog_project_create.value?.close()
}

const handleUpdate = async (data: ProjectUpdate) => {
  await store_project.updateProject(data)
  dialog_project_update.value?.close()
}

const handleDelete = async (data: ProjectUpdate) => {
  await store_project.deleteProject(data.rid)
  dialog_project_update.value?.close()
}
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <v-btn
        width="150px"
        color="addButton"
        prepend-icon="mdi-plus-circle"
        @click="openCreateProjectDialog"
      >
        Project
      </v-btn>

      <v-data-table class="bg-black" :items="store_project.projects" :headers="headers">
        <template v-slot:item="{ item }">
          <tr>
            <td>{{ item.id_project }}</td>
            <td>{{ item.title }}</td>
            <td>{{ item.project_datetime_start }}</td>
            <td>{{ item.project_datetime_end }}</td>
            <td>{{ item.name }}</td>
            <td>
              <v-btn
                size="small"
                prepend-icon="mdi-pencil"
                variant="outlined"
                @click="openUpdateProjectDialog(item)"
              >
                UPDATE
              </v-btn>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-sheet>
  </v-main>

  <CreateProjectDialog ref="dialog_project_create" @submit="handleEntry" />
  <UpdateProjectDialog ref="dialog_project_update" @submit="handleUpdate" @delete="handleDelete" />
</template>

<style scoped>
@import '@/assets/main.css';
</style>
