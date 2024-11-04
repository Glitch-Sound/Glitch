<script setup lang="ts">
import { defineProps, ref } from 'vue'

import type { Item, PanelRelation, StoryUpdate, TaskCreate, BugCreate } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import RelationStory from '@/components/panel/RelationStory.vue'
import MenuStory from '@/components/panel/MenuStory.vue'
import UserLabel from '@/components/common/UserLabel.vue'
import InformationStory from '@/components/panel/InformationStory.vue'
import CreateTaskDialog from '@/components/dialog/CreateTaskDialog.vue'
import CreateBugDialog from '@/components/dialog/CreateBugDialog.vue'
import DetailStoryDialog from '@/components/dialog/DetailStoryDialog.vue'
import UpdateStoryDialog from '@/components/dialog/UpdateStoryDialog.vue'

import { tree } from '@/components/panel/relation'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()

const menu = ref(false)
const dialog_create_task = ref()
const dialog_create_bug = ref()
const dialog_detail_story = ref()
const dialog_update_story = ref()

const openCreateTaskDialog = () => {
  dialog_create_task.value?.open(props.item)
}

const openCreateBugDialog = () => {
  dialog_create_bug.value?.open(props.item)
}

const openDetailStoryDialog = (data: Item) => {
  dialog_detail_story.value?.open(data)
}

const openUpdateStoryDialog = (data: Item) => {
  dialog_update_story.value?.open(data)
}

const handleCreateTask = async (data: TaskCreate) => {
  await store_item.createTask(data)
  dialog_create_task.value?.close()
}

const handleCreateBug = async (data: BugCreate) => {
  await store_item.createBug(data)
  dialog_create_bug.value?.close()
}

const handleDetailEditStory = () => {
  dialog_update_story.value?.open(props.item)
}

const handleUpdateStory = async (data: StoryUpdate) => {
  await store_item.updateStory(data)
  dialog_update_story.value?.close()
}

const handleDeleteStory = async (data: StoryUpdate) => {
  await store_item.deleteStory(data.rid)
  dialog_update_story.value?.close()
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
            @detail-story="openDetailStoryDialog(props.item)"
            @update-story="openUpdateStoryDialog(props.item)"
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
        <UserLabel :item="props.item" />
      </v-col>

      <v-col cols="auto" class="information">
        <InformationStory :item="props.item" />
      </v-col>
    </v-row>
  </div>

  <CreateTaskDialog ref="dialog_create_task" @submit="handleCreateTask" />
  <CreateBugDialog ref="dialog_create_bug" @submit="handleCreateBug" />
  <DetailStoryDialog ref="dialog_detail_story" @edit="handleDetailEditStory" />
  <UpdateStoryDialog
    ref="dialog_update_story"
    @submit="handleUpdateStory"
    @delete="handleDeleteStory"
  />
</template>

<style scoped>
@import '@/components/panel/panel.css';
</style>
