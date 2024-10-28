<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { type EmitType } from '@/components/common/events'

import useUserStore from '@/stores/UserStore'

const store_user = useUserStore()

const selected_option = ref<number | null>(null)

onMounted(() => {
  store_user.fetchUsers()
})

const emit = defineEmits<EmitType>()
const itemSelected = () => {
  const selectedItem = store_user.users.find((item) => item.rid === selected_option.value)
  if (selectedItem) {
    emit('itemSelected', selectedItem)
  }
}
</script>

<template>
  <v-select
    :items="store_user.users"
    v-model="selected_option"
    label="Reviewer"
    item-title="name"
    item-value="rid"
    required
    @update:modelValue="itemSelected"
  />
</template>

<style scoped></style>
