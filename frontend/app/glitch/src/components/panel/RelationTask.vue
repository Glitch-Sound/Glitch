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
    <svg class="overlap-svg" :width="tree.t.w" :height="tree.t.h">
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
        :y1="tree.e.t"
        :x2="tree.e.c"
        :y2="tree.e.m"
        :stroke="tree.e.color"
        :stroke-width="tree.e.sw"
      />

      <line
        v-if="props.relation.is_exist_next_event"
        :x1="tree.e.c"
        :y1="tree.e.m"
        :x2="tree.e.c"
        :y2="tree.e.b"
        :stroke="tree.e.color"
        :stroke-width="tree.e.sw"
      />

      <!-- feature -->
      <line
        v-if="props.relation.is_exist_next_feature"
        :x1="tree.f.c"
        :y1="tree.f.t"
        :x2="tree.f.c"
        :y2="tree.f.m"
        :stroke="tree.f.color"
        :stroke-width="tree.f.sw"
      />

      <line
        v-if="props.relation.is_exist_next_feature"
        :x1="tree.f.c"
        :y1="tree.f.m"
        :x2="tree.f.c"
        :y2="tree.f.b"
        :stroke="tree.f.color"
        :stroke-width="tree.f.sw"
      />

      <!-- story -->
      <line
        v-if="props.relation.is_exist_next_story"
        :x1="tree.s.c"
        :y1="tree.s.t"
        :x2="tree.s.c"
        :y2="tree.s.m"
        :stroke="tree.s.color"
        :stroke-width="tree.s.sw"
      />

      <line
        v-if="props.relation.is_exist_next_story"
        :x1="tree.s.c"
        :y1="tree.s.m"
        :x2="tree.s.c"
        :y2="tree.s.b"
        :stroke="tree.s.color"
        :stroke-width="tree.s.sw"
      />

      <!-- task:top -->
      <line
        v-if="props.relation.is_top"
        :x1="tree.t.s"
        :y1="tree.t.t"
        :x2="tree.t.c"
        :y2="tree.t.m"
        :stroke="tree.t.color"
        :stroke-width="tree.t.sw"
      />

      <line
        v-if="!props.relation.is_top"
        :x1="tree.t.c"
        :y1="tree.t.t"
        :x2="tree.t.c"
        :y2="tree.t.m"
        :stroke="tree.t.color"
        :stroke-width="tree.t.sw"
      />

      <!-- task:bottom -->
      <line
        v-if="!props.relation.is_bottom"
        :x1="tree.t.c"
        :y1="tree.t.m"
        :x2="tree.t.c"
        :y2="tree.t.b"
        :stroke="tree.t.color"
        :stroke-width="tree.t.sw"
      />

      <!-- task:child -->
      <line
        v-if="props.relation.has_child"
        :x1="tree.t.c"
        :y1="tree.t.m + 8"
        :x2="tree.t.c"
        :y2="tree.t.b"
        :stroke="tree.b.color"
        :stroke-width="tree.b.sw"
      />

      <!-- background:state -->
      <foreignObject :x="tree.t.ix" :y="tree.t.iy" :width="tree.t.iw" :height="tree.t.ih">
        <div xmlns="http://www.w3.org/1999/xhtml">
          <v-icon color="#000000" size="16">mdi-circle</v-icon>
        </div>
      </foreignObject>

      <!-- task:state -->
      <foreignObject :x="tree.t.ix" :y="tree.t.iy" :width="tree.t.iw" :height="tree.t.ih">
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.IDLE">
          <v-icon :color="tree.t.color" size="16">mdi-circle-outline</v-icon>
        </div>
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.RUN">
          <v-icon :color="tree.t.color" size="16">mdi-circle</v-icon>
        </div>
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.ALERT">
          <v-icon :color="tree.t.color" size="16">mdi-alert-circle</v-icon>
        </div>
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.REVIEW">
          <v-icon :color="tree.t.color" size="16">mdi-circle-multiple</v-icon>
        </div>
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.COMPLETE">
          <v-icon :color="tree.t.color" size="16">mdi-circle-slice-8</v-icon>
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
