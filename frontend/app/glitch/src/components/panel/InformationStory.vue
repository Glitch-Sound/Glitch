<script setup lang="ts">
import { defineProps } from 'vue'

import { type Item } from '@/types/Item'

const props = defineProps<{
  item: Item
}>()
</script>

<template>
  <div class="align-baseline">
    {{ props.item.story_datetime_start }}
    <span class="mx-1">~</span>
    {{ props.item.story_datetime_end }}
  </div>
</template>

<style scoped>
@import '@/components/panel/panel.css';
</style>
