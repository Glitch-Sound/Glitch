<script setup lang="ts">
import { ItemType, type PanelRelation } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import PanelEvent from '@/components/panel/PanelEvent.vue'
import PanelFeature from '@/components/panel/PanelFeature.vue'
import PanelStory from '@/components/panel/PanelStory.vue'
import PanelTask from '@/components/panel/PanelTask.vue'
import PanelBug from '@/components/panel/PanelBug.vue'

const store_item = useItemStore()

const getPanelRelation = (index: number): PanelRelation => {
  const isTop =
    index === 0 ? true : store_item.items[index].type !== store_item.items[index - 1].type

  const isBottom =
    index === store_item.items.length - 1
      ? true
      : store_item.items[index].type !== store_item.items[index + 1].type

  const nextEvent = store_item.items
    .slice(index + 1)
    .findIndex((item) => item.type === ItemType.EVENT)

  const nextFeature = store_item.items
    .slice(index + 1)
    .findIndex((item) => item.type === ItemType.FEATURE)

  const nextPositionStory = store_item.items
    .slice(index + 1)
    .findIndex((item) => item.type === ItemType.STORY)

  console.log('-------------------------------------------')
  console.log('isTop             : ' + isTop)
  console.log('isBottom          : ' + isBottom)
  console.log('nextEvent         : ' + nextEvent)
  console.log(nextEvent !== -1)
  console.log('nextFeature       : ' + nextFeature)
  console.log(nextFeature !== -1)
  console.log('nextPositionStory : ' + nextPositionStory)
  console.log(nextPositionStory !== -1)

  return {
    isTop,
    isBottom,
    isExistNextEvent: nextEvent !== -1,
    isExistNextFeature: nextFeature !== -1,
    isExistNextStory: nextPositionStory !== -1
  }
}
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <template v-for="(item, index) in store_item.items" :key="item.rid">
        <PanelEvent
          v-if="item.type == ItemType.EVENT"
          :item="item"
          :relation="getPanelRelation(index)"
        />

        <PanelFeature
          v-if="item.type == ItemType.FEATURE"
          :item="item"
          :relation="getPanelRelation(index)"
        />

        <PanelStory
          v-if="item.type == ItemType.STORY"
          :item="item"
          :relation="getPanelRelation(index)"
        />

        <PanelTask
          v-if="item.type == ItemType.TASK"
          :item="item"
          :relation="getPanelRelation(index)"
        />

        <PanelBug
          v-if="item.type == ItemType.BUG"
          :item="item"
          :relation="getPanelRelation(index)"
        />
      </template>
    </v-sheet>
  </v-main>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
