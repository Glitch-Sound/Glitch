<script setup lang="ts">
import { defineProps, ref } from 'vue'

import type { Item, PanelRelation } from '@/types/Item'

import RelationTask from '@/components/panel/RelationTask.vue'
import MenuTask from '@/components/panel/MenuTask.vue'

import { tree } from '@/components/panel/relation'

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()

const menu = ref(false)
</script>

<template>
  <div class="panel-common">
    <v-row class="align-end ma-0">
      <v-col cols="auto" class="relation">
        <v-menu v-model="menu" activator="parent" offset-y>
          <template v-slot:activator="{ props }">
            <RelationTask v-bind="props" :item="item" :relation="relation" />
          </template>

          <MenuTask :item="props.item" />
        </v-menu>
      </v-col>

      <v-col cols="auto" class="type ml-12">
        <v-icon size="small" :color="tree.t.color">mdi-label</v-icon>
      </v-col>

      <v-col class="title ml-0">
        {{ props.item.title }}
      </v-col>

      <v-col cols="auto" class="user">
        {{ props.item.name }}
      </v-col>
    </v-row>
  </div>
</template>

<style scoped>
@import '@/components/panel/panel.css';
</style>
