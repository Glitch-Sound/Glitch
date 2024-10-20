<script setup lang="ts">
import { defineProps } from 'vue'
import { VIcon } from 'vuetify/components'

import type { Item, PanelRelation } from '@/types/Item'

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()
</script>

<template>
  <div class="svg-container">
    <svg class="overlap-svg" width="120" height="36">
      <line x1="0" y1="18" x2="120" y2="18" stroke="#666" stroke-width="1" />
      <line x1="30" y1="0" x2="30" y2="36" stroke="#666" stroke-width="1" />
      <line x1="60" y1="0" x2="60" y2="36" stroke="#666" stroke-width="1" />
      <line x1="90" y1="0" x2="90" y2="36" stroke="#666" stroke-width="1" />

      <line x1="15" y1="0" x2="15" y2="36" stroke="#333" stroke-width="1" />
      <line x1="45" y1="0" x2="45" y2="36" stroke="#333" stroke-width="1" />
      <line x1="75" y1="0" x2="75" y2="36" stroke="#333" stroke-width="1" />
      <line x1="105" y1="0" x2="105" y2="36" stroke="#333" stroke-width="1" />

      <!-- -------------------------------------------------------------------------- -->

      <!-- event -->
      <line
        v-if="props.relation.is_exist_next_event"
        x1="15"
        y1="0"
        x2="15"
        y2="18"
        stroke="red"
        stroke-width="1"
      />

      <line
        v-if="props.relation.is_exist_next_event"
        x1="15"
        y1="18"
        x2="15"
        y2="36"
        stroke="red"
        stroke-width="1"
      />

      <!-- feature:top -->
      <line
        v-if="props.relation.is_top"
        x1="30"
        y1="0"
        x2="45"
        y2="18"
        stroke="red"
        stroke-width="1"
      />

      <line
        v-if="!props.relation.is_top"
        x1="45"
        y1="0"
        x2="45"
        y2="18"
        stroke="red"
        stroke-width="1"
      />

      <!-- feature:child -->
      <line
        v-if="props.relation.has_child"
        x1="45"
        y1="18"
        x2="60"
        y2="36"
        stroke="red"
        stroke-width="1"
      />

      <!-- feature:bottom -->
      <line
        v-if="props.relation.is_exist_next_feature"
        x1="45"
        y1="18"
        x2="45"
        y2="36"
        stroke="red"
        stroke-width="1"
      />

      <!-- feature:state -->
      <foreignObject x="36" y="3.5" width="30" height="30" opacity="0.8">
        <div xmlns="http://www.w3.org/1999/xhtml">
          <v-icon color="white" size="18">mdi-circle</v-icon>
        </div>
      </foreignObject>
    </svg>
  </div>
</template>

<style scoped>
.svg-container {
  display: flex;
}

.overlap-svg {
  margin-top: 0;
  margin-left: 0;
}
</style>
