<script setup lang="ts">
import { defineProps, ref } from 'vue'

import type { Item, PanelRelation, TaskUpdate } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import RelationTask from '@/components/panel/RelationTask.vue'
import MenuTask from '@/components/panel/MenuTask.vue'
import UserLabel from '@/components/common/UserLabel.vue'
import InformationTask from '@/components/panel/InformationTask.vue'
import UpdateTaskDialog from '@/components/dialog/UpdateTaskDialog.vue'

import { tree } from '@/components/panel/relation'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()

const menu = ref(false)
const dialog_update_task = ref()

const openUpdateTaskDialog = (data: Item) => {
  dialog_update_task.value?.open(data)
}

const handleUpdateTask = async (data: TaskUpdate) => {
  await store_item.updateTask(data)
  dialog_update_task.value?.close()
}

const handleDeleteTask = async (data: TaskUpdate) => {
  await store_item.deleteTask(data.rid)
  dialog_update_task.value?.close()
}
</script>

<template>
  <div class="panel-common">
    <v-row class="align-end ma-0">
      <v-col cols="auto" class="relation">
        <v-menu v-model="menu" activator="parent" offset-y>
          <template v-slot:activator="{ props }">
            <RelationTask v-bind="props" :item="item" :relation="relation" />
          </template>

          <MenuTask :item="props.item" @update-task="openUpdateTaskDialog(props.item)" />
        </v-menu>
      </v-col>

      <v-col cols="auto" class="type ml-15">
        <v-icon size="small" :color="tree.t.color">mdi-label</v-icon>
      </v-col>

      <v-col class="title ml-0">
        {{ props.item.title }}
      </v-col>

      <v-col cols="auto" class="user">
        <UserLabel :item="props.item" />
      </v-col>

      <v-col cols="auto" class="information">
        <InformationTask :item="props.item" />
      </v-col>
    </v-row>
  </div>

  <UpdateTaskDialog
    ref="dialog_update_task"
    @submit="handleUpdateTask"
    @delete="handleDeleteTask"
  />
</template>

<style scoped>
@import '@/components/panel/panel.css';
</style>
