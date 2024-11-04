<script setup lang="ts">
import { defineProps } from 'vue'

import { ItemState } from '@/types/Item'

const props = defineProps<{
  state: ItemState
}>()
</script>

<template>
  <v-chip size="small" v-if="props.state == ItemState.IDLE" prepend-icon="mdi-circle-outline">
    IDLE
  </v-chip>

  <v-chip size="small" v-if="props.state == ItemState.RUN" prepend-icon="mdi-circle"> RUN </v-chip>

  <v-chip size="small" v-if="props.state == ItemState.ALERT" prepend-icon="mdi-alert-box">
    ALERT
  </v-chip>

  <v-chip size="small" v-if="props.state == ItemState.REVIEW" prepend-icon="mdi-circle-multiple">
    REVIEW
  </v-chip>

  <v-chip size="small" v-if="props.state == ItemState.COMPLETE" prepend-icon="mdi-circle-slice-8">
    COMPLETE
  </v-chip>
</template>

<style scoped>
.v-chip {
  margin: 0 10px 0 0;
  padding: 0 14px;
}
</style>
