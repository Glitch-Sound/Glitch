<script setup lang="ts">
import { ref, defineProps, onMounted } from 'vue'

import { ItemType, ItemState } from '@/types/Item'
import StateLabelLarge from '@/components/common/StateLabelLarge.vue'
import { type EmitItemSelected } from '@/components/common/events'

const props = defineProps<{
  type: ItemType
  state: ItemState
}>()

const selected_state = ref(ItemState.NONE)
const selected_state_src = ref(ItemState.NONE)

onMounted(() => {
  selected_state_src.value = props.state
})

const emit = defineEmits<EmitItemSelected>()
const emitSelected = () => {
  emit('itemSelected', selected_state.value)
}
</script>

<template>
  <div class="d-flex justify-center">
    <v-chip-group
      v-model="selected_state"
      v-if="selected_state_src === ItemState.IDLE"
      @update:modelValue="emitSelected"
    >
      <StateLabelLarge :state="ItemState.IDLE" />
      <StateLabelLarge :state="ItemState.RUN" />
    </v-chip-group>

    <v-chip-group
      v-model="selected_state"
      v-if="selected_state_src === ItemState.RUN"
      @update:modelValue="emitSelected"
    >
      <StateLabelLarge :state="ItemState.RUN" />
      <StateLabelLarge :state="ItemState.IDLE" />
      <StateLabelLarge :state="ItemState.ALERT" />
      <StateLabelLarge :state="ItemState.REVIEW" />
      <StateLabelLarge :state="ItemState.COMPLETE" />
    </v-chip-group>

    <v-chip-group
      v-model="selected_state"
      v-if="selected_state_src === ItemState.ALERT"
      @update:modelValue="emitSelected"
    >
      <StateLabelLarge :state="ItemState.ALERT" />
      <StateLabelLarge :state="ItemState.IDLE" />
      <StateLabelLarge :state="ItemState.RUN" />
      <StateLabelLarge :state="ItemState.REVIEW" />
    </v-chip-group>

    <v-chip-group
      v-model="selected_state"
      v-if="selected_state_src === ItemState.REVIEW"
      @update:modelValue="emitSelected"
    >
      <StateLabelLarge :state="ItemState.REVIEW" />
      <StateLabelLarge :state="ItemState.IDLE" />
      <StateLabelLarge :state="ItemState.RUN" />
      <StateLabelLarge :state="ItemState.ALERT" />
    </v-chip-group>

    <v-chip-group
      v-model="selected_state"
      v-if="selected_state_src === ItemState.COMPLETE"
      @update:modelValue="emitSelected"
    >
      <StateLabelLarge :state="ItemState.COMPLETE" />
      <StateLabelLarge :state="ItemState.IDLE" />
      <StateLabelLarge :state="ItemState.RUN" />
      <StateLabelLarge :state="ItemState.ALERT" />
    </v-chip-group>
  </div>
</template>

<style scoped>
.v-chip-group {
  margin: 0 0 15px 0;
}
</style>
