<script setup lang="ts">
import { defineProps, ref } from 'vue'

import type { Item, TaskCreate } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import CreateTaskDialog from '@/components/dialog/CreateTaskDialog.vue'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
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
    <v-row class="align-baseline">
      <v-col class="title">
        {{ props.item.title }}
      </v-col>

      <v-col cols="auto">
        {{ props.item.name }}
      </v-col>

      <v-col cols="auto">
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
