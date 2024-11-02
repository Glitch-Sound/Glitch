<script setup lang="ts">
import { computed } from 'vue'

import { type EmitType } from '@/components/common/events'
import { ItemState, type Item } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import MenuState from '@/components/panel/MenuState.vue'

import { tree } from '@/components/panel/relation'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
}>()

const is_closed = computed(() => store_item.isClosed(props.item.rid))

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

    <v-list-item link @click="store_item.setExtractItem(props.item.rid)">
      <template v-slot:prepend>
        <v-icon size="small" class="mr-n4">mdi-relation-one-to-zero-or-many</v-icon>
      </template>
      <v-list-item-title>Jump Relation</v-list-item-title>
    </v-list-item>

    <v-list-item
      v-if="!is_closed"
      link
      @click="store_item.closeItem(props.item.rid)"
      :disabled="!store_item.is_enable_closed"
    >
      <template v-slot:prepend>
        <v-icon size="small" class="mr-n4">mdi-align-vertical-distribute</v-icon>
      </template>
      <v-list-item-title>Hide</v-list-item-title>
    </v-list-item>
    <v-list-item v-else link @click="store_item.openItem(props.item.rid)">
      <template v-slot:prepend>
        <v-icon size="small" class="mr-n4">mdi-menu</v-icon>
      </template>
      <v-list-item-title>Display</v-list-item-title>
    </v-list-item>
  </v-list>
</template>

<style scoped></style>
