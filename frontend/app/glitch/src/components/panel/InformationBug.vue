<script setup lang="ts">
import { defineProps } from 'vue'

import type { Item } from '@/types/Item'
import WorkloadLabel from '@/components/common/WorkloadLabel.vue'

const props = defineProps<{
  item: Item
}>()
</script>

<template>
  <div class="align-baseline">
    <WorkloadLabel :risk="props.item.risk" :workload="props.item.bug_workload" />
  </div>
</template>

<style scoped></style>
