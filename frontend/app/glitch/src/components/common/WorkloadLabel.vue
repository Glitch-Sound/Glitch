<script setup lang="ts">
import { defineProps } from 'vue'

import { WorkloadType } from '@/types/Item'

const props = defineProps<{
  workload: WorkloadType
}>()
</script>

<template>
  <div class="d-flex flex-row align-baseline justify-start pl-3">
    <template v-if="props.workload == WorkloadType.WITHIN_AN_HOUR">
      <v-icon size="x-small" icon="$vuetify">mdi-hexagon-outline</v-icon>
      <p>1 hour</p>
    </template>

    <template v-if="props.workload == WorkloadType.WITHIN_HALF_A_DAY">
      <v-icon icon="$vuetify">mdi-hexagon-multiple-outline</v-icon>
      <p>Half day</p>
    </template>

    <template v-if="props.workload == WorkloadType.WITHIN_A_DAY">
      <v-icon size="x-small" icon="$vuetify">mdi-card</v-icon>
      <p>1 day</p>
    </template>

    <template v-if="props.workload == WorkloadType.WITHIN_2_DAYS">
      <v-icon size="small" icon="$vuetify">mdi-view-stream</v-icon>
      <p>2 day</p>
    </template>

    <template v-if="props.workload == WorkloadType.WITHIN_3_DAYS">
      <v-icon icon="$vuetify">mdi-view-sequential</v-icon>
      <p>3 day</p>
    </template>

    <template v-if="props.workload == WorkloadType.WITHIN_A_WEEK">
      <v-icon icon="$vuetify">mdi-pentagon</v-icon>
      <p>1 week</p>
    </template>
  </div>
</template>

<style scoped>
.v-icon {
  width: 40px;
  align-items: center;
}

p {
  width: 70px;
  margin-left: 5px;
  text-align: left;
}
</style>
