<script setup lang="ts">
import { defineProps, ref } from 'vue'

import type { FeatureUpdate, Item, PanelRelation, StoryCreate } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import RelationFeature from '@/components/panel/RelationFeature.vue'
import MenuFeature from '@/components/panel/MenuFeature.vue'
import UserLabel from '@/components/common/UserLabel.vue'
import CreateStoryDialog from '@/components/dialog/CreateStoryDialog.vue'
import UpdateFeatureDialog from '@/components/dialog/UpdateFeatureDialog.vue'

import { tree } from '@/components/panel/relation'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()

const menu = ref(false)
const dialog_create_story = ref()
const dialog_update_feature = ref()

const openCreateStoryDialog = () => {
  dialog_create_story.value?.open(props.item)
}

const openUpdateFeatureDialog = (data: Item) => {
  dialog_update_feature.value?.open(data)
}

const handleCreateStory = async (data: StoryCreate) => {
  await store_item.createStory(data)
  dialog_create_story.value?.close()
}

const handleUpdateFeature = async (data: FeatureUpdate) => {
  await store_item.updateFeature(data)
  dialog_update_feature.value?.close()
}

const handleDeleteFeature = async (data: FeatureUpdate) => {
  await store_item.deleteFeature(data.rid)
  dialog_update_feature.value?.close()
}
</script>

<template>
  <div class="panel-common">
    <v-row class="align-end ma-0">
      <v-col cols="auto" class="relation">
        <v-menu v-model="menu" activator="parent" offset-y>
          <template v-slot:activator="{ props }">
            <RelationFeature v-bind="props" :item="item" :relation="relation" />
          </template>

          <MenuFeature
            :item="props.item"
            @create-story="openCreateStoryDialog"
            @update-feature="openUpdateFeatureDialog(props.item)"
          />
        </v-menu>
      </v-col>

      <v-col cols="auto" class="type ml-5">
        <v-icon size="small" :color="tree.f.color">mdi-apps</v-icon>
      </v-col>

      <v-col class="title ml-0">
        {{ props.item.title }}
      </v-col>

      <v-col cols="auto" class="user">
        <UserLabel :item="props.item" />
      </v-col>
    </v-row>
  </div>

  <CreateStoryDialog ref="dialog_create_story" @submit="handleCreateStory" />
  <UpdateFeatureDialog
    ref="dialog_update_feature"
    @submit="handleUpdateFeature"
    @delete="handleDeleteFeature"
  />
</template>

<style scoped>
@import '@/components/panel/panel.css';
</style>
