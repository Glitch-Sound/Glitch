<script setup lang="ts">
import { RouterView } from 'vue-router'

import HeaderView from '@/views/HeaderView.vue'
</script>

<template>
  <v-app>
    <HeaderView />
    <RouterView />
  </v-app>
</template>

<style scoped></style>
