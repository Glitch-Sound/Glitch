<script setup lang="ts">
import { defineProps } from 'vue'

import type { Item, PanelRelation } from '@/types/Item'

import RelationTask from '@/components/panel/RelationTask.vue'

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()
</script>

<template>
  <div class="panel-common">
    <v-row class="align-center ma-0">
      <v-col cols="auto" class="relation">
        <RelationTask :item="item" :relation="relation" />
      </v-col>

      <v-col class="title">
        {{ props.item.title }}
      </v-col>

      <v-col cols="auto" class="user">
        {{ props.item.name }}
      </v-col>

      <v-col cols="auto" class="button-plus">
        <v-btn icon variant="text" size="x-small">
          <v-icon>mdi-comment-plus-outline</v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<style scoped>
@import '@/components/panel/panel.css';
</style>
