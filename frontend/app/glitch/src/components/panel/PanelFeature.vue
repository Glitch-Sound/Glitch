<script setup lang="ts">
import { defineProps, ref } from 'vue'

import type { Item, PanelRelation, StoryCreate } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import RelationFeature from '@/components/panel/RelationFeature.vue'
import MenuFeature from '@/components/panel/MenuFeature.vue'
import CreateStoryDialog from '@/components/dialog/CreateStoryDialog.vue'

import { tree } from '@/components/panel/relation'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()

const menu = ref(false)
const dialog_create_story = ref()

const openCreateStoryDialog = () => {
  dialog_create_story.value?.open(props.item)
}

const handleEntry = async (data: StoryCreate) => {
  await store_item.createStory(data)
  dialog_create_story.value?.close()
}
</script>

<template>
  <div class="panel-common">
    <v-row class="align-end ma-0">
      <v-col cols="auto" class="relation">
        <v-menu v-model="menu" activator="parent" offset-y>
          <template v-slot:activator="{ props }">
            <RelationFeature v-bind="props" :item="item" :relation="relation" />
          </template>

          <MenuFeature :item="props.item" @add-story="openCreateStoryDialog" />
        </v-menu>
      </v-col>

      <v-col cols="auto" class="type ml-4">
        <v-icon size="small" :color="tree.f.color">mdi-apps</v-icon>
      </v-col>

      <v-col class="title ml-0">
        {{ props.item.title }}
      </v-col>

      <v-col cols="auto" class="user">
        {{ props.item.name }}
      </v-col>
    </v-row>
  </div>

  <CreateStoryDialog ref="dialog_create_story" @submit="handleEntry" />
</template>

<style scoped>
@import '@/components/panel/panel.css';
</style>
