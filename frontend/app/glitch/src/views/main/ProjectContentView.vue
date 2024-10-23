<script setup lang="ts">
import { ItemType } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import PanelEvent from '@/components/panel/PanelEvent.vue'
import PanelFeature from '@/components/panel/PanelFeature.vue'
import PanelStory from '@/components/panel/PanelStory.vue'
import PanelTask from '@/components/panel/PanelTask.vue'
import PanelBug from '@/components/panel/PanelBug.vue'

import { getPanelRelation } from '@/views/main/relation'

const store_item = useItemStore()
</script>

<template>
  <v-main class="mt-2">
    <v-sheet class="main">
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
    </v-sheet>
  </v-main>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
