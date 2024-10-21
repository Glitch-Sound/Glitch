<script setup lang="ts">
import { defineProps } from 'vue'
import { VIcon } from 'vuetify/components'

import { ItemState, type Item, type PanelRelation } from '@/types/Item'

import { tree } from '@/components/panel/relation'

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()
</script>

<template>
  <div class="svg-container">
    <svg class="overlap-svg" width="100" height="36">
      <!-- <line :x1="tree.e.s" :y1="0" :x2="tree.e.s" :y2="36" stroke="#666" stroke-width="1" />
      <line :x1="tree.f.s" :y1="0" :x2="tree.f.s" :y2="36" stroke="#666" stroke-width="1" />
      <line :x1="tree.s.s" :y1="0" :x2="tree.s.s" :y2="36" stroke="#666" stroke-width="1" />
      <line :x1="tree.t.s" :y1="0" :x2="tree.t.s" :y2="36" stroke="#666" stroke-width="1" />

      <line :x1="tree.e.c" :y1="0" :x2="tree.e.c" :y2="36" stroke="#333" stroke-width="1" />
      <line :x1="tree.f.c" :y1="0" :x2="tree.f.c" :y2="36" stroke="#333" stroke-width="1" />
      <line :x1="tree.s.c" :y1="0" :x2="tree.s.c" :y2="36" stroke="#333" stroke-width="1" />
      <line :x1="tree.t.c" :y1="0" :x2="tree.t.c" :y2="36" stroke="#333" stroke-width="1" /> -->

      <!-- -------------------------------------------------------------------------- -->

      <!-- event -->
      <line
        v-if="props.relation.is_exist_next_event"
        :x1="tree.e.c"
        :y1="0"
        :x2="tree.e.c"
        :y2="18"
        :stroke="tree.e.color"
        :stroke-width="tree.e.w"
      />

      <line
        v-if="props.relation.is_exist_next_event"
        :x1="tree.e.c"
        :y1="18"
        :x2="tree.e.c"
        :y2="36"
        :stroke="tree.e.color"
        :stroke-width="tree.e.w"
      />

      <!-- feature -->
      <line
        v-if="props.relation.is_exist_next_feature"
        :x1="tree.f.c"
        :y1="0"
        :x2="tree.f.c"
        :y2="18"
        :stroke="tree.f.color"
        :stroke-width="tree.f.w"
      />

      <line
        v-if="props.relation.is_exist_next_feature"
        :x1="tree.f.c"
        :y1="18"
        :x2="tree.f.c"
        :y2="36"
        :stroke="tree.f.color"
        :stroke-width="tree.f.w"
      />

      <!-- story:top -->
      <line
        v-if="props.relation.is_top"
        :x1="tree.s.s"
        :y1="0"
        :x2="tree.s.c"
        :y2="18"
        :stroke="tree.s.color"
        :stroke-width="tree.s.w"
      />

      <line
        v-if="!props.relation.is_top"
        :x1="tree.s.c"
        :y1="0"
        :x2="tree.s.c"
        :y2="18"
        :stroke="tree.s.color"
        :stroke-width="tree.s.w"
      />

      <!-- story:bottom -->
      <line
        v-if="props.relation.is_exist_next_story"
        :x1="tree.s.c"
        :y1="18"
        :x2="tree.s.c"
        :y2="36"
        :stroke="tree.s.color"
        :stroke-width="tree.s.w"
      />

      <!-- story:child -->
      <line
        v-if="props.relation.has_child"
        :x1="tree.s.c"
        :y1="18"
        :x2="tree.s.e"
        :y2="36"
        :stroke="tree.t.color"
        :stroke-width="tree.s.w"
      />

      <!-- background:state -->
      <foreignObject x="42" y="3.5" width="30" height="30" opacity="1.0">
        <div xmlns="http://www.w3.org/1999/xhtml">
          <v-icon color="#000000" size="14">mdi-circle</v-icon>
        </div>
      </foreignObject>

      <!-- story:state -->
      <foreignObject x="42" y="3.5" width="30" height="30" opacity="1.0">
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.IDLE">
          <v-icon :color="tree.s.color" size="16">mdi-circle-outline</v-icon>
        </div>
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.RUN">
          <v-icon :color="tree.s.color" size="16">mdi-circle</v-icon>
        </div>
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.ALERT">
          <v-icon :color="tree.s.color" size="16">mdi-alert-circle</v-icon>
        </div>
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.REVIEW">
          <v-icon :color="tree.s.color" size="16">mdi-circle-multiple</v-icon>
        </div>
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.COMPLETE">
          <v-icon :color="tree.s.color" size="16">mdi-circle-slice-8</v-icon>
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
