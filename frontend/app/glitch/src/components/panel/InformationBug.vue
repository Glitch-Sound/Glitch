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
    <WorkloadLabel :workload="props.item.bug_workload" :risk="props.item.risk" />
  </div>
</template>

<style scoped></style>
