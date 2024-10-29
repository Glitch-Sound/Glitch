<script setup lang="ts">
import { onMounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router'

import { ItemType } from '@/types/Item'

import useProjectStore from '@/stores/ProjectStore'
import useItemStore from '@/stores/ItemStore'
import useProgressStore from '@/stores/ProgressStore'
import UserHierarchy from '@/components/analyze/UserHierarchy.vue'
import SummaryUserTask from '@/components/analyze/SummaryUserTask.vue'
import SummaryUserBug from '@/components/analyze/SummaryUserBug.vue'
import PanelEvent from '@/components/panel/PanelEvent.vue'
import PanelFeature from '@/components/panel/PanelFeature.vue'
import PanelStory from '@/components/panel/PanelStory.vue'
import PanelTask from '@/components/panel/PanelTask.vue'
import PanelBug from '@/components/panel/PanelBug.vue'

import { getPanelRelation } from '@/views/main/relation'

const route = useRoute()
const store_project = useProjectStore()
const store_item = useItemStore()
const store_progress = useProgressStore()

const rid_user = computed(() => route.params.target)

onMounted(async () => {
  store_progress.setUser(Number(rid_user.value))
  if (store_project.selected_id_project) {
    common()
  }
})

watch(
  () => store_item.is_update,
  async (value_new) => {
    if (value_new) {
      common()
    }
  }
)

watch(
  () => store_progress.rid_users,
  (rid_users) => {
    store_progress.setUser(rid_users)
    common()
  }
)

const common = async () => {
  if (store_project.selected_id_project && store_progress.rid_users) {
    await store_progress.fetchSummariesUser(
      store_project.selected_id_project,
      store_progress.rid_users
    )
    await store_progress.fetchItems(store_project.selected_id_project, store_progress.rid_users)
  }
}
</script>

<template>
  <v-main class="mt-2 ml-n2">
    <v-sheet class="main">
      <v-row>
        <v-col cols="auto" class="d-flex align-center justify-center">
          <UserHierarchy
            :id_project="store_project.selected_id_project"
            :rid_users="store_progress.rid_users"
          />
        </v-col>

        <v-col cols="auto">
          <div class="title">Summary Item</div>
          <SummaryUserTask
            :id_project="store_project.selected_id_project"
            :rid_users="store_progress.rid_users"
          />

          <div class="title">Summary Bug & Alert</div>
          <SummaryUserBug
            :id_project="store_project.selected_id_project"
            :rid_users="store_progress.rid_users"
          />
        </v-col>
      </v-row>

      <div class="mt-10">
        <template v-for="(item, index) in store_item.items" :key="item.rid">
          <PanelEvent
            v-if="item.type == ItemType.EVENT"
            :item="item"
            :relation="getPanelRelation(store_item.items, index)"
          />

          <PanelFeature
            v-if="item.type == ItemType.FEATURE"
            :item="item"
            :relation="getPanelRelation(store_item.items, index)"
          />

          <PanelStory
            v-if="item.type == ItemType.STORY"
            :item="item"
            :relation="getPanelRelation(store_item.items, index)"
          />

          <PanelTask
            v-if="item.type == ItemType.TASK"
            :item="item"
            :relation="getPanelRelation(store_item.items, index)"
          />

          <PanelBug
            v-if="item.type == ItemType.BUG"
            :item="item"
            :relation="getPanelRelation(store_item.items, index)"
          />
        </template>
      </div>
    </v-sheet>
  </v-main>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
