<script setup lang="ts">
import { defineProps } from 'vue'

import { ItemState } from '@/types/Item'

const props = defineProps<{
  state: ItemState
}>()
</script>

<template>
  <v-chip
    size="x-small"
    class="mx-1"
    :value="ItemState.IDLE"
    v-if="props.state == ItemState.IDLE"
    prepend-icon="mdi-circle-outline"
    color="#b0e0e6"
  >
    IDLE
  </v-chip>

  <v-chip
    size="x-small"
    class="mx-1"
    :value="ItemState.RUN"
    v-if="props.state == ItemState.RUN"
    prepend-icon="mdi-circle"
    color="#84c69b"
  >
    RUN
  </v-chip>

  <v-chip
    size="x-small"
    class="mx-1"
    :value="ItemState.ALERT"
    v-if="props.state == ItemState.ALERT"
    prepend-icon="mdi-alert-box"
    color="#e94560"
  >
    ALERT
  </v-chip>

  <v-chip
    size="x-small"
    class="mx-1"
    :value="ItemState.REVIEW"
    v-if="props.state == ItemState.REVIEW"
    prepend-icon="mdi-circle-multiple"
    color="#dece9c"
  >
    REVIEW
  </v-chip>

  <v-chip
    size="x-small"
    class="mx-1"
    :value="ItemState.COMPLETE"
    v-if="props.state == ItemState.COMPLETE"
    prepend-icon="mdi-circle-slice-8"
    color="#a9a9a9"
  >
    COMPLETE
  </v-chip>
</template>

<style scoped></style>
