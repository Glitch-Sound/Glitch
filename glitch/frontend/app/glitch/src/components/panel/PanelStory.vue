<script setup lang="ts">
import { ref, defineProps } from 'vue'
import { useRoute } from 'vue-router'

import type { Item, TaskCreate, BugCreate } from '@/types/Item'
import useUserStore from '@/stores/UserStore'
import useItemStore from '@/stores/ItemStore'
import useSummaryStore from '@/stores/SummaryStore'
import CreateTaskDialog from '@/components/dialog/CreateTaskDialog.vue'
import CreateBugDialog from '@/components/dialog/CreateBugDialog.vue'
import TypeLabel from '@/components/common/TypeLabel.vue'
import StateLabel from '@/components/common/StateLabel.vue'
import TitleLabel from '@/components/common/TitleLabel.vue'
import UserLabel from '@/components/common/UserLabel.vue'
import InformationStory from '@/components/panel/InformationStory.vue'
import DetailStory from '@/components/panel/DetailStory.vue'

const props = defineProps<{
  item: Item
}>()

const route = useRoute()
const store_user = useUserStore()
const store_item = useItemStore()
const store_summary = useSummaryStore()

const expand = ref(false)
const dialogTask = ref(false)
const dialogBug = ref(false)

const dialog_form_data_task = ref<TaskCreate>({
  id_project: Number(route.params.id_project),
  rid_items: props.item.rid,
  rid_users: store_user.login_user?.rid ?? 0,
  title: '',
  detail: '',
  type: 0,
  workload: 0,
  number_completed: 0,
  number_total: 0
})

const dialog_form_data_bug = ref<BugCreate>({
  id_project: Number(route.params.id_project),
  rid_items: props.item.rid,
  rid_users: store_user.login_user?.rid ?? 0,
  title: '',
  detail: '',
  workload: 0
})

const openTaskDialog = () => {
  dialogTask.value = true
}

const openBugDialog = () => {
  dialogBug.value = true
}

const handleTaskSubmit = async (data: TaskCreate) => {
  const result = await store_item.createTask(data)
  store_summary.updateTaskBug(result.rid)
  dialogTask.value = false
}

const handleBugSubmit = async (data: BugCreate) => {
  const result = await store_item.createBug(data)
  store_summary.updateTaskBug(result.rid)
  dialogBug.value = false
}
</script>

<template>
  <div class="panel-common">
    <v-row class="align-baseline">
      <v-col class="state" cols="auto">
        <StateLabel :state="props.item.state" />
      </v-col>

      <v-col class="type type-story" cols="auto">
        <TypeLabel :item="props.item" />
      </v-col>

      <v-col class="title-story" @click="expand = !expand">
        <TitleLabel :item="props.item" />
      </v-col>

      <v-col cols="auto">
        <UserLabel :item="props.item" />
      </v-col>

      <v-col class="information" cols="auto">
        <InformationStory :item="props.item" />
      </v-col>

      <v-col cols="auto">
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn icon variant="text" size="x-small" v-bind="props">
              <v-icon>mdi-plus-thick</v-icon>
            </v-btn>
          </template>

          <v-list>
            <v-list-item-title>
              <v-btn prepend-icon="mdi-label" @click="openTaskDialog()">Task</v-btn>
            </v-list-item-title>
            <v-list-item-title>
              <v-btn prepend-icon="mdi-spider" @click="openBugDialog()">Bug</v-btn>
            </v-list-item-title>
          </v-list>
        </v-menu>
      </v-col>
    </v-row>

    <DetailStory v-bind="{ ...props, expand }" />
  </div>

  <CreateTaskDialog
    :dialog_show="dialogTask"
    :data_form="dialog_form_data_task"
    @update:showDialog="dialogTask = $event"
    @submit="handleTaskSubmit"
  />

  <CreateBugDialog
    :dialog_show="dialogBug"
    :data_form="dialog_form_data_bug"
    @update:showDialog="dialogBug = $event"
    @submit="handleBugSubmit"
  />
</template>

<style scoped>
@import '@/components/panel/panel.css';
</style>
