<script setup lang="ts">
import { defineProps, ref } from 'vue'

import type { Item, PanelRelation, BugUpdate } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import RelationBug from '@/components/panel/RelationBug.vue'
import MenuBug from '@/components/panel/MenuBug.vue'
import UserLabel from '@/components/common/UserLabel.vue'
import UpdateBugDialog from '@/components/dialog/UpdateBugDialog.vue'

import { tree } from '@/components/panel/relation'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()

const menu = ref(false)
const dialog_update_bug = ref()

const openUpdateBugDialog = (data: Item) => {
  dialog_update_bug.value?.open(data)
}

const handleUpdateBug = async (data: BugUpdate) => {
  await store_item.updateBug(data)
  dialog_update_bug.value?.close()
}

const handleDeleteBug = async (data: BugUpdate) => {
  await store_item.deleteBug(data.rid)
  dialog_update_bug.value?.close()
}
</script>

<template>
  <div class="panel-common">
    <v-row class="align-end ma-0">
      <v-col cols="auto" class="relation">
        <v-menu v-model="menu" activator="parent" offset-y>
          <template v-slot:activator="{ props }">
            <RelationBug v-bind="props" :item="item" :relation="relation" />
          </template>

          <MenuBug :item="props.item" @update-bug="openUpdateBugDialog(props.item)" />
        </v-menu>
      </v-col>

      <v-col cols="auto" class="type ml-15">
        <v-icon size="small" :color="tree.b.color">mdi-spider</v-icon>
      </v-col>

      <v-col class="title ml-0">
        {{ props.item.title }}
      </v-col>

      <v-col cols="auto" class="user">
        <UserLabel :item="props.item" />
      </v-col>
    </v-row>
  </div>

  <UpdateBugDialog ref="dialog_update_bug" @submit="handleUpdateBug" @delete="handleDeleteBug" />
</template>

<style scoped>
@import '@/components/panel/panel.css';
</style>
