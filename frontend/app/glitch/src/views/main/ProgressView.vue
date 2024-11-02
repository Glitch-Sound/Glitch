<script setup lang="ts">
import { onMounted } from 'vue'

import useCommonStore from '@/stores/CommonStore'
import ProgressMenuView from '@/views/main/ProgressMenuView.vue'
import ProgressContentView from '@/views/main/ProgressContentView.vue'

const store_common = useCommonStore()

onMounted(() => {
  store_common.setModeProgress()
})
</script>

<template>
  <ProgressMenuView />
  <ProgressContentView />
</template>

<style scoped></style>
