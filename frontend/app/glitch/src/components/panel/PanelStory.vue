<script setup lang="ts">
import { defineProps, ref } from 'vue'

import type { Item, PanelRelation, TaskCreate, BugCreate } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import RelationStory from '@/components/panel/RelationStory.vue'
import MenuStory from '@/components/panel/MenuStory.vue'
import CreateTaskDialog from '@/components/dialog/CreateTaskDialog.vue'
import CreateBugDialog from '@/components/dialog/CreateBugDialog.vue'

import { tree } from '@/components/panel/relation'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()

const menu = ref(false)
const dialog_create_task = ref()
const dialog_create_bug = ref()

const openCreateTaskDialog = () => {
  dialog_create_task.value?.open(props.item)
}

const openCreateBugDialog = () => {
  dialog_create_bug.value?.open(props.item)
}

const handleEntryTask = async (data: TaskCreate) => {
  await store_item.createTask(data)
  dialog_create_task.value?.close()
}

const handleEntryBug = async (data: BugCreate) => {
  await store_item.createBug(data)
  dialog_create_bug.value?.close()
}
</script>

<template>
  <div class="panel-common">
    <v-row class="align-end ma-0">
      <v-col cols="auto" class="relation">
        <v-menu v-model="menu" activator="parent" offset-y>
          <template v-slot:activator="{ props }">
            <RelationStory v-bind="props" :item="item" :relation="relation" />
          </template>

          <MenuStory
            :item="props.item"
            @add-task="openCreateTaskDialog"
            @add-bug="openCreateBugDialog"
          />
        </v-menu>
      </v-col>

      <v-col cols="auto" class="type ml-10">
        <v-icon size="small" :color="tree.s.color">mdi-arrow-expand-horizontal</v-icon>
      </v-col>

      <v-col class="title ml-0">
        {{ props.item.title }}
      </v-col>

      <v-col cols="auto" class="user">
        {{ props.item.name }}
      </v-col>
    </v-row>
  </div>

  <CreateTaskDialog ref="dialog_create_task" @submit="handleEntryTask" />
  <CreateBugDialog ref="dialog_create_bug" @submit="handleEntryBug" />
</template>

<style scoped>
@import '@/components/panel/panel.css';
</style>
