<script setup lang="ts">
import { onMounted, ref } from 'vue'

import type { Project, ProjectCreate, ProjectUpdate } from '@/types/Item'
import type { MemberCreate } from '@/types/User'

import useProjectStore from '@/stores/ProjectStore'
import CreateProjectDialog from '@/components/dialog/CreateProjectDialog.vue'
import UpdateProjectDialog from '@/components/dialog/UpdateProjectDialog.vue'
import MemberDialog from '@/components/dialog/MemberDialog.vue'

const headers = [
  { title: 'ID', width: ' 50px' },
  { title: 'TITLE', width: '800px' },
  { title: 'START', width: '150px' },
  { title: 'END', width: '150px' },
  { title: 'USER', width: '200px' }
]

const store_project = useProjectStore()

const dialog_project_create = ref()
const dialog_project_update = ref()
const dialog_member = ref()

onMounted(() => {
  store_project.fetchProjects()
})

const openCreateProjectDialog = () => {
  dialog_project_create.value?.open()
}

const openUpdateProjectDialog = (data: Project) => {
  dialog_project_update.value?.open(data)
}

const openMemberDialog = (data: Project) => {
  dialog_member.value?.open(data)
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

const handleEntryMember = async (data: MemberCreate[]) => {
  console.log(data)
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
              <div class="d-flex">
                <v-btn
                  size="small"
                  prepend-icon="mdi-pencil"
                  variant="outlined"
                  class="me-5"
                  @click="openUpdateProjectDialog(item)"
                >
                  UPDATE
                </v-btn>
                <v-btn
                  size="small"
                  prepend-icon="mdi-account-supervisor"
                  variant="outlined"
                  @click="openMemberDialog(item)"
                >
                  MEMBER
                </v-btn>
              </div>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-sheet>
  </v-main>

  <CreateProjectDialog ref="dialog_project_create" @submit="handleEntry" />
  <UpdateProjectDialog ref="dialog_project_update" @submit="handleUpdate" @delete="handleDelete" />
  <MemberDialog ref="dialog_member" @submit="handleEntryMember" />
</template>

<style scoped>
@import '@/assets/main.css';
</style>
