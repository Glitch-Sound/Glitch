<script setup lang="ts">
import { ref } from 'vue'

import useItemStore from '@/stores/ItemStore'
import { ItemState, type Item } from '@/types/Item'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
}>()

const submenu = ref(false)

const handleUpdateState = (state: ItemState) => {
  store_item.updateState(props.item.rid, state)
}
</script>

<template>
  <v-list>
    <v-list-item link>
      <v-list-item-title>Add Feature</v-list-item-title>
    </v-list-item>

    <v-list-item link>
      <v-list-item-title>Edit</v-list-item-title>
    </v-list-item>

    <v-menu v-model="submenu">
      <template v-slot:activator="{ props }">
        <v-list-item v-bind="props" link>
          <v-list-item-title>Update State</v-list-item-title>
          <template v-slot:append>
            <v-icon icon="mdi-menu-right" size="x-small"></v-icon>
          </template>
        </v-list-item>
      </template>

      <v-list>
        <v-list-item link @click="handleUpdateState(ItemState.IDLE)">IDLE</v-list-item>
        <v-list-item link @click="handleUpdateState(ItemState.RUN)">RUN</v-list-item>
        <v-list-item link @click="handleUpdateState(ItemState.ALERT)">ALERT</v-list-item>
        <v-list-item link @click="handleUpdateState(ItemState.REVIEW)">REVIEW</v-list-item>
        <v-list-item link @click="handleUpdateState(ItemState.COMPLETE)">COMPLETE</v-list-item>
      </v-list>
    </v-menu>

    <v-list-item link>
      <v-list-item-title>Priority high</v-list-item-title>
    </v-list-item>

    <v-list-item link>
      <v-list-item-title>Jump relation</v-list-item-title>
    </v-list-item>
  </v-list>
</template>

<style scoped></style>
