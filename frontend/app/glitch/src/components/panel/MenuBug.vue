<script setup lang="ts">
import { type EmitType } from '@/components/common/events'
import { ItemState, type Item, type BugPriorityUpdate } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import MenuState from '@/components/panel/MenuState.vue'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
}>()

const emit = defineEmits<EmitType>()
const handleUpdateBug = () => {
  emit('update-bug')
}
const handleOpenActivity = () => {
  emit('open-activity')
}

const handleUpdateState = (state: ItemState) => {
  store_item.updateState(props.item.rid, state)
}

const setPriority = async (priority: number) => {
  const data: BugPriorityUpdate = {
    rid: props.item.rid,
    priority: priority
  }
  store_item.updatePriorityBug(data)
}
</script>

<template>
  <v-list>
    <v-list-item link @click="handleOpenActivity">
      <template v-slot:prepend>
        <v-icon size="small" class="mr-n4" color="#97c5b0">mdi-comment-plus-outline</v-icon>
      </template>
      <v-list-item-title>Activity</v-list-item-title>
    </v-list-item>

    <v-list-item link>
      <template v-slot:prepend>
        <v-icon size="small" class="mr-n4">mdi-view-list</v-icon>
      </template>
      <v-list-item-title>Detail</v-list-item-title>
    </v-list-item>

    <v-list-item link @click="handleUpdateBug">
      <template v-slot:prepend>
        <v-icon size="small" class="mr-n4">mdi-pencil</v-icon>
      </template>
      <v-list-item-title>Edit</v-list-item-title>
    </v-list-item>

    <MenuState @update-state="handleUpdateState" />

    <v-list-item link v-if="props.item.priority == 0" @click="setPriority(1)">
      <template v-slot:prepend>
        <v-icon size="small" class="mr-n4">mdi-priority-high</v-icon>
      </template>
      <v-list-item-title>Priority High</v-list-item-title>
    </v-list-item>
    <v-list-item link v-else @click="setPriority(0)">
      <template v-slot:prepend>
        <v-icon size="small" class="mr-n4">mdi-priority-low</v-icon>
      </template>
      <v-list-item-title>Priority Low</v-list-item-title>
    </v-list-item>

    <v-list-item link @click="store_item.setExtractItem(props.item.rid)">
      <template v-slot:prepend>
        <v-icon size="small" class="mr-n4">mdi-relation-one-to-zero-or-many</v-icon>
      </template>
      <v-list-item-title>Jump Relation</v-list-item-title>
    </v-list-item>
  </v-list>
</template>

<style scoped></style>
