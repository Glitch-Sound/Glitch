<script setup lang="ts">
import { onMounted, watch } from 'vue'

import { ItemType } from '@/types/Item'

import useProjectStore from '@/stores/ProjectStore'
import useItemStore from '@/stores/ItemStore'
import useAnalyzeStore from '@/stores/AnalyzeStore'
import ProjectHierarchy from '@/components/analyze/ProjectHierarchy.vue'
import SummaryProjectTask from '@/components/analyze/SummaryProjectTask.vue'
import SummaryProjectBug from '@/components/analyze/SummaryProjectBug.vue'

import PanelEvent from '@/components/panel/PanelEvent.vue'
import PanelFeature from '@/components/panel/PanelFeature.vue'
import PanelStory from '@/components/panel/PanelStory.vue'
import PanelTask from '@/components/panel/PanelTask.vue'
import PanelBug from '@/components/panel/PanelBug.vue'

import { getPanelRelation } from '@/views/main/relation'

const store_project = useProjectStore()
const store_item = useItemStore()
const store_analyze = useAnalyzeStore()

onMounted(() => {
  common()
})

watch(
  () => store_item.is_update,
  async (value_new) => {
    if (value_new) {
      common()
    }
  }
)

const common = async () => {
  store_item.updated()
  await store_analyze.fetchItems(store_project.selected_id_project)
}
</script>

<template>
  <v-main class="mt-2 ml-n2">
    <v-sheet class="main">
      <v-row>
        <v-col cols="auto" class="d-flex align-center justify-center hierarchy">
          <ProjectHierarchy :id_project="store_project.selected_id_project" />
        </v-col>

        <v-col cols="auto">
          <div class="title">Summary Item</div>
          <SummaryProjectTask :id_project="store_project.selected_id_project" />

          <div class="title">Summary Bug & Alert</div>
          <SummaryProjectBug :id_project="store_project.selected_id_project" />
        </v-col>
      </v-row>

      <div class="mt-10">
        <template v-for="(item, index) in store_analyze.items" :key="item.rid">
          <PanelEvent
            v-if="item.type == ItemType.EVENT"
            :item="item"
            :relation="getPanelRelation(store_analyze.items, index)"
          />

          <PanelFeature
            v-if="item.type == ItemType.FEATURE"
            :item="item"
            :relation="getPanelRelation(store_analyze.items, index)"
          />

          <PanelStory
            v-if="item.type == ItemType.STORY"
            :item="item"
            :relation="getPanelRelation(store_analyze.items, index)"
          />

          <PanelTask
            v-if="item.type == ItemType.TASK"
            :item="item"
            :relation="getPanelRelation(store_analyze.items, index)"
          />

          <PanelBug
            v-if="item.type == ItemType.BUG"
            :item="item"
            :relation="getPanelRelation(store_analyze.items, index)"
          />
        </template>
      </div>
    </v-sheet>
  </v-main>
</template>

<style scoped>
@import '@/assets/main.css';

.hierarchy {
  min-width: 450px;
}
</style>
