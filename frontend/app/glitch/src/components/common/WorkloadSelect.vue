<script setup lang="ts">
import { ref, onMounted } from 'vue'

import { type EmitType } from '@/components/common/events'

const tickLabels: { [value: number]: string } = {
  1: 'Within an hour',
  3: 'Within half a day',
  7: 'Within a day',
  14: 'Within 2 days',
  21: 'Within 3 days',
  35: 'Within a week'
}
const custom_steps = Object.keys(tickLabels).map((key) => Number(key))

const props = defineProps<{
  workload: number | null
}>()

const slider_value = ref(1)

const emit = defineEmits<EmitType>()
onMounted(() => {
  if (props.workload) {
    slider_value.value = props.workload
  }
  emit('itemSelected', slider_value.value)
})

const emitSelected = () => {
  emit('itemSelected', slider_value.value)
}

const color = () => {
  let value = ''
  switch (slider_value.value) {
    case 1:
      value = '#28a745'
      break
    case 3:
      value = '#3ea956'
      break
    case 7:
      value = '#74c77c'
      break
    case 14:
      value = '#c1d982'
      break
    case 21:
      value = '#e8a44d'
      break
    case 35:
      value = '#bd533f'
      break
  }
  return value
}

const onSliderInput = (value: number) => {
  const closestStep = custom_steps.reduce((prev, curr) => {
    return Math.abs(curr - value) < Math.abs(prev - value) ? curr : prev
  })
  slider_value.value = closestStep
}
</script>

<template>
  <div class="d-flex flex-row justify-center mt-10">
    <p class="slider">
      <v-slider
        v-model="slider_value"
        :min="0"
        :max="36"
        :ticks="custom_steps"
        :color="color()"
        @update:modelValue="onSliderInput"
        @end="emitSelected"
        show-ticks="always"
      />
    </p>
    <p class="value" :style="{ color: color() }">
      {{ tickLabels[slider_value] }}
    </p>
  </div>
</template>

<style scoped>
.slider {
  width: 600px;
}

.value {
  width: 200px;
  margin: 0 0 0 20px;
  font-weight: bold;
}
</style>
