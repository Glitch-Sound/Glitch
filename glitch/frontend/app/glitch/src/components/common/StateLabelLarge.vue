<script setup lang="ts">
import { defineProps } from 'vue'

import { ItemState } from '@/types/Item'

const props = defineProps<{
  state: ItemState
}>()
</script>

<template>
  <v-chip
    size="normal"
    class="mx-2"
    :value="ItemState.IDLE"
    v-if="props.state == ItemState.IDLE"
    prepend-icon="mdi-circle-outline"
    color="#b0e0e6"
  >
    IDLE
  </v-chip>

  <v-chip
    size="normal"
    class="mx-2"
    :value="ItemState.RUN"
    v-if="props.state == ItemState.RUN"
    prepend-icon="mdi-circle"
    color="#84c69b"
  >
    RUN
  </v-chip>

  <v-chip
    size="normal"
    class="mx-2"
    :value="ItemState.ALERT"
    v-if="props.state == ItemState.ALERT"
    prepend-icon="mdi-alert-box"
    color="#e94560"
  >
    ALERT
  </v-chip>

  <v-chip
    size="normal"
    class="mx-2"
    :value="ItemState.REVIEW"
    v-if="props.state == ItemState.REVIEW"
    prepend-icon="mdi-circle-multiple"
    color="#dece9c"
  >
    REVIEW
  </v-chip>

  <v-chip
    size="normal"
    class="mx-2"
    :value="ItemState.COMPLETE"
    v-if="props.state == ItemState.COMPLETE"
    prepend-icon="mdi-circle-slice-8"
    color="#aaaaaa"
  >
    COMPLETE
  </v-chip>
</template>

<style scoped>
.v-chip {
  margin: 0 10px;
  padding: 2px 10px;
}
</style>
