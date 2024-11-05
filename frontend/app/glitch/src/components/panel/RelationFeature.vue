<script setup lang="ts">
import { defineProps, ref } from 'vue'
import { VIcon } from 'vuetify/components'

import { ItemState, type Item, type PanelRelation } from '@/types/Item'

import useItemStore from '@/stores/ItemStore'
import { tree } from '@/components/panel/relation'

const COLOR_MOUSE_OVER = '#e08dc0'

const store_item = useItemStore()

const props = defineProps<{
  item: Item
  relation: PanelRelation
}>()

const is_hovered = ref(false)

const onMouseOver = () => {
  is_hovered.value = true
}

const onMouseOut = () => {
  is_hovered.value = false
}
</script>

<template>
  <div class="svg-container">
    <svg
      class="overlap-svg"
      :width="tree.f.w"
      :height="tree.f.h"
      @mouseover="onMouseOver"
      @mouseout="onMouseOut"
    >
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

      <!-- feature:top -->
      <line
        v-if="props.relation.is_top"
        :x1="tree.f.s"
        :y1="tree.f.t"
        :x2="tree.f.c"
        :y2="tree.f.m"
        :stroke="tree.f.color"
        :stroke-width="tree.f.sw"
      />

      <line
        v-if="!props.relation.is_top"
        :x1="tree.f.c"
        :y1="tree.f.t"
        :x2="tree.f.c"
        :y2="tree.f.m"
        :stroke="tree.f.color"
        :stroke-width="tree.f.sw"
      />

      <!-- feature:bottom -->
      <line
        v-if="props.relation.is_exist_next_feature"
        :x1="tree.f.c"
        :y1="tree.f.m"
        :x2="tree.f.c"
        :y2="tree.f.b"
        :stroke="tree.f.color"
        :stroke-width="tree.f.sw"
      />

      <!-- feature:child -->
      <line
        v-if="props.relation.has_child"
        :x1="tree.f.c"
        :y1="tree.f.m"
        :x2="tree.f.e"
        :y2="tree.f.b"
        :stroke="tree.s.color"
        :stroke-width="tree.f.sw"
      />

      <!-- background:state -->
      <foreignObject :x="tree.f.ix" :y="tree.f.iy" :width="tree.f.iw" :height="tree.f.ih">
        <div xmlns="http://www.w3.org/1999/xhtml">
          <v-icon color="#000000" size="16">mdi-circle</v-icon>
        </div>
      </foreignObject>

      <!-- feature:state -->
      <foreignObject
        v-if="
          !store_item.isClosed(props.item.rid) ||
          (!store_item.is_enable_closed && store_item.isClosed(props.item.rid))
        "
        :x="tree.f.ix"
        :y="tree.f.iy"
        :width="tree.f.iw"
        :height="tree.f.ih"
      >
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.IDLE">
          <v-icon :color="is_hovered ? COLOR_MOUSE_OVER : tree.f.color" size="16">
            mdi-circle-outline
          </v-icon>
        </div>
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.RUN">
          <v-icon :color="is_hovered ? COLOR_MOUSE_OVER : tree.f.color" size="16">
            mdi-circle
          </v-icon>
        </div>
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.ALERT">
          <v-icon :color="is_hovered ? COLOR_MOUSE_OVER : tree.f.color" size="16">
            mdi-alert-circle
          </v-icon>
        </div>
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.REVIEW">
          <v-icon :color="is_hovered ? COLOR_MOUSE_OVER : tree.f.color" size="16">
            mdi-circle-multiple
          </v-icon>
        </div>
        <div xmlns="http://www.w3.org/1999/xhtml" v-if="props.item.state == ItemState.COMPLETE">
          <v-icon :color="is_hovered ? COLOR_MOUSE_OVER : tree.f.color" size="16">
            mdi-circle-slice-8
          </v-icon>
        </div>
      </foreignObject>
      <foreignObject v-else :x="tree.f.ix" :y="tree.f.iy" :width="tree.f.iw" :height="tree.f.ih">
        <div xmlns="http://www.w3.org/1999/xhtml">
          <v-icon :color="is_hovered ? COLOR_MOUSE_OVER : tree.f.color" size="16">
            mdi-align-vertical-distribute
          </v-icon>
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
