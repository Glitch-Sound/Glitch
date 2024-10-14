<script setup lang="ts"></script>

<template>
  <v-main>
    <v-row justify="center" class="mt-13 mx-auto">
      <v-col cols="auto">
        <v-card class="card">
          <v-card-title>
            <v-icon class="icon">mdi-checkbox-multiple-blank-circle</v-icon>
            <span class="title">Release</span>
          </v-card-title>
          <v-card-text class="detail">...</v-card-text>
        </v-card>
      </v-col>

      <v-col cols="auto">
        <v-card class="card">
          <v-card-title>
            <v-icon class="icon">mdi-help</v-icon>
            <span class="title">How to use</span>
          </v-card-title>
          <v-card-text class="detail">...</v-card-text>
        </v-card>
      </v-col>

      <v-col cols="auto">
        <v-card class="card">
          <v-card-title>
            <v-icon class="icon">mdi-spider</v-icon>
            <span class="title">Bug & Request</span>
          </v-card-title>
          <v-card-text class="detail">...</v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-main>
</template>

<style scoped>
.card {
  width: 400px;
  background-color: #000000;
}

.icon {
  color: #cfcfcf;
  font-size: 26px;
}

.title {
  color: #cfcfcf;
  font-weight: 900;
  margin-left: 16px;
}

.detail {
  color: #cfcfcf;
  padding: 20px 40px;
}
</style>
