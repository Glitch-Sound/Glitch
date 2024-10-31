<script setup lang="ts">
import { ItemType, type Item } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import PanelEvent from '@/components/panel/PanelEvent.vue'
import PanelFeature from '@/components/panel/PanelFeature.vue'
import PanelStory from '@/components/panel/PanelStory.vue'
import PanelTask from '@/components/panel/PanelTask.vue'
import PanelBug from '@/components/panel/PanelBug.vue'

import { getPanelRelation } from '@/views/main/relation'

const store_item = useItemStore()

const isHide = (item: Item) => {
  return store_item.isHideItem(item)
}

const isHideTarget = (item: Item) => {
  const latest_hide_type = store_item.latest_hide_type
  if (latest_hide_type === null) {
    return false
  }

  if (latest_hide_type < item.type) {
    return true
  } else {
    store_item.clearLaterstHideType()
    return false
  }
}
</script>

<template>
  <v-main class="mt-2 ml-n2">
    <v-sheet class="main">
      <template v-for="(item, index) in store_item.items" :key="item.rid">
        <PanelEvent
          v-if="item.type == ItemType.EVENT && !isHideTarget(item)"
          :item="item"
          :relation="getPanelRelation(store_item.items, index)"
          :is_hide="isHide(item)"
        />

        <PanelFeature
          v-if="item.type == ItemType.FEATURE && !isHideTarget(item)"
          :item="item"
          :relation="getPanelRelation(store_item.items, index)"
          :is_hide="isHide(item)"
        />

        <PanelStory
          v-if="item.type == ItemType.STORY && !isHideTarget(item)"
          :item="item"
          :relation="getPanelRelation(store_item.items, index)"
          :is_hide="isHide(item)"
        />

        <PanelTask
          v-if="item.type == ItemType.TASK && !isHideTarget(item)"
          :item="item"
          :relation="getPanelRelation(store_item.items, index)"
          :is_hide="isHide(item)"
        />

        <PanelBug
          v-if="item.type == ItemType.BUG && !isHideTarget(item)"
          :item="item"
          :relation="getPanelRelation(store_item.items, index)"
          :is_hide="isHide(item)"
        />
      </template>
    </v-sheet>
  </v-main>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
