<script setup lang="ts">
import { defineProps, ref } from 'vue'

import type { Item, PanelRelation, StoryCreate } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import RelationFeature from '@/components/panel/RelationFeature.vue'
import CreateStoryDialog from '@/components/dialog/CreateStoryDialog.vue'

import { tree } from '@/components/panel/relation'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()

const dialog_story_create = ref()

const openCreateStoryDialog = () => {
  dialog_story_create.value?.open(props.item)
}

const handleEntry = async (data: StoryCreate) => {
  await store_item.createStory(data)
  dialog_story_create.value?.close()
}
</script>

<template>
  <div class="panel-common">
    <v-row class="align-end ma-0">
      <v-col cols="auto" class="relation">
        <RelationFeature :item="item" :relation="relation" />
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

      <v-col cols="auto" class="button-plus">
        <v-btn icon variant="text" size="x-small" @click="openCreateStoryDialog()">
          <v-icon>mdi-plus-thick</v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </div>

  <CreateStoryDialog ref="dialog_story_create" @submit="handleEntry" />
</template>

<style scoped>
@import '@/components/panel/panel.css';
</style>
