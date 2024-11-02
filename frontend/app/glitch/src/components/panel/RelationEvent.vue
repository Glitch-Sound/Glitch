<script setup lang="ts">
import { defineProps } from 'vue'
import { VIcon } from 'vuetify/components'

import { ItemState, type Item, type PanelRelation } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import { tree } from '@/components/panel/relation'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()
</script>

<template>
  <div class="svg-container">
    <svg class="overlap-svg" :width="tree.e.w" :height="tree.e.h">
      <!-- event:top -->
      <line
        v-if="props.relation.is_top"
        :x1="tree.e.s"
        :y1="tree.e.t"
        :x2="tree.e.c"
        :y2="tree.e.m"
        :stroke="tree.e.color"
        :stroke-width="tree.e.sw"
      />

      <line
        v-if="!props.relation.is_top"
        :x1="tree.e.c"
        :y1="tree.e.t"
        :x2="tree.e.c"
        :y2="tree.e.m"
        :stroke="tree.e.color"
        :stroke-width="tree.e.sw"
      />

      <!-- event:bottom -->
      <line
        v-if="props.relation.is_exist_next_event"
        :x1="tree.e.c"
        :y1="tree.e.m"
        :x2="tree.e.c"
        :y2="tree.e.b"
        :stroke="tree.e.color"
        :stroke-width="tree.e.sw"
      />

      <!-- event:child -->
      <line
        v-if="props.relation.has_child"
        :x1="tree.e.c"
        :y1="tree.e.m"
        :x2="tree.e.e"
        :y2="tree.e.b"
        :stroke="tree.f.color"
        :stroke-width="tree.e.sw"
      />

      <!-- background:state -->
      <foreignObject :x="tree.e.ix" :y="tree.e.iy" :width="tree.e.iw" :height="tree.e.ih">
        <div xmlns="http://www.w3.org/1999/xhtml">
          <v-icon color="#000000" size="16">mdi-circle</v-icon>
        </div>
      </foreignObject>

      <!-- event:state -->
      <foreignObject
        v-if="
          !store_item.isClosed(props.item.rid) ||
          (!store_item.is_enable_closed && store_item.isClosed(props.item.rid))
        "
        :x="tree.e.ix"
        :y="tree.e.iy"
        :width="tree.e.iw"
        :height="tree.e.ih"
      >
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.IDLE">
          <v-icon :color="tree.e.color" size="16">mdi-circle-outline</v-icon>
        </div>
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.RUN">
          <v-icon :color="tree.e.color" size="16">mdi-circle</v-icon>
        </div>
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.ALERT">
          <v-icon :color="tree.e.color" size="16">mdi-alert-circle</v-icon>
        </div>
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.REVIEW">
          <v-icon :color="tree.e.color" size="16">mdi-circle-multiple</v-icon>
        </div>
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.COMPLETE">
          <v-icon :color="tree.e.color" size="16">mdi-circle-slice-8</v-icon>
        </div>
      </foreignObject>
      <foreignObject v-else :x="tree.e.ix" :y="tree.e.iy" :width="tree.e.iw" :height="tree.e.ih">
        <div xmlns="http://www.w3.org/1999/xhtml">
          <v-icon :color="tree.e.color" size="16">mdi-align-vertical-distribute</v-icon>
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
