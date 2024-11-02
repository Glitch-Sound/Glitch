<script setup lang="ts">
import { ref, watch } from 'vue'

import { ItemType, ExtractType, type EventCreate } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import CreateEventDialog from '@/components/dialog/CreateEventDialog.vue'

const store_item = useItemStore()

const dialog_event_create = ref()
const is_enabled_close = ref(true)

watch(is_enabled_close, (is_enabled) => {
  store_item.setEnableClosed(is_enabled)
})

const openCreateEventDialog = () => {
  dialog_event_create.value?.open()
}

const handleCreate = async (data: EventCreate) => {
  await store_item.createEvent(data)
  dialog_event_create.value?.close()
}

const setEnabledType = (type: ItemType) => {
  store_item.setEnabledType(type)
}
</script>

<template>
  <v-navigation-drawer class="no-border" color="background">
    <v-sheet class="navigation">
      <v-list-item class="mb-2">
        <v-btn
          width="250px"
          color="addButton"
          prepend-icon="mdi-plus-circle"
          @click="openCreateEventDialog"
        >
          Event
        </v-btn>
      </v-list-item>

      <v-list-item
        :class="{
          'extract-selected': store_item.type_extract === ExtractType.INCOMPLETE,
          'extract-unselected': store_item.type_extract !== ExtractType.INCOMPLETE
        }"
        @click="store_item.setExtractIncomplete()"
      >
        <v-icon icon="mdi-moon-waning-crescent" />Incomplete
      </v-list-item>

      <v-list-item
        :class="{
          'extract-selected': store_item.type_extract === ExtractType.ALL,
          'extract-unselected': store_item.type_extract !== ExtractType.ALL
        }"
        @click="store_item.setExtractAll()"
      >
        <v-icon icon="mdi-moon-full" />All
      </v-list-item>

      <v-list-item
        :class="{
          'extract-selected': store_item.type_extract === ExtractType.HIGH_RISK,
          'extract-unselected': store_item.type_extract !== ExtractType.HIGH_RISK
        }"
        @click="store_item.setExtractHighRisk()"
      >
        <v-icon icon="mdi-fire" />High Risk
      </v-list-item>

      <v-list-item
        :class="{
          'extract-selected': store_item.type_extract === ExtractType.ALERT,
          'extract-unselected': store_item.type_extract !== ExtractType.ALERT
        }"
        @click="store_item.setExtractAlert()"
      >
        <v-icon icon="mdi-alert-box" />Alert
      </v-list-item>

      <v-list-item
        :class="{
          'extract-selected': store_item.type_extract === ExtractType.ASSIGNMENT,
          'extract-unselected': store_item.type_extract !== ExtractType.ASSIGNMENT
        }"
        @click="store_item.setExtractAssignment()"
      >
        <v-icon icon="mdi-account" />Assignment
      </v-list-item>

      <v-list-item
        :class="{
          'extract-selected': store_item.type_extract === ExtractType.SEARCH,
          'extract-unselected': store_item.type_extract !== ExtractType.SEARCH
        }"
        @click="store_item.setExtractSearchUpdate()"
        :disabled="store_item.extract_search_target === ''"
      >
        <v-icon icon="mdi-magnify" />Search
      </v-list-item>

      <v-list-item
        :class="{
          'extract-selected': store_item.type_extract === ExtractType.RELATION,
          'extract-unselected': store_item.type_extract !== ExtractType.RELATION
        }"
        @click="store_item.setExtractItemUpdate()"
        :disabled="store_item.extract_rid_item === 0"
      >
        <v-icon icon="mdi-relation-many-to-many" />Relation
      </v-list-item>
    </v-sheet>

    <v-sheet class="navigation">
      <v-list-item
        @click="setEnabledType(ItemType.EVENT)"
        :variant="ItemType.EVENT <= store_item.type_enabled ? 'text' : 'plain'"
      >
        <v-icon icon="mdi-calendar-arrow-left" />
        Event
      </v-list-item>

      <v-list-item
        @click="setEnabledType(ItemType.FEATURE)"
        :variant="ItemType.FEATURE <= store_item.type_enabled ? 'text' : 'plain'"
      >
        <v-icon icon="mdi-apps" />
        Feature
      </v-list-item>

      <v-list-item
        @click="setEnabledType(ItemType.STORY)"
        :variant="ItemType.STORY <= store_item.type_enabled ? 'text' : 'plain'"
      >
        <v-icon icon="mdi-arrow-expand-horizontal" />
        Story
      </v-list-item>

      <v-list-item
        @click="setEnabledType(ItemType.TASK)"
        :variant="ItemType.TASK <= store_item.type_enabled ? 'text' : 'plain'"
      >
        <v-icon icon="mdi-label" />
        Task
      </v-list-item>

      <v-list-item
        @click="setEnabledType(ItemType.BUG)"
        :variant="ItemType.BUG <= store_item.type_enabled ? 'text' : 'plain'"
      >
        <v-icon icon="mdi-spider" />
        Bug
      </v-list-item>
    </v-sheet>

    <v-sheet class="information">
      <v-list-item>
        <v-switch color="primary" v-model="is_enabled_close" label="Enable closed" hide-details />
      </v-list-item>
    </v-sheet>
  </v-navigation-drawer>

  <CreateEventDialog ref="dialog_event_create" @submit="handleCreate" />
</template>

<style scoped>
@import '@/assets/main.css';

.v-icon {
  margin: 0 15px 0 0;
}

.extract-selected {
  border-left: 4px solid #196fb3;
}

.extract-unselected {
  border-left: 4px solid transparent;
}
</style>
