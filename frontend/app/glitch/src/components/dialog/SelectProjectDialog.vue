<script setup lang="ts">
import { ref, onMounted } from 'vue'

import { type EmitType } from '@/components/common/events'

import useProjectStore from '@/stores/ProjectStore'

const headers = [
  { title: 'ID', key: 'rid', width: '50px' },
  { title: 'TITLE', key: 'title' },
  { title: 'START', key: 'datetime_start', width: '120px' },
  { title: 'END', key: 'datetime_end', width: '120px' },
  { title: 'USER', key: 'name', width: '100px' }
]

const store_project = useProjectStore()

const dialog = ref(false)

defineExpose({
  open() {
    dialog.value = true
  },
  close() {
    dialog.value = false
  }
})

onMounted(() => {
  store_project.fetchProjects()
})

const emit = defineEmits<EmitType>()
const handleSubmit = async (id_project: number) => {
  store_project.setSelectedProjectID(id_project)
  emit('submit', id_project)
}
</script>

<template>
  <v-dialog v-model="dialog">
    <v-card class="dialog-card">
      <v-card-title>
        <span class="text-h5">Project</span>
      </v-card-title>

      <v-data-table class="ml-5 data-table" :items="store_project.projects" :headers="headers">
        <template v-slot:item="{ item }">
          <tr>
            <td>{{ item.id_project }}</td>
            <td class="title">
              <router-link
                :to="`/project/${item.id_project}`"
                @click="handleSubmit(item.id_project)"
              >
                {{ item.title }}
              </router-link>
            </td>
            <td>{{ item.project_datetime_start }}</td>
            <td>{{ item.project_datetime_end }}</td>
            <td>{{ item.name }}</td>
          </tr>
        </template>
      </v-data-table>

      <template v-slot:actions>
        <v-btn color="primary" class="ms-auto" text="Ok" @click="dialog = false"></v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.dialog-card {
  padding: 10px 20px;
}

.title {
  color: #ffffff;
}
</style>
