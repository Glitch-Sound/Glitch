<script setup lang="ts">
import { onMounted } from 'vue'

import useCommonStore from '@/stores/CommonStore'
import AnalyzeMenuView from '@/views/main/AnalyzeMenuView.vue'
import AnalyzeContentView from '@/views/main/AnalyzeContentView.vue'

const store_common = useCommonStore()

onMounted(() => {
  store_common.setModeAnalyze()
})
</script>

<template>
  <AnalyzeMenuView />
  <AnalyzeContentView />
</template>

<style scoped></style>
