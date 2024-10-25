<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import useProjectStore from '@/stores/ProjectStore'
import useItemStore from '@/stores/ItemStore'
import ProjectMenuView from '@/views/main/ProjectMenuView.vue'
import ProjectContentView from '@/views/main/ProjectContentView.vue'

const route = useRoute()
const router = useRouter()
const store_project = useProjectStore()
const store_item = useItemStore()

onMounted(() => {
  store_project.setSelectedProjectID(Number(route.params.id_project))
  common()
})

watch(
  () => store_item.is_update,
  async (is_update) => {
    if (is_update) {
      common()
    }
  }
)

const common = () => {
  store_item.fetchItems(router)
}
</script>

<template>
  <ProjectMenuView />
  <ProjectContentView />
</template>

<style scoped></style>
