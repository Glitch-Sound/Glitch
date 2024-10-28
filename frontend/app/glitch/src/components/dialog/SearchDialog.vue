<script setup lang="ts">
import { computed, ref } from 'vue'

import useItemStore from '@/stores/ItemStore'

const store_item = useItemStore()

defineExpose({
  open() {
    dialog.value = true
  },
  close() {
    dialog.value = false
  }
})

const dialog = ref(false)
const valid = ref(false)
const target = ref('')

const search = () => {
  store_item.setExtractSearch(target.value)
  dialog.value = false
}

const rules_search = computed(() => [
  (value: string) => !!value || 'Required field',
  (value: string) => value.length >= 2 || 'Please enter at least 2 characters'
])
</script>

<template>
  <v-dialog v-model="dialog" max-width="1000px">
    <v-card>
      <v-card-title>
        <span class="text-h5">Search</span>
      </v-card-title>

      <v-card-text>
        <v-form v-model="valid">
          <v-text-field v-model="target" :rules="rules_search" label="Target" required />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" :disabled="!valid" @click="search">Search</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped></style>
