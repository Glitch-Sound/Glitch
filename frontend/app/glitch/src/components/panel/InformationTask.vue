<script setup lang="ts">
import { defineProps } from 'vue'

import { type Item, TaskType } from '@/types/Item'
import WorkloadLabel from '@/components/common/WorkloadLabel.vue'

const props = defineProps<{
  item: Item
}>()
</script>

<template>
  <div class="align-baseline" v-if="props.item.task_type == TaskType.WORKLOAD">
    <WorkloadLabel :risk="props.item.risk" :workload="props.item.task_workload" />
  </div>

  <div class="align-baseline" v-if="props.item.task_type != TaskType.WORKLOAD">
    {{ props.item.task_number_completed }} / {{ props.item.task_number_total }}
  </div>
</template>

<style scoped></style>
