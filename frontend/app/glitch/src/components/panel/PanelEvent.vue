<script setup lang="ts">
import { defineProps, ref } from 'vue'

import type { Item, PanelRelation, EventUpdate, FeatureCreate } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import RelationEvent from '@/components/panel/RelationEvent.vue'
import MenuEvent from '@/components/panel/MenuEvent.vue'
import UserLabel from '@/components/common/UserLabel.vue'
import CreateFeatureDialog from '@/components/dialog/CreateFeatureDialog.vue'

import { tree } from '@/components/panel/relation'
import UpdateEventDialog from '@/components/dialog/UpdateEventDialog.vue'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()

const menu = ref(false)
const dialog_create_feature = ref()
const dialog_update_event = ref()

const openCreateFeatureDialog = () => {
  dialog_create_feature.value?.open(props.item)
}

const openUpdateEventDialog = (data: Item) => {
  dialog_update_event.value?.open(data)
}

const handleCreateFeature = async (data: FeatureCreate) => {
  await store_item.createFeature(data)
  dialog_create_feature.value?.close()
}

const handleUpdateEvent = async (data: EventUpdate) => {
  await store_item.updateEvent(data)
  dialog_update_event.value?.close()
}

const handleDeleteEvent = async (data: EventUpdate) => {
  await store_item.deleteEvent(data.rid)
  dialog_update_event.value?.close()
}
</script>

<template>
  <div class="panel-common">
    <v-row class="align-end ma-0">
      <v-col cols="auto" class="relation">
        <v-menu v-model="menu" activator="parent" offset-y>
          <template v-slot:activator="{ props }">
            <RelationEvent v-bind="props" :item="item" :relation="relation" />
          </template>

          <MenuEvent
            :item="props.item"
            @create-feature="openCreateFeatureDialog"
            @update-event="openUpdateEventDialog(props.item)"
          />
        </v-menu>
      </v-col>

      <v-col cols="auto" class="type ml-0">
        <v-icon size="small" :color="tree.e.color">mdi-calendar-arrow-left</v-icon>
      </v-col>

      <v-col class="title ml-0">
        {{ props.item.title }}
      </v-col>

      <v-col cols="auto" class="user">
        <UserLabel :item="props.item" />
      </v-col>
    </v-row>
  </div>

  <CreateFeatureDialog ref="dialog_create_feature" @submit="handleCreateFeature" />
  <UpdateEventDialog
    ref="dialog_update_event"
    @submit="handleUpdateEvent"
    @delete="handleDeleteEvent"
  />
</template>
<style scoped>
@import '@/components/panel/panel.css';
</style>
