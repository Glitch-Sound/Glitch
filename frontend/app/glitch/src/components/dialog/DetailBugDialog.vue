<script setup lang="ts">
import { type Item } from '@/types/Item'

import { useDisplayDialog } from '@/components/dialog/BaseDialog'
import StateLabel from '@/components/common/StateLabel.vue'
import UserLabel from '@/components/common/UserLabel.vue'

import { tree } from '@/components/panel/relation'

const emit = defineEmits(['edit'])
const { dialog, target, editData } = useDisplayDialog(emit)

defineExpose({
  open(item: Item) {
    dialog.value = true
    target.value = item
  },
  close() {
    dialog.value = false
  }
})
</script>

<template>
  <v-dialog v-model="dialog" max-width="1300px">
    <v-card class="mx-auto" width="100%">
      <template v-slot:prepend>
        <v-icon class="dialog-detail-icon-main-title" :color="tree.b.color">mdi-spider</v-icon>
      </template>

      <template v-slot:title>
        <span>{{ target.title }}</span>
      </template>

      <template v-slot:append>
        <StateLabel :state="target.state" />
        <UserLabel :item="target" />
      </template>

      <v-card-text>
        <div class="dialog-detail-title">Detail :</div>
        <div class="dialog-detail-detail">
          {{ target.detail }}
        </div>

        <div class="dialog-detail-title">Result :</div>
        <div class="dialog-detail-detail-end">
          {{ target.result }}
        </div>
      </v-card-text>

      <v-card-actions>
        <v-btn class="ms-auto" @click="editData">
          <v-icon class="dialog-detail-icon-edit">mdi-pencil</v-icon>
          Edit
        </v-btn>
        <v-spacer />
        <v-btn color="primary" class="ms-auto" @click="dialog = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
