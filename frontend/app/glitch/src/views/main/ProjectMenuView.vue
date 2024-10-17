<script setup lang="ts">
import { ExtractType } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'

const store_item = useItemStore()

const openDialog = () => {}
</script>

<template>
  <v-navigation-drawer class="no-border" color="background">
    <v-sheet class="navigation">
      <v-list-item class="mb-1">
        <v-btn width="250px" color="addButton" prepend-icon="mdi-plus-circle" @click="openDialog">
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
  </v-navigation-drawer>
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
