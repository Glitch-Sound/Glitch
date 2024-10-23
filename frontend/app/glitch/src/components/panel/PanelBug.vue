<script setup lang="ts">
import { defineProps } from 'vue'

import type { Item, PanelRelation } from '@/types/Item'

import RelationBug from '@/components/panel/RelationBug.vue'

import { tree } from '@/components/panel/relation'

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()
</script>

<template>
  <div class="panel-common">
    <v-row class="align-end ma-0">
      <v-col cols="auto" class="relation">
        <RelationBug :item="item" :relation="relation" />
      </v-col>

      <v-col cols="auto" class="type ml-12">
        <v-icon size="small" :color="tree.b.color">mdi-spider</v-icon>
      </v-col>

      <v-col class="title ml-0">
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
