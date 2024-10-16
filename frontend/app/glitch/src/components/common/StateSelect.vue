<script setup lang="ts">
import { defineProps, onMounted, ref } from 'vue'

import { ItemType, ItemState } from '@/types/Item'
import { type EmitType } from '@/components/common/events'

import StateLabel from '@/components/common/StateLabel.vue'

const props = defineProps<{
  type: ItemType
  state: ItemState
}>()

const selected_state_src = ref(ItemState.NONE)
const selected_state_dest = ref(ItemState.NONE)

onMounted(() => {
  selected_state_src.value = props.state
})

const emit = defineEmits<EmitType>()
const emitSelected = () => {
  emit('itemSelected', selected_state_dest.value)
}
</script>

<template>
  <div class="d-flex justify-center">
    <v-chip-group
      v-model="selected_state_dest"
      v-if="selected_state_src === ItemState.IDLE"
      @update:modelValue="emitSelected"
    >
      <StateLabel :state="ItemState.IDLE" />
      <StateLabel :state="ItemState.RUN" />
    </v-chip-group>

    <v-chip-group
      v-model="selected_state_dest"
      v-if="selected_state_src === ItemState.RUN"
      @update:modelValue="emitSelected"
    >
      <StateLabel :state="ItemState.RUN" />
      <StateLabel :state="ItemState.IDLE" />
      <StateLabel :state="ItemState.ALERT" />
      <StateLabel :state="ItemState.REVIEW" />
      <StateLabel :state="ItemState.COMPLETE" />
    </v-chip-group>

    <v-chip-group
      v-model="selected_state_dest"
      v-if="selected_state_src === ItemState.ALERT"
      @update:modelValue="emitSelected"
    >
      <StateLabel :state="ItemState.ALERT" />
      <StateLabel :state="ItemState.IDLE" />
      <StateLabel :state="ItemState.RUN" />
      <StateLabel :state="ItemState.REVIEW" />
    </v-chip-group>

    <v-chip-group
      v-model="selected_state_dest"
      v-if="selected_state_src === ItemState.REVIEW"
      @update:modelValue="emitSelected"
    >
      <StateLabel :state="ItemState.REVIEW" />
      <StateLabel :state="ItemState.IDLE" />
      <StateLabel :state="ItemState.RUN" />
      <StateLabel :state="ItemState.ALERT" />
    </v-chip-group>

    <v-chip-group
      v-model="selected_state_dest"
      v-if="selected_state_src === ItemState.COMPLETE"
      @update:modelValue="emitSelected"
    >
      <StateLabel :state="ItemState.COMPLETE" />
      <StateLabel :state="ItemState.IDLE" />
      <StateLabel :state="ItemState.RUN" />
      <StateLabel :state="ItemState.ALERT" />
    </v-chip-group>
  </div>
</template>

<style scoped>
.v-chip-group {
  margin: 0 0 15px 0;
}
</style>
