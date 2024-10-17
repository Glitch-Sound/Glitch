<script setup lang="ts">
import { defineProps, ref } from 'vue'

import type { Item, FeatureCreate } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import CreateFeatureDialog from '@/components/dialog/CreateFeatureDialog.vue'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
}>()

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
    <v-row class="align-baseline">
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
