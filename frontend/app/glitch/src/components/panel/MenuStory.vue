<script setup lang="ts">
import { type EmitType } from '@/components/common/events'
import { ItemState, type Item } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import MenuState from '@/components/panel/MenuState.vue'

import { tree } from '@/components/panel/relation'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
}>()

const emit = defineEmits<EmitType>()
const handleAddTask = () => {
  emit('add-task')
}
const handleAddBug = () => {
  emit('add-bug')
}
const handleUpdateStory = () => {
  emit('update-story')
}

const handleUpdateState = (state: ItemState) => {
  store_item.updateState(props.item.rid, state)
}
</script>

<template>
  <v-list>
    <v-list-item link @click="handleAddTask">
      <template v-slot:prepend>
        <v-icon size="small" class="mr-n4" :color="tree.t.color">mdi-label</v-icon>
      </template>
      <v-list-item-title>Add Task</v-list-item-title>
    </v-list-item>

    <v-list-item link @click="handleAddBug">
      <template v-slot:prepend>
        <v-icon size="small" class="mr-n4" :color="tree.b.color">mdi-spider</v-icon>
      </template>
      <v-list-item-title>Add Bug</v-list-item-title>
    </v-list-item>

    <v-list-item link>
      <template v-slot:prepend>
        <v-icon size="small" class="mr-n4">mdi-view-list</v-icon>
      </template>
      <v-list-item-title>Detail</v-list-item-title>
    </v-list-item>

    <v-list-item link @click="handleUpdateStory">
      <template v-slot:prepend>
        <v-icon size="small" class="mr-n4">mdi-pencil</v-icon>
      </template>
      <v-list-item-title>Edit</v-list-item-title>
    </v-list-item>

    <MenuState @update-state="handleUpdateState" />

    <v-list-item link>
      <template v-slot:prepend>
        <v-icon size="small" class="mr-n4">mdi-relation-one-to-zero-or-many</v-icon>
      </template>
      <v-list-item-title>Jump Relation</v-list-item-title>
    </v-list-item>
  </v-list>
</template>

<style scoped></style>
