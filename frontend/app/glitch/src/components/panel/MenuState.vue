<script setup lang="ts">
import { ref, defineEmits } from 'vue'

import { type EmitType } from '@/components/common/events'
import { ItemState } from '@/types/Item'

const submenu = ref(false)

const emit = defineEmits<EmitType>()
const handleUpdateState = (state: ItemState) => {
  emit('update-state', state)
}
</script>

<template>
  <v-menu v-model="submenu" location="end">
    <template v-slot:activator="{ props }">
      <v-list-item v-bind="props" link>
        <template v-slot:prepend>
          <v-icon size="small" class="mr-n4">mdi-state-machine</v-icon>
        </template>
        <v-list-item-title>Update State</v-list-item-title>
        <template v-slot:append>
          <v-icon icon="mdi-menu-right" size="x-small"></v-icon>
        </template>
      </v-list-item>
    </template>

    <v-list class="state">
      <v-list-item link @click="handleUpdateState(ItemState.IDLE)">
        <template v-slot:prepend>
          <v-icon color="#b0c0f6" size="x-small" class="mr-n4">mdi-circle-outline</v-icon>
        </template>
        IDLE
      </v-list-item>

      <v-list-item link @click="handleUpdateState(ItemState.RUN)">
        <template v-slot:prepend>
          <v-icon color="#84c69b" size="x-small" class="mr-n4">mdi-circle</v-icon>
        </template>
        RUN
      </v-list-item>

      <v-list-item link @click="handleUpdateState(ItemState.ALERT)">
        <template v-slot:prepend>
          <v-icon color="#e94560" size="x-small" class="mr-n4">mdi-alert-circle</v-icon>
        </template>
        ALERT
      </v-list-item>

      <v-list-item link @click="handleUpdateState(ItemState.COMPLETE)">
        <template v-slot:prepend>
          <v-icon color="#a9a9a9" size="x-small" class="mr-n4">mdi-circle-slice-8</v-icon>
        </template>
        COMPLETE
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<style scoped>
.state {
  margin-left: 6px;
}
</style>
