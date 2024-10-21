<script setup lang="ts">
import { defineProps } from 'vue'

import type { Item, PanelRelation } from '@/types/Item'

import RelationBug from '@/components/panel/RelationBug.vue'

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()
</script>

<template>
  <div class="panel-common">
    <v-row class="align-center ma-0">
      <v-col cols="auto" class="relation">
        <RelationBug :item="item" :relation="relation" />
      </v-col>

      <v-col class="title ml-12">
        {{ props.item.title }}
      </v-col>

      <v-col cols="auto">
        {{ props.item.name }}
      </v-col>

      <v-col cols="auto">
        <v-btn icon variant="text" size="x-small">
          <v-icon>mdi-plus-thick</v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<style scoped>
@import '@/components/panel/panel.css';
</style>
