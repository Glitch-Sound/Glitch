<script setup lang="ts"></script>

<template>
  <v-navigation-drawer class="no-border" color="background">
    <v-sheet class="navigation">
      <v-list-item>Main</v-list-item>
    </v-sheet>
  </v-navigation-drawer>
</template>

<style scoped>
@import '@/assets/main.css';

.v-icon {
  margin: 0 15px 0 0;
}

.extract-selected {
  border-left: 4px solid #196fb3;
}

.extract-unselected {
  border-left: 4px solid transparent;
}
</style>
