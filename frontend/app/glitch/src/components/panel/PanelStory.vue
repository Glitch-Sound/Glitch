<script setup lang="ts">
import { defineProps, ref } from 'vue'

import type { Item, PanelRelation, TaskCreate } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import RelationStory from '@/components/panel/RelationStory.vue'
import CreateTaskDialog from '@/components/dialog/CreateTaskDialog.vue'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()

const dialog_task_create = ref()

const openCreateTaskDialog = () => {
  dialog_task_create.value?.open(props.item)
}

const handleEntry = async (data: TaskCreate) => {
  await store_item.createTask(data)
  dialog_task_create.value?.close()
}
</script>

<template>
  <div class="panel-common">
    <v-row class="align-center ma-0">
      <v-col cols="auto" class="relation">
        <RelationStory :item="item" :relation="relation" />
      </v-col>

      <v-col class="title">
        {{ props.item.title }}
      </v-col>

      <v-col cols="auto" class="user">
        {{ props.item.name }}
      </v-col>

      <v-col cols="auto" class="button-plus">
        <v-btn icon variant="text" size="x-small" @click="openCreateTaskDialog()">
          <v-icon>mdi-plus-thick</v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </div>

  <CreateTaskDialog ref="dialog_task_create" @submit="handleEntry" />
</template>

<style scoped>
@import '@/components/panel/panel.css';
</style>
