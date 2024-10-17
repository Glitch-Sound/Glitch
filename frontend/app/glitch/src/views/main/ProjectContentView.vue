<script setup lang="ts">
import { ItemType } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import PanelEvent from '@/components/panel/PanelEvent.vue'
import PanelFeature from '@/components/panel/PanelFeature.vue'
import PanelStory from '@/components/panel/PanelStory.vue'
import PanelTask from '@/components/panel/PanelTask.vue'
import PanelBug from '@/components/panel/PanelBug.vue'

const store_item = useItemStore()
</script>

<template>
  <v-main>
    <v-sheet class="main">
      <template v-for="item in store_item.items" :key="item.rid">
        <PanelEvent v-if="item.type == ItemType.EVENT" :item="item" />
        <PanelFeature v-if="item.type == ItemType.FEATURE" :item="item" />
        <PanelStory v-if="item.type == ItemType.STORY" :item="item" />
        <PanelTask v-if="item.type == ItemType.TASK" :item="item" />
        <PanelBug v-if="item.type == ItemType.BUG" :item="item" />
      </template>
    </v-sheet>
  </v-main>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
