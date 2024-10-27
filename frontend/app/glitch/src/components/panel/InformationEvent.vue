<script setup lang="ts">
import { defineProps } from 'vue'

import type { Item } from '@/types/Item'

const props = defineProps<{
  item: Item
}>()
</script>

<template>
  <div class="align-baseline">
    <v-icon size="x-small" class="mb-1" icon="$vuetify">mdi-menu-left</v-icon>
    {{ props.item.event_datetime_end }}
  </div>
</template>

<style scoped>
@import '@/components/panel/panel.css';
</style>
