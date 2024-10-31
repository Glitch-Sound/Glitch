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

let latest_closed_item: Item | null = null

const isHide = (item: Item) => {
  if (store_item.isClosed(item.rid)) {
    if (!latest_closed_item || item.type < latest_closed_item.type) {
      latest_closed_item = item
    }
  }

  if (!latest_closed_item) {
    return false
  }

  if (latest_closed_item.type < item.type) {
    return true
  }

  if (latest_closed_item.rid !== item.rid) {
    latest_closed_item = null
  }

  return false
}
</script>

<template>
  <v-main class="mt-2 ml-n2">
    <v-sheet class="main">
      <template v-for="(item, index) in store_item.items" :key="item.rid">
        <PanelEvent
          v-if="item.type == ItemType.EVENT && !isHide(item)"
          :item="item"
          :relation="getPanelRelation(store_item.items, index)"
        />

        <PanelFeature
          v-if="item.type == ItemType.FEATURE && !isHide(item)"
          :item="item"
          :relation="getPanelRelation(store_item.items, index)"
        />

        <PanelStory
          v-if="item.type == ItemType.STORY && !isHide(item)"
          :item="item"
          :relation="getPanelRelation(store_item.items, index)"
        />

        <PanelTask
          v-if="item.type == ItemType.TASK && !isHide(item)"
          :item="item"
          :relation="getPanelRelation(store_item.items, index)"
        />

        <PanelBug
          v-if="item.type == ItemType.BUG && !isHide(item)"
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
