<script setup lang="ts">
import { defineProps, ref } from 'vue'

import type { Item, PanelRelation, FeatureCreate } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import RelationEvent from '@/components/panel/RelationEvent.vue'
import MenuEvent from '@/components/panel/MenuEvent.vue'
import CreateFeatureDialog from '@/components/dialog/CreateFeatureDialog.vue'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()

const menu = ref(false)
const dialog_feature_create = ref()

const openCreateFeatureDialog = () => {
  dialog_feature_create.value?.open(props.item)
}

const handleEntry = async (data: FeatureCreate) => {
  await store_item.createFeature(data)
  dialog_feature_create.value?.close()
}
</script>

<template>
  <div class="panel-common">
    <v-row class="align-center ma-0">
      <v-col cols="auto" class="relation">
        <v-menu v-model="menu" activator="parent" offset-y>
          <template v-slot:activator="{ props }">
            <RelationEvent v-bind="props" :item="item" :relation="relation" />
          </template>

          <MenuEvent :item="props.item" />
        </v-menu>
      </v-col>

      <v-col class="title">
        {{ props.item.title }}
      </v-col>

      <v-col cols="auto" class="user">
        {{ props.item.name }}
      </v-col>

      <v-col cols="auto" class="button-plus">
        <v-btn icon variant="text" size="x-small" @click="openCreateFeatureDialog()">
          <v-icon>mdi-plus-thick</v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </div>

  <CreateFeatureDialog ref="dialog_feature_create" @submit="handleEntry" />
</template>

<style scoped>
@import '@/components/panel/panel.css';
</style>
