<script setup lang="ts">
import { defineProps, onMounted, ref } from 'vue'

import { ItemType, ItemState } from '@/types/Item'
import { type EmitType } from '@/components/common/events'

import StateSelectLabel from '@/components/common/StateSelectLabel.vue'

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
      <StateSelectLabel :state="ItemState.IDLE" />
      <StateSelectLabel :state="ItemState.RUN" />
      <StateSelectLabel :state="ItemState.ALERT" />
      <StateSelectLabel :state="ItemState.REVIEW" />
      <StateSelectLabel :state="ItemState.COMPLETE" />
    </v-chip-group>

    <v-chip-group
      v-model="selected_state_dest"
      v-if="selected_state_src === ItemState.RUN"
      @update:modelValue="emitSelected"
    >
      <StateSelectLabel :state="ItemState.RUN" />
      <StateSelectLabel :state="ItemState.IDLE" />
      <StateSelectLabel :state="ItemState.ALERT" />
      <StateSelectLabel :state="ItemState.REVIEW" />
      <StateSelectLabel :state="ItemState.COMPLETE" />
    </v-chip-group>

    <v-chip-group
      v-model="selected_state_dest"
      v-if="selected_state_src === ItemState.ALERT"
      @update:modelValue="emitSelected"
    >
      <StateSelectLabel :state="ItemState.ALERT" />
      <StateSelectLabel :state="ItemState.IDLE" />
      <StateSelectLabel :state="ItemState.RUN" />
      <StateSelectLabel :state="ItemState.REVIEW" />
      <StateSelectLabel :state="ItemState.COMPLETE" />
    </v-chip-group>

    <v-chip-group
      v-model="selected_state_dest"
      v-if="selected_state_src === ItemState.REVIEW"
      @update:modelValue="emitSelected"
    >
      <StateSelectLabel :state="ItemState.REVIEW" />
      <StateSelectLabel :state="ItemState.IDLE" />
      <StateSelectLabel :state="ItemState.RUN" />
      <StateSelectLabel :state="ItemState.ALERT" />
      <StateSelectLabel :state="ItemState.COMPLETE" />
    </v-chip-group>

    <v-chip-group
      v-model="selected_state_dest"
      v-if="selected_state_src === ItemState.COMPLETE"
      @update:modelValue="emitSelected"
    >
      <StateSelectLabel :state="ItemState.COMPLETE" />
      <StateSelectLabel :state="ItemState.IDLE" />
      <StateSelectLabel :state="ItemState.RUN" />
      <StateSelectLabel :state="ItemState.ALERT" />
      <StateSelectLabel :state="ItemState.REVIEW" />
    </v-chip-group>
  </div>
</template>

<style scoped>
.v-chip-group {
  margin: 0 0 15px 0;
}
</style>
