<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import useProjectStore from '@/stores/ProjectStore'
import useProgressStore from '@/stores/ProgressStore'
import UserIcon from '@/components/common/UserIcon.vue'

const route = useRoute()
const router = useRouter()
const store_project = useProjectStore()
const store_progress = useProgressStore()

onMounted(() => {
  if (store_project.selected_id_project) {
    store_progress.fetchUsers(store_project.selected_id_project)
  }
})

const changeTarget = (rid_users: number) => {
  const idProject = route.params.id_project
  router.push(`/progress/${idProject}/${rid_users}`)
  store_progress.setUser(rid_users)
}
</script>

<template>
  <v-navigation-drawer class="no-border" color="background">
    <v-sheet class="navigation">
      <template v-for="user in store_progress.users" :key="user.rid">
        <v-list-item
          :class="{
            'extract-selected': store_progress.rid_users === user.rid,
            'extract-unselected': store_progress.rid_users !== user.rid
          }"
          @click="changeTarget(user.rid)"
        >
          <div style="display: flex; align-items: center">
            <UserIcon class="mr-3" :rid_users="user.rid" :name="user.name" :size="22" />
            {{ user.name }}
          </div>
        </v-list-item>
      </template>
    </v-sheet>
  </v-navigation-drawer>
</template>

<style scoped>
@import '@/assets/main.css';

.v-icon {
  margin: 0 15px 0 0;
}

.extract-selected {
  border-left: 4px solid #196fb3;
}

.extract-unselected {
  border-left: 4px solid transparent;
}
</style>
