<script setup lang="ts">
import { ref } from 'vue'

import LoginUser from '@/components/common/LoginUser.vue'

const title = ref('Glitch')

const link_disabled = ref(true)
const link_project = ref('/')
const link_progress = ref('/')
const link_analyze = ref('/')
</script>

<template>
  <v-app-bar color="#000000">
    <template v-slot:image>
      <v-img gradient="to top, rgba(0, 0, 0, 0), rgba(29, 35, 46, 0.4), rgba(106, 113, 124, 0.7)" />
    </template>

    <v-app-bar-title>
      <div class="d-flex align-center">
        <v-icon color="primary" size="small">mdi-grain</v-icon>
        <span class="ml-2">
          {{ title }}
        </span>
      </div>
    </v-app-bar-title>

    <v-btn icon>
      <router-link to="/">
        <v-icon color="icon">mdi-home</v-icon>
      </router-link>
    </v-btn>

    <v-btn icon :disabled="link_disabled">
      <router-link :to="link_project">
        <v-icon color="icon">mdi-view-list</v-icon>
      </router-link>
    </v-btn>

    <v-btn icon :disabled="link_disabled">
      <router-link :to="link_progress">
        <v-icon color="icon">mdi-account-tag</v-icon>
      </router-link>
    </v-btn>

    <v-btn icon :disabled="link_disabled">
      <router-link :to="link_analyze">
        <v-icon color="icon">mdi-chart-scatter-plot-hexbin</v-icon>
      </router-link>
    </v-btn>

    <v-spacer />

    <div class="mr-3">
      <LoginUser />
    </div>

    <v-btn icon>
      <v-icon color="icon">mdi-magnify</v-icon>
    </v-btn>

    <v-btn icon>
      <router-link to="/setting/main">
        <v-icon color="icon">mdi-cog</v-icon>
      </router-link>
    </v-btn>
  </v-app-bar>
</template>

<style scoped></style>
