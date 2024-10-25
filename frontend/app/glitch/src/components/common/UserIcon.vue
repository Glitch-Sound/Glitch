<script setup lang="ts">
import Identicon from 'identicon.js'
import * as CryptoJS from 'crypto-js'

import { defineProps, computed } from 'vue'

const props = defineProps<{
  rid_users: number
  name: string
  size: number
}>()

const hash_user = computed(() => {
  return CryptoJS.MD5(props.rid_users + props.name || '').toString()
})

const identicon_user = computed(() => {
  const options = {
    background: [255, 255, 255, 0] as [number, number, number, number],
    format: 'svg' as 'svg'
  }
  return 'data:image/svg+xml;base64,' + new Identicon(hash_user.value, options).toString()
})
</script>

<template>
  <img :src="identicon_user" :width="props.size" :height="props.size" />
</template>

<style scoped></style>
