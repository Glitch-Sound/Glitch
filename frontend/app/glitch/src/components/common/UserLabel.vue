<script setup lang="ts">
import { defineProps } from 'vue'

import { ItemState, type Item } from '@/types/Item'
import UserIcon from '@/components/common/UserIcon.vue'

const props = defineProps<{
  item: Item
}>()
</script>

<template>
  <div style="display: flex; align-items: center">
    {{ props.item.name }}

    <UserIcon class="ml-2" :rid_users="props.item.rid_users" :name="props.item.name" :size="20" />

    <UserIcon
      v-if="props.item.state == ItemState.REVIEW"
      class="ml-1"
      :rid_users="props.item.rid_users_review"
      :name="props.item.name_review"
      :size="20"
    />

    <div v-if="props.item.state != ItemState.REVIEW" class="ml-6"></div>
  </div>
</template>

<style scoped></style>
